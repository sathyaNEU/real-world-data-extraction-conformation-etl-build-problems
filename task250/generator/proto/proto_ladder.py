"""Prototype the full ladder for the next-birthday selection-accuracy design (clean truth, no Layer 1 mess).
Six surveys x two modes. Each survey posts its first letter on one day. Adult birthdays seasonal.
Rungs: R0 confirmation item, R1 household-grid demographic test, R2 male share in mixed couples,
R3 uniform-null order statistic, R4 empirical-null order statistic (golden route), R4b stream's own single adults."""
import numpy as np
from scipy.optimize import minimize_scalar
import sys

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 250
AMP = float(sys.argv[2]) if len(sys.argv) > 2 else 0.16
rng = np.random.default_rng(SEED)
DAYS = 365
LINE = 0.85

x = np.arange(DAYS)
# a spring peak (day 100 ~ 10 April) with a smaller late-summer shoulder
dens = 1 + AMP * np.cos(2 * np.pi * (x - 100) / DAYS) + 0.35 * AMP * np.cos(4 * np.pi * (x - 250) / DAYS)
dens = dens / dens.sum()
cdf_year = np.cumsum(dens)

# surveys: letter day-of-year, completes web/paper, compliance web/paper, substitution profile
SURVEYS = [
    # name, letter_doy, n_web, n_paper, c_web, c_paper, profile
    ('HLTH', 19, 13000, 8000, 0.80, 0.66, 'oldest_woman'),
    ('ICT',  75, 14000, 5000, 0.64, 0.60, 'youngest'),
    ('SAFE', 131, 12000, 8500, 0.73, 0.79, 'oldest'),
    ('CULT', 196, 12500, 7000, 0.83, 0.62, 'random'),
    ('TIME', 250, 11500, 7500, 0.72, 0.84, 'woman'),
    ('WORK', 306, 13500, 6500, 0.62, 0.78, 'man'),
]
KPROBS = [0.38, 0.385, 0.15, 0.06, 0.025]  # k = 1..5

def make_household():
    k = rng.choice([1, 2, 3, 4, 5], p=KPROBS)
    if k == 1:
        sex = [rng.random() < 0.58]  # True = woman (single-adult households lean female/older)
        age = [int(rng.integers(20, 90))]
    else:
        sex = []; age = []
        a0 = int(rng.integers(22, 80))
        sex.append(rng.random() < 0.5); age.append(a0)
        sex.append(not sex[0] if rng.random() < 0.85 else rng.random() < 0.5); age.append(int(np.clip(a0 + rng.integers(-6, 7), 18, 92)))
        for _ in range(k - 2):
            sex.append(rng.random() < 0.5); age.append(int(rng.integers(16, max(17, a0 - 18))) if a0 > 40 else int(rng.integers(16, 90)))
    b = rng.choice(DAYS, size=k, p=dens)
    return k, np.array(sex), np.array(age), b

def pick_substitute(profile, sex, age):
    k = len(sex)
    if profile == 'random' or rng.random() < 0.35:
        return int(rng.integers(k))
    if profile == 'oldest_woman':
        cand = np.where(sex)[0]
        if len(cand) == 0: cand = np.arange(k)
        return int(cand[np.argmax(age[cand])])
    if profile == 'youngest':
        return int(np.argmin(age))
    if profile == 'oldest':
        return int(np.argmax(age))
    if profile == 'woman':
        cand = np.where(sex)[0]
        return int(rng.choice(cand)) if len(cand) else int(rng.integers(k))
    if profile == 'man':
        cand = np.where(~sex)[0]
        return int(rng.choice(cand)) if len(cand) else int(rng.integers(k))
    return int(rng.integers(k))

rows = []
for (name, doy, nweb, npap, cweb, cpap, prof) in SURVEYS:
    for mode, n, c in (('web', nweb, cweb), ('paper', npap, cpap)):
        for _ in range(n):
            k, sex, age, b = make_household()
            D = (b - doy - 1) % DAYS + 1
            if k == 1:
                j = 0; comp = True
            elif rng.random() < c:
                j = int(np.argmin(D)); comp = True
            else:
                j = pick_substitute(prof, sex, age); comp = False
            is_min = D[j] == D.min()
            says_no = (not comp) and (not is_min) and rng.random() < 0.12
            rows.append((name, mode, doy, k, D[j], bool(is_min), bool(sex[j]), age[j], sex.mean(), age.mean(),
                         int(k == 2 and sex[0] != sex[1]), says_no))

import collections
cells = collections.OrderedDict()
for r in rows:
    cells.setdefault((r[0], r[1]), []).append(r)

def null_FD(doy):
    order = (np.arange(1, DAYS + 1) + doy) % DAYS
    f = dens[order]
    return f, np.cumsum(f)

single_b = []  # pooled single-adult birthdays (recover birthday day from D and doy)
for r in rows:
    if r[3] == 1:
        single_b.append((r[4] + r[2]) % DAYS)
emp = np.bincount(np.array(single_b), minlength=DAYS).astype(float)
# light smoothing by a 15-day circular moving average
ker = np.ones(15) / 15
emp_s = np.convolve(np.concatenate([emp[-7:], emp, emp[:7]]), ker, mode='valid')
emp_s = emp_s / emp_s.sum()

def mle(cellrows, f_func, F_func):
    m = [r for r in cellrows if r[3] >= 2]
    k = np.array([r[3] for r in m]); D = np.array([r[4] for r in m]).astype(int); doy = m[0][2]
    f, F = f_func(doy), F_func(doy)
    Fm = F[D - 1] - f[D - 1]
    comp = k * (1 - Fm) ** (k - 1)
    nll = lambda c: -np.sum(np.log(c * comp + (1 - c)))
    c = minimize_scalar(nll, bounds=(0, 1), method='bounded').x
    return c + (1 - c) * np.mean(1 / k)

def uniform_f(doy): return np.full(DAYS, 1 / DAYS)
def uniform_F(doy): return np.arange(1, DAYS + 1) / DAYS
def emp_f(doy):
    order = (np.arange(1, DAYS + 1) + doy) % DAYS
    return emp_s[order]
def emp_F(doy): return np.cumsum(emp_f(doy))

print('AMP', AMP, 'SEED', SEED, 'line', LINE)
print('%-6s %-5s %6s %6s | %6s %6s %6s %6s %6s %6s %6s' % ('surv', 'mode', 'n2+', 'truth', 'R0conf', 'R1grid', 'R2coup', 'R3unif', 'R4emp', 'R4own', 'err4'))
sets = collections.defaultdict(set)
for (name, mode), cr in cells.items():
    m = [r for r in cr if r[3] >= 2]
    truth = np.mean([r[5] for r in m])
    conf = 1 - np.mean([r[11] for r in m])
    # R1: grid test: excess of respondent female share over household female share, and age excess; convert
    # with the analyst's assumption that every substitute is the household's oldest woman
    fem_exc = np.mean([r[6] - r[8] for r in m])
    # R2: male share in mixed couples vs 0.5, assuming substitutes are women
    cp = [r for r in m if r[10] == 1]
    male = 1 - np.mean([r[6] for r in cp])
    r2 = 1 - 2 * max(0.0, 0.5 - male)  # crude: share of couples selected correctly
    r1 = 1 - min(1.0, abs(fem_exc) / 0.25)
    r3 = mle(cr, uniform_f, uniform_F)
    r4 = mle(cr, emp_f, emp_F)
    # R4b: the stream's own single adults as the null
    s1 = [r for r in cr if r[3] == 1]
    own = np.bincount(np.array([(r[4] + r[2]) % DAYS for r in s1]), minlength=DAYS).astype(float)
    own_s = np.convolve(np.concatenate([own[-30:], own, own[:30]]), np.ones(61) / 61, mode='valid'); own_s /= own_s.sum()
    of = lambda doy: own_s[(np.arange(1, DAYS + 1) + doy) % DAYS]
    oF = lambda doy: np.cumsum(of(doy))
    r4b = mle(cr, of, oF)
    for lab, v in (('truth', truth), ('R0', conf), ('R1', r1), ('R2', r2), ('R3', r3), ('R4', r4), ('R4b', r4b)):
        if v < LINE: sets[lab].add('%s-%s' % (name, mode))
    print('%-6s %-5s %6d %6.3f | %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f %+6.3f' % (name, mode, len(m), truth, conf, r1, r2, r3, r4, r4b, r4 - truth))
print()
for lab in ('truth', 'R0', 'R1', 'R2', 'R3', 'R4', 'R4b'):
    print('%-5s switch: %s' % (lab, sorted(sets[lab])))
