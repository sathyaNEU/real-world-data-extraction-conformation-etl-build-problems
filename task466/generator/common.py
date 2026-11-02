"""Shared helpers for task466: deterministic writers (csv, xlsx, pdf), time zones and paths."""
import datetime as dt
import io
import os
import zipfile
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
REPO = os.path.dirname(TASK)
TZ = ZoneInfo("America/Chicago")
UTC = dt.timezone.utc
FIXED_ZIP_TIME = (2027, 1, 14, 9, 0, 0)
AS_OF = "2027-01-15"


def utc(y, m, d, h=0, mi=0):
    return dt.datetime(y, m, d, h, mi, tzinfo=UTC)


def local(t):
    return t.astimezone(TZ)


def normalise_zip(path, when=FIXED_ZIP_TIME, stamp=None):
    """Rewrite an OOXML zip with fixed entry times (and fixed core-property dates) so builds are byte-identical."""
    import re
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    if stamp:
        fixed = []
        for name, data in items:
            if name == "docProps/core.xml":
                s = data.decode("utf-8")
                s = re.sub(r"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", r"\g<1>%s\g<2>" % stamp, s)
                s = re.sub(r"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", r"\g<1>%s\g<2>" % stamp, s)
                data = s.encode("utf-8")
            fixed.append((name, data))
        items = fixed
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in items:
            zi = zipfile.ZipInfo(name, date_time=when)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)
    with open(path, "wb") as f:
        f.write(buf.getvalue())


def save_workbook(wb, path, created, creator):
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.created = created
    wb.properties.modified = created
    wb.properties.title = None
    wb.save(path)
    normalise_zip(path, stamp=created.strftime("%Y-%m-%dT%H:%M:%SZ"))


def pdf_canvas_settings():
    from reportlab import rl_config
    rl_config.invariant = 1
    rl_config.pageCompression = 1


def write_csv(path, header, rows, sep=",", preamble=None):
    import csv
    with open(path, "w", encoding="utf-8", newline="") as f:
        if preamble:
            for line in preamble:
                f.write(line + "\r\n")
        w = csv.writer(f, delimiter=sep, lineterminator="\r\n", quoting=csv.QUOTE_MINIMAL)
        w.writerow(header)
        for r in rows:
            w.writerow(["" if v is None else str(v) for v in r])


def text_pdf(path, title, blocks, width_chars=104, author=""):
    """A plain text PDF: blocks are (text, style, size); style 'B' bold, '' regular, 'T' a table row (monospace)."""
    import textwrap
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(path, pagesize=letter, invariant=1)
    c.setTitle(title)
    c.setAuthor(author)
    c.setCreator("")
    top = 262 * mm
    y = top
    for text, style, size in blocks:
        if style == "PAGE":
            c.showPage()
            y = top
            continue
        if not text:
            y -= 3 * mm
            continue
        if style == "T":
            c.setFont("Courier", size)
            lines = [text]
        else:
            c.setFont("Helvetica-Bold" if style == "B" else "Helvetica", size)
            lines = textwrap.wrap(text, width_chars if size <= 9 else int(width_chars * 0.86))
        from reportlab.pdfbase.pdfmetrics import stringWidth
        font = "Courier" if style == "T" else ("Helvetica-Bold" if style == "B" else "Helvetica")
        for ln in lines:
            # nothing may run past the right margin (a clipped cell reads as generated)
            assert 17 * mm + stringWidth(ln, font, size) <= letter[0] - 12 * mm, (path, ln)
            if y < 18 * mm:
                c.showPage()
                y = top
                c.setFont("Courier" if style == "T" else ("Helvetica-Bold" if style == "B" else "Helvetica"), size)
            c.drawString(17 * mm, y, ln)
            y -= (3.9 if style == "T" else 4.5) * mm
    c.showPage()
    c.save()
