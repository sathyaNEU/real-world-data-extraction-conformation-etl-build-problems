"""The two documents in the pack: the Copperfield trial's final report and the ICB's service specification."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak

import world as W

BASE = ParagraphStyle('base', fontName='Helvetica', fontSize=9.6, leading=13.2, spaceAfter=5)
SMALL = ParagraphStyle('small', parent=BASE, fontSize=8.2, leading=10.6, textColor=colors.HexColor('#333333'))
H1 = ParagraphStyle('h1', parent=BASE, fontName='Helvetica-Bold', fontSize=15, leading=19, spaceAfter=6)
H2 = ParagraphStyle('h2', parent=BASE, fontName='Helvetica-Bold', fontSize=10.6, leading=14, spaceBefore=7, spaceAfter=3, keepWithNext=1)
H3 = ParagraphStyle('h3', parent=BASE, fontName='Helvetica-Bold', fontSize=9.6, leading=13, spaceBefore=4, spaceAfter=2, keepWithNext=1)
CELL = ParagraphStyle('cell', parent=BASE, fontSize=8.6, leading=11, spaceAfter=0)
TITLE = ParagraphStyle('title', parent=BASE, fontName='Helvetica-Bold', fontSize=19, leading=24, spaceAfter=10)


def _doc(path, title, author, subject, header, footer):
    def on_page(c, d):
        c.saveState()
        c.setFont('Helvetica-Bold', 8.5)
        c.setFillColor(colors.HexColor('#1f4e79'))
        c.drawString(18 * mm, A4[1] - 12 * mm, header)
        c.setFont('Helvetica', 7.8)
        c.setFillColor(colors.HexColor('#555555'))
        c.drawString(18 * mm, 10 * mm, footer)
        c.drawRightString(A4[0] - 18 * mm, 10 * mm, 'Page %d' % d.page)
        c.restoreState()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=20 * mm,
                            bottomMargin=18 * mm, title=title, author=author, subject=subject,
                            creator='', producer='', invariant=1)
    return doc, on_page


def _table(rows, widths, header_rows=1):
    t = Table([[Paragraph(str(c), CELL) for c in r] for r in rows], colWidths=[w * mm for w in widths], hAlign='LEFT')
    st = [('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#999999')),
          ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2)]
    if header_rows:
        st.append(('BACKGROUND', (0, 0), (-1, header_rows - 1), colors.HexColor('#dfe8f2')))
    t.setStyle(TableStyle(st))
    return t


def pct(r, n):
    return '%.1f' % (100.0 * r / n)


def npct(r, n):
    return '%s (%s)' % ('{:,}'.format(r), pct(r, n))


# the report's own wording for the risk reasons and feeding (the trial unit's labels, not the maternity system's)
REASON_TEXT = {'LPT': 'Late preterm, 35 or 36 weeks', 'BFP': 'Breastfed, first baby', 'EDC': 'Early discharge, under 18 hours',
               'WTL': 'Weight loss of 8 per cent or more', 'VJD': 'Jaundice visible at discharge',
               'SPH': 'Sibling treated with phototherapy'}
FEED_TEXT = {'Exclusive breast milk': 'Fed breast milk only', 'Breast and formula': 'Fed breast milk and formula',
             'Formula': 'Fed formula only'}


def report(path, st):
    doc, on_page = _doc(path, 'Copperfield neonatal outreach trial: final report', 'Copperfield neonatal outreach trial office',
                        'Final report version 1.0', 'Ravensby and Weald Community Health NHS Trust  |  Sedgefold and Wennby NHS Trust',
                        'Copperfield neonatal outreach trial, final report v1.0, 26 June 2026')
    o, c = st['outreach'], st['usual care']
    lo, hi = st['ci']
    red = 100 * (1 - st['rr'])
    p = st['p_interaction']
    ss = st['sample_size']
    bl = st['baseline']
    s = []
    # ------------------------------------------------------------------ title page
    s.append(Spacer(1, 30))
    s.append(Paragraph('Neonatal outreach after discharge: the Copperfield randomised trial', TITLE))
    s.append(Paragraph('Final report', H2))
    s.append(Spacer(1, 6))
    s.append(_table([
        ['Report version', '1.0, 26 June 2026'],
        ['Protocol', 'Version 2.0, 14 February 2024'],
        ['Registration', 'Sedgefold and Wennby NHS Trust research register, SW/RD/23/114'],
        ['Sponsor', 'Sedgefold and Wennby NHS Trust, research and development office'],
        ['Funder', 'Ravensby and Weald Integrated Care Board, maternity transformation fund'],
        ['Chief investigator', 'Dr Lucy Coates, Consultant Neonatologist, Copperfield Hospital'],
        ['Co-investigator', 'Hugh Brown, Community Midwifery Manager, Ravensby and Weald Community Health NHS Trust'],
        ['Trial statistician', 'Eric Lee, Sedgefold and Wennby NHS Trust research and development office'],
        ['Trial manager', 'Bernard Lord, Copperfield Hospital'],
        ['Approval', 'Trial steering committee, 22 June 2026'],
    ], [40, 128], header_rows=0))
    s.append(Spacer(1, 10))
    s.append(Paragraph('Summary', H2))
    s.append(Paragraph(
        '<b>Background.</b> Babies who go home from the postnatal ward with a feeding or jaundice risk are readmitted more often '
        'than other babies, mostly for jaundice and for feeding problems with weight loss. <b>Methods.</b> An individually '
        'randomised trial at Copperfield Hospital: babies discharged home between 1 April 2024 and 31 March 2026 with the '
        'newborn feeding or jaundice risk flag were allocated to the neonatal outreach service or to usual community midwifery '
        'care. <b>Results.</b> %s babies were randomised and %s analysed. %s of %s babies with outreach (%s per cent) had an '
        'unplanned readmission within 28 days of discharge, against %s of %s (%s per cent) with usual care: a risk ratio of '
        '%.2f (95 per cent confidence interval %.2f to %.2f). <b>Conclusion.</b> The service cut unplanned readmission within '
        '28 days by about %d per cent.' % (
            '{:,}'.format(st['randomised']), '{:,}'.format(o['n'] + c['n']), o['r'], '{:,}'.format(o['n']), pct(o['r'], o['n']),
            c['r'], '{:,}'.format(c['n']), pct(c['r'], c['n']), st['rr'], lo, hi, int(round(red, 0))), BASE))
    s.append(PageBreak())
    # ------------------------------------------------------------------ background and methods
    s.append(Paragraph('1. Background', H2))
    s.append(Paragraph(
        'Most readmissions of newborn babies in the first weeks at home are for jaundice needing phototherapy or for feeding '
        'difficulty with weight loss. Late preterm babies, breastfed first babies, babies discharged early and babies already '
        'losing weight are at higher risk, and the maternity units in the area flag them on the discharge record. Copperfield '
        'Hospital set up a neonatal outreach service for flagged babies in 2023 and agreed with the integrated care board to '
        'test it in a randomised trial before any wider rollout.', BASE))
    s.append(Paragraph('2. Methods', H2))
    s.append(Paragraph('2.1 Design and setting', H3))
    s.append(Paragraph('An individually randomised, unblinded, parallel group trial at the Copperfield Hospital maternity unit, '
                       'recruiting from 1 April 2024 to 31 March 2026.', BASE))
    s.append(Paragraph('2.2 Participants', H3))
    s.append(Paragraph('Babies discharged home from the postnatal ward or the birth centre with the newborn feeding or jaundice '
                       'risk flag recorded on the discharge record. Twins and other multiple births were outside the protocol. '
                       'Parents were told about the trial antenatally and on the ward and could decline at any point (opt-out '
                       'consent); parents who withdrew after randomisation were removed from the analysis with their data.', BASE))
    s.append(Paragraph('2.3 Randomisation', H3))
    s.append(Paragraph('One to one, computer generated in permuted blocks of varying size, concealed until the midwife completed '
                       'the discharge check, when the main risk reason on the record was entered with the allocation.', BASE))
    s.append(Paragraph('2.4 Intervention and comparator', H3))
    s.append(Paragraph(
        '<b>Intervention.</b> The neonatal outreach service. An outreach nurse first telephones the family, assesses feeding, '
        'the baby\'s weight and jaundice with the parent and arranges a review where needed; a home visit follows, with a weight '
        'and transcutaneous bilirubin check and feeding support, and telephone follow-up continues to day 28. '
        '<b>Comparator.</b> Routine postnatal visits by the community midwifery team (usual care).', BASE))
    s.append(Paragraph('2.5 Outcomes', H3))
    s.append(Paragraph(
        '<b>Primary outcome.</b> An unplanned admission of the baby to any hospital in the Ravensby and Weald area within 28 days '
        'of discharge home, taken from the integrated care board admissions extract; a baby counts once. <b>Process '
        'measures</b>, from the outreach service\'s contact log: home visits in which the nurse saw the baby, and telephone '
        'calls that reached a parent, in the 28 days after discharge. <b>Harms.</b> Serious adverse events reported to the '
        'trial steering committee.', BASE))
    s.append(Paragraph('2.6 Sample size', H3))
    s.append(Paragraph(
        'The protocol assumed that %d per cent of babies would be readmitted with usual care and sought to detect a %d per cent '
        'relative reduction with %d per cent power at the two-sided %d per cent level, which needs %s babies in each arm; '
        'recruitment ran for two years to allow for withdrawals.' % (
            int(round(100 * ss['p1'])), int(round(100 * ss['cut'])), int(round(100 * ss['power'])), int(round(100 * ss['alpha'])),
            '{:,}'.format(ss['per_arm'])), BASE))
    s.append(Paragraph('2.7 Statistical analysis', H3))
    s.append(Paragraph(
        'The primary analysis estimated one treatment effect for all babies analysed as randomised: the risk ratio of '
        'unplanned readmission with outreach against usual care, with its 95 per cent confidence interval. The pre-specified '
        'subgroups (gestation at birth, feeding at discharge and the main risk reason recorded at randomisation) were examined '
        'only as tests for interaction and were not used to adjust or divide the primary estimate.', BASE))
    # ------------------------------------------------------------------ results
    s.append(Paragraph('3. Results', H2))
    s.append(Paragraph('3.1 Participant flow', H3))
    s.append(Paragraph(
        'Between 1 April 2024 and 31 March 2026, %s babies went home from Copperfield Hospital with the risk flag; %s were twins '
        'and outside the protocol, and the remaining %s were randomised. Parents of %d babies withdrew after randomisation.' % (
            '{:,}'.format(st['flagged_cfh']), st['multiples_out'], '{:,}'.format(st['randomised']), st['withdrawn']), BASE))
    s.append(Paragraph('Table 1. Babies randomised and analysed', SMALL))
    s.append(_table([['', 'Neonatal outreach', 'Usual community care', 'All'],
                     ['Randomised', '{:,}'.format(st['rand_o']), '{:,}'.format(st['rand_c']), '{:,}'.format(st['randomised'])],
                     ['Withdrew consent', str(st['rand_o'] - o['n']), str(st['rand_c'] - c['n']), str(st['withdrawn'])],
                     ['Included in the analysis', '{:,}'.format(o['n']), '{:,}'.format(c['n']), '{:,}'.format(o['n'] + c['n'])]],
                    [52, 34, 38, 24]))
    s.append(Spacer(1, 5))
    s.append(Paragraph('3.2 Baseline characteristics', H3))
    bo, bc = bl['outreach'], bl['usual care']
    rows = [['', 'Neonatal outreach (n = %s)' % '{:,}'.format(bo['n']), 'Usual community care (n = %s)' % '{:,}'.format(bc['n'])],
            ['<b>Gestation at birth, weeks: n (per cent)</b>', '', '']]
    for (lab, xo), (_, xc) in zip(bo['gest'], bc['gest']):
        rows.append([lab, npct(xo, bo['n']), npct(xc, bc['n'])])
    rows.append(['<b>Birth weight, g: mean (SD)</b>', '{:,.0f} ({:.0f})'.format(bo['bw_mean'], bo['bw_sd']),
                 '{:,.0f} ({:.0f})'.format(bc['bw_mean'], bc['bw_sd'])])
    rows.append(['<b>Feeding at discharge: n (per cent)</b>', '', ''])
    for (lab, xo), (_, xc) in zip(bo['feed'], bc['feed']):
        rows.append([FEED_TEXT[lab], npct(xo, bo['n']), npct(xc, bc['n'])])
    rows.append(['<b>Main risk reason at randomisation: n (per cent)</b>', '', ''])
    for (r, xo), (_, xc) in zip(bo['primary'], bc['primary']):
        rows.append([REASON_TEXT[r], npct(xo, bo['n']), npct(xc, bc['n'])])
    rows.append(['<b>Hours from birth to discharge: median (IQR)</b>', '%.1f (%.1f to %.1f)' % bo['stay'], '%.1f (%.1f to %.1f)' % bc['stay']])
    s.append(KeepTogether([Paragraph('Table 2. Baseline characteristics of the babies analysed', SMALL), _table(rows, [72, 48, 48])]))
    s.append(Spacer(1, 5))
    s.append(Paragraph('3.3 Primary outcome', H3))
    s.append(Paragraph('Table 3. Unplanned readmission within 28 days of discharge', SMALL))
    s.append(_table([['', 'Babies', 'Readmitted', 'Per cent'],
                     ['Neonatal outreach', '{:,}'.format(o['n']), str(o['r']), pct(o['r'], o['n'])],
                     ['Usual community care', '{:,}'.format(c['n']), str(c['r']), pct(c['r'], c['n'])],
                     ['Risk ratio (95% CI)', '%.2f (%.2f to %.2f)' % (st['rr'], lo, hi), '', '']], [52, 40, 30, 22]))
    s.append(Spacer(1, 5))
    s.append(Paragraph('3.4 Pre-specified subgroups', H3))
    rows = [['Subgroup', 'Neonatal outreach: readmitted / babies', 'Usual community care: readmitted / babies', 'Risk ratio']]
    for name, v in st['subgroups'].items():
        rows.append([name, '%d / %s' % (v['ro'], '{:,}'.format(v['no'])), '%d / %s' % (v['rc'], '{:,}'.format(v['nc'])), '%.2f' % v['rr']])
    s.append(KeepTogether([Paragraph('Table 4. Pre-specified subgroups', SMALL), _table(rows, [52, 42, 42, 22])]))
    s.append(Spacer(1, 5))
    s.append(Paragraph(
        'The trial was not powered for subgroups. The effect did not differ by gestation, feeding at discharge or the main risk '
        'reason recorded at randomisation (tests for interaction p = %.2f, %.2f and %.2f); the estimates by main risk reason are '
        'in supplementary table S2.' % (p['gestation'], p['feeding'], p['primary reason']), BASE))
    s.append(Paragraph('3.5 Process measures and harms', H3))
    s.append(Paragraph('The process measures are summarised in appendix B, published separately by Ravensby and Weald Community '
                       'Health NHS Trust with the service\'s contact log. No serious adverse event related to the service was '
                       'reported to the trial steering committee.', BASE))
    # ------------------------------------------------------------------ discussion
    s.append(Paragraph('4. Discussion', H2))
    s.append(Paragraph(
        'In babies discharged with a feeding or jaundice risk, the neonatal outreach service cut unplanned readmission within '
        '28 days by about %d per cent, and the effect was consistent across the pre-specified subgroups. The trial was large, '
        'recruited almost every eligible baby at the unit and took its outcome from the same admissions extract the integrated '
        'care board uses to monitor readmissions.' % int(round(red, 0)), BASE))
    s.append(Paragraph(
        '<b>Limitations.</b> The trial ran at one unit with one outreach team, and parents and staff knew the allocation. The '
        'outcome comes from the board\'s admissions extract, so a baby admitted outside the area is not counted. Subgroup '
        'analyses were not powered and are reported as tests for interaction only. Units whose case mix or community staffing '
        'differ from Copperfield\'s may see a different effect.', BASE))
    s.append(Paragraph('5. Conclusion and recommendation', H2))
    s.append(Paragraph('The steering committee recommends that the integrated care board considers the service for the other '
                       'maternity units in the area.', BASE))
    s.append(Paragraph('Appendices: A, trial steering committee membership; B, process measures (published separately); '
                       'supplementary table S2, estimates by main risk reason.', SMALL))
    doc.build(s, onFirstPage=on_page, onLaterPages=on_page)


def spec(path):
    doc, on_page = _doc(path, 'Service specification: neonatal outreach after discharge, 2027/28',
                        'Ravensby and Weald Integrated Care Board', 'SS-MAT-027 version 1.2',
                        'Ravensby and Weald Integrated Care Board', 'SS-MAT-027 Neonatal outreach after discharge 2027/28, version 1.2')
    s = []
    s.append(Paragraph('Service specification: neonatal outreach after discharge, 2027/28', H1))
    s.append(_table([['Reference', 'SS-MAT-027'], ['Version', '1.2'],
                     ['Issued', '20 October 2026'], ['Owner', 'Kathryn Thompson, Head of Maternity and Children\'s Commissioning'],
                     ['Approved', 'Integrated Care Board, 15 October 2026'], ['Provider', 'Ravensby and Weald Community Health NHS Trust']],
                    [32, 120], header_rows=0))
    s.append(Spacer(1, 4))
    s.append(Paragraph('1. Purpose', H2))
    s.append(Paragraph('To reduce unplanned readmissions of newborn babies in the weeks after they go home from the maternity '
                       'units in the Ravensby and Weald area.', BASE))
    s.append(Paragraph('2. The service', H2))
    s.append(Paragraph('The neonatal outreach service evaluated in the Copperfield randomised trial (final report, June 2026), '
                       'delivered to the trial\'s model. The service at Copperfield Hospital continues under its existing '
                       'contract and is outside this specification.', BASE))
    s.append(Paragraph('3. Eligible babies', H2))
    s.append(Paragraph('Every baby discharged home from the maternity units at Ravensby Royal Infirmary, Kellingworth University '
                       'Hospital, Sedgefold Hospital, St Aldric\'s Hospital and Wennby Community Hospital with the newborn feeding '
                       'or jaundice risk flag recorded on the discharge record. Twins and other multiple births are eligible.', BASE))
    s.append(Paragraph('4. Referral', H2))
    s.append(Paragraph('Babies are referred to the service through the community midwifery office, which receives each '
                       'unit\'s discharge notifications.', BASE))
    s.append(Paragraph('5. Outcome measure', H2))
    s.append(Paragraph('An unplanned readmission is an emergency admission of the baby to any hospital in the Ravensby and Weald '
                       'area within 28 days of discharge home. A baby counts once however many admissions it has, and a transfer '
                       'between hospitals during one stay is part of that admission.', BASE))
    s.append(Paragraph('6. Posts', H2))
    s.append(Paragraph('The Board has funded 30 whole-time outreach nurse posts from 1 April 2027, sized to offer the service to '
                       'every eligible baby discharged from the five units.', BASE))
    s.append(Paragraph('7. Allocation of posts', H2))
    s.append(Paragraph('Each unit\'s share of the 30 posts follows its share of the readmissions the service is expected to avoid '
                       'among the unit\'s eligible babies over the planning basis year. Each unit takes the whole posts in its share; '
                       'the posts left over go one at a time to the units with the largest remaining fractions.', BASE))
    s.append(Paragraph('8. Planning basis', H2))
    s.append(Paragraph('Activity for 2027/28 is planned at the level of the twelve months to 30 September 2026: babies discharged '
                       'home from 1 October 2025 to 30 September 2026 inclusive.', BASE))
    s.append(Paragraph('9. Reporting', H2))
    s.append(Paragraph('The provider reports each quarter the eligible babies referred, the contacts made and the unplanned '
                       'readmissions among eligible babies, by unit.', BASE))
    s.append(Spacer(1, 8))
    s.append(KeepTogether([Paragraph('Revision history', H2), _table([
        ['Version', 'Date', 'Change'],
        ['1.0', '12 March 2026', 'First issue, for consultation with the provider and the two hospital trusts'],
        ['1.1', '9 July 2026', 'Outcome measure aligned with the Copperfield trial final report; 30 posts funded from 1 April 2027'],
        ['1.2', '20 October 2026', 'Planning basis set to the twelve months to 30 September 2026; allocation of posts added as section 7'],
    ], [18, 30, 120])]))
    s.append(Spacer(1, 10))
    s.append(_table([['Signed for the Integrated Care Board', 'Signed for the provider'],
                     ['Kathryn Thompson, Head of Maternity and Children\'s Commissioning',
                      'Frances Thomas, Director of Nursing, Ravensby and Weald Community Health NHS Trust'],
                     ['Date: 20 October 2026', 'Date: 22 October 2026']], [85, 85]))
    doc.build(s, onFirstPage=on_page, onLaterPages=on_page)
