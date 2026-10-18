"""task244 simulation: the labour force survey's rotating panel of dwellings in twelve districts, each adult's true labour
force status quarter to quarter on the district's own transition rates, the status each interview records (read with
the original interview's classification error), the households that split, move out or lose members between visits,
and the supervisors' reinterview of a random twelfth or so of each quarter's responding households, with its attempts,
completions and reconciled statuses. Districts are the 2027 districts throughout: the six enumeration areas that moved
from the Industrial Corridor to the Metropolitan Fringe on 1 April 2027 belong to the Fringe's labour market. Deterministic
for a given seed."""
import datetime as dt

import numpy as np

import params as P

S = P.STATUS


def mmat(m):
    return np.array([[1 - m["EU"] - m["EN"], m["EU"], m["EN"]],
                     [m["UE"], 1 - m["UE"] - m["UN"], m["UN"]],
                     [m["NE"], m["NU"], 1 - m["NE"] - m["NU"]]])


def pmat(r):
    out = np.zeros((3, 3))
    for k, v in r.items():
        out[S.index(k[0]), S.index(k[1])] = v
    for i in range(3):
        out[i, i] = 1 - out[i].sum()
    return out


def stationary(p):
    w, v = np.linalg.eig(p.T)
    s = np.real(v[:, np.argmin(abs(w - 1))])
    return s / s.sum()


def draw(rng, probs):
    """one categorical draw per row of probs"""
    u = rng.random(len(probs))
    return np.minimum((u[:, None] > probs.cumsum(1)).sum(1), probs.shape[1] - 1)


# age groups 15-24, 25-54, 55-64, 65 and over: the district's quarterly rates scaled for each (school leavers and
# students move in and out of the labour force more; older adults leave it and seldom return)
AGE_BREAKS = [25, 55, 65]
AGE_MULT = [dict(EU=1.4, EN=2.0, UE=0.8, UN=1.6, NE=0.6, NU=1.5),
            dict(EU=1.0, EN=1.0, UE=1.0, UN=1.0, NE=1.0, NU=1.0),
            dict(EU=0.9, EN=1.6, UE=0.8, UN=1.5, NE=0.5, NU=0.6),
            dict(EU=0.6, EN=3.0, UE=0.6, UN=2.0, NE=0.3, NU=0.3)]
HEAD_AGE = np.arange(22, 81)
HEAD_AGE_P = np.exp(-0.5 * ((HEAD_AGE - 44) / 13.0) ** 2)
HEAD_AGE_P = HEAD_AGE_P / HEAD_AGE_P.sum()
OTHER_AGE = np.arange(15, 81)
OTHER_AGE_P = np.exp(-(OTHER_AGE - 15) / 24.0)
OTHER_AGE_P = OTHER_AGE_P / OTHER_AGE_P.sum()


def agegroup(age):
    return int(sum(age >= b for b in AGE_BREAKS))


def household_ages(rng, n):
    """a household's adults: (relation, sex, age), the head first"""
    hsex = "M" if rng.random() < 0.72 else "F"
    hage = int(rng.choice(HEAD_AGE, p=HEAD_AGE_P))
    out = [("head", hsex, hage)]
    if n >= 2 and rng.random() < 0.75:
        ssex = "F" if hsex == "M" else "M"
        sage = max(18, hage + (int(rng.integers(-9, 3)) if ssex == "F" else int(rng.integers(-2, 9))))
        out.append(("spouse", ssex, sage))
    while len(out) < n:
        cage = hage - int(rng.integers(20, 37))
        if cage >= 15 and rng.random() < 0.8:
            out.append(("child", "M" if rng.random() < 0.5 else "F", cage))
        else:
            out.append(("other relative", "M" if rng.random() < 0.5 else "F", int(rng.choice(OTHER_AGE, p=OTHER_AGE_P))))
    return out


class Person:
    __slots__ = ("pid", "sex", "by", "bm", "rel", "line", "true", "alive", "ag")

    def __init__(self, pid, sex, by, bm, rel, line, true, ag):
        self.pid, self.sex, self.by, self.bm, self.rel, self.line, self.true = pid, sex, by, bm, rel, line, true
        self.ag = ag
        self.alive = True


class Household:
    __slots__ = ("hh", "members", "gone")

    def __init__(self, hh, members):
        self.hh, self.members, self.gone = hh, members, False


class World:
    pass


def ea_codes(d):
    """the 2027 district's enumeration areas, as (ea code in 2027, district before 1 April 2027, ea code before)"""
    own = [(e, d, e) for e in range(1, P.EAS_PER_DISTRICT + 1) if (d, e) not in P.MOVED_EAS]
    if d == "D02":
        own += [(P.EAS_PER_DISTRICT + 1 + i, od, oe) for i, (od, oe) in enumerate(P.MOVED_EAS)]
    return own


def fieldday(rng, q):
    """an interview day in the quarter's fieldwork weeks, Monday to Saturday"""
    while True:
        day = P.Q_START[P.QUARTERS[q]] + dt.timedelta(days=int(rng.integers(0, 7 * P.FIELD_WEEKS)))
        if day.weekday() < 6:
            return day


def make(seed=P.SIM_SEED):
    rng = np.random.default_rng(seed)
    W = World()
    W.seed = seed
    W.M = mmat(P.M_ORIG)
    W.MR = mmat(P.M_REINT)
    W.P, W.pi, W.F = {}, {}, {}
    for d in P.DCODES:
        r = {k: v * rng.uniform(1 - P.RATE_JITTER, 1 + P.RATE_JITTER) for k, v in P.ARCH[P.DTYPE[d]].items()}
        W.P[d] = [pmat({k: v * m[k] for k, v in r.items()}) for m in AGE_MULT]
        W.pi[d] = [stationary(x) for x in W.P[d]]
    nq = len(P.QUARTERS)
    W.hhq = []          # one record per interviewed household per quarter
    W.splits = []       # (quarter, dwelling, new household number, pids)
    W.moves = []        # (quarter, dwelling, household that left)
    W.taken = {}        # dwelling -> every (sex, birth year, birth month) of the people who lived there
    pid = [0]

    def person(year_now, rel, sex, age, line, q, taken, d):
        """a new adult, its status drawn from its district's and age group's own long-run shares; no two people ever
        living in one dwelling share sex and month and year of birth"""
        pid[0] += 1
        by = year_now - age - (1 if rng.random() < 0.5 else 0)
        bm = int(rng.integers(1, 13))
        while (sex, by, bm) in taken:
            bm = int(rng.integers(1, 13))
            if (sex, by, bm) in taken:
                by -= 1
        taken.add((sex, by, bm))
        ag = agegroup(age)
        st = int(draw(rng, W.pi[d][ag][None, :])[0])
        return Person(pid[0], sex, by, bm, rel, line, {q: st}, ag)

    def new_household(year_now, q, taken, d):
        n = int(rng.choice(P.ADULTS, p=P.ADULTS_P))
        return [person(year_now, rel, sx, age, j + 1, q, taken, d)
                for j, (rel, sx, age) in enumerate(household_ages(rng, n))]

    for d in P.DCODES:
        eas = ea_codes(d)
        for e in range(-3, nq):
            for k in range(P.DWELLINGS_PER_COHORT):
                ea, ed, ee = eas[int(rng.integers(0, len(eas)))]
                dw = "%s%02d%04d" % (ed[1:], ee, (e + 3) * P.DWELLINGS_PER_COHORT + k + 1)
                yr = 2026 + (e + 3) // 4
                taken = set()
                hhs = [Household(1, new_household(yr, e, taken, d))]
                W.taken[dw] = taken
                for v in range(4):
                    q = e + v
                    if v > 0:
                        _between(rng, W, d, dw, q, hhs, new_household, taken)
                    resp = rng.random(len(hhs)) < (P.RESP_FIRST if v == 0 else P.RESP_LATER)
                    if q < 0 or q >= nq:
                        continue
                    for h, ok in zip(hhs, resp):
                        alive = [p_ for p_ in h.members if p_.alive]
                        if h.gone or not ok or not alive:
                            continue
                        rec = draw(rng, W.M[[p_.true[q] for p_ in alive]])
                        day = fieldday(rng, q)
                        intv = 1 + (ea + q) % P.INTERVIEWERS_PER_DISTRICT
                        resp_line = alive[0].line if rng.random() < 0.6 else alive[min(1, len(alive) - 1)].line
                        proxy = rng.random(len(alive)) < P.PROXY
                        people = []
                        for p_, rs, px in zip(alive, rec, proxy):
                            people.append(dict(pid=p_.pid, line=p_.line, sex=p_.sex, by=p_.by, bm=p_.bm, rel=p_.rel,
                                               ag=p_.ag, true=p_.true[q], rec=int(rs),
                                               resp_line=resp_line if (px and len(alive) > 1) else p_.line))
                        W.hhq.append(dict(d=d, ea=ea, ed=ed, ee=ee, dw=dw, hh=h.hh, q=q, visit=v + 1, day=day,
                                          intv=intv, people=people))
    W.npersons = pid[0]
    _reinterview(np.random.default_rng([seed, P.REINT_SEED]), W)
    return W


def _between(rng, W, d, dw, q, hhs, new_household, taken):
    """a dwelling's households between two visits: statuses move on, adults leave, a household moves out (a new one moves
    in), a household splits (part of it forms a new household in the same dwelling, its lines numbered afresh)"""
    for h in list(hhs):
        if h.gone:
            continue
        alive = [p_ for p_ in h.members if p_.alive]
        for ag in range(len(AGE_MULT)):
            grp = [p_ for p_ in alive if p_.ag == ag]
            if grp:
                nxt = draw(rng, W.P[d][ag][[p_.true[q - 1] for p_ in grp]])
                for p_, s_ in zip(grp, nxt):
                    p_.true[q] = int(s_)
        for p_ in alive:
            if p_.rel != "head" and rng.random() < P.LEAVE:
                p_.alive = False
        if rng.random() < P.MOVE_OUT:
            h.gone = True
            W.moves.append((q, dw, h.hh))
            yr = 2026 + (q + 3) // 4
            hhs.append(Household(max(x.hh for x in hhs) + 1, new_household(yr, q, taken, d)))
            continue
        alive = [p_ for p_ in h.members if p_.alive]
        if len(alive) >= 3 and rng.random() < P.DSPLIT[d]:
            k = 1 + int(rng.integers(0, len(alive) - 2))
            movers = alive[-k:]
            moved = []
            for j, p_ in enumerate(movers):
                p_.alive = False
                moved.append(Person(p_.pid, p_.sex, p_.by, p_.bm, "head" if j == 0 else "other relative", j + 1,
                                    p_.true, p_.ag))
            nh = Household(max(x.hh for x in hhs) + 1, moved)
            hhs.append(nh)
            W.splits.append((q, dw, nh.hh, [p_.pid for p_ in moved]))


def _reinterview(rng, W):
    """each quarter a random 8 per cent of responding households is selected for the supervisors' reinterview of every
    adult interviewed in it; a few selected households leave before any attempt, and one supervisor's second-quarter
    workload in two districts was never attempted; the rest are completed within the window, completed late, refused or
    never contacted after three calls"""
    W.reint = []
    sup = {d: s for s, ds in P.SUPERVISORS.items() for d in ds}
    gap = P.SUPERVISOR_GAP
    outs = list(P.REINT_OUTCOMES)
    po = np.array([P.REINT_OUTCOMES[k] for k in outs])
    po = po / po.sum()
    for h in W.hhq:
        if rng.random() >= P.REINT_SHARE:
            continue
        qn = P.QUARTERS[h["q"]]
        never = rng.random() < P.NEVER_ATTEMPTED
        if qn == gap["quarter"] and h["d"] in gap["districts"] and rng.random() < gap["share"]:
            never = True
        out = "never" if never else outs[int(rng.choice(len(outs), p=po))]
        attempts = []
        if out != "never":
            first = h["day"] + dt.timedelta(days=int(rng.integers(2, 6)))
            calls = {"in_window": int(rng.integers(1, 3)), "late": int(rng.integers(2, 4)),
                     "refused": int(rng.integers(1, 3)), "no_contact": 3}[out]
            if out == "in_window":
                last = h["day"] + dt.timedelta(days=int(rng.integers(max(3, (first - h["day"]).days), 15)))
            elif out == "late":
                last = h["day"] + dt.timedelta(days=int(rng.integers(15, 31)))
            else:
                last = first + dt.timedelta(days=int(rng.integers(3, 12)))
            days = sorted({first + dt.timedelta(days=int(x)) for x in
                           np.linspace(0, max(0, (last - first).days), calls).round()})
            for i, day in enumerate(days):
                final = i == len(days) - 1
                res = {"in_window": "completed", "late": "completed", "refused": "refused",
                       "no_contact": "no contact"}[out] if final else "no contact"
                attempts.append((day, res))
        recs = []
        if out == "in_window":
            for p_ in h["people"]:
                reint = int(draw(rng, W.MR[[p_["true"]]])[0])
                # only a difference is reviewed with the respondent, and the review settles on the true status; two
                # readings that agree stand, right or wrong
                recs.append(dict(pid=p_["pid"], true=p_["true"], rec=p_["rec"], reint=reint,
                                 recon=p_["rec"] if reint == p_["rec"] else p_["true"]))
        W.reint.append(dict(h=h, sup=sup[h["d"]], out=out, attempts=attempts, recs=recs))


def clean_flows(W, d):
    """the district's true flows without sampling or reading error: each age group's long-run flows on its own rates,
    mixed in the shares of the district's persons due another visit"""
    w = np.zeros(len(AGE_MULT))
    ages = {}
    for h in W.hhq:
        if h["d"] == d and h["visit"] <= 3:
            for p in h["people"]:
                ages[p["pid"]] = p["ag"]
    for ag in ages.values():
        w[ag] += 1
    w = w / w.sum()
    return sum(w[g] * np.diag(W.pi[d][g]) @ W.P[d][g] for g in range(len(AGE_MULT)))
