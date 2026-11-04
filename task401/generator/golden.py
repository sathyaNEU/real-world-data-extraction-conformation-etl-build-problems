"""task401 golden: the call, the readers, the literal executions and the asks, computed from the shipped files under
target/ alone. golden.run() writes generator/figures.json and returns the figures; the readers and profiles are used
by checks.py and ceiling.py."""
import os, json, glob
from datetime import date, datetime, timedelta
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), 'target')
W0 = date(2024, 1, 1)
EXTRACT = date(2026, 3, 16)
YEAR0, YEAR1 = date(2026, 2, 2), date(2027, 2, 1)          # the 2026-27 membership year
PREV0 = date(2025, 2, 3)                                    # the 2025-26 membership year began
SHIFT = 364                                                 # the same weeks of the previous membership year
DATES = {'C': date(2026, 1, 12), 'A': date(2026, 2, 2), 'D': date(2026, 2, 2), 'E': date(2026, 2, 9), 'B': date(2026, 2, 16)}
NAMES = {'A': 'the Rewards closure', 'B': 'the member care calls', 'C': 'the daytime timetable', 'D': 'the legacy terms letters',
         'E': 'the shorter hours at Northgate and Westcroft'}
HOURS_SITES = ('Northgate', 'Westcroft')


def dn(d): return (d - W0).days


def load():
    reg = pd.read_csv(os.path.join(T, 'membership_register_2026-03-16.csv'), dtype=str)
    reg = reg.sort_values('membership_no').reset_index(drop=True)
    ix = {m: i for i, m in enumerate(reg.membership_no)}
    n = len(reg)
    joined = np.array([dn(date.fromisoformat(x)) for x in reg.joined])
    acct = np.array([dn(date.fromisoformat(x)) if isinstance(x, str) else 10 ** 6 for x in reg.rewards_account_opened])
    legacy = reg.tariff_code.str.startswith('L-').values
    home = reg.home_centre.values
    canc = pd.read_csv(os.path.join(T, glob.glob(os.path.join(T, 'cancellation_requests_*.csv'))[0]), dtype=str)
    canc['d'] = [dn(date.fromisoformat(x[:10])) for x in canc.received]
    first = canc.sort_values(['received', 'request_ref']).drop_duplicates('membership_no')
    freq = np.full(n, 10 ** 6); freq[[ix[m] for m in first.membership_no]] = first.d.values
    reason = np.full(n, '', dtype=object); reason[[ix[m] for m in first.membership_no]] = first.reason.values
    v = pd.read_parquet(glob.glob(os.path.join(T, 'access_weekly_usage_*.parquet'))[0])
    wk = np.array([(d - W0).days // 7 for d in v.week_commencing])
    mi = v.membership_no.map(ix).values
    NWK = wk.max() + 1
    VIS = np.zeros((n, NWK), bool); VIS[mi, wk] = True
    ENT = np.zeros((n, NWK), np.int32); np.add.at(ENT, (mi, wk), v.gate_entries.values.astype(np.int32))
    cen = v.centre.values
    bk = pd.read_parquet(glob.glob(os.path.join(T, 'class_bookings_*.parquet'))[0])
    st = pd.to_datetime(bk.session_start)
    daytime = (st.dt.weekday < 5) & (st.dt.hour < 17)
    def booked(a, b):
        sel = daytime & (st >= pd.Timestamp(a)) & (st <= pd.Timestamp(b) + pd.Timedelta(hours=23, minutes=59))
        m = np.zeros(n, bool); m[[ix[x] for x in bk.membership_no[sel].unique()]] = True
        return m
    let = pd.read_excel(os.path.join(T, 'legacy_terms_letters_2026-02.xlsx'), dtype=str)
    calls = pd.read_csv(glob.glob(os.path.join(T, 'member_care_calls_*.csv'))[0], dtype=str)
    calls['membership_no'] = calls.member.str.zfill(6)
    called = np.zeros(n, bool); called[[ix[m] for m in calls.membership_no if m in ix]] = True
    S = dict(reg=reg, ix=ix, n=n, joined=joined, acct=acct, legacy=legacy, home=home, freq=freq, reason=reason,
             VIS=VIS, ENT=ENT, v=v, vwk=wk, vmi=mi, vcen=cen, letters=let, called=called, calls=calls)
    yr = lambda d: d - timedelta(days=SHIFT)
    S['R26'] = {'A': acct <= dn(date(2026, 1, 31)), 'C': booked(date(2025, 10, 13), date(2026, 1, 11)), 'D': legacy,
                'E': np.isin(home, HOURS_SITES), 'B': called}
    S['R25'] = {'A': acct <= dn(yr(date(2026, 1, 31))), 'C': booked(yr(date(2025, 10, 13)), yr(date(2026, 1, 11))), 'D': legacy,
                'E': np.isin(home, HOURS_SITES)}
    return S


def on_books(S, d):
    """On the books and not leaving on day d: joined before d, no request to leave received before d."""
    x = dn(d); return (S['joined'] < x) & (S['freq'] >= x)


def idle(S, d, weeks=4):
    w = dn(d) // 7
    return on_books(S, d) & ~S['VIS'][:, max(0, w - weeks):w].any(1)


def leavers(S, m, a, b):
    return m & (S['freq'] >= dn(a)) & (S['freq'] < dn(b))


def so_far(S, k, ref=EXTRACT):
    d = DATES[k]; d0 = d - timedelta(days=SHIFT)
    n1 = S['R26'][k] & on_books(S, d); n0 = S['R25'][k] & on_books(S, d0)
    r1 = leavers(S, n1, d, ref).sum() / n1.sum(); r0 = leavers(S, n0, d0, ref - timedelta(days=SHIFT)).sum() / n0.sum()
    return (r1 - r0) * n1.sum()


HZ = {'6m': 182, '9m': 273, '10m': 304, '12m': 364, 'year': (date(2026, 2, 2) - (EXTRACT - timedelta(days=SHIFT))).days}


def project(S, k, thr=4, hz='year', src='reach', base='yoy', snap='extract'):
    """A change's cost over the membership year: its excess cancellations so far, plus its excess of members with no
    visit in the last thr weeks over the same date of the previous membership year, times the share of last year's such
    members (in its reach, or every member) who went on to cancel within hz."""
    r26, r25 = S['R26'][k], S['R25'][k]
    d1 = EXTRACT if snap == 'extract' else date(2026, 2, 2)
    d0 = d1 - timedelta(days=SHIFT)
    a1, a0 = on_books(S, d1) & r26, on_books(S, d0) & r25
    i1, i0 = (idle(S, d1, thr) & r26).sum() / a1.sum(), (idle(S, d0, thr) & r25).sum() / a0.sum()
    ex = (i1 - i0) * a1.sum()
    if base == 'did':
        b1, b0 = on_books(S, d1) & ~r26, on_books(S, d0) & ~r25
        ex -= ((idle(S, d1, thr) & ~r26).sum() / b1.sum() - (idle(S, d0, thr) & ~r25).sum() / b0.sum()) * a1.sum()
    c0 = EXTRACT - timedelta(days=SHIFT)
    coh = idle(S, c0, thr) & (r25 if src == 'reach' else True)
    conv = leavers(S, coh, c0, c0 + timedelta(days=HZ[hz])).sum() / coh.sum()
    return so_far(S, k) + ex * conv, dict(so_far=so_far(S, k), excess_idle=ex, conv=conv, n=int(a1.sum()))


def main_call(S):
    G, parts = {}, {}
    for k in 'ACDE':
        G[k], parts[k] = project(S, k)
    order = sorted(G, key=G.get, reverse=True)
    var = {}
    for thr in (3, 4, 5, 6, 8):
        for hz in HZ:
            for src in ('reach', 'pooled'):
                for base in ('yoy', 'did'):
                    for snap in ('extract', 'feb1'):
                        g = {k: project(S, k, thr, hz, src, base, snap)[0] for k in 'ACDE'}
                        var['t%d_%s_%s_%s_%s' % (thr, hz, src, base, snap)] = g
    return dict(G=G, parts=parts, call=order[0], runner=order[1], var=var, B_so_far=so_far(S, 'B') if False else None)


def weekly_series(S, mask, w_lo, w_hi):
    rows = []
    for w in range(w_lo, w_hi):
        s0, s1 = dn(W0 + timedelta(days=7 * w)), dn(W0 + timedelta(days=7 * w + 6))
        alive = mask & (S['joined'] <= s1) & (S['freq'] >= s0)
        act = alive & S['VIS'][:, max(0, w - 3):w + 1].any(1)
        rows.append((alive.sum(), S['ENT'][alive, w].sum(), act.sum()))
    return np.array(rows, float)


def readers(S):
    """The first looks the design is screened against, each naming a change: cancellations in each reach after against
    before its date (and net of 2025), the 28-day active share, active count and visits per member year on year, the
    count reader (cancellations plus lost actives), the centres, the stated reasons, and the literal executions."""
    out = {}
    fq = S['freq']
    best, bby = {}, {}
    for k, d in DATES.items():
        r = S['R26'][k]; vals, valy = [], []
        for ww in (2, 4, 6):
            for lag in (0, 2, 4, 6, 8):
                a = d + timedelta(weeks=lag); b = a + timedelta(weeks=ww)
                if b > EXTRACT: continue
                x = leavers(S, r, a, b).sum() - leavers(S, r, a - timedelta(weeks=ww), a).sum()
                vals.append(x)
                if k != 'B':
                    q = S['R25'][k]; a0 = a - timedelta(days=SHIFT); b0 = b - timedelta(days=SHIFT)
                    valy.append(x - (leavers(S, q, a0, b0).sum() - leavers(S, q, a0 - timedelta(weeks=ww), a0).sum()))
        best[k] = max(vals) if vals else -10 ** 9
        if valy: bby[k] = max(valy)
    out['FL'] = max(best, key=best.get); out['FLY'] = max(bby, key=bby.get)
    wcut = dn(EXTRACT) // 7
    eng = {'share': {}, 'vpm': {}, 'count': {}}
    for k in 'ACDE':
        w = dn(DATES[k]) // 7
        a = weekly_series(S, S['R26'][k], w - 6, wcut); b = weekly_series(S, S['R25'][k], w - 6 - 52, wcut - 52)
        for meas in eng:
            if meas == 'share': ma, mb = a[:, 2] / a[:, 0], b[:, 2] / b[:, 0]
            elif meas == 'vpm': ma, mb = a[:, 1] / a[:, 0], b[:, 1] / b[:, 0]
            else: ma, mb = a[:, 2], b[:, 2]
            gap = ma - mb
            dl = gap[7:].mean() - gap[:6].mean()
            eng[meas][k] = dl / (abs(ma[:6].mean()) if meas != 'count' else 1.0)
    for meas in eng:
        out['ENG_' + meas] = min(eng[meas], key=eng[meas].get)
    out['ENG'] = eng
    sf = {k: so_far(S, k) for k in 'ACDE'}
    harm = {k: sf[k] + max(0.0, -eng['count'][k]) for k in 'ACDE'}
    out['HARM'] = harm; out['HARM_top'] = max(harm, key=harm.get)
    out['HARM_margin'] = max(v for k, v in harm.items() if k != 'A') / harm['A']
    # centres: visits per member at each centre after 9 February against before, year on year
    v = S['v']; cen = S['vcen']; wk = S['vwk']
    wE = dn(DATES['E']) // 7
    falls = {}
    ecw = pd.Series(v.gate_entries.values.astype(np.int64)).groupby([cen, wk]).sum().to_dict()
    for c in sorted(set(cen)):
        homec = S['home'] == c
        def vpm(w):
            alive = homec & (S['joined'] <= dn(W0 + timedelta(days=7 * w + 6))) & (S['freq'] >= dn(W0 + timedelta(days=7 * w)))
            return ecw.get((c, w), 0) / max(alive.sum(), 1)
        gap = np.array([vpm(w) - vpm(w - 52) for w in range(wE - 6, wcut)])
        falls[c] = (gap[7:].mean() - gap[:6].mean()) / np.mean([vpm(w) for w in range(wE - 6, wE)])
    out['CENTRE_top'] = min(falls, key=falls.get); out['CENTRE_falls'] = falls
    # stated reasons
    mapr = {'D': 'Price or terms', 'E': 'Opening hours', 'C': 'Classes or timetable'}
    sr = {}
    for k, rs in mapr.items():
        d = DATES[k]; m = S['reason'] == rs
        sr[k] = int(leavers(S, m, d, EXTRACT).sum() - leavers(S, m, d - timedelta(days=SHIFT), EXTRACT - timedelta(days=SHIFT)).sum())
    out['SR'] = sr; out['SR_top'] = max(sr, key=sr.get)
    # literal executions and the flexible crackers on the cancellations to the extract
    a, b = YEAR0, EXTRACT; a0, b0 = a - timedelta(days=SHIFT), b - timedelta(days=SHIFT)
    def yoy(k, rest=False):
        q1, q0 = S['R26'][k], S['R25'][k]
        n1 = q1 & on_books(S, a); n0 = q0 & on_books(S, a0)
        x = (leavers(S, n1, a, b).sum() / n1.sum() - leavers(S, n0, a0, b0).sum() / n0.sum()) * n1.sum()
        if rest:
            m1 = ~q1 & on_books(S, a); m0 = ~q0 & on_books(S, a0)
            x -= (leavers(S, m1, a, b).sum() / m1.sum() - leavers(S, m0, a0, b0).sum() / m0.sum()) * n1.sum()
        return x
    est = {k: yoy(k, True) for k in 'ACDE'}; yo = {k: yoy(k) for k in 'ACDE'}
    sc = 365.0 / (b - a).days
    lit = {'L1_against_rest': dict(est), 'L2_year_on_year': dict(yo), 'L3_all_scaled': {k: x * sc for k, x in est.items()},
           'L4_ongoing_scaled_yoy': {'A': yo['A'] * sc, 'C': yo['C'] * sc, 'D': yo['D'], 'E': yo['E'] * sc},
           'L5_ongoing_scaled_rest': {'A': est['A'] * sc, 'C': est['C'] * sc, 'D': est['D'], 'E': est['E'] * sc}}
    out['LIT'] = {nm: max(x, key=x.get) for nm, x in lit.items()}
    out['LIT_values'] = lit
    out['so_far'] = sf
    return out


def run():
    import asks
    S = load(); mc = main_call(S); rd = readers(S)
    till = asks.till_count('golden'); dd = asks.dd_count('golden')
    G, P = mc['G'], mc['parts']
    order = sorted(G, key=G.get, reverse=True)
    F = {'call': NAMES[mc['call']], 'call_key': mc['call'], 'order': order,
         'cost': {k: int(round(G[k], -1)) for k in G},
         'so_far': {k: int(round(P[k]['so_far'])) for k in G},
         'excess_idle': {k: int(round(P[k]['excess_idle'])) for k in G},
         'conv_pct': {k: round(100 * P[k]['conv'], 1) for k in G},
         'reach_at_extract': {k: P[k]['n'] for k in G},
         'lead': round(G[order[0]] / G[order[1]], 2),
         'admissions': {'%s %s' % k: int(round(v, -1)) for k, v in till.items()},
         'fees': {'%s %s' % k: int(round(v, -2)) for k, v in dd.items()},
         'extract': EXTRACT.isoformat(), 'year': [YEAR0.isoformat(), (YEAR1 - timedelta(days=1)).isoformat()],
         'fewer_not_visiting': {k: int(round(-P[k]['excess_idle'])) for k in G},
         'constants': {'idle_days': 28, 'extract_day': EXTRACT.day, 'previous_year_offset_days': SHIFT,
                       'schedule_sections': [4.1, 4.3], 'swim_and_gym_half_line_gbp': 4.70, 'admissions_unit': 10, 'fees_unit_gbp': 100}}
    json.dump(F, open(os.path.join(HERE, 'figures.json'), 'w'), indent=1)
    return dict(F=F, S=S, mc=mc, rd=rd, till=till, dd=dd)
