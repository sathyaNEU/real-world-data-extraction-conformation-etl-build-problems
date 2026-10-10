"""Make office containers reproducible: fixed zip entry times, fixed PDF dates and document id."""
import hashlib
import re
import zipfile

FIXED = (2026, 9, 14, 9, 30, 0)


def normalize_zip(path, when=FIXED):
    stamp = "%04d-%02d-%02dT%02d:%02d:%02dZ" % when
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    with zipfile.ZipFile(path, "w") as z:
        for name, data in items:
            if name == "docProps/core.xml":
                data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                              lambda m: m.group(1) + stamp.encode() + m.group(2), data)
            if name == "docProps/app.xml":
                data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>Microsoft Excel</Application>", data)
                data = re.sub(rb"<AppVersion>3\.1</AppVersion>", b"<AppVersion>16.0300</AppVersion>", data)
            zi = zipfile.ZipInfo(name, date_time=when)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)


def normalize_pdf(path, stamp=b"D:20260318094100Z'", doc_id=b"6D1F4C0A92B83E57A1C4D90E3B7F2A61"):
    b = open(path, "rb").read()
    b = re.sub(rb"D:\d{14}Z'", lambda m: stamp[:len(m.group(0))], b)
    b = re.sub(rb"(/ID\s*\[\s*)<[0-9A-Fa-f]{32}>(\s*)<[0-9A-Fa-f]{32}>",
               lambda m: m.group(1) + b"<" + doc_id + b">" + m.group(2) + b"<" + doc_id + b">", b)
    b = re.sub(rb"/DocChecksum /[0-9A-F]{32}", b"/DocChecksum /" + doc_id[::-1], b)
    open(path, "wb").write(b)
