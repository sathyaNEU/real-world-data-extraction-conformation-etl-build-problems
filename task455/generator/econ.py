"""The simulation behind the pack: the valley's employer accounts, the businesses they belong to and every worker's
spells of employment, October 2024 to December 2026. Accounts are planned county by county from world.py's event
counts; workers are linked across accounts by hire (job changes, a business's staff moving to its new account, summer
staff returning); the quarterly reports and wage records are read off the spells."""
import datetime as dt
from collections import defaultdict

import numpy as np

import names as N
import world as W

D = dt.date
DAY = dt.timedelta(days=1)


def qstart(y, q):
    return D(y, 3 * (q - 1) + 1, 1)


def qend(y, q):
    return (D(y + 1, 1, 1) if q == 4 else D(y, 3 * q + 1, 1)) - DAY


def qof(d):
    return (d.year, (d.month - 1) // 3 + 1)


def prevq(y, q):
    return (y - 1, 4) if q == 1 else (y, q - 1)


def nextq(y, q):
    return (y + 1, 1) if q == 4 else (y, q + 1)


MONTHS = [D(2024, 10, 1), D(2024, 11, 1), D(2024, 12, 1)] + [D(y, m, 1) for y in (2025, 2026) for m in range(1, 13)]
TWELFTHS = [m.replace(day=12) for m in MONTHS]


def last_emp_month(last):
    """The month of the last 12th on which a spell ending `last` was active."""
    return (last.year, last.month) if last.day >= 12 else ((last - dt.timedelta(days=last.day)).year,
                                                           (last - dt.timedelta(days=last.day)).month)


class Acct:
    __slots__ = ("idx", "county", "zip", "town", "zip_county", "minority", "ind", "naics22", "naics17", "noun", "kind",
                 "year", "first", "last", "size", "source", "succ_type", "relet_of", "relet_adj", "displaced",
                 "business", "final_pay", "left_open", "reg", "liab", "inact", "legal", "trade", "fein", "addr",
                 "seasonal", "seasons", "resume", "wage", "tenure", "role", "successor", "never", "expand",
                 "absorbed_by", "layoff", "spinout_of", "handover", "merged_into", "pause", "caretaker")

    def __init__(self, **kw):
        for s in self.__slots__:
            setattr(self, s, kw.get(s))


class World:
    def __init__(self):
        self.rng = np.random.default_rng(W.SEED)
        self.crng = np.random.default_rng(W.SEED + 83)      # summer employers' winter caretakers
        self.accts = []
        self.namer = N.Namer(np.random.default_rng(W.SEED + 1))
        self.addr_used = set()
        self.fein_used = set()
        self.next_business = 0
        ind = {r[0]: r for r in W.INDUSTRIES}
        self.ind = ind
        self.seasonal_ind = {r[0] + "s": r for r in W.SEASONAL_INDUSTRIES}

    # ------------------------------------------------------------------ helpers
    def r(self):
        return float(self.rng.random())

    def ri(self, a, b):
        return int(self.rng.integers(a, b + 1))

    def choice(self, seq):
        return seq[int(self.rng.integers(len(seq)))]

    def day_in(self, d0, d1):
        return d0 + dt.timedelta(days=int(self.rng.integers(0, (d1 - d0).days + 1)))

    def start_day(self, y, m):
        return D(y, m, self.ri(2, 12))

    def industry(self, county, pool=None):
        rows = [r for r in W.INDUSTRIES if pool is None or r[0] in pool]
        tilt = W.TILT[county]
        wts = np.array([tilt.get(r[0][:3], 1.0) for r in rows], dtype=float)
        return rows[int(self.rng.choice(len(rows), p=wts / wts.sum()))]

    def size(self, profile, lo=1, hi=400):
        tables = {
            "micro": ([1, 2, 3, 4, 5, 7, 11], [0.30, 0.25, 0.17, 0.11, 0.09, 0.06, 0.02]),
            "small": ([1, 2, 3, 4, 6, 8, 12, 16, 24, 38], [0.10, 0.11, 0.11, 0.10, 0.16, 0.13, 0.12, 0.08, 0.06, 0.03]),
            "mid": ([2, 4, 6, 9, 13, 18, 26, 40, 70, 140], [0.06, 0.09, 0.12, 0.15, 0.17, 0.14, 0.12, 0.09, 0.04, 0.02]),
            "birth": ([1, 2, 3, 4, 5, 7, 10, 15, 24], [0.22, 0.20, 0.15, 0.12, 0.10, 0.10, 0.07, 0.03, 0.01]),
        }
        vals, p = tables[profile]
        for _ in range(100):
            base = vals[int(self.rng.choice(len(vals), p=p))]
            n = max(1, int(round(base * float(self.rng.uniform(0.85, 1.2)))))
            if lo <= n <= hi:
                return n
        return max(lo, min(hi, n))

    def fein(self):
        while True:
            f = "%02d-%07d" % (self.ri(10, 98), self.ri(1000000, 9999999))
            if f not in self.fein_used:
                self.fein_used.add(f)
                return f

    def zip_for(self, county):
        code, name, seat, zips = next(c for c in W.COUNTIES if c[1] == county)
        border_major = {b[0] for b in W.BORDER if b[1] == county}
        wts = np.array([3.0 if t == seat else 1.0 for z, t in zips])
        z, t = zips[int(self.rng.choice(len(zips), p=wts / wts.sum()))]
        return z, t

    def address(self, county, zip_town=None, street=None, suite=None):
        z, t = zip_town or self.zip_for(county)
        for _ in range(500):
            if street is None:
                st = self.choice(W.STREETS)
                stype = self.choice(W.STREET_TYPES[:4] * 3 + W.STREET_TYPES[4:])
            else:
                st, stype = street[0], (street[1], street[2])
            num = self.ri(2, 98) * (10 if self.r() < 0.7 else 1) + self.ri(0, 9)
            dirn = self.choice(W.DIRECTIONS) if self.r() < 0.18 else None
            ste = suite if suite is not None else (str(self.ri(1, 12)) if self.r() < 0.07 else None)
            key = (z, num, dirn[1] if dirn else "", st, stype[1], ste or "")
            if key not in self.addr_used:
                self.addr_used.add(key)
                return {"zip": z, "town": t, "num": num, "dirn": dirn, "street": st, "stype": stype, "suite": ste}
        raise RuntimeError("address space exhausted")

    def acct(self, county, kind, ind=None, **kw):
        ind = ind or self.industry(county)
        a = Acct(idx=len(self.accts), county=county, kind=kind, ind=ind, naics22=ind[0], naics17=ind[1], noun=ind[2],
                 wage=ind[3], tenure=ind[4], seasonal=False, minority=False, zip_county=county, displaced=False,
                 relet_adj=False, final_pay=False, left_open=False, never=False, **kw)
        if a.business is None:
            a.business = self.next_business
            self.next_business += 1
        self.accts.append(a)
        return a

    def place(self, a, addr=None):
        a.addr = addr or self.address(a.county)
        a.zip, a.town = a.addr["zip"], a.addr["town"]

    # ------------------------------------------------------------------ planning
    def plan(self):
        rng = self
        self.deaths25 = defaultdict(list)
        for county in W.ORDER:
            y25, y26 = W.Y25[county], W.Y26[county]
            # 2024Q4 deaths and births (texture for the 2024 quarter)
            n_d24, n_b24 = W.Q424[county]
            for _ in range(n_d24):
                a = self.acct(county, "inc", role="d24")
                a.last = self.day_in(D(2024, 10, 14), D(2024, 12, 31))
                self.place(a)
            for _ in range(n_b24):
                a = self.acct(county, "birth", role="b24", year=2024)
                a.first = self.start_day(2024, self.ri(10, 12))
                self.place(a)
            # 2025 incumbent deaths
            for _ in range(y25["D"]):
                a = self.acct(county, "inc", role="d25")
                if self.r() < 0.3:
                    y, q = 2025, self.ri(1, 4)
                    a.last = qend(y, q) - dt.timedelta(days=self.ri(0, 9))
                    a.final_pay = True
                else:
                    a.last = self.day_in(D(2025, 1, 12), D(2025, 12, 31))
                self.place(a)
                self.deaths25[county].append(a)
            # summer employers and dormant accounts
            for i in range(y25["S"]):
                srow = self.choice(W.SEASONAL_INDUSTRIES)
                a = self.acct(county, "seasonal", ind=(srow[0], srow[1], srow[2], srow[3], 4, "micro"), role="seasonal")
                a.seasonal = True
                a.seasons = [2025] if i < y25["Sx"] else [2025, 2026]
                a.caretaker = 2026 in a.seasons and bool(self.crng.random() < W.CARETAKER)
                self.place(a)
            for _ in range(y25["Dr"]):
                a = self.acct(county, "dormant", role="dormant")
                a.first = self.start_day(2025, self.ri(2, 8))
                self.place(a)
            # 2025 births
            for i in range(y25["T"]):
                a = self.acct(county, "birth", year=2025, role="b25")
                a.first = self.start_day(2025, int(self.rng.choice(12, p=self._month_p())) + 1)
                if self.r() < W.SHORT_LIVED_25 and a.first < D(2025, 9, 1):
                    a.last = self.day_in(a.first + dt.timedelta(days=75), D(2025, 12, 31))
                if i < y25["R"]:
                    a.role = "relet25"
                self.place(a)
            # 2025 continuations
            for kind, n in (("filed", y25["F"]), ("same", y25["U"]), ("moved", y25["Um"])):
                for _ in range(n):
                    self.continuation(county, county, kind, self.choice([qstart(2025, q) for q in (1, 2, 3, 4)]))
            # 2026 births (re-lets planned below for Quarrin's downtown)
            births26 = []
            for i in range(y26["T"]):
                a = self.acct(county, "birth", year=2026, role="b26")
                a.first = self.start_day(2026, int(self.rng.choice(12, p=self._month_p())) + 1)
                births26.append(a)
            self.births26 = getattr(self, "births26", {})
            self.births26[county] = births26
            # 2026 filed and same-address continuations (Caldmere's stores apart)
            n_same = y26["Us"] - (W.CHAIN if county == "Caldmere" else 0) - (1 if county in W.RESOLD_2026 else 0)
            for kind, n in (("filed", y26["F"]), ("same", n_same)):
                for _ in range(n):
                    self.continuation(county, county, kind, self.choice([qstart(2026, q) for q in (1, 2, 3, 4)]))
            for _ in range(W.NEVER_EMPLOYED_2026[county]):
                a = self.acct(county, "never", role="never", year=2026)
                a.never = True
                self.place(a)
        # Caldmere's stores, Tolbeck's park and the other moves
        fuel = [r for r in W.INDUSTRIES if r[0] in ("457110", "445131")]
        for i in range(W.CHAIN):
            ind = fuel[0] if i < 15 else fuel[1]
            self.continuation("Caldmere", "Caldmere", "chain", D(2026, 4, 1), ind=ind, store=i)
        park_inds = [r for r in W.INDUSTRIES if r[0] in ("332710", "332322", "337110", "238220", "238210", "423830",
                                                         "484121", "811310", "424410", "236118")]
        k = 0
        for src_county, n in W.PARK_FROM.items():
            for _ in range(n):
                q = W.PARK_QUARTERS[k]
                k += 1
                self.continuation("Tolbeck", src_county, "park", qstart(2026, q), ind=self.choice(park_inds), park_no=k)
        for dst, src in W.MOVED_OTHER:
            self.continuation(dst, src, "moved", self.choice([qstart(2026, q) for q in (1, 2, 3)]))
        # 2026 births that changed hands within the year
        for county in W.RESOLD_2026:
            b = next(a for a in self.births26[county] if a.role == "b26")
            b.role = "resold"
            b.first = self.start_day(2026, self.ri(1, 2))
            b.size = max(6, self.size("birth", lo=6, hi=14))
            self.continuation(county, county, "resold", D(2026, 7, 1), src=b)
        self.plan_relets()
        for county in W.ORDER:
            for a in self.births26[county]:
                if a.addr is None:
                    self.place(a)
        self.calibrate()
        self.deaths26()
        self.border()
        self.dates_and_names()
        self.nudge()
        self.restructure()

    def nudge(self):
        """A few more closures, drawn from their own stream so nothing planned before them moves."""
        keep = self.rng
        self.rng = np.random.default_rng(W.SEED + 99)
        nm_rng = self.namer.rng
        self.namer.rng = np.random.default_rng(W.SEED + 98)
        for county in W.ORDER:
            x, y = W.NUDGE[county]
            for k in range(x + y):
                a = self.acct(county, "inc", role="d24" if k < x else "d25")
                a.last = (self.day_in(D(2024, 10, 14), D(2024, 12, 31)) if k < x
                          else self.day_in(D(2025, 1, 14), D(2025, 9, 30)))
                self.place(a)
                prof = a.ind[5] if len(a.ind) > 5 else "micro"
                a.size = self.size(prof)
                y0 = int(self.rng.choice(np.arange(1988, 2025), p=self._age_p()))
                a.liab = min(D(y0, self.ri(1, 12), self.ri(1, 28)), D(2024, 6, 28))
                a.reg = a.liab - dt.timedelta(days=self.ri(0, 45))
                a.fein = self.fein()
                a.inact = a.last + dt.timedelta(days=self.ri(20, 210))
                a.legal, a.trade = self.namer.business(a.noun, a.county, a.town)
                if k >= x:
                    self.deaths25[county].append(a)
        self.rng = keep
        self.namer.rng = nm_rng

    def _month_p(self):
        p = np.array([1.05, 1.0, 1.15, 1.2, 1.15, 1.05, 0.95, 0.95, 0.9, 0.9, 0.85, 0.85])
        return p / p.sum()

    # ------------------------------------------------------------------ restructuring, on its own stream
    def restructure(self):
        """What the workforce does around a change of account beyond a plain take-over, drawn from its own random
        stream after everything planned so the planned counts and bases stand: take-overs dated in the first days of a
        quarter; expansions (the new owner hiring from the first day, the old staff a minority of the new payroll);
        large closures and the new businesses their former workers started; 2025 closures whose staff an established
        employer took on; 2025 take-overs changing hands inside a quarter; 2025 mergers; winter pauses."""
        keep, keep_nm = self.rng, self.namer.rng
        self.rng = np.random.default_rng(W.SEED + 77)
        self.namer.rng = np.random.default_rng(W.SEED + 78)
        A = self.accts
        succs = [a for a in A if a.kind == "succ"]
        # old tenants of re-let premises carried four workers or more
        for a in A:
            if a.role in ("old_tenant", "old_tenant26", "old_tenant25") and a.size < 4:
                a.size = self.ri(4, 9)
        # 1. take-over dates in the first days of the quarter's first month
        for a in succs:
            if a.first.day == 1 and a.first.month in (1, 4, 7, 10) and a.succ_type != "resold":
                self._move_start(a, a.first + dt.timedelta(days=self.ri(0, 6 if a.succ_type == "chain" else 10)))
        used = set()
        # 2. expansions
        for key, n in W.EXPAND26.items():
            if key in ("chain", "park"):
                pool = [a for a in succs if a.succ_type == key]
            else:
                pool = [a for a in succs if a.county == key and a.year == 2026 and a.succ_type in ("same", "moved")]
            for a in self._pick(pool, n):
                a.expand = float(self.rng.uniform(*W.EXPAND_RATIO.get(key, W.EXPAND_RATIO["default"])))
                used.add(a.idx)
        for county, n in W.EXPAND25.items():
            pool = [a for a in succs if a.county == county and a.year == 2025 and a.succ_type in ("same", "moved")]
            for a in self._pick(pool, n):
                a.expand = float(self.rng.uniform(*W.EXPAND_RATIO["default"]))
                used.add(a.idx)
        # 3. 2025 take-overs changing hands inside a quarter
        for county, n in W.HANDOVER25.items():
            pool = [a for a in succs if a.county == county and a.year == 2025 and a.succ_type in ("same", "moved")
                    and a.idx not in used]
            for a in self._pick(pool, n):
                q = qof(a.first)[1] if qof(a.first)[1] <= 3 else self.ri(1, 3)
                mo = 3 * (q - 1) + self.ri(1, 2)
                last = self.day_in(D(2025, mo, 12), D(2025, mo + 1, 11))
                self._move_start(a, last + DAY)
                a.handover = True
                used.add(a.idx)
        # 4. 2025 mergers: a second closing business of the same trade joins a take-over
        for county in W.MERGE25:
            pool = [a for a in succs if a.county == county and a.year == 2025 and a.succ_type in ("same", "moved")
                    and a.idx not in used and a.first <= D(2025, 9, 30)]
            for a in self._pick(pool, 1):
                src = A[a.source]
                cands = [x for x in self.deaths25[county] if x.role == "d25" and not x.minority and x.successor is None
                         and x.last < D(2025, 10, 12)]
                x = self._pick(cands, 1)[0]
                self.set_ind(x, src.ind)
                x.size = max(6, int(round(src.size * float(self.rng.uniform(0.7, 1.25)))))
                self._retime_end(x, a.first - DAY)
                x.merged_into = a.idx
                x.role = "merged"
                x.final_pay = False
                x.legal, x.trade = self.namer.business(x.noun, x.county, x.town)
                used.add(a.idx)
        # 5. large closures and the new businesses their former workers started
        taken = set()
        for county, naics, size, last, n, (sy, sq) in W.LAYOFFS:
            in25 = last >= D(2025, 10, 12)
            if last.year == 2025:
                cands = [x for x in self.deaths25[county] if x.role == "d25" and not x.minority and x.successor is None
                         and x.merged_into is None and qof(x.last) == qof(last)
                         and (x.last >= D(2025, 10, 12)) == in25]
            else:
                cands = [x for x in A if x.county == county and x.role == "d26" and x.last is not None
                         and x.last.year == 2026]
            x = self._pick(cands, 1)[0]
            self.set_ind(x, self.ind_row(naics))
            x.size = size
            self._retime_end(x, last)
            x.final_pay = False
            x.layoff = (n, (sy, sq))
            x.role = "layoff" if x.role == "d25" else x.role
            x.legal, x.trade = self.namer.business(x.noun, x.county, x.town)
            taken.add(x.idx)
            pool = [b for b in A if b.kind == "birth" and b.year == sy and b.county == county and b.role in ("b25", "b26")
                    and not b.minority and b.last is None and b.relet_of is None and qof(b.first) == (sy, sq)]
            picks = self._pick(pool, min(n, len(pool)))
            if len(picks) < n:
                more = [b for b in A if b.kind == "birth" and b.year == sy and b.county == county
                        and b.role in ("b25", "b26") and not b.minority and b.last is None and b.relet_of is None
                        and b not in picks and qof(b.first) != (sy, sq) and qof(b.first)[1] in (sq - 1, sq + 1)]
                for b in self._pick(more, n - len(picks)):
                    self._move_birth(b, self.start_day(sy, 3 * (sq - 1) + self.ri(1, 3)))
                    picks.append(b)
            for b in picks:
                b.spinout_of = x.idx
                b.size = self.ri(3, 6)
                self.set_ind(b, self.ind_row(self.choice(W.SPINOUT_TRADES[naics])))
                b.legal, b.trade = self.namer.business(b.noun, b.county, b.town)
        # 6. 2025 closures whose staff an established employer took on
        buyers = set()
        for county, n in W.ABSORB25.items():
            cands = [x for x in self.deaths25[county] if x.role == "d25" and not x.minority and x.successor is None
                     and x.merged_into is None and x.idx not in taken and D(2025, 1, 20) <= x.last <= D(2025, 12, 5)]
            pref = [x for x in cands if x.ind[0] in W.ABSORB_TRADES]
            picks = self._pick(pref, min(n, len(pref)))
            picks += self._pick([x for x in cands if x not in picks], n - len(picks))
            for x in picks:
                if x.ind[0] not in W.ABSORB_TRADES:
                    self.set_ind(x, self.ind_row(self.choice(W.ABSORB_TRADES)))
                x.size = max(x.size or 0, self.ri(6, 13))
                x.final_pay = False
                plain = [p for p in A if p.county == county and p.role == "plain" and p.last is None
                         and p.idx not in buyers and p.pause is None]
                same = [p for p in plain if p.naics22 == x.naics22 and (p.size or 0) >= x.size]
                if same:
                    buyer = self._pick(same, 1)[0]
                else:
                    big = [p for p in plain if (p.size or 0) >= x.size + 2] or plain
                    buyer = self._pick(big, 1)[0]
                    self.set_ind(buyer, x.ind)
                    buyer.legal, buyer.trade = self.namer.business(buyer.noun, buyer.county, buyer.town)
                buyers.add(buyer.idx)
                x.absorbed_by = buyer.idx
                x.role = "absorbed"
                x.legal, x.trade = self.namer.business(x.noun, x.county, x.town)
                taken.add(x.idx)
        # 7. winter pauses
        for county, n in W.PAUSE.items():
            pool = [p for p in A if p.county == county and p.role == "plain" and p.last is None and p.idx not in buyers
                    and p.pause is None and (p.size or 0) >= 2]
            for p in self._pick(pool, n):
                p.pause = (self.day_in(D(2025, 10, 14), D(2025, 11, 28)), self.day_in(D(2026, 1, 19), D(2026, 3, 27)))
        self.rng, self.namer.rng = keep, keep_nm

    def ind_row(self, code):
        return next(r for r in W.INDUSTRIES if r[0] == code)

    def _pick(self, pool, n):
        if n <= 0 or not pool:
            return []
        idx = sorted(self.rng.choice(len(pool), size=min(n, len(pool)), replace=False).tolist())
        return [pool[i] for i in idx]

    def _move_start(self, a, first):
        """Move a successor's first day and its source's last day, keeping the register's offsets."""
        src = self.accts[a.source]
        d_liab, d_reg = (a.liab - a.first).days, (a.reg - a.first).days
        a.first = first
        a.liab = first + dt.timedelta(days=d_liab)
        a.reg = first + dt.timedelta(days=d_reg)
        if a.year == 2026:
            a.reg = max(a.reg, D(2026, 1, 2))
        self._retime_end(src, first - DAY)

    def _retime_end(self, x, last):
        old = x.last
        x.last = last
        if x.inact is not None:
            x.inact = x.inact + (last - old)

    def _move_birth(self, b, first):
        d_liab, d_reg = (b.liab - b.first).days, (b.reg - b.first).days
        b.first = first
        b.liab = first + dt.timedelta(days=d_liab)
        b.reg = first + dt.timedelta(days=d_reg)
        if b.year == 2026:
            b.reg = min(max(b.reg, D(2026, 1, 2)), b.first)

    def continuation(self, county, src_county, kind, start, ind=None, src=None, **extra):
        """A business going on under a new account from `start`: its source account (an incumbent created here,
        or `src`) stops the day before; the successor gets most of its staff."""
        if src is None:
            ind = ind or self.industry(src_county)
            lo = 6 if kind in ("same", "moved", "park", "chain") else 1
            hi = 14 if kind == "chain" else 45 if kind == "park" else 400
            src = self.acct(src_county, "inc", ind=ind, role="src_" + kind)
            src.size = self.size(ind[5] if kind != "chain" else "small", lo=lo, hi=hi)
            self.place(src, self.address(src_county, street=("Highway", "Highway", "HWY")
                                         if kind == "chain" and self.r() < 0.4 else None))
        src.last = start - DAY
        ind = ind or src.ind
        succ = self.acct(county, "succ", ind=ind, year=start.year, first=start, source=src.idx, succ_type=kind,
                         business=src.business, role="succ_" + kind)
        src.successor = succ.idx
        succ.size = max(src.size or 1, 1)
        if kind in ("filed", "same", "chain", "resold"):
            succ.addr = dict(src.addr) if src.addr else None
            if succ.addr is None:
                self.place(src)
                succ.addr = dict(src.addr)
            succ.zip, succ.town = succ.addr["zip"], succ.addr["town"]
        elif kind == "park":
            num = 100 + 20 * extra["park_no"] + self.ri(0, 9)
            succ.addr = {"zip": "56871", "town": "Tolbeck", "num": num, "dirn": None, "street": W.PARK_STREET[0],
                         "stype": (W.PARK_STREET[1], W.PARK_STREET[2]), "suite": None}
            self.addr_used.add(("56871", num, "", W.PARK_STREET[0], W.PARK_STREET[2], ""))
            succ.zip, succ.town = "56871", "Tolbeck"
        else:
            self.place(succ)
        if kind == "chain":
            src.role, succ.role = "chain_src", "chain"
        if kind == "chain" or (kind == "park" and self.r() < 0.62):
            alt = W.ALT_CODE.get(ind[0])
            if alt:
                succ.naics22 = succ.naics17 = alt
        return succ

    def plan_relets(self):
        """New businesses in premises a closed business left: Quarrin's downtown program and a few elsewhere. The
        old tenants are the county's 2025 or 2026 closures; an adjacent re-let opens the quarter after its old
        tenant's last payroll and is in a different line of business; the others follow a vacancy of two quarters
        or more."""
        plan = {"Quarrin": [(1, 3, 4), (2, 3, 4), (3, 3, 3), (4, 2, 2)]}
        self.relet_pairs = []
        for county in W.ORDER:
            y26 = W.Y26[county]
            spec = plan.get(county)
            if spec is None:
                adj = y26["Radj"]
                gap = y26["R"] - adj
                spec = [(self.ri(2, 4), 1, 0) for _ in range(adj)] + [(self.ri(1, 4), 0, 1) for _ in range(gap)]
            births = [a for a in self.births26[county] if a.role == "b26"]
            bi = 0
            for q, n_adj, n_gap in spec:
                for j in range(n_adj + n_gap):
                    b = births[bi]
                    bi += 1
                    b.role = "relet"
                    self.set_ind(b, self.industry(county, pool=W.STOREFRONT))
                    b.first = self.start_day(2026, 3 * (q - 1) + self.ri(1, 3))
                    b.relet_adj = j < n_adj
                    if b.relet_adj:
                        oy, oq = prevq(2026, q)
                        old_last = self.day_in(qstart(oy, oq) + dt.timedelta(days=12), qend(oy, oq))
                    else:
                        # a vacancy of two quarters or more: the old tenant's last payroll at least two quarters back
                        hi_q = prevq(*prevq(2026, q))
                        cands = [(y, qq) for (y, qq) in W.QUARTERS[1:] if (y, qq) <= hi_q]
                        oy, oq = self.choice(cands)
                        old_last = self.day_in(qstart(oy, oq) + dt.timedelta(days=12), qend(oy, oq))
                    street = None
                    if county in W.DOWNTOWN:
                        street = self.choice(W.DOWNTOWN[county])
                    if old_last.year == 2025:
                        old = self.acct(county, "inc", role="old_tenant")
                        old.last = old_last
                        self.deaths25[county].append(old)
                    else:
                        old = self.acct(county, "inc", role="old_tenant26")
                        old.last = old_last
                    old.size = self.size("small", lo=3, hi=12)
                    self.set_ind(old, self.industry(county, pool=W.STOREFRONT))
                    if b.relet_adj:
                        # a different line of business from the old tenant's
                        while old.ind[0][:3] == b.ind[0][:3]:
                            self.set_ind(old, self.industry(county, pool=W.STOREFRONT))
                    elif self.r() < 0.5:
                        self.set_ind(old, b.ind)
                    seat = next(c for c in W.COUNTIES if c[1] == county)[3][0]
                    self.place(old, self.address(county, zip_town=seat if street else None, street=street))
                    b.addr = dict(old.addr)
                    b.zip, b.town = b.addr["zip"], b.addr["town"]
                    b.relet_of = old.idx
                    self.relet_pairs.append((b.idx, old.idx))
        # 2025 re-lets: old tenants among the 2024Q4 and early 2025 closures
        for county in W.ORDER:
            for b in [a for a in self.accts if a.county == county and a.role == "relet25"]:
                b.first = max(b.first, D(2025, 4, 2))
                if b.first.day > 12:
                    b.first = b.first.replace(day=12)
                old = self.acct(county, "inc", role="old_tenant25")
                old.last = self.day_in(D(2024, 10, 14), D(2024, 12, 31))
                old.size = self.size("small", lo=2, hi=10)
                self.place(old)
                b.addr = dict(old.addr)
                b.zip, b.town = b.addr["zip"], b.addr["town"]
                b.relet_of = old.idx
                b.role = "relet25"

    def set_ind(self, a, ind):
        a.ind = ind
        a.naics22, a.naics17, a.noun, a.wage, a.tenure = ind[0], ind[1], ind[2], ind[3], ind[4]

    def in_base25(self, a):
        """Employment on the 12th of October, November or December 2025."""
        if a.kind == "seasonal":
            return bool(a.caretaker)
        if a.never:
            return False
        first = a.first or D(2024, 1, 1)
        last = a.last or D(2027, 1, 1)
        return any(first <= t <= last for t in (D(2025, 10, 12), D(2025, 11, 12), D(2025, 12, 12)))

    def calibrate(self):
        """Fill each county with the incumbents that operate through 2025 so its 2025Q4 base is the planned count."""
        self.plain = defaultdict(list)
        for county in W.ORDER:
            have = sum(1 for a in self.accts if a.county == county and self.in_base25(a))
            need = W.Y26[county]["B"] - have
            assert need > 0, (county, need)
            for _ in range(need):
                a = self.acct(county, "inc", role="plain")
                self.place(a)
                self.plain[county].append(a)

    def deaths26(self):
        """2026 closures: the old tenants planned with the re-lets, then births and plain incumbents."""
        for county in W.ORDER:
            n = W.D26[county] - sum(1 for a in self.accts if a.county == county and a.role == "old_tenant26")
            b25 = [a for a in self.accts if a.county == county and a.role in ("b25", "relet25") and a.last is None
                   and a.successor is None]
            b26 = [a for a in self.births26[county] if a.role == "b26" and a.last is None]
            pool = list(self.plain[county])
            k25 = int(round(W.CLOSE_26_OF_25 * len(b25)))
            k26 = int(round(W.CLOSE_26_OF_26 * len(b26)))
            picks = [b25[i] for i in self.rng.choice(len(b25), size=k25, replace=False)]
            picks += [b26[i] for i in self.rng.choice(len(b26), size=k26, replace=False)]
            rest = n - len(picks)
            picks += [pool[i] for i in self.rng.choice(len(pool), size=rest, replace=False)]
            for a in picks:
                lo = max(D(2026, 1, 12), (a.first or D(2026, 1, 1)) + dt.timedelta(days=60))
                if lo > D(2026, 12, 20):
                    continue
                if self.r() < 0.3:
                    q = self.ri(qof(lo)[1], 4)
                    a.last = max(lo, qend(2026, q) - dt.timedelta(days=self.ri(0, 9)))
                    a.final_pay = a.last < D(2026, 12, 20)
                else:
                    a.last = self.day_in(lo, D(2026, 12, 31))
                if a.role == "plain":
                    a.role = "d26"

    def border(self):
        """Worksites in the minority part of a ZIP code that crosses a county line: the ZIP's own county is not the
        county the worksite lies in. Among them: incumbents in the 2024Q4 base (some closing in the first half of
        2025) and 2025 births opening in the first half of the year."""
        for z, zip_county, minority, m in W.BORDER:
            town = next(t for c in W.COUNTIES for zz, t in c[3] if zz == z)
            kd = W.BORDER_DEATHS[z]
            dead = [a for a in self.deaths25[minority] if a.role == "d25" and a.successor is None and not a.minority
                    and D(2025, 1, 14) <= a.last <= D(2025, 6, 30)]
            cands = [a for a in self.accts if a.county == minority and a.kind == "inc" and a.role in ("plain", "d26")
                     and a.successor is None and not a.minority]
            pick = [dead[i] for i in sorted(self.rng.choice(len(dead), size=kd, replace=False))]
            pick += [cands[i] for i in sorted(self.rng.choice(len(cands), size=m - kd, replace=False))]
            births = [a for a in self.accts if a.county == minority and a.kind == "birth" and a.year == 2025
                      and a.role == "b25" and not a.minority and a.first < D(2025, 7, 1) and a.last is None]
            kb = W.BORDER_BIRTHS[z]
            pick += [births[i] for i in sorted(self.rng.choice(len(births), size=kb, replace=False))]
            for a in pick:
                a.minority = True
                a.zip_county = zip_county
                a.addr = self.address(minority, zip_town=(z, town))
                a.zip, a.town = z, town

    def dates_and_names(self):
        for a in self.accts:
            if a.size is None:
                prof = "birth" if a.kind in ("birth", "dormant") else (a.ind[5] if len(a.ind) > 5 else "micro")
                a.size = self.size(prof)
                if a.kind == "seasonal":
                    a.size = self.ri(3, 16)
            # registration and liability
            if a.kind in ("inc", "seasonal", "dormant"):
                y = int(self.rng.choice(np.arange(1988, 2025), p=self._age_p()))
                liab = D(y, self.ri(1, 12), self.ri(1, 28))
                if liab > D(2024, 6, 30):
                    liab = D(2024, 6, self.ri(1, 28))
                if a.kind == "seasonal":
                    liab = liab.replace(month=self.ri(5, 6))
                a.liab = liab
                a.reg = liab - dt.timedelta(days=self.ri(0, 45))
            elif a.kind == "never":
                a.reg = self.day_in(D(2026, 1, 5), D(2026, 11, 30))
                a.liab = None
            else:
                a.liab = a.first + dt.timedelta(days=self.ri(4, 13))
                if a.kind == "succ":
                    if a.first.year == 2026 and a.first.month == 1:
                        a.reg = a.first + dt.timedelta(days=self.ri(1, 19))
                    else:
                        a.reg = a.first - dt.timedelta(days=self.ri(3, 25))
                elif a.year == 2026:
                    a.reg = max(D(2026, 1, 2), a.first - dt.timedelta(days=self.ri(2, 45)))
                    a.reg = min(a.reg, a.first)
                else:
                    a.reg = a.first - dt.timedelta(days=self.ri(2, 45))
                    if a.year == 2025 and a.first.month == 1 and self.r() < 0.45:
                        a.reg = D(2024, self.ri(10, 12), self.ri(1, 28))
            a.fein = self.fein()
        # inactivation
        for a in self.accts:
            if a.successor is not None:
                succ = self.accts[a.successor]
                if succ.succ_type == "filed":
                    a.inact = a.last
                else:
                    a.inact = a.last + dt.timedelta(days=self.ri(20, 150))
            elif a.kind == "seasonal" and 2026 not in a.seasons:
                a.inact = D(2025, 9, 30) + dt.timedelta(days=self.ri(40, 200))
            elif a.last is not None:
                if self.r() < 0.08:
                    a.left_open = True
                else:
                    a.inact = a.last + dt.timedelta(days=self.ri(20, 210))
            elif a.never and self.r() < 0.3:
                a.inact = a.reg + dt.timedelta(days=self.ri(120, 300))
        self.names()

    def _age_p(self):
        ages = np.arange(1988, 2025)
        p = np.exp((ages - 2024) / 9.0)
        return p / p.sum()

    def names(self):
        nm = self.namer
        for a in self.accts:
            if a.kind == "succ":
                continue
            if a.role == "chain_src":
                a.trade = "Halvard Fuel Stop #%d" % (11 + 2 * self._chain_no(a))
                a.legal = "Halvard Stations %d LLC" % (11 + 2 * self._chain_no(a))
                nm.legal.add(a.legal)
                continue
            a.legal, a.trade = nm.business(a.noun, a.county, a.town)
        for a in self.accts:
            if a.kind != "succ":
                continue
            src = self.accts[a.source]
            t = a.succ_type
            if t == "chain":
                no = 301 + self._chain_no(src)
                a.trade = "Pellworth Market %d" % no
                a.legal = "Pellworth Caldmere %d LLC" % no
                nm.legal.add(a.legal)
            elif t == "park":
                if self.r() < 0.16:
                    a.trade = src.trade.split(" of ")[0]
                    a.legal = "%s of Tolbeck LLC" % a.trade.replace("'s ", " ")
                    nm.legal.add(a.legal)
                else:
                    a.legal, a.trade = nm.business(a.noun, "Tolbeck", "Tolbeck",
                                                   style="place" if self.r() < 0.6 else "surname")
            elif t in ("filed", "resold"):
                a.trade = src.trade if self.r() < 0.75 else nm.business(a.noun, a.county, a.town)[1]
                a.legal = nm.legal_for(a.trade)
            elif t == "same":
                if self.r() < 0.6:
                    a.trade = src.trade
                    a.legal = nm.legal_for(a.trade)
                else:
                    a.legal, a.trade = nm.business(a.noun, a.county, a.town)
            else:
                a.legal, a.trade = nm.business(a.noun, a.county, a.town)

    def _chain_no(self, src):
        if not hasattr(self, "_chain_order"):
            self._chain_order = [a.idx for a in self.accts if a.role == "chain_src"]
        return self._chain_order.index(src.idx)


# ---------------------------------------------------------------------- workers
class Spells:
    """Columns of every spell of employment: account, start, end (inclusive), monthly wage, the spell it continues
    (the same worker's previous spell, or -1) and whether it is reserved for a planned continuation."""

    def __init__(self):
        self.acct, self.start, self.end, self.wage, self.prev, self.kind = [], [], [], [], [], []

    def add(self, acct, start, end, wage, kind, prev=-1):
        self.acct.append(acct)
        self.start.append(start)
        self.end.append(end)
        self.wage.append(wage)
        self.prev.append(prev)
        self.kind.append(kind)
        return len(self.acct) - 1


def staff(world):
    """Every account's spells. Positions are held continuously: a leaver is replaced the next day. An account whose
    business goes on elsewhere keeps its staff through its last two quarters; the workers who move stay at the new
    payroll through the quarter after they arrive."""
    rng = world.rng
    prng = np.random.default_rng(W.SEED + 85)       # pauses and caretakers
    S = Spells()
    by_acct = defaultdict(list)
    win1 = W.WIN1
    pre = D(2024, 9, 30)

    def wage_of(a):
        return float(a.wage) * float(np.exp(rng.normal(0.0, 0.33)))

    def duration(a):
        return dt.timedelta(days=max(14, int(rng.exponential(a.tenure * 30.4))))

    def run_position(a, start, end, first_kind="hire", prev=-1, hold_until=None, hold_to=None):
        """One position from `start` to `end`: successive spells, the first continuing `prev` if given. Returns the
        last spell."""
        s = start
        kind = first_kind
        i = -1
        while s <= end:
            e = s + duration(a)
            if hold_until is not None and kind == first_kind and e < hold_until:
                e = hold_until
            if hold_to is not None and e >= hold_to[0] and e < hold_to[1]:
                e = hold_to[1]
            e = min(e, end)
            i = S.add(a.idx, s, e, wage_of(a), kind, prev)
            by_acct[a.idx].append(i)
            prev = -1
            kind = "hire"
            s = e + DAY
        return i

    def hold_of(a, last):
        ly, lq = qof(last)
        if a.successor is not None or a.absorbed_by is not None or a.merged_into is not None:
            return (qstart(*prevq(ly, lq)), last)
        if a.layoff is not None:
            return (qstart(ly, lq), last)
        return None

    for a in world.accts:
        if a.never:
            continue
        last = a.last or win1
        hold = hold_of(a, last) if a.last is not None else None
        if a.kind == "seasonal":
            for y in a.seasons:
                m0, m1 = W.SEASON[a.ind[0]]
                s0 = D(y, m0, world.ri(1, 10))
                e0 = D(y, m1, world.ri(15, 30))
                for _ in range(a.size):
                    i = S.add(a.idx, s0 + dt.timedelta(days=world.ri(0, 6)), e0 - dt.timedelta(days=world.ri(0, 5)),
                              wage_of(a), "season%d" % y)
                    by_acct[a.idx].append(i)
            if a.caretaker:
                run_position(a, pre - dt.timedelta(days=int(prng.integers(200, 3000))), win1, first_kind="initial")
            continue
        if a.kind == "inc":
            for k in range(a.size):
                tenure_start = pre - dt.timedelta(days=int(rng.exponential(a.tenure * 30.4)))
                end = last
                if k > 0 and a.role == "plain" and a.size > 2 and rng.random() < W.CONTRACT / max(1, a.size // 4):
                    end = min(last, D(2025, 1, 1) + dt.timedelta(days=int(rng.integers(0, 700))))
                if a.pause is not None and end >= a.pause[0]:
                    p0, p1 = a.pause
                    i = run_position(a, tenure_start, p0 - DAY, first_kind="initial")
                    if prng.random() < 0.8:
                        run_position(a, p1, end, first_kind="return", prev=i)
                    else:
                        run_position(a, p1 + dt.timedelta(days=int(prng.integers(0, 15))), end)
                    continue
                run_position(a, tenure_start, end, first_kind="initial", hold_to=hold)
            if a.role == "plain" and rng.random() < W.EXPAND:
                for _ in range(max(1, int(round(a.size * rng.uniform(0.08, 0.35))))):
                    s = D(2025, 1, 2) + dt.timedelta(days=int(rng.integers(0, 690)))
                    if s < last and not (a.pause is not None and a.pause[0] - dt.timedelta(days=30) <= s <= a.pause[1]):
                        run_position(a, s, last)
        elif a.kind == "dormant":
            for _ in range(a.size):
                run_position(a, a.first, last, first_kind="initial")
        elif a.kind == "birth":
            n1 = a.size
            for k in range(n1):
                s = a.first if k < max(1, int(round(0.7 * n1))) else a.first + dt.timedelta(days=world.ri(10, 70))
                if a.spinout_of is not None:
                    s = a.first + dt.timedelta(days=world.ri(0, 12) if k else 0)
                if s > last:
                    s = a.first
                run_position(a, s, last, first_kind="initial", hold_to=hold,
                             hold_until=qend(*qof(a.first)) if a.spinout_of is not None else None)
            if a.year in (2025, 2026) and rng.random() < 0.35 and a.first + dt.timedelta(days=150) < last:
                for _ in range(max(1, int(round(n1 * rng.uniform(0.15, 0.5))))):
                    run_position(a, a.first + dt.timedelta(days=world.ri(120, 300)), last, hold_to=hold)
        elif a.kind == "succ":
            pass   # filled after the sources' staff exist
    # successors: movers from the source's staff (and a merging business's) on its last day, then the new owner's hires
    merging = defaultdict(list)
    for x in world.accts:
        if x.merged_into is not None:
            merging[x.merged_into].append(x)
    for a in sorted((x for x in world.accts if x.kind == "succ"), key=lambda x: x.first):
        movers = []
        for src in [world.accts[a.source]] + merging.get(a.idx, []):
            on_last = [i for i in by_acct[src.idx] if S.end[i] == src.last]
            frac = float(rng.uniform(0.88, 1.0))
            movers += [on_last[i] for i in sorted(rng.choice(len(on_last), size=max(1, int(round(frac * len(on_last)))),
                                                              replace=False))] if on_last else []
        last = a.last or win1
        hold = hold_of(a, last) if a.last is not None else None
        fy, fq = qof(a.first)
        keep_to = qend(*nextq(fy, fq)) if (a.handover or merging.get(a.idx)) else qend(fy, fq)
        for i in movers:
            run_position(a, a.first, last, first_kind="mover", prev=i, hold_until=keep_to, hold_to=hold)
        if a.expand:
            for _ in range(int(round(a.expand * len(movers)))):
                run_position(a, a.first + dt.timedelta(days=world.ri(0, 14)), last, hold_to=hold,
                             hold_until=qend(fy, fq))
        else:
            extra = min(max(0, a.size - len(movers)), int(len(movers) * 0.12))
            for _ in range(extra):
                run_position(a, a.first + dt.timedelta(days=world.ri(0, 40)), last, hold_to=hold)
    # businesses an established employer took on: the staff on the last day move to the buyer's payroll
    for x in world.accts:
        if x.absorbed_by is None:
            continue
        buyer = world.accts[x.absorbed_by]
        on_last = [i for i in by_acct[x.idx] if S.end[i] == x.last]
        frac = float(rng.uniform(0.88, 1.0))
        movers = [on_last[i] for i in sorted(rng.choice(len(on_last), size=max(1, int(round(frac * len(on_last)))),
                                                         replace=False))]
        start = x.last + DAY
        for i in movers:
            run_position(buyer, start, buyer.last or win1, first_kind="mover", prev=i,
                         hold_until=qend(*nextq(*qof(start))))
    world.by_acct = by_acct
    return S


def link(world, S):
    """Give hires their workers: a mover continues the source spell; a returning summer worker continues last
    summer's spell; a birth's first-quarter hires come from no covered job, from one other account at most once each,
    one from the closed account for a re-let or a hire displaced by a closure, or (a business started by a closed
    payroll's former workers) mostly from that payroll; other hires take a worker who left another account in the past
    sixty days or a new entrant. A closed business's workers never land two at one account, and the workers of a
    closure of two or fewer take no covered job in its last two quarters or the next."""
    rng = world.rng
    A = world.accts
    n = len(S.acct)
    starts = np.array([s.toordinal() for s in S.start])
    ends = np.array([e.toordinal() for e in S.end])
    nxt = np.full(n, -1)
    reserved = np.zeros(n, dtype=bool)
    for i in range(n):
        p = S.prev[i]
        if p >= 0:
            nxt[p] = i
            reserved[p] = True
    # summer staff returning
    for a in A:
        if a.kind == "seasonal" and 2026 in a.seasons:
            s25 = [i for i in world.by_acct[a.idx] if S.kind[i] == "season2025"]
            s26 = [i for i in world.by_acct[a.idx] if S.kind[i] == "season2026"]
            back = int(round(0.6 * min(len(s25), len(s26))))
            for p, i in zip(s25[:back], s26[:back]):
                S.prev[i] = p
                nxt[p] = i
                reserved[p] = True
    # closures: accounts that stopped employing for good with no business going on
    closing = set()
    for a in A:
        if a.never or not world.by_acct.get(a.idx):
            continue
        ended = a.last is not None or (a.kind == "seasonal" and 2026 not in a.seasons)
        if ended and a.successor is None and a.absorbed_by is None and a.merged_into is None:
            closing.add(a.idx)
    tiny = np.zeros(n, dtype=bool)
    on_last_n = {}
    for c in closing:
        sp = world.by_acct[c]
        lastday = max(S.end[k] for k in sp)
        on_last_n[c] = sum(1 for k in sp if S.end[k] == lastday)
        lq = qof(lastday)
        ly, lm = last_emp_month(lastday)
        quarters = {lq, prevq(*lq), qof(D(ly, lm, 1))}
        cnt = min(sum(1 for k in sp if S.start[k] <= qend(*qq) and S.end[k] >= qstart(*qq)) for qq in quarters)
        if cnt <= 2:
            lo = qstart(*prevq(*lq))
            for k in sp:
                if S.end[k] >= lo:
                    tiny[k] = True
    # pool of spells that ended with no planned successor, by end date
    by_end = defaultdict(list)
    for i in np.argsort(ends, kind="stable"):
        i = int(i)
        if not reserved[i] and ends[i] < W.WIN1.toordinal() and not tiny[i]:
            by_end[ends[i]].append(i)
    taken = reserved.copy()
    acct_last = {a.idx: (a.last or D(2027, 1, 1)).toordinal() for a in A}
    used_pair = set()

    def attach(i, j, recv):
        S.prev[i] = j
        taken[j] = True
        nxt[j] = i
        if S.acct[j] in closing:
            used_pair.add((S.acct[j], recv))

    def free(j, recv):
        return not taken[j] and not tiny[j] and (S.acct[j] not in closing or (S.acct[j], recv) not in used_pair)

    def find(start_ord, pred, window=60, tries=40):
        for _ in range(tries):
            d = start_ord - int(rng.integers(1, window + 1))
            lst = by_end.get(d)
            if not lst:
                continue
            j = lst[int(rng.integers(len(lst)))]
            if not taken[j] and pred(j):
                return j
        return -1

    # births' first quarters
    first_q = {}
    for a in A:
        if a.kind == "birth" and a.year in (2025, 2026):
            first_q[a.idx] = qof(a.first)
    hires = [i for i in range(n) if S.prev[i] < 0 and S.kind[i] in ("initial", "hire") and S.start[i] >= W.WIN0]
    hires.sort(key=lambda i: (starts[i], i))
    closed_by_q = defaultdict(list)       # closures in a quarter by county, four workers or more on the last day
    for c in sorted(closing):
        a = A[c]
        if a.kind in ("inc", "birth") and a.last is not None and on_last_n.get(c, 0) >= 4:
            closed_by_q[(qof(a.last), a.county)].append(c)
    used_src = defaultdict(set)
    special_done = set()
    spun = defaultdict(int)
    for i in hires:
        a = A[S.acct[i]]
        s_ord = starts[i]
        if a.kind == "dormant" and S.kind[i] == "initial":
            continue                                      # a dormant account's staff come back from no covered job
        if a.idx in first_q and qof(S.start[i]) == first_q[a.idx]:
            y, q = first_q[a.idx]
            q0 = qstart(*prevq(y, q)).toordinal()
            n_first = sum(1 for k in world.by_acct[a.idx] if qof(S.start[k]) <= (y, q) and S.kind[k] != "mover")
            if a.spinout_of is not None:
                src = A[a.spinout_of]
                if spun[a.idx] < min(4, max(2, int(np.ceil(0.62 * n_first)))):
                    cands = [k for k in world.by_acct[src.idx] if S.end[k] == src.last and not taken[k]]
                    j = cands[int(rng.integers(len(cands)))]
                    S.prev[i] = j
                    taken[j] = True
                    nxt[j] = i
                    spun[a.idx] += 1
                continue
            if n_first <= 2:
                continue                                  # new entrants only
            if a.idx not in special_done:
                special_done.add(a.idx)
                if a.relet_of is not None:
                    old = A[a.relet_of]
                    cands = [k for k in world.by_acct[old.idx] if S.end[k] == old.last and free(k, a.idx)]
                    if cands:
                        attach(i, cands[int(rng.integers(len(cands)))], a.idx)
                        used_src[a.idx].add(old.idx)
                    continue
                share = W.DISPLACED_HIRE.get(a.county, W.DISPLACED_HIRE["default"])
                if rng.random() < share:
                    closers = [c for c in closed_by_q.get((prevq(y, q), a.county), []) if c not in used_src[a.idx]]
                    rng.shuffle(closers)
                    for c in closers:
                        cands = [k for k in world.by_acct[c] if S.end[k] == A[c].last and free(k, a.idx)]
                        if cands:
                            attach(i, cands[int(rng.integers(len(cands)))], a.idx)
                            used_src[a.idx].add(c)
                            a.displaced = True
                            break
                    if a.displaced:
                        continue
            if rng.random() < 0.35:
                def ok(j, a=a, q0=q0, y=y, q=q):
                    src = S.acct[j]
                    return (src != a.idx and src not in used_src[a.idx] and starts[j] <= q0
                            and acct_last[src] >= qstart(y, q).toordinal() and A[src].kind != "seasonal"
                            and free(j, a.idx))
                j = find(s_ord, ok, window=45)
                if j >= 0:
                    attach(i, j, a.idx)
                    used_src[a.idx].add(S.acct[j])
            continue
        if rng.random() < 0.42:
            j = find(s_ord, lambda j, a=a: S.acct[j] != a.idx and free(j, a.idx))
            if j >= 0:
                attach(i, j, a.idx)
    # workers: follow each chain of spells from its first spell
    gid = np.full(n, -1)
    order = np.argsort(starts, kind="stable")
    w = 0
    for i in order:
        i = int(i)
        p = S.prev[i]
        if p >= 0 and gid[p] >= 0:
            gid[i] = gid[p]
        elif gid[i] < 0:
            gid[i] = w
            w += 1
    S.worker = gid
    S.n_workers = w
    world.closing = closing
    return S


def build():
    world = World()
    world.plan()
    S = staff(world)
    link(world, S)
    return world, S
