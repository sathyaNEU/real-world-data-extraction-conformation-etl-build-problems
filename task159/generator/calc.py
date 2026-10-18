"""task159 calc: the golden and every rival, computed from the shipped pack alone (no world import).

The golden forecasts each watch-list platform's morning peak for an average weekday of the spring 2027 pick the way
transit capacity analysis builds platform loading: the census's flows onto and off every platform, carried to the
spring weekday by the fare export's weekday index and the spring-over-autumn ratio, run train by train through the
spring timetable, each train taking at most the room it has left (its cars at the fleet register's maximum load less
the riders it brings from upstream, plus the riders who get off), the riders it cannot take waiting for the next."""
from __future__ import annotations

import datetime as dt
import math
import os
from collections import defaultdict

import numpy as np
import pandas as pd

F_FARE = "vtc_fare_entries_hourly_2024-06-03_2027-01-10.parquet"
F_CENSUS = "station_census_2026-10.xlsx"
F_COUNTS = "platform_counts_autumn_2026.xlsx"
F_CAP = "platform_capacity_register.csv"
F_TT = "weekday_timetables_aut26_spr27.csv"
F_FLEET = "fleet_register.csv"
F_COMPLEX = "complex_reference.csv"
F_INV = "station_elements_inventory.csv"
F_ASSET = "escalator_asset_register.csv"
F_CTRL = "escalator_controller_log_2026-09-01_2026-12-31.csv"
F_WO = "elevator_work_orders_2026-09-01_2026-12-31.csv"
F_MON = "elevator_monitoring_2026-09-01_2026-12-31.csv"

PICK = (dt.date(2027, 3, 1), dt.date(2027, 6, 25))
AUTUMN = (dt.date(2026, 9, 8), dt.date(2026, 12, 18))
WD = ["Mon", "Tue", "Wed", "Thu", "Fri"]
THRESH = 0.85
# federal holidays and the day after Thanksgiving in the windows the calc reads (the service plans and the calendar)
FEDERAL = {dt.date(2024, 9, 2), dt.date(2024, 10, 14), dt.date(2024, 11, 11), dt.date(2024, 11, 28),
           dt.date(2024, 11, 29), dt.date(2025, 5, 26), dt.date(2025, 6, 19), dt.date(2025, 9, 1),
           dt.date(2025, 10, 13), dt.date(2025, 11, 11), dt.date(2025, 11, 27), dt.date(2025, 11, 28),
           dt.date(2026, 5, 25), dt.date(2026, 6, 19), dt.date(2026, 9, 7), dt.date(2026, 10, 12),
           dt.date(2026, 11, 11), dt.date(2026, 11, 26), dt.date(2026, 11, 27), dt.date(2027, 5, 31),
           dt.date(2027, 6, 18)}
HOLIDAY_TT = {dt.date(2026, 11, 26), dt.date(2026, 11, 27), dt.date(2027, 5, 31), dt.date(2025, 5, 26),
              dt.date(2026, 5, 25), dt.date(2025, 11, 27), dt.date(2025, 11, 28), dt.date(2024, 11, 28),
              dt.date(2024, 11, 29), dt.date(2025, 9, 1), dt.date(2026, 9, 7), dt.date(2024, 9, 2)}
DIRW = {"S": "southbound", "N": "northbound", "E": "eastbound", "W": "westbound"}


def eastern_offset(d, hour):
    y = d.year
    mar = dt.date(y, 3, 8)
    s = mar + dt.timedelta(days=(6 - mar.weekday()) % 7)
    nov = dt.date(y, 11, 1)
    e = nov + dt.timedelta(days=(6 - nov.weekday()) % 7)
    if s < d < e:
        return 4
    if d == s:
        return 4 if hour >= 2 else 5
    if d == e:
        return 5 if hour >= 2 else 4
    return 5


def daterange(a, b):
    d = a
    while d <= b:
        yield d
        d += dt.timedelta(days=1)


# ---------------------------------------------------------------------------------------------------- loading
_PACKS = {}
_MORNING = {}
_CENSUS = {}


def get_pack(folder):
    if folder not in _PACKS:
        _PACKS[folder] = Pack(folder)
    return _PACKS[folder]


def get_morning(P, hours, tz_mode="ok"):
    key = (P.folder, tuple(hours), tz_mode)
    if key not in _MORNING:
        _MORNING[key] = morning_entries(P, hours, tz_mode)
    return _MORNING[key]


class Pack:
    def __init__(self, folder):
        self.folder = folder
        p = lambda f: os.path.join(folder, f)
        self.cx = pd.read_csv(p(F_COMPLEX))
        self.name_of = dict(zip(self.cx.complex_id, self.cx.complex))
        self.id_of = dict(zip(self.cx.complex, self.cx.complex_id))
        self.cap = pd.read_csv(p(F_CAP), dtype=str)
        self.tt = pd.read_csv(p(F_TT))
        self.fleet = pd.read_csv(p(F_FLEET))
        self.census = pd.read_excel(p(F_CENSUS), sheet_name="Counts")
        self.counts = {}
        xl = pd.ExcelFile(p(F_COUNTS))
        for sh in xl.sheet_names:
            if sh != "Method":
                self.counts[sh] = xl.parse(sh, dtype={"Due": str, "Arrived": str})
        self._fare = None
        self._local = None
        self._trips = {}

    @property
    def fare(self):
        if self._fare is None:
            t = pd.read_parquet(os.path.join(self.folder, F_FARE))
            self._fare = t
        return self._fare


def fare_local(P):
    """Hourly entries with their local date and hour."""
    if P._local is None:
        f = P.fare.copy()
        utc = f.hour_utc.dt.tz_convert("America/New_York")
        f["ldate"] = utc.dt.date
        f["lhour"] = utc.dt.hour
        P._local = f
    return P._local


def morning_entries(P, hours=(6, 7, 8, 9), tz_mode="ok"):
    """{(complex_id, local date): entries in the local hours given}. tz_mode, for the mess-neutrality checks:
    'utc_as_local' reads the UTC hours as local, 'fixed4' and 'fixed5' convert at four or five hours all year."""
    if tz_mode == "ok":
        f = fare_local(P)
    else:
        f = P.fare.copy()
        off = {"utc_as_local": 0, "fixed4": 4, "fixed5": 5}[tz_mode]
        t = f.hour_utc.dt.tz_localize(None) - pd.Timedelta(hours=off)
        f["ldate"] = t.dt.date
        f["lhour"] = t.dt.hour
    m = f[f.lhour.isin(hours)]
    g = m.groupby(["complex_id", "ldate"]).entries.sum()
    return g.to_dict()


def weekday_index(me, cids, window=AUTUMN, drop=FEDERAL):
    """Each complex's mean morning entries by weekday over the window's weekdays (federal holidays out), over its
    Tuesday-to-Thursday mean."""
    out = {}
    for c in cids:
        by = defaultdict(list)
        for d in daterange(*window):
            if d.weekday() < 5 and d not in drop and (c, d) in me:
                by[WD[d.weekday()]].append(me[(c, d)])
        mid = np.mean(by["Tue"] + by["Wed"] + by["Thu"])
        out[c] = {wd: float(np.mean(by[wd]) / mid) for wd in WD}
        out[c]["_mid"] = float(mid)
    return out


def spring_ratio(me, cids, year, drop=FEDERAL):
    """The network's mean weekday morning entries over the spring pick's dates of `year` against its autumn pick
    weekdays of year-1 (federal holidays out of both)."""
    def mean_over(a, b):
        tot = defaultdict(float)
        for c in cids:
            for d in daterange(a, b):
                if d.weekday() < 5 and d not in drop and (c, d) in me:
                    tot[d] += me[(c, d)]
        return float(np.mean(list(tot.values())))
    sp = mean_over(dt.date(year, 3, 1), dt.date(year, 6, 25))
    au = mean_over(dt.date(year - 1, 9, 8), dt.date(year - 1, 12, 18))
    return sp / au


def capacity_at(P, code, day=PICK[0]):
    c = P.cap[P.cap.platform_code == code]
    for _, r in c.iterrows():
        a = dt.date.fromisoformat(r.effective_from)
        b = dt.date.fromisoformat(r.effective_to) if isinstance(r.effective_to, str) and r.effective_to else dt.date(2100, 1, 1)
        if a <= day <= b:
            return int(r.rated_capacity)
    raise KeyError(code)


WATCH = [("GAR-2", "Garnett Street", "Line 2 island platform"), ("GAR-3S", "Garnett Street", "Line 3 southbound platform"),
         ("SAL-1S", "Sallow Park", "Line 1 southbound platform"), ("SAL-1N", "Sallow Park", "Line 1 northbound platform"),
         ("SAL-4S", "Sallow Park", "Line 4 southbound platform"), ("HES-1S", "Hesper Avenue", "Line 1 southbound platform"),
         ("HES-3", "Hesper Avenue", "Line 3 island platform"), ("COR-5W", "Corran Junction", "Line 5 westbound platform"),
         ("COR-2", "Corran Junction", "Line 2 island platform"), ("FER-5W", "Ferrier Square", "Line 5 westbound platform"),
         ("FER-4S", "Ferrier Square", "Line 4 southbound platform"), ("FER-4N", "Ferrier Square", "Line 4 northbound platform"),
         ("ALB-3S", "Albrecht Place", "Line 3 southbound platform"), ("ALB-3N", "Albrecht Place", "Line 3 northbound platform"),
         ("ALB-6", "Albrecht Place", "Line 6 island platform"), ("QUA-1S", "Quarry Road", "Line 1 southbound platform"),
         ("QUA-6", "Quarry Road", "Line 6 island platform")]


def code_label(code):
    for c, s, lab in WATCH:
        if c == code:
            return s, lab
    raise KeyError(code)


def plat_key(label):
    """'Line 1 southbound platform' -> ('1', 'S'); 'Line 2 island platform' -> ('2', None)"""
    parts = label.split()
    line = parts[1]
    w = parts[2]
    if w == "island":
        return line, None
    return line, {v: k for k, v in DIRW.items()}[w]


# ---------------------------------------------------------------------------------------------------- counts
def count_peaks(P, code):
    """{date: (peak quarter-hour mean, quarter start)} from the count sheets."""
    st, lab = code_label(code)
    df = P.counts[st]
    line, d = plat_key(lab)
    want = "Line %s island" % line if d is None else "Line %s %s" % (line, DIRW[d].capitalize())
    df = df[df.Platform == want]
    out = {}
    for day, g in df.groupby("Date"):
        mins = g.Arrived.map(lambda s: int(s[:2]) * 60 + int(s[3:5]))
        best, bq = -1, None
        for q in range(7 * 60, 9 * 60 + 31, 15):
            xs = g.People[(mins >= q) & (mins < q + 15)]
            if len(xs):
                m = float(xs.mean())
                if m > best:
                    best, bq = m, q
        out[pd.Timestamp(day).date()] = (best, bq)
    return out


# ---------------------------------------------------------------------------------------------------- census rates
class Census:
    """Per-minute flows from the census, normalised to an ordinary autumn 2026 Tuesday-to-Thursday morning."""

    def __init__(self, P, me, idx, island_split=0.5, early=0.5, quarter_shift=0):
        c = P.census
        self.station_day = {}
        self.to = defaultdict(lambda: np.zeros(16))       # (station, line, dir or None) -> people per quarter
        self.frm = defaultdict(lambda: np.zeros(16))
        self.passage = []                                   # (station, (line, dir|None, trains dir), (...), arr)
        q_index = {"%02d:%02d" % divmod(6 * 60 + 15 * i, 60): i for i in range(16)}
        for (st, cid, day), g in c.groupby(["Station", "Complex ID", "Census date"]):
            d = pd.Timestamp(day).date()
            norm = idx[cid]["_mid"] / me.get((cid, d), idx[cid]["_mid"])
            self.station_day[st] = (d, norm)
            for _, r in g.iterrows():
                qi = min(15, max(0, q_index[r["Quarter-hour"]] + quarter_shift))
                loc = r.Location
                if r.Direction in ("to platform", "from platform"):
                    lab = loc.split(",")[0]
                    line, dd = plat_key(lab)
                    key = (st, line, dd)
                    (self.to if r.Direction == "to platform" else self.frm)[key][qi] += r.People * norm
                else:
                    self._passage(st, loc, qi, r.People * norm)
        self.island_split = island_split
        self.early = early
        self._pass = defaultdict(lambda: np.zeros(16))
        for (st, a, b, qi, v) in self.passage:
            self._pass[(st, a, b)][qi] += v

    def _passage(self, st, loc, qi, v):
        # "Passage, Line 1 southbound platform to Line 4 southbound platform (southbound to eastbound trains)"
        body = loc[len("Passage, "):]
        trains = None
        if "(" in body:
            body, trains = body[:body.index("(")].strip(), body[body.index("(") + 1:-1]
        a, b = body.split(" to ")
        la, da = plat_key(a)
        lb, db = plat_key(b)
        if trains:
            ta, tb = trains.replace(" trains", "").split(" to ")
            inv = {v: k for k, v in DIRW.items()}
            da = da or inv[ta]
            db = db or inv[tb]
        self.passage.append((st, (la, da), (lb, db), qi, v))

    def rates(self, line, d, station, factor):
        """(arrive, alight) per-minute arrays over minutes 300..660 for a line-direction at a station."""
        key = (line, d, station)
        if not hasattr(self, "_rc"):
            self._rc = {}
        if key not in self._rc:
            self._rc[key] = self._rates(line, d, station)
        a, x = self._rc[key]
        return a * factor, x * factor

    def _rates(self, line, d, station):
        factor = 1.0
        arr = np.zeros(361)
        ali = np.zeros(361)

        def spread(q16, out, share=1.0):
            for i in range(16):
                a = 60 + 15 * i
                out[a:a + 15] += q16[i] / 15.0 * share * factor
            out[30:60] += q16[0] / 15.0 * self.early * share * factor
            out[0:30] += q16[0] / 15.0 * self.early * 0.4 * share * factor
            out[300:361] += q16[15] / 15.0 * share * factor

        if (station, line, d) in self.to:
            spread(self.to[(station, line, d)], arr)
            spread(self.frm[(station, line, d)], ali)
        elif (station, line, None) in self.to:
            sh = self.island_split if d == LINE_DIRS[line][0] else 1.0 - self.island_split
            spread(self.to[(station, line, None)], arr, sh)
            spread(self.frm[(station, line, None)], ali, sh)
        for (st, a, b), q16 in self._pass.items():
            if st != station:
                continue
            if a == (line, d):
                spread(q16, ali)
            if b == (line, d):
                spread(q16, arr)
        return arr, ali


LINE_DIRS = {"1": ("S", "N"), "4": ("S", "N"), "5": ("W", "E"), "2": ("E", "W"), "3": ("S", "N"), "6": ("E", "W")}


def trips(P, plan, line, d):
    """[(trip, [(station, arrival minute)])] in order of departure."""
    if (plan, line, d) in P._trips:
        return P._trips[(plan, line, d)]
    t = P.tt[(P.tt.plan == plan) & (P.tt.line == int(line)) & (P.tt.direction == d)]
    out = []
    for trip, g in t.groupby("trip", sort=False):
        stops = [(r.station, int(r.arrive[:2]) * 60 + int(r.arrive[3:5]) + int(r.arrive[6:8]) / 60.0)
                 for r in g.itertuples()]
        if stops[0][1] > 11 * 60 or stops[-1][1] < 5 * 60:
            continue
        out.append((trip, stops))
    out.sort(key=lambda x: x[1][0][1])
    P._trips[(plan, line, d)] = out
    return out


def cars_of(P, plan, line):
    t = P.tt[(P.tt.plan == plan) & (P.tt.line == int(line))]
    return int(t.cars.iloc[0])


def run_line(P, C, plan, line, d, factor_of, car_load=150, room_override=None):
    """At-arrival crowds at every station of a line-direction: {station: [(t, crowd, left)]}"""
    T = trips(P, plan, line, d)
    cap = cars_of(P, plan, line) * car_load
    stations = [s for s, _ in T[0][1]]
    rates = {s: C.rates(line, d, s, factor_of(s)) for s in stations}
    cum = {s: (np.concatenate([[0], np.cumsum(rates[s][0])]), np.concatenate([[0], np.cumsum(rates[s][1])]))
           for s in stations}

    def integ(cs, a, b):
        def at(x):
            x = min(max(x - 300.0, 0.0), 361.0)
            i = int(x)
            if i >= len(cs) - 1:
                return cs[-1]
            return cs[i] + (cs[i + 1] - cs[i]) * (x - i)
        return max(0.0, at(b) - at(a))

    carry = {s: 0.0 for s in stations}
    last = {s: None for s in stations}
    ev = {s: [] for s in stations}
    for trip, stops in T:
        load = 0.0
        for s, t in stops:
            tp = last[s] if last[s] is not None else t - 6.0
            n = integ(cum[s][0], tp, t)
            x = integ(cum[s][1], tp, t)
            a = min(load, x)
            crowd = carry[s] + n
            room = cap - (load - a) if room_override is None else room_override(s, t, cap, load - a)
            b = min(crowd, max(room, 0.0))
            carry[s] = crowd - b
            load = load - a + b
            ev[s].append((t, crowd, carry[s]))
            last[s] = t
    return ev


def run_all(P, C, plan, factor_of, car_load=150, room_override=None):
    out = {}
    for line, dirs in LINE_DIRS.items():
        for d in dirs:
            out[(line, d)] = run_line(P, C, plan, line, d, factor_of, car_load, room_override)
    return out


def _waiting(events, t):
    prev = nxt = None
    for e in events:
        if e[0] <= t:
            prev = e
        else:
            nxt = e
            break
    if prev is None:
        return 0.0
    if nxt is None:
        return prev[2]
    span = nxt[0] - prev[0]
    return prev[2] + max(0.0, (nxt[1] - prev[2]) * (t - prev[0]) / span if span > 0 else 0.0)


def platform_series(out, station, label):
    line, d = plat_key(label)
    if d is None:
        d1, d2 = LINE_DIRS[line]
        e1, e2 = out[(line, d1)][station], out[(line, d2)][station]
        res = [(t, c + _waiting(e2, t)) for (t, c, _l) in e1] + [(t, c + _waiting(e1, t)) for (t, c, _l) in e2]
        return sorted(res)
    return [(t, c) for (t, c, _l) in out[(line, d)][station]]


def peak_quarter(series):
    best, bq = 0.0, None
    for q in range(7 * 60, 9 * 60 + 31, 15):
        xs = [c for (t, c) in series if q <= t < q + 15]
        if xs:
            m = sum(xs) / len(xs)
            if m > best:
                best, bq = m, q
    return best, bq


# ---------------------------------------------------------------------------------------------------- the golden
class Model:
    def __init__(self, folder, island_split=0.5, spring_year_ratio=None, hours=(6, 7, 8, 9), tz_mode="ok",
                 quarter_shift=0):
        self.P = get_pack(folder)
        self.me = get_morning(self.P, hours, tz_mode)
        cids = sorted(self.P.name_of)
        self.idx = weekday_index(self.me, cids)
        self.r2025 = spring_ratio(self.me, cids, 2025)
        self.r2026 = spring_ratio(self.me, cids, 2026)
        self.spring = self.r2026 if spring_year_ratio is None else spring_year_ratio
        ck = (folder, island_split, tuple(hours), tz_mode, quarter_shift)
        if ck not in _CENSUS:
            _CENSUS[ck] = Census(self.P, self.me, self.idx, island_split=island_split, quarter_shift=quarter_shift)
        self.C = _CENSUS[ck]
        self.caps = {code: capacity_at(self.P, code) for code, _s, _l in WATCH}

    def factor(self, wd, spring=True):
        sp = self.spring if spring else 1.0
        return lambda s: self.idx[self.P.id_of[s]][wd] * sp

    def forecast(self, plan="SPR27", spring=True, car_load=150, room_override=None, wds=WD):
        """{code: {wd: peak / capacity}}"""
        res = defaultdict(dict)
        for wd in wds:
            out = run_all(self.P, self.C, plan, self.factor(wd, spring), car_load, room_override)
            for code, st, lab in WATCH:
                pk, _q = peak_quarter(platform_series(out, st, lab))
                res[code][wd] = pk / self.caps[code]
        return dict(res)


def tally(fc, thresh=THRESH):
    posts = {c: [wd for wd in WD if fc[c][wd] > thresh] for c in fc}
    per_wd = {wd: sum(1 for c in fc if fc[c][wd] > thresh) for wd in WD}
    return sum(per_wd.values()), per_wd, posts


def golden(folder):
    M = Model(folder)
    fc = M.forecast()
    total, per_wd, posts = tally(fc)
    return dict(model=M, forecast=fc, total=total, per_wd=per_wd, posts=posts)


# ---------------------------------------------------------------------------------------------------- the default path
def default_path(M, spring=None, use_hybrid=False, scale_8car=False):
    """R0: each platform's mid-week counted peak carried to each spring weekday by its complex's weekday index and
    the spring ratio."""
    sp = M.spring if spring is None else spring
    fc = {}
    for code, st, lab in WATCH:
        pk = count_peaks(M.P, code)
        mids = [v[0] for d, v in pk.items() if d.weekday() in (1, 2, 3)]
        mid = float(np.mean(mids))
        cid = M.P.id_of[st]
        fc[code] = {}
        for wd in WD:
            v = mid * M.idx[cid][wd] * sp
            if use_hybrid:
                hyb = [vv[0] for d, vv in pk.items() if WD[d.weekday()] == wd and d.weekday() in (0, 4)]
                if hyb:
                    v = hyb[0] * sp
            if scale_8car and code == "COR-5W":
                v *= 6.0 / 8.0
            fc[code][wd] = v / M.caps[code]
    return fc


# ---------------------------------------------------------------------------------------------------- rivals
def forecast_rooms(M, plan, wd, spring=True, car_load=150):
    """The room each train had at each station on a weekday: {(line, d, station, k): room}."""
    rooms = {}

    def rec(s, t, cap, onboard, _store=rooms, _ctr={}):
        return cap - onboard

    out = {}
    for line, dirs in LINE_DIRS.items():
        for d in dirs:
            T = trips(M.P, plan, line, d)
            k_of = {}

            def ov(s, t, cap, onboard, line=line, d=d, k_of=k_of):
                k = k_of.get(s, 0)
                k_of[s] = k + 1
                rooms[(line, d, s, k)] = cap - onboard
                return cap - onboard
            run_line(M.P, M.C, plan, line, d, M.factor(wd, spring), car_load, ov)
    return rooms


def forecast_constant_room(M, base_wd="Wed", plan="SPR27"):
    """A queue model whose trains keep the room they had on a mid-week morning whatever the weekday."""
    rooms = forecast_rooms(M, plan, base_wd)
    res = defaultdict(dict)
    for wd in WD:
        out = {}
        for line, dirs in LINE_DIRS.items():
            for d in dirs:
                k_of = {}

                def ov(s, t, cap, onboard, line=line, d=d, k_of=k_of):
                    k = k_of.get(s, 0)
                    k_of[s] = k + 1
                    return rooms.get((line, d, s, k), cap - onboard)
                out[(line, d)] = run_line(M.P, M.C, plan, line, d, M.factor(wd), 150, ov)
        for code, st, lab in WATCH:
            pk, _q = peak_quarter(platform_series(out, st, lab))
            res[code][wd] = pk / M.caps[code]
    return dict(res)


def forecast_scaled_room(M, k, plan="SPR27", spring=True):
    return M.forecast(plan=plan, spring=spring, room_override=lambda s, t, cap, onboard: (cap - onboard) * k)


def forecast_no_queue(M, plan="SPR27"):
    return M.forecast(plan=plan, room_override=lambda s, t, cap, onboard: 1e9)


def rival_complex_level(M):
    """The complex's forecast peak (its watch platforms' counted peaks summed, carried as R0) against the sum of
    their rated capacities: a complex over the line posts every watch-list platform it has."""
    r0 = default_path(M)
    by = defaultdict(list)
    for code, st, lab in WATCH:
        by[st].append(code)
    fc = {}
    for st, codes in by.items():
        for wd in WD:
            num = sum(r0[c][wd] * M.caps[c] for c in codes)
            den = sum(M.caps[c] for c in codes)
            for c in codes:
                fc.setdefault(c, {})[wd] = num / den
    return fc


def rival_equal_split(M, hours=(8,)):
    """Each complex's busiest morning hour of autumn mid-week entries split equally over its platforms, one
    headway's share standing on each, carried by the weekday index and the spring ratio."""
    f = fare_local(M.P)
    hw = {"1": 4.0, "4": 4.0, "5": 4.0, "2": 6.0, "3": 6.0, "6": 7.5}
    nplat = defaultdict(int)
    for _, r in M.P.cap.iterrows():
        nplat[r.complex] += 1
    fc = {}
    for code, st, lab in WATCH:
        cid = M.P.id_of[st]
        line, d = plat_key(lab)
        peak_hour = M.idx[cid]["_mid"] / 4.0          # four morning hours, the mean hour
        per_min = peak_hour * 1.35 / 60.0 / nplat[st]
        crowd = per_min * hw[line] * (2 if d is None else 1)
        fc[code] = {wd: crowd * M.idx[cid][wd] * M.spring / M.caps[code] for wd in WD}
    return fc


def rival_weekly_average(fc):
    out = {}
    for c in fc:
        m = float(np.mean([fc[c][wd] for wd in WD]))
        out[c] = {wd: m for wd in WD}
    return out


def rival_one_scalar(M):
    """The no-queue census model scaled by one network-wide factor fitted to every mid-week count."""
    nq_aut = forecast_no_queue_plan(M, "AUT26", spring=False)
    num = den = 0.0
    for code, st, lab in WATCH:
        pk = count_peaks(M.P, code)
        for d, v in pk.items():
            if d.weekday() in (1, 2, 3):
                num += v[0] / M.caps[code]
                den += nq_aut[code][WD[d.weekday()]]
    k = num / den
    nq = forecast_no_queue(M)
    return {c: {wd: nq[c][wd] * k for wd in WD} for c in nq}, k


def rival_per_platform_scalar(M):
    """The no-queue census model scaled platform by platform to its own mid-week counts."""
    nq_aut = forecast_no_queue_plan(M, "AUT26", spring=False)
    nq = forecast_no_queue(M)
    out = {}
    for code, st, lab in WATCH:
        pk = count_peaks(M.P, code)
        obs = [v[0] / M.caps[code] for d, v in pk.items() if d.weekday() in (1, 2, 3)]
        mod = [nq_aut[code][WD[d.weekday()]] for d, v in pk.items() if d.weekday() in (1, 2, 3)]
        k = float(np.mean(obs) / np.mean(mod))
        out[code] = {wd: nq[code][wd] * k for wd in WD}
    return out


def rival_counts_as_is(M):
    """Last autumn's mid-week counted peaks as every spring weekday's (no weekday index, no spring ratio)."""
    out = {}
    for code, st, lab in WATCH:
        pk = count_peaks(M.P, code)
        mid = float(np.mean([v[0] for d, v in pk.items() if d.weekday() in (1, 2, 3)]))
        out[code] = {wd: mid / M.caps[code] for wd in WD}
    return out


def forecast_no_queue_plan(M, plan, spring=True):
    return M.forecast(plan=plan, spring=spring, room_override=lambda s, t, cap, onboard: 1e9)


# ---------------------------------------------------------------------------------------------------- Ask A: escalators
WATCH_COMPLEXES = ["Garnett Street", "Sallow Park", "Hesper Avenue", "Corran Junction", "Ferrier Square",
                   "Albrecht Place", "Quarry Road"]
RATED = {600: 40, 800: 60, 1000: 80}


def _platform_escalators(folder):
    inv = pd.read_csv(os.path.join(folder, F_INV))
    e = inv[(inv.type == "escalator") & (inv.complex.isin(WATCH_COMPLEXES)) & inv.to_area.str.contains("platform")]
    return e


def escalator_directions_peak(folder, start=7 * 60, end=9 * 60 + 30):
    """{unit: the set of directions it was set to run between 07:00 and 09:30 local on the autumn pick's weekdays},
    from the controllers' log."""
    log = pd.read_csv(os.path.join(folder, F_CTRL))
    log["t"] = pd.to_datetime(log.event_utc).dt.tz_localize("UTC").dt.tz_convert("America/New_York")
    log["ld"] = log.t.dt.date
    log["lm"] = log.t.dt.hour * 60 + log.t.dt.minute + log.t.dt.second / 60.0
    runs = log[log.event.str.startswith("RUN")]
    days = set(autumn_weekdays())
    out = {}
    for unit, g in runs.groupby("unit"):
        dirs = set()
        for d, gg in g.groupby("ld"):
            if d not in days:
                continue
            before = gg[gg.lm <= start]
            if len(before):
                dirs.add(before.event.iloc[-1].split()[1].lower())
            for e in gg[(gg.lm > start) & (gg.lm < end)].event:
                dirs.add(e.split()[1].lower())
        out[unit] = dirs
    return out


def _flow(r, asset, route):
    speed = float(r.speed_mps) if route in ("natural", "dir_only") else float(asset.loc[r.unit, "speed_mps"])
    mm_ = float(r.width) * (25.4 if r.width_unit == "in" else 1.0)
    step = max(b for b in RATED if b <= mm_ + 1e-9) if mm_ >= 600 else 600
    return RATED[step] * speed / 0.5


def _timelines(folder):
    """{unit: (UTC instants as int64 ns, events)} from the controllers' log, in time order."""
    log = pd.read_csv(os.path.join(folder, F_CTRL))
    log["t"] = pd.to_datetime(log.event_utc).dt.tz_localize("UTC")
    out = {}
    for unit, g in log.sort_values("t", kind="stable").groupby("unit"):
        out[unit] = (g.t.dt.as_unit("ns").astype("int64").to_numpy(), list(g.event))
    return out


def _window_shares(tl, a, b):
    """{('up'|'down', running): share of the window a..b (pd.Timestamps)}: the direction the escalator is set to run
    (its last RUN) and whether it is running (its last event a RUN) through the window."""
    ts, ev = tl
    a_, b_ = a.as_unit("ns").value, b.as_unit("ns").value
    i = int(np.searchsorted(ts, a_, side="right")) - 1
    set_dir = None
    k = i
    while k >= 0 and not ev[k].startswith("RUN"):
        k -= 1
    if k >= 0:
        set_dir = ev[k].split()[1].lower()
    running = i >= 0 and ev[i].startswith("RUN")
    out = defaultdict(float)
    t = a_
    j = i + 1
    while j < len(ts) and ts[j] < b_:
        out[(set_dir, running)] += (ts[j] - t) / (b_ - a_)
        if ev[j].startswith("RUN"):
            set_dir, running = ev[j].split()[1].lower(), True
        else:
            running = False
        t = ts[j]
        j += 1
    out[(set_dir, running)] += (b_ - t) / (b_ - a_)
    return out


def _peak_windows(days, utc=False, start=(7, 0), end=(9, 30), fixed=None):
    out = []
    for d in days:
        if fixed is not None:
            out.append((pd.Timestamp(dt.datetime.combine(d, dt.time(*start)), tz="UTC") + pd.Timedelta(hours=fixed),
                        pd.Timestamp(dt.datetime.combine(d, dt.time(*end)), tz="UTC") + pd.Timedelta(hours=fixed)))
        elif utc:
            out.append((pd.Timestamp(dt.datetime.combine(d, dt.time(*start)), tz="UTC"),
                        pd.Timestamp(dt.datetime.combine(d, dt.time(*end)), tz="UTC")))
        else:
            out.append((pd.Timestamp(dt.datetime.combine(d, dt.time(*start)), tz="America/New_York").tz_convert("UTC"),
                        pd.Timestamp(dt.datetime.combine(d, dt.time(*end)), tz="America/New_York").tz_convert("UTC")))
    return out


def unit_day_windows(folder):
    """{(unit, day): (shares, events, state at 07:00)} for every escalator between a mezzanine and a platform on every
    weekday-timetable day of the autumn pick: its shares of 07:00 to 09:30 local by (set direction, running), the log
    events inside the window and the last event before it."""
    e = _platform_escalators(folder)
    tls = _timelines(folder)
    days = autumn_weekdays()
    wins = _peak_windows(days)
    out = {}
    for u in e.unit:
        ts, ev = tls[u]
        for d, (a, b) in zip(days, wins):
            a_, b_ = a.as_unit("ns").value, b.as_unit("ns").value
            i0 = int(np.searchsorted(ts, a_, side="right"))
            i1 = int(np.searchsorted(ts, b_, side="left"))
            out[(u, d)] = (dict(_window_shares(tls[u], a, b)), ev[i0:i1], ev[i0 - 1] if i0 > 0 else None)
    return out


def ask_a(folder, route="golden", unrounded=False):
    """{complex: (down, up)} people a minute between 07:00 and 09:30. route: golden (every escalator between a
    mezzanine and a platform, the controllers' directions, the asset register's speeds, the autumn pick's
    weekday-timetable days); natural (the inventory's direction and speed); dir_only (the controllers' directions, the
    inventory's speed); speed_only (the inventory's direction, the asset register's speeds); and the readings the
    filed text rules out: time_weighted (each escalator's flow in the direction it is set to run, weighted over the
    window: the golden's own figure when every escalator keeps one direction), fault_deducted (weighted by the share
    of the window it was running), watch_only (only the escalators to watch-list platforms), with_holidays (the mean
    over every Monday to Friday of the pick, the holiday-timetable days in), utc_window (07:00 to 09:30 read in the
    log's UTC), fixed4 and fixed5 (the log converted at four or five hours all autumn, the clock change missed)."""
    e = _platform_escalators(folder)
    asset = pd.read_csv(os.path.join(folder, F_ASSET)).set_index("unit")
    if route == "watch_only":
        watch = {(w[1], w[2]) for w in WATCH}
        e = e[[(st, lab) in watch for st, lab in zip(e.complex, e.to_area)]]
    res = {}
    if route in ("time_weighted", "fault_deducted", "with_holidays", "utc_window", "fixed4", "fixed5"):
        tls = _timelines(folder)
        days = [d for d in daterange(*AUTUMN) if d.weekday() < 5] if route == "with_holidays" else autumn_weekdays()
        wins = _peak_windows(days, utc=(route == "utc_window"),
                             fixed={"fixed4": 4, "fixed5": 5}.get(route))
        for cx in WATCH_COMPLEXES:
            down = up = 0.0
            for r in e[e.complex == cx].itertuples():
                f = _flow(r, asset, "golden")
                for a, b in wins:
                    for (dirn, run), w in _window_shares(tls[r.unit], a, b).items():
                        if route == "fault_deducted" and not run:
                            continue
                        if dirn == "down":
                            down += f * w / len(wins)
                        elif dirn == "up":
                            up += f * w / len(wins)
            res[cx] = (down, up) if unrounded else (int(round(down)), int(round(up)))
        return res
    dirs = escalator_directions_peak(folder)
    for cx in WATCH_COMPLEXES:
        down = up = 0.0
        for r in e[e.complex == cx].itertuples():
            if route in ("golden", "dir_only", "watch_only"):
                ds = dirs[r.unit]
                assert len(ds) == 1, (r.unit, ds)
                dirn = next(iter(ds))
            else:
                dirn = r.direction
            f = _flow(r, asset, route)
            if dirn == "down":
                down += f
            else:
                up += f
        res[cx] = (down, up) if unrounded else (int(round(down)), int(round(up)))
    return res


# ---------------------------------------------------------------------------------------------------- Ask B: elevators
def autumn_weekdays():
    return [d for d in daterange(*AUTUMN) if d.weekday() < 5 and d not in HOLIDAY_TT]


def _windows(days=None, utc=False, fixed=None):
    out = []
    for d in (autumn_weekdays() if days is None else days):
        if fixed is not None:
            a = pd.Timestamp(dt.datetime.combine(d, dt.time(7, 0)), tz="UTC") + pd.Timedelta(hours=fixed)
            b = pd.Timestamp(dt.datetime.combine(d, dt.time(9, 45)), tz="UTC") + pd.Timedelta(hours=fixed)
        elif utc:
            a = pd.Timestamp(dt.datetime.combine(d, dt.time(7, 0)), tz="UTC")
            b = pd.Timestamp(dt.datetime.combine(d, dt.time(9, 45)), tz="UTC")
        else:
            a = pd.Timestamp(dt.datetime.combine(d, dt.time(7, 0)), tz="America/New_York").tz_convert("UTC")
            b = pd.Timestamp(dt.datetime.combine(d, dt.time(9, 45)), tz="America/New_York").tz_convert("UTC")
        out.append((a, b))
    return out


def _overlap(intervals, wins):
    tot = 0.0
    for a, b in intervals:
        for x, y in wins:
            lo, hi = max(a, x), min(b, y)
            if hi > lo:
                tot += (hi - lo).total_seconds() / 3600.0
    return tot


def _union_hours(ivs, wins):
    ivs = sorted(ivs)
    merged = []
    for a, b in ivs:
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))
    return _overlap(merged, wins)


def ask_b(folder, route="golden"):
    """{complex: elevator-hours out of service in 07:00-09:45 on the autumn pick's weekday-timetable mornings}.
    route: golden (the monitoring's modes for faults, the work orders for planned maintenance: the union of the two),
    work_orders (every work order's times), monitoring (the monitoring's modes alone); and the readings the filed
    text rules out: with_holidays (every Monday to Friday of the pick, the holiday-timetable days included),
    mean_per_day (the total over the mornings divided by their number), platform_only (the street elevators left
    out), utc_window (07:00 to 09:45 read in the logs' UTC), summed (overlapping intervals counted twice), fixed4
    and fixed5 (the logs converted at four or five hours all autumn)."""
    days = None
    if route == "with_holidays":
        days = [d for d in daterange(*AUTUMN) if d.weekday() < 5]
    wins = _windows(days, utc=(route == "utc_window"), fixed={"fixed4": 4, "fixed5": 5}.get(route))
    wo = pd.read_csv(os.path.join(folder, F_WO))
    mon = pd.read_csv(os.path.join(folder, F_MON))
    mon["t"] = pd.to_datetime(mon.event_utc).dt.tz_localize("UTC")
    ivs = defaultdict(list)
    cx_of = dict(zip(wo.unit, wo.complex))
    union = route not in ("work_orders", "monitoring")
    if route != "work_orders":
        for unit, g in mon.groupby("unit"):
            rows = list(g.sort_values("t").itertuples())
            for r, nx in zip(rows, rows[1:] + [None]):
                if r.mode != "NORMAL":
                    end = nx.t if nx is not None else pd.Timestamp("2027-01-01", tz="UTC")
                    ivs[unit].append((r.t, end))
    for r in wo.itertuples():
        if route == "work_orders" or (union and (r.type == "PM" or route == "summed")):
            ivs[r.unit].append((pd.Timestamp(r.out_of_service_at, tz="UTC"), pd.Timestamp(r.in_service_at, tz="UTC")))
    skip = set()
    if route == "platform_only":
        inv = pd.read_csv(os.path.join(folder, F_INV))
        skip = set(inv[(inv.type == "elevator") & (inv.from_area == "Street")].unit)
    res = defaultdict(float)
    for unit, iv in ivs.items():
        if unit in skip:
            continue
        res[cx_of.get(unit, "")] += (_overlap(iv, wins) if route == "summed" else _union_hours(iv, wins))
    out = {cx: res.get(cx, 0.0) for cx in WATCH_COMPLEXES}
    if route == "mean_per_day":
        out = {cx: v / len(wins) for cx, v in out.items()}
    return out
