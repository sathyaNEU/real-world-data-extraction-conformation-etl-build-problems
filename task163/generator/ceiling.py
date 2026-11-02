"""task163 ceiling: the honest careful solver run on the cut pack, never a narrowed one. It lands the call (the ceiling
prices the asks for a response on the call), reads every field by its plain meaning, executes every filed rule as worded
and runs the hygiene battery (duplicates and re-graded rows, anti-joins, re-keyed records, clocks, labels against a
sequence, comments, pairing a header to its rows, reconciling to a filed rate). Every ask figure it files is scored
against figures.json at the asked rounding. Exit 1 when the cracker keeps an ask figure, the pair exceeds 60, two
careful responses on the call reach 70, or the full includer fails to reproduce figures.json.

    python3 task163/generator/ceiling.py
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import calc as C     # noqa: E402
import common as K   # noqa: E402
import pack as PK    # noqa: E402

TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")


def digest():
    h = hashlib.md5()
    for fn in sorted(os.listdir(T)):
        h.update(fn.encode())
        h.update(open(os.path.join(T, fn), "rb").read())
    return h.hexdigest()


# ------------------------------------------------------------------ Ask A routes
def a_routes():
    hours, prem = C.agency(T)
    base = defaultdict(lambda: [0.0, 0.0])
    for r in hours:
        k = "%d-%02d" % (r["d"].year, r["d"].month)
        base[k][0] += r["amt"]
        base[k][1] += r["h"]
    routes = {}
    # 1. every line by its own date: hours by the shift's start, the premium line by its invoice date
    p_inv = defaultdict(float)
    for inv, amt in prem:
        p_inv["%d-%02d" % (inv.year, inv.month)] += amt
    routes["each line by its own date"] = {k: (base[k][0] + p_inv[k]) / base[k][1] for k in base}
    # 2. the reflex repair: a reconciliation billed early in a month is last month's arrears
    p_prev = defaultdict(float)
    for inv, amt in prem:
        m = inv.replace(day=1) - dt.timedelta(1)
        p_prev["%d-%02d" % (m.year, m.month)] += amt
    routes["premium as last month's arrears"] = {k: (base[k][0] + p_prev[k]) / base[k][1] for k in base}
    # 3. pairing the line to the invoice's own rows: the premium belongs to the invoice week's shifts, by their hours
    wk_hours = defaultdict(lambda: defaultdict(float))
    for r in hours:
        wk_hours[K.monday(r["d"])][r["d"]] += r["h"]
    p_week = defaultdict(float)
    for inv, amt in prem:
        mon = inv - dt.timedelta(8)
        tot = sum(wk_hours[mon].values())
        for d, h in wk_hours[mon].items():
            p_week["%d-%02d" % (d.year, d.month)] += amt * h / tot
    routes["premium on the invoice week's shifts"] = {k: (base[k][0] + p_week[k]) / base[k][1] for k in base}
    # 4. premiums left out as a reconciliation of earlier billing (the hours' own lines only)
    routes["hours lines only"] = {k: base[k][0] / base[k][1] for k in base}
    return routes


# ------------------------------------------------------------------ Ask B routes
def b_routes():
    it = C.items(T)
    units = C.graded(T)
    raw_rows = K.read_csv(os.path.join(T, PK.F_RET))

    def shares(rows, legend_of):
        fam = defaultdict(lambda: [0, 0, 0, 0.0])
        for u in rows:
            if not (K.ASK_B_FROM <= u["day"] <= K.ASK_B_TO):
                continue
            f = fam[it[u["item"]]["family"]]
            fate = legend_of(u)[u["grade"]]
            f[0] += 1
            f[1] += fate == "repack"
            f[2] += fate == "scrap"
            f[3] += it[u["item"]]["cost"] if fate == "scrap" else 0.0
        return {k: dict(repack_pct=100.0 * v[1] / v[0], scrap_pct=100.0 * v[2] / v[0], scrap_value=v[3])
                for k, v in fam.items()}
    filed = lambda u: C.OLD
    routes = {"the procedure's grades as written, latest grade per return": shares(units, filed)}
    every = [dict(day=dt.date.fromisoformat(r["graded_at"][:10]), item=int(r["item_code"]), grade=int(r["grade"]))
             for r in raw_rows]
    routes["the procedure's grades, every row"] = shares(every, filed)
    routes["grades swapped for the whole year"] = shares(units, lambda u: C.APP)
    for sw in (dt.date(2026, 6, 1), dt.date(2026, 7, 1)):
        routes["grades swapped from %s" % sw.isoformat()] = shares(units, lambda u, s=sw: C.OLD if u["day"] < s else C.APP)
    return routes


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    gold_a = fig["ask_a"]
    gold_b = fig["ask_b"]
    figs = [("A", k) for k in sorted(gold_a)] + [("B", (f, m)) for f in sorted(gold_b)
                                                  for m in ("repack_pct", "scrap_pct", "scrap_value")]
    n = len(figs)

    def hits_a(route):
        return {k for k in gold_a if K.round_half_up(route[k], 2) == gold_a[k]}

    def hits_b(route):
        out = set()
        for f in gold_b:
            for m, nd in (("repack_pct", 1), ("scrap_pct", 1), ("scrap_value", 0)):
                v = K.round_half_up(route[f][m], nd)
                if (int(v) if nd == 0 else v) == gold_b[f][m]:
                    out.add((f, m))
        return out
    print("task163 ceiling on target/ md5 %s" % digest())
    best_a, best_b = set(), set()
    honest_a, honest_b = set(), set()
    print("Ask A, the cost of an agency hour by month (12 figures, to the penny):")
    for name, route in a_routes().items():
        h = hits_a(route)
        gap = min(abs(route[k] - fig["ask_a_raw"][k]) for k in gold_a)
        print("  %-42s keeps %2d of 12   smallest gap GBP %.4f" % (name, len(h), gap))
        best_a = max(best_a, h, key=len)
        honest_a = max(honest_a, h, key=len)
    print("Ask B, repacked and scrapped shares and the value scrapped by family (15 figures):")
    for name, route in b_routes().items():
        h = hits_b(route)
        half = "swapped" in name
        print("  %-52s keeps %2d of 15%s" % (name, len(h), "   (half-handled: the swap found, misdated)" if half else ""))
        best_b = max(best_b, h, key=len)
        if not half:
            honest_b = max(honest_b, h, key=len)
    honest = len(honest_a) + len(honest_b)
    print("the honest careful cracker (battery run, every field by its plain meaning) keeps %d of %d" % (honest, n))
    kept = len(best_a) + len(best_b)
    Lc = kept / n
    C_ = 38 + 7 + 55 * Lc
    S_ = 5 + 7 + 55 * Lc            # the asks are decoupled from the call: the best response off it keeps as much
    pair = (C_ + S_) / 2.0
    print("best route of any kind, half-handled devices included, keeps %d of %d ask figures (%.1f per cent of the ask "
          "weight)" % (kept, n, 100 * Lc))
    print("one careful response on the call %.1f; the best response off it %.1f; pair %.1f; two careful responses on "
          "the call %.1f" % (C_, S_, pair, C_))
    print("mirror leakage (the best off-call rung's share of ask weight): %.1f per cent" % (100 * Lc))
    # the full includer: the golden's own handling reproduces figures.json
    a, _ = C.ask_a(T)
    b, _ = C.ask_b(T)
    full_ok = hits_a(a) == set(gold_a) and len(hits_b(b)) == 15
    print("full includer (pay periods by the identity; the handheld's legend by the invoices) reproduces figures.json: %s"
          % ("yes" if full_ok else "NO"))
    ok = honest == 0 and pair <= 60 and C_ < 70 and full_ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
