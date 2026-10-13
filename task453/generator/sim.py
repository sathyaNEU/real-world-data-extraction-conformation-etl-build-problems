"""The simulation behind task453. Every region's monthly payroll jobs come first, as the Agency would have counted
them at the workplace (own jobs) plus the jobs at its workplaces of employers whose account address is in the Capital
or Saltmere Coast (branch jobs); before January 2026 the Agency's statistics placed the branch jobs at the account
address. Then the municipality by sector cells of every month, the two March workplace returns that add up to those
cells, the preliminary months and their revisions, and the two background series (the labour force survey and the
population estimates)."""
import collections
import datetime as dt

import numpy as np

import world as W

MONTHS = []
y, m = W.FIRST
while (y, m) <= W.LAST:
    MONTHS.append((y, m))
    y, m = (y + 1, 1) if m == 12 else (y, m + 1)
N = len(MONTHS)
T = np.arange(N)
MO = np.array([m for _, m in MONTHS])
YR = np.array([y for y, _ in MONTHS])
BRK = MONTHS.index(W.BREAK)
JUL25 = MONTHS.index((2025, 7))
AUG26 = MONTHS.index((2026, 8))
Q1_27 = YR == 2027
Y26 = YR == 2026
RAMP = np.clip((T - (BRK + 5)) / 7.0, 0, 1)        # 0 to June 2026, 1 from January 2027
MAR26 = MONTHS.index((2026, 3))
MAR27 = MONTHS.index((2027, 3))


def rng(*keys):
    h = 0
    for k in keys:
        for ch in str(k):
            h = (h * 131 + ord(ch)) % (2 ** 61 - 1)
    return np.random.default_rng([W.SEED, h])


def month_label(i):
    y, m = MONTHS[i]
    return "%04d-%02d" % (y, m)


# ------------------------------------------------------------------------------------------- regional series
def regional():
    """own and branch jobs (floats) and the seasonal pattern of each region; before January 2026 each region's branch
    jobs sit in the regions of their employers' account addresses"""
    R = {}
    for code, name, cds, size, hq, share, amp, noise, target, slope, turn in W.REGIONS:
        g = rng("region", code)
        ph = g.uniform(-0.4, 0.4)
        s = amp * np.cos(2 * np.pi * (MO - 7.2 + ph) / 12) + 0.25 * amp * np.cos(4 * np.pi * (MO - 7 + g.uniform(0, 6)) / 12)
        s = s - s[:12].mean()
        gr = np.where(YR <= 2022, g.uniform(0.02, 0.04), g.uniform(0.004, 0.012)) / 12
        base = np.cumsum(gr) + np.cumsum(g.normal(0, 0.0006, N))
        base = base - base[JUL25]
        base = np.where(T >= JUL25, 0.0, base)
        path = np.where(T >= JUL25, slope / 100.0 * (T - JUL25) / 12.0, 0.0) + \
            np.where(T >= AUG26, turn / 100.0 * (T - AUG26) / 7.0, 0.0)
        eps = g.normal(0, noise, N)
        R[code] = dict(name=name, size=size * 1000.0, hq=hq or {}, share=share, seas=s, base=base + path, eps=eps,
                       off=0.0, target=target, amp=amp, noise=noise)
    for _ in range(8):
        rep = reported(R)
        for code, d in R.items():
            d["off"] += np.log1p((d["target"] - truth(R, rep, code)) / 100.0)
    return R


def own_branch(R):
    own, br = {}, {}
    for code, d in R.items():
        lv = np.log(d["size"] * (1 - d["share"])) + d["base"] + d["off"] * RAMP + d["seas"] + d["eps"]
        own[code] = np.exp(lv)
        br[code] = own[code] * d["share"] / (1 - d["share"])
    return own, br


def reported(R):
    """each region's payroll jobs as the Agency's statistics place them"""
    own, br = own_branch(R)
    rep = {c: own[c] + np.where(T >= BRK, br[c], 0.0) for c in R}
    for c, d in R.items():
        for h, f in d["hq"].items():
            rep[h] = rep[h] + np.where(T < BRK, f * br[c], 0.0)
    return rep


def truth(R, rep, code):
    """the region's Q1 2027 payroll jobs over its own seasonal factors, against its 2026 average"""
    y = rep[code]
    return 100 * ((y / np.exp(R[code]["seas"]))[Q1_27].mean() / y[Y26].mean() - 1)


# ------------------------------------------------------------------------------------------- cells
def _largest_remainder(values, total):
    v = np.maximum(np.asarray(values, dtype=float), 0)
    if v.sum() <= 0:
        out = np.zeros(len(v), dtype=int)
        out[0] = total
        return out
    x = v / v.sum() * total
    f = np.floor(x).astype(int)
    short = int(total - f.sum())
    order = np.argsort(-(x - f), kind="stable")
    f[order[:short]] += 1
    return f


def munis_at(code, i):
    """the region's municipalities in force in month i with their weights"""
    y = MONTHS[i][0]
    out = []
    for mc, nm, cd, w, vf, vt in W.MUNIS:
        if W.MUNI_REGION[mc] != code:
            continue
        if vf and y < int(vf[:4]):
            continue
        if vt and y > int(vt[:4]):
            continue
        out.append((mc, w))
    return out


SEASONAL_SECTORS = {"11": 2.4, "23": 1.6, "71": 2.2, "72": 1.8, "31-33": 0.6, "48-49": 0.5}


def branch_mix(hq):
    w = collections.OrderedDict()
    for h, s, *_rest in W.BRANCH_EMPLOYERS:
        if h == hq:
            w[s] = w.get(s, 0.0) + _rest[-1]
    tot = sum(w.values())
    return collections.OrderedDict((s, v / tot) for s, v in w.items())


class Shares:
    """the sector and municipality shares each region's jobs are spread over, month by month"""

    def __init__(self, R):
        self.mix, self.drift, self.mdrift, self.bmix = {}, {}, {}, {}
        for code in R:
            g = rng("mix", code, "own")
            base = np.array([W.MIX[W.KIND[code]][s] for s in W.SECTOR_CODES], dtype=float)
            self.mix[code] = base * np.exp(g.normal(0, 0.18, len(base)))
            self.drift[code] = rng("drift", code).normal(0, 0.002, (N, len(W.SECTOR_CODES))).cumsum(axis=0)
            for h in R[code]["hq"]:
                bm = branch_mix(h)
                noise = np.exp(rng("bmix", code, h).normal(0, 0.25, len(bm)))
                v = np.array(list(bm.values())) * noise
                self.bmix[(code, h)] = collections.OrderedDict(zip(bm.keys(), v / v.sum()))
        for mc, *_ in W.MUNIS:
            self.mdrift[mc] = rng("mdrift", mc).normal(0, 0.0015, N).cumsum()
        # sectors with no own employment in a small municipality (a mine, a head office or a broadcaster is not in
        # every town); Wexleigh-Dorran keeps every sector either predecessor had
        self.present = {}
        for mc, nm, cd, w, vf, vt in W.MUNIS:
            code = W.MUNI_REGION[mc]
            base = self.mix[code] / self.mix[code].sum()
            g = rng("present", mc)
            keep = np.ones(len(W.SECTOR_CODES))
            if mc not in W.HEAD_OFFICE_MUNI.values() and w < 0.25:
                for k, s in enumerate(W.SECTOR_CODES):
                    if s in ("11", "23", "44-45", "61", "62", "72", "81", "91"):
                        continue
                    p = 0.6 if base[k] < 0.015 else (0.3 if base[k] < 0.04 else 0.0)
                    if g.random() < p:
                        keep[k] = 0.0
            self.present[mc] = keep
        self.present["0814"] = np.maximum(self.present["0803"], self.present["0806"])

    def sectors(self, code, i):
        m = MONTHS[i][1]
        seas = np.array([SEASONAL_SECTORS.get(s, 0.0) * 0.02 * np.cos(2 * np.pi * (m - 7) / 12) for s in W.SECTOR_CODES])
        v = self.mix[code] * np.exp(self.drift[code][i] + seas)
        return v / v.sum()

    def munis(self, code, i):
        ms = munis_at(code, i)
        w = np.array([wt * np.exp(self.mdrift[mc][i]) for mc, wt in ms])
        return [mc for mc, _ in ms], w / w.sum()


def parts(R, S, own, br, i):
    """the month's float jobs: {(region of the cell, muni, sector, kind): jobs}, kind 'own' or ('branch', origin, hq)"""
    out = collections.OrderedDict()
    for code, d in R.items():
        ms, mw = S.munis(code, i)
        sm = S.sectors(code, i)
        for mc, wv in zip(ms, mw):
            sk = sm * S.present[mc]
            sk = sk / sk.sum()
            for k, s in enumerate(W.SECTOR_CODES):
                if sk[k] > 0:
                    out[(code, mc, s, "own")] = own[code][i] * wv * sk[k]
        for h, f in d["hq"].items():
            tot = br[code][i] * f
            for s, bv in S.bmix[(code, h)].items():
                if i >= BRK:
                    for mc, wv in zip(ms, mw):
                        out[(code, mc, s, ("branch", code, h))] = tot * bv * wv
                else:
                    hm = W.HEAD_OFFICE_MUNI[h]
                    out[(h, hm, s, ("branch", code, h))] = tot * bv
    return out


def cells(R, S=None):
    """{month index: {(muni, sector): jobs}}, integers; each region's month total is its rounded reported jobs"""
    S = S or Shares(R)
    rep = reported(R)
    own, br = own_branch(R)
    out = {}
    for i in range(N):
        p = parts(R, S, own, br, i)
        cell = {}
        for reg in R:
            keys = collections.OrderedDict()
            for (r, mc, s, kind), v in p.items():
                if r == reg:
                    keys[(mc, s)] = keys.get((mc, s), 0.0) + v
            ks = list(keys)
            ints = _largest_remainder([keys[k] for k in ks], int(round(rep[reg][i])))
            for k, v in zip(ks, ints):
                cell[k] = int(v)
        out[i] = cell
    return out


# ------------------------------------------------------------------------------------------- releases
PRELIM = {(2027, 1): 0.0002, (2027, 2): 0.0006, (2027, 3): 0.0021}


def preliminary(cells_rev):
    """the 23 April extract's January to March 2027 cells: the revised cells less the returns that arrived after it"""
    out = {}
    for ym, frac in PRELIM.items():
        i = MONTHS.index(ym)
        g = rng("late", ym)
        cur = {}
        for k in sorted(cells_rev[i]):
            v = cells_rev[i][k]
            late = min(v, int(g.poisson(v * frac * float(g.gamma(3.0, 1 / 3.0))))) if v > 0 else 0
            cur[k] = v - late
        out[i] = cur
    return out


def lfs(R):
    """the labour force survey's three-month moving averages by economic region, January 2025 to March 2027:
    residents employed (thousands), the unemployment rate and the participation rate"""
    own, br = own_branch(R)
    rows = []
    for code in R:
        g = rng("lfs", code)
        jobs = own[code] + br[code]                     # where the region's residents work, near enough
        emp = jobs * float(g.uniform(1.08, 1.16)) * np.exp(g.normal(0, 0.035 if code != "E01" else 0.015, N))
        ur = float(g.uniform(5.0, 9.5)) + 1.8 * np.cos(2 * np.pi * (MO - 2) / 12) * (0.6 if code == "E01" else 1.0) + g.normal(0, 0.7, N)
        pr = float(g.uniform(58.0, 66.0)) + g.normal(0, 0.9, N)
        e3 = np.convolve(emp, np.ones(3) / 3, mode="full")[:N]
        u3 = np.convolve(ur, np.ones(3) / 3, mode="full")[:N]
        p3 = np.convolve(pr, np.ones(3) / 3, mode="full")[:N]
        for i in range(N):
            if MONTHS[i] < (2025, 1):
                continue
            rows.append((month_label(i), code, W.RNAME[code], round(e3[i] / 1000.0, 1), round(u3[i], 1), round(p3[i], 1)))
    return rows


def population(R):
    """municipal population on 1 July 2024, 2025 and 2026, total and aged 15 to 64"""
    own, br = own_branch(R)
    rows = []
    for mc, nm, cd, w, vf, vt in W.MUNIS:
        code = W.MUNI_REGION[mc]
        g = rng("pop", mc)
        base = (own[code][MONTHS.index((2025, 7))] + br[code][MONTHS.index((2025, 7))]) * w * float(g.uniform(1.85, 2.35))
        gr = float(g.uniform(-0.006, 0.014))
        for year in (2024, 2025, 2026):
            if vt and year > int(vt[:4]):
                continue
            if vf and year < int(vf[:4]):
                continue
            p = base * (1 + gr) ** (year - 2025)
            if mc == "0814" and year >= 2025:
                p = p
            share = float(g.uniform(0.60, 0.66))
            rows.append((mc, nm, year, int(round(p)), int(round(p * share))))
    return rows
