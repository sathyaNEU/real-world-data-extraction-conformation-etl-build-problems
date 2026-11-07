"""task165: OOXML packages rewritten at one fixed time (members and core properties), so two builds match."""
import io
import re
import zipfile


def _excel_app(sheets):
    """docProps/app.xml as Excel writes it for a workbook of these sheets."""
    n = len(sheets)
    parts = b"".join(b"<vt:lpstr>" + s + b"</vt:lpstr>" for s in sheets)
    return (b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
            b'<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
            b'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
            b"<Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>"
            b'<HeadingPairs><vt:vector size="2" baseType="variant"><vt:variant><vt:lpstr>Worksheets</vt:lpstr>'
            b"</vt:variant><vt:variant><vt:i4>" + str(n).encode() + b"</vt:i4></vt:variant></vt:vector></HeadingPairs>"
            b'<TitlesOfParts><vt:vector size="' + str(n).encode() + b'" baseType="lpstr">' + parts +
            b"</vt:vector></TitlesOfParts><Company>Quessling Sewer Authority</Company><LinksUpToDate>false"
            b"</LinksUpToDate><SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged>"
            b"<AppVersion>16.0300</AppVersion></Properties>")


CELL = re.compile(rb'<c ([^>]*?)t="inlineStr"><is><t(?: [^>]*)?>(.*?)</t></is></c>', re.S)


def _shared_strings(items):
    """Excel keeps cell text in xl/sharedStrings.xml; move each inline string there, in order of first use."""
    sst, index, total = [], {}, [0]

    def sub(m):
        txt = m.group(2)
        if txt not in index:
            index[txt] = len(sst)
            sst.append(txt)
        total[0] += 1
        return b'<c ' + m.group(1) + b't="s"><v>' + str(index[txt]).encode() + b'</v></c>'
    out = []
    for n, d in items:
        if n.startswith("xl/worksheets/") and n.endswith(".xml"):
            d = CELL.sub(sub, d)
        out.append((n, d))
    body = b"".join(b'<si><t' + (b' xml:space="preserve"' if t[:1] == b" " or t[-1:] == b" " else b"") + b'>' + t +
                    b'</t></si>' for t in sst)
    xml = (b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<sst xmlns="http://schemas.openxmlformats.org/'
           b'spreadsheetml/2006/main" count="' + str(total[0]).encode() + b'" uniqueCount="' + str(len(sst)).encode() +
           b'">' + body + b'</sst>')
    res = []
    for n, d in out:
        if n == "[Content_Types].xml":
            d = d.replace(b"</Types>", b'<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.'
                          b'openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/></Types>')
        if n == "xl/_rels/workbook.xml.rels":
            d = d.replace(b"</Relationships>", b'<Relationship Type="http://schemas.openxmlformats.org/officeDocument/'
                          b'2006/relationships/sharedStrings" Target="sharedStrings.xml" Id="rId99"/></Relationships>')
        res.append((n, d))
        if n == "xl/styles.xml":
            res.append(("xl/sharedStrings.xml", xml))
    if not any(n == "xl/sharedStrings.xml" for n, _ in res):
        res.append(("xl/sharedStrings.xml", xml))
    return res


def normalize(path, created, modified):
    """created, modified: naive datetimes for the core properties (written as UTC, as Office writes them)."""
    blob = normalize_bytes(open(path, "rb").read(), created, modified)
    open(path, "wb").write(blob)


def normalize_bytes(blob, created, modified):
    src = zipfile.ZipFile(io.BytesIO(blob))
    items = [(i.filename, src.read(i.filename)) for i in src.infolist()]
    src.close()
    items = [(n, normalize_bytes(d, created, modified) if n.endswith(".xlsx") else d) for n, d in items]
    names = dict(items)
    if "xl/workbook.xml" in names and "xl/sharedStrings.xml" not in names and any(
            b't="inlineStr"' in d for n, d in items if n.startswith("xl/worksheets/")):
        items = _shared_strings(items)
        names = dict(items)
    if "xl/workbook.xml" in names and "docProps/app.xml" in names:
        sheets = re.findall(rb'<sheet [^>]*name="([^"]+)"', names["xl/workbook.xml"])
        items = [(n, _excel_app(sheets) if n == "docProps/app.xml" else d) for n, d in items]
    c = created.strftime("%Y-%m-%dT%H:%M:%SZ").encode()
    m = modified.strftime("%Y-%m-%dT%H:%M:%SZ").encode()
    zt = modified.timetuple()[:6]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in items:
            if name == "docProps/core.xml":
                data = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", rb"\g<1>" + c + rb"\g<2>", data)
                data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>" + m + rb"\g<2>", data)
            zi = zipfile.ZipInfo(name, date_time=zt)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)
    return buf.getvalue()
