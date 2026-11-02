"""task304 architecture 5: the pair ceiling, scored on the cut pack (target/) by running each response's handling stops.

The cracker lands the call, runs the hygiene battery and executes every filed rule: on the annex it de-duplicates on
the reference (each record's own key), applies the fatal collision unit's 30-day deaths and leaves out the roads the
register gives to the strategic road network (by road number, the whole road). The mirror stops at the cluster-site
route on the call (each listed junction's 2021 to 2025 count as its expected count) and handles the annex as the
cracker does. Scores use the 38 / 7 / 55 weights: C = 38 + 7 + 55 Lc, S = r + 7 + 55 Ls, r the mirror's share of the
main side."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import analysis as AN  # noqa: E402


def r1(x):
    return float("%.1f" % (x + 1e-9))


def score():
    pk = AN.Pack(os.path.join(TASK, "target"))
    F = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    gold_a, gold_b = pk.ask_a(), pk.ask_b()
    crack_a = pk.ask_a(dedupe="ref", deaths="match", trunk="road")
    crack_b = pk.ask_b(dedupe="ref", deaths="match", trunk="road")
    hits_a = sum(crack_a[k] == gold_a[k] for k in gold_a)
    hits_b = sum(crack_b[k] == gold_b[k] for k in gold_b)
    n_ask = len(gold_a) + len(gold_b)
    Lc = (hits_a + hits_b) / n_ask
    Ls = Lc
    figs = pk.junction_figures()
    main_crit = len(figs) + 2                       # every junction's benefit, the junction, the runner-up
    mirror_hits = sum(r1(r["obs_benefit"]) == F["benefit"][r["name"]] for r in figs.values())
    r = 38.0 * mirror_hits / main_crit
    C = 38 + 7 + 55 * Lc
    S = r + 7 + 55 * Ls
    return dict(hits_a=hits_a, n_a=len(gold_a), hits_b=hits_b, n_b=len(gold_b), mirror_hits=mirror_hits,
                main_crit=main_crit, r=r, C=C, S=S, pair=(C + S) / 2, leak=100 * Ls,
                crack_a=crack_a, crack_b=crack_b, gold_a=gold_a, gold_b=gold_b)


def main():
    s = score()
    print("ask A cracker hits: %d of %d (re-sends kept twice, trunk by road number)" % (s["hits_a"], s["n_a"]))
    print("ask B cracker hits: %d of %d" % (s["hits_b"], s["n_b"]))
    print("mirror main-side hits: %d of %d -> r = %.1f" % (s["mirror_hits"], s["main_crit"], s["r"]))
    print("cracker C = %.1f, mirror S = %.1f" % (s["C"], s["S"]))
    print("Pair ceiling: %.1f" % s["pair"])
    print("Mirror leakage: %.1f per cent of ask weight" % s["leak"])
    return s


if __name__ == "__main__":
    main()
