"""Screens for candidate G1 on the clean truth. One summary line per screen.
usage: python3 screens.py N_SEEDS [key=value ...]   (key=value override world parameters)"""
import sys, json, numpy as np, pandas as pd
from scipy import stats
from world3 import make, LIMIT, WIN0, WIN1
UNIT = {"C": "cell", "N2": "cell", "D": "basin", "D2": "basin", "D3": "basin", "N1": "basin", "F2": "pond", "N3": "pond",
        "R": "yard", "N4": "yard", "UG-1": "upgradient", "UG-2": "upgradient", "none": "none", "tie": "tie"}

def inwin(d): return (d >= WIN0) & (d <= WIN1)

def golden(S, Lv, mode="prev", ndays=None, src="logger", start=None, look=None):
    """unexplained window exceedances per well: an exceedance is explained when the well's water level
    rose above every earlier level (since `start`, or over the `look` days before) between the previous
    sample and this one (mode prev), or in the `ndays` before the sample (mode n), or stood at or above
    the earlier maximum on the sample day (mode at)."""
    out = {}
    for w, g in S.groupby("well"):
        g = g.sort_values("date").reset_index(drop=True)
        L = Lv[w] if start is None else Lv[w][Lv.index >= pd.Timestamp(start)]
        rm = L.cummax(); man = g.level.cummax().values
        ex = un = 0
        for i in range(len(g)):
            r = g.iloc[i]
            if not inwin(r.date) or r.boron <= LIMIT: continue
            ex += 1
            if r.date < L.index[0]: continue
            t0 = (g.date[i - 1] if i > 0 else L.index[0]) if mode in ("prev", "at") else r.date - pd.Timedelta(days=ndays)
            if src == "manual":
                rose = r.level > (man[i - 1] if i > 0 else -1e9)
            elif look:
                ref = Lv[w].loc[t0 - pd.Timedelta(days=look): t0].max()
                rose = Lv[w].loc[t0: r.date].max() > ref
            elif mode == "at":
                before = L.loc[:t0]; rose = L.loc[r.date] >= (before.max() if len(before) else -1e9)
            else:
                before = rm.loc[:t0]; prior = before.iloc[-1] if len(before) else -1e9
                rose = rm.loc[r.date] > prior
            if not rose: un += 1
        out[w] = (ex, un)
    return out

def pick(d):  # d: well -> score; sums scores by site and returns a well of the top site, or 'none'
    u = {}
    for w, v in d.items():
        k = UNIT.get(w, w)
        if k == "upgradient": continue
        u[k] = u.get(k, 0) + (v if v > 0 else 0)
    if not u or max(u.values()) <= 0: return "none"
    best = max(u, key=u.get)
    if sorted(u.values())[-1] == sorted(u.values())[-2] if len(u) > 1 else False: return "tie"
    return [w for w in d if UNIT.get(w) == best][0]

def sen(x, y):
    if len(x) < 3: return 0.0
    return stats.theilslopes(y, x)[0]

def readers(S, Lv):
    R = {}
    W = S[inwin(S.date)]
    exc = W.assign(e=W.boron > LIMIT).groupby("well").e.sum().to_dict()
    R["first_look_count"] = pick(exc)
    R["max_conc"] = W.groupby("well").boron.max().idxmax()
    R["mean_conc"] = W.groupby("well").boron.mean().idxmax()
    # rung 0: Mann-Kendall / Sen slope over the window, wells with an exceedance
    sl = {}
    for w, g in W.groupby("well"):
        x = (g.date - WIN0).dt.days.values; tau_, p_ = stats.kendalltau(x, g.boron.values)
        sl[w] = sen(x, g.boron.values) if (exc.get(w, 0) and tau_ > 0 and p_ < 0.05) else -1e9
    R["sen_slope_window"] = max(sl, key=sl.get) if max(sl.values()) > -1e9 else "none"
    sl2 = {}
    for w, g in S[S.date >= "2020-01-01"].groupby("well"):
        x = (g.date - WIN0).dt.days.values; tau_, p_ = stats.kendalltau(x, g.boron.values)
        sl2[w] = sen(x, g.boron.values) if (exc.get(w, 0) and tau_ > 0 and p_ < 0.05) else -1e9
    R["sen_slope_2020on"] = max(sl2, key=sl2.get) if max(sl2.values()) > -1e9 else "none"
    # intrawell prediction limit on each well's first 8 samples (log scale, k=2.6)
    intra = {}
    for w, g in S.groupby("well"):
        g = g.sort_values("date"); b = np.log(g.boron.values[:8])
        pl = np.exp(b.mean() + 2.6 * b.std(ddof=1))
        gw = g[inwin(g.date)]; intra[w] = int(((gw.boron > pl) & (gw.boron > LIMIT)).sum())
    R["intrawell_PL"] = pick(intra)
    intra2 = {}
    for w, g in S.groupby("well"):
        g = g.sort_values("date"); b = np.log(g.boron.values[:8])
        pl = np.exp(b.mean() + 2.6 * b.std(ddof=1))
        gw = g[inwin(g.date)]; intra2[w] = int((gw.boron > pl).sum())
    R["intrawell_PL_any"] = pick(intra2)
    # interwell against pooled upgradient
    ub = np.log(S[S.well.str.startswith("UG")].boron.values)
    plu = np.exp(ub.mean() + 2.6 * ub.std(ddof=1))
    inter = W.assign(e=W.boron > plu).groupby("well").e.sum()
    inter = inter[~inter.index.str.startswith("UG")].to_dict()
    R["interwell_PL"] = pick(inter)
    # level-correlation reader: wells whose boron rises with level are 'mobilisation'
    keep = {}
    for w, g in S.groupby("well"):
        rho, p = stats.spearmanr(g.level, g.boron)
        keep[w] = exc.get(w, 0) if not (rho > 0 and p < 0.05) else 0
    R["level_corr_discount"] = pick(keep)
    # naive mobilisation: discount exceedances at high water (top p of the well's logger record)
    for q in (0.75, 0.90, 0.95, 0.98):
        rem = {}
        for w, g in W.groupby("well"):
            thr = np.quantile(Lv[w].values, q)
            rem[w] = int(((g.boron > LIMIT) & (g.level < thr)).sum())
        R[f"pct_discount_{int(q*100)}"] = pick(rem)
    # rising-limb reader: discount exceedances where level rose since previous sample
    rem = {}
    for w, g in S.groupby("well"):
        g = g.sort_values("date").reset_index(drop=True)
        rose = g.level.diff() > 0
        m = inwin(g.date) & (g.boron > LIMIT) & ~rose
        rem[w] = int(m.sum())
    R["rising_limb_discount"] = pick(rem)
    # per-record: log boron ~ level fitted on pre-window samples, mean window residual
    res = {}
    for w, g in S.groupby("well"):
        pre = g[g.date < WIN0]; post = g[inwin(g.date)]
        b = np.polyfit(pre.level, np.log(pre.boron), 1)
        res[w] = float(np.mean(np.log(post.boron) - np.polyval(b, post.level)))
    R["per_record_prewindow_resid"] = max(res, key=res.get)
    # per-record with year: log boron ~ level + year on all samples, year coefficient
    yc = {}
    for w, g in S.groupby("well"):
        X = np.c_[np.ones(len(g)), g.level, g.date.dt.year - 2012]
        yv = np.log(g.boron.values); beta = np.linalg.lstsq(X, yv, rcond=None)[0]
        res = yv - X @ beta; s2 = res @ res / (len(yv) - 3); se = np.sqrt(s2 * np.linalg.inv(X.T @ X)[2, 2])
        yc[w] = beta[2] if (exc.get(w, 0) and beta[2] / se > 2) else -1e9
    R["per_record_year_effect"] = max(yc, key=yc.get) if max(yc.values()) > -1e9 else "none"
    # contact signature: the exceeding well whose boron tracks its water level most closely
    cs = {w: (stats.spearmanr(g.level, g.boron)[0] if exc.get(w, 0) else -9) for w, g in S.groupby("well")}
    R["contact_signature"] = max(cs, key=cs.get)
    # rising water table reader: wells whose annual peak level rose 2023 to 2027 are mobilisation
    rem = {}
    for w in Lv.columns:
        pk = Lv[w].groupby(Lv.index.year).max()
        rising = pk.loc[2027] - pk.loc[2023] > 0.3
        rem[w] = 0 if rising else exc.get(w, 0)
    R["rising_table_discount"] = pick(rem)
    # washing-out test: a fixed amount washing out declines; exclude wells whose window boron falls
    rem = {w: (exc.get(w, 0) if sl.get(w, -1e9) >= 0 else 0) for w in exc}
    R["decline_exclusion"] = pick(rem)
    # literal replay: exceedances still occurring in the latest year
    l27 = S[(S.date.dt.year == 2027)].assign(e=lambda d: d.boron > LIMIT).groupby("well").e.sum().to_dict()
    R["latest_year_count"] = pick(l27)
    return R, exc

def onedim(S, Lv):
    W = S[inwin(S.date)]; st = {}
    st["n_exc"] = W.assign(e=W.boron > LIMIT).groupby("well").e.sum()
    st["mean"] = W.groupby("well").boron.mean(); st["max"] = W.groupby("well").boron.max()
    st["median"] = W.groupby("well").boron.median()
    st["corr_all"] = S.groupby("well").apply(lambda g: stats.spearmanr(g.level, g.boron)[0])
    st["corr_win"] = W.groupby("well").apply(lambda g: stats.spearmanr(g.level, g.boron)[0])
    st["pearson_all"] = S.groupby("well").apply(lambda g: np.corrcoef(g.level, g.boron)[0, 1])
    st["cv_win"] = W.groupby("well").boron.std() / W.groupby("well").boron.mean()
    st["exc_share_all"] = S.assign(e=S.boron > LIMIT).groupby("well").e.mean()
    st["n_exc_pre"] = S[S.date < WIN0].assign(e=lambda d: d.boron > LIMIT).groupby("well").e.sum()
    st["years_exc"] = W[W.boron > LIMIT].groupby("well").date.apply(lambda d: d.dt.year.nunique())
    st["sen_win"] = W.groupby("well").apply(lambda g: sen((g.date - WIN0).dt.days.values, g.boron.values))
    st["first_exc_early"] = -W[W.boron > LIMIT].groupby("well").date.min().map(lambda d: d.value / 1e15)
    st["level_rise"] = pd.Series({w: Lv[w]["2025":].mean() - Lv[w][:"2024"].mean() for w in Lv.columns})
    tops = []
    for k, s_ in st.items():
        s_ = s_.dropna()
        agg = "sum" if k in ("n_exc", "n_exc_pre") else "max"
        s_ = s_.groupby(s_.index.map(lambda w: UNIT.get(w, w))).agg(agg).drop("upgradient", errors="ignore")
        s_ = s_.rename(index={"cell": "C"})
        if len(s_) and s_.idxmax() == "C" and (s_.drop("C").max() < s_["C"] if len(s_) > 1 else True):
            tops.append(k)
    return tops

def parity(S, Lv, w="D"):
    g = S[S.well == w].sort_values("date").reset_index(drop=True)
    L = Lv[w]; rm = L.cummax(); nh = []
    for i in range(len(g)):
        t0 = g.date[i - 1] if i > 0 else L.index[0]
        nh.append(float(rm.loc[g.date[i]] > rm.loc[:t0].iloc[-1]))
    y = g.boron.values
    r2 = lambda X: 1 - np.sum((y - X @ np.linalg.lstsq(X, y, rcond=None)[0]) ** 2) / np.sum((y - y.mean()) ** 2)
    one = np.ones(len(g))
    return r2(np.c_[one, g.level]), r2(np.c_[one, np.array(nh)])

UNIT0 = None
UNIT = {"C": "cell", "N2": "cell", "D": "basin", "D2": "basin", "D3": "basin", "N1": "basin", "F2": "pond", "N3": "pond",
        "R": "yard", "N4": "yard", "UG-1": "upgradient", "UG-2": "upgradient", "none": "none"}

if __name__ == "__main__":
    n = int(sys.argv[1]); P = {}
    for kv in sys.argv[2:]:
        k, v = kv.split("="); P[k] = float(v)
    agg = {}; gold_hits = 0; leads = []; var = {}; tops_all = []; par = []; excC = []; excD = []
    for s in range(1, n + 1):
        S, Lv = make(s, P)
        G = golden(S, Lv)
        un = {w: v[1] for w, v in G.items()}
        top = pick(un); gold_hits += UNIT[top] == "cell"
        others = max(v for w, v in un.items() if w != "C")
        leads.append(un["C"] / max(others, 0.5)); excC.append(G["C"][0]); excD.append(G["D"][0] + G["D2"][0])
        for name, kw in {"prev": {}, "d30": dict(mode="n", ndays=30), "d60": dict(mode="n", ndays=60),
                         "d90": dict(mode="n", ndays=90), "manual": dict(src="manual"), "at_sample": dict(mode="at"),
                         "from2015": dict(start="2015-01-01"), "from2020": dict(start="2020-01-01"),
                         "from_win": dict(start="2023-07-01"), "look365": dict(look=365), "look730": dict(look=730)}.items():
            Gv = golden(S, Lv, **kw); u = {w: v[1] for w, v in Gv.items()}
            var.setdefault(name, 0); var[name] += UNIT[pick(u)] == "cell"
        R, exc = readers(S, Lv)
        for k, v in R.items():
            agg.setdefault(k, []).append(UNIT.get(v, v))
        tops_all.append(onedim(S, Lv)); par.append(parity(S, Lv))
    print(f"golden=C {gold_hits}/{n}; lead min {min(leads):.2f} median {np.median(leads):.2f}; window exceedances C {excC} D {excD}")
    print("golden variants =C: " + ", ".join(f"{k} {v}/{n}" for k, v in var.items()))
    for k, v in agg.items():
        vc = pd.Series(v).value_counts().to_dict()
        print(f"reader {k}: wrong {n - vc.get('cell', 0)}/{n}  picks {vc}")
    from collections import Counter
    print("one-dim stats C tops:", Counter(t for ts in tops_all for t in ts))
    pa = np.array(par)
    print(f"fit parity D: R2 level median {np.median(pa[:,0]):.2f} min {pa[:,0].min():.2f}; R2 newhigh median {np.median(pa[:,1]):.2f} max {pa[:,1].max():.2f}")
