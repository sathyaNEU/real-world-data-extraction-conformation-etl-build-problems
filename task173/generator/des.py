"""The 2026 season at the level the CRM and the ACD record it: a discrete-event simulation of both expert queues.

Each day, experts work their scheduled shifts with their breaks; customers join the queue (new cases on the day's
intraday profile, follow-ups when they come back); the queue offers the waiting customer to the expert who has been
free longest; an offer an expert misses is re-offered (the ACD's redirect on no answer); a video session that fails
to connect after an expert accepts goes back into the queue as a new ACD contact with the same session; a customer
who has waited past their patience leaves and tries again later. Behaviour (who settles a case at the first contact,
how long a contact takes) is world.py's, so the 2026 season follows the same rules as every earlier one."""
from __future__ import annotations

import datetime as dt
import heapq
import math

import numpy as np

import common as K
import world as W

HOURLY = np.array([0.55, 0.85, 1.05, 1.12, 1.02, 0.95, 0.98, 1.02, 1.0, 0.98, 1.06, 1.14, 1.08, 0.92, 0.72, 0.52])  # 08-24


def open_hours(d, y):
    f0, f1 = K.fortnight(y)
    return (8.0, 24.0) if f0 <= d <= f1 else (8.0, 22.0)


def intraday_weights(d, y):
    o, c = open_hours(d, y)
    w = HOURLY[: int(c - o)]
    return w / w.sum()


# ------------------------------------------------------------------------------------------------- shifts
def weekly_hours(y, e, d, level):
    """The hours an in-house expert is scheduled in the week of day d, and how many days."""
    f0, f1 = K.fortnight(y)
    if f0 <= d <= f1:
        return K.SCHEDULE_HOURS / 2, 6
    if d > f1:
        return 16.0, 4
    base = {1: 16.0, 2: 26.0, 3: 35.0, 4: 40.0}[d.month] * level
    return base, (4 if base < 22 else 5)


def week_plan(R, y, monday_, hours, days, queue):
    """An expert's shifts for one week: working days drawn with weight on the busier days, each shift's length
    in proportion to that day's expected demand, kept between 3.5 and 11 hours, the week's hours held."""
    week = [monday_ + dt.timedelta(k) for k in range(7)]
    dem = np.array([W.demand_curve(dd, y, 1.0, queue) for dd in week])
    pick = R.choice(7, size=days, replace=False, p=dem / dem.sum())
    pick = sorted(int(k) for k in pick)
    raw = np.array([dem[k] for k in pick])
    length = hours * raw / raw.sum()
    for _ in range(4):
        length = np.clip(length, 3.5, 11.0)
        length = length * hours / length.sum()
    return {week[k]: float(round(l * 4) / 4) for k, l in zip(pick, length)}


def shift_for(R, d, y, length, close=None):
    """A shift of `length` hours inside the open hours, starts staggered to follow the intraday profile."""
    o, c = open_hours(d, y)
    c = min(c, close) if close else c
    latest = c - length
    starts = np.arange(o, latest + 0.01, 0.5)
    if len(starts) == 0:
        return o, c
    # weight a start by the demand it covers
    w = np.array([HOURLY[int(s - 8): int(min(s + length, c) - 8)].sum() + 0.3 for s in starts])
    s = float(R.choice(starts, p=w / w.sum()))
    return s, s + length


def breaks_for(R, s, e):
    """Breaks inside a shift: 15 minutes per full 4 hours and a 30-minute meal for shifts of 6 hours or more."""
    out = []
    length = e - s
    if length >= 6:
        mid = s + length / 2 + float(R.uniform(-0.5, 0.5))
        out.append((mid, mid + 0.5, "Meal"))
    n15 = int(length // 4) + (1 if length >= 6 else 0)
    for k in range(n15):
        t = s + (k + 1) * length / (n15 + 1) + float(R.uniform(-0.3, 0.3))
        if all(abs(t - b0) > 0.75 for b0, _, _ in out):
            out.append((t, t + 0.25, "Break"))
    return sorted(out)


# ------------------------------------------------------------------------------------------------- the season
REC = np.dtype([("day", "i4"), ("queue", "i1"), ("case", "i4"), ("pos", "i2"), ("expert", "i4"), ("arrive", "f8"),
                ("offer", "f8"), ("start", "f8"), ("end", "f8"), ("talk", "f4"), ("wrap", "f4"), ("topic", "i1"),
                ("channel", "i1"), ("followed", "b1"), ("disp", "i1"), ("session", "i4")])
# one row per offer the ACD makes, and one per customer who leaves the queue unanswered
ATT = np.dtype([("day", "i4"), ("queue", "i1"), ("session", "i4"), ("acd_contact", "i4"), ("queued", "f8"),
                ("offered", "f8"), ("ended", "f8"), ("expert", "i4"), ("result", "i1"), ("channel", "i1"),
                ("case", "i4"), ("lost", "f4")])
# results: 0 answered and connected, 1 not answered by the offered expert (re-offered on the same ACD contact),
# 2 accepted but the video session failed to connect (the customer re-queued as a new ACD contact, same session),
# 3 left the queue unanswered
SHIFT = np.dtype([("day", "i4"), ("expert", "i4"), ("start", "f8"), ("end", "f8")])
BREAK = np.dtype([("day", "i4"), ("expert", "i4"), ("start", "f8"), ("end", "f8"), ("kind", "i1")])


def simulate_2026(people, vendors):
    y = K.SEASON_CRM
    R0 = K.rng("des", y)
    staff = [e for e in people if y in e.seasons] + list(vendors)
    idx_of = {id(e): i for i, e in enumerate(staff)}
    level = {id(e): float(np.clip(R0.normal(1.0, 0.12), 0.7, 1.3)) for e in staff}
    patterns = {}
    f0, f1 = K.fortnight(y)
    vend = W.BENCH[y]["vendor"]
    nv, span, hv = vend
    v0 = f0 - dt.timedelta(7)
    topic_w_early = np.array([t[1] for t in W.TOPICS]); topic_w_late = np.array([t[2] for t in W.TOPICS])
    t_mult = np.array([t[3] for t in W.TOPICS]); a_mult = np.array([t[4] for t in W.TOPICS])
    ch_w = np.array([c[1] for c in W.CHANNELS]); ch_mult = np.array([c[2] for c in W.CHANNELS])
    lag_days = np.array([l for l, _ in W.LAGS]); lag_p = np.array([p for _, p in W.LAGS])
    recs, atts, shifts, brks, brks_taken = [], [], [], [], []
    vend_events = []                                  # ("lock", day, expert, at, hours) and ("crash", day, expert, at, hours)
    case_meta = []
    # four outsourcer agents fail their sign-in at the start of one shift and wait for a new login
    RL = K.rng("lockouts", y)
    lock_from = {}
    for i in sorted(RL.choice(len(vendors), size=4, replace=False)):
        lock_from[vendors[int(i)].emp] = (v0 + dt.timedelta(int(RL.integers(2, 16))), float(RL.uniform(0.25, 0.85)))
    lock_done = set()
    pending = {}                                      # (date, queue) -> [(case, pos, earliest hour)]
    session_no = [0]
    acd_no = [0]
    D0, D1 = K.season_open(y), K.season_close(y)
    d = D0
    while d <= D1:
        mix = topic_w_early if d.month <= 2 else topic_w_late
        mix = mix / mix.sum()
        o, c = open_hours(d, y)
        for qi, queue in enumerate(("EN", "FR")):
            # who works today, when
            on = []
            mon = K.monday(d)
            for e in staff:
                if e.queue != queue or not W.on_queue(e, d, y):
                    continue
                key = (id(e), mon)
                if key not in patterns:
                    rw = K.rng("week", e.emp, mon.toordinal())
                    if e.kind == "vendor":
                        if not (v0 <= d <= f1):
                            patterns[key] = {}
                        else:
                            patterns[key] = week_plan(rw, y, mon, hv / 3.0, 5, queue)
                    else:
                        hours, days = weekly_hours(y, e, d, level[id(e)])
                        patterns[key] = week_plan(rw, y, mon, hours, days, queue)
                plan = patterns[key]
                if d not in plan:
                    continue
                if e.kind == "expert" and e.first == y and d < e.golive:
                    continue
                length = plan[d]
                rs = K.rng("shift", e.emp, d.toordinal())
                close = 20.5 if (e.kind == "vendor" and d.weekday() == 6) else None
                s0, t_end = shift_for(rs, d, y, length, close)
                brs = breaks_for(rs, s0, t_end)
                lock = 0.0
                if e.kind == "vendor":
                    lf = lock_from.get(e.emp)
                    if lf and d >= lf[0] and e.emp not in lock_done:
                        lock = lf[1]
                        lock_done.add(e.emp)
                on.append([e, s0, t_end, brs, lock, None])
                shifts.append((d.toordinal(), idx_of[id(e)], s0, t_end))
                for b0, b1, kind in brs:
                    brks.append((d.toordinal(), idx_of[id(e)], b0, b1, 0 if kind == "Break" else 1))
            # softphone crashes among the outsourcer's agents: a few on every day they work
            vend_on = [k for k, row in enumerate(on) if row[0].kind == "vendor"]
            if vend_on:
                rc = K.rng("crashes", d.toordinal())
                want = max(3, int(rc.poisson(3.0)))
                for k in rc.permutation(vend_on):
                    if want == 0:
                        break
                    e, s0, t_end, brs, lock, _ = on[int(k)]
                    lo_, hi_ = s0 + lock + 0.4, t_end - 1.8
                    if hi_ <= lo_:
                        continue
                    for _try in range(6):
                        ca = lo_ + float(rc.random()) * (hi_ - lo_)
                        if all(not (ca - 0.1 <= b0 <= ca + 1.85) for b0, _b1, _k in brs):
                            on[int(k)][5] = ca
                            want -= 1
                            break
            if not on:
                continue
            # arrivals: new cases on the profile, follow-ups due today (each day's draws on their own streams, so the
            # demand a day brings does not depend on how the queue served the days before it)
            RA = K.rng("arrivals", y, d.toordinal(), qi)
            R = K.rng("service", y, d.toordinal(), qi)
            lam = W.demand_curve(d, y, W.SCALE[y], queue) * float(np.exp(RA.normal(0, 0.05)))
            n_new = int(RA.poisson(lam))
            w = intraday_weights(d, y)
            hrs = RA.choice(len(w), size=n_new, p=w)
            arr_t = o + hrs + RA.random(n_new)
            events = []                               # (time, seq, kind, payload)
            seq = 0
            for t in arr_t:
                events.append((float(t), seq, "arrive", (-1, 1, None, 0, None, None))); seq += 1
            for (case, pos, earliest) in pending.pop((d, queue), []):
                t = max(earliest, o + float(RA.choice(len(w), p=w)) + float(RA.random()))
                events.append((min(t, c - 0.05), seq, "arrive", (case, pos, None, 0, None, None))); seq += 1
            for e, s0, t_end, brs, lock, crash in on:
                events.append((s0 + lock, seq, "free", (idx_of[id(e)],))); seq += 1
                if lock:
                    vend_events.append(("lock", d.toordinal(), idx_of[id(e)], s0, lock))
            events.append((c, seq, "close", ())); seq += 1
            heapq.heapify(events)
            ex_state = {}
            for e, s0, t_end, brs, lock, crash in on:
                ex_state[idx_of[id(e)]] = dict(e=e, start=s0, end=t_end, breaks=list(brs), busy_until=s0 + lock,
                                               since=s0, crash_at=crash, ghost_until=-1.0)
            free = {}                                  # expert -> idle since
            free_heap = []                             # (idle since, expert), lazily cleaned
            queue_wait = []                            # FIFO of (arrival time, key), lazily cleaned
            waiting = {}                               # key -> (arrival time, payload, patience deadline)
            day_ord = d.toordinal()

            def take_break_or_free(xi, t):
                st = ex_state[xi]
                if t >= st["end"] - 1e-9:
                    return
                if st["crash_at"] is not None and t >= st["crash_at"] - 1e-9:
                    # the softphone freezes as the agent goes ready; they restart it and sign in again
                    st["crash_at"] = None
                    clear = t <= st["end"] - 1.6 and all(not (t - 0.05 <= b0 <= t + 1.6) for b0, _b1, _k in st["breaks"])
                    if not clear and t + 0.4 <= st["end"] - 1.65:
                        st["crash_at"] = t + 0.4
                    if clear:
                        gap = float(K.rng("relogin", xi, day_ord).uniform(1.0, 4.0)) / 60
                        vend_events.append(("crash", day_ord, xi, t, gap))
                        st["busy_until"] = t + gap
                        st["ghost_until"] = t + 1.55
                        heapq.heappush(events, (t + gap, next_seq(), "free", (xi,)))
                        return
                for b in list(st["breaks"]):
                    b0, b1, kind = b
                    if b0 <= t + 1e-9:
                        st["breaks"].remove(b)
                        dur = b1 - b0
                        st["busy_until"] = t + dur
                        brks_taken.append((day_ord, xi, t, t + dur, 0 if kind == "Break" else 1))
                        heapq.heappush(events, (t + dur, next_seq(), "free", (xi,)))
                        return
                free[xi] = t
                heapq.heappush(free_heap, (t, xi))

            seq_box = [seq]

            def pop_free():
                while free_heap:
                    since, xi = heapq.heappop(free_heap)
                    if free.get(xi) == since:
                        del free[xi]
                        return xi
                return None

            def next_seq():
                seq_box[0] += 1
                return seq_box[0]

            def offer(t):
                """Offer waiting customers to free experts, the longest-waiting customer to the longest-idle expert."""
                while queue_wait and free:
                    a_t, key = queue_wait[0]
                    if key not in waiting:
                        heapq.heappop(queue_wait)
                        continue
                    xi = pop_free()
                    if xi is None:
                        break
                    heapq.heappop(queue_wait)
                    _a, payload, _p = waiting.pop(key)
                    serve(xi, t, a_t, payload)

            def abandon(t, payload, retry=True):
                """The customer leaves the queue at t; they try again later today or tomorrow, as a new session."""
                case, pos, sess, tries, acd, queued = payload
                atts.append((day_ord, qi, sess, acd, queued, np.nan, t, -1, 3, -1, case, 0.0))
                if retry and tries < 3:
                    back = t + float(R.uniform(0.25, 1.5))
                    if back < c - 0.3:
                        heapq.heappush(events, (back, next_seq(), "arrive", (case, pos, None, tries + 1, None, None)))
                    else:
                        pending.setdefault((d + dt.timedelta(1), queue), []).append((case, pos, 0.0))
                elif not retry:
                    pending.setdefault((d + dt.timedelta(1), queue), []).append((case, pos, 0.0))

            def serve(xi, t, a_t, payload):
                case, pos, sess, tries, acd, queued = payload
                st = ex_state[xi]
                e = st["e"]
                first_offer = t
                # redirect on no answer: the offered expert misses it, the ACD offers the same contact to the next
                missed = R.random() < 0.035
                if missed and free and t >= st.get("ghost_until", -1.0):
                    miss = t + 15 / 3600
                    atts.append((day_ord, qi, sess, acd, queued, t, miss, xi, 1, -1, case, 0.0))
                    st["busy_until"] = t + 75 / 3600
                    heapq.heappush(events, (t + 75 / 3600, next_seq(), "free", (xi,)))
                    xi2 = pop_free()
                    xi, st, e = xi2, ex_state[xi2], ex_state[xi2]["e"]
                    queued = miss
                    t = miss + 3 / 3600
                if case < 0:
                    topic = int(R.choice(len(W.TOPICS), p=mix))
                    channel = int(R.choice(3, p=ch_w))
                    case_meta.append((topic, channel, qi))
                    case = len(case_meta) - 1
                else:
                    topic, channel, _ = case_meta[case]
                    if R.random() < 0.2:
                        channel = int(R.choice(3, p=ch_w))
                # a video session can fail to connect after the expert accepts: the ACD queues the customer again
                # as a new contact on the same session; nothing reaches the CRM
                vfail = R.random() < 0.025
                if channel == 0 and vfail and t < c - 0.1:
                    lost = float(R.uniform(60, 150)) / 3600
                    atts.append((day_ord, qi, sess, acd, queued, t, t, xi, 2, channel, case, lost))
                    st["busy_until"] = t + lost
                    heapq.heappush(events, (t + lost, next_seq(), "free", (xi,)))
                    acd_no[0] += 1
                    back = t + float(R.uniform(20, 60)) / 3600
                    heapq.heappush(events, (back, next_seq(), "requeue", (case, pos, sess, tries, acd_no[0], back,
                                                                          a_t)))
                    return
                mins = W.handle_minutes(e, d, y) * a_mult[topic] * ch_mult[channel]
                hmin = mins * float(np.exp(R.normal(-W.PAR["contact_sd"] ** 2 / 2, W.PAR["contact_sd"])))
                hsec = max(90.0, hmin * 60.0)
                wrap = hsec * float(np.clip(R.normal(0.17, 0.05), 0.04, 0.35))
                pf = W.follow_chance(e, d, y)
                chance = (pf if pos == 1 else W.PAR["q"]) * t_mult[topic]
                fol = bool(R.random() < chance)
                end = t + hsec / 3600
                if fol:
                    lag = int(R.choice(lag_days, p=lag_p))
                    if lag == 0:
                        back = end + float(R.uniform(0.25, 2.5))
                        if back < c - 0.3:
                            heapq.heappush(events, (back, next_seq(), "arrive", (case, pos + 1, None, 0, None, None)))
                        else:
                            pending.setdefault((d + dt.timedelta(1), queue), []).append((case, pos + 1, 0.0))
                    else:
                        nd = d + dt.timedelta(lag)
                        if nd <= D1:
                            pending.setdefault((nd, queue), []).append((case, pos + 1, 0.0))
                        else:
                            fol = False
                rd = R.random()
                new_hand = e.kind == "vendor" or e.first == y
                if not fol:
                    disp = 0 if rd < 0.91 else (1 if rd < 0.96 else (2 if rd < 0.985 else 3))
                else:
                    cut = 0.70 if new_hand else 0.56
                    disp = 0 if rd < cut else (1 if rd < cut + 0.24 else (2 if rd < cut + 0.33 else 3))
                atts.append((day_ord, qi, sess, acd, queued, t, t, xi, 0, channel, case, 0.0))
                recs.append((day_ord, qi, case, pos, xi, a_t, first_offer, t, end, hsec - wrap, wrap, topic, channel,
                             fol, disp, sess))
                st["busy_until"] = end
                heapq.heappush(events, (end, next_seq(), "free", (xi,)))

            clock = 0.0
            while events:
                t, _, kind, payload = heapq.heappop(events)
                assert t >= clock - 1e-9, "event out of order"
                clock = t
                if kind in ("arrive", "requeue"):
                    if kind == "arrive":
                        case, pos, sess, tries, acd, queued = payload
                        if t >= c:
                            pending.setdefault((d + dt.timedelta(1), queue), []).append((case, pos, 0.0))
                            continue
                        session_no[0] += 1
                        acd_no[0] += 1
                        payload = (case, pos, session_no[0], tries, acd_no[0], t)
                        a_first = t
                        patience = t + float(R.exponential(0.45)) + 0.05
                    else:
                        # a customer queued again after a failed video waits at the head of the queue for an expert
                        case, pos, sess, tries, acd, queued, a_first = payload
                        payload = (case, pos, sess, tries, acd, queued)
                        _draw = float(R.exponential(0.45))
                        patience = t + 12.0
                    key = next_seq()
                    waiting[key] = (a_first, payload, patience)
                    heapq.heappush(queue_wait, (a_first, key))
                    heapq.heappush(events, (patience, next_seq(), "patience", (key,)))
                elif kind == "patience":
                    key = payload[0]
                    if key in waiting:
                        _a, pl, _p = waiting.pop(key)
                        abandon(t, pl)
                    continue
                elif kind == "close":
                    # whoever is still waiting when the queue closes is asked to come back tomorrow
                    for key in sorted(waiting):
                        _a, pl, _p = waiting[key]
                        abandon(t, pl, retry=False)
                    waiting.clear()
                    queue_wait.clear()
                    continue
                else:
                    xi = payload[0]
                    if xi in free or t < ex_state[xi]["busy_until"] - 1e-9:
                        continue
                    take_break_or_free(xi, t)
                offer(t)
        d += dt.timedelta(1)
    return (np.array(recs, dtype=REC), np.array(atts, dtype=ATT), np.array(shifts, dtype=SHIFT),
            np.array(brks_taken, dtype=BREAK), staff, case_meta, vend_events)
