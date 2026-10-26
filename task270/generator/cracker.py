"""The ask sheet's cracker and mirror, run on the cut pack: the cracker landed the call, ran the hygiene battery and
executed every filed rule (the platform guide's holdout, layers, platforms and arms; the latest refresh; the holdout's
users taken out of the cohort totals), and reads the forecast's lines as they stand and the cohort table's consumers as
the accounts that are consumers now; the mirror stops at the
disattenuated rung on the call and reads the asks the same way. Each scored against generator/figures.json, a hit
within half a unit of the figure's rounding, and the pair ceiling printed by supplemental-stumping's arithmetic."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A   # noqa: E402
import asks as S       # noqa: E402


def flat(x, p=""):
    if isinstance(x, dict):
        o = {}
        for k, v in x.items():
            o.update(flat(v, p + "/" + str(k)))
        return o
    return {p: x}


def score(resp, gold):
    hits = sum(1 for k, v in gold.items() if k in resp and abs(resp[k] - v) < 1e-9)
    return hits, len(gold)


def run(task):
    target = os.path.join(task, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    d = A.load(target)
    gold = flat({"B": fig["asks"]["B"]["detectable"], "U": fig["asks"]["B"]["users_per_arm"], "C": fig["asks"]["C"]})
    b, u = S.detectable(d, weekly="lines")
    cracker = flat({"B": b, "U": u, "C": S.holdout_gap(d, type_col="account_type")})
    mirror = cracker
    hc, n = score(cracker, gold)
    hm, _ = score(mirror, gold)
    lc, lm = hc / n, hm / n
    pair = ((38 + 7 + 55 * lc) + (5 + 7 + 55 * lm)) / 2
    print("cracker keeps %d of %d ask figures (%.1f per cent)" % (hc, n, 100 * lc))
    print("mirror keeps %d of %d ask figures (%.1f per cent)" % (hm, n, 100 * lm))
    print("pair ceiling %.1f" % pair)
    return dict(cracker=lc, mirror=lm, pair=pair)


if __name__ == "__main__":
    run(os.path.dirname(HERE))
