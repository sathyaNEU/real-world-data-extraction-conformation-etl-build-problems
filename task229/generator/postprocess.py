"""Make office containers reproducible: fixed zip entry times, fixed PDF dates and document id."""
import hashlib
import re
import zipfile

FIXED = (2026, 12, 7, 7, 20, 0)


DECL = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
NS_REL = b"http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def normalize_zip(path, when=FIXED, modified=None, company="Corderoy Logistics"):
    """Repack an office container reproducibly. A workbook is laid out the way Excel saves one (shared
    strings, its own calc id and extended properties, its entry order, the 1980 entry stamp Office
    writes) and keeps its own last-saved stamp, given as `modified`; the cells are not touched."""
    stamp = modified or "%04d-%02d-%02dT%02d:%02d:%02dZ" % when
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    names = [n for n, _ in items]
    is_docx = "word/document.xml" in names
    if not is_docx:
        items = _excel_like(dict(items), stamp, company)
        when = (1980, 1, 1, 0, 0, 0)
    doc_text = ""
    if is_docx:
        xml = dict(items)["word/document.xml"].decode("utf-8")
        doc_text = " ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", xml))
    with zipfile.ZipFile(path, "w") as z:
        for name, data in items:
            if is_docx and name == "docProps/core.xml":
                data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                              lambda m: m.group(1) + stamp.encode() + m.group(2), data)
            if is_docx and name == "docProps/app.xml":
                data = _word_app(data, doc_text)
            zi = zipfile.ZipInfo(name, date_time=when)
            zi.compress_type = zipfile.ZIP_DEFLATED
            if is_docx:
                zi.external_attr = 0o600 << 16
            else:
                zi.create_system = 0
            z.writestr(zi, data)


def _excel_like(parts, modified, company):
    sst, index, count = [], {}, [0]

    def shared(m):
        key = m.group(3)
        if key not in index:
            index[key] = len(sst)
            sst.append(key)
        count[0] += 1
        return b"<c " + m.group(1) + b't="s"' + m.group(2) + b"><v>%d</v></c>" % index[key]

    sheets = sorted((n for n in parts if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", n)),
                    key=lambda n: int(re.search(r"(\d+)\.xml$", n).group(1)))
    def blank(m):
        attrs = (m.group(1) + m.group(2)).strip()
        return b"<c " + attrs + b"/>" if b" s=" in b" " + attrs else b""

    for n in sheets:
        # an empty string reads as no value; Excel stores no cell for it, or a styled blank
        parts[n] = re.sub(rb'<c ([^>]*?)t="inlineStr"([^>]*)></c>', blank, parts[n])
        parts[n] = re.sub(rb'<c ([^>]*?)t="inlineStr"([^>]*)><is>(.*?)</is></c>', shared, parts[n], flags=re.S)
        assert b"inlineStr" not in parts[n] and b"<is>" not in parts[n], n
        parts[n] = re.sub(rb'(<c [^>]*?) t="n"', rb"\1", parts[n])
        parts[n] = parts[n].replace(b'<sheetPr><outlinePr summaryBelow="1" summaryRight="1"/><pageSetUpPr/></sheetPr>', b"")
        parts[n] = re.sub(rb"<pageMargins [^>]*/>", b'<pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" '
                          b'header="0.3" footer="0.3"/>', parts[n])
    parts["xl/sharedStrings.xml"] = (b'<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                                     b'count="%d" uniqueCount="%d">' % (count[0], len(sst))
                                     + b"".join(b"<si>" + s_ + b"</si>" for s_ in sst) + b"</sst>")
    ct = parts["[Content_Types].xml"]
    if b"/xl/sharedStrings.xml" not in ct:
        ct = ct.replace(b"</Types>", b'<Override PartName="/xl/sharedStrings.xml" ContentType="application/'
                        b'vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/></Types>')
    parts["[Content_Types].xml"] = ct
    parts["_rels/.rels"] = parts["_rels/.rels"].replace(b'Target="/', b'Target="')
    rels = parts["xl/_rels/workbook.xml.rels"].replace(b'Target="/xl/', b'Target="')
    if b"sharedStrings.xml" not in rels:
        rid = 1 + max(int(x) for x in re.findall(rb'Id="rId(\d+)"', rels))
        rels = rels.replace(b"</Relationships>", b'<Relationship Id="rId%d" Type="%s/sharedStrings" '
                            b'Target="sharedStrings.xml"/></Relationships>' % (rid, NS_REL))
    parts["xl/_rels/workbook.xml.rels"] = rels
    wb = parts["xl/workbook.xml"]
    wb = re.sub(rb"<calcPr[^>]*/>", b'<calcPr calcId="191029"/>', wb)
    wb = wb.replace(b"<workbookProtection/>", b"").replace(b"<definedNames/>", b"")
    wb = wb.replace(b"<workbookPr/>", b'<workbookPr defaultThemeVersion="124226"/>')
    wb = wb.replace(b' xmlns:r="%s"' % NS_REL, b"").replace(b' state="visible"', b"")
    wb = wb.replace(b'<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">',
                    b'<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="%s">' % NS_REL)
    wb = re.sub(rb"<workbookView [^>]*/>", b'<workbookView xWindow="-110" yWindow="-110" windowWidth="19420" '
                b'windowHeight="10300"/>', wb)
    parts["xl/workbook.xml"] = wb
    titles = re.findall(rb'<sheet [^>]*name="([^"]*)"', wb)
    parts["docProps/app.xml"] = (
        b'<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        b'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        b"<Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>"
        b'<HeadingPairs><vt:vector size="2" baseType="variant"><vt:variant><vt:lpstr>Worksheets</vt:lpstr></vt:variant>'
        b"<vt:variant><vt:i4>%d</vt:i4></vt:variant></vt:vector></HeadingPairs>" % len(titles)
        + b'<TitlesOfParts><vt:vector size="%d" baseType="lpstr">' % len(titles)
        + b"".join(b"<vt:lpstr>" + t_ + b"</vt:lpstr>" for t_ in titles)
        + b"</vt:vector></TitlesOfParts><Company>" + company.encode() + b"</Company><LinksUpToDate>false</LinksUpToDate>"
        b"<SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion>"
        b"</Properties>")
    core = parts["docProps/core.xml"]
    who = re.search(rb"<dc:creator[^>]*>([^<]*)</dc:creator>", core).group(1)
    last = re.search(rb"<cp:lastModifiedBy[^>]*>([^<]*)</cp:lastModifiedBy>", core)
    made = re.search(rb"<dcterms:created[^>]*>([^<]*)</dcterms:created>", core).group(1)
    parts["docProps/core.xml"] = (
        b'<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        b'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
        b'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        b"<dc:creator>" + who + b"</dc:creator><cp:lastModifiedBy>" + (last.group(1) if last else who)
        + b'</cp:lastModifiedBy><dcterms:created xsi:type="dcterms:W3CDTF">' + made
        + b'</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">' + modified.encode()
        + b"</dcterms:modified></cp:coreProperties>")
    for n in parts:
        if n.endswith((".xml", ".rels")) and not parts[n].startswith(b"<?xml"):
            parts[n] = DECL + parts[n]
    head = ["[Content_Types].xml", "_rels/.rels", "xl/workbook.xml", "xl/_rels/workbook.xml.rels"] + sheets
    tail = ["xl/theme/theme1.xml", "xl/styles.xml", "xl/sharedStrings.xml", "docProps/core.xml", "docProps/app.xml"]
    rest = [n for n in parts if n not in head and n not in tail]
    return [(n, parts[n]) for n in head + rest + tail if n in parts]


def _word_app(data, text):
    words = len(text.split())
    chars = len(text.replace(" ", ""))
    pages = max(1, -(-words // 520))
    data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>Microsoft Office Word</Application>", data)
    for tag, val in (("Words", words), ("Characters", chars), ("Pages", pages),
                     ("CharactersWithSpaces", len(text)), ("Lines", max(1, words // 11)),
                     ("Paragraphs", max(1, words // 45))):
        data = re.sub(("<%s>[^<]*</%s>" % (tag, tag)).encode(), ("<%s>%d</%s>" % (tag, val, tag)).encode(), data)
    data = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0000</AppVersion>", data)
    return data


def normalize_pdf(path, stamp=b"D:20260911143200Z'", doc_id=b"3B9E07C4A1D25F68E0C7B4A91D3F2E85"):
    b = open(path, "rb").read()
    b = re.sub(rb"D:\d{14}Z'", lambda m: stamp[:len(m.group(0))], b)
    b = re.sub(rb"(/ID\s*\[\s*)<[0-9A-Fa-f]{32}>(\s*)<[0-9A-Fa-f]{32}>",
               lambda m: m.group(1) + b"<" + doc_id + b">" + m.group(2) + b"<" + doc_id + b">", b)
    b = re.sub(rb"/DocChecksum /[0-9A-F]{32}", b"/DocChecksum /" + doc_id[::-1], b)
    open(path, "wb").write(b)
