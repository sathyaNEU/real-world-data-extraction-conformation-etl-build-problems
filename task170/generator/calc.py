"""The children's part of the C7 order, computed on a clean view of the register: the golden, the family of
constructions that must agree with it, every rival route on the ladder, and the same routes stood at earlier dates
for the out-of-sample record.

A view is two DataFrames:
  kids   one row per child: uid, dob (date), sex (F/M), art_start (date), outcome (None or a code), outcome_date
         (date or None), as the register stood at the pull;
  visits one row per clinic visit: uid, date (date), weight (float, NaN for a collection without a weighing),
         regimen (national code), months (months dispensed), next_appt (date).
A frame fixes the origin (the count, or an earlier month end for a back-test), the month ends of the window and the
months of stock added on its last month. Every quantity is computed forward from the view's rows."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np
import pandas as pd
from scipy.stats import norm

import common as C

D = dt.date
DPM = 30.4375
TLD = C.REG_TLD
PAED1 = ("P1-AB3D10", "P1-AB3D50")


def add_months(d, k):
    y, m = d.year + (d.month - 1 + k) // 12, (d.month - 1 + k) % 12 + 1
    return D(y, m, min(d.day, 28))


def divmod_month(y, m, k):
    t = y * 12 + (m - 1) + k
    return t // 12, t % 12 + 1


def mend(y, m):
    return add_months(D(y, m, 1), 1) - dt.timedelta(days=1)


class Frame:
    def __init__(self, origin, n_months, buffer):
        self.origin = origin
        y, m = origin.year, origin.month
        self.ends = [mend(*divmod_month(y, m, k)) for k in range(1, n_months + 1)]
        self.buffer = buffer

    def mfrac(self, d):
        return (d - self.origin).days / DPM

    def pos(self, d):
        """Window-month position of date d (0 for the first month after the origin)."""
        return (d.year - self.origin.year) * 12 + d.month - self.origin.month - 1


MAIN = Frame(C.COUNT, 10, C.MAX_MONTHS)


# ------------------------------------------------------------------------------------------------ population
def population(kids, visits, fr):
    """Children under 15 at the origin, started on ART on or before it, with no outcome recorded at the origin;
    the last visit on or before the origin says whether each is on TLD, on an adult second line, on the paediatric
    second line (which moves to the adult second line, not to TLD) or a candidate for TLD."""
    o = fr.origin
    try:
        lim15 = D(o.year - 15, o.month, o.day)
    except ValueError:
        lim15 = D(o.year - 15, o.month, 28)
    k = kids[(kids.dob > lim15) & (kids.art_start <= o) &
             (kids.outcome.isna() | (kids.outcome_date > o))]
    v = visits[(visits.date <= o) & visits.uid.isin(k.uid)]
    last = v.sort_values(["uid", "date"]).groupby("uid").tail(1).set_index("uid")
    reg = last.regimen
    on = list(reg.index[reg == TLD])
    cand = list(reg.index[reg.isin(PAED1)])
    return on, cand, last


# ------------------------------------------------------------------------------------------------ retention
def hazards(kids, fr, months=12, by_age=True):
    """Monthly exit hazard: outcomes (lost to follow-up, transferred out, died; not the transfer to adult care at
    twenty) dated in the `months` months to the origin, over children in care at each month's start, under 20, by
    age group (under 12, 12 and over) or pooled."""
    o = fr.origin
    first = add_months(D(o.year, o.month, 1), 1 - months)
    k = kids[kids.art_start <= o]
    dob = pd.to_datetime(k.dob).values
    st = pd.to_datetime(k.art_start).values
    od = pd.to_datetime(k.outcome_date).values
    oc = k.outcome.fillna("").values
    is_exit = np.isin(oc, ["LTFU", "TO", "DIED"])
    num = np.zeros(2)
    den = np.zeros(2)
    for j in range(months):
        a0 = add_months(first, j)
        m0 = np.datetime64(a0)
        m1 = np.datetime64(add_months(a0, 1) - dt.timedelta(days=1))
        alive = np.isnat(od) | (od >= m0)
        age = (m0 - dob).astype("timedelta64[D]").astype(float) / 365.25
        inreg = (st <= m1) & alive & (age < 20)
        ev = is_exit & ~np.isnat(od) & (od >= m0) & (od <= m1)
        g = (age >= 12).astype(int)
        for a in (0, 1):
            sel = inreg & (g == a)
            den[a] += sel.sum()
            num[a] += (sel & ev).sum()
    if by_age:
        return {0: num[0] / den[0], 1: num[1] / den[1]}
    tot = num.sum() / den.sum()
    return {0: tot, 1: tot}


def survival(dobs, h, fr):
    if not len(dobs):
        return np.zeros((0, len(fr.ends)))
    ages = np.array([[(e - b).days / 365.25 for e in fr.ends] for b in dobs])
    hz = np.where(ages < 12, h[0], h[1])
    return np.cumprod(1 - hz, axis=1)


# ------------------------------------------------------------------------------------------------ growth fits
def fits(visits, uids, fr, window_months=None, form="lin", min_n=3):
    """Per-child straight line of weight (or log weight) on months to the origin, from the weighings on or before
    the origin (every weighing in the extract, or the last `window_months`); a, b are the level at the origin and the
    slope per month, sig the pooled residual SD over the children's degrees of freedom."""
    o = fr.origin
    v = visits[visits.uid.isin(uids) & visits.weight.notna() & (visits.date <= o)]
    if window_months is not None:
        v = v[v.date > add_months(o, -window_months)]
    x = np.array([(d - o).days / DPM for d in v.date])
    y = v.weight.values.astype(float) if form == "lin" else np.log(v.weight.values.astype(float))
    df = pd.DataFrame(dict(uid=v.uid.values, x=x, y=y))
    df["xx"] = df.x * df.x
    df["xy"] = df.x * df.y
    g = df.groupby("uid")
    n = g.size()
    sx, sy, sxx, sxy = g.x.sum(), g.y.sum(), g.xx.sum(), g.xy.sum()
    den = n * sxx - sx * sx
    ok = (n >= min_n) & (den > 1e-9)
    n, sx, sy, sxx, sxy, den = n[ok], sx[ok], sy[ok], sxx[ok], sxy[ok], den[ok]
    b = (n * sxy - sx * sy) / den
    a = (sy - b * sx) / n
    d2 = df[df.uid.isin(a.index)]
    yh = a.reindex(d2.uid).values + b.reindex(d2.uid).values * d2.x.values
    wh = yh if form == "lin" else np.exp(yh)
    wobs = d2.y.values if form == "lin" else np.exp(d2.y.values)
    res = wobs - wh
    nn = n.reindex(d2.uid).values
    sig = float(np.sqrt(np.sum(res ** 2) / np.sum(1 - 2.0 / nn)))
    return a, b, sig, n


def future_visits(last, uids, fr, monthly=False):
    """The scheduled visits from the origin to the window's end: the last visit's next appointment, then every
    `months dispensed` months; an appointment already passed at the origin is carried forward by the same
    interval. Returns, per child, fractional months from the origin and window-month positions."""
    out_x, out_k = [], []
    endw = fr.ends[-1]
    for u in uids:
        r = last.loc[u]
        step = 1 if monthly else int(r["months"])
        d = r["next_appt"]
        while d <= fr.origin:
            d = add_months(d, step)
        xs, ks = [], []
        while d <= endw:
            xs.append(fr.mfrac(d))
            ks.append(fr.pos(d))
            d = add_months(d, step)
        out_x.append(np.array(xs))
        out_k.append(np.array(ks, int))
    return out_x, out_k


def first_passage(mu_list, k_list, sig, q, thr, nm):
    """P(switched by the end of each window month): each scheduled visit has a weighing with probability q, the
    weighing reads mu + N(0, sig), and the switch is the first reading at or over the threshold."""
    P = np.zeros((len(mu_list), nm))
    for j, (mu, ks) in enumerate(zip(mu_list, k_list)):
        if len(mu) == 0:
            continue
        p = (norm.sf((thr - mu) / sig) if sig > 0 else (mu >= thr).astype(float)) * q
        cum = 1 - np.cumprod(1 - p)
        idx = np.searchsorted(ks, np.arange(nm), side="right") - 1
        P[j] = np.where(idx >= 0, cum[np.clip(idx, 0, None)], 0.0)
    return P


def pickup_share(visits, uids, fr):
    o = fr.origin
    v = visits[visits.uid.isin(uids) & (visits.date > add_months(o, -12)) & (visits.date <= o)]
    return float(v.weight.isna().mean())


class Ctx:
    pass


def context(kids, visits, fr=MAIN, hz_months=12, by_age=True):
    c = Ctx()
    c.fr = fr
    c.kids, c.visits = kids, visits
    c.on, c.cand, c.last = population(kids, visits, fr)
    kk = kids.set_index("uid")
    c.kk = kk
    c.dob = kk.dob
    c.sex = kk.sex
    c.h = hazards(kids, fr, hz_months, by_age)
    c.S_on = survival(c.dob.reindex(c.on).values, c.h, fr)
    c.S_c = survival(c.dob.reindex(c.cand).values, c.h, fr)
    c.fx, c.fk = future_visits(c.last, c.cand, fr)
    c.q = 1 - pickup_share(visits, c.cand, fr)
    v = visits[visits.uid.isin(c.cand) & visits.weight.notna() & (visits.date <= fr.origin)]
    c.lastw = v.sort_values(["uid", "date"]).groupby("uid").weight.last().to_dict()
    c.nm = len(fr.ends)
    return c


def total(c, P, S_on=None, S_c=None):
    """Bottles over the window: each child on TLD at a month's end takes one bottle; the buffer months on the last
    month's."""
    S_on = c.S_on if S_on is None else S_on
    S_c = c.S_c if S_c is None else S_c
    Cm = S_on.sum(0) + (P * S_c).sum(0)
    return float(Cm.sum() + c.fr.buffer * Cm[-1]), Cm


def switches(c, P):
    """Expected switches among the candidates by the window's end (in care at the end)."""
    return float((P[:, -1] * c.S_c[:, -1]).sum())


def mu_line(c, a, b, form="lin", fx=None):
    fx = c.fx if fx is None else fx
    out = []
    for j, u in enumerate(c.cand):
        xs = fx[j]
        if u in a.index:
            y = a[u] + b[u] * xs
            out.append(y if form == "lin" else np.exp(y))
        else:
            out.append(np.full(len(xs), c.lastw.get(u, 0.0)))
    return out


def P_noisy(c, window=None, thr=29.95, q=None, form="lin", sig=None, monthly=False):
    a, b, s, n = fits(c.visits, c.cand, c.fr, window, form)
    if monthly:
        fx, fk = future_visits(c.last, c.cand, c.fr, monthly=True)
    else:
        fx, fk = c.fx, c.fk
    mu = mu_line(c, a, b, form, fx)
    return first_passage(mu, fk, s if sig is None else sig, c.q if q is None else q, thr, c.nm), s


def scatter(c, kind):
    """Other estimates of a weighing's scatter around the candidates' lines through every weighing: "rms" the
    residuals' root mean square with no allowance for the two fitted parameters, "mad" 1.4826 times their median
    absolute deviation, "diff" from consecutive weighings net of the line's slope, "near" the residual SD of the
    children whose line stands at 24 to 30 kg at the origin."""
    o = c.fr.origin
    a, b, s, n = fits(c.visits, c.cand, c.fr, None, "lin")
    v = c.visits[c.visits.uid.isin(a.index) & c.visits.weight.notna() & (c.visits.date <= o)].copy()
    v["x"] = [(d - o).days / DPM for d in v.date]
    res = v.weight.values - (a.reindex(v.uid).values + b.reindex(v.uid).values * v.x.values)
    if kind == "rms":
        return float(np.sqrt(np.mean(res ** 2)))
    if kind == "mad":
        return float(1.4826 * np.median(np.abs(res - np.median(res))))
    if kind == "diff":
        vv = v.sort_values(["uid", "date"])
        dw = vv.groupby("uid").weight.diff().values
        dx = vv.groupby("uid").x.diff().values
        bb = b.reindex(vv.uid).values
        m = ~np.isnan(dw)
        return float(np.sqrt(np.mean((dw[m] - bb[m] * dx[m]) ** 2) / 2))
    near = v.uid.map(lambda u: 24 <= a[u] < 30).values
    return float(np.sqrt(np.sum(res[near] ** 2) / (near.sum() - 2 * len(set(v.uid[near])))))


def P_smooth(c, window=None, form="lin", thr=30.0):
    a, b, s, n = fits(c.visits, c.cand, c.fr, window, form)
    return first_passage(mu_line(c, a, b, form), c.fk, 0.0, 1.0, thr, c.nm)


def P_pooled_velocity(c, thr=29.95, pool="cand"):
    """Each child's level at the origin from its line, the slope pooled by sex and year of age from consecutive
    weighings over the 24 months to the origin, over the candidates (pool "cand") or every child under 15 on a
    paediatric regimen at the weighing (pool "all")."""
    o = c.fr.origin
    a, b, s, n = fits(c.visits, c.cand, c.fr, None, "lin")
    v = c.visits[c.visits.weight.notna() & (c.visits.date <= o) & (c.visits.date > add_months(o, -24))]
    if pool == "cand":
        v = v[v.uid.isin(c.cand)]
    elif pool == "paed":
        v = v[v.regimen.isin(PAED1)]
    v = v.sort_values(["uid", "date"]).copy()
    dob = c.dob.reindex(v.uid).values
    v["age"] = [(d - b_).days / 365.25 for d, b_ in zip(v.date, dob)]
    v["sx"] = c.sex.reindex(v.uid).values
    v["dw"] = v.groupby("uid").weight.diff()
    v["dt"] = [(z.days / DPM) if isinstance(z, dt.timedelta) else np.nan for z in v.groupby("uid").date.diff()]
    v = v[(v.dt > 0) & (v.dt <= 3.5)]
    v["ab"] = np.floor(v.age)
    vel = (v.groupby(["sx", "ab"]).dw.sum() / v.groupby(["sx", "ab"]).dt.sum()).to_dict()
    mu = []
    for j, u in enumerate(c.cand):
        age0 = (o - c.dob[u]).days / 365.25
        vv = vel.get((c.sex[u], float(math.floor(age0))), 0.2)
        w0 = a[u] if u in a.index else c.lastw.get(u, 0.0)
        mu.append(w0 + vv * c.fx[j])
    return first_passage(mu, c.fk, s, c.q, thr, c.nm)


def P_eb(c, thr=29.95):
    """Each child's slope shrunk toward the candidates' mean slope by its own precision, the between-child variance
    taken from unweighted moments (on this register it comes out at zero, so every child takes the mean slope)."""
    o = c.fr.origin
    a, b, s, n = fits(c.visits, c.cand, c.fr, None, "lin")
    v = c.visits[c.visits.uid.isin(a.index) & c.visits.weight.notna() & (c.visits.date <= o)].copy()
    v["x"] = [(d - o).days / DPM for d in v.date]
    g = v.groupby("uid")
    xb = g.x.mean()
    sxx = (v.x ** 2).groupby(v.uid).sum() - g.size() * xb ** 2
    se2 = s ** 2 / sxx
    vb = max(1e-6, float(b.var() - se2.mean()))
    w = vb / (vb + se2)
    bs = w * b + (1 - w) * float(b.mean())
    ash = g.weight.mean() - bs * xb
    return first_passage(mu_line(c, ash, bs), c.fk, s, c.q, thr, c.nm)


def dersimonian_laird(bv, se2):
    """The random-effects mean and between-unit variance of estimates `bv` with sampling variances `se2`
    (DerSimonian and Laird): returns (mean, tau2, Q, k)."""
    w = 1.0 / se2
    mu = float((w * bv).sum() / w.sum())
    Q = float((w * (bv - mu) ** 2).sum())
    k = len(bv)
    t2 = max(0.0, (Q - (k - 1)) / float(w.sum() - (w ** 2).sum() / w.sum()))
    return mu, t2, Q, k


def P_eb_dl(c, thr=30.0, by_group=False):
    """Each child's slope shrunk toward the candidates' random-effects mean slope (or its sex and year of age's) by
    its own precision, the between-child variance estimated by DerSimonian and Laird."""
    o = c.fr.origin
    a, b, s, n = fits(c.visits, c.cand, c.fr, None, "lin")
    v = c.visits[c.visits.uid.isin(a.index) & c.visits.weight.notna() & (c.visits.date <= o)].copy()
    v["x"] = [(d - o).days / DPM for d in v.date]
    g = v.groupby("uid")
    xb = g.x.mean()
    sxx = (v.x ** 2).groupby(v.uid).sum() - g.size() * xb ** 2
    se2 = s ** 2 / sxx
    bs = pd.Series(index=b.index, dtype=float)
    if by_group:
        age = pd.Series({u: (o - c.dob[u]).days / 365.25 for u in a.index})
        grp = pd.Series({u: "%s%d" % (c.sex[u], math.floor(age[u])) for u in a.index})
        for _, idx in grp.groupby(grp).groups.items():
            mu, t2, _, _ = dersimonian_laird(b[idx], se2[idx])
            w = t2 / (t2 + se2[idx])
            bs[idx] = w * b[idx] + (1 - w) * mu
    else:
        mu, t2, _, _ = dersimonian_laird(b, se2)
        w = t2 / (t2 + se2)
        bs[:] = w * b + (1 - w) * mu
    ash = g.weight.mean() - bs * xb
    return first_passage(mu_line(c, ash, bs), c.fk, s, c.q, thr, c.nm)


def slope_heterogeneity(c):
    """The candidates' per-child slopes against their estimation error: (tau, Q, k) by DerSimonian and Laird."""
    o = c.fr.origin
    a, b, s, n = fits(c.visits, c.cand, c.fr, None, "lin")
    v = c.visits[c.visits.uid.isin(a.index) & c.visits.weight.notna() & (c.visits.date <= o)].copy()
    v["x"] = [(d - o).days / DPM for d in v.date]
    g = v.groupby("uid")
    xb = g.x.mean()
    sxx = (v.x ** 2).groupby(v.uid).sum() - g.size() * xb ** 2
    mu, t2, Q, k = dersimonian_laird(b, s ** 2 / sxx)
    return math.sqrt(t2), Q, k


def P_monte_carlo(c, draws=400, seed=7, thr=29.95):
    a, b, s, n = fits(c.visits, c.cand, c.fr, None, "lin")
    mu = mu_line(c, a, b)
    rng = np.random.default_rng(seed)
    P = np.zeros((len(c.cand), c.nm))
    for j, (m_, ks) in enumerate(zip(mu, c.fk)):
        if len(m_) == 0:
            continue
        r = m_[None, :] + rng.normal(0, s, (draws, len(m_)))
        hit = (r >= thr) & (rng.random((draws, len(m_))) < c.q)
        first = np.where(hit.any(1), hit.argmax(1), 10 ** 6)
        idx = np.searchsorted(ks, np.arange(c.nm), side="right") - 1
        for m in range(c.nm):
            if idx[m] >= 0:
                P[j, m] = (first <= idx[m]).mean()
    return P


# ------------------------------------------------------------------------------------------------ switch history
def switch_dates(c):
    """The first visit on TLD of each child whose earlier visit in the extract was on a paediatric first line."""
    if hasattr(c, "_sw"):
        return c._sw
    v = c.visits[(c.visits.date <= c.fr.origin)]
    t = v[v.regimen == TLD].groupby("uid").date.min()
    prev = v[v.regimen.isin(PAED1)].groupby("uid").date.min()
    t = t[t.index.isin(prev.index)]
    t = t[np.array([prev[u] < t[u] for u in t.index], bool)]
    c._sw = t
    return t


def _months_between(a, b):
    return (b.year - a.year) * 12 + b.month - a.month


def P_band_hazard(c, bw=0.5, lo_months=30, hi_months=10):
    """Rung: the register's own switches by recorded weight band. At each month end from 30 to 10 months before the
    origin, children under 15 in care on a paediatric first line are banded by their last recorded weight; the
    cumulative share switching within k months (Kaplan-Meier, censored at an outcome or the origin) is carried to
    each candidate's last recorded weight."""
    o = c.fr.origin
    sw = switch_dates(c)
    kk = c.kk
    vv = c.visits[(c.visits.date <= o)].sort_values("date")
    vw = vv[vv.weight.notna()]
    rows = []
    for back in range(lo_months, hi_months - 1, -1):
        S = mend(*divmod_month(o.year, o.month, -back))
        lw = vw[vw.date <= S].groupby("uid").weight.last()
        lr = vv[vv.date <= S].groupby("uid").regimen.last().reindex(lw.index)
        dob = kk.dob.reindex(lw.index)
        od = kk.outcome_date.reindex(lw.index)
        under15 = np.array([(S - b).days / 365.25 < 15 for b in dob])
        alive = np.array([(x is None) or pd.isna(x) or (x > S) for x in od])
        ok = under15 & alive & lr.isin(PAED1).values & (lw.values >= 18) & (lw.values < 30)
        for u, w in zip(lw.index[ok], lw.values[ok]):
            rows.append((u, S, w))
    R = pd.DataFrame(rows, columns=["uid", "S", "w"])
    R["band"] = np.floor(R.w / bw) * bw
    KH = c.nm + 1
    F = {}
    for bnd, dd in R.groupby("band"):
        dsw, dex = [], []
        for u, S in zip(dd.uid, dd.S):
            s_ = sw.get(u, None)
            ksw = _months_between(S, s_) if (s_ is not None and not pd.isna(s_)) else 10 ** 6
            oc = kk.outcome_date.get(u, None)
            kex = _months_between(S, oc) if (oc is not None and not pd.isna(oc)) else 10 ** 6
            dsw.append(ksw)
            dex.append(min(kex, _months_between(S, o) + 1))
        dsw, dex = np.array(dsw), np.array(dex)
        Fk = np.zeros(KH + 1)
        s = 1.0
        for k in range(1, KH + 1):
            ar = (np.minimum(dsw, dex) >= k).sum()
            ev = ((dsw == k) & (dex >= k)).sum()
            if ar > 0:
                s *= 1 - ev / ar
            Fk[k] = 1 - s
        F[bnd] = Fk
    P = np.zeros((len(c.cand), c.nm))
    for j, u in enumerate(c.cand):
        bnd = math.floor(c.lastw.get(u, 0.0) / bw) * bw
        if bnd in F:
            P[j] = F[bnd][1:c.nm + 1]
    return P


def new_switches_total(c, new):
    """Bottles when `new[k]` children switch in window month k: each on TLD from that month, at the candidates'
    average survival from then on."""
    sbar = c.S_c.mean(0) if len(c.cand) else np.ones(c.nm)
    Cm = c.S_on.sum(0).copy()
    for k in range(c.nm):
        for m in range(k, c.nm):
            Cm[m] += new[k] * (sbar[m] / sbar[k] if sbar[k] > 0 else 1.0)
    return float(Cm.sum() + c.fr.buffer * Cm[-1])


def need_band_chain(c, months=12):
    """Rung: the quantification's weight-band chain. Children on a paediatric first line in the 20-24.9 kg and
    25-29.9 kg bands (last recorded weight), monthly transition rates between the bands and onto TLD measured over
    the last `months` months, run forward as a chain."""
    o = c.fr.origin
    sw = switch_dates(c)
    kk = c.kk
    vw = c.visits[c.visits.weight.notna() & (c.visits.date <= o)].sort_values("date")
    vv = c.visits[(c.visits.date <= o)].sort_values("date")
    n20 = n25 = up20 = up25 = 0
    for back in range(months, 0, -1):
        S = mend(*divmod_month(o.year, o.month, -back))
        S1 = mend(*divmod_month(o.year, o.month, -back + 1))
        lw = vw[vw.date <= S].groupby("uid").weight.last()
        lr = vv[vv.date <= S].groupby("uid").regimen.last().reindex(lw.index)
        nw = vw[vw.date <= S1].groupby("uid").weight.last().reindex(lw.index)
        dob = kk.dob.reindex(lw.index)
        od = kk.outcome_date.reindex(lw.index)
        under15 = np.array([(S - b).days / 365.25 < 15 for b in dob])
        alive = np.array([(x is None) or pd.isna(x) or (x > S) for x in od])
        paed = lr.isin(PAED1).values
        swd = sw.reindex(lw.index)
        swnext = np.array([(not pd.isna(x)) and (S < x <= S1) for x in swd])
        base = under15 & alive & paed
        b20 = base & (lw.values >= 20) & (lw.values < 25)
        b25 = base & (lw.values >= 25) & (lw.values < 30)
        n20 += b20.sum()
        n25 += b25.sum()
        up20 += (b20 & (nw.values >= 25)).sum()
        up25 += (b25 & swnext).sum()
    r20, r25 = up20 / max(1, n20), up25 / max(1, n25)
    s20 = float(sum(1 for u in c.cand if 20 <= c.lastw.get(u, 0) < 25))
    s25 = float(sum(1 for u in c.cand if 25 <= c.lastw.get(u, 0) < 30))
    new = []
    for k in range(c.nm):
        m20, m25 = s20 * r20, s25 * r25
        s20 -= m20
        s25 += m20 - m25
        new.append(m25)
    return new_switches_total(c, np.array(new))


def need_recent(c, months):
    """Rung: the switches of the last `months` months, carried at the same monthly count."""
    sw = switch_dates(c)
    o = c.fr.origin
    lo = mend(*divmod_month(o.year, o.month, -months))
    r = float(((sw > lo) & (sw <= o)).sum()) / months
    return new_switches_total(c, np.full(c.nm, r))


def need_trend(c):
    """Rung: the last four half-years' switch counts, a straight line carried forward."""
    sw = switch_dates(c)
    o = c.fr.origin
    hy = []
    for k in range(4, 0, -1):
        a = mend(*divmod_month(o.year, o.month, -6 * k))
        b = mend(*divmod_month(o.year, o.month, -6 * (k - 1)))
        hy.append(float(((sw > a) & (sw <= b)).sum()))
    sl = np.polyfit(np.arange(4), hy, 1)
    rates = [np.polyval(sl, 4) / 6] * 6 + [np.polyval(sl, 5) / 6] * 6
    return new_switches_total(c, np.array(rates[:c.nm]))


def median_switch_age(c, months=18):
    o = c.fr.origin
    sw = switch_dates(c)
    lo = mend(*divmod_month(o.year, o.month, -months))
    rec = sw[(sw > lo) & (sw <= o)]
    med = {}
    for s in ("F", "M"):
        us = [u for u in rec.index if c.sex[u] == s]
        med[s] = float(np.median([(rec[u] - c.dob[u]).days / 365.25 for u in us])) if us else 11.0
    return med


def P_age(c, age=None, backlog=True):
    """Rung: the switch at a fixed age (the median age of the last 18 months' switchers by sex when age is None),
    at the first scheduled visit at or after it; a child already older switches at its next visit (backlog) or not
    at all (backlog False)."""
    o = c.fr.origin
    med = median_switch_age(c)
    P = np.zeros((len(c.cand), c.nm))
    for j, u in enumerate(c.cand):
        A = med[c.sex[u]] if age is None else age
        a0 = (o - c.dob[u]).days / 365.25
        ks, xs = c.fk[j], c.fx[j]
        if len(ks) == 0:
            continue
        if a0 >= A:
            if not backlog:
                continue
            k0 = ks[0]
        else:
            hit = np.where(a0 + xs * DPM / 365.25 >= A)[0]
            if not len(hit):
                continue
            k0 = ks[hit[0]]
        P[j, k0:] = 1.0
    return P


def P_now_if(c, cond):
    """Rung: every candidate meeting `cond(uid)` switches at its next scheduled visit."""
    P = np.zeros((len(c.cand), c.nm))
    for j, u in enumerate(c.cand):
        if cond(u) and len(c.fk[j]):
            P[j, c.fk[j][0]:] = 1.0
    return P


def crossing_age(c, look=12, bw=0.25, smooth=5, stat="median", interp=False, by_sex=True):
    """The age at which the register's weight for age (the last `look` months' weighings, in age bins of `bw` years,
    the bin's median or mean, a `smooth`-point running median) reaches 30 kg: the first bin at or over it, or the
    age interpolated between that bin and the one before."""
    o = c.fr.origin
    v = c.visits[c.visits.weight.notna() & (c.visits.date <= o) & (c.visits.date > add_months(o, -look))].copy()
    v["age"] = [(d - b).days / 365.25 for d, b in zip(v.date, c.dob.reindex(v.uid).values)]
    v["sx"] = c.sex.reindex(v.uid).values if by_sex else "A"
    v["ab"] = np.round(v.age / bw) * bw
    g = v.groupby(["sx", "ab"]).weight
    med = g.median() if stat == "median" else g.mean()
    cross = {}
    for s in sorted(set(v.sx)):
        mm = med.loc[s]
        if smooth > 1:
            mm = mm.rolling(smooth, center=True, min_periods=1).median()
        idx, val = np.array(mm.index, float), np.array(mm.values, float)
        k = np.where(val >= 30)[0]
        if not len(k):
            cross[s] = 99.0
        elif interp and k[0] > 0:
            j = k[0]
            cross[s] = float(idx[j - 1] + (30 - val[j - 1]) / (val[j] - val[j - 1]) * (idx[j] - idx[j - 1]))
        else:
            cross[s] = float(idx[k[0]])
    if not by_sex:
        cross = {"F": cross["A"], "M": cross["A"]}
    return cross


def P_crossing_age(c, backlog=False, **kw):
    """Rung: each candidate switches at its first scheduled visit at or after the register's crossing age; a child
    already past it switches at its first visit (backlog) or not at all (window)."""
    cross = crossing_age(c, **kw)
    o = c.fr.origin
    P = np.zeros((len(c.cand), c.nm))
    for j, u in enumerate(c.cand):
        A = cross[c.sex[u]]
        a0 = (o - c.dob[u]).days / 365.25
        ks, xs = c.fk[j], c.fx[j]
        if len(ks) == 0:
            continue
        if a0 >= A:
            if backlog:
                P[j, ks[0]:] = 1.0
            continue
        hit = np.where(a0 + xs * DPM / 365.25 >= A)[0]
        if len(hit):
            P[j, ks[hit[0]]:] = 1.0
    return P, cross


def P_mean_curve(c):
    """Rung: the age at which the register's median weight for age (last 12 months' weighings, by sex, in quarter
    years, a five-point running median) reaches 30 kg, each candidate switching at its first visit at or after it."""
    return P_crossing_age(c)


def P_centile_tracking(c):
    """Rung: each candidate follows the register's median weight-for-age curve (last 12 months' weighings, by sex,
    quarter years, five-point running median) from its own level at the origin, the switch at the first scheduled
    visit at which that path reaches 30 kg."""
    o = c.fr.origin
    v = c.visits[c.visits.weight.notna() & (c.visits.date <= o) & (c.visits.date > add_months(o, -12))].copy()
    v["age"] = [(d - b).days / 365.25 for d, b in zip(v.date, c.dob.reindex(v.uid).values)]
    v["sx"] = c.sex.reindex(v.uid).values
    v["ab"] = np.round(v.age * 4) / 4
    med = v.groupby(["sx", "ab"]).weight.median()
    curve = {}
    for s in ("F", "M"):
        mm = med.loc[s].rolling(5, center=True, min_periods=1).median()
        curve[s] = (np.array(mm.index, float), np.array(mm.values, float))
    a, b, sig, n = fits(c.visits, c.cand, c.fr, None, "lin")
    mu = []
    for j, u in enumerate(c.cand):
        ages, wts = curve[c.sex[u]]
        a0 = (o - c.dob[u]).days / 365.25
        lvl = a[u] if u in a.index else c.lastw.get(u, 0.0)
        at = a0 + c.fx[j] * DPM / 365.25
        mu.append(lvl + np.interp(at, ages, wts) - np.interp(a0, ages, wts))
    return first_passage(mu, c.fk, 0.0, 1.0, 30.0, c.nm)


def P_lead_shift(c, months=24):
    """Rung: the smooth line moved earlier by the register's own median lead: for each child who switched in the
    last `months` months, the months from the switch to the month its line (fitted to the weighings before the
    switch) reaches 30 kg."""
    o = c.fr.origin
    sw = switch_dates(c)
    lo = mend(*divmod_month(o.year, o.month, -months))
    rec = sw[(sw > lo) & (sw <= o)]
    leads = []
    vv = c.visits[c.visits.weight.notna() & c.visits.uid.isin(rec.index)]
    for u, g in vv.groupby("uid"):
        g = g[g.date < rec[u]]
        if len(g) < 4:
            continue
        x = np.array([(d - rec[u]).days / DPM for d in g.date])
        bb, aa = np.polyfit(x, g.weight.values.astype(float), 1)
        if bb <= 0.02:
            continue
        leads.append((30.0 - aa) / bb)
    L = float(np.median(leads))
    a, b, s, n = fits(c.visits, c.cand, c.fr, None, "lin")
    mu = [m + b.get(u, 0.0) * L for m, u in zip(mu_line(c, a, b), c.cand)]
    return first_passage(mu, c.fk, 0.0, 1.0, 30.0, c.nm), L


def actual_switches(c_origin, visits_all):
    """Switches recorded in the register among an origin's candidates, by window month (a back-test's outcome)."""
    sw = visits_all[visits_all.regimen == TLD].groupby("uid").date.min()
    out = np.zeros(c_origin.nm)
    for u in c_origin.cand:
        d = sw.get(u, None)
        if d is not None and d > c_origin.fr.origin:
            k = c_origin.fr.pos(d)
            if 0 <= k < c_origin.nm:
                out[k:] += 1
    return out
