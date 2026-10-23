"""task170 pack: every file under target/, written from the world in the layouts the hospital group's systems
export."""
from __future__ import annotations

import csv
import io
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

import common as C
import docs as DOCS
import postprocess as PP
import records as R
import world as W

D = C.D
BOLD = Font(name="Calibri", size=11, bold=True)
BODY = Font(name="Calibri", size=11)
HEAD_FILL = PatternFill("solid", fgColor="DDEBF7")

F_HR = "hr_employment_history_2019_2026.csv"
F_REG = "ledstrand_member_register_2026-10.xlsx"
F_IPC = "tarnmark_ipc_bordereau_2019_2026.csv"
F_DED = "payroll_deductions_2025-11_2026-10.csv"
F_PLAN = "vch_hiring_plan_2027.xlsx"
F_SURV = "staff_benefits_survey_2025.xlsx"
F_ABS = "sickness_absence_2025_2026.csv"
F_DICT = "data_dictionary.txt"
F_MAN = "export_manifest.csv"

HR_HEAD = ["employee_no", "legacy_employee_no", "spell", "hospital", "department", "grade", "fte", "contract_start",
           "contract_end", "end_reason"]
REG_HEAD = ["member_no", "membership", "employer_ref", "hospital_at_join", "joined", "rate_at_join_pct",
            "current_rate_pct", "status", "status_date"]
IPC_HEAD = ["policy_no", "previous_policy_no", "employer_ref", "hospital", "basis", "cover_start",
            "cancellation_received", "cover_end", "end_reason"]
DED_HEAD = ["payroll", "pay_date", "run", "employee_ref", "assignment", "cost_centre", "code", "basic_pay",
            "rate_pct", "amount"]
PLAN_HEAD = ["requisition", "hospital", "department", "job_family", "grade", "fte", "planned_start", "approved"]
JOB_FAMILY = {"G1": "Support services", "G2": "Healthcare assistant", "G3": "Healthcare assistant",
              "G4": "Registered nurse", "G5": "Registered nurse", "G6": "Senior nurse or allied professional",
              "G7": "Specialist clinician", "G8": "Consultant or manager"}


def _csv(path, head, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(head)
    for r in rows:
        w.writerow(r)
    open(path, "w", encoding="utf-8", newline="").write(buf.getvalue())


def _sheet(ws, head, rows, widths=None, start_row=1, fmt=None):
    for j, h in enumerate(head):
        c = ws.cell(row=start_row, column=j + 1, value=h)
        c.font = BOLD
        c.fill = HEAD_FILL
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            c = ws.cell(row=start_row + 1 + i, column=j + 1, value=v)
            c.font = BODY
            if isinstance(v, D):
                c.number_format = "yyyy-mm-dd"
            elif fmt and j in fmt:
                c.number_format = fmt[j]
    for j, h in enumerate(head):
        ws.column_dimensions[get_column_letter(j + 1)].width = (widths[j] if widths else max(10, len(h) + 2))


def _save(wb, path, creator, last_by, created, modified):
    wb.save(path)
    PP.normalize_ooxml(path, creator, last_by, created, modified, excel=True, company=C.ORG)


def _iso(v):
    return v.isoformat() if isinstance(v, D) else v


# ---------------------------------------------------------------------------------------------------- world
def make_world():
    S = R.enrich(W.spells())
    P = W.plan_2027()
    return dict(S=S, P=P)


def write_hr(out, Wd):
    rows = [[_iso(x) for x in r] for r in R.hr_rows(Wd["S"])]
    _csv(out + "/" + F_HR, HR_HEAD, rows)
    return len(rows)


def write_register(out, Wd, rng):
    rows = R.register_rows(Wd["S"], rng)
    wb = Workbook()
    ws = wb.active
    ws.title = "Members"
    _sheet(ws, REG_HEAD, rows, widths=[12, 12, 13, 16, 12, 16, 17, 10, 12])
    ws.freeze_panes = "A2"
    _save(wb, out + "/" + F_REG, C.ADMIN, C.ADMIN, "2026-10-28T05:10:00Z", "2026-10-28T05:10:00Z")
    return len(rows)


def write_ipc(out, Wd, rng):
    rows = [[_iso(x) for x in r] for r in R.ipc_rows(Wd["S"], rng)]
    _csv(out + "/" + F_IPC, IPC_HEAD, rows)
    return len(rows)


def write_deductions(out, Wd, rng):
    rows = [[_iso(x) for x in r] for r in R.deduction_rows(Wd["S"], rng)]
    order = {"MAIN": 0, "REVERSAL": 1, "RERUN": 2}
    rows.sort(key=lambda r: (r[0], order[r[2]], r[5], r[3], r[4], r[6]))
    _csv(out + "/" + F_DED, DED_HEAD, rows)
    return len(rows)


def write_plan(out, Wd, rng):
    """The approved 2027 hiring plan as HR's requisition tracker exports it."""
    rows = []
    n = [0]

    def req():
        n[0] += 1 + int(rng.integers(0, 3))
        return "R27-%04d" % n[0]

    for r in sorted(Wd["P"], key=lambda x: (x["month"], x["hosp"], x["grade"])):
        dept = str(rng.choice(R.DEPTS[r["hosp"]]))
        start = C.first_working_day(C.FY, r["month"])
        approved = D(2026, int(rng.integers(6, 11)), int(rng.integers(1, 29)))
        rows.append([req(), r["hosp"], dept, JOB_FAMILY[r["grade"]], r["grade"], r["fte"], start, approved])
    wb = Workbook()
    ws = wb.active
    ws.title = "Requisitions"
    _sheet(ws, PLAN_HEAD, rows, widths=[12, 10, 20, 34, 7, 6, 13, 12], fmt={5: "0.00"})
    ws.freeze_panes = "A2"
    ws2 = wb.create_sheet("Notes")
    for i, line in enumerate([
            "2027 hiring plan as approved by the executive team on 3 November 2026.",
            "One row per approved requisition; the date it was approved in the last column.",
            "Planned start: the induction day of the month the post is planned to be filled.",
            "Grade and FTE are the post's; pay follows the 2027 pay scale."]):
        ws2.cell(row=i + 1, column=1, value=line).font = BODY
    ws2.column_dimensions["A"].width = 110
    _save(wb, out + "/" + F_PLAN, C.PEOPLE["me"], C.PEOPLE["me"], "2026-06-30T08:02:00Z", "2026-11-04T15:27:00Z")
    return len(rows)


def write_survey(out, rng):
    rows = []
    for h in C.H_CODES:
        n = int(W.STOCK[h] * rng.uniform(0.32, 0.46))
        rows.append([h, C.H_NAME[h], n, round(float(rng.uniform(0.34, 0.47)), 3), round(float(rng.uniform(0.48, 0.66)), 3),
                     round(float(rng.uniform(0.41, 0.58)), 3), round(float(rng.uniform(0.52, 0.71)), 3)])
    wb = Workbook()
    ws = wb.active
    ws.title = "By hospital"
    _sheet(ws, ["hospital", "name", "respondents", "response_rate", "aware_of_employer_match",
                "satisfied_with_total_reward", "would_recommend_as_employer"], rows,
           widths=[10, 28, 12, 14, 24, 26, 27], fmt={3: "0.0%", 4: "0.0%", 5: "0.0%", 6: "0.0%"})
    _save(wb, out + "/" + F_SURV, C.PEOPLE["me"], C.PEOPLE["me"], "2025-11-20T09:30:00Z", "2025-12-02T10:44:00Z")


def write_absence(out, rng):
    rows = []
    for (y, m) in C.months((2025, 1), (2026, 9)):
        for h in C.H_CODES:
            for grp in ("Nursing", "Medical", "Allied health", "Support"):
                base = {"Nursing": 0.058, "Medical": 0.027, "Allied health": 0.041, "Support": 0.064}[grp]
                season = 1.0 + (0.18 if m in (1, 2, 12) else -0.08 if m in (6, 7, 8) else 0.0)
                rows.append(["%d-%02d" % (y, m), h, grp, round(base * season * rng.uniform(0.86, 1.14), 4)])
    _csv(out + "/" + F_ABS, ["month", "hospital", "staff_group", "absence_rate"], rows)


DICTIONARY = """Vindeholm County Hospitals: data dictionary for the files pulled on 9 November 2026
HR and Reward, for the FY2027 budget

Employee numbers. The HR and payroll system cut over on 1 February 2026. The new system issued every current and
former employee an E-number (E followed by six digits) and keeps the old system's V-number beside it in the HR
history. Files keep the number they were written under: the payroll deductions use V-numbers for the November 2025
to January 2026 payrolls and E-numbers from February 2026; Ledstrand's register and Tarnmark's bordereau keep the
number a membership or policy was opened under.

Hospital codes. VCS Vindeholm Central Hospital, RDH Rendholm Hospital, ASK Askvik Hospital, OSV Ostervall Hospital,
BRB Brannby Hospital, LDM Lidmark Hospital. LRC was Lidmark Rehabilitation Centre, merged into Lidmark Hospital on
1 July 2024; records closed or opened before the merger may carry LRC.

hr_employment_history_2019_2026.csv (HR system, every employment spell in post at any time from 1 January 2019)
  employee_no, legacy_employee_no   E-number and V-number
  spell                             1 for the first employment, 2 and up for a rehire under the same number
  hospital, department              where the spell was held (a transfer between hospitals ends one spell)
  grade, fte                        the post's grade and contracted hours as a share of full time
  contract_start, contract_end      first and last day of the spell; contract_end blank while in post. Staff start on
                                    the month's induction day and leave at a month end.
  end_reason                        HR's leaving reason

ledstrand_member_register_2026-10.xlsx (Ledstrand Pension Administration, sheet Members, at the October 2026 payroll)
  member_no, membership             one member number a person; membership 1, 2 and up for each time they joined
  employer_ref                      the employee number the membership was opened under
  hospital_at_join
  joined                            pay date of the membership's first contribution
  rate_at_join_pct, current_rate_pct  contribution rate, per cent of basic pay
  status, status_date               Active, or Deferred from the date employment ended

tarnmark_ipc_bordereau_2019_2026.csv (Tarnmark Mutual, the income protection cover)
  The cover pays two thirds of basic pay after 90 days of sickness absence. Its premium is 0.4 per cent of basic pay,
  deducted through payroll. Since January 2019 every new hire has been enrolled in the cover at hire (basis Auto) and
  may cancel at any time; staff hired before 2019 could take it out (basis Voluntary). A cancellation received by the
  10th stops that month's premium.
  policy_no, previous_policy_no     policies opened before Tarnmark's July 2022 system change keep their old number
  employer_ref                      employee number the policy was opened under
  cover_start, cancellation_received, cover_end, end_reason

payroll_deductions_2025-11_2026-10.csv (payroll, one line per payroll, employee, assignment and code)
  payroll (YYYYMM), pay_date, run (MAIN; a payroll reversed and run again also carries REVERSAL and RERUN lines),
  employee_ref, assignment (1 the main post, 2 a bank post), cost_centre (hospital and department code; 950 is the
  bank pool)
  code: PEN the employee's plan contribution, ERM the employer's match, IPC the cover's premium
  basic_pay                         the assignment's basic pay for the month, TNK
  rate_pct                          the contribution rate on PEN lines
  amount                            TNK

vch_hiring_plan_2027.xlsx (HR requisition tracker, the approved 2027 hiring plan; sheet Notes)

staff_benefits_survey_2025.xlsx (the November 2025 staff survey, benefits module, by hospital)
sickness_absence_2025_2026.csv (monthly sickness absence rate by hospital and staff group)
vch_savings_plan_rules_2024.pdf, vch_savings_plan_amendment_2027.docx, vch_pay_scales_2026_2027.pdf
"""


def write_dictionary(out):
    open(out + "/" + F_DICT, "w", encoding="utf-8", newline="").write(DICTIONARY.replace("\n", "\r\n"))


MANIFEST = [
    (F_HR, "HR and Reward", "HR system extract, employment spells", "2019-01-01 to 2026-10-31"),
    (F_REG, "Ledstrand Pension Administration", "Member register after the October 2026 contribution file", "to 2026-10"),
    (F_IPC, "Tarnmark Mutual", "Income protection bordereau, Vindeholm County Hospitals scheme", "2019-01 to 2026-10"),
    (F_DED, "Payroll services", "Deduction lines PEN, ERM, IPC", "payrolls 2025-11 to 2026-10"),
    (F_PLAN, "HR and Reward", "2027 hiring plan, requisition tracker", "2027"),
    (DOCS.F_RULES, "HR and Reward", "Plan rules, consolidated", "from 2024-02"),
    (DOCS.F_AMEND, "HR and Reward", "Committee paper, automatic enrolment", "from 2027-01-01"),
    (DOCS.F_SCALE, "HR and Reward", "Collective agreement, pay scale extract", "2026 and 2027"),
    (F_SURV, "HR and Reward", "Staff survey 2025, benefits module", "2025-11"),
    (F_ABS, "HR and Reward", "Sickness absence by hospital and staff group", "2025-01 to 2026-09"),
    (F_DICT, "HR and Reward", "Field definitions for this pull", "as at 2026-11-09"),
]


def write_manifest(out):
    _csv(out + "/" + F_MAN, ["file", "owner", "what_it_is", "covers"], [list(r) for r in MANIFEST])


def build_pack(out):
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        os.remove(os.path.join(out, f))
    Wd = make_world()
    n = {}
    n[F_HR] = write_hr(out, Wd)
    n[F_REG] = write_register(out, Wd, np.random.default_rng(C.SEED + 51))
    n[F_IPC] = write_ipc(out, Wd, np.random.default_rng(C.SEED + 52))
    n[F_DED] = write_deductions(out, Wd, np.random.default_rng(C.SEED + 53))
    n[F_PLAN] = write_plan(out, Wd, np.random.default_rng(C.SEED + 54))
    write_survey(out, np.random.default_rng(C.SEED + 55))
    write_absence(out, np.random.default_rng(C.SEED + 56))
    DOCS.write_rules(out)
    DOCS.write_scales(out)
    DOCS.write_amendment(out)
    write_dictionary(out)
    write_manifest(out)
    return n, Wd
