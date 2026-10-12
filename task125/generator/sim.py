"""Simulate the HLS: every quarterly intake of addresses, the households behind them, each member's labour market
status quarter by quarter, the wave-1 visits it takes to find someone at home, the telephone waves 2 to 5 and the
roster changes between them. The counterfactual six-visit intakes for July to December 2026 are kept for the checks
(never shipped)."""
import datetime as dt

import numpy as np

import world as W

STATES = np.array(["E", "U", "I"])


def _rng(*keys):
    return np.random.default_rng([W.SEED, W.SALT] + list(keys))


def _age_group_idx(age):
    return np.searchsorted(np.array(W.AGE_EDGES[1:]), age, side="right")


def _tables():
    g = W.AGE_GROUPS
    return (np.array([W.E_TO_U[x] for x in g]), np.array([W.U_TO_E[x] for x in g]), np.array([W.E_TO_I[x] for x in g]),
            np.array([W.I_TO_E[x] for x in g]), np.array([W.I_TO_U[x] for x in g]))


EU, UE, EI, IE, IU = _tables()


def step(status, age, cls_a, q, rng):
    """One quarter of the status chain (0 employed, 1 unemployed, 2 inactive)."""
    gi = _age_group_idx(age)
    m = W.MACRO[q]
    eu = EU[gi] * m * np.where(cls_a, W.CLASS_EU["A"], W.CLASS_EU["R"])
    ue = UE[gi] * np.where(cls_a, W.CLASS_UE["A"], W.CLASS_UE["R"])
    r = rng.random(status.size)
    out = status.copy()
    e, u, i = status == 0, status == 1, status == 2
    out[e & (r < eu)] = 1
    out[e & (r >= eu) & (r < eu + EI[gi])] = 2
    out[u & (r < ue)] = 0
    out[u & (r >= ue) & (r < ue + W.U_TO_I)] = 2
    out[i & (r < IE[gi])] = 0
    out[i & (r >= IE[gi]) & (r < IE[gi] + IU[gi])] = 1
    return out


def _ages(cls_a, size, rng):
    """Members' ages at intake: out-by-day households are working-age adults, the rest a mix."""
    ages, hh = [], []
    for h, (a, k) in enumerate(zip(cls_a, size)):
        if a:
            base = rng.choice([1, 2, 3], p=[0.55, 0.35, 0.10])
            first = rng.uniform(22, 62)
            mem = [first] + [float(np.clip(first + rng.normal(0, 4), 19, 66)) for _ in range(1, k)]
            if k >= 3:
                mem[-1] = rng.uniform(17, 24)
            del base
        else:
            kind = rng.choice(["older", "family", "young", "mixed"], p=[0.36, 0.30, 0.14, 0.20])
            if kind == "older":
                first = rng.uniform(62, 90)
                mem = [first] + [float(np.clip(first + rng.normal(0, 4), 55, 95)) for _ in range(1, k)]
            elif kind == "family":
                first = rng.uniform(32, 58)
                mem = [first, float(np.clip(first + rng.normal(0, 3), 25, 64))] + [rng.uniform(15, 24) for _ in range(2, k)]
                mem = mem[:k]
            elif kind == "young":
                mem = [rng.uniform(16, 30) for _ in range(k)]
            else:
                mem = [rng.uniform(20, 85) for _ in range(k)]
        for j in range(1, len(mem)):                  # clipped ages never give two members one birth date
            while any(abs(mem[j] - x) < 0.01 for x in mem[:j]):
                mem[j] += 0.37
        ages += mem
        hh += [h] * k
    return np.array(ages), np.array(hh)


def _initial_status(age, cls_a, rng):
    gi = _age_group_idx(age)
    p_inact = np.array([0.42, 0.14, 0.12, 0.13, 0.27, 0.72, 0.93])[gi]
    p_inact = np.where(cls_a, p_inact * 0.25, p_inact)
    r = rng.random(age.size)
    st = np.where(r < p_inact, 2, 0)
    st[(st == 0) & (rng.random(age.size) < np.where(cls_a, 0.02, 0.06))] = 1
    return st


def qmid(q):
    return dt.date(q[0], 3 * q[1] - 1, 15)


def age_at(dob, q):
    m = qmid(q)
    return m.year - dob.year - ((m.month, m.day) < (dob.month, dob.day))


def intake(c, cap=None):
    """One quarterly intake c = (year, q). Returns addresses, persons by wave and the wave-1 call history."""
    rng = _rng(*c)
    n = W.ISSUED_PER_INTAKE
    shares = np.array([r[2] for r in W.REGIONS])
    region = rng.choice(len(W.REGIONS), n, p=shares / shares.sum())
    district = np.array([rng.integers(1, W.DISTRICTS[W.RCODES[r]] + 1) for r in region])
    eligible = rng.random(n) >= W.INELIGIBLE
    p_a = np.array([r[3] for r in W.REGIONS])[region]
    cls_a = rng.random(n) < p_a
    size = np.where(cls_a, rng.choice([1, 2, 3], n, p=[0.42, 0.46, 0.12]), rng.choice([1, 2, 3, 4], n, p=[0.36, 0.40, 0.14, 0.10]))
    age0, hh = _ages(cls_a, size, rng)
    pa = cls_a[hh]
    sex = rng.choice([1, 2], age0.size)
    # birth dates from the age at the intake quarter's midpoint
    mid = dt.date(c[0], 3 * c[1] - 1, 15)
    dob = [mid - dt.timedelta(days=int(a * 365.25)) for a in age0]
    # burn-in of eight quarters to the intake
    q0 = W.qnext(c, -8)
    st = _initial_status(age0 - 2.0, pa, rng)
    for k in range(8):
        st = step(st, age0 - 2.0 + 0.25 * k, pa, W.qnext(q0, k), rng)
    statuses = [st]
    for k in range(1, W.WAVES):
        statuses.append(step(statuses[-1], age0 + 0.25 * k, pa, W.qnext(c, k), rng))
    # roster: a member may leave between waves (never the first)
    present = [np.ones(age0.size, bool)]
    first = np.r_[True, hh[1:] != hh[:-1]]
    for k in range(1, W.WAVES):
        leave = (~first) & (rng.random(age0.size) < 0.018)
        present.append(present[-1] & ~leave)
    # wave 1: visits until someone is found at home
    home = np.zeros(n, bool)
    for w0 in (1, 2):
        sel = statuses[0] == w0
        at = sel & (rng.random(age0.size) < (W.P_HOME_U if w0 == 1 else W.P_HOME_I))
        np.logical_or.at(home, hh[at], True)
    p = np.where(home, W.P_CONTACT_HOME, np.where(cls_a, W.P_CONTACT_AWAY["A"], W.P_CONTACT_AWAY["R"]))
    need = rng.geometric(p)
    refuse = rng.random(n) < W.REFUSAL
    maxv = W.CAP_VISITS if (cap if cap is not None else W.capped(c)) else W.MAX_VISITS
    contact = eligible & (need <= maxv)
    resp = [contact & ~refuse]
    # telephone waves
    for k in range(1, W.WAVES):
        hk = np.zeros(n, bool)
        for w0 in (1, 2):
            sel = (statuses[k] == w0) & present[k]
            at = sel & (rng.random(age0.size) < (W.P_HOME_U if w0 == 1 else W.P_HOME_I))
            np.logical_or.at(hk, hh[at], True)
        pr = np.where(hk, W.P_TEL_HOME, W.P_TEL_AWAY)
        resp.append(resp[-1] & (rng.random(n) < pr))
    # hours actually worked in the reference week, each quarter, for the employed
    hours = []
    for k in range(W.WAVES):
        away = rng.random(age0.size) < 0.065
        part = rng.random(age0.size) < np.where(pa, 0.15, 0.30)
        h = np.where(part, rng.normal(19.5, 6.0, age0.size), rng.normal(40.5, 5.5, age0.size))
        h = np.clip(np.round(h * 4) / 4, 1.0, 72.0)
        hours.append(np.where(away, 0.0, h))
    ages_q = [np.array([age_at(b, W.qnext(c, k)) for b in dob]) for k in range(W.WAVES)]
    return dict(intake=c, ages_q=ages_q, region=region, district=district, eligible=eligible, cls_a=cls_a, size=size, hh=hh, age0=age0,
                sex=sex, dob=dob, statuses=statuses, present=present, home=home, need=need, refuse=refuse,
                maxv=maxv, resp=resp, hours=hours)


def simulate_all():
    """Every intake whose waves fall in the person file, and the six-visit counterfactuals of the capped intakes."""
    intakes = {c: intake(c) for c in W.qrange(W.FIRST_INTAKE, W.LAST_Q)}
    counterfactual = {c: intake(c, cap=False) for c in intakes if W.capped(c)}
    return dict(intakes=intakes, counterfactual=counterfactual)
