"""task169 records: each person's life after release, written as the four agencies would record it.

Regime "old": the record (2019 to the cut). A parolee's arrest is answered by the Board's revocation with the
district's in-lieu share (felony A-B scaled), the person held on the parole hold until the hearing and the case
nolle prossed; otherwise the case goes to court and becomes a prison commitment with the class's probability,
admitted after the class's lag. Condition violations without an arrest are revoked with TECH_REVOKE. After the
maximum date there is no supervision and every arrest goes to court.

Regime "act": Act 26-114. No revocation of any kind; every arrest goes to court on the same terms."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import world as W
from common import RECORD_START, CUT, CLASSES, add, days

INF = float("inf")


class Book:
    def __init__(self):
        self.releases = []     # pid, release_date, rtype, max_date, district, release_no
        self.admissions = []   # pid, date, atype (NC, PVT, PVN), otn or "", violation_id or ""
        self.arrests = []      # pid, date, otn, cls, onsup
        self.cases = []        # otn, pid, arrest_date, route, disp, disp_date, sentence, sent_date
        self.violations = []   # vid, pid, report_date, vtype (N or C), otn, hearing_date, decision, term_days
        self.deaths = []       # pid, date
        self.holds = []        # vid, pid, lodged, lifted (None when the hold ended in a Department admission), admitted
        self.rescinds = []     # vid, pid, rescind date
        self.in_custody = []   # pid, scheduled release date, release type, max date (people inside at the end)
        self.n_otn = 0
        self.n_vid = 0


def _otn(book, rng):
    book.n_otn += 1
    return book.n_otn


def live(p, rng, regime, end, book, horizon=None):
    """simulate one person from p['rel0'] to `end`; returns days to first admission after the first release
    (INF if none within horizon)"""
    S = p["rel0"]
    maxd = add(S, p["term0"])
    commits = 0
    supervised = True
    rno = 1
    book.releases.append((p["pid"], S, "PAROLE", maxd, p["dist"], rno))
    first_rel = S
    first_adm = INF
    cls_p = W.CLASS_BASE[p["off"]]
    pend = []                        # (convert_date, otn, cls) prison conversions scheduled
    age_off = 0.0
    while True:
        # one spell at liberty starting S
        t = 0.0                      # days since S
        age = p["age0"] + days(p["rel0"], S) / 365.25
        eta = W.eta_of(p, age, p["priors"] + commits)
        lam0 = W.A0 * math.exp(eta) * p["z"]
        lam_max = lam0 * 1.70
        tech_rate = W.TECH_RATE * math.exp(0.4 * eta) * p["z"] ** 0.5
        nxt_arr = rng.exponential(1 / lam_max)
        nxt_tech = rng.exponential(1 / tech_rate) if (supervised and regime == "old") else INF
        nxt_death = rng.exponential(1 / W.DEATH_RATE)
        custody = None               # (admit date, atype, otn, vid, term)
        held_until = None            # a Board hold in the county jail pending a hearing that continued supervision
        while True:
            conv = min([days(S, c[0]) for c in pend], default=INF)
            ev = min(nxt_arr, nxt_tech, nxt_death, conv)
            date = add(S, int(ev)) if ev < INF else None
            if date is None or date > end:
                return first_adm
            if horizon is not None and days(first_rel, date) > horizon:
                return first_adm
            onsup = supervised and date < maxd
            if held_until is not None and date < held_until and ev in (nxt_arr, nxt_tech):
                if ev == nxt_arr:
                    nxt_arr = ev + rng.exponential(1 / lam_max)
                else:
                    nxt_tech = ev + rng.exponential(1 / tech_rate)
                continue
            if ev == nxt_death:
                book.deaths.append((p["pid"], date))
                return first_adm
            if ev == conv:
                c = min(pend, key=lambda x: x[0])
                pend.remove(c)
                custody = (date, "NC", c[1], "", None)
                break
            if ev == nxt_tech:
                nxt_tech = t_next = ev + rng.exponential(1 / tech_rate)
                if not onsup:
                    nxt_tech = INF
                    continue
                book.n_vid += 1
                vid = book.n_vid
                if rng.random() < W.TECH_REVOKE:
                    hd = add(date, int(rng.integers(*W.HEARING_DELAY)))
                    term = int(rng.integers(*W.REVOKE_TERM))
                    book.violations.append((vid, p["pid"], date, "C", "", hd, "REVOKED", term))
                    ad = add(hd, int(rng.integers(1, 15)))
                    book.holds.append((vid, p["pid"], date, None, ad))
                    custody = (ad, "PVT", "", vid, term)
                    break
                hd = add(date, int(rng.integers(*W.HEARING_DELAY)))
                book.violations.append((vid, p["pid"], date, "C", "", hd, "CONTINUED", 0))
                if rng.random() < 0.35:
                    book.holds.append((vid, p["pid"], date, hd, None))
                    held_until = hd
                continue
            # an arrest (thinned)
            nxt_arr = ev + rng.exponential(1 / lam_max)
            if rng.random() > W.g_of(ev) / 1.70:
                continue
            ci = rng.choice(3, p=cls_p)
            cls = CLASSES[ci]
            otn = _otn(book, rng)
            book.arrests.append((p["pid"], date, otn, cls, onsup))
            r = W.R_INLIEU[p["dist"]] * (W.R_F1_SCALE if cls == "F1" else 1.0)
            if regime == "old" and onsup and rng.random() < r:
                book.n_vid += 1
                vid = book.n_vid
                hd = add(date, int(rng.integers(*W.HEARING_DELAY)))
                term = int(rng.integers(*W.REVOKE_TERM))
                book.violations.append((vid, p["pid"], date, "N", otn, hd, "REVOKED", term))
                book.cases.append((otn, p["pid"], date, "BOARD", "NOLLE", add(hd, int(rng.integers(3, 40))), "", None))
                ad = add(hd, int(rng.integers(1, 15)))
                book.holds.append((vid, p["pid"], date, None, ad))
                custody = (ad, "PVN", otn, vid, term)
                break
            if regime == "old" and onsup:
                book.n_vid += 1
                hd = add(date, int(rng.integers(*W.HEARING_DELAY)))
                book.violations.append((book.n_vid, p["pid"], date, "N", otn, hd, "CONTINUED", 0))
                if rng.random() < 0.6:
                    book.holds.append((book.n_vid, p["pid"], date, hd, None))
                    held_until = hd
            u = rng.random()
            lag = rng.gamma(W.LAG_SHAPE, W.LAG_MEAN[cls] / W.LAG_SHAPE)
            dd = add(date, max(20, int(lag)))
            if u < W.P_PRISON[cls]:
                sd = add(dd, -int(rng.integers(1, 9)))
                book.cases.append((otn, p["pid"], date, "COURT", "CONVICTED", sd, "PRISON", sd))
                pend.append((dd, otn, cls))
            elif u < W.P_PRISON[cls] + W.P_CONVICT_OTHER[cls]:
                book.cases.append((otn, p["pid"], date, "COURT", "CONVICTED", dd,
                                   "JAIL" if rng.random() < 0.55 else "PROBATION", dd))
            else:
                book.cases.append((otn, p["pid"], date, "COURT", "DISMISSED" if rng.random() < 0.85 else "ACQUITTED",
                                   dd, "", None))
        # custody
        adate, atype, otn, vid, term = custody
        if adate > end:
            return first_adm
        if horizon is not None and days(first_rel, adate) > horizon:
            return first_adm
        book.admissions.append((p["pid"], adate, atype, otn, vid))
        if first_adm == INF:
            first_adm = days(first_rel, adate)
            if horizon is not None:
                return first_adm
        if atype == "NC":
            commits += 1
            months = float(np.clip(rng.lognormal(math.log(W.NEWCOMMIT_MONTHS[0]), W.NEWCOMMIT_MONTHS[1]), 12, 96))
            out = add(adate, int(months * 30.44))
            # conversions still pending are served concurrently
            pend = [c for c in pend if c[0] > out]
            S = out
            maxd = add(S, int(np.clip(rng.lognormal(math.log(20.0), 0.5), 6, 60) * 30.44))
            supervised = True
            rtype = "PAROLE"
        else:
            out = add(adate, term)
            if atype == "PVT" and regime == "old" and rng.random() < 0.06:
                out = add(adate, int(rng.integers(12, 46)))
                book.rescinds.append((vid, p["pid"], add(out, -int(rng.integers(0, 3)))))
            # a conversion falling inside the revocation term turns the stay into a new commitment
            inside = [c for c in pend if c[0] <= out]
            if inside:
                c = min(inside, key=lambda x: x[0])
                pend.remove(c)
                commits += 1
                months = float(np.clip(rng.lognormal(math.log(W.NEWCOMMIT_MONTHS[0]), W.NEWCOMMIT_MONTHS[1]), 12, 96))
                out = add(c[0], int(months * 30.44))
                pend = [x for x in pend if x[0] > out]
                maxd = add(out, int(np.clip(rng.lognormal(math.log(20.0), 0.5), 6, 60) * 30.44))
                rtype = "PAROLE"
                supervised = True
            elif out >= maxd:
                out = maxd
                rtype = "EXPIRATION"
                supervised = False
            else:
                rtype = "REPAROLE"
                supervised = True
            S = out
        if S > end:
            if horizon is None:
                book.in_custody.append((p["pid"], S, rtype, maxd if supervised else None, rno, commits))
            return first_adm
        rno += 1
        book.releases.append((p["pid"], S, rtype, maxd if supervised else None, p["dist"], rno))


def history():
    rng = W.stream("lives/history")
    book = Book()
    ppl = W.history_people()
    for p in ppl:
        live(p, rng, "old", CUT, book)
    return ppl, book


def cohort(ppl, book):
    """the 2027 projected releases: people inside at the cut whose release to parole falls in 2027, and people
    whose first release since 2019 falls in 2027"""
    by = {p["pid"]: p for p in ppl}
    out = []
    for pid, S, rtype, maxd, rno, commits in book.in_custody:
        if S.year != 2027 or rtype == "EXPIRATION":
            continue
        p = dict(by[pid])
        p["age0"] = p["age0"] + days(p["rel0"], S) / 365.25
        p["priors"] = p["priors"] + commits
        p["rel0"] = S
        p["term0"] = days(S, maxd)
        p["rtype"] = rtype
        p["inrecord"] = True
        out.append(p)
    for p in W.new_cohort_people():
        p = dict(p)
        p["rtype"] = "PAROLE"
        p["inrecord"] = False
        out.append(p)
    return out


def cohort_truth(cp, reps=20):
    """the expected share of the 2027 cohort admitted within 730 days, under the Act and under the old regime"""
    out = {}
    for regime in ("act", "old"):
        tot = np.zeros(len(cp))
        for r in range(reps):
            rng = W.stream("lives/cohort/%s/%d" % (regime, r))
            for i, p in enumerate(cp):
                b = Book()
                fa = live(p, rng, regime, dt.date(2031, 1, 1), b, horizon=730)
                tot[i] += fa <= 730
        out[regime] = tot / reps
    return out
