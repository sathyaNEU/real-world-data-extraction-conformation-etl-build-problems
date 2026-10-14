"""The true timeline: every long-stay care home resident the partnership funds or pays free personal care for, from
2006, with admission, home, care type, conversion to council funding, home moves and exit; and the short placements
(interim and respite) beside them. Event times are drawn per admission-year cohort on stratified uniforms, so the
empirical hazards by months since admission do not drift from window to window."""
import numpy as np

import world as W

MONTH = W.MONTH


def inv_piecewise(E, breaks, rates):
    """time t (months) at which the cumulative hazard of a piecewise-constant hazard reaches E.
    breaks: upper edges of the segments (last is inf), rates: hazard per month in each"""
    t = np.full(E.shape, np.inf)
    left = E.copy()
    lo = 0.0
    done = np.zeros(E.shape, bool)
    for hi, r in zip(breaks, rates):
        width = hi - lo
        cap = r * width
        hit = (~done) & (left <= cap) if np.isfinite(width) else (~done)
        if r > 0:
            t[hit] = lo + left[hit] / r
        done |= hit
        left = np.where(done, left, left - cap)
        lo = hi
    return t


def death_segments(nursing):
    m = W.NURSING_DEATH if nursing else 1.0
    br = [3, 6, 12, np.inf]
    rt = [W.DEATH_BASE * m * W.death_mult(x) + W.DISCH for x in (0, 3, 6, 12)]
    return br, rt


def strat_u(rng, n):
    if n == 0:
        return np.zeros(0)
    return (rng.permutation(n) + rng.uniform(0, 1, n)) / n


class World:
    pass


def homes_table():
    """index, name, locality (or council for an out-of-area home), nursing, places, opened day, out-of-area?"""
    H = []
    for name, loc, prov, nurs, places, reg in W.HOMES:
        opened = W.NEW_HOMES.get(name, W.dn(__import__("datetime").date.fromisoformat(reg)))
        H.append(dict(name=name, loc=loc, prov=prov, nursing=nurs, places=places, opened=opened, ooa=False))
    for name, council, nurs in W.OOA_HOMES:
        H.append(dict(name=name, loc=council, prov="", nursing=nurs, places=40, opened=0, ooa=True))
    return H


def choose_home(rng, H, team, care, day, ooa_p, exclude_new=True):
    if ooa_p > 0 and rng.random() < ooa_p:
        cands = [i for i, h in enumerate(H) if h["ooa"] and (h["nursing"] or care == 0)]
        return cands[rng.integers(len(cands))]
    if rng.random() < 0.655:
        loc = W.LOCS[team]
    else:
        others = [l for k, l in enumerate(W.LOCS) if k != team]
        loc = others[rng.integers(4)]
    cands = [i for i, h in enumerate(H) if not h["ooa"] and h["loc"] == loc and h["opened"] <= day
             and (h["nursing"] or care == 0) and not (exclude_new and h["name"] in W.NEW_HOMES)]
    if not cands:
        cands = [i for i, h in enumerate(H) if not h["ooa"] and h["opened"] <= day and (h["nursing"] or care == 0)
                 and not (exclude_new and h["name"] in W.NEW_HOMES)]
    w = np.array([H[i]["places"] for i in cands], float)
    return cands[rng.choice(len(cands), p=w / w.sum())]


def simulate(seed=W.SEED, sf_surge=1.0):
    rng = np.random.default_rng(seed)
    H = homes_table()
    recs = []      # kind, admit, care, team, home
    month_starts = np.arange(W.SIM_START, W.SIM_END, MONTH)
    # council-funded direct admissions: a flat number each calendar year (a different number in each year of the
    # shipped history), dates at random within the year; drawn on their own stream
    rng_d = np.random.default_rng(seed + 7)
    years = list(range(2006, 2029))
    offs = dict(zip(years, rng_d.integers(-4, 5, len(years))))
    recent = rng_d.permutation([-3, -2, -1, 0, 1, 2, 3])
    for k, y in enumerate(range(2021, 2028)):
        offs[y] = int(recent[k])
    for y in years:
        a0, a1 = W.dn(__import__("datetime").date(y, 1, 1)), W.dn(__import__("datetime").date(y + 1, 1, 1))
        n = 192 + int(offs[y])
        days = np.sort(rng_d.uniform(a0, a1, n))
        for a in days:
            care = 1 if rng_d.random() < 0.42 else 0
            team = rng_d.choice(5, p=W.TEAM_W)
            recs.append((0, a, care, team, choose_home(rng_d, H, team, care, a, 0.045)))
    # self-funded admissions
    d = __import__("datetime").date
    for ms in month_starts:
        lam = 22.0
        if ms >= W.dn(d(2025, 4, 1)):
            ramp = min(1.0, (ms - W.dn(d(2025, 4, 1))) / (W.dn(d(2025, 12, 1)) - W.dn(d(2025, 4, 1))))
            lam = 22.0 * (1.0 + 0.40 * ramp * sf_surge)
        for _ in range(rng.poisson(lam)):
            a = ms + rng.uniform(0, MONTH)
            care = 1 if rng.random() < 0.36 else 0
            team = rng.choice(5, p=W.TEAM_W)
            recs.append((1, a, care, team, choose_home(rng, H, team, care, a, 0.0)))
        for name, rate, lo, hi in (("Larchgrove House", 6.0, d(2025, 6, 2), d(2026, 4, 1)),
                                   ("Pinewell Lodge", 5.5, d(2025, 9, 15), d(2026, 7, 1))):
            if W.dn(lo) <= ms < W.dn(hi):
                hidx = [i for i, h in enumerate(H) if h["name"] == name][0]
                for _ in range(rng.poisson(rate * sf_surge)):
                    a = max(ms + rng.uniform(0, MONTH), W.dn(lo))
                    care = 1 if rng.random() < 0.40 else 0
                    # people come to the new homes from across the partnership
                    team = rng.choice(5, p=W.TEAM_W)
                    recs.append((1, a, care, team, hidx))
    R = np.array(recs, dtype=float)
    kind, admit, care, team, home = (R[:, i] for i in range(5))
    n = len(R)
    admit = np.floor(admit)
    ayear = np.array([W.dd(a).year for a in admit])
    # stratified uniforms per (kind, admission year, care type)
    u_exit = np.zeros(n)
    u_conv = np.zeros(n)
    u_why = np.zeros(n)
    for key in sorted(set(zip(kind, ayear, care))):
        idx = np.where((kind == key[0]) & (ayear == key[1]) & (care == key[2]))[0]
        u_exit[idx] = strat_u(rng, len(idx))
        u_conv[idx] = strat_u(rng, len(idx))
        u_why[idx] = rng.uniform(0, 1, len(idx))
    t_exit = np.zeros(n)
    for c in (0, 1):
        m = care == c
        br, rt = death_segments(c == 1)
        t_exit[m] = inv_piecewise(-np.log(u_exit[m]), br, rt)
    br = [hi for hi, _ in W.CONV]
    br[-1] = np.inf
    t_conv = inv_piecewise(-np.log(u_conv), br, [r for _, r in W.CONV])
    t_conv[kind == 0] = np.inf
    # death or discharge, by the hazard shares at the exit duration
    why = np.ones(n, int)
    for i in range(n):
        mo = t_exit[i]
        dh = W.DEATH_BASE * (W.NURSING_DEATH if care[i] else 1.0) * W.death_mult(mo)
        if u_why[i] < W.DISCH / (dh + W.DISCH):
            why[i] = 2
    exit_day = admit + np.floor(t_exit * MONTH) + 1          # out at the end of the day before; at least one night
    conv_day = admit + np.floor(t_conv * MONTH) + 1
    # each self-funder's weekly drawdown on their savings: the home's fee less free personal (and nursing) care and
    # their income. A rise in the upper capital limit brings the day their capital reaches it forward by the rise over
    # the drawdown, and anyone within the rise of the old limit qualifies on the day it changes. The limits were frozen
    # from 2019 and rise on 6 April 2026 and 5 April 2027. Drawn on its own stream.
    rng_s = np.random.default_rng(seed + 31)
    home_level = np.array([1.22 if h["name"] in W.NEW_HOMES else 1.0 for h in H])
    lvl = rng_s.uniform(0.86, 1.14, len(H))
    income = np.clip(rng_s.normal(235, 55, n), 150, 420)
    hi_ = home.astype(int)
    fee26 = np.where(care == 1, W.SF_FEE_2026[1], W.SF_FEE_2026[0]) * home_level[hi_] * lvl[hi_]
    fpnc26 = W.FPNC[2026][0] + np.where(care == 1, W.FPNC[2026][1], 0.0)
    draw26 = np.maximum(fee26 - fpnc26 - income, 150.0)
    for y in range(2007, 2028):
        D = W.uprate_day(y)
        rise = W.CAPITAL[y][1] - W.CAPITAL[y - 1][1]
        if rise <= 0:
            continue
        adv = 7.0 * rise / (draw26 * W.SF_FEE_GROWTH ** (y - 2026))
        m = (kind == 1) & (admit < D) & (conv_day > D) & np.isfinite(conv_day)
        conv_day[m] = np.maximum(D, np.round(conv_day[m] - adv[m]))
    conv_day[conv_day >= exit_day] = np.inf
    # nothing happens on the as-of date itself: an admission, exit or change of funding on 31 December 2026 moves to
    # the next day, so the end-of-day convention cannot move the count
    for arr in (admit, exit_day, conv_day):
        arr[arr == W.ASOF] += 1
    # a conversion on 1 January 2027 would end its free personal care award on 31 December 2026, inside the records:
    # it takes effect a day later, so no award ends on the as-of date either
    conv_day[conv_day == W.ASOF + 1] += 1
    exit_day = np.maximum(exit_day, admit + 1)
    conv_day[conv_day >= exit_day] = np.inf
    S = World()
    S.H, S.kind, S.admit, S.care, S.team, S.home = H, kind.astype(int), admit, care.astype(int), team.astype(int), home.astype(int)
    S.exit, S.why, S.conv = exit_day, why, conv_day
    S.draw26 = draw26
    S.n = n
    # home moves inside a stay (about 2.5 per cent a year), never in the first month or the last fortnight
    S.moves = {}
    for i in range(n):
        a, e = admit[i], min(exit_day[i], W.SIM_END)
        t = a + 30
        while True:
            t += rng.exponential(365.25 / 0.025)
            if t >= e - 14:
                break
            cf_now = kind[i] == 0 or conv_day[i] <= t
            nh = choose_home(rng, H, int(team[i]), int(care[i]), t, 0.045 if cf_now else 0.0)
            prev = S.moves[i][-1][1] if S.moves.get(i) else int(home[i])
            if nh != prev:
                S.moves.setdefault(i, []).append((float(np.floor(t)), nh))
    return S


def home_at(S, i, day):
    h = int(S.home[i])
    for t, nh in S.moves.get(i, []):
        if t <= day:
            h = nh
    return h


def cf_on(S, day):
    """council-funded long-stay residents in place at the end of the day"""
    inplace = (S.admit <= day) & (S.exit > day)
    return inplace & ((S.kind == 0) | (S.conv <= day))


def sf_on(S, day):
    inplace = (S.admit <= day) & (S.exit > day)
    return inplace & (S.kind == 1) & ~(S.conv <= day)


def truth_inputs(S):
    """stay and award inputs straight from the timeline, as records with no Layer 1 mess would give them"""
    A = W.ASOF
    I = {}
    cfd = (S.kind == 0) & (S.admit <= A)
    cfc = (S.kind == 1) & (S.conv <= A)
    adm = np.concatenate([S.admit[cfd], S.admit[cfc]])
    ent = np.concatenate([S.admit[cfd], S.conv[cfc]])
    ex = np.concatenate([S.exit[cfd], S.exit[cfc]])
    ex = np.where(ex > A, np.inf, ex)
    I.update(cf_admit=adm, cf_entry=ent, cf_exit=ex, cf_care=np.concatenate([S.care[cfd], S.care[cfc]]),
             cf_route=np.array(["DIRECT"] * int(cfd.sum()) + ["CONV"] * int(cfc.sum())))
    sf = (S.kind == 1) & (S.admit <= A)
    end = np.minimum(S.conv[sf], S.exit[sf])
    reason = np.where(S.conv[sf] < S.exit[sf], "CONV", "EXIT")
    reason = np.where(end > A, "", reason)
    end = np.where(end > A, np.inf, end)
    I.update(sf_admit=S.admit[sf], sf_award=S.admit[sf], sf_entry=S.admit[sf], sf_end=end, sf_reason=reason,
             sf_care=S.care[sf])
    return I
