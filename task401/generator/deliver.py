"""task401: the golden deliverables from generator/figures.json (the review PDF with its bridge chart, the readiness
workbook). Every figure is read from figures.json; nothing is typed.
    python3 deliver.py            writes <task>/golden/
"""
import io, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import docs  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.platypus import Paragraph, Spacer, Image  # noqa: E402

TASK = os.path.dirname(HERE)
OUT = os.path.join(TASK, 'golden')
F = json.load(open(os.path.join(HERE, 'figures.json')))
P = lambda s, st='p': Paragraph(s, docs.S[st])
REGION_ORDER = sorted(F['ask_a']['counts'])
WEEKS = ['1 Sep', '8 Sep', '15 Sep', '22 Sep', '29 Sep', '6 Oct', '13 Oct', '20 Oct', '27 Oct']
MONTHS = [(7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')]
CHANNELS = ['Direct web', 'Comparison site', 'Phone', 'Broker']


def chart():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8.5, 'svg.hashsalt': 'task401'})
    b = F['bridge']
    steps = [('H1 2025', F['share_h1_2025'], 'total'), ('Quote journey\nquotes', -b['quote'], 'step'),
             ('October\ntariff rise', -b['tariff rise'], 'step'), ('Contact centre\nmove', -b['contact centre'], 'step'),
             ('Platform and\nthe rest', -b['platform and the rest'], 'step'), ('H1 2026', F['share_h1_2026'], 'total')]
    fig, ax = plt.subplots(figsize=(6.4, 3.1), dpi=200)
    level = 0.0
    for i, (lab, v, kind) in enumerate(steps):
        if kind == 'total':
            ax.bar(i, v - 60, bottom=60, color='#3b4a5a', width=0.62)
            ax.text(i, v + 0.3, '%.1f' % v, ha='center', va='bottom', fontsize=8.5, color='#222222')
            level = v
        else:
            col = '#c4572a' if i == 1 else ('#8a9aa8' if v < 0 else '#6f9f6a')
            ax.bar(i, v, bottom=level, color=col, width=0.62)
            ax.text(i, max(level, level + v) + 0.3, '%+.1f' % v, ha='center', va='bottom', fontsize=8.5, color='#222222')
            level += v
    ax.set_xticks(range(len(steps))); ax.set_xticklabels([s[0] for s in steps])
    ax.set_ylim(60, 80); ax.set_ylabel('Share satisfied, per cent')
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.set_title('Most of the 9.1-point fall sits with the quotes, not the platform', fontsize=9.5, loc='left')
    fig.tight_layout()
    buf = io.BytesIO(); fig.savefig(buf, format='png', metadata={'Software': None}); plt.close(fig)
    buf.seek(0)
    return buf


def review():
    path = os.path.join(OUT, 'six_month_satisfaction_review.pdf')
    flow = [
        P('Customer Insight, %s' % docs.ORG, 'sub'),
        P('<b>To</b> Joanne O\'Brien, Chief Customer Officer; Elliot Davies, Billing Programme Director<br/>'
          '<b>From</b> Rita Fisher, Head of Customer Insight<br/><b>Date</b> 9 November 2026<br/>'
          '<b>Subject</b> Six-month satisfaction, first half of 2025 to first half of 2026', 'p'),
        P('The fall came from the quotes new customers were sold on, not from the billing platform', 'title'),
        P('Six-month satisfaction among new customers fell from %.1f per cent in the first half of 2025 to %.1f per cent '
          'in the first half of 2026, a fall of %.1f points.<super>1</super> Since the quote and switch journey was '
          'relaunched on 6 May 2025 it no longer pre-fills the industry annual quantity (EAC or AQ) for the customer\'s '
          'meter points: customers are quoted on the use they type in, or on typical values when they give none. Six months '
          'on, the customers whose meter points\' annual quantities cost more than their quote, at the quote\'s own rates, '
          'are the ones who are less satisfied, and more than half of the fall is theirs.' % (
              F['share_h1_2025'], F['share_h1_2026'], F['fall_points'])),
        P('The test of the platform is the customers whose quote did cover the cost of their metered use. In the first '
          'half of 2026 they were billed on the new platform; in the first half of 2025 their counterparts were billed on '
          'the legacy one. Around four in five of them were satisfied in both half-years. Satisfaction fell among the '
          'customers who were told to expect less than their meters then recorded, and the share of new customers in that '
          'position rose after the relaunch.'),
        Spacer(1, 4),
        Image(chart(), width=160 * mm, height=77.5 * mm),
        P('Source: six-month survey exports (H1 2025, H1 2026), quote log, supply registrations, meter point annual '
          'quantities and tariff rates. Each customer\'s metered annual cost is set against their quote in a model of '
          'satisfaction with the October tariff rise, the contact centre move and the 2026 platform term; the fall is '
          'split over the four causes, averaged over every order.', 'small'),
        P('What the other explanations rest on', 'h'),
        P('<b>Billing platform.</b> Every 2026 respondent is billed on it and the billing accuracy and bill clarity ratings '
          'fell furthest, so a driver analysis of the ratings points at it. The ratings fell where bills ran above what '
          'the customer had been told to expect; customers whose quote covered their use rated their bills as 2025\'s '
          'customers did. The estimated-bill defect in the phase 1 close-out (BT-118) was real and was fixed by mid-November '
          '2025.'),
        P('<b>October tariff rise and contact centre move.</b> Variable-tariff customers and customers who contacted us '
          'fell by one to two points more than the rest; neither comes near the size of the fall.'),
        P('<b>Survey vendor change.</b> The questions and the scale are unchanged between the two vendors, and the '
          'customers whose quote covered their use held their level across the change.'),
        P('What it means', 'h'),
        P('Phase 2 can cut over on 1 February 2027 as planned: none of the fall belongs to the platform. The fix is in the '
          'quote journey. Where a customer\'s meter points are known, pre-fill the industry quantity again; where the '
          'customer types their use or takes typical values, show the quote against the meter point quantity before the '
          'sale. The phase 2 scope, the phase 1 weekly moves and the July to December switches by channel are in '
          'phase2_readiness.xlsx.'),
        Spacer(1, 6),
        P('<super>1</super> Satisfied means a 4 or 5 on the overall question, one response per account (the first '
          'answered), as set in the six-month survey measurement framework v2.1; the 2026 export\'s labels are mapped by '
          'its scale table.', 'small'),
    ]
    docs._pdf(path, 'Six-month satisfaction, H1 2025 to H1 2026', 'Rita Fisher', flow)


def workbook():
    import openpyxl
    from openpyxl.styles import Font, Alignment
    path = os.path.join(OUT, 'phase2_readiness.xlsx')
    wb = openpyxl.Workbook()
    bold = Font(bold=True)
    ws = wb.active; ws.title = 'Phase 2 scope'
    ws.append(['Accounts phase 2 will move, by region: prepayment accounts still supplied on 1 November 2026']); ws['A1'].font = bold
    ws.append([])
    ws.append(['Region', 'Accounts'])
    for r in REGION_ORDER:
        ws.append([r, F['ask_a']['counts'][r]])
    ws.append(['Total', sum(F['ask_a']['counts'].values())])
    ws.append([])
    ws.append(['Annual quantity of the meter points phase 2 will move (in force on 1 November 2026)', 'GWh'])
    ws.append(['Electricity', F['ask_a']['elec_gwh']]); ws.append(['Gas', F['ask_a']['gas_gwh']])
    for row in ws.iter_rows(min_row=4, max_row=4 + len(REGION_ORDER), min_col=2, max_col=2):
        for c in row:
            c.number_format = '#,##0'
    for c in (ws.cell(row=ws.max_row - 1, column=2), ws.cell(row=ws.max_row, column=2)):
        c.number_format = '0.0'
    for c in ws[3]:
        c.font = bold
    ws.cell(row=4 + len(REGION_ORDER), column=1).font = bold
    ws.column_dimensions['A'].width = 26; ws.column_dimensions['B'].width = 12; ws.freeze_panes = 'A4'
    ws2 = wb.create_sheet('Phase 1 moves')
    ws2.append(['Accounts phase 1 moved to the new platform, by week (Monday to Sunday, UK time)']); ws2['A1'].font = bold
    ws2.append([])
    ws2.append(['Week commencing', 'Electricity-only', 'Dual fuel', 'Total'])
    for k, w in enumerate(WEEKS, 1):
        e, d = F['ask_b']['%d|ELEC' % k], F['ask_b']['%d|DUAL' % k]
        ws2.append(['%s 2025' % w, e, d, e + d])
    te = sum(F['ask_b']['%d|ELEC' % k] for k in range(1, 10)); td = sum(F['ask_b']['%d|DUAL' % k] for k in range(1, 10))
    ws2.append(['Total', te, td, te + td])
    for c in ws2[3]:
        c.font = bold
    ws2.cell(row=13, column=1).font = bold
    for row in ws2.iter_rows(min_row=4, max_row=13, min_col=2, max_col=4):
        for c in row:
            c.number_format = '#,##0'
    ws2.column_dimensions['A'].width = 18
    for col in 'BCD':
        ws2.column_dimensions[col].width = 15
    ws2.freeze_panes = 'A4'
    ws3 = wb.create_sheet('Switches by channel')
    ws3.append(['Switches each sales channel brought in, by the month first supply started, July to December 2025']); ws3['A1'].font = bold
    ws3.append([])
    ws3.append(['Month'] + CHANNELS + ['Total'])
    for m, name in MONTHS:
        vals = [F['ask_c']['%s|%d' % (c, m)] for c in CHANNELS]
        ws3.append([name] + vals + [sum(vals)])
    tot = [sum(F['ask_c']['%s|%d' % (c, m)] for m, _ in MONTHS) for c in CHANNELS]
    ws3.append(['Total'] + tot + [sum(tot)])
    for c in ws3[3]:
        c.font = bold
    ws3.cell(row=10, column=1).font = bold
    for row in ws3.iter_rows(min_row=4, max_row=10, min_col=2, max_col=6):
        for c in row:
            c.number_format = '#,##0'
    ws3.column_dimensions['A'].width = 13
    for col in 'BCDEF':
        ws3.column_dimensions[col].width = 16
    ws3.freeze_panes = 'B4'
    ws4 = wb.create_sheet('Notes')
    for line in ('Phase 2 scope per the phase 2 cutover plan v1.3: prepayment accounts on the legacy platform still supplied on '
                 '1 November 2026 on at least one meter point; a meter point passes to the account that took it on last.',
                 'Annual quantities: each meter point\'s industry annual quantity in force on 1 November 2026, day and night '
                 'together on a two-rate meter.',
                 'Phase 1 moves: each account counted once, in the week its last load completed, UK time, with the fuels that '
                 'load carried; accounts returned to the legacy platform were not moved.',
                 'Switches: one per customer, in the month first supply started, credited to the sale the switch was '
                 'registered on; switches withdrawn before supply began are left out.',
                 'Prepared by Customer Insight, 9 November 2026.'):
        ws4.append([line])
    ws4.column_dimensions['A'].width = 120
    for row in ws4.iter_rows():
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical='top')
    wb.save(path)
    docs.scrub_xlsx(path, 'Rita Fisher', '2026-11-04T09:10:00Z', '2026-11-09T16:25:00Z', stamp=(2026, 11, 9, 16, 25, 0))


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    review(); workbook()
    for fn in os.listdir(OUT):
        os.utime(os.path.join(OUT, fn), (1794240000, 1794240000))   # 2026-11-09 the review's date
    print('golden written:', sorted(os.listdir(OUT)))
