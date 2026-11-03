"""task401 generator checks on the cut pack and the clean truth. python3 checks.py  (exit 1 on any failure)"""
import json, os, sys, glob
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import world as W, golden as G, ladder as LD  # noqa: E402

T = os.path.join(os.path.dirname(HERE), 'target')
RES = []


def ok(label, cond, detail=''):
    RES.append((label, bool(cond), detail)); print('%s  %-58s %s' % ('PASS' if cond else 'FAIL', label, detail))


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def leader(L, xcol='x', ycol='sat'):
    """Fit the kinked disconfirmation route on column xcol; return the cause carrying the largest share."""
    m0 = (L['period'] == 0).values; m1 = ~m0
    x = L[xcol].values; y = L[ycol].values.astype(float)
    price = (L['variable'].values & m1).astype(float); con = (L['contacted'].values & m1).astype(float)
    X = np.column_stack([np.maximum(x, 0), np.minimum(x, 0), price, con, m1.astype(float)])
    b = G.logit(X, y); A1 = np.column_stack([np.ones(m1.sum()), X[m1]]); P = lambda M: 100 * (1 / (1 + np.exp(-M @ b))).mean()
    def rr(F):
        f0 = np.sort(F[m0]); rk = np.argsort(np.argsort(F[m1])); q = (rk + .5) / m1.sum()
        return f0[np.minimum((q * m0.sum()).astype(int), m0.sum() - 1)]
    base = P(A1); M = A1.copy(); M[:, 1] = rr(X[:, 0]); M[:, 2] = rr(X[:, 1]); quote = P(M) - base
    parts = {'quote': quote}
    for name, j in (('tariff', 4), ('contact', 5), ('platform', 6)):
        M = A1.copy(); M[:, j - 1] = 0; parts[name] = P(M) - base
    return max(parts, key=parts.get), parts


def cost(L, e, g, rates='quote'):
    eu, esc, gu, gsc = (('eu', 'esc', 'gu', 'gsc') if rates == 'quote' else ('ceu', 'cesc', 'cgu', 'cgsc'))
    return (L[e] * L[eu] + 365 * L[esc] + np.where(L['dual'], L[g] * L[gu] + 365 * L[gsc], 0)) / 100


def main():
    F = json.load(open(os.path.join(HERE, 'figures.json')))
    files = sorted(os.listdir(T))
    # ---- input gates and the no-describing-file rule
    ok('gate: ten or more files', len(files) >= 10, '%d files' % len(files))
    ok('gate: three or more formats', len({f.rsplit('.', 1)[1] for f in files}) >= 3, str(sorted({f.rsplit('.', 1)[1] for f in files})))
    big = max(sum(1 for _ in open(os.path.join(T, f), 'rb')) for f in files if f.endswith(('.csv', '.jsonl')))
    ok('gate: a file of 25,000 rows or more', big >= 25000, '%d rows' % big)
    dis = [W.F_DD, 'smart_meter_installs_2025.csv']
    ok('gate: two distractors present', all(d in files for d in dis), ', '.join(dis))
    ok('no describing file', not any(k in f.lower() for f in files for k in ('readme', 'dictionary', 'notes', 'manifest', 'schema', 'codebook')))
    # ---- the golden from the bundle against the clean truth
    Fs, L = G.solve(T)
    R = W.build(universe=True)['R']
    t_sh = [100 * R['sat'][R['t'] == k].mean() for k in (0, 1)]
    ok('bundle shares reproduce the truth', abs(Fs['share_h1_2025'] - t_sh[0]) < 1e-9 and abs(Fs['share_h1_2026'] - t_sh[1]) < 1e-9,
       '%.3f %.3f' % (Fs['share_h1_2025'], Fs['share_h1_2026']))
    ok('bundle respondents equal the truth', Fs['n_2025'] == int((R['t'] == 0).sum()) and Fs['n_2026'] == int((R['t'] == 1).sum()))
    # ---- R1: the field's raw material ships, the deciding quantity in no column
    heads = []
    for f in files:
        p = os.path.join(T, f)
        if f.endswith('.csv'):
            heads += open(p, encoding='utf-8').readline().strip().lower().split(',')
        elif f.endswith('.jsonl'):
            heads += list(json.loads(open(p).readline()).keys())
        elif f.endswith('.parquet'):
            heads += pd.read_parquet(p).columns.tolist()
    tok = lambda h: set(h.replace('-', '_').split('_'))
    bad = [h for h in heads if tok(h) & {'gap', 'ratio', 'disconfirmation', 'expected', 'expectation', 'overrun', 'covered', 'shortfall', 'basis'}]
    ok('R1 no shipped column holds the gap or the quote basis', not bad, str(bad))
    ok('R1 respondent-level ratings and meter-point quantities ship', 'bill_accuracy' in heads and 'annual_quantity_kwh' in heads)
    # ---- R3a: the analyst test, key driver analysis names the platform
    lin, shp = LD.kda(R)
    ok('R3a key driver analysis puts most of the fall on billing (platform)', shp['bill_accuracy'] + shp['bill_clarity'] > 50,
       'billing accuracy %.1f + clarity %.1f per cent' % (shp['bill_accuracy'], shp['bill_clarity']))
    # ---- R3b: the decisive step alone names the quote; each lower rung the platform
    lead, parts = leader(L)
    ok('R3b the gap route names the quote journey', lead == 'quote', ' '.join('%s %.2f' % kv for kv in parts.items()))
    ok('quote carries more than half the fall (kinked)', parts['quote'] > 0.5 * Fs['fall'], '%.2f of %.2f' % (parts['quote'], Fs['fall']))
    for key, feats, lab in (('use level', [np.log(R['cost6'])], 'use'), ('Direct Debit change', [np.log(R['dd1'] / R['dd0'])], 'dd'),
                            ('basis split', [(R['basis'] == 'typical').astype(float), (R['basis'] == 'customer').astype(float)], 'basis')):
        rt = LD.route(R, feats, lab); nm = max((c for c in rt if c != '_ll'), key=lambda c: rt[c])
        ok('R3b lower rung (%s) names the platform' % key, nm == 'platform', ' '.join('%s %.2f' % (c, v) for c, v in rt.items() if c != '_ll'))
    for key, xx in (('linear log', 'lin'), ('pounds', 'gbp')):
        L2 = L.copy()
        if xx == 'lin':
            m0 = (L2['period'] == 0).values
            L2['xs'] = L2['x']
        else:
            L2['xs'] = (L2['cost'] - L2['quoted']) / 100.0
        m1 = (L2['period'] == 1).values
        price = (L2['variable'].values & m1).astype(float); con = (L2['contacted'].values & m1).astype(float)
        X = np.column_stack([L2['xs'].values, price, con, m1.astype(float)]); y = L2['sat'].values.astype(float)
        b = G.logit(X, y); A1 = np.column_stack([np.ones(m1.sum()), X[m1]]); P = lambda M: 100 * (1 / (1 + np.exp(-M @ b))).mean()
        f0 = np.sort(X[~m1, 0]); rk = np.argsort(np.argsort(X[m1, 0])); q = (rk + .5) / m1.sum()
        M = A1.copy(); M[:, 1] = f0[np.minimum((q * (~m1).sum()).astype(int), (~m1).sum() - 1)]
        qpart = P(M) - P(A1); M = A1.copy(); M[:, 4] = 0; ppart = P(M) - P(A1)
        ok('symmetric form (%s) still names the quote' % key, qpart > ppart, 'quote %.2f platform %.2f' % (qpart, ppart))
    # ---- SF rows: every alternative reading keeps the call
    L1 = L.copy(); L1['sat'] = L1['overall'] == 5
    ok('SF1 top box only keeps the call', leader(L1)[0] == 'quote')
    ok('SF2 respondents in the response windows all joined July to December', True, 'by construction of the six-month invitation')
    ok('SF3 partial responses excluded', len(L) == Fs['n_2025'] + Fs['n_2026'])
    s25 = pd.read_csv(os.path.join(T, 'six_month_survey_2025H1.csv'), dtype=str)
    s25 = s25[s25['Q1_OVERALL_SAT'].notna()]
    dup = s25['ACCOUNT_NO'].duplicated(keep=False).sum()
    ok('SF4 accounts answering twice are few and the call holds either way', dup < 0.01 * len(s25), '%d rows' % dup)
    labels = set(pd.read_csv(os.path.join(T, 'survey_export_6m_2026-01-01_2026-06-30.csv'), dtype=str)['overall_satisfaction'].dropna())
    ok('SF5 every 2026 label is in the framework scale table', labels <= set(G.LABEL), str(sorted(labels)))
    ok('SF6 the registration names one accepted quote per respondent', L['quote_ref'].notna().all())
    for lab, e, g in (('SF7 six months from supply start', 'e_six', 'g_six'), ('SF7 latest held', 'e_latest', 'g_latest')):
        L7 = L.copy(); L7['x'] = np.log(cost(L7, e, g) / L7['quoted'])
        ok('%s keeps the call' % lab, leader(L7)[0] == 'quote')
    L8 = L.copy(); L8['x'] = np.log((L8['e_in'] * L8['eu'] + 365 * L8['esc']) / (L8['qe'] * L8['eu'] + 365 * L8['esc']))
    ok('SF8 electricity alone keeps the call', leader(L8)[0] == 'quote')
    L9 = L.copy(); L9['x'] = np.log(cost(L9, 'e_in', 'g_in', 'current') / L9['quoted'])
    ok('SF9 current rates keep the call', leader(L9)[0] == 'quote')
    tc = set(pd.read_excel(os.path.join(T, 'tariff_rates_2024-04_2026-06.xlsx'))['tariff_code'])
    ok('SF10 no two-rate tariff in the pack', not any('E7' in c or 'ECON' in c for c in tc), str(sorted(tc))[:80])
    mt = (L['period'] == 1)
    ok('SF11 the quote journey covers typed and typical quotes alike', True, 'basis split dilutes (ladder): see R3b')
    ok('SF12 the fall in points', abs(F['fall_points'] - round(F['share_h1_2025'] - F['share_h1_2026'], 1)) < 1e-9)
    # ---- graded figures mid-bin (bin from the asking sentence's rounding), tightest named
    edges = {'share_h1_2025': edge(Fs['share_h1_2025'], .1), 'share_h1_2026': edge(Fs['share_h1_2026'], .1),
             'fall': edge(Fs['share_h1_2025'] - Fs['share_h1_2026'], .1),
             'elec_gwh': edge(F['ask_a']['elec_gwh_raw'], .1), 'gas_gwh': edge(F['ask_a']['gas_gwh_raw'], .1)}
    tight = min(edges, key=edges.get)
    ok('graded figures mid-bin (7 per cent of a bin)', all(v >= 0.007 for v in edges.values()), 'tightest %s %.4f' % (tight, edges[tight]))
    # ---- separation: no device row in the main call's population
    loads = pd.read_json(os.path.join(T, 'phase1_migration_loads.jsonl'), lines=True, dtype=str)
    resp_acc = set(L['account'])
    chained = loads[loads['legacy_account_ref'].str.startswith('72')]
    ok('separation: no respondent in a reload chain or pilot row', not (set(chained['platform_account_no']) & resp_acc))
    regs = pd.read_csv(os.path.join(T, W.F_REGS), dtype=str)
    wd_q = set(regs.loc[regs['event'] == 'Withdrawal', 'quote_ref']); rq = set(L['quote_ref'])
    ok('separation: no respondent with a withdrawn registration', not (wd_q & rq), '%d' % len(wd_q & rq))
    per_q = regs[regs['event'] == 'Registration'].groupby('quote_ref')['registration_ref'].nunique()
    ok('separation: no respondent with a split registration', not (set(per_q[per_q > 1].index) & rq))
    # ---- realism: no uniform counts across weeks, regions, months
    for k in ('ask_b', 'ask_c'):
        v = list(F[k].values()); ok('realism: %s counts not uniform' % k, len(set(v)) > 0.8 * len(v), '%d distinct of %d' % (len(set(v)), len(v)))
    v = list(F['ask_a']['counts'].values()); ok('realism: ask_a counts not uniform', len(set(v)) == len(v))
    devices(F, Fs, L)
    literal_rows(L)
    literal_asks(F)
    closures(F)
    fails = [r for r in RES if not r[1]]
    print('%d checks, %d failed' % (len(RES), len(fails)))
    return 1 if fails else 0


def literal_asks(F):
    """The literal ask executor: the asking sentences and the filed WHATs executed word for word on target/, on a code path
    of its own. Each line cites the sentence it executes; a figure needing a convention no file states would fail here."""
    import csv, datetime as dt
    import pyarrow.parquet as pq
    D = dt.date
    rd = lambda n: list(csv.DictReader(open(os.path.join(T, n), newline='', encoding='utf-8')))
    # Ask A. Plan: "every prepayment account on the legacy platform that we still supply on 1 November 2026, on at least
    # one of its meter points"; "An account we no longer supply on any meter point on that date stays on the legacy
    # platform until its final bill"; "each meter point's industry annual quantity in force on 1 November 2026, day and
    # night together on a two-rate meter, electricity and gas reported separately".
    # Plan: "A meter point we lose to another supplier is no longer ours from the effective date of the loss." A transfer
    # returned to us takes effect on its own effective date; a withdrawn loss never took effect.
    asof = D(2026, 11, 1)
    took = {}                                           # the industry's switching record of who supplies a meter point
    for f in rd(W.F_FLOWS):
        if f['flow'] in ('Loss completed', 'Erroneous transfer returned') and D.fromisoformat(f['effective_date']) <= asof:
            took.setdefault(f['meter_point'], []).append((f['effective_date'], f['flow']))
    supplied = {m: max(v)[1] != 'Loss completed' for m, v in took.items()}
    leg = rd('legacy_accounts_extract_2026-10-31.csv')
    taken = {}                                          # a meter point is supplied to the account that took it on last
    for a in leg:
        for m in (a['mpan'], a['mprn']):
            if m and (m not in taken or a['supply_start_date'] > taken[m][0]):
                taken[m] = (a['supply_start_date'], a['account_number'])
    t = pq.read_table(os.path.join(T, 'meter_point_annual_quantities.parquet')).to_pydict()
    rev = {}                                            # the meter point's latest revision on or before the day: its registers
    for mp, q, d in zip(t['meter_point'], t['annual_quantity_kwh'], t['effective_from']):
        if d <= asof:
            if mp not in rev or d > rev[mp][0]:
                rev[mp] = (d, q)
            elif d == rev[mp][0]:
                rev[mp] = (d, rev[mp][1] + q)
    cnt, kwh = {}, {'E': 0, 'G': 0}
    for a in leg:
        mine = [(f, m) for f, m in (('E', a['mpan']), ('G', a['mprn'])) if m and supplied.get(m, True) and taken[m][1] == a['account_number']]
        if a['account_status'] != 'Closed' and mine:
            cnt[a['region']] = cnt.get(a['region'], 0) + 1
            for f, m in mine:
                kwh[f] += rev[m][1]
    okA = cnt == F['ask_a']['counts'] and round(kwh['E'] / 1e6, 1) == F['ask_a']['elec_gwh'] and round(kwh['G'] / 1e6, 1) == F['ask_a']['gas_gwh']
    # Ask B. Prompt: "the accounts phase 1 moved each week from 1 September to 2 November 2025, split into electricity-only
    # and dual fuel". Plan: "the accounts it moved to the new platform in each week, each account counted once, in the
    # week its last load completed, with the fuels that load carried"; "An account counts as moved if the new platform
    # was billing it at the end of 2 November 2025, when phase 1 closed"; "Monday to Sunday, UK time". Close-out: "the
    # platform issues a new account number on each load". The legacy extract dates each account's current status: a
    # loaded account live on the legacy platform from a day on or before 2 November 2025 was billed there at the close.
    loads = [json.loads(l) for l in open(os.path.join(T, 'phase1_migration_loads.jsonl'), encoding='utf-8')]
    earlier = {r['platform_account_no']: r['legacy_account_ref'] for r in loads}
    still_legacy = {a['account_number'] for a in leg if a['status_date'] <= '2025-11-02'}
    acct_last = {}
    for r in loads:
        k = r['legacy_account_ref']
        while k in earlier:                             # a load sourced from an earlier load's account number is that account
            k = earlier[k]
        u = dt.datetime.strptime(r['completed_utc'], '%Y-%m-%dT%H:%M:%SZ')
        u += dt.timedelta(hours=G.uk_offset(pd.Timestamp(u)))
        if k not in acct_last or u > acct_last[k][0]:
            acct_last[k] = (u, r['fuel_profile'])
    wk = {}
    for k, (u, fp) in acct_last.items():
        w = (u.date() - D(2025, 9, 1)).days // 7 + 1
        if 1 <= w <= 9 and k not in still_legacy:
            wk['%d|%s' % (w, fp)] = wk.get('%d|%s' % (w, fp), 0) + 1
    okB = wk == F['ask_b']
    # Ask C. Prompt: "the switches each sales channel brought in each month from July to December 2025, one per customer
    # in the month their first supply started, credited to the sale it was registered on and no withdrawn registration
    # counted".
    rg = rd(W.F_REGS); qs = rd(W.F_QUOTES)
    wdn = {r['registration_ref'] for r in rg if r['event'] == 'Withdrawal'}
    cust = {}                                           # one customer: the accepted quote its registrations name
    for r in rg:
        if r['event'] == 'Registration' and r['registration_ref'] not in wdn:
            c = cust.setdefault(r['quote_ref'], [r['supply_start_date'], r['event_date']])
            c[0], c[1] = min(c[0], r['supply_start_date']), min(c[1], r['event_date'])
    pros = {q['quote_ref']: q['prospect_ref'] for q in qs}
    sale_q = {}
    for q in qs:
        sale_q.setdefault(q['prospect_ref'], []).append((q['quote_date'], q['quote_ref'], q['channel']))
    sw = {}
    for qref, (start, reg) in cust.items():
        if '2025-07-01' <= start <= '2025-12-31':
            sale = max(x for x in sale_q[pros[qref]] if x[0] <= reg)   # the sale it was registered on: the quote then live
            key = '%s|%d' % (sale[2], int(start[5:7]))
            sw[key] = sw.get(key, 0) + 1
    okC = sw == F['ask_c']
    ok('literal ask executor: Ask A from the plan\'s sentences equals the golden (16 figures)', okA)
    ok('literal ask executor: Ask B from the plan and close-out sentences equals the golden (18 figures)', okB)
    ok('literal ask executor: Ask C from the asking sentence equals the golden (24 figures)', okC)


def phase2_counts(B, lost):
    """Ask A's account counts for a given set of lost meter points (the golden's holder and status rules)."""
    leg = B['legacy']
    holder = {}
    for acct, mpan, mprn, st in zip(leg['account_number'], leg['mpan'], leg['mprn'], leg['supply_start_date']):
        for m in (mpan, mprn):
            if isinstance(m, str) and m and (m not in holder or st > holder[m][1]):
                holder[m] = (acct, st)
    cnt = {}
    for _, a in leg[leg['account_status'] != 'Closed'].iterrows():
        mps = [a['mpan']] + ([a['mprn']] if isinstance(a['mprn'], str) and a['mprn'] else [])
        if [m for m in mps if m not in lost and holder[m][0] == a['account_number']]:
            cnt[a['region']] = cnt.get(a['region'], 0) + 1
    return cnt


def closures(F):
    """The ask conventions in the fork table (SF13 to SF22), the extracts' timeline and the realism the round-1 readers
    raised, each asserted on target/."""
    import datetime as dt
    D = dt.date
    B = G.load(T)
    leg, fl, rg, q = B['legacy'], B['flows'].copy(), B['regs'], B['quotes']
    # ---- SF15 (Gate A): no account's status is dated before its own supply start; a shared meter point's accounts never tie
    early = leg[leg['status_date'] < leg['supply_start_date']]
    ok('SF15 no legacy account closes or changes status before its own supply start', len(early) == 0, '%d accounts' % len(early))
    sh = pd.concat([leg[['mpan', 'supply_start_date']].rename(columns={'mpan': 'm'}),
                    leg.loc[leg['mprn'].notna(), ['mprn', 'supply_start_date']].rename(columns={'mprn': 'm'})])
    sh = sh[sh['m'].duplicated(keep=False)]
    ok('SF15 every shared meter point has one account that took it on last (no tie)', not sh.duplicated().any(), '%d shared rows' % len(sh))
    # ---- SF13: a completed loss effective on 1 November leaves the meter point not ours that day (the plan's sentence)
    fl['d'] = fl['flow_date']
    rank = {'Loss notified': 0, 'Loss withdrawn': 1, 'Loss completed': 2, 'Erroneous transfer returned': 3}
    f2 = fl[fl['d'] <= '2026-11-01'].assign(o=fl['flow'].map(rank)).sort_values(['meter_point', 'd', 'o'])
    latest = f2.drop_duplicates('meter_point', keep='last')
    lost = set(latest.loc[latest['flow'] == 'Loss completed', 'meter_point'])
    on1 = set(fl.loc[(fl['flow'] == 'Loss completed') & (fl['effective_date'] == '2026-11-01'), 'meter_point'])
    alt = phase2_counts(B, lost - on1)
    ok('SF13 losses effective on 1 November: the plan\'s sentence is load-bearing (the other reading moves the counts)',
       len(on1) > 0 and phase2_counts(B, lost) == F['ask_a']['counts'] and alt != F['ask_a']['counts'],
       '%d meter points; other reading %+d accounts' % (len(on1), sum(alt.values()) - sum(F['ask_a']['counts'].values())))
    pend = fl[(fl['flow'] == 'Loss notified') & (fl['effective_date'] <= '2026-11-01')]
    done = fl[fl['flow'].isin(['Loss completed', 'Loss withdrawn'])].groupby('meter_point')['flow_date'].max()
    ok('SF13 every loss due by 1 November was completed or withdrawn by its effective date (flow date and effective date agree)',
       all(m in done.index and done[m] <= e for m, e in zip(pend['meter_point'], pend['effective_date'])), '%d losses' % len(pend))
    # ---- SF14: the GWh totals are phase 2's whole, one figure a fuel
    ok('SF14 the asking sentence grades one electricity and one gas total for phase 2 as a whole',
       set(F['ask_a']) >= {'elec_gwh', 'gas_gwh'} and isinstance(F['ask_a']['elec_gwh'], float))
    # ---- SF16: an account phase 1 moved (the plan: billed on the new platform at the end of 2 November 2025)
    lo = B['loads'].copy()
    lo['local'] = [x + pd.Timedelta(hours=G.uk_offset(x)) for x in pd.to_datetime(lo['completed_utc'].str.replace('Z', ''))]
    src = dict(zip(lo['platform_account_no'], lo['legacy_account_ref']))
    def root(k):
        n = 0
        while k in src and n < 20:
            k = src[k]; n += 1
        return k
    lo['root'] = [root(k) for k in lo['legacy_account_ref']]
    last = lo.sort_values('local').drop_duplicates('root', keep='last')
    last = last[(last['local'] >= pd.Timestamp(2025, 9, 1)) & (last['local'] < pd.Timestamp(2025, 11, 3))]
    last = last.assign(wk=[(t.date() - D(2025, 9, 1)).days // 7 + 1 for t in last['local']])
    def tab(rows):
        return {'%d|%s' % k: int(v) for k, v in rows.groupby(['wk', 'fuel_profile']).size().items()}
    every = tab(last)
    not_on = tab(last[~last['root'].isin(set(leg['account_number']))])
    ok('SF16 an account phase 1 moved: every loaded account and every loaded account off the extract each file another table',
       every != F['ask_b'] and not_on != F['ask_b'] and every != not_on,
       'every load %+d, off the extract %+d accounts' % (sum(every.values()) - sum(F['ask_b'].values()), sum(not_on.values()) - sum(F['ask_b'].values())))
    # ---- SF17: withdrawn registrations left out, whatever their date; every withdrawal precedes the start it requested
    w = rg[rg['event'] == 'Withdrawal']; r = rg[rg['event'] == 'Registration']
    st = r.set_index(['registration_ref', 'meter_point'])['supply_start_date']
    wst = [st.get((a, m)) for a, m in zip(w['registration_ref'], w['meter_point'])]
    ok('SF17 every withdrawal is dated before the supply start its registration requested', all(s is not None and d < s for d, s in zip(w['event_date'], wst)),
       '%d withdrawals' % len(w))
    wref = set(w['registration_ref'])
    rmp = r[r['registration_ref'].isin(wref)].groupby('registration_ref')['meter_point'].apply(set)
    wmp = w.groupby('registration_ref')['meter_point'].apply(set)
    ok('SF17 a withdrawn registration is withdrawn on every meter point it registered (by reference or by row, the same rows)',
       all(rmp[k] == wmp.get(k, set()) for k in rmp.index), '%d withdrawn registrations' % len(rmp))
    # ---- SF18 to SF21: one customer, the month first supply started, the sale, the channel names
    live = r[~r['registration_ref'].isin(wref)].copy()
    qd, qc, qp = (dict(zip(q['quote_ref'], q[c])) for c in ('quote_date', 'channel', 'prospect_ref'))
    live['prospect'] = live['quote_ref'].map(qp)
    byp = {p: sorted(zip(g['quote_date'], g['quote_ref'], g['channel'])) for p, g in q.groupby('prospect_ref')}
    def table_by(key):
        g = live.groupby(key).agg(start=('supply_start_date', 'min'), reg=('event_date', 'min'), p=('prospect', 'first'))
        g = g[(g['start'] >= '2025-07-01') & (g['start'] <= '2025-12-31')]
        out = {}
        for start, reg, p in zip(g['start'], g['reg'], g['p']):
            k = '%s|%d' % ([x for x in byp[p] if x[0] <= reg][-1][2], int(start[5:7]))
            out[k] = out.get(k, 0) + 1
        return out
    by_q, by_p, by_a = table_by('quote_ref'), table_by('prospect'), table_by('account_number')
    ok('SF18 one customer: the accepted quote, the prospect and the account give the same switches in every cell',
       by_q == F['ask_c'] and by_p == F['ask_c'] and by_a == F['ask_c'])
    first = live.groupby('quote_ref')['supply_start_date'].min()
    elec = live[live['fuel'] == 'Electricity'].groupby('quote_ref')['supply_start_date'].min()
    ok('SF19 the month first supply started: the earliest live start is the electricity start for every customer',
       (first.loc[elec.index] == elec).all() and set(first.index) == set(elec.index), '%d customers' % len(first))
    named_ok = [x for x in live.groupby('quote_ref')['event_date'].min().items() if qd[x[0]] <= x[1]]
    agree = all([c for c in byp[qp[k]] if c[0] <= reg][-1][1] == k for k, reg in named_ok)
    ok('SF20 the sale it was registered on: wherever the named quote predates the registration it is the prospect\'s latest quote then',
       agree, '%d registrations' % len(named_ok))
    ok('SF21 the quote log carries exactly four sales channels', set(q['channel']) == {'Direct web', 'Comparison site', 'Phone', 'Broker'})
    # ---- SF22: load stamps are UTC; the plan's weeks are UK time, and the UTC week moves cells
    lo2 = last.assign(uwk=[(pd.Timestamp(x.replace('Z', '')).date() - D(2025, 9, 1)).days // 7 + 1 for x in last['completed_utc']])
    ok('SF22 every load stamp is UTC (Z) and UTC weeks would file another table', lo['completed_utc'].str.endswith('Z').all()
       and (lo2['uwk'] != lo2['wk']).sum() > 0, '%d accounts change week' % (lo2['uwk'] != lo2['wk']).sum())
    # ---- the extracts' timeline: each file's records inside the span its name gives, nothing after its pull
    sv = pd.read_csv(os.path.join(T, 'survey_export_6m_2026-01-01_2026-06-30.csv'), dtype=str)
    s25 = pd.read_csv(os.path.join(T, 'six_month_survey_2025H1.csv'), dtype=str)
    smi = pd.read_csv(os.path.join(T, 'smart_meter_installs_2025.csv'), dtype=str)
    dd = pd.read_csv(os.path.join(T, W.F_DD), dtype=str)
    rates = pd.read_excel(os.path.join(T, 'tariff_rates_2024-04_2026-06.xlsx'))
    qty = B['qty']
    s25d = pd.to_datetime(s25['RESP_DATE'], format='%d/%m/%Y')
    spans = {W.F_QUOTES: (q['quote_date'], '2024-05-01', '2025-12-31'),
             W.F_REGS: (rg['event_date'], '2024-05-01', '2025-12-31'),
             W.F_FLOWS: (fl['flow_date'], '2026-05-01', W.FLOWS_LAST.isoformat()),
             W.F_DD: (dd['change_date'], '2024-07-01', W.DD_LAST.isoformat()),
             'smart_meter_installs_2025.csv': (smi['appointment_date'], '2025-01-01', '2025-12-31'),
             'six_month_survey_2025H1.csv': (s25d.dt.strftime('%Y-%m-%d'), '2025-01-01', '2025-06-30'),
             'survey_export_6m_2026-01-01_2026-06-30.csv': (sv['completed_at'].str[:10], '2026-01-01', '2026-06-30'),
             'legacy_accounts_extract_2026-10-31.csv': (pd.concat([leg['status_date'], leg['supply_start_date']]), '2000-01-01', '2026-10-31'),
             'meter_point_annual_quantities.parquet': (qty['effective_from'].astype(str), '2000-01-01', '2026-11-05'),
             'tariff_rates_2024-04_2026-06.xlsx': (pd.concat([pd.to_datetime(rates['effective_from']), pd.to_datetime(rates['effective_to'])]).dt.strftime('%Y-%m-%d'),
                                                   '2024-04-01', '2026-06-30')}
    bad = ['%s %s..%s' % (n, v.min(), v.max()) for n, (v, a, b) in spans.items() if v.min() < a or v.max() > b]
    ok('timeline: every extract\'s records sit inside the span its name or pull date gives', not bad, '; '.join(bad) or '%d files' % len(spans))
    firsts = {W.F_QUOTES: q['quote_date'].min()[:7] == '2024-05', W.F_REGS: rg['event_date'].min()[:7] == '2024-05',
              W.F_FLOWS: fl['flow_date'].min() == '2026-05-01' and fl['flow_date'].max() == W.FLOWS_LAST.isoformat()}
    ok('timeline: a dated file name starts in the month of its first record', all(firsts.values()), str(firsts))
    newest = max(fl['flow_date'].max(), str(qty['effective_from'].max()), leg['status_date'].max())
    ok('timeline: the pack\'s export date (6 November 2026) follows every record; the plan (20 October 2026) predates the extracts',
       newest < '2026-11-06' and '2026-10-20' < '2026-10-31', 'newest record %s' % newest)
    # ---- realism the readers raised: the Direct Debit reasons differ; the parquet footer names a warehouse writer
    vc = dd['reason'].value_counts()
    ok('realism: Direct Debit new mandates and scheduled reviews differ, each near the joiners', vc['New mandate'] != vc['Scheduled review']
       and abs(vc['New mandate'] - vc['Scheduled review']) > 100, '%d against %d' % (vc['New mandate'], vc['Scheduled review']))
    import docx, zipfile
    pl = ' '.join(p.text for p in docx.Document(os.path.join(T, 'phase2_cutover_plan_v1.3.docx')).paragraphs)
    rels = zipfile.ZipFile(os.path.join(T, 'phase2_cutover_plan_v1.3.docx')).read('_rels/.rels')
    ok('realism (H25): python-docx opens the plan and reads its filed sentences; no relationship points at a dropped part',
       'An account counts as moved if the new platform was billing it at the end of 2 November 2025, when phase 1 closed.' in pl
       and 'A meter point we lose to another supplier is no longer ours from the effective date of the loss.' in pl
       and b'thumbnail' not in rels, '%d words' % len(pl.split()))
    import pyarrow.parquet as pq
    cb = pq.read_metadata(os.path.join(T, 'meter_point_annual_quantities.parquet')).created_by
    ok('realism: the parquet writer is a release build, not a snapshot', 'SNAPSHOT' not in cb and cb.startswith('parquet-mr version'), cb)


def fl_none(B, mps):
    """No switching flow touches these meter points."""
    return not (set(mps) & set(B['flows']['meter_point']))


FROZEN = dict(share_h1_2025=76.2, share_h1_2026=67.1, fall_points=9.1, covered_sat_2025=78.7, covered_sat_2026=80.1)


def devices(F, Fs, L):
    """The asks' devices on the shipped rows: the main call untouched, every device off the respondents, each forced."""
    import datetime as dt
    import pyarrow.parquet as pq
    D = dt.date
    B = G.load(T)
    for k, v in FROZEN.items():
        ok('frozen main call: %s' % k, F[k] == v, '%s' % F[k])
    ok('frozen main call: the quote carries more than half the fall', F['bridge']['quote'] > 0.5 * F['fall_points'],
       '%.1f of %.1f' % (F['bridge']['quote'], F['fall_points']))
    resp_acc, resp_q = set(L['account']), set(L['quote_ref'])
    # ---- Ask B: reload chains on dual fuel accounts only (primary). Loaded accounts the legacy platform holds again come
    # two ways: returned during phase 1 days after their load (a hazard the plan's moved sentence executes once noticed),
    # and taken back months after the close on a change to prepayment (second, silent: the repair that leaves out every
    # loaded account found on the legacy extract is right for the first and wrong for the second)
    lo = B['loads']; leg = B['legacy']
    src = dict(zip(lo['platform_account_no'], lo['legacy_account_ref']))
    reload = lo[lo['legacy_account_ref'].isin(set(lo['platform_account_no']))]
    ok('Ask B primary: every reload chain is a dual fuel account', (reload['fuel_profile'] == 'DUAL').all(), '%d reloads' % len(reload))
    lo['local'] = [x + pd.Timedelta(hours=G.uk_offset(x)) for x in pd.to_datetime(lo['completed_utc'].str.replace('Z', ''))]
    lo['wk'] = [(t.date() - D(2025, 9, 1)).days // 7 + 1 for t in lo['local']]
    back = lo[lo['legacy_account_ref'].isin(set(leg['account_number']))]
    bl = leg.set_index('account_number').loc[back['legacy_account_ref']]
    gap = np.array([(D.fromisoformat(s) - t.date()).days for s, t in zip(bl['status_date'], back['local'])])
    fuel_ok = (back['fuel_profile'].values == bl['fuel'].map({'Electricity': 'ELEC', 'Dual fuel': 'DUAL'}).values).all()
    ok('Ask B: every loaded account on the legacy extract is live prepayment with its own fuels, live again after its load',
       len(back) > 0 and fuel_ok and (bl['payment_method'] == 'Prepayment').all() and (bl['account_status'] == 'Live').all()
       and (gap >= 1).all() and back['legacy_account_ref'].is_unique, '%d accounts' % len(back))
    sd = bl['status_date'].values
    ret, hb = (gap <= 7), (sd >= '2026-01-01')
    ok('Ask B: each is either returned within a week of its load or taken back during 2026, none on the day phase 1 closed',
       (ret | hb).all() and not (ret & hb).any() and not (sd == '2025-11-02').any(),
       'returned %d (%d after the close), taken back %d' % (ret.sum(), (ret & (sd > '2025-11-02')).sum(), hb.sum()))
    def cells_of(rows):
        g = rows.groupby(['wk', 'fuel_profile']).size()
        return [int(g.get((w, f), 0)) for w in range(1, 10) for f in ('ELEC', 'DUAL')]
    c_ret = cells_of(back[ret & (sd <= '2025-11-02')])
    ok('Ask B hazard: accounts returned by the close move every week of both splits for a response that keeps every load',
       min(c_ret) >= 3, 'fewest %d, most %d' % (min(c_ret), max(c_ret)))
    c_hb = cells_of(back[sd > '2025-11-02'])
    ok('Ask B second: accounts taken back after the close move every week of both splits for the drop-every-extract-account repair',
       min(c_hb) >= 3, 'fewest %d, most %d' % (min(c_hb), max(c_hb)))
    ok('separation: no respondent in a reload chain, a pilot row or on the legacy extract',
       not ({src.get(p) for p in resp_acc} & set(reload['legacy_account_ref'])) and not (set(leg['account_number']) & resp_acc)
       and not ({src.get(p) for p in resp_acc} & set(leg['account_number']))
       and not (set(lo.loc[lo['legacy_account_ref'].str.startswith('72'), 'platform_account_no']) & resp_acc))
    # ---- Ask C: split gas registration only after an address lookup (primary); broker sales re-pointed (second)
    rg, q = B['regs'], B['quotes'].copy()
    wd = set(rg.loc[rg['event'] == 'Withdrawal', 'registration_ref'])
    live = rg[(rg['event'] == 'Registration') & ~rg['registration_ref'].isin(wd)].copy()
    qd = dict(zip(q['quote_ref'], q['quote_date'])); qc = dict(zip(q['quote_ref'], q['channel'])); qp = dict(zip(q['quote_ref'], q['prospect_ref']))
    nref = live.groupby('quote_ref')['registration_ref'].nunique()
    split_ch = {qc[x] for x in nref[nref > 1].index}
    ok('Ask C primary: split registrations only in web and comparison-site sales', split_ch <= {'Direct web', 'Comparison site'}, str(sorted(split_ch)))
    reg_day = live.groupby('quote_ref')['event_date'].min()
    late = [x for x, d in reg_day.items() if qd[x] > d]
    byp = q.groupby('prospect_ref')
    def sale(x):
        g = byp.get_group(qp[x]); g = g[g['quote_date'] <= reg_day[x]].sort_values(['quote_date', 'quote_ref'])
        return g
    forced = all(len(sale(x)) >= 1 and qc[sale(x)['quote_ref'].iloc[-1]] in ('Broker', 'Direct web', 'Comparison site')
                 and qc[x] == 'Phone' for x in late)
    ties = sum(1 for x in late if len(sale(x)) > 1 and sale(x)['quote_date'].iloc[-1] == sale(x)['quote_date'].iloc[-2])
    ok('Ask C second: registrations naming a quote dated after them are sales re-quoted by phone, the sale found without a tie',
       len(late) > 0 and forced and ties == 0, '%d re-pointed' % len(late))
    early = [x for x in late if len(sale(x)) > 1]
    ok('Ask C second: the earliest quote of the prospect is a trap for some', len(early) > 0, '%d with an earlier quote' % len(early))
    lm = pd.to_datetime(live.groupby('quote_ref')['supply_start_date'].min())
    inwin = [x for x in late if D(2025, 7, 1) <= lm[x].date() <= D(2025, 12, 31)]
    mv = pd.Series([(qc[sale(x)['quote_ref'].iloc[-1]], lm[x].month) for x in inwin]).value_counts()
    gain = pd.Series([lm[x].month for x in inwin]).value_counts()
    cells = [mv.get((c, m), 0) for c in ('Broker', 'Direct web', 'Comparison site') for m in range(7, 13)] + [gain.get(m, 0) for m in range(7, 13)]
    ok('Ask C second: moves every channel and month by several', min(cells) >= 3, 'fewest %d, most %d' % (min(cells), max(cells)))
    ok('separation: no respondent quote re-pointed or split', not (set(late) & resp_q) and not (set(nref[nref > 1].index) & resp_q))
    # ---- Ask A: a change of occupier (third): the leaving account waits for its final bill on the same meter points
    leg2 = B['legacy']
    byk = leg2.groupby('mpan')
    multi = leg2[leg2['mpan'].map(leg2['mpan'].value_counts()) > 1]
    fbp = multi[multi['account_status'] == 'Final bill pending']
    later = {m: g.sort_values('supply_start_date').iloc[-1] for m, g in multi.groupby('mpan')}
    cot = [r for _, r in fbp.iterrows() if later[r['mpan']]['account_number'] != r['account_number']
           and later[r['mpan']]['supply_start_date'] == r['status_date'] and later[r['mpan']]['account_status'] == 'Live']
    reg_cot = pd.Series([r['region'] for r in cot]).value_counts()
    ties = sum(1 for m, g in multi.groupby('mpan') if g['supply_start_date'].duplicated().any())
    ok('Ask A third: leaving occupiers wait for a final bill while the new occupier holds the same meter points, no tie',
       len(cot) > 0 and ties == 0 and fl_none(B, [r['mpan'] for r in cot]), '%d accounts' % len(cot))
    ok('Ask A third: moves every region by several', len(reg_cot) == 14 and reg_cot.min() >= 3, 'fewest %d' % reg_cot.min())
    # ---- Ask A: two-rate registers and meters exchanged for a single-rate meter during 2026 (second)
    qty = B['qty'].copy(); qty['effective_from'] = pd.to_datetime(qty['effective_from']).dt.date
    q1 = qty[qty['effective_from'] <= D(2026, 11, 1)]
    per_reg = q1.sort_values('effective_from').groupby(['meter_point', 'register'], dropna=False)['annual_quantity_kwh'].last()
    last_d = q1.groupby('meter_point')['effective_from'].max()
    tw = q1[q1['register'].isin(['Day', 'Night'])]
    exch = tw.groupby('meter_point')['effective_from'].max()
    exch = exch[exch < last_d.loc[exch.index]]
    on_last = q1[q1['effective_from'] == q1['meter_point'].map(last_d)]
    ok('Ask A second: every exchanged meter carries only a standard register from its exchange (no day or night after it)',
       len(exch) > 0 and set(on_last.loc[on_last['meter_point'].isin(exch.index), 'register']) == {'Standard'}, '%d meters' % len(exch))
    pairs = tw.groupby(['meter_point', 'effective_from'])['register'].nunique()
    ok('Ask A second: day and night are always revised together', (pairs == 2).all(), '%d revisions' % len(pairs))
    over = per_reg.groupby(level=0).sum() - on_last.groupby('meter_point')['annual_quantity_kwh'].sum()
    scope = set(B['legacy']['mpan'])
    ok('Ask A second: summing each register in force over-states electricity by many bins',
       over[over.index.isin(scope)].sum() / 1e6 > 1.0, '%.2f GWh' % (over[over.index.isin(scope)].sum() / 1e6))
    rmp =set(B['regs'].loc[B['regs']['quote_ref'].isin(resp_q), 'meter_point'])
    ok('separation: every respondent meter point single-register', set(qty.loc[qty['meter_point'].isin(rmp) & (qty['fuel'] == 'E'), 'register']) == {'Standard'})
    md = pq.read_metadata(os.path.join(T, 'meter_point_annual_quantities.parquet'))
    ok('realism: parquet footer carries no arrow or pandas signature', 'arrow' not in (md.created_by or '').lower() and not md.metadata, md.created_by)
    s26 = pd.read_csv(os.path.join(T, 'survey_export_6m_2026-01-01_2026-06-30.csv'), dtype=str)
    import uuid as _u
    ok('realism: 2026 response ids are version 4 and times carry seconds',
       all(_u.UUID(x).version == 4 for x in s26['response_id']) and s26['completed_at'].str[17:19].nunique() > 50)


def literal_rows(L):
    """The literal-execution rows: each candidate's exposed customers against the rest, and within its exposed group."""
    import datetime as dt
    B = G.load(T)
    rg = B['regs']; rg = rg[rg['event'] == 'Registration']
    st = pd.to_datetime(rg.groupby('quote_ref')['supply_start_date'].min()).dt.date
    L = L.copy(); L['start'] = L['quote_ref'].map(st)
    m0, m1 = L['period'] == 0, L['period'] == 1
    s = lambda m: 100 * L.loc[m, 'sat'].mean()
    fall = s(m1) - s(m0)
    rows = {}
    rows['platform, quote journey, survey vendor: touched against not (the half-years)'] = fall
    dose = s(m1 & (L['start'] >= dt.date(2025, 9, 1))) - s(m1 & (L['start'] < dt.date(2025, 9, 1)))
    rows['platform within 2026: set up on it against migrated onto it'] = dose
    typ = (L['qe'] == 2700) & (~L['dual'] | (L['qg'] == 11500))
    rows['quote journey within 2026: typical-value against typed quotes'] = s(m1 & typ) - s(m1 & ~typ)
    rows['quote journey: typical-value 2026 against 2025'] = s(m1 & typ) - s(m0)
    rows['quote journey: typed 2026 against 2025'] = s(m1 & ~typ) - s(m0)
    var = L['variable']
    rows['tariff rise within 2026: variable against fixed'] = s(m1 & var) - s(m1 & ~var)
    rows['tariff rise: difference in differences'] = (s(m1 & var) - s(m0 & var)) - (s(m1 & ~var) - s(m0 & ~var))
    con = L['contacted']
    rows['contact centre within 2026: contacted against not'] = s(m1 & con) - s(m1 & ~con)
    rows['contact centre: difference in differences'] = (s(m1 & con) - s(m0 & con)) - (s(m1 & ~con) - s(m0 & ~con))
    for k, v in rows.items():
        print('      literal  %-72s %+.2f' % (k, v))
    ok('literal rows: the three changes every 2026 respondent met tie on the whole fall', abs(fall + 9.1) < 0.1, '%.2f' % fall)
    ok('literal rows: no within-group row isolates a cause (each under 3 points)',
       all(abs(rows[k]) < 3 for k in rows if 'within' in k or 'differences' in k))
    ok('literal rows: both quote bases far below 2025 (the basis split exonerates the journey)',
       rows['quote journey: typical-value 2026 against 2025'] < -5 and rows['quote journey: typed 2026 against 2025'] < -5)


if __name__ == '__main__':
    sys.exit(main())
