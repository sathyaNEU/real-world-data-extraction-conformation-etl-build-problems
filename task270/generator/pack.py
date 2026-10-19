"""Readers of the cut pack: everything the analysis, the checks and the cracker compute is computed from the shipped
files through these, never from the generator's objects."""
import csv
import datetime as dt
import os
import zoneinfo

import openpyxl

import common as K

EASTERN = zoneinfo.ZoneInfo("America/New_York")
COMP = K.COMPONENTS


def rows(target, key):
    with open(os.path.join(target, K.FILES[key]), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _sheets(target, key):
    wb = openpyxl.load_workbook(os.path.join(target, K.FILES[key]), read_only=True, data_only=True)
    out = {}
    for ws in wb.worksheets:
        it = ws.iter_rows(values_only=True)
        head = [str(h) for h in next(it)]
        out[ws.title] = [dict(zip(head, r)) for r in it if any(v is not None for v in r)]
    return out


def scores(target, oral="mean", pat="best_points", sjt_key="Scaled score", inventory="dependability",
           written="scaled_score"):
    """Each candidate's five component scores as the pack records them, keyed by candidate number. A component the
    candidate did not sit is missing. The keyword arguments switch a component to another reading of its record."""
    S = {}
    xw = {r["candidate_no"]: r for r in rows(target, "crosswalk")}
    by_hss = {r["hss_candidate_id"]: r["candidate_no"] for r in xw.values()}
    by_ng = {r["pellwyn_id"]: r["candidate_no"] for r in xw.values() if r["pellwyn_id"]}
    for r in rows(target, "written"):
        S.setdefault(r["client_reference"], {})["written"] = float(r[written])
    acc = {}
    for r in rows(target, "oral"):
        acc.setdefault(r["candidate_no"], []).append(int(r["rating"]))
    for c, v in acc.items():
        S.setdefault(c, {})["oral"] = (sum(v) / len(v) * 20) if oral == "mean" else float(sum(v))
    best = {}
    for r in rows(target, "pat"):
        t = float(r["course_seconds"])
        p = float(r["points"])
        c = r["candidate_no"]
        if pat == "first" and r["attempt"] != "1":
            continue
        cur = best.get(c)
        if cur is None or t < cur[0]:
            best[c] = (t, p)
    for c, (t, p) in best.items():
        S.setdefault(c, {})["pat"] = p if pat in ("best_points", "first") else -t
    for sheet in _sheets(target, "sjt").values():
        for r in sheet:
            S.setdefault(by_ng[r["Pellwyn ID"]], {})["sjt"] = float(r[sjt_key])
    for r in rows(target, "inventory"):
        S.setdefault(by_hss[r["hss_candidate_id"]], {})["inventory"] = float(r[inventory])
    return S


def register(target):
    return {r["candidate_no"]: r for r in rows(target, "roster")}


def academy(target, separated=True):
    """The academy's criterion by employee number: the final (weighted) average, or the average at separation."""
    out = {}
    for name, sheet in _sheets(target, "academy").items():
        for r in sheet:
            if "Recruit No." in r:
                emp, v = r["Recruit No."], r["Final Average"]
                sep = str(r["Status"]).startswith("Separated")
            else:
                emp = r["Employee ID"]
                sep = r["Outcome"] == "Separated"
                v = r["Average at Separation"] if sep else r["Weighted Average"]
            if sep and not separated:
                continue
            out[int(emp)] = float(v)
    return out


def sample(target, **kw):
    """The candidate pool (everyone who sat all five components) with each member's scores, veteran credit, physical
    ability test pass, appointment and academy criterion. The appointees are the pool members the lists appointed."""
    S = scores(target, **{k: v for k, v in kw.items() if k in ("oral", "pat", "sjt_key", "inventory", "written")})
    reg = register(target)
    acad = academy(target, separated=kw.get("separated", True))
    pat_pass = {}
    for r in rows(target, "pat"):
        pat_pass[r["candidate_no"]] = pat_pass.get(r["candidate_no"], False) or r["result"] == "Pass"
    out = []
    for c, s in sorted(S.items()):
        if kw.get("pool", "all_five") == "all_five" and not all(k in s for k in COMP):
            continue
        g = reg.get(c)
        appointed = bool(g) and g["disposition"] == "Appointed"
        y = acad.get(int(g["employee_no"])) if appointed and g["employee_no"] else None
        out.append(dict(cand=c, s=s, vet=bool(g) and g["veteran_credit"] == "5.00", listed=bool(g),
                        pat_pass=pat_pass.get(c, False), final=float(g["final_score"]) if g else None,
                        appointed=appointed and y is not None, y=y))
    return out


# ------------------------------------------------------------------------------------------------ the ledger
ADM_NAMES = ["Autumn 2023", "Spring 2024", "Autumn 2024", "Spring 2025", "Autumn 2025", "Spring 2026"]
TRIAL_NAMES = [a["name"] for a in K.ADMIN]


def ledger(target):
    out = []
    for r in rows(target, "ledger"):
        r = dict(r)
        r["amount"] = float(r["amount"])
        r["date"] = dt.date.fromisoformat(r["posting_date"])
        out.append(r)
    return out


# ------------------------------------------------------------------------------------------------ applications
def applications(target):
    """Both tracking exports as records: (administration, record) for every form, with the fields the identity work
    needs normalised only as far as the export itself fixes them (no date-of-birth repair)."""
    out = []
    for r in rows(target, "ats_old"):
        out.append(dict(system="legacy", ref=r["posting_no"], title=r["posting_title"], first=r["first_name"],
                        last=r["last_name"], dob=dt.datetime.strptime(r["date_of_birth"], "%m/%d/%Y").date(),
                        email=r["email"], phone=r["phone"], source=r["source"], status=r["status"],
                        submitted=(dt.datetime.strptime(r["submitted"], "%m/%d/%Y %H:%M") if r["submitted"] else None),
                        officer=""))
    for r in rows(target, "ats_new"):
        sub = None
        if r["submitted_at_utc"]:
            u = dt.datetime.strptime(r["submitted_at_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
            sub = u.astimezone(EASTERN).replace(tzinfo=None)
        out.append(dict(system="new", ref=r["requisition_id"], title=r["job_title"], first=r["first_name"],
                        last=r["last_name"], dob=dt.date.fromisoformat(r["birth_date"]), email=r["email"],
                        phone=r["phone"], source=r["source"], status=r["application_status"], submitted=sub,
                        officer=r["currently_employed_peace_officer"], utc=r["submitted_at_utc"]))
    return out
