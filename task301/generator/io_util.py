"""Deterministic writers and readers for the pack: CSV, XLSX and DOCX (repacked with fixed metadata and zip times),
PDF (reportlab with the producer comment blanked and fixed dates), and text readers for PDF (ASCII85 then Flate
streams) and DOCX (document.xml runs). The verifier reads the bundle back through the readers here."""
import base64
import csv
import io
import re
import zipfile
import zlib

ZIP_TIME = (2026, 11, 6, 9, 15, 0)


def write_csv(path, header, rows, delimiter=",", encoding="utf-8"):
    with open(path, "w", newline="", encoding=encoding) as f:
        w = csv.writer(f, delimiter=delimiter, lineterminator="\r\n" if delimiter == ";" else "\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    return len(rows)


def read_csv(path, delimiter=",", encoding="utf-8"):
    with open(path, newline="", encoding=encoding) as f:
        rows = list(csv.reader(f, delimiter=delimiter))
    return rows[0], rows[1:]


def comma(x, nd=2):
    """A number written the Spanish way: decimal comma, no thousands separator."""
    if x is None or x == "":
        return ""
    return ("%.*f" % (nd, x)).replace(".", ",")


def uncomma(s):
    s = (s or "").strip()
    if s == "":
        return None
    return float(s.replace(".", "").replace(",", ".")) if "," in s else float(s)


def _core(creator, modified_by, created, modified, title):
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<dc:title>%s</dc:title><dc:creator>%s</dc:creator><cp:lastModifiedBy>%s</cp:lastModifiedBy>'
            '<dcterms:created xsi:type="dcterms:W3CDTF">%s</dcterms:created>'
            '<dcterms:modified xsi:type="dcterms:W3CDTF">%s</dcterms:modified></cp:coreProperties>'
            % (title, creator, modified_by, created, modified))


def _app(company, application, version):
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
            'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
            '<Application>%s</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>'
            '<Company>%s</Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
            '<HyperlinksChanged>false</HyperlinksChanged><AppVersion>%s</AppVersion></Properties>'
            % (application, company, version))


def repack_ooxml(path, creator, modified_by, created, modified, title, company, application="Microsoft Excel",
                 version="16.0300"):
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
                data = _app(company, application, version).encode()
            zi = zipfile.ZipInfo(n, date_time=ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)
        if "docProps/app.xml" not in names:
            zi = zipfile.ZipInfo("docProps/app.xml", date_time=ZIP_TIME)
            z.writestr(zi, _app(company, application, version).encode())
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
            col = ws.cell(row=ws.max_row, column=i + 1).column_letter
            ws.column_dimensions[col].width = (widths or {}).get(h, max(10, min(48, len(str(h)) + 4)))
    wb.save(path)
    repack_ooxml(path, *meta)


def read_xlsx(path, sheet):
    """(header, rows) of a sheet: the header is the first row with at least two cells, all strings, after any
    title lines."""
    from openpyxl import load_workbook
    ws = load_workbook(path, read_only=True, data_only=True)[sheet]
    rows = [list(r) for r in ws.iter_rows(values_only=True)]
    for i, r in enumerate(rows):
        cells = [c for c in r if c is not None]
        if len(cells) >= 2 and all(isinstance(c, str) for c in cells):
            return [str(c) for c in r if c is not None], [x for x in rows[i + 1:] if any(c is not None for c in x)]
    return [], rows


def sheet_names(path):
    from openpyxl import load_workbook
    return load_workbook(path, read_only=True).sheetnames


def write_docx(path, title, paragraphs, meta):
    """paragraphs: list of (style, text); style in title, sub, h, p, table (text is a list of rows)."""
    import docx
    from docx.shared import Pt
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for kind, val in paragraphs:
        if kind == "title":
            d.add_heading(val, level=1)
        elif kind == "h":
            d.add_heading(val, level=2)
        elif kind == "sub":
            p = d.add_paragraph(val)
            p.runs[0].italic = True
        elif kind == "table":
            t = d.add_table(rows=len(val), cols=len(val[0]))
            t.style = "Table Grid"
            for i, r in enumerate(val):
                for j, c in enumerate(r):
                    t.cell(i, j).text = str(c)
        else:
            d.add_paragraph(val)
    d.core_properties.title = title
    d.save(path)
    repack_ooxml(path, *meta, application="Microsoft Office Word", version="16.0000")


def docx_text(path):
    """Every paragraph and table cell of a DOCX, in document order."""
    z = zipfile.ZipFile(path)
    xml = z.read("word/document.xml").decode("utf-8")
    z.close()
    paras = re.findall(r"<w:p[ >].*?</w:p>", xml, re.S)
    out = []
    for p in paras:
        out.append("".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, re.S)))
    txt = "\n".join(x for x in out if x)
    return txt.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _styles():
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    base = dict(fontName="Helvetica", fontSize=9.3, leading=12.4, textColor=colors.HexColor("#1f2428"))
    return {
        "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=5,
                                textColor=colors.HexColor("#17212b")),
        "sub": ParagraphStyle("sub", fontName="Helvetica", fontSize=8.2, leading=11, spaceAfter=7,
                              textColor=colors.HexColor("#56626b")),
        "h": ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10.4, leading=13.6, spaceBefore=6, spaceAfter=3),
        "p": ParagraphStyle("p", spaceAfter=5, **base),
        "small": ParagraphStyle("small", fontName="Helvetica", fontSize=7.8, leading=10, spaceAfter=4,
                                textColor=colors.HexColor("#4a545b")),
        "head": ParagraphStyle("head", fontName="Helvetica-Bold", fontSize=8.2, leading=10.2),
        "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=8.2, leading=10.2),
    }


def write_pdf(path, title, author, producer, blocks, footer, created, modified, colw=None):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    st = _styles()

    def page(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.0)
        canvas.setFillColor(colors.HexColor("#5b666d"))
        canvas.drawString(20 * mm, 10 * mm, footer)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "%d" % d.page)
        canvas.restoreState()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=17 * mm,
                            bottomMargin=17 * mm, title=title, author=author, creator=producer, producer=producer,
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
    """Every text string drawn on a PDF's pages, in order (ASCII85 then Flate streams decoded)."""
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
    return re.sub(r"\s+", " ", " ".join(out))
