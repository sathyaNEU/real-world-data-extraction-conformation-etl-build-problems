"""Container hygiene: in-fiction authors and dates inside every binary, one export time on the folder, and the two
upload archives."""
import datetime as dt
import io
import os
import re
import zipfile
from pathlib import Path

from pypdf import PdfReader, PdfWriter

import docs
import pack
import world as W

META = {
    docs.F_METHOD: ("Office of Revenue Analysis", "Lodging Tax Revenue Variance Statement: Standing Procedure",
                    dt.datetime(2023, 3, 14, 10, 5)),
    docs.F_STATEMENTS: ("Office of Revenue Analysis", "Certified Lodging Tax Variance Statements FY2024 and FY2025",
                        dt.datetime(2025, 9, 9, 8, 40)),
    pack.F_APPENDIX: ("Office of Revenue Analysis", "", dt.datetime(2025, 9, 8, 17, 12)),
}
EXPORT = W.EXTRACT_DATE
DECK_SENT = dt.datetime(2026, 9, 8, 16, 45)


def _cdt(t):
    def nth_sunday(y, m, n):
        d = dt.date(y, m, 1)
        d += dt.timedelta(days=(6 - d.weekday()) % 7)
        return d + dt.timedelta(weeks=n - 1)
    return dt.datetime.combine(nth_sunday(t.year, 3, 2), dt.time(2)) <= t < \
        dt.datetime.combine(nth_sunday(t.year, 11, 1), dt.time(2))


def _pdfdate(t):
    return t.strftime("D:%Y%m%d%H%M%S") + ("-05'00'" if _cdt(t) else "-06'00'")


def seal_pdf(path, author, title, when):
    r = PdfReader(str(path))
    w = PdfWriter()
    for pg in r.pages:
        w.add_page(pg)
    w.add_metadata({"/Author": author, "/Creator": "Microsoft Word", "/Producer": "Microsoft Word", "/Title": title,
                    "/CreationDate": _pdfdate(when), "/ModDate": _pdfdate(when)})
    buf = io.BytesIO()
    w.write(buf)
    path.write_bytes(buf.getvalue())


def seal_ooxml(path, author, when, app_name="Microsoft Excel"):
    src = zipfile.ZipFile(path)
    items = [(i, src.read(i.filename)) for i in src.infolist()]
    src.close()
    stamp = (when + dt.timedelta(hours=5 if _cdt(when) else 6)).strftime("%Y-%m-%dT%H:%M:%SZ")
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
           '<Application>%s</Application></Properties>' % app_name).encode()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for info, data in items:
            if info.filename == "docProps/thumbnail.jpeg":
                continue
            if info.filename == "docProps/core.xml":
                data = core
            elif info.filename == "docProps/app.xml":
                data = app
            elif info.filename == "_rels/.rels":
                data = re.sub(rb'<Relationship [^>]*Target="docProps/thumbnail.jpeg"[^>]*/>', b"", data)
            zi = zipfile.ZipInfo(info.filename, date_time=when.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)
    path.write_bytes(buf.getvalue())


def stamp_dir(T, when):
    ts = when.timestamp()
    for pth in Path(T).iterdir():
        os.utime(pth, (ts, ts))


def seal(T: Path):
    T = Path(T)
    for name, (author, title, when) in META.items():
        pth = T / name
        if pth.suffix == ".pdf":
            seal_pdf(pth, author, title, when)
        else:
            seal_ooxml(pth, author, when)
    stamp_dir(T, EXPORT)


def bundle(root: Path):
    """The two upload archives, cut last: flat, members in name order, stamped with the export time and the deck's
    date."""
    root = Path(root)
    for name, src, when in (("target.zip", root / "target", EXPORT), ("golden.zip", root / "golden", DECK_SENT)):
        with zipfile.ZipFile(root / name, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted((p for p in src.iterdir() if p.is_file()), key=lambda p: p.name.lower()):
                zi = zipfile.ZipInfo(f.name, date_time=when.timetuple()[:6])
                zi.compress_type = zipfile.ZIP_DEFLATED
                zi.external_attr = 0o644 << 16
                z.writestr(zi, f.read_bytes())
