"""The goldens from figures.json: the placement workbook (the falls figures by locality, and the placement) and the
board's case paper with its chart."""
import io
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from docx import Document  # noqa: E402
from docx.enum.table import WD_TABLE_ALIGNMENT  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Cm, Pt, RGBColor  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill  # noqa: E402
from openpyxl.utils import get_column_letter  # noqa: E402

import params as P  # noqa: E402
import postprocess  # noqa: E402

XLSX = "deprescribing_placement_2027.xlsx"
DOCX = "deprescribing_case_2027.docx"
HEAD = PatternFill("solid", fgColor="DCE6F0")
PICK = PatternFill("solid", fgColor="FFF2CC")
NHS_BLUE, GREY, INK, MUTED, GRID = "#005EB8", "#848F96", "#212B32", "#4C6272", "#D8DDE0"


def c(x):
    return "{:,}".format(int(x))


def _sheet(ws, title, header, rows, widths, fmts=None, note=None, pick=None):
    ws.cell(row=1, column=1, value=title).font = Font(bold=True, size=12)
    for j, h in enumerate(header, 1):
        cell = ws.cell(row=3, column=j, value=h)
        cell.font = Font(bold=True)
        cell.fill = HEAD
        cell.alignment = Alignment(vertical="top", wrap_text=True)
    for i, row in enumerate(rows, 4):
        for j, v in enumerate(row, 1):
            cell = ws.cell(row=i, column=j, value=v)
            if pick is not None and row[0] == pick:
                cell.fill = PICK
    for j, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    for col, f in (fmts or {}).items():
        for i in range(4, 4 + len(rows)):
            ws.cell(row=i, column=col).number_format = f
    ws.row_dimensions[3].height = 45
    ws.freeze_panes = "A4"
    if note:
        ws.cell(row=5 + len(rows), column=1, value=note).font = Font(italic=True, size=9, color="555555")


def workbook(path, fig):
    wb = Workbook()
    ws = wb.active
    ws.title = "Falls 2025-26"
    a = fig["asks"]
    order = [k for k, _, _, _ in P.LOCALITIES]
    rows = [[k, fig["localities"][k]["name"], a[k]["falls_65_79"], a[k]["falls_80"], a[k]["bed_days"],
             a[k]["readmitted"]] for k in order]
    t = fig["ask_totals"]
    rows.append(["", "Kestrel Vale", t["falls_65_79"], t["falls_80"], t["bed_days"], t["readmitted"]])
    _sheet(ws, "Emergency admissions for a fall, patients aged 65 or over, 2025-26",
           ["Locality code", "Locality", "Admissions for a fall, aged 65 to 79", "Admissions for a fall, aged 80 or over",
            "Bed-days of those admissions", "Admissions followed by an emergency readmission within 30 days"],
           rows, [11, 20, 15, 15, 15, 20], {c_: "#,##0" for c_ in (3, 4, 5, 6)},
           note="Falls dashboard definitions F1 to F3, version 2 (February 2026), on the SUS falls cohort extract. "
                "An admission is one stay in hospital care, including any move to another hospital.")
    ws.cell(row=4 + len(rows) - 1, column=2).font = Font(bold=True)
    ws2 = wb.create_sheet("Placement 2027")
    L = fig["localities"]
    prow = sorted(order, key=lambda k: -L[k]["avoided"])
    _sheet(ws2, "Hypnotic deprescribing team: emergency admissions for a fall avoided in 2027",
           ["Locality code", "Locality", "Current users aged 65+", "Of whom first started on or after 1 April 2025",
            "Admissions for a fall avoided, 1 April to 31 December 2027"],
           [[k, L[k]["name"], L[k]["users"], L[k]["recent"], L[k]["avoided_r"]] for k in prow],
           [11, 20, 14, 18, 20], {3: "#,##0", 4: "#,##0", 5: "0"}, pick=fig["winner"],
           note="Policy MO-17 (version 1.2): 45 in 100 current users come off, off the drug from 1 April 2027; rate "
                "ratio by time since the patient first started a benzodiazepine or Z-drug, dated from the start of "
                "their first repeat template.")
    r = 6 + len(prow)
    ws2.cell(row=r + 1, column=1, value="Recommended").font = Font(bold=True)
    ws2.cell(row=r + 1, column=2, value="%s: %d admissions avoided in 2027" % (fig["winner_name"], fig["avoided_r"]))
    ws2.cell(row=r + 2, column=1, value="Runner-up").font = Font(bold=True)
    ws2.cell(row=r + 2, column=2, value="%s: %d avoided, %d fewer" % (fig["runner_name"], fig["runner_avoided_r"],
                                                                       fig["gap_r"]))
    for sh in (ws, ws2):
        sh.print_title_rows = "3:3"
        sh.page_setup.orientation = "landscape"
        sh.page_setup.fitToWidth = 1
    ws3 = wb.create_sheet("Notes")
    notes = [
        ("Prepared", "%s, %s, 23 October 2026, for the board of 5 November 2026." % (P.PEOPLE["analyst"], P.CSU)),
        ("Falls 2025-26", "Falls dashboard definitions version 2 (February 2026): F1 an emergency admission for a fall, "
                          "one stay in hospital care, a move to another hospital included, with W00 to W19 in its first "
                          "episode, by age and the registered practice's locality at the start of the admission and by "
                          "the date of admission; F2 the days from admission to leaving hospital care; F3 an emergency "
                          "admission again on the day of leaving or in the 30 days after, the patient alive on leaving."),
        ("Source", "SUS admitted patient care falls cohort, 1 March 2025 to 31 July 2026; provider site codes; "
                   "practice register (Q80117, on the cohort's episodes before October 2025, is Fenmarsh Health "
                   "Centre's previous practice code)."),
        ("Placement 2027", "Policy MO-17 version 1.2: current users aged 65 or over on 1 January 2027 with a "
                           "benzodiazepine or Z-drug dispensed 1 July to 30 September 2026; 45 in 100 come off and are "
                           "off the drug from 1 April to 31 December 2027; 4.0 admissions for a fall per 100 a year off "
                           "the drug, times the rate ratio for the months since the patient first started."),
        ("Rounding", "Admissions, bed-days and readmissions are whole numbers; admissions avoided are rounded to "
                     "whole admissions at the end."),
    ]
    ws3.cell(row=1, column=1, value="Notes").font = Font(bold=True, size=12)
    for i, (k, v) in enumerate(notes, 3):
        ws3.cell(row=i, column=1, value=k).font = Font(bold=True)
        cell = ws3.cell(row=i, column=2, value=v)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        ws3.row_dimensions[i].height = 15 * (1 + len(v) // 95)
    ws3.column_dimensions["A"].width = 16
    ws3.column_dimensions["B"].width = 100
    wb.properties.creator = P.PEOPLE["analyst"]
    wb.properties.lastModifiedBy = P.PEOPLE["analyst"]
    wb.save(path)
    postprocess.scrub(path, P.ORG, "2026-10-23")
    postprocess.finish_office(path, "2026-10-21T08:55:00Z", "2026-10-23T15:20:00Z", P.ORG, person=P.PEOPLE["analyst"])


def chart(fig):
    """admissions avoided by locality, the recommended locality in blue; the paper's table carries every value"""
    L = fig["localities"]
    order = sorted(L, key=lambda k: -L[k]["avoided"])
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "svg.hashsalt": "task118"})
    f, ax = plt.subplots(figsize=(6.3, 3.0), dpi=150)
    vals = [L[k]["avoided"] for k in order]
    cols = [NHS_BLUE if k == fig["winner"] else GREY for k in order]
    ax.bar(range(len(order)), vals, 0.6, color=cols, zorder=2)
    for i, k in enumerate(order):
        if k in (fig["winner"], fig["runner"]):
            ax.text(i, vals[i] + 0.35, "%d" % L[k]["avoided_r"], ha="center", va="bottom", color=INK, fontsize=9,
                    fontweight="bold" if k == fig["winner"] else "normal")
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels([L[k]["name"].replace(" ", "\n", 1) for k in order], color=INK)
    ax.set_ylabel("Admissions avoided", color=MUTED)
    ax.set_ylim(0, max(vals) * 1.2)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6, zorder=0)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(axis="both", length=0, colors=MUTED)
    f.text(0.012, 0.955, "%s avoids the most emergency admissions for a fall" % fig["winner_name"], ha="left",
           va="top", fontsize=10, color=INK, fontweight="bold")
    f.text(0.012, 0.885, "Admissions avoided by the team, 1 April to 31 December 2027, by locality", ha="left",
           va="top", fontsize=8.2, color=MUTED)
    f.tight_layout(rect=(0, 0, 1, 0.84))
    buf = io.BytesIO()
    f.savefig(buf, format="png", facecolor="#FFFFFF", metadata={"Software": None})
    plt.close(f)
    return buf.getvalue()


def paper(path, fig):
    L = fig["localities"]
    w, r = fig["winner"], fig["runner"]
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10.5)
    for sec in d.sections:
        sec.left_margin = sec.right_margin = Cm(2.2)
    p = d.add_paragraph()
    run = p.add_run("%s: Board, 5 November 2026. Item 9." % P.ORG)
    run.bold = True
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x42, 0x55, 0x63)
    h = d.add_paragraph()
    run = h.add_run("Hypnotic deprescribing team: place it in %s for 2027" % fig["winner_name"])
    run.bold = True
    run.font.size = Pt(15)
    d.add_paragraph().add_run("Presented by %s, Chief Pharmacist. Prepared by %s (%s). Purpose: for decision." % (
        P.PEOPLE["chief"], P.PEOPLE["analyst"], P.CSU)).font.size = Pt(9)
    foot = d.sections[0].footer.paragraphs[0]
    run = foot.add_run("%s: board meeting, 5 November 2026, item 9. Page " % P.ORG)
    run.font.size = Pt(8)
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    r_ = OxmlElement("w:r")
    t_ = OxmlElement("w:t")
    t_.text = "1"
    r_.append(t_)
    fld.append(r_)
    foot._p.append(fld)
    d.add_heading("Recommendation", level=2)
    d.add_paragraph(
        "Place the deprescribing team in %s from January 2027. On the deprescribing policy it will avoid %d emergency "
        "admissions for a fall in 2027. %s is the runner-up at %d, %d fewer." % (
            fig["winner_name"], fig["avoided_r"], fig["runner_name"], fig["runner_avoided_r"], fig["gap_r"]))
    d.add_heading("Why %s" % fig["winner_name"], level=2)
    d.add_paragraph(
        "The team takes 45 in every 100 current users off the drug from 1 April, and each one it takes off stops "
        "running the extra risk of a fall that the drug carries. That extra risk depends on how long the patient has "
        "been taking a benzodiazepine or Z-drug: the policy puts it at 1.8 times the rate of a patient not taking one "
        "until two years after they first started, and 1.1 times after that. So the team avoids most where the current "
        "users started most recently, not where there are most of them.")
    d.add_paragraph(
        "%s has %s current users, and %s of them first started on or after 1 April 2025, more than in any other "
        "locality. Corvenham Central has the most current users (%s) but only %s started that recently; most have "
        "taken the drug for years and carry little extra risk now." % (
            fig["winner_name"], c(L[w]["users"]), c(L[w]["recent"]), c(L["CC"]["users"]), c(L["CC"]["recent"])))
    d.add_paragraph(
        "Each patient's first start is the start of their first repeat template, traced back through every "
        "re-authorisation, and for %s in %s through the templates exported from its previous clinical system, "
        "because its July move re-created every active template with the date of the move. The "
        "dispensing extract cannot date a start: it begins on 1 April 2026, so everyone already on the drug appears to "
        "start that month." % (fig["migrated_practice_name"], fig["migrated_name"]))
    d.add_picture(io.BytesIO(chart(fig)), width=Cm(15.5))
    d.add_heading("The six localities", level=2)
    order = sorted(L, key=lambda k: -L[k]["avoided"])
    t = d.add_table(rows=1, cols=4)
    t.style = "Light Grid Accent 1"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, hd in enumerate(["Locality", "Current users", "First started since April 2025", "Admissions avoided"]):
        t.rows[0].cells[i].text = hd
    for k in order:
        row = t.add_row().cells
        row[0].text, row[1].text, row[2].text = L[k]["name"], c(L[k]["users"]), c(L[k]["recent"])
        row[3].text = "%d" % L[k]["avoided_r"]
    note = d.add_paragraph()
    note.add_run("Current users: patients aged 65 or over on 1 January 2027 with a benzodiazepine or Z-drug dispensed "
                 "between 1 July and 30 September 2026 (policy MO-17, section 4). Admissions avoided are rounded to "
                 "whole admissions.").font.size = Pt(8)
    src = d.add_paragraph()
    src.add_run("Sources: dispensing extract April to September 2026; repeat templates as at 1 October 2026; "
                "%s previous-system template export; practice register; policy MO-17." %
                fig["migrated_practice_name"]).font.size = Pt(8)
    d.add_heading("Falls burden", level=2)
    d.add_paragraph(
        "The placement workbook gives each locality's emergency admissions for a fall in 2025-26 by age band, the "
        "bed-days they used and the readmissions within 30 days, on the falls dashboard's version 2 definitions.")
    d.add_heading("Risks", level=2)
    d.add_paragraph(
        "The figure assumes the pilot's 45 in 100 holds in %s and that the policy's rate ratios hold for its patients. "
        "If fewer come off, the number avoided falls in proportion in every locality, so the order does not change." %
        fig["winner_name"])
    d.core_properties.author = P.PEOPLE["analyst"]
    d.core_properties.title = "Deprescribing team placement 2027"
    d.save(path)
    postprocess.scrub(path, P.ORG, "2026-10-23")
    postprocess.finish_office(path, "2026-10-22T09:30:00Z", "2026-10-23T15:45:00Z", P.ORG, person=P.PEOPLE["analyst"],
                              revision=5)


def write(folder, fig):
    os.makedirs(folder, exist_ok=True)
    workbook(os.path.join(folder, XLSX), fig)
    paper(os.path.join(folder, DOCX), fig)
