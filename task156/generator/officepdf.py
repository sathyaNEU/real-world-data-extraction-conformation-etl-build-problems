"""task127: the issuing office's PDF, written the way an office writes it. A document's story (paragraphs,
spacers, tables and page breaks) becomes a Word document, LibreOffice Writer exports it to PDF, and the PDF's
dates and file identifier are set to the issue date at equal length, so the cross-reference table holds and two
builds are byte-identical. Producer and Creator stay as Writer wrote them."""
import datetime as dt
import hashlib
import html
import os
import re
import shutil
import subprocess
import tempfile

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor
from reportlab.platypus import PageBreak, Paragraph, Spacer, Table

FONT = "Liberation Sans"


def _text(p):
    t = getattr(p, "text", None)
    if t is None:
        t = "".join(getattr(f, "text", "") for f in getattr(p, "frags", []))
    return t


def _add_runs(par, markup, size, bold, color, italic=False):
    parts = re.split(r"(<b>|</b>|<br\s*/?>)", markup)
    on = bold
    for part in parts:
        if part == "<b>":
            on = True
            continue
        if part == "</b>":
            on = bold
            continue
        if re.fullmatch(r"<br\s*/?>", part or ""):
            par.add_run().add_break()
            continue
        if not part:
            continue
        r = par.add_run(html.unescape(re.sub(r"<[^>]+>", "", part)))
        r.font.name = FONT
        r.font.size = Pt(size)
        r.font.bold = on
        r.font.italic = italic
        if color:
            r.font.color.rgb = RGBColor.from_string(color)


def _style_of(st):
    color = None
    tc = getattr(st, "textColor", None)
    if tc is not None and hasattr(tc, "hexval"):
        hv = tc.hexval()[2:].upper()
        color = None if hv in ("000000",) else hv
    return st.fontSize, "Bold" in st.fontName, color, getattr(st, "spaceBefore", 0), getattr(st, "spaceAfter", 0)


ALIGN = {0: WD_ALIGN_PARAGRAPH.LEFT, 1: WD_ALIGN_PARAGRAPH.CENTER, 2: WD_ALIGN_PARAGRAPH.RIGHT,
         4: WD_ALIGN_PARAGRAPH.JUSTIFY}


def _paragraph(doc, p):
    size, bold, color, before, after = _style_of(p.style)
    par = doc.add_paragraph()
    par.paragraph_format.space_before = Pt(before)
    par.paragraph_format.space_after = Pt(after)
    par.alignment = ALIGN.get(getattr(p.style, "alignment", 0), WD_ALIGN_PARAGRAPH.LEFT)
    _add_runs(par, _text(p), size, bold, color, italic="Oblique" in p.style.fontName or "Italic" in p.style.fontName)


def _border_below(cell):
    tcpr = cell._tc.get_or_add_tcPr()
    b = OxmlElement("w:tcBorders")
    e = OxmlElement("w:bottom")
    e.set(qn("w:val"), "single")
    e.set(qn("w:sz"), "6")
    e.set(qn("w:color"), "333333")
    b.append(e)
    tcpr.append(b)


def _table(doc, t):
    rows = t._cellvalues
    widths = list(getattr(t, "_colWidths", []) or [])
    tab = doc.add_table(rows=len(rows), cols=len(rows[0]))
    tab.autofit = False
    tblpr = tab._tbl.tblPr
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    tblpr.append(lay)
    mm = [w / 72.0 * 25.4 for w in widths]
    for j, gc in enumerate(tab._tbl.tblGrid.findall(qn("w:gridCol"))):
        if j < len(mm):
            gc.set(qn("w:w"), str(int(round(mm[j] / 25.4 * 1440))))
    for j, col in enumerate(tab.columns):
        if j < len(mm):
            col.width = Mm(mm[j])
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            cell = tab.cell(i, j)
            if j < len(widths) and widths[j]:
                cell.width = Mm(widths[j] / 72.0 * 25.4)
            par = cell.paragraphs[0]
            par.paragraph_format.space_after = Pt(0)
            if isinstance(v, Paragraph):
                size, bold, color, _, _ = _style_of(v.style)
                _add_runs(par, _text(v), size, bold, color)
            else:
                _add_runs(par, html.escape(str(v)), 8.0, i == 0, None)
            if i == 0:
                _border_below(cell)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def _page_field(par):
    r = par.add_run()
    for kind, txt in (("begin", None), (None, "PAGE"), ("end", None)):
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
    r.font.size = Pt(7)


def build(path, story, title, author, subject, footer, created, modified, margin_mm=18, top_mm=17, bottom_mm=17,
          producer=None):
    """producer: the LibreOffice release the issuing office ran at the document's date (default: the one installed)."""
    """created and modified: aware datetimes, the document's in-fiction issue and last-saved times."""
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(margin_mm)
    sec.top_margin, sec.bottom_margin = Mm(top_mm), Mm(bottom_mm)
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(9.2)
    first = True
    for fl in story:
        if isinstance(fl, Paragraph):
            _paragraph(doc, fl)
        elif isinstance(fl, Table):
            _table(doc, fl)
        elif isinstance(fl, Spacer):
            sp = doc.add_paragraph()
            sp.paragraph_format.space_after = Pt(0)
            sp.paragraph_format.line_spacing = Pt(max(1, fl.height))
        elif isinstance(fl, PageBreak):
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        first = False
    fp = sec.footer.paragraphs[0]
    r = fp.add_run(footer + "\tPage ")
    r.font.name = FONT
    r.font.size = Pt(7)
    r.font.color.rgb = RGBColor.from_string("555555")
    _page_field(fp)
    cp = doc.core_properties
    cp.title, cp.author, cp.subject = title, author, subject
    cp.last_modified_by = author
    cp.created = created.astimezone(dt.timezone.utc).replace(tzinfo=None)
    cp.modified = modified.astimezone(dt.timezone.utc).replace(tzinfo=None)
    cp.revision = 1
    work = tempfile.mkdtemp(prefix="officepdf-")
    try:
        src = os.path.join(work, "document.docx")
        doc.save(src)
        prof = "file://" + os.path.join(work, "profile")
        subprocess.run(["soffice", "-env:UserInstallation=" + prof, "--headless", "--convert-to",
                        "pdf:writer_pdf_Export", "--outdir", work, src],
                       check=True, capture_output=True, timeout=180, env=dict(os.environ, TZ="UTC"))
        b = open(os.path.join(work, "document.pdf"), "rb").read()
    finally:
        shutil.rmtree(work, ignore_errors=True)
    if producer:
        b = _producer(b, producer)
    b = _fix(b, created, modified)
    open(path, "wb").write(b)


def _pdfdate(d):
    off = d.utcoffset() or dt.timedelta(0)
    sign = "+" if off >= dt.timedelta(0) else "-"
    mins = abs(int(off.total_seconds())) // 60
    return ("D:%s%s%02d'%02d'" % (d.strftime("%Y%m%d%H%M%S"), sign, mins // 60, mins % 60)).encode()


def _producer(b, name):
    """Set the info dictionary's Producer to the release the office ran, as Writer writes it (UTF-16 hex). The info
    dictionary is the last object before the cross-reference table, so only startxref moves; every object offset
    in the table is asserted to sit before the change."""
    m = re.search(rb"/Producer<(FEFF[0-9A-F]*)>", b)
    assert m, "no Producer in the export"
    new = ("FEFF" + "".join("%04X" % ord(ch) for ch in name)).encode()
    delta = len(new) - len(m.group(1))
    x = b.rfind(b"\nxref\n")
    assert m.end() < x
    offs = [int(o) for o in re.findall(rb"^(\d{10}) \d{5} n", b[x:], re.M)]
    assert max(offs) < m.start(1), "an object after the info dictionary"
    b = b[:m.start(1)] + new + b[m.end(1):]
    s = re.search(rb"startxref\n(\d+)\n%%EOF", b)
    old = int(s.group(1))
    assert old == x + 1, (old, x)
    b = b[:s.start(1)] + str(old + delta).encode() + b[s.end(1):]
    return b


def _fix(b, created, modified):
    """Writer stamps the export clock as D:YYYYMMDDHHMMSSZ' and adds a random /DocChecksum and file /ID; each is
    set from the issue date and the content, at equal length."""
    n = len(b)
    m = re.search(rb"/CreationDate\((D:[^)]*)\)", b)
    if m:
        new = created.astimezone(dt.timezone.utc).strftime("D:%Y%m%d%H%M%SZ'").encode()
        assert len(new) == len(m.group(1)), (new, m.group(1))
        b = b[:m.start(1)] + new + b[m.end(1):]
    core = re.sub(rb"/ID\s*\[[^\]]*\]", b"", re.sub(rb"/DocChecksum\s*/[0-9A-Fa-f]+", b"", b))
    digest = hashlib.sha256(core).hexdigest().upper().encode()
    b = re.sub(rb"(/DocChecksum\s*/)([0-9A-Fa-f]+)", lambda m: m.group(1) + digest[-len(m.group(2)):], b)

    def repl(m):
        out = bytearray(m.group(0))
        for g in (1, 2):
            a, z = m.start(g) - m.start(0), m.end(g) - m.start(0)
            out[a:z] = digest[:z - a]
        return bytes(out)
    b = re.sub(rb"/ID\s*\[\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*\]", repl, b)
    assert len(b) == n, "PDF length changed"
    return b
