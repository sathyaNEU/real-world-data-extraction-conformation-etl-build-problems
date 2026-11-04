"""task403 independent verifier: reads only target/ (and figures.json to compare), recomputes every graded figure.

    python3 verify.py        # exit 0 when every figure recomputes at its printed precision
"""
import json
import os
import re
import sys
import numpy as np
import pandas as pd
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
TGT = os.path.join(os.path.dirname(HERE), 'target')
TOR = 'America/Toronto'
PRICES = (999, 1499, 1199, 1699)


def f(name):
    return os.path.join(TGT, name)


def load():
    reg = pd.read_csv(f('trial_register.csv'), dtype=str)
    view = pd.read_parquet(f('trial_viewing_2024-11_2026-02.parquet'))
    ca = pd.read_csv(f('charges_processor_a_2024-11_2025-09.csv'), dtype={'merchant_ref': str})
    cb = pd.read_csv(f('charges_processor_b_2025-09_2026-02.csv'), dtype={'merchant_reference': str})
    pc = pd.read_csv(f('plan_changes.csv'), dtype=str)
    xa = pd.read_csv(f('account_crosswalk.csv'), dtype=str)
    xc = pd.read_csv(f('content_crosswalk.csv'), dtype=str)
    cal = pd.read_excel(f('release_calendar.xlsx'), dtype={'content_id_en': str, 'content_id_fr': str})
    return reg, view, ca, cb, pc, xa, xc, cal


def trials(reg, xc, cal):
    """One row per trial. The old platform's rows after the cut-over carry Toronto wall-clock time with a Z; its copies
    of web and phone sign-ups match a new-platform row on every field once re-timed, and are dropped."""
    t = pd.to_datetime(reg.trial_start_utc.str.rstrip('Z'))
    old = reg.trial_id.str.fullmatch(r'T\d{7}')
    first_new = t[~old].min()
    late = old & (t >= first_new - pd.Timedelta(hours=4))
    loc = t[late].dt.tz_localize(TOR).dt.tz_convert('UTC').dt.tz_localize(None)
    t = t.copy()
    t[late] = loc
    page = reg.signup_page.map(dict(zip(xc.legacy_id, xc.content_id))).fillna(reg.signup_page)
    R = reg.assign(start=t, page=page)
    key = ['start', 'province', 'plan', 'signup_channel', 'signup_device', 'page', 'language']
    newrows = R[~old][key].assign(_n=1)
    m = R[late][key + ['trial_id']].merge(newrows, on=key, how='left')
    twins = set(m.loc[m._n.notna(), 'trial_id'])
    R = R[~R.trial_id.isin(twins)].copy()
    R['end'] = R.start + pd.Timedelta(days=7)
    loc = R.start.dt.tz_localize('UTC').dt.tz_convert(TOR)
    R['month'] = loc.dt.strftime('%Y-%m')
    R['per'] = np.select([(loc >= pd.Timestamp('2024-11-01', tz=TOR)) & (loc < pd.Timestamp('2025-02-01', tz=TOR)),
                          (loc >= pd.Timestamp('2025-11-01', tz=TOR)) & (loc < pd.Timestamp('2026-02-01', tz=TOR))],
                         ['W24', 'W25'], 'x')
    return R.reset_index(drop=True), len(twins)


def attempts(ca, cb):
    a = pd.DataFrame({'ref': ca.merchant_ref, 't': pd.to_datetime(ca.attempted_at_utc.str.rstrip('Z')),
                      'ok': ca.outcome.eq('approved'), 'cents': ca.amount_cents.astype(float), 'proc': 'a'})
    tb = pd.to_datetime(cb.created, utc=True).dt.tz_localize(None)
    b = pd.DataFrame({'ref': cb.merchant_reference, 't': tb, 'ok': cb.status.eq('CAPTURED'),
                      'cents': np.round(100 * cb.amount.astype(float)), 'proc': 'b',
                      'rate': (cb.tax_amount.astype(float) / cb.amount.astype(float)).round(4)})
    A = pd.concat([a, b], ignore_index=True)
    A['rate'] = A['rate'].where(A.proc == 'b')
    # first processor: the tax-inclusive cents give the rate on the one list price that fits
    for p in PRICES:
        r = A.cents / p - 1
        fit = (A.proc == 'a') & (r > 0.03) & (r < 0.17) & A.rate.isna()
        A.loc[fit, 'rate'] = r[fit]
    A['group'] = np.round(np.where((A.rate - 0.14975).abs() < 0.003, 0.15, A.rate), 2)
    g = A.sort_values('t').groupby('ref').agg(first=('t', 'min'), paid=('ok', 'max'), group=('group', 'first'))
    return g


def link(R, ch, pc, window=pd.Timedelta(hours=1)):
    nxt = dict(zip(pc.subscription_id, pc.resulting_subscription_id))
    ends = []
    for s in R.subscription_id:
        hops = 0
        while s in nxt and nxt[s] != s and hops < 6:
            s = nxt[s]
            hops += 1
        ends.append(s)
    R = R.assign(charged_sub=ends)
    R['charged'] = R.charged_sub.isin(ch.index)
    # each province's tax group, read off its linked charges (by period, for the April 2025 change)
    lk = R[R.charged].assign(group=R.loc[R.charged, 'charged_sub'].map(ch.group),
                             first=R.loc[R.charged, 'charged_sub'].map(ch['first']))
    lk['half'] = np.where(lk['first'] < pd.Timestamp('2025-04-01 04:00'), 'pre', 'post')
    pg = lk.groupby(['province', 'half']).group.agg(lambda s: s.mode().iloc[0])
    R['half'] = np.where(R.end < pd.Timestamp('2025-04-01 04:00'), 'pre', 'post')
    R['group'] = [pg.get((p, h), np.nan) for p, h in zip(R.province, R.half)]
    used = set(R.loc[R.charged, 'charged_sub'])
    orphans = ch[~ch.index.isin(used)].sort_values('first')
    free = R[~R.charged].sort_values('end')
    taken = {}
    for ref, o in orphans.iterrows():
        cand = free[(free.group == o.group) & (free.end <= o['first']) & (free.end > o['first'] - window)]
        cand = cand[~cand.trial_id.isin(taken.values())]
        if len(cand):
            taken[ref] = cand.iloc[-1].trial_id
    back = {v: k for k, v in taken.items()}
    R['charged_sub'] = np.where(R.trial_id.isin(back), R.trial_id.map(back), R.charged_sub)
    R['paid'] = R.charged_sub.map(ch.paid).fillna(False).astype(bool)
    R['attempted'] = R.charged_sub.isin(ch.index)
    return R, len(orphans), len(taken)


def plays(R, view, xa, xc, cal):
    v = view.drop_duplicates().copy()
    acct = dict(zip(xa.old_account_no, xa.account_id))
    v['acct'] = v.account_ref.map(acct).fillna(v.account_ref)
    v['content'] = v.content_id.map(dict(zip(xc.legacy_id, xc.content_id))).fillna(v.content_id)
    cal = cal.assign(season_key=cal.series + ' S' + cal.season.astype(str))
    ep = pd.concat([cal[['content_id_en', 'season_key', 'episode', 'runtime_min']].rename(columns={'content_id_en': 'content'}),
                    cal[['content_id_fr', 'season_key', 'episode', 'runtime_min']].rename(columns={'content_id_fr': 'content'})])
    v = v.merge(ep, on='content', how='left')
    assert v.season_key.notna().all()
    v['t'] = pd.to_datetime(v.play_start_utc).dt.tz_localize(None)
    # the smart TV app from 8 February to 27 October 2025 wrote one row per autoplay run: the episode named and the
    # season's following episodes, as many as the minutes reach on the calendar's runtimes
    lo, hi = pd.Timestamp('2025-02-08 05:00'), pd.Timestamp('2025-10-27 04:00')
    runtimes = {k: g.set_index('episode').runtime_min.to_dict() for k, g in cal.groupby('season_key')}
    run = (v.device_type == 'smart_tv') & (v.t >= lo) & (v.t < hi) & (v.minutes_watched > v.runtime_min)
    extra = []
    for r in v[run].itertuples():
        rt = runtimes[r.season_key]
        left, e = r.minutes_watched - r.runtime_min, r.episode + 1
        while left > 0 and e in rt:
            extra.append((r.acct, r.season_key, e, r.t))
            left -= rt[e]
            e += 1
    x = pd.DataFrame(extra, columns=['acct', 'season_key', 'episode', 't'])
    v = pd.concat([v[['acct', 'season_key', 'episode', 't']], x], ignore_index=True)
    acct_reg = R.account_id.map(acct).fillna(R.account_id)
    tr = pd.DataFrame({'acct': acct_reg, 'trial_id': R.trial_id, 'start': R.start, 'end': R.end})
    m = v.merge(tr, on='acct')
    m = m[(m.t >= m.start) & (m.t < m.end)]
    return m, int(run.sum())


def main():
    figs = json.load(open(os.path.join(HERE, 'figures.json')))
    reg, view, ca, cb, pc, xa, xc, cal = load()
    R, n_twins = trials(reg, xc, cal)
    ch = attempts(ca, cb)
    R, n_orph, n_matched = link(R, ch, pc)
    m, n_runs = plays(R, view, xa, xc, cal)
    eps = m.drop_duplicates(['trial_id', 'season_key', 'episode']).groupby('trial_id').size()
    R['episodes'] = R.trial_id.map(eps).fillna(0)
    R['played'] = R.trial_id.isin(set(m.trial_id))
    cal2 = cal.assign(season_key=cal.series + ' S' + cal.season.astype(str))
    lastrel = cal2.assign(t=pd.to_datetime(cal2.release_toronto).dt.tz_localize(TOR).dt.tz_convert('UTC').dt.tz_localize(None)
                          ).groupby('season_key').t.max()
    seas = m.drop_duplicates(['trial_id', 'season_key'])
    seas = seas[seas.season_key.map(lastrel).values > seas.end.values]
    R['run'] = R.trial_id.isin(set(seas.trial_id))
    a, b = R[R.per == 'W24'], R[R.per == 'W25']
    n25 = len(b)
    out = {}
    for nm, X in (('w24', a), ('w25', b)):
        out['stage_trials_%s' % nm] = len(X)
        out['stage_played_%s' % nm] = round(100 * X.played.mean(), 1)
        out['stage_subscribed_%s' % nm] = round(100 * X.attempted.mean(), 1)
        out['stage_collected_%s' % nm] = round(100 * X[X.attempted].paid.mean(), 1)
        out['paid_rate_%s' % nm] = round(100 * X.paid.mean(), 1)
    p24, p25 = a.paid.mean(), b.paid.mean()
    p24_norun = a[~a.run].paid.mean()
    C = (p24 - p24_norun) * n25
    within = (p24_norun - p25) * n25
    fa = ca.assign(ref=ca.merchant_ref).sort_values(['ref', 'attempt'])
    fb = cb.assign(ref=cb.merchant_reference).sort_values(['ref', 'retry_count'])
    dec = pd.concat([fa.groupby('ref').outcome.first().eq('declined'), fb.groupby('ref').status.first().eq('REFUSED')])
    R['declined'] = R.charged_sub.map(dec).fillna(False).astype(bool)
    a, b = R[R.per == 'W24'], R[R.per == 'W25']
    B = (a[a.declined].paid.mean() - b[b.declined].paid.mean()) * b.declined.sum()
    s24 = a.groupby('signup_channel').size() / len(a)
    s25 = b.groupby('signup_channel').size() / len(b)
    D = float(((s24 - s25) * b.groupby('signup_channel').paid.mean()).sum()) * n25
    A = within - B - D
    out['conv_slate'] = int(round(C, -2))
    out['conv_price'] = int(round(A, -2))
    out['conv_recovery'] = int(round(B, -2))
    out['conv_channel'] = int(round(D, -2))
    out['conv_gap'] = int(round(C - A, -2))
    out['conv_fall'] = int(round((p24 - p25) * n25, -2))
    out['waterfall_start'] = int(round(p24 * n25, -2))
    out['waterfall_end'] = int(round(b.paid.sum(), -2))
    vals = {'C': C, 'A': A, 'B': B, 'D': D}
    order = sorted(vals, key=vals.get, reverse=True)
    out['pick'], out['runner_up'] = order[0], order[1]
    M = R[R.month.isin(['2025-%02d' % k for k in range(2, 11)])]
    for mo, g in M.groupby('month'):
        out['ask_paid_share_%s' % mo] = round(100 * g.paid.mean(), 1)
        out['ask_episodes_%s' % mo] = round(g.episodes.mean(), 1)
    # the documents read back through one extractor, with a positive control each
    std = ' '.join(p.extract_text() for p in PdfReader(f('conversion_standard_v3.pdf')).pages)
    std = re.sub(r'\s+', ' ', std)
    assert 'its first charge is the first charge of the subscription the trial ends on' in std.replace('Its', 'its')
    assert 'whether the viewer started it or the player moved on to it from the episode before' in std
    bad = [k for k in out if k in figs and out[k] != figs[k]]
    for k in sorted(out):
        if k in figs:
            print('%-26s %-10s %-10s %s' % (k, out[k], figs[k], 'ok' if out[k] == figs[k] else 'DIFFERS'))
    print('twin rows dropped %d; unlinked charges %d, matched %d; session rows expanded %d' % (n_twins, n_orph, n_matched, n_runs))
    if bad:
        print('VERIFY FAIL:', bad)
        return 1
    print('VERIFY PASS: %d figures recomputed from target/' % len([k for k in out if k in figs]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
