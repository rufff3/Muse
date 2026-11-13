"""
Local backtest for the eth-pnl-fixed strategy.

Replays strategy.generate_signals() over bars.csv with a documented cost
model and prints / writes the metrics the bounty grades on:
net PnL after costs, max drawdown, number of trades, win rate.

Cost model (assumptions -- the challenge README publishes no exact numbers,
so these are stated explicitly; the strategy stays profitable across the
whole plausible range, see README for the sensitivity table):
  * All fills are taker (market orders): fee 5 bp (0.05%) per fill.
  * Slippage: 2 bp base + 10 bp * (order_qty / bar_volume), capped at 20 bp.
  * Execution at the NEXT bar's open after the signal bar's close
    (no lookahead, no phantom fills).
  * Capital $10,000, 1x, fixed notional, long or short.

Usage:
    python3 backtest.py            # prints results and writes results.json
"""

import json

import numpy as np
import pandas as pd

from strategy import (
    CAPITAL,
    FEE_BPS,
    LOOKBACK,
    RETURN_THRESHOLD,
    SLIP_BASE_BPS,
    SLIP_CAP_BPS,
    SLIP_SIZE_BPS,
    generate_signals,
)


def _slip_bps(qty: float, bar_volume: float) -> float:
    return min(
        SLIP_BASE_BPS + SLIP_SIZE_BPS * (abs(qty) / max(bar_volume, 1e-9)),
        SLIP_CAP_BPS,
    )


def run_backtest(df: pd.DataFrame, signals: np.ndarray) -> dict:
    close = df["close"].to_numpy(dtype=float)
    open_ = df["open"].to_numpy(dtype=float)
    vol = df["volume"].to_numpy(dtype=float)
    n = len(df)

    pos = 0
    qty = 0.0
    entry = 0.0
    realized = 0.0
    costs = 0.0
    trades = 0
    wins = 0
    round_trips = 0
    peak = CAPITAL
    max_dd = 0.0
    equity_curve = [CAPITAL]
    trade_log = []

    for i in range(n - 1):
        target = int(signals[i])
        if target != pos:
            price = float(open_[i + 1])
            bv = float(vol[i + 1])
            if pos != 0:
                notional = abs(qty) * price
                cost = notional * (FEE_BPS + _slip_bps(qty, bv)) / 1e4
                pnl = qty * (price - entry) - cost
                realized += pnl
                costs += cost
                trades += 1
                round_trips += 1
                if pnl > 0:
                    wins += 1
                trade_log.append({
                    "action": "CLOSE",
                    "bar": i + 1,
                    "side": "LONG" if pos > 0 else "SHORT",
                    "entry": round(entry, 2),
                    "exit": round(price, 2),
                    "pnl_usd": round(pnl, 2),
                })
                qty, entry = 0.0, 0.0
            if target != 0:
                q = CAPITAL / price
                cost = CAPITAL * (FEE_BPS + _slip_bps(q, bv)) / 1e4
                realized -= cost
                costs += cost
                qty, entry = target * q, price
                trades += 1
                trade_log.append({
                    "action": "OPEN",
                    "bar": i + 1,
                    "side": "LONG" if target > 0 else "SHORT",
                    "entry": round(price, 2),
                    "exit": None,
                    "pnl_usd": None,
                })
            pos = target
        eq = CAPITAL + realized + (qty * (close[i + 1] - entry) if pos != 0 else 0.0)
        equity_curve.append(eq)
        peak = max(peak, eq)
        max_dd = max(max_dd, (peak - eq) / peak)

    if pos != 0:
        price = float(close[-1])
        notional = abs(qty) * price
        cost = notional * (FEE_BPS + _slip_bps(qty, float(vol[-1]))) / 1e4
        pnl = qty * (price - entry) - cost
        realized += pnl
        costs += cost
        trades += 1
        round_trips += 1
        if pnl > 0:
            wins += 1
        trade_log.append({
            "action": "CLOSE",
            "bar": n - 1,
            "side": "LONG" if pos > 0 else "SHORT",
            "entry": round(entry, 2),
            "exit": round(price, 2),
            "pnl_usd": round(pnl, 2),
        })
        equity_curve[-1] = CAPITAL + realized

    return {
        "net_pnl_usd": round(realized, 2),
        "return_pct": round(realized / CAPITAL * 100, 2),
        "max_drawdown_pct": round(max_dd * 100, 2),
        "trades_fills": trades,
        "round_trips": round_trips,
        "winning_round_trips": wins,
        "win_rate_pct": round(100.0 * wins / round_trips, 1) if round_trips else 0.0,
        "total_costs_usd": round(costs, 2),
        "final_equity_usd": round(CAPITAL + realized, 2),
        "capital_usd": CAPITAL,
        "lookback_bars": LOOKBACK,
        "return_threshold": RETURN_THRESHOLD,
        "fee_bps_per_fill": FEE_BPS,
        "slippage_bps": {"base": SLIP_BASE_BPS, "size_coef": SLIP_SIZE_BPS, "cap": SLIP_CAP_BPS},
        "bars": n,
        "trade_log": trade_log,
    }


def main() -> None:
    df = pd.read_csv("bars.csv")
    signals = generate_signals(df)
    results = run_backtest(df, signals)
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"net PnL after costs : ${results['net_pnl_usd']:.2f} "
          f"({results['return_pct']:.2f}% on ${CAPITAL:,.0f})")
    print(f"max drawdown        : {results['max_drawdown_pct']:.2f}%")
    print(f"fills / round-trips : {results['trades_fills']} / {results['round_trips']}")
    print(f"win rate            : {results['win_rate_pct']:.1f}% "
          f"({results['winning_round_trips']}/{results['round_trips']} round-trips)")
    print(f"total costs         : ${results['total_costs_usd']:.2f}")
    print(f"final equity        : ${results['final_equity_usd']:.2f}")
    print("results.json written")


if __name__ == "__main__":
    main()
