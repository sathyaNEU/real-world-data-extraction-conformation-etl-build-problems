"""The independent verifier: reads only target/, on its own code path (pandas, the documents' own text), and
recomputes every graded figure and every rung against generator/figures.json.

    python3 task314/generator/verify.py
"""
import json
import math
import os
import re
import sys
import zipfile
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, 'target')
AF_GAL = 325851.0
CCF_GAL = None          # read from the rate resolution
FAILS = []


def check(name, ok, detail=''):
    print('%-4s %-62s %s' % ('PASS' if ok else 'FAIL', name, detail))
    if not ok:
        FAILS.append(name)


def pdf_text(name):
    from pypdf import PdfReader
    r = PdfReader(os.path.join(TGT, name))
    return '\n'.join(p.extract_text() for p in r.pages)


def docx_text(name):
    from docx import Document
    d = Document(os.path.join(TGT, name))
    parts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            parts.append(' | '.join(c.text for c in row.cells))
    return '\n'.join(parts)


def num(s):
    return float(s.replace(',', ''))


def schedule_from(text):
    """Base charges and blocks of the single-family class from a resolution's Exhibit A."""
    t = re.sub(r'\s+', ' ', text)
    sec = t[t.index('1. Single-family residential'):t.index('2. Multi-family')]
    b34 = num(re.search(r'3/4 inch (\d+\.\d\d)', sec).group(1))
    b1 = num(re.search(r'(?<!/)1 inch (\d+\.\d\d)', sec).group(1))
    blocks = re.findall(r'(?:0 to ([\d,]+)|([\d,]+) to ([\d,]+)|Over ([\d,]+)) (\d+\.\d\d)', sec)
    tiers = []
    for g in blocks:
        if g[0]:
            tiers.append((num(g[0]) / 1000.0, num(g[4])))
        elif g[2]:
            tiers.append((num(g[2]) / 1000.0, num(g[4])))
        else:
            tiers.append((None, num(g[4])))
    return dict(base={0.75: b34, 1.0: b1}, tiers=tiers)


def main():
    global CCF_GAL
    fig = json.load(open(os.path.join(HERE, 'figures.json')))
    # ------------------------------------------------------------ the documents, through their own text
    r2144 = pdf_text('RES 2021-44.pdf')
    r2312 = pdf_text('RES 2023-12.pdf')
    r2417 = pdf_text('RES 2024-17.pdf')
    plan = pdf_text('Drought Contingency Plan Rev 2 (2025).pdf')
    notice = pdf_text('UBBWCD Notice 2026-07 Dry-Year Allocation 2027.pdf')
    staff = docx_text('Agenda Report Stage 2 Drought Rate Options DRAFT 2026-10-27.docx')
    for nm, tx, ctl in (('Res 2021-44', r2144, 'January 1, 2022'), ('Res 2023-12', r2312, 'July 1, 2023'),
                        ('Res 2024-17', r2417, 'July 1, 2024'), ('plan', plan, 'Sizing a rate measure'),
                        ('notice', notice, '78 per cent'), ('staff report', staff, 'Option C, drought surcharge')):
        check('read back %s (positive control)' % nm, len(tx) > 400 and ctl in re.sub(r'\s+', ' ', tx), '%d chars' % len(tx))
    old = schedule_from(r2144)
    new = schedule_from(r2312)
    CCF_GAL = num(re.search(r'billed as ([\d.]+) gallons', re.sub(r'\s+', ' ', r2312)).group(1))
    fm_charge = num(re.search(r'charge of USD (\d+\.\d\d) a month', re.sub(r'\s+', ' ', r2417)).group(1))
    st = re.sub(r'\s+', ' ', staff)
    a_t1 = num(re.search(r'billed at USD (\d+\.\d\d) for each 1,000 gallons in place of', st).group(1))
    a_t3 = num(re.search(r'third block \(over 15,000 gallons\) at USD (\d+\.\d\d)', st).group(1))
    b_add = num(re.search(r'USD (\d+\.\d\d) is added to the charge for each 1,000 gallons', st).group(1))
    c_sur = num(re.search(r'drought surcharge of USD (\d+\.\d\d) is added to each monthly bill', st).group(1))
    check('rates read from the documents', len(new['tiers']) == 3 and len(old['tiers']) == 3,
          'new %s old %s; FM %.2f; A %.2f/%.2f B %.2f C %.2f; CCF %.3f' % (new, old, fm_charge, a_t1, a_t3, b_add, c_sur, CCF_GAL))
    p53 = re.sub(r'\s+', ' ', plan)
    check('the plan files the estimand (5.3)', 'billed in each of the eight June to September bill months' in p53
          and 'average of the use billed to the account on that month' in p53)

    # ------------------------------------------------------------ the bills
    b = pd.read_csv(os.path.join(TGT, 'cis_water_bills_2022-06_to_2026-10.csv'), dtype={'account_no': str, 'bill_no': str,
                    'replaces_bill_no': str, 'read_cycle': str, 'meter_size_in': str})
    check('bill export read', len(b) > 25000, '%d rows' % len(b))
    s = b[(b.customer_class == 'RES-SF') & (b.bill_status != 'CANCELLED')].copy()
    s['kgal'] = np.where(s.uom == 'CCF', s.consumption * CCF_GAL / 1000.0, s.consumption)
    s['bd'] = pd.to_datetime(s.bill_date)
    s['y'] = s.bd.dt.year
    s['m'] = s.bd.dt.month
    s['fm'] = s.service_area == 'FENWICK MESA'
    s['meter'] = s.meter_size_in.astype(float)
    g = s.groupby(['account_no', 'y', 'm'], as_index=False).agg(kgal=('kgal', 'sum'), fm=('fm', 'first'),
                                                                 meter=('meter', 'first'))
    summer = [(y, m) for y in (2025, 2026) for m in (6, 7, 8, 9)]
    pv = g.pivot_table(index='account_no', columns=['y', 'm'], values='kgal', aggfunc='sum')
    have = pv[[c for c in summer]].notna().all(axis=1)
    pop = pv.index[have]
    info = g.groupby('account_no').agg(fm=('fm', 'first'), meter=('meter', 'first'))
    check('population', len(pop) == fig['accounts'], '%d accounts' % len(pop))
    base = {m: (pv.loc[pop, (2025, m)] + pv.loc[pop, (2026, m)]) / 2.0 for m in (6, 7, 8, 9)}
    base_af = sum(base[m].sum() for m in base) * 1000.0 / AF_GAL
    check('baseline', abs(base_af - fig['baseline_af']) < 0.06, '%.2f acre-feet' % base_af)

    def bill(q, meter, sched, cap=0.0, adder=0.0, t1=None, t3=None, sur=0.0):
        tiers = list(sched['tiers'])
        if t1 is not None:
            tiers[0] = (tiers[0][0], t1)
        if t3 is not None:
            tiers[2] = (None, t3)
        q = np.asarray(q, dtype=float)
        lo = 0.0
        vol = np.zeros_like(q)
        for hi, p in tiers:
            top = q if hi is None else np.minimum(q, hi)
            vol += np.maximum(0.0, top - lo) * (p + adder)
            if hi is not None:
                lo = hi
        return np.vectorize(lambda m: sched['base'][m])(meter) + vol + cap + sur

    def vol_only(q, sched, adder=0.0, t1=None, t3=None):
        return bill(q, np.full(len(np.atleast_1d(q)), 0.75), sched, 0.0, adder, t1, t3) - sched['base'][0.75]

    def mprice(q, sched, adder=0.0, t1=None, t3=None):
        tiers = list(sched['tiers'])
        if t1 is not None:
            tiers[0] = (tiers[0][0], t1)
        if t3 is not None:
            tiers[2] = (None, t3)
        q = np.asarray(q, dtype=float)
        out = np.full(q.shape, tiers[2][1] + adder)
        out = np.where(q <= tiers[1][0], tiers[1][1] + adder, out)
        out = np.where(q <= tiers[0][0], tiers[0][1] + adder, out)
        return out

    # ------------------------------------------------------------ the elasticity from the Fenwick Mesa charge
    k0 = [(2023, m) for m in (7, 8, 9)]
    k1 = [(2025, m) for m in (7, 8, 9)]
    ok = (pv[k0 + k1] > 0.3).all(axis=1)
    sub = pv.loc[ok]
    fm = info.loc[sub.index, 'fm'].values
    mt = info.loc[sub.index, 'meter'].values
    lq0 = np.log(sub[k0].values).mean(axis=1)
    lq1 = np.log(sub[k1].values).mean(axis=1)
    lp0 = np.mean([np.log(bill(sub[k].values, mt, new) / sub[k].values) for k in k0], axis=0)
    lp1 = np.mean([np.log(bill(sub[k].values, mt, new, np.where(fm, fm_charge, 0.0)) / sub[k].values) for k in k0], axis=0)
    did_q = (lq1 - lq0)[fm].mean() - (lq1 - lq0)[~fm].mean()
    did_p = (lp1 - lp0)[fm].mean() - (lp1 - lp0)[~fm].mean()
    eta = did_q / did_p
    check('elasticity on the whole-bill price', abs(eta - fig['elasticity_4dp']) < 0.00006, '%.4f (%d FM, %d city)' % (eta, fm.sum(), (~fm).sum()))

    # ------------------------------------------------------------ each option on each account's baseline bill
    pm = info.loc[pop, 'meter'].values
    pf = np.where(info.loc[pop, 'fm'].values, fm_charge, 0.0)
    opts = {'A': dict(t1=a_t1, t3=a_t3), 'B': dict(adder=b_add), 'C': dict(sur=c_sur)}

    def saving(model, e, o):
        tot = 0.0
        for m in (6, 7, 8, 9):
            q = base[m].values
            keep = q > 0
            q, mm, ff = q[keep], pm[keep], pf[keep]
            if model == 'AP':
                p0 = bill(q, mm, new, ff) / q
                p1 = bill(q, mm, new, ff, **opts[o]) / q
            elif model == 'VAP':
                p0 = vol_only(q, new) / q
                kw = {k: v for k, v in opts[o].items() if k != 'sur'}
                p1 = vol_only(q, new, **kw) / q
            else:
                p0 = mprice(q, new)
                kw = {k: v for k, v in opts[o].items() if k != 'sur'}
                p1 = mprice(q, new, **kw)
            tot += float((q * (1 - (p1 / p0) ** e)).sum())
        return tot * 1000.0 / AF_GAL

    sav = {o: saving('AP', eta, o) for o in 'ABC'}
    for o in 'ABC':
        check('option %s saving' % o, abs(sav[o] - fig['saving_af'][o]) < 0.06, '%.2f acre-feet' % sav[o])
    win = max(sav, key=sav.get)
    check('the call', fig['call'].startswith('Option %s' % win), win)
    # the redesign read on the block price, and the per-gallon price (the rungs below)
    j0 = [(2022, m) for m in (7, 8, 9)]
    j1 = [(2023, m) for m in (7, 8, 9)]
    okr = (pv[j0 + j1] > 0.3).all(axis=1) & (~info.loc[pv.index, 'fm'].values)
    sr = pv.loc[okr]
    y = np.log(sr[j1].values).mean(axis=1) - np.log(sr[j0].values).mean(axis=1)
    xm = np.mean([np.log(mprice(sr[j0[i]].values, new)) - np.log(mprice(sr[j0[i]].values, old)) for i in range(3)], axis=0)
    xv = np.mean([np.log(vol_only(sr[j0[i]].values, new) / sr[j0[i]].values) -
                  np.log(vol_only(sr[j0[i]].values, old) / sr[j0[i]].values) for i in range(3)], axis=0)
    e_mp = float(np.polyfit(xm, y, 1)[0])
    e_vap = float(np.polyfit(xv, y, 1)[0])
    check('redesign on the block price', abs(e_mp - fig['redesign_marginal_price_elasticity_4dp']) < 0.00006, '%.4f' % e_mp)
    r0 = {o: saving('MP', -0.40, o) for o in 'ABC'}
    r1 = {o: saving('MP', e_mp, o) for o in 'ABC'}
    r2 = {o: saving('VAP', e_vap, o) for o in 'ABC'}
    for nm, r, want in (('rung 0, literature block-price elasticity', r0, 'A'), ('rung 1, own block-price elasticity', r1, 'A'),
                        ('rung 2, per-gallon price', r2, 'B'), ('rung 3, whole-bill price', sav, 'C')):
        srt = sorted(r.values(), reverse=True)
        check(nm, max(r, key=r.get) == want and srt[0] >= 1.15 * srt[1],
              '%s, margin %.2f, %s' % (max(r, key=r.get), srt[0] / max(srt[1], 1e-9), {k: round(v, 1) for k, v in r.items()}))

    # ------------------------------------------------------------ the 2026 base for the City's own measures
    fs = pd.read_csv(os.path.join(TGT, 'fill_station_transactions_2026-01-01_2026-10-31.csv'))
    fs['local_date'] = pd.to_datetime(fs.txn_start.str[:10])
    one = fs.sort_values('meter_end_gal').groupby(['bay', 'meter_start_gal'], as_index=False).agg(
        first=('local_date', 'min'), end=('meter_end_gal', 'max'))
    one['gal'] = one.end - one.meter_start_gal
    for m, nm in ((6, 'June'), (7, 'July'), (8, 'August'), (9, 'September')):
        sel = one[(one['first'].dt.month == m)]
        check('fill station %s' % nm, int(math.floor(sel.gal.sum() / 1000.0 + 0.5)) == fig['ask']['fill_kgal'][nm]
              and len(sel) == fig['ask']['fills'][nm], '%.3f kgal, %d fills' % (sel.gal.sum() / 1000.0, len(sel)))
    xl = pd.read_excel(os.path.join(TGT, 'corvane_bws_monthly_activity_2026.xlsx'), header=5)
    check('vendor report read', len(xl) == 30, '%d rows' % len(xl))
    rd = pd.read_csv(os.path.join(TGT, 'city_facility_meter_reads_2025-09_2026-10.csv'), dtype={'register': float})
    rd['d'] = pd.to_datetime(rd.read_date, format='%m/%d/%Y')
    rd = rd.sort_values(['facility_id', 'd', 'read_time']).groupby(['facility_id', 'd'], as_index=False).last()
    fl = pd.read_csv(os.path.join(TGT, 'city_facility_meters_2026-10-30.csv'))
    wo = pd.read_excel(os.path.join(TGT, 'meter_shop_completed_work_orders_2025-2026.xlsx'))
    wf = wo[wo.location_type == 'CITY FACILITY']
    unit = dict(zip(fl.meter_id, fl.register_unit))
    for _, w in wf.iterrows():
        unit.setdefault(w.old_meter_id, w.old_register_unit)
        unit.setdefault(w.new_meter_id, w.new_register_unit)
    adv = {}
    for fid, grp in rd.groupby('facility_id'):
        grp = grp.sort_values('d')
        prev = None
        for _, r in grp.iterrows():
            if prev is not None:
                f = CCF_GAL if unit[r.meter_id] == 'CCF' else 1.0
                if r.meter_id == prev.meter_id:
                    gal = (r.register - prev.register) * f
                else:
                    w = wf[(wf.location_id == fid) & (wf.new_meter_id == r.meter_id)].iloc[0]
                    gal = (w.old_final_read - prev.register) + (r.register - w.new_initial_read) * f
                adv.setdefault(fid, {})[(r.d.year, r.d.month)] = gal
            prev = r
    # meters at one service address: one whose every advance sits inside another's, leaving a steady remainder, is
    # on that meter's service, and its water is already on the other meter
    addr = dict(zip(fl.facility_id, fl.service_address))
    inside = set()
    for p_ in adv:
        for c_ in adv:
            if p_ == c_ or addr[p_] != addr[c_]:
                continue
            ks = sorted(set(adv[p_]) & set(adv[c_]))
            dd = np.array([adv[p_][k] - adv[c_][k] for k in ks])
            cc = np.array([adv[c_][k] for k in ks])
            if (dd >= 0).all() and dd.std() / dd.mean() < 0.5 and cc.std() / cc.mean() > 1.0:
                inside.add(c_)
    check('one meter found inside another', len(inside) == 1, ', '.join(sorted(inside)))
    fac = {m: 0.0 for m in (6, 7, 8, 9)}
    for fid, d in adv.items():
        if fid in inside:
            continue
        for (yy, mm), gal in d.items():
            if yy == 2026 and mm in fac:
                fac[mm] += gal
    for m, nm in ((6, 'June'), (7, 'July'), (8, 'August'), (9, 'September')):
        af = fac[m] / AF_GAL
        check('facilities %s' % nm, round(af + 1e-9, 1) == fig['ask']['facilities_af'][nm], '%.4f acre-feet' % af)
    for name in ('corvane_bws_monthly_activity_2026.xlsx', 'meter_shop_completed_work_orders_2025-2026.xlsx'):
        with zipfile.ZipFile(os.path.join(TGT, name)) as z:
            check('xlsx container %s' % name, 'xl/workbook.xml' in z.namelist())
    print('verify: %d FAIL' % len(FAILS))
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())
