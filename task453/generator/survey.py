"""The survey as collected. The sample is fixed slots (a primary sampling unit, a rotation group and a line); every
month one rotation group's slots pass to newly selected dwellings. Each month, region and rotation group carries its
responding dwellings, the persons aged 15 and over in them by sex and age band, how many of those are in the labour
force and how many unemployed, and the weight that carries the rotation group to the whole population.

Draws are inverse-CDF on fixed uniforms, so tuning a rate moves counts smoothly and two builds are identical. The
fourth quarter of 2026 is simulated dwelling by dwelling (the fieldwork log the pack ships); the other months are
drawn at the month x region x group level from the same response model."""
import numpy as np
from scipy.stats import binom, norm

import world as W

SHAPE = (W.T, W.R, 6, 2, len(W.AGES))


def psu_regions():
    """primary sampling units by region (square-root allocation), numbered region by region"""
    share = np.sqrt(W.POP15) / np.sqrt(W.POP15).sum()
    n = np.floor(share * W.PSUS).astype(int)
    n[np.argsort(-(share * W.PSUS - n))[:W.PSUS - n.sum()]] += 1
    rng = np.random.default_rng(W.SEED + 11)
    numbers = rng.choice(np.arange(1001, 4999), size=W.PSUS, replace=False)
    numbers.sort()
    reg = np.repeat(np.arange(W.R), n)
    order = rng.permutation(W.PSUS)                 # unit numbers are not in region order
    return numbers, reg[order]


def uniforms(seed=W.SEED):
    rng = np.random.default_rng(seed)
    return {"dw": rng.random((W.T, W.R, 6)), "pers": rng.standard_normal((W.T, W.R, 6)),
            "split": rng.standard_normal(SHAPE), "lf": rng.random(SHAPE), "u": rng.random(SHAPE),
            "partr": rng.standard_normal((W.R, 2, len(W.AGES))), "el": rng.random((W.T, W.R, 6))}


def lines():
    """sample references in each unit's rotation groups: about twelve, nine to fifteen with the size of the blocks the
    group was listed from"""
    rng = np.random.default_rng(W.SEED + 17)
    return np.clip(np.round(W.LINES + 1.4 * rng.standard_normal((W.PSUS, 6))), 9, 15).astype(int)


def slots_by_region():
    """sample references by region and rotation group"""
    _, reg = psu_regions()
    L = lines()
    return np.stack([np.bincount(reg, weights=L[:, g], minlength=W.R) for g in range(6)], axis=1).astype(int)


def fieldwork_q4():
    """the fourth quarter of 2026, dwelling by dwelling: one row per slot and month"""
    numbers, reg = psu_regions()
    L = lines()
    rng = np.random.default_rng(W.SEED + 29)
    rows = []
    c = {(t, r, m): norm.ppf(W.response(t, W.RCODE[r], m)) * np.sqrt(1 + 1.2 ** 2)
         for t in W.Q4 for r in range(W.R) for m in range(1, 7)}
    area = {}
    arng = np.random.default_rng(W.SEED + 23)
    k, left, i_prev_reg = 100, 0, -1
    for i in sorted(range(len(numbers)), key=lambda i: (reg[i], numbers[i])):    # areas of three to eight units
        if left == 0 or i_prev_reg != reg[i]:
            k, left = k + 1, int(arng.integers(3, 9))
        area[numbers[i]] = "IA-%03d" % k
        left, i_prev_reg = left - 1, reg[i]
    latent = {}
    for t in W.Q4:
        for i, p in enumerate(numbers):
            r = reg[i]
            for g in range(6):
                m = W.mis(t, g)
                e = W.entered(t, g)
                for line in range(1, L[i, g] + 1):
                    key = (p, g, line, e)
                    if key not in latent:
                        u = rng.random()
                        kind = ("derelict" if u < W.DERELICT else "vacant" if u < W.VACANT else
                                "nonprivate" if u < W.VACANT + W.NONPRIVATE else "private")
                        latent[key] = (kind, rng.standard_normal(), rng.random())
                    kind, z, mode_u = latent[key]
                    if kind == "derelict":
                        code = 32
                    elif kind == "vacant":
                        code = 31
                    elif kind == "nonprivate":
                        code = 33
                    else:
                        if c[(t, r, m)] + 1.2 * z + rng.standard_normal() > 0:
                            code = 12 if rng.random() < W.PARTIAL else 11
                        else:
                            v = rng.random()
                            code = 21 if v < 0.55 else (22 if v < 0.90 else 23)
                    if m == 1:
                        mode = "TEL" if mode_u < 0.08 else "F2F"
                    else:
                        mode = "F2F" if mode_u < 0.15 else "TEL"
                    rows.append((W.MONTHS[t], "%04d" % p, W.GROUPS[g], line, m, W.MONTHS[e], code, mode, area[p], r))
    return rows


def responding(U, q4rows):
    """eligible and responding dwellings, and persons aged 15 and over in the responding ones, by month, region and
    rotation group"""
    slots = slots_by_region()
    E = np.zeros((W.T, W.R, 6), int)
    D = np.zeros((W.T, W.R, 6), int)
    for t in range(W.T):
        for g in range(6):
            m = W.mis(t, g)
            E[t, :, g] = binom.ppf(U["el"][t, :, g], slots[:, g], 1 - W.VACANT - W.NONPRIVATE).astype(int)
            prob = np.array([W.response(t, c, m) for c in W.RCODE])
            D[t, :, g] = binom.ppf(U["dw"][t, :, g], E[t, :, g], prob).astype(int)
    if q4rows is not None:
        tix = {W.MONTHS[t]: t for t in W.Q4}
        D[W.Q4] = 0
        E[W.Q4] = 0
        for row in q4rows:
            k = (tix[row[0]], row[9], W.GROUPS.index(row[2]))
            if row[6] not in (31, 32, 33):
                E[k] += 1
            if row[6] in (11, 12):
                D[k] += 1
    P = np.round(D * W.PERSONS * (1 + 0.012 * U["pers"])).astype(int)
    share = W.SEX_SHARE[:, None] * W.AGE_SHARE[None, :]
    n = np.round(P[..., None, None] * share[None, None, None] * (1 + 0.03 * U["split"])).astype(int)
    return D, E, np.maximum(n, 6)


def population():
    """persons aged 15 and over by month, region, sex and age; growing 0.8 per cent a year"""
    grow = 1.0 + 0.008 * (np.arange(W.T) - W.Y26) / 12.0
    irr = 1.0 + 0.025 * np.random.default_rng(W.SEED + 19).standard_normal((W.R, 2, len(W.AGES)))
    P = (W.POP15[None, :, None, None] * 1000.0 * W.SEX_SHARE[None, None, :, None] * W.AGE_SHARE[None, None, None, :] *
         irr[None])
    return np.round(P * grow[:, None, None, None])


def participation(U):
    return np.clip(W.PART[None] * (1 + 0.025 * U["partr"]), 0.2, 0.97)          # region x sex x age


def unemp_norm():
    lf = W.AGE_SHARE[None, :] * W.SEX_SHARE[:, None] * W.PART
    return (lf * W.UFAC).sum() / lf.sum()


def true_rates(level):
    """the unemployment rate (per cent) each cell's questionnaire measures, by month, region, group, sex, age"""
    nrm = unemp_norm()
    p = np.zeros(SHAPE)
    for t in range(W.T):
        for r, code in enumerate(W.RCODE):
            lvl = level[r] * W.UFAC / nrm
            add = W.SEAS[t % 12] + W.NAT[t] + W.DRIFT[code] * t / (W.T - 1)
            for g in range(6):
                m = W.mis(t, g)
                eff = W.MIS_BIAS[m - 1]
                if W.redesigned(t, g):
                    eff += W.FIRST_EFFECT if m == 1 else W.LATER_EFFECT
                p[t, r, g] = lvl + add + eff
    return np.clip(p, 0.3, 60.0)


def collect(level, U, q4rows):
    D, E, n = responding(U, q4rows)
    part = participation(U)
    lf = binom.ppf(U["lf"], n, part[None, :, None]).astype(int)
    p = true_rates(level)
    u = binom.ppf(U["u"], lf, p / 100.0).astype(int)
    pop = population()
    cal = 1.0 + 0.006 * np.random.default_rng(W.SEED + 3).standard_normal(SHAPE)   # calibration moves weights a little
    w = pop[:, :, None] / n * cal                 # each rotation group weighted to the whole population
    emp = np.round((lf - u) * w).astype(np.int64)
    une = np.round(u * w).astype(np.int64)
    nilf = np.round((n - lf) * w).astype(np.int64)
    return dict(D=D, E=E, n=n, lf=lf, u=u, p=p, emp=emp, une=une, nilf=nilf)


def published(S):
    """the published monthly estimates: every rotation group (both questionnaires in July to November 2025)"""
    U = S["une"].sum(axis=(2, 3, 4)).astype(float)
    L = (S["une"] + S["emp"]).sum(axis=(2, 3, 4)).astype(float)
    return 100.0 * U / L, 100.0 * U.sum(1) / L.sum(1), U / 6.0, L / 6.0


def tune(U, q4rows, rounds=6):
    """the regional levels that put each region's 2026 rate (the mean of its twelve published monthly rates) on its
    target"""
    target = np.array([W.TARGET26[c] for c in W.RCODE])
    level = target - 0.5
    for _ in range(rounds):
        S = collect(level, U, q4rows)
        reg = published(S)[0]
        level = level + (target - np.round(reg[W.Y26:], 1).mean(0))
    for _ in range(6):            # no region's 2026 average left on a two-decimal rounding edge
        avg = np.round(published(collect(level, U, q4rows))[0][W.Y26:], 1).mean(0)
        edge = np.abs((avg * 100) % 1 - 0.5) < 0.15
        if not edge.any():
            break
        level = level + 0.01 * edge
    return level


def simulate():
    U = uniforms()
    q4 = fieldwork_q4()
    level = tune(U, q4)
    S = collect(level, U, q4)
    S["q4"] = q4
    S["level"] = level
    return S
