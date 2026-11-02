"""The ask sheet's pair ceiling and mirror leakage, measured on the cut pack: the cracker (lands the call, runs the
hygiene battery, executes every filed rule it points at) and the mirror (the best response off the call, the coverage
rate rung, with the same ask handling), each ask figure kept only when it equals the golden at the stated precision.
Also prints each ask's ladder stops and the full includer."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import analysis as AN  # noqa: E402
import checks as CK  # noqa: E402

T = os.path.join(TASK_DIR, "target")


def kept1(path, gold):
    return sum(1 for ym in gold for pc in gold[ym] if path[ym].get(pc) == gold[ym][pc])


def kept2(path, gold):
    k = 0
    for pc in gold:
        k += (path[pc][0] == gold[pc][0]) + (path[pc][1] == gold[pc][1]) + (path[pc][2] == gold[pc][2])
    return k


def main():
    G = AN.golden(T)
    fam, fw = G["families"], G["fieldwork"]
    n1, n2 = sum(len(v) for v in fam.values()), 3 * len(fw)
    stops1 = {
        "granted rows, every hazard handled (the careful route)": CK.ask1_cracker(T),
        "the register's province column as residence": CK.ask1_cracker(T, "office"),
        "every open row counted (the review-month overlap)": CK.ask1_cracker(T, "rows"),
        "moves ignored": CK.ask1_cracker(T, "nomoves"),
        "revoked awards kept as standing at the cut-off (the full includer)": CK.ask1_cracker(T, revoked=True),
    }
    print("Ask 1 ladder (four quarter-end months by three provinces, families):")
    for name, path in stops1.items():
        print("  %-70s keeps %2d of %d" % (name, kept1(path, fam), n1))
    stops2 = {
        "each reference once at its last issue (the careful route)": CK.ask2_cracker(T),
        "the office as the province": CK.ask2_cracker(T, "office"),
    }
    print("Ask 2 ladder (eligible dwellings, complete interviews, response rate by province):")
    for name, path in stops2.items():
        print("  %-70s keeps %2d of %d" % (name, kept2(path, fw), n2))
    print("  %-70s keeps %2d of %d" % ("each reissue joined to the case it reissues (the full includer)", n2, n2))
    crack = kept1(stops1["granted rows, every hazard handled (the careful route)"], fam) + kept2(
        stops2["each reference once at its last issue (the careful route)"], fw)
    lc = crack / float(n1 + n2)
    L = AN.ladder(T)
    off = max(L["R1"], key=lambda m: L["R1"][m])
    lm = lc
    print("cracker: the call %s (landed), asks kept %d of %d (L = %.3f)" % (max(L["R3"], key=lambda m: L["R3"][m]),
                                                                         crack, n1 + n2, lc))
    print("mirror: the call %s (off, the coverage rate rung), the same ask handling (L = %.3f)" % (off, lm))
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lm
    print("Pair ceiling: %.1f ((38 + 7 + 55 x %.3f) and (5 + 7 + 55 x %.3f), averaged)" % ((c + s) / 2, lc, lm))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * lm))
    print("Full includer (both devices handled): L = 1.000, landed 100.0, off the call 67.0")


if __name__ == "__main__":
    main()
