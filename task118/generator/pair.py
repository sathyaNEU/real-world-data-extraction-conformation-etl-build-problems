"""The pair ceiling on the cut pack (supplemental-stumping Part 0 weights: 38 call and components, 7 instructions, 55
asks). The cracker lands the call, runs the hygiene battery (the retired practice code joined through the register's
previous codes) and executes the falls definitions as filed (a stay runs on through a discharge to another hospital;
readmissions counted from the day the patient leaves hospital care, alive). What it has to build is the stay: each
path below is one way of executing F1's stay sentence. The mirror stops at a wrong rung of the call and handles the
asks the same way, since nothing in them touches the call. Each figure is scored against figures.json, exact.

    python3 task118/generator/pair.py [target]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve as SV  # noqa: E402

FIELDS = (("falls_65_79", "admissions for a fall aged 65 to 79"), ("falls_80", "admissions for a fall aged 80 or over"),
          ("bed_days", "bed-days"), ("readmitted", "readmitted within 30 days"))
PATHS = (
    ("each spell an admission (a move in is not an emergency admission)", dict(link="none")),
    ("each spell an admission, every emergency method on F1's list", dict(link="none", emergency=SV.EMERGENCY)),
    ("spells sorted by admission date, a discharge to another hospital joined to the next row", dict(link="shift")),
    ("a discharge to another hospital joined to a spell admitted from a hospital (source 49 to 53)",
     dict(link="dest_src")),
    ("a discharge to another hospital joined to a spell admitted by transfer (2B or 81)", dict(link="dest_method")),
    ("a discharge to another hospital joined to a spell admitted from a hospital or by transfer",
     dict(link="dest_either")),
    ("a discharge to another hospital joined to the spell beginning the same day", dict(link="dest", gap=0)),
    ("any spell beginning the day the last ended, or the next, joined (the battery's consecutive-spell merge)",
     dict(link="consecutive")),
)


def main(target):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    gold = fig["asks"]
    n = 4 * len(gold)
    best = {f: 0 for f, _ in FIELDS}
    for label, kw in PATHS:
        v = SV.asks(target, **kw)
        h = {f: sum(1 for k in gold if v[k][f] == gold[k][f]) for f, _ in FIELDS}
        for f in h:
            best[f] = max(best[f], h[f])
        print("  %-100s %s" % (label, " ".join("%d" % h[f] for f, _ in FIELDS)))
    crack = sum(best.values())
    mirror = crack
    c_score = 38 + 7 + 55.0 * crack / n
    m_score = 5 + 7 + 55.0 * mirror / n
    pair = (c_score + m_score) / 2
    for f, lab in FIELDS:
        print("  cracker keeps %d of 6 on %s" % (best[f], lab))
    print("cracker %.1f (call landed, %d of %d ask figures); mirror %.1f (off the call, %d of %d)" %
          (c_score, crack, n, m_score, mirror, n))
    print("Pair ceiling: %.1f" % pair)
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * mirror / n))
    full = SV.asks(target)
    keep = sum(1 for k in gold for f, _ in FIELDS if full[k][f] == gold[k][f])
    print("  if the cracker joins every move whatever its codes and its order: %d of %d, pair %.1f" % (
        keep, n, ((38 + 7 + 55.0 * keep / n) + m_score) / 2))
    print("  and if the mirror does too: pair %.1f" % (((38 + 7 + 55.0) + (5 + 7 + 55.0)) / 2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
