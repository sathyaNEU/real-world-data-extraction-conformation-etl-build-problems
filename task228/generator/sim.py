"""The 2026 experiments: per-install telemetry for both arms of every experiment, each experiment's truth (incident kind,
engagement effect) placed so that every valid test of every check lands clear of the hold line."""
from datetime import date, timedelta
from math import sqrt

import numpy as np

import params as P
import world as W

RATIO = {"gap": "gaps", "dup": "dups", "late": "lates"}


def mondays():
    d, out = P.FIRST_START, []
    while d <= P.LAST_START:
        out.append(d)
        d += timedelta(days=7)
    return out


def schedule(rng):
    """82 experiments on Monday starts, each with a team, title, split, size and truth"""
    starts = mondays()
    n = P.N_CLEAN + len(P.INCIDENTS)
    # two or three starts a Monday, spread over the year
    extra = n - 2 * len(starts)
    idx = np.sort(np.concatenate([np.arange(len(starts)), np.arange(len(starts)),
                                  rng.choice(len(starts), extra, replace=False)]))
    kinds = ["clean"] * P.N_CLEAN + list(P.INCIDENTS)
    # incidents spread through the year: shuffle, then require each quarter to hold incidents of most kinds
    order = rng.permutation(n)
    kinds = [kinds[i] for i in order]
    titles = []
    for t, ts in W.TITLES.items():
        titles += [(t, x) for x in ts]
    titles = [titles[i] for i in rng.permutation(len(titles))]
    splits = list(P.SPLITS)
    splits = [splits[i] for i in rng.permutation(len(splits))]
    exps = []
    for i in range(n):
        st = starts[idx[i]]
        team, title = titles[i]
        exps.append(dict(i=i, start=st, end=st + timedelta(days=P.RUN_DAYS - 1), team=team, title=title,
                         kind=kinds[i], split=splits[i], eng=0.0))
    clean = [e for e in exps if e["kind"] == "clean"]
    for k, e in enumerate(rng.choice(len(clean), P.N_ENGAGE, replace=False)):
        # five that cut reading, four that raised it
        sign = -1.0 if k < 5 else 1.0
        clean[e]["eng"] = sign * float(rng.uniform(*P.ENGAGE))
    for q, e in enumerate(exps):
        e["key"] = "AV-26-%03d" % (q + 1)
    return exps


def arm(rng, n, kind=None, treat=False, eng=0.0, par=None):
    plat = rng.choice(3, n, p=P.PLATFORM_P)
    sess = rng.negative_binomial(P.SESS_K, P.SESS_K / (P.SESS_K + P.SESS_MEAN), n) + 1
    if treat and eng:
        sess = np.maximum(1, np.round(sess * np.exp(eng + rng.normal(0, 0.02, n)))).astype(int)
    fl = np.array([P.FLAKY[p] for p in P.PLATFORMS])[plat]
    flaky = rng.random(n) < fl
    p_gap = np.where(flaky, rng.beta(*P.GAP_FLAKY, n), rng.beta(*P.GAP_OK, n))
    flaky_d = rng.random(n) < P.DUP_FLAKY_P
    p_dup = np.where(flaky_d, rng.beta(*P.DUP_FLAKY, n), rng.beta(*P.DUP_OK, n))
    off = rng.random(n) < P.OFFLINE_P
    p_late = np.where(off, rng.beta(*P.LATE_OFFLINE, n), rng.beta(*P.LATE_OK, n))
    rate = rng.gamma(P.EVENTS_K, P.EVENTS_SCALE, n)
    heavy = np.zeros(n, bool)
    if treat and kind == "loss":
        heavy = sess >= np.quantile(sess, 1 - par["top"])
        p_gap = np.clip(p_gap + np.where(heavy, par["bump"], 0.0), 0, 1)
        if par.get("late"):
            p_late = np.clip(p_late + par["late"], 0, 1)
    if treat and kind == "dup":
        p_dup = np.clip(p_dup + np.where(plat == 1, par["bump"], 0.0), 0, 1)
    if treat and kind == "late":
        p_late = np.clip(p_late + par["bump"], 0, 1)
    gaps = rng.binomial(sess, p_gap)
    dups = rng.binomial(sess, p_dup)
    lates = rng.binomial(sess, p_late)
    ev = rng.poisson(sess * rate)
    if treat and kind == "loss":
        ev = np.where(heavy, rng.binomial(ev, 1 - 0.5 * par["bump"]), ev)
    if treat and kind == "dup":
        ev = ev + np.where(plat == 1, rng.binomial(ev, 0.5 * par["bump"]), 0)
    return dict(plat=plat.astype(np.int8), sess=sess.astype(np.int32), gaps=gaps.astype(np.int32),
                dups=dups.astype(np.int32), lates=lates.astype(np.int32), ev=ev.astype(np.int32))


# ------------------------------------------------------------------ the tests, in the hold direction
def _ratio(a, num):
    x, y = a[num].astype(float), a["sess"].astype(float)
    n = len(x)
    mx, my = x.mean(), y.mean()
    r = mx / my
    v = (x.var(ddof=1) - 2 * r * np.cov(x, y, ddof=1)[0, 1] + r * r * y.var(ddof=1)) / (my * my * n)
    return r, v


def z_delta(c, t, num):
    rc, vc = _ratio(c, num)
    rt, vt = _ratio(t, num)
    return (rt - rc) / sqrt(vc + vt)


def z_logdelta(c, t, num):
    rc, vc = _ratio(c, num)
    rt, vt = _ratio(t, num)
    return (np.log(rt) - np.log(rc)) / sqrt(vc / rc ** 2 + vt / rt ** 2)


def z_quasi(c, t, num):
    G, S, ph, df = [], [], 0.0, 0
    for a in (c, t):
        x, y = a[num].astype(float), a["sess"].astype(float)
        r = x.sum() / y.sum()
        mu = r * y
        ph += float(((x - mu) ** 2 / mu).sum())
        df += len(x)
        G.append(x.sum())
        S.append(y.sum())
    phi = ph / (df - 2)
    return np.log((G[1] / S[1]) / (G[0] / S[0])) / (sqrt(phi) * sqrt(1 / G[0] + 1 / G[1]))


def z_naive(c, t, num):
    xc, yc, xt, yt = float(c[num].sum()), float(c["sess"].sum()), float(t[num].sum()), float(t["sess"].sum())
    p = (xc + xt) / (yc + yt)
    return (xt / yt - xc / yc) / sqrt(p * (1 - p) * (1 / yc + 1 / yt))


def z_unpooled(c, t, num):
    xc, yc, xt, yt = float(c[num].sum()), float(c["sess"].sum()), float(t[num].sum()), float(t["sess"].sum())
    pc, pt = xc / yc, xt / yt
    return (pt - pc) / sqrt(pc * (1 - pc) / yc + pt * (1 - pt) / yt)


def z_mor(c, t, num):
    qc, qt = c[num] / c["sess"], t[num] / t["sess"]
    return (qt.mean() - qc.mean()) / sqrt(qc.var(ddof=1) / len(qc) + qt.var(ddof=1) / len(qt))


def z_epu(c, t):
    a, b = c["ev"].astype(float), t["ev"].astype(float)
    return (a.mean() - b.mean()) / sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))


def z_epu_pooled(c, t):
    a, b = c["ev"].astype(float), t["ev"].astype(float)
    na, nb = len(a), len(b)
    sp = ((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2)
    return (a.mean() - b.mean()) / sqrt(sp * (1 / na + 1 / nb))


def z_epu_poisson(c, t):
    a, b = c["ev"].astype(float), t["ev"].astype(float)
    return (a.mean() - b.mean()) / sqrt(a.mean() / len(a) + b.mean() / len(b))


def z_share(nc, nt, p):
    n = nc + nt
    return (n * p - nt) / sqrt(n * p * (1 - p))


def z_share_exact(nc, nt, p):
    """the exact binomial test's two-sided p-value turned into a hold-direction z"""
    from scipy.stats import binom, norm
    n = nc + nt
    lo = binom.cdf(nt, n, p)
    hi = binom.sf(nt - 1, n, p)
    pv = min(1.0, 2 * min(lo, hi))
    z = norm.isf(pv / 2)
    return z if nt < n * p else -z


def tests(c, t, split):
    z = {}
    for m, col in RATIO.items():
        z[m] = dict(delta=z_delta(c, t, col), logdelta=z_logdelta(c, t, col), quasi=z_quasi(c, t, col),
                    naive=z_naive(c, t, col), unpooled=z_unpooled(c, t, col), mor=z_mor(c, t, col))
    z["epu"] = dict(welch=z_epu(c, t), pooled=z_epu_pooled(c, t), poisson=z_epu_poisson(c, t))
    nc, nt = len(c["sess"]), len(t["sess"])
    z["share"] = dict(normal=z_share(nc, nt, split), exact=z_share_exact(nc, nt, split))
    return z


VALID = {"gap": ("delta", "logdelta", "quasi"), "dup": ("delta", "logdelta", "quasi"),
         "late": ("delta", "logdelta", "quasi"), "epu": ("welch", "pooled"), "share": ("normal", "exact")}
CHECKS = ["gap", "dup", "late", "epu", "share"]


def held(z, m, how=None):
    how = how or VALID[m][0]
    return z[m][how] > P.Z


def clear(z):
    """every valid method on the same side of the line, at least BAND from it"""
    for m, hows in VALID.items():
        vals = [z[m][h] for h in hows]
        if any(abs(v - P.Z) < P.BAND for v in vals):
            return False
        if len({v > P.Z for v in vals}) > 1:
            return False
    return True


def want(e, z):
    """the truth each experiment is placed on"""
    if not clear(z):
        return False
    k, role = e["kind"], e.get("role", set())
    hold = {m: held(z, m) for m in CHECKS}
    if k == "clean":
        need_epu = "epu_hold" in role
        ok = not hold["gap"] and not hold["dup"] and not hold["late"] and not hold["share"] and hold["epu"] == need_epu
        ok = ok and z["late"]["naive"] < P.Z and z["gap"]["mor"] < P.Z and z["late"]["mor"] < P.Z and z["dup"]["mor"] < P.Z
        if "naive_gap_fh" in role:
            ok = ok and z["gap"]["naive"] > P.Z + 0.25 and z["gap"]["unpooled"] > P.Z + 0.25
        return ok
    if k == "loss":
        hi = 9.5 if "mor" in role else 6.5
        ok = 3.0 <= z["gap"]["delta"] <= hi and not hold["dup"] and not hold["share"] and not hold["epu"]
        ok = ok and ((z["gap"]["mor"] > P.Z + 0.1) if "mor" in role else (z["gap"]["mor"] < P.Z - 0.1))
        if "late" in role:
            ok = ok and 2.9 <= z["late"]["delta"] <= 5.5 and z["late"]["mor"] > P.Z + 0.1
        elif "naive_late" in role:
            ok = ok and not hold["late"] and z["late"]["naive"] > P.Z + 0.08 and z["late"]["mor"] < P.Z - 0.1
        else:
            ok = ok and not hold["late"] and z["late"]["naive"] < P.Z and z["late"]["mor"] < P.Z
        return ok
    base = not hold["epu"] and z["late"]["naive"] < P.Z and z["gap"]["mor"] < P.Z and z["late"]["mor"] < P.Z
    if k == "dup":
        return base and z["dup"]["delta"] >= 3.2 and not hold["gap"] and not hold["late"] and not hold["share"]
    if k == "late":
        return (base or True) and z["late"]["delta"] >= 3.2 and z["late"]["mor"] > P.Z + 0.1 and not hold["gap"] \
            and not hold["dup"] and not hold["share"] and not hold["epu"] and z["gap"]["mor"] < P.Z
    if k == "consent":
        ok = base and z["share"]["normal"] >= 3.0 and not hold["gap"] and not hold["dup"] and not hold["late"]
        if "naive_gap" in role:
            ok = ok and z["gap"]["naive"] > P.Z + 0.1
        return ok
    return False


def draw(rng, e):
    n = int(rng.integers(*P.INSTALLS))
    nt = int(rng.binomial(n, e["split"]))
    nc = n - nt
    k = e["kind"]
    par = {}
    if k == "loss":
        if "mor" in e.get("role", set()):
            par = dict(bump=float(rng.uniform(*P.LOSS_BUMP_BROAD)), top=float(rng.uniform(*P.LOSS_TOP_BROAD)))
        else:
            par = dict(bump=float(rng.uniform(*P.LOSS_BUMP)), top=float(rng.uniform(*P.LOSS_TOP)))
        if "late" in e.get("role", set()):
            par["late"] = float(rng.uniform(*P.LOSS_LATE))
        elif "naive_late" in e.get("role", set()):
            par["late"] = float(rng.uniform(*P.LOSS_LATE_SMALL))
    elif k == "dup":
        par = dict(bump=float(rng.uniform(*P.DUP_BUMP)))
    elif k == "late":
        par = dict(bump=float(rng.uniform(*P.LATE_BUMP)))
    if k == "consent":
        lost = float(rng.uniform(*P.CONSENT_LOST))
        nt = int(round(nt * (1 - lost)))
        par = dict(lost=lost)
    c = arm(rng, nc)
    t = arm(rng, nt, k if k != "clean" else None, True, e["eng"], par)
    return c, t, par


def roles(exps, rng):
    loss = [e for e in exps if e["kind"] == "loss"]
    plan = [{"mor", "late"}, {"mor"}, {"mor"}, {"late"}, {"late"}, {"naive_late"}, set(), set(), set(), set()]
    for j, e in enumerate(loss):
        e["role"] = plan[j]
    cons = [e for e in exps if e["kind"] == "consent"]
    cons[0]["role"] = {"naive_gap"}
    eng_down = [e for e in exps if e["kind"] == "clean" and e["eng"] < 0]
    for e in eng_down[:3]:
        e["role"] = {"epu_hold"}
    plain = [e for e in exps if e["kind"] == "clean" and not e["eng"]]
    for j in rng.choice(len(plain), 2, replace=False):
        plain[j]["role"] = {"naive_gap_fh"}


def corpus(seed=P.SEED):
    rng = np.random.default_rng(seed)
    exps = schedule(rng)
    roles(exps, rng)
    data, tries = [], 0
    for e in exps:
        n_e = 0
        while True:
            tries += 1
            n_e += 1
            assert n_e < 6000, ("placement stuck", e["key"], e["kind"], e.get("role"))
            c, t, par = draw(rng, e)
            z = tests(c, t, e["split"])
            if want(e, z):
                break
        e["par"], e["z"] = par, z
        e["n_c"], e["n_t"] = len(c["sess"]), len(t["sess"])
        data.append((c, t))
    return exps, data, tries
