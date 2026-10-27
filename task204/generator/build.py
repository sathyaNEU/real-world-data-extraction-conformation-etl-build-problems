#!/usr/bin/env python3
"""task204, the single entry point: cut the pack, compute every shipped figure from the pack, write
the goldens, figures.json, metadata.json and the write-up's figure block.

    python3 task204/generator/build.py

Nothing else writes figures.json (reduce-house-fixes H33), so a rebuild is this one command and the
tree is clean afterwards.
"""
import csv
import datetime as dt
import json
import math
import os
import random
import shutil
import statistics
from decimal import ROUND_HALF_UP, Decimal

import analysis as A
import bundle as B
import docs as D
import params as P
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
MTIME = dt.datetime(2026, 12, 15, 16, 42, 0, tzinfo=dt.timezone.utc).timestamp()

MONTHS = [("2026-09", "September 2026"), ("2026-10", "October 2026"),
          ("2026-11", "November 2026"), ("2026-12", "December 2026")]


def half_up(value, places):
    q = Decimal(1).scaleb(-places)
    return float(Decimal(repr(float(value))).quantize(q, rounding=ROUND_HALF_UP))


def to_bin(value, step=0.5):
    return float(Decimal(repr(float(value) / step)).quantize(Decimal(1), rounding=ROUND_HALF_UP)) * step


def fmt(value, places):
    return ("%%.%df" % places) % half_up(value, places)


def write_csv(name, header, body):
    path = os.path.join(TARGET, name)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(body)
    return path


# ===================================================================== the pack

def cut_pack():
    if os.path.isdir(TARGET):
        shutil.rmtree(TARGET)
    os.makedirs(TARGET)

    stamp_list, outdoor, excess, occ, state, day_factor = W.truth_world()
    sess = W.sessions()
    kinds = {iso: k for iso, _, k in W.calendar_days()}
    ahu_of = {s[0]: s[3] for s in P.SPACES}
    name_of = {s[0]: s[1] for s in P.SPACES}
    block_of = {s[0]: s[2] for s in P.SPACES}

    # ---------------------------------------------------------------- the spine
    r_noise = W.rng("sensor-noise")
    r_drop = W.rng("dropout")
    swap = P.SENSOR_SWAP
    gone = {(swap["removed"], ), (swap["fitted"], )}
    removed_days = []
    d0 = dt.date.fromisoformat(swap["removed"])
    while d0 < dt.date.fromisoformat(swap["fitted"]):
        removed_days.append(d0.isoformat())
        d0 += dt.timedelta(days=1)

    spine = []
    received = {}
    for code, *_ in P.SPACES:
        point = "KMN." + P.ROOM_LABELS[code][0]
        drop_days = set(P.DROPOUT_DAYS[code])
        rate = P.DROPOUT_RATE[code]
        for i, (_, ld, lt, off) in enumerate(stamp_list):
            if code == swap["space"] and ld in removed_days:
                continue
            if ld in drop_days or r_drop.random() < rate:
                continue
            value = outdoor[i] + excess[code][i] + r_noise.gauss(0.0, P.SENSOR_NOISE_PPM)
            if code == swap["space"] and ld < swap["removed"]:
                value += swap["offset_before_ppm"]
            v = int(round(value))
            quality = "uncertain" if (code == swap["space"] and ld == swap["fitted"]) else "good"
            spine.append([point, code, "%s %s" % (ld, lt), off, "{:,} ppm".format(v), quality])
            received[(code, ld)] = received.get((code, ld), 0) + 1
    write_csv(B.SPINE,
              ["point_ref", "space_code", "timestamp_local", "utc_offset", "co2", "quality"], spine)

    # ---------------------------------------------------------------- plant status
    plant = []
    for ahu, d, t0, d1, t1, st in W.plant_intervals():
        off = None
        for (_, ld, lt, o) in stamp_list:
            if ld == d and lt[:5] == t0[:5]:
                off = o
                break
        cfg = P.AHU[ahu]
        speed = {"OCCUPIED": cfg["fan_occupied_pct"], "SETBACK": cfg["fan_setback_pct"],
                 "OFF": 0}[st]
        plant.append([ahu, "%s %s" % (d, t0[:5]), "%s %s" % (d1, t1[:5]), off or "+00:00",
                      st, speed])
    write_csv(B.PLANT, ["ahu_ref", "interval_start_local", "interval_end_local", "utc_offset",
                        "status", "supply_fan_speed_pct"], plant)

    # ---------------------------------------------------------------- timetable
    module_of = {}
    r_mod = W.rng("module")
    for g in P.GROUPS:
        module_of[g[0]] = "%s%d%02d" % (g[3], 4 + r_mod.randrange(0, 3), r_mod.randrange(10, 99))
    tt = []
    for s in sess:
        tt.append([s["session_id"], P.ROOM_LABELS[s["space"]][1], s["date"], s["period"],
                   s["start"], s["end"], s["group"], module_of[s["group"]], s["subject"],
                   W.staff_ref(s["tutor"])])
    write_csv(B.TIMETABLE, ["session_ref", "room_label", "date", "period", "start_time",
                            "end_time", "group_code", "module_code", "subject_code",
                            "tutor_staff_ref"], tt)

    # ---------------------------------------------------------------- attendance marks
    marks = W.attendance_rows(sess)
    write_csv(B.MARKS, ["session_ref", "date", "room_label", "period", "group_code", "person_ref",
                        "role", "mark", "amended"],
              [[m["session_id"], m["date"], P.ROOM_LABELS[m["space"]][1], m["period"], m["group"],
                m["person_ref"], m["role"], m["mark"], m["amended"]] for m in marks])

    # ---------------------------------------------------------------- outdoor analysers
    hour_of = {}
    for i, (t, ld, lt, off) in enumerate(stamp_list):
        if lt.endswith("00:00") and lt[3:5] == "00":
            hour_of[(ld, lt[:2], off)] = i
    campus, station = [], []
    gap0, gap1 = P.OUTDOOR_GAP
    r_st = W.rng("station")
    pre = dt.date.fromisoformat(P.TERM_START) - dt.timedelta(days=27)
    for key in sorted(hour_of, key=lambda k: hour_of[k]):
        ld, hh, off = key
        i = hour_of[key]
        v = outdoor[i]
        if not (gap0 <= ld <= gap1):
            campus.append(["%s %s:00:00" % (ld, hh), off, "%.1f" % v, "valid"])
        t = stamp_list[i][0]
        station.append([t.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "%.2f" % (v + P.NATIONAL_OFFSET_PPM + r_st.gauss(0.0, 1.1)), "A"])
    # the campus analyser also ran before the monitored window
    head = []
    r_pre = W.rng("outdoor-pre")
    d = pre
    while d < dt.date.fromisoformat(P.TERM_START):
        for hh in range(24):
            v = P.OUTDOOR_BASE_PPM - 0.6 + r_pre.gauss(0.0, 5.0) + \
                4.1 * math.cos(2 * math.pi * (hh - 5.0) / 24.0)
            head.append(["%s %02d:00:00" % (d.isoformat(), hh), "+01:00", "%.1f" % v, "valid"])
        d += dt.timedelta(days=1)
    write_csv(B.CAMPUS_OUT, ["timestamp_local", "utc_offset", "co2_ppm", "instrument_status"],
              head + campus)
    write_csv(B.STATION_OUT, ["datetime_utc", "co2_ppm", "flag"], station)

    # ---------------------------------------------------------------- room register
    r_reg = W.rng("register")
    reg = []
    for code, name, block, ahu, vol, q, a_off, a_sb, area, height in P.SPACES:
        reg.append([code, "KMN." + P.ROOM_LABELS[code][0], P.ROOM_LABELS[code][1],
                    "RDS-%s-%s" % (block[:3].upper(), code.split("-")[1]), block,
                    "Ground" if code.split("-")[1][0] in "G0" else "First", name,
                    "Practical teaching" if block == "Tulrohan" and code[4] == "G" else
                    ("General teaching" if block != "Annagloor" else "Specialist teaching"),
                    "%.1f" % area, ahu])
    other = [("Store", "Store"), ("Office", "Staff office"), ("Circulation", "Corridor"),
             ("Plant", "Plant room"), ("Welfare", "Changing room"), ("Library", "Learning centre")]
    for block, prefix, ahu in (("Tulrohan", "TUL", "AHU-03"), ("Drumlusk", "DRM", "AHU-01"),
                               ("Annagloor", "ANG", "AHU-02")):
        used = set()
        for k in range(9):
            while True:
                num = "%s%02d" % (r_reg.choice("GF0"), r_reg.randrange(1, 40))
                if num not in used:
                    used.add(num)
                    break
            use, nm = other[r_reg.randrange(len(other))]
            reg.append(["%s-%s" % (prefix, num), "", "", "RDS-%s-%s" % (prefix, num), block,
                        "Ground" if num[0] in "G0" else "First", "%s %s" % (nm, num), use,
                        "%.1f" % (8 + r_reg.randrange(1, 420) / 3.0), ahu])
    reg.sort(key=lambda r: (r[4], r[0]))
    write_csv(B.REGISTER, ["room_code", "bms_point_ref", "timetable_room_label",
                           "asbuilt_sheet_ref", "block", "floor", "room_name", "use_category",
                           "net_floor_area_m2", "ahu_ref"], reg)

    # ---------------------------------------------------------------- maintenance log
    r_wo = W.rng("workorder")
    r_tech = W.rng("tech")
    techs = [P.CONTROLS_TECHNICIAN, "Grainne Kilkenny", "Corrie MacCarville"]
    log = []
    for code, *_ in P.SPACES:
        wo = "WO%05d" % (12000 + r_wo.randrange(1, 900))
        raised = "2026-09-%02d" % (7 + r_wo.randrange(0, 14))
        done = "2026-09-%02d" % (int(raised[-2:]) + 1 + r_wo.randrange(0, 6))
        span = 1000
        read = span + (r_wo.randrange(-9, 10))
        log.append([wo, raised, done, code, "CO2-%s" % code.replace("-", ""),
                    "Annual span check", span, read, r_tech.choice(techs), ""])
    swapsp = swap["space"]
    log.append(["WO%05d" % (13000 + r_wo.randrange(1, 400)), "2026-11-04", swap["removed"],
                swapsp, "CO2-%s" % swapsp.replace("-", ""), "Span check, out of tolerance",
                1000, swap["span_before"], techs[0],
                "Analyser %s reads high against span gas; removal authorised" % swap["old_serial"]])
    log.append(["WO%05d" % (13000 + r_wo.randrange(401, 900)), swap["removed"], swap["fitted"],
                swapsp, "CO2-%s" % swapsp.replace("-", ""), "Analyser replacement",
                1000, swap["span_after"], techs[0],
                "Analyser %s fitted and span checked" % swap["new_serial"]])
    for k in range(6):
        code = P.SPACES[r_wo.randrange(len(P.SPACES))][0]
        raised = "2026-1%d-%02d" % (r_wo.randrange(0, 3), 1 + r_wo.randrange(0, 27))
        log.append(["WO%05d" % (13000 + r_wo.randrange(1, 900)), raised, raised, code,
                    "CO2-%s" % code.replace("-", ""), "Network fault, point offline", "", "",
                    r_tech.choice(techs), "Field bus repair"])
    log.sort(key=lambda r: (r[1], r[0]))
    write_csv("maintenance_log_iaq_sensors_2026.csv",
              ["work_order_ref", "raised_date", "completed_date", "room_code", "asset_ref",
               "activity", "span_gas_ppm", "reading_ppm", "technician", "notes"], log)

    # ---------------------------------------------------------------- distractors
    r_e = W.rng("energy")
    energy = []
    for mprn, base in (("10304471982", 46.0), ("10304471983", 18.5)):
        for i, (t, ld, lt, off) in enumerate(stamp_list):
            if lt[3:5] not in ("00", "30"):
                continue
            hh = int(lt[:2])
            k = kinds[ld]
            load = base * (0.28 if k != "teaching" else
                           (1.0 if 8 <= hh < 16 else (0.46 if 6 <= hh < 20 else 0.24)))
            energy.append([mprn, "%s %s" % (ld, lt[:5]), off, "%.3f" % (load * (1 + r_e.gauss(0, 0.06))),
                           "%.3f" % (load * 0.21 * (1 + r_e.gauss(0, 0.1)))])
    write_csv("campus_energy_halfhourly_2026.csv",
              ["mprn", "timestamp_local", "utc_offset", "kwh_import", "kvarh"], energy)

    r_t = W.rng("temp")
    temps = []
    for code, *_ in P.SPACES:
        for key in sorted(hour_of, key=lambda k: hour_of[k]):
            ld, hh, off = key
            i = hour_of[key]
            st = state[ahu_of[code]][i]
            base_t = 18.4 if st == "OFF" else (20.1 if st == "SETBACK" else 21.3)
            temps.append([code, "%s %s:00:00" % (ld, hh), off,
                          "%.1f" % (base_t + 0.0009 * excess[code][i] + r_t.gauss(0, 0.45)),
                          "%.1f" % (41 + 0.006 * excess[code][i] + r_t.gauss(0, 2.8))])
    write_csv("bms_temperature_rh_hourly_autumn2026.csv",
              ["space_code", "timestamp_local", "utc_offset", "air_temp_c",
               "relative_humidity_pct"], temps)

    write_workbooks()
    write_pdfs()
    write_thread()
    for root, _, files in os.walk(TARGET):
        for f in files:
            os.utime(os.path.join(root, f), (MTIME, MTIME))


# ===================================================================== workbooks

def write_workbooks():
    import openpyxl
    from openpyxl.styles import Alignment, Font
    from openpyxl.utils import get_column_letter

    def finish(ws, widths, freeze="A2"):
        for i, w in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w
        for c in ws[1]:
            c.font = Font(bold=True)
            c.alignment = Alignment(vertical="top", wrap_text=True)
        ws.freeze_panes = freeze

    # ---- the air handling unit time clocks
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Time clock"
    ws.append(["ahu_ref", "serves", "day_type", "occupied_from", "occupied_to", "setback_from",
               "setback_to", "fan_occupied_pct", "fan_setback_pct", "control_mode",
               "setting_changed", "changed_by"])
    for ahu in sorted(P.AHU):
        c = P.AHU[ahu]
        changed = "2021-08-19" if "timetable" in c["control"] else "2014-09-02"
        ws.append([ahu, c["serves"], "Term weekday", c["occupied"][0], c["occupied"][1],
                   c["setback"][0], c["setback"][1], c["fan_occupied_pct"], c["fan_setback_pct"],
                   c["control"], changed, P.FACILITIES_MANAGER])
        ws.append([ahu, c["serves"], "Weekend and closure", "", "", "", "", 0,
                   0, c["control"], changed, P.FACILITIES_MANAGER])
    finish(ws, [9, 28, 21, 14, 13, 13, 12, 11, 11, 25, 14, 18])
    ws2 = wb.create_sheet("Zone assignment")
    ws2.append(["ahu_ref", "room_code", "supply_terminal_ref", "terminal_count",
                "commissioned_date"])
    r = W.rng("terminal")
    for code, name, block, ahu, *_ in P.SPACES:
        ws2.append([ahu, code, "VT-%s-%02d" % (code.split("-")[1], 1 + r.randrange(0, 9)),
                    2 + r.randrange(0, 5), "2021-07-28" if block == "Tulrohan" else "2014-08-14"])
    finish(ws2, [9, 11, 20, 15, 18])
    path = os.path.join(TARGET, "ahu_timeclock_schedule.xlsx")
    wb.save(path)
    D.finalise_xlsx(path, "AHU time clock settings, Kilmoneen campus", P.FACILITIES_MANAGER,
                    P.FACILITIES_MANAGER, P.ETB_NAME, "2026-09-04", "2026-12-15")

    # ---- enrolment groups and staff
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Groups"
    ws.append(["group_code", "programme", "award_level", "enrolled", "coordinator_staff_ref",
               "campus"])
    r = W.rng("coordinator")
    tutors = W.group_tutors()
    for g in P.GROUPS:
        ws.append([g[0], g[1], int(g[0][3]) if g[0][3].isdigit() else 5, g[2],
                   W.staff_ref(tutors[g[0]]), P.CAMPUS_NAME])
    finish(ws, [12, 34, 12, 10, 20, 34])
    ws2 = wb.create_sheet("Staff")
    ws2.append(["staff_ref", "name", "role", "school"])
    schools = ["Engineering and Construction", "Business and Services",
               "Health and Social Care", "Science and Computing"]
    r2 = W.rng("staff-school")
    for n in P.TUTORS:
        ws2.append([W.staff_ref(n), n, "Tutor", schools[r2.randrange(len(schools))]])
    for n in P.ASSISTANTS:
        ws2.append([W.staff_ref(n), n, "Learning support assistant",
                    schools[r2.randrange(len(schools))]])
    finish(ws2, [11, 22, 27, 30])
    path = os.path.join(TARGET, "enrolment_groups_autumn2026.xlsx")
    wb.save(path)
    D.finalise_xlsx(path, "Enrolment groups, autumn term 2026", "Learner records office",
                    "Learner records office", P.ETB_NAME, "2026-09-25", "2026-12-15")

    # ---- the academic calendar
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Autumn term"
    ws.append(["date", "day", "status", "note"])
    label = {"teaching": "Teaching day", "weekend": "Weekend", "midterm": "Midterm break",
             "closure": "Campus closure"}
    names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for iso, wd, kind in W.calendar_days():
        ws.append([dt.date.fromisoformat(iso), names[wd], label[kind],
                   P.CLOSURE_DAYS.get(iso, "")])
    for c in ws["A"][1:]:
        c.number_format = "yyyy-mm-dd"
    finish(ws, [12, 12, 17, 46])
    ws2 = wb.create_sheet("Term dates")
    ws2.append(["term", "first_day", "last_day", "teaching_days", "midterm_break_from",
                "midterm_break_to"])
    ws2.append(["Autumn 2026", dt.date.fromisoformat(P.TERM_START),
                dt.date.fromisoformat(P.TERM_END), len(W.teaching_days()),
                dt.date.fromisoformat(P.MIDTERM_BREAK[0]),
                dt.date.fromisoformat(P.MIDTERM_BREAK[1])])
    ws2.append(["Spring 2027", dt.date(2027, 1, 11), dt.date(2027, 4, 2), 56,
                dt.date(2027, 2, 15), dt.date(2027, 2, 19)])
    for col in ("B", "C", "E", "F"):
        for c in ws2[col][1:]:
            c.number_format = "yyyy-mm-dd"
    finish(ws2, [14, 12, 12, 15, 20, 20])
    path = os.path.join(TARGET, "etb_academic_calendar_2026_27.xlsx")
    wb.save(path)
    D.finalise_xlsx(path, "Academic calendar 2026/27", "Registrar's office", "Registrar's office",
                    P.ETB_NAME, "2026-06-11", "2026-12-02")

    # ---- the capital bid sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Scope"
    ws.append(["Tulrohan Block, minor works bid 2027, scope of the two options"])
    ws.append([])
    ws.append(["room_code", "room_name", "net_floor_area_m2", "gross_internal_volume_m3",
               "air_handling_unit", "in_scope"])
    vols = {s[0]: s[4] for s in P.SPACES}
    areas = {s[0]: s[8] for s in P.SPACES}
    for code in P.BLOCK_SPACES:
        ws.append([code, dict((s[0], s[1]) for s in P.SPACES)[code], areas[code], vols[code],
                   dict((s[0], s[3]) for s in P.SPACES)[code], "Yes"])
    ws.append(["Total", "", "=SUM(C4:C9)", "=SUM(D4:D9)", "", ""])
    finish(ws, [12, 30, 18, 24, 18, 10], freeze="A4")
    ws2 = wb.create_sheet("Options")
    ws2.append(["option_ref", "description", "capital_cost_eur", "design_life_years",
                "lead_time_weeks", "programme_note"])
    ws2.append(["A", "Replace AHU-03 and AHU-04 and the Tulrohan supply and extract distribution",
                1_284_000, 25, 34, "Summer 2027 shutdown required"])
    ws2.append(["B", "Timetable change moving the four largest groups to the Drumlusk and "
                     "Annagloor rooms", 96_500, 1, 6,
                "Needs 11 additional room-hours a week across two blocks"])
    for c in ws2["C"][1:]:
        c.number_format = '#,##0'
    finish(ws2, [11, 62, 18, 17, 16, 46])
    path = os.path.join(TARGET, "capital_bid_tulrohan_block.xlsx")
    wb.save(path)
    D.finalise_xlsx(path, "Minor works bid 2027, Tulrohan Block", P.ESTATES_OFFICER,
                    P.ESTATES_OFFICER, P.ETB_NAME, "2026-11-26", "2026-12-14")


# ===================================================================== PDFs

def write_pdfs():
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, Spacer
    s = D.styles()
    vols = {x[0]: x[4] for x in P.SPACES}
    areas = {x[0]: x[8] for x in P.SPACES}
    heights = {x[0]: x[9] for x in P.SPACES}
    names = {x[0]: x[1] for x in P.SPACES}

    # ---------------- as-built room data sheets (the only record of the volumes)
    fl = [Paragraph("Room data sheets, as built", s["title"]),
          Paragraph("%s &nbsp;|&nbsp; %s<br/>Project 19-0442, Kilmoneen campus mechanical "
                    "upgrade &nbsp;|&nbsp; Issue D, record drawing set, 9 September 2021"
                    % (P.DESIGN_PRACTICE, P.CAMPUS_NAME), s["ref"]),
          Spacer(1, 7 * mm),
          Paragraph("Volumes below are gross internal, taken off the record drawings after the "
                    "2021 works and used for the air volume calculations in appendix C. Heights "
                    "are clear internal to the underside of structure; where a space has a "
                    "stepped soffit the volume is the sum of the measured parts and the height "
                    "shown is the area-weighted mean.", s["p"])]
    for block, prefix in (("Tulrohan Block", "TUL"), ("Drumlusk Block", "DRM"),
                          ("Annagloor Block", "ANG")):
        codes = [c for c in vols if c.startswith(prefix)]
        rowsd = [["Room", "Room name", "Floor area m2", "Clear height m",
                  "Gross internal volume m3", "Supply terminals"]]
        r = W.rng("rds-" + prefix)
        for c in codes:
            rowsd.append([c, names[c], "{:,.1f}".format(areas[c]), "%.1f" % heights[c],
                          "{:,}".format(vols[c]), str(2 + r.randrange(0, 5))])
        fl += [Paragraph(block, s["h"]),
               D.table(rowsd, [22 * mm, 46 * mm, 22 * mm, 22 * mm, 32 * mm, 22 * mm],
                       align=[2, 3, 4, 5]),
               Paragraph("Source: record drawing set 19-0442/M series, issue D.", s["src"])]
    fl.append(Paragraph(
        "The Tulrohan spaces were retained in the 2021 works and their volumes are unchanged from "
        "the 1978 record set; the Drumlusk and Annagloor volumes follow the 2014 reconfiguration. "
        "Air volumes in appendix C are calculated on these figures.", s["p"]))
    D.write_pdf(os.path.join(TARGET, B.ASBUILT),
                {"title": "Room data sheets as built, Kilmoneen campus",
                 "author": P.DESIGN_PRACTICE, "subject": "Project 19-0442 record information",
                 "creator": "%s, document control" % P.DESIGN_PRACTICE,
                 "producer": "%s publishing system" % P.DESIGN_PRACTICE},
                "19-0442 Room data sheets, issue D", fl, "2021-09-09")

    # ---------------- the standard extract
    g = P.GENERATION_L_PER_S
    fl = [Paragraph("%s: Ventilation and indoor air quality in education buildings" % P.STANDARD_REF,
                    s["title"]),
          Paragraph("%s<br/>%s &nbsp;|&nbsp; Extract: section 4, ventilation of teaching spaces, "
                    "and table 2.3" % (P.STANDARD_ISSUER, P.STANDARD_EDITION), s["ref"]),
          Spacer(1, 7 * mm),
          Paragraph("4.2 &nbsp; Teaching spaces", s["h"]),
          Paragraph("A teaching space shall be provided with outdoor air at not less than "
                    "%g litres per second per person at the occupancy at which the space is used. "
                    "The requirement applies to each teaching space separately."
                    % P.REQUIRED_LS_PER_PERSON, s["p"]),
          Paragraph("4.3 &nbsp; Demonstrating compliance", s["h"]),
          Paragraph("Compliance is demonstrated by the outdoor-air supply rate achieved in use. "
                    "For an existing building the rate is established from measurement in the "
                    "space itself over the periods for which the space is timetabled. Design "
                    "intent recorded at handover, and air volumes proved at a unit rather than at "
                    "the space, do not of themselves demonstrate compliance.", s["p"]),
          Paragraph("4.4 &nbsp; Reporting", s["h"]),
          Paragraph("Rates are reported per person present. Where a space serves groups of "
                    "different size the rate is reported over the whole of the period assessed "
                    "rather than for a single group.", s["p"]),
          Paragraph("Table 2.3 &nbsp; Design data, occupant emissions", s["h"]),
          D.table([["Quantity", "Value", "Unit"],
                   ["Carbon dioxide generation, one occupant of a teaching or practical space",
                    "%.4f" % g, "litres per second"],
                   ["Sensible heat gain, one occupant of a teaching or practical space", "75",
                    "watts"],
                   ["Moisture gain, one occupant of a teaching or practical space", "0.050",
                    "grammes per second"]],
                  [86 * mm, 24 * mm, 38 * mm], align=[1]),
          Paragraph("Source: table 2.3, unchanged from the 2019 edition.", s["src"]),
          Paragraph("Requirement 4.2 replaces the air change rate given in the 2009 guidance. "
                    "Where a space was built to the earlier guidance the requirement applies on "
                    "the next substantial alteration or on the next assessment of the space, "
                    "whichever is earlier.", s["p"])]
    D.write_pdf(os.path.join(TARGET, B.STANDARD),
                {"title": "%s extract, sections 4.2 to 4.4 and table 2.3" % P.STANDARD_REF,
                 "author": P.STANDARD_ISSUER,
                 "subject": "Technical guidance for education buildings",
                 "creator": "%s" % P.STANDARD_ISSUER,
                 "producer": "Department of Education publications service"},
                "%s, %s" % (P.STANDARD_REF, P.STANDARD_EDITION), fl, "2024-03-18")

    # ---------------- the campus monitoring procedure note
    codes = [x[0] for x in P.SPACES]
    fl = [Paragraph("Indoor air quality monitoring, campus procedure", s["title"]),
          Paragraph("%s, estates and compliance &nbsp;|&nbsp; Procedure note EST-14, revision 2"
                    "<br/>Approved 4 September 2026 by %s &nbsp;|&nbsp; Next review September 2027"
                    % (P.ETB_NAME, P.ESTATES_OFFICER), s["ref"]),
          Spacer(1, 7 * mm),
          Paragraph("1 &nbsp; Purpose and scope", s["h"]),
          Paragraph("This note sets out how the Board records and reports carbon dioxide "
                    "monitoring in the teaching spaces listed in schedule 1. It applies to the "
                    "%s campus for the 2026/27 year." % P.CAMPUS_NAME, s["p"]),
          Paragraph("2 &nbsp; Screening", s["h"]),
          Paragraph("A space is brought forward for assessment where its carbon dioxide "
                    "concentration passes %s ppm while the space is occupied. The indicator is a "
                    "screen for further work and is not a limit."
                    % "{:,}".format(int(P.SCREENING_PPM)), s["p"]),
          Paragraph("3 &nbsp; Conventions for reporting", s["h"]),
          Paragraph("A space counts as occupied for the hours in which the air handling unit "
                    "serving it stands in its occupied state. Each logged reading represents the "
                    "five minutes beginning at its timestamp. A reading counts in the calendar "
                    "month of its own local timestamp. Data capture is reported as the readings "
                    "received against the readings expected on the teaching days of the term.",
                    s["p"]),
          Paragraph("4 &nbsp; Rounding", s["h"]),
          Paragraph("Supply rates are reported to the nearest half litre per second per person. "
                    "Hours and occupant counts are reported to one decimal place and shares to "
                    "one decimal place as a percentage. A figure falling exactly on the rounding "
                    "point is reported upward. Figures are rounded once, at the point of "
                    "reporting, and not at any intermediate step.", s["p"]),
          Paragraph("Schedule 1 &nbsp; Spaces monitored in 2026/27", s["h"]),
          D.table([["Room", "Block", "Analyser asset"]] +
                  [[c, dict((x[0], x[2]) for x in P.SPACES)[c], "CO2-%s" % c.replace("-", "")]
                   for c in codes], [26 * mm, 32 * mm, 36 * mm]),
          Paragraph("Source: asset register extract of 4 September 2026.", s["src"])]
    D.write_pdf(os.path.join(TARGET, B.PROCEDURE),
                {"title": "Procedure note EST-14 revision 2, indoor air quality monitoring",
                 "author": "%s, estates and compliance" % P.ETB_NAME,
                 "subject": "Campus procedure for carbon dioxide monitoring",
                 "creator": "%s, estates and compliance" % P.ETB_NAME,
                 "producer": "Beldarrig ETB document services"},
                "Procedure note EST-14 revision 2", fl, "2026-09-04")

    # ---------------- the commissioning record (declared wrong-basis distractor)
    rowsd = [["Space", "Design occupancy", "Design supply litres per second",
              "Design supply per person"]]
    for c in P.BLOCK_SPACES:
        n = P.DESIGN_OCCUPANCY[c]
        rowsd.append([c, str(n), "{:,.0f}".format(n * P.DESIGN_SUPPLY_LS),
                      "%.1f" % P.DESIGN_SUPPLY_LS])
    fl = [Paragraph("Commissioning record, AHU-03 and AHU-04", s["title"]),
          Paragraph("%s &nbsp;|&nbsp; Contract 2021/KMN/M3, Tulrohan Block mechanical upgrade"
                    "<br/>Record issued 22 July 2021 &nbsp;|&nbsp; Engineer: %s"
                    % (P.COMMISSIONING_FIRM, P.COMMISSIONING_ENGINEER), s["ref"]),
          Spacer(1, 7 * mm),
          Paragraph("1 &nbsp; Scope of this record", s["h"]),
          Paragraph("Static completion and fan performance for the two replacement air handling "
                    "units serving the Tulrohan Block, together with the design air volumes "
                    "carried forward from the consulting engineer's appendix C. Fan curves, "
                    "motor currents and filter resistances were witnessed at each unit.", s["p"]),
          Paragraph("2 &nbsp; Design air volumes", s["h"]),
          D.table(rowsd, [24 * mm, 32 * mm, 48 * mm, 36 * mm], align=[1, 2, 3]),
          Paragraph("Source: consulting engineer's appendix C, issue C, March 2021.", s["src"]),
          Paragraph("3 &nbsp; Outstanding items at issue", s["h"]),
          Paragraph("Proving of air volumes at the supply terminals in each space was deferred at "
                    "the client's request so that the block could be handed back for the autumn "
                    "term, and remains outstanding at the date of this record. The figures in "
                    "section 2 are therefore design volumes at design occupancy and not volumes "
                    "measured in the spaces. Balancing dampers were left at their "
                    "commissioning-set positions.", s["p"]),
          Paragraph("4 &nbsp; Witnessed at the units", s["h"]),
          Paragraph("Fan total pressure and speed were witnessed within tolerance at both units "
                    "on 14 July 2021. No terminal-level measurement was taken. The record was "
                    "accepted by the Board subject to section 3.", s["p"])]
    D.write_pdf(os.path.join(TARGET, "commissioning_record_tulrohan_ahu.pdf"),
                {"title": "Commissioning record, contract 2021/KMN/M3",
                 "author": P.COMMISSIONING_FIRM, "subject": "Static completion, AHU-03 and AHU-04",
                 "creator": "%s, commissioning" % P.COMMISSIONING_FIRM,
                 "producer": "Westmeath Air Balancing document issue"},
                "Contract 2021/KMN/M3, commissioning record", fl, "2021-07-22")


# ===================================================================== the thread

def write_thread():
    text = """From: %s
To: %s
Sent: 11 December 2026 17:22
Subject: Tulrohan, January minor works list

Conall,

The senior management team settles the January minor works list on 14 January and I have to put
the Tulrohan bid in front of them with one number on it. Both options are costed and in the bid
sheet. What I do not have is what the block is actually getting, which is the thing they will ask
me first.

The autumn monitoring finished on 11 December and the trend export and the register are both
pulled, so the term is closed. Can you let me have the room data sheets for the block, the ones
with the volumes on them, and confirm the two unit schedules are the current settings.

Aileen


From: %s
To: %s
Sent: 12 December 2026 08:05
Subject: RE: Tulrohan, January minor works list

The record drawings are in the 19-0442 set, issue D, and I have put the room data sheets in the
same folder as the export. The time clocks are current: the two Tulrohan units went on the
timetable-linked schedule in the 2021 works and nothing has moved since, the other two are still
on the 2014 fixed clock.

One thing to flag on the export. The analyser in Annagloor 016 came out on 10 November and the
replacement went in on the 13th, so that point has nothing for three days and the span check
before it came out was out of tolerance. The work orders are in the maintenance log.

Conall
""" % (P.ESTATES_OFFICER, P.FACILITIES_MANAGER, P.FACILITIES_MANAGER, P.ESTATES_OFFICER)
    with open(os.path.join(TARGET, "minor_works_thread.txt"), "w", encoding="utf-8") as fh:
        fh.write(text)


if __name__ == "__main__":
    cut_pack()
    print("pack cut: %d files" % len(os.listdir(TARGET)))
