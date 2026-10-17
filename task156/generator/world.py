"""task156 world: the truth before any export layout, mess or document.

Every site's daily questions, its review-inbox items by type and its moderator flags; its volunteer reviewer pool
(each reviewer's own pace, monthly activity, join month and last month); its daily volunteer capacity; and the
72-hour hand-off run day by day (oldest item first), which decides which items the volunteers review and which reach
the paid team. The forward year (2027) is run the same way on the planning team's question plan, for the truth
column only: the golden is computed from the shipped files (calc.py), never from this module."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K


LAUNCH = {"web": (2012, 3), "mobile": (2012, 9), "data": (2014, 4), "databases": (2012, 11), "devops": (2013, 6),
          "gamedev": (2013, 2), "security": (2013, 10), "embedded": (2015, 5), "scicomp": (2016, 1)}
FLAG_CLOSED_SHARE = 0.062      # flags the platform closes because the post was deleted before a moderator acted


class Site:
    pass


class World:
    pass


def _level(d, drop):
    x = (K.month_frac(d) - K.month_frac(K.AI_MID)) / K.AI_WIDTH_M
    lv = 1.0 - drop * K.logistic(x)
    if d >= K.DRIFT_FROM:
        lv *= K.DRIFT_PER_YEAR ** ((d - K.DRIFT_FROM).days / 365.25)
    return lv


def _site_rates(code):
    r = K.rng("rates", code)
    item = {t: K.ITEM_RATE[t] * float(r.uniform(0.90, 1.10)) for t in K.ITEMS}
    flag = K.FLAG_RATE * float(r.uniform(0.88, 1.14))
    return item, flag


def expected_month_questions(code, y, m, base):
    mid = dt.date(y, m, 15)
    return base * _level(mid, K.SITE[code]["drop"]) * K.SEAS[m]


def _base(code):
    """Base volume so the January to September 2026 monthly mean is the site's q26."""
    lv = [_level(dt.date(2026, m, 15), K.SITE[code]["drop"]) * K.SEAS[m] for m in range(1, 10)]
    return K.SITE[code]["q26"] / (sum(lv) / 9.0)


def plan_2027(code, base):
    """The planning team's monthly question plan: the volume shape carried into 2027, rounded to tens."""
    return {m: int(K.round_half_up(expected_month_questions(code, 2027, m, base), -1)) for m in range(1, 13)}


def outlook_q4_2026(code, base):
    """The planning team's outlook for October to December 2026, issued with the plan."""
    return {m: int(K.round_half_up(expected_month_questions(code, 2026, m, base), -1)) for m in (10, 11, 12)}


def _daily_questions(code, base, hist_days, plan):
    r = K.rng("questions", code)
    out = {}
    by_month = {}
    for d in hist_days:
        by_month.setdefault((d.year, d.month), []).append(d)
    for (y, m), ds in by_month.items():
        if y == 2027:
            total = plan[m]
        else:
            total = expected_month_questions(code, y, m, base)
        wsum = sum(K.WD_Q[d.weekday()] for d in ds)
        for d in ds:
            lam = total * K.WD_Q[d.weekday()] / wsum
            if (d.month, d.day) in ((12, 25), (1, 1)):
                lam *= 0.62
            lam *= math.exp(float(r.normal(0.0, 0.022)))
            out[d] = int(r.poisson(lam)) if y < 2027 else lam
    return out


def _reviewers(code, R0, T):
    """The volunteer pool month by month over 2021-01 to 2027-12 (T months).

    Every reviewer stops at the same monthly rate (CHURN); exits are drawn uniformly among the reviewers active that
    month. The number leaving each month is CHURN times the month's pool with a small month-to-month swing that sums
    to zero over each calendar quarter, so the exit rate read over any whole quarters equals CHURN. New reviewers
    arrive at the old steady inflow until the reputation pipeline dries up in the autumn of 2024, then at a trickle."""
    r = K.rng("reviewers", code)
    kap_mu = math.log(K.KAPPA) - K.KAPPA_SIG ** 2 / 2.0
    kappa, join, last, granted = [], [], [], []
    active = []
    # the pool on 1 January 2021: tenure memoryless, access granted up to eight years earlier
    age = (K.D0.year - LAUNCH[code][0]) * 12 + (K.D0.month - LAUNCH[code][1])
    for i in range(int(round(R0))):
        kappa.append(float(r.lognormal(kap_mu, K.KAPPA_SIG)))
        join.append(-1)
        last.append(None)
        ten = int(r.exponential(1.0 / K.CHURN))
        if ten >= age - 2:
            ten = int(r.integers(0, max(1, age - 2)))
        granted.append(ten)
        active.append(i)
    inflow0 = K.CHURN * R0
    pipe_mid = K.month_frac(K.PIPE_MID)
    swing = None
    in_swing = [0.0, 0.0, 0.0]
    act = {}
    for t in range(T):
        y, m = K.D0.year + t // 12, t % 12 + 1
        x = (t + 0.5 - pipe_mid) / K.PIPE_WIDTH_M
        lam = inflow0 * (1.0 - (1.0 - K.PIPE_FLOOR) * K.logistic(x))
        if t % 3 == 0:
            b1, b2 = float(r.uniform(-0.12, 0.12)), float(r.uniform(-0.12, 0.12))
            in_swing = [b1, b2, -(b1 + b2)]
        n_in = int(r.poisson(lam)) if lam < 3.0 else int(K.round_half_up(lam * (1.0 + in_swing[t % 3])))
        for _ in range(n_in):
            i = len(kappa)
            kappa.append(float(r.lognormal(kap_mu, K.KAPPA_SIG)))
            join.append(t)
            last.append(None)
            granted.append(-1)
            active.append(i)
        n = len(active)
        g = r.gamma(K.ACT_SHAPE, 1.0 / K.ACT_SHAPE, size=n)
        act[t] = (np.array(active, dtype=np.int64), g)
        if t % 3 == 0:
            a1, a2 = float(r.uniform(-0.13, 0.13)), float(r.uniform(-0.13, 0.13))
            swing = [a1, a2, -(a1 + a2)]
        e = int(K.round_half_up(K.CHURN * n * (1.0 + swing[t % 3])))
        e = max(0, min(e, n))
        idx = r.choice(n, size=e, replace=False) if e else np.array([], dtype=np.int64)
        gone = set(int(active[j]) for j in idx)
        for i in gone:
            last[i] = t
        active = [i for i in active if i not in gone]
    return dict(kappa=np.array(kappa), join=join, last=last, granted=granted, act=act)


def _capacity(pool, T):
    kap = pool["kappa"]
    Km, Rm = np.zeros(T), np.zeros(T)
    for t in range(T):
        ids, g = pool["act"][t]
        Km[t] = float((kap[ids] * g).sum())
        Rm[t] = len(ids)
    return Km, Rm


def _fifo(code, all_days, items, Kday):
    """The 72-hour hand-off, day by day. Items entering on day d can be reviewed on d, d+1 and d+2, oldest first;
    whatever is left at the end of d+2 (and the share no volunteer ever picks up) reaches the paid team."""
    r = K.rng("skip", code)
    queue = []                       # [entry day index, {type: reviewable count}]
    rev = {t: np.zeros(len(all_days)) for t in K.ITEMS}
    rout = {t: np.zeros(len(all_days)) for t in K.ITEMS}
    reviewed_on = np.zeros(len(all_days))
    for di, d in enumerate(all_days):
        today = {}
        for t in K.ITEMS:
            n = items[t][di]
            sk = int(r.binomial(n, K.SKIP_BY_TYPE[t])) if n > 0 else 0
            rout[t][di] += sk
            today[t] = float(n - sk)
        queue.append([di, today])
        cap = Kday[di]
        for c in queue:
            tot = sum(c[1].values())
            if tot <= 0 or cap <= 0:
                continue
            take = min(cap, tot)
            f = take / tot
            for t in K.ITEMS:
                x = c[1][t] * f
                rev[t][c[0]] += x
                c[1][t] -= x
            cap -= take
            reviewed_on[di] += take
        keep = []
        for c in queue:
            if di - c[0] >= K.HANDOFF_DAYS - 1:
                for t in K.ITEMS:
                    rout[t][c[0]] += c[1][t]
            else:
                keep.append(c)
        queue = keep
    return rev, rout, reviewed_on


def simulate():
    W = World()
    W.all_days = K.days(K.D0, K.D_END)
    W.hist_days = [d for d in W.all_days if d <= K.HIST_END]
    W.day_index = {d: i for i, d in enumerate(W.all_days)}
    T = len(K.months(K.D0, K.D_END))
    W.T = T
    W.sites = {}
    for code in K.SITES:
        S = Site()
        S.code = code
        S.item_rate, S.flag_rate = _site_rates(code)
        S.base = _base(code)
        S.plan = plan_2027(code, S.base)
        S.outlook = outlook_q4_2026(code, S.base)
        q = _daily_questions(code, S.base, W.all_days, S.plan)
        S.q = np.array([q[d] for d in W.all_days], dtype=float)
        # inbox items and flags by day
        r = K.rng("items", code)
        S.items = {}
        for t in K.ITEMS:
            lam = S.q * S.item_rate[t]
            if t == "edit":
                lam = lam * np.array([1.0 if d >= K.EDIT_QUEUE_START else 0.0 for d in W.all_days])
            S.items[t] = r.poisson(lam).astype(float)
        rf = K.rng("flags", code)
        S.flags = rf.poisson(S.q * S.flag_rate).astype(float)
        rc = K.rng("flagclosed", code)
        S.flag_closed = rc.binomial(S.flags.astype(np.int64), FLAG_CLOSED_SHARE).astype(float)
        # the reviewer pool, sized so January to September 2026 cover hits the site's target
        A_m = np.zeros(T)
        for di, d in enumerate(W.all_days):
            A_m[K.month_index(d.year, d.month)] += sum(S.items[t][di] for t in K.ITEMS)
        months26 = [K.month_index(2026, m) for m in range(1, 10)]
        pr = []
        rr = 1.0
        pipe_mid = K.month_frac(K.PIPE_MID)
        for t in range(T):
            x = (t + 0.5 - pipe_mid) / K.PIPE_WIDTH_M
            inflow = K.CHURN * (1.0 - (1.0 - K.PIPE_FLOOR) * K.logistic(x))
            rr = rr + inflow - K.CHURN * rr
            pr.append(rr)
        pr = np.array(pr)
        R0 = K.SITE[code]["cover"] * A_m[months26].sum() / (K.KAPPA * pr[months26].sum())
        S.R0 = R0
        S.pool = _reviewers(code, R0, T)
        S.Km, S.Rm = _capacity(S.pool, T)
        # daily capacity
        rk = K.rng("capday", code)
        Kday = np.zeros(len(W.all_days))
        mdays = {}
        for di, d in enumerate(W.all_days):
            mdays.setdefault(K.month_index(d.year, d.month), []).append(di)
        for t, dis in mdays.items():
            ws = sum(K.WD_K[W.all_days[di].weekday()] for di in dis)
            for di in dis:
                Kday[di] = S.Km[t] * K.WD_K[W.all_days[di].weekday()] / ws * math.exp(float(rk.normal(0.0, 0.05)))
        S.Kday = Kday
        S.rev, S.rout, S.reviewed_on = _fifo(code, W.all_days, S.items, Kday)
        W.sites[code] = S
    return W


# ------------------------------------------------------------------------------------------------- aggregates
def monthly(W, code, field):
    """Monthly totals by entry (or raise) month over 2021-01 to 2027-12 for one site."""
    S = W.sites[code]
    out = np.zeros(W.T)
    for di, d in enumerate(W.all_days):
        t = K.month_index(d.year, d.month)
        if field == "q":
            out[t] += S.q[di]
        elif field == "flags":
            out[t] += S.flags[di]
        elif field == "flags_handled":
            out[t] += S.flags[di] - S.flag_closed[di]
        elif field == "entered":
            out[t] += sum(S.items[x][di] for x in K.ITEMS)
        elif field == "reviewed":
            out[t] += sum(S.rev[x][di] for x in K.ITEMS)
        elif field == "routed":
            out[t] += sum(S.rout[x][di] for x in K.ITEMS)
        elif field == "reviewed_on":
            out[t] += S.reviewed_on[di]
        elif field.startswith("routed:"):
            out[t] += S.rout[field.split(":")[1]][di]
        elif field.startswith("entered:"):
            out[t] += S.items[field.split(":")[1]][di]
    return out


def paid_hours_month(W, code, std):
    S = W.sites[code]
    out = np.zeros(W.T)
    for di, d in enumerate(W.all_days):
        t = K.month_index(d.year, d.month)
        out[t] += (S.flags[di] - S.flag_closed[di]) * std["flag"] + sum(S.rout[x][di] * std[x] for x in K.ITEMS)
    return out / 60.0
