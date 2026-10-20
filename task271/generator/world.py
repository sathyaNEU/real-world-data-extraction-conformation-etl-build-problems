"""The truth: each sampled member's work in March 2026 and the calls that did or did not reach them.

The core (classes, call plans, each call's window and whether it reached the member) is drawn first from one stream,
exactly as the design search drew it, so the searched world is the built world. Every detail the files carry (dates
and times, ages, identifiers, noncontact results, agents, interview answers, the member services centre's other
outreach, the vendor's pilot calls) comes from separate streams that never touch the core."""
import datetime as dt

import numpy as np

import common as K
import core as C


def _logit(p):
    return np.log(p / (1 - p))


def core_draw(D, seed, n=K.N_PER_REGION):
    """cases: (cid, region, age band, sex, class, outcome, reaching call, planned calls, member services first, late);
    calls: (cid, attempt, centre 0 member services or 1 vendor, window 0 day 1 evening 2 Saturday, reached)."""
    r = np.random.default_rng(seed)
    cases, calls = [], []
    cid = 0
    for ri in range(10):
        for i in range(n):
            a = r.choice(3, p=[s for s, _ in C.AGE])
            s = r.choice(2, p=[s for s, _ in C.SEX])
            y = int(r.random() < 1 / (1 + np.exp(-(_logit(D["pi"][ri]) + C.AGE[a][1] + C.SEX[s][1]))))
            late = r.random() < D["late"][ri]
            msc_first = r.random() < D["msc"][ri]
            if msc_first:
                nm = 4 if late else 6
                tr = r.random() < D["transfer"][ri]
                nv = (max(1, D["vcalls"][ri] - (1 if late else 0))) if tr else 0
                plan = [("M", 0)] * nm + [("V", None)] * nv
            else:
                plan = [("V", None)] * (6 if late else 8)
            out, k_hit = 0, 0
            for k, (ctr, w) in enumerate(plan, 1):
                if w is None:
                    if msc_first:
                        w = r.choice(3, p=[0.20, 0.50, 0.30])
                    elif k == 1:
                        w = r.choice(3, p=[0.45, 0.40, 0.15])
                    else:
                        w = r.choice(3, p=[0.30, 0.45, 0.25])
                hit = r.random() < (C.P1 if y else C.P0)[w]
                calls.append((cid, k, 0 if ctr == "M" else 1, w, int(hit)))
                if hit:
                    k_hit = k
                    out = 2 if r.random() < C.RHO else 1
                    break
            cases.append((cid, ri, a, s, y, out, k_hit, len(plan), int(msc_first), int(late)))
            cid += 1
    return np.array(cases), np.array(calls)


def _business_days(start, end):
    d = start
    out = []
    while d <= end:
        if d.weekday() < 5 and d not in K.HOLIDAYS:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


BUSINESS = _business_days(dt.date(2026, 4, 13), K.FIELD_CLOSE)
SATURDAYS = [d for d in (dt.date(2026, 4, 18) + dt.timedelta(days=7 * i) for i in range(7)) if d <= K.FIELD_CLOSE]


def _next_day(after, window):
    """The first calling day on or after `after` for the window."""
    pool = SATURDAYS if window == 2 else BUSINESS
    for d in pool:
        if d >= after:
            return d
    return None


def _time(r, window, after=None):
    """A time in the window's shift, later than `after` (a time of day) by an hour when given; None if none fits."""
    (h0, m0), (h1, m1) = K.SHIFTS[K.WINDOWS[window]]
    lo, hi = h0 * 60 + m0, h1 * 60 + m1
    if after is not None:
        lo = max(lo, after.hour * 60 + after.minute + 60)
        if lo >= hi:
            return None
    mins = int(r.integers(lo, hi))
    return dt.time(mins // 60, mins % 60, int(r.integers(0, 60)))


def _fit(r, plan, start, late, tight):
    """Dates and times for one case's calls from `start`, or None when they cannot all be made by field close. A
    tight fit spaces the calls a day apart and lets the vendor's dialer retry later the same day."""
    day = start
    out = []
    prev_ctr = None
    for (ctr, win) in plan:
        kind = 2 if (ctr == 1 and win == 2) else 0
        shift = win if ctr == 1 else 0
        placed = None
        if prev_ctr == 0 and ctr == 1:
            day = day + dt.timedelta(days=1)          # the transfer, then the vendor's first call
        elif tight and prev_ctr == 1 and ctr == 1 and (out[-1].weekday() == 5) == (kind == 2):
            t = _time(r, shift, after=out[-1].time())
            if t is not None:
                placed = dt.datetime.combine(out[-1].date(), t)
        if placed is None:
            d = _next_day(day, kind)
            if d is None or d > K.FIELD_CLOSE:
                return None
            placed = dt.datetime.combine(d, _time(r, shift))
        out.append(placed)
        day = placed.date() + dt.timedelta(days=1 if tight else int(r.integers(1, 3 if late else 4)))
        prev_ctr = ctr
    return out


def schedule(cases, calls, seed):
    """Dates and times for every call, consistent with the centre, the window and the release. A case whose calls do
    not fit its release's calendar at the usual spacing is called at a day's spacing, then from its release's first
    day, then from the earlier release of its group (early or late)."""
    r = np.random.default_rng(seed + 11)
    by_case = {}
    for row in calls:
        by_case.setdefault(int(row[0]), []).append(row)
    wave = {}
    sched = {}
    for c in cases:
        cid, late = int(c[0]), int(c[9])
        plan = [(int(ctr), int(win)) for (_, k, ctr, win, hit) in by_case[cid]]
        w_ix = int(r.integers(2, 4)) if late else int(r.integers(0, 2))
        offset = int(r.integers(0, 3))
        tries = [(w_ix, offset, False), (w_ix, offset, True), (w_ix, 0, True), (w_ix - 1 if w_ix in (1, 3) else w_ix, 0, True)]
        for (wx, off, tight) in tries:
            got = _fit(r, plan, K.WAVES[wx] + dt.timedelta(days=off), late, tight)
            if got is not None:
                break
        if got is None:
            raise RuntimeError("calls past field close for case %d" % cid)
        wave[cid] = wx
        sched[cid] = got
    return wave, sched


def details(cases, seed):
    """Ages, languages, identifiers, and the interview answers of the members who completed."""
    r = np.random.default_rng(seed + 21)
    n = len(cases)
    lo, hi = [19, 30, 45], [29, 44, 64]
    age = np.array([int(r.integers(lo[a], hi[a] + 1)) for a in cases[:, 2]])
    langs = ["English", "Spanish", "Russian", "Vietnamese", "Somali", "Other"]
    lang = [langs[i] for i in r.choice(6, size=n, p=[0.852, 0.10, 0.02, 0.014, 0.009, 0.005])]
    member = ["P%09d" % v for v in r.choice(np.arange(100_000_000, 999_999_999), size=n, replace=False)]
    case_no = ["MW26-%05d" % v for v in r.permutation(np.arange(10_001, 10_001 + n))]
    hours = []
    for c in cases:
        y = int(c[4])
        if y:
            tot = int(r.integers(150, 186)) if r.random() < 0.7 else int(r.integers(80, 150))
        else:
            tot = 0 if r.random() < 0.62 else int(r.integers(4, 80))
        nj = 0 if tot == 0 else (1 if r.random() < 0.8 else (2 if r.random() < 0.85 else 3))
        if nj == 0:
            jobs = []
        elif nj == 1:
            jobs = [tot]
        else:
            cuts = sorted(r.choice(np.arange(1, tot), size=nj - 1, replace=False).tolist()) if tot > nj else []
            parts = np.diff([0] + cuts + [tot]).tolist() if cuts else [tot]
            jobs = [int(x) for x in parts]
        kinds = [("employee" if r.random() < 0.82 else ("self-employed" if r.random() < 0.6 else "app-based gig"))
                 for _ in jobs]
        look = "" if tot >= 80 else ("Yes" if r.random() < 0.38 else "No")
        limit = "Yes" if r.random() < 0.21 else "No"
        help_ = "Yes" if r.random() < 0.33 else "No"
        hours.append(dict(total=tot, jobs=jobs, kinds=kinds, looking=look, health_limits=limit, wants_help=help_))
    return dict(age=age, lang=lang, member=member, case_no=case_no, hours=hours)


def noncontact_results(calls, seed):
    """What a call that did not reach the member recorded: voicemail, no answer, busy or another person."""
    r = np.random.default_rng(seed + 31)
    codes = [3140, 3130, 3150, 2320]
    return [int(codes[i]) for i in r.choice(4, size=len(calls), p=[0.52, 0.33, 0.05, 0.10])]


def key_answers(cases, seed):
    """Whether a member who declined the interview answered the one key question; drawn for every case from its own
    stream and read for the members who declined."""
    return np.random.default_rng(seed + 81).random(len(cases)) < C.KEYQ


def world(seed=None, design=None):
    seed = C.SEED if seed is None else seed
    D = C.DESIGN if design is None else design
    cases, calls = core_draw(D, seed)
    wave, sched = schedule(cases, calls, seed)
    det = details(cases, seed)
    nc = noncontact_results(calls, seed)
    key = key_answers(cases, seed)
    return dict(seed=seed, design=D, cases=cases, calls=calls, wave=wave, sched=sched, det=det, noncontact=nc, key=key)


def histories(w):
    """The model's input from the truth: each case's calls up to the one that reached the member."""
    by = {}
    for row in w["calls"]:
        by.setdefault(int(row[0]), []).append(row)
    hist = []
    for c in w["cases"]:
        cid = int(c[0])
        out = int(c[5])
        y = int(c[4]) if (out == 1 or (out == 2 and w["key"][cid])) else -1
        cl = [((0 if ctr == 0 else 1 + win), k) for (_, k, ctr, win, hit) in by[cid]]
        hist.append((int(c[1]), int(c[2]), int(c[3]), y, out, cl))
    return hist
