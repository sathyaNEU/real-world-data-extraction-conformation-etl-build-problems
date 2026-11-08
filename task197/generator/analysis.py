"""Every route to the decision, computed on what the pack carries: monthly accidental under-six exposure counts
per watched product (from the enquiry export) and four-weekly scan sales (spread evenly over each period's days).

Used by build.py to write the figures and by checks.py; verify.py has its own code path.
"""
import datetime as dt
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import gamma as gamma_dist
from scipy.signal import lfilter

MONTH_DAYS = 30.4375


def mkey(d):
    return d.year * 12 + d.month - 1


class Series:
    """Daily purchases rebuilt from four-weekly periods, and monthly exposure counts."""

    def __init__(self, day0, ndays, periods, expo_by_month):
        # periods: list of (start_date, end_date, units) for one product, units summed over its SKUs and channels
        self.day0 = day0
        self.ndays = ndays
        self.days = [day0 + dt.timedelta(days=i) for i in range(ndays)]
        self.mk = np.array([mkey(d) for d in self.days])
        buys = np.zeros(ndays)
        for a, b, u in periods:
            ia, ib = (a - day0).days, (b - day0).days
            n = ib - ia + 1
            buys[ia:ib + 1] += u / n
        self.buys = buys
        self.expo = dict(expo_by_month)       # month key -> count
        self.month_keys = sorted(set(self.mk))

    def monthly_sum(self, daily):
        base = self.mk.min()
        sums = np.bincount(self.mk - base, weights=daily)
        return {base + i: float(v) for i, v in enumerate(sums)}

    def stock(self, L, kind="exp", shape=2.0):
        """Packs in homes, as a sum over each day's purchases surviving to the day."""
        n = self.ndays
        a = np.arange(n, dtype=float) / MONTH_DAYS          # age in months
        if kind == "exp":
            q = np.exp(-1.0 / (L * MONTH_DAYS))
            return lfilter([1.0], [1.0, -q], self.buys)
        if kind == "gamma":
            k = gamma_dist.sf(a, shape, scale=L / shape)
        elif kind == "box":
            k = (a < L).astype(float)
        else:
            raise ValueError(kind)
        return np.convolve(self.buys, k)[:n]

    def monthly_stock(self, L, kind="exp", shape=2.0):
        return self.monthly_sum(self.stock(L, kind, shape))

    def monthly_sales(self):
        return self.monthly_sum(self.buys)


def fit_hazard(series, months, L, kind="exp", shape=2.0, grain="month"):
    """Poisson maximum likelihood of exposures = h x monthly stock over the given months; returns (h, nll)."""
    st = series.monthly_stock(L, kind, shape)
    y = np.array([series.expo.get(k, 0) for k in months], dtype=float)
    x = np.array([st[k] for k in months])
    if grain == "quarter":
        n = len(months) // 3 * 3
        y = y[-n:].reshape(-1, 3).sum(1)
        x = x[-n:].reshape(-1, 3).sum(1)
    h = y.sum() / x.sum()
    mu = h * x
    nll = float(np.sum(mu - y * np.log(mu)))
    return h, nll


def fit_drain(series, months, kind="exp", shape=2.0, grain="month", lo=0.6, hi=120.0):
    """Maximum likelihood drain: a log-spaced grid first (the profile can carry a second, shallower basin at long
    drains), then a bounded refinement between the grid neighbours of the best point."""
    grid = np.exp(np.linspace(np.log(lo), np.log(hi), 61))
    vals = [fit_hazard(series, months, L, kind, shape, grain)[1] for L in grid]
    i = int(np.argmin(vals))
    a, b = grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)]
    r = minimize_scalar(lambda L: fit_hazard(series, months, L, kind, shape, grain)[1], bounds=(a, b),
                        method="bounded", options={"xatol": 1e-4})
    L = float(r.x)
    h, nll = fit_hazard(series, months, L, kind, shape, grain)
    return L, h, nll


def profile_interval(series, months, L_hat, nll_hat, kind="exp"):
    """The drain values within 1.92 of the best negative log-likelihood (a 95 per cent profile interval)."""
    grid = np.unique(np.concatenate([np.linspace(max(0.6, L_hat * 0.4), L_hat * 2.5, 241), [L_hat]]))
    ok = [L for L in grid if fit_hazard(series, months, L, kind)[1] - nll_hat <= 1.92]
    return min(ok), max(ok)


def effect_stock(series, pre_months, post_months, L, h, kind="exp", shape=2.0):
    st = series.monthly_stock(L, kind, shape)
    cf = h * sum(st[k] for k in post_months)
    obs = sum(series.expo.get(k, 0) for k in post_months)
    return obs, cf, obs / cf


def effect_per_sold(series, post_months, pre12):
    sa = series.monthly_sales()
    obs = sum(series.expo.get(k, 0) for k in post_months)
    pre = sum(series.expo.get(k, 0) for k in pre12)
    return (obs / sum(sa[k] for k in post_months)) / (pre / sum(sa[k] for k in pre12))


def effect_raw(series, post_months, pre12):
    obs = sum(series.expo.get(k, 0) for k in post_months)
    pre = sum(series.expo.get(k, 0) for k in pre12)
    return obs / pre


def effect_trailing(series, post_months, pre12, n=12):
    sa = series.monthly_sales()
    keys = sorted(sa)

    def trail(k):
        return sum(sa.get(j, 0.0) for j in range(k - n + 1, k + 1))

    obs = sum(series.expo.get(k, 0) for k in post_months)
    pre = sum(series.expo.get(k, 0) for k in pre12)
    return (obs / sum(trail(k) for k in post_months)) / (pre / sum(trail(k) for k in pre12))


def effect_its(series, pre_months, post_months):
    """Interrupted time series: Poisson regression of monthly exposures on log sales and a linear trend over
    the months before the change, projected over the window."""
    sa = series.monthly_sales()
    t0 = pre_months[0]

    def X(ks):
        return np.array([[1.0, np.log(sa[k]), (k - t0) / 12.0] for k in ks])

    Xp, y = X(pre_months), np.array([series.expo.get(k, 0) for k in pre_months], dtype=float)
    beta = np.array([np.log(max(y.mean(), 0.5)), 0.0, 0.0])
    for _ in range(100):           # iteratively reweighted least squares
        mu = np.exp(Xp @ beta)
        W = mu
        z = Xp @ beta + (y - mu) / mu
        A = Xp.T @ (W[:, None] * Xp)
        b = Xp.T @ (W * z)
        nb = np.linalg.solve(A, b)
        if np.max(np.abs(nb - beta)) < 1e-10:
            beta = nb
            break
        beta = nb
    cf = float(np.exp(X(post_months) @ beta).sum())
    obs = sum(series.expo.get(k, 0) for k in post_months)
    return obs / cf


def backtest(series, fit_months, test_months, L=None):
    """Fit on the earlier span, predict the later span; Poisson deviance of each route's monthly prediction."""
    y = np.array([series.expo.get(k, 0) for k in test_months], dtype=float)

    def dev(mu):
        mu = np.asarray(mu, dtype=float)
        with np.errstate(divide="ignore", invalid="ignore"):
            t = np.where(y > 0, y * np.log(y / mu), 0.0)
        return float(2 * np.sum(t - (y - mu)))

    Lf, hf, _ = fit_drain(series, fit_months)
    st = series.monthly_stock(Lf)
    stock_pred = [hf * st[k] for k in test_months]
    sa = series.monthly_sales()
    rate = sum(series.expo.get(k, 0) for k in fit_months) / sum(sa[k] for k in fit_months)
    sold_pred = [rate * sa[k] for k in test_months]
    # time series on log sales and trend, fitted on the earlier span
    t0 = fit_months[0]

    def X(ks):
        return np.array([[1.0, np.log(sa[k]), (k - t0) / 12.0] for k in ks])
    Xf, yf = X(fit_months), np.array([series.expo.get(k, 0) for k in fit_months], dtype=float)
    beta = np.array([np.log(max(yf.mean(), 0.5)), 0.0, 0.0])
    for _ in range(100):
        mu = np.exp(Xf @ beta)
        z = Xf @ beta + (yf - mu) / mu
        nb = np.linalg.solve(Xf.T @ (mu[:, None] * Xf), Xf.T @ (mu * z))
        if np.max(np.abs(nb - beta)) < 1e-10:
            beta = nb
            break
        beta = nb
    its_pred = list(np.exp(X(test_months) @ beta))
    return dict(L=Lf, stock=dev(stock_pred), sold=dev(sold_pred), its=dev(its_pred), n=len(test_months),
                stock_pred=stock_pred, sold_pred=sold_pred, its_pred=its_pred, y=list(y))


def _glm(X, y, offset=None):
    off = np.zeros(len(y)) if offset is None else offset
    beta = np.zeros(X.shape[1])
    beta[0] = np.log(max(y.mean(), 0.5)) - off.mean()
    for _ in range(300):
        eta = np.clip(X @ beta + off, -50, 50)
        mu = np.exp(eta)
        z = eta - off + (y - mu) / mu
        nb = np.linalg.solve(X.T @ (mu[:, None] * X) + 1e-9 * np.eye(X.shape[1]), X.T @ (mu * z))
        if np.max(np.abs(nb - beta)) < 1e-10:
            return nb
        beta = nb
    return beta


def cheap_routes(series, pre_all, post):
    """Every flow-based route a capable analyst could take without building the packs in use, each giving the
    product's effect: a rate per pack sold over several base windows; Poisson regressions over all the months before
    the change or the last 36 or 24 of them, with sales as an offset or a covariate, a trend and month of year; raw
    counts against the year before; and a rate per trailing-sales total. A sales covariate beside month of year is
    run on the full record only (on a short window seasonal scan sales and the month terms are collinear)."""
    ck = pre_all[-1] + 1
    sa = series.monthly_sales()
    y = lambda ks: np.array([series.expo.get(k, 0) for k in ks], dtype=float)
    obs = y(post).sum()
    out = {}
    for n in (6, 12, 24, 36, 48):
        out["sold_last%d" % n] = effect_per_sold(series, post, list(range(ck - n, ck)))
    out["sold_all"] = effect_per_sold(series, post, pre_all)
    for nm, base in (("all", pre_all), ("last36", list(range(ck - 36, ck))), ("last24", list(range(ck - 24, ck)))):
        t0 = base[0]

        def Xf(ks, kind):
            cols = [np.ones(len(ks))]
            if "trend" in kind:
                cols.append(np.array([(k - t0) / 12.0 for k in ks]))
            if "season" in kind:
                for m in range(1, 12):
                    cols.append(np.array([1.0 if k % 12 == m else 0.0 for k in ks]))
            if "logs" in kind:
                cols.append(np.log([sa[k] for k in ks]))
            return np.column_stack(cols)

        kinds = ["off", "off+trend", "off+season", "off+trend+season", "logs", "logs+trend", "trend", "trend+season"]
        if nm == "all":
            kinds += ["logs+season", "logs+trend+season"]
        for kind in kinds:
            off = np.log([sa[k] for k in base]) if kind.startswith("off") else None
            b = _glm(Xf(base, kind), y(base), off)
            offp = np.log([sa[k] for k in post]) if kind.startswith("off") else 0.0
            out["glm_%s_%s" % (kind, nm)] = obs / float(np.exp(np.clip(Xf(post, kind) @ b + offp, -50, 50)).sum())
    out["raw_last12"] = effect_raw(series, post, list(range(ck - 12, ck)))
    out["raw_same_months"] = effect_raw(series, post, list(range(ck - 11, ck + 1)))
    for n in (3, 6, 12, 18, 24, 36):
        out["trailing%d" % n] = effect_trailing(series, post, list(range(ck - 12, ck)), n=n)
    return out
