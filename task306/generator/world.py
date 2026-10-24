"""The cars of the five platforms and their packs, in integer days since 1970: new registrations in the Netherlands,
used imports arriving every month (before and after the register's date), each pack's life drawn from its published
curve, warranty replacements by the OEM, out-of-warranty replacements by a Voltwerk refurbished pack, and the cars that
failed outside the OEM warranty abroad and so were never imported. Same draws, same order as the scratch prototype."""
import numpy as np
import pandas as pd

import params as P

YD = 365.25
AGES = np.arange(0, 21).astype(float)
REF = 5


def D(s):
    return int(np.datetime64(s, "D").astype(np.int64))


def day(d):
    return int(np.datetime64(d, "D").astype(np.int64))


def date(i):
    return np.datetime64(int(i), "D").astype(object)


SNAP, Y0, Y1, END = day(P.SNAP), day(P.Y0), day(P.Y1), day(P.END)


def Fw(a, eta, beta):
    return 1 - np.exp(-(np.maximum(a, 0) / eta) ** beta)


def tables():
    """the published curves: cumulative share of packs failed by whole year of pack age, four decimals"""
    T = [np.round(Fw(AGES, P.PLAT[n][5], P.PLAT[n][6]), 4) for n in P.NAMES]
    T.append(np.round(Fw(AGES, *P.REFURB), 4))
    return T


def world(seed=P.SEED_WORLD):
    rs = np.random.default_rng(seed)
    T = tables()

    def draw(c, n):
        u = rs.random(n)
        t = T[c]
        i = np.clip(np.searchsorted(t, u), 1, len(t) - 1)
        lo, hi = t[i - 1], t[i]
        return np.where(u >= t[-1], AGES[-1] + 1, AGES[i - 1] + (u - lo) / np.maximum(hi - lo, 1e-12))

    PL, FU, NL, IM = [], [], [], []
    for pi, name in enumerate(P.NAMES):
        y_launch, peak, imp_m, imp_age, age_sd, eta, beta = P.PLAT[name]
        for y in range(y_launch, 2027):
            if y < 2026:
                n = int(peak * min(1.0, 0.25 + 0.25 * (y - y_launch)) * rs.uniform(0.9, 1.1))
            else:
                n = int(peak * 0.5 * rs.uniform(0.9, 1.1))
            d = D("%d-01-01" % y) + rs.integers(0, 365 if y < 2026 else 181, n)
            PL.append(np.full(n, pi)); FU.append(d); NL.append(d); IM.append(np.zeros(n, bool))
        months = pd.date_range("%d-01-01" % y_launch, "2027-12-01", freq="MS").values.astype("datetime64[D]").astype(np.int64)
        cnt = rs.poisson(imp_m, len(months))
        reg = np.repeat(months, cnt) + rs.integers(0, 28, cnt.sum())
        age = np.clip(rs.normal(imp_age, age_sd, cnt.sum()), max(1.5, imp_age - 2.2 * age_sd), imp_age + 2.2 * age_sd)
        fu = reg - np.round(age * YD).astype(np.int64)
        keep = fu >= D("%d-01-01" % y_launch)
        PL.append(np.full(keep.sum(), pi)); FU.append(fu[keep]); NL.append(reg[keep]); IM.append(np.ones(keep.sum(), bool))
    plat = np.concatenate(PL); fu = np.concatenate(FU); nl = np.concatenate(NL); imp = np.concatenate(IM)
    n = len(plat)
    exit_d = nl + np.round(np.minimum(rs.exponential(P.EXIT_MEAN, n), 60.0) * YD).astype(np.int64)
    war = np.array([P.WARRANTY[x] for x in P.NAMES], float)
    start = fu.copy(); curve = plat.copy(); oem_end = fu + np.round(war[plat] * YD).astype(np.int64)
    vw_end = np.full(n, -10 ** 9)
    horizon = np.where(nl <= SNAP, SNAP, nl)
    alive = np.ones(n, bool); active = np.ones(n, bool)
    EI, ED, EC, EP = [], [], [], []
    for _ in range(10):
        idx = np.where(active)[0]
        if not len(idx):
            break
        life = np.empty(len(idx))
        for c in np.unique(curve[idx]):
            m = curve[idx] == c
            life[m] = draw(c, m.sum())
        fd = start[idx] + np.round(life * YD).astype(np.int64)
        done = fd > horizon[idx]
        active[idx[done]] = False
        j = idx[~done]; f = fd[~done]
        out = (f < nl[j]) & (f >= oem_end[j])            # failed outside the OEM warranty abroad: never imported
        alive[j[out]] = False; active[j[out]] = False
        j, f = j[~out], f[~out]
        under = f < oem_end[j]
        vw = (curve[j] == REF) & (f < vw_end[j])
        cover = np.where(under, 0, np.where(vw, 1, 2))   # 0 OEM warranty, 1 Voltwerk warranty, 2 paid
        EI.append(j); ED.append(f); EC.append(cover); EP.append(curve[j].copy())
        start[j] = f
        curve[j] = np.where(under, plat[j], REF)
        vw_end[j] = np.where(under, vw_end[j], f + int(round(P.VW_WARRANTY * YD)))
    keep = alive & ((nl > SNAP) | (exit_d > SNAP))
    ev = pd.DataFrame({"i": np.concatenate(EI), "d": np.concatenate(ED), "cover": np.concatenate(EC),
                       "failed_curve": np.concatenate(EP)})
    W = dict(plat=plat, fu=fu, nl=nl, imp=imp, start=start, curve=curve, oem_end=oem_end, keep=keep, alive=alive,
             exit_d=exit_d, T=T)
    return W, ev


def p_due(T, start, curve, oem_end, at_risk_from, survived_to, y0=Y0, y1=Y1, cond=True):
    """chance the pack fitted on `start` fails in [max(y0, at_risk_from, oem_end), y1), given it works at survived_to"""
    out = np.zeros(len(start))
    for c in np.unique(curve):
        m = curve == c
        lo = np.maximum(np.maximum(y0, at_risk_from[m]), oem_end[m])
        a0 = (lo - start[m]) / YD; a1 = (y1 - start[m]) / YD; a_s = (survived_to[m] - start[m]) / YD
        F = lambda a: np.interp(a, AGES, T[c])
        num = np.maximum(F(a1) - F(a0), 0)
        out[m] = np.where(a1 > a0, num / (np.maximum(1 - F(a_s), 1e-9) if cond else 1.0), 0.0)
    return out


def lots(fc, total=P.SLOTS, lot=P.LOT):
    """largest remainder: whole lots of each share first, the lots left to the largest remainders; the margin is the
    gap between the last remainder that took a lot and the first that did not"""
    s = sum(fc.values())
    raw = {k: total * v / s / lot for k, v in fc.items()}
    b = {k: int(np.floor(x)) for k, x in raw.items()}
    rem = total // lot - sum(b.values())
    order = sorted(raw, key=lambda k: -(raw[k] - b[k]))
    for k in order[:rem]:
        b[k] += 1
    r = sorted([raw[k] - np.floor(raw[k]) for k in raw], reverse=True)
    margin = r[rem - 1] - r[rem] if 0 < rem < len(r) else 1.0
    return {k: v * lot for k, v in b.items()}, float(margin), raw


def later_truth(W):
    """the arrivals after the register's date: each at the pack it arrives with, at risk from its arrival"""
    keep = W["keep"]
    later = np.where(keep & (W["nl"] > SNAP))[0]
    p = p_due(W["T"], W["start"][later], W["curve"][later], W["oem_end"][later], W["nl"][later], W["nl"][later])
    return {P.NAMES[k]: float(p[W["plat"][later] == k].sum()) for k in range(len(P.NAMES))}
