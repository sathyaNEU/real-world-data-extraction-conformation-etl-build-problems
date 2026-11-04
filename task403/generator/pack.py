"""task403 pack: what each of Ellesmere's systems records of the world, written under target/.

Systems and their conventions (none of this ships as a description; each file carries its own):
- the subscription platform's trial register (UTC with Z; the old platform's account and trial numbers before the
  9 June 2025 cut-over, the new platform's after; the old platform's rows of 9 to 19 June written in Toronto wall-clock
  time with a Z, under account numbers the cut-over never mapped);
- the viewing service (UTC; legacy content numbers before the cut-over, GUIDs after; French versions under their own
  ids; the Google TV and Android TV app wrote no plays until its 1.4 release on 20 October 2025; a summary row written
  twice when an app reconnects);
- the licence server, for the trials started 1 February to 31 October 2025 (UTC; new account ids; every licence,
  episodes and the trailers TV home screens play);
- two card processors: the first to 7 September 2025 (cents, tax included, four attempts), the second from 8 September
  (dollars before tax, tax beside it, Toronto time with offset, three attempts);
- the plan-change register (no dates; from 3 February to 13 October 2025 a change opened a new subscription);
- the content system's release calendar (Toronto time) and the cut-over crosswalks (content and accounts).
"""
import gzip
import io
import os
import numpy as np
import pandas as pd
import world

NS = world.NS
DAY = world.DAY
TOR = world.TOR
ALNUM = np.array(list('abcdefghijklmnopqrstuvwxyz0123456789'))


def rid(rng, n, k, prefix=''):
    """n unique random ids of k base36 characters with a prefix."""
    out, seen = [], set()
    while len(out) < n:
        need = n - len(out)
        chars = ALNUM[rng.integers(0, 36, (need + 16, k))]
        for row in chars:
            s = prefix + ''.join(row)
            if s not in seen:
                seen.add(s)
                out.append(s)
                if len(out) == n:
                    break
    return np.array(out)


def rnum(rng, n, lo, hi, prefix=''):
    v = rng.choice(np.arange(lo, hi), size=n, replace=False)
    return np.array([prefix + str(x) for x in v])


def iso_z(ns):
    return pd.to_datetime(np.asarray(ns, dtype='int64')).strftime('%Y-%m-%dT%H:%M:%SZ')


def local_offset(ns):
    t = pd.to_datetime(np.asarray(ns, dtype='int64')).tz_localize('UTC').tz_convert(TOR)
    s = t.strftime('%Y-%m-%d %H:%M:%S%z')
    return np.array([x[:-2] + ':' + x[-2:] for x in s])


def tax_rate(prov, when_ns):
    """Sales tax on a digital subscription by province: HST, or GST plus the provincial tax that applies."""
    r = {'ON': 0.13, 'QC': 0.14975, 'BC': 0.12, 'AB': 0.05, 'MB': 0.12, 'SK': 0.11, 'NB': 0.15, 'NL': 0.15,
         'PE': 0.15, 'YT': 0.05, 'NT': 0.05, 'NU': 0.05, 'NS': 0.15}
    out = np.array([r[p] for p in prov])
    ns_cut = world.ts('2025-04-01 00:00').value
    out = np.where((np.asarray(prov) == 'NS') & (np.asarray(when_ns) >= ns_cut), 0.14, out)
    return out


def build_systems(W):
    """Identifiers, subscriptions, charges, register rows, viewing rows, licences: the systems' records."""
    rng = np.random.default_rng(W['seed'] + 7)
    T = W['T'].copy()
    P = W['P'].copy()
    cal, S = W['cal'], W['S']
    N = len(T)
    mig = world.MIGRATION.value
    pre = T.start.values < mig
    # accounts: the old platform's numbers before the cut-over, the new platform's ids after; every account that
    # existed at the cut-over is mapped
    T['acct_new'] = rid(rng, N, 10, 'ac')
    T['acct_old'] = np.where(pre, rnum(rng, N, 10_000_000, 99_999_999, ''), '')
    T['trial_id'] = np.where(pre, rnum(rng, N, 1_000_000, 9_999_999, 'T'), rid(rng, N, 10, 'tr_'))
    T['acct_reg'] = np.where(pre, T.acct_old, T.acct_new)
    # subscriptions and plan changes
    sub0 = np.where(pre, rnum(rng, N, 100_000_000, 999_999_999, 'S'), rid(rng, N, 12, 'sb_'))
    T['sub0'] = sub0
    in72 = (T.start.values >= world.PLATFORM_72.value) & (T.start.values < world.PLATFORM_76.value)
    T['chain'] = T.chg.values & in72
    n1 = rid(rng, N, 12, 'sb_')
    n2 = rid(rng, N, 12, 'sb_')
    T['sub1'] = np.where(T.chain, n1, '')
    T['sub2'] = np.where(T.chain & T.chg2, n2, '')
    T['sub_charged'] = np.where(T.sub2 != '', T.sub2, np.where(T.sub1 != '', T.sub1, T.sub0))
    # plan-change register rows (no dates)
    ch = []
    for i in np.where(T.chg.values)[0]:
        p0 = T.plan0.values[i]
        p1 = 'premium' if p0 == 'standard' else 'standard'
        src = rng.choice(['web', 'app', 'support'], p=[0.46, 0.47, 0.07])
        if T.chain.values[i]:
            ch.append((T.sub0.values[i], T.sub1.values[i], p0, p1, src))
            if T.chg2.values[i]:
                ch.append((T.sub1.values[i], T.sub2.values[i], p1, p0, rng.choice(['web', 'app'])))
        else:
            ch.append((T.sub0.values[i], T.sub0.values[i], p0, p1, src))
            if T.chg2.values[i]:
                ch.append((T.sub0.values[i], T.sub0.values[i], p1, p0, rng.choice(['web', 'app'])))
    CH = pd.DataFrame(ch, columns=['subscription_id', 'resulting_subscription_id', 'plan_before', 'plan_after', 'requested_via'])
    CH = CH.iloc[rng.permutation(len(CH))].reset_index(drop=True)
    CH.insert(0, 'change_ref', rid(rng, len(CH), 8, 'PC-').astype(str))
    # sign-up page: series code before the cut-over; after it, the season's GUID, except the web, which kept sending
    # series codes for the series that had one until its 30 September release
    season_id = dict(zip(S.season_key, S.season_id))
    code = T.acq_key.map(lambda k: world.SERIES_CODE.get(k.rsplit(' S', 1)[0], '')).values
    web_legacy = (T.device.values == 'web') & (T.start.values >= mig) & (T.start.values < world.WEB_LEGACY_END.value) & (code != '')
    page = np.where(pre | web_legacy, code, T.acq_key.map(season_id).values)
    page = np.where(page == '', T.acq_key.map(season_id).values, page)
    T['page'] = page
    # charges: first charge at the trial's end, then retries for a declined charge
    rows = []
    kept = np.where(T.keep.values)[0]
    for i in kept:
        e = T.end.values[i]
        old = e < world.PROCESSOR_SWITCH.value
        plan = T.plan_end.values[i]
        newp = int(T.newp.values[i])
        base = world.PRICES[(plan, newp)]
        sched = [0, 1, 3, 5] if old else [0, 1, 2]
        if not T.declined.values[i]:
            outcomes = ['ok']
        elif T.recovered.values[i]:
            k = int(rng.integers(1, len(sched)))
            outcomes = ['no'] * k + ['ok']
        else:
            outcomes = ['no'] * len(sched)
        for a, oc in enumerate(outcomes):
            t = e + sched[a] * DAY + int(rng.integers(0, 3600)) * NS + (int(rng.integers(1, 6)) * HOUR_NS if a else 0)
            rows.append((i, a + 1, t, oc, old, base))
    C = pd.DataFrame(rows, columns=['trial', 'attempt', 't', 'outcome', 'old', 'base'])
    C['sub'] = T.sub_charged.values[C.trial.values]
    C['prov'] = T.prov.values[C.trial.values]
    reasons = np.array(['insufficient_funds', 'do_not_honour', 'expired_card', 'card_velocity_exceeded', 'issuer_unavailable'])
    C['reason'] = np.where(C.outcome == 'no', reasons[rng.choice(5, len(C), p=[.52, .23, .13, .07, .05])], '')
    # register rows, and the old platform's rows of 9 to 19 June for web and phone sign-ups
    dual = (T.start.values >= mig) & (T.start.values < world.DUAL_END.value) & np.isin(T.device.values, ['web', 'ios', 'android'])
    T['dual'] = dual
    # viewing rows: account and content ids by the date of the play
    pl = P.copy()
    pl_pre = pl.play_utc.values < mig
    acct = np.where(pl_pre, T.acct_old.values[pl.trial.values], T.acct_new.values[pl.trial.values])
    # a trial started before the cut-over has an old number; its plays after the cut-over carry its new id
    pl['account'] = acct
    epi = cal[cal.kind == 'episode'].set_index(['season_key', 'episode'])
    key = list(zip(pl.season_key.values, pl.episode.values))
    fr = pl.lang.values == 'fr'
    gid = np.where(fr, epi.loc[key, 'id_fr'].values, epi.loc[key, 'id_en'].values)
    leg = np.where(fr, epi.loc[key, 'legacy_fr'].values, epi.loc[key, 'legacy_en'].values)
    pl['content'] = np.where(pl_pre, leg, gid)
    pl['gid'] = gid
    pl['profile'] = rng.choice([1, 1, 1, 1, 2, 2, 3, 4], len(pl))
    pl['seen_by_viewing'] = ~((pl.device.values == 'android_tv') & (pl.play_utc.values < world.ATV_SDK.value))
    return T, pl, C, CH


HOUR_NS = 3600 * NS


def write_register(T, rng, path):
    reg = pd.DataFrame({
        'trial_id': T.trial_id.values, 'account_id': T.acct_reg.values, 'subscription_id': T.sub0.values,
        'trial_start_utc': iso_z(T.start.values), 'province': T.prov.values, 'plan': T.plan0.values,
        'signup_channel': T.channel.values, 'signup_device': T.device.values, 'signup_page': T.page.values,
        'language': T.lang.values, '_t': T.start.values,
    })
    d = T[T.dual]
    tor = pd.to_datetime(d.start.values).tz_localize('UTC').tz_convert(TOR).tz_localize(None)
    old = pd.DataFrame({
        'trial_id': rnum(rng, len(d), 1_000_000, 9_999_999, 'T'),
        'account_id': rnum(rng, len(d), 10_000_000, 99_999_999, ''),
        'subscription_id': rnum(rng, len(d), 100_000_000, 999_999_999, 'S'),
        'trial_start_utc': tor.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'province': d.prov.values, 'plan': d.plan0.values, 'signup_channel': d.channel.values,
        'signup_device': d.device.values,
        'signup_page': d.acq_key.map(lambda k: world.SERIES_CODE.get(k.rsplit(' S', 1)[0], '')).values,
        'language': d.lang.values, '_t': d.start.values + 1,
    })
    old['signup_page'] = np.where(old.signup_page == '', reg.signup_page.values[np.where(T.dual.values)[0]], old.signup_page)
    # the old platform's numbers must not collide with the register's own
    clash = set(old.trial_id) & set(reg.trial_id)
    assert not clash, 'trial id clash'
    out = pd.concat([reg, old], ignore_index=True).sort_values(['_t', 'trial_id'], kind='stable').drop(columns='_t')
    out.to_csv(path, index=False)
    return out


def write_viewing(pl, rng, path):
    v = pl[pl.seen_by_viewing].copy()
    out = pd.DataFrame({
        'account_ref': v.account.values, 'profile_no': v.profile.values.astype('int8'), 'content_id': v.content.values,
        'play_start_utc': pd.to_datetime(v.play_utc.values).tz_localize('UTC'),
        'minutes_watched': v.minutes.values.astype('int16'), 'device_type': v.device.values,
    })
    dup = rng.random(len(out)) < 0.008
    out = pd.concat([out, out[dup]], ignore_index=True)
    out = out.sort_values(['play_start_utc', 'account_ref'], kind='stable').reset_index(drop=True)
    out.to_parquet(path, index=False, compression='zstd')
    return out


def write_licences(T, pl, cal, rng, path):
    lo, hi = world.ts('2025-02-01 00:00').value, world.ts('2025-11-01 00:00').value
    tri = np.where((T.start.values >= lo) & (T.start.values < hi))[0]
    sel = np.isin(pl.trial.values, tri)
    v = pl[sel]
    lic = pd.DataFrame({'requested_utc': v.play_utc.values - rng.integers(1, 9, len(v)) * NS,
                        'account': T.acct_new.values[v.trial.values], 'device_class': v.device.values,
                        'content_id': v.gid.values, 'licence': np.where(rng.random(len(v)) < 0.03, 'offline', 'stream')})
    # trailers on TV home screens: a preview starts after a few seconds of idle on the row
    tvs = tri[np.isin(T.device.values[tri], ['smart_tv', 'android_tv'])]
    tr = cal[cal.kind == 'trailer']
    rel = tr.release_utc.map(lambda t: t.value).values
    rows = []
    for i in tvs:
        k = rng.poisson(1.3)
        if not k:
            continue
        st = T.start.values[i]
        cands = np.where((rel <= st + 5 * DAY) & (rel >= st - 60 * DAY))[0]
        if not len(cands):
            continue
        for _ in range(k):
            j = cands[int(rng.integers(len(cands)))]
            t = st + int(rng.uniform(0.02, 6.5) * DAY)
            fr = T.lang.values[i] == 'fr'
            rows.append((t, T.acct_new.values[i], T.device.values[i], tr.id_fr.values[j] if fr else tr.id_en.values[j], 'stream'))
    lic = pd.concat([lic, pd.DataFrame(rows, columns=lic.columns)], ignore_index=True)
    lic['requested_utc'] = pd.to_datetime(lic.requested_utc.values).tz_localize('UTC')
    lic = lic.sort_values(['requested_utc', 'account'], kind='stable').reset_index(drop=True)
    lic.to_parquet(path, index=False, compression='zstd')
    return lic


def write_charges(C, rng, path_old, path_new):
    o = C[C.old]
    taxr = tax_rate(o.prov.values, o.t.values)
    old = pd.DataFrame({
        'txn_id': rnum(rng, len(o), 40_000_000_000, 49_999_999_999, 'TX'),
        'merchant_ref': o['sub'].values, 'attempted_at_utc': iso_z(o.t.values),
        'amount_cents': np.round(o.base.values * (1 + taxr)).astype(int), 'currency': 'CAD',
        'outcome': np.where(o.outcome == 'ok', 'approved', 'declined'), 'decline_reason': o.reason.values,
        'attempt': o.attempt.values,
    })
    old = old.iloc[np.argsort(o.t.values, kind='stable')]
    old.to_csv(path_old, index=False)
    n = C[~C.old]
    taxr = tax_rate(n.prov.values, n.t.values)
    new = pd.DataFrame({
        'psp_reference': rid(rng, len(n), 16, '').astype(str),
        'merchant_reference': n['sub'].values, 'created': local_offset(n.t.values),
        'amount': (n.base.values / 100).round(2), 'tax_amount': np.round(n.base.values * taxr / 100, 2),
        'currency': 'CAD', 'status': np.where(n.outcome == 'ok', 'CAPTURED', 'REFUSED'),
        'refusal_reason': n.reason.values, 'retry_count': n.attempt.values - 1,
    })
    new = new.iloc[np.argsort(n.t.values, kind='stable')]
    new.to_csv(path_new, index=False, float_format='%.2f')
    return old, new


def write_crosswalks(T, cal, S, path_content, path_accounts):
    rows = []
    for _, r in cal.iterrows():
        if r.legacy_en:
            rows.append((r.legacy_en, r.id_en, r.kind))
        if r.legacy_fr:
            rows.append((r.legacy_fr, r.id_fr, r.kind))
    mig = world.MIGRATION
    for name, codev in world.SERIES_CODE.items():
        live = S[(S.series == name) & (S['first'] <= mig + pd.Timedelta(days=7))]
        cur = live.sort_values('first').iloc[-1]
        rows.append((codev, cur.season_id, 'series_page'))
    cw = pd.DataFrame(rows, columns=['legacy_id', 'content_id', 'legacy_type'])
    cw = cw.sort_values(['legacy_type', 'legacy_id'], kind='stable').reset_index(drop=True)
    cw.to_csv(path_content, index=False)
    pre = T[T.acct_old != '']
    am = pd.DataFrame({'old_account_no': pre.acct_old.values, 'account_id': pre.acct_new.values})
    am = am.sort_values('old_account_no', kind='stable').reset_index(drop=True)
    am.to_csv(path_accounts, index=False)
    return cw, am


def write_plan_changes(CH, path):
    CH.to_csv(path, index=False)
    return CH
