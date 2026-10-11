"""File containers that rebuild byte for byte and carry their organisation's own stamps.

PDFs are written by LibreOffice from a Word document, headless, with tagged structure and embedded font subsets; the
export time and the document identifier LibreOffice stamps are then replaced, at equal length, by the in-fiction time
and an identifier derived from the document, so a rebuild is byte-identical. LibreOffice's own Producer and Creator
are left as LibreOffice wrote them.

The pack's workbooks are exports from the organisations' own systems and are left in the layout the export library
writes, with the person who ran the export and the time of the export in the document properties and on every entry;
nothing claims an application that did not write the file. Some PDFs are printed from HTML by headless Chromium, the
way a policy system or a client portal renders a document. The golden deliverables keep the Office part order and
properties of the analyst's own files."""
import datetime as dt
import hashlib
import io
import os
import re
import shutil
import subprocess
import tempfile
import zipfile

CENTRAL = dt.timezone(dt.timedelta(hours=-6))
DECL = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'


def central(d):
    """the UTC offset of a Minnesota local time"""
    y = d.year
    start = dt.date(y, 3, 8) + dt.timedelta(days=(6 - dt.date(y, 3, 8).weekday()) % 7)      # second Sunday of March
    end = dt.date(y, 11, 1) + dt.timedelta(days=(6 - dt.date(y, 11, 1).weekday()) % 7)      # first Sunday of November
    return dt.timezone(dt.timedelta(hours=-5 if start <= d.date() < end else -6))


# ------------------------------------------------------------------ PDF through LibreOffice
def soffice_pdf(docx_path, pdf_path, when):
    """convert a .docx to a tagged PDF with LibreOffice, then pin the export time to `when` (local Minnesota time)
    and the document identifier to one derived from the file, both at equal length"""
    work = tempfile.mkdtemp(prefix="lo-")
    try:
        env = dict(os.environ, TZ="America/Chicago", HOME=work)
        prof = "file://" + os.path.join(work, "profile")
        flt = 'pdf:writer_pdf_Export:{"UseTaggedPDF":{"type":"boolean","value":"true"},' \
              '"ExportBookmarks":{"type":"boolean","value":"true"}}'
        subprocess.run(["soffice", "-env:UserInstallation=" + prof, "--headless", "--norestore", "--convert-to", flt,
                        "--outdir", work, docx_path], check=True, env=env, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, timeout=180)
        out = os.path.join(work, os.path.splitext(os.path.basename(docx_path))[0] + ".pdf")
        b = open(out, "rb").read()
    finally:
        shutil.rmtree(work, ignore_errors=True)
    dates = re.findall(rb"D:\d{14}[+-]\d\d'\d\d'", b)
    assert dates, "no export time in the PDF"
    off = when.replace(tzinfo=central(when)).strftime("%z")
    new = ("D:" + when.strftime("%Y%m%d%H%M%S") + off[:3] + "'" + off[3:] + "'").encode()
    for old in set(dates):
        assert len(old) == len(new)
        b = b.replace(old, new)
    ids = re.findall(rb"/ID \[ <([0-9A-F]{32})>\s*<([0-9A-F]{32})> \]", b)
    assert len(ids) == 1, "one document identifier"
    pin = hashlib.md5(os.path.basename(pdf_path).encode() + new).hexdigest().upper().encode()
    for old in set(ids[0]):
        b = b.replace(old, pin)
    # LibreOffice's own checksum covers the export as first written, run clock included: recomputed over the pinned file
    assert len(re.findall(rb"/DocChecksum /[0-9A-F]{32}", b)) == 1, "one document checksum"
    blank = re.sub(rb"(/DocChecksum /)[0-9A-F]{32}", rb"\g<1>" + b"0" * 32, b)
    b = re.sub(rb"(/DocChecksum /)[0-9A-F]{32}", rb"\g<1>" + hashlib.md5(blank).hexdigest().upper().encode(), blank)
    open(pdf_path, "wb").write(b)


# ------------------------------------------------------------------ PDF through Chromium
CHROMIUM = "/opt/pw-browsers/chromium"


def chromium_pdf(html, pdf_path, when):
    """print an HTML document to PDF with headless Chromium (Skia), then pin the creation and modification times
    Chromium stamps to `when` (local Minnesota time, written in UTC as Chromium writes it), at equal length"""
    work = tempfile.mkdtemp(prefix="cr-")
    try:
        src = os.path.join(work, "doc.html")
        with open(src, "w", encoding="utf-8") as f:
            f.write(html)
        out = os.path.join(work, "doc.pdf")
        env = dict(os.environ, TZ="America/Chicago", HOME=work)
        subprocess.run([CHROMIUM, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                        "--user-data-dir=" + os.path.join(work, "profile"), "--print-to-pdf=" + out, "file://" + src],
                       check=True, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
        b = open(out, "rb").read()
    finally:
        shutil.rmtree(work, ignore_errors=True)
    dates = re.findall(rb"D:\d{14}\+00'00'", b)
    assert dates, "no creation time in the PDF"
    utc = when.replace(tzinfo=central(when)).astimezone(dt.timezone.utc)
    new = ("D:" + utc.strftime("%Y%m%d%H%M%S") + "+00'00'").encode()
    for old in set(dates):
        assert len(old) == len(new)
        b = b.replace(old, new)
    open(pdf_path, "wb").write(b)


# ------------------------------------------------------------------ document properties
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


# ------------------------------------------------------------------ Office packages
_INLINE = re.compile(rb'<c ([^>]*?)t="inlineStr"([^>]*)><is><t(?: xml:space="preserve")?>(.*?)</t></is></c>', re.S)
_INLINE_EMPTY = re.compile(rb'<c ([^>]*?)t="inlineStr"([^>]*)><is><t(?: xml:space="preserve")?/></is></c>')


def _shared_strings(items):
    """move every inline string into a shared string table, in order of first use, as Excel keeps them"""
    table, index, count = [], {}, [0]

    def sub(m):
        text = m.group(3)
        if text not in index:
            index[text] = len(table)
            table.append(text)
        count[0] += 1
        return b'<c ' + m.group(1) + b't="s"' + m.group(2) + b'><v>%d</v></c>' % index[text]

    out = []
    for name, data in items:
        if name.startswith("xl/worksheets/sheet") and name.endswith(".xml"):
            data = _INLINE.sub(sub, data)
            data = _INLINE_EMPTY.sub(lambda m: b'<c ' + m.group(1) + m.group(2).strip() + b'/>', data)
        out.append((name, data))
    si = b"".join(b'<si><t xml:space="preserve">' + t + b"</t></si>" if (t[:1].isspace() or t[-1:].isspace())
                  else b"<si><t>" + t + b"</t></si>" for t in table)
    sst = DECL + (b'<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="%d" uniqueCount="%d">'
                  % (count[0], len(table))) + si + b"</sst>"
    return out, sst


def _excel_order(name):
    order = ["[Content_Types].xml", "_rels/.rels", "xl/workbook.xml", "xl/_rels/workbook.xml.rels"]
    if name in order:
        return (order.index(name), 0, name)
    m = re.match(r"xl/worksheets/sheet(\d+)\.xml$", name)
    if m:
        return (4, int(m.group(1)), name)
    rest = {"xl/theme/theme1.xml": 5, "xl/styles.xml": 6, "xl/sharedStrings.xml": 7, "docProps/core.xml": 20,
            "docProps/app.xml": 21}
    return (rest.get(name, 10), 0, name)


def _word_order(name):
    order = ["[Content_Types].xml", "_rels/.rels", "word/document.xml", "word/_rels/document.xml.rels"]
    if name in order:
        return (order.index(name), name)
    rest = {"word/theme/theme1.xml": 8, "word/settings.xml": 9, "word/styles.xml": 10, "word/stylesWithEffects.xml": 11,
            "word/webSettings.xml": 12, "word/fontTable.xml": 13, "docProps/core.xml": 20, "docProps/app.xml": 21,
            "docProps/custom.xml": 22}
    if name.startswith("word/media/"):
        return (5, name)
    if name.startswith(("word/header", "word/footer", "word/footnotes", "word/endnotes", "word/numbering")):
        return (6, name)
    if name.startswith("customXml/"):
        return (15, name)
    return (rest.get(name, 14), name)


def _declared(name, data):
    if name.endswith((".xml", ".rels")) and not data.startswith(b"<?xml"):
        return DECL + data
    return data


def library_xlsx(path, core, when):
    """a workbook as an export library writes it, left in the library's own layout: the document properties name the
    person who ran the export and when, the extended-properties part (where the library would name itself) is left
    out rather than claiming an application that did not write the file, and every entry carries the time of the
    export"""
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    out = []
    for n, d in items:
        if n == "docProps/app.xml":
            continue
        if n == "docProps/core.xml":
            d = core
        elif n == "_rels/.rels":
            d = re.sub(rb'<Relationship [^>]*Target="/?docProps/app.xml"[^>]*/>', b"", d)
        elif n == "[Content_Types].xml":
            d = re.sub(rb'<Override PartName="/docProps/app.xml"[^>]*/>', b"", d)
        out.append((n, d))
    stamp = when.timetuple()[:6]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for name, data in out:
            zi = zipfile.ZipInfo(name, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.create_system = 3
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)
    open(path, "wb").write(buf.getvalue())


def repack(path, core, app, drop=()):
    """rewrite an Office package with fixed entry dates, the given document properties and the parts in the order
    the Office application writes them; an .xlsx gets a shared string table. A dropped part loses its relationship
    and content-type entry too."""
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
    if "docProps/app.xml" not in names and app is not None:
        items.append(("docProps/app.xml", app))
        items = [(n, d.replace(b"</Types>", b'<Override PartName="/docProps/app.xml" ContentType="application/vnd.'
                                            b'openxmlformats-officedocument.extended-properties+xml"/></Types>')
                  if n == "[Content_Types].xml" else d) for n, d in items]
    xlsx = path.endswith(".xlsx")
    if xlsx and "xl/sharedStrings.xml" not in names:
        items, sst = _shared_strings(items)
        items.append(("xl/sharedStrings.xml", sst))
        items = [(n, d.replace(b"</Types>", b'<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.'
                                            b'openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/></Types>')
                  if n == "[Content_Types].xml" else d) for n, d in items]
        rels = dict(items)["xl/_rels/workbook.xml.rels"]
        ids = [int(x) for x in re.findall(rb'Id="rId(\d+)"', rels)]
        rel = (b'<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/'
               b'sharedStrings" Target="sharedStrings.xml"/>' % (max(ids) + 1))
        items = [(n, d.replace(b"</Relationships>", rel + b"</Relationships>") if n == "xl/_rels/workbook.xml.rels" else d)
                 for n, d in items]
    items = [(n, core if n == "docProps/core.xml" else app if (n == "docProps/app.xml" and app is not None) else d)
             for n, d in items]
    items = [(n, _declared(n, d)) for n, d in items]
    items.sort(key=lambda x: _excel_order(x[0]) if xlsx else _word_order(x[0]))
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for name, data in items:
            zi = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.create_system = 0
            z.writestr(zi, data)
    open(path, "wb").write(buf.getvalue())
