"""Office containers laid out the way Office saves them, and the writer's signature removed (H1).

Order at every save: the library writes the file, scrub() removes the library's name and any out-of-band stamp,
then finish_office() lays the package out as Excel or Word would (shared strings, calc id, extended properties,
the 1980 entry stamp Office writes, no template thumbnail) with the document's own created and modified dates."""
import os
import re
import zipfile

OFFICE_ENTRY_TIME = (1980, 1, 1, 0, 0, 0)
DECL = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
NS_REL = b"http://schemas.openxmlformats.org/officeDocument/2006/relationships"
FLOOR, CEILING = "2012-01-01", "2026-10-31"


def _scrubber():
    import importlib.util
    here = os.path.dirname(os.path.abspath(__file__))
    p = os.path.join(here, "..", "..", ".claude", "skills", "reduce-house-fixes", "scripts", "scrub_producer_metadata.py")
    spec = importlib.util.spec_from_file_location("scrub_producer_metadata", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def scrub(path, producer, stamp):
    """remove the writing library's name and out-of-band stamps from a binary, right after it is saved (H1)"""
    s = _scrubber()
    if path.endswith(".pdf"):
        s.scrub_pdf(path, producer, stamp, FLOOR, CEILING)
    else:
        s.scrub_ooxml(path, producer, stamp, FLOOR, CEILING)
    names, bad = s.audit(path, FLOOR, CEILING)
    assert not names and not bad, (path, names, bad)


def _core(parts, created, modified):
    core = parts["docProps/core.xml"]
    who = re.search(rb"<dc:creator[^>]*>([^<]*)</dc:creator>", core)
    who = who.group(1) if who else b""
    last = re.search(rb"<cp:lastModifiedBy[^>]*>([^<]*)</cp:lastModifiedBy>", core)
    title = re.search(rb"<dc:title[^>]*>([^<]*)</dc:title>", core)
    rev = re.search(rb"<cp:revision[^>]*>([^<]*)</cp:revision>", core)
    out = (b'<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
           b'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
           b'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">')
    if title and title.group(1):
        out += b"<dc:title>" + title.group(1) + b"</dc:title>"
    out += b"<dc:creator>" + who + b"</dc:creator><cp:lastModifiedBy>" + (last.group(1) if last else who) + b"</cp:lastModifiedBy>"
    if rev and rev.group(1):
        out += b"<cp:revision>" + rev.group(1) + b"</cp:revision>"
    out += (b'<dcterms:created xsi:type="dcterms:W3CDTF">' + created.encode() + b"</dcterms:created>"
            b'<dcterms:modified xsi:type="dcterms:W3CDTF">' + modified.encode() + b"</dcterms:modified></cp:coreProperties>")
    parts["docProps/core.xml"] = out


def _excel(parts, company):
    sst, index, count = [], {}, [0]

    def shared(m):
        key = m.group(3)
        if key not in index:
            index[key] = len(sst)
            sst.append(key)
        count[0] += 1
        return b"<c " + m.group(1) + b't="s"' + m.group(2) + b"><v>%d</v></c>" % index[key]

    def blank(m):
        attrs = (m.group(1) + m.group(2)).strip()
        return b"<c " + attrs + b"/>" if b" s=" in b" " + attrs else b""

    sheets = sorted((n for n in parts if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", n)),
                    key=lambda n: int(re.search(r"(\d+)\.xml$", n).group(1)))
    for n in sheets:
        x = parts[n]
        x = re.sub(rb'<c ([^>]*?)t="inlineStr"([^>]*)></c>', blank, x)
        x = re.sub(rb'<c ([^>]*?)t="inlineStr"([^>]*)><is>(.*?)</is></c>', shared, x, flags=re.S)
        assert b"inlineStr" not in x, n
        x = re.sub(rb'(<c [^>]*?) t="n"', rb"\1", x)
        x = x.replace(b'<sheetPr><outlinePr summaryBelow="1" summaryRight="1"/><pageSetUpPr/></sheetPr>', b"")
        x = re.sub(rb"<pageMargins [^>]*/>", b'<pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" '
                   b'header="0.3" footer="0.3"/>', x)
        parts[n] = x
    parts["xl/sharedStrings.xml"] = (b'<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                                     b'count="%d" uniqueCount="%d">' % (count[0], len(sst))
                                     + b"".join(b"<si>" + s_ + b"</si>" for s_ in sst) + b"</sst>")
    ct = parts["[Content_Types].xml"]
    if b"/xl/sharedStrings.xml" not in ct:
        ct = ct.replace(b"</Types>", b'<Override PartName="/xl/sharedStrings.xml" ContentType="application/'
                        b'vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/></Types>')
    parts["[Content_Types].xml"] = ct
    rels = parts["xl/_rels/workbook.xml.rels"].replace(b'Target="/xl/', b'Target="')
    if b"sharedStrings.xml" not in rels:
        rid = 1 + max(int(x) for x in re.findall(rb'Id="rId(\d+)"', rels))
        rels = rels.replace(b"</Relationships>", b'<Relationship Id="rId%d" Type="%s/sharedStrings" '
                            b'Target="sharedStrings.xml"/></Relationships>' % (rid, NS_REL))
    parts["xl/_rels/workbook.xml.rels"] = rels
    parts["_rels/.rels"] = parts["_rels/.rels"].replace(b'Target="/', b'Target="')
    wb = parts["xl/workbook.xml"]
    wb = re.sub(rb"<calcPr[^>]*/>", b'<calcPr calcId="191029"/>', wb)
    wb = wb.replace(b"<workbookProtection/>", b"").replace(b"<definedNames/>", b"")
    wb = wb.replace(b"<workbookPr/>", b'<workbookPr defaultThemeVersion="166925"/>')
    wb = wb.replace(b' xmlns:r="%s"' % NS_REL, b"").replace(b' state="visible"', b"")
    wb = wb.replace(b'<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">',
                    b'<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="%s">' % NS_REL)
    wb = re.sub(rb"<workbookView [^>]*/>", b'<workbookView xWindow="-110" yWindow="-110" windowWidth="23260" '
                b'windowHeight="12460"/>', wb)
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
    head = ["[Content_Types].xml", "_rels/.rels", "xl/workbook.xml", "xl/_rels/workbook.xml.rels"] + sheets
    tail = ["xl/theme/theme1.xml", "xl/styles.xml", "xl/sharedStrings.xml", "docProps/core.xml", "docProps/app.xml"]
    rest = [n for n in parts if n not in head and n not in tail]
    return head + rest + [n for n in tail if n in parts]


def _word(parts, company):
    xml = parts["word/document.xml"].decode("utf-8")
    paras = re.findall(r"<w:p[ >].*?</w:p>", xml, flags=re.S)
    texts = ["".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p)) for p in paras]
    text = " ".join(t for t in texts if t)
    words = len(text.split())
    chars = len(text.replace(" ", ""))
    n_par = sum(1 for t in texts if t.strip())
    lines = max(n_par, int(round(len(text) / 92.0)))
    pages = max(1, -(-words // 480))
    a = parts["docProps/app.xml"]
    for tag, val in (("Words", words), ("Characters", chars), ("Pages", pages), ("CharactersWithSpaces", len(text)),
                     ("Lines", lines), ("Paragraphs", n_par), ("TotalTime", 41)):
        a = re.sub(("<%s>[^<]*</%s>" % (tag, tag)).encode(), ("<%s>%d</%s>" % (tag, val, tag)).encode(), a)
    a = re.sub(rb"<Application>[^<]*</Application>", b"<Application>Microsoft Office Word</Application>", a)
    a = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0000</AppVersion>", a)
    a = re.sub(rb"<Company/>|<Company>[^<]*</Company>", b"<Company>" + company.encode() + b"</Company>", a)
    a = re.sub(rb"<TitlesOfParts>.*?</TitlesOfParts>", b'<TitlesOfParts><vt:vector size="1" baseType="lpstr"><vt:lpstr>'
               b"</vt:lpstr></vt:vector></TitlesOfParts>", a, flags=re.S)
    parts["docProps/app.xml"] = a
    # the template's thumbnail is a blank page; Word saves none unless asked to
    parts.pop("docProps/thumbnail.jpeg", None)
    parts["_rels/.rels"] = re.sub(rb'<Relationship [^>]*metadata/thumbnail[^>]*/>', b"", parts["_rels/.rels"])
    if not any(n.endswith((".jpeg", ".jpg")) for n in parts):
        parts["[Content_Types].xml"] = re.sub(rb'<Default Extension="jpeg"[^>]*/>', b"", parts["[Content_Types].xml"])
    return list(parts)


def finish_office(path, created, modified, company):
    """lay an xlsx or docx out as Office saves it, with the document's own created and modified stamps"""
    with zipfile.ZipFile(path) as z:
        order = [i.filename for i in z.infolist()]
        parts = {n: z.read(n) for n in order}
    _core(parts, created, modified)
    if path.endswith(".xlsx"):
        names = _excel(parts, company)
    else:
        _word(parts, company)
        names = [n for n in order if n in parts]
    for n in names:
        if n.endswith((".xml", ".rels")) and not parts[n].lstrip().startswith(b"<?xml"):
            parts[n] = DECL + parts[n]
    with zipfile.ZipFile(path, "w") as z:
        for n in names:
            zi = zipfile.ZipInfo(n, date_time=OFFICE_ENTRY_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.create_system = 0
            z.writestr(zi, parts[n])
    s = _scrubber()
    names_found, bad = s.audit(path, FLOOR, CEILING)
    assert not names_found and not bad, (path, names_found, bad)
