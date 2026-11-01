"""Shared helpers: deterministic writers for csv, xlsx, docx and pdf, and the in-fiction export date."""
import csv
import io
import os
import zipfile

EXPORT_DATE = (2026, 10, 23, 9, 0, 0)       # every shipped file carries this as its modification time
EXPORT_ISO = "2026-10-23T09:00:00Z"
FIXED_TS = 1792746000                        # 2026-10-23 09:00:00 UTC as a unix time


def write_csv(path, header, rows, newline="\r\n"):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator=newline)
    w.writerow(header)
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())


def normalise_zip(path):
    """Rewrite an xlsx or docx so its bytes do not depend on the clock: fixed member times, same member order."""
    with zipfile.ZipFile(path, "r") as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for name, data in items:
            zi = zipfile.ZipInfo(name, date_time=EXPORT_DATE)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)
    os.replace(tmp, path)


def set_mtime(root):
    for dp, dn, fn in os.walk(root):
        for f in fn:
            os.utime(os.path.join(dp, f), (FIXED_TS, FIXED_TS))


def xlsx_props(wb, creator, title=None):
    import datetime
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.title = title
    wb.properties.created = datetime.datetime(2026, 10, 22, 16, 5, 0)
    wb.properties.modified = datetime.datetime(2026, 10, 22, 16, 5, 0)


def docx_props(doc, author, title):
    import datetime
    cp = doc.core_properties
    cp.author = author
    cp.last_modified_by = author
    cp.title = title
    cp.comments = ""
    cp.keywords = ""
    cp.subject = ""
    cp.created = datetime.datetime(2026, 10, 22, 15, 40, 0)
    cp.modified = datetime.datetime(2026, 10, 22, 15, 40, 0)
    cp.revision = 3
