"""The golden figures, from the rows the pack ships, and the three deliverables.

The figures run on the export rows exactly as written to target/ (status, unit, consumption, bill date), through
routes.py, the generator's code path; verify.py recomputes them from the files on its own path.
"""
import collections
import datetime as dt
import json
import math
import os
import numpy as np
import world as W
import routes as Rt
import records as R

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
GOLD = os.path.join(TASK, 'golden')
OPTIONS = {'A': 'Option A, conservation blocks', 'B': 'Option B, drought volume charge', 'C': 'Option C, drought surcharge'}
MONTH = {6: 'June', 7: 'July', 8: 'August', 9: 'September'}
# the estimate range every graded saving must hold over, with the three ways an elasticity is applied and the Fenwick
# Mesa charge in or out of the base bill
GRID = (-0.26, -0.265, -0.27, -0.275, -0.28, -0.285, -0.29, -0.295, -0.30, -0.305, -0.31, -0.315, -0.32, -0.325)
FORMS = ('log', 'lin', 'arc')


def sfr_rows(export):
    """(account, area, meter, bill year, bill month, kgal) for every single-family bill that stands."""
    out = []
    for r in export:
        if r['customer_class'] != 'RES-SF' or r['bill_status'] == 'CANCELLED':
            continue
        kg = r['consumption'] * W.CCF_KGAL if r['uom'] == 'CCF' else r['consumption']
        area = 'FMSA' if r['service_area'] == 'FENWICK MESA' else 'CITY'
        meter = float(r['meter_size_in'])
        out.append((r['account_no'], area, meter, r['bill_date'].year, r['bill_date'].month, kg))
    return out


def nearest(x, unit):
    return int(unit * math.floor(x / unit + 0.5))


def measured_family(pan):
    """Every estimate of the whole-bill elasticity the record licenses, by name."""
    fam = {}
    for kw in Rt.VARIANTS:
        lab = 'Fenwick Mesa comparison ' + (', '.join('%s=%s' % (k, v) for k, v in sorted(kw.items())) or 'July to September 2023 and 2025')
        fam[lab] = Rt.eta_fm(pan, **kw)[0]
    fam['Fenwick Mesa comparison, a year each side, own use'] = Rt.eta_fm_annual(pan)[0]
    fam['Fenwick Mesa comparison, a year each side, as billed'] = Rt.eta_fm_simple(pan)
    fam['panel, every bill, whole-bill price alone'] = Rt.panel_fe(pan, ('AP',))[0]
    fam['panel, every bill, both prices'] = Rt.panel_fe(pan, ('AP', 'MP'))[0]
    fam['panel, rest of city (2023 restructuring), whole-bill price alone'] = Rt.panel_fe(pan, ('AP',), area='CITY')[0]
    fam['panel, rest of city (2023 restructuring), both prices'] = Rt.panel_fe(pan, ('AP', 'MP'), area='CITY')[0]
    ev2 = set(k for k in W.BILL_MONTHS if k >= (2023, 7))
    fam['panel, bills from July 2023 (the Fenwick Mesa charge), whole-bill price alone'] = Rt.panel_fe(pan, ('AP',), months=ev2)[0]
    return fam


def main_call(export):
    pan = Rt.panel(sfr_rows(export))
    pop = Rt.population(pan)
    base = Rt.baseline(pan, pop)
    base_m = {m: sum(base[a][m] for a in pop) for m in Rt.SUMMER}
    # the price specification tested on every bill: both prices in one fit, then the whole-bill price alone
    two = Rt.panel_fe(pan, ('AP', 'MP'))
    two_city = Rt.panel_fe(pan, ('AP', 'MP'), area='CITY')
    eta = Rt.panel_fe(pan, ('AP',))[0]
    mp_panel = Rt.panel_fe(pan, ('MP',), area='CITY')[0]
    mp_fd = Rt.eta_redesign_mp(pan, price='MP')[0]
    vap_fd = Rt.eta_redesign_mp(pan, price='VAP')[0]
    fm, did_q, did_p, n_fm, n_city = Rt.eta_fm(pan)
    fam = measured_family(pan)
    sav = {o: Rt.forecast(pan, base, 'AP', eta, o) for o in 'ABC'}
    tot = {o: Rt.af(sum(sav[o].values())) for o in 'ABC'}
    rank = sorted('ABC', key=lambda o: -tot[o])
    # every estimate on the grid and every measured one, in every form, with the charge in and out of the base bill
    ratios = {(o, cap): Rt.ap_ratios(pan, base, o, cap) for o in 'ABC' for cap in (True, False)}
    grid = {}
    for e in sorted(set(GRID) | set(round(v, 6) for v in fam.values())):
        for form in FORMS:
            for cap in (True, False):
                grid[(e, form, cap)] = {o: Rt.af(Rt.respond(*ratios[(o, cap)], e, form).sum()) for o in 'ABC'}
    rungs = {}
    for label, model, e in (('rung0_block_price_literature', 'MP', Rt.LIT_ETA),
                            ('rung1_block_price_panel', 'MP', mp_panel),
                            ('rung1_block_price_differences', 'MP', mp_fd),
                            ('rung2_per_gallon_price', 'VAP', vap_fd),
                            ('decisive_whole_bill_price', 'AP', eta)):
        t = {o: Rt.af(sum(Rt.forecast(pan, base, model, e, o).values())) for o in 'ABC'}
        rungs[label] = dict(eta=e, savings=t, winner=max(t, key=t.get))
    means = did_table(pan)
    return dict(pan=pan, pop=pop, base=base, base_m=base_m, eta=eta, two=two, two_city=two_city, mp_panel=mp_panel,
                mp_fd=mp_fd, vap_fd=vap_fd, fm=fm, did_q=did_q, did_p=did_p, n_fm=n_fm, n_city=n_city, fam=fam,
                sav=sav, tot=tot, rank=rank, grid=grid, rungs=rungs, means=means)


def did_table(pan):
    """Mean log July to September use and mean log whole-bill price per thousand gallons, by area, in 2023 and 2025,
    on the accounts the Fenwick Mesa comparison uses."""
    acc = {'FMSA': collections.defaultdict(list), 'CITY': collections.defaultdict(list)}
    for a, d in pan.items():
        k0 = [(2023, m) for m in (7, 8, 9)]
        k1 = [(2025, m) for m in (7, 8, 9)]
        if not all(k in d and d[k] > 0.3 for k in k0 + k1):
            continue
        area, meter = d['area'], d['meter']
        g = acc[area]
        g['lq0'].append(np.mean([np.log(d[k]) for k in k0]))
        g['lq1'].append(np.mean([np.log(d[k]) for k in k1]))
        g['lp0'].append(np.mean([np.log(Rt.bill_at(d[k], meter, Rt._bd(*k), area) / d[k]) for k in k0]))
        g['lp1'].append(np.mean([np.log(Rt.bill_at(d[k0[i]], meter, Rt._bd(*k1[i]), area) / d[k0[i]]) for i in range(3)]))
    out = {}
    for area, g in acc.items():
        out[area] = dict(n=len(g['lq0']), lq0=float(np.mean(g['lq0'])), lq1=float(np.mean(g['lq1'])),
                         lp0=float(np.mean(g['lp0'])), lp1=float(np.mean(g['lp1'])))
    return out


def ask_figures(fill_rows, read_rows, wo_rows, fac_rows):
    """The 2026 base for the City's own Stage 2 measures, June to September by calendar month: the water drawn at
    the bulk fill station and the tanks filled there, and the water City facilities used on that month's reads."""
    # fill station: a resumed session repeats the session's opening register, so one tank per opening register a bay
    sess = {}
    for r in fill_rows:
        k = (r['bay'], r['m0'])
        if k not in sess or r['m1'] > sess[k]['m1']:
            sess[k] = dict(date=r['start'].date(), m1=r['m1'], m0=r['m0']) if k not in sess else dict(sess[k], m1=r['m1'])
    fill = {m: dict(kgal=0.0, fills=0) for m in Rt.SUMMER}
    for (bay, m0), s in sess.items():
        if s['date'].year == 2026 and s['date'].month in fill:
            fill[s['date'].month]['kgal'] += (s['m1'] - s['m0']) / 1000.0
            fill[s['date'].month]['fills'] += 1
    # facilities: the later read of a visit, exchanges through the work orders, the pool fill meter left out
    unit_of = {f['meter_id']: f['register_unit'] for f in fac_rows}
    swaps = {(w['location_id'], w['new_meter_id']): w for w in wo_rows if w['location_type'] == 'CITY FACILITY'}
    for w in swaps.values():
        unit_of.setdefault(w['old_meter_id'], w['old_register_unit'])
        unit_of.setdefault(w['new_meter_id'], w['new_register_unit'])
    by = collections.defaultdict(dict)
    for r in sorted(read_rows, key=lambda x: (x['read_date'], x['read_time'])):
        by[r['facility_id']][r['read_date']] = r
    per_fac = collections.defaultdict(dict)
    for fid, reads in by.items():
        seq = [reads[d] for d in sorted(reads)]
        for a, b in zip(seq, seq[1:]):
            if a['meter_id'] == b['meter_id']:
                u = unit_of[b['meter_id']]
                gal = (b['register'] - a['register']) * (W.CCF_KGAL * 1000.0 if u == 'CCF' else 1.0)
            else:
                w = swaps[(fid, b['meter_id'])]
                gal = (w['old_final_read'] - a['register']) + (b['register'] - w['new_initial_read']) * (
                    W.CCF_KGAL * 1000.0 if w['new_register_unit'] == 'CCF' else 1.0)
            per_fac[fid][(b['read_date'].year, b['read_date'].month)] = gal
    fac = {m: 0.0 for m in Rt.SUMMER}
    for fid, d in per_fac.items():
        if fid == R.SUBMETER:
            continue
        for m in Rt.SUMMER:
            fac[m] += d.get((2026, m), 0.0)
    return dict(fill=fill, fac_gal=fac, fac_af={m: fac[m] / (W.AF_KGAL * 1000.0) for m in fac}, per_fac=per_fac)


def bins_table(mc):
    """Each option's and the gap's range over the grid, every form, the charge in or out, and every measured estimate."""
    out = {}
    for key in ('A', 'B', 'C', 'gap'):
        if key == 'gap':
            v = [g['C'] - g['B'] for g in mc['grid'].values()]
        else:
            v = [g[key] for g in mc['grid'].values()]
        out[key] = dict(min=round(min(v), 2), max=round(max(v), 2))
    return out


def figures(mc, ask):
    t = mc['tot']
    win, run = mc['rank'][0], mc['rank'][1]
    fam = mc['fam']
    rng = bins_table(mc)
    f = {
        'call': OPTIONS[win], 'runner_up': OPTIONS[run],
        'baseline_af': round(Rt.af(sum(mc['base_m'].values())), 1),
        'baseline_af_nearest_10': nearest(Rt.af(sum(mc['base_m'].values())), 10),
        'accounts': len(mc['pop']),
        'saving_af': {o: round(t[o], 1) for o in 'ABC'},
        'saving_af_2dp': {o: round(t[o], 2) for o in 'ABC'},
        'saving_af_nearest_10': {o: nearest(t[o], 10) for o in 'ABC'},
        'gap_af': round(t[win] - t[run], 1),
        'gap_af_2dp': round(t[win] - t[run], 2),
        'gap_af_nearest_10': nearest(t[win] - t[run], 10),
        'saving_af_by_month': {o: {MONTH[m]: round(Rt.af(mc['sav'][o][m]), 2) for m in Rt.SUMMER} for o in 'ABC'},
        'elasticity': round(mc['eta'], 2),
        'elasticity_4dp': round(mc['eta'], 4),
        'two_price_every_bill': {'whole_bill_4dp': round(mc['two'][0], 4), 'whole_bill_2dp': round(mc['two'][0], 2),
                                 'block_4dp': round(mc['two'][1], 4), 'block_3dp': round(mc['two'][1], 3)},
        'two_price_rest_of_city': {'whole_bill_4dp': round(mc['two_city'][0], 4), 'whole_bill_2dp': round(mc['two_city'][0], 2),
                                   'block_4dp': round(mc['two_city'][1], 4), 'block_3dp': round(mc['two_city'][1], 3)},
        'block_price_alone_panel_4dp': round(mc['mp_panel'], 4),
        'block_price_alone_panel_2dp': round(mc['mp_panel'], 2),
        'block_price_differences_4dp': round(mc['mp_fd'], 4),
        'block_price_differences_2dp': round(mc['mp_fd'], 2),
        'per_gallon_price_differences_2dp': round(mc['vap_fd'], 2),
        'fenwick_comparison_4dp': round(mc['fm'], 4),
        'fenwick_comparison_2dp': round(mc['fm'], 2),
        'fenwick_mesa_use_change_pct': round(100 * (math.exp(mc['did_q']) - 1), 1),
        'fenwick_mesa_use_fall_pct': round(-100 * (math.exp(mc['did_q']) - 1), 1),
        'fenwick_mesa_price_change_pct': round(100 * (math.exp(mc['did_p']) - 1), 1),
        'elasticity_accounts': {'fenwick_mesa': mc['n_fm'], 'rest_of_city': mc['n_city']},
        'measured_estimates_4dp': {k: round(v, 4) for k, v in sorted(fam.items())},
        'measured_range_2dp': [round(max(fam.values()), 2), round(min(fam.values()), 2)],
        'estimate_grid': [GRID[0], GRID[-1]],
        'ranges_over_grid_forms_and_charge': rng,
        'fm_charge_usd': W.FM_CHARGE,
        'ccf_gallons': 748.052,
        'cited_plan_section': 5.3,
        'options': {'A_first_block': W.OPT_A_TIER1, 'A_third_block': W.OPT_A_TIER3, 'B_adder': W.OPT_B_ADDER,
                    'C_surcharge': W.OPT_C_SURCHARGE},
        'rungs': {k: dict(elasticity=round(v['eta'], 2), winner=v['winner'],
                          savings={o: round(x, 1) for o, x in v['savings'].items()}) for k, v in mc['rungs'].items()},
        'ask': {
            'fill_kgal': {MONTH[m]: nearest(ask['fill'][m]['kgal'], 1) for m in Rt.SUMMER},
            'fills': {MONTH[m]: ask['fill'][m]['fills'] for m in Rt.SUMMER},
            'facilities_af': {MONTH[m]: round(ask['fac_af'][m] + 1e-9, 1) for m in Rt.SUMMER},
        },
        'ask_unrounded': {
            'fill_kgal': {MONTH[m]: round(ask['fill'][m]['kgal'], 3) for m in Rt.SUMMER},
            'facilities_af': {MONTH[m]: round(ask['fac_af'][m], 4) for m in Rt.SUMMER},
        },
    }
    return f


# ---------------------------------------------------------------- the deliverables
def workbook(path, mc, ask, f, normalise):
    import openpyxl
    from openpyxl.styles import Font, Alignment, PatternFill
    from openpyxl.utils import get_column_letter
    wb = openpyxl.Workbook()
    wb.properties.creator = 'Tami Weaver'
    wb.properties.lastModifiedBy = 'Tami Weaver'
    created = dt.datetime(2026, 11, 3, 16, 47, 12)
    wb.properties.created = created
    wb.properties.modified = created
    bold = Font(bold=True)
    head_fill = PatternFill('solid', fgColor='DCE6F1')

    def header(ws, row, cols):
        for j, h in enumerate(cols, start=1):
            c = ws.cell(row=row, column=j, value=h)
            c.font = bold
            c.fill = head_fill
            c.alignment = Alignment(wrap_text=True, vertical='top')

    ws = wb.active
    ws.title = 'Options'
    ws['A1'] = 'Option C, the drought surcharge, takes the most water off single-family bills in June to September 2027'
    ws['A1'].font = Font(bold=True, size=12)
    ws['A2'] = ('Saving against the Plan Section 5.3 baseline, acre-feet, at the whole-bill elasticity of %.4f (Price '
                'response sheet). For the December 8, 2026 hearing.' % f['elasticity_4dp'])
    header(ws, 4, ['Option', 'June bills', 'July bills', 'August bills', 'September bills', 'June to September',
                   'Nearest 10 acre-feet', 'Reading'])
    r = 5
    win, run = mc['rank'][0], mc['rank'][1]
    for o in sorted('ABC'):
        ws.cell(row=r, column=1, value=OPTIONS[o])
        for j, m in enumerate(Rt.SUMMER, start=2):
            ws.cell(row=r, column=j, value=f['saving_af_by_month'][o][MONTH[m]]).number_format = '0.00'
        ws.cell(row=r, column=6, value=f['saving_af_2dp'][o]).number_format = '0.00'
        ws.cell(row=r, column=7, value=f['saving_af_nearest_10'][o])
        reading = {win: 'Recommended', run: 'Runner-up'}.get(o, 'No measurable saving once customers answer the whole bill')
        ws.cell(row=r, column=8, value=reading)
        r += 1
    r += 1
    ws.cell(row=r, column=1, value='Gap, recommended less runner-up').font = bold
    ws.cell(row=r, column=6, value=f['gap_af_2dp']).number_format = '0.00'
    ws.cell(row=r, column=7, value=f['gap_af_nearest_10'])
    r += 2
    ws.cell(row=r, column=1, value='Baseline, June to September (acre-feet)').font = bold
    for j, m in enumerate(Rt.SUMMER, start=2):
        ws.cell(row=r, column=j, value=round(Rt.af(mc['base_m'][m]), 2)).number_format = '0.0'
    ws.cell(row=r, column=7, value=f['baseline_af_nearest_10'])
    r += 1
    ws.cell(row=r, column=1, value='Accounts in the baseline')
    ws.cell(row=r, column=7, value=len(mc['pop']))
    r += 2
    ws.cell(row=r, column=1, value='Source: CIS bill export of November 2, 2026; Resolutions 2021-44, 2023-12 and 2024-17; '
                                   'agenda report options of October 27, 2026.').font = Font(italic=True, size=9)
    for row in ws.iter_rows(min_row=5, max_row=r - 1, min_col=2, max_col=7):
        for c in row:
            c.alignment = Alignment(horizontal='right')
    ws.column_dimensions['A'].width = 38
    for j in range(2, 8):
        ws.column_dimensions[get_column_letter(j)].width = 13
    ws.column_dimensions['H'].width = 50
    ws.freeze_panes = 'B5'

    ws2 = wb.create_sheet('Price response')
    ws2['A1'] = 'Which price customers answer: the whole bill per thousand gallons, not the block price'
    ws2['A1'].font = Font(bold=True, size=12)
    ws2['A2'] = ('Log use on log price, every single-family bill June 2022 to October 2026, with account-by-calendar-month '
                 'and bill-month effects; each price read at the account\'s mean use for that calendar month.')
    header(ws2, 4, ['Fit', 'Whole bill per thousand gallons', 'Block price of the last thousand gallons'])
    fits = [('Every bill, both prices', f['two_price_every_bill']['whole_bill_4dp'], f['two_price_every_bill']['block_4dp']),
            ('Rest of city only (the 2023 restructuring), both prices', f['two_price_rest_of_city']['whole_bill_4dp'],
             f['two_price_rest_of_city']['block_4dp']),
            ('Every bill, whole-bill price alone (used for the savings)', f['elasticity_4dp'], None),
            ('Rest of city only, block price alone', None, f['block_price_alone_panel_4dp'])]
    rr = 5
    for lab, a, b in fits:
        ws2.cell(row=rr, column=1, value=lab)
        if a is not None:
            ws2.cell(row=rr, column=2, value=a).number_format = '0.0000'
        if b is not None:
            ws2.cell(row=rr, column=3, value=b).number_format = '0.0000'
        rr += 1
    rr += 1
    ws2.cell(row=rr, column=1, value='Cross-check: Fenwick Mesa against the rest of the city, July to September 2023 and 2025').font = bold
    rr += 1
    header(ws2, rr, ['Area', 'Accounts', 'Mean log use 2023', 'Mean log use 2025', 'Change', 'Mean log price 2023',
                     'Mean log price 2025', 'Change'])
    rr += 1
    for area, label in (('FMSA', 'Fenwick Mesa'), ('CITY', 'Rest of city')):
        g = mc['means'][area]
        vals = [label, g['n'], g['lq0'], g['lq1'], g['lq1'] - g['lq0'], g['lp0'], g['lp1'], g['lp1'] - g['lp0']]
        for j, v in enumerate(vals, start=1):
            c = ws2.cell(row=rr, column=j, value=round(v, 5) if isinstance(v, float) else v)
            if isinstance(v, float):
                c.number_format = '0.0000'
        rr += 1
    ws2.cell(row=rr, column=1, value='Difference, Fenwick Mesa less rest of city')
    ws2.cell(row=rr, column=5, value=round(mc['did_q'], 5)).number_format = '0.0000'
    ws2.cell(row=rr, column=8, value=round(mc['did_p'], 5)).number_format = '0.0000'
    rr += 1
    ws2.cell(row=rr, column=1, value='Elasticity from the comparison')
    ws2.cell(row=rr, column=5, value=f['fenwick_comparison_4dp']).number_format = '0.0000'
    rr += 2
    ws2.cell(row=rr, column=1, value='The savings keep their 10 acre-foot bins for any elasticity from %.2f to %.3f, applied '
                                     'in constant-elasticity, linear or midpoint form, with the Fenwick Mesa charge in or '
                                     'out of the base bill.' % (f['estimate_grid'][0], f['estimate_grid'][1]))
    ws2.column_dimensions['A'].width = 58
    for j in range(2, 9):
        ws2.column_dimensions[get_column_letter(j)].width = 16

    ws3 = wb.create_sheet('City measures 2026')
    ws3['A1'] = 'City Stage 2 measures, 2026 base, June to September'
    ws3['A1'].font = Font(bold=True, size=12)
    header(ws3, 3, ['Month', 'Fill station water drawn (thousand gallons)', 'Fill station tanks filled',
                    'City facilities, use on the month\'s reads (acre-feet)'])
    rr = 4
    for m in Rt.SUMMER:
        ws3.cell(row=rr, column=1, value=MONTH[m] + ' 2026')
        ws3.cell(row=rr, column=2, value=f['ask']['fill_kgal'][MONTH[m]])
        ws3.cell(row=rr, column=3, value=f['ask']['fills'][MONTH[m]])
        ws3.cell(row=rr, column=4, value=f['ask']['facilities_af'][MONTH[m]]).number_format = '0.0'
        rr += 1
    rr += 1
    ws3.cell(row=rr, column=1, value='By facility, gallons on the month\'s reads').font = bold
    rr += 1
    header(ws3, rr, ['Facility'] + [MONTH[m] for m in Rt.SUMMER] + ['Counted'])
    rr += 1
    for fid in sorted(ask['per_fac']):
        ws3.cell(row=rr, column=1, value=fid)
        for j, m in enumerate(Rt.SUMMER, start=2):
            ws3.cell(row=rr, column=j, value=int(round(ask['per_fac'][fid].get((2026, m), 0.0))))
        ws3.cell(row=rr, column=6, value='No, its water is on WB-PAV' if fid == R.SUBMETER else 'Yes')
        rr += 1
    rr += 1
    ws3.cell(row=rr, column=1, value='Source: fill station transaction export to October 31, 2026; facility meter read log '
                                     'and meter list; meter shop work orders.').font = Font(italic=True, size=9)
    ws3.column_dimensions['A'].width = 22
    for j in range(2, 7):
        ws3.column_dimensions[get_column_letter(j)].width = 22
    ws3.freeze_panes = 'B4'

    ws4 = wb.create_sheet('Notes')
    notes = [
        ('As of', 'Bills to the October 2026 run (export of November 2, 2026); fill station and facility records to October 31, 2026.'),
        ('Accounts', 'Single-family residential accounts (RES-SF, both service areas) billed in each of the eight June to '
                     'September bill months of 2025 and 2026, Plan Section 5.3.'),
        ('Baseline', 'For each account and bill month, the average of its 2025 and 2026 billed use; a rebill stands in '
                     'place of the bill it cancels.'),
        ('Units', 'Hundred cubic feet at 748.052 gallons (Resolution 2023-12, Section 2); an acre-foot is 325,851 gallons.'),
        ('2027 rates', 'Resolution 2023-12 single-family rates and the Fenwick Mesa capital recovery charge, plus the option, '
                       'on bills issued May 1 to October 31, 2027.'),
        ('Price response', 'Both prices fitted together on every bill; the block price carries no response, so the savings '
                           'use the whole-bill price alone (%.4f), applied to each account\'s baseline bill.' % f['elasticity_4dp']),
        ('Fill station', 'Each tank filled counts once, a truck\'s tank and its trailer\'s each; a session resumed at bay 2 '
                         'after the coupling faulted is one tank, from its opening register; months by local start.'),
        ('City facilities', 'Register advance to the read dated in the month; the later read of a visit stands; the Westbrook '
                            'pool fill meter is on the pavilion service and is not added again.'),
        ('Rounding', 'Savings and the gap to the nearest 10 acre-feet; fill station water to the thousand gallons; facility '
                     'use to one decimal of an acre-foot.'),
    ]
    ws4.column_dimensions['A'].width = 18
    ws4.column_dimensions['B'].width = 110
    for i, (k, v) in enumerate(notes, start=1):
        ws4.cell(row=i, column=1, value=k).font = bold
        ws4.cell(row=i, column=2, value=v).alignment = Alignment(wrap_text=True, vertical='top')
    wb.save(path)
    normalise(path, 'Microsoft Excel')


def memo(path, mc, ask, f, normalise):
    from docx import Document
    from docx.shared import Pt, Inches
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    d = Document()
    st = d.styles['Normal']
    st.font.name = 'Calibri'
    st.font.size = Pt(11)
    for sec in d.sections:
        sec.left_margin = sec.right_margin = Inches(1.0)
        fp = sec.footer.paragraphs[0]
        fp.text = 'Water Department, Stage 2 rate recommendation, December 8, 2026 hearing. Page '
        frun = fp.add_run()
        fld = OxmlElement('w:fldSimple')
        fld.set(qn('w:instr'), 'PAGE')
        frun._r.append(fld)
        for rn in fp.runs:
            rn.font.size = Pt(8.5)
    win, run = mc['rank'][0], mc['rank'][1]
    last = mc['rank'][2]
    s2 = f['saving_af_2dp']
    n10 = f['saving_af_nearest_10']
    for k, v in (('To', 'City Council, through Jason Morgan, Utilities Director'),
                 ('From', 'Tami Weaver, Rates and Finance Manager'), ('Date', 'November 3, 2026'),
                 ('Subject', 'Stage 2 drought rate measure for single-family bills, May to October 2027')):
        p = d.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.add_run(k + ': ').bold = True
        p.add_run(v)
    d.add_paragraph('')
    d.add_heading('Adopt the drought surcharge: it takes the most water off single-family bills', level=1)
    d.add_heading('Recommendation', level=2)
    prose = {o: OPTIONS[o].replace(', ', ', the ') for o in OPTIONS}
    d.add_paragraph('Adopt %s, for single-family bills issued May 1 to October 31, 2027. It takes about %d acre-feet off '
                    'the June to September bills (%.2f), against about %d for %s (%.2f), a gap of about %d acre-feet '
                    '(%.2f). %s, takes no measurable water off (%.2f acre-feet, 0 to the nearest 10): once customers '
                    'answer the whole bill, its cheaper first block offsets most of what the dearer third block '
                    'saves.' % (prose[win], n10[win], s2[win], n10[run], prose[run], s2[run], f['gap_af_nearest_10'],
                                f['gap_af_2dp'], prose[last][0].upper() + prose[last][1:], s2[last]))
    tb = d.add_table(rows=5, cols=3)
    tb.style = 'Table Grid'
    rows = [('June to September 2027', 'Acre-feet', 'Nearest 10')]
    for o in 'CBA':
        rows.append((OPTIONS[o] + ', saving', '%.2f' % s2[o], '%d' % n10[o]))
    rows.append(('Baseline, %s accounts (Plan Section 5.3)' % '{:,}'.format(len(mc['pop'])), '%.1f' % f['baseline_af'],
                 '%d' % f['baseline_af_nearest_10']))
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            tb.cell(i, j).text = v
            if i == 0:
                tb.cell(i, j).paragraphs[0].runs[0].bold = True
    note = d.add_paragraph('Saving against each account\'s Plan Section 5.3 baseline, at the 2026 rates plus the option; '
                           'the split by bill month is in stage2_drought_rates_2027.xlsx. Source: CIS bill export of '
                           'November 2, 2026.')
    note.runs[0].font.size = Pt(8.5)
    note.runs[0].italic = True
    d.add_heading('Why the surcharge saves the most', level=2)
    d.add_paragraph('Every single-family bill since June 2022 was fitted with both prices a customer sees: the block price '
                    'of the last thousand gallons and what the whole bill comes to per thousand gallons. The whole-bill '
                    'price carries the response (elasticity %.4f) and the block price none (%+.4f); the 2023 '
                    'restructuring alone, in the rest of the city, gives the same reading (%.4f and %+.4f). Fenwick Mesa '
                    'confirms it: from the July 2024 bills its capital recovery charge added USD %.2f to every bill and '
                    'changed no block price, and against the rest of the city its July to September use fell %.1f per '
                    'cent between 2023 and 2025 while its bills per thousand gallons rose %.1f per cent.' % (
                        f['two_price_every_bill']['whole_bill_4dp'], f['two_price_every_bill']['block_4dp'],
                        f['two_price_rest_of_city']['whole_bill_4dp'], f['two_price_rest_of_city']['block_4dp'],
                        W.FM_CHARGE, f['fenwick_mesa_use_fall_pct'], f['fenwick_mesa_price_change_pct']))
    d.add_paragraph('Priced on the whole bill at each account\'s baseline use, with the whole-bill price alone (%.4f), the '
                    'surcharge raises every bill and moves the most water. Option B adds less than the surcharge to most '
                    'bills. Read on the block price instead, Option A would look best, which is why the price test '
                    'matters. The ranking and every rounded figure hold for any elasticity from %.2f to %.3f, however '
                    'the elasticity is applied.' % (f['elasticity_4dp'], f['estimate_grid'][0], f['estimate_grid'][1]))
    d.add_heading('City measures, 2026 base', level=2)
    d.add_paragraph('For the 2027 targets for the City\'s own measures, the June to September 2026 figures are:')
    tb2 = d.add_table(rows=5, cols=4)
    tb2.style = 'Table Grid'
    hdr = ('Month', 'Fill station, thousand gallons', 'Tanks filled', 'City facilities, acre-feet')
    for j, v in enumerate(hdr):
        tb2.cell(0, j).text = v
        tb2.cell(0, j).paragraphs[0].runs[0].bold = True
    for i, m in enumerate(Rt.SUMMER, start=1):
        tb2.cell(i, 0).text = MONTH[m]
        tb2.cell(i, 1).text = '{:,}'.format(f['ask']['fill_kgal'][MONTH[m]])
        tb2.cell(i, 2).text = '%d' % f['ask']['fills'][MONTH[m]]
        tb2.cell(i, 3).text = '%.1f' % f['ask']['facilities_af'][MONTH[m]]
    n2 = d.add_paragraph('A truck\'s tank and its trailer\'s count as two tanks; a fill resumed at bay 2 after the coupling '
                         'faulted is one tank, from its opening register. The pool fill meter at Westbrook is read for '
                         'pool operations; its water is already on the pavilion meter and is not added again. Source: '
                         'fill station transaction export; facility meter read log; meter shop work orders.')
    n2.runs[0].font.size = Pt(8.5)
    n2.runs[0].italic = True
    d.add_paragraph('Staff will report the drought reserve revenue of the recommended option with the hearing packet, '
                    'as the agenda report says.')
    cp = d.core_properties
    cp.author = 'Tami Weaver'
    cp.last_modified_by = 'Tami Weaver'
    cp.created = dt.datetime(2026, 11, 3, 9, 42, 16)
    cp.modified = dt.datetime(2026, 11, 3, 17, 26, 41)
    cp.revision = 3
    cp.title = 'Stage 2 drought rate recommendation'
    cp.comments = ''
    d.save(path)
    normalise(path, 'Microsoft Office Word', keep_modified=True, total_time=118)


def chart(path, mc, f):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    ink, ink2, grid, surface = '#0b0b0b', '#52514e', '#e1e0d9', '#fcfcfb'
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.edgecolor': ink2,
                         'axes.labelcolor': ink2, 'xtick.color': ink2, 'ytick.color': ink2})
    fig, ax = plt.subplots(figsize=(7.4, 4.8), dpi=150)
    fig.patch.set_facecolor(surface)
    ax.set_facecolor(surface)
    ramp = {6: '#86b6ef', 7: '#5598e7', 8: '#2a78d6', 9: '#184f95'}     # bill months, light to dark
    x = np.arange(3)
    bottom = np.zeros(3)          # saving months stack up from zero
    under = np.zeros(3)           # months whose use rises stack down from zero
    for m in Rt.SUMMER:
        v = np.array([Rt.af(mc['sav'][o][m]) for o in 'ABC'])
        up = np.where(v > 0, v, 0.0)
        dn = np.where(v < 0, v, 0.0)
        ax.bar(x, up, 0.52, bottom=bottom, color=ramp[m], label=MONTH[m] + ' bills', edgecolor=surface, linewidth=1.6,
               zorder=3)
        ax.bar(x, dn, 0.52, bottom=under, color=ramp[m], edgecolor=surface, linewidth=1.6, zorder=3)
        bottom += up
        under += dn
    ax.axhline(0, color=ink2, linewidth=0.9, zorder=4)
    win = mc['rank'][0]
    for i, o in enumerate('ABC'):
        n = f['saving_af_nearest_10'][o]
        lab = 'about %d acre-feet' % n if n else 'no measurable saving:\nJune and September use rises'
        ax.text(i, bottom[i] + 0.45, lab, ha='center', va='bottom', fontsize=10 if n else 8.8, color=ink,
                fontweight='bold' if o == win else 'normal')
    ax.set_xticks(x)
    ax.set_xticklabels(['Option A\nconservation blocks', 'Option B\ndrought volume charge',
                        'Option C\ndrought surcharge\n(recommended)'])
    for lab in ax.get_xticklabels():
        if 'recommended' in lab.get_text():
            lab.set_fontweight('bold')
            lab.set_color(ink)
    ax.set_ylabel('Acre-feet off June to September bills')
    ax.yaxis.grid(True, color=grid, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for sp in ('top', 'right', 'left'):
        ax.spines[sp].set_visible(False)
    ax.tick_params(axis='y', length=0)
    ax.set_ylim(min(under) * 1.35 - 0.5, max(bottom) * 1.25)
    fig.text(0.02, 0.965, 'The drought surcharge takes the most water off single-family bills', ha='left', va='top',
             fontsize=12, fontweight='bold', color=ink)
    fig.text(0.02, 0.918, 'Saving against the drought plan baseline, June to September 2027 bills, by bill month',
             ha='left', va='top', fontsize=9.5, color=ink2)
    ax.legend(frameon=False, fontsize=8.5, loc='upper left', labelcolor=ink2)
    fig.text(0.02, 0.012, 'Source: CIS bill export of November 2, 2026; Plan Section 5.3; agenda report options of October '
             '27, 2026.\nSavings rounded to the nearest 10 acre-feet.', fontsize=7.5, color=ink2, va='bottom')
    fig.tight_layout(rect=(0, 0.07, 1, 0.88))
    fig.savefig(path, metadata={'Software': None}, facecolor=surface)
    plt.close(fig)


def main(export, fill_rows, read_rows, wo_rows, fac_rows, normalise):
    os.makedirs(GOLD, exist_ok=True)
    mc = main_call(export)
    ask = ask_figures(fill_rows, read_rows, wo_rows, fac_rows)
    f = figures(mc, ask)
    workbook(os.path.join(GOLD, 'stage2_drought_rates_2027.xlsx'), mc, ask, f, normalise)
    memo(os.path.join(GOLD, 'stage2_rate_recommendation.docx'), mc, ask, f, normalise)
    chart(os.path.join(GOLD, 'summer_2027_savings.png'), mc, f)
    with open(os.path.join(HERE, 'figures.json'), 'w') as fh:
        json.dump(f, fh, indent=1, sort_keys=True)
    return mc, ask, f
