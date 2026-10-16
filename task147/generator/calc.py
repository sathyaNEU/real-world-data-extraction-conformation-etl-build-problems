"""Every figure the write-up and the goldens state, computed from the shipped pack alone (the files under target/), and
the rivals, constructions and ask stops checks.py asserts.

The block week: each 2027 roster week's forecast room-nights above the crew's 380 a night (HK-04 3.2), forecast on the
book of the extract (06:12 on Thursday 1 July 2027). The golden simulates the bookings still to come on the booking
process's own unit, the stay: each past season's post-confirmation bookings (made after its own confirmation morning,
HK-04 4.2, aligned on the festival's opening) are replayed whole, in booking order, against this year's book, each taken
only if every night of it has a room. The book itself is realised at each night's past rate; on the two nights already
full (Friday 13 and Saturday 14 August 2027) the only rooms a later stay can find are those the nights' own bookings will
release, at each rate code's past release rate. The five seasons are the replicates; the forecast is their mean."""
from __future__ import annotations

import datetime as dt
import json
import os
import re

import numpy as np
import pandas as pd

import common as K
import records as R

CAP, CREW = K.CAP, K.CREW
Y27 = K.YEAR
HIST = K.HIST_YEARS
NIGHTS = K.season_nights(Y27)
WEEKS = K.roster_weeks(Y27)
WEEK_NAMES = ["Monday %d to Sunday %d %s" % (m.day, s.day, "August" if s.month == 8 else "July")
              if m.month == s.month else "Monday %d %s to Sunday %d %s" % (m.day, m.strftime("%B"), s.day,
                                                                               s.strftime("%B"))
              for m, s in WEEKS]
D0 = np.datetime64("2021-01-01")


def di64(s):
    return ((pd.to_datetime(s).values.astype("datetime64[D]") - D0).astype(int))


def cut_utc(y):
    """The comparable point in year y: 06:12:44 on the Thursday five weeks before the opening night (HK-04 4.2),
    as a UTC numpy datetime."""
    loc = dt.datetime.combine(K.confirmation_day(y), K.EXTRACT_LOCAL.time())
    return np.datetime64(K.local_to_utc(loc))


def aligned(y, n27):
    """The night of year y at the same position from the festival's first Friday as 2027's night n27."""
    return K.fest_open(y) + (n27 - K.fest_open(Y27))


class Pack:
    pass


def from_pack(target):
    """Read the reservation extract and its amendment log into arrays."""
    V = Pack()
    V.target = target
    E = pd.read_csv(os.path.join(target, R.F_EXTRACT), dtype={"confirmation_no": np.int64, "booking_ref": str,
                                                                "rate_code": str, "status": str,
                                                                "group_code": str, "country": str},
                    keep_default_na=False, na_values={"cancelled_utc": [""]})
    V.n = len(E)
    V.conf = E["confirmation_no"].values
    V.created = pd.to_datetime(E["created_utc"]).values
    V.cancelled = pd.to_datetime(E["cancelled_utc"]).values
    V.arr = di64(E["arrival"])
    V.dep = di64(E["departure"])
    V.status = E["status"].values
    V.rate = E["rate_code"].values
    V.ref = E["booking_ref"].values
    V.stayed = np.isin(V.status, ["OUT", "INH"])
    V.overnight = V.dep > V.arr
    A = pd.read_csv(os.path.join(target, R.F_AMEND), dtype=str, keep_default_na=False)
    A = A[A["field"].isin(["ARRIVAL", "DEPARTURE"])].copy()
    A["t"] = pd.to_datetime(A["changed_utc"]).values
    A["conf"] = A["confirmation_no"].astype(np.int64)
    A["old"] = di64(A["old_value"])
    A = A.sort_values(["t", "conf", "field"], kind="mergesort")
    V.amend = A
    V.pos = {int(c): i for i, c in enumerate(V.conf)}
    return V


def dates_at(V, t):
    """Each reservation's arrival and departure as they stood at time t (later amendments undone)."""
    arr, dep = V.arr.copy(), V.dep.copy()
    later = V.amend[V.amend["t"] > t]
    first = later.drop_duplicates(["conf", "field"], keep="first")
    for c, f, o in zip(first["conf"].values, first["field"].values, first["old"].values):
        i = V.pos.get(int(c))
        if i is None:
            continue
        if f == "ARRIVAL":
            arr[i] = o
        else:
            dep[i] = o
    return arr, dep


def _cover(lo, hi, mask, n0, L, w=None):
    """Rooms on each night n0..n0+L-1 from the rows in mask covering [lo, hi)."""
    lo, hi = lo[mask], hi[mask]
    a = np.clip(lo - n0, 0, L)
    b = np.clip(hi - n0, 0, L)
    keep = b > a
    diff = np.zeros(L + 1)
    np.add.at(diff, a[keep], 1 if w is None else w[mask][keep])
    np.add.at(diff, b[keep], -1 if w is None else -w[mask][keep])
    return np.cumsum(diff)[:L]


def night_stats(V, t, n0, L, full=()):
    """For nights n0..n0+L-1 (day indices) and a cut t: the book at t (by its dates at t), the final occupied rooms,
    the book's rooms that stayed on the night, the rooms of stays booked after t, and of those the rooms of stays that
    ran through any night in full."""
    arr_t, dep_t = dates_at(V, t)
    alive = (V.created < t) & ((V.status != "CXL") | (V.cancelled > t)) & (dep_t > arr_t)
    book = _cover(arr_t, dep_t, alive, n0, L)
    final = _cover(V.arr, V.dep, V.stayed & V.overnight, n0, L)
    lo = np.maximum(arr_t, V.arr)
    hi = np.minimum(dep_t, V.dep)
    real = _cover(lo, hi, alive & V.stayed & V.overnight, n0, L)
    post = (V.created >= t) & V.stayed & V.overnight
    new = _cover(V.arr, V.dep, post, n0, L)
    thru_m = np.zeros(V.n, dtype=bool)
    for f in full:
        thru_m |= (V.arr <= f) & (V.dep > f)
    thru = _cover(V.arr, V.dep, post & thru_m, n0, L)
    return dict(book=book, final=final, real=real, new=new, thru=thru)


def wk(v):
    v = np.asarray(v, dtype=float)
    return [float(np.maximum(0.0, v[7 * w:7 * w + 7] - CREW).sum()) for w in range(5)]


def top(v):
    o = sorted(range(5), key=lambda i: (-v[i], i))
    return o[0], o[1], v[o[0]] / max(v[o[1]], 1e-9)


def history(V, years=HIST, cut=cut_utc, full_offsets=(7, 8)):
    """Each past season's tables on the nights aligned with 2027's, at that year's comparable point."""
    H = {}
    for y in years:
        n0 = K.di(aligned(y, NIGHTS[0]))
        fo = K.di(K.fest_open(y))
        H[y] = night_stats(V, cut(y), n0, len(NIGHTS), full=[fo + k for k in full_offsets])
    return H


def book27(V, t=None):
    t = cut_utc(Y27) if t is None else t
    return night_stats(V, t, K.di(NIGHTS[0]), len(NIGHTS))["book"]


def full_nights(V):
    if "_full" not in V.__dict__:
        b = book27(V)
        V._full = [NIGHTS[i] for i in range(len(NIGHTS)) if b[i] >= CAP]
    return V._full


def event_noshow(V):
    """The event rate's no-show share in the reservation history (rooms)."""
    m = (V.rate == "EVT") & np.isin(V.status, ["OUT", "NS"])
    return float((V.status[m] == "NS").sum()) / float(m.sum())


def event_fridays(target, full_only=False, V=None):
    """The Fridays of the past event weekends in the sales office's diary (sport, concerts, conferences); with
    full_only, those whose Friday and Saturday were full on the book 36 days before the Friday."""
    out = []
    for e in diary_events(target):
        if e["cat"] not in ("Sport", "Concert", "Conference"):
            continue
        d = e["frm"]
        while d.weekday() != 4:
            d -= dt.timedelta(days=1)
        if d.year < Y27:
            out.append(d)
    out = sorted(set(out))
    if full_only:
        keep = []
        for fri in out:
            S = night_stats(V, event_cut(fri), K.di(fri), 2)
            if S["book"][0] >= CAP and S["book"][1] >= CAP:
                keep.append(fri)
        out = keep
    return out


def event_cut(fri):
    return np.datetime64(K.local_to_utc(dt.datetime.combine(fri - dt.timedelta(days=36), K.EXTRACT_LOCAL.time())))


def _release_counts(V, cases, codes=None, exclude=None):
    """Rooms on each case's nights' book at its cut, and how many of them their bookings later cancelled, by code."""
    num, den = {}, {}
    for t, nights in cases:
        a, d = dates_at(V, t)
        al = (V.created < t) & ((V.status != "CXL") | (V.cancelled > t)) & (d > a)
        for f in nights:
            m = al & (a <= f) & (d > f)
            if codes is not None:
                m &= np.isin(V.rate, codes)
            if exclude is not None:
                m &= ~np.isin(V.rate, exclude)
            for rc in np.unique(V.rate[m]):
                mm = m & (V.rate == rc)
                den[rc] = den.get(rc, 0) + int(mm.sum())
                num[rc] = num.get(rc, 0) + int((mm & (V.status == "CXL")).sum())
    return num, den


def release_rates(V, skip_event=None):
    cache = V.__dict__.setdefault("_rel", {})
    if skip_event not in cache:
        cache[skip_event] = _release_rates(V, skip_event)
    return cache[skip_event]


def _release_rates(V, skip_event=None):
    """Each rate code's release rate: the share of the rooms on a night's book at the cut that their bookings later
    cancelled. The event rate from the past event weekends (the book 36 days before the Friday, the Friday and
    Saturday); every other code from the aligned festival Friday and Saturday at each past season's comparable
    point. skip_event leaves one event weekend out (the out-of-sample test)."""
    cases = [(cut_utc(y), (K.di(K.fest_open(y)) + 7, K.di(K.fest_open(y)) + 8)) for y in HIST]
    num, den = _release_counts(V, cases, exclude=["EVT"])
    ev = [(event_cut(f), (K.di(f), K.di(f) + 1)) for f in event_fridays(V.target) if f != skip_event]
    n2, d2 = _release_counts(V, ev, codes=["EVT"])
    num.update(n2)
    den.update(d2)
    pooled = sum(num.get(k, 0) for k in den if k != "EVT") / max(1, sum(v for k, v in den.items() if k != "EVT"))
    return {k: num.get(k, 0) / den[k] for k in den if den[k]}, pooled


def night_release(V, t, nights, rates, pooled):
    """Rooms each night's book at t is expected to release later: its rooms at their codes' release rates."""
    a, d = dates_at(V, t)
    al = (V.created < t) & ((V.status != "CXL") | (V.cancelled > t)) & (d > a)
    out = []
    for f in nights:
        m = al & (a <= f) & (d > f)
        out.append(float(sum(rates.get(rc, pooled) * int((m & (V.rate == rc)).sum()) for rc in np.unique(V.rate[m]))))
    return out


def replay_season(V, start, y, cut=cut_utc, target_year=Y27):
    """One past season's post-confirmation bookings replayed, whole and in booking order, against a book: each is
    taken only if every night of it has a room for all of its rooms. Returns the rooms taken on each 2027 season
    night."""
    t = cut(y)
    shift = K.di(K.fest_open(target_year)) - K.di(K.fest_open(y))
    n0 = K.di(NIGHTS[0])
    L = len(NIGHTS)
    post = (V.created >= t) & V.stayed & V.overnight
    lo, hi = K.di(aligned(y, NIGHTS[0])) - 21, K.di(aligned(y, NIGHTS[-1])) + 21
    idx = np.where(post & (V.dep > lo) & (V.arr <= hi))[0]
    order = sorted(idx, key=lambda i: (V.created[i], V.conf[i]))
    groups = {}
    for i in order:
        groups.setdefault(V.ref[i], []).append(i)
    booked = np.zeros(L + 60)
    booked[30:30 + L] = start
    seen = set()
    for i in order:
        ref = V.ref[i]
        if ref in seen:
            continue
        seen.add(ref)
        rows = groups[ref]
        a = max(0, int(V.arr[rows[0]]) + shift - n0 + 30)
        d = min(L + 60, int(V.dep[rows[0]]) + shift - n0 + 30)
        if a < d and np.all(booked[a:d] + len(rows) <= CAP):
            booked[a:d] += len(rows)
    return booked[30:30 + L] - start


def event_realisation(V):
    """The event rate's share of its rooms on the book 36 days before a past event weekend that stayed on the event
    nights."""
    if "_evt_real" not in V.__dict__:
        on = stay = 0
        for fri in event_fridays(V.target):
            t = event_cut(fri)
            a, d = dates_at(V, t)
            al = (V.created < t) & ((V.status != "CXL") | (V.cancelled > t)) & (d > a) & (V.rate == "EVT")
            for f in (K.di(fri), K.di(fri) + 1):
                m = al & (a <= f) & (d > f)
                on += int(m.sum())
                stay += int((m & V.stayed & (V.arr <= f) & (V.dep > f)).sum())
        V._evt_real = stay / on
    return V._evt_real


def book27_by_code(V, t=None):
    """The 2027 book at t split into the event rate's rooms and every other room."""
    t = cut_utc(Y27) if t is None else t
    a, d = dates_at(V, t)
    al = (V.created < t) & ((V.status != "CXL") | (V.cancelled > t)) & (d > a)
    n0, L = K.di(NIGHTS[0]), len(NIGHTS)
    return _cover(a, d, al & (V.rate != "EVT"), n0, L), _cover(a, d, al & (V.rate == "EVT"), n0, L)


def golden(V, years=HIST, cut=cut_utc, t27=None, H=None, start="realised", freed=None, full_occ=None,
           real_mode="code"):
    """The forecast by stay: each past season's later bookings replayed whole against this year's book (the book
    realised by rate code, each night's other rooms at that night's past rate and the event rate's rooms at the event
    rate's own; on the full nights only the rooms their own bookings will release), the five seasons' mean; the full
    nights at 480 less the event rate's no-shows."""
    H = H or history(V, years, cut)
    t27 = cut_utc(Y27) if t27 is None else t27
    b = book27(V, t27)
    b_o, b_e = book27_by_code(V, t27)
    fi = [i for i, n in enumerate(NIGHTS) if n in full_nights(V)]
    real = np.sum([H[y]["real"] for y in years], axis=0) / np.sum([H[y]["book"] for y in years], axis=0)
    breal = b_o * real + b_e * event_realisation(V) if real_mode == "code" else b * real
    new = np.mean([H[y]["new"] for y in years], axis=0)
    thru = np.mean([H[y]["thru"] for y in years], axis=0)
    if freed is None:
        rates, pooled = release_rates(V)
        freed = night_release(V, t27, [K.di(NIGHTS[i]) for i in fi], rates, pooled)
    st = breal.copy() if start == "realised" else b.copy()
    for i, fr in zip(fi, freed):
        st[i] = CAP - fr
    adds = [replay_season(V, st, y, cut) for y in years]
    g = breal + np.mean(adds, axis=0)
    g[fi] = CAP * (1.0 - event_noshow(V)) if full_occ is None else full_occ
    return np.minimum(CAP, g), dict(book=b, real=real, breal=breal, new=new, thru=thru, fi=fi, freed=list(freed),
                                    adds=adds)


def filtered(V, years=HIST, cut=cut_utc, t27=None, H=None):
    """The replay's expectation with no capacity check off the full nights and no resale: the book realised by rate
    code, plus the past seasons' later stays, less those through the aligned full nights."""
    H = H or history(V, years, cut)
    b_o, b_e = book27_by_code(V, t27)
    fi = [i for i, n in enumerate(NIGHTS) if n in full_nights(V)]
    real = np.sum([H[y]["real"] for y in years], axis=0) / np.sum([H[y]["book"] for y in years], axis=0)
    g = b_o * real + b_e * event_realisation(V) + np.mean([H[y]["new"] - H[y]["thru"] for y in years], axis=0)
    g[fi] = CAP * (1.0 - event_noshow(V))
    return np.minimum(CAP, g)


def rivals(V, H=None):
    """The night-level forecasts a strong analyst reaches first, and the partial stay-level one."""
    H = H or history(V)
    b = book27(V)
    Y = HIST
    out = {}
    out["R0 seasonal average of the past finals"] = wk(np.mean([H[y]["final"] for y in Y], axis=0))
    pick = np.mean([H[y]["final"] - H[y]["book"] for y in Y], axis=0)
    out["R1 book plus average pickup (default)"] = wk(np.minimum(CAP, b + pick))
    ratio = np.sum([H[y]["final"] for y in Y], axis=0) / np.sum([H[y]["book"] for y in Y], axis=0)
    out["R1m book times final-to-book ratio"] = wk(np.minimum(CAP, b * ratio))
    real = np.sum([H[y]["real"] for y in Y], axis=0) / np.sum([H[y]["book"] for y in Y], axis=0)
    newm = np.mean([H[y]["new"] for y in Y], axis=0)
    out["R1t book realised plus later bookings"] = wk(np.minimum(CAP, b * real + newm))
    out["R1L last year's pickup"] = wk(np.minimum(CAP, b + H[2026]["final"] - H[2026]["book"]))
    # regressions of final on book: one pooled slope with weekday effects, and one effect per night
    X, yv, wdays, idx = [], [], [], []
    for y in Y:
        for i in range(len(NIGHTS)):
            X.append(H[y]["book"][i])
            yv.append(H[y]["final"][i])
            wdays.append(NIGHTS[i].weekday())
            idx.append(i)
    X, yv, wdays, idx = map(np.array, (X, yv, wdays, idx))
    D = np.column_stack([X] + [(wdays == k).astype(float) for k in range(7)])
    beta = np.linalg.lstsq(D, yv, rcond=None)[0]
    Dn = np.column_stack([b] + [np.array([n.weekday() == k for n in NIGHTS], dtype=float) for k in range(7)])
    out["R1r final on book, weekday effects"] = wk(np.minimum(CAP, Dn @ beta))
    xm = np.array([X[idx == i].mean() for i in range(len(NIGHTS))])
    ym = np.array([yv[idx == i].mean() for i in range(len(NIGHTS))])
    xd, yd = X - xm[idx], yv - ym[idx]
    slope = float((xd * yd).sum() / (xd * xd).sum())
    out["R1rf final on book, an effect per night"] = wk(np.minimum(CAP, ym + slope * (b - xm)))
    # the book realised by rate plan (the event rate's rooms kept), plus the later bookings
    out["R2 book realised by rate plan"] = wk(np.minimum(CAP, plan_realised(V) + newm))
    # the full nights' stays taken out of the concert week only
    g, parts = golden(V, H=H)
    part = b * real + newm
    w3 = range(14, 21)
    for i in w3:
        part[i] = g[i]
    out["R2b stays through the full nights out of the concert week only"] = wk(np.minimum(CAP, part))
    return out


def plan_realised(V):
    """The 2027 book realised at each rate plan's past rate on the aligned night (pooled over the five years)."""
    t27 = cut_utc(Y27)
    n27 = K.di(NIGHTS[0])
    L = len(NIGHTS)
    plans = ["EVT", "OTHER"]
    pl = np.where(V.rate == "EVT", "EVT", "OTHER")
    arr_t, dep_t = dates_at(V, t27)
    out = np.zeros(L)
    num = {p: np.zeros(L) for p in plans}
    den = {p: np.zeros(L) for p in plans}
    for y in HIST:
        t = cut_utc(y)
        a_t, d_t = dates_at(V, t)
        alive = (V.created < t) & ((V.status != "CXL") | (V.cancelled > t)) & (d_t > a_t)
        n0 = K.di(aligned(y, NIGHTS[0]))
        for p in plans:
            m = alive & (pl == p)
            den[p] += _cover(a_t, d_t, m, n0, L)
            num[p] += _cover(np.maximum(a_t, V.arr), np.minimum(d_t, V.dep), m & V.stayed & V.overnight, n0, L)
    alive27 = (V.created < t27) & ((V.status != "CXL") | (V.cancelled > t27)) & (dep_t > arr_t)
    for p in plans:
        bk = _cover(arr_t, dep_t, alive27 & (pl == p), n27, L)
        rate = np.where(den[p] > 0, num[p] / np.maximum(den[p], 1), 0.97 if p == "EVT" else 0.9)
        if p == "EVT":
            m = (V.rate == "EVT") & np.isin(V.status, ["OUT", "NS"])
            rate = np.full(L, 1.0 - float((V.status[m] == "NS").sum()) / float(m.sum()))
        out += bk * rate
    return out


def pooled_release(V, share="cancelled"):
    """The pooled share of the aligned festival Friday and Saturday's book at the comparable point that did not stay
    (share="not stayed", no-shows included) or was cancelled (share="cancelled"), every code together."""
    num = den = 0
    for y in HIST:
        t = cut_utc(y)
        a, d = dates_at(V, t)
        al = (V.created < t) & ((V.status != "CXL") | (V.cancelled > t)) & (d > a)
        fo = K.di(K.fest_open(y))
        for f in (fo + 7, fo + 8):
            m = al & (a <= f) & (d > f)
            den += int(m.sum())
            if share == "cancelled":
                num += int((m & (V.status == "CXL")).sum())
            else:
                num += int((m & ~(V.stayed & (V.arr <= f) & (V.dep > f))).sum())
    return num / den


def constructions(V):
    """Every defensible construction of the stay-level forecast, each week's figure; the rivals the data rejects are
    keyed 'rival:'."""
    H = history(V)
    out = {}
    g, parts = golden(V, H=H)
    out["golden: all five seasons replayed"] = wk(g)
    for y in HIST:
        ys = [x for x in HIST if x != y]
        out["leave out %d" % y] = wk(golden(V, years=ys)[0])
    out["last three seasons"] = wk(golden(V, years=[2024, 2025, 2026])[0])
    out["last two seasons"] = wk(golden(V, years=[2025, 2026])[0])
    mid = lambda y: np.datetime64(K.local_to_utc(dt.datetime.combine(K.confirmation_day(y), dt.time(0, 0))))
    out["books at midnight"] = wk(golden(V, cut=mid, t27=mid(Y27))[0])
    jul1 = lambda y: np.datetime64(K.local_to_utc(dt.datetime(y, 7, 1, 6, 12, 44)))
    out["past books on 1 July"] = wk(golden(V, cut=jul1)[0])
    out["no resale on the full nights"] = wk(golden(V, H=H, freed=[0.0] * len(parts["fi"]))[0])
    out["full nights at 480"] = wk(golden(V, H=H, full_occ=CAP)[0])
    pc = pooled_release(V, "cancelled")
    out["full nights' releases at the pooled cancellation share"] = wk(golden(
        V, H=H, freed=[CAP * pc] * len(parts["fi"]))[0])
    out["the filter: later stays less those through the full nights, no capacity check"] = wk(filtered(V, H=H))
    b = book27(V)
    pick = np.mean([H[y]["final"] - H[y]["book"] for y in HIST], axis=0)
    add = b + pick - parts["thru"]
    add[parts["fi"]] = CAP * (1.0 - event_noshow(V))
    out["additive: book plus pickup less the blocked stays"] = wk(np.minimum(CAP, add))
    out["book realised at each night's pooled past rate, every code together"] = wk(golden(
        V, H=H, real_mode="pooled")[0])
    out["rival: replay against the 2027 book as it stands"] = wk(golden(V, H=H, start="raw")[0])
    pn = pooled_release(V, "not stayed")
    out["rival: full nights' releases at the pooled share that did not stay"] = wk(golden(
        V, H=H, freed=[CAP * pn] * len(parts["fi"]))[0])
    return out


def precision(V):
    """The golden's standard error per week from the five seasons' spread (each season's replay one replicate)."""
    H = history(V)
    g, parts = golden(V, H=H)
    breal, fi = parts["breal"], parts["fi"]
    per = []
    for a in parts["adds"]:
        gy = breal + a
        gy[fi] = CAP * (1.0 - event_noshow(V))
        per.append(wk(np.minimum(CAP, gy)))
    per = np.array(per)
    return list(per.std(axis=0, ddof=1) / np.sqrt(len(HIST)))


def release_backtest(V):
    """Out of sample on the past event weekends full five weeks out: the rooms their full Friday and Saturday
    released after the cut, against each night's book at its codes' release rates (the event rate from the other
    event weekends) and against the pooled festival shares."""
    fris = event_fridays(V.target, full_only=True, V=V)
    pc, pn = pooled_release(V, "cancelled"), pooled_release(V, "not stayed")
    act = byc = 0.0
    nights = 0
    for fri in fris:
        rates, pooled = release_rates(V, skip_event=fri)
        t0 = event_cut(fri)
        a, d = dates_at(V, t0)
        al = (V.created < t0) & ((V.status != "CXL") | (V.cancelled > t0)) & (d > a)
        for f, r in zip((K.di(fri), K.di(fri) + 1), night_release(V, t0, (K.di(fri), K.di(fri) + 1), rates, pooled)):
            m = al & (a <= f) & (d > f)
            act += int((m & (V.status == "CXL")).sum())
            byc += r
            nights += 1
    return dict(events=len(fris), nights=nights, actual=act, by_code=byc, pooled_cancelled=CAP * pc * nights,
                pooled_not_stayed=CAP * pn * nights, pc=pc, pn=pn)


# ---------------------------------------------------------------------------------------------------- back-test
def diary_events(target):
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, R.F_DIARY), read_only=True)
    ws = wb["Diary"]
    out = []
    for row in ws.iter_rows(min_row=5, values_only=True):
        if row[0] is None:
            continue
        out.append(dict(frm=row[0].date(), to=row[1].date(), event=row[2], venue=row[3], cat=row[4]))
    return out


def backtest(V, target):
    """The past event weekends whose Friday and Saturday were full five weeks out: each week's other nights forecast
    at the Thursday five weeks before the Friday (night-level pickup from comparable weekends without an event, and the
    same less the comparable weekends' stays through their Friday and Saturday), against the finals; and how much of
    the comparable weekends' through-stays came back on the other nights as stays that miss the full nights."""
    evs = [e for e in diary_events(target) if e["cat"] in ("Sport", "Concert", "Conference")]
    fris = []
    for e in evs:
        d = e["frm"]
        while d.weekday() != 4:
            d -= dt.timedelta(days=1)
        if d.year < Y27:
            fris.append(d)
    fris = sorted(set(fris))
    rows = []
    for fri in fris:
        t0 = np.datetime64(K.local_to_utc(dt.datetime.combine(fri - dt.timedelta(days=36), K.EXTRACT_LOCAL.time())))
        n0 = K.di(fri) - 4
        S = night_stats(V, t0, n0, 9, full=[K.di(fri), K.di(fri) + 1])
        if not (S["book"][4] >= CAP and S["book"][5] >= CAP):
            continue
        adj = [0, 1, 2, 3, 6, 7, 8]
        refp, reft, refn, nref = np.zeros(9), np.zeros(9), np.zeros(9), 0
        for yy in HIST:
            if yy == fri.year:
                continue
            cand = dt.date(yy, fri.month, min(fri.day, 28))
            while cand.weekday() != 4:
                cand += dt.timedelta(days=1)
            if any(abs((f - cand).days) < 10 for f in fris) or \
                    K.fest_open(yy) - dt.timedelta(days=12) <= cand <= K.fest_open(yy) + dt.timedelta(days=26):
                continue
            t2 = np.datetime64(K.local_to_utc(dt.datetime.combine(cand - dt.timedelta(days=36),
                                                                  K.EXTRACT_LOCAL.time())))
            S2 = night_stats(V, t2, K.di(cand) - 4, 9, full=[K.di(cand), K.di(cand) + 1])
            refp += S2["final"] - S2["book"]
            reft += S2["thru"]
            refn += S2["new"] - S2["thru"]
            nref += 1
        refp /= nref
        reft /= nref
        refn /= nref
        for j in adj:
            fn = min(CAP, S["book"][j] + refp[j])
            fs = min(CAP, S["book"][j] + refp[j] - reft[j])
            rows.append((fri, j, fn - S["final"][j], fs - S["final"][j], reft[j],
                         (S["new"][j] - S["thru"][j]) - refn[j]))
    en = np.array([r[2] for r in rows])
    es = np.array([r[3] for r in rows])
    se = en.std(ddof=1) / np.sqrt(len(en))
    through = float(np.mean([r[4] for r in rows]))
    shorter = float(np.mean([r[5] for r in rows]))
    return dict(events=len({r[0] for r in rows}), nights=len(rows), night_bias=float(en.mean()),
                night_t=float(en.mean() / se), night_mae=float(np.abs(en).mean()), stay_bias=float(es.mean()),
                stay_mae=float(np.abs(es).mean()),
                stay_t=float(es.mean() / (es.std(ddof=1) / np.sqrt(len(es)))), through=through,
                shorter=shorter, recovered_share=shorter / through)


def august_backtest(V):
    """The night-level default's own back-test on the past Augusts at their comparable points (no night full):
    each season forecast from the other four years' pickup, against its finals, by week."""
    H = history(V)
    out = []
    for y in HIST:
        others = [x for x in HIST if x != y]
        pick = np.mean([H[x]["final"] - H[x]["book"] for x in others], axis=0)
        f = np.minimum(CAP, H[y]["book"] + pick)
        out.append(float(np.mean(f - H[y]["final"])))
    return out


# ---------------------------------------------------------------------------------------------------- the main call
def ladder(V):
    H = history(V)
    g, parts = golden(V, H=H)
    gw = wk(g)
    w1, w2, m = top(gw)
    rv = rivals(V, H)
    return dict(H=H, g=g, gw=gw, parts=parts, pick=w1, runner=w2, margin=m, rivals=rv,
                default=rv["R1 book plus average pickup (default)"], full=full_nights(V))


def components(V, L):
    """The critical components: the concert nights full on the book; the past post-confirmation stays through the
    aligned Friday and Saturday on the concert week's other nights (room-nights a season); the concert week's and the
    block week's forecasts."""
    H = L["H"]
    w3 = range(14, 21)
    fi = L["parts"]["fi"]
    thru_w3 = float(np.mean([sum(H[y]["thru"][i] for i in w3 if i not in fi) for y in HIST]))
    thru_w4 = float(np.mean([sum(H[y]["thru"][i] for i in range(21, 28)) for y in HIST]))
    b = L["parts"]["book"]
    return dict(full=L["full"], book_full=[int(b[i]) for i in fi], thru_w3=thru_w3, thru_w4=thru_w4,
                gw=L["gw"], default=L["default"], freed=L["parts"]["freed"])


# ---------------------------------------------------------------------------------------------------- Ask A
TASKS_F = "hk_task_log_2026-07-27_2026-08-30.csv"
USERS_F = "hk_app_users_2027-06-28.csv"
HR_F = "hr_housekeeping_staff_2027-06-28.xlsx"
TS_F = "brennock_timesheets_weighhouse_summer_2026.xlsx"
PAY_F = "payroll_overtime_lines_2026-P14-P19.csv"
ACCESS_F = "staff_access_events_2026-08.csv"
BADGE_F = "reception_day_badge_log_2026-08.csv"
WEEKS26 = K.roster_weeks(2026)


def timesheets(target):
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, TS_F), read_only=True)
    out = []
    for ws in wb.worksheets:
        for row in ws.iter_rows(min_row=5, values_only=True):
            if row[0] is None:
                continue
            out.append(dict(bhs=row[0], name=row[1], kind=row[2], date=row[3].date(), start=row[4], end=row[5],
                            brk=row[6], hours=row[7], approver=row[8], note=row[9]))
    return out


def week_of(d):
    for w, (m, s) in enumerate(WEEKS26):
        if m <= d <= s:
            return w
    return None


def ask_a(target, mode="golden"):
    """Each 2026 roster week's departure cleans and stayover services by the crew and by Brennock's temps, and the
    crew's overtime hours. mode selects a stop for checks.py: golden; current_group (the user list's group as it
    stands); login (the login's user, the notes unread); cracker (the login's current group, the notes unread, the
    overtime by pay period end); recleans (re-cleans counted); created2026 (every login created in 2026 counted as
    Brennock's); paid (the overtime by pay period end, the services as golden)."""
    T = pd.read_csv(os.path.join(target, TASKS_F), dtype=str, keep_default_na=False)
    U = pd.read_csv(os.path.join(target, USERS_F), dtype=str, keep_default_na=False)
    users = {r.login: r for r in U.itertuples()}
    ts = timesheets(target)
    brn_on = {(r["name"], r["date"]) for r in ts}
    brn_names = {r["name"] for r in ts}
    firsts = {}
    for r in U.itertuples():
        if r.login.startswith("block"):
            continue
        f = r.display_name.split(" ")[0]
        firsts.setdefault(f, set()).add(r.display_name)
    for n in brn_names:
        firsts.setdefault(n.split(" ")[0], set()).add(n)
    paid = mode in ("paid", "cracker")
    mode = "golden" if mode == "paid" else mode
    keep = T["task_type"].isin(["Departure", "Stayover"]) & (T["status"] == "Completed")
    if mode == "recleans":
        keep = T["task_type"].isin(["Departure", "Stayover", "Re-clean"]) & (T["status"] == "Completed")
    par = {r.task_id: r.task_type for r in T.itertuples()}
    out = {w: dict(crew_dep=0, crew_stay=0, brn_dep=0, brn_stay=0, ot=0.0) for w in range(5)}
    for r in T[keep].itertuples():
        d = dt.date.fromisoformat(r.service_date)
        w = week_of(d)
        if w is None:
            continue
        u = users[r.user_login]
        person = u.display_name
        if mode in ("golden", "current_group", "created2026", "recleans") and \
                u.user_group == "Housekeeping Supervisors" and r.note:
            hits = [f for f in firsts if re.search(r"\b%s\b" % re.escape(f), r.note)]
            assert len(hits) == 1, r.note
            names = firsts[hits[0]]
            assert len(names) == 1
            person = list(names)[0]
        if mode in ("golden", "recleans"):
            brn = (u.user_group == "Agency - Brennock" and person == u.display_name) or (person, d) in brn_on
        elif mode in ("current_group", "login", "cracker"):
            pu = [x for x in users.values() if x.display_name == person]
            grp = pu[0].user_group if pu else ("Agency - Brennock" if person in brn_names else "")
            brn = grp == "Agency - Brennock"
        elif mode == "created2026":
            pu = [x for x in users.values() if x.display_name == person]
            brn = (pu and pu[0].created >= "2026-01-01" and pu[0].created < "2027-01-01") or \
                (not pu and person in brn_names)
        else:
            raise ValueError(mode)
        ttype = r.task_type if r.task_type != "Re-clean" else par[r.parent_task_id]
        side = "brn" if brn else "crew"
        out[w]["%s_%s" % (side, "dep" if ttype == "Departure" else "stay")] += 1
    P = pd.read_csv(os.path.join(target, PAY_F), dtype=str, keep_default_na=False)
    for r in P.itertuples():
        if paid:
            d = dt.date.fromisoformat(r.period_end)
        else:
            m = re.match(r"OT (\d\d)/(\d\d)/(\d\d) ([\d.]+)h$", r.reference)
            d = dt.date(2000 + int(m.group(3)), int(m.group(2)), int(m.group(1)))
            assert abs(float(m.group(4)) - float(r.hours)) < 1e-9
        w = week_of(d)
        if w is not None:
            out[w]["ot"] += float(r.hours)
    return out


# ---------------------------------------------------------------------------------------------------- Ask B
def ask_b(target, mode="golden"):
    """For each day of the 2026 block week, the hours Brennock may bill for the block under the framework agreement
    (4.1 to 4.3) and the charge before VAT (5.1). mode: golden; local (the loading bay's times read as local);
    nomin (4.3 not applied); nosunday (5.1's Sunday rate not applied); shifted (every access time moved an hour)."""
    ts = timesheets(target)
    block = [r for r in ts if r["kind"] == "Block"]
    days = sorted({r["date"] for r in block})
    Bg = pd.read_csv(os.path.join(target, BADGE_F), dtype=str, keep_default_na=False)
    badge = {(r.date, r.issued_to): r.badge for r in Bg.itertuples()}
    Ac = pd.read_csv(os.path.join(target, ACCESS_F), dtype=str, keep_default_na=False)
    ev = {}
    for r in Ac.itertuples():
        t = dt.datetime.fromisoformat(r.event_time)
        if r.reader == "LB-02" and mode not in ("local",):
            t = K.utc_to_local(t)
        if mode == "shifted":
            t = t + dt.timedelta(hours=1) if r.reader != "LB-02" else t
        ev.setdefault((t.date().isoformat(), r.badge), []).append((t, r.direction))
    out = {}
    for d in days:
        hrs = 0.0
        for r in [x for x in block if x["date"] == d]:
            b = badge[(d.isoformat(), r["name"])]
            e = sorted(ev[(d.isoformat(), b)])
            ins = [t for t, k in e if k == "IN"]
            outs = [t for t, k in e if k == "OUT"]
            bs = dt.datetime.combine(d, dt.time.fromisoformat(r["start"]))
            be = dt.datetime.combine(d, dt.time.fromisoformat(r["end"]))
            s = max(bs, min(ins))
            en = min(be, max(outs))
            mins = max(0.0, (en - s).total_seconds() / 60.0)
            h = np.floor(mins / 15.0 + 1e-9) / 4.0
            if h > 6.0:
                h -= 0.5
            if mode != "nomin" and ins:
                h = max(h, 4.0)
            hrs += h
        rate = 22.56 * (1.25 if (d.weekday() == 6 and mode != "nosunday") else 1.0)
        out[d] = (float(hrs), K.round_dp(hrs * rate, 2))
    return out


def week_charge(b):
    """The week's charge before VAT: each day's billable hours at its rate (framework agreement 5.1), to the cent."""
    tot = sum(h * 22.56 * (1.25 if d.weekday() == 6 else 1.0) for d, (h, _) in b.items())
    return K.round_dp(tot, 2)


def invoice_b(target):
    import pdfplumber
    pdf = pdfplumber.open(os.path.join(target, "brennock_invoice_BHS-INV-2026-0833.pdf"))
    text = "\n".join(p.extract_text() for p in pdf.pages)
    out = {}
    for m in re.finditer(r"\w{3} (\d\d)/(\d\d)/(\d{4}) (\d+) ([\d.]+) ([\d.]+) ([\d,]+\.\d\d)", text):
        d = dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        out[d] = (float(m.group(5)), float(m.group(7).replace(",", "")))
    return out
