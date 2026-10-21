"""task178 pack: writes every file under target/ from records.py and docs.py."""
from __future__ import annotations

import datetime as dt
import os

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font

import common as C
import docs as D
import postprocess as PP
import records as R
import world as W

DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")


def wb_write(path, sheets, stamp, widths=None, bold_header=True):
    wb = openpyxl.Workbook()
    first = True
    for name, rows in sheets.items():
        ws = wb.active if first else wb.create_sheet()
        ws.title = name
        first = False
        for r in rows:
            ws.append(list(r))
        if bold_header and rows:
            for c in ws[1]:
                c.font = Font(bold=True)
        for k, w in (widths or {}).get(name, {}).items():
            ws.column_dimensions[k].width = w
    wb.save(path)
    creator, last_by, created, modified = stamp
    PP.normalize_ooxml(path, creator, last_by, created, modified, excel=True, company=C.CITY)
    return sum(len(r) - 1 for r in sheets.values())


def fmt_utc(h):
    d = C.from_hours(h + 1e-7)
    return d.strftime("%Y-%m-%d %H:%M")


def write_verified(out):
    t, v, q = R.verified()
    path = os.path.join(out, C.F_VER)
    pre = ["# City of Port Tessaly, DPW Waterfront and Harbor Engineering",
           "# Tide gauge PTG-01 (Cutler Wharf), verified water level, 15-minute",
           "# Export 2026-12-08 from the city data system. Units: feet. Datum: station datum STND (1995)."]
    rows = []
    for x, y, f in zip(t, v, q):
        rows.append((fmt_utc(x), "" if np.isnan(y) else "%.3f" % y, f))
    return C.write_csv(path, ("timestamp_utc", "water_level_ft", "quality"), rows, preamble=pre)


def write_telemetry(out):
    t, v = R.telemetry()
    rows = [(C.from_hours(x + 1e-7).strftime("%Y-%m-%dT%H:%M:00Z"), "%.3f" % y, "P") for x, y in zip(t, v)]
    return C.write_csv(os.path.join(out, C.F_TEL), ("time_utc", "wl_m", "qc"), rows, crlf=False)


def write_board(out):
    t, v = R.tide_board()
    rows = []
    for x, y in zip(t, v):
        loc, _ = C.to_local(C.from_hours(x + 1e-7).replace(second=0, microsecond=0))
        rows.append(("%d/%d/%d %02d:%02d" % (loc.month, loc.day, loc.year, loc.hour, loc.minute), "%.2f" % y))
    return C.write_csv(os.path.join(out, C.F_BOARD), ("reading_time", "board_ft"), rows)


def write_tables(out):
    rows = R.tide_table_rows()
    wb = openpyxl.Workbook()
    ws0 = wb.active
    n = 0
    for y in range(1995, 2028):
        ws = ws0 if y == 1995 else wb.create_sheet()
        ws.title = str(y)
        yr = [r for r in rows if r[0].year == y]
        if y <= 2006:
            ws.append(["PORT TESSALY, MAINE"])
            ws.append(["TIDE TABLE %d   HIGH AND LOW WATERS" % y])
            ws.append(["Times are Eastern Standard Time. Add one hour for daylight saving time. Heights in feet above mean lower low water."])
            ws.append([])
            ws.append(["Date", "Day", "Time", "Ht ft", "H/L"])
            for loc, h, kind, zone in sorted(((r[0] - dt.timedelta(hours=1) if r[3] == "EDT" else r[0]), r[1], r[2], r[3]) for r in yr):
                ws.append([loc.date(), DAYS[loc.weekday()], "%02d%02d" % (loc.hour, loc.minute), h, kind])
                ws.cell(row=ws.max_row, column=1).number_format = "mm/dd/yyyy"
                n += 1
        elif y <= 2018:
            ws.append(["Port Tessaly, ME  Tide Predictions %d" % y])
            ws.append(["Times local (EST/EDT). Heights ft above MLLW. 1983-2001 epoch."])
            ws.append(["Date", "High/Low", "Time", "Height (ft)"])
            for loc, h, kind, zone in yr:
                ws.append([loc.date(), "High" if kind == "H" else "Low", loc.strftime("%I:%M %p").lstrip("0"), h])
                ws.cell(row=ws.max_row, column=1).number_format = "yyyy-mm-dd"
                n += 1
        else:
            ws.append(["Port Tessaly (PTG-01) predicted high and low waters, %d" % y])
            ws.append(["Issued by the Harbormaster's Office %s. Heights: feet above MLLW (1983-2001 epoch). Time zone: LST/LDT."
                       % ("2026-10-01" if y == 2027 else "%d-10-01" % (y - 1))])
            ws.append(["Date", "Day", "Time", "Pred (ft)", "Type"])
            for loc, h, kind, zone in yr:
                ws.append([loc.date(), DAYS[loc.weekday()], loc.strftime("%H:%M"), h, kind])
                ws.cell(row=ws.max_row, column=1).number_format = "yyyy-mm-dd"
                n += 1
        ws.column_dimensions["A"].width = 12
    path = os.path.join(out, C.F_TABLES)
    wb.save(path)
    PP.normalize_ooxml(path, "Regina Lang", "Regina Lang", "2007-01-08T14:55:02Z", "2026-10-01T13:17:40Z", excel=True,
                       company=C.CITY)
    return n


def _fmt_close(dtv, system):
    if dtv is None:
        return ""
    if system == "WOMS":
        return "%d/%d/%d %d:%02d" % (dtv.month, dtv.day, dtv.year, dtv.hour, dtv.minute)
    return dtv.strftime("%Y-%m-%d %H:%M")


def write_closures(out):
    rows, _ = R.closures()
    rr = [(r["wo"], r["system"], r["source"], _fmt_close(r["opened"], r["system"]), _fmt_close(r["closed"], r["system"]),
           r["location"], r["reason"], r["note"]) for r in rows]
    return C.write_csv(os.path.join(out, C.F_CLOSE), ("wo_number", "system", "source", "opened", "closed", "location",
                                                       "reason", "notes"), rr)


def write_weather(out):
    rng = C.stream("weather")
    th, s = W.surge_hourly()
    rows = []
    d = dt.date(2015, 1, 1)
    while d <= dt.date(2026, 11, 30):
        doy = d.timetuple().tm_yday
        clim = 55 - 25 * np.cos(2 * np.pi * (doy - 20) / 365.25)
        tmax = clim + 9 + rng.normal(0, 6); tmin = clim - 9 + rng.normal(0, 5)
        a = C.hours(dt.datetime(d.year, d.month, d.day, 5)); m = (th >= a) & (th < a + 24)
        sd = float(s[m].mean()) if m.any() else 0.0
        slp = 1015 - 40 * sd + rng.normal(0, 5)
        gust = max(8, 18 + 45 * max(sd, 0) + rng.normal(0, 7))
        pr = 0.0 if rng.uniform() < 0.62 else round(float(rng.exponential(0.35 + 0.8 * max(sd, 0))), 2)
        rows.append((d.isoformat(), "%.0f" % tmax, "%.0f" % tmin, "%.2f" % pr, "%.1f" % slp, "%.0f" % gust,
                     "%d" % (int(rng.integers(0, 36)) * 10)))
        d += dt.timedelta(days=1)
    return C.write_csv(os.path.join(out, C.F_WX), ("date", "tmax_f", "tmin_f", "precip_in", "slp_mb_mean", "gust_mph",
                                                    "gust_dir_deg"), rows)


def write_river(out):
    rng = C.stream("river")
    rows = []
    d = dt.date(2015, 1, 1)
    q = 900.0
    while d <= dt.date(2026, 11, 30):
        doy = d.timetuple().tm_yday
        base = 650 + 2400 * np.exp(-0.5 * ((doy - 105) / 18) ** 2) + 300 * np.exp(-0.5 * ((doy - 320) / 25) ** 2)
        q = 0.8 * q + 0.2 * base * float(np.exp(rng.normal(0, 0.35)))
        code = "P" if d >= dt.date(2025, 10, 1) else ("e" if rng.uniform() < 0.01 else "A")
        rows.append((d.isoformat(), "%.0f" % q, code))
        d += dt.timedelta(days=1)
    return C.write_csv(os.path.join(out, C.F_RIVER), ("date", "discharge_cfs", "code"), rows)


def write_manifest(out, counts):
    desc = {
        C.F_VER: ("PTG-01 verified water level, 15-minute", "1995-01-01 to 2026-06-30 UTC", "city data system (verified product)"),
        C.F_TEL: ("PTG-01 telemetry, 6-minute, provisional", "2026-05-01 to 2026-11-30 UTC", "city data system (telemetry feed)"),
        C.F_BOARD: ("harbormaster's tide board log, hourly", "2015-01-01 to 2026-11-30", "harbormaster's office logger"),
        C.F_TABLES: ("published tide tables, one sheet a year", "1995 to 2027", "harbormaster's office"),
        C.F_LOG: ("PTG-01 station log", "1994-11 to 2026-11", "Waterfront and Harbor Engineering"),
        C.F_DATUMS: ("PTG-01 datum sheet, revision 2026-06", "", "Waterfront and Harbor Engineering"),
        C.F_SLR: ("sea level and coastal flooding guidance, 2026 update", "", "Waterfront and Harbor Engineering"),
        C.F_BASIS: ("Granite Wharf trestle design basis, revision B", "", "Waterfront and Harbor Engineering"),
        C.F_CLOSE: ("DPW street closure work orders, reason FLOOD", "2016-01-01 to 2026-11-30", "WOMS to June 2023, PWWorks from July 2023"),
        C.F_WX: ("municipal airport daily weather", "2015-01-01 to 2026-11-30", "airport weather station"),
        C.F_RIVER: ("Pennock River at Tessaly Falls, daily mean flow", "2015-01-01 to 2026-11-30", "river gauge"),
        C.F_DICT: ("column meanings for the exports", "", "Waterfront and Harbor Engineering"),
    }
    rows = [(f, desc[f][0], desc[f][1], desc[f][2], counts.get(f, ""), "2026-12-08") for f in C.ALL_FILES if f != C.F_MANIFEST]
    return C.write_csv(os.path.join(out, C.F_MANIFEST), ("file", "contents", "coverage", "source", "rows", "pulled"), rows)


def tables_annual():
    t, v, q = R.verified()
    yr, _, _ = R.ymd_arrays(t)
    a = {int(y): float(np.nanmean(v[(yr == y) & (q != "M")]) - C.STND_BELOW_MLLW) for y in range(1995, 2026)}
    ys = np.array(sorted(a)); vals = np.array([a[y] for y in ys])
    b, c = np.polyfit(ys + 0.5, vals, 1)
    design = round(float(c + b * 2027.5), 2)
    return {int(y): round(float(a[y]), 2) for y in ys}, design, float(b)


def build_pack(out):
    os.makedirs(out, exist_ok=True)
    n = {}
    n[C.F_VER] = write_verified(out)
    n[C.F_TEL] = write_telemetry(out)
    n[C.F_BOARD] = write_board(out)
    n[C.F_TABLES] = write_tables(out)
    n[C.F_CLOSE] = write_closures(out)
    n[C.F_WX] = write_weather(out)
    n[C.F_RIVER] = write_river(out)
    n[C.F_LOG] = D.write_log(out, lambda p, s, st: wb_write(p, s, st, widths={"Log": {"A": 12, "B": 5, "C": 110}}))
    n[C.F_DICT] = D.write_dict(out, lambda p, s, st: wb_write(p, s, st))
    dat = {k: round((v - W.datums()['MLLW']) / C.FT, 2) for k, v in W.datums().items()}
    D.write_datums(out, dat)
    annual, design, slope = tables_annual()
    D.write_slr(out, annual, design, slope)
    D.write_basis(out)
    n[C.F_MANIFEST] = write_manifest(out, n)
    return n
