"""task401 independent verifier. Reads only the bundle (target/) and, to compare, generator/figures.json; shares no code
with the generator. Every format the pack ships is read back here, and every document that carries a filed sentence is
read through one extractor with a positive control on the same code path.
    python3 verify.py <target dir> <figures.json>          exit 1 on any failure
"""
import csv, json, math, re, sys, zipfile
from collections import defaultdict
from datetime import date, datetime, timedelta

OUT = []


def check(label, cond, detail=''):
    OUT.append((label, bool(cond))); print('%s  %-66s %s' % ('PASS' if cond else 'FAIL', label, detail))


def table(T, name):
    with open('%s/%s' % (T, name), newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def text_of(path):
    """The one extractor for documents: PDF text through pypdf, DOCX paragraphs from the package XML; whitespace folded."""
    if path.endswith('.pdf'):
        from pypdf import PdfReader
        raw = ' '.join(p.extract_text() or '' for p in PdfReader(path).pages)
    elif path.endswith('.docx'):
        xml = zipfile.ZipFile(path).read('word/document.xml').decode('utf-8')
        paras = re.findall(r'<w:p[ >].*?</w:p>', xml, re.S)
        raw = ' '.join(''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', p)) for p in paras)
        raw = raw.replace('&amp;', '&').replace('&#39;', "'").replace('&apos;', "'")
    else:
        raise ValueError(path)
    return re.sub(r'\s+', ' ', raw).replace('’', "'")


def uk_local(t):
    def last_sunday(m):
        d = date(t.year, m + 1, 1) - timedelta(days=1)
        return d - timedelta(days=(d.weekday() + 1) % 7)
    on = datetime.combine(last_sunday(3), datetime.min.time()) + timedelta(hours=1)
    off = datetime.combine(last_sunday(10), datetime.min.time()) + timedelta(hours=1)
    return t + timedelta(hours=1) if on <= t < off else t


SCALE = {'Very satisfied': 5, 'Fairly satisfied': 4, 'Neither satisfied nor dissatisfied': 3, 'Fairly dissatisfied': 2,
         'Very dissatisfied': 1}


def respondents(T):
    out = {}
    a = [r for r in table(T, 'six_month_survey_2025H1.csv') if r['Q1_OVERALL_SAT']]
    a.sort(key=lambda r: (datetime.strptime(r['RESP_DATE'], '%d/%m/%Y'), int(r['RESP_ID'])))
    for r in a:
        d = datetime.strptime(r['RESP_DATE'], '%d/%m/%Y').date()
        if r['ACCOUNT_NO'] not in out and date(2025, 1, 1) <= d <= date(2025, 6, 30):
            out[r['ACCOUNT_NO']] = dict(p=0, d=d, o=int(r['Q1_OVERALL_SAT']), c=r['Q3_CONTACTED_3M'] == 'Y')
    b = [r for r in table(T, 'survey_export_6m_2026-01-01_2026-06-30.csv') if r['overall_satisfaction']]
    for r in b:
        r['_l'] = uk_local(datetime.strptime(r['completed_at'], '%Y-%m-%dT%H:%M:%SZ'))
    b.sort(key=lambda r: (r['_l'], r['response_id']))
    for r in b:
        d = r['_l'].date()
        if r['account_number'] not in out and date(2026, 1, 1) <= d <= date(2026, 6, 30):
            out[r['account_number']] = dict(p=1, d=d, o=SCALE[r['overall_satisfaction']], c=r['contacted_last_3_months'] == 'TRUE')
    return out


def quantities(T):
    import pyarrow.parquet as pq
    t = pq.read_table(T + '/meter_point_annual_quantities.parquet').to_pydict()
    by = defaultdict(list)
    for mp, reg, q, d in zip(t['meter_point'], t['register'], t['annual_quantity_kwh'], t['effective_from']):
        by[mp].append((d, reg, q))
    return by


def in_force(rows, day):
    """The meter's quantity on a day: every register on its latest revision date on or before the day, summed."""
    ds = [d for d, _, _ in rows if d <= day]
    if not ds:
        return None
    last = max(ds)
    return sum(q for d, _, q in rows if d == last)


def rates_table(T):
    import openpyxl
    ws = openpyxl.load_workbook(T + '/tariff_rates_2024-04_2026-06.xlsx', read_only=True)['Rates']
    it = ws.iter_rows(values_only=True); head = next(it)
    out = defaultdict(list)
    for row in it:
        r = dict(zip(head, row))
        f, to = r['effective_from'], r['effective_to']
        r['f'] = f.date() if hasattr(f, 'date') else f; r['t'] = to.date() if hasattr(to, 'date') else to
        out[(r['tariff_code'], r['region'])].append(r)
    return out


def rate_on(rt, code, region, day):
    rows = sorted(rt[(code, region)], key=lambda r: r['f'])
    if code == 'SVT':
        return [r for r in rows if r['f'] <= day <= r['t']][-1]
    return [r for r in rows if r['f'] <= day][-1]


def live_registrations(T):
    rg = table(T, 'supply_registrations_2024-05_2025-12.csv')
    gone = {r['registration_ref'] for r in rg if r['event'] == 'Withdrawal'}
    return [r for r in rg if r['event'] == 'Registration' and r['registration_ref'] not in gone]


def logit_fit(X, y, it=12):
    k = len(X[0]) + 1; b = [0.0] * k
    for _ in range(it):
        g = [0.0] * k; H = [[0.0] * k for _ in range(k)]
        for xi, yi in zip(X, y):
            v = [1.0] + xi; z = sum(bb * vv for bb, vv in zip(b, v)); p = 1 / (1 + math.exp(-z)); w = p * (1 - p)
            for i in range(k):
                g[i] += (yi - p) * v[i]
                for j in range(k):
                    H[i][j] += w * v[i] * v[j]
        # solve H d = g (Gauss-Jordan)
        A = [H[i][:] + [g[i]] for i in range(k)]
        for c in range(k):
            piv = max(range(c, k), key=lambda r: abs(A[r][c])); A[c], A[piv] = A[piv], A[c]
            for r in range(k):
                if r != c:
                    f = A[r][c] / A[c][c]
                    A[r] = [a - f * cc for a, cc in zip(A[r], A[c])]
        b = [bb + A[i][k] / A[i][i] for i, bb in enumerate(b)]
    return b


def main_call(T):
    R = respondents(T)
    loads = [json.loads(l) for l in open(T + '/phase1_migration_loads.jsonl', encoding='utf-8')]
    to_legacy = {r['platform_account_no']: r['legacy_account_ref'] for r in loads}
    regs = defaultdict(list)
    for r in live_registrations(T):
        regs[r['account_number']].append(r)
    quotes = {r['quote_ref']: r for r in table(T, 'quote_log_2024-05_2025-12.csv')}
    rt = rates_table(T); Q = quantities(T)
    rows = []
    for acct, v in R.items():
        g = regs.get(acct) or regs.get(to_legacy.get(acct, ''))
        qr = quotes[g[0]['quote_ref']]; qd = date.fromisoformat(qr['quote_date'])
        r = rate_on(rt, qr['tariff_code'], qr['region'], qd)
        kwh = {x['fuel']: in_force(Q[x['meter_point']], v['d']) for x in g}
        cost = (kwh['Electricity'] * r['elec_unit_p_per_kwh'] + 365 * r['elec_standing_p_per_day'] +
                ((kwh['Gas'] * r['gas_unit_p_per_kwh'] + 365 * r['gas_standing_p_per_day']) if 'Gas' in kwh else 0)) / 100
        rows.append(dict(p=v['p'], sat=v['o'] >= 4, x=math.log(cost / float(qr['projected_annual_cost_gbp'])),
                         var=qr['tariff_code'] == 'SVT', c=v['c']))
    share = lambda f: 100 * sum(r['sat'] for r in rows if f(r)) / sum(1 for r in rows if f(r))
    s0, s1 = share(lambda r: r['p'] == 0), share(lambda r: r['p'] == 1)
    cov0, cov1 = share(lambda r: r['p'] == 0 and r['x'] <= 0), share(lambda r: r['p'] == 1 and r['x'] <= 0)
    X = [[max(r['x'], 0), min(r['x'], 0), float(r['var'] and r['p']), float(r['c'] and r['p']), float(r['p'])] for r in rows]
    b = logit_fit(X, [float(r['sat']) for r in rows])
    pred = lambda M: 100 * sum(1 / (1 + math.exp(-(b[0] + sum(bb * mm for bb, mm in zip(b[1:], m))))) for m in M) / len(M)
    X1 = [x for x, r in zip(X, rows) if r['p'] == 1]
    g0 = sorted(r['x'] for r in rows if r['p'] == 0); n0 = len(g0)
    order = sorted(range(len(X1)), key=lambda i: X1[i][0] + X1[i][1])
    M = [m[:] for m in X1]
    for rank, i in enumerate(order):
        x0 = g0[min(int((rank + 0.5) / len(X1) * n0), n0 - 1)]
        M[i][0], M[i][1] = max(x0, 0), min(x0, 0)
    quote_part = pred(M) - pred(X1)
    return dict(s0=s0, s1=s1, fall=s0 - s1, cov0=cov0, cov1=cov1, quote_part=quote_part, n=len(rows))


def ask_a(T):
    leg = table(T, 'legacy_accounts_extract_2026-10-31.csv'); fl = table(T, 'switching_flows_2026-05-01_2026-11-05.csv')
    asof = date(2026, 11, 1)
    # the plan: a meter point we lose is no longer ours from the loss's effective date; a transfer returned to us takes
    # effect on its own effective date; a withdrawn loss never took effect
    took = defaultdict(list)
    for f in fl:
        if f['flow'] in ('Loss completed', 'Erroneous transfer returned') and date.fromisoformat(f['effective_date']) <= asof:
            took[f['meter_point']].append((date.fromisoformat(f['effective_date']), f['flow']))
    state = {m: max(v)[1] for m, v in took.items()}
    holder = {}
    for a in leg:
        for m in (a['mpan'], a['mprn']):
            if m and (m not in holder or a['supply_start_date'] > holder[m][1]):
                holder[m] = (a['account_number'], a['supply_start_date'])
    Q = quantities(T)
    counts, e, g, seen = defaultdict(int), 0, 0, set()
    for a in leg:
        if a['account_status'] == 'Closed' or a['account_number'] in seen:
            continue
        seen.add(a['account_number'])
        mine = [(f, m) for f, m in (('E', a['mpan']), ('G', a['mprn'])) if m and state.get(m) != 'Loss completed'
                and holder[m][0] == a['account_number']]
        if mine:
            counts[a['region']] += 1
            for f, m in mine:
                q = in_force(Q[m], asof)
                e, g = (e + q, g) if f == 'E' else (e, g + q)
    return dict(counts), e / 1e6, g / 1e6


def ask_b(T):
    loads = [json.loads(l) for l in open(T + '/phase1_migration_loads.jsonl', encoding='utf-8')]
    # the plan: moved means the new platform was billing the account at the end of 2 November 2025, so a loaded account
    # whose legacy record was live again on or before that day was not moved
    close = date(2025, 11, 2)
    on_legacy = {a['account_number'] for a in table(T, 'legacy_accounts_extract_2026-10-31.csv')
                 if date.fromisoformat(a['status_date']) <= close}
    src = {r['platform_account_no']: r['legacy_account_ref'] for r in loads}
    def first(k):
        for _ in range(50):
            if k not in src:
                return k
            k = src[k]
        return k
    last = {}
    for r in loads:
        t = uk_local(datetime.strptime(r['completed_utc'], '%Y-%m-%dT%H:%M:%SZ')); k = first(r['legacy_account_ref'])
        if k not in last or t > last[k][0]:
            last[k] = (t, r['fuel_profile'])
    out = defaultdict(int)
    for k, (t, fp) in last.items():
        w = (t.date() - date(2025, 9, 1)).days // 7 + 1
        if 1 <= w <= 9 and k not in on_legacy:
            out['%d|%s' % (w, fp)] += 1
    return dict(out)


def ask_c(T):
    quotes = table(T, 'quote_log_2024-05_2025-12.csv')
    by_q = {q['quote_ref']: q for q in quotes}
    by_p = defaultdict(list)
    for q in quotes:
        by_p[q['prospect_ref']].append(q)
    sw = {}
    for r in live_registrations(T):
        s = sw.setdefault(r['quote_ref'], [r['supply_start_date'], r['event_date']])
        s[0], s[1] = min(s[0], r['supply_start_date']), min(s[1], r['event_date'])
    out = defaultdict(int)
    for qref, (start, reg) in sw.items():
        if not ('2025-07-01' <= start <= '2025-12-31'):
            continue
        cands = sorted((q['quote_date'], q['quote_ref'], q['channel']) for q in by_p[by_q[qref]['prospect_ref']] if q['quote_date'] <= reg)
        out['%s|%d' % (cands[-1][2], int(start[5:7]))] += 1
    return dict(out)


def documents(T):
    fw = text_of(T + '/six_month_survey_measurement_framework_v2.1.pdf')
    co = text_of(T + '/billing_platform_phase1_closeout_report.pdf')
    pl = text_of(T + '/phase2_cutover_plan_v1.3.docx')
    check('PDF framework read: control sentence found', 'who answer 4 or 5 to the overall question' in fw, '%d chars' % len(fw))
    check('PDF framework files the windows and the one-per-account rule',
          'from 1 January to 30 June, or from 1 July to 31 December, UK time' in fw and 'the first answered response is the one that counts' in fw)
    check('PDF framework names no quote, consumption, expectation or driver model (control above)',
          not re.search(r'\b(quote|quoted|expect\w*|consumption|disconfirm\w*|driver)\b', fw, re.I))
    check('PDF close-out read: control sentence found', 'nine weekly load batches from 1 September to 2 November 2025' in co, '%d chars' % len(co))
    check('PDF close-out dates every change in the period',
          all(s in co for s in ('relaunched on 6 May 2025', 'rose on 1 October 2025', 'on 10 November 2025',
                                'New customers have been set up on the new platform from 1 September 2025')))
    check('PDF close-out files that prepayment stays on the legacy platform', 'Prepayment accounts remain on the legacy platform for phase 2' in co)
    check('DOCX plan read: control sentence found', 'Weekly figures in this plan and in its reports run Monday to Sunday, UK time.' in pl, '%d chars' % len(pl))
    check('DOCX plan files the scope, the day and the register sum',
          'that we still supply on 1 November 2026, on at least one of its meter points' in pl
          and 'in force on 1 November 2026, day and night together on a two-rate meter' in pl)
    check('DOCX plan files the phase 1 report', 'the accounts it moved to the new platform in each week, each account counted once, '
          'in the week its last load completed, with the fuels that load carried' in pl)
    check('DOCX plan files what counts as moved, at the close of phase 1',
          'An account counts as moved if the new platform was billing it at the end of 2 November 2025, when phase 1 closed.' in pl)
    check('DOCX plan files when a lost meter point stops being ours',
          'A meter point we lose to another supplier is no longer ours from the effective date of the loss.' in pl)
    import pyarrow.parquet as pq
    md = pq.read_metadata(T + '/meter_point_annual_quantities.parquet')
    check('parquet read back: columns and writer', md.schema.names == ['meter_point', 'fuel', 'register', 'annual_quantity_kwh', 'effective_from', 'source']
          and 'arrow' not in md.created_by.lower(), md.created_by)
    rt = rates_table(T)
    svt = sorted(rt[('SVT', 'London')], key=lambda r: r['f'])
    check('XLSX read back: the Standard Variable step on 1 October 2025', any(r['f'] == date(2025, 10, 1) for r in svt), '%d SVT rows in London' % len(svt))
    n = sum(1 for _ in open(T + '/phase1_migration_loads.jsonl', encoding='utf-8'))
    check('JSONL read back', n > 25000, '%d loads' % n)
    for f in ('direct_debit_changes_2024-07_2026-06.csv', 'smart_meter_installs_2025.csv'):
        check('CSV read back: %s' % f, len(table(T, f)) > 1000)


def main(T, F):
    documents(T)
    m = main_call(T)
    r1 = lambda v: round(v + 1e-12, 1)
    check('main call: share satisfied H1 2025', r1(m['s0']) == F['share_h1_2025'], '%.3f' % m['s0'])
    check('main call: share satisfied H1 2026', r1(m['s1']) == F['share_h1_2026'], '%.3f' % m['s1'])
    check('main call: the fall', r1(m['fall']) == F['fall_points'], '%.3f' % m['fall'])
    check('main call: covered customers H1 2025 and H1 2026', r1(m['cov0']) == F['covered_sat_2025'] and r1(m['cov1']) == F['covered_sat_2026'],
          '%.2f %.2f' % (m['cov0'], m['cov1']))
    check('main call: the quote carries more than half the fall', m['quote_part'] > 0.5 * m['fall'], '%.2f of %.2f' % (m['quote_part'], m['fall']))
    counts, e, g = ask_a(T)
    check('Ask A: accounts in each region', counts == F['ask_a']['counts'], '%d accounts' % sum(counts.values()))
    check('Ask A: electricity and gas GWh', round(e, 1) == F['ask_a']['elec_gwh'] and round(g, 1) == F['ask_a']['gas_gwh'], '%.4f %.4f' % (e, g))
    check('Ask B: accounts moved each week by fuels', ask_b(T) == F['ask_b'])
    check('Ask C: switches by channel and month', ask_c(T) == F['ask_c'])
    fails = [x for x in OUT if not x[1]]
    print('%d checks, %d failed' % (len(OUT), len(fails)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], json.load(open(sys.argv[2]))))
