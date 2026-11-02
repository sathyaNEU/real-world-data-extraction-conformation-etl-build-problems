"""Make Office zip containers byte-stable: fixed entry times, sorted entries, scrubbed core properties."""
import io
import re
import zipfile

FIXED = (2026, 10, 16, 17, 40, 0)


def normalise(path, creator="Tawi Bank Limited", app=None):
    with open(path, "rb") as f:
        data = f.read()
    zin = zipfile.ZipFile(io.BytesIO(data))
    out = io.BytesIO()
    zout = zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED)
    names = zin.namelist()
    # keep [Content_Types].xml first, then the rest in a stable order
    order = [n for n in names if n == "[Content_Types].xml"] + sorted(n for n in names if n != "[Content_Types].xml")
    for n in order:
        b = zin.read(n)
        if n == "docProps/core.xml":
            s = b.decode("utf-8")
            s = re.sub(r"<dc:creator>.*?</dc:creator>", "<dc:creator>%s</dc:creator>" % creator, s)
            s = re.sub(r"<cp:lastModifiedBy>.*?</cp:lastModifiedBy>", "<cp:lastModifiedBy>%s</cp:lastModifiedBy>"
                       % creator, s)
            s = re.sub(r"<dcterms:created([^>]*)>.*?</dcterms:created>",
                       r"<dcterms:created\1>2026-10-16T14:40:00Z</dcterms:created>", s)
            s = re.sub(r"<dcterms:modified([^>]*)>.*?</dcterms:modified>",
                       r"<dcterms:modified\1>2026-10-16T14:40:00Z</dcterms:modified>", s)
            s = re.sub(r"<cp:revision>.*?</cp:revision>", "<cp:revision>1</cp:revision>", s)
            b = s.encode("utf-8")
        if n == "docProps/app.xml" and app:
            s = b.decode("utf-8")
            s = re.sub(r"<Application>.*?</Application>", "<Application>%s</Application>" % app, s)
            s = re.sub(r"<AppVersion>.*?</AppVersion>", "", s)
            b = s.encode("utf-8")
        zi = zipfile.ZipInfo(n, date_time=FIXED)
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.external_attr = 0o600 << 16
        zout.writestr(zi, b)
    zout.close()
    with open(path, "wb") as f:
        f.write(out.getvalue())
