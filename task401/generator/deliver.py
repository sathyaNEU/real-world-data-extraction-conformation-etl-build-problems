"""task401 golden deliverables under golden/: change_review.pdf (the memo, with its chart) and monthly_return.xlsx."""
import os, io
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.platypus import Image, Paragraph, Spacer
from reportlab.lib.units import mm
import docs

HERE = os.path.dirname(os.path.abspath(__file__))
GOLD = os.path.join(os.path.dirname(HERE), 'golden')
LABEL = {'A': 'Rewards closed (1 Feb)', 'D': 'Legacy terms letters (2 Feb)', 'C': 'Daytime timetable (12 Jan)', 'E': 'Shorter hours, Northgate and Westcroft (9 Feb)'}


def chart(F, P):
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9})
    order = list(F['order'])[::-1]
    lab = {'A': 'Rewards closed (1 Feb)', 'D': 'Legacy terms letters (2 Feb)', 'C': 'Daytime timetable (12 Jan)',
           'E': 'Shorter hours at two centres (9 Feb)'}
    so = np.array([P[k]['so_far'] for k in order]); yr = np.array([P[k]['so_far'] + P[k]['excess_idle'] * P[k]['conv'] for k in order])
    fig, ax = plt.subplots(figsize=(7.0, 3.3), dpi=150)
    y = np.arange(len(order))
    ax.barh(y + 0.19, so, height=0.36, color='#a9bccf', label='Cancelled by 16 March')
    ax.barh(y - 0.19, yr, height=0.36, color='#2f5d8a', label='Over the 2026-27 membership year')
    for i in range(len(order)):
        for val, off in ((so[i], 0.19), (yr[i], -0.19)):
            v = int(round(val)) if off > 0 else int(round(val, -1))
            ax.text(val + (18 if val >= 0 else -18), i + off, '{:,}'.format(v), va='center', ha='left' if val >= 0 else 'right', fontsize=8)
    ax.axvline(0, color='#777777', lw=0.8)
    ax.set_yticks(y); ax.set_yticklabels([lab[k] for k in order])
    ax.set_xlim(min(so.min(), yr.min(), 0) - 160, max(so.max(), yr.max()) + 170)
    ax.set_xlabel('Members lost, net of the same weeks of 2025-26')
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=8, frameon=False)
    for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
    fig.tight_layout()
    b = io.BytesIO(); fig.savefig(b, format='png', metadata={'Software': None}); plt.close(fig)
    b.seek(0)
    return b


def memo(F, P, path):
    c = F['cost']
    blocks = [('title', 'Which of the February changes to reverse'),
              ('sub', 'Membership. Prepared for the 2026-27 plan, from the extract of 16 March 2026.'),
              ('h', 'Answer'),
              ('p', 'Reverse the closure of Rewards. On the trust\'s records it will cost about %d members over the 2026-27 membership year '
                    '(2 February 2026 to 31 January 2027), roughly %.1f times the legacy terms letters, the next largest at about %d.'
                    % (c['A'], F['lead'], c['D'])),
              ('p', 'The letters produced February\'s spike: %d more legacy members asked to leave by 16 March than in the same weeks of 2025. '
                    'Almost all of them had stopped coming months before, and on last year\'s record most of that group would have left '
                    'during the year anyway; legacy members not visiting are now %d fewer than a year ago, so the year\'s net cost of the '
                    'letters is much smaller than the spike.' % (F['so_far']['D'], -F['excess_idle']['D'])),
              ('p', 'The closure has barely shown in cancellations yet (%+d against last year), but %d more Rewards holders have made no '
                    'visit in the last 28 days than at the same point last year. They are still paying. Last year %.1f per cent of holders '
                    'in that position cancelled before the membership year ended, so most of the closure\'s cost is still to come.'
                    % (F['so_far']['A'], F['excess_idle']['A'], F['conv_pct']['A'])),
              ('h', 'Why each of the others costs fewer members'),
              ('p', 'Daytime timetable: about %d over the year. Older class users came less often after 12 January and some stopped for a '
                    'while, but the group is small and last year only %.1f per cent of its members in that position went on to cancel.'
                    % (c['C'], F['conv_pct']['C'])),
              ('p', 'Shorter hours at Northgate and Westcroft: about nil (%+d). Visits at the two centres fell, but members moved to other '
                    'centres and times; there are fewer of their members not visiting than a year ago.' % c['E']),
              ('p', 'Member care calls: they reduce cancellations rather than add to them. The team calls members who have stopped '
                    'coming, and some come back.'),
              ('h', 'Members lost to each change over the year')]
    img = chart(F, P)
    flow_extra = [Image(img, width=165 * mm, height=72 * mm)]
    tail = [('p', 'Each change is read on the members it applies to (Schedule 4, 4.3, and the savings programme paper), set against '
                  'the same weeks of 2025-26. The year\'s cost is the cancellations so far plus the change in members not visiting, '
                  'carried through at the rate last year\'s members in the same position went on to cancel by the end of that year.')]
    from reportlab.platypus import SimpleDocTemplate
    flow = []
    for kind, val in blocks:
        flow.append(Paragraph(val, docs.ST[kind]))
    flow += flow_extra + [Spacer(1, 4)]
    for kind, val in tail:
        flow.append(Paragraph(val, docs.ST[kind]))
    buf = io.BytesIO()
    from reportlab.lib.pagesizes import A4
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm, bottomMargin=16 * mm,
                            title='Which of the February changes to reverse', author='Sophie Newman', creator=docs.WORD, producer=docs.WORD)
    doc.build(flow)
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import NameObject, TextStringObject, DictionaryObject
    r = PdfReader(io.BytesIO(buf.getvalue())); w = PdfWriter()
    for pg in r.pages: w.add_page(pg)
    w._info = w._add_object(DictionaryObject({NameObject('/Title'): TextStringObject('Which of the February changes to reverse'),
                                              NameObject('/Author'): TextStringObject('Sophie Newman'),
                                              NameObject('/Creator'): TextStringObject(docs.WORD), NameObject('/Producer'): TextStringObject(docs.WORD),
                                              NameObject('/CreationDate'): TextStringObject("D:20260318143000+00'00'"),
                                              NameObject('/ModDate'): TextStringObject("D:20260318143000+00'00'")}))
    b2 = io.BytesIO(); w.write(b2)
    open(path, 'wb').write(b2.getvalue())


def workbook(F, path):
    mon = [('2025-10', 'October 2025'), ('2025-11', 'November 2025'), ('2025-12', 'December 2025'), ('2026-01', 'January 2026'), ('2026-02', 'February 2026')]
    adm = pd.DataFrame([dict(month=lab, northgate_and_westcroft=F['admissions']['%s NW' % m], other_centres=F['admissions']['%s other' % m]) for m, lab in mon])
    fee = pd.DataFrame([dict(month=lab, legacy_tariffs_gbp=F['fees']['%s legacy' % m], tariffs_2023_gbp=F['fees']['%s 2023' % m]) for m, lab in mon[1:]])
    from openpyxl import Workbook
    wb = Workbook(); ws = wb.active; ws.title = 'Admissions'
    ws.append(['Month', 'Northgate and Westcroft', 'Other centres'])
    for r in adm.itertuples(index=False): ws.append(list(r))
    ws2 = wb.create_sheet('Fees')
    ws2.append(['Month paid for', 'Legacy tariffs (GBP)', '2023 tariffs (GBP)'])
    for r in fee.itertuples(index=False): ws2.append(list(r))
    for s in (ws, ws2):
        for col, wdt in zip('ABC', (16, 24, 20)): s.column_dimensions[col].width = wdt
    for row in ws2.iter_rows(min_row=2, min_col=2, max_col=3):
        for c in row: c.number_format = '#,##0'
    wb.save(path)
    docs.scrub_xlsx(path, 'Sophie Newman', '2026-03-17T09:20:00Z', '2026-03-18T14:25:00Z', (2026, 3, 18, 14, 25, 0))


def run(R):
    os.makedirs(GOLD, exist_ok=True)
    F, P = R['F'], R['mc']['parts']
    memo(F, P, os.path.join(GOLD, 'change_review.pdf'))
    workbook(F, os.path.join(GOLD, 'monthly_return.xlsx'))
