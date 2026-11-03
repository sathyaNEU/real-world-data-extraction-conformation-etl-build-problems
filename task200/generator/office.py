"""Office and PDF writers that save the way the airport's own tools save: a workbook laid out as Excel writes it, a
Word package written part by part with a lean styles part and the Office theme, a PDF stamped with its own dates and
the producing application, and every zip member dated at the save."""
import datetime as dt
import io
import re
import zipfile

_HEAD = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
_W = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')
_R = ""
_CT = "application/vnd.openxmlformats-officedocument.wordprocessingml."


def _x(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _stamp(iso):
    d = dt.datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ")
    return (d.year, d.month, d.day, d.hour, d.minute, d.second)


# ----------------------------------------------------------------------------------------------- workbook
APP_XLSX = ('<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
            'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Microsoft Excel'
            '</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop><HeadingPairs><vt:vector size="2" '
            'baseType="variant"><vt:variant><vt:lpstr>Worksheets</vt:lpstr></vt:variant><vt:variant><vt:i4>{n}</vt:i4>'
            '</vt:variant></vt:vector></HeadingPairs><TitlesOfParts><vt:vector size="{n}" baseType="lpstr">{titles}'
            '</vt:vector></TitlesOfParts><Company>{company}</Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false'
            '</SharedDoc><HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>')
CORE = ('<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">{title}'
        '<dc:creator>{author}</dc:creator><cp:lastModifiedBy>{last}</cp:lastModifiedBy>'
        '<dcterms:created xsi:type="dcterms:W3CDTF">{created}</dcterms:created>'
        '<dcterms:modified xsi:type="dcterms:W3CDTF">{modified}</dcterms:modified></cp:coreProperties>')


def xlsx(path, sheets, author, created, modified, widths=None, company="Brackenford Airport Ltd", last=None,
         title="", number_formats=None, notes_rows=None):
    """sheets: [(name, DataFrame)]; dates as datetime written dd/mm/yyyy; numbers as numbers."""
    import os
    import pandas as pd
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wb = Workbook()
    wb.remove(wb.active)
    for name, df in sheets:
        ws = wb.create_sheet(name)
        top = 1
        if notes_rows and name in notes_rows:
            for line in notes_rows[name]:
                ws.cell(row=top, column=1, value=line).font = Font(bold=(top == 1), size=11 if top == 1 else 10)
                top += 1
            top += 1
        for j, c in enumerate(df.columns, 1):
            cell = ws.cell(row=top, column=j, value=str(c))
            cell.font = Font(bold=True)
            cell.fill = PatternFill("solid", fgColor="D9E1F2")
            cell.alignment = Alignment(vertical="center", wrap_text=True)
        fmts = (number_formats or {}).get(name, {})
        for i, row in enumerate(df.itertuples(index=False), top + 1):
            for j, v in enumerate(row, 1):
                col = df.columns[j - 1]
                if isinstance(v, pd.Timestamp):
                    v = v.to_pydatetime()
                if isinstance(v, float) and v != v:
                    v = None
                if hasattr(v, "item") and not isinstance(v, (str, bytes)):
                    v = v.item()
                cell = ws.cell(row=i, column=j, value=v)
                if isinstance(v, dt.datetime):
                    cell.number_format = "dd/mm/yyyy"
                if col in fmts:
                    cell.number_format = fmts[col]
        ws.freeze_panes = ws.cell(row=top + 1, column=1)
        for j, w in enumerate((widths or {}).get(name, []), 1):
            ws.column_dimensions[get_column_letter(j)].width = w
    buf = io.BytesIO()
    wb.save(buf)
    raw = _resave_xlsx(buf.getvalue(), author, last or author, created, modified, company, title)
    with open(path, "wb") as fh:
        fh.write(raw)


def _resave_xlsx(raw, author, last, created, modified, company, title):
    zin = zipfile.ZipFile(io.BytesIO(raw))
    names = zin.namelist()
    wbx = zin.read("xl/workbook.xml").decode("utf-8")
    titles = re.findall(r'<sheet [^>]*name="([^"]*)"', wbx)
    out = io.BytesIO()
    zout = zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED)
    order = ["[Content_Types].xml", "_rels/.rels", "xl/workbook.xml", "xl/_rels/workbook.xml.rels"]
    order += sorted([n for n in names if n.startswith("xl/worksheets/")])
    order += [n for n in names if n not in order]
    stamp = _stamp(modified)
    for n in order:
        if n not in names:
            continue
        data = zin.read(n)
        if n == "docProps/app.xml":
            data = (_HEAD + APP_XLSX.format(n=len(titles), titles="".join("<vt:lpstr>%s</vt:lpstr>" % _x(t) for t in titles),
                                            company=_x(company))).encode("utf-8")
        elif n == "docProps/core.xml":
            t = "<dc:title>%s</dc:title>" % _x(title) if title else ""
            data = (_HEAD + CORE.format(title=t, author=_x(author), last=_x(last), created=created,
                                        modified=modified)).encode("utf-8")
        elif n == "xl/workbook.xml":
            s = data.decode("utf-8")
            s = re.sub(r"<workbookPr[^>]*/>", '<workbookPr defaultThemeVersion="166925"/>', s)
            s = re.sub(r'<calcPr[^>]*/>', '<calcPr calcId="191029"/>', s)
            data = s.encode("utf-8")
        zi = zipfile.ZipInfo(n, date_time=stamp)
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.create_system = 0
        zout.writestr(zi, data)
    zout.close()
    return out.getvalue()


# ----------------------------------------------------------------------------------------------- Word
_SCRIPTS = ("Jpan", "Hang", "Hans", "Hant", "Arab", "Hebr", "Thai", "Ethi", "Beng", "Gujr", "Khmr", "Knda", "Guru",
            "Cans", "Cher", "Yiii", "Tibt", "Thaa", "Deva", "Telu", "Taml", "Syrc", "Orya", "Mlym", "Laoo", "Sinh",
            "Mong", "Viet", "Uigh", "Geor", "Armn", "Bugi", "Bopo", "Java", "Lisu", "Mymr", "Nkoo", "Olck", "Osma",
            "Phag", "Syrn", "Syrj", "Syre", "Sora", "Tale", "Talu", "Tfng")
_MAJOR = ("游ゴシック Light", "맑은 고딕", "等线 Light", "新細明體", "Times New Roman", "Times New Roman", "Angsana New",
          "Nyala", "Vrinda", "Shruti", "MoolBoran", "Tunga", "Raavi", "Euphemia", "Plantagenet Cherokee",
          "Microsoft Yi Baiti", "Microsoft Himalaya", "MV Boli", "Mangal", "Gautami", "Latha", "Estrangelo Edessa",
          "Kalinga", "Kartika", "DokChampa", "Iskoola Pota", "Mongolian Baiti", "Times New Roman", "Microsoft Uighur",
          "Sylfaen", "Arial", "Leelawadee UI", "Microsoft JhengHei", "Javanese Text", "Segoe UI", "Myanmar Text",
          "Ebrima", "Nirmala UI", "Ebrima", "Phagspa", "Estrangelo Edessa", "Estrangelo Edessa", "Estrangelo Edessa",
          "Nirmala UI", "Microsoft Tai Le", "Microsoft New Tai Lue", "Ebrima")
_MINOR = ("游明朝", "맑은 고딕", "等线", "新細明體", "Arial", "Arial", "Cordia New", "Nyala", "Vrinda", "Shruti", "DaunPenh",
          "Tunga", "Raavi", "Euphemia", "Plantagenet Cherokee", "Microsoft Yi Baiti", "Microsoft Himalaya", "MV Boli",
          "Mangal", "Gautami", "Latha", "Estrangelo Edessa", "Kalinga", "Kartika", "DokChampa", "Iskoola Pota",
          "Mongolian Baiti", "Arial", "Microsoft Uighur", "Sylfaen", "Arial", "Leelawadee UI", "Microsoft JhengHei",
          "Javanese Text", "Segoe UI", "Myanmar Text", "Ebrima", "Nirmala UI", "Ebrima", "Phagspa", "Estrangelo Edessa",
          "Estrangelo Edessa", "Estrangelo Edessa", "Nirmala UI", "Microsoft Tai Le", "Microsoft New Tai Lue", "Ebrima")


def _theme():
    def fonts(tag, latin, panose, faces):
        return ('<a:%s><a:latin typeface="%s" panose="%s"/><a:ea typeface=""/><a:cs typeface=""/>%s</a:%s>' % (
            tag, latin, panose, "".join('<a:font script="%s" typeface="%s"/>' % sf for sf in zip(_SCRIPTS, faces)), tag))
    clr = "".join('<a:%s><a:srgbClr val="%s"/></a:%s>' % (k, v, k) for k, v in (
        ("dk2", "44546A"), ("lt2", "E7E6E6"), ("accent1", "4472C4"), ("accent2", "ED7D31"), ("accent3", "A5A5A5"),
        ("accent4", "FFC000"), ("accent5", "5B9BD5"), ("accent6", "70AD47"), ("hlink", "0563C1"), ("folHlink", "954F72")))
    line = ('<a:ln w="%d" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
            '<a:prstDash val="solid"/><a:miter lim="800000"/></a:ln>')

    def gs(pos, mods):
        return '<a:gs pos="%d"><a:schemeClr val="phClr">%s</a:schemeClr></a:gs>' % (
            pos, "".join('<a:%s val="%d"/>' % m for m in mods))
    grad = '<a:gradFill rotWithShape="1"><a:gsLst>%s</a:gsLst><a:lin ang="5400000" scaled="0"/></a:gradFill>'
    fill = ('<a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>' +
            grad % (gs(0, [("lumMod", 110000), ("satMod", 105000), ("tint", 67000)]) +
                    gs(50000, [("lumMod", 105000), ("satMod", 103000), ("tint", 73000)]) +
                    gs(100000, [("lumMod", 105000), ("satMod", 109000), ("tint", 81000)])) +
            grad % (gs(0, [("satMod", 103000), ("lumMod", 102000), ("tint", 94000)]) +
                    gs(50000, [("satMod", 110000), ("lumMod", 100000), ("shade", 100000)]) +
                    gs(100000, [("lumMod", 99000), ("satMod", 120000), ("shade", 78000)])) + '</a:fillStyleLst>')
    bg = ('<a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr '
          'val="phClr"><a:tint val="95000"/><a:satMod val="170000"/></a:schemeClr></a:solidFill>' +
          grad % (gs(0, [("tint", 93000), ("satMod", 150000), ("shade", 98000), ("lumMod", 102000)]) +
                  gs(50000, [("tint", 98000), ("satMod", 130000), ("shade", 90000), ("lumMod", 103000)]) +
                  gs(100000, [("shade", 63000), ("satMod", 120000)])) + '</a:bgFillStyleLst>')
    effects = ('<a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/>'
               '</a:effectStyle><a:effectStyle><a:effectLst><a:outerShdw blurRad="57150" dist="19050" dir="5400000" '
               'algn="ctr" rotWithShape="0"><a:srgbClr val="000000"><a:alpha val="63000"/></a:srgbClr></a:outerShdw>'
               '</a:effectLst></a:effectStyle></a:effectStyleLst>')
    return _HEAD + (
        '<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Office Theme">'
        '<a:themeElements><a:clrScheme name="Office"><a:dk1><a:sysClr val="windowText" lastClr="000000"/></a:dk1>'
        '<a:lt1><a:sysClr val="window" lastClr="FFFFFF"/></a:lt1>' + clr + '</a:clrScheme><a:fontScheme name="Office">' +
        fonts("majorFont", "Calibri Light", "020F0302020204030204", _MAJOR) +
        fonts("minorFont", "Calibri", "020F0502020204030204", _MINOR) + '</a:fontScheme><a:fmtScheme name="Office">' +
        fill + '<a:lnStyleLst>' + "".join(line % w for w in (6350, 12700, 19050)) + '</a:lnStyleLst>' + effects + bg +
        '</a:fmtScheme></a:themeElements><a:objectDefaults/><a:extraClrSchemeLst/><a:extLst><a:ext '
        'uri="{05A4C25C-085E-4340-85A3-A5531E510DB2}"><thm15:themeFamily '
        'xmlns:thm15="http://schemas.microsoft.com/office/thememl/2012/main" name="Office Theme" '
        'id="{62F939B6-93AF-4DB8-9C6B-D6C7DFDC589F}" vid="{4A3C46E8-61CC-4603-A589-7422A47A8E4A}"/></a:ext>'
        '</a:extLst></a:theme>')


def _run(text, bold=False):
    rpr = "<w:rPr><w:b/></w:rPr>" if bold else ""
    return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, _x(text))


def _para(style, text):
    ppr = '<w:pPr><w:pStyle w:val="%s"/></w:pPr>' % style if style else ""
    # **bold** spans inside a block
    parts = re.split(r"(\*\*[^*]+\*\*)", text)
    runs = "".join(_run(p[2:-2], True) if p.startswith("**") else _run(p) for p in parts if p)
    return "<w:p>%s%s</w:p>" % (ppr, runs)


def _table(rows, widths):
    grid = "".join('<w:gridCol w:w="%d"/>' % w for w in widths)
    out = ['<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="0" w:type="auto"/><w:tblLook w:val="04A0" '
           'w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr>'
           '<w:tblGrid>%s</w:tblGrid>' % grid]
    for i, row in enumerate(rows):
        cells = []
        for w, c in zip(widths, row):
            cells.append('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/></w:tcPr><w:p><w:pPr><w:spacing w:after="0"/>'
                         '</w:pPr>%s</w:p></w:tc>' % (w, _run(str(c), bold=(i == 0))))
        out.append("<w:tr>%s</w:tr>" % "".join(cells))
    out.append("</w:tbl>")
    return "".join(out)


def docx(path, blocks, author, created, modified, revision, total_time, company="Brackenford Airport Ltd",
         lang="en-GB", header_text=None):
    """blocks: [(style, text)] with style in (None, Heading1, Heading2, ListBullet) or ('TABLE', (rows, widths))."""
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    body = []
    text = []
    has_table = False
    for style, content in blocks:
        if style == "TABLE":
            rows, widths = content
            body.append(_table(rows, widths))
            body.append("<w:p/>")
            has_table = True
            text.extend(" ".join(str(c) for c in r) for r in rows)
        else:
            body.append(_para(style, content))
            text.append(content.replace("**", ""))
    sect = ('<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1304" w:right="1247" w:bottom="1247" '
            'w:left="1247" w:header="709" w:footer="709" w:gutter="0"/><w:cols w:space="708"/>'
            '<w:docGrid w:linePitch="360"/></w:sectPr>')
    document = _HEAD + '<w:document %s><w:body>%s%s</w:body></w:document>' % (_W, "".join(body), sect)
    table_style = ('<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:basedOn w:val="TableNormal"/>'
                   '<w:uiPriority w:val="39"/><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>'
                   '<w:tblPr><w:tblBorders><w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:left w:val="single" '
                   'w:sz="4" w:space="0" w:color="auto"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
                   '<w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:insideH w:val="single" w:sz="4" '
                   'w:space="0" w:color="auto"/><w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
                   '</w:tblBorders></w:tblPr></w:style>') if has_table else ""
    styles = _HEAD + (
        '<w:styles %s><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:asciiTheme="minorHAnsi" '
        'w:eastAsiaTheme="minorHAnsi" w:hAnsiTheme="minorHAnsi" w:cstheme="minorBidi"/><w:sz w:val="21"/>'
        '<w:szCs w:val="21"/><w:lang w:val="%s" w:eastAsia="en-US" w:bidi="ar-SA"/></w:rPr></w:rPrDefault>'
        '<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="259" w:lineRule="auto"/></w:pPr></w:pPrDefault>'
        '</w:docDefaults>'
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>'
        '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>'
        '<w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="240" '
        'w:after="120"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:rFonts w:asciiTheme="majorHAnsi" '
        'w:eastAsiaTheme="majorEastAsia" w:hAnsiTheme="majorHAnsi" w:cstheme="majorBidi"/><w:b/><w:color w:val="1F3864"/>'
        '<w:sz w:val="30"/><w:szCs w:val="30"/></w:rPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>'
        '<w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:unhideWhenUsed/><w:qFormat/><w:pPr><w:keepNext/>'
        '<w:spacing w:before="200" w:after="80"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:rFonts '
        'w:asciiTheme="majorHAnsi" w:eastAsiaTheme="majorEastAsia" w:hAnsiTheme="majorHAnsi" w:cstheme="majorBidi"/>'
        '<w:b/><w:color w:val="1F3864"/><w:sz w:val="23"/><w:szCs w:val="23"/></w:rPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="ListBullet"><w:name w:val="List Bullet"/><w:basedOn w:val="Normal"/>'
        '<w:uiPriority w:val="99"/><w:unhideWhenUsed/><w:pPr><w:numPr><w:numId w:val="1"/></w:numPr>'
        '<w:spacing w:after="60"/><w:contextualSpacing/></w:pPr></w:style>'
        '<w:style w:type="character" w:default="1" w:styleId="DefaultParagraphFont"><w:name w:val="Default Paragraph '
        'Font"/><w:uiPriority w:val="1"/><w:semiHidden/><w:unhideWhenUsed/></w:style>'
        '<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/>'
        '<w:uiPriority w:val="99"/><w:semiHidden/><w:unhideWhenUsed/><w:tblPr><w:tblInd w:w="0" w:type="dxa"/>'
        '<w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/>'
        '<w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>' + table_style +
        '<w:style w:type="numbering" w:default="1" w:styleId="NoList"><w:name w:val="No List"/>'
        '<w:uiPriority w:val="99"/><w:semiHidden/><w:unhideWhenUsed/></w:style></w:styles>') % (_W, lang)
    numbering = _HEAD + (
        '<w:numbering %s><w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="singleLevel"/>'
        '<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:pStyle w:val="ListBullet"/>'
        '<w:lvlText w:val="&#61623;"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="360" w:hanging="360"/></w:pPr>'
        '<w:rPr><w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default"/></w:rPr></w:lvl></w:abstractNum>'
        '<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>') % _W
    settings = _HEAD + (
        '<w:settings %s><w:zoom w:percent="100"/><w:proofState w:spelling="clean" w:grammar="clean"/>'
        '<w:defaultTabStop w:val="720"/><w:characterSpacingControl w:val="doNotCompress"/><w:compat>'
        '<w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/>'
        '</w:compat><w:themeFontLang w:val="%s"/><w:clrSchemeMapping w:bg1="light1" w:t1="dark1" '
        'w:bg2="light2" w:t2="dark2" w:accent1="accent1" w:accent2="accent2" w:accent3="accent3" w:accent4="accent4" '
        'w:accent5="accent5" w:accent6="accent6" w:hyperlink="hyperlink" w:followedHyperlink="followedHyperlink"/>'
        '<w:decimalSymbol w:val="."/><w:listSeparator w:val=","/></w:settings>') % (_W, lang)
    web = _HEAD + '<w:webSettings %s><w:optimizeForBrowser/><w:allowPNG/></w:webSettings>' % _W
    fonts = _HEAD + (
        '<w:fonts %s><w:font w:name="Calibri"><w:panose1 w:val="020F0502020204030204"/><w:charset w:val="00"/>'
        '<w:family w:val="swiss"/><w:pitch w:val="variable"/></w:font><w:font w:name="Times New Roman">'
        '<w:panose1 w:val="02020603050405020304"/><w:charset w:val="00"/><w:family w:val="roman"/>'
        '<w:pitch w:val="variable"/></w:font><w:font w:name="Symbol"><w:panose1 w:val="05050102010706020507"/>'
        '<w:charset w:val="02"/><w:family w:val="roman"/><w:pitch w:val="variable"/></w:font><w:font w:name="Calibri Light">'
        '<w:panose1 w:val="020F0302020204030204"/><w:charset w:val="00"/><w:family w:val="swiss"/>'
        '<w:pitch w:val="variable"/></w:font></w:fonts>') % _W
    words = sum(len(t.split()) for t in text)
    chars = sum(len(t.replace(" ", "")) for t in text)
    spaced = sum(len(t) for t in text) + len(text) - 1
    lines = sum(max(1, -(-len(t) // 95)) for t in text)
    pages = max(1, -(-words // 520))
    core_xml = _HEAD + (
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        '<dc:title></dc:title><dc:subject></dc:subject><dc:creator>%s</dc:creator><cp:keywords></cp:keywords>'
        '<dc:description></dc:description><cp:lastModifiedBy>%s</cp:lastModifiedBy><cp:revision>%d</cp:revision>'
        '<dcterms:created xsi:type="dcterms:W3CDTF">%s</dcterms:created>'
        '<dcterms:modified xsi:type="dcterms:W3CDTF">%s</dcterms:modified></cp:coreProperties>') % (
        _x(author), _x(author), revision, created, modified)
    app_xml = _HEAD + (
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Template>Normal.dotm'
        '</Template><TotalTime>%d</TotalTime><Pages>%d</Pages><Words>%d</Words><Characters>%d</Characters>'
        '<Application>Microsoft Office Word</Application><DocSecurity>0</DocSecurity><Lines>%d</Lines>'
        '<Paragraphs>%d</Paragraphs><ScaleCrop>false</ScaleCrop><Company>%s</Company><LinksUpToDate>false'
        '</LinksUpToDate><CharactersWithSpaces>%d</CharactersWithSpaces><SharedDoc>false</SharedDoc>'
        '<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0000</AppVersion></Properties>') % (
        total_time, pages, words, chars, lines, len(text), _x(company), spaced)
    rels = _HEAD + (
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/'
        'extended-properties" Target="docProps/app.xml"/><Relationship Id="rId2" Type="http://schemas.'
        'openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/'
        'officeDocument" Target="word/document.xml"/></Relationships>')
    base = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/"
    doc_rels = _HEAD + '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(
        '<Relationship Id="rId%d" Type="%s%s" Target="%s"/>' % (k, base, t, f) for k, (t, f) in enumerate(
            [("numbering", "numbering.xml"), ("styles", "styles.xml"), ("settings", "settings.xml"),
             ("webSettings", "webSettings.xml"), ("fontTable", "fontTable.xml"), ("theme", "theme/theme1.xml")],
            1)) + "</Relationships>"
    types = _HEAD + (
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" '
        'ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" '
        'ContentType="application/xml"/>' + "".join(
            '<Override PartName="/word/%s.xml" ContentType="%s%s+xml"/>' % (p, _CT, c) for p, c in (
                ("document", "document.main"), ("numbering", "numbering"), ("styles", "styles"),
                ("settings", "settings"), ("webSettings", "webSettings"), ("fontTable", "fontTable"))) +
        '<Override PartName="/word/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.'
        'theme+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.'
        'core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-'
        'officedocument.extended-properties+xml"/></Types>')
    parts = [("[Content_Types].xml", types), ("_rels/.rels", rels), ("word/document.xml", document),
             ("word/_rels/document.xml.rels", doc_rels), ("word/theme/theme1.xml", _theme()),
             ("word/numbering.xml", numbering), ("word/settings.xml", settings), ("word/styles.xml", styles),
             ("word/webSettings.xml", web), ("word/fontTable.xml", fonts), ("docProps/core.xml", core_xml),
             ("docProps/app.xml", app_xml)]
    stamp = _stamp(modified)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in parts:
            zi = zipfile.ZipInfo(name, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.create_system = 0
            zf.writestr(zi, data.encode("utf-8"))


# ----------------------------------------------------------------------------------------------- PDF
def pdf(path, story_fn, title, author, created_pdf, producer="Microsoft\u00ae Word for Microsoft 365",
        creator="Microsoft\u00ae Word for Microsoft 365", footer=None):
    """created_pdf like 20260930141200: written into CreationDate and ModDate with the UK offset of that date."""
    import os
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate
    os.makedirs(os.path.dirname(path), exist_ok=True)
    buf = io.BytesIO()

    def _foot(canv, doc):
        if footer:
            canv.saveState()
            canv.setFont("Helvetica", 7)
            canv.drawString(18 * mm, 10 * mm, footer)
            canv.drawRightString(192 * mm, 10 * mm, "Page %d" % doc.page)
            canv.restoreState()
    doc = SimpleDocTemplate(buf, pagesize=A4, title=title, author=author, creator=creator, producer=producer,
                            leftMargin=52, rightMargin=52, topMargin=56, bottomMargin=56)
    doc.build(story_fn(), onFirstPage=_foot, onLaterPages=_foot)
    raw = buf.getvalue()
    month = int(created_pdf[4:6])
    off = "+01'00'" if 4 <= month <= 10 else "+00'00'"
    raw = re.sub(rb"D:\d{14}[+-]\d\d'\d\d'", lambda m: ("D:%s%s" % (created_pdf, off)).encode(), raw)
    raw = re.sub(rb"D:\d{14}Z00'00'", lambda m: ("D:%s%s" % (created_pdf, off)).encode()[:len(m.group(0))].ljust(
        len(m.group(0)), b" "), raw)
    raw = re.sub(rb"(?i)reportlab generated pdf document[^\r\n]*", lambda m: b" " * len(m.group(0)), raw)
    raw = re.sub(rb"(?i)reportlab[^\r\n)]*", lambda m: b" " * len(m.group(0)), raw)
    raw = re.sub(rb"\(anonymous\)", b"(         )", raw)
    assert not re.search(rb"(?i)reportlab", raw), "library string left in " + path
    with open(path, "wb") as fh:
        fh.write(raw)
