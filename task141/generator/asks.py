"""The two asks' figures on the world (the truth the pack must reproduce).

Ask A: for each quarter from October 2025 to September 2026, the felony and the misdemeanor violator bed-days: one for
each person in the Detention Center at 00:00 county time on a revocation commitment, felony when the commitment revokes
a felony term (a person held on commitments revoking a felony and a misdemeanor term counted once, as felony).
Ask B: the felony probationers on supervision on 30 September 2026 in each supervising office by time on supervision
(under one year, one to under two, two to under three, three or more)."""
from __future__ import annotations

import numpy as np

import common as K

QDAYS = [(K.day(a), K.day(b), lab) for a, b, lab in K.QUARTERS]


def quarter_of(d):
    for i, (a, b, _) in enumerate(QDAYS):
        if a <= d <= b:
            return i
    return None


def bed_days_truth(W):
    """from the world's commitments, each from the court's order to its release (a weekend sentence weekend by
    weekend): a person at 00:00 on any commitment is a violator bed-day, felony if any commitment then running revokes
    a felony term"""
    stop = K.at(K.EXTRACT + 1, 0)
    days = {}
    for person, a, b, lvl in W.commit_spans:
        end = min(b, stop)
        d = K.day(a.date()) + 1
        while K.at(d, 0) < end:
            k = (person, d)
            if days.get(k) != "F":
                days[k] = lvl
            d += 1
    tab = np.zeros((4, 2), dtype=int)
    for (person, d), lvl in days.items():
        q = quarter_of(d)
        if q is not None:
            tab[q, 0 if lvl == "F" else 1] += 1
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


def ask_b_truth(W, at_intake=False):
    """felony probationers on supervision at the extract by supervising office (the office of the officer then
    supervising the term) and time on supervision; at_intake takes the office CMS 2 keeps (the office that took the
    term in)"""
    tab = {(o[0], k): 0 for o in K.OFFICES for k in range(4)}
    for c in open_felony(W):
        o = W.sup_office[c['id']] if at_intake else W.officer_hist[c['id']][-1][2]
        tab[(o, sup_band(c))] += 1
    return tab
