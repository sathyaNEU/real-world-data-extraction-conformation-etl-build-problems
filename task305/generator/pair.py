"""The pair ceiling on the cut pack (supplemental-stumping Part 0 weights: 38 call and components, 7 instructions, 55
asks). The cracker lands the call, runs the hygiene battery and executes every filed rule (FIN-07's valuation, the plan
rates, the end of a cancelled subscription at its ended event, past-due subscriptions kept); the mirror stops at the
default rung and handles the bridge the same way. Each bridge figure is scored against figures.json, a hit within half a
pound.

    python3 task305/generator/pair.py [target]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve as S

PATHS = {
    "the billing platform's customer record as the customer": dict(key="customer"),
    "the account as the customer": dict(key="account"),
    "the subscription as the customer": dict(key="subscription"),
    "the customer record, a cancellation ending at its request": dict(key="customer", cancel="request"),
    "the customer record, past-due subscriptions left out": dict(key="customer", past_due=False),
    "the account, a cancellation ending at its request": dict(key="account", cancel="request"),
    "the person who pays, a cancellation ending at its request": dict(cancel="request"),
    "the person who pays, the opening at the 2025/26 plan rates": dict(fx_open="2025/26"),
    "the person who pays, past-due subscriptions left out": dict(past_due=False),
}
# a careful response reaches the person who pays only by joining records on two keys at once; the cracker's own
# handling is the billing customer or the account, with every filed rule executed
CRACKER = ("the billing platform's customer record as the customer", "the account as the customer",
           "the subscription as the customer")


def main(target):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    gold = fig["ask"]
    n = len(S.ASK_KEYS)
    kept = {}
    for name, kw in PATHS.items():
        x = S.bridge(target, **kw)
        kept[name] = sum(1 for k in S.ASK_KEYS if abs(x[k] - gold[k]) <= 0.5)
        print("  %-62s %2d of %d" % (name, kept[name], n))
    crack = max(kept[k] for k in CRACKER)
    half = max(kept.values())
    mirror = crack
    c_score = 38 + 7 + 55.0 * crack / n
    m_score = 5 + 7 + 55.0 * mirror / n
    print("cracker %.1f (call landed, %d of %d bridge figures); mirror %.1f (default rung, %d of %d)" % (
        c_score, crack, n, m_score, mirror, n))
    print("best half-handled stop: %d of %d" % (half, n))
    print("Pair ceiling: %.1f" % ((c_score + m_score) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * mirror / n))
    print("if both responses read the person who pays: pair %.1f" % (((38 + 7 + 55.0) + (5 + 7 + 55.0)) / 2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
