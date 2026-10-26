"""The pair arithmetic, measured on the cut pack.

Runs every cracker and mirror stop named in the design note's ask sheet against the golden and reports the
ask weight each keeps, then the pair ceiling. It scores nothing unless the pack is built, and it refuses
rather than reporting a pass on an empty denominator (reduce-house-fixes H34).

    python3 task184/generator/pair.py            # exit 0 only when the pair sits at or under 40
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
PACK = os.path.join(TASK, "target")

# Ask weight, shared out across the three asks in proportion to their separately gradable figures, which
# is how the generated rubric distributes the ask side's 55 to 60 per cent.
def ask_weight(gold):
    n = {k: len(v) for k, v in gold["asks"].items()}
    total = float(sum(n.values()))
    return {k: v / total for k, v in n.items()}


def load_golden():
    path = os.path.join(HERE, "figures.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def stops():
    """Each ask's cracker and mirror stops, measured on the cut pack.

    Returns {ask: {"cracker": {figure: value}, "mirror": {figure: value}}} with the figure names keyed
    exactly as figures.json keys them, so the comparison is on the graded figures and nothing else.
    """
    import csv

    import analysis as AN
    import asks as A
    import ledger as L
    import records as R

    sim = L.materialise()
    t25 = L.entry_table(sim, "FY25")
    accr = A.accruals(sim)
    control = A.ap_control(accr)
    till = A.tills(sim)
    sales = A.sales_control(till)
    log = A.run_log(t25)
    rd = lambda name: [tuple(r) for r in csv.reader(open(os.path.join(PACK, name), encoding="utf-8"))][1:]

    s1 = AN.ask1_stops(accr, control)
    s2 = AN.ask2_stops(till, sales)
    s3 = AN.ask3_stops(rd(R.FY25_SUMMARY), rd(A.RUN_LOG))
    out = {}
    out["ask1"] = {who: {"%s|subledger" % u: v for u, v in s1[who].items()}
                   for who in ("cracker", "mirror")}
    out["ask2"] = {who: {"%s|%s" % (k, f): s2[who][k][f] for k in s2[who] for f in s2[who][k]}
                   for who in ("cracker", "mirror")}
    out["ask3"] = {who: dict(s3[who]) for who in ("cracker", "mirror")}
    return out


def main():
    sys.path.insert(0, HERE)
    if not os.path.isdir(PACK):
        print("REFUSE  no pack at %s: nothing to measure" % PACK)
        print("        the design note's Pair ceiling and Mirror leakage are design targets until stage 3")
        return 3
    gold = load_golden()
    if not gold:
        print("REFUSE  no generator/figures.json: nothing to score against")
        return 3
    routes = stops()
    if routes is None:
        print("REFUSE  analysis.askN_stops not available: the ask stops are not implemented yet")
        return 3
    weight = ask_weight(gold)

    scored = 0
    cracker_kept = mirror_kept = 0.0
    for ask, by_stop in routes.items():
        figures = gold["asks"][ask]
        if not figures:
            print("REFUSE  %s has no golden figures: an empty denominator is not a pass" % ask)
            return 3
        for who, keep in (("cracker", "cracker"), ("mirror", "mirror")):
            got = by_stop.get(keep)
            if got is None:
                print("REFUSE  %s has no %s stop" % (ask, who))
                return 3
            hits = sum(1 for k, v in figures.items() if k in got and got[k] == v)
            scored += len(figures)
            share = hits / float(len(figures))
            if who == "cracker":
                cracker_kept += share * weight[ask]
            else:
                mirror_kept += share * weight[ask]
            print("%-6s %-8s %3d of %3d figures  %5.1f per cent of the ask"
                  % (ask, who, hits, len(figures), 100.0 * share))

    if scored == 0:
        print("REFUSE  scored nothing")
        return 3
    total = sum(weight.values())
    lc = cracker_kept / total
    ls = mirror_kept / total
    pair = 28.5 + 27.5 * (lc + ls)
    print()
    print("cracker keeps %.1f per cent of ask weight, mirror keeps %.1f per cent" % (100 * lc, 100 * ls))
    print("pair ceiling %.1f (bar 50, build to 40)" % pair)
    if 100 * ls >= 35.0:
        print("FAIL  mirror leakage %.1f per cent is at or over 35" % (100 * ls))
        return 1
    if pair > 40.0:
        print("FAIL  pair ceiling %.1f is over 40" % pair)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
