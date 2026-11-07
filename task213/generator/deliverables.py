"""Golden deliverables for task213 (q3_ratings_sweep.xlsx, q3_sweep_chart.png) and submission.md, every figure read
from figures.json."""
import datetime as dt
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from docs import normalize_ooxml, xlsx_props

BLUE, ORANGE, SURFACE, INK, MUTED, GRID = '#2a78d6', '#eb6834', '#fcfcfb', '#2b2b28', '#6b6a63', '#e4e3de'
MKT = {'NG': 'Nigeria (NGN)', 'GH': 'Ghana (GHS)', 'KE': 'Kenya (KES)', 'GB': 'United Kingdom (GBP)'}
MON = {'Jul': 'July 2026', 'Aug': 'August 2026', 'Sep': 'September 2026'}
THIN = Side(style='thin', color='B9B8B1')


def fmt(n):
    return '{:,}'.format(n)


def sheet(ws, title, sub, head, rows, widths, total=None, notes=()):
    ws['A1'] = title; ws['A1'].font = Font(bold=True, size=13)
    ws['A2'] = sub; ws['A2'].font = Font(italic=True, size=9, color='555555')
    r0 = 4
    for j, h in enumerate(head, 1):
        c = ws.cell(row=r0, column=j, value=h)
        c.font = Font(bold=True); c.fill = PatternFill('solid', fgColor='ECE9E1')
        c.alignment = Alignment(horizontal='left' if j == 1 else 'right', wrap_text=True, vertical='bottom')
        c.border = Border(bottom=THIN)
    r = r0
    for row in rows:
        r += 1
        for j, v in enumerate(row, 1):
            c = ws.cell(row=r, column=j, value=v)
            if j > 1:
                c.number_format = '#,##0'; c.alignment = Alignment(horizontal='right')
    if total:
        r += 1
        for j, v in enumerate(total, 1):
            c = ws.cell(row=r, column=j, value=v); c.font = Font(bold=True); c.border = Border(top=THIN)
            if j > 1:
                c.number_format = '#,##0'; c.alignment = Alignment(horizontal='right')
    r += 2
    for n in notes:
        ws.cell(row=r, column=1, value=n).font = Font(size=8.5, color='555555'); r += 1
    for j, wd in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = wd
    ws.row_dimensions[r0].height = 30
    ws.freeze_panes = ws.cell(row=r0 + 1, column=2)
    return r


def workbook(F, path):
    wb = openpyxl.Workbook()
    ws = wb.active; ws.title = 'Q3 sweep'
    rings = F['rings']; c = F['call']
    rows = [[r['ring'], r['accounts'], r['given'], r['held'], r['expunged']] for r in rings]
    end = sheet(ws, 'Q3 2026 ring sweep: %s ratings expunged' % fmt(c['notice']),
                'For the integrity notice of 1 December 2026. Integrity Policy working file, sweep of 1 July to 30 September 2026 (UTC).',
                ['Ring (its seller with the most Q3 orders)', 'Accounts suspended', 'Q3 ratings given', 'Held for manual review', 'Ratings expunged'],
                rows, [40, 13, 13, 14, 13], total=['All rings', c['accounts_suspended'], c['ratings_given'], c['held'], c['expunged_exact']],
                notes=['Ratings given: each rating once in its latest version, counted in the quarter it was first given (playbook 1.2).',
                       'Held for manual review: playbook 3.3; no account loses more than half, rounded down, of the ratings it received as the seller, suspended accounts included.',
                       'One held rating sits on a seller outside the rings whose only Q3 rating came from a ring account; it is counted with that ring.'])
    ws.cell(row=end + 1, column=1, value='Notice figure, to the nearest hundred').font = Font(bold=True)
    cc = ws.cell(row=end + 1, column=5, value=c['notice']); cc.number_format = '#,##0'; cc.font = Font(bold=True)
    ws.print_title_rows = '4:4'

    ws = wb.create_sheet('Disputes')
    sheet(ws, 'Q3 2026 disputes by market', 'Support desk cases opened in Q3 2026, one count per order.',
          ['Market (order currency)', 'Disputed orders', 'Decided for the buyer'],
          [[MKT[k], F['disputes'][k]['disputed'], F['disputes'][k]['for_buyer']] for k in ('NG', 'GH', 'KE', 'GB')], [26, 15, 17],
          notes=['A case is counted on the order whose coins the escrow held when it was opened (SD-04, 1.2), whichever order the customer cited.',
                 'Decided for the buyer: a buyer\'s case upheld (U) or a seller\'s case rejected (R).'])
    ws = wb.create_sheet('Withdrawals')
    sheet(ws, 'Users\' on-chain withdrawals, Q3 2026', 'By the UTC month the custodian\'s transfer confirmed.',
          ['Month', 'Withdrawn by users (USDT)', 'Network fees paid by the custodian (USDT)'],
          [[MON[k], F['onchain'][k]['withdrawn'], F['onchain'][k]['fees']] for k in ('Jul', 'Aug', 'Sep')], [18, 20, 24],
          notes=['Custodian outbound transfers to addresses outside Calabash; the nightly sweeps of user deposit addresses into the hot wallets are not withdrawals.',
                 'A withdrawal above the app\'s 1,000 USDT request limit is two wallet requests and one custodian transfer.'])
    ws = wb.create_sheet('Cashback')
    sheet(ws, 'Merchant-group cashback paid in Q3 2026', 'Transfers from each group\'s treasury wallet to buyers\' accounts.',
          ['Market (group)', 'Cashback paid (USDT)', 'Different buyers'],
          [[MKT[k], F['cashback'][k]['cashback'], F['cashback'][k]['buyers']] for k in ('NG', 'GH', 'KE', 'GB')], [26, 18, 15],
          notes=['Four groups moved to a new treasury wallet in the first week of August; the old wallet\'s July and August cashback is counted with its group.'])
    xlsx_props(wb, 'Q3 2026 ring sweep')
    wb.save(path); normalize_ooxml(path, dt.datetime(2026, 11, 5, 16, 20, 0))


def chart(F, path):
    rings = list(reversed(F['rings']))
    names = [r['ring'] for r in rings]
    ex = [r['expunged'] for r in rings]; he = [r['held'] for r in rings]
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'axes.edgecolor': GRID, 'axes.labelcolor': MUTED,
                         'xtick.color': MUTED, 'ytick.color': INK, 'svg.hashsalt': 'task213'})
    fig, ax = plt.subplots(figsize=(8.4, 4.2), dpi=150)
    fig.patch.set_facecolor(SURFACE); ax.set_facecolor(SURFACE)
    y = range(len(rings))
    ax.barh(y, ex, height=0.52, color=BLUE, edgecolor=SURFACE, linewidth=2, label='Expunged')
    ax.barh(y, he, left=ex, height=0.52, color=ORANGE, edgecolor=SURFACE, linewidth=2, label='Held for manual review')
    for i, (e, h) in enumerate(zip(ex, he)):
        ax.text(e + h + 18, i, '%s expunged, %s held' % (fmt(e), fmt(h)), va='center', fontsize=8.2, color=INK)
    ax.set_yticks(list(y)); ax.set_yticklabels(names)
    ax.set_xlim(0, max(e + h for e, h in zip(ex, he)) * 1.42)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: fmt(int(v))))
    ax.set_xlabel('Q3 2026 ratings given by the ring\'s accounts')
    ax.grid(axis='x', color=GRID, linewidth=0.8); ax.set_axisbelow(True)
    for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
    ax.tick_params(axis='y', length=0)
    ax.legend(loc='lower right', bbox_to_anchor=(1.0, 1.0), ncol=2, frameon=False, fontsize=8.2, handlelength=1.2, borderaxespad=0.2)
    fig.suptitle('The Q3 sweep expunges %s ratings across %d rings' % (fmt(F['call']['notice']), F['call']['rings']),
                 x=0.012, y=0.975, ha='left', fontsize=11.5, fontweight='bold', color=INK)
    ax.set_title('%s ratings given, %s held under playbook 3.3; rings named by their busiest seller' %
                 (fmt(F['call']['ratings_given']), fmt(F['call']['held'])), loc='left', fontsize=8.6, color=MUTED, pad=18)
    fig.tight_layout(rect=(0, 0, 1, 0.965))
    fig.savefig(path, facecolor=SURFACE, metadata={'Software': None})
    plt.close(fig)


def submission(F, path):
    c = F['call']; rv = F['rivals']; L = []
    L += ['## Tags', '', '**Domain:** Banking, Credit & Financial Risk (fraud and AML detection).',
          '**Analytical objective:** Anomaly Detection & Diagnostics.', '']
    L += ['## 1. Final Recommendation', '',
          '**The 1 December integrity notice should report that the Q3 2026 sweep expunges %s ratings.**' % fmt(c['notice']),
          'The sweep suspends %s accounts in %d rings, which gave %s Q3 ratings; the holdback keeps %s for manual review and the '
          'sweep expunges %s. Not the %s that shared-phone links give, which miss the rings run from one phone per account. Not '
          'a scaling of the Q2 notice\'s count or the transparency report\'s prevalence, which count another quarter\'s rings '
          'or every inauthentic rating.' % (fmt(c['accounts_suspended']), c['rings'], fmt(c['ratings_given']), fmt(c['held']),
                                           fmt(c['expunged_exact']), fmt(rv['default_notice'])), '']
    L += ['## 2. Critical Components', '',
          '1. Ring accounts, every account on a purchase passed within the hour to an account that tops up the seller it was bought from: **%s** in **%d** rings' % (fmt(c['accounts_suspended']), c['rings']),
          '2. Q3 ratings those accounts gave, each once in its latest version: **%s**' % fmt(c['ratings_given']),
          '3. Ratings the playbook 3.3 holdback keeps for manual review: **%s**' % fmt(c['held']),
          '4. Ratings expunged: **%s**, **%s** to the nearest hundred' % (fmt(c['expunged_exact']), fmt(c['notice'])), '']
    L += ['## 3. Step-by-Step Solution', '',
          '1. Read moderation_playbook_v4.2.pdf: a ring is accounts one person or group controls that trade with one another to rate one another, and the sweep expunges every rating its accounts gave in the quarter (1.2, 3.1) less the holdback of 3.3, which covers suspended accounts too.',
          '2. Resolved the released orders in escrow_orders_2026-07.csv, escrow_orders_2026-08.csv and escrow_orders_2026-09.csv by handle, and the wallet_ledger_2026q3.parquet transfers by wallet number with posted_at converted from Lagos time to UTC, to accounts as at each record through accounts.csv and handle_changes.csv.',
          '3. Kept every released order whose buyer made a wallet transfer within the hour after it to an account that made a wallet transfer to that order\'s seller in the quarter; the buyers, those accounts and the sellers are %s ring accounts in %d connected rings.' % (fmt(c['accounts_suspended']), c['rings']),
          '4. Counted the ratings those accounts gave in ratings_2026q3.parquet (latest version per rating_id, first version in Q3) and applied the holdback seller by seller: %s given, %s held, %s expunged.' % (fmt(c['ratings_given']), fmt(c['held']), fmt(c['expunged_exact'])),
          '5. For the disputes, put each case in support_cases_2026q3.xlsx on the order whose coins the escrow held at opened_wat (SD-04 1.2: the cited order_ref when it was open then, otherwise the same two accounts\' order open then), counted each order once by its fiat currency, and read U and R against the customer who opened the case.',
          '6. For the withdrawals, summed amount_usdt and network_fee_usdt in custodian_outbound_2026q3.parquet over transfers to addresses outside Calabash, by the UTC month of confirmed_at, leaving out the sweeps whose from_address is a deposit address in the wallet ledger\'s deposit rows.',
          '7. For the cashback, took each group\'s treasury as the wallet that funded its desks in each week (four groups in merchant_programme_2026-09-30.xlsx moved theirs in August, the old wallet sending its balance to the new one) and summed its transfers to buyers\' accounts in Q3 by the group\'s market, with the different buyers paid.',
          '8. The notice reports %s ratings expunged.' % fmt(c['notice']), '']
    L += ['## 4. Deliverable Answers', '', '### q3_ratings_sweep.xlsx', '',
          '1. One line per ring, in any order and named by any of its accounts (accounts suspended, Q3 ratings given, held for manual review, expunged):']
    for r in F['rings']:
        L.append('   - Ring of %s accounts (busiest seller %s): %s given, %s held, %s expunged' % (fmt(r['accounts']), r['ring'], fmt(r['given']), fmt(r['held']), fmt(r['expunged'])))
    L.append('   - All rings: %s accounts, %s given, %s held, %s expunged' % (fmt(c['accounts_suspended']), fmt(c['ratings_given']), fmt(c['held']), fmt(c['expunged_exact'])))
    L.append('2. Notice figure: %s ratings expunged' % fmt(c['notice']))
    L.append('3. Q3 disputes by market (disputed orders, decided for the buyer):')
    for k in ('NG', 'GH', 'KE', 'GB'):
        L.append('   - %s: %s disputed, %s decided for the buyer' % (MKT[k], fmt(F['disputes'][k]['disputed']), fmt(F['disputes'][k]['for_buyer'])))
    L.append('4. Users\' on-chain withdrawals by the UTC month the custodian\'s transfer confirmed (USDT withdrawn, network fees):')
    for k in ('Jul', 'Aug', 'Sep'):
        L.append('   - %s: %s USDT withdrawn, %s USDT in network fees' % (MON[k].split()[0], fmt(F['onchain'][k]['withdrawn']), fmt(F['onchain'][k]['fees'])))
    L.append('5. Merchant-group cashback paid in Q3 by market (USDT paid, different buyers):')
    for k in ('NG', 'GH', 'KE', 'GB'):
        L.append('   - %s: %s USDT to %s buyers' % (MKT[k], fmt(F['cashback'][k]['cashback']), fmt(F['cashback'][k]['buyers'])))
    L += ['', '### q3_sweep_chart.png', '',
          '6. Horizontal stacked bar per ring, expunged and held ratings, rings in descending order of expunged, each bar labelled with both counts and the title giving the %s notice figure' % fmt(c['notice']), '']
    Path(path).write_text('\n'.join(L))


def write_all(F, task):
    g = Path(task) / 'golden'; g.mkdir(exist_ok=True)
    workbook(F, g / 'q3_ratings_sweep.xlsx')
    chart(F, g / 'q3_sweep_chart.png')
    submission(F, Path(task) / 'submission.md')
