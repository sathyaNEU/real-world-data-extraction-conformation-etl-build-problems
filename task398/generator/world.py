"""task398's world: Brennick (a fictional city in northeast Iowa), its supply reservoir Lake Merrin on the Tessel
River, five tributary sub-watersheds, and the 2026 season from 1 January to 31 October.

The clean truth is simulated here and nowhere else: each tributary's daily flow, water temperature and atrazine;
a horizontally mixed, vertically resolved reservoir held as a stack of water parcels (mass conserved by
construction), into which each inflow is inserted at the depth where the lake is as warm as the inflow; the city's
intake at its fixed elevation, the bottom outlet and the spillway withdrawing at their own elevations; and the
atrazine each source left in the water the intake drew, day by day."""
import datetime as dt
import math

import numpy as np

SEED = 39804
D0 = dt.date(2026, 1, 1)
D_END = dt.date(2026, 10, 31)
ND = (D_END - D0).days + 1
FT = 0.3048
CFS = 0.0283168466            # m3/s per cfs
MGD = 3785.411784 / 86400.0   # m3/s per MGD

CITY = "Brennick"
UTILITY = "Brennick Water"
DEPT = "City of Brennick Water Department"
LAKE = "Lake Merrin"
DAM = "Merrin Dam"
PLANT = "Merrin Water Treatment Plant"
COUNTY = "Haldane County"

FULL_POOL_FT = 863.0          # spillway crest, NGVD29
BOTTOM_FT = 801.0             # deepest point at the dam, NGVD29
INTAKE_FT = 829.0             # intake port centreline, NGVD29
NAVD_MINUS_NGVD_FT = 0.24     # NAVD88 = NGVD29 + 0.24 ft at the dam benchmark
AREA_FP_M2 = 8.70e6
P_HYPS = 2.2
SPILL_C, SPILL_L_FT = 3.32, 210.0       # ogee crest, Q = C L H^1.5 in cfs and ft

TRIGGER = 3.0                 # ug/L, the carbon-feed trigger
SUBS = ["TES", "FEN", "OXL", "DUN", "LAD"]
NAME = dict(TES="Tessel River", FEN="Fennick Creek", OXL="Oxley Creek", DUN="Dunmore Creek", LAD="Ladd Branch")
STATION = dict(TES="TR-01", FEN="FC-02", OXL="OC-03", DUN="DC-04", LAD="LB-05")
AREA_KM2 = dict(TES=822.4, FEN=117.6, OXL=231.3, DUN=149.8, LAD=34.9)
BASE = dict(TES=3.4, FEN=1.10, OXL=0.70, DUN=0.80, LAD=0.34)              # m3/s summer baseflow
RRATIO = dict(TES=0.24, FEN=0.20, OXL=0.30, DUN=0.24, LAD=0.14)            # storm runoff over rain
TAU = dict(TES=3.2, FEN=2.0, OXL=1.3, DUN=1.5, LAD=1.8)                    # recession, days
LAG = dict(TES=3, FEN=2, OXL=2, DUN=3, LAD=1)                              # days from the station to the dam
APPLIED = dict(TES=20400.0, FEN=3350.0, OXL=7100.0, DUN=2900.0, LAD=110.0) # kg a.i. applied in 2026
EXPORT = dict(TES=0.0145, FEN=0.0150, OXL=0.0270, DUN=0.0418, LAD=0.012)   # share of applied lost in runoff, Apr-Sep
GW = dict(TES=0.34, FEN=1.00, OXL=0.62, DUN=1.18, LAD=0.10)                # ug/L summer baseflow atrazine

KEYS = SUBS + ["OLD"]
NK = len(KEYS)


def di(m, d):
    return (dt.date(2026, m, d) - D0).days


def day(i):
    return D0 + dt.timedelta(days=i)


def smooth(x, pts):
    return float(np.interp(x, [p[0] for p in pts], [p[1] for p in pts]))


# ------------------------------------------------------------------ hypsography
def storage_ft(elev_ft):
    h = max(0.0, (elev_ft - BOTTOM_FT) / (FULL_POOL_FT - BOTTOM_FT))
    H = (FULL_POOL_FT - BOTTOM_FT) * FT
    return AREA_FP_M2 * H * h ** (P_HYPS + 1) / (P_HYPS + 1)


def area_ft(elev_ft):
    h = max(0.0, (elev_ft - BOTTOM_FT) / (FULL_POOL_FT - BOTTOM_FT))
    return AREA_FP_M2 * h ** P_HYPS


_E = np.linspace(BOTTOM_FT * FT, 870.0 * FT, 6001)
_S = np.array([storage_ft(e / FT) for e in _E])


def elev_of_storage(s):
    return float(np.interp(s, _S, _E))


def stor_of_elev(e_m):
    return float(np.interp(e_m, _E, _S))


# ------------------------------------------------------------------ the lake's temperature (the buoy's truth)
def profile_params(i):
    ts = smooth(i, [(0, 1.0), (di(3, 20), 2.5), (di(4, 10), 6.5), (di(4, 25), 9.8), (di(5, 20), 18.0),
                    (di(6, 10), 23.2), (di(7, 10), 26.6), (di(7, 28), 27.4), (di(8, 25), 25.4), (di(9, 15), 22.0),
                    (di(10, 1), 18.6), (di(10, 20), 15.0), (di(10, 31), 12.6)])
    tb = smooth(i, [(0, 3.6), (di(3, 20), 3.9), (di(4, 10), 6.2), (di(4, 25), 8.4), (di(5, 20), 9.6),
                    (di(6, 15), 10.6), (di(7, 15), 11.3), (di(8, 15), 11.8), (di(9, 10), 12.1), (di(9, 28), 12.6),
                    (di(10, 8), 15.6), (di(10, 20), 15.0), (di(10, 31), 12.6)])
    zt = smooth(i, [(0, 30.0), (di(4, 22), 30.0), (di(5, 1), 2.6), (di(5, 20), 3.4), (di(6, 1), 4.6),
                    (di(6, 20), 5.8), (di(7, 15), 6.8), (di(8, 15), 7.4), (di(9, 10), 8.8), (di(9, 28), 11.6),
                    (di(10, 7), 16.5), (di(10, 12), 30.0), (di(10, 31), 30.0)])
    w = smooth(i, [(0, 2.0), (di(5, 1), 1.4), (di(6, 15), 1.8), (di(8, 15), 2.1), (di(9, 28), 2.4),
                   (di(10, 31), 2.5)])
    return ts, tb, zt, w


def temp_at(i, z):
    """Lake temperature at depth z (m below the surface) on day i, C. Ice and the spring and autumn mixed
    periods are nearly isothermal; the summer lake is a smooth step from the surface to the hypolimnion."""
    ts, tb, zt, w = profile_params(i)
    if zt >= 29.0:
        if i < di(4, 1):
            return tb + (ts - tb) * math.exp(-z / 6.0)
        return (ts + tb) / 2.0
    return tb + (ts - tb) / (1.0 + math.exp((z - zt) / w))


# ------------------------------------------------------------------ weather, flow, temperature, atrazine
STORMS = [(di(2, 25), 15), (di(3, 18), 24), (di(4, 28), 31), (di(5, 13), 46), (di(5, 27), 38), (di(6, 7), 52),
          (di(6, 18), 41), (di(6, 27), 57), (di(7, 12), 34), (di(7, 24), 44), (di(8, 6), 29), (di(8, 19), 37),
          (di(9, 4), 26), (di(9, 23), 33), (di(10, 14), 22)]


def storms(rng):
    out = []
    for d, mm in STORMS:
        fac = {k: float(np.clip(rng.normal(1.0, 0.07), 0.82, 1.18)) for k in SUBS}
        out.append((d, mm, fac))
    return out


def rainfall(rng, ST):
    """Daily rain at the dam, mm: the storms plus ordinary showers."""
    r = np.zeros(ND)
    for d, mm, fac in ST:
        r[d] += mm * float(np.mean(list(fac.values())))
        if d + 1 < ND:
            r[d + 1] += mm * float(rng.uniform(0.05, 0.22))
    p_wet = np.array([smooth(i, [(0, 0.18), (di(4, 1), 0.30), (di(6, 15), 0.33), (di(8, 15), 0.26),
                                 (di(10, 31), 0.22)]) for i in range(ND)])
    wet = rng.random(ND) < p_wet
    r += wet * rng.gamma(0.7, 3.2, ND)
    return np.round(r, 1)


def flows(rng, ST):
    seas = np.array([smooth(i, [(0, 0.85), (di(4, 1), 1.45), (di(6, 1), 1.25), (di(8, 1), 0.80), (di(9, 15), 0.70),
                                (di(10, 31), 0.78)]) for i in range(ND)])
    Q, QS = {}, {}
    for k in SUBS:
        q = BASE[k] * seas * np.exp(rng.normal(0, 0.025, ND))
        qs = np.zeros(ND)
        shape = np.array([0.55] + [math.exp(-(t - 1) / TAU[k]) for t in range(1, 25)])
        for d, mm, fac in ST:
            wet = 1.0 if di(4, 1) <= d <= di(7, 15) else 0.75
            vol = RRATIO[k] * wet * mm / 1000.0 * AREA_KM2[k] * 1e6 * fac[k]
            pk = vol / (86400.0 * shape.sum())
            for t in range(len(shape)):
                if d + t < ND:
                    qs[d + t] += pk * shape[t]
        Q[k] = q + qs
        QS[k] = qs
    return Q, QS


TEMP_PTS = dict(
    TES=[(0, 0.6), (di(3, 20), 3.0), (di(4, 15), 9.5), (di(5, 15), 16.8), (di(6, 10), 22.4), (di(7, 15), 25.6),
         (di(8, 1), 25.8), (di(8, 25), 23.8), (di(9, 20), 19.0), (di(10, 31), 9.8)],
    FEN=[(0, 6.6), (di(3, 20), 7.2), (di(4, 15), 8.1), (di(5, 15), 9.0), (di(5, 25), 9.86), (di(5, 28), 10.13),
         (di(6, 1), 10.36), (di(6, 10), 10.93),
         (di(6, 25), 11.95), (di(7, 1), 12.3), (di(7, 15), 13.3), (di(8, 1), 14.05), (di(8, 15), 14.45),
         (di(9, 1), 15.3), (di(9, 15), 16.0), (di(9, 25), 15.2), (di(10, 31), 10.6)],
    OXL=[(0, 0.4), (di(3, 20), 3.2), (di(4, 15), 10.2), (di(5, 15), 17.6), (di(6, 10), 23.4), (di(7, 15), 26.4),
         (di(8, 1), 26.6), (di(8, 25), 24.2), (di(9, 20), 18.6), (di(10, 31), 9.0)],
    DUN=[(0, 1.2), (di(3, 20), 4.0), (di(4, 15), 10.0), (di(5, 15), 15.6), (di(6, 10), 20.0), (di(7, 15), 22.6),
         (di(8, 1), 22.8), (di(8, 25), 21.4), (di(9, 20), 17.4), (di(10, 31), 9.4)],
    LAD=[(0, 7.0), (di(3, 20), 7.3), (di(4, 15), 8.0), (di(5, 15), 8.7), (di(6, 10), 9.2), (di(7, 15), 9.8),
         (di(8, 10), 10.1), (di(9, 1), 10.2), (di(9, 25), 10.0), (di(10, 31), 8.8)])
DIURNAL = dict(TES=1.6, FEN=0.35, OXL=2.6, DUN=1.4, LAD=0.25)            # C, half-range of the daily cycle


def wtemps(rng, QS):
    eff = dict(TES=-1.6, FEN=0.10, OXL=-2.0, DUN=-1.2, LAD=0.05)
    sd = dict(TES=0.25, FEN=0.07, OXL=0.30, DUN=0.20, LAD=0.06)
    T = {}
    for k in SUBS:
        base = np.array([smooth(i, TEMP_PTS[k]) for i in range(ND)])
        rel = QS[k] / max(QS[k].max(), 1e-6)
        T[k] = np.maximum(base + eff[k] * np.clip(rel * 3, 0, 1) + rng.normal(0, sd[k], ND), 0.05)
    return T


def atrazine(rng, Q, QS, ST):
    """A field stock built by the season's applications and lost to breakdown, washed off by each storm in
    proportion to its rain; the storm's export rides its runoff, more of it on the rising days; a baseflow part
    that groundwater-fed creeks carry more of."""
    C = {}
    for k in SUBS:
        g = np.array([GW[k] * smooth(i, [(0, 0.35), (di(4, 20), 0.4), (di(6, 15), 1.0), (di(8, 30), 1.0),
                                          (di(10, 31), 0.6)]) for i in range(ND)])
        stock, ex = 0.0, np.zeros(ND)
        for i in range(ND):
            if di(4, 18) <= i <= di(6, 20):
                stock += APPLIED[k] * math.exp(-((i - di(5, 14)) / 15.0) ** 2) / (15.0 * math.sqrt(math.pi))
            stock *= math.exp(-math.log(2) / 25.0)
            for d, mm, fac in ST:
                if i == d and stock > 1e-6:
                    e = stock * (1 - math.exp(-0.0042 * mm * fac[k]))
                    stock -= e
                    w = np.array([QS[k][j] * (1.6 if j - d <= 1 else 1.0) * math.exp(-(j - d) / 3.0)
                                  if j < ND else 0.0 for j in range(d, d + 10)])
                    if w.sum() > 0:
                        for t, ww in enumerate(w):
                            if d + t < ND:
                                ex[d + t] += e * ww / w.sum()
        a0, a1 = di(4, 1), di(9, 30) + 1
        cur = ex[a0:a1].sum()
        ex = ex * (EXPORT[k] * APPLIED[k] / cur) if cur > 0 else ex
        cs = ex * 1e9 / np.maximum(Q[k] * 86400.0 * 1000.0, 1)
        C[k] = (g + cs) * np.exp(rng.normal(0, 0.03, ND))
    return C


# ------------------------------------------------------------------ the reservoir, a stack of parcels
class Lake:
    def __init__(self, elev_ft, c0):
        s = storage_ft(elev_ft)
        n = 40
        self.v = np.full(n, s / n)
        self.m = np.zeros((n, NK))
        self.m[:, KEYS.index("OLD")] = c0 * 1e-6 * self.v

    def bounds(self):
        cs = np.concatenate([[0.0], np.cumsum(self.v)])
        e = np.interp(cs, _S, _E)
        return e[:-1], e[1:]

    def mids(self):
        lo, hi = self.bounds()
        return (lo + hi) / 2

    def surface(self):
        return elev_of_storage(self.v.sum())

    def insert(self, elev, vol, mass):
        lo, hi = self.bounds()
        j = min(int(np.searchsorted(hi, elev)), len(self.v) - 1)
        den = stor_of_elev(hi[j]) - stor_of_elev(lo[j])
        f = (stor_of_elev(elev) - stor_of_elev(lo[j])) / den if den > 1e-9 else 0.5
        f = min(max(f, 0.0), 1.0)
        nv = np.concatenate([self.v[:j], [self.v[j] * f, vol, self.v[j] * (1 - f)], self.v[j + 1:]])
        nm = np.vstack([self.m[:j], (self.m[j] * f)[None], mass[None], (self.m[j] * (1 - f))[None], self.m[j + 1:]])
        self.v, self.m = nv, nm
        self.tidy()

    def withdraw(self, vol, weights, cap=0.9):
        if vol <= 0:
            return np.zeros(NK)
        take = vol * weights / weights.sum()
        for _ in range(60):
            over = take > cap * self.v + 1e-6
            if not over.any():
                break
            excess = (take[over] - cap * self.v[over]).sum()
            take[over] = cap * self.v[over]
            room = (~over) & (self.v > 0)
            if not room.any():
                break
            w2 = weights * room
            take = take + excess * w2 / w2.sum()
        frac = np.where(self.v > 0, take / self.v, 0)
        mt = (self.m * frac[:, None]).sum(axis=0)
        self.m = self.m * (1 - frac)[:, None]
        self.v = self.v - take
        self.tidy()
        return mt

    def merge(self, mask):
        idx = np.where(mask)[0]
        if len(idx) < 2:
            return
        a, b = idx[0], idx[-1]
        v = self.v[a:b + 1].sum()
        m = self.m[a:b + 1].sum(axis=0)
        self.v = np.concatenate([self.v[:a], [v], self.v[b + 1:]])
        self.m = np.vstack([self.m[:a], m[None], self.m[b + 1:]])

    def tidy(self):
        if (self.v <= 50.0).any():
            v, m = list(self.v), list(self.m)
            i = 0
            while i < len(v):
                if v[i] <= 50.0 and len(v) > 1:
                    t = i + 1 if i + 1 < len(v) else i - 1
                    v[t] += v[i]
                    m[t] = m[t] + m[i]
                    del v[i], m[i]
                    continue
                i += 1
            self.v, self.m = np.array(v), np.array(m)
        while len(self.v) > 160:
            j = int(np.argmin(self.v[:-1] + self.v[1:]))
            self.merge(np.isin(np.arange(len(self.v)), [j, j + 1]))

    def diffuse(self, kz, mixed_mask, thermo_mask):
        for j in range(len(self.v) - 1):
            if mixed_mask[j] and mixed_mask[j + 1]:
                continue
            r = kz * (0.015 if (thermo_mask[j] or thermo_mask[j + 1]) else 1.0)
            ex = r * min(self.v[j], self.v[j + 1])
            f = ex * (self.m[j] / self.v[j] - self.m[j + 1] / self.v[j + 1])
            self.m[j] -= f
            self.m[j + 1] += f


def entry_depth(i, surf_m, t_in):
    """Depth below the surface at which an inflow this warm enters the lake on day i (None when it is mixed)."""
    ts, tb, zt, ww = profile_params(i)
    if zt >= 29.0:
        return None
    bot = BOTTOM_FT * FT
    zz = np.linspace(0.05, surf_m - bot - 0.05, 400)
    tt = np.array([temp_at(i, z) for z in zz])
    if t_in >= tt[0]:
        return 0.3
    if t_in <= tt[-1]:
        return surf_m - bot - 0.2
    return float(np.interp(-t_in, -tt, zz))


def simulate(rng, Q, T, C, sig_out=0.8, kz=0.012, c0=0.32, hl_epi=110.0, hl_hyp=240.0):
    """Run the lake day by day. Returns per-day records: the intake's atrazine by source (ug/L), the intake's
    water temperature, each inflow's entry depth, the surface elevation, the spill and the outlet release."""
    lake = Lake(862.4, c0)
    bot = BOTTOM_FT * FT
    intake_m = INTAKE_FT * FT
    queue = {k: [] for k in SUBS}
    cap_s = storage_ft(FULL_POOL_FT)
    q_city = city_draw(rng)
    rec = []
    for i in range(ND):
        surf = lake.surface()
        ts, tb, zt, ww = profile_params(i)
        mixed = zt >= 29.0
        entry = {}
        for k in SUBS:
            queue[k].append((i + LAG[k], Q[k][i] * 86400.0, C[k][i] * Q[k][i] * 86400.0 / 1e6, T[k][i]))
        arrivals = []
        for k in SUBS:
            arr = [x for x in queue[k] if x[0] == i]
            queue[k] = [x for x in queue[k] if x[0] != i]
            arrivals += [(k,) + x[1:] for x in arr]
        for k, v_in, m_in, t_in in arrivals:
            mass = np.zeros(NK)
            mass[KEYS.index(k)] = m_in
            z_e = entry_depth(i, surf, t_in)
            if z_e is None:
                lo, hi = lake.bounds()
                e = (lo[0] + hi[-1]) / 2
            else:
                e = surf - z_e
            entry[k] = z_e
            lake.insert(e, v_in, mass)
        surf = lake.surface()
        zmix = 999.0 if mixed else max(0.8, zt - 1.3 * ww)
        lake.merge(surf - lake.mids() < zmix)
        surf = lake.surface()
        mids = lake.mids()
        depth = surf - mids
        wI = lake.v * np.exp(-0.5 * ((mids - intake_m) / sig_out) ** 2)
        wIn = wI / wI.sum()
        conc = lake.m / lake.v[:, None] * 1e6
        by = {k: float((conc[:, n] * wIn).sum()) for n, k in enumerate(KEYS)}
        prof = np.array([temp_at(i, max(0.05, d)) for d in depth])
        t_int = float((prof * wIn).sum())
        lake.withdraw(q_city[i] * 86400.0, wI)
        q_rel = 1.30 + 0.05 * sum(Q[k][i] for k in SUBS)
        mids = lake.mids()
        lake.withdraw(q_rel * 86400.0, lake.v * np.exp(-((mids - bot) / 4.0) ** 2), cap=0.6)
        evap = 0.0050 * area_ft(lake.surface() / FT) * (1.0 if 120 < i < 270 else 0.3)
        lake.v[-1] = max(lake.v[-1] - evap, 60.0)
        spill = max(0.0, lake.v.sum() - cap_s)
        if spill > 0:
            depth = lake.surface() - lake.mids()
            lake.withdraw(spill, lake.v * np.exp(-np.clip(depth, 0, None) / 1.5), cap=0.95)
        surf = lake.surface()
        depth = surf - lake.mids()
        lake.diffuse(kz, depth < zmix, (np.abs(depth - zt) < 2.0 * ww) & (not mixed))
        hl = np.where(depth < max(zmix, 3.0), hl_epi, hl_hyp)
        lake.m = lake.m * np.exp(-math.log(2) / hl)[:, None]
        rec.append(dict(i=i, date=day(i), surf_m=surf, by=by, intake=sum(by.values()), intake_t=t_int,
                        entry=entry, spill_m3s=spill / 86400.0, rel_m3s=q_rel, city_m3s=q_city[i], zt=zt,
                        evap_m3=evap, mass={k: float(lake.m[:, n].sum()) for n, k in enumerate(KEYS)}))
    return rec


def city_draw(rng):
    """The plant's raw-water pumping, m3/s: a summer peak, weekday rhythm and day-to-day noise."""
    base = np.array([smooth(i, [(0, 5.6), (di(5, 1), 6.2), (di(7, 15), 7.3), (di(9, 1), 6.8), (di(10, 31), 5.9)])
                     for i in range(ND)])
    wk = np.array([1.03 if day(i).weekday() < 5 else 0.94 for i in range(ND)])
    return base * wk * np.exp(rng.normal(0, 0.035, ND)) * MGD


def build(seed=SEED):
    rng = np.random.default_rng(seed)
    ST = storms(rng)
    rain = rainfall(rng, ST)
    Q, QS = flows(rng, ST)
    T = wtemps(rng, QS)
    C = atrazine(rng, Q, QS, ST)
    rec = simulate(np.random.default_rng(seed + 1), Q, T, C)
    return dict(ST=ST, rain=rain, Q=Q, QS=QS, T=T, C=C, rec=rec)


if __name__ == "__main__":
    W = build()
    rec = W["rec"]
    for k in SUBS:
        q, c = W["Q"][k], W["C"][k]
        load = sum(q[i] * c[i] * 86400 / 1e6 for i in range(di(4, 1), di(9, 30) + 1))
        print("%s load %.1f kg  peak C %.1f" % (k, load, c.max()))
    ex = [r for r in rec if r["intake"] > TRIGGER]
    print("truth days above trigger:", len(ex))
    print({k: sum(1 for r in ex if r["intake"] - r["by"][k] <= TRIGGER) for k in SUBS})
    print("max other share on those days:", max(max(r["by"][k] for k in SUBS if k != "FEN") for r in ex))
