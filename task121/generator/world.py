"""The borough's schools and pupils: fourteen secondaries, sixty-two primaries placed on the map, each primary's
leavers choosing a secondary by distance, catchment, faith and how sought after it is, and every pupil of the
2022, 2023 and 2024 key stage 4 cohorts with their key stage 2 results, census record, year 11 attendance and
key stage 4 grades. Progress 8 is the Department's: Attainment 8 against the national estimate for the pupil's key
stage 2 prior attainment, divided by ten. Every draw comes from a stream keyed on what it describes."""
import hashlib
import numpy as np
import pandas as pd
import common as K


def rng_for(*key, seed=None):
    s = K.SEED if seed is None else seed
    h = hashlib.sha256(("|".join(str(k) for k in (s,) + key)).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


def national_estimate(ks2, year):
    """The Department's estimated Attainment 8 for a key stage 2 average scaled score (a smooth curve read at the
    prior attainment group's centre), by key stage 4 year: 2022 graded on the transition year's boundaries."""
    base = 9.5 + 73.0 / (1.0 + np.exp(-(np.asarray(ks2, float) - 101.0) / 5.3))
    return base + {2022: 2.6, 2023: -0.5, 2024: 0.0}[year]


PAG_EDGES = np.array([80.0, 82.0, 84.0, 86.0, 88.0, 90.0, 91.5, 93.0, 94.0, 95.0, 96.0, 97.0, 98.0, 99.0, 100.0,
                      101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 108.0, 109.0, 110.0, 111.0, 112.0, 113.5,
                      115.0, 116.5, 118.0, 120.01])


def pag(ks2):
    """Prior attainment group (1 to 31) of a key stage 2 average scaled score, and the group's centre."""
    k = np.clip(np.asarray(ks2, float), 80.0, 120.0)
    g = np.searchsorted(PAG_EDGES, k, side="right")
    g = np.clip(g, 1, len(PAG_EDGES) - 1)
    centre = (PAG_EDGES[g - 1] + np.minimum(PAG_EDGES[g], 120.0)) / 2.0
    return g, centre


def pag_table(year):
    """The national estimates by prior attainment group: overall and per element (English and maths double-weighted,
    the EBacc and open elements three slots each), to two decimals."""
    rows = []
    for g in range(1, len(PAG_EDGES)):
        lo, hi = PAG_EDGES[g - 1], min(PAG_EDGES[g], 120.0)
        c = (lo + hi) / 2.0
        a8 = float(national_estimate(c, year))
        m = a8 / 10.0
        eng, mat = 2 * min(9, m * 1.04), 2 * min(9, m * 1.01)
        ebac = 3 * min(9, m * 0.97)
        opn = a8 - eng - mat - ebac
        rows.append(dict(pag=g, low=lo, high=hi if g < len(PAG_EDGES) - 1 else 120.0, a8=round(a8, 2),
                         eng=round(eng, 2), mat=round(mat, 2), ebac=round(ebac, 2), open=round(opn, 2)))
    return rows


class World:
    def __init__(self, seed=None):
        self.seed = K.SEED if seed is None else seed
        self.schools()
        self.primaries()
        self.feeding()
        self.pupils()

    def r(self, *key):
        return rng_for(*key, seed=self.seed)

    def schools(self):
        rg = self.r("own effects")
        S = K.SECONDARIES
        self.sec = [s[0] for s in S]
        self.sec_name = {s[0]: s[1] for s in S}
        self.sec_xy = {s[0]: np.array(s[4]) for s in S}
        self.attract = {s[0]: s[5] for s in S}
        u = {s[0]: 0.12 * s[5] + rg.normal(0, 0.11) for s in S}
        others = [k for k in K.TRUST_KEYS if k != K.FOCAL]
        m = np.mean([u[k] for k in others])
        for k in others:
            u[k] -= m
        u[K.FOCAL] = K.HALWICK_OWN
        self.u = u

    def primaries(self):
        rg = self.r("primaries")
        n = len(K.PRIMARY_NAMES)
        hosts = [k for k in self.sec if k not in ("HAL", "SWF", "OKV")]
        xy, dep, eal, mu, size = [], [], [], [], []
        j = 0
        for p in range(n):
            if p in K.FEEDERS:
                ang = 2 * np.pi * p / 7 + rg.normal(0, 0.25)
                c = self.sec_xy["HAL"] + rg.uniform(0.5, 1.6) * np.array([np.cos(ang), np.sin(ang)])
                d = rg.uniform(0.40, 0.56)
            elif p in K.CATHOLIC or p in K.CHURCH:
                c = np.array([rg.uniform(0.8, 12.6), rg.uniform(0.8, 9.2)])
                d = float(np.clip(rg.normal(0.24, 0.07), 0.08, 0.45))
            else:
                h = hosts[j % len(hosts)]
                j += 1
                c = self.sec_xy[h] + rg.normal(0, 0.9, 2)
                d = float(np.clip(rg.normal(0.26 + 0.06 * (self.attract[h] < 0), 0.09), 0.06, 0.55))
            xy.append(c)
            dep.append(d)
            eal.append(float(np.clip(rg.normal(0.12, 0.07), 0.01, 0.38)))
            mu.append(float(-1.1 * (d - 0.27) + rg.normal(0, 0.12)))
            size.append(int(rg.choice([30, 45, 60, 60, 60, 90]) * rg.uniform(0.88, 1.0)))
        self.p_xy, self.dep, self.eal, self.mu, self.size = np.array(xy), np.array(dep), np.array(eal), np.array(mu), size
        rv = self.r("primary effects")
        v = rv.normal(0, K.SD_PRIMARY, n)
        rest = [p for p in range(n) if p not in K.FEEDERS and p not in K.OTHER_WEAK]
        v[rest] -= v[rest].mean()
        for p in K.FEEDERS:
            v[p] = K.FEEDER_SHORTFALL + rv.normal(0, 0.06)
        for p in K.OTHER_WEAK:
            v[p] = K.OTHER_WEAK_SHORTFALL + rv.normal(0, 0.05)
        self.v = v

    def catchment(self, p):
        if p in K.FEEDERS:
            return "HAL"
        ds = {k: np.linalg.norm(self.p_xy[p] - self.sec_xy[k]) for k in self.sec if k not in ("SWF", "OKV")}
        return min(ds, key=ds.get)

    def feeding(self):
        """Each primary's leavers spread over the secondaries by distance, catchment, faith and how sought after
        each school is; each secondary's admission number then holds its intake near its planned size (a school
        constant fitted to the expected flows)."""
        n = len(K.PRIMARY_NAMES)
        base = np.zeros((n, len(self.sec)))
        for p in range(n):
            c = self.catchment(p)
            for j, k in enumerate(self.sec):
                d = np.linalg.norm(self.p_xy[p] - self.sec_xy[k])
                x = -d / 1.25 + 0.9 * self.attract[k] + (1.7 if k == c else 0.0)
                if k == "SWF":
                    x += 3.2 if p in K.CATHOLIC else -1.4
                if k == "OKV":
                    x += 1.6 if p in K.CHURCH else -0.6
                base[p, j] = x
        size = np.array(self.size, float) * 0.93
        tgt = np.array([K.PLANNED[k] for k in self.sec], float)
        tgt = tgt / tgt.sum() * size.sum()
        cst = np.zeros(len(self.sec))
        for _ in range(200):
            lg = base + cst
            e = np.exp(lg - lg.max(axis=1, keepdims=True))
            pr = e / e.sum(axis=1, keepdims=True)
            got = (pr * size[:, None]).sum(axis=0)
            cst += 0.8 * np.log(tgt / got)
        self.prob = {p: pr[p] for p in range(n)}

    def pupils(self):
        rows = []
        for year in K.COHORTS:
            for p in range(len(K.PRIMARY_NAMES)):
                rg = self.r("cohort", year, p)
                n = int(round(self.size[p] * rg.uniform(0.86, 1.0)))
                ss = rg.choice(len(self.sec), n, p=self.prob[p])
                for i in range(n):
                    rows.append(self.pupil(rg, year, p, self.sec[ss[i]], self.v[p], self.dep[p], self.eal[p], self.mu[p]))
            for k in self.sec:          # pupils who sat key stage 2 outside the borough
                rg = self.r("incomers", year, k)
                for i in range(int(rg.integers(5, 12))):
                    rows.append(self.pupil(rg, year, -1, k, rg.normal(0, K.SD_PRIMARY), float(rg.uniform(0.15, 0.4)),
                                           0.18, float(rg.normal(-0.1, 0.2))))
        self.D = pd.DataFrame(rows)

    def pupil(self, rg, year, p, s, v, dep, eal, mu):
        girl = rg.random() < 0.49
        dis = rg.random() < dep
        sen = "E" if rg.random() < 0.025 else ("K" if rg.random() < 0.12 else "N")
        e = rg.random() < 0.12
        ab = rg.normal(mu - 0.30 * dis - 0.55 * (sen == "K") - 1.3 * (sen == "E"), 0.95)
        rd = float(np.clip(np.round(104 + 6.6 * ab + rg.normal(0, 3.4)), 80, 120))
        ma = float(np.clip(np.round(104 + 6.6 * ab + rg.normal(0, 3.4)), 80, 120))
        no_ks2 = rg.random() < (0.02 if p >= 0 else 0.22)
        possible = int(rg.integers(250, 266))
        rate = float(np.clip(rg.gamma(2.0, 2.9) + 3.2 * dis + 6.5 * (dep - 0.27)
                             + rg.normal(0, 1.0), 0.0, 75.0))
        missed = int(round(rate * possible / 100.0))
        unauth = int(round(missed * float(np.clip(rg.beta(2, 5) + 0.15 * dis, 0, 1))))
        absr = 100.0 * missed / possible
        ks2 = (rd + ma) / 2.0
        g, centre = pag(ks2)
        est = float(national_estimate(centre, year))
        p8t = (K.BOROUGH_LEVEL + self.u[s] + v + K.B_ABSENCE * (absr - 8.5) + K.B_DISADV * dis
               + K.B_GIRL * (girl - 0.49) + (K.B_SEN_K if sen == "K" else K.B_SEN_E if sen == "E" else 0.0)
               + K.B_EAL * e + rg.normal(0, K.SD_PUPIL))
        a8t = est + 10.0 * p8t
        m = float(np.clip(a8t / 10.0, 0.0, 9.0))
        gr = np.clip(np.round(m + rg.normal(0, 0.55, 8)), 0, 9)
        if m < 1.2:
            gr[rg.random(8) < 0.35] = 0
        a8 = float(2 * gr[0] + 2 * gr[1] + gr[2:5].sum() + gr[5:8].sum())
        p8 = round((a8 - est) / 10.0, 2)
        return dict(year=year, p=p, s=s, girl=float(girl), dis=float(dis), sen=sen, eal=float(e), ks2_read=rd,
                    ks2_mat=ma, ks2=ks2, no_ks2=no_ks2, pag=int(g), est=round(est, 2), possible=possible,
                    missed=missed, unauth=unauth, absr=absr, eng=int(gr[0]), mat=int(gr[1]),
                    ebac=float(gr[2:5].sum()), opn=float(gr[5:8].sum()), a8=a8,
                    p8=(np.nan if no_ks2 else p8), v=v)
