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


_FW = np.array([c[2] for c in K.FEL_CELLS]); _FW = _FW / _FW.sum()


def act_cap(c):
    """the latest day SB 26-118 lets a felony term run to"""
    if c['imposed'] >= K.ACT:
        return K.add_months(c['sup'], 24)
    return max(K.add_months(c['sup'], 24), K.TRANS)


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
                    et=P['et_hazard'], et_after=P['et_after'], q=P['q_open'], a=P['a_pet'], b=P['b_ext'],
                    s=P['s_sub'])
    return dict(abs=P['m_abs'], conv_o=P['m_conv'], conv_r=P['m_conv'], conv_a=min(0.9, P['m_conv'] + 0.25),
                p_rev=P['m_p_rev'], p_ext=P['m_p_ext'], ext=P['m_ext_months'], p_ext_rev=P['m_p_ext'] * 0.8,
                et=P['m_et_hazard'], et_after=P['m_et_after'], q=P['m_q_open'], a=P['m_a_pet'], b=P['m_b_ext'],
                s=P['m_s_sub'])


def fresh(c):
    return dict(t=c['imposed'], sched=c['orig'], pending=None, pkind=None, pfile=None, reviewed=None, closed=None,
                had_pet=False, review_at=None, mods=[], act_applied=False, term_m=c['term'], ext_at=None, ext_m=0)


def room(c, st, act):
    """the months a court may still add to the term: under its class maximum and, once the Act is in force, under
    the Act's cap"""
    r = c['max_m'] - st['term_m']
    if act and c['lvl'] == 'F' and st['t'] >= K.ACT:
        r = min(r, (act_cap(c) - st['sched']) / M)
    return r


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
                st['ext_at'] = None
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
                ext = min(int(rng.choice(q['ext'])), int(max(0.0, room(c, st, act))))
                new += K.months(ext)
                st['term_m'] += ext
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
            st['ext_at'] = None
            if rng.random() < q['q']:
                u = rng.random()
                rm = room(c, st, act)
                if rm >= 1:
                    if u < q['b']:
                        off = int(rng.integers(P['ext_lo'], P['ext_hi'] + 1))
                        st['ext_at'] = max(st['sched'] - off, t)
                        st['ext_m'] = min(int(rng.choice(P['ext_end_months'])), int(rm))
                    elif u < q['b'] + q['a']:
                        off = int(rng.triangular(P['rev_lo'], P['rev_mode'], W))
                        st['review_at'] = max(st['sched'] - off, t)
                elif u < q['a'] + q['s'] * q['b']:
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
        xa = st['ext_at']
        if xa is not None and xa < stop and (f is None or xa <= f) and (st['review_at'] is None or xa <= st['review_at']):
            new = st['sched'] + K.months(st['ext_m'])
            st['mods'].append((xa, st['sched'], new, 'EXTEND', st['ext_m']))
            st['term_m'] += st['ext_m']
            st.update(sched=new, reviewed=None, review_at=None, ext_at=None, t=xa)
            continue
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
            st.update(pending=dec, pkind=ev, pfile=f, had_pet=True, t=f, review_at=None, ext_at=None)
            continue
        st['t'] = stop


# ---------------------------------------------------------------------------------------------------- cases
def _term_jail(r, lvl):
    if lvl == 'F':
        k = int(r.choice(len(K.FEL_CELLS), p=_FW))
        term = K.FEL_CELLS[k][1]
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


def _klass(r, lvl, term):
    """a felony term's class, drawn with its length from the State's sentencing table (FEL_CELLS); a misdemeanor
    term's class is drawn last from the case's stream (make_cases), so this returns a placeholder"""
    if lvl != 'F':
        return None, None
    mx = dict(K.CLASSES)
    ks = [i for i, (c, l, _) in enumerate(K.FEL_CELLS) if l == term]
    w = np.array([K.FEL_CELLS[i][2] for i in ks])
    k = K.FEL_CELLS[ks[int(r.choice(len(ks), p=w / w.sum()))]][0]
    return k, mx[k]


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
            klass, max_m = _klass(r, lvl, term)
            gap = jail + int(r.integers(0, 4)) if jail else int(r.integers(P['intake_lo'], P['intake_hi']))
            sc = int(np.clip(round(r.normal(10.5 if lvl == 'F' else 8.5, 3.6)), 0, 20))
            office = K.OFFICES[int(r.choice(4, p=K.OFFICE_W))][0]
            if lvl == 'M':
                klass, max_m = K.MIS_CLASSES[int(r.random() < P['m_class2'])]
            out.append(dict(id=k, lvl=lvl, imposed=s, term=term, jail=jail, sup=s + gap, score=sc,
                            orig=s + K.months(term), office=office, klass=klass, max_m=max_m))
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
    supervision(W)
    return W


# ---------------------------------------------------------------------------------------------------- offices and officers
def office_of(district, t, east):
    """the office supervising a district on day t: the eastern townships from Central or Riverside (east, the case's
    own) until Eastfield opens; a specialized caseload from Central"""
    if district == 'EFD' and t < K.EFD_OPEN:
        return east
    if district == 'SPEC':
        return 'CEN'
    return district


def officers(W):
    """the Department's line officers, one career at a time in each office's posts: a post vacated is filled after a
    vacancy, an officer is promoted in place (a new assignment row), and on Eastfield's opening the officers then in
    thirteen Central and eight Riverside posts move there with their posts, beside two new posts. W.roster maps a
    badge to its rows [office, position, from, to] (to None while the assignment runs)"""
    r = K.rng('officers')
    posts = []
    for o in ('CEN', 'NGT', 'RVS'):
        n_before, n_after = K.POOLS[o]
        moved = K.EFD_FROM.get(o, 0)
        for i in range(n_before):
            posts.append((o, 'EFD' if i < moved else o, K.BURN - int(r.integers(0, 3650))))
    for i in range(K.POOLS['EFD'][1] - sum(K.EFD_FROM.values())):
        posts.append(('EFD', 'EFD', K.EFD_OPEN))
    roster = {}
    badge = [0]

    def career(o_before, o_after, start):
        badge[0] += 1
        b = badge[0]
        leave = start + int(r.exponential(P['tenure_years'] * 365.25))
        cuts = [(start, 'PO I')]
        if start + 3 * 365 < leave:
            cuts.append((start + 3 * 365 + int(r.integers(0, 120)), 'PO II'))
        if start + 8 * 365 < leave and r.random() < 0.4:
            cuts.append((start + 8 * 365 + int(r.integers(0, 365)), 'SR PO'))
        rows = []
        for j, (a, pos) in enumerate(cuts):
            z = (cuts[j + 1][0] - 1) if j + 1 < len(cuts) else leave
            rows.append([pos, a, z])
        out = []
        for pos, a, z in rows:
            if o_before != o_after and a < K.EFD_OPEN <= z:
                out.append([o_before, pos, a, K.EFD_OPEN - 1])
                out.append([o_after, pos, K.EFD_OPEN, z])
            else:
                out.append([o_after if a >= K.EFD_OPEN else o_before, pos, a, z])
        roster[b] = out
        return leave
    for o_before, o_after, start in posts:
        t = start
        while t <= K.EXTRACT:
            leave = career(o_before, o_after, t)
            t = leave + int(r.integers(P['vacancy_lo'], P['vacancy_hi'] + 1))
            if o_before != o_after and leave < K.EFD_OPEN <= t:
                t = max(t, K.EFD_OPEN)
    for b, rows in roster.items():
        for row in rows:
            if row[3] >= K.EXTRACT + 1:
                row[3] = None
        roster[b] = [row for row in rows if row[2] <= K.EXTRACT]
    # badges are issued in order of hire
    rb = K.rng('badges')
    nxt, W.roster = 1100, {}
    for b in sorted((b for b in roster if roster[b]), key=lambda b: (roster[b][0][2], b)):
        nxt += int(rb.integers(1, 4))
        W.roster[nxt] = roster[b]
    idx = {}
    for b, rows in W.roster.items():
        for o, pos, a, z in rows:
            idx.setdefault(o, []).append((a, 10 ** 7 if z is None else z, b))
    W.post_idx = {o: (np.array([x[0] for x in v]), np.array([x[1] for x in v]), np.array([x[2] for x in v]))
                  for o, v in idx.items()}


def _pick(W, office, t, r):
    a, z, b = W.post_idx[office]
    on = b[(a <= t) & (z >= t)]
    return int(on[int(r.integers(0, len(on)))])


def _office_end(W, badge, t):
    """the last day of the officer's unbroken run at the office the officer holds on day t"""
    rows = W.roster[badge]
    i = max(j for j, row in enumerate(rows) if row[2] <= t)
    o = rows[i][0]
    z = rows[i][3]
    while z is not None and i + 1 < len(rows) and rows[i + 1][0] == o and rows[i + 1][2] == z + 1:
        i += 1
        z = rows[i][3]
    return 10 ** 7 if z is None else z


def supervision(W):
    """each term CMS 2 holds, from the day supervision begins to its close or the extract: the office that took it
    in (kept by CMS 2 as the term's office) and its officers; a move to another district transfers the term to an
    officer there, an officer's leaving his office reassigns it within the office, Eastfield's opening moves the
    eastern townships' terms to its officers"""
    officers(W)
    W.sup_office = {}
    W.officer_hist = {}
    w = np.array(K.OFFICE_W)
    codes = [o[0] for o in K.OFFICES]
    for c in W.cases:
        st = W.states[c['id']]
        if c['sup'] > K.EXTRACT:
            continue
        r = K.rng('staff', c['id'])
        east = 'CEN' if r.random() < 0.55 else 'RVS'
        t = c['sup']
        district = c['office']
        office = office_of(district, t, east)
        W.sup_office[c['id']] = office
        if st['closed'] is not None and st['closed'][0] < K.CMS2_LIVE:
            continue
        end = min(st['closed'][0], K.EXTRACT) if st['closed'] is not None else K.EXTRACT
        officer = _pick(W, office, t, r)
        hist = [(t, officer, office)]
        nxt_move = t + int(r.exponential(365.25 / P['move_rate']))
        spec = r.random() < (P['spec_fel'] if c['lvl'] == 'F' else P['spec_mis'])
        spec_at = t + int(r.integers(P['spec_lo'], P['spec_hi'] + 1)) if spec and office != 'CEN' else None
        if spec and office == 'CEN':
            district = 'SPEC'
        while True:
            ev = []
            if nxt_move <= end and district != 'SPEC':
                ev.append((nxt_move, 1, 'move'))
            oe = _office_end(W, officer, t)
            if oe + 1 <= end:
                ev.append((oe + 1, 2, 'officer'))
            if district == 'EFD' and office != 'EFD' and t < K.EFD_OPEN <= end:
                ev.append((K.EFD_OPEN, 0, 'efd'))
            if spec_at is not None and spec_at <= end:
                ev.append((spec_at, 0, 'spec'))
            if not ev:
                break
            t, _, kind = min(ev)
            if kind == 'move':
                p = w * np.array([cd != district for cd in codes])
                district = codes[int(r.choice(4, p=p / p.sum()))]
                nxt_move = t + int(r.exponential(365.25 / P['move_rate']))
                new = office_of(district, t, east)
                if new == office:
                    continue
                office = new
            elif kind == 'efd':
                office = 'EFD'
            elif kind == 'spec':
                # a specialized caseload (sex offense, serious mental illness, domestic violence) is supervised from
                # Central's specialized unit, whatever the district, once the intake assessment is done
                spec_at = None
                district = 'SPEC'
                office = 'CEN'
            officer = _pick(W, office, t, r)
            hist.append((t, officer, office))
        W.officer_hist[c['id']] = hist


def officer_at(W, cid, d):
    h = W.officer_hist[cid]
    return [x for x in h if x[0] <= d][-1]


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
