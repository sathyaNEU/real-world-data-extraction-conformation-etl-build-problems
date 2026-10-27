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

    # the scattered sample losses: a fixed count of teaching-day samples per space, drawn from the
    # stamps that space actually logged, plus a proportional share of non-teaching-day samples
    teaching = {iso for iso, _, k in W.calendar_days() if k == "teaching"}
    r_pick = W.rng("scatter-pick")
    lost = {}
    for code, *_ in P.SPACES:
        drop_days = set(P.DROPOUT_DAYS[code])
        pool_t, pool_o = [], []
        for i, (_, ld, lt, off) in enumerate(stamp_list):
            if ld in drop_days:
                continue
            if code == swap["space"] and ld in removed_days:
                continue
            (pool_t if ld in teaching else pool_o).append(i)
        k_t = P.SCATTERED_LOSSES[code]
        k_o = int(round(k_t * len(pool_o) / float(len(pool_t))))
        lost[code] = set(r_pick.sample(pool_t, k_t)) | set(r_pick.sample(pool_o, k_o))

    spine = []
    received = {}
    for code, *_ in P.SPACES:
        point = "KMN." + P.ROOM_LABELS[code][0]
        drop_days = set(P.DROPOUT_DAYS[code])
        for i, (_, ld, lt, off) in enumerate(stamp_list):
            if code == swap["space"] and ld in removed_days:
                continue
            if ld in drop_days or i in lost[code]:
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
    techs = list(P.MAINTENANCE_TECHNICIANS)
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
    outages = sorted((d, code) for code, days in P.DROPOUT_DAYS.items() for d in days)
    for d, code in outages:
        log.append(["WO%05d" % (13000 + r_wo.randrange(1, 900)), d, d, code,
                    "CO2-%s" % code.replace("-", ""), "Network fault, point offline", "", "",
                    r_tech.choice(techs), "Field bus segment repaired, point restored next day"])
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
                    P.FACILITIES_MANAGER, P.ETB_NAME,
                    *P.XLSX_FILED["ahu_timeclock_schedule.xlsx"])

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
    r2 = W.rng("staff-school")
    for n in P.TUTORS:
        ws2.append([W.staff_ref(n), n, "Tutor", P.TUTOR_SCHOOL[n]])
    for n in P.ASSISTANTS:
        ws2.append([W.staff_ref(n), n, "Learning support assistant", "Learner support"])
    finish(ws2, [11, 22, 27, 30])
    path = os.path.join(TARGET, "enrolment_groups_autumn2026.xlsx")
    wb.save(path)
    D.finalise_xlsx(path, "Enrolment groups, autumn term 2026", "Learner records office",
                    "Learner records office", P.ETB_NAME,
                    *P.XLSX_FILED["enrolment_groups_autumn2026.xlsx"])

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
                    P.ETB_NAME, *P.XLSX_FILED["etb_academic_calendar_2026_27.xlsx"])

    # ---- the capital bid sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Scope"
    ws.append(["Tulrohan Block, minor works bid 2027, scope of the two options"])
    ws.append([])
    ws.append(["room_code", "room_name", "net_floor_area_m2", "air_handling_unit",
               "as_built_sheet_ref", "in_scope"])
    areas = {s[0]: s[8] for s in P.SPACES}
    for code in P.BLOCK_SPACES:
        ws.append([code, dict((s[0], s[1]) for s in P.SPACES)[code], areas[code],
                   dict((s[0], s[3]) for s in P.SPACES)[code],
                   "RDS-TUL-%s" % code.split("-")[1], "Yes"])
    ws.append(["Total", "", "=SUM(C4:C9)", "", "", ""])
    finish(ws, [12, 30, 18, 18, 20, 10], freeze="A4")
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
                    P.ESTATES_OFFICER, P.ETB_NAME,
                    *P.XLSX_FILED["capital_bid_tulrohan_block.xlsx"])


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
                "19-0442 Room data sheets, issue D", fl, P.PDF_FILED["asbuilt_room_data_sheets_kilmoneen.pdf"])

    # ---------------- the standard extract
    g = P.GENERATION_L_PER_S
    fl = [Paragraph("%s: Ventilation and indoor air quality in education buildings" % P.STANDARD_REF,
                    s["title"]),
          Paragraph("%s<br/>%s &nbsp;|&nbsp; Extract: section 4, ventilation of teaching spaces, "
                    "and table 2.3" % (P.STANDARD_ISSUER, P.STANDARD_EDITION), s["ref"]),
          Spacer(1, 7 * mm),
          Paragraph("%s &nbsp; Teaching spaces" % P.STANDARD_CLAUSE_REQUIREMENT, s["h"]),
          Paragraph("A teaching space shall be provided with outdoor air at not less than "
                    "%g litres per second per person at the occupancy at which the space is used. "
                    "The requirement applies to each teaching space separately."
                    % P.REQUIRED_LS_PER_PERSON, s["p"]),
          Paragraph("%s &nbsp; Demonstrating compliance" % P.STANDARD_CLAUSE_COMPLIANCE, s["h"]),
          Paragraph("Compliance is demonstrated by the outdoor-air supply rate a space achieves "
                    "in use, established in that space and over the periods for which it is "
                    "timetabled. Records of design information and of plant performance are kept "
                    "with the assessment and are not a substitute for it.", s["p"]),
          Paragraph("%s &nbsp; Reporting" % P.STANDARD_CLAUSE_REPORTING, s["h"]),
          Paragraph("Rates are reported per person present. Where a space serves groups of "
                    "different size the rate is reported over the whole of the period assessed "
                    "rather than for a single group.", s["p"]),
          Paragraph("Table %s &nbsp; Design data, occupant emissions" % P.STANDARD_TABLE, s["h"]),
          D.table([["Quantity", "Value", "Unit"],
                   ["Carbon dioxide generation, one occupant of a teaching or practical space",
                    "%.4f" % g, "litres per second"],
                   ["Sensible heat gain, one occupant of a teaching or practical space", "75",
                    "watts"],
                   ["Moisture gain, one occupant of a teaching or practical space", "0.050",
                    "grammes per second"]],
                  [86 * mm, 24 * mm, 38 * mm], align=[1]),
          Paragraph("Source: table %s, unchanged from the 2019 edition." % P.STANDARD_TABLE, s["src"]),
          Paragraph("Requirement %s replaces the air change rate given in the 2009 guidance. "
                    "Where a space was built to the earlier guidance the requirement applies on "
                    "the next substantial alteration or on the next assessment of the space, "
                    "whichever is earlier." % P.STANDARD_CLAUSE_REQUIREMENT, s["p"])]
    D.write_pdf(os.path.join(TARGET, B.STANDARD),
                {"title": "%s extract, sections %s to %s and table %s" % (P.STANDARD_REF, P.STANDARD_CLAUSE_REQUIREMENT, P.STANDARD_CLAUSE_REPORTING, P.STANDARD_TABLE),
                 "author": P.STANDARD_ISSUER,
                 "subject": "Technical guidance for education buildings",
                 "creator": "%s" % P.STANDARD_ISSUER,
                 "producer": "Department of Education publications service"},
                "%s, %s" % (P.STANDARD_REF, P.STANDARD_EDITION), fl, P.PDF_FILED["tgd_m4_ventilation_extract.pdf"])

    # ---------------- the campus monitoring procedure note
    codes = [x[0] for x in P.SPACES]
    fl = [Paragraph("Indoor air quality monitoring, campus procedure", s["title"]),
          Paragraph("%s, estates and compliance &nbsp;|&nbsp; Procedure note %s, revision 2"
                    "<br/>Approved 4 September 2026 by %s &nbsp;|&nbsp; Next review September 2027"
                    % (P.ETB_NAME, P.PROCEDURE_REF, P.ESTATES_OFFICER), s["ref"]),
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
          Paragraph("4 &nbsp; Occupants present", s["h"]),
          Paragraph("The occupants present in a session are the persons the attendance register "
                    "marks present for that session, in whichever role the register records them: "
                    "learners, the tutor taking the session and any learning support assistant "
                    "alike. A person the register marks absent, or absent with authorisation, is "
                    "not present. The register holds one mark for each person for each session, "
                    "and a mark corrected after the session stands as corrected, so the amendment "
                    "flag records that a correction was made and does not set a second mark "
                    "aside.", s["p"]),
          Paragraph("5 &nbsp; Rounding", s["h"]),
          Paragraph("Supply rates are reported to the nearest half litre per second per person. "
                    "Hours are reported to two decimal places, occupant counts as whole persons "
                    "and shares to one decimal place as a percentage. A figure falling exactly on "
                    "the rounding point is reported upward. Figures are rounded once, at the point "
                    "of reporting, and not at any intermediate step.", s["p"]),
          Paragraph("Schedule 1 &nbsp; Spaces monitored in 2026/27", s["h"]),
          D.table([["Room", "Block", "Analyser asset"]] +
                  [[c, dict((x[0], x[2]) for x in P.SPACES)[c], "CO2-%s" % c.replace("-", "")]
                   for c in codes], [26 * mm, 32 * mm, 36 * mm]),
          Paragraph("Source: asset register extract of 4 September 2026.", s["src"])]
    D.write_pdf(os.path.join(TARGET, B.PROCEDURE),
                {"title": "Procedure note %s revision 2, indoor air quality monitoring" % P.PROCEDURE_REF,
                 "author": "%s, estates and compliance" % P.ETB_NAME,
                 "subject": "Campus procedure for carbon dioxide monitoring",
                 "creator": "%s, estates and compliance" % P.ETB_NAME,
                 "producer": "Beldarrig ETB document services"},
                "Procedure note %s revision 2" % P.PROCEDURE_REF, fl, P.PDF_FILED["iaq_monitoring_procedure_note.pdf"])

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
                    "measured in the spaces. Regulating dampers were left at their "
                    "commissioning-set positions.", s["p"]),
          Paragraph("4 &nbsp; Witnessed at the units", s["h"]),
          Paragraph("Fan total pressure and speed were witnessed within tolerance at both units "
                    "on 14 July 2021. No terminal-level measurement was taken. The record was "
                    "accepted by the Board subject to section 3.", s["p"])]
    D.write_pdf(os.path.join(TARGET, "commissioning_record_tulrohan_ahu.pdf"),
                {"title": "Commissioning record, contract 2021/KMN/M3",
                 "author": P.COMMISSIONING_FIRM, "subject": "Static completion, AHU-03 and AHU-04",
                 "creator": "%s, commissioning" % P.COMMISSIONING_FIRM,
                 "producer": "Westmeath Commissioning Services document issue"},
                "Contract 2021/KMN/M3, commissioning record", fl, P.PDF_FILED["commissioning_record_tulrohan_ahu.pdf"])


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


# ===================================================================== the figures, from the pack

def occupied_state(target):
    """A lookup from (unit, local date, local hh:mm) to the unit's state, from the status log."""
    ps = B.plant_state(target)

    def state(ahu, date, hhmm):
        m = int(hhmm[:2]) * 60 + int(hhmm[3:5])
        for a, b, st in ps.get((ahu, date), ()):
            if a <= m < b:
                return st
        return "OFF"
    return state


def measure(target):
    """Every shipped figure, computed from target/ and nothing else."""
    import csv as _csv
    vols = B.room_volumes(target)
    std = B.standard_figures(target)
    A.VOL = vols
    A.G = std["generation_l_per_s"] / 1000.0
    required = std["required_ls_per_person"]
    screen = B.screening_ppm(target)
    block = B.block_rooms(target)
    teaching = set(B.teaching_days(target))
    state = occupied_state(target)
    reg = [r for r in B.rows(target, B.REGISTER) if r["bms_point_ref"]]
    ahu_of = {r["room_code"]: r["ahu_ref"] for r in reg}
    spaces = sorted(ahu_of)

    frames = B.frames(target)
    frames_strict = B.frames(target, strict=True)
    bf = [x for x in frames if x["space"] in block]
    bfs = [x for x in frames_strict if x["space"] in block]

    call = A.aggregate(bf, lambda x: A.q_integrated(x))
    out = {
        "constants": {
            "required_ls_per_person": required,
            "generation_l_per_s": std["generation_l_per_s"],
            "screening_ppm": screen,
            "rate_bin": P.RATE_BIN,
            "standard_clause_requirement": P.STANDARD_CLAUSE_REQUIREMENT,
            "standard_clause_compliance": P.STANDARD_CLAUSE_COMPLIANCE,
            "standard_table": P.STANDARD_TABLE,
            "procedure_ref": P.PROCEDURE_REF,
            "window_start": P.TERM_START,
            "window_end": P.TERM_END,
            "teaching_days": len(teaching),
            "readings_per_day": 24 * 3600 // P.STEP_S,
            "block_rooms": block,
            "block_volumes_m3": {k: vols[k] for k in block},
        },
        "call": {
            "block_rate_ls_per_occupant": to_bin(call),
            "block_rate_unrounded": round(call, 4),
            "verdict": "below the %g litres per second per person TGD-M4 requires" % required,
            "shortfall_factor": round(required / call, 3),
            "remedy": "Option A, replace AHU-03 and AHU-04 and the Tulrohan distribution",
        },
    }

    # ---- critical components
    sess = B.sessions(target)
    bsess = [s for s in sess if s["space"] in block]
    occ_hours = sum(s["occupants"] * (int(s["end"][:2]) * 60 + int(s["end"][3:5])
                                      - int(s["start"][:2]) * 60 - int(s["start"][3:5]))
                    for s in bsess) / 60.0
    per_space_rate = A.per_space(bf, lambda x: A.q_integrated(x))
    air_m3 = sum(A.q_integrated(x) * x["seconds"] for x in bf)
    resp = {k: vols[k] / A.q_integrated_space(bf, k) / 60.0 for k in block}
    out["components"] = {
        "block_sessions": len(bsess),
        "occupant_hours_present": half_up(occ_hours, 1),
        "shortest_response_minutes": int(math.floor(min(resp.values()))),
        "period_minutes": 55,
        "spaces_below_requirement": sum(1 for k in block if per_space_rate[k] < required),
        "spaces_in_block": len(block),
    }

    # ---- the ladder and the families, measured on the pack
    rivals = {b: A.aggregate(bf, lambda x, bb=b: A.q_steady(x, bb))
              for b in ("session mean", "final 15 minutes", "last sample", "peak sample",
                        "median sample", "95th percentile")}
    gfam = {}
    for q in A.QUAD:
        gfam["%s quadrature" % q] = A.aggregate(bf, lambda x, qq=q: A.q_integrated(x, quad=qq))
    for e in (2, 3):
        gfam["%d minute decimation" % (5 * e)] = A.aggregate(bf, lambda x, ee=e: A.q_integrated(x, every=ee))
    reg_q = A.q_regression(bf)
    gfam["derivative regression"] = (1000.0 * sum(reg_q[x["space"]] * x["seconds"] for x in bf)
                                     / sum(x["occupants"] * x["seconds"] for x in bf))
    out["measured"] = {
        "rivals": {k: round(v, 4) for k, v in rivals.items()},
        "golden_family": {k: round(v, 4) for k, v in gfam.items()},
        "golden_strict_variant": round(A.aggregate(bfs, lambda x: A.q_integrated(x)), 4),
        "pooled_over_14": round(A.aggregate(frames, lambda x: A.q_integrated(x)), 4),
        "naive_per_space": {k: round(v, 4) for k, v in
                            A.per_space(bf, lambda x: A.q_steady(x, "session mean")).items()},
        "truth_per_space": {k: round(v, 4) for k, v in per_space_rate.items()},
        "response_time_min": {k: round(resp[k], 1) for k in block},
        "outdoor_air_supplied_m3": int(half_up(air_m3, 0)),
        "per_space_rate_unrounded": {k: round(per_space_rate[k], 4) for k in block},
        "bin_edge_call": round(A.bin_edge_distance(call), 4),
    }

    # ---- ask A: recorded occupied hours and occupied hours over the indicator
    hours = {}
    over = {}
    with open(os.path.join(target, B.SPINE), newline="", encoding="utf-8") as fh:
        for r in _csv.DictReader(fh):
            sp, ts = r["space_code"], r["timestamp_local"]
            if state(ahu_of[sp], ts[:10], ts[11:16]) != "OCCUPIED":
                continue
            key = (sp, ts[:7])
            hours[key] = hours.get(key, 0) + 1
            if B.ppm(r["co2"]) > screen:
                over[key] = over.get(key, 0) + 1
    ask_a = []
    for sp in spaces:
        for key, label in MONTHS:
            ask_a.append({"space": sp, "month": label,
                          "occupied_hours": half_up(hours.get((sp, key), 0) / 12.0, 2),
                          "hours_over_indicator": half_up(over.get((sp, key), 0) / 12.0, 2)})

    # ---- ask B: capture share over the term
    recv = {}
    with open(os.path.join(target, B.SPINE), newline="", encoding="utf-8") as fh:
        for r in _csv.DictReader(fh):
            if r["timestamp_local"][:10] in teaching:
                recv[r["space_code"]] = recv.get(r["space_code"], 0) + 1
    expected = 288 * len(teaching)
    ask_b = [{"space": sp, "received": recv.get(sp, 0), "expected": expected,
              "share_pct": half_up(100.0 * recv.get(sp, 0) / expected, 1)} for sp in spaces]

    # ---- ask C: mean occupants present per timetabled session
    ask_c = []
    for sp in block:
        rowsc = [s for s in bsess if s["space"] == sp]
        ask_c.append({"space": sp, "sessions": len(rowsc),
                      "mean_occupants": int(half_up(sum(s["occupants"] for s in rowsc) / len(rowsc), 0))})

    # ---- ask D: the four largest within-session rises in the block
    rises = sorted(((x["readings"][-1] - x["readings"][0], x["space"], x["date"], x["period"])
                    for x in bf), reverse=True)
    ask_d = [{"rank": i + 1, "space": r[1], "date": r[2], "period": r[3]}
             for i, r in enumerate(rises[:4])]
    out["asks"] = {"A": ask_a, "B": ask_b, "C": ask_c, "D": ask_d}
    out["ask_detail"] = {"rises_top6": [(round(r[0], 1), r[1], r[2], r[3]) for r in rises[:6]],
                         "rise_gap_4_to_5": round(rises[3][0] - rises[4][0], 2)}
    return out


# ===================================================================== the goldens

PALETTE = {"surface": "#fcfcfb", "ink": "#0b0b0b", "ink2": "#52514e", "series1": "#2a78d6",
           "series3": "#1baf7a", "critical": "#d03b3b", "grid": "#d8d7d2"}


def write_goldens(m, target):
    if os.path.isdir(GOLDEN):
        shutil.rmtree(GOLDEN)
    os.makedirs(GOLDEN)
    golden_workbook(m)
    golden_chart(m, target)
    for f in sorted(os.listdir(GOLDEN)):
        os.utime(os.path.join(GOLDEN, f), (MTIME, MTIME))


def golden_workbook(m):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter

    bold = Font(bold=True)
    head = Font(bold=True, color="FFFFFF")
    fill = PatternFill("solid", fgColor="1F4E79")
    thin = Side(style="thin", color="BFBFBF")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Assessment"
    c = m["call"]
    comp = m["components"]
    rowsa = [
        ("Tulrohan Block, outdoor air per occupant present, autumn term 2026", ""),
        ("", ""),
        ("Outdoor air supplied, litres per second per occupant present",
         c["block_rate_ls_per_occupant"]),
        ("TGD-M4 requirement 4.2, litres per second per person",
         m["constants"]["required_ls_per_person"]),
        ("Requirement as a multiple of the rate achieved", half_up(c["shortfall_factor"], 2)),
        ("Teaching spaces in the block below the requirement",
         "%d of %d" % (comp["spaces_below_requirement"], comp["spaces_in_block"])),
        ("", ""),
        ("Timetabled sessions assessed, 28 Sep to 11 Dec 2026", comp["block_sessions"]),
        ("Occupant-hours present across those sessions", comp["occupant_hours_present"]),
        ("Shortest response time in the block, volume over supply, minutes",
         comp["shortest_response_minutes"]),
        ("Length of a teaching period, minutes", comp["period_minutes"]),
        ("", ""),
        ("Recommendation for the January minor works allocation",
         "Option A, replace AHU-03 and AHU-04 and the Tulrohan supply and extract distribution"),
    ]
    for r in rowsa:
        ws.append(list(r))
    ws["A1"].font = Font(bold=True, size=13)
    for r in (3, 4, 5, 6, 8, 9, 10, 11, 13):
        ws.cell(row=r, column=1).font = bold
    ws["B3"].number_format = "0.0"
    ws["B4"].number_format = "0.0"
    ws["B5"].number_format = '0.00"x"'
    ws["B9"].number_format = "#,##0.0"
    ws["B13"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.column_dimensions["A"].width = 62
    ws.column_dimensions["B"].width = 46
    ws.row_dimensions[13].height = 30

    ws2 = wb.create_sheet("Occupied hours by month")
    ws2.append(["Room", "Block", "Month", "Occupied hours recorded",
                "Occupied hours above 1,500 ppm"])
    block_of = {s[0]: s[2] for s in P.SPACES}
    for a in m["asks"]["A"]:
        ws2.append([a["space"], block_of[a["space"]], a["month"], a["occupied_hours"],
                    a["hours_over_indicator"]])
    for col in ("D", "E"):
        for cell in ws2[col][1:]:
            cell.number_format = "0.00"

    ws3 = wb.create_sheet("Data capture")
    ws3.append(["Room", "Block", "Readings received", "Readings expected", "Capture share %"])
    for b in m["asks"]["B"]:
        ws3.append([b["space"], block_of[b["space"]], b["received"], b["expected"],
                    b["share_pct"]])
    for cell in ws3["E"][1:]:
        cell.number_format = "0.0"
    for col in ("C", "D"):
        for cell in ws3[col][1:]:
            cell.number_format = "#,##0"

    ws4 = wb.create_sheet("Session occupancy")
    ws4.append(["Room", "Timetabled sessions", "Mean occupants present per session"])
    for x in m["asks"]["C"]:
        ws4.append([x["space"], x["sessions"], x["mean_occupants"]])
    for cell in ws4["C"][1:]:
        cell.number_format = "0"

    ws5 = wb.create_sheet("Largest session rises")
    ws5.append(["Rank", "Room", "Date", "Period"])
    for x in m["asks"]["D"]:
        ws5.append([x["rank"], x["space"], x["date"], x["period"]])

    ws6 = wb.create_sheet("Basis")
    ws6.append(["Item", "Basis used"])
    for k, v in [
        ("Assessed period", "28 September to 11 December 2026, the autumn term's "
                            "timetabled sessions"),
        ("Population", "the six Tulrohan Block rooms in the minor works bid scope"),
        ("Denominator", "the persons the attendance register marks present, in whichever role, "
                        "procedure note %s section 4" % P.PROCEDURE_REF),
        ("Occupied hours", "the hours the serving air handling unit stands in its occupied "
                           "state, procedure note %s section 3" % P.PROCEDURE_REF),
        ("Readings expected", "288 a day on the 48 teaching days of the term, "
                              "procedure note %s section 3" % P.PROCEDURE_REF),
        ("Outdoor baseline", "the campus analyser, and the Mace Head station for 12 to 25 "
                             "October while the campus analyser was away"),
        ("Rounding", "once at the point of reporting, procedure note %s section 5"
                     % P.PROCEDURE_REF),
        ("Source of volumes", "as-built room data sheets, project 19-0442 issue D"),
        ("Extract pulled", P.EXPORT_DATE),
    ]:
        ws6.append([k, v])
    for cell in ws6["B"][1:]:
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    ws6.column_dimensions["A"].width = 22
    ws6.column_dimensions["B"].width = 78

    for ws_ in (ws2, ws3, ws4, ws5):
        for cell in ws_[1]:
            cell.font = head
            cell.fill = fill
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = Border(bottom=thin)
        ws_.freeze_panes = "A2"
        ws_.auto_filter.ref = ws_.dimensions
    for ws_, widths in ((ws2, [10, 11, 16, 15, 17]), (ws3, [10, 11, 18, 18, 15]),
                        (ws4, [10, 20, 30]), (ws5, [7, 10, 13, 10]), ):
        for i, w in enumerate(widths, start=1):
            ws_.column_dimensions[get_column_letter(i)].width = w
    ws6["A1"].font = head
    ws6["A1"].fill = fill
    ws6["B1"].font = head
    ws6["B1"].fill = fill
    ws2.print_area = "A1:E57"
    ws2.print_title_rows = "1:1"

    path = os.path.join(GOLDEN, P.WORKBOOK_NAME)
    wb.save(path)
    D.finalise_xlsx(path, "Tulrohan Block ventilation assessment, autumn term 2026",
                    P.ESTATES_OFFICER, P.ESTATES_OFFICER, P.ETB_NAME,
                    *P.XLSX_FILED["tulrohan_ventilation_assessment.xlsx"])


def golden_chart(m, target):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt

    space = m["asks"]["D"][0]["space"]
    day = m["asks"]["D"][0]["date"]
    ser = B.series(target)[space]
    base = B.outdoor_baseline(target)
    pts = sorted((dt.datetime.fromisoformat(ts), v, base[(ts[:13], off)])
                 for (ts, off), v in ser.items() if ts[:10] == day)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    bl = [p[2] for p in pts]

    sess = sorted((s for s in B.sessions(target) if s["space"] == space and s["date"] == day),
                  key=lambda s: s["start"])
    plant = B.plant_state(target)
    ahu = {s[0]: s[3] for s in P.SPACES}[space]

    fig, ax = plt.subplots(figsize=(12.6, 6.6), dpi=170)
    fig.patch.set_facecolor(PALETTE["surface"])
    ax.set_facecolor(PALETTE["surface"])
    for a, b, st in plant.get((ahu, day), ()):
        if st == "SETBACK":
            ax.axvspan(dt.datetime.fromisoformat(day) + dt.timedelta(minutes=a),
                       dt.datetime.fromisoformat(day) + dt.timedelta(minutes=b),
                       color="#ecebe4", zorder=0)
    for s in sess:
        a = dt.datetime.fromisoformat("%s %s" % (day, s["start"]))
        b = dt.datetime.fromisoformat("%s %s" % (day, s["end"]))
        ax.axvspan(a, b, color="#dbe8f8", zorder=0)
    ax.plot(xs, ys, color=PALETTE["series1"], linewidth=2.2, zorder=3,
            label="%s, logged every five minutes" % space)
    ax.plot(xs, bl, color=PALETTE["ink2"], linewidth=1.3, linestyle=(0, (4, 3)), zorder=2,
            label="campus outdoor analyser")
    screen = m["constants"]["screening_ppm"]
    ax.axhline(screen, color=PALETTE["critical"], linewidth=1.7, linestyle=(0, (6, 3)), zorder=4)

    lo, hi = 380, max(ys) * 1.14
    for s in sess:
        a = dt.datetime.fromisoformat("%s %s" % (day, s["start"]))
        b = dt.datetime.fromisoformat("%s %s" % (day, s["end"]))
        ax.text(a + (b - a) / 2, hi * 0.995, "%s\n%d present" % (s["period"], s["occupants"]),
                ha="center", va="top", fontsize=8.4, color=PALETTE["ink2"], linespacing=1.4)
    first = sess[0]
    a = dt.datetime.fromisoformat("%s %s" % (day, first["start"]))
    b = dt.datetime.fromisoformat("%s %s" % (day, first["end"]))
    y0 = next(y for x, y in zip(xs, ys) if x == a)
    y1 = next(y for x, y in zip(xs, ys) if x == b)
    ax.annotate("", xy=(b, y1), xytext=(b, y0),
                arrowprops=dict(arrowstyle="<->", color=PALETTE["series3"], linewidth=1.6))
    ax.annotate("the period ends %d ppm above where it started,\nand the slope is still positive"
                % round(y1 - y0), xy=(b, (y0 + y1) / 2), xytext=(14, -6),
                textcoords="offset points", fontsize=9.4, color=PALETTE["series3"],
                linespacing=1.45)
    ax.set_ylim(lo, hi)
    ax.set_xlim(dt.datetime.fromisoformat(day + " 06:00"),
                dt.datetime.fromisoformat(day + " 18:00"))
    ax.text(dt.datetime.fromisoformat(day + " 06:10"), screen + 24,
            "%s ppm screening indicator" % "{:,}".format(int(screen)),
            color=PALETTE["critical"], fontsize=9.4)
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.yaxis.set_major_locator(plt.MultipleLocator(200))
    ax.set_ylabel("carbon dioxide, ppm", color=PALETTE["ink2"], fontsize=10)
    ax.grid(axis="y", color=PALETTE["grid"], linewidth=0.7)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(PALETTE["grid"])
    ax.tick_params(colors=PALETTE["ink2"], labelsize=9)
    ax.set_title("No period ends at a settled level: the block gets %.1f litres per second per "
                 "occupant present, not the %g TGD-M4 requires"
                 % (m["call"]["block_rate_ls_per_occupant"],
                    m["constants"]["required_ls_per_person"]),
                 loc="left", fontsize=13.0, color=PALETTE["ink"], pad=30)
    ax.text(0.0, 1.018, "%s, %s. Blue bands are the timetabled periods; the grey band at midday "
                        "is AHU-03 at setback." % (space, dt.date.fromisoformat(day).strftime(
                            "%A %d %B %Y")),
            transform=ax.transAxes, fontsize=9.4, color=PALETTE["ink2"])
    ax.legend(loc="upper left", bbox_to_anchor=(0.012, 0.80), frameon=False, fontsize=9.4,
              labelcolor=PALETTE["ink2"])
    fig.text(0.008, 0.013, "Source: bms_co2_5min_autumn2026.csv, timetable_autumn2026.csv, "
                           "attendance_marks_autumn2026.csv and campus_outdoor_co2_hourly_2026.csv, "
                           "extract of %s." % P.EXPORT_DATE,
             fontsize=8.2, color=PALETTE["ink2"])
    fig.tight_layout(rect=(0, 0.035, 1, 1))
    path = os.path.join(GOLDEN, P.CHART_NAME)
    fig.savefig(path, facecolor=PALETTE["surface"],
                metadata={"Software": "%s, estates and compliance" % P.ETB_NAME,
                          "Author": P.ESTATES_OFFICER,
                          "Title": "Tulrohan Block carbon dioxide day profile",
                          "Creation Time": "2026-12-18T11:05:00"})
    plt.close(fig)
    raw = open(path, "rb").read()
    assert b"matplotlib" not in raw.lower(), "chart carries the writer signature"


# ===================================================================== figures, metadata, write-up

def write_figures(m):
    path = os.path.join(HERE, "figures.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(m, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return path


def file_rows(target):
    counts = {}
    for name in sorted(os.listdir(target)):
        if name.endswith(".csv"):
            with open(os.path.join(target, name), encoding="utf-8") as fh:
                counts[name] = sum(1 for _ in fh) - 1
        else:
            counts[name] = ""
    return counts


def write_metadata(m, target):
    counts = file_rows(target)
    src = {
        B.SPINE: ("Building management system trend export, Kilmoneen campus, pulled %s"
                  % P.EXPORT_DATE),
        B.PLANT: "Building management system plant status log, pulled %s" % P.EXPORT_DATE,
        B.TIMETABLE: "Learner records system timetable export, autumn term 2026",
        B.MARKS: "Statutory attendance register export, autumn term 2026",
        B.CAMPUS_OUT: "Campus outdoor analyser hourly means, 1 September to 11 December 2026",
        B.STATION_OUT: ("Hourly background carbon dioxide, %s, in the layout that station "
                        "publishes" % P.NATIONAL_STATION),
        B.REGISTER: "Campus room register, estates asset system",
        B.ASBUILT: "As-built room data sheets, consulting engineer's record set 19-0442 issue D",
        B.STANDARD: "Extract of the Department of Education technical guidance %s" % P.STANDARD_REF,
        B.PROCEDURE: "Education and Training Board procedure note %s revision 2" % P.PROCEDURE_REF,
        B.BID: "Minor works capital bid sheet for the Tulrohan Block, 2027 programme",
        B.CALENDAR: "Education and Training Board academic calendar 2026/27",
        "ahu_timeclock_schedule.xlsx": "Building management system time clock settings export",
        "enrolment_groups_autumn2026.xlsx": "Learner records system enrolment and staff export",
        "maintenance_log_iaq_sensors_2026.csv": ("Maintenance contractor's work order log for the "
                                                 "carbon dioxide analysers"),
        "campus_energy_halfhourly_2026.csv": "Half-hourly metered electricity import, two meter points",
        "bms_temperature_rh_hourly_autumn2026.csv": ("Building management system hourly air "
                                                     "temperature and relative humidity export"),
        "commissioning_record_tulrohan_ahu.pdf": ("Commissioning contractor's static completion "
                                                  "record for AHU-03 and AHU-04, July 2021"),
        "minor_works_thread.txt": "Internal electronic mail thread, estates and facilities",
    }
    meta = {
        "task": "task204",
        "as_of": P.EXPORT_DATE,
        "bundle": "target/",
        "answer": None,
        "files": {name: {"rows": counts[name], "source": src[name],
                         "licence": "Synthetic record, no third party rights",
                         "date": P.EXPORT_DATE} for name in counts},
        "distractor_files": [
            "campus_energy_halfhourly_2026.csv",
            "bms_temperature_rh_hourly_autumn2026.csv",
        ],
        "wrong_basis_distractor": {
            "file": "commissioning_record_tulrohan_ahu.pdf",
            "basis": ("design supply of %.1f litres per second per person at design occupancy, "
                      "carried from the consulting engineer's appendix C"
                      % P.DESIGN_SUPPLY_LS),
            "ruled_out_by": ("its own section 3, which records that proving of air volumes at the "
                             "supply terminals was deferred and remains outstanding, and TGD-M4 "
                             "4.3, which says design intent and volumes proved at a unit do not "
                             "demonstrate compliance"),
            "value": P.DESIGN_SUPPLY_LS,
        },
        "stated_inputs": ["1,500", "1500", "8", "0.5", "2026", "28", "11"],
        "field_terms": [],
        "notes": ("Synthetic pack describing a fictional Education and Training Board campus in the "
                  "Irish west midlands. Building physics, Irish local time and its October change, "
                  "school building ventilation practice and the Mace Head station's publishing "
                  "layout are real; every board, campus, block, room, group, learner, staff member "
                  "and work order is invented. Built by generator/build.py from generator/params.py."),
    }
    path = os.path.join(TASK, "metadata.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1, sort_keys=True)
        fh.write("\n")


def write_submission(m):
    c, comp, k = m["call"], m["components"], m["constants"]
    block_of = {s[0]: s[2] for s in P.SPACES}
    L = []
    w = L.append
    w("## Tags\n")
    w("**Domain:** Physical and environmental sciences (indoor air quality monitoring of an "
      "education estate).")
    w("**Analytical objective:** Anomaly Detection and Diagnostics.\n")

    w("## 1. Final Recommendation\n")
    w("**January's minor-works allocation funds option A, replacing AHU-03 and AHU-04 and the "
      "Tulrohan supply and extract distribution.**")
    w("The block's six teaching spaces are supplied with **%.1f** litres per second per occupant "
      "present across the term's timetabled sessions, so the **%g** TGD-M4 requires is **%.2f** "
      "times the rate achieved. Not the timetable change, which leaves the supply where it is. "
      "Not the commissioning record's design supply, which its own outstanding-items section "
      "records as never proved at the spaces."
      % (c["block_rate_ls_per_occupant"], k["required_ls_per_person"], c["shortfall_factor"]))
    w("")

    w("## 2. Critical Components\n")
    w("1. Timetabled sessions in the six block rooms over 28 September to 11 December 2026: "
      "**%s**" % "{:,}".format(comp["block_sessions"]))
    w("2. Occupant-hours present across those sessions: **%s**"
      % "{:,.1f}".format(comp["occupant_hours_present"]))
    w("3. Shortest response time in the block, gross internal volume over the outdoor air "
      "recovered: **%d minutes**, against a teaching period of **%d minutes**"
      % (comp["shortest_response_minutes"], comp["period_minutes"]))
    w("4. Block rooms below the requirement on their own records: **%d of %d**"
      % (comp["spaces_below_requirement"], comp["spaces_in_block"]))
    w("")

    w("## 3. Step-by-Step Solution\n")
    w("1. Keyed bms_co2_5min_autumn2026.csv to room codes through campus_room_register.csv and "
      "took each reading's excess over campus_outdoor_co2_hourly_2026.csv, filling the analyser's "
      "12 to 25 October absence from macehead_gaw_co2_hourly_2026.csv.")
    w("2. Took the six rooms in scope from capital_bid_tulrohan_block.xlsx and their gross "
      "internal volumes from asbuilt_room_data_sheets_kilmoneen.pdf.")
    w("3. Took the block's sessions from timetable_autumn2026.csv and the occupants present in "
      "each from attendance_marks_autumn2026.csv: %s sessions and %s occupant-hours."
      % ("{:,}".format(comp["block_sessions"]),
         "{:,.1f}".format(comp["occupant_hours_present"])))
    w("4. Integrated each session's carbon dioxide balance across the session, the stored term "
      "being the room's volume times the change between the session's first and last reading and "
      "the source term the %s litres per second per person in the TGD-M4 extract's design data "
      "table times the occupants present, and solved each session for the outdoor air supplied."
      % k["generation_l_per_s"])
    w("5. Divided the outdoor air so recovered by the occupant-seconds present over the same "
      "sessions: %.1f litres per second per occupant present, against the %g TGD-M4 requires."
      % (c["block_rate_ls_per_occupant"], k["required_ls_per_person"]))
    w("6. Checked that no reading in the record is a settled one: the shortest response time in "
      "the block, volume over the recovered supply, is %d minutes against a %d minute period, and "
      "%d of the %d rooms sit below the requirement."
      % (comp["shortest_response_minutes"], comp["period_minutes"],
         comp["spaces_below_requirement"], comp["spaces_in_block"]))
    w("7. Counted occupied hours, hours over the indicator and readings received on procedure note "
      "%s's bases, the unit's occupied state from bms_plant_status_autumn2026.csv, five "
      "minutes to a reading, and %d a day on the %d teaching days in "
      "etb_academic_calendar_2026_27.xlsx."
      % (k["procedure_ref"], k["readings_per_day"], k["teaching_days"]))
    w("8. The allocation funds option A in capital_bid_tulrohan_block.xlsx, the air-handling "
      "replacement, and not option B.")
    w("")

    w("## 4. Deliverable Answers\n")
    w("### %s\n" % P.WORKBOOK_NAME)
    w("1. Outdoor air supplied to the Tulrohan Block across the term's timetabled sessions: "
      "**%.1f** litres per second per occupant present; remedy: option A, replace AHU-03 and "
      "AHU-04 and the Tulrohan supply and extract distribution."
      % c["block_rate_ls_per_occupant"])
    w("2. Occupied hours recorded and occupied hours over 1,500 ppm, each monitored space by "
      "calendar month, 56 rows in room then month order, hours to two decimals:")
    for a in m["asks"]["A"]:
        w("   - %s, %s: %.2f recorded, %.2f over" % (a["space"], a["month"], a["occupied_hours"],
                                                     a["hours_over_indicator"]))
    w("3. Share of expected readings received over the term, each monitored space, one decimal "
      "as a percentage:")
    for b in m["asks"]["B"]:
        w("   - %s: %.1f" % (b["space"], b["share_pct"]))
    w("4. Mean occupants present per timetabled session, the six block rooms, nearest whole:")
    for x in m["asks"]["C"]:
        w("   - %s: %d" % (x["space"], x["mean_occupants"]))
    w("5. The four largest rises between a timetabled session's first and last reading in the "
      "block, in descending order:")
    for x in m["asks"]["D"]:
        w("   - %s, period %s on %s" % (x["space"], x["period"], x["date"]))
    w("")
    w("### %s\n" % P.CHART_NAME)
    w("6. One space's timetabled sessions across a day, the five-minute carbon dioxide trace "
      "against the campus outdoor analyser, the timetabled periods and the midday setback shaded, "
      "the 1,500 ppm screening indicator drawn and labelled, the occupants present marked on each "
      "period, and the block's rate against the requirement stated in the title.")
    w("")
    path = os.path.join(TASK, "submission.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


if __name__ == "__main__":
    cut_pack()
    print("pack cut: %d files" % len(os.listdir(TARGET)))
    _m = measure(TARGET)
    write_goldens(_m, TARGET)
    print("goldens: %s" % ", ".join(sorted(os.listdir(GOLDEN))))
    write_figures(_m)
    write_metadata(_m, TARGET)
    write_submission(_m)
    print("figures.json, metadata.json and submission.md written")
