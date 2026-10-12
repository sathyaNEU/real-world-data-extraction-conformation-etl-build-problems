"""The golden solution, computed from the files under target/ only (pandas path).

OM-4 s.2 read literally: the managers that report holdings for December are every manager with a December
holdings or combination report on file, and every manager with a September holdings or combination report
and no December notice; the holdings of the reports not yet filed are estimated on the basis that, run on
the September window at the same day (3 November 2022, completing from June), comes closest to September's
ownership on all the reports since filed, by the largest miss across the twelve names.

Also computes every rung of the main ladder, every basis in the back-test, the golden's own variants, and
every ask device's wrong stops, so checks.py can assert them. Nothing here reads simulation state.
"""
import datetime as dt
import itertools
import os

import numpy as np
import pandas as pd

EXTRACT = dt.date(2023, 2, 3)
SWITCH = dt.date(2023, 1, 3)
PERIOD = {"Q2": dt.date(2022, 6, 30), "Q3": dt.date(2022, 9, 30), "Q4": dt.date(2022, 12, 31)}
DAYS = (EXTRACT - PERIOD["Q4"]).days
CUT = {q: PERIOD[q] + dt.timedelta(days=DAYS) for q in PERIOD}
DROPS = ["form13f_2022q3", "form13f_2022q4", "edgar13f_daily_20230103_20230203"]
PASSIVE = "Index and ETF sponsor"


def cusip_check(base8):
    total = 0
    for i, ch in enumerate(base8):
        v = int(ch) if ch.isdigit() else ord(ch.upper()) - 55
        if i % 2 == 1:
            v *= 2
        total += v // 10 + v % 10
    return str((10 - total % 10) % 10)


def sdate(s):
    return dt.datetime.strptime(s, "%d-%b-%Y").date()


def load(target):
    subs, covs, infs = [], [], []
    for d in DROPS:
        s = pd.read_csv(os.path.join(target, d, "SUBMISSION.tsv"), sep="\t", dtype=str, keep_default_na=False)
        c = pd.read_csv(os.path.join(target, d, "COVERPAGE.tsv"), sep="\t", dtype=str, keep_default_na=False)
        i = pd.read_csv(os.path.join(target, d, "INFOTABLE.tsv"), sep="\t", dtype=str, keep_default_na=False)
        s["drop"] = d
        subs.append(s); covs.append(c); infs.append(i)
    sub = pd.concat(subs, ignore_index=True)
    cov = pd.concat(covs, ignore_index=True)
    inf = pd.concat(infs, ignore_index=True)
    f = sub.merge(cov, on="ACCESSION_NUMBER", how="left")
    f["fdate"] = f["FILING_DATE"].map(sdate)
    f["period"] = f["REPORTCALENDARORQUARTER"].map(sdate)
    f["CIK"] = f["CIK"].astype(int)
    f["amendno"] = pd.to_numeric(f["AMENDMENTNO"].replace("", "0")).astype(int)
    inf["VALUE"] = inf["VALUE"].astype(np.int64)
    inf["SSHPRNAMT"] = inf["SSHPRNAMT"].astype(np.int64)
    return f, inf


def watch_table(target):
    w = pd.read_excel(os.path.join(target, "client_watchlist_crowding_2022Q4.xlsx"), sheet_name="Watchlist",
                      header=4, dtype=str)
    w = w.dropna(subset=["CUSIP"])
    w["Issuer CIK"] = w["Issuer CIK"].astype(int)
    w["Seq"] = w["Seq"].astype(int)
    return w.sort_values("Seq").reset_index(drop=True)


def register(target):
    reg = pd.read_csv(os.path.join(target, "manager_register.csv"), dtype=str, keep_default_na=False)
    reg["cik"] = reg["cik"].astype(int)
    return reg


def counts(target, wl):
    sub = pd.read_csv(os.path.join(target, "fsds_cover_extract", "sub.txt"), sep="\t", dtype=str)
    num = pd.read_csv(os.path.join(target, "fsds_cover_extract", "num.txt"), sep="\t", dtype=str)
    n = num[num.tag == "EntityCommonStockSharesOutstanding"].merge(sub[["adsh", "cik", "form", "filed", "period"]], on="adsh")
    n["cik"] = n["cik"].astype(int)
    n["ddate"] = pd.to_datetime(n["ddate"]).dt.date
    n["value"] = n["value"].astype(float).round().astype(np.int64)
    out = {}
    for _, r in wl.iterrows():
        x = n[n.cik == r["Issuer CIK"]]
        for q in ("Q2", "Q3", "Q4"):
            y = x[x.ddate <= PERIOD[q]].sort_values("ddate")
            out[(r["CUSIP"], q)] = int(y.iloc[-1]["value"])
        z = x[x.ddate > PERIOD["Q3"]].sort_values("ddate")
        out[(r["CUSIP"], "Q3_after")] = int(z.iloc[0]["value"])
        z = x[(x.form == "10-Q") & (x.period == "20220630")]
        out[(r["CUSIP"], "Q3_10q")] = int(z.iloc[0]["value"])
        out[(r["CUSIP"], "latest")] = int(x.sort_values("ddate").iloc[-1]["value"])
        out[(r["CUSIP"], "n_q3_amend")] = int(((x.form == "10-Q/A") & (x.period == "20220930")).sum())
    return out


def stem(name):
    return name.upper().replace(".", "").split()[0]


def normalise_cusips(inf, wl):
    """OM-4 s.4: nine characters, upper case, leading zeros restored; a CUSIP failing its check digit is
    matched on issuer name and title of class where exactly one covered security fits."""
    c = inf["CUSIP"].str.strip().str.upper().str.zfill(9)
    ok = c.map(lambda s: len(s) == 9 and s[:8].isalnum() and cusip_check(s[:8]) == s[8])
    stems = {}
    for _, r in wl.iterrows():
        stems.setdefault(stem(r["Issuer"]), []).append(r["CUSIP"])
    fixed = c.copy()
    how = pd.Series("", index=inf.index)
    how[(inf["CUSIP"] != c) & ok] = "keyed"
    for idx in inf.index[~ok]:
        hits = stems.get(stem(inf.at[idx, "NAMEOFISSUER"]), [])
        if len(hits) == 1 and inf.at[idx, "TITLEOFCLASS"] == "COM":
            fixed.at[idx] = hits[0]
            how.at[idx] = "base" if c.at[idx][:8] == hits[0][:8] else "name"
    return fixed, how


def is_option(e):
    return (e.PUTCALL != "") | e.TITLEOFCLASS.isin(["CALL", "PUT"])


MODES = ("num", "file", "on_or_after", "after", "latest", "sum_all", "original")


def sub_period(f):
    """the same filings keyed to the period in the submission header instead of the cover page"""
    g = f.copy()
    g["period"] = g["PERIODOFREPORT"].map(sdate)
    return g


def effective_accessions(f, period, cut=None, mode="num"):
    """Accessions making up each manager's report for the period, as amended, filings on or before `cut`.
    'num' (the golden): in filing order, amendments filed on one day in amendment-number order; a
    RESTATEMENT (or an original) replaces what came before and a NEW HOLDINGS amendment adds to it. The other
    modes are the asks' wrong stops: 'file' the data set's own order (filing date, then accession);
    'on_or_after' and 'after' the latest restatement plus every new holdings amendment filed on or after (or
    after) its date; 'latest' the last accession; 'sum_all' every version; 'original' the original alone."""
    g = f[(f.period == period) & (f.REPORTTYPE != "13F NOTICE")]
    if cut is not None:
        g = g[g.fdate <= cut]
    keep = []
    for cik, gg in g.groupby("CIK"):
        if mode == "num":
            gg = gg.sort_values(["fdate", "amendno", "ACCESSION_NUMBER"])
        else:
            gg = gg.sort_values(["fdate", "ACCESSION_NUMBER"])
        nh = (gg.ISAMENDMENT == "Y") & (gg.AMENDMENTTYPE == "NEW HOLDINGS")
        if mode == "sum_all":
            keep += list(gg.ACCESSION_NUMBER)
        elif mode == "latest":
            keep.append(gg.ACCESSION_NUMBER.iloc[-1])
        elif mode == "original":
            o = gg[gg.ISAMENDMENT != "Y"]
            keep.append((o if len(o) else gg).ACCESSION_NUMBER.iloc[0])
        elif mode in ("on_or_after", "after"):
            base = gg[~nh]
            b = base.iloc[-1] if len(base) else gg.iloc[0]
            add = gg[nh & ((gg.fdate >= b.fdate) if mode == "on_or_after" else (gg.fdate > b.fdate))]
            keep += [b.ACCESSION_NUMBER] + [a for a in add.ACCESSION_NUMBER if a != b.ACCESSION_NUMBER]
        else:
            cur = []
            for _, r in gg.iterrows():
                if r["ISAMENDMENT"] == "Y" and r["AMENDMENTTYPE"] == "NEW HOLDINGS":
                    cur.append(r["ACCESSION_NUMBER"])
                else:
                    cur = [r["ACCESSION_NUMBER"]]
            keep += cur
    return set(keep)


def lines_for(f, inf, period, cut=None, mode="num"):
    acc = effective_accessions(f, period, cut, mode)
    e = inf[inf.ACCESSION_NUMBER.isin(acc) & (inf.SSHPRNAMTTYPE == "SH")]
    return e.merge(f[["ACCESSION_NUMBER", "CIK", "fdate"]].drop_duplicates("ACCESSION_NUMBER"), on="ACCESSION_NUMBER")


def holdings(f, inf, period, cut=None, cusips=None, mode="num"):
    e = lines_for(f, inf, period, cut, mode)
    e = e[~is_option(e)]
    if cusips is not None:
        e = e[e.cusip9.isin(cusips)]
    return e


def dollar_values(e, f):
    """VALUE on a whole-dollar basis: x1000 for filings before 3 January 2023 and for a report whose cover
    page states its values in thousands."""
    d = f.set_index("ACCESSION_NUMBER")
    e = e.copy()
    k = e.ACCESSION_NUMBER.map(d["fdate"]) < SWITCH
    note = e.ACCESSION_NUMBER.map(d["ADDITIONALINFORMATION"]).str.contains("thousands of dollars", regex=False)
    e["usd"] = np.where(k | note, e.VALUE * 1000, e.VALUE).astype(np.int64)
    e.attrs["thousands_after_switch"] = sorted(set(e.ACCESSION_NUMBER[note & ~k]))
    return e


def _sum(e, by="cusip9"):
    return e.groupby(by).SSHPRNAMT.sum()


STAKE_BASES = ("sponsors_stake", "stake_sponsors", "stake_all", "stake_type_pooled_all")
GRID_SP = ("none", "pooled", "stake", "per_name")
GRID_OT = ("flat", "own_pooled", "own_per_name", "stake", "sp_pooled", "sp_per_name")


def window(f, inf, W9, mtype, qn, qp, cut, mode="num", Sn=None, Sp=None):
    """qn: the open period, qp: the previous one, cut: the extract day, Sn and Sp the OM-4 s.5 counts of the
    two periods. Every basis's per-name share estimate plus its parts; parts["bases"](Sn, Sp) recomputes every
    basis (the stake bases read the counts) and parts["grid"](Sn, Sp) the sponsors-by-others grid."""
    def per(e, cs=W9):
        s = _sum(e)
        return {c: int(s.get(c, 0)) for c in cs}
    fn = f[(f.period == PERIOD[qn]) & (f.fdate <= cut)]
    filed_any = set(fn.CIK)
    filed_hold = set(fn[fn.REPORTTYPE != "13F NOTICE"].CIK)
    prev_hold = set(f[(f.period == PERIOD[qp]) & (f.REPORTTYPE != "13F NOTICE")].CIK)
    due = prev_hold - filed_any
    both = filed_hold & prev_hold
    hn = holdings(f, inf, PERIOD[qn], cut=cut, mode=mode)                      # every security
    hp = holdings(f, inf, PERIOD[qp], mode=mode)
    hnw, hpw = hn[hn.cusip9.isin(W9)], hp[hp.cusip9.isin(W9)]
    on = per(hnw)
    dueH = hpw[hpw.CIK.isin(due)]
    due_by = dueH.groupby(["CIK", "cusip9"]).SSHPRNAMT.sum()
    due_t = {}
    for (cik, c), v in due_by.items():
        due_t[(mtype[cik], c)] = due_t.get((mtype[cik], c), 0) + float(v)
    types_due = sorted({t for t, c in due_t})
    bothN, bothP = hnw[hnw.CIK.isin(both)], hpw[hpw.CIK.isin(both)]
    tN = bothN.CIK.map(mtype); tP = bothP.CIK.map(mtype)
    rt = (bothN.groupby(tN).SSHPRNAMT.sum() / bothP.groupby(tP).SSHPRNAMT.sum()).to_dict()
    aN = hn[hn.CIK.isin(both)]; aP = hp[hp.CIK.isin(both)]
    rt_all = (aN.groupby(aN.CIK.map(mtype)).SSHPRNAMT.sum() / aP.groupby(aP.CIK.map(mtype)).SSHPRNAMT.sum()).to_dict()
    Nt = {k: float(v) for k, v in bothN.groupby([tN, "cusip9"]).SSHPRNAMT.sum().items()}
    Pt = {k: float(v) for k, v in bothP.groupby([tP, "cusip9"]).SSHPRNAMT.sum().items()}
    rt_name = {k: Nt.get(k, 0) / v for k, v in Pt.items() if v > 0}
    r_pool = bothN.SSHPRNAMT.sum() / bothP.SSHPRNAMT.sum()
    r_pool_name = (_sum(bothN) / _sum(bothP)).to_dict()
    mN = bothN.groupby("CIK").SSHPRNAMT.sum(); mP = bothP.groupby("CIK").SSHPRNAMT.sum()
    ratios = (mN.reindex(mP.index).fillna(0) / mP)[mP > 0]
    r_mean = ratios.groupby(ratios.index.map(mtype)).mean().to_dict()
    rp = rt[PASSIVE]

    def stake_change(t, Sn_, Sp_):
        """the filed managers' summed stakes in the twelve names, this period over the last"""
        num = sum(Nt.get((t, c), 0) / Sn_[c] for c in W9)
        den = sum(Pt.get((t, c), 0) / Sp_[c] for c in W9)
        return num / den

    def est(fn_rate):
        out = {c: float(on[c]) for c in W9}
        for (t, c), v in sorted(due_t.items()):
            out[c] += v * fn_rate(t, c)
        return out

    def bases(Sn_, Sp_):
        g = {c: Sn_[c] / Sp_[c] for c in W9}
        kP = stake_change(PASSIVE, Sn_, Sp_)
        kt = {t: stake_change(t, Sn_, Sp_) for t in types_due}
        B = {}
        B["sponsors_per_name"] = est(lambda t, c: rt_name.get((PASSIVE, c), rp) if t == PASSIVE else rt.get(t, 1.0))
        B["sponsors_per_name_flat"] = est(lambda t, c: rt_name.get((PASSIVE, c), rp) if t == PASSIVE else 1.0)
        B["sponsors_stake"] = est(lambda t, c: kP * g[c] if t == PASSIVE else 1.0)
        B["type_pooled"] = est(lambda t, c: rt.get(t, 1.0))
        B["type_allsec"] = est(lambda t, c: rt_all.get(t, 1.0))
        B["sponsors_only"] = est(lambda t, c: rp if t == PASSIVE else 1.0)
        B["stake_sponsors"] = est(lambda t, c: g[c] if t == PASSIVE else 1.0)
        B["stake_all"] = est(lambda t, c: g[c])
        B["stake_type_pooled_all"] = est(lambda t, c: kt[t] * g[c])
        B["one_rate"] = est(lambda t, c: rp)
        B["one_rate_per_name"] = est(lambda t, c: rt_name.get((PASSIVE, c), rp))
        B["all_pooled"] = est(lambda t, c: r_pool)
        B["type_mean_ratio"] = est(lambda t, c: r_mean.get(t, 1.0))
        B["flat"] = est(lambda t, c: 1.0)
        B["all_per_name"] = est(lambda t, c: r_pool_name.get(c, 1.0))
        B["type_per_name"] = est(lambda t, c: rt_name.get((t, c), 1.0))
        B["onfile"] = {c: float(on[c]) for c in W9}
        return B

    def grid(Sn_, Sp_):
        """the sponsors' factor (none, pooled, stake without growth, per name) against every other type's (flat,
        its own pooled change, its own per-name change, its stake, the sponsors' pooled change, the sponsors'
        per-name change)"""
        g = {c: Sn_[c] / Sp_[c] for c in W9}
        fs = {"none": lambda c: 1.0, "pooled": lambda c: rp, "stake": lambda c: g[c],
              "per_name": lambda c: rt_name.get((PASSIVE, c), rp)}
        fo = {"flat": lambda t, c: 1.0, "own_pooled": lambda t, c: rt.get(t, 1.0),
              "own_per_name": lambda t, c: rt_name.get((t, c), 1.0), "stake": lambda t, c: g[c],
              "sp_pooled": lambda t, c: rp, "sp_per_name": lambda t, c: rt_name.get((PASSIVE, c), rp)}
        return {(a, b): est(lambda t, c, a=a, b=b: fs[a](c) if t == PASSIVE else fo[b](t, c))
                for a in GRID_SP for b in GRID_OT}

    B = bases(Sn, Sp) if Sn is not None else {}
    parts = dict(on=on, due=sorted(due), both=sorted(both), rt=rt, rt_all=rt_all, r_pool=r_pool,
                 r_pool_name=r_pool_name, r_mean=r_mean, due_by=due_by, due_t=due_t, n_prev=len(prev_hold),
                 n_in=len(prev_hold & filed_any), hpw=hpw, bothN_sum=float(bothN.SSHPRNAMT.sum()),
                 bothP_sum=float(bothP.SSHPRNAMT.sum()), bothN_name=_sum(bothN).to_dict(), bothP_name=_sum(bothP).to_dict(),
                 due_sum={c: float(dueH[dueH.cusip9 == c].SSHPRNAMT.sum()) for c in W9}, rt_name=rt_name,
                 Nt=Nt, Pt=Pt, stake_change=stake_change, bases=bases, grid=grid, types_due=types_due)
    return B, parts


def make_backtest(f, inf, W9, mtype, S, mode="num"):
    """OM-4 s.2's criterion on the September window at day 34, completing from June, with the amendments
    read in `mode` on the filings `f` (cover-page or header periods). Returns the per-basis largest miss
    function, which also takes the ask hazards as added September shares on bank trust lines filed by the
    cut (`delta`) and replacement September counts (`Ssep`, read by the stake bases too)."""
    sep_shares = {c: int(v) for c, v in _sum(holdings(f, inf, PERIOD["Q3"], cusips=W9, mode=mode)).items()}
    sep_shares = {c: sep_shares.get(c, 0) for c in W9}
    B3, P3 = window(f, inf, W9, mtype, "Q3", "Q2", CUT["Q3"], mode, S["Q3"], S["Q2"])
    h2w = holdings(f, inf, PERIOD["Q2"], cusips=W9, mode=mode)
    all2 = dollar_values(holdings(f, inf, PERIOD["Q2"], mode=mode), f)
    c_val2 = all2[all2.fdate <= CUT["Q2"]].usd.sum() / all2.usd.sum()
    d2 = (_sum(h2w[h2w.fdate <= CUT["Q2"]]) / _sum(h2w)).to_dict()
    jun_io = {c: 100 * float(_sum(h2w).get(c, 0)) / S["Q2"][c] for c in W9}
    cache = {}

    def backtest(delta=None, Ssep=None):
        delta = delta or {c: 0 for c in W9}
        Ssep = Ssep or S["Q3"]
        key = tuple(Ssep[c] for c in W9)
        if key not in cache:
            cache[key] = B3 if Ssep == S["Q3"] else P3["bases"](Ssep, S["Q2"])
        Bx = cache[key]
        fin = {c: sep_shares[c] + delta[c] for c in W9}
        on = {c: P3["on"][c] + delta[c] for c in W9}
        E = {}
        for k in Bx:
            if k in ("all_pooled", "all_per_name"):
                continue
            E[k] = {c: Bx[k][c] + delta[c] for c in W9}
        rp = (P3["bothN_sum"] + sum(delta.values())) / P3["bothP_sum"]
        E["all_pooled"] = {c: on[c] + (B3["all_pooled"][c] - P3["on"][c]) / P3["r_pool"] * rp for c in W9}
        E["all_per_name"] = {}
        for c in W9:
            r0 = P3["bothN_name"].get(c, 0) / P3["bothP_name"][c]
            r1 = (P3["bothN_name"].get(c, 0) + delta[c]) / P3["bothP_name"][c]
            E["all_per_name"][c] = on[c] + (B3["all_per_name"][c] - P3["on"][c]) / r0 * r1
        E["issuer_factor"] = {c: on[c] / d2[c] for c in W9}
        E["value_share"] = {c: on[c] / c_val2 for c in W9}
        E["filer_share"] = {c: on[c] / (P3["n_in"] / P3["n_prev"]) for c in W9}
        out = {}
        for k, e in E.items():
            out[k] = max(abs(100 * (e[c] - fin[c]) / Ssep[c]) for c in W9)
        out["last_quarter"] = max(abs(jun_io[c] - 100 * fin[c] / Ssep[c]) for c in W9)
        return out
    return backtest, dict(B3=B3, P3=P3, jun_io=jun_io, d2=d2, c_val2=c_val2, h2w=h2w, sep_shares=sep_shares)


def ask_parts(f, inf, W9, mode="num", sep_drops=None):
    """Ask A's per-name September shares and Ask B's bridge for one reading of the records: `f` keyed by the
    cover page or the header, amendments in `mode`, September reports from `sep_drops` (all by default).
    Also each hazard's per-name delta when mishandled on that reading's lines."""
    def per(e):
        s = _sum(e)
        return {c: int(s.get(c, 0)) for c in W9}
    g = f if sep_drops is None else f[(f.period != PERIOD["Q3"]) | f["drop"].isin(sep_drops)]
    l3e = lines_for(g, inf, PERIOD["Q3"], mode=mode)
    good = l3e[~is_option(l3e) & l3e.cusip9.isin(W9)]
    shares = per(good)
    titleopt = l3e[(l3e.PUTCALL == "") & l3e.TITLEOFCLASS.isin(["CALL", "PUT"]) & l3e.cusip9.isin(W9)]
    haz = {"a2|kept": per(titleopt),
           "title|com_only": {c: -v for c, v in per(good[good.TITLEOFCLASS != "COM"]).items()},
           "a3|exact": {c: -v for c, v in per(good[good.fix.isin(["name", "base"])]).items()},
           "a3|base8": {c: -v for c, v in per(good[good.fix == "name"]).items()},
           "keyed|exact": {c: -v for c, v in per(good[good.fix == "keyed"]).items()}}
    q3acc = set(g[g.period == PERIOD["Q3"]].ACCESSION_NUMBER)
    l3 = inf[inf.ACCESSION_NUMBER.isin(q3acc)]
    exact = l3[l3.CUSIP.isin(W9)]
    raw_total = int(exact.SSHPRNAMT.sum())
    opt = int(exact[is_option(exact)].SSHPRNAMT.sum())
    eff = effective_accessions(g, PERIOD["Q3"], mode=mode)
    sup = exact[(~is_option(exact)) & (~exact.ACCESSION_NUMBER.isin(eff))]
    superseded = int(sup.SSHPRNAMT.sum())
    rep = l3[(~l3.CUSIP.isin(W9)) & (l3.cusip9.isin(W9)) & (~is_option(l3)) & (l3.ACCESSION_NUMBER.isin(eff))]
    repaired = int(rep.SSHPRNAMT.sum())
    prn = int(exact[(exact.SSHPRNAMTTYPE != "SH")].SSHPRNAMT.sum())
    bridge = dict(raw=raw_total, options=opt, superseded=superseded, principal=prn, cusip_repaired=repaired,
                  conformed=raw_total - opt - superseded - prn + repaired)
    return dict(shares=shares, haz=haz, bridge=bridge, eff=eff)


def compute(target):
    f, inf = load(target)
    wl = watch_table(target)
    reg = register(target)
    mtype = dict(zip(reg.cik, reg.manager_type))
    W9 = list(wl["CUSIP"])
    inf["cusip9"], inf["fix"] = normalise_cusips(inf, wl)
    so = counts(target, wl)
    res = {"cusips": W9, "tickers": list(wl["Ticker"]), "issuers": list(wl["Issuer"]), "so": {f"{k[0]}|{k[1]}": v for k, v in so.items()}}
    S = {q: {c: so[(c, q)] for c in W9} for q in ("Q2", "Q3", "Q4")}
    res["S_sep"], res["S_dec"], res["S_jun"] = S["Q3"], S["Q4"], S["Q2"]

    # ---------------------------------------------------------------- September, every report as amended (Ask A)
    h3 = holdings(f, inf, PERIOD["Q3"], cusips=W9)
    s3 = _sum(h3)
    res["sep_shares"] = {c: int(s3.get(c, 0)) for c in W9}
    res["sep_io"] = {c: 100 * res["sep_shares"][c] / S["Q3"][c] for c in W9}

    # ---------------------------------------------------------------- December (the call)
    B4, P4 = window(f, inf, W9, mtype, "Q4", "Q3", EXTRACT, "num", S["Q4"], S["Q3"])
    res["due_ciks"] = P4["due"]
    res["_due_by"] = P4["due_by"]
    res["_P4"] = P4
    res["n_reporting_onfile"] = len(set(f[(f.period == PERIOD["Q4"]) & (f.fdate <= EXTRACT) & (f.REPORTTYPE != "13F NOTICE")].CIK))
    res["type_change"] = P4["rt"]
    res["type_change_allsec"] = P4["rt_all"]
    res["sponsor_change_name"] = {c: P4["rt_name"][(PASSIVE, c)] for c in W9}
    res["sponsor_stake_change"] = P4["stake_change"](PASSIVE, S["Q4"], S["Q3"])
    res["dec_onfile_shares"] = P4["on"]
    res["dec_shares_est"] = B4["sponsors_per_name"]
    res["dec_io"] = {c: 100 * B4["sponsors_per_name"][c] / S["Q4"][c] for c in W9}
    res["flag"] = {c: res["dec_io"][c] > 80.0 for c in W9}
    VAR = ("sponsors_per_name_flat", "sponsors_stake")
    res["dec_variants"] = {k: {c: 100 * B4[k][c] / S["Q4"][c] for c in W9} for k in VAR}
    rungs = {k: {c: 100 * v[c] / S["Q4"][c] for c in W9} for k, v in B4.items()
             if k not in VAR and k != "sponsors_per_name"}
    # own trend: each manager still due by its own June-to-September change (cannot be run at day 34 of the
    # September window, so the criterion cannot select it; a rival rung)
    h2w = holdings(f, inf, PERIOD["Q2"], cusips=W9)
    own = (_sum(h3, "CIK") / _sum(h2w, "CIK")).to_dict()
    ot = {c: float(P4["on"][c]) for c in W9}
    for (cik, c), v in P4["due_by"].items():
        ot[c] += v * own.get(cik, 1.0)
    rungs["own_trend"] = {c: 100 * ot[c] / S["Q4"][c] for c in W9}
    rungs["R1_last_quarter"] = dict(res["sep_io"])
    rungs["R2_filer_share"] = {c: rungs["onfile"][c] * P4["n_prev"] / P4["n_in"] for c in W9}
    all3 = dollar_values(holdings(f, inf, PERIOD["Q3"]), f)
    c_val3 = all3[all3.fdate <= CUT["Q3"]].usd.sum() / all3.usd.sum()
    rungs["R3_value_share"] = {c: rungs["onfile"][c] / c_val3 for c in W9}
    d3 = (_sum(h3[h3.fdate <= CUT["Q3"]]) / _sum(h3)).to_dict()
    rungs["issuer_factor"] = {c: rungs["onfile"][c] / d3[c] for c in W9}
    res["grid"] = {k: {c: 100 * v[c] / S["Q4"][c] for c in W9} for k, v in P4["grid"](S["Q4"], S["Q3"]).items()}
    res["rungs"] = rungs
    res["c_val3"], res["c_count4"] = c_val3, P4["n_in"] / P4["n_prev"]

    # ---------------------------------------------------------------- the back-test (OM-4 s.2's criterion)
    bt, BT = make_backtest(f, inf, W9, mtype, S, "num")
    assert BT["sep_shares"] == res["sep_shares"]
    res["jun_io"] = BT["jun_io"]
    res["bt_est"] = BT["B3"]
    res["bt_P3"] = BT["P3"]
    res["r_mean"], res["r_mean3"], res["type_change3"] = P4["r_mean"], BT["P3"]["r_mean"], BT["P3"]["rt"]
    res["backtest"] = bt()
    res["_backtest_fn"] = bt

    # ---------------------------------------------------------------- the asks on every reading of the records
    fsub = sub_period(f)
    readings = {}
    for per_src, ff in (("cover", f), ("header", fsub)):
        for mode in MODES:
            readings[(per_src, mode, "all")] = ask_parts(ff, inf, W9, mode)
            readings[(per_src, mode, "q4")] = ask_parts(ff, inf, W9, mode, sep_drops=["form13f_2022q4"])
    gold = readings[("cover", "num", "all")]
    assert gold["shares"] == res["sep_shares"]
    res["bridge"] = dict(gold["bridge"], conformed_check=int(sum(res["sep_shares"].values())))
    res["readings"] = readings
    res["_frames"] = dict(f=f, fsub=fsub, inf=inf, mtype=mtype, S=S)
    res["dev_counts"] = {"q10": {c: so[(c, "Q3_10q")] for c in W9}, "oct": {c: so[(c, "Q3_after")] for c in W9}}

    def io(r):
        return {c: 100 * r["shares"][c] / S["Q3"][c] for c in W9}
    STOPS_A = {"S1": ("header", "file"), "S2": ("cover", "file"), "S3": ("header", "num"), "S4": ("cover", "latest"),
               "S5": ("cover", "num")}
    STOPS_B = {"S1": ("header", "file", "all"), "S2": ("cover", "file", "all"), "S3": ("header", "num", "all"),
               "S4": ("cover", "num", "q4"), "S5": ("cover", "num", "all")}
    res["stops_a"] = {k: io(readings[(p, m, "all")]) for k, (p, m) in STOPS_A.items()}
    res["stops_b"] = {k: readings[v]["bridge"] for k, v in STOPS_B.items()}

    # device hosts: every CIK with a hazard line or more than one September filing
    l3e = lines_for(f, inf, PERIOD["Q3"])
    good = l3e[~is_option(l3e) & l3e.cusip9.isin(W9)]
    titleopt = l3e[(l3e.PUTCALL == "") & l3e.TITLEOFCLASS.isin(["CALL", "PUT"]) & l3e.cusip9.isin(W9)]
    devlines = pd.concat([titleopt, good[good.TITLEOFCLASS != "COM"], good[good.fix != ""]])
    q3f = f[(f.period == PERIOD["Q3"]) & (f.REPORTTYPE != "13F NOTICE")]
    multi = set(q3f[q3f.duplicated("CIK", keep=False)].CIK)
    res["device_hosts"] = sorted(set(devlines.CIK) | multi)
    return res


HAZ = (("a2", ("kept",)), ("title", ("com_only",)), ("a3", ("exact", "base8")), ("keyed", ("exact",)))


def device_combos(res):
    """every combination of September device handling on Ask A: the header or cover period (DV-2), seven
    amendment orders (DV-1), the four line hazards and the three counts; per-name ownership and the bridge"""
    W9 = res["cusips"]
    out = []
    hz = [[("correct", None)] + [(f"{k}|{m}", None) for m in ms] for k, ms in HAZ]
    cn = [("correct", res["S_sep"]), ("q10", res["dev_counts"]["q10"]), ("oct", res["dev_counts"]["oct"])]
    for per_src in ("cover", "header"):
        for mode in MODES:
            for drops in ("all", "q4"):
                r = res["readings"][(per_src, mode, drops)]
                for hc in itertools.product(*hz):
                    sh = dict(r["shares"])
                    b = dict(r["bridge"])
                    for name, _ in hc:
                        if name == "correct":
                            continue
                        d = r["haz"][name]
                        for c in W9:
                            sh[c] += d[c]
                        tot = sum(d.values())
                        if name == "a2|kept":
                            b["options"] -= tot
                        elif name.startswith(("a3", "keyed")):
                            b["cusip_repaired"] += tot
                        b["conformed"] += tot
                    for cname, Sx in cn:
                        names = (per_src, mode, drops) + tuple(x[0] for x in hc) + (cname,)
                        own = {c: 100 * sh[c] / Sx[c] for c in W9}
                        delta = {c: sh[c] - res["sep_shares"][c] for c in W9}
                        touched = {c for c in W9 if delta[c] != 0 or Sx[c] != res["S_sep"][c]}
                        out.append(dict(names=names, delta=delta, S=Sx, own=own, touched=touched, bridge=b,
                                        end=b["conformed"], golden=(per_src, mode, drops) == ("cover", "num", "all")
                                        and all(x[0] == "correct" for x in hc) and cname == "correct"))
    return out
