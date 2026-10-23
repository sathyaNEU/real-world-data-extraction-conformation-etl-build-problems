"""The pair ceiling on the cut pack (supplemental-stumping Part 0, on its 38, 7 and 55 weights).

The cracker lands the call (the unit's findings resolved strongest first, no person holding two records of one source)
and executes every filed rule the asks point at: the guide's night convention, bed-night services for the
night-by-night shelter and the head of household's move-in date. It reads ask A as each stay's nights plus the respite's
bed nights, summed by Continuum and quarter, and ask B as each head of household's move-in against the entry of the
enrollment that carries it. The mirror stops at the default path (every chain of links merged) and reads the asks the
same way, since the asks read no linkage finding (checks.py X1 and X2). The other rows give the cracker one more repair
at a time. A hit is a figure equal to the golden at its stated rounding.

    python3 task486/generator/ceiling.py [target]
"""
import os
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import bundle as B   # noqa: E402

W_REC, W_IF, W_ASK, R_WRONG = 38.0, 7.0, 55.0, 5.0


def figures(I, act, call, a_kw, b_kw):
    roots = I.resolve(constrained=(call == "golden"))
    cnt = I.counts(I.served(roots, act))
    am = B.allocation(cnt)
    out = {"call": tuple(am[k] for k in B.RECIPIENTS)}
    for k in B.RECIPIENTS:
        out["m|people|" + k] = cnt[k]
        out["m|amount|" + k] = am[k]
    out["m|people|ALL"] = sum(cnt.values())
    n = B.shelter_nights(I, **a_kw)
    for c in B.COCS:
        for q in range(4):
            out["A|%s|Q%d" % (c, q + 1)] = n[c][q]
    w = B.rrh_waits(I, **b_kw)
    for k in B.COCS + ["ALL"]:
        for t in B.TYPES:
            out["B|%s|%s" % (k, t)] = B.hround(w[(k, t)], 1)
    return out


def score(gold, resp):
    asks = [k for k in gold if k[:2] in ("A|", "B|")]
    main = [k for k in gold if k.startswith("m|")]
    kept = [k for k in asks if resp[k] == gold[k]]
    call = resp["call"] == gold["call"]
    mk = sum(1 for k in main if resp[k] == gold[k])
    rec = (W_REC * (0.4 + 0.6 * mk / len(main))) if call else R_WRONG
    return rec + W_IF + W_ASK * len(kept) / len(asks), kept, asks, call, mk, len(main)


CRACK_A = dict(dedup=False)                 # every stay's nights plus the respite's bed nights, summed
CRACK_B = dict(chain=None)                  # the head's move-in against its own enrollment's entry


def rows(I, act):
    return {
        "cracker": figures(I, act, "golden", CRACK_A, CRACK_B),
        "mirror": figures(I, act, "default", CRACK_A, CRACK_B),
        "cracker who counts a person's night once": figures(I, act, "golden", {}, CRACK_B),
        "cracker who drops the earlier of two overlapping stays": figures(I, act, "golden", dict(drop_earlier=True),
                                                                          CRACK_B),
        "cracker who follows same-day moves through heads of household": figures(I, act, "golden", CRACK_A,
                                                                                 dict(chain="hoh")),
        "cracker who follows same-day moves through any member": figures(I, act, "golden", CRACK_A, {}),
        "cracker who reads every row carrying a move-in date": figures(I, act, "golden", CRACK_A,
                                                                       dict(chain=None, rows="all")),
        "mirror who counts a person's night once": figures(I, act, "default", {}, CRACK_B),
        "cracker who does both asks": figures(I, act, "golden", {}, {}),
    }


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    I = B.Inputs(target)
    act = I.activity()
    gold = figures(I, act, "golden", {}, {})
    out = {}
    for name, resp in rows(I, act).items():
        sc, kept, asks, call, mk, nm = score(gold, resp)
        out[name] = (sc, kept, asks)
        ka = sum(1 for k in kept if k.startswith("A|"))
        kb = sum(1 for k in kept if k.startswith("B|"))
        print("%-64s call %-5s main %2d/%d  ask A %2d/16  ask B %2d/10  score %.1f" % (name, call, mk, nm, ka, kb, sc))
    sc, sm = out["cracker"][0], out["mirror"][0]
    worst = max((out[c][0] + out[m][0]) / 2 for c in ("cracker", "cracker who counts a person's night once")
                for m in ("mirror", "mirror who counts a person's night once"))
    print("Pair ceiling: %.1f (with the person-night repair on both: %.1f)" % ((sc + sm) / 2, worst))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * len(out["mirror"][1]) / len(out["mirror"][2])))
    return (sc + sm) / 2, worst


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
