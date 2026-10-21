"""task177 world: the clean truth before any record is written.

Prairie Works Manitoba (fictional) runs employment and income assistance for jobseekers across the province. A
jobseeker with an open claim contacts the service about it (a payment, an earnings report, an appointment, a
document) either by calling the claimant line, where an adviser answers, or by opening a conversation with the
service's digital assistant, Ask Prairie Works, in the app or on the web. The assistant went live on 5 January 2026.
When the claimant queue is in overflow, the platform transfers each call that reaches it to the assistant's voice
service instead of letting it wait: the jobseeker chose the phone and met the assistant.

Each jobseeker chooses a channel for each contact from what the two channels have done for them: a value for each
channel moved after every contact towards its outcome (resolved or not), a softmax over the two values with the
jobseeker's own lean, and a pull towards the channel chosen last time. A contact the jobseeker was sent to by the
overflow moves the assistant's value a fifth as far as one they chose. That is the generating process; nothing in
the pack names it.

Every process parameter below was fixed by rule before any outcome was measured; the seeds are named streams."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as C

# --- how jobseekers choose and learn -------------------------------------------------------------------------------
LEARN = dict(a_free=0.40,      # the update after a contact the jobseeker chose
             a_forced=0.08,    # the update after an overflow transfer (a fifth of a chosen one)
             beta=5.0,         # the weight on the difference between the two channels' values
             bias=-0.40,       # the average lean towards the phone (the assistant's logit at equal values)
             bias_sd=0.00,     # the spread of the lean across jobseekers
             kappa=0.30,       # the pull towards the channel chosen last time (+1 assistant, -1 phone)
             q0=0.50)          # both channels' value at a jobseeker's first contact after the launch

# --- what each channel does ----------------------------------------------------------------------------------------
P_ABANDON = 0.025              # calls given up in the claimant queue
P_ADVISER_RES = 0.905          # calls an adviser resolves (the rest end with a callback booked)
P_PHONE = (1 - P_ABANDON) * P_ADVISER_RES
OLD_ASST = dict(resolved=0.50, handoff=0.36, abandoned=0.14)    # the 2026 assistant, chat and voice alike
NEW_ASST = 2003 / 2400         # the upgraded assistant, the acceptance test's resolved share
P_SPLIT = 0.01                 # jobseekers' chat conversations that time out and are reopened (a second session)

# --- jobseekers and their claims -------------------------------------------------------------------------------
DRAW = "d7"                    # the world's draw (its random streams carry this tag)
N_OPEN_AT_LAUNCH = 13500
NEW_PER_WEEKDAY = 64.5
NEW_SEASON = (1.22, 1.12, 1.05, 0.98, 0.92, 0.90, 0.95, 0.97, 1.08, 1.02, 0.95, 0.84)
SHORT = (0.0, 9.5)             # share of new claims that are short, and their mean length in months
LONG = (1.0, 9.5)
RATE = (4.0, 0.375)            # (unused) gamma rates of an earlier draft
CYCLE = 14                     # days between check-ins
LATE = (0.60, 0.20, 0.12, 0.08)                                  # check-in made 0 to 3 days after it is due
ADHOC = 0.50                   # questions a month in between check-ins, every jobseeker alike
DOW = (1.25, 1.10, 1.05, 1.00, 0.95, 0.60, 0.50)                # Monday first
HOLIDAY_W = 0.55
XMAS = (dt.date(2026, 12, 21), dt.date(2027, 1, 3), 0.65)

# --- the claimant line ---------------------------------------------------------------------------------------------
PHONE_HOURS = {0: (8, 18), 1: (8, 18), 2: (8, 18), 3: (8, 18), 4: (8, 18), 5: (9, 13)}     # by weekday, local
# when in the day a jobseeker sets about a contact (local hour 0 to 23); a call the line is closed for is made at the
# next opening, within the first hour and a half
DAY_PROFILE = (0.20, 0.10, 0.05, 0.05, 0.05, 0.15, 0.40, 0.80, 1.30, 1.60, 1.60, 1.50, 1.40, 1.40, 1.40, 1.30, 1.20,
               1.10, 1.00, 1.00, 1.00, 0.80, 0.60, 0.35)
DEFER = 90                     # minutes after the opening a deferred call is made, uniform
# overflow: episodes when the queue's predicted wait passes its threshold, mostly the first hours of a Monday or the
# day after a holiday; every call reaching the queue in one is transferred to the assistant
EPISODE_P = {0: 0.40, 1: 0.16, 2: 0.07, 3: 0.08, 4: 0.06, 5: 0.0}
EPISODE_AFTER_HOLIDAY = 0.60
EPISODE_LEN = (15, 70)         # minutes, uniform
EPISODE_START = (8 * 60 + 5, 10 * 60 + 40)
SECOND_EPISODE_P = 0.18        # a second episode the same day, around the lunch hour


def day_weight(d):
    w = DOW[d.weekday()]
    if d in C.HOLIDAYS:
        w *= HOLIDAY_W
    if XMAS[0] <= d <= XMAS[1]:
        w *= XMAS[2]
    return w * 7.0 / sum(DOW)


def phone_open(d):
    return d.weekday() in PHONE_HOURS and d not in C.HOLIDAYS


def next_open(d):
    d = d + dt.timedelta(days=1)
    while not phone_open(d):
        d += dt.timedelta(days=1)
    return d


def call_time(d, t, delay):
    """the day and minute a call is made for a contact set about on day d at minute t"""
    if phone_open(d):
        o, c = PHONE_HOURS[d.weekday()]
        if o * 60 <= t < c * 60:
            return d, t
        if t < o * 60:
            return d, o * 60 + delay
    nd = next_open(d)
    return nd, PHONE_HOURS[nd.weekday()][0] * 60 + delay


def in_window(windows, d, t):
    wins = windows.get(d)
    return bool(wins) and any(a <= t < b for a, b in wins)


def overflow_windows(day_list, rng):
    """{date: [(start_minute, end_minute), ...]} in local time"""
    out = {}
    prev_closed = False
    for d in day_list:
        if not phone_open(d):
            prev_closed = d.weekday() < 5     # a weekday holiday piles calls onto the next open day
            continue
        p = EPISODE_P[d.weekday()]
        if prev_closed:
            p = max(p, EPISODE_AFTER_HOLIDAY)
        prev_closed = False
        wins = []
        if rng.random() < p:
            s = int(rng.integers(EPISODE_START[0], EPISODE_START[1]))
            if d.weekday() == 5:
                s = int(rng.integers(9 * 60 + 5, 10 * 60 + 30))
            ln = int(rng.integers(EPISODE_LEN[0], EPISODE_LEN[1] + 1))
            wins.append((s, s + ln))
            if rng.random() < SECOND_EPISODE_P and d.weekday() < 5:
                s2 = int(rng.integers(11 * 60 + 30, 13 * 60 + 30))
                wins.append((s2, s2 + int(rng.integers(15, 50))))
        if wins:
            out[d] = wins
    return out


def _profile_minutes(rng, n, profile, start_hour):
    p = np.array(profile, float)
    h = rng.choice(len(p), size=n, p=p / p.sum())
    return (start_hour + h) * 60 + rng.integers(0, 60, size=n)


class Claims:
    """every claim open at some point from the launch to the record's end"""

    def __init__(self):
        rng = C.stream("claims/" + DRAW)
        rows = []
        # claims open at the launch: length-biased towards long claims, opened 2023 to 2025
        w_long = LONG[0] * LONG[1] / (LONG[0] * LONG[1] + SHORT[0] * SHORT[1])
        for i in range(N_OPEN_AT_LAUNCH):
            long_ = rng.random() < w_long
            mean = (LONG if long_ else SHORT)[1]
            age = rng.gamma(2.0, mean * 30.44 / 2.0)            # days since it opened (length-biased age)
            opened = C.LAUNCH - dt.timedelta(days=int(age) + 1)
            rest = rng.exponential(mean * 30.44)
            closed = C.LAUNCH + dt.timedelta(days=int(rest))
            rows.append((opened, closed, long_))
        for d in C.days(C.LAUNCH, C.REC_END):
            if d.weekday() >= 5 or d in C.HOLIDAYS:
                continue
            k = rng.poisson(NEW_PER_WEEKDAY * NEW_SEASON[d.month - 1])
            for _ in range(k):
                long_ = rng.random() < LONG[0]
                mean = (LONG if long_ else SHORT)[1]
                closed = d + dt.timedelta(days=int(rng.exponential(mean * 30.44)) + 1)
                rows.append((d, closed, long_))
        self.opened = np.array([r[0] for r in rows], dtype="datetime64[D]")
        self.closed = np.array([r[1] for r in rows], dtype="datetime64[D]")   # the first day the claim is closed
        self.long = np.array([r[2] for r in rows])
        self.n = len(rows)
        self.rate = rng.gamma(RATE[0], RATE[1], self.n)
        self.bias = LEARN["bias"] + LEARN["bias_sd"] * rng.standard_normal(self.n)


class Timeline:
    """minute by minute from a start date: whether the claimant line is open, the next minute it is, and whether the
    claimant queue is in an overflow episode"""

    def __init__(self, start, end, windows):
        self.start = start
        self.days = C.days(start, end + dt.timedelta(days=10))    # room for calls carried past the end
        n = len(self.days) * 1440
        self.open = np.zeros(n, bool)
        self.over = np.zeros(n, bool)
        for i, d in enumerate(self.days):
            if phone_open(d):
                o, c = PHONE_HOURS[d.weekday()]
                self.open[i * 1440 + o * 60:i * 1440 + c * 60] = True
            for a_, b_ in windows.get(d, []):
                self.over[i * 1440 + a_:i * 1440 + b_] = True
        nxt = np.full(n, n, dtype=np.int64)
        idx = np.flatnonzero(self.open)
        pos = np.searchsorted(idx, np.arange(n))
        ok = pos < idx.size
        nxt[ok] = idx[pos[ok]]
        self.next_open = nxt
        self.windows = windows

    def call_minute(self, m, delay):
        """the minute a call is made for a contact set about at minute m"""
        m = np.asarray(m)
        return np.where(self.open[m], m, self.next_open[m] + delay)

    def day_of(self, m):
        return [self.days[int(x) // 1440] for x in np.atleast_1d(m)]


class Contacts:
    """each jobseeker's contacts over a span: when each is set about (minutes from the span's start), the fortnightly
    check-ins and the questions in between, and the draws that settle the choice, the call's delay and the outcome"""

    def __init__(self, claims, start=C.REC_START, end=C.REC_END, tag="hist", windows=None):
        rng = C.stream("contacts/" + tag + "/" + DRAW)
        dl = C.days(start, end)
        dnum = np.array(dl, dtype="datetime64[D]")
        w = np.array([day_weight(d) for d in dl])
        self.days = dl
        if windows is None:
            windows = overflow_windows(C.days(start, end + dt.timedelta(days=10)), C.stream("overflow/" + tag + "/" + DRAW))
        self.tl = Timeline(start, end, windows)
        self.windows = windows
        one = np.timedelta64(1, "D")
        lo = np.maximum(claims.opened, np.datetime64(start))
        hi = np.minimum(claims.closed, np.datetime64(end) + one)              # exclusive
        cum = np.concatenate([[0.0], np.cumsum(w)])
        i0 = np.clip((lo - dnum[0]).astype(int), 0, len(dl))
        i1 = np.clip((hi - dnum[0]).astype(int), 0, len(dl))
        # the fortnightly check-in: due every 14 days from the claim's opening, made on the day or up to three
        # days late, while the claim is open
        who_c, di_c = [], []
        late = rng.choice(4, size=claims.n * 40, p=LATE)
        q = 0
        op = (claims.opened - dnum[0]).astype(int)
        for i in range(claims.n):
            if i1[i] <= i0[i]:
                continue
            k = max(1, -(-(i0[i] - op[i]) // CYCLE))
            while True:
                due = op[i] + CYCLE * k
                if due >= i1[i]:
                    break
                d_ = due + int(late[q % late.size]); q += 1
                if i0[i] <= d_ < i1[i]:
                    who_c.append(i); di_c.append(d_)
                k += 1
        # questions in between, at one rate for every jobseeker, by the day weights
        expo = np.where(i1 > i0, cum[i1] - cum[i0], 0.0)
        n = rng.poisson(ADHOC * 12.0 / 365.25 * expo)
        who_a = np.repeat(np.arange(claims.n), n)
        u = rng.random(who_a.size)
        target = cum[i0[who_a]] + u * (cum[i1[who_a]] - cum[i0[who_a]])
        di_a = np.clip(np.searchsorted(cum, target, side="right") - 1, i0[who_a], i1[who_a] - 1)
        who = np.concatenate([np.array(who_c, int), who_a])
        di = np.concatenate([np.array(di_c, int), di_a])
        kind = np.concatenate([np.ones(len(who_c), bool), np.zeros(who_a.size, bool)])   # True: a check-in
        m = who.size
        im = _profile_minutes(rng, m, DAY_PROFILE, 0)
        order = np.lexsort((im, di, who))
        self.who, self.kind = who[order], kind[order]
        self.init = (di[order] * 1440 + im[order]).astype(np.int64)     # minutes from the span's start
        self.m = m
        self.delay = rng.integers(0, DEFER, size=m)
        self.u_choice = rng.random(m)
        self.u_out = rng.random(m)
        self.u_kind = rng.random(m)          # which way an unresolved contact ended
        self.u_split = rng.random(m)
        first = np.r_[0, np.flatnonzero(np.diff(self.who)) + 1] if m else np.zeros(0, int)
        self.first = first
        self.count = np.diff(np.r_[first, m]) if m else np.zeros(0, int)
        self.pos = np.arange(m) - np.repeat(first, self.count)


def run_learning(claims, ct, P, imposed_until=None, p_bot=None, phone_p=P_PHONE, q_init=None):
    """play every jobseeker's contacts in order. A contact is set about no earlier than the jobseeker's previous one
    started; a phone choice is made as a call at that minute or the line's next opening; a call reaching the claimant
    queue in an overflow episode, or any call before minute imposed_until, meets the assistant. Returns per contact
    the choice, the transfer, the outcome and the minute it started, and the end state."""
    tl = ct.tl
    m = ct.m
    L = int(ct.count.max()) if m else 0
    if q_init is None:
        qb = np.full(claims.n, P["q0"]); qp = np.full(claims.n, P["q0"]); last = np.zeros(claims.n)
    else:
        qb, qp, last = (x.copy() for x in q_init)
    busy = np.full(claims.n, -1, dtype=np.int64)
    choice = np.zeros(m, bool)
    red = np.zeros(m, bool)
    res = np.zeros(m, bool)
    start = np.zeros(m, np.int64)
    pb_ = OLD_ASST["resolved"] if p_bot is None else p_bot
    bias = claims.bias
    for t in range(L):
        idx = np.flatnonzero(ct.pos == t)
        if idx.size == 0:
            break
        w = ct.who[idx]
        x = P["beta"] * (qb[w] - qp[w]) + bias[w] + P["kappa"] * last[w]
        cb = ct.u_choice[idx] < 1.0 / (1.0 + np.exp(-x))
        s0 = np.maximum(ct.init[idx], busy[w] + 1)
        call = tl.call_minute(s0, ct.delay[idx])
        st = np.where(cb, s0, call)
        if imposed_until is None:
            rd = (~cb) & tl.over[np.minimum(call, tl.over.size - 1)]
        else:
            rd = (~cb) & ((call < imposed_until) | tl.over[np.minimum(call, tl.over.size - 1)])
        gb = cb | rd
        r = np.where(gb, ct.u_out[idx] < pb_, ct.u_out[idx] < phone_p)
        a = np.where(rd, P["a_forced"], P["a_free"])
        qb[w] = np.where(gb, qb[w] + a * (r - qb[w]), qb[w])
        qp[w] = np.where(~gb, qp[w] + P["a_free"] * (r - qp[w]), qp[w])
        last[w] = np.where(cb, 1.0, -1.0)
        busy[w] = st
        choice[idx], red[idx], res[idx], start[idx] = cb, rd, r, st
    return dict(choice=choice, red=red, res=res, start=start, qb=qb, qp=qp, last=last)


class _Pop:
    """the planning population as a claims-like object, each claim closing after its drawn remaining life"""

    def __init__(self, claims, pop, life_days):
        self.n = pop.size
        self.opened = claims.opened[pop]
        self.closed = np.datetime64(C.POP_DATE) + np.timedelta64(1, "D") + life_days.astype("timedelta64[D]")
        self.bias = claims.bias[pop]


def forecast_truth(claims, end_state, P, reps=40):
    """the true expected share of the planning population's own contacts started in the assistant in the window:
    their check-ins and questions from 4 January to 25 April 2027 while their claims stay open, the assistant-first
    weeks sending every call to the upgraded assistant, then the line back to advisers with its overflow"""
    pop = np.flatnonzero((claims.opened <= np.datetime64(C.POP_DATE)) & (claims.closed > np.datetime64(C.POP_DATE)))
    af_end = ((C.AF_END - C.AF_START).days + 1) * 1440
    w0 = (C.WIN_START - C.AF_START).days * 1440
    w1 = ((C.WIN_END - C.AF_START).days + 1) * 1440
    tb = tt = tb_af = tt_af = 0
    for k in range(reps):
        rng = C.stream("forecast_truth/life/%d" % k)
        life = rng.exponential(LONG[1] * 30.44, size=pop.size).astype(int)
        pc = _Pop(claims, pop, life)
        win = overflow_windows(C.days(C.AF_START, C.WIN_END + dt.timedelta(days=10)), C.stream("overflow/2027/%d" % k))
        ct = Contacts(pc, start=C.AF_START, end=C.WIN_END, tag="2027/%d" % k, windows=win)
        R = run_learning(pc, ct, P, imposed_until=af_end, p_bot=NEW_ASST,
                         q_init=(end_state["qb"][pop], end_state["qp"][pop], end_state["last"][pop]))
        inw = (R["start"] >= w0) & (R["start"] < w1)
        inaf = R["start"] < af_end
        tb += int((R["choice"] & inw).sum()); tt += int(inw.sum())
        tb_af += int((R["choice"] & inaf).sum()); tt_af += int(inaf.sum())
    return dict(share=tb / tt, share_af=tb_af / tt_af, contacts=tt / reps, pop=pop.size)
