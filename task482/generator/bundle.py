"""Read the cut pack the way an analyst would, and run every route the design names on it. Nothing here reads
world.py's truth; golden.py, checks.py, verify.py and ceiling.py all go through it.

    load(target)            the conformed register, referral list, audit outcomes and gazette notices
    rates(b, route)         each region's share of its 30 April 2026 records in error under a route
    chosen(b, r)            the regions over 4 per cent
    ask_a(b, local)         each region's third-quarter 2026 registrations
    ask_b(b, restored)      each region's companies struck off in the quarter and still dissolved at its end"""
import csv
import datetime as dt
import os

FILES = {
    "register": "sar_business_register_extract_2026-09-30.csv",
    "screen": "sar_register_risk_screen_referrals_2026-05.csv",
    "audit": "sar_register_quality_audit_summer_2026.csv",
    "codes": "sar_region_code_crosswalk_2025.csv",
    "gazette": "ardmuir_gazette_company_notices_2026q3.csv",
}
LINE = 0.04
GOLDEN_FORMS = ("golden", "design_weights", "hajek")
ROUTES = GOLDEN_FORMS + ("audited_share", "unflagged_only", "whole_extract")


def _csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def local(s):
    """A UTC timestamp to Ardmuir local time (British Summer Time from the last Sunday of March to the last Sunday of
    October, at 01:00 UTC)."""
    t = dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
    y = t.year
    start = max(dt.datetime(y, 3, d) for d in range(25, 32) if dt.date(y, 3, d).weekday() == 6) + dt.timedelta(hours=1)
    end = max(dt.datetime(y, 10, d) for d in range(25, 32) if dt.date(y, 10, d).weekday() == 6) + dt.timedelta(hours=1)
    return t + dt.timedelta(hours=1) if start <= t < end else t


def load(target):
    reg = _csv(os.path.join(target, FILES["register"]))
    region = {r["record_id"]: r["region"] for r in reg}
    created = {r["record_id"]: local(r["created_at_utc"]) for r in reg}
    flagged = {r["record_id"] for r in _csv(os.path.join(target, FILES["screen"])) if r["referred"] == "Y"}
    code = {r["region_old"]: r["region"] for r in _csv(os.path.join(target, FILES["codes"]))}
    audit = []
    for r in _csv(os.path.join(target, FILES["audit"])):
        err = r["outcome"] in ("FAIL", "1", "2", "3", "4")
        audit.append((r["record_id"], code[r["region_old"]], err))
    ids = sorted(set(region.values()))
    gaz = _csv(os.path.join(target, FILES["gazette"]))
    return {"reg": reg, "region": region, "created": created, "flagged": flagged, "audit": audit, "ids": ids,
            "gaz": gaz}


def rates(b, route="golden"):
    cut = dt.datetime(2026, 5, 1)
    frame = {k for k, t in b["created"].items() if t < cut} if route != "whole_extract" else set(b["created"])
    N = {(u, f): 0 for u in b["ids"] for f in (True, False)}
    for k in frame:
        N[(b["region"][k], k in b["flagged"])] += 1
    n = {key: [0, 0] for key in N}
    for k, u, e in b["audit"]:
        n[(u, k in b["flagged"])][0] += 1
        n[(u, k in b["flagged"])][1] += e
    out = {}
    for u in b["ids"]:
        tot = N[(u, True)] + N[(u, False)]
        if route == "audited_share":
            out[u] = (n[(u, True)][1] + n[(u, False)][1]) / (n[(u, True)][0] + n[(u, False)][0])
        elif route == "unflagged_only":
            out[u] = n[(u, False)][1] / n[(u, False)][0]
        elif route == "design_weights":
            p = {True: 0.24, False: 0.04}
            out[u] = sum(n[(u, f)][1] / p[f] for f in (True, False)) / tot
        elif route == "hajek":
            p = {True: 0.24, False: 0.04}
            out[u] = sum(n[(u, f)][1] / p[f] for f in (True, False)) / sum(n[(u, f)][0] / p[f] for f in (True, False))
        else:
            out[u] = sum(N[(u, f)] * n[(u, f)][1] / n[(u, f)][0] for f in (True, False)) / tot
    return out


def chosen(b, r):
    return sorted(u for u in r if r[u] > LINE)


def ask_a(b, as_local=True):
    """Registrations created in the third quarter of 2026, by the register's own quarter in Ardmuir local time."""
    out = {u: 0 for u in b["ids"]}
    for r in b["reg"]:
        t = local(r["created_at_utc"]) if as_local else dt.datetime.strptime(r["created_at_utc"], "%Y-%m-%dT%H:%M:%SZ")
        if dt.datetime(2026, 7, 1) <= t < dt.datetime(2026, 10, 1):
            out[r["region"]] += 1
    return out


def ask_b(b, restored=True):
    """Companies struck off and dissolved in the quarter and still dissolved at its end (a restoration later in the
    quarter takes the company back onto the register)."""
    last = {}
    for r in sorted(b["gaz"], key=lambda r: (r["gazette_date"], r["notice_id"])):
        if r["notice_type"] == "struck off and dissolved":
            last[r["record_id"]] = "dissolved"
        elif r["notice_type"] == "restored to the register" and restored:
            last[r["record_id"]] = "restored"
    out = {u: 0 for u in b["ids"]}
    for k, s in last.items():
        if s == "dissolved":
            out[b["region"][k]] += 1
    return out
