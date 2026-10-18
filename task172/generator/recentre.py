"""task172 re-centre rule (design note, Residual), executed: for every paperwork mean from 12 to 30 days the pack is
rebuilt in a scratch folder, the construction family and its one-sigma margin are read on it (ladder.margin), and the
generator's process 80th percentile for the quarter is taken (world.process_q80, 200 re-runs); the value chosen is the
one nearest 5.50 months among those whose family clears the margin. Not part of build.py (it takes about forty minutes).

    python3 task172/generator/recentre.py"""
from __future__ import annotations

import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as K      # noqa: E402
import common as C    # noqa: E402
import ladder as L    # noqa: E402
import pack as P      # noqa: E402
import world as Wm    # noqa: E402


def main():
    keep = Wm.PAPER_MEAN
    rows = []
    try:
        for pm in range(12, 31):
            Wm.PAPER_MEAN = pm
            tmp = tempfile.mkdtemp(prefix="t172_recentre_")
            try:
                W, R = P.records()
                P.build_pack(tmp, (W, R))
                Q = K.quote(tmp)
                mg = L.margin(Q)
            finally:
                shutil.rmtree(tmp)
            q, n, _ = Wm.process_q80(W)
            rows.append(dict(pm=pm, golden=Q["months"], lo=mg["lo"], hi=mg["hi"], ok=mg["ok"], process=q / C.MONTH_DAYS))
            print("PAPER_MEAN %2d  golden %.3f  family with one sigma %.3f to %.3f  edges %.3f %.3f  %s  process %.4f" % (
                pm, Q["months"], mg["lo"], mg["hi"], mg["edge_lo"], mg["edge_hi"], "clears" if mg["ok"] else "fails",
                q / C.MONTH_DAYS), flush=True)
    finally:
        Wm.PAPER_MEAN = keep
    ok = [r for r in rows if r["ok"]]
    if not ok:
        print("no value in the range clears the margin: report, do not loosen")
        return 1
    best = min(ok, key=lambda r: (abs(r["process"] - 5.5), r["pm"]))
    print("clear: %s; chosen %d (process %.4f); world.PAPER_MEAN is %d" % (
        ", ".join(str(r["pm"]) for r in ok), best["pm"], best["process"], keep))
    return 0 if best["pm"] == keep else 1


if __name__ == "__main__":
    sys.exit(main())
