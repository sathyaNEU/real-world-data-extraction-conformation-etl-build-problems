"""The ask layer measured on the cut pack: the cracker (lands the call, runs the hygiene battery, executes every filed
rule it points at) and the mirror (stops at the most attractive wrong rung, the default path) priced against
generator/figures.json.

    python3 task479/generator/ceiling.py [target]

Weights 38 / 7 / 55: the call 10 (the five 8, the county next in line 2) and the fourteen rates 2 each (28);
instructions 7; the 56 ask figures 55 / 56 each. A figure is kept when it prints in the golden's cell at the ask's
rounding."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B    # noqa: E402

TASK = os.path.dirname(HERE)
ASK_W = 55.0 / 56


def kept_a(golden, got, nm):
    c = sum(got[f][0] == golden[nm[f]]["claims"] for f in got)
    p = sum(int(round(got[f][1])) == golden[nm[f]]["payments"] for f in got)
    return c, p


def kept_b(golden, got, nm):
    c = sum(got[f][0] == golden[nm[f]]["buildings"] for f in got)
    s = sum(got[f][1] == golden[nm[f]]["federal_share"] for f in got)
    return c, s


def main_block(fig, res, nm):
    five, nxt = B.slate(res)
    gold_five = set(fig["call"]["five"])
    pts = 8 * (set(nm[f] for f in five) == gold_five) + 2 * (nm[nxt] == fig["call"]["next"])
    pts += 2 * sum("%.1f" % res[f][2] == fig["components"]["rates"][nm[f]] for f in res)
    return pts


def main(target=None):
    target = target or os.path.join(TASK, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    nm = B.load(target)["names"]
    ga, gb = fig["a_losses"], fig["b_pipeline"]
    print("Ask A, claims on 2026 losses with a building payment, and the payments")
    a_routes = {r: B.losses_2026(target, r) for r in B.A_ROUTES}
    for k, v in a_routes.items():
        print("  %-24s keeps claims %2d of 14, payments %2d of 14" % ((k,) + kept_a(ga, v, nm)))
    print("Ask B, buildings in projects not completed on 30 September 2026, and the federal share")
    b_routes = {r: B.pipeline(target, r) for r in B.B_ROUTES}
    for k, v in b_routes.items():
        print("  %-24s keeps buildings %2d of 14, federal share %2d of 14" % ((k,) + kept_b(gb, v, nm)))
    # the cracker: the hygiene battery's path. Claim numbers are unique and no row repeats; a building and date of
    # loss carried by more than one claim is resolved by keeping the latest record (the battery's repair), and a
    # project property is pending while its status says so, at the federal share the register gives it.
    ca = sum(kept_a(ga, a_routes["bdol_latest"], nm))
    cb = sum(kept_b(gb, b_routes["status"], nm))
    C = 38 + 7 + ASK_W * (ca + cb)
    # the mirror: the default path (every claim filed before a building's elevation dropped), its asks handled the
    # cracker's way
    m = main_block(fig, B.rates(target, "E1"), nm)
    S = m + 7 + ASK_W * (ca + cb)
    best_other = max(main_block(fig, B.rates(target, r), nm) for r in ("E0", "E2", "E3", "E7"))
    print()
    print("cracker: call landed (38), instructions (7), ask figures kept %d of 56 (A %d, B %d): %.1f" % (
        ca + cb, ca, cb, C))
    print("mirror (the default path): main block %.1f (the call missed, %d rates kept), ask figures kept %d of 56: %.1f"
          % (m, m // 2, ca + cb, S))
    print("best other wrong rung's main block: %.1f" % best_other)
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * (ca + cb) / 56))
    print("Pair ceiling: %.1f" % ((C + S) / 2))
    return (C + S) / 2


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
