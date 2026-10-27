"""Cut the pack's record files from the world: the Department's two case-management exports, the Circuit Court's term
orders and violation petitions, the Detention Center's probation bookings, the person crosswalk, the daily headcount
and the code lists. Every file is written as its own system exports it."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as K
import world as WD

M = K.M


# ---------------------------------------------------------------------------------------------------- identifiers
def assign_ids(W):
    """court case numbers by year of imposition and level, the Department's person numbers, Sheriff's numbers with
    the merges the Sheriff's Office made when it found one person under two numbers"""
    r = K.rng('ids')
    seq = {}
    for c in sorted(W.cases, key=lambda c: (c['imposed'], c['id'])):
        y = K.date_of(c['imposed']).year
        key = (y, c['lvl'])
        seq[key] = seq.get(key, 0) + int(r.integers(1, 4))
        c['case_no'] = '%d-%s-%06d' % (y, 'CF' if c['lvl'] == 'F' else 'CM', seq[key])
    perm = r.permutation(np.arange(110000, 110000 + W.n_persons * 3))[:W.n_persons]
    W.apd_id = {i: 'AP%06d' % int(perm[i]) for i in range(W.n_persons)}
    sperm = r.permutation(np.arange(2100000, 2100000 + W.n_persons * 4))
    W.so_id = {i: 'SO%07d' % int(sperm[i]) for i in range(W.n_persons)}
    # a person booked under a second number before the records were merged
    W.so_old, W.merge_day = {}, {}
    k = W.n_persons
    for i in range(W.n_persons):
        if r.random() < 0.025:
            W.so_old[i] = 'SO%07d' % int(sperm[k]); k += 1
            W.merge_day[i] = int(r.integers(K.day('2019-06-01'), K.day('2026-08-31')))
    # PV-OOS: people held for other states, in no Okelan register
    W.oos = []
    for j in range(560):
        W.oos.append('SO%07d' % int(sperm[k])); k += 1


def sheriff_for(W, person, d):
    if person in W.so_old and d < W.merge_day[person]:
        return W.so_old[person]
    return W.so_id[person]


# ---------------------------------------------------------------------------------------------------- registers
def legacy_score(score, r):
    """CMS 1 scored the risk screen on its 0 to 40 scale; the 2023 rescaling halved it"""
    return int(np.clip(2 * score + int(r.integers(0, 2)), 0, 40))


def _mdY(n):
    d = K.date_of(n)
    return '%02d/%02d/%04d' % (d.month, d.day, d.year)


def register_rows(W):
    """CMS 1 holds the terms closed before the 12 June 2023 move; CMS 2 the terms open that day, which moved
    across with their history, and every term opened since. A term enters the Department's register the day
    supervision begins, so a term still in its jail condition at the extract is in neither."""
    rows1, rows2 = [], []
    leg = {o[0]: o[2] for o in K.OFFICES}
    close1 = {'REVOKED': 'REV', 'EXPIRED': 'EXP', 'EARLY_TERM': 'ETERM'}
    close2 = {'REVOKED': 'REVOKED', 'EXPIRED': 'EXPIRED', 'EARLY_TERM': 'EARLY TERMINATION'}
    for c in sorted(W.cases, key=lambda c: (c['sup'], c['id'])):
        if c['sup'] > K.EXTRACT:
            continue
        st = W.states[c['id']]
        closed = st['closed'] if st['closed'] is not None and st['closed'][0] <= K.EXTRACT else None
        if closed is not None and closed[0] < K.RECORD_START:
            continue
        r = K.rng('register', c['id'])
        mods = [m for m in st['mods'] if m[0] <= K.EXTRACT]
        exp_now = c['orig']
        ext_months = 0
        for m in mods:
            if m[3] in ('EXTEND', 'TOLL'):
                exp_now = m[2]
                ext_months += m[4]
        if closed is not None and closed[0] < K.CMS2_LIVE:
            rows1.append(dict(CASE_NO=c['case_no'], APD_PERSON_NO=W.apd_id[c['person']], LEVEL=c['lvl'],
                              OFFICE=leg[c['office']], SUP_BEGIN=_mdY(c['sup']),
                              TERM_DAYS=int(round((c['term'] + ext_months) * M)),
                              EXPIRES=_mdY(exp_now), RISK_SCORE=legacy_score(c['score'], r), STATUS='CLSD',
                              CLOSE_DATE=_mdY(closed[0]), CLOSE_CODE=close1[closed[1]]))
            continue
        migrated = c['sup'] < K.CMS2_LIVE
        rows2.append(dict(case_number=c['case_no'], person_id=W.apd_id[c['person']],
                          offense_level='FELONY' if c['lvl'] == 'F' else 'MISDEMEANOR', office=c['office'],
                          supervision_begin=K.date_of(c['sup']).isoformat(), term_months=c['term'] + ext_months,
                          expiration_date=K.date_of(exp_now).isoformat(), csrs_score=c['score'],
                          case_status='CLOSED' if closed else 'OPEN',
                          closed_date=K.date_of(closed[0]).isoformat() if closed else None,
                          closure_reason=close2[closed[1]] if closed else None, moved_from_cms1='Y' if migrated else 'N'))
    return rows1, rows2


CMS1_COLS = ['CASE_NO', 'APD_PERSON_NO', 'LEVEL', 'OFFICE', 'SUP_BEGIN', 'TERM_DAYS', 'EXPIRES', 'RISK_SCORE', 'STATUS',
             'CLOSE_DATE', 'CLOSE_CODE']
CMS2_COLS = ['case_number', 'person_id', 'offense_level', 'office', 'supervision_begin', 'term_months', 'expiration_date',
             'csrs_score', 'case_status', 'closed_date', 'closure_reason', 'moved_from_cms1']


# ---------------------------------------------------------------------------------------------------- court
ORDER_COLS = ['case_number', 'order_date', 'order_type', 'months_extended', 'days_tolled', 'term_months_after',
              'expiration_before', 'expiration_after']


def order_rows(W):
    """every order that changed a term's scheduled expiration: tolling for the time a warrant was out, an extension
    after a petition was continued, an early termination"""
    out = []
    for c in W.cases:
        st = W.states[c['id']]
        term = c['term']
        for m in st['mods']:
            d, old, new, typ, ext = m
            if d > K.EXTRACT or d < K.RECORD_START or typ == 'ACT':
                continue
            if typ == 'EARLY TERMINATION':
                out.append(dict(case_number=c['case_no'], order_date=K.date_of(d).isoformat(), order_type='EARLY TERMINATION',
                                term_months_after=term, expiration_before=K.date_of(old).isoformat(),
                                expiration_after=K.date_of(d).isoformat()))
                continue
            toll = new - old - K.months(ext)
            mid = old
            if toll > 0:
                mid = old + toll
                out.append(dict(case_number=c['case_no'], order_date=K.date_of(d).isoformat(), order_type='TOLLING',
                                days_tolled=toll, term_months_after=term, expiration_before=K.date_of(old).isoformat(),
                                expiration_after=K.date_of(mid).isoformat()))
            if ext:
                term += ext
                out.append(dict(case_number=c['case_no'], order_date=K.date_of(d).isoformat(), order_type='EXTENSION',
                                months_extended=ext, term_months_after=term, expiration_before=K.date_of(mid).isoformat(),
                                expiration_after=K.date_of(new).isoformat()))
    rank = {'TOLLING': 0, 'EXTENSION': 1, 'EARLY TERMINATION': 2}
    out.sort(key=lambda r: (r['order_date'], r['case_number'], rank[r['order_type']]))
    return out


PET_COLS = ['petition_no', 'case_number', 'filed_date', 'allegations', 'process', 'disposition_date', 'disposition',
            'jail_days_ordered', 'served_as']


def petition_rows(W):
    out = []
    n = 0
    allp = []
    for cid, lg in W.log.items():
        c = W.C[cid]
        for e in lg:
            if e['file'] > K.EXTRACT:
                continue
            allp.append((e['file'], c['case_no'], c, e))
    allp.sort(key=lambda t: (t[0], t[1]))
    seq = {}
    for f, cno, c, e in allp:
        y = K.date_of(f).year
        seq[y] = seq.get(y, 0) + 1
        e['petition_no'] = 'VP-%d-%05d' % (y, seq[y])
        if f < K.RECORD_START:
            continue
        pend = e['decided'] > K.EXTRACT
        if pend:
            disp = None
        elif e.get('revoked'):
            disp = 'REVOKED'
        else:
            disp = 'CONTINUED AND EXTENDED' if e.get('ext') else ('CONTINUED' if K.rng('disp', c['id'], e['seq']).random() < 0.7 else 'DISMISSED')
        out.append(dict(petition_no=e['petition_no'], case_number=cno, filed_date=K.date_of(f).isoformat(),
                        allegations=';'.join(e['alleg']), process='WARRANT' if e['warrant'] else 'SUMMONS',
                        disposition_date=None if pend else K.date_of(e['decided']).isoformat(), disposition=disp,
                        jail_days_ordered=e['jail_days'] if disp == 'REVOKED' else None,
                        served_as=('WEEKENDS' if e['intermittent'] else 'CONSECUTIVE') if disp == 'REVOKED' else None))
    return out


# ---------------------------------------------------------------------------------------------------- jail
class Booking:
    __slots__ = ('person', 'so', 'start', 'end', 'cls', 'fac', 'reason', 'oos', 'lvl')

    def __init__(self, person, start, end, cls, fac, reason, so=None, lvl=None):
        self.person, self.start, self.end, self.cls, self.fac, self.reason = person, start, end, cls, fac, reason
        self.so, self.oos, self.lvl = so, False, lvl


def _next_friday(n):
    d = K.date_of(n)
    return n + ((4 - d.weekday()) % 7)


def bookings(W):
    """the custody the record implies, as local datetimes: jail conditions, holds on a warrant to the hearing,
    commitments on revocation (one per person and hearing day; a felony probationer's commitment carries the felony
    classification whatever term it revokes), annex moves, weekend sentences, out-of-state holds; then swept into one
    booking at a time per person (resolve)"""
    B = []
    lo, hi = K.at(K.BOOKINGS_FROM, 0), K.at(K.EXTRACT + 1, 0)
    for c in W.cases:
        if c['jail']:
            r = K.rng('cond', c['id'])
            a = K.at(c['imposed'], int(r.integers(13 * 60, 17 * 60 + 30)))
            b = K.at(c['imposed'] + c['jail'], int(r.integers(6 * 60 + 30, 10 * 60)))
            B.append(Booking(c['person'], a, b, 'PROB-COND', 'MAIN', 'SENTENCE COMPLETE'))
    commits = {}
    for cid, lg in W.log.items():
        c = W.C[cid]
        for e in lg:
            r = K.rng('jail', cid, e['seq'])
            hear = K.at(min(e['decided'], 10 ** 6), e['hearing_min'])
            decided = e['decided'] <= K.EXTRACT
            if e['warrant'] and e['arrest'] is not None:
                a = K.at(e['arrest'], int(r.integers(0, 24 * 60)))
                if decided and e.get('revoked'):
                    if a < hear:
                        B.append(Booking(c['person'], a, hear, 'PV-HOLD', 'MAIN', 'RECLASSIFIED'))
                elif decided:
                    if e['arrest'] < e['decided']:
                        B.append(Booking(c['person'], a, hear + dt.timedelta(minutes=int(r.integers(60, 300))), 'PV-HOLD',
                                         'MAIN', 'RETURNED TO SUPERVISION'))
                elif e['arrest'] <= K.EXTRACT:
                    B.append(Booking(c['person'], a, None, 'PV-HOLD', 'MAIN', None))
            if decided and e.get('revoked'):
                key = (c['person'], e['decided'])
                commits.setdefault(key, []).append((c, e, hear))
    W.commitments = []
    for (person, d), lst in sorted(commits.items()):
        lst.sort(key=lambda t: (t[0]['lvl'] != 'F', t[0]['id']))
        c, e, hear = lst[0]
        felony = any(x[0]['lvl'] == 'F' for x in lst)
        lvl = 'F' if felony else 'M'
        cls = 'PV-FEL' if (felony or WD.on_felony(W, person, d)) else 'PV-MIS'
        r = K.rng('commit', person, d)
        W.commitments.append(dict(person=person, day=d, lvl=lvl, cls=cls))
        if c['lvl'] == 'M' and e['intermittent'] and not felony:
            f0 = _next_friday(d + 7)
            for k in range(e['jail_days'] // 2):
                fr = f0 + 7 * k
                a = K.at(fr, int(r.integers(17 * 60 + 30, 19 * 60 + 30)))
                b = K.at(fr + 2, int(r.integers(16 * 60 + 30, 18 * 60 + 30)))
                B.append(Booking(person, a, b, cls, 'MAIN', 'SCHEDULED RELEASE', lvl=lvl))
            continue
        days = max(e['jail_days'] for _, e, _ in lst)
        served = max(1, int(round(days * e['served_share'])))
        end = K.at(d + served, int(r.integers(6 * 60, 11 * 60)))
        if e['annex'] and served > 20:
            mv = hear + dt.timedelta(days=int(served * e['annex_at']), minutes=int(r.integers(9 * 60, 15 * 60)))
            mv = mv.replace(hour=9, minute=0, second=0, microsecond=0) + dt.timedelta(minutes=int(r.integers(0, 6 * 60)))
            arr = mv + dt.timedelta(minutes=int(r.integers(20, 95)))
            B.append(Booking(person, hear, mv, cls, 'MAIN', 'TRANSFER TO ANNEX', lvl=lvl))
            B.append(Booking(person, mv, arr, cls, 'TRANSIT', None, lvl=lvl))
            B.append(Booking(person, arr, end, cls, 'ANNEX', 'SENTENCE COMPLETE', lvl=lvl))
        else:
            B.append(Booking(person, hear, end, cls, 'MAIN', 'SENTENCE COMPLETE', lvl=lvl))
    r = K.rng('oos')
    for so in W.oos:
        d0 = int(r.integers(K.BOOKINGS_FROM - 30, K.EXTRACT - 2))
        a = K.at(d0, int(r.integers(0, 24 * 60)))
        b = a + dt.timedelta(days=int(r.integers(3, 46)), minutes=int(r.integers(0, 600)))
        bk = Booking(None, a, b if b < hi else None, 'PV-OOS', 'MAIN', 'RELEASED TO SENDING STATE' if b < hi else None, so=so)
        bk.oos = True
        B.append(bk)
    B = resolve(B)
    out = []
    for b in B:
        if b.end is not None and b.end < lo:
            continue
        if b.start >= hi:
            continue
        if b.end is not None and b.end >= hi:
            b.end, b.reason = None, None
        out.append(b)
    out.sort(key=lambda b: (b.start, b.so or '', b.person if b.person is not None else -1, b.cls))
    return out


RANK = {'PV-FEL': 4, 'PV-MIS': 3, 'PV-HOLD': 2, 'PROB-COND': 1}


def resolve(B):
    """one booking at a time per person: at each moment the person is booked under the highest-ranking ground of
    custody then running (a felony commitment over a misdemeanor one, either over a hold, a hold over a jail
    condition); a change of ground while the person stays in custody closes the booking RECLASSIFIED and opens the
    next at the same moment, and a booking closes with its own reason when custody ends"""
    far = K.at(K.EXTRACT + 4000, 0)
    out, by = [], {}
    for b in B:
        if b.oos:
            out.append(b)
        else:
            by.setdefault(b.person, []).append(b)
    for person, lst in by.items():
        ev = {}
        for i, b in enumerate(lst):
            assert b.end is None or b.end > b.start, (person, b.cls, b.start, b.end)
            ev.setdefault(b.start, ([], []))[0].append(i)
            ev.setdefault(b.end or far, ([], []))[1].append(i)
        active = set()
        cur, cur_key, cur_start = None, None, None
        for t in sorted(ev):
            starts, ends = ev[t]
            ended = [i for i in ends if i in active]
            active.difference_update(ends)
            active.update(starts)
            if active:
                top = max(active, key=lambda i: (RANK[lst[i].cls], lst[i].lvl == 'F', lst[i].start, i))
                key = (lst[top].cls, lst[top].fac, lst[top].lvl)
            else:
                top, key = None, None
            if key == cur_key:
                continue
            if cur is not None:
                if key is None or key[1] == 'TRANSIT':
                    last = max(ended, key=lambda i: (RANK[lst[i].cls], i)) if ended else cur
                    reason = lst[last].reason
                else:
                    reason = 'RECLASSIFIED'
                end = None if t >= far else t
                out.append(Booking(person, cur_start, end, lst[cur].cls, lst[cur].fac, reason if end else None,
                                   lvl=lst[cur].lvl))
            if key is not None and key[1] != 'TRANSIT':
                cur, cur_key, cur_start = top, key, t
            else:
                cur, cur_key, cur_start = None, key, None
    return out


BOOK_COLS = ['booking_number', 'sheriff_id', 'booked_at', 'classification', 'facility', 'released_at', 'release_reason']


def booking_rows(W, B):
    """the old jail system to 4 February 2025 writes local times and its own booking numbers; the new system writes UTC
    and restarted the numbering. A spell open across the move was closed in the old system and opened again in the new"""
    live = K.at(K.JMS_LIVE, 3 * 60 + 10)
    rows = []
    seq_old = {}
    seq_new = {}

    def old_no(t):
        y = t.year % 100
        seq_old[y] = seq_old.get(y, 0) + 1
        return 'B%02d%06d' % (y, seq_old[y])

    def new_no(t):
        seq_new[t.year] = seq_new.get(t.year, 0) + 1
        return 'OK%d%06d' % (t.year, seq_new[t.year])

    def fmt_old(t):
        return None if t is None else '%02d/%02d/%04d %02d:%02d' % (t.month, t.day, t.year, t.hour, t.minute)

    def fmt_new(t):
        if t is None:
            return None
        u = K.to_utc(t)
        return u.strftime('%Y-%m-%dT%H:%M:00Z')
    for b in B:
        so = b.so if b.oos else sheriff_for(W, b.person, b.start.toordinal() - K.DAY0.toordinal())
        if b.start < live and (b.end is None or b.end > live):
            rows.append(dict(booking_number=old_no(b.start), sheriff_id=so, booked_at=fmt_old(b.start), classification=b.cls,
                             facility=b.fac, released_at=fmt_old(live), release_reason='CONVERTED TO NEW JMS'))
            t2 = live
            rows.append(dict(booking_number=new_no(t2), sheriff_id=so, booked_at=fmt_new(t2), classification=b.cls,
                             facility=b.fac, released_at=fmt_new(b.end), release_reason=b.reason))
        elif b.start < live:
            rows.append(dict(booking_number=old_no(b.start), sheriff_id=so, booked_at=fmt_old(b.start), classification=b.cls,
                             facility=b.fac, released_at=fmt_old(b.end), release_reason=b.reason))
        else:
            rows.append(dict(booking_number=new_no(b.start), sheriff_id=so, booked_at=fmt_new(b.start), classification=b.cls,
                             facility=b.fac, released_at=fmt_new(b.end), release_reason=b.reason))
    return rows


PERSON_COLS = ['apd_person_id', 'sheriff_id', 'sheriff_id_status', 'merged_into', 'merged_on']


def exported(W, c):
    st = W.states[c['id']]
    if c['sup'] > K.EXTRACT:
        return False
    return not (st['closed'] is not None and st['closed'][0] < K.RECORD_START)


def person_rows(W):
    out = []
    seen = set()
    for c in W.cases:
        if not exported(W, c):
            continue
        i = c['person']
        if i in seen:
            continue
        seen.add(i)
        out.append(dict(apd_person_id=W.apd_id[i], sheriff_id=W.so_id[i], sheriff_id_status='CURRENT'))
        if i in W.so_old:
            out.append(dict(apd_person_id=W.apd_id[i], sheriff_id=W.so_old[i], sheriff_id_status='MERGED',
                            merged_into=W.so_id[i], merged_on=K.date_of(W.merge_day[i]).isoformat()))
    out.sort(key=lambda r: (r['apd_person_id'], r['sheriff_id_status'] != 'CURRENT'))
    return out


# ---------------------------------------------------------------------------------------------------- headcount
HEAD_COLS = ['count_date', 'housing_unit', 'persons_at_0600']


def headcount_rows(W, B):
    """the 06:00 count by housing unit, 1 January 2025 to 30 September 2026: the five violator pods, the annex, intake
    and holding, sentenced housing and general population (people the probation extract does not hold)"""
    r = K.rng('headcount')
    d0, d1 = K.day('2025-01-01'), K.EXTRACT
    nd = d1 - d0 + 1
    arrs = {u: np.zeros(nd + 1) for u in ('pods', 'annex', 'hold', 'sent')}
    base = K.at(d0, 360)
    for b in B:
        if b.oos or b.cls == 'PV-HOLD':
            u = 'hold'
        elif b.fac == 'ANNEX':
            u = 'annex'
        elif b.cls == 'PV-FEL':
            u = 'pods'
        else:
            u = 'sent'
        e = b.end or K.at(K.EXTRACT + 2, 0)
        # count days k with s <= base + k days < e
        k0 = int(np.ceil((b.start - base).total_seconds() / 86400.0))
        k1 = int(np.ceil((e - base).total_seconds() / 86400.0))
        k0, k1 = max(k0, 0), min(k1, nd)
        if k1 > k0:
            arrs[u][k0] += 1
            arrs[u][k1] -= 1
    pods, annex, hold, sent = (np.cumsum(arrs[u])[:nd] for u in ('pods', 'annex', 'hold', 'sent'))
    gen = 610 + 25 * np.sin(np.arange(nd) / 365.25 * 2 * np.pi + 1.1) + np.cumsum(r.normal(0, 3.2, nd)) * 0.2
    out = []
    for k in range(nd):
        dd = K.date_of(d0 + k).isoformat()
        for unit, v in (('V PODS 1-5', pods[k]), ('ANNEX', annex[k]), ('INTAKE AND HOLDING', hold[k]),
                        ('SENTENCED', sent[k]), ('GENERAL POPULATION', max(0, gen[k] + r.normal(0, 9)))):
            out.append(dict(count_date=dd, housing_unit=unit, persons_at_0600=int(round(v))))
    return out
