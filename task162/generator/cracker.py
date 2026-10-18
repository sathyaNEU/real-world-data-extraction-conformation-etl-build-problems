"""task162 pair ceiling (supplemental-stumping Part 0 and Part 7), on the rubric weights the 40 bar was calibrated on:
the call and its critical components 38, the instructions 7, the asks 55 over every ask criterion (Ask A's 8 weekly
figures, Ask B's 8 group figures, the chart's content and its parts).

The cracker lands the call, executes every filed definition, drops the re-sent copies on the old bug number, finds the
moved reports, replays each report's state at the run's end; its natural readings of a report's filing time are each
run as a path: the new tracker's created, the old tracker's opened through Legacy bug (reports without the field
dropped, or read from created), and the same with a moved report's number read from its changelog. The mirror stops
at R1 (6 triagers) and reads the triage project as it stands. Every route is executed on the cut pack by calc.py.

    python3 task162/generator/cracker.py [target]"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def main(target=None):
    import calc as C
    rep = C.ceiling_report(target)
    ok = rep["pair"] <= 40 and rep["mirror_leakage"] < 35
    print("natural paths: pair ceiling %.1f (the worst), mirror leakage %.1f per cent; every device found: pair %.1f"
          % (rep["pair"], rep["mirror_leakage"], rep["pairs"]["cracker_full"]["pair"]))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
