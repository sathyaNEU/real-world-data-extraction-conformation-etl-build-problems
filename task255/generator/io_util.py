"""Writers that give byte-identical files on every run, each document carrying its own producer and dates,
and the readers the analysis and the verifier share for the formats the pack ships."""
import base64
import csv
import io
import re
import zipfile
import zlib

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ZIP_TIME = (2026, 11, 13, 8, 20, 0)


def write_csv(path, header, rows, delimiter=",", newline="\r\n", preamble=None):
    buf = io.StringIO()
    for line in preamble or []:
        buf.write(line + newline)
    w = csv.writer(buf, delimiter=delimiter, lineterminator=newline)
    w.writerow(header)
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    return len(rows)


def read_csv(path, delimiter=",", skip=0):
    with open(path, encoding="utf-8", newline="") as f:
        lines = f.read().splitlines()
    rows = list(csv.reader(lines[skip:], delimiter=delimiter))
    return rows[0], rows[1:]


def _core(creator, modified_by, created, modified, title):
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<dc:title>%s</dc:title><dc:creator>%s</dc:creator><cp:lastModifiedBy>%s</cp:lastModifiedBy>'
            '<dcterms:created xsi:type="dcterms:W3CDTF">%s</dcterms:created>'
            '<dcterms:modified xsi:type="dcterms:W3CDTF">%s</dcterms:modified></cp:coreProperties>'
            % (title, creator, modified_by, created, modified))


def _app(company):
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
            'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
            '<Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>'
            '<Company>%s</Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
            '<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>' % company)


def repack_xlsx(path, creator, modified_by, created, modified, title, company):
    src = zipfile.ZipFile(path)
    items = [(n, src.read(n)) for n in src.namelist()]
    src.close()
    names = [n for n, _ in items]
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for n, data in items:
            if n == "docProps/core.xml":
                data = _core(creator, modified_by, created, modified, title).encode()
            elif n == "docProps/app.xml":
                data = _app(company).encode()
            zi = zipfile.ZipInfo(n, date_time=ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)
        if "docProps/app.xml" not in names:
            zi = zipfile.ZipInfo("docProps/app.xml", date_time=ZIP_TIME)
            z.writestr(zi, _app(company).encode())
    open(path, "wb").write(out.getvalue())


def write_xlsx(path, sheets, meta, widths=None):
    """sheets: list of (name, header, rows, preamble_lines)."""
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    wb.remove(wb.active)
    for name, header, rows, pre in sheets:
        ws = wb.create_sheet(name)
        for line in pre or []:
            ws.append([line])
        ws.append(header)
        for c in ws[ws.max_row]:
            c.font = Font(bold=True)
        for r in rows:
            ws.append(list(r))
        for i, h in enumerate(header):
            col = ws.cell(row=1, column=i + 1).column_letter
            ws.column_dimensions[col].width = max(10, min(46, len(str(h)) + 4))
    wb.save(path)
    repack_xlsx(path, *meta)


def read_xlsx(path, sheet, header_row=None):
    from openpyxl import load_workbook
    wb = load_workbook(path, data_only=True, read_only=True)
    ws = wb[sheet]
    rows = [list(r) for r in ws.iter_rows(values_only=True)]
    wb.close()
    if header_row is None:
        header_row = 0
        for i, r in enumerate(rows):
            if r and sum(1 for c in r if c not in (None, "")) >= 2:
                header_row = i
                break
    return [str(c) for c in rows[header_row] if c is not None], rows[header_row + 1:]


INK = colors.HexColor("#1d2731")


def _styles():
    base = ParagraphStyle("p", fontName="Helvetica", fontSize=9.2, leading=12.6, textColor=INK, alignment=TA_LEFT,
                          spaceAfter=5)
    return {"t": ParagraphStyle("t", parent=base, fontName="Helvetica-Bold", fontSize=13.5, leading=17,
                                spaceAfter=4),
            "s": ParagraphStyle("s", parent=base, fontSize=8.0, leading=10.6, textColor=colors.HexColor("#4f5b62")),
            "h": ParagraphStyle("h", parent=base, fontName="Helvetica-Bold", fontSize=10.2, leading=13.6,
                                spaceBefore=6),
            "p": base,
            "cell": ParagraphStyle("cell", parent=base, fontSize=8.3, leading=10.6, spaceAfter=0),
            "head": ParagraphStyle("head", parent=base, fontName="Helvetica-Bold", fontSize=8.3, leading=10.6,
                                   spaceAfter=0)}


def esc(x):
    return str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write_pdf(path, title, author, producer, blocks, footer, created, modified, colw=None):
    st = _styles()

    def page(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.2)
        canvas.setFillColor(colors.HexColor("#5b666d"))
        canvas.drawString(20 * mm, 10 * mm, footer)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Pagina %d" % d.page)
        canvas.restoreState()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=producer, producer=producer,
                            invariant=1)
    story = []
    width = A4[0] - 40 * mm
    for kind, val in blocks:
        if kind == "table":
            ncol = max(len(r) for r in val)
            cw = (colw or {}).get(ncol) or [width / ncol] * ncol
            data = [[Paragraph(esc(c), st["head"] if i == 0 else st["cell"]) for c in r] for i, r in enumerate(val)]
            t = Table(data, colWidths=cw, hAlign="LEFT", repeatRows=1)
            t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#7d8b93")),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                                   ("TOPPADDING", (0, 0), (-1, -1), 2)]))
            story += [t, Spacer(1, 6)]
        elif kind == "img":
            from reportlab.platypus import Image
            story += [Image(val[0], width=val[1], height=val[2]), Spacer(1, 6)]
        else:
            story.append(Paragraph(val, st[kind]))
    doc.build(story, onFirstPage=page, onLaterPages=page)
    scrub_pdf(path, created, modified)


def scrub_pdf(path, created, modified):
    data = open(path, "rb").read()
    for sig in (b"ReportLab Generated PDF document (opensource)",
                b"ReportLab generated PDF document -- digest (opensource)",
                b"ReportLab Generated PDF document http://www.reportlab.com", b"(unspecified)"):
        data = data.replace(sig, b" " * len(sig))
    data = re.sub(rb"/CreationDate \(D:[^)]*\)", b"/CreationDate (" + created.encode() + b")", data)
    data = re.sub(rb"/ModDate \(D:[^)]*\)", b"/ModDate (" + modified.encode() + b")", data)
    open(path, "wb").write(data)


def pdf_text(path):
    """Every text string drawn on a shipped PDF's pages, in order (ASCII85 then Flate streams decoded)."""
    data = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", data, re.S):
        raw = m.group(1).strip()
        txt = raw
        try:
            if raw.endswith(b"~>"):
                raw = base64.a85decode(raw[:-2] if not raw.startswith(b"<~") else raw[2:-2])
            txt = zlib.decompress(raw)
        except Exception:
            pass
        for s in re.findall(rb"\((.*?)(?<!\\)\)\s*Tj", txt, re.S):
            out.append(_unescape(s))
    return " ".join(out)


def _unescape(s):
    """A PDF literal string's escapes: \\ddd octal, \\n, \\r, \\t, \\(, \\), \\\\."""
    out = bytearray()
    i = 0
    while i < len(s):
        c = s[i]
        if c == 0x5C and i + 1 < len(s):
            n = s[i + 1]
            if 0x30 <= n <= 0x37:
                j = i + 1
                k = j
                while k < len(s) and k < j + 3 and 0x30 <= s[k] <= 0x37:
                    k += 1
                out.append(int(s[j:k], 8) & 0xFF)
                i = k
                continue
            out.append({0x6E: 0x0A, 0x72: 0x0D, 0x74: 0x09}.get(n, n))
            i += 2
            continue
        out.append(c)
        i += 1
    return bytes(out).decode("latin-1")
