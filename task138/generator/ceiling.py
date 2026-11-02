"""Pair ceiling on the cut pack: the cracker (lands the call, links every file it can, pairs the unlabelled Holter
recordings in recording order) and the mirror (stops on the 24-hour own-exponent line, same ask handling).
Weights: 38 main and critical components, 7 instruction-following, 55 asks.
Run: python3 ceiling.py <target_dir> <figures.json>"""
import json
import sys

import analysis as A

MAIN = dict(call=14.0, c_high=3.0, below10=2.0, chart_part=2.25)
IF = 7.0
ASK = 55.0


def score(target, figs):
    F = A.golden(target)
    D, recs, owner = F["D"], F["recs"], F["owner"]
    n_ask = 5 + 8
    w = ASK / n_ask

    def ask_hits(pairing):
        hits = 0
        gm = A.ask_a(D)[0]
        hits += sum(A.sig2(gm[d])[0] == figs["auc_sad_%d" % d] for d in gm)
        nb = A.ask_b(D, recs, owner, pairing)[0]
        hits += sum(round(v + 0.0, 1) == figs["night_hr_%s_%d" % k] for k, v in nb.items())
        return hits

    naive = A.naive_pairing(recs, owner)
    # cracker: on the call
    hc = ask_hits(naive)
    main_c = MAIN["call"] + 3 * MAIN["c_high"] + 3 * MAIN["below10"] + 4 * MAIN["chart_part"]
    C = main_c + IF + w * hc
    # mirror: the 24-hour own line, 25 mg; exposures right, 50 mg wrongly over the bound
    mir = F["rungs"]["pooled_own"]
    below = sum(("yes" if mir["ubs"][d] < 10 else "no") == figs["below10_%d" % d] for d in (25, 50, 100))
    main_m = 3 * MAIN["c_high"] + below * MAIN["below10"] + 2 * MAIN["chart_part"]
    hm = ask_hits(naive)
    S = main_m + IF + w * hm
    full = main_c + IF + w * ask_hits(F["pairing"])
    out = dict(cracker=round(C, 1), mirror=round(S, 1), pair=round((C + S) / 2, 1),
               cracker_ask_keep=round(hc / n_ask, 3), mirror_ask_keep=round(hm / n_ask, 3),
               mirror_call=mir["call"], full_includer_pair=round((full + S) / 2, 1))
    return out


if __name__ == "__main__":
    figs = json.load(open(sys.argv[2]))
    r = score(sys.argv[1], figs)
    for k, v in r.items():
        print("%s: %s" % (k, v))
    ok = r["pair"] <= 60 and r["mirror_ask_keep"] < 0.5
    print("CEILING %s" % ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
