"""Paper simulation 2: induction dose for phase 3 (300, 600, 1200 mg) from a 600 mg phase 2.
Closed-form one-compartment concentrations with clearance that falls after day 21 in remitters."""
import numpy as np, sys
from scipy.optimize import minimize

def run(seed, NA=660, NP=300, verbose=True):
    rng = np.random.default_rng(seed)
    N = NA + NP
    act = np.r_[np.ones(NA, bool), np.zeros(NP, bool)]
    wt = np.exp(rng.normal(np.log(74), 0.22, N))
    alb = rng.normal(38.5, 4.5, N)
    crp = np.exp(rng.normal(np.log(8), 0.95, N))
    mayo = rng.integers(6, 13, N)
    biol = rng.random(N) < 0.48
    eta = rng.normal(0, 0.33, N)
    V = 5.8 * (wt / 74) ** 0.6
    CL0 = 0.21 * (wt / 74) ** 0.8 * (alb / 38.5) ** -0.5 * (crp / 8) ** 0.08 * np.exp(eta)
    # causal exposure: mean concentration days 0-84 with baseline clearance, doses at 0, 28, 56 (bolus approx)
    k0 = CL0 / V
    def cavg_base(dose):
        # average over 0-84 of superposed exponentials
        tot = 0.0
        for td in (0, 28, 56):
            T = 84 - td
            tot = tot + dose / V * (1 - np.exp(-k0 * T)) / k0
        return tot / 84
    c_causal = np.where(act, cavg_base(600.0), 0.0)
    EC50, EMAX = 3.0, 1.60
    def drug(c):
        return EMAX * c / (EC50 + c)
    lp_base = -1.70 + 0.040 * (alb - 38.5) - 0.16 * (mayo - 9) - 0.60 * biol - 0.12 * np.log(crp / 8)
    p = 1 / (1 + np.exp(-(lp_base + np.where(act, drug(c_causal), 0.0))))
    rem = rng.random(N) < p
    drop = np.where(rem, 0.33, -0.05)
    # observed concentrations with time-varying clearance: integrate numerically on a 0.5 day grid
    dt = 0.5
    grid = np.arange(0, 84 + dt, dt)
    amt = np.zeros(N); conc = np.zeros((len(grid), N))
    for i, t in enumerate(grid):
        if t in (0.0, 28.0, 56.0):
            amt = amt + np.where(act, 600.0, 0.0)
        f = 0.0 if t < 21 else 1 - np.exp(-(t - 21) / 16.0)
        k = CL0 * (1 - drop * f) / V
        conc[i] = amt / V
        amt = amt * np.exp(-k * dt)
    def at(day):
        return conc[int(round(day / dt))]
    err = lambda: np.exp(rng.normal(0, 0.12, N))
    m = {'day14': at(14) * err(), 'trough wk4': at(27.5) * err(), 'trough wk8': at(55.5) * err(),
         'wk12': at(84) * err(), 'cavg 0-84': conc.mean(axis=0)}
    A = act
    covs = np.column_stack([(alb - 38.5), (mayo - 9), biol.astype(float), np.log(crp / 8)])
    res = {}
    for name, x in m.items():
        for cov in (False, True):
            X = np.column_stack([np.ones(A.sum()), np.log(x[A])] + ([covs[A]] if cov else []))
            y = rem[A].astype(float)
            nll = lambda b: np.sum(np.logaddexp(0, X @ b)) - y @ (X @ b)
            b = minimize(nll, np.zeros(X.shape[1]), method='BFGS').x
            preds = {}
            for d in (300, 600, 1200):
                X2 = X.copy(); X2[:, 1] = np.log(x[A] * d / 600.0)
                preds[d] = (1 / (1 + np.exp(-(X2 @ b)))).mean() * 100
            call = next(d for d in (300, 600, 1200) if preds[1200] - preds[d] <= 3.0)
            res[(name, cov)] = (b[1], preds, call)
    if verbose:
        r = rem[A]
        print('seed %d  remission active %.1f placebo %.1f' % (seed, rem[A].mean() * 100, rem[~A].mean() * 100))
        for name, x in m.items():
            ratio = np.exp(np.log(x[A][r]).mean() - np.log(x[A][~r]).mean())
            line = []
            for cov in (False, True):
                s, pr, call = res[(name, cov)]
                line.append('cov=%d slope %.2f 300:%.1f 600:%.1f 1200:%.1f call %d' % (cov, s, pr[300], pr[600], pr[1200], call))
            print('%-11s ratio %.2f | %s' % (name, ratio, ' | '.join(line)))
    return res

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'sweep':
        from collections import Counter
        tally = {}
        for s in range(1, 41):
            res = run(s, verbose=False)
            for k, v in res.items():
                tally.setdefault(k, Counter())[v[2]] += 1
        for k, c in tally.items():
            print(k, dict(c))
    else:
        run(int(sys.argv[1]) if len(sys.argv) > 1 else 141)
