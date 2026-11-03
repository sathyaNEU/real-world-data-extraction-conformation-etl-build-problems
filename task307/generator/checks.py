"""task307 generator checks: the three rules on the clean truth, every semantic fork, the ladder, separation, the input
gates and the realism sweep. Run after make.py:

    python3 task307/generator/checks.py          exit 1 on any failed assertion
"""
import datetime as dt
import json
import os
import re
import sys
import zipfile
import numpy as np
import world as Wm
import truth as Tm
import verify as V
from world import UNITS, L, NH, LIMIT, local

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, 'target')
RESULTS = []


def check(tag, ok, detail=''):
    RESULTS.append((tag, bool(ok), detail))


def rnd(x, step):
    return int(np.floor(x / step + 0.5) * step)


def carry(W, rate, what, mode_cross=True):
    """Carry every present runner from its last inspection at `rate` per counted hour; returns rows like Tm.call."""
    rows = {}
    for u in UNITS:
        rn = Tm.current_runner(u)
        f = Tm.last_inspection(W, rn)
        p0 = f['found'] if f['repaired_to'] is None else f['repaired_to']
        now = p0 + rate * Tm.runner_counts(W, rn, f['i'], NH, what)
        q26 = Tm.runner_counts(W, rn, L(2026, 1, 1), NH, what)
        cross, p = None, now
        for y in range(2027, 2032):
            p += rate * q26
            if p >= LIMIT and cross is None:
                cross = y
        if now >= LIMIT:
            cross = 2027
        gen = Tm.winter_generation(W, u) if cross else 0.0
        rows[u] = {'now': now, 'cross': cross, 'gen': gen, 'per_mnok': gen / Wm.QUOTE_MNOK[u]}
    return rows, sorted(UNITS, key=lambda u: -rows[u]['per_mnok'])


def main():
    W = Wm.build()
    F = json.load(open(os.path.join(HERE, 'figures.json'), encoding='utf-8'))
    gold, order = Tm.call(W, 'rz')
    G = order[0]
    check('golden pick', G == F['call']['chosen'] == 'NSV-G1', G)

    # ---- The three rules, executed on the clean truth (dataset-generation 7.1) ----
    ladder = {m: Tm.call(W, m)[1][0] for m in ('run_pooled', 'counters', 'run_own', 'run_pooled_all', 'starts')}
    check('R1 analyst test: the default path (fleet pitting per running hour, peaker set aside) files NSV-G2',
          ladder['run_pooled'] == 'NSV-G2', ladder['run_pooled'])
    check('R1 analyst test: the counter route with every pre-period pair files NSV-G2', ladder['counters'] == 'NSV-G2',
          ladder['counters'])
    check('R1 each runner on its own pairs per running hour files NSV-G2', ladder['run_own'] == 'NSV-G2', ladder['run_own'])
    check('R1 per running hour with the peaker pooled files OSD-G1', ladder['run_pooled_all'] == 'OSD-G1', ladder['run_pooled_all'])
    check('R1 per start files SDL-G3', ladder['starts'] == 'SDL-G3', ladder['starts'])
    cheap = [m for m, p in ladder.items() if p == G]
    check('R1 cheap routes landing the call: none', not cheap, ','.join(cheap) or 'none')
    rows0, _ = Tm.call(W, 'run_pooled')
    check('R1 the default path takes no runner but NSV-G2 past the limit before 2032',
          [u for u in UNITS if rows0[u]['cross']] == ['NSV-G2'], str([u for u in UNITS if rows0[u]['cross']]))
    # Rule 2: every Layer 1 handling leaves the call and its graded figures unchanged (on the cut pack, below).
    # Rule 3: the standing family (rates per restricted-band hour under every estimator) agrees on every graded figure;
    # the enumerated family spreads the pick.
    P = Tm.pairs(W)
    inc = [(p[0], p[4] - p[2], Tm.runner_counts(W, p[0], p[1], p[3], 'rz')) for p in P]
    ests = {'pooled': sum(a for _, a, b in inc) / sum(b for _, a, b in inc),
            'mean of ratios': float(np.mean([a / b for _, a, b in inc])),
            'median': float(np.median([a / b for _, a, b in inc])),
            'base-load pairs only': sum(a for r, a, b in inc if r != 'R-207') / sum(b for r, a, b in inc if r != 'R-207'),
            'peaker pairs only': sum(a for r, a, b in inc if r == 'R-207') / sum(b for r, a, b in inc if r == 'R-207'),
            'least squares through zero': sum(a * b for _, a, b in inc) / sum(b * b for _, a, b in inc)}
    ref = None
    for k, rate in ests.items():
        rows, o = carry(W, rate, 'rz')
        figs = (o[0], o[1], tuple((rnd(rows[u]['now'], 10), rows[u]['cross'], rnd(rows[u]['gen'], 100),
                                   rnd(rows[u]['per_mnok'], 10)) for u in UNITS))
        ref = ref or figs
        check('R3 standing family agrees: %s' % k, figs == ref, '%.5f' % rate)
    picks = {Tm.call(W, m)[1][0] for m in ('run_pooled', 'run_own', 'counters', 'starts', 'run_pooled_all', 'rz')}
    check('R3 enumerated family spreads the pick over four units', len(picks) == 4, ','.join(sorted(picks)))
    ratios = [a / b for _, a, b in inc]
    check('band rate fits every pair, the peaker included, within 1 per cent', max(ratios) / min(ratios) - 1 < 0.01,
          '%.4f to %.4f' % (min(ratios), max(ratios)))
    runr = [(p[0], (p[4] - p[2]) / Tm.runner_counts(W, p[0], p[1], p[3], 'run')) for p in P if p[0] != 'R-207']
    spread = max(r for _, r in runr) / min(r for _, r in runr) - 1
    check('back-test: pitting per running hour across the base-load pairs within 15 per cent', spread < 0.15,
          'spread %.1f per cent' % (100 * spread))
    peak = [(p[4] - p[2]) / Tm.runner_counts(W, p[0], p[1], p[3], 'run') for p in P if p[0] == 'R-207']
    check('the peaker wears about ten times as fast per running hour', min(peak) / max(r for _, r in runr) > 5,
          '%.4f against %.4f' % (min(peak), max(r for _, r in runr)))
    check('no inspection pair of a reserve unit spans its reserve duty',
          all(not (p[0] in ('R-205', 'R-501') and p[3] > L(2022, 1, 1)) for p in P))
    # margins
    a, b = order[0], order[1]
    check('lead over the runner-up at least 1.1 times per NOK million', gold[a]['per_mnok'] / gold[b]['per_mnok'] >= 1.1,
          '%.2f' % (gold[a]['per_mnok'] / gold[b]['per_mnok']))
    check('NSV-G1 passes the limit in 2027 and SDL-G1 in 2029', gold['NSV-G1']['cross'] == 2027 and gold['SDL-G1']['cross'] == 2029)
    # the one-dimensional statistic law: the pick is never first on a statistic the pack carries or a reader sorts on
    gen16, st16 = Tm.totals(W)
    last = {u: Tm.last_inspection(W, Tm.current_runner(u)) for u in UNITS}
    stats = {
        'pitting at last inspection': {u: gold[u]['last_pitting'] for u in UNITS},
        'age of last inspection': {u: -last[u]['i'] for u in UNITS},
        'running hours since last inspection': {u: Tm.runner_counts(W, Tm.current_runner(u), last[u]['i'], NH, 'run') for u in UNITS},
        'starts since 2016': st16, 'generation since 2016': gen16,
        'rating': Wm.RATED, 'lowest quote': {u: -Wm.QUOTE_MNOK[u] for u in UNITS},
        'winter generation per NOK million': {u: Tm.winter_generation(W, u) / Wm.QUOTE_MNOK[u] for u in UNITS},
        'reserve capacity': {u: {'SDL-G1': 10.0, 'NSV-G1': 9.0}.get(u, 0.0) for u in UNITS},
        'own pair pitting per running hour': {u: max([r for rn, r in runr if rn == Tm.current_runner(u)] or [0]) for u in UNITS},
    }
    for k, v in stats.items():
        top = max(v, key=lambda u: v[u])
        check('shock: the pick is not first on %s' % k, top != G, top)

    # ---- Semantic forks (every SF row of the design note's fork table) ----
    D = V.load()
    raw = D['insp']
    blade_cols = [c for c in raw.columns if c.startswith('Skovl') or c == 'Bånd']
    ok = all(abs(sum(V.num(r[c]) for c in blade_cols) - V.num(r['Funn totalt (cm²)'])) < 0.05 for _, r in raw.iterrows())
    check('SF1 pitting is the total over blades and band: every register row sums to its total', ok)
    import pdfplumber
    with pdfplumber.open(os.path.join(TGT, 'runner_standard_TS07_rev3.pdf')) as pdf:
        stdtext = ' '.join(p.extract_text() for p in pdf.pages)
    check('SF1 TS-07 4.2 files pitting as the total pitted area of blades and band', 'total pitted area of the runner' in stdtext)
    check('SF2 the repair limit is 2,400 cm2 of total pitting and no per-blade limit is filed',
          '2,400 cm2' in stdtext and 'blade with' not in stdtext)
    S, assign = V.series(D)
    check('SF3 the record and the projection end at 31 December 2026 24:00 local',
          local(NH - 1).strftime('%Y-%m-%d %H') == '2026-12-31 23' and len(S['NSV-G1']) == NH)
    # SF4: the year read at year ends equals the year read hour by hour with 2026 repeated
    for u in ('NSV-G1', 'SDL-G1', 'SDL-G3'):
        rn = Tm.current_runner(u)
        rate = gold[u]['rate']
        hrs = W['inz'][u][L(2026, 1, 1):NH] & (W['occ'][u][L(2026, 1, 1):NH] == rn)
        cum = gold[u]['now'] + rate * np.cumsum(np.tile(hrs, 5))
        k = int(np.argmax(cum >= LIMIT)) if (cum >= LIMIT).any() else None
        year = 2027 + k // len(hrs) if k is not None else None
        check('SF4 %s passes the limit in the same year read hour by hour' % u, year == gold[u]['cross'], str(year))
    # SF5: the outage valued as 14 weeks of the unit's mean generation over the whole of 2021 to 2025, not its winter weeks
    check('SF5 the outage counted from 1 December (TS-07 6.1, note 3.1)', '1 December of the year' in stdtext)
    flat = {}
    for u in UNITS:
        o = W['out'][u][L(2021, 1, 1):L(2026, 1, 1)]
        flat[u] = (o.sum() / 5 * 14 * 7 / 365.25 / Wm.QUOTE_MNOK[u]) if gold[u]['cross'] else 0.0
    check('SF5 the call holds when the 14 weeks are valued at the year-round mean', max(UNITS, key=lambda u: flat[u]) == G)
    # SF6: all winters since 2016/17 instead of the last five
    w_all = {}
    for u in UNITS:
        o = W['out'][u]
        tot = [o[L(y, 12, 1):Wm.hidx(dt.datetime(y, 12, 1, tzinfo=Wm.OSLO) + dt.timedelta(weeks=14))].sum() for y in range(2016, 2026)]
        w_all[u] = np.mean(tot) if gold[u]['cross'] else 0.0
    check('SF6 the call holds on every winter since 2016/17',
          max(UNITS, key=lambda u: w_all[u] / Wm.QUOTE_MNOK[u]) == G)
    # SF7: outages ending before 2032 drop the 2031 outage; the call holds
    end32 = {u: (gold[u]['per_mnok'] if gold[u]['cross'] and gold[u]['cross'] < 2031 else 0.0) for u in UNITS}
    check('SF7 the call holds when the window counts only outages ending before 2032', max(UNITS, key=lambda u: end32[u]) == G)
    # SF8: duty carried at the 2022 to 2026 mean instead of 2026
    rows8 = {}
    for u in UNITS:
        rn = Tm.current_runner(u)
        q = np.mean([Tm.runner_counts(W, rn, L(y, 1, 1), L(y + 1, 1, 1), 'rz') for y in range(2022, 2027)])
        p, cross = gold[u]['now'], None
        for y in range(2027, 2032):
            p += gold[u]['rate'] * q
            if p >= LIMIT and cross is None:
                cross = y
        rows8[u] = (Tm.winter_generation(W, u) / Wm.QUOTE_MNOK[u]) if cross else 0.0
    check('SF8 the call holds with duty carried at the 2022 to 2026 mean', max(UNITS, key=lambda u: rows8[u]) == G)
    # SF9: reading each unit's latest register row instead of its present runner's latest row gives the same start
    regrows = V.inspections(D)
    same9 = True
    for u in UNITS:
        by_unit = [r for r in regrows if r['unit'] == u][-1]
        by_runner = [r for r in regrows if r['runner'] == Tm.current_runner(u)][-1]
        same9 &= by_unit == by_runner
    check('SF9 each unit\'s latest register row is its present runner\'s latest row (same call)', same9)
    with pdfplumber.open(os.path.join(TGT, 'runner_standard_TS07_rev3.pdf')) as pdf:
        pass
    check('SF9 TS-07 2.1 ties condition limits to the runner across moves', 'whichever unit it is installed in' in stdtext)
    reg = D['units']
    check('SF9 the register names each unit\'s present runner',
          all(reg[reg['Aggregat'] == u]['Løpehjul'].iloc[0] == Tm.current_runner(u) for u in UNITS))
    # SF10: VAT included scales every quote alike
    check('SF10 the call holds with VAT included', max(UNITS, key=lambda u: gold[u]['gen_mwh'] / (1.25 * Wm.QUOTE_MNOK[u])) == G)
    # SF11: other band edges
    for lo, hi in ((0.25, 0.60), (0.30, 0.5801), (0.2999, 0.58)):
        rz = {u: (W['out'][u] >= lo * Wm.RATED[u] - 1e-9) & (W['out'][u] < hi * Wm.RATED[u] - 1e-9) for u in UNITS}
        W2 = dict(W)
        W2['inz'] = rz
        p2 = Tm.call(W2, 'rz')[1][0]
        check('SF11 the call holds with the band at %.4f to %.4f' % (lo, hi), p2 == G, p2)
    check('SF11 the operating range table files the band from 30 per cent to 58 per cent', D['band'] == (0.30, 0.58))
    # SF12 and SF14: the asks sum each hour once, gross at the terminals, and count starts on consecutive hours
    g_pack, s_pack = V.asks(S)
    check('SF12 generation since 2016 sums each hour of the record once',
          all(rnd(g_pack[u], 100) == F['asks']['generation_2016_2026_mwh'][u] == rnd(gen16[u], 100) for u in UNITS))
    check('SF14 starts count standstill to generation between consecutive hours',
          all(s_pack[u] == F['asks']['starts_2016_2026'][u] == st16[u] for u in UNITS))
    # SF13: the record's bounds are the same in local time and UTC (no exported hour outside 2016 to 2026 local)
    new = D['new']
    last_new = V.pd.to_datetime(new['time_utc'].iloc[-1], utc=True).tz_convert('Europe/Oslo')
    first_old = D['old']['Tidspunkt'].iloc[0]
    check('SF13 the record runs from 01.01.2016 00:00 to 31.12.2026 23:00 local',
          first_old == '01.01.2016 00:00' and last_new.strftime('%Y-%m-%d %H:%M') == '2026-12-31 23:00')

    # ---- The cut pack ----
    rows, porder = V.call(D, S)
    same = all((rnd(rows[u]['now'], 10), rows[u]['cross'], rnd(rows[u]['gen'], 100), rnd(rows[u]['per_mnok'], 10)) ==
               (F['units'][u]['now_cm2'], F['units'][u]['cross_year'], F['units'][u]['gen_mwh'], F['units'][u]['per_mnok'])
               for u in UNITS)
    check('the pack recomputes every call figure', same and porder[:2] == [G, order[1]])
    base_g, base_s = g_pack, s_pack
    for kw in (dict(swap='map'), dict(swap='map', overlap='twice'), dict(swap='map', dst='label'), dict(overlap='twice'),
               dict(dst='label')):
        S2, _ = V.series(D, **kw)
        r2, o2 = V.call(D, S2)
        inv = o2[:2] == porder[:2] and all((rnd(r2[u]['now'], 10), r2[u]['cross'], rnd(r2[u]['gen'], 100)) ==
                                           (rnd(rows[u]['now'], 10), rows[u]['cross'], rnd(rows[u]['gen'], 100)) for u in UNITS)
        check('separation: the call and its figures hold under %s' % kw, inv)
    S_map, _ = V.series(D, swap='map')
    gm, sm = V.asks(S_map)
    check('device D1 moves every generation figure by three bins or more', all(abs(gm[u] - base_g[u]) >= 300 for u in UNITS),
          str({u: round(gm[u] - base_g[u]) for u in UNITS}))
    check('device D1 moves every starts figure by three or more', all(abs(sm[u] - base_s[u]) >= 3 for u in UNITS),
          str({u: sm[u] - base_s[u] for u in UNITS}))
    check('the slot re-assignment recovers the wiring the world used',
          all(assign[st][0] == {t: u for t, u in Wm.OLD_SLOT.items() if t[:3].replace('NES', 'NSV') == st} for st in assign))
    # the swaps sit outside every window the call reads: each pair starts, and each present runner's last inspection
    # falls, on or after its station's RTU replacement
    station = {u: u[:3] for u in UNITS}
    unit_of = {f['runner']: f['unit'] for f in W['found']}
    ok_pairs = all(L(*Wm.RTU_NEW[station[unit_of[p[0]]]]) <= p[1] for p in P)
    ok_proj = all(L(*Wm.RTU_NEW[station[u]]) <= last[u]['i'] for u in UNITS)
    check('the slot swaps end before every inspection pair and projection window', ok_pairs and ok_proj)
    # ---- Input gates ----
    files = sorted(os.listdir(TGT))
    exts = {os.path.splitext(f)[1] for f in files}
    check('input gate: ten or more files', len(files) >= 10, str(len(files)))
    check('input gate: three or more formats', len(exts) >= 3, ','.join(sorted(exts)))
    big = max(sum(1 for _ in open(os.path.join(TGT, f), encoding='utf-8')) for f in files if f.endswith('.csv'))
    check('input gate: a file of 25,000 rows or more', big >= 25000, str(big))
    meta = json.load(open(os.path.join(TASK, 'metadata.json'), encoding='utf-8'))
    dis = meta.get('distractors', [])
    check('input gate: two or more distractors named in metadata.json and shipped',
          len(dis) >= 2 and all(d['file'] in files for d in dis))
    check('input gate: every file has source, date and license in metadata.json',
          {f['file'] for f in meta['files']} == set(files) and all(f.get('license') and f.get('source') and f.get('date')
                                                                for f in meta['files']))
    check('no data dictionary, readme, manifest, codebook or notes file shipped',
          not [f for f in files if re.search(r'readme|dictionary|manifest|codebook|notes|field_guide', f, re.I)])
    # ---- Realism sweep ----
    tells = []
    for f in files:
        p = os.path.join(TGT, f)
        if f.endswith(('.xlsx', '.docx')):
            z = zipfile.ZipFile(p)
            names = z.namelist()
            blob = b''.join(z.read(n) for n in names if n.startswith('docProps/'))
            if any(n.startswith('customXml/') or 'thumbnail' in n for n in names):
                tells.append(f + ' thumbnail or customXml')
            if re.search(rb'openpyxl|python-docx|Macintosh|Compatible', blob, re.I):
                tells.append(f + ' library app name')
            if not re.search(rb'Microsoft (Excel|Office Word)', blob):
                tells.append(f + ' no Office app name')
            if len({zi.date_time for zi in z.infolist()}) != 1:
                tells.append(f + ' member dates differ')
        if f.endswith('.pdf'):
            b = open(p, 'rb').read()
            if b'ReportLab' in b or b'(anonymous)' in b or b'reportlab' in b:
                tells.append(f + ' ReportLab stamp')
        if f.endswith('.csv'):
            t = open(p, encoding='utf-8').read(200000)
            if '—' in t or '–' in t:
                tells.append(f + ' dash')
    check('realism sweep: no library stamps, thumbnails or dashes', not tells, '; '.join(tells))
    note = open(os.path.join(TASK, 'DESIGN_NOTE.md'), encoding='utf-8').read()
    check('no em dash in the design note or prompt', '—' not in note and '—' not in open(os.path.join(TASK, 'prompt.txt')).read())

    bad = [r for r in RESULTS if not r[1]]
    for tag, ok, detail in RESULTS:
        print('%s  %s%s' % ('PASS' if ok else 'FAIL', tag, ('  [' + detail + ']') if detail else ''))
    print('%d checks, %d failed' % (len(RESULTS), len(bad)))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
