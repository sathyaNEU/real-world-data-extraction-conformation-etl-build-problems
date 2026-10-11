"""Make the containers reproducible and true to the fiction: office files carry their owner and their own
saved stamps, not the writing library and the build clock; PDFs carry their issue date and no library
banner. Every substitution keeps byte lengths where the format needs it."""
import re
import zipfile

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


def normalize_ooxml(path, creator, last_by, created, modified, title=None):
    """created and modified as ISO stamps (UTC, ending Z). Entries keep their names and order (a workbook's
    take Excel's, with its strings shared and an XML declaration on every part); every entry gets the 1980
    stamp Office writes, so two builds of the same content are byte-identical."""
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
                data = data.replace(b"</Properties>", b"<Company>Southern Inland Local Health District</Company></Properties>")
        out.append((name, data))
    if ext == ".xlsx":
        out = [(n, d if d.startswith(b"<?xml") else XML_DECL + d) for n, d in share_strings(out)]
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
    for banner in (b"ReportLab Generated PDF document (opensource)", b"ReportLab generated PDF document -- digest (opensource)"):
        b = b.replace(banner, b" " * len(banner))
    assert len(b) == n and b"ReportLab" not in b and b"reportlab" not in b
    open(path, "wb").write(b)
