"""Prototype: next-birthday selection accuracy estimated from respondents' days to next birthday.
Clean truth only. Measures (a) the precision of the birthday-mixture estimator per stream and
(b) the bias of a uniform-birthday null when a stream's selection dates sit in one season."""
import numpy as np
from scipy.optimize import minimize_scalar

rng = np.random.default_rng(250)
DAYS = 365

def birthday_density(amp, peak_day, spike_jan1=0.0):
    x = np.arange(DAYS)
    d = 1 + amp * np.cos(2 * np.pi * (x - peak_day) / DAYS)
    d = d / d.sum()
    if spike_jan1 > 0:
        d = d * (1 - spike_jan1)
        d[0] += spike_jan1
    return d

def sample_birthdays(dens, n):
    return rng.choice(DAYS, size=n, p=dens)

def sim_stream(n_multi, n_single, sel_day_window, s_true_c, dens, kprobs):
    ks = rng.choice([2, 3, 4, 5], size=n_multi, p=kprobs)
    t_multi = rng.integers(sel_day_window[0], sel_day_window[1] + 1, size=n_multi) % DAYS
    D_resp = np.empty(n_multi)
    is_min = np.empty(n_multi, bool)
    for i in range(n_multi):
        b = sample_birthdays(dens, ks[i])
        D = (b - t_multi[i] - 1) % DAYS + 1  # days 1..365 to next birthday after the date
        if rng.random() < s_true_c:
            j = np.argmin(D)
        else:
            j = rng.integers(ks[i])
        D_resp[i] = D[j]
        is_min[i] = D[j] == D.min()
    t_single = rng.integers(sel_day_window[0], sel_day_window[1] + 1, size=n_single) % DAYS
    b1 = sample_birthdays(dens, n_single)
    D_single = (b1 - t_single - 1) % DAYS + 1
    return dict(k=ks, t=t_multi, D=D_resp, is_min=is_min, D1=D_single, t1=t_single)

def null_cdf_for_date(dens, t):
    # distribution of D (1..365) for a random adult at selection date t
    order = (np.arange(1, DAYS + 1) + t) % DAYS  # birthday day for D=1..365
    f = dens[order]
    F = np.cumsum(f)
    return f, F

def mle_c(st, f_of, F_of):
    k = st['k']; D = st['D'].astype(int)
    f = f_of(st, D); F = F_of(st, D)
    Fm = F - f  # P(D' < d) for the strictly-earlier part; use (1-F_prev)^(k-1) approx with ties ignored
    surv = 1 - Fm
    comp = k * surv ** (k - 1)
    def nll(c):
        return -np.sum(np.log(c * comp + (1 - c)))
    r = minimize_scalar(nll, bounds=(0, 1), method='bounded')
    c = r.x
    s = c + (1 - c) * np.mean(1 / k)
    return c, s

def run(amp, windows, cs, n_multi=8000, n_single=4000, seed_note=''):
    dens = birthday_density(amp, peak_day=200)
    kprobs = [0.62, 0.24, 0.10, 0.04]
    print('amp', amp)
    for w, c in zip(windows, cs):
        st = sim_stream(n_multi, n_single, w, c, dens, kprobs)
        s_real = st['is_min'].mean()
        # uniform null
        uf = lambda st, D: np.full(D.shape, 1 / DAYS)
        uF = lambda st, D: D / DAYS
        _, s_u = mle_c(st, uf, uF)
        # empirical (true population density) null at each household's date
        def ef(st, D):
            t = st['t']
            return dens[(D + t) % DAYS]
        cumcache = {}
        def eF(st, D):
            t = st['t']
            out = np.empty(D.shape)
            for i in range(len(D)):
                tt = t[i]
                if tt not in cumcache:
                    cumcache[tt] = null_cdf_for_date(dens, tt)[1]
                out[i] = cumcache[tt][D[i] - 1]
            return out
        _, s_e = mle_c(st, ef, eF)
        mean_single = st['D1'].mean()
        print('  window %s c %.2f  s_real %.3f  uniform-null %.3f (bias %+.3f)  empirical %.3f (err %+.3f)  single-adult mean D %.1f'
              % (w, c, s_real, s_u, s_u - s_real, s_e, s_e - s_real, mean_single))

if __name__ == '__main__':
    windows = [(30, 44), (110, 124), (150, 164), (200, 214), (260, 274), (330, 344)]
    cs = [0.70] * 6
    for amp in (0.10, 0.15, 0.20):
        run(amp, windows, cs)
