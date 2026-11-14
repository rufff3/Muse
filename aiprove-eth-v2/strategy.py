"""
AIProve bounty: eth-pnl-fixed — v2 strategy (designed by GPT gpt-6.1-sol, iteration 7, final).
Strategy: Warm-Up-Gated Asymmetric Donchian Trend Capture.

Spec (from GPT output v7, implemented exactly):
- Warm-up: NO entries before bar 720.
- Short entry: fresh 90-bar breakdown (prior-bars-only channel, 0 buffer):
  close[i] < L90(i) and R90(i) <= -0.50%, and bar i-1 did NOT satisfy both
  the breakdown and the return condition (freshness).
- Long entry: fresh 120-bar breakout (prior-bars-only channel, 0 buffer):
  close[i] > H120(i); close[i] > EMA240; EMA240 rising over 30 bars;
  R240(i) >= +0.75%; and bar i-1 did NOT satisfy all four long conditions.
- Exit: 1.25% trailing retracement from the most favorable close since the
  fill bar. No ATR stop, no EMA-reversal exit.
- Cooldown 45 bars after an exit signal; first eligible entry bar e+46.
- Hard cap: max 4 completed round trips.
- Fills at next bar's open (backtester handles it).

Cost model identical to v1 (challenge assumptions, documented):
  taker fee 5 bp/fill; slippage 2 bp base + 10 bp * (qty/bar_volume), cap 20 bp;
  capital $10,000, 1x, fixed notional, long/short.
"""

import numpy as np
import pandas as pd

WARMUP = 720
LB_SHORT = 90
LB_LONG = 120
EMA_REGIME = 240
SLOPE_LB_LONG = 30
RET_SHORT = -0.005
RET_LONG = 0.0075
TRAIL = 0.0125
COOLDOWN = 45
MAX_ROUND_TRIPS = 4

CAPITAL = 10_000.0
FEE_BPS = 5.0
SLIP_BASE_BPS = 2.0
SLIP_SIZE_BPS = 10.0
SLIP_CAP_BPS = 20.0


def _ema(close: np.ndarray, n: int) -> np.ndarray:
    out = np.full(len(close), np.nan)
    alpha = 2.0 / (n + 1)
    seed = close[:n].mean()
    out[n - 1] = seed
    prev = seed
    for i in range(n, len(close)):
        prev = alpha * close[i] + (1 - alpha) * prev
        out[i] = prev
    return out


def generate_signals(df: pd.DataFrame) -> np.ndarray:
    close = df["close"].to_numpy(dtype=float)
    high = df["high"].to_numpy(dtype=float)
    low = df["low"].to_numpy(dtype=float)
    n = len(df)
    ema240 = _ema(close, EMA_REGIME)

    def ret(i: int, L: int) -> float:
        return close[i] / close[i - L] - 1.0

    def chan_high(i: int, L: int) -> float:
        # max high of the L PRIOR bars i-L .. i-1 (current bar excluded)
        return high[max(0, i - L):i].max()

    def chan_low(i: int, L: int) -> float:
        return low[max(0, i - L):i].min()

    def short_cond(i: int) -> bool:
        return close[i] < chan_low(i, LB_SHORT) and ret(i, LB_SHORT) <= RET_SHORT

    def long_cond(i: int) -> bool:
        return (
            close[i] > chan_high(i, LB_LONG)
            and close[i] > ema240[i]
            and ema240[i] > ema240[i - SLOPE_LB_LONG]
            and ret(i, 240) >= RET_LONG
        )

    signals = np.zeros(n, dtype=int)
    pos = 0
    extreme = None
    last_exit_bar = None
    completed_rts = 0

    def in_cooldown(i: int) -> bool:
        return last_exit_bar is not None and i <= last_exit_bar + COOLDOWN

    def long_ok(i: int) -> bool:
        if completed_rts >= MAX_ROUND_TRIPS or in_cooldown(i) or i < WARMUP:
            return False
        return long_cond(i) and not long_cond(i - 1)

    def short_ok(i: int) -> bool:
        if completed_rts >= MAX_ROUND_TRIPS or in_cooldown(i) or i < WARMUP:
            return False
        return short_cond(i) and not short_cond(i - 1)

    for i in range(1, n):
        if i == n - 1:
            signals[i] = 0
            pos = 0
            continue
        if pos == 0:
            if long_ok(i) and short_ok(i):
                signals[i] = 0
            elif long_ok(i):
                pos = 1
                extreme = None
                signals[i] = 1
            elif short_ok(i):
                pos = -1
                extreme = None
                signals[i] = -1
            else:
                signals[i] = 0
        else:
            if extreme is None:
                extreme = close[i]
            if pos == 1:
                extreme = max(extreme, close[i])
                if close[i] <= (1 - TRAIL) * extreme:
                    pos = 0
                    completed_rts += 1
                    last_exit_bar = i
                    signals[i] = 0
                    continue
            else:
                extreme = min(extreme, close[i])
                if close[i] >= (1 + TRAIL) * extreme:
                    pos = 0
                    completed_rts += 1
                    last_exit_bar = i
                    signals[i] = 0
                    continue
            signals[i] = pos
    signals[n - 1] = 0
    return signals


def main() -> None:
    df = pd.read_csv("bars.csv")
    sig = generate_signals(df)
    prev = 0
    for i, s in enumerate(sig):
        if s != prev:
            print(f"  bar {i:4d} -> {'LONG' if s == 1 else 'SHORT' if s == -1 else 'FLAT'} "
                  f"close={df['close'].iloc[i]:.2f}")
            prev = s


if __name__ == "__main__":
    main()
