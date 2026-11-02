"""Deterministic writers (CSV, XLSX, PDF) with fixed metadata, and the shared PDF text decoder."""
import base64
import csv
import io
import os
import re
import zipfile
import zlib

import params as P

FIXED_ZIP_DT = (2026, 11, 13, 9, 30, 0)
COMPANY = "Aubreth Gold Corporation"


def write_csv(path, header, rows, lineterminator="\r\n", preamble=None):
    with open(path, "w", newline="", encoding="utf-8") as f:
        if preamble:
            for line in preamble:
                f.write(line + lineterminator)
        w = csv.writer(f, lineterminator=lineterminator)
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def _normalise_zip(path, core_xml, app_xml):
    with zipfile.ZipFile(path) as z:
        items = [(n, z.read(n)) for n in z.namelist()]
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for n, data in sorted(items, key=lambda x: (x[0] != "[Content_Types].xml", x[0])):
            if n == "docProps/core.xml":
                data = core_xml.encode("utf-8")
            if n == "docProps/app.xml":
                data = app_xml.encode("utf-8")
            zi = zipfile.ZipInfo(n, date_time=FIXED_ZIP_DT)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)
    with open(path, "wb") as f:
        f.write(out.getvalue())


def core_props(title, creator, created, modified=None):
    modified = modified or created
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f'<dc:title>{title}</dc:title><dc:creator>{creator}</dc:creator><cp:lastModifiedBy>{creator}</cp:lastModifiedBy>'
            f'<dcterms:created xsi:type="dcterms:W3CDTF">{created}</dcterms:created>'
            f'<dcterms:modified xsi:type="dcterms:W3CDTF">{modified}</dcterms:modified>'
            '</cp:coreProperties>')


def app_props(app="Microsoft Excel", company=COMPANY):
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
            'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
            f'<Application>{app}</Application><Company>{company}</Company></Properties>')


def save_xlsx(wb, path, title, creator, created, company=COMPANY):
    wb.save(path)
    _normalise_zip(path, core_props(title, creator, created), app_props("Microsoft Excel", company))


def set_mtime(path, when=None):
    ts = (when or P.EXPORT_MTIME).timestamp()
    os.utime(path, (ts, ts))


def pdf_text(path):
    """Text of a PDF written by reportlab (ASCII85 then Flate, or Flate alone), one string."""
    raw = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"stream\r?\n(.*?)\s*endstream", raw, re.S):
        data = m.group(1)
        head = raw[raw.rfind(b"<<", 0, m.start()):m.start()]
        try:
            if b"ASCII85Decode" in head:
                d = data.strip()
                if d.endswith(b"~>"):
                    d = d[:-2]
                if d.startswith(b"<~"):
                    d = d[2:]
                data = base64.a85decode(d)
            if b"FlateDecode" in head:
                data = zlib.decompress(data)
        except Exception:
            continue
        for t in re.findall(rb"\((.*?)(?<!\\)\)\s*Tj", data, re.S):
            out.append(t.decode("latin-1").replace("\\(", "(").replace("\\)", ")").replace("\\\\", "\\"))
    return "\n".join(out)


def write_pdf(path, title, author, pages, stamp, producer=COMPANY):
    """pages: list of pages; each page a list of (font, size, text or cells, xs or None, dy)."""
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(path, pagesize=A4, invariant=1)
    c.setTitle(title)
    c.setAuthor(author)
    c.setCreator(author)
    c.setProducer(producer)
    c.setSubject(title)
    w, h = A4
    for lines in pages:
        y = h - 56
        for item in lines:
            font, size, text, xs = item[:4]
            dy = item[4] if len(item) > 4 else (16 if size >= 10 else 12.5)
            c.setFont(font, size)
            if xs is None:
                c.drawString(52, y, text)
            else:
                for x, cell in zip(xs, text):
                    if isinstance(x, tuple):          # right-aligned at x[0]
                        c.drawRightString(x[0], y, cell)
                    else:
                        c.drawString(x, y, cell)
            y -= dy
        c.showPage()
    c.save()
    _scrub(path, stamp)


def _scrub(path, stamp):
    before = pdf_text(path)
    b = open(path, "rb").read()
    n = len(b)

    def blank(m):
        return m.group(1) + b" " * (len(m.group(0)) - len(m.group(1)))
    b = re.sub(rb"(%\x93\x8c\x8b\x9e)[^\n]*ReportLab[^\n]*", blank, b)
    b = re.sub(rb"(%)[^\n]*ReportLab[^\n]*", blank, b)
    for o in set(re.findall(rb"/(?:CreationDate|ModDate) \((D:[^)]*)\)", b)):
        assert len(o) == len(stamp), (o, stamp)
        b = b.replace(o, stamp.encode("latin-1"))
    assert len(b) == n and b"ReportLab" not in b
    open(path, "wb").write(b)
    assert pdf_text(path) == before
