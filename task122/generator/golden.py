"""The golden deliverables: the executive team paper (docx, with its chart) and the trial figures workbook (xlsx).
Every figure comes from figures.json, computed by figs.py from target/."""
import datetime as dt
import io
import os
import re
import sys
import zipfile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt   # noqa: E402
import numpy as np   # noqa: E402
import openpyxl   # noqa: E402
from docx import Document   # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH   # noqa: E402
from docx.oxml import OxmlElement   # noqa: E402
from docx.oxml.ns import qn   # noqa: E402
from docx.shared import Cm, Pt, RGBColor   # noqa: E402
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P   # noqa: E402

DOCX = "probe_decision_2027.docx"
XLSX = "probe_trial_figures.xlsx"
MONTHS = ["April", "May", "June", "July", "August", "September"]
INK = "#1f2a33"
OFF_C = "#9aa5ae"
ON_C = "#1d5f8a"


def chart(fig, path):
    lv = fig["chart"]
    x = np.arange(len(lv["levels"]))
    f, (a1, a2) = plt.subplots(1, 2, figsize=(9.2, 3.6), dpi=160, gridspec_kw={"width_ratios": [1, 1.25]})
    for a in (a1, a2):
        a.spines[["top", "right"]].set_visible(False)
        a.tick_params(colors=INK, labelsize=8.5)
        for sp in ("left", "bottom"):
            a.spines[sp].set_color("#7d8790")
    a1.bar(x, [100 * v for v in lv["share_running"]], color=ON_C, width=0.62)
    a1.set_xticks(x, lv["levels"])
    a1.set_xlabel("Aircraft climbing or descending in the sector", fontsize=8.5, color=INK)
    a1.set_ylabel("Minutes with the probe running (%)", fontsize=8.5, color=INK)
    a1.set_title("Planners ran the probe when climbs and descents gathered", fontsize=9.2, color=INK, loc="left")
    for xi, v in zip(x, lv["share_running"]):
        a1.text(xi, 100 * v + 1.2, "%d" % round(100 * v), ha="center", fontsize=7.6, color=INK)
    w = 0.38
    a2.bar(x - w / 2, lv["expected"], width=w, color=OFF_C, label="Would have raised without the probe")
    a2.bar(x + w / 2, lv["observed"], width=w, color=ON_C, label="Raised with the probe running")
    a2.set_xticks(x, lv["levels"])
    a2.set_xlabel("Aircraft climbing or descending in the sector", fontsize=8.5, color=INK)
    a2.set_ylabel("STCA activations in the probe's running time", fontsize=8.5, color=INK)
    a2.set_title("Fewer activations at every level of climbing and descending traffic", fontsize=9.2, color=INK,
                 loc="left")
    a2.legend(frameon=False, fontsize=7.6, loc="upper right")
    f.text(0.01, 0.005, "Source: FDPS crossing list, STCA log and planner workstation log, 1 April to 30 September 2026. "
           "Expected counts from the minutes without the probe in the same sector with the same number of aircraft "
           "and the same number climbing or descending.", fontsize=6.6, color="#5b6670")
    f.tight_layout(rect=(0, 0.04, 1, 1))
    f.savefig(path, format="png", metadata={"Software": None})
    plt.close(f)


def _field(par, code):
    r = par.add_run()
    a = OxmlElement("w:fldChar")
    a.set(qn("w:fldCharType"), "begin")
    b = OxmlElement("w:instrText")
    b.set(qn("xml:space"), "preserve")
    b.text = code
    c = OxmlElement("w:fldChar")
    c.set(qn("w:fldCharType"), "end")
    r._r.append(a)
    r._r.append(b)
    r._r.append(c)


def _cell(c, text, bold=False, align=None, size=9):
    c.text = ""
    p = c.paragraphs[0]
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    if align == "r":
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT


def paper(fig, path, png):
    d = Document()
    sec = d.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    sec.left_margin = sec.right_margin = Cm(2.2)
    sec.top_margin, sec.bottom_margin = Cm(1.9), Cm(1.8)
    st = d.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    hdr = sec.header.paragraphs[0]
    hdr.text = "Tasman Air Navigation  |  Executive team paper ET 2026/11-04  |  In confidence"
    hdr.runs[0].font.size = Pt(7.5)
    hdr.runs[0].font.color.rgb = RGBColor(0x5b, 0x66, 0x70)
    ft = sec.footer.paragraphs[0]
    ft.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = ft.add_run("Page ")
    r.font.size = Pt(7.5)
    _field(ft, "PAGE")

    def para(text, bold=False, size=10, space=6, color=None, italic=False):
        p = d.add_paragraph()
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.size = Pt(size)
        if color:
            run.font.color.rgb = RGBColor.from_string(color)
        p.paragraph_format.space_after = Pt(space)
        return p

    t = d.add_table(rows=5, cols=2)
    meta = [("To", "Executive team, meeting of 10 November 2026"),
            ("From", "Tessa Freeman, Human Factors Lead, Area Control Centre"),
            ("Prepared by", "Kieran McMurray, Safety Analyst"),
            ("Date", "30 October 2026"),
            ("Subject", "PROBE-M: mandatory use at every en-route planner position from 1 April 2027")]
    for row, (k, v) in zip(t.rows, meta):
        _cell(row.cells[0], k, bold=True)
        _cell(row.cells[1], v)
        row.cells[0].width = Cm(3.2)
        row.cells[1].width = Cm(13.4)
    para("", space=2)
    pct = fig["share_prevented_pct_nearest5"]
    para("PROBE-M prevented about %d per cent of the STCA activations in the time it ran. We recommend it becomes "
         "mandatory at every en-route planner position from 1 April 2027." % pct, bold=True, size=12.5, space=8,
         color="1F2A33")
    para("Decision sought", bold=True, size=10.5, space=3)
    para("That the executive team makes PROBE-M mandatory at the planner positions of KAIPARA, HAURAKI, WAIKATO, "
         "TARANAKI, TAUPO and KAPITI from 1 April 2027, with the training in the first quarter of 2027 set out in "
         "the training plan.")
    para("The criterion", bold=True, size=10.5, space=3)
    para("The Safety Review Board's acceptance criteria (SRB 2026/04, section 3.1) make the probe mandatory if, over "
         "the trial, its use prevented at least one in five of the STCA activations the six sectors would have raised "
         "in the time it was running. Activations are counted as the Safety Performance Report counts them: live "
         "alerts, once per event, in the sector where the alert began.")
    para("What the trial shows", bold=True, size=10.5, space=3)
    para("Over the trial the probe ran for %s sector-hours. In that time the six sectors raised %s "
         "activations. Minutes without the probe in the same sector, with the same number of aircraft in the sector "
         "and the same number of them climbing or descending, put the activations the sectors would have raised in "
         "that time at %s. The probe prevented %s of them, about %d per cent, above the one in five the criterion "
         "asks for." % ("{:,}".format(fig["probe_hours"]), "{:,}".format(fig["observed"]),
                         "{:,}".format(int(round(fig["expected"]))), "{:,}".format(int(round(fig["prevented"]))), pct))
    para("Why the published rate points the other way", bold=True, size=10.5, space=3)
    para("On the Safety Performance Report's own measure, activations per 1,000 flight hours, the sectors ran at %.1f "
         "with the probe on and %.1f with it off. That comparison sets the probe's minutes against quieter ones. "
         "Planners switched the probe on as climbing and descending traffic gathered around the Auckland and "
         "Wellington banks, and almost every activation involves an aircraft climbing or descending, so the minutes "
         "the probe ran carried more of that traffic than the minutes it did not, even at the same number of "
         "aircraft in the sector. Read at the same count and the same climbing and descending traffic, minute by "
         "minute, the probe's minutes raised fewer activations at every level of traffic (Figure 1)."
         % (fig["rate_on_per_1000fh"], fig["rate_off_per_1000fh"]))
    d.add_picture(png, width=Cm(16.4))
    cap = para("Figure 1. Left: the share of minutes with the probe running, by the number of aircraft climbing or "
               "descending in the sector. Right: activations in the probe's running time, as raised and as the same "
               "traffic raised without the probe.", size=8, space=8, color="5B6670")
    para("The trial in figures", bold=True, size=10.5, space=3)
    tb = d.add_table(rows=1, cols=2)
    tb.style = "Light List"
    _cell(tb.rows[0].cells[0], "Measure", bold=True)
    _cell(tb.rows[0].cells[1], "Trial, 1 April to 30 September 2026", bold=True, align="r")
    lines = [("Probe running, sector-hours", "{:,}".format(fig["probe_hours"])),
             ("Activations raised in that time", "{:,}".format(fig["observed"])),
             ("Activations the same traffic would have raised without the probe", "{:,}".format(int(round(fig["expected"])))),
             ("Activations prevented", "{:,}".format(int(round(fig["prevented"])))),
             ("Share prevented", "about %d per cent (criterion: 20 per cent)" % pct)]
    for k, v in lines:
        row = tb.add_row()
        _cell(row.cells[0], k)
        _cell(row.cells[1], v, align="r")
    para("", space=2)
    para("Activations are live STCA alerts once per event in the sector where they began (Safety Performance Report "
         "2024/25, section 2). Expected counts sum, over the probe's running minutes, the rate of the minutes without "
         "it in the same sector at the same number of aircraft and the same number climbing or descending.",
         size=8, space=8, color="5B6670", italic=True)
    para("Introducing the mandate", bold=True, size=10.5, space=3)
    para("The training plan schedules a classroom module, two simulator sessions and a competency check for every "
         "planner between January and March 2027, with backfill on the roster. The planners' survey and the "
         "workload ratings go to the Safety Review Board with the rollout plan; under the acceptance criteria they "
         "inform how the mandate is introduced, not whether.")
    d.core_properties.author = "Kieran McMurray"
    d.core_properties.last_modified_by = "Tessa Freeman"
    d.core_properties.created = dt.datetime(2026, 10, 26, 21, 4, 0)
    d.core_properties.modified = dt.datetime(2026, 10, 29, 23, 41, 0)
    d.core_properties.revision = 7
    d.core_properties.title = "PROBE-M: mandatory use from 1 April 2027"
    d.core_properties.comments = ""
    buf = io.BytesIO()
    d.save(buf)
    _restamp(buf.getvalue(), path, dt.datetime(2026, 10, 29, 23, 41, 0), b"Microsoft Office Word")


def _restamp(data, path, when, app):
    src = zipfile.ZipFile(io.BytesIO(data))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for info in src.infolist():
            b = src.read(info.filename)
            if info.filename == "docProps/app.xml":
                b = re.sub(rb"<Application>[^<]*</Application>", b"<Application>" + app + b"</Application>", b)
            zi = zipfile.ZipInfo(info.filename, date_time=when.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, b)


def workbook(fig, path):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    thin = Side(style="thin", color="B7BEC4")
    head = Font(bold=True, color="FFFFFF")
    fill = PatternFill("solid", fgColor="1D5F8A")

    def sheet(title, header, rows, fmt, widths, note):
        ws = wb.create_sheet(title)
        ws.append([note])
        ws["A1"].font = Font(italic=True, color="5B6670", size=9)
        ws.append(header)
        for c in ws[2]:
            c.font = head
            c.fill = fill
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        for r in rows:
            ws.append(list(r))
        for row in ws.iter_rows(min_row=3, max_row=ws.max_row):
            for j, c in enumerate(row):
                if j > 0:
                    c.number_format = fmt
                    c.alignment = Alignment(horizontal="right")
                c.border = Border(bottom=thin)
        for col, w in zip("ABCDEFGHI", widths):
            ws.column_dimensions[col].width = w
        ws.freeze_panes = "B3"
        return ws

    hrs = fig["flight_hours"]
    rows = [[s] + hrs[s] for s in P.SECTORS]
    sheet("Flight hours", ["Sector"] + [m + " 2026" for m in MONTHS], rows, "#,##0", (12, 12, 12, 12, 12, 12, 12),
          "Flight hours by sector and month, New Zealand time; each flight's crossings from its latest plan "
          "revision, split at month ends. Whole hours.")
    rt = fig["stca_rate"]
    rows = [[s] + rt[s] for s in P.SECTORS]
    sheet("STCA rate", ["Sector"] + [m + " 2026" for m in MONTHS], rows, "0.0", (12, 12, 12, 12, 12, 12, 12),
          "STCA activations per 1,000 flight hours, counted as the Safety Performance Report counts them (live, once "
          "per event, where it began). One decimal.")
    fh = fig["flights_handled"]
    sheet("Flights handled", ["Sector", "Flights handled, 1 April to 30 September 2026"],
          [[s, fh[s]] for s in P.SECTORS], "#,##0", (12, 30),
          "Each flight once in each sector it entered, however many times it entered it.")
    ws = wb.create_sheet("Probe effect")
    ws.append(["The probe's running time against the same traffic without it, by sector"])
    ws["A1"].font = Font(italic=True, color="5B6670", size=9)
    ws.append(["Sector", "Probe running (hours)", "Activations raised", "Would have raised without the probe",
               "Prevented"])
    for c in ws[2]:
        c.font = head
        c.fill = fill
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for s in P.SECTORS:
        b = fig["by_sector"][s]
        ws.append([s, b["hours"], b["observed"], b["expected"], b["prevented"]])
    ws.append(["All sectors", fig["probe_hours"], fig["observed"], round(fig["expected"], 1), round(fig["prevented"], 1)])
    for row in ws.iter_rows(min_row=3, max_row=ws.max_row):
        for j, c in enumerate(row):
            if j in (1, 2):
                c.number_format = "#,##0"
            elif j in (3, 4):
                c.number_format = "#,##0.0"
            if j > 0:
                c.alignment = Alignment(horizontal="right")
    for c in ws[ws.max_row]:
        c.font = Font(bold=True)
    ws.append([])
    ws.append(["Share prevented, all sectors", "about %d per cent" % fig["share_prevented_pct_nearest5"]])
    ws.append(["Expected counts: for each probe-running minute, the rate of the minutes without the probe in the same "
               "sector with the same number of aircraft and the same number climbing or descending."])
    for col, w in zip("ABCDE", (28, 18, 16, 22, 14)):
        ws.column_dimensions[col].width = w
    ws = wb.create_sheet("Notes")
    for line in ["Sources: FDPS crossing list, STCA log, planner workstation log and configuration log, 1 April to "
                 "30 September 2026 (extracts of 5 October 2026); Safety Performance Report 2024/25 for the definitions.",
                 "Times: the FDPS and STCA logs are in UTC, the planner workstation and configuration logs in New "
                 "Zealand time (NZDT to 5 April, NZST to 27 September, NZDT after).",
                 "Combined sectors: overnight the sectors run in pairs (KPA/HKI, WKO/TKI, TPO/KPT); a combined "
                 "position's probe covers both sectors, and a combined-sector activation is counted in the sector "
                 "that held the first-named aircraft.",
                 "Prepared by K. McMurray, Safety Analyst, 29 October 2026."]:
        ws.append([line])
    ws.column_dimensions["A"].width = 120
    wb.properties.creator = "Kieran McMurray"
    wb.properties.lastModifiedBy = "Kieran McMurray"
    wb.properties.created = dt.datetime(2026, 10, 22, 2, 15, 0)
    wb.properties.modified = dt.datetime(2026, 10, 29, 4, 2, 0)
    buf = io.BytesIO()
    wb.save(buf)
    src = zipfile.ZipFile(io.BytesIO(buf.getvalue()))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for info in src.infolist():
            b = src.read(info.filename)
            if info.filename == "docProps/app.xml":
                b = re.sub(rb"<Application>[^<]*</Application>", b"<Application>Microsoft Excel</Application>", b)
            if info.filename == "docProps/core.xml":
                b = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                           b"\\g<1>2026-10-29T04:02:00Z\\g<2>", b)
                b = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)",
                           b"\\g<1>2026-10-22T02:15:00Z\\g<2>", b)
            zi = zipfile.ZipInfo(info.filename, date_time=(2026, 10, 29, 17, 2, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, b)


def write_all(golden_dir, fig):
    os.makedirs(golden_dir, exist_ok=True)
    png = os.path.join(golden_dir, "_figure1.png")
    chart(fig, png)
    paper(fig, os.path.join(golden_dir, DOCX), png)
    os.remove(png)
    workbook(fig, os.path.join(golden_dir, XLSX))
