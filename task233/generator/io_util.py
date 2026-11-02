"""Writers that give byte-identical files on every run and carry each document's own producer and save dates."""
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
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ZIP_TIME = (2026, 10, 15, 8, 30, 0)


def write_csv(path, header, rows, newline="\r\n"):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator=newline)
    w.writerow(header)
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    return len(rows)


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


def repack_xlsx(path, creator, created, modified, title, company, stamp=ZIP_TIME):
    """Rewrite docProps in the issuing body's own voice and fix every entry's date, so two runs match."""
    src = zipfile.ZipFile(path)
    items = [(n, src.read(n)) for n in src.namelist()]
    src.close()
    names = [n for n, _ in items]
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for n, data in items:
            if n == "docProps/core.xml":
                data = _core(creator, creator, created, modified, title).encode()
            elif n == "docProps/app.xml":
                data = _app(company).encode()
            zi = zipfile.ZipInfo(n, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)
        if "docProps/app.xml" not in names:
            zi = zipfile.ZipInfo("docProps/app.xml", date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, _app(company).encode())
    open(path, "wb").write(out.getvalue())


INK = colors.HexColor("#1d2731")
RULE = colors.HexColor("#7b8790")


def _styles():
    base = ParagraphStyle("p", fontName="Helvetica", fontSize=9.4, leading=12.8, textColor=INK, alignment=TA_LEFT,
                          spaceAfter=5)
    return {"t": ParagraphStyle("t", parent=base, fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4),
            "s": ParagraphStyle("s", parent=base, fontSize=8.2, leading=10.8, textColor=colors.HexColor("#4d5961")),
            "h": ParagraphStyle("h", parent=base, fontName="Helvetica-Bold", fontSize=10.2, leading=13.6, spaceBefore=6),
            "p": base,
            "cell": ParagraphStyle("cell", parent=base, fontSize=8.4, leading=10.6, spaceAfter=0),
            "head": ParagraphStyle("head", parent=base, fontName="Helvetica-Bold", fontSize=8.4, leading=10.6, spaceAfter=0)}


def esc(x):
    return str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write_pdf(path, title, author, producer, blocks, footer, created, modified, widths=None):
    """blocks: (style, text) paragraphs, ("table", rows) or ("image", (png_path, width_mm, height_mm));
    created and modified as PDF dates, e.g. D:20261016101500+13'00'."""
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
                            subject=title, invariant=1)
    story = []
    width = A4[0] - 40 * mm
    for kind, val in blocks:
        if kind == "table":
            ncol = max(len(r) for r in val)
            w = widths.get(ncol) if widths else None
            cw = w or ([48 * mm, width - 48 * mm] if ncol == 2 else [width / ncol] * ncol)
            data = [[Paragraph(esc(c), st["head"] if i == 0 else st["cell"]) for c in r] for i, r in enumerate(val)]
            t = Table(data, colWidths=cw, hAlign="LEFT", repeatRows=1)
            t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("TOPPADDING", (0, 0), (-1, -1), 2)]))
            story += [t, Spacer(1, 6)]
        elif kind == "image":
            p, wmm, hmm = val
            story += [Image(p, width=wmm * mm, height=hmm * mm), Spacer(1, 6)]
        elif kind == "space":
            story.append(Spacer(1, val))
        else:
            story.append(Paragraph(val, st[kind]))
    doc.build(story, onFirstPage=page, onLaterPages=page)
    data = open(path, "rb").read()
    for sig in (b"ReportLab Generated PDF document (opensource)", b"ReportLab generated PDF document -- digest (opensource)",
                b"ReportLab Generated PDF document http://www.reportlab.com"):
        data = data.replace(sig, b" " * len(sig))
    data = re.sub(rb"/CreationDate \(D:[^)]*\)", b"/CreationDate (" + created.encode() + b")", data)
    data = re.sub(rb"/ModDate \(D:[^)]*\)", b"/ModDate (" + modified.encode() + b")", data)
    open(path, "wb").write(data)


def pdf_text(path):
    """Every text string drawn on a shipped PDF's pages, in order (ASCII85 then Flate streams decoded)."""
    data = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"stream\s*\n(.*?)endstream", data, re.S):
        raw = m.group(1).strip()
        txt = raw
        try:
            if raw.endswith(b"~>"):
                raw = base64.a85decode(raw[:-2], adobe=False)
            txt = zlib.decompress(raw)
        except Exception:
            try:
                txt = zlib.decompress(raw)
            except Exception:
                txt = raw
        for s in re.findall(rb"\((.*?)(?<!\\)\)\s*Tj", txt, re.S):
            out.append(s.replace(rb"\(", b"(").replace(rb"\)", b")").replace(rb"\\", b"\\").decode("latin-1"))
    return " ".join(out)
