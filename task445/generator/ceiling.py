"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files, and the pair priced on the
planning weights (38 for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task445/generator/ceiling.py

Rows: the cracker lands the call (the register joined to both offices' logs), runs the battery (each register
entry once by its district and number under the latest-row rule that the battery applies to every amended record,
exact duplicate rows dropped, the south export's UTC stamps read as local dates) and executes every filed rule, and
counts each office's quarter on its cases, since nothing keys a referral the coroner sent back to the case the
office reopened for it; the mirror stops at the completed register on the call and handles the asks the same way,
since they carry nothing from it; the full includer also merges each office's cases on the person and reads each
entry on its registration row, version 1, for every field (a stress row, not the gate)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve as SV  # noqa: E402
import world as W  # noqa: E402

BANKED = 0


def figures(P, b_mode, c_mode):
    b = SV.ask_b(P, b_mode)
    c = SV.ask_c(P, c_mode)[0]
    return {k: int(v) for k, v in b.items()}, {k: SV.r1(v) for k, v in c.items()}


def kept(resp, gold):
    return sum(resp[0][k] == v for k, v in gold[0].items()) + sum(resp[1][k] == v for k, v in gold[1].items())


def main(target=W.TARGET):
    P = SV.Pack(target)
    gold = figures(P, "golden", "golden")
    n = len(gold[0]) + len(gold[1]) + BANKED
    crack = kept(figures(P, "rows", "latest"), gold) + BANKED
    full = kept(figures(P, "person", "first"), gold) + BANKED
    lc = crack / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    print("cracker (lands the call, battery, filed rules; each office's quarter counted on its cases, each amended "
          "entry read on its latest row): keeps %d of %d ask criteria, response %.1f" % (crack, n, c))
    print("mirror (the completed register on the call, same ask handling): keeps %d of %d, response %.1f" % (crack, n, s))
    print("full includer (cases merged on the person, every field off version 1, stress row): keeps %d of %d, "
          "response %.1f" % (full, n, 38 + 7 + 55 * full / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    return (c + s) / 2, 100 * lc, crack, full, n


if __name__ == "__main__":
    main()
