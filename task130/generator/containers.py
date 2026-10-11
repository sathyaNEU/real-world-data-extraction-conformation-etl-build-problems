"""File containers that rebuild byte for byte and carry their organisation's own stamps.

PDFs come out of reportlab in invariant mode with the library's banner comments left out, then the fixed creation
date is swapped, at equal length, for the in-fiction one. Office packages are rewritten with fixed entry dates and
document properties that name the person and the application that saved them."""
import datetime as dt
import io
import re
import zipfile

from reportlab.pdfbase import pdfdoc

CENTRAL = dt.timezone(dt.timedelta(hours=-6))


def _plain_header(self, pdfVersion=pdfdoc.PDF_VERSION_DEFAULT):
    self.strings = []
    self.write = self.strings.append
    self.offset = 0
    self.add(pdfdoc.pdfdocEnc("%%PDF-%s.%s" % pdfVersion) + b"\n%\xe2\xe3\xcf\xd3\n")


def _plain_id(self):
    if self._ID:
        return self._ID
    ids = pdfdoc.PDFText(self.signature.digest(), enc="raw").format(pdfdoc.DummyDoc())
    self._ID = b"\n[" + ids + ids + b"]\n"
    return self._ID


pdfdoc.PDFFile.__init__ = _plain_header
pdfdoc.PDFDocument.ID = _plain_id


def pdf_stamp(path, when):
    """replace the invariant creation and modification dates with a local Minnesota time, same byte length"""
    b = open(path, "rb").read()
    inv = re.findall(rb"D:\d{14}[+-]\d\d'\d\d'", b)
    assert inv, "no date in %s" % path
    off = "-06'00'" if not (dt.date(when.year, 3, 14) <= when.date() < dt.date(when.year, 11, 7)) else "-05'00'"
    new = ("D:" + when.strftime("%Y%m%d%H%M%S") + off).encode()
    for old in set(inv):
        assert len(old) == len(new)
        b = b.replace(old, new)
    open(path, "wb").write(b)


def _w3c(d):
    return d.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def core_props(creator, last_by, created, modified, title="", revision=None):
    x = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
         '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
         'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
         'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">')
    if title:
        x += "<dc:title>%s</dc:title>" % title.replace("&", "&amp;")
    x += "<dc:creator>%s</dc:creator><cp:lastModifiedBy>%s</cp:lastModifiedBy>" % (creator, last_by)
    if revision:
        x += "<cp:revision>%d</cp:revision>" % revision
    x += ('<dcterms:created xsi:type="dcterms:W3CDTF">%s</dcterms:created>'
          '<dcterms:modified xsi:type="dcterms:W3CDTF">%s</dcterms:modified></cp:coreProperties>' % (_w3c(created), _w3c(modified)))
    return x.encode("utf-8")


def app_props_xlsx(sheets, company):
    n = len(sheets)
    parts = "".join("<vt:lpstr>%s</vt:lpstr>" % s.replace("&", "&amp;") for s in sheets)
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
            '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
            'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Microsoft Excel</Application>'
            '<DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop><HeadingPairs><vt:vector size="2" baseType="variant">'
            '<vt:variant><vt:lpstr>Worksheets</vt:lpstr></vt:variant><vt:variant><vt:i4>%d</vt:i4></vt:variant></vt:vector>'
            '</HeadingPairs><TitlesOfParts><vt:vector size="%d" baseType="lpstr">%s</vt:vector></TitlesOfParts>'
            '<Company>%s</Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
            '<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>'
            % (n, n, parts, company.replace("&", "&amp;"))).encode("utf-8")


def app_props_docx(company, pages, words, chars):
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
            '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
            'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Template>Normal.dotm</Template>'
            '<TotalTime>47</TotalTime><Pages>%d</Pages><Words>%d</Words><Characters>%d</Characters>'
            '<Application>Microsoft Office Word</Application><DocSecurity>0</DocSecurity><Lines>%d</Lines>'
            '<Paragraphs>%d</Paragraphs><ScaleCrop>false</ScaleCrop><Company>%s</Company><LinksUpToDate>false</LinksUpToDate>'
            '<CharactersWithSpaces>%d</CharactersWithSpaces><SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged>'
            '<AppVersion>16.0000</AppVersion></Properties>'
            % (pages, words, chars, max(1, chars // 70), max(1, words // 40), company.replace("&", "&amp;"),
               chars + words)).encode("utf-8")


def repack(path, core, app, drop=()):
    """rewrite an Office package: fixed entry dates, given document properties, entries in their original order;
    a dropped part loses its relationship and content-type entry too"""
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist() if i.filename not in drop]
    for part in drop:
        items = [(n, re.sub(rb'<Relationship [^>]*Target="/?%s"[^>]*/>' % re.escape(part.encode()), b"", d)
                  if n.endswith(".rels") else
                  re.sub(rb'<Override PartName="/%s"[^>]*/>' % re.escape(part.encode()), b"", d)
                  if n == "[Content_Types].xml" else d) for n, d in items]
        if part.endswith(".jpeg"):
            items = [(n, re.sub(rb'<Default Extension="jpeg"[^>]*/>', b"", d) if n == "[Content_Types].xml" else d)
                     for n, d in items]
    names = [n for n, _ in items]
    if "docProps/core.xml" not in names:
        items.append(("docProps/core.xml", core))
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for name, data in items:
            if name == "docProps/core.xml":
                data = core
            elif name == "docProps/app.xml" and app is not None:
                data = app
            zi = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.create_system = 0
            z.writestr(zi, data)
    open(path, "wb").write(buf.getvalue())
