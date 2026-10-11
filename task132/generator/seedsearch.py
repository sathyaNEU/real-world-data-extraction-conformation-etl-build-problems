"""Search world seeds for a draw whose ladder separates cleanly; prints one line per seed."""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W

KEYS = ["window_no_renewal", "install_renewal", "install_no_renewal", "relay_age_window_no_renewal", "trailing_rate",
        "station_first_stage", "station_last_stage", "plan_2025", "all_psu_wos", "window_hold_band_no_renewal"]


def main(seeds, scale=None):
    import build as B
    import estimators as E
    if scale:
        W.WEIBULL_SCALE = scale
    tmp = tempfile.mkdtemp()
    for sd in seeds:
        W.SEED = sd
        W.TUNE = ()
        B.build(tmp)
        r, avail = E.rungs(tmp)
        ans, L = r["ANSWER"]
        land = [k for k in KEYS if r[k][1] == L]
        print(sd, "ans %.1f L%d" % (ans, L), " ".join("%s %+.0f%%/%+d" % (k[:12], 100 * (r[k][0] / ans - 1), r[k][1] - L) for k in KEYS),
              "LAND:" + ",".join(land), flush=True)


if __name__ == "__main__":
    main(range(int(sys.argv[1]), int(sys.argv[2])), float(sys.argv[3]) if len(sys.argv) > 3 else None)
