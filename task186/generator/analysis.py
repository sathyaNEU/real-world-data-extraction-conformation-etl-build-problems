"""The golden and every rung, from the generator's clean truth: each station's daily time-weighted regular price
(06:00 to 22:00 local), its daily margin (net of the 5 per cent sales tax, the levy in force and the day's rack price),
its margin change across 1 January 2026, the null that holds the false discovery rate (the station's own 28-day
changes at dates whose windows hold no levy change), Benjamini-Hochberg at 5 per cent across every examined station,
each brand's share found and the inquiry; the two other admissible nulls and the default path's tests; the asks."""
import datetime as dt
import math

import numpy as np
from scipy import stats

import market as M
import world as W

N = M.N
CH = M.CH


# ---------------------------------------------------------------- daily prices and margins
def daily_prices(events, opened=None, closed=None):
    """time-weighted price (tenths of a cent) over 06:00 to 22:00 local on each day with a price in force all window;
    events: [(day index, local minute, price)] sorted"""
    out = np.full(N, np.nan)
    if not events:
        return out
    ev = sorted(events)
    j = 0
    cur = None
    first_k = ev[0][0]
    for k in range(first_k, N):
        if closed is not None and W.DAYS[k] >= closed:
            break
        todays = []
        while j < len(ev) and ev[j][0] == k:
            todays.append((ev[j][1], ev[j][2]))
            j += 1
        start_price = cur
        for minute, p in todays:
            if minute <= W.DAY_FROM:
                start_price = p
        if start_price is None:
            if todays:
                cur = todays[-1][1]
            continue
        total, t, p = 0.0, W.DAY_FROM, start_price
        for minute, q in todays:
            if minute <= W.DAY_FROM:
                continue
            m = min(minute, W.DAY_TO)
            total += p * (m - t)
            t = m
            p = q
            if minute >= W.DAY_TO:
                break
        total += p * (W.DAY_TO - t)
        out[k] = total / (W.DAY_TO - W.DAY_FROM)
        if todays:
            cur = todays[-1][1]
    return out


def rack_cents(rack):
    """the day's rack price for regular in cents a litre: the latest published on or before the day"""
    return np.array([M.latest(rack["RUL"], d) * 100.0 for d in W.DAYS])


LEVY = np.array([W.levy_regular(d) for d in W.DAYS])


def margins(price_tenths, rack_c):
    return price_tenths / 10.0 / (1 + W.SALES_TAX) - LEVY - rack_c


def window_change(m, k, w=W.WINDOW, need=W.MIN_DAYS):
    a, b = m[k:k + w], m[k - w:k]
    if np.sum(~np.isnan(a)) < need or np.sum(~np.isnan(b)) < need:
        return np.nan
    return float(np.nanmean(a) - np.nanmean(b))


# ---------------------------------------------------------------- the false discovery rate
def bh(p, q=W.FDR):
    p = np.asarray(p, float)
    m = len(p)
    o = np.argsort(p, kind="mergesort")
    ok = p[o] <= q * np.arange(1, m + 1) / m
    k = int(np.max(np.where(ok)[0]) + 1) if ok.any() else 0
    f = np.zeros(m, bool)
    f[o[:k]] = True
    return f


def by(p, q=W.FDR):
    m = len(p)
    return bh(p, q / np.sum(1.0 / np.arange(1, m + 1)))


def storey(p, q=W.FDR, lam=0.5):
    p = np.asarray(p, float)
    pi0 = min(1.0, float(np.mean(p > lam)) / (1 - lam))
    return bh(p, q / max(pi0, 1e-9))


# ---------------------------------------------------------------- the world as built
def state(sim=None):
    sim = sim or M.simulate()
    rk = rack_cents(sim["rack"])
    st = {s.uid: s for s in sim["stations"]}
    dp, mg = {}, {}
    for s in sim["stations"]:
        dp[s.uid] = daily_prices(sim["events"][s.uid], closed=s.closed)
        mg[s.uid] = margins(dp[s.uid], rk)
    sim.update(rack_c=rk, by_uid=st, daily=dp, margin=mg)
    return sim


def examined(sim, brand_of=None):
    """stations carrying a monitored brand on 1 January 2026 with a price on 20 or more days of each window"""
    out = []
    for s in sim["stations"]:
        b = (brand_of or (lambda s: s.brand_on(W.CHANGE)))(s)
        if b not in W.CODES:
            continue
        d = window_change(sim["margin"][s.uid], CH)
        if not np.isnan(d):
            out.append((s.uid, b, d))
    return out


def placebo_p(sim, ex):
    pl = M.placebo_indices()
    p = []
    for uid, b, d in ex:
        m = sim["margin"][uid]
        ref = np.array([window_change(m, k) for k in pl])
        ref = ref[~np.isnan(ref)]
        p.append((1 + np.sum(ref >= d)) / (len(ref) + 1))
    return np.array(p)


def empirical_p(ex):
    d = np.array([x[2] for x in ex])
    med = np.median(d)
    s0 = (np.percentile(d, 75) - np.percentile(d, 25)) / 1.349
    return 1 - stats.norm.cdf((d - med) / s0)


def within_area_p(sim, ex):
    d = {uid: dd for uid, b, dd in ex}
    rel = []
    for uid, b, dd in ex:
        a = sim["by_uid"][uid].area
        others = [d[u] for u, bb, _ in ex if bb != b and sim["by_uid"][u].area == a and u != uid]
        rel.append(dd - float(np.mean(others)))
    rel = np.array(rel)
    s1 = 1.4826 * np.median(np.abs(rel - np.median(rel)))
    return 1 - stats.norm.cdf((rel - np.median(rel)) / s1)


def welch_p(sim, ex):
    p = []
    for uid, b, d in ex:
        m = sim["margin"][uid]
        a, z = m[CH:CH + W.WINDOW], m[CH - W.WINDOW:CH]
        p.append(stats.ttest_ind(a[~np.isnan(a)], z[~np.isnan(z)], equal_var=False, alternative="greater")[1])
    return np.array(p)


def mannwhitney_p(sim, ex):
    p = []
    for uid, b, d in ex:
        m = sim["margin"][uid]
        a, z = m[CH:CH + W.WINDOW], m[CH - W.WINDOW:CH]
        p.append(stats.mannwhitneyu(a[~np.isnan(a)], z[~np.isnan(z)], alternative="greater")[1])
    return np.array(p)


def neweywest_p(sim, ex, lags):
    p = []
    for uid, b, d in ex:
        m = sim["margin"][uid][CH - W.WINDOW:CH + W.WINDOW]
        x = np.r_[np.zeros(W.WINDOW), np.ones(W.WINDOW)]
        keep = ~np.isnan(m)
        y, x = m[keep], x[keep]
        X = np.c_[np.ones(len(y)), x]
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ beta
        g = X * e[:, None]
        S = g.T @ g
        for L in range(1, lags + 1):
            w = 1 - L / (lags + 1)
            G = g[L:].T @ g[:-L]
            S += w * (G + G.T)
        Xi = np.linalg.inv(X.T @ X)
        V = Xi @ S @ Xi
        p.append(1 - stats.norm.cdf(beta[1] / math.sqrt(V[1, 1])))
    return np.array(p)


def province_relative_p(sim, ex):
    """each station's daily margin less the mean margin of every examined station that day, tested like the default"""
    lo, hi = CH - W.WINDOW, CH + W.WINDOW
    mat = np.array([sim["margin"][uid][lo:hi] for uid, b, d in ex])
    common = np.nanmean(mat, axis=0)
    p = []
    for row in mat:
        r = row - common
        a, z = r[W.WINDOW:], r[:W.WINDOW]
        p.append(stats.ttest_ind(a[~np.isnan(a)], z[~np.isnan(z)], equal_var=False, alternative="greater")[1])
    return np.array(p)


def shares(ex, found):
    out = {}
    for b in W.CODES:
        idx = [i for i, x in enumerate(ex) if x[1] == b]
        out[b] = (int(np.sum(found[idx])), len(idx))
    return out


def inquiry(sh):
    best = max(W.CODES, key=lambda b: sh[b][0] / sh[b][1])
    top = sh[best][0] / sh[best][1]
    tied = [b for b in W.CODES if sh[b][0] / sh[b][1] == top]
    if top < W.INQUIRY_SHARE or len(tied) > 1:
        return None
    return best


def tens(x):
    return int(math.floor(x * 10 + 0.5)) * 10


def golden(sim):
    """the golden: each examined station's change against its own changes at dates whose windows hold no levy change,
    Benjamini-Hochberg at 5 per cent, each brand's share found and the inquiry"""
    ex = examined(sim)
    p = placebo_p(sim, ex)
    found = bh(p)
    sh = shares(ex, found)
    towns = {sim["by_uid"][uid].area for (uid, b, d), f in zip(ex, found) if f}
    return {"ex": ex, "p": p, "found": found, "shares": sh, "call": inquiry(sh),
            "reissued": sum(1 for s in sim["stations"] if getattr(s, "reissued_to", None)),
            "found_towns": [a for a in W.AREA_CODES if a in towns]}


def main_call(sim):
    out = golden(sim)
    ex, p = out["ex"], out["p"]
    nulls = {"placebo": p, "empirical": empirical_p(ex), "within_area": within_area_p(sim, ex)}
    out["valid"] = {k: shares(ex, bh(v)) for k, v in nulls.items()}
    out["valid_procs"] = {"by": shares(ex, by(p)), "storey": shares(ex, storey(p))}
    naive = {"welch": welch_p(sim, ex), "mann_whitney": mannwhitney_p(sim, ex)}
    for L in (3, 7, 14):
        naive["newey_west_%d" % L] = neweywest_p(sim, ex, L)
    naive["province_relative"] = province_relative_p(sim, ex)
    out["naive"] = {k: shares(ex, bh(v)) for k, v in naive.items()}
    out["mean_change"] = {b: float(np.mean([x[2] for x in ex if x[1] == b])) for b in W.CODES}
    return out
