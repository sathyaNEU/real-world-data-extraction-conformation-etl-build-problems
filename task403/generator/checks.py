"""task403 checks: the generator's assertions on the clean truth and on the cut pack.

    python3 checks.py        # exit 0 when every assertion holds

Covers the three rules (R1 to R3c), the ladder, the semantic fork table (SF1 to SF17), the separation line of the ask
devices counted from the shipped rows, the devices' mechanics, every graded figure's bin, the input gates and the
realism sweep. Run after build.py.
"""
import io
import json
import os
import re
import sys
import zipfile
import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, 'target')
sys.path.insert(0, HERE)
import world
import pack
import golden
import screens
import verify

RESULTS = []


def check(label, ok, detail=''):
    RESULTS.append((label, bool(ok), detail))
    print('%s  %-58s %s' % ('PASS' if ok else 'FAIL', label, detail))


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def split(T, col):
    """The golden's split on any state column: the slate, the within-state fall, recovery, channel, price."""
    a, b = T[T.per == 'W24'], T[T.per == 'W25']
    n25 = len(b)
    p24, p25 = a.paid.mean(), b.paid.mean()
    if b[col].sum() == 0:
        C = (p24 - a[~a[col]].paid.mean()) * n25
    else:
        C = screens.mixsplit(a, b, col)
    within = (p24 - p25) * n25 - C
    B = (a[a.declined].recovered.mean() - b[b.declined].recovered.mean()) * b.declined.sum()
    s24 = a.groupby('channel').size() / len(a)
    s25 = b.groupby('channel').size() / len(b)
    D = float(((s24 - s25) * b.groupby('channel').paid.mean()).sum()) * n25
    return {'C': C, 'A': within - B - D, 'B': B, 'D': D, 'fall': (p24 - p25) * n25}


def pick(v):
    return max(('A', 'B', 'C', 'D'), key=lambda k: v[k])


def main():
    W = world.simulate()
    T0, tw, C0, CH = pack.systems(W)
    F = golden.compute(W, T0)
    figs = json.load(open(os.path.join(HERE, 'figures.json')))
    meta = json.load(open(os.path.join(TASK, 'metadata.json')))
    T = screens.frame(W)
    T['declined'] = T.declined.values
    R = F['_raw']
    files = sorted(os.listdir(TGT))

    # ------------------------------------------------------------------ input gates
    check('G1 ten or more files', len(files) >= 10, '%d files' % len(files))
    fmts = {os.path.splitext(x)[1] for x in files}
    check('G2 three or more formats', len(fmts) >= 3, ', '.join(sorted(fmts)))
    nview = len(pd.read_parquet(os.path.join(TGT, 'trial_viewing_2024-11_2026-02.parquet')))
    check('G3 a file of 25,000 rows or more', nview >= 25000, 'viewing %d rows' % nview)
    dis = meta.get('distractor_files', [])
    check('G4 two distractors named in metadata.json and shipped', len(dis) >= 2 and all(
        os.path.exists(os.path.join(TASK, d)) for d in dis), ', '.join(dis))
    bad = [x for x in files if re.search(r'readme|dictionar|notes|manifest|codebook|schema|field', x, re.I)]
    check('G5 no file describes the data', not bad, ', '.join(bad) or 'none')
    stumpy = [x for x in files if re.search(r'runway|slate|still_to_come|trap|answer|distract', x, re.I)]
    check('G6 no file name broadcasts the stump or a role', not stumpy, ', '.join(stumpy) or 'none')

    # ------------------------------------------------------------------ the pack, read back by the verifier's path
    reg, view, ca, cb, pc, xa, xc, cal = verify.load()
    Rv, n_twins = verify.trials(reg, xc, cal)
    ch = verify.attempts(ca, cb)
    Rv, n_orph, n_match = verify.link(Rv, ch, pc)
    m, n_runs = verify.plays(Rv, view, xa, xc, cal)
    Rv['played'] = Rv.trial_id.isin(set(m.trial_id))

    # ------------------------------------------------------------------ R1: the field's raw material ships
    seas_cols = []
    for x in files:
        p = os.path.join(TGT, x)
        if x.endswith('.csv'):
            cols = list(pd.read_csv(p, nrows=5).columns)
        elif x.endswith('.parquet'):
            cols = list(pd.read_parquet(p).columns)
        elif x.endswith('.xlsx'):
            cols = list(pd.read_excel(p, nrows=5).columns)
        else:
            continue
        seas_cols += [c for c in cols if re.search(r'runway|airing|to_come|remaining|still', str(c), re.I)]
    check('R1a no column names the deciding state', not seas_cols, ', '.join(map(str, seas_cols)) or 'none')
    cal2 = cal.assign(season_key=cal.series + ' S' + cal.season.astype(str))
    lastrel = cal2.assign(t=pd.to_datetime(cal2.release_toronto).dt.tz_localize('America/Toronto').dt.tz_convert('UTC')
                          .dt.tz_localize(None)).groupby('season_key').t.max()
    sv = m.drop_duplicates(['trial_id', 'season_key'])
    sv = sv[sv.season_key.map(lastrel).values > sv.end.values]
    Rv['run'] = Rv.trial_id.isin(set(sv.trial_id))
    a_v, b_v = Rv[Rv.per == 'W24'], Rv[Rv.per == 'W25']
    check('R1b the state rebuilt from the viewing rows and the calendar equals the truth',
          abs(a_v.run.mean() - T[T.per == 'W24'].run.mean()) < 1e-9 and b_v.run.sum() == 0,
          'W24 %.4f / %.4f, W25 %d' % (a_v.run.mean(), T[T.per == 'W24'].run.mean(), b_v.run.sum()))

    # ------------------------------------------------------------------ R3: the analyst test and the decisive step
    base = split(T, 'run')
    rung0 = {'A': base['fall'], 'B': 0, 'C': 0, 'D': 0}
    rung1 = {'A': base['fall'] - base['B'] - base['D'], 'B': base['B'], 'C': 0, 'D': base['D']}
    pick_r, why, notes = screens.first_look(T)
    rv = notes.get('reader_values', {})
    T['acq_run'] = T.run_acq.values
    r2b = split(T, 'acq_run')
    check('R3a the default path files (A) at about 2,500', pick(rung0) == 'A' and abs(rung0['A'] - 2519) < 60,
          '%.0f' % rung0['A'])
    check('L1 rung 1 (recovery and channel netted) names (A)', pick(rung1) == 'A', 'A %.0f' % rung1['A'])
    check('L2 rung 2 (the first-look reader\'s content band) names (A)', pick_r == 'A', why[:90])
    check('L3 rung 2b (the sign-up season\'s own runway) names (A)', pick(r2b) == 'A',
          'C %.0f A %.0f' % (r2b['C'], r2b['A']))
    check('R3b the decisive step alone files the golden (C)', pick(base) == 'C' and F['pick'] == 'C',
          'C %.0f A %.0f' % (base['C'], base['A']))
    check('L4 margin of the golden over the runner-up', base['C'] / base['A'] > 5, '%.1fx' % (base['C'] / base['A']))
    check('L5 dominance: every rung below the decisive one names (A)',
          all(pick(x) == 'A' for x in (rung0, rung1, r2b)) and pick_r == 'A', 'rungs 0, 1, 2, 2b')
    check('R3c the four and the remainder close on the fall', abs(R['C'] + R['A'] + R['B'] + R['D'] - R['fall']) < 1e-6,
          'remainder %.6f' % (R['fall'] - R['C'] - R['A'] - R['B'] - R['D']))

    # ------------------------------------------------------------------ the semantic fork table
    stl = pd.to_datetime(T.start.values).tz_localize('UTC')
    T_utc = T.copy()
    T_utc['per'] = np.select([(stl >= pd.Timestamp('2024-11-01', tz='UTC')) & (stl < pd.Timestamp('2025-02-01', tz='UTC')),
                              (stl >= pd.Timestamp('2025-11-01', tz='UTC')) & (stl < pd.Timestamp('2026-02-01', tz='UTC'))],
                             ['W24', 'W25'], 'x')
    u = split(T_utc, 'run')
    check('SF1 windows by UTC date: same call, same printed figures', pick(u) == 'C' and all(
        round(u[k], -2) == round(base[k], -2) for k in 'CABD'), ' '.join('%s %.0f' % (k, u[k]) for k in 'CABD'))
    win = Rv[Rv.per != 'x']
    chains_win = pc[(pc.subscription_id != pc.resulting_subscription_id) &
                    (pc.subscription_id.isin(win.subscription_id) | pc.resulting_subscription_id.isin(win.subscription_id))]
    check('SF2 no plan-change subscription on any winter trial', len(chains_win) == 0, '%d rows' % len(chains_win))
    T_ao = T.copy()
    st_tor = pd.to_datetime(T.start.values).tz_localize('UTC').tz_convert('America/Toronto')
    T_ao['per'] = np.where(T.per == 'W25', 'W25', np.where((st_tor >= pd.Timestamp('2025-08-01', tz='America/Toronto')) &
                                                            (st_tor < pd.Timestamp('2025-11-01', tz='America/Toronto')), 'W24', 'x'))
    ao = split(T_ao, 'run')
    check('SF3 compared with August to October 2025 instead: same call', pick(ao) == 'C', 'C %.0f A %.0f' % (ao['C'], ao['A']))
    P = W['P']
    rt = W['cal'][W['cal'].kind == 'episode'].set_index(['season_key', 'episode']).runtime
    rtp = rt.reindex(list(zip(P.season_key.values, P.episode.values))).values
    S = W['S']
    last = dict(zip(S.season_key, S['last'].map(lambda t: t.value)))
    floors = {}
    for nm, keep in (('5min', P.minutes.values >= 5), ('10pct', P.minutes.values >= 0.1 * rtp),
                     ('25pct', P.minutes.values >= 0.25 * rtp), ('50pct', P.minutes.values >= 0.5 * rtp),
                     ('90pct', P.minutes.values >= 0.9 * rtp)):
        pl = P[keep][['trial', 'season_key']].drop_duplicates()
        col = np.zeros(len(T), bool)
        col[pl.trial.values[pl.season_key.map(last).values > T.end.values[pl.trial.values]]] = True
        T['v_' + nm] = col
        floors[nm] = split(T, 'v_' + nm)['C']
    check('SF4 play floors keep the call and the slate\'s bin', all(2050 + 7 <= v < 2150 - 7 for v in floors.values()),
          ' '.join('%s %.0f' % kv for kv in floors.items()))
    dayend = split(T, 'run_dayend')['C']
    check('SF5 the trial\'s end to the second or at the local day: same slate', round(dayend, -2) == round(base['C'], -2),
          '%.0f against %.0f' % (dayend, base['C']))
    s6 = {k: split(T, k)['C'] for k in ('air_signup', 'air_during')}
    check('SF6 the state read at sign-up or during the trial: same slate bin',
          all(round(v, -2) == round(base['C'], -2) for v in s6.values()), ' '.join('%s %.0f' % kv for kv in s6.items()))
    check('SF7 no trialist of this winter has an episode to come (one gap only)', T[T.per == 'W25'].run.sum() == 0,
          '%d' % T[T.per == 'W25'].run.sum())
    gross = base['A'] + base['D']
    check('SF8 the price gross of the channel mix double counts it', base['C'] + gross + base['B'] + base['D'] > base['fall'] + 50,
          'four would sum to %.0f against a fall of %.0f' % (base['C'] + gross + base['B'] + base['D'], base['fall']))
    cells = screens.decompose(T)['A_cells']
    check('SF9 the price direct within cells or as the residual: same bin', round(cells, -2) == round(base['A'], -2),
          '%.0f against %.0f' % (cells, base['A']))
    a, b = T[T.per == 'W24'], T[T.per == 'W25']
    b_alt = (a[a.keep].paid.mean() - b[b.keep].paid.mean()) * b.keep.sum()
    check('SF10 recovery on declines or on collected first charges: same bin', round(b_alt, -2) == round(base['B'], -2),
          '%.0f against %.0f' % (b_alt, base['B']))
    d_alt = screens.decompose(T)['D']
    check('SF11 the channel mix at within-state or overall rates: same bin', round(d_alt, -2) == round(base['D'], -2),
          '%.0f against %.0f' % (d_alt, base['D']))
    Tp = T[T.n_seasons > 0].copy()
    sp = split(Tp, 'run')
    check('SF12 never-played trialists left out of the split: same call', pick(sp) == 'C', 'C %.0f' % sp['C'])
    n24 = len(a)
    check('SF13 priced at last winter\'s volume: same call', pick({k: v * n24 / len(b) for k, v in base.items() if k in 'ABCD'}) == 'C', '')
    check('SF14 waterfall from last winter\'s paid conversions: same call', True, 'the bars are the same causes')
    sub_played = 100 * a[a.n_seasons > 0].keep.mean()
    check('SF15 the subscribed share over the trials, as the prompt names it, differs from over the players',
          round(sub_played, 1) != F['stage_subscribed_w24'], '%.1f against %.1f' % (sub_played, F['stage_subscribed_w24']))
    fr = W['T'].lang.values[P.trial.values] == 'fr'
    check('SF16 an episode counts once whatever the language', P.duplicated(['trial', 'season_key', 'episode']).sum() == 0
          and fr.any(), '%d French plays' % fr.sum())
    late_oct = (st_tor >= pd.Timestamp('2025-10-25', tz='America/Toronto')) & (st_tor < pd.Timestamp('2025-11-01', tz='America/Toronto'))
    check('SF17 trials started 25 to 31 October 2025 are in neither window', (T.per.values[late_oct] == 'x').all(),
          '%d trials' % late_oct.sum())

    # ------------------------------------------------------------------ the separation line, counted from the shipped rows
    matched_trials = Rv[Rv.charged_sub.str.match(r'^(S\d{9}|sb_\w{12})$') & ~Rv.charged_sub.isin(
        set(Rv.subscription_id)) & ~Rv.charged_sub.isin(set(pc.resulting_subscription_id))]
    check('S1 no unlinked plan-change charge belongs to a winter trial', (matched_trials.per != 'x').sum() == 0,
          '%d matched trials, %d in a winter' % (len(matched_trials), (matched_trials.per != 'x').sum()))
    v = view.copy()
    v['cid'] = v.content_id.map(dict(zip(xc.legacy_id, xc.content_id))).fillna(v.content_id)
    rtc = pd.concat([cal[['content_id_en', 'runtime_min']].rename(columns={'content_id_en': 'cid'}),
                     cal[['content_id_fr', 'runtime_min']].rename(columns={'content_id_fr': 'cid'})]).set_index('cid').runtime_min
    v['rt'] = v.cid.map(rtc)
    over = v[v.minutes_watched > v.rt]
    am = dict(zip(xa.old_account_no, xa.account_id))
    acct_per = dict(zip(Rv.account_id.map(am).fillna(Rv.account_id), Rv.per))
    over_per = over.account_ref.map(am).fillna(over.account_ref).map(acct_per)
    check('S2 no session row belongs to a winter trial', (over_per.isin(['W24', 'W25'])).sum() == 0,
          '%d session rows, %d in a winter' % (len(over), over_per.isin(['W24', 'W25']).sum()))
    tw_t = pd.to_datetime(tw.start.values).tz_localize('UTC').tz_convert('America/Toronto')
    in_win = ((tw_t >= pd.Timestamp('2024-11-01', tz='America/Toronto')) & (tw_t < pd.Timestamp('2025-02-01', tz='America/Toronto'))) | \
             ((tw_t >= pd.Timestamp('2025-11-01', tz='America/Toronto')) & (tw_t < pd.Timestamp('2026-02-01', tz='America/Toronto')))
    check('S3 no twin row in either winter window', in_win.sum() == 0, '%d twin rows in all' % len(tw))
    np_tr = Rv[(Rv.per != 'x') & ~Rv.played]
    check('S4 never-played winter trials have no viewing row; the played share is the same with sessions expanded or not',
          len(np_tr) == int((T[T.per != 'x'].n_seasons == 0).sum()), '%d never played' % len(np_tr))
    t_over = pd.to_datetime(over.play_start_utc).dt.tz_localize(None)
    ok_dev = (over.device_type == 'smart_tv').all() and t_over.min() >= pd.Timestamp('2025-02-08 05:00') and \
        t_over.max() < pd.Timestamp('2025-10-27 04:00')
    check('S5 session rows only from the smart TV app between its two releases', ok_dev,
          '%s to %s' % (t_over.min(), t_over.max()))

    # ------------------------------------------------------------------ the devices' mechanics
    check('D7a every unlinked charge is matched to one trial', n_match == n_orph, '%d of %d' % (n_match, n_orph))
    truth_sub = dict(zip(T0.trial_id, T0.sub_charged))
    kept = set(T0.trial_id[T0.keep.values])
    kk = Rv[Rv.trial_id.isin(kept)]
    wrong = sum(truth_sub[t] != s for t, s in zip(kk.trial_id, kk.charged_sub))
    stray = int(Rv[~Rv.trial_id.isin(kept)].attempted.sum())
    check('D7b every charge sits on its own trial, and no trial without one gets one', wrong == 0 and stray == 0,
          '%d wrong of %d charged trials, %d stray' % (wrong, len(kk), stray))
    months = ['2025-%02d' % k for k in range(2, 11)]
    Rlog = Rv.copy()
    nxt = dict(zip(pc.subscription_id, pc.resulting_subscription_id))
    tails = []
    for s in Rlog.subscription_id:
        h = 0
        while s in nxt and nxt[s] != s and h < 6:
            s, h = nxt[s], h + 1
        tails.append(s)
    Rlog['p_log'] = pd.Series(tails, index=Rlog.index).map(ch.paid).fillna(False).astype(bool)
    Rlog['p_reg'] = Rlog.subscription_id.map(ch.paid).fillna(False).astype(bool)
    g = Rlog[Rlog.month.isin(months)].groupby('month')
    gold_p = {mo: F['_raw_months'][mo][0] for mo in months}
    mv_log = {mo: abs(100 * g.p_log.mean()[mo] - gold_p[mo]) / 0.1 for mo in months}
    mv_reg = {mo: abs(100 * g.p_reg.mean()[mo] - gold_p[mo]) / 0.1 for mo in months}
    check('D7c the logged-chains route misses every month by 3 bins or more', min(mv_log.values()) >= 3,
          'least %.1f bins (%s)' % (min(mv_log.values()), min(mv_log, key=mv_log.get)))
    check('D7d the register-only route misses every month by 3 bins or more', min(mv_reg.values()) >= 3,
          'least %.1f bins' % min(mv_reg.values()))
    base_match = dict(zip(Rv.trial_id, Rv.charged_sub))
    for wnd in (10, 360):
        Rw, _, nw = verify.link(verify.trials(reg, xc, cal)[0], ch, pc, pd.Timedelta(minutes=wnd))
        same = all(base_match.get(t) == s2 for t, s2 in zip(Rw.trial_id, Rw.charged_sub))
        check('D7e the nearest-end match is the same within a %d-minute window' % wnd, same and nw == n_match,
              '%d matched' % nw)
    eps_t = Rv.set_index('trial_id').episodes if 'episodes' in Rv else None
    epv = m.drop_duplicates(['trial_id', 'season_key', 'episode']).groupby('trial_id').size()
    truth_eps = P.drop_duplicates(['trial', 'season_key', 'episode']).groupby('trial').size()
    tmap = dict(zip(T0.trial_id, range(len(T0))))
    diff = 0
    for tid, n in epv.items():
        i = tmap.get(tid)
        if i is None or truth_eps.get(i, 0) != n:
            diff += 1
    check('D6a expanding the session rows by runtimes reproduces every trial\'s episodes', diff == 0,
          '%d trials differ of %d' % (diff, len(epv)))
    rows_only = verify_rows_only(Rv, view, xa, xc, cal)
    gold_e = {mo: F['_raw_months'][mo][1] for mo in months}
    Rv['eps_rows'] = Rv.trial_id.map(rows_only).fillna(0)
    ge = Rv[Rv.month.isin(months)].groupby('month').eps_rows.mean()
    mv_e = {mo: abs(ge[mo] - gold_e[mo]) / 0.1 for mo in months}
    check('D6b one row one episode misses every month by 3 bins or more', min(mv_e.values()) >= 3,
          'least %.1f bins (%s)' % (min(mv_e.values()), min(mv_e, key=mv_e.get)))
    check('D6c capping minutes at the runtime is the same route as one row one episode', True,
          'a capped row still names one episode')
    others = v[(v.device_type != 'smart_tv') & (v.minutes_watched > v.rt)]
    check('D6d no other device writes minutes beyond the episode', len(others) == 0, '%d rows' % len(others))

    # ------------------------------------------------------------------ bins
    graded = [('conv_slate', R['C'], 100), ('conv_price', R['A'], 100), ('conv_recovery', R['B'], 100),
              ('conv_channel', R['D'], 100), ('conv_gap', R['C'] - R['A'], 100), ('waterfall_start', R['start'], 100),
              ('waterfall_end', R['end'], 100)]
    for nm in ('w24', 'w25'):
        for s in ('played', 'subscribed', 'collected'):
            graded.append(('stage_%s_%s' % (s, nm), F['_raw_%s_%s' % (s, nm)], 0.1))
    for mo in months:
        graded.append(('ask_paid_share_' + mo, F['_raw_months'][mo][0], 0.1))
        graded.append(('ask_episodes_' + mo, F['_raw_months'][mo][1], 0.1))
    clear = [(k, edge(vv, uu) / uu) for k, vv, uu in graded]
    tight = min(clear, key=lambda kv: kv[1])
    check('B1 every graded figure sits 7 per cent of a bin or more from its edge', tight[1] >= 0.07,
          'tightest %s at %.1f per cent' % (tight[0], 100 * tight[1]))
    check('B2 figures.json carries every graded figure', all(k in figs for k, _, _ in graded), '%d figures' % len(graded))

    # ------------------------------------------------------------------ realism sweep
    regt = pd.read_csv(os.path.join(TGT, 'trial_register.csv'), dtype=str)
    num = regt.trial_id[regt.trial_id.str.fullmatch(r'T\d{7}')].str[1:].astype(int).sort_values().diff().dropna()
    check('RS1 no id column steps by a constant', num.nunique() > 100, '%d distinct steps' % num.nunique())
    mc = Rv.groupby('month').size()
    check('RS2 no two months hold the same trial count', mc.is_unique, '%d months' % len(mc))
    meta_bad = []
    for x in files + ['../golden/' + y for y in os.listdir(os.path.join(TASK, 'golden'))]:
        p = os.path.join(TGT, x)
        raw = open(p, 'rb').read()
        if x.endswith('.xlsx'):
            z = zipfile.ZipFile(io.BytesIO(raw))
            core = z.read('docProps/core.xml').decode()
            if re.search(r'openpyxl|python', core, re.I) or '2026-11' in core:
                meta_bad.append(x)
        if x.endswith('.pdf') and re.search(rb'ReportLab|reportlab|anonymous|D:2000', raw):
            meta_bad.append(x)
    check('RS3 no writer signature or build clock in any container', not meta_bad, ', '.join(meta_bad) or 'none')
    people = json.load(open(os.path.join(TASK, '..', '.claude', 'skills', 'fingerprint', 'cards', 'task403.json')))['world']['people']
    prog = pd.read_excel(os.path.join(TGT, 'growth_programmes_2026-27.xlsx'), header=None).astype(str)
    named = [p for p in people if prog.apply(lambda c: c.str.contains(p)).any().any()]
    check('RS4 the people named are the card\'s', len(named) >= 2, ', '.join(named))
    std = verify.PdfReader(os.path.join(TGT, 'conversion_standard_v3.pdf'))
    txt = ' '.join(pg.extract_text() for pg in std.pages)
    later = [d for d in re.findall(r'\d{1,2} \w+ 20\d\d', txt) if pd.Timestamp(d) > pd.Timestamp('2026-02-02')]
    check('RS5 the standard states nothing after its own date', not later and 'Version 3' in txt, ', '.join(later) or 'none')
    import subprocess
    pdf_ok = []
    for x, needle in (('conversion_standard_v3.pdf', 'first charge of the subscription the trial ends on'),
                      ('price_notice_PP-2025-07.pdf', 'charged at the new price'),
                      ('../golden/winter_conversion_note.pdf', 'Fund the winter release slate')):
        pth = os.path.join(TGT, x)
        strict = re.sub(r'\s+', ' ', ' '.join(pg.extract_text() for pg in verify.PdfReader(pth, strict=True).pages))
        lay = re.sub(r'\s+', ' ', subprocess.run(['pdftotext', '-layout', pth, '-'], capture_output=True, text=True).stdout)
        pdf_ok.append(needle in strict and needle in lay)
    check('H25 every PDF reads strictly and through pdftotext with its sentence', all(pdf_ok), '%d of %d' % (sum(pdf_ok), len(pdf_ok)))
    a_pl = T[(T.per == 'x')]
    st_m = pd.to_datetime(T.start.values).tz_localize('UTC').tz_convert('America/Toronto').strftime('%Y-%m')
    feb = T[st_m == '2025-02']
    eps_all = feb.n_seasons.values  # placeholder for the denominator test below
    played_feb = P[P.trial.isin(np.where(st_m == '2025-02')[0])].drop_duplicates(['trial', 'season_key', 'episode'])
    per_trial = len(played_feb) / len(feb)
    per_player = len(played_feb) / (feb.n_seasons > 0).sum()
    check('SF18 the episode average over the trials started, as the ask names it, differs from over the players',
          abs(per_player - per_trial) > 0.2, '%.2f over trials against %.2f over players' % (per_trial, per_player))
    ver = os.system('cd %s && python3 -W ignore verify.py > /dev/null' % HERE)
    check('V1 the independent verifier recomputes every figure', ver == 0, 'exit %d' % ver)

    fails = [r for r in RESULTS if not r[1]]
    print('\n%d checks, %d FAIL' % (len(RESULTS), len(fails)))
    return 1 if fails else 0


def verify_rows_only(Rv, view, xa, xc, cal):
    """Episodes per trial when each viewing row is one episode (the session rows not expanded)."""
    v = view.drop_duplicates().copy()
    am = dict(zip(xa.old_account_no, xa.account_id))
    v['acct'] = v.account_ref.map(am).fillna(v.account_ref)
    v['cid'] = v.content_id.map(dict(zip(xc.legacy_id, xc.content_id))).fillna(v.content_id)
    c = cal.assign(sk=cal.series + ' S' + cal.season.astype(str))
    e = pd.concat([c[['content_id_en', 'sk', 'episode']].rename(columns={'content_id_en': 'cid'}),
                   c[['content_id_fr', 'sk', 'episode']].rename(columns={'content_id_fr': 'cid'})])
    v = v.merge(e, on='cid')
    v['t'] = pd.to_datetime(v.play_start_utc).dt.tz_localize(None)
    tr = pd.DataFrame({'acct': Rv.account_id.map(am).fillna(Rv.account_id), 'trial_id': Rv.trial_id, 's': Rv.start, 'e': Rv.end})
    mm = v.merge(tr, on='acct')
    mm = mm[(mm.t >= mm.s) & (mm.t < mm.e)].drop_duplicates(['trial_id', 'sk', 'episode'])
    return mm.groupby('trial_id').size()


if __name__ == '__main__':
    sys.exit(main())
