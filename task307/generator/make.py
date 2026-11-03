"""Build task307's pack (target/), goldens (golden/), figures.json and target.zip.

    python3 task307/generator/make.py
"""
import datetime as dt
import io
import json
import os
import shutil
import zipfile
import numpy as np
import world as Wm
import truth as Tm
import office
from world import UNITS, RATED, L, local, NH

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, 'target')
GOLD = os.path.join(TASK, 'golden')
OLD_TAGS = ['OSD_U1', 'OSD_U2', 'SDL_U1', 'SDL_U2', 'SDL_U3', 'NES_U1', 'NES_U2']
NEW_TAG = {u: u + '.P' for u in UNITS}
OLD_END = L(2023, 3, 21)              # the old historian's last exported hour is 20 March 2023 23:00 local
NEW_START = L(2023, 3, 18)            # the new historian's first hour, 18 March 2023 00:00 local
SLOT_UNIT = {'OSD_U1': 'OSD-G1', 'OSD_U2': 'OSD-G2', 'SDL_U1': 'SDL-G1', 'SDL_U2': 'SDL-G2', 'SDL_U3': 'SDL-G3',
             'NES_U1': 'NSV-G1', 'NES_U2': 'NSV-G2'}


def rnd(x, step):
    return int(np.floor(x / step + 0.5) * step)


def comma(x, nd=1):
    return ('%.*f' % (nd, x)).replace('.', ',')


def write_csv(name, header, rows, sep=','):
    import csv
    with open(os.path.join(TGT, name), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter=sep, lineterminator='\r\n')
        w.writerow(header)
        w.writerows(rows)


def old_source(tag, i):
    """The unit whose output an old-historian tag carried in hour i (slot wiring before each RTU replacement)."""
    st = tag[:3].replace('NES', 'NSV')
    if i < L(*Wm.RTU_NEW[st]):
        return Wm.OLD_SLOT[tag]
    return SLOT_UNIT[tag]


def historian(W):
    out = W['out']
    rows = []
    for i in range(OLD_END):
        rows.append([local(i).strftime('%d.%m.%Y %H:%M')] + [comma(out[old_source(t, i)][i], 2) for t in OLD_TAGS])
    write_csv('historian_export_2016_2023.csv', ['Tidspunkt'] + OLD_TAGS, rows, sep=';')
    rows = []
    for i in range(NEW_START, NH):
        t = (Wm.T0 + dt.timedelta(hours=i)).strftime('%Y-%m-%dT%H:%M:%SZ')
        rows.append([t] + ['%.3f' % out[u][i] for u in UNITS])
    write_csv('historian_export_2023_2026.csv', ['time_utc'] + [NEW_TAG[u] for u in UNITS], rows)
    rows = [[t, NEW_TAG[SLOT_UNIT[t]], '%s %s active power, hourly mean' % (Wm.STATION[SLOT_UNIT[t][:3]], SLOT_UNIT[t][-2:]), 'MW']
            for t in OLD_TAGS]
    write_csv('historian_tag_map_2023.csv', ['old_tag', 'new_tag', 'description', 'eng_unit'], rows)


def xlsx_save(wb, path, author, created, modified, title=''):
    b = io.BytesIO()
    wb.save(b)
    raw = office.resave(b.getvalue(), 'xlsx', author, created, modified, title=title)
    with open(path, 'wb') as f:
        f.write(raw)


def unit_register():
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Aggregater'
    ws.append(['Aggregat', 'Stasjon', 'Ytelse (MW)', 'Turbintype', 'Idriftsatt', 'Løpehjul', 'Løpehjul montert'])
    since = {'OSD-G1': '12.07.2004', 'OSD-G2': '06.09.2004', 'SDL-G1': '17.08.2009', 'SDL-G2': '22.07.2019',
             'SDL-G3': '24.06.2024', 'NSV-G1': '30.06.2008', 'NSV-G2': '27.05.2015'}
    for u in UNITS:
        ws.append([u, Wm.STATION[u[:3]], RATED[u], 'Francis, vertikal', Wm.COMMISSIONED[u], Wm.RUNNER_IN[u][-1][1], since[u]])
    for c in ws[1]:
        c.font = Font(bold=True)
    for col, w in zip('ABCDEFG', (11, 13, 12, 17, 11, 10, 17)):
        ws.column_dimensions[col].width = w
    ws2 = wb.create_sheet('Driftsområder')
    ws2.append(['Område', 'Fra og med (andel av ytelse)', 'Til (andel av ytelse)'])
    ws2.append(['Normal', '58 %', '100 %'])
    ws2.append(['Begrenset', '30 %', '58 %'])
    ws2.append(['Start og stopp', '0 %', '30 %'])
    for c in ws2[1]:
        c.font = Font(bold=True)
    ws2.column_dimensions['A'].width = 16
    ws2.column_dimensions['B'].width = 28
    ws2.column_dimensions['C'].width = 22
    ws3 = wb.create_sheet('Stasjoner')
    ws3.append(['Stasjon', 'Aggregater', 'Nettilknytning', 'Linjebryter'])
    for st, grid in (('OSD', 'Storstølen'), ('SDL', 'Sørdalseid'), ('NSV', 'Fjordbotn')):
        ws3.append([Wm.STATION[st], ', '.join(u for u in UNITS if u[:3] == st), '%d kV-linje til %s transformatorstasjon' % (LINE_KV, grid),
                    'Ja, med gjeninnkobling'])
    for c in ws3[1]:
        c.font = Font(bold=True)
    for col, w in zip('ABCD', (13, 26, 40, 22)):
        ws3.column_dimensions[col].width = w
    xlsx_save(wb, os.path.join(TGT, 'unit_register.xlsx'), 'Arild Sivertsen', '2019-02-11T08:14:00Z', '2024-06-28T13:42:00Z')


def inspections(W):
    import openpyxl
    from openpyxl.styles import Font
    rng = np.random.default_rng(9307)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Inspeksjoner'
    ws.append(['Løpehjul', 'Dato', 'Aggregat', 'Funn totalt (cm²)'] + ['Skovl %02d' % k for k in range(1, 14)] +
              ['Bånd', 'Reparert', 'Etter reparasjon (cm²)', 'Merknad'])
    recs = [(dt.date(*p['date']), p['runner'], p['unit'], p['found'], p['repaired_to']) for p in W['pre_insp']]
    recs += [(local(f['i']).date(), f['runner'], f['unit'], f['found'], f['repaired_to']) for f in W['found']]
    recs.sort(key=lambda r: (r[0], r[1]))
    for (d, rn, u, f, rep) in recs:
        if f > 0:
            w = rng.dirichlet(np.full(14, 6.0))
            parts = np.round(w * f, 1)
            parts[-1] = round(f - parts[:-1].sum(), 1)
        else:
            parts = np.zeros(14)
        note = ''
        if rn == 'R-208':
            note = 'nytt løpehjul, mottakskontroll'
        elif rn == 'R-410' and d.year == 2015:
            note = 'demontert, sendt til verksted'
        elif rn == 'R-410' and d.year == 2019:
            note = 'reservehjul montert'
        elif rn == 'R-207' and d.year == 2024:
            note = 'demontert, kassert'
        elif rn == 'R-206' and d.year == 2019:
            note = 'demontert'
        ws.append([rn, d.strftime('%d.%m.%Y'), u, comma(f)] + [comma(p) for p in parts] +
                  ['Ja' if rep is not None else 'Nei', comma(rep) if rep is not None else '', note])
    for c in ws[1]:
        c.font = Font(bold=True)
    xlsx_save(wb, os.path.join(TGT, 'runner_inspections.xlsx'), 'Arild Sivertsen', '2016-09-02T10:05:00Z', '2024-07-03T09:21:00Z')


def maintenance(W):
    rows = []
    for u in UNITS:
        for d0 in W['annual'][u]:
            rows.append([d0.isoformat(), u, 'annual maintenance start', 'unit out of service'])
            rows.append([(d0 + dt.timedelta(days=10)).isoformat(), u, 'annual maintenance end', 'returned to service'])
        for (s, e) in Wm.OVERHAULS[u]:
            rows.append([dt.date(*s).isoformat(), u, 'overhaul start', 'planned overhaul, unit out of service'])
            rows.append([dt.date(*e).isoformat(), u, 'overhaul end', 'returned to service'])
    rows += [
        ['2016-03-14', '', 'runner shop', 'R-410 weld repaired at the runner shop, held as spare'],
        ['2016-08-01', '', 'control system', 'Øvre Sørdal station RTU replaced, new RTU in service'],
        ['2017-06-12', '', 'control system', 'Sørdal station RTU replaced, new RTU in service'],
        ['2017-07-24', '', 'control system', 'Nesvik station RTU replaced, new RTU in service'],
        ['2019-06-11', 'SDL-G2', 'runner removed', 'R-206 removed at overhaul and scrapped'],
        ['2019-07-22', 'SDL-G2', 'runner installed', 'spare runner R-410 installed'],
        ['2021-03-01', '', 'maintenance system', 'new maintenance system in service'],
        ['2022-01-01', 'SDL-G1', 'reserve duty', 'frequency containment reserve (FCR-N) contract in force'],
        ['2022-01-01', 'NSV-G1', 'reserve duty', 'frequency containment reserve (FCR-N) contract in force'],
        ['2023-03-18', '', 'historian', 'new station historian in service'],
        ['2023-03-20', '', 'historian', 'old station historian stopped'],
        ['2024-06-24', 'SDL-G3', 'runner installed', 'new runner R-208 installed, R-207 scrapped'],
    ]
    rows.sort(key=lambda r: (r[0], r[1]))
    write_csv('maintenance_history.csv', ['date', 'unit', 'event', 'detail'], rows)


def counters(W):
    rows = []
    k = 0
    for r in sorted(Tm.counter_readings(W), key=lambda r: (r['date'], r['unit'])):
        k += 1
        wo = ('AO-%05d' % (31000 + k * 37)) if r['date'] < dt.date(2021, 3, 1) else ('WO%07d' % (4100000 + k * 113))
        rows.append([r['date'].isoformat(), r['unit'], wo, r['kind'], r['hours'], r['starts']])
    write_csv('unit_counter_readings.csv', ['date', 'unit', 'work_order', 'reading', 'running_hours_total', 'starts_total'],
              rows)


LINE_KV = 132
LINE = {st: '%d kV %s' % (LINE_KV, far) for st, far in (('OSD', 'Storstølen'), ('SDL', 'Sørdalseid'), ('NSV', 'Fjordbotn'))}
UNIT_FN = ['stator earth fault 64S', 'loss of excitation 40', 'voltage restrained overcurrent 51V', 'generator differential 87G',
           'reverse power 32', 'overspeed 12', 'guide bearing temperature 38', 'overvoltage 59']
LINE_FN = ['distance protection zone 1', 'distance protection zone 2', 'directional earth fault 67N']


def trip_log(W):
    """The control centre's protection log: every protection operation, its breaker and the reclosure that followed,
    plus pick-ups that started a protection function without operating it. UTC to the second."""
    r = np.random.default_rng(5307)
    rows = []

    def ts(sec):
        return (Wm.T0 + dt.timedelta(seconds=int(sec))).strftime('%Y-%m-%d %H:%M:%S')
    for e in W['trips']:
        st = Wm.STATION[e['station']]
        if e['kind'] in ('long', 'quick'):
            obj = e['unit']
            fns = list(r.choice(UNIT_FN, size=1 + int(r.random() < 0.3), replace=False))
            for k, fn in enumerate(fns):
                rows.append([ts(e['t0'] + k), st, obj, 'protection operated', fn])
            rows.append([ts(e['t0'] + len(fns) - 1), st, obj, 'breaker open', 'generator breaker, trip'])
            rows.append([ts(e['t1']), st, obj, 'breaker closed', 'generator breaker, synchronised'])
        else:
            obj = LINE[e['station']]
            fns = list(r.choice(LINE_FN, size=1 + int(r.random() < 0.4), replace=False))
            for k, fn in enumerate(fns):
                rows.append([ts(e['t0'] + k), st, obj, 'protection operated', fn])
            rows.append([ts(e['t0'] + len(fns) - 1), st, obj, 'breaker open', 'line breaker, trip'])
            rows.append([ts(e['t1']), st, obj, 'breaker closed', 'line breaker, synchrocheck reclose'])
    # pick-ups without operation, on units and lines alike
    for st in ('OSD', 'SDL', 'NSV'):
        objs = [u for u in UNITS if u[:3] == st] + [LINE[st]]
        for _ in range(int(r.integers(180, 260))):
            o = objs[int(r.integers(0, len(objs)))]
            fn = LINE_FN[int(r.integers(0, len(LINE_FN)))] if o.startswith('132') else UNIT_FN[int(r.integers(0, len(UNIT_FN)))]
            rows.append([ts(int(r.integers(3 * 86400, NH * 3600 - 3 * 86400))), Wm.STATION[st], o, 'protection started', fn])
    rows.sort(key=lambda x: x[0])
    write_csv('protection_log_2016_2026.csv', ['time_utc', 'station', 'object', 'event', 'detail'], rows)


def contracts():
    rows = []
    prices = {2022: 18.4, 2023: 26.1, 2024: 21.7, 2025: 17.9, 2026: 16.2}
    mw = {'SDL-G1': 10.0, 'NSV-G1': 9.0}
    k = 0
    for y in range(2022, 2027):
        for u in ('SDL-G1', 'NSV-G1'):
            k += 1
            rows.append(['FCRN-%d-%03d' % (y, 17 + k * 7 % 90), u, 'FCR-N', '%d-01-01' % y, '%d-12-31' % y, '%.1f' % mw[u],
                         '%.2f' % prices[y]])
    write_csv('reserve_contracts_2022_2026.csv', ['contract_id', 'unit', 'product', 'valid_from', 'valid_to', 'capacity_mw',
                                                  'price_eur_per_mw_h'], rows)


def distractors():
    rng = np.random.default_rng(1307)
    rows = []
    d = dt.date(2016, 1, 1)
    base = {'Øvre Sørdal magasin': 9.0, 'Sørdalsvatn': 14.0, 'Nesvikvatn': 11.5}
    while d <= dt.date(2026, 12, 31):
        doy = d.timetuple().tm_yday
        flood = np.exp(-((doy - 160) / 28.0) ** 2) * 4.2 + np.exp(-((doy - 290) / 22.0) ** 2) * 1.6 + 0.35
        for r, b in base.items():
            rows.append([d.isoformat(), r, '%.2f' % (b * flood * rng.lognormal(0, 0.28))])
        d += dt.timedelta(days=1)
    write_csv('reservoir_inflow_daily_2016_2026.csv', ['date', 'reservoir', 'inflow_m3s'], rows)
    rows = []
    d = dt.date(2022, 1, 1)
    lvl = 95.0
    while d <= dt.date(2026, 12, 31):
        lvl = max(4.0, lvl * 0.985 + 1.4 + rng.normal(0, 6.5))
        rows.append([d.isoformat(), 'NO5', '%.2f' % lvl])
        d += dt.timedelta(days=1)
    write_csv('day_ahead_prices_NO5_2022_2026.csv', ['date', 'bidding_zone', 'price_eur_mwh'], rows)


def docs(gen_report):
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    ss = getSampleStyleSheet()
    body = ParagraphStyle('b', parent=ss['BodyText'], fontSize=9.5, leading=13)
    h = ParagraphStyle('h', parent=ss['Heading2'], fontSize=11.5, spaceBefore=8)

    def P(t, s=body):
        return Paragraph(t, s)

    def std():
        return [P('Sørdal Kraft AS', ss['Title']), P('Technical standard TS-07: Francis runners', h),
                P('Revision 3, approved 14 March 2024. Owner: Production assets.'), Spacer(1, 8),
                P('1 Scope', h), P('This standard applies to the Francis runners of Øvre Sørdal, Sørdal and Nesvik power stations.'),
                P('2 General', h), P('2.1 Condition limits in this standard apply to the runner, whichever unit it is installed in. '
                  'A runner moved between units carries its inspection history with it.'),
                P('3 Inspections', h), P('3.1 Runners are inspected at each planned overhaul. Pitting is mapped blade by blade and on '
                  'the band and recorded in the inspection register.'),
                P('4 Cavitation pitting', h), P('4.1 Pitting is recorded as the area of runner surface with cavitation pitting, in '
                  'square centimetres.'),
                P('4.2 Pitting means the total pitted area of the runner\'s blades and band. The repair limit is 2,400 cm2 of pitting.'),
                P('5 Repairs', h), P('5.1 A weld repair is recorded in the register with the pitting left after the repair.'),
                P('6 Removal and outage planning', h), P('6.1 A runner whose pitting passes the repair limit is removed for shop repair. '
                  'For outage planning the removal is counted as an unplanned outage of 14 weeks beginning on 1 December of the year in '
                  'which the runner\'s pitting passes the limit.')]
    office.pdf(os.path.join(TGT, 'runner_standard_TS07_rev3.pdf'), 'TS-07 Francis runners', 'Rita Haugen', '20240314101500', std)

    def quotes():
        data = [['Unit', 'Runner', 'Scope', 'Price excl. VAT (NOK)', 'VAT 25 % (NOK)', 'Total (NOK)']]
        for u in UNITS:
            p = Wm.QUOTE_MNOK[u] * 1e6
            data.append([u, Wm.RUNNER_IN[u][-1][1], 'shop refurbishment', '{:,.0f}'.format(p), '{:,.0f}'.format(p * 0.25),
                         '{:,.0f}'.format(p * 1.25)])
        t = Table(data, repeatRows=1)
        t.setStyle(TableStyle([('FONT', (0, 0), (-1, -1), 'Helvetica', 8), ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 8),
                               ('GRID', (0, 0), (-1, -1), 0.4, colors.grey), ('ALIGN', (3, 1), (-1, -1), 'RIGHT')]))
        return [P('Vestlandet Turbinservice AS', ss['Title']), P('Quotation 2027-114 to Sørdal Kraft AS', h),
                P('Date: 6 November 2026. Valid to 31 March 2027. Price for one runner refurbishment in the 2027 summer window, '
                  'including transport, shop work, balancing and reinstallation support.'), Spacer(1, 8), t]
    office.pdf(os.path.join(TGT, 'runner_refurbishment_quote_2027.pdf'), 'Quotation 2027-114', 'Vestlandet Turbinservice AS',
               '20261106141000', quotes)

    def report():
        data = [['Station', '2024 (GWh)', '2025 (GWh)']]
        for st in ('OSD', 'SDL', 'NSV'):
            data.append([Wm.STATION[st], '%.1f' % gen_report[(st, 2024)], '%.1f' % gen_report[(st, 2025)]])
        t = Table(data)
        t.setStyle(TableStyle([('FONT', (0, 0), (-1, -1), 'Helvetica', 9), ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 9),
                               ('GRID', (0, 0), (-1, -1), 0.4, colors.grey)]))
        return [P('Sørdal Kraft AS', ss['Title']), P('Production report 2025', h), P('Generation by station', h), t, Spacer(1, 10),
                P('Definitions', h),
                P('Generation is gross energy at the generator terminals, taken from the station historian with each hour\'s mean '
                  'output in MW counted as that hour\'s MWh. Years and months are in Norwegian local time.'),
                P('A start is a run-up of a unit from standstill to generation; the governors count every start.'),
                P('A trip is an unplanned disconnection of a generating unit from the grid by protection.'),
                P('Reserve income is reported in the financial statements and is not part of this report.')]
    office.pdf(os.path.join(TGT, 'production_report_2025.pdf'), 'Production report 2025', 'Rita Haugen', '20260219090500', report)

    import docx
    d = docx.Document()
    d.add_heading('Outage planning note 2027', level=1)
    paras = [
        '1 Basis',
        '1.1 The note covers the seven units of Øvre Sørdal, Sørdal and Nesvik and the runners installed in them at 31 December 2026.',
        '1.2 Condition is stated at 31 December 2026.',
        '1.3 The planning window is 2027 to 2031: outages beginning in those years.',
        '2 Summer window',
        '2.1 The 2027 summer window, 7 June to 10 September, has crane, crew and runner-shop capacity for one runner refurbishment.',
        '2.2 A refurbished runner returns to service with its pitting repaired and does not reach the repair limit inside the '
        'planning window.',
        '2.3 Units other than the one refurbished keep their present runners through the planning window.',
        '2.4 For planning, each unit is assumed to run in each year of the planning window as it ran in 2026.',
        '3 Unplanned runner outages',
        '3.1 An unplanned runner outage is counted as in TS-07 section 6.1: 14 weeks from 1 December of the year the runner passes '
        'the repair limit.',
        '3.2 The outage is valued at the unit\'s mean generation over the 14 weeks from 1 December, Norwegian time, in each of the '
        'last five winters, 2021/22 to 2025/26, in MWh at the generator terminals.',
        '4 Cost',
        '4.1 Refurbishment cost is the runner shop\'s 2027 quotation excluding VAT, in NOK million.',
    ]
    words = 0
    for t in paras:
        if t[0].isdigit() and t[1] == ' ':
            d.add_heading(t, level=2)
        else:
            d.add_paragraph(t)
        words += len(t.split())
    b = io.BytesIO()
    d.save(b)
    raw = office.resave(office.lean_docx(b.getvalue()), 'docx', 'Rita Haugen', '2026-11-20T08:02:00Z', '2026-12-09T15:37:00Z',
                        title='Outage planning note 2027', words=words, rev=7)
    with open(os.path.join(TGT, 'outage_planning_note_2027.docx'), 'wb') as f:
        f.write(raw)


def golden(rows, order, tg, ts, tt):
    import openpyxl
    from openpyxl.styles import Font, Alignment
    os.makedirs(GOLD, exist_ok=True)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Runner decision'
    ws.append(['2027 summer runner refurbishment: runner condition at 31 December 2026 and generation at risk in 2027 to 2031'])
    ws['A1'].font = Font(bold=True, size=12)
    ws.append([])
    ws.append(['Unit', 'Runner', 'Last inspection', 'Pitting at last inspection (cm²)', 'Pitting at 31 Dec 2026 (cm²)',
               'Year pitting passes 2,400 cm²', 'Generation lost to the outage (MWh)', 'Quote excl. VAT (NOK m)',
               'Generation spared per NOK m (MWh)', 'Generation 2016 to 2026 (MWh)', 'Starts 2016 to 2026', 'Trips 2016 to 2026'])
    for c in ws[3]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical='top')
    for u in UNITS:
        r = rows[u]
        ws.append([u, r['runner'], r['last_date'].strftime('%d.%m.%Y'), rnd(r['last_pitting'], 10), rnd(r['now'], 10),
                   r['cross'] if r['cross'] else 'not before 2032', rnd(r['gen_mwh'], 100), Wm.QUOTE_MNOK[u],
                   rnd(r['per_mnok'], 10), rnd(tg[u], 100), ts[u], tt[u]])
    ws.append([])
    a, b = order[0], order[1]
    ws.append(['Refurbish in 2027', a, '', '', '', '', rnd(rows[a]['gen_mwh'], 100), '', rnd(rows[a]['per_mnok'], 10)])
    ws.append(['Runner-up', b, '', '', '', '', rnd(rows[b]['gen_mwh'], 100), '', rnd(rows[b]['per_mnok'], 10)])
    ws.append(['Lead over the runner-up (MWh per NOK m)', '', '', '', '', '', '', '',
               rnd(rows[a]['per_mnok'], 10) - rnd(rows[b]['per_mnok'], 10)])
    ws.append([])
    ws.append(['Pitting carried from each runner\'s last inspection at %.3f cm² per hour run between 30 and 58 per cent of '
               'rated output, the rate the inspection pairs 2016 to 2024 give; 2026 duty carried through 2031 (note 2.4).'
               % rows[a]['rate']])
    ws.append(['Starts count every run-up from standstill, the restarts after a trip inside the same hour included (protection '
               'log, tied to the governor start counters at each overhaul); trips count each unit\'s own breaker trips and the '
               '132 kV line trips that disconnected it while generating. Old historian tags before each RTU replacement '
               're-assigned to the units their logged outages match.'])
    for row in ws.iter_rows(min_row=4, max_row=ws.max_row):
        for c in row:
            if isinstance(c.value, (int, float)) and not isinstance(c.value, bool):
                if c.column_letter == 'H':
                    c.number_format = '0.0'
                elif c.column_letter == 'F':
                    c.number_format = '0'
                else:
                    c.number_format = '#,##0'
    ws.freeze_panes = 'B4'
    for col, w in zip('ABCDEFGHIJKL', (24, 9, 13, 14, 14, 13, 15, 11, 14, 15, 11, 10)):
        ws.column_dimensions[col].width = w
    ws.row_dimensions[3].height = 58
    xlsx_save(wb, os.path.join(GOLD, 'runner_2027.xlsx'), 'Rita Haugen', '2027-01-12T09:10:00Z', '2027-01-14T16:22:00Z',
              title='Runner refurbishment 2027')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams['svg.hashsalt'] = 'sordal-2027'
    vals = [rnd(rows[u]['per_mnok'], 10) for u in UNITS]
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.bar(UNITS, vals, color=['#1f5a96' if u == a else '#b7c4d4' for u in UNITS])
    for k, v in enumerate(vals):
        ax.text(k, v + 60, '{:,}'.format(v), ha='center', fontsize=8)
    ax.set_ylabel('MWh spared per NOK million')
    ax.set_title('Generation spared in 2027 to 2031 per NOK million of refurbishment', fontsize=10)
    k = UNITS.index(a)
    ax.annotate('refurbish 2027', xy=(k, vals[k]), xytext=(k - 1.9, vals[k] * 0.92), fontsize=8,
                arrowprops=dict(arrowstyle='->', lw=0.8))
    ax.spines[['top', 'right']].set_visible(False)
    fig.tight_layout()
    svg = io.StringIO()
    fig.savefig(svg, format='svg', metadata={'Date': None, 'Creator': None})
    plt.close(fig)
    text = svg.getvalue().replace('id="matplotlib.axis_1"', 'id="x-axis"').replace('id="matplotlib.axis_2"', 'id="y-axis"')
    with open(os.path.join(GOLD, 'runner_2027.svg'), 'w', encoding='utf-8') as f:
        f.write(text)


SOURCES = {
    'historian_export_2016_2023.csv': 'old station historian, hourly export by RTU tag, local time',
    'historian_export_2023_2026.csv': 'new station historian, hourly export by unit tag, UTC',
    'historian_tag_map_2023.csv': 'historian migration tag map, 2023',
    'unit_register.xlsx': 'unit register (production assets)',
    'runner_inspections.xlsx': 'runner inspection register',
    'maintenance_history.csv': 'maintenance system event history',
    'unit_counter_readings.csv': 'maintenance system counter readings at overhauls',
    'reserve_contracts_2022_2026.csv': 'frequency reserve contract register',
    'protection_log_2016_2026.csv': 'control centre protection log',
    'runner_standard_TS07_rev3.pdf': 'technical standard TS-07 revision 3',
    'outage_planning_note_2027.docx': 'outage planning note 2027',
    'runner_refurbishment_quote_2027.pdf': 'runner shop quotation 2027-114',
    'production_report_2025.pdf': 'annual production report 2025',
    'reservoir_inflow_daily_2016_2026.csv': 'reservoir inflow series',
    'day_ahead_prices_NO5_2022_2026.csv': 'day-ahead price series, bidding zone NO5',
}
DISTRACTORS = {
    'reservoir_inflow_daily_2016_2026.csv': 'inflow sets how much each station can run but enters no figure: generation, duty and '
                                            'pitting are read from the units\' own output',
    'day_ahead_prices_NO5_2022_2026.csv': 'the planning note values an outage in MWh at the terminals, not in money, so no price '
                                          'enters the call or an ask',
    'reserve_contracts_2022_2026.csv': 'the reserve contracts name two units and their prices; no graded figure reads them, the '
                                       'units\' duty being in their own output record',
}


def write_metadata():
    files = sorted(os.listdir(TGT))
    meta = {'task': 'task307', 'title': 'Sørdal Kraft: the 2027 summer runner refurbishment',
            'domain': 'Energy Systems & Utilities (hydropower asset condition)', 'client_domain': 'Energy Systems & Utilities',
            'task_type': 'asset-condition-maintenance', 'objective': 'Opportunity Sizing & Decision Support',
            'deliverables': ['runner_2027.xlsx', 'runner_2027.svg'], 'as_of': '2027-01-15',
            'files': [{'file': f, 'source': 'synthetic, task307 generator: ' + SOURCES[f], 'date': '2027-01-15',
                       'license': 'generated for this task, no third-party data', 'distractor': f in DISTRACTORS} for f in files],
            'distractors': [{'file': f, 'reason': r} for f, r in sorted(DISTRACTORS.items())],
            'rows': {f: sum(1 for _ in open(os.path.join(TGT, f), encoding='utf-8')) - 1 for f in files if f.endswith('.csv')}}
    with open(os.path.join(TASK, 'metadata.json'), 'w', encoding='utf-8') as fh:
        json.dump(meta, fh, indent=1, ensure_ascii=False)
        fh.write('\n')


def zip_target():
    with zipfile.ZipFile(os.path.join(TASK, 'target.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        for n in sorted(os.listdir(TGT)):
            zi = zipfile.ZipInfo('target/' + n, date_time=(2027, 1, 15, 8, 30, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            with open(os.path.join(TGT, n), 'rb') as f:
                z.writestr(zi, f.read())


def main():
    W = Wm.build()
    if os.path.isdir(TGT):
        shutil.rmtree(TGT)
    os.makedirs(TGT)
    rows, order = Tm.call(W, 'rz')
    gen, starts, run, rz = Tm.unit_year_stats(W)
    tg, ts = Tm.totals(W)
    tt = Tm.trip_counts(W)
    gen_report = {(st, y): sum(gen[(u, y)] for u in UNITS if u.startswith(st)) / 1000.0 for st in ('OSD', 'SDL', 'NSV')
                  for y in (2024, 2025)}
    historian(W)
    unit_register()
    inspections(W)
    maintenance(W)
    counters(W)
    trip_log(W)
    contracts()
    distractors()
    docs(gen_report)
    golden(rows, order, tg, ts, tt)
    a, b = order[0], order[1]
    figs = {'call': {'chosen': a, 'runner_up': b, 'chosen_gen_mwh': rnd(rows[a]['gen_mwh'], 100),
                     'chosen_per_mnok': rnd(rows[a]['per_mnok'], 10), 'runner_up_per_mnok': rnd(rows[b]['per_mnok'], 10),
                     'gap_per_mnok': rnd(rows[a]['per_mnok'], 10) - rnd(rows[b]['per_mnok'], 10)},
            'units': {u: {'runner': rows[u]['runner'], 'last_inspection': rows[u]['last_date'].isoformat(),
                          'last_pitting_cm2': rnd(rows[u]['last_pitting'], 10), 'now_cm2': rnd(rows[u]['now'], 10),
                          'cross_year': rows[u]['cross'], 'gen_mwh': rnd(rows[u]['gen_mwh'], 100),
                          'quote_mnok': Wm.QUOTE_MNOK[u], 'per_mnok': rnd(rows[u]['per_mnok'], 10)} for u in UNITS},
            'asks': {'generation_2016_2026_mwh': {u: rnd(tg[u], 100) for u in UNITS},
                     'starts_2016_2026': {u: ts[u] for u in UNITS},
                     'trips_2016_2026': {u: tt[u] for u in UNITS}},
            'rate_cm2_per_rough_zone_hour': round(rows[a]['rate'], 4), 'limit_cm2': 2400, 'outage_weeks': 14,
            'band_per_cent_of_rating': [30, 58], 'line_kv': LINE_KV}
    with open(os.path.join(HERE, 'figures.json'), 'w', encoding='utf-8') as f:
        json.dump(figs, f, indent=1, ensure_ascii=False)
        f.write('\n')
    write_metadata()
    zip_target()
    print('built', len(os.listdir(TGT)), 'files; chosen', a, 'runner-up', b)


if __name__ == '__main__':
    main()
