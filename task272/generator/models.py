"""Estimators of a hospital's drop after an approval, in percentage points (the chance of approving right after a
denial less the chance right after an approval), over a list of counsellor-days, each (counsellor, day, y) with y the
day's determinations in the order recorded, 1 an approval and 0 a denial.

The golden is `excess`: the within-day pooled contrast less its exact expectation when each day's determinations are
put in every order (each day's count of approvals held). The rest of the family estimates the same chance by other
routes the data's structure licenses (the held-day slope less its reordering expectation, Miller and Sanjurjo's per-day
excess, the Chamberlain conditional logit read as a marginal effect, a random intercept per counsellor-day by maximum
likelihood, the split-panel jackknife). The reflexes are the routes that skip a structure: consecutive determinations
pooled, the counsellor held, the day's rate over every determination as a control, each counsellor-day held, each day's
own drop averaged. The day's rate over the other determinations (one or both of the pair left out) is a family member:
the others' count carries what the day's applications say about the chance."""
from functools import lru_cache
from math import comb

import numpy as np


def _arr(days):
    return [(c, d, np.asarray(y, float)) for c, d, y in days]


def pairs_counts(days):
    """n11, n1, n01, n0 over within-day consecutive pairs, and their expectations under reordering of each day."""
    n11 = n1 = n01 = n0 = 0.0
    b11 = b1 = b01 = b0 = 0.0
    for _, _, y in days:
        n = len(y)
        if n < 2:
            continue
        k = y.sum()
        x, z = y[:-1], y[1:]
        n11 += (x * z).sum()
        n1 += x.sum()
        n01 += ((1 - x) * z).sum()
        n0 += (1 - x).sum()
        b11 += k * (k - 1) / n
        b1 += (n - 1) * k / n
        b01 += k * (n - k) / n
        b0 += (n - 1) * (n - k) / n
    return (n11, n1, n01, n0), (b11, b1, b01, b0)


def pooled(days):
    (n11, n1, n01, n0), _ = pairs_counts(days)
    return 100 * (n01 / n0 - n11 / n1)


def excess(days):
    """The golden: the pooled within-day contrast less its expectation under reordering within each day."""
    (n11, n1, n01, n0), (b11, b1, b01, b0) = pairs_counts(days)
    return 100 * ((n01 / n0 - n11 / n1) - (b01 / b0 - b11 / b1))


def benchmark(days):
    _, (b11, b1, b01, b0) = pairs_counts(days)
    return 100 * (b01 / b0 - b11 / b1)


def perm_fe(n, k):
    """E[S_xy], E[S_xx] of the held-day slope's sums for a day of n determinations with k approvals, every order equally
    likely (closed form; asserted against enumeration in checks)."""
    if n < 3 or k == 0 or k == n:
        return 0.0, 0.0
    m = n - 1
    e11 = k * (k - 1) / n
    exz = k * k - 2 * k * k / n + k * (k - 1) / (n * (n - 1))
    exx2 = k * k - 2 * k * k / n + k / n
    return e11 - exz / m, k * m / n - exx2 / m


def _fe_sums(days):
    sxy = sxx = 0.0
    for _, _, y in days:
        if len(y) < 3:
            continue
        x, z = y[:-1], y[1:]
        sxy += ((x - x.mean()) * (z - z.mean())).sum()
        sxx += ((x - x.mean()) ** 2).sum()
    return sxy, sxx


def day_fe(days):
    """Reflex: each counsellor-day held by its own fixed effect."""
    sxy, sxx = _fe_sums(days)
    return -100 * sxy / sxx


def excess_fe(days):
    sxy, sxx = _fe_sums(days)
    exy = exx = 0.0
    for _, _, y in days:
        a, b = perm_fe(len(y), int(y.sum()))
        exy += a
        exx += b
    return -100 * (sxy / sxx - exy / exx)


def per_day(days):
    """Reflex: each day's own drop, averaged over the days where both an approval and a denial precede a decision."""
    v = []
    for _, _, y in days:
        x, z = y[:-1], y[1:]
        if 0 < x.sum() < len(x):
            v.append(z[x == 0].mean() - z[x == 1].mean())
    return 100 * float(np.mean(v))


@lru_cache(maxsize=None)
def _perday_table(n):
    """For a day of n determinations, the mean per-day drop over every order of k approvals (k = 0..n), over the orders
    where it is defined: exact enumeration of all 2^n sequences up to n = 20, a seeded draw of 40,000 orders per k
    above."""
    out = np.zeros(n + 1)
    if n <= 20:
        s = ((np.arange(2 ** n)[:, None] >> np.arange(n)) & 1).astype(np.int8)
        k = s.sum(1)
        x, z = s[:, :-1], s[:, 1:]
        a1 = x.sum(1)
        a0 = (n - 1) - a1
        ok = (a1 > 0) & (a0 > 0)
        z1 = (x * z).sum(1)
        z0 = ((1 - x) * z).sum(1)
        v = np.where(ok, z0 / np.maximum(a0, 1) - z1 / np.maximum(a1, 1), 0.0)
        for kk in range(n + 1):
            m = ok & (k == kk)
            out[kk] = v[m].mean() if m.any() else 0.0
        return out
    r = np.random.default_rng(n * 1009)
    for kk in range(1, n):
        base = np.r_[np.ones(kk), np.zeros(n - kk)]
        ys = np.array([r.permutation(base) for _ in range(40000)])
        x, z = ys[:, :-1], ys[:, 1:]
        a1 = x.sum(1)
        a0 = (n - 1) - a1
        ok = (a1 > 0) & (a0 > 0)
        v = (((1 - x) * z).sum(1) / np.maximum(a0, 1) - (x * z).sum(1) / np.maximum(a1, 1))[ok]
        out[kk] = v.mean() if len(v) else 0.0
    return out


def _perday_null(n, k):
    return float(_perday_table(n)[k])


def per_day_excess(days):
    obs, exp = [], []
    for _, _, y in days:
        x, z = y[:-1], y[1:]
        if 0 < x.sum() < len(x):
            obs.append(z[x == 0].mean() - z[x == 1].mean())
            exp.append(_perday_null(len(y), int(y.sum())))
    return 100 * (float(np.mean(obs)) - float(np.mean(exp)))


def counsellor_fe(days):
    """Reflex: within-day pairs pooled within each counsellor over the year (the counsellor held, the day not)."""
    by = {}
    for c, _, y in days:
        if len(y) >= 2:
            by.setdefault(c, []).append((y[:-1], y[1:]))
    sxy = sxx = 0.0
    for lst in by.values():
        X = np.concatenate([a for a, _ in lst])
        Z = np.concatenate([b for _, b in lst])
        sxy += ((X - X.mean()) * (Z - Z.mean())).sum()
        sxx += ((X - X.mean()) ** 2).sum()
    return -100 * sxy / sxx


def _day_rate_control(days, mode):
    """Each determination on the one before, with counsellor fixed effects and the day's approval rate as a control:
    mode "all" over every determination of the day, "one" without the current one, "two" without the pair."""
    X, Y, R, G = [], [], [], []
    for c, _, y in days:
        n = len(y)
        if n < 4:
            continue
        k = y.sum()
        for t in range(1, n):
            X.append(y[t - 1])
            Y.append(y[t])
            R.append(k / n if mode == "all" else (k - y[t]) / (n - 1) if mode == "one"
                     else (k - y[t] - y[t - 1]) / (n - 2))
            G.append(c)
    X, Y, R = map(np.asarray, (X, Y, R))
    G = np.asarray([str(g) for g in G])
    cols = [np.ones(len(X)), X, R] + [(G == g).astype(float) for g in np.unique(G)[1:]]
    b = np.linalg.lstsq(np.column_stack(cols), Y, rcond=None)[0]
    return -100 * b[1]


def day_rate(days):
    """Reflex: the day's approval rate over every determination as the control."""
    return _day_rate_control(days, "all")


def leave_one_out(days):
    """The day's approval rate over the counsellor's other determinations that day as the control: the count of the
    others carries everything the day's applications say about the chance, so this conditions as the golden does."""
    return _day_rate_control(days, "one")


def leave_two_out(days):
    """The day's rate without the pair as the control (the pair's earlier member left out too)."""
    return _day_rate_control(days, "two")


def jackknife(days):
    """The split-panel jackknife on the held-day slope: twice the full slope less the mean of the two half-days'."""
    full, h1, h2 = [], [], []
    for c, d, y in days:
        full.append((c, d, y))
        m = len(y) // 2
        if m >= 3:
            h1.append((c, d, y[:m]))
            h2.append((c, d, y[m:]))
    s1 = _fe_sums(full)
    a = _fe_sums(h1)
    b = _fe_sums(h2)
    return -100 * (2 * s1[0] / s1[1] - 0.5 * (a[0] / a[1] + b[0] / b[1]))


@lru_cache(maxsize=None)
def _cl_table(n, k, a, b):
    out = {}
    for r1 in range(1, k + 1):
        if a == 1 and b == 1:
            r0 = r1 - 1
        elif a == 0 and b == 0:
            r0 = r1 + 1
        else:
            r0 = r1
        if r0 < 0 or (r0 == 0 and n - k > 0) or (r0 > 0 and n - k == 0):
            continue
        c1 = comb(k - 1, r1 - 1)
        c0 = comb(n - k - 1, r0 - 1) if r0 > 0 else 1
        if c1 * c0:
            out[k - r1] = out.get(k - r1, 0) + c1 * c0
    j = np.array(sorted(out), float)
    return j, np.log(np.array([out[x] for x in sorted(out)], float))


def cond_logit(days):
    """Chamberlain's conditional logit for a first-order chain with a day intercept (conditioning on each day's first
    and last determination and count), read as a marginal effect at each day's own approval rate."""
    stats = []
    for _, _, y in days:
        n, k = len(y), int(y.sum())
        if n < 4 or k in (0, n):
            continue
        j, lw = _cl_table(n, k, int(y[0]), int(y[-1]))
        if len(j) < 2:
            continue
        stats.append((float((y[:-1] * y[1:]).sum()), j, lw))
    g = 0.0
    for _ in range(80):
        sc = inf = 0.0
        for obs, j, lw in stats:
            l = lw + g * j
            l = l - l.max()
            p = np.exp(l)
            p /= p.sum()
            mj = (p * j).sum()
            sc += obs - mj
            inf += (p * j * j).sum() - mj * mj
        step = sc / inf
        g += step
        if abs(step) < 1e-12:
            break
    pb = np.array([y.mean() for _, _, y in days if len(y)])
    return -100 * g * float(np.mean(pb * (1 - pb)))


def random_day_ml(days):
    """A random intercept per counsellor-day and counsellor fixed effects, linear, maximum likelihood by profiling the
    variance ratio on a grid: what a mixed-model fit converges to."""
    X, Y, G, C = [], [], [], []
    cix = {c: i for i, c in enumerate(sorted({c for c, _, _ in days}))}
    for gi, (c, _, y) in enumerate(days):
        if len(y) < 2:
            continue
        X.append(y[:-1])
        Y.append(y[1:])
        G.append(np.full(len(y) - 1, gi))
        C.append(np.full(len(y) - 1, cix[c]))
    X, Y, G, C = map(np.concatenate, (X, Y, G, C))
    _, inv, cnt = np.unique(G, return_inverse=True, return_counts=True)
    gm = lambda v: (np.bincount(inv, v) / cnt)[inv]
    dums = [(C == cc).astype(float) for cc in np.unique(C)]
    N = len(Y)
    best = None
    for lam in np.r_[0, np.geomspace(1e-4, 50, 160)]:
        t = (1 - np.sqrt(1 / (1 + cnt * lam)))[inv]
        D = np.column_stack([X - t * gm(X)] + [u - t * gm(u) for u in dums])
        ys = Y - t * gm(Y)
        b = np.linalg.lstsq(D, ys, rcond=None)[0]
        rss = ((ys - D @ b) ** 2).sum()
        ll = -N / 2 * np.log(rss / N) - 0.5 * np.log(1 + cnt * lam).sum()
        if best is None or ll > best[0]:
            best = (ll, b[0])
    return -100 * best[1]


FAMILY = {"excess": excess, "excess_fe": excess_fe, "per_day_excess": per_day_excess, "cond_logit": cond_logit,
          "random_day_ml": random_day_ml, "jackknife": jackknife, "leave_one_out": leave_one_out,
          "leave_two_out": leave_two_out}
REFLEXES = {"pooled": pooled, "counsellor_fe": counsellor_fe, "day_rate": day_rate, "day_fe": day_fe,
            "per_day": per_day}


def family(days, members=None):
    days = _arr(days)
    return {k: f(days) for k, f in FAMILY.items() if members is None or k in members}


def reflexes(days):
    days = _arr(days)
    return {k: f(days) for k, f in REFLEXES.items()}
