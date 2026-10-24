"""Every graded figure from the pack alone: the call (the resident route and the golden, which carries the holiday
parks as origins), and the three asks. Reads only the files in target/."""
import collections
import csv
import datetime as dt
import io
import math
import os
import zipfile
import zoneinfo

import numpy as np
from openpyxl import load_workbook

import params as P

LONDON = zoneinfo.ZoneInfo("Europe/London")
UTC = dt.timezone.utc
OFF = ("2025-11", "2025-12", "2026-01", "2026-02")


def rd(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def sheet(path, name):
    ws = load_workbook(path, read_only=True, data_only=True)[name]
    it = ws.iter_rows(values_only=True)
    head = next(it)
    return [dict(zip(head, r)) for r in it if any(v is not None for v in r)]


class Pack:
    def __init__(self, target):
        F = {k: os.path.join(target, v) for k, v in P.FILES.items()}
        self.F = F
        hh = {r["geography code"]: int(r["Number of households"]) for r in rd(F["households"])}
        pwc = {r["OA21CD"]: (float(r["x"]), float(r["y"])) for r in rd(F["pwc"])}
        spend = {r["OA21CD"]: float(r["AvgWeeklyGrocerySpendPerHousehold_GBP_2026"]) for r in rd(F["spend"])}
        self.oas = [(pwc[k], hh[k] * spend[k] * 52 * P.INSTORE) for k in sorted(hh)]
        self.pc = {r["pcds"]: (float(r["oseast1m"]), float(r["osnrth1m"])) for r in rd(F["onspd"])}
        with open(F["voa_list"], encoding="utf-8", newline="") as fh:
            self.voa = [ln.rstrip("\r\n").split("*") for ln in fh if ln.strip()]
        self.smv = {r["uarn"]: (float(r["main_measure"]), r["unit_of_measurement"]) for r in rd(F["voa_smv"])}
        self.estate = sheet(F["estate"], "Stores")
        self.sites = sheet(F["shortlist"], "Shortlist")
        own_pc = {r["postcode"]: str(r["store_no"]) for r in self.estate}
        self.stores = []
        self.parks = []
        for r in self.voa:
            desc, uarn, pc = r[5], r[6], r[14]
            if desc in P.GROCERY and uarn in self.smv and self.smv[uarn][1] == "m2" and self.smv[uarn][0] >= P.MIN_AREA:
                self.stores.append(dict(id=own_pc.get(pc, "u" + uarn), own=pc in own_pc, xy=self.pc[pc], a=self.smv[uarn][0]))
            if uarn in self.smv and self.smv[uarn][1] == "pitches":
                self.parks.append(dict(uarn=uarn, desc=desc, pc=pc, xy=self.pc[pc], n=self.smv[uarn][0]))
        self.cards = rd(F["cards"])

    # ------------------------------------------------------------- the spend-share model
    @staticmethod
    def shares(xy, S):
        X = np.array([s["xy"][0] for s in S]); Y = np.array([s["xy"][1] for s in S])
        A = np.array([s["a"] for s in S], float) ** P.ALPHA
        w = A * np.exp(-P.BETA * P.ROADF * np.hypot(X - xy[0], Y - xy[1]) / 1000.0)
        return w / w.sum()

    def sales(self, S, origins):
        out = np.zeros(len(S))
        for xy, d in origins:
            out += d * self.shares(xy, S)
        return out

    def guests(self, off=OFF, gross=True, stores=None):
        """the guests' in-store spend at each of our stores: out-of-region card spend in the season above the store's
        own November to February level, grossed up by the store's card share"""
        share = {str(r["store_no"]): float(r["card_share_of_sales"]) for r in self.estate}
        nl = {}
        for r in self.cards:
            if not r["cardholder_home_sector"].startswith(P.AREA):
                nl.setdefault(r["store_no"], {}).setdefault(r["month"], 0.0)
                nl[r["store_no"]][r["month"]] += float(r["spend_gbp"])
        out = {}
        for s, mm in nl.items():
            level = np.mean([mm.get(m, 0.0) for m in off]) if off else 0.0
            season = [m for m in P.MONTHS if int(m[5:]) in P.SEASON]
            g = sum(mm.get(m, 0.0) - level for m in season)
            out[s] = g / (share[s] if gross else 1.0)
        return out

    def v_per_pitch(self, guests=None, parks=None, only=None):
        guests = guests if guests is not None else self.guests()
        parks = parks if parks is not None else self.parks
        own = [k for k, s in enumerate(self.stores) if s["own"] and (only is None or s["id"] in only)]
        den = 0.0
        for p in parks:
            sh = self.shares(p["xy"], self.stores)
            den += p["n"] * sum(sh[k] for k in own)
        num = sum(v for s, v in guests.items() if only is None or s in only)
        return num / den

    def appraise(self, V=None, parks=None, margin=P.MARGIN):
        """each site's addition: 26 per cent of its sales less 26 per cent of what it takes from our ten stores, less
        its running costs; V None is the resident route"""
        parks = parks if parks is not None else self.parks
        origins = list(self.oas) + ([(p["xy"], p["n"] * V) for p in parks] if V else [])
        S = self.stores
        own = [k for k, s in enumerate(S) if s["own"]]
        base = self.sales(S, origins)
        out = {}
        for r in self.sites:
            S2 = S + [dict(id=r["site"], own=True, xy=self.pc[r["postcode"]], a=float(r["proposed_floor_area_m2"]))]
            b2 = self.sales(S2, origins)
            took = sum(base[k] - b2[k] for k in own)
            cost = sum(float(r[c]) for c in ("rent_gbp", "business_rates_gbp", "staffing_gbp", "other_running_gbp"))
            out[r["site"]] = dict(new=b2[-1], took=took, cost=cost, add=margin * (b2[-1] - took) - cost)
        return out

    def call(self):
        V = self.v_per_pitch()
        g = self.appraise(V)
        r0 = self.appraise(None)
        win = max(g, key=lambda k: g[k]["add"])
        return dict(V=V, golden=g, resident=r0, site=win, add=g[win]["add"],
                    resident_site=max(r0, key=lambda k: r0[k]["add"]))


# ----------------------------------------------------------------- ask A
def to_local(s):
    t = dt.datetime.strptime(s, "%Y-%m-%d %H:%M").replace(tzinfo=UTC)
    return t.astimezone(LONDON).replace(tzinfo=None)


def _utc(s):
    return dt.datetime.strptime(s, "%Y-%m-%d %H:%M")


def turned_away(rows):
    """the deliveries a store turned away: the stop closed sooner than its cases could have come off the trailer
    (under 4 minutes plus 0.02 of a minute a case), the same cases going to the store again the next day"""
    out = set()
    for r in rows:
        if r["stop_type"] == "DEL":
            dwell = (_utc(r["depart_utc"]) - _utc(r["arrive_utc"])).total_seconds() / 60.0
            if dwell < 4 + 0.02 * int(r["cases"]):
                out.add((r["trip_id"], r["stop_seq"]))
    return out


def ask_a(target, mode="golden"):
    """the cases the DC delivered to each store a week over the 25 weeks, by the stop's UK arrival date: a load a store
    turned away is delivered once, by the next day's trip"""
    rows = rd(os.path.join(target, P.FILES["tms"]))
    dels = [r for r in rows if r["stop_type"] == "DEL" and r["status"] == "COMPLETE"]
    drop = set()
    if mode in ("golden", "utc"):
        drop = turned_away(dels)
    elif mode == "drop_short":
        drop = {(r["trip_id"], r["stop_seq"]) for r in dels
                if (_utc(r["depart_utc"]) - _utc(r["arrive_utc"])).total_seconds() / 60.0 < 15}
    elif mode == "dedup_equal":
        seen = {}
        for r in sorted(dels, key=lambda r: r["arrive_utc"]):
            d = to_local(r["arrive_utc"]).date()
            k = (r["store_no"], r["cases"])
            if k in seen and (d - seen[k]).days == 1:
                drop.add((r["trip_id"], r["stop_seq"]))
            seen[k] = d
    tot = {}
    for r in dels:
        if (r["trip_id"], r["stop_seq"]) in drop:
            continue
        d = to_local(r["arrive_utc"]).date() if mode != "utc" else _utc(r["arrive_utc"]).date()
        if P.TMS_FROM <= d <= P.TMS_TO:
            tot[r["store_no"]] = tot.get(r["store_no"], 0) + int(r["cases"])
    weeks = ((P.TMS_TO - P.TMS_FROM).days + 1) / 7.0
    return {k: v / weeks for k, v in tot.items()}


# ----------------------------------------------------------------- ask B
def wfm_lines(target):
    """the paid hours report's lines in file order: colleague, location, date, role and paid hours"""
    return [dict(r, i=i, paid=float(r["paid_hours"])) for i, r in enumerate(rd(os.path.join(target, P.FILES["wfm"])))]


def punches_by_employee(target):
    reg = {r["terminal_id"]: r["store_no"] for r in rd(os.path.join(target, P.FILES["terminals"]))}
    out = {}
    for p in rd(os.path.join(target, P.FILES["punches"])):
        out.setdefault(p["employee_no"], []).append(
            (dt.datetime.strptime(p["punch_time"], "%Y-%m-%d %H:%M"), p["punch"], reg[p["terminal_id"]]))
    for v in out.values():
        v.sort()
    return out


def punch_shifts(pun):
    """each colleague's shifts as the terminals recorded them: a clock-in and the clock-out after it are one shift, a
    clock-in with no clock-out or a clock-out with no clock-in is a shift whose other punch was forgotten. Each shift
    is dated by its clock-in (by its clock-out where there is none) and placed at that punch's store"""
    out = {}
    for e, ps in pun.items():
        opened = None
        for t, kind, store in ps:
            if kind == "IN":
                if opened is not None:
                    out.setdefault((e, opened[0].date().isoformat()), []).append(opened[1])
                opened = (t, store)
            else:
                if opened is not None and (t - opened[0]).total_seconds() <= 16 * 3600:
                    out.setdefault((e, opened[0].date().isoformat()), []).append(opened[1])
                else:
                    if opened is not None:
                        out.setdefault((e, opened[0].date().isoformat()), []).append(opened[1])
                    out.setdefault((e, t.date().isoformat()), []).append(store)
                opened = None
        if opened is not None:
            out.setdefault((e, opened[0].date().isoformat()), []).append(opened[1])
    return out


def _by_day(lines):
    g = {}
    for r in lines:
        g.setdefault((r["employee_no"], r["date"]), []).append(r)
    return g


def _day_store(pun):
    """the store of a colleague's first punch on each date, whatever the punch"""
    out = {}
    for e, ps in pun.items():
        for t, kind, store in ps:
            out.setdefault((e, t.date().isoformat()), store)
    return out


def ask_b(target, mode="golden"):
    """paid hours a week worked at each store over the 25 weeks: each shift worked once, at the hours it was paid, at
    the store its colleague clocked in at. The report lists a night shift against both dates it covers, so the lines
    a colleague has on a date are the shifts that start that date and any night that ended there; the shifts that
    start a date are the ones the terminals recorded starting it"""
    lines = wfm_lines(target)
    pun = punches_by_employee(target)
    tot = {}

    def add(store, h):
        tot[store] = tot.get(store, 0.0) + h
    if mode == "punch_hours":
        for e, ps in pun.items():
            for (t0, k0, s0), (t1, k1, s1) in zip(ps, ps[1:]):
                if k0 == "IN" and k1 == "OUT":
                    add(s0, (t1 - t0).total_seconds() / 3600.0)
        return {s: v / 25.0 for s, v in tot.items()}
    if mode == "location":
        for r in lines:
            add(r["location"], r["paid"])
        return {s: v / 25.0 for s, v in tot.items()}
    day = _day_store(pun)
    if mode in ("golden", "in_days", "exact_in_days"):
        starts = punch_shifts(pun)
        ins = {}
        for e, ps in pun.items():
            for t, kind, store in ps:
                if kind == "IN":
                    ins.setdefault((e, t.date().isoformat()), []).append(store)
        use = lines
        if mode == "exact_in_days":
            seen, use = set(), []
            for r in lines:
                k = (r["employee_no"], r["location"], r["date"], r["role"], r["paid_hours"])
                if k not in seen:
                    seen.add(k)
                    use.append(r)
        for key, g in _by_day(use).items():
            stores = starts.get(key, []) if mode == "golden" else ins.get(key, [])
            for r, store in zip(g, stores):
                add(store, r["paid"])
        return {s: v / 25.0 for s, v in tot.items()}
    if mode == "dedup_exact":
        seen, use = set(), []
        for r in lines:
            k = (r["employee_no"], r["location"], r["date"], r["role"], r["paid_hours"])
            if k not in seen:
                seen.add(k)
                use.append(r)
    elif mode == "dedup_day":
        use = [g[0] for g in _by_day(lines).values()]
    elif mode == "dedup_day_max":
        use = [max(g, key=lambda r: r["paid"]) for g in _by_day(lines).values()]
    else:                                   # "terminal_all": every line
        use = lines
    for r in use:
        add(day.get((r["employee_no"], r["date"]), r["location"]), r["paid"])
    return {s: v / 25.0 for s, v in tot.items()}


# ----------------------------------------------------------------- ask C
def _mins(t):
    h, m, s = (int(x) for x in t.split(":"))
    return 60 * h + m


def ask_c(target, mode="golden", day=P.BUS_DAY):
    """bus departures on the day, by the clock, from stops within 400 metres of each site: the day's own services up
    to midnight and the previous day's services after it (a GTFS service day runs past 24:00), no departure from a
    stop where the bus only sets down, and each bus once: a bus is its vehicle block, so a journey listed twice on the
    same block (both operators' feeds carry the jointly run routes, and one operator's Friday-late timetable repeats
    the evening's weekday journeys) is one departure, while a second bus on the same timetable (a school-day duplicate
    on a block of its own) is another"""
    import geo
    sites = sheet(os.path.join(target, P.FILES["shortlist"]), "Shortlist")
    pc = {r["pcds"]: (float(r["oseast1m"]), float(r["osnrth1m"])) for r in rd(os.path.join(target, P.FILES["onspd"]))}
    site_ll = {r["site"]: geo.bng_to_wgs84(*pc[r["postcode"]]) for r in sites}
    late = mode not in ("naive", "half")
    days = [(day, "today")] + ([(day - dt.timedelta(days=1), "eve")] if late else [])
    calls = []                      # (feed, site, which, route, direction, stop, minute, block)
    for fi, key in enumerate(("gtfs_lb", "gtfs_pdc")):
        with zipfile.ZipFile(os.path.join(target, P.FILES[key])) as z:
            R = lambda n: list(csv.DictReader(io.TextIOWrapper(z.open(n), encoding="utf-8")))
            cal = R("calendar.txt")
            cds = R("calendar_dates.txt")
            routes = {r["route_id"]: r["route_short_name"] for r in R("routes.txt")}
            trips = R("trips.txt")
            stops = {r["stop_id"]: (float(r["stop_lat"]), float(r["stop_lon"])) for r in R("stops.txt")}
            near = {k: {sid for sid, ll in stops.items() if geo.haversine_m(ll[0], ll[1], *site_ll[k]) <= P.BUS_RADIUS}
                    for k in site_ll}
            st = R("stop_times.txt")
            for d, which in days:
                ymd, dow = d.strftime("%Y%m%d"), d.strftime("%A").lower()
                on = {r["service_id"] for r in cal if r[dow] == "1" and r["start_date"] <= ymd <= r["end_date"]}
                for r in cds:
                    if r["date"] == ymd:
                        (on.add if r["exception_type"] == "1" else on.discard)(r["service_id"])
                if mode == "no_fl":
                    fri = {r["service_id"] for r in cal if r["friday"] == "1" and r["monday"] == "0" and r["saturday"] == "0"}
                    on -= fri
                tr = {r["trip_id"]: (routes[r["route_id"]], r["direction_id"], r["block_id"]) for r in trips
                      if r["service_id"] in on}
                for r in st:
                    if r["trip_id"] not in tr or (r["pickup_type"] == "1" and mode != "all_calls"):
                        continue
                    m = _mins(r["departure_time"])
                    if which == "today" and mode != "naive" and m >= 1440:
                        continue
                    if which == "eve" and m < 1440:
                        continue
                    route, direction, block = tr[r["trip_id"]]
                    for k in site_ll:
                        if r["stop_id"] in near[k]:
                            calls.append((fi, k, which, route, direction, r["stop_id"], m, block))
    out = {k: 0 for k in site_ll}
    if mode in ("golden", "all_calls", "no_fl"):
        for c in set(c[1:3] + c[5:8] for c in calls):
            out[c[0]] += 1
        return out
    if mode == "nodedup":
        for c in calls:
            out[c[1]] += 1
        return out
    if mode in ("set", "naive", "half"):
        for c in set(c[1:7] for c in calls):
            out[c[0]] += 1
        return out
    # "maxfeed": each feed's calls counted, the larger of the two feeds' counts taken for each route, stop and time
    per = [collections.Counter(c[1:7] for c in calls if c[0] == fi) for fi in (0, 1)]
    for key in set(per[0]) | set(per[1]):
        out[key[0]] += max(per[0][key], per[1][key])
    return out
