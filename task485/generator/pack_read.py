"""Read the cut pack back into rows: golden.py, ceiling.py and checks.py compute from the pack as shipped, never from
the world."""
import csv
import datetime as dt
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
EXTRACT = "population_register_extract_20260930.csv"
ARCHIVE = "population_register_legacy_archive_2014_2023.csv"
XWALK = "registration_number_crosswalk_2023.csv"
SECTORS = "sector_classification_2026.json"


def iso(s):
    return dt.date.fromisoformat(s) if s else None


def dmy(s):
    if not s:
        return None
    d, m, y = (int(x) for x in s.split("/"))
    return dt.date(y, m, d)


def read(target=TARGET):
    sc = json.load(open(os.path.join(target, SECTORS)))
    to26 = {c["code"]: c["sector_2026"] for c in sc["activity_codes_2014"]}
    to26.update({c["code"]: c["code"] for c in sc["sectors_2026"]})
    cur = []
    for r in csv.DictReader(open(os.path.join(target, EXTRACT), encoding="utf-8")):
        cur.append(dict(reg=r["reg_no"], ref=r["stay_ref"], origin=r["record_origin"], arrive=iso(r["arrival_date"]),
                        registered=iso(r["registered_on"]), code=r["activity_code"], sector=to26[r["activity_code"]],
                        parish=r["parish_code"], sex=r["sex"], yob=int(r["birth_year"]), nat=r["nationality"],
                        leave=iso(r["leaving_date"]), notice=iso(r["notice_received"])))
    arc = []
    for r in csv.DictReader(open(os.path.join(target, ARCHIVE), encoding="utf-8")):
        arc.append(dict(legacy=r["LEGACY_NO"], arrive=dmy(r["DATE_OF_ARRIVAL"]), registered=dmy(r["DATE_REGISTERED"]),
                        code=r["ACTIVITY"], sector=to26[r["ACTIVITY"]], parish=r["PARISH"], sex=r["SEX"],
                        yob=int(r["YOB"]), nat=r["NATIONALITY"], leave=dmy(r["DATE_OF_LEAVING"]),
                        closure=r["CLOSURE"], closed=dmy(r["CLOSED_ON"])))
    xw = {r["legacy_no"]: r["reg_no"] for r in csv.DictReader(open(os.path.join(target, XWALK), encoding="utf-8"))}
    return dict(cur=cur, arc=arc, xw=xw, to26=to26, sectors=[c["code"] for c in sc["sectors_2026"]],
                names={c["code"]: c["name"] for c in sc["sectors_2026"]})
