"""The pair ceiling on the cut pack. The cracker lands the call and reads the asks the careful way the round-2 readers
did: every filed rule executed (accepted transactions, residential addresses, the window from the close of census day
in each platform's time basis, each person once, the platforms' death codes from the code list and the migration
notes), a person every record reference CORRECTS_TXN ties together, on the roll on census day if they have a removal in
the window, enrolments that put a removal right left out, reinstatements netted only where CORRECTS_TXN names the
removal, and the
electorate numbers read as the concordance's; the mirror stops at the default path (dual-system estimates within the
survey's cells) and reads the asks the same way. Weights 38 / 7 / 55: the call 8, each of the 16 regions' organisers
1.875, each of the 32 ask figures 55/32. The sensitivity lines climb the asks' ladder one find at a time.

    python3 task471/generator/ceiling.py     exit 0 at 40 or under
"""
import os
import sys

import bundle as B
import calibrate as C
import world as W

W_CALL, W_ORG, W_INSTR, W_ASK = 8.0, 1.875, 7.0, 55.0 / 32
HERE = os.path.dirname(os.path.abspath(__file__))
ROUND_2 = dict(person="reftxn", prior="any", reinstated=False, reversal_new="drop")
LADDER = [   # (label, new electors' reading, removals' reading), each adding one find to the one before
    ("the round-2 readers' reading", dict(vintage=False, **ROUND_2), dict(vintage=False, reversals="reftxn")),
    ("+ the old platform's 2020 numbers", dict(vintage=True, **ROUND_2), dict(vintage=True, reversals="reftxn")),
    ("+ a person an elector number, on the roll if a removal took off a record the window had not put on",
     dict(vintage=True, prior="record", reinstated=False), dict(vintage=True, reversals="reftxn")),
    ("+ reinstatements of removals made before census day as additions", dict(vintage=True),
     dict(vintage=True, reversals="reftxn")),
    ("+ reversals tied by the record, in the window", dict(vintage=True), dict(vintage=True, reversals="record_window")),
    ("+ reversals after the window (the golden)", dict(vintage=True), dict(vintage=True)),
]


def hits(a, b):
    return sum(1 for c in W.CODES if a[c] == b[c])


def main(target=None, quiet=False):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    pk = B.Pack(target)
    d = pk.d
    rg = C.rungs(d)
    gold = C.allocation(d, rg["R3 golden"])[0]
    ga, gb = pk.new_electors(), pk.removed_dead()
    keeps = [(lab, hits(pk.new_electors(**a), ga), hits(pk.removed_dead(**b), gb)) for lab, a, b in LADDER]
    base = keeps[0][1] + keeps[0][2]
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
        for lab, ka, kb in keeps[1:]:
            c2 = W_CALL + W_ORG * 16 + W_INSTR + W_ASK * (ka + kb)
            m2 = W_ORG * mirror_rungs[best] + W_INSTR + W_ASK * (ka + kb)
            print("sensitivity %s: keeps %d + %d of 32; cracker %.1f, pair %.1f; two such readers off the call %.1f" % (
                lab, ka, kb, c2, (c2 + mirror) / 2, m2))
    return pair


if __name__ == "__main__":
    sys.exit(0 if main() <= 40.0 else 1)
