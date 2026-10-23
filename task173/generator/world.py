"""task173 world: Hollis Bend's water mains, service lines, premises and meters, every meter event from 2012 to
September 2026, every service leak and main break with its repair, the 2027 AMI install schedule and capital
program, and the restoration contractor's work. Everything here is the clean truth; pack.py writes the exports.

Time is an integer day offset from 2012-01-01 throughout."""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field

import numpy as np

import common as C

D0 = C.HIST_START
T_END = (C.RECORDS_END - D0).days            # last recorded day (inclusive)
T27 = (dt.date(2027, 1, 1) - D0).days
T28 = (dt.date(2028, 1, 1) - D0).days

MATS = ["CU", "GALV", "PB", "PE"]
BASE = {"CU": 0.0072, "GALV": 0.0218, "PB": 0.0231, "PE": 0.0040}     # leaks per service-year at age 35, zone 1
ZONE_F = {"UPPER": 1.14, "CENTRAL": 1.00, "RIVER": 0.90}
MONTH_F = np.array([1.12, 1.06, 0.86, 0.80, 0.84, 0.94, 1.18, 1.34, 1.30, 1.04, 0.78, 0.80])
MONTH_F = MONTH_F / MONTH_F.mean()
YEAR_F = {2012: 0.97, 2013: 1.03, 2014: 0.99, 2015: 1.02, 2016: 0.98, 2017: 1.01, 2018: 1.04, 2019: 0.98,
          2020: 1.00, 2021: 1.01, 2022: 1.05, 2023: 1.02, 2024: 0.99, 2025: 0.985, 2026: 1.01, 2027: 1.0}
# an exchange visit's induced chance of a leak, by the era the setter and angle valve were set in, and material
PX_ERA = [(1900, 1970, 0.0158), (1970, 1990, 0.0116), (1990, 2010, 0.0068), (2010, 2100, 0.0031)]
PX_MAT = {"CU": 1.0, "GALV": 1.15, "PB": 1.25, "PE": 0.9}
DELAY_SHAPE, DELAY_MEAN = 1.3, 24.0          # days from the visit to the leak showing
FREEZE = (dt.date(2021, 2, 15), dt.date(2021, 2, 24), 330)   # the February 2021 hard freeze: extra leaks


PX_SCALE = 0.906


def px_of(setter_yr, mat):
    p = 0.0
    for a, b, v in PX_ERA:
        if a <= setter_yr < b:
            p = v
    return p * PX_MAT[mat] * PX_SCALE


@dataclass
class World:
    seed: str = "w1"
    streets: list = field(default_factory=list)

    def __post_init__(self):
        self.r = C.stream("world/" + self.seed)
        self._streets()
        self._mains()
        self._services()
        self._premises()
        self._meters()
        self._capital()
        self._leaks()
        self._breaks()
        self._ami()
        self._restoration()

    # ------------------------------------------------------------------ geography
    def _streets(self):
        r = C.stream("streets")
        stems = ("Pecan Mesquite Live Oak Cedar Elm Hackberry Sycamore Bois d'Arc Cottonwood Willow Magnolia Redbud "
                 "Chinaberry Yaupon Agarita Huisache Persimmon Walnut Laurel Juniper Bluebonnet Primrose Indian Paint "
                 "Brush Sage Thistle Bluestem Gramma Switchgrass Caddo Comanche Tonkawa Wichita Brazos Navasota Lavaca "
                 "Guadalupe Nueces Frio Llano Pedernales Bosque Leon Lampasas Paluxy Sabinal Medina Blanco Colorado "
                 "Trinity Sulphur Angelina Neches Hickory Post Oak Blackjack Spanish Oak Chisholm Goodnight Loving "
                 "Kendall Travis Fannin Lamar Rusk Burleson Austin Houston Milam Bowie Crockett Navarro Seguin Zavala "
                 "Ruiz Navarro Menchaca Arocha Treviño Garza Benavides Salinas Cantu Villarreal Ybarra Escobedo "
                 "Hollis Tolliver Brennan Whitcomb Ashby Dunlap Kessler Harlan Prewitt Coker Stroud Ledbetter Pruitt "
                 "Haskett Mabry Odom Pickens Raney Sewell Tatum Upshaw Vick Wofford Yancey Bratton Cogburn Dorsey "
                 "Eakin Fulbright Gentry Hightower Ivey Jaco Kilgore Lusk Maddux Nunley Ogle Pettit Quarles Ridley "
                 "Spradlin Tidwell Vance Wheeler Yoakum Zuber Abernathy Bledsoe Cullen Daugherty Ennis Fowler").split()
        words, seen = [], set()
        i = 0
        while i < len(stems):
            w = stems[i]
            if w in ("Live", "Bois", "Indian", "Post", "Spanish"):
                w = w + " " + stems[i + 1]
                i += 1
            if w not in seen:
                seen.add(w)
                words.append(w)
            i += 1
        sufs = ["ST", "AVE", "DR", "LN", "CT", "TRL", "RD", "BLVD", "CIR", "PL", "WAY", "PKWY", "LOOP", "PASS"]
        sw = [.24, .12, .20, .14, .07, .05, .06, .02, .03, .02, .02, .01, .01, .01]
        out = set()
        while len(out) < 1150:
            w = words[r.integers(len(words))]
            pre = ""
            u = r.random()
            if u < 0.10:
                pre = ["N", "S", "E", "W"][r.integers(4)] + " "
            elif u < 0.16:
                pre = "OLD "
            s = sufs[r.choice(len(sufs), p=np.array(sw) / sum(sw))]
            out.add((pre + w.upper() + " " + s).replace("  ", " "))
        self.streets = sorted(out)

    # ------------------------------------------------------------------ mains
    def _mains(self):
        r = C.stream("mains")
        n = 9420
        era = r.choice(4, n, p=[.24, .31, .20, .25])            # CI, AC, DI, PVC
        mat = np.array(["CI", "AC", "DI", "PVC"])[era]
        yr = np.where(era == 0, r.integers(1928, 1966, n), np.where(era == 1, r.integers(1956, 1983, n),
                      np.where(era == 2, r.integers(1976, 2001, n), r.integers(1986, 2026, n))))
        dia = r.choice([4, 6, 8, 12, 16], n, p=[.08, .52, .26, .10, .04])
        length = np.round(r.gamma(2.2, 760, n) + 120).astype(int)
        # service centre and pressure zone come with the main's place; older areas sit toward the river
        cen = np.where(r.random(n) < np.where(yr < 1970, .52, .28), 0, np.where(r.random(n) < .55, 1, 2))
        cen = np.array(C.CENTERS)[cen]
        zone = np.where(r.random(n) < np.where(yr < 1970, .45, .20), "RIVER",
                        np.where(r.random(n) < .74, "CENTRAL", "UPPER"))
        st = r.integers(0, len(self.streets), n)
        ids = r.choice(np.arange(10000, 99999), n, replace=False)
        self.main_id = np.array(["WM-%05d" % i for i in ids])
        self.main_mat, self.main_yr, self.main_dia, self.main_len = mat, yr, dia, length
        self.main_cen, self.main_zone, self.main_st = cen, zone, st
        self.main_active_from = np.zeros(n, dtype=int) - 10 ** 6
        self.main_retired = np.zeros(n, dtype=int) + 10 ** 6
        self.n_mains = n

    # ------------------------------------------------------------------ services
    def _services(self):
        r = C.stream("services")
        # services per main roughly with length (about one per 70 feet of residential frontage)
        k = np.maximum(1, r.poisson(self.main_len / 121.0))
        midx = np.repeat(np.arange(self.n_mains), k)
        n = len(midx)
        myr = self.main_yr[midx]
        inst = myr + np.where(r.random(n) < .82, 0, r.integers(0, 25, n))
        inst = np.minimum(inst, 2025)
        u = r.random(n)
        mat = np.where(inst < 1962, np.where(u < .58, "GALV", "CU"),
                       np.where(inst < 1979, np.where(u < .12, "GALV", "CU"),
                                np.where(inst < 1996, np.where(u < .46, "PB", "CU"),
                                         np.where(u < .70, "PE", "CU"))))
        # new connections 2012-2026 (growth), on PVC mains in the newer areas
        newer = np.nonzero(self.main_yr >= 2005)[0]
        nnew = 9100
        nm = newer[r.integers(0, len(newer), nnew)]
        ndays = np.sort(r.integers(0, T_END + 1, nnew))
        midx = np.concatenate([midx, nm])
        inst = np.concatenate([inst, np.array([(D0 + dt.timedelta(days=int(d))).year for d in ndays])])
        mat = np.concatenate([mat, np.where(r.random(nnew) < .74, "PE", "CU")])
        start = np.concatenate([np.full(n, -10 ** 6), ndays])
        N = len(midx)
        self.n_svc = N
        self.svc_main = midx
        self.svc_inst = inst.astype(int)
        self.svc_mat0 = mat.copy()                   # material as laid (before any renewal)
        self.svc_mat = mat.copy()
        self.svc_start = start.astype(int)
        self.svc_size = np.where(r.random(N) < .90, "3/4", np.where(r.random(N) < .7, "1", "2"))
        self.svc_zone = self.main_zone[midx]
        self.svc_cen = self.main_cen[midx]
        self.svc_frail = r.gamma(2.6, 1 / 2.6, N)
        self.svc_renew = np.full(N, 10 ** 6)        # day the service was renewed by a capital project
        self.svc_setter_yr = self.svc_inst.copy()
        ids = r.choice(np.arange(100000, 999999), N, replace=False)
        self.svc_id = np.array(["SV-%06d" % i for i in ids])
        # addresses: house numbers along the main's street
        st = self.main_st[midx].copy()
        hn = np.zeros(N, dtype=int)
        base_no = r.integers(1, 98, self.n_mains) * 100
        order = np.argsort(midx, kind="stable")
        pos = np.zeros(N, dtype=int)
        cnt = np.zeros(self.n_mains, dtype=int)
        for j in order:
            m = midx[j]
            pos[j] = cnt[m]
            cnt[m] += 1
        hn = base_no[midx] + 2 * pos + (r.random(N) < .5)
        # a few services sit on a cross street at a corner
        cross = r.random(N) < .04
        st[cross] = r.integers(0, len(self.streets), cross.sum())
        self.svc_hn, self.svc_st = hn, st
        # de-duplicate exact address collisions by bumping the number
        seen = {}
        for j in range(N):
            key = (int(self.svc_hn[j]), int(self.svc_st[j]))
            while key in seen:
                self.svc_hn[j] += 200
                key = (int(self.svc_hn[j]), int(self.svc_st[j]))
            seen[key] = j

    def address(self, j):
        return "%d %s" % (self.svc_hn[j], self.streets[self.svc_st[j]])

    # ------------------------------------------------------------------ premises
    def _premises(self):
        r = C.stream("premises")
        N = self.n_svc
        k = np.where(r.random(N) < .955, 1, np.where(r.random(N) < .8, 2, r.integers(3, 5, N)))
        k[self.svc_start > 0] = 1
        p_svc = np.repeat(np.arange(N), k)
        unit = np.concatenate([[""] if kk == 1 else (["A", "B", "C", "D"][:kk]) for kk in k])
        P = len(p_svc)
        ids = r.choice(np.arange(1000000, 9999999), P, replace=False)
        self.prem_id = np.array(["%07d" % i for i in ids])
        self.prem_svc = p_svc
        self.prem_unit = unit
        self.n_prem = P
        # meter reading routes: 520, by centre, contiguous in street order
        self.prem_route = np.zeros(P, dtype=int)
        rid = 0
        self.route_cen = []
        for cen in C.CENTERS:
            idx = np.nonzero(self.svc_cen[p_svc] == cen)[0]
            idx = idx[np.lexsort((self.svc_hn[p_svc[idx]], self.svc_st[p_svc[idx]]))]
            nr = int(round(520 * len(idx) / P))
            for chunk in np.array_split(idx, nr):
                self.prem_route[chunk] = rid
                self.route_cen.append(cen)
                rid += 1
        self.n_routes = rid
        pref = {"NORTH": "N", "SOUTH": "S", "WEST": "W"}
        self.route_name = []
        cnt = {c: 100 for c in C.CENTERS}
        for i in range(rid):
            c = self.route_cen[i]
            cnt[c] += 1 + (r.random() < .07)
            self.route_name.append("%s-%03d" % (pref[c], cnt[c]))

    # ------------------------------------------------------------------ meters and exchanges
    def _meters(self):
        r = C.stream("meters")
        P = self.n_prem
        age0 = r.gamma(2.6, 4.4, P)                       # meter age in years on 2012-01-01
        age0 = np.minimum(age0, 34)
        start = self.svc_start[self.prem_svc]
        new = start > 0
        set_day = np.where(new, start, -np.round(age0 * 365.25).astype(int))
        ev_p, ev_t, ev_reason, ev_by, ev_gap = [], [], [], [], []
        cur = set_day.astype(float)
        mon_w = np.array([.06, .07, .09, .10, .10, .09, .09, .09, .09, .09, .07, .06])
        for y in range(2012, 2027):
            y0 = (dt.date(y, 1, 1) - D0).days
            y1 = min((dt.date(y + 1, 1, 1) - D0).days - 1, T_END)
            age = (y0 - cur) / 365.25
            p = np.clip(0.003 + 0.0068 * np.maximum(age - 12.5, 0), 0, 0.32)
            p = np.where(start > y1, 0, p)
            if y == 2022:
                p = p * 1.42
            m = np.nonzero(r.random(P) < p)[0]
            mon = r.choice(12, len(m), p=mon_w)
            d = np.array([(dt.date(y, mm + 1, 1) - D0).days for mm in mon]) + r.integers(0, 28, len(m))
            ok = (d <= y1) & (d > start[m] + 30)
            m, d = m[ok], d[ok]
            # workdays only
            wd = np.array([(D0 + dt.timedelta(days=int(x))).weekday() for x in d])
            d = d + np.where(wd == 5, 2, np.where(wd == 6, 1, 0))
            ok = d <= y1
            m, d = m[ok], d[ok]
            u = r.random(len(m))
            reason = np.where(u < .64, "AGE", np.where(u < .87, "STOP", np.where(u < .95, "TEST", np.where(u < .985, "CUST", "SIZE"))))
            if y == 2026:
                # scheduled age change-outs stop when the AMI contract is awarded (April 2026)
                keep = ~((reason == "AGE") & (d >= (dt.date(2026, 4, 1) - D0).days))
                m, d, reason, u = m[keep], d[keep], reason[keep], u[keep]
            by = np.where((y == 2022) & (reason == "STOP") & (r.random(len(m)) < .78), "ARR", "MSHOP")
            gap = np.where(r.random(len(m)) < .09, 1, 0)
            gap = np.where((gap == 1) & (np.array([(D0 + dt.timedelta(days=int(x))).weekday() for x in d]) == 4), 3, gap)
            ev_p.append(m); ev_t.append(d); ev_reason.append(reason); ev_by.append(by); ev_gap.append(gap)
            cur[m] = d + gap
        self.ex_prem = np.concatenate(ev_p)
        self.ex_day = np.concatenate(ev_t)
        self.ex_reason = np.concatenate(ev_reason)
        self.ex_by = np.concatenate(ev_by)
        self.ex_gap = np.concatenate(ev_gap)
        o = np.lexsort((self.ex_prem, self.ex_day))
        for a in ("ex_prem", "ex_day", "ex_reason", "ex_by", "ex_gap"):
            setattr(self, a, getattr(self, a)[o])
        self.ex_svc = self.prem_svc[self.ex_prem]
        self.meter_set_day = cur.astype(int)                # set day of the meter in place on 2026-09-30
        self.prem_first_set = set_day.astype(int)
        # meter numbers: one per meter ever set
        nmeters = P + len(self.ex_prem)
        mids = r.choice(np.arange(10 ** 7, 9 * 10 ** 7), nmeters, replace=False)
        self.meter_no_initial = mids[:P]
        self.meter_no_ex = mids[P:]

    # ------------------------------------------------------------------ capital renewals
    def _capital(self):
        r = C.stream("capital")
        old = np.nonzero((self.main_mat == "CI") | ((self.main_mat == "AC") & (self.main_yr < 1972)))[0]
        r.shuffle(old)
        used = 0
        self.cap_hist = []         # (main index, completion day)
        for y in range(2012, 2027):
            nm = int(r.integers(15, 22))
            for m in old[used:used + nm]:
                d = (dt.date(y, int(r.integers(2, 12)), int(r.integers(1, 28))) - D0).days
                if d > T_END:
                    continue
                self.cap_hist.append((int(m), d))
            used += nm
        self.cap_2027 = []
        pool = old[used:used + 30]
        months = [2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 12]
        for i, m in enumerate(pool[:22]):
            d = (dt.date(2027, months[i], 1) - D0).days + int(r.integers(5, 25))
            self.cap_2027.append((int(m), d))
        svc_by_main = {}
        for j, m in enumerate(self.svc_main):
            svc_by_main.setdefault(int(m), []).append(j)
        self.svc_by_main = svc_by_main
        for m, d in self.cap_hist:
            for j in svc_by_main.get(m, []):
                if self.svc_start[j] < d:
                    self.svc_renew[j] = d
                    self.svc_mat[j] = "PE"
                    self.svc_setter_yr[j] = (D0 + dt.timedelta(days=d)).year
            self.main_retired[m] = d
        self.svc_renew27 = np.full(self.n_svc, 10 ** 6)
        for m, d in self.cap_2027:
            for j in svc_by_main.get(m, []):
                self.svc_renew27[j] = d

    # ------------------------------------------------------------------ hazards
    def base_rate(self, j_idx, year, after_renew):
        """annual leak rate of services j_idx in a calendar year, on the service as it stood"""
        if not hasattr(self, "_b0"):
            self._b0 = np.array([BASE[m] for m in self.svc_mat0])
            self._zf = np.array([ZONE_F[z] for z in self.svc_zone])
        age = np.where(after_renew, 3, np.maximum(year - self.svc_inst[j_idx], 0))
        b = np.where(after_renew, BASE["PE"], self._b0[j_idx])
        return b * np.exp(0.0105 * (age - 35)) * self._zf[j_idx] * self.svc_frail[j_idx]

    def _leaks(self):
        r = C.stream("leaks")
        N = self.n_svc
        rows_s, rows_t, rows_kind, rows_x = [], [], [], []
        allj = np.arange(N)
        for y in range(2012, 2027):
            for mth in range(1, 13):
                a = (dt.date(y, mth, 1) - D0).days
                if a > T_END:
                    break
                b = (dt.date(y + (mth == 12), mth % 12 + 1, 1) - D0).days
                ndays = b - a
                live = self.svc_start < b
                ren = self.svc_renew < a + ndays / 2
                lam = self.base_rate(allj, y, ren) * MONTH_F[mth - 1] * YEAR_F[y] * ndays / 365.25
                lam = np.where(live, lam, 0)
                c = r.poisson(lam)
                j = np.repeat(np.nonzero(c)[0], c[c > 0])
                lo = np.maximum(a, self.svc_start[j] + 1)
                t = lo + np.floor(r.random(len(j)) * (b - lo)).astype(int)
                rows_s.append(j); rows_t.append(t); rows_kind.append(np.full(len(j), 0)); rows_x.append(np.full(len(j), -1))
        # the February 2021 freeze
        f0 = (FREEZE[0] - D0).days
        f1 = (FREEZE[1] - D0).days
        w = self.base_rate(allj, 2021, self.svc_renew < f0) * np.where(self.svc_start < f0, 1, 0)
        j = r.choice(N, FREEZE[2], p=w / w.sum())
        rows_s.append(j); rows_t.append(r.integers(f0, f1 + 1, len(j))); rows_kind.append(np.full(len(j), 2)); rows_x.append(np.full(len(j), -1))
        # induced by exchange visits
        svc = self.ex_svc
        sy = self.svc_setter_yr.copy()
        # a setter renewed after the visit does not count backward; setter year at the visit
        sy_at = np.where(self.svc_renew[svc] <= self.ex_day, [int((D0 + dt.timedelta(days=int(d))).year) for d in self.svc_renew[svc].clip(0, 20000)], self.svc_inst[svc])
        mat_at = np.where(self.svc_renew[svc] <= self.ex_day, "PE", self.svc_mat0[svc])
        self.ex_px = np.array([px_of(int(a), b) for a, b in zip(sy_at, mat_at)])
        hit = r.random(len(svc)) < self.ex_px
        dly = np.ceil(r.gamma(DELAY_SHAPE, DELAY_MEAN / DELAY_SHAPE, len(svc))).astype(int)
        t = self.ex_day + self.ex_gap + dly
        k = hit & (t <= T_END + 60)
        rows_s.append(svc[k]); rows_t.append(t[k]); rows_kind.append(np.full(k.sum(), 1)); rows_x.append(np.nonzero(k)[0])
        s = np.concatenate(rows_s); t = np.concatenate(rows_t)
        kind = np.concatenate(rows_kind); xi = np.concatenate(rows_x)
        # leaks on a service renewed before the leak are on the new service (renewal resets); drop those before start
        ok = t > self.svc_start[s]
        s, t, kind, xi = s[ok], t[ok], kind[ok], xi[ok]
        # report and repair
        rep = t + np.floor(r.exponential(1.4, len(t))).astype(int)
        fix = rep + np.floor(r.exponential(2.6, len(t))).astype(int) + (r.random(len(t)) < .1) * r.integers(3, 12, len(t))
        o = np.lexsort((s, t))
        self.lk_svc, self.lk_t, self.lk_kind, self.lk_ex = s[o], t[o], kind[o], xi[o]
        self.lk_rep, self.lk_fix = rep[o], fix[o]
        n = len(self.lk_svc)
        comp_b = ["SERVICE PIPE", "CORP STOP", "ANGLE VALVE", "METER COUPLING", "SETTER", "METER BOX"]
        pb = [.55, .12, .10, .10, .08, .05]
        pi = [.16, .02, .40, .30, .12, .00]
        u = r.random(n)
        cb = np.searchsorted(np.cumsum(pb), u * .9999)
        ci = np.searchsorted(np.cumsum(pi), u * .9999)
        self.lk_comp = np.where(self.lk_kind == 1, np.array(comp_b)[ci], np.array(comp_b)[cb])
        self.lk_inv = r.random(n) < .38            # an investigation order before the repair
        self.lk_rst = r.random(n) < .64            # needs restoration by the contractor

    def expected_2027(self):
        """the 2027 expectation: each service's own rate (renewed services from their 2027 completion) plus each
        scheduled exchange's induced chance that its repair falls in 2027, plus late-2026 routine visits"""
        from scipy.stats import gamma
        N = self.n_svc
        allj = np.arange(N)
        tot = 0.0
        for mth in range(1, 13):
            a = (dt.date(2027, mth, 1) - D0).days
            b = (dt.date(2027 + (mth == 12), mth % 12 + 1, 1) - D0).days
            ren = (self.svc_renew < a) | (self.svc_renew27 < a + (b - a) / 2)
            lam = self.base_rate(allj, 2027, ren) * MONTH_F[mth - 1] * (b - a) / 365.25
            tot += lam.sum()
        base = tot
        ex = self.ami_exch
        sy = self.svc_setter_yr[self.prem_svc[ex]]
        mat = self.svc_mat[self.prem_svc[ex]]
        px = np.array([px_of(int(a), b) for a, b in zip(sy, mat)])
        # repair lag is about four days; the delay's tail past 31 December is negligible for a July finish
        rem = T28 - self.ami_day[ex] - 4
        ind = (px * gamma.cdf(rem, DELAY_SHAPE, scale=DELAY_MEAN / DELAY_SHAPE)).sum()
        # routine visits of October to December 2026 at the 2025 pace, their leaks that fall in 2027
        q4 = ((self.ex_day >= (dt.date(2025, 10, 1) - D0).days) & (self.ex_day < (dt.date(2026, 1, 1) - D0).days))
        late = (self.ex_px[q4] * 0.42).sum()
        return {"base": base, "induced": ind, "late2026": late, "total": base + ind + late, "px_mean": px.mean(),
                "n_exch": len(ex)}

    # ------------------------------------------------------------------ main breaks
    def _breaks(self):
        r = C.stream("breaks")
        rate = {"CI": 0.42, "AC": 0.27, "DI": 0.075, "PVC": 0.035}     # per mile-year
        b_m, b_t = [], []
        miles = self.main_len / 5280.0
        rate_arr = np.array([rate[x] for x in self.main_mat])
        for y in range(2012, 2027):
            for mth in range(1, 13):
                a = (dt.date(y, mth, 1) - D0).days
                if a > T_END:
                    break
                b = (dt.date(y + (mth == 12), mth % 12 + 1, 1) - D0).days
                live = (self.main_retired > a)
                lam = rate_arr * miles * MONTH_F[mth - 1] ** 1.6 * YEAR_F[y] * (b - a) / 365.25
                lam = np.where(live, lam, 0)
                c = r.poisson(lam)
                m = np.repeat(np.nonzero(c)[0], c[c > 0])
                b_m.append(m); b_t.append(a + r.integers(0, b - a, len(m)))
        m = np.concatenate(b_m); t = np.concatenate(b_t)
        o = np.lexsort((m, t))
        m, t = m[o], t[o]
        n0 = len(m)
        mins = r.integers(0, 1440, n0)                               # reported minute of the day
        u = r.random(n0)
        mode = np.where(u < .61, "CREW", np.where(u < .87, "HANDOFF", "CONTRACTOR"))
        # a second break found on the same main while the crew is out on the first call: its own repair, the same
        # call, another location along the main
        sec = (mode == "CREW") & (r.random(n0) < .11)
        k = np.nonzero(sec)[0]
        m = np.concatenate([m, m[k]]); t = np.concatenate([t, t[k]]); mins = np.concatenate([mins, mins[k]])
        mode = np.concatenate([mode, np.full(len(k), "CREW")])
        self.br_second = np.concatenate([np.zeros(n0, dtype=bool), np.ones(len(k), dtype=bool)])
        o = np.lexsort((self.br_second, m, t))
        self.br_main, self.br_day, self.br_min, self.br_mode = m[o], t[o], mins[o], mode[o]
        self.br_second = self.br_second[o]
        n = len(self.br_main)
        self.br_crew_fix = self.br_day + np.floor(r.exponential(0.6, n)).astype(int)
        self.br_perm = np.where(self.br_mode == "CREW", self.br_crew_fix,
                                self.br_day + 2 + np.floor(r.gamma(2.0, 5.5, n)).astype(int))
        own = np.array([C.CENTERS.index(c) for c in self.main_cen[m]])
        mutual = r.random(n) < .12
        other = (own + r.integers(1, 3, n)) % 3
        self.br_yard = np.array(C.CENTERS)[np.where(mutual, other, own)]
        self.br_rst = r.random(n) < .93

    # ------------------------------------------------------------------ the AMI schedule
    def _ami(self):
        r = C.stream("ami")
        P = self.n_prem
        cut = (dt.date(2019, 1, 1) - D0).days
        on_cap = self.svc_renew27[self.prem_svc] < 10 ** 6
        live = self.svc_start[self.prem_svc] <= T_END
        kind = np.where(on_cap, "D", np.where(self.meter_set_day < cut, "X", "R"))
        kind = np.where(live, kind, "")
        # routes in a deployment sequence, North first, two to three weeks each, February to July
        mondays = []
        d = C.AMI_FIRST
        while d <= C.AMI_LAST:
            mondays.append(d)
            d += dt.timedelta(days=7)
        order = np.argsort(np.array([C.CENTERS.index(self.route_cen[i]) + r.random() * 1.4 for i in range(self.n_routes)]), kind="stable")
        wk = np.zeros(self.n_routes, dtype=int)
        for rank, i in enumerate(order):
            wk[i] = min(int(rank * len(mondays) / self.n_routes), len(mondays) - 1)
        self.route_week = [mondays[w] for w in wk]
        pw = np.array([(self.route_week[self.prem_route[p]] - D0).days for p in range(P)])
        self.prem_kind = kind
        self.prem_week = pw
        self.ami_exch = np.nonzero(kind == "X")[0]
        # the install day: within the planned week (the schedule carries the week only)
        self.ami_day = np.zeros(P, dtype=int)
        self.ami_day[self.ami_exch] = pw[self.ami_exch] + r.integers(0, 5, len(self.ami_exch))

    # ------------------------------------------------------------------ restoration
    def _restoration(self):
        r = C.stream("restoration")
        # restoration sites: service leak repairs and main breaks that need surface restoration
        sites = []
        for i in np.nonzero(self.lk_rst)[0]:
            sites.append(("S", int(i), int(self.lk_fix[i])))
        for i in np.nonzero(self.br_rst)[0]:
            sites.append(("M", int(i), int(self.br_perm[i])))
        sites.sort(key=lambda x: (x[2], x[0], x[1]))
        out = []
        for typ, i, fixd in sites:
            done = fixd + 4 + int(r.gamma(2.2, 6.0))
            if typ == "S":
                u = r.random()
                items = [("0440", round(float(r.uniform(4, 24)), 1))] if u < .70 else []
                if u >= .55:
                    items.append(("0430" if r.random() < .6 else "0431", round(float(r.uniform(3, 14)), 1)))
                if r.random() < .08:
                    items.append(("0410", round(float(r.uniform(4, 12)), 1)))
            else:
                u = r.random()
                items = []
                if u < .62:
                    items.append(("0410", round(float(r.uniform(9, 46)), 1)))
                    items.append(("0460", round(float(r.uniform(14, 60)), 0)))
                elif u < .80:
                    items.append(("0420", round(float(r.uniform(8, 38)), 1)))
                    items.append(("0460", round(float(r.uniform(12, 44)), 0)))
                if r.random() < .45:
                    items.append(("0440", round(float(r.uniform(6, 40)), 1)))
                if r.random() < .25:
                    items.append(("0430", round(float(r.uniform(4, 18)), 1)))
                if r.random() < .22:
                    items.append(("0450", round(float(r.uniform(6, 30)), 0)))
            if items:
                out.append((typ, i, done, items))
        self.rst_sites = out
