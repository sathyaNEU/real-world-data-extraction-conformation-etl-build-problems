"""Expected window counts (sums of the Poisson means) for tuning the world before any seed is drawn."""
import numpy as np
from world import (population_tables, place_rates, N, NAMES, GROUPS, REP, PHI, SR, POB, DORMS, BARANGAYS)


def expected(weeks_win=(37, 40), year=2027):
    pop, grp, W, workers = population_tables()
    weeks, lh, lw, lo = place_rates()
    ts = [t for t, (y, w) in enumerate(weeks) if y == year and weeks_win[0] <= w <= weeks_win[1]]
    res = np.zeros((N, 4)); place = np.zeros(N)
    for t in ts:
        for i in range(N):
            for gi, g in enumerate(GROUPS):
                n = grp[i, gi]
                if g != "employed":
                    m = n * REP[g] * lh[t, i]; res[i, gi] += m; place[i] += m
                    continue
                m = n * REP[g] * (1 - PHI) * lh[t, i]; res[i, gi] += m; place[i] += m
                sh = W[i, :N].copy()
                if i == SR:
                    me = n * REP[g] * PHI * sh[SR] * (0.7 * lw[t, SR] + 0.3 * lh[t, SR])
                    res[i, gi] += me; place[SR] += me; sh[SR] = 0
                mw = n * REP[g] * PHI * sh * lw[t]
                res[i, gi] += mw.sum(); place += mw
                res[i, gi] += n * REP[g] * PHI * W[i, N] * lo[t]
    return res, place, grp, W


if __name__ == "__main__":
    res, place, grp, W = expected()
    import routes as R
    f05 = R.fractional(res, grp, W, 0.5); f10 = R.fractional(res, grp, W, 1.0)
    for i in range(N):
        if BARANGAYS[i][1] in ("dorm", "cbd", "estate_host", "loc1", "loc2") or res[i].sum() > 22:
            print("%-16s %-11s E res %5.1f emp %5.1f nonemp %5.1f place %6.1f f0.5 %5.1f f1.0 %5.1f" % (
                NAMES[i], BARANGAYS[i][1], res[i].sum(), res[i, 1], res[i].sum() - res[i, 1], place[i], f05[i], f10[i]))
