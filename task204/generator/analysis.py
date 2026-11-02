"""Every rung, the golden and every ask, computed from target/ alone (no world state)."""
import csv
import datetime as dt
import json
import math
import os
from collections import defaultdict
from zoneinfo import ZoneInfo

import openpyxl

TZL = ZoneInfo("America/Edmonton")
UTC = ZoneInfo("UTC")
W26 = (dt.date(2026, 2, 9), dt.date(2026, 5, 3))
W25 = (dt.date(2025, 2, 10), dt.date(2025, 5, 4))
PERIODS25 = [(dt.date(2025, 2, 10), dt.date(2025, 3, 9)), (dt.date(2025, 3, 10), dt.date(2025, 4, 6)),
             (dt.date(2025, 4, 7), dt.date(2025, 5, 4))]
EASTLINE = ["Westgate", "Centre Square", "Union Yards", "Millbrook", "Fairgrounds", "Cobb Street", "Ashford Road",
            "Ridgeview", "Prairie Gate"]
DISTRICTS = ["D%d" % i for i in range(1, 11)]


def utc_to_local(s):
    t = dt.datetime.strptime(s, "%Y-%m-%dT%H:%MZ" if len(s) == 17 else "%Y-%m-%dT%H:00Z")
    return t.replace(tzinfo=UTC).astimezone(TZL).replace(tzinfo=None)


def parse_local(s):
    return dt.datetime.strptime(s, "%Y-%m-%d %H:%M")


# ---- readers ------------------------------------------------------------------------------------------
def read_rms(target):
    with open(os.path.join(target, "rms_occurrence_extract_20260511.csv"), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_tpo(target):
    wb = openpyxl.load_workbook(os.path.join(target, "tpo_occurrence_log_2025_2026.xlsx"), read_only=True)
    ws = wb["Occurrences"]
    rows = list(ws.iter_rows(values_only=True))
    head = list(rows[1])
    return [dict(zip(head, r)) for r in rows[2:]]


def read_codes(target):
    wb = openpyxl.load_workbook(os.path.join(target, "carvale_transit_codes.xlsx"), read_only=True)
    out = {}
    for sheet in ("Stations", "Fare gates"):
        rows = list(wb[sheet].iter_rows(values_only=True))
        head = list(rows[0])
        out[sheet] = [dict(zip(head, r)) for r in rows[1:]]
    return out


def array_station(codes):
    """Each gate array's station, from the fare systems code list (arrays keep their id when codes change)."""
    return {r["gate_array"].replace("-", "").lower(): r["station_name"] for r in codes["Fare gates"]}


def code_current(codes, code):
    """The station a code means in the current code list (a join on the code alone)."""
    for r in codes["Fare gates"]:
        if r["gate_code"] == code:
            return r["station_name"]
    return None


def read_fare_codes(target):
    """(code, local date) -> gate array, from the 2026 hourly file and the 2025 daily summary."""
    seen = {}
    with open(os.path.join(target, "fare_gate_entries_hourly_2026.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            d = utc_to_local(r["hour_start_utc"]).date()
            seen[(r["gate_code"], d)] = r["array_id"]
    with open(os.path.join(target, "fare_gate_daily_summary_2025.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            d = dt.datetime.strptime(r["service_day"], "%d/%m/%Y").date()
            seen[(r["gate"], d)] = r["array"]
    return seen


def code_on(fare_codes, arrays, code, d):
    """The station a code stood for on date d: the array that carried the code that day."""
    for k in range(0, 8):
        for dd in (d - dt.timedelta(days=k), d + dt.timedelta(days=k)):
            a = fare_codes.get((code, dd))
            if a:
                return arrays.get(a)
    return None


def read_geojson(target, name):
    with open(os.path.join(target, name), encoding="utf-8") as f:
        fc = json.load(f)
    polys = []
    for ft in fc["features"]:
        for poly in ft["geometry"]["coordinates"]:
            polys.append((ft["properties"]["DISTRICT"], poly[0]))
    return polys


def point_in_ring(x, y, ring):
    inside = False
    n = len(ring)
    for i in range(n - 1):
        x1, y1 = ring[i]
        x2, y2 = ring[i + 1]
        if (y1 > y) != (y2 > y):
            xi = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < xi:
                inside = not inside
    return inside


def district_at(polys, x, y):
    for d, ring in polys:
        if point_in_ring(x, y, ring):
            return d
    return None


def read_station_reference():
    """The CAU's station reference (2026 layout), as printed in its PDF (the verifier reads the PDF itself)."""
    return {"Westgate": "D2", "Centre Square": "D1", "Union Yards": "D4", "Millbrook": "D6", "Fairgrounds": "D6",
            "Cobb Street": "D8", "Ashford Road": "D7", "Ridgeview": "D9", "Prairie Gate": "D9", "Station Hill": "D3",
            "Kerr Park": "D3", "Hollin": "D5", "Larchmont": "D10"}


RMS_STATION = {"WESTGATE LRT STN": "Westgate", "CENTRE SQ LRT STN": "Centre Square", "UNION YARDS LRT STN": "Union Yards",
               "MILLBROOK LRT STN": "Millbrook", "FAIRGROUNDS LRT STN": "Fairgrounds", "COBB ST LRT STN": "Cobb Street",
               "ASHFORD RD LRT STN": "Ashford Road", "RIDGEVIEW LRT STN": "Ridgeview", "PRAIRIE GATE LRT STN": "Prairie Gate",
               "STATION HILL LRT STN": "Station Hill", "KERR PARK LRT STN": "Kerr Park", "HOLLIN LRT STN": "Hollin",
               "LARCHMONT LRT STN": "Larchmont"}


def rms_station(loc_text):
    base = loc_text.replace(" (ON TRAIN)", "")
    return RMS_STATION.get(base)


# ---- the population -----------------------------------------------------------------------------------
def phone_offences(rms, tpo, codes, window, dedupe=True, date_aware_codes=True, fare_codes=None, ref_window_min=20):
    """Robbery and theft from a person with a phone taken, reported to the Service or to transit officers, once."""
    out = []
    in_win = lambda d: window[0] <= d <= window[1]
    files = set()
    for r in rms:
        if r["offence_code"] not in ("ROB-PERS", "THFT-PERS") or "CELL PHONE" not in r["property_taken"]:
            continue
        t = parse_local(r["occurred_from_local"])
        if not in_win(t.date()):
            continue
        files.add(r["occurrence_no"])
        out.append({"src": "RMS", "id": r["occurrence_no"], "t": t, "station": rms_station(r["location_text"]),
                    "x": float(r["x_utm12n"]), "y": float(r["y_utm12n"]), "district_rec": r["patrol_district"],
                    "mo": r["mo_code"], "sus": int(r["num_suspects"]) if r["num_suspects"] else 0,
                    "alo": int(r["suspect_age_from"]) if r["suspect_age_from"] else None,
                    "ahi": int(r["suspect_age_to"]) if r["suspect_age_to"] else None,
                    "loc": r["location_type"], "offence": r["offence_code"]})
    rms_station_events = defaultdict(list)
    for o in out:
        if o["station"]:
            rms_station_events[o["station"]].append(o)
    for r in tpo:
        if r["Category"] not in ("THEFT FROM PERSON", "ROBBERY") or r["Property"] != "CELL PHONE":
            continue
        t = utc_to_local(r["Logged (UTC)"])
        d = t.date()
        st = (code_on(fare_codes, array_station(codes), r["Station Code"], d) if date_aware_codes
              else code_current(codes, r["Station Code"]))
        if not in_win(d):
            continue
        if dedupe:
            if r["CPS File #"] and r["CPS File #"] in files:
                continue
            if r["Referred To Police"] == "Y" and not r["CPS File #"]:
                # referred without the file number: the police file is the RMS row at the same station shortly before
                match = [o for o in rms_station_events.get(st, []) if 0 <= (t - o["t"]).total_seconds() <= ref_window_min * 60]
                if match:
                    continue
        out.append({"src": "TPO", "id": r["TPO Log #"], "t": t, "station": st, "x": None, "y": None,
                    "district_rec": None, "mo": "", "sus": int(r["Suspects"] or 0), "alo": None, "ahi": None,
                    "loc": "LRT TRAIN" if r["Location"] == "ON TRAIN" else "LRT PLATFORM",
                    "offence": "THFT-PERS" if r["Category"] == "THEFT FROM PERSON" else "ROB-PERS"})
    return out


# ---- linkage ------------------------------------------------------------------------------------------
def _uf(n):
    par = list(range(n))

    def find(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i

    def union(i, j):
        par[find(i)] = find(j)
    return find, union


def behaviour_match(a, b):
    if a["mo"] != b["mo"] or not a["mo"]:
        return False
    if a["alo"] is None or b["alo"] is None:
        return False
    return min(a["ahi"], b["ahi"]) >= max(a["alo"], b["alo"])


def local_series(offs, dmax=1000.0, days=28):
    """The field's default linkage: same method and overlapping descriptions, within dmax metres and `days` days."""
    grp = [o for o in offs if o["sus"] >= 2 and o["x"] is not None]
    find, union = _uf(len(grp))
    for i in range(len(grp)):
        for j in range(i + 1, len(grp)):
            a, b = grp[i], grp[j]
            if not behaviour_match(a, b):
                continue
            if abs((a["t"] - b["t"]).total_seconds()) > days * 86400:
                continue
            if math.hypot(a["x"] - b["x"], a["y"] - b["y"]) > dmax:
                continue
            union(i, j)
    comps = defaultdict(list)
    for i, o in enumerate(grp):
        comps[find(i)].append(o)
    return [c for c in comps.values() if len(c) >= 3]


def corridor_series(offs, days=28, dmax=1000.0):
    """Platform offences on one line linked whatever the station; street offences keep the distance rule."""
    line = lambda o: ("EL" if o["station"] in EASTLINE[2:] + ["Westgate"] else ("NL" if o["station"] else None))
    grp = [o for o in offs if o["sus"] >= 2 and o["x"] is not None]
    find, union = _uf(len(grp))
    for i in range(len(grp)):
        for j in range(i + 1, len(grp)):
            a, b = grp[i], grp[j]
            if not behaviour_match(a, b) or abs((a["t"] - b["t"]).total_seconds()) > days * 86400:
                continue
            la, lb = line(a), line(b)
            if a["loc"] == "LRT PLATFORM" and b["loc"] == "LRT PLATFORM" and la and la == lb:
                union(i, j)
            elif math.hypot(a["x"] - b["x"], a["y"] - b["y"]) <= dmax:
                union(i, j)
    comps = defaultdict(list)
    for i, o in enumerate(grp):
        comps[find(i)].append(o)
    return [c for c in comps.values() if len(c) >= 3]


# ---- the timetable --------------------------------------------------------------------------------------
class GTFS:
    def __init__(self, target):
        g = os.path.join(target, "gtfs")
        rd = lambda n: list(csv.DictReader(open(os.path.join(g, n), encoding="utf-8")))
        self.stops = {r["stop_id"]: r for r in rd("stops.txt")}
        self.trips = {r["trip_id"]: r for r in rd("trips.txt")}
        self.cal = {r["service_id"]: r for r in rd("calendar.txt")}
        self.cdates = defaultdict(dict)
        for r in rd("calendar_dates.txt"):
            self.cdates[r["service_id"]][r["date"]] = r["exception_type"]
        self.st = defaultdict(list)
        for r in rd("stop_times.txt"):
            self.st[r["trip_id"]].append(r)
        self.freq = defaultdict(list)
        if os.path.exists(os.path.join(g, "frequencies.txt")):
            for r in rd("frequencies.txt"):
                self.freq[r["trip_id"]].append(r)
        self.expand = True
        self.station_of_stop = {sid: s["stop_name"].rsplit(" Station", 1)[0] for sid, s in self.stops.items()}
        self.route_line = {"201": "EL", "202": "NL"}

    def runs_on(self, service_id, d):
        c = self.cal[service_id]
        ds = d.strftime("%Y%m%d")
        ex = self.cdates.get(service_id, {}).get(ds)
        if ex == "2":
            return False
        if ex == "1":
            return True
        if not (c["start_date"] <= ds <= c["end_date"]):
            return False
        return c[["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"][d.weekday()]] == "1"

    def departures(self, d):
        """(station, departure datetime, service date, trip_id, pickup_type) for every trip running on service date d."""
        out = []
        sec = lambda x: int(x[0:-6]) * 3600 + int(x[-5:-3]) * 60 + int(x[-2:])
        base = dt.datetime(d.year, d.month, d.day)
        for tid, tr in self.trips.items():
            if not self.runs_on(tr["service_id"], d):
                continue
            rows = self.st[tid]
            starts = [(tid, 0)]
            if self.expand and self.freq.get(tid):
                first = sec(rows[0]["departure_time"])
                starts = []
                for f in self.freq[tid]:
                    t0, t1, hw = sec(f["start_time"]), sec(f["end_time"]), int(f["headway_secs"])
                    k = t0
                    while k < t1:
                        starts.append(("%s@%d" % (tid, k), k - first))
                        k += hw
            for sid_, shift in starts:
                for r in rows:
                    t = base + dt.timedelta(seconds=sec(r["departure_time"]) + shift)
                    out.append((self.station_of_stop[r["stop_id"]], t, d, sid_, r["pickup_type"], self.route_line[tr["route_id"]]))
        return out


def trip_candidates(gtfs, offs, tol_min=3.0, cache=None):
    cache = {} if cache is None else cache
    res = []
    for o in offs:
        cands = set()
        for dd in (o["t"].date() - dt.timedelta(days=1), o["t"].date()):
            if dd not in cache:
                cache[dd] = gtfs.departures(dd)
            for st, t, sd, tid, pick, line in cache[dd]:
                if st == o["station"] and pick == "0" and abs((t - o["t"]).total_seconds()) <= tol_min * 60:
                    cands.add((sd, tid))
        res.append(cands)
    return res


def golden_series(offs, gtfs, tol_min=3.0, dmax=1000.0, days=28, cache=None):
    """Local series by the field's linkage, then series joined where their offences sat on the same train trip."""
    local = local_series(offs, dmax, days)
    plat = [o for c in local for o in c if o["loc"] == "LRT PLATFORM" and o["station"]]
    cands = trip_candidates(gtfs, plat, tol_min, cache)
    which = {}
    for k, c in enumerate(local):
        for o in c:
            which[id(o)] = k
    find, union = _uf(len(local))
    runs = []
    for i in range(len(plat)):
        for j in range(i + 1, len(plat)):
            if plat[i]["station"] != plat[j]["station"] and cands[i] & cands[j]:
                union(which[id(plat[i])], which[id(plat[j])])
                runs.append(sorted(cands[i] & cands[j])[0])
    merged = defaultdict(list)
    for k, c in enumerate(local):
        merged[find(k)].extend(c)
    return list(merged.values()), sorted(set(runs))


def simultaneity(series, offs, minutes=3.0):
    """Offences of one series that fell within `minutes` of another series' offence at a different station."""
    sets = [{id(o) for o in c} for c in series]
    which = {}
    for k, c in enumerate(series):
        for o in c:
            which[id(o)] = k
    plat = [o for c in series for o in c if o["station"] and o["loc"] == "LRT PLATFORM"]
    pairs = set()
    for a in plat:
        for b in plat:
            if which[id(a)] < which[id(b)] and a["station"] != b["station"]:
                if abs((a["t"] - b["t"]).total_seconds()) <= minutes * 60:
                    pairs.add((which[id(a)], which[id(b)], a["t"].date()))
    out = defaultdict(set)
    for ka, kb, d in pairs:
        out[(ka, kb)].add(d)
    return {k: sorted(v) for k, v in out.items()}


def team_table(series, polys26):
    out = []
    for c in series:
        ds = sorted({district_at(polys26, o["x"], o["y"]) for o in c}, key=lambda s: int(s[1:]))
        out.append({"districts": ds, "n": len(c), "stations": sorted({o["station"] for o in c if o["station"]}),
                    "ids": sorted(o["id"] for o in c)})
    out.sort(key=lambda r: (-r["n"], r["districts"]))
    return out


# ---- asks -------------------------------------------------------------------------------------------------
def ask_a(rms, tpo, codes, polys26, stref, fare_codes, redistrict=True, date_aware=True, dedupe=True, ref_window_min=20):
    offs = phone_offences(rms, tpo, codes, W25, dedupe=dedupe, date_aware_codes=date_aware, fare_codes=fare_codes,
                          ref_window_min=ref_window_min)
    grid = {d: [0, 0, 0] for d in DISTRICTS}
    for o in offs:
        if o["src"] == "RMS":
            dist = district_at(polys26, o["x"], o["y"]) if redistrict else o["district_rec"]
        else:
            dist = stref.get(o["station"])
        if dist not in grid:
            continue
        for k, (a, b) in enumerate(PERIODS25):
            if a <= o["t"].date() <= b:
                grid[dist][k] += 1
    return grid


def ask_b(target, codes, date_aware=True, local_window=True):
    out = {s: 0 for s in EASTLINE}
    arrays = array_station(codes)
    with open(os.path.join(target, "fare_gate_entries_hourly_2026.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            tu = dt.datetime.strptime(r["hour_start_utc"], "%Y-%m-%dT%H:00Z")
            t = utc_to_local(r["hour_start_utc"]) if local_window else tu
            if not (W26[0] <= t.date() <= W26[1]):
                continue
            st = arrays.get(r["array_id"]) if date_aware else code_current(codes, r["gate_code"])
            if st in out:
                out[st] += int(r["entries"])
    return out


def ask_c(gtfs, by_service_date=False, pickups_only=False, cache=None):
    cache = {} if cache is None else cache
    out = {s: 0 for s in EASTLINE}
    lo = dt.datetime(W26[0].year, W26[0].month, W26[0].day)
    hi = dt.datetime(W26[1].year, W26[1].month, W26[1].day) + dt.timedelta(days=1)
    d = W26[0] - dt.timedelta(days=1)
    while d <= W26[1]:
        if d not in cache:
            cache[d] = gtfs.departures(d)
        for st, t, sd, tid, pick, line in cache[d]:
            if line != "EL" or st not in out:
                continue
            if pickups_only and pick != "0":
                continue
            inside = (W26[0] <= sd <= W26[1]) if by_service_date else (lo <= t < hi)
            if inside:
                out[st] += 1
        d += dt.timedelta(days=1)
    return out


def run_all(target):
    rms = read_rms(target)
    tpo = read_tpo(target)
    codes = read_codes(target)
    polys26 = read_geojson(target, "patrol_districts_2026.geojson")
    gtfs = GTFS(target)
    stref = read_station_reference()
    cache = {}
    fare_codes = read_fare_codes(target)
    offs = phone_offences(rms, tpo, codes, W26, fare_codes=fare_codes)
    r0 = local_series(offs)
    r2 = corridor_series(offs)
    gold, runs = golden_series(offs, gtfs, cache=cache)
    res = {
        "n_offences_w26": len(offs),
        "n_group_scope": sum(1 for o in offs if o["sus"] >= 2),
        "rung0": team_table(r0, polys26),
        "rung2": team_table(r2, polys26),
        "golden": team_table(gold, polys26),
        "runs": runs,
        "ask_a": ask_a(rms, tpo, codes, polys26, stref, fare_codes),
        "ask_b": ask_b(target, codes),
        "ask_c": ask_c(gtfs, cache=cache),
    }
    res["simultaneous"] = simultaneity(gold, offs)
    r1 = sorted({d for t in res["rung0"] for d in t["districts"]}, key=lambda s: int(s[1:]))
    res["rung1"] = [{"districts": [d], "n": sum(1 for t in res["rung0"] for o in t["ids"]
                                                if d in t["districts"])} for d in r1]
    res["_offs"] = offs
    res["_gtfs"] = gtfs
    res["_cache"] = cache
    res["_rms"], res["_tpo"], res["_codes"], res["_polys26"], res["_stref"] = rms, tpo, codes, polys26, stref
    res["_fare_codes"] = fare_codes
    return res


if __name__ == "__main__":
    import sys
    r = run_all(sys.argv[1])
    for k in ("n_offences_w26", "n_group_scope", "rung0", "rung1", "rung2", "golden", "ask_a", "ask_b", "ask_c"):
        v = r[k]
        if isinstance(v, list):
            print(k, [(t["districts"], t["n"]) for t in v])
        else:
            print(k, v)
    print("runs", len(r["runs"]))
