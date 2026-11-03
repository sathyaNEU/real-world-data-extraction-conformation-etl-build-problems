"""Multi-seed sweep of the stage-2 harness (never shipped)."""
import sys
import world as W
import harness as H

keys = ["A_landmark", "A_landmark_band", "A_pooled", "A_agency_unbroken", "A_all_handovers", "A_first_kind",
        "C_golden", "C_default", "C_left", "B", "B_vs24", "D", "E", "A_default"]
seeds = [int(s) for s in sys.argv[1:]] or [402, 1, 2, 3, 4, 5]
print("seed " + " ".join(f"{k[:10]:>10s}" for k in keys) + "  broken  bef2  lw_emp  sa_rate se_rate")
for s in seeds:
    w = W.simulate(s)
    m = H.measure(w)
    r = H.price(m, w)
    xt = r["xtab"]
    try:
        lw_emp = int(xt.loc[(True, "employed"), "size"])
    except KeyError:
        lw_emp = 0
    try:
        sa = round(100 * xt.loc[(False, "agency"), "mean"], 1)
    except KeyError:
        sa = None
    se = round(100 * xt.loc[(False, "employed"), "mean"], 1)
    print(f"{s:4d} " + " ".join(f"{r[k]:10.1f}" for k in keys) +
          f"  {r['broken_n']:6d}  {r['broken_before2']:4d}  {lw_emp:6d}  {sa}  {se}")
