"""Document writers: PDFs whose container carries the issuing office's own metadata and filing time, and
workbooks re-serialised so they read as saved from Excel by a person in that office.

The OOXML pass re-serialises the parts (reduce-house-fixes H25): strings go to a shared-strings part, the
extended properties are Excel's own, the core properties carry the office's author and save times, and
every zip entry carries the save time. The PDF pass swaps the writer's invariant date for the document's
filing instant and its comment-line signature for the issuing office's producer string, at equal byte
length, so no cross-reference offset moves.
"""
import re
import zipfile

import reportlab.rl_config as rl_config

rl_config.invariant = 1

from reportlab.lib import colors                                    # noqa: E402
from reportlab.lib.enums import TA_JUSTIFY                          # noqa: E402
from reportlab.lib.pagesizes import letter                          # noqa: E402
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet  # noqa: E402
from reportlab.lib.units import mm                                  # noqa: E402
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,  # noqa: E402
                                Spacer, Table, TableStyle, Image, KeepTogether)

INVARIANT_DATE = b"D:20000101000000"
SIGNATURES = ("ReportLab", "reportlab", "openpyxl", "Openpyxl", "matplotlib", "Matplotlib")

__all__ = ["styles", "table", "write_pdf", "finalise_xlsx", "Paragraph", "Spacer", "Image", "KeepTogether",
           "mm", "colors"]


def styles():
    ss = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("t", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=13, leading=16,
                                spaceAfter=6),
        "ref": ParagraphStyle("r", parent=ss["Normal"], fontName="Helvetica", fontSize=8.2, leading=11,
                              textColor=colors.HexColor("#3f3f3f")),
        "h": ParagraphStyle("h", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=9.8, leading=12.5,
                            spaceBefore=8, spaceAfter=3),
        "p": ParagraphStyle("p", parent=ss["Normal"], fontName="Helvetica", fontSize=9.1, leading=12.3,
                            spaceAfter=4.5, alignment=TA_JUSTIFY),
        "small": ParagraphStyle("sm", parent=ss["Normal"], fontName="Helvetica", fontSize=7.8, leading=10,
                                textColor=colors.HexColor("#444444"), spaceAfter=3),
    }


def table(data, widths, align=None, small=False, zebra=False, header=True):
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    cmds = [
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold" if header else "Helvetica"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold" if not header else "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.4 if small else 8.2),
        ("LEADING", (0, 0), (-1, -1), 9.4 if small else 10.4),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6 if header else 0, colors.HexColor("#444444") if header else colors.white),
        ("LINEBELOW", (0, -1), (-1, -1), 0.4, colors.HexColor("#888888")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.0),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
    ]
    if header:
        cmds.append(("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"))
    for col in (align or []):
        cmds.append(("ALIGN", (col, 1), (col, -1), "RIGHT"))
    if zebra:
        for r in range(2, len(data), 2):
            cmds.append(("BACKGROUND", (0, r), (-1, r), colors.HexColor("#f2f2f2")))
    t.setStyle(TableStyle(cmds))
    return t


class _Doc(BaseDocTemplate):
    def __init__(self, path, meta, running, footer, **kw):
        self._meta = meta
        self._running = running
        self._footer = footer
        BaseDocTemplate.__init__(self, path, pagesize=letter, leftMargin=21 * mm, rightMargin=19 * mm,
                                 topMargin=21 * mm, bottomMargin=18 * mm, **kw)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="f")
        self.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=self._furniture)])

    def _furniture(self, canv, doc):
        canv.saveState()
        canv.setFont("Helvetica", 7.2)
        canv.setFillColor(colors.HexColor("#555555"))
        canv.drawString(21 * mm, letter[1] - 12 * mm, self._running)
        canv.drawString(21 * mm, 11 * mm, self._footer)
        canv.drawRightString(letter[0] - 19 * mm, 11 * mm, "Page %d" % doc.page)
        canv.setStrokeColor(colors.HexColor("#999999"))
        canv.setLineWidth(0.4)
        canv.line(21 * mm, letter[1] - 14 * mm, letter[0] - 19 * mm, letter[1] - 14 * mm)
        canv.restoreState()

    def handle_documentBegin(self):
        BaseDocTemplate.handle_documentBegin(self)
        c = self.canv
        c.setTitle(self._meta["title"])
        c.setAuthor(self._meta["author"])
        c.setSubject(self._meta.get("subject", ""))
        c.setCreator(self._meta["creator"])
        c.setProducer(self._meta["producer"])


def write_pdf(path, meta, running, footer, flowables, stamp):
    """stamp: the document's filing instant, "YYYY-MM-DD HH:MM:SS"."""
    doc = _Doc(path, meta, running, footer)
    doc.build(list(flowables))
    _finalise_pdf(path, stamp, meta["producer"])


def _finalise_pdf(path, stamp, producer):
    b = open(path, "rb").read()
    n0 = len(b)
    want = ("D:%s" % re.sub(r"[^0-9]", "", stamp)).encode()
    assert len(want) == len(INVARIANT_DATE), "%s: stamp %r is not a full instant" % (path, stamp)
    b = b.replace(INVARIANT_DATE, want)
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


def _entry_time(instant):
    d, t = instant.split("T")
    return tuple(int(x) for x in d.split("-")) + tuple(int(x) for x in t.split(":"))


def _sub_inline(m, shared, order):
    txt = m.group(3)
    if txt not in shared:
        shared[txt] = len(order)
        order.append(txt)
    return b'<c r="%s"%s t="s"><v>%d</v></c>' % (m.group(1), m.group(2), shared[txt])


def finalise_xlsx(path, title, creator, modified_by, company, created, modified):
    """created and modified: instants "YYYY-MM-DDTHH:MM:SS" (UTC, as Excel stores them)."""
    assert "T" in created and "T" in modified
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        data = {n: z.read(n) for n in names}
    sheet_names = re.findall(rb'<sheet [^>]*name="([^"]*)"', data["xl/workbook.xml"])
    titles = "".join("<vt:lpstr>%s</vt:lpstr>" % _esc(s.decode()) for s in sheet_names)
    # any inline strings move into the shared-strings part
    pat = re.compile(rb'<c r="([A-Z]+\d+)"((?: s="\d+")?) t="inlineStr"[^>]*><is><t[^>]*>(.*?)</t></is></c>')
    if any(pat.search(data[n]) for n in names if n.startswith("xl/worksheets/sheet")):
        shared, order, total = {}, [], 0
        for n in [x for x in names if x.startswith("xl/worksheets/sheet")]:
            body, k = pat.subn(lambda m: _sub_inline(m, shared, order), data[n])
            data[n] = body
            total += k
        items = b"".join(b"<si><t xml:space=\"preserve\">" + s + b"</t></si>" for s in order)
        data["xl/sharedStrings.xml"] = (
            b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            b'<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="%d" '
            b'uniqueCount="%d">%s</sst>' % (total, len(order), items))
        rels = data["xl/_rels/workbook.xml.rels"].decode()
        if "sharedStrings" not in rels:
            nid = max(int(x) for x in re.findall(r'Id="rId(\d+)"', rels)) + 1
            rels = rels.replace("</Relationships>", '<Relationship Id="rId%d" Type="http://schemas.openxmlformats.'
                                'org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>'
                                '</Relationships>' % nid)
            data["xl/_rels/workbook.xml.rels"] = rels.encode()
        ct = data["[Content_Types].xml"].decode()
        if "sharedStrings" not in ct:
            ct = ct.replace("</Types>", '<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.'
                            'openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/></Types>')
            data["[Content_Types].xml"] = ct.encode()
    data["xl/workbook.xml"] = data["xl/workbook.xml"].replace(b"<workbookProtection/>", b"")
    data["docProps/app.xml"] = APP_XML.format(n=len(sheet_names), titles=titles, company=_esc(company)).encode()
    data["docProps/core.xml"] = CORE_XML.format(title=_esc(title), creator=_esc(creator),
                                                modified_by=_esc(modified_by), created=created,
                                                modified=modified).encode()
    first = ["[Content_Types].xml", "_rels/.rels", "xl/workbook.xml", "xl/_rels/workbook.xml.rels"]
    order_out = [n for n in first if n in data] + sorted(n for n in data if n.startswith("xl/worksheets/")) + \
        [n for n in ("xl/sharedStrings.xml", "xl/styles.xml", "xl/theme/theme1.xml", "docProps/core.xml",
                     "docProps/app.xml") if n in data]
    order_out += sorted(n for n in data if n not in order_out)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for n in order_out:
            zi = zipfile.ZipInfo(n, date_time=_entry_time(modified))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data[n])
    blob = b""
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            blob += z.read(n)
    for s in SIGNATURES:
        assert s.encode() not in blob, "%s: %s survived" % (path, s)
