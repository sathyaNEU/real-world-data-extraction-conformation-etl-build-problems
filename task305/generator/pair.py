"""The pair ceiling on the cut pack (supplemental-stumping Part 0 weights: 38 call and components, 7 instructions, 55
asks). The cracker lands the call, runs the hygiene battery and executes every filed rule; the mirror stops at the
resident route. Each ask figure is scored against figures.json, a hit within half a unit of the stated rounding.

    python3 task305/generator/pair.py <target dir>
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve as S


def score(got, gold):
    return sum(1 for k, v in gold.items() if k in got and abs(got[k] - v) < 0.5)


def main(target):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    A, B, C = fig["ask_a"], fig["ask_b"], fig["ask_c"]
    n = len(A) + len(B) + len(C)
    # the paths each response takes on each ask, computed on the pack
    paths = {
        "A natural (every DEL stop's cases, UK dates)": score(S.ask_a(target, "naive"), A),
        "A short stops dropped (under 15 minutes)": score(S.ask_a(target, "drop_short"), A),
        "A next-day repeats deduplicated": score(S.ask_a(target, "dedup_equal"), A),
        "B natural (paid hours by location)": score(S.ask_b(target, "location"), B),
        "B every line by its punch store": score(S.ask_b(target, "terminal_all"), B),
        "B exact duplicate lines removed": score(S.ask_b(target, "dedup_exact"), B),
        "B one line a colleague a day": score(S.ask_b(target, "dedup_day"), B),
        "B lines kept only where a clock-in falls": score(S.ask_b(target, "in_days"), B),
        "B exact duplicates removed, then clock-in dates only": score(S.ask_b(target, "exact_in_days"), B),
        "B clocked hours (punch to punch)": score(S.ask_b(target, "punch_hours"), B),
        "C natural (the day's services, every call)": score(S.ask_c(target, "naive"), C),
        "C half (the day's services before 24:00 only)": score(S.ask_c(target, "half"), C),
        "C both feeds counted": score(S.ask_c(target, "nodedup"), C),
        "C round-2 reader (both feeds as one set)": score(S.ask_c(target, "set"), C),
        "C round-3 reader (the larger feed's count of each call)": score(S.ask_c(target, "maxfeed"), C),
    }
    for k, v in paths.items():
        print("  %-62s %d" % (k, v))
    crack = paths["A natural (every DEL stop's cases, UK dates)"] + \
        max(v for k, v in paths.items() if k.startswith("B ")) + \
        max(v for k, v in paths.items() if k.startswith("C "))
    mirror = crack
    c_score = 38 + 7 + 55.0 * crack / n
    m_score = 5 + 7 + 55.0 * mirror / n
    pair = (c_score + m_score) / 2
    print("cracker %.1f (call landed, %d of %d ask figures); mirror %.1f (resident route, %d of %d)" %
          (c_score, crack, n, m_score, mirror, n))
    print("Pair ceiling: %.1f" % pair)
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * mirror / n))
    # sensitivity: the cracker reads one ask's device
    for lab, k in (("A", len(A)), ("B", len(B)), ("C", len(C))):
        print("  if the cracker reads ask %s's device: pair %.1f" % (lab, ((38 + 7 + 55.0 * (crack + k) / n) + m_score) / 2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
