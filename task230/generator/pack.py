"""The data exports: the capture platform's first-pass log and field edits, the QA tool's blind re-key audit,
the workforce register, the stream register, the plan of record, form specifications, client forecasts,
the billing register, the second-pass session export, delivery manifests, client audits and two extracts
the solution does not read."""
import datetime as dt
import json
import math
import os

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

import asks_sim as AS
import nov
import postprocess
import sim
import world as W

FILES = {
    "spine": "first_pass_verifications_2026q3.parquet",
    "edits": "first_pass_field_edits_2026q3.parquet",
    "audit": "blind_rekey_audit_2026q3.parquet",
    "workforce": "workforce_register.xlsx",
    "streams": "stream_register.csv",
    "plan": "november_operating_plan.xlsx",
    "qcp": "QCP-04_first_pass_quality_control.docx",
    "schedules": "client_quality_schedules_2026.pdf",
    "pilot": "hollings_pryce_pilot_report.docx",
    "sessions": "second_pass_sessions_2026_09.csv",
    "labour": "second_pass_labour_planning_note.docx",
    "forms": "form_specifications.xlsx",
    "fc_kba": "kessington_volume_forecast_nov26.csv",
    "fc_us": "us_client_forecasts_nov26.xlsx",
    "fc_au": "wattlebird_coolabah_forecasts_fy27.xlsx",
    "fc_uk": "uk_client_forecasts_nov26.csv",
    "fc_hpy": "hollings_pryce_forecast_nov26.json",
    "ca_kba": "kessington_audit_findings_q3.csv",
    "ca_us": "client_audits_us_q3.xlsx",
    "ca_au": "client_audits_au_q3.xlsx",
    "ca_uk": "client_portal_audits_uk_q3.json",
    "manifests": "delivery_manifests_2026q3.csv",
    "index": "delivery_index_2026q3.parquet",
    "ocr": "ocr_confidence_summary_2026q3.csv",
    "keys": "verifier_keystroke_telemetry_2026q3.parquet",
    "notes": "capture_mis_extract_notes.md",
}
DISTRACTORS = ["ocr", "keys", "fc_kba", "fc_us", "fc_au", "fc_uk", "fc_hpy"]
DAY = dt.timedelta(days=1)


def _write_parquet(df, path):
    t = pa.Table.from_pandas(df, preserve_index=False)
    t = t.replace_schema_metadata(None)
    pq.write_table(t, path, compression="snappy", use_dictionary=True, write_statistics=True, row_group_size=500_000)


def _xlsx_save(wb, path, who, created, modified):
    wb.save(path)
    postprocess.scrub(path, who, modified[:10])
    postprocess.finish_office(path, created, modified, W.ORG)


def _header(ws, cols, row=1):
    for j, c in enumerate(cols, start=1):
        cell = ws.cell(row=row, column=j, value=c)
        cell.font = Font(bold=True)
        cell.fill = PatternFill("solid", fgColor="DDE4EE")


# ----------------------------------------------------------------------------------------------- the main path
def spine_and_edits(S, target):
    rng = np.random.default_rng(W.SEED + 1)
    docs, F, P = S["docs"], S["F"], S["P"]
    badge = P.badge.values
    start = np.array([np.datetime64(sim.shift_start(d, q)) for d, q in zip(docs.day.values, docs.queue.values)])
    close = start + (docs.tmin.values * 60).astype("timedelta64[s]")
    dur = (docs.kf.values * rng.uniform(2.0, 3.4, size=len(docs)) + rng.uniform(4, 25, size=len(docs))).astype(int)
    opened = close - dur.astype("timedelta64[s]")
    E = F[(F.err & ~F.miss) | F.fa]
    nedit = E.groupby("doc").size().reindex(docs.doc.values, fill_value=0).values
    sub = pd.DataFrame({"document_id": docs.doc_id.values, "stream_code": docs.code.map(W.SID).values,
                        "form_version": docs.version.values, "badge_no": badge[docs.pid.values], "opened_at": opened,
                        "closed_at": close, "outcome": "SUBMITTED", "key_fields": docs.kf.values.astype("int16"),
                        "fields_keyed_over": nedit.astype("int16"), "_doc": docs.doc.values})
    t = docs[docs.timeout]
    tstart = start[t.doc.values] + (t.to_tmin.values * 60).astype("timedelta64[s]")
    tout = pd.DataFrame({"document_id": t.doc_id.values, "stream_code": t.code.map(W.SID).values,
                         "form_version": t.version.values, "badge_no": badge[t.to_pid.values.astype(int)], "opened_at": tstart,
                         "closed_at": tstart + np.timedelta64(15 * 60, "s"), "outcome": "TIMED_OUT",
                         "key_fields": t.kf.values.astype("int16"), "fields_keyed_over": np.zeros(len(t), "int16"),
                         "_doc": t.doc.values})
    sp = pd.concat([sub, tout], ignore_index=True).sort_values(["opened_at", "document_id"]).reset_index(drop=True)
    sp.insert(0, "screen_id", [f"FP{40000000 + i * 3 + (i % 7):09d}" for i in range(len(sp))])
    sp["opened_at"] = sp.opened_at.astype("datetime64[s]")
    sp["closed_at"] = sp.closed_at.astype("datetime64[s]")
    # field edits on submitted screens
    sid = sp[sp.outcome == "SUBMITTED"].set_index("_doc").screen_id
    so = sp[sp.outcome == "SUBMITTED"].set_index("_doc")
    E = E.assign(field_name=sim.fname_vec(E))
    o = so.opened_at.reindex(E.doc.values).values
    c = so.closed_at.reindex(E.doc.values).values
    frac = rng.uniform(0.05, 0.95, size=len(E))
    keyed = o + ((c - o).astype("timedelta64[s]").astype(np.int64) * frac).astype("timedelta64[s]")
    ed = pd.DataFrame({"screen_id": sid.reindex(E.doc.values).values, "document_id": docs.doc_id.values[E.doc.values],
                       "field_name": E.field_name.values, "keyed_at": keyed.astype("datetime64[s]")})
    ed = ed.sort_values(["keyed_at", "screen_id", "field_name"]).reset_index(drop=True)
    ed.insert(0, "edit_id", np.arange(7_300_001, 7_300_001 + len(ed)))
    _write_parquet(sp.drop(columns="_doc"), os.path.join(target, FILES["spine"]))
    _write_parquet(ed, os.path.join(target, FILES["edits"]))
    return sp, ed


def audit(S, target):
    rng = np.random.default_rng(W.SEED + 2)
    docs, F = S["docs"], S["F"]
    A = F[F.audited].copy()
    A["field_name"] = sim.fname_vec(A)
    res = np.where(A.err & A.miss, "R", np.where(A.err, "C", np.where(A.fa, "V", "M")))
    rounds = np.where(rng.random(len(A)) < np.where(A.err | A.fa, 0.22, 0.025), 3, 2)
    lag = rng.integers(2, 9, size=len(A))
    adj = (pd.to_datetime(A.day).values + (lag * 86400).astype("timedelta64[s]")).astype("datetime64[D]")
    did = docs.doc_id.values[A.doc.values]
    out = pd.DataFrame({"document_id": did, "client_code": A.code.map(lambda c: W.STREAMS[c]["client"]).values,
                        "stream_code": A.code.map(W.SID).values, "form_version": A.version.values,
                        "field_name": A.field_name.values, "rekey_rounds": rounds.astype("int8"), "result_code": res,
                        "adjudicated_on": adj})
    order = np.lexsort((A.fpos.values, did, adj))
    out = out.iloc[order].reset_index(drop=True)
    # audit references are per document
    first = ~out.document_id.duplicated()
    refs = np.cumsum(first) + 512000
    out.insert(0, "audit_ref", [f"QA{r:07d}" for r in refs])
    _write_parquet(out, os.path.join(target, FILES["audit"]))
    return out


def workforce_register(S, target):
    P = S["P"]
    wb = Workbook()
    ws = wb.active
    ws.title = "Employees"
    _header(ws, ["Emp No", "Role", "Date of joining", "Date of exit", "Location"])
    for r in P.sort_values("emp").itertuples():
        ws.append([r.emp, "Process Associate, first-pass verification", r.hire, r.leave, "Salt Lake Sec V, Tower 2"])
    ws2 = wb.create_sheet("Badge allocation")
    _header(ws2, ["Badge", "Emp No", "Valid from", "Valid to", "Reason"])
    for r in P.sort_values(["badge", "hire"]).itertuples():
        frm = max(r.hire, dt.date(2024, 4, 1))
        reason = "Reissued" if (P.badge == r.badge).sum() > 1 and r.hire > P[P.badge == r.badge].hire.min() else "New joiner"
        if r.hire < dt.date(2024, 4, 1):
            reason = "Badge migration (HRMS cutover)"
        ws2.append([r.badge, r.emp, frm, r.leave, reason])
    ws3 = wb.create_sheet("Queue rota Q3")
    _header(ws3, ["Emp No", "Month", "Queue", "Weekly off"])
    offs = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for r in P.sort_values("emp").itertuples():
        for m in (7, 8, 9):
            if r.group not in sim.ROTATION[m]:
                continue
            if r.hire > dt.date(2026, m, 28) or (r.leave and r.leave < dt.date(2026, m, 1)):
                continue
            ws3.append([r.emp, dt.date(2026, m, 1).strftime("%b-%Y"), {"D": "Day (AU/UK)", "N": "Night (US)"}[sim.ROTATION[m][r.group]],
                        offs[r.pid % 6]])
    for w in (ws, ws2, ws3):
        for col in "ABCDE":
            w.column_dimensions[col].width = 18
        for row in w.iter_rows(min_row=2):
            for cell in row:
                if isinstance(cell.value, dt.date):
                    cell.number_format = "dd-mmm-yyyy"
    _xlsx_save(wb, os.path.join(target, FILES["workforce"]), W.PEOPLE["mis"], "2024-04-02T05:12:00Z", "2026-10-26T11:48:00Z")


def stream_register(target):
    rows = []
    for code, s in W.STREAMS.items():
        c = W.CLIENTS[s["client"]]
        base = dict(stream_code=s["sid"], client_code=s["client"], client_name=c["name"], description=s["label"],
                    form_family=s["family"], contract_ccy=c["ccy"], audit_sample_pct=round(100 * W.audit_share(code), 0) if code != "D6" else 10)
        if code == "D5":
            rows.append(dict(base, queue="DAY", queue_from="2025-03-03", queue_to="2026-10-31"))
            rows.append(dict(base, queue="NIGHT", queue_from="2026-11-01", queue_to=""))
        elif code == "D6":
            rows.append(dict(base, queue="DAY", queue_from="2026-08-17", queue_to="2026-09-26", audit_sample_pct=100, description=s["label"] + " (pilot)"))
            rows.append(dict(base, queue="DAY", queue_from="2026-11-01", queue_to=""))
        else:
            rows.append(dict(base, queue={"N": "NIGHT", "D": "DAY"}[s["q3"]], queue_from="2024-01-02" if s["client"] in ("KBA", "HPB") else "2025-02-03", queue_to=""))
    df = pd.DataFrame(rows)
    df["audit_sample_pct"] = df.audit_sample_pct.astype(int)
    df.to_csv(os.path.join(target, FILES["streams"]), index=False, lineterminator="\n")
    return df


def form_specs(target):
    wb = Workbook()
    ws = wb.active
    ws.title = "Versions"
    _header(ws, ["Stream", "Form version", "Effective from (shift-day)", "Key fields per document", "Notes"])
    notes = {"D6": "Scanned in bundles of 25 documents (contract schedule 2)", "N3": "Treating dentist NPI added as a key field",
             "D3": "Rehabilitation provider added", "N2": "Referring provider NPI added (client change 2026-14)",
             "D2": "Provider location added", "D4": "Excess applied added", "D5": "Notification = one FNOL form"}
    for code in W.ORDER:
        for v, eff, add in W.VERSIONS[code]:
            ws.append([W.SID[code], v, eff, len(W.fields(code, v)), notes.get(code, "") if (add or code in ("D5",)) or (code == "D6" and not add) else ""])
    ws2 = wb.create_sheet("Key fields")
    _header(ws2, ["Stream", "Form version", "Field", "Field type"])
    for code in W.ORDER:
        for v, eff, add in W.VERSIONS[code]:
            for n, t in W.fields(code, v):
                ws2.append([W.SID[code], v, n, t])
    for w in (ws, ws2):
        for col, wd in zip("ABCDE", (12, 16, 24, 22, 48)):
            w.column_dimensions[col].width = wd
        for row in w.iter_rows(min_row=2):
            for cell in row:
                if isinstance(cell.value, dt.date):
                    cell.number_format = "yyyy-mm-dd"
    _xlsx_save(wb, os.path.join(target, FILES["forms"]), W.PEOPLE["mis"], "2025-01-06T06:30:00Z", "2026-10-19T09:02:00Z")


def operating_plan(S, plan, roster, target):
    wb = Workbook()
    ws = wb.active
    ws.title = "Plan of record"
    lines = [
        ["November 2026 operating plan, first-pass capture"],
        [],
        ["Plan of record", "Version 3"],
        ["Issued", dt.date(2026, 10, 23)],
        ["Owner", W.PEOPLE["ops"] + ", Head of Operations"],
        ["Approved", "Head of Operations, 23 Oct 2026"],
        ["Covers", "Shift-days 1 to 30 November 2026 (a night shift belongs to the date it starts)"],
        [],
        ["Notes"],
        ["Volumes are the clients' weekly forecasts as accepted for planning, spread evenly over each client's working days in the week, any remainder on the earliest days."],
        ["Hollings & Pryce forecast in bundles; one bundle is 25 documents."],
        ["Thistlecombe Motor moves to the night queue from 1 November to free day capacity for the Hollings & Pryce go-live."],
        ["Second-pass streams for November are set on the head of operations' list, not here."],
    ]
    for l in lines:
        ws.append(l)
    ws["A1"].font = Font(bold=True, size=13)
    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 60
    ws["B4"].number_format = "dd-mmm-yyyy"
    ws2 = wb.create_sheet("Routing")
    _header(ws2, ["Stream", "Client", "Queue (October)", "Queue (November)", "Change"])
    for code, s in W.STREAMS.items():
        oq = {"N": "Night", "D": "Day", None: "-"}[s["q3"]]
        if code == "D6":
            oq = "-"
        ch = "Moves to nights 1 Nov" if code == "D5" else ("Go-live 2 Nov (first shift-day)" if code == "D6" else "")
        ws2.append([s["sid"], W.CLIENTS[s["client"]]["name"], oq, {"N": "Night", "D": "Day"}[s["nov"]], ch])
    ws3 = wb.create_sheet("Daily key fields")
    cols = ["Shift-day", "Day"] + [W.SID[c] for c in W.ORDER]
    _header(ws3, cols)
    piv = plan.pivot_table(index="day", columns="code", values="kf", aggfunc="sum")
    for d in nov.days_in_nov():
        row = [d, d.strftime("%a")]
        for c in W.ORDER:
            v = piv.loc[d, c] if (d in piv.index and c in piv.columns and not pd.isna(piv.loc[d, c])) else None
            row.append(int(v) if v is not None else None)
        ws3.append(row)
    for row in ws3.iter_rows(min_row=2):
        row[0].number_format = "dd-mmm-yy"
        for cell in row[2:]:
            cell.number_format = "#,##0"
    ws3.column_dimensions["A"].width = 12
    ws3.freeze_panes = "C2"
    ws4 = wb.create_sheet("Roster")
    _header(ws4, ["Badge", "Emp No", "Queue", "Note"])
    for r in roster.sort_values(["queue", "badge"]).itertuples():
        note = "Joined Oct-26, training complete 30 Oct" if r.hire >= dt.date(2026, 10, 1) else ""
        ws4.append([r.badge, r.emp, {"D": "Day", "N": "Night"}[r.queue], note])
    ws5 = wb.create_sheet("October second pass")
    ws5.append(["Second-pass verification, October 2026 (as signed 28 Sep 2026)"])
    ws5["A1"].font = Font(bold=True)
    _header(ws5, ["Stream", "Client"], row=2)
    for c in W.OCT_SECOND_PASS:
        ws5.append([W.SID[c], W.CLIENTS[W.STREAMS[c]["client"]]["name"]])
    ws6 = wb.create_sheet("Budget rates")
    _header(ws6, ["Currency", "INR per unit (FY27 budget)"])
    for k, v in W.BUDGET_INR.items():
        ws6.append([k, v])
    ws6.append([])
    ws6.append(["Contract amounts in different currencies are compared at these budget rates."])
    for w in (ws2, ws4, ws5, ws6):
        for col in "ABCDE":
            w.column_dimensions[col].width = 26
    _xlsx_save(wb, os.path.join(target, FILES["plan"]), W.PEOPLE["ops"], "2026-10-06T04:20:00Z", "2026-10-23T12:36:00Z")


# ----------------------------------------------------------------------------------------------- forecasts and billing
def forecasts(fc, target):
    # revisions other than the accepted one were each the client's own re-forecast, week by week
    fc = fc.copy()
    na = ~fc.accepted
    import hashlib
    wob = [(int(hashlib.md5(f"{w}-{rv}-{c}".encode()).hexdigest(), 16) % 91 - 45) / 1000.0
           for w, rv, c in zip(fc.week_start, fc.revision, fc.code)]
    fc.loc[na, "units"] = [int(round(u * (1 + x))) for u, x, m in zip(fc.units, wob, na) if m]

    def us_week_label(d):
        return f"Week ending {d + dt.timedelta(days=6):%m/%d/%Y}"
    k = fc[fc.client == "KBA"].copy()
    rows = []
    for r in k.sort_values(["sent", "week_start", "code"]).itertuples():
        rows.append({"FcstRev": r.revision, "SentDate": f"{r.sent:%m/%d/%Y}", "WeekBeginning": f"{r.week_start:%m/%d/%Y}",
                     "ClaimType": {"N1": "INSTITUTIONAL (UB-04)", "N2": "PROFESSIONAL (CMS-1500)"}[r.code],
                     "ProjectedClaims": r.units})
    pd.DataFrame(rows).to_csv(os.path.join(target, FILES["fc_kba"]), index=False, lineterminator="\r\n")

    wb = Workbook()
    first = True
    for c, title, unit in (("NDS", "Northgate", "Claims"), ("BMC", "Brightmoor", "First reports"), ("HPB", "Harbison", "Claims")):
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = title
        g = fc[fc.client == c]
        weeks = sorted(g.week_start.unique())
        ws.append([f"{W.CLIENTS[c]['name']}: volume forecast for Tamralipta capture, November 2026"])
        ws.append([f"Unit: {unit.lower()} per week (week runs Sunday to Saturday)"])
        ws.append([])
        ws.append(["Revision", "Sent"] + [us_week_label(w) for w in weeks])
        for (rev, sent), gg in g.groupby(["revision", "sent"], sort=False):
            vals = gg.set_index("week_start").units
            ws.append([rev, sent] + [int(vals[w]) for w in weeks])
        for row in ws.iter_rows(min_row=5):
            row[1].number_format = "mm/dd/yyyy"
        ws.column_dimensions["A"].width = 12
        ws.column_dimensions["B"].width = 12
    _xlsx_save(wb, os.path.join(target, FILES["fc_us"]), "Planning Desk", "2026-09-24T14:10:00Z", "2026-10-22T16:40:00Z")

    wb = Workbook()
    ws = wb.active
    ws.title = "Forecast"
    _header(ws, ["Insurer", "Line", "Forecast ID", "Issued", "FY27 week", "Claims"])
    for c in ("WBH", "CIP"):
        g = fc[fc.client == c].sort_values(["sent", "code", "week_start"])
        for r in g.itertuples():
            line = {"D1": "Hospital", "D2": "Extras", "D3": "Income protection"}[r.code]
            ws.append([W.CLIENTS[c]["name"], line, r.revision, r.sent, f"FY27-W{nov.fiscal_week_au(r.week_start):02d}", r.units])
    for row in ws.iter_rows(min_row=2):
        row[3].number_format = "dd/mm/yyyy"
    ws2 = wb.create_sheet("FY27 calendar")
    _header(ws2, ["FY27 week", "Monday", "Sunday"])
    d = dt.date(2026, 6, 29)
    while d <= dt.date(2026, 12, 28):
        ws2.append([f"FY27-W{nov.fiscal_week_au(d):02d}", d, d + dt.timedelta(days=6)])
        d += dt.timedelta(days=7)
    for row in ws2.iter_rows(min_row=2):
        row[1].number_format = "dd/mm/yyyy"
        row[2].number_format = "dd/mm/yyyy"
    for w in (ws, ws2):
        for col in "ABCDEF":
            w.column_dimensions[col].width = 20
    _xlsx_save(wb, os.path.join(target, FILES["fc_au"]), "Partner Operations", "2026-09-29T00:10:00Z", "2026-10-21T05:05:00Z")

    rows = []
    for c in ("WPC", "TCM"):
        g = fc[fc.client == c].sort_values(["sent", "week_start"])
        for r in g.itertuples():
            rows.append({"client": W.CLIENTS[c]["name"], "forecast_version": r.revision, "issued": f"{r.sent:%d/%m/%Y}",
                         "iso_week": f"{r.week_start.isocalendar()[0]}-W{r.week_start.isocalendar()[1]:02d}",
                         "volume": r.units, "unit": "notifications" if c == "TCM" else "claims"})
    pd.DataFrame(rows).to_csv(os.path.join(target, FILES["fc_uk"]), index=False, lineterminator="\n")

    g = fc[fc.client == "HPY"].sort_values(["sent", "week_start"])
    js = {"supplier": "Tamralipta Data Services", "account": "HPY-TDS-01", "unit": "bundle", "revisions": []}
    for (rev, sent), gg in g.groupby(["revision", "sent"], sort=False):
        js["revisions"].append({"revision": rev, "issued": f"{sent:%Y-%m-%d}",
                                "weeks": [{"week_commencing": f"{w:%Y-%m-%d}", "bundles": int(u)} for w, u in zip(gg.week_start, gg.units)]})
    with open(os.path.join(target, FILES["fc_hpy"]), "w") as fh:
        json.dump(js, fh, indent=2)
        fh.write("\n")


def billing_register(target, oct_docs):
    wb = Workbook()
    ws = wb.active
    ws.title = "Accounts"
    _header(ws, ["Account", "Client", "Stream", "Billing unit", "Currency", "Band", "Band set on", "Unit price", "Last invoice"])
    for c, b in W.BANDS.items():
        n = oct_docs.get(c, 0)
        bi = max(i for i, f in enumerate(b["floors"]) if n >= f)
        for code, prices in b["price"].items():
            ws.append([f"{c}-TDS-01", W.CLIENTS[c]["name"], W.SID[code], b["unit"], W.CLIENTS[c]["ccy"], b["names"][bi],
                       "Oct-2026 volume" if c != "HPY" else "Pilot (Aug-Sep 2026)", prices[bi], "INV-OCT26" if c != "HPY" else "INV-PILOT"])
    for col, wd in zip("ABCDEFGHI", (14, 32, 12, 14, 10, 8, 20, 10, 12)):
        ws.column_dimensions[col].width = wd
    _xlsx_save(wb, os.path.join(target, FILES["billing"]), "Finance Shared Services", "2025-04-01T03:30:00Z", "2026-10-07T10:15:00Z")


# ----------------------------------------------------------------------------------------------- second pass and client audits
def sessions_export(L, target):
    start = np.array([np.datetime64(sim.shift_start(d, q)) for d, q in zip(L.day.values, L.queue.values)])
    t = start + (L.offset_min.values * 60).astype("timedelta64[s]")
    out = pd.DataFrame({"session_ref": L.session.values, "work_date": [f"{d:%d-%m-%Y}" for d in L.day],
                        "sp_badge": L.badge.values, "basket": L.basket.map(W.SP_BASKET).values,
                        "document_id": L.doc_id.values, "doc_opened": pd.to_datetime(t).strftime("%d-%m-%Y %H:%M:%S"),
                        "handling_sec": L.secs.values})
    out["_t"] = pd.to_datetime(t)
    out = out.sort_values(["_t", "session_ref"]).drop(columns="_t")
    out.to_csv(os.path.join(target, FILES["sessions"]), index=False, lineterminator="\n")


def manifests(D, target):
    out = pd.DataFrame({"file_name": D.file, "stream_code": D.code.map(W.SID), "shift_date": [f"{d:%Y-%m-%d}" for d in D.day],
                        "batch": D.batch, "transmitted_at": [f"{t:%Y-%m-%dT%H:%M:00}+05:30" for t in D.sent_ist],
                        "record_count": D.records, "status": "ACK"})
    out = out.sort_values(["transmitted_at", "file_name"])
    out.to_csv(os.path.join(target, FILES["manifests"]), index=False, lineterminator="\n")


def delivery_index(I, target):
    import asks_sim as _AS
    out = pd.DataFrame({"file_name": I.file.values,
                        "claim_ref": [_AS._claim_ref(c, k, n) for c, k, n in zip(I.client.values, I.code.values, I.claim.values)],
                        "document_id": I.doc_id.values, "sheet": I.sheet.values.astype("int8")})
    _write_parquet(out, os.path.join(target, FILES["index"]))


def client_audit_files(Fd, D, target):
    utc = D.set_index("file").sent_utc
    Fd = Fd.copy()
    Fd["received"] = [AS.received_business_date(utc[f], c, cl) for f, c, cl in zip(Fd.file, Fd.client, Fd.claim)]
    Fd["version"] = [W.version_on(c, d) for c, d in zip(Fd.code, Fd.day)]
    Fd["ref"] = [AS._claim_ref(c, k, n) for c, k, n in zip(Fd.client, Fd.code, Fd.claim)]

    def rdate(r):
        base = min(r.received + dt.timedelta(days=9 + (int(r.claim) % 11)), dt.date(2026, 10, 9) - dt.timedelta(days=int(r.claim) % 4))
        if r.rnd == 2:
            return min(base + dt.timedelta(days=21 + int(r.claim) % 9), dt.date(2026, 10, 16) - dt.timedelta(days=int(r.claim) % 3))
        return base

    # Kessington: CSV from its claims system
    k = Fd[Fd.client == "KBA"].sort_values(["received", "ref", "seq", "rnd"])
    rows = []
    for r in k.itertuples():
        rows.append({"Claim Nbr": r.ref, "Src File": r.file, "Rcvd Bus Dt": f"{r.received:%Y-%m-%d}",
                     "Form": r.version, "Finding Seq": r.seq if r.seq else "", "Finding Cd": r.reason, "Review Rnd": r.rnd if r.seq else "",
                     "Review Dt": f"{rdate(r):%Y-%m-%d}"})
    pd.DataFrame(rows).to_csv(os.path.join(target, FILES["ca_kba"]), index=False, lineterminator="\r\n")

    # US others: one sheet per client in its own layout
    wb = Workbook()
    first = True
    for c, title in (("NDS", "Northgate"), ("BMC", "Brightmoor"), ("HPB", "Harbison")):
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = title
        g = Fd[Fd.client == c].sort_values(["received", "ref", "seq", "rnd"])
        if c == "NDS":
            _header(ws, ["Claim ID", "Batch File", "Received", "Finding #", "Error Code", "Status"])
            for r in g.itertuples():
                st = "" if not r.seq else ("SUPERSEDED" if not r.final else ("RE-REVIEWED" if r.rnd == 2 else "FINAL"))
                ws.append([r.ref, r.file, r.received, r.seq or None, r.reason or None, st or "NO FINDING"])
        elif c == "BMC":
            _header(ws, ["Report No", "Inbound File", "Receipt Date", "Line", "Discrepancy", "Round", "Reviewer Outcome"])
            for r in g.itertuples():
                outc = "" if not r.seq else ("Replaced on re-review" if not r.final else ("Re-review" if r.rnd == 2 else "Initial"))
                ws.append([r.ref, r.file, r.received, r.seq or None, r.reason or "CLEAN", r.rnd if r.seq else None, outc or None])
        else:
            _header(ws, ["Rx Claim", "Source", "Recd", "Err Seq", "Err Code", "Rev", "Rev Date"])
            for r in g.itertuples():
                ws.append([r.ref, r.file, r.received, r.seq or None, r.reason or None, r.rnd if r.seq else None, rdate(r) if r.seq else None])
        for row in ws.iter_rows(min_row=2):
            for cell in row:
                if isinstance(cell.value, (dt.datetime, dt.date)):
                    cell.number_format = "yyyy-mm-dd"
        for col in "ABCDEFG":
            ws.column_dimensions[col].width = 22
    _xlsx_save(wb, os.path.join(target, FILES["ca_us"]), "Client Services", "2026-10-05T07:20:00Z", "2026-10-20T13:44:00Z")

    wb = Workbook()
    first = True
    for c, title in (("WBH", "Wattlebird QA"), ("CIP", "Coolabah QA")):
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = title
        g = Fd[Fd.client == c].sort_values(["received", "ref", "seq", "rnd"])
        _header(ws, ["Claim", "Stream", "File", "Lodged", "Item", "Reason", "Review", "Current"])
        for r in g.itertuples():
            ws.append([r.ref, W.SID[r.code], r.file, r.received, r.seq or None, r.reason or "NIL",
                       ("Second review" if r.rnd == 2 else "First review") if r.seq else None, ("Y" if r.final else "N") if r.seq else None])
        for row in ws.iter_rows(min_row=2):
            row[3].number_format = "dd/mm/yyyy"
        for col in "ABCDEFGH":
            ws.column_dimensions[col].width = 18
    _xlsx_save(wb, os.path.join(target, FILES["ca_au"]), "Client Services", "2026-10-06T02:10:00Z", "2026-10-20T13:51:00Z")

    js = {"export": "partner-quality-findings", "exported_at": "2026-10-19T08:14:22", "partner": "TDS", "records": []}
    for c in ("WPC", "TCM"):
        g = Fd[Fd.client == c].sort_values(["received", "ref", "seq", "rnd"])
        for (ref, cfile), gg in g.groupby(["ref", "file"], sort=False):
            r0 = gg.iloc[0]
            rec = {"insurer": W.CLIENTS[c]["name"], "claim_ref": ref, "batch": cfile,
                   "received_on": f"{r0.received:%Y-%m-%d}", "findings": []}
            for r in gg.itertuples():
                if not r.seq:
                    continue
                rec["findings"].append({"n": int(r.seq), "code": r.reason, "review": int(r.rnd), "active": bool(r.final)})
            js["records"].append(rec)
    with open(os.path.join(target, FILES["ca_uk"]), "w") as fh:
        json.dump(js, fh, indent=1)
        fh.write("\n")
    return Fd


# ----------------------------------------------------------------------------------------------- not read by the solution
def ocr_summary(S, target):
    rng = np.random.default_rng(W.SEED + 7)
    F = S["F"]
    F = F.assign(month=pd.to_datetime(F.day).dt.month)
    g = F.groupby(["code", "version", "fpos", "month"]).agg(n=("err", "size"), e=("err", "mean")).reset_index()
    names = []
    for r in g.itertuples():
        names.append(W.fields(r.code, r.version)[r.fpos][0])
    g["field"] = names
    conf = 97.8 - 120 * g.e.values + rng.normal(0, 0.9, size=len(g))
    low = np.clip(1.6 * 100 * g.e.values + rng.normal(0, 0.8, size=len(g)), 0.2, None)
    out = pd.DataFrame({"month": [f"2026-{m:02d}" for m in g.month], "stream": g.code.map(W.SID), "form_version": g.version,
                        "field": g.field, "fields_read": g.n, "mean_confidence": np.round(conf, 1), "pct_below_80": np.round(low, 1)})
    out = out.sort_values(["month", "stream", "form_version", "field"])
    out.to_csv(os.path.join(target, FILES["ocr"]), index=False, lineterminator="\n")


def keystroke_telemetry(sp, target):
    rng = np.random.default_rng(W.SEED + 8)
    s = sp[sp.outcome == "SUBMITTED"].copy()
    s["shift_date"] = s.opened_at.dt.date
    g = s.groupby(["badge_no", "shift_date"]).agg(screens=("screen_id", "size"), fields=("key_fields", "sum"),
                                                 first=("opened_at", "min"), last=("closed_at", "max")).reset_index()
    span = (g["last"] - g["first"]).dt.total_seconds() / 60
    active = np.minimum(span, 480) * rng.uniform(0.78, 0.93, size=len(g))
    out = pd.DataFrame({"badge_no": g.badge_no, "login_date": g.shift_date.astype("datetime64[s]"),
                        "active_min": np.round(active, 0).astype(int), "idle_min": np.round(np.maximum(0, span - active), 0).astype(int),
                        "keystrokes": (g.fields * rng.uniform(0.55, 0.9, size=len(g))).astype(int),
                        "fields_per_hr": np.round(g.fields / np.maximum(active, 1) * 60, 1)})
    _write_parquet(out.sort_values(["login_date", "badge_no"]).reset_index(drop=True), os.path.join(target, FILES["keys"]))
