"""Deterministic writers and readers for the pack: CSV, XLSX (repacked with fixed metadata), PDF (reportlab with the
producer scrubbed), and a PDF text reader that decodes ASCII85 then Flate streams."""
import base64
import csv
import io
import re
import zipfile
import zlib

ZIP_TIME = (2027, 2, 12, 8, 40, 0)


def write_csv(path, header, rows, delimiter=","):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=delimiter, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    return len(rows)


def read_csv(path, delimiter=","):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f, delimiter=delimiter))
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


def _app(company, application="Microsoft Excel"):
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
            'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
            '<Application>%s</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>'
            '<Company>%s</Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
            '<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>'
            % (application, company))


def repack_ooxml(path, creator, modified_by, created, modified, title, company, application="Microsoft Excel"):
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
                data = _app(company, application).encode()
            zi = zipfile.ZipInfo(n, date_time=ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)
        if "docProps/app.xml" not in names:
            zi = zipfile.ZipInfo("docProps/app.xml", date_time=ZIP_TIME)
            z.writestr(zi, _app(company, application).encode())
    open(path, "wb").write(out.getvalue())


def write_xlsx(path, sheets, meta):
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
            col = ws.cell(row=ws.max_row, column=i + 1).column_letter
            ws.column_dimensions[col].width = max(10, min(46, len(str(h)) + 4))
    wb.save(path)
    repack_ooxml(path, *meta)


def read_xlsx(path, sheet):
    """(header, rows) of a sheet; the header is the first row whose cells are all filled strings."""
    from openpyxl import load_workbook
    ws = load_workbook(path, read_only=True, data_only=True)[sheet]
    rows = [list(r) for r in ws.iter_rows(values_only=True)]
    for i, r in enumerate(rows):
        cells = [c for c in r if c is not None]
        if len(cells) >= 2 and len(cells) == len([c for c in r if c is not None]) and all(isinstance(c, str) for c in r):
            return [str(c) for c in r], [x for x in rows[i + 1:] if any(c is not None for c in x)]
    return [], rows


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _styles():
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    base = dict(fontName="Helvetica", fontSize=9.4, leading=12.6, textColor=colors.HexColor("#1d2327"))
    return {
        "t": ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=14, leading=18, spaceAfter=6,
                            textColor=colors.HexColor("#14202a")),
        "s": ParagraphStyle("s", fontName="Helvetica", fontSize=8.2, leading=11, spaceAfter=6,
                            textColor=colors.HexColor("#56626b")),
        "h": ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10.6, leading=14, spaceBefore=6, spaceAfter=3),
        "p": ParagraphStyle("p", spaceAfter=5, **base),
        "head": ParagraphStyle("head", fontName="Helvetica-Bold", fontSize=8.4, leading=10.5),
        "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=10.5),
    }


def write_pdf(path, title, author, producer, blocks, footer, created, modified, colw=None):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    st = _styles()

    def page(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.2)
        canvas.setFillColor(colors.HexColor("#5b666d"))
        canvas.drawString(20 * mm, 10 * mm, footer)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Page %d" % d.page)
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
            story += [Image(val[0], width=val[1], height=val[2]), Spacer(1, 6)]
        else:
            story.append(Paragraph(esc(val), st[kind]))
    doc.build(story, onFirstPage=page, onLaterPages=page)
    scrub_pdf(path, created, modified)


def scrub_pdf(path, created, modified):
    data = open(path, "rb").read()
    # the writer's comment lines (the binary marker line keeps its high bytes): blanked at equal length
    data = re.sub(rb"(%[\x80-\xff]*)([^\n]*ReportLab[^\n]*)\n",
                  lambda m: m.group(1) + b" " * len(m.group(2)) + b"\n", data)
    data = re.sub(rb"/CreationDate \(D:[^)]*\)", lambda m: b"/CreationDate (" + created.encode().ljust(
        len(m.group(0)) - 16, b" ")[:len(m.group(0)) - 16] + b")", data)
    data = re.sub(rb"/ModDate \(D:[^)]*\)", lambda m: b"/ModDate (" + modified.encode().ljust(
        len(m.group(0)) - 11, b" ")[:len(m.group(0)) - 11] + b")", data)
    open(path, "wb").write(data)


def _unescape(s):
    s = re.sub(rb"\\([0-7]{1,3})", lambda m: bytes([int(m.group(1), 8) & 0xFF]), s)
    s = s.replace(rb"\(", b"(").replace(rb"\)", b")").replace(rb"\n", b"\n").replace(rb"\r", b"\r")
    s = s.replace(rb"\t", b"\t").replace(b"\\\\", b"\\")
    return s.decode("latin-1")


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
