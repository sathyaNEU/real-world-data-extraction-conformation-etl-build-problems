"""task247 aiming, run by hand, never by make.py: each site's 2027 heat amplitude enters the sea, the near-real-time
analysis and the reprocessed record linearly (a clear day reads it, a filled day keeps it decaying), so every route's
season maximum is a function of one number per site; this finds the amplitude that puts the refilled maximum on its
target and prints every route there.

    python3 task247/generator/aim.py <sim_seed> [trough_share]
"""
import sys

import numpy as np

import estim as E
import params as P
import sim

# the refilled season maximum each site is aimed at (degree-weeks)
TARGET = [3.0, 5.0, 2.0, 6.0, 5.0,
          9.0, 11.0, 7.0, 10.0, 12.0,
          13.0, 10.0, 12.0, 9.0, 11.0, 6.0]
VARIANTS = ["temp", "pchip", "sbias", "hbias", "carry", "near", "first"]


class World:
    def __init__(self, seed):
        self.W = W = sim.make(seed, amp27=[0.0] * P.NSITE)
        D, clim = W["D"], W["clim"]
        self.cloud, self.obs, self.late = W["cloud"], W["observed"], W["late"]
        yr = np.array([d.year for d in D]); mon = np.array([d.month for d in D])
        y19 = yr == 2019
        self.mmm = np.round([max(clim[s, y19 & (mon == m)].mean() for m in range(1, 13)) for s in range(P.NSITE)], 2)
        self.season = np.array([P.SEASON[0] <= d <= P.SEASON[1] for d in D])
        self.mon_ = np.array([d.weekday() == 0 for d in D])       # the Tuesday bulletin reports Monday's analysis
        past = yr <= 2026
        obs, fil = self.obs, ~self.obs
        diff = W["final"] - W["rep"]
        self.b_all = diff[:, past].mean()
        self.b_obs = diff[:, past][obs[:, past]].mean()
        self.b_fill = diff[:, past][fil[:, past]].mean()
        self.b_site = [diff[s, past & obs[s]].mean() for s in range(P.NSITE)]
        heat = past & (mon >= 6) & (mon <= 10)
        self.b_heat = diff[:, heat][obs[:, heat]].mean()
        fa = (W["final"] - clim)[:, past][fil[:, past]]
        ra = (W["rep"] - clim)[:, past][fil[:, past]]
        self.k1, self.k0 = np.polyfit(fa, ra, 1)
        self.shape = W["shape27"]
        self.g = np.zeros((P.NSITE, len(D)))
        for s in range(P.NSITE):
            last = 0.0
            for t in range(len(D)):
                last = self.shape[s, t] if not self.cloud[s, t] else last * np.exp(-1 / P.TAU)
                self.g[s, t] = last
        self.gf = np.where(self.late, self.shape, self.g)

    def arrays(self, s, a):
        W = self.W
        return (W["final"][s] + a * self.gf[s], W["nrt"][s] + a * self.g[s], W["rep"][s] + a * self.shape[s],
                W["clim"][s])

    def gold(self, s, a):
        fin, _, _, clim = self.arrays(s, a)
        return E.season_max(E.refill(fin, self.obs[s], clim, self.b_obs), self.mmm[s], self.season)

    def routes(self, s, a):
        fin, first, rep, clim = self.arrays(s, a)
        m, se, ob = self.mmm[s], self.season, self.obs[s]
        fl = ~ob
        sm = lambda x: E.season_max(x, m, se)
        return dict(
            truth=sm(rep),
            decl=float(E.dhw(fin, m)[se & self.mon_].max()),
            pooled=sm(fin - self.b_all),
            flag=sm(fin - np.where(fl, self.b_fill, self.b_obs)),
            site=sm(fin - np.where(fl, self.b_fill, self.b_site[s])),
            regr=sm(np.where(fl, clim + self.k0 + self.k1 * (fin - clim), fin - self.b_obs)),
            nobias=sm(E.refill(fin, ob, clim, 0.0)),
            gold=sm(E.refill(fin, ob, clim, self.b_obs)),
            temp=sm(E.refill(fin, ob, clim, self.b_obs, "temperature")),
            pchip=sm(E.refill(fin, ob, clim, self.b_obs, "pchip")),
            sbias=sm(E.refill(fin, ob, clim, self.b_site[s])),
            hbias=sm(E.refill(fin, ob, clim, self.b_heat)),
            carry=sm(E.refill(fin, ob, clim, self.b_obs, "carry")),
            near=sm(E.refill(fin, ob, clim, self.b_obs, "nearest")),
            first=sm(E.refill(first, ~self.cloud[s], clim, self.b_obs)),
        )

    def aim(self, s, target):
        lo, hi = 0.5, 2.5
        for _ in range(36):
            mid = 0.5 * (lo + hi)
            if self.gold(s, mid) < target:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)


LV = lambda x: "AL2" if x >= 8 else ("AL1" if x >= 4 else "--")
RUNGS = ["truth", "decl", "pooled", "flag", "site", "regr", "nobias", "gold"]


def table(w, amps):
    R = [w.routes(s, amps[s]) for s in range(P.NSITE)]
    lists = {k: tuple(P.SITES[s][0] for s in range(P.NSITE) if R[s][k] >= 8) for k in RUNGS + VARIANTS}
    diffs = []
    for s, r in enumerate(R):
        g = round(r["gold"])
        for k in VARIANTS:
            if round(r[k]) != g or LV(r[k]) != LV(r["gold"]):
                diffs.append((P.SITES[s][0], k, r[k], r["gold"]))
    return R, lists, diffs


def show(w, amps):
    R, lists, diffs = table(w, amps)
    print("bias all %.3f obs %.3f fill %.3f heat %.3f  regression %.2f + %.2f x" %
          (w.b_all, w.b_obs, w.b_fill, w.b_heat, w.k0, w.k1))
    for s, r in enumerate(R):
        print("%s amp %.3f | " % (P.SITES[s][0], amps[s]) +
              " ".join("%s %5.2f %s" % (k, r[k], LV(r[k])) for k in RUNGS) + " | " +
              " ".join("%s %.2f" % (k, r[k]) for k in VARIANTS))
    for k in RUNGS + VARIANTS:
        print("  %-7s AL2 %2d: %s" % (k, len(lists[k]), " ".join(lists[k])))
    print("  variant figures off the golden:", diffs)


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    if len(sys.argv) > 2:
        sim.TROUGHS[0] = sim.TROUGHS[0][:3] + (float(sys.argv[2]),)
    w = World(seed)
    amps = [round(w.aim(s, TARGET[s]), 4) for s in range(P.NSITE)]
    print("seed", seed, "AMP27 =", amps)
    show(w, amps)
