"""The world before any file is written: every Larch driver account's weekly trips and online time from launch to
the end of March 2027, the guarantee windows' qualifiers, the payments system's runs, returns and recoveries, the
onboarding pipeline and the screening vendor's orders. Only records the operator's systems would hold are later
written out; the driver kinds below (regular, seasonal, bonus, tryer, occasional, rental) are the world's latent
truth and appear in no file.

Kinds:
  R regular     drives the year round at its own pace and stops for good at its own hazard (rarely in winter)
  W seasonal    a worker laid off for the winter: drives from a personal week each winter (relative to the guarantee's
                first Monday) to early April, then goes back to its trade; comes back the next winter or not
  B bonus       a 2026 campaign recruit who drove February and March for the installments and stopped in April
  N tryer       drives a few weeks and stops
  I occasional  on and off for years, a background of returns in every month
  F rental      a driver of the 2025 rental programme: February and March 2025 only
"""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as K

# ------------------------------------------------------------------------------------------------- parameters
BASE = {2021: 46, 2022: 52, 2023: 56, 2024: 60, 2025: 62, 2026: 63, 2027: 64}   # organic first-trip drivers a week
WINTER_UPLIFT = 1.2
MIX_WINTER = dict(W=0.22, R=0.43, N=0.28, I=0.07)     # first trip from November to February
MIX_OTHER = dict(R=0.572, N=0.338, I=0.09)
CAMPAIGN_N = 2215
CAMPAIGN_MIX = dict(W=0.675, B=0.17, R=0.10, N=0.055)
CAMPAIGN_WEEKS = [0.24, 0.22, 0.20, 0.19, 0.15]       # first trips over the five weeks from 2 February 2026
RENTAL_N = 352
# a seasonal driver's personal return week, relative to the guarantee's first Monday (week 0)
REL = list(range(-7, 6))
PROF = [0.07, 0.10, 0.13, 0.12, 0.03, 0.012, 0.006, 0.26, 0.14, 0.075, 0.035, 0.012, 0.0]
W_RET = ([0.80, 0.92, 0.97], [0.25, 0.45, 0.30])     # chance of coming back each winter, by driver
W_ACT = 0.88
R_HAZ = ([0.004, 0.012, 0.03], [0.45, 0.40, 0.15])
I_ON = 0.15                                           # occasional drivers' weekly chance of coming back on
R_WINTER = 0.12                                       # regular drivers' stopping hazard in December to February
TOPUP_LO, TOPUP_P = 34, 0.55                          # drivers within reach of 40 push to it during a window
WEEKDAY_W = np.array([0.11, 0.12, 0.13, 0.14, 0.18, 0.19, 0.13])
MONTH_SEAS = {1: 1.04, 2: 1.0, 3: 0.97, 4: 0.95, 5: 0.95, 6: 0.97, 7: 0.98, 8: 0.98, 9: 0.97, 10: 1.0, 11: 1.03, 12: 1.07}
DUP_PERSONS = {2025: 4, 2026: 7}                      # people who drove the window on two accounts, both paid
LATE_CREDIT = {2025: 17, 2026: 21}                    # drivers credited trips after the run's review cut
FRAUD = {2025: 9, 2026: 12}                           # payments recovered for trips refunded as fraudulent


class World:
    pass


def _deal(r, n):
    """Return weeks for one winter's n returning seasonal drivers: the trades' calendar (PROF) rounded to whole
    drivers by largest remainder, dealt in a shuffled order."""
    p = np.array(PROF, dtype=float)
    p = p / p.sum()
    raw = p * n
    cnt = np.floor(raw).astype(int)
    short = n - int(cnt.sum())
    if short > 0:
        order = np.argsort(-(raw - cnt), kind="stable")
        cnt[order[:short]] += 1
    deck = np.repeat(REL, cnt)
    r.shuffle(deck)
    return [int(x) for x in deck]


def _pick(r, mix):
    keys = list(mix)
    p = np.array([mix[k] for k in keys], dtype=float)
    return keys[int(r.choice(len(keys), p=p / p.sum()))]


def simulate():
    W = World()
    NW = K.NW
    week_dates = [K.wdate(i) for i in range(NW)]
    week_month = np.array([d.month for d in week_dates])
    seas = np.array([MONTH_SEAS[m] for m in week_month])

    # ---------------------------------------------------------------- entrants
    kinds, entry, src = [], [], []
    for i in range(K.widx(dt.date(2027, 3, 1))):
        d = week_dates[i]
        winter = d.month in (11, 12, 1, 2)
        lam = BASE[d.year] * (WINTER_UPLIFT if winter else 1.0)
        r = K.rng("entry", i)
        n = int(r.poisson(lam))
        mix = MIX_WINTER if winter else MIX_OTHER
        for _ in range(n):
            kinds.append(_pick(r, mix))
            entry.append(i)
            src.append("organic")
    r = K.rng("campaign")
    w0 = K.widx(K.CAMPAIGN_FIRST)
    for j in range(CAMPAIGN_N):
        kinds.append(_pick(r, CAMPAIGN_MIX))
        entry.append(w0 + int(r.choice(5, p=CAMPAIGN_WEEKS)))
        src.append("campaign")
    r = K.rng("rental")
    w1 = K.widx(K.RENTAL_FIRST)
    for j in range(RENTAL_N):
        kinds.append("F")
        entry.append(w1 + int(r.choice(2, p=[0.62, 0.38])))
        src.append("rental")
    kinds = np.array(kinds)
    entry = np.array(entry)
    src = np.array(src)
    n = len(kinds)

    trips = np.zeros((n, NW), dtype=np.int16)
    hours = np.zeros((n, NW), dtype=np.float32)
    tph = np.zeros(n)
    personal = np.full(n, -99)
    w_mean = np.zeros(n)
    w_pret = np.zeros(n)
    ret_years = {}                         # seasonal driver -> winters (by guarantee year) it came back for
    for k in range(n):
        t, e = kinds[k], int(entry[k])
        r = K.rng("drv", k)
        tph[k] = float(np.clip(r.normal(1.92, 0.24), 1.25, 2.75))
        if t == "R":
            mean = r.gamma(2.2, 6.6)
            act = r.beta(6, 2)
            haz = float(r.choice(R_HAZ[0], p=R_HAZ[1]))
            span = NW - e
            hz = np.where(np.isin(week_month[e:], (12, 1, 2)), haz * R_WINTER, haz)
            u = r.random(span)
            dead = np.where((u < hz) & (np.arange(span) > 2))[0]
            end = e + (int(dead[0]) if len(dead) else span)
            on = r.random(end - e) < act
            trips[k, e:end] = np.where(on, r.poisson(mean * seas[e:end]), 0)
        elif t == "W":
            mean = r.gamma(6.0, 4.0)
            w_mean[k] = mean
            w_pret[k] = float(r.choice(W_RET[0], p=W_RET[1]))
        elif t == "B":
            mean = r.gamma(4.0, 4.0)
            stop = K.widx(dt.date(2026, 4, 1)) + int(r.integers(-1, 3))
            on = r.random(stop - e) < 0.9
            trips[k, e:stop] = np.where(on, r.poisson(mean * seas[e:stop]), 0)
        elif t == "F":
            mean = r.gamma(8.0, 3.4)
            stop = K.widx(K.RENTAL_END) + 1
            on = r.random(stop - e) < 0.93
            trips[k, e:stop] = np.where(on, r.poisson(mean * seas[e:stop]), 0)
        elif t == "N":
            mean = r.gamma(2.0, 5.0)
            dur = 1 + int(r.geometric(0.15))
            b = min(e + dur, NW)
            on = r.random(b - e) < 0.75
            trips[k, e:b] = np.where(on, r.poisson(mean * seas[e:b]), 0)
        elif t == "I":
            mean = r.gamma(2.0, 5.0)
            state = r.random() < 0.5
            u1, u2, u3, u4 = r.random(NW), r.random(NW), r.random(NW), r.random(NW)
            pois = r.poisson(mean * seas)
            for i in range(e, NW):
                if state:
                    if u1[i] < 0.08:
                        state = False
                elif u1[i] < I_ON:
                    state = True
                if state and u2[i] < 0.8:
                    trips[k, i] = pois[i]
                if u3[i] < 0.002:
                    break
    _seasonal(kinds, entry, trips, seas, week_dates, personal, w_mean, w_pret, ret_years)
    for k in range(n):
        r = K.rng("hours", k)
        act_w = trips[k] > 0
        if act_w.any():
            noise = r.normal(1.0, 0.09, act_w.sum()).clip(0.7, 1.35)
            hours[k, act_w] = (trips[k, act_w] / tph[k]) * noise
    # a first trip is the first week with a trip; drivers whose spell produced no trip are dropped (never drove)
    has = trips > 0
    drove = has.any(1)
    W.kind = kinds[drove]
    W.entry = entry[drove]
    W.src = src[drove]
    W.trips = trips[drove]
    W.hours = hours[drove]
    W.tph = tph[drove]
    W.personal = personal[drove]
    old_to_new = np.cumsum(drove) - 1
    W.ret_years = {int(old_to_new[k]): v for k, v in ret_years.items() if drove[k]}
    W.n = int(drove.sum())
    W.has = W.trips > 0
    W.first_week = W.has.argmax(1)
    W.week_dates = week_dates
    W.week_month = week_month
    _qualify(W)
    return W


def _seasonal(kinds, entry, trips, seas, week_dates, personal, w_mean, w_pret, ret_years):
    """Each seasonal driver drives its first winter from its first trip to early April. Each later winter, every
    driver who drove the winter before comes back at its own chance or stops for good, and the winter's returning
    drivers come back on the trades' calendar (PROF, relative to the guarantee's first Monday): which driver comes
    back which week changes from winter to winter, the calendar does not."""
    NW = trips.shape[1]
    ws = np.where(kinds == "W")[0]
    gy = {}
    for k in ws:
        ed = week_dates[int(entry[k])]
        gy[k] = ed.year + (1 if ed.month >= 10 else 0)
        ret_years[k] = []
    last = {k: gy[k] for k in ws}          # the guarantee year of each driver's latest winter
    alive = set(int(k) for k in ws)
    for y in range(min(gy.values()), 2028):
        firsts = [int(k) for k in ws if gy[k] == y]
        elig = sorted(k for k in alive if last[k] == y - 1 and gy[k] < y)
        r = K.rng("returns", y)
        u = r.random(len(elig))
        back = [k for k, x in zip(elig, u) if x < w_pret[k]]
        for k, x in zip(elig, u):
            if x >= w_pret[k]:
                alive.discard(k)
        weeks = _deal(r, len(back))
        for k, pw in zip(back, weeks):
            personal[k] = pw
        for k in firsts + back:
            rr = K.rng("season", k, y)
            start = int(entry[k]) if k in firsts else K.widx(K.first_monday(y)) + int(personal[k])
            if k not in firsts:
                ret_years[k].append((y, int(personal[k])))
                last[k] = y
            stop = K.widx(dt.date(y, 4, 1)) + int(rr.integers(-1, 4))
            a, b = max(start, 0), min(stop, NW)
            if b > a:
                on = rr.random(b - a) < W_ACT
                trips[k, a:b] = np.where(on, rr.poisson(w_mean[k] * seas[a:b]), 0)


def window_trips(W, y):
    a = K.widx(K.WINDOW[y][0])
    return W.trips[:, a:a + 4].sum(1).astype(int)


def _qualify(W):
    """The payments system counts a window's completed trips per account; drivers within reach of 40 push to it."""
    W.wtrips, W.qual = {}, {}
    for y in K.GUARANTEE_YEARS:
        T = window_trips(W, y)
        r = K.rng("topup", y)
        u = r.random(W.n)
        near = (T >= TOPUP_LO) & (T < K.THRESHOLD)
        push = near & (u < TOPUP_P)
        if push.any():
            a = K.widx(K.WINDOW[y][0])
            # the extra trips land in the window's last week
            add = (K.THRESHOLD - T[push]) + (r.random(push.sum()) < 0.35).astype(int)
            W.trips[push, a + 3] += add.astype(np.int16)
            W.hours[push, a + 3] += (add / W.tph[push]).astype(np.float32)
            T = window_trips(W, y)
        W.wtrips[y] = T
        W.qual[y] = T >= K.THRESHOLD
    W.has = W.trips > 0


def monthly(W, values=None, rkey="split"):
    """Split each week's trips (or online hours) into calendar months by the weekday profile: a week straddling a
    month end sends each trip to the earlier month with the share of the week's weighted days that fall in it."""
    V = W.trips if values is None else values
    NW = V.shape[1]
    mlist = K.months(K.LAUNCH, K.wdate(NW - 1) + dt.timedelta(days=6))
    midx = {m: j for j, m in enumerate(mlist)}
    out = np.zeros((V.shape[0], len(mlist)), dtype=np.float64 if values is not None else np.int32)
    for i in range(NW):
        d0 = K.wdate(i)
        days = [d0 + dt.timedelta(days=j) for j in range(7)]
        m_a = K.ym(days[0])
        m_b = K.ym(days[6])
        col = V[:, i]
        if m_a == m_b:
            out[:, midx[m_a]] += col
            continue
        p = float(sum(WEEKDAY_W[j] for j in range(7) if K.ym(days[j]) == m_a) / WEEKDAY_W.sum())
        if values is None:
            r = K.rng(rkey, i)
            first = r.binomial(col.astype(np.int64), p)
            out[:, midx[m_a]] += first
            out[:, midx[m_b]] += col - first
        else:
            out[:, midx[m_a]] += col * p
            out[:, midx[m_b]] += col * (1 - p)
    return mlist, out
