"""The two documents in the pack: the Copperfield trial's final report and the ICB's service specification."""
import datetime as dt
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether

BASE = ParagraphStyle('base', fontName='Helvetica', fontSize=9.6, leading=13.2, spaceAfter=5)
SMALL = ParagraphStyle('small', parent=BASE, fontSize=8.2, leading=10.6, textColor=colors.HexColor('#333333'))
H1 = ParagraphStyle('h1', parent=BASE, fontName='Helvetica-Bold', fontSize=15, leading=19, spaceAfter=6)
H2 = ParagraphStyle('h2', parent=BASE, fontName='Helvetica-Bold', fontSize=10.6, leading=14, spaceBefore=7, spaceAfter=3)
CELL = ParagraphStyle('cell', parent=BASE, fontSize=8.6, leading=11, spaceAfter=0)


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
                            creator=author, producer=author, invariant=1)
    return doc, on_page


def _table(rows, widths, header_rows=1, align_right_from=1):
    t = Table([[Paragraph(str(c), CELL) for c in r] for r in rows], colWidths=[w * mm for w in widths], hAlign='LEFT')
    st = [('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#999999')),
          ('BACKGROUND', (0, 0), (-1, header_rows - 1), colors.HexColor('#dfe8f2')),
          ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2)]
    t.setStyle(TableStyle(st))
    return t


def pct(r, n):
    return '%.1f' % (100.0 * r / n)


def report(path, st):
    doc, on_page = _doc(path, 'Copperfield neonatal outreach trial: final report', 'Copperfield neonatal outreach trial office',
                        'Final report version 1.0', 'Ravensby and Weald Community Health NHS Trust  |  Sedgefold and Wennby NHS Trust',
                        'Copperfield neonatal outreach trial, final report v1.0, June 2026')
    o, c = st['outreach'], st['usual care']
    lo, hi = st['ci']
    red = 100 * (1 - st['rr'])
    s = []
    s.append(Paragraph('Neonatal outreach after discharge: the Copperfield randomised trial', H1))
    s.append(Paragraph('Final report, version 1.0, 26 June 2026', BASE))
    s.append(Paragraph('Chief investigator: Dr Lucy Coates, Consultant Neonatologist, Copperfield Hospital. '
                       'Co-investigator: Hugh Brown, Community Midwifery Manager, Ravensby and Weald Community Health NHS Trust. '
                       'Approved by the trial steering committee on 22 June 2026.', SMALL))
    s.append(Spacer(1, 4))
    s.append(Paragraph('Summary', H2))
    s.append(Paragraph(
        'Babies who go home from the postnatal ward with a feeding or jaundice risk are readmitted more often than other babies, '
        'mostly for jaundice and for feeding problems with weight loss. Between 1 April 2024 and 31 March 2026 we randomised '
        '%s babies discharged home from Copperfield Hospital with the newborn feeding or jaundice risk flag to the neonatal '
        'outreach service or to usual community midwifery care. %s parents later withdrew consent. Of %s babies analysed in the '
        'outreach arm, %s (%s per cent) had an unplanned readmission within 28 days of discharge, against %s of %s (%s per cent) '
        'with usual care: a risk ratio of %.2f (95 per cent confidence interval %.2f to %.2f).' % (
            '{:,}'.format(st['randomised']), st['withdrawn'], '{:,}'.format(o['n']), o['r'], pct(o['r'], o['n']), c['r'],
            '{:,}'.format(c['n']), pct(c['r'], c['n']), st['rr'], lo, hi), BASE))
    s.append(Paragraph('Methods', H2))
    s.append(Paragraph(
        '<b>Design and setting.</b> An individually randomised, unblinded trial at the Copperfield Hospital maternity unit. '
        '<b>Participants.</b> Babies discharged home from the postnatal ward or birth centre with the newborn feeding or jaundice '
        'risk flag recorded on the discharge record, whose parents consented on the ward. Twins and other multiple births were '
        'outside the protocol. <b>Randomisation.</b> One to one, computer generated, allocation concealed until the midwife '
        'completed the discharge check. <b>Intervention.</b> The neonatal outreach service: a telephone contact from an outreach '
        'nurse, a home visit with a weight and transcutaneous bilirubin check and feeding support, and telephone follow-up to '
        'day 28. <b>Comparator.</b> Routine postnatal visits by the community midwifery team (usual care). <b>Outcome.</b> An unplanned '
        'admission of the baby to any hospital in the Ravensby and Weald area within 28 days of discharge home, taken from the '
        'integrated care board admissions extract; a baby counts once. <b>Analysis.</b> By allocated arm, as a risk ratio with a '
        '95 per cent confidence interval. Three subgroups were specified before the analysis: gestation at birth, feeding at '
        'discharge, and the primary risk reason recorded at randomisation.', BASE))
    s.append(Paragraph('Results', H2))
    s.append(Paragraph('Table 1. Babies randomised and analysed', SMALL))
    n_o_rand = o['n'] + sum(1 for _ in range(0))
    s.append(_table([['', 'Neonatal outreach', 'Usual community care', 'All'],
                     ['Randomised', '{:,}'.format(st['rand_o']), '{:,}'.format(st['rand_c']), '{:,}'.format(st['randomised'])],
                     ['Withdrew consent', str(st['rand_o'] - o['n']), str(st['rand_c'] - c['n']), str(st['withdrawn'])],
                     ['Included in the analysis', '{:,}'.format(o['n']), '{:,}'.format(c['n']), '{:,}'.format(o['n'] + c['n'])]],
                    [52, 30, 30, 30]))
    s.append(Spacer(1, 5))
    s.append(Paragraph('Table 2. Unplanned readmission within 28 days of discharge', SMALL))
    s.append(_table([['', 'Babies', 'Readmitted', 'Per cent'],
                     ['Neonatal outreach', '{:,}'.format(o['n']), str(o['r']), pct(o['r'], o['n'])],
                     ['Usual community care', '{:,}'.format(c['n']), str(c['r']), pct(c['r'], c['n'])],
                     ['Risk ratio (95% CI)', '%.2f (%.2f to %.2f)' % (st['rr'], lo, hi), '', '']], [52, 40, 30, 22]))
    s.append(Spacer(1, 5))
    rows = [['Subgroup', 'Neonatal outreach: readmitted / babies', 'Usual community care: readmitted / babies', 'Risk ratio']]
    for name, v in st['subgroups'].items():
        rows.append([name, '%d / %s' % (v['ro'], '{:,}'.format(v['no'])), '%d / %s' % (v['rc'], '{:,}'.format(v['nc'])), '%.2f' % v['rr']])
    s.append(KeepTogether([Paragraph('Table 3. Pre-specified subgroups', SMALL), _table(rows, [52, 42, 42, 22])]))
    p = st['p_interaction']
    s.append(Spacer(1, 5))
    s.append(Paragraph(
        'The trial was not powered for subgroups. The effect did not differ by gestation, feeding at discharge or the primary '
        'risk reason recorded at randomisation (tests for interaction p = %.2f, %.2f and %.2f).' % (
            p['gestation'], p['feeding'], p['primary reason']), BASE))
    s.append(Paragraph(
        'Outreach contacts were recorded by the nurses on the service tablet application; the contact log is held by Ravensby '
        'and Weald Community Health NHS Trust.', BASE))
    s.append(Paragraph('Conclusion', H2))
    s.append(Paragraph(
        'In babies discharged with a feeding or jaundice risk, the neonatal outreach service cut unplanned readmission within '
        '28 days by about %d per cent. The steering committee recommends that the integrated care board considers the service '
        'for the other maternity units in the area.' % int(round(red, 0)), BASE))
    doc.build(s, onFirstPage=on_page, onLaterPages=on_page)


def spec(path):
    doc, on_page = _doc(path, 'Service specification: neonatal outreach after discharge, 2027/28',
                        'Ravensby and Weald Integrated Care Board', 'SS-MAT-027 version 1.2',
                        'Ravensby and Weald Integrated Care Board', 'SS-MAT-027 Neonatal outreach after discharge 2027/28, version 1.2')
    s = []
    s.append(Paragraph('Service specification: neonatal outreach after discharge, 2027/28', H1))
    s.append(_table([['Reference', 'SS-MAT-027'], ['Version', '1.2'],
                     ['Issued', '21 September 2026'], ['Owner', 'Kathryn Thompson, Head of Maternity and Children\'s Commissioning'],
                     ['Approved', 'Integrated Care Board, 17 September 2026'], ['Provider', 'Ravensby and Weald Community Health NHS Trust']],
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
    s.append(Spacer(1, 10))
    s.append(_table([['Signed for the Integrated Care Board', 'Signed for the provider'],
                     ['Kathryn Thompson, Head of Maternity and Children\'s Commissioning', 'Director of Nursing, Ravensby and Weald Community Health NHS Trust'],
                     ['Date: 21 September 2026', 'Date: 24 September 2026']], [85, 85]))
    doc.build(s, onFirstPage=on_page, onLaterPages=on_page)
