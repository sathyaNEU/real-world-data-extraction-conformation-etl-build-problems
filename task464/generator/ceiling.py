#!/usr/bin/env python3
"""task464: the pair arithmetic behind the design note's `Pair ceiling:` and `Mirror leakage:` lines.

    python3 generator/ceiling.py

One row per response, the two scored from DIFFERENT ask readings (supplemental-stumping Part 7): the
response that lands the main call is the cracker, which runs the hygiene battery, executes every filed rule
and matches every control, and the response off the call is the mirror, which stops at the revealed volume
ceiling (rung 2). Weights are Part 0's, 38 for the recommendation and critical components, 7 for instruction
following and 55 for the asks, so builds are comparable.

At stage 2 the per-ask stop counts come from `## Ask sheet`'s cracker and mirror sheets, which are a model.
Stage 3 re-runs this script against the cut pack and the figures measured on it, and the gated fields take
the worst honest measurement.
"""
W_REC, W_INSTR, W_ASK = 38.0, 7.0, 55.0
REC_KEPT_OFF_CALL = 5.0        # what a wrong call keeps of the recommendation weight

# ask -> (graded figures, figures the cracker reaches, figures the mirror reaches)
ASKS = {
    "A out-of-network volume by area and half": (48, 0, 18),
    "B licensed supply by area":                 (24, 0, 10),
    "C the dropped sites by area":               (24, 0, 0),
}


def ask_share(which):
    total = sum(n for n, _, _ in ASKS.values())
    got = sum(c if which == "cracker" else m for _, c, m in ASKS.values())
    return got / total


def main():
    print("ask                                             figures  cracker  mirror")
    for name, (n, c, m) in ASKS.items():
        print("%-46s %7d %8d %7d" % (name, n, c, m))
    lc, ls = ask_share("cracker"), ask_share("mirror")
    cracker = W_REC + W_INSTR + W_ASK * lc
    mirror = REC_KEPT_OFF_CALL + W_INSTR + W_ASK * ls
    pair = (cracker + mirror) / 2.0
    print()
    print("cracker  lands the call, keeps %.3f of the ask weight -> %.1f" % (lc, cracker))
    print("mirror   stops at rung 2,     keeps %.3f of the ask weight -> %.1f" % (ls, mirror))
    print("Mirror leakage: %.1f per cent of ask weight (bar: under 35)" % (ls * 100.0))
    print("Pair ceiling: %.1f (build target 60, this build's brief 40)" % pair)
    print()
    for k in (0.10, 0.20, 0.30, 0.40):
        c2 = W_REC + W_INSTR + W_ASK * k
        print("  if the cut pack lets the cracker keep %.2f of the ask weight, the pair reads %.1f"
              % (k, (c2 + mirror) / 2.0))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
