"""The college's exports, written from the clean truth: IR's fall entering-student files, the student system's
admissions and exits, the associate degree conferrals, the 2024 conversion's student-number map, the term calendar,
the fall 2026 census registrations, the program-of-record history, the fall 2026 section schedule, the program
register, IR's course success rates and the workforce office's occupational outlook."""
import csv
import datetime as dt

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

import common as K
import population as PO
import term26 as T26
import world as W

R_SEED = 26613
CONVERTED_ON = dt.date(2024, 7, 13)


def rng_for(*keys):
    return np.random.default_rng([R_SEED] + [int(k) for k in keys])


def _head(ws, header, widths, fill="1F4E79"):
    ws.append(header)
    for c in ws[ws.max_row]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=fill)
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for i, w in enumerate(widths):
        ws.column_dimensions[chr(65 + i) if i < 26 else "A" + chr(65 + i - 26)].width = w
    ws.freeze_panes = "A%d" % (ws.max_row + 1)


def _csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


# ---------------------------------------------------------------------------------------------- IR's entering files
def attributes(T):
    """Age at the fall census, Pell and census credits for each entering student."""
    for i, r in enumerate(T["entering"]):
        rng = rng_for(1, i)
        if r["tr_in"]:
            age = int(rng.choice([19, 20, 21, 22, 23, 24, 26, 28, 31, 35, 41], p=[.08, .16, .16, .13, .1, .08, .08, .07,
                                                                                     .06, .05, .03]))
        elif rng.random() < (.62 if not r["pt"] else .34):
            age = int(rng.choice([17, 18, 19], p=[.04, .78, .18]))
        else:
            age = int(rng.integers(19, 47))
        r["age"] = age
        r["credits"] = int(rng.choice([12, 13, 14, 15, 15, 16, 16, 17])) if not r["pt"] else \
            int(rng.choice([3, 4, 6, 6, 7, 8, 9, 9, 10, 11]))


def write_cohorts(path, T):
    attributes(T)
    wb = Workbook()
    first = True
    n = 0
    for cls in K.CLASSES:
        rows = sorted((r for r in T["entering"] if r["cls"] == cls),
                      key=lambda r: (r["lid"] if cls == 2023 else r["sid"]))
        ws = wb.active if first else wb.create_sheet()
        first = False
        if cls == 2023:
            ws.title = "Fall 2023"
            _head(ws, ["ID", "Term", "Prog", "Camp", "Type", "Load", "Age", "Pell", "Cr"],
                  [10, 8, 10, 6, 6, 6, 6, 6, 5], fill="44546A")
            for r in rows:
                ws.append([int(r["lid"]), "2023FA", K.LEGACY[r["prog"]], K.LEGACY_CAMPUS[r["campus"]],
                           "T" if r["tr_in"] else "F", "P" if r["pt"] else "F", r["age"], "Y" if r["pell"] else None,
                           r["credits"]])
        else:
            ws.title = "Fall %d" % cls
            _head(ws, ["Student ID", "Cohort Term", "Program Code", "Campus", "Entry Type", "Attendance",
                       "Age at Census", "Pell", "Census Credits"], [12, 11, 13, 9, 12, 12, 9, 6, 9])
            for r in rows:
                ws.append([r["sid"], K.fall(cls), K.SIS[r["prog"]], r["campus"],
                           "Transfer" if r["tr_in"] else "First-time", "Part-time" if r["pt"] else "Full-time",
                           r["age"], "Y" if r["pell"] else "N", r["credits"]])
        n += len(rows)
    ws = wb.create_sheet("About these files")
    ws.column_dimensions["A"].width = 112
    for line in [
        "Fall entering-student files, Office of Institutional Research",
        "",
        "Each sheet is the fall entering-student file frozen at that term's census: the degree-seeking students in their",
        "first term at the college, first-time in college or transferring in, in an associate-degree program.",
        "Fall 2023 was frozen in the legacy student system before the 2024 conversion and keeps its student numbers,",
        "program codes and term code (Camp Q, T, H; Type F first-time, T transfer; Load F full-time, P part-time).",
        "Fall 2024 and fall 2025 were frozen in the current student system.",
        "Census credits are the credit hours the student was registered for at the census.",
        "Prepared by %s, Director of Institutional Research. Files frozen %s, %s and %s." % (
            K.PEOPLE["ir"], (K.TERM[K.fall(2023)]["census"] + dt.timedelta(days=9)).strftime("%d %B %Y").lstrip("0"),
            (K.TERM[K.fall(2024)]["census"] + dt.timedelta(days=8)).strftime("%d %B %Y").lstrip("0"),
            (K.TERM[K.fall(2025)]["census"] + dt.timedelta(days=10)).strftime("%d %B %Y").lstrip("0")),
    ]:
        ws.append([line or None])
    ws["A1"].font = Font(bold=True)
    wb.save(path)
    return n


# ---------------------------------------------------------------------------------------------- the student system
def write_admissions(path, T):
    rows = []
    for a in T["adm"]:
        if not ("202410" <= a["admit"] <= K.LAST):
            continue
        prog = K.SIS[a["prog"]] if a["prog"] in K.SIS else a["prog"]
        rows.append([a["sid"], a["admit"], a["type"], prog, a["campus"] if a["campus"] in K.CAMPUS else "QNL",
                     a["exit"] or "", a["reason"] or "",
                     a["recorded"].isoformat() if a.get("recorded") else "",
                     a["changed"].isoformat() if a.get("changed") else ""])
    rows.sort(key=lambda r: (r[1], r[0]))
    return _csv(path, ["student_id", "admit_term", "admit_type", "program_code", "campus", "exit_term", "exit_reason",
                       "exit_recorded_on", "reason_changed_on"], rows)


def conferrals(T):
    out = []
    for a in T["adm"]:
        if a["reason"] == "GR" and not a["cert"] and a["prog"] in K.CODES and a["exit"] >= "202410":
            prog = PO.program_at(a, a["exit"])
            out.append(dict(sid=a["sid"], award=K.AWARD[prog], prog=K.SIS[prog], date=K.TERM[a["exit"]]["confer"],
                            term=a["exit"]))
    out.sort(key=lambda c: (c["date"], c["sid"], c["prog"]))
    return out


def write_conferrals(path, T):
    T["conferrals"] = conferrals(T)
    rows = [[c["sid"], c["award"], c["prog"], c["date"].isoformat(), c["term"]] for c in T["conferrals"]]
    return _csv(path, ["student_id", "award", "program_code", "conferral_date", "term_code"], rows)


def write_idmap(path, T):
    rng = rng_for(3)
    rows = []
    last = {}
    for a in T["adm"]:
        if a["sid"] in T["legacy_of"]:
            t = min(a["exit"] or "202430", "202430") if a["admit"] <= "202430" else "202430"
            last[a["sid"]] = max(last.get(a["sid"], "0"), t)
    leg = {c["code"]: c["legacy"] for c in K.TERMS if c["legacy"]}
    for sid, lid in sorted(T["legacy_of"].items()):
        code = last.get(sid, "202430")
        code = code if code in leg else "202430"
        rows.append((lid, sid, leg[code]))
    early = [c["legacy"] for c in K.TERMS if c["legacy"] and c["code"] <= "202320"]
    for sid, lid in T["converted_only"]:
        rows.append((lid, sid, early[int(rng.integers(len(early)))]))
    rows.sort()
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("LEGACY_ID|NEW_ID|CONVERTED_ON|LAST_LEGACY_TERM\r\n")
        for lid, sid, t in rows:
            fh.write("%s|%s|%s|%s\r\n" % (lid, sid, CONVERTED_ON.strftime("%Y%m%d"), t))
    return len(rows)


def write_terms(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Terms"
    _head(ws, ["Term code", "Legacy term code", "Term", "First day", "Census date", "Last day", "Conferral date"],
          [11, 12, 13, 12, 12, 12, 13])
    n = 0
    for t in K.TERMS:
        if t["code"] < "201910":
            continue
        ws.append([t["code"], t["legacy"] or None, K.term_name(t["code"]), t["start"], t["census"], t["end"],
                   t["confer"]])
        for c in range(4, 8):
            ws.cell(ws.max_row, c).number_format = "yyyy-mm-dd"
        n += 1
    wb.save(path)
    return n


# ---------------------------------------------------------------------------------------------- history and fall 2026
def history(T):
    """The program-of-record rows in effect at any time from fall 2023 to spring 2027."""
    rng = rng_for(4)
    out = []
    reason = {"N": "ADM", "T": "ADM", "R": "RDM", "S": "SEC", "D": "ADM", "V": "ADM"}
    for a in T["adm"]:
        prog0 = K.SIS.get(a["prog"], a["prog"])
        spans = [(a["admit"], prog0, reason[a["type"]])] + [(c, K.SIS.get(p, p), "CHG") for c, p in a["switches"]]
        for k, (eff, prog, why) in enumerate(spans):
            end = K.nth(spans[k + 1][0], -1) if k + 1 < len(spans) else (a["exit"] or "")
            if end and end < "202410":
                continue
            t = K.TERM[eff]
            on = (t["start"] - dt.timedelta(days=int(rng.integers(3, 40)))) if why != "CHG" else \
                (t["census"] - dt.timedelta(days=int(rng.integers(2, 60))))
            out.append(dict(sid=a["sid"], prog=prog, eff=eff, end=end, why=why, on=on))
    out.sort(key=lambda h: (h["sid"], h["eff"], h["prog"]))
    return out


def current_program(H):
    cur = {}
    for h in H:
        cur[h["sid"]] = h["prog"]
    return cur


def write_history(path, T):
    H = history(T)
    T["history"] = H
    rows = [[h["sid"], h["prog"], h["eff"], h["end"], h["why"], h["on"].isoformat()] for h in H]
    return _csv(path, ["student_id", "program_code", "effective_term", "end_term", "change_reason", "entered_on"], rows)


def write_registrations(path, T):
    F = T["fall26"]
    secs = {s["crn"]: s for s in F["sections"]}
    cur = current_program(T["history"])
    rows = []
    for r in F["rows"]:
        s = secs[r["crn"]]
        rows.append([K.FALL26, r["sid"], r["crn"], s["subj"], s["num"], s["sec"], T26.COURSES[s["course"]][1],
                     r["status"], r["date"].isoformat(), s["campus"], cur.get(r["sid"], "")])
    rows.sort(key=lambda x: (x[1], x[2], x[8]))
    return _csv(path, ["term_code", "student_id", "crn", "subject", "course_number", "section", "credit_hours",
                       "reg_status", "status_date", "campus", "program_code"], rows)


def write_schedule(path, T):
    F = T["fall26"]
    exp = {}
    for r in F["rows"]:
        if r["status"] in ("RE", "RW"):
            exp[r["crn"]] = exp.get(r["crn"], 0) + 1
    secs = sorted(F["sections"], key=lambda s: (s["subj"], s["num"], s["sec"] or "", s["crn"]))
    wb = Workbook()
    ws = wb.active
    ws.title = "Fall 2026 sections"
    _head(ws, ["CRN", "Subj", "Crse", "Sec", "Title", "Type", "Link", "Camp", "Room", "Days", "Begin", "End",
               "Instructor", "Cr Hrs", "Max", "Enrl", "Status"],
          [7, 6, 6, 5, 34, 6, 7, 6, 12, 6, 7, 7, 10, 7, 6, 6, 7])
    for s in secs:
        online = s["kind"] == "ONL"
        days = "TBA" if online else s["slot"][0]
        begin = None if online else s["slot"][1]
        end = None if online else s["slot"][2]
        kind = "LEC" if s["kind"] in ("LEC", "ONL") else s["kind"]
        ws.append([int(s["crn"]), s["subj"], s["num"], s["sec"], s["title"], kind, int(s["link"]) if s["link"] else None,
                   s["campus"], s["room"] if s["status"] == "A" else None, days, begin, end,
                   s["inst"] if s["status"] == "A" else None, s["credits"], s["cap"],
                   exp.get(s["crn"], 0) if s["status"] == "A" else 0, s["status"]])
    wb.save(path)
    return len(secs)


# ---------------------------------------------------------------------------------------------- context and distractors
FIRST = {"GS": 1971, "BIO": 1988, "BUS": 1969, "PSY": 1994, "MA": 2003, "ECE": 1991, "CJ": 1977, "HVR": 2009,
         "NUR": 1974}
CREDITS = {"GS": 60, "BIO": 62, "BUS": 61, "PSY": 60, "MA": 64, "ECE": 63, "CJ": 61, "HVR": 66, "NUR": 68}
SUBJECT_NAMES = {"IDS": "Interdisciplinary Studies", "BIO": "Biology", "BUS": "Business", "ACC": "Accounting",
                 "PSY": "Psychology", "MDA": "Medical Assisting", "ECE": "Early Childhood Education",
                 "CRJ": "Criminal Justice", "HVR": "Heating, Ventilation, Air Conditioning and Refrigeration",
                 "NUR": "Nursing", "WLD": "Welding", "CHE": "Chemistry", "PHY": "Physics", "ENG": "English",
                 "MAT": "Mathematics", "HIS": "History", "SOC": "Sociology", "COM": "Communication",
                 "CIS": "Computer Information Systems", "ART": "Art", "PHI": "Philosophy", "ECO": "Economics",
                 "SPA": "Spanish"}


def write_register(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Programs"
    _head(ws, ["Program code", "Legacy code", "Program", "Award", "CIP", "Campuses", "First offered", "Credits"],
          [12, 11, 52, 11, 9, 16, 12, 9])
    camp = {"NUR": "QNL, TRV", "HVR": "QNL, TRV, HOL"}
    for p in K.CODES:
        ws.append([K.SIS[p], K.LEGACY[p], K.NAME[p], {"AA": "AA", "AS": "AS", "AAS": "AAS"}[K.AWARD[p]], K.CIP[p],
                   camp.get(p, "QNL, TRV, HOL"), FIRST[p], CREDITS[p]])
    for code, leg, name, award, cip in K.OTHER:
        ws.append([code, leg, name, award, cip or None, "QNL, TRV, HOL" if code != "CERT.WELD" else "QNL, TRV",
                   {"CERT.PHLB": 2012, "CERT.HVTC": 2010, "CERT.CDAP": 2015, "CERT.WELD": 2018, "CERT.ACCT": 1998,
                    "DE.HSDE": 2006, "ND.NDEG": 1969}[code],
                   {"CERT.PHLB": 16, "CERT.HVTC": 30, "CERT.CDAP": 18, "CERT.WELD": 32, "CERT.ACCT": 30}.get(code)])
    ws2 = wb.create_sheet("Subjects")
    _head(ws2, ["Subject", "Subject name", "Program code"], [9, 52, 18])
    owner = {s: K.SIS[p] for p in K.CODES for s in K.OWNS[p]}
    owner.update({"WLD": "CERT.WELD"})
    for subj in sorted(SUBJECT_NAMES):
        ws2.append([subj, SUBJECT_NAMES[subj], owner.get(subj, "General Education")])
    wb.save(path)
    return len(K.CODES) + len(K.OTHER)


def write_success(path):
    rng = rng_for(7)
    wb = Workbook()
    ws = wb.active
    ws.title = "Success by subject"
    _head(ws, ["Term code", "Subject", "Enrollments", "Successful (A, B, C, P)", "Success rate"], [10, 9, 12, 14, 12])
    base = {s: float(rng.uniform(.58, .84)) for s in sorted(SUBJECT_NAMES)}
    terms = [t["code"] for t in K.TERMS if "202210" <= t["code"] <= "202620" and t["season"] != "SU"]
    n = 0
    for t in terms:
        for s in sorted(SUBJECT_NAMES):
            size = {"ENG": 1700, "MAT": 1400, "PSY": 1500, "BIO": 1350, "IDS": 600, "BUS": 700, "ACC": 380,
                    "NUR": 420, "CRJ": 450, "ECE": 520, "MDA": 330, "HVR": 210, "CHE": 300, "PHY": 90, "WLD": 120,
                    "SOC": 380, "HIS": 300, "COM": 260, "CIS": 330, "ART": 150, "PHI": 110, "ECO": 140, "SPA": 120}[s]
            e = int(size * (1 if t.endswith("10") else .88) * rng.uniform(.9, 1.1))
            k = int(round(e * min(.95, max(.4, base[s] + rng.normal(0, .025)))))
            ws.append([t, s, e, k, k / e])
            ws.cell(ws.max_row, 5).number_format = "0.0%"
            n += 1
    wb.save(path)
    return n


OUTLOOK = [("29-1141", "Registered Nurses", "AAS.NURS", 3480, 3712, 214, 49.10),
           ("31-9092", "Medical Assistants", "AAS.MEDA", 1105, 1268, 162, 19.74),
           ("31-9097", "Phlebotomists", "CERT.PHLB", 296, 327, 41, 20.52),
           ("49-9021", "Heating, Air Conditioning, and Refrigeration Mechanics and Installers", "AAS.HVAC", 642, 701,
            74, 27.86),
           ("25-2011", "Preschool Teachers, Except Special Education", "AAS.ECED", 718, 744, 96, 16.41),
           ("39-9011", "Childcare Workers", "AAS.ECED; CERT.CDAP", 1622, 1580, 268, 14.12),
           ("33-3051", "Police and Sheriff's Patrol Officers", "AAS.CRJU", 865, 872, 61, 33.86),
           ("33-3012", "Correctional Officers and Jailers", "AAS.CRJU", 744, 701, 63, 24.95),
           ("21-1093", "Social and Human Service Assistants", "AA.PSYC", 912, 1003, 118, 18.83),
           ("29-2053", "Psychiatric Technicians", "AA.PSYC", 214, 229, 26, 18.20),
           ("19-4021", "Biological Technicians", "AS.BIOL", 188, 204, 21, 23.37),
           ("43-3031", "Bookkeeping, Accounting, and Auditing Clerks", "AS.BUSA; CERT.ACCT", 1290, 1162, 141, 21.18),
           ("43-1011", "First-Line Supervisors of Office and Administrative Support Workers", "AS.BUSA", 1034, 1027,
            104, 29.60),
           ("51-4121", "Welders, Cutters, Solderers, and Brazers", "CERT.WELD", 571, 598, 66, 23.15),
           ("43-6013", "Medical Secretaries and Administrative Assistants", "AAS.MEDA", 830, 902, 103, 19.02)]


def write_outlook(path):
    rows = []
    for soc, title, progs, e24, e34, openings, wage in OUTLOOK:
        rows.append([soc, title, progs, e24, e34, e34 - e24, "%.1f" % (100 * (e34 - e24) / e24), openings,
                     "%.2f" % wage])
    return _csv(path, ["soc_code", "occupation", "related_programs", "employment_2024", "employment_2034", "change",
                       "percent_change", "annual_openings", "median_hourly_wage_2024"], rows)
