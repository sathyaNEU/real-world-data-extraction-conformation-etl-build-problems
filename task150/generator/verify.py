"""Independent verifier for task150: reads only the shipped bundle (target/), the goldens and figures.json, on its own
code path (pandas frames, no generator module), and recomputes the placement schedule, the classroom needs, the
default path's schedule, the back-test figures the write-up states, and both asks."""
from __future__ import annotations

import json
import math
import os
import re
import sys

import numpy as np
import openpyxl
import pandas as pd

OCT1 = pd.Timestamp("2026-10-01")


def frames(target):
    codes = pd.read_csv(os.path.join(target, "school_codes.csv"), dtype=str)
    leg = pd.read_csv(os.path.join(target, "membership_oct2013-oct2018.txt"), sep="|", dtype=str, keep_default_na=False)
    cur = pd.read_csv(os.path.join(target, "october_membership_2019-2026.csv"), dtype=str, keep_default_na=False)
    xw = pd.read_csv(os.path.join(target, "student_number_crosswalk_2019.csv"), dtype=str)
    leg = leg.merge(xw[["STU_NBR", "STATE_ID"]], on="STU_NBR", how="left")
    leg["pupil"] = np.where(leg.STATE_ID.notna(), leg.STATE_ID, "L" + leg.STU_NBR)
    leg["school"] = leg.SCH_CD.map(dict(zip(codes.legacy_school_code, codes.state_school_code)))
    leg["grade"] = leg.GRADE.replace({"KG": "00"}).astype(int)
    leg["year"] = leg.SCHL_YR.str[:4].astype(int)
    cur["pupil"] = cur.student_id
    cur["school"] = cur.school_code
    cur["grade"] = cur.grade_level.astype(int)
    cur["year"] = cur.school_year.str[:4].astype(int)
    roll = pd.concat([leg[["year", "pupil", "school", "grade"]], cur[["year", "pupil", "school", "grade"]]],
                     ignore_index=True)
    b = pd.read_csv(os.path.join(target, "brandt_county_births_by_attendance_area_2008-2025.csv"))
    area = dict(zip(codes.attendance_area, codes.state_school_code))
    b = b[b.attendance_area.isin(area)].copy()
    b["school"] = b.attendance_area.map(area)
    births = b.pivot(index="school", columns="birth_year", values="births")
    ws = openpyxl.load_workbook(os.path.join(target, "facilities_capacity_report_2026-09.xlsx"), data_only=True).active
    rows = list(ws.iter_rows(values_only=True))
    h = next(k for k, r in enumerate(rows) if r and "Rated capacity (K-5)" in r)
    hdr = rows[h]
    cap = {}
    for r in rows[h + 1:]:
        if not r or r[0] is None:
            break
        cap[str(r[hdr.index("State code")])] = float(r[hdr.index("Rated capacity (K-5)")])
    schools = list(codes.state_school_code)
    return roll, births, pd.Series(cap)[schools], schools, codes


def transitions(roll):
    """One row per pupil in K-4 on an October roll, with where he is on the next one (or nowhere)."""
    out = []
    years = sorted(roll.year.unique())
    for y in years[1:]:
        a = roll[(roll.year == y - 1) & (roll.grade <= 4)]
        nxt = roll[roll.year == y][["pupil", "school", "grade"]].rename(columns={"school": "s2", "grade": "g2"})
        m = a.merge(nxt, on="pupil", how="left")
        m["to"] = y
        out.append(m)
    return pd.concat(out, ignore_index=True)


def new_pupils(roll):
    out = []
    years = sorted(roll.year.unique())
    for y in years[1:]:
        prev = set(roll.loc[roll.year == y - 1, "pupil"])
        now = roll[roll.year == y]
        out.append(now[~now.pupil.isin(prev)])
    return pd.concat(out, ignore_index=True)


def gross(roll, births, schools, years, bavg=(2023, 2024, 2025)):
    T = transitions(roll)
    T = T[T.to.isin(years)]
    N = new_pupils(roll)
    N = N[N.year.isin(years)]
    S = len(schools)
    si = {s: k for k, s in enumerate(schools)}
    base = T.groupby("school").size().reindex(schools).values.astype(float)
    exits = T[T.s2.isna()].groupby("school").size().reindex(schools, fill_value=0).values
    mv = np.zeros((S, S))
    for (s, s2), n in T[T.s2.notna() & (T.s2 != T.school)].groupby(["school", "s2"]).size().items():
        mv[si[s], si[s2]] = n
    rep = T[(T.s2 == T.school) & (T.g2 == T.grade)].groupby(["school", "grade"]).size()
    at_risk = T.groupby(["school", "grade"]).size()
    ret = np.zeros((S, 6))
    for (s, gr), n in rep.items():
        ret[si[s], gr] = n / at_risk[(s, gr)]
    arr = np.zeros((S, 6))
    for (s, gr), n in N[N.grade >= 1].groupby(["school", "grade"]).size().items():
        arr[si[s], gr] = n / len(years)
    kent = N[N.grade == 0].groupby("school").size().reindex(schools, fill_value=0)
    kr = np.array([kent[s] / sum(births.loc[s, y - 5] for y in years) for s in schools])
    outr = exits / base
    mvr = mv / base[:, None]
    E26 = np.zeros((S, 6))
    for (s, gr), n in roll[roll.year == 2026].groupby(["school", "grade"]).size().items():
        E26[si[s], gr] = n
    cur = E26
    tot = {}
    for y in range(2027, 2033):
        nxt = np.zeros((S, 6))
        for k, s in enumerate(schools):
            bb = births.loc[s, y - 5] if y - 5 <= 2025 else np.mean([births.loc[s, t] for t in bavg])
            nxt[k, 0] = kr[k] * bb
        for k in range(S):
            for gr in range(5):
                n = cur[k, gr]
                nxt[k, gr] += n * ret[k, gr]
                nxt[k, gr + 1] += n * (1 - outr[k] - mvr[k].sum() - ret[k, gr])
                nxt[:, gr + 1] += n * mvr[k]
        nxt[:, 1:] += arr[:, 1:]
        tot[y] = nxt.sum(axis=1)
        cur = nxt
    return np.mean([tot[y] for y in range(2028, 2033)], axis=0)


def gpr(roll, births, schools, win):
    S = len(schools)
    si = {s: k for k, s in enumerate(schools)}
    cnt = roll.groupby(["year", "school", "grade"]).size()

    def c(y, s, gr):
        return cnt.get((y, s, gr), 0)

    ratio = np.array([[0.0] + [sum(c(y, s, gr) for y in win) / sum(c(y - 1, s, gr - 1) for y in win)
                               for gr in range(1, 6)] for s in schools])
    kr = np.array([sum(c(y, s, 0) for y in win) / sum(births.loc[s, y - 5] for y in win) for s in schools])
    cur = np.array([[c(2026, s, gr) for gr in range(6)] for s in schools], dtype=float)
    tot = {}
    for y in range(2027, 2033):
        nxt = np.zeros((S, 6))
        for k, s in enumerate(schools):
            bb = births.loc[s, y - 5] if y - 5 <= 2025 else np.mean([births.loc[s, t] for t in (2023, 2024, 2025)])
            nxt[k, 0] = kr[k] * bb
            nxt[k, 1:] = cur[k, :5] * ratio[k, 1:]
        tot[y] = nxt.sum(axis=1)
        cur = nxt
    return np.mean([tot[y] for y in range(2028, 2033)], axis=0)


def place(avg, cap, oct26):
    exc = avg - cap.values
    need = np.array([math.ceil(e / 24) if e > 0 else 0 for e in exc])
    left = 24
    out = np.zeros(len(exc), int)
    for k in sorted([k for k in range(len(exc)) if exc[k] > 0], key=lambda k: (-exc[k], -oct26[k])):
        out[k] = min(need[k], 8, left)
        left -= out[k]
    return need, out, exc


def ask_a(target):
    sec = pd.read_csv(os.path.join(target, "sections_fall2026.csv"), dtype=str, keep_default_na=False)
    lin = pd.read_csv(os.path.join(target, "section_enrollment_fall2026.csv"), dtype=str, keep_default_na=False)
    lin["s"] = pd.to_datetime(lin.start_date)
    lin["e"] = pd.to_datetime(lin.end_date.replace("", "2099-01-01"))
    open_ids = set(lin[(lin.s <= OCT1) & (lin.e >= OCT1)].section_id)
    hr = sec[sec.course_code.str.startswith("HR-")].copy()
    hr = hr[(pd.to_datetime(hr.section_start) <= OCT1) & (pd.to_datetime(hr.section_end) >= OCT1) &
            hr.section_id.isin(open_ids)]
    hr["band"] = np.where(hr.course_code.isin(["HR-K", "HR-1", "HR-2"]), "K-2", "3-5")
    return hr.drop_duplicates(["school_code", "band", "room", "session"]).groupby(["school_name", "band"]).size()


def ask_b(target):
    p = pd.read_csv(os.path.join(target, "preschool_enrollments_2026-27.csv"), dtype=str, keep_default_na=False)
    p = p[(pd.to_datetime(p.enroll_start) <= OCT1) &
          (pd.to_datetime(p.enroll_end.replace("", "2099-01-01")) >= OCT1)].copy()
    p["room"] = p.class_name.str.extract(r"^(Rm \d+)")[0]
    ws = openpyxl.load_workbook(os.path.join(target, "ecse_roster_2026-10-01.xlsx"), data_only=True).active
    rows = list(ws.iter_rows(values_only=True))
    h = next(k for k, r in enumerate(rows) if r and r[0] == "State ID")
    r = pd.DataFrame([x for x in rows[h + 1:] if x[0] is not None], columns=rows[h])
    r = r[r["Service model"].isin(["ECSE classroom", "Inclusive classroom"])]
    kids = pd.concat([p[["site", "state_id"]], r.rename(columns={"Case school": "site", "State ID": "state_id"})[
        ["site", "state_id"]].astype(str)]).drop_duplicates()
    rooms = pd.concat([p[["site", "room"]], r.rename(columns={"Case school": "site", "Classroom": "room"})[
        ["site", "room"]]]).drop_duplicates()
    return kids.groupby("site").size(), rooms.groupby("site").size()


def main(target, golden, figures_path):
    figs = json.load(open(figures_path, encoding="utf-8"))
    roll, births, cap, schools, codes = frames(target)
    short = dict(zip(codes.state_school_code, codes.school_name.str.replace(" Elementary", "")))
    oct26 = roll[roll.year == 2026].groupby("school").size().reindex(schools).values
    fails = []
    allw = list(range(2014, 2027))
    need, out, exc = place(gross(roll, births, schools, allw), cap, oct26)
    for k, s in enumerate(schools):
        if str(out[k]) != figs["call"][short[s]]:
            fails.append(("placed", short[s], out[k], figs["call"][short[s]]))
        if str(need[k]) != figs["critical_components"]["classroom_need"][short[s]]:
            fails.append(("need", short[s], need[k]))
        if "{:,}".format(int(round(exc[k]))) != figs["steps"]["excess"][short[s]]:
            fails.append(("excess", short[s], exc[k], figs["steps"]["excess"][short[s]]))
    for win in (list(range(2022, 2027)), list(range(2019, 2027)), list(range(2024, 2027))):
        n2, o2, _ = place(gross(roll, births, schools, win), cap, oct26)
        if list(o2) != list(out) or list(n2) != list(need):
            fails.append(("construction", win[0], list(o2)))
    dn, do, _ = place(gpr(roll, births, schools, list(range(2022, 2027))), cap, oct26)
    for k, s in enumerate(schools):
        if str(do[k]) != figs["default_path"]["placement"][short[s]]:
            fails.append(("default", short[s], do[k]))
    if list(do) == list(out):
        fails.append(("default equals golden",))
    A = ask_a(target)
    for r in figs["ask_a_homeroom_classes"]:
        if str(A.get((r["school"], "K-2"), 0)) != r["k2"] or str(A.get((r["school"], "3-5"), 0)) != r["g35"]:
            fails.append(("ask A", r["school"], A.get((r["school"], "K-2")), A.get((r["school"], "3-5"))))
    kids, rooms = ask_b(target)
    for r in figs["ask_b_preschool"]:
        if str(kids[r["site"]]) != r["children"] or str(rooms[r["site"]]) != r["classrooms"]:
            fails.append(("ask B", r["site"], kids[r["site"]], rooms[r["site"]]))
    wb = openpyxl.load_workbook(os.path.join(golden, "classroom_placement_2028-33.xlsx"), data_only=True)
    for row in wb["Placement"].iter_rows(min_row=5, values_only=True):
        if row[1] in schools:
            k = schools.index(row[1])
            if int(row[6]) != need[k] or int(row[8]) != out[k]:
                fails.append(("workbook", row[1], row[6], row[8]))
    sub = open(os.path.join(os.path.dirname(golden), "submission.md"), encoding="utf-8").read()
    for k, s in enumerate(schools):
        nm = codes.school_name[k]
        if not re.search(r"%s: need %d, placed %d" % (re.escape(nm), need[k], out[k]), sub):
            fails.append(("submission", nm))
    if fails:
        for f in fails:
            print("VERIFY FAIL", f)
        raise SystemExit(1)
    print("verify.py: placement %s, needs %s, default %s, Ask A %d figures, Ask B %d figures: all recomputed from the "
          "bundle" % (dict(zip([short[s] for s in schools], out.tolist())), need.tolist(), do.tolist(),
                      2 * len(figs["ask_a_homeroom_classes"]), 2 * len(figs["ask_b_preschool"])))


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                            "target")
    root = os.path.dirname(t)
    main(t, os.path.join(root, "golden"), os.path.join(root, "generator", "figures.json"))
