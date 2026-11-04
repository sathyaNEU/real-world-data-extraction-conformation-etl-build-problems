"""task211 golden deliverables, written from generator/figures.json: golden/placement.xlsx and golden/panel_deck.pptx.
Run after build.py: python3 task211/generator/golden.py"""
import io, json, os, re, zipfile, datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
OUT = os.path.join(TASK, "golden")
F = json.load(open(os.path.join(HERE, "figures.json")))
ST = F["stated"]
STAMP = dt.datetime(2026, 9, 30, 16, 5, 0)
AUTHOR = "Andreas Jespersen"
SITES = sorted(F["avoided_days"], key=lambda s: -F["avoided_days"][s])
NAVY = RGBColor(0x1F, 0x3A, 0x5F); GREY = RGBColor(0x9A, 0xA5, 0xB1)


def scrub(path, app):
    with open(path, "rb") as f:
        data = scrub_bytes(f.read(), app)
    with open(path, "wb") as f:
        f.write(data)


def scrub_bytes(blob, app):
    src = zipfile.ZipFile(io.BytesIO(blob))
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for info in sorted(src.infolist(), key=lambda i: i.filename):
            data = src.read(info.filename)
            if info.filename == "docProps/core.xml":
                for tag in ("created", "modified"):
                    data = re.sub(rb"(<dcterms:%s[^>]*>)[^<]*(<)" % tag.encode(),
                                  rb"\g<1>" + STAMP.strftime("%Y-%m-%dT%H:%M:%SZ").encode() + rb"\g<2>", data)
                data = re.sub(rb"<cp:revision>[^<]*</cp:revision>", b"<cp:revision>4</cp:revision>", data)
            if info.filename == "docProps/app.xml":
                data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>" + app + b"</Application>", data)
                data = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0000</AppVersion>", data)
            if info.filename.endswith(".xlsx"):
                data = scrub_bytes(data, b"Microsoft Excel")
            zi = zipfile.ZipInfo(info.filename, (2026, 9, 30, 16, 5, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)
    return out.getvalue()


def workbook():
    wb = Workbook(); ws = wb.active; ws.title = "Placement"
    bold = Font(bold=True); head = PatternFill("solid", fgColor="DCE3EC")
    ws.append(["NM Atlas placement, winter campaign 1 Nov 2026 to 28 Feb 2027"]); ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Fleet weather downtime per campaign plan section 4.3, 18 winters of buoy record 2008/09 to 2025/26, "
               "whole days"])
    ws.append([])
    ws.append(["Site", "Downtime avoided with NM Atlas there (days)", "Own floating-vessel downtime, all sites floating (days)"])
    for c in ws[4]:
        c.font = bold; c.fill = head; c.alignment = Alignment(wrap_text=True, vertical="top")
    for s in SITES:
        ws.append([s, ST["avoided_whole_days"][s], ST["own_whole_days"][s]])
    ws.append([])
    ws.append(["Pick", F["call"]]); ws.append(["Runner-up", F["runner_up"]]); ws.append(["Gap (days)", ST["gap_whole_days"]])
    for r in range(11, 14):
        ws.cell(r, 1).font = bold
    for col, w in zip("ABC", (24, 30, 34)):
        ws.column_dimensions[col].width = w
    ws.row_dimensions[4].height = 32
    d = wb.create_sheet("Developer standby")
    d.append(["Developer", "Winter", "Standby acknowledged (days)"])
    for k, v in sorted(F["ask_statements_days"].items()):
        dev, win = k.split("|")
        d.append([dev, win, round(v, 2)])
        d.cell(d.max_row, 3).number_format = "0.00"
    a = wb.create_sheet("NM Atlas standby")
    a.append(["Winter", "Weather standby (hours)"])
    for k, v in sorted(F["ask_atlas_weather_standby_hours"].items()):
        a.append([k, v])
    p = wb.create_sheet("Port dues")
    p.append(["Port", "Winter", "Shelter-call port dues (EUR)"])
    p.append(["Hjortby Havn", "2023/24", 0])
    for k, v in sorted(ST["port_dues_nearest_10"].items(), key=lambda x: (x[0].split("|")[0] != "Tranevig", x[0])):
        port, win = k.split("|")
        p.append([port, win, v])
        p.cell(p.max_row, 3).number_format = "#,##0"
    p.cell(2, 3).number_format = "#,##0"
    for sh in (d, a, p):
        for c in sh[1]:
            c.font = bold; c.fill = head
        for col in "ABC":
            sh.column_dimensions[col].width = 28
        sh.freeze_panes = "A2"
    ws.freeze_panes = "A5"
    n = wb.create_sheet("Notes")
    for line in [
            ["Basis", "Campaign plan NM-MO-CP-2627 rev. 3, sections 3 and 4; weather procedure WP-FHL rev. 4"],
            ["Record", "Buoy record at the five site buoys, winters 2008/09 to 2025/26, 1 Nov 00:00 to 28 Feb 24:00 Danish time"],
            ["Released vessel", "The floating vessel at NM Atlas's site takes no part in the campaign (plan section 2)"],
            ["Taken berth", "A vessel finding its shelter port's heavy-lift berth taken goes on to the Kalvholm storm "
                            "moorings, as every such arrival in the 2023/24 to 2025/26 progress reports did"],
            ["Developer standby", "Statement lines by the month the standby was worked; a revision replaces only the "
                                  "line it restates"],
            ["NM Atlas standby", "Before the 15 Jan 2026 reporting go-live WW and WS were weather codes; the 15 to 25 Jan "
                                 "gap is taken from the owner's final hire statement"],
            ["Port dues", "Shelter calls only; a Tranevig call carried over a week end is counted once"],
            ["As of", "25 Sep 2026"]]:
        n.append(line)
    n.column_dimensions["A"].width = 20; n.column_dimensions["B"].width = 110
    for c in n["A"]:
        c.font = bold
    pr = wb.properties
    pr.creator = AUTHOR; pr.lastModifiedBy = AUTHOR; pr.created = STAMP; pr.modified = STAMP
    path = os.path.join(OUT, "placement.xlsx")
    wb.save(path)
    scrub(path, b"Microsoft Excel")


def deck():
    prs = Presentation(); prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    def title(slide, text, sub=None):
        tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(12.1), Inches(1.0)).text_frame
        tb.word_wrap = True
        tb.text = text; tb.paragraphs[0].runs[0].font.size = Pt(26); tb.paragraphs[0].runs[0].font.bold = True
        tb.paragraphs[0].runs[0].font.color.rgb = NAVY
        if sub:
            p = tb.add_paragraph(); p.text = sub; p.runs[0].font.size = Pt(15)

    s1 = prs.slides.add_slide(blank)
    title(s1, "NM Atlas to Skarvgrund for winter 2026/27",
          "Avoids %d days of floating-vessel weather downtime, %d days more than at %s (%d)"
          % (ST["avoided_whole_days"][F["call"]], ST["gap_whole_days"], F["runner_up"], ST["avoided_whole_days"][F["runner_up"]]))
    tb = s1.shapes.add_textbox(Inches(0.6), Inches(2.0), Inches(12.0), Inches(4.0)).text_frame
    tb.word_wrap = True
    lines = ["Mobilisation order to be placed by 9 October 2026; campaign 1 November 2026 to 28 February 2027.",
             "Basis: campaign plan section 4.3, fleet weather downtime with and without the jack-up, 18 winters of buoy record.",
             "Skarvgrund and Lillevig Banke shelter at Bramso Havn, which has one heavy-lift berth. Fronts reach "
             "Skarvgrund first; when its vessel holds the berth, Lillevig Banke's goes on to the Kalvholm storm moorings "
             "(every such arrival in the 2023/24 to 2025/26 progress reports).",
             "With the jack-up at Skarvgrund those passages stop, so the placement saves Skarvgrund's own downtime and "
             "most of Lillevig Banke's extra."]
    for i, t in enumerate(lines):
        p = tb.paragraphs[0] if i == 0 else tb.add_paragraph()
        p.text = t; p.runs[0].font.size = Pt(16); p.space_after = Pt(10)

    s2 = prs.slides.add_slide(blank)
    title(s2, "Skarvgrund avoids the most downtime: %d days" % ST["avoided_whole_days"][F["call"]])
    cd = CategoryChartData(); cd.categories = SITES
    cd.add_series("Downtime avoided (days)", [ST["avoided_whole_days"][s] for s in SITES])
    gf = s2.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.8), Inches(1.5), Inches(11.6), Inches(5.4), cd)
    ch = gf.chart; ch.has_legend = False
    plot = ch.plots[0]; plot.gap_width = 70; plot.has_data_labels = True
    plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END; plot.data_labels.font.size = Pt(14)
    ser = plot.series[0]
    for i, s in enumerate(SITES):
        pt = ser.points[i]; pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = NAVY if s == F["call"] else GREY
    va = ch.value_axis; va.has_title = True; va.axis_title.text_frame.text = "Days a campaign, mean of 18 winters"
    va.minimum_scale = 0; va.has_major_gridlines = False
    va.axis_title.text_frame.paragraphs[0].runs[0].font.size = Pt(12)
    ch.category_axis.tick_labels.font.size = Pt(13)
    note = s2.shapes.add_textbox(Inches(9.0), Inches(1.4), Inches(3.6), Inches(0.6)).text_frame
    note.text = "Pick: %s" % F["call"]; note.paragraphs[0].runs[0].font.bold = True
    note.paragraphs[0].runs[0].font.color.rgb = NAVY

    s3 = prs.slides.add_slide(blank)
    title(s3, "Lillevig Banke's own downtime reaches %d days because its vessel goes on to Kalvholm when "
              "Skarvgrund's holds the berth" % ST["own_whole_days"]["Lillevig Banke"])
    tb = s3.shapes.add_textbox(Inches(0.6), Inches(1.6), Inches(12.0), Inches(4.5)).text_frame
    for i, s in enumerate(SITES):
        p = tb.paragraphs[0] if i == 0 else tb.add_paragraph()
        p.text = "%s: %d own, %d avoided with NM Atlas there" % (s, ST["own_whole_days"][s], ST["avoided_whole_days"][s])
        p.runs[0].font.size = Pt(18); p.space_after = Pt(8)
    for i, sl in enumerate(prs.slides, 1):
        ft = sl.shapes.add_textbox(Inches(0.6), Inches(7.0), Inches(12.1), Inches(0.35)).text_frame
        ft.text = ("Source: buoy record 2008/09 to 2025/26; campaign plan NM-MO-CP-2627 rev. 3; progress reports "
                   "2023/24 to 2025/26. Marine Operations, 30 September 2026.     %d" % i)
        ft.paragraphs[0].runs[0].font.size = Pt(10); ft.paragraphs[0].runs[0].font.color.rgb = GREY
    cp = prs.core_properties
    cp.author = AUTHOR; cp.last_modified_by = AUTHOR; cp.title = "NM Atlas placement 2026/27"
    cp.created = STAMP; cp.modified = STAMP; cp.revision = 4; cp.comments = ""; cp.subject = ""; cp.keywords = ""
    path = os.path.join(OUT, "panel_deck.pptx")
    prs.save(path)
    scrub(path, b"Microsoft Office PowerPoint")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    workbook(); deck()
    print(sorted(os.listdir(OUT)))
