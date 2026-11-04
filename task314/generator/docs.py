"""The documents in the pack: three water rate resolutions, the drought contingency plan, the district's dry-year
notice and the department's agenda report on the Stage 2 rate options."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak

import world as W

SERIF = 'Times-Roman'
SERIF_B = 'Times-Bold'
BASE = ParagraphStyle('base', fontName=SERIF, fontSize=11, leading=14.2, spaceAfter=7)
CENTER = ParagraphStyle('center', parent=BASE, alignment=1)
CENTER_B = ParagraphStyle('centerb', parent=BASE, alignment=1, fontName=SERIF_B)
HEAD = ParagraphStyle('head', parent=BASE, fontName=SERIF_B, spaceBefore=6, spaceAfter=4, keepWithNext=1)
CELL = ParagraphStyle('cell', parent=BASE, fontSize=9.6, leading=11.8, spaceAfter=0)
CELL_B = ParagraphStyle('cellb', parent=CELL, fontName=SERIF_B)
SMALL = ParagraphStyle('small', parent=BASE, fontSize=9, leading=11, textColor=colors.HexColor('#333333'))
SANS = ParagraphStyle('sans', fontName='Helvetica', fontSize=9.8, leading=13.0, spaceAfter=6)
SANS_H = ParagraphStyle('sansh', parent=SANS, fontName='Helvetica-Bold', fontSize=10.6, leading=14, spaceBefore=8,
                        spaceAfter=3, keepWithNext=1)
SANS_H3 = ParagraphStyle('sansh3', parent=SANS, fontName='Helvetica-Bold', fontSize=9.8, spaceBefore=4, spaceAfter=2,
                         keepWithNext=1)
SANS_CELL = ParagraphStyle('sanscell', parent=SANS, fontSize=8.8, leading=11, spaceAfter=0)
SANS_TITLE = ParagraphStyle('sanstitle', parent=SANS, fontName='Helvetica-Bold', fontSize=17, leading=22, spaceAfter=6)

COUNCIL = ['Randy Silva', 'Ebony Valentine', 'Corey Lam', 'Nathaniel Cannon', 'Gary Riley', 'Julie Bowers']
MAYOR = 'Laurie Stuart'
CLERK = 'Beth Sheppard'
ATTORNEY = 'Theresa Howard'


def _doc(path, title, author, subject, creator, producer, header, footer, sans=False, total_pages=None):
    def on_page(c, d):
        c.saveState()
        c.setFont('Helvetica' if sans else SERIF, 8.5)
        c.setFillColor(colors.HexColor('#444444'))
        if header:
            c.drawRightString(letter[0] - 1.0 * inch, letter[1] - 0.55 * inch, header)
        c.drawString(1.0 * inch, 0.55 * inch, footer)
        if total_pages:
            c.drawRightString(letter[0] - 1.0 * inch, 0.55 * inch, 'Page %d of %d' % (d.page, total_pages))
        else:
            c.drawRightString(letter[0] - 1.0 * inch, 0.55 * inch, 'Page %d' % d.page)
        c.restoreState()
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=1.0 * inch, rightMargin=1.0 * inch, topMargin=0.9 * inch,
                            bottomMargin=0.85 * inch, title=title, author=author, subject=subject, creator=creator,
                            producer=producer, invariant=1)
    return doc, on_page


def _table(rows, widths, style=CELL, bold=CELL_B, header_rows=1, grid='#777777', shade='#e8e8e8'):
    data = []
    for i, r in enumerate(rows):
        data.append([Paragraph(str(c), bold if i < header_rows else style) for c in r])
    t = Table(data, colWidths=[w * inch for w in widths], hAlign='LEFT')
    st = [('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor(grid)), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
          ('TOPPADDING', (0, 0), (-1, -1), 2.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5)]
    if header_rows:
        st.append(('BACKGROUND', (0, 0), (-1, header_rows - 1), colors.HexColor(shade)))
    t.setStyle(TableStyle(st))
    return t


def two_pass(fn, path):
    """Build once in memory to count the pages, then build the document with its true page total."""
    import io
    n = fn(io.BytesIO(), None)
    fn(path, n)


def _money(x):
    return '%.2f' % x


def _letterhead_city(s, dept=None):
    s.append(Paragraph('CITY OF ARDLEY SPRINGS', ParagraphStyle('lh', parent=CENTER_B, fontSize=15, leading=18, spaceAfter=1)))
    s.append(Paragraph(dept or '100 East Main Street, Ardley Springs', ParagraphStyle('lh2', parent=CENTER, fontSize=9.5,
                                                                                      leading=11, spaceAfter=10)))


def _signatures(s, adopted_text, vote):
    s.append(Spacer(1, 6))
    s.append(Paragraph(adopted_text, BASE))
    s.append(Paragraph('AYES: %s' % ', '.join(vote[0]), BASE))
    s.append(Paragraph('NAYS: %s' % (', '.join(vote[1]) if vote[1] else 'None'), BASE))
    s.append(Paragraph('ABSENT: %s' % (', '.join(vote[2]) if vote[2] else 'None'), BASE))
    s.append(Spacer(1, 14))
    sig = Table([['_______________________________', '', '_______________________________'],
                 ['%s, Mayor' % MAYOR, '', 'ATTEST: %s, City Clerk' % CLERK]],
                colWidths=[2.9 * inch, 0.5 * inch, 2.9 * inch], hAlign='LEFT')
    sig.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), SERIF), ('FONTSIZE', (0, 0), (-1, -1), 10.5)]))
    s.append(KeepTogether([sig, Spacer(1, 14),
                           Paragraph('APPROVED AS TO FORM: _______________________________ %s, City Attorney' % ATTORNEY,
                                     BASE)]))


def _sfr_rows(sched):
    t = sched['tiers']
    lo1, lo2 = int(t[0][0] * 1000), int(t[1][0] * 1000)
    return [['Usage block (gallons a month)', 'Charge per 1,000 gallons'],
            ['0 to %s' % '{:,}'.format(lo1), _money(t[0][1])],
            ['%s to %s' % ('{:,}'.format(lo1 + 1), '{:,}'.format(lo2)), _money(t[1][1])],
            ['Over %s' % '{:,}'.format(lo2), _money(t[2][1])]]


# ---------------------------------------------------------------- the rate resolutions
def resolution_2021_44(path, total_pages=None):
    doc, on_page = _doc(path, 'Resolution No. 2021-44', 'bsheppard', 'Water rates and charges',
                        'Microsoft\xae Word for Microsoft 365', 'Microsoft\xae Word for Microsoft 365', '',
                        'Resolution No. 2021-44', total_pages=total_pages)
    s = []
    _letterhead_city(s)
    s.append(Paragraph('RESOLUTION NO. 2021-44', CENTER_B))
    s.append(Paragraph('A RESOLUTION OF THE CITY COUNCIL OF THE CITY OF ARDLEY SPRINGS ESTABLISHING RATES AND CHARGES '
                       'FOR WATER SERVICE AND REPEALING RESOLUTION NO. 2019-31', CENTER_B))
    s.append(Spacer(1, 4))
    for w in ['WHEREAS, Chapter 13.08 of the Ardley Springs Municipal Code provides that rates and charges for water '
              'service shall be established by resolution of the City Council; and',
              'WHEREAS, the City completed the annexation of the Fenwick Mesa area and the acquisition of the Fenwick '
              'Mesa Water Company system on September 30, 2021, and the former company\'s customers are now customers '
              'of the City water utility; and',
              'WHEREAS, the City Council held a public hearing on December 14, 2021, after notice published as '
              'required by law, and considered all testimony received;']:
        s.append(Paragraph(w, BASE))
    s.append(Paragraph('NOW, THEREFORE, BE IT RESOLVED by the City Council of the City of Ardley Springs as follows:', BASE))
    s.append(Paragraph('<b>Section 1.</b> The rates and charges for water service set out in Exhibit A are adopted and '
                       'apply to all bills issued on or after January 1, 2022, in every part of the City water service '
                       'area, including the Fenwick Mesa service area.', BASE))
    s.append(Paragraph('<b>Section 2.</b> Water is billed monthly on the consumption registered between consecutive '
                       'meter readings. Where a meter registers in hundred cubic feet, each hundred cubic feet is billed '
                       'as 748.052 gallons.', BASE))
    s.append(Paragraph('<b>Section 3.</b> Resolution No. 2019-31 is repealed effective with the bills issued on '
                       'January 1, 2022.', BASE))
    s.append(Paragraph('<b>Section 4.</b> The City Clerk shall certify to the adoption of this resolution.', BASE))
    _signatures(s, 'PASSED, APPROVED AND ADOPTED this 14th day of December, 2021, by the following vote:',
                (COUNCIL[:5], [], [COUNCIL[5]]))
    s.append(PageBreak())
    s.append(Paragraph('EXHIBIT A TO RESOLUTION NO. 2021-44', CENTER_B))
    s.append(Paragraph('Water Rates and Charges, effective with bills issued on or after January 1, 2022', CENTER))
    s.append(Paragraph('1. Single-family residential (rate code W10)', HEAD))
    s.append(_table([['Meter size', 'Monthly base charge'], ['3/4 inch', _money(W.SFR_OLD['base'][0.75])],
                     ['1 inch', _money(W.SFR_OLD['base'][1.0])]], [2.2, 2.2]))
    s.append(Spacer(1, 5))
    s.append(_table(_sfr_rows(W.SFR_OLD), [2.8, 2.2]))
    s.append(Paragraph('2. Multi-family residential (rate code W20)', HEAD))
    s.append(Paragraph('A monthly base charge of %s for each complete block of four dwelling units served by the meter, '
                       'and not less than one block; and %s for each 1,000 gallons.' % (_money(W.MFR_OLD['base']),
                                                                                       _money(W.MFR_OLD['vol'])), BASE))
    s.append(Paragraph('3. Commercial (rate code W30) and irrigation (rate code W40)', HEAD))
    s.append(_table([['Meter size', 'Monthly base charge'], ['1 inch', _money(W.COM_BASE_OLD[1.0])],
                     ['1-1/2 inch', _money(W.COM_BASE_OLD[1.5])], ['2 inch', _money(W.COM_BASE_OLD[2.0])]], [2.2, 2.2]))
    s.append(Spacer(1, 5))
    s.append(Paragraph('Commercial: %s for each 1,000 gallons. Irrigation: %s for each 1,000 gallons. Irrigation meters '
                       'are locked from November 1 to March 31 and the base charge is not billed on bills issued in '
                       'November through March.' % (_money(W.COM_VOL[0]), _money(W.IRR_VOL[0])), BASE))
    s.append(Paragraph('4. Other charges', HEAD))
    s.append(_table([['Charge', 'Amount'], ['Bulk water at the City fill station, each 100 gallons or part', '0.85'],
                     ['Account set-up', '25.00'], ['Returned payment', '30.00'],
                     ['Meter test at customer request (refunded if the meter registers over 101.5 per cent)', '60.00']],
                    [4.6, 1.4]))
    doc.build(s, onFirstPage=on_page, onLaterPages=on_page)
    return doc.page


def resolution_2023_12(path, total_pages=None):
    doc, on_page = _doc(path, 'Resolution No. 2023-12', 'bsheppard', 'Water rates and charges',
                        'Microsoft\xae Word for Microsoft 365', 'Microsoft\xae Word for Microsoft 365', '',
                        'Resolution No. 2023-12', total_pages=total_pages)
    s = []
    _letterhead_city(s)
    s.append(Paragraph('RESOLUTION NO. 2023-12', CENTER_B))
    s.append(Paragraph('A RESOLUTION OF THE CITY COUNCIL OF THE CITY OF ARDLEY SPRINGS AMENDING THE RATES AND CHARGES '
                       'FOR WATER SERVICE AND REPEALING RESOLUTION NO. 2021-44', CENTER_B))
    s.append(Spacer(1, 4))
    for w in ['WHEREAS, the City retained a consultant to prepare a cost of service and rate study for the water '
              'utility, and the study report dated February 2023 was presented to the City Council at its study '
              'session of March 14, 2023; and',
              'WHEREAS, the study recommended revised base charges and revised usage blocks for the single-family '
              'residential class, and adjustments to the charges of the other classes, to meet the utility\'s revenue '
              'requirement for fiscal years 2024 through 2028; and',
              'WHEREAS, notice of the proposed rates was mailed to every customer of record, and the City Council '
              'held a public hearing on May 23, 2023, and considered all testimony received;']:
        s.append(Paragraph(w, BASE))
    s.append(Paragraph('NOW, THEREFORE, BE IT RESOLVED by the City Council of the City of Ardley Springs as follows:', BASE))
    s.append(Paragraph('<b>Section 1.</b> The rates and charges for water service set out in Exhibit A are adopted and '
                       'apply to all bills issued on or after July 1, 2023, in every part of the City water service area.',
                       BASE))
    s.append(Paragraph('<b>Section 2.</b> Water is billed monthly on the consumption registered between consecutive '
                       'meter readings. Where a meter registers in hundred cubic feet, each hundred cubic feet is billed '
                       'as 748.052 gallons.', BASE))
    s.append(Paragraph('<b>Section 3.</b> Resolution No. 2021-44 is repealed effective with the bills issued on '
                       'July 1, 2023. Bills issued before that date remain subject to Resolution No. 2021-44.', BASE))
    s.append(Paragraph('<b>Section 4.</b> The City Clerk shall certify to the adoption of this resolution.', BASE))
    _signatures(s, 'PASSED, APPROVED AND ADOPTED this 23rd day of May, 2023, by the following vote:',
                (COUNCIL[:4] + COUNCIL[5:], [COUNCIL[4]], []))
    s.append(PageBreak())
    s.append(Paragraph('EXHIBIT A TO RESOLUTION NO. 2023-12', CENTER_B))
    s.append(Paragraph('Water Rates and Charges, effective with bills issued on or after July 1, 2023', CENTER))
    s.append(Paragraph('1. Single-family residential (rate code W10)', HEAD))
    s.append(_table([['Meter size', 'Monthly base charge'], ['3/4 inch', _money(W.SFR_NEW['base'][0.75])],
                     ['1 inch', _money(W.SFR_NEW['base'][1.0])]], [2.2, 2.2]))
    s.append(Spacer(1, 5))
    s.append(_table(_sfr_rows(W.SFR_NEW), [2.8, 2.2]))
    s.append(Paragraph('2. Multi-family residential (rate code W20)', HEAD))
    s.append(Paragraph('A monthly base charge of %s for each complete block of four dwelling units served by the meter, '
                       'and not less than one block; and %s for each 1,000 gallons.' % (_money(W.MFR_NEW['base']),
                                                                                       _money(W.MFR_NEW['vol'])), BASE))
    s.append(Paragraph('3. Commercial (rate code W30) and irrigation (rate code W40)', HEAD))
    s.append(_table([['Meter size', 'Monthly base charge'], ['1 inch', _money(W.COM_BASE_NEW[1.0])],
                     ['1-1/2 inch', _money(W.COM_BASE_NEW[1.5])], ['2 inch', _money(W.COM_BASE_NEW[2.0])]], [2.2, 2.2]))
    s.append(Spacer(1, 5))
    s.append(Paragraph('Commercial: %s for each 1,000 gallons. Irrigation: %s for each 1,000 gallons. Irrigation meters '
                       'are locked from November 1 to March 31 and the base charge is not billed on bills issued in '
                       'November through March.' % (_money(W.COM_VOL[1]), _money(W.IRR_VOL[1])), BASE))
    s.append(Paragraph('4. Other charges', HEAD))
    s.append(_table([['Charge', 'Amount'], ['Bulk water at the City fill station, each 100 gallons or part', '0.95'],
                     ['Account set-up', '25.00'], ['Returned payment', '30.00'],
                     ['Meter test at customer request (refunded if the meter registers over 101.5 per cent)', '60.00']],
                    [4.6, 1.4]))
    doc.build(s, onFirstPage=on_page, onLaterPages=on_page)
    return doc.page


def resolution_2024_17(path, total_pages=None):
    doc, on_page = _doc(path, 'Resolution No. 2024-17', 'bsheppard', 'Fenwick Mesa capital recovery charge',
                        'Microsoft\xae Word for Microsoft 365', 'Microsoft\xae Word for Microsoft 365', '',
                        'Resolution No. 2024-17', total_pages=total_pages)
    s = []
    _letterhead_city(s)
    s.append(Paragraph('RESOLUTION NO. 2024-17', CENTER_B))
    s.append(Paragraph('A RESOLUTION OF THE CITY COUNCIL OF THE CITY OF ARDLEY SPRINGS ESTABLISHING A FENWICK MESA '
                       'CAPITAL RECOVERY CHARGE ON WATER BILLS IN THE FENWICK MESA SERVICE AREA', CENTER_B))
    s.append(Spacer(1, 4))
    for w in ['WHEREAS, under the Fenwick Mesa Annexation and Utility Transfer Agreement of June 8, 2021, the City '
              'acquired the water system of the Fenwick Mesa Water Company and agreed that the cost of acquiring the '
              'system and of replacing its storage tank, its transmission main and its meters would be recovered from '
              'the accounts served in the Fenwick Mesa service area; and',
              'WHEREAS, the City issued its Water Revenue Bonds, Series 2021B, in the principal amount of USD 4,100,000, '
              'maturing over twenty years, to finance those costs; and',
              'WHEREAS, the Agreement provides that the recovery shall be made by a monthly charge on each account in '
              'the Fenwick Mesa service area, beginning no later than the July 2024 billing; and',
              'WHEREAS, the City Council held a public hearing on June 11, 2024, after notice mailed to every account '
              'in the Fenwick Mesa service area, and considered all testimony received;']:
        s.append(Paragraph(w, BASE))
    s.append(Paragraph('NOW, THEREFORE, BE IT RESOLVED by the City Council of the City of Ardley Springs as follows:', BASE))
    s.append(Paragraph('<b>Section 1.</b> A Fenwick Mesa capital recovery charge of USD %.2f a month is established on '
                       'each water account served in the Fenwick Mesa service area, of every customer class.' % W.FM_CHARGE,
                       BASE))
    s.append(Paragraph('<b>Section 2.</b> The charge applies to all bills issued on or after July 1, 2024, and ends '
                       'with the bills issued in June 2044, or earlier on the retirement of the Series 2021B bonds. It is '
                       'shown on each bill as a separate line.', BASE))
    s.append(Paragraph('<b>Section 3.</b> The rates and charges for water service in Resolution No. 2023-12 are not '
                       'otherwise amended and continue to apply in the Fenwick Mesa service area.', BASE))
    s.append(Paragraph('<b>Section 4.</b> Proceeds of the charge shall be deposited in the Fenwick Mesa debt service '
                       'account and used only for the Series 2021B bonds.', BASE))
    s.append(Paragraph('<b>Section 5.</b> The Fenwick Mesa service area is the area described in Exhibit A, being the '
                       'area served by the Fenwick Mesa Water Company on the date of transfer.', BASE))
    _signatures(s, 'PASSED, APPROVED AND ADOPTED this 11th day of June, 2024, by the following vote:',
                (COUNCIL[:3] + COUNCIL[4:], [], [COUNCIL[3]]))
    s.append(PageBreak())
    s.append(Paragraph('EXHIBIT A TO RESOLUTION NO. 2024-17', CENTER_B))
    s.append(Paragraph('Fenwick Mesa Service Area', CENTER))
    for w in ['The Fenwick Mesa service area comprises the lands within the following subdivisions and parcels, as '
              'recorded in the office of the County Recorder, together with any later division of those lands:',
              'Fenwick Mesa Subdivision, Filings 1 through 6; Caprock Estates, Filings 1 and 2; Rimrock Heights; '
              'Saltgrass Ranchettes; Chamisa Hills Planned Unit Development; Desert Willow Townhomes; Tableland Commons; '
              'and the unplatted parcels lying north of Windmill Road and east of the Gambel Oak Drive right-of-way that '
              'were served by the Fenwick Mesa Water Company on September 30, 2021.',
              'The boundary is shown on the Fenwick Mesa service area map, Water Department drawing W-2021-114, '
              'revision B, on file with the City Clerk. Where the map and this description differ, this description '
              'governs.',
              'Accounts in the service area are identified in the City billing system by the service area code FENWICK '
              'MESA. A premise later connected inside the boundary is included from its first bill.']:
        s.append(Paragraph(w, BASE))
    doc.build(s, onFirstPage=on_page, onLaterPages=on_page)
    return doc.page


# ---------------------------------------------------------------- the drought contingency plan
def drought_plan(path, total_pages=None):
    doc, on_page = _doc(path, 'Drought Contingency Plan, Revision 2', 'chaley', 'Ardley Springs Water Department',
                        'Microsoft\xae Word 2019', 'Microsoft\xae Word 2019',
                        'City of Ardley Springs Drought Contingency Plan, Rev. 2', 'Water Department, Water Resources Division',
                        sans=True, total_pages=total_pages)
    s = []
    s.append(Spacer(1, 70))
    s.append(Paragraph('CITY OF ARDLEY SPRINGS WATER DEPARTMENT', SANS_H))
    s.append(Paragraph('Drought Contingency Plan', SANS_TITLE))
    s.append(Paragraph('Revision 2, adopted by the City Council by Resolution No. 2025-08 on March 25, 2025', SANS))
    s.append(Spacer(1, 16))
    s.append(_table([['Rev.', 'Date', 'Description', 'By'],
                     ['0', 'April 12, 2016', 'Plan adopted (Resolution No. 2016-19).', 'Water Resources'],
                     ['1', 'May 26, 2020', 'Stage triggers tied to the district\'s annual allocation; Stage 4 added.',
                      'Water Resources'],
                     ['2', 'March 25, 2025', 'Fenwick Mesa service area brought into the plan; Section 5 on drought '
                      'rate measures rewritten; bulk fill station and City facility measures added to Stage 2.',
                      'Water Resources']],
                    [0.45, 1.2, 3.6, 1.15], style=SANS_CELL, bold=ParagraphStyle('sb', parent=SANS_CELL, fontName='Helvetica-Bold')))
    s.append(Spacer(1, 30))
    sig = Table([['Prepared by:', '_____________________________', 'Date: ____________'],
                 ['', 'Clifford Haley, Water Resources Manager', ''],
                 ['', '', ''],
                 ['Approved by:', '_____________________________', 'Date: ____________'],
                 ['', 'Jason Morgan, Utilities Director', '']],
                colWidths=[1.1 * inch, 3.0 * inch, 1.8 * inch], hAlign='LEFT')
    sig.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 9.5)]))
    s.append(sig)
    s.append(PageBreak())
    p = lambda t: s.append(Paragraph(t, SANS))
    h = lambda t: s.append(Paragraph(t, SANS_H))
    h3 = lambda t: s.append(Paragraph(t, SANS_H3))
    h('1. Purpose and authority')
    p('This plan sets out how the City of Ardley Springs Water Department responds to a shortage in the water '
      'available to the City, the stages of that response and the measures in each stage. It is adopted under '
      'Chapter 13.10 of the Municipal Code, which authorizes the City Council to declare a drought stage by '
      'resolution and the Utilities Director to implement the measures this plan assigns to that stage.')
    h3('1.1 Scope')
    p('The plan applies to every customer of the City water utility, in every customer class and in every part of the '
      'service area, including the Fenwick Mesa service area, and to the City\'s own departments and facilities.')
    h3('1.2 Definitions')
    s.append(_table([['Term', 'Meaning in this plan'],
                     ['Delivery season', 'May 1 to October 31, the season for which the district sets its allocation.'],
                     ['District allocation', 'The share of the City\'s contract entitlement the district will deliver '
                      'in a delivery season, as noticed by the district.'],
                     ['Production', 'Water taken from the district at the City\'s turnouts plus water pumped at the '
                      'City\'s wells.'],
                     ['Single-family residential account', 'An account billed under rate code W10.'],
                     ['Bill month', 'The calendar month in which a bill is issued.'],
                     ['City facilities', 'Parks, the golf course, the cemetery, medians, buildings and yards served '
                      'by the City water system and operated by City departments.'],
                     ['Bulk fill station', 'The card-operated hauling station at the Public Works Yard.']],
                    [1.9, 4.5], style=SANS_CELL, bold=ParagraphStyle('sbd', parent=SANS_CELL, fontName='Helvetica-Bold')))
    p('')
    h('2. Water supply')
    p('The City takes most of its summer supply from the Upper Brennan Basin Water Conservancy District under a '
      'contract entitlement of 4,200 acre-feet a delivery season, delivered through two turnouts on the district\'s '
      'Kestle Canyon pipeline. The City\'s three wells (Hollis Road Wells 1 and 2 and North Mesa Well 3) supply the '
      'remainder and all winter demand. The Fenwick Mesa service area has been served from the City system since the '
      'Fenwick Mesa storage tank was connected in 2022.')
    p('The district announces each member\'s allocation for the coming delivery season, as a share of its contract '
      'entitlement, by October 31 of the preceding year, and may revise it by April 15.')
    h('3. Stages and triggers')
    s.append(_table([['Stage', 'Trigger', 'Demand reduction sought'],
                     ['Stage 1, Drought Watch', 'District allocation below 100 per cent of entitlement, or two '
                      'consecutive dry winters at the Sawtooth Saddle snow course', 'Voluntary, 5 per cent'],
                     ['Stage 2, Drought Warning', 'District allocation below 90 per cent of entitlement', '15 per cent'],
                     ['Stage 3, Drought Emergency', 'District allocation below 70 per cent of entitlement, or a well '
                      'out of service for more than 30 days in a Stage 2 summer', '25 per cent'],
                     ['Stage 4, Critical', 'District allocation below 50 per cent of entitlement', '40 per cent']],
                    [1.6, 3.4, 1.4], style=SANS_CELL, bold=ParagraphStyle('sb2', parent=SANS_CELL, fontName='Helvetica-Bold')))
    p('')
    p('A stage declared on a district allocation applies from April 1 to October 31 of the delivery season, unless '
      'the City Council ends it earlier on a revised allocation. The demand reduction sought is measured against the '
      'City\'s production in the same months of the two preceding years and is met by all of the stage\'s measures '
      'together.')
    h('4. Stage measures')
    h3('4.1 Stage 1')
    p('Public information campaign; voluntary outdoor watering on no more than three days a week; free irrigation '
      'audits for single-family and irrigation accounts; leak alerts sent to customers whose meters show continuous '
      'flow.')
    h3('4.2 Stage 2')
    p('(a) Outdoor watering limited to three assigned days a week and prohibited from 10 a.m. to 6 p.m.; '
      '(b) no new turf planted except under a landscape plan approved before the stage was declared; '
      '(c) irrigation at City parks, the golf course, the cemetery and City medians reduced by at least 20 per cent '
      'from the same months of the prior year, with sports fields and the golf course greens and tees exempt from '
      'the day limits; (d) the bulk water fill station restricted to haulers holding a City hauling permit, with '
      'no more than 6,000 gallons a day on any card; (e) hydrant flushing suspended except for water quality '
      'complaints; and (f) a drought rate measure for the single-family residential class under Section 5.')
    h3('4.3 Stages 3 and 4')
    p('Stage 3 adds a ban on filling private pools, outdoor watering limited to two days a week, the closure of '
      'the bulk fill station to all but emergency and City use, and drought rate measures for every class. Stage 4 '
      'limits outdoor watering to trees and shrubs by hand or drip, suspends irrigation of City turf other than '
      'sports fields, and adopts per-account allotments under a separate resolution.')
    h('5. Drought rate measures')
    h3('5.1 Adoption')
    p('A drought rate measure is adopted by resolution of the City Council. It applies to the bills issued in the '
      'months of the declared stage and is added to the water rates otherwise in force on those bills. Revenue from '
      'a drought rate measure is deposited in the drought reserve fund.')
    h3('5.2 Options')
    p('Before the City Council acts on a drought rate measure for a stage, the Water Department brings it the '
      'options it has prepared, each defined as an addition to the rates in force, together with the reduction each '
      'option would achieve, sized under Section 5.3, and a recommendation.')
    h3('5.3 Sizing a rate measure')
    p('The reduction a Stage 2 rate measure achieves is the fall it brings about in the water billed to '
      'single-family residential accounts on the June to September bills of the year it applies, from what those '
      'bills would have carried at the rates otherwise in force. Each account\'s use without the measure is its '
      'baseline: for each of the four bill months, the average of the use billed to the account on that month\'s '
      'bills in the two preceding years. The accounts are the single-family residential accounts billed in each of '
      'the eight June to September bill months of those two years. Reductions are stated in acre-feet.')
    h3('5.4 Review')
    p('Within 60 days after the last bills of a stage are issued, the Water Department reports to the City Council '
      'the water billed to each class in the stage\'s months against the same months of the two preceding years.')
    h('6. Monitoring and reporting during a stage')
    p('While a stage is in force the Water Resources Division reports each month to the Utilities Director the '
      'water taken from the district at each turnout, the water produced at each well, the water drawn at the bulk '
      'fill station and the water used by City facilities, against the same month of the two preceding years, and '
      'the progress of the stage toward its demand reduction.')
    h('7. Communication')
    p('The City notifies customers of a declared stage by a bill insert, its website and a mailed notice no later '
      'than March 15 for a stage beginning April 1, and publishes the measures in force, the watering days by '
      'address and the drought rates on the bills of each month of the stage.')
    h('8. Ending a stage')
    p('A stage ends on October 31 of its delivery season, or earlier by resolution of the City Council where the '
      'district revises its allocation to a level outside the stage\'s trigger. Measures carried into the next '
      'delivery season require a new declaration.')
    h('9. Enforcement')
    p('Violations of the outdoor watering limits in a declared stage are handled by Water Department staff as '
      'follows: a written notice left at the premise for a first violation; a second notice and a USD 50 charge on '
      'the next bill for a second violation within the stage; and a USD 150 charge for each later violation. A '
      'customer may ask the Utilities Director to review a charge within 30 days of the bill on which it appears.')
    h('10. Variances')
    p('A customer may apply for a variance from a stage measure where compliance would cause a health or safety '
      'hazard, where the premise is newly landscaped under an approved plan, or where the measure cannot be met '
      'because of the use the premise is put to. Applications are made on the Water Department\'s variance form. '
      'A variance states its term and conditions and ends with the stage.')
    h('11. Coordination with the district')
    p('The Water Resources Manager is the City\'s contact with the district during a declared stage, reports the '
      'City\'s monthly deliveries against its allocation as the district requests, and brings any district notice '
      'that would move the City to another stage to the Utilities Director within five working days.')
    h('12. Review of the plan')
    p('The Water Department reviews the plan after any delivery season in which a stage of 2 or higher was in '
      'force, and in any case every five years, and brings proposed revisions to the City Council with the review.')
    h('Appendix A. Turnouts and wells')
    s.append(_table([['Source', 'Location', 'Capacity'],
                     ['District turnout ASP-North', 'Kestle Canyon pipeline at Northgate Way', '7.5 cfs'],
                     ['District turnout ASP-South', 'Kestle Canyon pipeline at Quarry Road', '5.0 cfs'],
                     ['Hollis Road Well 1', 'Hollis Road at Delmar Avenue', '650 gpm'],
                     ['Hollis Road Well 2', 'Hollis Road at Delmar Avenue', '600 gpm'],
                     ['North Mesa Well 3', 'North Mesa reservoir site', '450 gpm']],
                    [2.0, 3.0, 1.4], style=SANS_CELL, bold=ParagraphStyle('sb3', parent=SANS_CELL, fontName='Helvetica-Bold')))
    p('')
    h('Appendix B. Stage 2 actions by department')
    s.append(_table([['Department', 'Stage 2 actions', 'Reports'],
                     ['Water Resources', 'Declares the watering days by address; issues leak alerts; prepares the '
                      'monthly stage report (Section 6).', 'Monthly, to the Utilities Director'],
                     ['Rates and Finance', 'Prepares the drought rate options and their sizing (Section 5); sets up the '
                      'adopted drought rates in the billing system.', 'With the options; Section 5.4 review'],
                     ['Parks and Recreation', 'Cuts irrigation at parks, the golf course, the cemetery and medians '
                      '(Section 4.2(c)); sets each site\'s monthly targets.', 'Monthly site meter reads'],
                     ['Public Works', 'Issues hauling permits; sets the fill station card limits (Section 4.2(d)); '
                      'suspends hydrant flushing.', 'Monthly fill station activity'],
                     ['Customer Service', 'Bill inserts and notices (Section 7); enforcement notices (Section 9).',
                      'Weekly violation log']],
                    [1.4, 3.6, 1.4], style=SANS_CELL, bold=ParagraphStyle('sb4', parent=SANS_CELL, fontName='Helvetica-Bold')))
    doc.build(s, onFirstPage=lambda c, d: None, onLaterPages=on_page)
    return doc.page


# ---------------------------------------------------------------- the district's notice
def district_notice(path, total_pages=None):
    doc, on_page = _doc(path, 'Notice of 2027 Dry-Year Allocation', 'Sylvia Chavez', '2027 delivery season',
                        'Acrobat PDFMaker 24 for Word', 'Adobe PDF Library 24.2.159', '',
                        'UBBWCD Notice 2026-07', sans=True, total_pages=total_pages)
    s = []
    s.append(Paragraph('UPPER BRENNAN BASIN WATER CONSERVANCY DISTRICT', ParagraphStyle('dl', parent=SANS_H, fontSize=13,
                                                                                         leading=16, alignment=1)))
    s.append(Paragraph('1810 Canal Road, Brennan, P.O. Box 77', ParagraphStyle('dl2', parent=SANS, alignment=1,
                                                                               fontSize=8.8)))
    s.append(Spacer(1, 10))
    s.append(Paragraph('October 15, 2026', SANS))
    s.append(Paragraph('To: General managers and water directors of the District\'s member entities', SANS))
    s.append(Paragraph('Re: Notice 2026-07, Dry-Year Allocation for the 2027 Delivery Season', SANS_H3))
    p = lambda t: s.append(Paragraph(t, SANS))
    p('At its meeting of October 13, 2026, the Board of Directors found that the District\'s supply for the 2027 '
      'delivery season will be short of its members\' contract entitlements and declared a dry-year allocation under '
      'Article 9 of the member water service contracts.')
    p('Storage in Granite Draw and Upper Fork reservoirs on October 1, 2026 was 41 per cent of capacity, against a '
      'thirty-year average of 63 per cent for that date. Snowpack at the District\'s three index sites peaked at 58 '
      'per cent of median in the 2026 water year, the second consecutive year below 70 per cent, and the Bureau\'s '
      'October outlook places 2027 April to July inflow to Granite Draw Reservoir at 55 to 75 per cent of average.')
    p('Each member\'s 2027 allocation is therefore 78 per cent of its contract entitlement for the delivery season of '
      'May 1 to October 31, 2027. Deliveries above a member\'s allocation will be made only from water the member '
      'holds in carryover storage, at the District\'s carryover delivery charge.')
    s.append(_table([['Member entity', 'Contract entitlement (acre-feet)', '2027 allocation (acre-feet)'],
                     ['City of Ardley Springs', '4,200', '3,276'],
                     ['Town of Sagecrest Water Works', '2,650', '2,067'],
                     ['Hollis Ranch Mutual Water Company', '900', '702'],
                     ['Upper Fork Irrigation Company', '6,100', '4,758'],
                     ['Total', '13,850', '10,803']],
                    [2.8, 1.9, 1.7], style=SANS_CELL, bold=ParagraphStyle('db', parent=SANS_CELL, fontName='Helvetica-Bold')))
    p('')
    p('The Board will review the allocation at its April 13, 2027 meeting on the April 1 snow survey and storage, '
      'and any revision will be noticed to members by April 15, 2027. Members should plan their 2027 operations and '
      'their customers\' drought measures on the allocation in this notice.')
    p('Questions about this notice may be directed to the District office or to the undersigned.')
    s.append(Spacer(1, 16))
    p('_____________________________')
    p('Sylvia Chavez, General Manager')
    p('cc: Helen Nelson, President, Board of Directors')
    doc.build(s, onFirstPage=on_page, onLaterPages=on_page)
    return doc.page


# ---------------------------------------------------------------- the department's agenda report (docx)
def staff_report(path, created, modified):
    from docx import Document
    from docx.shared import Pt, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    d = Document()
    st = d.styles['Normal']
    st.font.name = 'Calibri'
    st.font.size = Pt(11)
    for sec in d.sections:
        sec.left_margin = sec.right_margin = Inches(1.0)
        sec.top_margin = Inches(0.9)
        fp = sec.footer.paragraphs[0]
        fp.text = 'Agenda Report, Stage 2 drought rate options for 2027, draft for department review'
        fp.runs[0].font.size = Pt(8.5)
    t = d.add_paragraph()
    r = t.add_run('CITY OF ARDLEY SPRINGS')
    r.bold = True
    r.font.size = Pt(14)
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t2 = d.add_paragraph('COUNCIL AGENDA REPORT')
    t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t2.runs[0].bold = True
    tb = d.add_table(rows=6, cols=2)
    tb.style = 'Table Grid'
    for i, (k, v) in enumerate([('Meeting date', 'December 8, 2026'), ('Agenda item', 'Public hearing: Stage 2 drought rate measure for the 2027 delivery season'),
                                ('From', 'Tami Weaver, Rates and Finance Manager'), ('Through', 'Jason Morgan, Utilities Director'),
                                ('Department', 'Water Department'), ('Status', 'Draft, October 27, 2026')]):
        tb.cell(i, 0).text = k
        tb.cell(i, 1).text = v
    d.add_paragraph('')
    d.add_heading('Background', level=2)
    d.add_paragraph('On October 15, 2026 the Upper Brennan Basin Water Conservancy District set each member\'s 2027 '
                    'allocation at 78 per cent of its contract entitlement (District Notice 2026-07). For the City that '
                    'is 3,276 acre-feet against an entitlement of 4,200 acre-feet. An allocation below 90 per cent is the '
                    'Stage 2 trigger in the City\'s Drought Contingency Plan (Revision 2), and staff will ask the Council '
                    'in January to declare Stage 2 for April 1 to October 31, 2027.')
    d.add_paragraph('Stage 2 includes a drought rate measure for the single-family residential class (Plan, Section '
                    '4.2(f)). Section 5.2 of the Plan asks the department to bring the Council its rate options, the '
                    'reduction each would achieve, sized under Section 5.3, and a recommendation. This report sets out '
                    'the options staff have prepared. The sizing and the recommendation will be added for the hearing.')
    d.add_heading('Options', level=2)
    d.add_paragraph('Each option is an addition to the single-family residential rates of Resolution No. 2023-12 and '
                    'applies to single-family residential bills issued from May 1 to October 31, 2027. The Fenwick Mesa '
                    'capital recovery charge (Resolution No. 2024-17) continues unchanged on Fenwick Mesa bills under '
                    'every option.')
    d.add_paragraph('Option A, conservation blocks. The first usage block (0 to 6,000 gallons) is billed at USD %.2f '
                    'for each 1,000 gallons in place of USD %.2f, and the third block (over 15,000 gallons) at USD %.2f '
                    'in place of USD %.2f. The base charges and the second block are unchanged.'
                    % (W.OPT_A_TIER1, W.SFR_NEW['tiers'][0][1], W.OPT_A_TIER3, W.SFR_NEW['tiers'][2][1]))
    d.add_paragraph('Option B, drought volume charge. USD %.2f is added to the charge for each 1,000 gallons in every '
                    'usage block. The base charges are unchanged.' % W.OPT_B_ADDER)
    d.add_paragraph('Option C, drought surcharge. A drought surcharge of USD %.2f is added to each monthly bill. The '
                    'base charges and the usage blocks are unchanged.' % W.OPT_C_SURCHARGE)
    tb2 = d.add_table(rows=6, cols=4)
    tb2.style = 'Table Grid'
    hdr = ['Single-family charge', 'Option A', 'Option B', 'Option C']
    body = [['Base charge, 3/4 inch / 1 inch', '%.2f / %.2f' % (W.SFR_NEW['base'][0.75], W.SFR_NEW['base'][1.0])] * 1 + ['%.2f / %.2f' % (W.SFR_NEW['base'][0.75], W.SFR_NEW['base'][1.0])] * 2,
            ['Block 1, 0 to 6,000 gallons, per 1,000', '%.2f' % W.OPT_A_TIER1, '%.2f' % (W.SFR_NEW['tiers'][0][1] + W.OPT_B_ADDER), '%.2f' % W.SFR_NEW['tiers'][0][1]],
            ['Block 2, 6,001 to 15,000 gallons, per 1,000', '%.2f' % W.SFR_NEW['tiers'][1][1], '%.2f' % (W.SFR_NEW['tiers'][1][1] + W.OPT_B_ADDER), '%.2f' % W.SFR_NEW['tiers'][1][1]],
            ['Block 3, over 15,000 gallons, per 1,000', '%.2f' % W.OPT_A_TIER3, '%.2f' % (W.SFR_NEW['tiers'][2][1] + W.OPT_B_ADDER), '%.2f' % W.SFR_NEW['tiers'][2][1]],
            ['Drought surcharge, per bill', 'None', 'None', '%.2f' % W.OPT_C_SURCHARGE]]
    for j, v in enumerate(hdr):
        tb2.cell(0, j).text = v
    for i, row in enumerate(body, start=1):
        for j, v in enumerate(row):
            tb2.cell(i, j).text = v
    d.add_paragraph('')
    d.add_heading('Other Stage 2 measures', level=2)
    d.add_paragraph('The watering-day limits, the City facility irrigation cut and the bulk fill station restrictions '
                    'of Section 4.2 take effect with the stage declaration and need no rate action. For the City\'s own '
                    'measures, the Water Resources Division will set its 2027 monthly targets from the 2026 June to '
                    'September figures for the bulk fill station and the City facility meters.')
    d.add_heading('Fiscal impact', level=2)
    d.add_paragraph('Revenue from the drought rate measure is deposited in the drought reserve fund (Plan, Section 5.1). '
                    'Staff will report the expected revenue of the recommended option with the recommendation.')
    d.add_heading('Next steps', level=2)
    d.add_paragraph('Staff will complete the sizing of the three options under Section 5.3 of the Plan and the '
                    'recommendation for the December 8 hearing. A notice of the proposed drought rates will be mailed '
                    'to single-family customers with the November bills.')
    d.add_heading('Attachments', level=2)
    d.add_paragraph('1. Upper Brennan Basin Water Conservancy District Notice 2026-07')
    d.add_paragraph('2. Drought Contingency Plan, Revision 2, Section 5')
    cp = d.core_properties
    cp.author = 'Tami Weaver'
    cp.last_modified_by = 'Tami Weaver'
    cp.created = created
    cp.modified = modified
    cp.revision = 4
    cp.title = 'Agenda Report, Stage 2 drought rate options'
    cp.comments = ''
    d.save(path)
