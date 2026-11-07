"""Build task214: target/, golden/, figures.json, metadata.json, target.zip.  python3 build.py [seed]"""
import datetime as dt
import json
import os
import shutil
import sys
import zipfile

import world
import pack
import golden
import docs

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, 'target')
GOLD = os.path.join(TASK, 'golden')
SEED = 214
MTIME = dt.datetime(2027, 10, 19, 7, 40).timestamp()

FILES = {
    'lines': 'public_health/case_line_list_cryptosporidiosis_2027.xlsx',
    'rating': 'council/rating_connections_2027-10-18.parquet',
    'census': 'public_health/meshblock_usually_resident_2023_by_supply_zone.csv',
    'register': 'council/supply_zone_register_issue7.pdf',
    'network': 'council/network_model_export_2027-10-01.xlsx',
    'valveops': 'council/valve_operations_2027-07-01_2027-10-18.csv',
    'wos': 'council/work_orders_2027-07-01_2027-10-18.csv',
    'renewal': 'council/kowhai_hills_feed_main_renewal_plan_revB.pdf',
    'tor': 'public_health/outbreak_control_team_terms_of_reference_v1-1.pdf',
    'measures': 'council/water_services_performance_measures_2027-28.pdf',
    'lab': 'laboratories/community_lab_faecal_parasites_2027-07-01_2027-10-18.csv',
    'ref': 'laboratories/reference_lab_cryptosporidium_typing_2027.xlsx',
    'crm': 'council/crm_water_contacts_2027-07-01_2027-10-18.csv',
    'web': 'council/website_water_quality_reports_2027.csv',
    'sr': 'council/service_requests_2027-07-01_2027-10-18.csv',
    'jobs': 'council/crew_job_times_2027.xlsx',
    'ah': 'council/afterhours_service_calls_2027.csv',
    'rain': 'council/rainfall_daily_council_gauges_2027.csv',
    'samples': 'council/drinking_water_compliance_samples_2027.csv',
    'plant': 'council/treatment_plant_daily_log_2027.csv',
}
DISTRACTORS = ['rain', 'samples', 'plant']


def d(x):
    return x.isoformat() if x else ''


def make(seed=SEED, write=True):
    W = world.simulate(seed)
    trunk, mains, valves = pack.network(seed)
    ops, wos_rep = pack.operations(seed, W, trunk, valves)
    plan = pack.renewal_plan(seed, trunk, valves)
    mbs = pack.census(seed)
    reg, _ = pack.register(seed, mbs)
    case_rows = pack.cases(seed, W, reg)
    lab_rows, ref_rows = pack.laboratory(seed, case_rows, reg)
    crm, web = pack.complaints(seed, reg)
    srs, jobs, ah, wos_plan = pack.callouts(seed, wos_rep, reg)
    rain, samples, plant = pack.distractors(seed, W)
    S = dict(W=W, trunk=trunk, mains=mains, valves=valves, ops=ops, wos_rep=wos_rep, plan=plan, mbs=mbs, reg=reg,
             cases=case_rows, lab=lab_rows, ref=ref_rows, crm=crm, web=web, srs=srs, jobs=jobs, ah=ah,
             wos_plan=wos_plan, rain=rain, samples=samples, plant=plant)
    if write:
        write_target(S)
    return S


def write_target(S):
    if os.path.exists(TARGET):
        shutil.rmtree(TARGET)
    for sub in sorted({v.split('/')[0] for v in FILES.values()}):
        os.makedirs(os.path.join(TARGET, sub))
    P = lambda k: os.path.join(TARGET, FILES[k])
    # line list
    rows = []
    for c in S['cases']:
        rows.append([c['case'], c['nhi'], c['surname'], c['given'], d(c['dob']), c['sex'], c['address'], c['suburb'],
                     c['mb'], d(c['onset']), d(c['specimen']), d(c['report']), c['status'], c['hosp'], c['tap'],
                     c['pool'], c['animal'], c['childcare'], c['travel']])
    pack.write_xlsx(P('lines'), [('Line list', ['Case ID', 'NHI', 'Surname', 'Given name', 'Date of birth', 'Sex',
                                                'Home address', 'Suburb or town', 'Meshblock 2023', 'Onset date',
                                                'Specimen date', 'Notified', 'Case status', 'Hospitalised',
                                                'Tap water glasses per day', 'Public pool in last 2 weeks',
                                                'Farm animal contact', 'Childcare attendance', 'Overseas travel'], rows)],
                    'Public Health Service', 'Cryptosporidiosis line list', dt.datetime(2027, 10, 10, 23, 52),
                    dt.datetime(2027, 10, 18, 18, 12))
    # rating database
    reg = S['reg']
    pack.write_parquet(P('rating'), dict(
        valuation_ref=[r['valuation'] for r in reg], property_address=[r['address'] for r in reg],
        suburb_locality=[r['suburb'] for r in reg], supply_type=[r['supply'] for r in reg],
        water_connection=[r['connection'] for r in reg], supply_zone=[r['zone'] for r in reg],
        connected_date=[d(r['connected']) for r in reg], rating_category=[r['category'] for r in reg],
        meshblock_2023=[r['mb'] for r in reg]))
    # census by zone
    pack.write_csv(P('census'), ['meshblock_2023', 'supply_zone', 'usually_resident_population_2023'],
                   [[m['mb'], pack.ZCODE[m['zone']], m['pop']] for m in S['mbs']])
    # network model
    mrows = [[m['main_id'], m['cls'], m['frm'], m['to'], m['zone'], m['dia'], m['mat'], m['year'], m['length']] for m in S['mains']]
    vrows = [[v['valve_id'], v['tag'], v['main_id'], v['vtype'], v['normal'], v['street']] for v in S['valves']]
    nodes = sorted({m['frm'] for m in S['mains']} | {m['to'] for m in S['mains']})
    pack.write_xlsx(P('network'), [('Mains', ['main_id', 'class', 'from_node', 'to_node', 'supply_zone', 'diameter_mm',
                                              'material', 'install_year', 'length_m'], mrows),
                                   ('Valves', ['valve_id', 'field_tag', 'main_id', 'valve_type', 'normal_position', 'street'], vrows)],
                    'Kotare District Council GIS', 'Water network model export', dt.datetime(2027, 9, 30, 21, 14))
    # valve operations, local time with offset
    pack.write_csv(P('valveops'), ['operation_time', 'field_tag', 'operation', 'crew', 'work_order'],
                   [[pack.iso_local(t), tag, op, crew, wo] for t, tag, op, crew, wo in S['ops']])
    # work orders: repairs and planned maintenance
    wrows = [[w['wo'], w['wtype'], w['main'], w['street'], w['start'].strftime('%d/%m/%Y %H:%M'),
              w['finish'].strftime('%d/%m/%Y %H:%M'), w['crew']] for w in S['wos_rep'] + S['wos_plan']]
    wrows.sort(key=lambda r: (dt.datetime.strptime(r[4], '%d/%m/%Y %H:%M'), r[0]))
    pack.write_csv(P('wos'), ['work_order', 'type', 'main_id', 'street', 'started', 'completed', 'crew'], wrows)
    # documents
    docs.terms_of_reference(P('tor'))
    docs.performance_measures(P('measures'))
    docs.zone_register(P('register'), S['trunk'])
    docs.renewal_programme(P('renewal'), S['trunk'], S['plan'])
    # ask 1: laboratories
    lrows = []
    for r in S['lab']:
        lrows.append([r['acc'], r['nhi'], r['surname'], r['given'], d(r['dob']), r['sex'], r['address'], r['town'],
                      r['requester'], d(r['collected']), r['received'].strftime('%Y-%m-%d %H:%M'), 'FPAR',
                      'Faecal parasites (Cryptosporidium/Giardia antigen)', r['result'],
                      'Amended' if r.get('amended') else 'Final', r['reported'].strftime('%Y-%m-%d %H:%M')])
    pack.write_csv(P('lab'), ['accession', 'nhi', 'surname', 'given_name', 'dob', 'sex', 'address', 'town', 'requester',
                              'collected', 'received', 'test_code', 'test_name', 'result', 'report_status', 'reported'], lrows)
    refrows = [[x['racc'], x['referrer'], x['refs'], x['name'], d(x['dob']), x['nhi'], d(x['collected']), d(x['received']),
                x['result'], x['gp60'], d(x['reported'])] for x in S['ref']]
    pack.write_xlsx(P('ref'), [('Typing results', ['Lab number', 'Referring laboratory', 'Referrer reference', 'Patient',
                                                   'DOB', 'NHI', 'Date collected', 'Date received', 'Result',
                                                   'gp60 subtype', 'Report date'], refrows)],
                    'Reference Laboratory, Enteric Reference Unit', 'Cryptosporidium typing report',
                    dt.datetime(2027, 7, 18, 22, 31), dt.datetime(2027, 10, 18, 2, 47))
    # ask 2: complaints
    pack.write_csv(P('crm'), ['contact_id', 'received', 'channel', 'category', 'description', 'address_as_given',
                              'valuation_ref', 'status'],
                   [[c['cid'], c['received'].strftime('%Y-%m-%d %H:%M'), c['channel'], c['category'], c['desc'],
                     c['address'], c['vref'], c['status']] for c in S['crm']])
    pack.write_csv(P('web'), ['submission_id', 'submitted', 'name', 'address', 'issue', 'details', 'crm_case'],
                   [[w['wid'], w['submitted'].strftime('%Y-%m-%d %H:%M'), w['name'], w['address'], w['issue'], w['details'],
                     w['crm']] for w in S['web']])
    # ask 3: call-outs
    pack.write_csv(P('sr'), ['request_id', 'received', 'priority', 'problem', 'address', 'job_no', 'external_ref', 'closure_note'],
                   [[s['sr'], s['received'].strftime('%Y-%m-%d %H:%M'), s['priority'], s['problem'], s['address'], s['job'],
                     s['ext'], s['note']] for s in S['srs']])
    jrows = [[j['job'], j['sr'], j['crew'], pack.to_utc(j['dispatched']).strftime('%Y-%m-%dT%H:%M:%SZ'),
              pack.to_utc(j['onsite']).strftime('%Y-%m-%dT%H:%M:%SZ'), pack.to_utc(j['done']).strftime('%Y-%m-%dT%H:%M:%SZ')]
             for j in S['jobs']]
    pack.write_xlsx(P('jobs'), [('Jobs', ['job_no', 'request_id', 'crew', 'dispatched_utc', 'on_site_utc', 'completed_utc'], jrows)],
                    'FieldForce mobile', 'Crew job times', dt.datetime(2027, 10, 18, 18, 40))
    pack.write_csv(P('ah'), ['ah_reference', 'call_received', 'caller_address', 'problem', 'priority', 'crew_paged'],
                   [[a['ref'], pack.iso_local(a['call']), a['address'], a['problem'], a['priority'], pack.iso_local(a['paged'])]
                    for a in S['ah']])
    # distractors
    pack.write_csv(P('rain'), ['date', 'gauge', 'site', 'rainfall_mm'], [[d(x[0]), x[1], x[2], '%.1f' % x[3]] for x in S['rain']])
    pack.write_csv(P('samples'), ['sample_id', 'site', 'supply_zone', 'sampled', 'e_coli_mpn_100ml', 'total_coliforms_mpn_100ml',
                                  'free_available_chlorine_mg_l', 'turbidity_ntu'],
                   [[s['sid'], s['site'], s['zone'], s['t'].strftime('%Y-%m-%d %H:%M'), s['ecoli'], s['tc'], '%.2f' % s['fac'],
                     '%.2f' % s['turb']] for s in S['samples']])
    pack.write_csv(P('plant'), ['date', 'plant', 'raw_turbidity_ntu', 'filtered_turbidity_ntu', 'uv_dose_mj_cm2',
                                'free_chlorine_out_mg_l'], [[d(x[0]), x[1], x[2], x[3], x[4], x[5]] for x in S['plant']])
    for f in target_files():
        os.utime(os.path.join(TARGET, f), (MTIME, MTIME))


def figures(S):
    M = golden.main_figures(S['W'], S['mbs'], S['cases'])
    L = golden.lab_figures(S['lab'], S['ref'])
    C = golden.complaint_figures(S['crm'], S['web'], S['reg'])
    O = golden.callout_figures(S['srs'])
    return M, L, C, O


def target_files():
    return sorted(os.path.relpath(os.path.join(dp, f), TARGET).replace(os.sep, '/')
                  for dp, _, fs in os.walk(TARGET) for f in fs)


def zip_target():
    out = os.path.join(TASK, 'target.zip')
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in target_files():
            zi = zipfile.ZipInfo('target/' + f, pack.ZIP_DT)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, f), 'rb').read())
    os.utime(out, (MTIME, MTIME))


def labels(S):
    out = {}
    for r in world.RES:
        out[r] = (pack.RNAME[r], 'Service reservoir', pack.RNODE[r])
    for b, (za, zb) in world.ICS.items():
        mid = S['trunk'][b]['main_id']
        out[b] = ('boundary main %s (%s to %s)' % (mid, pack.ZNAME[za], pack.ZNAME[zb]), 'Boundary main', mid)
    return out


def r1(x):
    return round(x + 1e-9, 1)


def r2(x):
    return round(x + 1e-9, 2)


def figures_json(S, M, L, C, O):
    lab = labels(S)
    supplied = [a for a in golden.ASSETS if M['rd'][a] > 0]
    fig = dict(
        task='task214',
        call=dict(asset=lab[M['call']][0], asset_id=lab[M['call']][2], rate=r1(M['rate'][M['call']]),
                  cases=M['cases'][M['call']], runner_up=lab[M['runner_up']][0], runner_up_id=lab[M['runner_up']][2],
                  runner_up_rate=r1(M['rate'][M['runner_up']]), runner_up_cases=M['cases'][M['runner_up']],
                  forward_residents=M['forward_residents'], forward_zones=[pack.ZNAME[z] for z in M['fwd_zones']]),
        reservoirs={lab[r][0]: dict(cases=M['cases'][r], rate=r1(M['rate'][r]), resident_days=M['rd'][r]) for r in world.RES},
        assets_supplied={lab[a][0]: dict(cases=M['cases'][a], resident_days=M['rd'][a], rate=r1(M['rate'][a])) for a in supplied},
        asks=dict(lab=dict(tested=L['tested'], parvum=L['parvum'], hominis=L['hominis']),
                  complaints={k: {c: r2(v) for c, v in x['rates'].items()} for k, x in C.items()},
                  connections={k: x['connections'] for k, x in C.items()},
                  callouts={k: dict(urgent_attend=round(x['urgent_attend']), urgent_resolve=round(x['urgent_resolve']),
                                    nonurgent_attend=r1(x['nonurgent_attend']), nonurgent_resolve=r1(x['nonurgent_resolve']))
                            for k, x in O.items()}),
        steps=dict(confirmed_resident_cases=sum(1 for c in S['cases'] if c['status'] == 'Confirmed' and c['zkey']
                                                and golden.CASE_FROM <= c['onset'] <= golden.CASE_TO),
                   zone_residents={pack.ZNAME[z]: v for z, v in M['zres'].items()}),
        constants=dict(window_first_day=1, window_last_day=12, rate_per=100000, complaints_per=1000,
                       minimum_cases=golden.MIN_CASES))
    json.dump(fig, open(os.path.join(HERE, 'figures.json'), 'w'), indent=1, sort_keys=True)
    return fig


def onset_chart(S, path):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    counts = {}
    for c in S['cases']:
        if c['status'] == 'Confirmed' and c['zkey'] and golden.CASE_FROM <= c['onset'] <= golden.CASE_TO:
            counts[c['onset']] = counts.get(c['onset'], 0) + 1
    days = [golden.CASE_FROM + dt.timedelta(days=i) for i in range((golden.CASE_TO - golden.CASE_FROM).days + 1)]
    fed = feed_days(S)
    rise = min(x for x in days if x > fed[-1] and counts.get(x, 0) >= 2)
    plt.rcParams['font.family'] = 'DejaVu Sans'
    fig, ax = plt.subplots(figsize=(6.6, 2.6), dpi=150)
    if fed:
        start = dt.datetime.combine(fed[0], dt.time()) - dt.timedelta(hours=12)
        end = dt.datetime.combine(fed[-1], dt.time()) + dt.timedelta(hours=12)
        ax.axvspan(start, end, color='#E4E7EA', zorder=0, lw=0)
        ax.text(start - dt.timedelta(hours=6), max(counts.values()) * 0.97,
                'WM55081 supplying\nKowhai Hills and Matai Valley\n%s to %s' % (fed[0].strftime('%-d'), fed[-1].strftime('%-d %b')),
                ha='right', va='top', fontsize=6.6, color='#4A4F55')
    ax.bar(days, [counts.get(x, 0) for x in days], width=0.8, color='#3B6E8F', zorder=2)
    ax.set_ylabel('Confirmed cases', fontsize=7.5, color='#4A4F55')
    ax.set_title('Onsets rose from %s, after boundary main WM55081 fed Kowhai Hills and Matai Valley'
                 % rise.strftime('%-d %B'),
                 fontsize=8.6, loc='left', color='#22262A')
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    for side in ('left', 'bottom'):
        ax.spines[side].set_color('#9AA1A8')
    ax.yaxis.grid(True, color='#E9ECEF', lw=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=7, colors='#4A4F55')
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%-d %b'))
    ax.set_xlim(days[0] - dt.timedelta(days=1), days[-1] + dt.timedelta(days=1))
    fig.tight_layout()
    fig.savefig(path, metadata={'Software': None})
    plt.close(fig)


def feed_days(S):
    """Days in the case window on which the boundary main carried water into a zone for most of the day."""
    P = S['W']['P']
    out = []
    for d in range((golden.CASE_FROM - world.D0).days, (golden.CASE_TO - world.D0).days + 1):
        if any(pth and 'BM3' in pth for pth in P[d].values()):
            out.append(world.D0 + dt.timedelta(days=d))
    return out


def deliver(S, fig):
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Mm, Pt, RGBColor
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    if os.path.exists(GOLD):
        shutil.rmtree(GOLD)
    os.makedirs(GOLD)
    M = golden.main_figures(S['W'], S['mbs'], S['cases'])
    lab = labels(S)
    head_font = Font(name='Calibri', bold=True, size=10)
    head_fill = PatternFill('solid', fgColor='DDE3E8')
    note_font = Font(name='Calibri', italic=True, size=9, color='555555')

    def style(ws, widths, formats, header_rows=1):
        for i, w in enumerate(widths):
            ws.column_dimensions[chr(65 + i)].width = w
        for c in ws[header_rows]:
            c.font = head_font
            c.fill = head_fill
            c.alignment = Alignment(wrap_text=True, vertical='top')
        ws.row_dimensions[header_rows].height = 30
        ws.freeze_panes = 'A%d' % (header_rows + 1)
        for col, fmt in formats.items():
            for cell in ws[col][header_rows:]:
                if isinstance(cell.value, (int, float)):
                    cell.number_format = fmt

    wb = Workbook()
    ws = wb.active
    ws.title = 'Source assessment'
    ws.append(['Asset', 'Type', 'Asset ID', 'Confirmed cases (water in the 1-12 days before onset)',
               'Resident-days, 20 Aug-17 Oct', 'Attack rate per 100,000 resident-days', 'Ranked'])
    for a in sorted([a for a in golden.ASSETS if M['rd'][a] > 0], key=lambda a: -M['rate'][a]):
        ws.append([lab[a][0], lab[a][1], lab[a][2], M['cases'][a], M['rd'][a], r1(M['rate'][a]),
                   'yes' if M['cases'][a] >= golden.MIN_CASES else 'no, under 5 cases'])
    ws.append([])
    ws.append(['Take out of service', fig['call']['asset'], fig['call']['asset_id'], '', '', fig['call']['rate']])
    ws.append(['Runner-up', fig['call']['runner_up'], fig['call']['runner_up_id'], '', '', fig['call']['runner_up_rate']])
    ws.append(['Residents drinking through it during the renewal', fig['call']['forward_residents']])
    for r in range(ws.max_row - 2, ws.max_row + 1):
        ws.cell(r, 1).font = Font(name='Calibri', bold=True, size=10)
    ws.append([])
    ws.append(['Supply rebuilt for each zone and day from the valve operations log through the network model export of '
               '1 October 2027; cases from the line list, residents from the 2023 census meshblock table.'])
    ws.cell(ws.max_row, 1).font = note_font
    style(ws, [44, 16, 11, 20, 16, 16, 17], {'D': '0', 'E': '#,##0', 'F': '0.0'})
    ws.cell(ws.max_row - 2, 2).number_format = '#,##0'

    w2 = wb.create_sheet('Testing')
    w2.append(['Month collected', 'Residents tested for Cryptosporidium'])
    for (a, b, label), n in zip(pack.MONTHS, fig['asks']['lab']['tested']):
        w2.append([label, n])
    w2.append([])
    w2.append(['Typed by reference lab, 1 Jul-17 Oct', 'Residents'])
    w2.cell(w2.max_row, 1).font = head_font
    w2.cell(w2.max_row, 2).font = head_font
    w2.append(['Cryptosporidium parvum', fig['asks']['lab']['parvum'][0]])
    w2.append(['Cryptosporidium hominis', fig['asks']['lab']['hominis'][0]])
    w2.append([])
    w2.append(['Residents only, each counted once in a month (terms of reference, section 6).'])
    w2.cell(w2.max_row, 1).font = note_font
    style(w2, [36, 22], {'B': '0'})

    w3 = wb.create_sheet('Complaints')
    w3.append(['Per 1,000 connections', 'Clarity', 'Taste', 'Odour', 'Pressure or flow', 'Continuity of supply', 'Connections'])
    for k in ('July to September',):
        x = fig['asks']['complaints'][k]
        w3.append([k] + [x[c] for c in pack.CATS] + [fig['asks']['connections'][k]])
    w3.append([])
    w3.append(['Measure 4: networked connections in the rating database at 30 September 2027.'])
    w3.cell(w3.max_row, 1).font = note_font
    style(w3, [22, 10, 10, 10, 12, 12, 12], {'B': '0.00', 'C': '0.00', 'D': '0.00', 'E': '0.00', 'F': '0.00', 'G': '#,##0'})

    w4 = wb.create_sheet('Call-outs')
    w4.append(['Month notified', 'Urgent attendance (min)', 'Urgent resolution (min)', 'Non-urgent attendance (h)',
               'Non-urgent resolution (h)'])
    for m in ('July', 'August', 'September'):
        x = fig['asks']['callouts'][m]
        w4.append([m, x['urgent_attend'], x['urgent_resolve'], x['nonurgent_attend'], x['nonurgent_resolve']])
    w4.append([])
    w4.append(['Measure 3 medians, by the month the council or its after-hours service received the call.'])
    w4.cell(w4.max_row, 1).font = note_font
    style(w4, [16, 13, 13, 13, 13], {'B': '0', 'C': '0', 'D': '0.0', 'E': '0.0'})

    w5 = wb.create_sheet('Notes')
    w5.append(['Notes'])
    for line in (
            'Records: line list and laboratory exports to 18 October 2027; council records as exported at 07:40 on '
            '19 October 2027 (terms of reference, section 7).',
            'Attack rate (terms of reference, section 4): confirmed cases among residents with onset from 1 September to '
            '18 October 2027 whose supply zone received the asset\'s water for most of a day on at least one of the 1 to 12 '
            'days before onset, per 100,000 resident-days of the zones the asset supplied, 20 August to 17 October 2027. '
            'Assets whose water reached fewer than five cases are not ranked.',
            'Renewal: residents of the zones whose water would pass through the asset under the planned valve operations '
            'in plan revision B (terms of reference, section 5).',
            'Complaints and call-outs follow measures 4 and 3 of the water services performance measures 2027/28.'):
        w5.append([line])
        w5.cell(w5.max_row, 1).alignment = Alignment(wrap_text=True, vertical='top')
    w5['A1'].font = head_font
    w5.column_dimensions['A'].width = 110
    for r in range(2, w5.max_row + 1):
        w5.row_dimensions[r].height = 42
    for w in (ws, w2, w3, w4, w5):
        w.sheet_view.showGridLines = w is not w5
        w.page_setup.orientation = 'landscape'
        w.page_setup.fitToWidth = 1
    wb.properties.creator = 'Public Health Service'
    wb.properties.lastModifiedBy = 'Public Health Service'
    wb.properties.created = dt.datetime(2027, 10, 19, 3, 20)
    wb.properties.modified = dt.datetime(2027, 10, 19, 3, 20)
    xp = os.path.join(GOLD, 'outbreak_source.xlsx')
    wb.save(xp)
    pack.norm_zip(xp)

    png = os.path.join(HERE, 'onset_chart.png')
    onset_chart(S, png)
    fed = feed_days(S)
    doc = Document()
    for sec in doc.sections:
        sec.left_margin = sec.right_margin = Mm(20)
        sec.top_margin = sec.bottom_margin = Mm(15)
        fp = sec.footer.paragraphs[0]
        fp.text = 'Public Health Service, Kotare region. Outbreak Control Team, cryptosporidiosis 2027.'
        fp.runs[0].font.size = Pt(8)
        fp.runs[0].font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    doc.styles['Normal'].font.name = 'Calibri'
    doc.styles['Normal'].font.size = Pt(10)
    c = fig['call']
    t = doc.add_table(rows=4, cols=2)
    for i, (k, v) in enumerate((('To', 'Three Waters Services, Kotare District Council'),
                                ('From', 'Outbreak Control Team (chair: Dr Anna Gullery, Medical Officer of Health)'),
                                ('Date', '19 October 2027'),
                                ('Subject', 'Source of the cryptosporidiosis outbreak and the Kowhai Hills feed main renewal'))):
        t.cell(i, 0).text = k
        t.cell(i, 1).text = v
        t.cell(i, 0).paragraphs[0].runs[0].font.bold = True
        t.cell(i, 0).width = Mm(22)
        t.cell(i, 1).width = Mm(148)
        for cell in (t.cell(i, 0), t.cell(i, 1)):
            cell.paragraphs[0].runs[0].font.size = Pt(9)
    h = doc.add_heading('Take boundary main %s out of service before the renewal starts on 26 October' % c['asset_id'], level=1)
    h.runs[0].font.size = Pt(14)
    doc.add_paragraph(
        'Take %s out of service before the Kowhai Hills feed main renewal starts. Its water reached the confirmed cases at '
        '%.1f per 100,000 resident-days in the 1 to 12 days before onset, against %.1f for the runner-up, %s. The supply '
        'zone register gives %s as the source of %s, but from %s to %s, after heavy rain, those zones drew Ferndale Road\'s '
        'water through the boundary main. The renewal plan opens it again to supply %s, where %s residents would drink water '
        'through it during the works.'
        % (c['asset'], c['rate'], c['runner_up_rate'], c['runner_up'], c['runner_up'], ' and '.join(feed_zones(S, fed)),
           fed[0].strftime('%-d'), fed[-1].strftime('%-d %B'), ' and '.join(c['forward_zones']),
           format(c['forward_residents'], ',')))
    doc.add_picture(png, width=Mm(168))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.LEFT
    src = doc.add_paragraph('Confirmed cases among district residents by date of onset, 1 September to 18 October 2027 '
                            '(terms of reference, section 3).')
    src.runs[0].font.size = Pt(8)
    src.runs[0].font.italic = True
    doc.add_paragraph(
        'Each zone\'s supply on each day is taken from the valve operations log read against the network model, not from '
        'the supply zone register, which records the normal arrangement. Rates follow section 4 of the terms of reference; '
        'assets whose water reached fewer than five cases are not ranked.')
    cp = doc.core_properties
    cp.author = 'Public Health Service'
    cp.last_modified_by = 'Public Health Service'
    cp.created = dt.datetime(2027, 10, 19, 3, 25)
    cp.modified = dt.datetime(2027, 10, 19, 3, 25)
    cp.title = 'Outbreak Control Team brief'
    cp.revision = 1
    dp = os.path.join(GOLD, 'incident_brief.docx')
    doc.save(dp)
    text = ' '.join(p.text for p in doc.paragraphs) + ' ' + ' '.join(cl.text for row in t.rows for cl in row.cells)
    pack.norm_zip(dp, app_fields={'Words': len(text.split()), 'Characters': len(text.replace(' ', '')),
                                  'CharactersWithSpaces': len(text), 'Paragraphs': len(doc.paragraphs),
                                  'Lines': sum(-(-len(p.text) // 95) for p in doc.paragraphs) + 4})
    os.remove(png)
    for f in os.listdir(GOLD):
        os.utime(os.path.join(GOLD, f), (MTIME, MTIME))


def feed_zones(S, fed):
    P = S['W']['P']
    zs = set()
    for x in fed:
        zs.update(pack.ZNAME[z] for z, pth in P[(x - world.D0).days].items() if pth and 'BM3' in pth)
    return sorted(zs)


def metadata():
    src = {'lines': 'Public Health Service line list export', 'rating': 'District council rating database export',
           'census': 'Council GIS meshblock concordance with 2023 Census usually resident counts',
           'register': 'Council supply zone register, issue 7', 'network': 'Council GIS network model export',
           'valveops': 'Council valve management system export', 'wos': 'Council maintenance management system export',
           'renewal': 'Council capital works plan, revision B', 'tor': 'Outbreak Control Team terms of reference v1.1',
           'measures': 'Council water services performance measures 2027/28', 'lab': 'Community laboratory results export',
           'ref': 'Reference laboratory typing report', 'crm': 'Council customer request system export',
           'web': 'Council website form submissions export', 'sr': 'Council service request export',
           'jobs': 'Field crew mobile job export', 'ah': 'After-hours service call log', 'rain': 'Council rain gauge network',
           'samples': 'Drinking water compliance sampling results', 'plant': 'Water treatment plant daily log'}
    files = {'target/' + name: dict(source=src[k], date='2027-10-19', licence='synthetic data, CC BY 4.0',
                                    made='simulated district records written by generator/build.py')
             for k, name in FILES.items()}
    meta = dict(task='task214', domain='epidemiology-public-health', objective='anomaly-detection',
                decision='which drinking-water asset the council takes out of service before the 26 October 2027 feed main renewal',
                deliverables=['outbreak_source.xlsx', 'incident_brief.docx'],
                distractor_files=['target/' + FILES[k] for k in DISTRACTORS], files=files)
    json.dump(meta, open(os.path.join(TASK, 'metadata.json'), 'w'), indent=1, sort_keys=True)


if __name__ == '__main__':
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else SEED
    S = make(seed)
    M, L, C, O = figures(S)
    fig = figures_json(S, M, L, C, O)
    deliver(S, fig)
    metadata()
    zip_target()
    print('call', fig['call']['asset'], fig['call']['rate'], 'runner-up', fig['call']['runner_up'], fig['call']['runner_up_rate'])
