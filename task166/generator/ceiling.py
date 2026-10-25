"""task166's ask ceiling, measured on the cut pack: every route a careful solver takes through the payoff desk's records is
run on the shipped files and scored count by count against the golden (a hit is the exact whole number), and the pair
ceiling is computed on the generated rubric's weights (38 the recommendation, 7 instruction following, 55 the ask),
with the best response off the call keeping 5 of the recommendation's 38.

    python3 task166/generator/ceiling.py [target]"""
from __future__ import annotations

import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C          # noqa: E402

W_REC, W_IF, W_ASK, R_MISS = 38.0, 7.0, 55.0, 5.0
CHART_STRUCTURE = 2       # one bar per quarter; split by center (kept by any response that draws the chart)
CHART_LABELS = 1          # each segment labelled with its count (right only with the right counts)


def route_tables(target):
    leg, core, los = C.load(target)
    paid = C.paid_by_asof(core)
    golden = C.ask_table(C.statement_loans(target, los, core), paid)
    routes = {
        "quotes naming the loan, updates and voids handled, lines excluded (the battery's route)":
            C.ask_table(C.statement_loans(target, los, core, with_mortgages=False, with_manual=False), paid),
        "the battery's route with the outage workbook matched by address":
            C.ask_table(C.statement_loans(target, los, core, with_mortgages=False, with_manual=True), paid),
        "the battery's route with the first-mortgage statements and no outage workbook":
            C.ask_table(C.statement_loans(target, los, core, with_mortgages=True, with_manual=False), paid),
        "every first-mortgage statement on a property with a booked home equity loan, amounts not reconciled":
            C.ask_table(C.statement_loans(target, los, core, with_mortgages=True, with_manual=True, reconcile=False),
                        paid),
    }
    # statements, not loans; and voided requests kept
    log = pd.read_csv(os.path.join(target, C.F_LOG), dtype={"account_reference": str})
    xref = pd.read_csv(os.path.join(target, C.F_XREF), dtype=str)
    x = dict(zip(xref.legacy_loan_no, xref.loan_number))
    rows = []
    for r in log.itertuples(index=False):
        ref = x.get(r.account_reference, r.account_reference)
        if ref in los.index:
            rows.append((ref, C.eastern_date(r.issued_utc), r.statement_status))
    L = pd.DataFrame(rows, columns=["key", "d", "status"])
    L["region"] = L.key.map(los.region)
    L["quarter"] = [C.quarter_of(d) for d in L.d]
    for name, keep, distinct in (("statements counted, not loans", ("ISSUED", "UPDATED"), False),
                                 ("voided requests kept", ("ISSUED", "UPDATED", "VOID"), True)):
        S = L[L.status.isin(keep) & L.quarter.notna()]
        t = {}
        for rg in C.REG_ORDER:
            for q, _, _ in C.QUARTERS:
                part = S[(S.region == rg) & (S.quarter == q)]
                n = part.key.nunique() if distinct else len(part)
                t[(rg, q)] = (n, len(set(part.key) & paid))
        routes[name] = t
    return golden, routes


def score(golden, table):
    hits = 0
    for k, (a, b) in golden.items():
        hits += int(table[k][0] == a) + int(table[k][1] == b)
    return hits


CRACKER = "the battery's route with the outage workbook matched by address"
MIRROR = "quotes naming the loan, updates and voids handled, lines excluded (the battery's route)"
DEVICE_FOUND = "the battery's route with the first-mortgage statements and no outage workbook"
UNRECONCILED = "every first-mortgage statement on a property with a booked home equity loan, amounts not reconciled"


def main(target):
    """the cracker lands the call, runs the battery and reads every file the pack names (the outage workbook among them);
    the mirror stops at a wrong rung and takes the battery's route; the route that finds primary 1 is printed apart, as
    what a reader who reconciles the mortgage statements' amounts keeps"""
    golden, routes = route_tables(target)
    n = 2 * len(golden)
    total = n + CHART_STRUCTURE + CHART_LABELS
    print("route                                                                                     counts kept")
    sc = {}
    for name, t in routes.items():
        sc[name] = score(golden, t)
        tag = " (cracker)" if name == CRACKER else (" (mirror)" if name == MIRROR else
                                                     (" (primary 1 found)" if name == DEVICE_FOUND else
                                                      (" (primary 1 seen, not reconciled)" if name == UNRECONCILED
                                                       else "")))
        print("  %-86s %2d of %d%s" % (name, sc[name], n, tag))
    worst_silent = max(v for k, v in sc.items() if k not in (DEVICE_FOUND, UNRECONCILED))
    lc = (sc[CRACKER] + CHART_STRUCTURE + (CHART_LABELS if sc[CRACKER] == n else 0)) / total
    ls = (sc[MIRROR] + CHART_STRUCTURE + (CHART_LABELS if sc[MIRROR] == n else 0)) / total
    print("every route that does not reconcile the mortgage statements keeps at most %d of %d" % (worst_silent, n))
    cracker = W_REC + W_IF + W_ASK * lc
    mirror = R_MISS + W_IF + W_ASK * ls
    pair = (cracker + mirror) / 2
    print("ask criteria %d (32 counts, %d chart structure, %d chart labels)" % (total, CHART_STRUCTURE, CHART_LABELS))
    print("cracker (call landed, best route) %.1f; mirror (off the call, best route) %.1f" % (cracker, mirror))
    print("Pair ceiling: %.1f" % pair)
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * ls))
    return pair


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
