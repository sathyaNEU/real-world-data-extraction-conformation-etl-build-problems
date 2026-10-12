"""Make the containers reproducible and true to the fiction: office files carry their owner and their own
saved stamps, not the writing library and the build clock; PDFs carry their issue date and no library
banner. Every substitution keeps byte lengths where the format needs it."""
import re
import zipfile

COMPANY = "Kestrel Bend Irrigation District"

APP = {".xlsx": ("Microsoft Excel", "16.0300"), ".docx": ("Microsoft Office Word", "16.0000"),
       ".pptx": ("Microsoft Office PowerPoint", "16.0000")}
XML_DECL = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
INLINE = re.compile(rb'<c((?: [a-zA-Z:]+="[^"]*")*?) t="inlineStr"((?: [a-zA-Z:]+="[^"]*")*)><is><t>(.*?)</t></is></c>')
# the part order Excel writes when it saves a workbook
EXCEL_ORDER = ("[Content_Types].xml", "_rels/.rels", "xl/workbook.xml", "xl/_rels/workbook.xml.rels", "xl/worksheets/",
               "xl/theme/", "xl/styles.xml", "xl/sharedStrings.xml", "docProps/core.xml", "docProps/app.xml")


def _sheet_no(name):
    return int(re.search(r"sheet(\d+)\.xml$", name).group(1))


def share_strings(items):
    """Excel keeps a workbook's text in one shared-strings table; the writing library puts it inline in each
    cell. Move every inline string into xl/sharedStrings.xml (first use, sheet by sheet), register the part,
    and put the parts in the order Excel saves them. Cell values are unchanged."""
    parts = dict(items)
    table, index, refs = [], {}, [0]

    def to_shared(m):
        text = m.group(3)
        if text not in index:
            index[text] = len(table)
            table.append(text)
        refs[0] += 1
        return b'<c%s t="s"%s><v>%d</v></c>' % (m.group(1), m.group(2), index[text])

    for name in sorted((n for n in parts if n.startswith("xl/worksheets/sheet")), key=_sheet_no):
        parts[name] = INLINE.sub(to_shared, parts[name])
        assert b'inlineStr' not in parts[name], name
    si = b"".join(b'<si><t xml:space="preserve">%s</t></si>' % t if t[:1].isspace() or t[-1:].isspace()
                  else b"<si><t>%s</t></si>" % t for t in table)
    parts["xl/sharedStrings.xml"] = (XML_DECL + b'<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
                                     b' count="%d" uniqueCount="%d">%s</sst>' % (refs[0], len(table), si))
    ct = parts["[Content_Types].xml"]
    parts["[Content_Types].xml"] = ct.replace(b"</Types>", b'<Override PartName="/xl/sharedStrings.xml" ContentType='
                                              b'"application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings'
                                              b'+xml"/></Types>')
    rels = parts["xl/_rels/workbook.xml.rels"]
    rid = 1 + max(int(n) for n in re.findall(rb'Id="rId(\d+)"', rels))
    parts["xl/_rels/workbook.xml.rels"] = rels.replace(b"</Relationships>", b'<Relationship Type="http://schemas.'
                                                       b'openxmlformats.org/officeDocument/2006/relationships/'
                                                       b'sharedStrings" Target="sharedStrings.xml" Id="rId%d"/>'
                                                       b'</Relationships>' % rid)

    def rank(name):
        for i, p in enumerate(EXCEL_ORDER):
            if name == p or (p.endswith("/") and name.startswith(p)):
                return (i, _sheet_no(name) if p == "xl/worksheets/" else 0, name)
        return (len(EXCEL_ORDER), 0, name)
    return sorted(parts.items(), key=lambda kv: rank(kv[0]))


MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_SHEET = "application/vnd.openxmlformats-officedocument.spreadsheetml"
X14AC = "http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac"
X15 = "http://schemas.microsoft.com/office/spreadsheetml/2010/11/main"


def _guid(*keys):
    import uuid
    return "{%s}" % str(uuid.uuid5(uuid.NAMESPACE_URL, "/".join(keys))).upper()


def _width(w):
    """A column width as Excel stores it: whole characters of the default font plus its 5-pixel padding."""
    import math
    return math.floor((float(w) * 7 + 5) / 7 * 256) / 256


def _col_index(ref):
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group(0):
        n = n * 26 + ord(ch) - 64
    return n


def _excel_styles(data):
    """The workbook's styles as Excel writes them: every font spelled out, fills with their alpha, the cell formats
    with their apply flags, only the number formats in use, Excel's own default styles and no legacy palette."""
    import xml.etree.ElementTree as ET
    ns = {"m": MAIN}
    root = ET.fromstring(data)
    fmts = {int(e.get("numFmtId")): e.get("formatCode") for e in root.findall("m:numFmts/m:numFmt", ns)}
    xfs = []
    for e in root.findall("m:cellXfs/m:xf", ns):
        al = e.find("m:alignment", ns)
        xfs.append(dict(num=int(e.get("numFmtId")), font=int(e.get("fontId")), fill=int(e.get("fillId")),
                        border=int(e.get("borderId")), align=dict(al.attrib) if al is not None else {}))
    used = []
    for x in xfs:
        if x["num"] >= 164 and x["num"] not in used:
            used.append(x["num"])
    renum = {old: 164 + k for k, old in enumerate(used)}
    out = ['<styleSheet xmlns="%s" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
           'mc:Ignorable="x14ac x16r2 xr" xmlns:x14ac="%s" '
           'xmlns:x16r2="http://schemas.microsoft.com/office/spreadsheetml/2015/02/main" '
           'xmlns:xr="http://schemas.microsoft.com/office/spreadsheetml/2014/revision">' % (MAIN, X14AC)]
    if used:
        out.append('<numFmts count="%d">%s</numFmts>' % (len(used), "".join(
            '<numFmt numFmtId="%d" formatCode="%s"/>' % (renum[o], fmts[o]) for o in used)))
    fonts = []
    for f in root.findall("m:fonts/m:font", ns):
        get = lambda tag: f.find("m:" + tag, ns)
        parts = []
        if get("b") is not None and get("b").get("val", "1") not in ("0", "false"):
            parts.append("<b/>")
        if get("i") is not None and get("i").get("val", "1") not in ("0", "false"):
            parts.append("<i/>")
        parts.append('<sz val="%s"/>' % (get("sz").get("val") if get("sz") is not None else "11"))
        parts.append('<color theme="1"/>')
        parts.append('<name val="%s"/>' % (get("name").get("val") if get("name") is not None else "Calibri"))
        parts.append('<family val="2"/><scheme val="minor"/>')
        fonts.append("<font>%s</font>" % "".join(parts))
    out.append('<fonts count="%d" x14ac:knownFonts="1">%s</fonts>' % (len(fonts), "".join(fonts)))
    fills = []
    for f in root.findall("m:fills/m:fill", ns):
        pf = f.find("m:patternFill", ns)
        kind = pf.get("patternType") if pf is not None else None
        if kind == "solid":
            rgb = pf.find("m:fgColor", ns).get("rgb")
            fills.append('<fill><patternFill patternType="solid"><fgColor rgb="FF%s"/><bgColor indexed="64"/>'
                         '</patternFill></fill>' % rgb[-6:])
        else:
            fills.append('<fill><patternFill patternType="%s"/></fill>' % (kind or "none"))
    out.append('<fills count="%d">%s</fills>' % (len(fills), "".join(fills)))
    out.append('<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
               '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>')
    cells = []
    for x in xfs:
        num = renum.get(x["num"], x["num"])
        attrs = 'numFmtId="%d" fontId="%d" fillId="%d" borderId="%d" xfId="0"' % (num, x["font"], x["fill"], x["border"])
        attrs += ' applyNumberFormat="1"' if num else ""
        attrs += ' applyFont="1"' if x["font"] else ""
        attrs += ' applyFill="1"' if x["fill"] else ""
        if x["align"]:
            al = "".join(' %s="%s"' % (k, x["align"][k]) for k in ("horizontal", "vertical", "wrapText") if k in x["align"])
            cells.append('<xf %s applyAlignment="1"><alignment%s/></xf>' % (attrs, al))
        else:
            cells.append("<xf %s/>" % attrs)
    out.append('<cellXfs count="%d">%s</cellXfs>' % (len(cells), "".join(cells)))
    out.append('<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles><dxfs count="0"/>'
               '<tableStyles count="0" defaultTableStyle="TableStyleMedium2" defaultPivotStyle="PivotStyleLight16"/>'
               '<extLst><ext uri="{EB79DEF2-80B8-43e5-95BD-54CBDDF9020C}" '
               'xmlns:x14="http://schemas.microsoft.com/office/spreadsheetml/2009/9/main">'
               '<x14:slicerStyles defaultSlicerStyle="SlicerStyleLight1"/></ext>'
               '<ext uri="{9260A510-F301-46a8-8635-F512D64BE5F5}" xmlns:x15="%s">'
               '<x15:timelineStyles defaultTimelineStyle="TimeSlicerStyleLight1"/></ext></extLst></styleSheet>' % X15)
    return XML_DECL + "".join(out).encode(), renum


def _excel_sheet(data, key, first):
    """A worksheet as Excel writes it: its namespaces and revision id, the frozen panes' selections, Excel's row and
    column records and page margins, numbers without an explicit type."""
    s = data.decode()
    s = re.sub(r"<\?xml[^>]*\?>\s*", "", s)
    s = s.replace('<worksheet xmlns="%s">' % MAIN,
                  '<worksheet xmlns="%s" xmlns:r="%s" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
                  'mc:Ignorable="x14ac xr xr2 xr3" xmlns:x14ac="%s" '
                  'xmlns:xr="http://schemas.microsoft.com/office/spreadsheetml/2014/revision" '
                  'xmlns:xr2="http://schemas.microsoft.com/office/spreadsheetml/2015/revision2" '
                  'xmlns:xr3="http://schemas.microsoft.com/office/spreadsheetml/2016/revision3" xr:uid="%s">'
                  % (MAIN, REL, X14AC, _guid(key, "sheet")), 1)
    s = re.sub(r"<sheetPr>(.*?)</sheetPr>", lambda m: '<sheetPr><pageSetUpPr fitToPage="1"/></sheetPr>'
               if 'fitToPage="1"' in m.group(1) else "", s, count=1)
    pane = re.search(r'<pane xSplit="(\d+)" ySplit="(\d+)" topLeftCell="([A-Z]+\d+)"', s)
    if pane:
        tl = pane.group(3)
        col = re.match(r"[A-Z]+", tl).group(0)
        row = re.search(r"\d+", tl).group(0)
        sel = ('<selection pane="topRight" activeCell="%s1" sqref="%s1"/><selection pane="bottomLeft" activeCell="A%s" '
               'sqref="A%s"/><selection pane="bottomRight" activeCell="%s" sqref="%s"/>' % (col, col, row, row, tl, tl))
        s = re.sub(r'<selection pane="topRight"/><selection pane="bottomLeft"/><selection pane="bottomRight"[^>]*/>', sel, s)
    if first:
        s = s.replace('<sheetView workbookViewId="0">', '<sheetView tabSelected="1" workbookViewId="0">', 1)
    s = re.sub(r'<sheetFormatPr[^>]*/>', '<sheetFormatPr defaultRowHeight="15" x14ac:dyDescent="0.25"/>', s)
    s = re.sub(r'<col width="([\d.]+)" customWidth="1" min="(\d+)" max="(\d+)"/>',
               lambda m: '<col min="%s" max="%s" width="%s" customWidth="1"/>' % (m.group(2), m.group(3),
                                                                                  repr(_width(m.group(1)))), s)
    s = s.replace(' t="n"', "")
    # spans: the first and last column with a cell in each block of 16 rows
    rows = {int(m.group(1)): m.group(2) for m in re.finditer(r'<row r="(\d+)"[^>]*>(.*?)</row>', s)}
    spans = {}
    for r_, body in rows.items():
        cols = [_col_index(c) for c in re.findall(r'<c r="([A-Z]+)\d+"', body)]
        if cols:
            blk = (r_ - 1) // 16
            lo, hi = spans.get(blk, (min(cols), max(cols)))
            spans[blk] = (min(lo, min(cols)), max(hi, max(cols)))

    def row_tag(m):
        r_ = int(m.group(1))
        rest = m.group(2)
        lo, hi = spans.get((r_ - 1) // 16, (1, 1))
        return '<row r="%d" spans="%d:%d"%s x14ac:dyDescent="0.25">' % (r_, lo, hi, rest)
    s = re.sub(r'<row r="(\d+)"((?: ht="[\d.]+" customHeight="1")?)>', row_tag, s)
    s = re.sub(r'<autoFilter ref="([A-Z]+\d+:[A-Z]+\d+)"/>',
               lambda m: '<autoFilter ref="%s" xr:uid="%s"/>' % (m.group(1), _guid(key, "filter")), s)
    s = re.sub(r"<pageMargins[^>]*/>",
               '<pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/>', s)
    return XML_DECL + s.encode()


def excel_dialect(items, key, app_version="16.0300", company=None):
    """Rewrite a workbook's parts in the dialect Excel saves (not the writing library's): content types and
    relationships in Excel's order with relative targets, the workbook with its file version, window and current
    calculation id, the extended properties with the sheet titles, styles, worksheets and theme as above. Cell
    values, number formats, shared strings, panes and filters are unchanged."""
    parts = dict(items)
    wb = parts["xl/workbook.xml"].decode()
    sheets = re.findall(r'<sheet [^>]*name="([^"]+)" sheetId="(\d+)"[^>]*r:id="(rId\d+)"/>', wb)
    names = [n for n, _, _ in sheets]
    defined = re.search(r"<definedNames>.*?</definedNames>", wb)
    n = len(sheets)
    parts["xl/workbook.xml"] = XML_DECL + (
        '<workbook xmlns="%s" xmlns:r="%s" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
        'mc:Ignorable="x15 xr xr6 xr10 xr2" xmlns:x15="%s" '
        'xmlns:xr="http://schemas.microsoft.com/office/spreadsheetml/2014/revision" '
        'xmlns:xr6="http://schemas.microsoft.com/office/spreadsheetml/2016/revision6" '
        'xmlns:xr10="http://schemas.microsoft.com/office/spreadsheetml/2016/revision10" '
        'xmlns:xr2="http://schemas.microsoft.com/office/spreadsheetml/2015/revision2">'
        '<fileVersion appName="xl" lastEdited="7" lowestEdited="7" rupBuild="28526"/>'
        '<workbookPr defaultThemeVersion="124226"/>'
        '<bookViews><workbookView xWindow="-110" yWindow="-110" windowWidth="25820" windowHeight="15500" '
        'xr2:uid="%s"/></bookViews><sheets>%s</sheets>%s<calcPr calcId="191029"/>'
        '<extLst><ext uri="{140A7094-0E35-4892-8432-C4D2E57EDEB5}" xmlns:x15="%s">'
        '<x15:workbookPr chartTrackingRefBase="1"/></ext></extLst></workbook>' % (
            MAIN, REL, X15, _guid(key, "view"),
            "".join('<sheet name="%s" sheetId="%d" r:id="rId%d"/>' % (nm, k + 1, k + 1) for k, nm in enumerate(names)),
            defined.group(0) if defined else "", X15)).encode()
    rel = lambda rid, kind, target: '<Relationship Id="rId%d" Type="%s/%s" Target="%s"/>' % (rid, REL, kind, target)
    parts["xl/_rels/workbook.xml.rels"] = XML_DECL + (
        '<Relationships xmlns="%s">%s%s%s%s</Relationships>' % (
            PKG_REL, "".join(rel(k, "worksheet", "worksheets/sheet%d.xml" % k) for k in range(n, 0, -1)),
            rel(n + 3, "sharedStrings", "sharedStrings.xml"), rel(n + 2, "styles", "styles.xml"),
            rel(n + 1, "theme", "theme/theme1.xml"))).encode()
    parts["_rels/.rels"] = XML_DECL + (
        '<Relationships xmlns="%s"><Relationship Id="rId3" Type="%s/extended-properties" Target="docProps/app.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/'
        'core-properties" Target="docProps/core.xml"/><Relationship Id="rId1" Type="%s/officeDocument" '
        'Target="xl/workbook.xml"/></Relationships>' % (PKG_REL, REL, REL)).encode()
    ov = lambda part, ct: '<Override PartName="%s" ContentType="%s"/>' % (part, ct)
    parts["[Content_Types].xml"] = XML_DECL + (
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>%s%s%s%s%s%s%s</Types>' % (
            ov("/xl/workbook.xml", CT_SHEET + ".sheet.main+xml"),
            "".join(ov("/xl/worksheets/sheet%d.xml" % k, CT_SHEET + ".worksheet+xml") for k in range(1, n + 1)),
            ov("/xl/theme/theme1.xml", "application/vnd.openxmlformats-officedocument.theme+xml"),
            ov("/xl/styles.xml", CT_SHEET + ".styles+xml"), ov("/xl/sharedStrings.xml", CT_SHEET + ".sharedStrings+xml"),
            ov("/docProps/core.xml", "application/vnd.openxmlformats-package.core-properties+xml"),
            ov("/docProps/app.xml", "application/vnd.openxmlformats-officedocument.extended-properties+xml"))).encode()
    parts["docProps/app.xml"] = XML_DECL + (
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Microsoft Excel'
        '</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop><HeadingPairs><vt:vector size="2" '
        'baseType="variant"><vt:variant><vt:lpstr>Worksheets</vt:lpstr></vt:variant><vt:variant><vt:i4>%d</vt:i4>'
        '</vt:variant></vt:vector></HeadingPairs><TitlesOfParts><vt:vector size="%d" baseType="lpstr">%s</vt:vector>'
        '</TitlesOfParts><Company>%s</Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false'
        '</SharedDoc><HyperlinksChanged>false</HyperlinksChanged><AppVersion>%s</AppVersion></Properties>' % (
            n, n, "".join("<vt:lpstr>%s</vt:lpstr>" % nm for nm in names), company or COMPANY, app_version)).encode()
    parts["xl/styles.xml"], _ = _excel_styles(parts["xl/styles.xml"])
    for k in range(1, n + 1):
        name = "xl/worksheets/sheet%d.xml" % k
        parts[name] = _excel_sheet(parts[name], key + "/" + names[k - 1], k == 1)
    theme = parts["xl/theme/theme1.xml"]
    parts["xl/theme/theme1.xml"] = XML_DECL + re.sub(rb">\s+<", b"><", re.sub(rb"^<\?xml[^>]*\?>\s*", b"", theme)).strip()
    order = ["[Content_Types].xml", "_rels/.rels", "xl/workbook.xml", "xl/_rels/workbook.xml.rels"] + \
        ["xl/worksheets/sheet%d.xml" % k for k in range(1, n + 1)] + \
        ["xl/theme/theme1.xml", "xl/styles.xml", "xl/sharedStrings.xml", "docProps/core.xml", "docProps/app.xml"]
    assert sorted(order) == sorted(parts), sorted(set(parts) ^ set(order))
    return [(nm, parts[nm]) for nm in order]


def normalize_ooxml(path, creator, last_by, created, modified, title=None, excel=False, company=None):
    """created and modified as ISO stamps (UTC, ending Z). Entries keep their names and order (a workbook's
    take Excel's, with its strings shared and an XML declaration on every part); every entry gets the 1980
    stamp Office writes, so two builds of the same content are byte-identical. excel=True also rewrites a
    workbook's parts in Excel's own dialect (excel_dialect)."""
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
            data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>" + app_name.encode() + b"</Application>", data)
            data = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>" + app_ver.encode() + b"</AppVersion>", data)
            if b"<Company>" not in data:
                data = data.replace(b"</Properties>", b"<Company>" + (company or COMPANY).encode() + b"</Company></Properties>")
        out.append((name, data))
    if ext == ".xlsx":
        out = [(n, d if d.startswith(b"<?xml") else XML_DECL + d) for n, d in share_strings(out)]
        if excel:
            out = excel_dialect(out, key=path.replace("\\", "/").rsplit("/", 1)[-1], company=company)
    with zipfile.ZipFile(path, "w") as z:
        for name, data in out:
            zi = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            if excel:
                zi.create_system = 0
            z.writestr(zi, data)


def normalize_pdf(path, created, modified):
    """created, modified: the in-fiction stamps as PDF dates of the invariant date's length, D:YYYYMMDDHHMMSS+HH'MM'
    (the info dictionary carries the creation date before the modification date). The library's banners are blanked
    and its sequential font-subset tags (AAAAAA+, AAAAAB+) become the six-letter tags other producers write, each
    substitution at equal length so the cross-reference offsets hold."""
    import hashlib
    b = open(path, "rb").read()
    n = len(b)
    inv = b"D:20000101000000+00'00'"
    assert len(created) == len(modified) == len(inv) and b.count(inv) == 2
    b = b.replace(inv, created, 1).replace(inv, modified, 1)
    for banner in (b"ReportLab Generated PDF document (opensource)", b"ReportLab generated PDF document -- digest (opensource)"):
        b = b.replace(banner, b" " * len(banner))
    tags = {}
    for m in re.finditer(rb"/([A-Z]{6})\+([A-Za-z0-9-]+)", b):
        key = m.group(0)
        if key not in tags:
            h = hashlib.sha256(key + created).digest()
            tags[key] = b"/" + bytes(65 + x % 26 for x in h[:6]) + b"+" + m.group(2)
    for old, new in tags.items():
        b = re.sub(re.escape(old) + rb"(?![A-Za-z0-9-])", new, b)
    assert len(b) == n and b"ReportLab" not in b and b"reportlab" not in b and b"AAAAAA+" not in b
    open(path, "wb").write(b)
