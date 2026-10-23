"""task170 deliverables: figures.json, the golden workbook and budget note, and submission.md, all from the pack."""
from __future__ import annotations

import io
import json
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import calc
import common as C
import postprocess as PP

F_XLSX = "vindeholm_match_forecast_2027.xlsx"
F_DOCX = "match_forecast_note_2027.docx"
BOLD = Font(name="Calibri", size=11, bold=True)
BODY = Font(name="Calibri", size=11)
TITLE = Font(name="Calibri", size=13, bold=True, color="163F6B")
FILL = PatternFill("solid", fgColor="DCE6F1")
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def rnd(v, unit):
    return int(round(v / float(unit))) * unit


def monthly(G):
    """The golden's match by payroll month of 2027, every hospital together."""
    cv, P = G["cv"], G["P"]
    d = C.DEFAULT_RATE / 100
    out = [0.0] * 12
    for m, pay in zip(P["month"], P["pay"]):
        for k in range(1, 14 - int(m)):
            i = k - 1
            A = cv["C"][i] / cv["p"]
            out[int(m) + k - 2] += cv["Se"][i] * pay * ((1 - A) * d + cv["C"][i] * cv["mb"])
    return out


def figures(target):
    G = calc.golden(target)
    cv = G["cv"]
    rival = calc.forecast(target, cv, "ipc_carry", G["P"])
    ded = calc.deductions(target)
    paid = calc.match_paid_2026(target, "golden", ded)
    mem = calc.members_pre2019(target, "golden", ded)
    F = {"call_match_fy2027_tnk": rnd(G["total"], 500000)}
    for h in C.H_CODES:
        F["call_match_fy2027_%s" % h] = rnd(G["by"][h], 100000)
    F["call_contributing_dec2027"] = rnd(G["heads_total"], 100)
    F["component_prefer_to_save_pct"] = int(round(100 * cv["p"]))
    F["component_chosen_by_12th_payroll_pct"] = int(round(100 * G["chosen"][12]))
    F["step_match_unrounded_tnk"] = int(round(G["total"]))
    F["step_intake_requisitions"] = int(len(G["P"]))
    F["step_employed_dec2027"] = rnd(G["staff_total"], 100)
    F["rival_cover_carry_tnk"] = rnd(rival["total"], 500000)
    for h in C.H_CODES:
        F["ask_match_paid_2026_%s" % h] = rnd(paid[h], 1000)
    for h in C.H_CODES:
        F["ask_members_pre2019_%s" % h] = int(mem[h])
    return F, G, paid, mem


def _w(ws, r, c, v, font=BODY, fmt=None):
    cell = ws.cell(row=r, column=c, value=v)
    cell.font = font
    if fmt:
        cell.number_format = fmt
    return cell


def _head(ws, r, labels):
    for j, h in enumerate(labels):
        c = _w(ws, r, j + 1, h, BOLD)
        c.fill = FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")


def write_xlsx(out, F, G, paid, mem):
    cv = G["cv"]
    wb = Workbook()
    ws = wb.active
    ws.title = "FY2027 intake match"
    _w(ws, 1, 1, "Employer match on the 2027 intake, FY2027 budget line", TITLE)
    _w(ws, 2, 1, "Approved 2027 hiring plan (%s requisitions), 2027 pay scale, automatic enrolment at 3 per cent from "
                 "the first payroll. Forecast from the group's hires since January 2019." % "{:,}".format(F["step_intake_requisitions"]))
    _head(ws, 4, ["Hospital", "Employer match FY2027, TNK (nearest 100,000)", "Unrounded, TNK",
                  "Intake contributing on the December 2027 payroll", "Intake on the December 2027 payroll"])
    for i, h in enumerate(C.H_CODES):
        r = 5 + i
        _w(ws, r, 1, C.H_NAME[h])
        _w(ws, r, 2, F["call_match_fy2027_%s" % h], fmt="#,##0")
        _w(ws, r, 3, round(G["by"][h]), fmt="#,##0")
        _w(ws, r, 4, round(G["heads"][h]), fmt="#,##0")
        _w(ws, r, 5, round(G["staff"][h]), fmt="#,##0")
    r = 5 + len(C.H_CODES)
    _w(ws, r, 1, "Group", BOLD)
    _w(ws, r, 2, F["call_match_fy2027_tnk"], BOLD, "#,##0")
    _w(ws, r, 3, F["step_match_unrounded_tnk"], BOLD, "#,##0")
    _w(ws, r, 4, F["call_contributing_dec2027"], BOLD, "#,##0")
    _w(ws, r, 5, F["step_employed_dec2027"], BOLD, "#,##0")
    _w(ws, r + 1, 1, "Group match to the nearest TNK 500,000 and December contributors to the nearest 100; hospital "
                     "figures are rounded on their own and need not add to the group's.")
    for j, wdt in enumerate([30, 22, 16, 22, 20]):
        ws.column_dimensions[get_column_letter(j + 1)].width = wdt
    ws.row_dimensions[4].height = 48
    ws.freeze_panes = "B5"

    m = wb.create_sheet("By payroll month")
    _w(m, 1, 1, "FY2027 match on the intake by payroll month, TNK", TITLE)
    _head(m, 3, ["Payroll", "Employer match"])
    mon = monthly(G)
    for i, v in enumerate(mon):
        _w(m, 4 + i, 1, "%s 2027" % MONTHS[i])
        _w(m, 4 + i, 2, round(v), fmt="#,##0")
    _w(m, 16, 1, "Total", BOLD)
    _w(m, 16, 2, round(sum(mon)), BOLD, "#,##0")
    m.column_dimensions["A"].width = 14
    m.column_dimensions["B"].width = 18

    b = wb.create_sheet("Basis")
    _w(b, 1, 1, "What the forecast rests on: hires January 2019 to October 2026, all hospitals", TITLE)
    _w(b, 3, 1, "Hires in the record (spells starting from January 2019)")
    _w(b, 3, 2, cv["n_hires"], fmt="#,##0")
    _w(b, 4, 1, "Share of hires who join the plan when joining is their own choice (join curve at five years)")
    _w(b, 4, 2, round(cv["p"], 4), BOLD, "0.0%")
    _w(b, 5, 1, "Average employer match of a joiner's chosen rate, per cent of basic pay")
    _w(b, 5, 2, round(100 * cv["mb"], 3), fmt="0.00")
    _head(b, 7, ["Payroll month of service", "Joined the plan (opt-in record)", "Made a choice (joined over the five-"
                 "year share)", "Still on the payroll", "Contributing under automatic enrolment",
                 "Cover cancelled (income protection)"])
    for k in range(1, 13):
        r = 7 + k
        i = k - 1
        A = cv["C"][i] / cv["p"]
        _w(b, r, 1, k)
        _w(b, r, 2, round(float(cv["C"][i]), 4), fmt="0.0%")
        _w(b, r, 3, round(float(A), 4), fmt="0.0%")
        _w(b, r, 4, round(float(cv["Se"][i]), 4), fmt="0.0%")
        _w(b, r, 5, round(float((1 - A) + cv["C"][i]), 4), fmt="0.0%")
        _w(b, r, 6, round(float(cv["G"][i]), 4), fmt="0.0%")
    _w(b, 21, 1, "Until a hire makes a choice the default holds: no contribution in the opt-in record, 3 per cent "
                 "under automatic enrolment. A hire who chooses either joins at the rate chosen or contributes "
                 "nothing; the opt-in record shows only the first kind, so the share who have chosen by each month "
                 "is the join curve over its five-year level.")
    b.cell(row=21, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    b.merge_cells("A21:F21")
    b.row_dimensions[21].height = 48
    for j, wdt in enumerate([44, 18, 22, 16, 22, 20]):
        b.column_dimensions[get_column_letter(j + 1)].width = wdt
    b.row_dimensions[7].height = 48

    a = wb.create_sheet("2026 actuals")
    _w(a, 1, 1, "Employer match paid and long-standing members, 2026", TITLE)
    _head(a, 3, ["Hospital", "Employer match paid, January to October 2026 payrolls, TNK (nearest 1,000)",
                 "Members since before 2019 still active on 1 November 2026"])
    for i, h in enumerate(C.H_CODES):
        _w(a, 4 + i, 1, C.H_NAME[h])
        _w(a, 4 + i, 2, F["ask_match_paid_2026_%s" % h], fmt="#,##0")
        _w(a, 4 + i, 3, F["ask_members_pre2019_%s" % h], fmt="#,##0")
    _w(a, 10, 1, "Group", BOLD)
    _w(a, 10, 2, sum(F["ask_match_paid_2026_%s" % h] for h in C.H_CODES), BOLD, "#,##0")
    _w(a, 10, 3, sum(F["ask_members_pre2019_%s" % h] for h in C.H_CODES), BOLD, "#,##0")
    _w(a, 12, 1, "Match: ERM lines of every run, counted once per employee and payroll (payroll writes the person's "
                 "match on each assignment's line). Members: Ledstrand's Active memberships opened before 1 January 2019, "
                 "less those whose employment ended on 31 October 2026, by the cost centre of the October payroll.")
    a.cell(row=12, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    a.merge_cells("A12:C12")
    a.row_dimensions[12].height = 62
    a.row_dimensions[3].height = 48
    for j, wdt in enumerate([30, 34, 30]):
        a.column_dimensions[get_column_letter(j + 1)].width = wdt
    n = wb.create_sheet("Notes")
    notes = [
        ("As of", "Files pulled 9 November 2026; the October 2026 payroll is the last in the record."),
        ("Intake", "Approved requisitions in the 2027 hiring plan (tracker of 4 November 2026), each filled at its "
                   "planned start (committee paper, section 4)."),
        ("Pay", "2027 scale for the post's grade times its FTE, every 2027 payroll (collective agreement extract)."),
        ("Enrolment", "3 per cent from the first payroll; a choice received by the 10th applies that month (plan "
                      "rules, section 3; committee paper, section 3)."),
        ("Match", "100 per cent of the contribution up to 3 per cent of basic pay and 50 per cent between 3 and 6 "
                  "(plan rules, section 4)."),
        ("Experience", "Every employment spell starting January 2019 to October 2026, rehires included as new spells, "
                       "all six hospitals together; LRC spells read as Lidmark."),
        ("2026 actuals", "Payroll's deduction export, every run of the January to October 2026 payrolls; Ledstrand's "
                         "register after the October contribution file, read against HR's leavers."),
        ("Rounding", "Group match to the nearest TNK 500,000, hospitals to the nearest TNK 100,000, December "
                     "contributors to the nearest 100, 2026 match to the nearest TNK 1,000, each from unrounded figures."),
    ]
    for i, (k, v) in enumerate(notes):
        _w(n, 1 + i, 1, k, BOLD)
        c = _w(n, 1 + i, 2, v)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        n.row_dimensions[1 + i].height = 15 * (1 + len(v) // 95)
    n.column_dimensions["A"].width = 14
    n.column_dimensions["B"].width = 100
    ws.print_title_rows = "4:4"
    ws.page_setup.orientation = "landscape"
    path = os.path.join(out, F_XLSX)
    wb.save(path)
    PP.normalize_ooxml(path, C.PEOPLE["me"], C.PEOPLE["me"], "2026-11-10T07:48:00Z", "2026-11-13T14:22:00Z",
                       excel=True, company=C.ORG)


def chart_png(G, F):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "svg.hashsalt": "task170",
                         "path.simplify": False})
    fig, ax = plt.subplots(figsize=(6.2, 2.7), dpi=150)
    names = [C.H_NAME[h].replace(" Hospital", "") for h in C.H_CODES]
    vals = [G["by"][h] / 1e6 for h in C.H_CODES]
    ax.barh(names[::-1], vals[::-1], color="#2f5d8c", height=0.6)
    for y, v in enumerate(vals[::-1]):
        ax.text(v + 0.04, y, "%.1f" % v, va="center", fontsize=8.5)
    ax.set_xlabel("Employer match on the 2027 intake, FY2027, TNK million")
    ax.set_title("Vindeholm Central carries a third of the line", loc="left", fontsize=10, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlim(0, max(vals) * 1.15)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def write_docx(out, F, G, paid, mem):
    from docx import Document
    from docx.shared import Cm, Pt
    cv = G["cv"]
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for s in d.sections:
        s.left_margin = s.right_margin = Cm(2.2)
        s.top_margin = s.bottom_margin = Cm(1.9)
    d.add_heading("Budget TNK %s million for the match on the 2027 intake" % "{:.1f}".format(F["call_match_fy2027_tnk"] / 1e6),
                  level=1)
    d.add_paragraph("To: the employment committee (copy: Erik Palm, director of finance). From: Caroline Hagman, reward "
                    "and pensions. 13 November 2026.")
    d.add_paragraph(
        "Budget TNK %s million for the employer's match on the staff we hire in 2027 (TNK %s unrounded). About %s of "
        "the %s intake still with us on the December 2027 payroll will be contributing."
        % ("{:.1f}".format(F["call_match_fy2027_tnk"] / 1e6), "{:,}".format(F["step_match_unrounded_tnk"]),
           "{:,}".format(F["call_contributing_dec2027"]), "{:,}".format(F["step_employed_dec2027"])))
    d.add_paragraph(
        "Automatic enrolment changes who has to act, not what people want. Under opt-in, %d per cent of our hires "
        "eventually join, but they take their time: only by their twelfth payroll have %d per cent of hires "
        "made any choice. From January every hire starts at 3 per cent and stays there until they choose, so those who will "
        "opt out leave gradually, and those who join at their own rate move off the default just as gradually."
        % (F["component_prefer_to_save_pct"], F["component_chosen_by_12th_payroll_pct"]))
    d.add_paragraph(
        "We should not budget off the income protection cover's cancellations (about TNK %s million): far fewer "
        "hires want to drop a 0.4 per cent cover than decline the plan, so its cancellation rate understates the "
        "opt-outs we will see." % ("{:.1f}".format(F["rival_cover_carry_tnk"] / 1e6)))
    t = d.add_table(rows=1, cols=2)
    t.style = "Light Grid Accent 1"
    t.rows[0].cells[0].text, t.rows[0].cells[1].text = "Hospital", "FY2027 match, TNK"
    for h in C.H_CODES:
        r = t.add_row().cells
        r[0].text, r[1].text = C.H_NAME[h], "{:,}".format(F["call_match_fy2027_%s" % h])
    r = t.add_row().cells
    r[0].text, r[1].text = "Group", "{:,}".format(F["call_match_fy2027_tnk"])
    d.add_paragraph("Hospital figures are rounded on their own and do not add to the group's. Source: HR history, "
                    "Ledstrand register and the 2027 hiring plan, pulled 9 November 2026.").runs[0].font.size = Pt(8.5)
    d.add_picture(io.BytesIO(chart_png(G, F)), width=Cm(15.5))
    d.add_paragraph(
        "Basis: the approved 2027 hiring plan (%s requisitions) at the 2027 pay scale; leaving and choosing as our "
        "%s hires since January 2019 did, all hospitals together. The workbook has the monthly profile, the "
        "curves and the 2026 actuals." % ("{:,}".format(F["step_intake_requisitions"]), "{:,}".format(cv["n_hires"])))
    d.core_properties.title = "FY2027 budget: employer match on the 2027 intake"
    path = os.path.join(out, F_DOCX)
    d.save(path)
    PP.normalize_docx(path, C.PEOPLE["me"], C.PEOPLE["me"], "2026-11-12T08:05:00Z", "2026-11-13T14:40:00Z", 4, 96,
                      seed=C.SEED, title="FY2027 budget: employer match on the 2027 intake", company=C.ORG)


def submission(F):
    hosp = "\n".join("   - %s: %s" % (C.H_NAME[h], "{:,}".format(F["call_match_fy2027_%s" % h])) for h in C.H_CODES)
    paid = "\n".join("   - %s: %s" % (C.H_NAME[h], "{:,}".format(F["ask_match_paid_2026_%s" % h])) for h in C.H_CODES)
    mem = "\n".join("   - %s: %s" % (C.H_NAME[h], "{:,}".format(F["ask_members_pre2019_%s" % h])) for h in C.H_CODES)
    return f"""## Tags

**Domain:** Psychology and behavioural science (decision-making and computational behavioural modelling).
**Analytical objective:** Forecasting and predictive modelling.

## 1. Final Recommendation

**Budget about TNK {F['call_match_fy2027_tnk']:,} for the employer's match on Vindeholm County Hospitals' 2027 intake in FY2027, with about {F['call_contributing_dec2027']:,} of the intake contributing on the December 2027 payroll.**
Every hire holds the three per cent default until making a choice, and the opt-in record shows that {F["component_chosen_by_12th_payroll_pct"]} per cent have chosen by their twelfth payroll while {F['component_prefer_to_save_pct']} per cent of those who choose join. Not the income protection cover's cancellations carried as the plan's opt-outs (about TNK {F['rival_cover_carry_tnk']:,}).

## 2. Critical Components

1. Share of hires who join when joining is their own choice (the join curve's five-year level): **{F['component_prefer_to_save_pct']} per cent**.
2. Share of hires who have made a choice by their twelfth payroll (the join curve over that level): **{F['component_chosen_by_12th_payroll_pct']} per cent**.

## 3. Step-by-Step Solution

1. Took every spell starting from January 2019 in hr_employment_history_2019_2026.csv as a hire, followed to the October 2026 payroll or the month it ended.
2. Placed each membership in ledstrand_member_register_2026-10.xlsx on its spell through either employee number and the month of its first contribution, and built the share of hires joined by each payroll month of service, leavers censored (Kaplan-Meier); its five-year level is {F['component_prefer_to_save_pct']} per cent.
3. Read the share who have made a choice by each month as the join curve over its five-year level ({F['component_chosen_by_12th_payroll_pct']} per cent by the twelfth payroll); the income protection cancellations in tarnmark_ipc_bordereau_2019_2026.csv, over their own five-year level, run on the same clock.
4. Built the share of hires still on the payroll by month of service from the same spells, and the average match on joiners' rates at join under the rules' formula.
5. For each requisition in vch_hiring_plan_2027.xlsx, paid at the 2027 scale for its grade and FTE from its planned start, summed over its 2027 payrolls: still employed times pay times (not yet chosen at three per cent plus joined at their own rates' match).
6. The 2026 match: ERM lines on the January to October 2026 payrolls of every run, each employee's line counted once per payroll and run, by cost centre.
7. Members: Ledstrand's Active memberships opened before 1 January 2019, less those whose HR contract ended on 31 October 2026, by the cost centre of their October 2026 payroll.
8. The FY2027 match on the 2027 intake is about TNK {F['call_match_fy2027_tnk']:,}.

## 4. Deliverable Answers

### vindeholm_match_forecast_2027.xlsx

1. Employer match on the 2027 intake, FY2027, group (to the nearest half million TNK): {F['call_match_fy2027_tnk']:,}
2. By hospital (to the nearest hundred thousand TNK):
{hosp}
3. Intake contributing on the December 2027 payroll (to the nearest hundred): {F['call_contributing_dec2027']:,}
4. Employer match paid on the January to October 2026 payrolls (to the nearest thousand TNK):
{paid}
5. Members since before 2019 still active on 1 November 2026:
{mem}

### match_forecast_note_2027.docx

1. A one-page note to the employment committee stating the FY2027 line (TNK {F['call_match_fy2027_tnk']:,}) and each hospital's figure.
"""


def deliver(target, golden_dir, figures_path, submission_path):
    os.makedirs(golden_dir, exist_ok=True)
    for f in os.listdir(golden_dir):
        os.remove(os.path.join(golden_dir, f))
    F, G, paid, mem = figures(target)
    write_xlsx(golden_dir, F, G, paid, mem)
    write_docx(golden_dir, F, G, paid, mem)
    with open(figures_path, "w") as fh:
        json.dump(F, fh, indent=1, sort_keys=False)
        fh.write("\n")
    open(submission_path, "w").write(submission(F))
    return F, G
