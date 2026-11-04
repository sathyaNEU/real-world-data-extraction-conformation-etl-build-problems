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


def main_call(export):
    pan = Rt.panel(sfr_rows(export))
    pop = Rt.population(pan)
    base = Rt.baseline(pan, pop)
    base_m = {m: sum(base[a][m] for a in pop) for m in Rt.SUMMER}
    eta, did_q, did_p, n_fm, n_city = Rt.eta_fm(pan)
    fam = [Rt.eta_fm(pan, **kw)[0] for kw in Rt.VARIANTS]
    sav = {o: Rt.forecast(pan, base, 'AP', eta, o) for o in 'ABC'}
    tot = {o: Rt.af(sum(sav[o].values())) for o in 'ABC'}
    fam_tot = {o: [Rt.af(sum(Rt.forecast(pan, base, 'AP', e, o).values())) for e in fam] for o in 'ABC'}
    rank = sorted('ABC', key=lambda o: -tot[o])
    # the rungs below, on the same rows
    eta_mp = Rt.eta_redesign_mp(pan, price='MP')[0]
    eta_vap = Rt.eta_redesign_mp(pan, price='VAP')[0]
    rungs = {}
    for label, model, e in (('rung0_mp_literature', 'MP', Rt.LIT_ETA), ('rung1_mp_own', 'MP', eta_mp),
                            ('rung2_vap_own', 'VAP', eta_vap), ('rung3_ap_fenwick', 'AP', eta)):
        t = {o: Rt.af(sum(Rt.forecast(pan, base, model, e, o).values())) for o in 'ABC'}
        rungs[label] = dict(eta=e, savings=t, winner=max(t, key=t.get))
    # the means behind the elasticity, for the workbook
    means = did_table(pan)
    return dict(pan=pan, pop=pop, base=base, base_m=base_m, eta=eta, did_q=did_q, did_p=did_p, n_fm=n_fm,
                n_city=n_city, fam=fam, sav=sav, tot=tot, fam_tot=fam_tot, rank=rank, rungs=rungs, means=means,
                eta_mp=eta_mp, eta_vap=eta_vap)


def did_table(pan):
    """Mean log July to September use and mean log whole-bill price per thousand gallons, by area, in 2023 and 2025,
    on the accounts the elasticity uses."""
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
    the bulk fill station and its fills, and the water City facilities used on that month's reads."""
    # fill station: a resumed session repeats the session's opening register, so one fill per opening register a bay
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


def figures(mc, ask):
    t = mc['tot']
    win, run = mc['rank'][0], mc['rank'][1]
    f = {
        'call': OPTIONS[win], 'runner_up': OPTIONS[run],
        'baseline_af': round(Rt.af(sum(mc['base_m'].values())), 1),
        'baseline_af_nearest_10': nearest(Rt.af(sum(mc['base_m'].values())), 10),
        'accounts': len(mc['pop']),
        'saving_af': {o: round(t[o], 1) for o in 'ABC'},
        'saving_af_nearest_10': {o: nearest(t[o], 10) for o in 'ABC'},
        'gap_af': round(t[win] - t[run], 1),
        'gap_af_nearest_10': nearest(t[win] - t[run], 10),
        'saving_af_by_month': {o: {MONTH[m]: round(Rt.af(mc['sav'][o][m]), 1) for m in Rt.SUMMER} for o in 'ABC'},
        'elasticity': round(mc['eta'], 2),
        'elasticity_4dp': round(mc['eta'], 4),
        'redesign_marginal_price_elasticity_4dp': round(mc['eta_mp'], 4),
        'elasticity_band': [round(max(mc['fam']), 2), round(min(mc['fam']), 2)],
        'fm_charge_usd': W.FM_CHARGE,
        'ccf_gallons': 748.052,
        'fenwick_mesa_use_change_pct': round(100 * (math.exp(mc['did_q']) - 1), 1),
        'fenwick_mesa_use_fall_pct': round(-100 * (math.exp(mc['did_q']) - 1), 1),
        'rungs': {k: dict(elasticity=round(v['eta'], 2), winner=v['winner'],
                          savings={o: round(x, 1) for o, x in v['savings'].items()}) for k, v in mc['rungs'].items()},
        'fenwick_mesa_price_change_pct': round(100 * (math.exp(mc['did_p']) - 1), 1),
        'elasticity_accounts': {'fenwick_mesa': mc['n_fm'], 'rest_of_city': mc['n_city']},
        'redesign_marginal_price_elasticity': round(mc['eta_mp'], 2),
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
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
    from openpyxl.utils import get_column_letter
    wb = openpyxl.Workbook()
    wb.properties.creator = 'Tami Weaver'
    wb.properties.lastModifiedBy = 'Tami Weaver'
    created = dt.datetime(2026, 11, 3, 16, 47, 12)
    wb.properties.created = created
    wb.properties.modified = created
    bold = Font(bold=True)
    head_fill = PatternFill('solid', fgColor='DCE6F1')
    thin = Side(style='thin', color='999999')

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
    ws['A2'] = ('Saving against the Plan Section 5.3 baseline, acre-feet; bill months at one decimal, the summer to the '
                'nearest 10. For the December 8, 2026 hearing.')
    header(ws, 4, ['Option', 'June bills', 'July bills', 'August bills', 'September bills',
                   'June to September, nearest 10 acre-feet'])
    r = 5
    order = sorted('ABC')
    for o in order:
        ws.cell(row=r, column=1, value=OPTIONS[o])
        for j, m in enumerate(Rt.SUMMER, start=2):
            ws.cell(row=r, column=j, value=round(Rt.af(mc['sav'][o][m]), 2)).number_format = '0.0'
        ws.cell(row=r, column=6, value=f['saving_af_nearest_10'][o])
        r += 1
    r += 1
    ws.cell(row=r, column=1, value='Baseline, June to September (acre-feet)').font = bold
    for j, m in enumerate(Rt.SUMMER, start=2):
        ws.cell(row=r, column=j, value=round(Rt.af(mc['base_m'][m]), 2)).number_format = '0.0'
    ws.cell(row=r, column=6, value=f['baseline_af_nearest_10'])
    r += 1
    ws.cell(row=r, column=1, value='Accounts in the baseline')
    ws.cell(row=r, column=6, value=len(mc['pop']))
    r += 2
    win, run = mc['rank'][0], mc['rank'][1]
    ws.cell(row=r, column=1, value='Recommended').font = bold
    ws.cell(row=r, column=2, value=OPTIONS[win])
    r += 1
    ws.cell(row=r, column=1, value='Runner-up')
    ws.cell(row=r, column=2, value=OPTIONS[run])
    r += 1
    ws.cell(row=r, column=1, value='Gap, June to September (acre-feet)')
    ws.cell(row=r, column=6, value=f['gap_af_nearest_10'])
    r += 2
    ws.cell(row=r, column=1, value='Source: CIS bill export of November 2, 2026; Resolutions 2023-12 and 2024-17; agenda '
                                   'report options of October 27, 2026.').font = Font(italic=True, size=9)
    for row in ws.iter_rows(min_row=5, max_row=r - 1, min_col=3, max_col=6):
        for c in row:
            c.alignment = Alignment(horizontal='right')
    ws.column_dimensions['A'].width = 40
    for j in range(2, 6):
        ws.column_dimensions[get_column_letter(j)].width = 13
    ws.column_dimensions['F'].width = 22
    ws.freeze_panes = 'B5'

    ws2 = wb.create_sheet('Price response')
    ws2['A1'] = 'Summer price response, read from the July 2024 Fenwick Mesa capital recovery charge'
    ws2['A1'].font = Font(bold=True, size=12)
    ws2['A2'] = ('Single-family accounts billed July to September in both 2023 and 2025. Price is the whole bill per '
                 'thousand gallons at the account\'s 2023 use.')
    header(ws2, 4, ['Area', 'Accounts', 'Mean log use 2023', 'Mean log use 2025', 'Change', 'Mean log price 2023',
                    'Mean log price 2025', 'Change'])
    rr = 5
    for area, label in (('FMSA', 'Fenwick Mesa'), ('CITY', 'Rest of city')):
        g = mc['means'][area]
        vals = [label, g['n'], g['lq0'], g['lq1'], g['lq1'] - g['lq0'], g['lp0'], g['lp1'], g['lp1'] - g['lp0']]
        for j, v in enumerate(vals, start=1):
            c = ws2.cell(row=rr, column=j, value=round(v, 5) if isinstance(v, float) else v)
            if isinstance(v, float):
                c.number_format = '0.0000'
        rr += 1
    ws2.cell(row=rr, column=1, value='Difference, Fenwick Mesa less rest of city').font = bold
    ws2.cell(row=rr, column=5, value=round(mc['did_q'], 5)).number_format = '0.0000'
    ws2.cell(row=rr, column=8, value=round(mc['did_p'], 5)).number_format = '0.0000'
    rr += 2
    ws2.cell(row=rr, column=1, value='Elasticity of use on the whole-bill price').font = bold
    ws2.cell(row=rr, column=5, value=f['elasticity']).number_format = '0.00'
    rr += 1
    ws2.cell(row=rr, column=1, value='Same comparison, other summers and prices (range)')
    ws2.cell(row=rr, column=5, value='%.2f to %.2f' % tuple(f['elasticity_band']))
    rr += 1
    ws2.cell(row=rr, column=1, value='July 2023 restructuring read on the last block price (for reference)')
    ws2.cell(row=rr, column=5, value=f['redesign_marginal_price_elasticity']).number_format = '0.00'
    ws2.column_dimensions['A'].width = 44
    for j in range(2, 9):
        ws2.column_dimensions[get_column_letter(j)].width = 15

    ws3 = wb.create_sheet('City measures 2026')
    ws3['A1'] = 'City Stage 2 measures, 2026 base, June to September'
    ws3['A1'].font = Font(bold=True, size=12)
    header(ws3, 3, ['Month', 'Fill station water drawn (thousand gallons)', 'Fill station tank fills',
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
        ('Price response', 'Fenwick Mesa against the rest of the city, July to September 2023 and 2025, on the whole bill per '
                           'thousand gallons; see the Price response sheet.'),
        ('Fill station', 'One tank fill per opening register on a bay, dated by its local start; a resumed bay 2 session is one tank fill, a trailer filled after its truck another.'),
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
    d = Document()
    st = d.styles['Normal']
    st.font.name = 'Calibri'
    st.font.size = Pt(11)
    for sec in d.sections:
        sec.left_margin = sec.right_margin = Inches(1.0)
    t = mc['tot']
    win, run = mc['rank'][0], mc['rank'][1]
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    for sec in d.sections:
        fp = sec.footer.paragraphs[0]
        fp.text = 'Water Department, Stage 2 rate recommendation, December 8, 2026 hearing. Page '
        frun = fp.add_run()
        fld = OxmlElement('w:fldSimple')
        fld.set(qn('w:instr'), 'PAGE')
        frun._r.append(fld)
        for rn in fp.runs:
            rn.font.size = Pt(8.5)
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
                    'the June to September bills, against about %d for %s, and about %d for %s, so it beats the '
                    'runner-up by about %d acre-feet.' % (
                        prose[win], f['saving_af_nearest_10'][win], f['saving_af_nearest_10'][run], prose[run],
                        f['saving_af_nearest_10'][mc['rank'][2]], prose[mc['rank'][2]], f['gap_af_nearest_10']))
    tb = d.add_table(rows=5, cols=2)
    tb.style = 'Table Grid'
    rows = [('', 'June to September 2027, acre-feet (nearest 10)')]
    for o in 'ABC':
        rows.append((OPTIONS[o] + ', saving', '%d' % f['saving_af_nearest_10'][o]))
    rows.append(('Baseline, %s accounts (Plan Section 5.3)' % '{:,}'.format(len(mc['pop'])), '%d' % f['baseline_af_nearest_10']))
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            tb.cell(i, j).text = v
            if i == 0 and v:
                tb.cell(i, j).paragraphs[0].runs[0].bold = True
    note = d.add_paragraph('Saving against each account\'s Plan Section 5.3 baseline, at the 2026 rates plus the option; '
                           'the split by bill month is in stage2_drought_rates_2027.xlsx. Source: CIS bill export of '
                           'November 2, 2026.')
    note.runs[0].font.size = Pt(8.5)
    note.runs[0].italic = True
    d.add_heading('Why the surcharge saves the most', level=2)
    d.add_paragraph('The July 2023 restructuring raised the last block price sharply for heavy summer users and their '
                    'use barely moved, which on its own suggests customers do not respond to the block price on their '
                    'last thousand gallons. The Fenwick Mesa capital recovery charge is the test: from the July 2024 '
                    'bills it added USD %.2f to every Fenwick Mesa bill and changed no block price, and against the rest '
                    'of the city Fenwick Mesa\'s July to September use fell %.1f per cent between 2023 and 2025 while '
                    'its bills per thousand gallons rose %.1f per cent. Customers answer what the whole bill comes to per '
                    'thousand gallons, at an elasticity of about %.2f (%.2f to %.2f across the other summers and price '
                    'readings of the same comparison).' % (
                        W.FM_CHARGE, f['fenwick_mesa_use_fall_pct'], f['fenwick_mesa_price_change_pct'], f['elasticity'],
                        f['elasticity_band'][0], f['elasticity_band'][1]))
    d.add_paragraph('Priced that way, at each account\'s baseline use on each bill, the surcharge raises every bill and '
                    'moves the most water. Option A barely changes the bill of a typical household (it cuts the first '
                    'block as it raises the third), and Option B adds less to most bills than Option C does.')
    d.add_heading('City measures, 2026 base', level=2)
    d.add_paragraph('For the 2027 targets for the City\'s own measures, the June to September 2026 figures are:')
    tb2 = d.add_table(rows=5, cols=4)
    tb2.style = 'Table Grid'
    hdr = ('Month', 'Fill station, thousand gallons', 'Tank fills', 'City facilities, acre-feet')
    for j, v in enumerate(hdr):
        tb2.cell(0, j).text = v
        tb2.cell(0, j).paragraphs[0].runs[0].bold = True
    for i, m in enumerate(Rt.SUMMER, start=1):
        tb2.cell(i, 0).text = MONTH[m]
        tb2.cell(i, 1).text = '{:,}'.format(f['ask']['fill_kgal'][MONTH[m]])
        tb2.cell(i, 2).text = '%d' % f['ask']['fills'][MONTH[m]]
        tb2.cell(i, 3).text = '%.1f' % f['ask']['facilities_af'][MONTH[m]]
    n2 = d.add_paragraph('A fill resumed at bay 2 after the coupling faulted is counted once, from its opening register. '
                         'The pool fill meter at Westbrook is read for pool operations; its water is already on the '
                         'pavilion meter and is not added again. Source: fill station transaction export; facility meter '
                         'read log; meter shop work orders.')
    n2.runs[0].font.size = Pt(8.5)
    n2.runs[0].italic = True
    d.add_paragraph('Staff will report the drought reserve revenue of the recommended option with the hearing packet, '
                    'as the agenda report says.')
    cp = d.core_properties
    cp.author = 'Tami Weaver'
    cp.last_modified_by = 'Tami Weaver'
    created = dt.datetime(2026, 11, 3, 17, 26, 41)
    cp.created = created
    cp.modified = created
    cp.revision = 3
    cp.title = 'Stage 2 drought rate recommendation'
    cp.comments = ''
    d.save(path)
    normalise(path, 'Microsoft Office Word')


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
    bottom = np.zeros(3)
    for m in Rt.SUMMER:
        v = np.array([Rt.af(mc['sav'][o][m]) for o in 'ABC'])
        ax.bar(x, v, 0.52, bottom=bottom, color=ramp[m], label=MONTH[m] + ' bills', edgecolor=surface, linewidth=1.6,
               zorder=3)
        bottom += v
    win = mc['rank'][0]
    for i, o in enumerate('ABC'):
        ax.text(i, bottom[i] + 0.7, 'about %d acre-feet' % f['saving_af_nearest_10'][o], ha='center', va='bottom',
                fontsize=10, color=ink, fontweight='bold' if o == win else 'normal')
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
    ax.set_ylim(0, max(bottom) * 1.22)
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
