"""Reproducible office containers: a workbook laid out the way Excel saves one, fixed entry stamps and
in-fiction document properties; PDFs with fixed dates and document ids."""
import re
import zipfile

DECL = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
NS_REL = b"http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def normalize_xlsx(path, creator, created, modified, company="Upper Kestrel Valley Air Quality Management District"):
    with zipfile.ZipFile(path) as z:
        parts = {i.filename: z.read(i.filename) for i in z.infolist()}
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
        assert b"inlineStr" not in x
        x = re.sub(rb'(<c [^>]*?) t="n"', rb"\1", x)
        x = x.replace(b'<sheetPr><outlinePr summaryBelow="1" summaryRight="1"/><pageSetUpPr/></sheetPr>', b"")
        x = re.sub(rb"<pageMargins [^>]*/>", b'<pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" '
                   b'header="0.3" footer="0.3"/>', x)
        parts[n] = x
    if sst:
        parts["xl/sharedStrings.xml"] = (b'<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                                         b'count="%d" uniqueCount="%d">' % (count[0], len(sst))
                                         + b"".join(b"<si>" + s + b"</si>" for s in sst) + b"</sst>")
        ct = parts["[Content_Types].xml"]
        if b"/xl/sharedStrings.xml" not in ct:
            ct = ct.replace(b"</Types>", b'<Override PartName="/xl/sharedStrings.xml" ContentType="application/'
                            b'vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/></Types>')
        parts["[Content_Types].xml"] = ct
        rels = parts["xl/_rels/workbook.xml.rels"]
        if b"sharedStrings.xml" not in rels:
            rid = 1 + max(int(x) for x in re.findall(rb'Id="rId(\d+)"', rels))
            rels = rels.replace(b"</Relationships>", b'<Relationship Id="rId%d" Type="%s/sharedStrings" '
                                b'Target="sharedStrings.xml"/></Relationships>' % (rid, NS_REL))
        parts["xl/_rels/workbook.xml.rels"] = rels
    parts["_rels/.rels"] = parts["_rels/.rels"].replace(b'Target="/', b'Target="')
    parts["xl/_rels/workbook.xml.rels"] = parts["xl/_rels/workbook.xml.rels"].replace(b'Target="/xl/', b'Target="')
    wb = parts["xl/workbook.xml"]
    wb = re.sub(rb"<calcPr[^>]*/>", b'<calcPr calcId="191029"/>', wb)
    wb = wb.replace(b"<workbookProtection/>", b"").replace(b"<definedNames/>", b"")
    wb = wb.replace(b"<workbookPr/>", b'<workbookPr defaultThemeVersion="164011"/>')
    wb = re.sub(rb"<workbookView [^>]*/>", b'<workbookView xWindow="-120" yWindow="-120" windowWidth="29040" '
                b'windowHeight="15720"/>', wb)
    parts["xl/workbook.xml"] = wb
    titles = re.findall(rb'<sheet [^>]*name="([^"]*)"', wb)
    parts["docProps/app.xml"] = (
        b'<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        b'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        b"<Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>"
        b'<HeadingPairs><vt:vector size="2" baseType="variant"><vt:variant><vt:lpstr>Worksheets</vt:lpstr></vt:variant>'
        b"<vt:variant><vt:i4>%d</vt:i4></vt:variant></vt:vector></HeadingPairs>" % len(titles)
        + b'<TitlesOfParts><vt:vector size="%d" baseType="lpstr">' % len(titles)
        + b"".join(b"<vt:lpstr>" + t + b"</vt:lpstr>" for t in titles)
        + b"</vt:vector></TitlesOfParts><Company>" + company.encode() + b"</Company><LinksUpToDate>false</LinksUpToDate>"
        b"<SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion>"
        b"</Properties>")
    parts["docProps/core.xml"] = (
        b'<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        b'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
        b'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        b"<dc:creator>" + creator.encode() + b"</dc:creator><cp:lastModifiedBy>" + creator.encode()
        + b'</cp:lastModifiedBy><dcterms:created xsi:type="dcterms:W3CDTF">' + created.encode()
        + b'</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">' + modified.encode()
        + b"</dcterms:modified></cp:coreProperties>")
    for n in parts:
        if n.endswith((".xml", ".rels")) and not parts[n].startswith(b"<?xml"):
            parts[n] = DECL + parts[n]
    head = ["[Content_Types].xml", "_rels/.rels", "xl/workbook.xml", "xl/_rels/workbook.xml.rels"] + sheets
    tail = ["xl/theme/theme1.xml", "xl/styles.xml", "xl/sharedStrings.xml", "docProps/core.xml", "docProps/app.xml"]
    rest = [n for n in parts if n not in head and n not in tail]
    order = [n for n in head + rest + tail if n in parts]
    with zipfile.ZipFile(path, "w") as z:
        for name in order:
            zi = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.create_system = 0
            z.writestr(zi, parts[name])


def normalize_pdf(path, stamp, creator):
    """Carry the issuing office's date on the PDF's info dates (equal length) and replace the library's
    comment lines at equal length, so the cross-reference table stays valid."""
    b = open(path, "rb").read()
    n0 = len(b)
    fixed = b"D:20000101000000+00'00'"
    assert len(stamp) == len(fixed), stamp
    b = b.replace(fixed, stamp)
    for line in re.findall(rb"%[^\n]*ReportLab[^\n]*", b):
        b = b.replace(line, (b"% " + creator.encode()).ljust(len(line))[:len(line)])
    assert len(b) == n0 and b"ReportLab" not in b
    open(path, "wb").write(b)
