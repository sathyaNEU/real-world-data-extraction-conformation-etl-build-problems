"""The callback model and its family. Each sampled member is in one of two classes (worked for pay 80 hours or more in
March 2026, or not); each call reaches the member with a chance that depends on the class and on when the call is
made; a member reached completes the interview or declines, the same chance in either class. The class is known for
members interviewed and for members who declined but answered the key question, and inferred for the rest from their
call histories. Estimated by EM."""
import numpy as np

COMBOS = ["msc_day", "vendor_day", "vendor_evening", "vendor_saturday"]


def summarise(hist):
    """hist: per case (region index, age band, sex, class or -1 when unknown, outcome, [(combo, attempt), ...] calls up
    to and including the reaching call). Returns arrays for the EM: failed calls by combo, the reaching combo (or -1),
    outcome codes (1 complete, 2 declined, 0 never reached), class, region, age band, sex and the per-call rows."""
    N = len(hist)
    F = np.zeros((N, 4))
    hit = np.full(N, -1)
    out = np.zeros(N, int)
    y = np.full(N, -1)
    reg = np.zeros(N, int)
    age = np.zeros(N, int)
    sex = np.zeros(N, int)
    rows = []
    for i, (r, a, s, cls, o, calls) in enumerate(hist):
        reg[i], age[i], sex[i], out[i] = r, a, s, o
        y[i] = cls
        for j, (c, k) in enumerate(calls):
            last = j == len(calls) - 1
            if last and o in (1, 2):
                hit[i] = c
            else:
                F[i, c] += 1
            rows.append((i, c, k, int(last and o in (1, 2))))
    return dict(F=F, hit=hit, out=out, y=y, reg=reg, age=age, sex=sex, rows=np.array(rows), N=N)


def em(S, contact="window", rate_by="pooled", share_by="region", refusal="informative", n_regions=10,
       iters=20000, tol=1e-12):
    """contact: window (day, evening, Saturday), centre (member services day, vendor day, evening, Saturday) or none;
    rate_by: pooled or region; share_by: region or cell (region by age band by sex); refusal: informative (a declining
    member's call history counts) or flat (a declining member carries the region's share). Returns each region's
    estimated share, the answer rates and the iterations used."""
    F, hit, out, y, reg = S["F"], S["hit"], S["out"], S["y"], S["reg"]
    N = S["N"]
    cmap = {"window": np.array([0, 0, 1, 2]), "centre": np.array([0, 1, 2, 3]), "none": np.array([0, 0, 0, 0])}[contact]
    J = cmap.max() + 1
    Fj = np.zeros((N, J))
    for c in range(4):
        Fj[:, cmap[c]] += F[:, c]
    hj = np.where(hit >= 0, cmap[np.maximum(hit, 0)], -1)
    G = n_regions if rate_by == "region" else 1
    g = reg if rate_by == "region" else np.zeros(N, int)
    cell = reg if share_by == "region" else reg * 6 + S["age"] * 2 + S["sex"]
    C = int(cell.max()) + 1
    comp, ref = out == 1, out == 2
    known = y >= 0
    pi = np.full(C, 0.5)
    p = np.zeros((G, 2, J))
    p[:, 0, :], p[:, 1, :] = 0.35, 0.15
    hh = hj >= 0
    w = np.where(known, y, 0.5).astype(float)
    rho = np.array([0.1, 0.1])
    contacted = comp | ref
    for it in range(iters):
        ll = np.zeros((N, 2))
        for k in (0, 1):
            pk = p[g, k, :]
            ll[:, k] = (Fj * np.log(1 - pk)).sum(1)
            ll[hh, k] += np.log(pk[hh, hj[hh]])
        pc = pi[cell]
        a1 = np.log(pc) + ll[:, 1]
        a0 = np.log(1 - pc) + ll[:, 0]
        if refusal == "by_class":
            a1 = a1 + np.where(ref, np.log(rho[1]), 0.0)
            a0 = a0 + np.where(ref, np.log(rho[0]), 0.0)
        post = 1 / (1 + np.exp(a0 - a1))
        if refusal == "flat":
            post = np.where(ref, pc, post)
        w = np.where(known, y, post)
        pi_new = np.bincount(cell, weights=w, minlength=C) / np.bincount(cell, minlength=C)
        p_new = np.zeros_like(p)
        for gg in range(G):
            m = g == gg
            if refusal == "flat":
                m = m & ~(ref & ~known)   # a declining member's calls carry no class information under this variant
            for k, wk in ((1, w), (0, 1 - w)):
                for j in range(J):
                    s = (wk[m] * (hj[m] == j)).sum()
                    t = s + (wk[m] * Fj[m, j]).sum()
                    p_new[gg, k, j] = s / t if t > 0 else 0.5
        if refusal == "by_class":
            rho = np.array([((1 - w) * ref).sum() / ((1 - w) * contacted).sum(), (w * ref).sum() / (w * contacted).sum()])
        d = max(np.abs(pi_new - pi).max(), np.abs(p_new - p).max())
        pi, p = pi_new, p_new
        if d < tol:
            break
    share = np.bincount(reg, weights=w, minlength=n_regions) / np.bincount(reg, minlength=n_regions)
    return share, p, it


def em_attempt(S, n_regions=10, iters=400, tol=1e-10):
    """The window model with an attempt-number effect shared by the classes (logit of the chance a call reaches the
    member = class-by-window level + attempt term, attempts 1 to 9). EM with a weighted logistic M-step."""
    import statsmodels.api as sm
    rows = S["rows"]                      # case, combo, attempt, reached
    out, y, reg = S["out"], S["y"], S["reg"]
    known = y >= 0
    win = np.array([0, 0, 1, 2])[rows[:, 1].astype(int)]
    att = np.clip(rows[:, 2].astype(int), 1, 9)
    hitr = rows[:, 3].astype(float)
    case = rows[:, 0].astype(int)
    n = len(rows)
    # design: class-by-window dummies (6) and attempt dummies 2..9 (8)
    Xw = np.zeros((n, 3))
    Xw[np.arange(n), win] = 1
    Xa = np.zeros((n, 8))
    for k in range(2, 10):
        Xa[att == k, k - 2] = 1
    X = np.vstack([np.hstack([Xw, np.zeros((n, 3)), Xa]), np.hstack([np.zeros((n, 3)), Xw, Xa])])
    Y = np.concatenate([hitr, hitr])
    pi = np.full(n_regions, 0.5)
    beta = np.zeros(14)
    beta[:6] = np.log(np.array([0.35, 0.35, 0.35, 0.15, 0.15, 0.15]) / (1 - np.array([0.35, 0.35, 0.35, 0.15, 0.15, 0.15])))
    w = np.where(known, y, 0.5).astype(float)
    for it in range(iters):
        eta = X @ beta
        pr = 1 / (1 + np.exp(-eta))
        lc = Y * np.log(pr) + (1 - Y) * np.log(1 - pr)
        l0 = np.bincount(case, weights=lc[:n], minlength=S["N"])
        l1 = np.bincount(case, weights=lc[n:], minlength=S["N"])
        pc = pi[reg]
        post = 1 / (1 + np.exp((np.log(1 - pc) + l0) - (np.log(pc) + l1)))
        w = np.where(known, y, post)
        pi_new = np.bincount(reg, weights=w, minlength=n_regions) / np.bincount(reg, minlength=n_regions)
        wt = np.concatenate([1 - w[case], w[case]])
        fit = sm.GLM(Y, X, family=sm.families.Binomial(), freq_weights=wt).fit(start_params=beta)
        d = max(np.abs(pi_new - pi).max(), np.abs(fit.params - beta).max())
        pi, beta = pi_new, fit.params
        if d < tol:
            break
    share = np.bincount(reg, weights=w, minlength=n_regions) / np.bincount(reg, minlength=n_regions)
    return share, beta, it


FAMILY = {
    "window, pooled (the golden)": dict(),
    "window, by region": dict(rate_by="region"),
    "centre and window, pooled": dict(contact="centre"),
    "window, pooled, shares by age band and sex": dict(share_by="cell"),
    "window, pooled, declining by class": dict(refusal="by_class"),
}
