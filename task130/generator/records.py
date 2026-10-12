"""The pack's flat files: the claims register extract, the legacy payroll history, the 2026 HCM pay lines, the HCM job
profile crosswalk, the cost centre directory, the carrier notice log, Stoneleigh's loss run, the patient safety event
extract and the extract log."""
from __future__ import annotations

import csv
import datetime as dt

import common as K
import world as WD


def write_csv(path, header, rows, crlf=False):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n" if crlf else "\n")
        w.writerow(header)
        n = 0
        for r in rows:
            w.writerow(["" if v is None else v for v in r])
            n += 1
    return n


def money(x):
    return "" if x is None else "%.2f" % x


def iso(d):
    return "" if d is None else d.isoformat()


def us(d):
    return "" if d is None else "%02d/%02d/%04d" % (d.month, d.day, d.year)


# ------------------------------------------------------------------------------------------------ claims register
REGISTER_COLS = ["claim_no", "incident_no", "defendant_seq", "clinician_id", "defendant_role", "specialty",
                 "coverage_line", "entity_at_incident", "incident_date", "claim_made_date", "matter_type", "allegation",
                 "status", "closed_date", "indemnity_paid", "defense_paid", "indemnity_reserve", "defense_reserve",
                 "prior_claim_no", "valuation_date"]


def register_rows(rows):
    out = []
    for r in sorted(rows, key=lambda r: (r["claim_no"], r["defendant_seq"])):
        out.append([r["claim_no"], r["incident_no"], r["defendant_seq"], r["clinician_id"], r["defendant_role"],
                    r["specialty"], r["coverage_line"], r["entity_at_incident"], iso(r["incident_date"]),
                    iso(r["claim_made_date"]), r["matter_type"], r["allegation"], r["status"], iso(r["closed_date"]),
                    money(r["indemnity_paid"]), money(r["defense_paid"]), money(r["indemnity_reserve"]),
                    money(r["defense_reserve"]), r["prior_claim_no"], K.VALUATION.isoformat()])
    return out


# ------------------------------------------------------------------------------------------------ legacy payroll
PAYROLL_COLS = ["pay_month", "employee_id", "job_code", "job_title", "cost_centre", "entity_code", "fte", "emp_status"]
TITLE16 = {j[0]: j[3].upper().replace(" - ", "-") for j in K.JOBS}
TITLE20 = {j[0]: j[3] for j in K.JOBS}


def payroll_rows(W):
    out = []
    for (p, y, m, f) in WD.position_months(W, K.LEGACY_FIRST, K.LEGACY_LAST):
        new_codes = (y, m) >= K.CODE_SWITCH
        code = K.JOB[p.job][2] if new_codes else K.JOB[p.job][1]
        title = TITLE20[p.job] if new_codes else TITLE16[p.job]
        last = dt.date(y, m, K.days_in_month(y, m))
        status = "L" if (y, m) in p.leave else ("T" if p.end is not None and p.end <= last and
                                                  not _continues(W, p, y, m) else "A")
        out.append((K.month_key(y, m), p.emp, code, title, p.cc, p.entity, "%.1f" % f, status))
    out.sort(key=lambda r: (r[0], r[1], r[4]))
    return out


def _continues(W, p, y, m):
    """A position ending in a month whose employee holds another position the next month (a transfer)."""
    nxt = dt.date(y + (m == 12), m % 12 + 1, 1)
    return any(q.emp == p.emp and q is not p and q.start <= nxt and (q.end is None or q.end >= nxt)
               for q in W.by_emp.get(p.emp, ()))


# ------------------------------------------------------------------------------------------------ HCM pay lines
HCM_COLS = ["worker_id", "position_id", "work_month", "earning_code", "earning_description", "hours", "fte",
            "job_profile_code", "job_profile", "cost_centre", "home_entity", "pay_group"]
EARNINGS = {"REG": "Regular salary", "PTO": "Paid time off", "CALL": "Call pay", "ADMIN": "Administrative stipend",
            "LOA": "Leave of absence (unpaid)"}
PROFILE_NAME = {code: name for j in K.JOBS for code, name in j[5]}


def hcm_rows(W):
    rng = K.stream("hcm-lines")
    admin = set()
    for p in sorted(W.positions, key=lambda p: p.pid):
        if rng.random() < 0.06 and K.JOB[p.job][6] in ("hosp", "phys"):
            admin.add(p.pid)
    out = []
    for p in sorted(W.positions, key=lambda p: p.pid):
        home = WD.home_entity(W, p.emp)
        group = "PHYS" if p.job not in ("NP", "PA", "CRNA", "CNM", "PSYC") else "APC"
        if p.job in ("RES", "FEL"):
            group = "GME"
        for (y, m) in K.months(K.HCM_FIRST, K.HCM_LAST):
            f = p.paid(y, m)
            if f is None:
                continue
            fte = p.fte_in(y, m)
            wm = K.month_key(y, m)
            base = [p.emp, p.pid, wm]
            tail = ["%.2f" % fte, p.hcm_profile, PROFILE_NAME[p.hcm_profile], p.cc, home, group]
            if (y, m) in p.leave:
                out.append(base + ["LOA", EARNINGS["LOA"], "0.00"] + tail)
                continue
            std = 173.33 * f
            out.append(base + ["REG", EARNINGS["REG"], "%.2f" % std] + tail)
            if rng.random() < 0.42:
                out.append(base + ["PTO", EARNINGS["PTO"], "%.2f" % float(8 * rng.integers(1, 6))] + tail)
            if K.JOB[p.job][6] == "hosp" and rng.random() < 0.6:
                out.append(base + ["CALL", EARNINGS["CALL"], "%.2f" % float(rng.integers(12, 61))] + tail)
            if p.pid in admin:
                out.append(base + ["ADMIN", EARNINGS["ADMIN"], "0.00"] + tail)
    out.sort(key=lambda r: (r[2], r[0], r[1], r[3]))
    return out


CROSSWALK_COLS = ["job_profile_code", "job_profile", "legacy_job_code", "legacy_job_title", "effective_date"]


def crosswalk_rows():
    out = []
    for j in K.JOBS:
        for code, name in j[5]:
            out.append([code, name, j[2], TITLE20[j[0]], "2026-01-01"])
    out.sort()
    return out


DIRECTORY_COLS = ["cost_centre", "company", "entity_code", "entity_name", "department", "effective_from",
                  "effective_to", "status"]


def directory_rows():
    out = []
    for e in K.ENTITY_ORDER:
        ent = K.ENTITIES[e]
        for suffix, dept, _ in K.DEPTS[e]:
            frm = "2012-01-01"
            if e == "BCH":
                frm = "2019-07-01"
            if e == "BCH" and suffix == "7110":
                frm = "2026-10-01"
            if e == "CMG" and suffix == "7810":
                frm = "2018-03-01"
            out.append([K.cost_centre(e, suffix), ent["company"], e, ent["name"], dept, frm, "", "Active"])
    # retired cost centres the directory still carries
    out.append(["110-6615", "110", "AMC", "Alderwick Medical Center", "Hospital APC Services (former)", "2012-01-01",
                "2019-06-30", "Inactive"])
    out.append(["300-7125", "300", "CMG", "Corvane Medical Group", "Riverside Family Medicine (closed)", "2012-01-01",
                "2021-03-31", "Inactive"])
    out.sort()
    return out


# ------------------------------------------------------------------------------------------------ carrier notices
NOTICE_COLS = ["notice_no", "incident_no", "entity_code", "carrier", "sent_date", "event_date", "event_category"]


def notice_rows(incidents, notice_only):
    out = []
    for inc in incidents + notice_only:
        if inc.notice is None:
            continue
        out.append([inc.notice_no, inc.incident_no, inc.entity, K.CARRIERS[K.ENTITIES[inc.entity]["carrier"]],
                    iso(inc.notice), iso(inc.date), inc.allegation])
    out.sort()
    return out


# ------------------------------------------------------------------------------------------------ Stoneleigh loss run
SC_COLS = ["POLICY_NO", "POL_EFF", "POL_EXP", "INSURED_NAME", "CLAIM_NO", "INSURED_REF", "DATE_OF_LOSS",
           "DATE_RPTD", "CLM_TYPE", "CLM_STATUS", "IND_PAID", "EXP_PAID", "IND_RESV", "EXP_RESV", "TOTAL_INCURRED",
           "VALUATION_DT"]
SC_NAME = {"CMG": "CORVANE MEDICAL GROUP", "BCH": "BRENNICK COMMUNITY HOSP"}
SC_TYPE = {"Claim": "CLM", "Suit": "SUIT", "Incident": "INC"}
SC_STATUS = {"Open": "O", "Closed": "C", "Reopened": "R"}


def sc_rows(recs, nums, V):
    out = []
    for r in recs:
        if K.ENTITIES[r["entity"]]["carrier"] != "SC":
            continue
        ref = "".join(ch for ch in r["ref"] if ch.isalnum())
        tot = r["paid_ind"] + r["paid_exp"] + r["res_ind"] + r["res_exp"]
        out.append([r["policy"], us(r["period"][0]), us(r["period"][1]), SC_NAME[r["entity"]], nums[r["incident_no"]],
                    ref, us(r["date_of_loss"]), us(r["created"]), SC_TYPE[r["ctype"]], SC_STATUS[r["status"]],
                    "%.2f" % r["paid_ind"], "%.2f" % r["paid_exp"], "%.2f" % r["res_ind"], "%.2f" % r["res_exp"],
                    "%.2f" % tot, us(V)])
    out.sort(key=lambda x: (x[0], x[4]))
    return out


# ------------------------------------------------------------------------------------------------ safety events
SAFETY_COLS = ["event_id", "event_date", "entity_code", "department", "event_type", "harm_level", "reporter_role",
               "rm_referral"]
EVENT_TYPES = [("Medication", 0.24), ("Fall", 0.17), ("Skin integrity", 0.08), ("Diagnostic test", 0.07),
               ("Surgery or procedure", 0.07), ("Care coordination", 0.09), ("Equipment or device", 0.06),
               ("Infection", 0.04), ("Behavioral", 0.06), ("Lab specimen", 0.07), ("Blood product", 0.02),
               ("Maternal or perinatal", 0.03)]
HARM = [("No harm", 0.62), ("Mild harm", 0.27), ("Moderate harm", 0.085), ("Severe harm", 0.019), ("Death", 0.006)]
ROLES = [("RN", 0.58), ("Pharmacist", 0.09), ("Physician", 0.07), ("APC", 0.03), ("Technician", 0.1),
         ("Therapist", 0.05), ("Other staff", 0.08)]


def safety_rows():
    rng = K.stream("safety")
    rate = {"AMC": 205, "TFH": 74, "CMG": 52, "BCH": 34}
    pick = lambda opts: opts[int(rng.choice(len(opts), p=[w for _, w in opts]))][0]
    out = []
    seq = 2118400
    for (y, m) in K.months((2019, 1), (2026, 9)):
        days = []
        for e in K.ENTITY_ORDER:
            if e == "BCH" and (y, m) < (2019, 7):
                continue
            depts = [d[1] for d in K.DEPTS[e] if d[0] not in ("6910",)]
            lam = rate[e] * (1 + 0.012 * (y - 2019)) * (0.92 if m in (7, 8) else 1.0)
            for _ in range(int(rng.poisson(lam))):
                d = dt.date(y, m, int(rng.integers(1, K.days_in_month(y, m) + 1)))
                harm = pick(HARM)
                days.append((d, e, depts[int(rng.integers(0, len(depts)))], pick(EVENT_TYPES), harm, pick(ROLES),
                             "Y" if harm in ("Severe harm", "Death") or (harm == "Moderate harm" and rng.random() < 0.4)
                             else "N"))
        days.sort(key=lambda t: (t[0], t[1]))
        for t in days:
            seq += int(rng.integers(1, 3))
            out.append(["SE%07d" % seq, t[0].isoformat()] + list(t[1:]))
    return out


EXTRACT_LOG_COLS = ["file_name", "source", "run_or_received", "records", "owner", "coverage"]
