"""The cracker and the mirror on the cut pack, for the asks: the cracker lands the call (routes 3, 7, 31 and 40), runs
the hygiene battery and executes every filed rule, and takes each ask the way the files invite; the mirror stops at
the default path (routes 7, 14, 31 and 40) and takes the asks the same way. Prints each ask figure's verdict and the
pair arithmetic; run() returns the counts for checks.py.

    python3 task269/generator/cracker.py"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402
import pack as PK    # noqa: E402

TASK = os.path.dirname(HERE)


def totals(shifts):
    return {rt: sum(n for (r, _), n in shifts.items() if r == rt) for rt in K.ROUTES}


def run(task=TASK, quiet=False):
    target = os.path.join(task, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    gold_a, gold_b = fig["ask_a"], fig["ask_b"]
    paths = {}
    # Ask A: the pilot-post rows counted, cancellations out (nothing joins the two systems, no row repeats in one)
    a_rows = PK.pilot_shifts(target, "rows")
    paths["A natural (rows)"] = totals(a_rows)
    paths["A matched, month-first dates"] = totals(PK.pilot_shifts(target, "monthfirst"))
    paths["A matched on route, day and peak"] = totals(PK.pilot_shifts(target, "routeday"))
    b_paths = {
        "B natural (route lines, central lines shared, A natural)": PK.pilot_cost(target, a_rows, "lines"),
        "B 2025-26 year only, A natural": PK.pilot_cost(target, a_rows, "fy26"),
        "B golden ledger handling, A natural": PK.pilot_cost(target, a_rows, "golden"),
        "B natural ledger, A golden": PK.pilot_cost(target, PK.pilot_shifts(target), "lines"),
        "B 2025-26 year only, A golden": PK.pilot_cost(target, PK.pilot_shifts(target), "fy26"),
    }
    report = {}
    for name, v in paths.items():
        hits = [rt for rt in K.ROUTES if v[rt] == gold_a[rt]]
        report[name] = hits
    for name, v in b_paths.items():
        hits = [rt for rt in K.ROUTES if int(round(v[rt])) == gold_b[rt]]
        report[name] = hits
    cracker_a = paths["A natural (rows)"]
    cracker_b = b_paths["B natural (route lines, central lines shared, A natural)"]
    ca = sum(1 for rt in K.ROUTES if cracker_a[rt] == gold_a[rt])
    cb = sum(1 for rt in K.ROUTES if int(round(cracker_b[rt])) == gold_b[rt])
    # planning weights: the call side 38 (the call, the first route below, eight route figures, three components and
    # the chart's four parts: 17 criteria), instruction-following 7, the asks 55 (16 figures)
    main_n, ask_n = 17, 16
    lc = (ca + cb) / ask_n
    c = 38 + 7 + 55 * lc
    # the mirror keeps the four unbranched routes' figures and two of the chart's parts on the call side
    ls = lc
    s = 38 * 6 / main_n + 7 + 55 * ls
    out = dict(cracker_a_hits=ca, cracker_b_hits=cb, cracker=c, mirror=s, pair=(c + s) / 2,
               mirror_leakage=100.0 * ls, report=report)
    if not quiet:
        for name, hits in report.items():
            print("%-58s hits %d of 8 %s" % (name, len(hits), hits if hits else ""))
        print("cracker %.1f, mirror %.1f, pair %.1f, mirror leakage %.1f per cent" % (c, s, (c + s) / 2, 100 * ls))
    return out


if __name__ == "__main__":
    run()
