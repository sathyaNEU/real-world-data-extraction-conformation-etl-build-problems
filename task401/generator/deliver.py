"""task401: the golden deliverables, coldmere_ammonia_briefing.pptx (with the drill-down chart) and
coldmere_evidence.xlsx. Graded figures are read from generator/figures.json; the chart's series and the day list are
computed from target/ with golden.py. Nothing is typed.

    python3 deliver.py            writes <task>/golden/
"""
import io, json, os, re, sys, zipfile
from datetime import date, datetime, timedelta
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import golden as G  # noqa: E402

TASK = os.path.dirname(HERE)
T = os.path.join(TASK, 'target')
OUT = os.path.join(TASK, 'golden')
F = json.load(open(os.path.join(HERE, 'figures.json')))
MONTH_NAMES = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June', '07': 'July',
               '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}
STAMP = (2026, 11, 9, 16, 20, 0)
AUTHOR = 'Gerard Norris'


def month_label(m):
    return '%s %s' % (MONTH_NAMES[m[5:]], m[:4])


def series():
    days = G.monitor_days(T)
    fe = G.historian_fe(T)
    ev = sorted(G.dairy_events(T))
    exc = G.exceedances(days, *G.WIN)
    span = [G.WIN[0] + timedelta(days=i) for i in range((G.WIN[1] - G.WIN[0]).days + 1)]
    return days, fe, ev, exc, span


def chart(days, fe, ev, exc, span):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8.5, 'svg.hashsalt': 'task401'})
    fig, axs = plt.subplots(3, 1, figsize=(10.0, 4.9), dpi=200, sharex=True,
                            gridspec_kw={'height_ratios': [2.2, 2.0, 0.8], 'hspace': 0.18})
    acc, grey, dark = '#b5452b', '#7d8a96', '#2f3b47'
    ax = axs[0]
    ax.plot(span, [days.get(d, float('nan')) for d in span], color=grey, lw=1.0)
    ax.scatter(exc, [days[d] for d in exc], s=12, color=acc, zorder=3, label='Exceedance day')
    ax.axhline(0.6, color=dark, lw=0.8, ls='--')
    ax.text(span[-1] + timedelta(days=1), 0.6, ' 0.6 standard', va='center', fontsize=7.5, color=dark)
    ax.set_ylabel('River ammonia\nmg/l as N, day mean')
    ax.set_title('1  River Allery below Coldmere: day means at the downstream monitor', loc='left', fontsize=9)
    ax = axs[1]
    ax.plot(span, [fe.get(d, float('nan')) for d in span], color=grey, lw=1.0)
    ax.scatter(exc, [fe[d] for d in exc], s=12, color=acc, zorder=3)
    ax.set_ylabel('Final effluent\nmg/l as N, day mean')
    ax.set_title('2  Coldmere WRC: final effluent ammonia from the historian, exceedance days in red', loc='left', fontsize=9)
    ax = axs[2]
    evw = [d for d in ev if span[0] - timedelta(days=2) <= d <= span[-1]]
    ax.vlines(evw, 0, 1, color=dark, lw=1.1)
    ax.set_yticks([])
    ax.set_ylim(0, 1)
    ax.set_title('3  Thornlea Dairy: evenings with a whey discharge in its chamber record', loc='left', fontsize=9)
    for a in axs:
        for s in ('top', 'right'):
            a.spines[s].set_visible(False)
        a.grid(axis='y', color='#e3e6e9', lw=0.6)
    axs[2].xaxis.set_major_locator(mdates.MonthLocator())
    axs[2].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    axs[2].set_xlim(span[0] - timedelta(days=2), span[-1] + timedelta(days=1))
    fig.subplots_adjust(left=0.09, right=0.93, top=0.95, bottom=0.07)
    buf = io.BytesIO()
    fig.savefig(buf, format='png', metadata={'Software': None})
    plt.close(fig)
    buf.seek(0)
    return buf


def deck(png, exc):
    from pptx import Presentation
    from pptx.util import Emu, Pt, Inches
    from pptx.dml.color import RGBColor
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]
    navy, ink, mute = RGBColor(0x1f, 0x3a, 0x52), RGBColor(0x22, 0x22, 0x22), RGBColor(0x5a, 0x63, 0x6b)

    def text(slide, x, y, w, h, paras, size=16, colour=ink, bold_first=False):
        tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        for i, ptxt in enumerate(paras):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = ptxt
            p.space_after = Pt(8)
            for r in p.runs:
                r.font.size = Pt(size)
                r.font.name = 'Calibri'
                r.font.color.rgb = colour
                r.font.bold = bool(bold_first and i == 0)
        return tb

    def header(slide, title, n):
        bar = slide.shapes.add_shape(1, 0, 0, prs.slide_width, Inches(0.12))
        bar.fill.solid(); bar.fill.fore_color.rgb = navy; bar.line.fill.background()
        text(slide, 0.6, 0.35, 12.1, 1.0, [title], size=26, colour=navy)
        text(slide, 0.6, 6.95, 9.0, 0.4, ['Wendmoor Water, Environment Programme. Coldmere ammonia investigation, '
                                         'November 2026.'], size=10, colour=mute)
        text(slide, 12.2, 6.95, 0.6, 0.4, [str(n)], size=10, colour=mute)

    s = prs.slides.add_slide(blank)
    bar = s.shapes.add_shape(1, 0, 0, prs.slide_width, Inches(0.12))
    bar.fill.solid(); bar.fill.fore_color.rgb = navy; bar.line.fill.background()
    text(s, 0.8, 2.3, 11.5, 1.4, ['Coldmere ammonia: what drove the River Allery\'s failures this winter'], size=34, colour=navy)
    text(s, 0.8, 3.9, 11.5, 1.2, ['Evidence for the environment programme submission, January 2027',
                                  'Environment Programme, Wendmoor Water. November 2026'], size=16, colour=mute)

    s = prs.slides.add_slide(blank)
    header(s, 'Thornlea Dairy\'s evening whey discharges drive the failures; the upgrade would not stop them', 2)
    text(s, 0.6, 1.6, 12.0, 5.0, [
        'The downstream monitor recorded %d exceedance days from November 2025 to March 2026, against %d in the same '
        'months a year earlier.' % (F['exc_window'], F['exc_prior']),
        'All %d fell on the first or second day after an evening on which Thornlea Dairy ran acid whey to its trade '
        'effluent drain, as its own fifteen-minute chamber record shows. None fell on the works\' load and the cold alone.'
        % F['dairy_reach'],
        'The whey\'s oxygen demand reaches Coldmere overnight, the blowers cannot hold the oxygen, nitrification stops for '
        'a day and the works\' effluent ammonia passes to the river until the nitrifiers recover.',
        'The ammonia-based aeration control and the nitrification upgrade each reach %d of the %d days. Stopping the whey '
        'discharges at the dairy reaches all %d.' % (F['upgrade_reach'], F['exc_window'], F['dairy_reach'])], size=18)

    s = prs.slides.add_slide(blank)
    header(s, 'Every exceedance day sits one or two days after a Thornlea whey evening', 3)
    s.shapes.add_picture(png, Inches(0.6), Inches(1.35), width=Inches(12.1))
    text(s, 0.6, 6.55, 12.0, 0.4, ['Sources: Allery downstream monitor (UK days, valid readings, as the investigation terms '
                                   'define them); Coldmere historian; Thornlea Dairy chamber record under its consent.'],
         size=10, colour=mute)

    s = prs.slides.add_slide(blank)
    header(s, 'The control, the cold and the works\' capacity reach none of the exceedance days', 4)
    text(s, 0.6, 1.6, 12.0, 5.0, [
        'The control went into service on 27 October 2025, a week before the dairy\'s new line started on 3 November. '
        'Dates alone cannot separate them, and a process model on temperature, load and the go-live books the winter to '
        'the control.',
        'The record does separate them: no exceedance day in either winter fell without a whey discharge on one of the two '
        'evenings before, and on every other day the works met the river standard, in the coldest weeks and at the '
        'highest loads included.',
        'The oxygen sags the historian shows on the mornings after a discharge look like the control\'s own night-load '
        'sags; only the dairy\'s record tells them apart.',
        'The dairy\'s weekly composites and pH log pass its consent, so the charging and compliance records never flagged '
        'it: its composites run Wednesday to Thursday and no discharge fell on a Wednesday evening.'], size=17)

    s = prs.slides.add_slide(blank)
    header(s, 'Take the upgrade out of the ammonia answer and act at Thornlea', 5)
    text(s, 0.6, 1.6, 12.0, 5.0, [
        'Do not put the GBP %.1f million nitrification upgrade into the submission as the answer to the Allery\'s ammonia: '
        'it would have prevented none of this winter\'s %d exceedance days.' % (F['upgrade_cost_m'], F['exc_window']),
        'Review Thornlea Dairy\'s consent (option 3 in the terms): contained whey storage with a collection backstop, a '
        'condition on whey reaching the drain, and continuous flow and pH reporting in the evenings.',
        'Keep the aeration control in service; it is not behind the failures.',
        'Re-read the monitor against the dairy\'s record over the first full month after the dairy\'s measures are in.'],
         size=18)

    s = prs.slides.add_slide(blank)
    header(s, 'The evidence workbook carries the days by month and the trade effluent figures', 6)
    text(s, 0.6, 1.6, 12.0, 5.0, [
        'Exceedance days by month for both winters, with each exceedance day and the whey evening before it.',
        'Each trade discharger\'s chargeable volume and its settled COD and suspended solids strengths for 2025-26, under '
        'the 2025-26 charges scheme.'], size=18)

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, 'coldmere_ammonia_briefing.pptx')
    cp = prs.core_properties
    cp.author = AUTHOR; cp.last_modified_by = AUTHOR; cp.title = 'Coldmere ammonia investigation'
    cp.created = datetime(2026, 11, 6, 10, 12); cp.modified = datetime(2026, 11, 9, 16, 20); cp.revision = 7
    cp.subject = ''; cp.keywords = ''; cp.comments = ''; cp.category = ''
    prs.save(path)
    scrub_office(path, 'Microsoft Office PowerPoint')
    return path


def workbook(days, fe, ev, exc):
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment
    wb = Workbook()
    ws = wb.active
    ws.title = 'Exceedance days'
    ws.append(['Month', 'Exceedance days 2025-26', 'Month a year earlier', 'Exceedance days 2024-25'])
    win, prv = list(F['exc_by_month_window'].items()), list(F['exc_by_month_prior'].items())
    for (m1, n1), (m0, n0) in zip(win, prv):
        ws.append([month_label(m1), n1, month_label(m0), n0])
    ws.append(['Total', F['exc_window'], 'Total', F['exc_prior']])

    ws2 = wb.create_sheet('Exceedance day list')
    ws2.append(['Exceedance day', 'River day mean (mg/l as N)', 'Works final effluent day mean (mg/l as N)',
                'Thornlea whey evening before', 'Days after the evening'])
    for d in exc:
        before = [e for e in ev if 1 <= (d - e).days <= 2]
        e = max(before)
        ws2.append([d, round(days[d], 2), round(fe[d], 1), e, (d - e).days])

    ws3 = wb.create_sheet('Trade effluent 2025-26')
    ws3.append(['Discharger', 'Chargeable volume (m3)', 'Settled COD strength (mg/l)', 'Suspended solids strength (mg/l)'])
    for name in sorted(F['ask_a']):
        v = F['ask_a'][name]
        ws3.append([name, v['volume'], v['ot'], v['st']])
    ws4 = wb.create_sheet('Notes')
    ws4.append(['Note'])
    for line in (
            'Exceedance day: a UK day whose mean of valid fifteen-minute ammonium readings at the downstream monitor is above '
            '0.6 mg/l as N; readings flagged at a maintenance visit are not valid and a day needs 72 valid readings '
            '(investigation terms, section 2).',
            'Winters compared: 1 November 2025 to 31 March 2026 against 1 November 2024 to 31 March 2025 (investigation '
            'terms, section 2).',
            'Whey evening: an evening on which Thornlea Dairy\'s chamber record shows low pH at '
            'production flow after 20:00; an exceedance day is counted against the latest such evening one or two days '
            'before it.',
            'Chargeable volume: the advance between the 00:00 reads on 1 April 2025 and 1 April 2026, taken meter by meter '
            'where a meter was exchanged, times the consent\'s register multiplier, less the consent\'s allowance '
            '(charges scheme 2025-26, section 3).',
            'Strengths: the means over the composites collected at the consented sampling point in 2025-26; a composite that '
            'filled a second bottle is taken at the strength of the effluent both bottles hold, each bottle weighted by the '
            'volume in the samplers\' download log (charges scheme 2025-26, section 4).',
            'Sources: Allery downstream monitor export, Coldmere historian, Thornlea Dairy chamber record, trade effluent '
            'meter reads, round sheets, sampler downloads and laboratory results, as exported on 19 October 2026.'):
        ws4.append([line])
    ws4.column_dimensions['A'].width = 120
    for r in ws4.iter_rows(min_row=2):
        r[0].alignment = Alignment(wrap_text=True, vertical='top')

    for w in (ws, ws2, ws3):
        w.freeze_panes = 'A2'
    for w in (ws, ws2, ws3, ws4):
        for c in w[1]:
            c.font = Font(bold=True)
            c.alignment = Alignment(wrap_text=True, vertical='top')
        w.row_dimensions[1].height = 32
    for col, wd in zip('ABCD', (16, 22, 20, 22)):
        ws.column_dimensions[col].width = wd
    for col, wd in zip('ABCDE', (15, 16, 20, 18, 12)):
        ws2.column_dimensions[col].width = wd
    for r in ws2.iter_rows(min_row=2):
        r[0].number_format = 'dd/mm/yyyy'; r[3].number_format = 'dd/mm/yyyy'
    for col, wd in zip('ABCD', (26, 16, 18, 20)):
        ws3.column_dimensions[col].width = wd
    for r in ws3.iter_rows(min_row=2, max_row=1 + len(F['ask_a'])):
        r[1].number_format = '#,##0'; r[2].number_format = '#,##0'; r[3].number_format = '#,##0'
    wb.properties.creator = AUTHOR; wb.properties.lastModifiedBy = AUTHOR
    wb.properties.created = datetime(2026, 11, 6, 9, 41); wb.properties.modified = datetime(2026, 11, 9, 15, 58)
    path = os.path.join(OUT, 'coldmere_evidence.xlsx')
    wb.save(path)
    scrub_office(path, 'Microsoft Excel')
    return path


def scrub_office(path, app):
    src = zipfile.ZipFile(path)
    items = [(i.filename, src.read(i.filename)) for i in src.infolist()]
    src.close()
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in items:
            if name == 'docProps/app.xml':
                data = re.sub(rb'<Application>[^<]*</Application>', b'<Application>' + app.encode() + b'</Application>', data)
                if b'<Application>' not in data:
                    data = data.replace(b'</Properties>', b'<Application>' + app.encode() + b'</Application></Properties>')
                data = re.sub(rb'<AppVersion>[^<]*</AppVersion>', b'<AppVersion>16.0000</AppVersion>', data)
            if name == 'docProps/core.xml':
                data = re.sub(rb'python-pptx|openpyxl', AUTHOR.encode(), data)
            zi = zipfile.ZipInfo(name, date_time=STAMP); zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)


if __name__ == '__main__':
    days, fe, ev, exc, span = series()
    png = chart(days, fe, ev, exc, span)
    print(deck(png, exc))
    print(workbook(days, fe, ev, exc))
