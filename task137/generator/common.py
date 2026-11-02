"""Writers shared by the pack and the goldens: fixed document properties and zip entry times, so every rebuild is
byte-identical."""
import csv
import datetime as dt
import os
import re
import zipfile

import params as P


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(header)
        w.writerows(rows)


def _rezip(tmp, path, when, fix):
    with zipfile.ZipFile(tmp) as zin, zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            zi = zipfile.ZipInfo(info.filename, date_time=(when.year, when.month, when.day, when.hour, when.minute, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            zout.writestr(zi, fix(info.filename, zin.read(info.filename)))
    os.remove(tmp)


def save_xlsx(wb, path, when, author, company=P.COMPANY):
    wb.properties.created = when
    wb.properties.modified = when
    wb.properties.creator = author
    wb.properties.lastModifiedBy = author
    tmp = path + ".tmp"
    wb.save(tmp)

    def fix(name, data):
        if name == "docProps/app.xml":
            data = (b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Properties xmlns="http://schemas.'
                    b'openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats'
                    b'.org/officeDocument/2006/docPropsVTypes"><Application>Microsoft Excel</Application><DocSecurity>0'
                    b'</DocSecurity><ScaleCrop>false</ScaleCrop><Company>' + company.encode() + b'</Company>'
                    b'<LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc><HyperlinksChanged>false'
                    b'</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>')
        if name == "docProps/core.xml":
            stamp = when.strftime("%Y-%m-%dT%H:%M:%SZ").encode()
            data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>" + stamp + rb"\g<2>", data)
            data = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", rb"\g<1>" + stamp + rb"\g<2>", data)
        return data
    _rezip(tmp, path, when, fix)


def save_docx(doc, path, when, author):
    cp = doc.core_properties
    cp.author = author
    cp.last_modified_by = author
    cp.created = when
    cp.modified = when
    cp.revision = 3
    cp.title = ""
    cp.comments = ""
    tmp = path + ".tmp"
    doc.save(tmp)

    def fix(name, data):
        if name == "docProps/app.xml":
            data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>Microsoft Office Word</Application>", data)
            data = re.sub(rb"<Company>[^<]*</Company>", b"<Company>" + P.COMPANY.encode() + b"</Company>", data)
        return data
    _rezip(tmp, path, when, fix)


def clean_pdf(path, when):
    """The PDF library leaves its name in two comments and a fixed 2000 date in the document information; overwrite them
    in place at equal length, so every byte offset (and the cross-reference table) stays where it was."""
    b = open(path, "rb").read()
    n0 = len(b)
    for tag in (b" ReportLab Generated PDF document (opensource)", b" ReportLab generated PDF document -- digest (opensource)",
                b" ReportLab Generated PDF document http://www.reportlab.com"):
        b = b.replace(tag, b" " * len(tag))
    stamp = ("D:%s+00'00'" % when.strftime("%Y%m%d%H%M%S")).encode()
    b = re.sub(rb"D:20000101000000\+00'00'", stamp, b)
    assert len(b) == n0 and b"ReportLab" not in b and b"D:2000" not in b, path
    open(path, "wb").write(b)


def ddmmyyyy(d):
    return d.strftime("%d/%m/%Y")


def hhmm(h):
    m = int(round(h * 60))
    return "%02d:%02d" % (m // 60, m % 60)


STAMP = dt.datetime(2026, 11, 2, 16, 40)
