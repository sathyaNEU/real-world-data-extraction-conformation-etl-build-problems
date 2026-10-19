"""The exports the trust's systems write from the clean truth: the old clinical information system's ACE-III forms and
diagnoses (to 5 January 2024), the electronic patient record's cognitive observations, problem list, episodes and
outpatient appointments (from 8 January 2024), the master patient index, the Memory Assessment Service's pathway
tracker, the clinic register, last year's service audit and the planning team's catchment populations.

Everything random here draws from streams of its own, so the world's draws never move."""
import csv
import datetime as dt
import numpy as np
import common as K
import world as W

GO = K.EPR_GO_LIVE
EXTRACT = K.EXTRACT
END = K.WINDOW[1]
ROLES_CIS = ["Nurse specialist", "Specialty doctor", "Consultant psychiatrist", "Assistant psychologist"]
ROLES_EPR = ["Memory nurse specialist", "Specialty doctor", "Consultant psychiatrist", "Assistant psychologist"]
ITEMS = [("ACE3_ATT", 0), ("ACE3_MEM", 1), ("ACE3_FLU", 2), ("ACE3_LAN", 3), ("ACE3_VIS", 4)]


def stream(seed, k):
    return np.random.default_rng([seed, 7000 + k])


def bst(d):
    """British Summer Time: last Sunday of March to last Sunday of October."""
    def last_sunday(y, m):
        x = dt.date(y, m, 31)
        return x - dt.timedelta(days=(x.weekday() + 1) % 7)
    return last_sunday(d.year, 3) <= d < last_sunday(d.year, 10)


def stamp(d, minutes):
    off = "+01:00" if bst(d) else "+00:00"
    return "%sT%02d:%02d:00%s" % (d.isoformat(), minutes // 60, minutes % 60, off)


def ddmmyyyy(d):
    return d.strftime("%d/%m/%Y")


def workdays_after(d, n):
    for _ in range(n):
        d = W.weekday(d + dt.timedelta(days=1))
    return d


def write_csv(path, header, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


# ------------------------------------------------------------------ the derived record of each patient
def derive(w):
    """Admin dates, appointment bookings, set identifiers and the rest the exports need, from their own streams."""
    seed = w["seed"]
    rng = stream(seed, 1)
    pats = w["patients"]
    by_clinic_day = {}
    for p in pats:
        for i, s in enumerate(p["sittings"]):
            by_clinic_day.setdefault((s["clinic"], s["date"]), []).append((p["pid"], i))
    for p in pats:
        r = np.random.default_rng([seed, 31, p["pid"]])
        # episodes: when the record was closed on the system
        for ep in p["episodes"]:
            if ep["end"] is None:
                ep["closed_on"] = None
                continue
            reason = ep["reason"]
            if reason == "Died":
                lag = int(r.integers(5, 61))
                ep["closed_on"] = W.weekday(ep["end"] + dt.timedelta(days=lag))
            elif reason.startswith("Transferred"):
                ep["closed_on"] = ep["end"]
            elif reason.startswith("Care passed"):
                ep["closed_on"] = workdays_after(ep["end"], int(min(60, 4 + r.geometric(0.055))))
            elif reason == "Moved out of area":
                ep["closed_on"] = W.weekday(ep["end"] + dt.timedelta(days=int(r.integers(0, 11))))
            else:
                # a discharge is closed when the discharge letter goes, a few days to some weeks on
                ep["closed_on"] = workdays_after(ep["end"], int(min(60, 4 + r.geometric(0.055))))
        # sittings: identifiers and the role who gave the test
        for s in p["sittings"]:
            s["minutes"] = int(r.choice([9 * 60, 9 * 60 + 30, 10 * 60 + 15, 11 * 60, 13 * 60 + 45, 14 * 60 + 30,
                                         15 * 60 + 15]))
            s["role"] = int(r.choice(4, p=[0.55, 0.2, 0.1, 0.15]))
            s["hpn_used"] = p["hpn"]
            if p["hpn2"] and s["date"] < GO and r.random() < 0.4:
                s["hpn_used"] = p["hpn2"]
        # the care home liaison team also advises on patients who stay under the clinic
        if p["typ"] in ("AD", "MCI") and p["sittings"] and r.random() < 0.05:
            d0 = p["sittings"][-1]["date"]
            d1 = min(p["episodes"][-1]["end"] or END, END)
            if d0 >= GO and (d1 - d0).days > 20:
                p["events"].append(dict(kind="advice", date=W.weekday(d0 + dt.timedelta(days=int(r.integers(7, (d1 - d0).days)))),
                                        clinic=p["episodes"][-1]["clinic"]))
        # a stable patient discharged to the GP is often told at the review before
        revs = [e for e in p["events"] if e["kind"] == "review"]
        if len(revs) >= 2 and revs[-1].get("discharged") and p["episodes"][-1]["reason"] == "Discharged to GP" \
                and r.random() < 0.6:
            revs[-2]["planned"] = True
        # and a stable patient still under follow-up whose next review will be the last
        last_ep = p["episodes"][-1] if p["episodes"] else None
        if (revs and last_ep and last_ep["end"] is None and p.get("stable_at") and p["typ"] == "MCI"
                and not any(x["code"] != "MCI" for x in p["dx"]) and revs[-1]["date"] >= dt.date(2025, 10, 1)
                and p["stable_at"] <= revs[-1]["date"] + dt.timedelta(days=430) and r.random() < 0.6):
            revs[-1]["planned"] = True
        # appointments in the electronic record's time
        appts = []
        for ev in p["events"]:
            d = ev["date"]
            if d < GO:
                continue
            kind = ev["kind"]
            if kind == "assessment":
                typ, dur = "New patient assessment", 90
                out = "Attended - diagnosis given" if ev.get("dx_given") else "Attended"
            elif kind == "feedback":
                typ, dur, out = "Diagnosis feedback", 45, "Attended - diagnosis given"
            elif kind == "discharge_at_feedback":
                continue
            elif kind == "nurse_call":
                typ, dur, out = "Medication review (telephone)", 20, "Attended"
            elif kind == "handover":
                typ, dur, out = "Care home liaison (telephone)", 30, "Attended - care passed to care home liaison team"
            elif kind == "advice":
                typ, dur, out = "Care home liaison (telephone)", 30, "Attended - advice given, memory clinic follow-up continues"
            else:
                typ, dur = "Memory review", 60
                out = "Attended - discharged from service" if ev.get("discharged") else "Attended"
                if ev.get("planned"):
                    out = "Attended - discharge planned at next review"
            if kind == "feedback" and any(e["kind"] == "discharge_at_feedback" for e in p["events"]):
                out = "Attended - diagnosis given, discharged from service"
            # an earlier booking the patient missed or cancelled
            if kind in ("feedback", "review", "assessment") and r.random() < 0.13:
                pre = W.weekday(d - dt.timedelta(days=int(r.integers(14, 43))))
                if pre >= GO:
                    o = "Did not attend" if r.random() < 0.55 else ("Cancelled by patient" if r.random() < 0.6
                                                                   else "Cancelled by service")
                    appts.append(dict(date=pre, type=typ, dur=dur, outcome=o, clinic=ev["clinic"],
                                      booked=pre - dt.timedelta(days=int(r.integers(20, 70)))))
            appts.append(dict(date=d, type=typ, dur=dur, outcome=out, clinic=ev["clinic"],
                              booked=d - dt.timedelta(days=int(r.integers(14, 80))), ev=ev))
        # the next review, booked ahead, for a patient still under follow-up at the extract
        last = p["episodes"][-1] if p["episodes"] else None
        if last and last["end"] is None and p.get("first") and p["typ"] not in ("NOD", "DEP"):
            reviews = [e["date"] for e in p["events"] if e["kind"] in ("review", "assessment", "feedback")]
            nxt = W.weekday(max(reviews) + dt.timedelta(days=int(r.integers(300, 420))))
            if nxt > EXTRACT and nxt < dt.date(2027, 6, 30):
                appts.append(dict(date=nxt, type="Memory review", dur=60, outcome="", clinic=last["clinic"],
                                  booked=max(reviews) + dt.timedelta(days=int(r.integers(0, 20)))))
        for a in appts:
            a["minutes"] = int(r.choice([9 * 60, 9 * 60 + 30, 10 * 60 + 30, 11 * 60 + 15, 13 * 60 + 30, 14 * 60 + 15,
                                         15 * 60]))
            a["role"] = int(r.choice(4, p=[0.45, 0.25, 0.2, 0.1]))
            if a["type"] == "Medication review (telephone)":
                a["role"] = 0
            if a["booked"] >= a["date"]:
                a["booked"] = a["date"] - dt.timedelta(days=7)
        p["appts"] = sorted(appts, key=lambda a: (a["date"], a["minutes"]))
    number(w, stream(seed, 4))
    # a test entered on the wrong patient's record, then marked entered in error and entered again on the right one
    eie = []
    for p in pats:
        for i, s in enumerate(p["sittings"]):
            if s["date"] >= GO and rng.random() < 0.003:
                if rng.random() < 0.75:
                    slip = int(rng.choice([-3, -2, -1, 1, 2, 3]))
                    eie.append(dict(pid=p["pid"], of=p["pid"], sitting=i, slip=slip,
                                    obs_id="OBS-%08d" % (int(s["obs_id"][4:]) - 1)))
                    continue
                others = [q for q, j in by_clinic_day.get((s["clinic"], s["date"]), []) if q != p["pid"]]
                if not others:
                    others = [q["pid"] for q in pats[max(0, p["pid"] - 40):p["pid"] + 40]
                              if q["pid"] != p["pid"] and q["sittings"]]
                wrong = others[int(rng.integers(0, len(others)))]
                eie.append(dict(pid=wrong, of=p["pid"], sitting=i, slip=0,
                                obs_id="OBS-%08d" % (int(s["obs_id"][4:]) - 1)))
    w["eie"] = eie
    return w


def number(w, r):
    """Identifiers as the systems hand them out: in the order things were recorded."""
    pats = w["patients"]
    forms = sorted(((s["date"], s["minutes"], p["pid"], i) for p in pats for i, s in enumerate(p["sittings"])
                    if s["date"] < GO))
    n = 300017
    for d, m, pid, i in forms:
        n += int(r.integers(1, 4))
        pats[pid]["sittings"][i]["form_id"] = "CIS-ACE-%06d" % n
    sets = sorted(((s["date"], s["minutes"], p["pid"], i) for p in pats for i, s in enumerate(p["sittings"])
                   if s["date"] >= GO))
    n = 40011237
    for d, m, pid, i in sets:
        n += int(r.integers(2, 9))          # a set entered on the wrong record takes the number before its own
        pats[pid]["sittings"][i]["obs_id"] = "OBS-%08d" % n
    eps = sorted(((ep["start"], p["pid"], j) for p in pats for j, ep in enumerate(p["episodes"])))
    n = 5000031
    for d, pid, j in eps:
        n += int(r.integers(1, 4))
        pats[pid]["episodes"][j]["id"] = "EP%08d" % n
    apps = sorted(((a["booked"], a["date"], p["pid"], j) for p in pats for j, a in enumerate(p["appts"])))
    n = 210004518
    for b, d, pid, j in apps:
        n += int(r.integers(1, 6))
        pats[pid]["appts"][j]["id"] = "APT%09d" % n
    paths = sorted(((p["registered"], p["pid"]) for p in pats))
    n = 880112
    for d, pid in paths:
        n += int(r.integers(1, 3))
        pats[pid]["pathway_id"] = "MAS-%07d" % n


# ------------------------------------------------------------------ the master patient index
def nhs_fmt(n, r):
    return "%s %s %s" % (n[:3], n[3:6], n[6:]) if r.random() < 0.03 else n


def postcode(p, r):
    last = p["episodes"][-1] if p["episodes"] else None
    if last and last.get("reason") == "Moved out of area":
        return "BM%d" % int(r.integers(2, 15))
    clinic = last["clinic"] if last else p["clinic0"]
    if last and last.get("reason", "") and last["reason"].startswith("Transferred"):
        clinic = last["reason"].split(" to ")[1]
    ds = K.DISTRICTS[clinic]
    if clinic == p["clinic0"]:
        return p["district"]
    return ds[int(r.integers(0, len(ds)))]


def write_pmi(path, w):
    r = stream(w["seed"], 2)
    rows = []
    for p in w["patients"]:
        death = p["death"].isoformat() if (p["death"] and p["death"] <= EXTRACT) else ""
        pc = postcode(p, r)
        rows.append((p["hpn"], nhs_fmt(p["nhs"], r), p["dob"].isoformat(), p["sex"], pc, death, "Active"))
        if p["hpn2"]:
            rows.append((p["hpn2"], nhs_fmt(p["nhs"], r), p["dob"].isoformat(), p["sex"], pc, death,
                         "Merged into %s" % p["hpn"]))
    rows.sort(key=lambda x: x[0])
    return write_csv(path, ["hpn", "nhs_number", "date_of_birth", "sex", "postcode_district", "date_of_death",
                            "record_status"], rows)


# ------------------------------------------------------------------ the old system
def write_cis_ace(path, w):
    r = stream(w["seed"], 3)
    rows = []
    for p in w["patients"]:
        for s in p["sittings"]:
            if s["date"] >= GO:
                continue
            doms = ["" if x is None else x for x in s["domains"]]
            hpn = s["hpn_used"] + (" " if r.random() < 0.004 else "")
            rows.append((s["form_id"], hpn, K.CIS_CODE[s["clinic"]], ddmmyyyy(s["date"]), ROLES_CIS[s["role"]],
                         "C" if s["completed"] else "A", *doms, s["total"]))
    rows.sort(key=lambda x: x[0])
    return write_csv(path, ["form_id", "hpn", "clinic_code", "assessment_date", "administered_by", "form_status",
                            "attention", "memory", "fluency", "language", "visuospatial", "total"], rows)


def write_cis_dx(path, w):
    rows = []
    for p in w["patients"]:
        for x in p["dx"]:
            if x["entered"] >= GO:
                continue
            code, desc = K.DX[x["code"]]
            rows.append((p["hpn"], ddmmyyyy(x["entered"]), code, desc, x["status"], K.CIS_CODE[x["clinic"]]))
    rows.sort(key=lambda x: (x[0], dt.datetime.strptime(x[1], "%d/%m/%Y")))
    return write_csv(path, ["hpn", "diagnosis_date", "icd10_code", "diagnosis", "diagnosis_status", "clinic_code"],
                     rows)


# ------------------------------------------------------------------ the electronic patient record
def write_epr_obs(path, w):
    rows = []
    pats = w["patients"]
    eie_by = {}
    for e in w["eie"]:
        eie_by.setdefault(e["pid"], []).append(e)
    for p in pats:
        for s in p["sittings"]:
            if s["date"] < GO:
                continue
            when = stamp(s["date"], s["minutes"])
            status = "Final" if s["completed"] else "Incomplete"
            for code, i in ITEMS:
                if s["domains"][i] is None:
                    continue
                rows.append((s["obs_id"], p["nhs"], K.SITE[s["clinic"]], when, code, s["domains"][i], status,
                             ROLES_EPR[s["role"]]))
            rows.append((s["obs_id"], p["nhs"], K.SITE[s["clinic"]], when, "ACE3_TOTAL", s["total"], status,
                         ROLES_EPR[s["role"]]))
        for e in eie_by.get(p["pid"], []):
            src = pats[e["of"]]["sittings"][e["sitting"]]
            when = stamp(src["date"], src["minutes"])
            doms = list(src["domains"])
            if e["slip"]:
                j = 1 if doms[1] is not None else 0
                doms[j] = int(min(max(0, doms[j] + e["slip"]), K.DOMAINS[j][2]))
            for code, i in ITEMS:
                if doms[i] is None:
                    continue
                rows.append((e["obs_id"], p["nhs"], K.SITE[src["clinic"]], when, code, doms[i],
                             "Entered in error", ROLES_EPR[src["role"]]))
            rows.append((e["obs_id"], p["nhs"], K.SITE[src["clinic"]], when, "ACE3_TOTAL",
                         int(sum(x for x in doms if x is not None)), "Entered in error", ROLES_EPR[src["role"]]))
    order = {c: i for i, (c, _) in enumerate(ITEMS + [("ACE3_TOTAL", 5)])}
    rows.sort(key=lambda x: (x[3][:10], x[0], order[x[4]]))
    return write_csv(path, ["obs_set_id", "nhs_number", "site_code", "performed_at", "item_code", "value",
                            "set_status", "entered_by_role"], rows)


def migrated_dx(p):
    """The diagnosis copied onto the new record for a patient still under the service at go-live."""
    open_at_go = any(ep["start"] < GO and (ep["end"] is None or ep["end"] >= GO) for ep in p["episodes"])
    before = [x for x in p["dx"] if x["entered"] < GO]
    if not open_at_go or not before:
        return None
    return max(before, key=lambda x: (x["entered"], x["given"]))


def write_epr_dx(path, w):
    rows = []
    for p in w["patients"]:
        entries = []
        m = migrated_dx(p)
        if m:
            entries.append((GO, m["code"], "CIS migration"))
        for x in p["dx"]:
            if GO <= x["entered"] <= EXTRACT:
                entries.append((x["entered"], x["code"], "EPR"))
        entries.sort(key=lambda e: e[0])
        for i, (d, code, src) in enumerate(entries):
            c, desc = K.DX[code]
            status = "Active" if i == len(entries) - 1 else "Inactive"
            rows.append((p["nhs"], c, desc, d.isoformat(), status, src))
    rows.sort(key=lambda x: (x[3], x[0]))
    return write_csv(path, ["nhs_number", "problem_code", "problem_description", "recorded_on", "problem_status",
                            "source"], rows)


def write_episodes(path, w):
    rows = []
    for p in w["patients"]:
        for ep in p["episodes"]:
            if ep["end"] is not None and ep["end"] < GO:
                continue
            if ep["start"] > EXTRACT:
                continue
            closed = ep["closed_on"] is not None and ep["closed_on"] <= EXTRACT
            rows.append((ep["id"], p["nhs"], K.SITE[ep["clinic"]], ep["start"].isoformat(),
                         ep["end"].isoformat() if closed else "", ep["reason"] if closed else "",
                         "Y" if ep["start"] < GO else "N"))
    rows.sort(key=lambda x: x[0])
    return write_csv(path, ["episode_id", "nhs_number", "site_code", "episode_start", "episode_end", "end_reason",
                            "migrated_from_cis"], rows)


def write_appointments(path, w):
    rows = []
    for p in w["patients"]:
        for a in p["appts"]:
            if a["booked"] > EXTRACT:
                continue
            rows.append((a["id"], p["nhs"], K.SITE[a["clinic"]], a["type"], ROLES_EPR[a["role"]],
                         a["booked"].isoformat(), stamp(a["date"], a["minutes"]), a["dur"],
                         a["outcome"] if a["date"] <= EXTRACT else ""))
    rows.sort(key=lambda x: (x[6][:10], x[0]))
    return write_csv(path, ["appointment_id", "nhs_number", "site_code", "appointment_type", "clinician_role",
                            "booked_on", "appointment_start", "duration_min", "outcome"], rows)


# ------------------------------------------------------------------ the service's pathway tracker
def tracker_rows(w):
    rows = []
    for p in w["patients"]:
        reg = p["registered"]
        first = p.get("first")
        if reg < GO and not (first and first >= GO):
            continue
        dx0 = p["dx"][0] if p["dx"] else None
        diag = dx0 if (dx0 and dx0["entered"] <= EXTRACT) else None
        if first is None or first > EXTRACT:
            status = "Awaiting assessment"
        elif diag is None:
            status = "Assessed, awaiting diagnosis"
        else:
            status = "Diagnosed"
        rows.append(dict(pathway=p["pathway_id"], nhs=p["nhs"], clinic=p["clinic0"], referral=reg,
                         source=p["source"], first=first if (first and first <= EXTRACT) else None,
                         diagnosis_date=diag["entered"] if diag else None,
                         diagnosis=K.DX[diag["code"]][1] if diag else "", status=status))
    rows.sort(key=lambda x: x["pathway"])
    return rows


def write_tracker(path, w):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    rows = tracker_rows(w)
    wb = Workbook()
    ws = wb.active
    ws.title = "Pathways"
    head = ["Pathway ID", "NHS number", "Clinic", "Referral date", "Referral source", "First assessment",
            "Diagnosis date", "Diagnosis", "Pathway status"]
    ws.append(head)
    for c in ws[1]:
        c.font = Font(bold=True)
    for x in rows:
        ws.append([x["pathway"], x["nhs"], x["clinic"], x["referral"], x["source"], x["first"], x["diagnosis_date"],
                   x["diagnosis"] or None, x["status"]])
    for col in ("D", "F", "G"):
        for cell in ws[col][1:]:
            cell.number_format = "dd/mm/yyyy"
    widths = [13, 13, 13, 14, 26, 16, 14, 52, 28]
    for i, wdt in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = wdt
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = "A1:I%d" % (len(rows) + 1)
    notes = wb.create_sheet("Notes")
    for line in [
        ["Memory Assessment Service pathway tracker"],
        ["One row per referral accepted by a memory clinic since the service moved to the electronic patient "
         "record on 8 January 2024, with the referrals still waiting for a first assessment on that day."],
        ["Refreshed from the electronic patient record on %s." % EXTRACT.strftime("%d %B %Y").lstrip("0")],
        ["Maintained by the service's information team for the six-week referral to diagnosis standard."],
    ]:
        notes.append(line)
    notes.column_dimensions["A"].width = 120
    wb.save(path)
    return len(rows)


# ------------------------------------------------------------------ the clinic register, the audit, the populations
def write_clinics(path):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Clinics"
    ws.append(["Clinic", "CIS clinic code", "EPR site code", "First clinic held", "Base", "Consultant sessions a week",
               "Notes"])
    base = {"Thurlwick": "Thurlwick Health Centre", "Penwardine": "Penwardine Community Hospital",
            "Swinholt": "Swinholt Resource Centre", "Brindlemere": "Brindlemere Health Centre",
            "Ravensfold": "Ravensfold Clinic", "Corvale": "Corvale Community Hospital",
            "Mosswick": "Mosswick Primary Care Centre", "Quarndale": "Quarndale Health and Wellbeing Hub"}
    sess = {"Thurlwick": 4, "Penwardine": 4, "Swinholt": 3, "Brindlemere": 3, "Ravensfold": 3, "Corvale": 3,
            "Mosswick": 2, "Quarndale": 3}
    notes = {"Quarndale": "Opened 8 April 2024 for districts HL19 and HL20 (from Corvale), HL23 and HL24 (from "
                          "Mosswick) and HL25 to HL27 (commissioned from April 2024). Patients already under Corvale "
                          "or Mosswick stayed with those clinics.",
             "Corvale": "Districts HL19 and HL20 passed to Quarndale on 8 April 2024.",
             "Mosswick": "Districts HL23 and HL24 passed to Quarndale on 8 April 2024."}
    for nm, cis, site, opened in K.CLINICS:
        ws.append([nm, cis, site, opened, base[nm], sess[nm], notes.get(nm)])
    for c in ws[1]:
        c.font = Font(bold=True)
    for cell in ws["D"][1:]:
        cell.number_format = "dd/mm/yyyy"
    for col, wd in zip("ABCDEFG", (14, 15, 14, 16, 36, 12, 90)):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A2"
    ds = wb.create_sheet("Districts")
    ds.append(["Postcode district", "Clinic", "From", "To"])
    rows = []
    for nm, cis, site, opened in K.CLINICS:
        for d in K.DISTRICTS.get(nm, []):
            if nm == "Quarndale":
                rows.append((d, nm, K.OPENED["Quarndale"], None))
            elif nm in K.QUARNDALE_FROM and d in K.QUARNDALE_FROM[nm]:
                rows.append((d, nm, opened, K.OPENED["Quarndale"] - dt.timedelta(days=1)))
            else:
                rows.append((d, nm, opened, None))
    rows.sort(key=lambda r: (int(r[0][2:]), r[2]))
    for r in rows:
        ds.append(list(r))
    for c in ds[1]:
        c.font = Font(bold=True)
    for col in ("C", "D"):
        for cell in ds[col][1:]:
            cell.number_format = "dd/mm/yyyy"
    for col, wd in zip("ABCD", (16, 14, 12, 12)):
        ds.column_dimensions[col].width = wd
    ds.freeze_panes = "A2"
    wb.save(path)
    return len(K.CLINICS) + len(rows)


def under_follow_up(p, day):
    """The clinic following the patient on a day (the clean truth), or None."""
    if p["death"] and p["death"] <= day:
        return None
    for ep in p["episodes"]:
        if ep["start"] <= day and (ep["end"] is None or ep["end"] > day):
            return ep["clinic"]
    return None


def write_audit(path, w):
    """The service's 2024-25 audit for the commissioners: another year and other measures."""
    from openpyxl import Workbook
    from openpyxl.styles import Font
    a0, a1 = dt.date(2024, 4, 1), dt.date(2025, 3, 31)
    stats = {c: dict(ref=0, waits=[], appts=0, dna=0, dx=0, case=0) for c in K.NAMES}
    for p in w["patients"]:
        c0 = p["clinic0"]
        if a0 <= p["registered"] <= a1:
            stats[c0]["ref"] += 1
        if p.get("first") and a0 <= p["first"] <= a1:
            stats[c0]["waits"].append((p["first"] - p["registered"]).days / 7.0)
        for a in p.get("appts", []):
            if a0 <= a["date"] <= a1 and a["outcome"]:
                if a["outcome"].startswith("Cancelled"):
                    continue
                stats[a["clinic"]]["appts"] += 1
                stats[a["clinic"]]["dna"] += a["outcome"] == "Did not attend"
        if p["dx"] and a0 <= p["dx"][0]["given"] <= a1 and p["dx"][0]["code"] not in ("MCI", "NOD", "DEP"):
            stats[c0]["dx"] += 1
        c = under_follow_up(p, a1)
        if c:
            stats[c]["case"] += 1
    wb = Workbook()
    ws = wb.active
    ws.title = "Audit 2024-25"
    ws.append(["Memory Assessment Service: annual audit for the commissioners, 1 April 2024 to 31 March 2025"])
    ws.append([])
    head = ["Clinic", "Referrals accepted", "Median weeks, referral to first assessment",
            "Appointments not attended (%)", "New diagnoses of dementia", "Caseload, 31 March 2025"]
    ws.append(head)
    for c in K.NAMES:
        st = stats[c]
        med = float(np.median(st["waits"])) if st["waits"] else None
        ws.append([c, st["ref"], round(med, 1) if med is not None else None,
                   round(100.0 * st["dna"] / st["appts"], 1) if st["appts"] else None, st["dx"], st["case"]])
    for cell in ws[3]:
        cell.font = Font(bold=True)
    ws["A1"].font = Font(bold=True)
    for col, wd in zip("ABCDEF", (14, 12, 18, 16, 14, 14)):
        ws.column_dimensions[col].width = wd
    ws.append([])
    ws.append(["Quarndale's figures run from its opening on 8 April 2024. Dementia diagnoses exclude mild cognitive "
               "impairment. Prepared by the information team, May 2025."])
    wb.save(path)
    return len(K.NAMES)


def write_population(path, seed):
    r = stream(seed, 9)
    rows = []
    owner = {}
    for nm, ds in K.DISTRICTS.items():
        for d in ds:
            owner[d] = nm if nm == "Quarndale" or d not in K.QUARNDALE_FROM.get(nm, []) else "Quarndale"
    for d in sorted(owner, key=lambda x: int(x[2:])):
        p65 = int(r.integers(3800, 11200))
        p80 = int(p65 * r.uniform(0.24, 0.33))
        rows.append((d, owner[d], p65, p80))
    return write_csv(path, ["postcode_district", "memory_clinic", "residents_65_and_over", "residents_80_and_over"],
                     rows)
