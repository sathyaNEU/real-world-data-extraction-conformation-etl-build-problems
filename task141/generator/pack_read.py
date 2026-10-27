"""Read the cut pack back: golden.py, ceiling.py and checks.py compute from the pack as shipped, never from the world.

record(P) builds the forecast record forecast.py runs on (the felony terms of both CaseTrak systems with their
supervision begin day, risk score on version 2, imposed term, scheduled expiration in force at each date and closure,
and the Circuit Court's petitions on them); the rest are the asks' inputs."""
from __future__ import annotations

import csv
import datetime as dt
import os

import common as K
import forecast as F

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
M = K.M
CLOSE1 = {"EXP": "EXPIRED", "REV": "REVOKED", "ETERM": "EARLY_TERM"}
CLOSE2 = {"EXPIRED": "EXPIRED", "REVOKED": "REVOKED", "EARLY TERMINATION": "EARLY_TERM"}


def rows(target, name):
    with open(os.path.join(target, name), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def mdy(s):
    if not s:
        return None
    m, d, y = (int(x) for x in s.split("/"))
    return dt.date(y, m, d)


def iso(s):
    return dt.date.fromisoformat(s) if s else None


def read(target=TARGET):
    return dict(cms1=rows(target, K.CMS1), cms2=rows(target, K.CMS2), orders=rows(target, K.ORDERS),
                pets=rows(target, K.PETITIONS), book=rows(target, K.BOOKINGS), persons=rows(target, K.PERSONS))


def terms(P):
    """every supervision term of both systems, keyed by case number"""
    out = {}
    for r in P["cms1"]:
        out[r["CASE_NO"]] = dict(case=r["CASE_NO"], person=r["APD_PERSON_NO"], lvl=r["LEVEL"],
                                 office={o[2]: o[0] for o in K.OFFICES}[r["OFFICE"]], sup=K.day(mdy(r["SUP_BEGIN"])),
                                 length=round(int(r["TERM_DAYS"]) / M), exp=K.day(mdy(r["EXPIRES"])),
                                 score=int(r["RISK_SCORE"]) // 2, open=False,
                                 closed=(K.day(mdy(r["CLOSE_DATE"])), CLOSE1[r["CLOSE_CODE"]]))
    for r in P["cms2"]:
        cd = iso(r["closed_date"])
        out[r["case_number"]] = dict(case=r["case_number"], person=r["person_id"], lvl=r["offense_level"][0],
                                     office=r["office"], sup=K.day(iso(r["supervision_begin"])),
                                     length=int(r["term_months"]), exp=K.day(iso(r["expiration_date"])),
                                     score=int(r["csrs_score"]), open=r["case_status"] == "OPEN",
                                     closed=(K.day(cd), CLOSE2[r["closure_reason"]]) if cd else None)
    ext = {}
    for o in P["orders"]:
        if o["order_type"] == "EXTENSION":
            ext[o["case_number"]] = ext.get(o["case_number"], 0) + int(o["months_extended"])
    for t in out.values():
        t["extended"] = ext.get(t["case"], 0)
        t["imposed"] = t["length"] - t["extended"]
    return out


def record(P):
    """the forecast record of the felony terms"""
    T = terms(P)
    R = F.Rec()
    R.cases = []
    for t in sorted(T.values(), key=lambda t: (t["sup"], t["case"])):
        if t["lvl"] == "F":
            R.cases.append(dict(id=t["case"], sup=t["sup"], score=t["score"], term=t["imposed"]))
    R.C = {c["id"]: c for c in R.cases}
    by = {}
    for o in P["orders"]:
        if o["case_number"] in R.C and o["order_type"] != "EARLY TERMINATION":
            by.setdefault(o["case_number"], []).append(o)
    R.scheds, R.sched_now, R.close = {}, {}, {}
    for c in R.cases:
        t = T[c["id"]]
        os_ = by.get(c["id"], [])
        orig = K.day(iso(os_[0]["expiration_before"])) if os_ else t["exp"]
        sch = [(-10 ** 6, orig)]
        for o in os_:
            d = K.day(iso(o["order_date"]))
            v = K.day(iso(o["expiration_after"]))
            if sch[-1][0] == d:
                sch[-1] = (d, v)
            else:
                sch.append((d, v))
        R.scheds[c["id"]] = sch
        R.sched_now[c["id"]] = sch[-1][1]
        if t["closed"] is not None:
            R.close[c["id"]] = t["closed"]
    R.pet, R.byc = [], {}
    for p in P["pets"]:
        if p["case_number"] not in R.C:
            continue
        dd = iso(p["disposition_date"])
        q = dict(case=p["case_number"], file=K.day(iso(p["filed_date"])), decided=K.day(dd) if dd else None,
                 revoked=(p["disposition"] == "REVOKED") if dd else None)
        R.pet.append(q)
        R.byc.setdefault(q["case"], []).append(q)
    F.finish(R)
    return R


# ---------------------------------------------------------------------------------------------------- bookings
def local(s):
    """a booking time as county (Central) local time: the old system writes it local, the new one in UTC"""
    if not s:
        return None
    if s.endswith("Z"):
        return K.from_utc(dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:00Z"))
    return dt.datetime.strptime(s, "%m/%d/%Y %H:%M")


def bookings(P, utc_as_local=False):
    out = []
    for r in P["book"]:
        if utc_as_local:
            f = (lambda s: dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:00Z") if s and s.endswith("Z") else local(s))
        else:
            f = local
        out.append(dict(no=r["booking_number"], so=r["sheriff_id"], start=f(r["booked_at"]), end=f(r["released_at"]),
                        cls=r["classification"], fac=r["facility"], reason=r["release_reason"]))
    return out


def sheriff_to_person(P, merged=True):
    m = {}
    for r in P["persons"]:
        if r["sheriff_id_status"] == "CURRENT" or merged:
            m[r["sheriff_id"]] = r["apd_person_id"]
    return m
