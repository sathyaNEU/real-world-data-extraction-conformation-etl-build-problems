"""Prototype 2: a clean-truth world of hospitals x MS-DRG families, honest severity coding driven by a latent
illness burden, one hospital adding one MCC only where it is the claim's only MCC. Every route a strong analyst
would take is run and scored over seeds."""
import sys
import numpy as np

FAMS = {  # family: (levels, weights by level MCC/CC/none, base MCC-code multiplier, volume share)
    "HF": (3, (1.34, 0.91, 0.66), 1.0, 0.22),
    "PNEU": (3, (1.30, 0.89, 0.70), 0.9, 0.20),
    "COPD": (3, (1.18, 0.84, 0.69), 0.8, 0.14),
    "UTI": (2, (1.07, 0.78, 0.78), 0.9, 0.16),
    "SEPS": (2, (1.86, 1.03, 1.03), 1.6, 0.16),
    "GIB": (3, (1.62, 0.96, 0.66), 0.8, 0.12),
}
MCC = {  # code: (base prevalence at z=0, loading on general burden, loading on respiratory burden)
    "J96.01": (0.050, 0.7, 1.0), "N17.0": (0.018, 0.8, 0.0), "I21.4": (0.030, 0.6, 0.0),
    "E43": (0.020, 0.9, 0.0), "G93.41": (0.035, 0.8, 0.0), "J69.0": (0.018, 0.7, 0.2),
    "I26.99": (0.010, 0.4, 0.0), "A41.9": (0.025, 0.8, 0.0), "L89.154": (0.008, 0.9, 0.0),
}
CC = {"N17.9": (0.10, 0.6), "E87.1": (0.12, 0.5), "J18.9": (0.08, 0.5), "N18.4": (0.06, 0.6),
      "E44.0": (0.05, 0.6), "D62": (0.05, 0.4), "N39.0": (0.07, 0.4), "J44.1": (0.08, 0.3)}
CODES = list(MCC)


def logit(p):
    return np.log(p / (1 - p))


def world(seed, u_main=0.050, u_second=0.030):
    rng = np.random.default_rng(seed)
    H = 20
    hosp = [f"H{i:02d}" for i in range(H)]
    mu = rng.normal(0, 0.15, H)
    resp = rng.normal(0, 0.10, H)
    vol = rng.lognormal(np.log(2200), 0.45, H)
    # roles
    A, B, U, D, E = 0, 1, 2, 3, 4
    mu[A], vol[A] = 0.62, 5200      # academic centre: sicker, part of it through transfers
    mu[B], resp[B], vol[B] = 0.22, 0.75, 3300  # regional hospital, heavy chronic lung disease burden
    mu[U], vol[U] = 0.12, 3600      # the hospital whose coding follows the payment
    mu[D], vol[D] = -0.85, 1200     # small rural, low acuity
    mu[E], vol[E] = 0.05, 2500      # own skilled nursing unit, early discharges
    rows = []
    for h in range(H):
        for f, (lev, w, mult, share) in FAMS.items():
            n = rng.poisson(vol[h] * share)
            transfer = rng.random(n) < (0.16 if h == A else 0.04)
            age = np.clip(rng.normal(77 + (2 if h == D else 0), 7.5, n), 65, 101)
            dual = rng.random(n) < 0.18
            prior = rng.poisson(0.6 + 0.4 * (h == A), n)
            zg = mu[h] + rng.normal(0, 1, n) + 0.55 * transfer + 0.02 * (age - 77) + 0.12 * prior
            zr = resp[h] + 0.3 * rng.normal(0, 1, n)
            pres = {}
            for k, (p, bg, br) in MCC.items():
                base = logit(min(0.5, p * mult))
                pr = 1 / (1 + np.exp(-(base + bg * zg + br * zr)))
                pres[k] = rng.random(n) < pr
            ccs = {}
            for k, (p, bg) in CC.items():
                pr = 1 / (1 + np.exp(-(logit(p) + bg * zg)))
                ccs[k] = rng.random(n) < pr
            anycc = np.zeros(n, bool)
            for k in CC:
                anycc |= ccs[k]
            los = np.maximum(1, np.round(rng.lognormal(np.log(3.6) + 0.18 * zg, 0.45))).astype(int)
            added = np.zeros(n, bool)
            if h == U and f in ("HF", "PNEU"):
                cstar = "E43" if f == "HF" else "G93.41"
                u = u_main if f == "HF" else u_second
                other = np.zeros(n, bool)
                for k in CODES:
                    if k != cstar:
                        other |= pres[k]
                pr_add = u * np.where(los >= 3, 1.25, 0.55)
                added = (~other) & (~pres[cstar]) & (rng.random(n) < pr_add)
                pres[cstar] = pres[cstar] | added
            if h == E:
                los = np.maximum(1, los - (rng.random(n) < 0.5) * np.round(0.35 * los).astype(int))
            for i in range(n):
                codes = [k for k in CODES if pres[k][i]]
                rows.append((h, f, codes, bool(anycc[i]), int(los[i]), bool(transfer[i]), float(age[i]),
                             bool(dual[i]), int(prior[i]), bool(added[i])))
    return hosp, rows


def drop(f, has_cc):
    lev, w, _, _ = FAMS[f]
    return w[0] - (w[1] if (has_cc and lev == 3) else w[2])


def analyse(rows):
    import collections
    by = collections.defaultdict(list)
    for r in rows:
        by[(r[0], r[1])].append(r)
    # network rates
    net_mcc = {f: np.mean([len(r[2]) > 0 for r in rows if r[1] == f]) for f in FAMS}
    res = {}
    # R0: excess MCC claims over the network rate, priced
    r0 = {}
    for (h, f), rs in by.items():
        n = len(rs)
        obs = sum(len(r[2]) > 0 for r in rs)
        avg_drop = np.mean([drop(f, r[3]) for r in rs])
        r0[(h, f)] = (obs - n * net_mcc[f]) * avg_drop
    res["R0"] = max(r0, key=r0.get)
    # R1: risk adjusted by the claim's observed covariates (transfer, age, dual, prior, any CC)
    import statsmodels.api as sm
    r1 = {}
    for f in FAMS:
        rs = [r for r in rows if r[1] == f]
        X = np.array([[1, r[5], (r[6] - 77) / 10, r[7], r[8], r[3]] for r in rs], float)
        y = np.array([len(r[2]) > 0 for r in rs], float)
        m = sm.Logit(y, X).fit(disp=0)
        p = m.predict(X)
        acc = collections.defaultdict(lambda: [0.0, 0.0, 0.0])
        for r, pi, yi in zip(rs, p, y):
            a = acc[r[0]]
            a[0] += yi; a[1] += pi; a[2] += drop(f, r[3])
        for h, (o, e, dsum) in acc.items():
            n = sum(1 for r in rs if r[0] == h)
            r1[(h, f)] = (o - e) * dsum / n
    res["R1"] = max(r1, key=r1.get)
    # R1b: code-level excess over the network's code rate, priced at the family drop
    r1b = {}
    for f in FAMS:
        rs = [r for r in rows if r[1] == f]
        for k in CODES:
            rate = np.mean([k in r[2] for r in rs])
            for h in set(r[0] for r in rs):
                hs = [r for r in rs if r[0] == h]
                r1b[(h, f, k)] = (sum(k in r[2] for r in hs) - rate * len(hs)) * np.mean([drop(f, r[3]) for r in hs])
    res["R1b"] = max(r1b, key=r1b.get)
    # R2: LOS gradient, lowest ratio of MCC to non-MCC mean LOS among cells with 100+ claims
    r2 = {}
    for (h, f), rs in by.items():
        if len(rs) < 100:
            continue
        lm = [r[4] for r in rs if r[2]]
        ln = [r[4] for r in rs if not r[2]]
        if len(lm) > 20 and len(ln) > 20:
            r2[(h, f)] = np.mean(lm) / np.mean(ln)
    res["R2"] = min(r2, key=r2.get)
    # R2b: share of MCC claims carrying exactly one MCC
    r2b = {}
    for (h, f), rs in by.items():
        m = [r for r in rs if r[2]]
        if len(m) >= 40:
            r2b[(h, f)] = np.mean([len(r[2]) == 1 for r in m])
    res["R2b"] = max(r2b, key=r2b.get)
    # R3: the footprint. For each family and code, the honest ratio of the code's rate where it is the only MCC
    # candidate (no other MCC) to its rate beside another MCC, pooled over every other hospital; each cell's
    # excess where it decides the DRG is its observed count less N0 x ratio x its own rate beside others.
    r3 = {}
    for f in FAMS:
        rs = [r for r in rows if r[1] == f]
        hs_all = sorted(set(r[0] for r in rs))
        for k in CODES:
            def strata(sub):
                n0 = sum(1 for r in sub if not any(c != k for c in r[2]))
                c0 = sum(1 for r in sub if k in r[2] and not any(c != k for c in r[2]))
                n1 = sum(1 for r in sub if any(c != k for c in r[2]))
                c1 = sum(1 for r in sub if k in r[2] and any(c != k for c in r[2]))
                return n0, c0, n1, c1
            st = {h: strata([r for r in rs if r[0] == h]) for h in hs_all}
            for h in hs_all:
                others = [st[g] for g in hs_all if g != h]
                N0 = sum(o[0] for o in others); C0 = sum(o[1] for o in others)
                N1 = sum(o[2] for o in others); C1 = sum(o[3] for o in others)
                if C1 == 0:
                    continue
                rho = (C0 / N0) / (C1 / N1)
                n0, c0, n1, c1 = st[h]
                if n1 == 0:
                    continue
                exp0 = n0 * rho * (c1 / n1)
                hs = [r for r in rs if r[0] == h and k in r[2] and not any(c != k for c in r[2])]
                d = np.mean([drop(f, r[3]) for r in hs]) if hs else 0
                r3[(h, f, k)] = (c0 - exp0) * d
    best = sorted(r3, key=r3.get, reverse=True)
    res["R3"] = best[0]
    res["R3_second"] = best[1]
    res["R3_margin"] = r3[best[0]] / r3[best[1]]
    res["R3_truth"] = None
    return res, r0, r1, r3


if __name__ == "__main__":
    seeds = range(int(sys.argv[1]) if len(sys.argv) > 1 else 6)
    import collections
    tally = collections.defaultdict(collections.Counter)
    for s in seeds:
        hosp, rows = world(1000 + s)
        res, r0, r1, r3 = analyse(rows)
        truth_added = sum(r[9] for r in rows if r[0] == 2 and r[1] == "HF")
        print(s, {k: v for k, v in res.items()}, "added HF", truth_added,
              "R3 est HF E43 at U", round(r3.get((2, "HF", "E43"), 0) / np.mean([drop("HF", True), drop("HF", False)]), 1))
        for k in ("R0", "R1", "R1b", "R2", "R2b", "R3"):
            tally[k][str(res[k][:2])] += 1
    for k, c in tally.items():
        print(k, dict(c))
