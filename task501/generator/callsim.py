"""The records the main call reads: the national population behind the contact survey, the survey itself (its
participants' reported contacts and the reciprocity-corrected matrix it publishes), the department's projection of
the region's residents at 1 January 2028, the national immunity profile and the options paper's figures."""
import datetime as dt

import numpy as np

import world as W

AGES = np.arange(0, 101)          # 100 = 100 and over


def _shape(knots, vals):
    return np.interp(AGES, knots, vals)


def national_2023():
    v = _shape(W.NAT_KNOTS, W.NAT_SHAPE)
    v = v / v.sum() * W.NAT_TOTAL_2023
    return np.round(v).astype(int)


def regional_2028():
    """Projected residents at 1 January 2028 by county and single year of age (index 100 = 100 and over)."""
    v = _shape(W.NAT_KNOTS, W.REG_SHAPE)
    v = v / v.sum() * W.REG_TOTAL_2028
    out = {}
    shares = {}
    for c in W.COUNTIES:
        tilt = W.COUNTY_AGE_TILT[c] * np.maximum(AGES - 40, 0) - W.COUNTY_AGE_TILT[c] * np.maximum(18 - AGES, 0) * 0.5
        shares[c] = np.maximum(W.COUNTY_SHARE[c] + tilt, 0.01)
    tot = sum(shares.values())
    rng = np.random.default_rng(W.SEED + 11)
    for c in W.COUNTIES:
        s = shares[c] / tot
        noise = 1 + rng.normal(0, 0.012, size=len(AGES))
        out[c] = np.round(v * s * noise).astype(int)
    return out


def group_of_age(a):
    for k, (lo, hi) in enumerate(W.GROUPS):
        if lo <= a <= hi:
            return k
    raise ValueError(a)


GROUP_OF_AGE = np.array([group_of_age(a) for a in AGES])


def to_groups(v):
    return np.array([v[GROUP_OF_AGE == g].sum() for g in range(W.NG)], dtype=float)


def published_population(nat):
    """The survey's Table 1 population by group: the statistics office's estimate for 1 January 2023, each group within
    about a quarter of a per cent of the national shape's total (its own stream, so nothing else moves)."""
    rng = np.random.default_rng(W.NAT_PUBLISHED_SEED)
    N = to_groups(nat)
    return np.round(N * (1 + rng.normal(0, W.NAT_PUBLISHED_SD, size=len(N)))).astype(int)


# --- the contact survey: contacts per day by setting and single year, four kinds of day ---------------------------
def _gauss(d, s):
    return np.exp(-d * d / (2.0 * s * s))


def components(nat, day, p=None):
    """Expected contacts a person aged b has with people aged a on a day of kind `day` ('tw' a school-term weekday,
    'te' a term weekend day, 'hw' a summer-holiday weekday, 'he' a holiday weekend day), by setting, single years
    0-89 and 90 for 90 and over: {setting: M[a, b]}, before reciprocity."""
    p = p or W.CONTACT
    ages = np.arange(0, 91).astype(float)
    pop = nat[:91].astype(float).copy()
    pop[90] = nat[90:].sum()
    A = ages[:, None]
    B = ages[None, :]
    D = A - B
    b = ages

    def comp(intensity, kernel):
        K = kernel * pop[:, None]
        K = K / np.maximum(K.sum(axis=0, keepdims=True), 1e-12)
        return K * intensity[None, :]
    out = {}
    term = day[0] == "t"
    wkday = day[1] == "w"
    z = np.zeros((91, 91))
    school = z.copy()
    if term and wkday:
        sp = np.interp(b, [3, 4, 12, 12.5], [0, p["s_prim"], p["s_prim"], 0])
        school += comp(sp, _gauss(D, p["sig_prim"]) * ((A >= 4) & (A <= 13)))
        ss = np.interp(b, [12, 13, 17, 18, 19], [0, p["s_sec"], p["s_sec"], p["s_sec"] * 0.5, 0])
        school += comp(ss, _gauss(D, p["sig_sec"]) * ((A >= 12) & (A <= 19)))
        tch = np.where((b >= 4) & (b <= 18), p["teach"], 0.0)
        school += comp(tch, ((A >= 25) & (A <= 64)).astype(float))
        cl = np.interp(b, [17, 18, 22, 24], [0, p["col"], p["col"], 0])
        school += comp(cl, _gauss(D, p["sig_col"]) * ((A >= 17) & (A <= 26)))
    out["school"] = school
    care = z.copy()
    if wkday:
        cr = np.interp(b, [0, 1, 4, 5], [0, p["creche"], p["creche"], 0])
        care += comp(cr, _gauss(D, 1.0) * (A <= 5))
    out["childcare"] = care
    wk = np.interp(b, [17, 18, 22, 25, 60, 66, 67], [0, p["work"] * 0.7, p["work"], p["work"], p["work"],
                                                     p["work"] * 0.5, 0])
    f = 1.0
    if not term:
        f *= p["work_hol"]
    if not wkday:
        f *= p["work_wkend"]
    out["work"] = comp(wk * f, _gauss(D, p["sig_work"]) * ((A >= 18) & (A <= 70)))
    pc = np.interp(b, [0, 18, 25, 30, 45, 55, 70, 90], [p["hh_pc"], p["hh_pc"], p["hh_pc"] * 0.5, p["hh_pc"], p["hh_pc"],
                                                         p["hh_pc"] * 0.6, p["hh_pc"] * 0.3, p["hh_pc"] * 0.2])
    home = comp(pc, _gauss(D - 31, 5) + _gauss(D + 31, 5))
    home += comp(np.where(b >= 20, p["hh_partner"], 0.0), _gauss(D, 3) * (A >= 20))
    home += comp(np.where(b <= 20, p["hh_sib"], 0.0), _gauss(D, 3) * (A <= 22))
    out["home"] = home
    cm = np.interp(b, [0, 5, 15, 25, 65, 80, 90], [p["comm"] * 0.5, p["comm"] * 0.8, p["comm"], p["comm"],
                                                    p["comm"] * 0.9, p["comm"] * 0.6, p["comm"] * 0.5])
    if not wkday:
        cm = cm * p["comm_wkend"]
    out["other"] = comp(cm, np.ones((91, 91)))
    lt = np.interp(b, [10, 13, 16, 20, 25, 30], [0, p["leis_teen"], p["leis_teen"], p["leis_teen"], p["leis_teen"] * 0.6, 0])
    if not term:
        lt = lt * p["leis_hol"]
    if not wkday:
        lt = lt * p["leis_wkend"]
    out["leisure"] = comp(lt, _gauss(D, p["sig_leis"]) * ((A >= 10) & (A <= 32)))
    return out, pop


def reciprocal_components(nat, day, p=None):
    """Each setting made reciprocal on the population: the contacts a group has with another equal, in total, those
    the other has with it."""
    comps, pop = components(nat, day, p)
    out = {}
    for k, M in comps.items():
        T = M * pop[None, :]
        T = 0.5 * (T + T.T)
        out[k] = T / pop[None, :]
    return out, pop


GROUP_OF_AGE_91 = np.array([group_of_age(min(a, 100)) for a in range(91)])
DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def _dates_by_weekday(a, b):
    out = {k: [] for k in range(7)}
    d = a
    while d <= b:
        out[d.weekday()].append(d)
        d += dt.timedelta(days=1)
    return out


def survey(nat, p=None, seed=None):
    """The survey's public use file. Each participant kept a diary for one assigned day in one of the two fieldwork
    periods; the day's contacts are drawn around the expected contacts for the participant's single year of age and
    kind of day, with a participant-level multiplier, up to the diary's 45 lines. Returns (participants, contacts):
    participants as dicts (part, band, age, date, period); contacts as tuples (part, contact band or -1 for an age
    the participant could not give, setting drawn from)."""
    seed = W.SURVEY_SEED if seed is None else seed
    rng = np.random.default_rng(seed)
    pop = nat[:91].astype(float).copy()
    pop[90] = nat[90:].sum()
    comps = {}
    for day in ("tw", "te", "hw", "he"):
        comps[day], _ = reciprocal_components(nat, day, p)
    parts, contacts = [], []
    pid = 0
    for period, a, b, n in W.SURVEY_PERIODS:
        wd = _dates_by_weekday(a, b)
        for band in range(W.NG):
            ages = np.where(GROUP_OF_AGE_91 == band)[0]
            w = pop[ages] / pop[ages].sum()
            per_day = n // 7
            for dow in range(7):
                for _ in range(per_day):
                    d = wd[dow][int(rng.integers(0, len(wd[dow])))]
                    age = int(rng.choice(ages, p=w))
                    wk = d.weekday() < 5
                    day = ("t" if period == "May" else "h") + ("w" if wk else "e")
                    lam = {s: comps[day][s][:, age] for s in comps[day]}
                    mult = rng.gamma(W.SURVEY_DISPERSION, 1.0 / W.SURVEY_DISPERSION)
                    pid += 1
                    parts.append(dict(part=pid, band=band, age=age, date=d, period=period))
                    cnt = []
                    for s, v in lam.items():
                        nn = rng.poisson(v * mult)
                        for a_ in np.nonzero(nn)[0]:
                            cnt.extend([(s, int(a_))] * int(nn[a_]))
                    if len(cnt) > W.SURVEY_CAP:
                        idx = rng.choice(len(cnt), size=W.SURVEY_CAP, replace=False)
                        cnt = [cnt[i] for i in sorted(idx)]
                    for s, a_ in cnt:
                        cb = int(GROUP_OF_AGE_91[a_]) if rng.random() >= W.SURVEY_UNKNOWN_AGE else -1
                        contacts.append((pid, cb, s, a_))
    return parts, contacts


def survey_matrix(parts, contacts, periods=None, unknown="drop"):
    """C[i, j]: mean contacts a participant in band j reported with band i, over the diaries of the given periods
    (None: every diary). unknown: 'drop' leaves contacts of unknown age out; 'spread' shares them over the
    participant band's known bands in proportion."""
    band = {q["part"]: q["band"] for q in parts if periods is None or q["period"] in periods}
    n = np.zeros(W.NG)
    for q in parts:
        if q["part"] in band:
            n[q["band"]] += 1
    C = np.zeros((W.NG, W.NG))
    unk = np.zeros(W.NG)
    for c in contacts:
        j = band.get(c[0])
        if j is None:
            continue
        if c[1] < 0:
            unk[j] += 1
        else:
            C[c[1], j] += 1
    if unknown == "spread":
        C = C + unk[None, :] * C / np.maximum(C.sum(axis=0, keepdims=True), 1e-9)
    return C / n[None, :]


# --- the profile and the options ------------------------------------------------------------------------------------
def profile():
    v, basis = W.profile_values()
    return v, basis


def immune_by_age(prof):
    """Share immune by age at 1 January 2028 (age = 2027 - year of birth; 100 and over at the 1927-and-earlier value)."""
    out = np.zeros(len(AGES))
    for a in AGES:
        y = max(2027 - a, 1927)
        out[a] = prof[y] / 100.0
    return out


def options_paper(reg_total, prof):
    """Each option's people (projection), estimated susceptible and expected people made immune, per year-of-birth span;
    E carries its two spans as the paper lists them."""
    imm = immune_by_age(prof)
    rows = {}
    for k in W.OPTION_KEYS:
        o = W.OPTIONS[k]
        lo, hi = o["years"]
        spans = [(lo, hi)] if k != "E" else [(1993, 1997), (1998, 2002)]
        parts = []
        for a, b in spans:
            ages = [2027 - y for y in range(a, b + 1)]
            people = int(sum(reg_total[x] for x in ages))
            sus = float(sum(reg_total[x] * (1 - imm[x]) for x in ages))
            made = int(round(sus * o["uptake"] * W.EFFECTIVENESS, -1))
            parts.append(dict(years=(a, b), people=people, susceptible=int(round(sus)), made=made))
        rows[k] = parts
    return rows
