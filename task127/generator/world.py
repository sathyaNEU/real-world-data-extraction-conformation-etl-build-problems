"""The world behind the pack: every bodily injury claimant feature Ninebark Mutual's book produced from 2017 to the
January 2027 extract, how it settled, what it paid and how the two claims systems and the ledger recorded it.

The one fact no file states: from the platform going live (1 July 2024) the represented claims (the attorney-
represented injuries that carry most of the dollars) progressed at SPEED of their former pace. Everything else is
the ordinary working of the systems."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K

YEAR = 365.25


# ------------------------------------------------------------------ calendar

def _observed(d: dt.date) -> dt.date:
    if d.weekday() == 5:
        return d - dt.timedelta(days=1)
    if d.weekday() == 6:
        return d + dt.timedelta(days=1)
    return d


def _nth_weekday(y, m, wd, n):
    d = dt.date(y, m, 1)
    d += dt.timedelta(days=(wd - d.weekday()) % 7)
    return d + dt.timedelta(days=7 * (n - 1))


def _last_weekday(y, m, wd):
    d = dt.date(y, m + 1, 1) - dt.timedelta(days=1) if m < 12 else dt.date(y, 12, 31)
    return d - dt.timedelta(days=(d.weekday() - wd) % 7)


def holidays(y: int) -> set:
    """The company's office holidays: New Year, Memorial Day, Independence Day, Labor Day, Thanksgiving and the
    day after, Christmas (observed when they fall at a weekend)."""
    return {_observed(dt.date(y, 1, 1)), _last_weekday(y, 5, 0), _observed(dt.date(y, 7, 4)),
            _nth_weekday(y, 9, 0, 1), _nth_weekday(y, 11, 3, 4), _nth_weekday(y, 11, 3, 4) + dt.timedelta(days=1),
            _observed(dt.date(y, 12, 25))}


_HOL = set()
for _y in range(2016, 2029):
    _HOL |= holidays(_y)


def business(d: dt.date) -> bool:
    return d.weekday() < 5 and d not in _HOL


def next_business(d: dt.date) -> dt.date:
    while not business(d):
        d += dt.timedelta(days=1)
    return d


def nth_business_day(y: int, m: int, n: int) -> dt.date:
    d, k = dt.date(y, m, 1), 0
    while True:
        if business(d):
            k += 1
            if k == n:
                return d
        d += dt.timedelta(days=1)


def _date_of(day: float) -> dt.date:
    return (K.EPOCH + dt.timedelta(days=math.floor(day))).date()


def _day_of(d: dt.date) -> int:
    return (dt.datetime(d.year, d.month, d.day) - K.EPOCH).days


def office_time(rng, day: float, lo=8.0, hi=17.5, late=0.0) -> float:
    """A working moment on or after `day`: the next business day if `day` is not one, at an office hour
    (a share `late` in the evening, 18:00 to 22:00)."""
    d = next_business(_date_of(day))
    base = _day_of(d)
    if base == math.floor(day) and (day - base) * 24 > hi:
        d = next_business(d + dt.timedelta(days=1))
        base = _day_of(d)
    h = rng.uniform(18.0, 22.0) if rng.random() < late else rng.uniform(lo, hi)
    return base + h / 24.0


def check_run(day: float) -> float:
    """Checks print in the platform's (and the legacy system's) evening run on the business day the payment is
    approved."""
    d = next_business(_date_of(day))
    return _day_of(d) + (K.CHECK_RUN[0] + K.CHECK_RUN[1] / 60.0) / 24.0


LIVE = K.day(K.PLATFORM_LIVE)
CUT = K.day(K.CUTOVER)
VAL = K.day(K.VAL)
RUN = K.day(K.RUN)


# ------------------------------------------------------------------ the settlement clock

def clock(start: float, work_years: float, slowed: bool) -> float:
    """The day a piece of work started at `start` (days) and needing `work_years` of handling at the former pace
    is done; a slowed feature progresses at SPEED from the platform going live."""
    w = work_years * YEAR
    if not slowed:
        return start + w
    if start >= LIVE:
        return start + w / K.SPEED
    if start + w <= LIVE:
        return start + w
    return LIVE + (w - (LIVE - start)) / K.SPEED


# ------------------------------------------------------------------ the claimant features

class Feature:
    __slots__ = ("occ", "claimant", "aq", "acc", "rep", "created", "state", "kind", "work", "sev", "pays",
                 "closings", "outcome", "legacy_key", "platform_id", "claim_no", "dup_of", "system", "converted",
                 "recreated", "recreated_at", "reopen_ct_legacy", "entered", "paid_on")

    def __init__(self):
        self.pays = []          # [day, amount, method, payee, void_day or None, reissue_of index or None]
        self.closings = []      # [(close_day, disposition, reopen_day or None)]
        self.dup_of = None
        self.converted = False
        self.recreated = False
        self.recreated_at = None
        self.reopen_ct_legacy = 0
        self.legacy_key = None
        self.platform_id = None
        self.claim_no = None
        self.entered = None     # when the feature's platform record began (creation, conversion or re-entry)
        self.paid_on = None     # a duplicate feature a payment of this feature was issued on


def _lognormal(rng, median, sigma):
    return median * math.exp(sigma * rng.normal())


def simulate(seed=K.SEED):
    """Accidents quarter by quarter, each with one to three injured claimants (a claimant feature each), until the
    quarter's features are drawn."""
    rng = np.random.default_rng(seed)
    feats = []
    occ = 0
    for i in range(K.N_AQ):
        q0 = K.day(K.quarter_start(i))
        q1 = K.day(K.quarter_start(i + 1))
        n = int(rng.poisson(K.BASE_FEATURES * K.GROWTH ** (i / 4.0)))
        while n > 0:
            k = min(n, 1 if rng.random() < 0.70 else (2 if rng.random() < 0.73 else 3))
            n -= k
            occ += 1
            acc = q0 + rng.random() * (q1 - q0)
            lag = rng.exponential(K.LONG_REPORT_MEAN_DAYS) if rng.random() < K.LONG_REPORT_SHARE \
                else rng.exponential(K.REPORT_MEAN_DAYS)
            state = K.STATES[int(np.searchsorted(np.cumsum(K.STATE_SHARE), rng.random()))]
            for j in range(k):
                f = Feature()
                f.occ, f.claimant = occ, j + 1
                f.aq, f.acc, f.state = i, acc, state
                f.rep = acc + lag + (0.0 if j == 0 or rng.random() < 0.8 else rng.exponential(12.0))
                u = rng.random()
                f.kind = "cnp" if u < K.P_CNP else ("fast" if u < K.P_CNP + K.P_FAST else "rep")
                med, sd = K.WORK[f.kind]
                f.work = min(_lognormal(rng, med, sd), K.MAX_WORK)
                yrs = acc / YEAR
                if f.kind == "cnp":
                    f.sev = 0.0
                elif f.kind == "fast":
                    f.sev = K.SEV["fast"] * math.exp(K.SEV_SIGMA * rng.normal()) * K.TREND ** yrs
                else:
                    f.sev = (K.SEV["rep"] * (f.work / K.WORK["rep"][0]) ** K.SEV_WORK_POWER
                             * math.exp(K.SEV_SIGMA * rng.normal()) * K.TREND ** yrs)
                feats.append(f)
    feats.sort(key=lambda f: (f.rep, f.occ, f.claimant))
    for f in feats:
        _settle(rng, f)
    return feats


def _settle(rng, f: Feature):
    """The feature's handling: advance, settlement or other closing, reopening, and the payments that go with them."""
    slowed = f.kind == "rep"
    f.created = office_time(rng, f.rep, late=0.03)
    if rng.random() < 0.06:
        f.created = office_time(rng, f.created + rng.integers(1, 4))
    start = f.created
    close_work = clock(start, f.work, slowed)
    pays = []
    adv = None
    if f.kind == "rep" and rng.random() < K.ADVANCE_SHARE:
        w1 = min(rng.uniform(0.05, 0.30), f.work * 0.6)
        adv = check_run(clock(start, w1, slowed))
        pays.append([adv, round(K.ADVANCE_FRACTION * f.sev, 2), "CHECK", "CLAIMANT", None, None])
    close = office_time(rng, close_work, late=0.05)
    if f.kind == "cnp":
        disp = ["DENIED", "WITHDRAWN", "NO_INJURY"][int(rng.integers(0, 3))]
        f.outcome = "cnp"
    elif adv is not None and rng.random() < K.ADVANCE_THEN_NO_SETTLEMENT:
        disp = "WITHDRAWN" if rng.random() < 0.6 else "DENIED"
        f.outcome = "advance_only"
        if rng.random() < 0.3:                         # the advance check was never cashed and was voided
            pays[0][4] = office_time(rng, pays[0][0] + rng.uniform(95, 150))
            f.outcome = "advance_voided"
    elif f.kind == "rep" and adv is None and rng.random() < K.SETTLED_UNDER_PD:
        disp = "SETTLED"
        f.outcome = "settled_under_pd"
    else:
        disp = "SETTLED"
        f.outcome = "settled"
        amount = round(f.sev - (pays[0][1] if pays else 0.0), 2)
        pay_day = close - rng.uniform(0.0, 6.0)
        if amount >= K.WIRE_FROM:
            when = office_time(rng, pay_day)
            method = "WIRE"
        else:
            when = check_run(pay_day)
            method = "CHECK"
        if rng.random() < K.LIEN_SPLIT and amount > 2000:
            lien = round(amount * rng.uniform(0.08, 0.30), 2)
            pays.append([when, round(amount - lien, 2), method, "ATTORNEY" if f.kind == "rep" else "CLAIMANT", None, None])
            pays.append([when, lien, "CHECK" if method == "CHECK" else "WIRE", "LIENHOLDER", None, None])
        else:
            pays.append([when, amount, method, "ATTORNEY" if f.kind == "rep" else "CLAIMANT", None, None])
        close = max(close, when + 0.01)
        close = office_time(rng, close, late=0.05)
    reopen = None
    if f.outcome == "settled" and rng.random() < K.REOPEN.get(f.kind, 0.0):
        reopen = office_time(rng, close + rng.uniform(0.1, 3.0) * YEAR)
    elif f.outcome == "cnp" and disp == "WITHDRAWN" and rng.random() < K.REOPEN_WITHDRAWN:
        reopen = office_time(rng, close + rng.uniform(0.2, 2.5) * YEAR)     # the claimant came back with counsel
    f.closings.append([close, disp, reopen])
    if reopen is not None and f.outcome == "cnp":
        f.kind, slowed = "rep", True
        yrs = f.acc / YEAR
        f.sev = K.SEV["rep"] * math.exp(K.SEV_SIGMA * rng.normal()) * K.TREND ** yrs
        extra = min(_lognormal(rng, 1.0, 0.45), 3.0)
        reclose = office_time(rng, clock(reopen, extra, slowed), late=0.05)
        when = check_run(reclose - rng.uniform(0.0, 4.0))
        pays.append([when, round(f.sev, 2), "CHECK" if f.sev < K.WIRE_FROM else "WIRE", "ATTORNEY", None, None])
        f.outcome = "reopened_settled"
        f.closings.append([office_time(rng, max(reclose, when + 0.01), late=0.05), "SETTLED", None])
    elif reopen is not None:
        extra = min(_lognormal(rng, 0.30, 0.50), 2.0)
        reclose = office_time(rng, clock(reopen, extra, slowed), late=0.05)
        if rng.random() < 0.5:
            amt = round(0.10 * f.sev, 2)
            when = check_run(reclose - rng.uniform(0.0, 4.0))
            pays.append([when, amt, "CHECK", "ATTORNEY" if f.kind == "rep" else "CLAIMANT", None, None])
            reclose = office_time(rng, max(reclose, when + 0.01), late=0.05)
            f.closings.append([reclose, "SETTLED", None])
        else:
            f.closings.append([reclose, disp, None])
    # every feature is resolved inside ten years of its accident quarter's start (age 40 at the latest)
    limit = K.day(K.quarter_start(f.aq)) + 9.75 * YEAR
    if f.closings[-1][0] > limit:
        if len(f.closings) > 1:
            f.closings = [f.closings[0][:2] + [None]]
            pays[:] = [p for p in pays if p[0] <= f.closings[0][0] + 1.0]
        if f.closings[0][0] > limit:
            shift = f.closings[0][0] - limit
            f.closings[0][0] = office_time(rng, limit - 3.0)
            for p in pays:
                if p[0] > f.closings[0][0] - 10.0:
                    p[0] = check_run(f.closings[0][0] - 2.0) if p[2] == "CHECK" else office_time(rng, f.closings[0][0] - 2.0)
    # stale and lost checks: voided and, almost always, reissued
    for p in list(pays):
        if p[2] != "CHECK" or p[4] is not None:
            continue
        u = rng.random()
        if u < K.VOID_REISSUE:
            vd = office_time(rng, p[0] + rng.uniform(20, 120))
            p[4] = vd
            pays.append([check_run(vd + rng.uniform(1, 9)), p[1], "CHECK", p[3], None, pays.index(p)])
    f.pays = pays


# ------------------------------------------------------------------ the two systems

def assign_systems(rng, feats):
    """Which system holds each feature and under what keys: features open at the conversion weekend moved to the
    platform (CV in the legacy archive); legacy features closed before it stay in the archive, and one that reopens
    after the platform went live is re-entered on the platform with its legacy reference while the archive keeps its
    closed row; features reported from the conversion weekend on are platform features. An accident's features share
    a claim number in each system."""
    legacy_claim, platform_claim = {}, {}
    seq_legacy = {}
    seq_claim = [7100000]
    seq_feat = [10230000]
    for f in sorted(feats, key=lambda f: (f.created, f.occ, f.claimant)):
        if f.created < CUT:
            f.system = "legacy"
            if f.occ not in legacy_claim:
                yy = _date_of(f.acc).year % 100
                key = (f.state, yy)
                seq_legacy[key] = seq_legacy.get(key, 0) + int(rng.integers(1, 3))
                legacy_claim[f.occ] = ["%s-%02d-%06d" % (f.state, yy, seq_legacy[key]), 0]
            legacy_claim[f.occ][1] += 1
            f.legacy_key = "%s-%02d" % (legacy_claim[f.occ][0], legacy_claim[f.occ][1])
            if _open_at(f, CUT):
                f.converted = True
                f.entered = CUT + 0.4 + rng.uniform(0.0, 1.2)
            else:
                later = [c for c in f.closings if c[2] is not None and c[2] >= LIVE]
                if later:
                    f.recreated = True
                    f.recreated_at = later[0][2]
                    f.entered = later[0][2]
            f.reopen_ct_legacy = sum(1 for c in f.closings if c[2] is not None and c[2] < CUT)
        else:
            f.system = "platform"
            if f.created < LIVE:
                f.created = office_time(rng, LIVE)
                for c in f.closings:
                    if c[0] < f.created:
                        c[0] = office_time(rng, f.created + 1.0)
            f.entered = f.created
    for f in sorted([f for f in feats if f.entered is not None], key=lambda f: (f.entered, f.occ, f.claimant)):
        if f.occ not in platform_claim:
            seq_claim[0] += int(rng.integers(1, 3))
            platform_claim[f.occ] = "C%02d-%07d" % (_date_of(f.entered).year % 100, seq_claim[0])
        f.claim_no = platform_claim[f.occ]
        seq_feat[0] += int(rng.integers(1, 4))
        f.platform_id = "F%08d" % seq_feat[0]
    return feats


def _open_at(f: Feature, t: float) -> bool:
    """Reported and not closed at t, by the feature's own closing history."""
    if f.created > t:
        return False
    state_open = True
    for close, disp, reopen in f.closings:
        if close <= t:
            state_open = False
            if reopen is not None and reopen <= t:
                state_open = True
        else:
            break
    return state_open


def duplicates(rng, feats):
    """Features opened in error: a second feature for the same claimant on the same accident, closed as a duplicate
    within days."""
    out = []
    for f in feats:
        if rng.random() >= K.DUPLICATE_SHARE:
            continue
        d = Feature()
        d.occ, d.claimant = f.occ, f.claimant + 10
        d.aq, d.acc, d.rep, d.state, d.kind = f.aq, f.acc, f.rep, f.state, "dup"
        d.work, d.sev, d.outcome = 0.0, 0.0, "duplicate"
        d.created = office_time(rng, f.created + rng.uniform(0, 4))
        if CUT <= d.created < LIVE:
            d.created = office_time(rng, LIVE)
        d.closings = [[office_time(rng, d.created + rng.uniform(1, 20)), "DUPLICATE", None]]
        d.dup_of = f
        out.append(d)
    return out


def tidy_cutover(feats):
    """Nothing is processed over the conversion weekend: an event that would fall between the start of 29 June and
    the platform going live waits for 1 July."""
    for f in feats:
        for p in f.pays:
            if CUT <= p[0] < LIVE:
                p[0] = check_run(LIVE) if p[2] == "CHECK" else LIVE + 10.0 / 24
            if p[4] is not None and CUT <= p[4] < LIVE:
                p[4] = LIVE + 11.0 / 24
        for c in f.closings:
            if CUT <= c[0] < LIVE:
                c[0] = LIVE + 14.0 / 24
            if c[2] is not None and CUT <= c[2] < LIVE:
                c[2] = LIVE + 15.0 / 24


def keep_quarter_ends_clear(rng, feats):
    """No void lands on the last day of a calendar quarter (the ledger's quarter boundaries then carry only
    issued checks): a void that would is processed on the next business day."""
    ends = {dt.date(y, m, d) for y in range(2017, 2028) for m, d in ((3, 31), (6, 30), (9, 30), (12, 31))}
    for f in feats:
        for p in f.pays:
            if p[4] is not None and _date_of(p[4]) in ends:
                p[4] = office_time(rng, math.floor(p[4]) + 1.0)


def legacy_voids_stay_legacy(feats):
    """A legacy check is voided (and reissued) inside the legacy era or not at all: one still uncashed at the
    conversion was honoured."""
    for f in feats:
        drop = set()
        for k, p in enumerate(f.pays):
            if p[0] < CUT and p[4] is not None and p[4] >= CUT:
                p[4] = None
                drop |= {j for j, q in enumerate(f.pays) if q[5] == k}
        if drop:
            keep = [p for j, p in enumerate(f.pays) if j not in drop]
            remap = {old: new for new, old in enumerate(j for j in range(len(f.pays)) if j not in drop)}
            for p in keep:
                if p[5] is not None:
                    p[5] = remap[p[5]]
            f.pays = keep
        # a check voided before the conversion is reissued before it too
        for p in f.pays:
            if p[5] is not None and p[0] >= CUT and f.pays[p[5]][0] < CUT:
                p[0] = max(check_run(CUT - 3.0), f.pays[p[5]][4] + 0.05)


def quarter_end_wires(rng, feats):
    """Settlements wired late on a quarter's last business day (after the bank's 15:00 cutoff) value-date to the
    next business day: on each such day from December 2025, one wire released in the afternoon rush."""
    for d in (dt.date(2025, 12, 31), dt.date(2026, 3, 31), dt.date(2026, 6, 30), dt.date(2026, 9, 30)):
        day0 = _day_of(d)
        same = [(f, p) for f in feats for p in f.pays if p[2] == "WIRE" and day0 <= p[0] < day0 + 1
                and all(c[0] > day0 + 1 for c in f.closings)]
        if not same:
            near = sorted(((abs(p[0] - day0 - 0.5), f, p) for f in feats for p in f.pays
                           if p[2] == "WIRE" and day0 - 3 <= p[0] < day0 and all(c[0] > day0 + 1 for c in f.closings)),
                          key=lambda x: x[0])
            same = [(f, p) for _, f, p in near[:1]]
        for f, p in same[:2]:
            p[0] = day0 + (15.0 + rng.uniform(0.4, 1.9)) / 24.0


def year_end_returns(rng, feats):
    """Checks mailed in December 2026 and returned undeliverable are voided in the first week of January 2027 and
    reissued once a new address is found (after the extracts ran)."""
    lo, hi = _day_of(dt.date(2026, 12, 1)), _day_of(dt.date(2026, 12, 24))
    for f in feats:
        for p in f.pays:
            if p[2] == "CHECK" and p[4] is None and lo <= p[0] < hi and rng.random() < 0.06:
                p[4] = office_time(rng, _day_of(dt.date(2027, 1, 4)) + rng.uniform(0, 1.6))


def pay_on_duplicates(rng, feats, dups):
    """A settlement issued on the duplicate feature of a single-claimant platform claim before the duplicate was
    closed: the payment stays on the duplicate's record."""
    real = {}
    for f in feats:
        real.setdefault(f.occ, []).append(f)
    for d in dups:
        f = d.dup_of
        if len(real[f.occ]) != 1 or f.outcome != "settled":
            continue
        if rng.random() >= 0.5:
            continue
        settle = [k for k, p in enumerate(f.pays) if p[5] is None and p[4] is None and p[0] >= d.created
                  and ((p[0] < CUT - 30) if d.created < CUT else (p[0] >= LIVE))]
        if settle:
            f.paid_on = (d, settle[0])
            d.closings[0][0] = office_time(rng, max(d.closings[0][0], f.pays[settle[0]][0] + 2.0))


def build_world(seed=K.SEED):
    rng = np.random.default_rng(seed + 1)
    feats = simulate(seed)
    tidy_cutover(feats)
    keep_quarter_ends_clear(rng, feats)
    legacy_voids_stay_legacy(feats)
    quarter_end_wires(rng, feats)
    year_end_returns(rng, feats)
    dups = duplicates(rng, feats)
    pay_on_duplicates(rng, feats, dups)
    return assign_systems(rng, feats + dups)
