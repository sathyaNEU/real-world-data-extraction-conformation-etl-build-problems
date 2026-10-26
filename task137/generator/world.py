"""The world at day grain, before any record is written: latent demand by referrer group and practice, the clinic's
staffing and ticket allocation, which days ran out, and who was turned away. Practices with their own phlebotomy
clinic book their patients in-house for weeks after the walk-in clinic has kept running out: each week's run-out share
holds their referrals down for the eight weeks that follow."""
import datetime as dt
import numpy as np
import params as P

WD = np.array([1.21, 1.05, 1.00, 0.96, 0.85])
MON = np.array([1.05, 1.04, 1.02, 1.00, 1.00, 0.96, 0.92, 0.85, 0.97, 1.03, 1.05, 0.89])


def clinic_days(a=P.START, b=P.END):
    out, d = [], a
    while d <= b:
        if d.weekday() < 5 and d not in P.BH:
            out.append(d)
        d += dt.timedelta(1)
    return out


def fy(d):
    return d.year - (d.month < 4)


def simulate(seed=P.SEED, K=P.K_DETER, dseed=P.DEMAND_SEED, weeks=P.DETER_WEEKS):
    rs = np.random.default_rng([seed, 1])     # staffing
    rd = np.random.default_rng([dseed, 2])    # demand
    days = clinic_days()
    n = len(days)
    t = np.array([(x - P.START).days / 365.25 for x in days])
    cal = np.array([WD[x.weekday()] * MON[x.month - 1] for x in days]) * (1 + P.GROWTH) ** t
    pbh = np.zeros(n, bool)
    for i in range(1, n):
        if (days[i] - days[i - 1]).days not in (1, 3):
            pbh[i] = True
    cal[pbh] *= 1.17
    lam = {g: P.BASE_DAILY * s * cal for g, s in P.SHARES.items()}
    # hospital programmes add visits on their specialty's clinic weekdays and the day after
    spec_days = {s[0]: s[1] for s in P.SPECIALTIES}
    prog = np.zeros(n)
    prog_spec = [dict() for _ in range(n)]
    for sp, a, b, v in P.PROGRAMMES:
        for i, x in enumerate(days):
            if a <= x <= b:
                w = 1.0 if x.weekday() in spec_days[sp] else 0.55
                add = v * w * WD[x.weekday()] / 1.03
                prog[i] += add
                prog_spec[i][sp] = prog_spec[i].get(sp, 0.0) + add
    lamH2 = lam["H"] + prog
    # staffing: short sickness, long-term sickness, annual leave, the vacancy and bank cover
    status = np.full((n, P.POSTS), "CLIN", dtype=object)
    for p in range(P.POSTS):
        i = 0
        while i < n:
            if rs.random() < 0.0010:
                L = int(rs.choice([3, 5, 5, 8, 10]))
                status[i:i + L, p] = "SICK"
                i += L
            else:
                if rs.random() < 0.010:
                    status[i, p] = "SICK"
                i += 1
    lts = np.zeros((n, P.POSTS), bool)
    for p, a, b in P.LONG_TERM_SICK:
        for i, x in enumerate(days):
            if a <= x <= b:
                status[i, p] = "SICK"
                lts[i, p] = True
    for i, x in enumerate(days):
        pal = 0.07 if x.month in (7, 8) else (0.04 if x.month in (4, 10, 12, 2) else 0.022)
        for p in range(P.POSTS):
            if status[i, p] == "CLIN" and rs.random() < pal:
                status[i, p] = "AL"
    vac = np.array([P.VACANCY[0] <= x <= P.VACANCY[1] for x in days])
    status[vac, P.POSTS - 1] = "VAC"
    worked = (status == "CLIN").sum(axis=1)
    nlts = lts.sum(axis=1)
    short = P.POSTS - worked - vac.astype(int) - nlts
    # the bank office backfills the vacant line and long-term sickness lines on most days
    vbank = np.array([(1 if (vac[i] and rs.random() < 0.85) else 0) + sum(1 for _ in range(int(nlts[i])) if rs.random() < 0.9)
                      for i in range(n)])
    obank = np.array([min(s, rs.binomial(s, 0.5)) if s >= 1 else 0 for s in short])
    bank = vbank + obank
    adj = rs.choice([0, 0, 0, 0, 5, -5], size=n)
    alloc = (worked * P.PER_HEAD + bank * P.BANK_HEAD + adj).astype(int)
    # demand, run-outs and the turned away
    wk = np.array([x - dt.timedelta(x.weekday()) for x in days])
    A = {g: np.zeros(n, int) for g in "PNH"}
    seen = {g: np.zeros(n, int) for g in "PNH"}
    away = {g: np.zeros(n, int) for g in "PNH"}
    ro = np.zeros(n, bool)
    E = np.zeros(n)
    wk_ro = {}
    for i in range(n):
        sh = [wk_ro.get(wk[i] - dt.timedelta(7 * k), (0, 0)) for k in range(1, weeks + 1)]
        E[i] = sum(r / c if c else 0.0 for r, c in sh) / weeks
        mus = {"P": lam["P"][i] * np.exp(-K * E[i]), "N": lam["N"][i], "H": lamH2[i]}
        for g in "PNH":
            A[g][i] = int(rd.poisson(rd.gamma(P.SHAPE, mus[g] / P.SHAPE)))
        tot = A["P"][i] + A["N"][i] + A["H"][i]
        if tot > alloc[i]:
            ro[i] = True
            ex = tot - alloc[i]
            w = np.array([A["P"][i], A["N"][i], A["H"][i] * 1.3], float)
            aw = rd.multinomial(ex, w / w.sum())
            cap = np.array([A["P"][i], A["N"][i], A["H"][i]])
            aw = np.minimum(aw, cap)
            j = 0
            while aw.sum() < ex:
                if aw[j % 3] < cap[j % 3]:
                    aw[j % 3] += 1
                j += 1
            for k, g in enumerate("PNH"):
                away[g][i] = int(aw[k])
                seen[g][i] = A[g][i] - int(aw[k])
        else:
            for g in "PNH":
                seen[g][i] = A[g][i]
        r0, c0 = wk_ro.get(wk[i], (0, 0))
        wk_ro[wk[i]] = (r0 + int(ro[i]), c0 + 1)
    return dict(days=days, n=n, t=t, pbh=pbh, lam=lam, lamH2=lamH2, prog=prog, prog_spec=prog_spec, status=status,
                lts=lts, vac=vac, bank=bank, vbank=vbank, worked=worked, alloc=alloc, wk=wk, A=A, seen=seen, away=away,
                ro=ro, E=E, K=K)


def truth(W):
    """Latent GP-referred demand by financial year: what a clinic that never ran out would have seen."""
    out = {}
    for i, x in enumerate(W["days"]):
        f = fy(x)
        out[f] = out.get(f, 0.0) + W["lam"]["P"][i] + W["lam"]["N"][i]
    return out
