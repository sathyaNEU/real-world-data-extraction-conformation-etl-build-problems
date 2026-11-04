"""The pair ceiling on the cut pack, from the same code the golden runs. The cracker lands the call: it links every
tree not found to the added record standing on it, reads every filed rule (conditions, the September heights, the
volume rules) and so files the shares and the CSV, but it looks for added records only where a tree was not found,
so an added record standing on a tree the crew also entered under its found tag stays in its 2026 counts. The mirror
stops at the tag join and handles the asks as the cracker does. The full includer is the cracker that also merges
the found-tag entries. Weights 38 / 7 / 55: the call 14, the burned stands left unmarked 6, every stand's share 12,
the CSV's rows 3 and its re-tallied trees 3; instructions 7; every stand's 2026 live basal area per acre 27.5 and
its net volume per acre 27.5. A figure scores when it prints the golden's value at the asked rounding."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B   # noqa: E402
import golden as G   # noqa: E402
import world as W    # noqa: E402

W_CALL, W_BURN, W_SH, W_ROWS, W_RET, W_INSTR, W_BA, W_VOL = 14.0, 6.0, 12.0, 3.0, 3.0, 7.0, 27.5, 27.5


def score(d, gold, resp):
    stands = sorted(gold["shares"])
    burned = sorted(W.BURN_DATES)
    main = (W_CALL if resp["marked"] == gold["marked"] else 0) + \
        (W_BURN if not set(burned) & set(resp["marked"]) else 0)
    sh_hit = sum(1 for s in stands if G.r1(100 * resp["shares"][s]["share"]) == G.r1(100 * gold["shares"][s]["share"]))
    main += W_SH * sh_hit / len(stands)
    main += W_ROWS
    ret = [t for t in gold["res"]["retag"]]
    ret_hit = sum(1 for t in ret if resp["fate"][t][0] == "live")
    main += W_RET * ret_hit / len(ret)
    ba_hit = sum(1 for s in stands if G.r1(resp["pa"][s]["ba"]) == G.r1(gold["pa"][s]["ba"]))
    vol_hit = sum(1 for s in stands if G.r10(resp["pa"][s]["vol"]) == G.r10(gold["pa"][s]["vol"]))
    ask = W_BA * ba_hit / len(stands) + W_VOL * vol_hit / len(stands)
    return dict(total=main + W_INSTR + ask, main=main, ask=ask, sh=sh_hit, ba=ba_hit, vol=vol_hit, n=len(stands))


def main(target=None, quiet=False):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    d = B.load(target)
    gold = G.compute(d)
    cracker = G.compute(d, centric="M", dedupe=False)
    mirror = G.compute(d, route="TAG", dedupe=False)
    full = G.compute(d)
    c, m, f = score(d, gold, cracker), score(d, gold, mirror), score(d, gold, full)
    ceiling = (c["total"] + m["total"]) / 2
    if not quiet:
        for name, s in (("cracker", c), ("mirror", m), ("full includer", f)):
            print("%-13s %5.1f  (main %.1f, asks %.1f; shares %d of %d, live basal area %d of %d, volume %d of %d)" % (
                name, s["total"], s["main"], s["ask"], s["sh"], s["n"], s["ba"], s["n"], s["vol"], s["n"]))
        print("pair ceiling %.1f; mirror leakage %.1f per cent of ask weight; with the full includer on the call %.1f" % (
            ceiling, 100.0 * m["ask"] / (W_BA + W_VOL), (f["total"] + m["total"]) / 2))
    return ceiling


if __name__ == "__main__":
    sys.exit(0 if main() <= 60.0 else 1)
