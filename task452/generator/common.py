"""Shared helpers: deterministic file writing (xlsx, pdf, zip) and paths."""
import io
import os
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
FIXED_ZIP_TIME = (2027, 1, 6, 9, 0, 0)


def normalise_zip(path, when=FIXED_ZIP_TIME):
    """Rewrite an OOXML zip with fixed entry times so two builds are byte-identical."""
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
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
    import datetime as dt
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.created = created
    wb.properties.modified = created
    wb.properties.title = None
    wb.save(path)
    normalise_zip(path)


def pdf_canvas_settings():
    from reportlab import rl_config
    rl_config.invariant = 1
    rl_config.pageCompression = 1


def write_csv(path, header, rows, sep=","):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(sep.join(header) + "\r\n")
        for r in rows:
            f.write(sep.join("" if v is None else str(v) for v in r) + "\r\n")
