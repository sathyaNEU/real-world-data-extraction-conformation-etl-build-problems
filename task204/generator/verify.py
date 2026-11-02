"""Independent verifier for task204 v2. Its own code path (no import of the generator or analysis modules): reads every
shipped format back (CSV, XLSX and DOCX through their XML, PDF through ASCII85 and Flate, GeoJSON, the GTFS feed),
recomputes the call and every ask, and compares them with the golden workbook, the golden memo and figures.json."""
import base64
import bisect
import csv
import datetime as dt
import json
import math
import os
import re
import sys
import zipfile
import zlib
from collections import defaultdict
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
MT = ZoneInfo("America/Edmonton")
REVIEW = (dt.date(2026, 2, 9), dt.date(2026, 5, 3))
LAST_YEAR = (dt.date(2025, 2, 10), dt.date(2025, 5, 4))
FAIL = []


def ok(label, cond, detail=""):
    print("%s  %s%s" % ("PASS" if cond else "FAIL", label, "" if cond else "  [%s]" % detail))
    if not cond:
        FAIL.append(label)


# ---- format readers -------------------------------------------------------------------------------------------
def xlsx_sheets(path):
    z = zipfile.ZipFile(path)
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        sx = z.read("xl/sharedStrings.xml").decode("utf-8")
        for si in re.findall(r"<si>(.*?)</si>", sx, re.S):
            shared.append("".join(re.findall(r"<t[^>]*>(.*?)</t>", si, re.S)))
    wb = z.read("xl/workbook.xml").decode("utf-8")
    rels = z.read("xl/_rels/workbook.xml.rels").decode("utf-8")
    target = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', rels))
    target.update({k: v for v, k in re.findall(r'Target="([^"]+)"[^>]*Id="(rId\d+)"', rels)})
    out = {}
    for name, rid in re.findall(r'<sheet [^>]*name="([^"]+)"[^>]*r:id="(rId\d+)"', wb):
        sx = z.read("xl/" + target[rid].lstrip("/").replace("xl/", "")).decode("utf-8")
        rows = []
        for rx in re.findall(r"<row[^>]*>(.*?)</row>", sx, re.S):
            cells = {}
            for ref, attrs, body in re.findall(r'<c r="([A-Z]+)\d+"([^>]*)>(.*?)</c>', rx, re.S):
                v = re.search(r"<v>(.*?)</v>", body, re.S)
                if 't="s"' in attrs:
                    val = shared[int(v.group(1))]
                elif 't="inlineStr"' in attrs:
                    val = "".join(re.findall(r"<t[^>]*>(.*?)</t>", body, re.S))
                elif 't="str"' in attrs:
                    val = v.group(1) if v else ""
                else:
                    val = float(v.group(1)) if v else None
                    if val is not None and val == int(val):
                        val = int(val)
                cells[col_index(ref)] = unescape(val) if isinstance(val, str) else val
            if cells:
                rows.append([cells.get(i) for i in range(max(cells) + 1)])
            else:
                rows.append([])
        out[unescape(name)] = rows
    return out


def col_index(ref):
    n = 0
    for ch in ref:
        n = n * 26 + ord(ch) - 64
    return n - 1


def unescape(s):
    return s.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&apos;", "'").replace("&amp;", "&")


def docx_text(path):
    x = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")
    return unescape(re.sub(r"<[^>]+>", "", x.replace("</w:p>", "\n")))


def pdf_fragments(path):
    data = open(path, "rb").read()
    frags = []
    for m in re.finditer(rb"/Filter\s*\[\s*/ASCII85Decode\s*/FlateDecode\s*\][^>]*>>\s*stream\r?\n(.*?)endstream", data, re.S):
        raw = m.group(1).strip()
        if raw.startswith(b"<~"):
            raw = raw[2:]
        if raw.endswith(b"~>"):
            raw = raw[:-2]
        content = zlib.decompress(base64.a85decode(raw)).decode("latin-1")
        for s in re.findall(r"\(((?:\\.|[^\\)])*)\)\s*Tj", content):
            frags.append(re.sub(r"\\(.)", r"\1", s))
    return frags


# ---- geometry ----------------------------------------------------------------------------------------------------
def districts(name):
    fc = json.load(open(os.path.join(T, name), encoding="utf-8"))
    out = []
    for f in fc["features"]:
        for poly in f["geometry"]["coordinates"]:
            out.append((f["properties"]["DISTRICT"], poly[0]))
    return out


def winding(x, y, ring):
    """Winding number test (a different algorithm from the generator's ray cast)."""
    wn = 0
    for (x1, y1), (x2, y2) in zip(ring, ring[1:]):
        cross = (x2 - x1) * (y - y1) - (x - x1) * (y2 - y1)
        if y1 <= y < y2 and cross > 0:
            wn += 1
        elif y2 <= y < y1 and cross < 0:
            wn -= 1
    return wn != 0


def district_of(polys, x, y):
    hits = [d for d, ring in polys if winding(x, y, ring)]
    return hits[0] if len(hits) == 1 else None


# ---- the timetable ---------------------------------------------------------------------------------------------------
class Feed:
    def __init__(self):
        g = os.path.join(T, "gtfs")
        rd = lambda n: list(csv.DictReader(open(os.path.join(g, n), encoding="utf-8-sig")))
        self.station = {r["stop_id"]: r["stop_name"].split(" Station")[0] for r in rd("stops.txt")}
        routes = {r["route_id"]: (r.get("route_long_name", "") + " " + r.get("route_short_name", "")) for r in rd("routes.txt")}
        self.trips = {r["trip_id"]: (r["service_id"], "Eastline" in routes[r["route_id"]]) for r in rd("trips.txt")}
        self.cal = {r["service_id"]: r for r in rd("calendar.txt")}
        self.exc = {(r["service_id"], r["date"]): r["exception_type"] for r in rd("calendar_dates.txt")}
        self.rows = defaultdict(list)
        for r in rd("stop_times.txt"):
            self.rows[r["trip_id"]].append((int(r["stop_sequence"]), r["stop_id"], hms(r["arrival_time"]), hms(r["departure_time"])))
        for k in self.rows:
            self.rows[k].sort()
        self.freq = defaultdict(list)
        for r in rd("frequencies.txt"):
            self.freq[r["trip_id"]].append((hms(r["start_time"]), hms(r["end_time"]), int(r["headway_secs"])))
        self._day = {}

    def active(self, sid, d):
        key = d.strftime("%Y%m%d")
        e = self.exc.get((sid, key))
        if e:
            return e == "1"
        c = self.cal[sid]
        return c["start_date"] <= key <= c["end_date"] and c[d.strftime("%A").lower()] == "1"

    def day(self, d):
        """Every scheduled call on service date d: (station, local datetime, trip instance, eastline)."""
        if d in self._day:
            return self._day[d]
        out = []
        midnight = dt.datetime.combine(d, dt.time())
        for tid, (sid, east) in self.trips.items():
            if not self.active(sid, d):
                continue
            rows = self.rows[tid]
            if tid in self.freq:
                t0 = rows[0][3]
                shifts = [(k - t0, "%s+%d" % (tid, k)) for a, b, h in self.freq[tid] for k in range(a, b, h)]
            else:
                shifts = [(0, tid)]
            for sh, inst in shifts:
                for _, stop, arr, dep in rows:
                    out.append((self.station[stop], midnight + dt.timedelta(seconds=dep + sh), (d, inst), east))
        self._day[d] = out
        return out


def hms(s):
    h, m, sec = s.strip().split(":")
    return int(h) * 3600 + int(m) * 60 + int(sec)


# ---- main ------------------------------------------------------------------------------------------------------------
def main():
    # positive controls on every PDF before anything is read from them
    directive = " ".join(pdf_fragments(os.path.join(T, "ops41_series_crime_response_directive.pdf")))
    ok("V-pdf-control-directive: the directive decodes and carries its definitions",
       "three or more offences committed by the same offender group" in directive and "twelve completed weeks" in directive)
    cal = " ".join(pdf_fragments(os.path.join(T, "cpsd_school_year_calendar_2025_26.pdf")))
    ok("V-pdf-control-calendar: the school calendar decodes", "Spring break" in cal)
    frags = pdf_fragments(os.path.join(T, "cau_lrt_station_reference_2026.pdf"))
    ref = {}
    for i, f in enumerate(frags):
        if f.endswith("LRT STN") and i >= 2 and re.fullmatch(r"D\d+", frags[i + 1] or ""):
            ref[f] = (frags[i - 2], frags[i + 1])
    ok("V-pdf-control-reference: the station reference yields thirteen stations with districts", len(ref) == 13, len(ref))
    name_district = {v[0]: v[1] for v in ref.values()}

    # occurrence records
    rms = list(csv.DictReader(open(os.path.join(T, "rms_occurrence_extract_20260511.csv"), encoding="utf-8")))
    tpo_rows = xlsx_sheets(os.path.join(T, "tpo_occurrence_log_2025_2026.xlsx"))["Occurrences"]
    head = tpo_rows[1]
    tpo = [dict(zip(head, r)) for r in tpo_rows[2:] if r]
    codes = xlsx_sheets(os.path.join(T, "carvale_transit_codes.xlsx"))
    fg = codes["Fare gates"]
    array_station = {}
    for r in fg[1:]:
        if r and r[0]:
            rec = dict(zip(fg[0], r))
            array_station[re.sub(r"[^0-9a-z]", "", str(rec["gate_array"]).lower())] = rec["station_name"]
    poly26 = districts("patrol_districts_2026.geojson")
    feed = Feed()
    when = lambda s: dt.datetime.strptime(s, "%Y-%m-%d %H:%M")
    utc = lambda s: dt.datetime.strptime(s, "%Y-%m-%dT%H:%MZ").replace(tzinfo=dt.timezone.utc).astimezone(MT).replace(tzinfo=None)

    # code -> array by local date, from the fare files (arrays keep their id when codes change)
    code_day = {}
    with open(os.path.join(T, "fare_gate_entries_hourly_2026.csv"), encoding="utf-8") as f:
        hourly = list(csv.DictReader(f))
    for r in hourly:
        local = dt.datetime.strptime(r["hour_start_utc"], "%Y-%m-%dT%H:%MZ").replace(tzinfo=dt.timezone.utc).astimezone(MT)
        code_day[(r["gate_code"], local.date())] = r["array_id"]
    with open(os.path.join(T, "fare_gate_daily_summary_2025.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            d, m, y = r["service_day"].split("/")
            code_day[(r["gate"], dt.date(int(y), int(m), int(d)))] = r["array"]

    def station_for_code(code, d):
        for k in range(8):
            for dd in (d - dt.timedelta(days=k), d + dt.timedelta(days=k)):
                a = code_day.get((code, dd))
                if a:
                    return array_station.get(re.sub(r"[^0-9a-z]", "", a.lower()))
        return None

    def population(window):
        out, rms_at = [], defaultdict(list)
        files = set()
        for r in rms:
            if r["offence_code"] in ("ROB-PERS", "THFT-PERS") and "CELL PHONE" in r["property_taken"]:
                t = when(r["occurred_from_local"])
                if window[0] <= t.date() <= window[1]:
                    st = ref.get(r["location_text"].replace(" (ON TRAIN)", ""), (None,))[0]
                    o = {"src": "RMS", "id": r["occurrence_no"], "t": t, "st": st, "x": float(r["x_utm12n"]),
                         "y": float(r["y_utm12n"]), "mo": r["mo_code"], "n": int(r["num_suspects"] or 0),
                         "lo": int(r["suspect_age_from"]) if r["suspect_age_from"] else None,
                         "hi": int(r["suspect_age_to"]) if r["suspect_age_to"] else None, "where": r["location_type"]}
                    out.append(o)
                    files.add(r["occurrence_no"])
                    if st:
                        rms_at[st].append(t)
        for r in tpo:
            if r["Category"] not in ("THEFT FROM PERSON", "ROBBERY") or r["Property"] != "CELL PHONE":
                continue
            t = utc(r["Logged (UTC)"])
            if not (window[0] <= t.date() <= window[1]):
                continue
            if r["CPS File #"] and r["CPS File #"] in files:
                continue
            st = station_for_code(r["Station Code"], t.date())
            if r["Referred To Police"] == "Y" and not r["CPS File #"] and any(
                    0 <= (t - x).total_seconds() <= 1800 for x in rms_at.get(st, [])):
                continue
            out.append({"src": "TPO", "id": r["TPO Log #"], "t": t, "st": st, "x": None, "y": None, "mo": "",
                        "n": int(r["Suspects"] or 0), "lo": None, "hi": None, "where": "TPO"})
        return out

    # the call
    offs = population(REVIEW)
    ok("V-tpo-lone: every transit-only report in the review period has one suspect", all(o["n"] <= 1 for o in offs if o["src"] == "TPO"))
    grp = [o for o in offs if o["n"] >= 2 and o["x"] is not None]
    parent = list(range(len(grp)))

    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    same = lambda a, b: a["mo"] and a["mo"] == b["mo"] and a["lo"] is not None and b["lo"] is not None and \
        max(a["lo"], b["lo"]) <= min(a["hi"], b["hi"])
    for i in range(len(grp)):
        for j in range(i):
            a, b = grp[i], grp[j]
            if same(a, b) and abs((a["t"] - b["t"]).total_seconds()) <= 28 * 86400 and math.hypot(a["x"] - b["x"], a["y"] - b["y"]) <= 1000:
                parent[root(i)] = root(j)
    local = defaultdict(list)
    for i in range(len(grp)):
        local[root(i)].append(i)
    n_local = sum(1 for v in local.values() if len(v) >= 3)
    ok("V-rung0: the field's linkage alone gives seven series", n_local == 7, n_local)
    # place each platform offence on the trips leaving its station within three minutes
    on = {}
    for i, o in enumerate(grp):
        if o["where"] != "LRT PLATFORM" or not o["st"]:
            continue
        hits = set()
        for d in (o["t"].date() - dt.timedelta(days=1), o["t"].date()):
            for st, t, inst, east in feed.day(d):
                if st == o["st"] and abs((t - o["t"]).total_seconds()) <= 180:
                    hits.add(inst)
        on[i] = hits
    trips_used = set()
    keys = sorted(on)
    for a in range(len(keys)):
        for b in range(a):
            i, j = keys[a], keys[b]
            common = on[i] & on[j]
            if common and grp[i]["st"] != grp[j]["st"] and same(grp[i], grp[j]):
                parent[root(i)] = root(j)
                trips_used.add(min(common))
    comps = defaultdict(list)
    for i in range(len(grp)):
        comps[root(i)].append(grp[i])
    series = [c for c in comps.values() if len(c) >= 3]
    teams = sorted((tuple(sorted({district_of(poly26, o["x"], o["y"]) for o in c}, key=lambda s: int(s[1:]))), len(c)) for c in series)

    # asks
    def period(d):
        for k in range(3):
            a = LAST_YEAR[0] + dt.timedelta(days=28 * k)
            if a <= d <= a + dt.timedelta(days=27):
                return k
        return None
    grid = {"D%d" % k: [0, 0, 0] for k in range(1, 11)}
    for o in population(LAST_YEAR):
        dist = district_of(poly26, o["x"], o["y"]) if o["src"] == "RMS" else name_district.get(o["st"])
        if dist in grid and period(o["t"].date()) is not None:
            grid[dist][period(o["t"].date())] += 1
    east = ["Westgate", "Centre Square", "Union Yards", "Millbrook", "Fairgrounds", "Cobb Street", "Ashford Road", "Ridgeview",
            "Prairie Gate"]
    entries = {s: 0 for s in east}
    for r in hourly:
        local = dt.datetime.strptime(r["hour_start_utc"], "%Y-%m-%dT%H:%MZ").replace(tzinfo=dt.timezone.utc).astimezone(MT)
        st = array_station.get(re.sub(r"[^0-9a-z]", "", r["array_id"].lower()))
        if REVIEW[0] <= local.date() <= REVIEW[1] and st in entries:
            entries[st] += int(r["entries"])
    calls = {s: 0 for s in east}
    d = REVIEW[0] - dt.timedelta(days=1)
    while d <= REVIEW[1]:
        for st, t, inst, is_east in feed.day(d):
            if is_east and st in calls and REVIEW[0] <= t.date() <= REVIEW[1]:
                calls[st] += 1
        d += dt.timedelta(days=1)

    # compare with the golden workbook, the memo and figures.json
    gw = xlsx_sheets(os.path.join(TASK, "golden", "series_assessment_2026.xlsx"))
    g_teams = sorted((tuple("D" + x.strip() for x in str(r[2]).split(",")), int(r[3]))
                     for r in gw["Series teams"] if r and isinstance(r[0], str) and r[0].startswith("Team "))
    g_n = [r[1] for r in gw["Series teams"] if r and r[0] == "Series teams required"][0]
    ok("V-call: the recomputed teams, grounds and counts match the golden workbook", teams == g_teams, (teams, g_teams))
    ok("V-count: four series teams, as the workbook states", len(series) == 4 and g_n == 4, (len(series), g_n))
    ok("V-trips: eighteen train trips join the Eastline group's offences", len(trips_used) == 18, len(trips_used))
    g_grid = {str(r[0]).replace("District ", "D"): [int(r[1]), int(r[2]), int(r[3])] for r in gw["2025 by district"]
              if r and isinstance(r[0], str) and r[0].startswith("District ")}
    ok("V-ask2: the 2025 grid matches the golden workbook cell for cell", grid == g_grid,
       [(k, grid[k], g_grid.get(k)) for k in grid if grid[k] != g_grid.get(k)])
    g_st = {r[0]: (int(r[1]), int(r[2])) for r in gw["Eastline stations"] if r and r[0] in east}
    ok("V-ask3: entries and calls match the golden workbook at every station",
       all(g_st[s] == (entries[s], calls[s]) for s in east), [(s, g_st.get(s), entries[s], calls[s]) for s in east])
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    f_teams = sorted((tuple("D" + x for x in t["districts"]), t["n"]) for t in figs["teams"])
    ok("V-figures: figures.json agrees with the recomputation", f_teams == teams and figs["ask_b"] == entries
       and figs["ask_c"] == calls and {k: v for k, v in figs["ask_a"].items()} == grid and figs["eastline_trips"] == len(trips_used))
    memo = docx_text(os.path.join(TASK, "golden", "summer_series_deployment_memo.docx"))
    ok("V-memo: the memo states the count and every team's offences", "four series teams" in memo and all(
        ("%d offences" % n) in memo for _, n in teams))
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    ok("V-submission: submission.md states the call and every grid row", "four series teams" in sub and all(
        ("District %s: %d" % (k[1:], v[0])) in sub for k, v in grid.items()))
    print("verify: %d failed" % len(FAIL))
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
