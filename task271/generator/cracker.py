"""task271 cracker: the response that landed the call, ran the hygiene battery (key uniqueness, exact and near
duplicates, unmatched joins, a clock read from its hour profile, cancelled rows) and executed every filed rule the asks
point at, scored figure by figure against the golden at the asks' rounding.

    python3 task271/generator/cracker.py [task271/target]"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C      # noqa: E402
import common as K    # noqa: E402


def battery_notes(P):
    """Cancelled notes out; the near-duplicate pairs (same order, trade date, time and shares, two systems) collapsed;
    every other note kept."""
    N = P["N"][P["N"]["note_status"] != "CANCELLED"].copy()
    N["trade_day"] = pd.to_datetime(N["trade_date"], format="%d/%m/%Y").dt.date
    N = N.drop_duplicates(["client_order_ref", "trade_date", "trade_time", "shares", "side"], keep="first")
    return N


def clock_is_utc(W):
    """The battery's clock test: the placing hours' profile in January against July; a one-hour shift says UTC."""
    ts = pd.to_datetime(W["placed_at"])
    jan = ts[ts.dt.month == 1].dt.hour.value_counts(normalize=True).sort_index()
    jul = ts[ts.dt.month == 7].dt.hour.value_counts(normalize=True).sort_index()
    hrs = range(24)
    a = np.array([jan.get(h, 0.0) for h in hrs])
    b = np.array([jul.get(h, 0.0) for h in hrs])
    shift = int(np.argmax([np.dot(a, np.roll(b, k)) for k in (-2, -1, 0, 1, 2)])) - 2
    return shift != 0


def cracker_a(P):
    closed = set(pd.to_datetime(P["CAL"].loc[P["CAL"]["uk_market"] == "CLOSED", "date"]).dt.date)
    N = battery_notes(P)
    sh = N.groupby("client_order_ref")["shares"].sum()
    in_2026 = set(N.loc[(N["trade_day"] >= dt.date(2026, 1, 1)) & (N["trade_day"] <= K.DATA_END), "client_order_ref"])
    W = P["W"][P["W"]["client_order_ref"].isin(in_2026)].copy()
    W["q"] = W["client_order_ref"].map(sh).astype(float)
    ts = pd.to_datetime(W["placed_at"])
    ts = ts.dt.tz_localize("UTC") if clock_is_utc(P["W"]) else ts.dt.tz_localize("Europe/London", ambiguous="NaT",
                                                                                  nonexistent="shift_forward")
    pts = [C.london_point(t, closed) if not pd.isna(t) else (dt.date(1900, 1, 1), 0) for t in ts]
    W["pday"] = [x[0] for x in pts]
    W["point"] = [x[1] for x in pts]
    W["signed"] = np.where(W["side"] == "BUY", W["q"], -W["q"])
    G = W.groupby(["pday", "point", "isin"])["signed"].sum().reset_index()
    G = G[G["signed"] != 0].copy()
    adv = dict(zip(P["M"]["isin"], P["M"]["adv_shares_2026"]))
    # the order book's code joins the master on every row, so no unmatched join sends the cracker to the
    # corporate actions file
    G["pct"] = G["signed"].abs() / G["isin"].map(adv) * 100.0
    counts = {pi: int((G["point"] == pi).sum()) for pi in range(3)}
    sizes = {pi: float(G.loc[G["point"] == pi, "pct"].mean()) for pi in range(3)}
    return counts, sizes


def cracker_b(P):
    N = battery_notes(P)
    N = N[(N["trade_day"] >= dt.date(2026, 1, 1)) & (N["trade_day"] <= K.DATA_END)]
    N["m"] = N["trade_day"].map(lambda d: d.month)
    g = N.groupby(["m", "side"])["consideration_gbp"].sum()
    return {m: (float(g.get((m, "BUY"), 0.0)) - float(g.get((m, "SELL"), 0.0))) / 1e6 for m in range(1, 11)}


def main(target):
    P = C.load(target)
    A = C.ask_a(P)
    B = C.ask_b(P)
    ca, sa = cracker_a(P)
    cb = cracker_b(P)
    rows = []
    for i in range(3):
        rows.append(("A size %s" % ["09:30", "12:00", "14:30"][i], abs(sa[i] - A["sizes"][i]) < 0.0005,
                     sa[i], A["sizes"][i]))
    for m in sorted(B):
        rows.append(("B net %s" % K.MON3[m], abs(cb[m] - B[m]) < 0.005, cb[m], B[m]))
    kept = sum(r[1] for r in rows)
    print("cracker: %d of %d ask figures kept (%.1f per cent)" % (kept, len(rows), 100.0 * kept / len(rows)))
    for label, ok, got, want in rows:
        print("  %-14s %-5s cracker %.3f against %.3f" % (label, "kept" if ok else "miss", got, want))
    print("cracker clock test reads placed_at as UTC: %s" % clock_is_utc(P["W"]))
    return kept, len(rows)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
