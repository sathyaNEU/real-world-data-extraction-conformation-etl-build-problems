"""task247 ladder figures on the cut pack: --ladder prints the design note's ladder (each rung's season maxima and
list, the refill's variants, the back-test). The ask layer is measured by ceiling.py (the careful solver's routes, the
mirror and the full includer's control); run without --ladder this script runs it.

    python3 task247/generator/pair.py --ladder [target]
    python3 task247/generator/pair.py [pack]          (the same as ceiling.py [pack])
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
import solve

TARGET = os.path.join(os.path.dirname(HERE), "target")


def main(target=None):
    import ceiling
    return ceiling.main(target)


def ladder(target=TARGET):
    pk, b, rows = solve.solve(target, B.FILES)
    ru, c = pk.rungs()
    var = pk.variants(b)
    print("constants", {k: round(v, 4) for k, v in c.items()}, "clear-sky", round(b, 4))
    print("%-22s %s" % ("", " ".join("%5s" % x for x in pk.codes)))
    for k, v in ru.items():
        print("%-22s %s  %s" % (k, " ".join("%5.2f" % x for x in v), [pk.codes[i] for i in range(16) if v[i] >= 8]))
    print("%-22s %s" % ("golden", " ".join("%5.2f" % r["dhw"] for r in rows)))
    for k, v in var.items():
        print("%-22s %s" % (k, " ".join("%5.2f" % x for x in v)))
    for k, v in pk.backtest(b).items():
        print("back-test %-10s rmse %.3f hot mean %+.3f (%d days, %d hot)" % ((k,) + v))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    t = args[0] if args else TARGET
    if "--ladder" in sys.argv:
        ladder(t)
    else:
        main(t)
