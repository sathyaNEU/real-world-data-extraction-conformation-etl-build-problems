"""The governing and context documents (DOCX through python-docx, PDF through reportlab), scrubbed of toolchain marks."""
import io, os, re, zipfile
from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import docx
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

FONT_DIR = '/usr/share/fonts/truetype/crosextra'
pdfmetrics.registerFont(TTFont('Carlito', os.path.join(FONT_DIR, 'Carlito-Regular.ttf')))
pdfmetrics.registerFont(TTFont('Carlito-Bold', os.path.join(FONT_DIR, 'Carlito-Bold.ttf')))
WORD = 'Microsoft\xae Word for Microsoft 365'
ORG = 'Norvale Electric Cooperative'
ST = dict(
    title=ParagraphStyle('t', fontName='Carlito-Bold', fontSize=14, leading=18, spaceAfter=4),
    sub=ParagraphStyle('s', fontName='Carlito', fontSize=9.5, leading=12, textColor=colors.HexColor('#444444'), spaceAfter=10),
    h=ParagraphStyle('h', fontName='Carlito-Bold', fontSize=11, leading=14, spaceBefore=8, spaceAfter=3),
    p=ParagraphStyle('p', fontName='Carlito', fontSize=10.5, leading=14, spaceAfter=5))
APP_XML = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Properties xmlns="http://schemas.openxmlformats.org/'
           'officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
           '<Template>Normal.dotm</Template><TotalTime>%d</TotalTime><Pages>%d</Pages><Words>%d</Words><Characters>%d</Characters>'
           '<Application>Microsoft Office Word</Application><DocSecurity>0</DocSecurity><Lines>%d</Lines><Paragraphs>%d</Paragraphs>'
           '<ScaleCrop>false</ScaleCrop><Company>%s</Company><LinksUpToDate>false</LinksUpToDate><CharactersWithSpaces>%d</CharactersWithSpaces>'
           '<SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0000</AppVersion></Properties>')


def scrub_docx(path, author, stamp, created):
    src = zipfile.ZipFile(path)
    items = [(i.filename, src.read(i.filename)) for i in src.infolist()]
    src.close()
    body = [d for n, d in items if n == 'word/document.xml'][0]
    words = len(re.sub(rb'<[^>]+>', b' ', body).split())
    out = []
    for name, data in items:
        if name in ('word/stylesWithEffects.xml', 'docProps/thumbnail.jpeg'):
            continue
        if name == 'docProps/app.xml':
            data = (APP_XML % (31, max(1, words // 420), words, words * 6, words // 11, 21, ORG, words * 7)).encode()
        if name == 'docProps/core.xml':
            data = re.sub(rb'(<dc:creator[^>]*>)[^<]*', rb'\g<1>' + author.encode(), data)
            data = re.sub(rb'(<cp:lastModifiedBy[^>]*>)[^<]*', rb'\g<1>' + author.encode(), data)
            data = re.sub(rb'(<dcterms:created[^>]*>)[^<]*', rb'\g<1>' + created.encode(), data)
            data = re.sub(rb'(<dcterms:modified[^>]*>)[^<]*', rb'\g<1>' + created.encode(), data)
            data = re.sub(rb'<cp:revision>[^<]*</cp:revision>', b'<cp:revision>4</cp:revision>', data)
            data = re.sub(rb'<dc:description>[^<]*</dc:description>|<dc:description/>', b'', data)
            data = re.sub(rb'<cp:keywords>[^<]*</cp:keywords>|<cp:keywords/>', b'', data)
            data = re.sub(rb'<dc:subject>[^<]*</dc:subject>|<dc:subject/>', b'', data)
            data = re.sub(rb'<cp:category>[^<]*</cp:category>|<cp:category/>', b'', data)
            data = re.sub(rb'(<dc:title>)[^<]*(</dc:title>)|<dc:title/>', b'', data)
        if name in ('[Content_Types].xml', 'word/_rels/document.xml.rels', '_rels/.rels'):
            data = re.sub(rb'<(Override|Relationship)[^>]*(stylesWithEffects|thumbnail)[^>]*/>', b'', data)
            data = re.sub(rb'<Default Extension="jpeg"[^>]*/>', b'', data)
        out.append((name, data))
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in out:
            zi = zipfile.ZipInfo(name, date_time=stamp); zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)


def scrub_xlsx(path, author, created, modified, stamp):
    src = zipfile.ZipFile(path)
    items = [(i.filename, src.read(i.filename)) for i in src.infolist()]
    src.close()
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in items:
            if name == 'docProps/core.xml':
                data = re.sub(rb'(<dc:creator[^>]*>)[^<]*', rb'\g<1>' + author.encode(), data)
                data = re.sub(rb'(<cp:lastModifiedBy[^>]*>)[^<]*', rb'\g<1>' + author.encode(), data)
                data = re.sub(rb'(<dcterms:created[^>]*>)[^<]*', rb'\g<1>' + created.encode(), data)
                data = re.sub(rb'(<dcterms:modified[^>]*>)[^<]*', rb'\g<1>' + modified.encode(), data)
            if name == 'docProps/app.xml':
                data = re.sub(rb'<Application>[^<]*</Application>', b'<Application>Microsoft Excel</Application>', data)
                data = re.sub(rb'<AppVersion>[^<]*</AppVersion>', b'<AppVersion>16.0300</AppVersion>', data)
                data = re.sub(rb'<Company>[^<]*</Company>', b'<Company>' + ORG.encode() + b'</Company>', data)
            zi = zipfile.ZipInfo(name, date_time=stamp); zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)


def _docx(path, blocks, author, stamp, created):
    d = docx.Document()
    st = d.styles['Normal']; st.font.name = 'Calibri'; st.font.size = Pt(11)
    for kind, val in blocks:
        if kind == 'title':
            p = d.add_paragraph(); r = p.add_run(val); r.bold = True; r.font.size = Pt(15)
        elif kind == 'sub':
            p = d.add_paragraph(); r = p.add_run(val); r.font.size = Pt(9.5)
        elif kind == 'h':
            p = d.add_paragraph(); r = p.add_run(val); r.bold = True; r.font.size = Pt(12)
        elif kind == 'p':
            d.add_paragraph(val)
        elif kind == 'table':
            t = d.add_table(rows=len(val), cols=len(val[0])); t.style = 'Table Grid'
            for i, row in enumerate(val):
                for j, c in enumerate(row):
                    cell = t.cell(i, j); cell.text = str(c)
                    if i == 0:
                        for r in cell.paragraphs[0].runs:
                            r.bold = True
    d.core_properties.author = author
    d.save(path)
    scrub_docx(path, author, stamp, created)


def _pdf(path, title, author, flow, issued):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=LETTER, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=20 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=WORD, producer=WORD)
    doc.build(flow)
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import NameObject, TextStringObject, DictionaryObject
    r = PdfReader(io.BytesIO(buf.getvalue())); w = PdfWriter()
    for pg in r.pages:
        w.add_page(pg)
    info = DictionaryObject({NameObject('/Title'): TextStringObject(title), NameObject('/Author'): TextStringObject(author),
                             NameObject('/Creator'): TextStringObject(WORD), NameObject('/Producer'): TextStringObject(WORD),
                             NameObject('/CreationDate'): TextStringObject('D:' + issued), NameObject('/ModDate'): TextStringObject('D:' + issued)})
    w._info = w._add_object(info)
    b2 = io.BytesIO(); w.write(b2)
    open(path, 'wb').write(b2.getvalue())


def _tbl(rows, widths):
    t = Table(rows, colWidths=widths)
    t.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), 'Carlito'), ('FONTSIZE', (0, 0), (-1, -1), 9.5),
                           ('FONTNAME', (0, 0), (-1, 0), 'Carlito-Bold'), ('LINEBELOW', (0, 0), (-1, 0), 0.6, colors.black),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
    return t


def policy(out):
    B = [('title', 'Board Policy 407: Reliability Work Plan'),
         ('sub', 'Norvale Electric Cooperative, Board of Trustees. Adopted 14 March 2019; last revised 11 February 2025 (resolution 2025-03).'),
         ('h', '1. Purpose'),
         ('p', 'Each November the Board of Trustees adopts a reliability work plan for the coming calendar year. The plan carries the '
               'routine programmes in the budget and funds one fix: work that undoes or answers one change made in the fiscal '
               'year just closed.'),
         ('h', '2. The annual reliability review'),
         ('p', 'Reliability Engineering presents the review at the October meeting. It reports the indices for the fiscal '
               'year and lists the changes made during the year that bear on service to members, each with the date it took '
               'effect and what it applies to.'),
         ('h', '3. Costing a change'),
         ('p', '3.1 Each change in the review is costed in sustained customer interruptions: the customer interruptions in '
               'the fiscal year that would not have occurred without the change, everything else as it was.'),
         ('p', '3.2 Sustained customer interruptions are counted as the outage management system records them: each '
               'unplanned interruption record of five minutes or longer, with its customers interrupted. Interruptions on '
               'major event days are excluded, major event days being identified under IEEE Std 1366 from the daily SAIDI of '
               'the five fiscal years before the review year.'),
         ('p', '3.3 The fiscal year runs from 1 October to 30 September, on the Cooperative\'s local time.'),
         ('h', '4. The fix'),
         ('p', 'The plan funds a fix for the change with the largest cost. Where the largest cost is shared by two changes '
               'within 10 per cent of each other, the Board chooses between them.'),
         ('h', '5. Review of this policy'),
         ('p', 'This policy is reviewed every three years by the Governance Committee.'),
         ('sub', 'Lawrence Reed, Secretary to the Board of Trustees')]
    _docx(os.path.join(out, 'board_policy_407_reliability_work_plan.docx'), B, 'Lawrence Reed', (2025, 2, 12, 9, 4, 0), '2025-02-12T15:04:00Z')


def review(out, idx, members):
    rows = [['Fiscal year', 'Members served (average)', 'SAIFI', 'SAIDI (min)', 'CAIDI (min)', 'Major event days']] + idx
    ch = [['Change', 'In place', 'Applies to', 'Recorded by'],
          ['Load study waived for heat pumps connected under the air-source heat pump rebate', '1 Nov 2025',
           'Services connected under the rebate from that date', 'Member Services'],
          ['Restoration switching template SO-7 revised to shorten restoration times', '1 Dec 2025',
           'All restorations switched by the control centre', 'System Operations'],
          ['Pre-winter riser termination replacements suspended; the 2025 list not worked', '1 Oct 2025',
           'Risers on the 2025 replacement list', 'Operations'],
          ['Animal guard programme ended; the 2026 site list not fitted', '1 Jan 2026', 'Sites on the 2026 list', 'Operations'],
          ['Pole-top transformer supply moved to Brekke Power Products', '1 Feb 2026',
           'Transformer units fitted from that date', 'Purchasing']]
    B = [('title', 'Reliability Review, Fiscal 2026'),
         ('sub', 'Reliability Engineering, for the Board of Trustees meeting of 27 October 2026. Prepared by Kayla Dean.'),
         ('h', '1. Indices'),
         ('p', 'Indices are for unplanned sustained interruptions with major event days excluded (IEEE Std 1366), per member '
               'on the average number of members served in each fiscal year. The system register counted %s members at '
               '30 September 2026.' % format(members, ',')),
         ('table', rows),
         ('p', 'District scorecards carry momentary interruption events per member (MAIFIe as IEEE Std 1366 defines it), '
               'all days included, alongside the sustained indices.'),
         ('h', '2. Changes in fiscal 2026'),
         ('p', 'The following changes took effect during the year. They are listed for costing under Board Policy 407.'),
         ('table', ch),
         ('h', '3. Next steps'),
         ('p', 'Each change is to be costed under section 3 of the policy for the November meeting, where the Board adopts '
               'the 2027 work plan and its one fix.'),
         ]
    _docx(os.path.join(out, 'reliability_review_fy2026.docx'), B, 'Kayla Dean', (2026, 10, 21, 16, 12, 0), '2026-10-21T21:12:00Z')


def rebate_terms(out):
    B = [('title', 'Air-Source Heat Pump Rebate: Terms and Connection, 2025-26'),
         ('sub', 'Norvale Electric Cooperative, Member Services. Effective 1 October 2025; amended 1 November 2025.'),
         ('h', 'Who can apply'),
         ('p', 'Members whose home is heated mainly by electric resistance heat (baseboard, electric furnace or electric '
               'boiler) on the Cooperative\'s system. The heat pump becomes the home\'s main heat; the existing resistance '
               'heat may stay as backup.'),
         ('h', 'Equipment and rebate'),
         ('p', 'Cold-climate air-source heat pumps listed by AHRI, 1.5 to 5 tons, installed by a participating contractor. '
               'The rebate is 400 dollars a ton, paid on the member\'s bill after the contractor\'s completion form is received.'),
         ('h', 'Connection'),
         ('p', 'Before a heat pump is connected, Engineering completes a load study: it checks the service transformer and '
               'the secondary conductor serving the member against the added load, and replaces either where the load '
               'requires it. The study reference is recorded on the rebate.'),
         ('p', 'From 1 November 2025, heat pumps connected under this rebate are connected without a load study.'),
         ('h', 'Contact'),
         ('p', 'Member Services, weekdays 7:30 to 4:30.')]
    _docx(os.path.join(out, 'heat_pump_rebate_terms_2025-26.docx'), B, 'Member Services', (2025, 10, 30, 11, 20, 0), '2025-10-30T16:20:00Z')


def agreement(out, classes, holidays):
    fl = [Paragraph('Labor Agreement 2024 to 2027: Articles 14 and 18 and Wage Schedule A (extract)', ST['title']),
          Paragraph('Between Norvale Electric Cooperative and its represented line and operations employees. Rates in '
                    'Schedule A apply from 1 October 2025 to 30 September 2026.', ST['sub']),
          Paragraph('Article 14. Callout', ST['h']),
          Paragraph('14.1 An employee called out to work outside the employee\'s scheduled hours is paid at time and one-half '
                    'for the hours worked, with a minimum of two hours\' pay at time and one-half for each callout.', ST['p']),
          Paragraph('14.2 A callout runs from the start of work until the employee is released from the last job of the '
                    'callout, travel between jobs included.', ST['p']),
          Paragraph('14.3 Callout hours worked on a holiday listed in Article 18 are paid at double time.', ST['p']),
          Paragraph('14.4 The crew foreman enters each crew member\'s callout time in the timekeeping system each Monday for '
                    'the week before, against the work order of each job. A correction is entered as a new entry for the '
                    'same job and, once the foreman approves it, replaces the earlier entry. Callout time is paid on the '
                    'entries the foreman approves; an entry the foreman rejects is not paid.', ST['p']),
          Paragraph('Article 18. Holidays, fiscal 2026', ST['h']),
          _tbl([['Holiday', 'Date']] + [[n, d] for n, d in holidays], [95 * mm, 45 * mm]),
          Spacer(1, 6),
          Paragraph('Wage Schedule A, hourly base rates', ST['h']),
          _tbl([['Classification', 'Base rate (USD per hour)']] + [[k, '%.2f' % v] for k, v in classes.items()], [95 * mm, 45 * mm])]
    _pdf(os.path.join(out, 'labor_agreement_2024-2027_extract.pdf'), 'Labor Agreement 2024-2027 extract', 'Human Resources', fl,
         "20251006091500-05'00'")
