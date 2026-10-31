"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files, and the pair priced on the
planning weights (38 for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task306/generator/ceiling.py

Rows: the cracker lands the call, runs the battery (each execution id once, pounds fills read as pence, cancelled
orders for their filled quantity) and executes every filed rule (the dated account register, value-weighting by
filled quantity at arrival), but measures the orders the backup system re-created after each failover from their own
arrival mids, since nothing keys them to the orders they continue, and reads each portfolio's orders off the
blotter's account codes, leaving the block orders on the desk's block account instead of taking each book's share
from the post-trade allocation export; the mirror stops at the size-blind rung on the
call and handles the asks the same way, since they carry nothing from it; the full includer also merges each
re-created order into its original and allocates the blocks (a stress row, not the gate)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402

BANKED = 0


def figures(P, failover, blocks):
    ex = A.allocated(P, A.with_size(P, A.executions(P, failover=failover)), blocks)
    a, b = A.ask_shortfall(P, ex), A.ask_traded(P, ex)
    return {k: round(v, 1) for k, v in a.items()}, {k: int(round(v / 1e6)) for k, v in b.items()}


def kept(resp, gold):
    return sum(resp[0][k] == v for k, v in gold[0].items()) + sum(resp[1][k] == v for k, v in gold[1].items())


def main(target=TARGET):
    P = A.Pack(target)
    gold = figures(P, True, True)
    n = len(gold[0]) + len(gold[1]) + BANKED
    crack = kept(figures(P, False, False), gold) + BANKED
    full = kept(figures(P, True, True), gold) + BANKED
    lc = crack / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    print("cracker (lands the call, battery, filed rules; re-created orders on their own, block orders left on the "
          "block account): keeps %d of "
          "%d ask criteria, response %.1f" % (crack, n, c))
    print("mirror (the size-blind rung, same ask handling): keeps %d of %d, response %.1f" % (crack, n, s))
    print("full includer (re-created orders merged, blocks allocated, stress row): keeps %d of %d, response %.1f"
          % (full, n, 38 + 7 + 55 * full / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    return (c + s) / 2, 100 * lc


if __name__ == "__main__":
    main()
