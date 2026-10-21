"""Readers of the cut pack, shared by the analysis and the cracker: every figure the build reports is computed from the
files in target/, never from the world. The three hubs' extracts are conformed to one row shape: hospital, local
datetime, user, application, guarantor, type (INITIAL, RECON, PRESUMPTIVE), outcome (approve, deny, pend, withdraw),
the percent written off and the raw reason code."""
import csv
import datetime as dt
import os
from zoneinfo import ZoneInfo

import common as K

PACIFIC = ZoneInfo("America/Los_Angeles")
SYSTEM = set(K.SYSTEM_USER.values())


def rows(target, key):
    with open(os.path.join(target, K.FILES[key]), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def conformed(target, utc_as_local=False):
    """Every row of the three extracts in one shape. utc_as_local reads the Columbia clock as if it were local."""
    out = []
    for r in rows(target, "puget"):
        out.append(dict(code=r["hospital_code"], when=dt.datetime.strptime(r["determined_at"], "%Y-%m-%d %H:%M:%S"),
                        user=r["user_id"], app=r["application_id"], guarantor=r["guarantor_id"],
                        type={"INITIAL": "INITIAL", "RECONSIDERATION": "RECON",
                              "PRESUMPTIVE": "PRESUMPTIVE"}[r["determination_type"]],
                        outcome={"APPROVED": "approve", "DENIED": "deny", "PENDED": "pend",
                                 "WITHDRAWN": "withdraw"}[r["outcome"]],
                        pct=int(r["discount_pct"]) if r["discount_pct"] else None,
                        reason=int(r["denial_reason"]) if r["denial_reason"] else None, hub="puget",
                        rid=r["determination_id"]))
    for r in rows(target, "willamette"):
        when = dt.datetime.strptime(r["DET_DATE"] + " " + r["DET_TIME"], "%m/%d/%Y %H:%M:%S")
        out.append(dict(code=r["HOSP_ID"], when=when, user=r["USER_ID"], app=r["APPL_NO"], guarantor=r["GUAR_NO"],
                        type="PRESUMPTIVE" if r["USER_ID"] in SYSTEM else ("RECON" if r["RECON"] == "Y" else "INITIAL"),
                        outcome={"A": "approve", "D": "deny", "P": "pend", "X": "withdraw"}[r["RESULT"]],
                        pct=int(r["ADJ_PCT"]) if r["ADJ_PCT"] else None,
                        reason=int(r["DENY_RSN"]) if r["DENY_RSN"] else None, hub="willamette", rid=r["DET_NO"]))
    for r in rows(target, "columbia"):
        t = dt.datetime.strptime(r["ts_utc"], "%Y-%m-%dT%H:%M:%SZ")
        when = t if utc_as_local else t.replace(tzinfo=ZoneInfo("UTC")).astimezone(PACIFIC).replace(tzinfo=None)
        d = int(r["decision"])
        out.append(dict(code=r["facility"], when=when, user=r["staff_key"], app=r["app_ref"], guarantor=r["guarantor"],
                        type={"new": "INITIAL", "recheck": "RECON", "screen": "PRESUMPTIVE"}[r["kind"]],
                        outcome={1: "approve", 2: "approve", 3: "deny", 8: "withdraw", 9: "pend"}[d],
                        pct=int(r["pct"]) if r["pct"] else None, reason=int(r["reason"]) if r["reason"] else None,
                        hub="columbia", rid=r["seq"]))
    return out


def counsellor_days(target, rows_=None, keep=None):
    """By hospital, the counsellor-days of the criteria: each counsellor's approvals and denials on each local working
    day, in the order recorded (1 an approval). keep(row) may widen or narrow the rows for a stop."""
    rows_ = conformed(target) if rows_ is None else rows_
    keep = keep or (lambda r: r["outcome"] in ("approve", "deny") and r["user"] not in SYSTEM)
    by = {}
    for r in rows_:
        if not keep(r):
            continue
        by.setdefault(r["code"], {}).setdefault((r["user"], r["when"].date()), []).append(r)
    out = {}
    for code, days in by.items():
        lst = []
        for (user, day), rs in sorted(days.items()):
            rs.sort(key=lambda x: x["when"])
            lst.append((user, day, [1 if x["outcome"] == "approve" else 0 for x in rs]))
        out[code] = lst
    return out


def ledger(target, dedupe=True):
    L = rows(target, "ledger")
    if not dedupe:
        return L
    seen, out = set(), []
    for r in L:
        k = tuple(r.values())
        if k not in seen:
            seen.add(k)
            out.append(r)
    return out
