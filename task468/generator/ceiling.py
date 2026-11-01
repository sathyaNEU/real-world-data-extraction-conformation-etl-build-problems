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


def asks(D, S, vol):
    ss = SV.masses(D, S, vol, None, analyte="ss")
    a = {c: [int(round(x)) for x in vol[c]["q"]] for c in D["custs"]}
    b = {c: "%.1f" % ss[c] for c in D["custs"]}
    return a, b


def kept(a, b):
    n = sum(a[c][q] == FIG["ask_a"][c][q] for c in a for q in range(4)) + sum(b[c] == FIG["ask_b"][c] for c in b)
    return n, 4 * len(a) + len(b)


def main():
    D = SV.load(T)
    crack = kept(*asks(D, SV.lab(D), SV.volumes(D)))
    seg = {c: [(r["Flow meter"], None, None, None, None)] for c, r in ((r["Customer"], r) for r in D["reg"])}
    tel_utc = SV.telemetry(D, clock="utc")
    try:
        vol_m = SV.volumes(D, tel=tel_utc, seg=seg)
    except KeyError:
        vol_m = SV.volumes(D, tel=tel_utc)
    mirror = kept(*asks(D, SV.lab(D, dup="own", rerun="own"), vol_m))
    n = crack[1]
    sc = 45 + 55.0 * crack[0] / n
    sm = 12 + 55.0 * mirror[0] / n
    print("cracker on the call keeps %d of %d ask figures: %.1f" % (crack[0], n, sc))
    print("mirror off the call keeps %d of %d ask figures: %.1f" % (mirror[0], n, sm))
    print("Pair ceiling: %.1f" % ((sc + sm) / 2))
    print("Mirror leakage: %.1f per cent of the ask weight" % (100.0 * mirror[0] / n))


if __name__ == "__main__":
    main()
