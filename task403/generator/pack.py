"""task403 pack: what each of Ellesmere's systems records of the world, written under target/.

Systems and the conventions each one writes (none of this ships as a description; each file carries its own form):
- the subscription platform's trial register: the old platform's account, trial and subscription numbers before the
  9 June 2025 cut-over, the new platform's ids after. From 9 to 19 June the old platform kept running beside the new
  one: web and phone sign-ups were written by both from 04:00 on 9 June, when the old platform's mirror of them was
  switched on two hours after the new platform opened (the old copy under numbers nothing else uses), TV and tablet
  sign-ups by the old platform alone until the TV apps moved on 19 June. The old platform's rows of those days carry
  Toronto wall-clock time with a Z;
- the viewing service (UTC; legacy content and account numbers before the cut-over, ids after; French versions under
  their own ids; the smart TV app from its 8 February 2025 release to its 27 October release reported one row per
  autoplay run; a row written twice when an app reconnects);
- two card processors: the first to 7 September 2025 (cents, tax included, four scheduled attempts), the second from
  8 September (dollars before tax, tax beside it, Toronto time with an offset, three attempts);
- the account service's plan-change log (no dates): from the plan-change launch on 3 February 2025 to the rebuilt flow
  of 14 October a change opened a new subscription; the old platform's changes before 9 June never reached the log, and
  until 14 October the apps' changes did not either; from 14 October a change keeps the subscription. While a change
  opened a new subscription, a subscription opened in an app was managed in the apps and one opened on the web or by
  support on the web, so a trialist's second change went through the same kind of surface as the first: a trial's
  changes are all logged or none of them is;
- the content system's release calendar (Toronto time) and the cut-over crosswalks (content and accounts).
"""
import numpy as np
import pandas as pd
import world

NS = world.NS
DAY = world.DAY
HOUR = 3600 * NS
MINUTE = 60 * NS
TOR = world.TOR
ALNUM = np.array(list('abcdefghijklmnopqrstuvwxyz0123456789'))

SMARTTV_30 = world.ts('2025-02-08 00:00').value     # smart TV app 3.0: the new player, autoplay
SMARTTV_34 = world.ts('2025-10-27 00:00').value     # smart TV app 3.4: player update
PLAN_LAUNCH = world.PLATFORM_72.value               # plan changes during the free trial (3 February 2025)
PLAN_REBUILT = world.PLATFORM_76.value              # plan change flow rebuilt (14 October 2025)
MIG = world.MIGRATION.value
DUAL_END = world.DUAL_END.value
MIRROR_START = world.ts('2025-06-09 04:00').value  # the old platform's mirror of web and phone sign-ups
SWITCH = world.PROCESSOR_SWITCH.value


def rid(rng, n, k, prefix=''):
    """n unique random ids of k base36 characters with a prefix."""
    out, seen = [], set()
    while len(out) < n:
        chars = ALNUM[rng.integers(0, 36, (n - len(out) + 16, k))]
        for row in chars:
            s = prefix + ''.join(row)
            if s not in seen:
                seen.add(s)
                out.append(s)
                if len(out) == n:
                    break
    return np.array(out, dtype=object)


def rnum(rng, n, lo, hi, prefix='', exclude=()):
    """n distinct random numbers in [lo, hi) as strings with a prefix, none of them in exclude."""
    ex = set(exclude)
    out, seen = [], set()
    while len(out) < n:
        for x in rng.integers(lo, hi, n - len(out) + 64):
            s = prefix + str(int(x))
            if s not in seen and s not in ex:
                seen.add(s)
                out.append(s)
                if len(out) == n:
                    break
    return np.array(out, dtype=object)


def iso_z(ns):
    return pd.to_datetime(np.asarray(ns, dtype='int64')).strftime('%Y-%m-%dT%H:%M:%SZ')


def toronto_as_z(ns):
    """Toronto wall-clock time written with a Z, as the old platform wrote its rows after the cut-over."""
    t = pd.to_datetime(np.asarray(ns, dtype='int64')).tz_localize('UTC').tz_convert(TOR).tz_localize(None)
    return t.strftime('%Y-%m-%dT%H:%M:%SZ')


def local_offset(ns):
    t = pd.to_datetime(np.asarray(ns, dtype='int64')).tz_localize('UTC').tz_convert(TOR)
    s = t.strftime('%Y-%m-%d %H:%M:%S%z')
    return np.array([x[:-2] + ':' + x[-2:] for x in s])


TAX = {'ON': 0.13, 'QC': 0.14975, 'BC': 0.12, 'AB': 0.05, 'MB': 0.12, 'SK': 0.11, 'NB': 0.15, 'NL': 0.15,
       'PE': 0.15, 'YT': 0.05, 'NT': 0.05, 'NU': 0.05, 'NS': 0.15}
NS_CUT = world.ts('2025-04-01 00:00').value


def tax_rate(prov, when_ns):
    out = np.array([TAX[p] for p in prov])
    return np.where((np.asarray(prov) == 'NS') & (np.asarray(when_ns) >= NS_CUT), 0.14, out)


def systems(W):
    """Identifiers, subscriptions, register rows, charges, plan-change rows, viewing rows: the systems' records."""
    rng = np.random.default_rng(W['seed'] + 7)
    T = W['T'].copy()
    N = len(T)
    st = T.start.values
    dev = T.device.values
    pre = st < MIG
    dual = (st >= MIG) & (st < DUAL_END)
    single = dual & np.isin(dev, ['smart_tv', 'android_tv', 'tablet'])
    twin = dual & ~single
    oldfmt = pre | single
    T['pre'], T['single'], T['twin'] = pre, single, twin
    # accounts and ids
    T['acct_new'] = rid(rng, N, 10, 'ac')
    n_old = int(oldfmt.sum()) + int(twin.sum())
    old_accts = rnum(rng, n_old, 10_000_000, 99_999_999)
    old_trials = rnum(rng, n_old, 1_000_000, 9_999_999, 'T')
    old_subs = rnum(rng, n_old, 100_000_000, 999_999_999, 'S')
    T['acct_old'] = ''
    T['trial_id'] = ''
    T['sub0'] = ''
    k = int(oldfmt.sum())
    T.loc[oldfmt, 'acct_old'] = old_accts[:k]
    T.loc[oldfmt, 'trial_id'] = old_trials[:k]
    T.loc[oldfmt, 'sub0'] = old_subs[:k]
    newfmt = ~oldfmt
    T.loc[newfmt, 'trial_id'] = rid(rng, int(newfmt.sum()), 10, 'tr_')
    T.loc[newfmt, 'sub0'] = rid(rng, int(newfmt.sum()), 12, 'sb_')
    T['acct_reg'] = np.where(oldfmt, T.acct_old.values, T.acct_new.values)
    # the old platform's copies of web and phone sign-ups of 9 to 19 June
    tw = T[twin].copy()
    tw['copy_acct'] = old_accts[k:]
    tw['copy_trial'] = old_trials[k:]
    tw['copy_sub'] = old_subs[k:]
    tw['copy_acct_new'] = rid(rng, len(tw), 10, 'ac')
    # plan changes: from the launch to the rebuilt flow a change opened a new subscription
    chain = T.chg.values & (st >= PLAN_LAUNCH) & (st < PLAN_REBUILT)
    T['chain'] = chain
    via = np.where(rng.random(N) < 0.07, 'support', np.where(rng.random(N) < 0.495, 'web', 'app'))
    T['via1'] = via
    # while a change opened a new subscription (7.2 to 8.4), the new subscription was managed where it was opened: an
    # app's in the apps, the web's and support's on the web; after 8.4 a trialist changes wherever they like
    v2 = np.where(rng.random(N) < 0.5, 'web', 'app')
    T['via2'] = np.where(chain, np.where(via == 'app', 'app', 'web'), v2)
    s1_old = rnum(rng, N, 100_000_000, 999_999_999, 'S', exclude=set(old_subs))
    s2_old = rnum(rng, N, 100_000_000, 999_999_999, 'S', exclude=set(old_subs) | set(s1_old))
    s1_new = rid(rng, N, 12, 'sb_')
    s2_new = rid(rng, N, 12, 'sb_')
    T['sub1'] = np.where(chain, np.where(pre, s1_old, s1_new), '')
    T['sub2'] = np.where(chain & T.chg2.values, np.where(pre, s2_old, s2_new), '')
    T['sub_charged'] = np.where(T.sub2 != '', T.sub2, np.where(T.sub1 != '', T.sub1, T.sub0))
    logged1 = chain & ~pre & (via != 'app')
    logged2 = logged1 & T.chg2.values & (T.via2.values != 'app')
    T['linked'] = ~chain | logged1 & (~T.chg2.values | logged2)
    rows = []
    for i in np.where(T.chg.values)[0]:
        p0 = T.plan0.values[i]
        p1 = 'premium' if p0 == 'standard' else 'standard'
        s0 = T.sub0.values[i]
        if st[i] >= PLAN_REBUILT:
            rows.append((s0, s0, p0, p1, via[i]))
            if T.chg2.values[i]:
                rows.append((s0, s0, p1, p0, T.via2.values[i]))
        elif chain[i] and not pre[i]:
            if logged1[i]:
                rows.append((s0, T.sub1.values[i], p0, p1, via[i]))
            if T.chg2.values[i] and T.via2.values[i] != 'app':
                rows.append((T.sub1.values[i], T.sub2.values[i], p1, p0, T.via2.values[i]))
    CH = pd.DataFrame(rows, columns=['subscription_id', 'resulting_subscription_id', 'plan_before', 'plan_after',
                                     'requested_via'])
    CH = CH.iloc[rng.permutation(len(CH))].reset_index(drop=True)
    CH.insert(0, 'change_ref', rid(rng, len(CH), 8, 'PC-'))
    # the charges draw on their own stream, so the log's length never moves an attempt
    C = charges(T, np.random.default_rng(W['seed'] + 17))
    # the old platform mirrored web and phone sign-ups from 04:00 Toronto on 9 June; the first two hours' were written
    # by the new platform alone (their copy numbers stay drawn, so no other identifier moves)
    tw = tw[tw.start.values >= MIRROR_START]
    return T, tw, C, CH


def charges(T, rng):
    """First-charge attempts: the first at the trial's end, then the processor's scheduled retries. An unlinked
    plan-change subscription's first attempt is re-timed so that no other trial without a linked charge, in a province
    of the same charged amount, ended between its trial's end and that attempt."""
    kept = np.where(T.keep.values)[0]
    end = T.end.values
    prov = T.prov.values
    plan_end = T.plan_end.values
    newp = T.newp.values.astype(int)
    price = np.array([world.PRICES[(plan_end[i], newp[i])] for i in range(len(T))])
    rate = tax_rate(prov, end)
    cents = np.round(price * (1 + rate)).astype(int)
    old = end < SWITCH
    # the tax rate a solver reads off a charge names a group of provinces, never the plan (Quebec's rate and the 15 per
    # cent provinces print the same standard charge, so they are one group)
    group = np.round(np.where(np.isclose(rate, 0.14975), 0.15, rate), 2)
    delay = (rng.uniform(30, 360, len(T)) * NS).astype('int64')
    linked_charge = T.keep.values & T.linked.values
    unlinked_pool = ~linked_charge          # trials a solver would see without a linked charge
    for i in np.where(T.keep.values & ~T.linked.values)[0]:
        same = unlinked_pool & (group == group[i])
        same[i] = False
        later = end[same]
        later = later[later > end[i]]
        gap = (later.min() - end[i]) if len(later) else 10 * MINUTE
        if delay[i] >= gap:
            delay[i] = max(int(gap * 0.5), 5 * NS)
    rows = []
    for i in kept:
        e = end[i] + delay[i]
        o = old[i]
        sched = [0, 1, 3, 5] if o else [0, 1, 2]
        if not T.declined.values[i]:
            outcomes = ['ok']
        elif T.recovered.values[i]:
            k = int(rng.integers(1, len(sched)))
            outcomes = ['no'] * k + ['ok']
        else:
            outcomes = ['no'] * len(sched)
        for a, oc in enumerate(outcomes):
            t = e + sched[a] * DAY + (int(rng.integers(0, 3600)) * NS + int(rng.integers(1, 6)) * HOUR if a else 0)
            rows.append((i, a + 1, t, oc, o, price[i], cents[i]))
    C = pd.DataFrame(rows, columns=['trial', 'attempt', 't', 'outcome', 'old', 'price', 'cents'])
    C['sub'] = T.sub_charged.values[C.trial.values]
    C['prov'] = prov[C.trial.values]
    reasons = np.array(['insufficient_funds', 'do_not_honour', 'expired_card', 'card_velocity_exceeded', 'issuer_unavailable'])
    C['reason'] = np.where(C.outcome == 'no', reasons[rng.choice(5, len(C), p=[.52, .23, .13, .07, .05])], '')
    return C


def viewing(W, T):
    """The viewing service's rows for every play during a trial."""
    rng = np.random.default_rng(W['seed'] + 11)
    P = W['P'].copy()
    cal = W['cal']
    epi = cal[cal.kind == 'episode'].set_index(['season_key', 'episode'])
    tr = P.trial.values
    t = P.play_utc.values
    # smart TV app 3.x: one row per autoplay run
    sess_first = P.groupby('session').play_utc.transform('min').values
    run = (P.device.values == 'smart_tv') & (sess_first >= SMARTTV_30) & (sess_first < SMARTTV_34)
    P['run'] = run
    head = P[run].sort_values(['session', 'play_utc']).groupby('session').agg(
        trial=('trial', 'first'), season_key=('season_key', 'first'), episode=('episode', 'first'),
        play_utc=('play_utc', 'first'), minutes=('minutes', 'sum'), device=('device', 'first'),
        lang=('lang', 'first'), n=('episode', 'size')).reset_index()
    rest = P[~run][['session', 'trial', 'season_key', 'episode', 'play_utc', 'minutes', 'device', 'lang']].assign(n=1)
    V = pd.concat([rest, head], ignore_index=True)
    tr = V.trial.values
    t = V.play_utc.values
    pre_tr = T.pre.values[tr]
    single_tr = T.single.values[tr]
    old_acct = (pre_tr & (t < MIG)) | (single_tr & (t < DUAL_END))
    V['account'] = np.where(old_acct, T.acct_old.values[tr], T.acct_new.values[tr])
    key = list(zip(V.season_key.values, V.episode.values))
    fr = V.lang.values == 'fr'
    gid = np.where(fr, epi.loc[key, 'id_fr'].values, epi.loc[key, 'id_en'].values)
    leg = np.where(fr, epi.loc[key, 'legacy_fr'].values, epi.loc[key, 'legacy_en'].values)
    V['content'] = np.where((t < MIG) & (leg != ''), leg, gid)
    # profiles: most plays on the account's first profile, a household's others on some sessions
    prof_of_session = rng.choice([1, 1, 1, 1, 1, 2, 2, 3, 4], int(V.session.max()) + 1)
    V['profile'] = prof_of_session[V.session.values]
    out = pd.DataFrame({
        'account_ref': V.account.values, 'profile_no': V.profile.values.astype('int8'), 'content_id': V.content.values,
        'play_start_utc': pd.to_datetime(V.play_utc.values).tz_localize('UTC'),
        'minutes_watched': V.minutes.values.astype('int16'), 'device_type': V.device.values,
    })
    dup = rng.random(len(out)) < 0.008
    out = pd.concat([out, out[dup]], ignore_index=True)
    out = out.sort_values(['play_start_utc', 'account_ref', 'content_id'], kind='stable').reset_index(drop=True)
    return out, V


def register(T, tw, cal, S):
    """The trial register export: one row per trial on each platform."""
    page_new = dict(zip(S.season_key, S.season_id))
    page_old = season_legacy_pages(cal, S)
    oldfmt = (T.pre | T.single).values
    page = np.where(oldfmt, T.acq_key.map(page_old).fillna(T.acq_key.map(page_new)).values, T.acq_key.map(page_new).values)
    start_txt = np.where(T.single.values, toronto_as_z(T.start.values), iso_z(T.start.values))
    reg = pd.DataFrame({
        'trial_id': T.trial_id.values, 'account_id': T.acct_reg.values, 'subscription_id': T.sub0.values,
        'trial_start_utc': start_txt, 'province': T.prov.values, 'plan': T.plan0.values,
        'signup_channel': T.channel.values, 'signup_device': T.device.values, 'signup_page': page,
        'language': T.lang.values, '_t': T.start.values,
    })
    cp = pd.DataFrame({
        'trial_id': tw.copy_trial.values, 'account_id': tw.copy_acct.values, 'subscription_id': tw.copy_sub.values,
        'trial_start_utc': toronto_as_z(tw.start.values), 'province': tw.prov.values, 'plan': tw.plan0.values,
        'signup_channel': tw.channel.values, 'signup_device': tw.device.values,
        'signup_page': tw.acq_key.map(page_old).fillna(tw.acq_key.map(page_new)).values,
        'language': tw.lang.values, '_t': tw.start.values - 4 * HOUR + 1,
    })
    out = pd.concat([reg, cp], ignore_index=True).sort_values(['_t', 'trial_id'], kind='stable').drop(columns='_t')
    assert out.trial_id.is_unique and out.subscription_id.is_unique
    return out.reset_index(drop=True)


def season_legacy_pages(cal, S):
    """The old content system's numbers for the season pages it held before the cut-over."""
    rng = np.random.default_rng(4031)
    held = S['first'].map(lambda x: x.value).values < MIG + 30 * DAY
    nums = rng.choice(np.arange(210000, 299999), size=len(S), replace=False)
    return {k: str(n) for k, n, h in zip(S.season_key, nums, held) if h}


def crosswalks(T, tw, cal, S):
    rows = []
    for _, r in cal[cal.kind == 'episode'].iterrows():
        if r.legacy_en:
            rows.append((r.legacy_en, r.id_en, 'episode'))
        if r.legacy_fr:
            rows.append((r.legacy_fr, r.id_fr, 'episode'))
    pages = season_legacy_pages(cal, S)
    sid = dict(zip(S.season_key, S.season_id))
    for k, n in pages.items():
        rows.append((n, sid[k], 'season_page'))
    cw = pd.DataFrame(rows, columns=['legacy_id', 'content_id', 'legacy_type'])
    cw = cw.sort_values(['legacy_id'], kind='stable').reset_index(drop=True)
    o = T[(T.pre | T.single).values]
    am = pd.concat([pd.DataFrame({'old_account_no': o.acct_old.values, 'account_id': o.acct_new.values}),
                    pd.DataFrame({'old_account_no': tw.copy_acct.values, 'account_id': tw.copy_acct_new.values})],
                   ignore_index=True).sort_values('old_account_no', kind='stable').reset_index(drop=True)
    return cw, am


def charge_exports(C, rng):
    o = C[C.old]
    a = pd.DataFrame({
        'txn_id': rnum(rng, len(o), 40_000_000_000, 49_999_999_999, 'TX'),
        'merchant_ref': o['sub'].values, 'attempted_at_utc': iso_z(o.t.values),
        'amount_cents': o.cents.values.astype(int), 'currency': 'CAD',
        'outcome': np.where(o.outcome == 'ok', 'approved', 'declined'), 'decline_reason': o.reason.values,
        'attempt': o.attempt.values,
    }).iloc[np.argsort(o.t.values, kind='stable')].reset_index(drop=True)
    n = C[~C.old]
    rate = tax_rate(n.prov.values, n.t.values)
    b = pd.DataFrame({
        'psp_reference': rid(rng, len(n), 16, ''),
        'merchant_reference': n['sub'].values, 'created': local_offset(n.t.values),
        'amount': (n.price.values / 100).round(2), 'tax_amount': np.round(n.price.values * rate / 100, 2),
        'currency': 'CAD', 'status': np.where(n.outcome == 'ok', 'CAPTURED', 'REFUSED'),
        'refusal_reason': n.reason.values, 'retry_count': n.attempt.values - 1,
    }).iloc[np.argsort(n.t.values, kind='stable')].reset_index(drop=True)
    return a, b


def calendar_sheet(cal):
    ep = cal[cal.kind == 'episode'].copy()
    rel = ep.release_utc.dt.tz_convert(TOR).dt.strftime('%Y-%m-%d %H:%M')
    fr_series = ep.title_fr.values
    out = pd.DataFrame({
        'series': ep.series.values, 'series_fr': fr_series, 'season': ep.season.values.astype(int),
        'episode': ep.episode.values.astype(int), 'release_toronto': rel.values, 'runtime_min': ep.runtime.values.astype(int),
        'content_id_en': ep.id_en.values, 'content_id_fr': ep.id_fr.values, 'season_page': ep.season_id.values,
    })
    return out.sort_values(['release_toronto', 'series', 'episode'], kind='stable').reset_index(drop=True)
