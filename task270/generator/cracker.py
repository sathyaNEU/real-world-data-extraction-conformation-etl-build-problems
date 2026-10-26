"""The cracker's path on the cut pack (supplemental-stumping 1.1): a response that lands the call, runs the hygiene
battery (key uniqueness, exact and near-exact duplicates, unmatched joins, fan-out) and executes every filed rule it
points at. On the asks it reads each file as the battery leaves it: each pack's refrigerant from the F-gas register,
the record of what each pack holds, at the strategy's GWP table; the job sheet's kilograms on each cabinet and cold
room line added up, every line a distinct asset and no two lines duplicates. The mirror (the response on the top-up
count, the North East) reads the asks the same way. Every ask figure is scored against figures.json: a hit is within
half a unit of the stated rounding. Prints the sheet and the pair ceiling."""
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

CRACKER = dict(gas_source="register", eq_mode="lines")


def score(target, fig, kw, P, J):
    a = AS.all_asks(target, P=P, J=J, **kw)
    g = fig["asks"]
    rows = []
    for t in K.REGIONS:
        rows.append(("A", "full charge CO2e %s" % t, a["charge_co2e_t"][t] == g["charge_co2e_t"][t]))
    for t in K.REGIONS:
        rows.append(("A", "R404A CO2e %s" % t, a["r404a_co2e_t"][t] == g["r404a_co2e_t"][t]))
    for t in K.REGIONS:
        rows.append(("B", "cabinets and cold rooms %s" % t, abs(a["equipment_kg"][t] - g["equipment_kg"][t]) < 0.05))
    return rows


if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
    target = os.path.join(task, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    P = A.packs(target)
    J = A.pack_jobs(target, P)
    crk = score(target, fig, CRACKER, P, J)
    mir = crk                     # the mirror reads the asks as the cracker does; no ask reads the call
    for name, rows in (("cracker", crk), ("mirror", mir)):
        for ask in "AB":
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
