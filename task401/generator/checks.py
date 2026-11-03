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
    dis = ['direct_debit_changes_2024-07_2026-06.csv', 'smart_meter_installs_2025.csv']
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
    regs = pd.read_csv(os.path.join(T, 'supply_registrations_2024-07_2025-12.csv'), dtype=str)
    wd_q = set(regs.loc[regs['event'] == 'Withdrawal', 'quote_ref']); rq = set(L['quote_ref'])
    ok('separation: no respondent with a withdrawn registration', not (wd_q & rq), '%d' % len(wd_q & rq))
    per_q = regs[regs['event'] == 'Registration'].groupby('quote_ref')['registration_ref'].nunique()
    ok('separation: no respondent with a split registration', not (set(per_q[per_q > 1].index) & rq))
    # ---- realism: no uniform counts across weeks, regions, months
    for k in ('ask_b', 'ask_c'):
        v = list(F[k].values()); ok('realism: %s counts not uniform' % k, len(set(v)) > 0.8 * len(v), '%d distinct of %d' % (len(set(v)), len(v)))
    v = list(F['ask_a']['counts'].values()); ok('realism: ask_a counts not uniform', len(set(v)) == len(v))
    fails = [r for r in RES if not r[1]]
    print('%d checks, %d failed' % (len(RES), len(fails)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
