"""Deterministic writers: CSV, XLSX, DOCX and PDF with fixed metadata so two builds are byte-identical."""
import csv
import datetime as dt
import io
import os
import re
import zipfile

import params as P

FIXED_ZIP_DT = P.ZIP_DT


def write_csv(path, header, rows, delimiter=","):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=delimiter, lineterminator="\r\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)


TEMPLATE_PARTS = ("word/stylesWithEffects.xml", "docProps/thumbnail.jpeg")


def _normalise_zip(path, core_xml=None, app_xml=None, stamp=None):
    """Rewrite an OOXML zip with sorted members, scrubbed core properties, the writing library's template parts removed
    (with their relationships and content types) and every entry dated by the document's own last-saved stamp."""
    when = FIXED_ZIP_DT
    if stamp:
        d = dt.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ")
        when = (d.year, d.month, d.day, d.hour, d.minute, d.second)
    with zipfile.ZipFile(path) as z:
        items = [(n, z.read(n)) for n in z.namelist() if n not in TEMPLATE_PARTS]
    names = {n for n, _ in items}
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for n, data in sorted(items, key=lambda x: (x[0] != "[Content_Types].xml", x[0])):
            if n == "docProps/core.xml" and core_xml is not None:
                data = core_xml.encode("utf-8")
            if n == "docProps/app.xml" and app_xml is not None:
                data = app_xml.encode("utf-8")
            if n == "[Content_Types].xml" or n.endswith(".rels"):
                txt = data.decode("utf-8")
                for part in TEMPLATE_PARTS:
                    leaf = part.split("/")[-1]
                    txt = re.sub(r'<Override[^>]*PartName="/%s"[^>]*/>' % re.escape(part), "", txt)
                    txt = re.sub(r'<Relationship[^>]*Target="(?:/?%s|%s)"[^>]*/>' % (re.escape(part), re.escape(leaf)), "", txt)
                if n == "[Content_Types].xml" and not any(m.endswith((".jpeg", ".jpg")) for m in names):
                    txt = re.sub(r'<Default[^>]*Extension="jpe?g"[^>]*/>', "", txt)
                data = txt.encode("utf-8")
            zi = zipfile.ZipInfo(n, date_time=when)
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


def app_props(app="Microsoft Excel", company="Fendmouth Borough Council"):
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
            'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
            f'<Application>{app}</Application><Company>{company}</Company></Properties>')


def save_xlsx(wb, path, title, creator, created, company="Fendmouth Borough Council", modified=None):
    wb.save(path)
    _normalise_zip(path, core_props(title, creator, created, modified), app_props("Microsoft Excel", company),
                   stamp=modified or created)


def save_docx(doc, path, title, creator, created, company="Fendmouth Borough Council", modified=None):
    doc.save(path)
    _normalise_zip(path, core_props(title, creator, created, modified), app_props("Microsoft Office Word", company),
                   stamp=modified or created)


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
