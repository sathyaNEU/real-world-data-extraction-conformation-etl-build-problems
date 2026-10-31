"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling, and the pair priced on the planning weights
(38 for the call and its components, 7 for instruction-following, 55 for the asks).

    python3 task125/generator/ceiling.py

Rows. The cracker lands the call (each unit's load carried down from its inflows), runs the battery (the latest
return for a month, the laboratory's re-runs, the loggers' UTC clock read as SAST, the totaliser readings
differenced and the inspection's final reading at Silwane's meter change) and executes every filed rule, but takes
each return's sulfate as it stands and each logger's readings as they stand, telemetry only. The mirror stops at the
boundary samples on the call and handles the asks the same way, since they carry nothing from the call. The full
includer also restates the three mines' as-S sulfate, takes the loggers' fouling drift off and fills their gaps from
the memory downloads (a stress row, not the gate). The workbook's unit-load table is banked by every response that
builds it from its own call, so it is scored with the call, not here."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import figs as F  # noqa: E402

BANKED = 1        # the brief's chart structure


def score(a, b, ga, gb):
    ka = sum(round(a[k], -1) == round(ga[k], -1) for k in ga)
    kb = sum(b[k] == gb[k] for k in gb)
    return ka, kb


def main(target=TARGET):
    ga, gb = F.ask_a(target), F.ask_b(target)
    n = len(ga) + len(gb) + BANKED
    ca, cb = score(F.ask_a(target, as_s="raw"), F.ask_b(target, drift="none", memory=False), ga, gb)
    fa, fb = score(F.ask_a(target), F.ask_b(target), ga, gb)
    crack = ca + cb + BANKED
    lc = crack / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    print("cracker (lands the call, battery, filed rules; the returns' sulfate and the loggers' readings as they "
          "stand, telemetry only): keeps %d of %d ask criteria (A %d of %d, B %d of %d), response %.1f"
          % (crack, n, ca, len(ga), cb, len(gb), c))
    print("mirror (the boundary samples on the call, same ask handling): keeps %d of %d, response %.1f" % (crack, n, s))
    print("full includer (as-S restated, drift off, gaps filled; stress row): keeps %d of %d, response %.1f"
          % (fa + fb + BANKED, n, 38 + 7 + 55 * (fa + fb + BANKED) / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * lc))
    return (c + s) / 2, 100 * lc


if __name__ == "__main__":
    main()
