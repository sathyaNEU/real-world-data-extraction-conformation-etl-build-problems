"""Deterministic writers: CSV, XLSX, DOCX and PDF with fixed metadata so two builds are byte-identical."""
import csv
import datetime as dt
import io
import os
import re
import zipfile

import params as P

FIXED_ZIP_DT = (2026, 10, 16, 9, 12, 0)


def write_csv(path, header, rows, delimiter=","):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=delimiter, lineterminator="\r\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def _normalise_zip(path, core_xml=None, app_xml=None):
    """Rewrite an OOXML zip with fixed timestamps, sorted members and scrubbed core properties."""
    with zipfile.ZipFile(path) as z:
        items = [(n, z.read(n)) for n in z.namelist()]
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for n, data in sorted(items, key=lambda x: (x[0] != "[Content_Types].xml", x[0])):
            if n == "docProps/core.xml" and core_xml is not None:
                data = core_xml.encode("utf-8")
            if n == "docProps/app.xml" and app_xml is not None:
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


def app_props(app="Microsoft Excel", company="Orari Bank Limited"):
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
            'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
            f'<Application>{app}</Application><Company>{company}</Company></Properties>')


def save_xlsx(wb, path, title, creator, created):
    wb.save(path)
    _normalise_zip(path, core_props(title, creator, created), app_props("Microsoft Excel"))


def save_docx(doc, path, title, creator, created):
    doc.save(path)
    _normalise_zip(path, core_props(title, creator, created), app_props("Microsoft Office Word"))


def set_mtime(path):
    ts = P.EXPORT_DATE.timestamp()
    os.utime(path, (ts, ts))


def fmt_date(d, style="dmy_slash"):
    if style == "dmy_slash":
        return d.strftime("%d/%m/%Y")
    if style == "iso":
        return d.isoformat()
    if style == "dmy_mon":
        return d.strftime("%d-%b-%Y")
    raise ValueError(style)


def pdf_text(path):
    """Extract text from a PDF written by reportlab (ASCII85 then Flate, or Flate alone)."""
    import base64
    import zlib
    raw = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"stream\r?\n(.*?)\s*endstream", raw, re.S):
        data = m.group(1)
        dict_start = raw.rfind(b"<<", 0, m.start())
        head = raw[dict_start:m.start()]
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
        for arr in re.findall(rb"\[(.*?)\]\s*TJ", data, re.S):
            parts = re.findall(rb"\((.*?)(?<!\\)\)", arr, re.S)
            out.append("".join(p.decode("latin-1") for p in parts))
    return "\n".join(out)
