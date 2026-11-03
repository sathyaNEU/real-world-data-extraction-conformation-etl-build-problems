"""task401: cut the data files of the pack from world.py's truth (documents are docs.py's)."""
import csv, datetime as dt, json, os
import numpy as np
import pandas as pd
import pyarrow as pa, pyarrow.parquet as pq
import world as W

D = dt.date
UK = 'Europe/London'
LABELS = {5: 'Very satisfied', 4: 'Fairly satisfied', 3: 'Neither satisfied nor dissatisfied',
          2: 'Fairly dissatisfied', 1: 'Very dissatisfied'}


def bst(d):
    """UK clock offset in hours on date d (last Sunday of March to last Sunday of October)."""
    def last_sun(y, m):
        x = D(y, m + 1, 1) - dt.timedelta(days=1)
        return x - dt.timedelta(days=(x.weekday() + 1) % 7)
    return 1 if last_sun(d.year, 3) <= d < last_sun(d.year, 10) else 0


class Ids:
    def __init__(self, rng):
        self.rng, self.used = rng, set()

    def draw(self, f):
        while True:
            v = f()
            if v not in self.used:
                self.used.add(v); return v

    def legacy(self):
        return self.draw(lambda: '4%07d' % self.rng.integers(0, 10 ** 7))

    def platform(self):
        return self.draw(lambda: '72%08d' % self.rng.integers(0, 10 ** 8))

    def mpan(self, dno):
        return self.draw(lambda: W.mpan_core(dno, self.rng))

    def mprn(self):
        return self.draw(lambda: '%d' % self.rng.integers(10 ** 9, 10 ** 10 - 1))

    def quote(self):
        a = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
        return self.draw(lambda: 'Q' + ''.join(a[k] for k in self.rng.integers(0, len(a), 9)))


def universe(seed=W.SEED):
    U = W.build(seed=seed, universe=True)
    rng = np.random.default_rng(seed + 77)
    ids = Ids(rng)
    J, R, table = U['J'], U['R'], U['table']
    n = len(J['t'])
    # accounts, meter points and quote references for every joiner
    J['quote_ref'] = np.array([ids.quote() for _ in range(n)])
    J['mpan'] = np.array([ids.mpan(W.REGIONS[r][1]) for r in J['region']])
    J['mprn'] = np.array([ids.mprn() if d else '' for d in J['dual']])
    J['legacy'] = np.array(['' for _ in range(n)], dtype=object)
    J['platform'] = np.array(['' for _ in range(n)], dtype=object)
    onboard_platform = np.array([s >= W.PHASE1_START for s in J['start']])
    for i in range(n):
        if onboard_platform[i]:
            J['platform'][i] = ids.platform()
        else:
            J['legacy'][i] = ids.legacy()
    U['onboard_platform'] = onboard_platform
    U['ids'], U['rng2'] = ids, rng
    return U


def write_csv(path, header, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(header); w.writerows(rows)


def cut(out, seed=W.SEED):
    os.makedirs(out, exist_ok=True)
    U = universe(seed)
    J, table, rng, ids = U['J'], U['table'], U['rng2'], U['ids']
    n = len(J['t'])
    facts = {}
    # ---------- phase 1: every credit account live on 1 September 2025 (joiners before September and an older book)
    jidx = [i for i in range(n) if not U['onboard_platform'][i]]
    stays = rng.random(len(jidx)) < np.where(J['t'][jidx] == 0, 0.91, 1.0)   # some 2024 joiners left before September
    p1 = [dict(legacy=J['legacy'][i], dual=bool(J['dual'][i]), region=int(J['region'][i]), joiner=i)
          for i, s in zip(jidx, stays) if s or J['resp'][i]]
    for _ in range(84630):
        r = int(rng.choice(len(W.REGIONS), p=np.array([w for _, _, w in W.REGIONS]) / 1.0))
        # the 2024 platform pilot's accounts carry their pilot platform number as the source reference
        src = ids.platform() if rng.random() < 0.016 else ids.legacy()
        p1.append(dict(legacy=src, dual=bool(rng.random() < 0.71), region=r, joiner=None))
    order = rng.permutation(len(p1))
    p1 = [p1[k] for k in order]
    weeks = [W.PHASE1_START + dt.timedelta(days=7 * k) for k in range(9)]
    wshare = np.array([.06, .09, .12, .13, .12, .13, .12, .12, .11]); wshare /= wshare.sum()
    wk = rng.choice(9, len(p1), p=wshare)
    loads, final_platform = [], {}
    lid = 0
    for a, w in zip(p1, wk):
        day = weeks[w] + dt.timedelta(days=int(rng.integers(0, 7)))
        hh = int(rng.choice([22, 23, 0, 1, 2, 3, 4], p=[.12, .2, .22, .18, .14, .09, .05]))
        local = dt.datetime.combine(day, dt.time(hh, int(rng.integers(0, 60)), int(rng.integers(0, 60))))
        if hh < 12:
            local += dt.timedelta(days=1)            # an overnight run finishes after midnight
        utc = local - dt.timedelta(hours=bst(local.date()))
        plat = U['J']['platform'][a['joiner']] if (a['joiner'] is not None and U['J']['platform'][a['joiner']]) else ids.platform()
        lid += 1
        loads.append(dict(load_id='L%06d' % lid, legacy=a['legacy'], platform=plat, utc=utc, dual=a['dual'],
                          batch='P1-W%02d' % (w + 1)))
        final = (plat, utc)
        if a['joiner'] is None and rng.random() < 0.034:   # validation failure: reloaded from the platform's exception queue
            rerun_local = local + dt.timedelta(days=int(rng.integers(3, 17)), minutes=int(rng.integers(-90, 90)))
            rerun_utc = rerun_local - dt.timedelta(hours=bst(rerun_local.date()))
            plat2 = ids.platform(); lid += 1
            rb = 'P1-W%02d' % (1 + (rerun_local.date() - W.PHASE1_START).days // 7)
            loads.append(dict(load_id='L%06d' % lid, legacy=plat, platform=plat2, utc=rerun_utc,
                              dual=a['dual'], batch=rb, root=a['legacy']))
            final = (plat2, rerun_utc)
        final_platform[a['legacy']] = final
        if a['joiner'] is not None:
            U['J']['platform'][a['joiner']] = final[0] if not U['J']['platform'][a['joiner']] else U['J']['platform'][a['joiner']]
    # a joiner's platform number is the final load's number
    for a in p1:
        if a['joiner'] is not None:
            U['J']['platform'][a['joiner']] = final_platform[a['legacy']][0]
    loads.sort(key=lambda r: (r['utc'], r['load_id']))
    base_id = 208113
    for k, r in enumerate(loads):                     # the platform numbers its loads as they complete
        r['load_id'] = 'L%07d' % (base_id + k * 3 + int(rng.integers(0, 3)))
    with open(os.path.join(out, 'phase1_migration_loads.jsonl'), 'w', encoding='utf-8') as f:
        for r in loads:
            f.write(json.dumps({'load_id': r['load_id'], 'batch': r['batch'], 'legacy_account_ref': r['legacy'],
                                'platform_account_no': r['platform'], 'fuel_profile': 'DUAL' if r['dual'] else 'ELEC',
                                'completed_utc': r['utc'].strftime('%Y-%m-%dT%H:%M:%SZ')}, separators=(',', ':')) + '\n')
    U['loads'] = loads; U['final_platform'] = final_platform
    # ---------- quotes and registrations (every joiner; re-quotes; withdrawn and re-registered switches)
    qrows, rrows = [], []
    reg_no = [0]
    def reg_ref():
        reg_no[0] += 1; return 'R%08d' % (31700000 + reg_no[0] * 7 + int(rng.integers(0, 7)))
    def acct_at(i, day):
        return J['platform'][i] if (not J['legacy'][i] or day >= W.PHASE1_START) else J['legacy'][i]
    def fuel_name(d):
        return 'Dual fuel' if d else 'Electricity'
    def quote_row(qref, day, ch, region, tariff, fuel_dual, ekwh, gkwh, cost, prospect):
        qrows.append([qref, day.isoformat(), W.CHANNELS[ch], W.REGIONS[region][0], tariff, fuel_name(fuel_dual),
                      int(ekwh), int(gkwh) if fuel_dual else '', '%.2f' % cost, prospect])
    prospect = np.array(['P%07d' % (1200000 + k * 3 + int(rng.integers(0, 3))) for k in range(n)])
    J['prospect'] = prospect
    rereg = np.zeros(n, bool)
    for i in range(n):
        quote_row(J['quote_ref'][i], J['qdate'][i], J['channel'][i], J['region'][i], J['tariff'][i], J['dual'][i],
                  J['qe'][i], J['qg'][i], J['quoted'][i], prospect[i])
        if rng.random() < 0.17:                       # an earlier quote through another channel, not taken up
            ch2 = int(rng.choice([c for c in range(4) if c != J['channel'][i]]))
            d2 = J['qdate'][i] - dt.timedelta(days=int(rng.integers(2, 25)))
            r2 = W.rates_for(table, J['tariff'][i] if J['tariff'][i] == 'SVT' else 'SVT', int(J['region'][i]), d2)
            quote_row(ids.quote(), d2, ch2, J['region'][i], 'SVT', J['dual'][i], J['qe'][i], J['qg'][i],
                      W.cost_gbp(J['qe'][i], J['qg'][i], J['dual'][i], r2), prospect[i])
        rd = J['qdate'][i] + dt.timedelta(days=int(rng.integers(1, 4)))
        if (not J['resp'][i]) and rng.random() < 0.024:   # registered, withdrawn in the cooling-off period, registered again
            rereg[i] = True
            first_start = J['start'][i] - dt.timedelta(days=int(rng.integers(18, 40)))
            first_reg = first_start - dt.timedelta(days=int(rng.integers(16, 22)))
            ref0 = reg_ref()
            for fuel, mp in (('Electricity', J['mpan'][i]), ('Gas', J['mprn'][i])):
                if fuel == 'Gas' and not J['dual'][i]:
                    continue
                acct = acct_at(i, first_reg)
                rrows.append([ref0, acct, mp, fuel, J['quote_ref'][i], 'Registration', first_reg.isoformat(), first_start.isoformat()])
                rrows.append([ref0, acct, mp, fuel, J['quote_ref'][i], 'Withdrawal',
                              (first_reg + dt.timedelta(days=int(rng.integers(2, 13)))).isoformat(), ''])
        ref = reg_ref()
        gas_lag = int(rng.choice([0, 0, 0, 1, 2, 3, 5])) if J['dual'][i] else 0
        # a gas registration rejected for a meter point mismatch is raised again under its own reference
        split = bool(J['dual'][i] and not J['resp'][i] and rng.random() < 0.065)
        if split:
            gas_lag = int(rng.integers(3, 13))
        for fuel, mp, st in (('Electricity', J['mpan'][i], J['start'][i]), ('Gas', J['mprn'][i], J['start'][i] + dt.timedelta(days=gas_lag))):
            if fuel == 'Gas' and not J['dual'][i]:
                continue
            if fuel == 'Gas' and split:
                rd2 = rd + dt.timedelta(days=int(rng.integers(2, 10)))
                if rd < W.PHASE1_START <= rd2:
                    rd2 = W.PHASE1_START - dt.timedelta(days=1)
                rrows.append([reg_ref(), acct_at(i, rd2), mp, fuel, J['quote_ref'][i], 'Registration', rd2.isoformat(), st.isoformat()])
                continue
            rrows.append([ref, acct_at(i, rd), mp, fuel, J['quote_ref'][i], 'Registration', rd.isoformat(), st.isoformat()])
    U['rereg'] = rereg
    # withdrawn switches that never started (not joiners): July to December of each year
    for t in (0, 1):
        y = 2024 + t
        for _ in range(int(0.041 * W.N_JOIN[t])):
            region = int(rng.choice(len(W.REGIONS), p=np.array([w for _, _, w in W.REGIONS])))
            dual = bool(rng.random() < 0.74); ch = int(rng.choice(4, p=W.CH_P[t]))
            st = D(y, 7, 1) + dt.timedelta(days=int(rng.integers(0, 184)))
            qd = st - dt.timedelta(days=int(rng.integers(16, 31)))
            e, g = round(float(rng.lognormal(np.log(2700), .5))), round(float(rng.lognormal(np.log(11000), .45)))
            r = W.rates_for(table, 'SVT', region, qd); q = ids.quote()
            quote_row(q, qd, ch, region, 'SVT', dual, e, g, W.cost_gbp(e, g, dual, r), 'P%07d' % int(rng.integers(1100000, 1199999)))
            rdd = qd + dt.timedelta(days=int(rng.integers(1, 4))); ref = reg_ref()
            acct = ids.platform() if rdd >= W.PHASE1_START else ids.legacy()
            mpan = ids.mpan(W.REGIONS[region][1]); mprn = ids.mprn() if dual else ''
            for fuel, mp in (('Electricity', mpan), ('Gas', mprn)):
                if fuel == 'Gas' and not dual:
                    continue
                rrows.append([ref, acct, mp, fuel, q, 'Registration', rdd.isoformat(), st.isoformat()])
                # a registration can only be withdrawn before the supply it requested starts
                wdd = min(rdd + dt.timedelta(days=int(rng.integers(1, 14))), st - dt.timedelta(days=1))
                rrows.append([ref, acct, mp, fuel, q, 'Withdrawal', wdd.isoformat(), ''])
    qrows.sort(key=lambda r: (r[1], r[0])); rrows.sort(key=lambda r: (r[6], r[0], r[3], r[5]))
    write_csv(os.path.join(out, W.F_QUOTES),
              ['quote_ref', 'quote_date', 'channel', 'region', 'tariff_code', 'fuel', 'annual_kwh_electricity',
               'annual_kwh_gas', 'projected_annual_cost_gbp', 'prospect_ref'], qrows)
    write_csv(os.path.join(out, W.F_REGS),
              ['registration_ref', 'account_number', 'meter_point', 'fuel', 'quote_ref', 'event', 'event_date',
               'supply_start_date'], rrows)
    U['qrows'], U['rrows'] = qrows, rrows
    tracker(out, U, rng)
    quantities(out, U, rng, p1)
    U['p1'] = p1
    tariffs(out, U)
    distractors(out, U, rng, p1)
    phase2(out, U, rng, ids)
    import devices
    devices.apply(out, U)
    return U, facts


def tracker(out, U, rng):
    J = U['J']
    resp = np.where(J['resp'])[0]
    R = U['R']                                       # R is J[resp] in the same order
    rows25, rows26 = [], []
    hexd = '0123456789abcdef'
    for k, i in enumerate(resp):
        t = int(J['t'][i]); d = R['response'][k]
        ratings = [int(R[c][k]) for c in ('bill_accuracy', 'bill_clarity', 'value', 'contact_ease', 'resolution', 'app')]
        app_na = rng.random() < 0.09
        ltr = int(np.clip(round(7.6 + 2.2 * (R['overall'][k] - 3.6) + rng.normal(0, 1.2)), 0, 10))
        contacted = bool(R['contacted'][k])
        hh = int(rng.integers(8, 22)); mm = int(rng.integers(0, 60))
        reps = 2 if rng.random() < 0.004 else 1      # re-invited after a re-registration: answered twice
        for rep in range(reps):
            dd_ = d + dt.timedelta(days=rep * int(rng.integers(3, 12)))
            if dd_ > D(2025 + t, 6, 30):
                dd_ = d
            ov = int(R['overall'][k]) if rep == 0 else int(np.clip(R['overall'][k] + rng.integers(-1, 2), 1, 5))
            if t == 0:
                rows25.append([str(30418000 + 3 * len(rows25) + int(rng.integers(0, 3))), J['legacy'][i], '6M',
                               dd_.strftime('%d/%m/%Y'), ov] + ratings[:5] + ['' if app_na else ratings[5],
                               'Y' if contacted else 'N', ltr])
            else:
                local = dt.datetime.combine(dd_, dt.time(hh, mm))
                utc = local - dt.timedelta(hours=bst(dd_))
                rid = ''.join(hexd[c] for c in rng.integers(0, 16, 32))
                rid = '%s-%s-%s-%s-%s' % (rid[:8], rid[8:12], rid[12:16], rid[16:20], rid[20:])
                rows26.append([rid, J['platform'][i], utc.strftime('%Y-%m-%dT%H:%M:%SZ'), LABELS[ov]] + ratings[:5] +
                              ['N/A' if app_na else ratings[5], 'TRUE' if contacted else 'FALSE', ltr])
    # partial responses (overall question left unanswered) from customers who are not in the analysed set
    for t, rows in ((0, rows25), (1, rows26)):
        nonresp = np.where((~J['resp']) & (J['t'] == t))[0]
        for i in rng.choice(nonresp, int(0.031 * len(rows)), replace=False):
            d = J['start'][i] + dt.timedelta(days=int(rng.integers(182, 200)))
            d = min(d, D(2025 + t, 6, 30))
            if t == 0:
                rows.append([str(30418000 + 3 * len(rows) + 1), J['legacy'][i], '6M', d.strftime('%d/%m/%Y'), '',
                             '', '', '', '', '', '', '', ''])
            else:
                rid = ''.join(hexd[c] for c in rng.integers(0, 16, 32))
                rows.append(['%s-%s-%s-%s-%s' % (rid[:8], rid[8:12], rid[12:16], rid[16:20], rid[20:]), J['platform'][i],
                             dt.datetime.combine(d, dt.time(int(rng.integers(9, 21)), 5)).strftime('%Y-%m-%dT%H:%M:%SZ'),
                             '', '', '', '', '', '', '', '', ''])
    rows25.sort(key=lambda r: (r[3][6:] + r[3][3:5] + r[3][:2], r[0]))
    rows26.sort(key=lambda r: (r[2], r[0]))
    write_csv(os.path.join(out, 'six_month_survey_2025H1.csv'),
              ['RESP_ID', 'ACCOUNT_NO', 'WAVE', 'RESP_DATE', 'Q1_OVERALL_SAT', 'Q2A_BILL_ACCURACY', 'Q2B_BILL_CLARITY',
               'Q2C_VALUE_FOR_MONEY', 'Q2D_EASE_OF_CONTACT', 'Q2E_RESOLUTION', 'Q2F_APP', 'Q3_CONTACTED_3M', 'Q4_LTR'], rows25)
    write_csv(os.path.join(out, 'survey_export_6m_2026-01-01_2026-06-30.csv'),
              ['response_id', 'account_number', 'completed_at', 'overall_satisfaction', 'bill_accuracy', 'bill_clarity',
               'value_for_money', 'ease_of_contact', 'resolution', 'app_experience', 'contacted_last_3_months',
               'likelihood_to_recommend'], rows26)
    U['rows25'], U['rows26'] = rows25, rows26


def quantities(out, U, rng, p1):
    J = U['J']; rows = []
    pull = D(2026, 10, 15)
    for i in range(len(J['t'])):
        s = J['start'][i]
        for fuel, mp, reg, six in (('E', J['mpan'][i], J['e_reg'][i], J['e_six'][i]), ('G', J['mprn'][i], J['g_reg'][i], J['g_six'][i])):
            if fuel == 'G' and not J['dual'][i]:
                continue
            mid = reg * (six / reg) ** rng.uniform(0.3, 0.7)
            rows.append((mp, fuel, int(round(reg)), s, 'Registration'))
            rows.append((mp, fuel, int(round(mid)), s + dt.timedelta(days=int(rng.integers(70, 111))), 'Revision'))
            rows.append((mp, fuel, int(round(six)), s + dt.timedelta(days=int(rng.integers(140, 176))), 'Revision'))
            later = s + dt.timedelta(days=int(rng.integers(300, 421)))
            if later <= pull:
                rows.append((mp, fuel, int(round(six * rng.lognormal(0, 0.03))), later, 'Revision'))
    for a in p1:                                      # the older credit book: the quantity currently held
        if a['joiner'] is not None:
            continue
        a['mpan'] = U['ids'].mpan(W.REGIONS[a['region']][1]); a['mprn'] = U['ids'].mprn() if a['dual'] else ''
        rows.append((a['mpan'], 'E', int(round(rng.lognormal(np.log(2750), .5))), D(2026, 1, 1) + dt.timedelta(days=int(rng.integers(0, 280))), 'Revision'))
        if a['dual']:
            rows.append((a['mprn'], 'G', int(round(rng.lognormal(np.log(11200), .45))), D(2026, 1, 1) + dt.timedelta(days=int(rng.integers(0, 280))), 'Revision'))
    U['qty_rows'] = rows                              # phase 2 rows are appended by phase2()


def tariffs(out, U):
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'Rates'
    ws.append(['tariff_code', 'tariff_name', 'region', 'effective_from', 'effective_to', 'elec_unit_p_per_kwh',
               'elec_standing_p_per_day', 'gas_unit_p_per_kwh', 'gas_standing_p_per_day'])
    for c in ws[1]:
        c.font = Font(bold=True)
    for r in sorted(U['table'], key=lambda r: (r['code'] != 'SVT', r['code'], r['region'], r['start'])):
        ws.append([r['code'], r['name'], W.REGIONS[r['region']][0], r['start'], r['end'], r['e_unit'], r['e_sc'],
                   r['g_unit'], r['g_sc']])
    for row in ws.iter_rows(min_row=2, min_col=4, max_col=5):
        for c in row:
            c.number_format = 'dd/mm/yyyy'
    for col, w in zip('ABCDEFGHI', (13, 22, 24, 14, 14, 20, 23, 19, 22)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = 'A2'
    wb.save(os.path.join(out, 'tariff_rates_2024-04_2026-06.xlsx'))


def distractors(out, U, rng, p1):
    J, R, table = U['J'], U['R'], U['table']
    rows = []
    resp_ix = {i: k for k, i in enumerate(np.where(J['resp'])[0])}
    for i in range(len(J['t'])):
        n0 = len(rows)
        s = J['start'][i]
        def acct(day):
            return J['platform'][i] if (not J['legacy'][i] or day >= W.PHASE1_START) else J['legacy'][i]
        dd0 = round(J['cost_reg'][i] / 12)
        rows.append([acct(s), s.isoformat(), '%.2f' % dd0, '', 'New mandate'])
        rv = s + dt.timedelta(days=int(rng.integers(140, 165)))
        r = W.rates_for(table, J['tariff'][i], int(J['region'][i]), rv)
        dd1 = round(W.cost_gbp(round(J['e_six'][i]), round(J['g_six'][i]), J['dual'][i], r) / 12)
        cur = dd0
        if J['tariff'][i] == 'SVT' and s < D(2025, 10, 1) < rv:
            new = round(cur * 1.02); rows.append([acct(D(2025, 10, 1)), '2025-10-01', '%.2f' % new, '%.2f' % cur, 'Tariff change']); cur = new
        if rng.random() < 0.03:
            fd = s + dt.timedelta(days=int(rng.integers(35, 130)))
            rows.append([acct(fd), fd.isoformat(), '%.2f' % cur, '%.2f' % cur, 'Payment failed'])
        rows.append([acct(rv), rv.isoformat(), '%.2f' % dd1, '%.2f' % cur, 'Scheduled review']); cur = dd1
        if rng.random() < 0.025:
            cd = rv + dt.timedelta(days=int(rng.integers(5, 60)))
            new = round(cur * rng.uniform(0.85, 1.1)); rows.append([acct(cd), cd.isoformat(), '%.2f' % new, '%.2f' % cur, 'Customer request'])
        for r in rows[n0:]:
            r.append(i)                               # the joiner each row belongs to (never written)
    rows.sort(key=lambda r: (r[1], r[0], r[4]))
    U['dd_rows'] = rows                               # written by devices.debits()
    inst = []
    pool = [(J['platform'][i] or J['legacy'][i], J['mpan'][i]) for i in rng.choice(len(J['t']), 5200, replace=False)]
    pool += [(a['legacy'], a['mpan']) for a in [p1[k] for k in rng.choice(len(p1), 3900, replace=False)] if 'mpan' in a]
    for k, (acct_no, mp) in enumerate(pool):
        d = D(2025, 1, 6) + dt.timedelta(days=int(rng.integers(0, 357)))
        if d.weekday() == 6:
            d -= dt.timedelta(days=1)
        oc = rng.choice(['Installed', 'Installed', 'Installed', 'Installed', 'Installed', 'Installed', 'Aborted - no access',
                         'Aborted - customer cancelled on the day', 'Aborted - meter position unsafe'])
        inst.append(['SMI-%06d' % (510000 + 7 * k + int(rng.integers(0, 7))), acct_no, mp, d.isoformat(), 'SMETS2', oc])
    inst.sort(key=lambda r: (r[3], r[0]))
    write_csv(os.path.join(out, 'smart_meter_installs_2025.csv'),
              ['job_ref', 'account_number', 'mpan', 'appointment_date', 'meter_type', 'outcome'], inst)
    U['smi_accts'] = {r[1] for r in inst}


def phase2(out, U, rng, ids):
    """The legacy platform's prepayment book (phase 2's population) and the industry switching flows."""
    accts, flows, qty = [], [], U['qty_rows']
    fref = [0]
    def next_ref():
        fref[0] += 1; return 'SF%07d' % (4400000 + fref[0] * 5 + int(rng.integers(0, 5)))
    reg_w = np.array([w for _, _, w in W.REGIONS]); reg_w = reg_w / reg_w.sum()
    truth = []
    for k in range(33620):
        region = int(rng.choice(len(W.REGIONS), p=reg_w)); dual = bool(rng.random() < 0.63)
        acct = ids.legacy(); mpan = ids.mpan(W.REGIONS[region][1]); mprn = ids.mprn() if dual else ''
        start = D(2012, 1, 1) + dt.timedelta(days=int(rng.integers(0, 5000)))
        mps = [('E', mpan)] + ([('G', mprn)] if dual else [])
        state = {}
        for fuel, mp in mps:
            qe = int(round(rng.lognormal(np.log(2500 if fuel == 'E' else 10200), .48)))
            qty.append((mp, fuel, qe, D(2026, 1, 1) + dt.timedelta(days=int(rng.integers(0, 280))), 'Revision'))
            if rng.random() < 0.15:
                qty.append((mp, fuel, int(round(qe * rng.lognormal(0, .04))), D(2026, 11, 2) + dt.timedelta(days=int(rng.integers(0, 10)) % 4), 'Revision'))
            state[mp] = 'supplied'
        lost_any = False
        u = rng.random()
        if u < 0.072:                                 # a loss notified May to October 2026
            which = mps if (not dual or rng.random() < 0.8) else [mps[int(rng.integers(0, 2))]]
            nd = D(2026, 5, 1) + dt.timedelta(days=int(rng.integers(0, 183)))
            eff = nd + dt.timedelta(days=int(rng.integers(5, 16)))
            v = rng.random()
            for fuel, mp in which:
                r1 = next_ref()
                flows.append([r1, mp, fuel, 'Loss notified', nd.isoformat(), eff.isoformat()])
                if v < 0.18 and eff > nd + dt.timedelta(days=2):
                    wd = nd + dt.timedelta(days=int(rng.integers(1, (eff - nd).days)))
                    flows.append([next_ref(), mp, fuel, 'Loss withdrawn', wd.isoformat(), ''])
                elif eff <= W.PHASE2_ASOF:
                    flows.append([next_ref(), mp, fuel, 'Loss completed', eff.isoformat(), eff.isoformat()])
                    state[mp] = 'lost'
                    ret = eff + dt.timedelta(days=int(rng.integers(9, 46)))
                    if rng.random() < 0.11 and ret < W.PHASE2_ASOF:   # an erroneous transfer, returned to us
                        flows.append([next_ref(), mp, fuel, 'Erroneous transfer returned', ret.isoformat(), ret.isoformat()])
                        state[mp] = 'supplied'
            lost_any = True
            returned = any(f[3] == 'Erroneous transfer returned' and f[1] in state for f in flows[-6:])
            if v < 0.18:
                status = 'Final bill pending' if rng.random() < 0.6 else 'Live'
                sdate = nd
            elif returned:
                status, sdate = ('Final bill pending', nd) if rng.random() < 0.65 else ('Live', min(nd + dt.timedelta(days=35), D(2026, 10, 30)))
            elif eff > W.PHASE2_ASOF:
                status, sdate = 'Final bill pending', nd
            elif all(state[mp] == 'lost' for _, mp in mps) and (W.PHASE2_ASOF - eff).days > 40:
                status, sdate = 'Closed', eff + dt.timedelta(days=int(rng.integers(30, 41)))
            else:
                status, sdate = 'Final bill pending', nd
        elif u < 0.085:                               # closed on a change of occupier: a new account holds the supply
            status, sdate = 'Closed', D(2025, 6, 1) + dt.timedelta(days=int(rng.integers(0, 480)))
            if start >= sdate:                        # the leaving occupier's account began before it closed
                start = start - dt.timedelta(days=3 * 365)
            for mp in state:
                state[mp] = 'other_account'
            acct2 = ids.legacy()
            accts.append([acct2, W.REGIONS[region][0], 'Prepayment', 'Dual fuel' if dual else 'Electricity', 'Live',
                          sdate.isoformat(), mpan, mprn, sdate.isoformat()])
            truth.append((acct2, region, {mp: 'supplied' for _, mp in mps}, mps))
        else:
            status, sdate = 'Live', start
        accts.append([acct, W.REGIONS[region][0], 'Prepayment', 'Dual fuel' if dual else 'Electricity', status,
                      sdate.isoformat(), mpan, mprn, start.isoformat()])
        truth.append((acct, region, state, mps))
    accts.sort(key=lambda r: r[0]); flows.sort(key=lambda r: (r[4], r[0]))
    write_csv(os.path.join(out, 'legacy_accounts_extract_2026-10-31.csv'),
              ['account_number', 'region', 'payment_method', 'fuel', 'account_status', 'status_date', 'mpan', 'mprn',
               'supply_start_date'], accts)
    # the flows extract was pulled on 6 November 2026: it holds every flow dated up to the day before
    write_csv(os.path.join(out, W.F_FLOWS),
              ['flow_ref', 'meter_point', 'fuel', 'flow', 'flow_date', 'effective_date'],
              [f for f in flows if f[4] <= W.FLOWS_LAST.isoformat()])
    U['phase2_truth'], U['phase2_accts'], U['flows'] = truth, accts, flows
    qty.sort(key=lambda r: (r[0], r[3]))
    tbl = pa.table({'meter_point': [r[0] for r in qty], 'fuel': [r[1] for r in qty],
                    'annual_quantity_kwh': pa.array([r[2] for r in qty], pa.int32()),
                    'effective_from': pa.array([r[3] for r in qty], pa.date32()), 'source': [r[4] for r in qty]})
    pq.write_table(tbl, os.path.join(out, 'meter_point_annual_quantities.parquet'), compression='snappy')
    U['qty_rows'] = qty
