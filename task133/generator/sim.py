"""The simulated truth: every Bellbird personal loan from go-live in October 2019 to the reporting date, instalment
by instalment. Each repayment falls due on the borrower's repayment day (the next business day when that is a weekend
or NSW public holiday); each instalment has the date it was made good: on time, a few days late, caught up with a later
instalment, capitalised when a hardship arrangement started, or never, in a run that ends in default. Days past due,
balances (interest accrued daily, charged on each repayment date), defaults, write-offs and recoveries all follow."""
import datetime as dt
import math

import numpy as np

import world as W

EPOCH = dt.date(2019, 1, 1)
BIG = 10 ** 7
J = 66                      # instalment slots: a 60-month term plus six months of post-maturity arrears
REASONS = ["Unemployment", "Reduced income", "Illness or injury", "Relationship breakdown", "Increased expenses", "Other"]
REASON_P = [0.24, 0.30, 0.17, 0.08, 0.14, 0.07]


def dn(d):
    return (d - EPOCH).days


def dd(n):
    return EPOCH + dt.timedelta(days=int(n))


class Calendar:
    def __init__(self, last=dt.date(2034, 12, 31)):
        n = dn(last) + 1
        hol = set()
        for y in range(EPOCH.year, last.year + 1):
            hol |= W.nsw_holidays(y)
        self.hol = hol
        days = [EPOCH + dt.timedelta(days=i) for i in range(n)]
        self.is_bd = np.array([d.weekday() < 5 and d not in hol for d in days])
        self.month = np.array([d.month for d in days], np.int64)
        nxt = np.empty(n, np.int64)
        nb = BIG
        for i in range(n - 1, -1, -1):
            if self.is_bd[i]:
                nb = i
            nxt[i] = nb
        prv = np.empty(n, np.int64)
        pb = -BIG
        for i in range(n):
            if self.is_bd[i]:
                pb = i
            prv[i] = pb
        self.next_bd, self.prev_bd = nxt, prv
        nm = (last.year - EPOCH.year + 1) * 12 + 1
        self.ms = np.array([dn(dt.date(EPOCH.year + k // 12, k % 12 + 1, 1)) for k in range(nm)], np.int64)
        self.me = self.ms[1:] - 1
        self.mi_of = np.zeros(n, np.int64)
        for k in range(nm - 1):
            self.mi_of[self.ms[k]:self.ms[k + 1]] = k
        self.n = n

    def month_end_of(self, d):
        return self.me[self.mi_of[d]]

    def bdays(self, lo, hi):
        """business days in [lo, hi]"""
        if hi < lo:
            return np.zeros(0, np.int64)
        idx = np.arange(lo, hi + 1)
        return idx[self.is_bd[lo:hi + 1]]


def month_index(d):
    return (d.year - EPOCH.year) * 12 + d.month - 1


def add_months(dnum, n):
    """the same day n months later (clipped to the month's length), as a day number"""
    d = dd(dnum)
    k = month_index(d) + n
    y, m = EPOCH.year + k // 12, k % 12 + 1
    last = (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)).day
    return dn(dt.date(y, m, min(d.day, last)))


def luhn(q):
    tot = 0
    for i, c in enumerate(str(q)[::-1]):
        x = int(c)
        if i % 2 == 0:
            x *= 2
            if x > 9:
                x -= 9
        tot += x
    return (10 - tot % 10) % 10


# ---------------------------------------------------------------------------------------------- originations

def originations(rng, cal):
    R = dn(W.REPORT)
    draws = []
    m = W.GO_LIVE
    vol = W.VOL_START
    while m <= W.REPORT:
        if m > W.GO_LIVE:
            vol *= math.exp(W.period_value(W.VOL_GROWTH, m))
        lam = vol * W.SEASON[m.month] * W.VOL_SHOCK.get((m.year, m.month), 1.0)
        n = int(rng.poisson(lam))
        nxt = dt.date(m.year + (m.month == 12), m.month % 12 + 1, 1)
        days = cal.bdays(dn(m), min(dn(nxt) - 1, R))
        w = np.array([W.DOW_WEIGHT[dd(x).weekday()] for x in days], float)
        w[-4:] *= 1.15                        # broker settlements bunch into the last week of the month
        draws.append(np.sort(rng.choice(days, size=n, p=w / w.sum())))
        m = nxt
    draw = np.concatenate(draws)
    N = len(draw)
    L = dict(draw=draw)
    dates = [dd(x) for x in draw]
    # application score (v3 scale), truncated at the approval floor of the day
    mu, sd = W.APP_SCORE
    floor = np.array([580.0 if W.TIGHTENED[0] <= d <= W.TIGHTENED[1] else 545.0 for d in dates])
    s = rng.normal(mu, sd, N)
    bad = s < floor
    while bad.any():
        s[bad] = rng.normal(mu, sd, int(bad.sum()))
        bad = s < floor
    v4 = np.array([d >= W.SCORECARD_SWITCH for d in dates])
    a, b = W.SCORE_MAP
    s4 = np.rint(a * s + b + rng.normal(0, 4.0, N))
    orig = np.where(v4, s4, np.rint(s)).astype(int)
    f3 = np.array([f for _, f in W.BANDS_V3])
    f4 = np.array([f for _, f in W.BANDS_V4])
    grade = np.full(N, 4)
    for gi in range(4, -1, -1):
        grade = np.where(orig >= np.where(v4, f4[gi], f3[gi]), gi, grade)
    ov = rng.random(N) < 0.012                           # credit officer overrides, one notch either way
    grade = np.where(ov, np.clip(grade + rng.choice([-1, 1], N), 0, 4), grade)
    L.update(score_v3=s, v4=v4, orig_score=orig, grade=grade)
    # amount requested, term chosen, establishment fee added to the amount financed
    shift = np.array([0.12, 0.06, 0.0, -0.06, -0.15])[grade]
    amt = np.exp(rng.normal(math.log(15000) + shift, 0.62))
    p60 = 1 / (1 + np.exp(-2.0 * np.log(amt / 16500.0)))
    p60 = np.where(grade == 4, 0.75 * p60, p60)
    pl60 = rng.random(N) < p60
    u = rng.random(N)
    step = np.select([u < 0.40, u < 0.72, u < 0.86, u < 0.94], [5000, 1000, 500, 100], 1)
    amt = np.where(step > 1, np.rint(amt / step) * step, np.rint(amt))
    amt = np.where((step == 5000) & (amt < 5000), np.rint(amt / 1000) * 1000, amt)
    pl60 = np.where(amt > 35000, True, np.where(amt < 5000, False, pl60))
    amt = np.clip(amt, 3000, 50000)
    pct = np.array([W.FEE_PCT[W.GRADES[g]][int(d >= W.FEE_CHANGE)] for g, d in zip(grade, dates)])
    fee = np.clip(np.rint(pct * amt / 5) * 5, W.FEE_FLOOR, W.FEE_CAP)
    fee = np.where(rng.random(N) < W.FEE_UPFRONT, 0, fee)
    L.update(pl60=pl60, requested=amt, financed=(amt + fee).astype(np.int64), T=np.where(pl60, 60, 36))
    # channel and state
    yrs = np.array([d.year for d in dates])
    ch = np.zeros(N, int)
    uc = rng.random(N)
    for y, (pb, po, _) in W.CHANNEL_MIX.items():
        sel = yrs == y
        ch[sel] = np.where(uc[sel] < pb, 0, np.where(uc[sel] < pb + po, 1, 2))
    L["channel"] = ch
    L["state"] = rng.choice(len(W.STATES), size=N, p=W.STATE_P)
    # pricing: the rate card (repriced three weeks after each cash rate move), a score tier inside the grade,
    # the broker's loading and a returning-customer discount
    card = np.array([W.RATE_BASE[W.GRADES[g]] + (W.PL60_LOADING if p else 0.0)
                     + W.PASS_THROUGH * (W.cash_rate(d - dt.timedelta(days=W.REPRICE_LAG_DAYS)) - 0.0010)
                     for g, p, d in zip(grade, pl60, dates)]) * 100
    base = np.floor(card)
    cands = np.stack([base - 0.01, base + 0.49, base + 0.99], 1)
    card = cands[np.arange(N), np.argmin(np.abs(cands - card[:, None]), 1)]
    lo = np.where(v4, f4[grade], f3[grade])
    width = np.where(v4, np.array([67, 50, 45, 39, 40])[grade], np.array([60, 45, 40, 35, 35])[grade])
    pos = np.clip((orig - lo) / width, 0, 0.999)
    tier = np.array([0.80, 0.40, 0.0, -0.40, -0.80])[(pos * 5).astype(int)]
    load = np.where(ch == 0, rng.choice([0.0, 0.5, 1.0, 1.5], N, p=[0.45, 0.30, 0.17, 0.08]), 0.0)
    disc = np.where((ch == 2) & (rng.random(N) < 0.3), -0.25, 0.0)
    rate = np.clip(card + tier + load + disc, 5.99, W.RATE_CAP * 100)
    L["rate"] = np.round(rate / 100, 4)
    # first repayment: one month after drawdown unless the borrower picks a repayment day, 2 to 6 weeks out
    wday = np.ones(28)
    for dday, x in {1: 3.0, 5: 1.1, 10: 1.2, 14: 1.5, 15: 2.5, 16: 1.3, 20: 1.2, 25: 1.3, 28: 1.8}.items():
        wday[dday - 1] = x
    chosen = rng.choice(np.arange(1, 29), size=N, p=wday / wday.sum())
    default_day = rng.random(N) < 0.40
    first_mi = np.zeros(N, np.int64)
    rday = np.zeros(N, np.int64)
    for i in range(N):
        d = dates[i]
        if default_day[i] and d.day <= 28:
            rday[i], first_mi[i] = d.day, month_index(d) + 1
        elif default_day[i]:
            rday[i], first_mi[i] = 1, month_index(d) + 2
        else:
            c = int(chosen[i])
            earliest = draw[i] + 14
            k = int(cal.mi_of[earliest])
            if cal.ms[k] + c - 1 < earliest:
                k += 1
            rday[i], first_mi[i] = c, k
    L.update(rday=rday, first_mi=first_mi)
    # loan numbers: allocated at application, in application order, with gaps for applications never funded
    app = draw - rng.integers(3, 26, N)
    order = np.lexsort((np.arange(N), app))
    seq = np.zeros(N, np.int64)
    seq[order] = 100100 + np.cumsum(1 + rng.poisson(1.35, N))
    L["loan_no"] = np.array(["BPL%06d%d" % (q, luhn(q)) for q in seq])
    return L


# ---------------------------------------------------------------------------------------------- the simulation

class Sim:
    pass


def simulate(seed=W.SEED):
    rng = np.random.default_rng(seed)
    cal = Calendar()
    L = originations(rng, cal)
    N = len(L["draw"])
    R = dn(W.REPORT)
    T = L["T"]
    grade = L["grade"]
    rate = L["rate"]
    jj = np.arange(1, J + 1)
    rows = np.arange(N)
    # repayment calendar: nominal dates (interest is charged on these) and the business day each falls due
    nom = cal.ms[L["first_mi"][:, None] + jj[None, :] - 1] + L["rday"][:, None] - 1
    due = cal.next_bd[nom]
    inside = jj[None, :] <= T[:, None]
    i_m = rate / 12.0
    P = np.ceil(L["financed"] * i_m / (1 - (1 + i_m) ** (-T.astype(float))) * 100) / 100
    final_nom = nom[rows, T - 1]
    # default onset: the first instalment of a run that is never made good
    lvl = np.where(L["pl60"], W.ONSET_LEVEL["PL60"], W.ONSET_LEVEL["PL36"])
    mult = np.array([W.GRADE_MULT[g] for g in W.GRADES])[grade]
    shape = W.ONSET_FLOOR + (jj / W.ONSET_PEAK) * np.exp(1 - jj / W.ONSET_PEAK)
    haz = np.minimum(lvl[:, None] * mult[:, None] * shape[None, :], 0.5)
    haz[~inside] = 0.0
    cumh = np.cumsum(-np.log1p(-haz), 1)
    j0 = (cumh < -np.log(rng.random(N))[:, None]).sum(1) + 1
    j0 = np.where(j0 <= T, j0, 0)
    # full payout
    ramp = np.minimum(1.0, np.array([0.3, 0.6, 0.85] + [1.0] * (J - 3)))
    pp = W.PREPAY * np.array([W.PREPAY_GRADE[g] for g in W.GRADES])[grade][:, None] * ramp[None, :]
    pp = np.where(jj[None, :] < T[:, None], pp, 0.0)
    cump = np.cumsum(-np.log1p(-pp), 1)
    jp = (cump < -np.log(rng.random(N))[:, None]).sum(1) + 1
    jp = np.where(jp < T, jp, 0)
    up = rng.random(N)
    lo_p = np.where(jp == 1, L["draw"] + 7, due[rows, np.maximum(jp - 2, 0)] + 1)
    hi_p = due[rows, np.maximum(jp - 1, 0)] - 1
    pay_dt = cal.next_bd[(lo_p + up * np.maximum(hi_p - lo_p, 0)).astype(np.int64)]
    pay_dt = np.where(pay_dt > hi_p, cal.prev_bd[hi_p], pay_dt)
    payout_wins = (jp > 0) & ((j0 == 0) | (jp <= j0))
    j0 = np.where(payout_wins, 0, j0)
    # instalments made good on the due date, or late and caught up within 12 weeks
    season = np.array([0.0] + [W.LATE_SEASON[k] for k in range(1, 13)])[cal.month[due]]
    yrf = np.where(due >= dn(dt.date(2023, 1, 1)), 1.12, 1.0)
    q = np.array([W.LATE[g] for g in W.GRADES])[grade][:, None] * season * yrf
    late = (rng.random((N, J)) < q) & inside
    late &= ~((j0[:, None] > 0) & (jj[None, :] >= j0[:, None] - 3))
    r = rng.random((N, J))
    short = np.minimum(rng.geometric(0.28, (N, J)), 12)
    nxt_gap = np.diff(due, axis=1, append=due[:, -1:] + 30) + rng.integers(0, 5, (N, J))
    delay = np.select([r < 0.72, r < 0.91, r < 0.97], [short, nxt_gap, rng.integers(35, 61, (N, J))],
                      rng.integers(61, 85, (N, J)))
    clear = np.where(late, cal.next_bd[due + delay], due)
    clear = np.where(clear - due > 86, cal.prev_bd[due + 86], clear)
    cash = np.where(inside, P[:, None], 0.0)
    run = (j0[:, None] > 0) & (jj[None, :] >= j0[:, None])
    clear = np.where(run, BIG, clear)
    cash = np.where(run, 0.0, cash)
    S = Sim()
    S.cal, S.N, S.R, S.J, S.rng = cal, N, R, J, rng
    S.L, S.T, S.P, S.nom, S.due, S.final_nom = L, T, P, nom, due, final_nom
    S.haz, S.j0 = haz, j0
    S.clear, S.cash = clear, cash
    S.close = np.where(payout_wins, pay_dt, BIG).astype(np.int64)
    S.close_type = np.where(payout_wins, 1, 0).astype(np.int8)  # 0 open, 1 paid out, 2 matured, 3 written off, 4 settled
    S.extras = []                              # (loan, date, amount): extra and part repayments
    S.arr = []                                 # hardship arrangements
    S.cured = np.zeros(N, bool)
    S.e_def = np.full(N, BIG, np.int64)
    S.m_def = np.zeros(N, np.int64)
    defaults(S)
    hardship(S)
    finish(S)
    return S


def defaults(S):
    """default detection, then a settlement, a catch-up, a collections hardship arrangement, or write-off in the
    month-end batch once 180 days past due"""
    cal, rng, R = S.cal, S.rng, S.R
    settle, cure, hcure = W.POST_DEFAULT
    ar = np.arange(J)
    for i in np.nonzero(S.j0 > 0)[0]:
        j0 = int(S.j0[i])
        T = int(S.T[i])
        d0 = int(S.due[i, j0 - 1])
        d90 = d0 + 90
        e_def = int(cal.month_end_of(d90))
        S.e_def[i] = e_def
        S.m_def[i] = int((S.due[i, :T] <= e_def).sum())
        if rng.random() < 0.35:                 # part payments in arrears, never enough to clear an instalment
            for _ in range(int(rng.integers(1, 4))):
                x = int(cal.next_bd[d0 + int(rng.integers(5, 170))])
                if x <= R:
                    S.extras.append((int(i), x, float(np.round(rng.uniform(0.05, 0.28) * S.P[i], 2))))
        if d90 > R:
            continue
        e_wo = int(cal.month_end_of(d0 + 180))
        out = None
        for k in range(int(cal.mi_of[d90]), int(cal.mi_of[e_wo]) + 1):
            u = rng.random()
            days = cal.bdays(max(d90 + 1, int(cal.ms[k])), min(int(cal.me[k]), R, e_wo - 1))
            if len(days) == 0:
                continue
            x = int(days[int(rng.integers(len(days)))])
            if u < settle:
                out = ("settle", x)
            elif u < settle + cure:
                out = ("cure", x)
            elif u < settle + cure + hcure:
                out = ("hcure", x)
            if out:
                break
        if out and out[0] == "hcure":
            dec = int(cal.next_bd[out[1] + int(rng.integers(2, 7))])
            later = np.nonzero(S.due[i, :T] >= dec)[0]
            if len(later) == 0:
                out = ("cure", out[1])
            elif int(S.due[i, later[0]]) > e_wo:
                out = None
            else:
                js = int(later[0])
                n = min(6, T - js)
                start = int(S.due[i, js])
                end = min(add_months(start, n) - 1, int(S.final_nom[i]))
                if end == R:
                    end -= 1
                red = max(20.0, float(np.round(S.P[i] * rng.uniform(0.35, 0.6) / 5) * 5))
                cap = (S.due[i] < start) & (ar < T)
                S.clear[i][cap] = np.minimum(S.clear[i][cap], start)
                S.cash[i][cap & (S.clear[i] == start)] = 0.0
                var = (S.due[i] >= start) & (S.due[i] <= end) & (ar < T)
                S.clear[i][var] = S.due[i][var]
                S.cash[i][var] = red
                after = (S.due[i] > end) & (ar < T)
                S.clear[i][after] = S.due[i][after]
                S.cash[i][after] = S.P[i]
                S.cured[i] = True
                S.arr.append(dict(loan=int(i), received=out[1], start=start, end=end, kind="Reduced repayments",
                                  outcome="complete", reduced=red, reason=pick_reason(rng, out[1]), cancel=None))
                continue
        if out is None:
            if e_wo <= R:
                S.close[i], S.close_type[i] = e_wo, 3
            continue
        if out[0] == "settle":
            S.close[i], S.close_type[i] = out[1], 4
            continue
        x = out[1]
        sel = (ar >= j0 - 1) & (ar < T)
        paid = sel & (S.due[i] <= x)
        S.clear[i][paid] = x
        S.cash[i][paid] = S.P[i]
        nxt = sel & (S.due[i] > x)
        S.clear[i][nxt] = S.due[i][nxt]
        S.cash[i][nxt] = S.P[i]
        S.cured[i] = True


def pick_reason(rng, when):
    p = np.array(REASON_P, float)
    if dd(when) >= dt.date(2022, 7, 1):
        p[4] += 0.10
        p[1] += 0.04
    p /= p.sum()
    return REASONS[int(rng.choice(len(REASONS), p=p))]


def hardship(S):
    cal, rng, R, N = S.cal, S.rng, S.R, S.N
    L = S.L
    ar = np.arange(J)
    life_end = np.minimum(np.minimum(S.close, S.final_nom), R)
    onset_due = np.where(S.j0 > 0, S.due[np.arange(N), np.maximum(S.j0 - 1, 0)], BIG)
    busy = {}                                   # loan -> list of (from, to) already taken by an arrangement

    def free(i, a, b):
        return all(b + 45 < x or a > y + 45 for x, y in busy.get(i, []))

    # arrangements around a default: a pause that ends with no repayment resumed, or reduced repayments never made
    for i in np.nonzero(S.j0 > 0)[0]:
        j0 = int(S.j0[i])
        u = rng.random()
        if u < 0.25 and j0 >= 5:
            n = min(int(rng.choice([1, 2, 3])), j0 - 3)
            js = j0 - 1 - n
            start = int(S.due[i, js])
            x = int(cal.next_bd[start - int(rng.integers(6, 17))])
            if x <= R and x > L["draw"][i] + 60:
                end = min(add_months(start, n) - 1, int(S.due[i, j0 - 1]) - 1)
                if end == R:
                    end -= 1
                S.arr.append(dict(loan=int(i), received=x, start=start, end=end, kind="Payment pause", outcome="complete",
                                  reduced=0.0, reason=pick_reason(rng, x), cancel=None))
                busy.setdefault(int(i), []).append((x, end))
                zero = (ar >= js) & (ar < j0 - 1)
                cap = (S.due[i] < start) & (S.clear[i] > start)
                S.clear[i][cap] = start
                S.cash[i][cap] = 0.0
                S.clear[i][zero] = S.due[i][zero]
                S.cash[i][zero] = 0.0
        elif u < 0.45 and j0 >= 3:
            start = int(S.due[i, j0 - 1])
            x = int(cal.next_bd[start - int(rng.integers(5, 16))])
            if x <= R and x > L["draw"][i] + 60:
                n = int(rng.choice([3, 4, 6]))
                end = min(add_months(start, n) - 1, int(S.final_nom[i]))
                if end == R:
                    end -= 1
                c = int(cal.next_bd[start + int(rng.integers(25, 46))])
                if c == R:
                    c = int(cal.prev_bd[R - 1])
                red = max(20.0, float(np.round(S.P[i] * rng.uniform(0.35, 0.6) / 5) * 5))
                S.arr.append(dict(loan=int(i), received=x, start=start, end=end, kind="Reduced repayments",
                                  outcome="failed", reduced=red, reason=pick_reason(rng, x), cancel=c))
                busy.setdefault(int(i), []).append((x, end))
    for a in S.arr:                             # collections arrangements made after a default
        busy.setdefault(a["loan"], []).append((a["received"], a["end"]))
    events = []                                 # (loan, received, kind, months, reason, outcome)
    # COVID-19 payment pauses, March to May 2020
    open_apr = (L["draw"] < dn(dt.date(2020, 4, 1))) & (life_end > dn(dt.date(2020, 4, 1)))
    days = cal.bdays(dn(dt.date(2020, 3, 23)), dn(dt.date(2020, 5, 29)))
    for i in np.nonzero(open_apr & (rng.random(N) < 0.085))[0]:
        events.append((int(i), int(rng.choice(days)), "Payment pause", 3 if rng.random() < 0.65 else 6, "COVID-19",
                       "complete" if rng.random() < 0.93 else "withdrawn"))
    # floods in NSW and Queensland, February to April 2022
    open_mar = (L["draw"] < dn(dt.date(2022, 3, 1))) & (life_end > dn(dt.date(2022, 3, 1))) & np.isin(L["state"], [0, 2])
    days = cal.bdays(dn(dt.date(2022, 2, 28)), dn(dt.date(2022, 4, 14)))
    for i in np.nonzero(open_mar & (rng.random(N) < 0.007))[0]:
        events.append((int(i), int(rng.choice(days)), "Payment pause", int(rng.choice([1, 2, 3])), "Natural disaster", "complete"))
    # ordinary requests through the life of the loan
    gm = np.array([W.HARDSHIP_GRADE[g] for g in W.GRADES])[L["grade"]]
    for k in range(int(cal.mi_of[dn(W.GO_LIVE)]), int(cal.mi_of[R]) + 1):
        lo, hi = int(cal.ms[k]), min(int(cal.me[k]), R)
        lam = W.period_value(W.HARDSHIP_RATE, dd(lo))
        elig = (L["draw"] + 50 <= hi) & (life_end - 25 >= lo)
        hit = np.nonzero(elig & (rng.random(N) < lam * gm))[0]
        days = cal.bdays(lo, hi)
        for i in hit:
            x = int(days[int(rng.integers(len(days)))])
            if x < L["draw"][i] + 50 or x > life_end[i] - 25:
                continue
            if rng.random() < 0.40:
                kind, n = "Payment pause", int(rng.choice([1, 2, 3], p=[0.30, 0.45, 0.25]))
            else:
                kind, n = "Reduced repayments", int(rng.choice([3, 4, 6], p=[0.45, 0.20, 0.35]))
            v = rng.random()
            outcome = "withdrawn" if v < 0.08 else ("failed" if v < 0.17 else "complete")
            events.append((int(i), x, kind, n, pick_reason(rng, x), outcome))
            if rng.random() < 0.15:             # a second request once the first has run its course
                y = x + int(rng.integers(150, 420))
                if y <= min(R, life_end[i] - 25):
                    y = int(cal.next_bd[y])
                    events.append((int(i), y, "Reduced repayments" if rng.random() < 0.6 else "Payment pause",
                                   int(rng.choice([2, 3, 6])), pick_reason(rng, y), "complete" if rng.random() < 0.85 else "failed"))
    events.sort(key=lambda e: (e[0], e[1]))
    for (i, x, kind, n, reason, outcome) in events:
        T = int(S.T[i])
        if x > R:
            continue
        dec = int(cal.next_bd[x + int(rng.integers(1, 9))])
        later = np.nonzero(S.due[i, :T] >= dec + 2)[0]
        if len(later) == 0:
            continue
        js = int(later[0])
        start = int(S.due[i, js])
        n = min(n, T - js)
        if n < 1:
            continue
        end = add_months(start, n) - 1
        if end == R:
            end = add_months(start, n + 1) - 1 if js + n + 1 <= T else add_months(start, n - 1) - 1
        if end < start or end > S.final_nom[i] or end + 30 >= S.close[i] or end + 60 >= onset_due[i]:
            continue
        if not free(i, x, end):
            continue
        busy.setdefault(i, []).append((x, end))
        red = 0.0 if kind == "Payment pause" else max(20.0, float(np.round(S.P[i] * rng.uniform(0.35, 0.65) / 5) * 5))
        rec = dict(loan=i, received=x, start=start, end=end, kind=kind, outcome=outcome, reduced=red, reason=reason, cancel=None)
        if outcome == "withdrawn":
            lo = int(cal.next_bd[x + 1])
            c = int(cal.prev_bd[lo + int(rng.integers(0, max(1, start - lo)))])
            rec["cancel"] = min(c, int(cal.prev_bd[start - 1]))
            if rec["cancel"] == R:
                rec["cancel"] = int(cal.prev_bd[R - 1])
            S.arr.append(rec)
            continue
        row_c, row_m = S.clear[i], S.cash[i]
        # repayments around the arrangement are as varied; arrears at the start are capitalised
        near = (S.due[i] >= x) & (S.due[i] <= end + 100) & (ar < T)
        row_c[near] = S.due[i][near]
        np.maximum.accumulate(row_c, out=row_c)
        cap = (S.due[i] < start) & (row_c > start)
        row_c[cap] = start
        row_m[cap] = 0.0
        var = (S.due[i] >= start) & (S.due[i] <= end) & (ar < T)
        row_c[var] = S.due[i][var]
        row_m[var] = red
        if outcome == "failed":
            first = int(np.nonzero(var)[0][0])
            c = int(cal.next_bd[int(S.due[i, first]) + int(rng.integers(25, 46))])
            y = min(int(cal.next_bd[c + int(rng.integers(5, 26))]), int(cal.prev_bd[int(S.due[i, first]) + 84]))
            owed = (ar >= first) & (S.due[i] <= y) & (ar < T)
            row_c[owed] = y
            row_m[owed] = S.P[i]
            resumed = var & (S.due[i] > c)
            row_m[resumed] = S.P[i]
            if c == R:
                c = int(cal.prev_bd[R - 1])
            rec["cancel"] = c
        S.arr.append(rec)


def finish(S):
    """made-good dates in order, loan closures, extra repayments"""
    cal, rng, R, N = S.cal, S.rng, S.R, S.N
    np.maximum.accumulate(S.clear, axis=1, out=S.clear)
    T = S.T
    last_clear = S.clear[np.arange(N), T - 1]
    matured = (S.close == BIG) & (last_clear < BIG)
    S.close[matured] = last_clear[matured]
    S.close_type[matured] = 2
    # extra repayments, each below a quarter of the scheduled balance at the time, by borrowers not heading for default
    L = S.L
    k = np.minimum(rng.poisson(0.25, N), np.where(L["pl60"], 3, 2))
    k = np.where(S.j0 > 0, 0, k)
    hi = np.minimum(S.close, R) - 1
    windows = {}
    for a in S.arr:
        windows.setdefault(a["loan"], []).append((a["received"] - 60, a["end"] + 60))
    for i in np.nonzero(k > 0)[0]:
        lo = int(L["draw"][i]) + 45
        if hi[i] <= lo:
            continue
        for _ in range(int(k[i])):
            x = int(cal.next_bd[lo + int(rng.integers(0, hi[i] - lo))])
            if x > hi[i] or any(a <= x <= b for a, b in windows.get(int(i), [])):
                continue
            paid = int((S.due[i, :T[i]] <= x).sum())
            im = L["rate"][i] / 12
            sched = L["financed"][i] * ((1 + im) ** T[i] - (1 + im) ** paid) / ((1 + im) ** T[i] - 1)
            if rng.random() < 0.45:
                amt = float(rng.choice([200, 250, 300, 500, 500, 1000, 1000, 1500, 2000, 2500, 3000, 5000]))
            else:
                amt = float(np.round(np.exp(rng.normal(math.log(900), 0.8)), 2))
            amt = min(amt, float(np.floor(0.25 * sched)))
            if amt >= 50:
                S.extras.append((int(i), x, amt))
    # a loan whose extra repayments have cleared what it owes is closed at that repayment, ahead of its term
    S.early = np.zeros(N, bool)
    by_loan = {}
    for l, x, a in S.extras:
        by_loan.setdefault(l, []).append((x, a))
    for i, ex in by_loan.items():
        if S.j0[i] > 0:
            continue
        x = payoff_date(S, i, ex)
        if x is not None and x < S.close[i]:
            S.close[i], S.close_type[i] = int(cal.next_bd[x]), 2
            S.early[i] = True
    for key, amt in sorted(W.TUNE.items()):
        i = int(key) - 1
        last = int(S.nom[i][S.nom[i] <= R].max()) if (S.nom[i] <= R).any() else int(L["draw"][i])
        lastdue = int(S.due[i][S.due[i] <= R].max()) if (S.due[i] <= R).any() else last
        x = min(int(cal.next_bd[max(last, lastdue) + 3]), R)
        S.extras.append((i, x, float(amt)))


def payoff_date(S, i, extras):
    """the first repayment after which nothing is owed: interest is charged on each nominal repayment date, so between
    charges the balance is the last charged balance less repayments since"""
    T = int(S.T[i])
    tau = int(min(S.close[i], S.cal.n - 1))
    pays = [(int(S.clear[i, j]), float(S.cash[i, j])) for j in range(J) if S.cash[i, j] > 0 and S.clear[i, j] <= tau]
    pays += [(int(x), float(a)) for x, a in extras if x <= tau]
    pays.sort()
    final = int(S.due[i, T - 1])
    B = float(S.L["financed"][i])
    prev = int(S.L["draw"][i])
    r = float(S.L["rate"][i]) / 365.0
    p = 0
    for c in S.nom[i]:
        c = int(c)
        if c > tau:
            break
        paid = wsum = 0.0
        while p < len(pays) and pays[p][0] <= c:
            d, a = pays[p]
            if B - paid - a <= 0.005 and d < final:
                return d
            paid += a
            wsum += a * (c - d)
            p += 1
        B = B + r * (B * (c - prev) - wsum) - paid
        prev = c
    paid = 0.0
    while p < len(pays):
        d, a = pays[p]
        if B - paid - a <= 0.005 and d < final:
            return d
        paid += a
        p += 1
    return None


# ---------------------------------------------------------------------------------------------- measurement

def dpd_at(S, t, rows=None):
    """days past due at close of business on day t: days since the oldest instalment not yet made good"""
    rows = np.arange(S.N) if rows is None else np.asarray(rows)
    c = S.clear[rows]
    unpaid = c > t
    jstar = unpaid.argmax(1)
    d = S.due[rows, jstar]
    return np.where(unpaid.any(1) & (d < t), t - d, 0)


def open_at(S, t):
    return (S.L["draw"] <= t) & (S.close > t)


def balance_path(S, rows, tau):
    """account balance after each nominal repayment date up to day tau[i] (interest accrued daily at the contract rate
    and charged on each nominal repayment date, less every repayment received), and repayments after the last charge"""
    rows = np.asarray(rows)
    n = len(rows)
    tau = np.asarray(tau, np.int64)
    c = S.nom[rows].astype(np.int64)
    m = (S.cash[rows] > 0) & (S.clear[rows] <= tau[:, None])
    pi, pj = np.nonzero(m)
    pdt = [S.clear[rows][pi, pj]]
    pam = [S.cash[rows][pi, pj]]
    pis = [pi]
    pos_of = {int(r): k for k, r in enumerate(rows)}
    ex = [(pos_of[l], x, a) for (l, x, a) in S.extras if l in pos_of]
    if ex:
        e = np.array(ex)
        k = e[:, 0].astype(np.int64)
        keep = e[:, 1].astype(np.int64) <= tau[k]
        pis.append(k[keep])
        pdt.append(e[keep, 1].astype(np.int64))
        pam.append(e[keep, 2])
    pi, pdt, pam = np.concatenate(pis), np.concatenate(pdt), np.concatenate(pam)
    flat = (np.arange(n, dtype=np.int64)[:, None] * 10 ** 6 + c).ravel()
    k = np.searchsorted(flat, pi * 10 ** 6 + pdt, side="left") - pi * J
    kk = np.minimum(k, J - 1)
    charged = (k < J) & (c[pi, kk] <= tau[pi])
    Ssum = np.zeros((n, J))
    Wsum = np.zeros((n, J))
    np.add.at(Ssum, (pi[charged], kk[charged]), pam[charged])
    np.add.at(Wsum, (pi[charged], kk[charged]), pam[charged] * (c[pi[charged], kk[charged]] - pdt[charged]))
    tail = np.zeros(n)
    np.add.at(tail, pi[~charged], pam[~charged])
    B = S.L["financed"][rows].astype(float)
    prev = S.L["draw"][rows].astype(np.int64)
    r = S.L["rate"][rows] / 365.0
    path = np.zeros((n, J))
    for j in range(J):
        act = c[:, j] <= tau
        newB = B + r * (B * (c[:, j] - prev) - Wsum[:, j]) - Ssum[:, j]
        B = np.where(act, newB, B)
        prev = np.where(act, c[:, j], prev)
        path[:, j] = B
    return path, B - tail


def balances(S, rows, tau):
    return balance_path(S, rows, tau)[1]
