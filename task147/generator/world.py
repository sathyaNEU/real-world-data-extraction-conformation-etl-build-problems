"""The Weighhouse's booking book, January 2022 to the 1 July 2027 extract, simulated stay by stay.

Every stay request carries its arrival, length, rooms, rate plan, channel and booking time, and the times it would be
cancelled, amended or not shown, drawn from its own stream when it is created. Requests are taken in booking-time order
and a stay is accepted only when every night of it has a room (the booking limit is the hotel's 480 rooms); a refused
request is lost. Cancellations free their rooms when they happen. Nothing here is shipped directly: records.py writes the
extracts from the accepted reservations."""
from __future__ import annotations

import datetime as dt
import heapq
import math

import numpy as np

import common as K

# ---------------------------------------------------------------------------------------------------- the demand
P = dict(wk0=0.55, wk1=1.55, wk2=1.15, wk3=1.50, close=1.4, unc=1.18, base_aug=300.0, disp=1.05,
         ws=92.0, ss=118.0, spring=0.50, sp_med=95.0, su_med=24.0, conc=700.0)

SEASON = {1: 255, 2: 270, 3: 300, 4: 330, 5: 355, 6: 380, 7: 370, 8: P["base_aug"], 9: 370, 10: 345, 11: 300, 12: 290}

LOS_LEIS = np.array([.30, .32, .20, .10, .05, .02, .01, 0])
LOS_BUS = np.array([.45, .35, .15, .05, 0, 0, 0, 0])
LOS_EVT = np.array([.42, .48, .10, 0, 0, 0, 0, 0])
LOS_WEEK = np.array([0, 0, 0, .04, .08, .12, .64, .12])      # festival week stays
LOS_SHORT = np.array([.22, .44, .26, .08, 0, 0, 0, 0])       # festival short stays
ROOMS_P = np.array([0.86, 0.10, 0.03, 0.01])
ROOMS_EVT = np.array([0.80, 0.16, 0.03, 0.01])

# rate plans: code -> (free cancellation until N days before arrival, chance the booking is cancelled)
PLANS = {"FLX": (2, 0.22), "SEMI": (14, 0.14), "APR": (None, 0.03), "EVT": (None, 0.015), "GRP": (21, 0.10),
         "COMP": (None, 0.0), "HSE": (None, 0.0)}
NOSHOW = {"FLX": 0.024, "SEMI": 0.020, "APR": 0.022, "EVT": 0.030, "GRP": 0.005, "COMP": 0.0, "HSE": 0.0}
AMEND_P = {"FLX": 0.030, "SEMI": 0.025, "APR": 0.0, "EVT": 0.0, "GRP": 0.0, "COMP": 0.0, "HSE": 0.0}

SEG_PLANS = {"BUS": (["FLX", "SEMI", "APR"], [0.70, 0.20, 0.10]),
             "LEIS": (["FLX", "SEMI", "APR"], [0.45, 0.25, 0.30]),
             "FWK": (["FLX", "SEMI", "APR"], [0.40, 0.25, 0.35]),
             "FSH": (["FLX", "SEMI", "APR"], [0.50, 0.25, 0.25])}
SEG_CHANNELS = {"BUS": (["GDS", "CORP", "WEB", "PHONE", "OTA1"], [0.34, 0.28, 0.22, 0.08, 0.08]),
                "LEIS": (["OTA1", "OTA2", "WEB", "PHONE", "OTA3"], [0.38, 0.17, 0.33, 0.06, 0.06]),
                "FWK": (["WEB", "OTA1", "OTA2", "PHONE", "OTA3"], [0.41, 0.30, 0.12, 0.12, 0.05]),
                "FSH": (["OTA1", "WEB", "OTA2", "PHONE", "OTA3"], [0.40, 0.34, 0.14, 0.06, 0.06]),
                "EVT": (["WEB", "OTA1", "OTA2", "PHONE"], [0.46, 0.36, 0.12, 0.06]),
                "GRP": (["GROUP"], [1.0]), "COMP": (["HOUSE"], [1.0]), "HSE": (["HOUSE"], [1.0])}


def er(lp, rp=ROOMS_P):
    return float(((lp / lp.sum()) * np.arange(1, 9)).sum() * ((rp / rp.sum()) * np.arange(1, 5)).sum())


E_LEIS, E_BUS, E_EVT = er(LOS_LEIS), er(LOS_BUS), er(LOS_EVT, ROOMS_EVT)


def cnt(r, lam, disp=None):
    """A request count with mean lam and a variance well under Poisson's (the hotel's demand is steady)."""
    disp = P["disp"] if disp is None else disp
    if lam <= 0:
        return 0
    n = max(int(math.ceil(disp * lam)), int(math.ceil(lam)) + 1)
    return int(r.binomial(n, lam / n))


def base_target(d):
    m = SEASON[d.month]
    w = d.weekday()
    summer = d.month in (7, 8)
    f = (1.00 if not summer else 0.97) if w <= 3 else {4: 1.07, 5: 1.12, 6: 0.84}[w]
    if d in K.HOLIDAYS and w == 6:
        f *= 1.12     # the Sunday of a bank holiday weekend
    return m * f


def fest_arrivals(d):
    """Expected festival requests arriving on d: (week stays, short stays). A week stay belongs to the roster week
    holding most of its nights (arrival plus two days); a short stay to the week it arrives in."""
    y = d.year
    k = (d - K.fest_open(y)).days
    if k < -2 or k > 23:
        return 0.0, 0.0
    w = d.weekday()
    sc = {0: P["wk0"], 1: P["wk1"], 2: P["wk2"], 3: P["wk3"]}
    wk_w = (k + 2 + 4) // 7
    wk_s = (k + 4) // 7
    wk_arr = {5: 0.60, 6: 0.20, 4: 0.12, 0: 0.05, 1: 0.03, 2: 0.0, 3: 0.0}[w]
    week = P["ws"] * sc.get(wk_w, 0) * wk_arr if (k + 7 <= 25) else 0.0
    sh_arr = {3: 0.20, 4: 0.34, 5: 0.24, 0: 0.06, 1: 0.06, 2: 0.06, 6: 0.04}[w]
    short = P["ss"] * sc.get(wk_s, 0) * sh_arr if k >= 0 else 0.0
    if k in (21, 22):
        short *= P["close"]       # the closing weekend's finale
    return week, short


# events that fill Friday and Saturday nights weeks ahead: (announced, nights, requests per night, label)
EVENTS = [
    (dt.date(2022, 9, 20), [dt.date(2022, 11, 11), dt.date(2022, 11, 12)], 520, "rugby"),
    (dt.date(2023, 3, 6), [dt.date(2023, 5, 19), dt.date(2023, 5, 20)], 560, "concert"),
    (dt.date(2023, 7, 31), [dt.date(2023, 10, 13), dt.date(2023, 10, 14)], 500, "conference"),
    (dt.date(2024, 1, 15), [dt.date(2024, 3, 8), dt.date(2024, 3, 9)], 540, "rugby"),
    (dt.date(2024, 4, 22), [dt.date(2024, 6, 28), dt.date(2024, 6, 29)], 600, "concert"),
    (dt.date(2024, 9, 2), [dt.date(2024, 11, 15), dt.date(2024, 11, 16)], 500, "rugby"),
    (dt.date(2025, 3, 3), [dt.date(2025, 5, 2), dt.date(2025, 5, 3)], 560, "concert"),
    (dt.date(2025, 7, 14), [dt.date(2025, 9, 26), dt.date(2025, 9, 27)], 580, "concert"),
    (dt.date(2026, 1, 12), [dt.date(2026, 3, 13), dt.date(2026, 3, 14)], 540, "rugby"),
    (dt.date(2026, 3, 30), [dt.date(2026, 6, 5), dt.date(2026, 6, 6)], 600, "concert"),
    (dt.date(2026, 8, 31), [dt.date(2026, 11, 6), dt.date(2026, 11, 7)], 520, "rugby"),
    (dt.date(2027, 6, 15), K.CONCERT_NIGHTS, P["conc"], "concert"),
]


class Req:
    __slots__ = ("bt", "a", "los", "rooms", "plan", "seg", "chan", "ct", "noshow", "amend", "key")

    def __init__(self, bt, a, los, rooms, plan, seg, chan, ct, noshow, amend, key):
        self.bt, self.a, self.los, self.rooms, self.plan, self.seg = bt, a, los, rooms, plan, seg
        self.chan, self.ct, self.noshow, self.amend, self.key = chan, ct, noshow, amend, key


def cancel_time(r, bt, a, plan):
    """The time a booking would be cancelled, or None: soon after booking, near its free-cancellation deadline, or
    anywhere between."""
    days, p = PLANS[plan]
    if r.uniform() >= p:
        return None
    lo = bt + 0.01
    hi = a - days if days is not None else a - 0.05
    hi = max(lo + 0.02, hi)
    u = r.uniform()
    if u < 0.45:
        t = lo + r.exponential(6.0)
    elif u < 0.75:
        t = hi - r.exponential(3.0)
    else:
        t = r.uniform(lo, hi)
    return min(max(t, lo), hi)


def lead_draw(r, seg, n, med, sig):
    if seg in ("FWK", "FSH"):
        spring = r.uniform(size=n) < P["spring"]
        lead = np.where(spring, np.exp(r.normal(math.log(P["sp_med"]), 0.30, size=n)),
                        np.exp(r.normal(math.log(P["su_med"]), 0.55, size=n)))
        return np.minimum(lead, 300.0)
    return np.minimum(np.exp(r.normal(math.log(med), sig, size=n)), 340.0)


def make(seg, d, n, lp, med, sig, rp=ROOMS_P, bt_fixed=None, plan_fixed=None, tag="", min_bt=None):
    """n requests of one segment arriving on d, each with every attribute drawn from the stream (seg, d, tag)."""
    if n <= 0:
        return []
    r = K.rng("req", seg, d.isoformat(), tag)
    a = K.di(d)
    los = r.choice(np.arange(1, 9), size=n, p=lp / lp.sum())
    rooms = r.choice(np.arange(1, 5), size=n, p=rp / rp.sum())
    lead = lead_draw(r, seg, n, med, sig) if bt_fixed is None else None
    bts = (a - lead + r.uniform(0, 0.5, size=n)) if bt_fixed is None else bt_fixed(r, n)
    if plan_fixed:
        plans = [plan_fixed] * n
    else:
        codes, w = SEG_PLANS[seg]
        plans = list(r.choice(codes, size=n, p=w))
    chans_c, chans_w = SEG_CHANNELS[seg]
    chans = list(r.choice(chans_c, size=n, p=chans_w))
    out = []
    for j in range(n):
        bt = float(bts[j])
        if bt >= a:
            bt = a - r.uniform(0.05, 0.9)
        plan = str(plans[j])
        ct = cancel_time(r, bt, a, plan)
        ns = r.uniform() < NOSHOW[plan]
        am = None
        if r.uniform() < AMEND_P[plan]:
            at = r.uniform(bt + 0.5, max(bt + 0.6, a - 1.0))
            shift = int(r.choice([-2, -1, 1, 2, 0, 0], p=[0.15, 0.30, 0.30, 0.15, 0.05, 0.05]))
            dlos = 0 if shift != 0 else int(r.choice([-1, 1]))
            am = (at, shift, dlos)
        if min_bt is not None and bt < min_bt:
            continue
        out.append(Req(bt, a, int(los[j]), int(rooms[j]), plan, seg, str(chans[j]), ct, ns, am,
                       "%s|%s|%s|%d" % (seg, d.isoformat(), tag, j)))
    return out


def requests(nights, min_bt=None, tag="", events=EVENTS):
    out = []
    nset = set(nights)
    for d in nights:
        w = d.weekday()
        bt = base_target(d) * P["unc"]
        bshare = 0.45 if (w <= 3 and d.month not in (7, 8)) else (0.25 if w <= 3 else 0.08)
        rb = K.rng("cnt", d.isoformat(), tag)
        out += make("BUS", d, cnt(rb, bt * bshare / E_BUS * (1.0 if w in (0, 1, 2, 3, 6) else 0.4)), LOS_BUS, 12,
                    0.8, tag=tag, min_bt=min_bt)
        out += make("LEIS", d, cnt(rb, bt * (1 - bshare) / E_LEIS), LOS_LEIS, 38, 0.9, tag=tag, min_bt=min_bt)
        wa, sa = fest_arrivals(d)
        if wa > 0:
            out += make("FWK", d, cnt(rb, wa * P["unc"]), LOS_WEEK, 0, 0, tag=tag, min_bt=min_bt)
        if sa > 0:
            out += make("FSH", d, cnt(rb, sa * P["unc"]), LOS_SHORT, 0, 0, tag=tag, min_bt=min_bt)
        # complimentary and house-use rooms (staff on call, guests of the hotel): a few a night
        nc = int(rb.poisson(0.9))
        if nc:
            out += make("COMP", d, nc, np.array([.5, .3, .2, 0, 0, 0, 0, 0]), 9, 0.7,
                        rp=np.array([1.0, 0, 0, 0]), plan_fixed="COMP" if rb.uniform() < 0.6 else "HSE",
                        tag=tag, min_bt=min_bt)
        # coach tours in late spring, summer and early autumn: whole groups on one booking reference
        if d.month in (5, 6, 7, 9) and w in (0, 3, 6) and rb.uniform() < 0.22:
            out += make("GRP", d, 1, np.array([0, .45, .40, .15, 0, 0, 0, 0]), 110, 0.35,
                        rp=np.array([1.0, 0, 0, 0]), plan_fixed="GRP", tag=tag, min_bt=min_bt)
    for ann, ev_nights, nreq, lab in events:
        ann_t = K.di(ann) + 0.42
        for nt in ev_nights:
            for arr, share in ((nt - dt.timedelta(days=1), 0.35), (nt, 0.65)):
                if arr not in nset:
                    continue
                re = K.rng("evcnt", arr.isoformat(), nt.isoformat(), tag)
                n = cnt(re, nreq * share / E_EVT)
                if nt in K.CONCERT_NIGHTS:
                    on_sale = K.from_local(K.CONCERT_ON_SALE)
                    fixed = lambda r, n: on_sale + r.exponential(1.6, size=n)
                else:
                    fixed = lambda r, n, t=ann_t: t + 4 + r.exponential(5.0, size=n)
                out += make("EVT", arr, n, LOS_EVT, 0, 0, rp=ROOMS_EVT, bt_fixed=fixed, plan_fixed="EVT",
                            tag=tag + "|" + nt.isoformat(), min_bt=min_bt)
    # group bookings carry several rooms each: 8 to 22 rooms, one row per room downstream
    for q in out:
        if q.seg == "GRP":
            rg = K.rng("grp", q.key)
            q.rooms = int(rg.integers(8, 23))
    out.sort(key=lambda q: (q.bt, q.key))
    return out


class Res:
    __slots__ = ("q", "a", "los", "status", "ct", "amended", "orig_a", "orig_los", "rid")

    def __init__(self, q, rid):
        self.q, self.a, self.los, self.ct, self.rid = q, q.a, q.los, None, rid
        self.status, self.amended, self.orig_a, self.orig_los = "OK", None, q.a, q.los


def run(reqs, booked, res, heap, t_stop=None):
    """Take requests in booking-time order; each accepted only if every night has a room. Cancellations and
    amendments are events on the heap, applied when their time comes."""
    def settle(upto):
        while heap and heap[0][0] <= upto:
            t, kind, i = heapq.heappop(heap)
            rr = res[i]
            if rr.status != "OK":
                continue
            if kind == 0:      # cancellation
                booked[rr.a:rr.a + rr.los] -= rr.q.rooms
                rr.status, rr.ct = "CXL", t
            else:              # amendment: move the stay if the new nights have room, otherwise keep it
                _, shift, dlos = rr.q.amend
                na, nl = rr.a + shift, max(1, rr.los + dlos)
                booked[rr.a:rr.a + rr.los] -= rr.q.rooms
                if np.all(booked[na:na + nl] + rr.q.rooms <= K.CAP) and na > t:
                    booked[na:na + nl] += rr.q.rooms
                    rr.amended = (t, rr.a, rr.los, na, nl)
                    rr.a, rr.los = na, nl
                else:
                    booked[rr.a:rr.a + rr.los] += rr.q.rooms
    for q in reqs:
        if t_stop is not None and q.bt >= t_stop:
            break
        settle(q.bt)
        if np.all(booked[q.a:q.a + q.los] + q.rooms <= K.CAP):
            booked[q.a:q.a + q.los] += q.rooms
            rr = Res(q, len(res))
            res.append(rr)
            if q.amend is not None and (q.ct is None or q.amend[0] < q.ct):
                heapq.heappush(heap, (q.amend[0], 1, rr.rid))
            if q.ct is not None:
                heapq.heappush(heap, (q.ct, 0, rr.rid))
    if t_stop is not None:
        settle(t_stop)


def nights_range(first, last):
    return [first + dt.timedelta(days=i) for i in range((last - first).days + 1)]


def simulate():
    nights = nights_range(K.SIM_FIRST_NIGHT, K.SIM_LAST_NIGHT)
    reqs = requests(nights)
    N = K.di(dt.date(2028, 2, 1))
    booked = np.zeros(N, dtype=np.int32)
    res, heap = [], []
    run(reqs, booked, res, heap, t_stop=K.T_EXTRACT)
    W = type("World", (), {})()
    W.res, W.booked, W.heap, W.reqs_n = res, booked, heap, len(reqs)
    W.pending = list(heap)
    return W


def occupied(res, first, last, t_obs=None):
    """Rooms occupied each night first..last by reservations that stayed (not cancelled, not a no-show)."""
    n0, n1 = K.di(first), K.di(last)
    occ = np.zeros(n1 - n0 + 1)
    for rr in res:
        if rr.status != "OK" or rr.q.noshow:
            continue
        lo, hi = max(rr.a, n0), min(rr.a + rr.los - 1, n1)
        if lo <= hi:
            occ[lo - n0:hi - n0 + 1] += rr.q.rooms
    return occ


def mc_truth(W, runs=24):
    """The expected occupied rooms of each 2027 season night given the book at the extract: fresh demand after the
    extract and the live book's future cancellations, no-shows and amendments redrawn, run to the end (truth only)."""
    season = K.season_nights(K.YEAR)
    first, last = season[0], season[-1]
    out = []
    t0 = K.T_EXTRACT
    window = nights_range(dt.date(2027, 6, 20), dt.date(2027, 9, 30))
    for m in range(runs):
        r2 = K.rng("mc", m)
        booked = W.booked.copy()
        res = []
        heap = []
        for rr in W.res:
            c = Res(rr.q, len(res))
            c.a, c.los, c.status, c.ct, c.amended = rr.a, rr.los, rr.status, rr.ct, rr.amended
            res.append(c)
            if c.status == "OK" and c.a + c.los > K.di(dt.date(2027, 6, 30)) and c.a > t0 - 400:
                # live at the extract: redraw a future cancellation from its conditional law
                for _ in range(200):
                    ct = cancel_time(r2, rr.q.bt, rr.a, rr.q.plan)
                    if ct is None or ct > t0:
                        break
                if ct is not None and ct < c.a:
                    heapq.heappush(heap, (ct, 0, c.rid))
        fut = requests(window, min_bt=t0, tag="mc%d" % m, events=[EVENTS[-1]])
        nb = len(res)
        run(fut, booked, res, heap)
        occ = np.zeros(len(season))
        n0 = K.di(first)
        for c in res:
            if c.status != "OK":
                continue
            ns = c.q.noshow if c.rid >= nb else (r2.uniform() < NOSHOW[c.q.plan])
            if ns:
                continue
            lo, hi = max(c.a, n0), min(c.a + c.los - 1, n0 + len(season) - 1)
            if lo <= hi:
                occ[lo - n0:hi - n0 + 1] += c.q.rooms
        out.append(occ)
    return np.array(out)
