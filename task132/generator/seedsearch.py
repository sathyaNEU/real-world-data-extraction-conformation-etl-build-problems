"""Search world seeds for a draw whose ladder separates cleanly; prints one line per seed."""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W


def main(seeds):
    import build as B
    import estimators as E
    tmp = tempfile.mkdtemp()
    for sd in seeds:
        W.SEED = sd
        W.TUNE = ()
        B.build(tmp)
        r, avail = E.rungs(tmp)
        ans = r["ANSWER"][0]
        tr = r["trailing_rate"][0] / ans - 1
        bi = r["banded_install"][0] / ans - 1
        # serviceable stock that would centre the answer in its lot bin (q95 = lam + 1.645 sqrt(lam))
        q = ans + 1.645 * ans ** 0.5
        lots = int(-(-(q - 39) // 25))
        print(sd, round(ans, 1), "trail %+.3f" % tr, "bandI %+.3f" % bi,
              "pooledW %+.3f" % (r["pooled_window"][0] / ans - 1), "lots@39", lots, flush=True)


if __name__ == "__main__":
    main(range(int(sys.argv[1]), int(sys.argv[2])))
