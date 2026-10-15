"""Small per-group nudges to the net worth factors (hundredths of a per cent) so every graded survey figure sits at
least $150 from a thousand-dollar rounding edge. Medians and replicate medians scale exactly with a group's factor
(its medians are positive), so the search rescales one computed set of estimates."""
import itertools
import numpy as np
import common as K
import est as E
import world as W

d = W.core()
w = np.round(d["w"] * K.POPULATION_HOUSEHOLDS / d["w"].sum(), 4)
R = np.round(d["mult"] * w[None, :], 4)
band = K.band_of(np.minimum(d["older"], 85))
nw, _ = W.wealth(d)
sv = E.Survey(nw, w, R)
EST, REP = [], []
for g in range(6):
    e, r = sv.median(band == g)
    assert (e > 0).all()
    EST.append(e)
    REP.append(r)


def margins(f):
    m = []
    for g in range(6):
        th, u, b, t, se = E.Survey.combine(EST[g] * f[g], REP[g] * f[g])
        m += [abs(th % 1000 - 500), abs(se % 1000 - 500)]
    for g in range(5):
        th, u, b, t, se = E.Survey.combine(EST[g + 1] * f[g + 1] - EST[g] * f[g], REP[g + 1] * f[g + 1] - REP[g] * f[g])
        m += [abs(abs(th) % 1000 - 500), abs(se % 1000 - 500), abs(abs(th / se) * 10 % 1 - 0.5) * 1000]
    return min(m)


grid = np.arange(-12, 13) * 0.0001
best = (margins([1] * 6), [1] * 6)
r = np.random.default_rng(1)
for _ in range(60000):
    f = 1 + r.choice(grid, 6)
    sc = margins(f)
    if sc > best[0]:
        best = (sc, list(f))
        if sc >= 160:
            break
print("margin %.1f" % best[0], "factors", [round(K.TUNE[g] * best[1][g], 6) for g in range(6)])
