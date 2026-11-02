"""Shared helpers: deterministic writers (csv, jsonl, xlsx, docx, pdf) and paths."""
import csv
import io
import json
import os
import re
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
REPO = os.path.dirname(TASK)
FIXED_ZIP_TIME = (2026, 11, 16, 9, 0, 0)


def write_csv(path, header, rows, sep=",", crlf=True):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=sep, lineterminator="\r\n" if crlf else "\n", quoting=csv.QUOTE_MINIMAL)
        w.writerow(header)
        for r in rows:
            w.writerow(["" if v is None else str(v) for v in r])


def write_jsonl(path, records):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n")


def normalise_zip(path, when=FIXED_ZIP_TIME, stamp=None):
    """Rewrite an OOXML zip with fixed entry times and fixed core-property dates so builds are byte-identical."""
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    if stamp:
        fixed = []
        for name, data in items:
            if name == "docProps/core.xml":
                s = data.decode("utf-8")
                s = re.sub(r"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", r"\g<1>%s\g<2>" % stamp, s)
                s = re.sub(r"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", r"\g<1>%s\g<2>" % stamp, s)
                data = s.encode("utf-8")
            fixed.append((name, data))
        items = fixed
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in items:
            zi = zipfile.ZipInfo(name, date_time=when)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)
    with open(path, "wb") as f:
        f.write(buf.getvalue())


def save_workbook(wb, path, created, creator):
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.created = created
    wb.properties.modified = created
    wb.properties.title = None
    wb.save(path)
    normalise_zip(path, stamp=created.strftime("%Y-%m-%dT%H:%M:%SZ"))


def save_docx(doc, path, created, creator):
    cp = doc.core_properties
    cp.author = creator
    cp.last_modified_by = creator
    cp.created = created
    cp.modified = created
    cp.revision = 1
    cp.title = ""
    cp.comments = ""
    doc.save(path)
    normalise_zip(path, stamp=created.strftime("%Y-%m-%dT%H:%M:%SZ"))


def pdf_invariant():
    from reportlab import rl_config
    rl_config.invariant = 1
    rl_config.pageCompression = 1


def fmt_int(n):
    return "{:,}".format(int(n))
