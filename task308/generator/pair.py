"""The ask sheet's measurement on the cut pack: the cracker (lands the call, executes every filed rule, runs the
battery) and the mirror (the rated-peaker call), scored figure by figure on the 38/7/55 weights, with every path
each ask offers a response that does not meet its device.

    python3 task308/generator/pair.py <target dir>
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build  # noqa: E402
import params as P  # noqa: E402
import solve as S  # noqa: E402

REC, IF, ASK = 38.0, 7.0, 55.0


def hits(path, gold, unit):
    return sum(1 for k in P.MEMBERS if round(path[k] / unit) == round(gold[k] / unit))


def call_hits(c, gold):
    n = int(c["best"] == gold["best"])
    n += int(round(c["base"] / 100) == round(gold["base"] / 100))
    for o in P.OFFERS:
        n += int(round(c["removed"][o] / 100) == round(gold["removed"][o] / 100))
        n += int(round(c["net"][o]) == round(gold["net"][o]))
    return n


def main(target):
    pk = S.Pack(target, build.FILES)
    g = pk.call("golden")
    mirror = pk.call("rated")
    call_n = 10
    m_call = call_hits(mirror, g)
    m = S.Meter(target, build.FILES)
    A = m.energy()
    B, _ = m.cp12()
    pa = {"every latest interval summed as exported, delivered less received (the natural read)": m.energy(fix_mult=False),
          "the natural read with each point on its year-end member": m.energy(fix_mult=False, transfer=False),
          "delivered only": m.energy(fix_mult=False, net=False)}
    pb = {"the natural read: export stamps and multipliers as they stand": m.cp12(fix_mult=False, fix_clock=False)[0],
          "the natural read on delivered only": m.cp12(fix_mult=False, fix_clock=False, net=False)[0]}
    met_b = {"the multiplier repaired, the clocks not": m.cp12(fix_clock=False)[0],
             "the clocks repaired, the multipliers not": m.cp12(fix_mult=False)[0]}
    ha = {k: hits(v, A, 1.0) for k, v in pa.items()}
    hb = {k: hits(v, B, 0.1) for k, v in pb.items()}
    print("ask A, 2025 net energy by member (8 figures):")
    for k, v in ha.items():
        print("   %-88s %d of 8" % (k, v))
    print("ask B, 2025 12-CP average by member (8 figures):")
    for k, v in hb.items():
        print("   %-88s %d of 8" % (k, v))
    print("ask B, stops after meeting one of its two devices (the ladder):")
    for k, v in met_b.items():
        print("   %-88s %d of 8" % (k, hits(v, B, 0.1)))
    keep = max(ha.values()) + max(hb.values())
    ls = keep / 16.0
    cracker = REC + IF + ASK * ls
    mirror_s = REC * m_call / call_n + IF + ASK * ls
    pair = (cracker + mirror_s) / 2
    print("mirror call figures right: %d of %d (the award and the peaker's two figures wrong)" % (m_call, call_n))
    print("cracker: %.1f, mirror: %.1f" % (cracker, mirror_s))
    print("Pair ceiling: %.1f" % pair)
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * ls))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(build.TASK, "target")))
