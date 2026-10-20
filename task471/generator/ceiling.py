"""The pair ceiling on the cut pack. The cracker lands the call and reads the asks the careful way: every filed rule
executed (accepted transactions, residential addresses, the window from the close of census day in each platform's
time basis, each person once, the platforms' death codes from the dictionary and the migration notes, reinstatements
netted), with the electorate numbers read as the concordance's current ones and one person to a reference, as the
round-1 readers took them; the mirror stops at the default path (dual-system estimates within the survey's cells) and
reads the asks the same way. Weights 38 / 7 / 55: the call 8, each of the 16 regions' organisers 1.875, each of the 32
ask figures 55/32. The sensitivity lines show what the cracker keeps if it also finds the old platform's 2020 numbers,
or the links REF_TXN makes, or both.

    python3 task471/generator/ceiling.py     exit 0 at 40 or under
"""
import os
import sys

import bundle as B
import calibrate as C
import methods as M
import world as W

W_CALL, W_ORG, W_INSTR, W_ASK = 8.0, 1.875, 7.0, 55.0 / 32
HERE = os.path.dirname(os.path.abspath(__file__))


def hits(a, b):
    return sum(1 for c in W.CODES if a[c] == b[c])


def main(target=None, quiet=False):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    pk = B.Pack(target)
    d = pk.d
    rg = C.rungs(d)
    gold = C.allocation(d, rg["R3 golden"])[0]
    ga, gb = pk.new_electors(), pk.removed_dead()

    def ask_keep(vintage, link):
        return (hits(pk.new_electors(vintage=vintage, link=link), ga) +
                hits(pk.removed_dead(vintage=vintage, reversals="all" if link else "rei"), gb))
    base = ask_keep(False, False)
    mirror_rungs = {k: hits(C.allocation(d, a)[0], gold) for k, a in rg.items() if k != "R3 golden"}
    best = max(mirror_rungs, key=mirror_rungs.get)
    cracker = W_CALL + W_ORG * 16 + W_INSTR + W_ASK * base
    mirror = W_ORG * mirror_rungs[best] + W_INSTR + W_ASK * base
    pair = (cracker + mirror) / 2
    if not quiet:
        print("best mirror %s keeps %d of the 16 regions' organisers" % (best, mirror_rungs[best]))
        print("the cracker's ask reading keeps %d of 32 ask figures" % base)
        print("cracker %.2f, mirror %.2f, pair ceiling %.1f, mirror leakage %.1f per cent of ask weight" % (
            cracker, mirror, pair, 100.0 * base / 32))
        for label, vintage, link in (("the old platform's 2020 electorate numbers found", True, False),
                                     ("the links REF_TXN makes found", False, True), ("both", True, True)):
            k = ask_keep(vintage, link)
            c2 = W_CALL + W_ORG * 16 + W_INSTR + W_ASK * k
            print("sensitivity, a cracker with %s: keeps %d of 32, cracker %.1f, pair %.1f" % (
                label, k, c2, (c2 + W_ORG * mirror_rungs[best] + W_INSTR + W_ASK * base) / 2))
    return pair


if __name__ == "__main__":
    sys.exit(0 if main() <= 40.0 else 1)
