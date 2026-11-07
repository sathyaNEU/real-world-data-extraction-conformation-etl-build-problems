"""Prototype 4: septicemia (871/872, two-level) as the target family. U codes metabolic encephalopathy where it is
the claim's only MCC; C is a genuine twin (an older, nursing-home population, more encephalopathy everywhere); A is
sicker through transfers; B carries a chronic lung burden no claim field records. Vectorised per cell."""
import sys, collections
import numpy as np

FAMS = {  # family: (three-level?, weights MCC/CC/none, MCC multiplier, share of volume)
    "SEPS": (False, (1.88, 1.04, 1.04), 1.5, 0.20),
    "UTI": (False, (1.09, 0.79, 0.79), 0.8, 0.15),
    "HF": (True, (1.32, 0.90, 0.64), 1.0, 0.21),
    "PNEU": (True, (1.29, 0.88, 0.69), 0.9, 0.18),
    "COPD": (True, (1.17, 0.83, 0.68), 0.8, 0.14),
    "GIB": (True, (1.60, 0.95, 0.66), 0.8, 0.12),
}
FL = list(FAMS)
# MCC codes: base prevalence, loading on general burden zg, on lung burden zr, on cognitive burden zc
MCC = {"J96.01": (0.045, 0.7, 1.0, 0.0), "N17.0": (0.018, 0.8, 0.0, 0.0), "I21.4": (0.028, 0.6, 0.0, 0.0),
       "E43": (0.020, 0.9, 0.0, 0.2), "G93.41": (0.040, 0.8, 0.0, 1.0), "J69.0": (0.018, 0.7, 0.2, 0.5),
       "I26.99": (0.010, 0.4, 0.0, 0.0), "R65.20": (0.050, 0.9, 0.0, 0.0), "L89.154": (0.008, 0.9, 0.0, 0.4)}
CODES = list(MCC)
GI = CODES.index("G93.41")


def logit(p):
    return np.log(p / (1 - p))


def world(seed, u_seps=0.11, u_uti=0.06, mu_u=-0.25):
    rng = np.random.default_rng(seed)
    H = 20
    mu = rng.normal(0, 0.14, H); resp = rng.normal(0, 0.10, H); cog = rng.normal(0, 0.10, H)
    vol = rng.lognormal(np.log(2300), 0.45, H)
    tr = np.full(H, 0.04)
    hospice = rng.uniform(0.02, 0.06, H)
    A, B, U, C, F = 0, 1, 2, 3, 4
    mu[A], vol[A], tr[A] = 0.30, 5600, 0.20
    mu[B], resp[B], vol[B] = 0.10, 0.85, 3400
    mu[U], vol[U] = mu_u, 3900
    mu[C], cog[C], vol[C] = 0.05, 0.70, 3200
    hospice[F] = 0.22
    cells = {}
    for h in range(H):
        for f, (three, w, mult, share) in FAMS.items():
            n = rng.poisson(vol[h] * share)
            transfer = rng.random(n) < tr[h]
            age = np.clip(rng.normal(76 + 3 * (h == C), 7.5, n), 65, 101)
            dual = rng.random(n) < 0.18
            prior = rng.poisson(0.6, n)
            zg = mu[h] + rng.normal(0, 1, n) + 0.9 * transfer + 0.02 * (age - 76) + 0.12 * prior
            zr = resp[h] + 0.3 * rng.normal(0, 1, n)
            zc = cog[h] + 0.4 * rng.normal(0, 1, n) + 0.015 * (age - 76)
            P = np.zeros((n, len(CODES)), bool)
            for j, (k, (p, bg, br, bc)) in enumerate(MCC.items()):
                pr = 1 / (1 + np.exp(-(logit(min(0.5, p * mult)) + bg * zg + br * zr + bc * zc)))
                P[:, j] = rng.random(n) < pr
            anycc = rng.random(n) < 1 / (1 + np.exp(-(0.4 + 0.6 * zg)))
            los = np.maximum(1, np.round(rng.lognormal(np.log(3.8) + 0.16 * zg + 0.05 * P.sum(1), 0.45))).astype(int)
            died = rng.random(n) < 1 / (1 + np.exp(-(-3.2 + 0.7 * zg + 0.35 * P.sum(1))))
            to_hospice = (~died) & (rng.random(n) < hospice[h] * (1 + zg.clip(0)))
            died = died & ~(rng.random(n) < hospice[h] * 2.5)  # hospices take dying patients before death
            added = np.zeros(n, bool)
            if h == U and f in ("SEPS", "UTI"):
                u = u_seps if f == "SEPS" else u_uti
                other = P[:, [j for j in range(len(CODES)) if j != GI]].any(1)
                pr_add = u * np.where(los >= 4, 1.35, 0.45)
                added = (~other) & (~P[:, GI]) & (rng.random(n) < pr_add)
                P[:, GI] |= added
            cells[(h, f)] = dict(P=P, anycc=anycc, los=los, died=died, transfer=transfer, age=age, dual=dual,
                                 prior=prior, added=added, hospice=to_hospice)
    return cells


def drop(f, cc):
    three, w, _, _ = FAMS[f]
    return w[0] - (w[1] if (three and cc) else w[2])


def routes(cells):
    out = {}
    # R0 unadjusted
    r0 = {}
    for f in FL:
        allP = np.concatenate([cells[(h, g)]["P"] for (h, g) in cells if g == f])
        rate = allP.any(1).mean()
        for (h, g), c in cells.items():
            if g != f:
                continue
            n = len(c["los"]); obs = c["P"].any(1).sum()
            d = np.mean([drop(f, x) for x in c["anycc"]]) if n else 0
            r0[(h, f)] = (obs - rate * n) * d
    out["R0"] = sorted(r0, key=r0.get, reverse=True)[:3]
    # R1 risk adjusted on visible covariates
    import statsmodels.api as sm
    r1 = {}
    for f in FL:
        keys = [k for k in cells if k[1] == f]
        X = np.concatenate([np.column_stack([np.ones(len(cells[k]["los"])), cells[k]["transfer"],
                                             (cells[k]["age"] - 76) / 10, cells[k]["dual"], cells[k]["prior"],
                                             cells[k]["anycc"]]) for k in keys]).astype(float)
        y = np.concatenate([cells[k]["P"].any(1) for k in keys]).astype(float)
        m = sm.Logit(y, X).fit(disp=0)
        p = m.predict(X)
        i = 0
        for k in keys:
            n = len(cells[k]["los"])
            o = y[i:i + n].sum(); e = p[i:i + n].sum(); i += n
            d = np.mean([drop(f, x) for x in cells[k]["anycc"]]) if n else 0
            r1[k] = (o - e) * d
    out["R1"] = sorted(r1, key=r1.get, reverse=True)[:3]
    # R2 code-level risk adjusted excess
    r2 = {}
    for f in FL:
        keys = [k for k in cells if k[1] == f]
        X = np.concatenate([np.column_stack([np.ones(len(cells[k]["los"])), cells[k]["transfer"],
                                             (cells[k]["age"] - 76) / 10, cells[k]["dual"], cells[k]["prior"],
                                             cells[k]["anycc"]]) for k in keys]).astype(float)
        for j, code in enumerate(CODES):
            y = np.concatenate([cells[k]["P"][:, j] for k in keys]).astype(float)
            m = sm.Logit(y, X).fit(disp=0)
            p = m.predict(X)
            i = 0
            for k in keys:
                n = len(cells[k]["los"])
                o = y[i:i + n].sum(); e = p[i:i + n].sum(); i += n
                d = np.mean([drop(f, x) for x in cells[k]["anycc"]]) if n else 0
                r2[(k[0], f, code)] = (o - e) * d
    out["R2"] = sorted(r2, key=r2.get, reverse=True)[:3]
    # R2c outcome validation: lowest in-hospital mortality among the code's claims, for the code with largest excess
    # R3 footprint
    r3 = {}
    for f in FL:
        keys = [k for k in cells if k[1] == f]
        for j, code in enumerate(CODES):
            st = {}
            for k in keys:
                P = cells[k]["P"]
                other = P[:, [x for x in range(len(CODES)) if x != j]].any(1)
                st[k] = ((~other).sum(), (P[:, j] & ~other).sum(), other.sum(), (P[:, j] & other).sum())
            for k in keys:
                oth = [st[g] for g in keys if g != k]
                N0 = sum(o[0] for o in oth); C0 = sum(o[1] for o in oth); N1 = sum(o[2] for o in oth); C1 = sum(o[3] for o in oth)
                n0, c0, n1, c1 = st[k]
                if C1 == 0 or n1 == 0 or C0 == 0:
                    continue
                rho = (C0 / N0) / (C1 / N1)
                exp0 = n0 * rho * (c1 / n1)
                P = cells[k]["P"]; other = P[:, [x for x in range(len(CODES)) if x != j]].any(1)
                sel = P[:, j] & ~other
                d = np.mean([drop(f, x) for x in cells[k]["anycc"][sel]]) if sel.any() else 0
                r3[(k[0], f, code)] = (c0 - exp0) * d
    out["R3"] = sorted(r3, key=r3.get, reverse=True)[:3]
    out["R3v"] = [round(r3[k], 1) for k in out["R3"]]
    return out, r0, r1, r2, r3


def estimators(cells, U=2, f="SEPS", code="G93.41"):
    j = CODES.index(code)
    keys = [k for k in cells if k[1] == f]
    st = {}
    for k in keys:
        P = cells[k]["P"]; other = P[:, [x for x in range(len(CODES)) if x != j]].any(1)
        st[k] = ((~other).sum(), (P[:, j] & ~other).sum(), other.sum(), (P[:, j] & other).sum())
    oth = [st[g] for g in keys if g[0] != U]
    N0 = sum(o[0] for o in oth); C0 = sum(o[1] for o in oth); N1 = sum(o[2] for o in oth); C1 = sum(o[3] for o in oth)
    n0, c0, n1, c1 = st[(U, f)]
    a = c0 - n0 * (C0 / N0) / (C1 / N1) * (c1 / n1)
    b = c0 - n0 * (C0 / N0)
    ratios = [(o[1] / o[0]) / (o[3] / o[2]) for o in oth if o[1] > 0 and o[3] > 0]
    c = c0 - n0 * np.median(ratios) * (c1 / n1)
    # logit with hospital fixed effects and an other-MCC term; the U x decisive cell set to zero
    import statsmodels.api as sm
    rows_X, rows_y, sel = [], [], []
    hs = sorted(set(k[0] for k in keys))
    for k in keys:
        P = cells[k]["P"]; other = P[:, [x for x in range(len(CODES)) if x != j]].any(1)
        n = len(other)
        fe = np.zeros((n, len(hs) - 1)); idx = hs.index(k[0])
        if idx > 0:
            fe[:, idx - 1] = 1
        inter = ((k[0] == U) & ~other).astype(float)
        rows_X.append(np.column_stack([np.ones(n), other.astype(float), fe, inter]))
        rows_y.append(P[:, j].astype(float)); sel.append((k[0] == U) & ~other)
    X = np.concatenate(rows_X); y = np.concatenate(rows_y); s = np.concatenate(sel)
    m = sm.Logit(y, X).fit(disp=0)
    Xc = X.copy(); Xc[:, -1] = 0
    d = y[s].sum() - m.predict(Xc[s]).sum()
    truth = cells[(U, f)]["added"].sum()
    return truth, a, b, c, d, st[(U, f)]


if __name__ == "__main__":
    n = int(sys.argv[1])
    args = [float(x) for x in sys.argv[2:]]
    tal = collections.defaultdict(collections.Counter)
    for s in range(n):
        cells = world(5000 + s, *args)
        out, r0, r1, r2, r3 = routes(cells)
        tr, a, b, c, d, st = estimators(cells)
        print(s, "R0", out["R0"][0], "R1", out["R1"][0], "R2", out["R2"][0], "R3", out["R3"][:2], out["R3v"][:2],
              "truth", tr, "a %.1f b %.1f c %.1f d %.1f" % (a, b, c, d), st)
        for k in ("R0", "R1", "R2", "R3"):
            tal[k][str(out[k][0][:2])] += 1
    for k, cc in tal.items():
        print(k, dict(cc))
