"""Paper world for task141 architecture 3: felony probation revocations on two clocks.

Ordinary violation petitions arrive on the time-since-start clock (front-loaded, scaled by the risk score); before
a term lapses, officers file a petition on cases with an unresolved matter so the court keeps jurisdiction (the
review clock, days to scheduled expiration). A 2027 Act caps felony terms at 24 months and ends every felony term
already past 24 months on 31 March 2027. The record runs to the extract; the truth is the generator re-run forward
from each case's state at the extract, many times; routes see only the record.
"""
import numpy as np, sys

P = dict(
    fel_starts_per_month=210, mis_starts_per_month=150,
    terms=(18, 24, 30, 36, 42, 48, 60, 72), term_w=(0.05, 0.12, 0.06, 0.30, 0.07, 0.15, 0.20, 0.05),
    h0=0.030, h_inf=0.0075, h_tau=7.0,     # ordinary monthly petition hazard h_inf + (h0 - h_inf) exp(-m / tau)
    score_beta=0.075,
    conv_ord=0.48, conv_rev=0.50,
    p_rev=0.22, rev_lo=6, rev_hi=75,         # review petition: probability, filed this many days before expiry
    lag_mean=72.0, lag_shape=3.0,
    et_hazard=0.006, abscond=0.0012,
)
M = 30.4375
DAY0 = np.datetime64('2017-01-01')


def d(s):
    return int((np.datetime64(s) - DAY0).astype(int))


EXTRACT = d('2026-09-30')
ACT = d('2027-01-01')
TRANS = d('2027-03-31')
Y0, Y1 = d('2027-01-01'), d('2027-12-31')


def act_expiry(start, orig):
    """the Act's expiry for a felony term: new terms capped at 24 months; a term running on 1 January 2027 ends on
    the earlier of its original expiry and 24 months from start, but not before 31 March 2027"""
    if orig < ACT:
        return orig
    cap = start + int(round(24 * M))
    if start >= ACT:
        return min(orig, cap)
    return min(orig, max(cap, TRANS))


def hazard(p, m, score):
    return (p['h_inf'] + (p['h0'] - p['h_inf']) * np.exp(-m / p['h_tau'])) * np.exp(p['score_beta'] * (score - 10))


def step_case(rng, p, c, t_from, t_to, state, exp_day, log):
    """advance one case from day t_from to t_to (exclusive); state: dict(pending_until, reviewed, closed)"""
    start = c['start']
    m = int((t_from - start) // M)
    while True:
        if state['closed'] is not None:
            return
        m_start = start + int(round(m * M))
        m_end = start + int(round((m + 1) * M))
        if m_start >= t_to:
            return
        if m_start >= exp_day:
            if state['pending_until'] < m_start:
                state['closed'] = (exp_day, 'EXPIRED')
            return
        lo = max(m_start, t_from)
        win_open = exp_day - 90
        if (not state['reviewed']) and m_end > win_open and lo <= max(win_open, lo) and state['pending_until'] < win_open:
            if max(win_open, lo) < t_to:
                state['reviewed'] = True
                if rng.random() < p['p_rev']:
                    f = exp_day - int(rng.triangular(p['rev_lo'], p['rev_lo'] + 12, p['rev_hi']))
                    f = max(f, lo)
                    rev = rng.random() < p['conv_rev']
                    adm = f + int(rng.gamma(p['lag_shape'], p['lag_mean'] / p['lag_shape']))
                    log.append(dict(case=c['id'], file=f, kind='REVIEW', revoked=rev, decided=adm))
                    state['had_petition'] = True
                    state['pending_until'] = adm
                    if rev:
                        state['closed'] = (adm, 'REVOKED')
                        return
        if lo >= t_to:
            return
        if m_end > state['pending_until'] and m_end > t_from:
            frac = 1.0 if m_start >= t_from else (m_end - t_from) / max(m_end - m_start, 1)
            if rng.random() < hazard(p, m, c['score']) * frac:
                f = max(max(m_start, t_from) + int(rng.integers(0, max(1, min(30, m_end - max(m_start, t_from))))), state['pending_until'] + 1)
                if f < exp_day and f < t_to:
                    rev = rng.random() < p['conv_ord']
                    adm = f + int(rng.gamma(p['lag_shape'], p['lag_mean'] / p['lag_shape']))
                    log.append(dict(case=c['id'], file=f, kind='ORDINARY', revoked=rev, decided=adm))
                    state['had_petition'] = True
                    state['pending_until'] = adm
                    if rev:
                        state['closed'] = (adm, 'REVOKED')
                        return
            if m >= 18 and not state.get('had_petition') and rng.random() < p['et_hazard'] * frac:
                if state['pending_until'] < m_end:
                    state['closed'] = (m_end, 'EARLY_TERM')
                    return
            if rng.random() < p['abscond'] * frac:
                state['closed'] = (m_end, 'ABSCOND')
                return
        m += 1


def make_cases(rng, p, d_from, d_to, felony_only=False, id0=0):
    out = []
    nm = int((d_to - d_from) / M) + 1
    k = id0
    for mi in range(nm):
        base = d_from + int(mi * M)
        for fel in ((True,) if felony_only else (True, False)):
            n = rng.poisson(p['fel_starts_per_month'] if fel else p['mis_starts_per_month'])
            for _ in range(n):
                s = base + int(rng.integers(0, 30))
                if s >= d_to:
                    continue
                term = int(rng.choice(p['terms'], p=p['term_w'])) if fel else 12
                sc = int(np.clip(round(rng.normal(10.5 if fel else 8.0, 3.6)), 0, 20))
                out.append(dict(id=k, start=s, term=term, score=sc, fel=fel, orig=s + int(round(term * M))))
                k += 1
    return out


def record(seed, p=P):
    rng = np.random.default_rng(seed)
    cases = make_cases(rng, p, 0, EXTRACT)
    log, states = [], {}
    for c in cases:
        st = dict(pending_until=-1, reviewed=False, closed=None)
        exp_day = act_expiry(c['start'], c['orig']) if c['fel'] else c['orig']
        step_case(rng, p, c, c['start'], EXTRACT + 1, st, exp_day, log)
        states[c['id']] = st
    return cases, log, states


def truth(seed, cases, log, states, p=P, reps=12):
    """expected felony revocation admissions dated in 2027 under the Act, given the record"""
    res = []
    by_case = {}
    for e in log:
        by_case.setdefault(e['case'], []).append(e)
    for r in range(reps):
        rng = np.random.default_rng(10_000 + seed * 100 + r)
        n = 0
        for c in cases:
            if not c['fel']:
                continue
            st0 = states[c['id']]
            if st0['closed'] is not None and st0['closed'][0] <= EXTRACT:
                continue
            st = dict(pending_until=st0['pending_until'], reviewed=st0['reviewed'], closed=None, had_petition=st0.get('had_petition', False))
            # a petition pending at the extract: its decision is still to come; re-draw it
            pend = [e for e in by_case.get(c['id'], []) if e['file'] <= EXTRACT < e['decided']]
            exp_day = act_expiry(c['start'], c['orig'])
            if pend:
                e = pend[-1]
                rev = rng.random() < (p['conv_rev'] if e['kind'] == 'REVIEW' else p['conv_ord'])
                lag = int(rng.gamma(p['lag_shape'], p['lag_mean'] / p['lag_shape']))
                adm = max(e['file'] + lag, EXTRACT + 1 + int(rng.integers(0, 60)))
                if rev:
                    n += Y0 <= adm <= Y1
                    continue
                st['pending_until'] = adm
            fut = []
            step_case(rng, p, c, EXTRACT + 1, Y1 + 400, st, exp_day, fut)
            n += sum(1 for e in fut if e['revoked'] and Y0 <= e['decided'] <= Y1)
        new = make_cases(rng, p, EXTRACT + 1, Y1, felony_only=True, id0=10**7)
        for c in new:
            st = dict(pending_until=-1, reviewed=False, closed=None)
            fut = []
            step_case(rng, p, c, c['start'], Y1 + 400, st, act_expiry(c['start'], c['orig']), fut)
            n += sum(1 for e in fut if e['revoked'] and Y0 <= e['decided'] <= Y1)
        res.append(n)
    return float(np.mean(res)), float(np.std(res))


if __name__ == '__main__':
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 141
    cases, log, states = record(seed)
    fel_ids = {c['id'] for c in cases if c['fel']}
    adm = np.array([e['decided'] for e in log if e['revoked'] and e['case'] in fel_ids and e['decided'] <= EXTRACT])
    print('cases', len(cases), 'felony', len(fel_ids), 'petitions', len(log))
    print('felony revocation admissions in the 12 months to the extract', int(((adm > EXTRACT - 365)).sum()))
    act = [c for c in cases if c['fel'] and (states[c['id']]['closed'] is None or states[c['id']]['closed'][0] > EXTRACT)]
    print('felony active at the extract', len(act), 'past 24 months on 1 Jan 2027',
          sum(1 for c in act if ACT - c['start'] >= 24 * M and c['orig'] >= ACT))
    rv = [e for e in log if e['kind'] == 'REVIEW' and e['case'] in fel_ids]
    print('review petitions in the record', len(rv), 'ordinary', sum(1 for e in log if e['kind'] == 'ORDINARY' and e['case'] in fel_ids))
    t, s = truth(seed, cases, log, states, reps=int(sys.argv[2]) if len(sys.argv) > 2 else 6)
    print('truth: felony revocation admissions dated in 2027 under the Act %.1f (sd over reps %.1f)' % (t, s))
