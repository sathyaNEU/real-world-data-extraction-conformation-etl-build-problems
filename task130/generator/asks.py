"""The two asks from the shipped pack, with the stops a solver lands on when a device or hazard is mishandled.

Ask A: for each entity, the open claims under its occurrence policies that are missing from its carrier's latest loss
run, how many and the register's reserves on them.
Ask B: each entity's covered clinician FTE in September 2026 by specialty class, from the HCM pay lines."""
from __future__ import annotations

import csv
import datetime as dt
import os

import openpyxl

import analysis as AN
import common as K

QM_NAMES = {"Tolliver Falls Hospital": "TFH", "Alderwick Medical Center": "AMC"}
SC_NAMES = {"CORVANE MEDICAL GROUP": "CMG", "BRENNICK COMMUNITY HOSP": "BCH"}


def norm(ref):
    return "".join(ch for ch in str(ref).upper() if ch.isalnum())


def load_qm(target, fname):
    wb = openpyxl.load_workbook(os.path.join(target, fname), data_only=True)
    ws = wb["Loss Run"]
    valued = None
    for row in ws.iter_rows(min_row=1, max_row=6, values_only=True):
        if row[0] and str(row[0]).startswith("Valuation Date"):
            m, d, y = str(row[0]).split(": ")[1].split("/")
            valued = dt.date(int(y), int(m), int(d))
    out = []
    for row in ws.iter_rows(min_row=8, values_only=True):
        if not row[3]:
            continue
        out.append(dict(entity=QM_NAMES[row[2]], ref=row[4], ctype=row[7], status=row[8]))
    return valued, out


def load_sc(target):
    out = []
    valued = None
    with open(os.path.join(target, K.SC_SEP), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out.append(dict(entity=SC_NAMES[r["INSURED_NAME"]], ref=r["INSURED_REF"], ctype=r["CLM_TYPE"],
                            status=r["CLM_STATUS"]))
            m, d, y = r["VALUATION_DT"].split("/")
            valued = dt.date(int(y), int(m), int(d))
    return valued, out


def load_notices(target):
    with open(os.path.join(target, K.NOTICES), encoding="utf-8") as fh:
        return {r["notice_no"]: r["incident_no"] for r in csv.DictReader(fh)}


def _open_by_incident(rows, line):
    opn, res = {}, {}
    for r in rows:
        if r["coverage_line"] == line and r["status"] in ("OPEN", "REOPENED"):
            opn[r["incident_no"]] = True
    for r in rows:
        if r["coverage_line"] == line and r["incident_no"] in opn:
            res[r["incident_no"]] = res.get(r["incident_no"], 0.0) + (r["indemnity_reserve"] or 0.0) + \
                (r["defense_reserve"] or 0.0)
    return sorted(opn), res


def ask_a(target, rows=None):
    rows = rows if rows is not None else AN.load_register(target)
    notices = load_notices(target)
    claim_inc = {}
    for r in rows:
        claim_inc[norm(r["claim_no"])] = r["incident_no"]
    notice_inc = {norm(k): v for k, v in notices.items()}
    qm_v, qm = load_qm(target, K.QM_SEP)
    qmj_v, qmj = load_qm(target, K.QM_JUN)
    sc_v, sc = load_sc(target)
    assert qm_v == K.VALUATION and sc_v == K.VALUATION and qmj_v == dt.date(2026, 6, 30)
    latest = {"TFH": qm, "AMC": qm, "CMG": sc, "BCH": sc}
    delivered_last = {"TFH": qmj, "AMC": qmj, "CMG": sc, "BCH": sc}

    def mapped(run, e, use_notices=True):
        out = set()
        for x in run:
            if x["entity"] != e:
                continue
            k = norm(x["ref"])
            if k in claim_inc:
                out.add(claim_inc[k])
            elif use_notices and k in notice_inc:
                out.add(notice_inc[k])
        return out

    res = {}
    for e in K.ENTITY_ORDER:
        line = K.ENTITIES[e]["line"]
        opn, reserve = _open_by_incident(rows, line)
        found = mapped(latest[e], e)
        miss = [i for i in opn if i not in found]
        # stops
        refs = {norm(x["ref"]) for x in latest[e] if x["entity"] == e}
        open_nos = sorted({r["claim_no"] for r in rows if r["coverage_line"] == line and r["status"] in ("OPEN", "REOPENED")})
        res_no = {}
        prior = {}
        for r in rows:
            if r["coverage_line"] == line and r["claim_no"] in open_nos:
                res_no[r["claim_no"]] = res_no.get(r["claim_no"], 0.0) + (r["indemnity_reserve"] or 0.0) + \
                    (r["defense_reserve"] or 0.0)
                prior[r["claim_no"]] = r["prior_claim_no"]
        s1 = [c for c in open_nos if norm(c) not in refs]
        s2 = [c for c in open_nos if norm(c) not in refs and norm(prior[c]) not in refs]
        found_j = mapped(delivered_last[e], e)
        s3 = [i for i in opn if i not in found_j]
        res[e] = dict(open=len(opn), missing=miss, count=len(miss), reserves=sum(reserve[i] for i in miss),
                      s1=(len(s1), sum(res_no[c] for c in s1)), s2=(len(s2), sum(res_no[c] for c in s2)),
                      s3=(len(s3), sum(reserve[i] for i in s3)))
    return res


def crosswalk(target):
    with open(os.path.join(target, K.CROSSWALK), encoding="utf-8") as fh:
        return {r["job_profile_code"]: r["legacy_job_code"] for r in csv.DictReader(fh)}


def directory(target):
    with open(os.path.join(target, K.DIRECTORY), encoding="utf-8") as fh:
        return {r["cost_centre"]: r["entity_code"] for r in csv.DictReader(fh)}


def ask_b(target):
    """Each entity's covered clinician FTE in September 2026: one FTE per position held that month, covered by its job
    profile through the crosswalk and Schedule B, on the entity of the cost centre its lines are charged to."""
    sb = AN.schedule_b()
    xw = crosswalk(target)
    cc = directory(target)
    lines = []
    with open(os.path.join(target, K.HCM), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["work_month"] == "2026-09":
                lines.append(r)
    out = {name: {} for name in ("gold", "s1", "s2", "s3", "s4")}
    add = lambda d, key, v: d.__setitem__(key, d.get(key, 0.0) + v)
    seen = {name: set() for name in out}
    title_class = {"Physician, Cardiology Fellow": "HM", "Physician, Critical Care Fellow": "HM"}
    for r in lines:
        k = sb.get(xw[r["job_profile_code"]])
        f = float(r["fte"])
        pos = (r["worker_id"], r["position_id"])
        if k:
            add(out["s1"], r["home_entity"], f)                                   # every line, home entity
            if r["worker_id"] not in seen["s2"]:                                  # one FTE per worker, home entity
                seen["s2"].add(r["worker_id"])
                add(out["s2"], r["home_entity"], f)
            if pos not in seen["s4"]:                                             # one per position, home entity
                seen["s4"].add(pos)
                add(out["s4"], r["home_entity"], f)
            if pos not in seen["gold"]:                                           # one per position, cost centre
                seen["gold"].add(pos)
                add(out["gold"], cc[r["cost_centre"]], f)
        k3 = k or title_class.get(r["job_profile"])
        if k3 and pos not in seen["s3"]:                                          # fellows read as specialists
            seen["s3"].add(pos)
            add(out["s3"], cc[r["cost_centre"]], f)
    res = {name: {e: round(d.get(e, 0.0), 1) for e in K.ENTITY_ORDER} for name, d in out.items()}
    res["raw"] = out["gold"]
    return res
