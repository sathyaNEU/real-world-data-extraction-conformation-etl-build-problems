"""Office packages written the way Word and Excel write them: a .docx from a list of blocks, and an .xlsx from an
openpyxl workbook. Shared strings, Excel's own style and part order, Word's paragraph ids and rsids, document
properties with UTC instants, zip entries stamped 1980-01-01 as Office stamps them."""
import collections
import datetime as dt
import os
import random
import re
import shutil
import subprocess
import tempfile
import zipfile
from xml.sax.saxutils import escape

import world as W

OFFICE_TIME = (1980, 1, 1, 0, 0, 0)


def esc(s):
    return escape(str(s), {'"': "&quot;"})


def write_zip(path, parts):
    """entries stamped 1980-01-01 with no file-system attributes, as Office writes a package"""
    with zipfile.ZipFile(path, "w") as z:
        for name, data in parts:
            zi = zipfile.ZipInfo(name, date_time=OFFICE_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.create_system = 0
            z.writestr(zi, data.encode("utf-8") if isinstance(data, str) else data)
            zi.external_attr = 0                 # kept for the central directory, written on close


# The Office 2013-2022 "Office Theme" (theme family 62F939B6, Calibri Light and Calibri) as Word and Excel 2016 and
# later write it into a document that was created before the 2023 Aptos theme: one line after the declaration. Word's
# copy differs from Excel's only in three script fonts (Thai, and the Japanese body font).
THEME_COLOURS = [("dk2", "44546A"), ("lt2", "E7E6E6"), ("accent1", "4472C4"), ("accent2", "ED7D31"), ("accent3", "A5A5A5"),
                 ("accent4", "FFC000"), ("accent5", "5B9BD5"), ("accent6", "70AD47"), ("hlink", "0563C1"),
                 ("folHlink", "954F72")]
THEME_SCRIPTS = [("Jpan", "游ゴシック Light", "游ゴシック"), ("Hang", "맑은 고딕", "맑은 고딕"), ("Hans", "等线 Light", "等线"),
                 ("Hant", "新細明體", "新細明體"), ("Arab", "Times New Roman", "Arial"), ("Hebr", "Times New Roman", "Arial"),
                 ("Thai", "Tahoma", "Tahoma"), ("Ethi", "Nyala", "Nyala"), ("Beng", "Vrinda", "Vrinda"),
                 ("Gujr", "Shruti", "Shruti"), ("Khmr", "MoolBoran", "DaunPenh"), ("Knda", "Tunga", "Tunga"),
                 ("Guru", "Raavi", "Raavi"), ("Cans", "Euphemia", "Euphemia"), ("Cher", "Plantagenet Cherokee", "Plantagenet Cherokee"),
                 ("Yiii", "Microsoft Yi Baiti", "Microsoft Yi Baiti"), ("Tibt", "Microsoft Himalaya", "Microsoft Himalaya"),
                 ("Thaa", "MV Boli", "MV Boli"), ("Deva", "Mangal", "Mangal"), ("Telu", "Gautami", "Gautami"),
                 ("Taml", "Latha", "Latha"), ("Syrc", "Estrangelo Edessa", "Estrangelo Edessa"), ("Orya", "Kalinga", "Kalinga"),
                 ("Mlym", "Kartika", "Kartika"), ("Laoo", "DokChampa", "DokChampa"), ("Sinh", "Iskoola Pota", "Iskoola Pota"),
                 ("Mong", "Mongolian Baiti", "Mongolian Baiti"), ("Viet", "Times New Roman", "Arial"),
                 ("Uigh", "Microsoft Uighur", "Microsoft Uighur"), ("Geor", "Sylfaen", "Sylfaen"), ("Armn", "Arial", "Arial"),
                 ("Bugi", "Leelawadee UI", "Leelawadee UI"), ("Bopo", "Microsoft JhengHei", "Microsoft JhengHei"),
                 ("Java", "Javanese Text", "Javanese Text"), ("Lisu", "Segoe UI", "Segoe UI"), ("Mymr", "Myanmar Text", "Myanmar Text"),
                 ("Nkoo", "Ebrima", "Ebrima"), ("Olck", "Nirmala UI", "Nirmala UI"), ("Osma", "Ebrima", "Ebrima"),
                 ("Phag", "Phagspa", "Phagspa"), ("Syrn", "Estrangelo Edessa", "Estrangelo Edessa"),
                 ("Syrj", "Estrangelo Edessa", "Estrangelo Edessa"), ("Syre", "Estrangelo Edessa", "Estrangelo Edessa"),
                 ("Sora", "Nirmala UI", "Nirmala UI"), ("Tale", "Microsoft Tai Le", "Microsoft Tai Le"),
                 ("Talu", "Microsoft New Tai Lue", "Microsoft New Tai Lue"), ("Tfng", "Ebrima", "Ebrima")]
THEME_WORD_SCRIPTS = {("Thai", 0): "Angsana New", ("Thai", 1): "Cordia New", ("Jpan", 1): "游明朝"}
THEME_FMT = (
    '<a:fmtScheme name="Office"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:gradFill rotWithShape="1">'
    '<a:gsLst><a:gs pos="0"><a:schemeClr val="phClr"><a:lumMod val="110000"/><a:satMod val="105000"/><a:tint val="67000"/>'
    '</a:schemeClr></a:gs><a:gs pos="50000"><a:schemeClr val="phClr"><a:lumMod val="105000"/><a:satMod val="103000"/>'
    '<a:tint val="73000"/></a:schemeClr></a:gs><a:gs pos="100000"><a:schemeClr val="phClr"><a:lumMod val="105000"/>'
    '<a:satMod val="109000"/><a:tint val="81000"/></a:schemeClr></a:gs></a:gsLst><a:lin ang="5400000" scaled="0"/></a:gradFill>'
    '<a:gradFill rotWithShape="1"><a:gsLst><a:gs pos="0"><a:schemeClr val="phClr"><a:satMod val="103000"/><a:lumMod val="102000"/>'
    '<a:tint val="94000"/></a:schemeClr></a:gs><a:gs pos="50000"><a:schemeClr val="phClr"><a:satMod val="110000"/>'
    '<a:lumMod val="100000"/><a:shade val="100000"/></a:schemeClr></a:gs><a:gs pos="100000"><a:schemeClr val="phClr">'
    '<a:lumMod val="99000"/><a:satMod val="120000"/><a:shade val="78000"/></a:schemeClr></a:gs></a:gsLst>'
    '<a:lin ang="5400000" scaled="0"/></a:gradFill></a:fillStyleLst><a:lnStyleLst>%s</a:lnStyleLst><a:effectStyleLst>'
    '<a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst>'
    '<a:outerShdw blurRad="57150" dist="19050" dir="5400000" algn="ctr" rotWithShape="0"><a:srgbClr val="000000">'
    '<a:alpha val="63000"/></a:srgbClr></a:outerShdw></a:effectLst></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst>'
    '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"><a:tint val="95000"/>'
    '<a:satMod val="170000"/></a:schemeClr></a:solidFill><a:gradFill rotWithShape="1"><a:gsLst><a:gs pos="0">'
    '<a:schemeClr val="phClr"><a:tint val="93000"/><a:satMod val="150000"/><a:shade val="98000"/><a:lumMod val="102000"/>'
    '</a:schemeClr></a:gs><a:gs pos="50000"><a:schemeClr val="phClr"><a:tint val="98000"/><a:satMod val="130000"/>'
    '<a:shade val="90000"/><a:lumMod val="103000"/></a:schemeClr></a:gs><a:gs pos="100000"><a:schemeClr val="phClr">'
    '<a:shade val="63000"/><a:satMod val="120000"/></a:schemeClr></a:gs></a:gsLst><a:lin ang="5400000" scaled="0"/>'
    '</a:gradFill></a:bgFillStyleLst></a:fmtScheme>'
    % "".join('<a:ln w="%d" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
              '<a:prstDash val="solid"/><a:miter lim="800000"/></a:ln>' % w for w in (6350, 12700, 19050)))


def theme_xml(app="excel"):
    """the Office 2013-2022 theme part, as the application writes it"""
    def font(k, latin, panose):
        f = "".join('<a:font script="%s" typeface="%s"/>'
                    % (s, THEME_WORD_SCRIPTS.get((s, k), fonts[k]) if app == "word" else fonts[k])
                    for s, *fonts in THEME_SCRIPTS)
        tag = ("a:majorFont", "a:minorFont")[k]
        return '<%s><a:latin typeface="%s" panose="%s"/><a:ea typeface=""/><a:cs typeface=""/>%s</%s>' % (tag, latin, panose, f, tag)
    clr = "".join('<a:%s><a:srgbClr val="%s"/></a:%s>' % (k, v, k) for k, v in THEME_COLOURS)
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
            '<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Office Theme"><a:themeElements>'
            '<a:clrScheme name="Office"><a:dk1><a:sysClr val="windowText" lastClr="000000"/></a:dk1><a:lt1>'
            '<a:sysClr val="window" lastClr="FFFFFF"/></a:lt1>%s</a:clrScheme><a:fontScheme name="Office">%s%s</a:fontScheme>%s'
            '</a:themeElements><a:objectDefaults/><a:extraClrSchemeLst/><a:extLst><a:ext uri="{05A4C25C-085E-4340-85A3-A5531E510DB2}">'
            '<thm15:themeFamily xmlns:thm15="http://schemas.microsoft.com/office/thememl/2012/main" name="Office Theme" '
            'id="{62F939B6-93AF-4DB8-9C6B-D6C7DFDC589F}" vid="{4A3C46E8-61CC-4603-A589-7422A47A8E4A}"/></a:ext></a:extLst>'
            '</a:theme>' % (clr, font(0, "Calibri Light", "020F0302020204030204"), font(1, "Calibri", "020F0502020204030204"),
                            THEME_FMT))


def core_xml(creator, modified_by, created, modified, title=None, revision=None):
    t = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
         '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
         'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
         'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">')
    if title is not None:
        t += "<dc:title>%s</dc:title><dc:subject></dc:subject>" % esc(title)
    t += "<dc:creator>%s</dc:creator>" % esc(creator)
    if title is not None:
        t += "<cp:keywords></cp:keywords><dc:description></dc:description>"
    t += "<cp:lastModifiedBy>%s</cp:lastModifiedBy>" % esc(modified_by)
    if revision is not None:
        t += "<cp:revision>%d</cp:revision>" % revision
    t += ('<dcterms:created xsi:type="dcterms:W3CDTF">%s</dcterms:created>'
          '<dcterms:modified xsi:type="dcterms:W3CDTF">%s</dcterms:modified></cp:coreProperties>'
          % (W.utc_stamp(created), W.utc_stamp(modified)))
    return t


# ------------------------------------------------------------------------------------------------------- Word

WNS = ('xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
       'xmlns:cx="http://schemas.microsoft.com/office/drawing/2014/chartex" '
       'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
       'xmlns:aink="http://schemas.microsoft.com/office/drawing/2016/ink" '
       'xmlns:am3d="http://schemas.microsoft.com/office/drawing/2017/model3d" '
       'xmlns:o="urn:schemas-microsoft-com:office:office" '
       'xmlns:oel="http://schemas.microsoft.com/office/2019/extlst" '
       'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
       'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
       'xmlns:v="urn:schemas-microsoft-com:vml" '
       'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
       'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
       'xmlns:w10="urn:schemas-microsoft-com:office:word" '
       'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
       'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
       'xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" '
       'xmlns:w16cex="http://schemas.microsoft.com/office/word/2018/wordml/cex" '
       'xmlns:w16cid="http://schemas.microsoft.com/office/word/2016/wordml/cid" '
       'xmlns:w16="http://schemas.microsoft.com/office/word/2018/wordml" '
       'xmlns:w16sdtdh="http://schemas.microsoft.com/office/word/2020/wordml/sdtdatahash" '
       'xmlns:w16se="http://schemas.microsoft.com/office/word/2015/wordml/symex" '
       'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
       'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" '
       'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
       'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
       'mc:Ignorable="w14 w15 w16se w16cid w16 w16cex w16sdtdh wp14"')
WIGN = ('xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
        'xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" '
        'xmlns:w16cex="http://schemas.microsoft.com/office/word/2018/wordml/cex" '
        'xmlns:w16cid="http://schemas.microsoft.com/office/word/2016/wordml/cid" '
        'xmlns:w16="http://schemas.microsoft.com/office/word/2018/wordml" '
        'xmlns:w16sdtdh="http://schemas.microsoft.com/office/word/2020/wordml/sdtdatahash" '
        'xmlns:w16se="http://schemas.microsoft.com/office/word/2015/wordml/symex" '
        'mc:Ignorable="w14 w15 w16se w16cid w16 w16cex w16sdtdh"')

def latent_styles():
    """Word's built-in latent style table as Word 2016 and later write it: 376 names, each with the attributes that
    differ from the table's defaults"""
    sh = dict(semiHidden=1, unhideWhenUsed=1)
    out = [("Normal", dict(uiPriority=0, qFormat=1)), ("heading 1", dict(uiPriority=9, qFormat=1))]
    out += [("heading %d" % i, dict(semiHidden=1, uiPriority=9, unhideWhenUsed=1, qFormat=1)) for i in range(2, 10)]
    out += [("index %d" % i, sh) for i in range(1, 10)]
    out += [("toc %d" % i, dict(semiHidden=1, uiPriority=39, unhideWhenUsed=1)) for i in range(1, 10)]
    out += [(n, sh) for n in ["Normal Indent", "footnote text", "annotation text", "header", "footer", "index heading"]]
    out += [("caption", dict(semiHidden=1, uiPriority=35, unhideWhenUsed=1, qFormat=1))]
    out += [(n, sh) for n in ["table of figures", "envelope address", "envelope return", "footnote reference",
                               "annotation reference", "line number", "page number", "endnote reference", "endnote text",
                               "table of authorities", "macro", "toa heading", "List", "List Bullet", "List Number"]
            + ["List %d" % i for i in range(2, 6)] + ["List Bullet %d" % i for i in range(2, 6)]
            + ["List Number %d" % i for i in range(2, 6)]]
    out += [("Title", dict(uiPriority=10, qFormat=1)), ("Closing", sh), ("Signature", sh),
            ("Default Paragraph Font", dict(semiHidden=1, uiPriority=1, unhideWhenUsed=1)), ("Body Text", sh),
            ("Body Text Indent", sh), ("List Continue", sh)]
    out += [("List Continue %d" % i, sh) for i in range(2, 6)]
    out += [("Message Header", sh), ("Subtitle", dict(uiPriority=11, qFormat=1))]
    out += [(n, sh) for n in ["Salutation", "Date", "Body Text First Indent", "Body Text First Indent 2", "Note Heading",
                               "Body Text 2", "Body Text 3", "Body Text Indent 2", "Body Text Indent 3", "Block Text",
                               "Hyperlink", "FollowedHyperlink"]]
    out += [("Strong", dict(uiPriority=22, qFormat=1)), ("Emphasis", dict(uiPriority=20, qFormat=1))]
    out += [(n, sh) for n in ["Document Map", "Plain Text", "E-mail Signature", "HTML Top of Form", "HTML Bottom of Form",
                               "Normal (Web)", "HTML Acronym", "HTML Address", "HTML Cite", "HTML Code", "HTML Definition",
                               "HTML Keyboard", "HTML Preformatted", "HTML Sample", "HTML Typewriter", "HTML Variable",
                               "Normal Table", "annotation subject", "No List", "Outline List 1", "Outline List 2",
                               "Outline List 3"]
            + ["Table Simple %d" % i for i in range(1, 4)] + ["Table Classic %d" % i for i in range(1, 5)]
            + ["Table Colorful %d" % i for i in range(1, 4)] + ["Table Columns %d" % i for i in range(1, 6)]
            + ["Table Grid %d" % i for i in range(1, 9)] + ["Table List %d" % i for i in range(1, 9)]
            + ["Table 3D effects %d" % i for i in range(1, 4)]
            + ["Table Contemporary", "Table Elegant", "Table Professional", "Table Subtle 1", "Table Subtle 2",
               "Table Web 1", "Table Web 2", "Table Web 3", "Balloon Text"]]
    out += [("Table Grid", dict(uiPriority=39)), ("Table Theme", sh), ("Placeholder Text", dict(semiHidden=1)),
            ("No Spacing", dict(uiPriority=1, qFormat=1))]
    fam = ["Light Shading", "Light List", "Light Grid", "Medium Shading 1", "Medium Shading 2", "Medium List 1",
           "Medium List 2", "Medium Grid 1", "Medium Grid 2", "Medium Grid 3", "Dark List", "Colorful Shading",
           "Colorful List", "Colorful Grid"]
    out += [(n, dict(uiPriority=60 + k)) for k, n in enumerate(fam)]
    for acc in range(1, 7):
        for k, n in enumerate(fam):
            out.append(("%s Accent %d" % (n, acc), dict(uiPriority=60 + k)))
            if acc == 1 and n == "Medium List 1":
                out += [("Revision", dict(semiHidden=1)), ("List Paragraph", dict(uiPriority=34, qFormat=1)),
                        ("Quote", dict(uiPriority=29, qFormat=1)), ("Intense Quote", dict(uiPriority=30, qFormat=1))]
    out += [("Subtle Emphasis", dict(uiPriority=19, qFormat=1)), ("Intense Emphasis", dict(uiPriority=21, qFormat=1)),
            ("Subtle Reference", dict(uiPriority=31, qFormat=1)), ("Intense Reference", dict(uiPriority=32, qFormat=1)),
            ("Book Title", dict(uiPriority=33, qFormat=1)),
            ("Bibliography", dict(semiHidden=1, uiPriority=37, unhideWhenUsed=1)),
            ("TOC Heading", dict(semiHidden=1, uiPriority=39, unhideWhenUsed=1, qFormat=1))]
    out += [("Plain Table %d" % i, dict(uiPriority=40 + i)) for i in range(1, 6)]
    out += [("Grid Table Light", dict(uiPriority=40))]
    seven = ["1 Light", "2", "3", "4", "5 Dark", "6 Colorful", "7 Colorful"]
    for kind in ("Grid Table", "List Table"):
        for acc in [""] + [" Accent %d" % i for i in range(1, 7)]:
            out += [("%s %s%s" % (kind, t, acc), dict(uiPriority=46 + k)) for k, t in enumerate(seven)]
    out += [(n, sh) for n in ["Mention", "Smart Hyperlink", "Hashtag", "Unresolved Mention", "Smart Link"]]
    return out


def styles_xml(font, size_half_points, heading_colour):
    lsd = []
    for name, at in latent_styles():
        lsd.append('<w:lsdException w:name="%s"%s/>' % (name, "".join(' w:%s="%d"' % (k, at[k]) for k in
                   ("semiHidden", "uiPriority", "unhideWhenUsed", "qFormat") if k in at)))
    sz = size_half_points
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<w:styles %s>'
            '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:asciiTheme="minorHAnsi" w:eastAsiaTheme="minorHAnsi" '
            'w:hAnsiTheme="minorHAnsi" w:cstheme="minorBidi"/><w:kern w:val="2"/><w:sz w:val="22"/><w:szCs w:val="22"/>'
            '<w:lang w:val="en-GB" w:eastAsia="en-US" w:bidi="ar-SA"/><w14:ligatures w14:val="standardContextual"/></w:rPr>'
            '</w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="160" w:line="259" w:lineRule="auto"/></w:pPr>'
            '</w:pPrDefault></w:docDefaults>'
            '<w:latentStyles w:defLockedState="0" w:defUIPriority="99" w:defSemiHidden="0" w:defUnhideWhenUsed="0" '
            'w:defQFormat="0" w:count="%d">%s</w:latentStyles>'
            '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/>'
            '<w:pPr><w:spacing w:after="120" w:line="264" w:lineRule="auto"/></w:pPr><w:rPr><w:rFonts w:ascii="{f}" '
            'w:hAnsi="{f}" w:cs="{f}"/><w:sz w:val="{s}"/><w:szCs w:val="{s}"/></w:rPr></w:style>'
            '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>'
            '<w:next w:val="Normal"/><w:link w:val="Heading1Char"/><w:uiPriority w:val="9"/><w:qFormat/><w:pPr><w:keepNext/>'
            '<w:keepLines/><w:spacing w:before="240" w:after="80"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:bCs/>'
            '<w:color w:val="{c}"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>'
            '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>'
            '<w:next w:val="Normal"/><w:link w:val="Heading2Char"/><w:uiPriority w:val="9"/><w:unhideWhenUsed/><w:qFormat/>'
            '<w:pPr><w:keepNext/><w:keepLines/><w:spacing w:before="160" w:after="60"/><w:outlineLvl w:val="1"/></w:pPr>'
            '<w:rPr><w:b/><w:bCs/><w:color w:val="{c}"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>'
            '<w:style w:type="character" w:default="1" w:styleId="DefaultParagraphFont"><w:name w:val="Default Paragraph Font"/>'
            '<w:uiPriority w:val="1"/><w:semiHidden/><w:unhideWhenUsed/></w:style>'
            '<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/><w:uiPriority w:val="99"/>'
            '<w:semiHidden/><w:unhideWhenUsed/><w:tblPr><w:tblInd w:w="0" w:type="dxa"/><w:tblCellMar><w:top w:w="0" w:type="dxa"/>'
            '<w:left w:w="108" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar>'
            '</w:tblPr></w:style>'
            '<w:style w:type="numbering" w:default="1" w:styleId="NoList"><w:name w:val="No List"/><w:uiPriority w:val="99"/>'
            '<w:semiHidden/><w:unhideWhenUsed/></w:style>'
            '<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/>'
            '<w:link w:val="TitleChar"/><w:uiPriority w:val="10"/><w:qFormat/><w:pPr><w:spacing w:after="80" w:line="240" '
            'w:lineRule="auto"/><w:contextualSpacing/></w:pPr><w:rPr><w:b/><w:bCs/><w:color w:val="{c}"/><w:kern w:val="28"/>'
            '<w:sz w:val="30"/><w:szCs w:val="30"/></w:rPr></w:style>'
            '<w:style w:type="character" w:customStyle="1" w:styleId="TitleChar"><w:name w:val="Title Char"/>'
            '<w:basedOn w:val="DefaultParagraphFont"/><w:link w:val="Title"/><w:uiPriority w:val="10"/><w:rPr><w:rFonts w:ascii="{f}" '
            'w:hAnsi="{f}"/><w:b/><w:bCs/><w:color w:val="{c}"/><w:kern w:val="28"/><w:sz w:val="30"/><w:szCs w:val="30"/></w:rPr></w:style>'
            '<w:style w:type="character" w:customStyle="1" w:styleId="Heading1Char"><w:name w:val="Heading 1 Char"/>'
            '<w:basedOn w:val="DefaultParagraphFont"/><w:link w:val="Heading1"/><w:uiPriority w:val="9"/><w:rPr><w:rFonts w:ascii="{f}" '
            'w:hAnsi="{f}"/><w:b/><w:bCs/><w:color w:val="{c}"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>'
            '<w:style w:type="character" w:customStyle="1" w:styleId="Heading2Char"><w:name w:val="Heading 2 Char"/>'
            '<w:basedOn w:val="DefaultParagraphFont"/><w:link w:val="Heading2"/><w:uiPriority w:val="9"/><w:rPr><w:rFonts w:ascii="{f}" '
            'w:hAnsi="{f}"/><w:b/><w:bCs/><w:color w:val="{c}"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:style>'
            '<w:style w:type="paragraph" w:styleId="Header"><w:name w:val="header"/><w:basedOn w:val="Normal"/>'
            '<w:link w:val="HeaderChar"/><w:uiPriority w:val="99"/><w:unhideWhenUsed/><w:pPr><w:tabs><w:tab w:val="center" w:pos="4513"/>'
            '<w:tab w:val="right" w:pos="9026"/></w:tabs><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>'
            '<w:rPr><w:color w:val="595959"/><w:sz w:val="16"/><w:szCs w:val="16"/></w:rPr></w:style>'
            '<w:style w:type="character" w:customStyle="1" w:styleId="HeaderChar"><w:name w:val="Header Char"/>'
            '<w:basedOn w:val="DefaultParagraphFont"/><w:link w:val="Header"/><w:uiPriority w:val="99"/><w:rPr><w:rFonts w:ascii="{f}" '
            'w:hAnsi="{f}"/><w:color w:val="595959"/><w:sz w:val="16"/><w:szCs w:val="16"/></w:rPr></w:style>'
            '<w:style w:type="paragraph" w:styleId="Footer"><w:name w:val="footer"/><w:basedOn w:val="Normal"/>'
            '<w:link w:val="FooterChar"/><w:uiPriority w:val="99"/><w:unhideWhenUsed/><w:pPr><w:tabs><w:tab w:val="center" w:pos="4513"/>'
            '<w:tab w:val="right" w:pos="9026"/></w:tabs><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>'
            '<w:rPr><w:color w:val="595959"/><w:sz w:val="16"/><w:szCs w:val="16"/></w:rPr></w:style>'
            '<w:style w:type="character" w:customStyle="1" w:styleId="FooterChar"><w:name w:val="Footer Char"/>'
            '<w:basedOn w:val="DefaultParagraphFont"/><w:link w:val="Footer"/><w:uiPriority w:val="99"/><w:rPr><w:rFonts w:ascii="{f}" '
            'w:hAnsi="{f}"/><w:color w:val="595959"/><w:sz w:val="16"/><w:szCs w:val="16"/></w:rPr></w:style>'
            '<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:basedOn w:val="TableNormal"/>'
            '<w:uiPriority w:val="39"/><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:tblPr><w:tblBorders>'
            '<w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
            '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
            '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
            '</w:tblBorders></w:tblPr></w:style>'
            '</w:styles>' % (WIGN, len(lsd), "".join(lsd))).replace("{f}", font).replace("{s}", str(sz)).replace("{c}", heading_colour)


FONTS = {
    "Calibri": ('020F0502020204030204', 'swiss', 'E4002EFF', 'C200247B', '00000009', '00000000', '000001FF', '00000000'),
    "Times New Roman": ('02020603050405020304', 'roman', 'E0002EFF', 'C000785B', '00000009', '00000000', '000001FF', '00000000'),
    "Calibri Light": ('020F0302020204030204', 'swiss', 'E4002EFF', 'C200247B', '00000009', '00000000', '000001FF', '00000000'),
    "Arial": ('020B0604020202020204', 'swiss', 'E0002EFF', 'C000785B', '00000009', '00000000', '000001FF', '00000000'),
}


def font_table(names):
    out = []
    for n in names:
        p, fam, u0, u1, u2, u3, c0, c1 = FONTS[n]
        out.append('<w:font w:name="%s"><w:panose1 w:val="%s"/><w:charset w:val="00"/><w:family w:val="%s"/>'
                   '<w:pitch w:val="variable"/><w:sig w:usb0="%s" w:usb1="%s" w:usb2="%s" w:usb3="%s" w:csb0="%s" '
                   'w:csb1="%s"/></w:font>' % (n, p, fam, u0, u1, u2, u3, c0, c1))
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<w:fonts %s>%s</w:fonts>' % (WIGN, "".join(out))


class Rsid:
    """editing sessions: each paragraph carries the session that created it, as Word records. `sessions` is either a
    count (paragraphs spread over the sessions at random) or the document's history as (revision, sittings) pairs in
    the order it was edited, the first sitting of the first revision being the one that created the document; a
    paragraph tagged with a revision takes one of that revision's sittings, mostly the one before it."""

    def __init__(self, seed, sessions):
        self.r = random.Random(seed)
        self.by = None
        if isinstance(sessions, int):
            self.ids = sorted({"00%06X" % self.r.randrange(0x100000, 0xFFFFFF) for _ in range(sessions)})
            self.root = self.ids[0]
            return
        seen, self.by, self.cur = set(), {}, {}
        for v, n in sessions:
            got = []
            while len(got) < n:
                x = "00%06X" % self.r.randrange(0x100000, 0xFFFFFF)
                if x not in seen:
                    seen.add(x)
                    got.append(x)
            self.by[v] = got
        self.first, self.last = sessions[0][0], sessions[-1][0]
        self.root = self.by[self.first][0]
        self.ids = sorted(seen)

    def pick(self, v=None):
        if self.by is None or v is None:
            return self.r.choice(self.ids)
        got = self.by[v]
        k = self.cur.get(v, 0)
        if len(got) > 1 and self.r.random() < 0.3:
            k = self.r.randrange(len(got))
        self.cur[v] = k
        return got[k]

    def para_id(self):
        return "%08X" % self.r.randrange(0x01000000, 0x7FFFFFFF)


def run_xml(text, bold=False, italic=False, size=None, colour=None, rsid=None):
    rpr = ""
    if bold:
        rpr += "<w:b/><w:bCs/>"
    if italic:
        rpr += "<w:i/><w:iCs/>"
    if colour:
        rpr += '<w:color w:val="%s"/>' % colour
    if size:
        rpr += '<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (size, size)
    rpr = "<w:rPr>%s</w:rPr>" % rpr if rpr else ""
    sp = ' xml:space="preserve"' if text != text.strip() or "  " in text else ""
    return "<w:r%s>%s<w:t%s>%s</w:t></w:r>" % (' w:rsidR="%s"' % rsid if rsid else "", rpr, sp, esc(text))


def para_xml(rs, runs, style=None, ppr_extra="", v=None, vp=None):
    """v: the revision that created the paragraph; vp: a later revision that changed its formatting"""
    ppr = ""
    if style:
        ppr += '<w:pStyle w:val="%s"/>' % style
    ppr += ppr_extra
    ppr = "<w:pPr>%s</w:pPr>" % ppr if ppr else ""
    r1 = rs.pick(v)
    pid = rs.para_id()
    rp = rs.pick() if v is None else (rs.pick(vp) if vp else r1)
    return ('<w:p w14:paraId="%s" w14:textId="77777777" w:rsidR="%s" w:rsidRDefault="%s" w:rsidP="%s">%s%s</w:p>'
            % (pid, r1, r1, rp, ppr, "".join(runs)))


def field_runs(instr, shown):
    return ('<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> %s </w:instrText></w:r>'
            '<w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:rPr><w:noProof/></w:rPr><w:t>%s</w:t></w:r>'
            '<w:r><w:fldChar w:fldCharType="end"/></w:r>' % (instr, shown))


def table_xml(rs, rows, widths, header_fill="E7ECEF", size=None, hist=None):
    """hist: {"v": revision of the table, "rows": [revision of each row], "cells": {(row, column): revision that last
    retyped the cell}}"""
    hist = hist or {}
    grid = "".join('<w:gridCol w:w="%d"/>' % w for w in widths)
    out = ['<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="0" w:type="auto"/><w:tblLook w:val="04A0" '
           'w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr>'
           '<w:tblGrid>%s</w:tblGrid>' % grid]
    for k, row in enumerate(rows):
        cells = []
        keep = "<w:keepNext/>" if k < len(rows) - 1 else ""
        rv = hist["rows"][k] if "rows" in hist else hist.get("v")
        for j, (w, v) in enumerate(zip(widths, row)):
            shd = '<w:shd w:val="clear" w:color="auto" w:fill="%s"/>' % header_fill if k == 0 else ""
            cv = hist.get("cells", {}).get((k, j))
            run = run_xml(v, bold=(k == 0), size=size, rsid=rs.pick(cv) if cv else None)
            cells.append('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s</w:tcPr>%s</w:tc>'
                         % (w, shd, para_xml(rs, [run], ppr_extra=keep + '<w:spacing w:before="40" w:after="40"/>', v=rv)))
        rid = rs.pick(rv)
        out.append('<w:tr w:rsidR="%s" w:rsidTr="%s" w14:paraId="%s" w14:textId="77777777"><w:trPr><w:cantSplit/></w:trPr>%s</w:tr>'
                   % (rid, rid, rs.para_id(), "".join(cells)))
    out.append("</w:tbl>")
    return "".join(out)


def split_edits(text, edits):
    """a paragraph's text cut into (piece, revision) where a later revision typed the piece; None for the rest"""
    marks = []
    for sub, v in edits:
        i = text.find(sub)
        assert i >= 0, "edit %r not in %r" % (sub[:40], text[:60])
        marks.append((i, i + len(sub), v))
    out, pos = [], 0
    for a, b, v in sorted(marks):
        assert a >= pos, "overlapping edits in %r" % text[:60]
        if a > pos:
            out.append((text[pos:a], None))
        out.append((text[a:b], v))
        pos = b
    if pos < len(text) or not out:
        out.append((text[pos:], None))
    return out


def docx(path, blocks, header, footer, props, font="Calibri", size=21, heading_colour="1F3A4D", seed=0, sessions=9,
         margins=(1247, 1247, 1247, 1247), history=None):
    """blocks: ("title", text) ("h1", text) ("h2", text) ("p", text) ("p", [(text, bold, italic)]) ("small", text)
    ("table", rows, widths); header and footer: (left text, right text) with {PAGE} and {NUMPAGES} fields allowed.
    history: one entry per block, {"v": revision that wrote it, "vp": revision that last changed its formatting,
    "edits": [(text typed in a later revision, that revision)]} or, for a table, {"v", "rows", "cells"}; sessions is
    then the list of (revision, sittings) in order"""
    rs = Rsid(seed, sessions)
    body, plist = [], []        # plist: each body paragraph's text in document order; a table row's text on its first cell
    for b, h in zip(blocks, history or [None] * len(blocks)):
        h = h or {}
        kind = b[0]
        if kind == "table":
            body.append(table_xml(rs, b[1], b[2], size=b[3] if len(b) > 3 else None, hist=h))
            body.append(para_xml(rs, [], ppr_extra='<w:spacing w:after="60"/>', v=h.get("v")))
            for row in b[1]:
                plist += [" ".join(v for v in row if v.strip())] + [""] * (len(row) - 1)
            plist.append("")
            continue
        if isinstance(b[1], str):
            runs_in = [(b[1], False, False)]
        else:
            runs_in = b[1]
        style = {"title": "Title", "h1": "Heading1", "h2": "Heading2"}.get(kind)
        size_ = 17 if kind == "small" else None
        colour = "595959" if kind == "small" else None
        runs = []
        for t, bo, it in runs_in:
            for piece, ev in split_edits(t, h.get("edits", [])):
                runs.append(run_xml(piece, bold=bo, italic=it, size=size_, colour=colour, rsid=rs.pick(ev) if ev else None))
        extra = '<w:spacing w:after="40"/>' if kind == "small" else ""
        body.append(para_xml(rs, runs, style=style, ppr_extra=extra, v=h.get("v"), vp=h.get("vp")))
        plist.append("".join(x[0] for x in runs_in))

    def hf(tag, left, right):
        def parts(s, rsid=None):
            out = []
            for piece in re.split(r"(\{PAGE\}|\{NUMPAGES\})", s):
                if piece == "{PAGE}":
                    out.append(field_runs("PAGE   \\* MERGEFORMAT", "1"))
                elif piece == "{NUMPAGES}":
                    out.append(field_runs("NUMPAGES   \\* MERGEFORMAT", "{NP}"))
                elif piece:
                    out.append(run_xml(piece, rsid=rsid))
            return out
        style = "Header" if tag == "hdr" else "Footer"
        # the footer's version line is retyped at each revision
        lr = rs.pick(rs.last) if (rs.by and tag == "ftr") else None
        p = para_xml(rs, parts(left, lr) + ['<w:r><w:tab/></w:r><w:r><w:tab/></w:r>'] + parts(right), style=style,
                     v=rs.first if rs.by else None)
        return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<w:%s %s>%s</w:%s>' % (tag, WNS, p, tag)

    ml, mr, mt, mb = margins
    sect = ('<w:sectPr w:rsidR="%s" w:rsidSect="%s"><w:headerReference w:type="default" r:id="rId4"/>'
            '<w:footerReference w:type="default" r:id="rId5"/><w:pgSz w:w="11906" w:h="16838" w:code="9"/>'
            '<w:pgMar w:top="%d" w:right="%d" w:bottom="%d" w:left="%d" w:header="567" w:footer="567" w:gutter="0"/>'
            '<w:cols w:space="708"/><w:docGrid w:linePitch="360"/></w:sectPr>'
            % (rs.pick(rs.first if rs.by else None), rs.root, mt, mr, mb, ml))
    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<w:document %s><w:body>%s%s</w:body></w:document>'
                % (WNS, "".join(body), sect))
    settings = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<w:settings %s '
                'xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
                'xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w10="urn:schemas-microsoft-com:office:word" '
                'xmlns:sl="http://schemas.openxmlformats.org/schemaLibrary/2006/main"><w:zoom w:percent="100"/>'
                '<w:proofState w:spelling="clean" w:grammar="clean"/><w:defaultTabStop w:val="720"/>'
                '<w:characterSpacingControl w:val="doNotCompress"/><w:hdrShapeDefaults><o:shapedefaults v:ext="edit" spidmax="2049"/>'
                '</w:hdrShapeDefaults><w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/>'
                '<w:compatSetting w:name="overrideTableStyleFontSizeAndJustification" w:uri="http://schemas.microsoft.com/office/word" w:val="1"/>'
                '<w:compatSetting w:name="enableOpenTypeFeatures" w:uri="http://schemas.microsoft.com/office/word" w:val="1"/>'
                '<w:compatSetting w:name="doNotFlipMirrorIndents" w:uri="http://schemas.microsoft.com/office/word" w:val="1"/>'
                '<w:compatSetting w:name="differentiateMultirowTableHeaders" w:uri="http://schemas.microsoft.com/office/word" w:val="1"/>'
                '<w:compatSetting w:name="useWord2013TrackBottomHyphenation" w:uri="http://schemas.microsoft.com/office/word" w:val="0"/>'
                '</w:compat><w:rsids><w:rsidRoot w:val="%s"/>%s</w:rsids><m:mathPr><m:mathFont m:val="Cambria Math"/>'
                '<m:brkBin m:val="before"/><m:brkBinSub m:val="--"/><m:smallFrac m:val="0"/><m:dispDef/><m:lMargin m:val="0"/>'
                '<m:rMargin m:val="0"/><m:defJc m:val="centerGroup"/><m:wrapIndent m:val="1440"/><m:intLim m:val="subSup"/>'
                '<m:naryLim m:val="undOvr"/></m:mathPr><w:themeFontLang w:val="en-GB"/><w:clrSchemeMapping w:bg1="light1" '
                'w:t1="dark1" w:bg2="light2" w:t2="dark2" w:accent1="accent1" w:accent2="accent2" w:accent3="accent3" '
                'w:accent4="accent4" w:accent5="accent5" w:accent6="accent6" w:hyperlink="hyperlink" '
                'w:followedHyperlink="followedHyperlink"/><w:shapeDefaults><o:shapedefaults v:ext="edit" spidmax="2049"/>'
                '<o:shapelayout v:ext="edit"><o:idmap v:ext="edit" data="1"/></o:shapelayout></w:shapeDefaults>'
                '<w:decimalSymbol w:val="."/><w:listSeparator w:val=","/><w14:docId w14:val="%s"/><w15:chartTrackingRefBased/>'
                '<w15:docId w15:val="{%s}"/></w:settings>'
                % (WIGN, rs.root, "".join('<w:rsid w:val="%s"/>' % x for x in rs.ids), rs.para_id(), guid(rs.r)))
    web = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<w:webSettings %s><w:optimizeForBrowser/><w:allowPNG/>'
           '</w:webSettings>' % WIGN)
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/webSettings" Target="webSettings.xml"/>'
            '<Relationship Id="rId7" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
            '<Relationship Id="rId6" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable" Target="fontTable.xml"/>'
            '<Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>'
            '<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>'
            '</Relationships>')
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
          '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
          '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
          '<Override PartName="/word/webSettings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.webSettings+xml"/>'
          '<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'
          '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
          '<Override PartName="/word/fontTable.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml"/>'
          '<Override PartName="/word/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
          '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
          '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
          '</Types>')
    pkg_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
                '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
                '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
                '</Relationships>')
    fonts = [font, "Times New Roman", "Calibri Light"] if font != "Calibri" else ["Calibri", "Times New Roman", "Calibri Light"]
    parts = [("[Content_Types].xml", ct), ("_rels/.rels", pkg_rels), ("word/document.xml", document),
             ("word/_rels/document.xml.rels", rels), ("word/header1.xml", hf("hdr", *header)),
             ("word/footer1.xml", hf("ftr", *footer)), ("word/theme/theme1.xml", theme_xml("word")),
             ("word/settings.xml", settings), ("word/styles.xml", styles_xml(font, size, heading_colour)),
             ("word/webSettings.xml", web), ("word/fontTable.xml", font_table(fonts))]
    # statistics as the word processor measures them on the laid-out document: pages, lines, paragraphs, words and
    # characters
    tmp = tempfile.mkdtemp()
    probe = os.path.join(tmp, "probe.docx")
    write_zip(probe, parts + [("docProps/core.xml", core_xml("x", "x", props["created"], props["modified"])),
                              ("docProps/app.xml", "<Properties/>")])
    pages, lines, starts, st = layout(probe)
    shutil.rmtree(tmp)
    words, chars, cws, paras = st["words"], st["chars"], st["cws"], st["paras"]
    # Word keeps where each page began when it last laid the document out, and the page count in the footer field
    document = rendered_breaks(document, plist, starts)
    parts = [(n, document if n == "word/document.xml" else d.replace("{NP}", str(pages))) for n, d in parts]
    app = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
           'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Template>Normal.dotm</Template>'
           '<TotalTime>%d</TotalTime><Pages>%d</Pages><Words>%d</Words><Characters>%d</Characters>'
           '<Application>Microsoft Office Word</Application><DocSecurity>0</DocSecurity><Lines>%d</Lines><Paragraphs>%d</Paragraphs>'
           '<ScaleCrop>false</ScaleCrop><HeadingPairs><vt:vector size="2" baseType="variant"><vt:variant><vt:lpstr>Title</vt:lpstr>'
           '</vt:variant><vt:variant><vt:i4>1</vt:i4></vt:variant></vt:vector></HeadingPairs><TitlesOfParts><vt:vector size="1" '
           'baseType="lpstr"><vt:lpstr>%s</vt:lpstr></vt:vector></TitlesOfParts><Company>%s</Company><LinksUpToDate>false</LinksUpToDate>'
           '<CharactersWithSpaces>%d</CharactersWithSpaces><SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged>'
           '<AppVersion>16.0000</AppVersion></Properties>'
           % (props["total_time"], pages, words, chars, lines, paras, esc(props["title"]), esc(props["company"]), cws))
    core = core_xml(props["creator"], props["modified_by"], props["created"], props["modified"], title=props["title"],
                    revision=props["revision"])
    write_zip(path, parts + [("docProps/core.xml", core), ("docProps/app.xml", app)])
    return pages


def guid(r):
    h = "%032X" % r.getrandbits(128)
    return "%s-%s-4%s-%s-%s" % (h[:8], h[8:12], h[13:16], "8" + h[17:20], h[20:32])


def layout(path):
    """the document as a word processor lays it out and counts it: pages; lines of text, each line of a table cell on
    its own and the running header and footer once; the first body line of each later page (the header is a page's
    first line and the footer its last); and the word processor's own paragraph, word and character counts"""
    from pypdf import PdfReader
    out = os.path.dirname(path)
    for fmt in ("pdf", "odt"):
        subprocess.run(["soffice", "--headless", "--convert-to", fmt, "--outdir", out, path], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    stem = os.path.splitext(path)[0]
    rd = PdfReader(stem + ".pdf")
    texts = [[l for l in p.extract_text().split("\n") if l.strip()] for p in rd.pages]
    frags = []                  # (page, y, x) of each piece of text the layout placed
    for k, p in enumerate(rd.pages):
        def seen(text, cm, tm, fd, fs, k=k):
            if text.strip():
                frags.append((k, round(tm[4] * cm[1] + tm[5] * cm[3] + cm[5], 1), round(tm[4] * cm[0] + tm[5] * cm[2] + cm[4], 1)))
        p.extract_text(visitor_text=seen)
    # a line starts at the margin, an indent or a table column's edge, positions that recur down the document; a piece
    # that starts mid-line (a change of run) does not start a line
    starts_at = {x for x, n in collections.Counter(x for _, _, x in frags).items() if n >= 3}
    lines = 2
    for k in range(len(rd.pages)):
        ys = sorted({y for kk, y, _ in frags if kk == k})
        body = set(ys[1:-1])
        lines += sum(1 for kk, y, x in frags if kk == k and y in body and x in starts_at)
    with zipfile.ZipFile(stem + ".odt") as z:
        meta = z.read("meta.xml").decode("utf-8")
    ds = dict(re.findall(r'meta:([a-z-]+)="(\d+)"', re.search(r"<meta:document-statistic[^>]*>", meta).group(0)))
    st = dict(words=int(ds["word-count"]), chars=int(ds["non-whitespace-character-count"]), cws=int(ds["character-count"]),
              paras=int(ds["paragraph-count"]))
    return len(rd.pages), lines, [t[1] for t in texts[1:] if len(t) > 2], st


def rendered_breaks(document, plist, starts):
    """put w:lastRenderedPageBreak where each later page begins: at the start of the paragraph (or table row) that
    opens the page, or inside the run where a paragraph runs over"""
    from xml.sax.saxutils import unescape
    paras = list(re.finditer(r"<w:p [^>]*>.*?</w:p>|<w:p [^>]*/>", document, re.S))
    assert len(paras) == len(plist), "paragraph count %d against %d texts" % (len(paras), len(plist))
    norm = lambda x: " ".join(x.split())
    marks, after = [], 0
    for line in starts:
        key = norm(line)[:40]
        hit = None
        for i in range(after, len(plist)):
            t = norm(plist[i])
            n = min(len(t), len(key))
            if n >= 6 and t[:n] == key[:n]:
                hit = (i, 0)
                break
            j = t.find(key)
            if j > 0:
                hit = (i, j)
                break
        if hit is None:
            continue
        marks.append(hit)
        after = hit[0] + 1
    for i, off in reversed(marks):
        m = paras[i]
        px = m.group(0)
        runs = list(re.finditer(r'(<w:r(?: w:rsidR="[0-9A-F]{8}")?>)(<w:rPr>.*?</w:rPr>)?<w:t(?: xml:space="preserve")?>(.*?)</w:t></w:r>',
                                px, re.S))
        pos = 0
        for r in runs:
            txt = unescape(r.group(3), {"&quot;": '"'})
            if off < pos + len(txt) or r is runs[-1]:
                k, ro, rpr = max(0, off - pos), r.group(1), r.group(2) or ""
                tx = lambda x: '<w:t%s>%s</w:t>' % (' xml:space="preserve"' if x != x.strip() or "  " in x else "", esc(x))
                new = ('%s%s<w:lastRenderedPageBreak/>%s</w:r>' % (ro, rpr, tx(txt)) if k == 0 else
                       '%s%s%s</w:r>%s%s<w:lastRenderedPageBreak/>%s</w:r>' % (ro, rpr, tx(txt[:k]), ro, rpr, tx(txt[k:])))
                px = px[:r.start()] + new + px[r.end():]
                break
            pos += len(txt)
        document = document[:m.start()] + px + document[m.end():]
    return document


def pdf_from_docx(docx_path, pdf_path):
    tmp = tempfile.mkdtemp()
    src = os.path.join(tmp, "note.docx")
    shutil.copy(docx_path, src)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, src], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.move(os.path.join(tmp, "note.pdf"), pdf_path)
    shutil.rmtree(tmp)


# ------------------------------------------------------------------------------------------------------- Excel

XNS = ('xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
       'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
       'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" mc:Ignorable="x14ac xr xr2 xr3" '
       'xmlns:x14ac="http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac" '
       'xmlns:xr="http://schemas.microsoft.com/office/spreadsheetml/2014/revision" '
       'xmlns:xr2="http://schemas.microsoft.com/office/spreadsheetml/2015/revision2" '
       'xmlns:xr3="http://schemas.microsoft.com/office/spreadsheetml/2016/revision3"')
BUILTIN_FMT = {"General": 0, "0": 1, "0.00": 2, "#,##0": 3, "#,##0.00": 4, "0%": 9, "0.00%": 10, "mm-dd-yy": 14,
               "d-mmm-yy": 15, "d/mm/yyyy": 14, "dd/mm/yyyy": 14}
EXCEL_EPOCH = dt.date(1899, 12, 30)


def col_letter(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def col_width(chars):
    return int((chars * 7 + 5) / 7 * 256) / 256.0


def num(v):
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, int):
        return str(v)
    r = repr(float(v))
    return r[:-2] if r.endswith(".0") else r


# the Excel window each author last saved from: maximised on one or two screens, or a restored window
WINDOWS = [(-120, -120, 29040, 15840), (-110, -110, 25820, 15500), (28680, -120, 29040, 15720), (-108, -108, 23256, 12576),
           (1950, 1560, 21600, 11295), (-120, -120, 38640, 21120), (0, 0, 28800, 12300)]
BUILDS = ["27425", "28526", "28827", "29127"]


def xlsx_from_openpyxl(wb, path, creator, modified_by, created, modified, company="Strathallan Council",
                       seed=0, active=0):
    rnd = random.Random(seed)
    window = WINDOWS[random.Random(seed * 7 + 3).randrange(len(WINDOWS))]
    build = BUILDS[random.Random(seed * 11 + 5).randrange(len(BUILDS))]
    fonts = ['<font><sz val="11"/><color theme="1"/><name val="Calibri"/><family val="2"/><scheme val="minor"/></font>']
    fills = ['<fill><patternFill patternType="none"/></fill>', '<fill><patternFill patternType="gray125"/></fill>']
    numfmts, xfs = {}, ['<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>']
    font_ix, fill_ix, xf_ix = {fonts[0]: 0}, {}, {(0, 0, 0, ""): 0}
    sst, sst_ix, sst_count = [], {}, [0]

    def argb(c):
        if c is None or not isinstance(getattr(c, "rgb", None), str):
            return None
        v = c.rgb.upper()
        v = v if len(v) == 8 else "FF" + v
        v = "FF" + v[2:]
        return None if v == "FF000000" else v

    def font_of(f):
        if f is None:
            return 0
        bold, ital, colour = bool(f.b), bool(f.i), argb(f.color)
        size = float(f.sz) if f.sz else 11.0
        if not bold and not ital and colour is None and size == 11.0:
            return 0
        x = "<font>%s%s<sz val=\"%s\"/>%s<name val=\"Calibri\"/><family val=\"2\"/><scheme val=\"minor\"/></font>" % (
            "<b/>" if bold else "", "<i/>" if ital else "", num(size),
            '<color rgb="%s"/>' % colour if colour else '<color theme="1"/>')
        if x not in font_ix:
            font_ix[x] = len(fonts)
            fonts.append(x)
        return font_ix[x]

    def fill_of(fl):
        if fl is None or fl.fill_type != "solid":
            return 0
        rgb = fl.fgColor.rgb if isinstance(fl.fgColor.rgb, str) else "FFFFFFFF"
        rgb = "FF" + rgb[-6:].upper()            # Excel writes an opaque colour
        x = '<fill><patternFill patternType="solid"><fgColor rgb="%s"/><bgColor indexed="64"/></patternFill></fill>' % rgb
        if x not in fill_ix:
            fill_ix[x] = len(fills)
            fills.append(x)
        return fill_ix[x]

    def fmt_of(code, is_date):
        if is_date and code in ("General", "yyyy-mm-dd h:mm:ss", "yyyy-mm-dd"):
            return 14
        if code in BUILTIN_FMT:
            return BUILTIN_FMT[code]
        if code not in numfmts:
            numfmts[code] = 164 + len(numfmts)
        return numfmts[code]

    def xf_of(cell, is_date):
        f, fl, nf = font_of(cell.font), fill_of(cell.fill), fmt_of(cell.number_format, is_date)
        al = cell.alignment
        align = ""
        if al is not None and (al.wrap_text or al.horizontal or al.vertical):
            align = "<alignment%s%s%s/>" % (' horizontal="%s"' % al.horizontal if al.horizontal else "",
                                             ' vertical="%s"' % al.vertical if al.vertical else "",
                                             ' wrapText="1"' if al.wrap_text else "")
        key = (nf, f, fl, align)
        if key not in xf_ix:
            attrs = '<xf numFmtId="%d" fontId="%d" fillId="%d" borderId="0" xfId="0"%s%s%s%s' % (
                nf, f, fl, ' applyNumberFormat="1"' if nf else "", ' applyFont="1"' if f else "", ' applyFill="1"' if fl else "",
                ' applyAlignment="1"' if align else "")
            xf_ix[key] = len(xfs)
            xfs.append(attrs + (">%s</xf>" % align if align else "/>"))
        return xf_ix[key]

    def s_index(text):
        sst_count[0] += 1
        if text not in sst_ix:
            sst_ix[text] = len(sst)
            sst.append(text)
        return sst_ix[text]

    sheets_xml, names, filters = [], [], []
    for si, ws in enumerate(wb.worksheets):
        names.append(ws.title)
        rows_out, maxc, maxr = [], 1, 1
        rows_raw = []                            # (row, first column, last column, height, cells)
        for row in ws.iter_rows():
            cells, used = [], []
            for c in row:
                v = c.value
                if v is None:
                    if c.has_style and c.fill is not None and c.fill.fill_type == "solid":
                        cells.append('<c r="%s" s="%d"/>' % (c.coordinate, xf_of(c, False)))
                        used.append(c.column)
                    continue
                if isinstance(v, (dt.datetime, dt.date)):
                    d = v.date() if isinstance(v, dt.datetime) else v
                    cells.append('<c r="%s" s="%d"><v>%d</v></c>' % (c.coordinate, xf_of(c, True), (d - EXCEL_EPOCH).days))
                elif isinstance(v, str):
                    st = xf_of(c, False)
                    cells.append('<c r="%s"%s t="s"><v>%d</v></c>' % (c.coordinate, ' s="%d"' % st if st else "", s_index(v)))
                else:
                    st = xf_of(c, False)
                    cells.append('<c r="%s"%s><v>%s</v></c>' % (c.coordinate, ' s="%d"' % st if st else "", num(v)))
                used.append(c.column)
            if cells:
                r = row[0].row
                maxr, maxc = max(maxr, r), max(maxc, max(used))
                rows_raw.append((r, min(used), max(used), ws.row_dimensions[r].height, cells))
        # Excel writes one spans value per block of 16 rows, the columns used anywhere in the block
        block = {}
        for r, lo, hi, _, _ in rows_raw:
            b = (r - 1) // 16
            block[b] = (min(lo, block.get(b, (lo, hi))[0]), max(hi, block.get(b, (lo, hi))[1]))
        for r, lo, hi, ht, cells in rows_raw:
            sp = block[(r - 1) // 16]
            rows_out.append('<row r="%d" spans="%d:%d"%s x14ac:dyDescent="0.25">%s</row>'
                            % (r, sp[0], sp[1], ' ht="%s" customHeight="1"' % num(ht) if ht else "", "".join(cells)))
        dim = "A1:%s%d" % (col_letter(maxc), maxr)
        cols = []
        for k in range(1, maxc + 1):
            cd = ws.column_dimensions.get(col_letter(k))
            if cd is not None and cd.width:
                cols.append('<col min="%d" max="%d" width="%s" customWidth="1"/>' % (k, k, num(col_width(cd.width))))
        fp = ws.freeze_panes
        if fp:
            m = re.match(r"([A-Z]+)(\d+)", fp)
            ysplit = int(m.group(2)) - 1
            view = ('<sheetView%s workbookViewId="0"><pane ySplit="%d" topLeftCell="%s" activePane="bottomLeft" state="frozen"/>'
                    '<selection pane="bottomLeft" activeCell="%s" sqref="%s"/></sheetView>'
                    % (' tabSelected="1"' if si == active else "", ysplit, fp, fp, fp))
        else:
            view = ('<sheetView%s workbookViewId="0"><selection activeCell="A1" sqref="A1"/></sheetView>'
                    % (' tabSelected="1"' if si == active else ""))
        af = ""
        if ws.auto_filter.ref:
            af = '<autoFilter ref="%s" xr:uid="{%s}"/>' % (ws.auto_filter.ref, guid(rnd))
            filters.append((si, ws.title, ws.auto_filter.ref))
        x = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<worksheet %s xr:uid="{%s}"><dimension ref="%s"/>'
             '<sheetViews>%s</sheetViews><sheetFormatPr defaultRowHeight="15" x14ac:dyDescent="0.25"/>%s<sheetData>%s</sheetData>'
             '%s<pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/>'
             '<pageSetup paperSize="9" orientation="%s"/></worksheet>'
             % (XNS, guid(rnd), dim, view, "<cols>%s</cols>" % "".join(cols) if cols else "", "".join(rows_out), af,
                "landscape" if maxc > 6 else "portrait"))
        sheets_xml.append(x)
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
              'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" mc:Ignorable="x14ac x16r2 xr" '
              'xmlns:x14ac="http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac" '
              'xmlns:x16r2="http://schemas.microsoft.com/office/spreadsheetml/2015/02/main" '
              'xmlns:xr="http://schemas.microsoft.com/office/spreadsheetml/2014/revision">%s'
              '<fonts count="%d" x14ac:knownFonts="1">%s</fonts><fills count="%d">%s</fills>'
              '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
              '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
              '<cellXfs count="%d">%s</cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
              '<dxfs count="0"/><tableStyles count="0" defaultTableStyle="TableStyleMedium2" defaultPivotStyle="PivotStyleLight16"/>'
              '<extLst><ext uri="{EB79DEF2-80B8-43e5-95BD-54CBDDF9020C}" xmlns:x14="http://schemas.microsoft.com/office/spreadsheetml/2009/9/main">'
              '<x14:slicerStyles defaultSlicerStyle="SlicerStyleLight1"/></ext><ext uri="{9260A510-F301-46a8-8635-F512D64BE5F5}" '
              'xmlns:x15="http://schemas.microsoft.com/office/spreadsheetml/2010/11/main"><x15:timelineStyles '
              'defaultTimelineStyle="TimeSlicerStyleLight1"/></ext></extLst></styleSheet>'
              % (('<numFmts count="%d">%s</numFmts>' % (len(numfmts), "".join('<numFmt numFmtId="%d" formatCode="%s"/>' % (i, esc(c))
                                                                                for c, i in numfmts.items()))) if numfmts else "",
                 len(fonts), "".join(fonts), len(fills), "".join(fills), len(xfs), "".join(xfs)))
    sst_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
               'count="%d" uniqueCount="%d">%s</sst>'
               % (sst_count[0], len(sst), "".join('<si><t%s>%s</t></si>' % (' xml:space="preserve"' if t != t.strip() else "", esc(t)) for t in sst)))
    dn = ""
    if filters:
        dn = "<definedNames>%s</definedNames>" % "".join(
            '<definedName name="_xlnm._FilterDatabase" localSheetId="%d" hidden="1">%s!%s</definedName>'
            % (si, ("'%s'" % t) if " " in t else t, "$" + "$".join(re.findall(r"[A-Z]+|\d+", ref.split(":")[0])) + ":$"
               + "$".join(re.findall(r"[A-Z]+|\d+", ref.split(":")[1]))) for si, t, ref in filters)
    workbook = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
                'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" mc:Ignorable="x15 xr xr6 xr10 xr2" '
                'xmlns:x15="http://schemas.microsoft.com/office/spreadsheetml/2010/11/main" '
                'xmlns:xr="http://schemas.microsoft.com/office/spreadsheetml/2014/revision" '
                'xmlns:xr6="http://schemas.microsoft.com/office/spreadsheetml/2016/revision6" '
                'xmlns:xr10="http://schemas.microsoft.com/office/spreadsheetml/2016/revision10" '
                'xmlns:xr2="http://schemas.microsoft.com/office/spreadsheetml/2015/revision2">'
                '<fileVersion appName="xl" lastEdited="7" lowestEdited="7" rupBuild="%s"/><workbookPr defaultThemeVersion="166925"/>'
                '<xr:revisionPtr revIDLastSave="0" documentId="13_ncr:1_{%s}" xr6:coauthVersionLast="47" xr6:coauthVersionMax="47" '
                'xr10:uidLastSave="{00000000-0000-0000-0000-000000000000}"/><bookViews><workbookView xWindow="%d" yWindow="%d" '
                'windowWidth="%d" windowHeight="%d"%s xr2:uid="{%s}"/></bookViews><sheets>%s</sheets>%s<calcPr calcId="191029"/>'
                '</workbook>'
                % ((build,) + (guid(rnd),) + window + (' activeTab="%d"' % active if active else "", guid(rnd)) +
                   ("".join('<sheet name="%s" sheetId="%d" r:id="rId%d"/>' % (esc(n), k + 1, k + 1) for k, n in enumerate(names)), dn)))
    n = len(names)
    wrels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">%s'
             '<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>'
             '<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
             '<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>'
             '</Relationships>'
             % ("".join('<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
                        'Target="worksheets/sheet%d.xml"/>' % (k + 1, k + 1) for k in range(n)), n + 1, n + 2, n + 3))
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>%s'
          '<Override PartName="/xl/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
          '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
          '<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>'
          '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
          '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>'
          % "".join('<Override PartName="/xl/worksheets/sheet%d.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
                    % (k + 1) for k in range(n)))
    pkg_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
                '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" Target="docProps/core.xml"/>'
                '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
                '</Relationships>')
    app = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
           'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Microsoft Excel</Application>'
           '<DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop><HeadingPairs><vt:vector size="2" baseType="variant"><vt:variant>'
           '<vt:lpstr>Worksheets</vt:lpstr></vt:variant><vt:variant><vt:i4>%d</vt:i4></vt:variant></vt:vector></HeadingPairs>'
           '<TitlesOfParts><vt:vector size="%d" baseType="lpstr">%s</vt:vector></TitlesOfParts><Company>%s</Company>'
           '<LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged>'
           '<AppVersion>16.0300</AppVersion></Properties>' % (n, n, "".join("<vt:lpstr>%s</vt:lpstr>" % esc(x) for x in names), esc(company)))
    parts = [("[Content_Types].xml", ct), ("_rels/.rels", pkg_rels), ("xl/workbook.xml", workbook),
             ("xl/_rels/workbook.xml.rels", wrels)]
    parts += [("xl/worksheets/sheet%d.xml" % (k + 1), x) for k, x in enumerate(sheets_xml)]
    parts += [("xl/theme/theme1.xml", theme_xml("excel")), ("xl/styles.xml", styles),
              ("xl/sharedStrings.xml", sst_xml), ("docProps/core.xml", core_xml(creator, modified_by, created, modified)),
              ("docProps/app.xml", app)]
    write_zip(path, parts)


def col_num(letters):
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n
