"""Port Ardell: the clean truth (lots, streets, areas, homes, permits 2008-2026) and the 2027 expectation.

Everything downstream (the pack, the golden, the checks) reads this module's World. One RNG stream per
component, fixed seeds, so two runs are byte-identical."""
import numpy as np
import datetime as dt

SEED = 175
R0 = 0.050        # yearly permit chance of a served dry vacant lot on a well-built street, market 1.0
CANAL = 1.45      # canal-front lots
CUST = 0.15       # share of the served chance that ignores the street (owner-builders, custom homes)
F0 = 0.15         # street term on a street with no home, relative to a well-built street
F1 = 0.78         # street term with one home standing on the street
FK = 2.5          # homes over which the term rises from F1 towards a well-built street
UNS = 0.012       # unserved (well and septic) chance relative to R0, flat across streets
MARKET = {2008: 0.55, 2009: 0.30, 2010: 0.28, 2011: 0.32, 2012: 0.45, 2013: 0.65, 2014: 0.80, 2015: 0.90,
          2016: 1.00, 2017: 1.05, 2018: 1.10, 2019: 1.05, 2020: 1.00, 2021: 1.45, 2022: 1.55, 2023: 1.00,
          2024: 1.00, 2025: 1.00, 2026: 1.00}
SEASON = np.array([0.074, 0.079, 0.094, 0.091, 0.090, 0.086, 0.081, 0.084, 0.079, 0.086, 0.077, 0.079])
SEASON = SEASON / SEASON.sum()
YEARS = list(range(2008, 2027))

# area, phase now, phase stored before the 2021 regrouping, accepted, units, built share 2008, started share, canal share
AREAS = [
    ("Core", "Core", "Core", None, 12, 0.66, 0.97, 0.40),
    ("Southwest 5", "1", "1", "2010-03-22", 2, 0.36, 0.92, 0.34),
    ("Southwest 6", "1", "1", "2011-02-14", 2, 0.33, 0.91, 0.31),
    ("Central 1", "1", "1", "2012-05-07", 2, 0.31, 0.90, 0.28),
    ("Central 2", "1", "1", "2013-01-28", 2, 0.29, 0.89, 0.30),
    ("Southwest 7", "2", "1", "2014-04-14", 2, 0.27, 0.88, 0.33),
    ("Central 3", "2", "2", "2015-06-01", 2, 0.25, 0.87, 0.24),
    ("Central 4", "2", "2", "2016-02-22", 2, 0.23, 0.86, 0.22),
    ("North 1", "2", "2", "2017-03-13", 2, 0.21, 0.85, 0.20),
    ("North 2", "3", "2", "2018-05-21", 2, 0.19, 0.84, 0.18),
    ("Southwest 8", "3", "2", "2019-01-14", 2, 0.18, 0.83, 0.29),
    ("North 3", "3", "3", "2020-02-10", 2, 0.16, 0.82, 0.15),
    ("North 4", "3", "3", "2021-04-19", 2, 0.15, 0.81, 0.14),
    ("Northwest 1", "4", "4", "2022-03-07", 2, 0.14, 0.80, 0.12),
    ("North 5", "4", "4", "2023-02-27", 2, 0.13, 0.79, 0.10),
    ("Northwest 2", "4", "4", "2024-01-22", 2, 0.12, 0.78, 0.11),
    ("North 6", "5", "5", "2027-01-04", 3, 0.022, 0.13, 0.05),
    ("North 7", "5", "5", "2027-02-01", 3, 0.020, 0.12, 0.04),
    ("Northwest 3", "5", "5", "2027-04-13", 3, 0.024, 0.14, 0.06),
    ("North 8", "6", "6", "2028-03-01", 2, 0.018, 0.11, 0.05),
    ("North 9", "6", "6", "2029-03-01", 2, 0.016, 0.10, 0.04),
    ("Northwest 4", "6", "6", "2029-09-01", 2, 0.019, 0.11, 0.05),
    ("Northwest 5", "6", "6", "2030-03-01", 2, 0.017, 0.10, 0.04),
]
FORWARD = ["North 6", "North 7", "Northwest 3"]
LOT_W, LOT_D, STREET_W = 24.4, 38.1, 15.2   # 80 ft by 125 ft lots, 50 ft right of way


def f_street(n):
    """street term by the number of completed homes standing on the lot's street segment"""
    n = np.asarray(n)
    return np.where(n <= 0, F0, 1 - (1 - F1) * np.exp(-(np.maximum(n, 1) - 1) / FK))


def d(s):
    return dt.date.fromisoformat(s)


class World:
    def __init__(self, seed=SEED):
        self.seed = seed
        g = np.random.default_rng([seed, 1])
        lots = {k: [] for k in ("area", "unit", "block", "lotno", "seg", "side", "pos", "x", "y", "canal",
                                 "street", "hnum")}
        self.seg_street, self.seg_hblock, self.seg_unit = [], [], []
        self.unit_area, self.unit_no, self.unit_book = [], [], []
        blk_global = 0
        unit_no = 0
        self.area_names = [a[0] for a in AREAS]
        x_origin = 0.0
        for ai, (name, ph, ph_old, acc, nunits, b08, pst, cshare) in enumerate(AREAS):
            for ui in range(nunits):
                unit_no += 1
                self.unit_area.append(ai); self.unit_no.append(unit_no)
                self.unit_book.append((8 + unit_no // 4, 10 + (unit_no * 7) % 90))
                nrow = int(g.integers(7, 12)); ncol = int(g.integers(7, 12))
                kcol = g.integers(6, 15, size=ncol)        # lots per side on each segment of a column
                base_num = 100 * int(g.integers(8, 40))    # first hundred-block on this unit's grid
                street_base = int(g.integers(1, 40))
                prefix = name.split()[0][0] if name != "Core" else ["SE", "SW", "NE", "SE"][ui % 4]
                prefix = {"S": "SW", "C": "SE", "N": "NE"}.get(prefix, prefix) if name != "Core" else prefix
                if name.startswith("Northwest"):
                    prefix = "NW"
                elif name.startswith("North"):
                    prefix = "NE" if ui % 2 == 0 else "N"
                suffixes = ["St", "Ter", "Pl", "Ln", "Ct"]
                canal_blocks = g.random((nrow + 1, ncol)) < cshare
                blk_ids = np.arange((nrow + 1) * ncol).reshape(nrow + 1, ncol) + blk_global
                blk_global += (nrow + 1) * ncol
                lotno_in_blk = np.zeros((nrow + 1, ncol), dtype=int)
                for j in range(nrow):
                    sname = "%s %d%s %s" % (prefix, street_base + j, _ord(street_base + j), suffixes[(j + ui) % 5])
                    xs = 0.0
                    for c in range(ncol):
                        k = int(kcol[c])
                        sid = len(self.seg_street)
                        self.seg_street.append(sname); self.seg_hblock.append(base_num + 100 * c)
                        self.seg_unit.append(unit_no)
                        for side in (0, 1):            # 0 south side (even numbers), 1 north side (odd)
                            bj = j + side              # north side lots belong to the block above street j
                            for p in range(k):
                                lotno_in_blk[bj, c] += 1
                                lots["area"].append(ai); lots["unit"].append(unit_no)
                                lots["block"].append(int(blk_ids[bj, c])); lots["lotno"].append(int(lotno_in_blk[bj, c]))
                                lots["seg"].append(sid); lots["side"].append(side); lots["pos"].append(p)
                                lots["x"].append(x_origin + xs + p * LOT_W + LOT_W / 2)
                                lots["y"].append(j * (2 * LOT_D + STREET_W) + (1 if side else -1) * (STREET_W + LOT_D) / 2)
                                lots["canal"].append(bool(canal_blocks[bj, c]))
                                lots["street"].append(sname)
                                lots["hnum"].append(base_num + 100 * c + 4 * p + (5 if side else 2))
                        xs += k * LOT_W + STREET_W
                x_origin += 6000.0
        for k in lots:
            lots[k] = np.array(lots[k])
        self.L = lots
        self.N = len(lots["area"])
        self.nseg = len(self.seg_street)
        self.seg_n = np.bincount(lots["seg"], minlength=self.nseg)
        self.area_phase = [a[1] for a in AREAS]
        self.area_phase_old = [a[2] for a in AREAS]
        self.area_acc = [d(a[3]) if a[3] else None for a in AREAS]
        self._initial_homes()
        self._history()
        self._forward()

    # homes standing on 1 January 2008, built 1962 to 2007 on a clustered pattern
    def _initial_homes(self):
        g = np.random.default_rng([self.seed, 2])
        L = self.L
        built = np.zeros(self.N, dtype=bool)
        seg_area = np.array([self.unit_area[u - 1] for u in self.seg_unit])
        for ai, a in enumerate(AREAS):
            b08, pst = a[5], a[6]
            segs = np.where(seg_area == ai)[0]
            started = g.random(len(segs)) < pst
            mean_in = min(0.95, b08 / pst)
            a_, b_ = 2.2, 2.2 * (1 - mean_in) / mean_in
            sh = np.where(started, g.beta(a_, b_, size=len(segs)), 0.0)
            seg_share = np.zeros(self.nseg); seg_share[segs] = sh
            lots_a = np.where(L["area"] == ai)[0]
            built[lots_a] = g.random(len(lots_a)) < seg_share[L["seg"][lots_a]]
            # started segments hold at least one home
            for s in segs[started]:
                ls = np.where(L["seg"] == s)[0]
                if not built[ls].any():
                    built[g.choice(ls)] = True
        yb = np.zeros(self.N, dtype=int)
        n = built.sum()
        core = L["area"] == 0
        yb_draw = np.where(core[built], np.clip(np.round(g.normal(1988, 9, n)), 1962, 2007),
                           np.clip(np.round(g.normal(1999, 6, n)), 1970, 2007)).astype(int)
        yb[built] = yb_draw
        self.yb0 = yb               # year built for homes standing before 2008, else 0

    def served_weight(self, area_idx, year):
        """Share of the year's seasonal weight in which lots of the area are served (from the acceptance day)."""
        acc = self.area_acc[area_idx]
        if AREAS[area_idx][0] == "Core":
            return 1.0
        if acc is None or acc.year > year:
            return 0.0
        if acc.year < year:
            return 1.0
        m = acc.month - 1
        dim = _mdays(year, acc.month)
        return float(SEASON[m + 1:].sum() + SEASON[m] * (dim - acc.day + 1) / dim)

    def _rate(self, idx, share, served):
        base = R0 * np.where(self.L["canal"][idx], CANAL, 1.0)
        return base * np.where(served, CUST + (1 - CUST) * f_street(share), UNS)  # share holds the homes count

    def _history(self):
        g = np.random.default_rng([self.seed, 3])
        L = self.L
        N = self.N
        co = np.full(N, np.datetime64("NaT", "D"))     # completion of a permitted home
        issued = np.full(N, np.datetime64("NaT", "D"))
        pre = self.yb0 > 0
        area = L["area"]
        acc_m = np.array([(a.year * 12 + a.month - 1) if a else 10 ** 6 for a in self.area_acc])
        acc_m[0] = -10 ** 6
        acc_d = np.array([a.day if a else 1 for a in self.area_acc])
        rec = []
        for y in YEARS:
            jan1 = np.datetime64("%d-01-01" % y)
            done = pre | (co < jan1)
            cnt = np.bincount(L["seg"], weights=done.astype(float), minlength=self.nseg)
            s_lot = cnt[L["seg"]]
            vac0 = ~pre & np.isnat(issued)
            for m in range(12):
                mm = y * 12 + m
                dim = _mdays(y, m + 1)
                # served from the acceptance day: the month splits into an unserved and a served part
                first = np.where(acc_m[area] < mm, 1, np.where(acc_m[area] > mm, dim + 1, acc_d[area]))
                for part in (0, 1):
                    lo_day = np.where(part == 0, 1, first)
                    hi_day = np.where(part == 0, first - 1, dim)
                    frac = np.maximum(hi_day - lo_day + 1, 0) / dim
                    p = MARKET[y] * SEASON[m] * frac * self._rate(np.arange(N), s_lot, np.full(N, part == 1))
                    vac = ~pre & np.isnat(issued)
                    hit = vac & (frac > 0) & (g.random(N) < p)
                    k = hit.sum()
                    span = (hi_day[hit] - lo_day[hit] + 1)
                    days = lo_day[hit] - 1 + np.floor(g.random(k) * span).astype(int)
                    idate = np.datetime64("%d-%02d-01" % (y, m + 1)) + days.astype("timedelta64[D]")
                    issued[hit] = idate
                    lag = np.round(g.gamma(16.0, 16.0, size=k)).astype(int)
                    co[hit] = idate + lag.astype("timedelta64[D]")
            rec.append((y, vac0, s_lot.copy()))
        self.issued, self.co = issued, co
        self.rec = rec

    def _forward(self):
        L = self.L
        jan1 = np.datetime64("2027-01-01")
        done = (self.yb0 > 0) | (self.co < jan1)
        cnt = np.bincount(L["seg"], weights=done.astype(float), minlength=self.nseg)
        self.share27 = cnt[L["seg"]]      # homes standing on the lot's street at 1 January 2027
        vac = (self.yb0 == 0) & np.isnat(self.issued)
        self.vac27 = vac
        area = L["area"]
        exp = np.zeros(self.N)
        expq = np.zeros((self.N, 4))
        for ai, name in enumerate(self.area_names):
            if name not in FORWARD:
                continue
            idx = np.where((area == ai) & vac)[0]
            acc = self.area_acc[ai]
            for m in range(12):
                dim = _mdays(2027, m + 1)
                if m + 1 < acc.month:
                    fs = 0.0
                elif m + 1 > acc.month:
                    fs = 1.0
                else:
                    fs = (dim - acc.day + 1) / dim
                p = MARKET[2026] * SEASON[m] * (fs * self._rate(idx, self.share27[idx], np.full(len(idx), True)) +
                                                (1 - fs) * self._rate(idx, self.share27[idx], np.full(len(idx), False)))
                exp[idx] += p
                expq[idx, m // 3] += p
        self.exp27 = exp
        self.exp27q = expq

    def truth(self):
        out = {}
        for name in FORWARD:
            ai = self.area_names.index(name)
            sel = self.L["area"] == ai
            out[name] = float((1 - np.exp(-self.exp27[sel])).sum())   # expected distinct lots permitted
        out["total"] = sum(out[n] for n in FORWARD)
        return out


def _ord(n):
    return "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


def _mdays(y, m):
    nxt = dt.date(y + (m == 12), m % 12 + 1, 1)
    return (nxt - dt.date(y, m, 1)).days


if __name__ == "__main__":
    import time
    t = time.time()
    w = World()
    print("lots", w.N, "segments", w.nseg, "seconds", round(time.time() - t, 1))
    yrs = w.issued.astype("datetime64[Y]").astype(int) + 1970
    for y in YEARS:
        print(y, int((yrs == y).sum()), end="; ")
    print()
    print("truth 2027", {k: round(v, 1) for k, v in w.truth().items()})
    for ai, nm in enumerate(w.area_names):
        sel = w.L["area"] == ai
        built = ((w.yb0 > 0) | ~np.isnat(w.issued))[sel].mean()
        print(nm, sel.sum(), "built end-2026 %.3f" % built, "canal %.2f" % w.L["canal"][sel].mean())
