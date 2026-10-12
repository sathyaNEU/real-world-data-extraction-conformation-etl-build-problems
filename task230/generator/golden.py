"""The two deliverables: november_second_pass_plan.xlsx (the call and the three figures per stream) and
second_pass_november.pptx (hours against credit at stake, ordered by the credit)."""
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.util import Emu, Inches, Pt

import postprocess
import world as W

WORKBOOK = "november_second_pass_plan.xlsx"
SLIDE = "second_pass_november.pptx"
SYM = {"USD": "USD", "GBP": "GBP", "AUD": "AUD"}


def short(code):
    s = W.STREAMS[code]
    return {"N1": "Kessington institutional", "N2": "Kessington professional", "N3": "Northgate dental",
            "N4": "Brightmoor workers' comp", "N5": "Harbison pharmacy", "D1": "Wattlebird hospital",
            "D2": "Wattlebird extras", "D3": "Coolabah income protection", "D4": "Whinfell pet",
            "D5": "Thistlecombe motor", "D6": "Hollings & Pryce typed"}[code]


def workbook(A, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "November plan"
    ws["A1"] = "Second-pass verification, November 2026: proposal to the service quality council"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Forecasts per QCP-04 4.1 to 4.3 from the Q3 first-pass log, the blind re-key audit and plan of record v3."
    ws["A2"].font = Font(italic=True, size=9, color="555555")
    hdr = ["Stream", "Client", "Queue (Nov)", "Limit per 1,000 key fields", "Second pass in November",
           "Second-pass hours, November", "Credit at stake, November", "Currency", "Q3 residual, client audit (per 1,000 key fields)"]
    thin = Side(style="thin", color="B7BEC8")
    for j, h in enumerate(hdr, start=1):
        c = ws.cell(row=4, column=j, value=h)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="2F4A6D")
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = Border(bottom=thin)
    r = 5
    for code in W.ORDER:
        yes = code in A["call"]
        vals = [W.SID[code], W.CLIENTS[W.STREAMS[code]["client"]]["name"], {"N": "Night", "D": "Day"}[W.STREAMS[code]["nov"]],
                A["limits"][code], "Yes" if yes else "No", A["hours"][code], A["credit"][code],
                W.CLIENTS[W.STREAMS[code]["client"]]["ccy"], A["client_audit"].get(code)]
        for j, v in enumerate(vals, start=1):
            c = ws.cell(row=r, column=j, value=v)
            c.border = Border(bottom=thin)
            if j == 4:
                c.number_format = "0.00" if code == "D6" else "0.0"
            if j in (6, 7):
                c.number_format = "#,##0"
            if j == 9:
                c.number_format = "0.0"
            if j == 5 and yes:
                c.font = Font(bold=True, color="9C2B23")
        if code == "D6":
            ws.cell(row=r, column=9, value="n/a")
            ws.cell(row=r, column=9).alignment = Alignment(horizontal="right")
        r += 1
    r += 1
    ws.cell(row=r, column=1, value="Hollings & Pryce: no client audit before Q1 2027 under its quality schedule.").font = Font(size=9, color="555555")
    ws.cell(row=r + 1, column=1, value="Credit at stake: the schedule's credit percentage of the stream's November invoice at plan volumes, in contract currency.").font = Font(size=9, color="555555")
    for col, w in zip("ABCDEFGHI", (12, 32, 11, 14, 14, 14, 15, 10, 20)):
        ws.column_dimensions[col].width = w
    ws.print_area = f"A1:I{r + 1}"
    ws.print_title_rows = "4:4"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    nt = wb.create_sheet("Notes")
    notes = [
        ("As of", "28 Oct 2026; Q3 exports closed, plan of record v3 (issued 23 Oct)"),
        ("Second pass", "Yes where the November first-pass residual forecast exceeds the schedule limit (QCP-04 4.2)"),
        ("Hours", "Plan documents (key fields over the form version's key fields per document, by shift-day) x September "
                  "productive minutes per document for the form family, sessions split at handover counted per part"),
        ("Credit at stake", "Schedule credit % x November invoice: plan documents priced at the account's November band, "
                            "anniversary indexation from its shift-day"),
        ("Client audit", "Capture-code findings per 1,000 key fields on sampled claims delivered in Jul-Sep by the client's "
                         "local date; a re-review replaces the original finding"),
    ]
    for a, b in notes:
        nt.append([a, b])
        nt.cell(row=nt.max_row, column=1).font = Font(bold=True)
        nt.cell(row=nt.max_row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
    nt.column_dimensions["A"].width = 16
    nt.column_dimensions["B"].width = 100
    ws.row_dimensions[4].height = 45
    ws.freeze_panes = "A5"
    wb.save(path)
    postprocess.scrub(path, W.PEOPLE["ops"], "2026-10-29")
    postprocess.finish_office(path, "2026-10-28T05:10:00Z", "2026-10-29T09:35:00Z", W.ORG)


def slide(A, path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    s = prs.slides.add_slide(prs.slide_layouts[5])
    order = A["chart_order"]
    lead = order[0]
    s.shapes.title.text = f"{short(lead)} carries the most credit at stake in November"
    ttl = s.shapes.title
    ttl.left, ttl.top, ttl.width, ttl.height = Inches(0.4), Inches(0.35), Inches(12.5), Inches(0.9)
    tf = ttl.text_frame
    from pptx.enum.text import PP_ALIGN
    tf.paragraphs[0].alignment = PP_ALIGN.LEFT
    tf.paragraphs[0].runs[0].font.size = Pt(26)
    tf.paragraphs[0].runs[0].font.bold = True
    cats = [f"{short(c)} ({W.CLIENTS[W.STREAMS[c]['client']]['ccy']} {A['credit'][c]:,})" for c in order]
    cd = CategoryChartData()
    cd.categories = list(reversed(cats))
    cd.add_series("Credit at stake, INR '000 at FY27 budget rates", [round(A["credit_inr"][c] / 1000, 1) for c in reversed(order)])
    gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(0.4), Inches(1.45), Inches(7.6), Inches(5.6), cd)
    ch = gf.chart
    ch.has_legend = False
    ch.has_title = True
    ch.chart_title.text_frame.text = "Credit at stake (INR '000 at budget rates; contract amount in brackets)"
    ch.chart_title.text_frame.paragraphs[0].runs[0].font.size = Pt(12)
    pl = ch.plots[0]
    pl.gap_width = 60
    pl.has_data_labels = True
    pl.data_labels.number_format = "#,##0.0"
    pl.data_labels.number_format_is_linked = False
    pl.data_labels.font.size = Pt(9)
    pl.series[0].format.fill.solid()
    pl.series[0].format.fill.fore_color.rgb = RGBColor(0x2F, 0x4A, 0x6D)
    ch.category_axis.tick_labels.font.size = Pt(9)
    ch.value_axis.tick_labels.font.size = Pt(9)
    cd2 = CategoryChartData()
    cd2.categories = list(reversed([short(c) for c in order]))
    cd2.add_series("Second-pass hours, November", [A["hours"][c] for c in reversed(order)])
    gf2 = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(8.2), Inches(1.45), Inches(4.8), Inches(5.6), cd2)
    c2 = gf2.chart
    c2.has_legend = False
    c2.has_title = True
    c2.chart_title.text_frame.text = "Second-pass hours, November"
    c2.chart_title.text_frame.paragraphs[0].runs[0].font.size = Pt(12)
    p2 = c2.plots[0]
    p2.gap_width = 60
    p2.has_data_labels = True
    p2.data_labels.number_format = "#,##0"
    p2.data_labels.number_format_is_linked = False
    p2.data_labels.font.size = Pt(9)
    p2.series[0].format.fill.solid()
    p2.series[0].format.fill.fore_color.rgb = RGBColor(0x8A, 0x9B, 0xB0)
    c2.category_axis.tick_labels.font.size = Pt(9)
    c2.value_axis.tick_labels.font.size = Pt(9)
    tb = s.shapes.add_textbox(Inches(0.4), Inches(7.05), Inches(12.5), Inches(0.35))
    tb.text_frame.text = ("Streams ordered by credit at stake. Credit: schedule percentage of the November invoice at plan volumes. "
                          "Hours: plan documents times September minutes per document for the form family.")
    tb.text_frame.paragraphs[0].runs[0].font.size = Pt(9)
    tb.text_frame.paragraphs[0].runs[0].font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    sn = s.shapes.add_textbox(Inches(12.6), Inches(7.05), Inches(0.5), Inches(0.35))
    sn.text_frame.text = "1"
    sn.text_frame.paragraphs[0].runs[0].font.size = Pt(9)
    prs.core_properties.author = W.PEOPLE["ops"]
    prs.core_properties.last_modified_by = W.PEOPLE["ops"]
    prs.core_properties.title = "Second pass, November 2026"
    prs.core_properties.comments = ""
    import datetime as _dt
    prs.core_properties.created = _dt.datetime(2026, 10, 28, 5, 40)
    prs.core_properties.modified = _dt.datetime(2026, 10, 29, 9, 20)
    prs.core_properties.revision = 3
    prs.save(path)
    _fix_embedded(path)
    postprocess.scrub(path, W.PEOPLE["ops"], "2026-10-29")


def _fix_embedded(path):
    """the chart workbooks python-pptx embeds carry the build clock; give them the deck's own date, and lay the
    package out with fixed entry stamps so two builds are byte-identical"""
    import io
    import re
    import zipfile
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    out = []
    for n, b in items:
        if n.endswith(".xlsx"):
            with zipfile.ZipFile(io.BytesIO(b)) as zz:
                inner = [(i.filename, zz.read(i.filename)) for i in zz.infolist()]
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zo:
                for m, bb in inner:
                    if m == "docProps/core.xml":
                        bb = re.sub(rb"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", b"2026-10-29T09:20:00Z", bb)
                        bb = re.sub(rb"<dc:creator>[^<]*</dc:creator>", b"<dc:creator>" + W.PEOPLE["ops"].encode() + b"</dc:creator>", bb)
                    zi = zipfile.ZipInfo(m, date_time=(1980, 1, 1, 0, 0, 0))
                    zi.compress_type = zipfile.ZIP_DEFLATED
                    zo.writestr(zi, bb)
            b = buf.getvalue()
        out.append((n, b))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for n, b in out:
            zi = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, b)


def write(A, golden_dir):
    os.makedirs(golden_dir, exist_ok=True)
    workbook(A, os.path.join(golden_dir, WORKBOOK))
    slide(A, os.path.join(golden_dir, SLIDE))
