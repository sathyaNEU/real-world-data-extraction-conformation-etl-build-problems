"""task178 pack: writes every file under target/ from world.py and docs.py."""
from __future__ import annotations

import datetime as dt
import math
import os

import numpy as np
import openpyxl
from openpyxl.styles import Font

import common as C
import docs as D
import postprocess as PP
import world as W


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
    PP.normalize_ooxml(path, creator, last_by, created, modified, excel=True, company=C.COMPANY)
    return sum(len(r) - 1 for r in sheets.values())


def sig3(x):
    if x <= 0:
        return 0.0
    d = 3 - int(math.floor(math.log10(abs(x)))) - 1
    v = round(x, d)
    return int(v) if d <= 0 else v


def mdy(d):
    return "%d/%d/%d" % (d.month, d.day, d.year)


# --------------------------------------------------------------------------------------- the annual peak register
REMARKS = {1986: "Crest-stage gage; recorder tape torn 11/23 to 11/26", 1997: "Peak from crest-stage gage, float line jammed",
           2007: "Crest-stage gage; logger battery failed 12/3"}


def write_peaks(out):
    ph = W.peak_stages()
    pd = W.peak_dates()
    rows = []
    for i, wy in enumerate(C.REGISTER_WY):
        h = ph[i] - (C.DATUM_SHIFT if wy < 2010 else 0.0)
        t = pd[i]
        tm = "" if wy in REMARKS else "%02d:%02d" % (t.hour, t.minute)
        rows.append([wy, mdy(t.date()), tm, "%.2f" % h, REMARKS.get(wy, "")])
    pre = ["Callender Paper Company, Sauer Mill Water Resources",
           "TUM-02 Tumwick River near Sauer: annual peak stage register, water years 1980-2015",
           "Gage height in feet on the gage datum in use at the time of the peak",
           "Kept by S. Huber; exported from TUM02_peaks.xlsx 2016-03-02"]
    return C.write_csv(os.path.join(out, C.F_PEAKS), ["WY", "Date", "Time", "Gage height (ft)", "Remarks"], rows,
                       preamble=pre)


# ---------------------------------------------------------------------------------------- the 15-minute record
def stage_rows():
    """(index, stamp, value) rows of the export: every reading in PST, the telemetry's re-sent rows kept"""
    h = W.stage_logged()
    r = C.stream("resend")
    dup = set(int(x) for x in r.choice(W.N15, size=640, replace=False))
    gaps = set()
    for _ in range(22):
        a = int(r.integers(0, W.N15 - 40))
        gaps.update(range(a, a + int(r.integers(1, 9))))
    keep = W.protected_indices()
    rows = []
    for j in range(W.N15):
        if j in gaps and j not in keep:
            continue
        rows.append(j)
        if j in dup:
            rows.append(j)
    return rows


def write_stage(out):
    h = W.stage_logged()
    out_rows = []
    for j in stage_rows():
        out_rows.append([W.t_of(j).strftime("%Y-%m-%d %H:%M"), "%.2f" % h[j], "P", ""])
    pre = ["# Callender Paper Company, Sauer mill hydrologic database export",
           "# Location: TUM-02 Tumwick River near Sauer",
           "# Parameter: Stage (gage height), ft; gage datum 182.40 ft NAVD88",
           "# Time zone: UTC-08:00 (PST, no daylight saving time)",
           "# Period: 2015-10-01 00:00 to 2025-09-30 23:45",
           "# Grade P = provisional (record review outstanding)",
           "# Exported 2026-01-20 09:12 by gwagner"]
    return C.write_csv(os.path.join(out, C.F_STAGE), ["timestamp", "stage_ft", "grade", "qualifier"], out_rows,
                       preamble=pre)


# ----------------------------------------------------------------------------------------- the measurements
def geometry(q, h):
    v = 1.75 * (q / 1000.0) ** 0.36
    area = q / v
    width = 118.0 + 4.0 * max(h - 6.0, 0.0) + (520.0 * max(h - W.HBF, 0.0) ** 0.55 if h > W.HBF else 0.0)
    return width, area, v


def numbered_measurements():
    M = W.measurements()
    out = []
    r = C.stream("measfields")
    for k, m in enumerate(M):
        mm = dict(m)
        mm["no"] = 101 + k
        dur = int(r.integers(5, 12)) * 5 if m["method"] == "wading" else (int(r.integers(4, 9)) * 5 if m["method"] == "ADCP" else int(r.integers(8, 16)) * 5)
        mm["start"] = m["time"]
        mm["end"] = m["time"] + dt.timedelta(minutes=dur)
        e = abs(np.log(m["q"] / m["q_true"]))
        if m["method"] == "wading":
            mm["rated"] = "E" if e < 0.02 and r.random() < 0.5 else ("G" if e < 0.06 else "F")
        elif m["kind"] == "flood":
            mm["rated"] = "F" if e < 0.08 or r.random() < 0.5 else "P"
        else:
            mm["rated"] = "G" if e < 0.05 else "F"
        mm["control"] = ["Clear", "Clear", "Clear", "Debris light", "Algae light"][int(r.integers(0, 5))] if m["kind"] == "routine" else "Drift"
        out.append(mm)
    return out


def write_meas_old(out):
    M = [m for m in numbered_measurements() if m["time"].date() < C.ADCP_FROM]
    sheets = {}
    s80 = [("No.", "Date", "Made by", "Width (ft)", "Area (sq ft)", "Velocity (ft/s)", "Gage ht (ft)", "Discharge (cfs)",
            "Rated", "Remarks")]
    s90 = [("No.", "Date", "Start", "End", "Made by", "Method", "Gage ht (ft)", "Width (ft)", "Area (sq ft)",
            "Velocity (ft/s)", "Discharge (cfs)", "Rated", "Remarks")]
    s00 = [("Meas no", "Date", "Start", "End", "Party", "Method", "GH start", "GH end", "Mean GH", "Width", "Area",
            "Mean vel", "Q (cfs)", "Rating", "Control", "Remarks")]
    r = C.stream("oldnotes")
    words = {"E": "Excellent", "G": "Good", "F": "Fair", "P": "Poor"}
    for m in M:
        gh = m["gh"] - C.DATUM_SHIFT
        q = sig3(m["q"])
        w, a, v = geometry(q, m["gh"])
        party = "RK" if m["time"].year < 1995 else ("RK/SH" if m["time"].year < 1999 else "SH")
        meth = {"wading": "Wading", "bridge": "Cableway" if m["kind"] == "routine" else "Cableway and boat"}.get(m["method"], "Cableway")
        rem = "Rising" if m["kind"] == "flood" and r.random() < 0.3 else ("Falling" if m["kind"] == "flood" else "")
        if m["time"].year < 1990:
            s80.append((m["no"], mdy(m["time"].date()), party, round(w), sig3(a), round(v, 2), round(gh, 2), q, m["rated"], rem))
        elif m["time"].year < 2000:
            s90.append((m["no"], mdy(m["time"].date()), m["start"].strftime("%H%M"), m["end"].strftime("%H%M"), party, meth,
                        round(gh, 2), round(w), sig3(a), round(v, 2), q, words[m["rated"]], rem))
        else:
            d = float(r.normal(0, 0.006))
            s00.append((m["no"], m["time"].strftime("%Y-%m-%d"), m["start"].strftime("%H:%M"), m["end"].strftime("%H:%M"),
                        party, meth, round(gh - d, 2), round(gh + d, 2), round(gh, 2), round(w), sig3(a), round(v, 2), q,
                        m["rated"], m["control"], rem))
    sheets["1980-1989"] = s80
    sheets["1990-1999"] = s90
    sheets["2000-2004"] = s00
    return wb_write(os.path.join(out, C.F_MEAS_OLD), sheets, ("Stacy Huber", "Stacy Huber", "2005-02-14T18:21:40Z",
                    "2016-03-02T16:05:12Z"))


def write_meas_new(out):
    M = [m for m in numbered_measurements() if m["time"].date() >= C.ADCP_FROM]
    rows = []
    r = C.stream("newmeas")
    for m in M:
        gh = m["gh"] - (C.DATUM_SHIFT if m["time"].date() < C.DATUM_CHANGE else 0.0)
        w, a, v = geometry(m["q"], m["gh"])
        si = m["method"] == "ADCP" and m["time"].date() <= C.CMS_TO
        if si:
            q, unit = sig3(m["q"] / C.CFS_PER_CMS), "m3/s"
            a_, w_, v_ = sig3(a * 0.092903), round(w * 0.3048, 1), round(v * 0.3048, 2)
        else:
            q, unit = sig3(m["q"]), "ft3/s"
            a_, w_, v_ = sig3(a), round(w), round(v, 2)
        party = "SH" if m["time"].year < 2016 else ("SH/GW" if m["time"].year < 2021 else ("GW/DM" if m["kind"] == "flood" else "GW"))
        inst = "FlowTracker" if m["method"] == "wading" else ("RiverRay ADCP" if m["time"].year >= 2013 else "StreamPro ADCP")
        rem = ""
        if m["kind"] == "flood" and m["gh"] > W.HBF:
            rem = "Cableway and boat" if r.random() < 0.6 else "Cableway; boat on left side"
        elif m["kind"] == "flood":
            rem = "From cableway"
        ntr = "" if m["method"] == "wading" else int(r.integers(2, 7))
        rows.append([m["no"], C.GAUGE_ID, m["time"].strftime("%Y-%m-%d"), m["start"].strftime("%H:%M"), m["end"].strftime("%H:%M"),
                     party, inst, "%.2f" % gh, q, unit, a_, w_, v_, ntr,
                     {"E": "Good", "G": "Good", "F": "Fair", "P": "Poor"}[m["rated"]], m["control"], rem])
    head = ["meas_no", "station_id", "meas_date", "start_time", "end_time", "party", "instrument", "mean_gh_ft",
            "discharge", "discharge_unit", "area", "width", "mean_velocity", "transects", "quality",
            "control_condition", "remarks"]
    return C.write_csv(os.path.join(out, C.F_MEAS_NEW), head, rows)


# ------------------------------------------------------------------------------------------------- the visits
def visit_rows():
    """every visit 2016 to 2025: the routine visits and the flood-measurement visits"""
    hl = W.stage_logged()
    st = W.stage_true()
    meas = [m for m in numbered_measurements() if m["time"] >= dt.datetime(2015, 10, 1)]
    rows = []
    for arrive, depart, purge, party in W.visits():
        i = W.i_of(C.local_to_pst(arrive))
        mn = [m["no"] for m in meas if m["kind"] == "routine" and arrive <= m["time"] <= depart]
        work = ["download"]
        if purge:
            work.append("orifice line purged %s" % purge.strftime("%H:%M"))
        work.append("staff check")
        if mn:
            work.append("Q meas")
        notes = ""
        if abs(arrive - C.LOGGER_SWAP) < dt.timedelta(hours=3):
            notes = "Controller replaced (new unit); offset entered from staff"
        if abs(arrive - C.LOGGER_FIX) < dt.timedelta(hours=3):
            notes = "Logger 0.47 above staff; offset reset to staff"
        staff = round(float(st[i]), 2)
        if abs(arrive - C.LOGGER_FIX) < dt.timedelta(hours=3):
            staff = round(float(hl[i]) - C.LOGGER_OFFSET_ERR, 2)
        rows.append(dict(arrive=arrive, depart=depart, party=party, staff=staff, logger=float(hl[i]),
                         meas=mn[0] if mn else "", work="; ".join(work), notes=notes))
    floods = {}
    for m in meas:
        if m["kind"] == "flood":
            floods.setdefault(m["time"].date(), []).append(m)
    for d, ms in floods.items():
        a = min(m["start"] for m in ms) - dt.timedelta(minutes=25)
        b = max(m["end"] for m in ms) + dt.timedelta(minutes=30)
        i = W.i_of(C.local_to_pst(a))
        rows.append(dict(arrive=a, depart=b, party="GW/DM" if d.year >= 2021 else "SH/GW", staff=round(float(st[i]), 2),
                         logger=float(hl[i]), meas=", ".join(str(m["no"]) for m in ms), work="Q meas (ADCP); staff check",
                         notes="High water"))
    rows.sort(key=lambda v: v["arrive"])
    return rows


def write_visits(out):
    rows = []
    for v in visit_rows():
        rows.append([v["arrive"].strftime("%Y-%m-%d"), v["arrive"].strftime("%H:%M"), v["depart"].strftime("%H:%M"), v["party"],
                     "%.2f" % v["staff"], "%.2f" % v["logger"], v["meas"], v["work"], v["notes"]])
    head = ["visit_date", "arrive", "depart", "party", "staff_gage_ft", "logger_ft", "meas_no", "work_done", "notes"]
    return C.write_csv(os.path.join(out, C.F_VISITS), head, rows)


# ------------------------------------------------------------------------------------------------- SCADA
def scada_stamp(j):
    """the historian's stamp for the PST reading j: UTC before the June 2022 upgrade, local wall clock after"""
    t = W.t_of(j)
    if t < C.local_to_pst(C.SCADA_UPGRADE):
        return C.pst_to_utc(t)
    return C.pst_to_local(t)


def scada_rows():
    i0, pipe, dist, level = W.radar()
    q, _ = W.series()
    st = W.stage_true()
    r = C.stream("scada")
    legacy_end = W.i_of(C.local_to_pst(dt.datetime(2022, 6, 20, 20, 0)))
    new_start = W.i_of(C.local_to_pst(C.SCADA_UPGRADE))
    keep = W.protected_indices()
    gaps = set()
    for _ in range(30):
        a = int(r.integers(i0, W.N15 - 20))
        gaps.update(range(a, a + int(r.integers(1, 7))))
    spikes = {}
    flood = np.flatnonzero(st[i0:] > 9.0) + i0
    for j in r.choice(flood, size=min(36, len(flood)), replace=False):
        if j not in keep:
            spikes[int(j)] = round(float(r.uniform(0.8, 3.2)), 2)
    rows = []
    hour = np.arange(W.N15) % 96 / 4.0
    flow = 19.5 + 3.2 * np.sin(2 * np.pi * (hour - 8) / 24.0) + r.normal(0, 0.25, W.N15)
    press = 91.0 - 0.08 * (flow - 19.5) + r.normal(0, 0.3, W.N15)
    for j in range(i0, W.N15):
        if legacy_end < j < new_start or (j in gaps and j not in keep):
            continue
        d = dist[j] - spikes.get(j, 0.0)
        rows.append((j, scada_stamp(j), round(d, 2), round(C.RADAR_FACE_INSTALL - d, 2), round(float(flow[j]), 2),
                     round(float(press[j]), 1)))
    return rows


def write_scada(out):
    rows = [[s.strftime("%Y-%m-%d %H:%M:%S"), "%.2f" % d, "%.2f" % l, "%.2f" % f, "%.1f" % p] for _, s, d, l, f, p in scada_rows()]
    pre = ["Historian export: SAUER crossing tags", "Interval 15 min, interpolated", "Exported 2026-01-12 14:03 by bdodson"]
    return C.write_csv(os.path.join(out, C.F_SCADA), ["Timestamp", "SAUER_RAD1_DIST.PV", "SAUER_RAD1_LVL.PV",
                       "SAUER_36IN_FLOW.PV", "SAUER_36IN_PRESS.PV"], rows, preamble=pre)


# -------------------------------------------------------------------------------------------------- CMMS
def work_orders():
    r = C.stream("wo")
    out = []
    n = 24800
    fixed = [(dt.datetime(2019, 3, 12, 8, 30), dt.datetime(2019, 3, 12, 15, 10), "PR", "SAUER-RAD1",
              "Install level radar on pipe bridge downstream truss, conduit to RTU"),
             (dt.datetime(2019, 3, 14, 9, 0), dt.datetime(2019, 3, 14, 11, 40), "PR", "SAUER-RTU",
              "Configure RAD1 tags in SCADA, alarm at 191.5"),
             (dt.datetime(2022, 6, 21, 6, 0), dt.datetime(2022, 6, 21, 17, 30), "PR", "SCADA-HIST",
              "Historian server replacement, mill control room"),
             (dt.datetime(2022, 11, 7, 7, 15), dt.datetime(2022, 11, 7, 12, 0), "CM", "SAUER-PB",
              "Remove drift from upstream truss face after 11/5 high water"),
             (dt.datetime(2022, 11, 16, 9, 30), dt.datetime(2022, 11, 16, 14, 45), "CM", "SAUER-RAD1",
              "Replace damaged mounting bracket on level radar RAD1 (drift strike 11/5)"),
             (dt.datetime(2025, 1, 8, 6, 40), dt.datetime(2025, 1, 10, 18, 0), "CM", "SAUER-PB",
              "Isolate 36in main at Sauer valves, drift strike on truss and pipe"),
             (dt.datetime(2025, 1, 13, 7, 0), dt.datetime(2025, 1, 21, 16, 30), "CM", "SAUER-PB",
              "Temporary pipe supports at panel points 4 to 6, return main to service"),
             (dt.datetime(2025, 3, 4, 8, 0), dt.datetime(2025, 3, 4, 15, 0), "CM", "SAUER-RAD1",
              "Clean radar face, check echo profile")]
    routine = [("PM", "SAUER-VLV1", "Exercise isolation valve V-1"), ("PM", "SAUER-VLV2", "Exercise isolation valve V-2"),
               ("PM", "SAUER-CP", "Cathodic protection test station readings"), ("PM", "SAUER-PB", "Pipe bridge visual inspection"),
               ("PM", "SAUER-RTU", "RTU battery and enclosure check"), ("PM", "SAUER-FM", "Flow meter verification"),
               ("CM", "SAUER-PB", "Remove drift from truss"), ("CM", "SAUER-RTU", "Comms failure, reset modem")]
    t = dt.datetime(2019, 1, 7, 8, 0)
    while t < dt.datetime(2025, 9, 30):
        typ, asset, desc = routine[int(r.integers(0, len(routine)))]
        start = t.replace(hour=int(r.integers(7, 13)), minute=int(r.integers(0, 4)) * 15)
        end = start + dt.timedelta(minutes=int(r.integers(4, 26)) * 15)
        out.append((start, end, typ, asset, desc))
        t += dt.timedelta(days=int(r.integers(9, 26)))
    out += fixed
    out.sort(key=lambda w: w[0])
    rows = []
    for k, (a, b, typ, asset, desc) in enumerate(out):
        rows.append(["WO-%06d" % (n + 7 * k + int(r.integers(0, 6))), asset, a.strftime("%m/%d/%Y %H:%M"),
                     b.strftime("%m/%d/%Y %H:%M"), typ, desc, "Closed"])
    return rows


def write_wo(out):
    return C.write_csv(os.path.join(out, C.F_WO), ["wo_no", "asset", "opened", "completed", "type", "description", "status"],
                       work_orders())


# ---------------------------------------------------------------------------------------------- distractors
def write_rain(out):
    r = C.stream("rain")
    rows = []
    d = dt.date(1979, 10, 1)
    q, ev = W.series()
    storm_days = {}
    for wy, t0, tp, size, kind in ev:
        day = W.t_of(t0 + tp // 2).date()
        storm_days[day] = storm_days.get(day, 0.0) + size
    while d <= dt.date(2025, 9, 30):
        doy = d.timetuple().tm_yday
        wet = 0.55 + 0.35 * math.cos(2 * math.pi * (doy - 15) / 365.25)
        p = 0.0
        if r.random() < wet * 0.75:
            p = float(r.gamma(0.8, 0.28 + 0.25 * wet))
        if d in storm_days:
            p += min(4.5, 0.0009 * storm_days[d] + float(r.uniform(0.2, 0.8)))
        rows.append([d.isoformat(), "%.2f" % p, "M" if r.random() < 0.002 else ""])
        d += dt.timedelta(days=1)
    return C.write_csv(os.path.join(out, C.F_RAIN), ["date", "precip_in", "flag"], rows,
                       preamble=["Sauer mill wastewater plant rain gage (tipping bucket, heated), daily totals 08:00 to 08:00"])


def write_marten(out):
    r = C.stream("marten")
    rows = []
    pd = W.peak_dates()
    for wy in range(1988, 2026):
        z = float(r.normal(0, 1))
        q = 10 ** (2.95 + 0.24 * z)
        h = 1.2 + 0.62 * (q / 100.0) ** 0.55
        t = pd[wy - C.WY_FIRST] + dt.timedelta(hours=float(r.uniform(-30, 20))) if r.random() < 0.7 else \
            dt.datetime(wy - 1, 12, 1) + dt.timedelta(days=float(r.uniform(0, 90)))
        rows.append([wy, t.strftime("%Y-%m-%d"), "%.2f" % h, int(round(q, -1)), "A"])
    return C.write_csv(os.path.join(out, C.F_KESSEL), ["water_year", "peak_date", "gage_height_ft", "peak_discharge_cfs", "code"],
                       rows, preamble=["MRT-01 Marten Creek at Hollis Road (Callender Paper Company, Sauer mill), annual peaks",
                                       "Drainage area 41.2 sq mi. Discharge from rating 6 (stable rock control)."])


# ------------------------------------------------------------------------------------------------- the build
def build_pack(out):
    os.makedirs(out, exist_ok=True)
    n = {}
    n[C.F_PEAKS] = write_peaks(out)
    n[C.F_STAGE] = write_stage(out)
    n[C.F_MEAS_OLD] = write_meas_old(out)
    n[C.F_MEAS_NEW] = write_meas_new(out)
    D.write_station(out)
    D.write_standard(out)
    D.write_study(out)
    D.write_levels(out)
    n[C.F_VISITS] = write_visits(out)
    n[C.F_SCADA] = write_scada(out)
    n[C.F_WO] = write_wo(out)
    n[C.F_RAIN] = write_rain(out)
    n[C.F_KESSEL] = write_marten(out)
    n[C.F_DICT] = D.write_dict(out, wb_write)
    return n
