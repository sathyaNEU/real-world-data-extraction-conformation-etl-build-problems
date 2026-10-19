"""Every route a reader might take, run on a sittings frame (the clean truth's, or the pack's as loaded): the golden
two-stage estimate and its family, the slope through every sitting, and the shortcuts a careful analyst might try."""
import datetime as dt
import numpy as np
import pandas as pd
import common as K

W0, W1 = K.WINDOW
YEAR = 365.25
Q, T, PW = "Quarndale", "Thurlwick", "Penwardine"


def frame(w):
    """One row per sitting of the clean truth, with each patient's latest recorded diagnosis on 30 September 2026."""
    rows = []
    for p in w["patients"]:
        if not p["sittings"]:
            continue
        dxs = sorted([x for x in p["dx"] if x["entered"] <= W1], key=lambda x: (x["entered"], x["given"]))
        latest = dxs[-1]["code"] if dxs else None
        first_ever = p["sittings"][0]["date"]
        for i, s in enumerate(p["sittings"]):
            rows.append((p["pid"], s["date"], s["clinic"], s["completed"], s["total"], s["k"], latest, first_ever,
                         p["rate"], p["typ"]))
    df = pd.DataFrame(rows, columns=["pid", "date", "clinic", "completed", "total", "k", "latest", "first_ever",
                                     "rate", "typ"])
    df["t"] = (pd.to_datetime(df.date) - pd.Timestamp("2022-01-01")).dt.days / YEAR
    df["first_t"] = (pd.to_datetime(df.first_ever) - pd.Timestamp("2022-01-01")).dt.days / YEAR
    return df


def population(df):
    """The paper's population: completed sittings in the window, Alzheimer's or MCI at the end, two or more."""
    w = df[df.completed & (df.date >= W0) & (df.date <= W1) & df.latest.isin(K.IN_SCOPE)].copy()
    w = w[w.groupby("pid").t.transform("size") >= 2].copy()
    w["step"] = (w.k >= 1).astype(float)
    w["s"] = w.total.astype(float)
    return w


def slopes(w, y):
    g = w.groupby("pid")
    tm = g.t.transform("mean")
    ym = g[y].transform("mean")
    return ((w.t - tm) * (w[y] - ym)).groupby(w.pid).sum() / ((w.t - tm) ** 2).groupby(w.pid).sum()


def endpoint(w, y):
    g = w.sort_values("t").groupby("pid")
    return (g[y].last() - g[y].first()) / (g.t.last() - g.t.first())


def fe(w, cols=("step",)):
    """Within-patient regression: each patient's own intercept and slope, a common step."""
    v = w[w.groupby("pid").t.transform("size") >= 3]
    gg = v.groupby("pid")
    xt = v.t - gg.t.transform("mean")
    stt = (xt * xt).groupby(v.pid).transform("sum")

    def resid(col):
        ym = gg[col].transform("mean")
        return v[col] - ym - ((xt * (v[col] - ym)).groupby(v.pid).transform("sum") / stt) * xt
    X = np.column_stack([resid(c) for c in cols])
    return np.linalg.lstsq(X, resid("s").values, rcond=None)[0]


def clinic_of(w):
    return w.sort_values(["pid", "t"]).groupby("pid").clinic.last()


def cavg(w, b):
    cl = clinic_of(w)
    return -(b.groupby(cl).mean())


def golden(w, P=None):
    if P is None:
        P = fe(w)[0]
    w = w.copy()
    w["a"] = w.s - P * w.step
    return cavg(w, slopes(w, "a")), P


def all_history(df):
    """Every completed sitting of every patient with two or more, any window, any diagnosis: the gain from all."""
    h = df[df.completed].copy()
    h = h[h.groupby("pid").t.transform("size") >= 2]
    h["step"] = (h.k >= 1).astype(float)
    h["s"] = h.total.astype(float)
    return h


def routes(df, mixed=False):
    w = population(df)
    out = {}
    out["naive"] = cavg(w, slopes(w, "s"))
    out["gold"], Pw = golden(w)
    Pall = fe(all_history(df))[0]
    out["gold_allP"], _ = golden(w, Pall)
    ww = w.copy()
    ww["a"] = ww.s - Pw * ww.step
    out["gold_ep"] = cavg(ww, endpoint(ww, "a"))
    ww["k2"] = (ww.k >= 2).astype(float)
    b2 = fe(ww, ("step", "k2"))
    ww["c"] = ww.s - b2[0] * ww.step - b2[1] * ww.k2
    out["gold_kd"] = cavg(ww, slopes(ww, "c"))
    fw = w.first_t
    for nm, lo in (("recent", 2024.25), ("recent0", 2024.0), ("recent5", 2024.5), ("since23", 2023.0),
                   ("incident", 2022.0)):
        sub = w[fw >= lo - 2022.0]
        out[nm + "_naive"] = cavg(sub, slopes(sub, "s"))
        sub = sub.copy()
        sub["a"] = sub.s - Pw * sub.step
        out[nm + "_gold"] = cavg(sub, slopes(sub, "a"))
    nw = w.groupby("pid").t.transform("size")
    two = w[(nw == 2) & (fw >= 0)]
    out["two_new"] = cavg(two, slopes(two, "s"))
    d = w[w.k >= 1]
    d = d[d.groupby("pid").t.transform("size") >= 2]
    out["dropfirst"] = cavg(d, slopes(d, "s"))
    b = slopes(w, "s")
    cl = clinic_of(w)
    nn = w.groupby("pid").t.size()
    first_s = w.sort_values("t").groupby("pid").s.first()
    for nm, cov in (("adj_nsit", 1.0 / nn), ("adj_base", first_s), ("adj_both", None)):
        X = pd.get_dummies(cl).astype(float)
        if cov is None:
            X["z1"] = 1.0 / nn - (1.0 / nn).mean()
            X["z2"] = first_s - first_s.mean()
            k = 2
        else:
            X["z"] = cov - cov.mean()
            k = 1
        beta = np.linalg.lstsq(X.values, b.loc[X.index].values, rcond=None)[0]
        out[nm] = pd.Series({c: -beta[i] for i, c in enumerate(X.columns[:-k])})
    wt = ((w.t - w.groupby("pid").t.transform("mean")) ** 2).groupby(w.pid).sum()
    out["wls_naive"] = -((b * wt).groupby(cl).sum() / wt.groupby(cl).sum())
    # the two systems read apart: only the EPR's sittings (2024 on)
    e = w[w.t >= (K.EPR_GO_LIVE - W0).days / YEAR]
    e = e[e.groupby("pid").t.transform("size") >= 2]
    out["epr_only_naive"] = cavg(e, slopes(e, "s"))
    # more reflexes: one diagnosis at a time, a robust centre, reliable slopes only, first to last
    typ_last = w.groupby("pid").latest.last()
    for nm, keep in (("ad_only_naive", K.AD_CODES), ("mci_only_naive", ("MCI",))):
        sub = w[w.pid.map(typ_last).isin(keep)]
        out[nm] = cavg(sub, slopes(sub, "s"))
    out["median_naive"] = -(b.groupby(cl).median())
    lo, hi = b.quantile(0.05), b.quantile(0.95)
    out["trimmed_naive"] = -(b.clip(lo, hi).groupby(cl).mean())
    ge3 = w[nw >= 3]
    out["ge3_naive"] = cavg(ge3, slopes(ge3, "s"))
    out["ends_naive"] = cavg(w, endpoint(w, "s"))
    ww2 = w.copy()
    ww2["a"] = ww2.s - Pw * ww2.step
    out["median_gold"] = -(slopes(ww2, "a").groupby(cl).median())
    out["_P"] = (Pw, Pall, b2[0], b2[1])
    out["_n"] = cl.value_counts()
    out["truth"] = w.groupby("pid").rate.first().groupby(cl).mean()
    if mixed:
        out.update(mixed_models(w))
    return out


AXES = ("t_cal", "t_win", "t_dx")
KINDS = {"rs": ("", True), "ri": ("", False), "rs_step": (" + step", True), "mundlak": (" + step + mstep", True)}


def mixed_frame(w):
    """The sittings with each patient at the paper's clinic and the three clocks a growth model might run on."""
    w = w.copy()
    g = w.groupby("pid")
    w["cl"] = w.pid.map(clinic_of(w))           # the clinic of the patient's last completed sitting (paper, 3.2)
    w["t_cal"] = w.t                            # years since 1 January 2022
    w["t_win"] = w.t - g.t.transform("min")     # years since the patient's first sitting in the period
    w["t_dx"] = w.t - w.first_t                 # years since the patient's first sitting ever
    w["mstep"] = g.step.transform("mean")       # the patient's mean of the step (Mundlak)
    return w


def mixed_fit(w, formula, re_formula):
    """A linear mixed model by REML, driven to convergence: BFGS, then L-BFGS and CG from the best point so far."""
    import warnings
    import statsmodels.formula.api as smf
    md = smf.mixedlm(formula, w, groups=w["pid"], re_formula=re_formula)
    best = None
    for meth in ("bfgs", "lbfgs", "cg"):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                f = md.fit(method=meth, maxiter=4000, start_params=None if best is None else best.params)
            except (ValueError, np.linalg.LinAlgError):
                continue
        if best is None or f.llf > best.llf:
            best = f
    return best


def _mixed_job(job):
    w, kind, ax = job
    rhs, slope = KINDS[kind]
    f = mixed_fit(w, "s ~ 0 + C(cl) + C(cl):%s%s" % (ax, rhs), "~%s" % ax if slope else "~1")
    out = {"%s_%s" % (kind, ax): pd.Series({c: -f.params["C(cl)[%s]:%s" % (c, ax)] for c in K.NAMES}),
           "_conv_%s_%s" % (kind, ax): bool(f.converged)}
    if "step" in rhs:
        out["_P_%s_%s" % (kind, ax)] = float(f.params["step"])
    if "mstep" in rhs:
        out["_z_mstep_%s" % ax] = float(f.tvalues["mstep"])
    return out


def mixed_models(w, kinds=("rs", "ri", "rs_step", "mundlak")):
    """Each clinic's slope from the growth models a careful analyst might fit, on each clock, with each patient at the
    paper's clinic: random intercepts and slopes (rs) and random intercepts only (ri), with no step; random intercepts
    and slopes with the step (rs_step), and with the step and the patient's mean of it (mundlak). The fits run in
    parallel; each is the same whichever process runs it."""
    from concurrent.futures import ProcessPoolExecutor
    w = mixed_frame(w)
    jobs = [(w, kind, ax) for kind in kinds for ax in AXES]
    out = {}
    with ProcessPoolExecutor(max_workers=4) as ex:
        for r in ex.map(_mixed_job, jobs):
            out.update(r)
    return out


def accidental(w):
    """Two routes that skip the gain and still name Quarndale and Thurlwick, both off the paper's unit: each clinic's
    sittings pooled in one regression on time since the patient's first sitting, and a random-slopes model on calendar
    time with each sitting labelled by its own clinic, which the patients seen at two clinics pin."""
    w = mixed_frame(w)
    out = {}
    for ax in ("t_win", "t_dx"):
        out["pooled_" + ax] = pd.Series({c: -np.polyfit(d[ax], d.s, 1)[0] for c, d in w.groupby("cl")})
    f = mixed_fit(w, "s ~ 0 + C(clinic) + C(clinic):t_cal", "~t_cal")
    out["perrow_rs_t_cal"] = pd.Series({c: -f.params["C(clinic)[%s]:t_cal" % c] for c in K.NAMES})
    out["_conv_perrow_rs_t_cal"] = bool(f.converged)
    movers = w.groupby("pid").clinic.nunique()
    out["_movers"] = int((movers > 1).sum())
    stay = w[w.pid.map(movers) == 1]
    f = mixed_fit(stay, "s ~ 0 + C(clinic) + C(clinic):t_cal", "~t_cal")
    out["perrow_rs_t_cal_stayers"] = pd.Series({c: -f.params["C(clinic)[%s]:t_cal" % c] for c in K.NAMES})
    return out


def top2(s):
    return frozenset(s.sort_values(ascending=False).index[:2])


def rank_of(s, c):
    return list(s.sort_values(ascending=False).index).index(c) + 1


GOLD = frozenset([Q, T])
NAIVE = frozenset([T, PW])
NO_INSIGHT = ["naive", "recent_naive", "recent0_naive", "recent5_naive", "since23_naive", "incident_naive", "two_new",
              "adj_nsit", "adj_base", "adj_both", "wls_naive", "epr_only_naive", "ad_only_naive", "mci_only_naive",
              "median_naive", "trimmed_naive", "ge3_naive", "ends_naive"]


def summary(out):
    lines = []
    for k, v in out.items():
        if isinstance(v, pd.Series) and not k.startswith("_"):
            o = v.sort_values(ascending=False)
            lines.append("  %-18s %-10s %s" % (k, "+".join(x[:4] for x in o.index[:2]),
                                              " ".join("%s %.2f" % (c[:4], o[c]) for c in o.index)))
    return "\n".join(lines)
