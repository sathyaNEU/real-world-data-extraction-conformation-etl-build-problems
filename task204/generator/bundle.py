#!/usr/bin/env python3
"""Read the shipped bundle the way a solver would, and build the session frames the estimates run on.

build.py uses this to compute every shipped figure from target/ rather than from the generator's own
state, so no figure can be right in the generator and wrong in the pack. verify.py reads the same
bundle on its own code path and must reach the same numbers.
"""
import csv
import datetime as dt
import os
import re
import zipfile
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Dublin")
UTC = dt.timezone.utc

SPINE = "bms_co2_5min_autumn2026.csv"
PLANT = "bms_plant_status_autumn2026.csv"
TIMETABLE = "timetable_autumn2026.csv"
MARKS = "attendance_marks_autumn2026.csv"
CAMPUS_OUT = "campus_outdoor_co2_hourly_2026.csv"
STATION_OUT = "macehead_gaw_co2_hourly_2026.csv"
REGISTER = "campus_room_register.csv"
ASBUILT = "asbuilt_room_data_sheets_kilmoneen.pdf"
STANDARD = "tgd_m4_ventilation_extract.pdf"
PROCEDURE = "iaq_monitoring_procedure_note.pdf"
BID = "capital_bid_tulrohan_block.xlsx"
CALENDAR = "etb_academic_calendar_2026_27.xlsx"


def rows(target, name):
    with open(os.path.join(target, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def ppm(text):
    """The spine's concentration column, exported with a thousands separator and its unit."""
    return float(re.sub(r"[^0-9.\-]", "", text))


def pdf_text(target, name):
    import pypdf
    r = pypdf.PdfReader(os.path.join(target, name))
    out = "\n".join(p.extract_text() or "" for p in r.pages)
    assert len(out) > 400, "%s: extracted %d characters" % (name, len(out))
    return out


def xlsx_rows(target, name, sheet):
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, name), data_only=True)
    ws = wb[sheet]
    data = [[c for c in row] for row in ws.iter_rows(values_only=True)]
    return data


# ----------------------------------------------------------------- the filed facts

def room_volumes(target):
    """Gross internal volumes, from the table inside the as-built room data sheets. The extractor
    returns one table cell per line, so the room code is found and the row read from the lines that
    follow it."""
    lines = [x.strip() for x in pdf_text(target, ASBUILT).split("\n")]
    out = {}
    for i, line in enumerate(lines):
        if re.fullmatch(r"[A-Z]{3}-[A-Z0-9]\d{2}", line) and i + 4 < len(lines):
            try:
                out[line] = float(lines[i + 4].replace(",", ""))
            except ValueError:
                continue
    assert len(out) >= 14, "as-built sheet: read %d volumes" % len(out)
    return out


def standard_figures(target):
    """The requirement and the per-person generation rate the standard's extract tables."""
    text = pdf_text(target, STANDARD)
    req = re.search(r"not less than\s+([\d.]+)\s+litres per second per person", text)
    lines = [x.strip() for x in text.split("\n")]
    gen = None
    for i, line in enumerate(lines):
        if line.startswith("Carbon dioxide generation") and i + 1 < len(lines):
            gen = float(lines[i + 1])
            break
    assert req and gen, "standard extract: requirement or generation rate not read"
    return {"required_ls_per_person": float(req.group(1)), "generation_l_per_s": gen}


def screening_ppm(target):
    text = pdf_text(target, PROCEDURE)
    m = re.search(r"([\d,]{4,5})\s*ppm", text)
    return float(m.group(1).replace(",", ""))


def block_rooms(target):
    """The six room codes the capital bid covers."""
    data = xlsx_rows(target, BID, "Scope")
    out = []
    for row in data:
        for cell in row:
            if isinstance(cell, str) and re.fullmatch(r"TUL-[A-Z]\d{2}", cell.strip()):
                out.append(cell.strip())
    return out


def teaching_days(target):
    data = xlsx_rows(target, CALENDAR, "Autumn term")
    out = []
    for row in data:
        if not row or not isinstance(row[0], (dt.date, dt.datetime, str)):
            continue
        d, status = row[0], row[2]
        if isinstance(d, (dt.date, dt.datetime)) and isinstance(status, str) and status == "Teaching day":
            out.append((d.date() if isinstance(d, dt.datetime) else d).isoformat())
    return out


# ----------------------------------------------------------------- the series

def outdoor_baseline(target):
    """One outdoor reading per local hour: the campus analyser, and the atmospheric station where the
    campus analyser was away."""
    base = {}
    for r in rows(target, CAMPUS_OUT):
        key = (r["timestamp_local"][:13], r["utc_offset"])
        base[key] = float(r["co2_ppm"])
    for r in rows(target, STATION_OUT):
        t = dt.datetime.strptime(r["datetime_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
        loc = t.astimezone(TZ)
        off = loc.utcoffset()
        key = (loc.strftime("%Y-%m-%d %H"),
               "+%02d:00" % (int(off.total_seconds()) // 3600))
        base.setdefault(key, float(r["co2_ppm"]))
    return base


def series(target):
    """{space: {(local_timestamp, offset): absolute ppm}}."""
    out = {}
    with open(os.path.join(target, SPINE), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out.setdefault(r["space_code"], {})[(r["timestamp_local"], r["utc_offset"])] = ppm(r["co2"])
    return out


def plant_state(target):
    """{(ahu, local_date): [(start_minute, end_minute, status)]}."""
    out = {}
    for r in rows(target, PLANT):
        a = r["ahu_ref"]
        d = r["interval_start_local"][:10]
        s = r["interval_start_local"][11:16]
        e = r["interval_end_local"][11:16]
        mins = lambda x: int(x[:2]) * 60 + int(x[3:5])
        end = 1440 if e == "24:00" else mins(e)
        out.setdefault((a, d), []).append((mins(s), end, r["status"]))
    return out


def sessions(target):
    """The timetable's sessions, keyed to room codes through the campus room register, with the
    occupants present counted from the attendance marks."""
    label_to_code = {}
    ahu_of = {}
    for r in rows(target, REGISTER):
        label_to_code[r["timetable_room_label"].strip()] = r["room_code"].strip()
        ahu_of[r["room_code"].strip()] = r["ahu_ref"].strip()
    present = {}
    with open(os.path.join(target, MARKS), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["mark"] == "present":
                present[r["session_ref"]] = present.get(r["session_ref"], 0) + 1
    out = []
    for r in rows(target, TIMETABLE):
        code = label_to_code[r["room_label"].strip()]
        out.append({"session_ref": r["session_ref"], "space": code, "ahu": ahu_of[code],
                    "date": r["date"], "period": r["period"],
                    "start": r["start_time"], "end": r["end_time"],
                    "group": r["group_code"], "subject": r["subject_code"],
                    "occupants": present.get(r["session_ref"], 0)})
    return out


def frames(target):
    """One session frame per timetabled session: the excess over the outdoor baseline at every
    five-minute stamp from the session's first reading to its last."""
    ser = series(target)
    base = outdoor_baseline(target)
    out = []
    for s in sessions(target):
        a = int(s["start"][:2]) * 60 + int(s["start"][3:5])
        b = int(s["end"][:2]) * 60 + int(s["end"][3:5])
        vals, missing = [], 0
        for k in range(a, b + 1, 5):
            hh, mm = divmod(k, 60)
            ts = "%s %02d:%02d:00" % (s["date"], hh, mm)
            got = None
            for off in ("+01:00", "+00:00"):
                if (ts, off) in ser.get(s["space"], {}):
                    got = (ser[s["space"]][(ts, off)], base[(ts[:13], off)])
                    break
            if got is None:
                missing += 1
                continue
            vals.append(got[0] - got[1])
        if missing or len(vals) < 3:
            continue
        out.append({"session_ref": s["session_ref"], "space": s["space"], "date": s["date"],
                    "period": s["period"], "group": s["group"], "occupants": s["occupants"],
                    "seconds": (b - a) * 60, "readings": vals})
    return out
