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
          ("windows of terms with nothing pending", dict(pwin_free=True)))
GOLD = dict(score_adjust=False)
RUNGS = (("persistence", "the trailing year's felony revocation admissions carried into 2027"),
         ("two_clock_from_supervision_start", "the two clocks with each term's exposure counted from the start of its "
                                              "supervision, before the extracts begin"),
         ("rate_on_exposure", "the trailing year's admissions per case-month on supervision, times the case-months "
                              "the Act leaves in 2027"),
         ("one_clock_by_term", "the hazard by month on supervision and term length, carried to each term's end under "
                               "the Act"),
         ("one_clock", "the hazard by month on supervision with the risk score, carried to each term's end under the "
                       "Act (the default path)"),
         ("two_clock_no_transition", "the two clocks, the petitions of the terms the Act ends on 31 March 2027 left "
                                     "out"),
         ("golden", "the two clocks: ordinary petitions by month on supervision, end-of-term petitions on each term's "
                    "end under the Act"))


def quarter_of(d):
    for i, (a, b, _) in enumerate(QDAYS):
        if a <= d <= b:
            return i
    return None


# ---------------------------------------------------------------------------------------------------- the call
def call(R):
    total, parts, est = F.two_clock(R, **GOLD)
    return dict(total=total, parts=parts, est=est, pods=K.pods(total), printed=K.round_to(total, 100))


def transition_terms(R):
    """open felony terms at the extract that section 4 ends on 31 March 2027 if still running"""
    n = 0
    for c in R.active:
        if R.sched_now[c["id"]] > K.TRANS and F.act_cap(c) == K.TRANS:
            n += 1
    return n


def end_of_term_share(R, window=120):
    """the record's terms reaching their last `window` days alive with nothing pending, and the share carrying a
    petition filed in those days, against the same days a year earlier"""
    E = F.estimates(R, window, score_adjust=False)
    near = E["wpet"] / E["reach"]
    reach0 = wpet0 = 0
    for c in R.cases:
        ps = R.byc.get(c["id"], [])
        e = F.end_of(R, c) if c["id"] in R.close else K.EXTRACT + 1
        for i, (since, s) in enumerate(R.scheds[c["id"]]):
            until = R.scheds[c["id"]][i + 1][0] if i + 1 < len(R.scheds[c["id"]]) else 10 ** 9
            wo = s - window - 365
            if s > K.EXTRACT - 30 or not (since <= wo < until) or e <= wo or c["sup"] > wo:
                continue
            reach0 += 1
            if any(wo <= p["file"] < wo + window for p in ps):
                wpet0 += 1
    return dict(near=near, reach=E["reach"], wpet=E["wpet"], year_before=wpet0 / reach0, reach0=reach0, wpet0=wpet0)


def rungs(R):
    out = {}
    out["golden"] = F.two_clock(R, **GOLD)[0]
    out["persistence"] = float(F.persistence(R))
    out["rate_on_exposure"] = F.rate_on_exposure(R)
    out["one_clock"] = F.one_clock(R)
    out["one_clock_by_term"] = F.one_clock(R, by_term=True)
    out["two_clock_no_transition"] = F.two_clock(R, skip_transition=True, **GOLD)[0]
    out["two_clock_from_supervision_start"] = from_start(R)
    fam = {}
    for name, kw in FAMILY:
        fam[name] = F.two_clock(R, **dict(GOLD, **kw))[0]
    return out, fam


def from_start(R):
    """the two clocks with every term's exposure counted from the day its supervision began, though the extracts
    hold no petition before 1 July 2016 (no delayed entry)"""
    keep = K.RECORD_START
    K.RECORD_START = -10 ** 6
    try:
        S = F.Rec()
        S.__dict__.update({k: v for k, v in R.__dict__.items() if k != "cache"})
        F.finish(S)
        return F.two_clock(S, **GOLD)[0]
    finally:
        K.RECORD_START = keep


def monthly_2027(R):
    out = []
    for mth in range(1, 13):
        a = dt.date(2027, mth, 1)
        b = dt.date(2027 + (mth == 12), 1 if mth == 12 else mth + 1, 1) - dt.timedelta(days=1)
        out.append(F.two_clock(R, y0=K.day(a), y1=K.day(b), **GOLD)[0])
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
def commitment_levels(P, how="golden"):
    """each probation commitment booking with the level of the term its commitment revokes; how: golden (linked to
    the court's revocation), classification (PV-FEL felony, PV-MIS misdemeanor), utc_as_local (linked, new system's
    times read as local), current_ids (linked through current Sheriff's numbers only)"""
    B = PR.bookings(P, utc_as_local=how in ("utc_as_local", "classification_utc"))
    so2p = PR.sheriff_to_person(P, merged=how != "current_ids")
    T = PR.terms(P)
    rev = {}
    for p in P["pets"]:
        if p["disposition"] == "REVOKED":
            t = T[p["case_number"]]
            rev.setdefault(t["person"], []).append((PR.iso(p["disposition_date"]), t["lvl"], p["served_as"]))
    by = {}
    for b in B:
        by.setdefault(so2p.get(b["so"], b["so"]), []).append(b)
    out = []
    known = set(so2p.values())
    for key, lst in by.items():
        lst.sort(key=lambda b: b["start"])
        person = key if key in known else None
        prev = None
        for b in lst:
            if b["cls"] in ("PV-FEL", "PV-MIS"):
                lvl = None
                b["first"] = True
                if how.startswith("classification"):
                    lvl = "F" if b["cls"] == "PV-FEL" else "M"
                elif prev is not None and prev["cls"] == b["cls"] and prev.get("lvl") and prev["end"] is not None and (
                        prev["end"] == b["start"] or (prev["reason"] == "TRANSFER TO ANNEX"
                                                      and dt.timedelta(0) < b["start"] - prev["end"] <= dt.timedelta(hours=2))):
                    lvl = prev["lvl"]
                    b["first"] = False
                elif b["cls"] == "PV-MIS":
                    lvl = "M"
                elif person is None:
                    lvl = "F"
                else:
                    day_rev = [r for r in rev.get(person, []) if r[0] == b["start"].date()]
                    if day_rev:
                        lvl = "F" if any(r[1] == "F" for r in day_rev) else "M"
                    else:
                        wk = [r for r in rev.get(person, []) if r[2] == "WEEKENDS" and r[0] < b["start"].date()]
                        lvl = max(wk)[1] if wk else "F"
                b["lvl"] = lvl
                out.append(b)
            prev = b
    return out


def bed_days(P, how="golden", holds=False):
    tab = np.zeros((4, 2), dtype=int)
    stop = K.at(K.EXTRACT + 1, 0)
    for b in commitment_levels(P, how):
        end = b["end"] or stop
        d = K.day(b["start"].date()) + 1
        while K.at(d, 0) < end:
            q = quarter_of(d)
            if q is not None:
                tab[q, 0 if b["lvl"] == "F" else 1] += 1
            d += 1
    if holds:
        for b in PR.bookings(P):
            if b["cls"] != "PV-HOLD":
                continue
            end = b["end"] or stop
            d = K.day(b["start"].date()) + 1
            while K.at(d, 0) < end:
                q = quarter_of(d)
                if q is not None:
                    tab[q, 0] += 1
                d += 1
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


def imposed_terms(P, how="golden"):
    """average term imposed at sentencing of the felony probationers on supervision at the extract, by office and by
    time on supervision; how: golden (term length less the months the term orders extended it), as_it_stands (term
    length), not_past_expiration (golden, open terms past their scheduled expiration left out), from_dates
    (expiration less supervision begin, in months)"""
    T = PR.terms(P)
    by_off, by_sup = {}, {}
    for t in T.values():
        if t["lvl"] != "F" or not t["open"]:
            continue
        if how == "not_past_expiration" and t["exp"] <= K.EXTRACT:
            continue
        v = {"golden": t["imposed"], "not_past_expiration": t["imposed"], "as_it_stands": t["length"],
             "from_dates": (t["exp"] - t["sup"]) / M}[how]
        by_off.setdefault(t["office"], []).append(v)
        by_sup.setdefault(sup_band(t["sup"]), []).append(v)
    offs = [float(np.mean(by_off[o[0]])) for o in K.OFFICES]
    sups = [float(np.mean(by_sup[k])) for k in range(4)]
    return offs, sups, [len(by_off[o[0]]) for o in K.OFFICES], [len(by_sup[k]) for k in range(4)]


# ---------------------------------------------------------------------------------------------------- all figures
def compute(P=None):
    P = P or PR.read()
    R = PR.record(P)
    G = call(R)
    rg, fam = rungs(R)
    share = end_of_term_share(R)
    mon = monthly_2027(R)
    hist = history(P)
    A = bed_days(P)
    offs, sups, n_off, n_sup = imposed_terms(P)
    trail = sum(v for (y, m), v in hist if (y, m) >= (2025, 10))
    return dict(R=R, call=G, rungs=rg, family=fam, share=share, monthly=mon, history=hist, ask_a=A, ask_b=(offs, sups),
                ask_b_n=(n_off, n_sup), transition=transition_terms(R), trailing=trail, P=P)
