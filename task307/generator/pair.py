"""The ask sheet's measurement on the cut pack: the cracker (lands the call, executes every filed rule, runs the
battery) and the mirror (the fixed-volume call), scored figure by figure on the 38/7/55 weights, with every path each
ask offers a response that does not meet its device.

    python3 task307/generator/pair.py <target dir>
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A  # noqa: E402
import pack  # noqa: E402

REC, IF, ASK = 38.0, 7.0, 55.0


def rnd(v, u):
    return math.floor(v / u + 0.5) * u


def main(target):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    n = pack.Net(target)
    fx = n.fixed()
    m_call = int(fx["best"] == F["award"])
    m_call += sum(rnd(fx[k]["annual"], 1000) == F["annual_vh"][k] for k in F["annual_vh"])
    m_call += sum(rnd(fx[k]["per_m"], 100) == F["per_musd_vh"][k] for k in F["per_musd_vh"])
    cnt = A.Counts(target)

    def h1(p):
        return (sum(rnd(p[s]["aadt"], 1) == F["aadt"][s] for s in p),
                sum("%.3f" % rnd(p[s]["k"], 0.001) == F["k_factor"][s] for s in p))

    def h2(p):
        return sum("%.1f" % rnd(v["pct"], 0.1) == F["validation_pct"]["%s %s %s" % k] for k, v in p.items())

    p1 = {"the filed rules only: status OK, carried polls dropped, AASHTO on valid days (the cracker)": dict(faults=False),
          "status OK in both directions only": dict(faults=False, carry=False),
          "the loop faults found, the carried polls kept": dict(carry=False),
          "the carried polls dropped, the faults kept": dict(faults=False),
          "every hour after an NR dropped, whole-day outages too": dict(carry_after_spell=True)}
    print("ask 1, AADT and K-factor by station (16 figures):")
    keep1 = 0
    for name, kw in p1.items():
        a, k = h1(cnt.ask1(**kw))
        print("   %-92s AADT %d of 8, K %d of 8" % (name, a, k))
        if "cracker" in name:
            keep1 = a + k
    print("   the plain mean of valid days (no AASHTO): AADT %d of 8" %
          sum(rnd(cnt.aadt(s, method="mean"), 1) == F["aadt"][s] for s in cnt.stations))
    p2 = {"the filed rules only (the cracker)": dict(faults=False), "the faults found": dict()}
    print("ask 2, base-year validation (12 figures):")
    keep2 = 0
    for name, kw in p2.items():
        v = h2(cnt.ask2(target, **kw))
        print("   %-92s %d of 12" % (name, v))
        if "cracker" in name:
            keep2 = v
    ls = (keep1 + keep2) / 28.0
    cracker = REC + IF + ASK * ls
    mirror = REC * m_call / 9.0 + IF + ASK * ls
    print("mirror call figures right: %d of 9" % m_call)
    print("cracker: %.1f, mirror: %.1f" % (cracker, mirror))
    print("Pair ceiling: %.1f" % ((cracker + mirror) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * ls))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
