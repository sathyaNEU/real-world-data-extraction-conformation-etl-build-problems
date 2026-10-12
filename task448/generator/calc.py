"""Every figure from the shipped files alone: the conformed lender table (HMDA for the reporters, the recorder file
for everyone), the recorder file's capture of the reporters' loans, each shortlisted lender's 2024 and 2025 count, and
the county figures; the golden method and every rung and alternative the checks hold it against."""
import datetime as dt
import os
import re

import numpy as np
import pandas as pd

REGION = ["Saline", "McPherson", "Dickinson", "Marion", "Rice", "Ottawa", "Ellsworth", "Lincoln"]
FOUR = ["Saline", "McPherson", "Dickinson", "Marion"]
FIPS = {"Saline": "20169", "McPherson": "20113", "Dickinson": "20041", "Marion": "20115", "Rice": "20159",
        "Ottawa": "20143", "Ellsworth": "20053", "Lincoln": "20105"}
WIN = (dt.date(2024, 1, 1), dt.date(2025, 12, 31))
PY = (dt.date(2025, 7, 1), dt.date(2026, 6, 30))
FEEDS = ["venridge_pmm_ks8_2024.txt", "venridge_pmm_ks8_2025.txt", "venridge_pmm_ks8_2026ytd.txt"]
V4 = {"RECORDING_DT": "MTG_REC_DATE", "DOC_DT": "MTG_INSTR_DATE", "LOAN_AMT": "MTG_AMT", "LENDER_NAME": "MORTGAGEE_NAME",
      "BORROWER_NAME": "MORTGAGOR_NAME", "DEED_RECORDING_DT": "DEED_REC_DATE", "SALE_AMT": "DEED_CONSIDERATION",
      "SELLER_NAME": "GRANTOR_NAME", "BUYER_NAME": "GRANTEE_NAME", "REMARKS": "DOC_REMARKS", "LOAD_TS": "LOAD_DATE"}


def r10(x):
    return int(np.floor(x / 10.0 + 0.5) * 10)


def _date(s):
    s = str(s)
    if "/" in s:
        m, d, y = s.split("/")
        return dt.date(int(y), int(m), int(d))
    return dt.date.fromisoformat(s[:10])


def load(target):
    """The bundle, conformed: the reporters' HMDA counts, the recorder rows with their lender, and the identifiers."""
    B = {}
    lar = pd.read_csv(os.path.join(target, "hmda_lar_kansas_2024_2025.csv"), dtype=str,
                      usecols=["activity_year", "lei", "county_code", "action_taken", "loan_purpose", "lien_status"])
    reg = lar[lar.county_code.isin(FIPS.values())]
    B["lar_region"] = reg
    pur = reg[(reg.action_taken == "1") & (reg.loan_purpose == "1") & (reg.lien_status == "1")]
    B["hmda"] = pur.groupby("lei").size()
    B["hmda_year"] = pur.groupby(["lei", "activity_year"]).size()
    inv = {v: k for k, v in FIPS.items()}
    B["hmda_county"] = pur.assign(county=pur.county_code.map(inv)).groupby(["lei", "county"]).size()
    B["hmda_bought"] = reg[(reg.action_taken == "6") & (reg.loan_purpose == "1") & (reg.lien_status == "1")].groupby(
        "lei").size()
    B["panel"] = pd.read_csv(os.path.join(target, "hmda_reporter_panel_2024_2025.csv"), dtype=str)
    B["register"] = pd.read_csv(os.path.join(target, "lender_register_2026-09.csv"), dtype=str).fillna("")
    B["alias"] = pd.read_csv(os.path.join(target, "mortgagee_alias_register.csv"), dtype=str)
    B["shortlist"] = pd.read_excel(os.path.join(target, "rural_lender_shortlist_2027.xlsx"), sheet_name="Shortlist",
                                   dtype=str)
    frames = []
    for f in FEEDS:
        d = pd.read_csv(os.path.join(target, f), sep="|", dtype=str, keep_default_na=False)
        d = d.rename(columns=V4)
        d["file"] = f
        frames.append(d)
    F = pd.concat(frames, ignore_index=True)
    for c in ("MTG_REC_DATE", "MTG_INSTR_DATE", "DEED_REC_DATE"):
        F[c] = F[c].map(_date)
    F["MTG_AMT"] = F.MTG_AMT.astype(float)
    F["county"] = F.CNTY_NAME.str.title().replace({"Mcpherson": "McPherson"})
    amap = dict(zip(B["alias"].mortgagee_as_indexed.str.strip(), B["alias"].nmls_id))
    F["nmls"] = F.MORTGAGEE_NAME.str.strip().map(amap).fillna("")
    lei = dict(zip(B["register"].nmls_id, B["register"].lei))
    F["lei"] = F.nmls.map(lei).fillna("")
    F["packaged"] = F.MTG_REC_DATE == F.DEED_REC_DATE
    F["qcd"] = F.DEED_TYPE == "QCD"
    F["rerecord"] = F.DOC_REMARKS.str.contains("RE-RECORD|RERECORD", regex=True)
    F["has_situs"] = F.SITUS_ADDR.str.strip() != ""
    # a second mortgage recorded against the same conveyance is a subordinate lien: the larger amount is the first
    base = F[~F.rerecord & ~F.qcd]
    key = base.CNTY_NAME + "|" + base.DEED_DOC_NO
    rank = base.assign(k=key).sort_values(["k", "MTG_AMT"], ascending=[True, False]).groupby("k").cumcount()
    F["second"] = False
    F.loc[rank.index[rank.values > 0], "second"] = True
    # one mortgage recorded in two counties: the same lender, borrower, amount and instrument date; the house stands
    # where the row has a property address
    sig = F.nmls + "|" + F.MORTGAGOR_NAME + "|" + F.MTG_AMT.astype(str) + "|" + F.MTG_INSTR_DATE.astype(str)
    F["sig"] = sig
    ok = ~F.rerecord & ~F.qcd & ~F.second
    nct = F[ok].groupby("sig").county.nunique()
    multi = set(nct[nct > 1].index)
    F["land_row"] = ok & F.sig.isin(multi) & ~F.has_situs
    F["mortgage"] = ok & ~F.land_row & (F.nmls != "")
    F["seller_note"] = ok & (F.nmls == "")
    B["F"] = F
    sl = B["shortlist"]
    B["short"] = list(zip(sl["NMLS ID"].astype(str), sl["Lender"]))
    reporters = set(B["hmda"].index)
    B["reporter_nmls"] = {n for n, l in lei.items() if l in reporters}
    B["lei_of"] = lei
    return B


def counts(B, sel, window=WIN, by=("nmls",), datecol="MTG_INSTR_DATE"):
    F = B["F"]
    d = F[sel(F) & F[datecol].between(*window)]
    return d.groupby(list(by)).size()


def route_of(B, window=WIN):
    """The route each lender's records took in the window: packaged with the deed, or separate."""
    F = B["F"]
    d = F[F.mortgage & F.MTG_INSTR_DATE.between(*window)]
    return d.groupby("nmls").packaged.mean()


def capture(B, sel=None, window=WIN, num=None, reporters=None, stratum=None):
    """Feed rows over HMDA counts for the reporters, by stratum (a function of the lender's nmls) or pooled."""
    F = B["F"]
    sel = sel or (lambda F: F.mortgage)
    feed = counts(B, sel, window)
    hm = B["hmda"]
    reps = sorted(reporters if reporters is not None else B["reporter_nmls"])
    out = {}
    for n in reps:
        k = stratum(n) if stratum else "all"
        f_ = float(feed.get(n, 0))
        h_ = float(hm.get(B["lei_of"][n], 0))
        a = out.setdefault(k, [0.0, 0.0])
        a[0] += f_
        a[1] += h_
    return {k: v[0] / v[1] for k, v in out.items()}


def lender_counts(B, method="golden", **kw):
    """Each shortlisted lender's 2024 and 2025 count under a method. Reporters take their HMDA count; the others
    their feed rows scaled by the capture the method estimates."""
    rt = route_of(B)
    route = lambda n: "P" if rt.get(n, 1.0) >= 0.5 else "S"
    sel = kw.get("sel", lambda F: F.mortgage)
    window = kw.get("window", WIN)
    datecol = kw.get("datecol", "MTG_INSTR_DATE")
    feed = counts(B, sel, window, datecol=datecol)
    if method == "hmda_only":
        cap = None
    elif method == "unscaled":
        cap = lambda n: 1.0
    elif method == "pooled":
        c = capture(B, sel, window)["all"]
        cap = lambda n: c
    elif method == "route":
        c = capture(B, sel, window, stratum=route)
        cap = lambda n: c[route(n)]
    elif method == "charter":
        ch = dict(zip(B["register"].nmls_id, B["register"].institution_type))
        c = capture(B, sel, window, stratum=lambda n: ch[n])
        cap = lambda n: c[ch[n]]
    elif method == "golden":
        c = capture(B, window=window, stratum=route)
        cap = lambda n: c[route(n)]
        feed = counts(B, lambda F: F.mortgage, window)
    else:
        raise ValueError(method)
    out = {}
    for n, name in B["short"]:
        lei = B["lei_of"].get(n, "")
        if lei in B["hmda"].index:
            out[name] = float(B["hmda"][lei])
        elif cap is None:
            out[name] = 0.0
        else:
            out[name] = float(feed.get(n, 0)) / cap(n)
    return out


def county_capture(B, sel=None):
    """Capture by county: the reporters' feed rows in each county over their HMDA loans there (HMDA's county)."""
    F = B["F"]
    sel = sel or (lambda F: F.mortgage)
    d = F[sel(F) & F.MTG_INSTR_DATE.between(*WIN) & F.nmls.isin(B["reporter_nmls"])]
    fc = d.groupby("county").size()
    hc = B["hmda_county"].groupby(level=1).sum()
    return {c: float(fc.get(c, 0)) / float(hc.get(c, 1)) for c in REGION}


def lender_counts_county(B):
    c = county_capture(B)
    F = B["F"]
    d = F[F.mortgage & F.MTG_INSTR_DATE.between(*WIN)]
    out = {}
    for n, name in B["short"]:
        lei = B["lei_of"].get(n, "")
        if lei in B["hmda"].index:
            out[name] = float(B["hmda"][lei])
        else:
            g = d[d.nmls == n].groupby("county").size()
            out[name] = sum(float(v) / c[k] for k, v in g.items())
    return out


def lender_counts_year(B):
    """Capture by year: each year's feed rows over each year's HMDA counts, pooled across routes."""
    out = {}
    tot = {}
    for y in (2024, 2025):
        w = (dt.date(y, 1, 1), dt.date(y, 12, 31))
        feed = counts(B, lambda F: F.mortgage, w)
        f_ = sum(float(feed.get(n, 0)) for n in B["reporter_nmls"])
        h_ = sum(float(B["hmda_year"].get((B["lei_of"][n], str(y)), 0)) for n in B["reporter_nmls"])
        c = f_ / h_
        for n, name in B["short"]:
            lei = B["lei_of"].get(n, "")
            if lei in B["hmda"].index:
                tot[name] = float(B["hmda"][lei])
            else:
                tot[name] = tot.get(name, 0.0) + float(feed.get(n, 0)) / c
    out.update(tot)
    return out


def five(v):
    s = sorted(v.items(), key=lambda kv: (-kv[1], kv[0]))
    return s[:5], s[5]


def captures(B):
    rt = route_of(B)
    route = lambda n: "P" if rt.get(n, 1.0) >= 0.5 else "S"
    return capture(B, stratum=route), route


def market_two_year(B, reporters="share", dedupe=True, hmda_county=False, sellers=False, keep=None):
    """Home-purchase first liens on homes in each county closed in 2024 and 2025, every lender: the reporters' HMDA
    counts spread over the counties their recorded mortgages stand in; the others' feed rows over their route's
    capture."""
    F = B["F"]
    if keep is None:
        c, route = captures(B)
    else:
        rt = route_of(B)
        route = lambda n: "P" if rt.get(n, 1.0) >= 0.5 else "S"
        c = capture(B, lambda F: F.mortgage & keep(F), stratum=route)
    sel = F.mortgage if dedupe else (F.mortgage | F.land_row)
    if keep is not None:
        sel = sel & keep(F)
    d = F[sel & F.MTG_INSTR_DATE.between(*WIN)]
    out = {k: 0.0 for k in REGION}
    for n, g in d.groupby("nmls"):
        lei = B["lei_of"].get(n, "")
        byc = g.groupby("county").size()
        if lei in B["hmda"].index:
            if hmda_county:
                for k in REGION:
                    out[k] += float(B["hmda_county"].get((lei, k), 0))
            elif reporters == "share":
                tot = float(B["hmda"][lei])
                for k, v in byc.items():
                    out[k] += tot * v / byc.sum()
            else:
                for k, v in byc.items():
                    out[k] += v / c[route(n)]
        else:
            for k, v in byc.items():
                out[k] += v / c[route(n)]
    # reporters with no recorded row at all keep their HMDA counts where HMDA puts them
    seen = set(d.nmls)
    for n in B["reporter_nmls"]:
        if n not in seen:
            lei = B["lei_of"][n]
            for k in REGION:
                out[k] += float(B["hmda_county"].get((lei, k), 0))
    if sellers:
        s = F[F.seller_note & F.MTG_INSTR_DATE.between(*WIN)].groupby("county").size()
        for k, v in s.items():
            out[k] += v / c["P"]
    return out


def program_year(B, per_record=True, own_capture=False, datecol="MTG_INSTR_DATE"):
    """Home-purchase first liens on homes in each county closed 1 July 2025 to 30 June 2026, every lender: each
    recorded mortgage over the capture of the route it was recorded by."""
    c, route = captures(B)
    F = B["F"]
    d = F[F.mortgage & F[datecol].between(*PY)]
    own = {}
    if own_capture:
        feed = counts(B, lambda F: F.mortgage)
        for n in B["reporter_nmls"]:
            own[n] = float(feed.get(n, 0)) / float(B["hmda"][B["lei_of"][n]])
    out = {k: 0.0 for k in REGION}
    for r in d.itertuples():
        rr = ("P" if r.packaged else "S") if per_record else route(r.nmls)
        cc = c[rr]
        if own_capture and r.nmls in own and rr == route(r.nmls):
            cc = own[r.nmls]
        out[r.county] += 1.0 / cc
    return out


def ask_figures(two, py):
    a = {k: two[k] for k in FOUR}
    a["other four"] = sum(two[k] for k in REGION if k not in FOUR)
    b = {k: py[k] for k in FOUR}
    b["other four"] = sum(py[k] for k in REGION if k not in FOUR)
    b["total"] = sum(py.values())
    return a, b


def estimate(B, sel=None, window=WIN, datecol="MTG_INSTR_DATE", stratum="route", estimator="ratio", reporters=None,
             hmda=None, per_year=False):
    """Each shortlisted lender's count under one handling: which recorder rows count (sel), the closing or recording
    window, the strata the capture is measured in (route, pooled, charter, county), the estimator within a stratum
    (ratio of totals, mean or median of the reporters' own ratios), the reporters it is measured on, and the HMDA
    counts it is measured against."""
    F = B["F"]
    sel = sel or (lambda F: F.mortgage)
    hm = B["hmda"] if hmda is None else hmda
    if per_year:
        out = {}
        for y in (2024, 2025):
            w = (dt.date(y, 1, 1), dt.date(y, 12, 31))
            hy = B["hmda_year"].xs(str(y), level=1)
            part = estimate(B, sel, w, datecol, stratum, estimator, reporters, hy)
            for k, v in part.items():
                out[k] = out.get(k, 0.0) + v
        for n, name in B["short"]:
            lei = B["lei_of"].get(n, "")
            if lei in B["hmda"].index:
                out[name] = float(B["hmda"][lei])
        return out
    d = F[sel(F) & F[datecol].between(*window)]
    feed = d.groupby("nmls").size()
    pk = d.groupby("nmls").packaged.mean()
    route = lambda n: "P" if pk.get(n, 1.0) >= 0.5 else "S"
    inst = dict(zip(B["register"].nmls_id, B["register"].institution_type))
    if stratum == "route":
        key = route
    elif stratum == "pooled":
        key = lambda n: "all"
    elif stratum == "charter":
        key = lambda n: inst[n]
    else:
        raise ValueError(stratum)
    reps = sorted(reporters if reporters is not None else B["reporter_nmls"])
    groups = {}
    for n in reps:
        h = float(hm.get(B["lei_of"][n], 0))
        if h <= 0:
            continue
        groups.setdefault(key(n), []).append((float(feed.get(n, 0)), h))
    cap = {}
    for k, g in groups.items():
        if estimator == "ratio":
            cap[k] = sum(a for a, _ in g) / sum(b for _, b in g)
        elif estimator == "mean":
            cap[k] = float(np.mean([a / b for a, b in g]))
        else:
            cap[k] = float(np.median([a / b for a, b in g]))
    out = {}
    for n, name in B["short"]:
        lei = B["lei_of"].get(n, "")
        if lei in B["hmda"].index:
            out[name] = float(B["hmda"][lei]) if hmda is None or per_year else float(hm.get(lei, 0))
        else:
            out[name] = float(feed.get(n, 0)) / cap[key(n)]
    return out
