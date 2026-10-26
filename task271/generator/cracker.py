"""The cracker's path on the cut pack (supplemental-stumping 1.1): a response that lands the call, runs the hygiene
battery (key uniqueness, exact and near-exact duplicates, unmatched joins, fan-out) and executes every filed rule it
points at. On the asks it reads each file as the battery leaves it: the flow tests joined to the register on the
hydrant number (every test finds a hydrant, so no unmatched-join sweep fires) and each test's flow read as the flow
the guide asks for; the brief's ratio rule executed (the ratio in effect on January 1, 2026) on the roll's assessed
values; the claim system's payments summed per claim, reopened lines folded into their claim and recoveries netted as
the brief says. The mirror (the response on the foundation model, Brookmere) reads the asks the same way. Every ask
figure is scored against figures.json: a hit is within half a unit of the stated rounding. Prints the sheet and the
pair ceiling."""
import json
import os
import sys
import warnings

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A    # noqa: E402
import asks as AS       # noqa: E402
import common as K      # noqa: E402

CRACKER = dict(renumber=False, at20=False, filters=True, appeals=False, ratio="certified", bordereau=False,
               reopen="combine", net=True)
HALF = dict(renumber=True, at20=False, filters=True, appeals=True, ratio="certified", bordereau=False,
            reopen="combine", net=True)


def score(target, fig, kw, d, homes):
    a = AS.all_asks(target, d, homes, **kw)
    g = fig["asks"]
    rows = []
    for t in K.CANDIDATES:
        rows.append(("A", "protected %s" % t, a["protected_homes"][t] == g["protected_homes"][t]))
    for t in K.CANDIDATES:
        rows.append(("B", "market %s" % t, abs(a["market_value_musd"][t] - g["market_value_musd"][t]) < 0.05))
    for y in ("2023", "2024", "2025"):
        rows.append(("C", "payment %s" % y, a["water_payment_by_accident_year"][y] ==
                     g["water_payment_by_accident_year"][y]))
    rows.append(("D", "fire unprotected", abs(a["fire_per_1000"]["unprotected"] - g["fire_per_1000"]["unprotected"])
                 < 0.05))
    return rows


if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
    target = os.path.join(task, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    d, _ = A.book_table(target)
    homes = A.township_homes(target)
    crk = score(target, fig, CRACKER, d, homes)
    mir = crk                     # the mirror reads the asks as the cracker does; no ask reads the call
    half = score(target, fig, HALF, d, homes)
    for name, rows in (("cracker", crk), ("mirror", mir), ("half-handled", half)):
        for ask in "ABCD":
            r = [x for x in rows if x[0] == ask]
            print("%s Ask %s: keeps %d of %d%s" % (name, ask, sum(x[2] for x in r), len(r),
                                                   "" if not any(x[2] for x in r) else
                                                   " (" + ", ".join(x[1] for x in r if x[2]) + ")"))
    n = len(crk)
    lc, lm = sum(x[2] for x in crk) / n, sum(x[2] for x in mir) / n
    pair = ((38 + 7 + 55 * lc) + (5 + 7 + 55 * lm)) / 2
    print("cracker %d of %d ask figures; mirror %d of %d; mirror leakage %.1f per cent; pair ceiling %.1f" % (
        sum(x[2] for x in crk), n, sum(x[2] for x in mir), n, 100 * lm, pair))
    sys.exit(0 if pair <= 40 else 1)
