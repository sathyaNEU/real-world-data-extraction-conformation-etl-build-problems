"""task401: the governing and context documents (PDF through reportlab, DOCX through python-docx, XLSX through
openpyxl), each scrubbed to the writer it claims."""
import datetime as dt
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
import world_asks as A

FONT_DIR = '/usr/share/fonts/truetype/crosextra'
pdfmetrics.registerFont(TTFont('Carlito', os.path.join(FONT_DIR, 'Carlito-Regular.ttf')))
pdfmetrics.registerFont(TTFont('Carlito-Bold', os.path.join(FONT_DIR, 'Carlito-Bold.ttf')))
WORD = 'Microsoft\xae Word for Microsoft 365'
ORG = 'Wendmoor Water Ltd'
S = dict(
    title=ParagraphStyle('t', fontName='Carlito-Bold', fontSize=15, leading=19, spaceAfter=4),
    sub=ParagraphStyle('s', fontName='Carlito', fontSize=9.5, leading=12, textColor=colors.HexColor('#444444'), spaceAfter=10),
    h=ParagraphStyle('h', fontName='Carlito-Bold', fontSize=11.5, leading=15, spaceBefore=8, spaceAfter=3),
    p=ParagraphStyle('p', fontName='Carlito', fontSize=10.5, leading=14, spaceAfter=5),
    small=ParagraphStyle('m', fontName='Carlito', fontSize=8.5, leading=11, textColor=colors.HexColor('#555555')))
ISSUED = {'wendmoor_trade_effluent_charges_scheme_2025-26.pdf': '20250203110000Z',
          'coldmere_wrc_permit_summary.pdf': '20240611093000Z'}


def _pdf(path, title, author, flow):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=20 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=WORD, producer=WORD)
    doc.build(flow)
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import NameObject, TextStringObject, DictionaryObject
    r = PdfReader(io.BytesIO(buf.getvalue())); w = PdfWriter()
    for pg in r.pages:
        w.add_page(pg)
    stamp = 'D:%s' % ISSUED[os.path.basename(path)]
    info = DictionaryObject({NameObject('/Title'): TextStringObject(title), NameObject('/Author'): TextStringObject(author),
                             NameObject('/Creator'): TextStringObject(WORD), NameObject('/Producer'): TextStringObject(WORD),
                             NameObject('/CreationDate'): TextStringObject(stamp), NameObject('/ModDate'): TextStringObject(stamp)})
    w._info = w._add_object(info)
    b2 = io.BytesIO(); w.write(b2)
    open(path, 'wb').write(b2.getvalue())


def _table(rows, widths):
    t = Table(rows, colWidths=widths)
    t.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), 'Carlito'), ('FONTSIZE', (0, 0), (-1, -1), 9.5),
                           ('FONTNAME', (0, 0), (-1, 0), 'Carlito-Bold'), ('LINEBELOW', (0, 0), (-1, 0), 0.6, colors.black),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
    return t


def charges_scheme(out):
    P, Sx = (lambda t: Paragraph(t, S['p'])), (lambda t: Paragraph(t, S['h']))
    r = A.RATES
    flow = [Paragraph('Trade Effluent Charges Scheme 2025-26', S['title']),
            Paragraph('Wendmoor Water Ltd. Charges Scheme made under section 143 of the Water Industry Act 1991. '
                      'Effective 1 April 2025 to 31 March 2026.', S['sub']),
            Sx('1. Who this applies to'),
            P('These charges apply to every trader who discharges trade effluent to our sewers under a consent issued by '
              'us. Domestic sewage and surface water from trade premises are charged under our wholesale and retail '
              'charges schemes, not under this scheme.'),
            Sx('2. The charging formula'),
            P('The charge for each cubic metre of chargeable volume is calculated with the Mogden formula: '
              'C = R + V + Bv + (Ot/Os) x B + (St/Ss) x S.'),
            _table([['Term', 'Meaning', '2025-26 value'],
                    ['R', 'Reception and conveyance, per m3', '\xa3%.4f' % r['R']],
                    ['V', 'Volumetric and primary treatment, per m3', '\xa3%.4f' % r['V']],
                    ['Bv', 'Additional volume charge for biological treatment, per m3', '\xa3%.4f' % r['Bv']],
                    ['B', 'Biological oxidation of settled sewage, per m3', '\xa3%.4f' % r['B']],
                    ['S', 'Treatment and disposal of primary sludge, per m3', '\xa3%.4f' % r['S']],
                    ['Os', 'Chemical oxygen demand of settled standard sewage', '%d mg/l' % r['Os']],
                    ['Ss', 'Suspended solids of standard sewage', '%d mg/l' % r['Ss']],
                    ['Ot', 'Settled chemical oxygen demand of the trade effluent', 'see section 4'],
                    ['St', 'Suspended solids of the trade effluent', 'see section 4']], [18 * mm, 105 * mm, 40 * mm]),
            Sx('3. Chargeable volume'),
            P('The chargeable volume for a charging year is the volume of trade effluent our meter at the trader\'s '
              'premises measured between 00:00 on 1 April and 00:00 on the following 1 April, less the allowance stated '
              'in the trader\'s consent for water that is not returned to the sewer. Our meters are read automatically at '
              '00:00 at the end of each quarter. A meter\'s register advance is multiplied by the register multiplier '
              'stated in the trader\'s consent.'),
            Sx('4. Strength'),
            P('Ot and St are the arithmetic means, over the composite samples we collect at the sampling point named in '
              'the trader\'s consent in the charging year, of each composite sample\'s settled chemical oxygen demand and '
              'suspended solids. A composite sample is everything our sampler at the trader\'s premises collects between '
              'one weekly round and the next; where the sampler fills a second bottle, the two bottles together are the '
              'composite sample. The strength of a composite sample is the strength of the effluent it holds. Where Ot '
              'or St is below the standard strength, the standard strength is not substituted.'),
            Sx('5. Calculation and billing'),
            P('The annual charge is the chargeable volume multiplied by the charge per cubic metre, calculated to the '
              'penny. Quarterly bills on account are reconciled to the annual charge after the end of the charging year. '
              'VAT is not charged on trade effluent charges.'),
            Sx('6. Disputes'),
            P('A trader who disputes a charge may ask for it to be reviewed within 28 days of the bill. Disputes about '
              'the terms of a consent are referred to Ofwat under section 122 of the Act.'),
            Spacer(1, 6), Paragraph('Trade Effluent Team, Wendmoor Water Ltd, Corrin House, Lowfield Road. Issued February 2025.', S['small'])]
    _pdf(os.path.join(out, 'wendmoor_trade_effluent_charges_scheme_2025-26.pdf'), 'Trade Effluent Charges Scheme 2025-26',
         'Trade Effluent Team', flow)


def permit_summary(out):
    P, Sx = (lambda t: Paragraph(t, S['p'])), (lambda t: Paragraph(t, S['h']))
    flow = [Paragraph('Coldmere Water Recycling Centre: environmental permit summary', S['title']),
            Paragraph('Permit EPR/WM4417KD, variation of June 2024. Summary prepared by Wendmoor Water for internal use; '
                      'the permit itself governs.', S['sub']),
            Sx('Discharge'),
            P('Final effluent to the River Allery at NGR SK 4410 2875, downstream of Hollins Bridge. Storm tank overflow '
              'to the Allery at the same outfall.'),
            Sx('Numeric limits for the final effluent'),
            _table([['Determinand', '95th percentile', 'Upper tier', 'Annual mean'],
                    ['Biochemical oxygen demand (ATU)', '15 mg/l', '50 mg/l', ''],
                    ['Suspended solids', '30 mg/l', '100 mg/l', ''],
                    ['Ammoniacal nitrogen (as N)', '5 mg/l', '20 mg/l', ''],
                    ['Total phosphorus (as P)', '', '', '0.5 mg/l']], [62 * mm, 33 * mm, 33 * mm, 33 * mm]),
            Sx('Compliance'),
            P('Compliance with the 95th percentile limits is assessed on the samples taken under the operator '
              'self-monitoring programme in each calendar year, against the look-up table in the permit.'),
            Sx('Flow'),
            P('Dry weather flow 9,600 m3/d. Flow to full treatment 412 l/s.')]
    _pdf(os.path.join(out, 'coldmere_wrc_permit_summary.pdf'), 'Coldmere WRC permit summary', 'Environment Planning', flow)


APP_XML = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Properties xmlns="http://schemas.openxmlformats.org/'
           'officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/'
           'docPropsVTypes"><Template>Normal.dotm</Template><TotalTime>%d</TotalTime><Pages>%d</Pages><Words>%d</Words>'
           '<Characters>%d</Characters><Application>Microsoft Office Word</Application><DocSecurity>0</DocSecurity>'
           '<Lines>%d</Lines><Paragraphs>%d</Paragraphs><ScaleCrop>false</ScaleCrop><Company>%s</Company>'
           '<LinksUpToDate>false</LinksUpToDate><CharactersWithSpaces>%d</CharactersWithSpaces><SharedDoc>false</SharedDoc>'
           '<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0000</AppVersion></Properties>')


def scrub_docx(path, words, pages, stamp):
    src = zipfile.ZipFile(path)
    items = [(i, src.read(i.filename)) for i in src.infolist()]
    src.close()
    out = []
    for info, data in items:
        name = info.filename
        if name in ('word/stylesWithEffects.xml', 'docProps/thumbnail.jpeg'):
            continue
        if name == 'docProps/app.xml':
            data = (APP_XML % (41, pages, words, words * 6, words // 11, 21, ORG, words * 7)).encode()
        if name in ('[Content_Types].xml', 'word/_rels/document.xml.rels'):
            data = re.sub(rb'<(Override|Relationship)[^>]*stylesWithEffects[^>]*/>', b'', data)
        if name == '_rels/.rels':
            data = re.sub(rb'<Relationship[^>]*metadata/thumbnail[^>]*/>', b'', data)
        if name == '[Content_Types].xml':
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
                data = re.sub(rb'(<dc:creator[^>]*>)[^<]*(</dc:creator>)', rb'\g<1>' + author.encode() + rb'\g<2>', data)
                data = re.sub(rb'(<cp:lastModifiedBy[^>]*>)[^<]*(</cp:lastModifiedBy>)', rb'\g<1>' + author.encode() + rb'\g<2>', data)
                data = re.sub(rb'(<dcterms:created[^>]*>)[^<]*', rb'\g<1>' + created.encode(), data)
                data = re.sub(rb'(<dcterms:modified[^>]*>)[^<]*', rb'\g<1>' + modified.encode(), data)
            if name == 'docProps/app.xml':
                data = re.sub(rb'<Application>[^<]*</Application>', b'<Application>Microsoft Excel</Application>', data)
                data = re.sub(rb'<AppVersion>[^<]*</AppVersion>', b'<AppVersion>16.0300</AppVersion>', data)
            zi = zipfile.ZipInfo(name, date_time=stamp); zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)


def _docx(path, author, created, modified, title, build, stamp):
    from docx import Document
    from docx.shared import Pt
    d = Document()
    st = d.styles['Normal']; st.font.name = 'Calibri'; st.font.size = Pt(11)
    build(d)
    cp = d.core_properties
    cp.author = author; cp.last_modified_by = author
    cp.created = created; cp.modified = modified
    cp.revision = 4; cp.title = title; cp.subject = ''; cp.keywords = ''; cp.comments = ''; cp.category = ''
    words = sum(len(p.text.split()) for p in d.paragraphs)
    d.save(path)
    scrub_docx(path, words=words, pages=max(1, words // 420 + 1), stamp=stamp)


def brief(out):
    def build(d):
        d.add_heading('Coldmere WRC: ammonia below the works, terms of the investigation', level=1)
        d.add_paragraph('Environment Programme, Wendmoor Water. For the environment programme submission to the '
                        'Environment Agency due in January 2027.')
        d.add_heading('1. Why we are looking', level=2)
        d.add_paragraph('The downstream monitor on the River Allery below Coldmere WRC recorded many more days above the '
                        'good-status standard for ammonia in the winter of 2025-26 than in the winter before. Our asset '
                        'plan carries a nitrification upgrade at Coldmere (an additional aeration lane and blower capacity '
                        'sized to 2031 growth, estimated at \xa314.2 million). The submission has to say whether that '
                        'upgrade is the answer to what the monitor recorded.')
        d.add_heading('2. What counts', level=2)
        d.add_paragraph('An exceedance day is a day, midnight to midnight UK time, on which the mean of the downstream '
                        'monitor\'s valid fifteen-minute ammonium readings (as N) is above 0.6 mg/l, the good-status '
                        'standard for the Allery\'s water body (lowland, high alkalinity). A reading flagged at a '
                        'maintenance visit is not valid. A day counts only with at least 72 valid readings. Ratified '
                        'readings are used where released, provisional readings after that.')
        d.add_paragraph('The investigation covers 1 November 2025 to 31 March 2026 and compares it with 1 November 2024 to '
                        '31 March 2025.')
        d.add_heading('3. What the review must answer', level=2)
        d.add_paragraph('For each option below, the review says which of the exceedance days of 1 November 2025 to 31 '
                        'March 2026 it would have prevented, and so whether it belongs in the submission.')
        for line in ('The nitrification upgrade at Coldmere.',
                     'Returning the aeration to its settings before the ammonia-based control went in on 27 October 2025.',
                     'Reviewing the consents of the trade dischargers to Coldmere\'s catchment.',
                     'Catchment measures upstream of the works with the farm advice team.'):
            d.add_paragraph(line, style='List Bullet')
        d.add_heading('4. Supporting figures for the submission', level=2)
        d.add_paragraph('Trade effluent: each discharger\'s chargeable volume and its settled COD and suspended solids '
                        'strengths for 2025-26 are as the 2025-26 charges scheme defines them.')
        d.add_heading('5. Contacts', level=2)
        d.add_paragraph('Environment programme: Gerard Norris. Trade effluent: Katy Hughes. Coldmere process science: '
                        'Sylvia Phillips.')
    _docx(os.path.join(out, 'coldmere_ammonia_investigation_terms.docx'), 'Gerard Norris', dt.datetime(2026, 9, 22, 8, 47),
          dt.datetime(2026, 10, 9, 15, 6), 'Coldmere WRC ammonia investigation terms', build, (2026, 10, 9, 15, 6, 0))


def works_record(out):
    def build(d):
        d.add_heading('Coldmere WRC: October 2025 shutdown, record of works', level=1)
        d.add_paragraph('Planned works 13 to 31 October 2025, compiled from the contractors\' completion sheets and the '
                        'permit-to-work log.')
        items = [
            ('13 to 15 October', 'Inlet screen 2 replaced (6 mm perforated plate). Screen 1 ran as duty throughout.'),
            ('14 October', 'Storm tank outlet penstock seals replaced; the tank was isolated for 9 hours.'),
            ('16 to 17 October', 'Return activated sludge pump 2 overhauled; pump 1 duty.'),
            ('20 to 24 October', 'Blower house B: the incomer current transformers were changed from 200/5 to 400/5 '
                                 'at 10:30 on 20 October to suit the new starters, meter BH-B being read at 10:30 '
                                 'immediately before the change; the blower motor starters were then replaced one machine '
                                 'at a time with the board live. Meter BH-A was read at 10:15 the same morning for the '
                                 'contractor\'s load survey.'),
            ('21 October', 'Mixed liquor suspended solids probes on both lanes cleaned and recalibrated.'),
            ('27 October', 'Turbo blower TB1 commissioned as the duty blower for both aeration lanes. TB1 is supplied '
                           'from the new LV board MCC 7 in the inlet works building and metered there; MCC 7 carries no '
                           'other load. The blower house B machines now run as standby.'),
            ('29 to 31 October', 'Final effluent sampler housing replaced; autosampler re-sited 2 m downstream.')]
        t = d.add_table(rows=1, cols=2)
        t.rows[0].cells[0].text = 'Date'; t.rows[0].cells[1].text = 'Work'
        for a, b in items:
            r = t.add_row().cells
            r[0].text = a; r[1].text = b
        d.add_paragraph('')
        d.add_paragraph('Permits to work closed and isolations removed by 31 October 2025.')
    _docx(os.path.join(out, 'coldmere_shutdown_works_record_oct2025.docx'), 'Leonard James',
          dt.datetime(2025, 11, 3, 9, 12), dt.datetime(2025, 11, 6, 16, 48), 'Coldmere WRC October 2025 shutdown works',
          build, (2025, 11, 6, 16, 48, 0))


def _xlsx(path, sheets, author, created, modified, stamp):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    wb.remove(wb.active)
    for title, rows, widths in sheets:
        ws = wb.create_sheet(title)
        for r in rows:
            ws.append(list(r))
        for c in ws[1]:
            c.font = Font(bold=True)
        for i, w in enumerate(widths):
            ws.column_dimensions[chr(65 + i)].width = w
    wb.save(path)
    scrub_xlsx(path, author, created, modified, stamp)


def consents_register(out):
    rows = [('discharger', 'customer_code', 'consent_ref', 'consent_issued', 'sampling_point', 'meter_point',
             'register_multiplier', 'max_daily_volume_m3', 'non_returned_allowance_pct', 'ph_range', 'max_temperature_c',
             'max_cod_settled_mg_l', 'max_ss_mg_l')]
    issued = ['2021-03-15', '2019-11-04', '2022-06-20', '2023-01-09', '2020-08-17']
    caps = [(420, 6000, 1500), (160, 8000, 1200), (180, 3000, 600), (130, 5000, 500), (110, 6000, 1800)]
    for (name, code, consent, lims, point, daily, allow, ot, st), iss, (mx, cod, ss) in zip(A.DISCHARGERS, issued, caps):
        rows.append((name, lims, consent, iss, point, 'MP-%s' % code[-3:], 10 if name == A.TEN_REGISTER else 1, mx,
                     round(allow * 100, 1), '6 to 11', 43, cod, ss))
    cond = [('condition', 'text'),
            ('1', 'The trade effluent shall be discharged only through the sampling point named in this consent.'),
            ('2', 'The pH of any sample of the trade effluent taken at the sampling point shall be not less than 6 nor '
                  'more than 11.'),
            ('3', 'The temperature of the trade effluent shall not exceed 43 degrees Celsius.'),
            ('4', 'The settled chemical oxygen demand and suspended solids of any sample shall not exceed the values in '
                  'the schedule.'),
            ('5', 'The discharger shall keep a continuous record of the flow, pH and temperature of the trade effluent at '
                  'the sampling chamber and make it available to the undertaker.'),
            ('6', 'The undertaker may take samples at any time.')]
    _xlsx(os.path.join(out, 'trade_effluent_consents_register.xlsx'),
          [('Consents', rows, [26, 14, 12, 14, 14, 12, 18, 18, 24, 10, 10, 20, 12]), ('Standard conditions', cond, [10, 120])],
          'Katy Hughes', '2023-02-01T09:15:00Z', '2025-10-06T11:20:00Z', (2025, 10, 6, 11, 20, 0))


def energy_register(out, snaps):
    meters = [('meter_id', 'location', 'supply', 'register_digits', 'ct_ratio', 'multiplier'),
              ('BH-A', 'Blower house A incomer', 'LV', 6, '200/5', 40),
              ('BH-B', 'Blower house B incomer', 'LV', 6, '400/5', 80),
              ('MCC-7', 'MCC 7, inlet works building', 'LV', 6, 'whole current', 1),
              ('INL-1', 'Inlet pumping station', 'LV', 6, 'whole current', 1),
              ('SLG-1', 'Sludge treatment building', 'LV', 6, 'whole current', 1)]
    reads = [('meter_id', 'read_at', 'register', 'read_type')]
    for s in sorted(snaps, key=lambda s: (s['meter'], s['read_at'])):
        reads.append((s['meter'], s['read_at'].strftime('%Y-%m-%d %H:%M'), s['register'], s['kind']))
    notes = [('convention',),
             ('Registers are cumulative in meter units and roll over to zero after 999999.',),
             ('A meter\'s consumption in kWh is its register advance multiplied by its multiplier.',),
             ('The monthly snapshot is the meter\'s own register at 00:00 UK time on the first of the month and is the '
              'count of record for the month\'s consumption.',),
             ('Half-hourly interval data are held in the energy data system.',),
             ('The Meters sheet shows each meter\'s current transformers and multiplier as at 30 September 2026.',)]
    _xlsx(os.path.join(out, 'coldmere_energy_metering_register.xlsx'),
          [('Meters', meters, [10, 44, 8, 16, 14, 11]), ('Register reads', reads, [10, 18, 12, 20]), ('Conventions', notes, [110])],
          'Site Energy Manager', '2021-05-11T07:58:00Z', '2026-10-01T08:41:00Z', (2026, 10, 1, 8, 41, 0))


def biology(out, rng):
    rows = [('site', 'survey_date', 'season', 'whpt_aspt', 'whpt_ntaxa', 'lifes')]
    for site in ('Allery u/s Hollins Bridge', 'Allery d/s Coldmere WRC', 'Allery at Mill Lane'):
        for d, sea in (('2025-04-23', 'Spring'), ('2025-10-08', 'Autumn')):
            rows.append((site, d, sea, round(float(rng.uniform(5.1, 6.4)), 2), int(rng.integers(14, 27)),
                         round(float(rng.uniform(6.4, 7.3)), 2)))
    _xlsx(os.path.join(out, 'allery_invertebrate_surveys_2025.xlsx'), [('Surveys', rows, [28, 12, 9, 11, 11, 8])],
          'Area Biology', '2025-11-19T10:05:00Z', '2025-11-19T10:31:00Z', (2025, 11, 19, 10, 31, 0))


def write_all(out, snaps, rng):
    charges_scheme(out); permit_summary(out); brief(out); works_record(out)
    consents_register(out); energy_register(out, snaps); biology(out, rng)
