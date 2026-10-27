"""task141 world: Okelan County's felony and misdemeanor probation terms from July 2016, the Circuit Court's violation
petitions on them and the Detention Center's probation bookings, to the extract of 30 September 2026; and the truth,
the same process run forward under SB 26-118.

Ordinary petitions arrive on the time-on-supervision clock, front-loaded and scaled by the risk screen. In the last
120 days before a term's scheduled expiration in force, the officer reviews the case and files on a share of the
terms that reach that point with nothing pending, on whatever is still unresolved (the second clock). A continued
petition may extend the term, a warrant tolls it, a compliant case may be terminated early. SB 26-118 caps felony
supervision at 24 months from the day it began; a felony term in effect on 1 January 2027 ends on the earlier of its
scheduled expiration and that day, but not before 31 March 2027, and no extension passes the cap."""
from __future__ import annotations

import numpy as np

import common as K

P = K.P
M = K.M


class World:
    pass


def act_cap(c):
    """the latest day SB 26-118 lets a felony term run to"""
    if c['imposed'] >= K.ACT:
        return c['sup'] + K.months(24)
    return max(c['sup'] + K.months(24), K.TRANS)


def hazard(c, m):
    if c['lvl'] == 'F':
        h = P['h_inf'] + (P['h0'] - P['h_inf']) * np.exp(-m / P['h_tau'])
    else:
        h = P['m_h_inf'] + (P['m_h0'] - P['m_h_inf']) * np.exp(-m / P['m_h_tau'])
    return h * np.exp(P['score_beta'] * (c['score'] - 10))


def lvl_par(c):
    if c['lvl'] == 'F':
        return dict(abs=P['abs_hazard'], conv_o=P['conv_ord'], conv_r=P['conv_rev'], conv_a=P['conv_abs'],
                    p_rev=P['p_rev'], p_ext=P['p_ext'], ext=P['ext_months'], p_ext_rev=P['p_ext_rev'],
                    et=P['et_hazard'], et_after=P['et_after'])
    return dict(abs=P['m_abs'], conv_o=P['m_conv'], conv_r=P['m_conv'], conv_a=min(0.9, P['m_conv'] + 0.25),
                p_rev=P['m_p_rev'], p_ext=P['m_p_ext'], ext=P['m_ext_months'], p_ext_rev=P['m_p_ext'] * 0.8,
                et=P['m_et_hazard'], et_after=P['m_et_after'])


def fresh(c):
    return dict(t=c['imposed'], sched=c['orig'], pending=None, pkind=None, pfile=None, reviewed=None, closed=None,
                had_pet=False, review_at=None, mods=[], act_applied=False)


def run(rng, c, st, t_to, lg, act=False):
    """advance case c from its state st to day t_to (exclusive); lg is the case's own petition list, the pending
    petition last. Monthly steps on the supervision clock, events dated to the day."""
    q = lvl_par(c)
    sup = c['sup']
    W = P['rev_window']
    while st['closed'] is None and st['t'] < t_to:
        t = st['t']
        if act and c['lvl'] == 'F' and t >= K.ACT and not st['act_applied']:
            st['act_applied'] = True
            cap = act_cap(c)
            if st['sched'] > cap:
                st['mods'].append((K.ACT, st['sched'], cap, 'ACT', 0))
                st['sched'] = cap
                st['review_at'] = None
                st['reviewed'] = None
        if st['pending'] is not None:
            dec = st['pending']
            if dec >= t_to:
                st['t'] = t_to
                return
            kind = st['pkind']
            conv = q['conv_r'] if kind == 'REVIEW' else (q['conv_a'] if kind == 'ABSCOND' else q['conv_o'])
            rev = bool(rng.random() < conv)
            lg[-1]['revoked'] = rev
            st['pending'] = None
            st['t'] = dec
            if rev:
                st['closed'] = (dec, 'REVOKED')
                return
            new = st['sched']
            toll = dec - st['pfile'] if kind == 'ABSCOND' else 0
            new += toll
            ext = 0
            if rng.random() < (q['p_ext_rev'] if kind == 'REVIEW' else q['p_ext']):
                ext = int(rng.choice(q['ext']))
                new += K.months(ext)
            if act and c['lvl'] == 'F' and dec >= K.ACT:
                new = min(new, act_cap(c))
            if new > st['sched']:
                st['mods'].append((dec, st['sched'], new, 'TOLL' if toll and not ext else ('EXTEND' if ext else 'TOLL'), ext))
                st['sched'] = new
                st['reviewed'] = None
                st['review_at'] = None
            lg[-1]['ext'] = ext
            if dec >= st['sched']:
                st['closed'] = (dec, 'EXPIRED')
                return
            continue
        if t < sup:
            st['t'] = min(sup, t_to)
            continue
        if t >= st['sched']:
            st['closed'] = (st['sched'], 'EXPIRED')
            return
        wo = st['sched'] - W
        if st['reviewed'] != st['sched'] and t >= wo:
            st['reviewed'] = st['sched']
            st['review_at'] = None
            if rng.random() < q['p_rev']:
                off = int(rng.triangular(P['rev_lo'], P['rev_mode'], W))
                st['review_at'] = max(st['sched'] - off, t)
        m = int((t - sup) // M)
        m_end = sup + int(round((m + 1) * M))
        stop = min(max(m_end, t + 1), t_to, st['sched'])
        if st['reviewed'] != st['sched'] and wo > t:
            stop = min(stop, wo)
        frac = (stop - t) / M
        hz = hazard(c, m) * frac
        ha = q['abs'] * frac
        he = q['et'] * frac if (m >= q['et_after'] and not st['had_pet']) else 0.0
        u = rng.random()
        ev = 'ORDINARY' if u < hz else ('ABSCOND' if u < hz + ha else ('EARLY_TERM' if u < hz + ha + he else None))
        f = t + int(rng.integers(0, max(1, stop - t))) if ev else None
        ra = st['review_at']
        if ra is not None and ra < stop and (f is None or ra <= f):
            dec = ra + 1 + int(rng.gamma(P['lag_shape'], P['lag_mean'] / P['lag_shape']))
            lg.append(dict(case=c['id'], file=ra, kind='REVIEW', decided=dec))
            st.update(pending=dec, pkind='REVIEW', pfile=ra, had_pet=True, t=ra, review_at=None)
            continue
        if ev == 'EARLY_TERM':
            st['closed'] = (f, 'EARLY_TERM')
            st['mods'].append((f, st['sched'], f, 'EARLY TERMINATION', 0))
            return
        if ev is not None:
            lagm, lags = (P['abs_lag_mean'], P['abs_lag_shape']) if ev == 'ABSCOND' else (P['lag_mean'], P['lag_shape'])
            dec = f + 1 + int(rng.gamma(lags, lagm / lags))
            lg.append(dict(case=c['id'], file=f, kind=ev, decided=dec))
            st.update(pending=dec, pkind=ev, pfile=f, had_pet=True, t=f, review_at=None)
            continue
        st['t'] = stop


# ---------------------------------------------------------------------------------------------------- cases
def _term_jail(r, lvl):
    if lvl == 'F':
        term = int(r.choice(P['terms'], p=P['term_w']))
        if r.random() < P['jail_share']:
            med = P['jail_med'] * (term / 36.0) ** P['jail_term_elast']
            jail = int(np.clip(np.exp(r.normal(np.log(med), P['jail_sig'])), P['jail_lo'], P['jail_hi']))
        else:
            jail = 0
    else:
        term = P['m_term']
        if r.random() < P['m_jail_share']:
            jail = int(np.clip(np.exp(r.normal(np.log(P['m_jail_med']), P['m_jail_sig'])), P['m_jail_lo'], P['m_jail_hi']))
        else:
            jail = 0
    return term, jail


def make_cases(lvl, d_from, d_to, id0, stream):
    """impositions from d_from to d_to (exclusive), each with its own random stream for its attributes"""
    out = []
    rate = P['fel_rate'] if lvl == 'F' else P['mis_rate']
    rc = K.rng(stream, lvl, 'counts')
    k = id0
    nm = int((d_to - d_from) / M) + 1
    for mi in range(nm):
        base = d_from + int(mi * M)
        n = rc.poisson(rate)
        days = np.sort(rc.integers(0, int(M), n))
        for dd in days:
            s = base + int(dd)
            if s >= d_to:
                continue
            r = K.rng(stream, 'case', k)
            term, jail = _term_jail(r, lvl)
            gap = jail + int(r.integers(0, 4)) if jail else int(r.integers(P['intake_lo'], P['intake_hi']))
            sc = int(np.clip(round(r.normal(10.5 if lvl == 'F' else 8.5, 3.6)), 0, 20))
            office = K.OFFICES[int(r.choice(4, p=K.OFFICE_W))][0]
            out.append(dict(id=k, lvl=lvl, imposed=s, term=term, jail=jail, sup=s + gap, score=sc,
                            orig=s + K.months(term), office=office))
            k += 1
    return out


def record_cases(cases, stream):
    log, states = {}, {}
    for c in cases:
        r = K.rng(stream, 'run', c['id'])
        st = fresh(c)
        lg = []
        run(r, c, st, K.EXTRACT + 1, lg)
        log[c['id']] = lg
        states[c['id']] = st
    return log, states


def simulate():
    W = World()
    fel = make_cases('F', K.BURN, K.EXTRACT + 1, 0, 'record')
    mis = make_cases('M', K.BURN, K.EXTRACT + 1, 500000, 'record')
    W.cases = fel + mis
    W.C = {c['id']: c for c in W.cases}
    W.log, W.states = record_cases(W.cases, 'record')
    persons(W)
    joint_hearings(W)
    petition_details(W)
    return W


# ---------------------------------------------------------------------------------------------------- people
def _open_until(W, c):
    st = W.states[c['id']]
    return st['closed'][0] if st['closed'] is not None else 10 ** 7


def persons(W):
    """felony terms each have their own person, bar repeat probationers whose earlier term had closed; a tenth of
    misdemeanor terms go to people then on felony probation, some to people with an earlier closed term"""
    r = K.rng('persons')
    fel = sorted((c for c in W.cases if c['lvl'] == 'F'), key=lambda c: (c['imposed'], c['id']))
    mis = sorted((c for c in W.cases if c['lvl'] == 'M'), key=lambda c: (c['imposed'], c['id']))
    nxt = 0
    closed_pool = []          # (closed day, person)
    for c in fel:
        reuse = None
        if r.random() < 0.08:
            cands = [i for i, (d, pid) in enumerate(closed_pool) if d + 330 <= c['imposed']]
            if cands:
                reuse = cands[int(r.integers(0, len(cands)))]
        if reuse is not None:
            c['person'] = closed_pool.pop(reuse)[1]
        else:
            c['person'] = nxt
            nxt += 1
        closed_pool.append((_open_until(W, c), c['person']))
        if len(closed_pool) > 4000:
            closed_pool = closed_pool[-4000:]
    # felony open intervals by imposition, for the misdemeanor draw
    fel_by_start = sorted(fel, key=lambda c: c['sup'])
    starts = np.array([c['sup'] for c in fel_by_start])
    ends = np.array([_open_until(W, c) for c in fel_by_start])
    mis_closed = []
    for c in mis:
        u = r.random()
        pid = None
        if u < P['m_on_felony']:
            j = np.searchsorted(starts, c['imposed'], side='right')
            lo = max(0, j - 3000)
            idx = np.nonzero((starts[lo:j] <= c['imposed']) & (ends[lo:j] > c['imposed'] + 30))[0]
            if len(idx):
                pid = fel_by_start[lo + int(idx[int(r.integers(0, len(idx)))])]['person']
        elif u < P['m_on_felony'] + 0.12:
            cands = [i for i, (d, p_) in enumerate(mis_closed) if d + 200 <= c['imposed']]
            if cands:
                pid = mis_closed.pop(cands[int(r.integers(0, len(cands)))])[1]
        if pid is None:
            pid = nxt
            nxt += 1
        c['person'] = pid
        mis_closed.append((_open_until(W, c), pid))
        if len(mis_closed) > 3000:
            mis_closed = mis_closed[-3000:]
    W.n_persons = nxt
    W.fel_spans = {}
    for c in fel:
        W.fel_spans.setdefault(c['person'], []).append((c['imposed'], _open_until(W, c)))


def joint_hearings(W):
    """a misdemeanor petition the court would revoke within three weeks before it revokes the same person's felony
    term is heard with the felony petition, so the person is committed once on both"""
    fel_rev = {}
    for cid, lg in W.log.items():
        c = W.C[cid]
        if c['lvl'] == 'F':
            for e in lg:
                if e.get('revoked'):
                    fel_rev.setdefault(c['person'], []).append(e['decided'])
    W.joint = 0
    for cid, lg in W.log.items():
        c = W.C[cid]
        if c['lvl'] != 'M' or c['person'] not in fel_rev:
            continue
        for e in lg:
            if not e.get('revoked'):
                continue
            later = [d for d in fel_rev[c['person']] if e['decided'] < d <= e['decided'] + 21]
            if later:
                e['decided'] = min(later)
                st = W.states[cid]
                if st['closed'] is not None and st['closed'][1] == 'REVOKED':
                    st['closed'] = (e['decided'], 'REVOKED')
                W.joint += 1


def on_felony(W, person, d):
    return any(a <= d < b for a, b in W.fel_spans.get(person, ()))


ALLEG = (('LAW', 0.34), ('RPT', 0.20), ('DRG', 0.18), ('TRT', 0.12), ('PAY', 0.08), ('CUR', 0.05), ('CNT', 0.03))


def petition_details(W):
    """allegations, warrant or summons, the arrest on a warrant, the jail ordered on revocation and how it is served;
    drawn from each petition's own stream so the process above is untouched"""
    codes = [a for a, _ in ALLEG]
    wts = np.array([w for _, w in ALLEG]); wts = wts / wts.sum()
    for cid, lg in W.log.items():
        c = W.C[cid]
        for i, e in enumerate(lg):
            r = K.rng('petition', cid, i)
            if e['kind'] == 'ABSCOND':
                al = ['ABS'] + ([codes[int(r.choice(len(codes), p=wts))]] if r.random() < 0.4 else [])
                e['warrant'] = True
                e['arrest'] = max(e['file'] + 1, e['decided'] - int(r.integers(3, 21)))
            else:
                k = 1 + int(r.random() < 0.45) + int(r.random() < 0.15)
                al = list(dict.fromkeys(codes[int(j)] for j in r.choice(len(codes), size=k, p=wts)))
                e['warrant'] = bool(r.random() < (0.62 if c['lvl'] == 'F' else 0.45))
                e['arrest'] = (e['file'] + int(r.integers(0, max(1, min(21, e['decided'] - e['file'] - 2))))) if e['warrant'] else None
            e['alleg'] = al
            if c['lvl'] == 'F':
                e['jail_days'] = int(np.clip(np.exp(r.normal(np.log(150), 0.55)), 30, 365))
                e['intermittent'] = False
            else:
                e['jail_days'] = int(np.clip(np.exp(r.normal(np.log(40), 0.6)), 6, 180))
                e['intermittent'] = bool(r.random() < P['m_intermittent'])
                if e['intermittent']:
                    e['jail_days'] = int(2 * int(r.integers(4, 13)))     # two days a weekend, four to twelve weekends
            e['hearing_min'] = int(r.integers(9 * 60, 16 * 60 + 30))
            e['served_share'] = float(r.uniform(0.62, 0.78))
            e['annex'] = bool(r.random() < 0.16)
            e['annex_at'] = float(r.uniform(0.15, 0.7))
            e['seq'] = i


# ---------------------------------------------------------------------------------------------------- the truth
def truth(W, reps=8, by_month=False):
    """expected felony revocation commitments dated in 2027 under the Act, given the record: every felony term open at
    the extract (those still in their jail condition included) re-run forward, and new felony terms imposed from the
    extract"""
    res = []
    monthly = np.zeros(12)
    for rr in range(reps):
        rng = K.rng('truth', rr)
        n = 0
        for c in W.cases:
            if c['lvl'] != 'F':
                continue
            st0 = W.states[c['id']]
            if st0['closed'] is not None:
                continue
            st = dict(st0)
            st['mods'] = list(st0['mods'])
            lg = []
            if st['pending'] is not None:
                kind = st['pkind']
                lagm, lags = (P['abs_lag_mean'], P['abs_lag_shape']) if kind == 'ABSCOND' else (P['lag_mean'], P['lag_shape'])
                for _ in range(60):
                    dec = st['pfile'] + 1 + int(rng.gamma(lags, lagm / lags))
                    if dec > K.EXTRACT:
                        break
                else:
                    dec = K.EXTRACT + 1 + int(rng.integers(0, 30))
                st['pending'] = dec
                lg = [dict(case=c['id'], file=st['pfile'], kind=kind, decided=dec)]
            run(rng, c, st, K.Y1 + 400, lg, act=True)
            for e in lg:
                if e.get('revoked') and K.Y0 <= e['decided'] <= K.Y1:
                    n += 1
                    monthly[min(11, int((e['decided'] - K.Y0) // M))] += 1
        new = make_cases('F', K.EXTRACT + 1, K.Y1 + 1, 10 ** 7, 'truth%d' % rr)
        for c in new:
            st = fresh(c)
            if c['imposed'] >= K.ACT:
                st['sched'] = min(st['sched'], act_cap(c))
            lg = []
            run(rng, c, st, K.Y1 + 400, lg, act=True)
            for e in lg:
                if e.get('revoked') and K.Y0 <= e['decided'] <= K.Y1:
                    n += 1
                    monthly[min(11, int((e['decided'] - K.Y0) // M))] += 1
        res.append(n)
    out = (float(np.mean(res)), float(np.std(res)))
    return (out, monthly / reps) if by_month else out
