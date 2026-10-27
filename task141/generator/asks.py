"""The two asks' figures on the world (the truth the pack must reproduce).

Ask A: for each quarter from October 2025 to September 2026, the felony and the misdemeanor violator bed-days: one for
each person in the Detention Center at 00:00 county time on a revocation commitment, felony when the commitment revokes
a felony term (a person held on commitments revoking a felony and a misdemeanor term counted once, as felony).
Ask B: the average term imposed at sentencing, in months, of the felony probationers on supervision on 30 September
2026, by supervising office and by time on supervision (under one year, one to under two, two to under three, three
or more)."""
from __future__ import annotations

import numpy as np

import common as K

QDAYS = [(K.day(a), K.day(b), lab) for a, b, lab in K.QUARTERS]


def quarter_of(d):
    for i, (a, b, _) in enumerate(QDAYS):
        if a <= d <= b:
            return i
    return None


def bed_days_truth(B):
    """from the generator's custody segments, each carrying the level of the commitment it serves"""
    tab = np.zeros((4, 2), dtype=int)
    stop = K.at(K.EXTRACT + 1, 0)
    for b in B:
        if b.cls not in ("PV-FEL", "PV-MIS"):
            continue
        end = b.end or stop
        d = K.day(b.start.date()) + 1
        while K.at(d, 0) < end:
            q = quarter_of(d)
            if q is not None:
                tab[q, 0 if b.lvl == "F" else 1] += 1
            d += 1
    return tab


def open_felony(W):
    out = []
    for c in W.cases:
        if c['lvl'] != 'F' or c['sup'] > K.EXTRACT:
            continue
        st = W.states[c['id']]
        if st['closed'] is not None and st['closed'][0] <= K.EXTRACT:
            continue
        out.append(c)
    return out


def sup_band(c):
    if c['sup'] > K.day('2025-09-30'):
        return 0
    if c['sup'] > K.day('2024-09-30'):
        return 1
    if c['sup'] > K.day('2023-09-30'):
        return 2
    return 3


def ask_b_truth(W, as_it_stands=False):
    """average imposed term by office and by time on supervision; as_it_stands takes CMS 2's term_months"""
    ext = {}
    for c in W.cases:
        ext[c['id']] = sum(m[4] for m in W.states[c['id']]['mods'] if m[0] <= K.EXTRACT and m[3] == 'EXTEND')
    by_off, by_sup = {}, {}
    for c in open_felony(W):
        t = c['term'] + (ext[c['id']] if as_it_stands else 0)
        by_off.setdefault(c['office'], []).append(t)
        by_sup.setdefault(sup_band(c), []).append(t)
    offs = [np.mean(by_off[o[0]]) for o in K.OFFICES]
    sups = [np.mean(by_sup[k]) for k in range(4)]
    return offs, sups, {o[0]: len(by_off[o[0]]) for o in K.OFFICES}, [len(by_sup[k]) for k in range(4)]
