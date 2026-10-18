"""Make the containers reproducible and true to the fiction: office files carry their owner and
their own saved stamps rather than the writing library and the build clock, and PDFs carry their
issue date and no library banner. Every substitution keeps byte lengths where the format needs it."""
import hashlib
import os
import re
import zipfile

import world as W

XML_DECL = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
INVARIANT = b"D:20000101000000+00'00'"
STAMPS = {
    "treatment_operation_codes.xlsx": (W.PEOPLE["register_liaison"], "2026-07-01T08:12:00Z", "2026-07-01T08:31:00Z"),
    "recovery_attainment_2026.xlsx": (W.PEOPLE["head_collection"], "2027-02-09T07:41:00Z", "2027-02-11T16:04:00Z"),
}
PDF_STAMPS = {
    "national_waste_management_plan_targets.pdf": ("20231214103000", "20231214103000"),
    "bws_2026_design_and_weighting.pdf": ("20270116091500", "20270116094200"),
    "waste_statistics_2025_release.pdf": ("20260930080000", "20260930081700"),
    "collection_capacity_note_2027.pdf": ("20270209074500", "20270211160900"),
}
COMPANY = W.INSTITUTE


def normalize_ooxml(path, creator, created, modified, title=None):
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
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
                    % (t, creator, creator, created, modified)).encode()
        elif name == "docProps/app.xml":
            data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>Microsoft Excel</Application>", data)
            data = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0300</AppVersion>", data)
            if b"<Company>" not in data:
                data = data.replace(b"</Properties>", b"<Company>" + COMPANY.encode() + b"</Company></Properties>")
        out.append((name, data))
    with zipfile.ZipFile(path, "w") as z:
        for name, data in out:
            zi = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)


def normalize_pdf(path, created, modified):
    b = open(path, "rb").read()
    n = len(b)
    cre = ("D:%s+00'00'" % created).encode()
    mod = ("D:%s+00'00'" % modified).encode()
    assert len(cre) == len(mod) == len(INVARIANT), (len(cre), len(mod))
    assert b.count(INVARIANT) == 2, b.count(INVARIANT)
    b = b.replace(INVARIANT, cre, 1).replace(INVARIANT, mod, 1)
    for banner in (b"ReportLab Generated PDF document (opensource)",
                   b"ReportLab generated PDF document -- digest (opensource)"):
        b = b.replace(banner, b" " * len(banner))
    producer = rb"ReportLab PDF Library - \(opensource\)"
    if producer in b:
        stand_in = rb"PDFlib 9.3.1 \(Linux\)"
        b = b.replace(producer, stand_in + b" " * (len(producer) - len(stand_in)))
    for banner in (b"% ReportLab generated PDF document -- digest (opensource)",
                   b"% ReportLab generated PDF document (opensource)"):
        b = b.replace(banner, b"%" + b" " * (len(banner) - 1))
    tags = {}
    for m in re.finditer(rb"/([A-Z]{6})\+([A-Za-z0-9-]+)", b):
        key = m.group(0)
        if key not in tags:
            h = hashlib.sha256(key + cre).digest()
            tags[key] = b"/" + bytes(65 + x % 26 for x in h[:6]) + b"+" + m.group(2)
    for old, new in tags.items():
        b = re.sub(re.escape(old) + rb"(?![A-Za-z0-9-])", new, b)
    assert len(b) == n and b"ReportLab" not in b and b"reportlab" not in b and b"AAAAAA+" not in b
    open(path, "wb").write(b)


def normalize_all(target, gold):
    for d in (target, gold):
        for f in sorted(os.listdir(d)):
            p = os.path.join(d, f)
            if f.endswith(".xlsx"):
                creator, created, modified = STAMPS[f]
                normalize_ooxml(p, creator, created, modified)
            elif f.endswith(".pdf"):
                created, modified = PDF_STAMPS[f]
                normalize_pdf(p, created, modified)
