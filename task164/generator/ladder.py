"""The ladder on the clean truth: every estimator in the golden family, every rung and every cheap route, with each
one's district counts and allocation. Used at design time and asserted in checks.py (R3a, R3b, LADDER, FAMILY)."""
from __future__ import annotations

import numpy as np
import pandas as pd

import common as K
import forward as FW
import world as W

REC = pd.Timestamp(K.RECORD_DATE)


def behaviour_demand(rate_class, seed=9, n=300000):
    """Average 4 to 9 pm charging demand per vehicle (kVA) over every summer day, and at the busiest quarter hour,
    from the behaviour model the load research sample is drawn from."""
    r = np.random.default_rng(seed)
    bev = r.random(n) < .8
    P = np.where(bev, r.choice([1.4, 7.2, 9.6, 11.5], p=[.15, .6, .15, .1], size=n), r.choice([1.4, 3.3], p=[.3, .7], size=n))
    q = np.where(bev, .5, .8)
    em = np.where(bev, 10, 6)
    pa = K.BEH[rate_class][0] + (1 - K.BEH[rate_class][0]) * K.SLIP[rate_class]
    ch = (r.random(n) < q) & (r.random(n) < pa)
    off = r.random(n) < (2 / 7)
    st = np.where(off, r.normal(15.8, 2.4, n), r.normal(17.6, 1.0, n))
    en = st + np.clip(r.gamma(4, em / 4), 1, 45) / P
    ov = np.clip(np.minimum(en[:, None], K.QSTART + .25) - np.maximum(st[:, None], K.QSTART), 0, .25) / .25
    kw = ov * P[:, None] * ch[:, None]
    return kw.mean() / K.PF, kw.mean(axis=0).max() / K.PF, P.mean() / K.PF


class Ladder:
    def __init__(self, T):
        self.T = T
        tx = T.tx
        self.thr = K.THRESH * tx["kva"].values
        self.k0, self.e0 = tx["k2026"].values, tx["e2026"].values
        self.k1, self.e1 = T.k1, T.e1
        self.p26 = tx["pk2026"].values
        self.sg = tx["sg"].values
        self.district = tx["district"].values
        # the changes since each transformer's 2026 peak, by kind
        v = T.veh
        pkd = dict(zip(tx["ti"], W.peak_date(tx, 2026)))
        v = v.assign(pk=v["ti"].map(pkd))
        alive_rec = v["dep"].isna() | (v["dep"] > REC)
        at_pk = (v["reg"] <= v["pk"]) & (v["dep"].isna() | (v["dep"] > v["pk"]))
        new = (v["reg"] > v["pk"]) & (v["reg"] <= REC) & alive_rec
        gone = at_pk & ~alive_rec
        self.rate_rec = np.array([W.rate_on(T.pr_base, T.sw, p, REC) for p in v["pi"]])
        self.rate_pk = np.array([W.rate_on(T.pr_base, T.sw, p, d) for p, d in zip(v["pi"], v["pk"])])
        ev_rec = self.rate_rec == K.RATE_EV
        ev_pk = self.rate_pk == K.RATE_EV
        idx = pd.Index(tx["ti"])

        def per_tx(mask):
            return pd.Series(1, index=v.index[mask]).groupby(v["ti"][mask]).sum().reindex(idx).fillna(0).astype(int).values
        self.newT, self.newE = per_tx(new & ~ev_rec), per_tx(new & ev_rec)
        self.goneT, self.goneE = per_tx(gone & ~ev_pk), per_tx(gone & ev_pk)
        self.switched = per_tx(at_pk & alive_rec & ~ev_pk & ev_rec)
        self.newT_oct = per_tx(new & ~ev_rec & (v["reg"] >= pd.Timestamp("2026-10-01")))
        self.newE_oct = per_tx(new & ev_rec & (v["reg"] >= pd.Timestamp("2026-10-01")))
        self.aT, self.bT, self.Pm = behaviour_demand("TOU")
        self.aE, self.bE, _ = behaviour_demand("EV")

    def counts(self, f):
        at = np.asarray(f) > self.thr
        return pd.Series(at).groupby(self.district).sum().reindex(K.NAMES).astype(int)

    def family_forecast(self, tab):
        return np.array([FW.forecast(tab, s, a, b, c, d, p) for s, a, b, c, d, p in
                         zip(self.sg, self.k0, self.e0, self.k1, self.e1, self.p26)])

    def constant(self, t, e, new_only=False, with_gone=True, with_switch=True):
        if new_only:
            return self.p26 + self.newT * t + self.newE * e
        d = self.newT * t + self.newE * e
        if with_gone:
            d = d - self.goneT * t - self.goneE * e
        if with_switch:
            d = d - self.switched * (t - e)
        return self.p26 + d

    def rungs(self, fam):
        g = fam[FW.GOLD]
        P = self.T.P
        pooled_any = float(P[((P.dk + P.de) == 1) & (P.dk >= 0) & (P.de >= 0)]["adj"].mean())
        mT1 = g["tou"][("M", 1)]
        R = {}
        R["H the 2026 recorded peak alone"] = self.p26
        R["R0 average 4-9 pm demand per vehicle, by rate, every change"] = self.constant(self.aT, self.aE)
        R["R0a average demand per vehicle, new vehicles only"] = self.constant(self.aT, self.aE, new_only=True)
        R["R0b busiest quarter-hour demand per vehicle, by rate"] = self.constant(self.bT, self.bE)
        R["R1 charger rating, every new vehicle"] = self.p26 + (self.newT + self.newE) * self.Pm
        R["R1b charger rating on the default rate, nil on the EV rate"] = self.constant(self.Pm, 0.0)
        R["R2 one recorded-peak increment pooled across rates"] = self.constant(pooled_any, pooled_any)
        R["R2b default-rate increment, EV rate nil"] = self.constant(mT1, 0.0)
        tabs = {k: v for k, v in fam.items()}
        gnew = np.array([FW.F(g, s, a + nt, b + ne) - FW.F(g, s, a, b) for s, a, b, nt, ne in
                         zip(self.sg, self.k0, self.e0, self.newT, self.newE)])
        R["R3 recorded-peak increments, new vehicles only"] = self.p26 + gnew
        k_ns = self.k1 + self.switched
        e_ns = self.e1 - self.switched
        R["R4 recorded-peak increments, the rate moves ignored"] = np.array(
            [FW.forecast(g, s, a, b, c, d, p) for s, a, b, c, d, p in zip(self.sg, self.k0, self.e0, k_ns, e_ns, self.p26)])
        k_ng = self.k1 + self.goneT
        e_ng = self.e1 + self.goneE
        R["R5 recorded-peak increments, departures ignored"] = np.array(
            [FW.forecast(g, s, a, b, c, d, p) for s, a, b, c, d, p in zip(self.sg, self.k0, self.e0, k_ng, e_ng, self.p26)])
        k_late = self.k1 - (self.newT - self.newT_oct)
        e_late = self.e1 - (self.newE - self.newE_oct)
        R["R6 recorded-peak increments, only vehicles registered from 1 October"] = np.array(
            [FW.forecast(g, s, a, b, c, d, p) for s, a, b, c, d, p in zip(self.sg, self.k0, self.e0, k_late, e_late, self.p26)])
        R["GOLD"] = self.family_forecast(g)
        return R

    def table(self, fam, extra=None):
        out = {}
        for name, f in self.rungs(fam).items():
            c = self.counts(f)
            a, q = FW.allocate(c)
            out[name] = (c, a, q)
        for name, tab in fam.items():
            c = self.counts(self.family_forecast(tab))
            a, q = FW.allocate(c)
            out["FAMILY " + name] = (c, a, q)
        return out


def show(T):
    L = Ladder(T)
    res = L.table(T.fam)
    ga = res["GOLD"][1]
    print("demand per vehicle: TOU average %.2f busiest %.2f, EV average %.3f busiest %.3f, rating %.2f kVA" % (
        L.aT, L.bT, L.aE, L.bE, L.Pm))
    g = T.fam[FW.GOLD]
    print("golden increments:", {k: round(v, 2) for k, v in g["tou"].items()}, "EV", round(g["ev"][0], 2))
    for name, tab in T.fam.items():
        print("   %-34s TOU S1 %.2f M1 %.2f L1 %.2f M2 %.2f EV %.2f/%.2f" % (
            name, tab["tou"][("S", 1)], tab["tou"][("M", 1)], tab["tou"][("L", 1)], tab["tou"][("M", 2)], tab["ev"][0], tab["ev"][1]))
    print("\n%-66s %5s %s" % ("construction", "N", " ".join("%8s" % n[:8] for n in K.NAMES)))
    for name, (c, a, q) in res.items():
        print("%-66s %5d %s off %2d |d| %2d FH %d" % (name[:66], c.sum(), " ".join("%3d/%3d " % (x, y) for x, y in zip(c, a)),
                                                      int((a != ga).sum()), int((a - ga).abs().sum()), a["Foothill"]))
    return L, res


if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    os.environ["T164_CACHE"] = "1"
    import truth
    T = truth.load()
    show(T)
