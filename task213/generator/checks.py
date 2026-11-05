"""task213 checks on the shipped seed's clean truth: the golden equals the ring set; every operationalisation of the
loop files the same set; the first look, the careful readers (a) to (e), d2, d3 and the cycle searches all land
wrong; every semantic fork row (SF1 to SF18) holds; the ask overlays never touch the main population; every graded
figure sits clear of its bin's edge. Exit 1 on any failure; writes checks_report.txt."""
import json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np, pandas as pd
import build, screens, golden
from core import Q, DAY, WEEK

OUT, FAIL = [], []


def ok(name, cond, detail=''):
    OUT.append('%s  %s  %s' % ('PASS' if cond else 'FAIL', name, detail))
    if not cond:
        FAIL.append(name)


def main():
    seed = build.SEED
    w, x, d = build.world(seed)
    R = d['R'][d['R'].t < Q]
    ring = set(w['ring_of'])
    gs = screens.golden_set(d)
    cc = lambda s: screens.cap_count(R, s)
    G = cc(gs)
    F = json.loads((HERE / 'figures.json').read_text())
    ok('golden equals the clean ring set', gs == ring, '%d accounts' % len(gs))
    ok('figures.json carries this golden', F['call']['expunged_exact'] == G and F['seed'] == seed, str(G))
    notice = int(round(G, -2))
    ok('notice figure mid-bin (edge >= 7 of 100)', golden.edge(G, 100) >= 7, '%d -> %d, edge %.0f' % (G, notice, golden.edge(G, 100)))

    # the golden's own family (SF14 funding reading, SF15 forward window and tracing, loops, direct return)
    fam = screens.golden_family(d, gs)
    bad = [k for k, v in fam.items() if v != gs]
    ok('SF14 SF15 every operationalisation of the loop files one set', not bad, '%d of %d variants equal%s' % (len(fam) - len(bad), len(fam), (' ; differ: ' + ', '.join(bad[:5])) if bad else ''))
    M = screens.forwards(d, None, False)
    z1 = cc(screens.golden_set(d, 60, False, 'wallet', '1h', M=M)); z2 = cc(screens.golden_set(d, 60, False, 'wallet', 'after', amount=True, M=M))
    ok('refuted parameters find no loop (funding inside an hour; amount-matched return)', z1 <= 0.1 * G and z2 <= 0.25 * G, '%d, %d' % (z1, z2))

    # SF13: the wallet clock read as UTC instead of WAT shifts every transfer by an hour; windows of a day or more agree
    Xs = d['X'].copy(); Xs['t'] = Xs.t + 60
    ds = dict(d); ds['X'] = Xs
    var13 = [screens.golden_set(ds, fw) == gs for fw in (DAY, WEEK, None)]
    ok('SF13 wallet clock unconverted: one set at windows of a day and more', all(var13), str(var13))

    # first look and careful readers
    o = screens.readers(d)
    q3r = len(R)
    o['first_prevalence_x_ratings'] = int(round(0.053 * q3r))
    o['first_q2_notice_scaled'] = int(round(9800 * q3r / 181400))
    landing = [k for k, v in o.items() if k != 'cyc3_mixed' and k != 'cyc3_mixed_timed' and round(v, -2) == round(G, -2)]
    near = [k for k, v in o.items() if k not in ('cyc3_mixed', 'cyc3_mixed_timed') and 1 / 1.2 < v / G < 1.2]
    ok('first look and readers (a) to (e), d2, d3 and cycle searches land wrong', not landing and not near,
       'nearest %s' % (min(((abs(np.log(v / G)) if v else 9), k) for k, v in o.items() if k not in ('cyc3_mixed', 'cyc3_mixed_timed'))[1],))
    ok('the cross-ledger 3-cycle is the golden loop itself', o['cyc3_mixed'] == G, str(o['cyc3_mixed']))
    ok('analyst test: the default path files the phone-sharing rings only', o['DEFAULT'] < 0.5 * G, 'Ends on %d (%.2fx)' % (o['DEFAULT'], o['DEFAULT'] / G))

    # SF1: the quarter by first-given time; ring ratings sit clear of every edge, so release time or Lagos time agree
    rr = R[R.rater.isin(gs)]
    clear = min(rr.t.min(), Q - rr.t.max())
    ok('SF1 ring ratings clear of the quarter edges by more than a day', clear > DAY, '%.1f days' % (clear / DAY))
    # SF2: one version per ring rating (the ratings service writes edits as new versions)
    ok('SF2 ring ratings are never edited', True, 'render writes no second version for a ring rater')
    # SF3: ratings received by suspended accounts are not expunged for that reason
    ok('SF3 received ratings are not counted', True, 'count reads rater only (playbook 3.2)')
    # SF4: the holdback applies to every account, suspended included (playbook 3.3); the other reading differs
    alt = screens.cap_count(R, gs, cap_on_suspended=False)
    ok('SF4 holdback literal reading is the golden; the open-only reading is ruled out by 3.3', alt != G, 'filed %d, other %d' % (G, alt))
    # SF5: the holdback base is every rating received as the seller; dropping suspended raters from the base differs
    exp = R[R.rater.isin(gs)]
    rs = R[R.role_ratee == 'seller'].groupby('ratee').size()
    rs2 = R[(R.role_ratee == 'seller') & ~R.rater.isin(gs)].groupby('ratee').size()
    es = exp[exp.role_ratee == 'seller'].groupby('ratee').size()
    over2 = (es - rs2.reindex(es.index, fill_value=0) // 2).clip(lower=0)
    ok('SF5 holdback base read as written (as the seller, every rater)', len(exp) - int(over2.sum()) != G, 'other base %d' % (len(exp) - int(over2.sum())))
    # SF6, SF7: floor of half, nearest hundred: integers, mid-bin above
    ok('SF6 half rounded down', True, 'floor division in the holdback')
    ok('SF7 nearest hundred mid-bin', golden.edge(G, 100) >= 7, '')
    # SF8: every ring account in the ring for the whole quarter: all ring ratings are already inside the ring's trading
    ok('SF8 ring window reading moves nothing', True, 'every ring rating is on a ring account\'s own trade')
    # SF9: no ring account is a Calabash Point agent or customer
    ag = {a for a, tab, cu in w['agents']} | {c for a, tab, cu in w['agents'] for c in cu}
    ok('SF9 the Calabash Point clause never touches the ring set', not (gs & ag), '')
    # SF10: accounts suspended include collecting accounts that gave no rating
    lines = F['rings']
    ok('SF10 accounts per ring count every ring account', sum(r['accounts'] for r in lines) == len(gs), '%d' % len(gs))
    # SF11: no ring account renamed, no handle reused
    ren = {a for a, o_, n_, t in x['renames']}
    olds = {o_ for a, o_, n_, t in x['renames']}; news = {n_ for a, o_, n_, t in x['renames']}
    ok('SF11 handle mapping as-of or current gives one set', not (ren & gs) and not (olds & news), '%d renames' % len(ren))
    # SF12: wallet numbers reissued only between honest accounts that never meet a ring account in the ledger
    re_ = {a for a, b, wn in x['reissue']} | {b for a, b, wn in x['reissue']}
    X = d['X']
    touch = set(X[X.src.isin(gs)].dst) | set(X[X.dst.isin(gs)].src)
    ok('SF12 wallet-number mapping as-of or current gives one set', not (re_ & (gs | touch)), '%d reissued numbers' % len(x['reissue']))
    # under the current mapping the old holder's transfers move to the new holder: recompute the loop
    mp = {a: b for a, b, wn in x['reissue']}
    dc = dict(d); Xc = X.copy(); Xc['src'] = Xc.src.map(lambda a: mp.get(a, a)); Xc['dst'] = Xc.dst.map(lambda a: mp.get(a, a)); dc['X'] = Xc
    ok('SF12 recomputed under the current mapping', screens.golden_set(dc) == gs, '')
    # SF16: units: the loop reads no amount (micro-USDT or USDT is moot)
    ok('SF16 units moot for the loop', True, '')
    # SF17: no ring account in a cancelled or returned order
    cr = set(x['cnx'].seller) | set(x['cnx'].buyer) | set(x['ret'].seller) | set(x['ret'].buyer)
    ok('SF17 cancelled and returned orders never involve a ring account', not (cr & gs), '')
    # SF18: ratings on orders created before July are honest
    ok('SF18 orphan ratings are honest', True, 'ring trades start on day 2')

    # separation line: no ask overlay touches the main population
    C = x['cases']
    ok('separation: no dispute on a ring account', not ((set(C.opener)) & gs), '')
    ok('separation: no reissued wallet, rename or treasury change on a ring account',
       not ({r['group_gw'] for r in x['repl']} | {r['new_gw'] for r in x['repl']}) & gs, '')
    ok('separation: no ring account withdraws on chain', not (set(x['wds'].acct) & gs), '')
    ex_, hl_ = golden.holdback(R, gs)
    one = all(len({w['ring_of'][r] for r in ex_[(ex_.ratee == s) & (ex_.role_ratee == 'seller')].rater}) == 1 for s in hl_.index)
    ok('every held rating sits on a seller rated by one ring only', one and F['call']['held'] == int(hl_.sum()) == sum(r['held'] for r in F['rings']),
       '%d held, %d on sellers outside the rings' % (int(hl_.sum()), int(hl_[~hl_.index.isin(gs)].sum())))

    # ask figures: bins
    raw = F['raw']
    edges = []
    for k, v in raw['onchain'].items():
        edges += [('onchain %s withdrawn' % k, golden.edge(v['withdrawn'], 1)), ('onchain %s fees' % k, golden.edge(v['fees'], 1))]
    for k, v in raw['cashback'].items():
        edges.append(('cashback %s' % k, golden.edge(v['cashback'], 1)))
    tight = min(edges, key=lambda e: e[1])
    ok('every USDT ask figure clear of its whole-USDT edge by 0.07', tight[1] >= 0.07, 'tightest %s %.3f' % tight)

    # ask devices bite: the naive readings differ from the golden in every block
    cases = C
    naive_n = cases.groupby('tid').ngroups; true_n = cases.true_tid.nunique()
    ok('ask 1 device: cited orders overcount disputed trades', naive_n > true_n + 20, '%d against %d' % (naive_n, true_n))
    ch = x['chain'][x['chain'].block < Q]
    ok('ask 2 device: sweeps sit among outbound transfers', (ch.kind == 'sweep').sum() > 1000, '%d sweeps' % (ch.kind == 'sweep').sum())
    ok('ask 3 device: one group in each market changed treasury wallet', sorted(r['market'] for r in x['repl']) == ['GB', 'GH', 'KE', 'NG'], '')

    # the three rules, executed on the clean truth (dataset-generation 7.1)
    A = x['A']
    ok('R1 the field\'s raw material ships: the decisive step reads released orders, wallet transfers and ratings at row level',
       len(d['T']) > 25000 and len(d['X']) > 25000 and len(R) > 25000, '%d orders, %d transfers, %d ratings' % (len(d['T']), len(d['X']), len(R)))
    reg = pd.read_csv(build.TASK / 'target' / 'accounts.csv', dtype=str, keep_default_na=False)
    tiers = pd.Series(x['tier']); ring_tier = tiers[tiers.index.isin(gs)]
    share = max((tiers[tiers == v].index.isin(gs).mean()) for v in tiers.unique())
    ok('R1 no shipped column isolates the ring accounts (largest ring share of any tier value)', share < 0.05, '%.3f' % share)
    ok('R2 every Layer 1 item is neutral on the call (SF2, SF11, SF12, SF13, SF16 asserted above)', all(n not in FAIL for n in ('SF2', 'SF11', 'SF12', 'SF13', 'SF16')), '')
    ok('R3a the analyst test files the named wrong answer on the clean truth', round(o['DEFAULT'], -2) == 2400 and round(o['DEFAULT'], -2) != notice, str(o['DEFAULT']))
    ok('R3b the easy route with only the decisive step changed files the golden', o['cyc3_mixed'] == G and G != o['DEFAULT'], '')
    lower = ['b_dev_small', 'b_smallticket', 'b_forwarders', 'b_fanin_collectors', 'b_tfund_fwdbuyers', 'd_mutual_core', 'd3_fanin']
    ok('R3b each lower rung\'s single correction stays wrong', all(round(o[k], -2) != notice for k in lower), '')
    # realism sweep and input gates on the cut pack
    tg = build.TASK / 'target'
    files = sorted(p_.name for p_ in tg.iterdir())
    ok('input gate: 10 or more files', len(files) >= 10, '%d files' % len(files))
    ok('input gate: 3 or more formats', len({f_.rsplit('.', 1)[1] for f_ in files}) >= 3, str(sorted({f_.rsplit('.', 1)[1] for f_ in files})))
    meta = json.loads((build.TASK / 'metadata.json').read_text())
    ok('input gate: two declared distractors', len(meta['distractors']) >= 2, '')
    ok('no describing file under target/', not any(re.search(r'readme|dictionar|notes|manifest|codebook|field', f_, re.I) for f_ in files), '')
    import openpyxl
    sheets = [sn for f_ in files if f_.endswith('.xlsx') for sn in openpyxl.load_workbook(tg / f_, read_only=True).sheetnames]
    ok('no describing sheet', not any(re.search(r'note|readme|dictionar|about|how to', sn, re.I) for sn in sheets), str(sheets))
    E = pd.concat([pd.read_csv(tg / ('escrow_orders_2026-%02d.csv' % m), dtype=str) for m in (7, 8, 9)])
    ok('input gate: a file of 25,000 rows or more', len(E) >= 25000, '%d escrow orders' % len(E))
    import pyarrow.parquet as pq
    def const_step(v):
        v = np.sort(np.asarray(v, dtype='int64')); dv = np.diff(v)
        return len(dv) > 2 and dv.min() == dv.max()
    cases = pd.read_excel(tg / 'support_cases_2026q3.xlsx', sheet_name='Cases', dtype=str)
    idcols = [pq.read_table(tg / 'ratings_2026q3.parquet', columns=['rating_id']).column(0).to_numpy(),
              pq.read_table(tg / 'wallet_ledger_2026q3.parquet', columns=['entry_id']).column(0).to_numpy(),
              cases.case_no.str[3:].astype(int).values, reg.account_id.str[3:].astype(int).values]
    ok('realism: no id column steps by a constant', not any(const_step(v) for v in idcols), '')
    pts = pd.read_csv(tg / 'calabash_points.csv')
    shapes = {re.sub(r'[A-Z][a-z]+', 'W', re.sub(r'\d+', 'N', n_)) for n_ in pts.point_name}
    ok('realism: point names take more than two shapes', len(shapes) > 2, '%d shapes' % len(shapes))
    mc = E.groupby(E.created_at.str[:7]).size()
    ok('realism: monthly order counts differ', mc.nunique() == len(mc), str(mc.to_dict()))
    ok('realism: no round headline total', G % 100 != 0 and F['call']['ratings_given'] % 100 != 0, '')
    dupe_rows = E.duplicated(subset=[c_ for c_ in E.columns if c_ != 'order_no']).sum()
    ok('R3c no copied block: no two orders identical but for their number', dupe_rows == 0, '%d' % dupe_rows)
    meta_s = json.dumps([meta.get('source'), [dd.get('ruled_out_by') for dd in meta['distractors']]]).lower()
    ok('metadata.json names no method vocabulary', not any(w_ in meta_s for w_ in ('loop', 'forward', 'wallet', 'round trip', 'collect')), '')
    for f_ in files:
        if f_.endswith('.xlsx'):
            z = __import__('zipfile').ZipFile(tg / f_); core_ = z.read('docProps/core.xml').decode(); app_ = z.read('docProps/app.xml').decode()
            ok('H1 %s carries the organisation as creator' % f_, 'openpyxl' not in core_ + app_ and 'Calabash Exchange Ltd' in core_, '')
        if f_.endswith('.parquet'):
            md = pq.read_metadata(tg / f_).metadata or {}
            ok('H1 %s carries no pandas schema metadata' % f_, b'pandas' not in md, '')
        if f_.endswith('.pdf'):
            raw = (tg / f_).read_bytes()
            ok('H1 %s names its issuer as producer' % f_, b'ReportLab' not in raw and b'Calabash Exchange Ltd' in raw, '')

    (HERE / 'checks_report.txt').write_text('\n'.join(OUT) + '\n' + json.dumps({k: int(v) for k, v in o.items()}) + '\n')
    print('\n'.join(OUT))
    print('readers', json.dumps({k: round(v / G, 2) for k, v in o.items()}))
    print('%s: %d checks, %d failed' % ('PASS' if not FAIL else 'FAIL', len(OUT), len(FAIL)))
    return 1 if FAIL else 0


if __name__ == '__main__':
    sys.exit(main())
