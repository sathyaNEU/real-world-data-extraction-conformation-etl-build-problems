"""task245 pair measurement on the cut pack: the cracker (lands the call, runs the hygiene battery: exact repeats dropped,
every filed definition executed: the procedure's NO2 at 20 C over valid hours, the plan's rate over the periods that
started in the year with the void period out) and the mirror (stops at the default path on the call, the count over valid
days scaled by data capture) each answer both asks the way that path does, and every ask figure is scored against the
golden at its rounding. The mirror's share of the call's per-station criteria is measured too (the notes it gets right,
the whole-year counts it lands inside the accepted range). Prints the cracker sheet, the mirror's leakage and the pair
ceiling; --ladder prints the design note's ladder figures.

    python3 task245/generator/pair.py [target]
    python3 task245/generator/pair.py --ladder
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
import estim as E
import params as P
import solve

TARGET = os.path.join(os.path.dirname(HERE), "target")


def ask_paths(target):
    F = B.FILES
    return {
        # the cracker: exact repeats dropped, the export taken as the procedure's 20 C basis, the plan's rate executed
        # with the laboratory's collecting area
        "cracker": (solve.no2_means(target, F, fits="none"), solve.deposition(target, F, area="lab")),
        # the cracker who takes the laboratory's own rates
        "cracker_lab_rates": (solve.no2_means(target, F, fits="none"), solve.lab_rates(target, F)),
        # the cracker who reads the plan's Annex A and puts the Frisbee gauge's area on every period
        "cracker_frisbee": (solve.no2_means(target, F, fits="none"), solve.deposition(target, F, area="frisbee")),
        # the cracker who reads the logger lines and rescales every hour of the year
        "cracker_every_hour": (solve.no2_means(target, F, fits="all"), solve.deposition(target, F, area="lab")),
        # the mirror, careful on the asks as the cracker is
        "mirror": (solve.no2_means(target, F, fits="none"), solve.deposition(target, F, area="lab")),
    }


def score(target, paths):
    F = B.FILES
    gold_a, gold_b = solve.no2_means(target, F), solve.deposition(target, F)
    n = len(gold_a) + len(gold_b)
    keep = {}
    for k, (a, b) in paths.items():
        hits = ["A " + c for c in gold_a if round(a[c], 1) == round(gold_a[c], 1)] + \
               ["B " + s for s in gold_b if round(b[s]) == round(gold_b[s])]
        keep[k] = len(hits) / n
        print("%-20s keeps %d of %d ask figures %s" % (k, len(hits), n, hits))
    return keep


def main(target=TARGET):
    keep = score(target, ask_paths(target))
    A = solve.answer(target, B.FILES)
    R = A["R"]
    wind = [k for k in R if k.startswith("wind")]
    gold = E.call(R)
    lo = {c: min(R[k][i] for k in wind) for i, c in enumerate(P.CODES)}
    hi = {c: max(R[k][i] for k in wind) for i, c in enumerate(P.CODES)}
    pro = {c: R["pro_rata"][i] for i, c in enumerate(P.CODES)}
    mnote = [c for c in P.CODES if pro[c] > 35]
    notes_right = sum((c in mnote) == (c in gold) for c in P.CODES)
    inside = sum(lo[c] - 1 <= round(pro[c]) <= hi[c] + 1 for c in P.CODES)
    share = (notes_right + inside) / 24.0
    r_miss = round(38 * 0.75 * share, 1)
    print("mirror on the call: notes %s; %d of 12 notes right, %d of 12 whole-year counts inside the accepted range; keeps "
          "%.1f of the 38 recommendation points" % (mnote, notes_right, inside, r_miss))
    lc = max(keep[k] for k in keep if k.startswith("cracker") and k != "cracker_every_hour")
    ls = keep["mirror"]
    c, s = 38 + 7 + 55 * lc, r_miss + 7 + 55 * ls
    print("Pair ceiling: %.1f" % ((c + s) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * ls))
    return (c + s) / 2, 100 * ls


def ladder(target=TARGET):
    """the design note's ladder: each rung's counts at the six stations it moves and its noted set, and the corridor"""
    A = solve.answer(target, B.FILES)
    R = A["R"]
    wind = [k for k in R if k.startswith("wind")]
    show = ["TBT1", "TBT2", "TH3", "TBT4", "TH5", "TH6"]
    noted = lambda key: [P.CODES[i] for i in range(len(P.CODES)) if R["valid_days"][i] <= 35 and
                         (R[key][i] > 50 if key.startswith("p904") else R[key][i] > 35)]
    for k in [k for k in R if not k.startswith("wind")]:
        print("%-24s %s  %s" % (k, " ".join("%5.1f" % R[k][P.CODES.index(c)] for c in show), noted(k) if k != "valid_days" else ""))
    print("%-24s %s  %s" % (E.REFERENCE, " ".join("%5d" % R[E.REFERENCE][P.CODES.index(c)] for c in show), noted(E.REFERENCE)))
    for c in P.CODES:
        i = P.CODES.index(c)
        print("%-5s valid %3d days, %2d above 50; scaled %.1f; rebuilds %d to %d over %d readings" % (
            c, int(E.daily(A["xv"], A["valid"])[1][i].sum()), R["valid_days"][i], R["pro_rata"][i],
            min(R[k][i] for k in wind), max(R[k][i] for k in wind), len(wind)))


if __name__ == "__main__":
    if "--ladder" in sys.argv:
        ladder()
    else:
        main(sys.argv[1] if len(sys.argv) > 1 else TARGET)
