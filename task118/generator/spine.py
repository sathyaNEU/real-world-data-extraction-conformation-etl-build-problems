"""Articles and the click-source spine (pageviews by article, source surface and age band)."""
import datetime as dt
import numpy as np

import params as P
from archive import rng_for

T0 = dt.datetime(2025, 1, 1)          # minute offsets are AEST wall-clock minutes from this instant
DAY = 1440

KIND = {"POL-N": "news", "BUS-N": "news", "POL-M": "news", "LOC-M": "news", "SPT-N": "sport",
        "SPT-M": "sport", "CUL-N": "culture", "GAM-A": "app", "PZL-A": "app", "RCP-A": "app", "WEL-A": "app"}
WEEKDAY_W = {"news": [1.0, 1.0, 1.0, 1.0, 0.97, 0.56, 0.5], "sport": [0.86, 0.8, 0.82, 0.9, 1.0, 1.16, 1.1],
             "culture": [0.9, 0.92, 0.95, 1.0, 1.06, 0.8, 0.86], "app": [1.0] * 7}
HOUR_W = {
    "news": [.2, .1, .1, .1, .2, .6, 1.2, 1.6, 1.7, 1.6, 1.4, 1.3, 1.3, 1.2, 1.2, 1.2, 1.2, 1.1, 1.0, .9, .8, .7, .5, .3],
    "sport": [.2, .1, .1, .1, .2, .5, .9, 1.1, 1.2, 1.1, 1.0, 1.0, 1.1, 1.1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.5, 1.6, 1.5, 1.0, .5],
    "culture": [.1, .1, .1, .1, .2, .4, .8, 1.2, 1.4, 1.5, 1.4, 1.3, 1.3, 1.3, 1.3, 1.2, 1.1, 1.0, 1.0, .9, .8, .6, .4, .2],
    "app": [3.0, 1.2, .3, .3, .6, 1.0, 1.0, .8, .6, .5, .5, .5, .5, .5, .5, .5, .6, .7, .8, .8, .7, .6, .5, .4],
}
SEASON = {"sport": [1.0, 1.02, 1.08, 1.04, 0.95, 0.9, 1.0, 1.08, 1.06, 1.07, 1.05, 1.1],
          "news": [1.0, 1.0, 0.85, 0.9, 1.02, 1.0, 1.0, 1.06, 1.04, 1.0, 1.02, 1.0],
          "culture": [1.0, 1.04, 1.06, 0.95, 1.0, 1.03, 1.0, 0.98, 0.97, 1.0, 1.02, 0.98],
          "app": [1.0] * 12}


def minutes(d):
    return int((dt.datetime(d.year, d.month, d.day) - T0).total_seconds() // 60)


def to_dt(m):
    return T0 + dt.timedelta(minutes=int(m))


def month_index(date):
    return (date.year - 2025) * 12 + date.month - 10


def window_days():
    out, d = [], P.WINDOW_START
    while d <= P.WINDOW_END:
        out.append(d)
        d += dt.timedelta(days=1)
    return out


def largest_remainder(x, total):
    """Integer vector proportional to x summing exactly to total."""
    x = np.asarray(x, float)
    e = x / x.sum() * total
    f = np.floor(e).astype(np.int64)
    r = int(total - f.sum())
    if r > 0:
        idx = np.argsort(-(e - f), kind="stable")[:r]
        f[idx] += 1
    return f


def ipf_rows(S, w, groups, targets, iters=60):
    """Rescale per-row shares S (rows sum to 1) so that each group's w-weighted class shares hit targets."""
    S = S.copy()
    for _ in range(iters):
        for g, tgt in targets.items():
            m = groups == g
            if not m.any():
                continue
            cur = (w[m, None] * S[m]).sum(0) / w[m].sum()
            fac = np.where(cur > 0, np.asarray(tgt) / np.maximum(cur, 1e-15), 0.0)
            S[m] = S[m] * fac
            S[m] = S[m] / S[m].sum(1, keepdims=True)
    return S


class DeskArticles:
    pass


def build_articles(desk):
    """Publication times, size weights and tested flags for one desk's base-year articles."""
    k = list(P.DESK).index(desk)
    rng = rng_for(200 + k)
    kind = KIND[desk]
    days = window_days()
    dw = np.array([WEEKDAY_W[kind][d.weekday()] * SEASON[kind][month_index(d)] for d in days])
    if desk in P.APP:
        dw = np.ones(len(days))
    n = P.N_ARTICLES[desk]
    di = rng.choice(len(days), size=n, p=dw / dw.sum())
    hw = np.array(HOUR_W[kind])
    hh = rng.choice(24, size=n, p=hw / hw.sum())
    mm = rng.integers(0, 60, size=n)
    pub = np.array([minutes(days[i]) for i in di]) + hh * 60 + mm
    pub = np.sort(pub)
    A = DeskArticles()
    A.desk = desk
    A.pub = pub
    A.date = [(T0 + dt.timedelta(minutes=int(m))).date() for m in pub]
    A.month = np.array([month_index(d) for d in A.date])
    A.w = rng.lognormal(0.0, 1.05 if desk not in P.APP else 0.7, size=n)
    A.tested = np.zeros(n, bool)
    if desk in P.WEB:
        n_tests = P.WEB_TESTS[desk]["n"]
        elig = np.array([(d > P.WINDOW_START) and (d < P.WINDOW_END) for d in A.date])
    elif desk == P.OPEN_EMBEDDING["desk"]:
        n_tests = P.OPEN_EMBEDDING["n"]
        elig = np.array([(dt.date(2026, 1, 5) <= d <= dt.date(2026, 9, 25)) for d in A.date])
    else:
        n_tests = 0
        elig = np.zeros(n, bool)
    if n_tests:
        counts = np.array([np.sum(elig & (A.month == m)) for m in range(12)], float)
        per_month = largest_remainder(np.maximum(counts, 1e-9), n_tests)
        score = A.w * rng.lognormal(0.0, 0.6, size=n)
        for m in range(12):
            idx = np.where(elig & (A.month == m))[0]
            if per_month[m] == 0:
                continue
            top = idx[np.argsort(-score[idx], kind="stable")[:per_month[m]]]
            A.tested[top] = True
    # old articles (published before the window) that still drew pageviews in it
    n_old = int(round(P.OLD_ARTICLE_SHARE[desk] * n))
    A.n_old = n_old
    if n_old:
        back = rng.integers(1, 730, size=n_old)
        back = np.sort(back)[::-1]
        oh = rng.choice(24, size=n_old, p=hw / hw.sum())
        A.old_pub = np.array([minutes(P.WINDOW_START - dt.timedelta(days=int(b))) for b in back]) + oh * 60 + rng.integers(0, 60, n_old)
        A.old_w = rng.lognormal(0.0, 1.0, size=n_old)
    else:
        A.old_pub = np.zeros(0, np.int64)
        A.old_w = np.zeros(0)
    return A


def scale_tested(A, rng):
    """Scale tested articles so they carry the desk's target share of in-window clicks, month by month."""
    desk = A.desk
    if desk == P.OPEN_EMBEDDING["desk"]:
        A.w[A.tested] *= 4.0          # the squad tests the day's lead puzzle
        return
    if desk not in P.WEB:
        return
    A.w[A.tested] = A.w[A.tested] ** 0.5
    s_old = P.OLD_CLICK_SHARE[desk]
    a_in = P.A_TESTED[desk] / (1 - s_old)
    for m in range(12):
        sel = A.month == m
        T = sel & A.tested
        U = sel & ~A.tested
        if not T.any():
            continue
        am = a_in * (1 + rng.uniform(-0.03, 0.03))
        g = am * A.w[U].sum() / ((1 - am) * A.w[T].sum())
        A.w[T] *= g
    g = a_in * A.w[~A.tested].sum() / ((1 - a_in) * A.w[A.tested].sum())
    A.w[A.tested] *= g


def class_targets(desk):
    """Platform / partner / other shares for the tested group, the untested in-window group and old articles."""
    old_mix = np.array([0.05, 0.10 if P.Q_PART.get(desk, 0) > 0 else 0.0, 0.0])
    old_mix[2] = 1 - old_mix[0] - old_mix[1]
    if desk in P.APP:
        return {"T": np.array([1.0, 0, 0]), "U": np.array([1.0, 0, 0])}, np.array([1.0, 0, 0])
    f, q, t, a, qt = P.F_PLAT[desk], P.Q_PART[desk], P.T_TESTED[desk], P.A_TESTED[desk], P.QT_TESTED[desk]
    s = P.OLD_CLICK_SHARE[desk]
    ft = t * f / a
    ot = 1 - ft - qt
    rest = 1 - a - s
    fu = (f - a * ft - s * old_mix[0]) / rest
    qu = (q - a * qt - s * old_mix[1]) / rest
    ou = 1 - fu - qu
    tg = {"T": np.array([ft, qt, ot]), "U": np.array([fu, qu, ou])}
    for v in tg.values():
        assert (v >= 0).all() and abs(v.sum() - 1) < 1e-9, (desk, tg)
    return tg, old_mix


def dirichlet_rows(rng, alpha):
    """One Dirichlet draw per row of an alpha matrix (zero alpha stays zero)."""
    g = rng.gamma(np.maximum(alpha, 1e-9)) * (alpha > 0)
    s = g.sum(1, keepdims=True)
    return np.where(s > 0, g / np.where(s > 0, s, 1), 0.0)


def build_mixes(A, rng):
    """Per-article source weights (11 codes) and age profiles (6 bands) for in-window and old articles."""
    desk = A.desk
    n = len(A.pub)
    tg, old_mix = class_targets(desk)
    groups = np.where(A.tested, "T", "U")
    base = np.vstack([tg[g] for g in groups])
    S = dirichlet_rows(rng, 30 * base)
    S = ipf_rows(S, A.w, groups, tg)
    inst = P.DESK[desk][5] or "app"
    plat = dirichlet_rows(rng, np.tile(40 * np.array(P.PLAT_SPLIT[inst]), (n, 1)))
    if desk in P.APP:
        other = np.zeros((n, 5))
    else:
        other = dirichlet_rows(rng, np.tile(25 * np.array(P.OTHER_SPLIT[desk]), (n, 1)))
        rank = np.argsort(np.argsort(-A.w)) / n
        has_nl = rng.random(n) < 0.32 + 0.4 * (rank < 0.2)
        has_al = rng.random(n) < np.where(rank < 0.05, 0.6, 0.03)
        other[~has_nl, 3] = 0
        other[~has_al, 4] = 0
        other = other / other.sum(1, keepdims=True)
    W = np.zeros((n, len(P.SOURCES)))
    W[:, 0:5] = S[:, [0]] * plat
    W[:, 5] = S[:, 2] * other[:, 0]          # search
    W[:, 6] = S[:, 2] * other[:, 1]          # discover
    W[:, 7] = S[:, 1]                        # partner_apps
    W[:, 8] = S[:, 2] * other[:, 2]          # social
    W[:, 9] = S[:, 2] * other[:, 3]          # newsletter
    W[:, 10] = S[:, 2] * other[:, 4]         # alerts
    A.src = W
    end_min = minutes(P.WINDOW_END) + DAY
    left_h = (end_min - A.pub) / 60.0
    open_band = (np.array(P.AGE_START_H)[None, :] < left_h[:, None])
    G = np.zeros((n, len(P.SOURCES), 6))
    for j, s in enumerate(P.SOURCES):
        if W[:, j].max() == 0:
            continue
        if desk in P.APP:
            pr = np.where(A.tested[:, None], np.array(P.AGE_PROFILE["app_tested"])[None, :],
                          np.array(P.AGE_PROFILE["app"])[None, :])
        elif j < 5:
            pr = np.where(A.tested[:, None], np.array(P.AGE_PROFILE["platform_tested"])[None, :],
                          np.array(P.AGE_PROFILE["platform"])[None, :])
        else:
            pr = np.tile(np.array(P.AGE_PROFILE[s]), (n, 1))
        g = dirichlet_rows(rng, 25 * pr) * open_band
        tot = g.sum(1, keepdims=True)
        G[:, j] = np.where(tot > 0, g / np.where(tot > 0, tot, 1), 0.0)
    A.age = G
    # old articles: mostly search, a little partner and related links, all at 3-7d or 7d+
    no = len(A.old_pub)
    if no:
        mean = np.zeros(len(P.SOURCES))
        if desk in P.APP:
            mean[2], mean[3], mean[4] = 0.25, 0.55, 0.20
        else:
            mean[4] = old_mix[0] * 0.8      # related_links
            mean[1] = old_mix[0] * 0.2      # section_web
        mean[7] = old_mix[1]
        mean[5] = old_mix[2] * 0.72
        mean[6] = old_mix[2] * 0.08
        mean[8] = old_mix[2] * 0.20
        OW = dirichlet_rows(rng, np.tile(60 * mean, (no, 1)))
        start_min = minutes(P.WINDOW_START)
        age_days = (start_min - A.old_pub) / DAY
        g = np.where((age_days < 7)[:, None], np.array([0, 0, 0, 0, 0.6, 0.4])[None, :],
                     np.array([0, 0, 0, 0, 0, 1.0])[None, :])
        A.old_src, A.old_age = OW, np.repeat(g[:, None, :], len(P.SOURCES), axis=1)
    else:
        A.old_src = np.zeros((0, len(P.SOURCES)))
        A.old_age = np.zeros((0, len(P.SOURCES), 6))


def expected_fractions(A):
    """Share of the desk's total pageviews in each (article, source, age) cell, before scaling."""
    desk = A.desk
    s_old = P.OLD_CLICK_SHARE[desk]
    win = (A.w / A.w.sum())[:, None, None] * A.src[:, :, None] * A.age * (1 - s_old)
    if len(A.old_pub):
        old = (A.old_w / A.old_w.sum())[:, None, None] * A.old_src[:, :, None] * A.old_age * s_old
    else:
        old = np.zeros((0, len(P.SOURCES), 6))
    return win, old


def allocate(A, total):
    win, old = expected_fractions(A)
    flat = np.concatenate([win.ravel(), old.ravel()])
    vals = largest_remainder(flat, total)
    A.pv = vals[:win.size].reshape(win.shape)
    A.old_pv = vals[win.size:].reshape(old.shape)
    A.total = int(total)
