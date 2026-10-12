"""The records the main call reads: the national population behind the contact survey, the survey itself (its
participants' reported contacts and the reciprocity-corrected matrix it publishes), the department's projection of
the region's residents at 1 January 2028, the national immunity profile and the options paper's figures."""
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


# --- the contact model: contacts per participant per day by single year, then by survey group -------------------------
def _gauss(d, s):
    return np.exp(-d * d / (2.0 * s * s))


def contact_single_year(nat, p=None):
    """M[a, b]: mean daily contacts a participant aged b has with people aged a (single years 0-89, 90 = 90 and over),
    built from school, work, household and community components and made reciprocal on the national population."""
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

    M = np.zeros((91, 91))
    s_int = np.interp(b, [3, 4, 8, 12, 13, 17, 18, 19], [0, p["s_prim"], p["s_prim"], p["s_mid"], p["s_sec"], p["s_sec"],
                                                         p["s_sec"] * 0.6, 0])
    s_sig = np.interp(b, [4, 12, 13, 18], [p["sig_prim"], p["sig_prim"], p["sig_sec"], p["sig_sec"]])
    M += comp(s_int, _gauss(D, s_sig[None, :]) * ((A >= 3) & (A <= 20)))
    w_int = np.interp(b, [17, 18, 22, 25, 60, 66, 67], [0, p["work"] * 0.8, p["work"], p["work"], p["work"],
                                                         p["work"] * 0.5, 0])
    M += comp(w_int, _gauss(D, p["sig_work"]) * ((A >= 18) & (A <= 70)))
    pc = np.interp(b, [0, 18, 25, 30, 45, 55, 70, 90], [p["hh_pc"], p["hh_pc"], p["hh_pc"] * 0.5, p["hh_pc"], p["hh_pc"],
                                                         p["hh_pc"] * 0.6, p["hh_pc"] * 0.3, p["hh_pc"] * 0.2])
    M += comp(pc, _gauss(D - 30, 5) + _gauss(D + 30, 5))
    M += comp(np.where(b >= 20, p["hh_partner"], 0.0), _gauss(D, 3) * (A >= 20))
    M += comp(np.where(b <= 20, p["hh_sib"], 0.0), _gauss(D, 3) * (A <= 22))
    c_int = np.interp(b, [0, 5, 15, 25, 65, 80, 90], [p["comm"] * 0.6, p["comm"], p["comm"] * 1.2, p["comm"],
                                                       p["comm"] * 0.9, p["comm"] * 0.6, p["comm"] * 0.5])
    M += comp(c_int, np.ones((91, 91)))
    T = M * pop[None, :]
    T = 0.5 * (T + T.T)
    return T / pop[None, :], pop


def contact_groups(nat, p=None):
    """C[i, j]: the true mean daily contacts a person in survey group j has with group i."""
    M, pop = contact_single_year(nat, p)
    g = np.array([group_of_age(min(a, 100)) for a in range(91)])
    C = np.zeros((W.NG, W.NG))
    for i in range(W.NG):
        for j in range(W.NG):
            ri, cj = g == i, g == j
            C[i, j] = (M[np.ix_(ri, cj)].sum(axis=0) * pop[cj]).sum() / pop[cj].sum()
    return C


def survey(nat, p=None, seed=None):
    """The survey: each participant's reported contacts by group (negative binomial around the true means), the
    weighted mean matrix by participant group, and the matrix the survey publishes, corrected for reciprocity on the
    national population and rounded to two decimals. Returned with participant rows: P[participant, contact]."""
    seed = W.SURVEY_SEED if seed is None else seed
    rng = np.random.default_rng(seed)
    C = contact_groups(nat, p)
    raw = np.zeros((W.NG, W.NG))
    k = W.SURVEY_DISPERSION
    for j in range(W.NG):
        lam = C[:, j]
        draws = rng.negative_binomial(k, k / (k + lam[None, :]), size=(W.SURVEY_PARTICIPANTS[j], W.NG))
        raw[j, :] = draws.mean(axis=0)
    N = to_groups(nat)
    T = raw * N[:, None]                  # total contacts reported by group j's population with group i
    pub = (0.5 * (T + T.T)) / N[:, None]
    return np.round(pub, 2), raw, C


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
