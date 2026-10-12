"""Container hygiene: in-fiction authors and dates in every binary's metadata, one export time on the folder."""
import datetime as dt
import io
import os
import zipfile
from pathlib import Path

from pypdf import PdfReader, PdfWriter

META = {
    "new_office_brief_stage2.pdf": ("Workplace Planning", "New office workplace brief, Rev C",
                                    dt.datetime(2026, 10, 2, 16, 20)),
    "room_utilisation_close_outs_fy2026.xlsx": ("Kristie Morgan", "", dt.datetime(2026, 10, 2, 11, 5)),
    "room_register.xlsx": ("Kristie Morgan", "", dt.datetime(2026, 10, 1, 15, 48)),
    "staff_directory_fy2026.xlsx": ("HR Systems", "", dt.datetime(2026, 10, 1, 9, 31)),
}
EXPORT = dt.datetime(2026, 10, 2, 17, 45)


def _pdfdate(t):
    return t.strftime("D:%Y%m%d%H%M%S-04'00'")


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
           '<Application>Microsoft Excel</Application></Properties>').encode()
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


def seal(T: Path):
    for name, (author, title, when) in META.items():
        p = T / name
        if p.suffix == ".pdf":
            seal_pdf(p, author, title, when)
        else:
            seal_ooxml(p, author, when)
    ts = EXPORT.timestamp()
    for p in T.iterdir():
        os.utime(p, (ts, ts))


def bundle(root: Path):
    """The two upload archives, flat, members in name order, stamped with the export time and the memo's date."""
    import zipfile
    for name, src, when in (("target.zip", root / "target", EXPORT),
                            ("golden.zip", root / "golden", dt.datetime(2026, 10, 9, 10, 40))):
        with zipfile.ZipFile(root / name, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(src.iterdir(), key=lambda f: f.name.lower()):
                zi = zipfile.ZipInfo(f.name, date_time=when.timetuple()[:6])
                zi.compress_type = zipfile.ZIP_DEFLATED
                zi.external_attr = 0o644 << 16
                z.writestr(zi, f.read_bytes())
