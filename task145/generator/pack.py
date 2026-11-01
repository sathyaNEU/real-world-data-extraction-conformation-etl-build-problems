"""task145 architecture 2: write the network's own exports from the clean truth (world.py). Each Layer 1 item is what
the system that writes it does: the student-information system changed in summer 2024 (the legacy year's minutes
against the new system's portions and periods, legacy ids, renamed exit codes), the new system opens a local id per
enrolment record, the state's id sync runs weeks behind, an exit is often entered days after the student starts at
another of the network's schools (the old school marks the student absent meanwhile), the behaviour system keeps an
amended suspension as a new incident, and the attendance office posts only some suspension days."""
import csv
import datetime as dt
import os

import numpy as np

import params as P
import world as WD

D = dt.timedelta
LEGACY = "2023-24"
OTHER_SCHOOLS = ["Pueblo Ridge High School", "Adams Valley Online Academy", "Westfield Senior High",
                 "Front Range Early College", "Las Animas County High", "Northgate STEM Academy",
                 "Big Sky High School, MT", "Desert Vista High School, AZ", "Eastview High School, NM"]
LEGACY_SCHOOL = {"CPP": "Cottonwood Plains Prep", "RBA": "Riverbend Acad", "MVH": "Mesa Vista HS",
                 "SHC": "Sandhill Coll"}
COURSES = {9: ["ENG9", "ALG1", "BIO1", "WHIS", "SPN1", "PE9", "ART1"],
           10: ["ENG10", "GEOM", "CHEM", "USHIS", "SPN2", "HLTH", "MUS1"],
           11: ["ENG11", "ALG2", "PHYS", "CIVX", "ECON", "CS1", "ART2"],
           12: ["ENG12", "PCAL", "ENVS", "GOVT", "PSYC", "FIN1", "CAP"]}


def utc(t):
    """A Mountain-time wall clock to UTC (daylight saving from the second Sunday of March to the first Sunday of
    November)."""
    y = t.year
    mar = dt.date(y, 3, 8) + D(days=(6 - dt.date(y, 3, 8).weekday()) % 7)
    nov = dt.date(y, 11, 1) + D(days=(6 - dt.date(y, 11, 1).weekday()) % 7)
    return t + D(hours=6 if mar <= t.date() < nov else 7)


def wcsv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def day_minutes(school, d):
    """The day's instructional minutes, and the minutes of its parts (the AM and PM sessions, or Mesa Vista's
    periods)."""
    if school == "MVH":
        per = P.MVH_WED if d.weekday() == 2 else P.MVH_STD
        return sum(m for _, m in per), per
    return P.AM_MIN + P.PM_MIN, [("AM", P.AM_MIN), ("PM", P.PM_MIN)]


def mvh_periods(rng, d, por):
    per = P.MVH_WED if d.weekday() == 2 else P.MVH_STD
    names = [n for n, _ in per]
    if por == "FULL":
        return names
    half = len(names) // 2
    if por == "AM":
        return names[:half + (1 if d.weekday() != 2 else 0)]
    return names[half + (1 if d.weekday() != 2 else 0):]


def build(target):
    W = WD.build()
    rng = np.random.default_rng(P.SEED + 7)
    Y, ST, cal = W["years"], W["students"], W["cal"]
    seq = [2104117]
    legacy_id = {}
    lseq = [106402]

    def new_id():
        seq[0] += int(rng.integers(1, 13))
        return "%07d" % seq[0]

    def leg(sid):
        if sid not in legacy_id:
            lseq[0] += int(rng.integers(1, 9))
            legacy_id[sid] = "%06d" % lseq[0]
        return legacy_id[sid]

    enrol, absrows_old, absrows, grades, inc_rows, req_rows = [], [], [], [], [], []
    recmap = {}     # (year, sid) -> [dict(lid, school, start, end_true, end_filed, code, kind)]
    inc_seq = [44120]
    seen = set()
    for label in WD.YEAR_LABELS:
        legacy = label == LEGACY
        first = P.YEARS[WD.YEAR_LABELS.index(label)][1]
        for sid in sorted(Y[label]):
            r = Y[label][sid]
            s = ST[sid]
            recs = []
            for i, (sc, a, b) in enumerate(r["recs"]):
                last_rec = i == len(r["recs"]) - 1
                if last_rec:
                    if r["out"] == "left":
                        kind, end = "left", r["exit_day"]
                    elif r["out"] == "grad":
                        kind, end = "grad", P.YEARS[WD.YEAR_LABELS.index(label)][4]
                    elif r["out"] == "xfer_out":
                        kind, end = "xfer_out", P.YEARS[WD.YEAR_LABELS.index(label)][4]
                    elif r["out"] == "on_roll":
                        kind, end = "open", None
                    else:
                        kind, end = "stay", None
                else:
                    kind = "move" if r["recs"][i + 1][0] != sc else "gap"
                    end = b
                lid = leg(sid) if legacy else new_id()
                # the exit of a move between the network's schools is entered after the new school's entry
                end_filed = end
                if kind == "move":
                    nd = [d for d in cal[(label, sc)] if d > end]
                    end_filed = nd[min(len(nd) - 1, int(rng.integers(2, 7)))]
                code = ""
                if kind == "left":
                    u = rng.random()
                    code = ("W3" if u < 0.74 else "W5" if u < 0.86 else "W9" if u < 0.92 else "WT") if legacy else \
                        ("DO" if u < 0.74 else "GE" if u < 0.86 else "EX" if u < 0.92 else "TU")
                elif kind == "xfer_out":
                    u = rng.random()
                    code = ("W1" if u < 0.45 else "W2" if u < 0.70 else "WT") if legacy else \
                        ("TI" if u < 0.45 else "TO" if u < 0.70 else "TU")
                elif kind == "grad":
                    code = "W0" if legacy else "GR"
                elif kind == "move":
                    code = "W1" if legacy else "TN"
                elif kind == "gap":
                    code = "WT" if legacy else "TU"
                if i == 0:
                    ecode = "C" if (sid in seen and a == first) else ("E1" if sid not in seen else "E2")
                else:
                    ecode = "E3" if kind != "gap" and recs and recs[-1]["kind"] == "move" else "E2"
                if i > 0 and recs[-1]["kind"] == "move":
                    ecode = "E3"
                created = a - D(days=int(rng.integers(0, 4)))
                sasid = sid
                if not legacy and (P.AS_OF - created).days <= 60 and i > 0:
                    sasid = ""
                recs.append(dict(lid=lid, school=sc, start=a, end=end, end_filed=end_filed, code=code, kind=kind,
                                 ecode=ecode, created=created, sasid=sasid))
            seen.add(sid)
            recmap[(label, sid)] = recs
            for rc in recs:
                exit_date = rc["end_filed"] if rc["code"] else None
                enrol.append([label, rc["lid"], rc["sasid"], s.last, s.first, s.dob.isoformat(),
                              P.SCHOOL_NO[rc["school"]], r["grade"], rc["start"].isoformat(), rc["ecode"],
                              exit_date.isoformat() if exit_date else "", rc["code"], rc["created"].isoformat()])
                lag = None
                if rc["kind"] == "xfer_out" and rc["code"] not in ("TU", "WT"):
                    lag = int(rng.integers(1, 31))
                elif rc["code"] in ("TU", "WT") and rc["kind"] != "gap":
                    if rc["kind"] == "xfer_out":
                        lag = int(rng.integers(3, 40)) if rng.random() < 0.85 else int(rng.integers(52, 110))
                    elif rng.random() < 0.12:
                        lag = int(rng.integers(60, 150))
                if lag is not None:
                    nm = s.last.upper() if rng.random() < 0.25 else s.last
                    pool = OTHER_SCHOOLS[:6] if rc["code"] in ("TI", "W1") else (
                        OTHER_SCHOOLS[6:] if rc["code"] in ("TO", "W2") else OTHER_SCHOOLS)
                    req_rows.append([(rc["end_filed"] + D(days=lag)).isoformat(), pool[int(rng.integers(len(pool)))],
                                     nm, s.first, s.dob.strftime("%m/%d/%Y"), P.SCHOOL_NAME[rc["school"]]])

            # absences: the fall and the spring, on the record the day belongs to
            def rec_on(d, sc):
                for rc in recs:
                    if rc["school"] == sc and rc["start"] <= d and (rc["end"] is None or d <= rc["end"]):
                        return rc
                return None
            days = [(d, sc, r["fall_ab"].get(d)) for d, sc in r["fall_days"]]
            days += [(d, sc, r["spring_ab"].get(d)) for d, sc in r.get("spring_days", [])]
            for d, sc, ab in days:
                if ab is None:
                    continue
                rc = rec_on(d, sc)
                if rc is None:
                    continue
                write_absence(rng, legacy, absrows_old, absrows, rc, d, sc, ab[0], ab[1])
            # the old school marks a moved student absent until the exit is entered
            for rc in recs:
                if rc["kind"] == "move":
                    for d in cal[(label, rc["school"])]:
                        if rc["end"] < d <= rc["end_filed"]:
                            write_absence(rng, legacy, absrows_old, absrows, rc, d, rc["school"], "FULL", "UX")
            # a school trip now and then (not an absence)
            if rng.random() < 0.18 and r["fall_days"]:
                d, sc = r["fall_days"][int(rng.integers(len(r["fall_days"])))]
                if d not in r["fall_ab"]:
                    rc = rec_on(d, sc)
                    if rc is not None:
                        write_absence(rng, legacy, absrows_old, absrows, rc, d, sc, "FULL", "ACT")
            # course grades
            for term, nf, ok in (("S1", r["fails"], True), ("S2", r["spring_fails"], label != P.CUR)):
                if not ok:
                    continue
                rc = recs[-1] if term == "S2" or len(recs) == 1 else recs[-1]
                if term == "S2" and r["out"] == "left" and r["exit_day"] and r["exit_day"] <= \
                        P.YEARS[WD.YEAR_LABELS.index(label)][2]:
                    continue
                cs = COURSES[r["grade"]]
                fset = set(rng.choice(len(cs), size=min(nf, len(cs)), replace=False).tolist()) if nf else set()
                for ci, c in enumerate(cs):
                    if ci in fset:
                        g = "F"
                    else:
                        g = ["A", "B", "C", "D"][int(rng.choice(4, p=[0.30, 0.36, 0.24, 0.10]))]
                    cr = 0.5
                    grades.append([label, term, rc["lid"], P.SCHOOL_NO[rc["school"]], c + ("-1" if term == "S1" else "-2"),
                                   g, "%.1f" % cr, "%.1f" % (0.0 if g == "F" else cr)])
            # behaviour incidents, a fall and a spring list; an amended suspension is a new row
            for lst in (r["inc"], r.get("spring_inc", [])):
                for d, cons, n in lst:
                    rc = None
                    for x in recs:
                        if x["start"] <= d and (x["end"] is None or d <= x["end"]):
                            rc = x
                    if rc is None:
                        continue
                    sc = rc["school"]
                    inc_seq[0] += int(rng.integers(1, 4))
                    lag = 0 if cons == "OSS" else int(rng.integers(0, 3))
                    ent = utc(dt.datetime.combine(d + D(days=lag), dt.time(15, int(rng.integers(0, 60)))))
                    beh = ["DISR", "DEFY", "FIGHT", "TOBV", "HARR", "TECH"][int(rng.integers(6))]
                    start = next((x for x in cal[(label, sc)] if x > d), d) if cons == "OSS" else d
                    inc_rows.append(["INC-%s-%05d" % (label[:4], inc_seq[0]), rc["lid"], P.SCHOOL_NO[sc], d.isoformat(),
                                     ent.strftime("%Y-%m-%dT%H:%M:%SZ"), beh, cons, n, start.isoformat()])
                    served = []
                    if cons == "OSS":
                        days_o = [x for x in cal[(label, sc)] if x >= start]
                        nn = n
                        u_appeal = rng.random()
                        if (n > 1 and u_appeal < 0.38) or (n == 1 and u_appeal < 0.14):
                            # the hearing officer reduces it (or lifts it); the behaviour system keeps both rows
                            nn = n - int(rng.integers(1, n)) if n > 1 else 0
                            inc_seq[0] += int(rng.integers(1, 4))
                            # entered the evening of the incident or of a day already served, never after more
                            # days than the amendment leaves
                            j = int(rng.integers(0, min(nn, 2) + 1))
                            hd = d if j == 0 else days_o[j - 1]
                            ent2 = utc(dt.datetime.combine(hd, dt.time(16 + int(rng.integers(0, 3)),
                                                                       int(rng.integers(0, 60)))))
                            beh2 = beh if rng.random() < 0.3 else \
                                [b for b in ["DISR", "DEFY", "FIGHT", "TOBV", "HARR", "TECH"] if b != beh][
                                    int(rng.integers(5))]
                            inc_rows.append(["INC-%s-%05d" % (label[:4], inc_seq[0]), rc["lid"], P.SCHOOL_NO[sc],
                                             d.isoformat(), ent2.strftime("%Y-%m-%dT%H:%M:%SZ"), beh2, cons, nn,
                                             start.isoformat()])
                        served = days_o[:nn]
                        for x in served:
                            if (rc["end"] is None or x <= rc["end"]) and rng.random() < 0.6:
                                write_absence(rng, legacy, absrows_old, absrows, rc, x, sc, "FULL", "SUS")
    W["recmap"] = recmap
    os.makedirs(target, exist_ok=True)
    wcsv(os.path.join(target, "enrollment_records_2023-24_to_2026-27.csv"),
         ["school_year", "local_id", "state_id", "last_name", "first_name", "birth_date", "school_number", "grade",
          "entry_date", "entry_code", "exit_date", "exit_code", "record_created"], enrol)
    absrows_old.sort(key=lambda x: (x[0], dt.datetime.strptime(x[2], "%m/%d/%Y")))
    wcsv(os.path.join(target, "attendance_absences_2023-24.csv"),
         ["Student ID", "School", "Absence Date", "Minutes Absent", "Reason", "Posted By"], absrows_old)
    absrows.sort(key=lambda x: (x[2], x[0]))
    wcsv(os.path.join(target, "attendance_absences_2024-25_to_2026-27.csv"),
         ["local_id", "school_number", "absence_date", "portion", "code", "recorded_utc"], absrows)
    grades.sort(key=lambda x: (x[0], x[1], x[2], x[4]))
    wcsv(os.path.join(target, "course_grades_2023-24_to_2026-27.csv"),
         ["school_year", "term", "local_id", "school_number", "course_section", "grade", "credits_attempted",
          "credits_earned"], grades)
    inc_rows.sort(key=lambda x: (x[3], x[0]))
    wcsv(os.path.join(target, "behavior_incidents_2023-24_to_2026-27.csv"),
         ["incident_id", "local_id", "school_number", "incident_date", "entered_utc", "behavior_code", "action",
          "action_days", "action_start"], inc_rows)
    req_rows.sort()
    wcsv(os.path.join(target, "registrar_records_requests_2023-2026.csv"),
         ["received", "requesting_school", "student_last_name", "student_first_name", "student_dob",
          "school_attended"], req_rows)
    write_calendars(W, os.path.join(target, "instructional_calendars_2023-24_to_2026-27.xlsx"))
    return W


def write_calendars(W, path):
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for label, first, fe, ss, last in P.YEARS:
        ws = wb.create_sheet(label)
        ws.append(["%s school calendar %s, by school (board-approved)" % (P.ORG, label)])
        ws.append(["Instructional days only count toward attendance and enrolled days. Early-release days are full "
                   "instructional days."])
        ws.append(["Date", "Day"] + [P.SCHOOL_NAME[s] for s in P.SCHOOLS])
        for c in ws[3]:
            c.font = Font(bold=True)
        d = first
        while d <= last:
            if d.weekday() < 5:
                ws.append([d, d.strftime("%a")] + [W["kinds"][(label, s)].get(d, "") for s in P.SCHOOLS])
                ws.cell(row=ws.max_row, column=1).number_format = "mm/dd/yyyy"
            d += D(days=1)
        ws.column_dimensions["A"].width = 12
        for col in "CDEF":
            ws.column_dimensions[col].width = 30
        ws.freeze_panes = "C4"
    wb.save(path)


def write_absence(rng, legacy, old, new, rc, d, sc, por, code):
    if legacy:
        total, parts = day_minutes(sc, d)
        if por == "FULL":
            mins = total
        elif sc == "MVH":
            per = dict(P.MVH_WED if d.weekday() == 2 else P.MVH_STD)
            mins = sum(per[p] for p in mvh_periods(rng, d, por))
        else:
            mins = P.AM_MIN if por == "AM" else P.PM_MIN
        reason = {"EX": "Excused", "UX": "Unexcused", "MED": "Medical", "SUS": "Suspension",
                  "ACT": "School activity"}[code]
        who = ["attclerk_%s" % sc.lower(), "teacher_sync", "frontoffice_%s" % sc.lower()][int(rng.integers(3))]
        old.append([rc["lid"], LEGACY_SCHOOL[sc], d.strftime("%m/%d/%Y"), mins, reason, who])
    else:
        if sc == "MVH":
            portion = "PER:" + ",".join(mvh_periods(rng, d, por))
        else:
            portion = por
        t = utc(dt.datetime.combine(d, dt.time(8, 0)) + D(minutes=int(rng.integers(20, 600))))
        new.append([rc["lid"], P.SCHOOL_NO[sc], d.isoformat(), portion, code, t.strftime("%Y-%m-%dT%H:%M:%SZ")])
