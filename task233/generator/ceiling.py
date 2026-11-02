"""Pair ceiling on the cut pack: the cracker (on the call, hygiene run, every filed rule executed, the
asks handled the careful way without the reconstructions) and the mirror (the raw-agreement call, the
same ask handling), scored on the rubric's 38 / 7 / 55 split. A full includer row is the stress check.

    python3 ceiling.py <target_dir> <figures.json>
"""
import json
import sys

import analysis

W_CALL, W_INSTR, W_ASK = 38.0, 7.0, 55.0


def score(p, fig, outs, credit, tim, missed, acc):
    R = p.regions
    call_items = [outs[r] == fig["deliverables"][r]["outcome"] for r in R]
    call_items.append("{:,}".format(int(round(credit))) == fig["call"]["credit_dollars"])
    call = W_CALL * sum(call_items) / len(call_items)
    asks = []
    for r in R:
        asks.append("%.1f" % tim[r] == fig["deliverables"][r]["timeliness"])
        asks.append(missed[r] == fig["deliverables"][r]["missed_visits"])
        asks.append("%.1f" % acc[r] == fig["deliverables"][r]["replacement_acceptance"])
    kept = sum(asks) / len(asks)
    return call + W_INSTR + W_ASK * kept, kept, sum(asks), len(asks)


def main(target, figpath):
    fig = json.load(open(figpath))
    p = analysis.Pack(target)
    gold = p.golden()
    outs = p.outcomes(gold)
    credit = p.credit(outs)
    # the careful solver's ask handling: the schedule against the visit log with the holiday window, each
    # sold branch left where the schedule names it; decisions read latest-first per quote
    tim_c, miss_c = p.timeliness(follow_takeover=False)
    acc_c, _ = p.acceptance(assign="all")
    cr, ck, ch, n = score(p, fig, outs, credit, tim_c, miss_c, acc_c)
    agree = p.agreement()
    mo = p.outcomes(agree)
    mr, mk, mh, _ = score(p, fig, mo, p.credit(mo), tim_c, miss_c, acc_c)
    tim_g, miss_g = p.timeliness()
    acc_g, _ = p.acceptance()
    sr, sk, sh, _ = score(p, fig, outs, credit, tim_g, miss_g, acc_g)
    print("cracker  %.1f  (call landed, %d of %d ask figures kept)" % (cr, ch, n))
    print("mirror   %.1f  (raw-agreement call, %d of %d ask figures kept)" % (mr, mh, n))
    print("pair ceiling %.1f" % ((cr + mr) / 2))
    print("mirror leakage %.1f per cent of the ask weight" % (100 * mk))
    print("stress: full includer %.1f (%d of %d ask figures)" % (sr, sh, n))
    return (cr + mr) / 2


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
