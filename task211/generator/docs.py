"""Documents, workbooks, distractors and metadata for task211's pack. Every OOXML file is rewritten with sorted
entries and one fixed date; every PDF is written with reportlab's invariant mode and neutral metadata."""
import datetime as dt, io, json, zipfile
from pathlib import Path
import pandas as pd
from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import openpyxl
from openpyxl.styles import Font
import world as W

FIXED = dt.datetime(2026, 7, 17, 8, 30, 0)
SS = getSampleStyleSheet()
BODY = ParagraphStyle('b', parent=SS['BodyText'], fontName='Helvetica', fontSize=9.5, leading=12.5, spaceAfter=5)
H1 = ParagraphStyle('h1', parent=SS['Heading1'], fontName='Helvetica-Bold', fontSize=13, spaceAfter=6)
H2 = ParagraphStyle('h2', parent=SS['Heading2'], fontName='Helvetica-Bold', fontSize=10.5, spaceBefore=6, spaceAfter=3)
SMALL = ParagraphStyle('s', parent=BODY, fontSize=8, leading=10, textColor=colors.HexColor('#444444'))


def normalize_ooxml(path):
    data = Path(path).read_bytes()
    zin = zipfile.ZipFile(io.BytesIO(data))
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for n in sorted(zin.namelist(), key=lambda s: (s != '[Content_Types].xml', s)):
            zi = zipfile.ZipInfo(n, date_time=(2026, 7, 17, 8, 30, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, scrub_part(n, zin.read(n)))
    Path(path).write_bytes(out.getvalue())


def scrub_part(name, data):
    """The property parts as the organisation's own files would carry them: no writer's name, the fixed date."""
    import re
    if name == 'docProps/app.xml' and b'penpyxl' in data:
        return (b'<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
                b'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Microsoft Excel'
                b'</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop><Company>Larkhaven Health</Company>'
                b'<AppVersion>16.0300</AppVersion></Properties>')
    if name == 'docProps/core.xml':
        stamp = FIXED.strftime('%Y-%m-%dT%H:%M:%SZ').encode()
        data = re.sub(rb'(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)', rb'\g<1>' + stamp + rb'\g<2>', data)
        data = re.sub(rb'(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)', rb'\g<1>' + stamp + rb'\g<2>', data)
        data = re.sub(rb'<dc:description>[^<]*</dc:description>', b'<dc:description/>', data)
    return data


def xlsx_props(wb, title):
    p = wb.properties
    p.creator = 'Larkhaven Health'
    p.lastModifiedBy = 'Larkhaven Health'
    p.title = title
    p.created = FIXED
    p.modified = FIXED


def pdf(path, story, title, author):
    def meta(c, d):
        c.setTitle(title); c.setAuthor(author); c.setCreator(author); c.setProducer(author); c.setSubject(''); c.setKeywords('')
    doc = SimpleDocTemplate(str(path), pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                            topMargin=0.8 * inch, bottomMargin=0.8 * inch, title=title, author=author)
    doc.build(story, onFirstPage=meta, onLaterPages=meta)
    raw = Path(path).read_bytes()
    for sig in (b'ReportLab Generated PDF document (opensource)', b'ReportLab generated PDF document -- digest (opensource)'):
        raw = raw.replace(sig, b' ' * len(sig))      # the writer's comment lines, blanked at equal length (offsets hold)
    Path(path).write_bytes(raw)


def table(rows, widths=None):
    t = Table(rows, colWidths=widths, hAlign='LEFT')
    t.setStyle(TableStyle([('FONT', (0, 0), (-1, -1), 'Helvetica', 8.5), ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 8.5),
                           ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#999999')),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#eeeeee'))]))
    return t


def procedure(path):
    P = lambda t: Paragraph(t, BODY)
    s = [Paragraph('Larkhaven Health, Pharmacy and Therapeutics Committee', SMALL),
         Paragraph('MS-12 Post-market surveillance of interchangeable products', H1),
         Paragraph('Version 4, approved 9 March 2026. Owner: Formulary Quality Group. Applies to every multi-source '
                   'oral solid on the Larkhaven formulary for which the Group holds a contract laboratory slot.', SMALL),
         Paragraph('1. Purpose', H2),
         P('Larkhaven dispenses interchangeable products of one molecule and strength from several labelers. Each half-year '
           'the Formulary Quality Group reviews whether any of them should be sent to the contract laboratory for assay and '
           'dissolution testing against the reference product. The laboratory examines what is in the tablet: its content '
           'and how it releases the drug. One product can be sent each quarter.'),
         Paragraph('2. The review', H2),
         P('2.1 Products. Every interchangeable product of the molecule and strength under review that Larkhaven pharmacies '
           'dispensed in the review window is reviewed. The reference product is the one the formulary lists as reference '
           'for that molecule and strength.'),
         P('2.2 Window. The review window is the half-year the Group names when it opens the review.'),
         P('2.3 Outcome. A qualifying visit is an emergency department visit or an urgent admission whose first-listed '
           'diagnosis is in Appendix A. A visit that continues by transfer to another hospital within 24 hours counts once, '
           'on its first arrival. Visits are dated by their arrival in Pacific time, whichever hospital system recorded them.'),
         P('2.4 Patients and supply. A patient is a Larkhaven member; a member\'s medical record numbers, including merged '
           'records, are one patient. A paid pharmacy claim is a fill; a claim later reversed is not, and its resubmission '
           'is. A fill supplies the patient from its service date for its days of supply. Where two fills\' supplies '
           'overlap, the days of the overlap belong to the later fill. A patient-month is 30.4375 days of supply.'),
         P('2.5 Attribution. A qualifying visit belongs to the product whose supply covers its date. A visit on a day no '
           'supply covers belongs to no product.'),
         P('2.6 The excess. A product\'s excess is its patients\' qualifying visits in the window less the visits the same '
           'patients, over the same days of supply, would have had if the product\'s tablets released and delivered the drug '
           'as the reference product\'s tablets do. It is stated per 1,000 patient-months of the product\'s supply in the '
           'window.'),
         Paragraph('3. Selection', H2),
         P('3.1 The Group sends the product with the largest excess, provided that excess is at least 2.0 qualifying visits '
           'per 1,000 patient-months. If no product reaches 2.0, no product is sent that quarter and the slot is released.'),
         P('3.2 The referral states the product sent and its excess.'),
         Paragraph('Appendix A. First-listed diagnoses that qualify', H2),
         P('ICD-10-CM G40 (every subcategory: epilepsy and recurrent seizures) and R56.9 (unspecified convulsions). R56.0 '
           '(febrile convulsions) and R56.1 (post-traumatic seizures) do not qualify.')]
    pdf(path, s, 'MS-12 Post-market surveillance of interchangeable products', 'Larkhaven Health')


def halvorne_notice(path):
    P = lambda t: Paragraph(t, BODY)
    rows = [['Larkhaven distribution centre', 'New-site stock from']]
    for k, c in enumerate(W.DCS):
        rows.append([c + ' DC', W.date_of(W.DC_SWITCH[k]).strftime('%d %B %Y').lstrip('0')])
    s = [Paragraph('Halvorne Generics, Customer Supply', SMALL),
         Paragraph('Notice of change of manufacturing site: Levetiracetam Tablets USP, 500 mg (NDC 69788-0231-01)', H1),
         P('To: Larkhaven Health, Pharmacy Supply Chain. Reference HG-SCN-2025-117, issued 24 November 2025.'),
         P('Halvorne Generics is moving manufacture of Levetiracetam Tablets USP, 500 mg, from Marrowby Pharma Services to '
           'Halvorne\'s own site in Fort Wayne, Indiana. The change was approved on 15 September 2025. The NDC, the bottle of '
           '100 and the labeling are unchanged.'),
         P('Tablets made at Fort Wayne are pink, oval, film-coated tablets debossed H 500 on one side and plain on the other. '
           'Tablets made by Marrowby are white, oval, film-coated tablets debossed M5 on one side and plain on the other.'),
         P('Supply to each Larkhaven distribution centre moves to Fort Wayne stock on the date below. On that date our '
           'carrier collects the remaining Marrowby stock from the centre and from the pharmacies it supplies, and from that '
           'date every bottle the centre receives and issues, and every bottle its pharmacies dispense, is Fort Wayne stock.'),
         table(rows, [2.6 * inch, 1.8 * inch]), Spacer(1, 8),
         P('Questions: customer.supply@halvorne-generics.example')]
    pdf(path, s, 'Halvorne Generics notice HG-SCN-2025-117', 'Halvorne Generics')


def corwen_notice(path):
    P = lambda t: Paragraph(t, BODY)
    s = [Paragraph('Corwen, Trade Relations', SMALL),
         Paragraph('Notice of film-coat change: Levetiracetam Tablets, 500 mg (NDC 70412-0155-10)', H1),
         P('To: Larkhaven Health, Pharmacy Supply Chain. Issued 4 August 2025.'),
         P('The film coat of Corwen levetiracetam 500 mg tablets changes from blue to beige. The tablets are otherwise '
           'unchanged: oval, film-coated, debossed AV on one side and 500 on the other, made by Avenmoor Pharmaceuticals.'),
         P('Every bottle shipped to Larkhaven from 1 September 2025 carries the beige tablets; bottles shipped before then '
           'carry the blue. Larkhaven\'s distribution centres and pharmacies return their blue stock on 1 September 2025; '
           'from that date Larkhaven pharmacies dispense only the beige tablets.')]
    pdf(path, s, 'Corwen notice of film-coat change', 'Corwen')


def terms(path):
    P = lambda t: Paragraph(t, BODY)
    s = [Paragraph('Larkhaven Health, Pharmacy Supply Chain', SMALL),
         Paragraph('Purchasing manual, section 7, and the wholesaler service schedule (extracts)', H1),
         Paragraph('Purchasing manual 7.3: spend', H2),
         P('A quarter\'s spend on a product is what Larkhaven is invoiced for the bottles of it that its distribution '
           'centres received in that quarter. A bottle is received on the day the receiving log books it in. An amount the '
           'wholesaler invoices later for bottles already '
           'received, a price correction included, belongs to the quarter those bottles were received in.'),
         Paragraph('Wholesaler service schedule, clause 4: backorders', H2),
         P('A backorder of a product runs from the day the wholesaler\'s backorder notice opens it until the day before the '
           'wholesaler next ships that product to any Larkhaven ship-to. Days are Pacific calendar days. A backorder day '
           'counts in the quarter it falls in.'),
         Paragraph('Wholesaler service schedule, clause 9: item numbers', H2),
         P('The wholesaler identifies products on notices by its own item numbers. Its item list gives each item\'s NDC.')]
    pdf(path, s, 'Purchasing manual section 7 and wholesaler service schedule', 'Larkhaven Health')


def lab_quote(path):
    P = lambda t: Paragraph(t, BODY)
    rows = [['Service', 'Price (USD)'], ['Assay and content uniformity, one lot', '1,850'],
            ['Dissolution profile against reference, one lot (12 units, 4 media)', '3,400'],
            ['Retained-sample storage per lot per quarter', '120'], ['Report and data package', '650']]
    s = [Paragraph('Meridian Analytical Services', SMALL), Paragraph('Quotation Q-26-0418: third-quarter 2026 testing slot', H1),
         P('Prepared for Larkhaven Health, Formulary Quality Group, 2 July 2026. Valid to 30 September 2026. The slot '
           'covers one product; the Group supplies three lots dispensed in the review window.'),
         table(rows, [4.2 * inch, 1.2 * inch])]
    pdf(path, s, 'Quotation Q-26-0418', 'Meridian Analytical Services')


def register(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Descriptions'
    hdr = ['product', 'labeler', 'ndc', 'formulary_role', 'manufactured_by', 'description', 'approved']
    ws.append(hdr)
    for c in ws[1]:
        c.font = Font(bold=True)
    blue = 'Blue, oval, film-coated tablet debossed AV on one side and 500 on the other'
    white = 'White, oval, film-coated tablet debossed M5 on one side, plain on the other'
    orange = 'Orange, capsule-shaped, film-coated tablet debossed BC on one side and 45 on the other'
    rows = [('Levaril', 'Avenmoor Pharmaceuticals', '64871-0500-01', 'Avenmoor Pharmaceuticals, Durham NC', blue, dt.date(2019, 5, 14)),
            ('Corwen', 'Corwen', '70412-0155-10', 'Avenmoor Pharmaceuticals, Durham NC', blue, dt.date(2021, 2, 8)),
            ('Corwen', 'Corwen', '70412-0155-10', 'Avenmoor Pharmaceuticals, Durham NC',
             'Beige, oval, film-coated tablet debossed AV on one side and 500 on the other', dt.date(2025, 7, 22)),
            ('Halvorne', 'Halvorne Generics', '69788-0231-01', 'Marrowby Pharma Services, Vadodara', white, dt.date(2020, 9, 30)),
            ('Halvorne', 'Halvorne Generics', '69788-0231-01', 'Halvorne Generics, Fort Wayne IN',
             'Pink, oval, film-coated tablet debossed H 500 on one side, plain on the other', dt.date(2025, 9, 15)),
            ('Pellbrook', 'Pellbrook Pharmaceuticals', '71336-0418-01', 'Marrowby Pharma Services, Vadodara', white, dt.date(2020, 6, 3)),
            ('Tessard', 'Tessard Laboratories', '72609-0507-01', 'Brennick Contract Manufacturing, Hyderabad', orange, dt.date(2018, 11, 20)),
            ('Wynfield', 'Wynfield Pharma', '68844-0362-01', 'Brennick Contract Manufacturing, Hyderabad', orange, dt.date(2019, 4, 9))]
    for r in rows:
        ws.append([r[0], r[1], r[2], 'reference' if r[0] == 'Levaril' else 'interchangeable'] + list(r[3:]))
    for row in ws.iter_rows(min_row=2, min_col=7, max_col=7):
        for c in row:
            c.number_format = 'yyyy-mm-dd'
    for col, w in zip('ABCDEFG', (12, 26, 15, 16, 40, 82, 12)):
        ws.column_dimensions[col].width = w
    xlsx_props(wb, 'Formulary product register: levetiracetam 500 mg')
    wb.save(path)
    normalize_ooxml(path)


def monitor(path, M):
    """Context artifact: dispensed bottles by month and centre, every product together; no rates, no ranking."""
    c = M['claims']
    c = c[c.claim_status == 'PAID']
    rev = set(M['claims'].loc[M['claims'].claim_status == 'REVERSED', 'reversal_of'])
    c = c[~c.claim_id.isin(rev)]
    ph = M['pharm'].set_index('pharmacy_id')['distribution_centre']
    c = c.assign(month=pd.to_datetime(c.service_date).dt.strftime('%Y-%m'), centre=c.pharmacy_id.map(ph))
    t = c.groupby(['month', 'centre']).agg(fills=('claim_id', 'size'), tablets=('quantity', 'sum')).reset_index()
    t = t[t.month >= '2025-07']
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Dispensing'
    ws.append(['Levetiracetam 500 mg tablets dispensed by Larkhaven pharmacies, by month and distribution centre (all products)'])
    ws.append(['Refreshed 2026-07-14 from the claims warehouse. Paid claims net of reversals.'])
    ws.append([])
    ws.append(['month', 'distribution_centre', 'fills', 'tablets'])
    for r in t.itertuples(index=False):
        ws.append([r.month, r.centre, int(r.fills), int(r.tablets)])
    ws.column_dimensions['B'].width = 22
    xlsx_props(wb, 'Levetiracetam supply monitor')
    wb.save(path)
    normalize_ooxml(path)


def list_prices(path):
    rows = [dict(ndc=p['ndc'], product=p['name'], list_price_per_100=lp, effective='2026-01-01')
            for p, lp in zip(W.PRODUCTS, (212.40, 11.80, 11.10, 13.25, 9.90, 10.35))]
    pd.DataFrame(rows).to_csv(path, index=False, lineterminator='\n')


def write_documents(target, S, M, X):
    procedure(target / 'ms12_interchangeable_product_surveillance.pdf')
    halvorne_notice(target / 'halvorne_site_change_notice.pdf')
    corwen_notice(target / 'corwen_film_coat_notice.pdf')
    terms(target / 'purchasing_manual_and_service_schedule.pdf')
    lab_quote(target / 'contract_lab_quotation_2026q3.pdf')
    register(target / 'product_register.xlsx')
    monitor(target / 'levetiracetam_supply_monitor.xlsx', M)
    list_prices(target / 'formulary_list_prices_2026.csv')


def write_metadata(task, target):
    files = sorted(p.name for p in target.iterdir())
    meta = dict(task='task211', setting_date='2026-07-20', synthetic=True, license='CC BY 4.0',
                source='synthetic, generated by task211/generator/build.py from one seed; invented organisations and people',
                files=[dict(name=n, bytes=(target / n).stat().st_size) for n in files],
                distractors=['contract_lab_quotation_2026q3.pdf', 'formulary_list_prices_2026.csv',
                             'levetiracetam_supply_monitor.xlsx'],
                deliverables=['retest_referral.docx', 'levetiracetam_products.xlsx'])
    (task / 'metadata.json').write_text(json.dumps(meta, indent=2) + '\n')
