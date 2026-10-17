"""task242 pair measurement on the cut pack: the cracker (lands the call, runs the hygiene battery, executes every filed
rule) and the mirror (stops at the default path on the call) each answer both asks the way that path does, and every
ask figure is scored against the golden at the stated rounding. The mirror's share of the call's per-zone criteria is
measured too (the zones it leaves unflagged rightly, the estimates its single sensitivity lands within the band). Prints
the cracker sheet, the mirror's leakage and the pair ceiling.

    python3 task242/generator/pair.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
import estim as E
import writeup as WU

TARGET = os.path.join(os.path.dirname(HERE), "target")


def main():
    D = E.load(TARGET, B.FILES)
    gold_a, gold_b = E.breteau(D), E.response(D)
    paths = {
        # the cracker: exact repeats dropped, the SOP's locked calls and follow-ups handled, the ward number joined to the
        # ward master; a responding household is one with a tested resident in the results file
        "cracker": (E.breteau(D, zone_from="ward", keep="inspected"), E.response(D, numerator="results")),
        # the mirror, careful on the asks as the cracker is
        "mirror": (E.breteau(D, zone_from="ward", keep="inspected"), E.response(D, numerator="results")),
        # the mirror, careless on the asks: every form counted, a completed interview as a response
        "mirror_careless": (E.breteau(D, zone_from="ward", keep="all"), E.response(D, numerator="outcome")),
    }
    n = 2 * len(E.ZONES)
    keep = {}
    for k, (a, b) in paths.items():
        hits = [("A " + z) for z in E.ZONES if round(a[z], 1) == round(gold_a[z], 1)] + \
               [("B " + z) for z in E.ZONES if round(b[z], 1) == round(gold_b[z], 1)]
        keep[k] = len(hits) / n
        print("%-16s keeps %d of %d ask figures %s" % (k, len(hits), n, hits))
    g = E.call(D, "golden")
    m = E.call(D, "from5")
    flags_right = sum(g[z]["flag"] == m[z]["flag"] for z in E.ZONES)
    est_in = sum(abs(m[z]["A"] / g[z]["A"] - 1) < WU.BAND for z in E.ZONES)
    share = (flags_right + est_in + 12) / 36.0       # flags, estimates and published shares, one criterion each
    r_miss = round(38 * 0.75 * share, 1)              # the call itself (a quarter of the weight) is lost
    print("mirror on the call: %d of 12 flags right (the unflagged zones), %d of 12 estimates within the band; "
          "keeps %.1f of the 38 recommendation points" % (flags_right, est_in, r_miss))
    lc, ls = keep["cracker"], max(keep["mirror"], keep["mirror_careless"])
    c, s = 38 + 7 + 55 * lc, r_miss + 7 + 55 * ls
    print("Pair ceiling: %.1f" % ((c + s) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * ls))
    return (c + s) / 2, 100 * ls


if __name__ == "__main__":
    main()
