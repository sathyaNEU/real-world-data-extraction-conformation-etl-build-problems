"""Shared helpers: fixed timestamps, deterministic workbooks and PDFs."""
import io, os, re, zipfile, shutil
from datetime import datetime

FIXED_ZIP_TIME = (2026, 11, 20, 6, 0, 0)
FIXED_ISO = "2026-11-20T06:00:00Z"
ASOF = "2026-11-20"

def normalize_zip(path):
    """Rewrite an OOXML file so its members carry fixed times and fixed core-property dates."""
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as out:
        for name, data in sorted(items, key=lambda x: x[0]):
            if name == "docProps/app.xml":
                txt = data.decode("utf-8")
                txt = re.sub(r"<AppVersion>[^<]*</AppVersion>", "<AppVersion>16.0300</AppVersion>", txt)
                data = txt.encode("utf-8")
            if name == "docProps/core.xml":
                txt = data.decode("utf-8")
                txt = re.sub(r"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", r"\g<1>%s\g<2>" % FIXED_ISO, txt)
                txt = re.sub(r"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", r"\g<1>%s\g<2>" % FIXED_ISO, txt)
                data = txt.encode("utf-8")
            zi = zipfile.ZipInfo(name, date_time=FIXED_ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            out.writestr(zi, data)
    with open(path, "wb") as f:
        f.write(buf.getvalue())

def save_workbook(wb, path, creator):
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.created = datetime(2026, 11, 20, 6, 0, 0)
    wb.properties.modified = datetime(2026, 11, 20, 6, 0, 0)
    wb.save(path)
    normalize_zip(path)

def pdf_setup():
    from reportlab import rl_config
    rl_config.invariant = 1
    rl_config.pageCompression = 1

def write_csv(path, header, rows, newline="\r\n"):
    with open(path, "w", newline="") as f:
        f.write(",".join(header) + newline)
        for r in rows:
            f.write(",".join("" if v is None else str(v) for v in r) + newline)
