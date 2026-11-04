"""task403 world: the clean truth of Ellesmere's free trials, November 2024 to January 2026.

Ellesmere is an originals-only Canadian streaming service. Every season is released weekly, one episode each Friday at
00:00 Toronto time. A trialist decides at the end of the seven-day trial whether to keep the subscription; what holds
them is a season they were watching that still has an episode to come after their trial ends. The price for new
subscriptions' first charges rose on 1 November 2025, the night the autumn seasons ended.

Everything here is the world before any export is written: true times, true devices, true subscriptions. `pack.py`
writes what each system records of it.
"""
import numpy as np
import pandas as pd
from zoneinfo import ZoneInfo

SEED = 40326
NS = 10**9
DAY = 86400 * NS
HOUR = 3600 * NS
TOR = ZoneInfo('America/Toronto')

# provinces: share of trials, IANA zone, sales tax on a digital subscription (rate, label) by date
PROV = {
    'ON': (0.385, 'America/Toronto'), 'QC': (0.222, 'America/Toronto'), 'BC': (0.138, 'America/Vancouver'),
    'AB': (0.116, 'America/Edmonton'), 'MB': (0.035, 'America/Winnipeg'), 'SK': (0.030, 'America/Regina'),
    'NS': (0.029, 'America/Halifax'), 'NB': (0.022, 'America/Moncton'), 'NL': (0.014, 'America/St_Johns'),
    'PE': (0.006, 'America/Halifax'), 'YT': (0.001, 'America/Whitehorse'), 'NT': (0.001, 'America/Yellowknife'),
    'NU': (0.001, 'America/Iqaluit'),
}

MIGRATION = pd.Timestamp('2025-06-09 06:00', tz='UTC')        # content and subscription platform cut-over
DUAL_END = pd.Timestamp('2025-06-20 04:00', tz='UTC')         # old platform's writes stop (19 June, Toronto)
WEB_LEGACY_END = pd.Timestamp('2025-10-01 04:00', tz='UTC')   # web front end sends series codes until 30 Sept
PLATFORM_72 = pd.Timestamp('2025-02-03 05:00', tz='UTC')      # plan change opens a new subscription
PLATFORM_76 = pd.Timestamp('2025-10-14 04:00', tz='UTC')      # plan change keeps the subscription
ATV_LAUNCH = pd.Timestamp('2025-02-03 05:00', tz='UTC')       # Google TV and Android TV app
ATV_SDK = pd.Timestamp('2025-10-20 04:00', tz='UTC')          # app 1.4 writes plays to the viewing service
PROCESSOR_SWITCH = pd.Timestamp('2025-09-08 04:00', tz='UTC')  # card processor change (retry schedule shortened)
PRICE_DATE = pd.Timestamp('2025-11-01 04:00', tz='UTC')       # first charges from 1 Nov (Toronto) at the new price
CAMPAIGN = pd.Timestamp('2025-11-03 05:00', tz='UTC')         # paid social campaign
EXTRACT = pd.Timestamp('2026-02-27 05:00', tz='UTC')

PRICES = {('standard', 0): 999, ('premium', 0): 1499, ('standard', 1): 1199, ('premium', 1): 1699}


def ts(s):
    """A Toronto wall-clock string to a UTC timestamp."""
    return pd.Timestamp(s, tz=TOR).tz_convert('UTC')


def allocate(rng, p, keys):
    """True for round(n * mean p) members of each cell of the keys, chosen at random inside the cell."""
    key = np.zeros(len(p), dtype='int64')
    for k in keys:
        k = np.asarray(k)
        _, inv = np.unique(k, return_inverse=True)
        key = key * (int(inv.max()) + 1) + inv
    u = rng.random(len(p))
    out = np.zeros(len(p), bool)
    order = np.lexsort((u, key))
    ks = key[order]
    bounds = np.flatnonzero(np.diff(ks)) + 1
    for grp in np.split(order, bounds):
        m = int(round(len(grp) * float(np.mean(p[grp]))))
        out[grp[:m]] = True
    return out


def weekly(first, n, skip=()):
    out, d = [], pd.Timestamp(first)
    while len(out) < n:
        if d.strftime('%Y-%m-%d') not in skip:
            out.append(d)
        d += pd.Timedelta(days=7)
    return out


# (series, season, French title, first Friday, episodes, runtime minutes, audience weight)
SEASONS = [
    ('Ashby Shore', 1, "Rive d'Ashby", '2023-03-03', 10, 47, 1.0),
    ('Harbourlight', 1, 'Phare du havre', '2023-09-08', 10, 52, 1.0),
    ('Ironwood', 1, 'Bois de fer', '2023-11-03', 12, 44, 1.0),
    ('Bellweather', 1, 'Bellweather', '2024-03-01', 8, 41, 1.0),
    ('Cutstone', 1, 'Pierre taillée', '2024-06-07', 8, 38, 1.0),
    ('Harbourlight', 2, 'Phare du havre', '2024-08-30', 10, 52, 1.0),
    ('Marrow Creek', 1, 'Ruisseau Marrow', '2024-10-25', 17, 49, 1.0),
    ('Quillon', 1, 'Quillon', '2025-02-14', 14, 46, 1.0),
    ('Cutstone', 2, 'Pierre taillée', '2025-04-11', 10, 39, 1.0),
    ('Tidewater Inn', 1, "L'Auberge des marées", '2025-06-13', 10, 43, 1.0),
    ('Ironwood', 2, 'Bois de fer', '2025-06-20', 10, 45, 1.0),
    ('Bellweather', 2, 'Bellweather', '2025-08-08', 12, 42, 1.0),
    ('Hollow Point Road', 1, 'Chemin Hollow Point', '2025-08-15', 12, 50, 1.0),
    ('Harbourlight', 3, 'Phare du havre', '2025-08-29', 10, 53, 1.0),
    ('Gravel & Gold', 1, "Gravier et or", '2026-04-03', 10, 47, 1.0),
]
SKIPS = {}
SERIES_CODE = {'Ashby Shore': 'ASHB', 'Harbourlight': 'HARB', 'Ironwood': 'IRON', 'Bellweather': 'BELL',
               'Cutstone': 'CUTS', 'Marrow Creek': 'MARR', 'Quillon': 'QUIL', 'Tidewater Inn': 'TIDE'}


def calendar(rng):
    """One row per release: every episode in English and French, and each season's trailer (episode 0)."""
    rows = []
    for (series, sn, fr, first, n, rt, w) in SEASONS:
        dates = weekly(first, n, SKIPS.get((series, sn), ()))
        for ep, d in enumerate(dates, 1):
            rel = ts(d.strftime('%Y-%m-%d 00:00'))
            run = int(rt + rng.integers(-5, 6))
            rows.append((series, sn, fr, ep, 'episode', rel, run, w))
        trailer = ts((dates[0] - pd.Timedelta(days=int(rng.integers(16, 23)))).strftime('%Y-%m-%d 09:00'))
        rows.append((series, sn, fr, 0, 'trailer', trailer, int(rng.integers(2, 4)), w))
    cal = pd.DataFrame(rows, columns=['series', 'season', 'title_fr', 'episode', 'kind', 'release_utc', 'runtime', 'weight'])
    cal['season_key'] = cal.series + ' S' + cal.season.astype(str)
    # identifiers: legacy numeric ids for anything the old content system held before the cut-over, new GUIDs for all
    n = len(cal)
    cal['id_en'] = ['%08x-%04x-4%03x-%04x-%012x' % tuple(int(x) for x in rng.integers(0, [2**32, 2**16, 2**12, 2**16, 2**48]))
                    for _ in range(n)]
    cal['id_fr'] = ['%08x-%04x-4%03x-%04x-%012x' % tuple(int(x) for x in rng.integers(0, [2**32, 2**16, 2**12, 2**16, 2**48]))
                    for _ in range(n)]
    held = cal.release_utc < MIGRATION + pd.Timedelta(days=30)   # created in the old system before the cut-over
    leg = rng.choice(np.arange(310000, 499999), size=2 * n, replace=False)
    cal['legacy_en'] = np.where(held, leg[:n].astype(str), '')
    cal['legacy_fr'] = np.where(held, leg[n:].astype(str), '')
    # season GUIDs (the page a sign-up comes from)
    keys = cal.season_key.unique()
    sg = {k: '%08x-%04x-4%03x-%04x-%012x' % tuple(int(x) for x in rng.integers(0, [2**32, 2**16, 2**12, 2**16, 2**48]))
          for k in keys}
    cal['season_id'] = cal.season_key.map(sg)
    return cal


def season_table(cal):
    ep = cal[cal.kind == 'episode']
    s = ep.groupby('season_key').agg(series=('series', 'first'), season=('season', 'first'), first=('release_utc', 'min'),
                                     last=('release_utc', 'max'), n=('episode', 'max'), weight=('weight', 'first'),
                                     season_id=('season_id', 'first')).reset_index()
    return s.sort_values('first').reset_index(drop=True)


def trial_times(rng, cal):
    """Trial starts, 1 November 2024 to 31 January 2026, in UTC, with each province's evening peak and the
    premiere-night rush on the Thursday before each season's first Friday."""
    days = pd.date_range('2024-11-01', '2026-01-31', freq='D')
    m = days.month.values
    lam = np.where(np.isin(m, [11, 12, 1]), 192.0, 136.0) * (1 + 0.035 * np.sin(np.arange(len(days)) / 23.0))
    dow = days.dayofweek.values
    lam *= np.array([0.93, 0.92, 0.95, 1.02, 1.12, 1.08, 0.98])[dow]
    cnt = rng.poisson(lam)
    day_idx = np.repeat(np.arange(len(days)), cnt)
    N = len(day_idx)
    prov_keys = list(PROV)
    pshare = np.array([PROV[k][0] for k in prov_keys]); pshare /= pshare.sum()
    prov = rng.choice(len(prov_keys), N, p=pshare)
    # local hour-of-day profile (evening peak), minute uniform
    prof = np.array([1.2, .8, .5, .35, .3, .35, .6, 1.0, 1.3, 1.5, 1.6, 1.7, 1.9, 1.9, 1.8, 1.9, 2.2, 2.6, 3.2, 3.8, 4.1,
                     3.9, 3.1, 2.0])
    prof /= prof.sum()
    hour = rng.choice(24, N, p=prof)
    sec = hour * 3600 + rng.integers(0, 3600, N)
    local_ns = days.as_unit('ns').asi8[day_idx] + sec.astype('int64') * NS
    starts = np.empty(N, dtype='int64')
    for pi, k in enumerate(prov_keys):
        idx = np.where(prov == pi)[0]
        if not len(idx):
            continue
        z = ZoneInfo(PROV[k][1])
        loc = pd.DatetimeIndex(local_ns[idx].astype('datetime64[ns]'))
        amb = np.zeros(len(idx), bool)
        loc = loc.tz_localize(z, nonexistent='shift_forward', ambiguous=amb).tz_convert('UTC').as_unit('ns')
        starts[idx] = loc.asi8
    return starts, np.array(prov_keys)[prov]


def simulate(seed=SEED, gain=0.177, price_eff=0.012, base=0.405):
    rng = np.random.default_rng(seed)
    cal = calendar(rng)
    S = season_table(cal)
    starts, prov = trial_times(rng, cal)
    # premiere-night rush: extra trials in the 90 minutes either side of each premiere (00:00 Toronto)
    extra_s, extra_p, extra_acq = [], [], []
    pshare = np.array([PROV[k][0] for k in PROV]); pshare /= pshare.sum()
    for i, r in S.iterrows():
        if r.weight < 0.5 or not (pd.Timestamp('2024-11-01', tz='UTC') <= r['first'] <= pd.Timestamp('2026-01-31', tz='UTC')):
            continue
        k = rng.poisson(76)
        off = rng.normal(15, 42, k) * 60 * NS
        extra_s.append(r['first'].value + off.astype('int64'))
        extra_p.append(rng.choice(list(PROV), k, p=pshare))
        extra_acq.append(np.full(k, i))
    if extra_s:
        starts = np.concatenate([starts, np.concatenate(extra_s)])
        prov = np.concatenate([prov, np.concatenate(extra_p)])
        forced = np.concatenate([np.full(len(starts) - sum(len(x) for x in extra_s), -1), np.concatenate(extra_acq)])
    else:
        forced = np.full(len(starts), -1)
    order = np.argsort(starts, kind='stable')
    starts, prov, forced = starts[order], prov[order], forced[order]
    keep = (starts >= ts('2024-11-01 00:00').value) & (starts < ts('2026-02-01 00:00').value)
    starts, prov, forced = starts[keep], prov[keep], forced[keep]
    # sign-ups pause for the cut-over's maintenance window (22:00 to 02:00 Toronto, 8 to 9 June 2025): a sign-up
    # attempted then went through when the new platform opened
    maint = (starts >= MIGRATION.value - 4 * HOUR) & (starts < MIGRATION.value)
    starts = np.where(maint, starts + 4 * HOUR, starts)
    o2 = np.argsort(starts, kind='stable')
    starts, prov, forced = starts[o2], prov[o2], forced[o2]
    N = len(starts)
    end = starts + 7 * DAY
    first = S['first'].map(lambda t: t.value).values
    last = S['last'].map(lambda t: t.value).values
    wgt = S.weight.values
    released = first <= EXTRACT.value
    # acquisition season (the page the sign-up came from)
    W = np.zeros((N, len(S)))
    for j in range(len(S)):
        if not released[j]:
            continue
        airing = (starts >= first[j] - 2 * DAY) & (starts <= last[j])
        recent = (starts > last[j]) & (starts <= last[j] + 56 * DAY)
        older = starts > last[j] + 56 * DAY
        w_air = 6.0 * wgt[j] if wgt[j] < 0.5 else 6.0
        W[:, j] = np.where(airing, w_air, np.where(recent, 4.5, np.where(older, 1.0, 0.0)))
    P = W / W.sum(1, keepdims=True)
    acq = (P.cumsum(1) < rng.random(N)[:, None]).sum(1)
    acq = np.where(forced >= 0, forced, acq).astype(int)
    # the sign-up device
    devices = np.array(['smart_tv', 'android_tv', 'ios', 'android', 'web', 'tablet'])
    atv_ok = starts >= ATV_LAUNCH.value
    dev_p_old = np.array([.40, 0.0, .17, .13, .22, .08])
    dev_p_new = np.array([.29, .12, .17, .13, .21, .08])
    u = rng.random(N)
    dev = np.where(atv_ok, (dev_p_new.cumsum()[None, :] < u[:, None]).sum(1), (dev_p_old.cumsum()[None, :] < u[:, None]).sum(1))
    # a sign-up made on a series page (every sign-up before the cut-over, and the web's until 30 September where the
    # series had a code) lands on the series' latest season released at that moment
    series = S.series.values
    on_series_page = (starts < MIGRATION.value) | ((devices[dev] == 'web') & (starts < WEB_LEGACY_END.value))
    coded = np.array([series[a] in SERIES_CODE for a in acq])
    sel = np.where(on_series_page & coded)[0]
    for i in sel:
        cand = np.where((series == series[acq[i]]) & (first <= starts[i]))[0]
        if len(cand):
            acq[i] = cand[np.argmax(first[cand])]
        else:
            # a sign-up in the minutes before a premiere lands on the premiering season
            acq[i] = np.where(series == series[acq[i]])[0][np.argmin(np.abs(first[series == series[acq[i]]] - starts[i]))]
    # channel, plan and language at sign-up
    chans = np.array(['search', 'social', 'tv_ad', 'referral', 'direct'])
    camp = starts >= CAMPAIGN.value
    u = rng.random(N)
    ch_old = np.array([.30, .25, .15, .10, .20]).cumsum(); ch_new = np.array([.26, .34, .12, .09, .19]).cumsum()
    chan = np.where(camp, (ch_new[None, :] < u[:, None]).sum(1), (ch_old[None, :] < u[:, None]).sum(1))
    plan0 = np.where(rng.random(N) < 0.22, 'premium', 'standard')
    lang = np.where((prov == 'QC') & (rng.random(N) < 0.76), 'fr', np.where(rng.random(N) < 0.02, 'fr', 'en'))
    month = pd.DatetimeIndex(starts.astype('datetime64[ns]')).tz_localize('UTC').tz_convert(TOR).strftime('%Y%m').astype(int).values
    # seasons played during the trial: the acquisition season and sampled seasons, drawn by allocation inside each
    # cell of start month, device and channel, so a season's viewers are spread over devices and channels as the
    # month's trials are
    watched = np.zeros((N, len(S)), bool)
    watched[np.arange(N), acq] = True
    for j in range(len(S)):
        if not released[j]:
            continue
        avail = first[j] <= end
        airing = (end >= first[j]) & (starts <= last[j])
        recent = (starts > last[j]) & (starts <= last[j] + 60 * DAY)
        if wgt[j] < 0.5:
            pr = np.where(airing, 0.05, 0.01)
        else:
            pr = np.where(airing, 0.55, np.where(recent, 0.30, 0.10))
        phase = np.where(airing, 2, np.where(recent, 1, 0))
        watched[:, j] |= avail & allocate(rng, pr * avail, [month, phase, avail, dev, chan])
    # nothing is played from a season before its first episode
    for j in range(len(S)):
        watched[:, j] &= first[j] < end
    # about one trialist in sixteen never plays anything during the trial; they decide at day 7 as a trialist with
    # nothing to come does
    noplay = rng.random(N) < 0.06
    watched[noplay] = False
    W0 = {'cal': cal, 'S': S, 'starts': starts, 'end': end, 'watched': watched, 'acq': acq}
    P = _plays(rng, W0)
    # runway: a season played during the trial with an episode released after the trial's end
    run = np.zeros(N, bool)
    lastrel = {k: g.release_utc.map(lambda t: t.value).max() for k, g in cal[cal.kind == 'episode'].groupby('season_key')}
    pl = P[['trial', 'season_key']].drop_duplicates()
    has_next = pl.season_key.map(lastrel).values > end[pl.trial.values]
    run[pl.trial.values[has_next]] = True
    newp = end >= PRICE_DATE.value
    seg = np.array([0.03, 0.025, -0.02, -0.035, 0.0, -0.01])[dev] + np.array([0.01, -0.062, 0.0, 0.03, 0.02])[chan]
    p_keep = base + gain * run - price_eff * newp + seg
    # the decision is drawn by allocation inside each cell of start month (Toronto), runway, price, device and channel:
    # the cell keeps round(n * p) of its trials, chosen at random, so every route that reads the cell reads its rate
    keep_sub = allocate(rng, p_keep, [month, run, newp, dev, chan])
    # plan changes during the trial (about 7 per cent, one in six of them twice)
    chg = rng.random(N) < 0.07
    chg2 = chg & (rng.random(N) < 0.16)
    plan_end = plan0.copy()
    one = chg & ~chg2
    plan_end[one] = np.where(plan0[one] == 'standard', 'premium', 'standard')
    # a trial not kept is cancelled after its last play, before its end
    lastplay = np.full(N, -1, dtype='int64')
    lp = P.groupby('trial').play_utc.max()
    lastplay[lp.index.values] = lp.values
    lo = np.where(lastplay > 0, lastplay + 20 * 60 * NS, starts + HOUR)
    lo = np.minimum(lo, end - 10 * 60 * NS)
    span = np.maximum(end - lo, 60 * NS)
    cancel_at = np.where(~keep_sub, lo + (span * rng.beta(1.4, 1.1, N)).astype('int64'), -1)
    # first charge at the trial's end; declines and retries (shorter schedule after the processor change)
    old_proc = end < PROCESSOR_SWITCH.value
    declined = keep_sub & allocate(rng, np.full(N, 0.071), [month, keep_sub, run])
    rec = allocate(rng, np.where(old_proc, 0.72, 0.525), [month, declined, old_proc, run]) & declined
    paid = keep_sub & (~declined | rec)
    T = pd.DataFrame({
        'start': starts, 'end': end, 'prov': prov, 'device': devices[dev], 'channel': chans[chan], 'plan0': plan0,
        'plan_end': plan_end, 'lang': lang, 'acq': acq, 'acq_key': S.season_key.values[acq], 'run': run,
        'newp': newp, 'keep': keep_sub, 'cancel_at': cancel_at, 'declined': declined,
        'recovered': declined & rec & keep_sub, 'paid': paid, 'chg': chg, 'chg2': chg2,
    })
    # play devices follow the sign-up device most of the time
    # every play of an autoplay session is on one device; a session is on the sign-up device most of the time
    sid = P.groupby(['trial', 'season_key', 'sess'], sort=False).ngroup().values
    ns = int(sid.max()) + 1
    first_trial = np.zeros(ns, dtype='int64')
    first_trial[sid] = P.trial.values
    sd = T.device.values[first_trial]
    alt = rng.choice(['smart_tv', 'ios', 'android', 'web', 'tablet'], ns)
    sdev = np.where(rng.random(ns) < 0.78, sd, alt)
    # a run of two or more episodes is often watched on the living-room set
    slen = np.bincount(sid, minlength=ns)
    sdev = np.where((slen >= 2) & (sdev != 'android_tv') & (rng.random(ns) < 0.35), 'smart_tv', sdev)
    P['session'] = sid
    P['device'] = sdev[sid]
    P['lang'] = T.lang.values[P.trial.values]
    T['n_seasons'] = P.groupby('trial').season_key.nunique().reindex(range(N)).fillna(0).astype(int).values
    T, P = bin_guard(T, P, cal, np.random.default_rng(seed + 101))
    T['n_seasons'] = P.groupby('trial').season_key.nunique().reindex(range(N)).fillna(0).astype(int).values
    return {'cal': cal, 'S': S, 'T': T, 'P': P, 'rng': rng, 'seed': seed}


ASK_MONTHS = ['2025-%02d' % m for m in range(2, 11)]


def _edge(v, u=0.1):
    return (u / 2 - abs(v - round(v / u) * u)) / u


def bin_guard(T, P, cal, rng, floor=0.22):
    """Keep every monthly figure of the trials started February to October 2025 clear of its one-decimal edge, and no
    two months on one trial count, by the smallest change to the records of those months: a declined first charge
    that a retry did or did not recover, one catalogue play more or less, a sign-up in a month's last minutes landing
    in the next ask month. Winter trials are never touched; every figure is then computed forward from the records."""
    month = pd.DatetimeIndex(pd.to_datetime(T.start.values)).tz_localize('UTC').tz_convert(TOR).strftime('%Y-%m')
    T = T.copy()
    T['month_'] = month
    ep = cal[cal.kind == 'episode']
    rel = {k: g.sort_values('episode').release_utc.map(lambda t: t.value).values for k, g in ep.groupby('season_key')}
    rts = {k: g.sort_values('episode').runtime.values for k, g in ep.groupby('season_key')}
    # monthly counts: no two months of the register on one count (move a last-minute sign-up between ask months)
    counts = T.groupby('month_').size()
    for _ in range(6):
        dup = counts[counts.duplicated(keep=False)]
        movable = [m for m in dup.index if m in ASK_MONTHS[:-1]]
        if not movable:
            break
        m = movable[0]
        last = T[(T.month_ == m)].start.max()
        i = T.index[(T.month_ == m) & (T.start == last)][0]
        shift = int(pd.Timestamp(month_end(m), tz=TOR).tz_convert('UTC').value - T.at[i, 'start']) + 7 * 60 * NS
        T.at[i, 'start'] += shift
        T.at[i, 'end'] += shift
        if T.at[i, 'cancel_at'] > 0:
            T.at[i, 'cancel_at'] += shift
        P.loc[P.trial == i, 'play_utc'] += shift
        T.at[i, 'month_'] = pd.Timestamp(T.at[i, 'start'], tz='UTC').tz_convert(TOR).strftime('%Y-%m')
        counts = T.groupby('month_').size()
    for m in ASK_MONTHS:
        sel = (T.month_ == m).values
        n = sel.sum()
        # the paid share: move toward the centre of its bin, one recovery at a time
        v0 = 100 * T.paid.values[sel].mean()
        up = (v0 - round(v0, 1)) <= 0
        for _ in range(40):
            v = 100 * T.paid.values[sel].mean()
            if _edge(v) >= floor:
                break
            if up:
                c = np.where(sel & T.keep.values & T.declined.values & ~T.recovered.values)[0]
                j = c[rng.integers(len(c))]
                T.at[j, 'recovered'] = True
                T.at[j, 'paid'] = True
            else:
                c = np.where(sel & T.keep.values & T.declined.values & T.recovered.values)[0]
                j = c[rng.integers(len(c))]
                T.at[j, 'recovered'] = False
                T.at[j, 'paid'] = False
        # the average number of episodes played
        ids = np.where(sel)[0]
        pm = P[P.trial.isin(ids)]
        seen = set(zip(pm.trial, pm.season_key, pm.episode))
        cnt = len(seen)
        add_rows, drop_idx = [], []
        last = pm.sort_values('play_utc').groupby(['trial', 'season_key']).tail(1)
        last = last.iloc[rng.permutation(len(last))]
        sz = pm.groupby('session').size()
        many = pm.groupby('trial').size()
        singles = pm[pm.session.isin(sz.index[sz == 1]) & (pm.trial.map(many) > 1).values]
        singles = singles.iloc[rng.permutation(len(singles))]
        li, si = 0, 0
        next_session = int(P.session.max()) + 1
        up_e = (cnt / n - round(cnt / n, 1)) <= 0
        for _ in range(400):
            v = cnt / n
            if _edge(v) >= floor:
                break
            if up_e:
                done = False
                while li < len(last):
                    r = last.iloc[li]
                    li += 1
                    e = int(r.episode)
                    if e < len(rel[r.season_key]) and (r.trial, r.season_key, e + 1) not in seen and \
                            rel[r.season_key][e] < T.at[r.trial, 'end'] - 3 * HOUR:
                        t = max(int(r.play_utc) + int(r.minutes) * 60 * NS + HOUR, int(rel[r.season_key][e]) + HOUR)
                        if t < T.at[r.trial, 'end'] - 2 * HOUR:
                            add_rows.append((r.trial, r.season_key, e + 1, t, int(round(rts[r.season_key][e] * 0.985)),
                                             int(r.sess) + 1000, next_session, r.device, r.lang))
                            next_session += 1
                            seen.add((r.trial, r.season_key, e + 1))
                            cnt += 1
                            done = True
                            break
                if not done:
                    break
            else:
                if si >= len(singles):
                    break
                r = singles.iloc[si]
                k = singles.index[si]
                si += 1
                key = (r.trial, r.season_key, r.episode)
                if ((pm.trial == r.trial) & (pm.season_key == r.season_key) & (pm.episode == r.episode)).sum() == 1:
                    drop_idx.append(k)
                    seen.discard(key)
                    cnt -= 1
        if drop_idx:
            P = P.drop(index=drop_idx)
        if add_rows:
            P = pd.concat([P, pd.DataFrame(add_rows, columns=['trial', 'season_key', 'episode', 'play_utc', 'minutes',
                                                                'sess', 'session', 'device', 'lang'])], ignore_index=True)
    P = P.sort_values(['play_utc', 'trial'], kind='stable').reset_index(drop=True)
    return T.drop(columns='month_'), P


def month_end(m):
    y, mo = int(m[:4]), int(m[5:])
    return '%04d-%02d-01 00:00' % (y + (mo == 12), mo % 12 + 1)


def _plays(rng, W0):
    """Episode plays across each trial's seven days for every season the trialist plays."""
    cal, S, starts, end, watched = W0['cal'], W0['S'], W0['starts'], W0['end'], W0['watched']
    ep = cal[cal.kind == 'episode']
    out = []
    for j in range(len(S)):
        k = S.season_key[j]
        g = ep[ep.season_key == k].sort_values('release_utc')
        e = g.release_utc.map(lambda t: t.value).values
        rt = g.runtime.values
        tr = np.nonzero(watched[:, j])[0]
        if not len(tr):
            continue
        st, en = starts[tr], end[tr]
        avail = np.searchsorted(e, en, side='right')
        ok = avail > 0
        tr, st, en, avail = tr[ok], st[ok], en[ok], avail[ok]
        airing = (e[0] <= st) & (e[-1] > st)
        latest = np.searchsorted(e, st, side='right')
        lo = np.where(airing & (rng.random(len(tr)) < 0.45), np.maximum(0, latest - 2), 0)
        lo = np.minimum(lo, avail - 1)
        n = np.minimum(rng.geometric(0.33, len(tr)), avail - lo)
        base_t = np.maximum(st, e[lo]) + (rng.exponential(0.7, len(tr)) * DAY).astype('int64')
        base_t = np.minimum(base_t, en - HOUR)
        base_t = np.where(base_t <= st, st + rng.integers(10, 300, len(tr)) * 60 * NS, base_t)
        nmax = int(n.max())
        prev_t = base_t.copy()
        prev_min = np.zeros(len(tr), dtype="int64")
        prev_done = np.zeros(len(tr), bool)
        sess = np.zeros(len(tr), dtype='int64')
        alive = np.ones(len(tr), bool)
        for q in range(nmax):
            idx = np.nonzero((n > q) & alive)[0]
            if not len(idx):
                break
            epi = lo[idx] + q
            # an episode of a season airing when the trial began is watched to the end far more often than a
            # catalogue episode sampled on the way in
            pc = np.where(airing[idx], 0.985, 0.72)
            done = rng.random(len(idx)) < pc
            frac = np.where(done, rng.uniform(0.97, 1.0, len(idx)), np.clip(rng.beta(5.0, 2.0, len(idx)), 0.3, 0.92))
            mins = np.maximum(1, np.round(rt[epi] * frac)).astype('int64')
            if q == 0:
                t = base_t[idx]
                auto = np.zeros(len(idx), bool)
            else:
                # the next episode starts on its own when the last one ends (autoplay), or the trialist comes back later
                auto = (rng.random(len(idx)) < 0.45) & prev_done[idx]
                after = prev_t[idx] + prev_min[idx] * 60 * NS
                t = np.where(auto, after + rng.integers(5, 150, len(idx)) * NS,
                             after + HOUR + (rng.exponential(1.1, len(idx)) * DAY).astype('int64'))
            rel = e[epi] + rng.integers(5, 240, len(idx)) * 60 * NS
            late = t < rel
            auto = auto & ~late
            t = np.maximum(t, rel)
            sess[idx] += (~auto).astype('int64') * (q > 0)
            ok = t < en[idx] - 60 * NS
            alive[idx[~ok]] = False
            idx, t, epi, mins = idx[ok], t[ok], epi[ok], mins[ok]
            good = t > st[idx]
            prev_t[idx] = t
            prev_min[idx] = mins
            prev_done[idx] = done[ok]
            out.append(pd.DataFrame({'trial': tr[idx][good], 'season_key': k, 'episode': epi[good] + 1,
                                     'play_utc': t[good], 'minutes': mins[good], 'sess': sess[idx][good]}))
    P = pd.concat(out, ignore_index=True)
    # the first play of a trial is its sign-up season: any play of another season that would come first moves to a
    # few minutes after the sign-up season's first play
    acq = W0['acq']
    P['is_acq'] = P.season_key.values == S.season_key.values[acq[P.trial.values]]
    fa = P[P.is_acq].groupby('trial').play_utc.min()
    f_acq = np.full(len(starts), np.iinfo(np.int64).max, dtype='int64')
    f_acq[fa.index.values] = fa.values
    t_acq = f_acq[P.trial.values]
    # (a season's plays move together, so an autoplay run stays one run; plays pushed past the trial's end drop out)
    P['first_s'] = P.groupby(['trial', 'season_key']).play_utc.transform('min')
    early_s = (~P.is_acq.values) & (P.first_s.values <= t_acq)
    keys = P.loc[early_s, ['trial', 'season_key']].drop_duplicates()
    delay = pd.Series(rng.integers(4, 90, len(keys)) * 60 * NS, index=pd.MultiIndex.from_frame(keys))
    if len(keys):
        d = delay.reindex(pd.MultiIndex.from_frame(P.loc[early_s, ['trial', 'season_key']])).values
        P.loc[early_s, 'play_utc'] = (P.loc[early_s, 'play_utc'].values - P.loc[early_s, 'first_s'].values
                                      + t_acq[early_s] + d)
    P = P[P.play_utc.values < end[P.trial.values] - 60 * NS].drop(columns='first_s')
    # a trial whose sign-up season has no play has no plays at all
    P = P[f_acq[P.trial.values] < np.iinfo(np.int64).max].drop(columns='is_acq')
    return P.sort_values(['play_utc', 'trial'], kind='stable').reset_index(drop=True)
