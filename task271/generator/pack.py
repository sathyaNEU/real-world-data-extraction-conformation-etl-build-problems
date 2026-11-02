"""task271 pack writer: every data file under target/, each in the form the system that keeps it writes it.

The creel survey's own exports (the flight counts the observer keys in after each loop, the clerks' tablet interviews),
the society's lake register, Vellacott Air's flight log and the hatchery's trip sheets, drop tallies and raceway samples,
the temperature loggers' compiled download, and the recreation sites' campground permits. Nothing here describes the
data: every file names its own columns the way its system does."""
from __future__ import annotations

import datetime as dt
import json
import math
import os

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

import common as K
import postprocess as PP
import world as W

F_REGISTER = "lake_register_2026.xlsx"
F_COUNTS = "survey_flight_counts_2026.csv"
F_INTERVIEWS = "creel_interviews_2026.csv"
F_FLIGHTLOG = "vellacott_air_flight_log_2026.xlsx"
F_TRIPS = "quillet_creek_trip_sheets_2026.xlsx"
F_DROPS = "quillet_creek_drop_tallies_2026.json"
F_SAMPLES = "quillet_creek_raceway_samples_2026.csv"
F_RACEWAYS = "quillet_creek_raceway_numbers.csv"
F_LOGGERS = "lake_temperature_loggers_2026.csv"
F_DEPLOY = "logger_deployments_2026.csv"
F_CAMP = "campground_permits_2026.xlsx"

# Vellacott's own lake names, as the observer keys them
VA_NAME = {"PP-03": "Tessaly L", "PP-07": "Kesterway", "PP-11": "Brackwater L", "PP-14": "Galloran",
           "PP-18": "Nockell L", "PP-22": "Ostrum", "PP-24": "Farrowdale L", "PP-27": "Pillory",
           "PP-31": "Saddlebank", "PP-33": "Copperjack L", "PP-05": "Ellerdine", "PP-09": "Quorrin L",
           "PP-16": "Ravensky", "PP-20": "Inverkeld L", "PP-26": "Kittiwake", "PP-29": "Mosswater",
           "PP-35": "Driftpine", "PP-37": "Merganser L", "PP-02": "Corriemore", "PP-12": "Pinewhistle L",
           "PP-19": "Kelloran", "PP-28": "Bufflehead L", "PP-30": "Canvasback", "PP-34": "Thornhollow"}
# the clerks' tablet pick list
TABLET_NAME = {L[0]: L[1].replace(" Lake", "") for L in W.LAKES}
INFO = {L[0]: L for L in W.LAKES}


def _xlsx_header(ws, cols, widths):
    ws.append(cols)
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
        c = ws.cell(row=1, column=i)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE4EC")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"


# ------------------------------------------------------------------------------------------------- register
def write_register(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Lakes"
    cols = ["PPFS code", "Lake", "Vellacott no.", "Regulation", "Surface area (ha)", "Max depth (m)", "Elevation (m)",
            "Access", "Campground", "Launch", "Catchables stocked 2026"]
    _xlsx_header(ws, cols, [10, 20, 11, 34, 13, 11, 11, 10, 11, 14, 13])
    g = K.rng_for("register")
    rows = sorted(W.LAKES, key=lambda L: L[0])
    for L in rows:
        code, name, cls, area, target, pos, elev, access, camp, launch, share = L
        depth = round(float(g.uniform(6.5, 24.0)), 1)
        ws.append([code, name, pos, W.REG_TEXT[cls], area, depth, elev, access, camp, launch,
                   "yes" if access != "walk-in" else "no"])
    for r in range(2, ws.max_row + 1):
        ws.cell(row=r, column=5).number_format = "0.0"
        ws.cell(row=r, column=6).number_format = "0.0"
    ws2 = wb.create_sheet("Revisions")
    ws2.append(["Date", "Change", "By"])
    ws2.append(["2025-11-04", "Surface areas updated from the 2025 bathymetry flights", K.PEOPLE["creel"]])
    ws2.append(["2026-03-20", "Regulation column brought in line with the 2026-2027 synopsis", K.PEOPLE["stocking"]])
    ws2.append(["2026-04-14", "Vellacott numbers re-issued for the 2026 route", K.PEOPLE["creel"]])
    for i, w in enumerate([12, 58, 18], start=1):
        ws2.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
    wb.save(path)
    PP.normalize_ooxml(path, K.PEOPLE["creel"], K.PEOPLE["stocking"], "2025-11-04T18:12:00Z", "2026-04-14T16:41:00Z",
                       excel=True, company=K.SOCIETY)
    return len(rows)


# ------------------------------------------------------------------------------------------------- counts
def count_rows(X):
    rows = []
    pos = {L[0]: L[5] for L in W.LAKES}
    obs_g = K.rng_for("observer")
    for f in X["flights"]:
        d = f["date"]
        obs = K.OBSERVERS[0] if obs_g.random() < 0.7 else K.OBSERVERS[1]
        recs = [c for c in X["counts"] if c["date"] == d and c["loop"] == f["loop"]]
        recs.sort(key=lambda c: pos[c["lake"]])
        for c in recs:
            if f["aborted"]:
                rows.append([d.isoformat(), f["loop"], pos[c["lake"]], VA_NAME[c["lake"]], "", "", "", obs,
                             "fog - loop not flown"])
                continue
            t = K.hm(c["t"])
            if c["boats"] is None:
                # smoke hid the lake: the aircraft turned back short of it, so no time over it was noted
                rows.append([d.isoformat(), f["loop"], pos[c["lake"]], VA_NAME[c["lake"]], "", "", "", obs,
                             "smoke - not counted"])
            else:
                rows.append([d.isoformat(), f["loop"], pos[c["lake"]], VA_NAME[c["lake"]], t, c["boats"], c["shore"],
                             obs, ""])
    return rows


COUNT_COLS = ["survey_date", "loop", "lake_no", "lake", "time_over", "boats", "shore_anglers", "observer", "remarks"]


# ------------------------------------------------------------------------------------------------- interviews
def _heap(x, g):
    u = g.random()
    if u < 0.55:
        q = 0.25
    elif u < 0.82:
        q = 0.5
    else:
        q = 1 / 12.0
    return round(x / q) * q


FSA = ["V2C", "V2B", "V2H", "V1S", "V1T", "V1Y", "V2E", "V0K", "V0E", "V5K", "V3R", "T2N", "T3A", "V2N", "V1H"]


def interview_rows(X):
    iv = sorted(X["interviews"], key=lambda r: (r["date"], r["lake"], r["end"]))
    seq = {}
    rows = []
    for r in iv:
        g = K.rng_for("ivrow", r["lake"], r["date"].isoformat(), "%.6f" % r["start"], "%.6f" % r["end"])
        clerk = r["clerk"]
        k = (clerk, r["date"])
        seq[k] = seq.get(k, 0) + 1
        no = "%s%02d%02d-%02d" % (clerk, r["date"].month, r["date"].day, seq[k])
        start = _heap(r["start"], g)
        start = min(max(start, K.DAY_OPEN), r["end"] - 1 / 12.0)
        finish = r["end"]
        hours = ""
        st = K.hm(start)
        if g.random() < 0.09:
            st = ""
            hours = "%.1f" % max(0.5, round((finish - r["start"]) * 2) / 2)
        lic_u = g.random()
        lic = "BC resident" if lic_u < 0.83 else ("non-resident" if lic_u < 0.91 else "youth (under 16)")
        rows.append([no, r["date"].isoformat(), clerk, TABLET_NAME[r["lake"]], "main access", r["size"],
                     "shore" if r["shore"] else "boat", st, K.hm(finish), hours, r["kept"], r["caught"] - r["kept"],
                     r["clipped"], FSA[int(g.integers(0, len(FSA)))], lic])
    return rows


INTERVIEW_COLS = ["interview_no", "date", "clerk", "lake", "access", "party_size", "fished_from", "started",
                  "finished", "hours_fished", "rb_kept", "rb_released", "kept_ad_clipped", "home_fsa", "licence"]


# ------------------------------------------------------------------------------------------------- flight log
def write_flight_log(path, X):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Flight log"
    cols = ["Flight", "Date (UTC)", "Aircraft", "Leg", "Block off (UTC)", "Take-off (UTC)", "Landing (UTC)",
            "Block on (UTC)", "Pilot", "Route", "Remarks"]
    _xlsx_header(ws, cols, [9, 11, 10, 5, 13, 13, 13, 13, 12, 11, 34])
    g = K.rng_for("flightlog")
    pilots = {"C-FVAB": ["M. Arsenault", "K. Duguay"], "C-GVAK": ["K. Duguay"]}
    for f in X["charter"]:
        d = f["date"]
        for leg, (b0, b1) in enumerate(f["blocks"], start=1):
            def utc(h):
                t = dt.datetime.combine(d, dt.time(0, 0)) + dt.timedelta(hours=h + 7)
                return t
            off = utc(b0)
            on = utc(b1)
            to = off + dt.timedelta(minutes=int(g.integers(5, 9)))
            ld = on - dt.timedelta(minutes=int(g.integers(4, 8)))
            rem = ""
            if f["aborted"]:
                rem = "Fog over plateau, RTB"
            elif len(f["blocks"]) > 1 and leg == 1:
                rem = "Smoke over east lakes, shut down at Pillory L. dock to wait"
            elif len(f["blocks"]) > 1 and leg == 2:
                rem = "Smoke not lifting, back to base"
            ws.append([f["flight"], off.date().isoformat(), f["reg"], leg, off.strftime("%H:%M"), to.strftime("%H:%M"),
                       ld.strftime("%H:%M"), on.strftime("%H:%M"), pilots[f["reg"]][int(g.integers(0, len(pilots[f["reg"]])))],
                       "PPFS-" + f["loop"], rem])
    wb.save(path)
    PP.normalize_ooxml(path, "Vellacott Air Ops", "Vellacott Air Ops", "2026-05-14T15:02:00Z", "2026-09-02T17:26:00Z",
                       excel=True, company=K.OPERATOR)
    return ws.max_row - 1


# ------------------------------------------------------------------------------------------------- hatchery
def write_trip_sheets(path, X):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Trips 2026"
    cols = ["Trip", "Date", "Truck", "Raceway", "Net load (kg)", "Destination", "Release site", "Driver",
            "Tank temp (C)"]
    _xlsx_header(ws, cols, [9, 11, 7, 9, 12, 18, 14, 12, 12])
    g = K.rng_for("trips_sheet")
    drivers = {"T1": ["P. Wong", "R. Fields"], "T2": ["S. Haldane", "P. Wong"]}
    n = 0
    for t in X["hatchery"]:
        new_template = t["date"] >= K.TRIPSHEET_SWITCH
        lab = t["rw_new"] if new_template else W.old_number(t["rw_new"])
        drv = drivers[t["truck"]][int(g.integers(0, 2))]
        for dr in t["drops"]:
            site = "main ramp" if INFO[dr["lake"]][9] in ("concrete ramp", "gravel ramp") else "shore access"
            ws.append([t["trip"], t["date"].isoformat(), t["truck"], lab, t["load"], INFO[dr["lake"]][1], site, drv,
                       t["tank_temp"] if new_template else None])
            n += 1
    for r in range(2, ws.max_row + 1):
        ws.cell(row=r, column=5).number_format = "0.0"
    wb.save(path)
    PP.normalize_ooxml(path, K.PEOPLE["hatchery"], K.PEOPLE["hatchery"], "2026-04-30T22:10:00Z", "2026-09-01T20:48:00Z",
                       excel=True, company=K.SOCIETY)
    return n


def write_drop_tallies(path, X):
    g = K.rng_for("drops")
    out = []
    for t in X["hatchery"]:
        for dr in t["drops"]:
            hh = 9.5 + g.uniform(0, 5.5)
            out.append({"tripId": t["trip"], "lakeCode": dr["lake"], "nets": dr["nets"], "doaFish": dr["doa"],
                        "releasedAt": "%sT%s:00-07:00" % (t["date"].isoformat(), K.hm(hh)),
                        "waterTempC": round(float(g.normal(14 if t["date"].month < 7 else 18.5, 1.6)), 1),
                        "crew": "QC drop crew"})
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"export": "drop-tally", "app_version": "3.4.1", "exported": "2026-09-02T08:15:00-07:00",
                   "records": out}, f, indent=1)
    return len(out)


def sample_rows(X):
    rows = []
    for s in X["samples"]:
        lab = W.old_number(s["rw_new"]) if s["date"] < K.RACEWAY_RENUMBER else s["rw_new"]
        rows.append([s["date"].isoformat(), lab, int(s["grams"]), s["count"], s["onhand"]])
    return rows


SAMPLE_COLS = ["sample_date", "raceway", "sample_g", "fish_counted", "fish_on_hand"]
RACEWAY_COLS = ["old_raceway", "new_raceway", "from_date"]


def raceway_rows():
    return [[k, W.old_number(k), K.RACEWAY_RENUMBER.isoformat()] for k in range(1, 9)]


# ------------------------------------------------------------------------------------------------- loggers
def logger_rows(X):
    """the compiled download: every reading each logger stored, stamped by the logger's own clock, with the station it
    was downloaded from"""
    station = {}
    for serial, code, depth, a, b in W.DEPLOYMENTS:
        if b is not None:
            station[serial] = (TABLET_NAME[code], depth)
    rows = []
    for serial in sorted(X["temps"]):
        clock = W.SERIALS[serial][0]
        site, depth = station[serial]
        for t, v, where in X["temps"][serial]:
            tt = t + dt.timedelta(hours=7) if clock == "utc" else t
            rows.append([serial, site, "%.1f" % depth, tt.strftime("%Y-%m-%d %H:%M"), "%.2f" % v])
    return rows


LOGGER_COLS = ["Logger SN", "Site", "Depth (m)", "Date Time", "Temp (C)"]
DEPLOY_COLS = ["logger_serial", "lake_code", "depth_m", "deployed", "retrieved"]


def deploy_rows():
    return [[s, c, "%.1f" % d, a.strftime("%Y-%m-%d %H:%M"), b.strftime("%Y-%m-%d %H:%M") if b else ""]
            for s, c, d, a, b in W.DEPLOYMENTS]


# ------------------------------------------------------------------------------------------------- campgrounds
def write_campgrounds(path, X):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Nightly occupancy"
    cols = ["Recreation site", "Night of", "Sites occupied", "Sites"]
    _xlsx_header(ws, cols, [26, 11, 13, 7])
    g = K.rng_for("camp")
    n = 0
    camps = [L for L in W.LAKES if L[8] == "yes"]
    for L in camps:
        sites = int(g.integers(8, 31))
        for d in K.SEASON_DAYS:
            base = 0.35 + (0.4 if K.day_type(d) == "weekend" else 0.0) + (0.15 if d.month in (7, 8) else 0.0)
            occ = int(min(sites, max(0, round(sites * min(1.0, base + g.normal(0, 0.12))))))
            ws.append([L[1] + " Recreation Site", d.isoformat(), occ, sites])
            n += 1
    wb.save(path)
    PP.normalize_ooxml(path, "Recreation Sites and Trails", "Recreation Sites and Trails", "2026-09-08T19:00:00Z",
                       "2026-09-08T19:04:00Z", excel=True, company="Recreation Sites and Trails")
    return n


def write_all(out, X):
    p = lambda f: os.path.join(out, f)
    n = {}
    n[F_REGISTER] = write_register(p(F_REGISTER))
    n[F_COUNTS] = K.write_csv(p(F_COUNTS), COUNT_COLS, count_rows(X))
    n[F_INTERVIEWS] = K.write_csv(p(F_INTERVIEWS), INTERVIEW_COLS, interview_rows(X))
    n[F_FLIGHTLOG] = write_flight_log(p(F_FLIGHTLOG), X)
    n[F_TRIPS] = write_trip_sheets(p(F_TRIPS), X)
    n[F_DROPS] = write_drop_tallies(p(F_DROPS), X)
    n[F_SAMPLES] = K.write_csv(p(F_SAMPLES), SAMPLE_COLS, sample_rows(X))
    n[F_RACEWAYS] = K.write_csv(p(F_RACEWAYS), RACEWAY_COLS, raceway_rows())
    n[F_LOGGERS] = K.write_csv(p(F_LOGGERS), LOGGER_COLS, logger_rows(X))
    n[F_DEPLOY] = K.write_csv(p(F_DEPLOY), DEPLOY_COLS, deploy_rows())
    n[F_CAMP] = write_campgrounds(p(F_CAMP), X)
    return n
