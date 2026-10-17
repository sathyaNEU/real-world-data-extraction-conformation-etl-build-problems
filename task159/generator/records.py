"""task159 records: the files each of the commission's systems exports, written from the world. Nothing here writes
a truth column: the count sheets carry the people on the platform as each train arrived, the census the flows
through each element, the fare system its taps per complex; no record says who a full train left behind."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K
import world as W
import sim as S

REF = W.year_level(dt.date(2026, 10, 15))

# ------------------------------------------------------------------------------------------------- complexes
# legacy fare-control codes: one per fare-control area before the back office; Kennet Street was its own station
LEGACY_CODE = {
    "Kettle Creek": "KTC", "Dorrance": "DRN", "Whitcombe": "WCB", "Pell Corners": "PLC", "Norland": "NRL",
    "Larch Hill": "LCH", "Sallow Park": "SLP", "Hesper Avenue": "HSP", "Quarry Road": "QRY", "Civic Center": "CVC",
    "Market Street": "MKT", "Harbor Terminal": "HBT", "Arbor Mills": "ABM", "Ganton": "GNT", "Brisco Road": "BRC",
    "Coyle Street": "CYL", "Tamsin Avenue": "TMS", "Ferrier Square": "FRS", "Wharf Street": "WHF", "Ossory": "OSY",
    "Linden Park": "LDP", "Coldwater": "CDW", "Marchmont": "MCM", "Easton Heights": "ETH", "Brack Road": "BKR",
    "Corran Junction": "CRJ", "Bayfront": "BYF", "Westmere": "WSM", "Holloway": "HLW", "Garnett Street": "GRN",
    "Tanner Street": "TNR", "Eastgate": "EGT", "Shore Road": "SHR", "Northgate": "NGT", "Elm Rise": "ELR",
    "Albrecht Place": "ALB", "University": "UNV", "Medical Center": "MDC", "Foundry Row": "FDR", "Mint Street": "MNT",
}
KENNET = ("KEN", "Kennet Street")
KENNET_SHARE = 0.31          # of Albrecht Place's street entries came in at Kennet Street's arrays

# complexes where the riders' rest of the day is entries home or onward (entries after 11:00 over the morning's)
REST_OF_DAY = {}
for _s in W.COMPLEXES:
    REST_OF_DAY[_s] = 0.62
for _s in ("Civic Center", "Market Street", "Harbor Terminal", "Bayfront", "Wharf Street", "Mint Street",
           "Tanner Street"):
    REST_OF_DAY[_s] = 4.6
for _s in ("University", "Medical Center", "Eastgate", "Foundry Row"):
    REST_OF_DAY[_s] = 2.1
for _s in W.WATCH_COMPLEXES:
    REST_OF_DAY[_s] = 1.15

# share of riders through the arrays without a valid tap (revenue protection's survey runs 4 to 9 per cent)
EVASION = {s: 0.045 + 0.04 * ((K.stable_hash("ev", s) % 1000) / 1000.0) for s in W.COMPLEXES}
# bus-to-subway transfers through the arrays, as a share of entries (bus hubs carry more)
BUS_SHARE = {s: 0.012 + 0.01 * ((K.stable_hash("bus", s) % 1000) / 1000.0) for s in W.COMPLEXES}
for _s, _v in (("Kettle Creek", 0.118), ("Arbor Mills", 0.104), ("Ossory", 0.126), ("Sallow Park", 0.071),
               ("Corran Junction", 0.064), ("Westmere", 0.082), ("Shore Road", 0.077), ("Northgate", 0.069),
               ("Foundry Row", 0.058)):
    BUS_SHARE[_s] = _v
STAFF_SHARE = {s: 0.004 + 0.004 * ((K.stable_hash("staff", s) % 1000) / 1000.0) for s in W.COMPLEXES}
for _s in ("Civic Center", "Harbor Terminal", "Market Street"):
    STAFF_SHARE[_s] = 0.011


def _rng(*keys):
    return np.random.default_rng([K.SEED] + [K.stable_hash(*keys) % (2 ** 31)])


# ------------------------------------------------------------------------------------------------- riding by day
class Levels:
    """Each complex's morning level on each date against an ordinary October 2026 Tuesday-to-Thursday morning:
    the calendar (weekday, month, year), the complex's own Monday and Friday, the weather, and its own noise."""

    def __init__(self, start=K.LEGACY_START, end=K.EXPORT_END):
        self.days = list(K.daterange(start, end))
        r = _rng("weather")
        self.sys = {}
        for d in self.days:
            e = r.normal(0.0, 0.018)
            self.sys[d] = e
        # the snow and storm mornings the network had (lighter riding, later starts)
        for d, cut in ((dt.date(2022, 12, 23), 0.24), (dt.date(2023, 1, 25), 0.19), (dt.date(2023, 2, 28), 0.15),
                       (dt.date(2024, 1, 16), 0.21), (dt.date(2024, 2, 13), 0.27), (dt.date(2025, 1, 21), 0.18),
                       (dt.date(2025, 2, 6), 0.12), (dt.date(2025, 12, 15), 0.16), (dt.date(2026, 1, 26), 0.31),
                       (dt.date(2026, 2, 23), 0.14), (dt.date(2026, 12, 8), 0.17), (dt.date(2027, 1, 7), 0.22)):
            if d in self.sys:
                self.sys[d] += math.log(1.0 - cut)
        self.cx = {}
        for s in W.COMPLEXES:
            rc = _rng("cxnoise", s)
            self.cx[s] = dict(zip(self.days, rc.normal(0.0, 0.011, len(self.days))))

    @staticmethod
    def kind_factor(s, d):
        k = W.day_kind(d)
        if k in K.WD:
            return W.weekday_factor(s, k)
        return {"reduced": 0.84, "winter": 0.62, "holiday": 0.31, "Sat": 0.30, "Sun": 0.22}[k]

    def level(self, s, d):
        return (self.kind_factor(s, d) * W.MONTH[d.month] * W.year_level(d) / REF
                * math.exp(self.sys[d] + self.cx[s][d]))


# morning street arrivals per minute for a complex (every platform's street boarding), on the sim's grid
def street_rate(station):
    tot = np.zeros_like(S.GRID)
    for (s, l, d), f in W.FLOWS.items():
        if s == station:
            tot = tot + f["board"] * np.array([W.profile(m, f["mu"], f["sd"]) for m in S.GRID])
    return tot


STREET = {s: street_rate(s) for s in W.COMPLEXES}


def morning_hours(station, level):
    """Expected people through the arrays in each local hour 05..10 on a day at `level`."""
    rate = STREET[station] * level
    out = {}
    for h in range(5, 11):
        a, b = h * 60 - S.T0, (h + 1) * 60 - S.T0
        out[h] = float(rate[a:b].sum())
    return out


# the rest of the day's entries by local hour (11..24, 24 being the hour from midnight), shares of the total
_REST = np.array([0.050, 0.052, 0.054, 0.058, 0.074, 0.118, 0.146, 0.128, 0.088, 0.066, 0.058, 0.046, 0.036, 0.026])
REST_SHAPE = _REST / _REST.sum()
_WEEKEND = np.array([0.010, 0.020, 0.032, 0.046, 0.060, 0.074, 0.082, 0.086, 0.088, 0.088, 0.086, 0.082, 0.072,
                     0.062, 0.050, 0.040, 0.026, 0.018, 0.010, 0.004])
WEEKEND_SHAPE = _WEEKEND / _WEEKEND.sum()          # local hours 05..24
WEEKEND_TOTAL = {"Sat": 0.40, "Sun": 0.30, "holiday": 0.34}


def day_people(station, d, L):
    """Expected people entering a complex in each local hour 05..24 on date d."""
    lv = L.level(station, d)
    k = W.day_kind(d)
    am = morning_hours(station, lv if k not in ("Sat", "Sun", "holiday") else
                       W.MONTH[d.month] * W.year_level(d) / REF * math.exp(L.sys[d] + L.cx[station][d]))
    am_tot = sum(am.values())
    if k in ("Sat", "Sun", "holiday"):
        total = am_tot * (1.0 + REST_OF_DAY[station]) * WEEKEND_TOTAL[k] / 0.31 * (0.31 if k == "holiday" else 1.0)
        return {h: total * WEEKEND_SHAPE[h - 5] for h in range(5, 25)}
    out = dict(am)
    rest = am_tot * REST_OF_DAY[station]
    for i, h in enumerate(range(11, 25)):
        out[h] = rest * REST_SHAPE[i]
    return out


def contactless_share(d, station):
    t = (d - dt.date(2024, 6, 1)).days / 950.0
    base = 0.37 + 0.36 * min(1.0, max(0.0, t))
    off = ((K.stable_hash("cl", station) % 1000) / 1000.0 - 0.5) * 0.10
    return min(0.93, max(0.2, base + off))


# ------------------------------------------------------------------------------------------------- fare export
FARE_COLS = ["hour_utc", "complex_id", "entries", "paid_contactless", "paid_card", "free_transfer", "staff"]


def fare_hourly(L, census_people=None):
    """The back office's hourly export: one row per complex and hour (UTC) with entries, 3 June 2024 to the hour
    starting 23:00 local on 10 January 2027. census_people: {(station, date, local hour): people} for the census
    mornings, so the taps that day come from the people the census counted."""
    census_people = census_people or {}
    days = [d for d in K.daterange(K.NEW_EXPORT_START, K.EXPORT_END)]
    rows = []
    for s in W.COMPLEXES:
        cid = W.COMPLEX_IDS[s]
        r = _rng("fare", s)
        ev, bus, stf = EVASION[s], BUS_SHARE[s], STAFF_SHARE[s]
        for d in days:
            ppl = day_people(s, d, L)
            cl = contactless_share(d, s)
            for h in range(5, 25):
                lam = ppl[h]
                key = (s, d, h)
                if key in census_people:
                    people = census_people[key]
                else:
                    people = int(r.poisson(lam / (1.0 - ev)))
                taps = int(r.binomial(people, 1.0 - ev)) if people > 0 else 0
                if taps == 0:
                    continue
                n_bus = int(r.binomial(taps, bus))
                n_stf = int(r.binomial(taps - n_bus, stf))
                paid = taps - n_bus - n_stf
                n_cl = int(r.binomial(paid, cl))
                hh = h % 24
                local_day = d if h < 24 else d + dt.timedelta(days=1)
                off = K.us_eastern_offset(local_day, hh)
                t_utc = dt.datetime.combine(local_day, dt.time(hh)) + dt.timedelta(hours=off)
                rows.append((t_utc, cid, taps, n_cl, paid - n_cl, n_bus, n_stf))
    rows.sort(key=lambda x: (x[0], x[1]))
    return rows


# ------------------------------------------------------------------------------------------------- legacy reads
LEGACY_COLS = ["svc_date", "period_end", "stn", "stn_name", "entries"]
_PERIODS = [("04:00", [24]), ("08:00", [5, 6, 7]), ("12:00", [8, 9, 10, 11]), ("16:00", [12, 13, 14, 15]),
            ("20:00", [16, 17, 18, 19]), ("24:00", [20, 21, 22, 23])]


def legacy_rows(L):
    """The legacy fare system's register reads: entries per station in each four-hour period (local time, the
    period ending at the time shown), 1 February 2022 to 30 June 2024. The period ending 04:00 holds the hour after
    midnight of the service day before."""
    rows = []
    for s in W.COMPLEXES:
        code = LEGACY_CODE[s]
        r = _rng("legacy", s)
        prev = None
        for d in K.daterange(K.LEGACY_START, K.LEGACY_END):
            ppl = day_people(s, d, L)
            for pe, hours in _PERIODS:
                if pe == "04:00":
                    lam = prev[24] if prev is not None else ppl[24] * 0.9
                else:
                    lam = sum(ppl[h] for h in hours)
                taps = int(r.poisson(lam))
                if s == "Albrecht Place" and d < K.KENNET_JOIN:
                    ken = int(round(taps * KENNET_SHARE))
                    rows.append((d.isoformat(), pe, KENNET[0], KENNET[1], ken))
                    taps -= ken
                rows.append((d.isoformat(), pe, code, s, taps))
            prev = ppl
    rows.sort(key=lambda x: (x[0], x[1], x[2]))
    return rows


# ------------------------------------------------------------------------------------------------- census
# The October 2026 station census: one Tuesday, Wednesday or Thursday at every station, 06:00 to 10:00, people a
# quarter-hour at each platform access and at each passage between platforms.
CENSUS_DAYS = [d for d in K.daterange(*K.CENSUS_WINDOW) if d.weekday() in (1, 2, 3) and d not in K.REDUCED]


def census_date(station):
    i = W.COMPLEXES.index(station)
    return CENSUS_DAYS[(i * len(CENSUS_DAYS)) // len(W.COMPLEXES)]


def _access(key):
    """The census screenlines for a platform: [(location name, share of the platform's flows)]."""
    station, rest = key.split("|")
    line = rest[0]
    ew = W.LINES[line]["dirs"][0] in ("E", "W")
    ends = ("west", "east") if ew else ("north", "south")
    busy = key in W.CAPACITY or station in ("Civic Center", "Market Street", "Harbor Terminal", "Bayfront",
                                              "Wharf Street", "University", "Medical Center", "Eastgate")
    if not busy:
        return [("access", 1.0)]
    a = 0.52 + 0.14 * ((K.stable_hash("acc", key) % 1000) / 1000.0)
    return [("%s access" % ends[0], a), ("%s access" % ends[1], 1.0 - a)]


def _rate(f, m, which):
    if which == "board":
        return f["board"] * W.profile(m, f["mu"], f["sd"])
    return f["exit"] * W.profile(m, f["mu"] + 8, f["sd"])


def _quarter_integral(fun, q0):
    # minutes q0 .. q0+15, midpoint rule on half-minutes
    return sum(fun(q0 + 0.25 + 0.5 * i) * 0.5 for i in range(30))


CENSUS_COLS = ["station", "complex_id", "census_date", "location_id", "location", "direction", "quarter_start",
               "people"]
CENSUS_QUARTERS = list(range(6 * 60, 10 * 60, 15))


def census_rows(L):
    rows = []
    for s in W.COMPLEXES:
        d = census_date(s)
        lv = L.level(s, d)
        r = _rng("census", s)
        n = 0
        for key, line, dirs in W.platforms_at(s):
            label = W._plat_label(key)
            for loc, share in _access(key):
                n += 1
                lid = "%d-C%02d" % (W.COMPLEX_IDS[s], n)
                name = "%s, %s" % (label, loc)
                for which, word in (("board", "to platform"), ("exit", "from platform")):
                    for q in CENSUS_QUARTERS:
                        e = 0.0
                        for dd in dirs:
                            f = W.FLOWS.get((s, line, dd))
                            if f:
                                e += _quarter_integral(lambda m: _rate(f, m, which), q)
                        people = int(r.poisson(e * share * lv))
                        rows.append((s, W.COMPLEX_IDS[s], d.isoformat(), lid, name, word,
                                     "%02d:%02d" % divmod(q, 60), people))
        for (st, a, b, rate) in W.TRANSFERS:
            if st != s:
                continue
            n += 1
            lid = "%d-C%02d" % (W.COMPLEX_IDS[s], n)
            ka = "%s|%s" % (s, a if (s, a[0]) not in W.ISLANDS else a[0])
            kb = "%s|%s" % (s, b if (s, b[0]) not in W.ISLANDS else b[0])
            name = "Passage, %s to %s" % (W._plat_label(ka), W._plat_label(kb))
            if (s, a[0]) in W.ISLANDS or (s, b[0]) in W.ISLANDS:
                name += " (%s to %s trains)" % (W.DIR_WORD[a[1:]].lower(), W.DIR_WORD[b[1:]].lower())
            for q in CENSUS_QUARTERS:
                e = _quarter_integral(lambda m: rate * W.profile(m, 488.0, 32.0), q)
                people = int(r.poisson(e * lv))
                rows.append((s, W.COMPLEX_IDS[s], d.isoformat(), lid, name, "passage", "%02d:%02d" % divmod(q, 60),
                             people))
    return rows


# ------------------------------------------------------------------------------------------------- platform counts
# The count programme's autumn 2026 schedule as the contractor was booked in September: two mid-week mornings for
# every watch-list platform, and for the hybrid-day sample a Monday and a Friday as well.
D = dt.date
COUNT_PLAN = {
    "Garnett Street": [D(2026, 10, 13), D(2026, 10, 22)],
    "Hesper Avenue": [D(2026, 10, 14), D(2026, 10, 27)],
    "Corran Junction": [D(2026, 10, 15), D(2026, 10, 28)],
    "Ferrier Square": [D(2026, 10, 20), D(2026, 10, 29)],
    "Albrecht Place": [D(2026, 10, 21), D(2026, 11, 3)],
    "Sallow Park": [D(2026, 11, 4), D(2026, 11, 12)],
    "Quarry Road": [D(2026, 11, 5), D(2026, 11, 10)],
}
HYBRID_DAYS = {
    "Garnett Street|2": [D(2026, 10, 19), D(2026, 10, 23)],
    "Hesper Avenue|3": [D(2026, 10, 26), D(2026, 10, 30)],
    "Corran Junction|5W": [D(2026, 11, 2), D(2026, 11, 6)],
    "Ferrier Square|5W": [D(2026, 11, 9), D(2026, 11, 13)],
    "Albrecht Place|6": [D(2026, 11, 16), D(2026, 11, 20)],
    "Quarry Road|6": [D(2026, 11, 16), D(2026, 11, 20)],
}
COUNT_START, COUNT_END = 6 * 60 + 45, 9 * 60 + 50


def count_days():
    """{date: [platform keys counted that morning]}"""
    out = {}
    for cx, days in COUNT_PLAN.items():
        keys = [k for k in W.WATCH_KEYS if k.startswith(cx + "|")]
        for d in days:
            out.setdefault(d, []).extend(keys)
    for k, days in HYBRID_DAYS.items():
        for d in days:
            out.setdefault(d, []).append(k)
    return dict(sorted(out.items()))


def count_morning(L, d, plan="autumn2026"):
    """One counted morning: the network run on the day's riding, trains a little late now and then."""
    rng = _rng("count-day", d.isoformat())
    drng = _rng("count-delay", d.isoformat())
    out, _a, _x, _t = S.run_all(lambda s: L.level(s, d), plan=plan, rng=rng, delay_rng=drng)
    return out


def _hhmm(m):
    m = int(math.floor(m + 1e-9))
    return "%02d:%02d" % divmod(m, 60)


def count_sheet_rows(L):
    """[(complex, date, platform label, direction or '', due, arrived, people, estimated)] for every counted train."""
    rows = []
    for d, keys in count_days().items():
        out = count_morning(L, d)
        for key in keys:
            station = key.split("|")[0]
            nr = _rng("enumerator", key, d.isoformat())
            for (t, crowd, line, dd, sched) in S.platform_series(out, key):
                if not (COUNT_START <= t <= COUNT_END):
                    continue
                if crowd < 200:
                    ppl = int(round(crowd * (1.0 + nr.normal(0.0, 0.02))))
                    est = ""
                else:
                    ppl = int(round(crowd * (1.0 + nr.normal(0.0, 0.035)) / 10.0) * 10)
                    est = "E"
                island = len(key.split("|")[1]) == 1
                rows.append((station, d, key, W.DIR_WORD[dd] if island else "", _hhmm(sched), _hhmm(t), ppl, est))
    return rows


# ------------------------------------------------------------------------------------------------- timetable
TT_COLS = ["plan", "line", "direction", "trip", "station", "arrive", "cars"]


def tt_headway(line, minute, plan):
    peak = {"1": 4.0, "4": 4.0, "5": 4.0, "2": 6.0, "3": 6.0, "6": 7.5}[line]
    shoulder = {"1": 6.0, "4": 6.0, "5": 6.0, "2": 8.0, "3": 8.0, "6": 10.0}[line]
    midday = {"1": 7.5, "4": 7.5, "5": 7.5, "2": 10.0, "3": 10.0, "6": 12.0}[line]
    evening = {"1": 8.0, "4": 8.0, "5": 8.0, "2": 10.0, "3": 10.0, "6": 12.0}[line]
    late = {"1": 12.0, "4": 12.0, "5": 12.0, "2": 15.0, "3": 15.0, "6": 15.0}[line]
    m = minute
    if m < 6 * 60 + 30:
        return shoulder
    if m < 9 * 60 + 30:
        return peak
    if m < 10 * 60 + 30:
        return shoulder
    if m < 15 * 60 + 30:
        return midday
    if m < 18 * 60 + 30:
        return peak
    if m < 21 * 60:
        return evening
    return late


def tt_departures(line, plan):
    """Origin departures for the weekday: the morning exactly as the sim runs it from 05:30, earlier trains back to
    05:00 at the shoulder headway, the rest of the day to 00:45."""
    deps = []
    t = 5 * 60 + 30.0
    while t <= 24 * 60 + 45:
        deps.append(t)
        t += tt_headway(line, t, plan)
    sh = tt_headway(line, 5 * 60, plan)
    t = 5 * 60 + 30.0 - sh
    while t >= 5 * 60:
        deps.insert(0, t)
        t -= sh
    return deps


def _hms(m):
    sec = int(round(m * 60))
    return "%02d:%02d:%02d" % (sec // 3600, (sec % 3600) // 60, sec % 60)


def timetable_rows():
    rows = []
    for plan, tag in (("autumn2026", "AUT26"), ("spring2027", "SPR27")):
        for l in ("1", "2", "3", "4", "5", "6"):
            cars = W.CARS[plan][l]
            for d in W.LINES[l]["dirs"]:
                stations, offs = W.arrival_offsets(l, d)
                for k, dep in enumerate(tt_departures(l, plan)):
                    trip = "%s-%s%s-%03d" % (tag, l, d, k + 1)
                    for s in stations:
                        rows.append((tag, l, d, trip, s, _hms(dep + offs[s]), cars))
    return rows


# ------------------------------------------------------------------------------------------------- registers
CAP_COLS = ["platform_code", "complex_id", "complex", "platform", "rated_capacity", "effective_from", "effective_to",
            "basis"]


def _other_capacity(key):
    station, rest = key.split("|")
    h = K.stable_hash("cap", key) % 1000
    if len(rest) == 1:
        return 300 + 10 * (h % 16)
    return 240 + 10 * (h % 17)


def platform_code(key):
    if key in W.CODE:
        return W.CODE[key]
    station, rest = key.split("|")
    return "%s-%s" % (LEGACY_CODE[station], rest)


def capacity_rows():
    rows = []
    for s in W.COMPLEXES:
        for key, line, dirs in W.platforms_at(s):
            code = platform_code(key)
            cap = W.CAPACITY.get(key, _other_capacity(key))
            label = W._plat_label(key)
            if key == "Ferrier Square|4S":
                rows.append((code, W.COMPLEX_IDS[s], s, label, 330, "2019-07-01", "2026-09-13", "2019 rating"))
                rows.append((code, W.COMPLEX_IDS[s], s, label, 300, "2026-09-14", "2027-02-12",
                             "temporary: stair S5 closed for rebuilding"))
                rows.append((code, W.COMPLEX_IDS[s], s, label, 330, "2027-02-13", "", "2019 rating restored"))
                continue
            if s == "Sallow Park":
                rows.append((code, W.COMPLEX_IDS[s], s, label, cap, "2019-07-01", "", "2019 rating, confirmed 2026-08"))
                continue
            rows.append((code, W.COMPLEX_IDS[s], s, label, cap, "2019-07-01", "", "2019 rating"))
    return rows


COMPLEX_COLS = ["complex_id", "complex", "lines", "legacy_codes", "notes"]


def complex_rows():
    rows = []
    for s in W.COMPLEXES:
        lines = ", ".join(W.lines_at(s))
        codes = LEGACY_CODE[s]
        note = ""
        if s == "Albrecht Place":
            codes += "; KEN"
            note = "Kennet Street (KEN) joined to Albrecht Place by passage 2024-03-04"
        rows.append((W.COMPLEX_IDS[s], s, lines, codes, note))
    return rows


FLEET_COLS = ["series", "builder", "delivered", "cars_owned", "lines", "car_length_m", "seats_per_car",
              "max_load_per_car", "planning_load_per_car"]


def fleet_rows():
    return [
        ("R68", "Pullman-Standard", "1968-1972", 312, "1, 4", 18.3, 44, 150, 110),
        ("R74", "Budd", "1973-1975", 184, "2, 3", 18.3, 44, 150, 110),
        ("M04", "Kawasaki", "2003-2004", 132, "5", 18.0, 40, 150, 110),
        ("M09", "Bombardier", "2008-2009", 96, "6", 18.0, 40, 150, 110),
        ("M26", "Kawasaki", "2026-06 to 2026-12", 56, "5", 18.0, 40, 150, 110),
    ]


CHANGE_COLS = ["ref", "effective", "scope", "change"]


def change_rows():
    return [
        ("SC-2024-03", "2024-03-04", "Albrecht Place", "Kennet Street joined to Albrecht Place by the new passage; one complex, one complex id from the back office's start"),
        ("SC-2024-06", "2024-06-03", "fare system", "back office parallel run with the legacy system (legacy remains system of record)"),
        ("SC-2024-07", "2024-07-01", "fare system", "back office becomes system of record; legacy register reads end 2024-06-30"),
        ("SC-2025-09", "2025-09-02", "Line 6", "peak headway 7.5 minutes (was 8)"),
        ("SC-2026-09a", "2026-09-08", "all lines", "autumn 2026 pick: service plan autumn 2026"),
        ("SC-2026-09b", "2026-09-14", "Ferrier Square", "stair S5 (Line 4 southbound) closed for rebuilding to 2027-02-12"),
        ("SC-2026-12", "2026-12-21", "all lines", "winter 2026-27 pick: service plan as autumn 2026"),
        ("SC-2027-03a", "2027-03-01", "all lines", "spring 2027 pick: service plan spring 2027"),
        ("SC-2027-03b", "2027-03-01", "Line 5", "eight-car trains in all service (M04 with M26 cars)"),
    ]


# ------------------------------------------------------------------------------------------------- dashboard
DASH_COLS = ["month", "complex_id", "complex", "avg_weekday_entries", "status"]


def dashboard_rows(fare_rows):
    """The ridership dashboard: each complex's average weekday entries by month, service days 03:00 to 02:59 local,
    federal holidays out, rounded to tens; the latest month preliminary."""
    from collections import defaultdict
    tot = defaultdict(int)
    for (t_utc, cid, n, *_r) in fare_rows:
        # local time
        off = 4
        loc = t_utc - dt.timedelta(hours=off)
        off = K.us_eastern_offset(loc.date(), loc.hour)
        loc = t_utc - dt.timedelta(hours=off)
        sd = loc.date() if loc.hour >= 3 else loc.date() - dt.timedelta(days=1)
        tot[(cid, sd)] += n
    days = defaultdict(list)
    for (cid, sd), n in tot.items():
        if sd.weekday() < 5 and sd not in K.HOLIDAYS and sd >= dt.date(2025, 1, 1):
            days[(cid, sd.strftime("%Y-%m"))].append(n)
    rows = []
    name = {W.COMPLEX_IDS[s]: s for s in W.COMPLEXES}
    for (cid, m), xs in sorted(days.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        if m > "2026-12":
            continue
        avg = int(round(sum(xs) / len(xs) / 10.0) * 10)
        rows.append((m, cid, name[cid], avg, "preliminary" if m == "2026-12" else "final"))
    return rows


# ------------------------------------------------------------------------------------------------- inventory
INV_COLS = ["unit", "complex_id", "complex", "type", "from_area", "to_area", "width", "width_unit", "direction",
            "speed_mps", "installed", "surveyed"]


def _installed(e):
    lines = [l for l in W.lines_at(e["complex"])]
    if e["unit_sys"] == "mm" or (e["kind"] == "elevator" and e["to"].startswith(("Line 5", "Line 6"))):
        return "2004" if "5" in lines else "2009"
    if e["kind"] == "elevator":
        return str(1996 + (K.stable_hash("lift", e["unit"]) % 14))
    if e["kind"] == "escalator":
        return str(1969 + (K.stable_hash("esc", e["unit"]) % 6))
    return str(1968 + (K.stable_hash("st", e["unit"]) % 7))


def inventory_rows():
    rows = []
    for e in W.ELEMENTS:
        w = e["width"] if e["kind"] != "elevator" else ""
        sp = W.SPEED_DESIGN if e["kind"] == "escalator" else ""
        rows.append((e["unit"], W.COMPLEX_IDS[e["complex"]], e["complex"], e["kind"], e["frm"], e["to"], w,
                     e["unit_sys"], e["direction"], sp, _installed(e), "2025-03"))
    return rows


ASSET_COLS = ["asset_no", "unit", "manufacturer", "model", "step_width_mm", "speed_mps", "rise_m", "installed",
              "last_overhaul"]


def asset_rows():
    rows = []
    n = 0
    for e in W.ELEMENTS:
        if e["kind"] != "escalator":
            continue
        n += 1
        step = W.step_mm(e)
        inst = _installed(e)
        if e["unit_sys"] == "in":
            maker, model = ("Westinghouse", "Type MS")
            ov = str(2010 + K.stable_hash("ov", e["unit"]) % 9)
        else:
            maker, model = ("Otis", "506 NCE")
            ov = ""
        rise = round(4.2 + (K.stable_hash("rise", e["unit"]) % 50) / 10.0, 1)
        rows.append(("ES-%04d" % (1100 + n * 7), e["unit"], maker, model, step, W.SPEED_SET[e["unit_sys"]], rise,
                     inst, ov))
    return rows


# ------------------------------------------------------------------------------------------------- escalator log
CTRL_COLS = ["event_utc", "unit", "event"]
CTRL_PERIOD = (dt.date(2026, 9, 1), dt.date(2026, 12, 31))


def _utc(d, minute):
    """Local minute after midnight of date d (may exceed 24 h) to a naive UTC datetime."""
    day = d + dt.timedelta(days=int(minute // (24 * 60)))
    m = minute % (24 * 60)
    off = K.us_eastern_offset(day, int(m // 60))
    return dt.datetime.combine(day, dt.time(0)) + dt.timedelta(minutes=m + off * 60)


def _weekday_tt(d):
    return d.weekday() < 5 and d not in K.HOLIDAYS


def controller_rows():
    rows = []
    for e in W.ELEMENTS:
        if e["kind"] != "escalator":
            continue
        r = _rng("ctrl", e["unit"])
        base = e["direction"]
        am = e.get("am", base)
        for d in K.daterange(*CTRL_PERIOD):
            on = 4 * 60 + 50 + r.uniform(0, 14)
            rows.append((_utc(d, on), e["unit"], "RUN " + base.upper()))
            cur = base
            ev = []
            if _weekday_tt(d) and am != base:
                t1 = 6 * 60 + 8 + r.uniform(0, 30)
                t2 = 9 * 60 + 34 + r.uniform(0, 30)
                ev += [(t1, "STOP"), (t1 + r.uniform(0.4, 1.6), "RUN " + am.upper()),
                       (t2, "STOP"), (t2 + r.uniform(0.4, 1.6), "RUN " + base.upper())]
            # faults: about one in three weeks
            if r.random() < 0.05:
                tf = 5 * 60 + r.uniform(30, 19 * 60)
                dur = 20 + r.exponential(70)
                ev += [(tf, "FAULT"), (tf + dur, "RESET")]
            ev.sort()
            for t, what in ev:
                if what == "RESET":
                    # back to the direction it was set to before the fault
                    what = "RUN " + cur.upper()
                if what.startswith("RUN "):
                    cur = what[4:].lower()
                rows.append((_utc(d, t), e["unit"], what))
            off = 24 * 60 + 60 + r.uniform(0, 20)
            rows.append((_utc(d, off), e["unit"], "STOP"))
    rows.sort(key=lambda x: (x[0], x[1]))
    return rows


# ------------------------------------------------------------------------------------------------- elevators
WO_COLS = ["wo", "unit", "complex_id", "complex", "type", "problem", "out_of_service_at", "in_service_at"]
MON_COLS = ["event_utc", "unit", "mode"]
LIFT_PERIOD = (dt.date(2026, 9, 1), dt.date(2026, 12, 31))
_PROBLEMS = ["door operator fault", "car door reopening", "leveling fault", "hall call buttons", "drive fault",
             "door interlock", "car stuck between floors", "hydraulic pressure", "emergency phone fault"]


def elevator_records():
    """(work orders, monitoring events) for every elevator, 1 September to 31 December 2026. A fault stops the car;
    the control centre opens the work order when the station reports it; the mechanic takes the car on independent
    service, and returns it to normal service when the repair is done, or shuts it down to wait for a part."""
    wos, mon = [], []
    n = 0
    for e in W.ELEMENTS:
        if e["kind"] != "elevator":
            continue
        s = e["complex"]
        r = _rng("lift", e["unit"])
        rate = (1.0 / (14 * 20 * 60)) * (1.7 if s in W.WATCH_COMPLEXES else 1.0)   # per operating minute
        busy_until = None
        events = []
        for d in K.daterange(*LIFT_PERIOD):
            # planned maintenance, one weekday a month, the mechanic working the car on inspection
            if d.day == 6 + (K.stable_hash("pm", e["unit"]) % 18) and d.weekday() < 5:
                t0 = 6 * 60 + r.uniform(0, 9 * 60)
                t1 = t0 + 55 + r.uniform(0, 50)
                events.append(("PM", d, t0, None, t0, None, t1))
            k = r.poisson(rate * 20 * 60)
            for _ in range(int(k)):
                t0 = 5 * 60 + r.uniform(0, 20 * 60)
                rep = 4 + r.exponential(12)
                arr = rep + 15 + r.exponential(35)
                fix = r.lognormal(math.log(45), 0.5)
                parts = r.random() < 0.12
                events.append(("CM", d, t0, t0 + rep, t0 + arr, parts, t0 + arr + fix))
        events.sort(key=lambda x: (x[1], x[2]))
        for (kind, d, t0, trep, tind, parts, tend) in events:
            start = _utc(d, t0)
            if busy_until is not None and start <= busy_until:
                continue
            n += 1
            wo = "WO-26-%05d" % (20000 + n * 3 + (K.stable_hash("wo", e["unit"]) % 3))
            if kind == "PM":
                # inspection operation is not one of the modes the remote monitoring reports
                wos.append((wo, e["unit"], W.COMPLEX_IDS[s], s, "PM", "planned maintenance", _utc(d, t0), _utc(d, tend)))
                busy_until = _utc(d, tend)
                continue
            mon.append((_utc(d, t0), e["unit"], "FAULT"))
            mon.append((_utc(d, tind), e["unit"], "INDEPENDENT"))
            if parts:
                tsd = tind + 25 + r.uniform(0, 40)
                mon.append((_utc(d, tsd), e["unit"], "SHUTDOWN"))
                nd = d + dt.timedelta(days=1)
                while not _weekday_tt(nd):
                    nd += dt.timedelta(days=1)
                tb = 9 * 60 + r.uniform(0, 150)
                mon.append((_utc(nd, tb), e["unit"], "INDEPENDENT"))
                tret = tb + 60 + r.uniform(0, 80)
                mon.append((_utc(nd, tret), e["unit"], "NORMAL"))
                end = _utc(nd, tret)
                prob = "awaiting part: " + _PROBLEMS[int(r.integers(0, len(_PROBLEMS)))]
            else:
                mon.append((_utc(d, tend), e["unit"], "NORMAL"))
                end = _utc(d, tend)
                prob = _PROBLEMS[int(r.integers(0, len(_PROBLEMS)))]
            wos.append((wo, e["unit"], W.COMPLEX_IDS[s], s, "CM", prob, _utc(d, trep), end))
            busy_until = end
    wos.sort(key=lambda x: (x[6], x[1]))
    # work order numbers run in the order the control centre opened them, shared with the escalator and other
    # station equipment work orders the export leaves out
    g = _rng("wo-numbers")
    num = 31408
    renum = []
    for w in wos:
        num += 1 + int(g.integers(0, 6))
        renum.append(("WO-%d" % num,) + w[1:])
    mon.sort(key=lambda x: (x[0], x[1]))
    return renum, mon
