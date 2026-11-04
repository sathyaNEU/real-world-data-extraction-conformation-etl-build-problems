"""Writers for the pack's workbooks and PDFs with fixed, organisation-side document properties (no toolchain
signature, no build time), so two builds are byte-identical."""
import datetime as dt
import io, re, zipfile
from openpyxl import Workbook
from openpyxl.styles import Font
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

STAMP = dt.datetime(2026, 9, 25, 14, 12, 0)
ZIPTIME = (2026, 9, 25, 14, 12, 0)


def xlsx(path, sheets, author="Nordvig Marine A/S", stamp=STAMP, created=None):
    """sheets: list of (title, rows, widths); the first row of each sheet is its header."""
    wb = Workbook()
    wb.remove(wb.active)
    for title, rows, widths in sheets:
        ws = wb.create_sheet(title)
        for r in rows:
            ws.append(r)
        if rows:
            for c in ws[1]:
                c.font = Font(bold=True)
        for i, col in enumerate(ws.columns):
            w = (widths[i] if widths and i < len(widths) else
                 min(46, max(9, max(len(str(c.value)) if c.value is not None else 0 for c in col) + 2)))
            ws.column_dimensions[col[0].column_letter].width = w
        ws.freeze_panes = "A2"
    p = wb.properties
    p.creator = author; p.lastModifiedBy = author; p.created = created or stamp; p.modified = stamp
    p.title = None; p.description = None; p.keywords = None
    buf = io.BytesIO()
    wb.save(buf)
    # rewrite the container with fixed entry times so the bytes do not depend on the build clock
    src = zipfile.ZipFile(io.BytesIO(buf.getvalue()))
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for info in src.infolist():
            data = src.read(info.filename)
            if info.filename == "docProps/core.xml":
                data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(<)", rb"\g<1>" + stamp.strftime("%Y-%m-%dT%H:%M:%SZ").encode() + rb"\g<2>", data)
            if info.filename == "docProps/app.xml":
                data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>Microsoft Excel</Application>", data)
                data = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0300</AppVersion>", data)
            zi = zipfile.ZipInfo(info.filename, ZIPTIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)
    with open(path, "wb") as f:
        f.write(out.getvalue())


def pdf(path, title, author, blocks, subject="", date="D:20260925141200+02'00'"):
    """blocks: list of ('h', text) heading, ('p', text) paragraph, ('t', rows, col_widths_mm) table, ('s', mm) space."""
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.2, leading=12.2, spaceAfter=4)
    head = ParagraphStyle("h", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=10.5, leading=13, spaceBefore=6,
                          spaceAfter=3)
    top = ParagraphStyle("t", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=13, leading=16, spaceAfter=6)
    small = ParagraphStyle("s", parent=body, fontSize=8.2, leading=10.2)
    story = []
    for b in blocks:
        if b[0] == "title":
            story.append(Paragraph(b[1], top))
        elif b[0] == "h":
            story.append(Paragraph(b[1], head))
        elif b[0] == "p":
            story.append(Paragraph(b[1], body))
        elif b[0] == "small":
            story.append(Paragraph(b[1], small))
        elif b[0] == "s":
            story.append(Spacer(1, b[1] * mm))
        elif b[0] == "t":
            rows = [[Paragraph(str(c), small) for c in r] for r in b[1]]
            t = Table(rows, colWidths=[w * mm for w in b[2]], repeatRows=1)
            t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                                   ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6e9ee")),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            story.append(t)
            story.append(Spacer(1, 3 * mm))
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=16 * mm, title=title, author=author, subject=subject, creator=author,
                            producer=author, invariant=1)
    doc.build(story)
    data = re.sub(rb"[^\r\n]*ReportLab[^\r\n]*", lambda m: b"%" + b" " * (len(m.group(0)) - 1), buf.getvalue())
    assert len(date) == 23
    data = data.replace(b"D:20000101000000+00'00'", date.encode())
    with open(path, "wb") as f:
        f.write(data)
