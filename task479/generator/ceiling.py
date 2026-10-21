"""The ask layer measured on the cut pack: the cracker (lands the call, runs the hygiene battery, keeps the later
submission of a resubmitted month, takes each report's county from the county code the report carries as the
dictionary describes it, and links the legacy properties through the crosswalk, trying the property name for the ones
it misses) and the mirror (the default path on the call, the asks handled the cracker's way), priced against
generator/figures.json on the weights 38 / 7 / 55.

    python3 task479/generator/ceiling.py [target]

The call is 38: the qualifying set 10 and the sixteen counties' growth figures 28 / 16 each. Instructions 7. The 64
ask figures (sixteen counties' occupancy, rate, rooms share and rooms change) are 55 / 64 each. A figure is kept when
it prints in the golden's cell at the ask's rounding. The asks consume nothing the call's construction produces, so
the cracker and the mirror take the same ask readings; checks.py X1 and X2 prove the separation."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B    # noqa: E402

TASK = os.path.dirname(HERE)
ASK_W = 55.0 / 64


def main(target=None):
    target = target or os.path.join(TASK, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    b = B.load(target)
    A = B.ask_a(b, "report")
    Bx = B.ask_b(b, "name")
    ka_o = sum(c in A and "%.1f" % A[c][0] == fig["ask_a"][c]["occupancy_pct"] for c in fig["ask_a"])
    ka_r = sum(c in A and "%.2f" % A[c][1] == fig["ask_a"][c]["adr_usd"] for c in fig["ask_a"])
    kb_s = sum("%.1f" % Bx[c][0] == fig["ask_b"][c]["rooms_share_pct"] for c in fig["ask_b"])
    kb_c = sum("%.1f" % Bx[c][1] == fig["ask_b"][c]["rooms_change_pct"] for c in fig["ask_b"])
    kept = ka_o + ka_r + kb_s + kb_c
    print("Ask A occupancy kept %d of 16, average daily rate kept %d of 16 (county from the report's code)" % (ka_o, ka_r))
    print("Ask B rooms share kept %d of 16, rooms change kept %d of 16 (crosswalk, then the property name)" % (kb_s, kb_c))
    C = 38 + 7 + ASK_W * kept
    g = B.growth(b, B.estimate(b, "flat_2024"))
    set_hit = B.qualify(b, B.estimate(b, "flat_2024")) == fig["call"]["qualifying"]
    rates = sum(int(round(100 * g[c])) == fig["growth_pct"][c] for c in g)
    m = 10 * set_hit + 28.0 / 16 * rates
    S = m + 7 + ASK_W * kept
    print("cracker: call landed (38), instructions (7), ask figures kept %d of 64: %.1f" % (kept, C))
    print("mirror (the default path): main block %.1f (set %s, %d growth figures kept), ask figures kept %d of 64: %.1f"
          % (m, "landed" if set_hit else "missed", rates, kept, S))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * kept / 64))
    print("Pair ceiling: %.1f" % ((C + S) / 2))
    return (C + S) / 2


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
