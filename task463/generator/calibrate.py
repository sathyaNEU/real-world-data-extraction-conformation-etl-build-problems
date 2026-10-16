"""Find each item's nudge (its lines' stream re-draw) so the world meets the design's margins on the pack the feeds
give: every drift-free comparison of the item's twelve-month change rounds to the same tenth with room from the edge; the
golden difference from the published rate sits well inside or well outside the 1.5-point line, with one item of the nine
whose goods keep the moving item nearest the line and Pasta and rice the staying item nearest it, each alone there;
linked month-on-month comparisons drift past the line for the items whose goods keep and not for the rest; unweighted
relatives add Pasta and rice and the item's unit value holds Coffee; and each item's verdict, and the two nearest items'
rates, stay put under every Layer 1 mishandling. Prints the NUDGE dict for world.py.

    python3 task463/generator/calibrate.py
"""
import datetime as dt
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import feeds as F       # noqa: E402
import golden as G      # noqa: E402
import methods as M     # noqa: E402
import published as PB  # noqa: E402
import sim as S         # noqa: E402
import world as W       # noqa: E402

STAY = {"1105", "1146", "1182"}
STORE_MOVE = {c for c, n, dip, *_ in W.ITEMS if dip >= 0.25} - STAY
FRESH_MOVE = {c for c, n, dip, *_ in W.ITEMS if dip < 0.25} - STAY
NEAREST_IN, NEAREST_OUT, UNIT_VALUE_MISS = "1103", "1105", "1211"
VARIANTS = ("week_start", "net", "returns", "unpadded")


def pack_arrays(ls, code, seed):
    """The item's panel as the pack gives it, read the plan's way (each week at its latest extract and in the month it
    ends, EANs to 13 digits, Calderby's values with GST added, returns netted), and under each Layer 1 mishandling."""
    sub = [L for L in ls if L["item"] == code]
    pms = {v: {} for v in ("base",) + VARIANTS}

    def add(v, k, u, val):
        c = pms[v].setdefault(k, [0, 0.0])
        c[0] += u
        c[1] += val
    latest = {}
    for r in F.wrenfold(sub, seed):
        k = (r[0], r[1])
        if k not in latest or r[5] > latest[k][5]:
            latest[k] = r
    for (we, g), r in latest.items():
        d = dt.date.fromisoformat(we)
        for v in pms:
            m = W.month_index(d - dt.timedelta(days=6) if v == "week_start" else d)
            add(v, ("W", g, m), int(r[3]), float(r[4]))
    for r in F.gorsedale(sub, seed):
        fy, n, ean = r[0], r[2], str(r[4])
        week_end = F.FY_START[fy] + dt.timedelta(days=7 * n - 1)
        for v in pms:
            if v == "unpadded" and len(ean) < 13:
                continue        # the number as written finds no GTIN in the classification
            m = W.month_index(week_end - dt.timedelta(days=6) if v == "week_start" else week_end)
            add(v, ("G", ean.zfill(13), m), int(r[6]), float(r[7]))
    crows, skus = F.calderby(sub, seed)
    gt = {s_[0]: s_[1] for s_ in skus}
    for d, st, sku, u, val in crows:
        m = W.month_index(dt.date.fromisoformat(d))
        for v in pms:
            if v == "returns" and u < 0:
                continue
            add(v, ("C", gt[sku], m), int(u), float(val) * (1.0 if v == "net" else 1 + W.GST))
    out = {}
    for v, pm in pms.items():
        lines = {}
        for (r, g, m), (u, val) in pm.items():
            if m is not None:
                lines.setdefault((r, g), {})[m] = (u, val)
        keys = sorted(k for k, ms in lines.items() if all(m in ms and ms[m][0] > 0 for m in range(W.NM)))
        P = np.array([[lines[k][m][1] / lines[k][m][0] for m in range(W.NM)] for k in keys])
        Q = np.array([[lines[k][m][0] for m in range(W.NM)] for k in keys], dtype=float)
        out[v] = (P, Q, P * Q)
    return out


def _edge_ok(v, edge=0.015):
    return abs((abs(v) * 10) % 1 - 0.5) > edge * 10


def item_ok(code, pr, arrs):
    P, Q, E = arrs["base"]
    df = M.drift_free(P, Q, E)
    rt = M.routes(P, Q, E)
    vals = list(df.values())
    if max(vals) - min(vals) > 0.08 or len({G.r1(v) for v in vals}) > 1 or not all(_edge_ok(v) for v in vals):
        return False
    g = df["direct_tornqvist"]
    d = abs(G.r1(G.r1(g) - pr))
    move = code not in STAY
    if code == NEAREST_IN and not 0.8 <= d <= 0.9:
        return False
    if move and code != NEAREST_IN and d > 0.5:
        return False
    if code == NEAREST_OUT and not 2.1 <= d <= 2.4:
        return False
    if not move and code != NEAREST_OUT and not 2.8 <= d <= 4.5:
        return False
    ct = rt["chained_tornqvist"]
    dc = G.r1(G.r1(ct) - pr)
    if code in STORE_MOVE:
        rel = (P[:, -1] / P[:, 0] - 1) * 100
        if not (-11 <= dc <= -3.5 and 4.5 <= g - ct <= 10.5 and ct < rel.min()):
            return False
    if code in FRESH_MOVE and (abs(dc) > 1.0 or abs(g - ct) > 0.4):
        return False
    if 1.0 < abs(dc) < 2.0:
        return False
    if code in STAY - {"1105"} and abs(dc) < 2.0:
        return False
    dj = abs(G.r1(G.r1(rt["direct_jevons"]) - pr))
    if (code == "1105" or move) and dj > 1.2:
        return False
    if code in STAY - {"1105"} and dj < 1.8:
        return False
    du = G.r1(G.r1(rt["unit_value"]) - pr)
    if code == UNIT_VALUE_MISS and du > -2.0:
        return False
    if code != UNIT_VALUE_MISS and (abs(du) > 1.2 if move else abs(du) < 1.8):
        return False
    for v in VARIANTS:
        gv = M.rate(M.tornqvist(*arrs[v], 0, W.NM - 1))
        dv = abs(G.r1(G.r1(gv) - pr))
        if code in (NEAREST_IN, NEAREST_OUT) and G.r1(gv) != G.r1(g):
            return False
        if move and dv > (0.9 if code == NEAREST_IN else 0.7):
            return False
        if not move and dv < (2.1 if code == NEAREST_OUT else 2.5):
            return False
    return True


def main():
    base_lines = S.lines(W.STREAM)
    nudge = {}
    for code in W.ICODE:
        for k in range(0, 600):
            trial = dict(nudge)
            trial[code] = k
            W.NUDGE = trial
            ls = S.monthly(W.STREAM, [dict(L) for L in base_lines], trial)
            q, _ = PB.quotes(ls, W.STREAM)
            pub = PB.published_index(q)
            pr = round((pub[code]["2026-09"] / pub[code]["2025-09"] - 1) * 100, 1)
            if item_ok(code, pr, pack_arrays(ls, code, W.STREAM)):
                nudge[code] = k
                print(code, k, flush=True)
                break
        else:
            raise SystemExit("no nudge found for %s" % code)
    print("NUDGE = %r" % {c: v for c, v in nudge.items() if v})


if __name__ == "__main__":
    main()
