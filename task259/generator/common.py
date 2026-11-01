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


def normalise_zip(path, modified="2026-10-22T16:05:00Z", application=None):
    """Rewrite an xlsx or docx so its bytes do not depend on the clock: fixed member times, same member order, the
    document's own modified stamp, and the producing system's name in place of the writer library's."""
    import re
    with zipfile.ZipFile(path, "r") as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    fixed = []
    for name, data in items:
        if name == "docProps/core.xml":
            txt = data.decode("utf-8")
            txt = re.sub(r"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", r"\g<1>%s\g<2>" % modified, txt)
            data = txt.encode("utf-8")
        if name == "docProps/app.xml" and application:
            txt = data.decode("utf-8")
            txt = re.sub(r"<Application>[^<]*</Application>", "<Application>%s</Application>" % application, txt)
            txt = re.sub(r"<AppVersion>[^<]*</AppVersion>", "<AppVersion>16.0300</AppVersion>", txt)
            data = txt.encode("utf-8")
        fixed.append((name, data))
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for name, data in fixed:
            zi = zipfile.ZipInfo(name, date_time=EXPORT_DATE)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)
    os.replace(tmp, path)


def scrub_pdf(path, stamp, producer):
    """Equal-length substitutions so the xref offsets stand: the writer's header comment, its producer string and its
    fixed placeholder dates become the publishing office's own (surplus as whitespace between tokens)."""
    raw = open(path, "rb").read()
    head = b" ReportLab Generated PDF document (opensource)"
    if head in raw:
        # the binary marker after the second line's % stays; only the comment text after it changes
        new = b" " + producer.encode("latin-1")
        raw = raw.replace(head, new + b" " * (len(head) - len(new)), 1)
    old_p = b"/Producer (ReportLab PDF Library - \\(opensource\\))"
    if old_p in raw:
        new = b"/Producer (" + producer.encode("latin-1") + b")"
        raw = raw.replace(old_p, new + b" " * (len(old_p) - len(new)), 1)
    tail = b"% ReportLab generated PDF document -- digest (opensource)"
    if tail in raw:
        new = b"% " + producer.encode("latin-1")
        raw = raw.replace(tail, new + b" " * (len(tail) - len(new)), 1)
    raw = raw.replace(b"D:20000101000000+00'00'", ("D:%s" % stamp).encode("latin-1"))
    open(path, "wb").write(raw)


def set_mtime(root):
    for dp, dn, fn in os.walk(root):
        for f in fn:
            os.utime(os.path.join(dp, f), (FIXED_TS, FIXED_TS))


def xlsx_props(wb, creator, title=None, created=(2026, 10, 22, 16, 5)):
    import datetime
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.title = title
    wb.properties.created = datetime.datetime(*created)
    wb.properties.modified = datetime.datetime(*created)


def docx_props(doc, author, title, created=(2026, 10, 22, 15, 40), modified=(2026, 10, 22, 15, 40)):
    import datetime
    cp = doc.core_properties
    cp.author = author
    cp.last_modified_by = author
    cp.title = title
    cp.comments = ""
    cp.keywords = ""
    cp.subject = ""
    cp.created = datetime.datetime(*created)
    cp.modified = datetime.datetime(*modified)
    cp.revision = 3
