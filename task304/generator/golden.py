"""task304 architecture 5: the golden deliverables, written from figures.json (computed by analysis.py from target/).

junction_bid_2027.docx: the county's bid document (the junction, every listed junction's benefit, a bar chart marking the
junction chosen, the estimate in one paragraph). bid_annex_2026.xlsx: the guidance's Annex A tables A1 and A2."""
import datetime as dt
import io
import os
import re
import zipfile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from docx import Document  # noqa: E402
from docx.enum.table import WD_TABLE_ALIGNMENT  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.shared import Pt, RGBColor, Mm  # noqa: E402
import openpyxl  # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill  # noqa: E402

ACCENT = "#0A6AA8"
MUTED = "#7C8C97"
INK = RGBColor(0x1F, 0x2A, 0x33)
GREY = RGBColor(0x6B, 0x77, 0x80)
LAYOUT = {"X": "Crossroads", "T": "T junction", "ST": "Staggered"}


def chart_png(F):
    names = sorted(F["junctions"], key=lambda n: -F["benefit"][n])
    vals = [F["benefit"][n] for n in names]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "svg.hashsalt": "task304"})
    fig, ax = plt.subplots(figsize=(6.6, 2.75), dpi=200)
    colors = [ACCENT if n == F["call"] else MUTED for n in names]
    bars = ax.bar(range(len(names)), vals, color=colors, width=0.62)
    for b_, v in zip(bars, vals):
        ax.text(b_.get_x() + b_.get_width() / 2, v + 0.03, "%.1f" % v, ha="center", va="bottom", fontsize=8.5, color="#1F2A33")
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels([n.replace(" Junction", "\nJunction").replace(" Crossroads", "\nCrossroads") for n in names], fontsize=8)
    ax.set_ylabel("Injury collisions prevented a year", fontsize=8.5)
    ax.set_ylim(0, max(vals) * 1.28)
    k = names.index(F["call"])
    ax.annotate("%s, the junction chosen" % F["call"], xy=(k, vals[k] + 0.17), xytext=(k + 0.55, max(vals) * 1.17),
                fontsize=8.5, color=ACCENT, fontweight="bold", ha="left",
                arrowprops=dict(arrowstyle="-", color=ACCENT, lw=0.8))
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color("#9AA5AD")
    ax.spines["bottom"].set_color("#9AA5AD")
    ax.tick_params(colors="#4A555D")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def _para(doc, text, size=10.5, bold=False, color=INK, space_after=6, italic=False):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    p.paragraph_format.space_after = Pt(space_after)
    return p


def bid_docx(path, F):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(22)
    sec.top_margin = sec.bottom_margin = Mm(20)
    best, ru = F["call"], F["runner_up"]
    _para(doc, "Junction Safety Fund 2027: Ardleshire County Council bid", 10, color=GREY, space_after=2)
    _para(doc, "Prepared by Halberd Transport Planning for Ardleshire County Council under the road safety engineering "
               "term contract. Alison Hartley, 4 December 2026. Bids close on 29 January 2027.", 9, color=GREY, space_after=10)
    _para(doc, "%s: a roundabout would prevent %.1f injury collisions a year" % (best, F["call_benefit"]), 17, bold=True,
          space_after=8)
    _para(doc, "1. The junction and the scheme", 12, bold=True, space_after=4)
    _para(doc, "The county bids for a roundabout at %s (node %s), the %s of %s. As it stands, at its 2026 traffic, the "
               "junction can be expected to have %.1f injury collisions a year; with the fund's crash modification factor "
               "for a %s of %.2f, a roundabout would prevent %.1f a year, more than at any other junction the 2026 "
               "screening listed. %s comes next at %.1f a year." % (
                   best, F["nodes"][best], LAYOUT[F["layout"][best]].lower(), F["roads"][best].replace(" / ", " and "),
                   F["call_expected"], LAYOUT[F["layout"][best]].lower(), F["cmf"][best], F["call_benefit"], ru,
                   F["runner_up_benefit"]))
    _para(doc, "2. Every listed junction's benefit", 12, bold=True, space_after=4)
    names = sorted(F["junctions"], key=lambda n: -F["benefit"][n])
    t = doc.add_table(rows=1 + len(names), cols=4)
    t.style = "Light Grid Accent 1"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    head = ["Junction", "Layout", "Crash modification factor", "Injury collisions prevented a year"]
    for j, h in enumerate(head):
        c = t.cell(0, j)
        c.text = h
        c.paragraphs[0].runs[0].font.bold = True
        c.paragraphs[0].runs[0].font.size = Pt(9.5)
    for i, n in enumerate(names, start=1):
        vals = [n, LAYOUT[F["layout"][n]], "%.2f" % F["cmf"][n], "%.1f" % F["benefit"][n]]
        for j, v in enumerate(vals):
            c = t.cell(i, j)
            c.text = v
            run = c.paragraphs[0].runs[0]
            run.font.size = Pt(9.5)
            run.font.bold = (n == best)
            if j >= 2:
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    _para(doc, "Source: the county's validated collision record 2021 to 2025 and junction inventory; factors from the "
               "fund's guidance, Table 2.", 8.5, color=GREY, space_after=8)
    doc.add_picture(io.BytesIO(chart_png(F)), width=Mm(150))
    _para(doc, "Figure 1. Injury collisions a roundabout would prevent each year at each listed junction.", 8.5, color=GREY,
          space_after=10)
    _para(doc, "3. How the expected collisions were estimated", 12, bold=True, space_after=4)
    _para(doc, "A junction listed for its recent collisions has, on average, fewer in the years that follow, because the "
               "count that put it on the list carries chance as well as risk. Each listed junction's expected annual injury "
               "collisions therefore combine its own 2021 to 2025 count with what the county's %s give-way and "
               "stop-controlled T, staggered and crossroads junctions of its layout and traffic have had (a safety "
               "performance function on major and minor road traffic, fitted by negative binomial regression), each "
               "weighted by how far those junctions spread beyond chance, and are carried to the junction's 2026 traffic. "
               "%s had the most collisions on the list but carries little traffic, so most of its count is chance; "
               "%s carries the most traffic but its own record runs well below what its traffic predicts." % (
                   "{:,}".format(F["reference_junctions"]), F["observed_route"], F["model_route"]))
    _para(doc, "Holt Lane's traffic fell by about a fifth from 2024 (junction inventory), so Saxby Cross's expected collisions "
               "are at its lower 2026 traffic. The supporting tables of the guidance's Annex A are in bid_annex_2026.xlsx.",
          8.5, color=GREY, italic=True, space_after=4)
    doc.core_properties.author = "Alison Hartley"
    doc.core_properties.last_modified_by = "Alison Hartley"
    doc.core_properties.title = "Junction Safety Fund 2027 bid"
    doc.core_properties.comments = ""
    doc.core_properties.created = dt.datetime(2026, 12, 2, 9, 31, 0)
    doc.core_properties.modified = dt.datetime(2026, 12, 4, 16, 12, 0)
    doc.core_properties.revision = 4
    doc.save(path)
    _normalise(path, "Microsoft Office Word")


def _normalise(path, app):
    buf = io.BytesIO()
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in sorted(zin.infolist(), key=lambda i: i.filename):
            data = zin.read(item.filename)
            if item.filename == "docProps/app.xml":
                data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>" + app.encode() + b"</Application>", data)
                data = data.replace(b"python-docx", app.encode())
            if item.filename == "docProps/core.xml":
                data = data.replace(b"generated using python-docx", b"")
            zi = zipfile.ZipInfo(item.filename, date_time=(2026, 12, 4, 16, 12, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            zout.writestr(zi, data)
    with open(path, "wb") as f:
        f.write(buf.getvalue())


def annex_xlsx(path, F):
    wb = openpyxl.Workbook()
    head_fill = PatternFill("solid", fgColor="1F2A33")
    sheets = [("A1 Collisions by severity", "Injury collisions on roads Ardleshire County Council is highway authority for, 2026, "
               "by quarter and severity (30-day definition)", ["Fatal", "Serious", "Slight"], F["ask_a"]),
              ("A2 Casualties by road user", "Casualties of those collisions, 2026, by quarter and road user",
               ["Pedestrian", "Pedal cyclist", "Motorcyclist", "Car occupant"], F["ask_b"])]
    first = True
    for title, caption, cols, data in sheets:
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = title
        ws["A1"] = caption
        ws["A1"].font = Font(bold=True, size=11)
        ws.append([])
        ws.append(["Quarter"] + cols + ["Total"])
        for c in ws[3]:
            c.font = Font(bold=True, color="FFFFFF")
            c.fill = head_fill
            c.alignment = Alignment(horizontal="center", wrap_text=True)
        for q in (1, 2, 3):
            vals = [data["Q%d" % q][c] for c in cols]
            ws.append(["Q%d 2026 (%s)" % (q, F["quarters"][str(q)] if str(q) in F["quarters"] else F["quarters"][q])] + vals + [sum(vals)])
        tot = [sum(data["Q%d" % q][c] for q in (1, 2, 3)) for c in cols]
        ws.append(["January to September 2026"] + tot + [sum(tot)])
        for c in ws[7]:
            c.font = Font(bold=True)
        for row in ws.iter_rows(min_row=4, max_row=7, min_col=2):
            for c in row:
                c.number_format = "#,##0"
                c.alignment = Alignment(horizontal="right")
        ws.column_dimensions["A"].width = 34
        for col in "BCDEF":
            ws.column_dimensions[col].width = 15
        ws.freeze_panes = "B4"
        ws.append([])
        ws.append(["Source: Ardleshire Police provisional collision data (old system to 31 May, new system from 1 June 2026), "
                   "the Fatal Collision Investigation Unit's notifications, and the county's road network register."])
        ws.cell(row=ws.max_row, column=1).font = Font(italic=True, size=9, color="6B7780")
    wb.properties.creator = "Alison Hartley"
    wb.properties.lastModifiedBy = "Alison Hartley"
    wb.save(path)
    buf = io.BytesIO()
    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<cp:coreProperties '
            'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<dc:creator>Alison Hartley</dc:creator><cp:lastModifiedBy>Alison Hartley</cp:lastModifiedBy>'
            '<dcterms:created xsi:type="dcterms:W3CDTF">2026-12-03T10:05:00Z</dcterms:created>'
            '<dcterms:modified xsi:type="dcterms:W3CDTF">2026-12-04T15:47:00Z</dcterms:modified></cp:coreProperties>')
    app = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Properties '
           'xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
           'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Microsoft Excel'
           '</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop><Company>Halberd Transport Planning'
           '</Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc><HyperlinksChanged>false'
           '</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>')
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in sorted(zin.infolist(), key=lambda i: i.filename):
            data = zin.read(item.filename)
            if item.filename == "docProps/core.xml":
                data = core.encode()
            elif item.filename == "docProps/app.xml":
                data = app.encode()
            zi = zipfile.ZipInfo(item.filename, date_time=(2026, 12, 4, 15, 47, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            zout.writestr(zi, data)
    with open(path, "wb") as f:
        f.write(buf.getvalue())


def write(golden_dir, F):
    os.makedirs(golden_dir, exist_ok=True)
    bid_docx(os.path.join(golden_dir, "junction_bid_2027.docx"), F)
    annex_xlsx(os.path.join(golden_dir, "bid_annex_2026.xlsx"), F)
