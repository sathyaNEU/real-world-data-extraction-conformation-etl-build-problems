"""Container hygiene: in-fiction authors and dates in every binary's metadata, one export time on the folder."""
import datetime as dt
import io
import os
import re
import zipfile
from pathlib import Path

from pypdf import PdfReader, PdfWriter

META = {
    "missed_appointment_review_procedure_FS-07.pdf": ("Field Performance", "FS-07 Missed appointment review",
                                                     dt.datetime(2025, 1, 6, 9, 30)),
    "field_working_time_policy_HR-FS-03.pdf": ("People Services", "HR-FS-03 Field working time",
                                              dt.datetime(2025, 4, 14, 11, 10)),
    "customer_service_standards_2026_extract.pdf": ("Customer Experience", "Customer Service Standards 2026 (extract)",
                                                   dt.datetime(2026, 2, 2, 14, 5)),
    "pathline_4.2_release_note.pdf": ("Planning Systems", "Pathline Scheduler 4.2 release note",
                                      dt.datetime(2026, 6, 24, 16, 40)),
    "field_review_2026-07-23_notes.docx": ("Gillian Sanderson", "", dt.datetime(2026, 7, 23, 15, 22)),
    "patch_boundaries_from_2026-08-01.docx": ("Ryan Webster", "", dt.datetime(2026, 7, 9, 11, 4)),
    "ooh_desk_callouts_2025-07_2026-10.xlsx": ("OOH Desk", "", dt.datetime(2026, 10, 5, 8, 12)),
    "field_workforce_register.xlsx": ("People Services", "", dt.datetime(2026, 10, 5, 9, 3)),
}
EXPORT = dt.datetime(2026, 10, 5, 17, 20)


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
           '<Application></Application></Properties>').encode()
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
