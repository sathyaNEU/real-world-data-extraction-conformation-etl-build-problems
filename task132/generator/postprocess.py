"""Make the office containers read as saved by the applications the fiction says made them, and reproducible:
shared strings and an Excel-shaped package for workbooks, the python-docx template residue removed from
documents, Office's own zip entry order and 1980 entry stamps, and a PDF whose producer and fonts are the
authoring application's."""
import re
import zipfile
from xml.sax.saxutils import escape

OFFICE_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
XLSX_ORDER = ["[Content_Types].xml", "_rels/.rels", "xl/workbook.xml", "xl/_rels/workbook.xml.rels"]
DOCX_ORDER = ["[Content_Types].xml", "_rels/.rels", "word/document.xml", "word/_rels/document.xml.rels"]


def _iso(t):
    return "%04d-%02d-%02dT%02d:%02d:%02dZ" % tuple(t[:6])


def _write(path, items, order):
    names = [n for n, _ in items]
    head = [n for n in order if n in names]
    tail_last = [n for n in ("docProps/core.xml", "docProps/app.xml") if n in names]
    mid = [n for n in names if n not in head and n not in tail_last]
    data = dict(items)
    with zipfile.ZipFile(path, "w") as z:
        for name in head + mid + tail_last:
            zi = zipfile.ZipInfo(name, date_time=OFFICE_ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data[name])


def _core(data, creator, last_by, created, modified, revision=None, title=None):
    """core properties written the way Office writes them, whatever the generating library left"""
    parts = []
    if title:
        parts.append("<dc:title>%s</dc:title>" % escape(title))
    parts.append("<dc:creator>%s</dc:creator>" % escape(creator))
    parts.append("<cp:lastModifiedBy>%s</cp:lastModifiedBy>" % escape(last_by))
    if revision is not None:
        parts.append("<cp:revision>%d</cp:revision>" % revision)
    parts.append('<dcterms:created xsi:type="dcterms:W3CDTF">%s</dcterms:created>' % _iso(created))
    parts.append('<dcterms:modified xsi:type="dcterms:W3CDTF">%s</dcterms:modified>' % _iso(modified))
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            + "".join(parts) + "</cp:coreProperties>").encode("utf-8")


# ---------------------------------------------------------------- workbooks

_INLINE = re.compile(r'<c ([^>]*?)t="inlineStr"([^>]*)><is><t(?: xml:space="preserve")?>(.*?)</t></is></c>', re.S)


def normalize_xlsx(path, creator, last_by, created, modified, company="Ironwood Hydro Distribution"):
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    data = dict(items)
    sst, index, refs = [], {}, 0
    sheets = sorted([n for n in data if n.startswith("xl/worksheets/sheet")], key=lambda n: int(re.findall(r"\d+", n)[0]))

    def repl(m):
        nonlocal refs
        text = m.group(3)
        if text not in index:
            index[text] = len(sst)
            sst.append(text)
        refs += 1
        return '<c %st="s"%s><v>%d</v></c>' % (m.group(1), m.group(2), index[text])

    for n in sheets:
        x = data[n].decode("utf-8")
        x = re.sub(r'<c ([^>]*?)t="inlineStr"([^>]*)>\s*</c>', lambda m: "<c %s%s/>" % (m.group(1).rstrip() + " " if m.group(1).strip() else "", m.group(2).strip()) if ' s="' in m.group(0) else "", x)
        x = re.sub(r'<c ([^>]*?)t="inlineStr"([^>]*)/>', lambda m: "<c %s%s/>" % (m.group(1), m.group(2).strip()) if ' s="' in m.group(0) else "", x)
        x = re.sub(r'<c ([^>]*?)t="inlineStr"([^>]*)><is><t(?: xml:space="preserve")?\s*/></is></c>', "", x)
        data[n] = _INLINE.sub(repl, x).encode("utf-8")
    if sst:
        body = "".join('<si><t%s>%s</t></si>' % (' xml:space="preserve"' if (t != t.strip()) else "", t) for t in sst)
        data["xl/sharedStrings.xml"] = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                                        '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="%d" uniqueCount="%d">%s</sst>'
                                        % (refs, len(sst), body)).encode("utf-8")
        rels = data["xl/_rels/workbook.xml.rels"].decode("utf-8")
        if "sharedStrings" not in rels:
            ids = [int(x) for x in re.findall(r'Id="rId(\d+)"', rels)]
            rels = rels.replace("</Relationships>", '<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/></Relationships>' % (max(ids) + 1))
            data["xl/_rels/workbook.xml.rels"] = rels.encode("utf-8")
        ct = data["[Content_Types].xml"].decode("utf-8")
        if "sharedStrings" not in ct:
            ct = ct.replace("</Types>", '<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/></Types>')
            data["[Content_Types].xml"] = ct.encode("utf-8")
    st = data["xl/styles.xml"].decode("utf-8")
    st = st.replace(' pivotButton="0"', "").replace(' quotePrefix="0"', "")
    data["xl/styles.xml"] = st.encode("utf-8")
    wb = data["xl/workbook.xml"].decode("utf-8")
    wb = wb.replace('calcId="124519"', 'calcId="191029"')
    wb = re.sub(r"<workbookProtection\s*/>", "", wb)
    data["xl/workbook.xml"] = wb.encode("utf-8")
    names = re.findall(r'<sheet [^>]*name="([^"]+)"', wb)
    app = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
           '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
           'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Microsoft Excel</Application>'
           '<DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop><HeadingPairs><vt:vector size="2" baseType="variant">'
           '<vt:variant><vt:lpstr>Worksheets</vt:lpstr></vt:variant><vt:variant><vt:i4>%d</vt:i4></vt:variant></vt:vector></HeadingPairs>'
           '<TitlesOfParts><vt:vector size="%d" baseType="lpstr">%s</vt:vector></TitlesOfParts><Company>%s</Company>'
           '<LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged>'
           '<AppVersion>16.0300</AppVersion></Properties>'
           % (len(names), len(names), "".join("<vt:lpstr>%s</vt:lpstr>" % n for n in names), escape(company)))
    data["docProps/app.xml"] = app.encode("utf-8")
    data["docProps/core.xml"] = _core(data["docProps/core.xml"], creator, last_by, created, modified)
    order = XLSX_ORDER + sheets + ["xl/theme/theme1.xml", "xl/styles.xml", "xl/sharedStrings.xml"]
    _write(path, list(data.items()), order)


# ---------------------------------------------------------------- documents

def _rsid(seed, k):
    import hashlib
    return "00" + hashlib.md5(("%s-%d" % (seed, k)).encode()).hexdigest()[:6].upper()


def normalize_docx(path, author, last_by, created, modified, revision, total_time, title=None,
                   company="Ironwood Hydro Distribution", seed="doc"):
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    data = dict(items)
    for n in [n for n in data if n.startswith("customXml/") or n in ("word/stylesWithEffects.xml", "docProps/thumbnail.jpeg")]:
        del data[n]
    rels = data["word/_rels/document.xml.rels"].decode("utf-8")
    rels = re.sub(r'<Relationship [^>]*Target="(?:\.\./customXml/[^"]*|stylesWithEffects\.xml)"[^>]*/>', "", rels)
    data["word/_rels/document.xml.rels"] = rels.encode("utf-8")
    root = data["_rels/.rels"].decode("utf-8")
    root = re.sub(r'<Relationship [^>]*thumbnail[^>]*/>', "", root)
    data["_rels/.rels"] = root.encode("utf-8")
    ct = data["[Content_Types].xml"].decode("utf-8")
    ct = re.sub(r'<Override PartName="/(?:customXml/[^"]*|word/stylesWithEffects\.xml|docProps/thumbnail\.jpeg)"[^>]*/>', "", ct)
    if not any(n.endswith((".jpeg", ".jpg")) for n in data):
        ct = re.sub(r'<Default Extension="jpe?g"[^>]*/>', "", ct)
    data["[Content_Types].xml"] = ct.encode("utf-8")
    doc = data["word/document.xml"].decode("utf-8")
    doc = re.sub(r'\s+xmlns:mo="[^"]*"', "", doc)
    doc = re.sub(r'\s+xmlns:mv="[^"]*"', "", doc)
    doc = re.sub(r'mc:Ignorable="([^"]*)"', lambda m: 'mc:Ignorable="%s"' % " ".join(t for t in m.group(1).split() if t not in ("mv", "mo")), doc)
    for tag in ("b", "i", "bCs", "iCs"):
        doc = doc.replace("<w:%s w:val=\"0\"/>" % tag, "")
    doc = doc.replace("<w:rPr></w:rPr>", "").replace("<w:rPr/>", "")
    # editing sessions: paragraphs carry the revision id of the session that wrote them
    paras = len(re.findall(r"<w:p[ >]", doc))
    sessions = [_rsid(seed, k) for k in range(max(2, min(6, 1 + paras // 12)))]
    count = {"k": 0}

    def tagp(m):
        k = min(len(sessions) - 1, count["k"] * len(sessions) // max(1, paras))
        count["k"] += 1
        return '<w:p w:rsidR="%s" w:rsidRDefault="%s"%s' % (sessions[k], sessions[k], m.group(1))

    doc = re.sub(r"<w:p( |>)", lambda m: tagp(m), doc)
    data["word/document.xml"] = doc.encode("utf-8")
    stt = data["word/settings.xml"].decode("utf-8")
    stt = stt.replace('w:val="14"/><w:compatSetting w:name="overrideTableStyleFontSizeAndJustification"',
                      'w:val="15"/><w:compatSetting w:name="overrideTableStyleFontSizeAndJustification"')
    stt = re.sub(r'(<w:compatSetting w:name="compatibilityMode"[^>]*w:val=")\d+(")', r"\g<1>15\g<2>", stt)
    stt = re.sub(r"<w:rsids>.*?</w:rsids>", "<w:rsids><w:rsidRoot w:val=\"%s\"/>%s</w:rsids>" % (
        sessions[0], "".join('<w:rsid w:val="%s"/>' % s for s in sorted(sessions))), stt, flags=re.S)
    stt = re.sub(r'<w:themeFontLang [^>]*/>', '<w:themeFontLang w:val="en-CA"/>', stt)
    stt = stt.replace("<w:savePreviewPicture/>", "")
    stt = re.sub(r'<w14:docId w14:val="[0-9A-F]+"/>', '<w14:docId w14:val="%s"/>' % _rsid(seed, 99)[2:].rjust(8, "1"), stt)
    data["word/settings.xml"] = stt.encode("utf-8")
    text = " ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", doc))
    words = len(text.split())
    chars = len(text.replace(" ", ""))
    npara = len([p for p in re.findall(r"<w:p [^>]*>(.*?)</w:p>", doc, flags=re.S) if "<w:t" in p])
    app = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
           '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
           'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Template>Normal.dotm</Template>'
           '<TotalTime>%d</TotalTime><Pages>%d</Pages><Words>%d</Words><Characters>%d</Characters>'
           '<Application>Microsoft Office Word</Application><DocSecurity>0</DocSecurity><Lines>%d</Lines>'
           '<Paragraphs>%d</Paragraphs><ScaleCrop>false</ScaleCrop><Company>%s</Company><LinksUpToDate>false</LinksUpToDate>'
           '<CharactersWithSpaces>%d</CharactersWithSpaces><SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged>'
           '<AppVersion>16.0000</AppVersion></Properties>'
           % (total_time, max(1, -(-words // 480)), words, chars, max(1, words // 12), npara, escape(company), len(text)))
    data["docProps/app.xml"] = app.encode("utf-8")
    data["docProps/core.xml"] = _core(data["docProps/core.xml"], author, last_by, created, modified, revision, title)
    order = DOCX_ORDER + sorted(n for n in data if re.fullmatch(r"word/(header|footer)\d+\.xml", n)) + [
        "word/media/image1.png", "word/numbering.xml", "word/theme/theme1.xml", "word/settings.xml", "word/styles.xml",
        "word/webSettings.xml", "word/fontTable.xml"]
    _write(path, list(data.items()), order)


# ---------------------------------------------------------------- PDF


def _same_len(b, old, new):
    """replace a byte string with one no longer than it, padding with spaces outside the token"""
    assert len(new) <= len(old), (old, new)
    return b.replace(old, new + b" " * (len(old) - len(new)))


def _pdf_text(s):
    return b"<FEFF" + s.encode("utf-16-be").hex().upper().encode() + b">"


def normalize_pdf(path, stamp, doc_id, producer="Microsoft\u00ae Word 2016", creator="Microsoft\u00ae Word 2016",
                  font_from=b"LiberationSans", font_to=b"ArialMT"):
    """stamp: the creation instant as a PDF date in UTC, e.g. b"D:20260820130500Z" (no longer than the original)"""
    b = open(path, "rb").read()
    b = re.sub(rb"\(D:\d{14}[^)]*\)", lambda m: _pad(b"(" + stamp + b")", len(m.group(0))), b)
    for key, val in ((b"/Producer", producer), (b"/Creator", creator)):
        m = re.search(re.escape(key) + rb"\s*(<FEFF[0-9A-Fa-f]*>|\([^)]*\))", b)
        if m:
            old = m.group(0)
            new = key + _pdf_text(val)
            if len(new) > len(old):
                new = key + b"(" + val.encode("latin-1", "replace") + b")"
            b = _same_len(b, old, new)
    b = re.sub(rb"([A-Z]{6}\+)" + font_from + rb"(-[A-Za-z]+)?",
               lambda m: _pad(m.group(1) + font_to + (b"," + m.group(2)[1:] if m.group(2) else b""), len(m.group(0))), b)
    b = re.sub(rb"(/ID\s*\[\s*)<[0-9A-Fa-f]{32}>(\s*)<[0-9A-Fa-f]{32}>",
               lambda m: m.group(1) + b"<" + doc_id + b">" + m.group(2) + b"<" + doc_id + b">", b)
    b = re.sub(rb"/DocChecksum /[0-9A-F]{32}", b"/DocChecksum /" + doc_id[::-1], b)
    open(path, "wb").write(b)


def _pad(new, n):
    assert len(new) <= n, (new, n)
    return new + b" " * (n - len(new))
