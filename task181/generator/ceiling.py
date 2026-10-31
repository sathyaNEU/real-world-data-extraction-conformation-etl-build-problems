"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files, and the pair priced on the
planning weights (38 for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task181/generator/ceiling.py

Rows. The cracker lands the call (it traces the trays to steriliser 3), runs the battery (latest record version,
cancelled bookings, returns to theatre, the principal line, the 2025 code change) and executes every filed rule, but
counts each booking as a procedure (an add-on booked on its own before the 2025 upgrade stays a second procedure)
and counts the surveillance export's infections under the consultant and date the export records, once per patient,
date and category. The mirror stops at the raw ratio against the limit on the call and handles the asks the same
way, since they carry nothing from the call. The full includer also merges the add-ons into their operations and
links each infection to its procedure (a stress row, not the gate). The chart's structure is banked by all."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import checks as K   # noqa: E402
import solve as S    # noqa: E402

BANKED = 1


def kept(resp, gold):
    return sum(resp.get(k, None) == v for k, v in gold.items())


def main():
    R = S.solve()
    D, P, inf = R["D"], R["P"], R["inf"]
    ga, gb = R["ask_a"], R["ask_b"]
    n = len(ga) + len(gb) + BANKED
    ca = S.ask_procedures(S.procedures(D, merge_addons=False))
    cb = K.cracker_infections(D)
    crack = kept(ca, ga) + kept(cb, gb) + BANKED
    fa = S.ask_procedures(P)
    fb = S.ask_infections(P, inf)
    full = kept(fa, ga) + kept(fb, gb) + BANKED
    lc = crack / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    print("cracker (lands the call, battery, filed rules; bookings counted as procedures, the export's own consultant "
          "and date): keeps %d of %d ask criteria (%d of %d procedures, %d of %d infections), response %.1f"
          % (crack, n, kept(ca, ga), len(ga), kept(cb, gb), len(gb), c))
    print("mirror (stops at the raw ratio, same ask handling): keeps %d of %d, response %.1f" % (crack, n, s))
    print("full includer (add-ons merged, infections linked to their procedures; stress row): keeps %d of %d, "
          "response %.1f" % (full, n, 38 + 7 + 55 * full / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    return (c + s) / 2, 100 * lc


if __name__ == "__main__":
    main()
