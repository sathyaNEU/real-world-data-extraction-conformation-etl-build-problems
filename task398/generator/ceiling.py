"""The pair ceiling, run on the cut pack. The ask figures are the sixteen monthly station loads (four sampled
stations, April to July) and the four monthly carbon figures (May to August); the chart's two content criteria are
counted as kept by every route.

  cracker   lands the call; runs the hygiene battery and every filed rule: the State laboratory's result where both
            ran a bottle, not detected as zero, the loggers' UTC clock converted, gage height from the field visits'
            mean offset, the rating in force by its effective time, SOP-WQ-07's pounds formula on the plant day's raw
            water; each bottle at the time the bottle log and both laboratories give it, and the carbon from the
            setpoints alone
  mirror    the cracker's ask handling, off the call (the mixed-lake route names the Tessel River)
  joined    the storm bottles joined to the autosampler log (positions that drew a sample), one mean offset, the
            feeder's interruptions taken out (run status and the low-low alarm)
  full      the full includer: joined, and the offsets stepping at each visit
  position  joined with the k-th bottle at the k-th carousel position

Weights 38, 7 and 55 (supplemental-stumping Part 0); r = 5 for the mirror's recommendation side; a hit only when
exact at the stated rounding.

    python3 ceiling.py [target]"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A            # noqa: E402

CHART = 2


def main(target):
    gold = A.monthly(target, **A.LOAD_ROUTES["golden"])
    cells = sorted(gold)
    pg = A.pac(target, "golden")
    load_routes = {"cracker": "cracker", "joined": "joined, mean offset", "full": "joined, visit offset",
                   "position": "joined by position, visit offset"}
    pac_routes = {"cracker": "nodown", "joined": "golden", "full": "golden", "position": "golden"}
    n = len(cells) + len(pg) + CHART
    keep = {}
    for name in load_routes:
        r = A.monthly(target, **A.LOAD_ROUTES[load_routes[name]])
        kl = [c for c in cells if round(r[c]) == round(gold[c])]
        rp = A.pac(target, pac_routes[name])
        kp = [m for m in pg if round(rp[m]) == round(pg[m])]
        keep[name] = (kl, kp)
        print("%-9s keeps %2d of %d load cells, %d of %d carbon months, %d chart criteria: %d of %d ask criteria"
              % (name, len(kl), len(cells), len(kp), len(pg), CHART, len(kl) + len(kp) + CHART, n))
        if kl:
            print("          load cells kept: %s" % ", ".join("%s %d" % c for c in kl))
    for how in A.PAC_ROUTES[1:]:
        rp = A.pac(target, how)
        print("carbon %-10s keeps %d of %d" % (how, sum(1 for m in pg if round(rp[m]) == round(pg[m])), len(pg)))
    L = (len(keep["cracker"][0]) + len(keep["cracker"][1]) + CHART) / n
    C = 38 + 7 + 55 * L
    S = 5 + 7 + 55 * L
    print("cracker %.1f, mirror %.1f on the cracker's ask route" % (C, S))
    print("Pair ceiling: %.1f" % ((C + S) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * L))
    for name in ("joined", "full", "position"):
        Ls = (len(keep[name][0]) + len(keep[name][1]) + CHART) / n
        print("stress, both top responses on the %s route: pair %.1f (ask weight kept %.1f per cent)"
              % (name, (38 + 7 + 55 * Ls + 5 + 7 + 55 * Ls) / 2, 100 * Ls))
    return 0


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    sys.exit(main(tgt))
