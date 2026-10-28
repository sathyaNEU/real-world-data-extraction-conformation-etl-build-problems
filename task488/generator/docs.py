"""Governing documents (PDF through reportlab with fixed metadata so rebuilds are byte-identical) and the workbook
metadata pin."""
from __future__ import annotations

import io
import re
import zipfile

from reportlab import rl_config
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

rl_config.invariant = 1

BODY = ParagraphStyle("b", fontName="Helvetica", fontSize=9.5, leading=12.5, spaceAfter=5)
HEAD = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10.5, leading=13, spaceBefore=6, spaceAfter=4)
TITLE = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=12.5, leading=15, spaceAfter=3)
SMALL = ParagraphStyle("s", fontName="Helvetica", fontSize=8, leading=10, textColor=colors.HexColor("#444444"))

APP_XML = (b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Properties xmlns="http://schemas.openxmlformats.'
           b'org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/'
           b'2006/docPropsVTypes"><Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity><ScaleCrop>'
           b'false</ScaleCrop><Company>%s</Company><AppVersion>16.0300</AppVersion></Properties>')


def _p(t, s=BODY):
    return Paragraph(t, s)


def pdf(path, story, title, author, created, tz="-05'00'"):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=author, producer=author,
                            subject="", keywords="")
    doc.build(story)
    data = buf.getvalue()
    stamp = (created.strftime("D:%Y%m%d%H%M%S") + tz).encode()
    data = re.sub(rb"/CreationDate \(D:[^)]*\)", b"/CreationDate (" + stamp + b")", data)
    data = re.sub(rb"/ModDate \(D:[^)]*\)", b"/ModDate (" + stamp + b")", data)
    for sig in (b"ReportLab Generated PDF document (opensource)",
                b"ReportLab generated PDF document -- digest (opensource)"):
        data = data.replace(sig, b" " * len(sig))
    assert b"reportlab" not in data.lower()
    with open(path, "wb") as f:
        f.write(data)


def table(rows, widths, head=True):
    t = Table(rows, colWidths=widths)
    st = [("FONT", (0, 0), (-1, -1), "Helvetica", 8.5), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#555555"))]
    if head:
        st.append(("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.5))
    t.setStyle(TableStyle(st))
    return t


def fixed_xlsx(path, when, company, author):
    stamp = ("%04d-%02d-%02dT%02d:%02d:%02dZ" % when).encode()
    with zipfile.ZipFile(path) as z:
        items = [(i, z.read(i.filename)) for i in z.infolist()]
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for info, data in items:
            if info.filename == "docProps/core.xml":
                data = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", rb"\g<1>" + stamp + rb"\g<2>", data)
                data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>" + stamp + rb"\g<2>", data)
                data = re.sub(rb"(<dc:creator[^>]*>)[^<]*(</dc:creator>)", rb"\g<1>" + author + rb"\g<2>", data)
                data = re.sub(rb"(<cp:lastModifiedBy[^>]*>)[^<]*(</cp:lastModifiedBy>)", rb"\g<1>" + author + rb"\g<2>", data)
            if info.filename == "docProps/app.xml":
                data = APP_XML % company
            zi = zipfile.ZipInfo(info.filename, date_time=when)
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)


def scale_note(path):
    import datetime as dt
    import params as P
    s = [_p("Quarrystone Regional Assessment Consortium", SMALL),
         _p("Quarrystone Interim, Mathematics: Scale and Cut Scores", TITLE),
         _p("Adopted by the Assessment Committee, 17 June 2021. Cut scores reviewed and kept, 12 August 2024.", SMALL),
         Spacer(1, 6)]
    secs = [
        ("1. The scale",
         "Each grade's results are reported on its own scale, the Quarrystone scale score (QSS), a linear "
         "transformation of the Rasch ability scale: QSS = 500 + 40 x theta, theta in logits. The scale was set by "
         "the spring 2021 launch calibration, in which the difficulty of every launch item was estimated under the "
         "Rasch model from the launch field test. Item difficulties and student "
         "scores are on the same scale: a student whose score equals an item's difficulty has an even chance of "
         "answering it correctly. The launch values are stored in the item bank to a tenth of a point."),
        ("2. Reporting",
         "Scale scores are reported as whole points from 340 to 660, each with its standard error of measurement. "
         "A test event that is invalidated is not reported."),
        ("3. Cut scores",
         "The cut scores below divide each grade's scale into four performance levels: Beginning, Approaching, "
         "Meets and Exceeds. A score at or above a cut is in the level the cut opens."),
    ]
    for h, b in secs:
        s += [_p(h, HEAD), _p(b)]
    rows = [["Grade", "Approaching", "Meets", "Exceeds"]]
    for g in P.GRADES:
        c = P.CUT_QSS[g]
        rows.append([str(g), "%d" % c, "%d" % (c + 27 + (g % 3)), "%d" % (c + 63 + (g % 2) * 2)])
    s += [table(rows, [30 * mm, 35 * mm, 35 * mm, 35 * mm]), Spacer(1, 8),
          _p("4. Use", HEAD),
          _p("The levels are reported to families and teachers after each window. Placement in district intervention "
             "programmes is a district decision and may use other evidence.")]
    pdf(path, s, "Quarrystone Interim scale and cut scores", "Quarrystone Regional Assessment Consortium",
        dt.datetime(2024, 8, 12, 15, 30))


def corvane_spec(path):
    import datetime as dt
    import params as P
    s = [_p("Corvane Assessment", SMALL),
         _p("Item Pool Import Specification, version 3.2", TITLE),
         _p("Prepared for the Quarrystone Regional Assessment Consortium, 9 February 2027. Applies to pools loaded "
            "for delivery from 1 July 2027.", SMALL), Spacer(1, 6)]
    secs = [
        ("1. Pools",
         "The import loads one pool for each grade. An item is in a grade's pool if it is operational in that grade "
         "at the time of the import; retired items are not loaded. Each item is loaded once, under the key of its "
         "current version."),
        ("2. Fields",
         "Each item is loaded with: item_key; grade; difficulty, on the customer's reporting scale, to one decimal; "
         "reporting_domain, the code of the domain the item reports to in the customer's 2026 mathematics "
         "framework; enemy_set, an identifier shared by the items of one enemy set; interaction_type. An item "
         "calibrated before the import keeps its existing difficulty. An item without a difficulty on the scale "
         "cannot be loaded."),
        ("3. Difficulties for items not yet calibrated",
         "The customer supplies a difficulty on its scale for every operational item not yet calibrated, estimated "
         "from the customer's 2025-26 operational responses: the responses scored in complete and incomplete test "
         "events. Responses from invalidated events are not operational."),
        ("4. Enemy sets",
         "An enemy set is two or more items of one grade's pool that must not be delivered in the same test. An "
         "item belongs to at most one set. Items of different grades' pools are never in one set."),
        ("5. Pool floor",
         "Adaptive delivery needs depth below grade level. A grade's pool must hold at least %d items whose "
         "difficulty is below the grade's Approaching cut before it opens for delivery. Where a pool is short, the "
         "customer commissions the difference as new items for field testing in the first window, and the pool "
         "opens once the commission is confirmed." % P.FLOOR),
    ]
    for h, b in secs:
        s += [_p(h, HEAD), _p(b)]
    pdf(path, s, "Item Pool Import Specification 3.2", "Corvane Assessment", dt.datetime(2027, 2, 9, 10, 15),
        tz="-06'00'")
