"""task403 screens on the clean truth: the golden decomposition under every convention a solver could defend, the
default path, and the first-look reader, run on one world or over redraws.

    python3 screens.py            # the build world, with every table
    python3 screens.py 20         # 20 redraws (seeds 1..20): the first-look reader and the golden family

The first-look reader is the coordinator's medium-effort analyst. It reads every file, tabulates the outcome by
trial-start week, lays every candidate's own dated record beside the series (the price notice, the processor
switch, the paid social campaign, the release calendar's premieres and finales), runs a before-and-after on each
date, and runs the reflex segmentations: plan, device, channel, province, language, acquisition title, the
acquisition title's airing status and age at sign-up, the most-watched title and its age at sign-up, the release
type (weekly for every title, so constant), and the engagement bands (minutes, seasons, viewing days). It reads any
cell holding at least 200 trials in each winter. It never sets a trialist's viewing against the release calendar's
dates around the trial itself: that relation, at sign-up, during the trial or at day 7, is the decisive family.

Its rule: book to C the largest share of the fall that the mix of any content band explains, to D the channel mix,
to B the recovery change, and the rest to A; before that, a content band whose readable segments show the fall
absent (under a quarter of it) in a segment holding a fifth or more of the 2025-26 trials books the fall to C.
"""
import sys
import numpy as np
import pandas as pd
import warnings
import world

warnings.filterwarnings('ignore')
TOR = 'America/Toronto'
DAY = world.DAY
FLOOR = 200


def frame(W):
    T = W['T'].copy()
    P = W['P']
    S = W['S']
    st = pd.to_datetime(T.start.values).tz_localize('UTC').tz_convert(TOR)
    T['per'] = np.select([(st >= pd.Timestamp('2024-11-01', tz=TOR)) & (st < pd.Timestamp('2025-02-01', tz=TOR)),
                          (st >= pd.Timestamp('2025-11-01', tz=TOR)) & (st < pd.Timestamp('2026-02-01', tz=TOR))],
                         ['W24', 'W25'], 'x')
    T['week'] = (st.tz_localize(None).normalize() - pd.to_timedelta(st.dayofweek, unit='D')).strftime('%Y-%m-%d')
    first = dict(zip(S.season_key, S['first'].map(lambda t: t.value)))
    last = dict(zip(S.season_key, S['last'].map(lambda t: t.value)))
    T['acq_airing'] = (T.start.values >= T.acq_key.map(first).values) & (T.start.values <= T.acq_key.map(last).values)
    T['acq_catalogue'] = T.start.values > T.acq_key.map(last).values
    T['acq_age'] = (T.start.values - T.acq_key.map(first).values) / DAY
    # viewing summaries (runway-free)
    agg = P.groupby('trial').agg(minutes=('minutes', 'sum'), seasons=('season_key', 'nunique'))
    vd = P.assign(d=(P.play_utc.values - T.start.values[P.trial.values]) // DAY).groupby('trial').d.nunique()
    T['minutes'] = agg.minutes.reindex(T.index).fillna(0).values
    T['seasons'] = agg.seasons.reindex(T.index).fillna(0).astype(int).values
    T['vdays'] = vd.reindex(T.index).fillna(0).astype(int).values
    top = (P.groupby(['trial', 'season_key']).minutes.sum().reset_index()
           .sort_values(['trial', 'minutes', 'season_key']).groupby('trial').tail(1).set_index('trial').season_key)
    T['top'] = top.reindex(T.index).fillna('none').values
    T['top_age'] = (T.start.values - T.top.map(first).fillna(np.inf).values) / DAY
    for k in (28, 56, 91):
        T['acq_new%d' % k] = T.acq_age.values <= k
        T['top_new%d' % k] = T.top_age.values <= k
    T['min_band'] = pd.cut(T.minutes, [-1, 0, 60, 180, 400, 1e9], labels=['0', '1-60', '61-180', '181-400', '400+']).astype(str)
    T['seas_band'] = np.minimum(T.seasons, 3)
    T['vday_band'] = np.minimum(T.vdays, 5)
    T['release_type'] = 'weekly'
    # the decisive family: viewing set against the calendar around each trial
    pl = P[['trial', 'season_key']].drop_duplicates()
    full = P[P.minutes.values >= 0.9 * 1]  # placeholder, replaced below with the runtime test
    tr = pl.trial.values
    f = pl.season_key.map(first).values
    l = pl.season_key.map(last).values
    s0, e0 = T.start.values[tr], T.end.values[tr]
    # the trial's last local day against each release's local day (a release on a later day than the trial's last)
    endday = pd.to_datetime(T.end.values).tz_localize('UTC').tz_convert(TOR).normalize() + pd.Timedelta(days=1)
    endday = endday.tz_convert('UTC').asi8 - 1
    variants = {
        'run': l > e0,                                   # an episode of a played season released after the trial's end
        'run_dayend': l > endday[tr],                    # ... on a later local day than the trial's last
        'air_signup': (f <= s0) & (l >= s0),             # a played season airing when the trial started
        'air_during': (f <= e0) & (l >= s0),             # a played season airing at any point of the trial
    }
    for k, v in variants.items():
        col = np.zeros(len(T), bool)
        col[tr[v]] = True
        T[k] = col
    # full-episode plays only (90 per cent of the runtime or more)
    cal = W['cal']
    rt = cal[cal.kind == 'episode'].set_index(['season_key', 'episode']).runtime
    r = rt.reindex(list(zip(P.season_key.values, P.episode.values))).values
    pf = P[P.minutes.values >= 0.9 * r][['trial', 'season_key']].drop_duplicates()
    col = np.zeros(len(T), bool)
    col[pf.trial.values[pf.season_key.map(last).values > T.end.values[pf.trial.values]]] = True
    T['run_full'] = col
    # acquisition season only
    T['run_acq'] = T.acq_key.map(last).values > T.end.values
    return T


def mixsplit(a, b, col, w='w24'):
    """The 2025-26 trials' paid conversions lost to the shift in col's mix, and the within-state change."""
    n25 = len(b)
    r24, r25 = a[col].mean(), b[col].mean()
    p24 = a.groupby(col).paid.mean()
    p25 = b.groupby(col).paid.mean()
    g25 = p25.get(True, np.nan) - p25.get(False, np.nan)
    g24 = p24.get(True, np.nan) - p24.get(False, np.nan)
    gap = {'w25': g25, 'w24': g24, 'mean': (g25 + g24) / 2}[w]
    if not np.isfinite(gap):
        gap = g24
    return (r24 - r25) * gap * n25


def decompose(T):
    """Each programme's paid conversions for the 2025-26 winter trials, under each convention.

    C, the slate: the shift in the runway share times the paid-rate gap between the states (2025-26 gap, literal:
    the winter's trials with last winter's slate, everything else as it was; variants at last winter's gap and the
    mean, and under each operationalisation of the state).
    A, the price: the change in the keep rate inside each runway state and channel, at 2025-26's mix, times
    2025-26's collection rate; variant inside runway state only; variant as the residual.
    B, recovery: the change in the share of declined first charges recovered, on 2025-26's declined charges.
    D, the channel mix: last winter's channel shares at 2025-26 keep rates inside each runway state.
    """
    a, b = T[T.per == 'W24'], T[T.per == 'W25']
    n25 = len(b)
    out = {'n25': n25, 'n24': len(a)}
    for col in ('run', 'run_dayend', 'run_full', 'run_acq', 'air_signup', 'air_during'):
        out['C_%s' % col] = mixsplit(a, b, col)
    out['C_w24gap'] = mixsplit(a, b, 'run', 'w24')
    out['C_meangap'] = mixsplit(a, b, 'run', 'mean')
    out['n25_run'] = int(b.run.sum())
    col25 = b[b.keep].paid.mean()
    ka = a.groupby(['run', 'channel']).keep.mean(); kb = b.groupby(['run', 'channel']).keep.mean()
    nb = b.groupby(['run', 'channel']).size()
    idx = ka.index.intersection(kb.index)
    out['A_cells'] = float(((ka[idx] - kb[idx]) * nb[idx]).sum()) * col25
    k24 = a.groupby('run').keep.mean(); k25 = b.groupby('run').keep.mean()
    out['A_run'] = float(((k24 - k25) * b.groupby('run').size()).sum()) * col25
    d24, d25 = a[a.declined], b[b.declined]
    out['B'] = (d24.recovered.mean() - d25.recovered.mean()) * len(d25)
    s24 = a.groupby('channel').size() / len(a); s25 = b.groupby('channel').size() / len(b)
    kc = b.groupby(['run', 'channel']).keep.mean().unstack()
    rs = b.groupby('run').size() / len(b)
    eff = sum(rs[rv] * ((s24 - s25) * kc.loc[rv]).sum() for rv in kc.index)
    out['D'] = eff * col25 * n25
    pc = b.groupby('channel').paid.mean()
    out['D_overall'] = float(((s24 - s25) * pc).sum()) * n25
    out['fall'] = (a.paid.mean() - b.paid.mean()) * n25
    out['A_resid'] = out['fall'] - out['C_run'] - out['B'] - out['D']
    out['r24'], out['r25'] = a.run.mean(), b.run.mean()
    return out


CONTENT = ['acq_key', 'acq_airing', 'acq_new28', 'acq_new56', 'acq_new91', 'top', 'top_new28', 'top_new56',
           'top_new91', 'release_type', 'min_band', 'seas_band', 'vday_band']
OTHER = ['plan0', 'device', 'channel', 'prov', 'lang']


def band(a, b, col):
    """Readable segments of col (FLOOR trials or more in each winter): each one's fall, the mix share of the fall."""
    na, nb = a[col].value_counts(), b[col].value_counts()
    keep = [k for k in na.index if na[k] >= FLOOR and nb.get(k, 0) >= FLOOR]
    if len(keep) < 2:
        return 0.0, {}, keep
    aa, bb = a[a[col].isin(keep)], b[b[col].isin(keep)]
    sa = aa.groupby(col).paid.agg(['mean', 'size']); sb = bb.groupby(col).paid.agg(['mean', 'size'])
    wa = sa['size'] / sa['size'].sum(); wb = sb['size'] / sb['size'].sum()
    comp = float(((wa - wb) * (sa['mean'] + sb['mean']) / 2).sum())
    f = aa.paid.mean() - bb.paid.mean()
    falls = {k: 100 * (sa['mean'][k] - sb['mean'][k]) for k in keep}
    shares = {k: float(wb[k]) for k in keep}
    return (comp / f if f else 0.0), falls, shares


def first_look(T):
    X = T[T.per != 'x']
    a, b = X[X.per == 'W24'], X[X.per == 'W25']
    fall = a.paid.mean() - b.paid.mean()
    n25 = len(b)
    D_ = lambda s: pd.Timestamp(s, tz=TOR).tz_convert('UTC').value
    # each candidate's own dated record, as the trial-start date whose first charge or decision it first touches
    dates = {'A price notice': D_('2025-10-25'), 'B processor switch': D_('2025-09-01'),
             'C autumn finales': D_('2025-10-24'),
             'D social campaign': D_('2025-11-03')}
    steps = {}
    for k, d in dates.items():
        bef = T[(T.start >= d - 28 * DAY) & (T.start < d)].paid.mean()
        aft = T[(T.start >= d) & (T.start < d + 28 * DAY)].paid.mean()
        steps[k] = 100 * (bef - aft)
    notes = {'fall_pts': round(100 * fall, 2), 'steps': {k: round(v, 2) for k, v in steps.items()}}
    best_c, best_col = 0.0, None
    for col in CONTENT + OTHER:
        share, falls, segs = band(a, b, col)
        notes[col] = (round(share, 3), {k: round(v, 1) for k, v in falls.items()})
        if col in CONTENT and falls:
            if share > best_c:
                best_c, best_col = share, col
            lo_k = min(falls, key=falls.get)
            if falls[lo_k] <= 25 * fall and segs.get(lo_k, 0) >= 0.2:
                return 'C', 'fall absent in %s=%s (%.1f of %.1f)' % (col, lo_k, falls[lo_k], 100 * fall), notes
    ch_share = notes['channel'][0]
    rec = 100 * (a[a.declined].recovered.mean() - b[b.declined].recovered.mean()) * b.declined.mean()
    C_r = max(best_c, 0) * fall
    D_r = max(ch_share, 0) * fall
    B_r = rec / 100
    A_r = fall - C_r - D_r - B_r
    vals = {'A': A_r * n25, 'B': B_r * n25, 'C': C_r * n25, 'D': D_r * n25}
    notes['reader_values'] = {k: round(v) for k, v in vals.items()}
    notes['best_content_band'] = (best_col, round(best_c, 3))
    pick = max(vals, key=vals.get)
    return pick, 'decomposition by %s: %s' % (best_col, notes['reader_values']), notes


def weekly(T):
    X = T[(T.start >= world.ts('2025-08-01 00:00').value) & (T.start < world.ts('2026-02-01 00:00').value)]
    return X.groupby('week').paid.agg(['mean', 'size']).round(3)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    seeds = list(range(1, n + 1)) if n else [world.SEED]
    picks, rows = [], []
    for s in seeds:
        W = world.simulate(seed=s)
        T = frame(W)
        pick, why, notes = first_look(T)
        d = decompose(T)
        picks.append(pick)
        rows.append(d)
        print('seed %5d  reader %s (%s)' % (s, pick, why))
        print('   fall %.0f  C %.0f [dayend %.0f full %.0f acq %.0f signup %.0f during %.0f w24gap %.0f mean %.0f]  '
              'A %.0f/%.0f/resid %.0f  B %.0f  D %.0f/%.0f  runway %.3f->%.3f' % (
                  d['fall'], d['C_run'], d['C_run_dayend'], d['C_run_full'], d['C_run_acq'], d['C_air_signup'],
                  d['C_air_during'], d['C_w24gap'], d['C_meangap'], d['A_cells'], d['A_run'], d['A_resid'], d['B'],
                  d['D'], d['D_overall'], d['r24'], d['r25']), flush=True)
        if not n:
            for k, v in notes.items():
                print('    ', k, v)
            print(weekly(T).to_string())
    print('first-look reader picks:', pd.Series(picks).value_counts().to_dict())
    if n:
        R = pd.DataFrame(rows)
        print(R.describe().loc[['mean', 'min', 'max']].round(0).T.to_string())


if __name__ == '__main__':
    main()
