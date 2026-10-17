"""Write the pack's data files: the two vendors' student results, the retiring test's test-taker crosswalk, the bridge
study's paired scores, the October 2026 enrolment spells, the nonpublic schools registry and the two neighbouring
state files (district spending and graduation rates)."""
import csv
import datetime as dt

import numpy as np

import sim as S
import world as W


def write_csv(path, header, rows, lineterminator="\r\n"):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator=lineterminator)
        wr.writerow(header)
        for r in rows:
            wr.writerow(r)
    return len(rows)


def _rng(*key):
    return np.random.default_rng([S.SEED, 60] + [int(k) for k in key])


HOLIDAYS = {dt.date(2026, 5, 25)}  # Memorial Day: no school


def _school_days(first, last):
    """The school days from first to last."""
    out, d = [], first
    while d <= last:
        if d.weekday() < 5 and d not in HOLIDAYS:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def _shift(d, k):
    """The school day k school days after d (before it when k is negative)."""
    step = 1 if k > 0 else -1
    for _ in range(abs(k)):
        d += dt.timedelta(days=step)
        while d.weekday() >= 5 or d in HOLIDAYS:
            d += dt.timedelta(days=step)
    return d


# each year's testing window (its last two school days left for classes tested after the school's day) and make-ups
WINDOW = {2025: (dt.date(2025, 4, 7), dt.date(2025, 4, 23)), 2026: (dt.date(2026, 4, 13), dt.date(2026, 5, 13))}
MAKEUP = {2025: (dt.date(2025, 5, 5), dt.date(2025, 5, 16)), 2026: (dt.date(2026, 5, 18), dt.date(2026, 5, 29))}


def _school_day(school, year):
    """The day a school sat a test: one of the window's school days."""
    days = _school_days(*WINDOW[year])
    return days[int(_rng(int(school), year).integers(0, len(days)))]


def _student_day(base, sid, salt):
    """A student's own sitting: the school's day or one of the next two school days (a class tested later)."""
    rng = _rng(int(sid[-6:]), salt)
    return _shift(base, int(rng.choice([0, 0, 0, 1, 1, 2])))


def _makeup_day(sid, year):
    days = _school_days(*MAKEUP[year])
    return days[int(_rng(int(sid[-6:]), year, 7).integers(0, len(days)))]


def raw_of(scale, grade):
    """The raw score a retiring-test scale score comes from (the lowest raw score at the floor, the highest at the
    ceiling)."""
    t = W.glra_table(grade)
    if scale == W.OLD["lo"]:
        return max(r for r, s in enumerate(t) if s == scale and r <= 1) if t[1] == scale else 0
    if scale == W.OLD["hi"]:
        return max(r for r, s in enumerate(t) if s == scale)
    return t.index(scale)


def old_level(score, grade):
    return W.OLD_LEVELS[S_level(score, W.OLD_CUTS[grade])]


def S_level(score, cuts):
    k = 0
    for c in cuts:
        if score >= c:
            k += 1
    return k


def _school_of(s, r):
    """The school a record was sat in."""
    if s.get("nonpublic"):
        return s["school"]
    if "school8" in s:
        return s["school8"]
    if r["year"] == 2025 and "school6" in s:
        return s["school6"]
    return s["school"]


def _people(x):
    return x["students"] + x["younger"] + x["np_only"]


# ---------------------------------------------------------------- the retiring test's 2025 student file
GLRA_COLS = ["TEST_TAKER_ID", "STATE_STUDENT_ID", "DISTRICT_CODE", "SCHOOL_CODE", "GRADE", "FORM", "SESSION",
             "TEST_DATE", "SCORE_STATUS", "RAW_SCORE", "SCALE_SCORE", "PERF_LEVEL"]
GLRA_STATUS = {"scored": "SCR", "absent": "ABS", "exempt": "EXM", "invalid": "INV"}


def glra_records(x):
    """(person, record, school, district code on the file) for every 2025 retiring-test record."""
    out = []
    for s in _people(x):
        for r in s["records"]:
            if r["test"] == "old":
                out.append((s, r, _school_of(s, r), s["tested_in"]))
    return out


def glra_rows(x):
    rows = []
    for s, r, school, dist in glra_records(x):
        g = r["grade"]
        day = _student_day(_school_day(school, 2025), s["sid"], g)
        sid = s["sid"] if r["sid_on_file"] else ""
        form = "G%d-25A" % g
        if r["status"] == "scored":
            rows.append([r["tt"], sid, dist, school, g, form, "Regular", day.isoformat(), "SCR", raw_of(r["score"], g),
                         r["score"], old_level(r["score"], g)])
        else:
            rows.append([r["tt"], sid, dist, school, g, form, "Regular", day.isoformat(), GLRA_STATUS[r["status"]],
                         "", "", ""])
            if r["status"] == "invalid" and r["retake"]:
                sc = r["retake_score"]
                rows.append([r["tt"], sid, dist, school, g, form, "Make-up", _makeup_day(s["sid"], 2025).isoformat(),
                             "SCR", raw_of(sc, g), sc, old_level(sc, g)])
    rows.sort(key=lambda t: (t[2], t[3], t[4], t[0], t[6] != "Regular"))
    return rows


# ---------------------------------------------------------------- the crosswalk of test-taker numbers
XWALK_COLS = ["TEST_TAKER_ID", "STATE_STUDENT_ID", "MATCH_METHOD", "MATCH_DATE"]


def xwalk_rows(x):
    rows = []
    for s, r, school, dist in glra_records(x):
        u = _rng(int(r["tt"][-7:]), 9).random()
        if r["sid_on_file"]:
            method, day = "Pre-ID label", dt.date(2025, 5, 30)
        else:
            method = "Demographic match" if u < 0.86 else "Manual review"
            day = dt.date(2025, 6, 9) + dt.timedelta(days=int(u * 20))
        rows.append([r["tt"], s["sid"], method, day.isoformat()])
    rows.sort(key=lambda t: t[0])
    return rows


# ---------------------------------------------------------------- the new test's 2026 student file
SLM_COLS = ["state_student_id", "district_code", "school_code", "grade", "session", "test_date", "status",
            "scale_score", "performance_level"]
SLM_STATUS = {"scored": "Scored", "absent": "Absent", "exempt": "Exempt", "invalid": "Invalidated"}


def slm_records(x):
    out = []
    for s in _people(x):
        for r in s["records"]:
            if r["test"] == "new":
                out.append((s, r, _school_of(s, r), s["tested_in"]))
    return out


def june_level(score, grade):
    return 1 + S_level(score, W.NEW_CUTS_JUNE[grade])


def slm_rows(x):
    rows = []
    for s, r, school, dist in slm_records(x):
        g = r["grade"]
        day = _student_day(_school_day(school, 2026), s["sid"], g)
        if r["status"] == "scored":
            rows.append([s["sid"], dist, school, g, "Main", day.isoformat(), "Scored", r["score"],
                         june_level(r["score"], g)])
        else:
            rows.append([s["sid"], dist, school, g, "Main", day.isoformat(), SLM_STATUS[r["status"]], "", ""])
            if r["status"] == "invalid" and r["retake"]:
                sc = r["retake_score"]
                rows.append([s["sid"], dist, school, g, "Make-up", _makeup_day(s["sid"], 2026).isoformat(), "Scored",
                             sc, june_level(sc, g)])
    rows.sort(key=lambda t: (t[1], t[2], t[3], t[0], t[4] != "Main"))
    return rows


# ---------------------------------------------------------------- the bridge study
BRIDGE_COLS = ["state_student_id", "district_code", "school_code", "order_of_tests", "glra_test_date", "glra_raw_score",
               "glra_scale_score", "slm_scale_score"]


def bridge_rows(x):
    rows = []
    for r in x["bridge"]["rows"]:
        s = r["student"]
        slm_day = _student_day(_school_day(r["school"], 2026), s["sid"], 8)
        d = _shift(slm_day, -2 if r["order"] == "GLRA" else 3)
        rows.append([s["sid"], s["tested_in"], r["school"], "GLRA first" if r["order"] == "GLRA" else "SLM first",
                     d.isoformat(), raw_of(r["old"], 8), r["old"], r["new"]])
    rows.sort(key=lambda t: (t[2], t[0]))
    return rows


# ---------------------------------------------------------------- the October 2026 enrolment spells
ENROL_COLS = ["district_code", "school_code", "state_student_id", "grade", "entry_date", "exit_date", "exit_reason"]


def enrol_rows(x):
    rows = []
    others = ("Moved out of state", "Moved out of state", "Withdrew", "Transferred to a nonpublic school",
              "Home instruction")
    for sp in x["spells"]:
        reason = ""
        if sp["exit"]:
            if sp["who"].get("transfer_from") == sp["district"] or sp.get("moved_to"):
                reason = "Transferred within state"
            else:
                reason = others[int(sp["sid"][-3:]) % len(others)]
        rows.append([sp["district"], sp["school"], sp["sid"], sp["grade"], sp["entry"], sp["exit"], reason])
    rows.sort(key=lambda t: (t[0], t[1], t[3], t[2], t[4]))
    return rows


# ---------------------------------------------------------------- the nonpublic schools registry
NONPUBLIC_COLS = ["school_code", "school_name", "county", "located_in_district", "grades_served", "affiliation",
                  "state_test_participation"]
AFFILIATION = {"Catholic": "Roman Catholic", "Parish": "Roman Catholic", "Hebrew": "Jewish", "Christian": "Christian",
               "Friends": "Religious Society of Friends", "Lutheran": "Lutheran", "Mennonite": "Mennonite",
               "Adventist": "Seventh-day Adventist", "Baptist": "Baptist", "Montessori": "Independent",
               "Country Day": "Independent", "Academy": "Independent"}


def nonpublic_rows():
    county = {c: cty for c, n, cty, *_ in W.DISTRICTS}
    county.update({"1701": county["1700"], "1702": county["1700"]})
    rows = []
    for code, name, where, per, mu in W.NONPUBLIC:
        aff = next(v for k, v in AFFILIATION.items() if k in name)
        rows.append([code, name, county[where] + " County", where, "K-8" if per < 30 else "PK-8", aff, "Yes"])
    for code, name, where, grades, aff in W.NONPUBLIC_OTHER:
        rows.append([code, name, county[where] + " County", where, grades, aff, "No"])
    return sorted(rows)


# ---------------------------------------------------------------- the two neighbouring state files (distractors)
FIN_COLS = ["district_code", "district_name", "fiscal_year", "fall_2024_enrollment", "current_expenditure",
            "expenditure_per_pupil"]


def _before_merger():
    """The districts as they stood before July 1, 2026: the consolidated district's two predecessors in its place."""
    out = []
    for code, name, cty, n10, n9, mu10, mu9 in W.DISTRICTS:
        if code in W.MERGER:
            for sub, sname, share in W.MERGER[code]:
                out.append((sub, sname, n10 * share, n9 * share, mu10, mu9))
        else:
            out.append((code, name, n10, n9, mu10, mu9))
    return out


def finance_rows(x):
    rows = []
    for code, name, n10, n9, mu10, mu9 in _before_merger():
        rng = _rng(int(code), 81)
        enrol = int(round((n10 + n9) / 2 * 13.1 * rng.uniform(0.97, 1.03)))
        pp = 14200 + 2600 * rng.normal() - 900 * (mu9 + mu10)
        rows.append([code, name, "FY2025", enrol, int(round(enrol * pp + rng.integers(0, 1000))), int(round(pp))])
    return rows


GRAD_COLS = ["district_code", "district_name", "class_of", "cohort_size", "graduates_four_year", "graduation_rate"]


def grad_rows(x):
    rows = []
    for code, name, n10, n9, mu10, mu9 in _before_merger():
        rng = _rng(int(code), 82)
        base = 0.86 + 0.06 * (mu10 + mu9) / 2
        for year in (2024, 2025):
            size = int(round(n10 * rng.uniform(0.95, 1.08)))
            rate = min(0.97, base + rng.normal(0, 0.02))
            grads = int(round(size * rate))
            rows.append([code, name, year, size, grads, "%.1f" % (100.0 * grads / size)])
    return rows
