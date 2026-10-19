"""task249's golden, computed from the shipped folder only.

Main call: each client account's share of its genuine shortlisted candidates the MAL-IS-04 section 3.2 check would
refer in the 2029 season, on the account's 2029 plan and an applicant pool like its 2028 one. Built through the
measurement model the files describe: a 2029 applicant's ability drawn from the account's 2028 pool (the 2028
scores with their standard errors taken out), the MAT-R estimate as ability plus the test's error at that ability
(Table 4.3), the shortlist the top of the account's applicants on MAT-R, MAT-V as ability plus the retest gain at
the selection day's interval (the equivalence study) plus MAT-V's error, and the referral rule as the platform
applies it. The lower rungs are kept beside it for the checks: the study's rates carried by interval, the model
without the retest gain, the model with one standard error for every ability."""
import datetime as dt
import os
import re
import numpy as np
import pandas as pd
import params as P

GRID = np.round(np.arange(-3.0, 3.01, 0.25), 2)
SIM_N = 1_200_000


def load(tgt, files):
    p = lambda k: os.path.join(tgt, files[k])
    att = pd.read_parquet(p("attempts"))
    reg = pd.read_csv(p("register"))
    shares = pd.read_csv(p("shares"))
    study = pd.read_csv(p("study"))
    plans = pd.read_excel(p("plans"), sheet_name="2029 plans", header=4)
    cols = pd.read_csv(p("colleges"))
    accts = pd.read_csv(p("accounts"))
    return dict(att=att, reg=reg, shares=shares, study=study, plans=plans, cols=cols, accts=accts)


# ------------------------------------------------------------------ Table 4.3 (the manual), as the solver reads it
def se_table():
    """the manual's Table 4.3 values; interpolated between tabled points"""
    u = np.array([round(float(P.se_online(t)), 3) for t in GRID])
    v = np.array([round(float(P.se_verify(t)), 3) for t in GRID])
    return u, v


def interp(t, tab):
    return np.interp(np.clip(t, GRID[0], GRID[-1]), GRID, tab)


# ------------------------------------------------------------------ the retest gain, from the study's pairs
def retest(study):
    d = study.dropna(subset=["mat_v_logit"]).copy()
    d["days"] = (pd.to_datetime(d["mat_v_started_ist"]).dt.normalize() - pd.to_datetime(d["mat_r_started_ist"]).dt.normalize()).dt.days
    d["gain"] = d["mat_v_logit"] - d["mat_r_logit"]
    by = d.groupby("days")["gain"].agg(["mean", "size"])
    # exponential fade fitted by least squares on the interval means (weights: pairs)
    x = by.index.values.astype(float)
    y = by["mean"].values
    wts = by["size"].values.astype(float)
    best = None
    for tau in np.arange(4.0, 60.01, 0.25):
        X = np.column_stack([np.ones_like(x), np.exp(-x / tau)])
        W = np.diag(wts)
        beta = np.linalg.solve(X.T @ W @ X, X.T @ W @ y)
        sse = float(((y - X @ beta) ** 2 * wts).sum())
        if best is None or sse < best[0]:
            best = (sse, tau, beta)
    _, tau, beta = best
    return dict(c=float(beta[0]), a=float(beta[1]), tau=float(tau), table=by, pairs=d)


def gain_fn(rt):
    return lambda g: rt["c"] + rt["a"] * np.exp(-np.asarray(g, float) / rt["tau"])


# ------------------------------------------------------------------ pools, plans and timing
def pools(L):
    """each 2029 account's 2028 applicant pool: the candidates whose result was shared with it (PGL folded into NVK,
    the 14 August re-send and withdrawals not changing who applied), at their completed MAT-R estimate"""
    reg = set(L["reg"]["candidate_id"])
    att = L["att"]
    comp = att[(att["attempt_status"] == "completed") & att["candidate_id"].isin(reg)]
    est = comp.set_index("candidate_id")[["theta_logit", "se_logit"]]
    sh = L["shares"].copy()
    sh["account_code"] = sh["account_code"].replace({"PGL": "NVK"})
    sh = sh[sh["account_code"].isin([a[0] for a in P.ACCOUNTS])]
    out = {}
    for code, g in sh.groupby("account_code"):
        c = g["candidate_id"] if L.get("keep_dupes") else g["candidate_id"].drop_duplicates()
        e = est.reindex(c).dropna()
        out[code] = e
    return out


def plan_rows(L):
    pl = L["plans"].dropna(subset=["Code"]).copy()
    pl = pl[pl["Code"].isin([a[0] for a in P.ACCOUNTS])]
    return pl.set_index("Code")


def gaps_for(row, rng, n, col_weeks):
    """days from the 2029 MAT-R sitting (day 1 or day 2 of a July test week) to the account's selection day"""
    fmt = row["Selection format"]
    if fmt in ("Day-one campus drive", "First-company campus drive"):
        return np.where(rng.random(n) < 0.0, 1, 2)
    m = re.search(r"(\d{1,2} \w+ 2029) to (\d{1,2} \w+ 2029)", str(row["Selection days"]))
    d0 = dt.datetime.strptime(m.group(1), "%d %B %Y").date()
    d1 = dt.datetime.strptime(m.group(2), "%d %B %Y").date()
    sel = np.array([d0 + dt.timedelta(days=int(k)) for k in rng.integers(0, (d1 - d0).days + 1, n)])
    wk = rng.choice(col_weeks, n)
    sit = np.array([w + dt.timedelta(days=int(k)) for w, k in zip(wk, rng.integers(0, 2, n))])
    return np.array([(a - b).days for a, b in zip(sel, sit)])


def rate(pool, q, gaps, rng, gain, seu, sev, deconv=True, with_gain=True, const_se=None, n=SIM_N):
    """share of genuine shortlisted candidates referred under section 3.2"""
    e, s = pool["theta_logit"].values, pool["se_logit"].values
    if deconv:
        mu = e.mean()
        tau = np.sqrt(max(e.var() - np.mean(s ** 2), 0.01))
        th = rng.normal(mu, tau, n)
    else:
        th = rng.choice(e, n, replace=True)
    su = interp(th, seu) if const_se is None else np.full(n, const_se)
    U = th + rng.normal(0, 1, n) * su
    cut = np.quantile(U, 1 - q)
    sel = U >= cut
    g = rng.choice(gaps, n)
    V = th + (gain(g) if with_gain else 0.0) + rng.normal(0, 1, n) * interp(th, sev)
    sv = interp(V, sev)
    ref = U > V + P.BAND_Z * sv
    return float(ref[sel].mean())


TH = np.linspace(-4.0, 5.0, 901)


def kelley(pool, q, gaps, rng, gain, seu, sev, se_at="ability", draws=300):
    """the account's top share of its own 2028 pool on MAT-R, each candidate's ability read by true-score shrinkage
    toward the pool (prior: the pool's mean and its variance less the mean squared standard error), MAT-V drawn
    from that ability, and the share the section 3.2 rule refers. se_at: 'reported' takes each candidate's own
    standard error (the error at the estimate); 'ability' reads Table 4.3 at the shrunken ability, iterated;
    'posterior' takes the full posterior on a grid with Table 4.3's error at each ability"""
    e, s = pool["theta_logit"].values, pool["se_logit"].values
    mu = e.mean()
    tau2 = max(e.var() - np.mean(s ** 2), 0.01)
    k = max(1, int(round(q * len(e))))
    ee = e[np.argsort(-e, kind="stable")[:k]]
    if se_at == "posterior":
        su = interp(TH, seu)
        lp = -(TH - mu) ** 2 / (2 * tau2)
        th = np.empty((k, draws))
        for lo in range(0, k, 2000):
            blk = ee[lo:lo + 2000]
            ll = lp[None, :] - (blk[:, None] - TH[None, :]) ** 2 / (2 * su[None, :] ** 2) - np.log(su)[None, :]
            post = np.exp(ll - ll.max(1, keepdims=True))
            cdf = np.cumsum(post, 1)
            cdf /= cdf[:, -1:]
            u = rng.random((len(blk), draws))
            th[lo:lo + 2000] = np.array([np.interp(u[j], cdf[j], TH) for j in range(len(blk))])
    else:
        if se_at == "reported":
            ss = s[np.argsort(-e, kind="stable")[:k]]
            m = mu + tau2 / (tau2 + ss ** 2) * (ee - mu)
        else:
            m = ee.copy()
            for _ in range(50):
                ss = interp(m, seu)
                m = mu + tau2 / (tau2 + ss ** 2) * (ee - mu)
        v = tau2 * ss ** 2 / (tau2 + ss ** 2)
        th = m[:, None] + np.sqrt(v)[:, None] * rng.normal(0, 1, (k, draws))
    g = rng.choice(gaps, (k, draws))
    V = th + gain(g) + rng.normal(0, 1, (k, draws)) * interp(th, sev)
    return float((ee[:, None] > V + P.BAND_Z * interp(V, sev)).mean())


def study_regression(pool, q, gaps, gain, sev, fit):
    """the study's own regression of MAT-V (less the retest gain) on MAT-R, carried to the account's top share of its
    2028 pool: the share referred under section 3.2"""
    from scipy.stats import norm
    alpha, beta, sig = fit
    e = pool["theta_logit"].values
    top = np.sort(e)[::-1][:max(1, int(round(q * len(e))))]
    v = np.linspace(-5.0, 7.0, 4801)
    vstar = np.interp(top, v + P.BAND_Z * interp(v, sev), v)
    gu, gw = np.unique(gaps, return_counts=True)
    p = sum(w * norm.cdf((vstar - (alpha + beta * top + gain(g))) / sig) for g, w in zip(gu, gw)) / gw.sum()
    return float(p.mean())


def shrinkage_check(rt):
    """the study's top tenth of MAT-R scorers: the mean MAT-V they scored, and the mean predicted by true-score
    shrinkage with the error read at the shrunken ability (Table 4.3) and at each volunteer's reported error"""
    seu, sev = se_table()
    d = rt["pairs"]
    e, s = d["mat_r_logit"].values, d["mat_r_se"].values
    mu = e.mean()
    tau2 = e.var() - np.mean(s ** 2)
    k = int(round(0.1 * len(d)))
    idx = np.argsort(-e, kind="stable")[:k]
    g = gain_fn(rt)(d["days"].values[idx])
    m = e[idx].copy()
    for _ in range(50):
        m = mu + tau2 / (tau2 + interp(m, seu) ** 2) * (e[idx] - mu)
    mk = mu + tau2 / (tau2 + s[idx] ** 2) * (e[idx] - mu)
    return dict(n=k, scored=float(d["mat_v_logit"].values[idx].mean()), at_ability=float((m + g).mean()),
                at_reported=float((mk + g).mean()))


def main_call(L, files=None, seed=P.SEED + 101, extra=False):
    seu, sev = se_table()
    rt = retest(L["study"])
    gain = gain_fn(rt)
    pl = plan_rows(L)
    po = pools(L)
    cw = [dt.date(2029, 7, 2), dt.date(2029, 7, 9), dt.date(2029, 7, 16), dt.date(2029, 7, 23)]
    pr = rt["pairs"]
    vv = pr["mat_v_logit"].values - gain(pr["days"].values)
    beta, alpha = np.polyfit(pr["mat_r_logit"].values, vv, 1)
    sfit = (alpha, beta, float(np.std(vv - alpha - beta * pr["mat_r_logit"].values, ddof=2)))
    rows = []
    for code, *_ in P.ACCOUNTS:
        row = pl.loc[code]
        q = float(row["Shortlist"]) / float(row["Expected applicants"])
        rng = np.random.default_rng(seed + sum(map(ord, code)))
        gaps = gaps_for(row, rng, 4000, cw)
        r = {}
        r["gold"] = rate(po[code], q, gaps, np.random.default_rng(seed + 1 + sum(map(ord, code))), gain, seu, sev)
        r["emp_pool"] = rate(po[code], q, gaps, np.random.default_rng(seed + 2 + sum(map(ord, code))), gain, seu, sev, deconv=False)
        r["no_gain"] = rate(po[code], q, gaps, np.random.default_rng(seed + 3 + sum(map(ord, code))), gain, seu, sev, with_gain=False)
        r["const_se"] = rate(po[code], q, gaps, np.random.default_rng(seed + 4 + sum(map(ord, code))), gain, seu, sev, const_se=0.38)
        r["study_reg"] = study_regression(po[code], q, gaps, gain, sev, sfit)
        r["kelley_reported"] = kelley(po[code], q, gaps, np.random.default_rng(seed + 5 + sum(map(ord, code))), gain, seu, sev, se_at="reported")
        if extra:
            r["kelley_ability"] = kelley(po[code], q, gaps, np.random.default_rng(seed + 6 + sum(map(ord, code))), gain, seu, sev, se_at="ability")
            r["posterior"] = kelley(po[code], q, gaps, np.random.default_rng(seed + 7 + sum(map(ord, code))), gain, seu, sev, se_at="posterior")
        rows.append(dict(code=code, client=row["Client"], fmt=row["Selection format"], expected=int(row["Expected applicants"]),
                         shortlist=int(row["Shortlist"]), depth=q, pool_n=len(po[code]),
                         pool_mu=float(po[code]["theta_logit"].mean()), mean_gap=float(np.mean(gaps)),
                         gain_at=float(np.mean(gain(gaps))), **r))
    df = pd.DataFrame(rows)
    df["flag"] = df["gold"] > P.CAP
    # the study's own rates by interval band, carried to each account (the default path)
    d = rt["pairs"]
    d = d.assign(ref=d["mat_r_logit"] > d["mat_v_logit"] + P.BAND_Z * d["mat_v_se"])
    short = float(d[d["days"] <= 3]["ref"].mean())
    long_ = float(d[d["days"] >= 42]["ref"].mean())
    df["study_rate"] = np.where(df["fmt"].isin(["Day-one campus drive", "First-company campus drive"]), short, long_)
    return df, rt, dict(study_short=short, study_long=long_)


# ------------------------------------------------------------------ the asks
def ask_exposure(tgt, files, ceiling=0.12):
    att = pd.read_parquet(os.path.join(tgt, files["attempts"]))
    ex = pd.read_parquet(os.path.join(tgt, files["exposure"]))
    reg = set(pd.read_csv(os.path.join(tgt, files["register"]))["candidate_id"])
    att = att[att["candidate_id"].isin(reg)].copy()
    t = pd.to_datetime(att["started_utc"]) + pd.Timedelta(hours=5, minutes=30)
    att["week"] = (t.dt.normalize() - pd.Timestamp("2028-07-03")).dt.days // 7
    e = ex.merge(att[["booking_ref", "attempt_no", "candidate_id", "week"]], on=["booking_ref", "attempt_no"])
    out, rested = [], set()
    for k in range(4):
        a = att[att["week"] == k]
        den = a["candidate_id"].nunique()
        num = e[e["week"] == k].groupby("item_id")["candidate_id"].nunique()
        x = num / den
        rested |= set(x.index[x > ceiling])
        out.append(dict(week=k, candidates=den, over=int((x > ceiling).sum()), top=float(x.max()), top_item=str(x.idxmax()),
                        nearest=float((x - ceiling).abs().min())))
    for o in out:
        o["rested_2029"] = len(rested)
    return out


def ask_impersonation(tgt, files):
    cases = pd.read_excel(os.path.join(tgt, files["cases"]), sheet_name="Case log")
    sl = pd.read_csv(os.path.join(tgt, files["shortlists"]))
    reg = pd.read_csv(os.path.join(tgt, files["register"])).set_index("candidate_id")["college_code"]
    tier = pd.read_csv(os.path.join(tgt, files["colleges"])).set_index("college_code")["tier"]
    # a candidate sits once a season (MAL-IS-04 s.2), so a sitting's standing is the latest decision on any of the
    # candidate's cases, the desk's appeal cases included
    last = cases.sort_values(["candidate_id", "decided", "case_ref"], kind="stable").groupby("candidate_id").tail(1)
    conf = last[last["finding"].isin(["confirmed impersonation", "confirmed on appeal"])].copy()
    conf["tier"] = conf["candidate_id"].map(reg).map(tier)
    sl["tier"] = sl["candidate_id"].map(reg).map(tier)
    n = conf.groupby("tier")["candidate_id"].nunique()
    den = sl.groupby("tier")["candidate_id"].nunique()
    return [dict(tier=t, confirmed=int(n.get(t, 0)), shortlisted=int(den[t]), per_thousand=1000 * n.get(t, 0) / den[t])
            for t in ("T1", "T2", "T3", "T4")]


def ask_interrupted(tgt, files):
    """one booking a candidate a season (MAL-IS-04 s.2): a candidate's attempts in time order are that booking's"""
    att = pd.read_parquet(os.path.join(tgt, files["attempts"]))
    reg = set(pd.read_csv(os.path.join(tgt, files["register"]))["candidate_id"])
    att = att[att["candidate_id"].isin(reg)].sort_values(["candidate_id", "started_utc"], kind="stable")
    first = att.groupby("candidate_id").head(1).set_index("candidate_id")
    last = att.groupby("candidate_id").tail(1).set_index("candidate_id")
    inter = att[att["attempt_status"] == "interrupted"].set_index("candidate_id")
    out = []
    for dev in ("desktop", "laptop", "tablet"):
        started = first[first["device"] == dev]
        k = inter[inter["device"] == dev]
        moved = int((last["device"].reindex(k.index) != dev).sum())
        out.append(dict(device=dev, bookings=len(started), interrupted=len(k), share=100.0 * len(k) / len(started),
                        moved=moved))
    return out
