"""task169 calc: every figure computed from the shipped files only (the golden method, the default path and the
rival routes), so deliver.py, checks.py and the cracker read one implementation and verify.py keeps its own."""
from __future__ import annotations

import datetime as dt
import os

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import statsmodels.api as sm

import common as C

CUT = pd.Timestamp(C.CUT)
COMPLETE_TO = CUT - pd.Timedelta(days=C.WINDOW)            # releases with a full 730 days of record
CONV_TO = pd.Timestamp("2024-06-30")                       # arrests old enough for their cases to have closed
BANDS = ((0, 90), (90, 180), (180, 365), (365, 730))
CLS = {"FA": "F1", "FB": "F1", "FC": "F2", "FD": "F2", "FE": "F2", "M1": "M", "M2": "M", "M3": "M"}
PAROLE_CODES = {"PAR", "RPR", "PAROLE", "REPAROLE"}
DIST_OF = {c.upper(): d for d, cs in C.COUNTIES.items() for c in cs}


def _mdy(s):
    return pd.to_datetime(s, format="%m/%d/%Y", errors="coerce").astype("datetime64[ns]")


def load(target):
    j = lambda f: os.path.join(target, f)
    rel = pd.read_csv(j(C.F_REL), dtype=str, keep_default_na=False)
    rel["rd"] = _mdy(rel.release_date)
    rel["birth"] = _mdy(rel.birth_date)
    rel["maxd"] = _mdy(rel.max_expiration_date)
    rel["code"] = rel.movement_code.map({"PAROLE": "PAR", "REPAROLE": "RPR", "MAX EXP": "EXP"}).fillna(rel.movement_code)
    rel["priors"] = rel.prior_commitments.astype(int)
    rel["prat"] = rel.prat_total.astype(int)
    rel["dist"] = rel.county_of_commitment.map(DIST_OF)
    adm = pd.read_csv(j(C.F_ADM), dtype=str, keep_default_na=False)
    adm["t"] = pd.to_datetime(adm.movement_datetime.str[:10]).astype("datetime64[ns]")
    arr = pq.read_table(j(C.F_ARR)).to_pandas()
    arr["date"] = pd.to_datetime(arr.arrest_date).astype("datetime64[ns]")
    xw = pd.read_csv(j(C.F_XW), dtype=str)
    xw["sbi_no"] = xw.sbi.str.replace("-", "", regex=False)
    arr = arr.merge(xw[["sbi_no", "doc_number"]], on="sbi_no", how="left")
    arr["cls"] = arr.top_charge_grade.map(CLS)
    aoc = pd.read_csv(j(C.F_AOC), dtype=str, keep_default_na=False)
    aoc = aoc.sort_values(["docket_no", "entry_date"]).groupby("docket_no", as_index=False).tail(1)
    leg = pd.read_excel(j(C.F_BLEG), sheet_name=None, dtype=str)
    leg = pd.concat(leg.values(), ignore_index=True).fillna("")
    new = pd.read_csv(j(C.F_BNEW), dtype=str, keep_default_na=False)
    death = pd.read_csv(j(C.F_DEATH), dtype=str, keep_default_na=False)
    death = death[death.match_score.astype(int) >= 80]
    proj = pd.read_csv(j(C.F_PROJ), dtype=str, keep_default_na=False)
    proj["rd"] = pd.to_datetime(proj.projected_release_date).astype("datetime64[ns]")
    proj["birth"] = _mdy(proj.birth_date)
    proj["priors"] = proj.prior_commitments.astype(int)
    proj["prat"] = proj.prat_total.astype(int)
    proj["dist"] = proj.county_of_commitment.map(DIST_OF)
    return dict(rel=rel, adm=adm, arr=arr, aoc=aoc, leg=leg, new=new, death=death, proj=proj)


def features(df, at):
    """the obvious covariates at release: age, prior commitments, offence, sex, district"""
    out = pd.DataFrame(index=df.index)
    out["age"] = (df[at] - df.birth).dt.days / 365.25
    out["lp"] = np.log1p(df.priors)
    for o in ("PROPERTY", "DRUG", "PUBLIC ORDER"):
        out["off_" + o[:3]] = (df.governing_offense == o).astype(float)
    out["female"] = (df.sex == "F").astype(float)
    for d in C.DISTRICTS[1:]:
        out["d_" + d[:3]] = (df.dist == d).astype(float)
    return sm.add_constant(out, has_constant="add")


def custody(D):
    """custody intervals per person: from each admission to the next release movement"""
    a = D["adm"][D["adm"].movement_type == "ADM"][["doc_number", "t", "movement_reason"]].copy()
    r = D["rel"][["doc_number", "rd"]].sort_values("rd")
    a = a.sort_values("t")
    m = pd.merge_asof(a, r.rename(columns={"rd": "out"}), left_on="t", right_on="out", by="doc_number",
                      direction="forward", allow_exact_matches=False)
    m["out"] = m.out.fillna(pd.Timestamp("2099-01-01"))
    return m


def spells(D):
    """complete-follow-up releases to parole, each with its first admission within 730 days"""
    rel = D["rel"]
    s = rel[rel.code.isin(["PAR", "RPR"]) & (rel.rd <= COMPLETE_TO)].copy().reset_index(drop=True)
    a = D["adm"][D["adm"].movement_type == "ADM"][["doc_number", "t", "movement_reason"]].sort_values("t")
    s = s.sort_values("rd")
    m = pd.merge_asof(s, a.rename(columns={"t": "ft", "movement_reason": "fr"}), left_on="rd", right_on="ft",
                      by="doc_number", direction="forward", allow_exact_matches=False)
    m["fdays"] = (m.ft - m.rd).dt.days
    m.loc[m.ft.isna(), "fdays"] = np.inf
    dd = D["death"].assign(dod=pd.to_datetime(D["death"].date_of_death)).groupby("doc_number").dod.min()
    m["dod"] = m.doc_number.map(dd)
    return m.reset_index(drop=True)


# ---------------------------------------------------------------- the default path and its neighbours
def default_rates(D, S=None):
    S = spells(D) if S is None else S
    X = features(S, "rd")
    Xp = features(D["proj"], "rd")
    y_nc = ((S.fdays <= 730) & (S.fr == "NEW COMMITMENT")).astype(float)
    y_all = (S.fdays <= 730).astype(float)
    m1 = sm.Logit(y_nc, X).fit(disp=0)
    m0 = sm.Logit(y_all, X).fit(disp=0)
    p1 = m1.predict(Xp)
    p0 = m0.predict(Xp)
    # revocations treated as competing exits: cause-specific hazard of a new-commitment admission, by band
    rows = []
    for k, (lo, hi) in enumerate(BANDS):
        end = np.minimum(S.fdays.clip(upper=730), hi)
        ex = (end - lo).clip(lower=0)
        ev = ((S.fr == "NEW COMMITMENT") & (S.fdays >= lo) & (S.fdays < hi)).astype(float)
        keep = ex > 0
        rows.append(pd.DataFrame({"i": S.index[keep], "b": k, "ex": ex[keep], "y": ev[keep]}))
    pe = pd.concat(rows, ignore_index=True)
    XB = X.loc[pe.i].reset_index(drop=True)
    for k in range(1, 4):
        XB["b%d" % k] = (pe.b.values == k).astype(float)
    mb = sm.GLM(pe.y.values, XB, family=sm.families.Poisson(), offset=np.log(pe.ex.values)).fit()
    H = np.zeros(len(Xp))
    for k, (lo, hi) in enumerate(BANDS):
        Z = Xp.copy()
        for j in range(1, 4):
            Z["b%d" % j] = 1.0 if j == k else 0.0
        H += mb.predict(Z[XB.columns]).values * (hi - lo)
    p2 = 1 - np.exp(-H)
    return dict(R0=np.asarray(p0), R1=np.asarray(p1), R2=p2, auc_nc=_auc(m1.predict(X), y_nc), auc_all=_auc(m0.predict(X), y_all))


def _auc(score, y):
    s = np.asarray(score)
    y = np.asarray(y).astype(bool)
    order = np.argsort(s, kind="mergesort")
    ranks = np.empty(len(s))
    ranks[order] = np.arange(1, len(s) + 1)
    # average ranks for ties
    df = pd.DataFrame({"s": s, "r": ranks})
    ranks = df.groupby("s").r.transform("mean").values
    n1 = y.sum()
    n0 = len(y) - n1
    return float((ranks[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


# ---------------------------------------------------------------- the golden method
def board_revoked_otns(D):
    leg, new = D["leg"], D["new"]
    a = set(leg[(leg.action == "REVOKE") & (leg.arrest_otn != "")].arrest_otn)
    b = set(new[(new.decision == "REVOKED") & (new.arrest_otn != "")].arrest_otn)
    return a | b


def _days(x):
    return (pd.to_datetime(x).values.astype("datetime64[D]").astype(np.int64))


def liberty(D, S, until_first=False, only=None):
    """days at liberty and arrests in each band after each complete release (only: the arrest numbers to count)"""
    cu = custody(D)
    arr = D["arr"].dropna(subset=["doc_number"])
    if only is not None:
        arr = arr[arr.otn.isin(only)]
    cu = cu.assign(a=_days(cu.t), e=_days(cu.out))
    cu_g = {k: v[["a", "e"]].values for k, v in cu.groupby("doc_number")}
    ar_g = {k: np.sort(_days(v.date)) for k, v in arr.groupby("doc_number")}
    rd = _days(S.rd)
    dod = np.where(S.dod.notna(), _days(S.dod.fillna(pd.Timestamp("2099-01-01"))), 10 ** 9)
    fd = np.minimum(S.fdays.values, 730)
    rows = []
    for i, doc in enumerate(S.doc_number.values):
        sp = cu_g.get(doc, ())
        ad = ar_g.get(doc)
        for k, (lo, hi) in enumerate(BANDS):
            a = rd[i] + lo
            b = rd[i] + hi
            if until_first:
                b = min(b, rd[i] + int(fd[i]))
            b = min(b, dod[i])
            if b <= a:
                continue
            ex = b - a
            if not until_first:
                for s_, e_ in sp:
                    ov = min(b, e_) - max(a, s_)
                    if ov > 0:
                        ex -= ov
            n = 0 if ad is None else int(np.searchsorted(ad, b, "left") - np.searchsorted(ad, a, "left"))
            if ex > 0:
                rows.append((i, k, ex, n))
    return pd.DataFrame(rows, columns=["i", "b", "ex", "n"])


def arrest_model(D, S, pe, X=None, nbands=4):
    X = features(S, "rd") if X is None else X
    XB = X.iloc[pe.i.values].reset_index(drop=True)
    if nbands > 1:
        for k in range(1, nbands):
            XB["b%d" % k] = (pe.b.values == k).astype(float)
    m = sm.GLM(pe.n.values, XB, family=sm.families.Poisson(), offset=np.log(pe.ex.values)).fit()
    return m, list(XB.columns)


def lam_projected(D, m, cols, nbands=4, Xp=None):
    Xp = features(D["proj"], "rd") if Xp is None else Xp
    lam = np.zeros((len(Xp), nbands))
    for k in range(nbands):
        Z = Xp.copy()
        for j in range(1, nbands):
            Z["b%d" % j] = 1.0 if j == k else 0.0
        lam[:, k] = m.predict(Z[cols]).values
    return lam


def conversion(D, source="court"):
    """a court-routed arrest's chance of a sentence to Department custody, by class, and the arrest-to-admission
    lag of those that were, from arrests old enough for their cases to have closed"""
    arr = D["arr"].dropna(subset=["doc_number"])
    arr = arr[(arr.date <= CONV_TO)]
    aoc = D["aoc"][["otn", "disposition", "sentence_type", "sentence_date"]]
    x = arr.merge(aoc, on="otn", how="left")
    rev = board_revoked_otns(D)
    x = x[~x.otn.isin(rev)]
    if source == "off":
        rel = D["rel"][D["rel"].code.isin(["PAR", "RPR"])][["doc_number", "rd", "maxd"]].sort_values("rd")
        x = x.sort_values("date")
        y = pd.merge_asof(x, rel, left_on="date", right_on="rd", by="doc_number", direction="backward")
        x = y[~((y.date < y.maxd))].copy()
    x["doc"] = x.sentence_type == "DOC"
    pc = x.groupby("cls").doc.mean().to_dict()
    pooled = float(x.doc.mean())
    a = D["adm"][(D["adm"].movement_type == "ADM") & (D["adm"].movement_reason == "NEW COMMITMENT")][["doc_number", "t"]]
    s = x[x.doc].copy()
    s["sd"] = pd.to_datetime(s.sentence_date).astype("datetime64[ns]")
    s = s.sort_values("sd")
    a = a.sort_values("t")
    s = pd.merge_asof(s, a, left_on="sd", right_on="t", by="doc_number", direction="forward",
                      tolerance=pd.Timedelta(days=60))
    s = s.dropna(subset=["t"])
    s["lag"] = (s.t - s.date).dt.days
    lags = {c: np.sort(g.lag.values) for c, g in s.groupby("cls")}
    mix = arr.merge(D["rel"].drop_duplicates("doc_number")[["doc_number", "governing_offense"]], on="doc_number")
    mix = mix.groupby("governing_offense").cls.value_counts(normalize=True).unstack().fillna(0)
    return dict(pc=pc, pooled=pooled, lags=lags, mix=mix, n=len(x))


def conversion_evidence(D):
    """the counts behind the courts' conversion, in the write-up's terms: what became of the arrests the Board revoked
    on, the DOC sentences of the arrests it did not, the arrests made once the Board could no longer revoke (on or
    after the maximum date of the parole release before them), and every arrest with the revoked ones in"""
    x = D["arr"].dropna(subset=["doc_number"])
    x = x[x.date <= CONV_TO].merge(D["aoc"][["otn", "disposition", "sentence_type"]], on="otn", how="left")
    rev = board_revoked_otns(D)
    xr, xn = x[x.otn.isin(rev)], x[~x.otn.isin(rev)]
    doc = lambda t: int((t.sentence_type == "DOC").sum())
    by = lambda t: {c: [doc(t[t.cls == c]), int((t.cls == c).sum())] for c in ("F1", "F2", "M")}
    rel = D["rel"][D["rel"].code.isin(["PAR", "RPR"])][["doc_number", "rd", "maxd"]].sort_values("rd")
    y = pd.merge_asof(x.sort_values("date"), rel, left_on="date", right_on="rd", by="doc_number", direction="backward")
    off = y[y.maxd.notna() & (y.date >= y.maxd)]
    return dict(revoked=len(xr), revoked_np=int((xr.disposition == "NP").sum()), others=len(xn),
                others_np=int((xn.disposition == "NP").sum()), others_doc=doc(xn), others_by=by(xn),
                off=len(off), off_doc=doc(off), off_by=by(off), off_revoked=int(off.otn.isin(rev).sum()),
                every=len(x), every_doc=doc(x))


def project(D, lam, cv, edges=(90, 180, 365), pooled=False, frail=None, mix_overall=False):
    proj = D["proj"]
    ds = np.arange(C.WINDOW)
    bd = np.digitize(ds, edges) if len(edges) else np.zeros(C.WINDOW, int)
    L = lam[:, bd]
    F = {c: np.searchsorted(cv["lags"][c], C.WINDOW - ds, side="right") / len(cv["lags"][c]) for c in cv["lags"]}
    if pooled:
        alll = np.sort(np.concatenate(list(cv["lags"].values())))
        w = cv["pooled"] * np.searchsorted(alll, C.WINDOW - ds, side="right") / len(alll)
        W = np.tile(w, (len(proj), 1))
    else:
        if mix_overall:
            m = cv["mix"].mean()
            rows = np.tile(m.values, (len(proj), 1))
        else:
            rows = cv["mix"].reindex(proj.governing_offense).values
        cols = list(cv["mix"].columns)
        W = sum(rows[:, [j]] * cv["pc"][c] * F[c][None, :] for j, c in enumerate(cols))
    H = (L * W).sum(1)
    if frail is None:
        return 1 - np.exp(-H)
    return 1 - (1 + H / frail) ** (-frail)


def golden(D, S=None):
    S = spells(D) if S is None else S
    pe = liberty(D, S)
    m, cols = arrest_model(D, S, pe)
    lam = lam_projected(D, m, cols)
    cv = conversion(D)
    p = project(D, lam, cv)
    return dict(p=p, cv=cv, model=m, pe=pe, S=S, lam=lam)


def doc_bound_route(D, S):
    """the readers' route: the hazard of an arrest that ended in a sentence to the Department, per day at liberty,
    projected with the arrest-to-admission time; an arrest the Board revoked on never reached a sentence"""
    aoc = D["aoc"]
    only = set(aoc[aoc.sentence_type == "DOC"].otn)
    pe = liberty(D, S, only=only)
    m, cols = arrest_model(D, S, pe)
    lam = lam_projected(D, m, cols)
    cv = conversion(D)
    alll = np.sort(np.concatenate(list(cv["lags"].values())))
    ds = np.arange(C.WINDOW)
    F = np.searchsorted(alll, C.WINDOW - ds, side="right") / len(alll)
    L = lam[:, np.digitize(ds, (90, 180, 365))]
    return 1 - np.exp(-(L * F[None, :]).sum(1))


def crude_count_route(D, S, cv=None, court_only=True):
    """arrests counted over the 730 days after each release with no allowance for time in custody, each at the
    courts' conversion and timing (court_only=False: only the arrests that did end in a sentence to the Department,
    each counted as a return, the record's route)"""
    arr = D["arr"].dropna(subset=["doc_number"])
    if not court_only:
        aoc = D["aoc"]
        arr = arr[arr.otn.isin(set(aoc[aoc.sentence_type == "DOC"].otn))]
    g = {k: np.sort(_days(v.date)) for k, v in arr.groupby("doc_number")}
    rd = _days(S.rd)
    n = np.array([0 if doc not in g else int(np.searchsorted(g[doc], r + 730) - np.searchsorted(g[doc], r, "right"))
                  for doc, r in zip(S.doc_number.values, rd)])
    X = features(S, "rd")
    m = sm.GLM(n, X, family=sm.families.Poisson()).fit()
    lam = np.tile((m.predict(features(D["proj"], "rd")).values / 730.0)[:, None], (1, 4))
    cv = conversion(D) if cv is None else cv
    if not court_only:
        cv = dict(cv, pc={c: 1.0 for c in cv["pc"]})
    return project(D, lam, cv)


def exposure_routes(D, S, cv=None):
    """portal round 4's exposure readings, each sending every arrest the Board did not revoke on through the courts'
    DOC share by grade: the record's arrests over the 730 calendar days after each release (judge 2's calendar
    basis, with and without the arrest-to-admission time), the same scaled by each release's 730 days over its days
    out of Department custody, and the share scaled whole by 730 over the mean days out (no admission time)"""
    cv = conversion(D) if cv is None else cv
    arr = D["arr"].dropna(subset=["doc_number"])
    ga = {k: (_days(v.date), v.cls.values) for k, v in arr.groupby("doc_number")}
    cu = custody(D)
    cu = cu.assign(a=_days(cu.t), e=_days(cu.out))
    cu_g = {k: v[["a", "e"]].values for k, v in cu.groupby("doc_number")}
    rd = _days(S.rd)
    dod = np.where(S.dod.notna(), _days(S.dod.fillna(pd.Timestamp("2099-01-01"))), 10 ** 9)
    F = {c: (lambda L: (lambda rem: np.searchsorted(L, rem, side="right") / len(L)))(cv["lags"][c]) for c in cv["lags"]}
    H0, H1, out = np.zeros(len(S)), np.zeros(len(S)), np.zeros(len(S))
    for i, doc in enumerate(S.doc_number.values):
        r = rd[i]
        if doc in ga:
            d, c = ga[doc]
            m = (d > r) & (d <= r + 730)
            for dd, cc in zip(d[m], c[m]):
                if cc in cv["pc"]:
                    H0[i] += cv["pc"][cc]
                    H1[i] += cv["pc"][cc] * F[cc](r + 730 - dd)
        b = min(r + 730, dod[i])
        ex = b - r
        for s_, e_ in cu_g.get(doc, ()):
            ov = min(b, e_) - max(r, s_)
            if ov > 0:
                ex -= ov
        out[i] = max(ex, 1)
    cal = float(np.mean(1 - np.exp(-H0)))
    return dict(calendar=cal, calendar_lag=float(np.mean(1 - np.exp(-H1))),
                scaled_lag=float(np.mean(1 - np.exp(-H1 * 730 / out))),
                share_scaled=float((1 - np.exp(-H0.mean())) * 730 / out.mean()), days_out=float(out.mean()))


def nc_out_of_custody(D, S):
    """the record's new-commitment admissions per day out of Department custody, by band and on the covariates,
    over all 730 days: the default path read on the methodology's days out of custody"""
    cu = custody(D)
    cu = cu.assign(a=_days(cu.t), e=_days(cu.out))
    cu_g = {k: v[["a", "e"]].values for k, v in cu.groupby("doc_number")}
    nc = cu[cu.movement_reason == "NEW COMMITMENT"]
    nc_g = {k: np.sort(v.a.values) for k, v in nc.groupby("doc_number")}
    rd = _days(S.rd)
    dod = np.where(S.dod.notna(), _days(S.dod.fillna(pd.Timestamp("2099-01-01"))), 10 ** 9)
    rows = []
    for i, doc in enumerate(S.doc_number.values):
        sp, ad = cu_g.get(doc, ()), nc_g.get(doc)
        for k, (lo, hi) in enumerate(BANDS):
            a, b = rd[i] + lo, min(rd[i] + hi, dod[i])
            if b <= a:
                continue
            ex = b - a
            for s_, e_ in sp:
                ov = min(b, e_) - max(a, s_)
                if ov > 0:
                    ex -= ov
            n = 0 if ad is None else int(np.searchsorted(ad, b, "left") - np.searchsorted(ad, a + 1, "left"))
            if ex > 0:
                rows.append((i, k, ex, n))
    pe = pd.DataFrame(rows, columns=["i", "b", "ex", "n"])
    m, cols = arrest_model(D, S, pe)
    lam = lam_projected(D, m, cols)
    L = lam[:, np.digitize(np.arange(C.WINDOW), (90, 180, 365))]
    return 1 - np.exp(-L.sum(1))


def summarise(D, p):
    proj = D["proj"]
    out = {"all": float(np.mean(p))}
    for d in C.DISTRICTS:
        out[d] = float(np.mean(p[(proj.dist == d).values]))
    return out


def step5(v):
    return int(5 * round(100 * v / 5))


# ---------------------------------------------------------------- the PRAT study (distractor document)
def prat_study(target):
    D = load(target)
    rel = D["rel"]
    s = rel[rel.code.isin(["PAR", "RPR"]) & (rel.rd >= "2019-01-01") & (rel.rd <= "2020-12-31")].copy()
    a = D["adm"][(D["adm"].movement_type == "ADM") & (D["adm"].t <= "2023-03-31")][["doc_number", "t"]].sort_values("t")
    s = s.sort_values("rd")
    m = pd.merge_asof(s, a, left_on="rd", right_on="t", by="doc_number", direction="forward", allow_exact_matches=False)
    y = ((m.t - m.rd).dt.days <= 730).fillna(False).values
    lv = pd.cut(m.prat, [-1, 7, 12, 17, 24], labels=["Low", "Moderate", "High", "Very high"])
    levels = [(l, int((lv == l).sum()), float(y[(lv == l).values].mean())) for l in ["Low", "Moderate", "High", "Very high"]]
    return dict(n=len(m), auc=_auc(m.prat.values, y), levels=levels)


# ---------------------------------------------------------------- the asks
OFFICES = ("D1", "D2", "D3", "D4")
FY = (pd.Timestamp(C.FY_START), pd.Timestamp(C.FY_END))
QUARTERS = (("Q1", "2025-01-01", "2025-03-31"), ("Q2", "2025-04-01", "2025-06-30"),
            ("Q3", "2025-07-01", "2025-09-30"), ("Q4", "2025-10-01", "2025-12-31"))
MONTHS = [pd.Timestamp(2025, m, 1) for m in range(7, 13)] + [pd.Timestamp(2026, m, 1) for m in range(1, 7)]
JAIL_DIST = {c: d for d, cs in C.COUNTIES.items() for c in cs}


def _ts(x, **kw):
    return pd.to_datetime(x, errors="coerce").astype("datetime64[ns]")


def _board(D):
    leg = D["leg"].copy()
    leg["ad"] = _ts(leg.action_date)
    leg["rep"] = _ts(leg.report_date)
    new = D["new"].copy()
    new["dd"] = _ts(new.decision_ts.str[:10], errors="coerce")
    new["rep"] = _ts(new.report_date, errors="coerce")
    return leg, new


def _key(t):
    return t.doc_number + "|" + t.rep.dt.strftime("%Y-%m-%d")


def revocations(D, dedupe=True, rescind=True, orders=True, rescind_by=FY[1], level="event", parallel="match"):
    """the Board's recommitments ordered in fiscal 2025-26: one per parolee per hearing, with its office, whether any
    report it took up was of an arrest, and the decision date (level "event": a rescission sets aside the case's
    latest order on or before it, "case": every order on a case with a rescission; parallel "match": a legacy entry
    after the close is dropped where the new system holds the carried-over case's decision, "date": every one)"""
    leg, new = _board(D)
    close = pd.Timestamp(C.BOARD_MIGRATE_CUT)
    L = leg[(leg.action == "REVOKE") & (leg.ad >= FY[0]) & (leg.ad <= FY[1])].copy()
    if dedupe:
        late = L.ad > close
        if parallel == "match":
            decided = set(_key(new[(new.opened_in == "LEGACY") & (new.decision != "")]))
            late &= _key(L).isin(decided)
        L = L[~late]
    if rescind:
        R_ = leg[(leg.action == "RESCIND") & (leg.ad <= rescind_by)]
        if level == "case":
            L = L[~L.case_no.isin(set(R_.case_no))]
        else:
            orders_ = leg[leg.action == "REVOKE"][["case_no", "ad"]]
            gone = set()
            for case, rd_ in zip(R_.case_no, R_.ad):
                o = orders_[(orders_.case_no == case) & (orders_.ad <= rd_)]
                if len(o):
                    gone.add((case, o.ad.max()))
            L = L[[(c, a) not in gone for c, a in zip(L.case_no, L.ad)]]
    N = new[(new.decision == "REVOKED") & (new.dd >= FY[0]) & (new.dd <= FY[1])].copy()
    if rescind:
        rd = _ts(N.rescinded_date)
        N = N[~(rd <= rescind_by)]
    out = pd.concat([pd.DataFrame({"doc": L.doc_number, "office": L.office, "arrest": L.arrest_otn != "", "d": L.ad}),
                     pd.DataFrame({"doc": N.doc_number, "office": N.office, "arrest": N.arrest_otn != "", "d": N.dd})],
                    ignore_index=True)
    if orders:
        out = out.groupby(["doc", "d"], as_index=False).agg(office=("office", "first"), arrest=("arrest", "max"))
    return out


def board_devices(D):
    """the counts the write-up states for the Board's records: legacy cases heard again after a rescission (REVOKE,
    RESCIND, REVOKE), and carried-over detainers the new system re-issued at its go-live with the legacy lodge dates
    they replaced"""
    leg, new = _board(D)
    acts = leg[leg.action.isin(["REVOKE", "RESCIND"])].sort_values(["case_no", "ad"])
    seqs = acts.groupby("case_no").action.apply(tuple)
    rehear = int((seqs == ("REVOKE", "RESCIND", "REVOKE")).sum())
    cn = new[(new.opened_in == "LEGACY") & (new.hold_start == C.BOARD_GOLIVE.isoformat())]
    lg = leg[leg.hold_lodged != ""]
    lodge = pd.to_datetime(lg.assign(k=_key(lg)).groupby("k").hold_lodged.min())
    lk = _key(cn).map(lodge)
    return dict(rehear=rehear, reissued=len(cn), lodge_from=lk.min().date(), lodge_to=lk.max().date())


def ask_a(D, **kw):
    r = revocations(D, **kw)
    res = {}
    for o in OFFICES:
        x = r[r.office == o]
        res[o] = {"arrest": int(x.arrest.sum()), "conditions": int((~x.arrest).sum())}
    return res


def ask_chart(D, **kw):
    b = ask_b(D, **kw)
    return {d: sum(b[d].values()) for d in C.DISTRICTS}


def holds(D, blank="admission", dedupe=True, case=None, migr=None, clip=False, carry="legacy"):
    """the Board's detainers as intervals [start, end): legacy and new systems, one interval per hold (clip: each also
    ended at the person's next Department admission, the physical exit, where that comes before the recorded end;
    carry "legacy": a carried-over case's detainer runs from its lodge day in the legacy table, the new system having
    re-issued it at go-live, "new": from the new system's date)"""
    leg, new = _board(D)
    close = pd.Timestamp(C.BOARD_MIGRATE_CUT)
    L = leg[leg.hold_lodged != ""].copy()
    L["s"] = _ts(L.hold_lodged, errors="coerce")
    lodged = L.assign(k=_key(L)).groupby("k").s.min()
    L["e"] = _ts(L.hold_lifted, errors="coerce")
    L["jail"] = L.hold_facility.str.replace(" CJ", "", regex=False)
    case = dedupe if case is None else case
    migr = dedupe if migr is None else migr
    if case:
        # one detainer per case: every action row of a legacy case repeats its detainer columns
        L = L.sort_values(["case_no", "ad"]).drop_duplicates(["case_no", "hold_lodged"], keep="last")
    if migr:
        # a case open when the legacy system closed was carried into the new system with its hold
        moved = set(new[new.opened_in == "LEGACY"].doc_number + "|" + new[new.opened_in == "LEGACY"].report_date)
        key = L.doc_number + "|" + L.rep.dt.strftime("%Y-%m-%d")
        L = L[~key.isin(moved)]
    blank_rows = L.e.isna()
    if blank == "admission":
        a = D["adm"][D["adm"].movement_type == "ADM"][["doc_number", "t"]].sort_values("t")
        q = L[blank_rows].assign(_ix=L.index[blank_rows]).sort_values("s")
        q = pd.merge_asof(q, a, left_on="s", right_on="t", by="doc_number", direction="forward")
        L.loc[q._ix.values, "e"] = q.t.values
    elif blank == "action":
        L.loc[blank_rows, "e"] = L.loc[blank_rows, "ad"]
    elif blank == "extract":
        L.loc[blank_rows, "e"] = pd.Timestamp(C.CUT)
    elif blank == "drop":
        L = L[~blank_rows]
    N = new[new.hold_start != ""].copy()
    N["s"] = _ts(N.hold_start)
    if carry == "legacy":
        k = _key(N)
        was = (N.opened_in == "LEGACY") & k.isin(lodged.index)
        N.loc[was, "s"] = k[was].map(lodged).values
    N["e"] = _ts(N.hold_end, errors="coerce").fillna(pd.Timestamp(C.CUT) + pd.Timedelta(days=1))
    N["jail"] = N.hold_facility.str.replace(" County Jail", "", regex=False)
    out = pd.concat([L[["doc_number", "jail", "s", "e"]], N[["doc_number", "jail", "s", "e"]]], ignore_index=True)
    out = out.dropna(subset=["s", "e"])
    if clip:
        a = D["adm"][D["adm"].movement_type == "ADM"][["doc_number", "t"]].sort_values("t")
        q = pd.merge_asof(out.assign(_ix=out.index).sort_values("s"), a, left_on="s", right_on="t", by="doc_number",
                          direction="forward")
        hit = q.t.notna() & (q.t < q.e)
        out.loc[q._ix[hit].values, "e"] = q.t[hit].values
    out["dist"] = out.jail.map(JAIL_DIST)
    return out


def _union(h):
    """merge each parolee's overlapping detainer intervals in one district"""
    out = []
    for (doc, dist), g in h.sort_values("s").groupby(["doc_number", "dist"]):
        cs, ce = None, None
        for s, e in zip(g.s, g.e):
            if cs is None:
                cs, ce = s, e
            elif s <= ce:
                ce = max(ce, e)
            else:
                out.append((doc, dist, cs, ce))
                cs, ce = s, e
        out.append((doc, dist, cs, ce))
    return pd.DataFrame(out, columns=["doc_number", "dist", "s", "e"])


HALVES = (("H1", "2025-01-01", "2025-06-30"), ("H2", "2025-07-01", "2025-12-31"))


def ask_b(D, both_days=False, union=True, periods=None, **kw):
    h = holds(D, **kw)
    if union:
        h = _union(h)
    res = {}
    for d in C.DISTRICTS:
        x = h[h.dist == d]
        row = {}
        for q, a, b in (periods or HALVES):
            a, b = pd.Timestamp(a), pd.Timestamp(b) + pd.Timedelta(days=1)
            end = x.e + (pd.Timedelta(days=1) if both_days else pd.Timedelta(0))
            ov = (end.clip(upper=b) - x.s.clip(lower=a)).dt.days.clip(lower=0)
            row[q] = int(ov.sum())
        res[d] = row
    return res


INSTITUTIONS = C.FACILITIES


def writ_trips(D, ended_by_release=True):
    """each trip out on a court writ: the institution left, the day out and the day back (a WRI, or the release
    movement for a person the court released)"""
    m = D["adm"][D["adm"].movement_type.isin(["WRO", "WRI", "ADM", "TRN"])][["doc_number", "t", "movement_type", "location"]]
    r = D["rel"][["doc_number", "rd"]].rename(columns={"rd": "t"}).assign(movement_type="REL", location="")
    ev = pd.concat([m, r], ignore_index=True)
    ev["k"] = ev.movement_type.map({"REL": 0, "ADM": 1, "TRN": 2, "WRI": 3, "WRO": 4})
    ev = ev.sort_values(["doc_number", "t", "k"])
    trips = []
    for doc, g in ev.groupby("doc_number", sort=False):
        open_ = None
        for t, mt, loc in zip(g.t, g.movement_type, g.location):
            if mt == "WRO":
                open_ = (t, loc)
            elif open_ is not None and (mt == "WRI" or (mt == "REL" and ended_by_release)):
                trips.append((doc, open_[1], open_[0], t))
                open_ = None
    return pd.DataFrame(trips, columns=["doc_number", "inst", "s", "e"])


def ask_c(D, **kw):
    w = writ_trips(D, **kw)
    res = {}
    for inst in INSTITUTIONS:
        x = w[w.inst == inst]
        row = {}
        for h, a, b in HALVES:
            a, b = pd.Timestamp(a), pd.Timestamp(b) + pd.Timedelta(days=1)
            row[h] = int((x.e.clip(upper=b) - x.s.clip(lower=a)).dt.days.clip(lower=0).sum())
        res[inst] = row
    return res
