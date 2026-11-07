"""Larix batch platform, first half of 2027: the clean truth (task214).

Everything here is the generating process. Nothing in this module is shipped; render.py writes the
records the platform keeps. Times are minutes from EPOCH (UTC). Deterministic from the seed.
"""
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import numpy as np

VIENNA = ZoneInfo('Europe/Vienna')
UTC = timezone.utc
EPOCH = datetime(2026, 12, 18, 0, 0, tzinfo=UTC)
HIST_START = date(2026, 12, 18)          # history nights (expected runtimes for early January)
H1_START, H1_END = date(2027, 1, 1), date(2027, 6, 30)
CUTOVER = date(2027, 4, 19)              # first business night on the new orchestrator
NIGHTS = [HIST_START + timedelta(days=k) for k in range((H1_END - HIST_START).days + 1)]
N_HIST = (H1_START - HIST_START).days

GENERAL, STORAGE, RESERVE = 36, 12, 6
HOSTS = GENERAL + STORAGE

# Physics (levels and sources in the design note's ## Draw and ## Ladder).
SIG_WORK, SIG_ENV = 0.08, 0.33
FAILSLOW_RATE = 1.6                      # episodes per host per half
FAILSLOW_MEDIAN_H, FAILSLOW_SIG = 16.0, 0.6
FAILSLOW_FACTOR = (6.0, 10.0)            # slowdown of fully disk-bound work
HEAVY_M = (3.0, 18.0)                    # heavy-shard work multiplier, log-uniform
VICTIM = (1.5, 1.9)                      # co-tenant slowdown under a heavy shard
LAUNCH_DELAY = (60.0, 140.0)             # seconds from trigger to a reserve copy running (pilot)
COMMIT = (1.5, 3.0)                      # minutes, commit step after the last shard
LOAD_RETRY_P = 0.004

# Families. SLA job: (job, deliverable, shards, expected minutes, local start minute after 18:00, slack,
#                     credit band 1 EUR, feed late probability, feed late mean minutes)
FAMILIES = {
    'CSET': dict(name='Card settlement', q=0.15, qload=0.15, ph=0.022, phl=0.010, place='general',
                 victim=VICTIM, load=(6, 26, 20), sig=SIG_WORK, sla=[
                     ('cset_merchant_settlement', 'CS-01', 24, 22, 60, 24, 2200, 0.02, 30),
                     ('cset_scheme_reconciliation', 'CS-02', 20, 25, 140, 26, 2000, 0.02, 30),
                     ('cset_posting_extract', 'CS-03', 28, 18, 220, 22, 2100, 0.02, 30)]),
    'PCLR': dict(name='Payments clearing', q=0.90, qload=0.15, ph=0.001, phl=0.001, place='general',
                 victim=VICTIM, load=(6, 26, 18), sig=SIG_WORK, sla=[
                     ('pclr_sct_inbound', 'PC-01', 14, 12, 60, 14, 4800, 0.02, 20),
                     ('pclr_sdd_collections', 'PC-02', 12, 13, 190, 14, 4600, 0.02, 20),
                     ('pclr_inst_settlement_file', 'PC-03', 16, 11, 320, 13, 4800, 0.02, 20)]),
    'TXIX': dict(name='Transaction search index', q=0.90, qload=0.90, ph=0.002, phl=0.002, place='storage',
                 victim=VICTIM, load=(8, 26, 22), sig=SIG_WORK, sla=[
                     ('txix_card_tx_index', 'TX-01', 20, 25, 80, 26, 1100, 0.10, 50),
                     ('txix_account_tx_index', 'TX-02', 22, 22, 180, 26, 1000, 0.10, 50),
                     ('txix_statement_search', 'TX-03', 18, 28, 280, 24, 1100, 0.10, 50)]),
    'REGR': dict(name='Regulatory reporting', q=0.90, qload=0.15, ph=0.001, phl=0.001, place='general',
                 victim=VICTIM, load=(6, 26, 16), sig=SIG_WORK, sla=[
                     ('regr_finrep_extract', 'RG-01', 14, 12, 420, 12, 4300, 0.02, 20),
                     ('regr_corep_liquidity', 'RG-02', 12, 13, 540, 12, 4200, 0.02, 20),
                     ('regr_anacredit_delta', 'RG-03', 16, 11, 660, 12, 4300, 0.02, 20)]),
    'RISK': dict(name='Risk aggregation', q=0.15, qload=0.15, ph=0.002, phl=0.002, place='general',
                 victim=(2.6, 3.4), load=(6, 26, 20), sig=SIG_WORK, sla=[
                     ('risk_market_var_cube', 'RK-01', 28, 13, 100, 10, 1900, 0.02, 20),
                     ('risk_credit_exposure_cube', 'RK-02', 24, 14, 230, 10, 1900, 0.02, 20),
                     ('risk_limits_snapshot', 'RK-03', 24, 12, 340, 9, 1800, 0.02, 20)]),
    'CAMS': dict(name='Customer analytics scoring', q=0.15, qload=0.15, ph=0.002, phl=0.002, place='general',
                 victim=VICTIM, load=(10, 30, 18), sig=0.35, sla=[
                     ('cams_next_best_offer', 'CA-01', 34, 16, 110, 40, 1300, 0.08, 40),
                     ('cams_churn_scores', 'CA-02', 32, 18, 240, 40, 1300, 0.08, 40),
                     ('cams_campaign_audiences', 'CA-03', 34, 15, 360, 38, 1300, 0.08, 40)]),
}
FAMILY_ORDER = ['CSET', 'PCLR', 'TXIX', 'REGR', 'RISK', 'CAMS']
LOAD_NAMES = {
    'CSET': ['cset_auth_match', 'cset_chargeback_feed', 'cset_interchange_calc', 'cset_merchant_fees',
             'cset_dispute_aging', 'cset_bin_refresh'],
    'PCLR': ['pclr_returns_sweep', 'pclr_iban_validate', 'pclr_sanctions_hits', 'pclr_fx_rates_apply',
             'pclr_liquidity_forecast', 'pclr_archive_rollup'],
    'TXIX': ['txix_segment_merge', 'txix_tokenise', 'txix_dedupe_merchants', 'txix_geo_enrich',
             'txix_snapshot_compact', 'txix_category_tags', 'txix_mcc_backfill', 'txix_reindex_hot'],
    'REGR': ['regr_gl_mapping', 'regr_counterparty_master', 'regr_collateral_join', 'regr_validation_rules',
             'regr_xbrl_render', 'regr_audit_trail'],
    'RISK': ['risk_position_load', 'risk_curve_build', 'risk_scenario_shocks', 'risk_greeks',
             'risk_pnl_explain', 'risk_backtest_window'],
    'CAMS': ['cams_feature_daily', 'cams_feature_weekly', 'cams_web_sessions', 'cams_app_events',
             'cams_propensity_train', 'cams_segment_refresh', 'cams_consent_filter', 'cams_contact_policy',
             'cams_uplift_eval', 'cams_export_crm'],
}


def local_to_min(d, minute_after_18):
    """Minutes from EPOCH for a wall-clock time in Vienna, given as minutes after 18:00 of business date d."""
    wall = datetime(d.year, d.month, d.day, 18, 0) + timedelta(minutes=float(minute_after_18))
    aware = wall.replace(tzinfo=VIENNA)
    return (aware.astimezone(UTC) - EPOCH).total_seconds() / 60.0


def build_jobs():
    """The job catalogue: every job with its family, schedule, shards, expected minutes and SLA terms."""
    jobs = []
    for fam in FAMILY_ORDER:
        F = FAMILIES[fam]
        for (jn, dv, n, E, sched, slack, credit, fp, fm) in F['sla']:
            dl = sched + E * 1.6 + 2.5 + slack + 6
            dl = 5 * int(np.ceil(dl / 5.0))
            jobs.append(dict(family=fam, job=jn, deliverable='SLA-' + dv, sla=True, shards=n, E=float(E),
                             sched=float(sched), deadline=float(dl), credit=float(credit), q=F['q'],
                             ph=F['ph'], feed_p=fp, feed_mean=fm, sig=F['sig']))
        k, nl, El = F['load']
        for t in range(k):
            sched = 20 + t * (700.0 / k)
            jobs.append(dict(family=fam, job=LOAD_NAMES[fam][t], deliverable=None, sla=False, shards=nl,
                             E=float(El), sched=float(round(sched / 5.0) * 5), deadline=None, credit=0.0,
                             q=F['qload'], ph=F['phl'], feed_p=0.02, feed_mean=20, sig=F['sig']))
    for j, J in enumerate(jobs):
        J['jid'] = j
    return jobs


def simulate(seed=214):
    rng = np.random.default_rng(seed)
    jobs = build_jobs()
    total_min = (len(NIGHTS) + 1) * 1440.0
    # fail-slow episodes
    eps = []
    for h in range(HOSTS):
        for _ in range(rng.poisson(FAILSLOW_RATE * len(NIGHTS) / 181.0)):
            s = rng.uniform(0, total_min)
            dur = 60.0 * float(np.clip(np.exp(rng.normal(np.log(FAILSLOW_MEDIAN_H), FAILSLOW_SIG)), 4, 72))
            eps.append((h, s, s + dur, rng.uniform(*FAILSLOW_FACTOR)))
    eps = np.array(eps, dtype=float).reshape(-1, 4)
    storage = np.arange(GENERAL, HOSTS)
    cols = {k: [] for k in ['jid', 'night', 'shard', 'host', 'start', 'Wwork', 'env', 'q', 'heavy', 'm',
                            'E', 'vlo', 'vhi']}
    runs = []
    for J in jobs:
        F = FAMILIES[J['family']]
        n = J['shards']
        for d_i, d in enumerate(NIGHTS):
            sched_min = local_to_min(d, J['sched'])
            late = rng.random() < J['feed_p']
            land = sched_min - 10 + (rng.exponential(J['feed_mean']) if late else rng.uniform(0, 8))
            start = max(sched_min, land) + rng.uniform(0.3, 1.5)
            vw = np.exp(rng.normal(0, J['sig'], n))
            heavy = rng.random(n) < J['ph']
            m = np.where(heavy, np.exp(rng.uniform(np.log(HEAVY_M[0]), np.log(HEAVY_M[1]), n)), 1.0)
            if F['place'] == 'storage':
                hosts = rng.choice(storage, n)
            elif J['sla']:
                hosts = rng.choice(GENERAL, n, replace=False)
            else:
                hosts = rng.integers(0, GENERAL, n)
            cols['jid'].append(np.full(n, J['jid'])); cols['night'].append(np.full(n, d_i))
            cols['shard'].append(np.arange(n)); cols['host'].append(hosts)
            cols['start'].append(start + rng.uniform(0, 0.6, n)); cols['Wwork'].append(J['E'] * vw * m)
            cols['env'].append(np.exp(rng.normal(0, SIG_ENV, n))); cols['q'].append(np.full(n, J['q']))
            cols['heavy'].append(heavy); cols['m'].append(m); cols['E'].append(np.full(n, J['E']))
            cols['vlo'].append(np.full(n, F['victim'][0])); cols['vhi'].append(np.full(n, F['victim'][1]))
            runs.append(dict(jid=J['jid'], night=d_i, sched=sched_min, land=land, start=start,
                             commit=rng.uniform(*COMMIT)))
    R = {k: np.concatenate(v) for k, v in cols.items()}
    N = len(R['jid'])
    hw = np.ones(N)
    for (h, s, e, f) in eps:
        sel = (R['host'] == h) & (R['start'] >= s) & (R['start'] < e)
        hw[sel] = 1 + R['q'][sel] * (f - 1)
    mix = R['heavy'] & (hw > 1)
    R['Wwork'][mix] /= R['m'][mix]
    R['m'][mix] = 1.0
    R['heavy'][mix] = False
    base = R['Wwork'] * R['env'] * hw
    rt = base.copy()
    order = np.lexsort((R['start'], R['host']))
    bnd = np.searchsorted(R['host'][order], np.arange(HOSTS + 1))
    for c in np.where(R['heavy'])[0]:
        h = R['host'][c]
        cs, ce = R['start'][c], R['start'][c] + base[c]
        seg = order[bnd[h]:bnd[h + 1]]
        s = R['start'][seg]
        cand = seg[np.searchsorted(s, cs - 600):np.searchsorted(s, ce)]
        js, je = R['start'][cand], R['start'][cand] + base[cand]
        ov = np.clip(np.minimum(je, ce) - np.maximum(js, cs), 0, None)
        ov[cand == c] = 0
        cf = R['vlo'][cand] + rng.random(len(cand)) * (R['vhi'][cand] - R['vlo'][cand])
        rt[cand] += ov * (cf - 1)
    R['rt'] = rt
    R['end'] = R['start'] + rt
    R['hw'] = hw
    R['launch_delay'] = rng.uniform(*LAUNCH_DELAY, N) / 60.0
    R['backup_env'] = np.exp(rng.normal(0, SIG_ENV, N))
    return dict(R=R, jobs=jobs, runs=runs, eps=eps, seed=seed)
