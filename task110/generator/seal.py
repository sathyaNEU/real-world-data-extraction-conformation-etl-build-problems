"""Container metadata set to the fiction, deterministically: OOXML docProps rewritten entry for entry
(every other entry's CRC asserted unchanged), PDF info dictionaries rewritten through pypdf with
the page text asserted unchanged, and every file's mtime set to the migration file's date."""
import datetime as dt
import io
import os
import re
import zipfile

from pypdf import PdfReader, PdfWriter

WRITERS = [b"openpyxl", b"Openpyxl", b"reportlab", b"ReportLab", b"matplotlib", b"Matplotlib", b"python-docx", b"pypdf"]

STAMPS = {   # file -> (author, ISO stamp)
    "YCB_asset_register_2026-10-02.xlsx": ("Wright Accounting Partners", "2026-10-02T15:41:07"),
    "YCB_trial_balance_30-09-2026.xlsx": ("Yacaaba Radiology", "2026-10-09T16:02:44"),
    "group_asset_class_mapping.xlsx": ("Ronald Lawrence", "2026-10-01T11:18:20"),
    "fa_load_specification.xlsx": ("Ronald Lawrence", "2026-06-18T09:42:55"),
    "YCB_FY2025_financial_statements_extract.pdf": ("Wright Accounting Partners", "2025-09-26T14:12:00"),
    "fa_migration_standard.pdf": ("Quandong Imaging Group", "2026-04-28T10:05:00"),
    "asset_verification_procedure.pdf": ("Quandong Imaging Group", "2026-07-29T16:30:00"),
    "RAY_count_sheet_07-10-2026.pdf": ("RAY-MFD", "2026-10-07T15:42:19"),
}
MTIME = dt.datetime(2026, 10, 13, 10, 12, 0)


def seal_xlsx(path, author, stamp):
    iso = (stamp + "Z").encode()
    zt = tuple(int(x) for x in re.split("[-T:]", stamp))
    with zipfile.ZipFile(path) as zin:
        infos = zin.infolist()
        data = {i.filename: zin.read(i.filename) for i in infos}
        crc = {i.filename: i.CRC for i in infos}
    core = data["docProps/core.xml"]
    core = re.sub(rb"(<dc:creator[^>]*>)[^<]*(</dc:creator>)", rb"\g<1>" + author.encode() + rb"\g<2>", core)
    if b"<cp:lastModifiedBy" in core:
        core = re.sub(rb"(<cp:lastModifiedBy[^>]*>)[^<]*(</cp:lastModifiedBy>)", rb"\g<1>" + author.encode() + rb"\g<2>", core)
    core = re.sub(rb"(<dcterms:(?:created|modified)[^>]*>)[^<]*(</dcterms:(?:created|modified)>)", rb"\g<1>" + iso + rb"\g<2>", core)
    data["docProps/core.xml"] = core
    if "docProps/app.xml" in data:
        app = data["docProps/app.xml"]
        app = re.sub(rb"(<Application>)[^<]*(</Application>)", rb"\g<1>Microsoft Excel\g<2>", app)
        app = re.sub(rb"(<AppVersion>)[^<]*(</AppVersion>)", rb"\g<1>16.0300\g<2>", app)
        data["docProps/app.xml"] = app
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
        for i in infos:
            zi = zipfile.ZipInfo(i.filename, date_time=zt)
            zi.compress_type, zi.external_attr = zipfile.ZIP_DEFLATED, 0o600 << 16
            zout.writestr(zi, data[i.filename])
    with zipfile.ZipFile(io.BytesIO(buf.getvalue())) as chk:
        assert [i.filename for i in chk.infolist()] == [i.filename for i in infos], path
        for i in chk.infolist():
            if not i.filename.startswith("docProps/"):
                assert i.CRC == crc[i.filename], (path, i.filename)
        meta = b"".join(chk.read(n) for n in chk.namelist() if n.startswith("docProps/"))
        assert not any(wr in meta for wr in WRITERS), path
    with open(path, "wb") as fh:
        fh.write(buf.getvalue())


def seal_pdf(path, author, stamp, title=None):
    r = PdfReader(path)
    before = [p.extract_text() for p in r.pages]
    w = PdfWriter(clone_from=r)
    from zoneinfo import ZoneInfo
    off = dt.datetime.fromisoformat(stamp).replace(tzinfo=ZoneInfo("Australia/Sydney")).utcoffset()
    hh = int(off.total_seconds() // 3600)
    d = "D:" + stamp.replace("-", "").replace("T", "").replace(":", "") + "+%02d'00'" % hh
    meta = {"/Author": author, "/Creator": "Microsoft Word" if "count_sheet" not in path else "RICOH IM C3000",
            "/Producer": "Microsoft: Print To PDF" if "count_sheet" not in path else "RICOH IM C3000",
            "/CreationDate": d, "/ModDate": d}
    if title or r.metadata and r.metadata.get("/Title"):
        meta["/Title"] = title or r.metadata.get("/Title")
    w.metadata = None
    w.add_metadata(meta)
    w._ID = None
    buf = io.BytesIO()
    w.write(buf)
    b = buf.getvalue()
    for wr in WRITERS:
        b = b  # writers are checked below
    assert not any(wr in b for wr in WRITERS), (path, [wr for wr in WRITERS if wr in b])
    after = [p.extract_text() for p in PdfReader(io.BytesIO(b)).pages]
    assert after == before, path
    with open(path, "wb") as fh:
        fh.write(b)


def touch(path, when=MTIME):
    t = when.timestamp()
    os.utime(path, (t, t))


def seal_target(target, files):
    for name in os.listdir(target):
        p = os.path.join(target, name)
        if name in STAMPS:
            author, stamp = STAMPS[name]
            if name.endswith(".xlsx"):
                seal_xlsx(p, author, stamp)
            elif name.endswith(".pdf"):
                seal_pdf(p, author, stamp)
        touch(p)


def seal_deliverables(out):
    for name in os.listdir(out):
        p = os.path.join(out, name)
        if name.endswith(".docx"):
            seal_docx(p, "Cynthia Rice", "2026-10-23T17:05:00")
        touch(p, dt.datetime(2026, 10, 23, 17, 5, 0))


def seal_docx(path, author, stamp):
    iso = (stamp + "Z").encode()
    zt = tuple(int(x) for x in re.split("[-T:]", stamp))
    with zipfile.ZipFile(path) as zin:
        infos = zin.infolist()
        data = {i.filename: zin.read(i.filename) for i in infos}
    core = data["docProps/core.xml"]
    core = re.sub(rb"(<dc:creator[^>]*>)[^<]*(</dc:creator>)", rb"\g<1>" + author.encode() + rb"\g<2>", core)
    if b"<cp:lastModifiedBy" in core:
        core = re.sub(rb"(<cp:lastModifiedBy[^>]*>)[^<]*(</cp:lastModifiedBy>)", rb"\g<1>" + author.encode() + rb"\g<2>", core)
    core = re.sub(rb"(<dcterms:(?:created|modified)[^>]*>)[^<]*(</dcterms:(?:created|modified)>)", rb"\g<1>" + iso + rb"\g<2>", core)
    core = re.sub(rb"(<cp:revision>)[^<]*(</cp:revision>)", rb"\g<1>4\g<2>", core)
    core = re.sub(rb"(<dc:description[^>]*>)[^<]*(</dc:description>)", rb"\g<1>\g<2>", core)
    data["docProps/core.xml"] = core
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
        for i in infos:
            zi = zipfile.ZipInfo(i.filename, date_time=zt)
            zi.compress_type, zi.external_attr = zipfile.ZIP_DEFLATED, 0o600 << 16
            zout.writestr(zi, data[i.filename])
    with open(path, "wb") as fh:
        fh.write(buf.getvalue())
