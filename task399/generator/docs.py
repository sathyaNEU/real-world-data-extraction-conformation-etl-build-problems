"""The pack's governing and reference documents: the safety review panel's terms of reference for the 2027
operating improvement plan, the operating centre's improvement catalogue, and the 2025 workload assessment."""
import os

from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import hashlib
import re

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import postprocess as PP
import world as W

LIB = "/usr/share/fonts/truetype/liberation/"
DJV = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("LiberationSans", LIB + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSans-Bold", LIB + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans", DJV + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", DJV + "DejaVuSans-Bold.ttf"))
FONT = {"route": ("LiberationSans", "LiberationSans-Bold"), "consultant": ("DejaVuSans", "DejaVuSans-Bold")}

SS = getSampleStyleSheet()


def styles(house):
    reg, bold = FONT[house]
    return dict(
        BODY=ParagraphStyle("b" + house, parent=SS["BodyText"], fontName=reg, fontSize=9.4, leading=12.8,
                            alignment=TA_JUSTIFY, spaceAfter=4.5),
        H1=ParagraphStyle("h1" + house, parent=SS["Heading1"], fontName=bold, fontSize=13.5, spaceAfter=3, leading=16),
        H2=ParagraphStyle("h2" + house, parent=SS["Heading2"], fontName=bold, fontSize=10, spaceAfter=3, spaceBefore=7),
        SMALL=ParagraphStyle("s" + house, parent=SS["BodyText"], fontName=reg, fontSize=8, leading=10.2,
                             alignment=TA_JUSTIFY, spaceAfter=4),
        CELL=ParagraphStyle("c" + house, fontName=reg, fontSize=8.1, leading=10),
        CELLB=ParagraphStyle("cb" + house, fontName=bold, fontSize=8.1, leading=10))


ST = styles("route")
BODY, H1, H2, SMALL, CELL, CELLB = ST["BODY"], ST["H1"], ST["H2"], ST["SMALL"], ST["CELL"], ST["CELLB"]


def normalize_pdf(path, created, modified, title, producer="LibreOffice 24.2", creator="Writer", extra=None,
                  version="1.7"):
    """Re-serialised through a second library, so the writing library's banners and its info dictionary do not
    survive: in-fiction dates, the exporting suite's creator and producer strings, the title, and the font subset
    tags as other producers draw them (renamed at equal length inside the name tokens before the re-write)."""
    import io
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import ArrayObject, ByteStringObject, DictionaryObject, NameObject, TextStringObject
    b = open(path, "rb").read()
    tags = {}
    for m in re.finditer(rb"/([A-Z]{6})\+([A-Za-z0-9-]+)", b):
        key = m.group(0)
        if key not in tags:
            h = hashlib.sha256(key + created).digest()
            tags[key] = b"/" + bytes(65 + x % 26 for x in h[:6]) + b"+" + m.group(2)
    n = len(b)
    for o, nw in tags.items():
        b = re.sub(re.escape(o) + rb"(?![A-Za-z0-9-])", nw, b)
    assert len(b) == n
    wr = PdfWriter(clone_from=PdfReader(io.BytesIO(b)))
    info = wr._info.get_object() if hasattr(wr._info, "get_object") else wr._info
    for k in list(info.keys()):
        del info[k]
    meta = [("/Title", title), ("/Creator", creator), ("/Producer", producer),
            ("/CreationDate", created.decode()), ("/ModDate", modified.decode())] + list((extra or {}).items())
    for k, v in meta:
        info[NameObject(k)] = NameObject(v) if v.startswith("/") else TextStringObject(v)
    wr.pdf_header = "%PDF-" + version
    digest = hashlib.md5(b + created).digest()
    wr._ID = ArrayObject([ByteStringObject(digest), ByteStringObject(digest)])
    out = io.BytesIO()
    wr.write(out)
    data = out.getvalue()
    low = data.lower()
    assert b"reportlab" not in low and b"pypdf" not in low and b"AAAAAA+" not in data
    back = PdfReader(io.BytesIO(data), strict=True)
    assert dict(back.metadata) == dict(meta)
    open(path, "wb").write(data)


TBL = TableStyle([("GRID", (0, 0), (-1, -1), 0.3, colors.Color(0.45, 0.45, 0.45)),
                  ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.89, 0.91, 0.94)),
                  ("VALIGN", (0, 0), (-1, -1), "TOP"),
                  ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                  ("TOPPADDING", (0, 0), (-1, -1), 1.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6)])


def wrap(rows, widths=None, st=None):
    st = st or ST
    t = Table([[Paragraph(str(c), st["CELLB"] if i == 0 else st["CELL"]) for c in row] for i, row in enumerate(rows)],
              colWidths=widths, hAlign="LEFT")
    t.setStyle(TBL)
    return t


def furniture(doc_id, org_line, classification, house):
    reg, bold = FONT[house]

    def draw(canv, doc):
        canv.saveState()
        canv.setFont(reg, 7.4)
        canv.setFillColor(colors.Color(0.3, 0.3, 0.3))
        canv.drawString(18 * mm, 11 * mm, doc_id)
        if classification:
            canv.drawCentredString(A4[0] / 2, 11 * mm, classification)
        canv.drawRightString(A4[0] - 18 * mm, 11 * mm, "Page %d of %s" % (doc.page, doc._pages_total))
        top = A4[1] - 12 * mm
        if house == "route":
            # the route's mark: a block with a chevron, then the organisation line
            canv.setFillColor(colors.Color(0.09, 0.27, 0.42))
            canv.rect(18 * mm, top - 1.6 * mm, 7 * mm, 5.2 * mm, stroke=0, fill=1)
            canv.setStrokeColor(colors.white)
            canv.setLineWidth(1.1)
            p = canv.beginPath()
            p.moveTo(19.4 * mm, top - 0.4 * mm)
            p.lineTo(21.5 * mm, top + 2.4 * mm)
            p.lineTo(23.6 * mm, top - 0.4 * mm)
            canv.drawPath(p, stroke=1, fill=0)
            x0 = 27 * mm
        else:
            canv.setFillColor(colors.Color(0.33, 0.47, 0.25))
            canv.circle(20.5 * mm, top + 1.0 * mm, 2.5 * mm, stroke=0, fill=1)
            x0 = 25 * mm
        canv.setFillColor(colors.Color(0.15, 0.15, 0.15))
        canv.setFont(bold, 8.4)
        canv.drawString(x0, top, org_line)
        canv.setStrokeColor(colors.Color(0.35, 0.35, 0.35))
        canv.setLineWidth(0.6)
        canv.line(18 * mm, A4[1] - 15 * mm, A4[0] - 18 * mm, A4[1] - 15 * mm)
        canv.restoreState()
    return draw


def two_pass(path, story_fn, doc_id, title, org_line, created, modified, classification="OFFICIAL", house="route",
             tool=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    total = "?"
    for _ in range(2):
        d = SimpleDocTemplate(path, pagesize=A4, title=title, author="", subject="", creator="Writer",
                              leftMargin=18 * mm, rightMargin=18 * mm, topMargin=21 * mm, bottomMargin=18 * mm)
        d._pages_total = total
        f = furniture(doc_id, org_line, classification, house)
        d.build(story_fn(), onFirstPage=f, onLaterPages=f)
        total = str(d.page)
    normalize_pdf(path, created, modified, title, **(tool or {}))


def signatures(rows, st=None):
    return wrap([["Role", "Name", "Signature", "Date"]] + rows, widths=[52 * mm, 44 * mm, 40 * mm, 32 * mm], st=st)


def terms_of_reference(path):
    def story():
        return [
            Paragraph("Fenmoor Rail Operating Centre: 2027 operating improvement plan", H1),
            Paragraph("Terms of reference of the Wyvern Route Safety Review Panel for the plan. Document "
                      "WR-SRP-TOR-26-04, revision 1, approved by the Panel on 3 September 2026.", SMALL),
            Paragraph("1 Purpose", H2),
            Paragraph("1.1 The safety regulator's letter of 21 July 2026 (reference SR/26/1184) asked the route for an "
                      "improvement plan for the incidents caused at Fenmoor Rail Operating Centre. The route will send "
                      "the plan to the regulator by 15 December 2026.", BODY),
            Paragraph("1.2 The plan funds one programme from the operating centre's improvement catalogue (ROC-IC-2027) "
                      "for delivery in 2027. The Panel meets on 8 December 2026 to agree it.", BODY),
            Paragraph("2 Choosing the programme", H2),
            Paragraph("2.1 The plan funds the programme whose cause produced the most of the operating centre's delay "
                      "minutes in the twelve months from 1 October 2025 to 30 September 2026.", BODY),
            Paragraph("2.2 The operating centre's incidents are those in its operating incident register whose delay is "
                      "attributed to the operating centre (responsible code OCF). An incident belongs to the twelve "
                      "months by the date and time it occurred, UK time.", BODY),
            Paragraph("2.3 An incident counts for a programme when it would not have happened had that programme been in "
                      "place.", BODY),
            Paragraph("2.4 An incident's delay minutes are the primary and reactionary minutes held against its TRUST "
                      "incident in the delay attribution records, after the moves the attribution review log records as "
                      "agreed.", BODY),
            Paragraph("2.5 Where a programme is delivered in stages, the plan begins with the stage that would have "
                      "removed the most of those minutes.", BODY),
            Paragraph("3 The case", H2),
            Paragraph("3.1 The operating centre's safety and assurance manager prepares the case for the Panel and "
                      "circulates it seven days before the meeting. The head of operations and the operating centre "
                      "manager review it before it is circulated.", BODY),
            Paragraph("3.2 The Panel may ask for the case to be extended to the staffing and the ARS records the "
                      "programmes would change.", BODY),
            Paragraph("4 Membership", H2),
            wrap([["Member", "Role on the Panel"],
                  ["Route director, Wyvern", "Chair"],
                  ["Head of operations, Wyvern", "Member"],
                  ["Operating centre manager, Fenmoor", "Member"],
                  ["Route safety and assurance lead", "Member"],
                  ["Trade union health and safety representative", "Member"],
                  ["Operating centre safety and assurance manager", "Secretary"]], widths=[86 * mm, 82 * mm]),
            Paragraph("The Panel is quorate with the chair or the head of operations and two other members.", SMALL),
            Spacer(1, 6),
            wrap([["Rev", "Date", "Change"],
                  ["Draft A", "12 August 2026", "First draft for comment."],
                  ["1", "3 September 2026", "Approved. Sections 2.2 and 2.4 reworded after comment from the route "
                                           "performance team."]], widths=[16 * mm, 32 * mm, 120 * mm]),
            Spacer(1, 8),
            signatures([["Prepared (Secretary)", "Helen Douglas", "", "12 August 2026"],
                        ["Reviewed", "Alan Pope", "", "26 August 2026"],
                        ["Approved (Chair)", "Route director, Wyvern", "Minute SRP/26/31", "3 September 2026"]]),
        ]
    two_pass(path, story, "WR-SRP-TOR-26-04 rev 1", "Fenmoor ROC 2027 operating improvement plan: terms of reference",
             "Wyvern Route  |  Safety Review Panel", b"D:20260903161224+01'00'", b"D:20260903161224+01'00'")


def workload_assessment(path):
    rows = [["Workstation", "00:00-06:00", "06:00-09:00", "09:00-16:00", "16:00-19:00", "19:00-24:00"],
            ["W01 Fenmoor", "38", "71", "63", "77", "52"],
            ["W02 Callowby", "29", "58", "49", "61", "41"],
            ["W03 Hatherby", "44", "86", "72", "91", "63"],
            ["W04 Tollinghurst", "33", "62", "54", "66", "46"],
            ["W05 Kestrow", "27", "53", "46", "57", "38"],
            ["W06 Wellanby", "31", "57", "51", "60", "43"]]

    tasks = [["Workstation", "Route setting", "Regulating", "Telephone", "Possessions", "Describer and log", "Other"],
             ["W01 Fenmoor", "31", "9", "24", "17", "12", "7"],
             ["W02 Callowby", "27", "8", "27", "16", "13", "9"],
             ["W03 Hatherby", "35", "12", "21", "15", "11", "6"],
             ["W04 Tollinghurst", "29", "10", "25", "17", "12", "7"],
             ["W05 Kestrow", "24", "7", "29", "19", "13", "8"],
             ["W06 Wellanby", "28", "9", "26", "16", "12", "9"]]
    C = styles("consultant")
    b, h1, h2, sm = C["BODY"], C["H1"], C["H2"], C["SMALL"]

    def story():
        return [
            Paragraph("Signaller workload assessment: Fenmoor Rail Operating Centre", h1),
            Paragraph("Report LE-2512-R2 for the Wyvern route, issued 28 March 2025. Prepared by Linwell Ergonomics Ltd "
                      "under purchase order WR-4471163.", sm),
            Paragraph("1 Scope", h2),
            Paragraph("1.1 The route asked for an assessment of signaller workload on the six workstations at Fenmoor "
                      "before the December 2025 timetable is finalised. The assessment covers the workstations as "
                      "operated in January and February 2025, with ARS in normal service.", b),
            Paragraph("1.2 Workload was observed on 22 shifts (14 day, 8 night) across the six workstations. Two "
                      "observers recorded each signaller's tasks (route setting, regulating decisions, telephone "
                      "calls, possession management, train describer interposing, log entries) in five-minute "
                      "periods, and signallers rated their workload every thirty minutes on a ten-point scale.", b),
            Paragraph("1.3 The observers sat behind the workstation and did not speak to the signaller except at the "
                      "thirty-minute ratings. Periods when the signaller was on a break, or handed over to a relief "
                      "signaller, were left out.", b),
            Paragraph("2 Results", h2),
            Paragraph("2.1 Table 1 gives the workload index for each workstation and time band: the observed time on "
                      "task as a share of the period, adjusted for the concurrent tasks recorded, so that 100 is a "
                      "signaller fully occupied for the whole band. The index is the mean over the observed shifts.",
                      b),
            wrap(rows, widths=[34 * mm, 26 * mm, 26 * mm, 26 * mm, 26 * mm, 26 * mm], st=C),
            Paragraph("Table 1. Workload index by workstation and time band, January and February 2025.", sm),
            Paragraph("2.2 Index values above 80 are taken in this report as high and above 90 as very high. W03 "
                      "Hatherby reached the high band in both peaks, and the very high band on four of the six "
                      "evening peaks observed. No other workstation reached the high band in any observed period.", b),
            Paragraph("2.3 Table 2 gives the share of observed time on task by kind of task. Route setting is the "
                      "signaller's own route requests; routes set by ARS are not counted.", b),
            wrap(tasks, widths=[34 * mm, 23 * mm, 22 * mm, 22 * mm, 23 * mm, 27 * mm, 17 * mm], st=C),
            Paragraph("Table 2. Share of time on task by kind of task (per cent), all observed periods.", sm),
            Paragraph("2.4 Signallers' own ratings followed the index closely (correlation 0.81 over the 30-minute "
                      "periods). Ratings at night were higher than the index on W01 and W03, where possession "
                      "management took a large share of the night's tasks.", b),
            Paragraph("2.5 The December 2025 timetable, as consulted on in February 2025, adds stopping services in "
                      "both peaks on the Fenmoor, Hatherby and Tollinghurst areas. On the task times observed it would "
                      "add between four and nine points to those workstations' peak index.", b),
            Paragraph("3 Limitations", h2),
            Paragraph("3.1 Observation affects behaviour, and two months in winter do not cover the autumn railhead "
                      "conditions or the summer engineering programme. Night shifts were sampled less than day "
                      "shifts. The index does not measure the difficulty of individual tasks.", b),
            Spacer(1, 6),
            wrap([["Rev", "Date", "Change"],
                  ["R1", "14 March 2025", "Draft to the route."],
                  ["R2", "28 March 2025", "Issued. Table 1 night band corrected for W05; section 2.5 added."]],
                 widths=[16 * mm, 32 * mm, 120 * mm], st=C),
            Spacer(1, 8),
            signatures([["Author", "Joanna Bryan", "", "26 March 2025"],
                        ["Checked", "Julian Thomson", "", "27 March 2025"],
                        ["Accepted for the route", "Alan Pope", "", "7 April 2025"]], st=C),
        ]
    # the consultancy typesets its reports in LaTeX; the route's own documents come out of an office suite
    two_pass(path, story, "LE-2512-R2", "Signaller workload assessment: Fenmoor ROC", "Linwell Ergonomics Ltd",
             b"D:20250328110407Z", b"D:20250328110407Z", classification="", house="consultant",
             tool=dict(creator="LaTeX with hyperref", producer="pdfTeX-1.40.25", version="1.5",
                       extra={"/PTEX.Fullbanner": "This is pdfTeX, Version 3.141592653-2.6-1.40.25 (TeX Live 2023) "
                                                  "kpathsea version 6.3.5", "/Trapped": "/False"}))


def catalogue(path):
    import docx
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt, Mm
    d = docx.Document()
    sec = d.sections[0]
    sec.page_height, sec.page_width = Mm(297), Mm(210)
    sec.left_margin = sec.right_margin = Mm(20)
    st = d.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10)
    hdr = sec.header.paragraphs[0]
    hdr.text = "Fenmoor Rail Operating Centre    ROC-IC-2027 issue 2"
    hdr.runs[0].font.size = Pt(8)
    ftr = sec.footer.paragraphs[0]
    ftr.text = "OFFICIAL"
    ftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ftr.runs[0].font.size = Pt(8)
    pg = sec.footer.add_paragraph()
    pg.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for k, piece in enumerate(("Page ", "PAGE", " of ", "NUMPAGES")):
        r = pg.add_run(piece if k % 2 == 0 else "")
        r.font.size = Pt(8)
        if k % 2:
            field(r, piece, "1" if piece == "PAGE" else "2")
    d.add_heading("Improvement catalogue 2027", level=1)
    ref = d.add_table(rows=1, cols=4)
    ref.style = "Table Grid"
    for k, v in enumerate(("Reference ROC-IC-2027", "Issue 2", "30 July 2026", "OFFICIAL")):
        ref.cell(0, k).text = v
    d.add_paragraph("The programmes the operating centre can deliver in 2027, for the route's operating improvement "
                    "plan. Issue 2, 30 July 2026. Owner: operating centre manager.")
    progs = [
        ("A", "Signaller competence: route setting and regulating",
         "A simulator and mentoring programme for every signaller in their first two years since qualifying: four "
         "simulator days a year on the workstation they work, covering route setting, regulating and degraded "
         "working, and a mentor on one shift in four during the first year.",
         "412,000", "From February 2027; every signaller in scope enrolled by April 2027.", "Operating centre manager"),
        ("B", "Workstation display renewal",
         "The six workstations' display system (Corvane VDS-3, in service since 2013 and supported to March 2028) "
         "replaced by the supplier's current product, VDS-5, on larger screens, with every screen's track layout "
         "redrawn on the new product from the signalling plans. The VDS-3 equipment removed from every workstation. "
         "Delivered one workstation at a time.",
         "1,860,000", "March to November 2027, about six weeks a workstation.", "Head of operations"),
        ("C", "Eight-hour shifts",
         "The operating centre's 12-hour day and night shifts replaced by 8-hour early, late and night shifts, with "
         "four signallers recruited to cover the extra handovers.",
         "690,000 a year", "From the May 2027 roster period.", "Operating centre manager"),
        ("D", "ARS timetable data rebuild",
         "The ARS timetable data rebuilt from the December 2026 timetable, with every later data load checked "
         "independently before it goes live.",
         "238,000", "Rebuild by December 2026 load; checking from then on.", "Route timetable manager"),
        ("E", "Seventh workstation",
         "The Hatherby area split between W03 and a new workstation, W07, in the spare position on the operating "
         "floor, with five signallers recruited for the new workstation.",
         "1,120,000", "Commissioning in September 2027.", "Head of operations"),
    ]
    for code, title, scope, cost, when, sponsor in progs:
        d.add_heading("%s. %s" % (code, title), level=2)
        p = d.add_paragraph()
        p.add_run("Scope. ").bold = True
        p.add_run(scope)
        t = d.add_table(rows=3, cols=2)
        t.style = "Table Grid"
        for k, (a, b) in enumerate((("Cost (GBP)", cost), ("Delivery", when), ("Sponsor", sponsor))):
            t.cell(k, 0).text = a
            t.cell(k, 1).text = b
        d.add_paragraph("")
    d.add_heading("Revision", level=2)
    t = d.add_table(rows=3, cols=3)
    t.style = "Table Grid"
    for k, row in enumerate((("Issue", "Date", "Change"), ("1", "18 June 2026", "First issue for the 2027 plan."),
                             ("2", "30 July 2026", "B's costs updated to the supplier's quotation of 14 July 2026; "
                                                   "E's position on the operating floor confirmed."))):
        for c, v in enumerate(row):
            t.cell(k, c).text = v
    d.add_paragraph("")
    d.add_heading("Approval", level=2)
    t = d.add_table(rows=4, cols=3)
    t.style = "Table Grid"
    for k, row in enumerate((("", "Name and role", "Date"),
                             ("Prepared", "Alan Pope, Operating centre manager", "30 July 2026"),
                             ("Checked", "Helen Douglas, Operating centre safety and assurance manager", "30 July 2026"),
                             ("Approved", "Jake Bray, Head of operations, Wyvern", "30 July 2026"))):
        for c, v in enumerate(row):
            t.cell(k, c).text = v
    os.makedirs(os.path.dirname(path), exist_ok=True)
    d.save(path)
    PP.normalize_ooxml(path, "Alan Pope", "Helen Douglas", "2026-06-18T09:31:00Z", "2026-07-30T15:12:00Z",
                       title="Improvement catalogue 2027")
    finish_docx(path, revision=9, total_time=287, pages=2)


def field(run, code, shown):
    """A Word field (PAGE, NUMPAGES) in a run, with its last computed value as Word stores it."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    for kind, text in (("begin", None), (None, " %s " % code), ("separate", None), (None, shown), ("end", None)):
        if kind:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), kind)
        else:
            el = OxmlElement("w:instrText" if text.strip() == code else "w:t")
            el.set(qn("xml:space"), "preserve")
            el.text = text
        run._r.append(el)


def finish_docx(path, revision, total_time, pages):
    """What Word itself leaves in a saved document: the template's own extras gone (its thumbnail, the 2010 styles
    part, the bibliography stub), the statistics Word computes on save, one company, and the revision count."""
    import zipfile
    import docx
    drop = {"docProps/thumbnail.jpeg", "word/stylesWithEffects.xml", "customXml/item1.xml",
            "customXml/_rels/item1.xml.rels", "customXml/itemProps1.xml"}
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    doc = docx.Document(path)
    paras = [p.text for p in doc.paragraphs if p.text.strip()]
    for t in doc.tables:
        for row in t.rows:
            seen = set()
            for c in row.cells:
                if id(c._tc) not in seen and c.text.strip():
                    seen.add(id(c._tc))
                    paras.append(c.text)
    text = " ".join(paras)
    words = len(text.split())
    chars = len(re.sub(r"\s", "", text))
    chars_sp = len(text)
    lines = sum(max(1, -(-len(p) // 92)) for p in paras)
    out = []
    for name, data in items:
        if name in drop:
            continue
        if name == "[Content_Types].xml":
            data = re.sub(rb'<Override PartName="/(customXml/itemProps1\.xml|word/stylesWithEffects\.xml|'
                          rb'docProps/thumbnail\.jpeg)"[^>]*/>', b"", data)
            data = re.sub(rb'<Default Extension="jpeg"[^>]*/>', b"", data)
        elif name == "_rels/.rels":
            data = re.sub(rb'<Relationship [^>]*Target="docProps/thumbnail\.jpeg"/>', b"", data)
        elif name == "word/_rels/document.xml.rels":
            data = re.sub(rb'<Relationship [^>]*Target="(stylesWithEffects\.xml|\.\./customXml/item1\.xml)"/>', b"", data)
        elif name == "docProps/app.xml":
            data = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<Properties xmlns="http://schemas.'
                    'openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats'
                    '.org/officeDocument/2006/docPropsVTypes"><Template>Normal.dotm</Template><TotalTime>%d</TotalTime>'
                    '<Pages>%d</Pages><Words>%d</Words><Characters>%d</Characters><Application>Microsoft Office Word'
                    '</Application><DocSecurity>0</DocSecurity><Lines>%d</Lines><Paragraphs>%d</Paragraphs><ScaleCrop>'
                    'false</ScaleCrop><HeadingPairs><vt:vector size="2" baseType="variant"><vt:variant><vt:lpstr>Title'
                    '</vt:lpstr></vt:variant><vt:variant><vt:i4>1</vt:i4></vt:variant></vt:vector></HeadingPairs>'
                    '<TitlesOfParts><vt:vector size="1" baseType="lpstr"><vt:lpstr>Improvement catalogue 2027</vt:lpstr>'
                    '</vt:vector></TitlesOfParts><Company>Wyvern Route</Company><LinksUpToDate>false</LinksUpToDate>'
                    '<CharactersWithSpaces>%d</CharactersWithSpaces><SharedDoc>false</SharedDoc><HyperlinksChanged>'
                    'false</HyperlinksChanged><AppVersion>16.0000</AppVersion></Properties>'
                    % (total_time, pages, words, chars, lines, len(paras), chars_sp)).encode()
        elif name == "docProps/core.xml":
            data = data.replace(b"</cp:lastModifiedBy>", b"</cp:lastModifiedBy><cp:revision>%d</cp:revision>" % revision)
        out.append((name, data))
    with zipfile.ZipFile(path, "w") as z:
        for name, data in out:
            zi = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        assert not (set(names) & drop) and z.read("docProps/app.xml").count(b"<Company>") == 1
        for n in names:
            if n.endswith(".rels") or n == "[Content_Types].xml":
                body = z.read(n)
                assert b"thumbnail" not in body and b"stylesWithEffects" not in body and b"customXml" not in body, n
    docx.Document(path)


def build(target, paths):
    terms_of_reference(paths["tor"])
    catalogue(paths["catalogue"])
    workload_assessment(paths["workload"])
