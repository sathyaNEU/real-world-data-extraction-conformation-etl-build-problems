"""The pack's data files, written from the truth in world.py: the federal directory, finance and 12-month enrollment
returns, the board's campus code list and credit hour file, the six branch campuses' fall 2026 census enrollment, and
the distractors (appropriations, tuition and graduation rates)."""
import csv
import datetime as dt

import numpy as np

import world as W

FILES = {
    "hd": "ipeds_hd2025_directory_lakemoor_public.csv",
    "f1a": "ipeds_f1a_fy2026_finance_lakemoor_public.csv",
    "e12": "ipeds_e12_2025-26_enrollment_lakemoor_public.csv",
    "codes": "lhecb_campus_codes_2026.csv",
    "ch": "lhecb_credit_hours_by_level_2025-26.csv",
    "census": "lhecb_fall2026_census_enrollment_branch_campuses.csv",
    "guide": "lhecb_instructional_investment_grant_guidelines_2027-28.pdf",
    "approp": "lhecb_fy2026_state_appropriations.xlsx",
    "tuition": "lhecb_2026-27_tuition_and_fees.csv",
    "grad": "ipeds_gr2025_graduation_rates_lakemoor_public.csv",
    "dictionary": "lhecb_data_dictionary.csv",
    "manifest": "lhecb_extract_manifest_2026-10-09.csv",
}
COMPANY = "Lakemoor Higher Education Coordinating Board"

HD_COLS = ["UNITID", "INSTNM", "CITY", "STABBR", "SECTOR", "C21BASIC", "OPENPUBL"]
F1A_COLS = ["UNITID", "PRCH_F", "IDX_F", "F1C011", "F1C021", "F1C031", "F1C051", "F1C061", "F1C071", "F1C191"]
E12_COLS = ["UNITID", "EFYTOTLT", "CDACTUA", "CDACTGA", "FTEUG", "FTEGD"]
CODES_COLS = ["campus_code", "campus_name", "unitid", "system", "code_effective", "note"]
CH_COLS = ["campus_code", "term", "course_level", "discipline_family", "student_credit_hours"]
CENSUS_COLS = ["term", "campus_code", "student_id", "birth_date", "sex", "home_zip", "subject", "course_number",
               "crn", "course_level", "credit_hours", "meeting_days", "start_time", "instructor_id"]
TUITION_COLS = ["unitid", "resident_tuition_fees", "nonresident_tuition_fees", "per_credit_resident"]
GRAD_COLS = ["UNITID", "GRTYPE", "COHORT", "GRAD150", "GRRT150"]
CITY = {"214330": "Ardmore Falls", "214418": "Bexley", "214506": "Carrow", "214594": "Eastmarch", "214682": "Felling",
        "214770": "Greywell", "214858": "Harrowby", "214946": "Inglenook", "215034": "Jessamine", "215122": "Kelderton",
        "215210": "Lowmoor", "215298": "Marchbank", "215386": "Northgale", "215474": "Orrinford", "215562": "Penmark",
        "215650": "Quarrel Hill", "216102": "Lakemoor City", "216190": "Ferris Bend", "216278": "Stoneleigh",
        "216366": "Westford", "216454": "Dunmere", "216542": "Halden", "216630": "Ashby", "216718": "Corley",
        "216806": "Southmoor", "216894": "Pell"}
SYSTEM = {"216102": "University of Lakemoor", "216190": "University of Lakemoor", "216278": "University of Lakemoor",
          "216366": "Western Lakemoor University", "216454": "Western Lakemoor University",
          "216542": "Lakemoor Polytechnic", "216630": "Lakemoor Polytechnic", "216718": "Lakemoor Polytechnic",
          "216806": "Southmoor University", "216894": "Southmoor University"}
CHILDREN = [u for u in W.IDS if W.KIND[u] == "C"]
MOVED = tuple(CHILDREN)              # every branch moved to its parent's student system in August 2026


def write_csv(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(cols)
        for r in rows:
            w.writerow(["" if v is None else v for v in r])
    return len(rows)


def codes(x):
    """The board's campus codes; Kelderton State University was re-coded when it took its present name in 2024."""
    out = {}
    for i, u in enumerate(W.IDS):
        out[u] = "LM%03d" % (101 + 4 * i)
    x["code"] = out
    return out


def hd_rows(x):
    rows = []
    for u in W.IDS:
        basic = {"S": 18, "P": 15, "C": 20}[W.KIND[u]]
        rows.append((u, W.NAME[u], CITY[u], "LM", 1, basic, 1))
    return rows


def f1a_rows(x):
    rng = np.random.default_rng(W.SEED + 1)
    rows = []
    for u in W.IDS:
        k = W.KIND[u]
        inst = x["reported"][u]
        if k == "C":
            rows.append((u, 2, W.PARENT[u], 0, 0, 0, 0, 0, 0, 0))
            continue
        res = round(inst * float(rng.uniform(0.05, 0.35 if k == "P" else 0.12)))
        pub = round(inst * float(rng.uniform(0.02, 0.06)))
        acad = round(inst * float(rng.uniform(0.18, 0.26)))
        stu = round(inst * float(rng.uniform(0.10, 0.16)))
        ins = round(inst * float(rng.uniform(0.16, 0.24)))
        tot = round(inst) + res + pub + acad + stu + ins + round(inst * float(rng.uniform(0.25, 0.4)))
        rows.append((u, 1 if k == "P" else "", "", round(inst), res, pub, acad, stu, ins, tot))
    return rows


def e12_rows(x):
    rows = []
    for u in W.IDS:
        ch = x["ch"][u]
        ug = ch["LD"] + ch["UD"]
        head = round((ug / 24.0 + ch["GR"] / 15.0) * 1.12)
        rows.append((u, head, ug, ch["GR"], round(ug / 30.0), round(ch["GR"] / 24.0)))
    return rows


FAMILIES = ["arts and humanities", "social sciences", "natural sciences and mathematics", "engineering and computing",
            "health professions", "business", "education"]


def ch_rows(x):
    """Credit hours by campus, term, level and discipline family, summing to each campus's year by level."""
    rng = np.random.default_rng(W.SEED + 2)
    rows = []
    lab = {"LD": "Lower division", "UD": "Upper division", "GR": "Graduate"}
    for u in W.IDS:
        for lv in W.LEVELS:
            tot = x["ch"][u][lv]
            terms = [round(tot * W.TERM_SHARE[t]) for t in W.TERMS]
            terms[0] = tot - sum(terms[1:])
            for t, tt in zip(W.TERMS, terms):
                w = rng.dirichlet(np.ones(len(FAMILIES)) * 3)
                parts = [int(round(tt * s)) for s in w]
                parts[0] = tt - sum(parts[1:])
                for fam, v in zip(FAMILIES, parts):
                    if v:
                        rows.append((x["code"][u], t, lab[lv], fam, v))
    return rows


def codes_rows(x):
    rows = []
    for u in W.IDS:
        note = ""
        eff = "2015-07-01"
        if u == "215122":
            note = "formerly Kelderton State College (LM161 until 30 June 2024)"
            eff = "2024-07-01"
        rows.append((x["code"][u], W.NAME[u], u, SYSTEM.get(u, ""), eff, note))
    return rows


SUBJECTS = {"LD": [("ENGL", 1010), ("MATH", 1110), ("HIST", 1020), ("BIOL", 1210), ("PSYC", 1010), ("CHEM", 1110),
                   ("COMM", 1050), ("SOCI", 1010), ("ECON", 2010), ("ART", 1030), ("SPAN", 1010), ("PHIL", 2020)],
            "UD": [("ENGL", 3150), ("BUSN", 3010), ("NURS", 3200), ("PSYC", 3410), ("HIST", 3410), ("BIOL", 3300),
                   ("EDUC", 3050), ("CRIM", 3100)],
            "GR": [("EDUC", 5100), ("BUSN", 6010), ("NURS", 5200)]}
CROSS = {("HIST", 3410): ("WGST", 3410), ("PSYC", 3410): ("SOCI", 3410), ("PHIL", 2020): ("RELS", 2020)}


def census(x):
    """The six branch campuses' fall 2026 census enrollment, one row per student and course: credit hours to match
    each branch's fall 2025 level mix at the 2026 size; a cross-listed course carries each student under both of its
    course numbers; at the branches, moved to their parents' student systems in August 2026, a student's courses
    registered in the spring under the old id stay under it and the courses added after the move sit under the new."""
    rng = np.random.default_rng(W.SEED + 3)
    rows = []
    truth = {}
    sid = 700000
    staff = {}
    for u in CHILDREN:
        code = x["code"][u]
        fall = {lv: x["ch"][u][lv] * W.TERM_SHARE["2025FA"] * float(rng.uniform(1.01, 1.05)) for lv in W.LEVELS}
        ch_tot = {lv: 0 for lv in W.LEVELS}
        students = []
        seen = set()
        while sum(ch_tot.values()) < sum(fall.values()):
            sid += int(rng.integers(1, 9))
            while True:
                bd = dt.date(int(rng.integers(1972, 2009)), int(rng.integers(1, 13)), int(rng.integers(1, 29)))
                sx = "F" if rng.random() < 0.56 else "M"
                z = "%05d" % (67000 + int(rng.integers(0, 900)))
                if (bd, sx, z) not in seen:
                    seen.add((bd, sx, z))
                    break
            grad = rng.random() < fall["GR"] / sum(fall.values()) * 1.6
            n = int(rng.choice([1, 2, 3, 4, 5], p=[0.12, 0.14, 0.2, 0.32, 0.22]))
            courses = []
            for _ in range(n):
                if grad:
                    lv = "GR"
                else:
                    lv = "UD" if rng.random() < fall["UD"] / (fall["LD"] + fall["UD"]) else "LD"
                subj, num = SUBJECTS[lv][int(rng.integers(0, len(SUBJECTS[lv])))]
                if (subj, num, lv) in [(c[0], c[1], c[2]) for c in courses]:
                    continue
                cr = 3
                if subj in ("BIOL", "CHEM") and lv == "LD":
                    cr = 4
                courses.append((subj, num, lv, cr))
                ch_tot[lv] += cr
            students.append((sid, bd, sx, z, courses))
        moved = u in MOVED
        fte = 0.0
        for s, bd, sx, z, courses in students:
            new_id = 1000000 + 100000 * CHILDREN.index(u) + s % 99991
            spring = rng.random() < 0.55
            for j, (subj, num, lv, cr) in enumerate(courses):
                sect = int(rng.integers(1, 4))
                days = ["MWF", "TR", "MW", "TR", "W"][(num + sect) % 5]
                start = ["08:00", "09:30", "11:00", "12:30", "14:00", "17:30"][(num * 7 + sect) % 6]
                inst = staff.setdefault((u, subj, num, sect), "I%05d" % (10417 + 37 * len(staff)))
                crn = "%s%d" % (str(num)[-3:], 10 + sect + 10 * W.IDS.index(u))
                who = s
                if moved and not (spring and j < len(courses) - 1):
                    who = new_id
                base = ("2026FA", code, who, bd.isoformat(), sx, z)
                rows.append(base + (subj, num, crn, lv, cr, days, start, inst))
                if (subj, num) in CROSS:
                    cs, cn = CROSS[(subj, num)]
                    rows.append(base + (cs, cn, "%06d" % (int(crn) + 4300), lv, cr, days, start, inst))
                fte += cr / (12.0 if lv == "GR" else 15.0)
        truth[u] = {"fte": round(fte, 1), "head": len(students)}
    rows.sort(key=lambda r: (r[1], r[2], r[6], r[7]))
    x["census_truth"] = truth
    return rows


def tuition_rows(x):
    rng = np.random.default_rng(W.SEED + 5)
    out = []
    for u in W.IDS:
        r = round(float(rng.uniform(7800, 11900)), -1)
        out.append((u, int(r), int(round(r * float(rng.uniform(2.3, 2.9)), -1)), int(round(r / 30))))
    return out


def grad_rows(x):
    rng = np.random.default_rng(W.SEED + 6)
    out = []
    for u in W.IDS:
        coh = int(x["fte"][u] * float(rng.uniform(0.16, 0.22)))
        rate = float(rng.uniform(0.38, 0.82) if W.KIND[u] != "C" else rng.uniform(0.22, 0.45))
        out.append((u, 2, coh, int(coh * rate), round(100 * rate)))
    return out
