"""The world behind the pack: Fenmore's SBA 7(a) book month by month from October 2009 to September 2026.

Each business is financed on its own 7(a) loan to its own company. Most borrowers are single businesses; operators
run several units, each unit's company guaranteed by the same individuals, and the bank's loan authorization
cross-defaults every loan those guarantors stand behind. A business fails by a hazard of its own months on book, the
same for every business; when one fails the bank accelerates every active loan of its guarantor group. A failure is
either fast (the business closes and the loans are accelerated that month) or slow (30, 60 and 90 days past due, the
default at 90). Most delinquencies are transient. A defaulted group cures, pays off in liquidation or is charged off.
Loans pay off by a hazard of their own months on book. While SBA paid a loan's instalments under Section 1112 the loan
could not fall behind: a business that failed in those months closed, and its loans were accelerated. Operators bought
units in blocks and rarely added one, until rates came down in fiscal years 2025 and 2026."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as K

# ---------------------------------------------------------------------------------------------------- the process
SINGLES = {2010: 1140, 2011: 1230, 2012: 1320, 2013: 1400, 2014: 1470, 2015: 1550, 2016: 1620, 2017: 1680, 2018: 1740,
           2019: 1300, 2020: 1110, 2021: 1520, 2022: 1800, 2023: 1670, 2024: 1740, 2025: 1950, 2026: 2070}
OPERATORS = {2010: 60, 2011: 68, 2012: 75, 2013: 82, 2014: 90, 2015: 98, 2016: 105, 2017: 112, 2018: 120,
             2019: 750, 2020: 600, 2021: 1000, 2022: 315, 2023: 255, 2024: 270, 2025: 330, 2026: 300}
BLOCK = ([1, 2, 3, 4], [0.65, 0.22, 0.09, 0.04])                               # units an operator starts with
BLOCK_RELIEF = ([1, 2, 3, 4, 5], [0.40, 0.28, 0.17, 0.10, 0.05])                # relief-era operators bought larger blocks
ADD = {fy: 0.02 for fy in range(2010, 2027)}                                     # add-on units per operator-year
ADD.update({2021: 0.05, 2025: 0.06, 2026: 1.15})
ADD_SINGLE, ADD_MULTI = 0.35, 1.30                                               # by the operator's units in service
FAST = 0.90
CURE, PIF_LIQ = 0.06, 0.02
TRANSIENT, TO60 = 0.005, 0.30
AMOUNT_SCALE = {2019: 0.889, 2020: 0.873, 2021: 0.777}                              # average loan size by vintage
WORLD_KEY = "w13"


def h_bus(mob):
    """Monthly failure hazard of a business by its loan's months on book (months since disbursement)."""
    m = np.maximum(np.asarray(mob, float), 1.0)
    return 0.0042 * np.exp(-0.5 * ((np.log(m) - np.log(19.0)) / 0.62) ** 2) + 0.00015


def p_pay(mob):
    m = np.asarray(mob)
    return np.select([m <= 12, m <= 36, m <= 72], [0.0008, 0.0022, 0.0045], 0.0065)


# Section 1112 (CARES Act and Economic Aid Act) as the world applies it
CARES_ENACTED = dt.date(2020, 3, 27)
CARES_NEW_END = dt.date(2020, 9, 27)
EAA_NEW_START, EAA_NEW_END = dt.date(2021, 2, 1), dt.date(2021, 9, 30)
EAA_90_START = dt.date(2020, 12, 28)
APR20, FEB21, APR21, MAY21, SEP21 = K.m_of(dt.date(2020, 4, 1)), K.m_of(dt.date(2021, 2, 1)), \
    K.m_of(dt.date(2021, 4, 1)), K.m_of(dt.date(2021, 5, 1)), K.m_of(dt.date(2021, 9, 1))
EAA_CAP = 9000.0
HARD_HIT = ("61", "71", "72", "213", "315", "448", "451", "481", "485", "487", "511", "512", "515", "532", "812")

# NAICS (2017) codes the book lends to, weights for single businesses and for multi-unit operators
NAICS = [
    ("722511", 6, 14), ("722513", 7, 30), ("722515", 3, 7), ("721110", 3, 6), ("812112", 3, 6), ("812111", 2, 2),
    ("812320", 2, 1), ("713940", 2, 6), ("611691", 1, 4), ("624410", 3, 5), ("621210", 5, 3), ("621111", 3, 1),
    ("621340", 2, 2), ("541110", 2, 0), ("541211", 2, 0), ("541330", 2, 0), ("238220", 4, 0), ("238210", 3, 0),
    ("236118", 3, 0), ("811111", 4, 3), ("811121", 3, 2), ("811192", 1, 3), ("445110", 2, 1), ("445120", 3, 2),
    ("453910", 2, 1), ("484121", 4, 0), ("484110", 3, 0), ("423830", 2, 0), ("332710", 3, 0), ("311811", 2, 1),
    ("312120", 1, 0), ("561730", 3, 0), ("561720", 2, 1), ("531130", 2, 1), ("623110", 1, 0), ("624120", 2, 1),
    ("448140", 1, 0), ("451110", 1, 1), ("485310", 1, 0), ("532111", 1, 0), ("512131", 1, 0), ("713110", 1, 0),
]


def sba_paid_months(appr, fp_m, naics):
    """The instalment months SBA paid under Section 1112, as (first, last, capped, programme) windows: six months
    under the CARES Act, then three more from February 2021 (or after the first six, if later) and five more for the
    hardest-hit industries, ending by September 2021; six months for loans approved from February to September 2021."""
    hard = naics.startswith(HARD_HIT)
    w = []
    if appr < CARES_ENACTED or appr <= CARES_NEW_END:
        s = max(fp_m, APR20) if appr < CARES_ENACTED else fp_m
        w.append((s, s + 5, False, "cares"))
        s2 = max(FEB21, s + 6)
        if s2 <= SEP21:
            w.append((s2, min(s2 + 2, SEP21), True, "eaa"))
            if hard and s2 + 3 <= SEP21:
                w.append((s2 + 3, min(s2 + 7, SEP21), True, "eaa"))
    elif EAA_NEW_START <= appr <= EAA_NEW_END:
        w.append((fp_m, fp_m + 5, True, "eaa"))
    return w


class World:
    pass


def annuity(bal, rate, n):
    r = rate / 1200.0
    return np.where(n > 0, np.where(r > 0, bal * r / (1 - (1 + r) ** (-np.maximum(n, 1))), bal / np.maximum(n, 1)), 0.0)


def _mix(z):
    with np.errstate(over="ignore"):
        z = z + np.uint64(0x9E3779B97F4A7C15)
        z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
        z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
        return z ^ (z >> np.uint64(31))


def uniform(seed, gs, k, t, r):
    """A uniform keyed by a group's stable id, a unit index, a month and a purpose: the same draw whatever else the
    world holds."""
    with np.errstate(over="ignore"):
        key = ((np.asarray(gs, np.uint64) * np.uint64(64) + np.asarray(k, np.uint64)) * np.uint64(256) +
               np.uint64(t)) * np.uint64(16) + np.uint64(r)
        z = _mix(_mix(key ^ np.uint64(seed)))
    return (z >> np.uint64(11)).astype(np.float64) * (2.0 ** -53)


def simulate(world_key=None):
    world_key = world_key or WORLD_KEY
    seed = int.from_bytes(__import__("hashlib").blake2b(("%d|%s" % (K.SEED, world_key)).encode(), digest_size=8).digest(),
                          "big") & 0x7FFFFFFFFFFFFFFF
    # ---- arrivals: (approval date, group, kind) with kind 0 single business, 1 operator unit; each group has a
    # stable id (fiscal year, kind, order within the year) and its own stream for its attributes
    arrivals = []
    stable = []
    op_first_m = {}
    attr = {}
    g_naics = []
    ns = [x[0] for x in NAICS]
    w_s = np.array([x[1] for x in NAICS], float)
    w_o = np.array([x[2] for x in NAICS], float)
    fy_start = lambda fy: dt.date(fy - 1, 10, 1)
    for fy in range(2010, 2027):
        rf = K.rng(world_key, "arrivals", fy)
        days = (fy_start(fy + 1) - fy_start(fy)).days
        for j, d in enumerate(rf.integers(0, days, SINGLES[fy])):
            g = len(stable)
            stable.append(fy * 100000 + j)
            ra = attr[g] = K.rng(world_key, "attr", stable[g])
            g_naics.append(ns[ra.choice(len(ns), p=w_s / w_s.sum())])
            arrivals.append((fy_start(fy) + dt.timedelta(days=int(d)), g, 0))
        for j, d in enumerate(rf.integers(0, days, OPERATORS[fy])):
            g = len(stable)
            stable.append(fy * 100000 + 50000 + j)
            ra = attr[g] = K.rng(world_key, "attr", stable[g])
            g_naics.append(ns[ra.choice(len(ns), p=w_o / w_o.sum())])
            a = fy_start(fy) + dt.timedelta(days=int(d))
            bl = BLOCK_RELIEF if K.POOL_FY[0] <= fy <= K.POOL_FY[1] else BLOCK
            k = int(ra.choice(bl[0], p=bl[1]))
            for _ in range(k):
                arrivals.append((a, g, 1))
            op_first_m[g] = K.m_of(a)
    G = len(stable)
    g_stable = np.array(stable, np.int64)
    is_op = np.zeros(G, bool)
    op_m = np.full(G, 10 ** 6)
    for g, m in op_first_m.items():
        is_op[g] = True
        op_m[g] = m
    g_naics = np.array(g_naics, dtype=object)
    arrivals.sort(key=lambda x: (x[0], stable[x[1]]))
    by_month = {}
    for a, g, k in arrivals:
        by_month.setdefault(K.m_of(a), []).append((a, g, k))

    cap = 70000
    W = World()
    W.G = G
    W.g_stable = g_stable
    W.is_op = is_op
    W.g_naics = g_naics
    f = {}
    for name, dtp in (("gid", np.int32), ("kind", np.int8), ("appr_m", np.int32), ("disb_m", np.int32),
                      ("fp_m", np.int32), ("term", np.int32), ("amt", float), ("ug", float), ("var", bool),
                      ("spread", float), ("rate", float), ("due_day", np.int8), ("lag", np.int32)):
        f[name] = np.zeros(cap, dtp)
    appr_date = [None] * cap
    disb_date = [None] * cap
    naics = [None] * cap
    windows = [None] * cap
    st = np.zeros(cap, np.int8)              # 0 approved, 1 performing, 2 in default, 3 charged off, 4 paid, 5 matured
    bal = np.zeros(cap)
    pay = np.zeros(cap)
    nleft = np.zeros(cap, np.int32)
    slow_m = np.full(cap, -1, np.int32)      # month a slow failure began
    dq = np.zeros(cap, np.int8)              # transient delinquency stage last month
    def_m = np.full(cap, -1, np.int32)
    def_bal = np.zeros(cap)
    trig = np.zeros(cap, bool)
    first_def = np.full(cap, -1, np.int32)
    end_m = np.full(cap, -1, np.int32)
    g_dead = np.zeros(G, bool)
    g_res_m = np.full(G, -1, np.int32)
    g_out = np.zeros(G, np.int8)
    g_def_m = np.full(G, -1, np.int32)
    n = 0
    rec = []
    events = []                              # (loan, month, kind) kind: 'default', 'trigger', 'cure', 'co', 'pif', 'mat'
    KMAX = 64
    k_of = np.zeros(cap, np.int32)
    g_units = np.zeros(G, np.int32)
    g_ndef = np.zeros(G, np.int32)

    def add(a, g, kind):
        nonlocal n
        i = n
        n += 1
        rg = attr[g]
        k_of[i] = g_units[g] % KMAX
        g_units[g] += 1
        f["gid"][i] = g
        f["kind"][i] = kind
        appr_date[i] = a
        f["appr_m"][i] = K.m_of(a)
        lag = int(np.clip(rg.lognormal(np.log(24), 0.6), 5, 120))
        d = a + dt.timedelta(days=lag)
        disb_date[i] = d
        f["lag"][i] = lag
        f["disb_m"][i] = K.m_of(d)
        f["fp_m"][i] = f["disb_m"][i] + 1 + (1 if d.day > 20 else 0)
        f["due_day"][i] = int(rg.choice([1, 1, 1, 5, 10, 15, 15, 20, 25]))
        f["term"][i] = 120 if rg.random() < 0.75 else 84
        nc = g_naics[g] if kind == 1 or rg.random() < 0.97 else ns[rg.choice(len(ns), p=w_s / w_s.sum())]
        naics[i] = nc
        scale = 1100e3 if nc == "721110" else (650e3 if nc in ("623110", "531130", "312120") else 420e3)
        amt = float(np.clip(np.exp(rg.normal(np.log(scale), 0.75)) * AMOUNT_SCALE.get(K.fy_of_date(a), 1.0), 25e3, 5e6))
        amt = round(amt / 100.0) * 100.0
        f["amt"][i] = amt
        gp = 0.85 if amt <= 150e3 else 0.75
        if EAA_90_START <= a <= EAA_NEW_END:
            gp = 0.90
        f["ug"][i] = round(1 - gp, 2)
        f["var"][i] = rg.random() < 0.85
        f["spread"][i] = float(rg.choice([2.25, 2.50, 2.75, 2.75, 2.75]))
        if f["var"][i]:
            f["rate"][i] = K.prime_on(a) + f["spread"][i]
        else:
            f["rate"][i] = round((K.prime_on(a) + f["spread"][i] + 0.5) * 8) / 8
        windows[i] = sba_paid_months(a, int(f["fp_m"][i]), nc)
        return i

    for t in range(K.H):
        y, mo = K.ym(t)
        for a, g, kind in by_month.get(t, []):
            if not g_dead[g]:
                add(a, g, kind)
        fy = K.fy_of_month(t)
        cand = np.where(is_op & (op_m + 6 <= t) & ~g_dead)[0]
        if len(cand):
            units = np.bincount(f["gid"][:n][(st[:n] == 1)], minlength=G)[cand]
            ua = uniform(seed, g_stable[cand], 63, t, 7)
            hit = cand[ua < ADD[fy] / 12.0 * np.where(units >= 2, ADD_MULTI, ADD_SINGLE)]
            first = K.month_first(t)
            nd = (K.month_end(t) - first).days + 1
            ud = uniform(seed, g_stable[hit], 63, t, 8)
            for g, u_ in zip(hit, ud):
                add(first + dt.timedelta(days=int(u_ * nd)), g, 1)
        N = n
        S = st[:N]
        gsN = g_stable[f["gid"][:N]]
        kN = k_of[:N]
        u_fail, u_fast, u_tr, u_60, u_po, u_dpd = (uniform(seed, gsN, kN, t, r) for r in range(6))
        # disbursement
        new = (S == 0) & (f["disb_m"][:N] == t)
        for i in np.where(new)[0]:
            S[i] = 1
            bal[i] = f["amt"][i]
            nleft[i] = f["term"][i]
        perf = S == 1
        mob = t - f["disb_m"][:N]
        due = perf & (t >= f["fp_m"][:N]) & (nleft[:N] > 0)
        # rate resets: variable loans on the first of January, April, July and October
        if mo in (1, 4, 7, 10):
            pr = K.prime_on(dt.date(y, mo, 1))
            v = perf & f["var"][:N] & (t > f["disb_m"][:N])
            f["rate"][:N][v] = pr + f["spread"][:N][v]
            pay[:N][v] = annuity(bal[:N][v], f["rate"][:N][v], nleft[:N][v])
        first_due = due & (pay[:N] == 0)
        pay[:N][first_due] = annuity(bal[:N][first_due], f["rate"][:N][first_due], nleft[:N][first_due])
        # SBA paid this month's instalment?
        paid = np.zeros(N, bool)
        capped = np.zeros(N, bool)
        for i in np.where(due & (t >= APR20) & (t <= SEP21 + 8))[0]:
            for s0, e0, cp, _ in windows[i]:
                if s0 <= t <= e0:
                    paid[i] = True
                    capped[i] = cp
        # failures
        live = perf & (mob >= 1) & (slow_m[:N] < 0)
        fail = live & (u_fail < h_bus(mob))
        fast = fail & ((u_fast < FAST) | paid)          # while SBA pays the instalments a failure shows as a closure
        slow = fail & ~fast
        slow_m[:N][slow] = t
        trig_now = fast | (perf & (slow_m[:N] >= 0) & (t - slow_m[:N] == 2))
        gt = np.zeros(G, bool)
        gt[f["gid"][:N][trig_now]] = True
        dflt = perf & gt[f["gid"][:N]]
        # transient delinquencies (no failure)
        calm = perf & ~dflt & (slow_m[:N] < 0)
        go30 = calm & (dq[:N] == 0) & due & ~paid & (u_tr < TRANSIENT)
        go60 = calm & (dq[:N] == 1) & (u_60 < TO60)
        prev_dq = dq[:N].copy()
        dq[:N][:] = 0
        dq[:N][go30] = 1
        dq[:N][go60] = 2
        # payoffs and maturities
        po = calm & (prev_dq == 0) & ~go30 & (u_po < p_pay(mob))
        # balances: performing loans pay the instalment due unless failing (slow transit) or defaulting
        payer = due & ~dflt & (slow_m[:N] < 0)
        intr = bal[:N] * f["rate"][:N] / 1200.0
        prin = np.minimum(np.maximum(pay[:N] - intr, 0), bal[:N])
        bal[:N] = np.where(payer, bal[:N] - prin, bal[:N])
        nleft[:N] = np.where(payer, nleft[:N] - 1, nleft[:N])
        mat = payer & (nleft[:N] <= 0) & ~po
        # status codes for the month-end row: 1 CUR 2 D30 3 D60 4 D90 5 ACC 6 LIQ 7 CO 8 PIF 9 MAT
        code = np.zeros(N, np.int8)
        dpd = np.zeros(N, np.int16)
        code[perf] = 1
        tr = perf & (slow_m[:N] >= 0)
        stage = t - slow_m[:N]
        code[tr & (stage == 0)] = 2
        code[tr & (stage == 1)] = 3
        code[go30] = 2
        code[go60] = 3
        code[dflt] = 5
        code[dflt & tr & (stage == 2)] = 4
        dd = f["due_day"][:N].astype(int)
        me = K.month_end(t).day
        dpd[code == 2] = (me - dd[code == 2]) + 30
        dpd[code == 3] = (me - dd[code == 3]) + 60
        dpd[code == 4] = (me - dd[code == 4]) + 90
        ac = (code == 5)
        dpd[ac] = np.where(u_dpd[ac] < 0.3, me - dd[ac], 0)
        dpd = np.maximum(dpd, 0).astype(np.int16)
        code[po] = 8
        code[mat] = 9
        liq = S == 2
        code[liq] = 6
        # group resolutions this month
        res_g = np.where((g_res_m == t) & g_dead)[0]
        cured = np.zeros(N, bool)
        for g in res_g:
            idx = np.where((f["gid"][:N] == g) & (S == 2))[0]
            if g_out[g] == 1:
                cured[idx] = True
                g_dead[g] = False
            elif g_out[g] == 2:
                code[idx] = 8
            else:
                code[idx] = 7
            g_res_m[g] = -1
        code[cured] = 1
        for i in np.where(dflt)[0]:
            events.append((i, t, "default"))
        for i in np.where(trig_now)[0]:
            events.append((i, t, "trigger"))
        out = (S >= 1) & (S <= 2) | dflt
        idx = np.where(out)[0]
        rowbal = bal[:N][idx].copy()
        rowbal[np.isin(code[idx], (7, 8, 9))] = 0.0
        rec.append((idx.astype(np.int32), np.full(len(idx), t, np.int16), code[idx], dpd[idx], rowbal,
                    f["rate"][:N][idx].astype(np.float32), paid[idx], capped[idx], pay[:N][idx].copy()))
        # state changes after the row
        def_m[:N][dflt] = t
        def_bal[:N][dflt] = bal[:N][dflt]
        first_def[:N][dflt & (first_def[:N] < 0)] = t
        trig[:N][trig_now] = True
        S[dflt] = 2
        slow_m[:N][dflt] = -1
        for g in np.where(gt)[0]:
            g_dead[g] = True
            g_def_m[g] = t
            ro = K.rng(world_key, "outcome", int(g_stable[g]), int(g_ndef[g]))
            g_ndef[g] += 1
            x = ro.random()
            if x < CURE:
                g_out[g], g_res_m[g] = 1, t + 2 + int(ro.integers(0, 3))
            elif x < CURE + PIF_LIQ:
                g_out[g], g_res_m[g] = 2, t + 3 + int(ro.integers(0, 8))
            else:
                g_out[g], g_res_m[g] = 3, t + 5 + int(ro.integers(0, 10))
        S[cured] = 1
        for i in np.where(cured)[0]:
            events.append((i, t, "cure"))
            nleft[i] = max(int(f["term"][i] - (t - f["fp_m"][i]) - 1), 1)
            pay[i] = float(annuity(np.array([bal[i]]), np.array([f["rate"][i]]), np.array([nleft[i]]))[0])
        closed_co = code == 7
        closed_pf = code == 8
        S[closed_co] = 3
        S[closed_pf] = 4
        S[mat] = 5
        bal[:N][mat] = 0.0
        bal[:N][po] = 0.0
        end_m[:N][closed_co | closed_pf | mat] = t
        for i in np.where(closed_co)[0]:
            events.append((i, t, "co"))

    N = n
    W.n = N
    for k, v in f.items():
        setattr(W, k, v[:N].copy())
    W.appr_date = appr_date[:N]
    W.disb_date = disb_date[:N]
    W.naics = naics[:N]
    W.windows = windows[:N]
    W.status = st[:N].copy()
    W.bal = bal[:N].copy()
    W.def_m = def_m[:N].copy()
    W.def_bal = def_bal[:N].copy()
    W.end_m = end_m[:N].copy()
    W.trig = trig[:N].copy()
    W.slow_now = {int(i): int(slow_m[i] + 2 - K.T_END - 1) for i in np.where(slow_m[:N] >= 0)[0]}
    W.events = events
    W.g_out = g_out
    W.g_def_m = g_def_m
    cols = ["i", "t", "code", "dpd", "bal", "rate", "sba", "capped", "pay"]
    W.rec = {c: np.concatenate([r[j] for r in rec]) for j, c in enumerate(cols)}
    W.fy = K.fy_of_month(W.appr_m)
    return W


if __name__ == "__main__":
    import time
    t0 = time.time()
    W = simulate()
    R = W.rec
    print("loans %d groups %d rows %d (%.1fs)" % (W.n, W.G, len(R["i"]), time.time() - t0))
    pool = np.isin(W.fy, [2019, 2020, 2021]) & np.isin(W.status, [1, 2])
    print("pool loans %d, in default %d, ug $M %.1f" % (pool.sum(), (pool & (W.status == 2)).sum(),
                                                        (W.bal * W.ug)[pool].sum() / 1e6))
    for c in range(1, 10):
        print(c, int((R["code"] == c).sum()), end="; ")
    print()
