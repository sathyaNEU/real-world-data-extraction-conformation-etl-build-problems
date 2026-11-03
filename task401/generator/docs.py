"""task401: the governing and context documents (PDF through reportlab, DOCX through python-docx), scrubbed."""
import io, os, re, zipfile
from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

FONT_DIR = '/usr/share/fonts/truetype/crosextra'
pdfmetrics.registerFont(TTFont('Carlito', os.path.join(FONT_DIR, 'Carlito-Regular.ttf')))
pdfmetrics.registerFont(TTFont('Carlito-Bold', os.path.join(FONT_DIR, 'Carlito-Bold.ttf')))
WORD = 'Microsoft\xae Word for Microsoft 365'
ORG = 'Ferncastle Energy Supply Ltd'

S = dict(
    title=ParagraphStyle('t', fontName='Carlito-Bold', fontSize=15, leading=19, spaceAfter=4),
    sub=ParagraphStyle('s', fontName='Carlito', fontSize=9.5, leading=12, textColor=colors.HexColor('#444444'), spaceAfter=10),
    h=ParagraphStyle('h', fontName='Carlito-Bold', fontSize=11.5, leading=15, spaceBefore=8, spaceAfter=3),
    p=ParagraphStyle('p', fontName='Carlito', fontSize=10.5, leading=14, spaceAfter=5),
    small=ParagraphStyle('m', fontName='Carlito', fontSize=8.5, leading=11, textColor=colors.HexColor('#555555')))


def _pdf(path, title, author, flow):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=20 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=WORD, producer=WORD)
    doc.build(flow)
    data = buf.getvalue()
    # rebuild the info dictionary: the producing application, the issue date, no empty or default entries
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import NameObject, TextStringObject, DictionaryObject
    r = PdfReader(io.BytesIO(data)); w = PdfWriter()
    for pg in r.pages:
        w.add_page(pg)
    stamp = 'D:%s' % ISSUED[os.path.basename(path)]
    info = DictionaryObject({NameObject('/Title'): TextStringObject(title), NameObject('/Author'): TextStringObject(author),
                             NameObject('/Creator'): TextStringObject(WORD), NameObject('/Producer'): TextStringObject(WORD),
                             NameObject('/CreationDate'): TextStringObject(stamp), NameObject('/ModDate'): TextStringObject(stamp)})
    w._info = w._add_object(info)
    b2 = io.BytesIO(); w.write(b2)
    open(path, 'wb').write(b2.getvalue())


ISSUED = {'six_month_survey_measurement_framework_v2.1.pdf': "20260114101500Z",
          'billing_platform_phase1_closeout_report.pdf': "20260109142200Z"}


def _table(rows, widths):
    t = Table(rows, colWidths=widths)
    t.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), 'Carlito'), ('FONTSIZE', (0, 0), (-1, -1), 9.5),
                           ('FONTNAME', (0, 0), (-1, 0), 'Carlito-Bold'), ('LINEBELOW', (0, 0), (-1, 0), 0.6, colors.black),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
    return t


def framework(out):
    P = lambda s, st='p': Paragraph(s, S[st])
    flow = [P('Six-month customer survey: measurement framework', 'title'),
            P('%s, Customer Insight. Version 2.1, approved 14 January 2026 by the Customer Experience Committee. '
              'Owner: Head of Customer Insight. Replaces version 1.4 (March 2024).' % ORG, 'sub'),
            P('1. What the survey is for', 'h'),
            P('We ask every new customer how they feel about us six months after their supply starts. The survey is the '
              'measure the Customer Experience Committee and the executive team use for new customers, and the measure '
              'reported in the monthly customer dashboard.'),
            P('2. Who is asked and when', 'h'),
            P('An invitation goes by email (by text message where we hold no email address) to the account holder of every '
              'Direct Debit account whose supply started six months earlier, in the week that anniversary falls. One '
              'reminder follows after seven days. Customers who have left us before the invitation date are not asked.'),
            P('3. The measure', 'h'),
            P('The population for a half-year is the customers who answered the overall question in a response received '
              'from 1 January to 30 June, or from 1 July to 31 December, UK time. A response counts when the overall '
              'question is answered; a survey started and left before that question is not a response.'),
            P('The measure is the share of those customers who answer 4 or 5 to the overall question, "Overall, how '
              'satisfied are you with %s?", on its five-point scale. Each account counts once in a half-year: where an '
              'account holder answers twice, the first answered response is the one that counts.' % ORG.replace(' Supply Ltd', '')),
            P('The share is reported unweighted, in per cent to one decimal. A movement between two half-years is the '
              'difference between their shares in percentage points; a review of a movement explains that difference.'),
            P('4. The scale', 'h'),
            P('From January 2026 the survey runs on a new vendor platform, whose export gives the overall answer as its '
              'label. The labels map to the scale as follows.'),
            _table([['Scale point', 'Label in the 2026 export'], ['5', 'Very satisfied'], ['4', 'Fairly satisfied'],
                    ['3', 'Neither satisfied nor dissatisfied'], ['2', 'Fairly dissatisfied'], ['1', 'Very dissatisfied']],
                   [30 * mm, 90 * mm]),
            Spacer(1, 6),
            P('The attribute questions (billing accuracy, bill clarity, value for money, ease of contact, resolution and the '
              'app) and the likelihood-to-recommend question are unchanged between the two vendors.'),
            P('5. Reporting and review', 'h'),
            P('Customer Insight publishes the half-year share in the second week after the half-year closes. A movement of '
              'two points or more between consecutive half-years is reviewed for the Customer Experience Committee.'),
            Spacer(1, 10),
            P('Document reference CI-FW-006. Next review January 2027.', 'small')]
    _pdf(os.path.join(out, 'six_month_survey_measurement_framework_v2.1.pdf'),
         'Six-month customer survey: measurement framework', 'Customer Insight', flow)


def closeout(out):
    P = lambda s, st='p': Paragraph(s, S[st])
    flow = [P('Billing platform programme: phase 1 close-out report', 'title'),
            P('%s, Billing Transformation. Issued 9 January 2026. Programme director\'s report to the Programme Board. '
              'Covers phase 1 delivery against plan and its defect log; it does not assess customer outcomes.' % ORG, 'sub'),
            P('1. Scope delivered', 'h'),
            P('Phase 1 moved the Direct Debit and credit accounts from the legacy billing platform to the new platform in '
              'nine weekly load batches from 1 September to 2 November 2025, as planned in October 2024. New customers '
              'have been set up on the new platform from 1 September 2025. Prepayment accounts remain on the legacy '
              'platform for phase 2.'),
            P('Loads ran overnight. An account that failed post-load validation was loaded again in a later run once its '
              'data was corrected; the platform issues a new account number on each load.'),
            P('2. Defects and their status at close', 'h'),
            _table([['Ref', 'Defect', 'Raised', 'Status'],
                    ['BT-118', 'Bills issued on estimated reads where a customer read was received within two days of the bill run', '22 Sep 2025', 'Fixed 31 Oct 2025'],
                    ['BT-131', 'Bill layout: standing charge shown per month rather than per day', '29 Sep 2025', 'Fixed 17 Nov 2025'],
                    ['BT-142', 'Payment reminder letters sent to accounts already in credit', '13 Oct 2025', 'Fixed 3 Nov 2025'],
                    ['BT-157', 'App login loop for accounts loaded twice', '27 Oct 2025', 'Fixed 21 Nov 2025'],
                    ['BT-163', 'Direct Debit collection date moved for a small number of accounts loaded near month end', '4 Nov 2025', 'Fixed 12 Dec 2025']],
                   [16 * mm, 92 * mm, 26 * mm, 32 * mm]),
            Spacer(1, 6),
            P('Bills on estimated reads ran above their usual level for about six weeks from late September (BT-118) and '
              'were back to their usual level by mid-November. Complaints about bill layout eased after BT-131.'),
            P('3. Lessons for phase 2', 'h'),
            P('Run validation before the load rather than after it, so that an account is loaded once. Publish the bill '
              'layout change to customers before the first bill. Keep the legacy platform\'s account status in step with '
              'the industry switching flows for accounts that leave during the migration window.'),
            Spacer(1, 10),
            P('Document reference BT-CR-011, version 1.0.', 'small')]
    _pdf(os.path.join(out, 'billing_platform_phase1_closeout_report.pdf'),
         'Billing platform programme: phase 1 close-out report', 'Billing Transformation', flow)


def cutover_plan(out):
    import docx
    from docx.shared import Pt
    d = docx.Document()
    st = d.styles['Normal']; st.font.name = 'Calibri'; st.font.size = Pt(10.5)
    d.add_heading('Billing platform programme: phase 2 cutover plan', level=1)
    d.add_paragraph('%s, Billing Transformation. Version 1.3, 20 October 2026, for the executive team. '
                    'Owner: Billing Programme Director.' % ORG)
    d.add_heading('1. Scope', level=2)
    d.add_paragraph('Phase 2 moves every prepayment account on the legacy platform that we still supply on 1 November '
                    '2026, on at least one of its meter points, to the new platform. An account we no longer supply on '
                    'any meter point on that date stays on the legacy platform until its final bill and closes there.')
    d.add_paragraph('Planning volumes use each meter point\'s industry annual quantity in force on 1 November 2026, '
                    'electricity and gas reported separately, for the meter points we still supply on that date.')
    d.add_heading('2. Timetable', level=2)
    for line in ('Code freeze on the legacy prepayment module: 16 November 2026.',
                 'Dress rehearsal on a copy of the legacy database: 30 November to 6 December 2026.',
                 'Go or no-go at the executive team meeting on 11 December 2026.',
                 'Load window: 1 to 28 February 2027, in four weekly batches.'):
        d.add_paragraph(line, style='List Bullet')
    d.add_heading('3. Reporting conventions', level=2)
    d.add_paragraph('Weekly figures in this plan and in its reports run Monday to Sunday, UK time.')
    d.add_paragraph('Phase 1 is reported as the accounts loaded in each week, each account counted once, in the week its '
                    'last load completed.')
    d.add_heading('4. Dependencies', level=2)
    d.add_paragraph('Prepayment key and card top-up feeds from the payment network to be repointed at the new platform. '
                    'Smart prepayment meters to receive new tariff tables over the air in the load window. The vulnerable '
                    'customer register to be reconciled between platforms before the dress rehearsal.')
    cp = d.core_properties
    import datetime as dt
    cp.author = 'Elliot Davies'; cp.last_modified_by = 'Elliot Davies'
    cp.created = dt.datetime(2026, 10, 14, 9, 12, 0); cp.modified = dt.datetime(2026, 10, 20, 16, 41, 0)
    cp.revision = 7; cp.title = 'Phase 2 cutover plan'; cp.subject = ''; cp.keywords = ''; cp.comments = ''
    cp.category = ''
    path = os.path.join(out, 'phase2_cutover_plan_v1.3.docx')
    d.save(path)
    scrub_docx(path, words=410, pages=2)


APP_XML = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Properties xmlns="http://schemas.openxmlformats.org/'
           'officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/'
           'docPropsVTypes"><Template>Normal.dotm</Template><TotalTime>%d</TotalTime><Pages>%d</Pages><Words>%d</Words>'
           '<Characters>%d</Characters><Application>Microsoft Office Word</Application><DocSecurity>0</DocSecurity>'
           '<Lines>%d</Lines><Paragraphs>%d</Paragraphs><ScaleCrop>false</ScaleCrop><Company>%s</Company>'
           '<LinksUpToDate>false</LinksUpToDate><CharactersWithSpaces>%d</CharactersWithSpaces><SharedDoc>false</SharedDoc>'
           '<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0000</AppVersion></Properties>')


def scrub_docx(path, words, pages):
    src = zipfile.ZipFile(path)
    items = [(i, src.read(i.filename)) for i in src.infolist()]
    src.close()
    out = []
    for info, data in items:
        name = info.filename
        if name == 'word/stylesWithEffects.xml':
            continue
        if name == 'docProps/app.xml':
            data = (APP_XML % (38, pages, words, words * 6, words // 11, 19, ORG, words * 7)).encode()
        if name in ('[Content_Types].xml', 'word/_rels/document.xml.rels'):
            data = re.sub(rb'<(Override|Relationship)[^>]*stylesWithEffects[^>]*/>', b'', data)
        if name == 'docProps/thumbnail.jpeg':
            continue
        out.append((name, data))
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in out:
            zi = zipfile.ZipInfo(name, date_time=(2026, 10, 20, 16, 41, 0)); zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)


def scrub_xlsx(path, author, created, modified):
    src = zipfile.ZipFile(path)
    items = [(i.filename, src.read(i.filename)) for i in src.infolist()]
    src.close()
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in items:
            if name == 'docProps/core.xml':
                data = re.sub(rb'<dc:creator>[^<]*</dc:creator>', ('<dc:creator>%s</dc:creator>' % author).encode(), data)
                data = re.sub(rb'<cp:lastModifiedBy>[^<]*</cp:lastModifiedBy>', ('<cp:lastModifiedBy>%s</cp:lastModifiedBy>' % author).encode(), data)
                data = re.sub(rb'(<dcterms:created[^>]*>)[^<]*', rb'\g<1>' + created.encode(), data)
                data = re.sub(rb'(<dcterms:modified[^>]*>)[^<]*', rb'\g<1>' + modified.encode(), data)
            if name == 'docProps/app.xml':
                data = re.sub(rb'<Application>[^<]*</Application>', b'<Application>Microsoft Excel</Application>', data)
                data = re.sub(rb'<AppVersion>[^<]*</AppVersion>', b'<AppVersion>16.0300</AppVersion>', data)
            zi = zipfile.ZipInfo(name, date_time=(2026, 10, 30, 11, 5, 0)); zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)


def write_all(out):
    framework(out); closeout(out); cutover_plan(out)
    scrub_xlsx(os.path.join(out, 'tariff_rates_2024-04_2026-06.xlsx'), 'Pricing Team', '2024-04-02T08:30:00Z', '2026-06-24T15:12:00Z')
