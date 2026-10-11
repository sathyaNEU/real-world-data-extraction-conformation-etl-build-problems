"""The golden solution, computed from the files under target/ only (pandas path).

Also computes every rung of the main ladder and every wrong stop of the asks, so checks.py can assert
them. Nothing here reads simulation state.
"""
import datetime as dt
import os

import numpy as np
import pandas as pd

EXTRACT = dt.date(2023, 2, 3)
SWITCH = dt.date(2023, 1, 3)
PERIOD = {"Q2": dt.date(2022, 6, 30), "Q3": dt.date(2022, 9, 30), "Q4": dt.date(2022, 12, 31)}
DROPS = ["form13f_2022q3", "form13f_2022q4", "edgar13f_daily_20230103_20230203"]


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


def shares_out(target, wl):
    sub = pd.read_csv(os.path.join(target, "fsds_cover_extract", "sub.txt"), sep="\t", dtype=str)
    num = pd.read_csv(os.path.join(target, "fsds_cover_extract", "num.txt"), sep="\t", dtype=str)
    n = num[num.tag == "EntityCommonStockSharesOutstanding"].merge(sub[["adsh", "cik", "form", "filed"]], on="adsh")
    n["cik"] = n["cik"].astype(int)
    n["ddate"] = pd.to_datetime(n["ddate"]).dt.date
    n["filed"] = pd.to_datetime(n["filed"]).dt.date
    n["value"] = n["value"].astype(float).round().astype(np.int64)
    out = {}
    for _, r in wl.iterrows():
        x = n[n.cik == r["Issuer CIK"]]
        for q in ("Q3", "Q4"):
            y = x[x.ddate <= PERIOD[q]].sort_values("ddate")
            out[(r["CUSIP"], q)] = int(y.iloc[-1]["value"])
        out[(r["CUSIP"], "latest")] = int(x.sort_values("ddate").iloc[-1]["value"])
        z = x[x.ddate > PERIOD["Q3"]].sort_values("ddate")
        out[(r["CUSIP"], "Q3_after")] = int(z.iloc[0]["value"])
    return out


def normalise_cusips(inf, wl):
    """OM-4 s.4: nine characters, upper case, leading zeros restored; failing check digit matched on
    issuer name and title where exactly one watchlist security fits."""
    c = inf["CUSIP"].str.strip().str.upper().str.zfill(9)
    ok = c.map(lambda s: len(s) == 9 and s[:8].isalnum() and cusip_check(s[:8]) == s[8])
    names = {r["Issuer"].upper().replace(".", ""): r["CUSIP"] for _, r in wl.iterrows()}
    fixed = c.copy()
    bad = ~ok
    for idx in inf.index[bad]:
        nm = inf.at[idx, "NAMEOFISSUER"].upper().replace(".", "")
        hits = [v for k, v in names.items() if k == nm]
        if len(hits) == 1 and inf.at[idx, "TITLEOFCLASS"] == "COM":
            fixed.at[idx] = hits[0]
    return fixed


def effective_lines(f, inf, period, cut=None):
    """Lines of each manager's report for the period, as amended (types applied in filing order),
    using filings accepted on or before `cut`."""
    g = f[(f.period == period) & (f.REPORTTYPE != "13F NOTICE")]
    if cut is not None:
        g = g[g.fdate <= cut]
    keep = []
    for cik, gg in g.groupby("CIK"):
        gg = gg.sort_values(["fdate", "ACCESSION_NUMBER"])
        cur = []
        for _, r in gg.iterrows():
            if r["ISAMENDMENT"] == "Y" and r["AMENDMENTTYPE"] == "NEW HOLDINGS":
                cur.append(r["ACCESSION_NUMBER"])
            else:  # original or RESTATEMENT
                cur = [r["ACCESSION_NUMBER"]]
        keep += cur
    return inf[inf.ACCESSION_NUMBER.isin(keep)]


def holdings(f, inf, wl, period, cut=None, cusips=None):
    e = effective_lines(f, inf, period, cut)
    e = e[(e.SSHPRNAMTTYPE == "SH") & (e.PUTCALL == "")]
    e = e.merge(f[["ACCESSION_NUMBER", "CIK", "fdate"]], on="ACCESSION_NUMBER")
    if cusips is not None:
        e = e[e.cusip9.isin(cusips)]
    return e


def dollar_values(e, f, all_lines):
    """Put VALUE on a whole-dollar basis: x1000 for filings before the switch, and for any filing
    after it whose implied prices sit a thousandth of every other filer's for the same securities."""
    acc_date = f.set_index("ACCESSION_NUMBER")["fdate"]
    e = e.copy()
    e["fdate_acc"] = e.ACCESSION_NUMBER.map(acc_date)
    e["usd"] = np.where(e.fdate_acc < SWITCH, e.VALUE * 1000, e.VALUE).astype(np.int64)
    # implied price per share against the median filer for the same security
    sh = e[e.SSHPRNAMT > 0]
    px = (sh.usd / sh.SSHPRNAMT)
    med = px.groupby(sh.cusip9).median()
    ratio = (px / sh.cusip9.map(med)).groupby(sh.ACCESSION_NUMBER).median()
    low = ratio[(ratio > 0.0005) & (ratio < 0.002)].index
    e.loc[e.ACCESSION_NUMBER.isin(low), "usd"] = e.loc[e.ACCESSION_NUMBER.isin(low), "VALUE"] * 1000
    e.attrs["thousands_after_switch"] = sorted(low)
    return e


def compute(target):
    f, inf = load(target)
    wl = watch_table(target)
    W9 = list(wl["CUSIP"])
    inf["cusip9"] = normalise_cusips(inf, wl)
    so = shares_out(target, wl)
    names = f.drop_duplicates("CIK", keep="last").set_index("CIK")["FILINGMANAGER_NAME"]
    res = {"cusips": W9, "tickers": list(wl["Ticker"]), "issuers": list(wl["Issuer"])}

    # ---- September (complete)
    h3 = holdings(f, inf, wl, PERIOD["Q3"], cusips=W9)
    sep_sh = h3.groupby("cusip9").SSHPRNAMT.sum()
    res["sep_shares"] = {c: int(sep_sh.get(c, 0)) for c in W9}
    res["S_sep"] = {c: so[(c, "Q3")] for c in W9}
    res["S_dec"] = {c: so[(c, "Q4")] for c in W9}
    res["sep_io"] = {c: 100 * res["sep_shares"][c] / res["S_sep"][c] for c in W9}

    # ---- December on file at the extract, and the managers still to file
    h4 = holdings(f, inf, wl, PERIOD["Q4"], cut=EXTRACT, cusips=W9)
    on4 = h4.groupby("cusip9").SSHPRNAMT.sum()
    filed4 = set(f[(f.period == PERIOD["Q4"]) & (f.fdate <= EXTRACT)].CIK)
    q3_filers = set(f[(f.period == PERIOD["Q3"]) & (f.REPORTTYPE != "13F NOTICE")].CIK)
    pend = q3_filers - filed4
    hp = h3[h3.CIK.isin(pend)]
    carried = hp.groupby("cusip9").SSHPRNAMT.sum()
    res["pending_ciks"] = sorted(pend)
    res["dec_onfile_shares"] = {c: int(on4.get(c, 0)) for c in W9}
    res["dec_carried_shares"] = {c: int(carried.get(c, 0)) for c in W9}
    res["dec_shares"] = {c: res["dec_onfile_shares"][c] + res["dec_carried_shares"][c] for c in W9}
    res["dec_io"] = {c: 100 * res["dec_shares"][c] / res["S_dec"][c] for c in W9}
    res["flag"] = {c: res["dec_io"][c] > 80.0 for c in W9}

    # ---- rungs
    res["R0"] = {c: 100 * res["dec_onfile_shares"][c] / res["S_dec"][c] for c in W9}
    res["R1"] = dict(res["sep_io"])
    n_q3 = len(q3_filers)
    n_in = len(q3_filers & filed4)
    res["c_count"] = n_in / n_q3
    res["R2"] = {c: res["R0"][c] / res["c_count"] for c in W9}
    # aggregate value share on file by the same day of the September window, all securities
    cut3 = PERIOD["Q3"] + (EXTRACT - PERIOD["Q4"])
    all3 = holdings(f, inf, wl, PERIOD["Q3"])
    all3 = dollar_values(all3, f, inf)
    early3 = all3[all3.fdate <= cut3]
    res["c_value"] = early3.usd.sum() / all3.usd.sum()
    res["R3"] = {c: res["R0"][c] / res["c_value"] for c in W9}
    # same-day share for the watchlist securities only (variant)
    w3 = all3[all3.cusip9.isin(W9)]
    res["c_value_watch"] = w3[w3.fdate <= cut3].usd.sum() / w3.usd.sum()
    res["R3w"] = {c: res["R0"][c] / res["c_value_watch"] for c in W9}
    # issuer-level completion from the September window (rigorous variant)
    d3 = (w3[w3.fdate <= cut3].groupby("cusip9").SSHPRNAMT.sum() / w3.groupby("cusip9").SSHPRNAMT.sum())
    res["R4dev"] = {c: res["R0"][c] / float(d3[c]) for c in W9}
    res["dev_share"] = {c: float(d3[c]) for c in W9}

    # ---- back-test in the September window: carry-forward from June vs the rungs
    h2 = holdings(f, inf, wl, PERIOD["Q2"], cusips=W9)
    filed3_cut = set(f[(f.period == PERIOD["Q3"]) & (f.fdate <= cut3)].CIK)
    q2_filers = set(f[(f.period == PERIOD["Q2"]) & (f.REPORTTYPE != "13F NOTICE")].CIK)
    pend3 = q2_filers - filed3_cut
    on3 = holdings(f, inf, wl, PERIOD["Q3"], cut=cut3, cusips=W9).groupby("cusip9").SSHPRNAMT.sum()
    car3 = h2[h2.CIK.isin(pend3)].groupby("cusip9").SSHPRNAMT.sum()
    # aggregate share in the June window at the same day (for the uniform method's own back-test)
    cut2 = PERIOD["Q2"] + (EXTRACT - PERIOD["Q4"])
    all2 = dollar_values(holdings(f, inf, wl, PERIOD["Q2"]), f, inf)
    c_val2 = all2[all2.fdate <= cut2].usd.sum() / all2.usd.sum()
    bt = {}
    for c in W9:
        final = res["sep_shares"][c]
        bt[c] = dict(final=final, onfile=int(on3.get(c, 0)), carried=int(car3.get(c, 0)),
                     cf_err_pp=100 * (on3.get(c, 0) + car3.get(c, 0) - final) / res["S_sep"][c],
                     uni_err_pp=100 * (on3.get(c, 0) / c_val2 - final) / res["S_sep"][c],
                     raw_err_pp=100 * (on3.get(c, 0) - final) / res["S_sep"][c])
    # issuer-level completion factor taken from the June window, applied in the September window
    w2 = all2[all2.cusip9.isin(W9)]
    d2 = (w2[w2.fdate <= cut2].groupby("cusip9").SSHPRNAMT.sum() / w2.groupby("cusip9").SSHPRNAMT.sum())
    for c in W9:
        bt[c]["dev_err_pp"] = 100 * (on3.get(c, 0) / float(d2[c]) - res["sep_shares"][c]) / res["S_sep"][c]
    res["backtest"] = bt
    res["c_value_june"] = c_val2

    # ---- top holder by market value at 31 December (filings in hand)
    h4all = holdings(f, inf, wl, PERIOD["Q4"], cut=EXTRACT)
    h4v = dollar_values(h4all, f, inf)
    res["thousands_after_switch"] = h4v.attrs["thousands_after_switch"]
    hv = h4v[h4v.cusip9.isin(W9)].groupby(["cusip9", "CIK"]).usd.sum().reset_index()
    top = {}
    for c in W9:
        x = hv[hv.cusip9 == c].sort_values(["usd", "CIK"], ascending=[False, True])
        top[c] = dict(cik=int(x.iloc[0].CIK), name=names[int(x.iloc[0].CIK)], usd=int(x.iloc[0].usd),
                      runner_cik=int(x.iloc[1].CIK), runner_usd=int(x.iloc[1].usd))
    res["top"] = top
    # wrong stops: values as reported (no restatement of the thousands filer), largest single line,
    # family consolidation
    h4raw = h4all.copy()
    h4raw["usd"] = h4raw.VALUE
    raw = h4raw[h4raw.cusip9.isin(W9)].groupby(["cusip9", "CIK"]).usd.sum().reset_index()
    line = h4v[h4v.cusip9.isin(W9)].groupby(["cusip9", "CIK"]).usd.max().reset_index()
    reg = pd.read_csv(os.path.join(target, "manager_register.csv"), dtype=str, keep_default_na=False)
    fam = {int(k): (v or str(k)) for k, v in zip(reg.cik, reg.family)}
    hvf = hv.copy()
    hvf["fam"] = hvf.CIK.map(fam)
    famv = hvf.groupby(["cusip9", "fam"]).usd.sum().reset_index()
    res["top_wrong"] = {}
    for c in W9:
        a = raw[raw.cusip9 == c].sort_values("usd", ascending=False).iloc[0]
        b = line[line.cusip9 == c].sort_values("usd", ascending=False).iloc[0]
        d_ = famv[famv.cusip9 == c].sort_values("usd", ascending=False).iloc[0]
        res["top_wrong"][c] = dict(as_reported=int(a.CIK), largest_line=int(b.CIK), family=str(d_.fam))
    # carried value of pending managers (for the contention check)
    pv = dollar_values(holdings(f, inf, wl, PERIOD["Q3"]), f, inf)
    pv = pv[pv.CIK.isin(pend) & pv.cusip9.isin(W9)].groupby(["cusip9", "CIK"]).SSHPRNAMT.sum()
    res["pending_max_shares"] = {c: int(pv[c].max()) if c in pv.index.get_level_values(0) else 0 for c in W9}

    # ---- the September bridge, watchlist combined, in shares
    q3acc = set(f[f.period == PERIOD["Q3"]].ACCESSION_NUMBER)
    l3 = inf[inf.ACCESSION_NUMBER.isin(q3acc)]
    exact = l3[l3.CUSIP.isin(W9)]
    raw_total = int(exact.SSHPRNAMT.sum())
    opt = int(exact[exact.PUTCALL != ""].SSHPRNAMT.sum())
    eff = set(effective_lines(f, inf, PERIOD["Q3"]).ACCESSION_NUMBER)
    sup = exact[(exact.PUTCALL == "") & (~exact.ACCESSION_NUMBER.isin(eff))]
    superseded = int(sup.SSHPRNAMT.sum())
    rep = l3[(~l3.CUSIP.isin(W9)) & (l3.cusip9.isin(W9)) & (l3.PUTCALL == "") & (l3.ACCESSION_NUMBER.isin(eff))]
    repaired = int(rep.SSHPRNAMT.sum())
    prn = int(exact[(exact.SSHPRNAMTTYPE != "SH")].SSHPRNAMT.sum())
    conformed = raw_total - opt - superseded - prn + repaired
    res["bridge"] = dict(raw=raw_total, options=opt, superseded=superseded, principal=prn,
                         cusip_repaired=repaired, conformed=conformed,
                         conformed_check=int(sum(res["sep_shares"].values())))
    # wrong stops for the September ask
    by_drop = f.set_index("ACCESSION_NUMBER")["drop"]
    res["sep_wrong"] = {}
    # (a) September from its own submission-quarter data set only
    f_q4drop = f[f["drop"] == "form13f_2022q4"]
    h3a = holdings(f_q4drop, inf, wl, PERIOD["Q3"], cusips=W9).groupby("cusip9").SSHPRNAMT.sum()
    # (b) latest accession per manager wins
    g = f[(f.period == PERIOD["Q3"]) & (f.REPORTTYPE != "13F NOTICE")].sort_values(["fdate", "ACCESSION_NUMBER"])
    last = set(g.groupby("CIK").ACCESSION_NUMBER.last())
    lb = inf[inf.ACCESSION_NUMBER.isin(last) & (inf.PUTCALL == "") & (inf.SSHPRNAMTTYPE == "SH") & inf.cusip9.isin(W9)]
    h3b = lb.groupby("cusip9").SSHPRNAMT.sum()
    # (c) every accession summed
    allacc = set(g.ACCESSION_NUMBER)
    lc = inf[inf.ACCESSION_NUMBER.isin(allacc) & (inf.PUTCALL == "") & (inf.SSHPRNAMTTYPE == "SH") & inf.cusip9.isin(W9)]
    h3c = lc.groupby("cusip9").SSHPRNAMT.sum()
    # (d) exact CUSIP join
    h3d = h3[h3.CUSIP == h3.cusip9].groupby("cusip9").SSHPRNAMT.sum()
    for c in W9:
        res["sep_wrong"][c] = dict(
            own_drop=100 * h3a.get(c, 0) / res["S_sep"][c],
            latest_wins=100 * h3b.get(c, 0) / res["S_sep"][c],
            sum_all=100 * h3c.get(c, 0) / res["S_sep"][c],
            exact_join=100 * h3d.get(c, 0) / res["S_sep"][c],
            later_count=100 * res["sep_shares"][c] / so[(c, "Q3_after")],
        )
    res["S_jan_latest"] = {c: so[(c, "latest")] for c in W9}
    return res
