"""task401: the golden solution, computed from the shipped bundle only (target/)."""
import datetime as dt, json, os
import numpy as np
import pandas as pd

D = dt.date
LABEL = {'Very satisfied': 5, 'Fairly satisfied': 4, 'Neither satisfied nor dissatisfied': 3,
         'Fairly dissatisfied': 2, 'Very dissatisfied': 1}
WEEK0 = D(2025, 9, 1)


def uk_offset(ts):
    """Hours to add to a UTC timestamp for UK local time."""
    y = ts.year
    def last_sun(m):
        x = pd.Timestamp(y, m + 1, 1) - pd.Timedelta(days=1)
        return x - pd.Timedelta(days=(x.weekday() + 1) % 7)
    start = last_sun(3) + pd.Timedelta(hours=1); end = last_sun(10) + pd.Timedelta(hours=1)
    return 1 if start <= ts < end else 0


def load(T):
    f = lambda n: os.path.join(T, n)
    s25 = pd.read_csv(f('six_month_survey_2025H1.csv'), dtype=str)
    s26 = pd.read_csv(f('survey_export_6m_2026-01-01_2026-06-30.csv'), dtype=str)
    quotes = pd.read_csv(f('quote_log_2024-05_2025-12.csv'), dtype=str)
    regs = pd.read_csv(f('supply_registrations_2024-05_2025-12.csv'), dtype=str)
    qty = pd.read_parquet(f('meter_point_annual_quantities.parquet'))
    rates = pd.read_excel(f('tariff_rates_2024-04_2026-06.xlsx'), sheet_name='Rates')
    loads = pd.read_json(f('phase1_migration_loads.jsonl'), lines=True, dtype={'legacy_account_ref': str, 'platform_account_no': str})
    legacy = pd.read_csv(f('legacy_accounts_extract_2026-10-31.csv'), dtype=str)
    flows = pd.read_csv(f('switching_flows_2026-05-01_2026-11-05.csv'), dtype=str)
    return dict(s25=s25, s26=s26, quotes=quotes, regs=regs, qty=qty, rates=rates, loads=loads, legacy=legacy, flows=flows)


def respondents(B):
    a = B['s25'].copy()
    a = a[a['Q1_OVERALL_SAT'].notna() & (a['Q1_OVERALL_SAT'] != '')]
    a['date'] = pd.to_datetime(a['RESP_DATE'], format='%d/%m/%Y').dt.date
    a['overall'] = a['Q1_OVERALL_SAT'].astype(int)
    a = a.sort_values(['date', 'RESP_ID']).drop_duplicates('ACCOUNT_NO', keep='first')
    a = pd.DataFrame({'period': 0, 'account': a['ACCOUNT_NO'], 'date': a['date'], 'overall': a['overall'],
                      'contacted': a['Q3_CONTACTED_3M'] == 'Y'})
    b = B['s26'].copy()
    b = b[b['overall_satisfaction'].notna() & (b['overall_satisfaction'] != '')]
    ts = pd.to_datetime(b['completed_at'].str.replace('Z', ''))
    b['local'] = [t + pd.Timedelta(hours=uk_offset(t)) for t in ts]
    b['date'] = [t.date() for t in b['local']]
    b['overall'] = b['overall_satisfaction'].map(LABEL)
    b = b.sort_values(['local', 'response_id']).drop_duplicates('account_number', keep='first')
    b = pd.DataFrame({'period': 1, 'account': b['account_number'], 'date': b['date'], 'overall': b['overall'],
                      'contacted': b['contacted_last_3_months'] == 'TRUE'})
    r = pd.concat([a, b], ignore_index=True)
    r = r[[(d >= D(2025 + p, 1, 1)) and (d <= D(2025 + p, 6, 30)) for d, p in zip(r['date'], r['period'])]]
    r['sat'] = r['overall'] >= 4
    return r.reset_index(drop=True)


def link(B, r):
    """Each respondent's accepted quote, its tariff rates, and the cost of the meter point quantities in force."""
    loads = B['loads']
    plat2legacy = dict(zip(loads['platform_account_no'], loads['legacy_account_ref']))
    regs = B['regs']
    live = regs[regs['event'] == 'Registration']
    wd = set(regs.loc[regs['event'] == 'Withdrawal', 'registration_ref'])
    live = live[~live['registration_ref'].isin(wd)]
    by_acct = {a: g for a, g in live.groupby('account_number')}
    q = B['quotes'].set_index('quote_ref')
    rates = B['rates'].copy()
    rates['effective_from'] = pd.to_datetime(rates['effective_from']).dt.date
    rates['effective_to'] = pd.to_datetime(rates['effective_to']).dt.date
    rx = {k: g.sort_values('effective_from') for k, g in rates.groupby(['tariff_code', 'region'])}
    qty = B['qty'].copy(); qty['effective_from'] = pd.to_datetime(qty['effective_from']).dt.date
    qx = {k: g.sort_values('effective_from') for k, g in qty.groupby('meter_point')}
    out = []
    for _, row in r.iterrows():
        acct = row['account']
        g = by_acct.get(acct)
        if g is None and acct in plat2legacy:
            g = by_acct.get(plat2legacy[acct])
        qref = g['quote_ref'].iloc[0]; qrow = q.loc[qref]
        qd = D.fromisoformat(qrow['quote_date'])
        tr = rx[(qrow['tariff_code'], qrow['region'])]
        if qrow['tariff_code'] == 'SVT':
            tr = tr[(tr['effective_from'] <= qd) & (tr['effective_to'] >= qd)]
        else:
            tr = tr[tr['effective_from'] <= qd]
        tr = tr.iloc[-1]
        kwh, latest, sixm = {}, {}, {}
        start = min(D.fromisoformat(s) for s in g['supply_start_date'])
        for _, mrow in g.iterrows():
            h0 = qx[mrow['meter_point']]; h = h0[h0['effective_from'] <= row['date']]
            kwh[mrow['fuel']] = float(h['annual_quantity_kwh'].iloc[-1])
            latest[mrow['fuel']] = float(h0['annual_quantity_kwh'].iloc[-1])
            h6 = h0[h0['effective_from'] <= start + dt.timedelta(days=182)]
            sixm[mrow['fuel']] = float(h6['annual_quantity_kwh'].iloc[-1])
        dual = 'Gas' in kwh
        cost = (kwh['Electricity'] * tr['elec_unit_p_per_kwh'] + 365 * tr['elec_standing_p_per_day'] +
                (kwh['Gas'] * tr['gas_unit_p_per_kwh'] + 365 * tr['gas_standing_p_per_day'] if dual else 0)) / 100
        quoted = float(qrow['projected_annual_cost_gbp'])
        cur = tr
        if qrow['tariff_code'] == 'SVT':
            c2 = rx[('SVT', qrow['region'])]; c2 = c2[(c2['effective_from'] <= row['date']) & (c2['effective_to'] >= row['date'])]
            cur = c2.iloc[-1]
        out.append(dict(quoted=quoted, cost=cost, x=np.log(cost / quoted), tariff=qrow['tariff_code'],
                        variable=qrow['tariff_code'] == 'SVT', channel=qrow['channel'], region=qrow['region'],
                        qe=float(qrow['annual_kwh_electricity']), qg=float(qrow['annual_kwh_gas']) if dual else 0.0,
                        dual=dual, e_in=kwh['Electricity'], g_in=kwh.get('Gas', 0.0), e_latest=latest['Electricity'],
                        g_latest=latest.get('Gas', 0.0), e_six=sixm['Electricity'], g_six=sixm.get('Gas', 0.0),
                        eu=tr['elec_unit_p_per_kwh'], esc=tr['elec_standing_p_per_day'], gu=tr['gas_unit_p_per_kwh'],
                        gsc=tr['gas_standing_p_per_day'], ceu=cur['elec_unit_p_per_kwh'], cesc=cur['elec_standing_p_per_day'],
                        cgu=cur['gas_unit_p_per_kwh'], cgsc=cur['gas_standing_p_per_day'], quote_ref=qref))
    return pd.concat([r, pd.DataFrame(out)], axis=1)


def logit(X, y, it=60):
    A = np.column_stack([np.ones(len(y)), X]); b = np.zeros(A.shape[1])
    for _ in range(it):
        p = 1 / (1 + np.exp(-A @ b)); W = p * (1 - p)
        b += np.linalg.solve(A.T @ (A * W[:, None]) + 1e-9 * np.eye(A.shape[1]), A.T @ (y - p))
    return b


def bridge(L):
    """The fall split on the kinked disconfirmation route, Shapley over every order of the four causes."""
    from itertools import permutations
    m0 = (L['period'] == 0).values; m1 = ~m0
    x = L['x'].values; over, under = np.maximum(x, 0), np.minimum(x, 0)
    price = (L['variable'].values & m1).astype(float); con = (L['contacted'].values & m1).astype(float)
    X = np.column_stack([over, under, price, con, m1.astype(float)]); y = L['sat'].values.astype(float)
    b = logit(X, y); A1 = np.column_stack([np.ones(m1.sum()), X[m1]])
    def rank_replace(F):
        f0 = np.sort(F[m0]); rk = np.argsort(np.argsort(F[m1])); qq = (rk + 0.5) / m1.sum()
        return f0[np.minimum((qq * m0.sum()).astype(int), m0.sum() - 1)]
    cf = {'quote': lambda M: (M.__setitem__((slice(None), 1), rank_replace(over)), M.__setitem__((slice(None), 2), rank_replace(under))),
          'tariff rise': lambda M: M.__setitem__((slice(None), 3), 0), 'contact centre': lambda M: M.__setitem__((slice(None), 4), 0),
          'platform and the rest': lambda M: M.__setitem__((slice(None), 5), 0)}
    P = lambda M: 100 * (1 / (1 + np.exp(-M @ b))).mean()
    acc = {k: [] for k in cf}
    for order in permutations(cf):
        M = A1.copy(); prev = P(M)
        for c in order:
            cf[c](M); cur = P(M); acc[c].append(cur - prev); prev = cur
    return {k: float(np.mean(v)) for k, v in acc.items()}


def ask_a(B):
    leg = B['legacy']; fl = B['flows']
    asof = D(2026, 11, 1)
    order = {'Loss notified': 0, 'Loss withdrawn': 1, 'Loss completed': 2, 'Erroneous transfer returned': 3}
    f2 = fl.copy(); f2['d'] = pd.to_datetime(f2['flow_date']).dt.date; f2['o'] = f2['flow'].map(order)
    f2 = f2[f2['d'] <= asof].sort_values(['meter_point', 'd', 'o'])
    latest = f2.drop_duplicates('meter_point', keep='last')
    lost = set(latest.loc[latest['flow'] == 'Loss completed', 'meter_point'])
    qty = B['qty'].copy(); qty['effective_from'] = pd.to_datetime(qty['effective_from']).dt.date
    qty = qty[qty['effective_from'] <= asof]
    # the meter's registers in force: every register on the meter point's latest date on or before 1 November
    qty = qty[qty['effective_from'] == qty.groupby('meter_point')['effective_from'].transform('max')]
    qmap = qty.groupby('meter_point')['annual_quantity_kwh'].sum().to_dict()
    # a meter point is supplied to the account that took it on last: a new occupier's account holds it from the move
    holder = {}
    for acct, mpan, mprn, st in zip(leg['account_number'], leg['mpan'], leg['mprn'], leg['supply_start_date']):
        for m in (mpan, mprn):
            if isinstance(m, str) and m and (m not in holder or st > holder[m][1]):
                holder[m] = (acct, st)
    acc = leg[leg['account_status'] != 'Closed'].drop_duplicates('account_number')
    counts, e_kwh, g_kwh = {}, 0.0, 0.0
    for _, a in acc.iterrows():
        mps = [('E', a['mpan'])] + ([('G', a['mprn'])] if isinstance(a['mprn'], str) and a['mprn'] else [])
        live = [(f, m) for f, m in mps if m not in lost and holder[m][0] == a['account_number']]
        if not live:
            continue
        counts[a['region']] = counts.get(a['region'], 0) + 1
        for f, m in live:
            if f == 'E':
                e_kwh += qmap[m]
            else:
                g_kwh += qmap[m]
    return counts, e_kwh / 1e6, g_kwh / 1e6


def ask_b(B):
    lo = B['loads'].copy()
    ts = pd.to_datetime(lo['completed_utc'].str.replace('Z', ''))
    lo['local'] = [t + pd.Timedelta(hours=uk_offset(t)) for t in ts]
    lo = lo.sort_values('local').reset_index(drop=True)
    # a reload from the exception queue names the failed load's platform number as its source: follow it back
    src_of = {}
    for p, s in zip(lo['platform_account_no'], lo['legacy_account_ref']):
        src_of[p] = s
    def root(s):
        seen = 0
        while s in src_of and seen < 10:
            s = src_of[s]; seen += 1
        return s
    lo['root'] = [root(s) for s in lo['legacy_account_ref']]
    last = lo.drop_duplicates('root', keep='last')
    # the plan: an account counts as moved if the new platform was billing it at the end of 2 November 2025. A loaded
    # account live again on the legacy platform by then (its legacy status set on or before that day) was not moved;
    # one the legacy platform took back later was.
    leg = B['legacy']
    back = set(leg.loc[leg['status_date'] <= '2025-11-02', 'account_number'])
    last = last[~last['root'].isin(back)]
    last = last[(last['local'] >= pd.Timestamp(2025, 9, 1)) & (last['local'] < pd.Timestamp(2025, 11, 3))]
    last['week'] = [(t.date() - WEEK0).days // 7 + 1 for t in last['local']]
    return {(int(w), f): int(n) for (w, f), n in last.groupby(['week', 'fuel_profile']).size().items()}


def sale_channel(B, sw):
    """The channel of the sale each switch was registered on: the latest quote of the named quote's prospect dated
    on or before the switch's registration."""
    q = B['quotes'].copy(); q['d'] = pd.to_datetime(q['quote_date']).dt.date
    pros = dict(zip(q['quote_ref'], q['prospect_ref']))
    byp = {p: list(zip(g['d'], g['quote_ref'], g['channel'])) for p, g in q.sort_values(['d', 'quote_ref']).groupby('prospect_ref')}
    out = []
    for qref, reg in zip(sw['quote_ref'], sw['reg']):
        cands = [c for c in byp[pros[qref]] if c[0] <= reg]
        out.append(cands[-1][2])
    return out


def ask_c(B):
    rg = B['regs']
    wd = set(rg.loc[rg['event'] == 'Withdrawal', 'registration_ref'])
    live = rg[(rg['event'] == 'Registration') & ~rg['registration_ref'].isin(wd)].copy()
    live['start'] = pd.to_datetime(live['supply_start_date']).dt.date
    live['reg'] = pd.to_datetime(live['event_date']).dt.date
    sw = live.groupby('quote_ref').agg(start=('start', 'min'), reg=('reg', 'min')).reset_index()
    sw = sw[(sw['start'] >= D(2025, 7, 1)) & (sw['start'] <= D(2025, 12, 31))]
    sw['channel'] = sale_channel(B, sw)
    sw['month'] = [d.month for d in sw['start']]
    return {(c, int(m)): int(n) for (c, m), n in sw.groupby(['channel', 'month']).size().items()}


def solve(T):
    B = load(T)
    r = respondents(B)
    L = link(B, r)
    s0 = 100 * L.loc[L['period'] == 0, 'sat'].mean(); s1 = 100 * L.loc[L['period'] == 1, 'sat'].mean()
    cov = L['x'] <= 0
    F = dict(share_h1_2025=s0, share_h1_2026=s1, fall=s0 - s1,
             covered_sat_2025=100 * L.loc[(L['period'] == 0) & cov, 'sat'].mean(),
             covered_sat_2026=100 * L.loc[(L['period'] == 1) & cov, 'sat'].mean(),
             short_share_2025=100 * (~cov[L['period'] == 0]).mean(), short_share_2026=100 * (~cov[L['period'] == 1]).mean(),
             short_sat_2025=100 * L.loc[(L['period'] == 0) & ~cov, 'sat'].mean(),
             short_sat_2026=100 * L.loc[(L['period'] == 1) & ~cov, 'sat'].mean(),
             n_2025=int((L['period'] == 0).sum()), n_2026=int((L['period'] == 1).sum()))
    F['bridge'] = bridge(L)
    a_counts, a_e, a_g = ask_a(B)
    F['ask_a'] = dict(counts=a_counts, elec_gwh=a_e, gas_gwh=a_g)
    F['ask_b'] = {'%d|%s' % k: v for k, v in ask_b(B).items()}
    F['ask_c'] = {'%s|%d' % k: v for k, v in ask_c(B).items()}
    return F, L


if __name__ == '__main__':
    import sys
    F, L = solve(sys.argv[1])
    print(json.dumps({k: v for k, v in F.items() if not k.startswith('ask')}, indent=1, default=float))
    print('ask_a', F['ask_a']['elec_gwh'], F['ask_a']['gas_gwh'], sorted(F['ask_a']['counts'].items())[:3])
    print('ask_b', sorted(F['ask_b'].items())[:4]); print('ask_c', sorted(F['ask_c'].items())[:4])
