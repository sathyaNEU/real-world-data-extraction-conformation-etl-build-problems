"""task403 golden: every graded figure from the clean truth, and the two deliverables."""
import io
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
import world
import docs

TOR = world.TOR
MONTHS = ['2025-%02d' % m for m in range(2, 11)]
MONTH_NAMES = {'2025-02': 'February', '2025-03': 'March', '2025-04': 'April', '2025-05': 'May', '2025-06': 'June',
               '2025-07': 'July', '2025-08': 'August', '2025-09': 'September', '2025-10': 'October'}


def periods(T):
    st = pd.to_datetime(T.start.values).tz_localize('UTC').tz_convert(TOR)
    per = np.select([(st >= pd.Timestamp('2024-11-01', tz=TOR)) & (st < pd.Timestamp('2025-02-01', tz=TOR)),
                     (st >= pd.Timestamp('2025-11-01', tz=TOR)) & (st < pd.Timestamp('2026-02-01', tz=TOR))],
                    ['W24', 'W25'], 'x')
    return per, st.strftime('%Y-%m')


def compute(W, T):
    P = W['P']
    S = W['S']
    T = T.copy()
    per, month = periods(T)
    T['per'], T['month'] = per, month
    played = np.zeros(len(T), bool)
    played[P.trial.unique()] = True
    T['played'] = played
    eps = P.drop_duplicates(['trial', 'season_key', 'episode']).groupby('trial').size()
    T['episodes'] = eps.reindex(range(len(T))).fillna(0).values
    a, b = T[T.per == 'W24'], T[T.per == 'W25']
    n25 = len(b)
    F = {}
    for nm, X in (('w24', a), ('w25', b)):
        F['stage_trials_%s' % nm] = int(len(X))
        F['stage_played_%s' % nm] = round(100 * X.played.mean(), 1)
        F['stage_subscribed_%s' % nm] = round(100 * X.keep.mean(), 1)
        F['stage_collected_%s' % nm] = round(100 * X[X.keep].paid.mean(), 1)
        F['paid_rate_%s' % nm] = round(100 * X.paid.mean(), 1)
        F['_raw_played_%s' % nm] = 100 * X.played.mean()
        F['_raw_subscribed_%s' % nm] = 100 * X.keep.mean()
        F['_raw_collected_%s' % nm] = 100 * X[X.keep].paid.mean()
    p24, p25 = a.paid.mean(), b.paid.mean()
    p24_run, p24_norun = a[a.run].paid.mean(), a[~a.run].paid.mean()
    assert b.run.sum() == 0
    fall = (p24 - p25) * n25
    C = (p24 - p24_norun) * n25
    within = (p24_norun - p25) * n25
    d24, d25 = a[a.declined], b[b.declined]
    B = (d24.recovered.mean() - d25.recovered.mean()) * len(d25)
    s24 = a.groupby('channel').size() / len(a)
    s25 = b.groupby('channel').size() / len(b)
    pc = b.groupby('channel').paid.mean()
    D = float(((s24 - s25) * pc).sum()) * n25
    A = within - B - D
    vals = {'C': C, 'A': A, 'B': B, 'D': D}
    order = sorted(vals, key=vals.get, reverse=True)
    F['_raw'] = {'fall': fall, 'C': C, 'A': A, 'B': B, 'D': D, 'within': within, 'start': p24 * n25,
                 'end': b.paid.sum(), 'r24': a.run.mean(), 'p24_run': p24_run, 'p24_norun': p24_norun, 'n25': n25,
                 'rec24': d24.recovered.mean(), 'rec25': d25.recovered.mean(), 'declined25': len(d25)}
    F['pick'] = order[0]
    F['runner_up'] = order[1]
    F['conv_slate'] = int(round(C, -2))
    F['conv_price'] = int(round(A, -2))
    F['conv_recovery'] = int(round(B, -2))
    F['conv_channel'] = int(round(D, -2))
    F['conv_gap'] = int(round(C - A, -2))
    F['conv_fall'] = int(round(fall, -2))
    F['waterfall_start'] = int(round(p24 * n25, -2))
    F['waterfall_end'] = int(round(b.paid.sum(), -2))
    F['paid_w24'] = int(a.paid.sum())
    F['paid_w25'] = int(b.paid.sum())
    F['runway_share_w24'] = round(100 * a.run.mean(), 1)
    F['paid_rate_w24_runway'] = round(100 * p24_run, 1)
    F['paid_rate_w24_norunway'] = round(100 * p24_norun, 1)
    F['recovered_w24'] = round(100 * d24.recovered.mean(), 1)
    F['recovered_w25'] = round(100 * d25.recovered.mean(), 1)
    M = T[T.month.isin(MONTHS)]
    g = M.groupby('month')
    F['_raw_months'] = {m: (100 * g.paid.mean()[m], g.episodes.mean()[m], int(g.size()[m])) for m in MONTHS}
    for m in MONTHS:
        F['ask_paid_share_%s' % m] = round(100 * g.paid.mean()[m], 1)
        F['ask_episodes_%s' % m] = round(g.episodes.mean()[m], 1)
    return F


PROG_NAMES = {'A': '(A) First-month price hold', 'B': '(B) First-charge payment recovery',
              'C': '(C) Winter release slate', 'D': '(D) Paid acquisition mix'}


def workbook(path, F):
    wb = Workbook()
    thin = Side(style='thin', color='999999')
    head = Font(bold=True)
    fill = PatternFill('solid', fgColor='E8EEF4')
    ws = wb.active
    ws.title = 'Winter stages'
    ws.append(['The fall sits at the day-7 decision: the share still subscribed when the trial ended'])
    ws['A1'].font = Font(bold=True, size=12)
    ws.append(['Shares of each winter\'s trials; first charges collected as a share of first charges attempted.'])
    ws.append([])
    ws.append(['Stage', '2024-25 winter', '2025-26 winter', 'Change (points)'])
    for c in ws[4]:
        c.font = head
        c.fill = fill
    ws.append(['Trials started', F['stage_trials_w24'], F['stage_trials_w25'], None])
    for lab, k in (('Played an episode (%)', 'played'), ('Still subscribed when the trial ended (%)', 'subscribed'),
                   ('First charges collected (%)', 'collected')):
        x, y = F['stage_%s_w24' % k], F['stage_%s_w25' % k]
        ws.append([lab, x, y, round(y - x, 1)])
    ws.append(['Paid conversion (%)', F['paid_rate_w24'], F['paid_rate_w25'], round(F['paid_rate_w25'] - F['paid_rate_w24'], 1)])
    for col, w in zip('ABCD', [42, 16, 16, 16]):
        ws.column_dimensions[col].width = w
    for row in ws.iter_rows(min_row=5, max_row=9):
        row[1].number_format = row[2].number_format = '#,##0' if row[0].value == 'Trials started' else '0.0'
        row[3].number_format = '0.0'

    ws = wb.create_sheet('Programmes')
    ws.append(['The winter release slate cost about %s of this winter\'s paid conversions' % '{:,}'.format(F['conv_slate'])])
    ws['A1'].font = Font(bold=True, size=12)
    ws.append(['Against the same months a year earlier, at this winter\'s trials; to the nearest hundred.'])
    ws.append([])
    ws.append(['Programme', 'Paid conversions lost to its cause', 'Rank'])
    for c in ws[4]:
        c.font = head
        c.fill = fill
    vals = {'C': F['conv_slate'], 'A': F['conv_price'], 'B': F['conv_recovery'], 'D': F['conv_channel']}
    rank = {k: i + 1 for i, k in enumerate(sorted(vals, key=lambda k: -F['_raw'][k]))}
    for k in ('A', 'B', 'C', 'D'):
        ws.append([PROG_NAMES[k], vals[k], rank[k]])
    ws.append([])
    ws.append(['Fund', PROG_NAMES[F['pick']]])
    ws.append(['Runner-up', PROG_NAMES[F['runner_up']]])
    ws.append(['Gap between them (paid conversions)', F['conv_gap']])
    ws.append([])
    ws.append(['Waterfall', 'Paid conversions'])
    ws.cell(row=ws.max_row, column=1).font = head
    ws.append(['Last winter\'s conversion rate at this winter\'s trials', F['waterfall_start']])
    ws.append(['Winter release slate', -F['conv_slate']])
    ws.append(['First-month price', -F['conv_price']])
    ws.append(['First-charge recovery', -F['conv_recovery']])
    ws.append(['Paid acquisition mix', -F['conv_channel']])
    ws.append(['This winter\'s paid conversions', F['waterfall_end']])
    for col, w in zip('ABC', [52, 32, 8]):
        ws.column_dimensions[col].width = w
    for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
        if isinstance(row[1].value, (int, float)):
            row[1].number_format = '#,##0'

    ws = wb.create_sheet('Months Feb-Oct 2025')
    ws.append(['Between the winters, conversion held near last winter\'s rate'])
    ws['A1'].font = Font(bold=True, size=12)
    ws.append(['Paid: first charge collected (standard, section 4). Episodes: episodes played during the trial, per trial (section 5).'])
    ws.append([])
    ws.append(['Month of trial start', 'Paid (%)', 'Average episodes played during the trial'])
    for c in ws[4]:
        c.font = head
        c.fill = fill
    for m in MONTHS:
        ws.append([MONTH_NAMES[m] + ' 2025', F['ask_paid_share_%s' % m], F['ask_episodes_%s' % m]])
    for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
        row[1].number_format = row[2].number_format = '0.0'
    for col, w in zip('ABC', [22, 12, 38]):
        ws.column_dimensions[col].width = w
    for sh in wb.worksheets:
        sh.freeze_panes = 'A5'
    ws = wb.create_sheet('Notes')
    notes = [
        ('Trials', 'Counted by start date in Toronto time (conversion standard v3, section 2). The old platform\'s copies '
                   'of web and phone sign-ups of 9 to 19 June 2025 are not trials and are left out.'),
        ('Paid', 'First monthly charge collected by the first attempt or a scheduled retry, on the subscription the trial '
                 'ended on (section 4).'),
        ('Episodes', 'Counted once a trial, whoever or whatever started them (section 5); smart TV rows of 8 February to '
                     '27 October 2025 cover the whole autoplay run.'),
        ('Rounding', 'Conversions to the nearest hundred; shares and averages to one decimal, from unrounded figures.'),
        ('As of', 'Register and charge exports pulled 27 February 2026; every January trial had matured.'),
    ]
    ws.append(['Notes'])
    ws['A1'].font = Font(bold=True, size=12)
    for k, v in notes:
        ws.append([k, v])
    ws.column_dimensions['A'].width = 12
    ws.column_dimensions['B'].width = 110
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        row[1].alignment = Alignment(wrap_text=True, vertical='top')
    wb.save(path)
    docs.xlsx_scrub(path, 'Kristen Hurst', '2026-03-09T16:20:00Z', 'Trial conversion review')


def waterfall_png(F):
    """The waterfall, in the validated slots: totals blue, causes orange, labels in text ink."""
    TOTAL, CAUSE, INK, MUTED, SURF = '#2a78d6', '#eb6834', '#0b0b0b', '#52514e', '#fcfcfb'
    labels = ['Last winter\'s rate at\nthis winter\'s trials', 'Winter release\nslate (C)', 'First-month\nprice (A)',
              'First-charge\nrecovery (B)', 'Paid acquisition\nmix (D)', 'This winter\'s\npaid conversions']
    start, end = F['waterfall_start'], F['waterfall_end']
    steps = [F['conv_slate'], F['conv_price'], F['conv_recovery'], F['conv_channel']]
    fig, ax = plt.subplots(figsize=(7.2, 3.6), dpi=170, facecolor=SURF)
    ax.set_facecolor(SURF)
    w = 0.58
    ax.bar(0, start, color=TOTAL, width=w, linewidth=0)
    level = start
    for i, st in enumerate(steps, 1):
        ax.bar(i, -st, bottom=level, color=CAUSE, width=w, linewidth=0)
        ax.plot([i - 1 + w / 2, i - w / 2], [level, level], color='#b9b8b3', linewidth=0.8)
        txt = '\u2212{:,}'.format(st)
        ax.text(i, level + 120, txt, ha='center', va='bottom', fontsize=8.5, color=INK,
                fontweight='bold' if i == 1 else 'normal')
        level -= st
    ax.plot([4 + w / 2, 5 - w / 2], [level, level], color='#b9b8b3', linewidth=0.8)
    ax.bar(5, end, color=TOTAL, width=w, linewidth=0)
    ax.text(0, start + 120, '{:,}'.format(start), ha='center', va='bottom', fontsize=8.5, color=INK)
    ax.text(5, end + 120, '{:,}'.format(end), ha='center', va='bottom', fontsize=8.5, color=INK)
    ax.text(1, start - F['conv_slate'] / 2, 'fund', ha='center', va='center', fontsize=8, color='white', fontweight='bold')
    ax.set_xticks(range(6))
    ax.set_xticklabels(labels, fontsize=7.4, color=MUTED)
    ax.set_ylabel('Paid conversions', fontsize=8, color=MUTED)
    ax.set_ylim(0, start * 1.13)
    ax.tick_params(axis='y', labelsize=7.5, colors=MUTED, length=0)
    ax.tick_params(axis='x', length=0)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: '{:,.0f}'.format(x)))
    ax.grid(axis='y', color='#e6e5e1', linewidth=0.6)
    ax.set_axisbelow(True)
    for sp in ('top', 'right', 'left'):
        ax.spines[sp].set_visible(False)
    ax.spines['bottom'].set_color('#b9b8b3')
    ax.set_title('The release slate, not the price, took this winter\'s paid conversions', fontsize=9.5, loc='left',
                 color=INK)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', facecolor=SURF, metadata={'Software': None})
    plt.close(fig)
    buf.seek(0)
    return buf


def note(path, F):
    body, h, t, small = docs.styles()
    R = F['_raw']

    def story():
        s = [Paragraph('Fund the winter release slate for November 2026', t),
             Paragraph('To: subscriber growth budget review, March 2026. From: Subscriber Growth Analytics. 9 March 2026. '
                       'Subject: the 2025-26 winter fall in trial-to-paid conversion and the programme to fund.', small),
             Spacer(1, 6),
             Paragraph('Fund the winter release slate (C). Paid conversion of the November to January trials fell from '
                       '%.1f to %.1f per cent. At this winter\'s trials that is about %s paid conversions; about %s of them '
                       'went with the winter\'s release slate, about %s with the new first-month price, and about %s each '
                       'with first-charge recovery and the paid acquisition mix. The price hold is the runner-up, about %s '
                       'conversions behind.'
                       % (F['paid_rate_w24'], F['paid_rate_w25'], '{:,}'.format(F['conv_fall']),
                          '{:,}'.format(F['conv_slate']), F['conv_price'], F['conv_recovery'], '{:,}'.format(F['conv_gap'])),
                       body),
             Paragraph('Why the slate and not the price: a trialist pays at day 7 when a season they are watching still '
                       'has episodes to come. Last winter %.1f per cent of trialists were playing a season that was still '
                       'releasing when their trial ended, and they paid at %.1f per cent against %.1f per cent for the rest. '
                       'This winter nothing new aired after the autumn finales of 24 and 31 October, so no trialist had a '
                       'season still to come. Among trialists with nothing to come, conversion fell only from %.1f to %.1f '
                       'per cent between the winters, and that small fall is where the price, recovery and the channel mix '
                       'sit. The drop on 1 November looks like the price because the finales and the price change landed '
                       'the same week, and sign-ups on finished seasons fell too because last winter those trialists went '
                       'on to watch Marrow Creek while it aired.'
                       % (F['runway_share_w24'], F['paid_rate_w24_runway'], F['paid_rate_w24_norunway'],
                          F['paid_rate_w24_norunway'], F['paid_rate_w25']), body),
             Image(waterfall_png(F), width=6.6 * inch, height=3.3 * inch),
             Paragraph('Trials started 1 November to 31 January in each winter, by start date in Toronto time; paid '
                       'conversions to the nearest hundred. Sources: trial register, both processors\' first-charge '
                       'attempts, trial viewing, release calendar.', small),
             Spacer(1, 4),
             Paragraph('The stages show the same thing: the share of trials that played an episode held (%.1f against '
                       '%.1f per cent), the share still subscribed at the end of the trial fell from %.1f to %.1f, and '
                       'first-charge collection slipped from %.1f to %.1f per cent with the shorter retry schedule.'
                       % (F['stage_played_w24'], F['stage_played_w25'], F['stage_subscribed_w24'], F['stage_subscribed_w25'],
                          F['stage_collected_w24'], F['stage_collected_w25']), body),
             Paragraph('The slate needs Gravel & Gold locked by July to air from November (programme sheet, line C). '
                       'Stage shares are of each winter\'s trials, first charges collected of those attempted (conversion '
                       'standard, section 3). Trials started 25 to 31 October 2025, whose first charge fell under the new '
                       'price, sit in neither winter. Detail: trial_conversion_review.xlsx.', small)]
        return s

    docs.pdf(path, 'Winter trial conversion: what to fund', 'Kristen Hurst', docs.stamp_tuple(2026, 3, 9), story)
