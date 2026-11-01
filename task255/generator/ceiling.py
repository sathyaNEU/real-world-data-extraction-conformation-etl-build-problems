"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files, and the pair priced on the
planning weights (38 for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task255/generator/ceiling.py [target_dir]

Rows. The cracker lands the call and runs the battery: it reads the player log's UTC stamps in local time across
the clock change, dates each re-cabling by the receiving player's display report as terms 6.2 files it, counts a
taken-down screen as dark, applies the 0.5 per cent allowance and rounds up (6.3), but builds offline spells from
the log's OFFLINE and ONLINE pairs; it keeps each asset tag's latest register row on 1 January 2027 and leaves out
the screens held outside the packages; it splits the VAT out of the legacy invoices, nets every credit note through
its invoice number, and shares each agency statement's amount over the bookings it lists by their value net of
credit notes (8.2, settled on the statement). The mirror stops at the line map's rung on the call and handles the
asks the same way, since nothing in them comes from the call. The full includer also opens a spell for a player
whose first status in the log is ONLINE, keeps one screen to a register position and recovers each agency's
contract rate from its statement (a stress row, not the gate)."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as AN  # noqa: E402


def r10(v):
    return int(math.floor(v / 10.0 + 0.5)) * 10


def figures(target, mapping, screens_rule, commission, lead="state"):
    mg = AN.make_good(target, mapping=mapping, lead=lead)
    sc = AN.screens_on_sale(target, screens_rule)
    rv = AN.net_revenue(target, commission=commission)
    return ({k: v["make_good"] for k, v in mg.items()}, sc, {k: r10(v) for k, v in rv.items()})


def kept(resp, gold):
    return [sum(resp[i][k] == v for k, v in gold[i].items()) for i in range(3)]


def main(target):
    gold = figures(target, "cms", "golden", "rate")
    n = sum(len(g) for g in gold)
    crack = kept(figures(target, "cms", "latest_no_pos", "statements", lead="pairs"), gold)
    full = kept(gold, gold)
    lc = sum(crack) / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    print("ask criteria: make-good %d, screens %d, net revenue %d (%d in all)" % (len(gold[0]), len(gold[1]), len(gold[2]), n))
    print("cracker (lands the call, the battery, every filed rule): keeps %d, %d and %d of them (%d of %d), response %.1f"
          % (crack[0], crack[1], crack[2], sum(crack), n, c))
    print("mirror (the line map's rung, the same ask handling): keeps %d of %d, response %.1f" % (sum(crack), n, s))
    print("full includer (stress row): keeps %d of %d, response %.1f" % (sum(full), n, 38 + 7 + 55 * sum(full) / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    return (c + s) / 2, 100 * lc


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target"))
