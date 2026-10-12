"""Container hygiene: in-fiction authors and dates in every binary's metadata, one export time on the folder."""
import datetime as dt
import io
import os
import zipfile
from pathlib import Path

import pyarrow.parquet as pq
from pypdf import PdfReader, PdfWriter

META = {
    "tallybridge_trust_licence_terms_2026.pdf": ("Tallybridge Maths Ltd", "Trust Licence terms",
                                                 dt.datetime(2026, 5, 12, 10, 4)),
    "tallybridge_price_list_2026-27.pdf": ("Tallybridge Maths Ltd", "School subscriptions price list 2026-27",
                                           dt.datetime(2026, 3, 18, 15, 22)),
    "trust_partnerships_plan_2027.docx": ("Pamela Andrews", "", dt.datetime(2026, 10, 8, 17, 41)),
    "trust_licence_pilot_2026.xlsx": ("Pamela Andrews", "", dt.datetime(2026, 9, 2, 11, 18)),
}
EXPORT = dt.datetime(2026, 10, 20, 17, 40)


def _pdfdate(t):
    return t.strftime("D:%Y%m%d%H%M%S+01'00'")


def seal_pdf(path, author, title, when):
    r = PdfReader(str(path))
    w = PdfWriter()
    for p in r.pages:
        w.add_page(p)
    w.add_metadata({"/Author": author, "/Creator": author, "/Producer": author, "/Title": title,
                    "/CreationDate": _pdfdate(when), "/ModDate": _pdfdate(when)})
    buf = io.BytesIO()
    w.write(buf)
    path.write_bytes(buf.getvalue())


def seal_ooxml(path, author, when):
    src = zipfile.ZipFile(path)
    items = [(i, src.read(i.filename)) for i in src.infolist()]
    src.close()
    stamp = when.strftime("%Y-%m-%dT%H:%M:%SZ")
    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<dc:creator>%s</dc:creator><cp:lastModifiedBy>%s</cp:lastModifiedBy>'
            '<dcterms:created xsi:type="dcterms:W3CDTF">%s</dcterms:created>'
            '<dcterms:modified xsi:type="dcterms:W3CDTF">%s</dcterms:modified></cp:coreProperties>'
            % (author, author, stamp, stamp)).encode()
    app = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
           '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
           '<Application>Microsoft Office</Application></Properties>').encode()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for info, data in items:
            if info.filename == "docProps/core.xml":
                data = core
            elif info.filename == "docProps/app.xml":
                data = app
            zi = zipfile.ZipInfo(info.filename, date_time=when.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)
    path.write_bytes(buf.getvalue())


def seal_parquet(path):
    t = pq.read_table(path)
    t = t.replace_schema_metadata(None)
    pq.write_table(t, path, compression="snappy")


def seal(T: Path):
    for name, (author, title, when) in META.items():
        p = T / name
        if p.suffix == ".pdf":
            seal_pdf(p, author, title, when)
        else:
            seal_ooxml(p, author, when)
    for p in T.glob("*.parquet"):
        seal_parquet(p)
    ts = EXPORT.timestamp()
    for p in T.iterdir():
        os.utime(p, (ts, ts))
