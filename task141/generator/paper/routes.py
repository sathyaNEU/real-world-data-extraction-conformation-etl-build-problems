"""Forecast routes for the 2027 felony revocation admissions, computed from the record only.
persistence | one-clock admissions hazard by month since start (pooled, and by original term) | the two-clock
golden (ordinary petitions on the start clock, a review window before each scheduled expiry, conversion and lag).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import sim_rev as S

M = S.M


def visible(cases, log, states):
    """what the record shows at the extract"""
    fel = [c for c in cases if c['fel']]
    pet = []
    for e in log:
        if e['file'] > S.EXTRACT:
            continue
        v = dict(case=e['case'], file=e['file'])
        if e['decided'] <= S.EXTRACT:
            v['decided'] = e['decided']; v['revoked'] = e['revoked']
        else:
            v['decided'] = None; v['revoked'] = None
        pet.append(v)
    close = {}
    for c in cases:
        st = states[c['id']]
        if st['closed'] is not None and st['closed'][0] <= S.EXTRACT:
            close[c['id']] = st['closed']
    return fel, pet, close


def new_starts_rate(fel):
    rec = [c for c in fel if S.EXTRACT - 365 < c['start'] <= S.EXTRACT]
    return len(rec) / 12.0, rec


def months_since(c, day):
    return int((day - c['start']) // M)


def admissions_hazard(fel, pet, close, by_term=False, max_m=72):
    """monthly hazard of a revocation admission by month since start, among cases on supervision that month"""
    adm_m = {}
    for p in pet:
        if p['revoked']:
            adm_m[p['case']] = p['decided']
    at, ev = {}, {}
    for c in fel:
        end = close[c['id']][0] if c['id'] in close else S.EXTRACT
        key = c['term'] if by_term else 0
        last = months_since(c, min(end, S.EXTRACT))
        for m in range(0, min(last, max_m) + 1):
            at[(key, m)] = at.get((key, m), 0) + 1
        if c['id'] in adm_m and adm_m[c['id']] <= S.EXTRACT:
            m = months_since(c, adm_m[c['id']])
            ev[(key, m)] = ev.get((key, m), 0) + 1
    h = {k: ev.get(k, 0) / v for k, v in at.items() if v > 0}
    return h


def other_exit_hazard(fel, close, max_m=72):
    at, ev = {}, {}
    for c in fel:
        end = close[c['id']][0] if c['id'] in close else S.EXTRACT
        last = months_since(c, end)
        for m in range(0, min(last, max_m) + 1):
            at[m] = at.get(m, 0) + 1
        if c['id'] in close and close[c['id']][1] in ('EARLY_TERM', 'ABSCOND'):
            ev[last] = ev.get(last, 0) + 1
    return {m: ev.get(m, 0) / at[m] for m in at}


def one_clock(fel, pet, close, by_term=False):
    h = admissions_hazard(fel, pet, close, by_term)
    ex = other_exit_hazard(fel, close)
    rate, _ = new_starts_rate(fel)
    total = 0.0
    active = [c for c in fel if c['id'] not in close]
    revoked_pending = set()
    for c in active:
        exp_day = S.act_expiry(c['start'], c['orig'])
        alive = 1.0
        day = S.EXTRACT + 1
        while day <= S.Y1 and day < exp_day:
            m = months_since(c, day)
            key = (c['term'] if by_term else 0, m)
            hh = h.get(key, h.get((key[0], max(k[1] for k in h if k[0] == key[0])), 0.0))
            if S.Y0 <= day:
                total += alive * hh
            alive *= (1 - hh) * (1 - ex.get(m, 0.0))
            day += int(M)
    # new starts from the extract to the end of 2027 on 24-month terms
    d = S.EXTRACT + 1
    while d <= S.Y1:
        for c0 in range(1):
            alive = rate
            day = d
            while day <= S.Y1:
                m = int((day - d) // M)
                key = (36 if by_term else 0, m)
                hh = h.get(key, 0.0)
                if day >= S.Y0:
                    total += alive * hh
                alive *= (1 - hh) * (1 - ex.get(m, 0.0))
                day += int(M)
        d += int(M)
    return total


def two_clock(fel, pet, close, window=90, score_adjust=True, skip_transition=False, double_count=False):
    """the golden: ordinary petitions on the start clock outside each case's last `window` days, a review window
    probability before each scheduled expiry, conversion by kind, the filing-to-admission lag"""
    byc = {}
    for p in pet:
        byc.setdefault(p['case'], []).append(p)

    def in_window(c, f):
        return c['orig'] - window <= f < c['orig']
    # case-months on supervision, not pending, outside the expiry window: (month since start, score, petition?)
    rows = []
    for c in fel:
        end = close[c['id']][0] if c['id'] in close else S.EXTRACT
        stop = min(end, S.EXTRACT, c['orig'] - window)
        pets = sorted(byc.get(c['id'], []), key=lambda p: p['file'])
        busy = [(p['file'], p['decided'] if p['decided'] is not None else S.EXTRACT) for p in pets]
        m = 0
        while True:
            a0 = c['start'] + int(round(m * M)); b0 = c['start'] + int(round((m + 1) * M))
            if a0 >= stop:
                break
            if not any(x <= a0 < y for x, y in busy):
                hit = any(a0 <= p['file'] < b0 for p in pets)
                rows.append((m, c['score'], 1 if hit else 0))
            m += 1
    R = np.array(rows)
    if score_adjust:
        sc = np.unique(R[:, 1]); xs, ys, ws = [], [], []
        for s_ in sc:
            k = R[:, 1] == s_
            if k.sum() > 300:
                xs.append(s_); ys.append(np.log(max(R[k, 2].sum(), 1) / k.sum())); ws.append(k.sum())
        beta = float(np.polyfit(xs, ys, 1, w=np.sqrt(ws))[0])
    else:
        beta = 0.0
    mult_r = np.exp(beta * (R[:, 1] - 10))
    g0 = {}
    for m in np.unique(R[:, 0]):
        k = R[:, 0] == m
        if k.sum() > 30:
            g0[int(m)] = R[k, 2].sum() / mult_r[k].sum()
    gmax = max(g0)
    # review window probability: cases that reached orig - window on supervision with no pending petition
    reach, wpet = 0, 0
    for c in fel:
        wo = c['orig'] - window
        if c['orig'] > S.EXTRACT - 30:
            continue
        end = close[c['id']][0] if c['id'] in close else S.EXTRACT + 1
        if end <= wo:
            continue
        pets = byc.get(c['id'], [])
        if any(p['file'] < wo and (p['decided'] is None or p['decided'] >= wo) for p in pets):
            continue
        reach += 1
        if any(wo <= p['file'] < c['orig'] for p in pets):
            wpet += 1
    p_win = wpet / reach
    offs = np.array([c['orig'] - p['file'] for c in fel for p in byc.get(c['id'], []) if c['orig'] - window <= p['file'] < c['orig']])
    old = [p for p in pet if p['file'] < S.EXTRACT - 400 and p['decided'] is not None]
    cw = [p['revoked'] for p in old if in_window(CASE[p['case']], p['file'])]
    co = [p['revoked'] for p in old if not in_window(CASE[p['case']], p['file'])]
    conv_w, conv_o = float(np.mean(cw)), float(np.mean(co))
    lags = np.array([p['decided'] - p['file'] for p in old])
    lag_m = float(lags.mean() / M)

    def p_land(f, given_after=None):
        L = lags if given_after is None else lags[lags > given_after - f]
        if len(L) == 0:
            return 0.0
        a_ = f + L
        return float(((a_ >= S.Y0) & (a_ <= S.Y1)).mean())
    ex = other_exit_hazard(fel, close)
    parts = dict(pending=0.0, ordinary=0.0, review=0.0, new=0.0)
    for c in fel:
        if c['id'] in close:
            continue
        exp_day = S.act_expiry(c['start'], c['orig'])
        mult = np.exp(beta * (c['score'] - 10))
        pets = byc.get(c['id'], [])
        pend = [p for p in pets if p['decided'] is None]
        alive = 1.0
        day = S.EXTRACT + 1
        if pend:
            p = pend[-1]
            cv = conv_w if in_window(c, p['file']) else conv_o
            parts['pending'] += cv * p_land(p['file'], given_after=S.EXTRACT)
            alive = 1 - cv
            L = lags[lags > S.EXTRACT - p['file']]
            day = int(p['file'] + np.median(L)) if len(L) else day
        wo = exp_day - window
        while day < min(wo, S.Y1 + 1):
            m = months_since(c, day)
            gg = g0.get(m, g0[gmax]) * mult
            gg = gg / (1 + gg * (1 - conv_o) * lag_m)
            parts['ordinary'] += alive * gg * conv_o * p_land(day + 15)
            alive *= (1 - gg * conv_o) * (1 - ex.get(m, 0.0))
            day += int(M)
        if skip_transition and exp_day == S.TRANS:
            continue
        if double_count:
            # the over-correction: the ordinary hazard carried through the window as well, the review added on top
            d2 = max(day, wo)
            while d2 < min(exp_day, S.Y1 + 1):
                m = months_since(c, d2)
                gg = g0.get(m, g0[gmax]) * mult
                parts['ordinary'] += alive * gg * conv_o * p_land(d2 + 15)
                d2 += int(M)
        if wo <= S.Y1 and exp_day > S.EXTRACT:
            if wo <= S.EXTRACT:
                if any(wo <= q['file'] <= S.EXTRACT for q in pets):
                    continue
                rem = offs[exp_day - offs > S.EXTRACT]
                share = len(rem) / len(offs)
            else:
                rem = offs
                share = 1.0
            if len(rem):
                land = float(np.mean([p_land(exp_day - o) for o in rem[:: max(1, len(rem) // 60)]]))
                parts['review'] += alive * p_win * share * conv_w * land
    rate, rec = new_starts_rate(fel)
    mbar = float(np.mean([np.exp(beta * (c['score'] - 10)) for c in rec]))
    d0 = S.EXTRACT + 1
    while d0 <= S.Y1:
        alive = rate
        day = d0
        while day <= S.Y1:
            m = int((day - d0) // M)
            gg = g0.get(m, g0[gmax]) * mbar
            gg = gg / (1 + gg * (1 - conv_o) * lag_m)
            parts['new'] += alive * gg * conv_o * p_land(day + 15)
            alive *= (1 - gg * conv_o) * (1 - ex.get(m, 0.0))
            day += int(M)
        d0 += int(M)
    return sum(parts.values()), parts, dict(p_win=p_win, conv_w=conv_w, conv_o=conv_o, beta=beta,
                                            lag_med=float(np.median(lags)))


CASE, SAMPLE = {}, []

if __name__ == '__main__':
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 141
    cases, log, states = S.record(seed)
    fel, pet, close = visible(cases, log, states)
    CASE.update({c['id']: c for c in fel})
    SAMPLE.extend(fel[::25])
    fel_ids = set(CASE)
    pet = [p for p in pet if p['case'] in fel_ids]
    adm = [p['decided'] for p in pet if p['revoked']]
    pers = sum(1 for a in adm if S.EXTRACT - 365 < a <= S.EXTRACT)
    t, sd = S.truth(seed, cases, log, states, reps=6)
    oc = one_clock(fel, pet, close)
    oct_ = one_clock(fel, pet, close, by_term=True)
    gc, parts, est = two_clock(fel, pet, close)
    print('seed %d truth %.0f | persistence %d (%.2fx) | one-clock %.0f (%.2fx) | one-clock by term %.0f (%.2fx) | two-clock %.0f (%.2fx)' % (
        seed, t, pers, pers / t, oc, oc / t, oct_, oct_ / t, gc, gc / t))
    print('  parts', {k: round(v, 1) for k, v in parts.items()}, {k: round(v, 3) for k, v in est.items()})
