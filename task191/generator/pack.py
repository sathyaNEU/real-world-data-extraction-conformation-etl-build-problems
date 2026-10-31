"""The pack: the files the platform's systems hold on the morning of 2 November 2026."""
import datetime as dt
import json
import os

import numpy as np
import openpyxl
from openpyxl.styles import Font

import common as C
import docs as D

FILES = {
    "alerts": "tm_alerts_2025-07_2026-10.csv",
    "cases": "fcm_cases_export_2026-11-02.json",
    "sars": "sar_filings_2025-07_2026-10.csv",
    "catalogue": "tm_scenario_catalogue_2026.xlsx",
    "runs": "tm_monitoring_runs_2025-07_2026-10.csv",
    "procedure": "aml_alert_handling_procedure_2026.pdf",
    "thread": "tuning_2027_thread.eml",
    "risk": "customer_risk_tiers_2026-10.csv",
    "capacity": "investigations_capacity_2027.xlsx",
    "qa": "qa_case_sampling_2026.csv",
}
DISTRACTORS = ("risk", "capacity", "qa")


def _status_at_extract(a, case):
    X = C.EXTRACT_UTC
    if a["triage_end"] > X:
        return "OPEN", None, None, None
    if a["triage"] == "DUP":
        return "CLOSED", a["triage_end"], "DUP", None
    if a["triage"] == "NSA":
        return "CLOSED", a["triage_end"], "NSA", None
    return "CLOSED", a["triage_end"], "ESC", a["case"]


def write_alerts(W, path):
    case = {c["case_id"]: c for c in W["cases"]}
    rows = []
    for a in sorted(W["alerts"], key=lambda a: (a["gen"], a["alert_id"])):
        if a["gen"] > C.EXTRACT_UTC or a["bdate"] < C.DATA0:
            continue
        st, closed, outcome, cid = _status_at_extract(a, case)
        rows.append([a["alert_id"], a["shown"], a["run_id"], C.iso_z(a["gen"]), a["customer"], a["account"], a["score"],
                     st, C.iso_z(closed) if closed else "", outcome or "", cid or ""])
    C.write_csv(path, ["alert_id", "scenario_code", "run_id", "created_at_utc", "customer_no", "account_no",
                       "alert_score", "triage_status", "triage_closed_at_utc", "triage_outcome", "case_id"], rows)
    return len(rows)


def write_cases(W, path):
    r = C.rng("case-events")
    X = C.EXTRACT_UTC
    alerts_of = {}
    for a in W["alerts"]:
        if a["case"] and a["triage_end"] <= X:
            alerts_of.setdefault(a["case"], []).append(a["alert_id"])
    teams = ["INV-East", "INV-Central", "INV-Merchant", "INV-Cross-border"]
    out = []
    for c in sorted(W["cases"], key=lambda c: (c["opened"], c["case_id"])):
        # the export holds every investigation open on 1 July 2025 or opened since
        if c["opened"] > X or c["case_id"] not in alerts_of or c["decided"] < C.DATA0_UTC:
            continue
        ev = [{"at": C.iso_z(c["opened"]), "event": "opened"}]
        t = c["opened"] + dt.timedelta(hours=float(r.uniform(2, 60)))
        ev.append({"at": C.iso_z(min(t, X)), "event": "assigned", "team": teams[int(r.integers(0, 4))]})
        span = (min(c["decided"], X) - c["opened"]).total_seconds()
        if span > 10 * 86400 and r.random() < 0.55:
            ev.append({"at": C.iso_z(c["opened"] + dt.timedelta(seconds=span * float(r.uniform(0.15, 0.45)))),
                       "event": "request_for_information"})
        done = c["decided"] <= X
        if c["outcome"] == "SAR":
            fiu = c["decided"] - dt.timedelta(days=float(r.uniform(18, 40)))
            if fiu <= X and fiu > c["opened"]:
                ev.append({"at": C.iso_z(fiu), "event": "referred_to_fiu"})
            qa = c["decided"] - dt.timedelta(days=float(r.uniform(2, 9)))
            if qa <= X and qa > c["opened"]:
                ev.append({"at": C.iso_z(qa), "event": "sar_quality_review"})
        if done:
            ev.append({"at": C.iso_z(c["decided"]), "event": "sar_filed" if c["outcome"] == "SAR" else "closed_no_sar"})
        ev.sort(key=lambda e: e["at"])
        out.append({"case_id": c["case_id"], "customer_no": c["customer"], "account_no": c["account"],
                    "opened_at": C.iso_z(c["opened"]), "alert_ids": sorted(alerts_of[c["case_id"]]),
                    "status": "CLOSED" if done else "OPEN",
                    "disposition": ("SAR filed" if c["outcome"] == "SAR" else "No SAR") if done else None,
                    "decided_at": C.iso_z(c["decided"]) if done else None, "events": ev})
    doc = {"export": {"system": "Financial crimes case manager", "exported_at": "2026-11-02T11:20:00Z",
                      "scope": "investigations open on 1 July 2025 or opened since"}, "cases": out}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=1, ensure_ascii=False)
        f.write("\n")
    C.set_mtime(path)
    return len(out)


def write_sars(W, path):
    rows = [[f["bsa_id"], f["case_id"], C.iso_z(f["filed"]), f["shown_prior"], f["start"].isoformat(), f["end"].isoformat(),
             f["amount"], f["subjects"]] for f in W["filings"] if f["filed"] >= C.DATA0_UTC]
    C.write_csv(path, ["bsa_id", "case_id", "filed_at_utc", "prior_bsa_id", "activity_start", "activity_end",
                       "amount_usd", "subjects"], rows)
    return len(rows)


def write_runs(W, path):
    rows = [[x["run_id"], x["bdate"].isoformat(), x["type"], C.iso_z(x["start"]), C.iso_z(x["end"]), x["n"], x["note"]]
            for x in sorted(W["runs"], key=lambda x: (x["start"], x["run_id"])) if x["bdate"] >= C.DATA0]
    C.write_csv(path, ["run_id", "business_date", "run_type", "started_at_utc", "completed_at_utc", "alerts_raised",
                       "note"], rows)


TYPOLOGY = {"CSH-LDS": "Structuring", "CSH-VEL": "Cash", "XB-HRJ": "Cross-border", "RMF-P2P": "Layering",
            "MUL-INF": "Money mules", "FAN-OUT": "Layering", "CHB-ABU": "Merchant abuse", "ATM-WDL": "Cash-out",
            "PRF-DEV": "Profile", "DRM-REA": "Account takeover", "MER-RND": "Merchant collusion",
            "CRY-OFF": "Virtual assets", "ELD-EXP": "Elder exploitation", "GMB-SPL": "Gambling"}
OWNER = {"CSH-LDS": "Retail cash", "CSH-VEL": "Retail cash", "XB-HRJ": "Cross-border", "RMF-P2P": "P2P",
         "MUL-INF": "P2P", "FAN-OUT": "P2P", "CHB-ABU": "Merchant", "ATM-WDL": "Card", "PRF-DEV": "Monitoring",
         "DRM-REA": "Monitoring", "MER-RND": "Merchant", "CRY-OFF": "Cross-border", "ELD-EXP": "Consumer",
         "GMB-SPL": "Merchant"}


def _xlsx(path, sheets, created, modified, author):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for title, rows, widths in sheets:
        ws = wb.create_sheet(title)
        for row in rows:
            ws.append(list(row))
        for c in ws[1]:
            c.font = Font(bold=True)
        for i, w in enumerate(widths):
            ws.column_dimensions[chr(65 + i)].width = w
    wb.save(path)
    C.normalise_zip(path, created, modified, author=author)


def write_catalogue(path):
    rows = [["scenario_code", "scenario_name", "typology", "owner", "in_production_from", "retired_on", "replaced_by",
             "notes"]]
    starts = {"CSH-LDS": "2021-03-01", "CSH-VEL": "2021-03-01", "XB-HRJ": "2021-09-13", "RMF-P2P": "2022-02-07",
              "MUL-INF": "2022-06-20", "FAN-OUT": "2022-06-20", "CHB-ABU": "2023-01-16", "ATM-WDL": "2021-03-01",
              "PRF-DEV": "2021-03-01", "DRM-REA": "2022-11-07", "MER-RND": "2023-08-14", "CRY-OFF": "2024-04-08",
              "ELD-EXP": "2024-10-21", "GMB-SPL": "2025-02-03"}
    for code in C.CODES:
        retired = "2026-03-31" if code in C.REPLACEMENT else ""
        rep = C.REPLACEMENT.get(code, "")
        note = "recalibrated and reissued as " + rep if rep else ""
        rows.append([code, C.NAME[code], TYPOLOGY[code], OWNER[code], starts[code], retired, rep, note])
        if rep:
            rows.append([rep, C.NAME[code] + " (recalibrated)", TYPOLOGY[code], OWNER[code], "2026-04-01", "", "",
                         "replaces " + code])
    _xlsx(path, [("Scenarios", rows, (11, 58, 18, 13, 18, 12, 12, 52))], "2021-02-22T15:10:00Z", "2026-04-02T13:46:00Z",
          "Miguel Swanson")


def write_risk(W, path):
    r = C.rng("risk")
    seen = sorted({a["customer"] for a in W["alerts"] if a["bdate"] >= C.DATA0 and a["gen"] <= C.EXTRACT_UTC})
    rows = []
    for cno in seen:
        tier = ["Low", "Medium", "High"][int(r.choice(3, p=[0.55, 0.33, 0.12]))]
        seg = "Merchant" if r.random() < 0.18 else "Consumer"
        on = dt.date(2019, 1, 1) + dt.timedelta(days=int(r.integers(0, 2400)))
        rev = max(on, dt.date(2026, 10, 30) - dt.timedelta(days=int(r.integers(0, 720))))
        rows.append([cno, seg, tier, on.isoformat(), rev.isoformat()])
    C.write_csv(path, ["customer_no", "segment", "risk_tier", "onboarded_on", "last_kyc_review"], rows)


def write_capacity(path):
    rows = [["team", "investigators_2026", "investigators_2027", "productive_hours_per_investigator", "notes"],
            ["INV-East", 9, 10, 1480, "one hire approved for Q1 2027"],
            ["INV-Central", 8, 8, 1480, ""],
            ["INV-Merchant", 6, 7, 1450, "merchant collusion specialist from February 2027"],
            ["INV-Cross-border", 5, 5, 1420, "shares the FIU's sanctions screening rota"],
            ["Triage pool", 14, 14, 1520, "contractors from the March 2026 surge retained"]]
    _xlsx(path, [("Capacity 2027", rows, (18, 18, 18, 30, 50))], "2026-08-19T14:02:00Z", "2026-10-28T20:31:00Z",
          "Leah Berg")


def write_qa(W, path):
    """Quality Assurance's monthly sample of closed investigations (procedure section 7), as its review log holds it."""
    r = C.rng("qa")
    findings = ["Rationale for closure not recorded in full", "Request for information not followed up",
                "Counterparty searches not evidenced", "SAR narrative missing the activity period",
                "Related alerts not reviewed before closure", "Escalation note does not cite the alert"]
    by_month = {}
    for c in W["cases"]:
        if c["decided"] > C.EXTRACT_UTC:
            continue
        d = C.to_eastern(c["decided"]).date()
        if d.year == 2026 and d.month <= 9:
            by_month.setdefault(d.month, []).append(c)
    rows = []
    ref = 30_000 + int(r.integers(100, 900))
    for m in sorted(by_month):
        pool = sorted(by_month[m], key=lambda c: c["case_id"])
        k = 16 + int(r.integers(0, 9))
        pick = sorted(int(i) for i in r.choice(len(pool), size=k, replace=False))
        for i in pick:
            c = pool[i]
            ref += int(r.integers(1, 6))
            reviewed = dt.date(2026, m, 1) + dt.timedelta(days=31 + int(r.integers(0, 20)))
            while reviewed.weekday() >= 5:
                reviewed += dt.timedelta(days=1)
            u = float(r.random())
            res = "Pass" if u < 0.80 else ("Pass with comments" if u < 0.94 else "Fail")
            note = "" if res == "Pass" else findings[int(r.integers(0, len(findings)))]
            rows.append(["QA-%d" % ref, "2026-%02d" % m, c["case_id"],
                         "SAR filed" if c["outcome"] == "SAR" else "No SAR", reviewed.isoformat(), res, note])
    C.write_csv(path, ["qa_ref", "sample_month", "case_id", "disposition", "reviewed_on", "result", "finding"], rows)


def build(W, folder):
    os.makedirs(folder, exist_ok=True)
    p = lambda k: os.path.join(folder, FILES[k])
    n = {}
    n["alerts"] = write_alerts(W, p("alerts"))
    n["cases"] = write_cases(W, p("cases"))
    n["sars"] = write_sars(W, p("sars"))
    write_runs(W, p("runs"))
    write_catalogue(p("catalogue"))
    write_risk(W, p("risk"))
    write_capacity(p("capacity"))
    write_qa(W, p("qa"))
    D.procedure_pdf(p("procedure"))
    D.thread_eml(p("thread"))
    return n
