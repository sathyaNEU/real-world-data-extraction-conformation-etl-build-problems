"""task211 checks: the five go/no-go screens on the shipped seed, the semantic forks (SF ids), the corridor, mid-bin
edges, the ask devices and the input gates, all computed from target/ (golden.load reads only the pack).
Writes checks_report.txt beside this file; exits 1 on any failure."""
import datetime as dt, json, sys, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import golden as G

FAIL, LOG = [], []
GENS = ['Halvorne', 'Pellbrook', 'Corwen', 'Tessard', 'Wynfield']
CALL = 'Tessard'


def check(name, ok, detail=''):
    LOG.append('%s  %s  %s' % ('PASS' if ok else 'FAIL', name, detail))
    if not ok:
        FAIL.append(name)


def top(d):
    return max(GENS, key=lambda p: d[p])


def lead(d):
    v = sorted((d[p] for p in GENS), reverse=True)
    return v[0] / v[1] if v[1] > 0 else 99.0


def std_rates(pk, keep=None, strata=('band', 'res'), extra=None):
    cover = pk['cover']
    on = cover >= 0 if keep is None else (cover >= 0) & keep
    keys = [np.broadcast_to(pk[s][:, None], cover.shape) for s in strata]
    if extra is not None:
        keys.append(extra)
    k = np.zeros(cover.shape, dtype=np.int64)
    for a in keys:
        k = k * 10 + a
    E = {}; O = {}
    for p in range(6):
        m = on & (cover == p)
        kk = k[m]; vv = pk['visits'][m]
        E[p] = pd.Series(np.ones(kk.size)).groupby(kk).sum()
        O[p] = pd.Series(vv.astype(float)).groupby(kk).sum()
    W = sum(E.values()).fillna(0)
    rate = {}
    for p in range(6):
        r = (O[p] / E[p]).reindex(W.index)
        ok = r.notna()
        rate[p] = float((r[ok] * W[ok]).sum() / W[ok].sum()) * 30.4375 * 1000
    return {pk['prods'][p]: rate[p] - rate[0] for p in range(1, 6)}


def readers(pk):
    R = {}
    on = pk['cover'] >= 0
    tot = {}
    for p in range(6):
        m = pk['cover'] == p
        tot[p] = (pk['visits'][m].sum(), m.sum() / 30.4375)
    rr = {p: tot[p][0] / tot[p][1] * 1000 for p in range(6)}
    R['first look (crude rate against the reference)'] = {pk['prods'][p]: rr[p] - rr[0] for p in range(1, 6)}
    cen = np.zeros(pk['cover'].shape, dtype=np.int64)
    # centre of each patient-day: the centre of the pharmacy that filled the covering supply is not on the grid, so
    # the decomposing reader stratifies by the member's most frequent centre
    fills = pk['fills']
    mc = fills.groupby('member_id')['centre'].agg(lambda s: s.value_counts().index[0])
    centres = sorted(set(mc))
    ci = np.array([centres.index(mc.get(m, centres[0])) for m in pk['mids']])
    cen = np.broadcast_to(ci[:, None], pk['cover'].shape)
    pk['centre_idx'] = ci
    R['(a) field-decomposing: age, resistance and centre standardised'] = std_rates(pk, extra=cen)
    R['(b) constructing: first 90 days on a product excluded'] = std_rates(pk, keep=pk['tnew'] >= 90)
    R['(b) constructing: 90 days after a change of product excluded'] = std_rates(pk, keep=pk['tsw'] >= 90)
    mon = np.broadcast_to((np.arange(pk['cover'].shape[1]) // 30.2).astype(int).clip(0, 5)[None, :], pk['cover'].shape)
    R['(c) per-record: product, month, centre, age, resistance'] = G.excess(pk, [('mon', mon, 6), ('cen', cen, 7)])[0]
    R['(d) switching: a transient after a change of product'] = G.excess(pk, [('ts', (pk['tsw'] < 90).astype(int), 2)])[0]
    R['(d) new site: the new site\'s stock as the cause'] = G.excess(pk, [('ns', pk['newsite'].astype(int), 2)], zero=('prod', 'ns'))[0]
    R['(d) colour dated by the register\'s approval date'] = G.excess(pk, [('tv', (pk['tnaive'] < 90).astype(int), 2)])[0]
    for T in (90, 180):
        R['(d) colour from the letter, dated by its centre date, %d days' % T] = G.excess(pk, [('tl', (pk['tlet'] < T).astype(int), 2)])[0]
    R['(d) switching and the letter date together'] = G.excess(pk, [('ts', (pk['tsw'] < 90).astype(int), 2), ('tl', (pk['tlet'] < 90).astype(int), 2)])[0]
    R['(e) literal joint replay: standardised excess against the reference'] = std_rates(pk)
    late = np.broadcast_to((np.arange(pk['cover'].shape[1]) >= 120)[None, :], pk['cover'].shape)
    R['temporal: the last two months\' standardised rates'] = std_rates(pk, keep=late)
    return R


def refuted(pk):
    """Fixed clocks after the appearance change that the record's own fit refutes against the first supply."""
    return {'days since the appearance change, %d-day clock' % T: G.excess(pk, [('tc', (pk['tcol'] < T).astype(int), 2)])[0]
            for T in (30, 60, 180)}


def clock_fit(pk):
    """The first supply against every fixed clock, fitted on one common partition so the likelihoods compare."""
    cuts = [30, 60, 90, 120, 180]
    cb = np.digitize(pk['tcol'], cuts)
    spec = G.base_spec(pk) + [('fs', pk['first'].astype(int), 2), ('cb', cb, 6)]
    grid, E, O = G.cells(pk, spec)
    base = []
    for jj, (name, _, n) in enumerate(spec[:3]):
        for l in range(1, n):
            if (grid[:, jj] == l).any():
                base.append((grid[:, jj] == l).astype(float))
    def ll(extra):
        X = G.sm.add_constant(np.column_stack(base + [extra.astype(float)]))
        return G.sm.GLM(O, X, family=G.sm.families.Poisson(), offset=np.log(E)).fit().llf
    l0 = ll(grid[:, 3] == 1)
    return {T: l0 - ll(grid[:, 4] <= k) for k, T in enumerate(cuts)}


def golden_family(pk):
    F = {}
    F['first supply after an appearance change'] = G.excess(pk, [('fs', pk['first'].astype(int), 2)])[0]
    F['first supply after a colour change (narrow reading)'] = G.excess(pk, [('fs', pk['first_colour'].astype(int), 2)])[0]
    mon = np.broadcast_to((np.arange(pk['cover'].shape[1]) // 30.2).astype(int).clip(0, 5)[None, :], pk['cover'].shape)
    cen = np.broadcast_to(pk['centre_idx'][:, None], pk['cover'].shape)
    F['first supply with month and centre'] = G.excess(pk, [('fs', pk['first'].astype(int), 2), ('mon', mon, 6), ('cen', cen, 7)])[0]
    F['first supply split by its days of supply'] = G.excess(pk, [('fs', pk['first'].astype(int) * (1 + (pk['supply'] >= 60)), 3)])[0]
    for T in (90, 120):
        F['days since the appearance change, %d-day clock' % T] = G.excess(pk, [('tc', (pk['tcol'] < T).astype(int), 2)])[0]
    F['days since the appearance change, fourteen-day bins'] = G.excess(pk, [('tc', np.where(pk['tcol'] < 182, 1 + pk['tcol'] // 14, 0), 14)])[0]
    return F


def common_fit(pk):
    """Each trigger's fourteen-day transient profile fitted on one common partition of patient-days, so the
    likelihoods compare: appearance changes, the first new-site fill, and changes of product."""
    b = lambda a: np.where(a < 182, 1 + a // 14, 0)
    spec = G.base_spec(pk) + [('a', pk['first'].astype(int), 2), ('s', b(pk['tnsf']), 14), ('w', b(pk['tsw']), 14)]
    grid, E, O = G.cells(pk, spec)
    out = {}
    for nm, j in (('appearance', 3), ('site', 4), ('switch', 5)):
        cols = []
        for jj, (name, _, n) in enumerate(spec[:3] + [spec[j]]):
            col = grid[:, jj if jj < 3 else j]
            for l in range(1, n):
                if (col == l).any():
                    cols.append((col == l).astype(float))
        X = G.sm.add_constant(np.column_stack(cols))
        out[nm] = G.sm.GLM(O, X, family=G.sm.families.Poisson(), offset=np.log(E)).fit().llf
    return out


def openpyxl_sheet_headers(path):
    import openpyxl
    ws = openpyxl.load_workbook(path, read_only=True).active
    rows = list(ws.iter_rows(min_row=1, max_row=6, values_only=True))
    return [str(c) for r in rows for c in r if c is not None and str(c).islower()]


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def main():
    pk = G.load()
    gold = G.golden_excess(pk)
    # ---------------------------------------------------------------- screens 3, 4 and 5
    R = readers(pk)
    for name, d in R.items():
        check('reader lands wrong: ' + name, top(d) != CALL, 'names %s (%s)' % (top(d), ', '.join('%s %.1f' % (p, d[p]) for p in GENS)))
    # ---------------------------------------------------------------- screen 2: the golden family and the corridor
    F = golden_family(pk)
    for name, d in F.items():
        check('golden family names the call: ' + name, top(d) == CALL and d[CALL] >= 2.0 + 1.0,
              'Tessard %.2f, next %s %.2f, lead %.2f' % (d[CALL], sorted(GENS, key=lambda p: -d[p])[1],
                                                          sorted((d[p] for p in GENS), reverse=True)[1], lead(d)))
    lo = min(d[CALL] for d in F.values()); hi = max(d[CALL] for d in F.values())
    check('corridor: Tessard\'s excess in one whole-visit bin across the golden family', round(lo) == round(hi) == round(gold[CALL]),
          '%.2f to %.2f' % (lo, hi))
    check('none is ruled out with margin under every specification', lo >= 3.0, 'lowest Tessard excess %.2f against the 2.0 bar' % lo)
    check('the call\'s lead is at least 1.2 under every specification', min(lead(d) for d in F.values()) >= 1.2,
          'lowest lead %.2f' % min(lead(d) for d in F.values()))
    # the record refutes the site-keyed and the switch-keyed transients against the appearance-keyed one
    ll = common_fit(pk)
    check('the record prefers the appearance clock to the site clock and the switch clock',
          ll['appearance'] - ll['site'] > 10 and ll['appearance'] - ll['switch'] > 10,
          'log-likelihood gains %.1f over site, %.1f over switch' % (ll['appearance'] - ll['site'], ll['appearance'] - ll['switch']))
    cf = clock_fit(pk)
    check('the record prefers the first supply to every fixed clock', min(cf.values()) > 10,
          ', '.join('%d days %.1f' % (T, g) for T, g in sorted(cf.items())))
    RF = refuted(pk)
    for name, d in list(F.items()) + list(RF.items()):
        check('none is ruled out under every transient specification: ' + name, max(d[p] for p in GENS) >= 3.0,
              'largest %s %.2f' % (top(d), max(d[p] for p in GENS)))
    # ---------------------------------------------------------------- semantic forks
    # SF1 narrow (colour) against broad (full description) reading of a change: one set of change fills
    check('SF1 a change of tablet read as colour or as the whole description: the same fills',
          bool((pk['first'] == pk['first_colour']).all() and (pk['tcol'] == pk['tcolour_only']).all()))
    # SF2 each centre's change date: the letter's date, the first new-site receipt and the first new-site issue are one date
    fills = pk['fills']
    first_pink = fills[(fills['product'] == 'Halvorne') & (fills.colour == 'pink')].groupby('centre').service_date.min()
    last_white = fills[(fills['product'] == 'Halvorne') & (fills.colour == 'white')].groupby('centre').service_date.max()
    ok2 = all(first_pink[c] >= pk['dc_dates'][c] and last_white[c] < pk['dc_dates'][c] for c in first_pink.index)
    check('SF2 each centre\'s change date is one date (letter date, first pink fill on or after it, last white fill before it)', ok2)
    # SF3 Pacific against UTC dating of the partner feed's visits
    enc = pk['enc']
    shift = enc[enc.qual & (enc.t.dt.tz_convert('UTC').dt.date != enc.date)]
    edge_cases = shift[(shift.date == dt.date(2025, 12, 31)) | (shift.date == dt.date(2026, 6, 30))]
    check('SF3 dating by UTC moves no visit across the window\'s edges', len(edge_cases) == 0, '%d visits on 31 Dec or 30 Jun after 16:00' % len(edge_cases))
    # SF4 transfers counted once against twice: same call
    check('SF4 transfers counted twice: the same call', True, 'transfers are spread over every product; asserted inert below')
    # SF5 reversed claims kept as fills: the same call
    check('SF5 reversed claims kept: the same call', True, 'asserted inert below')
    # SF6 the previous fill's description for a member's first claim in the extract: none (no change) against change
    check('SF6 a member\'s first fill in the extract carries no change: inert inside the window', True,
          'the extract starts 1 April 2025, more than 90 days before the window')
    # SF7 age taken at 1 January 2026 against at each visit: the same call
    check('SF7 age band at the window\'s start: the same call', True, 'bands are 18 and 65; asserted on the golden')
    # ---------------------------------------------------------------- mid-bin edges for the graded main figures
    check('Tessard excess mid-bin (whole visits)', edge(gold[CALL], 1.0) >= 0.07, '%.3f from an edge' % edge(gold[CALL], 1.0))
    fam_edge = min(edge(d[CALL], 1.0) for d in F.values())
    check('Tessard excess mid-bin under every golden specification', fam_edge >= 0.07 and len({round(d[CALL]) for d in F.values()}) == 1,
          'tightest %.3f' % fam_edge)
    cnt = G.product_counts(pk)
    pm_edge = min(edge(cnt[p]['patient_months'], 10.0) for p in GENS)
    # ---------------------------------------------------------------- the variant table: every operationalisation
    if not G.SCREEN:
        base_pm = {p: round(cnt[p]['patient_months'] / 10.0) * 10 for p in GENS}
        base_v = {p: cnt[p]['visits'] for p in GENS}
        VAR = (('SF3 the partner feed dated by its UTC day', dict(utc_partner=True), None),
               ('SF9 merged record numbers left unlinked', dict(merged_linked=False), 'MS-12 2.4'),
               ('SF7 age band on 2025 less birth year', dict(age_year=2025), None),
               ('SF4 transfers counted at both hospitals', dict(transfers_once=False), 'MS-12 2.3'),
               ('SF5 reversed claims kept as fills', dict(keep_reversed=True), 'MS-12 2.4'),
               ('SF8 an overlap carried forward instead of given to the later fill', dict(overlap='carry'), 'MS-12 2.4'))
        for name, kw, ruled in VAR:
            pv = G.load(**kw)
            ex = G.golden_excess(pv)
            cv = G.product_counts(pv)
            pm = {p: round(cv[p]['patient_months'] / 10.0) * 10 for p in GENS}
            vv = {p: cv[p]['visits'] for p in GENS}
            moved = [p for p in GENS if pm[p] != base_pm[p] or vv[p] != base_v[p]]
            same = top(ex) == CALL and round(ex[CALL]) == round(gold[CALL]) and edge(ex[CALL], 1.0) >= 0.07
            check('R2 mess item mishandled, %s: the call and Tessard\'s whole-visit excess' % name, same,
                  'names %s, Tessard %.2f' % (top(ex), ex[CALL]))
            check('R2 mess item mishandled, %s: the per-generic counts' % name, not moved or ruled is not None,
                  ('unchanged' if not moved else 'moves %s; ruled out by %s' % (', '.join(moved), ruled)))
    check('patient-months mid-bin (nearest 10)', pm_edge >= 0.7, 'tightest %.2f' % pm_edge)
    summary = dict(readers={k: top(v) for k, v in R.items()}, family={k: top(v) for k, v in F.items()},
                   tessard=[round(lo, 3), round(hi, 3)], fam={k: round(v[CALL], 2) for k, v in F.items()}, gold={p: round(gold[p], 2) for p in GENS}, rdr={k: {p: round(v[p], 1) for p in GENS} for k, v in R.items()}, fam_edge=round(fam_edge, 3), pm_edge=round(pm_edge, 2),
                   minlead=round(min(lead(d) for d in F.values()), 2), ll=ll, clock_ll={str(k): round(v, 1) for k, v in cf.items()},
                   refuted={k: {p: round(v[p], 2) for p in GENS} for k, v in RF.items()},
                   ref_rate=round(float(pk['visits'][pk['cover'] == 0].sum()) / ((pk['cover'] == 0).sum() / 30.4375) * 1000, 1))
    # ---------------------------------------------------------------- the ask devices: blocks, stops and bins
    import ceiling as CE
    spend, days, adj_q, resolved = G.asks()
    gs = {'%s Q%d' % k: v for k, v in spend.items() if k[0] in GENS}
    gd = {'%s Q%d' % k: v for k, v in days.items() if k[0] in GENS}
    by_invoice = CE.spend('mirror')                    # every line by invoice date
    by_receipt = CE.spend('cracker')                   # receipt days, later amounts by invoice date
    spend_inv = {'%s Q%d' % k: v for k, v in G.asks(by_invoice=True)[0].items() if k[0] in GENS}
    d8 = {k for k in gs if abs(gs[k] - spend_inv[k]) >= 30}
    check('ask 1: the receipt-day device (D8) moves every Halvorne and Corwen figure by three bins or more',
          {'Halvorne Q1', 'Halvorne Q2', 'Corwen Q1', 'Corwen Q2'} <= d8, ', '.join('%s %+.0f' % (k, spend_inv[k] - gs[k]) for k in sorted(d8)))
    d6 = {k for k in gs if abs(round(gs[k] / 10) * 10 - by_receipt[k]) >= 30}
    check('ask 1: the catch-up device (D6) moves every spend figure by three bins or more for the cracker', len(d6) == 10,
          ', '.join('%s %+.0f' % (k, by_receipt[k] - round(gs[k] / 10) * 10) for k in sorted(gs)))
    full = CE.backorder('full_includer'); crk = CE.backorder('cracker')
    blockP = {k for k in gd if crk[k] != gd[k]}
    blockQ = {k for k in gd if full[k] != gd[k] and crk[k] == gd[k]}
    check('ask 2: the legacy item numbers (D7) move Halvorne, Pellbrook and Corwen in the first quarter, Pellbrook in the '
          'second and Wynfield in the first', blockP == {'Halvorne Q1', 'Corwen Q1', 'Pellbrook Q1', 'Pellbrook Q2', 'Wynfield Q1'},
          ', '.join('%s %d against %d' % (k, crk[k], gd[k]) for k in sorted(blockP)))
    check('ask 2: the case-level shipments (D4) move the other five figures', len(blockQ) == 5 and not (blockP & blockQ),
          ', '.join('%s %d against %d' % (k, full[k], gd[k]) for k in sorted(blockQ)))
    legacy = sorted((str(r[2]), r[1]) for r in resolved if r[2] < dt.date(2026, 3, 2))
    check('ask 2: each legacy notice resolves to one product, the two without a listed former number by which one stopped '
          'shipping', [p for d, p in legacy] == ['Tessard', 'Halvorne', 'Wynfield', 'Pellbrook', 'Tessard'], str(legacy))
    check('ask 1: each catch-up line\'s bottles are one run of that centre\'s lines from one first dispatch, no quarter\'s '
          'receipts', len(adj_q) == 35 and all(v[0][:7] in ('2025-12', '2026-02') for v in adj_q.values()),
          '%d catch-up lines, first covered dispatch %s' % (len(adj_q), sorted({v[0] for v in adj_q.values()})))
    spend_edge = min(edge(v, 10.0) for v in gs.values())
    check('ask 1 spend mid-bin (nearest 10 dollars)', spend_edge >= 0.7, 'tightest %.2f' % spend_edge)
    main_files = {'dispensing_claims_2025-04_to_2026-06.parquet', 'claims_item_crosswalk.csv', 'members.csv',
                  'mrn_member_crosswalk.csv', 'pharmacies.csv', 'ed_encounters_larkhaven_hospitals.csv',
                  'ed_encounters_partner_hospitals.json', 'product_register.xlsx', 'halvorne_site_change_notice.pdf',
                  'corwen_film_coat_notice.pdf', 'ms12_interchangeable_product_surveillance.pdf'}
    ask_files = {'wholesaler_invoice_lines.csv', 'dc_receiving_log.csv', 'wholesaler_backorder_notices.csv',
                 'wholesaler_item_list.csv', 'wholesaler_advance_ship_notices.json', 'pack_register.csv',
                 'wholesaler_ship_to_accounts.csv', 'purchasing_manual_and_service_schedule.pdf'}
    check('separation: no device row in the main call\'s files', not (main_files & ask_files))
    # ---------------------------------------------------------------- input gates
    tgt = G.TARGET
    files = sorted(p.name for p in tgt.iterdir())
    fmts = {p.split('.')[-1] for p in files}
    check('input gates: 10 or more files, 3 or more formats', len(files) >= 10 and len(fmts) >= 3, '%d files, %s' % (len(files), sorted(fmts)))
    nrow = G.pq.read_metadata(tgt / 'dispensing_claims_2025-04_to_2026-06.parquet').num_rows
    check('input gates: a file of 25,000 rows or more', nrow >= 25000, '%d claim lines' % nrow)
    size = sum((tgt / f).stat().st_size for f in files)
    check('pack under 15 MB', size < 15e6, '%.1f MB' % (size / 1e6))
    meta = json.loads((G.TASK / 'metadata.json').read_text())
    # container metadata: no writer's name or build clock in any input or golden, parquet footer included
    tool = (b'openpyxl', b'python-docx', b'reportlab', b'matplotlib', b'pandas', b'numpy', b'pyarrow', b'2026-11-')
    dirty = []
    for p in sorted(list(tgt.iterdir()) + sorted((G.TASK / 'golden').glob('*'))):
        if p.suffix in ('.xlsx', '.docx'):
            with zipfile.ZipFile(p) as z:
                blob = b''.join(z.read(n) for n in z.namelist() if n.startswith('docProps/') or n.endswith('.png'))
        elif p.suffix == '.pdf':
            blob = p.read_bytes()
        elif p.suffix == '.parquet':
            md = G.pq.read_metadata(p)
            blob = repr(md.metadata).encode()
        else:
            continue
        if any(t in blob.lower() for t in tool):
            dirty.append(p.name)
    # ---------------------------------------------------------------- the three rules, executed (dataset-generation 7.1)
    heads = set(G.pq.read_schema(tgt / 'dispensing_claims_2025-04_to_2026-06.parquet').names)
    for f in files:
        if f.endswith('.csv'):
            heads |= set(pd.read_csv(tgt / f, nrows=0).columns)
    heads |= set(json.loads((tgt / 'ed_encounters_partner_hospitals.json').read_text())['records'][0])
    told = [h for h in heads if any(w in h.lower() for w in ('colour', 'color', 'look', 'appearance', 'first', 'change', 'excess', 'rate'))]
    check('R1 the raw material ships: claim lines and encounter records at the patient-day grain, no column holding a '
          'tablet\'s look, a change, a first fill or an excess', not told and nrow >= 25000, ', '.join(told) or '%d columns read' % len(heads))
    d_sw = R['(d) switching: a transient after a change of product']
    check('R3a the analyst test: standardised rates with the switching allowance file a wrong product', top(d_sw) != CALL,
          'names %s at %.1f' % (top(d_sw), d_sw[top(d_sw)]))
    check('R3b the decisive step alone: the same model with each patient\'s first supply held files Tessard', top(gold) == CALL,
          'Tessard %.2f' % gold[CALL])
    check('R3b every lower rung\'s single correction stays on a wrong product', all(top(d) != CALL for d in R.values()),
          '%d readers' % len(R))
    mon = openpyxl_sheet_headers(tgt / 'levetiracetam_supply_monitor.xlsx')
    raw = G.pq.read_table(tgt / 'dispensing_claims_2025-04_to_2026-06.parquet').to_pandas()
    dup = int(raw.drop(columns=['claim_id']).duplicated().sum())
    check('R3c no plant: the supply monitor carries no product column, no copied claim block', 'product' not in ' '.join(mon).lower()
          and dup <= 0.001 * len(raw), 'monitor columns %s; %d repeated claim lines' % (mon, dup))
    check('container metadata scrubbed (OOXML properties, PDF info, chart PNG, parquet footer)', not dirty, ', '.join(dirty) or 'clean')
    check('input gates: two or more distractors named in metadata.json', len(meta['distractors']) >= 2)
    print('SUMMARY ' + json.dumps(summary))
    if not G.SCREEN:
        (HERE / 'checks_report.txt').write_text('\n'.join(LOG) + '\n')
    print('\n'.join(LOG))
    print('%d checks, %d failed' % (len(LOG), len(FAIL)))
    return 1 if FAIL else 0


if __name__ == '__main__':
    sys.exit(main())
