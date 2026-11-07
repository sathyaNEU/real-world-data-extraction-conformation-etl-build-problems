"""task468 architecture 6: the file writers (CSV, workbook and PDF with their own stamps, email)."""
import csv
import io
import re
import zipfile

import openpyxl
from openpyxl.styles import Font
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def csv_file(path, header, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    if header:
        w.writerow(header)
    w.writerows(rows)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())


def xlsx(path, sheets, creator, created, modified, widths=None, company=None):
    """sheets: (title, rows, bold_row_numbers, {column_letter: number_format})."""
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for title, rows, bold, fmt in sheets:
        ws = wb.create_sheet(title)
        for r in rows:
            ws.append(list(r))
        for i in bold:
            for c in ws[i]:
                c.font = Font(bold=True)
        for col, nf in (fmt or {}).items():
            for c in ws[col][1:]:
                c.number_format = nf
        for k, wdt in enumerate(widths or [14, 16, 26, 18, 14, 16, 16, 16, 16, 16, 14, 14]):
            ws.column_dimensions[openpyxl.utils.get_column_letter(k + 1)].width = wdt
        ws.freeze_panes = "A2" if title not in ("Notes", "About") else None
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.created = created
    wb.properties.modified = modified
    wb.properties.title = None
    buf = io.BytesIO()
    wb.save(buf)
    src = zipfile.ZipFile(io.BytesIO(buf.getvalue()))
    app = (b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
           b'<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
           b'<Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>'
           + (b"<Company>" + company.encode() + b"</Company>" if company else b"")
           + b'<LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
           b'<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for info in src.infolist():
            data = src.read(info.filename)
            if info.filename == "docProps/core.xml":
                data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                              b"\\g<1>" + modified.strftime("%Y-%m-%dT%H:%M:%SZ").encode() + b"\\g<2>", data)
                data = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)",
                              b"\\g<1>" + created.strftime("%Y-%m-%dT%H:%M:%SZ").encode() + b"\\g<2>", data)
            if info.filename == "docProps/app.xml":
                data = app
            zi = zipfile.ZipInfo(info.filename, date_time=modified.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)


def _styles():
    base = ParagraphStyle("p", fontName="Helvetica", fontSize=9.6, leading=13, alignment=TA_LEFT, spaceAfter=5)
    return {"t": ParagraphStyle("t", parent=base, fontName="Helvetica-Bold", fontSize=13, leading=17, spaceAfter=4),
            "s": ParagraphStyle("s", parent=base, fontSize=8.4, leading=11, textColor=colors.HexColor("#4a5560")),
            "h": ParagraphStyle("h", parent=base, fontName="Helvetica-Bold", fontSize=10.4, leading=14, spaceBefore=6),
            "p": base,
            "cell": ParagraphStyle("c", parent=base, fontSize=8.2, leading=10.2, spaceAfter=0)}


def pdf(path, blocks, title, author, created, modified, footer, widths=None):
    """blocks: (kind, value); kind t, s, h, p, table (rows of cells, wrapped) or image (path, width_mm, height_mm)."""
    st = _styles()

    def page(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#5b6670"))
        canvas.drawString(20 * mm, 10 * mm, footer)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=author, producer=author,
                            invariant=1)
    story = []
    for kind, val in blocks:
        if kind == "table":
            rows, ws = val if isinstance(val, tuple) else (val, None)
            width = A4[0] - 40 * mm
            n = len(rows[0])
            ws = [w * mm for w in ws] if ws else [width / n] * n
            cells = [[Paragraph(str(c).replace("&", "&amp;"), st["cell"]) for c in r] for r in rows]
            t = Table(cells, colWidths=ws, hAlign="LEFT", repeatRows=1)
            t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#8a949c")),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
            story += [t, Spacer(1, 6)]
        elif kind == "image":
            p, wmm, hmm = val
            story += [Image(p, width=wmm * mm, height=hmm * mm), Spacer(1, 6)]
        else:
            story.append(Paragraph(val, st[kind]))
    doc.build(story, onFirstPage=page, onLaterPages=page)
    data = open(path, "rb").read()
    data = re.sub(rb"/CreationDate \(D:[^)]*\)", b"/CreationDate (" + created.encode() + b")", data)
    data = re.sub(rb"/ModDate \(D:[^)]*\)", b"/ModDate (" + modified.encode() + b")", data)
    for sig in (b"ReportLab Generated PDF document (opensource)",
                b"ReportLab generated PDF document -- digest (opensource)"):
        data = data.replace(sig, b" " * len(sig))
    open(path, "wb").write(data)
