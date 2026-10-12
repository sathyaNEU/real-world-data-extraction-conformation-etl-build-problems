"""Writers for target/: the complaint export and its field reference, the retired system's closing export, the
station's 5-minute records, readme and maintenance log, the procedure, the odor source list, the boundary, the
annual totals, and the distractors (the operators' monthly reports, the station's PM2.5 record, the airport's
hourly weather)."""
import csv
import datetime as dt
import json
import math
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

import core
import docs as D
import postprocess as PP
import records as R
import world as WD

FILES = {
    "complaints": "odor_complaints_export_2026-10-02.csv",
    "fields": "complaint_export_fields.txt",
    "ocs": "ocs_open_complaints_2025-12-31.csv",
    "met": "hfs_met_5min_2026-01-01_2026-09-30.csv",
    "readme": "hfs_station_readme.txt",
    "maint": "hfs_station_maintenance_log_2026.csv",
    "procedure": "cp14_odor_complaint_procedure_rev4.pdf",
    "permits": "odor_source_list_2026.xlsx",
    "boundary": "ukvaqmd_boundary.geojson",
    "totals": "odor_complaint_totals_2019-2025.csv",
    "operators": "operator_monthly_reports_2026.xlsx",
    "pm25": "hfs_pm25_hourly_2026.csv",
    "airport": "kestrel_county_airport_hourly_2026.csv",
}
DISTRACTORS = ["operators", "pm25", "airport"]
ZIP = "95957"


def _w(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def geocode(h):
    """The system geocodes an address the same way every time: most to the parcel, some along the street segment."""
    rng = WD.rng_for("geo", h["hid"])
    if h["unit"] is None and rng.random() < 0.11:
        ang = rng.uniform(0, 2 * math.pi)
        r = rng.uniform(0.025, 0.085)
        lat, lon = core.to_latlon(h["x"] + r * math.cos(ang), h["y"] + r * math.sin(ang))
        return round(lat, 6), round(lon, 6), "Street segment"
    return round(h["lat"], 6), round(h["lon"], 6), "Parcel"


def complaint_rows(W, rows):
    H = W["H"]
    out = []
    rng = WD.rng_for("export")
    allr = sorted(rows, key=lambda r: (r["received"], r["contact"], r["noticed"]))
    no = 0
    for r in allr:
        no += 1 + (1 if rng.random() < 0.03 else 0)
        if r["kind"] == "routed":
            lat, lon, gm = round(r["lat"], 6), round(r["lon"], 6), "Street segment"
        else:
            lat, lon, gm = geocode(H[r["hid"]])
        r["no"] = "OC-26-%05d" % no
        r["lat_x"], r["lon_x"], r["geo_x"] = lat, lon, gm
        status = "Open" if r["received"] >= dt.datetime(2026, 9, 28) and rng.random() < 0.6 else "Closed"
        out.append([r["no"], r["received"].strftime("%Y-%m-%d %H:%M"), r["channel"],
                    R.exported_noticed(r).strftime("%Y-%m-%d %H:%M"), r["contact"], r["address"], core.TOWN, ZIP,
                    "%.6f" % lat, "%.6f" % lon, gm, r["desc"], r["intensity"], r["duration"], r["follow"], r["finding"],
                    r["staff"], status])
    return out, allr


HEAD_C = ["complaint_no", "received", "channel", "noticed", "contact_id", "address", "city", "zip", "latitude",
          "longitude", "geocode_match", "description", "intensity", "duration", "follow_up", "finding", "staff", "status"]


def write_complaints(W, rows, target):
    out, allr = complaint_rows(W, rows)
    _w(os.path.join(target, FILES["complaints"]), HEAD_C, out)
    open(os.path.join(target, FILES["fields"]), "w", encoding="utf-8").write(
        D.FIELDS.format(export=core.EXPORT.strftime("%B %-d, %Y at %H:%M")))
    return allr


def write_ocs(legacy, target):
    rows = []
    for r in legacy:
        rec = r["received"]
        rows.append([r["ocs_no"], rec.strftime("%m/%d/%Y"), rec.strftime("%I:%M %p"), r["address"].upper(), r["desc"],
                     "OPEN", ["ES", "JR", "AW"][int(r["ocs_no"][-1]) % 3]])
    _w(os.path.join(target, FILES["ocs"]), ["case_no", "date_recd", "time_recd", "location", "complaint_text", "case_status",
                                           "assigned"], rows)


def write_met(station, target):
    rows = []
    for d in core.DAYS:
        for (mi, sp, dr, sig, t2, t10, sol, qc) in station[d]:
            t = dt.datetime(d.year, d.month, d.day) + dt.timedelta(minutes=mi)
            if qc == "M":
                rows.append([t.strftime("%Y-%m-%d %H:%M"), "", "", "", "", "", "", "M"])
            else:
                rows.append([t.strftime("%Y-%m-%d %H:%M"), "%.2f" % sp, "%.1f" % dr, "%.1f" % sig, "%.1f" % t2, "%.1f" % t10,
                             "%d" % round(sol), "V"])
    _w(os.path.join(target, FILES["met"]), ["datetime_pst", "ws_ms", "wd_deg", "sigma_theta_deg", "t2m_c", "t10m_c",
                                           "solar_wm2", "qc"], rows)
    open(os.path.join(target, FILES["readme"]), "w", encoding="utf-8").write(D.README.format(rows=len(rows)))
    return len(rows)


AUDIT = {
    "AW": ["Monthly audit: wind vane held on the north alignment mark and propeller held still for the bearing check; "
           "logger clock checked",
           "Monthly wind audit. Vane held at N mark, prop held, bearing torque and threshold OK. Logger time synced"],
    "RH": ["Monthly audit: wind vane held at true north for alignment, propeller held, bearing check, data logger check",
           "Monthly audit, vane held at north mark, prop held stationary for bearing check, DAS clock OK"],
}


def write_maint(held, target):
    rows = []
    aud = held[:-1]
    for (a, b) in aud:
        tech = ["AW", "RH"][a.month % 2]
        rows.append([a.strftime("%Y-%m-%d"), a.strftime("%H:%M"), b.strftime("%H:%M"), tech,
                     AUDIT[tech][(a.month // 2) % 2]])
    a, b = held[-1]
    rows.append([a.strftime("%Y-%m-%d"), a.strftime("%H:%M"), "", "RH", "Wind monitor bearing failure; monitor removed "
                 "for replacement, cable left unplugged"])
    rows.append([b.strftime("%Y-%m-%d"), "", b.strftime("%H:%M"), "RH", "New wind monitor installed and connected; "
                 "orientation checked against the alignment mark"])
    # the station's other work
    for t, text in R.other_work():
        rows.append([t.strftime("%Y-%m-%d"), t.strftime("%H:%M"), "", "RH", text])
    rows.sort(key=lambda r: (r[0], r[1] or r[2]))
    _w(os.path.join(target, FILES["maint"]), ["date", "start_pst", "end_pst", "technician", "work"], rows)


def write_procedure(target):
    D.procedure_pdf(os.path.join(target, FILES["procedure"]))


def _sheet(ws, head, rows, widths=None, fmt=None):
    ws.append(head)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE7DF")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append(r)
    if widths:
        for i, w in enumerate(widths):
            ws.column_dimensions[chr(65 + i)].width = w
    if fmt:
        for col, f in fmt.items():
            for row in ws.iter_rows(min_row=2, min_col=col, max_col=col):
                for c in row:
                    c.number_format = f
    ws.freeze_panes = "A2"


def write_permits(target):
    wb = Workbook()
    ws = wb.active
    ws.title = "Odor sources"
    addr = {"landfill": "8800 Pine Gulch Rd", "compost": "6150 Ridgeway Canyon Rd", "wwtp": "300 Creek Bend Rd",
            "render": "4420 North Slope Rd", "mush": "2975 Sutter Bend Rd"}
    proc = {"landfill": "Municipal solid waste landfill; active face, landfill gas collection and flare",
            "compost": "Open windrow composting of green waste and food waste",
            "wwtp": "Activated sludge treatment, anaerobic digestion, biosolids drying",
            "render": "Rendering of meat and poultry by-products; cookers with thermal oxidizer",
            "mush": "Phase I mushroom substrate composting (straw, manure, gypsum) on an open wharf"}
    thr = {"landfill": "1,150 tons per day", "compost": "500 tons per day of feedstock",
           "wwtp": "4.2 million gallons per day", "render": "260 tons per day of raw material",
           "mush": "180 tons per day of substrate ingredients"}
    expires = {"landfill": dt.date(2030, 3, 31), "compost": dt.date(2027, 7, 31), "wwtp": dt.date(2027, 11, 30),
               "render": dt.date(2028, 2, 29), "mush": dt.date(2027, 1, 31)}
    rows = []
    for k in core.FKEYS:
        f = core.FAC[k]
        rows.append([f["name"], f["permit"], f["operator"], addr[k], f["lat"], f["lon"], proc[k], thr[k], expires[k]])
    _sheet(ws, ["Facility", "Permit", "Operator", "Address", "Latitude", "Longitude", "Odor-producing process",
                "Permitted throughput", "Permit to operate expires"], rows,
           widths=[38, 9, 34, 26, 11, 12, 52, 30, 14], fmt={5: "0.00000", 6: "0.00000", 9: "mm/dd/yyyy"})
    acts = [(dt.date(2025, 3, 18), "landfill", "Title V permit renewed"),
            (dt.date(2025, 7, 21), "compost", "Permit to operate renewed"),
            (dt.date(2025, 9, 2), "landfill", "Authority to construct issued: Cell 7"),
            (dt.date(2025, 11, 4), "wwtp", "Permit issued: emergency standby generator (diesel, 450 kW)"),
            (dt.date(2026, 1, 26), "mush", "Permit transferred: Sutter Bend Farms (partnership) to Sutter Bend "
                                           "Mushroom Farms Inc., no change in operations"),
            (dt.date(2026, 2, 10), "render", "Change of responsible official")]
    acts += [(core.CHANGES[k][0], k, core.CHANGES[k][1]) for k in core.FKEYS]
    acts.sort()
    ws3 = wb.create_sheet("Permit actions")
    _sheet(ws3, ["Date", "Facility", "Permit", "Action"],
           [[d, core.FAC[k]["name"], core.FAC[k]["permit"], txt] for d, k, txt in acts],
           widths=[12, 38, 9, 90], fmt={1: "mm/dd/yyyy"})
    ws2 = wb.create_sheet("Notes")
    for line in ["Odor source list, Compliance Division, as of September 30, 2026.",
                 "Latitude and longitude locate each facility's main odor-producing area (the landfill's active face, "
                 "the compost windrow pad, the treatment plant's drying beds, the rendering cookers, the substrate wharf).",
                 "Ridgeway Organics' food waste comes under collection contracts with the City of Harlow Falls (from "
                 "March 2, 2026) and Kestrel County (from June 1, 2026), both running to June 30, 2030.",
                 "Each facility's odor complaint contact is on its permit file."]:
        ws2.append([line])
    ws2.column_dimensions["A"].width = 120
    p = os.path.join(target, FILES["permits"])
    wb.save(p)
    PP.normalize_xlsx(p, "Compliance Division", "2026-01-05T16:20:00Z", "2026-09-30T22:10:00Z")


def boundary_km():
    """The district line on the valley floor follows Kestrel Creek on the west; section lines and the ridge
    elsewhere. x, y in km from the station."""
    rng = WD.rng_for("boundary")
    west = [(-4.2, -9.0), (-4.4, -1.9), (-3.2, 0.9), (-3.0, 9.0)]
    pts = []
    for (x0, y0), (x1, y1) in zip(west, west[1:]):
        ln = math.hypot(x1 - x0, y1 - y0)
        n = max(2, int(ln / 0.42))
        nx, ny = (y1 - y0) / ln, -(x1 - x0) / ln
        for i in range(n):
            f = i / n
            off = 0.10 * math.sin(2.3 * (y0 + f * (y1 - y0))) + float(rng.normal(0, 0.025))
            pts.append((x0 + f * (x1 - x0) + off * nx, y0 + f * (y1 - y0) + off * ny))
    pts += [(-3.0, 9.0), (2.4, 9.0), (2.4, 8.2), (9.5, 8.2)]
    for i in range(1, 12):
        pts.append((9.5 + 0.35 * math.sin(1.7 * i) + float(rng.normal(0, 0.08)), 8.2 - i * 17.2 / 12))
    pts += [(9.5, -9.0), (3.1, -9.0), (3.1, -9.3), (-4.2, -9.3)]
    return pts


def boundary_polygon():
    return [core.to_latlon(x, y) for x, y in boundary_km()]


def point_in(lat, lon, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        (y1, x1), (y2, x2) = poly[i], poly[(i + 1) % n]
        if (y1 > lat) != (y2 > lat):
            xi = x1 + (lat - y1) * (x2 - x1) / (y2 - y1)
            if lon < xi:
                inside = not inside
    return inside


def write_boundary(target):
    poly = boundary_polygon()
    ring = [(lon, lat) for lat, lon in poly] + [(poly[0][1], poly[0][0])]
    coords = ",\n".join("     [%.6f, %.6f]" % xy for xy in ring)
    txt = ('{\n "type": "FeatureCollection",\n "name": "ukvaqmd_boundary",\n "crs": {"type": "name", "properties": '
           '{"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},\n "features": [\n  {\n   "type": "Feature",\n   "properties": '
           '{"district": "%s", "source": "District boundary as filed with the Air Resources Board, 2019"},\n'
           '   "geometry": {\n    "type": "Polygon",\n    "coordinates": [\n     [\n%s\n     ]\n    ]\n   }\n  }\n ]\n}\n'
           % (core.ORG, coords.replace("     [", "      [")))
    json.loads(txt)
    open(os.path.join(target, FILES["boundary"]), "w", encoding="utf-8").write(txt)


def write_totals(target):
    rows = [[2019, 171, 118], [2020, 188, 131], [2021, 164, 120], [2022, 203, 139], [2023, 182, 127], [2024, 207, 144],
            [2025, 196, 136]]
    _w(os.path.join(target, FILES["totals"]), ["year", "odor_complaints_received", "households"], rows)


def _after(m, day):
    """The share of month m (its first day) from `day` on."""
    nd = (dt.date(m.year + (m.month == 12), m.month % 12 + 1, 1) - m).days
    return min(1.0, max(0.0, ((m + dt.timedelta(nd)) - day).days / nd))


def write_operators(target):
    rng = WD.rng_for("operators")
    wb = Workbook()
    first = True
    months = [dt.date(2026, m, 1) for m in range(1, 10)]
    ndays = lambda m: (dt.date(2026, m.month + 1, 1) - m).days
    spec = {
        "Pine Gulch": (["Month", "Tons received", "Active cell", "Landfill gas flared (scfm, average)"],
                       lambda m: [m, int(ndays(m) * (905 + 70 * math.sin(math.pi * (m.month - 3) / 6.0)) + rng.normal(0, 600)),
                                  "6" if m.month < 5 else ("6 and 7 (7 from May 11)" if m.month == 5 else "7"),
                                  int(1450 + rng.normal(0, 40))]),
        "Ridgeway Organics": (["Month", "Green waste received (cubic yards)", "Food waste received (tons)",
                               "Windrows active", "Finished compost shipped (cubic yards)"],
                              lambda m: [m, int(9800 + 3400 * (m.month in (4, 5, 6, 10)) + rng.normal(0, 500)),
                                         0 if m.month < 3 else int((1150 if m.month < 6 else 2350) + rng.normal(0, 90)),
                                         int(26 + (m.month >= 3) * 6 + (m.month >= 6) * 5 + rng.integers(-2, 3)),
                                         int(5200 + rng.normal(0, 700))]),
        "Harlow Falls WPCP": (["Month", "Average flow (MGD)", "Biosolids produced (dry tons)", "Drying beds in use at "
                               "month end"],
                              lambda m: [m, round(2.9 + 0.3 * math.cos(m.month / 2.0) + rng.normal(0, 0.05), 2),
                                         round(118 + rng.normal(0, 6), 1), 0 if m.month < 4 else 4]),
        "Kestrel Valley Rendering": (["Month", "Raw material received (tons)", "Cooking shifts", "Oxidizer hours"],
                                     lambda m: [m, int(4300 + _after(m, dt.date(2026, 6, 15)) * 1900 + rng.normal(0, 150)),
                                                1 if m.month < 6 else (2 if m.month > 6 else "1, then 2 from June 15"),
                                                int(310 + _after(m, dt.date(2026, 6, 15)) * 150 + rng.normal(0, 8))]),
        "Sutter Bend": (["Month", "Substrate ingredients received (tons)", "Wharf bays", "Phase I batches"],
                        lambda m: [m, int(3600 + _after(m, dt.date(2026, 5, 18)) * 700 + rng.normal(0, 120)),
                                   6 if m.month < 5 else ("6, then 8 from May 18" if m.month == 5 else 8),
                                   int(18 + round(_after(m, dt.date(2026, 5, 18)) * 4) + rng.integers(-1, 2))]),
    }
    for name, (head, fn) in spec.items():
        ws = wb.active if first else wb.create_sheet(name)
        if first:
            ws.title = name
            first = False
        _sheet(ws, head, [fn(m) for m in months], widths=[12] + [24] * (len(head) - 1), fmt={1: "mmm yyyy"})
    p = os.path.join(target, FILES["operators"])
    wb.save(p)
    PP.normalize_xlsx(p, "Compliance Division", "2026-02-09T17:00:00Z", "2026-10-06T15:40:00Z")


def write_pm25(W, target):
    """Hourly PM2.5 from the station's monitor: an hour is missing when the monitor was serviced, when the filter tape
    broke (March 3 to 4) and now and then when the hourly cycle did not complete."""
    rng = WD.rng_for("pm25")
    service = {(t.date(), t.hour) for t, text in R.other_work() if text.startswith("PM2.5")}
    tape = (dt.datetime(2026, 3, 3, 21), dt.datetime(2026, 3, 4, 10))
    rows = []
    for d in core.DAYS:
        for h in range(24):
            reg = W["plans"][d]["reg"][h]
            base = 5.5 + (3.5 if reg in ("drain", "calm", "transition") else 0.0) + (4.0 if d.month in (1, 2, 12) and 17 <= h <= 23 else 0)
            v = max(0.0, base * rng.lognormal(0, 0.35))
            t = dt.datetime(d.year, d.month, d.day, h)
            miss = rng.random() < 0.006 or (d, h) in service or tape[0] <= t < tape[1]
            rows.append([t.strftime("%Y-%m-%d %H:%M"), "" if miss else "%.1f" % v, "M" if miss else "V"])
    _w(os.path.join(target, FILES["pm25"]), ["datetime_pst", "pm25_ugm3", "qc"], rows)


def write_airport(target):
    """The airport's routine observations at 53 minutes past the hour, the specials it sends when the wind shifts,
    and the hours its feed missed."""
    rng = WD.rng_for("airport")
    rows = []
    for d in core.DAYS:
        for h in range(24):
            t = dt.datetime(d.year, d.month, d.day, h, 53)
            # the plain: synoptic north-northwest and southerly flow, no valley drainage
            if rng.random() < 0.55:
                drct = int(round((330 + rng.normal(0, 25)) % 360 / 10.0) * 10)
            else:
                drct = int(round((180 + rng.normal(0, 30)) % 360 / 10.0) * 10)
            sknt = max(0, int(rng.normal(7, 3.5)))
            if sknt < 3:
                drct, sknt = 0, 0
            tmpf = 50 + 25 * math.sin(math.pi * ((d - dt.date(2026, 1, 1)).days - 20) / 330.0) + 9 * math.sin(math.pi * (h - 8) / 14.0)
            if rng.random() < 0.004:
                continue
            rows.append(["KCAP", (t + dt.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M"), drct, sknt, "%.0f" % tmpf])
            if sknt >= 12 and rng.random() < 0.3:
                ts = t + dt.timedelta(minutes=int(rng.integers(9, 50)))
                d2 = int(round((drct + rng.normal(0, 30)) % 360 / 10.0) * 10)
                rows.append(["KCAP", (ts + dt.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M"), d2 if d2 else 360,
                             max(3, sknt + int(rng.integers(-3, 6))), "%.0f" % tmpf])
    rows.sort(key=lambda r: r[1])
    _w(os.path.join(target, FILES["airport"]), ["station", "valid_utc", "drct", "sknt", "tmpf"], rows)
