"""task468 architecture 6: the pair ceiling on the cut pack. The cracker lands the call and executes every filed rule;
the mirror stops at the default path (each customer's own parallel ratio) and conforms the asks the habitual way (the
register's meter, UTC quarters, every LabWare row)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve as SV  # noqa: E402

T = os.path.join(os.path.dirname(HERE), "target")
FIG = json.load(open(os.path.join(HERE, "figures.json")))


def asks(D, S, vol, join, composites_only):
    ss = SV.masses(D, S, vol, None, analyte="ss", composites_only=composites_only)
    liq = SV.liquid(T, join=join)
    a = {t: [int(round(x)) for x in liq[t]] for t in liq}
    b = {c: "%.1f" % ss[c] for c in D["custs"]}
    return a, b


def kept(a, b):
    ka = sum(a[t][q] == FIG["ask_a"][t][q] for t in a for q in range(4))
    kb = sum(b[c] == FIG["ask_b"][c] for c in b)
    return ka + kb, 4 * len(a) + len(b), ka, kb


def main():
    D = SV.load(T)
    vol = SV.volumes(D)
    # the cracker: every filed rule, the battery, a docket join and every LabWare sample of the year
    crack = kept(*asks(D, SV.lab(D), vol, "docket", False))
    mirror = kept(*asks(D, SV.lab(D, dup="own", rerun="ignore"), vol, "docket", False))
    print("cracker ask A %d of 16, ask B %d of 12; mirror ask A %d, ask B %d" % (crack[2], crack[3], mirror[2],
                                                                                 mirror[3]))
    n = crack[1]
    sc = 45 + 55.0 * crack[0] / n
    sm = 12 + 55.0 * mirror[0] / n
    print("cracker on the call keeps %d of %d ask figures: %.1f" % (crack[0], n, sc))
    print("mirror off the call keeps %d of %d ask figures: %.1f" % (mirror[0], n, sm))
    print("Pair ceiling: %.1f" % ((sc + sm) / 2))
    print("Mirror leakage: %.1f per cent of the ask weight" % (100.0 * mirror[0] / n))


if __name__ == "__main__":
    main()
