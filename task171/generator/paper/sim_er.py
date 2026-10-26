"""Paper simulation 1 for the dovikizumab dose draw (task171 architecture 5, drawn in the task141 rework): does exposure
timing separate the dose calls?"""
import numpy as np, sys
from scipy.optimize import minimize

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 141
rng = np.random.default_rng(seed)
NA, NP = 360, 180
N = NA + NP
active = np.r_[np.ones(NA, bool), np.zeros(NP, bool)]
wt = np.exp(rng.normal(np.log(76), 0.22, N))
alb = rng.normal(39.5, 4.2, N)
crp = np.exp(rng.normal(np.log(7), 0.9, N))
mayo = rng.integers(6, 13, N)
biol = rng.random(N) < 0.45          # prior biologic failure
eta = rng.normal(0, 0.28, N)
V = 6.2 * (wt / 75) ** 0.55
CL0 = 0.20 * (wt / 75) ** 0.70 * (alb / 40) ** -0.6 * np.exp(eta)   # L/day

# latent disease: baseline prognosis, drug effect from FIRST-INTERVAL exposure (causal), remission at week 12
def conc_profile(dose, CLt, V, days):
    """one-compartment, IV bolus at days 0, 28, 56, clearance as a function of day; Euler at 0.25 day."""
    dt = 0.25
    t = np.arange(0, days + dt, dt)
    c = np.zeros((len(t), len(dose)))
    amt = np.zeros(len(dose))
    for i, ti in enumerate(t):
        if abs(ti - 0) < 1e-9 or abs(ti - 28) < 1e-9 or abs(ti - 56) < 1e-9:
            amt = amt + dose
        k = CLt(ti) / V
        c[i] = amt / V
        amt = amt * np.exp(-k * dt)
    return t, c

dose600 = np.where(active, 600.0, 0.0)
# first pass: clearance without response to get the causal early exposure
t, c0 = conc_profile(dose600, lambda ti: CL0, V, 84)
cavg_first = c0[(t >= 0) & (t < 28)].mean(axis=0)    # mean conc over days 0-28
EC50, EMAX = 4.0, 1.55
drug = np.where(active, EMAX * cavg_first / (EC50 + cavg_first), 0.0)
lp = -1.55 + 0.045 * (alb - 40) - 0.15 * (mayo - 9) - 0.55 * biol - 0.10 * np.log(crp / 7) + drug
p = 1 / (1 + np.exp(-lp))
rem = rng.random(N) < p
# reverse effect: remitters' clearance falls from day 28 by up to 32 per cent; non-remitters drift up 4 per cent
drop = np.where(rem, 0.32, -0.04)
def CLt(ti):
    f = 0.0 if ti < 21 else 1 - np.exp(-(ti - 21) / 18.0)
    return CL0 * (1 - drop * f)
t, c = conc_profile(dose600, CLt, V, 84)
def at(day):
    i = np.argmin(np.abs(t - day)); return c[i]
noise = lambda n: np.exp(rng.normal(0, 0.12, n))
d14 = at(14) * noise(N); tr28 = at(27.75) * noise(N); tr56 = at(55.75) * noise(N); s84 = at(84) * noise(N)
cavg_ind = c[(t >= 0) & (t <= 84)].mean(axis=0)

A = active
def fit(x, cov=True):
    X = [np.ones(A.sum()), np.log(x[A])]
    if cov:
        X += [(alb[A] - 40), (mayo[A] - 9), biol[A].astype(float), np.log(crp[A] / 7)]
    X = np.column_stack(X); y = rem[A].astype(float)
    nll = lambda b: np.sum(np.logaddexp(0, X @ b)) - y @ (X @ b)
    b = minimize(nll, np.zeros(X.shape[1]), method='BFGS').x
    return b, X

def predict(metric, cov, dose):
    b, X = fit(metric, cov)
    X2 = X.copy(); X2[:, 1] = np.log(metric[A] * dose / 600.0)
    pr = 1 / (1 + np.exp(-(X2 @ b)))
    g = biol[A]
    return b[1], pr[~g].mean() * 100, pr[g].mean() * 100

print('seed', seed, 'remission active %.1f placebo %.1f' % (rem[A].mean() * 100, rem[~A].mean() * 100))
for name, m in [('day14', d14), ('trough wk4', tr28), ('trough wk8', tr56), ('wk12', s84), ('cavg induction', cavg_ind)]:
    r = rem[A]
    print('%-15s remitter/non ratio %.2f' % (name, np.exp(np.log(m[A][r]).mean() - np.log(m[A][~r]).mean())))
    for cov in (False, True):
        out = []
        for d in (300, 450, 600):
            s, pn, pe = predict(m, cov, d)
            out.append((d, pn, pe))
        ref = out[-1]
        drops = ['%d: naive %.1f exp %.1f' % (d, ref[1] - pn, ref[2] - pe) for d, pn, pe in out[:-1]]
        call = next(d for d, pn, pe in out if ref[1] - pn <= 2.0 and ref[2] - pe <= 2.0)
        print('    cov=%-5s slope %.2f  drops %s  -> call %d' % (cov, s, '; '.join(drops), call))
