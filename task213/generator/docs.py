"""Documents and registers for task213's pack: the moderation playbook (the governing WHAT), the earlier integrity
notices and the Q2 transparency report (both declared wrong-basis distractors), the merchant programme register, the
support desk's case export and the custodian's outbound transfers. OOXML is rewritten with sorted entries and one
fixed date; PDFs use reportlab's invariant mode with neutral metadata."""
import datetime as dt, io, re, zipfile
from pathlib import Path
import numpy as np, pandas as pd
from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import openpyxl
from openpyxl.styles import Font
from render import utc, wat, T0
from core import Q, DAY

FIXED = dt.datetime(2026, 10, 6, 8, 40, 0)
ORG = 'Calabash Exchange Ltd'
SS = getSampleStyleSheet()
BODY = ParagraphStyle('b', parent=SS['BodyText'], fontName='Helvetica', fontSize=9.4, leading=12.6, spaceAfter=5)
H1 = ParagraphStyle('h1', parent=SS['Heading1'], fontName='Helvetica-Bold', fontSize=13.5, spaceAfter=4)
H2 = ParagraphStyle('h2', parent=SS['Heading2'], fontName='Helvetica-Bold', fontSize=10.4, spaceBefore=7, spaceAfter=3)
SMALL = ParagraphStyle('s', parent=BODY, fontSize=7.8, leading=9.8, textColor=colors.HexColor('#555555'))


def normalize_ooxml(path, stamp=None):
    data = Path(path).read_bytes()
    zin = zipfile.ZipFile(io.BytesIO(data))
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for n in sorted(zin.namelist(), key=lambda s: (s != '[Content_Types].xml', s)):
            zi = zipfile.ZipInfo(n, date_time=FIXED.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, scrub_part(n, zin.read(n), stamp or FIXED))
    Path(path).write_bytes(out.getvalue())


def scrub_part(name, data, when=None):
    if name == 'docProps/app.xml':
        return (b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
                b'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Microsoft Excel'
                b'</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop><Company>Calabash Exchange Ltd</Company>'
                b'<AppVersion>16.0300</AppVersion></Properties>')
    if name == 'docProps/core.xml':
        stamp = (when or FIXED).strftime('%Y-%m-%dT%H:%M:%SZ').encode()
        data = re.sub(rb'(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)', rb'\g<1>' + stamp + rb'\g<2>', data)
        data = re.sub(rb'(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)', rb'\g<1>' + stamp + rb'\g<2>', data)
        data = re.sub(rb'<dc:creator>[^<]*</dc:creator>', b'<dc:creator>Calabash Exchange Ltd</dc:creator>', data)
        data = re.sub(rb'<cp:lastModifiedBy>[^<]*</cp:lastModifiedBy>', b'<cp:lastModifiedBy>Calabash Exchange Ltd</cp:lastModifiedBy>', data)
        data = re.sub(rb'<dc:description>[^<]*</dc:description>', b'', data)
    return data


def xlsx_props(wb, title):
    p = wb.properties
    p.creator = ORG; p.lastModifiedBy = ORG; p.title = title; p.created = FIXED; p.modified = FIXED


def pdf(path, story, title, issued=None):
    def meta(c, d):
        c.setTitle(title); c.setAuthor(ORG); c.setCreator(ORG); c.setProducer(ORG); c.setSubject(''); c.setKeywords('')
        c.setFont('Helvetica', 7.2); c.setFillColor(colors.HexColor('#777777'))
        c.drawString(18 * mm, 10 * mm, '%s  |  %s  |  page %d' % (ORG, title, d.page))
    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=ORG)
    doc.build(story, onFirstPage=meta, onLaterPages=meta)
    raw = Path(path).read_bytes()
    for sig in (b'ReportLab Generated PDF document (opensource)', b'ReportLab generated PDF document -- digest (opensource)',
                b'ReportLab Generated PDF document', b'(opensource)'):
        raw = raw.replace(sig, b' ' * len(sig))
    if issued is not None:
        # the document's own issue time in place of the writer's fixed stamp, at equal length so offsets hold
        for k, when in ((b'/CreationDate', issued), (b'/ModDate', issued + dt.timedelta(minutes=7))):
            old = k + b" (D:20000101000000+00'00')"
            new = k + (" (D:%s+01'00')" % when.strftime('%Y%m%d%H%M%S')).encode()
            assert raw.count(old) == 1 and len(old) == len(new)
            raw = raw.replace(old, new)
    Path(path).write_bytes(raw)


def table(rows, widths=None):
    t = Table(rows, colWidths=widths, hAlign='LEFT')
    t.setStyle(TableStyle([('FONT', (0, 0), (-1, -1), 'Helvetica', 8.4), ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 8.4),
                           ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#9a9a9a')), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                           ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ece9e1'))]))
    return t


P = lambda s: Paragraph(s, BODY)


def playbook(path):
    st = [Paragraph('Trust and Safety: Moderation Playbook', H1),
          Paragraph('Version 4.2, in force from 1 July 2026. Owner: Integrity Policy. Replaces version 4.1 (March 2026).', SMALL),
          Spacer(1, 6),
          Paragraph('1. Ratings', H2),
          P('1.1 When an escrow order is released, the buyer and the seller may each rate the other once, from -10 to +10, '
            'within 72 hours of the release. A rating may be edited within 72 hours of being given; the ratings service keeps '
            'every version under the rating\'s ID.'),
          P('1.2 A rating counts once, in its latest version. A rating belongs to the calendar quarter, in UTC, in which it was '
            'first given; an edit does not move it to another quarter.'),
          P('1.3 Ratings on orders that the escrow cancelled or returned to the seller are not possible; the ratings service '
            'only opens a rating on a released order.'),
          Paragraph('2. Rating rings', H2),
          P('2.1 A rating ring is two or more accounts run together that trade with one another so that the accounts can rate '
            'one another. Accounts are run together when one person or group controls them.'),
          P('2.2 Every account in a ring is in the ring for the whole quarter swept, whatever date its part in the ring began.'),
          P('2.3 Calabash Points. A Calabash Point\'s tablet is used by the agent and by the customers the agent serves. An '
            'account a customer opened at a Calabash Point, or uses there, is the customer\'s own; it is not run together with '
            'the agent\'s account, or with other customers\' accounts, because it is used on the point\'s tablet.'),
          Paragraph('3. The quarterly sweep', H2),
          P('3.1 After each quarter closes, Integrity runs a sweep of the quarter. The sweep suspends every account in a ring and '
            'expunges every rating each of those accounts gave in the quarter swept, subject to 3.3.'),
          P('3.2 Ratings the suspended accounts received are not expunged for that reason alone.'),
          P('3.3 Holdback. No account loses more than half (rounded down) of the ratings it received as the seller in the '
            'quarter swept. This applies to every account, including an account the sweep suspends. Ratings above that number '
            'are held for manual review and are not expunged in the sweep; the review\'s decisions are reported separately.'),
          P('3.4 The Q3 2026 sweep runs in November 2026. Its result is published in the integrity notice of 1 December 2026, '
            'which states the number of ratings the sweep expunges to the nearest hundred.'),
          Paragraph('4. Appeals', H2),
          P('4.1 A suspended account may appeal within 30 days. Appeals are decided by a reviewer who did not take part in the '
            'sweep. An upheld appeal restores the account; it does not restore ratings expunged in the sweep.'),
          Paragraph('5. Records', H2),
          P('5.1 Integrity keeps the sweep\'s working files for seven years. Personal data in them is handled under the '
            'Privacy Notice and the Nigeria Data Protection Act 2023.')]
    pdf(path, st, 'Moderation Playbook v4.2', dt.datetime(2026, 6, 24, 10, 12, 0))


def notices(path):
    st = [Paragraph('Integrity notices, 2026', H1),
          Paragraph('Published quarterly on the Calabash Exchange help centre. Reproduced as issued.', SMALL), Spacer(1, 6),
          Paragraph('Integrity notice, 1 June 2026: the Q1 2026 sweep', H2),
          P('Our sweep of the first quarter, run in May, found rating rings among the accounts that traded between 1 January '
            'and 31 March 2026. We suspended 371 accounts and expunged 8,900 ratings those accounts gave in the quarter. A '
            'further 520 ratings were held for manual review under the holdback in section 3.3 of the moderation playbook.'),
          P('Ratings given on Calabash in Q1 2026: 168,900.'),
          Paragraph('Integrity notice, 1 September 2026: the Q2 2026 sweep', H2),
          P('Our sweep of the second quarter, run in August, found rating rings among the accounts that traded between 1 April '
            'and 30 June 2026. We suspended 412 accounts and expunged 9,800 ratings those accounts gave in the quarter. A '
            'further 610 ratings were held for manual review under the holdback.'),
          P('Ratings given on Calabash in Q2 2026: 181,400.'),
          P('Accounts suspended in a sweep remain suspended unless an appeal succeeds. Of the 371 accounts suspended in the Q1 '
            'sweep, 9 were restored on appeal; of the 412 suspended in the Q2 sweep, appeals are still being decided.')]
    pdf(path, st, 'Integrity notices 2026', dt.datetime(2026, 9, 1, 8, 5, 0))


def transparency(path, npoints=41):
    rows = [['Quarter', 'Ratings given', 'Sample labelled', 'Labelled inauthentic', 'Prevalence', '95% interval'],
            ['Q3 2025', '149,200', '2,000', '92', '4.6%', '3.7% to 5.6%'],
            ['Q4 2025', '158,700', '2,000', '102', '5.1%', '4.2% to 6.2%'],
            ['Q1 2026', '168,900', '2,000', '108', '5.4%', '4.5% to 6.5%'],
            ['Q2 2026', '181,400', '2,000', '106', '5.3%', '4.4% to 6.4%']]
    st = [Paragraph('Transparency report: Q2 2026', H1),
          Paragraph('Published 14 August 2026 by Integrity Policy.', SMALL), Spacer(1, 6),
          Paragraph('Inauthentic ratings', H2),
          P('Each quarter we draw a simple random sample of 2,000 of the ratings given in the quarter. Two reviewers label each '
            'sampled rating as authentic or inauthentic, and a third settles any disagreement. A rating is inauthentic if it was '
            'paid for, given under pressure, given in retaliation for a dispute, given by a fake account, or given by an account '
            'in a rating ring. Prevalence is the share of the sample labelled inauthentic.'),
          table(rows, [22 * mm, 26 * mm, 26 * mm, 32 * mm, 22 * mm, 30 * mm]), Spacer(1, 6),
          P('The Q3 2026 sample will be drawn when the quarter closes and labelled in January 2027, after the Q3 sweep, so '
            'that reviewers do not see the sweep\'s results while they label.'),
          Paragraph('Disputes', H2),
          P('Buyers and sellers can open a case with our support desk on any escrow order. In Q2 2026 the desk closed 1,794 '
            'cases. Most were complaints that coins had not been released after payment.'),
          Paragraph('Calabash Points', H2),
          P('Calabash Points are shops where customers can buy USDT for cash on the point\'s tablet. At 30 June 2026 there were '
            '%d points in Nigeria, Ghana and Kenya.' % npoints)]
    pdf(path, st, 'Transparency report Q2 2026', dt.datetime(2026, 8, 14, 9, 40, 0))


def merchant_programme(path, w, x, acct):
    rng = np.random.default_rng(31)
    A = x['A']
    words = ['Crest', 'Harbour', 'Kola', 'Savanna', 'Palm', 'Granite', 'Coral', 'Pilot', 'Orbit', 'Marula', 'Tamarind',
             'Copperleaf', 'Hibiscus', 'Ironwood', 'Okapi', 'Bluegum', 'Shea', 'Cowrie', 'Raffia', 'Ebonwood']
    tails = ['FX', 'Digital Assets', 'Exchange', 'Capital', 'Markets', 'OTC', 'Trading']
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'Groups'
    ws.append(['group_code', 'trading_name', 'market', 'treasury_wallet_no', 'joined_programme'])
    ws2 = wb.create_sheet('Desks'); ws2.append(['group_code', 'desk_handle', 'desk_type'])
    used = set()
    for i, (gw, desks, mk) in enumerate(w['groups']):
        code = 'MG%03d' % (i * 3 + 101 + rng.integers(0, 3))
        while True:
            nm = '%s %s' % (rng.choice(words), rng.choice(tails))
            if nm not in used: used.add(nm); break
        cur = x['tw'][gw]
        ws.append([code, nm, mk, x['wallet'][cur], (T0 - dt.timedelta(days=int(rng.integers(90, 700)))).date().isoformat()])
        for dsk in desks:
            ws2.append([code, x['handle_now'][dsk], rng.choice(['bank desk', 'mobile money desk', 'general desk'])])
    for s in (ws, ws2):
        for c in s[1]: c.font = Font(bold=True)
    xlsx_props(wb, 'Merchant programme register')
    wb.save(path); normalize_ooxml(path, dt.datetime(2026, 10, 1, 16, 42, 0))


def support_cases(path, x, render_out):
    rng = np.random.default_rng(37)
    C = x['cases'].sort_values('opened').reset_index(drop=True)
    order_of = render_out['order_of']
    nums = np.cumsum(rng.integers(1, 9, len(C))) + 418_200
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'Cases'
    ws.append(['case_no', 'opened_wat', 'customer_handle', 'order_ref', 'category', 'status', 'outcome', 'decided_wat'])
    for n, r in zip(nums, C.itertuples(index=False)):
        cat = 'coins not released' if r.role == 'buyer' else 'payment not received'
        ws.append(['CS-%d' % n, wat(r.opened), x['handle_at'](r.opener, r.opened), order_of[r.tid], cat, 'closed', r.code,
                   wat(r.decided)])
    ws2 = wb.create_sheet('Outcome codes')
    ws2.append(['code', 'meaning'])
    ws2.append(['U', 'Upheld: the desk decided the complaint in favour of the customer who opened the case.'])
    ws2.append(['R', 'Rejected: the desk decided the complaint against the customer who opened the case.'])
    ws2.append(['W', 'Withdrawn: the customer withdrew the complaint before a decision; the order completed normally.'])
    for s in (ws, ws2):
        for c in s[1]: c.font = Font(bold=True)
    xlsx_props(wb, 'Support desk cases Q3 2026')
    wb.save(path); normalize_ooxml(path, dt.datetime(2026, 10, 2, 8, 10, 0))
    return dict(zip(['CS-%d' % n for n in nums], C.index))


def desk_procedure(path):
    st = [Paragraph('Support Desk: Escrow Disputes Procedure', H1),
          Paragraph('SD-04, issue 3, in force from 1 June 2026. Owner: Customer Support Operations.', SMALL), Spacer(1, 6),
          Paragraph('1. Cases', H2),
          P('1.1 A buyer or a seller may open a case with the desk about an escrow order. Each customer opens their own '
            'case, so the buyer and the seller of one order may each have a case.'),
          P('1.2 A case is about the order whose coins the escrow is holding when the case is opened.'),
          Paragraph('2. Decisions', H2),
          P('2.1 The desk decides each complaint for or against the customer who opened the case, or records that the '
            'customer withdrew it. A decision for the buyer releases the coins to the buyer; a decision for the seller '
            'returns them to the seller.'),
          P('2.2 Decisions are recorded with the codes U (upheld), R (rejected) and W (withdrawn).'),
          Paragraph('3. Service levels', H2),
          P('3.1 The desk acknowledges a case within 30 minutes between 07:00 and 23:00 Lagos time and decides it within '
            '48 hours of the evidence being complete.'),
          Paragraph('4. Escalation', H2),
          P('4.1 A case involving suspected fraud is referred to Trust and Safety, which may suspend the accounts '
            'involved; the desk still records the case\'s decision.')]
    pdf(path, st, 'SD-04 Escrow Disputes Procedure', dt.datetime(2026, 5, 27, 15, 20, 0))


def programme_terms(path):
    st = [Paragraph('Merchant Programme: Terms for Merchant Groups', H1),
          Paragraph('MP-2, version 3, in force from 1 March 2026. Owner: Merchant Operations.', SMALL), Spacer(1, 6),
          Paragraph('1. Groups and desks', H2),
          P('1.1 A merchant group is a business that trades on Calabash through two or more desk accounts. Merchant '
            'Operations keeps a register of each group\'s desks and its treasury wallet.'),
          P('1.2 A group\'s treasury wallet is the wallet from which the group funds its desks and pays its cashback.'),
          Paragraph('2. Cashback', H2),
          P('2.1 A group may pay cashback to the buyers who trade with its desks. Cashback is paid to buyers\' own '
            'accounts, never to a desk or to another merchant.'),
          P('2.2 Cashback is promotional and is not a refund; it does not change the order it relates to.'),
          Paragraph('3. Conduct', H2),
          P('3.1 Desks of one group may not rate one another, and a group may not make cashback conditional on a rating.')]
    pdf(path, st, 'MP-2 Merchant Programme Terms', dt.datetime(2026, 2, 23, 11, 5, 0))


def custodian(path, x):
    C = x['chain'][x['chain'].block < Q].copy()
    from render import write_parquet, T0 as T0_
    out = pd.DataFrame({'tx_hash': C.tx.values, 'network': C.network.values,
                        'confirmed_at': pd.to_datetime([T0_ + dt.timedelta(minutes=float(b)) for b in C.block]).as_unit('s').tz_localize('UTC'),
                        'from_address': C.frm.values, 'to_address': C.to.values, 'amount_usdt': np.round(C.amt.values, 2),
                        'network_fee_usdt': np.round(C.fee.values, 4)})
    write_parquet(out, path)


def write_documents(target, w, x, ro):
    playbook(target / 'moderation_playbook_v4.2.pdf')
    notices(target / 'integrity_notices_2026.pdf')
    transparency(target / 'transparency_report_2026q2.pdf', len(w['agents']))
    merchant_programme(target / 'merchant_programme_2026-09-30.xlsx', w, x, ro['acct_id'])
    desk_procedure(target / 'support_desk_procedure_sd04.pdf')
    programme_terms(target / 'merchant_programme_terms_mp2.pdf')
    support_cases(target / 'support_cases_2026q3.xlsx', x, ro)
    custodian(target / 'custodian_outbound_2026q3.parquet', x)
