"""Write the bundle the bank would hand over."""
import csv
import datetime as dt
import json
import os
import random

import sim
import world as W

SHUT = {d for d, _ in W.HOLIDAYS}


def open_day(d):
    """the first day from d on which the bank is open"""
    while d.weekday() >= 5 or d in SHUT:
        d += dt.timedelta(days=1)
    return d


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
    "closed": "bank_closed_days.csv",
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
    """the line code the record carries, which the July 2026 reorganisation changed.

    Some feeds went on writing the retired code for a while after the merger, which is why the line
    structure register carries the mapping rather than a cut-over date alone.
    """
    cur = CODE[name]
    if cur not in OLD_BY_CURRENT:
        return cur
    olds = OLD_BY_CURRENT[cur]
    if when >= W.REORG:
        late = (when - W.REORG).days
        if late < 150 and (when.day * 7 + when.month) % 11 < (4 if late < 60 else 2):
            return olds[(when.month + when.day) % len(olds)]
        return cur
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
    earlier = {}
    for name in [l[0] for l in W.LINES]:
        earlier.setdefault(name, [])
        for c in cases[name]:
            if c["detected"] > W.AS_OF:
                continue                      # the bank holds no record of a case nobody has seen
            cid += 1
            lag = W.CONFIRM_LAG[[l[1] for l in W.LINES if l[0] == name][0]]
            conf = sim.add_months(c["detected"], int(rng.expovariate(1.0 / max(0.25, lag))))
            if conf > W.AS_OF:
                conf = W.AS_OF
            cur = "AUD" if (cid % 23 == 0) else "NZD"
            amt = round(8000 + rng.lognormvariate(10.4, 0.9), 2)
            ref = "CU%07d" % (100000 + (cid * 7919) % 850000)
            if earlier[name] and rng.random() < 0.062:
                ref = earlier[name][rng.randrange(0, len(earlier[name]))]
            else:
                earlier[name].append(ref)
            rows.append({"seq": cid, "case_id": "", "customer_ref": ref,
                         "line_code": recorded_line(name, c["onset"]),
                         "typology": c["typology"],
                         "onset_month": c["onset"].strftime("%Y-%m"),
                         "first_seen_month": c["detected"].strftime("%Y-%m"),
                         "confirmed_month": conf.strftime("%Y-%m"),
                         "disposition": "confirmed", "record_version": "1",
                         "amount": "%.2f" % amt, "currency": cur, "line": name})
    # cases amended after confirmation, a few of them twice: every version is kept
    amended = []
    for r in rows:
        if rng.random() > 0.011:
            continue
        v2 = dict(r)
        v2["record_version"] = "2"
        v2["amount"] = "%.2f" % round(float(r["amount"]) * (0.74 + rng.random() * 0.62), 2)
        amended.append(v2)
        if rng.random() < 0.17:
            v3 = dict(v2)
            v3["record_version"] = "3"
            v3["amount"] = "%.2f" % round(float(v2["amount"]) * (0.81 + rng.random() * 0.45), 2)
            amended.append(v3)
    # the cases put to the head of financial crime and not accepted: no confirmed month
    withdrawn = []
    for name in [l[0] for l in W.LINES]:
        own = [r for r in rows if r["line"] == name]
        for _ in range(int(round(0.068 * len(own)))):
            src = own[rng.randrange(0, len(own))]
            cid += 1
            onset = dt.date(int(src["onset_month"][:4]), int(src["onset_month"][5:7]), 1)
            withdrawn.append({"seq": cid, "case_id": "",
                              "customer_ref": "CU%07d" % (100000 + (cid * 7919) % 850000),
                              "line_code": recorded_line(name, onset),
                              "typology": src["typology"],
                              "onset_month": src["onset_month"],
                              "first_seen_month": src["first_seen_month"],
                              "confirmed_month": "",
                              "disposition": "withdrawn", "record_version": "1",
                              "amount": "%.2f" % round(8000 + rng.lognormvariate(10.4, 0.9), 2),
                              "currency": "AUD" if (cid % 23 == 0) else "NZD", "line": name})
    rows.extend(withdrawn)
    # the register numbers a case when it is opened: mostly the next number, now and then a jump
    # where numbers were taken by cases that were never registered
    nxt = 41207
    ident = {}
    for r in sorted(rows, key=lambda z: (z["first_seen_month"], (z["seq"] * 48611) % 99991)):
        u = rng.random()
        nxt += 1 if u < 0.86 else (2 if u < 0.95 else 2 + int(rng.expovariate(0.35)))
        ident[r["seq"]] = "CAS-%06d" % nxt
    for r in rows + amended:
        r["case_id"] = ident[r["seq"]]
    rows.extend(amended)
    path = os.path.join(target, FILES["cases"])
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CASE_COLS, lineterminator="\n", extrasaction="ignore")
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
                serves = {"card disputes": [("Cards", 1.0)],
                          "payment screening": [("Retail payments", 0.82),
                                                ("FX and remittance", 1.0)],
                          "trade documents": [("Trade finance", 0.88),
                                              ("Correspondent banking", 1.0)],
                          "onboarding": [("Deposits", 0.76), ("Private wealth", 1.0)],
                          "transaction monitoring": [("Business lending", 0.71),
                                                     ("Retail payments", 1.0)],
                          "sanctions screening": [("FX and remittance", 0.64),
                                                  ("Correspondent banking", 1.0)]}[q]
                u = rng.random()
                line = next(nm for nm, cut in serves if u <= cut)
                ref = "A%08d" % (200000 + (aid * 104729) % 700000)
                batch = "%s-%s-%02d" % (q[:3].upper(), raised.strftime("%Y%m"), 1 + (aid % 7))
                an = "AN%03d" % (1 + aid % 40)

                def put(stage, at, outcome="", analyst="", _a=aid, _q=qname, _r=ref, _ra=raised,
                        _b=batch):
                    if at > W.AS_OF:
                        return                 # the extract holds nothing after the day it was pulled
                    rows.append({"alert_id": "AL-%07d" % _a, "queue": _q, "customer_ref": _r,
                                 "line_code": recorded_line(line, _ra),
                                 "raised_at": _ra.isoformat(), "stage": stage,
                                 "stage_at": at.isoformat(), "outcome": outcome,
                                 "analyst": analyst, "batch_id": _b})

                put("raised", raised)
                if rng.random() < 0.019:
                    continue                   # still in the queue at the pull, no triage row yet
                closed = open_day(raised + dt.timedelta(days=1 + int(rng.lognormvariate(0.9, 0.85))))
                esc = rng.random() < 0.06
                put("triaged", closed, "escalated" if esc else "closed", an)
                if esc:
                    put("escalated", open_day(closed + dt.timedelta(days=2 + rng.randrange(0, 9))),
                        "with investigations", an)
                elif rng.random() < 0.014:     # reopened on new information, then closed again
                    ro = open_day(closed + dt.timedelta(days=5 + rng.randrange(0, 50)))
                    an2 = "AN%03d" % (1 + (aid * 3) % 40)
                    put("reopened", ro, "", an2)
                    put("triaged", open_day(ro + dt.timedelta(days=1 + rng.randrange(0, 9))),
                        "closed", an2)
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
                     "superseded", cur, note.split(" on ")[0]])
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
        rows.append([cu, a, "matched on account number" if rng.random() < 0.23 else
                     "matched on name, date of birth and account", "single"])
        if rng.random() < 0.009:            # two candidates the data office could not separate
            rows.append([cu, alerts[(i * 104729 + 17) % len(alerts)],
                         "matched on name and date of birth", "one of two candidates"])
    return _csv(os.path.join(target, FILES["crosswalk"]),
                ["case_customer_ref", "alert_customer_ref", "match_basis", "resolution"], rows)


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
    """the contractor's hours.

    One reversal a quarter was reissued weeks later under the credit note reference series, so the
    ledger reverses that ticket's hours twice. Nothing says so: each credit note names the ticket it
    reverses, and the pair reverses more hours than that ticket was ever billed.
    """
    rng = random.Random(W.SEED + 53)
    rows = []
    tid = 7100
    for (y, q) in ((2026, 1), (2026, 2), (2026, 3), (2026, 4)):
        start = dt.date(y, 1 + 3 * (q - 1), 1)
        billed = []
        for i in range(int((39 if q <= 2 else 46) + rng.randrange(0, 8))):
            d = start + dt.timedelta(days=rng.randrange(0, 88))
            hours = round(2.8 + rng.lognormvariate(1.42, 0.5), 1)
            kind = "review"
            rate = 285.0
            u = rng.random()
            if u < 0.055:                         # the expert's own rate, which the card carries
                kind, rate = "expert testimony", 410.0
            elif u < 0.105:                       # a rate agreed outside the schedule
                rate = rng.choice([312.5, 325.0, 340.0, 298.0])
            billed.append((d, hours, kind, rate))
        billed.sort(key=lambda z: z[0])           # the ticket system numbers in date order
        out = []
        for (d, hours, kind, rate) in billed:
            tid += 1 + (1 if rng.random() < 0.18 else 0)
            tk = "TKT-%05d" % tid
            out.append([tk, d.isoformat(), "%d-Q%d" % (y, q), "%.1f" % hours, "%.2f" % rate, kind,
                        "REF-%06d" % (500000 + tid), ""])
        rows += out
        # two reversals a quarter, one of them reissued weeks later under the credit note series
        top = sorted(range(len(out)), key=lambda i: -float(out[i][3]))[:7]
        first = top[rng.randrange(0, len(top))]
        other = (tid * 7 + 29) % len(out)
        while other == first:
            other = (other + 13) % len(out)
        pick = [first, other]
        qend = dt.date(y, 1 + 3 * (q - 1), 1) + dt.timedelta(days=88)
        qend = min(qend, dt.date(y, 12, 31) if q == 4 else dt.date(y, 3 * q, 28))
        for j, ix in enumerate(pick):
            tk, td, th = out[ix][0], dt.date.fromisoformat(out[ix][1]), float(out[ix][3])
            tid += 1
            d = min(qend, td + dt.timedelta(days=11 + rng.randrange(0, 40)))
            rows.append(["TKT-%05d" % tid, d.isoformat(), "%d-Q%d" % (y, q), "%.1f" % (-th),
                         "285.00", "credit note", "REF-%06d" % (500000 + tid), tk])
            if j == 0:
                again = min(qend, d + dt.timedelta(days=17 + rng.randrange(0, 30)))
                tid += 1
                rows.append(["TKT-%05d" % tid, again.isoformat(), "%d-Q%d" % (y, q), "%.1f" % (-th),
                             "285.00", "credit note", "CRN-%06d" % (900000 + tid), tk])
    return _csv(os.path.join(target, FILES["ledger"]),
                ["ticket", "ticket_date", "quarter", "hours", "hourly_rate", "ticket_type",
                 "reference", "reverses_ticket"], rows)


def write_lists(target):
    """the screening list's versions: entries added and removed over the year"""
    rng = random.Random(W.SEED + 59)
    versions = []
    entries = {}
    gone = set()
    eid = 3100
    for v, d in enumerate(["2026-01-22", "2026-03-06", "2026-06-11", "2026-09-30", "2026-12-17"], 1):
        added, removed = [], []
        for _ in range(int(14 + rng.expovariate(1.0 / 46))):
            eid += 1
            added.append("ENT-%05d" % eid)
            entries["ENT-%05d" % eid] = v
        if v > 1:
            live = sorted(e for e, fv in entries.items() if fv < v and e not in gone)
            rng.shuffle(live)
            for e in live[: 5 + int(rng.expovariate(1.0 / 11))]:
                removed.append(e)
                gone.add(e)
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
    alive, gone = {}, {}
    for v in versions:
        for e in v["entries_added"]:
            alive[e] = v["in_force_from"]
        for e in v["entries_removed"]:
            gone[e] = v["in_force_from"]
    ents = sorted(alive)
    d = dt.date(2026, 1, 20)
    while d <= W.AS_OF:
        for _ in range(6 + rng.randrange(0, 9)):
            mid += 1
            e = ents[(mid * 7919) % len(ents)]
            if alive[e] > d.isoformat() or gone.get(e, "9999") <= d.isoformat():
                continue                       # the entry was not on the list that day
            cleared = rng.random() < 0.62
            rows.append(["MCH-%06d" % mid, d.isoformat(), "CU%07d" % (100000 + (mid * 104729) % 850000),
                         e, "cleared" if cleared else "escalated",
                         "AN%03d" % (1 + mid % 40)])
        d += dt.timedelta(days=4)
    return _csv(os.path.join(target, FILES["matches"]),
                ["match_id", "screened_on", "customer_ref", "list_entry", "outcome", "analyst"], rows)


def write_closed_days(target):
    """the days the bank is closed, as the operations office keeps them"""
    rows = [[d.isoformat(), nm, "national" if nm not in ("Wellington Anniversary",) else "regional"]
            for d, nm in W.HOLIDAYS]
    return _csv(os.path.join(target, FILES["closed"]),
                ["closed_on", "occasion", "scope"], rows)


def write_branches(target):
    """branch and staff footprint: context the bank holds, no part of the placement"""
    rng = random.Random(W.SEED + 67)
    rows = []
    share = (("Northland", 0.06), ("Auckland", 0.34), ("Waikato", 0.11), ("Wellington", 0.19),
             ("Canterbury", 0.21), ("Otago", 0.09))
    for (name, code, lam, cust, wbar, backlog) in W.LINES:
        sites = max(3, int(round(2.0 + cust / 26.0)))
        for region, sh in share:
            b = max(0, int(round(sites * sh * (0.75 + 0.5 * rng.random()))))
            if b == 0 and rng.random() < 0.45:
                b = 1
            if b == 0:
                continue
            staff = int(round(b * (5.2 + 3.1 * rng.random())))
            rows.append([code, name, region, b, staff, round(b * (0.19 + 0.08 * rng.random()), 1)])
    return _csv(os.path.join(target, FILES["branches"]),
                ["line_code", "line_name", "region", "branches", "staff", "floor_area_000_sqm"], rows)


def write_training(target):
    rng = random.Random(W.SEED + 71)
    rows = []
    for (name, code, lam, cust, wbar, backlog) in W.LINES:
        n = max(18, int(round(28 + cust * 1.35)))
        rate = 0.74 + rng.random() * 0.14
        for m in range(1, 13):
            n = max(12, n + int(round(rng.gauss(0, max(1.0, n * 0.016)))))
            rate = min(0.999, max(0.6, rate + rng.gauss(0.013, 0.012)))
            rows.append([code, name, "2026-%02d" % m, n, round(rate, 3)])
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
        drift = 1.0
        trend = 1.0 + rng.gauss(0.004, 0.006)
        for j, mo in enumerate(months):
            drift *= trend * (1.0 + rng.gauss(0, 0.004))
            ws.cell(row=6 + i, column=3 + j,
                    value=round(cust * drift, 1 if cust >= 10 else 2))
    ws.cell(row=6 + len(W.LINES) + 1, column=2, value="Counts are thousands of customers with an open "
            "account at month end and exclude closed accounts.").font = Font(size=9, italic=True)
    for col, wd in (("A", 11), ("B", 24)):
        ws.column_dimensions[col].width = wd
    path = os.path.join(target, FILES["base"])
    wb.save(path)
    return path


def write_manifest(target, case_rows, alert_rows):
    """what the data office handed over, each file with its own row count and range"""
    def span(name, col_lo, col_hi):
        import csv as _csv_mod
        with open(os.path.join(target, name), encoding="utf-8") as fh:
            rd = list(_csv_mod.DictReader(fh))
        lo = min(r[col_lo] for r in rd if r[col_lo])
        hi = max(r[col_hi] for r in rd if r[col_hi])
        return str(len(rd)), lo, hi

    scope = {
        FILES["alerts"]: "every adjudication stage recorded for every alert raised since January 2025",
        FILES["cases"]: "every case put to the head of financial crime, each version as it was written",
        FILES["backlog"]: "the alerts awaiting a first review in each queue at each week ending",
        FILES["crosswalk"]: "the case system's customer reference against the alert system's",
        FILES["ledger"]: "every ticket the specialist review contractor has billed",
        FILES["matches"]: "every screening match recorded against a list entry",
        FILES["branches"]: "the branch and staff footprint by business line and region",
        FILES["training"]: "financial crime training completion by business line and month",
        FILES["closed"]: "the days the bank is closed",
    }
    cols = {
        FILES["alerts"]: ("raised_at", "stage_at"),
        FILES["cases"]: ("onset_month", "first_seen_month"),
        FILES["backlog"]: ("week_ending", "week_ending"),
        FILES["ledger"]: ("ticket_date", "ticket_date"),
        FILES["matches"]: ("screened_on", "screened_on"),
        FILES["training"]: ("month", "month"),
        FILES["closed"]: ("closed_on", "closed_on"),
    }
    rows = []
    for name in (FILES["alerts"], FILES["cases"], FILES["backlog"], FILES["crosswalk"],
                 FILES["ledger"], FILES["matches"], FILES["branches"], FILES["training"],
                 FILES["closed"]):
        if name in cols:
            n, lo, hi = span(name, *cols[name])
        else:
            with open(os.path.join(target, name), encoding="utf-8") as fh:
                n, lo, hi = str(sum(1 for _ in fh) - 1), "", ""
        rows.append([name, n, lo, hi, W.AS_OF.isoformat(), scope[name]])
    return _csv(os.path.join(target, FILES["manifest"]),
                ["file_name", "row_count", "earliest", "latest", "extracted", "scope"], rows)
