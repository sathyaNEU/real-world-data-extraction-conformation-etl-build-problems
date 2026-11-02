"""The ask layer measured on the cut pack: the careful solver's routes through each ask, and the pair arithmetic.

The cracker lands the call, reads every field by its plain meaning (the service date on a fee line, the item code or
description against the scheme rules' list, the net amount beside the tax, the UTC mark on the plant log and the
Eastern-time mark on the controller export, the alarm and reset events as written), executes every filed rule as worded
and runs the hygiene battery: a credit is paired to the line or the booking it reverses where one line or one booking's
lines equal it (the pairing of a header amount to its rows), and is otherwise taken where it was posted. The stops are
the other complete pipelines a careful solver could file. The full includer reproduces figures.json or this script exits
1. Run: python3 task453/generator/ceiling.py
"""
import datetime as dt
import hashlib
import json
import os
import sys
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as G   # noqa: E402
import world as W    # noqa: E402

TASK = os.environ.get("T453_ROOT", os.path.dirname(HERE))
TARGET = os.path.join(TASK, "target")
ET = ZoneInfo(W.TZ_NAME)
# rubric weights (the shape's arithmetic): the call side, instruction-following and the two ask blocks
W_CALL, W_FOLLOW, W_ASK_A, W_ASK_B = 38.0, 7.0, 27.5, 27.5


_CACHE = {}


def _ledger(target):
    if target not in _CACHE:
        _CACHE[target] = (G.register(target)[2], G.ledger_lines(target))
    return _CACHE[target]


def levy_route(target, adj_rule, by_posting=False):
    """Every crematorium's 2026 levy under one handling of the ledgers. adj_rule says where an account credit no single
    line or booking explains is taken: 'posted', 'month_before', 'ignore', 'year_before' or 'match' (the lines whose
    amounts sum to it)."""
    comm, L = _ledger(target)
    ab = lambda code, d: comm.get(code) is not None and d > comm[code]
    base = {}

    def add(code, d, cents):
        if d.year == W.YEAR:
            k = (code, ab(code, d))
            base[k] = base.get(k, 0) + cents
    inv = L[L.doc == "INV"]
    for i, r in enumerate(inv.itertuples()):
        if r.fee:
            d = dt.date.fromisoformat(r.posted if by_posting else r.service)
            add(r.code, d, r.cents)
    by_cust = {}
    for r in inv.itertuples():
        by_cust.setdefault((r.ledger, r.cust), []).append(r)
    books = {}
    for r in inv.itertuples():
        books.setdefault((r.ledger, r.ref), []).append(r)
    for r in L[L.doc == "CRN"].itertuples():
        if not r.adj:
            if r.fee:
                add(r.code, dt.date.fromisoformat(r.posted if by_posting else r.service), r.cents)
            continue
        posted = dt.date.fromisoformat(r.posted)
        amt = -r.cents
        if adj_rule == "match":
            win = [x for x in by_cust[(r.ledger, r.cust)] if x.service and
                   0 <= (posted - dt.date.fromisoformat(x.service)).days <= 200]
            g = {}
            for x in win:
                d = dt.date.fromisoformat(x.service)
                sig = (x.code, d.year, ab(x.code, d), x.fee)
                g[(x.cents, sig)] = g.get((x.cents, sig), 0) + 1
            eff = G._effects(amt, [(a, s, c) for (a, s), c in g.items()], 4)
            if len(eff) != 1:
                raise SystemExit("an account credit the lines do not settle: %s %s %s" % (r.ledger, r.cust, r.posted))
            (e,) = eff
            for (code, y, abt, fee), cts in e:
                if fee and y == W.YEAR:
                    k = (code, abt)
                    base[k] = base.get(k, 0) - cts
            continue
        # the battery: one line of the account, or one booking's lines, equal to the credit
        single = [x for x in by_cust[(r.ledger, r.cust)] if x.cents == amt and x.service and
                  0 <= (posted - dt.date.fromisoformat(x.service)).days <= 200]
        if single:
            x = single[-1]
            if x.fee:
                add(x.code, dt.date.fromisoformat(x.service), -amt)
            continue
        whole = []
        for ref in {x.ref for x in by_cust[(r.ledger, r.cust)] if x.ref}:
            rows = books[(r.ledger, ref)]
            if sum(x.cents for x in rows) == amt or sum(x.cents for x in rows if x.fee) == amt:
                whole.append(rows)
        if whole:
            for x in whole[-1]:
                if x.fee:
                    add(x.code, dt.date.fromisoformat(x.service), -x.cents)
            continue
        if adj_rule == "posted":
            add(r.code, posted, -amt)
        elif adj_rule == "month_before":
            add(r.code, posted.replace(day=1) - dt.timedelta(days=1), -amt)
        elif adj_rule == "year_before":
            add(r.code, dt.date(posted.year - 1, 12, 15) if posted.month in (1, 2) else posted, -amt)
        elif adj_rule == "ignore":
            pass
    out = {}
    for c in W.CREMATORIA:
        un, abt = base.get((c[0], False), 0), base.get((c[0], True), 0)
        out[c[0]] = int(np.floor((un * W.LEVY_UNABATED + abt * W.LEVY_ABATED) / 100 + 0.5))
    return out


def bypass_route(target, mode):
    """Each abated crematorium's cremations under way while its plant was bypassed, by quarter, under one reading of
    the plant log. mode: 'manual' (the bypass events as logged), 'alarms_clear' (every differential-pressure alarm from
    the alarm to its clearing, with the manual bypasses), 'late_clear' (alarms cleared after five minutes, to the
    clearing), 'reset' (the full includer: alarms not cleared within five minutes, to the reset), 'utc_as_local' (the
    full includer reading the UTC log as local time), 'count_events' (bypass episodes rather than cremations)."""
    comm = G.register(target)[2]
    pl = pd.read_parquet(os.path.join(target, W.FILES["plant"]))
    ev = pl[pl.record == "EVENT"].sort_values(["fund_code", "logged_utc"])
    cy = pd.read_csv(os.path.join(target, W.FILES["cycles"]), dtype={"fund_code": str})
    cy = cy[cy.cycle_type == "CREMATION"]
    out = {}
    for code, g in ev.groupby("fund_code"):
        rows = list(g.itertuples())
        iv = []
        for i, r in enumerate(rows):
            if r.event == "MANUAL BYPASS ON":
                off = next(x for x in rows[i + 1:] if x.event == "MANUAL BYPASS OFF")
                iv.append((r.logged_utc, off.logged_utc))
            if r.event == "ALARM" and r.detail.startswith("DP HIGH"):
                clr = next(x for x in rows[i + 1:] if x.event == "ALARM CLEARED" and x.detail == "DP HIGH")
                late = (clr.logged_utc - r.logged_utc) > pd.Timedelta(minutes=5)
                if mode == "alarms_clear" or (mode == "late_clear" and late):
                    iv.append((r.logged_utc, clr.logged_utc))
                if mode in ("reset", "utc_as_local", "count_events") and late:
                    rst = next(x for x in rows[i + 1:] if x.event == "PLANT RESET")
                    iv.append((r.logged_utc + pd.Timedelta(minutes=5), rst.logged_utc))
        c = cy[cy.fund_code == code]
        if mode == "utc_as_local":
            s = pd.to_datetime(c.charge_et).dt.tz_localize("UTC")
            e = pd.to_datetime(c.end_et).dt.tz_localize("UTC")
        else:
            s = pd.to_datetime(c.charge_et).dt.tz_localize(ET).dt.tz_convert("UTC")
            e = pd.to_datetime(c.end_et).dt.tz_localize(ET).dt.tz_convert("UTC")
        q = pd.to_datetime(c.charge_et).dt.quarter.values
        first_q = 1 if comm[code].year < W.YEAR else (comm[code].month - 1) // 3 + 1
        if mode == "count_events":
            qs = [pd.Timestamp(b0).tz_convert(ET).quarter for b0, b1 in iv]
            out[code] = {"Q%d" % k: int(sum(1 for x in qs if x == k)) for k in range(first_q, 5)}
            continue
        hit = np.zeros(len(c), bool)
        for b0, b1 in iv:
            hit |= ((s <= b1) & (e >= b0)).values
        out[code] = {"Q%d" % k: int(hit[q == k].sum()) for k in range(first_q, 5)}
    return out


def kept_a(route, gold):
    return sum(1 for k in gold if route[k] == gold[k]) / len(gold)


def kept_b(route, gold):
    cells = [(c, q) for c in gold for q in gold[c]]
    return sum(1 for c, q in cells if route.get(c, {}).get(q) == gold[c][q]) / len(cells)


def main():
    fig = json.load(open(os.path.join(TASK, "generator", "figures.json")))
    digest = hashlib.sha256(b"".join(open(os.path.join(TARGET, f), "rb").read() for f in sorted(os.listdir(TARGET))))
    print("ceiling measured on the cut pack (sha256 %s)" % digest.hexdigest()[:16])
    gold_a, gold_b = fig["levy"], fig["bypass"]
    routes_a = {
        "full includer: account credits matched to the lines they sum to": levy_route(TARGET, "match"),
        "cracker: battery pairing, else the posting date": levy_route(TARGET, "posted"),
        "stop: account credits to the month before posting": levy_route(TARGET, "month_before"),
        "stop: account credits left out": levy_route(TARGET, "ignore"),
        "stop: Jan and Feb account credits to the year before": levy_route(TARGET, "year_before"),
        "stop: every line and credit by its posting date": levy_route(TARGET, "posted", by_posting=True),
    }
    routes_b = {
        "full includer: alarms not cleared in five minutes, to the reset": bypass_route(TARGET, "reset"),
        "cracker: the bypass events as logged": bypass_route(TARGET, "manual"),
        "stop: every differential-pressure alarm to its clearing": bypass_route(TARGET, "alarms_clear"),
        "stop: late-cleared alarms to their clearing": bypass_route(TARGET, "late_clear"),
        "stop: the log's UTC read as local time": bypass_route(TARGET, "utc_as_local"),
        "stop: bypass episodes counted, not cremations": bypass_route(TARGET, "count_events"),
    }
    ok = True
    print("\nAsk A, each crematorium's 2026 levy (20 figures, nearest dollar): share of figures kept, and the smallest miss")
    for name, r in routes_a.items():
        miss = min(abs(r[k] - gold_a[k]) for k in gold_a if r[k] != gold_a[k]) if kept_a(r, gold_a) < 1 else 0
        print("  %-62s kept %5.1f%%  smallest miss %s" % (name, 100 * kept_a(r, gold_a), miss))
    if routes_a["full includer: account credits matched to the lines they sum to"] != gold_a:
        print("FULL INCLUDER DOES NOT REPRODUCE figures.json (Ask A)")
        ok = False
    print("\nAsk B, cremations under way while bypassed, each abated crematorium and quarter (24 cells): share kept")
    for name, r in routes_b.items():
        print("  %-62s kept %5.1f%%" % (name, 100 * kept_b(r, gold_b)))
    if routes_b["full includer: alarms not cleared in five minutes, to the reset"] != gold_b:
        print("FULL INCLUDER DOES NOT REPRODUCE figures.json (Ask B)")
        ok = False
    ca = routes_a["cracker: battery pairing, else the posting date"]
    cb = routes_b["cracker: the bypass events as logged"]
    ka, kb = kept_a(ca, gold_a), kept_b(cb, gold_b)
    best_a = max(kept_a(r, gold_a) for n, r in routes_a.items() if not n.startswith("full"))
    best_b = max(kept_b(r, gold_b) for n, r in routes_b.items() if not n.startswith("full"))
    cracker = W_CALL + W_FOLLOW + W_ASK_A * ka + W_ASK_B * kb
    # the mirror stops at the call's most attractive wrong rung (the survey's age profile at age at death): it keeps
    # the verdict and the instruction weight, misses the designations, and runs the same ask routes as the cracker
    mirror = 0.30 * W_CALL + W_FOLLOW + W_ASK_A * ka + W_ASK_B * kb
    best_careful = W_CALL + W_FOLLOW + W_ASK_A * best_a + W_ASK_B * best_b
    print("\nPair arithmetic (call %.0f, instructions %.0f, Ask A %.1f, Ask B %.1f):" % (W_CALL, W_FOLLOW, W_ASK_A, W_ASK_B))
    print("  cracker on the call            %.1f  (asks kept: A %.0f%%, B %.0f%%)" % (cracker, 100 * ka, 100 * kb))
    print("  mirror off the call            %.1f" % mirror)
    print("  pair (cracker, mirror)         %.1f" % ((cracker + mirror) / 2))
    print("  two careful responses on call  %.1f each at most (the best stop on each ask)" % best_careful)
    if (cracker + mirror) / 2 > 60 or best_careful >= 70:
        ok = False
        print("PAIR OVER THE BAR")
    if ka > 0 or kb > 0:
        ok = False
        print("THE CRACKER KEEPS AN ASK FIGURE")
    print("\n%s" % ("ceiling OK" if ok else "ceiling FAILED"))
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
