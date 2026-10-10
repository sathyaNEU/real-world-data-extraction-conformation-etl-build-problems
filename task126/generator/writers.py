"""Deterministic writers (the house pattern). Every OOXML file is repacked with fixed entry times after the producer scrub;
every PDF is written with ReportLab's invariant mode and then scrubbed at equal byte length; parquet,
csv, sqlite, txt and eml are written byte-stable. File times are set to one in-fiction date at the end."""
import csv
import datetime as dt
import importlib.util
import io
import os
import sqlite3
import zipfile
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
SCRUB_PATH = REPO / ".claude/skills/reduce-house-fixes/scripts/scrub_producer_metadata.py"
_spec = importlib.util.spec_from_file_location("scrub_producer_metadata", SCRUB_PATH)
SCRUB = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(SCRUB)

FLOOR, CEILING = "2018-01-01", "2026-11-23"


def write_csv(path, rows, columns):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(columns)
        for r in rows:
            w.writerow(["" if r.get(c) is None else r.get(c) for c in columns])
    return len(rows)


def write_parquet(path, columns, types, rows, row_group=100_000):
    """rows: a list of dicts, or a dict of column lists."""
    arrays = []
    for c, t in zip(columns, types):
        vals = rows[c] if isinstance(rows, dict) else [r[c] for r in rows]
        if t == "ts":
            arr = pa.array([None if v in ("", None) else dt.datetime.strptime(v, "%Y-%m-%d %H:%M") for v in vals],
                           pa.timestamp("s"))
        elif t == "date":
            arr = pa.array([None if v in ("", None) else dt.date.fromisoformat(v) for v in vals], pa.date32())
        elif t == "float":
            arr = pa.array([None if v in ("", None) else float(v) for v in vals], pa.float64())
        elif t == "int":
            arr = pa.array([None if v in ("", None) else int(v) for v in vals], pa.int32())
        else:
            arr = pa.array([None if v in ("", None) else str(v) for v in vals], pa.string())
        arrays.append(arr)
    table = pa.Table.from_arrays(arrays, names=columns).replace_schema_metadata(None)
    pq.write_table(table, str(path), compression="zstd", compression_level=9, row_group_size=row_group, write_statistics=True,
                   use_dictionary=True, store_schema=False)
    return table.num_rows


def repack_ooxml(path, when):
    """Rewrite the archive with the same entries in the same order and a fixed entry time."""
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        data = [(i.filename, z.read(i.filename), i.compress_type) for i in infos]
    tmp = str(path) + ".tmp"
    with zipfile.ZipFile(tmp, "w") as out:
        for name, blob, ct in data:
            zi = zipfile.ZipInfo(name, date_time=when.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            zi.create_system = 0
            out.writestr(zi, blob)
    os.replace(tmp, path)


def scrub_ooxml(path, producer, when):
    stamp = when.strftime("%Y-%m-%d")
    SCRUB.scrub_ooxml(str(path), producer, stamp, FLOOR, CEILING)
    repack_ooxml(path, when)


def scrub_pdf(path, producer, when):
    stamp = when.strftime("%Y-%m-%d")
    SCRUB.scrub_pdf(str(path), producer, stamp, FLOOR, CEILING)
    plain_pdf_comments(path)


def plain_pdf_comments(path):
    """Replace the writer's header comment with the usual binary marker and drop the comment inside the trailer,
    then shift the cross-reference table by the bytes removed, so the file carries no writer banner at all."""
    import re
    b = open(path, "rb").read()
    assert b.startswith(b"%PDF-1.4\n%")
    end = b.index(b"\n", 9) + 1
    marker = b"%\xe2\xe3\xcf\xd3\n"
    shift = (end - 9) - len(marker)
    b = b[:9] + marker + b[end:]
    xref = b.rindex(b"\nxref\n") + 1
    head, tail = b[:xref], b[xref:]
    tail = re.sub(rb"(\d{10}) (\d{5}) n ", lambda m: b"%010d %s n " % (int(m.group(1)) - shift, m.group(2)), tail)
    tail = re.sub(rb"\n%(?!%EOF)[^\n]*\n", b"\n", tail)
    tail = re.sub(rb"startxref\n(\d+)\n", lambda m: b"startxref\n%d\n" % (int(m.group(1)) - shift), tail)
    b = head + tail
    assert b.count(b"\n%") == 2 and b.endswith(b"%%EOF\n"), "a comment line left in the PDF"
    open(path, "wb").write(b)


# ---------------------------------------------------------------------------------------- docx
def write_docx(path, title, blocks, author, when, producer, org="Morvane Patent Office"):
    from docx import Document
    from docx.shared import Pt, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10.5)
    for s in doc.sections:
        s.left_margin = s.right_margin = Cm(2.2)
        s.top_margin = s.bottom_margin = Cm(2.0)
    hdr = doc.sections[0].header.paragraphs[0]
    hdr.text = org
    hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p = doc.add_paragraph()
    run = p.add_run(title)
    run.bold = True
    run.font.size = Pt(14)
    for kind, val in blocks:
        if kind == "meta":
            q = doc.add_paragraph()
            r = q.add_run(val)
            r.italic = True
            r.font.size = Pt(9.5)
        elif kind == "h":
            q = doc.add_paragraph()
            r = q.add_run(val)
            r.bold = True
            r.font.size = Pt(11)
        elif kind == "p":
            doc.add_paragraph(val)
        elif kind == "table":
            t = doc.add_table(rows=len(val), cols=len(val[0]))
            t.style = "Table Grid"
            for i, row in enumerate(val):
                for j, cell in enumerate(row):
                    t.cell(i, j).text = cell
                    if i == 0:
                        for rr in t.cell(i, j).paragraphs[0].runs:
                            rr.bold = True
        elif kind == "foot":
            ft = doc.sections[0].footer.paragraphs[0]
            ft.text = val
            for rr in ft.runs:
                rr.font.size = Pt(8)
    cp = doc.core_properties
    cp.author = author
    cp.last_modified_by = author
    cp.title = title
    cp.comments = ""
    cp.subject = ""
    cp.keywords = ""
    cp.category = ""
    cp.revision = 4
    cp.created = when - dt.timedelta(days=9, hours=3)
    cp.modified = when
    doc.save(str(path))
    SCRUB.scrub_ooxml(str(path), producer, when.strftime("%Y-%m-%d"), FLOOR, CEILING)
    tidy_word_package(path, minutes=52)
    repack_ooxml(path, when)


def tidy_word_package(path, minutes, pages=1):
    """A package as Word 2016 saves it: no template thumbnail, no customXml item, no Word 2010 stylesWithEffects
    part, and docProps/app.xml statistics counted from the body text with a non-zero editing time."""
    import html
    import math
    import re
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        data = {i.filename: z.read(i.filename) for i in infos}
    drop = [n for n in data if n == "docProps/thumbnail.jpeg" or n.startswith("customXml/")
            or n == "word/stylesWithEffects.xml"]
    for n in drop:
        data.pop(n)
    data["_rels/.rels"] = re.sub(rb'<Relationship [^>]*Target="docProps/thumbnail.jpeg"/>', b"", data["_rels/.rels"])
    rels = "word/_rels/document.xml.rels"
    data[rels] = re.sub(rb'<Relationship [^>]*Target="(?:\.\./customXml/[^"]*|stylesWithEffects.xml)"/>', b"", data[rels])
    ct = data["[Content_Types].xml"]
    ct = ct.replace(b'<Default Extension="jpeg" ContentType="image/jpeg"/>', b"")
    ct = re.sub(rb'<Override PartName="/(?:customXml/[^"]*|word/stylesWithEffects.xml)"[^>]*/>', b"", ct)
    data["[Content_Types].xml"] = ct
    body = data["word/document.xml"].decode("utf-8")
    paras = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", body, flags=re.S):
        txt = html.unescape("".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", p)))
        if txt.strip():
            paras.append(txt)
    stats = (("TotalTime", minutes), ("Pages", pages), ("Words", sum(len(p.split()) for p in paras)),
             ("Characters", sum(len(re.sub(r"\s", "", p)) for p in paras)),
             ("Lines", sum(max(1, math.ceil(len(p) / 90)) for p in paras)), ("Paragraphs", len(paras)),
             ("CharactersWithSpaces", sum(len(p) for p in paras)))
    app = data["docProps/app.xml"].decode("utf-8")
    for tag, val in stats:
        app = re.sub(r"<%s>\d+</%s>" % (tag, tag), "<%s>%d</%s>" % (tag, val, tag), app)
    app = re.sub(r"<AppVersion>[^<]*</AppVersion>", "<AppVersion>16.0000</AppVersion>", app)
    data["docProps/app.xml"] = app.encode("utf-8")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as out:
        for i in infos:
            if i.filename in data:
                out.writestr(i.filename, data[i.filename])


# ---------------------------------------------------------------------------------------- pdf
def write_pdf(path, title, sub, by, blocks, author, when, producer, fields=None):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from xml.sax.saxutils import escape
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=12.5, spaceAfter=5)
    small = ParagraphStyle("s", parent=body, fontSize=8.5, leading=10.5)
    h1 = ParagraphStyle("h1", parent=body, fontName="Helvetica-Bold", fontSize=13, leading=16, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=body, fontName="Helvetica-Bold", fontSize=10.5, leading=13, spaceBefore=6)
    meta = ParagraphStyle("m", parent=body, fontName="Helvetica-Oblique", fontSize=9, leading=11)
    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=2.1 * cm, rightMargin=2.1 * cm, topMargin=1.8 * cm,
                            bottomMargin=1.8 * cm, title=title, author=author, subject="", creator=author,
                            invariant=1)
    story = [Paragraph(escape(title), h1)]
    if sub:
        story.append(Paragraph(escape(sub), meta))
    if by:
        story.append(Paragraph(escape(by), meta))
    story.append(Spacer(1, 6))
    for kind, val in blocks:
        if kind == "h":
            story.append(Paragraph(escape(val), h2))
        elif kind == "p":
            story.append(Paragraph(escape(val), body))
        elif kind == "small":
            story.append(Paragraph(escape(val), small))
        elif kind == "table":
            data = [[Paragraph(escape(str(c)), small) for c in row] for row in val["rows"]]
            t = Table(data, colWidths=val.get("widths"), repeatRows=1)
            t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                                   ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.9, 0.9, 0.9)),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            story.append(t)
            story.append(Spacer(1, 6))
    doc.build(story)
    scrub_pdf(path, producer, when)


# ---------------------------------------------------------------------------------------- xlsx
def xlsx_book(path, title, author, company, when):
    import xlsxwriter
    wb = xlsxwriter.Workbook(str(path), {"strings_to_numbers": False})
    wb.set_properties({"title": title, "author": author, "company": company, "created": when})
    return wb


def close_xlsx(wb, path, producer, when):
    wb.close()
    scrub_ooxml(path, producer, when)


# ---------------------------------------------------------------------------------------- sqlite
def write_sqlite(path, schema, tables):
    if os.path.exists(path):
        os.remove(path)
    con = sqlite3.connect(str(path))
    con.execute("PRAGMA page_size=4096")
    con.execute("PRAGMA journal_mode=OFF")
    for ddl in schema:
        con.execute(ddl)
    for name, cols, rows in tables:
        con.executemany("INSERT INTO %s (%s) VALUES (%s)" % (name, ",".join(cols), ",".join("?" * len(cols))), rows)
    con.commit()
    con.execute("VACUUM")
    con.close()


def set_mtimes(root, when):
    ts = when.timestamp()
    for p in sorted(Path(root).rglob("*")):
        if p.is_file():
            os.utime(p, (ts, ts))


def write_text(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def write_json(path, obj):
    import json
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def set_mtime(path, when):
    ts = when.timestamp()
    os.utime(path, (ts, ts))
