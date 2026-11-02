"""Deterministic writers: CSV, XLSX, DOCX and PDF that rebuild byte for byte."""
import csv
import io
import os
import zipfile

FIXED_ZIP_TIME = (2026, 9, 1, 8, 0, 0)


def write_csv(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def normalise_zip(path, when=FIXED_ZIP_TIME, modified=None):
    """Rewrite an OOXML zip with fixed timestamps and a fixed member order; pin the core modified stamp."""
    import re
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    if modified is not None:
        stamp = modified.strftime("%Y-%m-%dT%H:%M:%SZ").encode()
        items = [(n, re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>" + stamp + rb"\g<2>", d)
                  if n == "docProps/core.xml" else d) for n, d in items]
    app = {".xlsx": (b"Microsoft Excel", b"16.0300"), ".docx": (b"Microsoft Office Word", b"16.0000")}.get(
        os.path.splitext(path)[1].lower())
    if app:
        items = [(n, re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>" + app[1] + b"</AppVersion>",
                            re.sub(rb"<Application>[^<]*</Application>", b"<Application>" + app[0] + b"</Application>", d))
                  if n == "docProps/app.xml" else d) for n, d in items]
    first = [x for x in items if x[0] == "[Content_Types].xml"]
    rest = sorted([x for x in items if x[0] != "[Content_Types].xml"], key=lambda x: x[0])
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as out:
        for name, data in first + rest:
            zi = zipfile.ZipInfo(name, date_time=(modified.timetuple()[:6] if modified is not None else when))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            out.writestr(zi, data)
    with open(path, "wb") as f:
        f.write(buf.getvalue())


def fix_xlsx_props(wb, when, creator):
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.created = when
    wb.properties.modified = when


def fix_docx_props(doc, when, author):
    cp = doc.core_properties
    cp.author = author
    cp.last_modified_by = author
    cp.created = when
    cp.modified = when
    cp.revision = 1
    cp.title = ""
    cp.comments = ""
    cp.keywords = ""
    cp.subject = ""
    cp.category = ""


def finish_pdf(path, producer, creator, when):
    """Re-serialise a written PDF (drops the writing library's header comment) with the issuer's own metadata."""
    import io as _io
    from pypdf import PdfReader, PdfWriter
    r = PdfReader(path)
    before = [p.extract_text() for p in r.pages]
    w = PdfWriter(clone_from=r)
    stamp = when.strftime("D:%Y%m%d%H%M%S-05'00'")
    w.add_metadata({"/Producer": producer, "/Creator": creator, "/CreationDate": stamp, "/ModDate": stamp})
    buf = _io.BytesIO()
    w.write(buf)
    data = buf.getvalue()
    after = [p.extract_text() for p in PdfReader(_io.BytesIO(data)).pages]
    assert before == after, path
    with open(path, "wb") as f:
        f.write(data)
