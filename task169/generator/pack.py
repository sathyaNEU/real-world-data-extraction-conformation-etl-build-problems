"""Write the evidence pack (target/) from the truth and the operating records. Nothing here decides anything: every
file is an export, a register, a document or a sheet as the organisation that keeps it would produce it."""
import csv
import io
import os
from datetime import date, datetime, timedelta, timezone

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import docs as D
import names as N
import postprocess as PP
import records as R
import world as W

F = dict(
    legacy="counts_summer2024_legacy.csv",
    platform="counts_summer2025_2026.parquet",
    register="counter_register.xlsx",
    inventory="cycleway_path_inventory_2026.xlsx",
    guide="cycle_design_guide_2023_section4.pdf",
    policy="cycleway_widening_allocation_policy_2026.pdf",
    notes="traffic_monitoring_data_notes.pdf",
    weather="weather_station_daily_2024-01-01_2026-09-30.csv",
    terms="school_term_dates_2023-2027.csv",
    log="counter_maintenance_log_2024-2026.csv",
    week="count_week_15min_2026-05-11_15.csv",
    volunteers="volunteer_count_may2026.xlsx",
    manifest="export_manifest.csv",
    dashboard="dashboard_headline_monthly_2019-2026.csv",
    events="events_programme_2024-2026.csv",
    app="activity_app_rides_monthly_2024-2026.csv",
)
DISTRACTORS = [F["dashboard"], F["events"], F["app"]]

# the Path Inventory: (ref, name, from, to, length m, minimum width m, surveyed, structure, surface, counter code)
INVENTORY = {
    "CW1": [("CW1-01", "Cathedral Green to St Anne's Gate", "Cathedral Green", "St Anne's Gate", 820, 4.2, "2024-04-16", "at grade", "asphalt", "TR1"),
            ("CW1-02", "St Anne's Gate to Mill Lane", "St Anne's Gate", "Tolland Bridge (north)", 1140, 3.7, "2024-04-16", "at grade", "asphalt", "TR2"),
            ("CW1-03", "Tolland Bridge", "Tolland Bridge (north)", "Tolland Bridge (south)", 96, 2.6, "2025-03-04", "bridge", "deck surfacing", "TR3"),
            ("CW1-04", "Mill Lane junction", "Tolland Bridge (south)", "Mill Lane", 60, 3.5, "2024-04-16", "at grade", "asphalt", None),
            ("CW1-05", "Mill Lane to Ashby Park", "Mill Lane", "Ashby Park", 1310, 3.2, "2023-05-22", "at grade", "asphalt", "TR4")],
    "CW2": [("CW2-01", "Station Square to Infirmary Road", "Station Square", "Infirmary Road", 640, 4.3, "2025-02-11", "at grade", "asphalt", "BF1"),
            ("CW2-02", "Infirmary Road crossing", "Infirmary Road", "Gasworks Lane", 45, 3.6, "2025-02-11", "crossing", "asphalt", None),
            ("CW2-03", "Gasworks Lane", "Gasworks Lane (west)", "Kiln Street", 380, 2.7, "2025-02-11", "at grade", "asphalt", "BF2"),
            ("CW2-04", "Kiln Street to Brickfields Estate", "Kiln Street", "Brickfields Estate", 920, 3.3, "2023-06-07", "at grade", "asphalt", "BF3")],
    "CW3": [("CW3-01", "Quayside", "Harbour Steps", "Boardwalk (west)", 760, 4.4, "2024-03-12", "promenade", "block paving", "EP1"),
            ("CW3-02", "The Boardwalk", "Boardwalk (west)", "Saltings", 410, 2.8, "2024-03-12", "boardwalk", "timber deck", "EP2"),
            ("CW3-03", "Saltings to Heron Point", "Saltings", "Heron Point", 1650, 3.1, "2023-04-18", "at grade", "resin bound gravel", "EP3"),
            ("CW3-04", "Heron Point slipway", "Heron Point", "Heron Point (east)", 70, 2.4, "2023-04-18", "at grade", "concrete", None),
            ("CW3-05", "Heron Point to Shingle Bay", "Heron Point (east)", "Shingle Bay", 2100, 3.6, "2023-04-18", "at grade", "asphalt", "EP4")],
    "CW4": [("CW4-01", "Exchange Street to Park Gates", "Exchange Street", "Park Gates", 540, 3.8, "2024-05-02", "at grade", "asphalt", "WP1"),
            ("CW4-02", "Lido Gate", "Park Gates", "Lido", 150, 2.55, "2024-05-02", "at grade", "asphalt", "WP2"),
            ("CW4-03", "Bandstand to Wardle Hill", "Lido", "Wardle Hill", 880, 3.4, "2024-05-02", "at grade", "asphalt", "WP3"),
            ("CW4-04", "Wardle Hill to Fenn Lane", "Wardle Hill", "Fenn Lane", 610, 3.9, "2023-07-11", "at grade", "asphalt", None)],
    "CW5": [("CW5-01", "Corn Exchange", "Cornmarket", "Butter Market", 310, 3.6, "2025-01-21", "at grade", "granite setts", "MS1"),
            ("CW5-02", "Butter Market", "Butter Market", "Guild Street", 180, 2.6, "2025-01-21", "at grade", "granite setts", "MS2"),
            ("CW5-03", "Guild Street", "Guild Street", "Tanners Row", 420, 3.2, "2025-01-21", "at grade", "asphalt", "MS3"),
            ("CW5-04", "Tanners Row", "Tanners Row", "Haymarket", 360, 3.05, "2025-01-21", "at grade", "asphalt", "MS4"),
            ("CW5-05", "Haymarket Steps ramp", "Haymarket", "Riverside", 120, 2.9, "2025-01-21", "ramp", "asphalt", "MS5")],
    "CW6": [("CW6-01", "Southgate to Belvoir Road", "Southgate", "Belvoir Road", 990, 3.9, "2024-06-25", "at grade", "asphalt", "SF1"),
            ("CW6-02", "Belvoir Road to Fenn Common", "Belvoir Road", "Fenn Common", 1420, 3.3, "2024-06-25", "at grade", "asphalt", "SF2"),
            ("CW6-03", "Fenn Common Bridge", "Fenn Common", "Fenn Common (south)", 88, 2.7, "2024-06-25", "bridge", "deck surfacing", "SF3"),
            ("CW6-04", "Fenn Common to Southfield Park", "Fenn Common (south)", "Southfield Park", 760, 4.0, "2023-08-15", "at grade", "asphalt", None)],
}
CW_NAMES = {cw: name for cw, name, segs in W.CYCLEWAYS}
SEG_REF = {s[9]: s[0] for cw, segs in INVENTORY.items() for s in segs if s[9]}

LOCAL_OFFSET_SUMMER = 1        # BST, every summer day June to August


def _utc_of_local(d, h, m=0):
    """UTC datetime of a local wall-clock time in the summer months (BST)"""
    return datetime(d.year, d.month, d.day, h, m) - timedelta(hours=LOCAL_OFFSET_SUMMER)


# ------------------------------------------------------------------ the counts as the counters recorded them
def recorded_summer(T):
    """per counter per summer: (days, n_in, n_out, lost bool, estimated bool, est_in, est_out) in local hours.
    Hours losing half or more are not recorded; hours losing less keep the riders of the minutes recorded."""
    out = {}
    for k, code in enumerate(W.SEGMENTS):
        out[code] = {}
        for y in W.SUMMERS:
            ds, lin, lout, nin, nout, comps = T["summer"][code][y]
            frac = R.lost_fraction(code, y, ds)
            rng = np.random.default_rng([W.SEED, 12, k, y])
            keep = 1.0 - frac
            a_in = np.where(frac > 0, rng.binomial(nin.astype(np.int64), np.clip(keep, 0, 1)), nin).astype(np.int64)
            a_out = np.where(frac > 0, rng.binomial(nout.astype(np.int64), np.clip(keep, 0, 1)), nout).astype(np.int64)
            lost = frac >= 0.5
            est = R.estimated_mask(code, y, ds) & ~lost
            e_in = np.round(lin).astype(np.int64)
            e_out = np.round(lout).astype(np.int64)
            out[code][y] = (ds, a_in, a_out, lost, est, e_in, e_out)
    return out


def flows_from_recorded(rec):
    """two-way counts per counter per summer, NaN where not recorded (lost or estimated): the golden's input"""
    fl = {}
    for code, per in rec.items():
        fl[code] = {}
        for y, (ds, a_in, a_out, lost, est, e_in, e_out) in per.items():
            a = (a_in + a_out).astype(float)
            a[lost | est] = np.nan
            fl[code][y] = a
    return fl


# ------------------------------------------------------------------ writers
def _write_csv(path, header, rows, delim=",", crlf=False, pre=None):
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=delim, lineterminator="\r\n" if crlf else "\n")
    if pre:
        for line in pre:
            buf.write(line + ("\r\n" if crlf else "\n"))
    w.writerow(header)
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
    return len(rows)


def write_legacy(out, rec):
    rows = []
    for code in sorted(W.SEGMENTS, key=lambda c: N.LEGACY_NAMES[c]):
        ds, a_in, a_out, lost, est, e_in, e_out = rec[code][2024]
        for i, d in enumerate(ds):
            for h in range(24):
                if lost[i, h]:
                    c1 = c2 = ""
                else:
                    cin, cout = int(a_in[i, h]), int(a_out[i, h])
                    c1, c2 = (cin, cout) if N.CH1_IN[code] else (cout, cin)
                rows.append([N.LEGACY_NAMES[code], d.strftime("%d/%m/%Y"), "%02d:00" % h, c1, c2])
    pre = ["Calvermouth City Council traffic counts archive;cycle counters;hourly;01/06/2024 to 31/08/2024"]
    return _write_csv(os.path.join(out, F["legacy"]), ["Site", "Date", "Hour", "Ch1", "Ch2"], rows, delim=";", crlf=True,
                      pre=pre)


def write_platform(out, rec):
    cid, ts, dr, cnt, st = [], [], [], [], []
    for code in sorted(W.SEGMENTS, key=lambda c: N.COUNTER_IDS[c]):
        for y in (2025, 2026):
            ds, a_in, a_out, lost, est, e_in, e_out = rec[code][y]
            for i, d in enumerate(ds):
                for h in range(24):
                    t = _utc_of_local(d, h).replace(tzinfo=timezone.utc)
                    for direction, a, e in (("in", a_in, e_in), ("out", a_out, e_out)):
                        cid.append(N.COUNTER_IDS[code])
                        ts.append(t)
                        dr.append(direction)
                        if lost[i, h]:
                            cnt.append(0)
                            st.append("no_data")
                        elif est[i, h]:
                            cnt.append(int(e[i, h]))
                            st.append("estimated")
                        else:
                            cnt.append(int(a[i, h]))
                            st.append("ok")
    tab = pa.table({"counter_id": pa.array(cid, pa.string()),
                    "timestamp_utc": pa.array(ts, pa.timestamp("s", tz="UTC")),
                    "direction": pa.array(dr, pa.string()),
                    "count": pa.array(cnt, pa.int32()),
                    "status": pa.array(st, pa.string())})
    pq.write_table(tab, os.path.join(out, F["platform"]), compression="snappy", row_group_size=65536,
                   use_dictionary=True, write_statistics=True)
    return len(cid)


def _sheet(ws, header, rows, widths=None, bold_header=True):
    ws.append(header)
    if bold_header:
        for c in ws[1]:
            c.font = Font(bold=True)
            c.fill = PatternFill("solid", fgColor="D9E1F2")
    for r in rows:
        ws.append(r)
    for i, wdt in enumerate(widths or [], 1):
        ws.column_dimensions[get_column_letter(i)].width = wdt
    ws.freeze_panes = "A2"


def write_register(out):
    path = os.path.join(out, F["register"])
    wb = Workbook()
    ws = wb.active
    ws.title = "Register"
    rows = []
    installed = {"TR1": "2019-03-14", "BF1": "2019-03-14", "EP1": "2018-07-02", "WP1": "2019-05-20", "SF1": "2020-02-26"}
    for code in sorted(W.SEGMENTS, key=lambda c: N.COUNTER_IDS[c]):
        seg = W.SEGMENTS[code]
        dash = code in W.HEADLINE
        ch1 = "towards centre" if N.CH1_IN[code] else "away from centre"
        if dash:
            if code == "MS1":
                rows.append([N.MS1_OLD_ID, "Corn Exchange (old unit)", N.LEGACY_NAMES[code], seg["cw"], SEG_REF[code],
                             "dashboard", "inductive loop", ch1, "2016-04-11", "2025-03-21", "2016-04-11", "2025-03-20",
                             "legacy only", "Replaced by CVC-1207; side-by-side 12 to 20 March 2025"])
                rows.append([N.COUNTER_IDS[code], "Corn Exchange", N.LEGACY_NAMES[code], seg["cw"], SEG_REF[code],
                             "dashboard", "inductive loop", "", "2025-03-12", "", "2025-03-21", "",
                             "2025-03-12", "Replacement unit for CVC-0388"])
                continue
            rows.append([N.COUNTER_IDS[code], seg["name"], N.LEGACY_NAMES[code], seg["cw"], SEG_REF[code], "dashboard",
                         N.TECH[code], ch1, installed[code], "", installed[code], "", "2025-01-06", ""])
        else:
            rows.append([N.COUNTER_IDS[code], seg["name"], N.LEGACY_NAMES[code], seg["cw"], SEG_REF[code], "summer",
                         N.TECH[code], ch1, "2022-05-31", "", "2022-06-01", "", "2025-06-01",
                         "Installed each year from late May to early September"])
    rows.sort(key=lambda r: r[0])
    _sheet(ws, ["counter_id", "site_name", "legacy_site_name", "cycleway", "segment_ref", "type", "technology",
                "ch1_direction", "installed", "removed", "unit_of_record_from", "unit_of_record_to", "platform_from",
                "notes"], rows, [11, 34, 30, 9, 11, 10, 22, 17, 11, 11, 18, 17, 13, 52])
    wb.save(path)
    PP.normalize_ooxml(path, N.PEOPLE["tmo"][0], N.PEOPLE["tmo"][0], "2023-01-17T10:05:00Z", "2026-10-02T13:20:00Z",
                       excel=True, company=N.COUNCIL)
    return len(rows)


def write_inventory(out):
    path = os.path.join(out, F["inventory"])
    wb = Workbook()
    ws = wb.active
    ws.title = "Segments"
    rows = []
    for cw in sorted(INVENTORY):
        for ref, name, a, b, ln, wd, sv, struct, surf, code in INVENTORY[cw]:
            rows.append([cw, CW_NAMES[cw], ref, name, a, b, ln, wd, sv, struct, surf,
                         N.COUNTER_IDS[code] if code else ""])
    _sheet(ws, ["cycleway", "cycleway_name", "segment_ref", "segment_name", "from", "to", "length_m", "min_width_m",
                "surveyed", "structure", "surface", "counter_id"], rows, [9, 15, 11, 34, 24, 24, 9, 12, 11, 11, 18, 11])
    for r in ws.iter_rows(min_row=2, min_col=8, max_col=8):
        for c in r:
            c.number_format = "0.00"
    w2 = wb.create_sheet("About")
    for line in (["Cycleway Path Inventory, segment register"], ["Kept by", "Highways Design, %s" % N.COUNCIL],
                 ["Updated", "2026-04-28"], ["Widths", "Minimum clear width over the segment, metres, from the latest survey"],
                 ["Lengths", "Metres along the centre line"], ["Counters", "counter_id is the counter on the segment, if any"]):
        w2.append(line)
    w2.column_dimensions["A"].width = 12
    w2.column_dimensions["B"].width = 70
    wb.save(path)
    PP.normalize_ooxml(path, N.PEOPLE["hde"][0], N.PEOPLE["hde"][0], "2022-09-08T09:40:00Z", "2026-04-28T15:12:00Z",
                       excel=True, company=N.COUNCIL)
    return len(rows)


def write_weather(out, T):
    wx = T["weather"]
    rows = []
    for i, d in enumerate(wx["days"]):
        if d in W.WEATHER_MISSING:
            rows.append([d.isoformat(), "", "", "", ""])
        else:
            rows.append([d.isoformat(), "%.1f" % wx["tmax"][i], "%.1f" % wx["tmin"][i], "%.1f" % wx["rain"][i],
                         "%.1f" % wx["sun"][i]])
    return _write_csv(os.path.join(out, F["weather"]), ["date", "tmax_c", "tmin_c", "rain_mm", "sunshine_h"], rows)


def write_terms(out):
    rows = []
    hols = W.SCHOOL_HOLIDAYS

    def ay(d):
        y = d.year if d.month >= 9 else d.year - 1
        return "%d-%02d" % (y, (y + 1) % 100)
    # terms run between holidays; the autumn term 2023 starts on 4 September 2023
    starts = [date(2023, 9, 4)] + [b + timedelta(days=1) for a, b, n in hols]
    names = {"Christmas": "Spring term", "February half term": "Spring term (second half)", "Easter": "Summer term",
             "May half term": "Summer term (second half)", "Summer": "Autumn term",
             "October half term": "Autumn term (second half)"}
    prev_name = "Autumn term"
    for k, (a, b, n) in enumerate(hols):
        s = starts[k]
        while s.weekday() >= 5:
            s += timedelta(days=1)
        e = a - timedelta(days=1)
        while e.weekday() >= 5:
            e -= timedelta(days=1)
        if s <= e:
            rows.append([ay(s), "term", prev_name, s.isoformat(), e.isoformat()])
        rows.append([ay(a), "school holiday", n, a.isoformat(), b.isoformat()])
        prev_name = names[n]
    for d in sorted(W.BANK_HOLIDAYS):
        rows.append([ay(d), "bank holiday", "Bank holiday", d.isoformat(), d.isoformat()])
    rows.sort(key=lambda r: (r[3], r[1]))
    return _write_csv(os.path.join(out, F["terms"]), ["academic_year", "type", "name", "first_day", "last_day"], rows)


def write_log(out, rows):
    def uk(s):
        return datetime.strptime(s, "%Y-%m-%d %H:%M").strftime("%d/%m/%Y %H:%M") if s else ""
    body = [[r["job_no"], r["parent_job"], r["asset_id"], r["site"], r["logged_by"], r["job_type"], uk(r["reported"]),
             uk(r["attended"]), uk(r["closed"]), r["downtime"], r["notes"]] for r in sorted(rows, key=lambda r: r["job_no"])]
    return _write_csv(os.path.join(out, F["log"]), ["job_no", "parent_job", "asset_id", "site", "logged_by", "job_type",
                                                     "reported", "attended", "closed", "downtime", "notes"], body)


def write_count_week(out, CW):
    """the platform's interval export: each 15-minute interval stamped at its end, in UTC, selected on the stamp from
    23:00 UTC on 10 May to 23:00 UTC on 15 May (the five local days). The Quayside and Corn Exchange loggers were
    restarted from a laptop on local time in the spring and kept it until the summer round, so their stamps are local
    interval ends."""
    lo = datetime(2026, 5, 10, 23, 0)
    hi = datetime(2026, 5, 15, 23, 0)
    rows = []
    for code in sorted(W.HEADLINE, key=lambda c: N.COUNTER_IDS[c]):
        tr = CW[code]
        recs = []
        for (d, h, q), (t_in, t_out, c_in, c_out, kept) in tr.items():
            if not kept:
                continue
            end_local = datetime(d.year, d.month, d.day, h, 0) + timedelta(minutes=15 * (q + 1))
            stamp = end_local if code in R.LOCAL_CLOCK else end_local - timedelta(hours=1)
            if lo <= stamp < hi:
                recs.append((stamp, c_in, c_out))
        recs.sort()
        for stamp, c_in, c_out in recs:
            s = stamp.strftime("%Y-%m-%dT%H:%M:%SZ")
            rows.append([N.COUNTER_IDS[code], s, "in", int(c_in)])
            rows.append([N.COUNTER_IDS[code], s, "out", int(c_out)])
    return _write_csv(os.path.join(out, F["week"]), ["counter_id", "timestamp_utc", "direction", "count"], rows)


VOL_TABS = {"TR1": "Cathedral Green", "MS1": "Corn Exchange", "BF1": "Station Sq", "WP1": "Exchange St",
            "EP1": "Quayside", "SF1": "Southgate"}
VOL_WEATHER = {"TR1": "Dry, cloudy, light wind", "MS1": "Dry, cloudy, light wind", "BF1": "Sunny spells, dry",
               "WP1": "Sunny spells, dry", "EP1": "Dry and bright, breezy on the quay", "SF1": "Dry and bright"}


def write_volunteers(out, sheets):
    path = os.path.join(out, F["volunteers"])
    wb = Workbook()
    first = True
    order = sorted(R.COUNT_DAYS, key=lambda c: (R.COUNT_DAYS[c], N.COUNTER_IDS[c]))
    for code in order:
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = VOL_TABS[code]
        d = R.COUNT_DAYS[code]
        ws.append(["%s, May 2026 cycle count" % N.FORUM])
        ws["A1"].font = Font(bold=True, size=12)
        ws.append(["Site", "%s (council counter %s)" % (N.LEGACY_NAMES[code], N.COUNTER_IDS[code])])
        ws.append(["Date", d.strftime("%A %d %B %Y").replace(" 0", " ")])
        ws.append(["Weather", VOL_WEATHER[code]])
        ws.append(["Tallies", "riders passing the counter cross-section, one volunteer per direction on the track"
                              " and one on the road"])
        ws.append([])
        ws.append(["Time", "Track towards centre", "Track away from centre", "Road (both ways)", "Notes"])
        for c in ws[7]:
            c.font = Font(bold=True)
        rows = sheets[code]
        tot = [0, 0, 0]
        for a, b in R.WINDOWS:
            if code == "MS1" and a == 7:
                for h in range(a, b):
                    vi = sum(r[2] for r in rows if r[0] == h)
                    vo = sum(r[3] for r in rows if r[0] == h)
                    rd = sum(r[4] for r in rows if r[0] == h)
                    ws.append(["%02d:00-%02d:00" % (h, h + 1), vi, vo, rd,
                               "Tallied by the hour this morning (one volunteer short)" if h == a else ""])
                    tot = [tot[0] + vi, tot[1] + vo, tot[2] + rd]
            else:
                for (h, q, vi, vo, rd) in [r for r in rows if a <= r[0] < b]:
                    m0 = 15 * q
                    t1 = datetime(2026, 1, 1, h, m0) + timedelta(minutes=15)
                    ws.append(["%02d:%02d-%s" % (h, m0, t1.strftime("%H:%M")), vi, vo, rd, ""])
                    tot = [tot[0] + vi, tot[1] + vo, tot[2] + rd]
            ws.append([])
        ws.append(["Total", tot[0], tot[1], tot[2], ""])
        ws[ws.max_row][0].font = Font(bold=True)
        ws.column_dimensions["A"].width = 14
        for col in "BCD":
            ws.column_dimensions[col].width = 21
        ws.column_dimensions["E"].width = 48
    wb.save(path)
    PP.normalize_ooxml(path, N.PEOPLE["vol"][0], N.PEOPLE["vol"][0], "2026-05-11T19:30:00Z", "2026-05-21T20:45:00Z",
                       excel=True, company=N.FORUM)
    return sum(len(v) for v in sheets.values())


def write_dashboard(out, rows):
    name = {c: N.LEGACY_NAMES[c] for c in W.HEADLINE}
    body = []
    for r in sorted(rows, key=lambda r: (r["year"], r["month"], N.COUNTER_IDS[r["site"]])):
        if (r["year"], r["month"]) > (2026, 9):
            continue
        body.append(["%04d-%02d" % (r["year"], r["month"]), name[r["site"]], r["total"], r["source"]])
    pre = ["# Active travel dashboard: cyclists per month past the six dashboard counters, both directions. Days a "
           "counter did not record carry the platform estimate. Refreshed 2026-10-05, Traffic Monitoring Unit, v2026.10"]
    return _write_csv(os.path.join(out, F["dashboard"]), ["month", "site", "cyclists", "source"], body, pre=pre)


def write_events(out):
    body = [[d, n, loc, att] for d, n, loc, att in sorted(R.EVENTS)]
    return _write_csv(os.path.join(out, F["events"]), ["date", "event", "location", "expected_attendance"], body)


def write_app(out, rows):
    body = [[r["month"], r["cycleway"], r["rides"], r["athletes"]] for r in rows]
    return _write_csv(os.path.join(out, F["app"]), ["month", "cycleway", "rides", "people"], body)


def write_manifest(out, n):
    rows = [
        [F["legacy"], "Traffic Monitoring Unit", "legacy logging platform archive", "2026-10-09 07:42",
         "01/06/2024 to 31/08/2024", n[F["legacy"]]],
        [F["platform"], "Traffic Monitoring Unit", "counter platform, hourly export", "2026-10-09 07:55",
         "2025-06-01 to 2026-08-31", n[F["platform"]]],
        [F["week"], "Traffic Monitoring Unit", "counter platform, interval export", "2026-10-09 08:03",
         "2026-05-11 to 2026-05-15", n[F["week"]]],
        [F["log"], "Traffic Monitoring Unit", "job system, counter assets", "2026-10-09 09:10", "2024-01-01 to 2026-10-08",
         n[F["log"]]],
        [F["register"], "Traffic Monitoring Unit", "counter register", "2026-10-02", "", n[F["register"]]],
        [F["inventory"], "Highways Design", "Path Inventory", "2026-04-28", "", n[F["inventory"]]],
        [F["weather"], "Traffic Monitoring Unit", "weather station CVM-WX1", "2026-10-09 08:20", "2024-01-01 to 2026-09-30",
         n[F["weather"]]],
        [F["terms"], "Education Services", "published term dates", "2026-09-15", "2023-24 to 2026-27", n[F["terms"]]],
        [F["volunteers"], N.FORUM, "count sheets", "2026-05-21", "2026-05-12 to 2026-05-14", ""],
        [F["dashboard"], "Traffic Monitoring Unit", "active travel dashboard", "2026-10-05", "2019-01 to 2026-09",
         n[F["dashboard"]]],
        [F["events"], "Events and Culture", "events programme", "2026-09-30", "2024 to 2026", n[F["events"]]],
        [F["app"], "Active Travel Team", "activity app partner data", "2026-10-06", "2024-01 to 2026-09", n[F["app"]]],
        [F["policy"], "Active Travel Team", "AT-POL-07 v1.0", "2026-03-18", "", ""],
        [F["guide"], "Highways Design", "Cycle Design Guide 2023, Section 4", "2025-02-14", "", ""],
        [F["notes"], "Traffic Monitoring Unit", "data notes, issue 4", "2026-10-02", "", ""],
    ]
    return _write_csv(os.path.join(out, F["manifest"]), ["file", "owner", "source", "pulled_or_issued", "covers", "rows"],
                      rows)


def build_pack(out):
    os.makedirs(out, exist_ok=True)
    T = W.build_truth()
    CW = R.build_count_week(T, np.random.default_rng([W.SEED, 6]))
    for k in range(500):                 # the first draw whose shortfalls sit clear of their printed cells' edges
        sheets = R.build_volunteers(CW, np.random.default_rng([W.SEED, 7, k]))
        if R.volunteers_ok(CW, sheets):
            break
    log_rows = R.build_log(np.random.default_rng([W.SEED, 5]))
    dash = R.build_dashboard(T, np.random.default_rng([W.SEED, 8]))
    app = R.build_app_rides(T, np.random.default_rng([W.SEED, 9]))
    rec = recorded_summer(T)
    n = {}
    n[F["legacy"]] = write_legacy(out, rec)
    n[F["platform"]] = write_platform(out, rec)
    n[F["register"]] = write_register(out)
    n[F["inventory"]] = write_inventory(out)
    n[F["weather"]] = write_weather(out, T)
    n[F["terms"]] = write_terms(out)
    n[F["log"]] = write_log(out, log_rows)
    n[F["week"]] = write_count_week(out, CW)
    n[F["volunteers"]] = write_volunteers(out, sheets)
    n[F["dashboard"]] = write_dashboard(out, dash)
    n[F["events"]] = write_events(out)
    n[F["app"]] = write_app(out, app)
    D.policy_pdf(os.path.join(out, F["policy"]))
    D.design_guide_pdf(os.path.join(out, F["guide"]), W.CAPACITY_BANDS)
    D.data_notes_pdf(os.path.join(out, F["notes"]))
    n[F["manifest"]] = write_manifest(out, n)
    return n, dict(T=T, CW=CW, sheets=sheets, log=log_rows, rec=rec, dash=dash, app=app)
