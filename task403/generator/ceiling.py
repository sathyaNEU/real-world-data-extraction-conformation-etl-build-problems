"""task403 ask ceiling, measured on the cut pack. Shares no code with the generator or the verifier: it reads target/
and the golden figures in generator/figures.json, executes each response's route for the ask as code, and scores it.

    python3 ceiling.py        # exit 1 when the pair ceiling is over 60 or the full includer keeps over two fifths

The routes, each a complete pipeline over the same files:
- the cracker: lands the call, runs the hygiene battery (exact duplicate rows dropped, clocks converted, legacy numbers
  mapped through both crosswalks, the old platform's June copies matched to their new-platform rows on the re-timed
  clock, the TV and tablet sign-ups only the old platform wrote kept and re-timed), follows every change the plan-change
  log records to the charge it produced (conversion standard, section 4) and counts an episode for each viewing row it
  attributes to a trial (section 5: an autoplayed episode counts; a row names an episode);
- the full includer: a blind medium-effort reader who reads every file and acts on every stated fact. Over the
  cracker it applies each processor's retry schedule to the letter (a charge collected after the last scheduled retry
  does not convert) and bounds the plan-change and smart TV releases by the release log's dates; it notices the first
  charges no file links to a trial and the smart TV rows longer than their episode, and with no file naming a trial for
  the one or the episodes in the other, counts neither;
- the no-repair reader: every row as it stands (the register's subscription only, written stamps as UTC, no copies
  dropped, viewing rows joined on their own account and content numbers, each row an episode);
- the mirror: stops on the price (rung 2) and handles the asks as the cracker does; on the main block it keeps the six
  stage shares of the thirteen main criteria.
For reference, never the gate: the strong reader (the cracker plus a nearest-trial-end match for every unlinked charge
within its tax group, and every smart TV row's minutes walked through the following episodes' runtimes), and two
partial handlings a sharp reader can reach from stated facts alone: each unlinked collected charge counted in the month
of its first attempt less the seven-day trial (section 2), and a long smart TV row read as minutes over the named
episode's runtime, rounded up.

A figure is a hit when it is within half a unit of the golden at the asking sentence's rounding (one decimal). A
landed call scores 38 for the call and its components plus 7 for instruction-following plus 55 times the share of ask
figures hit; the best miss scores the main-block criteria it reproduces out of 38, plus 7, plus 55 times its ask share.
"""
import hashlib
import json
import math
import os
import sys
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, 'target')
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
            pd.read_excel(g('release_calendar.xlsx'), dtype={'content_id_en': str, 'content_id_fr': str}),
            pd.read_excel(g('product_release_log.xlsx'), dtype=str))


def released(log, product, note):
    r = log[(log['Product'] == product) & log['Release note'].str.startswith(note)]
    return pd.Timestamp(r['Release date'].iloc[0]).tz_localize(TOR).tz_convert('UTC').tz_localize(None)


def register_rows(reg, xc, repair):
    ts = pd.to_datetime(reg.trial_start_utc.str.rstrip('Z'))
    oldfmt = reg.trial_id.str.fullmatch(r'T\d{7}')
    pg = reg.signup_page.map(dict(zip(xc.legacy_id, xc.content_id))).fillna(reg.signup_page)
    if repair:
        cutover = ts[~oldfmt].min()
        after = oldfmt & (ts >= cutover - pd.Timedelta(hours=4))
        ts = ts.copy()
        ts[after] = ts[after].dt.tz_localize(TOR).dt.tz_convert('UTC').dt.tz_localize(None)
        D = reg.assign(start=ts, pg=pg)
        k = ['start', 'province', 'plan', 'signup_channel', 'signup_device', 'pg', 'language']
        hit = D[after][k + ['trial_id']].merge(D[~oldfmt][k].assign(_x=1), on=k, how='left')
        D = D[~D.trial_id.isin(set(hit.loc[hit._x.notna(), 'trial_id']))].copy()
    else:
        D = reg.assign(start=ts, pg=pg)
    D['end'] = D.start + pd.Timedelta(days=7)
    D['month'] = D.start.dt.tz_localize('UTC').dt.tz_convert(TOR).dt.strftime('%Y-%m')
    return D.reset_index(drop=True)


def charge_table(ca, cb, strict):
    a = pd.DataFrame({'ref': ca.merchant_ref, 't': pd.to_datetime(ca.attempted_at_utc.str.rstrip('Z')),
                      'ok': ca.outcome == 'approved', 'c': ca.amount_cents.astype(float), 'r': np.nan,
                      'n': ca.attempt.astype(int), 'last': 4})
    b = pd.DataFrame({'ref': cb.merchant_reference, 't': pd.to_datetime(cb.created, utc=True).dt.tz_localize(None),
                      'ok': cb.status == 'CAPTURED', 'c': np.nan,
                      'r': cb.tax_amount.astype(float) / cb.amount.astype(float), 'n': cb.retry_count.astype(int) + 1,
                      'last': 3})
    X = pd.concat([a, b], ignore_index=True)
    if strict:
        first = X.groupby('ref').t.transform('min')
        span = np.where(X['last'] == 4, 5.25, 2.25)
        X['ok'] = X.ok & (X.n <= X['last']) & ((X.t - first) <= pd.to_timedelta(span, unit='D'))
    for p in LIST_PRICES:
        r = X.c / p - 1
        X.loc[X.r.isna() & (r > 0.03) & (r < 0.17), 'r'] = r
    X['grp'] = np.round(np.where((X.r - 0.14975).abs() < 0.003, 0.15, X.r), 2)
    return X.sort_values('t').groupby('ref').agg(t0=('t', 'min'), paid=('ok', 'max'), grp=('grp', 'first'))


def tails(D, pc, follow):
    if not follow:
        return D.subscription_id.values
    nx = dict(zip(pc.subscription_id, pc.resulting_subscription_id))
    out = []
    for s in D.subscription_id:
        n = 0
        while s in nx and nx[s] != s and n < 6:
            s, n = nx[s], n + 1
        out.append(s)
    return np.array(out, dtype=object)


def paid_shares(D, ch, pc, how):
    """The share that paid, by start month: 'register' (the register's subscription), 'chains' (the logged changes
    followed), 'match' (chains, then every unlinked charge to the nearest earlier trial end in its tax group) or 'date'
    (chains, then every unlinked collected charge counted in the month its first attempt less seven days falls in)."""
    D = D.assign(sub=tails(D, pc, how != 'register'))
    D['has'] = D['sub'].isin(ch.index)
    loose = ch[~ch.index.isin(set(D['sub']))].sort_values('t0')
    if how == 'match':
        lk = D[D.has]
        half = lambda t: np.where(t < pd.Timestamp('2025-04-01 04:00'), 0, 1)
        gp = pd.Series(lk['sub'].map(ch.grp).values, index=pd.MultiIndex.from_arrays(
            [lk.province.values, half(lk['sub'].map(ch.t0).values)])).groupby(level=[0, 1]).agg(lambda s: s.mode().iloc[0])
        D['grp'] = [gp.get((p, h), np.nan) for p, h in zip(D.province, half(D.end.values))]
        free = D[~D.has].sort_values('end')
        took = {}
        for ref, o in loose.iterrows():
            c = free[(free.grp == o.grp) & (free.end <= o.t0) & (free.end > o.t0 - pd.Timedelta(hours=1))]
            c = c[~c.trial_id.isin(set(took))]
            if len(c):
                took[c.iloc[-1].trial_id] = ref
        D['sub'] = [took.get(t, s) for t, s in zip(D.trial_id, D['sub'])]
    D['paid'] = D['sub'].map(ch.paid).fillna(False).astype(bool).values
    X = D[D.month.isin(MONTHS)]
    num = X.groupby('month').paid.sum().astype(float)
    if how == 'date':
        add = loose[loose.paid.astype(bool)]
        mo = (add.t0 - pd.Timedelta(days=7)).dt.tz_localize('UTC').dt.tz_convert(TOR).dt.strftime('%Y-%m')
        num = num.add(mo.value_counts(), fill_value=0).reindex(num.index)
    return (100 * num / X.groupby('month').size()).round(1).to_dict()


def episodes(D, view, xa, xc, cal, how, lo=None, hi=None):
    """Average episodes per trial started, by month: 'raw' (rows as they stand), 'rows' (each row its own episode once
    the battery has run), 'walk' (smart TV rows walked through the following episodes' runtimes) or 'ratio' (smart TV
    rows read as minutes over the named episode's runtime, rounded up)."""
    cal = cal.assign(sk=cal.series + '|' + cal.season.astype(str))
    e = pd.concat([cal[['content_id_en', 'sk', 'episode', 'runtime_min']].rename(columns={'content_id_en': 'cid'}),
                   cal[['content_id_fr', 'sk', 'episode', 'runtime_min']].rename(columns={'content_id_fr': 'cid'})])
    am = dict(zip(xa.old_account_no, xa.account_id))
    if how == 'raw':
        v = view.merge(e, left_on='content_id', right_on='cid', how='inner')
        v['acct'] = v.account_ref
        acct_tr = D.account_id
    else:
        v = view.drop_duplicates().copy()
        v['acct'] = v.account_ref.map(am).fillna(v.account_ref)
        v['cid'] = v.content_id.map(dict(zip(xc.legacy_id, xc.content_id))).fillna(v.content_id)
        v = v.merge(e, on='cid', how='inner')
        acct_tr = D.account_id.map(am).fillna(D.account_id)
    v['t'] = pd.to_datetime(v.play_start_utc).dt.tz_localize(None)
    rows = v[['acct', 'sk', 'episode', 't']]
    if how in ('walk', 'ratio'):
        rt = {k: g.set_index('episode').runtime_min.to_dict() for k, g in cal.groupby('sk')}
        long_ = v[(v.device_type == 'smart_tv') & (v.minutes_watched > v.runtime_min) & (v.t >= lo) & (v.t < hi)]
        add = []
        for r in long_.itertuples():
            if how == 'walk':
                left, n = r.minutes_watched - r.runtime_min, r.episode + 1
                while left > 0 and n in rt[r.sk]:
                    add.append((r.acct, r.sk, n, r.t))
                    left -= rt[r.sk][n]
                    n += 1
            else:
                for n in range(r.episode + 1, r.episode + math.ceil(r.minutes_watched / r.runtime_min)):
                    if n in rt[r.sk]:
                        add.append((r.acct, r.sk, n, r.t))
        rows = pd.concat([rows, pd.DataFrame(add, columns=rows.columns)], ignore_index=True)
    tr = pd.DataFrame({'acct': acct_tr, 'trial_id': D.trial_id, 's': D.start, 'e': D.end})
    m = rows.merge(tr, on='acct')
    m = m[(m.t >= m.s) & (m.t < m.e)]
    cnt = m.groupby('trial_id').size() if how == 'raw' else \
        m.drop_duplicates(['trial_id', 'sk', 'episode']).groupby('trial_id').size()
    X = D[D.month.isin(MONTHS)].assign(eps=lambda d: d.trial_id.map(cnt).fillna(0).values)
    return X.groupby('month').eps.mean().round(1).to_dict()


def hits(got, gold):
    return sum(abs(got[m] - gold[m]) <= 0.05 + 1e-9 for m in MONTHS)


def main():
    fig = json.load(open(os.path.join(HERE, 'figures.json')))
    gp = {m: fig['ask_paid_share_%s' % m] for m in MONTHS}
    ge = {m: fig['ask_episodes_%s' % m] for m in MONTHS}
    reg, view, ca, cb, pc, xa, xc, cal, log = read()
    digest = hashlib.sha256(open(os.path.join(TASK, 'target.zip'), 'rb').read()).hexdigest()[:12]
    lo = released(log, 'Smart TV app', 'New player; autoplay')
    hi = released(log, 'Smart TV app', 'Player update')
    D = register_rows(reg, xc, True)            # the plan-change chains reach outside the months: the whole register
    Dn = register_rows(reg, xc, False)
    ch, chs = charge_table(ca, cb, False), charge_table(ca, cb, True)
    P = {'cracker': paid_shares(D, ch, pc, 'chains'), 'full': paid_shares(D, chs, pc, 'chains'),
         'norepair': paid_shares(Dn, ch, pc, 'register'), 'strong': paid_shares(D, ch, pc, 'match'),
         'date': paid_shares(D, ch, pc, 'date')}
    E = {'cracker': episodes(D, view, xa, xc, cal, 'rows'), 'norepair': episodes(Dn, view, xa, xc, cal, 'raw'),
         'strong': episodes(D, view, xa, xc, cal, 'walk', lo, hi), 'ratio': episodes(D, view, xa, xc, cal, 'ratio', lo, hi)}
    E['full'] = E['cracker']                    # the long rows noticed, no episode they cover named by any file
    n = 2 * len(MONTHS)
    keep = {r: (hits(P[r], gp), hits(E[r], ge)) for r in ('cracker', 'full', 'norepair')}
    keep['mirror'] = keep['cracker']            # the asks do not turn on the call
    print('pack digest %s' % digest)
    print('| Route | Paid shares (9) | Episode averages (9) | Kept of 18 | Share | Verdict |')
    print('|---|---|---|---|---|---|')
    names = {'cracker': 'Cracker (lands the call, battery and filed rules)',
             'full': 'Full includer (every file, every stated fact)', 'norepair': 'No-repair (every row as it stands)',
             'mirror': 'Mirror (stops at rung 2 on (A), the cracker\'s ask route)'}
    for r in ('cracker', 'full', 'norepair', 'mirror'):
        a, b = keep[r]
        print('| %s | %d | %d | %d | %.1f%% | %s |' % (names[r], a, b, a + b, 100 * (a + b) / n,
                                                      'miss' if a + b == 0 else 'keeps %d' % (a + b)))
    Lc, Lm, Lf = sum(keep['cracker']) / n, sum(keep['mirror']) / n, sum(keep['full']) / n
    C = 38 + 7 + 55 * Lc
    S = 38 * 6 / 13 + 7 + 55 * Lm
    pair = (C + S) / 2
    print('landed %.1f, best miss %.1f, pair ceiling %.1f; mirror leakage %.1f per cent; full includer keeps %.1f per cent'
          % (C, S, pair, 100 * Lm, 100 * Lf))
    sp, se = hits(P['strong'], gp), hits(E['strong'], ge)
    print('reference, not the gate: strong reader keeps %d of 18 (%d paid, %d episodes); the seven-day dating of the '
          'unlinked charges keeps %d of 9 paid; minutes over runtime keeps %d of 9 episode averages'
          % (sp + se, sp, se, hits(P['date'], gp), hits(E['ratio'], ge)))
    print('month   gold paid cracker   full  norep strong   date |  gold eps cracker norep strong  ratio')
    for m in MONTHS:
        print('%s %8.1f %7.1f %6.1f %6.1f %6.1f %6.1f | %8.1f %7.1f %5.1f %6.1f %6.1f'
              % (m, gp[m], P['cracker'][m], P['full'][m], P['norepair'][m], P['strong'][m], P['date'][m], ge[m],
                 E['cracker'][m], E['norepair'][m], E['strong'][m], E['ratio'][m]))
    return 0 if pair <= 60 and Lf <= 0.4 else 1


if __name__ == '__main__':
    sys.exit(main())
