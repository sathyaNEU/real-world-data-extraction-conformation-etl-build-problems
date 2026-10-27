"""The golden from the cut pack: the 2027 projection of felony probation revocation admissions under SB 26-118 (the
two-clock construction), the pods the county's standard gives, every rung of the ladder and the standing family, and
the two asks (violator bed-days by quarter; the average imposed term of the felony probationers on supervision)."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as K
import forecast as F
import pack_read as PR

M = K.M
QDAYS = [(K.day(a), K.day(b), lab) for a, b, lab in K.QUARTERS]
FAMILY = (("window 90 days", dict(window=90)), ("window 105 days", dict(window=105)),
          ("window 150 days", dict(window=150)), ("CSRS score adjustment", dict(score_adjust=True)),
          ("mean lag", dict(mean_lag=True)), ("one conversion rate", dict(conv_pooled=True)),
          ("windows opening before 1 January 2027", dict(clip_act=False)),
          ("windows of terms with nothing pending", dict(pending_free=True)),
          ("extensions of 9 months", dict(ext_m=9)), ("extensions to the cap", dict(ext_m="cap")))
GOLD = dict(mode="golden")
RUNGS = (("persistence", "the trailing year's felony revocation admissions carried into 2027"),
         ("one_clock", "the hazard by month on supervision with the risk score, carried to each term's end under the "
                       "Act"),
         ("one_clock_by_term", "the hazard by month on supervision and term length, carried to each term's end under "
                               "the Act"),
         ("rate_on_exposure", "the trailing year's admissions per case-month on supervision, times the case-months "
                              "the Act leaves in 2027"),
         ("two_clock_no_extension", "the two clocks at the record's end-of-term rate, every term ending once under "
                                    "the Act"),
         ("pooled", "the two clocks at the record's end-of-term rates, extensions capped under the Act (the default "
                    "path)"),
         ("iia", "the would-be extensions shared between petition and lapse in the record's proportion"),
         ("full", "every would-be extension a petition"),
         ("golden", "the terms with no room to extend (the Act or the class maximum) at the end-of-term rate of the "
                    "terms the record saw at their class maximum"))


def quarter_of(d):
    for i, (a, b, _) in enumerate(QDAYS):
        if a <= d <= b:
            return i
    return None


# ---------------------------------------------------------------------------------------------------- the call
def call(R):
    total, parts, info = F.projection(R, **GOLD)
    return dict(total=total, parts=parts, info=info, pods=K.pods(total), printed=K.round_to(total, 100))


def transition_terms(R):
    """open felony terms at the extract that section 4 ends on 31 March 2027 if still running"""
    n = 0
    for c in R.active:
        if R.sched_now[c["id"]] > K.TRANS and F.act_cap(c) == K.TRANS:
            n += 1
    return n


def capped_terms(R):
    """open felony terms at the extract by their end under the Act: ended by section 4 on 31 March 2027 (scheduled
    expiration later, 24 months reached by then); ended on the day 24 months after supervision began (scheduled
    expiration later than that day, which falls after 31 March 2027); ending on their own scheduled expiration with less
    than a month of room left (under the class maximum or under the Act); ending on their own expiration with room"""
    out = dict(transition=0, cap=0, class_max=0, room=0)
    for c in R.active:
        cap = F.act_cap(c)
        s = R.sched_now[c["id"]]
        if s > K.TRANS and cap == K.TRANS:
            out["transition"] += 1
        elif s > cap:
            out["cap"] += 1
        else:
            rm = min(c["max_m"] - F.term_m_at(c, K.EXTRACT + 1), (cap - s) / M)
            out["room" if rm >= 1 else "class_max"] += 1
    return out


def rungs(R):
    out = {}
    for m in F.MODES:
        out[m] = F.projection(R, m)[0]
    out["persistence"] = float(F.persistence(R))
    out["rate_on_exposure"] = F.rate_on_exposure(R)
    out["one_clock"] = F.one_clock(R)
    out["one_clock_by_term"] = F.one_clock(R, by_term=True)
    out["two_clock_no_extension"] = F.two_clock(R, score_adjust=False)[0]
    fam = {}
    for name, kw in FAMILY:
        fam[name] = F.projection(R, **dict(GOLD, **kw))[0]
    return out, fam


def monthly_2027(R):
    out = []
    for mth in range(1, 13):
        a = dt.date(2027, mth, 1)
        b = dt.date(2027 + (mth == 12), 1 if mth == 12 else mth + 1, 1) - dt.timedelta(days=1)
        out.append(F.projection(R, y0=K.day(a), y1=K.day(b), **GOLD)[0])
    return out


def history(P):
    """felony probation revocation admissions by month from January 2019: one per person and day on which the court
    revoked a felony term"""
    T = PR.terms(P)
    seen = set()
    by = {}
    for p in P["pets"]:
        if p["disposition"] != "REVOKED" or T[p["case_number"]]["lvl"] != "F":
            continue
        d = PR.iso(p["disposition_date"])
        key = (T[p["case_number"]]["person"], d)
        if key in seen or d < dt.date(2019, 1, 1):
            continue
        seen.add(key)
        by[(d.year, d.month)] = by.get((d.year, d.month), 0) + 1
    out = []
    y, m = 2019, 1
    while (y, m) <= (2026, 9):
        out.append(((y, m), by.get((y, m), 0)))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


# ---------------------------------------------------------------------------------------------------- Ask A
def revocations(P):
    """each person's revocations: (order day, level of the term revoked, how the commitment is served)"""
    T = PR.terms(P)
    rev = {}
    for p in P["pets"]:
        if p["disposition"] == "REVOKED":
            t = T[p["case_number"]]
            rev.setdefault(t["person"], []).append((PR.iso(p["disposition_date"]), t["lvl"], p["served_as"]))
    for v in rev.values():
        v.sort()
    return rev


def commitments(P, how="golden"):
    """each commitment the bookings show, chained across annex moves, the system replacement and contiguous rows of
    one class, with its level and the first midnight it counts. how: golden (level from the term the court revoked;
    a commitment of a person the jail already held counted from the court's order, though the booking reclassifies
    only when the order reaches the jail), booking_start (level from the court, counted from the commitment booking),
    classification (PV-FEL felony, PV-MIS misdemeanor, from the booking), classification_utc and utc_as_local (the
    new system's times read as county time), current_ids (linked through current Sheriff's numbers only)"""
    B = PR.bookings(P, utc_as_local=how in ("utc_as_local", "classification_utc"))
    so2p = PR.sheriff_to_person(P, merged=how != "current_ids")
    rev = revocations(P)
    by = {}
    for b in B:
        if b["cls"] != "PV-OOS":
            by.setdefault(so2p.get(b["so"], b["so"]), []).append(b)
    out = []
    for person, lst in by.items():
        lst.sort(key=lambda b: b["start"])
        rv = rev.get(person, [])
        prev, cur = None, None
        for b in lst:
            if b["cls"] in ("PV-FEL", "PV-MIS"):
                if (cur is not None and prev["cls"] == b["cls"] and prev["end"] is not None and
                        (prev["end"] == b["start"] or (prev["reason"] == "TRANSFER TO ANNEX" and
                                                       dt.timedelta(0) < b["start"] - prev["end"] <= dt.timedelta(hours=2)))):
                    cur["end"] = b["end"]
                    prev = b
                    continue
                d0 = b["start"].date()
                held = prev is not None and prev["end"] == b["start"] and prev["reason"] == "RECLASSIFIED"
                order = None
                same = [r for r in rv if r[0] == d0 and r[2] == "CONSECUTIVE"]
                if same:
                    order = d0
                elif held:
                    near = [r[0] for r in rv if d0 - dt.timedelta(days=8) <= r[0] < d0 and r[2] == "CONSECUTIVE"]
                    order = max(near) if near else None
                if order is not None:
                    lvl = "F" if any(r[1] == "F" for r in rv if r[0] == order) else "M"
                else:
                    wk = [r for r in rv if r[2] == "WEEKENDS" and r[0] < d0]
                    lvl = max(wk)[1] if wk else "F"
                if b["cls"] == "PV-MIS":
                    lvl = "M"
                if how.startswith("classification"):
                    lvl = "F" if b["cls"] == "PV-FEL" else "M"
                first = d0 + dt.timedelta(days=1)
                if how in ("golden", "current_ids") and held and order is not None:
                    first = order + dt.timedelta(days=1)
                cur = dict(person=person, first=first, end=b["end"], lvl=lvl, order=order, start=b["start"],
                           held=held, cls=b["cls"])
                out.append(cur)
            else:
                cur = None
                if b["cls"] == "PV-HOLD" and b["end"] is None and how in ("golden", "current_ids"):
                    # still held at the extract on a commitment the court has ordered but the jail has not received
                    od = [r for r in rv if r[0] >= b["start"].date() and r[2] == "CONSECUTIVE"]
                    if od:
                        order = od[-1][0]
                        lvl = "F" if any(r[1] == "F" for r in rv if r[0] == order) else "M"
                        out.append(dict(person=person, first=order + dt.timedelta(days=1), end=None, lvl=lvl,
                                        order=order, start=b["start"], held=True, cls="PV-HOLD"))
            prev = b
    return out


def bed_days(P, how="golden", holds=False):
    stop = K.at(K.EXTRACT + 1, 0)
    days = {}
    for c in commitments(P, how):
        end = c["end"] or stop
        d = K.day(c["first"])
        while K.at(d, 0) < end:
            k = (c["person"], d)
            if days.get(k) != "F":
                days[k] = c["lvl"]
            d += 1
    if holds:
        so2p = PR.sheriff_to_person(P)
        for b in PR.bookings(P):
            if b["cls"] != "PV-HOLD":
                continue
            end = b["end"] or stop
            d = K.day(b["start"].date()) + 1
            while K.at(d, 0) < end:
                days.setdefault((so2p.get(b["so"], b["so"]), d), "F")
                d += 1
    tab = np.zeros((4, 2), dtype=int)
    for (person, d), lvl in days.items():
        q = quarter_of(d)
        if q is not None:
            tab[q, 0 if lvl == "F" else 1] += 1
    return tab


# ---------------------------------------------------------------------------------------------------- Ask B
def sup_band(sup):
    """time on supervision at the extract in whole years from the day supervision began: under one, one, two, three
    or more"""
    if sup > K.day("2025-09-30"):
        return 0
    if sup > K.day("2024-09-30"):
        return 1
    if sup > K.day("2023-09-30"):
        return 2
    return 3


def supervision_counts(P, how="golden"):
    """the felony probationers on supervision at the end of the extract in each supervising office by time on
    supervision. how: golden (the office the term's officer is assigned to at the extract), cms_office (CMS 2's
    office, the office that took the term in), first_assignment (the officer's first office on the roster),
    office_at_start (the officer's office on the day supervision began), current_assignment (the officer's open
    assignment on the roster as exported, whatever its start)"""
    T = PR.terms(P)
    ext = K.date_of(K.EXTRACT)
    off = PR.officer_office(P, ext)
    first, cur = {}, {}
    for r in P["roster"]:
        b = int(r["badge_no"])
        a = PR.dmy(r["assigned_from"])
        if b not in first or a < first[b][0]:
            first[b] = (a, r["office_code"])
        if not r["assigned_to"] and (b not in cur or a > cur[b][0]):
            cur[b] = (a, r["office_code"])
    tab = {(o[0], k): 0 for o in K.OFFICES for k in range(4)}
    for t in T.values():
        if t["lvl"] != "F" or not t["open"]:
            continue
        if how == "golden":
            o = off[t["officer"]]
        elif how == "cms_office":
            o = t["office"]
        elif how == "first_assignment":
            o = first[t["officer"]][1]
        elif how == "current_assignment":
            o = cur[t["officer"]][1]
        elif how == "office_at_start":
            o = PR.officer_office(P, K.date_of(t["sup"])).get(t["officer"]) or t["office"]
        tab[(o, sup_band(t["sup"]))] += 1
    return tab


# ---------------------------------------------------------------------------------------------------- all figures
def compute(P=None):
    P = P or PR.read()
    R = PR.record(P)
    G = call(R)
    rg, fam = rungs(R)
    mon = monthly_2027(R)
    hist = history(P)
    A = bed_days(P)
    Bt = supervision_counts(P)
    trail = sum(v for (y, m), v in hist if (y, m) >= (2025, 10))
    return dict(R=R, call=G, rungs=rg, family=fam, rates=F.window_rates(R), monthly=mon, history=hist, ask_a=A,
                ask_b=Bt, transition=transition_terms(R), capped=capped_terms(R), trailing=trail, P=P)
