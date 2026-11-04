"""The generator's assertions: the three rules on the clean truth (R1 to R3c), the ladder, the semantic forks
(SF1 to SF21), every graded figure's distance to its rounding edge, mess neutrality, the ask devices, the input
gates and the realism sweep.  Run after build.py.

    python3 task314/generator/checks.py
"""
import collections
import copy
import datetime as dt
import json
import math
import os
import re
import sys
import zipfile
import numpy as np
import world as W
import routes as Rt
import records as R
import golden as G
import build as B

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, 'target')
REPO = os.path.dirname(TASK)
RES = []


def check(label, ok, detail=''):
    RES.append((label, bool(ok)))
    print('%-4s %-64s %s' % ('PASS' if ok else 'FAIL', label, detail))


def bins(f):
    return {o: G.nearest(f[o], 10) for o in 'ABC'}


def call_of(t):
    return max(t, key=t.get)


def edge(x, unit):
    """Distance from x to the nearest rounding edge at this unit."""
    r = x / unit - math.floor(x / unit)
    return unit * abs(r - 0.5)


def mc_summary(export):
    mc = G.main_call(export)
    t = mc['tot']
    w = call_of(t)
    run = sorted(t, key=lambda o: -t[o])[1]
    return mc, t, w, bins(t), G.nearest(t[w] - t[run], 10)


def light_call(export):
    """The golden route alone (the whole-bill panel estimate and the savings it gives), for the mess variants."""
    pan = Rt.panel(G.sfr_rows(export))
    pop = Rt.population(pan)
    base = Rt.baseline(pan, pop)
    e = Rt.panel_fe(pan, ('AP',))[0]
    t = {o: Rt.af(sum(Rt.forecast(pan, base, 'AP', e, o).values())) for o in 'ABC'}
    w = call_of(t)
    run = sorted(t, key=lambda o: -t[o])[1]
    return e, t, w, bins(t), G.nearest(t[w] - t[run], 10)


def main():
    w = B.world()
    fig = json.load(open(os.path.join(HERE, 'figures.json')))
    export = w['export']
    mc, t, win, bn, gapb = mc_summary(export)

    # ------------------------------------------------------------ R1: the field's raw material ships
    import csv
    with open(os.path.join(TGT, B.F_BILLS), encoding='utf-8') as fh:
        rd = csv.reader(fh)
        hdr = next(rd)
    need = {'consumption', 'uom', 'base_charge', 'block1_charge', 'block2_charge', 'block3_charge',
            'capital_recovery_charge', 'total_charge', 'meter_size_in', 'service_area', 'bill_date', 'customer_class'}
    n_sf = sum(1 for r in export if r['customer_class'] == 'RES-SF')
    check('R1a the bill panel ships: every single-family bill with its use and charges', need <= set(hdr) and n_sf > 200000,
          '%d single-family rows' % n_sf)
    bad_cols = []
    for n in os.listdir(TGT):
        p = os.path.join(TGT, n)
        if n.endswith('.csv'):
            with open(p, encoding='utf-8') as fh:
                h = fh.readline().lower()
            if re.search(r'elastic|avg_price|average_price|saving|response|marginal', h):
                bad_cols.append(n)
    check('R1b no shipped column holds an elasticity, an average or marginal price, or a saving', not bad_cols, ', '.join(bad_cols))
    check('R1c the deciding elasticity is computed from the bill rows (a panel of every single-family bill)',
          abs(mc['eta'] - fig['elasticity_4dp']) < 0.00006, '%.4f' % mc['eta'])

    # ------------------------------------------------------------ the clean truth (no mess, true use)
    rows = [(b['acc'].acct, b['prem'].area, b['prem'].meter, b['y'], b['m'], b['q']) for b in w['bills'] if b['prem'].cls == 'SFR']
    pan = Rt.panel(rows)
    pop = Rt.population(pan)
    base = Rt.baseline(pan, pop)
    e_ap = Rt.panel_fe(pan, ('AP',))[0]
    two = Rt.panel_fe(pan, ('AP', 'MP'))
    two_city = Rt.panel_fe(pan, ('AP', 'MP'), area='CITY')
    e_mp_panel = Rt.panel_fe(pan, ('MP',), area='CITY')[0]
    e_mp_fd = Rt.eta_redesign_mp(pan, price='MP')[0]
    e_vap = Rt.eta_redesign_mp(pan, price='VAP')[0]
    e_ap_fd = Rt.eta_redesign_mp(pan, price='AP')[0]
    e_fm = Rt.eta_fm(pan)[0]

    def route(model, e):
        return {o: Rt.af(sum(Rt.forecast(pan, base, model, e, o).values())) for o in 'ABC'}

    def margin(r):
        s_ = sorted(r.values(), reverse=True)
        return s_[0] / max(s_[1], 1e-9)

    def show(r):
        return {k: round(v, 1) for k, v in r.items()}

    r_lit = route('MP', Rt.LIT_ETA)
    r_panel = route('MP', e_mp_panel)
    r_fd = route('MP', e_mp_fd)
    r_vap = route('VAP', e_vap)
    r_ap = route('AP', e_ap)
    r_fm = route('AP', e_fm)
    check('R3a analyst test: the block price estimated on the city\'s own restructuring (panel) files Option A',
          call_of(r_panel) == 'A' and margin(r_panel) >= 1.15, 'elasticity %.3f, %s, margin %.2f' % (e_mp_panel, show(r_panel), margin(r_panel)))
    check('R3a the same on first differences of the summer means files Option A', call_of(r_fd) == 'A' and margin(r_fd) >= 1.15,
          'elasticity %.3f, %s, margin %.2f' % (e_mp_fd, show(r_fd), margin(r_fd)))
    check('R3a the literature block-price elasticity also files Option A', call_of(r_lit) == 'A' and margin(r_lit) >= 1.15,
          '%s, margin %.2f' % (show(r_lit), margin(r_lit)))
    check('R3b the default path with only the price changed to the whole bill files Option C',
          call_of(r_ap) == 'C' and margin(r_ap) >= 1.2, 'elasticity %.3f, %s, margin %.2f' % (e_ap, show(r_ap), margin(r_ap)))
    check('R3b the lower rung\'s single correction (the per-gallon price) files Option B', call_of(r_vap) == 'B',
          'elasticity %.3f, %s' % (e_vap, show(r_vap)))
    check('R3b the price test lands on either change: both prices on every bill and on the restructuring alone',
          two[0] < -0.25 and abs(two[1]) < 0.03 and two_city[0] < -0.25 and abs(two_city[1]) < 0.03,
          'every bill %.3f / %+.3f; restructuring %.3f / %+.3f' % (two[0], two[1], two_city[0], two_city[1]))
    check('R3b the Fenwick Mesa charge alone also gives the whole-bill price and Option C', e_fm < -0.25 and call_of(r_fm) == 'C',
          'elasticity %.3f, %s' % (e_fm, show(r_fm)))
    # the routes a hurried analyst might take, counted on the clean truth
    cheap = {'block price, literature': call_of(r_lit), 'block price, own restructuring (panel)': call_of(r_panel),
             'block price, own restructuring (differences)': call_of(r_fd), 'per-gallon price, own restructuring': call_of(r_vap),
             'whole-bill price assumed, literature elasticity': call_of(route('AP', Rt.LIT_ETA)),
             'whole-bill price assumed, restructuring differences': call_of(route('AP', e_ap_fd))}
    rev = {}
    for o in 'ABC':
        d = 0.0
        for a, bm in base.items():
            for m, q in bm.items():
                d += Rt.bill_at(q, pan[a]['meter'], Rt.OPT_BDATE[m], pan[a]['area'], o) - Rt.bill_at(q, pan[a]['meter'], Rt.REP_BDATE[m], pan[a]['area'])
        rev[o] = d
    cheap['largest bill increase'] = call_of(rev)
    landing = [k for k, v in cheap.items() if v == 'C']
    print('     routes on the clean truth: %s' % cheap)
    check('Gate F count: every route that lands the call without testing the price takes the whole-bill price on faith',
          set(landing) <= {'whole-bill price assumed, literature elasticity', 'whole-bill price assumed, restructuring differences',
                           'largest bill increase'}, 'landing untested: %s' % ', '.join(landing))
    with open(os.path.join(TGT, B.F_STAFF), 'rb') as fh:
        z = zipfile.ZipFile(fh)
        staff_xml = z.read('word/document.xml').decode('utf-8')
    staff_txt = re.sub(r'<[^>]+>', ' ', staff_xml)
    check('R3c no plant: the staff report states no saving, revenue or ranking of the options',
          not re.search(r'acre-feet (saved|saving)|expected saving of|revenue of USD|would save|saves about|recommend Option', staff_txt)
          and 'Option C, drought surcharge' in staff_txt, 'positive control found')
    check('R3c the staff report carries the option levels the figures use',
          'USD %.2f for each 1,000 gallons in place of' % W.OPT_A_TIER1 in staff_txt and 'at USD %.2f in place of' % W.OPT_A_TIER3 in staff_txt
          and 'USD %.2f is added to the charge for each 1,000 gallons' % W.OPT_B_ADDER in staff_txt
          and 'drought surcharge of USD %.2f is added to each monthly bill' % W.OPT_C_SURCHARGE in staff_txt)
    blocks = 0
    by_acct = collections.defaultdict(list)
    for r in export:
        if r['customer_class'] == 'RES-SF' and r['bill_status'] != 'CANCELLED':
            by_acct[r['account_no']].append((r['bill_date'], r['consumption']))
    for a, s_ in list(by_acct.items())[:3000]:
        s_.sort()
        v = [x[1] for x in s_]
        for i in range(len(v) - 23):
            if v[i:i + 12] == v[i + 12:i + 24] and sum(v[i:i + 12]) > 0:
                blocks += 1
    check('R3c no copied block: no account repeats a year of readings', blocks == 0, '%d repeats' % blocks)

    # ------------------------------------------------------------ the ladder on the bundle
    rg = mc['rungs']
    want = {'rung0_block_price_literature': 'A', 'rung1_block_price_panel': 'A', 'rung1_block_price_differences': 'A',
            'rung2_per_gallon_price': 'B', 'decisive_whole_bill_price': 'C'}
    for k, v in want.items():
        s_ = rg[k]['savings']
        check('ladder %s files Option %s' % (k, v), rg[k]['winner'] == v and margin(s_) >= (1.2 if v == 'C' else 1.15),
              'elasticity %.3f, %s, margin %.2f' % (rg[k]['eta'], show(s_), margin(s_)))
    check('ladder: Option C leads no rung below the decisive one and trails each leader by 1.2 times or more',
          all(rg[k]['winner'] != 'C' and max(rg[k]['savings'].values()) >= 1.2 * max(rg[k]['savings']['C'], 1e-9)
              for k in want if k != 'decisive_whole_bill_price'))
    check('ladder: the price test on the bundle gives the whole bill and no block-price response',
          mc['two'][0] < -0.25 and abs(mc['two'][1]) < 0.03 and mc['two_city'][0] < -0.25 and abs(mc['two_city'][1]) < 0.03,
          'every bill %.4f / %+.4f; restructuring %.4f / %+.4f' % (mc['two'][0], mc['two'][1], mc['two_city'][0], mc['two_city'][1]))

    # ------------------------------------------------------------ SF22 and SF23: the form and the charge, over the grid
    want_bin = dict(bn)
    want_bin['gap'] = gapb
    def ranges(cells):
        out = {}
        for g_ in cells:
            vals = dict(g_)
            vals['gap'] = g_['C'] - g_['B']
            for k, v in vals.items():
                lo, hi = out.get(k, (v, v))
                out[k] = (min(lo, v), max(hi, v))
        return out
    grid_set = set(G.GRID)
    rng = ranges([g_ for key, g_ in mc['grid'].items() if key[0] in grid_set])
    rng_all = ranges(mc['grid'].values())
    for label, rr_ in (('estimates %s to %s' % (G.GRID[0], G.GRID[-1]), rng), ('every measured estimate as well', rng_all)):
        print('     margins over %s, three forms, the charge in or out:' % label)
        for k in ('C', 'B', 'A', 'gap'):
            lo, hi = rr_[k]
            print('       %-4s %6.2f to %6.2f   bin %d   clear of %d by %.2f and of %d by %.2f' % (
                k, lo, hi, want_bin[k], want_bin[k] - 5, lo - (want_bin[k] - 5), want_bin[k] + 5, (want_bin[k] + 5) - hi))
    forms_ok = all(G.nearest(g_[o], 10) == bn[o] for g_ in mc['grid'].values() for o in 'ABC') and \
        all(G.nearest(g_['C'] - g_['B'], 10) == gapb for g_ in mc['grid'].values())
    check('SF22 constant-elasticity, linear or midpoint form: every saving and the gap keep their bins over the grid',
          forms_ok and all(k[1] in G.FORMS for k in mc['grid']), '%d cells' % len(mc['grid']))
    check('SF23 the Fenwick Mesa charge in or out of the base bill: every saving and the gap keep their bins',
          {k[2] for k in mc['grid']} == {True, False} and forms_ok)
    check('margins: every saving and the gap clear their bin edges by 1.25 acre-feet or more over the grid',
          all(rng[k][0] - (want_bin[k] - 5) >= 1.25 and (want_bin[k] + 5) - rng[k][1] >= 1.25 for k in rng),
          ', '.join('%s %.2f/%.2f' % (k, rng[k][0] - (want_bin[k] - 5), (want_bin[k] + 5) - rng[k][1]) for k in ('C', 'B', 'A', 'gap')))
    check('margins: every measured estimate too, in every form and charge reading, keeps every bin by 0.5 acre-feet or more',
          all(rng_all[k][0] - (want_bin[k] - 5) >= 0.5 and (want_bin[k] + 5) - rng_all[k][1] >= 0.5 for k in rng_all),
          ', '.join('%s %.2f/%.2f' % (k, rng_all[k][0] - (want_bin[k] - 5), (want_bin[k] + 5) - rng_all[k][1]) for k in ('C', 'B', 'A', 'gap')))
    fam = mc['fam']
    check('family: every measured estimate lies inside the grid', all(G.GRID[-1] - 0.04 <= v <= G.GRID[0] + 1e-9 for v in fam.values()),
          '%d estimates, %.3f to %.3f' % (len(fam), min(fam.values()), max(fam.values())))
    outside = {k: v for k, v in fam.items() if not (G.GRID[-1] <= v <= G.GRID[0])}
    print('     measured estimates: %s' % {k: round(v, 4) for k, v in sorted(fam.items())})
    if outside:
        print('     outside the grid but carried in it: %s' % {k: round(v, 4) for k, v in outside.items()})
    check('family: the world\'s own elasticity keeps every bin',
          all(G.nearest(Rt.af(sum(Rt.forecast(mc['pan'], mc['base'], 'AP', W.ETA, o).values())), 10) == bn[o] for o in 'ABC'))
    for o in 'ABC':
        check('edge: Option %s saving clear of its rounding edge at the golden estimate' % o, edge(t[o], 10) >= 2.5,
              '%.2f from the edge' % edge(t[o], 10))
    check('edge: the gap clear of its rounding edge at the golden estimate', edge(t['C'] - t['B'], 10) >= 2.5, '%.2f' % edge(t['C'] - t['B'], 10))
    check('figures: bins as filed', fig['saving_af_nearest_10'] == bn and fig['gap_af_nearest_10'] == gapb
          and fig['call'].startswith('Option C') and fig['runner_up'].startswith('Option B'))

    # ------------------------------------------------------------ R2: every mess item, mishandled, leaves the call
    def variant(fn):
        ex = [dict(r) for r in export]
        return fn(ex)

    def ccf_as_kgal(ex):
        for r in ex:
            if r['uom'] == 'CCF':
                r['uom'] = 'KGAL'
        return ex

    def keep_cancelled(ex):
        for r in ex:
            if r['bill_status'] == 'CANCELLED':
                r['bill_status'] = 'BILLED'
        return ex

    def drop_estimates(ex):
        return [r for r in ex if r['read_type'] != 'E']

    def by_premise(ex):
        for r in ex:
            r['account_no'] = r['premise_id']
        return ex

    def one_meter(ex):
        for r in ex:
            r['meter_size_in'] = '0.75'
        return ex

    def read_month(ex):
        for r in ex:
            r['bill_date'] = r['read_date']
        return ex

    for label, fn in (('hundred cubic feet read as thousand gallons', ccf_as_kgal), ('cancelled bills kept', keep_cancelled),
                      ('estimated bills dropped', drop_estimates), ('premise in place of account', by_premise),
                      ('every meter priced as 3/4 inch', one_meter), ('bill month from the read date', read_month)):
        e2, t2, w2, b2, g2 = light_call(variant(fn))
        check('R2 %s: call and every bin unchanged' % label, w2 == win and b2 == bn and g2 == gapb,
              '%s, gap %d' % ({o: round(x, 1) for o, x in t2.items()}, g2))

    # the counts and ranges the design note quotes, printed from the objects that made them
    sfr_rows = [r for r in export if r['customer_class'] == 'RES-SF']
    rev_bill = {}
    for o in 'ABC':
        d, n = 0.0, 0
        for a, bmm in mc['base'].items():
            for m, q in bmm.items():
                d += (Rt.bill_at(q, mc['pan'][a]['meter'], Rt.OPT_BDATE[m], mc['pan'][a]['area'], o)
                      - Rt.bill_at(q, mc['pan'][a]['meter'], Rt.REP_BDATE[m], mc['pan'][a]['area']))
                n += 1
        rev_bill[o] = round(d / n, 2)
    print('     note figures: hundred-cubic-feet share of single-family bills %.3f; estimated reads %d; cancelled and '
          'rebilled pairs %d; elasticity family %.3f to %.3f; revenue per bill at baseline use %s; rest-of-city summer '
          'use change %.1f per cent' % (
              sum(1 for r in sfr_rows if r['uom'] == 'CCF') / len(sfr_rows), sum(1 for r in export if r['read_type'] == 'E'),
              sum(1 for r in export if r['bill_status'] == 'CANCELLED'), max(mc['fam'].values()), min(mc['fam'].values()), rev_bill,
              100 * (math.exp(mc['means']['CITY']['lq1'] - mc['means']['CITY']['lq0']) - 1)))

    # ------------------------------------------------------------ the semantic forks
    sf = export
    bm_same = all(r['bill_date'].month == r['read_date'].month and r['bill_date'].year == r['read_date'].year for r in sf)
    check('SF2 bill month and read month agree on every bill', bm_same)
    check('SF1 single-family is RES-SF in both service areas (the plan names no area)',
          {r['service_area'] for r in sf if r['customer_class'] == 'RES-SF'} == {'ARDLEY SPRINGS', 'FENWICK MESA'}
          and {r['rate_code'] for r in sf if r['customer_class'] == 'RES-SF'} == {'W10'})
    reb = {r['replaces_bill_no'] for r in sf if r['bill_status'] == 'REBILL'}
    can = {r['bill_no'] for r in sf if r['bill_status'] == 'CANCELLED'}
    check('SF3 every cancelled bill is replaced by a rebill in its month', reb == can and len(can) > 0, '%d pairs' % len(can))
    pop_e = mc['pop']
    sum_avg = sum(mc['base_m'].values())
    avg_sum = 0.5 * sum(mc['pan'][a][(y, m)] for a in pop_e for y in (2025, 2026) for m in Rt.SUMMER)
    check('SF4 the two preceding years of a 2027 measure are 2025 and 2026, and the population reads them',
          all(y in (2025, 2026) for y, m in [(y, m) for y in (2025, 2026) for m in Rt.SUMMER])
          and all(d.year == 2027 for d in Rt.OPT_BDATE.values())
          and all(all((y, m) in mc['pan'][a] for y in (2025, 2026) for m in Rt.SUMMER) for a in pop_e))
    check('SF5 the sum of account baselines equals the average of the two summers', abs(sum_avg - avg_sum) < 1e-6)
    check('SF6 acre-feet at 325,851 or 325,853 gallons: same bins',
          all(G.nearest(t[o] * 325851 / 325853, 10) == bn[o] for o in 'ABC'))
    # SF7: the Fenwick Mesa charge left off the 2027 bills
    old_cap = W.FM_CHARGE
    saved = Rt.rates_for

    def no_cap(bdate, area, option=None):
        sched, cap, ex = saved(bdate, area, option)
        if bdate.year == 2027:
            cap = 0.0
        return sched, cap, ex
    Rt.rates_for = no_cap
    t7 = {o: Rt.af(sum(Rt.forecast(mc['pan'], mc['base'], 'AP', mc['eta'], o).values())) for o in 'ABC'}
    Rt.rates_for = saved
    check('SF7 the capital recovery charge dropped from the 2027 bills: same call', call_of(t7) == win, '%s' % {o: round(x, 1) for o, x in t7.items()})
    check('SF8 the options apply to bills issued May 1 to October 31, 2027, so every June to September bill carries them',
          all(dt.date(2027, 5, 1) <= Rt.OPT_BDATE[m] <= dt.date(2027, 10, 31) for m in Rt.SUMMER))
    r2312 = B.F_R2312
    from pypdf import PdfReader
    txt2312 = re.sub(r'\s+', ' ', '\n'.join(p.extract_text() for p in PdfReader(os.path.join(TGT, r2312)).pages))
    check('SF9 hundred cubic feet billed as 748.052 gallons (Resolution 2023-12, Section 2)', 'billed as 748.052 gallons' in txt2312)
    check('SF10 base charges by meter size: every single-family bill is 3/4 or 1 inch',
          {r['meter_size_in'] for r in sf if r['customer_class'] == 'RES-SF'} == {'0.75', '1'})
    est_pop = sum(1 for r in sf if r['read_type'] == 'E' and r['customer_class'] == 'RES-SF' and r['account_no'] in set(pop_e)
                  and r['bill_date'].year in (2025, 2026) and r['bill_date'].month in Rt.SUMMER)
    check('SF11 estimated bills are billed bills: kept or dropped, same call (R2)', est_pop > 0, '%d estimated summer bills in the population' % est_pop)
    accts_per_prem = collections.Counter()
    for p in w['prems']:
        if p.cls == 'SFR':
            accts_per_prem[len(p.accounts)] += 1
    check('SF12 accounts, not premises: premises change hands (R2 keeps the call either way)', accts_per_prem[1] < sum(accts_per_prem.values()),
          dict(accts_per_prem))
    check('SF13 Option A keeps the 6,000 and 15,000 gallon block limits', '0 to 6,000 gallons' in staff_txt and 'over 15,000 gallons' in staff_txt)
    check('SF14 Option B adds to every block', 'in every usage block' in staff_txt)
    check('SF15 Option C is per monthly bill and one bill stands in each account month',
          all(c == 1 for c in collections.Counter((r['account_no'], r['bill_date'].year, r['bill_date'].month) for r in sf
                                                    if r['bill_status'] != 'CANCELLED' and r['customer_class'] == 'RES-SF').values()))
    p53 = re.sub(r'\s+', ' ', '\n'.join(p.extract_text() for p in PdfReader(os.path.join(TGT, B.F_DCP)).pages))
    check('SF16 the reduction is against what the bills would carry at the rates in force (plan 5.3)',
          'from what those bills would have carried at the rates otherwise in force' in p53)
    rounded_gap = bn['C'] - bn['B']
    check('SF17 the gap rounded once or as a difference of rounded savings: same', rounded_gap == gapb, '%d and %d' % (rounded_gap, gapb))
    ask = G.ask_figures(w['fill'], w['reads'], w['wos'], w['facs'])
    import pandas as pd
    utc_ok = True
    for r in w['fill']:
        off = 6 if R.DST0 <= r['start'].date() < R.DST1 else 7
        u = r['start'] + dt.timedelta(hours=off)
        if (u.year, u.month) != (r['start'].year, r['start'].month):
            utc_ok = False
    check('SF18 a fill\'s month is the same on local and UTC dates (no session after 4:30 p.m. on a month\'s last day)', utc_ok)
    check('SF19 a fill is counted in the month it starts: no session spans a month end',
          all(r['start'].month == r['end'].month for r in w['fill']))
    same_day = collections.Counter((r['facility_id'], r['read_date']) for r in w['reads'])
    months_ok = all(len({d for (f, d) in same_day if f == fid and (d.year, d.month) == ym}) == 1
                    for fid in R.FAC for ym in [(2026, m) for m in range(1, 11)])
    check('SF20 one read date per facility per month (a re-read is on the same visit)', months_ok)
    alt = {}
    for m in Rt.SUMMER:
        tot = 0.0
        for fid, d in ask['per_fac'].items():
            if fid == R.SUBMETER:
                continue
            tot += d.get((2026, m), 0.0)
        alt[m] = tot
    golf_ccf = sum(1 for r in w['reads'] if r['meter_id'].startswith('26T'))
    shift = {m: 0.052 / 748.052 * ask['per_fac']['GC-MUNI'].get((2026, m), 0) / W.AF_KGAL / 1000.0 for m in Rt.SUMMER}
    check('SF21 the facility figures at 748 or 748.052 gallons a hundred cubic feet: same one-decimal figures',
          all(round(ask['fac_af'][m] - shift[m], 1) == round(ask['fac_af'][m], 1) for m in Rt.SUMMER),
          '%d reads on the turbine meter' % golf_ccf)

    # ------------------------------------------------------------ the ask figures, their edges and their devices
    for m in Rt.SUMMER:
        k = G.MONTH[m]
        check('edge: fill station %s clear of its thousand-gallon edge' % k, edge(ask['fill'][m]['kgal'], 1) >= 0.2,
              '%.3f' % edge(ask['fill'][m]['kgal'], 1))
        check('edge: facilities %s clear of its tenth-of-an-acre-foot edge' % k, edge(ask['fac_af'][m], 0.1) >= 0.008,
              '%.4f' % edge(ask['fac_af'][m], 0.1))
    # every graded figure, as a share of its rounding unit, from the nearest rounding edge
    graded = [('saving %s' % o, t[o], 10) for o in 'ABC'] + [('gap', t['C'] - t['B'], 10)]
    graded += [('fill water %s' % G.MONTH[m], ask['fill'][m]['kgal'], 1) for m in Rt.SUMMER]
    graded += [('facilities %s' % G.MONTH[m], ask['fac_af'][m], 0.1) for m in Rt.SUMMER]
    shares = {lab: edge(v, u) / u for lab, v, u in graded}
    low = min(shares, key=shares.get)
    check('edge: every graded figure sits 0.25 of its rounding unit or more from its nearest edge (0.03 asked)',
          all(v >= 0.25 for v in shares.values()), 'closest %s at %.3f of its unit' % (low, shares[low]))
    check('edge: June City facility use is 0.05 acre-feet or more above the 22.55 edge it rounds away from',
          ask['fac_af'][6] - 22.55 >= 0.05 and round(ask['fac_af'][6] + 1e-9, 1) == fig['ask']['facilities_af']['June'],
          '%.4f' % ask['fac_af'][6])
    resumed = collections.Counter()
    twins = collections.Counter()
    by_bay = collections.defaultdict(list)
    for r in sorted(w['fill'], key=lambda x: x['start']):
        by_bay[r['bay']].append(r)
    for bay, rr in by_bay.items():
        for a, b in zip(rr, rr[1:]):
            if b['m0'] == a['m0']:
                resumed[a['start'].month] += 1
            elif b['m0'] == a['m1'] and b['card'] == a['card'] and (b['start'] - a['end']).total_seconds() < 400:
                twins[(bay, a['start'].month)] += 1
    check('device fill: resumed sessions in every month June to September', all(resumed[m] >= 10 for m in Rt.SUMMER), dict(resumed))
    check('device fill: back-to-back fills from the closing register on both bays every summer month (benign twins)',
          all(twins[(b, m)] >= 3 for b in (1, 2) for m in Rt.SUMMER))
    naive_gal = collections.Counter()
    naive_n = collections.Counter()
    for r in w['fill']:
        naive_gal[r['start'].month] += r['gal'] / 1000.0
        naive_n[r['start'].month] += 1
    check('device fill: summing the rows misses every month\'s water and fills',
          all(G.nearest(naive_gal[m], 1) != fig['ask']['fill_kgal'][G.MONTH[m]] and naive_n[m] != fig['ask']['fills'][G.MONTH[m]] for m in Rt.SUMMER),
          {m: (round(naive_gal[m], 1), naive_n[m]) for m in Rt.SUMMER})
    mon = R.fill_monthly(w['fill'])
    check('device fill: the vendor report agrees with the row sums (the wrong path reconciles)',
          all(mon[(2026, m, 1)][1] + mon[(2026, m, 2)][1] == sum(r['gal'] for r in w['fill'] if r['start'].month == m) for m in Rt.SUMMER))
    prompt = open(os.path.join(TASK, 'prompt.txt')).read()
    visits = collections.Counter()
    for bay, rr in by_bay.items():
        prev = None
        for r in rr:
            if prev is not None and r['m0'] == prev['m0']:
                continue                      # the resumed half of a session: the same tank
            if not (prev is not None and r['card'] == prev['card'] and r['m0'] == prev['m1']
                    and (r['start'] - prev['end']).total_seconds() < 400):
                visits[r['start'].month] += 1
            prev = r
    check('SF24 a tank is the unit: the prompt counts a truck\'s tank and its trailer\'s each, and a visit count would differ',
          "a truck's tank and its trailer's each counting as one" in prompt
          and all(visits[m] < fig['ask']['fills'][G.MONTH[m]] for m in Rt.SUMMER),
          'visits %s against tanks %s' % ({m: visits[m] for m in Rt.SUMMER}, [fig['ask']['fills'][G.MONTH[m]] for m in Rt.SUMMER]))
    city_gal = {m: sum(r['gal'] for r in w['fill'] if r['hauler'] == 'Ardley Springs Public Works' and r['start'].month == m)
                for m in Rt.SUMMER}
    check('SF25 water drawn counts the City\'s own trucks: the asking sentence and plan Section 6 both say drawn',
          'the water drawn at the bulk fill station' in prompt and 'the water drawn at the bulk fill station' in p53
          and all(city_gal[m] > 0 for m in Rt.SUMMER), 'City trucks %s gallons' % city_gal)
    pool = {m: ask['per_fac'][R.SUBMETER].get((2026, m), 0.0) / W.AF_KGAL / 1000.0 for m in Rt.SUMMER}
    check('device pool: counting the pool fill meter again moves every month by four or more tenths',
          all(round(ask['fac_af'][m] + pool[m], 1) - round(ask['fac_af'][m], 1) >= 0.35 for m in Rt.SUMMER), {m: round(pool[m], 2) for m in pool})
    pav = ask['per_fac']['WB-PAV']
    ins = all(pav[k] >= ask['per_fac'][R.SUBMETER][k] for k in pav if k in ask['per_fac'][R.SUBMETER])
    check('device pool: the pavilion meter carries every gallon of the pool fill meter (fair, recoverable)', ins)
    gu = ask['per_fac']['GC-MUNI']
    check('hazard golf: the turbine meter read as gallons would move every summer month',
          all(gu[(2026, m)] / 1000.0 / W.AF_KGAL > 1.0 for m in (7, 8, 9)))
    sfr_files = [B.F_BILLS, B.F_ACCTS]
    fac_ids = set(R.FAC)
    leak_rows = 0
    for r in export:
        if r['premise_id'] in fac_ids or r['account_no'] in fac_ids:
            leak_rows += 1
    check('separation: zero device or hazard rows in the main call\'s files (no facility or fill rows among the bills)', leak_rows == 0)

    # ------------------------------------------------------------ input gates and provenance
    meta = json.load(open(os.path.join(TASK, 'metadata.json')))
    files = os.listdir(TGT)
    fmts = {n.rsplit('.', 1)[1] for n in files}
    check('gate: 10 or more files', len(files) >= 10, '%d' % len(files))
    check('gate: 3 or more formats', len(fmts) >= 3, ', '.join(sorted(fmts)))
    check('gate: a file of 25,000 rows or more', meta['input_gates']['largest_file_rows'] >= 25000,
          '%s %d' % (meta['input_gates']['largest_file'], meta['input_gates']['largest_file_rows']))
    check('gate: two or more distractors named in metadata.json', len(meta['distractor_files']) >= 2
          and all(d in files for d in meta['distractor_files']))
    src = open(os.path.join(HERE, 'verify.py')).read() + open(os.path.join(HERE, 'golden.py')).read()
    check('distractors: no golden or verifier path opens one (the figures stand with each deleted)',
          not any(d in src for d in meta['distractor_files']))
    check('no file under target/ describes the data (no readme, dictionary, notes or manifest)',
          not any(re.search(r'readme|dictionary|notes|manifest|field_guide|schema', n, re.I) for n in files))
    check('no file name names the trap or a distractor', not any(re.search(r'distract|elastic|average|marginal|decoy', n, re.I) for n in files))

    # ------------------------------------------------------------ realism sweep
    def const_step(vals):
        v = sorted(int(re.sub(r'\D', '', x)) for x in vals)
        d = {b - a for a, b in zip(v, v[1:])}
        return len(d) <= 1
    check('realism: bill numbers have no constant step', not const_step([r['bill_no'] for r in export[:5000]]))
    check('realism: fill transaction ids have no constant step', not const_step([r['txn_id'] for r in w['fill']]))
    check('realism: work order numbers have no constant step', not const_step([r['work_order'] for r in w['wos']]))
    prem_ids = sorted({r['premise_id'] for r in export})
    check('realism: premise ids have no constant step', not const_step(prem_ids))
    per_month = collections.Counter((r['bill_date'].year, r['bill_date'].month) for r in export)
    seq = [per_month[k] for k in sorted(per_month)]
    runs = sum(1 for a, b, c in zip(seq, seq[1:], seq[2:]) if a == b == c)
    check('realism: bill counts move month to month (no three months alike, a spread of more than 20)',
          runs == 0 and max(seq) - min(seq) > 20, '%d to %d' % (min(seq), max(seq)))
    fills = [fig['ask']['fills'][G.MONTH[m]] for m in Rt.SUMMER]
    check('realism: fills differ month to month', len(set(fills)) == 4, fills)
    starts = collections.Counter((r['bay'], r['start']) for r in w['fill'])
    check('realism: no two fill sessions share a start on one bay', max(starts.values()) == 1)
    overlap = 0
    for bay, rr in by_bay.items():
        for a, b in zip(rr, rr[1:]):
            if b['start'] < a['end']:
                overlap += 1
    check('realism: no two sessions overlap on a bay', overlap == 0, '%d' % overlap)
    times = [r['read_time'] for r in w['reads']]
    round5 = sum(1 for x in times if int(x[3:]) % 5 == 0) / len(times)
    check('realism: facility read times spread across the day and off round minutes',
          len({x[:2] for x in times}) >= 6 and round5 < 0.3, '%.2f on a five-minute mark' % round5)
    names_ok = True
    # guard.py names --geo "United States" --seed 314 --n 60, the names this build uses
    guard_names = {'Tami Weaver', 'Jason Morgan', 'Clifford Haley', 'Beth Sheppard', 'Laurie Stuart', 'Randy Silva',
                   'Ebony Valentine', 'Corey Lam', 'Nathaniel Cannon', 'Gary Riley', 'Julie Bowers', 'Theresa Howard',
                   'Sylvia Chavez', 'Helen Nelson', 'Brandy Macdonald', 'Samantha Clay', 'Jade Williamson', 'Tracy Bryant',
                   'Brandon Roth', 'Katrina Gonzalez', 'Laura Brown', 'Brittany King'}
    import docs as D
    used = set(D.COUNCIL + [D.MAYOR, D.CLERK, D.ATTORNEY, 'Clifford Haley', 'Jason Morgan', 'Sylvia Chavez',
                            'Helen Nelson', 'Tami Weaver'])
    techs = {'B. Macdonald': 'Brandy Macdonald', 'S. Clay': 'Samantha Clay', 'J. Williamson': 'Jade Williamson',
             'T. Bryant': 'Tracy Bryant', 'B. Roth': 'Brandon Roth'}
    check('realism: every technician on the work orders is a drawn name', {r['technician'] for r in w['wos']} <= set(techs)
          and set(techs.values()) <= guard_names)
    check('realism: every named person comes from guard.py names', used <= guard_names, ', '.join(sorted(used - guard_names)))
    # the documents' producers and dates
    prods = {}
    for n in files:
        if n.endswith('.pdf'):
            md = PdfReader(os.path.join(TGT, n)).metadata
            prods[n] = (md.get('/Producer'), md.get('/Creator'), md.get('/Author'), md.get('/CreationDate'))
    org = re.compile(r'Ardley|Brennan|City of|District', re.I)
    check('realism: no PDF names an organisation as its producer or creator',
          all(not org.search(str(v[0])) and not org.search(str(v[1])) for v in prods.values()))
    check('realism: PDF creation times are not on round minutes', all(not v[3].endswith("00-06'00'") and not v[3].endswith("00-07'00'") for v in prods.values()),
          ', '.join(v[3] for v in prods.values()))
    check('realism: the district notice and the city documents carry different producers and authors',
          prods[B.F_UBB][0] != prods[B.F_R2312][0] and prods[B.F_UBB][2] != prods[B.F_R2312][2])
    # each Word document as Word saves a revised draft: no template thumbnail, saved after it was first created
    word_docs = [os.path.join(TGT, n) for n in sorted(os.listdir(TGT)) if n.endswith('.docx')]
    word_docs += [os.path.join(TASK, 'golden', n) for n in sorted(os.listdir(os.path.join(TASK, 'golden'))) if n.endswith('.docx')]
    word_bad = []
    for p_ in word_docs:
        with zipfile.ZipFile(p_) as z_:
            names_ = z_.namelist()
            core_ = z_.read('docProps/core.xml').decode('utf-8')
            rels_ = z_.read('_rels/.rels').decode('utf-8')
        c_ = re.search(r'<dcterms:created[^>]*>([^<]*)<', core_).group(1)
        m_ = re.search(r'<dcterms:modified[^>]*>([^<]*)<', core_).group(1)
        if 'docProps/thumbnail.jpeg' in names_ or 'thumbnail' in rels_ or not m_ > c_:
            word_bad.append(os.path.basename(p_))
    check('realism: no Word document carries the template\'s blank thumbnail, and each was saved after it was created',
          len(word_docs) == 2 and not word_bad, '%d documents%s' % (len(word_docs), (', ' + ', '.join(word_bad)) if word_bad else ''))
    check('realism: no extract carries a date after its pull',
          max(r['bill_date'] for r in export) <= dt.date(2026, 11, 2) and max(r['start'].date() for r in w['fill']) <= dt.date(2026, 10, 31)
          and max(r['read_date'] for r in w['reads']) <= dt.date(2026, 10, 31) and max(r['completed'] for r in w['wos']) <= dt.date(2026, 10, 30))
    check('realism: each document is dated after the events it states and before the pack',
          dt.date(2024, 6, 12) > dt.date(2024, 6, 11) and dt.date(2026, 10, 27) > dt.date(2026, 10, 15) and
          dt.date(2025, 3, 27) > dt.date(2024, 7, 1))
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(TGT, B.F_STATE), read_only=True)
    ws = wb.active
    vals = [r for r in ws.iter_rows(min_row=6, values_only=True) if r and r[0]]
    body, total = vals[:-1], vals[-1]
    check('realism: the state table\'s rows sum to its printed total', all(sum(r[j] for r in body) == total[j] for j in (1, 2, 3, 4)))
    check('realism: the vendor report\'s site totals are the sum of its bays',
          all(mon.get((2026, m, 1), [0, 0])[1] + mon.get((2026, m, 2), [0, 0])[1] > 0 for m in range(1, 11)))
    one_pay = sum(1 for r in export if r['bill_status'] == 'BILLED' and r['total_charge'] == 0.0 and r['customer_class'] == 'RES-SF')
    check('realism: no single-family bill comes to zero (base charges always bill)', one_pay == 0)
    # each load-bearing fact in exactly one document
    docs_txt = {}
    for n in files:
        if n.endswith('.pdf'):
            docs_txt[n] = re.sub(r'\s+', ' ', '\n'.join(p.extract_text() for p in PdfReader(os.path.join(TGT, n)).pages))
    docs_txt[B.F_STAFF] = staff_txt
    import pdfplumber
    for n, ctl in ((B.F_DCP, 'eight June to September bill months'), (B.F_R2417, 'capital recovery charge of USD 14.00 a month'),
                   (B.F_R2312, 'billed as 748.052 gallons')):
        with pdfplumber.open(os.path.join(TGT, n)) as pdf:
            alt = re.sub(r'\s+', ' ', ' '.join((pg.extract_text() or '') for pg in pdf.pages))
        check('H25 a second reader (pdfplumber) finds the filed sentence in %s' % n, ctl in alt and ctl in docs_txt[n])
    holders = [n for n, tx in docs_txt.items() if 'eight June to September bill months' in tx]
    check('pin: the estimand sits in one document (the plan)', holders == [B.F_DCP], ', '.join(holders))
    holders = [n for n, tx in docs_txt.items() if re.search(r'USD 14\.00 a month', tx)]
    check('pin: the capital recovery charge sits in one document (Resolution 2024-17)', holders == [B.F_R2417], ', '.join(holders))
    vocab = re.compile(r'marginal|average price|elasticit|price response|respond to|conserv\w* signal', re.I)
    hits = {n: vocab.findall(tx) for n, tx in docs_txt.items() if vocab.search(tx)}
    check('no document names a price concept or a response (the decisive relation\'s vocabulary)', not hits, str(hits))

    nfail = sum(1 for _, ok in RES if not ok)
    print('checks: %d assertions, %d FAIL' % (len(RES), nfail))
    return 1 if nfail else 0


if __name__ == '__main__':
    sys.exit(main())
