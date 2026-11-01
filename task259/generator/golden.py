"""The golden deliverables: the pilot-area workbook and the certification memo, written from figures computed on
target/ alone."""
import io
import os

import docx
import matplotlib
import openpyxl
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt
from openpyxl.styles import Alignment, Font

import common
from analysis import AREAS

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

WB = "pba_pilot_areas_2027.xlsx"
MEMO = "pba_pilot_certification_2027.docx"


def pct1(x):
    return "%.1f" % x


def write_workbook(F, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Pilot areas"
    ws.append(["WDA", "Workforce development area", "Employed residents holding more than one job (%)",
               "Qualifies under ARM 24.30.104"])
    for a in AREAS:
        ws.append([a, F["names"][a], round(F["share"][a], 1), "Yes" if a in F["certified"] else "No"])
    ws.append([])
    ws.append(["", "Statewide", round(F["statewide"]), ""])
    ws.append([])
    ws.append(["", "Four quarters 2025Q4 to 2026Q3, final weights (2026Q3 as reissued 16 Oct 2026). Second jobs "
               "counted on the respondent's own reporting basis per ARM 24.30.104(3)."])
    for col, w in zip("ABCD", (7, 28, 22, 18)):
        ws.column_dimensions[col].width = w
    for c in ws[1]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="bottom")
    for row in ws.iter_rows(min_row=2, max_row=9, min_col=3, max_col=3):
        for c in row:
            c.number_format = "0.0"
    ws.freeze_panes = "A2"
    ws2 = wb.create_sheet("Survey quality")
    ws2.append(["WDA", "Workforce development area", "Household response rate (%)", "Noncontact rate (%)",
                "Eligible housing units", "Interviewed households"])
    for a in AREAS:
        ws2.append([a, F["names"][a], round(F["rr"][a], 1), round(F["nc"][a], 1), F["eligible"][a],
                    F["interviewed"][a]])
    ws2.append([])
    ws2.append(["", "Housing units in sample counted once per quarter, 2025Q4 to 2026Q3; eligible means occupied "
                "when the interviewer visited."])
    for col, w in zip("ABCDEF", (7, 28, 16, 14, 14, 14)):
        ws2.column_dimensions[col].width = w
    for c in ws2[1]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="bottom")
    for row in ws2.iter_rows(min_row=2, max_row=9, min_col=3, max_col=4):
        for c in row:
            c.number_format = "0.0"
    for row in ws2.iter_rows(min_row=2, max_row=9, min_col=5, max_col=6):
        for c in row:
            c.number_format = "#,##0"
    ws2.freeze_panes = "A2"
    ws3 = wb.create_sheet("Notes")
    for line in (
            ["Basis", "ARM 24.30.104: employed residents aged 16 or over, each counted once in each quarter their "
                      "household was interviewed, 2025Q4 to 2026Q3, on the survey's final weights."],
            ["Second jobs", "Counted as residents report them themselves (24.30.104(3)). Answers given by another "
                            "household member are corrected by the share of second jobs they carry, measured on "
                            "residents who answered for themselves in an adjacent quarter."],
            ["Weights", "2026Q3 as reissued 16 October 2026 (Southwest Lakes control revised); the first issue "
                        "leaves every area's qualification unchanged."],
            ["Survey quality", "Each housing unit in sample counted once per quarter. Units vacant, demolished or "
                               "not housing units at the visit are not eligible, including units the master "
                               "address file had already removed as vacant or demolished."],
            ["Prepared", "Labor Market Information Bureau, 23 October 2026."]):
        ws3.append(line)
    ws3.column_dimensions["A"].width = 15
    ws3.column_dimensions["B"].width = 100
    for r in ws3.iter_rows():
        r[0].font = Font(bold=True)
        r[1].alignment = Alignment(wrap_text=True, vertical="top")
    common.xlsx_props(wb, "Mackenzie Parks", "2027 portable benefits pilot areas", created=(2026, 10, 23, 10, 15))
    wb.save(path)
    common.normalise_zip(path, "2026-10-23T16:15:00Z", "Microsoft Excel")


def chart_png(F):
    fig, ax = plt.subplots(figsize=(6.4, 3.4), dpi=150)
    labels = [F["names"][a] for a in AREAS]
    vals = [F["share"][a] for a in AREAS]
    cols = ["#2f5d8a" if a in F["certified"] else "#a9b4c0" for a in AREAS]
    ax.bar(range(len(AREAS)), vals, color=cols, width=0.65)
    ax.axhline(7.0, color="#b03a2e", lw=1.2, ls="--")
    ax.text(len(AREAS) - 0.6, 7.12, "7.0% threshold", color="#b03a2e", fontsize=7.5, ha="right")
    for i, v in enumerate(vals):
        ax.text(i, v + 0.12, "%.1f" % v, ha="center", fontsize=7.5)
    ax.set_xticks(range(len(AREAS)))
    ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=7.5)
    ax.set_ylabel("Employed residents with 2+ jobs (%)", fontsize=8)
    ax.set_ylim(0, max(vals) + 1.2)
    ax.tick_params(axis="y", labelsize=7.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_title("Four areas reach the 7.0%% line on the residents' own reporting (%s to %s)" %
                 ("2025Q4", "2026Q3"), fontsize=8.5)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def write_memo(F, path):
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    names = F["names"]
    cert = [names[a] for a in AREAS if a in F["certified"]]
    notc = [names[a] for a in AREAS if a not in F["certified"]]

    def p(text, bold=False, after=6):
        para = d.add_paragraph()
        r = para.add_run(text)
        r.bold = bold
        para.paragraph_format.space_after = Pt(after)
        return para

    p("MEMORANDUM", bold=True, after=2)
    p("To: Jason Holland, Commissioner of Labor and Industry", after=0)
    p("From: Mackenzie Parks, Chief, Labor Market Information Bureau", after=0)
    p("Date: 23 October 2026", after=0)
    p("Re: Four workforce areas qualify for the 2027 portable benefits pilot (ARM 24.30.104)", after=10)
    p("Recommendation", bold=True, after=2)
    p("Certify %s, %s, %s and %s as pilot areas for 2027. %s, %s, %s and %s do not qualify." %
      (tuple(cert) + tuple(notc)))
    p("Across the state, %d percent of employed residents held more than one job over the four quarters to "
      "September 2026, counted as residents report it themselves. The survey's published series, which takes "
      "every answer as given, shows %s percent." % (round(F["statewide"]), pct1(F["statewide_face"])))
    p("Basis of the estimates", bold=True, after=2)
    p("When an adult is out at the time of the interview, the household member answering gives that adult's "
      "answers. Residents who were answered for in one quarter and answered for themselves in an adjacent quarter "
      "show that these answers carry only about %d percent of the second jobs the residents report themselves. "
      "Second jobs are also more common among the residents who are out when we call, so the published series "
      "understates them, most in the areas where more adults are answered for. Each area's answered-for reports "
      "were corrected by that reporting rate; answers residents gave for themselves stand as given."
      % round(100 * F["sensitivity"]))
    t = d.add_table(rows=1, cols=3)
    t.style = "Light Grid Accent 1"
    hdr = t.rows[0].cells
    hdr[0].text, hdr[1].text, hdr[2].text = "Workforce area", "Employed with 2+ jobs (%)", "Qualifies"
    for a in AREAS:
        c = t.add_row().cells
        c[0].text, c[1].text, c[2].text = names[a], pct1(F["share"][a]), "Yes" if a in F["certified"] else "No"
    src_line = d.add_paragraph()
    rr_ = src_line.add_run("Source: Tamarack Household Employment Survey, 2025Q4 to 2026Q3, final weights; LMIB "
                           "calculations. Southwest Lakes' 2026Q3 weights are the 16 October reissue; the first issue "
                           "leaves every area's qualification unchanged.")
    rr_.italic = True
    rr_.font.size = Pt(8.5)
    d.add_picture(io.BytesIO(chart_png(F)), width=Inches(6.0))
    d.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    p("Survey quality", bold=True, after=2)
    p("Household response rates over the same four quarters ran from %s percent (%s) to %s percent (%s). Rates by "
      "area are in the workbook pba_pilot_areas_2027.xlsx, with noncontact rates; housing units found vacant or "
      "demolished at the visit are left out of the base." %
      (pct1(min(F["rr"].values())), names[min(F["rr"], key=F["rr"].get)], pct1(max(F["rr"].values())),
       names[max(F["rr"], key=F["rr"].get)]))
    foot = d.sections[0].footer.paragraphs[0]
    foot.text = "Labor Market Information Bureau, Tamarack Department of Labor and Industry"
    foot.runs[0].font.size = Pt(8)
    common.docx_props(d, "Mackenzie Parks", "2027 pilot areas", created=(2026, 10, 23, 11, 30),
                      modified=(2026, 10, 23, 14, 5))
    d.save(path)
    common.normalise_zip(path, "2026-10-23T20:05:00Z", "Microsoft Office Word")


def write_goldens(F, gdir):
    os.makedirs(gdir, exist_ok=True)
    write_workbook(F, os.path.join(gdir, WB))
    write_memo(F, os.path.join(gdir, MEMO))
