"""File writers with fixed metadata so two builds give identical bytes."""
import io
import os
import zipfile
import datetime as dt

FIXED = (2026, 10, 19, 8, 12, 0)          # the compile time of the pack (Monday 19 October 2026, 08:12)
ISO_STAMP = "2026-10-19T07:12:00Z"         # the same moment in UTC
AUTHOR = "Larrowmede Medical Relief - epidemiology cell"


def write_bytes(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    ts = dt.datetime(*FIXED).timestamp()
    os.utime(path, (ts, ts))


def write_text(path, text, bom=False):
    data = text.encode("utf-8")
    if bom:
        data = b"\xef\xbb\xbf" + data
    write_bytes(path, data)


def normalise_ooxml(raw, creator=AUTHOR, title=None):
    """Repack an xlsx/docx with fixed entry times and fixed core properties."""
    zin = zipfile.ZipFile(io.BytesIO(raw))
    out = io.BytesIO()
    zout = zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED)
    for info in zin.infolist():
        data = zin.read(info.filename)
        if info.filename == "docProps/core.xml":
            t = "<dc:title>%s</dc:title>" % title if title else ""
            data = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                    '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
                    'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
                    'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
                    '%s<dc:creator>%s</dc:creator><cp:lastModifiedBy>%s</cp:lastModifiedBy>'
                    '<dcterms:created xsi:type="dcterms:W3CDTF">%s</dcterms:created>'
                    '<dcterms:modified xsi:type="dcterms:W3CDTF">%s</dcterms:modified></cp:coreProperties>'
                    % (t, creator, creator, ISO_STAMP, ISO_STAMP)).encode("utf-8")
        if info.filename == "docProps/app.xml":
            data = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                    '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
                    'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
                    '<Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>'
                    '<Company>Larrowmede Medical Relief</Company><AppVersion>16.0300</AppVersion></Properties>').encode("utf-8")
        zi = zipfile.ZipInfo(info.filename, date_time=FIXED)
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.external_attr = 0o600 << 16
        zout.writestr(zi, data)
    zout.close()
    return out.getvalue()


def save_workbook(wb, path, title=None):
    bio = io.BytesIO()
    wb.save(bio)
    write_bytes(path, normalise_ooxml(bio.getvalue(), title=title))


def pdf_bytes(build_fn, title, author=AUTHOR):
    """Run a reportlab story builder into fixed-metadata PDF bytes."""
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate
    from reportlab import rl_config
    rl_config.invariant = 1
    bio = io.BytesIO()
    doc = SimpleDocTemplate(bio, pagesize=A4, title=title, author=author, creator=author, producer=author,
                            subject=title, leftMargin=52, rightMargin=52, topMargin=56, bottomMargin=56)
    build_fn(doc)
    data = bio.getvalue()
    return data
