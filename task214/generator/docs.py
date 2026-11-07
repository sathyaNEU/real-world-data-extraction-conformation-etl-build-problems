"""The four documents the organisations issued, as short PDFs (reportlab, invariant)."""
import datetime as dt

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import pack
import world

SS = getSampleStyleSheet()
BODY = ParagraphStyle('b', parent=SS['BodyText'], fontName='Helvetica', fontSize=9.4, leading=12.4, alignment=TA_LEFT)
H1 = ParagraphStyle('h1', parent=SS['Heading1'], fontName='Helvetica-Bold', fontSize=13.5, leading=16, spaceAfter=4)
H2 = ParagraphStyle('h2', parent=SS['Heading2'], fontName='Helvetica-Bold', fontSize=10.5, leading=13, spaceBefore=6, spaceAfter=2)
CELL = ParagraphStyle('c', parent=BODY, fontSize=8.2, leading=10)
SMALL = ParagraphStyle('s', parent=BODY, fontSize=8, leading=10, textColor=colors.HexColor('#444444'))


def build_pdf(path, story, title, author, subject, issued, offset):
    """issued is the local issue time, offset the hours ahead of UTC on that date (+12 NZST, +13 NZDT)."""
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=16 * mm, title=title, author=author, subject=subject, creator=author,
                            producer=author, invariant=1)
    doc.build(story)
    raw = open(path, 'rb').read()
    for old in (b'ReportLab Generated PDF document', b'ReportLab generated PDF document', b'ReportLab', b'reportlab'):
        raw = raw.replace(old, (b'Kotare document ' * 4)[:len(old)])
    # the invariant build's fixed date becomes the document's own issue time (creation, then the last save)
    fixed = b"D:20000101000000+00'00'"
    assert raw.count(fixed) == 2, raw.count(fixed)
    for when in (issued, issued + dt.timedelta(minutes=6)):
        stamp = ('D:' + when.strftime('%Y%m%d%H%M%S') + "%+03d'00'" % offset).encode()
        assert len(stamp) == len(fixed)
        i = raw.index(fixed)
        raw = raw[:i] + stamp + raw[i + len(fixed):]
    open(path, 'wb').write(raw)


def table(rows, widths, head=True):
    t = Table(rows, colWidths=[w * mm for w in widths], repeatRows=1 if head else 0)
    st = [('FONT', (0, 0), (-1, -1), 'Helvetica', 8.2), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
          ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#999999')), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
          ('TOPPADDING', (0, 0), (-1, -1), 2)]
    if head:
        st += [('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 8.2), ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8ECEF'))]
    t.setStyle(TableStyle(st))
    return t


def terms_of_reference(path):
    p = [Paragraph('Outbreak Control Team: terms of reference', H1),
         Paragraph('Cryptosporidiosis, Kotare District. Issued by the Medical Officer of Health, Public Health Service, '
                   'Kotare region. Version 1.1, 13 October 2027 (version 1.0 of 11 October superseded).', SMALL),
         Paragraph('1. Purpose', H2),
         Paragraph('The team investigates the cryptosporidiosis notified from the district since September 2027 and advises '
                   'Kotare District Council which drinking-water asset to take out of service before the renewal of the '
                   'Kowhai Hills feed main, programmed to start on 26 October 2027.', BODY),
         Paragraph('2. Membership', H2),
         Paragraph('Dr Anna Gullery, Medical Officer of Health (chair); Rhys Cook, Network Operations Lead, Kotare District '
                   'Council; two health protection officers; the laboratory liaison scientist; a communications adviser. '
                   'The water services regulator is kept informed by the council.', BODY),
         Paragraph('3. Case definitions', H2),
         Paragraph('A confirmed case is a person with compatible illness and Cryptosporidium detected in a faecal specimen by '
                   'antigen test, PCR or microscopy. A probable case is a person with compatible illness who is '
                   'epidemiologically linked to a confirmed case. The incubation period is 1 to 12 days, typically about 7. '
                   'Residents are people whose home address is in the district; a day runs from midnight to midnight, New '
                   'Zealand time.', BODY),
         Paragraph('4. Assessment of the source', H2),
         Paragraph('For each service reservoir and each boundary main, the team counts the confirmed cases among residents '
                   'with onset from 1 September to 18 October 2027 who, on at least one of the 1 to 12 days before their '
                   'onset, lived in a supply zone that received the asset\'s water for most of that day. The count is divided '
                   'by the asset\'s resident-days: the 2023 census usually resident population of each supply zone that '
                   'received the asset\'s water for most of a day, summed over the days from 20 August to 17 October 2027. '
                   'The rate is expressed per 100,000 resident-days. Assets whose water reached fewer than five cases are '
                   'not ranked. The asset recommended for removal from service is the one with the highest rate, and the '
                   'runner-up is the next highest.', BODY),
         Paragraph('5. Renewal', H2),
         Paragraph('The team reports the residents whose drinking water would pass through the recommended asset under the '
                   'renewal plan, so that the council can arrange their supply before work starts.', BODY),
         Paragraph('6. Testing summary', H2),
         Paragraph('The laboratory liaison scientist reports, for each month of specimen collection, the residents with at '
                   'least one faecal specimen tested for Cryptosporidium at the community laboratory, and the residents '
                   'whose specimen the reference laboratory typed as Cryptosporidium parvum or as C. hominis. A resident is '
                   'counted once in a month however many specimens they gave.', BODY),
         Paragraph('7. Meetings and records', H2),
         Paragraph('The team meets each weekday at 08:30 until the Medical Officer of Health stands it down. The health '
                   'protection officers keep the line list; the council provides its records as exported at 07:40 on 19 '
                   'October 2027.', BODY)]
    build_pdf(path, p, 'Outbreak Control Team terms of reference', 'Public Health Service, Kotare region',
              'Cryptosporidiosis outbreak control team', dt.datetime(2027, 10, 13, 16, 42), 13)


def performance_measures(path):
    p = [Paragraph('Water services: non-financial performance measures 2027/28', H1),
         Paragraph('Kotare District Council, Three Waters Services. Adopted with the Long-term Plan; this extract issued 1 '
                   'July 2027 for quarterly reporting.', SMALL),
         Paragraph('Measure 3: fault response times', H2),
         Paragraph('Where the council attends a call-out in response to a fault or unplanned interruption to its networked '
                   'reticulation system, the following median response times are measured: (a) attendance for urgent '
                   'call-outs, from the time the council receives notification to the time service personnel reach the '
                   'site; (b) resolution of urgent call-outs, from the time the council receives notification to the time '
                   'service personnel confirm resolution of the fault or interruption; (c) attendance for non-urgent '
                   'call-outs; and (d) resolution of non-urgent call-outs, measured the same way.', BODY),
         Paragraph('The council receives notification when the customer\'s call or message reaches the council or its '
                   'after-hours service. A call-out is urgent when the council grades it urgent at notification: a burst '
                   'main or a loss of supply. Medians are reported by the month in which notification was received, urgent '
                   'times in minutes and non-urgent times in hours.', BODY),
         Paragraph('Measure 4: customer satisfaction', H2),
         Paragraph('The total number of complaints received by the council about drinking water clarity, taste, odour, '
                   'pressure or flow, and continuity of supply, expressed per 1,000 connections to the council\'s networked '
                   'reticulation system. A complaint is a customer contact about one of these issues from a property '
                   'connected to the networked system, received through any channel the council takes complaints in: '
                   'phone, email, the website water quality form, the service centre counter and the after-hours service. '
                   'A complaint is counted in the period in which the customer made it. Connections are the networked '
                   'connections in the rating database at the end of the period.', BODY),
         Paragraph('Targets', H2),
         table([['Measure', 'Target 2027/28'], ['3(a) urgent attendance', '60 minutes or less'],
                ['3(b) urgent resolution', '480 minutes or less'], ['3(c) non-urgent attendance', '5 working days or less'],
                ['3(d) non-urgent resolution', '10 working days or less'],
                ['4 complaints, all five issues', '20 per 1,000 connections a year or fewer']], [80, 60])]
    build_pdf(path, p, 'Water services non-financial performance measures 2027/28', 'Kotare District Council',
              'Performance measures', dt.datetime(2027, 7, 1, 10, 15), 12)


def zone_register(path, trunk):
    rows = [['Supply zone', 'Name', 'Normal source', 'Inlet main']]
    order = sorted(world.ZONES, key=lambda z: pack.ZCODE[z])
    for z in order:
        parent = world.ZONES[z][0]
        src = parent
        while src not in world.RES:
            src = world.ZONES[src][0]
        via = '' if parent in world.RES else ' (through %s)' % pack.ZNAME[parent]
        rows.append([pack.ZCODE[z], pack.ZNAME[z], pack.RNAME[src] + via, trunk[world.ZONES[z][1]]['main_id']])
    p = [Paragraph('Supply zone register', H1),
         Paragraph('Kotare District Council, Three Waters Services. Normal supply arrangement of the networked supply. Issue 7, '
                   '16 August 2027.', SMALL), Spacer(1, 4), table(rows, [24, 40, 76, 28]), Spacer(1, 6),
         Paragraph('Revision history', H2),
         table([['Issue', 'Date', 'Change'],
                ['7', '16 Aug 2027', Paragraph('Zone boundary review: Totara Downs renumbered SZ13 to SZ31; Ngaio Rise '
                                               'renumbered SZ28 to SZ20.', CELL)],
                ['6', '3 Mar 2026', Paragraph('Eastfield inlet main replaced (new asset number).', CELL)],
                ['5', '20 Jul 2024', Paragraph('Ngaio Rise zone created from part of Pohutukawa Point.', CELL)]],
               [14, 24, 130])]
    build_pdf(path, p, 'Supply zone register, issue 7', 'Kotare District Council', 'Supply zone register',
              dt.datetime(2027, 8, 16, 14, 5), 12)


def renewal_programme(path, trunk, plan):
    rows = [['Date and time', 'Valve (field tag)', 'Operation']]
    for t, tag, op in plan:
        rows.append([t.strftime('%a %d %b %Y %H:%M'), tag, op])
    p = [Paragraph('Kowhai Hills feed main renewal: network and customer plan', H1),
         Paragraph('Kotare District Council, Capital Works. Contract CW-2027-0947. Plan revision B, 6 October 2027.', SMALL),
         Paragraph('Scope', H2),
         Paragraph('Replace %d m of the %d mm %s main %s from Kowhai Hills Reservoir to the Kowhai Hills zone inlet, and '
                   'reconnect the Matai Valley link main %s at the inlet chamber. Works run from 26 October to 6 November '
                   '2027, weekdays and the Saturday, 7:00 to 18:00.'
                   % (trunk['FM11']['length'], trunk['FM11']['dia'], trunk['FM11']['mat'], trunk['FM11']['main_id'],
                      trunk['LM12']['main_id']), BODY),
         Paragraph('Customers', H2),
         Paragraph('Supply is to be maintained to Kowhai Hills and Matai Valley throughout the works. Letters go to every '
                   'property in both zones by 21 October; the council\'s website carries the dates.', BODY),
         Paragraph('Planned valve operations', H2), table(rows, [55, 40, 30]), Spacer(1, 6),
         Paragraph('Operations are by the council\'s network crews under the network operations lead\'s permit.', SMALL)]
    build_pdf(path, p, 'Kowhai Hills feed main renewal plan', 'Kotare District Council', 'Capital works CW-2027-0947',
              dt.datetime(2027, 10, 6, 11, 20), 13)
