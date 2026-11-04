"""task403 documents and the two distractors: the conversion standard, the price notice, the programme sheet, the
product release log, the cancellation survey and the paid media report. Each in its producer's own form."""
import io
import re
import zipfile
import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
import world

TOR = world.TOR


# ---------------------------------------------------------------------------------------------- writers and scrubbing

def pdf(path, title, author, stamp, story_fn):
    """A PDF whose /Producer, /Creator, /Author and dates are the issuer's, rebuilt byte for byte."""
    def first(c, d):
        c._doc.info.producer = 'Microsoft Word for Microsoft 365'
        c._doc.info.creator = 'Microsoft Word for Microsoft 365'
        c._doc.info.author = author
        c._doc.info.title = title
        c._doc.info.subject = ''
        c.setFont('Helvetica', 7.5)
        c.drawString(0.9 * inch, 0.55 * inch, title)
        c.drawRightString(7.6 * inch, 0.55 * inch, 'Page %d' % c.getPageNumber())

    doc = SimpleDocTemplate(path, pagesize=letter, invariant=1, leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                            topMargin=0.85 * inch, bottomMargin=0.85 * inch)
    import calendar, os
    old = os.environ.get('SOURCE_DATE_EPOCH')
    os.environ['SOURCE_DATE_EPOCH'] = str(calendar.timegm(stamp))
    try:
        doc.build(story_fn(), onFirstPage=first, onLaterPages=first)
        scrub_pdf(path)
    finally:
        if old is None:
            del os.environ['SOURCE_DATE_EPOCH']
        else:
            os.environ['SOURCE_DATE_EPOCH'] = old


def scrub_pdf(path):
    """Blank the writer's comment lines byte for byte after their %, so every xref offset holds."""
    raw = open(path, 'rb').read()
    out = re.sub(rb'(%[^\n]*?)( ?ReportLab[^\n]*)', lambda m: m.group(1) + b' ' * len(m.group(2)), raw)
    assert len(out) == len(raw) and b'ReportLab' not in out
    open(path, 'wb').write(out)


def styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle('b', parent=ss['BodyText'], fontName='Helvetica', fontSize=9.6, leading=12.6, spaceAfter=5)
    h = ParagraphStyle('h', parent=ss['Heading2'], fontName='Helvetica-Bold', fontSize=11, spaceBefore=7, spaceAfter=3)
    t = ParagraphStyle('t', parent=ss['Title'], fontName='Helvetica-Bold', fontSize=14.5, alignment=0, spaceAfter=4)
    small = ParagraphStyle('s', parent=body, fontSize=8.2, leading=10.4, textColor=colors.HexColor('#333333'))
    return body, h, t, small


def xlsx_scrub(path, creator, stamp_iso, title=''):
    """Rewrite docProps of an openpyxl workbook so the issuer and the date are the organisation's, every other zip
    entry byte for byte, in the same order."""
    with open(path, 'rb') as f:
        src = f.read()
    zin = zipfile.ZipFile(io.BytesIO(src))
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == 'docProps/core.xml':
                data = (
                    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                    '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
                    'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
                    'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
                    '<dc:title>%s</dc:title><dc:creator>%s</dc:creator><cp:lastModifiedBy>%s</cp:lastModifiedBy>'
                    '<dcterms:created xsi:type="dcterms:W3CDTF">%s</dcterms:created>'
                    '<dcterms:modified xsi:type="dcterms:W3CDTF">%s</dcterms:modified></cp:coreProperties>'
                    % (title, creator, creator, stamp_iso, stamp_iso)).encode()
            elif info.filename == 'docProps/app.xml':
                data = (
                    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                    '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
                    'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
                    '<Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>'
                    '<Company>Ellesmere Media</Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
                    '<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>').encode()
            zi = zipfile.ZipInfo(info.filename, date_time=(2026, 2, 27, 9, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = info.external_attr
            zout.writestr(zi, data)
    with open(path, 'wb') as f:
        f.write(out.getvalue())


def stamp_tuple(y, m, d, hh=9, mm=0):
    import time
    return time.struct_time((y, m, d, hh, mm, 0, 0, 1, 0))


# ------------------------------------------------------------------------------------------------- governing documents

def conversion_standard(path):
    body, h, t, small = styles()

    def story():
        s = [Paragraph('Trial conversion: measurement standard', t),
             Paragraph('Ellesmere Media, Subscriber Growth Analytics. Version 3, issued 2 February 2026. Owner: Julie '
                       'Jacobson. Replaces version 2 of 15 September 2025.', small),
             Spacer(1, 6),
             Paragraph('1. Purpose', h),
             Paragraph('This standard sets how Subscriber Growth counts free trials and their conversion to paid for '
                       'monthly reporting, winter reviews and planning. Where another team\'s report counts differently, '
                       'this standard governs growth figures.', body),
             Paragraph('2. Trials', h),
             Paragraph('A trial is one account\'s free week on a monthly plan. A trial is counted in the month, and in '
                       'the winter, of its start date in Toronto time. It lasts seven days from its start, to the second; '
                       'the first monthly charge falls due when it ends.', body),
             Paragraph('3. Stages of a trial', h),
             Paragraph('A trial has played an episode when at least one episode was played during it (section 5). A '
                       'trial is still subscribed when it ends if its first charge is attempted. The share of first '
                       'charges collected is taken over the trials whose first charge was attempted.', body),
             Paragraph('4. Paid', h),
             Paragraph('A trial converts to paid when its first monthly charge is collected by the processor\'s first '
                       'attempt or by one of its scheduled retries: four attempts over five days on first charges due up '
                       'to 7 September 2025, three attempts over two days on those due from 8 September 2025. A charge '
                       'collected after the last scheduled retry does not convert the trial.', body),
             Paragraph('A plan change during the trial, including one made in its last minutes, does not end the '
                       'trial. Its first charge is the first charge of the subscription the trial ends on, on the plan in '
                       'force when it ends.', body),
             Paragraph('5. Viewing during a trial', h),
             Paragraph('An episode counts as played in a trial when any of it streams between the trial\'s start and '
                       'its end, whether the viewer started it or the player moved on to it from the episode before. A '
                       'play that stops partway, or in the credits, counts. Each episode counts once in a trial, in '
                       'English or in French, however often it is played or resumed.', body),
             Paragraph('6. Winter reviews', h),
             Paragraph('A winter review compares the trials started from 1 November to 31 January with the trials '
                       'started in the same months a year earlier. Programmes reviewed against a winter are valued as the '
                       'review\'s programme sheet states.', body),
             Paragraph('7. Revisions', h)]
        rev = [['Version', 'Issued', 'Change'],
               ['1', '7 October 2024', 'First issue.'],
               ['2', '15 September 2025', 'Retry schedule of the card processor in use from 8 September 2025.'],
               ['3', '2 February 2026', 'Plan changes during a trial (section 4); episodes played (section 5).']]
        tb = Table(rev, colWidths=[0.8 * inch, 1.4 * inch, 4.3 * inch])
        tb.setStyle(TableStyle([('FONT', (0, 0), (-1, -1), 'Helvetica', 8.6), ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 8.6),
                                ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black), ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
        s.append(tb)
        return s

    pdf(path, 'Trial conversion: measurement standard (v3)', 'Julie Jacobson', stamp_tuple(2026, 2, 2), story)


def price_notice(path):
    body, h, t, small = styles()

    def story():
        s = [Paragraph('New monthly prices for new subscriptions', t),
             Paragraph('Ellesmere Media, Pricing and Packaging. Notice PP-2025-07, issued 1 October 2025.', small),
             Spacer(1, 8),
             Paragraph('From 1 November 2025 the monthly price of a new Ellesmere subscription changes as follows, '
                       'before applicable sales tax.', body)]
        tb = Table([['Plan', 'Monthly price to 31 October 2025', 'Monthly price from 1 November 2025'],
                    ['Standard', 'CAD 9.99', 'CAD 11.99'], ['Premium', 'CAD 14.99', 'CAD 16.99']],
                   colWidths=[1.3 * inch, 2.4 * inch, 2.6 * inch])
        tb.setStyle(TableStyle([('FONT', (0, 0), (-1, -1), 'Helvetica', 9.2), ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 9.2),
                                ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black), ('TOPPADDING', (0, 0), (-1, -1), 3)]))
        s += [tb, Spacer(1, 8),
              Paragraph('A free trial that ends on or after 1 November 2025 is charged at the new price; a trial that '
                        'ends before then is charged at the old price. Subscriptions paid before 1 November 2025 keep '
                        'their price until further notice.', body),
              Paragraph('Customer notice: the sign-up pages, the plan pages in every app and the trial welcome e-mail '
                        'show the new prices from 1 November 2025. Customer care scripts are updated on 30 October.', body),
              Paragraph('Contact: Pricing and Packaging, Toronto.', small)]
        return s

    pdf(path, 'Notice PP-2025-07: new monthly prices', 'Pricing and Packaging', stamp_tuple(2025, 10, 1), story)


def programme_sheet(path, people):
    wb = Workbook()
    ws = wb.active
    ws.title = 'Programmes 2026-27'
    ws['A1'] = 'Subscriber growth budget: programmes for the 2026-27 winter'
    ws['A1'].font = Font(bold=True, size=12)
    ws['A2'] = ('Each programme is valued at the paid conversions the 2025-26 winter\'s trials (started 1 November 2025 to '
                '31 January 2026) lost to the cause it addresses, against the same months a year earlier; the four '
                'valuations and what none of them addresses account for the winter\'s fall once.')
    ws['A3'] = 'Prepared for the March 2026 review by %s. Sheet version 4, 6 March 2026.' % people[0]
    ws['A2'].alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells('A2:G2')
    ws.row_dimensions[2].height = 44
    hdr = ['Ref', 'Programme', 'What it does', 'Cause it addresses', 'Lead', 'Cost (CAD)', 'In place for 1 Nov 2026']
    rows = [
        ['A', 'First-month price hold', 'Trialists pay CAD 9.99 (Standard) or 14.99 (Premium) for their first paid '
         'month; later months at the list price.', 'The November 2025 price for new subscriptions', people[1], 1_180_000, 'Yes'],
        ['B', 'First-charge payment recovery', 'A fourth retry on first charges and a card updater with the processor.',
         'First charges declined and not recovered', people[2], 214_000, 'Yes'],
        ['C', 'Winter release slate', 'A weekly original airing from November to February: Gravel & Gold brought '
         'forward to November and a licensed weekly series for December and January.', 'The winter\'s release slate',
         'Content Planning', 2_650_000, 'Yes, if Gravel & Gold locks by July'],
        ['D', 'Paid acquisition mix', 'Move paid acquisition spend from social to search for the winter flights.',
         'The channel mix of trial sign-ups', people[1], 85_000, 'Yes'],
    ]
    ws.append([])
    ws.append(hdr)
    for c in ws[5]:
        c.font = Font(bold=True)
    for r in rows:
        ws.append(r)
    for col, w in zip('ABCDEFG', [5, 30, 62, 40, 18, 12, 30]):
        ws.column_dimensions[col].width = w
    for row in ws.iter_rows(min_row=6, max_row=9):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical='top')
        row[5].number_format = '#,##0'
    ws['A11'] = 'Funding: one programme from the subscriber growth budget, or none this cycle.'
    wb.properties.creator = people[0]
    wb.save(path)
    xlsx_scrub(path, people[0], '2026-03-06T10:12:00Z', 'Programmes 2026-27')


def release_log(path):
    """The product team's release log: every release across the apps, the platform and billing."""
    R = [
        ('2024-09-10', 'iOS app', '6.8', 'Continue watching row on the home screen'),
        ('2024-09-24', 'Web', '2024.38', 'Accessibility fixes on the player controls'),
        ('2024-10-08', 'Android app', '6.8', 'Downloads: storage picker'),
        ('2024-10-22', 'Smart TV app', '2.9', 'Faster start on older sets'),
        ('2024-11-05', 'Subscription platform', '6.4', 'Sales tax rounding for New Brunswick and Newfoundland and Labrador'),
        ('2024-11-19', 'iOS app', '6.9', 'French subtitles on downloads'),
        ('2024-12-03', 'Web', '2024.48', 'Gift card redemption page'),
        ('2024-12-17', 'Android app', '6.9', 'Crash fixes'),
        ('2025-01-14', 'Smart TV app', '2.10', 'Search by cast member'),
        ('2025-01-28', 'Viewing service', '11.2', 'Heartbeat interval from 60 to 30 seconds'),
        ('2025-02-03', 'Android TV app', '1.0', 'Launch on Google TV and Android TV'),
        ('2025-02-03', 'Subscription platform', '7.2', 'Plan changes during the free trial'),
        ('2025-02-08', 'Smart TV app', '3.0', 'New player; autoplay of the next episode'),
        ('2025-02-18', 'iOS app', '7.0', 'New player; autoplay of the next episode'),
        ('2025-02-25', 'Android app', '7.0', 'New player; autoplay of the next episode'),
        ('2025-03-11', 'Web', '2025.10', 'Autoplay of the next episode'),
        ('2025-03-25', 'Android TV app', '1.1', 'Remote control shortcuts'),
        ('2025-04-01', 'Subscription platform', '7.3', 'Nova Scotia HST at 14 per cent'),
        ('2025-04-15', 'Smart TV app', '3.1', 'Subtitle size settings'),
        ('2025-04-29', 'iOS app', '7.1', 'Widgets'),
        ('2025-05-13', 'Android app', '7.1', 'Widgets'),
        ('2025-05-27', 'Web', '2025.21', 'Profile icons'),
        ('2025-06-09', 'Subscription platform', '8.0', 'Accounts and subscriptions move to the new platform'),
        ('2025-06-09', 'Content system', '5.0', 'Catalogue and release calendar move to the new content system'),
        ('2025-06-19', 'Smart TV app', '3.2', 'Sign-up on TV moves to the new platform'),
        ('2025-06-19', 'Android TV app', '1.2', 'Sign-up on TV moves to the new platform'),
        ('2025-06-19', 'Tablet apps', '7.2', 'Sign-up on tablets moves to the new platform'),
        ('2025-07-08', 'iOS app', '7.2', 'Picture in picture'),
        ('2025-07-22', 'Android app', '7.2', 'Picture in picture'),
        ('2025-08-05', 'Viewing service', '12.0', 'New ingestion pipeline'),
        ('2025-08-19', 'Web', '2025.33', 'Search results grouped by series'),
        ('2025-09-08', 'Billing', '4.0', 'Card processing moves to the new provider'),
        ('2025-09-16', 'Smart TV app', '3.3', 'Faster menus'),
        ('2025-09-30', 'iOS app', '7.3', 'Crash fixes'),
        ('2025-10-14', 'Subscription platform', '8.4', 'Plan change flow rebuilt'),
        ('2025-10-20', 'Android TV app', '1.4', 'Player fixes'),
        ('2025-10-27', 'Smart TV app', '3.4', 'Player update'),
        ('2025-10-30', 'Web', '2025.44', 'New prices on sign-up and plan pages'),
        ('2025-10-30', 'iOS app', '7.4', 'New prices on plan pages'),
        ('2025-10-30', 'Android app', '7.4', 'New prices on plan pages'),
        ('2025-11-11', 'Viewing service', '12.1', 'Duplicate heartbeat filter on reconnect (shadow mode)'),
        ('2025-11-25', 'Web', '2025.48', 'Holiday collections'),
        ('2025-12-09', 'Smart TV app', '3.5', 'Holiday collections'),
        ('2026-01-13', 'iOS app', '7.5', 'Accessibility fixes'),
        ('2026-01-27', 'Android app', '7.5', 'Accessibility fixes'),
        ('2026-02-10', 'Subscription platform', '8.6', 'Gift card balance on the account page'),
    ]
    wb = Workbook()
    ws = wb.active
    ws.title = 'Releases'
    ws.append(['Release date', 'Product', 'Version', 'Release note'])
    for c in ws[1]:
        c.font = Font(bold=True)
    for r in R:
        ws.append(list(r))
    for col, w in zip('ABCD', [13, 24, 10, 70]):
        ws.column_dimensions[col].width = w
    wb.save(path)
    xlsx_scrub(path, 'Tamara Delgado', '2026-02-24T15:40:00Z', 'Product release log')
    return R


# ------------------------------------------------------------------------------------------------------- distractors

def cancellation_survey(path, T, rng):
    """The exit survey shown when a trialist cancels: about one in six answer; reasons multi-select."""
    st = T.start.values
    cancel = ~T.keep.values & (st >= world.ts('2024-11-01 00:00').value)
    idx = np.where(cancel & (rng.random(len(T)) < 0.17))[0]
    when = T.end.values[idx] - (rng.uniform(0.02, 3.0, len(idx)) * world.DAY).astype('int64')
    when = np.maximum(when, st[idx] + 3600 * world.NS)
    newp = when >= world.ts('2025-11-01 00:00').value
    run = T.run.values[idx]
    p_price = np.where(newp, 0.44, 0.19)
    p_new = np.where(run, 0.12, 0.27)
    p_fin = np.where(run, 0.10, 0.24)
    reasons = []
    for i in range(len(idx)):
        rr = []
        if rng.random() < p_price[i]:
            rr.append('too_expensive')
        if rng.random() < p_new[i]:
            rr.append('not_enough_new')
        if rng.random() < p_fin[i]:
            rr.append('finished_what_i_wanted')
        if rng.random() < 0.07:
            rr.append('technical_problems')
        if rng.random() < 0.06:
            rr.append('signed_up_elsewhere')
        if not rr:
            rr.append('other')
        reasons.append(';'.join(rr))
    acct = np.where(T.pre.values[idx], T.acct_old.values[idx], T.acct_new.values[idx])
    out = pd.DataFrame({'response_id': ['XS-%07d' % x for x in rng.choice(np.arange(1_000_000, 9_999_999), len(idx), replace=False)],
                        'account_ref': acct,
                        'responded_utc': pd.to_datetime(when).strftime('%Y-%m-%dT%H:%M:%SZ'),
                        'reasons': reasons})
    out = out.iloc[np.argsort(when, kind='stable')].reset_index(drop=True)
    out.to_csv(path, index=False)
    return out


def paid_media(path, T, rng):
    """The paid media team's monthly report: spend and platform-reported trial starts by channel."""
    st = pd.to_datetime(T.start.values).tz_localize('UTC').tz_convert(TOR)
    month = st.strftime('%Y-%m')
    rows = []
    for m in sorted(set(month)):
        if m < '2024-11' or m > '2026-01':
            continue
        sel = month == m
        for ch, cpa in (('search', 31.0), ('social', 23.5), ('tv_ad', 58.0)):
            n = int((T.channel.values[sel] == ch).sum())
            rep = int(round(n * rng.uniform(1.06, 1.22)))
            spend = round(n * cpa * rng.uniform(0.9, 1.12), 2)
            if ch == 'social' and m >= '2025-11':
                spend = round(spend * 1.31, 2)
            rows.append((m, ch, spend, rep, int(round(rep * rng.uniform(38, 61)))))
    df = pd.DataFrame(rows, columns=['month', 'channel', 'spend_cad', 'platform_trial_starts', 'clicks'])
    wb = Workbook()
    ws = wb.active
    ws.title = 'Paid media by month'
    ws.append(['Month', 'Channel', 'Spend (CAD)', 'Trial starts reported by platform', 'Clicks'])
    for c in ws[1]:
        c.font = Font(bold=True)
    for r in df.itertuples(index=False):
        ws.append(list(r))
    ws.append([])
    ws.append(['Platform-reported trial starts use each platform\'s own attribution window and are not the trial register.'])
    for col, w in zip('ABCDE', [10, 10, 14, 32, 10]):
        ws.column_dimensions[col].width = w
    wb.save(path)
    xlsx_scrub(path, 'Paid Media', '2026-02-12T14:05:00Z', 'Paid media by month')
    return df
