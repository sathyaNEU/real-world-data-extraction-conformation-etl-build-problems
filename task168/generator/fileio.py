"""Deterministic writers: xlsx and pptx zips with fixed member times, PDFs with invariant ids, fixed mtimes."""
import datetime as dt
import os
import zipfile

FIXED_ZIP_TIME = (2025, 12, 12, 9, 0, 0)


APPNAME = {".xlsx": b"Microsoft Excel", ".pptx": b"Microsoft Office PowerPoint", ".docx": b"Microsoft Office Word"}


def _normalise_inner(data, when):
    """An embedded workbook (a chart's data sheet) rewritten with fixed member times and the parent's date."""
    import io
    import re
    stamp = ("%04d-%02d-%02dT%02d:%02d:%02dZ" % when).encode()
    src = zipfile.ZipFile(io.BytesIO(data))
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for i in src.infolist():
            b = src.read(i.filename)
            if i.filename == "docProps/core.xml":
                b = re.sub(rb"(<dcterms:(?:created|modified)[^>]*>)[^<]*(</dcterms:(?:created|modified)>)",
                           lambda x: x.group(1) + stamp + x.group(2), b)
            if i.filename == "docProps/app.xml":
                b = re.sub(rb"<Application>[^<]*</Application>", b"<Application>Microsoft Excel</Application>", b)
            zi = zipfile.ZipInfo(i.filename, date_time=when)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, b)
    return out.getvalue()


def normalise_zip(path, when=FIXED_ZIP_TIME):
    """Rewrite an OOXML zip with every member at one fixed time and in a stable order, the application named as the
    office suite the organisation uses."""
    import re
    ext = os.path.splitext(path)[1].lower()
    with zipfile.ZipFile(path) as z:
        members = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    fixed = []
    for name, data in members:
        if name == "docProps/core.xml":
            # the writer stamps the save time as modified; the document's own date is its created stamp
            m = re.search(rb"<dcterms:created[^>]*>([^<]*)</dcterms:created>", data)
            if m:
                data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                              lambda x: x.group(1) + m.group(1) + x.group(2), data)
        if name.endswith(".xlsx") and name.startswith("ppt/embeddings/"):
            data = _normalise_inner(data, when)
        if name == "docProps/app.xml":
            data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>" + APPNAME[ext] + b"</Application>", data)
            data = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0300</AppVersion>", data)
        fixed.append((name, data))
    members = fixed
    first = [m for m in members if m[0] == "[Content_Types].xml"]
    rest = [m for m in members if m[0] != "[Content_Types].xml"]
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in first + rest:
            zi = zipfile.ZipInfo(name, date_time=when)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)
    os.replace(tmp, path)


def fix_workbook_props(wb, title, creator, created, modified=None):
    wb.properties.title = title
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.created = created
    wb.properties.modified = modified or created
    wb.properties.description = None
    wb.properties.keywords = None


def set_mtime(path, when=dt.datetime(2025, 12, 12, 9, 0, 0)):
    ts = when.timestamp()
    os.utime(path, (ts, ts))


def fix_pdf(path, when):
    """Give a ReportLab PDF the document's own date and drop the library's comment lines, at equal byte length so
    the cross-reference table stays valid. when: a datetime in Rome time."""
    import re
    b = open(path, "rb").read()
    n0 = len(b)
    stamp = when.strftime("D:%Y%m%d%H%M%S").encode() + b"+01'00'"
    b = re.sub(rb"D:\d{14}[+-]\d\d'\d\d'", lambda m: stamp, b)

    def blank(m):
        line = m.group(0)
        return b"%" + b" " * (len(line) - 1)
    b = re.sub(rb"%[^\n]*[Rr]eport[Ll]ab[^\n]*", blank, b)
    assert len(b) == n0
    assert b"ReportLab" not in b and b"reportlab" not in b
    with open(path, "wb") as fh:
        fh.write(b)


SWEPT = None


def binary_is_clean(path):
    """True when the file read as text spells none of the tokens a document sweep treats as author vocabulary."""
    import re
    global SWEPT
    if SWEPT is None:
        SWEPT = re.compile(r"\b(?:xxx|todo|fixme|lorem|traps?|decoys?|rungs?|stump\w*|golden|rubric|claude|llm|"
                           r"openai|placeholder|synthetic|ladder|naive|distractor)\b", re.I)
    t = open(path, "rb").read().decode("utf-8", "ignore")
    return SWEPT.search(t) is None
