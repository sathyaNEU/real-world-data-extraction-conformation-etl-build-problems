"""task403 ask ceiling, measured on the cut pack. Shares no code with the generator or the verifier: it reads target/
and the golden figures in generator/figures.json, executes the responses' routes for the ask as code, and scores them.

    python3 ceiling.py

The full includer (the cracker): a blind medium-effort reader who lands the call, reads every file and every filed
sentence and runs the hygiene battery. It drops exact duplicate rows, converts every clock, maps legacy numbers
through both crosswalks, matches the old platform's June copies to their new-platform rows on the re-timed clock and
keeps the TV and tablet sign-ups only the old platform wrote, follows every change the plan-change log records to the
charge it produced (the standard files that a plan change keeps the trial), and counts an episode for each viewing row
it attributes to a trial (the standard files that an autoplay start counts, and a row names an episode). It does not
invent a match for a charge no file links to a trial, and it does not read a row's minutes as further episodes.

The strong reader, printed for reference and not the gate: the cracker plus a nearest-trial-end match for every
unlinked charge within its tax group, and every smart TV row's minutes expanded into the following episodes.

The mirror stops on the price (rung 2) and runs the cracker's ask route; on the main block it keeps the stage shares.

A figure is a hit when it is within half a unit of the golden at the asking sentence's rounding (one decimal). A
landed call scores 38 for the call and its components plus 7 for instruction-following plus 55 times the share of ask
figures hit; the best miss scores the main-block criteria it reproduces (the six stage shares of the thirteen main
criteria) out of 38, plus 7, plus 55 times its ask share.
"""
import json
import os
import sys
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TGT = os.path.join(os.path.dirname(HERE), 'target')
TOR = 'America/Toronto'
MONTHS = ['2025-%02d' % m for m in range(2, 11)]
LIST_PRICES = (999, 1499, 1199, 1699)


def read():
    g = lambda n: os.path.join(TGT, n)
    return (pd.read_csv(g('trial_register.csv'), dtype=str),
            pd.read_parquet(g('trial_viewing_2024-11_2026-02.parquet')),
            pd.read_csv(g('charges_processor_a_2024-11_2025-09.csv'), dtype={'merchant_ref': str}),
            pd.read_csv(g('charges_processor_b_2025-09_2026-02.csv'), dtype={'merchant_reference': str}),
            pd.read_csv(g('plan_changes.csv'), dtype=str),
            pd.read_csv(g('account_crosswalk.csv'), dtype=str),
            pd.read_csv(g('content_crosswalk.csv'), dtype=str),
            pd.read_excel(g('release_calendar.xlsx'), dtype={'content_id_en': str, 'content_id_fr': str}))


def register_rows(reg, xc):
    ts = pd.to_datetime(reg.trial_start_utc.str.rstrip('Z'))
    oldfmt = reg.trial_id.str.fullmatch(r'T\d{7}')
    cutover = ts[~oldfmt].min()
    after = oldfmt & (ts >= cutover - pd.Timedelta(hours=4))
    ts = ts.copy()
    ts[after] = ts[after].dt.tz_localize(TOR).dt.tz_convert('UTC').dt.tz_localize(None)
    pg = reg.signup_page.map(dict(zip(xc.legacy_id, xc.content_id))).fillna(reg.signup_page)
    D = reg.assign(start=ts, pg=pg)
    k = ['start', 'province', 'plan', 'signup_channel', 'signup_device', 'pg', 'language']
    hit = D[after][k + ['trial_id']].merge(D[~oldfmt][k].assign(_x=1), on=k, how='left')
    D = D[~D.trial_id.isin(set(hit.loc[hit._x.notna(), 'trial_id']))].copy()
    D['end'] = D.start + pd.Timedelta(days=7)
    D['month'] = D.start.dt.tz_localize('UTC').dt.tz_convert(TOR).dt.strftime('%Y-%m')
    return D


def charge_table(ca, cb):
    a = pd.DataFrame({'ref': ca.merchant_ref, 't': pd.to_datetime(ca.attempted_at_utc.str.rstrip('Z')),
                      'ok': ca.outcome == 'approved', 'c': ca.amount_cents.astype(float), 'r': np.nan})
    b = pd.DataFrame({'ref': cb.merchant_reference, 't': pd.to_datetime(cb.created, utc=True).dt.tz_localize(None),
                      'ok': cb.status == 'CAPTURED', 'c': np.nan,
                      'r': cb.tax_amount.astype(float) / cb.amount.astype(float)})
    X = pd.concat([a, b], ignore_index=True)
    for p in LIST_PRICES:
        r = X.c / p - 1
        X.loc[X.r.isna() & (r > 0.03) & (r < 0.17), 'r'] = r
    X['grp'] = np.round(np.where((X.r - 0.14975).abs() < 0.003, 0.15, X.r), 2)
    return X.sort_values('t').groupby('ref').agg(t0=('t', 'min'), paid=('ok', 'max'), grp=('grp', 'first'))


def paid(D, ch, pc, match_unlinked):
    nx = dict(zip(pc.subscription_id, pc.resulting_subscription_id))
    tail = []
    for s in D.subscription_id:
        n = 0
        while s in nx and nx[s] != s and n < 6:
            s, n = nx[s], n + 1
        tail.append(s)
    D = D.assign(sub=tail)
    D['has'] = D['sub'].isin(ch.index)
    if match_unlinked:
        lk = D[D.has]
        half = lambda t: np.where(t < pd.Timestamp('2025-04-01 04:00'), 0, 1)
        gp = pd.Series(lk['sub'].map(ch.grp).values, index=pd.MultiIndex.from_arrays(
            [lk.province.values, half(lk['sub'].map(ch.t0).values)])).groupby(level=[0, 1]).agg(lambda s: s.mode().iloc[0])
        D['grp'] = [gp.get((p, h), np.nan) for p, h in zip(D.province, half(D.end.values))]
        free = D[~D.has].sort_values('end')
        used = set(D.loc[D.has, 'sub'])
        took = set()
        for ref, o in ch[~ch.index.isin(used)].sort_values('t0').iterrows():
            c = free[(free.grp == o.grp) & (free.end <= o.t0) & (free.end > o.t0 - pd.Timedelta(hours=1))]
            c = c[~c.trial_id.isin(took)]
            if len(c):
                tid = c.iloc[-1].trial_id
                took.add(tid)
                D.loc[D.trial_id == tid, 'sub'] = ref
    return D['sub'].map(ch.paid).fillna(False).astype(bool).values


def episodes(D, view, xa, xc, cal, expand):
    v = view.drop_duplicates().copy()
    am = dict(zip(xa.old_account_no, xa.account_id))
    v['acct'] = v.account_ref.map(am).fillna(v.account_ref)
    v['cid'] = v.content_id.map(dict(zip(xc.legacy_id, xc.content_id))).fillna(v.content_id)
    cal = cal.assign(sk=cal.series + '|' + cal.season.astype(str))
    e = pd.concat([cal[['content_id_en', 'sk', 'episode', 'runtime_min']].rename(columns={'content_id_en': 'cid'}),
                   cal[['content_id_fr', 'sk', 'episode', 'runtime_min']].rename(columns={'content_id_fr': 'cid'})])
    v = v.merge(e, on='cid', how='inner')
    v['t'] = pd.to_datetime(v.play_start_utc).dt.tz_localize(None)
    rows = v[['acct', 'sk', 'episode', 't']]
    if expand:
        rt = {k: g.set_index('episode').runtime_min.to_dict() for k, g in cal.groupby('sk')}
        add = []
        for r in v[(v.device_type == 'smart_tv') & (v.minutes_watched > v.runtime_min)].itertuples():
            left, n = r.minutes_watched - r.runtime_min, r.episode + 1
            while left > 0 and n in rt[r.sk]:
                add.append((r.acct, r.sk, n, r.t))
                left -= rt[r.sk][n]
                n += 1
        rows = pd.concat([rows, pd.DataFrame(add, columns=rows.columns)], ignore_index=True)
    tr = pd.DataFrame({'acct': D.account_id.map(am).fillna(D.account_id), 'trial_id': D.trial_id, 's': D.start, 'e': D.end})
    m = rows.merge(tr, on='acct')
    m = m[(m.t >= m.s) & (m.t < m.e)].drop_duplicates(['trial_id', 'sk', 'episode'])
    return D.trial_id.map(m.groupby('trial_id').size()).fillna(0).values


def route(D, view, ch, pc, xa, xc, cal, strong):
    X = D[D.month.isin(MONTHS)].copy()
    X['paid'] = paid(X, ch, pc, strong)
    X['eps'] = episodes(X, view, xa, xc, cal, strong)
    g = X.groupby('month')
    return (100 * g.paid.mean()).round(1).to_dict(), g.eps.mean().round(1).to_dict()


def hits(got, gold):
    return sum(abs(got[m] - gold[m]) <= 0.05 + 1e-9 for m in MONTHS)


def main():
    fig = json.load(open(os.path.join(HERE, 'figures.json')))
    gp = {m: fig['ask_paid_share_%s' % m] for m in MONTHS}
    ge = {m: fig['ask_episodes_%s' % m] for m in MONTHS}
    reg, view, ca, cb, pc, xa, xc, cal = read()
    # the cracker's route sees the whole register (the plan-change chains reach outside the months)
    D = register_rows(reg, xc)
    ch = charge_table(ca, cb)
    cp, ce = route(D, view, ch, pc, xa, xc, cal, strong=False)
    sp, se = route(D, view, ch, pc, xa, xc, cal, strong=True)
    n = 2 * len(MONTHS)
    hp, he = hits(cp, gp), hits(ce, ge)
    Lc = (hp + he) / n
    Ls = Lc
    r = 38 * 6 / 13
    C = 38 + 7 + 55 * Lc
    S = r + 7 + 55 * Ls
    print('| Cracker row (full includer) | Figures | Kept | Verdict |')
    print('|---|---|---|---|')
    print('| M paid shares (D7) | 9 | %d | %s |' % (hp, 'miss' if hp == 0 else 'keeps'))
    print('| M episode averages (D6) | 9 | %d | %s |' % (he, 'miss' if he == 0 else 'keeps'))
    print('| Full includer, both blocks | 18 | %d | %s |' % (hp + he, 'miss' if hp + he == 0 else 'keeps'))
    print('cracker ask keep %.1f per cent; mirror leakage %.1f per cent; landed %.1f, best miss %.1f, pair ceiling %.1f'
          % (100 * Lc, 100 * Ls, C, S, (C + S) / 2))
    shp, she = hits(sp, gp), hits(se, ge)
    print('strong reader (reference): keeps %d of 18 (%d paid, %d episodes)' % (shp + she, shp, she))
    print('month    gold paid  cracker  strong |  gold eps  cracker  strong')
    for m in MONTHS:
        print('%s  %6.1f  %7.1f  %6.1f |  %6.1f  %7.1f  %6.1f' % (m, gp[m], cp[m], sp[m], ge[m], ce[m], se[m]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
