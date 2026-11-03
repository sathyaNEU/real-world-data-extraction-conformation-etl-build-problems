"""task241 golden deliverables: the 2027 setup workbook and the one-page note."""
import io
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import params as P
import postprocess

XLSX = "amd_review_2027.xlsx"
PDF = "amd_review_2027.pdf"
NAVY, RED, BLUE, INK = "1F3A5F", "B23A2E", "3F78B5", "1E2430"   # off, stays on: checked for colour-blind separation


def short(name):
    return name.replace(" (landline)", "").replace(" Survey", "").replace(" Poll", " Poll")


def workbook(path, A):
    wb = Workbook()
    ws = wb.active
    ws.title = "2027 setup"
    ws["A1"] = "Detection off for six projects in 2027: a tenth or more of their machine-classed calls were people"
    ws["A1"].font = Font(bold=True, size=13, color=INK)
    ws["A2"] = ("Kettle River Research telephone centre. 2026 dialer call detail (twelve monthly exports), inbound switch "
                "log to 14 January 2027, case records and payroll hours. Prepared 15 January 2027.")
    ws["A2"].font = Font(italic=True, size=9, color="555555")
    head = ["Job", "Project", "Machine-classed calls 2026", "Rang back within 20 min", "Abandoned live answers 2026",
            "Rang back within 20 min ", "Share answered by a person", "Detection 2027",
            "Answered calls outside 8 am to 9 pm", "Completed interviews 2026", "Interviewer hours 2026"]
    fmt = [None, None, "#,##0", "#,##0", "#,##0", "#,##0", "0%", None, "#,##0", "#,##0", "#,##0.0"]
    thin = Side(style="thin", color="B9C0CC")
    r0 = 4
    for j, h in enumerate(head, 1):
        c = ws.cell(row=r0, column=j, value=h.strip())
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=NAVY)
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    ws.row_dimensions[r0].height = 45
    for i, r in enumerate(A["rows"], r0 + 1):
        vals = [r["job"], r["name"], r["n_am"], r["r_am"], r["n_ab"], r["r_ab"], r["pct"] / 100.0,
                "Off" if r["off"] else "On", r["outside"], r["completes"], r["hours"]]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=i, column=j, value=v)
            c.border = Border(bottom=thin)
            if fmt[j - 1]:
                c.number_format = fmt[j - 1]
                c.alignment = Alignment(horizontal="right")
            if j == 8:
                c.alignment = Alignment(horizontal="center")
                if r["off"]:
                    c.font = Font(bold=True, color=RED)
        if r["off"]:
            ws.cell(row=i, column=7).font = Font(bold=True, color=RED)
    end = r0 + len(A["rows"])
    t = end + 1
    ws.cell(row=t, column=1, value="Total").font = Font(bold=True)
    for j, key in [(3, "n_am"), (4, "r_am"), (5, "n_ab"), (6, "r_ab"), (9, "outside"), (10, "completes")]:
        col = get_column_letter(j)
        c = ws.cell(row=t, column=j, value=f"=SUM({col}{r0 + 1}:{col}{end})")
        c.number_format = "#,##0"
        c.font = Font(bold=True)
    c = ws.cell(row=t, column=11, value=f"=SUM(K{r0 + 1}:K{end})")
    c.number_format = "#,##0.0"
    c.font = Font(bold=True)
    notes = [
        "Share answered by a person: the machine-classed calls rung back from the dialed number within 20 minutes, as a "
        "share of the project's machine-classed calls, divided by the same share for its abandoned live answers, which "
        "hear the same recorded message. Each project on its own calls; the counts are the same for any window from 2 "
        "to 120 minutes, from the call's start or its end.",
        "Detection off where the share is one in ten or more (2027 dialer policy, section 3).",
        "Outside hours: answered calls that rang before 8 am or after 9 pm in the household's own local time, the "
        "household's state from its case record (calls to another of the household's numbers through the same case).",
        "Completed interviews: each case once, whether completed on an outbound call or when the household called the "
        "line; a supervisor's verification call does not add an interview.",
        "Interviewer hours: payroll hours (July to December written as hours.minutes) shared in each shift by each "
        "project's talk and wrap time; training shifts with no calls are not charged (policy, section 5).",
        P.ONE_OFF[0] + " " + P.ONE_OFF[1] + ", a one-off 2026 study (the register's closed jobs sheet), is not shown.",
    ]
    for k, s in enumerate(notes):
        c = ws.cell(row=t + 2 + k, column=1, value=s)
        c.font = Font(size=9, color="333333")
    for j, w in enumerate([10, 38, 13, 12, 13, 12, 12, 11, 14, 13, 13], 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = "C5"
    ws.sheet_view.zoomScale = 90
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_title_rows = "4:4"
    ws.print_area = "A1:K%d" % (t + 2 + len(notes))
    wb.save(path)
    postprocess.scrub(path, P.QA_LEAD, "2027-01-15")
    postprocess.finish_office(path, "2027-01-14T15:10:00Z", "2027-01-15T11:42:00Z", P.COMPANY)


def chart_png(A):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})
    rows = sorted(A["rows"], key=lambda r: r["share"])
    fig, ax = plt.subplots(figsize=(6.6, 3.05), dpi=200)
    y = range(len(rows))
    colors = ["#" + (RED if r["off"] else BLUE) for r in rows]
    ax.barh(list(y), [100 * r["share"] for r in rows], color=colors, height=0.66)
    ax.axvline(10, color="#" + INK, lw=1.0, ls="--")
    ax.text(10.4, -1.0, "limit, 1 in 10 (10%)", fontsize=7, color="#" + INK, va="center")
    ax.set_ylim(-1.5, len(rows) - 0.4)
    ax.set_yticks(list(y))
    ax.set_yticklabels([f"{r['job']} {short(r['name'])}" for r in rows], fontsize=7)
    for k, r in enumerate(rows):
        ax.text(100 * r["share"] + 0.4, k, f"{r['pct']}%", va="center", fontsize=7, color="#" + INK)
    ax.set_xlabel("2026 machine-classed calls answered by a person (per cent)")
    ax.set_title("Six projects at or above one in ten in 2026", loc="left", fontsize=9, fontweight="bold",
                 color="#" + INK)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color="#" + RED, label="Detection off for 2027"),
                       Patch(color="#" + BLUE, label="Detection stays on")], loc="lower right", frameon=False,
              fontsize=7)
    ax.grid(axis="x", color="#E3E6EA", lw=0.6)
    ax.set_axisbelow(True)
    ax.set_xlim(0, max(100 * r["share"] for r in rows) + 5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return buf


def note(path, A):
    from reportlab import rl_config
    rl_config.invariant = 1                  # no build clock or random document id in the file
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=12.6, spaceAfter=6)
    head = ParagraphStyle("h", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=13.5, leading=16, spaceAfter=2)
    sub = ParagraphStyle("s", parent=ss["Normal"], fontName="Helvetica", fontSize=8.6, textColor="#555555", spaceAfter=8)
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.8 * inch, rightMargin=0.8 * inch,
                            topMargin=0.6 * inch, bottomMargin=0.55 * inch,
                            title="Answering machine detection for 2027", author=P.QA_LEAD, creator=P.COMPANY,
                            subject="Answering machine detection at 2027 project setup")
    memo = ParagraphStyle("m", parent=ss["Normal"], fontName="Helvetica", fontSize=9, leading=12)
    story = [Paragraph("Switch detection off for six projects in 2027", head),
             Paragraph("<b>To</b> %s, director of telephone operations&nbsp;&nbsp; <b>From</b> %s, quality assurance lead"
                       % (P.DIRECTOR, P.QA_LEAD), memo),
             Paragraph("<b>Date</b> 15 January 2027&nbsp;&nbsp; <b>Subject</b> answering machine detection at 2027 project "
                       "setup (dialer policy, section 3)", memo),
             Spacer(1, 8)]
    for p in A["note_paragraphs"]:
        story.append(Paragraph(p, body))
    story.append(Spacer(1, 2))
    story.append(Image(chart_png(A), width=6.6 * inch, height=3.05 * inch))
    small = ParagraphStyle("f", parent=body, fontSize=8.0, leading=10.2, textColor="#444444", spaceAfter=3)
    story.append(Paragraph("Source: dialer call detail 2026 (twelve monthly exports, the repeated day of each export "
                           "counted once), inbound switch log to 14 January 2027 (one call per switch call id, the "
                           "quality assurance test calls left out).", small))
    story.append(Paragraph(A["note_footer"], small))

    def footer(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColorRGB(0.4, 0.4, 0.4)
        canvas.drawString(0.8 * inch, 0.35 * inch, "Kettle River Research, telephone operations")
        canvas.drawRightString(letter[0] - 0.8 * inch, 0.35 * inch, "Page 1 of 1")
        canvas.restoreState()
    doc.build(story, onFirstPage=footer)
    postprocess.scrub(path, P.COMPANY, "2027-01-15")


def write(folder, A):
    os.makedirs(folder, exist_ok=True)
    workbook(os.path.join(folder, XLSX), A)
    note(os.path.join(folder, PDF), A)
