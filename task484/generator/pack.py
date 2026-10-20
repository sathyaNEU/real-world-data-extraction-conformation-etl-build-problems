"""The pack's data files, cut from the truth."""
import csv
import datetime as dt
import functools

import numpy as np

import records as R
import sources as S
import world as W

METRO_COLS = ["PermitNumber", "Jurisdiction", "ParcelID", "WorkClass", "BldgType", "DwellingUnits", "ProjectName",
              "IssueDate", "Status", "ExpirationDate", "FinalDate"]
CIVIC_COLS = ["record_id", "city", "parcel_number", "project_name", "record_type", "occupancy_code", "units",
              "issued_on", "status", "expired_on", "co_issued_on"]
COUNTY_COLS = ["Permit #", "Municipality", "APN", "Issued", "Status", "Type Code", "Units", "Project",
               "C of O Date", "Expired"]
UTIL_COLS = ["premise_id", "service_city", "service_address", "bill_month", "residential_meters",
             "active_residential_accounts"]
DEMO_COLS = ["demo_permit", "city", "finaled", "units_removed"]
GQ_COLS = ["facility_id", "city", "gq_type", "residents_apr1_2026"]
SCHOOL_COLS = ["district", "city", "grade_band", "enrolled_oct1_2025"]
VOTER_COLS = ["city", "precincts", "active_registered", "inactive_registered", "as_of"]

CODE = {"metro": {"SF": "SFD", "TH": "SFA", "MF": "MF5+"},
        "county": {"SF": 101, "TH": 102, "MF": 105},
        "civic_old": {"SF": "R3", "TH": "R3T", "MF": "R2"},
        "civic_new": {"SF": "1-DET", "TH": "1-ATT", "MF": "MULTI"}}


@functools.lru_cache(None)
def everything():
    x = S.world(np.random.default_rng(W.SEED))
    return dict(x=x, permits=R.permits(np.random.default_rng(W.SEED + 1), x),
                util=R.utility(np.random.default_rng(W.SEED + 2), x))


def us(d):
    return d.strftime("%m/%d/%Y") if d else ""


def expired(p, rng):
    return p["issued"] + dt.timedelta(int(rng.integers(180, 200))) if p["status"] == "EXPIRED" else None


def metro_rows(e):
    rng = np.random.default_rng(W.SEED + 11)
    rows = []
    for c in sorted(e["permits"]):
        if W.CITIES[c][4] != "metro":
            continue
        for p in e["permits"][c]:
            rows.append(["BP-%d" % p["num"], c.upper(), "%03d-%03d-%03d" % (p["parcel"] // 1000000, p["parcel"] // 1000 % 1000,
                         p["parcel"] % 1000), "New Construction", CODE["metro"][p["kind"]], p["units"], p["project"],
                         us(p["issued"]), {"FINALED": "Finaled", "EXPIRED": "Expired", "ISSUED": "Issued"}[p["status"]],
                         us(expired(p, rng)), us(p["co"])])
    rows.sort(key=lambda r: r[0])
    return rows


def civic_rows(e):
    rng = np.random.default_rng(W.SEED + 12)
    rows = []
    for c in sorted(e["permits"]):
        if W.CITIES[c][4] != "civic":
            continue
        for p in e["permits"][c]:
            code = CODE["civic_new" if p["issued"] >= dt.date(2025, 1, 1) else "civic_old"][p["kind"]]
            ex = expired(p, rng)
            rows.append(["%s-%d" % (c[:3].upper(), p["num"]), c, "%09d" % p["parcel"], p["project"], "Residential Building",
                         code, p["units"], p["issued"].isoformat(), p["status"].title(), ex.isoformat() if ex else "",
                         p["co"].isoformat() if p["co"] else ""])
    rows.sort(key=lambda r: (r[7], r[0]))
    return rows


def county_rows(e):
    rng = np.random.default_rng(W.SEED + 13)
    rows = []
    for c in sorted(e["permits"]):
        if W.CITIES[c][4] != "county":
            continue
        for p in e["permits"][c]:
            ex = expired(p, rng)
            rows.append(["C%06d" % p["num"], c, "%d-%04d" % (p["parcel"] // 10000, p["parcel"] % 10000), p["issued"],
                         p["status"].title(), CODE["county"][p["kind"]], p["units"], p["project"], p["co"], ex])
    rows.sort(key=lambda r: (r[3], r[0]))
    return rows


def util_rows(e):
    names = {c: c.upper() for c in W.CITIES}
    return [[p, names[c], a, bm.strftime("%Y-%m"), m, act] for c, p, a, bm, m, act in
            sorted(e["util"], key=lambda r: (r[1], r[3]))]


def demo_rows(e):
    rows = []
    n = 300
    for c, v in sorted(e["x"].items()):
        for d in sorted(v["demo"], key=lambda d: d["date"]):
            n += 7
            rows.append(["DM-%05d" % n, c, d["date"].isoformat(), d["units"]])
    return rows


def gq_rows(e):
    rng = np.random.default_rng(W.SEED + 14)
    rows = []
    n = 4100
    for c, v in sorted(e["x"].items()):
        left = v["gq"]
        while left > 0:
            t = str(rng.choice(["Nursing facility", "College residence hall", "Group home", "Correctional facility",
                                "Assisted living"]))
            k = int(min(left, rng.integers(12, 420)))
            if left - k < 10:
                k = left
            left -= k
            n += int(rng.integers(1, 9))
            rows.append(["GQ%05d" % n, c, t, k])
    return rows


def school_rows(e):
    rng = np.random.default_rng(W.SEED + 15)
    rows = []
    for c in sorted(W.CITIES):
        for g, share in (("K-5", .082), ("6-8", .041), ("9-12", .054)):
            rows.append(["%s Public Schools" % c, c, g, int(W.DESIRED[c] * share * float(rng.uniform(.85, 1.15)))])
    return rows


def voter_rows(e):
    rng = np.random.default_rng(W.SEED + 16)
    return [[c, int(rng.integers(18, 31)), int(W.DESIRED[c] * float(rng.uniform(.58, .7))),
             int(W.DESIRED[c] * float(rng.uniform(.04, .08))), "2026-09-01"] for c in sorted(W.CITIES)]


def write_csv(path, cols, rows, crlf=False):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n" if crlf else "\n")
        w.writerow(cols)
        w.writerows(rows)
    return len(rows)
