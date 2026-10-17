"""Write the bundle the bank would hand over."""
import csv
import datetime as dt
import json
import os
import random

import sim
import world as W

FILES = {
    "alerts": "alert_adjudication_extract.csv",
    "cases": "confirmed_case_register.csv",
    "base": "customer_base_by_line.xlsx",
    "backlog": "alert_backlog_weekly.csv",
    "lines": "line_structure_register.csv",
    "crosswalk": "customer_id_crosswalk.csv",
    "ledger": "contractor_hours_ledger.csv",
    "lists": "screening_list_versions.json",
    "matches": "screening_match_log.csv",
    "manifest": "extract_manifest.csv",
    "branches": "branch_footprint.csv",
    "training": "aml_training_completion.csv",
}
CASE_COLS = ["case_id", "customer_ref", "line_code", "typology", "onset_month", "first_seen_month",
             "confirmed_month", "disposition", "record_version", "amount", "currency"]
ALERT_COLS = ["alert_id", "queue", "customer_ref", "line_code", "raised_at", "stage", "stage_at",
              "outcome", "analyst", "batch_id"]
CODE = {l[0]: l[1] for l in W.LINES}
OLD_BY_CURRENT = {}
for _oc, _on, _cur, _note in W.OLD_LINES:
    OLD_BY_CURRENT.setdefault(_cur, []).append(_oc)


def recorded_line(name, when):
    """the line code the record carries, which the July 2026 reorganisation changed"""
    cur = CODE[name]
    if when >= W.REORG or cur not in OLD_BY_CURRENT:
        return cur
    olds = OLD_BY_CURRENT[cur]
    return olds[(when.month + when.day) % len(olds)]


def all_cases():
    """every line's cases, with the line's delay mean calibrated to its target"""
    out = {}
    for line in W.LINES:
        wbar = sim.calibrate(line, line[2], line[4])
        out[line[0]] = sim.cases((line[0], line[1], line[2], line[3], wbar, line[5]))
    return out


def write_cases(target, cases):
    rng = random.Random(W.SEED + 11)
    rows = []
    cid = 41200
    for name in [l[0] for l in W.LINES]:
        code = [l[1] for l in W.LINES if l[0] == name][0]
        for c in cases[name]:
            if c["detected"] > W.AS_OF:
                continue                      # the bank holds no record of a case nobody has seen
            cid += 1
            conf = sim.add_months(c["detected"], rng.randrange(0, 3))
            if conf > W.AS_OF:
                conf = W.AS_OF
            cur = "AUD" if (cid % 23 == 0) else "NZD"
            amt = round(8000 + rng.lognormvariate(10.4, 0.9), 2)
            ref = "CU%07d" % (100000 + (cid * 7919) % 850000)
            rows.append({"case_id": "CAS-%06d" % cid, "customer_ref": ref,
                         "line_code": recorded_line(name, c["onset"]),
                         "typology": c["typology"],
                         "onset_month": c["onset"].strftime("%Y-%m"),
                         "first_seen_month": c["detected"].strftime("%Y-%m"),
                         "confirmed_month": conf.strftime("%Y-%m"),
                         "disposition": "confirmed", "record_version": "1",
                         "amount": "%.2f" % amt, "currency": cur})
    # a handful of cases were amended after confirmation: the register holds both versions
    for i, r in enumerate(rows):
        if i % 97 == 13:
            v2 = dict(r)
            v2["record_version"] = "2"
            v2["amount"] = "%.2f" % (float(r["amount"]) * 1.08)
            rows.append(v2)
    path = os.path.join(target, FILES["cases"])
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CASE_COLS, lineterminator="\n")
        w.writeheader()
        for r in sorted(rows, key=lambda z: (z["case_id"], z["record_version"])):
            w.writerow(r)
    return rows


def write_alerts(target, case_rows):
    """the alert system's own record: one row per alert per adjudication stage"""
    rng = random.Random(W.SEED + 23)
    rows = []
    aid = 880000
    start = dt.date(2025, 1, 1)
    months = sim.months_between(start, W.AS_OF) + 1
    for m in range(months):
        mon = sim.add_months(start, m)
        for q in W.ALERT_QUEUES:
            base = {"card disputes": 150, "payment screening": 120, "trade documents": 35,
                    "onboarding": 60, "transaction monitoring": 95, "sanctions screening": 45}[q]
            n = int(base * (0.82 + 0.36 * rng.random()))
            for _ in range(n):
                aid += 1
                day = 1 + rng.randrange(0, 27)
                raised = dt.date(mon.year, mon.month, day)
                qname = ("chargebacks" if q == "card disputes" and raised < dt.date(2026, 4, 1) else q)
                line = {"card disputes": "Cards", "payment screening": "Retail payments",
                        "trade documents": "Trade finance", "onboarding": "Deposits",
                        "transaction monitoring": "Business lending",
                        "sanctions screening": "FX and remittance"}[q]
                ref = "A%08d" % (200000 + (aid * 104729) % 700000)
                batch = "%s-%s-%02d" % (q[:3].upper(), raised.strftime("%Y%m"), 1 + (aid % 7))
                closed_in = 1 + rng.randrange(0, 11)
                rows.append({"alert_id": "AL-%07d" % aid, "queue": qname, "customer_ref": ref,
                             "line_code": recorded_line(line, raised), "raised_at": raised.isoformat(),
                             "stage": "raised", "stage_at": raised.isoformat(), "outcome": "",
                             "analyst": "", "batch_id": batch})
                closed = raised + dt.timedelta(days=closed_in)
                esc = rng.random() < 0.06
                rows.append({"alert_id": "AL-%07d" % aid, "queue": qname, "customer_ref": ref,
                             "line_code": recorded_line(line, raised), "raised_at": raised.isoformat(),
                             "stage": "triaged", "stage_at": closed.isoformat(),
                             "outcome": "escalated" if esc else "closed",
                             "analyst": "AN%03d" % (1 + aid % 40), "batch_id": batch})
                if esc:
                    rows.append({"alert_id": "AL-%07d" % aid, "queue": qname, "customer_ref": ref,
                                 "line_code": recorded_line(line, raised),
                                 "raised_at": raised.isoformat(), "stage": "escalated",
                                 "stage_at": (closed + dt.timedelta(days=2 + rng.randrange(0, 9))).isoformat(),
                                 "outcome": "with investigations", "analyst": "AN%03d" % (1 + aid % 40),
                                 "batch_id": batch})
    # one re-sent batch: the card disputes queue's June 2026 batch 3 was loaded twice
    resent = [dict(r) for r in rows if r["batch_id"] == "CAR-202606-03"]
    for r in resent:
        r["batch_id"] = "CAR-202606-03R"
    rows.extend(resent)
    path = os.path.join(target, FILES["alerts"])
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=ALERT_COLS, lineterminator="\n")
        w.writeheader()
        for r in sorted(rows, key=lambda z: (z["alert_id"], z["stage"])):
            w.writerow(r)
    return rows


def _csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    return path


def write_lines(target):
    rows = []
    for (name, code, lam, cust, wbar, backlog) in W.LINES:
        rows.append([code, name, W.SPAN_FROM.isoformat(), "", "current", code, ""])
    for (oc, on, cur, note) in W.OLD_LINES:
        rows.append([oc, on, W.SPAN_FROM.isoformat(), (W.REORG - dt.timedelta(days=1)).isoformat(),
                     "superseded", cur, note])
    return _csv(os.path.join(target, FILES["lines"]),
                ["line_code", "line_name", "effective_from", "effective_to", "status",
                 "current_line_code", "note"], rows)


def write_crosswalk(target, case_rows, alert_rows):
    rng = random.Random(W.SEED + 31)
    seen = {}
    for r in alert_rows:
        seen.setdefault(r["customer_ref"], None)
    cases = sorted({r["customer_ref"] for r in case_rows})
    alerts = sorted(seen)
    rows = []
    for i, cu in enumerate(cases):
        a = alerts[(i * 7919) % len(alerts)]
        rows.append([cu, a, "matched on name, date of birth and account" if i % 5 else
                     "matched on account number"])
    return _csv(os.path.join(target, FILES["crosswalk"]),
                ["case_customer_ref", "alert_customer_ref", "match_basis"], rows)


def write_backlog(target):
    rng = random.Random(W.SEED + 41)
    rows = []
    d = dt.date(2026, 1, 5)
    while d <= W.AS_OF:
        for (name, code, lam, cust, wbar, backlog) in W.LINES:
            v = int(backlog / 52.0 * (0.7 + 0.6 * rng.random()) * 52 / 52)
            weekly = max(0, int(backlog * (0.85 + 0.3 * rng.random()) / 52.0 * 52 / 52))
            rows.append([d.isoformat(), code, name, max(0, int(backlog * (0.88 + 0.24 * rng.random())))])
        d += dt.timedelta(days=7)
    return _csv(os.path.join(target, FILES["backlog"]),
                ["week_ending", "line_code", "line_name", "alerts_awaiting_review"], rows)


def write_ledger(target):
    """the contractor's hours, with one credit note reissued under a second reference"""
    rng = random.Random(W.SEED + 53)
    rows = []
    tid = 7100
    for (y, q) in ((2026, 1), (2026, 2), (2026, 3), (2026, 4)):
        start = dt.date(y, 1 + 3 * (q - 1), 1)
        for i in range(34 + rng.randrange(0, 9)):
            tid += 1
            d = start + dt.timedelta(days=rng.randrange(0, 88))
            hours = round(2.5 + rng.lognormvariate(1.2, 0.5), 1)
            rate = 285.0 if (tid % 11) else 410.0
            rows.append(["TKT-%05d" % tid, d.isoformat(), "%d-Q%d" % (y, q), "%.1f" % hours,
                         "%.2f" % rate, "review", "REF-%06d" % (500000 + tid), ""])
        for j in range(2):
            tid += 1
            d = start + dt.timedelta(days=60 + j * 9)
            hours = -round(1.5 + rng.random() * 6, 1)
            rows.append(["TKT-%05d" % tid, d.isoformat(), "%d-Q%d" % (y, q), "%.1f" % hours,
                         "285.00", "credit note", "REF-%06d" % (500000 + tid), ""])
            rows.append(["TKT-%05d" % tid, d.isoformat(), "%d-Q%d" % (y, q), "%.1f" % hours,
                         "285.00", "credit note", "CRN-%06d" % (900000 + tid),
                         "reissued under the credit note series"])
    return _csv(os.path.join(target, FILES["ledger"]),
                ["ticket", "ticket_date", "quarter", "hours", "hourly_rate", "ticket_type",
                 "reference", "note"], rows)


def write_lists(target):
    """the screening list's versions: entries added and removed over the year"""
    rng = random.Random(W.SEED + 59)
    versions = []
    entries = {}
    eid = 3100
    for v, d in enumerate(["2026-01-15", "2026-04-15", "2026-07-15", "2026-10-15", "2027-01-15"], 1):
        added, removed = [], []
        for _ in range(18 + rng.randrange(0, 10)):
            eid += 1
            added.append("ENT-%05d" % eid)
            entries["ENT-%05d" % eid] = v
        if v > 1:
            live = [e for e, fv in entries.items() if fv < v]
            for e in sorted(live)[:: max(1, len(live) // (4 + v))][: 3 + v]:
                removed.append(e)
        versions.append({"version": "v%d" % v, "in_force_from": d,
                         "entries_added": sorted(added), "entries_removed": sorted(removed)})
    out = {"list": "consolidated sanctions and politically exposed persons list",
           "maintained_by": W.SUPERVISOR, "compiled": W.AS_OF.isoformat(), "versions": versions}
    path = os.path.join(target, FILES["lists"])
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    return versions


def write_matches(target, versions):
    rng = random.Random(W.SEED + 61)
    rows = []
    mid = 60500
    alive = {}
    for v in versions:
        for e in v["entries_added"]:
            alive[e] = v["in_force_from"]
    ents = sorted(alive)
    d = dt.date(2026, 1, 20)
    while d <= W.AS_OF:
        for _ in range(3 + rng.randrange(0, 5)):
            mid += 1
            e = ents[(mid * 7919) % len(ents)]
            if alive[e] > d.isoformat():
                continue
            cleared = rng.random() < 0.62
            rows.append(["MCH-%06d" % mid, d.isoformat(), "CU%07d" % (100000 + (mid * 104729) % 850000),
                         e, "cleared" if cleared else "escalated",
                         "AN%03d" % (1 + mid % 40)])
        d += dt.timedelta(days=4)
    return _csv(os.path.join(target, FILES["matches"]),
                ["match_id", "screened_on", "customer_ref", "list_entry", "outcome", "analyst"], rows)


def write_branches(target):
    """branch and staff footprint: context the bank holds, no part of the placement"""
    rng = random.Random(W.SEED + 67)
    rows = []
    for (name, code, lam, cust, wbar, backlog) in W.LINES:
        for region in ("Northland", "Auckland", "Waikato", "Wellington", "Canterbury", "Otago"):
            rows.append([code, name, region, 1 + rng.randrange(0, 14),
                         4 + rng.randrange(0, 40), round(0.6 + rng.random() * 2.4, 1)])
    return _csv(os.path.join(target, FILES["branches"]),
                ["line_code", "line_name", "region", "branches", "staff", "floor_area_000_sqm"], rows)


def write_training(target):
    rng = random.Random(W.SEED + 71)
    rows = []
    for (name, code, lam, cust, wbar, backlog) in W.LINES:
        for m in range(1, 13):
            rows.append([code, name, "2026-%02d" % m, 40 + rng.randrange(0, 260),
                         round(0.78 + rng.random() * 0.21, 3)])
    return _csv(os.path.join(target, FILES["training"]),
                ["line_code", "line_name", "month", "staff_in_scope", "completion_rate"], rows)


def write_base(target):
    """the customer base, in the bank's own wide monthly layout"""
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font
    rng = random.Random(W.SEED + 79)
    wb = Workbook()
    ws = wb.active
    ws.title = "Customers by line"
    ws["A1"] = "%s: customers by business line" % W.BANK
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Month end counts, thousands of customers. Management information pack."
    ws["A3"] = "Prepared by the finance data office, %s." % W.AS_OF.strftime("%d %B %Y")
    months = [sim.add_months(dt.date(2026, 1, 1), m) for m in range(13)]
    ws.cell(row=5, column=1, value="Line code").font = Font(bold=True)
    ws.cell(row=5, column=2, value="Business line").font = Font(bold=True)
    for j, mo in enumerate(months):
        c = ws.cell(row=5, column=3 + j, value=mo.strftime("%b %Y"))
        c.font = Font(bold=True)
        c.alignment = Alignment(horizontal="center")
    for i, (name, code, lam, cust, wbar, backlog) in enumerate(W.LINES):
        ws.cell(row=6 + i, column=1, value=code)
        ws.cell(row=6 + i, column=2, value=name)
        for j, mo in enumerate(months):
            ws.cell(row=6 + i, column=3 + j,
                    value=round(cust * (0.985 + 0.03 * rng.random()), 1))
    ws.cell(row=6 + len(W.LINES) + 1, column=2, value="Counts are thousands of customers with an open "
            "account at month end and exclude closed accounts.").font = Font(size=9, italic=True)
    for col, wd in (("A", 11), ("B", 24)):
        ws.column_dimensions[col].width = wd
    path = os.path.join(target, FILES["base"])
    wb.save(path)
    return path


def write_manifest(target, case_rows, alert_rows):
    rows = [[FILES["alerts"], str(len(alert_rows)), min(r["raised_at"] for r in alert_rows),
             max(r["stage_at"] for r in alert_rows), W.AS_OF.isoformat(),
             "every adjudication stage of every alert raised since January 2025"],
            [FILES["cases"], str(len(case_rows)), min(r["onset_month"] for r in case_rows),
             max(r["confirmed_month"] for r in case_rows), W.AS_OF.isoformat(),
             "every confirmed case the bank holds a record of, all versions"]]
    return _csv(os.path.join(target, FILES["manifest"]),
                ["file_name", "row_count", "earliest", "latest", "extracted", "scope"], rows)
