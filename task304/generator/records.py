"""Write the shipped data files from the clean world, each the way its own producing system writes it.

Layer 1, all from the producers' own systems and none deciding the call:
- the laboratory's test codes renamed at its March 2021 system change (HCVAB and HCVPCR became HCV-AB-EIA and
  HCV-RNA-VL), results written as text, a viral load column, a month of rows re-sent by the new system;
- the network register's twelve-week results keyed by hand since the clinical system went live on 1 October 2024;
- the prison provider's workbook in two layouts (2017-20 and 2021-26), day-first text dates, the shared pseudonym
  written in lower case on the older sheet;
- the peer team's setting column written several ways, invalid kit results, tests at venues outside the four
  settings;
- the arrivals returns: the hostels write dates day-first, a person's second stay in a year is a second row;
- the pilot caseload as the 2019 evaluation kept it."""
import csv
import datetime as dt
import io
import hashlib
import os
from collections import defaultdict

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font

import params as P
import postprocess

D = dt.date


def _w(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(header)
        for r in rows:
            w.writerow(["" if v is None else v for v in r])


def _iso(d):
    return d.isoformat() if d else ""


def _dmy(d):
    return d.strftime("%d/%m/%Y") if d else ""


REQ_LOC = {
    "GP": [("C84%03d" % i, "GP") for i in (11, 23, 37, 40, 52, 66, 71, 89, 94, 108, 117, 125, 131, 146, 158, 162)],
    "ANTENATAL": [("RTB-ANC", "Antenatal"), ("RTB-ANC2", "Antenatal")],
    "SEXUAL_HEALTH": [("SH-FEN", "Sexual health"), ("SH-COR", "Sexual health")],
    "HOSPITAL": [("RTB-HEP", "Hospital"), ("RTB-AMU", "Hospital"), ("RTB-GAS", "Hospital")],
    "DRUG_SERVICE": [("FR-FEN", "Drug service"), ("FR-COR", "Drug service"), ("FR-SAL", "Drug service")],
    "OUTREACH_CLINIC": [("HCN-OUT", "Outreach clinic")],
    "COMMUNITY_CLINIC": [("HCN-COM", "Community hepatitis clinic")],
    "PHARMACY_CLINIC": [("HCN-PHC", "Pharmacy clinic")],
}


# how the requesting sites share the work: practice list sizes and site sizes differ, and a person keeps their site
LOC_WEIGHT = {
    "GP": [2.1, 0.6, 1.4, 0.9, 1.8, 0.7, 1.1, 0.5, 1.6, 0.8, 1.2, 0.4, 1.0, 1.5, 0.9, 0.7],
    "ANTENATAL": [0.72, 0.28],
    "SEXUAL_HEALTH": [0.66, 0.34],
    "HOSPITAL": [0.45, 0.20, 0.35],
    "DRUG_SERVICE": [0.52, 0.31, 0.17],
}


def _site(person, requester, locs):
    w = LOC_WEIGHT.get(requester)
    if not w or len(w) != len(locs):
        return None
    u = int(hashlib.sha256(("site-%d-%s-%s" % (P.SEED, person, requester)).encode()).hexdigest()[:12], 16) / 16 ** 12
    t, acc = u * sum(w), 0.0
    for loc, wi in zip(locs, w):
        acc += wi
        if t < acc:
            return loc
    return locs[-1]


def lab(W, path, rng):
    lims = lims_ids(W)
    rows = [x for x in W.lab if x["sample_date"] <= P.AS_OF]
    rows.sort(key=lambda x: (x["sample_date"], x["pid"], x["test"]))
    out = []
    seq = {}
    for x in rows:
        y = x["sample_date"].year
        seq[y] = seq.get(y, 0) + int(rng.integers(1, 7))       # other departments' samples take numbers too
        labno = "V%02d%06d" % (y % 100, seq[y])
        received = dt.datetime.combine(x["sample_date"], dt.time(0, 0)) + dt.timedelta(
            days=int(rng.integers(0, 3)), hours=int(rng.integers(8, 19)), minutes=int(rng.integers(0, 60)))
        auth = received.date() + dt.timedelta(days=int(rng.integers(1, 6 if x["test"] == "AB" else 9)))
        locs = REQ_LOC[x["requester"]]
        loc, rtype = locs[int(rng.integers(0, len(locs)))]        # drawn for every row, so the stream stays put
        kept = _site(W.alias.get(x["pid"], x["pid"]), x["requester"], locs)
        if kept is not None:
            loc, rtype = kept
        new = x["sample_date"] >= D(2021, 3, 15)
        code = {"AB": "HCV-AB-EIA" if new else "HCVAB", "RNA": "HCV-RNA-VL" if new else "HCVPCR"}[x["test"]]
        if x["test"] == "AB":
            text, val = x["result"], ""
        else:
            if x["result"] == "Not detected":
                text, val = "Not detected", ""
            elif x["vl"] is not None and x["vl"] < 15:
                text, val = "Detected <15 IU/mL", ""
            else:
                text, val = "Detected", "%d" % int(round(x["vl"]))
        p = W.people[x["pid"]]
        if x.get("skip"):
            continue
        out.append([labno, lims[W.alias.get(x["pid"], x["pid"])], x["pid"], p["sex"], p["birth_year"],
                    _iso(x["sample_date"]),
                    received.strftime("%Y-%m-%d %H:%M"), _iso(auth), loc, rtype, code, text, val])
    # the new system re-sent its first fortnight of authorised results a second time
    resent = [r for r in out if D(2021, 3, 15) <= D.fromisoformat(r[5]) <= D(2021, 3, 29)]
    out = out + resent
    out.sort(key=lambda r: (r[5], r[0]))
    _w(path, ["lab_number", "lims_patient_id", "pseudonym", "sex", "year_of_birth", "sample_taken", "received",
              "authorised",
              "requesting_location", "location_type", "test_code", "result", "viral_load_iu_ml"], out)
    return len(out)


def register(W, path, rng):
    rows = sorted(W.register, key=lambda c: (c["start"], c["pid"]))
    out = []
    seq = {}
    arrival_people = {a["pid"] for a in W.arrivals}
    last_test = {}
    for t in W.peer:
        if t["result"] == "Reactive":
            last_test[t["pid"]] = max(t["test_date"], last_test.get(t["pid"], t["test_date"]))
    ncourse = {}
    for c in rows:
        ncourse[c["pid"]] = ncourse.get(c["pid"], 0) + 1
    for c in rows:
        y = c["start"].year
        seq[y] = seq.get(y, 0) + 1
        ref = "FHC-%d-%04d" % (y, seq[y] * 3 + int(rng.integers(0, 3)))
        svr_d, svr_r = c["svr_date"], c["svr_result"]
        if c["outcome"] in ("Completed", "Stopped") and svr_r is None:
            svr_r = "Not done"
        # since the clinical system went live, the twelve-week result is keyed by hand and is often left blank
        if svr_d is not None and svr_d >= P.EPR_GO_LIVE:
            c["keyed"] = rng.random() < P.SVR_KEYED_SINCE_GOLIVE and not c.get("retired")
            if c["pid"] in last_test and c["start"] < last_test[c["pid"]]:
                c["keyed"] = True     # the setting arrivals' own courses before their test were keyed
            if not c["keyed"]:
                svr_d, svr_r = None, None
            if svr_d is not None and svr_d > P.AS_OF:
                svr_d, svr_r = None, None
        if svr_d is not None and svr_d > P.AS_OF:
            svr_d, svr_r = None, None
        if c["svr_date"] is not None and c["svr_date"] > P.AS_OF and c["svr_result"] is not None:
            svr_d, svr_r = None, None
        if c.get("untested") and svr_r is not None:
            svr_d, svr_r = None, "Not done"
        stopped = c["stopped"]
        outcome = c["outcome"]
        if c["planned_end"] > P.AS_OF and outcome == "Completed":
            outcome = "On treatment"
        c["ref"] = ref
        pid = c["pid"]
        if c["start"] > P.AS_OF:
            continue
        out.append([ref, pid, c["clinic"], c["route"], _iso(c["start"]), c["regimen"], c["weeks"],
                    _iso(c["planned_end"]), outcome, _iso(stopped), _iso(svr_d), svr_r or ""])
    _w(path, ["course_ref", "pseudonym", "clinic_code", "referral_route", "start_date",
              "regimen", "planned_weeks", "planned_end", "outcome", "stopped_on", "svr12_date", "svr12_result"], out)
    return len(out)


def prison(W, path, rng):
    wb = Workbook()
    ws1 = wb.active
    ws1.title = "Courses 2017-20"
    ws2 = wb.create_sheet("Courses 2021-26")
    h1 = ["Establishment", "NOMS no.", "Pseudo ID", "Start", "Drug", "Wks", "End", "Released in course",
          "SVR12 (date)", "SVR12"]
    h2 = ["Site", "Prison number", "Pseudonym", "Course start", "Regimen", "Planned weeks", "Course end",
          "Released before end", "Release date", "SVR12 date", "SVR12 result"]
    for ws, h in ((ws1, h1), (ws2, h2)):
        ws.append(h)
        for c in ws[1]:
            c.font = Font(bold=True)
    for c in sorted(W.prison, key=lambda c: (c["start"], c["prison"])):
        if c["start"] > P.AS_OF:
            continue
        svr_d, svr_r = c["svr_date"], c["svr_result"]
        rel = c["release"] if c["release"] is not None and c["release"] <= P.AS_OF else None
        released = bool(c["released_mid"]) and (rel is not None or c["start"].year <= 2020)
        if svr_d is not None and svr_d > P.AS_OF:
            svr_d, svr_r = None, None
        if svr_r is None and c["end"] + dt.timedelta(days=150) <= P.AS_OF:
            svr_r = "Not done"
        if c["start"].year <= 2020:
            ws1.append([P.PRISONS[c["prison"]], c["prisoner_no"], c["pid"], _dmy(c["start"]),
                        c["regimen"].replace("/", " + "), c["weeks"], _dmy(c["end"]),
                        "Y" if released else "N", _dmy(svr_d), svr_r or ""])
        else:
            ws2.append([P.PRISONS[c["prison"]].replace("HMP ", ""), c["prisoner_no"], c["pid"], c["start"],
                        c["regimen"], c["weeks"], c["end"], "Yes" if released else "No",
                        rel, svr_d, svr_r or ""])
    ws3 = wb.create_sheet("Reception BBV positives")
    ws3.append(["Site", "Prison number", "Pseudonym", "Reception test date", "HCV antibody", "HCV RNA"])
    for c in ws3[1]:
        c.font = Font(bold=True)
    for t in sorted(W.prison_tests, key=lambda t: (t["test_date"], t["prison"], t["prisoner_no"])):
        ws3.append([P.PRISONS[t["prison"]].replace("HMP ", ""), t["prisoner_no"], t["pid"], t["test_date"],
                    t["ab"], t["rna"]])
    for ws, cols in ((ws2, "DGIJ"), (ws3, "D")):
        for col in cols:
            for cell in ws[col][1:]:
                if cell.value is not None:
                    cell.number_format = "dd/mm/yyyy"
    for ws in (ws1, ws2, ws3):
        for col, wdt in zip("ABCDEFGHIJK", (16, 12, 14, 12, 26, 9, 12, 12, 12, 12, 13)):
            ws.column_dimensions[col].width = wdt
    wb.save(path)
    postprocess.scrub(path, P.PRISON_PROVIDER, "2026-10-05")
    postprocess.finish_office(path, "2017-04-03T09:12:00Z", "2026-10-05T15:41:00Z", P.PRISON_PROVIDER,
                              person="HCV lead nurse, Corvane Health")


SETTING_WRITTEN = {
    "AP": ["Approved Premises", "AP - Kimble House", "AP Orchard Street", "Approved premises (Linnet Rd)",
           "Probation accommodation", "CAS3 house"],
    "HH": ["Hostel", "Weaver House", "St Anselm's", "Brook Lodge hostel", "Castle Mews", "The Foyer"],
    "DS": ["Fenwold Recovery", "FR Fenwold hub", "FR Corrington", "Fenwold Recovery - Sallowby", "FR new entrant"],
    "NSP": ["NSP pharmacy", "Needle exchange", "Pharmacy NSP", "NX - Market St Pharmacy", "NSP (Boots Corrington)"],
}
OTHER_VENUES = ["Hope Street day centre", "Fenwold food bank", "Corrington Methodist hall", "Street outreach",
                "Sex worker drop-in", "Sallowby community centre", "Mosque health day", "Recovery cafe"]


def peer(W, path, rng):
    rows = []
    for t in W.peer:
        written = SETTING_WRITTEN[t["setting"]][int(rng.integers(0, len(SETTING_WRITTEN[t["setting"]])))]
        res = t["result"]
        lot = "OQ%d%02d%s" % (t["test_date"].year % 100, int(rng.integers(1, 13)), "ABCDEFGH"[int(rng.integers(0, 8))])
        if rng.random() < 0.012:      # an invalid kit, tested again with a second kit the same visit
            rows.append([t["test_date"], written, t["pid"], lot, "Invalid", ""])
        rows.append([t["test_date"], written, t["pid"], lot, res, "Yes" if res == "Reactive" else ""])
    # tests the team ran at its other venues (people not arriving in the four settings)
    n_other = int(len(W.peer) * 0.62)
    for _ in range(n_other):
        when = D.fromordinal(int(rng.integers(P.POOL_START.toordinal(), P.AS_OF.toordinal() + 1)))
        pid = W.person()
        pos = rng.random() < 0.11
        venue = OTHER_VENUES[int(rng.integers(0, len(OTHER_VENUES)))]
        anon = rng.random() < 0.18
        lot = "OQ%d%02d%s" % (when.year % 100, int(rng.integers(1, 13)), "ABCDEFGH"[int(rng.integers(0, 8))])
        rows.append([when, venue, "" if anon else pid, lot, "Reactive" if pos else "Non-reactive",
                     "Yes" if pos else ""])
    rows.sort(key=lambda r: (r[0], r[1], r[2]))
    out = []
    used = set()
    for i, r in enumerate(rows):
        while True:
            tid = "PT%s-%05d" % (r[0].strftime("%y%m"), int(rng.integers(100, 99999)))
            if tid not in used:
                used.add(tid)
                break
        out.append([tid, _iso(r[0])] + r[1:])
    _w(path, ["test_id", "test_date", "setting_or_venue", "pseudonym", "kit_lot", "result", "referred"], out)
    return len(out)


PROVIDER = {"AP": "National Probation Service (approved premises and CAS3)", "HH": "Fenwold supported housing",
            "DS": "Fenwold Recovery", "NSP": "Fenwold pharmacy needle and syringe programme"}


def arrivals(W, path, rng):
    rows = sorted(W.arrivals, key=lambda a: (a["setting"], a["arrival_date"], a["pid"]))
    out = []
    for a in rows:
        d = a["arrival_date"]
        ds = _dmy(d) if a["setting"] == "HH" else _iso(d)
        ref = "%s%s%04d" % (a["setting"], d.strftime("%y%m"), int(rng.integers(0, 10000)))
        out.append([a["setting"], PROVIDER[a["setting"]], a["pid"], ds, ref])
    _w(path, ["setting", "provider_return", "pseudonym", "arrival_date", "stay_ref"], out)
    return len(out)


def pilot(W, path, rng):
    site = {"HOPE": "Hope Street day centre", "CORR": "Corrington methadone clinic"}
    out = []
    for p in sorted(W.pilot, key=lambda p: (p["site"], p["arrival"], p["pid"])):
        out.append([site[p["site"]], p["pid"], _iso(p["arrival"]), "Y" if p["tested"] else "N", _iso(p["test_date"]),
                    p["ab"] or "", p["rna"] or "", "Y" if p["started"] else "N", _iso(p["start_date"])])
    _w(path, ["pilot_site", "pseudonym", "arrived", "tested_by_van", "test_date", "antibody", "rna",
              "treatment_started", "start_date"], out)
    return len(out)


def clinics(path):
    rows = [["HEP", "Hospital hepatology clinic", "Fenwold General Hospital", "Hospital"],
            ["COMM", "Community hepatitis clinic", "Ashgrove Health Centre, Fenwold", "Community"],
            ["FRC", "Fenwold Recovery clinic", "Fenwold Recovery hubs (Fenwold, Corrington, Sallowby)", "Drug service"],
            ["PHARM", "Pharmacy-led clinic", "Six community pharmacies", "Pharmacy"],
            ["OUT", "Outreach nurse clinic", "Brannock Trust venues and street outreach", "Outreach"]]
    _w(path, ["clinic_code", "clinic", "where_it_runs", "clinic_type"], rows)


def nsp_activity(W, path, rng):
    pharmacies = ["Market St Pharmacy", "Boots Corrington", "Lloyds Sallowby", "Hale Road Chemist",
                  "Westgate Pharmacy", "Rowan Pharmacy", "Station Pharmacy", "Kelsey Chemist", "Northfield Pharmacy",
                  "Abbey Pharmacy", "Quay Street Pharmacy", "Cross Lane Chemist"]
    out = []
    d = D(2025, 4, 7)
    while d <= P.AS_OF:
        for ph in pharmacies:
            base = rng.integers(4, 40)
            out.append([d.isoformat(), ph, int(base), int(rng.integers(0, base + 1)), int(rng.poisson(base * 0.9)),
                        int(rng.integers(0, 3))])
        d += dt.timedelta(days=7)
    _w(path, ["week_beginning", "pharmacy", "transactions", "packs_1ml", "packs_returned", "new_registrations_paper"],
       out)


def fibroscan(W, path, rng):
    wb = Workbook()
    ws = wb.active
    ws.title = "Sessions"
    ws.append(["Session date", "Venue", "Scans", "Median kPa", "Scans >=12.5 kPa", "Operator"])
    for c in ws[1]:
        c.font = Font(bold=True)
    venues = ["Fenwold General hepatology", "Ashgrove Health Centre", "FR Fenwold hub", "FR Corrington", "Van (pilot day)"]
    d = D(2025, 4, 2)
    while d <= P.AS_OF:
        for v in venues[:4]:
            if rng.random() < 0.55:
                n = int(rng.integers(3, 16))
                ws.append([d.strftime("%d/%m/%Y"), v, n, round(float(rng.normal(6.8, 1.6)), 1),
                           int(rng.binomial(n, 0.12)), ["CS", "JT", "MW", "RH"][int(rng.integers(0, 4))]])
        d += dt.timedelta(days=7)
    wb.save(path)
    postprocess.scrub(path, P.NETWORK, "2026-10-01")
    postprocess.finish_office(path, "2025-04-02T08:30:00Z", "2026-10-01T16:02:00Z", P.NETWORK,
                              person="Liver assessment service")


def merges(W, rng):
    """people the national spine found holding two NHS numbers: Fenwold Pathology holds their samples under both,
    joined by its own patient record, and the network's register carries the one number its clinical system holds.
    For the courses picked here the twelve-week sample, and any later RNA test, went in under the other number."""
    arrival_people = {a["pid"] for a in W.arrivals}
    n = defaultdict(int)
    for c in W.register:
        n[c["pid"]] += 1
    cand = defaultdict(list)
    for c in W.register:
        last = c["stopped"] or c["planned_end"]
        if (c["pid"] not in arrival_people and n[c["pid"]] == 1 and P.EPR_GO_LIVE <= last <= D(2025, 9, 30)
                and c["outcome"] in ("Completed", "Stopped") and c.get("true_cure")):
            h = 1 if last <= D(2025, 3, 31) else 2
            cand[(c["clinic"], h)].append(c)
    chosen = []
    for key in sorted(cand):
        cs = sorted(cand[key], key=lambda c: (c["start"], c["pid"]))
        pick = [cs[int(rng.integers(0, len(cs)))]]
        pick += [c for c in cs if c is not pick[0] and rng.random() < 0.10]
        chosen += pick
    moved = {}
    for c in chosen:
        retired = W.pid()
        c["retired"] = retired
        moved[c["pid"]] = ((c["stopped"] or c["planned_end"]) + dt.timedelta(days=56), retired)
    # the same two-number history on people whose courses ended well before the window (its own stream, so no other
    # draw moves)
    r2 = np.random.default_rng(P.SEED + 11)
    early = [c for c in sorted(W.register, key=lambda c: (c["start"], c["pid"]))
             if c["pid"] not in arrival_people and n[c["pid"]] == 1 and c["outcome"] in ("Completed", "Stopped")
             and c["svr_result"] is not None
             and (c["stopped"] or c["planned_end"]) < P.EPR_GO_LIVE - dt.timedelta(days=200)]
    for c in early:
        if r2.random() < P.TWO_NUMBER_SHARE:
            moved[c["pid"]] = ((c["stopped"] or c["planned_end"]) + dt.timedelta(days=56), W.pid())
    # courses whose twelve-week test was never taken (lost to follow-up after the course), across every year, on
    # people outside the settings (its own stream)
    r3 = np.random.default_rng(P.SEED + 13)
    drop = set()
    for c in sorted(W.register, key=lambda c: (c["start"], c["pid"])):
        if (c["pid"] not in arrival_people and c["pid"] not in moved and c["outcome"] in ("Completed", "Stopped")
                and c["svr_result"] is not None and r3.random() < P.UNTESTED_SHARE):
            c["untested"] = True
            drop.add((c["pid"], c["svr_date"]))
    # a course lost to follow-up: the person was not seen again by the clinic, and no RNA test follows the course
    gone = {}
    for c in W.register:
        if (c["outcome"] == "Lost to follow-up" and c["pid"] not in arrival_people and c["pid"] not in moved
                and n[c["pid"]] == 1):
            c["untested"] = True
            gone[c["pid"]] = c["planned_end"]
    W.lab = [x for x in W.lab if not (x["test"] == "RNA" and (x["pid"], x["sample_date"]) in drop)]
    for x in W.lab:
        if x["test"] == "RNA" and x["pid"] in gone and x["sample_date"] > gone[x["pid"]]:
            x["skip"] = True      # not written; the writer still draws for it, so no other file moves
    for x in W.lab:
        m = moved.get(x["pid"])
        if m and x["test"] == "RNA" and x["sample_date"] >= m[0]:
            x["pid"] = m[1]
    W.alias = {}
    for pid, (d, other) in moved.items():
        W.people[other] = dict(sex=W.people[pid]["sex"], birth_year=W.people[pid]["birth_year"])
        W.alias[other] = pid
    return len(chosen)


def lims_ids(W):
    """Fenwold Pathology's own patient number for every person with a sample, one per person, the same for both of a
    person's NHS-number pseudonyms"""
    people = sorted({W.alias.get(x["pid"], x["pid"]) for x in W.lab})
    out, used = {}, set()
    for p in people:
        k = 0
        while True:
            h = hashlib.sha256(("lims-%d-%s-%d" % (P.SEED, p, k)).encode()).hexdigest()
            v = "P%08d" % (int(h[:12], 16) % 10 ** 8)
            if v not in used:
                break
            k += 1
        used.add(v)
        out[p] = v
    return out


def write_all(W, target):
    rng = np.random.default_rng(P.SEED + 7)
    f = P.FILES
    n = {}
    n["merges"] = merges(W, rng)
    n["lab"] = lab(W, os.path.join(target, f["lab"]), rng)
    n["register"] = register(W, os.path.join(target, f["register"]), rng)
    prison(W, os.path.join(target, f["prison"]), rng)
    n["peer"] = peer(W, os.path.join(target, f["peer"]), rng)
    n["arrivals"] = arrivals(W, os.path.join(target, f["arrivals"]), rng)
    n["pilot"] = pilot(W, os.path.join(target, f["pilot"]), rng)
    clinics(os.path.join(target, f["clinics"]))
    nsp_activity(W, os.path.join(target, f["nsp_activity"]), rng)
    fibroscan(W, os.path.join(target, f["fibroscan"]), rng)
    return n
