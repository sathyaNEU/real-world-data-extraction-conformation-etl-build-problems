"""Make the office containers read as saved by the applications the fiction says made them, and reproducible:
Excel's own workbook, sheet and style parts for workbooks, Word's own parts for documents (namespaces, styles in
use, font table, settings, revision ids, paragraph ids, field results and page count from a real render), Office's
zip entries (Windows, 1980 stamps, Office's order), and a PDF rewritten through pypdf with the authoring
application's metadata, XMP packet and font subset names."""
import datetime as dt
import hashlib
import os
import random
import re
import shutil
import subprocess
import tempfile
import zipfile
from xml.sax.saxutils import escape

OFFICE_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
DECL = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
XLSX_ORDER = ["[Content_Types].xml", "_rels/.rels", "xl/workbook.xml", "xl/_rels/workbook.xml.rels"]
DOCX_ORDER = ["[Content_Types].xml", "_rels/.rels", "word/document.xml", "word/_rels/document.xml.rels"]
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"


def _iso(t):
    return "%04d-%02d-%02dT%02d:%02d:%02dZ" % tuple(t[:6])


def _hex(seed, n=8):
    return hashlib.md5(seed.encode()).hexdigest()[:n].upper()


def _guid(seed):
    h = hashlib.md5(seed.encode()).hexdigest().upper()
    return "{%s-%s-4%s-%s%s-%s}" % (h[:8], h[8:12], h[13:16], "89AB"[int(h[16], 16) % 4], h[17:20], h[20:32])


def _decl(x):
    """the XML declaration Office writes, on its own line"""
    x = re.sub(r"^\s*<\?xml[^>]*\?>\s*", "", x)
    return DECL + x


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
            zi.create_system = 0                # MS-DOS attributes, as Office writes its packages on Windows
            zi.create_version = 45
            zi.extract_version = 20
            z.writestr(zi, data[name])
    _zero_attrs(path)


def _zero_attrs(path):
    """no file attributes on the entries, as Office leaves them (zipfile fills in Unix permissions when given none)"""
    b = bytearray(open(path, "rb").read())
    end = b.rfind(b"PK\x05\x06")
    count = int.from_bytes(b[end + 10:end + 12], "little")
    i = int.from_bytes(b[end + 16:end + 20], "little")
    for _ in range(count):
        assert b[i:i + 4] == b"PK\x01\x02"
        n, m, k = (int.from_bytes(b[i + j:i + j + 2], "little") for j in (28, 30, 32))
        b[i + 38:i + 42] = b"\x00\x00\x00\x00"
        i += 46 + n + m + k
    open(path, "wb").write(bytes(b))


def _core(creator, last_by, created, modified, revision=None, title=None):
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
    return (DECL + '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            + "".join(parts) + "</cp:coreProperties>").encode("utf-8")


def _theme(x, variant="2013"):
    """the Office theme on one line: the theme of current Office versions (Calibri Light and Calibri, the 2013 colour
    set), or for a workbook started from an Excel 2007-2010 template the theme it was made with (Cambria and Calibri,
    the 2007 colours, which is the theme the writing library starts from)"""
    x = re.sub(r">\s+<", "><", _decl(x.decode("utf-8") if isinstance(x, bytes) else x).strip()) + ""
    x = x.replace("?><a:theme", "?>\r\n<a:theme")
    if variant == "2007":
        return x.encode("utf-8")
    for tag, val in (("dk2", "44546A"), ("lt2", "E7E6E6"), ("accent1", "4472C4"), ("accent2", "ED7D31"),
                     ("accent3", "A5A5A5"), ("accent4", "FFC000"), ("accent5", "5B9BD5"), ("accent6", "70AD47"),
                     ("hlink", "0563C1"), ("folHlink", "954F72")):
        x = re.sub(r'(<a:%s>)<a:srgbClr val="[0-9A-Fa-f]{6}"/>' % tag, r'\g<1><a:srgbClr val="%s"/>' % val, x)
    x = re.sub(r'(<a:majorFont>)<a:latin typeface="[^"]*"[^>]*/>',
               r'\g<1><a:latin typeface="Calibri Light" panose="020F0302020204030204"/>', x)
    x = re.sub(r'(<a:minorFont>)<a:latin typeface="[^"]*"[^>]*/>',
               r'\g<1><a:latin typeface="Calibri" panose="020F0502020204030204"/>', x)
    for block, fonts in (("majorFont", (("Jpan", "\u6e38\u30b4\u30b7\u30c3\u30af Light"), ("Hans", "\u7b49\u7ebf Light"))),
                         ("minorFont", (("Jpan", "\u6e38\u660e\u671d"), ("Hans", "\u7b49\u7ebf")))):
        i0, i1 = x.find("<a:%s>" % block), x.find("</a:%s>" % block)
        if i0 < 0:
            continue
        part = x[i0:i1]
        for script, face in fonts:
            part = re.sub(r'<a:font script="%s" typeface="[^"]*"/>' % script, '<a:font script="%s" typeface="%s"/>' % (script, face), part)
        x = x[:i0] + part + x[i1:]
    return x.encode("utf-8")


# ---------------------------------------------------------------- workbooks

_INLINE = re.compile(r'<c ([^>]*?)t="inlineStr"([^>]*)><is><t(?: xml:space="preserve")?>(.*?)</t></is></c>', re.S)
WS_ROOT = ('<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="%s" '
           'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" mc:Ignorable="x14ac xr xr2 xr3" '
           'xmlns:x14ac="http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac" '
           'xmlns:xr="http://schemas.microsoft.com/office/spreadsheetml/2014/revision" '
           'xmlns:xr2="http://schemas.microsoft.com/office/spreadsheetml/2015/revision2" '
           'xmlns:xr3="http://schemas.microsoft.com/office/spreadsheetml/2016/revision3" xr:uid="%s">')
FONT_ORDER = ["b", "i", "strike", "condense", "extend", "outline", "shadow", "u", "vertAlign", "sz", "color", "name",
              "family", "charset", "scheme"]


def _col_width(w):
    """the width Excel stores for a column w characters wide in Calibri 11 (7-pixel digits, 5 pixels of padding)"""
    px = int(w * 7 + 5)
    return int(px / 7.0 * 256) / 256.0


def _fmt_num(v):
    s = repr(float(v))
    return s[:-2] if s.endswith(".0") else s


def _sheet(x, uid, selected):
    x = re.sub(r"^\s*<\?xml[^>]*\?>\s*", "", x)
    x = re.sub(r"<worksheet[^>]*>", lambda m: WS_ROOT % (REL, uid), x, count=1)
    x = re.sub(r"<sheetPr>.*?</sheetPr>|<sheetPr/>", "", x, flags=re.S)
    if selected:
        x = x.replace('<sheetView workbookViewId="0"', '<sheetView tabSelected="1" workbookViewId="0"', 1)
    x = re.sub(r"<sheetFormatPr[^>]*/>", '<sheetFormatPr defaultRowHeight="15" x14ac:dyDescent="0.25"/>', x)

    def col(m):
        a = dict(re.findall(r'(\w+)="([^"]*)"', m.group(0)))
        out = '<col min="%s" max="%s"' % (a["min"], a["max"])
        if "width" in a:
            out += ' width="%s"' % _fmt_num(_col_width(float(a["width"])))
        for k in ("style", "hidden", "bestFit", "customWidth", "outlineLevel", "collapsed"):
            if k in a and not (k == "hidden" and a[k] == "0"):
                out += ' %s="%s"' % (k, a[k])
        return out + "/>"

    x = re.sub(r"<col [^>]*/>", col, x)

    def row(m):
        body = m.group(2)
        refs = [int(_colnum(c)) for c in re.findall(r'<c r="([A-Z]+)\d+"', body)]
        a = m.group(1)
        spans = ' spans="%d:%d"' % (min(refs), max(refs)) if refs else ""
        r_attr = re.search(r'r="(\d+)"', a).group(1)
        rest = re.sub(r'\s*r="\d+"', "", a).strip()
        return '<row r="%s"%s%s x14ac:dyDescent="0.25">%s</row>' % (r_attr, spans, (" " + rest) if rest else "", body)

    x = re.sub(r"<row ([^>]*?)(?<!/)>(.*?)</row>", row, x, flags=re.S)
    x = re.sub(r"<pageMargins[^>]*/>", '<pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/>', x)
    # numbers carry no type, an empty styled cell no value, and the cursor sits below a frozen header
    x = re.sub(r'(<c r="[A-Z]+\d+"(?: s="\d+")?) t="n"(?=[ />])', r"\1", x)
    x = re.sub(r'(<c r="[A-Z]+\d+"(?: s="\d+")?)></c>', r"\1/>", x)
    pane = re.search(r'<pane [^>]*topLeftCell="([A-Z]+\d+)"', x)
    if pane:
        x = re.sub(r'(<selection pane="[^"]+") activeCell="A1" sqref="A1"', r'\1 activeCell="%s" sqref="%s"' % (pane.group(1), pane.group(1)), x)
    return DECL + x


def _colnum(c):
    n = 0
    for ch in c:
        n = n * 26 + ord(ch) - 64
    return n


def _styles(x):
    x = re.sub(r"^\s*<\?xml[^>]*\?>\s*", "", x)
    x = re.sub(r"<styleSheet[^>]*>", '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
               'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" mc:Ignorable="x14ac x16r2 xr" '
               'xmlns:x14ac="http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac" '
               'xmlns:x16r2="http://schemas.microsoft.com/office/spreadsheetml/2015/02/main" '
               'xmlns:xr="http://schemas.microsoft.com/office/spreadsheetml/2014/revision">', x, count=1)
    x = x.replace('<numFmts count="0"/>', "")
    # custom number formats that no cell format uses (openpyxl's default date format) are dropped, the rest renumbered
    fmts = re.findall(r'<numFmt numFmtId="(\d+)" formatCode="([^"]*)"/>', x)
    used = set(re.findall(r'<xf [^>]*numFmtId="(\d+)"', x))
    keep = [(i, c) for i, c in fmts if i in used]
    new_id = {i: str(164 + k) for k, (i, _) in enumerate(keep)}
    x = re.sub(r"<numFmts[^>]*>.*?</numFmts>", ('<numFmts count="%d">%s</numFmts>' % (len(keep), "".join(
        '<numFmt numFmtId="%s" formatCode="%s"/>' % (new_id[i], c) for i, c in keep))) if keep else "", x, flags=re.S)
    x = re.sub(r'(<xf [^>]*numFmtId=")(\d+)(")', lambda m: m.group(1) + new_id.get(m.group(2), m.group(2)) + m.group(3), x)
    x = re.sub(r'rgb="00([0-9A-Fa-f]{6})"', r'rgb="FF\1"', x)
    default = re.search(r"<fonts[^>]*><font>(.*?)</font>", x, re.S).group(1)
    base = dict(re.findall(r"<(name|family|scheme|color)\b([^>]*)/>", default))

    def font(m):
        kids = re.findall(r"<(\w+)\b([^>]*?)/>", m.group(1))
        have = {k: a for k, a in kids}
        for k in ("name", "family", "scheme"):
            if k not in have and k in base:
                have[k] = base[k]
        if "sz" not in have:
            have["sz"] = ' val="11"'
        if "color" not in have and "color" in base:
            have["color"] = base["color"]
        out = []
        for k in FONT_ORDER:
            if k in have:
                a = have[k]
                if k in ("b", "i", "strike", "condense", "extend", "outline", "shadow") and a.strip() in ('val="1"', 'val="true"', ""):
                    a = ""
                out.append("<%s%s/>" % (k, a))
        return "<font>%s</font>" % "".join(out)

    x = re.sub(r"<font>(.*?)</font>", font, x, flags=re.S)
    x = re.sub(r'<fonts count="(\d+)">', r'<fonts count="\1" x14ac:knownFonts="1">', x)
    x = x.replace("<patternFill/>", '<patternFill patternType="none"/>')
    x = re.sub(r'(<patternFill patternType="solid"><fgColor [^>]*/>)(</patternFill>)', r'\1<bgColor indexed="64"/>\2', x)

    def xf(m):
        a = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
        out = ["numFmtId", "fontId", "fillId", "borderId", "xfId"]
        s = " ".join('%s="%s"' % (k, a[k]) for k in out if k in a)
        for flag, k in (("applyNumberFormat", "numFmtId"), ("applyFont", "fontId"), ("applyFill", "fillId"),
                        ("applyBorder", "borderId")):
            if a.get(k, "0") != "0" and "xfId" in a:
                s += ' %s="1"' % flag
        for k in ("applyAlignment", "applyProtection"):
            if a.get(k) == "1":
                s += ' %s="1"' % k
        return "<xf %s%s" % (s, m.group(2))

    x = re.sub(r"<xf ([^>]*?)(/?>)", xf, x)
    x = re.sub(r"<colors><indexedColors>.*?</indexedColors></colors>", "", x, flags=re.S)
    x = x.replace(' hidden="0"', "")
    if "<dxfs" not in x:
        x = x.replace("<tableStyles", '<dxfs count="0"/><tableStyles')
    x = re.sub(r'<tableStyles[^>]*/>', '<tableStyles count="0" defaultTableStyle="TableStyleMedium2" defaultPivotStyle="PivotStyleLight16"/>', x)
    return DECL + x


# the Excel that last saved each workbook: build, window, the theme and file lineage it was started from
EXCEL = {
    "default": dict(rup="27328", lowest="7", theme="2013", theme_version="166925", window=(-108, -108, 23256, 12456),
                    docid="13_ncr:1_", coauth="47", calc="191029"),
}


def _workbook(x, seed, prof):
    sheets = re.findall(r"<sheet [^>]*/>", x)
    out = []
    for s in sheets:
        a = dict(re.findall(r'([\w:]+)="([^"]*)"', s))
        st = ' state="%s"' % a["state"] if a.get("state") not in (None, "visible") else ""
        out.append('<sheet name="%s" sheetId="%s"%s r:id="%s"/>' % (a["name"], a["sheetId"], st, a["r:id"]))
    names = re.search(r"<definedNames>.*?</definedNames>", x, re.S)
    active = re.search(r'activeTab="(\d+)"', x)
    tab = ' activeTab="%s"' % active.group(1) if active and active.group(1) != "0" else ""
    xw, yw, ww, wh = prof["window"]
    return (DECL + '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="%s" '
            'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" mc:Ignorable="x15 xr xr6 xr10 xr2" '
            'xmlns:x15="http://schemas.microsoft.com/office/spreadsheetml/2010/11/main" '
            'xmlns:xr="http://schemas.microsoft.com/office/spreadsheetml/2014/revision" '
            'xmlns:xr6="http://schemas.microsoft.com/office/spreadsheetml/2016/revision6" '
            'xmlns:xr10="http://schemas.microsoft.com/office/spreadsheetml/2016/revision10" '
            'xmlns:xr2="http://schemas.microsoft.com/office/spreadsheetml/2015/revision2">'
            '<fileVersion appName="xl" lastEdited="7" lowestEdited="%s" rupBuild="%s"/>'
            '<workbookPr defaultThemeVersion="%s"/>'
            '<xr:revisionPtr revIDLastSave="0" documentId="%s%s" xr6:coauthVersionLast="%s" xr6:coauthVersionMax="%s" '
            'xr10:uidLastSave="{00000000-0000-0000-0000-000000000000}"/>'
            '<bookViews><workbookView xWindow="%d" yWindow="%d" windowWidth="%d" windowHeight="%d"%s xr2:uid="%s"/></bookViews>'
            '<sheets>%s</sheets>%s<calcPr calcId="%s"/></workbook>'
            % (REL, prof["lowest"], prof["rup"], prof["theme_version"], prof["docid"], _guid(seed + "doc"), prof["coauth"],
               prof["coauth"], xw, yw, ww, wh, tab, _guid(seed + "view"), "".join(out), names.group(0) if names else "",
               prof["calc"]))


def _num(v):
    """a cell value written the way Excel writes a double"""
    if float(v) == int(float(v)) and abs(float(v)) < 1e15:
        return str(int(float(v)))
    return repr(float(v))


def _formula_values(x):
    """cache the value of each formula the way Excel saves it (SUM over a range, or one reference divided by,
    multiplied by, added to or taken from another), evaluated in row order"""
    vals = {}
    for ref, v in re.findall(r'<c r="([A-Z]+\d+)"(?: s="\d+")?(?: t="n")?><v>([-0-9.Ee+]+)</v></c>', x):
        vals[ref] = float(v)

    def val(ref):
        return vals.get(ref, 0.0)

    def ev(f):
        m = re.fullmatch(r"SUM\(([A-Z]+)(\d+):([A-Z]+)(\d+)\)", f)
        if m:
            c1, r1, c2, r2 = _colnum(m.group(1)), int(m.group(2)), _colnum(m.group(3)), int(m.group(4))
            return sum(val("%s%d" % (_colname(c), r)) for c in range(c1, c2 + 1) for r in range(r1, r2 + 1))
        m = re.fullmatch(r"([A-Z]+\d+)([-+*/])([A-Z]+\d+)", f)
        if m:
            a, b = val(m.group(1)), val(m.group(3))
            return {"+": a + b, "-": a - b, "*": a * b, "/": a / b}[m.group(2)]
        raise ValueError(f)

    def repl(m):
        v = ev(m.group(2))
        vals[re.search(r'r="([A-Z]+\d+)"', m.group(1)).group(1)] = v
        return "%s<f>%s</f><v>%s</v></c>" % (m.group(1), m.group(2), _num(v))

    return re.sub(r'(<c r="[A-Z]+\d+"[^>]*>)<f>([^<]+)</f><v\s*/?>(?:</v>)?</c>', repl, x)


def _colname(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def normalize_xlsx(path, creator, last_by, created, modified, company="Tarrock Hydro Distribution", seed=None, excel=None):
    """created and modified: UTC time tuples to the second, as Excel stamps them; excel: the profile of the Excel that
    saved it (EXCEL keys)"""
    seed = seed or os.path.basename(path)
    prof = dict(EXCEL["default"], **(excel or {}))
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

    for k, n in enumerate(sheets):
        x = data[n].decode("utf-8")
        x = re.sub(r'<c ([^>]*?)t="inlineStr"([^>]*)>\s*</c>', lambda m: "<c %s%s/>" % (m.group(1).rstrip() + " " if m.group(1).strip() else "", m.group(2).strip()) if ' s="' in m.group(0) else "", x)
        x = re.sub(r'<c ([^>]*?)t="inlineStr"([^>]*)/>', lambda m: "<c %s%s/>" % (m.group(1), m.group(2).strip()) if ' s="' in m.group(0) else "", x)
        x = re.sub(r'<c ([^>]*?)t="inlineStr"([^>]*)><is><t(?: xml:space="preserve")?\s*/></is></c>', "", x)
        x = _INLINE.sub(repl, x)
        data[n] = _formula_values(_sheet(x, _guid("%s-sheet-%d" % (seed, k)), k == 0)).encode("utf-8")
    if sst:
        body = "".join('<si><t%s>%s</t></si>' % (' xml:space="preserve"' if (t != t.strip()) else "", t) for t in sst)
        data["xl/sharedStrings.xml"] = (DECL + '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="%d" uniqueCount="%d">%s</sst>'
                                        % (refs, len(sst), body)).encode("utf-8")
    # package relationships as Excel numbers them: the sheets, then theme, styles and shared strings
    n = len(sheets)
    rels = ['<Relationship Id="rId%d" Type="%s/worksheet" Target="worksheets/sheet%d.xml"/>' % (i, REL, i) for i in range(1, n + 1)]
    rels.append('<Relationship Id="rId%d" Type="%s/theme" Target="theme/theme1.xml"/>' % (n + 1, REL))
    rels.append('<Relationship Id="rId%d" Type="%s/styles" Target="styles.xml"/>' % (n + 2, REL))
    if "xl/sharedStrings.xml" in data:
        rels.append('<Relationship Id="rId%d" Type="%s/sharedStrings" Target="sharedStrings.xml"/>' % (n + 3, REL))
    data["xl/_rels/workbook.xml.rels"] = (DECL + '<Relationships xmlns="%s">%s</Relationships>' % (PKG_REL, "".join(rels))).encode("utf-8")
    data["_rels/.rels"] = (DECL + '<Relationships xmlns="%s"><Relationship Id="rId3" Type="%s/extended-properties" '
                           'Target="docProps/app.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" '
                           'Target="docProps/core.xml"/><Relationship Id="rId1" Type="%s/officeDocument" Target="xl/workbook.xml"/>'
                           '</Relationships>' % (PKG_REL, REL, REL)).encode("utf-8")
    ov = ['<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>']
    ov += ['<Override PartName="/xl/worksheets/sheet%d.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' % i
           for i in range(1, n + 1)]
    ov.append('<Override PartName="/xl/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>')
    ov.append('<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>')
    if "xl/sharedStrings.xml" in data:
        ov.append('<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>')
    ov.append('<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>')
    ov.append('<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>')
    data["[Content_Types].xml"] = (DECL + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                                   '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                                   '<Default Extension="xml" ContentType="application/xml"/>%s</Types>' % "".join(ov)).encode("utf-8")
    data["xl/styles.xml"] = _styles(data["xl/styles.xml"].decode("utf-8")).encode("utf-8")
    data["xl/theme/theme1.xml"] = _theme(data["xl/theme/theme1.xml"], prof["theme"])
    wb = data["xl/workbook.xml"].decode("utf-8")
    data["xl/workbook.xml"] = _workbook(wb, seed, prof).encode("utf-8")
    names = re.findall(r'<sheet [^>]*name="([^"]+)"', wb)
    app = (DECL + '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
           'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Microsoft Excel</Application>'
           '<DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop><HeadingPairs><vt:vector size="2" baseType="variant">'
           '<vt:variant><vt:lpstr>Worksheets</vt:lpstr></vt:variant><vt:variant><vt:i4>%d</vt:i4></vt:variant></vt:vector></HeadingPairs>'
           '<TitlesOfParts><vt:vector size="%d" baseType="lpstr">%s</vt:vector></TitlesOfParts><Company>%s</Company>'
           '<LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged>'
           '<AppVersion>16.0300</AppVersion></Properties>'
           % (len(names), len(names), "".join("<vt:lpstr>%s</vt:lpstr>" % n for n in names), escape(company)))
    data["docProps/app.xml"] = app.encode("utf-8")
    data["docProps/core.xml"] = _core(creator, last_by, created, modified)
    order = XLSX_ORDER + sheets + ["xl/theme/theme1.xml", "xl/styles.xml", "xl/sharedStrings.xml"]
    _write(path, list(data.items()), order)


# ---------------------------------------------------------------- documents

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W_NS = ('xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
        'xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" '
        'xmlns:w16cex="http://schemas.microsoft.com/office/word/2018/wordml/cex" '
        'xmlns:w16cid="http://schemas.microsoft.com/office/word/2016/wordml/cid" '
        'xmlns:w16="http://schemas.microsoft.com/office/word/2018/wordml" '
        'xmlns:w16du="http://schemas.microsoft.com/office/word/2023/wordml/word16du" '
        'xmlns:w16sdtdh="http://schemas.microsoft.com/office/word/2020/wordml/sdtdatahash" '
        'xmlns:w16se="http://schemas.microsoft.com/office/word/2015/wordml/symex"')
IGN = 'mc:Ignorable="w14 w15 w16se w16cid w16 w16cex w16sdtdh w16du"'
BODY_ROOT = ('xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
             'xmlns:cx="http://schemas.microsoft.com/office/drawing/2014/chartex" '
             'xmlns:cx1="http://schemas.microsoft.com/office/drawing/2015/9/8/chartex" '
             'xmlns:cx2="http://schemas.microsoft.com/office/drawing/2015/10/21/chartex" '
             'xmlns:cx3="http://schemas.microsoft.com/office/drawing/2016/5/9/chartex" '
             'xmlns:cx4="http://schemas.microsoft.com/office/drawing/2016/5/10/chartex" '
             'xmlns:cx5="http://schemas.microsoft.com/office/drawing/2016/5/11/chartex" '
             'xmlns:cx6="http://schemas.microsoft.com/office/drawing/2016/5/12/chartex" '
             'xmlns:cx7="http://schemas.microsoft.com/office/drawing/2016/5/13/chartex" '
             'xmlns:cx8="http://schemas.microsoft.com/office/drawing/2016/5/14/chartex" '
             'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
             'xmlns:aink="http://schemas.microsoft.com/office/drawing/2016/ink" '
             'xmlns:am3d="http://schemas.microsoft.com/office/drawing/2017/model3d" '
             'xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:oel="http://schemas.microsoft.com/office/2019/extlst" '
             'xmlns:r="%s" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
             'xmlns:v="urn:schemas-microsoft-com:vml" '
             'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
             'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
             'xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:w="%s" %s '
             'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
             'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" '
             'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
             'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
             'mc:Ignorable="w14 w15 w16se w16cid w16 w16cex w16sdtdh w16du wp14"' % (REL, W, W_NS))
PART_ROOT = ('xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:r="%s" xmlns:w="%s" %s %s'
             % (REL, W, W_NS, IGN))
FONTS = {
    "Calibri": ("020F0502020204030204", "swiss", "E4002EFF", "C000247B", "00000009", "000001FF"),
    "Times New Roman": ("02020603050405020304", "roman", "E0002EFF", "C000785B", "00000009", "000001FF"),
    "Calibri Light": ("020F0302020204030204", "swiss", "E4002EFF", "C000247B", "00000009", "000001FF"),
    "Arial": ("020B0604020202020204", "swiss", "E0002EFF", "C000785B", "00000009", "000001FF"),
}
DEFAULT_STYLES = ("Normal", "DefaultParagraphFont", "TableNormal", "NoList")


def _rsid(seed, k):
    return "00" + hashlib.md5(("%s-%d" % (seed, k)).encode()).hexdigest()[:6].upper()


def _root(x, tag, attrs):
    return re.sub(r"<%s\b[^>]*>" % re.escape(tag), "<%s %s>" % (tag, attrs), x, count=1)


def _clean_body(x):
    """python-docx residue out of a story part (body, header or footer)"""
    x = re.sub(r"^\s*<\?xml[^>]*\?>\s*", "", x)
    for tag in ("b", "i", "bCs", "iCs"):
        x = x.replace("<w:%s w:val=\"0\"/>" % tag, "")
    x = x.replace("<w:rPr></w:rPr>", "").replace("<w:rPr/>", "")
    x = re.sub(r'<w:r>(?:<w:rPr>(?:(?!</w:rPr>).)*</w:rPr>)?(?:<w:t(?: [^>]*)?/>|<w:t(?: [^>]*)?></w:t>)?</w:r>|<w:r/>', "", x)
    x = re.sub(r'<w:(tblW|tcW|tblInd) w:type="([^"]+)" w:w="([^"]+)"/>', r'<w:\1 w:w="\3" w:type="\2"/>', x)

    def look(m):
        a = dict(re.findall(r'w:(\w+)="([^"]*)"', m.group(0)))
        return "<w:tblLook %s/>" % " ".join('w:%s="%s"' % (k, a[k]) for k in
                                            ("val", "firstRow", "lastRow", "firstColumn", "lastColumn", "noHBand", "noVBand") if k in a)

    x = re.sub(r"<w:tblLook [^>]*/>", look, x)
    return _fonts_attr(x)


def _fonts_attr(x):
    def f(m):
        a = re.findall(r'(w:\w+)="([^"]*)"', m.group(0))
        rank = {"w:ascii": 0, "w:asciiTheme": 1, "w:eastAsia": 2, "w:eastAsiaTheme": 3, "w:hAnsi": 4, "w:hAnsiTheme": 5,
                "w:cs": 6, "w:cstheme": 7}
        a.sort(key=lambda kv: rank.get(kv[0], 9))
        return "<w:rFonts %s/>" % " ".join('%s="%s"' % kv for kv in a)
    return re.sub(r"<w:rFonts [^>]*/>", f, x)


class _Ids:
    """revision-session ids, paragraph ids and text ids, deterministic from the document's seed"""

    def __init__(self, seed, sessions):
        self.seed, self.sessions = seed, sessions
        self.rnd = random.Random(seed + "-ids")

    def _hex(self):
        return "%08X" % max(self.rnd.getrandbits(31), 1)

    def para(self):
        return self._hex()

    def text(self):
        return self._hex()

    def plan(self, n, first, last):
        """the session each paragraph was typed in, and the later session that edited it if any: a document is
        written in runs of paragraphs, later sessions insert a paragraph or a short run here and there and rewrite
        text in place, so the runs have no common length"""
        k = last - first + 1
        out, cur = [], first
        for p in range(n):
            if p and self.rnd.random() < 0.17:
                w = [max(1, 6 - 2 * j) for j in range(k)]
                cur = first + self.rnd.choices(range(k), weights=w)[0]
            edited = None
            if cur < last and self.rnd.random() < 0.15:
                edited = self.rnd.randint(cur + 1, last)
            out.append((cur, edited))
        return out


def _tag(x, ids, first, last):
    """paragraphs and table rows carry the editing session that created them (and the one that last edited them),
    Word's paragraph ids and its text ids"""
    total = len(re.findall(r"<w:p[ >]", x))
    plan = ids.plan(total, first, last)
    pos = {"p": 0}

    def tagp(m):
        created, edited = plan[min(pos["p"], total - 1)]
        pos["p"] += 1
        s0 = ids.sessions[created]
        rest = re.sub(r'\s*w:rsid\w*="[^"]*"', "", m.group(1))
        attrs = 'w14:paraId="%s" w14:textId="%s" w:rsidR="%s"' % (ids.para(), ids.text(), s0)
        if edited is not None and ids.rnd.random() < 0.4:
            attrs += ' w:rsidRPr="%s"' % ids.sessions[edited]
        attrs += ' w:rsidRDefault="%s"' % (ids.sessions[edited] if edited is not None and ids.rnd.random() < 0.6 else s0)
        if edited is not None and ids.rnd.random() < 0.5:
            attrs += ' w:rsidP="%s"' % ids.sessions[edited]
        return "<w:p %s%s>" % (attrs, rest)

    def tagr(m):
        created, _ = plan[min(pos["p"], total - 1)]
        s0 = ids.sessions[created]
        return '<w:tr w:rsidR="%s" w14:paraId="%s" w14:textId="%s" w:rsidTr="%s"%s>' % (s0, ids.para(), ids.text(), s0, m.group(2))

    def both(m):
        return tagr(m) if m.group(1) == "tr" else tagp(re.match(r"<w:p((?: [^>]*)?)>", m.group(0)))

    return re.sub(r"<w:(tr|p)((?: [^>]*)?)>", both, x)


def _prune_styles(st, used, session):
    blocks = re.findall(r'<w:style [^>]*>.*?</w:style>', st, re.S)
    by_id = {re.search(r'w:styleId="([^"]+)"', b).group(1): b for b in blocks}
    keep, todo = set(), [s for s in list(used) + list(DEFAULT_STYLES) if s in by_id]
    while todo:
        s = todo.pop()
        if s in keep:
            continue
        keep.add(s)
        for ref in re.findall(r'<w:(?:basedOn|link|next) w:val="([^"]+)"/>', by_id[s]):
            if ref in by_id and ref not in keep:
                todo.append(ref)
    kept = [b for b in blocks if re.search(r'w:styleId="([^"]+)"', b).group(1) in keep]
    kept = [re.sub(r'<w:rsid w:val="[0-9A-F]+"/>', '<w:rsid w:val="%s"/>' % session, b) for b in kept]
    head = st[:st.index("<w:style ")]
    head = re.sub(r'<w:lang w:val="[^"]*"', '<w:lang w:val="en-CA"', head, count=1)
    head = re.sub(r'<w:pPrDefault><w:pPr><w:spacing [^>]*/></w:pPr></w:pPrDefault>',
                  '<w:pPrDefault><w:pPr><w:spacing w:after="160" w:line="259" w:lineRule="auto"/></w:pPr></w:pPrDefault>', head)
    return head + "".join(kept) + "</w:styles>"


def _font_table(names):
    out = []
    for n in names:
        pan, fam, u0, u1, u2, c0 = FONTS[n]
        out.append('<w:font w:name="%s"><w:panose1 w:val="%s"/><w:charset w:val="00"/><w:family w:val="%s"/>'
                   '<w:pitch w:val="variable"/><w:sig w:usb0="%s" w:usb1="%s" w:usb2="%s" w:usb3="00000000" '
                   'w:csb0="%s" w:csb1="00000000"/></w:font>' % (n, pan, fam, u0, u1, u2, c0))
    return DECL + "<w:fonts %s>%s</w:fonts>" % (PART_ROOT, "".join(out))


def _settings(sessions, seed):
    return (DECL + '<w:settings xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
            'xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="%s" '
            'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:v="urn:schemas-microsoft-com:vml" '
            'xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:w="%s" %s '
            'xmlns:sl="http://schemas.openxmlformats.org/schemaLibrary/2006/main" %s>'
            '<w:zoom w:percent="100"/><w:proofState w:spelling="clean" w:grammar="clean"/><w:defaultTabStop w:val="720"/>'
            '<w:characterSpacingControl w:val="doNotCompress"/><w:compat>'
            '<w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/>'
            '<w:compatSetting w:name="overrideTableStyleFontSizeAndJustification" w:uri="http://schemas.microsoft.com/office/word" w:val="1"/>'
            '<w:compatSetting w:name="enableOpenTypeFeatures" w:uri="http://schemas.microsoft.com/office/word" w:val="1"/>'
            '<w:compatSetting w:name="doNotFlipMirrorIndents" w:uri="http://schemas.microsoft.com/office/word" w:val="1"/>'
            '<w:compatSetting w:name="differentiateMultirowTableHeaders" w:uri="http://schemas.microsoft.com/office/word" w:val="1"/>'
            '<w:compatSetting w:name="useWord2013TrackBottomHyphenation" w:uri="http://schemas.microsoft.com/office/word" w:val="0"/>'
            '</w:compat><w:rsids><w:rsidRoot w:val="%s"/>%s</w:rsids>'
            '<m:mathPr><m:mathFont m:val="Cambria Math"/><m:brkBin m:val="before"/><m:brkBinSub m:val="--"/>'
            '<m:smallFrac m:val="0"/><m:dispDef/><m:lMargin m:val="0"/><m:rMargin m:val="0"/><m:defJc m:val="centerGroup"/>'
            '<m:wrapIndent m:val="1440"/><m:intLim m:val="subSup"/><m:naryLim m:val="undOvr"/></m:mathPr>'
            '<w:themeFontLang w:val="en-CA"/><w:clrSchemeMapping w:bg1="light1" w:t1="dark1" w:bg2="light2" w:t2="dark2" '
            'w:accent1="accent1" w:accent2="accent2" w:accent3="accent3" w:accent4="accent4" w:accent5="accent5" '
            'w:accent6="accent6" w:hyperlink="hyperlink" w:followedHyperlink="followedHyperlink"/>'
            '<w:shapeDefaults><o:shapedefaults v:ext="edit" spidmax="1026"/><o:shapelayout v:ext="edit">'
            '<o:idmap v:ext="edit" data="1"/></o:shapelayout></w:shapeDefaults><w:decimalSymbol w:val="."/>'
            '<w:listSeparator w:val=","/><w14:docId w14:val="%s"/><w15:chartTrackingRefBased/>'
            '<w15:docId w15:val="%s"/></w:settings>'
            % (REL, W, W_NS, IGN, sessions[0], "".join('<w:rsid w:val="%s"/>' % s for s in sorted(sessions)),
               ("%08X" % (int(_hex(seed + "docid"), 16) & 0x7FFFFFFF)), _guid(seed + "w15")))


def _page_count(data, order):
    """pages when the document is laid out, from a render of the package as it stands"""
    from pypdf import PdfReader
    tmp = tempfile.mkdtemp()
    try:
        src = os.path.join(tmp, "doc.docx")
        _write(src, list(data.items()), order)
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, src],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return len(PdfReader(os.path.join(tmp, "doc.pdf")).pages)
    finally:
        shutil.rmtree(tmp)


def _set_fields(x, pages):
    """the cached result of PAGE and NUMPAGES as Word saves them after laying the document out"""
    return re.sub(r'(<w:instrText xml:space="preserve"> (?:PAGE|NUMPAGES) </w:instrText></w:r>'
                  r'(?:<w:r>(?:<w:rPr>(?:(?!</w:rPr>).)*</w:rPr>)?<w:fldChar w:fldCharType="separate"/></w:r>)'
                  r'<w:r>(?:<w:rPr>(?:(?!</w:rPr>).)*</w:rPr>)?<w:t>)\d+(</w:t>)', r"\g<1>%d\g<2>" % pages, x)


def normalize_docx(path, author, last_by, created, modified, revision, total_time, title=None,
                   company="Tarrock Hydro Distribution", seed="doc"):
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    data = dict(items)
    for n in [n for n in data if n.startswith("customXml/") or n in ("word/stylesWithEffects.xml", "docProps/thumbnail.jpeg")]:
        del data[n]
    stories = ["word/document.xml"] + sorted(n for n in data if re.fullmatch(r"word/(header|footer)\d+\.xml", n))
    doc_paras = len(re.findall(r"<w:p[ >]", data["word/document.xml"].decode("utf-8")))
    sessions = [_rsid(seed, k) for k in range(max(2, min(6, 1 + doc_paras // 12)))]
    ids = _Ids(seed, sessions)
    for n in stories:
        x = _clean_body(data[n].decode("utf-8"))
        tag = "w:document" if n == "word/document.xml" else ("w:hdr" if "header" in n else "w:ftr")
        x = _root(x, tag, BODY_ROOT)
        if n == "word/document.xml":
            x = _tag(x, ids, 0, len(sessions) - 1)
            x = re.sub(r"<w:sectPr\b[^>]*>", '<w:sectPr w:rsidR="%s" w:rsidSect="%s">' % (sessions[0], sessions[0]), x)
        else:
            x = _tag(x, ids, 0, 0)
        data[n] = (DECL + x).encode("utf-8")
    used = set()
    for n in stories:
        used |= set(re.findall(r'w:(?:pStyle|rStyle|tblStyle) w:val="([^"]+)"', data[n].decode("utf-8")))
    st = re.sub(r"^\s*<\?xml[^>]*\?>\s*", "", data["word/styles.xml"].decode("utf-8"))
    st = _fonts_attr(_root(_prune_styles(st, used, sessions[0]), "w:styles", PART_ROOT))
    data["word/styles.xml"] = (DECL + st).encode("utf-8")
    body = "".join(data[n].decode("utf-8") for n in stories) + st
    if "word/numbering.xml" in data and "w:numId" not in body:
        del data["word/numbering.xml"]
    fonts = ["Calibri", "Times New Roman"] + [f for f in ("Arial",) if 'w:ascii="%s"' % f in body] + ["Calibri Light"]
    data["word/fontTable.xml"] = _font_table(fonts).encode("utf-8")
    data["word/settings.xml"] = _settings(sessions, seed).encode("utf-8")
    data["word/webSettings.xml"] = (DECL + "<w:webSettings %s><w:optimizeForBrowser/><w:allowPNG/></w:webSettings>"
                                    % PART_ROOT).encode("utf-8")
    data["word/theme/theme1.xml"] = _theme(data["word/theme/theme1.xml"])
    # relationships numbered as Word numbers them, and the references in the stories with them
    old = re.findall(r'<Relationship ([^>]*)/>', data["word/_rels/document.xml.rels"].decode("utf-8"))
    rels = [dict(re.findall(r'(\w+)="([^"]*)"', r)) for r in old]
    rels = [r for r in rels if not r["Target"].startswith("../customXml") and r["Target"] != "stylesWithEffects.xml"
            and (r["Target"] != "numbering.xml" or "word/numbering.xml" in data)]
    rank = {"styles": 0, "settings": 1, "webSettings": 2, "numbering": 3, "footnotes": 4, "endnotes": 5, "header": 6,
            "footer": 7, "image": 8, "fontTable": 9, "theme": 10}
    rels.sort(key=lambda r: (rank.get(r["Type"].rsplit("/", 1)[1], 8), r["Target"]))
    remap = {r["Id"]: "rId%d" % (i + 1) for i, r in enumerate(rels)}
    for n in stories:
        data[n] = re.sub(r'(r:(?:id|embed)=")(rId\d+)(")', lambda m: m.group(1) + remap.get(m.group(2), m.group(2)) + m.group(3),
                         data[n].decode("utf-8")).encode("utf-8")
    data["word/_rels/document.xml.rels"] = (DECL + '<Relationships xmlns="%s">%s</Relationships>' % (PKG_REL, "".join(
        '<Relationship Id="%s" Type="%s" Target="%s"/>' % (remap[r["Id"]], r["Type"], r["Target"]) for r in rels))).encode("utf-8")
    data["_rels/.rels"] = (DECL + '<Relationships xmlns="%s"><Relationship Id="rId3" Type="%s/extended-properties" '
                           'Target="docProps/app.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" '
                           'Target="docProps/core.xml"/><Relationship Id="rId1" Type="%s/officeDocument" Target="word/document.xml"/>'
                           '</Relationships>' % (PKG_REL, REL, REL)).encode("utf-8")
    ct = ['<Default Extension="%s" ContentType="%s"/>' % e for e in
          (("png", "image/png"), ("rels", "application/vnd.openxmlformats-package.relationships+xml"), ("xml", "application/xml"))
          if e[0] != "png" or any(k.endswith(".png") for k in data)]
    parts = [("/word/document.xml", "wordprocessingml.document.main+xml"), ("/word/numbering.xml", "wordprocessingml.numbering+xml"),
             ("/word/styles.xml", "wordprocessingml.styles+xml"), ("/word/settings.xml", "wordprocessingml.settings+xml"),
             ("/word/webSettings.xml", "wordprocessingml.webSettings+xml")]
    parts += [("/" + n, "wordprocessingml.%s+xml" % ("header" if "header" in n else "footer")) for n in stories[1:]]
    parts += [("/word/fontTable.xml", "wordprocessingml.fontTable+xml"), ("/word/theme/theme1.xml", "theme+xml")]
    ct += ['<Override PartName="%s" ContentType="application/vnd.openxmlformats-officedocument.%s"/>' % p for p in parts if p[0][1:] in data]
    ct.append('<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>')
    ct.append('<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>')
    data["[Content_Types].xml"] = (DECL + '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">%s</Types>'
                                   % "".join(ct)).encode("utf-8")
    order = DOCX_ORDER + stories[1:] + ["word/media/image1.png", "word/numbering.xml", "word/theme/theme1.xml",
                                        "word/settings.xml", "word/styles.xml", "word/webSettings.xml", "word/fontTable.xml"]
    data["docProps/core.xml"] = _core(author, last_by, created, modified, revision, title)
    data["docProps/app.xml"] = (DECL + '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
                                'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"/>').encode("utf-8")
    pages = _page_count(data, order)
    for n in stories[1:]:
        data[n] = _set_fields(data[n].decode("utf-8"), pages).encode("utf-8")
    doc = data["word/document.xml"].decode("utf-8")
    text = " ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", doc))
    words = len(text.split())
    chars = len(text.replace(" ", ""))
    npara = len([p for p in re.findall(r"<w:p [^>]*>(.*?)</w:p>", doc, flags=re.S) if "<w:t" in p])
    tp = ('<HeadingPairs><vt:vector size="2" baseType="variant"><vt:variant><vt:lpstr>Title</vt:lpstr></vt:variant>'
          '<vt:variant><vt:i4>1</vt:i4></vt:variant></vt:vector></HeadingPairs><TitlesOfParts><vt:vector size="1" '
          'baseType="lpstr"><vt:lpstr>%s</vt:lpstr></vt:vector></TitlesOfParts>' % escape(title)) if title else ""
    app = (DECL + '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
           'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Template>Normal.dotm</Template>'
           '<TotalTime>%d</TotalTime><Pages>%d</Pages><Words>%d</Words><Characters>%d</Characters>'
           '<Application>Microsoft Office Word</Application><DocSecurity>0</DocSecurity><Lines>%d</Lines>'
           '<Paragraphs>%d</Paragraphs><ScaleCrop>false</ScaleCrop>%s<Company>%s</Company><LinksUpToDate>false</LinksUpToDate>'
           '<CharactersWithSpaces>%d</CharactersWithSpaces><SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged>'
           '<AppVersion>16.0000</AppVersion></Properties>'
           % (total_time, pages, words, chars, max(1, words // 11), npara, tp, escape(company), len(text)))
    data["docProps/app.xml"] = app.encode("utf-8")
    _write(path, list(data.items()), order)
    return pages


# ---------------------------------------------------------------- PDF

PS_NAMES = {"LiberationSans": "ArialMT", "LiberationSans-Bold": "Arial-BoldMT", "LiberationSans-Italic": "Arial-ItalicMT",
            "LiberationSans-BoldItalic": "Arial-BoldItalicMT", "Carlito": "Calibri", "Carlito-Bold": "Calibri-Bold",
            "Carlito-Italic": "Calibri-Italic", "Carlito-BoldItalic": "Calibri-BoldItalic"}


def _xmp(title, author, app, when, uuid):
    stamp = when.strftime("%Y-%m-%dT%H:%M:%S") + when.strftime("%z")[:3] + ":" + when.strftime("%z")[3:]
    body = ('<?xpacket begin="\ufeff" id="W5M0MpCehiHzreSzNTczkc9d"?><x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="3.1-701">\n'
            '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n'
            '<rdf:Description rdf:about=""  xmlns:pdf="http://ns.adobe.com/pdf/1.3/">\n'
            '<pdf:Producer>%s</pdf:Producer></rdf:Description>\n'
            '<rdf:Description rdf:about=""  xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
            '<dc:title><rdf:Alt><rdf:li xml:lang="x-default">%s</rdf:li></rdf:Alt></dc:title>'
            '<dc:creator><rdf:Seq><rdf:li>%s</rdf:li></rdf:Seq></dc:creator></rdf:Description>\n'
            '<rdf:Description rdf:about=""  xmlns:xmp="http://ns.adobe.com/xap/1.0/">\n'
            '<xmp:CreatorTool>%s</xmp:CreatorTool><xmp:CreateDate>%s</xmp:CreateDate><xmp:ModifyDate>%s</xmp:ModifyDate>'
            '</rdf:Description>\n<rdf:Description rdf:about=""  xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/">\n'
            '<xmpMM:DocumentID>uuid:%s</xmpMM:DocumentID><xmpMM:InstanceID>uuid:%s</xmpMM:InstanceID></rdf:Description>\n'
            '</rdf:RDF></x:xmpmeta>\n' % (escape(app), escape(title), escape(author), escape(app), stamp, stamp, uuid, uuid))
    pad = "\n".join(" " * 99 for _ in range(20))
    return (body + pad + '\n<?xpacket end="w"?>').encode("utf-8")


def normalize_pdf(path, title, author, when, uid, lang="en-CA", app="Microsoft Word for Microsoft 365"):
    """Rewrite the PDF through pypdf with a fresh cross-reference table: the document information and an XMP packet as
    the authoring application writes them, the document id, random-looking subset tags on the PostScript names of the
    faces the document set, and no converter's checksum or binary marker. when: a timezone-aware local datetime."""
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import ArrayObject, ByteStringObject, DecodedStreamObject, NameObject, TextStringObject
    w = PdfWriter(clone_from=PdfReader(path))
    rnd = random.Random(uid)
    tags = {}
    for page in w.pages:
        for ref in page["/Resources"]["/Font"].values():
            font = ref.get_object()
            group = [font] + [d.get_object() for d in font.get("/DescendantFonts", [])]
            for f in group:
                base = str(f["/BaseFont"])[1:]
                face = base.split("+", 1)[-1]
                if face not in tags:
                    tags[face] = "".join(rnd.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(6))
                name = NameObject("/%s+%s" % (tags[face], PS_NAMES.get(face, face)))
                f[NameObject("/BaseFont")] = name
                if "/FontDescriptor" in f:
                    f["/FontDescriptor"].get_object()[NameObject("/FontName")] = name
    stamp = when.strftime("D:%Y%m%d%H%M%S") + when.strftime("%z")[:3] + "'" + when.strftime("%z")[3:] + "'"
    w.metadata = {"/Title": title, "/Author": author, "/Creator": app, "/CreationDate": stamp, "/ModDate": stamp,
                  "/Producer": app}
    xmp = DecodedStreamObject()
    xmp.set_data(_xmp(title, author, app, when, uid))
    xmp.update({NameObject("/Type"): NameObject("/Metadata"), NameObject("/Subtype"): NameObject("/XML")})
    root = w.root_object
    for k in ("/OpenAction", "/PageMode"):
        if k in root:
            del root[k]
    root[NameObject("/Metadata")] = w._add_object(xmp)
    root[NameObject("/Lang")] = TextStringObject(lang)
    raw = bytes.fromhex(uid.replace("-", ""))
    w._ID = ArrayObject([ByteStringObject(raw), ByteStringObject(raw)])
    w.pdf_header = "%PDF-1.7"
    with open(path, "wb") as fh:
        w.write(fh)
    b = open(path, "rb").read()
    b = b.replace(b"%\xE2\xE3\xCF\xD3\n", b"%\xB5\xB5\xB5\xB5\n", 1)
    open(path, "wb").write(b)
