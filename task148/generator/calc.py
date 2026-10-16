"""The allowance and its rivals, computed from the world's monthly records the way an analyst computes them from the
servicing history, the loan master and the guarantee register.

Risk sets: a loan is at risk in month t when it was performing (current, 30 or 60 days past due) at the end of t-1 or
was disbursed in t-1; months on book are months since the disbursement month. A default is the first month-end at 90
or more days past due or accelerated; a payoff is a paid-in-full month-end while performing."""
from __future__ import annotations

import numpy as np
import pandas as pd

import common as K

NB = 25                 # six-month bands of months on book, the last open
PERF = (1, 2, 3)
DEFAULT = (4, 5)


def band(m, width=6, nb=NB):
    return np.minimum((np.asarray(m) - 1) // width, nb - 1)


class Panel:
    pass


def panel(W):
    """Loan-months at risk with events, group sizes and the reserve-date book."""
    R = W.rec
    df = pd.DataFrame({"i": R["i"], "t": R["t"].astype(np.int32), "code": R["code"], "dpd": R["dpd"], "bal": R["bal"],
                       "rate": R["rate"]})
    df.sort_values(["i", "t"], inplace=True, kind="mergesort")
    df.reset_index(drop=True, inplace=True)
    prev = df.groupby("i")["code"].shift(1)
    first = prev.isna()
    disb = W.disb_m[df.i.values]
    df["mob"] = df.t.values - disb
    at_risk = (~first & prev.isin(PERF)) | (first & False)
    # a loan disbursed in t-1 has its first row at t-1 (MOB 0): its month t row is at risk through prev in PERF
    df["risk"] = at_risk.values & (df.mob.values >= 1)
    df["dflt"] = df.risk & df.code.isin(DEFAULT)
    df["po"] = df.risk & (df.code == 8)
    df["gid"] = W.gid[df.i.values]
    # group size at the month: the group's loans at risk that month
    k = df[df.risk].groupby(["gid", "t"]).size()
    df["k"] = 0
    rk = df.risk.values
    key = pd.MultiIndex.from_arrays([df.gid.values[rk], df.t.values[rk]])
    df.loc[rk, "k"] = k.reindex(key).values
    P = Panel()
    P.df = df
    P.risk = df[df.risk].copy()
    P.risk["band"] = band(P.risk.mob.values)
    last = df.groupby("i").tail(1)
    on_books = last[(last.t == K.T_END) & ~last.code.isin((7, 8, 9))]
    P.last = last.set_index("i")
    P.on_books = on_books.set_index("i")
    P.W = W
    # charge-off share: loans whose default resolved, charged off against cured or paid in liquidation
    ev = df[df.dflt][["i", "t"]]
    res = []
    codes = df.code.values
    starts = df.groupby("i").head(1).index.values
    pos = pd.Series(np.arange(len(df)), index=df.index)
    nxt = df.groupby("i").cumcount()
    # walk forward from each default to its resolution
    by_i = {i: (s, s + c) for i, s, c in zip(df.i.values[starts], starts, df.groupby("i").size().values)}
    out = []
    for i, t in zip(ev.i.values, ev.t.values):
        s, e = by_i[i]
        j = s + (t - df.t.values[s])
        k2 = j + 1
        while k2 < e and codes[k2] == 6:
            k2 += 1
        if k2 >= e:
            out.append((i, t, "open"))
        else:
            c = codes[k2]
            out.append((i, t, "co" if c == 7 else ("cure" if c in PERF else "pif")))
    P.resol = pd.DataFrame(out, columns=["i", "t", "res"])
    rs = P.resol[P.resol.res != "open"]
    P.co_share = float((rs.res == "co").mean())
    return P


def rate_table(df, col, width=6, nb=NB):
    b = band(df.mob.values, width, nb)
    g = pd.DataFrame({"b": b, "e": df[col].values.astype(float)}).groupby("b")["e"].agg(["sum", "count"])
    return (g["sum"] / g["count"]).reindex(range(nb)).ffill().fillna(0.0).values


def remaining(W, i):
    """Instalments left after the reserve date: months from October 2026 to the maturity month."""
    mat = W.fp_m[i] + W.term[i] - 1
    return int(max(mat - K.T_END, 0))


def sched(b0, rate, rem):
    """Principal scheduled to be outstanding at the end of each of the next rem months at a fixed rate."""
    r = rate / 1200.0
    k = np.arange(1, rem + 1)
    if r == 0:
        return b0 * (1 - k / rem)
    return b0 * ((1 + r) ** rem - (1 + r) ** k) / ((1 + r) ** rem - 1)


class Book:
    pass


def book(P, fys=K.POOL_FY):
    W = P.W
    ob = P.on_books
    pool = ob[(W.fy[ob.index.values] >= fys[0]) & (W.fy[ob.index.values] <= fys[1])].copy()
    pool["ug"] = W.ug[pool.index.values]
    pool["fy"] = W.fy[pool.index.values]
    pool["gid"] = W.gid[pool.index.values]
    pool["perf"] = pool.code.isin(PERF)
    pool["mob_now"] = K.T_END - W.disb_m[pool.index.values]
    pool["rem"] = [remaining(W, i) for i in pool.index.values]
    members = ob[ob.code.isin(PERF)].copy()
    members["gid"] = W.gid[members.index.values]
    members["mob_now"] = K.T_END - W.disb_m[members.index.values]
    members["rem"] = [remaining(W, i) for i in members.index.values]
    members["fy"] = W.fy[members.index.values]
    members["ug"] = W.ug[members.index.values]
    B = Book()
    B.pool = pool
    B.members = members
    return B


def loan_level(B, hz, pz, co, width=6, nb=NB, mult=None, by=None):
    """Each performing pool loan on its own months on book: cumulative incidence of default against payoff and
    maturity, times the charge-off share, on the scheduled unguaranteed principal; loans in default at the share."""
    pool = B.pool
    out = {}
    for i, x in pool.iterrows():
        if not x.perf:
            v = co * x.bal * x.ug
        else:
            rem = int(x.rem)
            if rem <= 0:
                v = 0.0
            else:
                mobs = x.mob_now + np.arange(1, rem + 1)
                h = (hz if by is None else hz[by(x)])[band(mobs, width, nb)]
                if mult is not None:
                    h = h * mult(x)
                p = pz[band(mobs, width, nb)].copy()
                p[-1] = 0.0
                S = np.cumprod(np.r_[1.0, (1 - h - p)[:-1]])
                v = float((S * h * co * sched(x.bal, x.rate, rem)).sum() * x.ug)
        out[i] = v
    return pd.Series(out)


def union(B, hb, pb, co, width=6, nb=NB, pool_only=False, ignore_sib_po=False, sib_rate=None, ead_shift=False):
    """Each performing pool loan priced at its guarantor group's default: the group defaults at the first failure of
    any of its performing loans, each at its own months on book with its own payoff and maturity."""
    pool = B.pool
    out = {}
    for i, x in pool[~pool.perf].iterrows():
        out[i] = co * x.bal * x.ug
    mem = B.members
    if pool_only:
        mem = mem[(mem.fy >= K.POOL_FY[0]) & (mem.fy <= K.POOL_FY[1])]
    gids = set(pool[pool.perf].gid)
    for g, d in mem[mem.gid.isin(gids)].groupby("gid"):
        mob0 = d.mob_now.values
        rems = d.rem.values.astype(int)
        R = int(rems.max())
        if R <= 0:
            for i in d.index:
                if i in pool.index:
                    out[i] = 0.0
            continue
        steps = np.arange(1, R + 1)
        mobs = mob0[:, None] + steps[None, :]
        alive = steps[None, :] <= rems[:, None]
        hb_ = hb if sib_rate is None else sib_rate
        h = np.where(alive, hb[band(mobs, width, nb)], 0.0)
        p = np.where(alive & (steps[None, :] < rems[:, None]), pb[band(mobs, width, nb)], 0.0)
        S_own = np.cumprod(np.c_[np.ones(len(d)), (1 - h - p)[:, :-1]], axis=1)
        hs = np.where(alive, hb_[band(mobs, width, nb)], 0.0)
        ps = np.zeros_like(p) if ignore_sib_po else p
        S_sib = np.cumprod(np.c_[np.ones(len(d)), (1 - hs - ps)[:, :-1]], axis=1)
        pdf = S_sib * hs
        cum = np.cumsum(pdf, axis=1)
        untrig = np.c_[np.ones(len(d)), 1 - cum[:, :-1]]
        q = pdf / np.maximum(untrig, 1e-12)
        idx = list(d.index)
        for jj, i in enumerate(idx):
            if i not in pool.index or not pool.at[i, "perf"]:
                continue
            rj = int(rems[jj])
            if rj <= 0:
                out[i] = 0.0
                continue
            oth = [m for m in range(len(idx)) if m != jj]
            if oth:
                Ssib = np.prod(untrig[oth][:, :rj], axis=0)
                qs = 1 - np.prod(1 - q[oth][:, :rj], axis=0)
            else:
                Ssib = np.ones(rj)
                qs = np.zeros(rj)
            pdef = S_own[jj, :rj] * Ssib * (1 - (1 - h[jj, :rj]) * (1 - qs))
            ead = sched(pool.at[i, "bal"], pool.at[i, "rate"], rj)
            if ead_shift:
                ead = np.r_[pool.at[i, "bal"], ead[:-1]]
            out[i] = float((pdef * co * ead).sum() * pool.at[i, "ug"])
    for i in pool.index:
        out.setdefault(i, 0.0)
    return pd.Series(out)


def truth(W, B, reps=400, seed=("truth",)):
    """The world's own expected charge-offs on the pool: current members forward on the true hazards, fast and slow
    failures, payoffs and maturities, a defaulted group charged off with the world's probability; loans already in a
    slow failure default when it reaches 90 days."""
    import world as WD
    rg = K.rng(*seed)
    pool = B.pool
    pco = 1 - WD.CURE - WD.PIF_LIQ
    out = {}
    for i, x in pool[~pool.perf].iterrows():
        out[i] = pco * x.bal * x.ug
    mem = B.members
    gids = set(pool[pool.perf].gid)
    for g, d in mem[mem.gid.isin(gids)].groupby("gid"):
        nn = len(d)
        mob0 = d.mob_now.values
        rems = d.rem.values.astype(int)
        R = int(rems.max()) + 3
        steps = np.arange(1, R + 1)
        mobs = mob0[:, None] + steps[None, :]
        alive = steps[None, :] <= rems[:, None]
        U1 = rg.random((reps, nn, R)) < (WD.h_bus(mobs) * alive)[None]
        U2 = rg.random((reps, nn, R)) < (WD.p_pay(mobs) * (alive & (steps[None, :] < rems[:, None])))[None]
        slow = rg.random((reps, nn, R)) >= WD.FAST
        pof = np.where(U2.any(2), U2.argmax(2), 10 ** 6)
        valid = U1 & (steps[None, None, :] - 1 < pof[:, :, None])
        fm = np.where(valid.any(2), valid.argmax(2), 10 ** 6)
        sl = np.take_along_axis(slow, np.minimum(fm, R - 1)[:, :, None], 2)[:, :, 0]
        dm = np.where(fm < 10 ** 6, fm + np.where(sl, 2, 0), 10 ** 6)
        # a loan already 30 or 60 days past due in a slow failure at the reserve date
        for jj, i in enumerate(d.index):
            if i in W_slow_set(W) and W_slow_set(W)[i] >= 0:
                dm[:, jj] = W_slow_set(W)[i]
        gd = dm.min(1)
        for jj, i in enumerate(d.index):
            if i not in pool.index or not pool.at[i, "perf"]:
                continue
            rj = int(rems[jj])
            if rj <= 0:
                out[i] = 0.0
                continue
            ok = (gd < pof[:, jj]) & (gd < rj)
            bj = sched(pool.at[i, "bal"], pool.at[i, "rate"], rj)
            out[i] = float(pco * (ok * bj[np.clip(gd, 0, rj - 1)]).mean() * pool.at[i, "ug"])
    for i in pool.index:
        out.setdefault(i, 0.0)
    return pd.Series(out)


def W_slow_set(W):
    """Loans in a slow failure at the reserve date: the step index (0 for October) at which each reaches 90 days."""
    return W.slow_now


# ---------------------------------------------------------------------------------------------------- from the pack
CUR_CODE = {"CUR": 1, "D30": 2, "D60": 3, "D90": 4, "ACC": 5, "LIQ": 6, "CO": 7, "PIF": 8, "MAT": 9}
LEG_CODE = {"CURR": 1, "DLQ1": 2, "DLQ2": 3, "DLQ3": 4, "ACCL": 5, "LIQD": 6, "CHGO": 7, "PDOF": 8, "MATR": 9}
SUFFIX = {"JR", "SR", "II", "III", "IV"}


def guarantor_key(name, kind, tin4):
    """A guarantor across loans: an individual by surname and the TIN's last four, an entity by its name without
    punctuation or the LLC form and the TIN's last four."""
    import re
    s = re.sub(r"[.,]", " ", str(name)).upper().split()
    if kind == "Entity":
        s = [w for w in s if w not in ("LLC", "L", "C")]
        return ("E", " ".join(s), str(tin4).zfill(4))
    s = [w for w in s if w not in SUFFIX]
    return ("I", s[-1], str(tin4).zfill(4))


def party_key(name, kind, tin4, party=None):
    return party


def groups_from_register(reg, key=None):
    """Loans joined through shared guarantors (union-find over the register's rows), by the party number unless
    another key is given."""
    parent = {}

    def find(x):
        while parent.setdefault(x, x) != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    first = {}
    for loan, name, kind, tin, party in zip(reg["SBA Loan No"], reg["Guarantor"], reg["Type"], reg["TIN (last 4)"],
                                            reg["Party No"]):
        loan = str(loan)
        find(loan)
        k = party if key is None else key(name, kind, tin)
        if k in first:
            a, b = find(first[k]), find(loan)
            if a != b:
                parent[a] = b
        else:
            first[k] = loan
    return {x: find(x) for x in list(parent)}


def panel_from_pack(target):
    import os
    import pyarrow.parquet as pq
    import openpyxl
    from records import F_CURRENT, F_LEGACY, F_MASTER, F_REGISTER
    m = pd.read_csv(os.path.join(target, F_MASTER), dtype=str)
    leg2sba = dict(zip(m.legacy_loan_no.dropna(), m.sba_loan_no[m.legacy_loan_no.notna()]))
    note2sba = dict(zip(m.note_no.dropna(), m.sba_loan_no[m.note_no.notna()]))
    cur = pq.read_table(os.path.join(target, F_CURRENT)).to_pandas()
    leg = pq.read_table(os.path.join(target, F_LEGACY)).to_pandas()
    pe = pd.to_datetime(cur.period_end)
    c = pd.DataFrame({"sba": cur.note_no.map(note2sba).values,
                      "t": ((pe.dt.year * 12 + pe.dt.month - 1) - (2009 * 12 + 9)).values,
                      "code": cur.status.map(CUR_CODE).values, "bal": cur.principal_bal.values, "rate": cur.note_rate.values})
    lp = leg.PERIOD.values
    l = pd.DataFrame({"sba": leg.LOAN_NO.map(leg2sba).values, "t": ((lp // 100) * 12 + lp % 100 - 1) - (2009 * 12 + 9),
                      "code": leg.STAT_CD.map(LEG_CODE).values, "bal": leg.PRIN_BAL_CENTS.values / 100.0,
                      "rate": leg.INT_RT.values * 100.0})
    both = pd.concat([l[l.t < 96], c], ignore_index=True)
    sba_ids = sorted(both.sba.unique())
    idx = {s: k for k, s in enumerate(sba_ids)}
    both["i"] = both.sba.map(idx).astype(np.int64)
    both.sort_values(["i", "t"], inplace=True, kind="mergesort")
    both.reset_index(drop=True, inplace=True)
    wb = openpyxl.load_workbook(os.path.join(target, F_REGISTER), read_only=True)
    ws = wb["Guaranties"]
    rows = list(ws.iter_rows(values_only=True))
    reg = pd.DataFrame(rows[1:], columns=rows[0])
    root = groups_from_register(reg)
    ms = m.set_index("sba_loan_no")
    P = Panel()
    P.sba_ids = sba_ids
    P.gid_of = np.array([idx[root.get(s, s)] for s in sba_ids])
    ad = pd.to_datetime(ms.loc[sba_ids, "approval_date"])
    P.fy = np.where(ad.dt.month >= 10, ad.dt.year + 1, ad.dt.year)
    md = pd.to_datetime(ms.loc[sba_ids, "maturity_date"])
    P.mat_m = ((md.dt.year * 12 + md.dt.month - 1) - (2009 * 12 + 9)).values
    P.ug = 1 - ms.loc[sba_ids, "guaranty_pct"].astype(float).values / 100.0
    first_t = both.groupby("i").t.min()
    P.disb_m = first_t.reindex(range(len(sba_ids))).values
    return _finish(P, both)


def _finish(P, df):
    prev = df.groupby("i")["code"].shift(1)
    df["mob"] = df.t.values - P.disb_m[df.i.values]
    df["risk"] = prev.isin(PERF).values & (df.mob.values >= 1)
    df["dflt"] = df.risk & df.code.isin(DEFAULT)
    df["po"] = df.risk & (df.code == 8)
    df["gid"] = P.gid_of[df.i.values]
    rk = df.risk.values
    k = df[rk].groupby(["gid", "t"]).size()
    df["k"] = 0
    df.loc[rk, "k"] = k.reindex(pd.MultiIndex.from_arrays([df.gid.values[rk], df.t.values[rk]])).values
    P.df = df
    P.risk = df[df.risk].copy()
    last = df.groupby("i").tail(1)
    P.last = last.set_index("i")
    P.on_books = last[(last.t == K.T_END) & ~last.code.isin((7, 8, 9))].set_index("i")
    codes = df.code.values
    starts = df.groupby("i").head(1).index.values
    sizes = df.groupby("i").size().values
    by_i = {i: (s, s + n) for i, s, n in zip(df.i.values[starts], starts, sizes)}
    out = []
    ev = df[df.dflt]
    for i, t, pos in zip(ev.i.values, ev.t.values, ev.index.values):
        s, e = by_i[i]
        k2 = pos + 1
        while k2 < e and codes[k2] == 6:
            k2 += 1
        if k2 >= e:
            out.append((i, t, "open"))
        else:
            cc = codes[k2]
            out.append((i, t, "co" if cc == 7 else ("cure" if cc in PERF else "pif")))
    P.resol = pd.DataFrame(out, columns=["i", "t", "res"])
    rs = P.resol[P.resol.res != "open"]
    P.co_share = float((rs.res == "co").mean())
    return P


def book_from_pack(P, fys=K.POOL_FY):
    ob = P.on_books
    ii = ob.index.values
    pool = ob[(P.fy[ii] >= fys[0]) & (P.fy[ii] <= fys[1])].copy()
    pi = pool.index.values
    pool["ug"] = P.ug[pi]
    pool["fy"] = P.fy[pi]
    pool["gid"] = P.gid_of[pi]
    pool["perf"] = pool.code.isin(PERF)
    pool["mob_now"] = K.T_END - P.disb_m[pi]
    pool["rem"] = np.maximum(P.mat_m[pi] - K.T_END, 0)
    members = ob[ob.code.isin(PERF)].copy()
    mi = members.index.values
    members["gid"] = P.gid_of[mi]
    members["mob_now"] = K.T_END - P.disb_m[mi]
    members["rem"] = np.maximum(P.mat_m[mi] - K.T_END, 0)
    members["fy"] = P.fy[mi]
    members["ug"] = P.ug[mi]
    B = Book()
    B.pool = pool
    B.members = members
    return B


# ---------------------------------------------------------------------------------------------------- the asks, from the pack
def _master(target):
    import os
    from records import F_MASTER
    m = pd.read_csv(os.path.join(target, F_MASTER), dtype=str)
    ad = pd.to_datetime(m.approval_date)
    m["fy"] = np.where(ad.dt.month >= 10, ad.dt.year + 1, ad.dt.year)
    return m


def ask_a_lines(target):
    """Every Section 1112 line of the pool's loans, both layouts, in dollars, with the disbursement's line count."""
    import os
    import openpyxl
    from asks import F_CARES, F_EAA
    m = _master(target)
    fy = dict(zip(m.sba_loan_no, m.fy))
    c = pd.read_csv(os.path.join(target, F_CARES), dtype=str)
    c = pd.DataFrame({"remit": pd.to_datetime(c.remit_date, format="%m/%d/%Y"), "trace": c.trace_no, "sba": c.sba_loan_no,
                      "due": pd.to_datetime(c.installment_due, format="%m/%d/%Y"), "amount": c.pmt_amount.astype(float),
                      "layout": "cares"})
    wb = openpyxl.load_workbook(os.path.join(target, F_EAA), read_only=True)
    rows = list(wb.active.iter_rows(values_only=True))
    e = pd.DataFrame(rows[1:], columns=rows[0])
    e = pd.DataFrame({"remit": pd.to_datetime(e["Remit Date"]), "trace": e["ACH Trace"].astype(str),
                      "sba": e["SBA Loan Number"].str.replace("-", "", regex=False),
                      "due": pd.to_datetime(e["Due Date"]), "amount": e["Payment Amount (cents)"].astype(float) / 100.0,
                      "cents": e["Payment Amount (cents)"].astype(float), "layout": "eaa"})
    x = pd.concat([c, e], ignore_index=True)
    x["fy"] = x.sba.map(fy)
    x["n"] = x.groupby(["trace", "sba"]).sba.transform("size")
    x["m_due"] = (x.due.dt.year * 12 + x.due.dt.month - 1) - (2009 * 12 + 9)
    x["m_remit"] = (x.remit.dt.year * 12 + x.remit.dt.month - 1) - (2009 * 12 + 9)
    return x


def ask_a_from_pack(target, how="golden"):
    from asks import ASK_A_FIRST, ASK_A_LAST
    x = ask_a_lines(target)
    x = x[(x.fy >= K.POOL_FY[0]) & (x.fy <= K.POOL_FY[1])]
    if how == "golden":
        v, mcol = x.amount / x.n, "m_due"
    elif how == "lines":
        v, mcol = x.amount, "m_due"
    elif how == "remit":
        v, mcol = x.amount, "m_remit"
    elif how == "cents":
        v, mcol = np.where(x.layout == "eaa", x.cents, x.amount) / x.n, "m_due"
    elif how == "first":
        first = x.groupby(["trace", "sba"]).m_due.transform("min")
        keep = x.m_due == first
        x = x[keep]
        v, mcol = x.amount, "m_due"
    else:
        raise ValueError(how)
    mm = x[mcol].values
    sel = (mm >= ASK_A_FIRST) & (mm <= ASK_A_LAST)
    q = pd.Series(np.asarray(v)[sel]).groupby([K.fq_label(int(t)) for t in mm[sel]]).sum()
    return {k: float(q.get(k, 0.0)) for k in [K.fq_label(t) for t in range(ASK_A_FIRST, ASK_A_LAST + 1, 3)]}


def ask_b_parts(target):
    import os
    from asks import F_CREDITS, F_LEDGER, F_PAYSBA
    m = _master(target)
    fy = dict(zip(m.sba_loan_no, m.fy))
    ug = dict(zip(m.sba_loan_no, 1 - m.guaranty_pct.astype(float) / 100.0))
    n2s = dict(zip(m.note_no.dropna(), m.sba_loan_no[m.note_no.notna()]))
    n2s.update(dict(zip(m.legacy_loan_no.dropna(), m.sba_loan_no[m.legacy_loan_no.notna()])))
    L = pd.read_csv(os.path.join(target, F_LEDGER), dtype={"note_no": str})
    L["sba"] = L.note_no.map(n2s)
    L["posted"] = pd.to_datetime(L.posted)
    L["amount"] = L.amount.astype(float)
    Pm = pd.read_csv(os.path.join(target, F_PAYSBA), dtype={"sba_loan_no": str})
    Pm["paid"] = pd.to_datetime(Pm.paid)
    Pm = Pm[Pm.purpose == "SBA SHARE OF RECOVERY"]
    Cr = pd.read_csv(os.path.join(target, F_CREDITS), dtype=str)
    Cr = Cr[Cr.entry_description == "CS COLL"].copy()
    Cr["sba"] = Cr.addenda.str.extract(r"LN (\d{10})")[0]
    Cr["date"] = pd.to_datetime(Cr.settlement_date)
    Cr["amount"] = Cr.amount.astype(float)
    return m, fy, ug, L, Pm, Cr


def ask_b_from_pack(target, how="golden", switch=None):
    """Net charge-offs by (fiscal year, approval fiscal year). how: golden (receipts at the bank's share: the ledger's
    amount before the module switch, the receipt less SBA's share after it; Treasury offset shares added), ledger (the
    ledger's amounts as kept), netall (SBA's share netted from every receipt), notop (golden without the offsets)."""
    import datetime as _dt
    from asks import ASK_B_FYS, MODULE_SWITCH
    switch = switch or MODULE_SWITCH
    m, fy, ug, L, Pm, Cr = ask_b_parts(target)
    L = L[L.sba.map(fy).between(*K.POOL_FY)]
    out = {(f, v): 0.0 for f in ASK_B_FYS for v in range(K.POOL_FY[0], K.POOL_FY[1] + 1)}

    def add(d, s, v):
        k = (d.year + 1 if d.month >= 10 else d.year, int(fy[s]))
        if k in out:
            out[k] += v
    # SBA's share paid on each receipt: the first payment on the loan on or after the receipt not yet matched
    share = {}
    pm = Pm[Pm.sba_loan_no.map(fy).between(*K.POOL_FY)].sort_values(["sba_loan_no", "paid"])
    by_loan = {s: list(zip(d.paid, d.amount)) for s, d in pm.groupby("sba_loan_no")}
    rc = L[L.code == "RCV"].sort_values(["sba", "posted"])
    for s, d in rc.groupby("sba"):
        pays = by_loan.get(s, [])
        used = 0
        for idx, posted in zip(d.index, d.posted):
            while used < len(pays) and pays[used][0] < posted:
                used += 1
            if used < len(pays):
                share[idx] = pays[used][1]
                used += 1
    co_first = L[L.code == "CO"].groupby("sba").posted.min()
    for idx, r in L.iterrows():
        if r.code in ("CO", "REV"):
            add(r.posted, r.sba, r.amount)
        elif r.code == "RCV":
            amt = -r.amount
            old = r.sba not in co_first.index or co_first[r.sba].date() < switch
            if how == "ledger":
                kept = amt
            elif how == "netall":
                kept = amt - share.get(idx, 0.0)
            elif how == "bydate":
                kept = amt if r.posted.date() < switch else amt - share.get(idx, 0.0)
            else:
                kept = amt if old else amt - share.get(idx, 0.0)
            add(r.posted, r.sba, -kept)
    if how in ("golden", "netall", "ledger_top"):
        for d, s, a in zip(Cr.date, Cr.sba, Cr.amount):
            if s in fy and K.POOL_FY[0] <= fy[s] <= K.POOL_FY[1]:
                add(d, s, -a)
    return out
