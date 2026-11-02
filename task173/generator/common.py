"""Byte-stable writing helpers."""
import io
import re
import zipfile

FIXED = (2026, 10, 31, 17, 40, 0)
STAMP = "2026-10-31T17:40:00Z"


def freeze_xlsx(path, author="Performance and Information"):
    src = zipfile.ZipFile(path)
    items = [(i.filename, src.read(i.filename)) for i in src.infolist()]
    src.close()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in items:
            if name == "docProps/core.xml":
                t = data.decode()
                t = re.sub(r"<dcterms:created[^>]*>[^<]*</dcterms:created>", '<dcterms:created xsi:type="dcterms:W3CDTF">%s</dcterms:created>' % STAMP, t)
                t = re.sub(r"<dcterms:modified[^>]*>[^<]*</dcterms:modified>", '<dcterms:modified xsi:type="dcterms:W3CDTF">%s</dcterms:modified>' % STAMP, t)
                t = re.sub(r"<dc:creator>[^<]*</dc:creator>", "<dc:creator>%s</dc:creator>" % author, t)
                t = re.sub(r"<cp:lastModifiedBy>[^<]*</cp:lastModifiedBy>", "<cp:lastModifiedBy>%s</cp:lastModifiedBy>" % author, t)
                data = t.encode()
            zi = zipfile.ZipInfo(name, FIXED)
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)
    open(path, "wb").write(buf.getvalue())
