"""task401 golden deliverables under golden/: the committee report (maths_change_review.docx, with its chart) and the
table by school (support_and_staffing_by_school.csv), every figure from figures.json."""
import io
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import docx
from docx.shared import Pt, Cm

import docs

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
GD = os.path.join(TASK, 'golden')
AUTHOR = 'Aimee Williams'
CHANGE = {'A': 'the new mathematics framework', 'B': 'the homework platform switch (Mathsbridge for Corvella)',
          'C': 'the asymmetric week (S3 maths from five periods to four)', 'D': 'the support bases',
          'E': 'the shared maths posts'}
SHORT = {'Ardcorrie Academy': 'Ardcorrie', 'Balmorran High School': 'Balmorran', 'Glenwhinnie Academy': 'Glenwhinnie',
         'Kilbraith Academy': 'Kilbraith', 'Lochbrannie High School': 'Lochbrannie', 'Muirlees High School': 'Muirlees',
         "St Moluag's High School": "St Moluag's", 'Torranbrae High School': 'Torranbrae'}


def r100(x):
    return int(round(x / 100.0)) * 100


def chart(F):
    sch = sorted(F['by_school'])
    a = [F['by_school'][s]['2025'] for s in sch]
    b = [F['by_school'][s]['2026'] for s in sch]
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8.5})
    fig, ax = plt.subplots(figsize=(7.2, 3.3), dpi=150)
    x = range(len(sch))
    ax.bar([i - 0.2 for i in x], a, width=0.4, color='#9bb7d4', label='June 2025')
    ax.bar([i + 0.2 for i in x], b, width=0.4, color='#1f4e79', label='June 2026')
    for i in x:
        ax.text(i - 0.2, a[i] + 0.3, '%.1f' % a[i], ha='center', va='bottom', fontsize=6.5)
        ax.text(i + 0.2, b[i] + 0.3, '%.1f' % b[i], ha='center', va='bottom', fontsize=6.5)
    ax.set_xticks(list(x))
    ax.set_xticklabels([SHORT[s] for s in sch], rotation=0, fontsize=7)
    ax.set_ylabel('Mean mark (out of 60)')
    ax.set_ylim(0, 40)
    ax.set_title('Mean June common paper mark by school, S1 to S3', fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(frameon=False, fontsize=7, loc='upper right', ncol=2)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', metadata={'Software': None})
    plt.close(fig)
    buf.seek(0)
    return buf


def report(F):
    c, h, ex = F['costs'], F['head'], F['extra']
    d = docx.Document()
    st = d.styles['Normal']
    st.font.name = 'Calibri'
    st.font.size = Pt(11)
    def para(text, bold=False, size=None):
        p = d.add_paragraph()
        r = p.add_run(text)
        r.bold = bold
        if size:
            r.font.size = Pt(size)
        return p
    para('Education Committee', size=9.5)
    para('S1 to S3 mathematics: the 2025-26 change that cost the most marks in June 2026', bold=True, size=15)
    para('Report by the Performance and Improvement Lead, Education Service. June 2026.', size=9.5)
    para('Recommendation', bold=True, size=12)
    para('The change that cost S1 to S3 pupils the most marks in the June 2026 common papers was the homework platform '
         'switch, Mathsbridge in place of Corvella (change B). The committee is asked to recommend that the 2027-28 budget '
         'reverses it.')
    para('What happened in June', bold=True, size=12)
    para('%s pupils sat the June 2025 papers and %s sat the same papers in June 2026. The mean mark fell from %.1f to %.1f '
         'out of 60, and the share of pupils at 36 or more fell from %.1f%% (%s pupils) to %.1f%% (%s pupils). Every school '
         'fell (chart).' % ('{:,}'.format(h['2025']['sat']), '{:,}'.format(h['2026']['sat']), h['2025']['mean'],
                             h['2026']['mean'], h['2025']['share'], '{:,}'.format(h['2025']['secure']), h['2026']['share'],
                             '{:,}'.format(h['2026']['secure'])))
    d.add_picture(chart(F), width=Cm(16))
    para('Why the platform switch', bold=True, size=12)
    para('The two changes that reached every pupil on the same day, the framework and the platform switch, cannot be told '
         'apart by comparing groups of pupils, so we compared each pupil\'s own units. Taking the units each pupil got most '
         'wrong in their first homework on the unit (their bottom third by first-attempt accuracy), those units sat %.1f '
         'points of a unit\'s marks below the same pupil\'s other units in June 2025, under Corvella, and %.1f points below '
         'in June 2026, under Mathsbridge. Corvella\'s weekly retrieval tasks were drawn for each pupil from the skills they '
         'had got wrong; Mathsbridge sets each class the same review. The units pupils first struggled with stopped coming '
         'back to them, and stayed weak to June, across every school and year group.'
         % (-100 * ex['exB_2025'], -100 * ex['exB_2026']))
    para('Why each other change cost fewer marks', bold=True, size=12)
    para('Framework (A): the four rewritten units in each year group did fall further than each pupil\'s other units '
         'against June 2025, but by less than each pupil\'s weak units fell, and they are four units of twelve; the '
         'carried-over units fell no further than the platform effect explains.')
    para('Asymmetric week (C): it reached S3 pupils only (%s sat), whose shortfall against S1 and S2 grew a little against '
         'June 2025 once P7 attainment and free school meals are allowed for.' % '{:,}'.format(F['reach']['C']))
    para('Support bases (D): the heaviest loss a pupil of any change, but it reached only the %s pupils referred to a base '
         'who sat in June.' % F['reach']['D'])
    para('Shared posts (E): it reached the %s pupils in the split classes, and only from January.' % '{:,}'.format(F['reach']['E']))
    para('Base use and teaching continuity by school', bold=True, size=12)
    t = d.add_table(rows=1, cols=3)
    t.style = 'Table Grid'
    for i, x in enumerate(['School', 'Maths lessons missed in a base', 'Classes with more than one teacher']):
        t.rows[0].cells[i].text = x
    for s in sorted(F['ask_lessons']):
        row = t.add_row().cells
        row[0].text, row[1].text, row[2].text = s, str(F['ask_lessons'][s]), str(F['ask_classes'][s])
    para('Lessons are S1 to S3 maths lessons a pupil was signed in to a base for any part of, from 3 November to the papers, '
         'booked to the pupil\'s own school and to the class they were in on the day. Classes count the people who taught '
         'each S1 to S3 maths class on the timetable over the session.', size=9.5)
    d.core_properties.author = AUTHOR
    path = os.path.join(GD, 'maths_change_review.docx')
    d.save(path)
    docs.scrub_docx(path, AUTHOR, (2026, 6, 19, 16, 40, 0), '2026-06-19T15:05:00Z')


def table(F):
    lines = ['school,maths_lessons_missed_in_base,classes_with_more_than_one_teacher']
    for s in sorted(F['ask_lessons']):
        name = '"%s"' % s if ',' in s else s
        lines.append('%s,%d,%d' % (name, F['ask_lessons'][s], F['ask_classes'][s]))
    open(os.path.join(GD, 'support_and_staffing_by_school.csv'), 'w').write('\n'.join(lines) + '\n')


def run(F):
    os.makedirs(GD, exist_ok=True)
    for f in os.listdir(GD):
        os.remove(os.path.join(GD, f))
    report(F)
    table(F)
