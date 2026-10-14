"""The main call computed from the main-call inputs as the pack carries them: the golden (the dominant eigenvalue of
the next-generation matrix built from the contact diaries kept in school term, scaled to R0 at full susceptibility),
every defensible variant of it, and every rung below it, including the same eigenvalue on every diary in the survey.
Used by the generator's golden and checks; verify.py recomputes the golden on its own code path."""
import numpy as np

import world as W


def spectral_radius(M):
    return float(np.max(np.abs(np.linalg.eigvals(M))))


def term_diary(date):
    """The survey's first fieldwork period, 2 to 26 May 2023, school term; the second, 3 July to 18 August 2023, fell
    in the school summer holidays."""
    return date < "2023-06-01"


def summer_diary(date):
    return date >= "2023-06-01"


def survey_matrix(parts, contacts, select=None, unknown="drop"):
    """C[i, j]: mean contacts a participant in band j reported with band i, over the diaries whose date `select`
    accepts (None: every diary). parts: (part_id, band, date); contacts: (part_id, band or -1 for Unknown).
    unknown: 'drop' leaves contacts of unknown age out; 'spread' shares them over the participant band's known bands
    in proportion."""
    band = {p: b for p, b, d in parts if select is None or select(d)}
    n = np.zeros(W.NG)
    for b in band.values():
        n[b] += 1
    C = np.zeros((W.NG, W.NG))
    unk = np.zeros(W.NG)
    for p, cb in contacts:
        j = band.get(p)
        if j is None:
            continue
        if cb < 0:
            unk[j] += 1
        else:
            C[cb, j] += 1
    if unknown == "spread":
        C = C + unk[None, :] * C / np.maximum(C.sum(axis=0, keepdims=True), 1e-9)
    return C / n[None, :]


class CallInputs:
    """profile: {year_of_birth: per cent immune} (1927 = 1927 and earlier); persons: {age: residents} (100 = 100 and
    over); yob: {age: year of birth} as the projection states it; P: survey matrix [participant band, contact band];
    natpop: the codebook's population by band; options: {key: [ {years, people, susceptible, made} ... ]}."""

    def __init__(self, profile, persons, yob, P, natpop, options):
        self.profile, self.persons, self.yob, self.P, self.natpop, self.options = profile, persons, yob, P, natpop, options
        self.ages = sorted(persons)
        self.group = {a: next(k for k, (lo, hi) in enumerate(W.GROUPS) if lo <= a <= hi) for a in self.ages}
        self.survey = None

    def with_matrix(self, P):
        out = CallInputs(self.profile, self.persons, self.yob, P, self.natpop, self.options)
        out.survey = self.survey
        return out

    def matrix(self, select=None, unknown="drop"):
        """The survey matrix over the selected diaries, participant rows."""
        parts, contacts = self.survey
        return survey_matrix(parts, contacts, select, unknown).T

    def sus_age(self):
        return {a: self.persons[a] * (1 - self.profile[self.yob[a]] / 100.0) for a in self.ages}

    def groups(self, values):
        out = np.zeros(W.NG)
        for a, v in values.items():
            out[self.group[a]] += v
        return out

    def N(self):
        return self.groups(self.persons)

    def scenario_sus(self, key, alloc="sus"):
        """Susceptible people by age with option `key` delivered (None = no catch-up). The option's people made immune
        come off the ages of each span it covers, in proportion to their susceptibles (alloc='sus') or people ('pop')."""
        S = self.sus_age()
        if key is None:
            return S
        S = dict(S)
        for part in self.options[key]:
            lo, hi = part["years"]
            ages = [a for a in self.ages if lo <= self.yob[a] <= hi]
            base = {a: (S[a] if alloc == "sus" else self.persons[a]) for a in ages}
            tot = sum(base.values())
            for a in ages:
                S[a] -= part["made"] * base[a] / tot
        return S


def R_eigen(inp, key=None, P=None, norm="eig", share="weighted", alloc="sus", drop_70=False):
    """The reproduction number as the dominant eigenvalue of q diag(s) P^T. norm: 'eig' scales q so a wholly susceptible
    region has R0 (the golden); 'cbar' scales by the population's mean daily contacts (refused by standard 3.2)."""
    P = inp.P if P is None else P
    S = inp.scenario_sus(key, alloc)
    N = inp.N()
    if share == "weighted":
        s = inp.groups(S) / N
    else:   # a plain mean of the group's years
        s = np.zeros(W.NG)
        cnt = np.zeros(W.NG)
        for a in inp.ages:
            s[inp.group[a]] += S[a] / inp.persons[a]
            cnt[inp.group[a]] += 1
        s = s / cnt
    K = s[:, None] * P.T
    if drop_70:
        K = K[:-1, :-1]
        Pq = P[:-1, :-1]
    else:
        Pq = P
    if norm == "eig":
        q = W.R0 / spectral_radius(Pq)
    else:
        cbar = (Pq.sum(axis=1) * N[:len(Pq)]).sum() / N[:len(Pq)].sum()
        q = W.R0 / cbar
    return spectral_radius(q * K)


def scenarios(inp, **kw):
    return {("none" if k is None else k): R_eigen(inp, k, **kw) for k in [None] + W.OPTION_KEYS}


def R_average(inp, key=None):
    """Rung 0: R0 times the region's susceptible share."""
    S = inp.scenario_sus(key)
    return W.R0 * sum(S.values()) / sum(inp.persons.values())


def R_contact_weighted(inp, key=None, P=None):
    """Rung 1: R0 times each group's susceptible share weighted by its share of all contacts."""
    P = inp.P if P is None else P
    S = inp.scenario_sus(key)
    N = inp.N()
    s = inp.groups(S) / N
    c = P.sum(axis=1)          # a participant's daily contacts by group
    w = N * c
    return W.R0 * float((s * w).sum() / w.sum())


def matrix_variants(inp, P=None):
    """A survey matrix under each defensible treatment: as computed, transposed, made reciprocal on the codebook's
    national population or on the region's projection, density-adjusted to the region's age structure."""
    P = inp.P if P is None else P
    Nn = inp.natpop
    Nr = inp.N()

    def recip(Npop):
        T = P * Npop[:, None]
        return (0.5 * (T + T.T)) / Npop[:, None]
    dens = P * ((Nr / Nr.sum()) / (Nn / Nn.sum()))[None, :]
    return {"as computed": P, "transposed": P.T, "reciprocal national": recip(Nn), "reciprocal region": recip(Nr),
            "density region": dens}


def golden(inp):
    return scenarios(inp)


def family(inp, select=term_diary):
    """Every defensible golden-family member: the diaries' unknown ages dropped or spread, x matrix treatment x share
    weighting x allocation."""
    out = {}
    for unk in ("drop", "spread"):
        P0 = inp.matrix(select, unk)
        for mname, M in matrix_variants(inp, P0).items():
            for share in ("weighted", "plain"):
                for alloc in ("sus", "pop"):
                    out[(unk, mname, share, alloc)] = scenarios(inp, P=M, share=share, alloc=alloc)
    return out


def flip_people(inp, key="B", lo=0, hi=6000):
    """The people made immune at which option `key`'s reproduction number reaches one (bisection on the paper's
    figure, the span split kept in the paper's proportions)."""
    base = inp.options[key]
    tot = sum(p["made"] for p in base)

    def r_at(m):
        saved = inp.options[key]
        inp.options[key] = [dict(p, made=m * p["made"] / tot) for p in base]
        try:
            return R_eigen(inp, key)
        finally:
            inp.options[key] = saved
    a, b = lo, hi
    for _ in range(60):
        mid = 0.5 * (a + b)
        if r_at(mid) > 1.0:
            a = mid
        else:
            b = mid
    return 0.5 * (a + b)


def round1(x):
    """One decimal, half away from zero, on the unrounded figure."""
    return float(np.floor(x * 10 + 0.5) / 10)


def edge_distance(x):
    """Distance from x to the nearest one-decimal rounding edge (x.x5)."""
    f = x * 10 - np.floor(x * 10)
    return abs(f - 0.5) / 10
