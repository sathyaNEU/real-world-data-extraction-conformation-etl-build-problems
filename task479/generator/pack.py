"""The pack's data files, written from the truth in world.py: Quantilis's spring 2026 item responses in two layouts
across its March 2026 platform release, its spring score report and item bank, the fall and winter score reports, the
temporary id register, the student information system's rosters and its January 2026 id crosswalk, and two
distractors."""
import csv
import datetime as dt

import numpy as np

import world as W

FILES = {
    "resp1": "quantilis_spring2026_item_responses_through_2026-03-27.csv",
    "resp2": "quantilis_spring2026_item_responses_from_2026-03-30.csv",
    "spring": "quantilis_spring2026_score_report.csv",
    "bank": "quantilis_item_bank_2025-26.csv",
    "manual": "quantilis_benchmark_technical_summary_2025-26.pdf",
    "memo": "bellweather_tutoring_designation_2026-27.docx",
    "fall": "quantilis_fall2025_score_report.csv",
    "temp": "quantilis_temporary_id_register_fall2025.csv",
    "winter": "quantilis_winter2026_score_report.csv",
    "roster_f": "bellweather_sis_roster_2025-10-01.csv",
    "roster_s": "bellweather_sis_roster_2026-03-01.csv",
    "xwalk": "bellweather_sis_id_crosswalk_2026-01-05.csv",
    "state": "state_accountability_math_2025_bellweather.csv",
    "attend": "bellweather_chronic_absence_2025-26.csv",
    "dictionary": "bellweather_assessment_data_dictionary.csv",
    "manifest": "bellweather_assessment_extract_manifest_2026-10-02.csv",
}
NETWORK = "Bellweather Academies"
VENDOR = "Quantilis Assessment"
RELEASE = dt.date(2026, 3, 30)

FIRST = ["Aaliyah", "Aiden", "Amara", "Andre", "Ariana", "Ava", "Benjamin", "Brianna", "Caleb", "Camila", "Carlos",
         "Chloe", "Daniel", "Destiny", "Diego", "Elena", "Elijah", "Emily", "Ethan", "Gabriel", "Grace", "Hailey",
         "Isaac", "Isabella", "Jada", "Jayden", "Jordan", "Josiah", "Kayla", "Kevin", "Layla", "Liam", "Lucas",
         "Madison", "Malik", "Maria", "Mateo", "Maya", "Mia", "Nathan", "Nevaeh", "Noah", "Olivia", "Omar", "Priya",
         "Samuel", "Sofia", "Taylor", "Trinity", "Xavier", "Zoe", "Yusuf", "Imani", "Leah", "Ryan", "Jasmine"]
LAST = ["Adams", "Allen", "Bailey", "Baker", "Bell", "Brooks", "Brown", "Campbell", "Carter", "Clark", "Collins",
        "Cruz", "Davis", "Diaz", "Edwards", "Evans", "Flores", "Foster", "Garcia", "Gomez", "Gray", "Green", "Hall",
        "Harris", "Hill", "Hughes", "Jackson", "James", "Johnson", "Jones", "Kelly", "King", "Lee", "Lewis", "Lopez",
        "Martin", "Martinez", "Mitchell", "Moore", "Morgan", "Murphy", "Nelson", "Nguyen", "Ortiz", "Parker", "Patel",
        "Perez", "Phillips", "Price", "Ramirez", "Reed", "Reyes", "Rivera", "Roberts", "Robinson", "Rogers", "Ross",
        "Sanchez", "Scott", "Smith", "Stewart", "Taylor", "Thomas", "Torres", "Turner", "Walker", "Ward", "Washington",
        "Watson", "White", "Williams", "Wilson", "Wright", "Young"]


def write_csv(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(cols)
        for r in rows:
            w.writerow(["" if v is None else v for v in r])
    return len(rows)


def people(x):
    """Names, birth dates, old and new student ids, test dates, the December transfers, the fall restarts."""
    rng = np.random.default_rng(W.SEED + 1)
    seen = set()
    sess = {}
    for cid in W.NAMES:
        for g in W.GRADES:
            sess[(cid, g)] = dt.date(2026, 3, 23) + dt.timedelta(days=int(rng.integers(0, 14)))
            while sess[(cid, g)].weekday() >= 5:
                sess[(cid, g)] += dt.timedelta(days=1)
    for s in x["students"]:
        while True:
            fn, ln = FIRST[int(rng.integers(0, len(FIRST)))], LAST[int(rng.integers(0, len(LAST)))]
            by = 2026 - 6 - s["grade"] - (1 if rng.random() < 0.7 else 0)
            bd = dt.date(by, int(rng.integers(1, 13)), int(rng.integers(1, 29)))
            if (fn, ln, bd) not in seen:
                seen.add((fn, ln, bd))
                break
        s["first"], s["last"], s["dob"] = fn, ln, bd
        s["old_id"] = "BW%07d" % (1100000 + 17 * s["k"] + int(rng.integers(0, 9)))
        s["new_id"] = "S26%06d" % (400000 + 13 * s["k"])
        s["spring_date"] = sess[(s["campus"], s["grade"])]
        s["fall_campus"] = s["campus"]
        s["transfer"] = rng.random() < 0.045               # moved campus in December: missing from the crosswalk
        if s["transfer"]:
            s["fall_campus"] = W.NAMES[(W.NAMES.index(s["campus"]) + int(rng.integers(1, 14))) % 14]
        s["restart"] = rng.random() < 0.07                 # fall session restarted, the makeup under a temporary id
        s["fall_first"] = max(W.LOT, s["fall"] - int(rng.integers(25, 80)))
        s["temp_id"] = "TMP-%05d" % (20000 + 7 * s["k"]) if s["restart"] else None
    x["sess"] = sess


RESP1_COLS = ["StudentID", "FormID", "ItemSeq", "ItemID", "Response", "Scored", "ResponseTimeMs", "SessionDate"]
RESP2_COLS = ["student_id", "form_id", "item_seq", "item_id", "selected_option", "score", "response_time_s",
              "session_date"]


def resp_rows(x, part):
    rng = np.random.default_rng(W.SEED + 2 + part)
    items = {g: [it for it in x["items"] if it["grade"] == g] for g in W.GRADES}
    keys = {it["id"]: "ABCD"[int(rng.integers(0, 4))] for it in x["items"]}
    rows = []
    for s in sorted(x["students"], key=lambda s: (s["spring_date"], s["new_id"])):
        late = s["spring_date"] >= RELEASE
        if (part == 1 and late) or (part == 2 and not late):
            continue
        form = "MATH-G%d-SPR26" % s["grade"]
        for k, it in enumerate(items[s["grade"]]):
            sc = int(s["resp"][k])
            key = keys[it["id"]]
            sel = key if sc else "ABCD"[("ABCD".index(key) + 1 + int(rng.integers(0, 3))) % 4]
            t = float(s["rt"][k])
            if part == 1:
                rows.append((s["new_id"], form, k + 1, it["id"], sel, sc, int(round(t * 1000)), s["spring_date"].isoformat()))
            else:
                rows.append((s["new_id"], form, k + 1, it["id"], sel, sc, "%.1f" % t, s["spring_date"].isoformat()))
    return rows


SPRING_COLS = ["student_id", "campus_id", "grade", "test_date", "scale_score", "performance_level", "items_answered"]


def level(v):
    return "Below Basic" if v < W.BASIC else ("Basic" if v < W.PROFICIENT else ("Proficient" if v < 570 else "Advanced"))


def spring_rows(x):
    return [(s["new_id"], s["campus"], s["grade"], s["spring_date"].isoformat(), s["ss_vendor"], level(s["ss_vendor"]),
             W.N_ITEMS) for s in sorted(x["students"], key=lambda s: s["new_id"])]


BANK_COLS = ["item_id", "form_id", "position", "a", "b", "c", "reporting_category"]


def bank_rows(x):
    cats = ["Number", "Ratio and proportion", "Expressions and equations", "Geometry", "Statistics"]
    return [(it["id"], "MATH-G%d-SPR26" % it["grade"], it["pos"], "%.3f" % it["a"], "%.3f" % it["b"], "%.3f" % it["c"],
             cats[it["pos"] % 5]) for it in x["items"]]


FALL_COLS = ["student_id", "campus_id", "grade", "test_date", "scale_score"]


def fall_rows(x):
    rng = np.random.default_rng(W.SEED + 5)
    rows = []
    for s in x["students"]:
        d = dt.date(2025, 9, 22) + dt.timedelta(days=int(rng.integers(0, 10)))
        while d.weekday() >= 5:
            d += dt.timedelta(days=1)
        if s["restart"]:
            rows.append((s["old_id"], s["fall_campus"], s["grade"], d.isoformat(), s["fall_first"]))
            m = d + dt.timedelta(days=int(rng.integers(3, 12)))
            while m.weekday() >= 5:
                m += dt.timedelta(days=1)
            rows.append((s["temp_id"], s["fall_campus"], s["grade"], m.isoformat(), s["fall"]))
        else:
            rows.append((s["old_id"], s["fall_campus"], s["grade"], d.isoformat(), s["fall"]))
    rows.sort(key=lambda r: (r[3], r[0]))
    return rows


TEMP_COLS = ["temporary_student_id", "last_name", "first_name", "birth_date", "campus_id", "issued_on"]


def temp_rows(x):
    return [(s["temp_id"], s["last"], s["first"], s["dob"].isoformat(), s["fall_campus"], "2025-10-0%d" % (1 + s["k"] % 8))
            for s in x["students"] if s["restart"]]


WINTER_COLS = ["student_id", "campus_id", "grade", "test_date", "scale_score"]


def winter_rows(x):
    rng = np.random.default_rng(W.SEED + 6)
    rows = []
    for s in x["students"]:
        d = dt.date(2026, 1, 20) + dt.timedelta(days=int(rng.integers(0, 10)))
        while d.weekday() >= 5:
            d += dt.timedelta(days=1)
        rows.append((s["new_id"], s["campus"], s["grade"], d.isoformat(), s["winter"]))
    rows.sort(key=lambda r: (r[3], r[0]))
    return rows


ROSTER_COLS = ["student_id", "last_name", "first_name", "birth_date", "campus_id", "grade"]


def roster_rows(x, which):
    if which == "fall":
        return sorted((s["old_id"], s["last"], s["first"], s["dob"].isoformat(), s["fall_campus"], s["grade"])
                      for s in x["students"])
    return sorted((s["new_id"], s["last"], s["first"], s["dob"].isoformat(), s["campus"], s["grade"])
                  for s in x["students"])


XWALK_COLS = ["legacy_student_id", "student_id", "campus_id_at_migration"]


def xwalk_rows(x):
    return sorted((s["old_id"], s["new_id"], s["campus"]) for s in x["students"] if not s["transfer"])


STATE_COLS = ["campus_id", "campus_name", "grade_span", "students_tested", "pct_meets_or_exceeds", "pct_approaching",
              "pct_does_not_meet"]


def state_rows(x):
    rng = np.random.default_rng(W.SEED + 7)
    rows = []
    for cid, name, n, mu, *_ in W.CAMPUSES:
        m = 100 / (1 + np.exp(-(mu + 0.1) * 2.2)) * float(rng.uniform(0.85, 1.05))
        a = float(rng.uniform(22, 32))
        rows.append((cid, name, "6-8", int(n * 3 * float(rng.uniform(0.92, 1.0))), "%.1f" % m, "%.1f" % a,
                     "%.1f" % (100 - m - a)))
    return rows


ATTEND_COLS = ["campus_id", "month", "enrolled", "chronically_absent", "chronic_absence_pct"]


def attend_rows(x):
    rng = np.random.default_rng(W.SEED + 8)
    rows = []
    for cid, name, n, *_ in W.CAMPUSES:
        base = float(rng.uniform(0.12, 0.28))
        for mo in ("2025-10", "2025-12", "2026-02", "2026-04"):
            e = int(n * 3 * float(rng.uniform(0.97, 1.02)))
            ca = int(e * base * float(rng.uniform(0.9, 1.15)))
            rows.append((cid, mo, e, ca, "%.1f" % (100 * ca / e)))
    return rows
