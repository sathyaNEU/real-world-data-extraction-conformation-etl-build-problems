"""Estimators shared by the generator's own pipeline and checks.py (verify.py carries its own).

Rows are one region's sampled areas for one wave: dict(code, stratum, m_all, w, y) with w the final weight of each
completed interview in the area and y the usable answers (1 = a member did not fill a prescription because of cost).
"""
import numpy as np

BOOST = 1200


def flat(rows):
    y = np.concatenate([r["y"] for r in rows])
    w = np.concatenate([np.full(len(r["y"]), r["w"]) for r in rows])
    area = np.concatenate([np.full(len(r["y"]), i) for i, r in enumerate(rows)])
    strata = np.concatenate([np.full(len(r["y"]), r["stratum"], dtype=object) for r in rows])
    return y, w, area, strata


def estimate(rows):
    y, w, _, _ = flat(rows)
    return float((w * y).sum() / w.sum())


def design_var(rows, strata_key="stratum"):
    """Taylor linearisation of the weighted share, sampled areas as PSUs within strata, with replacement."""
    y, w, area, strata = flat(rows)
    W = w.sum()
    p = (w * y).sum() / W
    z = w * (y - p) / W
    v = 0.0
    for h in sorted(set(r[strata_key] for r in rows)):
        zc = np.array([z[area == i].sum() for i, r in enumerate(rows) if r[strata_key] == h])
        kh = len(zc)
        if kh > 1:
            v += kh / (kh - 1) * ((zc - zc.mean()) ** 2).sum()
    return float(p), float(v)


def deff(rows):
    y, w, _, _ = flat(rows)
    p, v = design_var(rows)
    return v / (p * (1 - p) / len(y))


def deff_w(rows, add=0.0):
    """Kish's weighting effect, n sum w^2 / (sum w)^2, over the usable answers (optionally at boosted takes)."""
    n = sum(len(r["y"]) + add for r in rows)
    s1 = sum((len(r["y"]) + add) * (r["w"] * r["m_all"] / (r["m_all"] + add)) for r in rows)
    s2 = sum((len(r["y"]) + add) * (r["w"] * r["m_all"] / (r["m_all"] + add)) ** 2 for r in rows)
    return n * s2 / s1 ** 2


def anova(rows, weighted=False):
    """One-way ANOVA components on the observed binary scale over the region's areas (strata pooled)."""
    ys = [r["y"] for r in rows if len(r["y"]) > 0]
    k = len(ys)
    m = np.array([len(a) for a in ys], float)
    n = m.sum()
    means = np.array([a.mean() for a in ys])
    ssw = sum(((a - a.mean()) ** 2).sum() for a in ys)
    msw = ssw / (n - k)
    if not weighted:
        gm = np.concatenate(ys).mean()
        msb = (m * (means - gm) ** 2).sum() / (k - 1)
        m0 = (n - (m ** 2).sum() / n) / (k - 1)
        sb = (msb - msw) / m0
    else:
        # E sum a (ybar_c - ybar_a)^2 = sb (1 - sum a^2) + sw sum a (1 - a) / m, with a the areas' weight shares
        a = np.array([r["w"] * r["m_all"] for r in rows if len(r["y"]) > 0])
        a = a / a.sum()
        gm = (a * means).sum()
        sb = ((a * (means - gm) ** 2).sum() - msw * (a * (1 - a) / m).sum()) / (1 - (a ** 2).sum())
    return max(float(sb), 0.0), float(msw)


def anova_by_stratum(rows):
    """Components within each stratum, returned per row (the stratum's own pair)."""
    out = {}
    for h in sorted(set(r["stratum"] for r in rows)):
        sub = [r for r in rows if r["stratum"] == h]
        out[h] = anova(sub)
    return out


def reml(rows):
    """One-way random-effects REML on the observed scale, profiled over lambda = sb / sw on a fine grid."""
    ys = [r["y"] for r in rows if len(r["y"]) > 0]
    m = np.array([len(a) for a in ys], float)
    sums = np.array([a.sum() for a in ys])
    sumsq = np.array([(a ** 2).sum() for a in ys])
    n = m.sum()
    best = None
    lams = np.concatenate([[0.0], np.exp(np.linspace(np.log(1e-5), np.log(5.0), 1500))])
    for lam in lams:
        d = 1.0 + lam * m
        wsum = (m / d).sum()
        mu = (sums / d).sum() / wsum
        rr = sumsq - 2 * mu * sums + m * mu ** 2
        sr = sums - m * mu
        q = (rr - lam / d * sr ** 2).sum()
        sw = q / (n - 1)
        ll = -0.5 * ((n - 1) * np.log(sw) + np.log(d).sum() + np.log(wsum))
        if best is None or ll > best[0]:
            best = (ll, lam, sw)
    _, lam, sw = best
    return float(lam * sw), float(sw)


def design_components(rows):
    """Design-based components: the within part from the areas' own sample variances, the between part what the
    design variance leaves once the within contribution is taken out."""
    _, v = design_var(rows)
    ys = [r["y"] for r in rows]
    m = np.array([len(a) for a in ys], float)
    k = len(ys)
    ssw = sum(((a - a.mean()) ** 2).sum() for a in ys if len(a) > 0)
    sw = ssw / (m.sum() - k)
    a = np.array([r["w"] * r["m_all"] for r in rows])
    a = a / a.sum()
    sb = (v - sw * (a ** 2 / m).sum()) / (a ** 2).sum()
    return max(float(sb), 0.0), float(sw)


def shares_a(rows):
    a = np.array([r["w"] * r["m_all"] for r in rows], float)
    return a / a.sum()


def comp_var(rows, sb, sw, add=0.0, by_stratum=None):
    a = shares_a(rows)
    m = np.array([len(r["y"]) for r in rows], float)
    if by_stratum is None:
        return float((a ** 2 * (sb + sw / (m + add))).sum())
    sbv = np.array([by_stratum[r["stratum"]][0] for r in rows])
    swv = np.array([by_stratum[r["stratum"]][1] for r in rows])
    return float((a ** 2 * (sbv + swv / (m + add))).sum())


def comp_share(rows, sb, sw, add, by_stratum=None):
    return 1.0 - np.sqrt(comp_var(rows, sb, sw, add, by_stratum) / comp_var(rows, sb, sw, 0.0, by_stratum))


def icc_share(rows, icc, add):
    """The projection with the between-area and within-area parts set by an intraclass correlation."""
    return comp_share(rows, icc, 1.0 - icc, add)


def pubbase_share(rows, sb, sw, add):
    """The boosted model variance over the realised 2025 design variance (the published error as the baseline)."""
    _, v = design_var(rows)
    return 1.0 - np.sqrt(comp_var(rows, sb, sw, add) / v)


def unfloored_share(rows, add):
    """Design-based components with no floor on the between part."""
    _, v = design_var(rows)
    ys = [r["y"] for r in rows]
    m = np.array([len(a) for a in ys], float)
    ssw = sum(((a - a.mean()) ** 2).sum() for a in ys if len(a) > 0)
    sw = ssw / (m.sum() - len(ys))
    a = shares_a(rows)
    sb = (v - sw * (a ** 2 / m).sum()) / (a ** 2).sum()
    v0 = (a ** 2 * (sb + sw / m)).sum()
    v1 = (a ** 2 * (sb + sw / (m + add))).sum()
    return float(1 - np.sqrt(max(v1, 1e-12) / v0))


def kish_share(rows, rho, add, deffw_held=True, use_deffw=True):
    n = sum(len(r["y"]) for r in rows)
    k = len(rows)
    mbar = n / k
    n2 = n + add * k
    mbar2 = mbar + add
    dw1 = deff_w(rows) if use_deffw else 1.0
    dw2 = dw1 if (deffw_held or not use_deffw) else deff_w(rows, add)
    v1 = dw1 * (1 + (mbar - 1) * rho) / n
    v2 = dw2 * (1 + (mbar2 - 1) * rho) / n2
    return float(1 - np.sqrt(v2 / v1))


def routes(rows):
    """Every rung's share of the 2027 error removed for one region, plus the quantities behind them."""
    k = len(rows)
    add = BOOST / k
    n = sum(len(r["y"]) for r in rows)
    mbar = n / k
    d = deff(rows)
    dw = deff_w(rows)
    sb_a, sw_a = anova(rows)
    rho_a = sb_a / (sb_a + sw_a)
    sb_r, sw_r = reml(rows)
    rho_r = sb_r / (sb_r + sw_r)
    sb_w, sw_w = anova(rows, weighted=True)
    sb_d, sw_d = design_components(rows)
    bys = anova_by_stratum(rows)
    rho_deff = (d - 1) / (mbar - 1)
    rho_kish = max((d / dw - 1) / (mbar - 1), 0.0)
    out = dict(
        R1=float(1 - np.sqrt(n / (n + BOOST))),
        R2=kish_share(rows, rho_deff, add, use_deffw=False),
        R3=kish_share(rows, rho_kish, add, deffw_held=True),
        R3_anova=kish_share(rows, rho_a, add, deffw_held=True),
        R3_reml=kish_share(rows, rho_r, add, deffw_held=True),
        G_anova=comp_share(rows, sb_a, sw_a, add),
        G_reml=comp_share(rows, sb_r, sw_r, add),
        G_wanova=comp_share(rows, sb_w, sw_w, add),
        G_design=comp_share(rows, sb_d, sw_d, add),
        G_strata=comp_share(rows, None, None, add, by_stratum=bys),
        G_kish_recomputed=kish_share(rows, rho_a, add, deffw_held=False),
        G_icc=icc_share(rows, round(max(rho_a, 0.0), 3), add),
        G_pubbase=pubbase_share(rows, sb_a, sw_a, add),
        G_unfloored=unfloored_share(rows, add),
        R3_icc=kish_share(rows, round(max(rho_a, 0.0), 3), add, deffw_held=True),
    )
    out["_"] = dict(n=n, k=k, add=add, mbar=mbar, deff=d, deffw=dw, rho_anova=rho_a, rho_reml=rho_r,
                    icc_pub=round(max(rho_a, 0.0), 3),
                    rho_deff=rho_deff, rho_kish=rho_kish, sb=sb_a, sw=sw_a)
    return out
