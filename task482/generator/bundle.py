"""Reads task482's pack as a solver holds it (target/ only) and computes every graded figure from it: each station's
monthly availability under Schedule C, the priority stations, the station that cleared the line by the least, each
station's Q4 pay-station card sales and the service hours its pay station could not take a card payment. It also
computes the rungs a solver can stop on, for the checks, the verifier and the ceiling script.

Nothing here imports the simulation: what it knows comes from the files."""
import bisect
import csv
import datetime as dt
import os
import re
from collections import defaultdict

import numpy as np

FILES = {
    "status": "wellhaven_station_status_archive_2026q4.csv",
    "notes": "station_status_archive_notes.pdf",
    "trips": "northlane_trips_2026q4.csv",
    "moves": "northlane_fleet_moves_2026q4.csv",
    "reports": "northlane_rider_fault_reports_2026q4.csv",
    "gbfs": "gbfs_station_information_2027-01-11.json",
    "stations": "wellhaven_bike_share_station_list.xlsx",
    "agreement": "bike_share_operating_agreement_schedules.pdf",
    "sales": "paystation_sales_2026q4.csv",
    "alarms": "paystation_alarm_log_2026q4.csv",
    "workorders": "paystation_work_orders_2026q4.xlsx",
    "register": "paystation_register_2027-01-08.xlsx",
    "weather": "wellhaven_daily_weather_2026q4.csv",
    "report": "northlane_wellhaven_quarterly_report_2026q4.pdf",
}
UTC = dt.timezone.utc
FALLBACK = dt.datetime(2026, 11, 1, 6, 0, tzinfo=UTC)          # 2:00 EDT, clocks back to 1:00 EST
ORIGIN = dt.datetime(2026, 9, 24, 0, 0, tzinfo=UTC)            # 20:00 on 23 September, where the records start
MONTHS = (10, 11, 12)
LINE = 90.0


def utc_of_local(t, second=False):
    """Eastern wall-clock time to UTC; in the repeated hour of 1 November the first (EDT) unless second"""
    edt = (t + dt.timedelta(hours=4)).replace(tzinfo=UTC)
    est = (t + dt.timedelta(hours=5)).replace(tzinfo=UTC)
    if edt < FALLBACK and est >= FALLBACK and second:
        return est
    return edt if edt < FALLBACK else est


def to_local(u):
    off = -4 if u < FALLBACK else -5
    return (u + dt.timedelta(hours=off)).replace(tzinfo=None)


def parse_local(s):
    return dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


def parse_z(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


def minute_index(u):
    """the grid minute whose start is u or the first start after it (a state set at u holds from that minute)"""
    s = (u - ORIGIN).total_seconds()
    k = int(s // 60)
    return k if s == k * 60 else k + 1


def month_service_minutes(mo):
    """grid minute indices of the minutes of service hours (6:00 to midnight Eastern) in a month of Q4 2026"""
    out = []
    d = dt.date(2026, mo, 1)
    while d.month == mo:
        a = utc_of_local(dt.datetime(d.year, d.month, d.day, 6, 0))
        b = utc_of_local(dt.datetime(d.year, d.month, d.day) + dt.timedelta(days=1))
        out.append(np.arange(minute_index(a), minute_index(b)))
        d += dt.timedelta(days=1)
    return np.concatenate(out)


SERVICE = {mo: month_service_minutes(mo) for mo in MONTHS}
EXTRACT = dt.datetime(2027, 1, 11, 1, 0, tzinfo=UTC)          # 20:00 on 10 January, where they end
GRID = minute_index(EXTRACT) + 2


def rows(target, key):
    with open(os.path.join(target, FILES[key]), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def sheet(target, key, name):
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, FILES[key]), read_only=True, data_only=True)
    ws = wb[name]
    it = ws.iter_rows(values_only=True)
    head = [str(h) for h in next(it)]
    out = [dict(zip(head, r)) for r in it if any(v is not None for v in r)]
    wb.close()
    return out


def pdf_text(target, key):
    from pypdf import PdfReader
    return "\n".join(p.extract_text() for p in PdfReader(os.path.join(target, FILES[key])).pages)


def bike_no(s):
    return int(re.sub(r"\D", "", str(s)))


class Inputs:
    def __init__(self, target, dedup=True, staff=True):
        self.target = target
        st = sheet(target, "stations", "Stations")
        self.city = {}            # feed station id -> City station number
        self.name = {}            # City station number -> name
        for r in st:
            no = int(str(r["Station"]).split("-")[1])
            self.city[int(r["Feed station ID"])] = no
            self.name[no] = r["Name"]
        self.nos = sorted(self.name)
        # trips, the re-run week's repeats dropped (the same trip id, every field the same)
        seen = set()
        self.trips = []
        self.dup_rows = 0
        for r in rows(target, "trips"):
            key = tuple(r.values())
            if key in seen:
                self.dup_rows += 1
                if dedup:
                    continue
            seen.add(key)
            if not staff and r["rider_type"] == "staff":
                continue
            a_l, b_l = parse_local(r["start_time"]), parse_local(r["end_time"])
            dur = int(r["duration_s"])
            a = b = None
            for x in (utc_of_local(a_l), utc_of_local(a_l, True)):
                for y in (utc_of_local(b_l), utc_of_local(b_l, True)):
                    if (y - x).total_seconds() == dur:
                        a, b = x, y
                        break
                if a:
                    break
            assert a is not None, r
            self.trips.append(dict(id=int(r["trip_id"]), bike=int(r["bike_id"]), a=a, b=b,
                                   s0=int(r["start_station_id"]), s1=int(r["end_station_id"]), who=r["rider_type"]))
        self.moves = []
        for r in rows(target, "moves"):
            self.moves.append(dict(t=utc_of_local(parse_local(r["logged_at"])), van=r["vehicle"], s=int(r["station_id"]),
                                   act="pickup" if r["action"] == "Pick up" else "drop", bike=bike_no(r["bike"])))
        self.reports = [dict(t=parse_z(r["reported_at"]), bike=int(r["bike_id"]), s=int(r["station_id"]))
                        for r in rows(target, "reports")]

    # ------------------------------------------------------------------------------------------------- spells
    def events(self):
        ev = defaultdict(list)
        for k, t in enumerate(self.trips):
            ev[t["bike"]].append((t["a"], 2, "rent", t["s0"], k))
            ev[t["bike"]].append((t["b"], 1, "dock", t["s1"], k))
        for k, m in enumerate(self.moves):
            ev[m["bike"]].append((m["t"], 0 if m["act"] == "pickup" else 1, m["act"], m["s"], k))
        for b in ev:
            ev[b].sort(key=lambda e: (e[0], e[1], e[4]))
        return ev

    def spells(self):
        """each bike's spells docked at a station: (bike, feed station, from, to, how it ended, back on the street).
        A bike whose first record takes it from a station was docked there from the start of the records."""
        out = []
        for b, seq in self.events().items():
            cur, a = None, None
            if seq[0][2] in ("rent", "pickup"):
                cur, a = seq[0][3], ORIGIN
            for i, (t, _, kind, s, _) in enumerate(seq):
                if kind in ("rent", "pickup"):
                    if cur is not None:
                        back = None
                        if kind == "pickup":
                            back = next((e[0] for e in seq[i + 1:] if e[2] in ("drop", "dock")), None)
                        out.append((b, cur, a, t, kind, back))
                    cur, a = None, None
                else:
                    cur, a = s, t
            if cur is not None:
                out.append((b, cur, a, None, "open", None))
        return out

    def rentals(self):
        out = defaultdict(list)
        for t in self.trips:
            out[t["s0"]].append(t["a"])
        for s in out:
            out[s].sort()
        return out


# ----------------------------------------------------------------------------------------------------- availability
def counts(I, spells, keep):
    """bikes docked at the start of each grid minute, per City station, over the spells keep() admits"""
    diff = {no: np.zeros(GRID + 1, dtype=np.int32) for no in I.nos}
    for sp in spells:
        if not keep(sp):
            continue
        b, s, a, z, kind, back = sp
        no = I.city[s]
        i = minute_index(a)
        j = minute_index(z) if z is not None else GRID
        if j > i:
            diff[no][i] += 1
            diff[no][j] -= 1
    return {no: np.cumsum(diff[no])[:GRID] for no in I.nos}


def availability(I, series):
    return {no: {mo: 100.0 * float((series[no][SERVICE[mo]] >= 1).mean()) for mo in MONTHS} for no in I.nos}


def designated(av, line=LINE):
    return sorted(no for no, d in av.items() if min(d.values()) < line)


def nearest_clear(av, line=LINE):
    """the station whose lowest month cleared the line by the least, and its margin in points"""
    clear = [(min(d.values()), no) for no, d in av.items() if min(d.values()) >= line]
    v, no = min(clear)
    return no, v - line


def broken_by_stay(I, hours=20.0):
    """the golden reading: a docked bike was out of working order from the end of the ride that left it until the
    van took it to the depot, where it stayed for repair (a day or more) before it was ridden or dropped again"""
    def f(sp):
        b, s, a, z, kind, back = sp
        if kind != "pickup":
            return False
        return back is None or (back - z).total_seconds() >= hours * 3600
    return f


def broken_by_pass(I):
    """a docked bike passed over by a renter at its station and then taken away by the van"""
    rent = I.rentals()

    def f(sp):
        b, s, a, z, kind, back = sp
        if kind != "pickup" or (back is not None and (back - z).total_seconds() < 3600):
            return False
        arr = rent.get(s, [])
        return bisect.bisect_left(arr, z) - bisect.bisect_right(arr, a) >= 1
    return f


def broken_by_pass_and_stay(I, hours=20.0):
    """the write-up's reading: passed over by a renter at its station, then taken by a van and kept at the depot
    a day or more"""
    a, b = broken_by_pass(I), broken_by_stay(I, hours)
    return lambda sp: a(sp) and b(sp)


def broken_by_van(I):
    """every bike a van took away rather than a rider, the station move's bikes excepted (back within the hour)"""
    def f(sp):
        b, s, a, z, kind, back = sp
        return kind == "pickup" and not (back is not None and (back - z).total_seconds() < 3600)
    return f


def working_counts(I, broken):
    sp = I.spells()
    return counts(I, sp, lambda x: not broken(x))


def golden(I):
    return availability(I, working_counts(I, broken_by_pass_and_stay(I)))


# ----------------------------------------------------------------------------------------------------- the default
def feed_counts(I, field="num_bikes_available"):
    """the archive's count at the start of each grid minute, per City station: each feed station's last row at or
    before the minute, carried across the spells the poller was down; a station that moved is read under its old
    feed ID until its new ID's first row"""
    by = defaultdict(list)
    for r in rows(I.target, "status"):
        t = dt.datetime.fromtimestamp(int(r["polled_at"]), UTC)
        by[int(r["station_id"])].append((minute_index(t), int(r[field])))
    first = {s: min(k for k, _ in lst) for s, lst in by.items()}
    stop = {}
    for s in by:
        later = [first[x] for x in by if x != s and I.city[x] == I.city[s] and first[x] > first[s]]
        stop[s] = min(later) if later else GRID
    out = {no: np.zeros(GRID, dtype=np.int32) for no in I.nos}
    for s, lst in by.items():
        no = I.city[s]
        lst.sort()
        for (k, v), nxt in zip(lst, lst[1:] + [(stop[s], None)]):
            hi = min(nxt[0], stop[s])
            if hi > k:
                out[no][k:hi] += v
    return out


def poller_gap_minutes(I):
    """grid minutes with no poll (the spells the notes list)"""
    polled = set()
    for r in rows(I.target, "status"):
        polled.add(minute_index(dt.datetime.fromtimestamp(int(r["polled_at"]), UTC)))
    return polled


def default(I):
    return availability(I, feed_counts(I))


# ----------------------------------------------------------------------------------------------------- ask A
QA = utc_of_local(dt.datetime(2026, 10, 1))
QB = utc_of_local(dt.datetime(2027, 1, 1))


def terminal_history(I):
    """each terminal's pay stations over time from the work orders: a list of (installed from, pay station number),
    the first entry (None) its pay station before the refurbishment; a terminal stays where it was installed until a
    work order installs it elsewhere"""
    wos = sheet(I.target, "workorders", "Work orders")
    swaps = sorted((r for r in wos if r["Work type"].startswith("Card terminal replacement")), key=lambda r: r["Opened"])
    hist = defaultdict(list)
    for r in swaps:
        no = int(r["Pay station"].split("-")[1])
        if not hist[r["Terminal removed"]]:
            hist[r["Terminal removed"]].append((None, no))
        hist[r["Terminal installed"]].append((r["Closed"], no))
    return hist


def placed(hist, ser, loc):
    """the pay station terminal ser was at, local time loc"""
    no = None
    for since, n in hist.get(ser, []):
        if since is None or since <= loc:
            no = n
    return no


def sales(I, attribution="history", tz="local", voids=True):
    hist = terminal_history(I)
    tot = defaultdict(float)
    vo = set()
    rs = rows(I.target, "sales")
    if voids:
        vo = {r["original_sale"] for r in rs if r["transaction"] == "VOID"}
    for r in rs:
        if r["transaction"] != "SALE" or r["sale_id"] in vo:
            continue
        u = parse_z(r["sold_at"])
        if tz == "local":
            if not (QA <= u < QB):
                continue
        else:
            if not (dt.datetime(2026, 10, 1, tzinfo=UTC) <= u < dt.datetime(2027, 1, 1, tzinfo=UTC)):
                continue
        if attribution == "column":
            no = int(r["pay_station"].split("-")[1])
        else:
            no = placed(hist, r["terminal"], to_local(u))
            assert no is not None, r
        tot[no] += float(r["amount"])
    return {no: round(tot[no], 2) for no in I.nos}


# ----------------------------------------------------------------------------------------------------- ask B
BLOCK = ("COMMS_LOST", "READER_FAULT")
CLEAR = {"COMMS_RESTORED": "COMMS_LOST", "READER_OK": "READER_FAULT"}


def service_windows(d0=dt.date(2026, 10, 1), d1=dt.date(2026, 12, 31)):
    out = []
    d = d0
    while d <= d1:
        out.append((utc_of_local(dt.datetime(d.year, d.month, d.day, 6, 0)),
                    utc_of_local(dt.datetime(d.year, d.month, d.day) + dt.timedelta(days=1))))
        d += dt.timedelta(days=1)
    return out


WINDOWS = service_windows()


def union(spans):
    out = []
    for a, b in sorted(spans):
        if out and a <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def in_service_s(spans, windows=WINDOWS):
    tot = 0.0
    for a, b in spans:
        for x, y in windows:
            lo, hi = max(a, x), min(b, y)
            if hi > lo:
                tot += (hi - lo).total_seconds()
    return tot


def down_spans(I, pairing="restart", merge=True, codes=BLOCK):
    """each pay station's spans with a blocking alarm active. pairing='restart': an alarm runs from its raise to its
    clear or the pay station's next restart; 'clear': to the next clear of its code (a raise while one is open is
    the same alarm); 'drop': raises with no clear before the next restart are left out; 'next_same': to the next
    clear or raise of its code; 'next_any': to the pay station's next event of any kind"""
    ev = defaultdict(list)
    for k, r in enumerate(rows(I.target, "alarms")):
        ev[int(r["pay_station"].split("-")[1])].append((parse_z(r["event_time"]), k, r["event"]))
    end = EXTRACT
    out = {}
    for no in I.nos:
        spans = []
        open_ = {}
        for t, _, code in sorted(ev[no]):
            if pairing == "next_any" and open_:
                for c, a in open_.items():
                    spans.append((a, t))
                open_ = {}
            if code == "RESTART":
                if pairing == "restart":
                    for c, a in open_.items():
                        spans.append((a, t))
                    open_ = {}
                elif pairing == "drop":
                    open_ = {}
                continue
            if code in codes:
                if code in open_ and pairing == "next_same":
                    spans.append((open_.pop(code), t))
                if code not in open_:
                    open_[code] = t
            elif code in CLEAR and CLEAR[code] in codes:
                c = CLEAR[code]
                if c in open_:
                    spans.append((open_.pop(c), t))
        for c, a in open_.items():
            spans.append((a, end))
        out[no] = union(spans) if merge else sorted(spans)
    return out


def downtime(I, **kw):
    sp = down_spans(I, **kw)
    return {no: round(in_service_s(sp[no]) / 3600.0, 4) for no in I.nos}


def hround(x, d=1):
    """half up at d decimals, the rounding the figures are stated in"""
    q = 10 ** d
    return float(np.floor(x * q + 0.5) / q)
