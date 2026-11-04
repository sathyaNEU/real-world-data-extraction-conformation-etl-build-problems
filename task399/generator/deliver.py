"""The golden deliverables, written from golden.compute(target): the panel's slides and the staffing and ARS
workbook, and the figures every write-up block is drafted from."""
import datetime as dt
import math
import os

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import postprocess as PP

DECK = "improvement_plan_case_2027.pptx"
BOOK = "staffing_and_ars_2025-26.xlsx"
DESK = {"W01": "Fenmoor", "W02": "Callowby", "W03": "Hatherby", "W04": "Tollinghurst", "W05": "Kestrow",
        "W06": "Wellanby"}
PROGRAMMES = {"A": "Signaller competence: route setting and regulating", "B": "Workstation display renewal",
              "C": "Eight-hour shifts", "D": "ARS timetable data rebuild", "E": "Seventh workstation"}


def r1(x):
    return round(x + 1e-9, 1)


def figures(res):
    M = res["main"]
    F = dict(call="B", call_name=PROGRAMMES["B"], call_minutes=M["b_minutes"], start_ws=M["start_ws"],
             start_ws_name=DESK[M["start_ws"]], b_by_ws={w: M["b_by_ws"][w] for w in DESK},
             total_oc_minutes=M["total"], slip_count=M["n_slips"], slip_minutes=M["slip_minutes"],
             eq_count=M["n_eq"], eq_minutes=M["eq_minutes"], findings=M["findings"],
             default_by_programme=M["by_prog_findings"],
             default_call="A", default_minutes=M["by_prog_findings"].get("A"),
             cited=dict(window_end_day=30, tor_sections=["2.2", "2.3", "2.4", "2.5"]),
             quick_cancels=M["quick_cancels"], quick_cancels_beside=M["quick_cancels_beside"],
             rs1_count=len(M["rs1_gaps"]), rs1_far=sum(1 for g in M["rs1_gaps"] if g > 12),
             # bounds round toward the bound: a range's floor down, its ceiling up
             gap_close_min_px=math.floor(10 * min(g for g in M["rs1_gaps"] if g <= 12)) / 10,
             gap_close_max_px=math.ceil(10 * max(g for g in M["rs1_gaps"] if g <= 12)) / 10,
             gap_far_min_px=math.floor(min(g for g in M["rs1_gaps"] if g > 12)),
             hours={w: {"first two years": r1(res["hours"][(w, "first two years")]),
                        "other": r1(res["hours"][(w, "other")])} for w in DESK},
             hours_raw={w: {"first two years": res["hours"][(w, "first two years")],
                            "other": res["hours"][(w, "other")]} for w in DESK},
             ars={w: {q: r1(res["ars"][(w, q)]) for q in ("2025 Q4", "2026 Q1", "2026 Q2", "2026 Q3")} for w in DESK},
             ars_raw={w: {q: res["ars"][(w, q)] for q in ("2025 Q4", "2026 Q1", "2026 Q2", "2026 Q3")} for w in DESK})
    return F


def write_book(F, path):
    wb = openpyxl.Workbook()
    thin = Side(style="thin", color="A6A6A6")
    box = Border(left=thin, right=thin, top=thin, bottom=thin)
    head = PatternFill("solid", fgColor="D9E1F2")
    sh = wb.active
    sh.title = "Signaller hours"
    sh["A1"] = "Hours worked on each workstation, 1 October 2025 to 30 September 2026"
    sh["A1"].font = Font(bold=True, size=12)
    sh["A2"] = "Signallers in their first two years since qualifying at the time worked, and the rest. Hours on the clock."
    sh["A2"].font = Font(italic=True, size=9, color="595959")
    cols = ["Workstation", "First two years (h)", "Other signallers (h)", "All (h)"]
    for c, v in enumerate(cols, start=1):
        cell = sh.cell(row=4, column=c, value=v)
        cell.font = Font(bold=True)
        cell.fill = head
        cell.border = box
        cell.alignment = Alignment(horizontal="center" if c > 1 else "left", wrap_text=True)
    row = 5
    for w in DESK:
        a = F["hours"][w]["first two years"]
        b = F["hours"][w]["other"]
        vals = ["%s %s" % (w, DESK[w]), a, b, r1(F["hours_raw"][w]["first two years"] + F["hours_raw"][w]["other"])]
        for c, v in enumerate(vals, start=1):
            cell = sh.cell(row=row, column=c, value=v)
            cell.border = box
            if c > 1:
                cell.number_format = "#,##0.0"
        row += 1
    tot = ["All workstations", r1(sum(F["hours_raw"][w]["first two years"] for w in DESK)),
           r1(sum(F["hours_raw"][w]["other"] for w in DESK)),
           r1(sum(F["hours_raw"][w]["first two years"] + F["hours_raw"][w]["other"] for w in DESK))]
    for c, v in enumerate(tot, start=1):
        cell = sh.cell(row=row, column=c, value=v)
        cell.border = box
        cell.font = Font(bold=True)
        if c > 1:
            cell.number_format = "#,##0.0"
    sh.column_dimensions["A"].width = 20
    for c in "BCD":
        sh.column_dimensions[c].width = 17
    sh.freeze_panes = "B5"
    sh.page_setup.orientation = "landscape"
    sh.print_title_rows = "4:4"
    sh2 = wb.create_sheet("ARS off")
    sh2["A1"] = "ARS sub-area hours switched off, by workstation and quarter"
    sh2["A1"].font = Font(bold=True, size=12)
    sh2["A2"] = "Summed over each workstation's sub-areas; quarters in UK time. October 2025 to September 2026."
    sh2["A2"].font = Font(italic=True, size=9, color="595959")
    qs = ["2025 Q4", "2026 Q1", "2026 Q2", "2026 Q3"]
    labels = ["Oct-Dec 2025", "Jan-Mar 2026", "Apr-Jun 2026", "Jul-Sep 2026"]
    for c, v in enumerate(["Workstation"] + labels, start=1):
        cell = sh2.cell(row=4, column=c, value=v)
        cell.font = Font(bold=True)
        cell.fill = head
        cell.border = box
        cell.alignment = Alignment(horizontal="center" if c > 1 else "left")
    row = 5
    for w in DESK:
        for c, v in enumerate(["%s %s" % (w, DESK[w])] + [F["ars"][w][q] for q in qs], start=1):
            cell = sh2.cell(row=row, column=c, value=v)
            cell.border = box
            if c > 1:
                cell.number_format = "#,##0.0"
        row += 1
    for c, v in enumerate(["All workstations"] + [r1(sum(F["ars_raw"][w][q] for w in DESK)) for q in qs], start=1):
        cell = sh2.cell(row=row, column=c, value=v)
        cell.border = box
        cell.font = Font(bold=True)
        if c > 1:
            cell.number_format = "#,##0.0"
    sh2.column_dimensions["A"].width = 20
    for c in "BCDE":
        sh2.column_dimensions[c].width = 14
    sh2.freeze_panes = "B5"
    sh2.page_setup.orientation = "landscape"
    sh2.print_title_rows = "4:4"
    sh3 = wb.create_sheet("Notes")
    notes = [
        ("Prepared", "Safety and assurance, Fenmoor ROC, for the 2027 improvement plan case (ToR WR-SRP-TOR-26-04, 3.2)."),
        ("Period", "1 October 2025 to 30 September 2026, UK time."),
        ("Signaller hours", "Each shift's signaller is the one the control system shows working the workstation "
                            "(roc_signaller_actions_20251001_20260930.csv): relief duties have no desk in the rosters, "
                            "and some changes made on the day never reached the roster changes list."),
        ("", "Shift times from the 2025-26 and 2026-27 rosters and the roster changes list; sickness cover from the "
             "time on the changes list. Hours are on the clock: the nights of 25 October 2025 and 28 March 2026 "
             "ran 13 and 11 hours."),
        ("", "First two years: from the date qualified in the signaller competence register to its second "
             "anniversary, by the date and time worked."),
        ("ARS off", "From ars_status_log_20251001_20260930.csv. Server B stamps Central European time in the "
                    "logged_utc column (its copies of server A's events sit one hour behind in winter, two in "
                    "summer); read as such, both servers merged into one event per change."),
        ("", "Sub-area codes before release 8.2 mapped to the current codes through the r8.2.1 layout export; a "
             "workstation-wide switch-off applies to every sub-area of the workstation until each is switched "
             "back on."),
        ("", "Hours summed over each workstation's sub-areas within each calendar quarter, UK time."),
        ("Rounding", "Hours to one decimal; totals from unrounded hours."),
    ]
    sh3["A1"] = "Notes"
    sh3["A1"].font = Font(bold=True, size=12)
    for k, (a_, b_) in enumerate(notes, start=3):
        sh3.cell(row=k, column=1, value=a_ or None).font = Font(bold=True)
        cell = sh3.cell(row=k, column=2, value=b_)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    sh3.column_dimensions["A"].width = 16
    sh3.column_dimensions["B"].width = 110
    wb.save(path)
    PP.normalize_ooxml(path, "Helen Douglas", "Helen Douglas", "2026-10-12T09:05:00Z", "2026-10-14T16:41:00Z",
                       title="Staffing and ARS, 2025-26", excel=True)


def fix_embedded(path, author, created, modified):
    """The chart's embedded workbook carries the deck's own author and dates, not the writing library's."""
    import io
    import re
    import zipfile
    zin = zipfile.ZipFile(path)
    items = [(i.filename, zin.read(i.filename)) for i in zin.infolist()]
    zin.close()
    out = []
    for name, data in items:
        if name.startswith("ppt/embeddings/") and name.endswith(".xlsx"):
            zi = zipfile.ZipFile(io.BytesIO(data))
            inner = [(j.filename, zi.read(j.filename)) for j in zi.infolist()]
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zo:
                for n2, d2 in inner:
                    if n2 == "docProps/core.xml":
                        d2 = re.sub(rb"<dc:creator>[^<]*</dc:creator>|<dc:creator/>",
                                    b"<dc:creator>" + author.encode() + b"</dc:creator>", d2)
                        d2 = re.sub(rb"<cp:lastModifiedBy>[^<]*</cp:lastModifiedBy>|<cp:lastModifiedBy/>",
                                    b"<cp:lastModifiedBy>" + author.encode() + b"</cp:lastModifiedBy>", d2)
                        d2 = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)",
                                    rb"\g<1>" + created.encode() + rb"\g<2>", d2)
                        d2 = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                                    rb"\g<1>" + modified.encode() + rb"\g<2>", d2)
                    info = zipfile.ZipInfo(n2, date_time=(1980, 1, 1, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    zo.writestr(info, d2)
            data = buf.getvalue()
        out.append((name, data))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zo:
        for name, data in out:
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            zo.writestr(info, data)


def write_deck(F, path):
    from pptx import Presentation
    from pptx.chart.data import CategoryChartData
    from pptx.dml.color import RGBColor
    from pptx.enum.chart import XL_CHART_TYPE
    from pptx.enum.text import PP_ALIGN
    from pptx.util import Emu, Pt
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    blank = prs.slide_layouts[6]
    navy = RGBColor(0x17, 0x45, 0x6B)
    grey = RGBColor(0x59, 0x59, 0x59)

    def title(slide, text, sub=None):
        tb = slide.shapes.add_textbox(Emu(457200), Emu(300000), Emu(11277600), Emu(820000))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = navy
        if sub:
            q = tf.add_paragraph()
            q.text = sub
            q.font.size = Pt(13)
            q.font.color.rgb = grey

    def foot(slide, text, number):
        tb = slide.shapes.add_textbox(Emu(457200), Emu(6230000), Emu(10500000), Emu(450000))
        tb.text_frame.word_wrap = True
        p = tb.text_frame.paragraphs[0]
        p.text = text
        p.font.size = Pt(9)
        p.font.color.rgb = grey
        nb = slide.shapes.add_textbox(Emu(11050000), Emu(6230000), Emu(680000), Emu(300000))
        q = nb.text_frame.paragraphs[0]
        q.text = "%d" % number
        q.font.size = Pt(9)
        q.font.color.rgb = grey
        q.alignment = PP_ALIGN.RIGHT

    s = prs.slides.add_slide(blank)
    title(s, "Fund B: the workstation display renewal",
          "Fenmoor ROC 2027 operating improvement plan: the case for the Safety Review Panel, for review by the head "
          "of operations and the operating centre manager before circulation")
    tb = s.shapes.add_textbox(Emu(457200), Emu(1600000), Emu(11277600), Emu(3800000))
    tf = tb.text_frame
    tf.word_wrap = True
    lines = [("{:,}".format(F["call_minutes"]) + " delay minutes", 40, True),
             ("the operating centre's minutes in the twelve months to 30 September 2026 from incidents that would "
              "not have happened with the display renewal in place", 15, False),
             ("", 8, False),
             ("Wrong routes where the exit set was drawn beside the exit required: %d incidents, %s minutes" % (
                 F["slip_count"], "{:,}".format(F["slip_minutes"])), 15, False),
             ("Workstation display faults: %d incidents, %s minutes" % (F["eq_count"], "{:,}".format(F["eq_minutes"])),
              15, False)]
    for k, (t, sz, bold) in enumerate(lines):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        p.text = t
        p.font.size = Pt(sz)
        p.font.bold = bold
        p.font.color.rgb = navy if bold else RGBColor(0x26, 0x26, 0x26)
    foot(s, "Incidents in both operating incident registers that occurred 1 October 2025 to 30 September 2026, UK time. "
            "Minutes: primary and reactionary in the OCF delay records, after the attribution reviews recorded as agreed; "
            "reviews still under review are not applied (ToR WR-SRP-TOR-26-04, 2.2 to 2.4).", 1)
    s = prs.slides.add_slide(blank)
    title(s, "Begin the renewal on %s %s" % (F["start_ws"], F["start_ws_name"]),
          "The display renewal's delay minutes by workstation, October 2025 to September 2026")
    order = sorted(DESK, key=lambda x: -F["b_by_ws"][x])
    cd = CategoryChartData()
    cd.categories = ["%s %s" % (w, DESK[w]) for w in order]
    cd.add_series("Delay minutes", [F["b_by_ws"][w] for w in order])
    gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Emu(457200), Emu(1400000), Emu(8300000), Emu(4700000), cd)
    ch = gf.chart
    ch.has_legend = False
    ch.has_title = False
    pl = ch.plots[0]
    pl.gap_width = 55
    pl.has_data_labels = True
    pl.data_labels.number_format = "#,##0"
    pl.data_labels.number_format_is_linked = False
    pl.data_labels.font.size = Pt(12)
    ch.category_axis.reverse_order = True
    ch.category_axis.tick_labels.font.size = Pt(12)
    ch.value_axis.visible = False
    ch.value_axis.has_major_gridlines = False
    ser = ch.series[0]
    ser.format.fill.solid()
    ser.format.fill.fore_color.rgb = RGBColor(0xA6, 0xA6, 0xA6)
    highlight = RGBColor(0x2F, 0x6E, 0xBA)
    for k, w in enumerate(order):
        if w == F["start_ws"]:
            pt = ser.points[k]
            pt.format.fill.solid()
            pt.format.fill.fore_color.rgb = highlight
    tb = s.shapes.add_textbox(Emu(9000000), Emu(1700000), Emu(2900000), Emu(3000000))
    tf = tb.text_frame
    tf.word_wrap = True
    for k, (t, sz, bold) in enumerate((("Delivery begins on %s %s" % (F["start_ws"], F["start_ws_name"]), 16, True),
                                       ("{:,} of the {:,} minutes".format(F["b_by_ws"][F["start_ws"]],
                                                                          F["call_minutes"]), 13, False),
                                       ("then the other workstations, about six weeks each, March to November 2027",
                                        12, False))):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        p.text = t
        p.font.size = Pt(sz)
        p.font.bold = bold
        p.font.color.rgb = navy if bold else RGBColor(0x26, 0x26, 0x26)
    foot(s, "Delivery runs one workstation at a time; ToR 2.5 starts it where it would have removed the most minutes. "
            "Workstation as recorded in the incident registers.", 2)
    prs.save(path)
    fix_embedded(path, "Helen Douglas", "2026-10-13T08:20:00Z", "2026-10-15T11:02:00Z")
    PP.normalize_ooxml(path, "Helen Douglas", "Helen Douglas", "2026-10-13T08:20:00Z", "2026-10-15T11:02:00Z",
                       title="Fenmoor ROC 2027 improvement plan case")


def write(res, golden_dir):
    F = figures(res)
    write_book(F, os.path.join(golden_dir, BOOK))
    write_deck(F, os.path.join(golden_dir, DECK))
    return F
