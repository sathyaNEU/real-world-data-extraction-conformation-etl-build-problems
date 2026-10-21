"""The clean world for task179: a Tamberlow virus disease outbreak in Dunmarrow Province (Republic of Orvanthe, a
fictional setting), day 0 = Monday 25 May 2026.
Everything the pack ships is derived from the objects built here; nothing is reverse-engineered to a figure."""
import datetime as dt
import numpy as np
from core import L, dgamma_pmf

DAY0 = dt.date(2026, 5, 25)
COMPLETE_LAST = 139      # Sunday 11 October 2026: onsets complete to here (notification within seven days)
EXTRACT_DAY = 146        # Sunday 18 October 2026, 23:59
BASE_FIRST = 98         # Monday 31 August 2026 (epi week 36)
CUT_FROM = 161           # Monday 2 November 2026
WIN_FIRST, WIN_LAST = 189, 216   # Monday 30 November to Sunday 27 December 2026 (epi weeks 49 to 52)
CUT = 0.50
SI_MEAN, SI_SD = 13.0, 7.6
R_EARLY, R_LATE, R_SWITCH = 1.85, 1.67, 49   # transmission eased slightly once the outbreak was declared (13 July)
K_DISP = 0.40
P_LINKED = 0.75
SEED = 36

ZONES = ["Tamberlow", "Quillmarsh", "Threlmarren", "Wendlecombe", "Brindlecourt", "Kettlebank North", "Kettlebank South"]
# move matrix: where a case's infectee lives, by the source's district (rows), roughly by road and river distance
MOVE = np.array([
    [0.80, 0.08, 0.02, 0.01, 0.03, 0.03, 0.03],
    [0.10, 0.80, 0.02, 0.01, 0.02, 0.03, 0.02],
    [0.02, 0.02, 0.82, 0.04, 0.03, 0.04, 0.03],
    [0.01, 0.01, 0.06, 0.84, 0.02, 0.03, 0.03],
    [0.02, 0.01, 0.02, 0.01, 0.78, 0.08, 0.08],
    [0.02, 0.01, 0.02, 0.01, 0.06, 0.78, 0.10],
    [0.02, 0.01, 0.02, 0.01, 0.06, 0.10, 0.78],
])


def date_of(day):
    return DAY0 + dt.timedelta(days=int(day))


def simulate(seed=SEED, until=EXTRACT_DAY + 10):
    rng = np.random.default_rng(seed)
    w = dgamma_pmf(SI_MEAN, SI_SD)
    lags_all = np.arange(1, L + 1)
    onset = [int(d) for d in rng.integers(0, 6, 3)]
    src = [-1, -1, -1]
    zone = [0, 0, 0]
    i = 0
    while i < len(onset):
        t = onset[i]
        R = R_EARLY if t < R_SWITCH else R_LATE
        n = rng.negative_binomial(K_DISP, K_DISP / (K_DISP + R))
        if n:
            for lag in rng.choice(lags_all, size=n, p=w):
                if t + lag <= until:
                    onset.append(int(t + lag))
                    src.append(i)
                    zone.append(int(rng.choice(7, p=MOVE[zone[i]])))
        i += 1
    order = np.argsort(np.array(onset), kind="stable")
    inv = np.empty_like(order)
    inv[order] = np.arange(len(order))
    onset = np.array(onset)[order]
    src = np.array([inv[s] if s >= 0 else -1 for s in np.array(src)[order]])
    zone = np.array(zone)[order]
    return {"onset": onset, "src": src, "zone": zone, "w": w}


if __name__ == "__main__":
    for s in range(1, 40):
        o = simulate(s)
        n = (o["onset"] <= COMPLETE_LAST).sum()
        print(s, n, np.bincount(o["onset"][o["onset"] <= COMPLETE_LAST] // 7)[-6:])
