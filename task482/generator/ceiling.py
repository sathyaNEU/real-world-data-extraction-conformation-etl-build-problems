"""The ask layer's pair ceiling on the cut pack (supplemental-stumping Part 0 and 1.1).

    python3 task482/generator/ceiling.py

The cracker lands the call, runs the hygiene battery and executes every filed rule: it applies amended and
supplemental returns as the ordinance says, splits each stay over its nights at the rate in force each night, and reads
the date in Kettle & Pine's reservation reference as each stay's arrival, the one date that file carries beside its
reporting period; it multiplies the pond systems' effluent flow by the days they discharged and every other plant's
by the days of the month, and keeps each e-reporting period's latest submission. The mirror stops at the default rung (residents plus the recorded paid stays) and does
everything else as the cracker does. Two sensitivity rows price a cracker that also finds one of the devices. Each
graded ask figure is scored against figures.json at the prompt's rounding."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import golden as G  # noqa: E402


def keep_a(figs, a):
    return sum(a[(n, q)] == figs["ask_a"][n]["q%d" % q] for n in G.TOWNS for q in (1, 2, 3, 4)), 32


def keep_b(figs, b):
    return sum(abs(b[(n, h)] - figs["ask_b"][n]["h%d" % h]) < 1e-9 for n in G.PLANTS_B for h in (1, 2)), 14


def pair(ka, kb, total):
    lc = (ka + kb) / float(total)
    C = 38 + 7 + 55 * lc
    S = 5 + 7 + 55 * lc
    return lc, C, S, (C + S) / 2


def main():
    p = G.load(os.path.join(TASK, "target"))
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    gold = G.golden(p)
    rec = G.records_route(p)
    assert [n for n in G.TOWNS if gold[n]["qualifies"]] == figs["call"]["qualify"]
    assert [n for n in G.TOWNS if rec[n]["qualifies"]] != figs["call"]["qualify"]
    ga, ta = keep_a(figs, G.ask_a(p))
    gb, tb = keep_b(figs, G.ask_b(p))
    assert ga == ta and gb == tb, "the golden handling must reproduce every ask figure"
    total = ta + tb
    ca, _ = keep_a(figs, G.ask_a(p, ck="arrival"))
    cb, _ = keep_b(figs, G.ask_b(p, pond_days="discharged", edmr="latest"))
    na, _ = keep_a(figs, G.ask_a(p, ck="period", split_nights=False, returns="latest"))
    nb, _ = keep_b(figs, G.ask_b(p, edmr="latest"))
    print("| Ask | Graded figures | Cracker keeps | Mirror keeps | Naive handling keeps | Cracker |")
    print("|---|---|---|---|---|---|")
    for name, t, c, nv in (("A fee by city and quarter of fiscal 2026, whole dollars", ta, ca, na),
                           ("B total phosphorus by plant and half of 2025, one decimal", tb, cb, nb)):
        print("| %s | %d | %d | %d | %d | %s |" % (name, t, c, c, nv, "misses" if c == 0 else "keeps %d" % c))
    lc, C, S, P = pair(ca, cb, total)
    print()
    print("cracker keeps %.1f per cent of ask weight (scores %.1f with the call); mirror %.1f per cent (scores %.1f); "
          "naive %.1f per cent" % (100 * lc, C, 100 * lc, S, 100 * (na + nb) / float(total)))
    print("Pair ceiling: %.1f" % P)
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * lc))
    print()
    print("Sensitivity (a cracker that also finds one device):")
    for label, ka, kb in (
            ("reads Kettle & Pine's reference date as the departure (the fee across the rate change says so)",
             keep_a(figs, G.ask_a(p))[0], cb),
            ("takes the ponds' flow as the month's average and the latest accepted submission",
             ca, keep_b(figs, G.ask_b(p))[0])):
        lc_, C_, S_, P_ = pair(ka, kb, total)
        print("  %s: keeps %d of %d, pair %.1f" % (label, ka + kb, total, P_))
    return 0


if __name__ == "__main__":
    sys.exit(main())
