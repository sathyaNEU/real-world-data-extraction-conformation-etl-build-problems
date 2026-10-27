#!/usr/bin/env python3
"""Document writers for task204: workbooks that look like a person saved them, and PDFs whose
container metadata matches the body that issued them.

Three bodies issue documents in this pack (the Education and Training Board, the Department of
Education and two private practices), so there is no single producer string: each document carries its
own, asserted per document in checks.py and verify.py.

The OOXML pass re-serialises the parts rather than patching bytes in a structured container
(reduce-house-fixes H25): inline strings move into a shared-strings part, a calculation chain is
written where the sheet carries formulas, the empty protection element openpyxl leaves behind is
dropped, and the extended properties are Excel's own. Every value is read back with openpyxl and
asserted unchanged.
"""
import datetime as dt
import re
import zipfile

import reportlab.rl_config as rl_config

rl_config.invariant = 1

from reportlab.lib import colors                                    # noqa: E402
from reportlab.lib.enums import TA_JUSTIFY                          # noqa: E402
from reportlab.lib.pagesizes import A4                              # noqa: E402
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet  # noqa: E402
from reportlab.lib.units import mm                                  # noqa: E402
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,  # noqa: E402
                               Spacer, Table, TableStyle)

INVARIANT_DATE = b"D:20000101000000"
SIGNATURES = ("ReportLab", "reportlab", "openpyxl", "Openpyxl")


# ----------------------------------------------------------------- PDF

def styles(body_font="Helvetica"):
    ss = getSampleStyleSheet()
    out = {
        "title": ParagraphStyle("t", parent=ss["Normal"], fontName=body_font + "-Bold",
                                fontSize=13.5, leading=16.5, spaceAfter=7),
        "ref": ParagraphStyle("r", parent=ss["Normal"], fontName=body_font, fontSize=8.2,
                              leading=11, textColor=colors.HexColor("#3f3f3f")),
        "h": ParagraphStyle("h", parent=ss["Normal"], fontName=body_font + "-Bold",
                            fontSize=10, leading=13, spaceBefore=9, spaceAfter=3),
        "p": ParagraphStyle("p", parent=ss["Normal"], fontName=body_font, fontSize=9.3,
                            leading=12.6, spaceAfter=5, alignment=TA_JUSTIFY),
        "src": ParagraphStyle("s", parent=ss["Normal"], fontName=body_font + "-Oblique",
                              fontSize=7.6, leading=9.6, textColor=colors.HexColor("#555555"),
                              spaceBefore=2, spaceAfter=8),
    }
    return out


def table(data, widths, align=None, small=False):
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    cmds = [
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.4 if small else 8.1),
        ("LEADING", (0, 0), (-1, -1), 9.6 if small else 10.4),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#444444")),
        ("LINEBELOW", (0, -1), (-1, -1), 0.4, colors.HexColor("#888888")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
    ]
    for col in (align or []):
        cmds.append(("ALIGN", (col, 1), (col, -1), "RIGHT"))
    t.setStyle(TableStyle(cmds))
    return t


class _Doc(BaseDocTemplate):
    def __init__(self, path, meta, running, **kw):
        self._meta = meta
        self._running = running
        BaseDocTemplate.__init__(self, path, pagesize=A4, leftMargin=22 * mm, rightMargin=20 * mm,
                                 topMargin=20 * mm, bottomMargin=18 * mm, **kw)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="f")
        self.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=self._furniture)])

    def _furniture(self, canv, doc):
        canv.saveState()
        canv.setFont("Helvetica", 7.2)
        canv.setFillColor(colors.HexColor("#555555"))
        canv.drawString(22 * mm, A4[1] - 12 * mm, self._running)
        canv.drawRightString(A4[0] - 20 * mm, 11 * mm, "Page %d" % doc.page)
        canv.setStrokeColor(colors.HexColor("#999999"))
        canv.setLineWidth(0.4)
        canv.line(22 * mm, A4[1] - 14 * mm, A4[0] - 20 * mm, A4[1] - 14 * mm)
        canv.restoreState()

    def handle_documentBegin(self):
        BaseDocTemplate.handle_documentBegin(self)
        c = self.canv
        c.setTitle(self._meta["title"])
        c.setAuthor(self._meta["author"])
        c.setSubject(self._meta["subject"])
        c.setCreator(self._meta["creator"])
        c.setProducer(self._meta["producer"])


def write_pdf(path, meta, running, flowables, stamp):
    """Write a PDF and give it the issuing body's own container metadata and file date.

    stamp is the document's own filing instant, "YYYY-MM-DD HH:MM:SS". Four issuing bodies file four
    documents at four different times of day; a set of creation dates all reading midnight to the
    second is a tell, and checks.py asserts the four differ.
    """
    doc = _Doc(path, meta, running)
    doc.build(list(flowables))
    _finalise_pdf(path, stamp, meta["producer"])


def _finalise_pdf(path, stamp, producer):
    b = open(path, "rb").read()
    n0 = len(b)
    want = ("D:%s" % re.sub(r"[^0-9]", "", stamp)).encode()
    assert len(want) == len(INVARIANT_DATE), "%s: stamp %r is not a full instant" % (path, stamp)
    assert len(want) == len(INVARIANT_DATE)
    b = b.replace(INVARIANT_DATE, want)
    # the writer's own comment lines: substitute the text after the comment marker, equal length,
    # so no cross-reference offset moves (reduce-house-fixes H1)
    out = []
    for line in b.split(b"\n"):
        if any(s.encode() in line for s in SIGNATURES):
            m = re.match(rb"(\s*%+[\x80-\xff ]*)(.*)$", line, re.S)
            if m:
                body = producer.encode().ljust(len(m.group(2)))[:len(m.group(2))]
                line = m.group(1) + body
        out.append(line)
    b = b"\n".join(out)
    assert len(b) == n0, "%s: byte length moved" % path
    for s in SIGNATURES:
        assert s.encode() not in b, "%s: %s survived" % (path, s)
    open(path, "wb").write(b)


# ----------------------------------------------------------------- XLSX

APP_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" \
xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">\
<Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>\
<HeadingPairs><vt:vector size="2" baseType="variant"><vt:variant><vt:lpstr>Worksheets</vt:lpstr>\
</vt:variant><vt:variant><vt:i4>{n}</vt:i4></vt:variant></vt:vector></HeadingPairs>\
<TitlesOfParts><vt:vector size="{n}" baseType="lpstr">{titles}</vt:vector></TitlesOfParts>\
<Company>{company}</Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>\
<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>"""

CORE_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" \
xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" \
xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\
<dc:title>{title}</dc:title><dc:creator>{creator}</dc:creator>\
<cp:lastModifiedBy>{modified_by}</cp:lastModifiedBy>\
<dcterms:created xsi:type="dcterms:W3CDTF">{created}Z</dcterms:created>\
<dcterms:modified xsi:type="dcterms:W3CDTF">{modified}Z</dcterms:modified>\
</cp:coreProperties>"""

_XML_ESC = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}


def _esc(s):
    for k, v in _XML_ESC.items():
        s = s.replace(k, v)
    return s


def finalise_xlsx(path, title, creator, modified_by, company, created, modified):
    """Re-serialise the workbook's parts so the file reads as one Excel saved.

    created and modified are full instants, "YYYY-MM-DDTHH:MM:SS". Each workbook in the pack has its
    own pair, because four workbooks from four offices sharing one clock time to the second is the
    tell that says one hand wrote them all; checks.py asserts the pairs differ.
    """
    assert "T" in created and "T" in modified, "%s: workbook stamps are not instants" % path
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        data = {n: z.read(n) for n in names}

    sheet_names = re.findall(rb'<sheet [^>]*name="([^"]*)"', data["xl/workbook.xml"])
    titles = "".join("<vt:lpstr>%s</vt:lpstr>" % _esc(s.decode()) for s in sheet_names)

    # inline strings move into a shared-strings part
    shared, order = {}, []
    pat = re.compile(rb'<c r="([A-Z]+\d+)"((?: s="\d+")?) t="inlineStr"[^>]*><is><t[^>]*>(.*?)</t></is></c>')
    total = 0
    for n in [x for x in names if x.startswith("xl/worksheets/sheet")]:
        body, k = pat.subn(lambda m: _sub_shim(m, shared, order), data[n])
        data[n] = body
        total += k
    if order:
        items = b"".join(b"<si><t xml:space=\"preserve\">" + s + b"</t></si>" for s in order)
        data["xl/sharedStrings.xml"] = (
            b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            b'<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="%d" '
            b'uniqueCount="%d">%s</sst>' % (total, len(order), items))

    # a calculation chain where the sheets carry formulas, as Excel writes one
    cells = []
    for si, n in enumerate([x for x in names if x.startswith("xl/worksheets/sheet")], start=1):
        for m in re.finditer(rb'<c r="([A-Z]+\d+)"[^>]*><f>', data[n]):
            cells.append((m.group(1).decode(), si))
    if cells:
        body = "".join('<c r="%s" i="%d"/>' % (r, s) for r, s in cells)
        data["xl/calcChain.xml"] = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<calcChain xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">%s'
            '</calcChain>' % body).encode()

    data["xl/workbook.xml"] = data["xl/workbook.xml"].replace(b"<workbookProtection/>", b"")
    data["docProps/app.xml"] = APP_XML.format(n=len(sheet_names), titles=titles,
                                              company=_esc(company)).encode()
    data["docProps/core.xml"] = CORE_XML.format(
        title=_esc(title), creator=_esc(creator), modified_by=_esc(modified_by),
        created=created, modified=modified).encode()

    rels = data["xl/_rels/workbook.xml.rels"].decode()
    nid = max(int(x) for x in re.findall(r'Id="rId(\d+)"', rels)) + 1
    add = ""
    if "xl/sharedStrings.xml" in data:
        add += ('<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/'
                '2006/relationships/sharedStrings" Target="sharedStrings.xml"/>' % nid)
        nid += 1
    if "xl/calcChain.xml" in data:
        add += ('<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/'
                '2006/relationships/calcChain" Target="calcChain.xml"/>' % nid)
    data["xl/_rels/workbook.xml.rels"] = rels.replace("</Relationships>", add + "</Relationships>").encode()

    ct = data["[Content_Types].xml"].decode()
    extra = ""
    if "xl/sharedStrings.xml" in data:
        extra += ('<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.'
                  'openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>')
    if "xl/calcChain.xml" in data:
        extra += ('<Override PartName="/xl/calcChain.xml" ContentType="application/vnd.'
                  'openxmlformats-officedocument.spreadsheetml.calcChain+xml"/>')
    data["[Content_Types].xml"] = ct.replace("</Types>", extra + "</Types>").encode()

    order_out = [n for n in ("[Content_Types].xml", "_rels/.rels", "xl/workbook.xml",
                             "xl/_rels/workbook.xml.rels")] + \
                [n for n in names if n.startswith("xl/worksheets/")] + \
                [n for n in ("xl/sharedStrings.xml", "xl/calcChain.xml", "xl/styles.xml",
                             "xl/theme/theme1.xml", "docProps/core.xml", "docProps/app.xml")]
    order_out += [n for n in data if n not in order_out]
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for n in order_out:
            if n not in data:
                continue
            zi = zipfile.ZipInfo(n, date_time=_entry_time(modified))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data[n])

    import openpyxl
    wb = openpyxl.load_workbook(path)
    assert [ws.title for ws in wb.worksheets] == [s.decode() for s in sheet_names]
    blob = b""
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if n.startswith("docProps/"):
                blob += z.read(n)
    for s in SIGNATURES:
        assert s.encode() not in blob, "%s: %s survived in docProps" % (path, s)
    return wb


def _entry_time(instant):
    d, t = instant.split("T")
    return tuple(int(x) for x in d.split("-")) + tuple(int(x) for x in t.split(":"))


def _sub_shim(m, shared, order):
    txt = m.group(3)
    if txt not in shared:
        shared[txt] = len(order)
        order.append(txt)
    return b'<c r="%s"%s t="s"><v>%d</v></c>' % (m.group(1), m.group(2), shared[txt])
