"""task403 screens on the clean truth: the golden decomposition under every convention a solver could defend, the
default path, and the first-look reader, run on one world or over redraws.

    python3 screens.py            # the build world
    python3 screens.py 20         # 20 redraws (seeds 1..20) of the first-look reader and the decomposition
"""
import sys
import numpy as np
import pandas as pd
import world

TOR = 'America/Toronto'


def frame(W):
    T = W['T'].copy()
    st = pd.to_datetime(T.start.values).tz_localize('UTC').tz_convert(TOR)
    T['per'] = np.select([(st >= pd.Timestamp('2024-11-01', tz=TOR)) & (st < pd.Timestamp('2025-02-01', tz=TOR)),
                          (st >= pd.Timestamp('2025-11-01', tz=TOR)) & (st < pd.Timestamp('2026-02-01', tz=TOR))],
                         ['W24', 'W25'], 'x')
    T['week'] = st.to_period('W').astype(str)
    S = W['S']
    first = dict(zip(S.season_key, S['first'].map(lambda t: t.value)))
    last = dict(zip(S.season_key, S['last'].map(lambda t: t.value)))
    T['acq_airing'] = (T.start.values >= T.acq_key.map(first).values) & (T.start.values <= T.acq_key.map(last).values)
    T['acq_catalogue'] = T.start.values > T.acq_key.map(last).values
    return T


def decompose(T):
    """Each programme's paid conversions for the 2025-26 winter trials, under each convention.

    C, the slate: the 2024-25 runway share at the 2025-26 runway gap (literal: the winter's trials with last winter's
    slate, everything else as it was); variants at last winter's gap and the mean gap.
    A, the price: the change in the keep rate inside each runway state, with the channel mix held at 2025-26's.
    B, recovery: the change in the share of declined first charges recovered, on 2025-26's declined charges.
    D, the channel mix: the 2024-25 channel shares at 2025-26 keep rates inside each runway state.
    """
    a, b = T[T.per == 'W24'], T[T.per == 'W25']
    n25 = len(b)
    out = {}
    r24, r25 = a.run.mean(), b.run.mean()
    col24 = a[a.keep].paid.mean(); col25 = b[b.keep].paid.mean()
    k24 = a.groupby('run').keep.mean(); k25 = b.groupby('run').keep.mean()
    p24 = a.groupby('run').paid.mean(); p25 = b.groupby('run').paid.mean()
    out['C_w25gap'] = (r24 - r25) * (p25[True] - p25[False]) * n25
    out['C_w24gap'] = (r24 - r25) * (p24[True] - p24[False]) * n25
    out['C_meangap'] = (out['C_w25gap'] + out['C_w24gap']) / 2
    # price: keep-rate change inside runway state and channel, at 2025-26's mix, times 2025-26's collection rate
    cells = ['run', 'channel']
    ka = a.groupby(cells).keep.mean(); kb = b.groupby(cells).keep.mean(); nb = b.groupby(cells).size()
    idx = ka.index.intersection(kb.index)
    out['A_cells'] = float(((ka[idx] - kb[idx]) * nb[idx]).sum()) * col25
    out['A_run'] = float(((k24 - k25) * b.groupby('run').size()).sum()) * col25
    # recovery: declined first charges recovered
    d24 = a[a.declined]; d25 = b[b.declined]
    out['B'] = (d24.recovered.mean() - d25.recovered.mean()) * len(d25)
    # channel mix at 2025-26 keep rates inside runway state
    s24 = a.groupby('channel').size() / len(a); s25 = b.groupby('channel').size() / len(b)
    kc = b.groupby(['run', 'channel']).keep.mean().unstack()
    rs = b.groupby('run').size() / len(b)
    eff = 0.0
    for rv in kc.index:
        eff += rs[rv] * ((s24 - s25) * kc.loc[rv]).sum()
    out['D'] = eff * col25 * n25
    out['fall'] = (a.paid.mean() - b.paid.mean()) * n25
    out['r24'], out['r25'], out['n25'] = r24, r25, n25
    return out


def first_look(T):
    """The coordinator's first-look reader: outcome by week, each candidate's date, a before-and-after on each,
    the reflex segmentations, and the content-neutral control. Returns its pick and its reasons."""
    X = T[T.per != 'x']
    a, b = X[X.per == 'W24'], X[X.per == 'W25']
    fall = a.paid.mean() - b.paid.mean()
    D = lambda s: pd.Timestamp(s, tz=TOR).tz_convert('UTC').value
    dates = {'A': D('2025-10-25'), 'B': D('2025-09-01'), 'C': D('2025-10-24'), 'D': D('2025-11-03')}
    steps = {}
    for k, d in dates.items():
        bef = T[(T.start >= d - 28 * world.DAY) & (T.start < d)].paid.mean()
        aft = T[(T.start >= d) & (T.start < d + 28 * world.DAY)].paid.mean()
        steps[k] = bef - aft
    notes = {'fall': round(100 * fall, 2), 'steps': {k: round(100 * v, 2) for k, v in steps.items()}}
    seg_to_cand = {'channel': 'D', 'acq_key': 'C', 'acq_airing': 'C', 'device': None, 'plan0': None, 'prov': None,
                   'lang': None}
    for col, cand in seg_to_cand.items():
        common = set(a[col].unique()) & set(b[col].unique())
        aa, bb = a[a[col].isin(common)], b[b[col].isin(common)]
        sa = aa.groupby(col).paid.agg(['mean', 'size']); sb = bb.groupby(col).paid.agg(['mean', 'size'])
        wa = sa['size'] / sa['size'].sum(); wb = sb['size'] / sb['size'].sum()
        comp = ((wa - wb) * (sa['mean'] + sb['mean']) / 2).sum()
        f = aa.paid.mean() - bb.paid.mean()
        big = [k for k in sa.index if (a[col] == k).mean() >= 0.03 and (b[col] == k).mean() >= 0.03]
        falls = {k: round(100 * (sa['mean'][k] - sb['mean'][k]), 1) for k in big}
        notes[col] = (round(comp / f, 3) if f else 0.0, falls)
        if cand and f and comp / f >= 0.5:
            return cand, 'mix in %s explains %.0f%%' % (col, 100 * comp / f), notes
        if cand and len(big) >= 2:
            lo, hi = min(falls.values()), max(falls.values())
            if lo < 0.4 * 100 * fall and hi > 1.2 * 100 * fall:
                return cand, 'fall absent in a %s segment (%.1f against %.1f)' % (col, lo, hi), notes
    big = [k for k in steps if steps[k] >= 0.5 * fall]
    if 'A' in big and 'C' in big:
        cat_a, cat_b = a[a.acq_catalogue], b[b.acq_catalogue]
        cf = cat_a.paid.mean() - cat_b.paid.mean()
        notes['catalogue_control'] = round(100 * cf, 2)
        return ('A' if cf >= 0.6 * fall else 'C'), 'A and C coincide; catalogue control fell %.1f of %.1f' % (100 * cf, 100 * fall), notes
    if big:
        return max(big, key=lambda c: steps[c]), 'largest step', notes
    return max(steps, key=lambda c: steps[c]), 'no big step', notes


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    seeds = list(range(1, n + 1)) if n else [world.SEED]
    picks = []
    for s in seeds:
        W = world.simulate(seed=s)
        T = frame(W)
        pick, why, notes = first_look(T)
        d = decompose(T)
        picks.append(pick)
        print('seed %5d  reader %s (%s)  fall %.0f  C %.0f/%.0f/%.0f  A %.0f/%.0f  B %.0f  D %.0f  runway %.3f->%.3f' % (
            s, pick, why, d['fall'], d['C_w25gap'], d['C_w24gap'], d['C_meangap'], d['A_cells'], d['A_run'], d['B'], d['D'],
            d['r24'], d['r25']))
        if not n:
            for k, v in notes.items():
                print('   ', k, v)
    print('first-look reader picks:', pd.Series(picks).value_counts().to_dict())


if __name__ == '__main__':
    main()
