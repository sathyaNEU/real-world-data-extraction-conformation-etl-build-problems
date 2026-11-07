"""task250: documents the way an office writes them.

A document's story becomes a Word document; LibreOffice Writer exports it to PDF, so Producer and Creator read
LibreOffice and Writer, the issuing organisation sits in Author only and the Subject is real. The export's dates,
/DocChecksum and file /ID are then set from the issue date and the content at equal length, so the cross-reference
table holds and two builds are byte-identical. Workbooks and Word files keep a lean package whose docProps name the
person who saved them and the application they used, with fixed member times."""
import datetime as dt
import hashlib
import io
import os
import re
import shutil
import subprocess
import tempfile
import zipfile

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor

FONT = "Liberation Sans"


def _run(par, text, size, bold=False, italic=False, color=None):
    r = par.add_run(text)
    r.font.name = FONT
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    if color:
        r.font.color.rgb = RGBColor.from_string(color)
    return r


def _rich(par, text, size, color=None):
    """**bold** spans inside a paragraph"""
    parts = re.split(r"(\*\*[^*]+\*\*)", text)
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            _run(par, part[2:-2], size, bold=True, color=color)
        else:
            _run(par, part, size, color=color)


def _cell_border(cell, edges=("bottom",), sz="6", color="666666"):
    tcpr = cell._tc.get_or_add_tcPr()
    b = OxmlElement("w:tcBorders")
    for e in edges:
        el = OxmlElement("w:" + e)
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), sz)
        el.set(qn("w:color"), color)
        b.append(el)
    tcpr.append(b)


def _shade(cell, fill):
    tcpr = cell._tc.get_or_add_tcPr()
    s = OxmlElement("w:shd")
    s.set(qn("w:val"), "clear")
    s.set(qn("w:color"), "auto")
    s.set(qn("w:fill"), fill)
    tcpr.append(s)


def _table(doc, rows, widths_mm, size=8.0, head=True, align=None):
    tab = doc.add_table(rows=len(rows), cols=len(rows[0]))
    tab.alignment = WD_TABLE_ALIGNMENT.LEFT
    tab.autofit = False
    tblpr = tab._tbl.tblPr
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    tblpr.append(lay)
    for j, gc in enumerate(tab._tbl.tblGrid.findall(qn("w:gridCol"))):
        gc.set(qn("w:w"), str(int(round(widths_mm[j] / 25.4 * 1440))))
    for j, col in enumerate(tab.columns):
        col.width = Mm(widths_mm[j])
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            cell = tab.cell(i, j)
            cell.width = Mm(widths_mm[j])
            par = cell.paragraphs[0]
            par.paragraph_format.space_after = Pt(1)
            par.paragraph_format.space_before = Pt(1)
            if align and align[j] == "r" and not (head and i == 0):
                par.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            _rich(par, str(v), size) if not (head and i == 0) else _run(par, str(v), size, bold=True)
            if head and i == 0:
                _cell_border(cell, ("bottom",), "8", "333333")
                _shade(cell, "EDEDED")
            else:
                _cell_border(cell, ("bottom",), "4", "BBBBBB")
    sp = doc.add_paragraph()
    sp.paragraph_format.space_after = Pt(2)


def _field(par, instr, size):
    r = par.add_run()
    for kind, txt in (("begin", None), (None, instr), ("end", None)):
        if kind:
            f = OxmlElement("w:fldChar")
            f.set(qn("w:fldCharType"), kind)
            r._r.append(f)
        else:
            it = OxmlElement("w:instrText")
            it.set(qn("xml:space"), "preserve")
            it.text = txt
            r._r.append(it)
    r.font.name = FONT
    r.font.size = Pt(size)


def build_docx(story, title, author, subject, header, footer, created, modified, last_by=None, margin_mm=20,
               base_size=9.5, keywords=""):
    """story: list of tuples ("title", text) ("h1", text) ("h2", text) ("p", text) ("small", text)
    ("table", rows, widths_mm[, align]) ("img", path, width_mm) ("break",) ("sig", [(name, role), ...])"""
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(margin_mm)
    sec.top_margin, sec.bottom_margin = Mm(22), Mm(18)
    sec.header_distance, sec.footer_distance = Mm(9), Mm(8)
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(base_size)
    for item in story:
        kind = item[0]
        if kind == "title":
            par = doc.add_paragraph()
            par.paragraph_format.space_after = Pt(4)
            _run(par, item[1], 15, bold=True, color="1F3A5F")
        elif kind == "subtitle":
            par = doc.add_paragraph()
            par.paragraph_format.space_after = Pt(8)
            _run(par, item[1], 10, color="444444")
        elif kind == "h1":
            par = doc.add_paragraph()
            par.paragraph_format.space_before = Pt(9)
            par.paragraph_format.space_after = Pt(3)
            par.paragraph_format.keep_with_next = True
            _run(par, item[1], 11.5, bold=True, color="1F3A5F")
        elif kind == "h2":
            par = doc.add_paragraph()
            par.paragraph_format.space_before = Pt(6)
            par.paragraph_format.space_after = Pt(2)
            par.paragraph_format.keep_with_next = True
            _run(par, item[1], 10, bold=True)
        elif kind == "p":
            par = doc.add_paragraph()
            par.paragraph_format.space_after = Pt(4)
            _rich(par, item[1], base_size)
        elif kind == "small":
            par = doc.add_paragraph()
            par.paragraph_format.space_after = Pt(3)
            _rich(par, item[1], base_size - 1.5, color="444444")
        elif kind == "table":
            _table(doc, item[1], item[2], size=base_size - 1.5, align=(item[3] if len(item) > 3 else None))
        elif kind == "img":
            par = doc.add_paragraph()
            par.add_run().add_picture(item[1], width=Mm(item[2]))
        elif kind == "break":
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        elif kind == "sig":
            rows = [["" for _ in item[1]], [n for n, _ in item[1]], [r for _, r in item[1]]]
            tab = doc.add_table(rows=3, cols=len(item[1]))
            for j in range(len(item[1])):
                c0 = tab.cell(0, j)
                c0.paragraphs[0].add_run(" ")
                _cell_border(c0, ("bottom",), "6", "333333")
                _run(tab.cell(1, j).paragraphs[0], rows[1][j], base_size - 1)
                _run(tab.cell(2, j).paragraphs[0], rows[2][j], base_size - 2, color="555555")
            doc.add_paragraph()
    hp = sec.header.paragraphs[0]
    _run(hp, header, 7.5, color="555555")
    fp = sec.footer.paragraphs[0]
    _run(fp, footer + "    Página ", 7, color="555555")
    _field(fp, "PAGE", 7)
    _run(fp, " de ", 7, color="555555")
    _field(fp, "NUMPAGES", 7)
    cp = doc.core_properties
    cp.title, cp.author, cp.subject = title, author, subject
    cp.keywords = keywords
    cp.comments = ""
    cp.last_modified_by = last_by or author
    cp.created = created.astimezone(dt.timezone.utc).replace(tzinfo=None)
    cp.modified = modified.astimezone(dt.timezone.utc).replace(tzinfo=None)
    cp.revision = 3
    return doc


def export_pdf(doc, path, created, modified):
    work = tempfile.mkdtemp(prefix="officedoc-")
    try:
        src = os.path.join(work, "document.docx")
        doc.save(src)
        prof = "file://" + os.path.join(work, "profile")
        subprocess.run(["soffice", "-env:UserInstallation=" + prof, "--headless", "--convert-to",
                        "pdf:writer_pdf_Export", "--outdir", work, src],
                       check=True, capture_output=True, timeout=240, env=dict(os.environ, TZ="UTC"))
        b = open(os.path.join(work, "document.pdf"), "rb").read()
    finally:
        shutil.rmtree(work, ignore_errors=True)
    b = _fix_pdf(b, created, modified)
    with open(path, "wb") as fh:
        fh.write(b)


def _fix_pdf(b, created, modified):
    n = len(b)
    m = re.search(rb"/CreationDate\((D:[^)]*)\)", b)
    if m:
        new = created.astimezone(dt.timezone.utc).strftime("D:%Y%m%d%H%M%SZ'").encode()
        assert len(new) == len(m.group(1)), (new, m.group(1))
        b = b[:m.start(1)] + new + b[m.end(1):]
    m = re.search(rb"/ModDate\((D:[^)]*)\)", b)
    if m:
        new = modified.astimezone(dt.timezone.utc).strftime("D:%Y%m%d%H%M%SZ'").encode()
        if len(new) == len(m.group(1)):
            b = b[:m.start(1)] + new + b[m.end(1):]
    core = re.sub(rb"/ID\s*\[[^\]]*\]", b"", re.sub(rb"/DocChecksum\s*/[0-9A-Fa-f]+", b"", b))
    digest = hashlib.sha256(core).hexdigest().upper().encode()
    b = re.sub(rb"(/DocChecksum\s*/)([0-9A-Fa-f]+)", lambda mm: mm.group(1) + digest[-len(mm.group(2)):], b)

    def repl(mm):
        out = bytearray(mm.group(0))
        for g in (1, 2):
            a, z = mm.start(g) - mm.start(0), mm.end(g) - mm.start(0)
            out[a:z] = digest[:z - a]
        return bytes(out)
    b = re.sub(rb"/ID\s*\[\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*\]", repl, b)
    assert len(b) == n, "PDF length changed"
    return b


# ------------------------------------------------------------------ OOXML packages

def _iso(d):
    return d.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def core_xml(title, subject, creator, last_by, created, modified, keywords=""):
    esc = lambda s: (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<dc:title>%s</dc:title><dc:subject>%s</dc:subject><dc:creator>%s</dc:creator><cp:keywords>%s</cp:keywords>'
            '<cp:lastModifiedBy>%s</cp:lastModifiedBy>'
            '<dcterms:created xsi:type="dcterms:W3CDTF">%s</dcterms:created>'
            '<dcterms:modified xsi:type="dcterms:W3CDTF">%s</dcterms:modified></cp:coreProperties>'
            % (esc(title), esc(subject), esc(creator), esc(keywords), esc(last_by), _iso(created), _iso(modified))).encode()


def app_xml_excel(sheets, company):
    parts = "".join("<vt:lpstr>%s</vt:lpstr>" % s for s in sheets)
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
            'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
            '<Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>'
            '<HeadingPairs><vt:vector size="2" baseType="variant"><vt:variant><vt:lpstr>Worksheets</vt:lpstr>'
            '</vt:variant><vt:variant><vt:i4>%d</vt:i4></vt:variant></vt:vector></HeadingPairs>'
            '<TitlesOfParts><vt:vector size="%d" baseType="lpstr">%s</vt:vector></TitlesOfParts>'
            '<Company>%s</Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
            '<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>'
            % (len(sheets), len(sheets), parts, company)).encode()


def app_xml_word(pages, words, chars, company, paragraphs, lines):
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
            'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
            '<Template>Normal.dotm</Template><TotalTime>94</TotalTime><Pages>%d</Pages><Words>%d</Words>'
            '<Characters>%d</Characters><Application>Microsoft Office Word</Application><DocSecurity>0</DocSecurity>'
            '<Lines>%d</Lines><Paragraphs>%d</Paragraphs><ScaleCrop>false</ScaleCrop><Company>%s</Company>'
            '<LinksUpToDate>false</LinksUpToDate><CharactersWithSpaces>%d</CharactersWithSpaces>'
            '<SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0000</AppVersion>'
            '</Properties>' % (pages, words, chars, lines, paragraphs, company, chars + words)).encode()


_DROP_DOCX = ("docProps/thumbnail.jpeg", "customXml/", "word/stylesWithEffects.xml")


def repack(path, core, app, stamp, drop=()):
    """Rewrite an OOXML package: docProps replaced, the writer library's extra parts dropped, every member written
    with the save's time so two builds are byte-identical."""
    with zipfile.ZipFile(path) as zin:
        items = [(i.filename, zin.read(i.filename)) for i in zin.infolist()]
    keep = []
    for name, data in items:
        if any(name == d or (d.endswith("/") and name.startswith(d)) for d in drop):
            continue
        if name == "docProps/core.xml":
            data = core
        elif name == "docProps/app.xml":
            data = app
        elif name == "[Content_Types].xml":
            data = re.sub(rb'<Override PartName="/docProps/thumbnail.jpeg"[^>]*/>', b"", data)
            data = re.sub(rb'<Override PartName="/customXml/[^"]*"[^>]*/>', b"", data)
            data = re.sub(rb'<Override PartName="/word/stylesWithEffects.xml"[^>]*/>', b"", data)
            data = re.sub(rb'<Default Extension="jpeg"[^>]*/>', b"", data) if b"jpeg" not in b"".join(
                n.encode() for n, _ in items if not n.startswith("docProps/thumbnail")) else data
        elif name == "_rels/.rels":
            data = re.sub(rb'<Relationship [^>]*Target="docProps/thumbnail.jpeg"[^>]*/>', b"", data)
        elif name == "word/_rels/document.xml.rels":
            data = re.sub(rb'<Relationship [^>]*Target="\.\./customXml/[^"]*"[^>]*/>', b"", data)
            data = re.sub(rb'<Relationship [^>]*Target="stylesWithEffects.xml"[^>]*/>', b"", data)
        keep.append((name, data))
    t = (stamp.year, stamp.month, stamp.day, stamp.hour, stamp.minute, stamp.second)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in keep:
            zi = zipfile.ZipInfo(name, date_time=t)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            zout.writestr(zi, data)
    with open(path, "wb") as fh:
        fh.write(buf.getvalue())


def docx_counts(doc):
    words = 0
    chars = 0
    paras = 0
    for p in doc.paragraphs:
        t = p.text.strip()
        if t:
            paras += 1
            words += len(t.split())
            chars += len(t.replace(" ", ""))
    for tab in doc.tables:
        for row in tab.rows:
            for c in row.cells:
                t = c.text.strip()
                if t:
                    words += len(t.split())
                    chars += len(t.replace(" ", ""))
    return words, chars, paras
