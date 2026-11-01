"""Deterministic writers shared by the pack and the golden deliverables."""
import io
import os
import zipfile

FIXED_ZIP_TIME = (2026, 11, 17, 6, 0, 0)


def write_text(path, text, encoding="utf-8"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding=encoding, newline="") as f:
        f.write(text)


def normalize_zip(path):
    """Rewrite an OOXML container with fixed entry times and order so two builds are byte-identical."""
    import re
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    fixed = []
    for name, data in items:
        if name == "docProps/core.xml":
            txt = data.decode("utf-8")
            txt = re.sub(r"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", r"\g<1>2026-11-17T06:00:00Z\g<2>", txt)
            txt = re.sub(r"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", r"\g<1>2026-11-17T06:00:00Z\g<2>", txt)
            data = txt.encode("utf-8")
        fixed.append((name, data))
    items = fixed
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as out:
        for name, data in items:
            info = zipfile.ZipInfo(name, date_time=FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o600 << 16
            out.writestr(info, data)
    with open(path, "wb") as f:
        f.write(buf.getvalue())


def save_workbook(wb, path, creator="Regione - Osservatorio turistico"):
    import datetime as dt
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.created = dt.datetime(2026, 11, 17, 6, 0, 0)
    wb.properties.modified = dt.datetime(2026, 11, 17, 6, 0, 0)
    wb.properties.title = None
    wb.properties.description = None
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wb.save(path)
    normalize_zip(path)


def it_num(x, dec=0):
    """Italian number format: decimal comma, no thousands separator (as the tax offices' exports write it)."""
    s = ("%." + str(dec) + "f") % x
    return s.replace(".", ",")


def pdf_setup():
    from reportlab import rl_config
    rl_config.invariant = 1
    rl_config.pageCompression = 1
