"""The credit union's own documents: its AML/ATF compliance programme (version 6.1) and the AML
Compliance Committee's terms of reference.

The programme files what the January review tests and how the credit union counts large cash for
reporting. It says nothing about how the cash a member's trade produced is estimated.
"""
import datetime as dt
import os

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import common as C

SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["BodyText"], fontName="Helvetica", fontSize=9, leading=12.4,
                      alignment=TA_JUSTIFY, spaceAfter=4.5)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, spaceAfter=6)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=10, spaceAfter=3, spaceBefore=7)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=7.6, leading=9.6)
CELL = ParagraphStyle("c", fontName="Helvetica", fontSize=7.8, leading=9.6)
TBL = TableStyle([("GRID", (0, 0), (-1, -1), 0.3, colors.Color(0.5, 0.5, 0.5)),
                  ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.88, 0.91, 0.94)),
                  ("VALIGN", (0, 0), (-1, -1), "TOP"),
                  ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                  ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)])

CONTROL = {
    "hrcu_aml_atf_compliance_programme_v6-1.pdf": "by at least twice the cash that trade produced",
    "aml_compliance_committee_terms_of_reference.docx": "up to four new enhanced investigations",
}


def _footer(canv, doc):
    canv.saveState()
    canv.setFont("Helvetica", 7)
    canv.drawString(20 * mm, 11 * mm, "Harlow Reach Credit Union  |  AML/ATF Compliance Programme v6.1  |  Internal")
    canv.drawRightString(196 * mm, 11 * mm, "Page %d" % doc.page)
    canv.restoreState()


def _scrub(path):
    """Put the credit union's compliance office in the producer fields instead of the writing library's
    name, keeping every byte offset (reduce-house-fixes H1)."""
    data = bytearray(open(path, "rb").read())
    org = C.PRODUCER.encode()
    for comment in (b"ReportLab Generated PDF document (opensource)",
                    b"ReportLab generated PDF document -- digest (opensource)"):
        i = data.find(comment)
        while i != -1:
            data[i:i + len(comment)] = org[:len(comment)].ljust(len(comment), b" ")
            i = data.find(comment)
    for key in (b"/Producer (", b"/Creator ("):
        i = data.find(key)
        while i != -1:
            j = i + len(key)
            while j < len(data):
                if data[j:j + 1] == b"\\":
                    j += 2
                    continue
                if data[j:j + 1] == b")":
                    break
                j += 1
            old = data[i + len(key):j]
            data[i + len(key):j] = org[:len(old)].ljust(len(old), b" ")
            i = data.find(key, j)
    stamp = b"D:20260324090000+00'00'"
    for field in (b"/CreationDate (", b"/ModDate ("):
        i = data.find(field)
        while i != -1:
            j = data.find(b")", i + len(field))
            if j != -1 and j - (i + len(field)) == len(stamp):
                data[i + len(field):j] = stamp
            i = data.find(field, j if j != -1 else i + len(field))
    open(path, "wb").write(bytes(data))


def programme(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    doc = SimpleDocTemplate(path, pagesize=LETTER, title="AML/ATF Compliance Programme v6.1", author="",
                            subject="", creator="", leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=17 * mm, bottomMargin=18 * mm)
    P = lambda t: Paragraph(t, BODY)
    s = []
    s.append(Paragraph("Harlow Reach Credit Union<br/>Anti-Money Laundering and Anti-Terrorist Financing "
                       "Compliance Programme", H1))
    s.append(Table([[Paragraph("<b>Version</b>", CELL), Paragraph("6.1", CELL), Paragraph("<b>Approved</b>", CELL),
                     Paragraph("Board of Directors, 24 March 2026", CELL)],
                    [Paragraph("<b>Effective</b>", CELL), Paragraph("1 April 2026", CELL), Paragraph("<b>Owner</b>", CELL),
                     Paragraph("Chief Anti-Money Laundering Officer (Kristine Kirby)", CELL)],
                    [Paragraph("<b>Replaces</b>", CELL), Paragraph("Version 6.0 (April 2025)", CELL),
                     Paragraph("<b>Next review</b>", CELL), Paragraph("March 2027", CELL)]],
                   colWidths=[22 * mm, 40 * mm, 24 * mm, 88 * mm], style=TBL))
    s.append(Spacer(1, 5))
    s.append(Paragraph("1. Purpose and scope", H2))
    s.append(P("This programme sets out how Harlow Reach Credit Union meets its obligations under the Proceeds of "
               "Crime (Money Laundering) and Terrorist Financing Act and its regulations. It applies to every "
               "branch, deposit ATM, night depository and channel through which the credit union serves members, "
               "and to Regional Cash Services, which counts night deposits for the branches that have no vault "
               "staff. Version 6.1 adds section 7.3. Section 6.2 restates, without change, the large cash transaction "
               "window and reporting rules in force since version 6.0 (April 2025)."))
    s.append(Paragraph("2. Governance", H2))
    s.append(P("The Board approves the programme and receives the Chief Anti-Money Laundering Officer's report each "
               "quarter. The AML Compliance Committee, under its own terms of reference, oversees the programme's "
               "operation and approves enhanced investigations. Business Services, which holds the business members' "
               "relationships, is the first line: it keeps their client due diligence current, performs the enhanced "
               "due diligence the higher-risk segments require and refers members to the Financial Intelligence Unit "
               "(the Unit). The Unit, led by the FIU Lead, Jeffrey Melendez, reviews monitoring alerts, conducts "
               "investigations and prepares reports to FINTRAC."))
    s.append(Paragraph("3. Risk assessment and segments", H2))
    s.append(P("Members are assigned to monitoring segments on the business type recorded in the member register. The "
               "cash-intensive business segment (CIB) holds the business members whose business type is a "
               "full-service restaurant; a quick-service or takeout restaurant; a cafe or bakery; a convenience "
               "store; a grocery or specialty food store; a bar or pub; a hair, nail or beauty salon; a car wash; a "
               "laundromat or dry cleaner; or a mobile food vendor. The segment is rated higher risk for the "
               "placement of criminal cash because its members take cash from the public in the ordinary course of "
               "trade."))
    s.append(Paragraph("4. Know your client", H2))
    s.append(P("The credit union identifies every member and every person holding 25 per cent or more of a business "
               "member, and records a client due diligence profile at onboarding: the nature of the business, its "
               "anticipated annual turnover and its anticipated monthly deposits, cash and total, as the member "
               "states them. The profile is reviewed annually for members rated High, every two years for Medium "
               "and every three years for Low, and whenever an event calls for it."))
    s.append(Paragraph("5. Ongoing monitoring", H2))
    s.append(P("Transactions on business accounts are monitored on the core banking system each night. Alerts are "
               "reviewed by the Unit within ten business days and are closed, escalated or referred for an "
               "enhanced investigation under section 7. For monitoring and the January review, cash is counted on "
               "the credit union's business date of each credit."))
    s.append(Paragraph("6. Reporting to FINTRAC", H2))
    s.append(P("<b>6.1 Large cash transaction reports.</b> The credit union reports the receipt of CAD 10,000 or more "
               "in cash in a single transaction, or in two or more transactions that together total CAD 10,000 or "
               "more within 24 consecutive hours, received from or on behalf of the same member."))
    s.append(P("<b>6.2 The window.</b> A window opens at a member's first cash receipt and closes 24 hours later. "
               "Cash the member pays into any of its accounts, at any branch, deposit ATM or night depository, "
               "counts toward the open window, and a receipt after the window closes opens a new one. A night "
               "deposit is received when its bag is opened and counted. Only the cash in a deposit counts; "
               "cheques deposited with it do not. Each window whose cash totals CAD 10,000 or more requires one "
               "report, and each report has its own reference. A correction carries the reference of the report it "
               "amends; it is not a further report, and the amended report keeps the submission date of the "
               "original. A report is due within 15 calendar days after the day, on Pacific time, on which the first "
               "cash it reports was received. Windows belong to the quarter in which they open, on Pacific time, and a "
               "report to the quarter of the transaction date it reports."))
    s.append(P("<b>6.3 Suspicious transaction reports</b> are submitted as soon as practicable once the Unit has "
               "reasonable grounds to suspect that a transaction is related to money laundering or terrorist "
               "activity financing. <b>6.4 Electronic funds transfer reports</b> are made for international "
               "transfers of CAD 10,000 or more, under the same 24-hour rule."))
    s.append(Paragraph("7. Enhanced investigation", H2))
    s.append(P("<b>7.1 Triggers.</b> An enhanced investigation can follow an escalated alert, a branch referral, a "
               "request from law enforcement, or a referral from the January review in section 7.2."))
    s.append(P("<b>7.2 The January review.</b> Each January Business Services reviews every member of the "
               "cash-intensive business segment on the calendar year just closed, as the segment's enhanced due "
               "diligence."))
    s.append(P("<b>7.3 Case acceptance.</b> Business Services refers to the Unit for an enhanced investigation a "
               "member of the cash-intensive business segment where the cash paid into the member's accounts in the "
               "calendar year exceeds the cash the member's trade with its customers produced in that year by CAD "
               "100,000 or more, and by at least twice the cash that trade produced. Cash is counted on the credit "
               "union's business date of each credit. The members that meet the test are presented to the Committee "
               "at its January meeting, in descending order of the excess."))
    s.append(P("<b>7.4 Conduct.</b> An investigation reviews the member's accounts, its profile and its counterparties, "
               "and closes with no further action, a suspicious transaction report, or a recommendation to exit the "
               "relationship."))
    s.append(Paragraph("8. Records and training", H2))
    s.append(P("Records are kept for at least five years. Staff who handle cash or open accounts complete AML training "
               "on joining and each year. The programme's effectiveness is reviewed by an independent party every "
               "two years."))
    doc.build(s, onFirstPage=_footer, onLaterPages=_footer)
    _scrub(path)


TOR = [
    ("Heading1", "AML Compliance Committee: Terms of Reference"),
    (None, "Harlow Reach Credit Union. Approved by the Board of Directors on 14 November 2025."),
    ("Heading2", "Purpose"),
    (None, "The Committee oversees the operation of the credit union's AML/ATF compliance programme and approves the "
           "enhanced investigations the Financial Intelligence Unit brings to it."),
    ("Heading2", "Membership"),
    ("ListBullet", "Chief Anti-Money Laundering Officer, Kristine Kirby (Chair)"),
    ("ListBullet", "FIU Lead, Jeffrey Melendez"),
    ("ListBullet", "Vice-President, Member Services"),
    ("ListBullet", "Manager, Business Services"),
    ("ListBullet", "Director, Enterprise Risk"),
    ("ListBullet", "Manager, Retail Banking"),
    ("Heading2", "Meetings"),
    (None, "The Committee meets in January, April, July and October, and whenever the Chair calls a meeting. Three "
           "members, one of them the Chair, make a quorum. The January 2027 meeting is on Wednesday 20 January 2027."),
    ("Heading2", "Responsibilities"),
    ("ListBullet", "Approve the enhanced investigations the Unit presents, including those Business Services refers "
                   "under section 7.3 of the programme after the January review."),
    ("ListBullet", "Receive the Unit's quarterly report on large cash transaction, suspicious transaction and "
                   "electronic funds transfer reporting."),
    ("ListBullet", "Track remediation of findings from FINTRAC examinations and the independent effectiveness review."),
    ("Heading2", "Capacity"),
    (None, "The Unit can take up to four new enhanced investigations in a quarter alongside its alert work. Where more "
           "are approved, the Committee sets the order in which they start."),
    ("Heading2", "Minutes"),
    (None, "The Unit keeps the minutes. They record each investigation approved and the reason, and are kept with the "
           "programme's records."),
]

# the terms of reference were last saved when the 2027 meeting dates went in (UTC, as the property part keeps it)
TOR_SAVED = "2026-11-23T18:41:00Z"

_W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
_R = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
_HEAD = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
_CT = "application/vnd.openxmlformats-officedocument.wordprocessingml."


def _x(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


_SCRIPTS = ("Jpan", "Hang", "Hans", "Hant", "Arab", "Hebr", "Thai", "Ethi", "Beng", "Gujr", "Khmr", "Knda", "Guru",
            "Cans", "Cher", "Yiii", "Tibt", "Thaa", "Deva", "Telu", "Taml", "Syrc", "Orya", "Mlym", "Laoo", "Sinh",
            "Mong", "Viet", "Uigh", "Geor", "Armn", "Bugi", "Bopo", "Java", "Lisu", "Mymr", "Nkoo", "Olck", "Osma",
            "Phag", "Syrn", "Syrj", "Syre", "Sora", "Tale", "Talu", "Tfng")
_MAJOR = ("游ゴシック Light", "맑은 고딕", "等线 Light",
          "新細明體", "Times New Roman", "Times New Roman", "Angsana New", "Nyala", "Vrinda", "Shruti",
          "MoolBoran", "Tunga", "Raavi", "Euphemia", "Plantagenet Cherokee", "Microsoft Yi Baiti", "Microsoft Himalaya",
          "MV Boli", "Mangal", "Gautami", "Latha", "Estrangelo Edessa", "Kalinga", "Kartika", "DokChampa",
          "Iskoola Pota", "Mongolian Baiti", "Times New Roman", "Microsoft Uighur", "Sylfaen", "Arial",
          "Leelawadee UI", "Microsoft JhengHei", "Javanese Text", "Segoe UI", "Myanmar Text", "Ebrima", "Nirmala UI",
          "Ebrima", "Phagspa", "Estrangelo Edessa", "Estrangelo Edessa", "Estrangelo Edessa", "Nirmala UI",
          "Microsoft Tai Le", "Microsoft New Tai Lue", "Ebrima")
_MINOR = ("游明朝", "맑은 고딕", "等线", "新細明體", "Arial",
          "Arial", "Cordia New", "Nyala", "Vrinda", "Shruti", "DaunPenh", "Tunga", "Raavi", "Euphemia",
          "Plantagenet Cherokee", "Microsoft Yi Baiti", "Microsoft Himalaya", "MV Boli", "Mangal", "Gautami", "Latha",
          "Estrangelo Edessa", "Kalinga", "Kartika", "DokChampa", "Iskoola Pota", "Mongolian Baiti", "Arial",
          "Microsoft Uighur", "Sylfaen", "Arial", "Leelawadee UI", "Microsoft JhengHei", "Javanese Text", "Segoe UI",
          "Myanmar Text", "Ebrima", "Nirmala UI", "Ebrima", "Phagspa", "Estrangelo Edessa", "Estrangelo Edessa",
          "Estrangelo Edessa", "Nirmala UI", "Microsoft Tai Le", "Microsoft New Tai Lue", "Ebrima")


def _theme():
    """The Office theme a Word 2016 save carries in word/theme/theme1.xml (Calibri Light and Calibri, the Office
    colour set)."""
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


def _docx_parts(blocks, core, app):
    """A Word package written part by part: the document, the Office theme, one small styles part (Normal, two
    headings and List Bullet on the theme's fonts), the bullet's numbering, settings, web settings, the font table
    and the two property parts. No thumbnail, no custom XML and no second styles part."""
    body = []
    for style, text in blocks:
        ppr = '<w:pPr><w:pStyle w:val="%s"/></w:pPr>' % style if style else ""
        body.append('<w:p>%s<w:r><w:t>%s</w:t></w:r></w:p>' % (ppr, _x(text)))
    sect = ('<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" '
            'w:left="1440" w:header="708" w:footer="708" w:gutter="0"/><w:cols w:space="708"/>'
            '<w:docGrid w:linePitch="360"/></w:sectPr>')
    document = _HEAD + '<w:document %s %s><w:body>%s%s</w:body></w:document>' % (_W, _R, "".join(body), sect)
    styles = _HEAD + (
        '<w:styles %s><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:asciiTheme="minorHAnsi" '
        'w:eastAsiaTheme="minorHAnsi" w:hAnsiTheme="minorHAnsi" w:cstheme="minorBidi"/><w:sz w:val="21"/><w:szCs w:val="21"/><w:lang w:val="en-CA" '
        'w:eastAsia="en-US" w:bidi="ar-SA"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="120" '
        'w:line="264" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>'
        '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>'
        '<w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="240" '
        'w:after="160"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:rFonts w:asciiTheme="majorHAnsi" '
        'w:eastAsiaTheme="majorEastAsia" w:hAnsiTheme="majorHAnsi" w:cstheme="majorBidi"/><w:b/><w:color w:val="1F3B57"/><w:sz w:val="30"/>'
        '<w:szCs w:val="30"/></w:rPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/>'
        '<w:next w:val="Normal"/><w:uiPriority w:val="9"/><w:unhideWhenUsed/><w:qFormat/><w:pPr><w:keepNext/>'
        '<w:spacing w:before="200" w:after="80"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:rFonts '
        'w:asciiTheme="majorHAnsi" w:eastAsiaTheme="majorEastAsia" w:hAnsiTheme="majorHAnsi" w:cstheme="majorBidi"/><w:b/>'
        '<w:color w:val="1F3B57"/><w:sz w:val="23"/><w:szCs w:val="23"/></w:rPr></w:style>'
        '<w:style w:type="paragraph" w:styleId="ListBullet"><w:name w:val="List Bullet"/><w:basedOn w:val="Normal"/>'
        '<w:uiPriority w:val="99"/><w:unhideWhenUsed/><w:pPr><w:numPr><w:numId w:val="1"/></w:numPr>'
        '<w:spacing w:after="60"/><w:contextualSpacing/></w:pPr></w:style>'
        '<w:style w:type="character" w:default="1" w:styleId="DefaultParagraphFont"><w:name w:val="Default Paragraph '
        'Font"/><w:uiPriority w:val="1"/><w:semiHidden/><w:unhideWhenUsed/></w:style>'
        '<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/>'
        '<w:uiPriority w:val="99"/><w:semiHidden/><w:unhideWhenUsed/><w:tblPr><w:tblInd w:w="0" w:type="dxa"/>'
        '<w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/>'
        '<w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>'
        '<w:style w:type="numbering" w:default="1" w:styleId="NoList"><w:name w:val="No List"/>'
        '<w:uiPriority w:val="99"/><w:semiHidden/><w:unhideWhenUsed/></w:style></w:styles>') % _W
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
        '</w:compat><w:themeFontLang w:val="en-CA"/><w:clrSchemeMapping w:bg1="light1" w:t1="dark1" '
        'w:bg2="light2" w:t2="dark2" w:accent1="accent1" w:accent2="accent2" w:accent3="accent3" w:accent4="accent4" '
        'w:accent5="accent5" w:accent6="accent6" w:hyperlink="hyperlink" w:followedHyperlink="followedHyperlink"/>'
        '<w:decimalSymbol w:val="."/><w:listSeparator w:val=","/>'
        '</w:settings>') % _W
    web = _HEAD + '<w:webSettings %s><w:optimizeForBrowser/><w:allowPNG/></w:webSettings>' % _W
    fonts = _HEAD + (
        '<w:fonts %s><w:font w:name="Calibri"><w:panose1 w:val="020F0502020204030204"/><w:charset w:val="00"/>'
        '<w:family w:val="swiss"/><w:pitch w:val="variable"/></w:font><w:font w:name="Times New Roman">'
        '<w:panose1 w:val="02020603050405020304"/><w:charset w:val="00"/><w:family w:val="roman"/>'
        '<w:pitch w:val="variable"/></w:font><w:font w:name="Symbol"><w:panose1 w:val="05050102010706020507"/>'
        '<w:charset w:val="02"/><w:family w:val="roman"/><w:pitch w:val="variable"/></w:font><w:font w:name="Calibri Light">'
        '<w:panose1 w:val="020F0302020204030204"/><w:charset w:val="00"/><w:family w:val="swiss"/>'
        '<w:pitch w:val="variable"/></w:font></w:fonts>') % _W
    text = [t for _s, t in blocks]
    words = sum(len(t.split()) for t in text)
    chars = sum(len(t.replace(" ", "")) for t in text)
    spaced = sum(len(t) for t in text) + len(text) - 1
    lines = sum(max(1, -(-len(t) // 92)) for t in text)
    org = _x(C.ORG)
    core_xml = _HEAD + (
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        '<dc:title></dc:title><dc:subject></dc:subject><dc:creator>%s</dc:creator><cp:keywords></cp:keywords>'
        '<dc:description></dc:description><cp:lastModifiedBy>%s</cp:lastModifiedBy><cp:revision>%d</cp:revision>'
        '<dcterms:created xsi:type="dcterms:W3CDTF">%s</dcterms:created>'
        '<dcterms:modified xsi:type="dcterms:W3CDTF">%s</dcterms:modified></cp:coreProperties>') % (
        org, org, core["revision"], core["created"], core["modified"])
    app_xml = _HEAD + (
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Template>Normal.dotm'
        '</Template><TotalTime>%d</TotalTime><Pages>%d</Pages><Words>%d</Words><Characters>%d</Characters>'
        '<Application>Microsoft Office Word</Application><DocSecurity>0</DocSecurity><Lines>%d</Lines>'
        '<Paragraphs>%d</Paragraphs><ScaleCrop>false</ScaleCrop><Company>%s</Company><LinksUpToDate>false'
        '</LinksUpToDate><CharactersWithSpaces>%d</CharactersWithSpaces><SharedDoc>false</SharedDoc>'
        '<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0000</AppVersion></Properties>') % (
        app["total_time"], app["pages"], words, chars, lines, len(text), org, spaced)
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
        'theme+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+'
        'xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.'
        'extended-properties+xml"/></Types>')
    return [("[Content_Types].xml", types), ("_rels/.rels", rels), ("word/document.xml", document),
            ("word/_rels/document.xml.rels", doc_rels), ("word/theme/theme1.xml", _theme()),
            ("word/numbering.xml", numbering), ("word/settings.xml", settings), ("word/styles.xml", styles),
            ("word/webSettings.xml", web), ("word/fontTable.xml", fonts), ("docProps/core.xml", core_xml),
            ("docProps/app.xml", app_xml)]


def terms_of_reference(path):
    """The committee's terms of reference as the Unit keeps them: approved in November 2025, last saved when the
    2027 meeting dates were entered."""
    import zipfile
    os.makedirs(os.path.dirname(path), exist_ok=True)
    core = {"revision": 9, "created": "2025-10-02T17:12:00Z", "modified": TOR_SAVED}
    parts = _docx_parts(TOR, core, {"total_time": 64, "pages": 1})
    saved = dt.datetime.strptime(TOR_SAVED, "%Y-%m-%dT%H:%M:%SZ")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in parts:
            # every member carries the save's own time, the clock the property part records
            zi = zipfile.ZipInfo(name, date_time=saved.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.create_system = 0
            zf.writestr(zi, data.encode("utf-8"))


def write_all(target):
    import pack
    programme(os.path.join(target, pack.P_PROG))
    terms_of_reference(os.path.join(target, pack.P_TOR))
