"""task210 documents in their issuers' own forms: the decision notice's conditions, the noise management plan, the
draft January working scheme, the plant register, the network operator's interruption notices, and the workbooks."""
import calendar
import datetime as dt
import io
import os
import re
import zipfile
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import world as W

MANAGER, OFFICER, CONSULTANT = 'Garry Fry', 'Maurice Russell', 'Leanne Smith'


# ------------------------------------------------------------------------------------------------ writers, scrubbing

def pdf(path, title, author, producer, stamp, story_fn, footer):
    def deco(c, d):
        c._doc.info.producer = producer
        c._doc.info.creator = producer
        c._doc.info.author = author
        c._doc.info.title = title
        c._doc.info.subject = ''
        c.setFont('Helvetica', 7.2)
        c.drawString(18 * mm, 10 * mm, footer)
        c.drawRightString(192 * mm, 10 * mm, 'Page %d' % c.getPageNumber())
    doc = SimpleDocTemplate(path, pagesize=A4, invariant=1, leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=17 * mm, bottomMargin=18 * mm)
    old = os.environ.get('SOURCE_DATE_EPOCH')
    os.environ['SOURCE_DATE_EPOCH'] = str(calendar.timegm(stamp))
    try:
        doc.build(story_fn(), onFirstPage=deco, onLaterPages=deco)
    finally:
        if old is None:
            del os.environ['SOURCE_DATE_EPOCH']
        else:
            os.environ['SOURCE_DATE_EPOCH'] = old
    raw = open(path, 'rb').read()
    out = re.sub(rb'(%[^\n]*?)( ?ReportLab[^\n]*)', lambda m: m.group(1) + b' ' * len(m.group(2)), raw)
    for tag in (rb'/Trapped /False', rb'/Keywords ()', rb'/Subject ()', rb'/Subject (\(unspecified\))'):
        out = out.replace(tag, b' ' * len(tag))
    assert len(out) == len(raw) and b'ReportLab' not in out
    open(path, 'wb').write(out)


def st():
    ss = getSampleStyleSheet()
    body = ParagraphStyle('b', parent=ss['BodyText'], fontName='Helvetica', fontSize=9.4, leading=12.4, spaceAfter=4.5)
    h = ParagraphStyle('h', parent=ss['Heading2'], fontName='Helvetica-Bold', fontSize=10.6, spaceBefore=7, spaceAfter=3)
    t = ParagraphStyle('t', parent=ss['Title'], fontName='Helvetica-Bold', fontSize=13.5, alignment=0, spaceAfter=3)
    small = ParagraphStyle('s', parent=body, fontSize=8.0, leading=10.2, textColor=colors.HexColor('#333333'))
    return body, h, t, small


def tstyle(head_bg='#E6E6E6'):
    return TableStyle([('FONT', (0, 0), (-1, -1), 'Helvetica', 7.8), ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 7.8),
                       ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(head_bg)),
                       ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#999999')),
                       ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 3),
                       ('RIGHTPADDING', (0, 0), (-1, -1), 3)])


def stamp(y, m, d, hh=9, mi=0):
    return (y, m, d, hh, mi, 0, 0, 1, 0)


def office_scrub(path, kind, creator, company, stamp_iso, title=''):
    """Rewrite an openpyxl or python-docx package's docProps to its issuer and fixed dates, zip entries in order."""
    src = open(path, 'rb').read()
    zin = zipfile.ZipFile(io.BytesIO(src))
    out = io.BytesIO()
    app = 'Microsoft Excel' if kind == 'xlsx' else 'Microsoft Office Word'
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == 'docProps/core.xml':
                data = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
                        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
                        'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
                        '<dc:title>%s</dc:title><dc:creator>%s</dc:creator><cp:lastModifiedBy>%s</cp:lastModifiedBy>'
                        '<cp:revision>3</cp:revision>'
                        '<dcterms:created xsi:type="dcterms:W3CDTF">%s</dcterms:created>'
                        '<dcterms:modified xsi:type="dcterms:W3CDTF">%s</dcterms:modified></cp:coreProperties>'
                        % (title, creator, creator, stamp_iso.split('|')[0], stamp_iso.split('|')[-1])).encode()
            elif info.filename == 'docProps/app.xml':
                data = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
                        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
                        '<Application>%s</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>'
                        '<Company>%s</Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
                        '<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>'
                        % (app, company)).encode()
            zi = zipfile.ZipInfo(info.filename, date_time=(2026, 11, 27, 9, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = info.external_attr
            zout.writestr(zi, data)
    open(path, 'wb').write(out.getvalue())


def xlsx(path, sheets, creator, company, stamp_iso, title, widths=None):
    wb = Workbook()
    first = True
    for name, header, rows in sheets:
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = name
        ws.append(header)
        for c in ws[1]:
            c.font = Font(bold=True)
        for r in rows:
            ws.append(list(r))
        for i, w in enumerate((widths or {}).get(name, [])):
            ws.column_dimensions[chr(65 + i)].width = w
    wb.save(path)
    office_scrub(path, 'xlsx', creator, company, stamp_iso, title)


# ------------------------------------------------------------------------------------------------ the conditions

def conditions(path):
    body, h, t, small = st()
    def story():
        s = [Paragraph('Holmeshire County Council', small), Paragraph('Town and Country Planning Act 1990', small),
             Paragraph('Decision notice R/2019/0447: Ravensby Quarry, Ulverthorpe', t),
             Paragraph('Continuation of limestone extraction with lateral extension (Phases 3 and 4), processing and '
                       'restoration. Applicant: Calderwick Stone Ltd. Permission granted 14 November 2019 subject to the '
                       'conditions below (extract: conditions 9 to 22).', body)]
        conds = [
            ('9', 'Hours.', 'No extraction, haulage or processing shall take place outside 07:00 to 17:00 Monday to '
                  'Friday and 07:00 to 12:00 on Saturdays, save for maintenance of plant and the operations permitted by '
                  'condition 12. No operations shall take place on Sundays or Bank Holidays.'),
            ('12', 'Processing hours.', 'The processing plant may operate from 06:30 to 18:30 Monday to Friday.'),
            ('14', 'Blasting.', 'Blasting shall take place only between 10:00 and 16:00 Monday to Friday, and ground '
                   'vibration at any dwelling shall not exceed a peak particle velocity of 6 mm/s in 95 per cent of '
                   'blasts measured over any six-month period, no blast exceeding 12 mm/s.'),
            ('16', 'Temporary operations.', 'Soil stripping, bund formation and removal may be carried out for up to eight '
                   'weeks in any calendar year, during which the specific sound level at monitoring location MP1 shall not '
                   'exceed 70 dB LAeq,1h (free field). The operator shall notify the Mineral Planning Authority five working '
                   'days before temporary operations begin.'),
            ('17', 'Noise.', 'Except during temporary operations under condition 16, the specific sound level from '
                   'operations at the site shall not exceed 45 dB LAeq,1h (free field) at monitoring location MP1 '
                   '(Ulverthorpe Lane) between 07:00 and 19:00 Monday to Friday, and 42 dB LAeq,1h (free field) at all other '
                   'times.'),
            ('18', 'Noise monitoring.', 'Noise shall be monitored continuously at MP1 in accordance with the noise '
                   'management plan approved under this condition, and the results reported to the Mineral Planning '
                   'Authority quarterly.'),
            ('19', 'Working schemes.', 'No extraction shall take place in Phase 4 except in accordance with a working scheme '
                   'for each calendar month, submitted to the Mineral Planning Authority by the 10th day of the preceding '
                   'month, stating the haul road to be used, the haulage hours and the number of dump trucks allocated to '
                   'that haul road.'),
            ('21', 'Vehicle movements.', 'The number of heavy goods vehicles leaving the site shall not exceed 140 in any '
                   'day; a record of departures shall be kept and made available on request.'),
            ('22', 'Dust.', 'Haul roads shall be maintained and watered as necessary so that no visible dust crosses the '
                   'site boundary.'),
        ]
        rows = [['No.', 'Condition']] + [[a, Paragraph('<b>%s</b> %s' % (b, c), small)] for (a, b, c) in conds]
        tb = Table(rows, colWidths=[12 * mm, 160 * mm])
        tb.setStyle(tstyle())
        s += [Spacer(1, 4), tb, Spacer(1, 6),
              Paragraph('Monitoring location MP1 is the free-field position on the verge of Ulverthorpe Lane shown on '
                        'drawing RQ/19/22.', small),
              Paragraph('Signed on behalf of the Council: Head of Planning Services. Date: 14 November 2019.', small)]
        return s
    pdf(path, 'Decision notice R/2019/0447 conditions', 'Holmeshire County Council', 'Acrobat PDFMaker 19 for Word',
        stamp(2019, 11, 14), story, 'R/2019/0447  Ravensby Quarry')


# ----------------------------------------------------------------------------------------- noise management plan

def nmp(path, residual_db):
    body, h, t, small = st()
    def story():
        s = [Paragraph('Calderwick Stone Ltd, Ravensby Quarry', small),
             Paragraph('Noise management plan, revision 3', t),
             Paragraph('Approved by the Mineral Planning Authority under condition 18 of R/2019/0447 on 26 March 2026. '
                       'Prepared by %s, MIOA, for the operator. Supersedes revision 2 (June 2023).' % CONSULTANT, small),
             Paragraph('1. Purpose', h),
             Paragraph('This plan sets out how noise from Ravensby Quarry is monitored, apportioned between the site\'s '
                       'activities and controlled through the monthly working schemes, so that the limits of condition 17 '
                       'are met at the nearest dwellings in Ulverthorpe.', body),
             Paragraph('2. Receptors', h),
             Paragraph('The nearest dwellings are on Ulverthorpe Lane and Low Green, to the north-east of the processing '
                       'plant. Monitoring location MP1 on the Ulverthorpe Lane verge represents them.', body),
             Paragraph('3. Limits', h),
             Paragraph('Condition 17: 45 dB LAeq,1h (free field) at MP1 between 07:00 and 19:00 Monday to Friday, 42 dB '
                       'LAeq,1h at all other times, except during temporary operations under condition 16.', body),
             Paragraph('4. Monitoring', h),
             Paragraph('4.1 A Class 1 sound level meter with an outdoor microphone kit is installed at MP1, the microphone '
                       '1.5 m above ground, free field. It logs LAeq, LA90, LA10 and LAFmax over consecutive 15-minute '
                       'periods, each stamped at the end of its period on the logger\'s clock. The specific sound level of '
                       'an activity is the sound level at MP1 attributable to that activity over the reference period of '
                       'one hour.', body),
             Paragraph('4.2 The meter is field-checked with a calibrator at each battery change and laboratory-calibrated '
                       'every two years. Data are downloaded monthly and reported to the Mineral Planning Authority each '
                       'quarter.', body),
             Paragraph('5. Apportionment of the limit', h),
             Paragraph('5.1 Two activities contribute to the specific sound level at MP1 during the working day: the '
                       'processing plant and haulage on the site\'s haul roads.', body),
             Paragraph('5.2 The baseline survey of 2 and 3 March 2026 measured at MP1, with the site stopped, a residual '
                       'sound level of %.1f dB LAeq over 07:00 to 17:00, and from plant-only running the processing plant\'s '
                       'specific sound level of 37.5 dB LAeq,1h. Of the 45 dB limit at MP1, haulage on the site\'s haul '
                       'roads is held to 44.0 dB LAeq,1h.' % residual_db, body),
             Paragraph('6. Working schemes', h),
             Paragraph('6.1 Each monthly working scheme under condition 19 states the number of articulated dump trucks '
                       'allocated to the scheme\'s haul road and the loaded haul movements each truck makes in an hour on '
                       'it. The allocation is set so that the specific sound level of the scheme\'s haulage at MP1, at the '
                       'scheme\'s haul rate, is within the 44.0 dB share of paragraph 5.2.', body),
             Paragraph('6.2 A haul movement is one loaded trip from the working face to its tipping point and the '
                       'truck\'s empty return. The haul rate is the number of trucks allocated multiplied by the loaded '
                       'movements each truck makes in an hour.', body),
             Paragraph('6.3 Trucks are allocated in whole numbers. A scheme that cannot be held within the share at one '
                       'truck is not submitted.', body),
             Paragraph('7. Complaints', h),
             Paragraph('Complaints are logged on receipt with the caller\'s address and description, acknowledged within '
                       'two working days, and reviewed against the MP1 record for the period described.', body),
             Paragraph('8. Review', h),
             Paragraph('This plan is reviewed annually and whenever a new phase of extraction begins.', body)]
        return s
    pdf(path, 'Ravensby Quarry noise management plan rev 3', CONSULTANT, 'Microsoft Word for Microsoft 365',
        stamp(2026, 3, 26), story, 'Ravensby Quarry NMP rev 3, March 2026')


# ------------------------------------------------------------------------------------------- the working scheme

def scheme(path):
    from docx import Document
    from docx.shared import Pt
    doc = Document()
    stl = doc.styles['Normal']; stl.font.name = 'Calibri'; stl.font.size = Pt(10.5)
    doc.add_heading('Ravensby Quarry: Phase 4 working scheme, January 2027 (draft)', level=1)
    doc.add_paragraph('Condition 19 of R/2019/0447. For submission to Holmeshire County Council by 10 December 2026. '
                      'Prepared by %s, quarry manager. Draft of 27 November 2026.' % MANAGER)
    def table(rows):
        tb = doc.add_table(rows=1, cols=4)
        tb.style = 'Table Grid'
        for i, hd in enumerate(['Point', 'Latitude', 'Longitude', 'Level (m AOD)']):
            tb.rows[0].cells[i].text = hd
        for (lab, x, y, z) in rows:
            la, lo = W.to_latlon(x, y)
            row = tb.add_row().cells
            row[0].text = lab
            row[1].text = '%.6f' % la
            row[2].text = '%.6f' % lo
            row[3].text = '%.1f' % z
    doc.add_heading('1. Area worked', level=2)
    doc.add_paragraph('Extraction moves to the first bench of the Phase 4 extension, on the east side of the existing pit, '
                      'from Monday 4 January 2027. Bench 1 is worked at 46 m AOD. The existing faces are held for blasting '
                      'and stocking during the month. All loads from Phase 4 are hauled to the primary crusher feed hopper. '
                      'Bench 1 crest as set out:')
    table([('C-%d' % (i + 1), x, y, z) for i, (x, y, z) in enumerate(W.bench_crest())])
    doc.add_heading('2. Haul road', level=2)
    doc.add_paragraph('Loaded trucks climb out of the bench by its access ramp (R-1 to R-3) and run north-west on the Phase 4 '
                      'haul road (P4-1 to P4-6) to the primary crusher, returning empty by the same road. Alignment and '
                      'levels as surveyed for construction:')
    table([('R-%d' % (i + 1), x, y, z) for i, (x, y, z) in enumerate(W.ROADS['ext_up']['pts'][:-1])] +
          [('P4-%d' % (i + 1), x, y, z) for i, (x, y, z) in enumerate(W.ROADS['ext']['pts'])])
    doc.add_heading('3. Haulage', level=2)
    doc.add_paragraph('Haulage hours 07:00 to 17:00 Monday to Friday, with a half-hour break at 12:00. No haulage on '
                      'Friday 1 January 2027 (Bank Holiday).')
    doc.add_paragraph('Each articulated dump truck on the Phase 4 haul road completes 4.5 loaded movements an hour '
                      '(cycle measured on the bench trial of 18 November 2026).')
    doc.add_paragraph('Articulated dump trucks allocated to the Phase 4 haul road: [to be confirmed]')
    doc.add_heading('4. Other operations', level=2)
    doc.add_paragraph('The processing plant runs 06:30 to 17:30 on haulage days. Blasting on the existing faces as '
                      'required, at about 12:15 during the haulage break.')
    doc.core_properties.author = MANAGER
    buf = io.BytesIO()
    doc.save(path)
    office_scrub(path, 'docx', MANAGER, 'Calderwick Stone Ltd', '2026-11-19T08:55:00Z|2026-11-27T16:40:00Z', 'Phase 4 working scheme January 2027')


# ------------------------------------------------------------------------------------------------- plant register

def register(path):
    body, h, t, small = st()
    def story():
        rows = [['Fleet no.', 'Type', 'Make and model', 'Serial', 'Telematics unit', 'Rated payload (t)',
                 'Guaranteed LWA dB (2000/14/EC)', 'On hire from']]
        sers = {'T27': 'VCE0A40GV00712', 'T31': 'VCE0A40GC00933', 'T33': 'CAT0740GCLX21094', 'T38': 'VCE0A40GJ01147',
                'T41': 'CAT0740GCLX21388', 'T44': 'VCE0A40GL01206', 'T52': 'BELB40E2201784'}
        hire = {'T27': '06/01/2025', 'T31': '06/01/2025', 'T33': '14/04/2025', 'T38': '03/02/2026', 'T41': '03/02/2026',
                'T44': '20/04/2026', 'T52': '20/04/2026'}
        for (fn, unit, model) in W.FLEET:
            rows.append([fn, 'Articulated dump truck', model, sers[fn], unit, '39.0' if 'Volvo' in model else ('38.0' if 'Cat' in model else '40.0'),
                         '%d' % W.DECLARED_LWA[model], hire[fn]])
        rows += [['L3104', 'Wheel loader', 'Volvo L150H', 'VCE0L150HE04112', '-', '-', '106', '11/03/2024'],
                 ['E2201', 'Tracked excavator', 'Komatsu PC490LC-11', 'KMTPC490K31027', '-', '-', '107', '02/09/2024'],
                 ['E2207', 'Tracked excavator', 'Volvo EC480E', 'VCEC480EK20418', '-', '-', '107', '17/02/2025']]
        tb = Table(rows, colWidths=[15 * mm, 30 * mm, 30 * mm, 30 * mm, 22 * mm, 15 * mm, 18 * mm, 17 * mm])
        tb.setStyle(tstyle())
        return [Paragraph('Calderwick Stone Ltd', small), Paragraph('Ravensby Quarry plant register', t),
                Paragraph('Mobile plant on site at 2 November 2026. Dump trucks are hired from Thwaite Plant Hire with '
                          'operators; fleet numbers are the hire company\'s.', body), tb, Spacer(1, 6),
                Paragraph('Register kept by the quarry manager. Last updated 2 November 2026.', small)]
    pdf(path, 'Ravensby plant register', MANAGER, 'Microsoft Excel for Microsoft 365', stamp(2026, 11, 2), story,
        'Ravensby Quarry plant register')


# ------------------------------------------------------------------------------------------- interruption notices

def dno(path, outages):
    body, h, t, small = st()
    def story():
        rows = [['Ref.', 'Date', 'Supply lost', 'Supply restored', 'Cause']]
        causes = ['Fault on 11 kV overhead line (wind)', 'Fault on 11 kV overhead line (tree contact)',
                  'Protection operation, cause not found', 'Third-party damage to 11 kV cable', 'Lightning']
        for i, (a, b) in enumerate(sorted(outages)):
            rows.append(['NF-%d-%04d' % (a.year, 3117 + 23 * i + (i * i) % 17), a.strftime('%d/%m/%Y'), a.strftime('%H:%M'),
                         b.strftime('%H:%M'), causes[(i * 3 + a.day) % len(causes)]])
        tb = Table(rows, colWidths=[28 * mm, 22 * mm, 22 * mm, 24 * mm, 78 * mm])
        tb.setStyle(tstyle())
        return [Paragraph('Northfell Electricity Networks', small),
                Paragraph('Supply interruptions: Ravensby Quarry (MPAN 17 2204 6611 093)', t),
                Paragraph('Unplanned interruptions to the site\'s 11 kV supply between 1 May and 31 October 2026, from our '
                          'network control logs. Times are local.', body), tb, Spacer(1, 6),
                Paragraph('Issued on request to the customer, 6 November 2026.', small)]
    pdf(path, 'Supply interruptions Ravensby Quarry 2026', 'Northfell Electricity Networks', 'Microsoft Word for Microsoft 365',
        stamp(2026, 11, 6), story, 'Northfell Electricity Networks customer notice')
