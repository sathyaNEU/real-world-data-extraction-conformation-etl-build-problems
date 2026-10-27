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


def month_ym(j):
    """(year, month) of month index j, months since January 2021 (negative before it)."""
    return K.D0.year + j // 12, j % 12 + 1


def grant_shape(code, T):
    """Review grants a month at unit scale, from the site's launch to December 2027, keyed by month index: they ramp
    up over the site's first two years and follow the site's question level (the reputation that earns access comes
    from answering); from 1 September 2026 access is by moderator invitation only, a trickle."""
    L = (LAUNCH[code][0] - K.D0.year) * 12 + LAUNCH[code][1] - 1
    closed = K.month_index(K.INVITE_ONLY.year, K.INVITE_ONLY.month)
    out = {}
    for t in range(L, T):
        y, m = month_ym(t)
        lv = _level(dt.date(y, m, 15), K.SITE[code]["drop"])
        ramp = min(1.0, (t - L + 1) / K.GRANT_RAMP_M)
        out[t] = ramp * lv ** K.GRANT_ELASTICITY * (K.INVITE_SHARE if t >= closed else 1.0)
    return out


def expected_pool(shape):
    """Expected active reviewers a month at unit scale, casual and steady reviewers carried at their own stop rates."""
    c = v = 0.0
    out = {}
    for t in sorted(shape):
        c = c * (1.0 - K.STOP_CASUAL) + shape[t] * K.CASUAL_SHARE
        v = v * (1.0 - K.STOP_STEADY) + shape[t] * (1.0 - K.CASUAL_SHARE)
        out[t] = c + v
    return out


def _reviewers(code, scale, shape, T):
    """The volunteer pool month by month from the site's launch to December 2027.

    Each new reviewer is casual (CASUAL_SHARE of grants) or steady, and stops for good after any month with that type's
    own monthly chance; nobody's chance changes with time, so the pool's overall stop rate falls only as its casual
    reviewers leave first. Review grants a month are the Poisson count at scale times the site's grant shape, read at a
    fixed quantile per month; each reviewer's type, pace, months active and monthly activity come from their own
    stream, so a change of scale adds or removes reviewers at the margin and leaves everyone else as they were. A
    reviewer granted in a month is active from that month; one who stops after month t made a last review in t."""
    from scipy.stats import poisson
    kap_mu = math.log(K.KAPPA) - K.KAPPA_SIG ** 2 / 2.0
    months_ = sorted(shape)
    u = K.rng("grants", code).random(len(months_))
    kappa, join, last, stop, acts = [], [], [], [], []
    for t, ut in zip(months_, u):
        lam = scale * shape[t]
        n_in = int(poisson.ppf(ut, lam)) if lam > 0 else 0
        for k in range(n_in):
            rr = K.rng("reviewer", code, t, k)
            casual = rr.random() < K.CASUAL_SHARE
            th = K.STOP_CASUAL if casual else K.STOP_STEADY
            life = int(rr.geometric(th))
            kappa.append(float(rr.lognormal(kap_mu, K.KAPPA_SIG)))
            stop.append(th)
            join.append(t)
            end = t + life - 1
            last.append(end if end < T else None)
            span = min(end, T - 1) - t + 1
            acts.append(rr.gamma(K.ACT_SHAPE, 1.0 / K.ACT_SHAPE, size=max(span, 0)))
    act_ids = {t: [] for t in range(T)}
    act_g = {t: [] for t in range(T)}
    for i, (j, L, g) in enumerate(zip(join, last, acts)):
        hi = (T - 1) if L is None else L
        for t in range(max(j, 0), hi + 1):
            act_ids[t].append(i)
            act_g[t].append(g[t - j])
    act = {t: (np.array(act_ids[t], dtype=np.int64), np.array(act_g[t])) for t in range(T)}
    return dict(kappa=np.array(kappa), join=join, last=last, stop=np.array(stop), act=act)


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
        # the reviewer pool, its grants scaled so January to September 2026 cover hits the site's target
        A_m = np.zeros(T)
        for di, d in enumerate(W.all_days):
            A_m[K.month_index(d.year, d.month)] += sum(S.items[t][di] for t in K.ITEMS)
        months26 = [K.month_index(2026, m) for m in range(1, 10)]
        shape = grant_shape(code, T)
        ep = expected_pool(shape)
        S.scale = K.SITE[code]["cover"] * A_m[months26].sum() / (K.KAPPA * sum(ep[t] for t in months26))
        S.pool = _reviewers(code, S.scale, shape, T)
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
