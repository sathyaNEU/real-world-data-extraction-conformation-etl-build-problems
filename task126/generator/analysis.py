"""Generator-side constructions on the in-memory world: every rung, grid cell, partial, corpus back-test and ask
cell. The independent verifier recomputes all of them from the shipped files on its own code path."""
import math

import numpy as np

import params as P

BIG = 10 ** 9
M = P.M


def r1(x):
    """Round half up to one decimal (the charter's 'to one decimal')."""
    return math.floor(x * 10 + 0.5) / 10


def km_days(t, ev, q, strict=False):
    """Kaplan-Meier quantile in days: the first event time at which survival falls to 1-q or below
    (strict: below). Events sort before censorings at the same time."""
    t = np.asarray(t, dtype=np.int64)
    ev = np.asarray(ev, dtype=bool)
    o = np.lexsort((~ev, t))
    t, ev = t[o], ev[o]
    n = len(t)
    at_risk = n - np.arange(n)
    f = np.where(ev, 1.0 - 1.0 / at_risk, 1.0)
    S = np.cumprod(f)
    tgt = 1 - q
    hit = (S < tgt - 1e-12) if strict else (S <= tgt + 1e-12)
    hit &= ev
    k = np.argmax(hit)
    return int(t[k]) if hit[k] else None


def plain_q(t, ev, q, how):
    """Empirical quantile with the undecided placed above every decision (they are all older than any graded
    quantile). how: 'lower', 'higher', 'midpoint', 'linear'."""
    t = np.where(ev, t, BIG)
    return float(np.quantile(np.asarray(t, dtype=float), q, method=how))


class Arrays:
    def __init__(self, W):
        self.W = W
        n = W.n()
        self.n = n
        self.start = np.array(W.start, dtype=np.int64)
        self.kind = np.array(W.kind, dtype=np.int8)
        self.route = np.array(W.route, dtype=np.int8)
        self.child = np.array(W.child, dtype=np.int64)
        self.parent = np.array(W.parent, dtype=np.int64)
        self.prog = np.array(W.prog, dtype=bool)
        self.status = np.array(W.status)
        self.code = np.array(W.code)
        self.dec = np.array(W.dec, dtype=np.int64)
        self.close = np.array([c if c is not None else BIG for c in W.close], dtype=np.int64)
        self.grant = np.array([g if g is not None else BIG for g in W.grant], dtype=np.int64)
        X = P.EXTRACT
        # decided by the extract (a decision notice served): ALW/ABN/REF/CX, or allowed and awaiting grant
        self.decided = (self.status != "") | ((self.code == "A") & (self.dec <= X))
        lo, hi = P.FY22
        self.infy = (self.start >= lo) & (self.start <= hi)
        # chain walks
        child, route = W.child, W.route
        last_all, app_last, endtype = [0] * n, [0] * n, [0] * n
        for i in range(n):
            j = i
            while child[j] >= 0:
                j = child[j]
            last_all[i] = j
            j = i
            while child[j] >= 0 and route[child[j]] == 1:
                j = child[j]
            app_last[i] = j
            endtype[i] = 1 if child[j] >= 0 else 0
        self.last_all = np.array(last_all, dtype=np.int64)
        self.app_last = np.array(app_last, dtype=np.int64)
        self.app_endtype = np.array(endtype, dtype=np.int8)

    def app_end(self, i_arr, use_grant=False, at_close=False):
        """Rung-4 final decision date for application filing dockets i_arr (BIG when undecided)."""
        j = self.app_last[i_arr]
        cont = self.app_endtype[i_arr] == 1
        e = np.where(self.decided[j], self.dec[j], BIG)
        if use_grant:
            e = np.where(self.code[j] == "A", np.where(self.grant[j] <= P.EXTRACT, self.grant[j], BIG), e)
        return np.where(cont, self.close[j] if at_close else self.dec[j], e)

    def chain_end(self, i_arr, use_grant=False):
        """Rung-3 end: the last docket of the CX chain."""
        j = self.last_all[i_arr]
        e = np.where(self.decided[j], self.dec[j], BIG)
        if use_grant:
            e = np.where(self.code[j] == "A", np.where(self.grant[j] <= P.EXTRACT, self.grant[j], BIG), e)
        return e


def summary(starts, ends):
    """(t, ev) arrays from filing and end dates (BIG = undecided, censored at the extract)."""
    ev = ends <= P.EXTRACT
    t = np.where(ev, ends - starts, P.EXTRACT - starts)
    return t, ev


def med_m(starts, ends, q=0.5):
    t, ev = summary(starts, ends)
    d = km_days(t, ev, q)
    return d / M


def rungs(A):
    X = P.EXTRACT
    out = {}
    idx = np.where(A.infy)[0]
    s = A.start[idx]
    # rung 0: docket close (grant for an allowed docket)
    out["R0"] = med_m(s, np.where(A.close[idx] <= X, A.close[idx], BIG))
    # rung 1: decision notice, a CX docket ended at its refusal
    e1 = np.where(A.decided[idx], A.dec[idx], BIG)
    out["R1"] = med_m(s, e1)
    # rung 2: CX dockets censored at the transfer
    ev2 = A.decided[idx] & (A.status[idx] != "CX")
    t2 = np.where(A.decided[idx], A.dec[idx] - s, X - s)
    out["R2"] = km_days(t2, ev2, 0.5) / M
    # rung 3: every CX edge chained
    r3 = np.where(A.infy & (A.kind != 1))[0]
    out["R3"] = med_m(A.start[r3], A.chain_end(r3))
    # rung 4: the answer
    r4 = np.where(A.infy & ((A.kind != 1) | (A.route == 2)))[0]
    out["R4"] = med_m(A.start[r4], A.app_end(r4))
    return out, r3, r4


def chain_root(A, i):
    while A.kind[i] == 1:
        i = A.parent[i]
    return i


def grid(A, r3, r4):
    """Every cell of the correction grid and the partials (FY2022 median, months)."""
    X = P.EXTRACT
    lo, hi = P.FY22
    g = {}
    g["chains_grant_end"] = med_m(A.start[r3], A.chain_end(r3, use_grant=True))
    g["split_grant_end"] = med_m(A.start[r4], A.app_end(r4, use_grant=True))
    g["left_out"] = med_m(A.start[r3], A.app_end(r3))
    cont22 = np.where(A.infy & (A.route == 2))[0]
    g["parents_chained_cont_added"] = med_m(np.r_[A.start[r3], A.start[cont22]],
                                            np.r_[A.chain_end(r3), A.app_end(cont22)])
    allcont = np.where(A.route == 2)[0]
    roots = np.array([chain_root(A, i) for i in allcont], dtype=np.int64)
    keep = (A.start[roots] >= lo) & (A.start[roots] <= hi)
    g["benefit_dated"] = med_m(np.r_[A.start[r3], A.start[roots[keep]]],
                               np.r_[A.app_end(r3), A.app_end(allcont[keep])])
    g["parent_at_close"] = med_m(A.start[r4], A.app_end(r4, at_close=True))
    e4 = A.app_end(r4)
    dd = (e4 - A.start[r4])[e4 <= X]
    g["decided_only"] = float(np.quantile(dd.astype(float), 0.5, method="lower")) / M
    # family chain: CX, CN and DV edges all chained from each FY2022 original filing
    kids = {}
    for i in np.where((A.kind == 2) | (A.kind == 3))[0]:
        kids.setdefault(int(A.parent[i]), []).append(int(i))
    ends3 = {}

    def fam_end(i):
        e = int(A.chain_end(np.array([i]))[0])
        out = [e]
        j = i
        while True:
            for k in kids.get(j, []):
                out.append(fam_end(k))
            if A.child[j] >= 0:
                j = int(A.child[j])
            else:
                break
        return BIG if max(out) >= BIG else max(out)

    fr = np.where(A.infy & (A.kind == 0))[0]
    g["family_chain"] = med_m(A.start[fr], np.array([fam_end(int(i)) for i in fr], dtype=np.int64))
    ship_lo = P.fy_bounds(P.SHIP_FROM_FY)[0]
    anyr = np.array(sorted(r for r in {chain_root(A, int(i)) for i in np.where(A.infy)[0]}
                           if A.start[r] >= ship_lo), dtype=np.int64)
    g["any_docket_cohort"] = med_m(A.start[anyr], A.chain_end(anyr))
    t, ev = summary(A.start[r4], e4)
    g["plain_median_undecided_at_extract"] = plain_q(np.where(ev, t, X - A.start[r4]), np.ones(len(t), bool), 0.5,
                                                     "lower") / M
    import datetime as dt
    c0, c1 = dt.date(2022, 1, 1).toordinal(), dt.date(2022, 12, 31).toordinal()
    cy = np.where(((A.kind != 1) | (A.route == 2)) & (A.start >= c0) & (A.start <= c1))[0]
    g["calendar_year_2022"] = med_m(A.start[cy], A.app_end(cy))
    return g


def headline(A, r4):
    """The answer and its supporting figures."""
    X = P.EXTRACT
    s = A.start[r4]
    e = A.app_end(r4)
    t, ev = summary(s, e)
    h = {"n": len(r4), "median_days": km_days(t, ev, 0.5), "lq_days": km_days(t, ev, 0.25),
         "undecided": int((~ev).sum()), "within36": int(((t <= 1095) & ev).sum())}
    h["median"] = h["median_days"] / M
    h["lq"] = h["lq_days"] / M
    h["undecided_pct"] = 100 * h["undecided"] / h["n"]
    h["within36_pct"] = 100 * h["within36"] / h["n"]
    h["min_undecided_age"] = int((X - s[~ev]).min())
    # convergence: every quantile definition and every day-count convention files the same tenth
    alts = {"km_strict": km_days(t, ev, 0.5, strict=True)}
    for how in ("lower", "higher", "midpoint", "linear"):
        alts[how] = plain_q(t, ev, 0.5, how)
    h["median_alts"] = alts
    h["dur_hist_1095_1096"] = int((((t == 1095) | (t == 1096)) & ev).sum())
    return h


def cells_for(t, ev, labels):
    """Per group: (lower quartile months, median months, share decided within 36 months %)."""
    out = {}
    for g in P.GROUPS:
        a = labels == g
        lq, md = km_days(t[a], ev[a], 0.25), km_days(t[a], ev[a], 0.5)
        sh = 100 * ((t[a] <= 1095) & ev[a]).sum() / a.sum()
        out[g] = (lq / M, md / M, sh, int(a.sum()))
    return out


def rounded(cells):
    return {g: (r1(v[0]), r1(v[1]), r1(v[2])) for g, v in cells.items()}


def group_labels(A, idx):
    """The group of each application under the answer and under each designed stop."""
    W, S = A.W, A.W.S
    aud = [W.au_dock[i] for i in idx]
    auc = [W.au_close[i] for i in idx]
    exc = [W.ex_close[i] for i in idx]
    st = A.start[idx]
    lab = {
        "answer": np.array([S.cur_group[a] for a in aud]),
        "S1_tg_column": np.array([S.old_group[a] if s < P.RECUT else S.cur_group[a] for a, s in zip(aud, st)]),
        "S2_asof_docketing_au": np.array([S.old_group[a] if s < P.RECUT else S.cur_group[a]
                                          for a, s in zip(aud, st)]),
        "S2b_asof_art_unit_column": np.array([S.old_group[a] if s < P.RECUT else S.cur_group[a]
                                              for a, s in zip(auc, st)]),
        "S3_current_group_art_unit_column": np.array([S.cur_group[a] for a in auc]),
        "S4_roster_home_au": np.array([S.cur_group[S.home[e]] for e in exc]),
        "S5_old_group_docketing_au_restated_never": np.array([S.old_group[a] for a in aud]),
    }
    return lab


def ask_cells(A, r3, r4):
    e4 = A.app_end(r4)
    t, ev = summary(A.start[r4], e4)
    labs = group_labels(A, r4)
    res = {k: cells_for(t, ev, v) for k, v in labs.items()}
    t3, ev3 = summary(A.start[r3], A.chain_end(r3))
    res["rung3_answer_groups"] = cells_for(t3, ev3, group_labels(A, r3)["answer"])
    # convergence of each answer cell across quantile definitions
    conv = {}
    lab = labs["answer"]
    for g in P.GROUPS:
        a = lab == g
        vals = []
        for q in (0.25, 0.5):
            d = [km_days(t[a], ev[a], q), km_days(t[a], ev[a], q, strict=True)]
            d += [plain_q(t[a], ev[a], q, how) for how in ("lower", "higher", "midpoint", "linear")]
            vals.append({r1(x / M) for x in d})
        conv[g] = vals
    return res, conv, (t, ev, lab)


def corpus(A):
    """The partner office's acknowledgements: programme applications filed FY2019 to FY2022."""
    X = P.EXTRACT
    lo = P.fy_bounds(P.CORPUS_FY[0])[0]
    hi = P.fy_bounds(P.CORPUS_FY[1])[1]
    cases = np.where(A.prog & (A.kind == 0) & (A.start >= lo) & (A.start <= hi))[0]
    e3 = A.chain_end(cases)
    e4 = A.app_end(cases)
    last = A.last_all[cases]
    dtype = np.where(e3 <= X, A.code[last], "")
    reex = A.child[cases] >= 0
    # rival readings of each case
    r0 = np.where(A.close[cases] <= X, A.close[cases], BIG)
    r1_ = np.where(A.decided[cases], A.dec[cases], BIG)
    r2 = np.where(A.decided[cases] & (A.status[cases] != "CX"), A.dec[cases], BIG)
    # successors in programme chains credited 1N (route 2): must be none
    n1n = 0
    for i in cases:
        j = int(i)
        while A.child[j] >= 0:
            j = int(A.child[j])
            n1n += int(A.route[j] == 2)
    return dict(cases=cases, e3=e3, e4=e4, dtype=dtype, reex=reex, r0=r0, r1=r1_, r2=r2, n1n=n1n)


def quarter_label(o):
    import datetime as dt
    d = dt.date.fromordinal(int(o))
    return "%d-Q%d" % (d.year, (d.month - 1) // 3 + 1)


def partner_median(days):
    """Median days from filing to the acknowledged decision, an open case counted as still waiting
    (above every decision); for an even count the mean of the two middle values."""
    v = np.sort(np.asarray(days, dtype=float))
    n = len(v)
    m = v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2
    return m


def corpus_quarters(A, C, ends):
    q = np.array([quarter_label(s) for s in A.start[C["cases"]]])
    out = {}
    for lab in sorted(set(q)):
        a = q == lab
        d = np.where(ends[a] <= P.EXTRACT, ends[a] - A.start[C["cases"]][a], BIG)
        out[lab] = partner_median(d)
    return out


def p1_table(A):
    """Last year's Table P1: examiner docket pendency by docketing year, months from docketing to docket close
    (the grant for an allowed docket), reported once 98 per cent of the year's dockets have closed."""
    X25 = P.EXTRACT_2025
    rows = {}
    for fy in range(P.P1_FROM_FY, 2026):
        lo, hi = P.fy_bounds(fy)
        a = (A.start >= lo) & (A.start <= hi)
        cl = A.close[a]
        ev25 = cl <= X25
        t25 = np.where(ev25, cl - A.start[a], X25 - A.start[a])
        share = ev25.mean()
        k25 = km_days(t25, ev25, 0.5)
        med25 = k25 / M if k25 is not None else None
        ev26 = cl <= P.EXTRACT
        t26 = np.where(ev26, cl - A.start[a], P.EXTRACT - A.start[a])
        k26 = km_days(t26, ev26, 0.5)
        med26 = k26 / M if k26 is not None else None
        rows[fy] = dict(n=int(a.sum()), closed_share=share, med25=med25, med26=med26)
    return rows
