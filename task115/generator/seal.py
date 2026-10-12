"""Seal the written files: in-fiction authors and dates inside every container, no writer's name,
reproducible bytes, file times set to each file's own date, and the two archives cut from the trees.

    python3 seal.py           # cut target.zip and golden.zip (after build.py, deliver.py and the checks)

build.py and deliver.py call seal_dir() on their own output, so a rebuild is sealed without this step."""
import datetime as dt
import os
import re
import sys
import time
import zipfile
from pathlib import Path

from docx import Document

ROOT = Path(__file__).resolve().parent.parent
OFFICE_EPOCH = (1980, 1, 1, 0, 0, 0)        # what Word and Excel write for every package entry
IRL = "+01'00'"                             # Irish summer time, to 25 October 2026

# file -> (author, department or producing team, in-fiction save time)
TARGET = {
    "TullanInsight_tea_store_week_2024W41-2026W40.csv": ("", "", dt.datetime(2026, 10, 5, 6, 40)),
    "tullan_tea_range_2026.csv": ("", "", dt.datetime(2026, 10, 5, 6, 41)),
    "big_deals_calendar_2024-2026.csv": ("", "", dt.datetime(2026, 9, 28, 10, 15)),
    "tullan_members_jan2026.xlsx": ("Tullan Grocers", "Member Services", dt.datetime(2026, 1, 12, 11, 20)),
    "tullan_area_structure_from_6_July_2026.docx": ("Martina Mulgrew", "Member Services",
                                                    dt.datetime(2026, 6, 22, 15, 5)),
    "member_news_2026.docx": ("Tullan Grocers", "Member Services", dt.datetime(2026, 8, 31, 12, 30)),
    "Big_Deals_Spring_2027_supplier_brief.docx": ("George Fenelon", "Buying", dt.datetime(2026, 9, 28, 9, 30)),
    "big_deals_review_tea_2025-26.pdf": ("Tullan Grocers", "Category Insights", dt.datetime(2026, 10, 6, 16, 10)),
    "tullan_own_brand_rrp_2026.pdf": ("Tullan Grocers", "Own Brand", dt.datetime(2025, 12, 15, 10, 0)),
    "TullanInsight_category_feed_v3_spec.pdf": ("Tullan Grocers", "Data Services", dt.datetime(2024, 3, 18, 14, 0)),
    "tullan_debit_notes_Delahunt_2026.xlsx": ("Tullan Grocers", "Finance", dt.datetime(2026, 10, 7, 17, 30)),
    "tullan_deal_funding_lines_Delahunt_2026.csv": ("", "", dt.datetime(2026, 10, 7, 17, 31)),
    "tullan_manual_returns_2026.csv": ("", "", dt.datetime(2026, 10, 6, 9, 0)),
    "delahunt_deal_reviews_2025-26.xlsx": ("Rebekah Masterson", "Revenue Growth", dt.datetime(2026, 4, 17, 15, 40)),
    "delahunt_commercial_thread_oct2026.txt": ("", "", dt.datetime(2026, 10, 7, 16, 45)),
    "README_tullan_spring_2027.txt": ("", "", dt.datetime(2026, 10, 8, 8, 50)),
}
GOLDEN = {
    "march_offer_paper.pdf": ("Tess Tuohey", "Revenue Growth", dt.datetime(2026, 10, 20, 17, 10)),
    "march_offer_workings.xlsx": ("Tess Tuohey", "Revenue Growth", dt.datetime(2026, 10, 20, 16, 55)),
}
SIGNATURES = [b"python-docx", b"openpyxl", b"Openpyxl", b"reportlab", b"ReportLab", b"matplotlib", b"Matplotlib"]


def iso(t):
    return (t - dt.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")        # Irish summer time to UTC


def pdfdate(t):
    return ("D:" + t.strftime("%Y%m%d%H%M%S") + IRL).encode()


def word_counts(path):
    d = Document(str(path))
    texts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for r in t.rows:
            for c in r.cells:
                texts.extend(p.text for p in c.paragraphs)
    joined = " ".join(texts)
    words = len(joined.split())
    chars = len(joined.replace(" ", ""))
    paras = sum(1 for x in texts if x.strip())
    return words, chars, len(joined), paras, max(1, round(words / 430 + 0.4)), max(paras, round(len(joined) / 85))


def seal_ooxml(path, author, when):
    ext = path.suffix.lower()
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        data = {i.filename: z.read(i.filename) for i in infos}
    drop = {n for n in data if n == "docProps/thumbnail.jpeg"}
    if drop:      # the writer's template thumbnail is a blank page, not this document
        data["_rels/.rels"] = re.sub(rb'<Relationship Id="rId\d+" Type="[^"]+/thumbnail" Target="docProps/thumbnail.jpeg"/>',
                                     b"", data["_rels/.rels"])
        data["[Content_Types].xml"] = data["[Content_Types].xml"].replace(
            b'<Default Extension="jpeg" ContentType="image/jpeg"/>', b"")
    core = data["docProps/core.xml"]
    core = re.sub(rb"<dc:creator([^>]*)>[^<]*</dc:creator>", lambda m: b"<dc:creator" + m.group(1) + b">" +
                  author.encode() + b"</dc:creator>", core)
    core = re.sub(rb"<dc:description>[^<]*</dc:description>", b"<dc:description/>", core)
    if b"lastModifiedBy" in core:
        core = re.sub(rb"<cp:lastModifiedBy\s*/>|<cp:lastModifiedBy>[^<]*</cp:lastModifiedBy>",
                      b"<cp:lastModifiedBy>" + author.encode() + b"</cp:lastModifiedBy>", core)
    else:
        core = core.replace(b"</cp:coreProperties>", b"<cp:lastModifiedBy>" + author.encode() +
                            b"</cp:lastModifiedBy></cp:coreProperties>")
    created = when - dt.timedelta(days=2, hours=3, minutes=12) if ext == ".docx" else when - dt.timedelta(hours=5)
    stamps = iter([iso(created).encode(), iso(when).encode()])
    core = re.sub(rb"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", lambda m: next(stamps), core)
    core = core.replace(b"<cp:revision>1</cp:revision>", b"<cp:revision>3</cp:revision>")
    data["docProps/core.xml"] = core
    app = data["docProps/app.xml"]
    if ext == ".xlsx":
        app = re.sub(rb"<Application>[^<]*</Application>", b"<Application>Microsoft Excel</Application>", app)
        app = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0300</AppVersion>", app)
    else:
        w, c, cs, p, pages, lines = word_counts(path)
        for tag, v in ((b"Application", b"Microsoft Office Word"), (b"AppVersion", b"16.0000"),
                       (b"Pages", str(pages).encode()), (b"Words", str(w).encode()),
                       (b"Characters", str(c).encode()), (b"CharactersWithSpaces", str(cs).encode()),
                       (b"Paragraphs", str(p).encode()), (b"Lines", str(lines).encode()),
                       (b"TotalTime", str(max(4, w // 45)).encode())):
            app = re.sub(rb"<" + tag + rb">[^<]*</" + tag + rb">", b"<" + tag + b">" + v + b"</" + tag + b">", app)
    data["docProps/app.xml"] = app
    tmp = path.with_suffix(path.suffix + ".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as out:
        for i in infos:
            if i.filename in drop:
                continue
            zi = zipfile.ZipInfo(i.filename, date_time=OFFICE_EPOCH)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0
            out.writestr(zi, data[i.filename])
    with zipfile.ZipFile(tmp) as chk:
        for i in chk.infolist():
            if not i.filename.startswith("docProps/") and i.filename not in ("_rels/.rels", "[Content_Types].xml"):
                assert chk.read(i.filename) == data[i.filename], i.filename
        meta = b"".join(chk.read(n) for n in chk.namelist() if n.startswith("docProps/"))
        assert not any(s in meta for s in SIGNATURES), path
    os.replace(tmp, path)


def seal_pdf(path, when):
    """reportlab runs with rl_config.invariant, so its dates and /ID are fixed placeholders: put the
    in-fiction save time in the dates at equal length and blank the writer's comment line."""
    b = path.read_bytes()
    n0 = len(b)
    placeholder = b"D:20000101000000+00'00'"
    assert b.count(placeholder) == 2, path
    b = b.replace(placeholder, pdfdate(when))
    hits = list(re.finditer(rb"^(%[^\n]*?)(ReportLab [Gg]enerated PDF document[^\n]*)$", b, re.M))
    assert len(hits) == 2, (path, len(hits))          # the header line and the trailer's digest line
    for m in hits:
        b = b[:m.start(2)] + b" " * (m.end(2) - m.start(2)) + b[m.end(2):]
    assert len(b) == n0 and not any(s in b for s in SIGNATURES), path
    path.write_bytes(b)


def seal_dir(folder, table):
    folder = Path(folder)
    names = sorted(p.name for p in folder.iterdir() if p.is_file())
    assert names == sorted(table), (set(names) ^ set(table))
    for name in names:
        p = folder / name
        author, dept, when = table[name]
        if p.suffix.lower() in (".docx", ".xlsx"):
            seal_ooxml(p, author, when)
        elif p.suffix.lower() == ".pdf":
            seal_pdf(p, when)
        ts = time.mktime(when.timetuple())
        os.utime(p, (ts, ts))


def cut(folder, table, archive):
    """A flat archive, one entry per file in name order, each dated with its file's own time."""
    folder = Path(folder)
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(table):
            zi = zipfile.ZipInfo(name, date_time=table[name][2].timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, (folder / name).read_bytes())
    with zipfile.ZipFile(archive) as z:
        assert z.namelist() == sorted(table)
        for name in table:
            assert z.read(name) == (folder / name).read_bytes(), name


if __name__ == "__main__":
    cut(ROOT / "target", TARGET, ROOT / "target.zip")
    cut(ROOT / "golden", GOLDEN, ROOT / "golden.zip")
    print("cut", ROOT / "target.zip", ROOT / "golden.zip")
