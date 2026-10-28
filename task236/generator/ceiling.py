"""The cracker sheet for task236's two asks, run on the cut pack.

The cracker lands the call, runs the hygiene battery and executes every rule CDB-FLU-03 s.2 and s.3 file: cases built
from every result reporting influenza, preliminary or final, a person's positives within 14 days of the first one case,
notified at the first such result's receipt, placed by residential postcode under the concordance in force with the
requesting service's postcode for a blank or 0000, residents of other states out, counted by 09:00 Monday local. Where
it can still go wrong is who a person is (every gateway key a person), which postcode places a case (the first row's)
and which report a specimen is read off; every such reading is scored here against the golden, figure by figure, a hit
being the same whole count or a rate within 0.05 per 100,000.

The pair ceiling uses supplemental-stumping Part 0's weights: 38 for the recommendation and its components, 7 for
instruction-following, 55 for the asks spread over their 20 criteria (8 season-to-date counts, 8 week 36 rates and the
chart's four parts). The cracker keeps the chart's four (panels, weeks 26 to 36, change weeks, the flagged regions it
landed); the mirror, off the call at positivity, keeps three, and its recommendation keeps 5.

    python3 task236/generator/ceiling.py [target]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
import estim as E

ASK_CRITERIA = 20
CHART_CRACKER, CHART_MIRROR = 4, 3


def sheet(target):
    D = E.load(target, B.FILES)
    erp = E.erp_by_region(D)
    gold = E.cases(D)
    gA, gB = E.season_to_date(gold), E.week_rate(gold, erp)
    A, Bs = {}, {}
    for name, c in E.readings(D).items():
        A[name], Bs[name] = E.season_to_date(c), E.week_rate(c, erp)
    out = []
    for name in E.READINGS:
        a, b = A[name], Bs[name]
        out.append((name, [k for k in E.EIGHT if a[k] == gA[k]] + [k + " rate" for k in E.EIGHT if abs(b[k] - gB[k]) < 0.05]))
    return gA, gB, A, Bs, out


def ceiling(kept_cracker, kept_mirror):
    lc = (kept_cracker + CHART_CRACKER) / ASK_CRITERIA
    ls = (kept_mirror + CHART_MIRROR) / ASK_CRITERIA
    c, s = 38 + 7 + 55 * lc, 5 + 7 + 55 * ls
    return lc, ls, c, s, (c + s) / 2


def main(target):
    gA, gB, A, Bs, rows = sheet(target)
    cr = E.CRACKER
    print("| Region | Golden season | Cracker season | Golden week 36 rate | Cracker week 36 rate |")
    print("|---|---|---|---|---|")
    for k in E.EIGHT:
        print("| %s | %s | %s | %.1f | %.1f |" % (k, format(gA[k], ","), format(A[cr][k], ","), gB[k], Bs[cr][k]))
    print()
    print("| Reading (the cracker's first, then every careful variant) | Figures kept | Cracker sheet |")
    print("|---|---|---|")
    for name, hits in sorted(rows, key=lambda x: x[0] != cr):
        print("| %s | %s | %s |" % (name, ", ".join(hits) if hits else "none", "keeps" if hits else "miss"))
    kept = sum(len(h) for n, h in rows if n == cr)
    worst = max(len(h) for n, h in rows)
    lc, ls, c, s, pair = ceiling(kept, kept)
    print()
    print("cracker keeps %d of 16 figures; the best of %d careful readings keeps %d" % (kept, len(rows), worst))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * ls))
    print("Pair ceiling: %.1f (C = 38 + 7 + 55 x %.2f = %.1f; S = 5 + 7 + 55 x %.2f = %.1f)" % (pair, lc, c, ls, s))
    lc, ls, c, s, pair = ceiling(worst, worst)
    print("best careful reading, both responses on it: pair %.1f" % pair)
    return rows


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
