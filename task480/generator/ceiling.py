"""The pair ceiling on the cut pack. The cracker lands the call (every county's 2027 NOx, its verdict and the set) and
runs the hygiene battery, executing every filed rule it points at: ask A by the voucher register's PAID vouchers per
applicant county, each priced at its tow zone's charge (Oakhaven's repeated invoice totals re-priced, as all four stage 4
readers did). The mirror stops at the most attractive wrong rung (R1, each vehicle's reading over its age) and takes the
asks by the same paths. Weights 38 / 7 / 55; the main block grades the set, each county's NOx and each county's
verdict (25); the ask is 8 figures."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import asks as A       # noqa: E402
import methods as M    # noqa: E402
import world as W      # noqa: E402

W_CALL, W_INSTR, W_ASK = 38.0, 7.0, 55.0


def r0(v):
    return int(v + 0.5)


def main(target=None, quiet=False):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    R = M.routes(target)
    gold, mir = R["golden"], R["R1"]
    gset, mset = M.designated(gold), M.designated(mir)
    keep = (gset == mset) + sum(r0(mir[c]) == r0(gold[c]) for c in W.NAMES) + \
        sum((mir[c] >= W.THRESHOLD_TONS) == (gold[c] >= W.THRESHOLD_TONS) for c in W.NAMES)
    p, pn = A.pilot_figures(target), A.pilot_figures(target, drop_reinstated=False)
    rows = []
    for c in W.PILOT_COUNTIES:
        rows.append(("A", "%s vehicles retired" % c, p[c]["n"], pn[c]["n"]))
        rows.append(("A", "%s dismantler charges ($)" % c, round(p[c]["charges"]), round(pn[c]["charges"])))
    hits = sum(g == x for _, _, g, x in rows)
    ask = W_ASK * hits / len(rows)
    cracker = W_CALL + W_INSTR + ask
    mirror = W_CALL * keep / 25.0 + W_INSTR + ask
    if not quiet:
        print("| ask | figure | golden | cracker's path | cracker |")
        print("|---|---|---|---|---|")
        for a, lab, g, x in rows:
            print("| %s | %s | %s | %s | %s |" % (a, lab, "{:,}".format(g), "{:,}".format(x), "hit" if g == x else "miss"))
        print("golden %s; mirror (R1) %s" % (gset, mset))
        print("mirror keeps %d of 25 main criteria; the cracker's ask paths keep %d of %d figures" % (keep, hits, len(rows)))
        print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage %.1f per cent of ask weight" % (
            cracker, mirror, (cracker + mirror) / 2, 100.0 * hits / len(rows)))
    return (cracker + mirror) / 2, 100.0 * hits / len(rows)


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else None
    pc, leak = main(t)
    sys.exit(0 if pc <= 40.0 and leak < 35.0 else 1)
