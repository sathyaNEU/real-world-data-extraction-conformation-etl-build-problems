"""Readers of the shipped pack: every file read the way an analyst reads it, with the reference workbook's codes, so the
analysis and the asks run on the files and never on the generator's world."""
import os
import datetime as dt

import pandas as pd

import common as K


def load(target):
    p = lambda k: os.path.join(target, K.FILES[k])
    d = {}
    d["audits"] = pd.read_csv(p("audits"), dtype=str)
    d["acuity"] = pd.read_csv(p("acuity"), dtype={"ward": str, "shift": str, "bed": str, "encounter": str})
    d["roster"] = pd.read_csv(p("roster"), dtype=str)
    d["isolates"] = pd.read_csv(p("isolates"), dtype=str)
    d["admissions"] = pd.read_csv(p("admissions"), dtype=str)
    d["transfers"] = pd.read_csv(p("transfers"), dtype=str)
    d["census"] = pd.read_csv(p("census"), dtype={"ward": str})
    d["issues"] = pd.read_csv(p("issues"), dtype=str)
    d["rounds"] = pd.read_csv(p("rounds"), dtype=str)
    x = pd.ExcelFile(p("wards"))
    d["wards"] = x.parse("Wards", dtype=str)
    d["areas"] = x.parse("Areas", dtype=str)
    d["dispensers"] = x.parse("Dispensers", dtype=str)
    return d


def maps(d):
    """the reference workbook's crosswalks: application department, laboratory location and dispenser to ward, and the
    code each ward carried; S1A is ward 6A's code from 2 February 2026"""
    w = d["wards"]
    code_of = {}
    for _, r in w.iterrows():
        c = r["code"]
        canon = K.MOVED[0] if c == K.MOVED[1] else c
        code_of[c] = canon
    dept = {r["audit_application_department"]: code_of[r["code"]] for _, r in w.iterrows()}
    lab = {r["laboratory_location"]: code_of[r["code"]] for _, r in w.iterrows()}
    for _, r in d["areas"].iterrows():
        dept[r["audit_application_department"]] = r["code"]
        lab[r["laboratory_location"]] = r["code"]
    disp = {r["dispenser_id"]: code_of.get(r["ward_or_area"], r["ward_or_area"]) for _, r in d["dispensers"].iterrows()}
    cc = {r["cost_centre"]: code_of[r["code"]] for _, r in w.iterrows()}
    return dict(ward=code_of, dept=dept, lab=lab, disp=disp, cc=cc)


def shift_of(hhmm):
    """the roster shift a session began in: AM 07:00 to 15:30, PM 13:00 to 21:30, night 21:00 to 07:30; no session
    begins in an overlap"""
    h, m = int(hhmm[:2]), int(hhmm[3:])
    t = h * 60 + m
    if 7 * 60 <= t < 13 * 60:
        return "AM"
    if 15 * 60 + 30 <= t < 21 * 60:
        return "PM"
    if t >= 21 * 60 + 30 or t < 7 * 60:
        return "ND"
    return "overlap"


def day_shifts(d, m, supernumerary=False, escalation=True):
    """each ward's AM and PM shifts with the required care hours of its patients (acuity) and the worked nursing
    hours of its rostered nurses, supernumerary shifts left out; the options run the mishandled readings"""
    a = d["acuity"].copy()
    if not escalation:
        a = a[~a["bed"].str.contains("ESC")]
    a["ward"] = a["ward"].map(m["ward"])
    a["date"] = pd.to_datetime(a["shift_date"]).dt.date
    a["required_care_hours"] = a["required_care_hours"].astype(float)
    req = a.groupby(["ward", "date", "shift"])["required_care_hours"].sum()
    npts = a.groupby(["ward", "date", "shift"]).size()
    r = d["roster"].copy()
    r = r[r["shift_code"].isin(["AM", "PM"])]
    if not supernumerary:
        r = r[r["shift_category"] == "Rostered"]
    r["ward"] = r["ward"].map(m["ward"])
    r["date"] = pd.to_datetime(r["roster_date"], format="%d/%m/%Y").dt.date
    r["worked_hours"] = r["worked_hours"].astype(float)
    worked = r.groupby(["ward", "date", "shift_code"])["worked_hours"].sum()
    worked.index = worked.index.set_names(["ward", "date", "shift"])
    out = pd.concat([req.rename("req"), worked.rename("worked"), npts.rename("npts")], axis=1).reset_index()
    out["v"] = out["req"] / out["worked"]
    return out[out["v"].notna() & (out["worked"] > 0)].reset_index(drop=True)


def ward_audits(d, m):
    """the ward sessions' moments with their ward, date and shift"""
    a = d["audits"].copy()
    a["ward"] = a["department"].map(m["dept"])
    a["date"] = pd.to_datetime(a["session_date"], format="%d/%m/%Y").dt.date
    a["shift"] = a["session_start"].map(shift_of)
    a["performed"] = a["action"].isin(["Hand rub", "Hand wash"]).astype(int)
    return a
