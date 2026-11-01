"""The pair ceiling and the mirror's leakage, scored on the cut pack (target/) by real handling stops.

Weights (the client's split): the call and its critical components 38 (the call 14; each provider's outcome
and operations placed 1.2 each), instruction-following 7, the chart's form 3, the asks 52 over thirty
figures. A figure is kept when it rounds to the golden's whole number."""
import hashlib
import json
import os
import sys
import analysis as AN

W_CALL, W_EACH, W_IF, W_CHART, W_ASKS = 14.0, 1.2, 7.0, 3.0, 52.0


def rnd(x):
    import math
    return int(math.floor(x + 0.5))


def pack_digest(target):
    h = hashlib.sha256()
    for fn in sorted(os.listdir(target)):
        h.update(fn.encode())
        h.update(open(os.path.join(target, fn), "rb").read())
    return h.hexdigest()[:12]


def figures(res, main_key, askA_key, askB_key):
    out = {}
    sc = res["R"][main_key] if main_key in res["R"] else res["fam"][main_key]
    pl = res["place"][main_key]
    for u in sorted(sc):
        out["outcome_%s" % u] = rnd(sc[u])
        out["placed_%s" % u] = pl[u]
    out["call"] = tuple(sorted(u for u in pl if pl[u] > 0)) + (sum(pl.values()),)
    A = res["askA"][askA_key]
    for u in sorted(A):
        out["A_over52_%s" % u] = A[u]["over52"]
        out["A_within18_%s" % u] = rnd(A[u]["within18"])
    B = res["askB"][askB_key]
    for u in sorted(B):
        out["B_part_%s" % u] = rnd(B[u])
    return out


def score(fig, gold):
    s = W_IF + W_CHART
    s += W_CALL if fig["call"] == gold["call"] else 0.0
    main = [k for k in gold if k.startswith("outcome_") or k.startswith("placed_")]
    s += sum(W_EACH for k in main if fig[k] == gold[k])
    asks = [k for k in gold if k.startswith("A_") or k.startswith("B_")]
    kept = [k for k in asks if fig[k] == gold[k]]
    s += W_ASKS * len(kept) / len(asks)
    return s, kept, asks


def run(target):
    res = AN.run(target)
    gold = figures(res, "GOLD", "golden", "golden")
    routes = {
        "cracker": figures(res, "GOLD", "cracker", "cracker"),
        "mirror": figures(res, "R2_casemix_imputation", "cracker", "cracker"),
        "natural": figures(res, "R2_casemix_imputation", "natural", "natural"),
        "full_includer": figures(res, "GOLD", "golden", "golden"),
    }
    out = {"pack": pack_digest(target), "routes": {}}
    for k, f in routes.items():
        s, kept, asks = score(f, gold)
        out["routes"][k] = dict(score=round(s, 1), asks_kept=len(kept), asks=len(asks), kept=kept,
                                ask_share=round(100.0 * len(kept) / len(asks), 1))
    c, m = out["routes"]["cracker"], out["routes"]["mirror"]
    out["pair_ceiling"] = round((c["score"] + m["score"]) / 2.0, 1)
    out["mirror_leakage"] = m["ask_share"]
    out["pair_if_cracker_matches_keyless"] = round((out["routes"]["full_includer"]["score"] + m["score"]) / 2.0, 1)
    return out, res


if __name__ == "__main__":
    o, _ = run(sys.argv[1])
    print(json.dumps({k: v for k, v in o.items() if k != "routes"}, indent=1))
    for k, v in o["routes"].items():
        print(k, v["score"], "asks kept %d of %d" % (v["asks_kept"], v["asks"]), v["kept"][:12])
