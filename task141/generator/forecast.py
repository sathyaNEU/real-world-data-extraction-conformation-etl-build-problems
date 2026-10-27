"""The forecast routes on a record (built from the pack by golden.py, or straight from the world for tuning): the
golden two-clock construction and every rung of the ladder.

A record R carries the felony terms the Department's registers hold at the extract (each with its supervision begin
day, risk score, scheduled expiration as it now stands and closure), every change of a scheduled expiration the
court ordered (dated), and the Circuit Court's petitions on those terms (filing day, disposition day and whether the
term was revoked, blank while pending)."""
from __future__ import annotations

import numpy as np

import common as K

M = K.M


class Rec:
    pass


def record_from_world(W):
    """what the pack shows of the felony record at the extract, read straight off the world (tuning only)"""
    R = Rec()
    R.cases = []
    for c in W.cases:
        if c['lvl'] != 'F' or c['sup'] > K.EXTRACT:
            continue
        st = W.states[c['id']]
        if st['closed'] is not None and st['closed'][0] < K.RECORD_START:
            continue
        early_ext = sum(m[4] for m in st['mods'] if m[0] < K.RECORD_START and m[3] == 'EXTEND')
        R.cases.append(dict(id=c['id'], sup=c['sup'], score=c['score'], term=c['term'] + early_ext, klass=c['klass'],
                            max_m=c['max_m'], imposed_term=c['term'] + early_ext,
                            exts=sorted((m[0], m[4]) for m in st['mods'] if m[3] == 'EXTEND' and
                                        K.RECORD_START <= m[0] <= K.EXTRACT)))
    R.C = {c['id']: c for c in R.cases}
    R.pet, R.byc, R.close, R.scheds, R.sched_now = [], {}, {}, {}, {}
    for c in R.cases:
        w = W.C[c['id']]
        st = W.states[c['id']]
        for e in W.log[c['id']]:
            if e['file'] > K.EXTRACT or e['file'] < K.RECORD_START:
                continue
            dec = e['decided'] if e['decided'] <= K.EXTRACT else None
            p = dict(case=c['id'], file=e['file'], decided=dec, revoked=(bool(e.get('revoked')) if dec is not None else None))
            R.pet.append(p)
            R.byc.setdefault(c['id'], []).append(p)
        if st['closed'] is not None and st['closed'][0] <= K.EXTRACT:
            R.close[c['id']] = st['closed']
        mods = [m for m in st['mods'] if m[0] <= K.EXTRACT and m[3] not in ('EARLY TERMINATION', 'ACT')]
        early = [m for m in mods if m[0] < K.RECORD_START]
        late = [m for m in mods if m[0] >= K.RECORD_START]
        sch = [(-10 ** 6, early[-1][2] if early else w['orig'])] + [(m[0], m[2]) for m in late]
        R.scheds[c['id']] = sch
        R.sched_now[c['id']] = sch[-1][1]
    finish(R)
    return R


def finish(R):
    for v in R.byc.values():
        v.sort(key=lambda p: p['file'])
    R.active = [c for c in R.cases if c['id'] not in R.close]
    R.cache = {}


def sched_at(R, c, d):
    s = None
    for since, v in R.scheds[c['id']]:
        if since <= d:
            s = v
    return s


def end_of(R, c):
    return R.close[c['id']][0] if c['id'] in R.close else K.EXTRACT


def act_cap(c):
    return max(K.add_months(c['sup'], 24), K.TRANS)


def act_end(R, c):
    return min(R.sched_now[c['id']], act_cap(c))


# ---------------------------------------------------------------------------------------------------- landing
class Lags:
    def __init__(self, lags):
        self.L = np.sort(np.asarray(lags, dtype=float))
        self.n = len(self.L)

    def F(self, x):
        return np.searchsorted(self.L, x, side='right') / self.n

    def land(self, f, y0=K.Y0, y1=K.Y1, after=None):
        """P(a petition filed on day f, or days f, is disposed inside [y0, y1]); `after` conditions on its being
        undecided at the end of that day"""
        f = np.asarray(f, dtype=float)
        lo, hi = y0 - f - 1, y1 - f
        if after is None:
            return np.maximum(self.F(hi) - self.F(lo), 0.0)
        a = after - f
        tail = 1.0 - self.F(a)
        return np.where(tail > 0, np.maximum(self.F(hi) - self.F(np.maximum(lo, a)), 0.0) / np.maximum(tail, 1e-12), 0.0)


def decided_old(R, cut=400):
    return [p for p in R.pet if p['decided'] is not None and p['file'] < K.EXTRACT - cut]


def persistence(R):
    return sum(1 for p in R.pet if p['revoked'] and K.EXTRACT - 365 < p['decided'] <= K.EXTRACT)


def new_starts(R, months_back=12):
    rec = [c for c in R.cases if K.EXTRACT - M * months_back < c['sup'] <= K.EXTRACT]
    return len(rec) / float(months_back), rec


def score_beta(rows):
    """the log rate's slope on the risk screen across scores with enough exposure, weighted by exposure"""
    xs, ys, ws = [], [], []
    for s_ in np.unique(rows[:, 1]):
        k = rows[:, 1] == s_
        if rows[k, 3].sum() > 2000:
            xs.append(s_); ys.append(np.log(max(rows[k, 2].sum(), 1) / rows[k, 3].sum())); ws.append(rows[k, 3].sum())
    return float(np.polyfit(xs, ys, 1, w=np.sqrt(ws))[0])


# ---------------------------------------------------------------------------------------------------- one clock
def entry_month(c):
    """the first month on supervision the extracts see whole (delayed entry for terms begun before them)"""
    return max(0, int(np.ceil((K.RECORD_START - c['sup']) / M)))


def commitment_rows(R, by_term=False):
    """case-months on supervision by month since supervision began, from the extracts' first day, and the
    commitments dated in them"""
    adm = {p['case']: p['decided'] for p in R.pet if p['revoked']}
    at, ev, rows = {}, {}, []
    for c in R.cases:
        e = end_of(R, c)
        if e <= c['sup']:
            continue
        key = c['term'] if by_term else 0
        last = int((e - c['sup']) // M)
        m0 = entry_month(c)
        if m0 > last:
            continue
        for m in range(m0, last + 1):
            at[(key, m)] = at.get((key, m), 0) + 1
        hit = c['id'] in adm and adm[c['id']] <= K.EXTRACT
        if hit:
            m = int((adm[c['id']] - c['sup']) // M)
            ev[(key, m)] = ev.get((key, m), 0) + 1
        rows.append((0, c['score'], 1 if hit else 0, last + 1 - m0))
    return at, ev, np.array(rows, dtype=float)


def exit_hazard(R):
    at, ev = {}, {}
    for c in R.cases:
        e = end_of(R, c)
        if e <= c['sup']:
            continue
        last = int((e - c['sup']) // M)
        if entry_month(c) > last:
            continue
        for m in range(entry_month(c), last + 1):
            at[m] = at.get(m, 0) + 1
        if c['id'] in R.close and R.close[c['id']][1] == 'EARLY_TERM':
            ev[last] = ev.get(last, 0) + 1
    return {m: ev.get(m, 0) / at[m] for m in at if at[m] >= 30}


def one_clock(R, by_term=False, score_adjust=True):
    """the field's survival projection: the commitment hazard by month on supervision (score adjusted), carried over
    each open term's months to its end under the Act, new terms at the trailing year's rate, pending petitions at
    their conversion"""
    at, ev, rows = commitment_rows(R, by_term)
    beta = score_beta(rows) if score_adjust else 0.0
    h = {k: ev.get(k, 0) / v for k, v in at.items() if v >= 30}
    keys = {}
    for k in h:
        keys.setdefault(k[0], []).append(k[1])
    ex = exit_hazard(R)
    lags = Lags([p['decided'] - p['file'] for p in decided_old(R)])
    conv = float(np.mean([p['revoked'] for p in decided_old(R)]))
    mean_mult = float(np.mean([np.exp(beta * (c['score'] - 10)) for c in R.cases]))

    def hh(key, m):
        if (key, m) in h:
            return h[(key, m)]
        return h.get((key, max(keys.get(key, [0]))), 0.0)
    total = 0.0
    for c in R.active:
        key = c['term'] if by_term else 0
        mult = np.exp(beta * (c['score'] - 10)) / mean_mult
        end = act_end(R, c)
        alive = 1.0
        d = K.EXTRACT + 1
        pend = [p for p in R.byc.get(c['id'], []) if p['decided'] is None]
        if pend:
            p = pend[-1]
            total += conv * float(lags.land(p['file'], after=K.EXTRACT))
            alive = 1 - conv
            L = lags.L[lags.L > K.EXTRACT - p['file']]
            d = int(p['file'] + np.median(L)) if len(L) else d
        while d <= K.Y1 and d < end:
            m = int((d - c['sup']) // M)
            x = hh(key, m) * mult
            if d >= K.Y0:
                total += alive * x
            alive *= (1 - x) * (1 - ex.get(m, 0.0))
            d += int(M)
    rate, rec = new_starts(R)
    k = 0
    while True:
        s0 = K.EXTRACT + 1 + int(round((k + 0.5) * M))
        if s0 > K.Y1:
            break
        alive = rate
        d = s0
        while d <= K.Y1:
            m = int((d - s0) // M)
            x = hh(24 if by_term else 0, m)
            if d >= K.Y0:
                total += alive * x
            alive *= (1 - x) * (1 - ex.get(m, 0.0))
            d += int(M)
        k += 1
    return total


def rate_on_exposure(R):
    """the trailing year's commitments per case-month on supervision, times the case-months the Act leaves in 2027"""
    num = persistence(R)
    den = 0.0
    for c in R.cases:
        a, b = max(c['sup'], K.EXTRACT - 365), min(end_of(R, c), K.EXTRACT)
        if b > a:
            den += (b - a) / M
    exp27 = 0.0
    for c in R.active:
        a, b = max(c['sup'], K.Y0), min(act_end(R, c), K.Y1 + 1)
        if b > a:
            exp27 += (b - a) / M
    r, _ = new_starts(R)
    k = 0
    while True:
        s0 = K.EXTRACT + 1 + int(round((k + 0.5) * M))
        if s0 > K.Y1:
            break
        a = max(s0, K.Y0)
        exp27 += r * (K.Y1 + 1 - a) / M
        k += 1
    return num / den * exp27


# ---------------------------------------------------------------------------------------------------- two clocks
def estimates(R, window=120, score_adjust=True, pwin_free=False):
    key = ('est', window, score_adjust, pwin_free)
    if key in R.cache:
        return R.cache[key]

    def in_window(c, f):
        s = sched_at(R, c, f)
        return s - window <= f < s
    ms_all, sc_all, hit_all = [], [], []
    for c in R.cases:
        e = min(end_of(R, c), K.EXTRACT)
        if e <= c['sup']:
            continue
        n = int((e - c['sup']) // M) + 1
        mm = np.arange(n)
        a0 = c['sup'] + np.round(mm * M).astype(int)
        keep = (a0 < e) & (a0 >= K.RECORD_START)
        sch = R.scheds[c['id']]
        chg = np.array([s for s, _ in sch])
        vals = np.array([v for _, v in sch])
        idx = np.searchsorted(chg, a0, side='right') - 1
        s = vals[np.maximum(idx, 0)]
        keep &= a0 < s - window
        hit = np.zeros(n, dtype=int)
        for p in R.byc.get(c['id'], []):
            b = p['decided'] if p['decided'] is not None else K.EXTRACT + 1
            keep &= ~((a0 >= p['file']) & (a0 < b))
            if not in_window(c, p['file']):
                k = int((p['file'] - c['sup']) // M)
                if 0 <= k < n:
                    hit[k] = 1
        ms_all.append(mm[keep]); sc_all.append(np.full(int(keep.sum()), c['score'])); hit_all.append(hit[keep])
    A = np.column_stack([np.concatenate(ms_all), np.concatenate(sc_all), np.concatenate(hit_all)]).astype(float)
    A4 = np.column_stack([A, np.ones(len(A))])
    beta = score_beta(A4) if score_adjust else 0.0
    mult_r = np.exp(beta * (A[:, 1] - 10))
    g0 = {}
    for m in np.unique(A[:, 0]):
        k = A[:, 0] == m
        if k.sum() > 30:
            g0[int(m)] = A[k, 2].sum() / mult_r[k].sum()
    reach = wpet = 0
    offs = []
    for c in R.cases:
        ps = R.byc.get(c['id'], [])
        e = end_of(R, c) if c['id'] in R.close else K.EXTRACT + 1
        sch = R.scheds[c['id']]
        for i, (since, s) in enumerate(sch):
            until = sch[i + 1][0] if i + 1 < len(sch) else 10 ** 9
            wo = s - window
            if s > K.EXTRACT - 30 or not (since <= wo < until) or wo < K.RECORD_START:
                continue
            if e <= wo or c['sup'] > wo:
                continue
            if pwin_free and any(p['file'] < wo and (p['decided'] is None or p['decided'] >= wo) for p in ps):
                continue
            reach += 1
            hit = [p for p in ps if wo <= p['file'] < s]
            if hit:
                wpet += 1
                offs.append(s - hit[0]['file'])
    old = decided_old(R)
    cw = [p['revoked'] for p in old if in_window(R.C[p['case']], p['file'])]
    co = [p['revoked'] for p in old if not in_window(R.C[p['case']], p['file'])]
    lags = Lags([p['decided'] - p['file'] for p in old])
    out = dict(g0=g0, gmax=max(g0), beta=beta, p_win=wpet / reach, offs=np.array(offs, dtype=float),
               conv_w=float(np.mean(cw)), conv_o=float(np.mean(co)), lags=lags, lag_m=float(lags.L.mean() / M),
               ex=exit_hazard(R), reach=reach, wpet=wpet, window=window, n_w=len(cw), n_o=len(co))
    R.cache[key] = out
    return out


def two_clock(R, window=120, score_adjust=True, skip_transition=False, clip_act=True, pwin_free=False, thin=True,
              mean_lag=False, conv_pooled=False, y0=K.Y0, y1=K.Y1, ns_months=12):
    E = estimates(R, window, score_adjust, pwin_free)
    g0, gmax, beta, p_win, offs = E['g0'], E['gmax'], E['beta'], E['p_win'], E['offs']
    conv_w, conv_o, lag_m, ex = E['conv_w'], E['conv_o'], E['lag_m'], E['ex']
    if conv_pooled:
        old = decided_old(R)
        conv_w = conv_o = float(np.mean([p['revoked'] for p in old]))
    lags = Lags([int(round(E['lags'].L.mean()))]) if mean_lag else E['lags']

    def gg_at(m, mult):
        g = g0.get(m, g0[gmax]) * mult
        return g / (1 + g * (1 - conv_o) * lag_m) if thin else g

    def ordinary(sup, mult, d, stop, alive):
        out = 0.0
        while d < stop and d <= y1:
            m = int((d - sup) // M)
            m_end = sup + int(round((m + 1) * M))
            if m_end <= d:                       # a day on a rounded month boundary belongs to the next month
                m += 1
                m_end = sup + int(round((m + 1) * M))
            nxt = min(m_end, stop)
            frac = (nxt - d) / M
            g = gg_at(m, mult) * frac
            out += alive * g * conv_o * float(lags.land((d + nxt) / 2.0, y0, y1))
            alive *= (1 - g * conv_o) * (1 - ex.get(m, 0.0) * frac)
            d = nxt
        return out, alive
    parts = dict(pending=0.0, ordinary=0.0, window=0.0, new=0.0)
    trans = dict(window=0.0, n=0)
    for c in R.active:
        end = act_end(R, c)
        moved = end < R.sched_now[c['id']]
        mult = np.exp(beta * (c['score'] - 10))
        ps = R.byc.get(c['id'], [])
        pend = [p for p in ps if p['decided'] is None]
        alive = 1.0
        d = max(K.EXTRACT + 1, c['sup'])
        if pend:
            p = pend[-1]
            s_then = sched_at(R, c, p['file'])
            cv = conv_w if s_then - window <= p['file'] < s_then else conv_o
            parts['pending'] += cv * float(lags.land(p['file'], y0, y1, after=K.EXTRACT))
            alive = 1 - cv
            Lc = lags.L[lags.L > K.EXTRACT - p['file']]
            if len(Lc):
                d = max(d, int(p['file'] + np.median(Lc)))
        wo = end - window
        if moved and clip_act:
            wo = max(wo, K.ACT)
        o, alive = ordinary(c['sup'], mult, d, min(wo, end), alive)
        parts['ordinary'] += o
        if skip_transition and moved and end == K.TRANS:
            continue
        if end <= K.EXTRACT or wo > y1:
            continue
        if wo <= K.EXTRACT and any(wo <= q['file'] <= K.EXTRACT for q in ps):
            continue
        fil = end - offs
        if wo <= K.EXTRACT:
            fil = fil[fil > K.EXTRACT]
            share = len(fil) / len(offs)
        else:
            share = 1.0
        if moved and clip_act:
            fil = np.maximum(fil, K.ACT)
        if len(fil):
            v = alive * p_win * share * conv_w * float(lags.land(fil, y0, y1).mean())
            parts['window'] += v
            if moved and end == K.TRANS:
                trans['window'] += v
                trans['n'] += 1
    rate, rec = new_starts(R, ns_months)
    mbar = float(np.mean([np.exp(beta * (c['score'] - 10)) for c in rec]))
    k = 0
    while True:
        s0 = K.EXTRACT + 1 + int(round((k + 0.5) * M))
        if s0 > y1:
            break
        o, _ = ordinary(s0, mbar, s0, y1 + 1, rate)
        parts['new'] += o
        k += 1
    return sum(parts.values()), parts, dict(E, trans=trans)


# ---------------------------------------------------------------------------------------------------- the other clock alone
def to_expiry(R, score_adjust=True):
    """every petition read on one clock, months to the scheduled expiration in force (score adjusted), carried over
    each open term's months to its end under the Act; new terms on the same clock to their 24-month end"""
    rows, ev, ex = [], {}, {}
    for c in R.cases:
        e = min(end_of(R, c), K.EXTRACT)
        if e <= c['sup']:
            continue
        n = int((e - c['sup']) // M) + 1
        a0 = c['sup'] + np.round(np.arange(n) * M).astype(int)
        keep = (a0 < e) & (a0 >= K.RECORD_START)
        sch = R.scheds[c['id']]
        chg = np.array([s for s, _ in sch])
        vals = np.array([v for _, v in sch])
        s = vals[np.maximum(np.searchsorted(chg, a0, side='right') - 1, 0)]
        k = np.floor((s - a0) / M).astype(int)
        hit = np.zeros(n, dtype=int)
        for p in R.byc.get(c['id'], []):
            j = int((p['file'] - c['sup']) // M)
            if 0 <= j < n:
                hit[j] = 1
        for kk, hh, ok in zip(k, hit, keep):
            if ok and kk >= 0:
                rows.append((kk, c['score'], hh))
    A = np.array(rows, dtype=float)
    beta = score_beta(np.column_stack([A, np.ones(len(A))])) if score_adjust else 0.0
    mult = np.exp(beta * (A[:, 1] - 10))
    h = {}
    for kk in np.unique(A[:, 0]):
        sel = A[:, 0] == kk
        if sel.sum() > 30:
            h[int(kk)] = A[sel, 2].sum() / mult[sel].sum()
    kmax = max(h)
    old = decided_old(R)
    conv = float(np.mean([p['revoked'] for p in old]))
    lags = Lags([p['decided'] - p['file'] for p in old])
    total = 0.0

    def run(sup, end, mult_, d, alive):
        out = 0.0
        while d < end and d <= K.Y1:
            kk = int((end - d) // M)
            g = h.get(kk, h[kmax]) * mult_
            nxt = min(d + int(M), end)
            frac = (nxt - d) / M
            out += alive * g * frac * conv * float(lags.land((d + nxt) / 2.0))
            alive *= 1 - g * frac * conv
            d = nxt
        return out
    for c in R.active:
        mult_ = np.exp(beta * (c['score'] - 10))
        pend = [p for p in R.byc.get(c['id'], []) if p['decided'] is None]
        alive, d = 1.0, K.EXTRACT + 1
        if pend:
            total += conv * float(lags.land(pend[-1]['file'], after=K.EXTRACT))
            alive = 1 - conv
        total += run(c['sup'], act_end(R, c), mult_, d, alive)
    rate, rec = new_starts(R)
    mbar = float(np.mean([np.exp(beta * (c['score'] - 10)) for c in rec]))
    k = 0
    while True:
        s0 = K.EXTRACT + 1 + int(round((k + 0.5) * M))
        if s0 > K.Y1:
            break
        total += run(s0, K.add_months(s0, 24), mbar, s0, rate)
        k += 1
    return total


# ---------------------------------------------------------------------------------------------------- the room to extend
def term_m_at(c, d):
    """the term in force on day d, in months: the term imposed and every extension ordered before d"""
    return c['imposed_term'] + sum(e for dd, e in c['exts'] if dd < d)


def window_rates(R, window=120, pending_free=False):
    """every end-of-term window the record saw open (the last `window` days before a scheduled expiration in force,
    the term alive and on supervision), split by whether the term then had room under its class maximum: the share
    with a petition filed in the window and the share extended in it"""
    key = ('rates', window, pending_free)
    if key in R.cache:
        return R.cache[key]
    rows = []
    for c in R.cases:
        ps = R.byc.get(c['id'], [])
        e = end_of(R, c) if c['id'] in R.close else K.EXTRACT + 1
        sch = R.scheds[c['id']]
        for i, (since, s_) in enumerate(sch):
            until = sch[i + 1][0] if i + 1 < len(sch) else 10 ** 9
            wo = s_ - window
            if s_ > K.EXTRACT - 30 or not (since <= wo < until) or wo < K.RECORD_START:
                continue
            if e <= wo or c['sup'] > wo:
                continue
            if pending_free and any(p['file'] < wo and (p['decided'] is None or p['decided'] >= wo) for p in ps):
                continue
            hit = any(wo <= p['file'] < s_ for p in ps)
            ext = any(wo <= dd < s_ for dd, _ in c['exts'])
            rows.append((term_m_at(c, wo) >= c['max_m'], hit, ext))
    A = np.array(rows, dtype=float)
    n = A[:, 0] == 1
    out = dict(pool=A[:, 1].mean(), e=A[~n, 1].mean(), n=A[n, 1].mean(), x_pool=A[:, 2].mean(), x_e=A[~n, 2].mean(),
               x_n=A[n, 2].mean(), n_windows=len(A), n_nonext=int(n.sum()), hits_n=int(A[n, 1].sum()),
               hits_e=int(A[~n, 1].sum()), hits=int(A[:, 1].sum()))
    R.cache[key] = out
    return out


MODES = ('pooled', 'golden', 'full', 'iia')


def projection(R, mode='golden', window=120, score_adjust=False, clip_act=True, y0=K.Y0, y1=K.Y1, conv_pooled=False,
               mean_lag=False, pending_free=False, ns_months=12, skip_transition=False, ext_m=K.EXT_MONTHS,
               act_room=True, second=True):
    """the 2027 projection on the two clocks with each term's room to extend. A term ending under the Act with no room
    (under its class maximum, or under the Act's cap) files at the end-of-term rate of `p_non`; one with room at
    `p_ext_end`, and is extended at `x_end` by `ext_m` months (or to the cap if sooner) to a second end with no room.
    mode: golden (no room at the rate of the terms the record saw at their class maximum, room at the rate of the terms
    with room), pooled (every end at the record's pooled rate), full (every would-be extension a petition), iia (the
    extension share reallocated to petition and lapse in proportion)"""
    E = estimates(R, window, score_adjust)
    g0, gmax, beta, offs = E['g0'], E['gmax'], E['beta'], E['offs']
    conv_w, conv_o, lag_m, ex = E['conv_w'], E['conv_o'], E['lag_m'], E['ex']
    if conv_pooled:
        old = decided_old(R)
        conv_w = conv_o = float(np.mean([p['revoked'] for p in old]))
    lags = Lags([int(round(E['lags'].L.mean()))]) if mean_lag else E['lags']
    W_ = window_rates(R, window, pending_free)
    pe, pn, pp, xe, xp = W_['e'], W_['n'], W_['pool'], W_['x_e'], W_['x_pool']
    if mode == 'pooled':
        p_non, p_ext_end, x_end = pp, pp, xp
    elif mode == 'golden':
        p_non, p_ext_end, x_end = pn, pe, xe
    elif mode == 'full':
        p_non, p_ext_end, x_end = pp + xp, pp, xp
    elif mode == 'iia':
        lapse = 1 - pp - xp
        p_non, p_ext_end, x_end = pp + xp * pp / (pp + lapse), pp, xp
    else:
        raise ValueError(mode)

    def gg_at(m, mult):
        g = g0.get(m, g0[gmax]) * mult
        return g / (1 + g * (1 - conv_o) * lag_m)

    def ordinary(sup, mult, d, stop, alive):
        out = 0.0
        while d < stop and d <= y1:
            m = int((d - sup) // M)
            m_end = sup + int(round((m + 1) * M))
            if m_end <= d:                       # a day on a rounded month boundary belongs to the next month
                m += 1
                m_end = sup + int(round((m + 1) * M))
            nxt = min(m_end, stop)
            frac = (nxt - d) / M
            g = gg_at(m, mult) * frac
            out += alive * g * conv_o * float(lags.land((d + nxt) / 2.0, y0, y1))
            alive *= (1 - g * conv_o) * (1 - ex.get(m, 0.0) * frac)
            d = nxt
        return out, alive

    def window_part(end, alive, rate, moved):
        wo = end - window
        if moved and clip_act:
            wo = max(wo, K.ACT)
        fil = end - offs
        share = 1.0
        if wo <= K.EXTRACT:
            fil = fil[fil > K.EXTRACT]
            share = len(fil) / len(offs)
        if moved and clip_act:
            fil = np.maximum(fil, K.ACT)
        if not len(fil):
            return 0.0
        return alive * rate * share * conv_w * float(lags.land(fil, y0, y1).mean())

    parts = dict(pending=0.0, ordinary=0.0, window=0.0, new=0.0)
    info = dict(n_room=0, n_none=0, transition=0.0, n_transition=0, room=0.0, none=0.0)
    for c in R.active:
        cap = act_cap(c)
        end = act_end(R, c)
        moved = end < R.sched_now[c['id']]
        mult = np.exp(beta * (c['score'] - 10))
        ps = R.byc.get(c['id'], [])
        pend = [p for p in ps if p['decided'] is None]
        alive = 1.0
        d = max(K.EXTRACT + 1, c['sup'])
        if pend:
            p = pend[-1]
            s_then = sched_at(R, c, p['file'])
            cv = conv_w if s_then - window <= p['file'] < s_then else conv_o
            parts['pending'] += cv * float(lags.land(p['file'], y0, y1, after=K.EXTRACT))
            alive = 1 - cv
            Lc = lags.L[lags.L > K.EXTRACT - p['file']]
            if len(Lc):
                d = max(d, int(p['file'] + np.median(Lc)))
        rm = c['max_m'] - term_m_at(c, K.EXTRACT + 1)
        if act_room:
            rm = min(rm, (cap - end) / M)
        wo = end - window
        if moved and clip_act:
            wo = max(wo, K.ACT)
        o, alive = ordinary(c['sup'], mult, d, min(wo, end), alive)
        parts['ordinary'] += o
        if skip_transition and moved and end == K.TRANS:
            continue
        if end <= K.EXTRACT or wo > y1:
            continue
        if wo <= K.EXTRACT and any(wo <= q['file'] <= K.EXTRACT for q in ps):
            continue
        if rm >= 1:
            info['n_room'] += 1
            v = window_part(end, alive, p_ext_end, moved)
            new_end = cap if ext_m == 'cap' else min(end + K.months(ext_m), cap)
            if second and new_end > end and new_end - window <= y1:
                a2 = alive * x_end
                o2, a2 = ordinary(c['sup'], mult, end, new_end - window, a2)
                parts['ordinary'] += o2
                v += window_part(new_end, a2, p_non, False)
            parts['window'] += v
            info['room'] += v
        else:
            info['n_none'] += 1
            v = window_part(end, alive, p_non, moved)
            parts['window'] += v
            info['none'] += v
            if moved and end == K.TRANS:
                info['transition'] += v
                info['n_transition'] += 1
    rate, rec = new_starts(R, ns_months)
    mbar = float(np.mean([np.exp(beta * (c['score'] - 10)) for c in rec]))
    k = 0
    while True:
        s0 = K.EXTRACT + 1 + int(round((k + 0.5) * M))
        if s0 > y1:
            break
        o, _ = ordinary(s0, mbar, s0, y1 + 1, rate)
        parts['new'] += o
        k += 1
    return sum(parts.values()), parts, dict(W_, **info, est=E)
