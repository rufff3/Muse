"""
AIProve bounty: eth-pnl-fixed
Strategy: N-bar Donchian breakout with return confirmation.

Idea
----
On 1-minute bars the market is mostly noise (mean absolute 1-minute move is
~7 bp, smaller than a round-trip cost of ~15 bp), so a strategy that trades
often bleeds out on fees. This strategy trades rarely and only when a real
trend is under way:

  * Look back N = 90 bars (~1.5 h).
  * Go LONG when the close breaks above the highest HIGH of the last N bars
    AND the N-bar return is already above +0.5%.
  * Go SHORT when the close breaks below the lowest LOW of the last N bars
    AND the N-bar return is already below -0.5%.
  * Hold the position until the opposite signal fires. No stop-loss, no
    take-profit, no time exit -- the position rides the trend.

The return-confirmation filter is what keeps the strategy out of the
sideways chop that dominates the first half of the sample: a breakout with
no follow-through return behind it is ignored.

No lookahead
------------
Every decision at bar i uses only bars 0..i (high/low/close of the last N
bars and the close at i). Fills happen at the NEXT bar's open, so the
strategy can never trade at a price it has already seen move.

Parameters (only two; both sit in the middle of a broad positive plateau,
not on a tuned spike -- see README):
  * LOOKBACK = 90 bars
  * RETURN_THRESHOLD = 0.005 (0.5%)

Usage
-----
    python3 strategy.py            # prints the signal summary
    python3 backtest.py            # runs the backtest, writes results.json
"""

import numpy as np
import pandas as pd

LOOKBACK = 90
RETURN_THRESHOLD = 0.005

# Cost model used by the local backtest (the challenge publishes no exact
# numbers, so these are documented assumptions; the strategy is profitable
# across a wide range of fee/slippage values -- see README):
#   * taker fee 5 bp (0.05%) per fill, all fills are market orders
#   * slippage 2 bp base + 10 bp * (order_qty / bar_volume), capped at 20 bp
#   * capital $10,000, 1x, fixed notional, long/short
CAPITAL = 10_000.0
FEE_BPS = 5.0
SLIP_BASE_BPS = 2.0
SLIP_SIZE_BPS = 10.0
SLIP_CAP_BPS = 20.0


def generate_signals(df: pd.DataFrame) -> np.ndarray:
    """Return target position in {-1, 0, 1} for each bar.

    The signal at bar i is decided using only bars 0..i. A position is held
    until the opposite signal fires; before the first signal the target is 0.
    """
    close = df["close"].to_numpy(dtype=float)
    high = df["high"].to_numpy(dtype=float)
    low = df["low"].to_numpy(dtype=float)
    n = len(df)
    signals = np.zeros(n, dtype=int)
    pos = 0
    for i in range(LOOKBACK, n):
        hi = high[i - LOOKBACK:i].max()
        lo = low[i - LOOKBACK:i].min()
        ret_n = close[i] / close[i - LOOKBACK] - 1.0
        if close[i] > hi and ret_n > RETURN_THRESHOLD and pos != 1:
            pos = 1
        elif close[i] < lo and ret_n < -RETURN_THRESHOLD and pos != -1:
            pos = -1
        signals[i] = pos
    return signals


def main() -> None:
    df = pd.read_csv("bars.csv")
    sig = generate_signals(df)
    n_long = int((sig == 1).sum())
    n_short = int((sig == -1).sum())
    n_flat = int((sig == 0).sum())
    changes = int((np.diff(sig) != 0).sum())
    print(f"bars={len(df)} long={n_long} short={n_short} flat={n_flat} "
          f"position_changes={changes}")
    # list the position changes (bar, new position, close)
    prev = 0
    for i, s in enumerate(sig):
        if s != prev:
            print(f"  bar {i:4d} -> {'LONG' if s == 1 else 'SHORT' if s == -1 else 'FLAT'} "
                  f"close={df['close'].iloc[i]:.2f}")
            prev = s


if __name__ == "__main__":
    main()
