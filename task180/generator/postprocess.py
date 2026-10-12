"""Make the containers reproducible and true to the fiction: office files carry their owner and their own saved
stamps, not the writing library and the build clock; PDFs carry their issue date and no library banner. Every
substitution keeps byte lengths where the format needs it."""
import re
import zipfile

APP = {".xlsx": ("Microsoft Excel", "16.0300"), ".docx": ("Microsoft Office Word", "16.0000")}


def normalize_ooxml(path, creator, last_by, created, modified, title=None, company="The Agency"):
    """created and modified as ISO stamps (UTC, ending Z). Entries keep their names and order; every entry gets the
    1980 stamp Office writes, so two builds of the same content are byte-identical."""
    ext = path[path.rfind("."):]
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    app_name, app_ver = APP[ext]
    out = []
    for name, data in items:
        if name == "docProps/core.xml":
            t = ("<dc:title>%s</dc:title>" % title) if title else ""
            data = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
                    '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
                    'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
                    'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
                    '%s<dc:creator>%s</dc:creator><cp:lastModifiedBy>%s</cp:lastModifiedBy>'
                    '<dcterms:created xsi:type="dcterms:W3CDTF">%s</dcterms:created>'
                    '<dcterms:modified xsi:type="dcterms:W3CDTF">%s</dcterms:modified></cp:coreProperties>'
                    % (t, creator, last_by, created, modified)).encode()
        elif name == "docProps/app.xml":
            data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>" + app_name.encode() + b"</Application>",
                          data)
            data = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>" + app_ver.encode() + b"</AppVersion>", data)
            data = re.sub(rb"<Company>[^<]*</Company>", b"", data)
            data = data.replace(b"</Properties>", b"<Company>" + company.encode() + b"</Company></Properties>")
        out.append((name, data))
    with zipfile.ZipFile(path, "w") as z:
        for name, data in out:
            zi = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)


def normalize_pdf(path, stamp):
    """stamp: the in-fiction issue time as a PDF date of the invariant date's length, D:YYYYMMDDHHMMSS+HH'MM'."""
    b = open(path, "rb").read()
    n = len(b)
    inv = b"D:20000101000000+00'00'"
    assert len(stamp) == len(inv) and inv in b
    b = b.replace(inv, stamp)
    for banner in (b"ReportLab Generated PDF document (opensource)", b"ReportLab generated PDF document -- digest (opensource)",
                   b"ReportLab Generated PDF document http://www.reportlab.com"):
        b = b.replace(banner, b" " * len(banner))
    assert len(b) == n and b"ReportLab" not in b and b"reportlab" not in b
    open(path, "wb").write(b)
