"""The goldens (remand_gap_drill.xlsx, remand_gap_briefing.pdf), submission.md and metadata.json, every figure read
from figures.json (golden.py), none typed."""
import io
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill  # noqa: E402
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer  # noqa: E402

import postprocess as PP  # noqa: E402
import world as W  # noqa: E402

MONTH = {10: "Oct", 11: "Nov", 12: "Dec", 1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul",
         8: "Aug", 9: "Sep"}
MONTHS = [(2025, m) for m in (10, 11, 12)] + [(2026, m) for m in range(1, 10)]
COURTS = [("Kestrel Bay", "KB"), ("Dunmore", "DN"), ("Ashgrove", "AG"), ("Thornmere", "RC")]


def p1(v):
    return "%.1f" % v


def drill_rows(f):
    rows = [("Halsey Coast region", f["region_gap_2025"], f["region_gap_2026"])]
    rows += [(n, f["gap_%s_2025" % c], f["gap_%s_2026" % c]) for n, c in COURTS]
    return rows


def workbook(f, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Drill"
    bold = Font(bold=True)
    head = PatternFill("solid", fgColor="DCE6F0")
    ws.append(["Custody remand gap at first appearance, no lawyer of record minus lawyer of record (percentage points)"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append([])
    ws.append(["Level 1: courthouse", "Year to Sep 2025", "Year to Sep 2026", "Change"])
    for c in "ABCD":
        ws["%s3" % c].font = bold
        ws["%s3" % c].fill = head
    for name, a, b in drill_rows(f):
        ws.append([name, round(a, 1), round(b, 1), round(b - a, 1)])
    ws.append([])
    r0 = ws.max_row + 1
    ws.append(["Level 2: Kestrel Bay custody list, year to Sep 2026", "Gap", "Community magistrate", "Judges"])
    for c in "ABCD":
        ws["%s%d" % (c, r0)].font = bold
        ws["%s%d" % (c, r0)].fill = head
    ws.append(["Called while the AVL remand list sat (courtroom 2)", round(f["kb_avl_gap"], 1),
               round(f["kb_avl_mag_gap"], 1), round(f["kb_avl_judges_gap"], 1)])
    ws.append(["Called at other times", round(f["kb_other_gap"], 1), round(f["kb_other_mag_gap"], 1),
               round(f["kb_other_judges_gap"], 1)])
    ws.append([])
    ws.append(["Source: CMS appearance extract and court sitting calendar, pulled 2 November 2026."])
    ws.cell(row=ws.max_row, column=1).font = Font(italic=True, size=9)
    for col, wdt in (("A", 58), ("B", 18), ("C", 22), ("D", 12)):
        ws.column_dimensions[col].width = wdt
    ws.freeze_panes = "B4"
    ws.page_setup.orientation = "landscape"
    ws.print_title_rows = "3:3"
    em = wb.create_sheet("EM turnaround")
    em.append(["Month ordered", "Average days, order to filed report"])
    for c in "AB":
        em["%s1" % c].font = bold
        em["%s1" % c].fill = head
    for y, m in MONTHS:
        em.append(["%s %d" % (MONTH[m], y), round(f["em_%d_%02d" % (y, m)], 1)])
    em.column_dimensions["A"].width = 16
    em.column_dimensions["B"].width = 34
    em.freeze_panes = "A2"
    bh = wb.create_sheet("Bail house nights")
    bh.append(["Month", "Occupied nights, both houses"])
    for c in "AB":
        bh["%s1" % c].font = bold
        bh["%s1" % c].fill = head
    for y, m in MONTHS:
        bh.append(["%s %d" % (MONTH[m], y), int(f["bh_%d_%02d" % (y, m)])])
    bh.column_dimensions["A"].width = 16
    bh.column_dimensions["B"].width = 30
    bh.freeze_panes = "A2"
    nt = wb.create_sheet("Notes")
    for line in [
        ["Notes"],
        ["As of: every extract pulled 2 November 2026; years run 1 October to 30 September."],
        ["Gap: section 3 of the Budget 2027 bid instructions. Every first appearance from police custody at the four "
         "courts, once each on its New Zealand date; the share remanded in custody, no lawyer of record at that "
         "appearance minus a lawyer of record."],
        ["EM turnaround: sections 1 and 2 of the EM bail service standard. Calendar days from a District Court's "
         "order to the first filing of the assessment report, one assessment per order, in the order's month. "
         "Orders the High Court made on cases transferred to it are not in the standard's scope."],
        ["Occupied nights: clause 4 of the support contract's schedule 2. A night dated by its evening and counted "
         "when the resident is at the house at midnight; nights in custody, in hospital, out past curfew and on "
         "approved leave excluded."],
        ["Rounding: gaps to one decimal of a percentage point, days to one decimal, nights whole."],
    ]:
        nt.append(line)
    nt["A1"].font = bold
    nt.column_dimensions["A"].width = 118
    for row in nt.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    for s in (ws, em, bh):
        for row in s.iter_rows():
            for cell in row:
                if isinstance(cell.value, float):
                    cell.number_format = "0.0"
                elif isinstance(cell.value, int):
                    cell.number_format = "#,##0"
    wb.save(path)
    PP.normalize_ooxml(path, "Freya Herd", "Freya Herd", "2026-11-03T01:40:00Z", "2026-11-03T03:05:00Z",
                       excel=True, company="Ministry of Justice")


def chart(f):
    labels, a25, a26 = [], [], []
    for name, a, b in drill_rows(f):
        labels.append(name)
        a25.append(a)
        a26.append(b)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.2, 3.9), gridspec_kw={"width_ratios": [1.15, 1]})
    y = list(range(len(labels)))[::-1]
    ax1.barh([v + 0.18 for v in y], a25, height=0.34, color="#9fb6cd", label="Year to Sep 2025")
    ax1.barh([v - 0.18 for v in y], a26, height=0.34, color="#2f5d8a", label="Year to Sep 2026")
    for yy, v in zip(y, a26):
        ax1.text(v + 0.3, yy - 0.18, p1(v), va="center", fontsize=8)
    for yy, v in zip(y, a25):
        ax1.text(v + 0.3, yy + 0.18, p1(v), va="center", fontsize=8, color="#555555")
    ax1.set_yticks(y)
    ax1.set_yticklabels(labels, fontsize=8.5)
    ax1.set_xlabel("Gap, percentage points", fontsize=8.5)
    ax1.set_title("Level 1: gap by courthouse", fontsize=9.5, loc="left")
    ax1.legend(fontsize=7.5, frameon=False, loc="lower right")
    ax1.set_xlim(0, max(a26 + a25) * 1.25)
    groups = ["AVL list sitting:\nmagistrate", "AVL list sitting:\njudges", "Other times:\nmagistrate",
              "Other times:\njudges"]
    vals = [f["kb_avl_mag_gap"], f["kb_avl_judges_gap"], f["kb_other_mag_gap"], f["kb_other_judges_gap"]]
    yy2 = list(range(len(groups)))[::-1]
    ax2.barh(yy2, vals, height=0.55, color=["#b5462f", "#b5462f", "#7f8c99", "#7f8c99"])
    for yv, v in zip(yy2, vals):
        ax2.text(v + 0.6, yv, p1(v), va="center", fontsize=8)
    ax2.set_yticks(yy2)
    ax2.set_yticklabels(groups, fontsize=8)
    ax2.set_xlim(0, max(vals) * 1.25)
    ax2.set_xlabel("Gap, percentage points", fontsize=8.5)
    ax2.set_title("Level 2: Kestrel Bay custody list, year to Sep 2026", fontsize=9.5, loc="left")
    for ax in (ax1, ax2):
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.tick_params(axis="x", labelsize=8)
    fig.suptitle("The 2026 widening sits in Kestrel Bay calls made while the AVL remand list sat",
                 fontsize=10.5, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=170, metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return buf


def briefing(f, path):
    body = ParagraphStyle("b", fontName="Helvetica", fontSize=9.6, leading=13.0, spaceAfter=6)
    h1 = ParagraphStyle("h1", parent=body, fontName="Helvetica-Bold", fontSize=13, leading=16.5, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=body, fontName="Helvetica-Bold", fontSize=10.4, spaceBefore=5, spaceAfter=3)
    meta = ParagraphStyle("m", parent=body, fontSize=8.8, leading=11.6, spaceAfter=1)
    small = ParagraphStyle("s", parent=body, fontSize=7.8, leading=10, textColor=colors.HexColor("#444444"))
    s = [Paragraph("To: Deputy Secretary, Regional Operations", meta),
         Paragraph("From: Freya Herd, Regional Manager, Criminal Court Operations, Halsey Coast", meta),
         Paragraph("Date: 3 November 2026", meta),
         Paragraph("Subject: Budget 2027 bid, custody remand gap at first appearance", meta), Spacer(1, 6),
         Paragraph("The remand gap widened in the Kestrel Bay calls heard while the duty lawyer was on the AVL list",
                   h1),
         Paragraph("Recommendation", h2),
         Paragraph("Put the duty lawyer roster forward: a second rostered duty lawyer at Kestrel Bay District Court on "
                   "every sitting day.", body),
         Image(chart(f), width=170 * mm, height=72 * mm),
         Paragraph("Source: CMS appearance extract and court sitting calendar, pulled 2 November 2026; duty lawyer "
                   "returns, 2024/25 to 2026/27.", small),
         Paragraph("What moved", h2),
         Paragraph("The gap between defendants with no lawyer of record and defendants with one widened from %s "
                   "points in the year to September 2025 to %s points in the year to September 2026.<super>1</super> "
                   "The widening is at Kestrel Bay (%s to %s points); the other three courts moved far less." % (
                       p1(f["region_gap_2025"]), p1(f["region_gap_2026"]), p1(f["gap_KB_2025"]),
                       p1(f["gap_KB_2026"])), body),
         Paragraph("Since December 2025 the AVL remand list from the remand centre has sat in courtroom 2 on most "
                   "Monday to Thursday sittings while the custody list runs in courtroom 1, and the roster keeps one "
                   "duty lawyer at Kestrel Bay. Custody-list defendants called while the AVL list was sitting show a "
                   "gap of %s points; those called at other times show %s points, against %s for Kestrel Bay's whole "
                   "custody list in the year before. The community magistrate who took the custody list in December "
                   "presides over most of the AVL hours, which is why the gap reads as his at first sight, but his gap "
                   "at other times is %s points against the judges' %s." % (
                       p1(f["kb_avl_gap"]), p1(f["kb_other_gap"]), p1(f["gap_KB_2025"]), p1(f["kb_other_mag_gap"]),
                       p1(f["kb_other_judges_gap"])), body),
         Paragraph("Why not the other lines", h2),
         Paragraph("A judge on the custody list would not change the calls made while the duty lawyer is in the "
                   "other courtroom. EM bail capacity matters for how long defendants wait once remanded, but EM "
                   "bail is sought at a later appearance, never at the first. The EM, bail house and reminder lines "
                   "are costed in remand_gap_drill.xlsx.", body),
         Spacer(1, 4),
         Paragraph("<super>1</super> The gap as section 3 of the bid instructions defines it: every first appearance "
                   "from police custody at the four courts, once each on its New Zealand date, remanded in custody "
                   "whatever else the court ordered; no lawyer of record at that appearance minus a lawyer of "
                   "record, in percentage points.", small)]

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(18 * mm, 10 * mm, "Halsey Coast region, criminal court operations. Budget 2027 bid.")
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()

    PP.word_pdf_info()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=15 * mm,
                            bottomMargin=17 * mm, title="Budget 2027 bid: custody remand gap", author="Freya Herd",
                            creator=PP.WORD_PDF, producer=PP.WORD_PDF)
    doc.build(s, onFirstPage=footer, onLaterPages=footer)
    PP.normalize_pdf(path, b"D:20261103141000+13'00'", b"D:20261103160500+13'00'")


def submission(f, path):
    em = ", ".join("%s %d %s" % (MONTH[m], y, p1(f["em_%d_%02d" % (y, m)])) for y, m in MONTHS)
    bh = ", ".join("%s %d %d" % (MONTH[m], y, int(f["bh_%d_%02d" % (y, m)])) for y, m in MONTHS)
    lines = [
        "## Tags", "",
        "**Domain:** Criminology & Justice (sentencing and bail disparity analysis).",
        "**Analytical objective:** Root-Cause Analysis.", "",
        "## 1. Final Recommendation", "",
        "**Put the duty lawyer roster forward: a second rostered duty lawyer at Kestrel Bay District Court on every "
        "sitting day.** The region's gap widened from %s to %s points, and the widening sits in Kestrel Bay "
        "custody-list calls made while the AVL remand list sat in courtroom 2 (gap %s points, against %s for the "
        "other calls). Not a judge on the custody list: outside AVL time the community magistrate's gap is %s points "
        "and the judges' %s. Not EM bail capacity: no first appearance decides EM bail." % (
            p1(f["region_gap_2025"]), p1(f["region_gap_2026"]), p1(f["kb_avl_gap"]), p1(f["kb_other_gap"]),
            p1(f["kb_other_mag_gap"]), p1(f["kb_other_judges_gap"])), "",
        "## 2. Critical Components", "",
        "1. The region's gap is **%s** points in the year to September 2025 and **%s** in the year to September "
        "2026." % (p1(f["region_gap_2025"]), p1(f["region_gap_2026"])),
        "2. Kestrel Bay's gap is **%s** then **%s** points." % (p1(f["gap_KB_2025"]), p1(f["gap_KB_2026"])),
        "3. Kestrel Bay, year to September 2026: calls made while the AVL remand list sat **%s** points, other calls "
        "**%s**." % (p1(f["kb_avl_gap"]), p1(f["kb_other_gap"])),
        "4. Outside AVL time the community magistrate's gap is **%s** points and the judges' **%s**; while the AVL "
        "list sat, **%s** and **%s**." % (p1(f["kb_other_mag_gap"]), p1(f["kb_other_judges_gap"]),
                                          p1(f["kb_avl_mag_gap"]), p1(f["kb_avl_judges_gap"])), "",
        "## 3. Step-by-Step Solution", "",
        "1. In cms_appearances_oct2024_sep2026.csv took the \"First appearance (custody)\" rows by AppearanceDate, a "
        "remand in custody where Outcome is \"Remanded in custody\" and no lawyer of record where CounselOfRecord is "
        "blank, per section 3 of budget2027_bid_instructions_halsey_coast.pdf: the region's gap is %s then %s points."
        % (p1(f["region_gap_2025"]), p1(f["region_gap_2026"])),
        "2. By Court, the widening sits at Kestrel Bay (KBY): %s to %s points." % (p1(f["gap_KB_2025"]),
                                                                                   p1(f["gap_KB_2026"])),
        "3. Set each Kestrel Bay custody-list first appearance's CalledAt against that day's AVL remand list sitting "
        "in court_sitting_calendar_2024-2026.xlsx (Courtroom 2, Start to Finish), with one duty lawyer rostered at "
        "Kestrel Bay each day in the duty lawyer returns: calls made while the AVL list sat show a gap of %s points, "
        "other calls %s." % (p1(f["kb_avl_gap"]), p1(f["kb_other_gap"])),
        "4. By JudicialOfficer within those two groups the community magistrate and the judges match: %s and %s "
        "outside AVL time, %s and %s while it sat." % (p1(f["kb_other_mag_gap"]), p1(f["kb_other_judges_gap"]),
                                                      p1(f["kb_avl_mag_gap"]), p1(f["kb_avl_judges_gap"])),
        "5. No first appearance in the extract carries an EM bail assessment order; every order sits on a later "
        "appearance.",
        "6. EM turnaround per sections 1 and 2 of em_bail_service_standard_v4.pdf: each order's date from its "
        "\"Remanded in custody, EM bail address assessment ordered\" appearance in the extract (by CRN, else surname, "
        "first name and date of birth; orders carried into em_case_system_assessments.csv joined by their addresses); "
        "an order with no such appearance sits on a case the extract shows \"Transferred to the High Court\" before it, "
        "is the High Court's and is left out; its report from the first \"EM address assessment report\" in "
        "em_document_uploads.csv on its New Zealand date, averaged by order month.",
        "7. Occupied nights per clause 4 of bail_support_contract_schedule2.pdf: each placement from its \"Resident "
        "arrived\" incident in bail_house_incidents.csv to the day the resident left (a move-out, or a departure that "
        "neither a logged return nor an absence on the Away sheet of bail_house_register_2025-26.xlsx closes), less "
        "the nights away: each departure to its logged return at midnight, and each absence on the Away sheet, "
        "approved leave included, by month.",
        "8. The duty lawyer roster is the only shortlisted line that acts on a first appearance's representation, "
        "and the widening sits in calls made while the AVL list sat next door with one duty lawyer rostered that day: "
        "put it forward.", "",
        "## 4. Deliverable Answers", "",
        "### remand_gap_briefing.pdf", "",
        "1. The call: the duty lawyer roster, a second rostered duty lawyer at Kestrel Bay District Court on every "
        "sitting day.",
        "2. Chart on page 1: the gap for the region and each courthouse in both years, then Kestrel Bay's year to "
        "September 2026 split into calls made while the AVL remand list sat and other calls.", "",
        "### remand_gap_drill.xlsx", "",
        "1. Gap by courthouse, year to September 2025 then 2026, percentage points:",
    ]
    for name, a, b in drill_rows(f):
        lines.append("   - %s: %s, %s" % (name, p1(a), p1(b)))
    lines += [
        "2. Kestrel Bay custody list, year to September 2026, percentage points:",
        "   - Called while the AVL remand list sat: %s" % p1(f["kb_avl_gap"]),
        "   - Called at other times: %s" % p1(f["kb_other_gap"]),
        "3. EM bail assessment turnaround, average days by order month: %s." % em,
        "4. Occupied nights at the supported bail houses by month: %s." % bh,
    ]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


FILES = {
    "cms_appearances_oct2024_sep2026.csv": "District Court case management system appearance extract, every appearance "
                                           "October 2024 to September 2026 at the four Halsey Coast courts",
    "court_sitting_calendar_2024-2026.xlsx": "court scheduling export of sittings by courtroom and list",
    "duty_lawyer_returns_2024-25.xlsx": "duty lawyer service daily returns, financial year 2024/25 (October 2024 on)",
    "duty_lawyer_returns_2025-26.xlsx": "duty lawyer service daily returns, financial year 2025/26",
    "duty_lawyer_returns_2026-27.xlsx": "duty lawyer service daily returns, financial year 2026/27 to September",
    "police_bail_summaries_2024-2026.csv": "police prosecution bail summaries for first appearances from custody",
    "offence_seriousness_scale.csv": "offence seriousness scale, offence codes to bands",
    "em_bail_tracker_2025-26.xlsx": "EM Bail Unit tracker, assessments referred to 30 January 2026",
    "em_case_system_assessments.csv": "EM case system export of assessments from 2 February 2026",
    "em_document_uploads.csv": "EM case system document upload log",
    "em_bail_service_standard_v4.pdf": "Department of Corrections EM bail address assessment service standard",
    "bail_house_register_2025-26.xlsx": "supported bail houses placement register and away records",
    "bail_house_incidents.csv": "supported bail provider incident log",
    "bail_support_contract_schedule2.pdf": "supported bail accommodation agreement, schedule of service measures",
    "budget2027_bid_instructions_halsey_coast.pdf": "Ministry of Justice Budget 2027 regional bid instructions",
    "remand_centre_daily_muster.csv": "remand centre daily muster by unit",
    "court_reminder_service_log.csv": "court-date text reminder service send log",
}


def metadata(task_dir):
    md = {
        "task": "task399",
        "domain": "Criminology & Justice",
        "objective": "Root-Cause Analysis",
        "decision": "which initiative on the region's Budget 2027 shortlist removes the change in the custody "
                    "remand gap at first appearance between the two years to September",
        "deliverables": ["remand_gap_briefing.pdf", "remand_gap_drill.xlsx"],
        "distractor_files": ["target/remand_centre_daily_muster.csv", "target/court_reminder_service_log.csv"],
        "files": [{"file": k, "path": "target/" + k, "source": "synthetic, constructed for this task in the layout "
                                                                 "of the producing organisation's own export",
                   "covers": v, "date": "2026-11-02", "licence": "CC BY 4.0", "organisation": _org(k)}
                  for k, v in sorted(FILES.items())],
    }
    with open(os.path.join(task_dir, "metadata.json"), "w", encoding="utf-8") as fh:
        json.dump(md, fh, indent=1)
        fh.write("\n")


def _org(k):
    if k.startswith(("em_",)):
        return "Department of Corrections (fictional region)"
    if k.startswith(("bail_house", "bail_support")):
        return "Coastline Bail Support Trust (fictional)"
    if k.startswith("police"):
        return "New Zealand Police prosecutions (fictional region)"
    if k.startswith("remand_centre"):
        return "Department of Corrections (fictional region)"
    return "Ministry of Justice (fictional region)"


def build_all(w, figs, task_dir):
    gd = os.path.join(task_dir, "golden")
    os.makedirs(gd, exist_ok=True)
    workbook(figs, os.path.join(gd, "remand_gap_drill.xlsx"))
    briefing(figs, os.path.join(gd, "remand_gap_briefing.pdf"))
    submission(figs, os.path.join(task_dir, "submission.md"))
    metadata(task_dir)
