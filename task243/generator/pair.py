"""task243 pair measurement on the cut pack: the cracker (lands the call, runs the hygiene battery: exact repeats
dropped, residence spellings mapped, the year's births and deaths by their own dates, every filed definition executed)
and the mirror (stops at the default path on the call, the growth balance taken as closed) each answer both asks the way
that path does, and every ask figure is scored against the golden at one decimal. The mirror's share of the call's
per-LGU criteria is measured too (the alerts it gets right, the completeness it lands inside the accepted interval).
Prints the cracker sheet, the mirror's leakage and the pair ceiling.

    python3 task243/generator/pair.py [target]
    python3 task243/generator/pair.py --ladder      (the design note's ladder figures)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
import estim as E

TARGET = os.path.join(os.path.dirname(HERE), "target")


def main(target=TARGET):
    D = E.load(target, B.FILES)
    gold_a, gold_b = E.ask_a(D), E.ask_b(D)
    paths = {
        # the cracker: exact repeats dropped, residence spellings mapped, a birth per certificate, a certifier read by
        # the title written under the signature
        "cracker": (E.ask_a(D, dedupe="none"), E.ask_b(D, roster=False, dedupe=False)),
        # the cracker who also joins the certifiers to the roster but counts every certificate
        "cracker_roster": (E.ask_a(D, dedupe="none"), E.ask_b(D, roster=True, dedupe=False)),
        # the cracker who dedupes twins away with the repeats (mother and date of birth)
        "cracker_overclean": (E.ask_a(D, dedupe="mother_day"), E.ask_b(D, roster=False, dedupe=True)),
        # the mirror, careful on the asks as the cracker is
        "mirror": (E.ask_a(D, dedupe="none"), E.ask_b(D, roster=False, dedupe=False)),
    }
    n = 2 * len(E.CODES)
    keep = {}
    for k, (a, b) in paths.items():
        hits = [("A " + s) for c, s in zip(E.CODES, E.SHOW) if round(a[c], 1) == round(gold_a[c], 1)] + \
               [("B " + s) for c, s in zip(E.CODES, E.SHOW) if round(b[c], 1) == round(gold_b[c], 1)]
        keep[k] = len(hits) / n
        print("%-18s keeps %d of %d ask figures %s" % (k, len(hits), n, hits))
    g = E.call(D)
    m = E.rung(D, "closed")
    lo_hi = interval(D)
    flags_right = sum((m[c] < E.ALERT) == g[c]["alert"] for c in E.CODES)
    est_in = sum(lo_hi[c][0] <= round(100 * m[c]) <= lo_hi[c][1] for c in E.CODES)
    share = (flags_right + est_in) / 24.0
    r_miss = round(38 * 0.75 * share, 1)
    print("mirror on the call: %d of 12 alerts right, %d of 12 completeness figures inside the accepted interval; keeps "
          "%.1f of the 38 recommendation points" % (flags_right, est_in, r_miss))
    lc = max(keep["cracker"], keep["cracker_roster"], keep["cracker_overclean"])
    ls = keep["mirror"]
    c, s = 38 + 7 + 55 * lc, r_miss + 7 + 55 * ls
    print("Pair ceiling: %.1f" % ((c + s) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * ls))
    return (c + s) / 2, 100 * ls


def interval(D):
    """each LGU's accepted completeness, whole per cent, the readings' range rounded outward"""
    import math
    rd = E.readings(D)
    return {c: (math.floor(100 * min(rd[c])), math.ceil(100 * max(rd[c]))) for c in E.CODES}


def ladder(target=TARGET):
    """the design note's ladder figures: each rung's completeness and set, the readings' range, the other death
    distribution methods carrying the movement, and the asks' stops against the golden"""
    import checks as C
    X = E.solve(target, B.FILES)
    D = X["D"]
    fl = lambda v: [s for c, s in zip(E.CODES, E.SHOW) if v[c] < E.ALERT]
    for r in ("closed", "closed_trimmed", "seg", "in_province", "brass"):
        print("%-15s %s  %s" % (r, " ".join("%.3f" % X["rungs"][r][c] for c in E.CODES), fl(X["rungs"][r])))
    print("golden          %s  %s" % (" ".join("%.3f" % X["call"][c]["c"] for c in E.CODES), fl({c: X["call"][c]["c"] for c in E.CODES})))
    om = C.other_methods(D)
    for c, s in zip(E.CODES, E.SHOW):
        print("%-19s closed readings %.3f-%.3f  readings %.3f-%.3f (%d)  SEG and hybrid %.3f-%.3f  interval %s" % (
            s, min(X["closed_readings"][c]), max(X["closed_readings"][c]), min(X["readings"][c]), max(X["readings"][c]),
            len(X["readings"][c]), min(om[c]), max(om[c]), X["interval"][c]))
    g = [c for c in E.CODES if X["call"][c]["alert"]]
    print("readings: flagged max %.3f, others min %.3f; other methods: flagged max %.3f, others min %.3f" % (
        max(max(X["readings"][c]) for c in g), min(min(X["readings"][c]) for c in E.CODES if c not in g),
        max(max(om[c]) for c in g), min(min(om[c]) for c in E.CODES if c not in g)))
    print("net movers 50+ (census age, five years):", {s: X["counts"]["net_movers_50plus"][c] for c, s in zip(E.CODES, E.SHOW)})
    a, b = X["ask_a"], X["ask_b"]
    stops = {"A per certificate": E.ask_a(D, "none"), "A mother and day": E.ask_a(D, "mother_day"),
             "A registered in 2022": C.ask_a_registered(D), "A by registering office": C.ask_a_office(D)}
    stops.update({"B " + k: v for k, v in X["ask_b_paths"].items()})
    for k, s in stops.items():
        gold = a if k.startswith("A") else b
        dl = [s[c] - gold[c] for c in E.CODES]
        print("%-24s %+.1f to %+.1f, %d of 12 kept" % (k, min(dl), max(dl), sum(round(s[c], 1) == round(gold[c], 1) for c in E.CODES)))


if __name__ == "__main__":
    if "--ladder" in sys.argv:
        ladder()
    else:
        main(sys.argv[1] if len(sys.argv) > 1 else TARGET)
