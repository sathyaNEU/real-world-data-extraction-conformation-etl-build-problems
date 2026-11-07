"""Cut the evidence pack from the simulation: the two case systems, the crew assignments, the crew register, the
timesheets by pay period, the payroll calendar and the 2027 work plan. Layer 1 is what Redbud's systems produce: a
case system replaced in June 2024 with the open cases migrated, the nurse line's interface opening cases of its own
beside the supervisors' reports, cases revised after entry, crews recoded at the March 2025 reorganisation, hours
by type with prior-period adjustments."""
import csv
import datetime as dt
import hashlib
import os

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

import postprocess as PP
import sim
import world as W

FILES = {
    "legacy": "ehs_case_log_2021-2024.csv",
    "cases": "case_management_export_2024-2026.xlsx",
    "assign": "crew_assignments_2020-2026.csv",
    "register": "crew_register_2026.xlsx",
    "hours": "timesheet_hours_by_pay_period_2021-2026.csv",
    "calendar": "payroll_calendar_2021-2027.csv",
    "plan": "work_plan_hours_2027.xlsx",
    "standard": "pinewater_contractor_safety_standard_cs4.pdf",
    "programme": "crew_safety_recognition_programme.pdf",
    "notice": "recognition_programme_2027_notice.docx",
    "nearmiss": "good_catch_reports_2025-2026.csv",
    "subs": "subcontractor_monthly_safety_2026.csv",
}
CLS_LEGACY = {"FA": "First aid", "MT": "Medical treatment", "RW": "Restricted work", "DA": "Days away"}
BODY = ["Hand/fingers", "Back", "Knee", "Ankle/foot", "Shoulder", "Eye", "Wrist", "Head/face", "Arm", "Leg"]
NATURE = ["Laceration", "Strain/sprain", "Contusion", "Foreign body", "Fracture", "Puncture", "Burn", "Insect sting",
          "Dermatitis", "Heat illness"]


def _rng(*keys):
    h = hashlib.blake2b(("|".join(str(k) for k in (W.SEED, "pack") + keys)).encode(), digest_size=8).digest()
    return np.random.default_rng(int.from_bytes(h, "little"))


def period_start(d):
    return W.HIST0 + dt.timedelta(days=14 * ((d - W.HIST0).days // 14))


def pay_date(d):
    """Pay day: the Friday after the pay period the day falls in ends."""
    return period_start(d) + dt.timedelta(days=13 + 5)


def mdY(d):
    return d.strftime("%m/%d/%Y")


def derive(S):
    """Turn the truth into the records each system holds."""
    rng = _rng("derive")
    crews = S["crews"]
    logged = [i for i in S["injuries"] if i["reported"] and W.HIST0 <= i["date"] <= W.HIST1]
    logged.sort(key=lambda i: (i["date"], i["emp"], i["cls"]))
    cases = []
    wo = 410000
    for n, i in enumerate(logged):
        wo += int(rng.integers(3, 40))
        if i["mutual_aid"]:
            job = "MA-%s-%02d" % (("SER", "TCE", "GFC", "ORC")[i["date"].year % 4], i["date"].month)
        elif i["unit"] == "tech":
            job = ("PW-MS-%s-%06d" if i["type"] == "MTR" else "PW-LT-%s-%06d") % (W.DCODE[i["work_district"]], wo)
        else:
            job = "PW-WO-%s-%06d" % (W.DCODE[i["work_district"]], wo)
        hh = int(rng.integers(7, 17))
        mm = int(rng.integers(0, 12)) * 5
        c = dict(emp=i["emp"], date=i["date"], loc=i["work_district"], time="%02d:%02d" % (hh, mm), job=job, cls=i["cls"],
                 unit=i["unit"], district=i["district"], type=i["type"], code=i["code"], mutual_aid=i["mutual_aid"],
                 body=BODY[int(rng.integers(len(BODY)))], nature=NATURE[int(rng.integers(len(NATURE)))],
                 cycle_day=i["cycle_day"], ci=i.get("ci"))
        # first entries: some medical-treatment cases go in as first aid and are revised once the clinic visit
        # is known (more often late in a crew's count); some restricted-work cases become days away when the
        # worker is kept home
        first = c["cls"]
        lag = 0
        late = c["unit"] == "crew" and (c["cycle_day"] or 0) >= 60
        if c["cls"] == "MT" and rng.random() < (0.40 if late else 0.12):
            first, lag = "FA", int(rng.integers(2, 13))
        elif c["cls"] == "RW" and rng.random() < 0.18:
            first, lag = "RW", int(rng.integers(2, 9))
            c["cls"] = "DA"
        c["first"], c["lag"] = first, lag
        c["days_away"] = int(rng.integers(1, 46)) if c["cls"] == "DA" else 0
        c["days_rw"] = int(rng.integers(2, 30)) if c["cls"] in ("RW", "DA") and (c["cls"] == "RW" or first == "RW") else 0
        c["entered"] = c["date"] + dt.timedelta(days=int(rng.integers(0, 3)))
        c["recurrence_of"] = None
        cases.append(c)
    # recurrences: the same injury flaring again weeks later, opened as a case of its own and linked to the first;
    # under 29 CFR 1904.6 it is not a new case
    spans = {}
    for (ci, s), tl in S["slots"].items():
        for k, (start, emp) in enumerate(tl):
            end = tl[k + 1][0] - dt.timedelta(days=1) if k + 1 < len(tl) else W.ASOF
            spans.setdefault(emp, []).append((start, end))
    for e in S["tech_ids"]:
        spans.setdefault(e, []).append((W.BURN0, W.ASOF))
    recur = []
    for c in cases:
        if c["cls"] in ("MT", "RW", "DA") and rng.random() < 0.07:
            when = c["date"] + dt.timedelta(days=int(rng.integers(20, 81)))
            if when > W.HIST1 or not any(a <= when <= b for a, b in spans.get(c["emp"], [])):
                continue
            r = dict(c, date=when, cls="MT" if rng.random() < 0.7 else "RW", first=None, lag=0, recurrence_of=c,
                     time="%02d:%02d" % (int(rng.integers(7, 17)), int(rng.integers(0, 12)) * 5),
                     entered=when + dt.timedelta(days=int(rng.integers(0, 3))), days_away=0)
            r["first"] = r["cls"]
            r["days_rw"] = int(rng.integers(2, 15)) if r["cls"] == "RW" else 0
            r["mutual_aid"] = False
            recur.append(r)
    cases = sorted(cases + recur, key=lambda c: (c["date"], c["emp"], c["time"]))
    # the nurse line (from the June 2024 cutover): a worker who calls it gets a case of its own, opened by the
    # line's interface as first aid, dated the day of the call, with no time of injury; the supervisor's report,
    # when there is one, is a separate case. Calls are kept clear of any other injury to the same worker within a
    # week, so every nurse-line case belongs to one injury.
    by_emp = {}
    for c in cases:
        by_emp.setdefault(c["emp"], []).append(c)
    lag_v = [k for k, _ in W.NURSE_LAG]
    lag_p = [p for _, p in W.NURSE_LAG]
    nurse = []
    for c in cases:
        if c["recurrence_of"] is not None or c["date"] < W.CUTOVER:
            continue
        if any(x is not c and abs((x["date"] - c["date"]).days) <= 7 for x in by_emp[c["emp"]]):
            continue
        if rng.random() >= W.NURSE_CALL[c["cls"]]:
            continue
        lag = lag_v[int(rng.choice(len(lag_v), p=lag_p))]
        when = c["date"] + dt.timedelta(days=lag)
        if when > W.LOG1 or not any(a <= when <= b for a, b in spans.get(c["emp"], [])):
            continue
        if lag == 0:
            job = c["job"]
        elif c["mutual_aid"]:
            job = c["job"]
        else:
            wo_n = int(rng.integers(400000, 999999))
            job = c["job"].rsplit("-", 1)[0] + "-%06d" % wo_n
        nurse.append(dict(c, date=when, time="", job=job, cls="FA", first="FA", lag=0, days_away=0, days_rw=0,
                          entered=when, recurrence_of=None, source="Nurse line", nurse_of=c, nurse_lag=lag))
        if c["cls"] == "FA" and rng.random() >= W.NURSE_ALSO_REPORTED:
            c["nurse_only"] = True
    for c in cases:
        c.setdefault("source", "Supervisor")
        c.setdefault("nurse_only", False)
    cases = sorted(cases + nurse, key=lambda c: (c["date"], c["emp"], c["time"], c["source"]))
    return dict(cases=cases)


def write_cases(S, D, target):
    rng = _rng("cases")
    legacy, new = [], []
    year_seq = {}
    seq = 1180
    for c in D["cases"]:
        if c.get("nurse_only"):
            continue          # a first-aid injury the nurse line handled and no supervisor reported
        in_legacy = c["date"] < W.CUTOVER
        last_change = c["entered"] + dt.timedelta(days=c["lag"])
        migrated = in_legacy and c["date"] >= W.CUTOVER - dt.timedelta(days=24) and (
            c["cls"] in ("DA", "RW") or last_change >= W.CUTOVER)
        orig = c["recurrence_of"]
        link_legacy = orig.get("legacy_no", "") if orig is not None else ""
        if in_legacy:
            y = c["date"].year
            year_seq[y] = year_seq.get(y, 0) + int(rng.integers(1, 3))
            c["legacy_no"] = "EHS-%d-%04d" % (y, year_seq[y])
            revs = [(1, c["first"], c["entered"])]
            if c["first"] != c["cls"] and (last_change < W.CUTOVER or not migrated):
                revs.append((2, c["cls"], last_change))
            for r, cls, when in revs:
                status = "Open" if (migrated and r == len(revs)) else "Closed"
                legacy.append([c["legacy_no"], c["emp"], mdY(c["date"]), c["time"], c["job"], c["loc"], CLS_LEGACY[cls],
                               c["days_away"] if cls == "DA" else 0,
                               c["days_rw"] if cls in ("RW", "DA") else 0, c["body"], c["nature"], mdY(when),
                               status, r, link_legacy])
        if not in_legacy or migrated:
            seq += int(rng.integers(1, 4))
            c["case_id"] = "CM-%07d" % seq
            ref = c.get("legacy_no", "") if migrated else ""
            link = (orig.get("case_id") or orig.get("legacy_no", "")) if orig is not None else ""
            if migrated:
                revs = [(1, c["cls"] if last_change < W.CUTOVER else c["first"], W.CUTOVER)]
                if revs[0][1] != c["cls"]:
                    revs.append((2, c["cls"], max(last_change, W.CUTOVER + dt.timedelta(days=1))))
            else:
                revs = [(1, c["first"], c["entered"])]
                if c["first"] != c["cls"]:
                    revs.append((2, c["cls"], last_change))
            nl = c["source"] == "Nurse line"
            for r, cls, when in revs:
                status = "Closed" if (nl or when < W.LOG1 - dt.timedelta(days=20)) else "Open"
                new.append([c["case_id"], ref, c["emp"], c["date"].isoformat(), c["time"], c["job"], c["loc"], cls,
                            c["days_away"] if cls == "DA" else 0, c["days_rw"] if cls in ("RW", "DA") else 0,
                            c["body"], c["nature"], r, when.isoformat(), status, link,
                            c["source"]])
    head = ["case_no", "employee_no", "injury_date", "injury_time", "job_ref", "district", "classification",
            "days_away", "days_restricted", "body_part", "nature", "entered", "status", "revision", "recurrence_of"]
    with open(os.path.join(target, FILES["legacy"]), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(head)
        for row in sorted(legacy, key=lambda r: (r[0], r[13])):
            w.writerow(row)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Cases"
    hnew = ["case_id", "legacy_case_no", "employee_id", "injury_date", "injury_time", "job_reference", "district",
            "osha_class", "days_away", "days_job_transfer_restriction", "body_part", "nature_of_injury", "revision",
            "revised_on", "case_status", "recurrence_of_case", "source"]
    ws.append(hnew)
    for row in sorted(new, key=lambda r: (r[0], r[12])):
        ws.append([None if v == "" else v for v in row])
    for cell in ws[1]:
        cell.font = Font(bold=True)
    widths = [12, 15, 12, 12, 11, 18, 12, 10, 10, 12, 14, 18, 9, 12, 11, 16, 12]
    for k, wdt in enumerate(widths):
        ws.column_dimensions[openpyxl.utils.get_column_letter(k + 1)].width = wdt
    ws.freeze_panes = "A2"
    cl = wb.create_sheet("Codes")
    for row in [["osha_class", "meaning"], ["FA", "First aid only (29 CFR 1904.7(b)(5)(ii)), not recordable"],
                ["MT", "Medical treatment beyond first aid"], ["RW", "Job transfer or restriction"],
                ["DA", "Days away from work"],
                ["revision", "1 is the case as first entered; a later revision replaces it"],
                ["legacy_case_no", "the EHS log's case number, for cases open at the 1 June 2024 migration"],
                ["recurrence_of_case", "the earlier case this one recurs from (the case or EHS log number)"],
                ["source", "Supervisor: the EHS office's case from the supervisor's injury report, classified "
                           "and revised by the EHS office; Nurse line: a case the 24-hour nurse line's interface "
                           "opens from the worker's call, recorded as first aid and not revised"]]:
        cl.append(row)
    cl.column_dimensions["A"].width = 16
    cl.column_dimensions["B"].width = 70
    path = os.path.join(target, FILES["cases"])
    wb.save(path)
    PP.normalize_ooxml(path, "CaseTrack Export", "CaseTrack Export", "2026-10-12T06:00:00Z", "2026-10-12T06:00:00Z",
                       excel=True, company=W.COMPANY)
    return len(legacy), len(new)


def write_assignments(S, target):
    rows = []
    crews = S["crews"]
    for (ci, s), tl in sorted(S["slots"].items()):
        c = crews[ci]
        for k, (start, emp) in enumerate(tl):
            end = tl[k + 1][0] - dt.timedelta(days=1) if k + 1 < len(tl) else None
            if end is not None and end < W.BURN0:
                continue
            # the reorganisation recoded the moved crews: the assignment ends the day before and restarts on it
            if c["code_new"] and start < W.RENAME and (end is None or end >= W.RENAME):
                rows.append([emp, c["code"], start.isoformat(), (W.RENAME - dt.timedelta(days=1)).isoformat()])
                rows.append([emp, c["code_new"], W.RENAME.isoformat(), end.isoformat() if end else ""])
            else:
                code = c["code_new"] if (c["code_new"] and start >= W.RENAME) else c["code"]
                rows.append([emp, code, start.isoformat(), end.isoformat() if end else ""])
    for ti, t in enumerate(S["techs"]):
        rows.append([S["tech_ids"][ti], t["team"], W.BURN0.isoformat(), ""])
    rows.sort(key=lambda r: (r[0], r[2]))
    with open(os.path.join(target, FILES["assign"]), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["employee_id", "crew_or_team", "assigned_from", "assigned_to"])
        w.writerows(rows)
    return len(rows)


def write_register(S, target):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Crews"
    ws.append(["unit_code", "unit_type", "type_name", "district", "status", "recoded_to", "recode_effective"])
    rows = []
    for c in S["crews"]:
        nm = W.CREW_TYPES[c["type"]]["name"]
        if c["code_new"]:
            rows.append([c["code"], c["type"], nm, c["district"], "Recoded", c["code_new"], W.RENAME.isoformat()])
            rows.append([c["code_new"], c["type"], nm, c["district_new"], "Active", "", ""])
        else:
            rows.append([c["code"], c["type"], nm, c["district"], "Active", "", ""])
    for t, spec in W.TECH_TYPES.items():
        for dist in W.DISTRICTS:
            rows.append(["%s-%s" % (W.DCODE[dist], t), t, spec["name"] + " (technician team)", dist, "Active", "", ""])
    for r in sorted(rows):
        ws.append([None if v == "" else v for v in r])
    for cell in ws[1]:
        cell.font = Font(bold=True)
    for k, wdt in enumerate([12, 10, 34, 12, 10, 12, 16]):
        ws.column_dimensions[openpyxl.utils.get_column_letter(k + 1)].width = wdt
    ws.freeze_panes = "A2"
    path = os.path.join(target, FILES["register"])
    wb.save(path)
    PP.normalize_ooxml(path, W.PEOPLE["ops"], W.PEOPLE["ops"], "2025-03-03T14:12:00Z", "2026-09-29T15:40:00Z",
                       excel=True, company=W.COMPANY)
    return len(rows)


def write_hours(S, target):
    """One row per unit and pay period as first approved, and a prior-period adjustment row, posted in a later pay
    period, for the timesheets a supervisor corrected after approval (missed overtime, a day keyed twice)."""
    rng = _rng("hours")
    rows = []
    last = W.HIST1 - dt.timedelta(days=13)
    for (code, ps, _wd), r in sorted(S["weekly"].items()):
        if not (W.HIST0 <= ps and ps + dt.timedelta(days=13) <= W.HIST1):
            continue
        reg, ot = r["regular"], r["overtime"]
        adj = None
        if reg + ot > 0 and rng.random() < 0.015:
            post = ps + dt.timedelta(days=14 * int(rng.integers(1, 3)))
            if post <= last:
                d_ot = float(rng.choice([4.0, 6.0, 8.0, 10.0, 12.0, 16.0]))
                d_reg = -8.0 if (reg >= 8.0 and rng.random() < 0.3) else 0.0
                adj = (post, d_reg, d_ot)
                reg, ot = reg - d_reg, ot - d_ot
                if ot < 0:
                    adj = (post, d_reg, d_ot + ot)
                    ot = 0.0
        rows.append([ps.isoformat(), (ps + dt.timedelta(days=13)).isoformat(), code, r["district"], r["type"],
                     "%.2f" % reg, "%.2f" % ot, "%.2f" % r["pto"], "%.2f" % r["holiday"], "%.2f" % r["mutual_aid"], ""])
        if adj:
            post, d_reg, d_ot = adj
            rows.append([post.isoformat(), (post + dt.timedelta(days=13)).isoformat(), code, r["district"], r["type"],
                         "%.2f" % d_reg, "%.2f" % d_ot, "0.00", "0.00", "0.00", ps.isoformat()])
    rows.sort(key=lambda x: (x[0], x[2], x[10]))
    with open(os.path.join(target, FILES["hours"]), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["pay_period_start", "pay_period_end", "unit_code", "district", "unit_type", "regular_hours",
                    "overtime_hours", "pto_hours", "holiday_hours", "mutual_aid_hours", "adjusts_pay_period"])
        w.writerows(rows)
    return len(rows)


def write_calendar(target):
    rows = []
    ps = W.HIST0
    while ps.year <= 2027:
        year = (ps + dt.timedelta(days=13 + 5)).year
        rows.append([ps, ps + dt.timedelta(days=13), ps + dt.timedelta(days=18), year])
        ps += dt.timedelta(days=14)
    out, n, cur = [], 0, None
    for ps, pe, pd, y in rows:
        n = n + 1 if y == cur else 1
        cur = y
        out.append([y, n, ps.isoformat(), pe.isoformat(), pd.isoformat()])
    with open(os.path.join(target, FILES["calendar"]), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["payroll_year", "period", "period_start", "period_end", "pay_date"])
        w.writerows(out)
    return len(out)


def plan_hours(S):
    """2027 planned hours worked by district, unit type and quarter: the 2025 hours on Pinewater work grown by each
    district's 2027 release, split by quarter on the plan's own profile."""
    base = {}
    for (code, ps, _wd), r in S["weekly"].items():
        if dt.date(2025, 1, 1) <= ps <= dt.date(2025, 12, 31):
            k = (r["district"], r["type"])
            base[k] = base.get(k, 0.0) + r["regular"] + r["overtime"]
    plan = {}
    for (dist, t), h in sorted(base.items()):
        tot = round(h * W.PLAN_GROWTH[dist] / 100) * 100
        q = [round(tot * s / 100) * 100 for s in W.QUARTER_SHARE]
        q[-1] = tot - sum(q[:-1])
        plan[(dist, t)] = q
    return plan


def write_plan(S, target):
    plan = plan_hours(S)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "2027 hours"
    ws.append(["Redbud Line Services - Pinewater EMC 2027 work plan: hours worked by district and unit type"])
    ws.append(["Hours are planned hours worked on Pinewater work (regular and overtime), from Pinewater's 2027 work "
               "release of 14 October 2026."])
    ws.append([None])
    ws.append(["District", "Unit type", "Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027", "2027"])
    order = list(W.CREW_TYPES) + list(W.TECH_TYPES)
    for dist in W.DISTRICTS:
        for t in order:
            q = plan[(dist, t)]
            ws.append([dist, t] + q + [sum(q)])
    tot = [sum(plan[(d, t)][k] for d in W.DISTRICTS for t in order) for k in range(4)]
    ws.append(["All districts", "All"] + tot + [sum(tot)])
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"].font = Font(italic=True, size=9)
    for cell in ws[4]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="7A2E1F")
    for row in ws.iter_rows(min_row=5, max_row=ws.max_row, min_col=3, max_col=7):
        for cell in row:
            cell.number_format = "#,##0"
    for k, wdt in enumerate([14, 10, 12, 12, 12, 12, 13]):
        ws.column_dimensions[openpyxl.utils.get_column_letter(k + 1)].width = wdt
    key = wb.create_sheet("Unit types")
    key.append(["Unit type", "Description"])
    for t, spec in list(W.CREW_TYPES.items()) + list(W.TECH_TYPES.items()):
        key.append([t, spec["name"] + (" crews" if t in W.CREW_TYPES else " technicians")])
    key.column_dimensions["A"].width = 10
    key.column_dimensions["B"].width = 36
    path = os.path.join(target, FILES["plan"])
    wb.save(path)
    PP.normalize_ooxml(path, W.PEOPLE["ops"], W.PEOPLE["ops"], "2026-10-14T13:05:00Z", "2026-10-15T09:22:00Z",
                       excel=True, company=W.COMPANY)
    return plan
