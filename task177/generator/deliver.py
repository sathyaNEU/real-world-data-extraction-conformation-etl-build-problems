"""task177 goldens: the forecast workbook, the note for the board, generator/figures.json and submission.md, every
figure computed once from the shipped files (calc.py) and carried."""
from __future__ import annotations

import io
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as K           # noqa: E402
import common as C         # noqa: E402
import postprocess as PP   # noqa: E402

F_BOOK = "libranza_empresarial_default_forecast.xlsx"
F_NOTE = "launch_default_note.docx"
SECTOR_LABEL = {"contact centres": "Contact centres", "retail chains": "Retail chains",
                "security services": "Security services", "logistics and courier": "Logistics and courier",
                "food processing": "Food processing", "private clinics": "Private clinics"}
TYPE_LABEL = {"national": "National", "territorial": "Territorial", "health": "Health", "education": "Education"}


def figures(target):
    cf = K.call_figures(target)
    B, A = K.load_launch(target)
    n_sec = B.groupby("sector").size().reindex(list(C.SECTORS)).to_dict()
    hl = np.array([cf["h"][n] for n in B["employer_nit"]])
    rr = K.ratio_route(target, cf)
    a = K.ask_a(target)
    b = K.ask_b(target)
    dp = K.default_path(target)
    nit_sector = dict(zip(A["employer_nit"], A["sector"]))
    emp = []
    for nit in sorted(cf["h"], key=lambda n: (C.SECTORS.index(nit_sector[n]), -cf["h"][n])):
        emp.append(dict(nit=nit, name=A[A["employer_nit"] == nit]["legal_name"].iloc[0], sector=nit_sector[nit],
                        expo=int(cf["expo"][nit]), leavers=int(cf["leavers"][nit]), h=cf["h"][nit],
                        loans=int((B["employer_nit"] == nit).sum())))
    F = dict(
        call_total=C.nearest(cf["total"], C.ROUND_TOTAL),
        call_total_unrounded=round(cf["total"], 1),
        call_share={s: C.nearest(100 * cf["sectors"][s] / n_sec[s], C.ROUND_SHARE) for s in C.SECTORS},
        call_share_unrounded={s: round(100 * cf["sectors"][s] / n_sec[s], 1) for s in C.SECTORS},
        call_expected={s: round(cf["sectors"][s], 1) for s in C.SECTORS},
        n_sec=n_sec, n_launch=cf["n_launch"],
        conv_pct=C.nearest(100 * cf["F"][12], 1),
        F=[round(float(x), 4) for x in cf["F"]],
        n_runs=cf["n_runs"],
        resid=cf["resid"],
        leave_launch_pct=C.nearest(100 * float(hl.mean()), 1),
        leave_launch_raw=round(100 * float(hl.mean()), 2),
        leave_public_pct=C.nearest(100 * rr["hpub"] * 12, 1),
        pd12_public=round(100 * rr["pd12"], 1),
        employers=emp,
        default_total=C.nearest(dp["total"], 50),
        askA_deducted={s: C.nearest(a["deducted"][s], C.ROUND_AMOUNT) for s in C.SECTORS},
        askA_outstanding={s: C.nearest(a["outstanding"][s], C.ROUND_AMOUNT) for s in C.SECTORS},
        askB_recovered={str(y): {t: C.nearest(b[y][t], C.ROUND_AMOUNT) for t in C.AGENCY_TYPES} for y in (2023, 2024)},
    )
    return F


def _money(v):
    return "VMP {:,}".format(int(v))


# --------------------------------------------------------------------------------------------------- the workbook
def write_workbook(path, F):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    wb = Workbook()
    head_fill = PatternFill("solid", fgColor="DCE7E2")
    bold = Font(bold=True)

    def header(ws, row, cols):
        for j, h in enumerate(cols):
            c = ws.cell(row=row, column=j + 1, value=h)
            c.font = bold
            c.fill = head_fill
            c.alignment = Alignment(wrap_text=True, vertical="top")

    ws = wb.active
    ws.title = "Forecast"
    ws["A1"] = "Libranza Empresarial launch, 1 February 2027: loans in default by 31 January 2028"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Default: an instalment 90 or more days past due at a month-end (product rules 5.1). Pull of 22 January 2027."
    ws["A4"] = "Loans in default by 31 January 2028, nearest 50"
    ws["B4"] = F["call_total"]
    ws["A4"].font = bold
    ws["B4"].font = Font(bold=True, size=12)
    ws["A5"] = "Expected loans in default (unrounded)"
    ws["B5"] = F["call_total_unrounded"]
    ws["B5"].number_format = "0.0"
    header(ws, 7, ("Sector", "Launch loans", "Expected loans in default", "Share of the sector's loans, nearest 5%",
                   "Share, unrounded %"))
    for i, s in enumerate(C.SECTORS):
        r = 8 + i
        ws.cell(row=r, column=1, value=SECTOR_LABEL[s])
        ws.cell(row=r, column=2, value=F["n_sec"][s])
        c = ws.cell(row=r, column=3, value=F["call_expected"][s])
        c.number_format = "0.0"
        ws.cell(row=r, column=4, value=F["call_share"][s])
        c = ws.cell(row=r, column=5, value=F["call_share_unrounded"][s])
        c.number_format = "0.0"
    ws.cell(row=14, column=1, value="All sectors").font = bold
    ws.cell(row=14, column=2, value=F["n_launch"]).font = bold
    c = ws.cell(row=14, column=3, value=F["call_total_unrounded"])
    c.number_format = "0.0"
    c.font = bold
    for col, w in zip("ABCDE", (52, 14, 22, 24, 16)):
        ws.column_dimensions[col].width = w

    ws2 = wb.create_sheet("Method")
    ws2["A1"] = "How the forecast is built"
    ws2["A1"].font = Font(bold=True, size=12)
    lines = [
        "Public book: a payroll-deduction loan falls behind almost only when the Tesoreria stops paying the borrower "
        "(SIN SALARIO returns) while the loan is open.",
        "Of the %s public loans whose borrower stopped being paid by the payroll with the loan open (first SIN SALARIO "
        "month January 2017 to December 2025), %d%% went into default, three to five months after that month."
        % ("{:,}".format(F["n_runs"]), F["conv_pct"]),
        "Private employers: each employer's monthly rate of staff with a year's service working their last month "
        "(final settlement), from its payroll registers since the agreement.",
        "Each launch loan: the chance its borrower leaves in each month from February 2027, times the share of such "
        "loans in default by 31 January 2028 given the months left, plus the on-payroll route.",
    ]
    for i, t in enumerate(lines):
        c = ws2.cell(row=3 + i, column=1, value=t)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    header(ws2, 8, ("Months from the first SIN SALARIO month", "Share of those loans in default by then"))
    for j in range(13):
        ws2.cell(row=9 + j, column=1, value=j)
        c = ws2.cell(row=9 + j, column=2, value=F["F"][j])
        c.number_format = "0.0%"
    ws2.cell(row=23, column=1, value="On-payroll default rate per loan-month (no SIN SALARIO run before default)")
    c = ws2.cell(row=23, column=2, value=F["resid"])
    c.number_format = "0.00000"
    header(ws2, 25, ("Employer", "NIT", "Sector", "Employee-months with a year's service", "Leavers",
                     "Monthly leaving rate", "Launch loans"))
    for i, e in enumerate(F["employers"]):
        r = 26 + i
        vals = (e["name"], e["nit"], SECTOR_LABEL[e["sector"]], e["expo"], e["leavers"], e["h"], e["loans"])
        for j, v in enumerate(vals):
            c = ws2.cell(row=r, column=j + 1, value=v)
            if j == 5:
                c.number_format = "0.00%"
    for col, w in zip("ABCDEFG", (58, 16, 22, 20, 10, 14, 12)):
        ws2.column_dimensions[col].width = w

    ws3 = wb.create_sheet("Savings remittances")
    ws3["A1"] = "Members' savings contributions deducted for the months of 2026, and not received by 31 December 2026"
    ws3["A1"].font = Font(bold=True, size=12)
    header(ws3, 3, ("Sector", "Deducted, VMP", "Not received by 31 December 2026, VMP"))
    for i, s in enumerate(C.SECTORS):
        ws3.cell(row=4 + i, column=1, value=SECTOR_LABEL[s])
        ws3.cell(row=4 + i, column=2, value=F["askA_deducted"][s]).number_format = "#,##0"
        ws3.cell(row=4 + i, column=3, value=F["askA_outstanding"][s]).number_format = "#,##0"
    ws3["A11"] = ("Deducted: each employer's latest schedule for a month where it was filed again for the same members, "
                  "with any supplement for members left off. Received: transfers into the collection account to 31 "
                  "December 2026, a group's single transfer counted against each schedule it pays.")
    ws3["A11"].alignment = Alignment(wrap_text=True, vertical="top")
    for col, w in zip("ABC", (60, 22, 34)):
        ws3.column_dimensions[col].width = w

    ws4 = wb.create_sheet("Recoveries")
    ws4["A1"] = "Public loans in default in 2023 and 2024: recovered by 31 December 2026, other than by netting the member's own savings"
    ws4["A1"].font = Font(bold=True, size=12)
    header(ws4, 3, ("Unit type", "Defaulted in 2023, VMP", "Defaulted in 2024, VMP"))
    for i, t in enumerate(C.AGENCY_TYPES):
        ws4.cell(row=4 + i, column=1, value=TYPE_LABEL[t])
        ws4.cell(row=4 + i, column=2, value=F["askB_recovered"]["2023"][t]).number_format = "#,##0"
        ws4.cell(row=4 + i, column=3, value=F["askB_recovered"]["2024"][t]).number_format = "#,##0"
    ws4["A9"] = ("Receipts net of reversals. Transfers from the borrowing member's own savings account are the netting "
                 "and are left out; transfers from another member's savings account are payments.")
    ws4["A9"].alignment = Alignment(wrap_text=True, vertical="top")
    for col, w in zip("ABC", (60, 26, 26)):
        ws4.column_dimensions[col].width = w
    wb.save(path)
    PP.normalize_ooxml(path, "Paola Ayala", "Paola Ayala", "2027-01-23T13:05:00Z", "2027-01-26T18:41:00Z",
                       excel=True, company=C.ORG)


# ------------------------------------------------------------------------------------------------------- the note
def chart_png(F):
    import matplotlib
    matplotlib.use("Agg")
    matplotlib.rcParams["svg.hashsalt"] = "task177"
    import matplotlib.pyplot as plt
    ACCENT, REST, INK, INK2, MUTED, GRID, AXIS = ("#1f5b4a", "#9aa39f", "#0b0b0b", "#52514e", "#898781", "#e1e0d9",
                                                  "#c3c2b7")
    labels = [SECTOR_LABEL[s] for s in C.SECTORS]
    v = [F["call_share_unrounded"][s] for s in C.SECTORS]
    fig, ax = plt.subplots(figsize=(7.2, 3.4), dpi=150)
    fig.patch.set_facecolor("#fcfcfb")
    ax.set_facecolor("#fcfcfb")
    y = np.arange(len(labels))[::-1]
    ax.barh(y, v, color=ACCENT, height=0.62, zorder=2)
    ax.axvline(F["pd12_public"], color=INK, linewidth=1.0, linestyle=(0, (4, 3)), zorder=3)
    ax.text(F["pd12_public"] + 0.3, len(labels) - 0.45, "Public servants' loans, first year: %.1f%%" % F["pd12_public"],
            fontsize=7.6, color=INK, va="center")
    for yi, vi in zip(y, v):
        ax.text(vi + 0.3, yi, "%.0f%%" % vi, fontsize=7.6, color=INK2, va="center")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlabel("Share of the sector's launch loans in default by 31 January 2028", fontsize=8.2, color=INK2)
    ax.set_title("Private employers' staff leave their jobs far more often, and leaving is how a libranza defaults",
                 fontsize=9.0, loc="left", color=INK)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6, zorder=0)
    ax.tick_params(labelsize=7.8, colors=MUTED, length=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(AXIS)
    ax.set_xlim(0, max(v) + 4)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None}, facecolor=fig.get_facecolor())
    plt.close(fig)
    return buf.getvalue()


def note_paragraphs(F):
    sh = F["call_share"]
    return [
        "About %d of the %s Libranza Empresarial loans we disburse on 1 February will have gone into default by 31 "
        "January 2028, roughly one in ten. Our public servants' loans run at %.1f per cent in their first year; the "
        "launch book will not." % (F["call_total"], "{:,}".format(F["n_launch"]), F["pd12_public"]),
        "A libranza is paid at source, so it falls behind almost only when the borrower stops being paid by the "
        "payroll while the loan is open. In our public book that happens to about %d per cent of borrowers a year, "
        "and when it does, %d per cent of those loans go into default three to five months later. Staff with a "
        "year's service at the 38 agreement employers leave at about %d per cent a month on their own payroll "
        "registers since 2025, several times the public rate, so the same mechanism produces several times the "
        "defaults."
        % (F["leave_public_pct"], F["conv_pct"], F["leave_launch_pct"]),
        "A model fitted to the public book's borrower attributes does not see this: public servants rarely leave, and "
        "the temporary staff who do hold loans that end before their contracts, so the book's low default looks like "
        "borrower quality. Scored on the launch file it gives about %d." % F["default_total"],
        "By sector the expected share in default is about %d per cent in contact centres, %d in retail chains, %d in "
        "security services, %d in logistics and courier, %d in food processing and %d in private clinics."
        % (sh["contact centres"], sh["retail chains"], sh["security services"], sh["logistics and courier"],
           sh["food processing"], sh["private clinics"]),
    ]


def write_note(path, F):
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Inches, Pt, RGBColor
    GREY = RGBColor(0x5D, 0x68, 0x75)
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(11)
    for label, value in (("To", "Board of Directors"), ("From", "Paola Ayala, Finance"),
                         ("Date", "26 January 2027"), ("Subject", "Libranza Empresarial launch: first-year defaults")):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        r1 = p.add_run("%s: " % label)
        r1.bold = True
        r1.font.size = Pt(9.5)
        r2 = p.add_run(value)
        r2.font.size = Pt(9.5)
    doc.add_paragraph()
    t = doc.add_paragraph()
    r = t.add_run("About %d of the 2,400 launch loans will go into default within the first year" % F["call_total"])
    r.bold = True
    r.font.size = Pt(15)
    r.font.color.rgb = RGBColor(0x1F, 0x5B, 0x4A)
    for para in note_paragraphs(F):
        doc.add_paragraph(para)
    doc.add_picture(io.BytesIO(chart_png(F)), width=Inches(6.3))
    cap = doc.add_paragraph("Sources: payroll loan book and Tesoreria returns 2017 to 2026; default register; the 38 "
                            "employers' payroll registers 2025 to 2026; launch disbursement file of 22 January 2027.")
    cap.runs[0].font.size = Pt(8.5)
    cap.runs[0].font.color.rgb = GREY
    fn = doc.add_paragraph("Default is an instalment 90 or more days past due at a month-end (product rules 5.1), the "
                           "definition of our annual return; the counts are expected values over the 2,400 loans. "
                           "Leaving rates are each employer's own, from the staff with a year's service on its "
                           "registers, since every launch borrower has saved with us for twelve months.")
    fn.runs[0].font.size = Pt(8.5)
    fn.runs[0].font.color.rgb = GREY
    p = doc.add_paragraph()
    p.add_run("For the provision").bold = True
    doc.add_paragraph("The savings the employers deducted for 2026, what had not reached us by year end, and what we "
                      "recovered on the public loans that went into default in 2023 and 2024 are in the workbook.")
    foot = doc.sections[0].footer.paragraphs[0]
    foot.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    fr = foot.add_run("Coopservir. Finance. Internal. Page ")
    fr.font.size = Pt(8)
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    rn = OxmlElement("w:r")
    tx = OxmlElement("w:t")
    tx.text = "1"
    rn.append(tx)
    fld.append(rn)
    foot._p.append(fld)
    doc.save(path)
    PP.normalize_docx(path, "Paola Ayala", "Paola Ayala", "2027-01-26T14:10:00Z", "2027-01-26T19:02:00Z",
                      revision=7, total_time=88, seed="note2027", title="Libranza Empresarial launch: first-year defaults",
                      company=C.ORG)


# ---------------------------------------------------------------------------------------------- figures and write-up
def write_figures(path, F):
    flat = dict(call_total=F["call_total"], call_total_unrounded=F["call_total_unrounded"],
                call_share=F["call_share"], call_share_unrounded=F["call_share_unrounded"],
                cc_conversion_pct=F["conv_pct"], cc_leave_launch_pct=F["leave_launch_pct"],
                ask_a_deducted=F["askA_deducted"], ask_a_outstanding=F["askA_outstanding"],
                ask_b_recovered=F["askB_recovered"],
                counts={"n_launch": F["n_launch"], "n_runs": F["n_runs"]},
                parameters={"default_path_total": F["default_total"], "public_pd12_pct": F["pd12_public"],
                            "public_leave_pct_year": F["leave_public_pct"], "rounding_amount_vmp": C.ROUND_AMOUNT,
                            "rounding_total_loans": C.ROUND_TOTAL, "rounding_share_pct": C.ROUND_SHARE})
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(flat, fh, indent=1, ensure_ascii=False, sort_keys=True)
        fh.write("\n")


def write_submission(path, F):
    sh = F["call_share"]
    L = []
    L += ["## Tags", "",
          "**Domain:** Banking, Credit & Financial Risk, credit scoring and PD modelling.",
          "**Analytical objective:** Forecasting & Predictive Modeling.", ""]
    L += ["## 1. Final Recommendation", "",
          "**About %d of the %s Libranza Empresarial loans disbursed on 1 February 2027 will go into default by 31 "
          "January 2028.**" % (F["call_total"], "{:,}".format(F["n_launch"])),
          "A payroll-deduction loan defaults almost only when its borrower stops being paid by the payroll with the "
          "loan open, %d per cent of such public loans went into default, and the agreement employers' staff with a "
          "year's service work their last month at about %d per cent a month. Not the %d a PD model on the public book's borrower "
          "attributes gives, which reads the public servants' rare leaving as borrower quality."
          % (F["conv_pct"], F["leave_launch_pct"], F["default_total"]), ""]
    L += ["## 2. Critical Components", "",
          "1. Of the public loans whose borrower stopped being paid by the payroll with the loan open, **%d per cent** "
          "went into default." % F["conv_pct"],
          "2. Staff with a year's service at the employers of the launch loans work their last month at about **%d per "
          "cent** a month."
          % F["leave_launch_pct"], ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Joined %s, %s (legacy numbers through %s) and %s; marked the first month of each run of SIN SALARIO "
          "(01) returns on a loan, the month the Tesoreria stopped paying the borrower with the loan open." %
          (C.F_LOANS, C.F_RETURNS, C.F_XWALK, C.F_DEFAULTS),
          "2. For runs starting January 2017 to December 2025, took the share of those loans whose default date falls "
          "within each number of months of that first month: %d per cent by five months, none before three, the "
          "conversion by months left." % F["conv_pct"],
          "3. Took the monthly default rate of loans still paid by the payroll (defaults with no SIN SALARIO run "
          "before them, per loan-month) as the on-payroll route.",
          "4. From %s (repeated uploads dropped, employee ids without the CC prefix and dots), took each employer's "
          "monthly rate of staff with twelve or more months' service working their last month (the LIQUIDACION row), "
          "over employee-months since its first register." % C.F_REGISTERS,
          "5. For each loan in %s, summed over February 2027 to January 2028 the chance its borrower leaves at the "
          "end of each month times the conversion for the months then left, plus the on-payroll route; by sector "
          "through %s." % (C.F_LAUNCH, C.F_AGREE),
          "6. Savings in %s: where an employer filed a second schedule for a month with the same members, only the "
          "later counts, and a schedule for members missing from the month adds to it; received from %s, a returned "
          "transfer counted once, a group parent's single transfer paying its own and its subsidiary's schedules "
          "of the month (its amount is their sum)." % (C.F_SCHED, C.F_STMT),
          "7. Recoveries in %s on the loans whose default date in %s falls in 2023 or 2024, net of reversals, "
          "leaving out transfers from the borrowing member's own account in %s (another member's savings account "
          "paying is a recovery), by unit_type in %s." % (C.F_RECEIPTS, C.F_DEFAULTS, C.F_SAVINGS, C.F_LOANS),
          "8. Recommendation: about %d of the %s loans in default by 31 January 2028." %
          (F["call_total"], "{:,}".format(F["n_launch"])), ""]
    L += ["## 4. Deliverable Answers", "", "### %s" % F_BOOK, "",
          "1. Libranza Empresarial loans in default by 31 January 2028: %d." % F["call_total"],
          "2. Share of each sector's launch loans in default by 31 January 2028, nearest 5 per cent:"]
    for s in C.SECTORS:
        L.append("   - %s: %d per cent" % (SECTOR_LABEL[s], sh[s]))
    L.append("3. Members' savings contributions the employers deducted for the months of 2026, VMP to the nearest 1,000:")
    for s in C.SECTORS:
        L.append("   - %s: %s" % (SECTOR_LABEL[s], _money(F["askA_deducted"][s])))
    L.append("4. Of that, not received by 31 December 2026, VMP to the nearest 1,000:")
    for s in C.SECTORS:
        L.append("   - %s: %s" % (SECTOR_LABEL[s], _money(F["askA_outstanding"][s])))
    L.append("5. Recovered by 31 December 2026 other than by netting the member's own savings, VMP to the nearest 1,000:")
    for y in ("2023", "2024"):
        for t in C.AGENCY_TYPES:
            L.append("   - Defaulted in %s, %s: %s" % (y, TYPE_LABEL[t].lower(), _money(F["askB_recovered"][y][t])))
    L += ["", "### %s" % F_NOTE, "",
          "1. The forecast for the board: about %d of the 2,400 loans in default by 31 January 2028, with the reason "
          "(leaving the payroll with the loan open, far more frequent at the agreement employers)." % F["call_total"],
          "2. Bar chart of the expected share in default by sector against the public loans' first-year rate.", ""]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


def main(target, golden, figures_path, submission):
    os.makedirs(golden, exist_ok=True)
    F = figures(target)
    write_workbook(os.path.join(golden, F_BOOK), F)
    write_note(os.path.join(golden, F_NOTE), F)
    write_figures(figures_path, F)
    write_submission(submission, F)
    return F
