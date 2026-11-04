"""The golden deliverables: the allocation workbook and the posts chart."""
import datetime as dt
import os
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import world as W
import records as R

ORG = 'Ravensby and Weald Integrated Care Board, maternity commissioning'
SHORT = {'RRI': 'Ravensby Royal Infirmary', 'KUH': 'Kellingworth University Hospital', 'SDH': 'Sedgefold Hospital',
         'SAH': "St Aldric's Hospital", 'WCH': 'Wennby Community Hospital'}
THIN = Side(style='thin', color='A6A6A6')


def _hdr(ws, row, cols):
    for j, h in enumerate(cols, start=1):
        c = ws.cell(row=row, column=j, value=h)
        c.font = Font(bold=True)
        c.fill = PatternFill('solid', fgColor='DCE6F1')
        c.alignment = Alignment(wrap_text=True, vertical='top')
        c.border = Border(bottom=THIN)


def workbook(path, C, A, Bk):
    import build
    wb = openpyxl.Workbook()
    wb.properties.creator = ORG
    wb.properties.lastModifiedBy = ORG
    wb.properties.created = dt.datetime(2026, 11, 3, 16, 20)
    wb.properties.modified = dt.datetime(2026, 11, 3, 16, 20)
    ws = wb.active
    ws.title = 'Posts by unit'
    ws['A1'] = 'Neonatal outreach posts from 1 April 2027 (specification SS-MAT-027 v1.2, section 7)'
    ws['A1'].font = Font(bold=True, size=12)
    ws['A2'] = 'Planning basis: babies discharged home 1 October 2025 to 30 September 2026 with the feeding or jaundice risk flag'
    _hdr(ws, 4, ['Maternity unit', 'Eligible babies discharged home', 'Posts'])
    for i, u in enumerate(W.FIVE):
        r = 5 + i
        ws.cell(row=r, column=1, value=SHORT[u])
        ws.cell(row=r, column=2, value=C['eligible'][i]).number_format = '#,##0'
        ws.cell(row=r, column=3, value=C['posts'][i])
    r = 5 + len(W.FIVE)
    ws.cell(row=r, column=1, value='All five units').font = Font(bold=True)
    ws.cell(row=r, column=2, value=sum(C['eligible'])).number_format = '#,##0'
    ws.cell(row=r, column=3, value=sum(C['posts']))
    for j in (1, 2, 3):
        ws.cell(row=r, column=j).border = Border(top=THIN)
    ws.cell(row=r + 2, column=1, value='Readmissions the service avoids in 2027/28, to the nearest 25').font = Font(bold=True)
    ws.cell(row=r + 2, column=3, value=C['total_rounded']).font = Font(bold=True)
    ws.cell(row=r + 4, column=1, value=('Each unit\'s share follows its eligible babies\' unplanned readmissions in the planning year that '
                                        'came after the outreach line could first have reached the family: the community midwifery office\'s '
                                        'receipt of the discharge notification, or 08:00 when it arrived outside the line\'s calling hours of '
                                        '08:00 to 19:00. Readmissions before that point are beyond the service. The trial\'s cut in '
                                        'readmission after its first call, %d per cent, is applied to the rest.' % C['theta_pct']))
    ws.cell(row=r + 4, column=1).alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells(start_row=r + 4, start_column=1, end_row=r + 4, end_column=3)
    ws.row_dimensions[r + 4].height = 72
    ws.column_dimensions['A'].width = 46
    ws.column_dimensions['B'].width = 18
    ws.column_dimensions['C'].width = 12
    ws.freeze_panes = 'A5'

    ws2 = wb.create_sheet('Trial readmissions by reason')
    ws2['A1'] = 'Copperfield trial: unplanned readmission within 28 days of discharge home, by risk reason on the discharge record'
    ws2['A1'].font = Font(bold=True)
    _hdr(ws2, 3, ['Risk reason', 'Outreach: babies', 'Outreach: readmitted', 'Usual care: babies', 'Usual care: readmitted',
                  'Usual care: readmitted (%)', 'Risk ratio, outreach against usual care'])
    for i, rcode in enumerate(W.REASONS):
        r = 4 + i
        a = A[rcode]
        vals = [R.REASON_LABEL[rcode], a['no'], a['ro'], a['nc'], a['rc'], a['rate_c'], a['rr']]
        for j, v in enumerate(vals, start=1):
            c = ws2.cell(row=r, column=j, value=v)
            if j == 6:
                c.number_format = '0.0'
            elif j == 7:
                c.number_format = '0.00'
            elif j > 1:
                c.number_format = '#,##0'
    ws2.cell(row=11, column=1, value=('Babies analysed as randomised (final list). A baby with more than one reason is counted under '
                                      'each; a baby readmitted more than once counts once. Copperfield Hospital admits a baby who '
                                      'returns to its postnatal ward under the mother\'s record; those admissions are counted for the '
                                      'baby, so the counts run above the final report\'s.')).font = Font(italic=True)
    ws2.cell(row=11, column=1).alignment = Alignment(wrap_text=True, vertical='top')
    ws2.merge_cells('A11:G11')
    ws2.row_dimensions[11].height = 44
    ws2.column_dimensions['A'].width = 34
    for j in range(2, 8):
        ws2.column_dimensions[get_column_letter(j)].width = 15
    ws2.row_dimensions[3].height = 44
    ws2.freeze_panes = 'B4'

    ws3 = wb.create_sheet('Outreach contacts by reason')
    ws3['A1'] = 'Copperfield trial, outreach arm: home visits made and telephone calls in the 28 days after discharge, per baby'
    ws3['A1'].font = Font(bold=True)
    _hdr(ws3, 3, ['Risk reason', 'Babies randomised to outreach (analysed)', 'Home visits per baby', 'Telephone calls per baby'])
    for i, rcode in enumerate(W.REASONS):
        r = 4 + i
        hv, tel, n = Bk[rcode]
        for j, v in enumerate([R.REASON_LABEL[rcode], n, hv, tel], start=1):
            c = ws3.cell(row=r, column=j, value=v)
            if j in (3, 4):
                c.number_format = '0.00'
            elif j == 2:
                c.number_format = '#,##0'
    ws3.cell(row=11, column=1, value=('Calls logged under a parent\'s NHS number are counted for the baby; a contact re-sent by the '
                                      'tablet application counts once. Visits with no access (NA) and unanswered calls (TNA) are not '
                                      'counted; before those codes came into use on 6 January 2025 such attempts were filed as HV or '
                                      'TEL with a few minutes against them, and are left out too.')).alignment = Alignment(wrap_text=True, vertical='top')
    ws3.merge_cells('A11:D11')
    ws3.row_dimensions[11].height = 58
    ws3.column_dimensions['A'].width = 34
    for j in range(2, 5):
        ws3.column_dimensions[get_column_letter(j)].width = 20
    ws3.freeze_panes = 'B4'

    ws4 = wb.create_sheet('Notes')
    notes = [('Prepared', '3 November 2026 for the maternity and neonatal programme board'),
             ('Sources', 'Both trusts\' maternity discharge extracts, the community midwifery office notification log, the ICB '
                         'admissions extract and master patient index, the Copperfield final randomisation list, contact log and '
                         'final report, all as extracted on 2 November 2026'),
             ('Readmission', 'Specification SS-MAT-027 section 5: emergency admission to any hospital in the area within 28 days of '
                             'discharge home, once per baby'),
             ('Rounding', 'Rates to one decimal place, contacts per baby to two decimals, readmissions avoided to the nearest 25')]
    for i, (k, v) in enumerate(notes, start=1):
        ws4.cell(row=i, column=1, value=k).font = Font(bold=True)
        ws4.cell(row=i, column=2, value=v).alignment = Alignment(wrap_text=True, vertical='top')
        ws4.row_dimensions[i].height = 30
    ws4.column_dimensions['A'].width = 14
    ws4.column_dimensions['B'].width = 100
    wb.save(path)
    build.normalise_zip(path)


def chart(path, C):
    """Posts by unit as horizontal bars, largest first, each bar labelled; written as SVG with fixed ids."""
    plt.rcParams['svg.hashsalt'] = 'task313-outreach-posts'
    plt.rcParams['font.family'] = 'DejaVu Sans'
    names = ['Ravensby Royal Infirmary', 'Kellingworth University Hospital', 'Sedgefold Hospital', "St Aldric's Hospital",
             'Wennby Community Hospital']
    posts = C['posts']
    order = sorted(range(5), key=lambda i: (-posts[i], i))
    fig, ax = plt.subplots(figsize=(7.4, 3.8))
    ys = list(range(5))[::-1]
    for y, i in zip(ys, order):
        ax.barh(y, posts[i], color='#1f4e79' if i == order[0] else '#6f8fb3', height=0.6)
        ax.text(posts[i] + 0.15, y, '%d' % posts[i], va='center', fontsize=10, color='#222222')
    ax.set_yticks(ys)
    ax.set_yticklabels([names[i] for i in order], fontsize=9)
    ax.set_xlabel('Whole-time outreach nurse posts from 1 April 2027', fontsize=9)
    ax.set_xlim(0, max(posts) + 1.6)
    ax.set_xticks(range(0, max(posts) + 2, 2))
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    fig.text(0.012, 0.955, 'Kellingworth takes %d of the 30 posts, St Aldric\'s %d' % (posts[1], posts[3]),
             fontsize=11.5, fontweight='bold', color='#222222', va='top')
    fig.text(0.012, 0.885, 'Neonatal outreach posts by maternity unit from April 2027; about %d readmissions avoided in 2027/28'
             % C['total_rounded'], fontsize=9, color='#444444', va='top')
    fig.text(0.012, 0.02, 'Allocation by SS-MAT-027 section 7 on babies discharged home 1 October 2025 to 30 September 2026.\n'
             'Ravensby and Weald ICB, maternity commissioning, 3 November 2026.', fontsize=7, color='#555555', va='bottom')
    fig.tight_layout(rect=(0, 0.08, 1, 0.84))
    fig.savefig(path, format='svg', metadata={'Date': None, 'Creator': None, 'Title': 'Neonatal outreach posts by unit, 2027/28'})
    plt.close(fig)
