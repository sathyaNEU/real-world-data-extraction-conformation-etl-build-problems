"""The main call's records as the district's systems write them: the legacy student system's October rolls (2013 to
2018, pipe-delimited, local numbers and codes), the current system's October membership snapshots (2019 to 2026, state
IDs and codes), IT's 2019 conversion crosswalk, the school code list and the county's births by attendance area."""
from __future__ import annotations

import datetime as dt
import os

import numpy as np

import common as K
import world as WD

F_LEGACY = "membership_oct2013-oct2018.txt"
F_MEMBERS = "october_membership_2019-2026.csv"
F_XWALK = "student_number_crosswalk_2019.csv"
F_CODES = "school_codes.csv"
F_BIRTHS = "brandt_county_births_by_attendance_area_2008-2025.csv"

OLD_GRADE = {0: "KG", 1: "01", 2: "02", 3: "03", 4: "04", 5: "05"}
NEW_GRADE = {0: "00", 1: "01", 2: "02", 3: "03", 4: "04", 5: "05"}


def school_name(z, y):
    if z == "D" and dt.date(y, 10, 1) < K.KESSLER_RENAMED:
        return "Southeast Elementary"
    return K.SCHOOLS[z]["name"]


def legacy_rows(W):
    rows = []
    for y in K.OLD_YEARS:
        cd = K.COUNT_DAY[y]
        recs = []
        for (pid, s, g) in W.snap[y]:
            z = WD.Z[s]
            info = W.info[pid]
            ed, code, old = W.spell[(pid, y)]
            sasid = "" if (pid, y) in W.sid_blank else info["sid"]
            sex = info["sex"] if info["sex"] != "X" else "M"
            recs.append([K.SCHOOLS[z]["local"], OLD_GRADE[g], W.local[pid], [
                "%d-%d" % (y, y + 1), K.us(cd), K.SCHOOLS[z]["local"], K.SCHOOLS[z]["old_name"], W.local[pid], sasid,
                OLD_GRADE[g], K.us(info["birth"]), sex, K.us(ed), old,
                "Y" if WD.ell_on(W, pid, y) else "N", "Y" if WD.iep_on(W, pid, y) else "N"]])
        recs.sort(key=lambda t: (t[0], t[1], t[2]))
        rows.extend(r[3] for r in recs)
    return rows


def member_rows(W):
    rows = []
    for y in K.NEW_YEARS:
        cd = K.COUNT_DAY[y]
        recs = []
        for (pid, s, g) in W.snap[y]:
            z = WD.Z[s]
            info = W.info[pid]
            ed, code, old = W.spell[(pid, y)]
            recs.append([K.SCHOOLS[z]["state"], NEW_GRADE[g], info["sid"], [
                K.school_year(y), K.iso(cd), K.SCHOOLS[z]["state"], school_name(z, y), info["sid"], NEW_GRADE[g],
                K.iso(info["birth"]), info["sex"], K.iso(ed), code,
                "Y" if WD.ell_on(W, pid, y) else "N", "Y" if WD.iep_on(W, pid, y) else "N"]])
        recs.sort(key=lambda t: (t[0], t[1], t[2]))
        rows.extend(r[3] for r in recs)
    return rows


def write_legacy(W, out):
    hdr = ["SCHL_YR", "CNT_DT", "SCH_CD", "SCH_NAME", "STU_NBR", "SASID", "GRADE", "BIRTH_DT", "SEX", "ENTRY_DT",
           "ENTRY_CD", "ELL", "SPED"]
    return K.write_csv(os.path.join(out, F_LEGACY), hdr, legacy_rows(W), delimiter="|")


def write_members(W, out):
    hdr = ["school_year", "count_date", "school_code", "school_name", "student_id", "grade_level", "birth_date",
           "gender", "entry_date", "entry_type", "ell", "iep"]
    return K.write_csv(os.path.join(out, F_MEMBERS), hdr, member_rows(W))


def write_crosswalk(W, out):
    """IT's conversion table: every legacy student number on the 2018-19 roll with the state ID it converted to."""
    rows = []
    for (pid, s, g) in W.snap[2018]:
        z = WD.Z[s]
        rows.append([W.local[pid], W.info[pid]["sid"], K.SCHOOLS[z]["local"], "06/28/2019"])
    rows.sort(key=lambda r: r[0])
    return K.write_csv(os.path.join(out, F_XWALK), ["STU_NBR", "STATE_ID", "LAST_SCH_CD", "CONVERTED"], rows)


def write_codes(out):
    rows = []
    hist = {"D": "Southeast Elementary to June 30, 2020; renamed for Dorothy Kessler, principal 1994 to 2016"}
    opened = {"P": "1952", "C": "1961", "A": "1988", "B": "1996", "D": "1999", "E": "1974", "F": "1983"}
    for z in K.LIST_ORDER:
        sc = K.SCHOOLS[z]
        rows.append([sc["state"], sc["local"], sc["name"], sc["area"], opened[z], hist.get(z, "")])
    return K.write_csv(os.path.join(out, F_CODES),
                       ["state_school_code", "legacy_school_code", "school_name", "attendance_area", "opened",
                        "name_history"], rows)


def births_rows(W):
    """Births to county residents, geocoded from the mother's address on the birth record to the district's attendance
    areas; addresses outside the district and those that could not be matched in their own rows; 2025 provisional."""
    r = K.rng("births_file")
    rows = []
    for y in K.BIRTH_YEARS_SHIPPED:
        ng_share = float(r.uniform(0.014, 0.019))
        tot_ng = 0
        for z in K.LIST_ORDER:
            true_b = W.births[z][y]
            ng = int(round(true_b * ng_share))
            b = true_b - ng
            if y == 2025:
                late = int(round(b * 0.016))
                b -= late
            tot_ng += ng
            rows.append([y, K.SCHOOLS[z]["area"], b, "PROVISIONAL" if y == 2025 else "FINAL"])
        outside = int(round(K.lin([[2008, 1720], [2016, 1805], [2025, 1690]], y) + r.normal(0, 30)))
        rows.append([y, "OUTSIDE RE-6", outside, "PROVISIONAL" if y == 2025 else "FINAL"])
        rows.append([y, "NOT GEOCODED", tot_ng + int(r.integers(14, 31)), "PROVISIONAL" if y == 2025 else "FINAL"])
    return rows


def write_births(W, out):
    rows = births_rows(W)
    K.write_csv(os.path.join(out, F_BIRTHS), ["birth_year", "attendance_area", "births", "status"], rows)
    return rows
