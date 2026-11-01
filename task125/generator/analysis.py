"""task125 analysis, from target/ alone: the records conformed under the protocol, each segment's founded patrol
crimes by day, the venues' event nights from the paid-duty register, each segment's steady rate and its excess on
each venue's event nights, the 2027 expectation carried by the 2027 calendar, the designation, the routes the
ladder prices, and the three 2026 ward figures."""
import csv
import datetime as dt
import os
import re
import statistics
import zoneinfo

import numpy as np

TZ = zoneinfo.ZoneInfo("America/Toronto")
PATROL = {"1610", "1420", "1430", "2120", "2142", "2170", "3370"}
YEARS = range(2022, 2027)
D0, D1 = dt.date(2022, 1, 1), dt.date(2026, 12, 31)
NDAYS = (D1 - D0).days + 1
GARDENS_KEYS = ("MEMORIAL GARDENS", "MEM GARDENS")
LAKESHORE_KEYS = ("LAKESHORE CENTRE", "LAKESHORE CTR")
MARINERS = "MOUNTJOY MARINERS HOCKEY CLUB"
CAP = 20


def _read(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_t(x):
    """A records-system time: day first where the legacy system wrote it, ISO otherwise."""
    x = (x or "").strip()
    if not x:
        return None
    if "/" in x:
        return dt.datetime.strptime(x, "%d/%m/%Y %H:%M")
    return dt.datetime.strptime(x[:16], "%Y-%m-%d %H:%M")


def parse_utc(x):
    """A CAD stamp as local time, for dates and tours. Never subtract two of these: in one zone Python subtracts by
    wall clock, an hour out across a clock change; elapsed time comes from utc_of."""
    if not x:
        return None
    return dt.datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).astimezone(TZ)


def utc_of(x):
    """A CAD stamp as a UTC instant, for elapsed time."""
    if not x:
        return None
    return dt.datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)


class Pack:
    def __init__(self, target):
        self.dir = target
        f = lambda n: os.path.join(target, n)
        self.rms = _read(f("mps_rms_occurrences_2022_2026.csv"))
        self.xwalk = {r["legacy_code"]: r["ucr2_code"] for r in _read(f("rms_offence_code_crosswalk_2023.csv"))}
        self.segs = {int(r["segment_id"]): r for r in _read(f("mountjoy_street_segments.csv"))}
        self.cad = _read(f("mps_cad_calls_2026.csv"))
        self.roster = _read(f("mps_patrol_roster_2026.csv"))
        self.register = _read_register(f("mps_paid_duty_register_2022_2027.xlsx"))


def _read_register(path):
    from openpyxl import load_workbook
    wb = load_workbook(path, read_only=True, data_only=True)
    out = {}
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        head = [str(h) for h in rows[0]]
        out[ws.title] = [dict(zip(head, r)) for r in rows[1:]]
    return out


# ----------------------------------------------------------------------------------------------- the records
def conform(P, legacy_dayfirst=True):
    """Each founded patrol crime once: (segment, date) on its latest version, legacy codes read through the
    crosswalk, unfounded dropped, the occurred-from date or the report date where there is none."""
    latest = {}
    for r in P.rms:
        k = r["occurrence_no"]
        if k not in latest or int(r["version"]) > int(latest[k]["version"]):
            latest[k] = r
    out = []
    for r in latest.values():
        code = P.xwalk.get(r["offence_code"], r["offence_code"])
        if code not in PATROL or r["status"] == "UNFOUNDED" or not r["segment_id"]:
            continue
        t = r["occurred_from"] or r["reported"]
        if legacy_dayfirst:
            d = parse_t(t)
        else:
            d = _monthfirst(t)
        if d is None:
            continue
        d = d.date()
        if D0 <= d <= D1:
            out.append((int(r["segment_id"]), d))
    return out


def _monthfirst(x):
    x = (x or "").strip()
    if not x:
        return None
    if "/" in x:
        a, b, rest = x.split("/")
        try:
            return dt.datetime.strptime("%s/%s/%s" % (b, a, rest), "%d/%m/%Y %H:%M")
        except ValueError:
            return dt.datetime.strptime(x, "%d/%m/%Y %H:%M")
    return dt.datetime.strptime(x[:16], "%Y-%m-%d %H:%M")


def daily_matrix(P, crimes):
    """Segments in the street file by day 2022 to 2026."""
    ids = sorted(P.segs)
    pos = {s: k for k, s in enumerate(ids)}
    m = np.zeros((len(ids), NDAYS), dtype=np.int32)
    for s, d in crimes:
        if s in pos:
            m[pos[s], (d - D0).days] += 1
    return ids, m


def yearly(ids, m):
    out = {}
    for y in YEARS:
        a = (dt.date(y, 1, 1) - D0).days
        b = (dt.date(y, 12, 31) - D0).days + 1
        out[y] = dict(zip(ids, m[:, a:b].sum(axis=1).tolist()))
    return out


# ----------------------------------------------------------------------------------------------- the venues
def _date(x):
    if isinstance(x, dt.datetime):
        return x.date()
    if isinstance(x, dt.date):
        return x
    x = str(x)
    return dt.datetime.strptime(x, "%d/%m/%Y").date() if "/" in x else dt.date.fromisoformat(x[:10])


def venue_nights(P):
    """Each venue's event nights from the register, every year's sheet in its own layout, with the Mariners'."""
    out = {"G": set(), "L": set(), "MG": set(), "ML": set()}
    for sheet, rows in P.register.items():
        for r in rows:
            loc = str(r.get("Location") or r.get("location") or "")
            cat = r.get("Category") or r.get("category")
            status = str(r.get("Status") or r.get("status") or "")
            if cat != "EVENT" or status.startswith("CANC"):
                continue
            d = _date(r.get("Duty Date") or r.get("duty_date"))
            client = r.get("Client") or r.get("client")
            v = "G" if any(k in loc for k in GARDENS_KEYS) else ("L" if any(k in loc for k in LAKESHORE_KEYS)
                                                                  else None)
            if v:
                out[v].add(d)
                if client == MARINERS:
                    out["M" + v].add(d)
    return out


def indicators(nights, venue, y0=2022, y1=2026):
    x = np.zeros(NDAYS)
    for d in nights[venue]:
        if y0 <= d.year <= y1 and D0 <= d <= D1:
            x[(d - D0).days] = 1.0
    return x


def decompose(m, nights, y0=2022, y1=2026, dow=False):
    """Each segment's steady crimes a day and its excess on each venue's event nights, by least squares on its
    daily counts over the window (with day-of-week terms when asked)."""
    a = (dt.date(y0, 1, 1) - D0).days
    b = (dt.date(y1, 12, 31) - D0).days + 1
    g = indicators(nights, "G", y0, y1)[a:b]
    l = indicators(nights, "L", y0, y1)[a:b]
    cols = [np.ones(b - a), g, l]
    if dow:
        wd = np.array([(D0 + dt.timedelta(k)).weekday() for k in range(a, b)])
        for k in range(1, 7):
            cols.append((wd == k).astype(float) - (wd == 0).astype(float))
    X = np.column_stack(cols)
    Y = m[:, a:b].T.astype(float)
    coef, *_ = np.linalg.lstsq(X, Y, rcond=None)
    return coef[0], coef[1], coef[2]


def calendar_2027(nights, how="replay"):
    """The 2027 event nights at each venue. replay: 2026's nights with the Mariners' home games at the Lakeshore
    Centre; booked: only the duties booked for 2027 by the extract; average: the 2022 to 2026 mean with the move."""
    def yr(v, y):
        return sum(1 for d in nights[v] if d.year == y)
    mar26 = sum(1 for d in nights["MG"] if d.year == 2026)
    if how == "replay":
        return yr("G", 2026) - mar26, yr("L", 2026) + mar26
    if how == "booked":
        return yr("G", 2027), yr("L", 2027)
    if how == "average":
        g = np.mean([yr("G", y) for y in YEARS])
        l = np.mean([yr("L", y) for y in YEARS])
        mar = np.mean([sum(1 for d in nights["MG"] if d.year == y) for y in YEARS])
        return g - mar, l + mar
    raise ValueError(how)


def expected_2027(m, nights, y0=2022, y1=2026, how="replay", dow=False):
    base, eg, el = decompose(m, nights, y0, y1, dow)
    ng, nl = calendar_2027(nights, how)
    return base * 365 + eg * ng + el * nl


def designate(ids, exp, n=CAP):
    order = sorted(range(len(ids)), key=lambda k: (-exp[k], ids[k]))
    return [ids[k] for k in order[:n]], order


def pool(ids, yr):
    return sorted(s for s in ids if max(yr[y][s] for y in YEARS) >= 25)


def solve(P):
    crimes = conform(P)
    ids, m = daily_matrix(P, crimes)
    nights = venue_nights(P)
    exp = expected_2027(m, nights)
    top, order = designate(ids, exp)
    yr = yearly(ids, m)
    cands = pool(ids, yr)
    return {"ids": ids, "m": m, "nights": nights, "exp": dict(zip(ids, exp.tolist())), "top": top,
            "order": [ids[k] for k in order], "yearly": yr, "pool": cands, "crimes": crimes}


# ----------------------------------------------------------------------------------------------- the routes
def route_sets(S):
    """Each route the ladder prices, as the 20 segments it designates."""
    ids, m, nights, yr = S["ids"], S["m"], S["nights"], S["yearly"]
    out = {}
    for y in (2025, 2026):
        out["count %d" % y] = designate(ids, np.array([yr[y][s] for s in ids], float))[0]
    for y0 in (2022, 2024):
        mean = np.mean([[yr[y][s] for s in ids] for y in range(y0, 2027)], axis=0)
        out["mean %d-2026" % y0] = designate(ids, mean)[0]
    mean5 = np.mean([[yr[y][s] for s in ids] for y in YEARS], axis=0)
    var = np.var([[yr[y][s] for s in ids] for y in YEARS], axis=0, ddof=1)
    mu = mean5.mean()
    tau2 = max(var.mean() * 0 + mean5.var() - mu, 1e-6)
    w = tau2 / (tau2 + mu / 5)
    out["shrunk mean"] = designate(ids, mu + w * (mean5 - mu))[0]
    t = np.arange(5) - 2.0
    slope = np.array([[yr[y][s] for y in YEARS] for s in ids]) @ t / (t @ t)
    out["trend"] = designate(ids, mean5 + slope * 3)[0]
    last12 = m[:, -365:].sum(axis=1)
    out["last 365 days"] = designate(ids, last12.astype(float))[0]
    # event-aware routes that do not decompose: the 2026 count scaled by the venue's 2027 nights over its 2026
    # nights for the segments a venue's event nights move; the Gardens' event-night excess removed only.
    base, eg, el = decompose(m, nights)
    ng26 = sum(1 for d in nights["G"] if d.year == 2026)
    nl26 = sum(1 for d in nights["L"] if d.year == 2026)
    ng27, nl27 = calendar_2027(nights)
    c26 = np.array([yr[2026][s] for s in ids], float)
    scaled = c26.copy()
    for k in range(len(ids)):
        if eg[k] > 0.3:
            scaled[k] = c26[k] * ng27 / ng26
        elif el[k] > 0.3:
            scaled[k] = c26[k] * nl27 / nl26
    out["2026 scaled by nights"] = designate(ids, scaled)[0]
    out["Gardens excess removed"] = designate(ids, c26 - np.maximum(eg, 0) * ng26)[0]
    return out


def standing_family(S):
    """The event-aware constructions: windows, 2027 calendars and the day-of-week terms."""
    ids, m, nights = S["ids"], S["m"], S["nights"]
    out = {}
    for y0 in (2022, 2023, 2024, 2025, 2026):
        for how in ("replay", "average", "booked"):
            for dow in (False, True):
                exp = expected_2027(m, nights, y0, 2026, how, dow)
                out["%d-2026 %s%s" % (y0, how, " dow" if dow else "")] = designate(ids, exp)
    return out


# ----------------------------------------------------------------------------------------------- the asks
def tour_of(t):
    h = t.hour + t.minute / 60.0
    if 7 <= h < 19:
        return t.date(), "D"
    if h >= 19:
        return t.date(), "N"
    return t.date() - dt.timedelta(1), "N"


def tour_naive(t):
    h = t.hour + t.minute / 60.0
    return t.date(), ("D" if 7 <= h < 19 else "N")


def crews(P):
    return {(dt.date.fromisoformat(r["tour_date"]), r["tour"], r["unit"]): 1 + (1 if r["officer_2"] else 0)
            for r in P.roster}


def _ward_of_event(P, r, by_district):
    if by_district:
        return int(r["district"]) if r["district"] else None
    s = int(r["segment_id"]) if r["segment_id"] else None
    return int(P.segs[s]["ward"]) if s in P.segs else None


def tour_elapsed(t):
    """A night tour dated by subtracting a day of elapsed time from an after-midnight dispatch (a pandas habit),
    which differs from the calendar reading only in the first hour after a spring-forward change."""
    h = t.hour + t.minute / 60.0
    if 7 <= h < 19:
        return t.date(), "D"
    if h >= 19:
        return t.date(), "N"
    back = (t.astimezone(dt.timezone.utc) - dt.timedelta(days=1)).astimezone(TZ)
    return back.date(), "N"


def tour_naive_wall(t):
    """A tour dated on the naive local wall clock, seven hours back for the night tour's date."""
    w = t.replace(tzinfo=None)
    h = w.hour + w.minute / 60.0
    if 7 <= h < 19:
        return w.date(), "D"
    return (w - dt.timedelta(hours=7)).date(), "N"


def tour_midnight_elapsed(t):
    """A night tour dated from the local midnight of an after-midnight dispatch less a day of elapsed time (pandas'
    normalize, then a Timedelta), which on the morning after the spring change is 23:00 two evenings back."""
    h = t.hour + t.minute / 60.0
    if 7 <= h < 19:
        return t.date(), "D"
    if h >= 19:
        return t.date(), "N"
    mid = dt.datetime(t.year, t.month, t.day, tzinfo=TZ)
    return (mid.astimezone(dt.timezone.utc) - dt.timedelta(days=1)).astimezone(TZ).date(), "N"


def tour_seven_back(t):
    """A tour dated seven hours of elapsed time back, its letter from the shifted hour."""
    s = (t.astimezone(dt.timezone.utc) - dt.timedelta(hours=7)).astimezone(TZ)
    return s.date(), ("D" if s.hour < 12 else "N")


def tour_seven_back_own_letter(t):
    """A tour's date seven hours of elapsed time back, its letter from the dispatch's own hour."""
    s = (t.astimezone(dt.timezone.utc) - dt.timedelta(hours=7)).astimezone(TZ)
    h = t.hour + t.minute / 60.0
    return s.date(), ("D" if 7 <= h < 19 else "N")


def tours_twelve_elapsed(t):
    """Every tour holding an instant when each tour runs twelve hours of elapsed time from its local start."""
    out = []
    at = t.astimezone(dt.timezone.utc)
    for back in (1, 0):
        d = t.astimezone(TZ).date() - dt.timedelta(back)
        for letter, hh in (("D", 7), ("N", 19)):
            st = dt.datetime(d.year, d.month, d.day, hh, 0, tzinfo=TZ).astimezone(dt.timezone.utc)
            if st <= at < st + dt.timedelta(hours=12):
                out.append((d, letter))
    return out


TOUR_READINGS = {"a day of elapsed time back": tour_elapsed, "local midnight less a day": tour_midnight_elapsed,
                 "seven hours back": tour_seven_back, "seven hours back, own letter": tour_seven_back_own_letter,
                 "the naive wall clock": tour_naive_wall}


def ask_officer_hours(P, by_district=False, naive_tour=False, tour=None, intervals="keep", wall_hours=False):
    """Each ward's officer-hours on 2026 calls for service, by quarter of the call's local date. wall_hours reads a
    unit's hours as the difference of its local wall-clock times (an hour out for a unit working across a change)."""
    cr = crews(P)
    out = {(w, q): 0.0 for w in range(1, 9) for q in range(1, 5)}
    for r in P.cad:
        if r["source"] == "OFFICER" or not r["unit"]:
            continue
        rec = parse_utc(r["received_utc"])
        if rec.year != 2026:
            continue
        w = _ward_of_event(P, r, by_district)
        if w is None:
            continue
        dsp, clr = parse_utc(r["dispatched_utc"]), parse_utc(r["cleared_utc"])
        key = (tour or (tour_naive if naive_tour else tour_of))(dsp)
        n = cr.get(key + (r["unit"],), 1)
        q = (rec.month - 1) // 3 + 1
        hours = (utc_of(r["cleared_utc"]) - utc_of(r["dispatched_utc"])).total_seconds() / 3600.0
        if wall_hours:
            hours = (clr.replace(tzinfo=None) - dsp.replace(tzinfo=None)).total_seconds() / 3600.0
        if hours < 0 and intervals == "drop":
            continue
        if hours < 0 and intervals == "clip":
            hours = 0.0
        out[(w, q)] += hours * n
    return out


def ask_p1(P, by_district=False):
    """Each ward's median minutes from receipt to the first arrival, priority 1 calls received in 2026."""
    first = {}
    for r in P.cad:
        if r["source"] == "OFFICER" or r["priority"] != "1":
            continue
        rec = parse_utc(r["received_utc"])
        if rec.year != 2026:
            continue
        w = _ward_of_event(P, r, by_district)
        if w is None:
            continue
        k = r["event_no"]
        if r["onscene_utc"]:
            mins = (parse_utc(r["onscene_utc"]) - rec).total_seconds() / 60.0
            first[k] = (w, min(first.get(k, (w, mins))[1], mins))
    out = {}
    for w in range(1, 9):
        v = [x[1] for x in first.values() if x[0] == w]
        out[w] = statistics.median(v)
    return out


_NUM = re.compile(r"^(\d+)\s+(.+)$")


def street_index(P):
    by_street = {}
    for s, r in P.segs.items():
        by_street.setdefault(r["street"], []).append(r)
    return by_street


def ward_of_location(P, loc, idx):
    loc = loc.split(", ", 1)[1] if ", " in loc else loc
    if " / " in loc:
        a, b = loc.split(" / ")
        wards = {int(r["ward"]) for r in idx.get(a, []) if b in (r["from_street"], r["to_street"])}
        wards |= {int(r["ward"]) for r in idx.get(b, []) if a in (r["from_street"], r["to_street"])}
        return wards.pop() if len(wards) == 1 else None
    m = _NUM.match(loc)
    n, street = int(m.group(1)), m.group(2)
    hit = set()
    for r in idx.get(street, []):
        if n % 2 and int(r["left_from"]) <= n <= int(r["left_to"]):
            hit.add(int(r["ward"]))
        if n % 2 == 0 and int(r["right_from"]) <= n <= int(r["right_to"]):
            hit.add(int(r["ward"]))
    return hit.pop() if len(hit) == 1 else None


def ask_paid_duty(P):
    """Each ward's paid-duty hours officers worked on 2026 duties, from the Duty Desk lines."""
    idx = street_index(P)
    out = {w: 0.0 for w in range(1, 9)}
    for r in P.register["2026"]:
        if r["status"] != "WORKED":
            continue
        a, b = r["actual_start"], r["actual_end"]
        ma = int(a[:2]) * 60 + int(a[3:])
        mb = int(b[:2]) * 60 + int(b[3:])
        if mb <= ma:
            mb += 1440
        w = ward_of_location(P, r["location"], idx)
        out[w] += (mb - ma) / 60.0
    return out


def half_up(x, nd=0):
    import decimal
    q = decimal.Decimal(1).scaleb(-nd)
    return float(decimal.Decimal(repr(x)).quantize(q, rounding=decimal.ROUND_HALF_UP))


def asks(P, by_district=False, naive_tour=False, tour=None):
    a = ask_officer_hours(P, by_district, naive_tour, tour)
    return ({k: int(half_up(v)) for k, v in a.items()},)


def asks_raw(P, by_district=False, naive_tour=False, tour=None):
    return (ask_officer_hours(P, by_district, naive_tour, tour),)
