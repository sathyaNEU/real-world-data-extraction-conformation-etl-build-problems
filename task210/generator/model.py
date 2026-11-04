"""The main call's analysis on the clean truth: the golden (reader e) and every rival reader, shared by checks.py.

Golden: a Poisson model of firm brakes per pass with section-direction, hour, day-type, darkness, new-operator and
school-morning terms and a glare term (1 + G * glare * sun), glare computed from the sun's position against each
section direction's bearing; projected to the January pick's weekday peak passes under the station's normal sunshine.
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.optimize import minimize_scalar
import world as W
import simulate as S

KEYS = ["sd", "hour", "wkend", "dark", "newop", "school_am"]
_FWD = {}


def forward():
    """The January pick's weekday peak passes (entry inside SRM-07's peak windows), with the sun at each pass."""
    if "F" not in _FWD:
        T = S.simulate(seed=W.SEED, start=W.PICK_START, end=W.PICK_END, holidays=W.PICK_HOLIDAYS,
                       runs_adj=W.PICK_RUN_ADJ)
        F = T["passes"]
        F = F[(F["peak"] != "OFF")].copy()
        F["newop"] = 0.0
        F["psun"] = F["month"].map(W.SUN_NORM).values / 100.0
        _FWD["F"] = F.reset_index(drop=True)
    return _FWD["F"]


def truth_rates(T, G=None, base=None):
    G = W.G_TRUE if G is None else G
    base = W.BASE if base is None else base
    F = forward()
    b = np.where(F["track"].values == "street", base["street"], base["reserved"])
    dk = np.where(F["track"].values == "street", W.DARK["street"], W.DARK["reserved"])
    hf = F["hour"].map(lambda h: W.HOUR_F.get(h, 0.9)).values
    sch = 1 + np.where(F["track"].values == "street", W.SCHOOL, 0.0) * F["school_am"].values
    r = b * F["sd"].map(T["noise"]).values * hf * (1 + dk * F["dark"].values) * sch * (1 + G * F["glare"].values * F["psun"].values)
    return pd.Series(r).groupby([F["sd"].values, F["peak"].values]).mean()


def cells(P, cone=W.CONE, efull=W.E_FULL, ezero=W.E_ZERO, shape="cos2", sunmap=None, gbin=False):
    g = S.glare(P["elev"].values, P["az"].values, P["bearing"].values, cone, efull, ezero, shape)
    sun = P["sun"].values if sunmap is None else P["cover"].map(sunmap).values
    d = pd.DataFrame({k: P[k].values for k in ["sd", "hour", "dark", "newop", "school_am"]})
    d["wkend"] = (P["daytype"].values != "weekday").astype(float)
    d["n_fb"] = P["n_fb"].values
    d["gs"] = g * sun
    keys = KEYS + (["gb"] if gbin else [])
    if gbin:
        d["gb"] = np.round(d["gs"] * 20) / 20
    return d.groupby(keys, as_index=False).agg(y=("n_fb", "sum"), n=("n_fb", "size"), sgs=("gs", "sum"))


def design(c, hourfe=True, controls=("wkend", "dark", "newop", "school_am")):
    X = pd.get_dummies(c["sd"], prefix="sd").astype(float)
    if hourfe:
        X = pd.concat([X, pd.get_dummies(c["hour"].astype(str), prefix="h", drop_first=True).astype(float)], axis=1)
    for k in controls:
        X[k] = c[k].astype(float).values
    return X


def fit(P, cone=W.CONE, efull=W.E_FULL, ezero=W.E_ZERO, shape="cos2", form="linear", hourfe=True, sunmap=None,
        controls=("wkend", "dark", "newop", "school_am")):
    c = cells(P, cone, efull, ezero, shape, sunmap, gbin=(form == "loglin"))
    X = design(c, hourfe, controls)
    y, n, Xv = c["y"].values, c["n"].values.astype(float), X.values
    if form == "loglin":
        m = sm.GLM(y, np.column_stack([Xv, c["gb"].values]), family=sm.families.Poisson(), offset=np.log(n)).fit()
        coef = dict(zip(list(X.columns) + ["gs"], m.params))
        return coef, coef["gs"], m.llf
    nll = lambda G: -sm.GLM(y, Xv, family=sm.families.Poisson(), offset=np.log(n + G * c["sgs"].values)).fit().llf
    Gh = minimize_scalar(nll, bounds=(0.0, 10.0), method="bounded", options={"xatol": 0.005}).x
    m = sm.GLM(y, Xv, family=sm.families.Poisson(), offset=np.log(n + Gh * c["sgs"].values)).fit()
    return dict(zip(X.columns, m.params)), Gh, m.llf


def project(coef, Gh, cone=W.CONE, efull=W.E_FULL, ezero=W.E_ZERO, shape="cos2", form="linear", psun_scale=1.0,
            held=None):
    F = forward()
    g = S.glare(F["elev"].values, F["az"].values, F["bearing"].values, cone, efull, ezero, shape)
    if held is not None:   # reader d: each cell's observed alignment held in place of January's
        g = np.array([held.get((sd, pk), 0.0) for sd, pk in zip(F["sd"].values, F["peak"].values)])
    ps = F["psun"].values * psun_scale
    hc = np.array([coef.get(f"h_{h}", 0.0) for h in F["hour"].values])
    lin = (np.array([coef[f"sd_{s}"] for s in F["sd"].values]) + hc + coef.get("dark", 0.0) * F["dark"].values
           + coef.get("school_am", 0.0) * F["school_am"].values)
    mult = (ps * np.exp(Gh * g) + (1 - ps)) if form == "loglin" else (1 + Gh * g * ps)
    r = np.exp(lin) * mult * 1000
    return pd.Series(r).groupby([F["sd"].values, F["peak"].values]).mean()


def golden(P, **kw):
    fkw = {k: v for k, v in kw.items() if k in ("cone", "efull", "ezero", "shape", "form", "hourfe", "sunmap", "controls")}
    pkw = {k: v for k, v in kw.items() if k in ("cone", "efull", "ezero", "shape", "form", "psun_scale")}
    coef, Gh, _ = fit(P, **fkw)
    return project(coef, Gh, **pkw), Gh


def slate(rates, cap=W.CAP):
    return set(rates.sort_values(ascending=False).index[:cap])


# ---------------- rival readers ----------------
def obs_peak(P, months=None):
    d = P[P["peak"] != "OFF"]
    if months is not None:
        d = d[d["month"].isin(months)]
    t = d.groupby(["sd", "peak"])["n_fb"].agg(["sum", "size"])
    return t["sum"] / t["size"] * 1000


def reader_a(P):
    """Field-decomposing: cell (sd x peak), month, darkness, sky, new operators, school; October's level carried."""
    d = P[P["peak"] != "OFF"]
    c = d.groupby(["sd", "peak", "month", "dark", "newop", "school_am", "sun"], as_index=False).agg(y=("n_fb", "sum"), n=("n_fb", "size"))
    X = pd.get_dummies(c["sd"] + "|" + c["peak"], prefix="c").astype(float)
    X = pd.concat([X, pd.get_dummies(c["month"].astype(str), prefix="m", drop_first=True).astype(float)], axis=1)
    for k in ("dark", "newop", "school_am", "sun"):
        X[k] = c[k].astype(float).values
    m = sm.GLM(c["y"].values, X.values, family=sm.families.Poisson(), offset=np.log(c["n"].values)).fit()
    coef = dict(zip(X.columns, m.params))
    F = forward()
    fd = F.groupby("peak")["dark"].mean()
    fs = F.groupby("peak")["school_am"].mean()
    out = {}
    for k in coef:
        if k.startswith("c_"):
            sd, pk = k[2:].split("|")
            out[(sd, pk)] = np.exp(coef[k] + coef.get("m_10", 0.0) + coef["dark"] * fd[pk] + coef["school_am"] * fs[pk]
                                   + coef["sun"] * 0.68) * 1000
    return pd.Series(out)


def reader_b_lowsun(P):
    """Constructing: a non-directional low-sun term (sun up and under 20 degrees, sky clear), darkness, school."""
    low = ((P["elev"] > 0.5) & (P["elev"] < 20)).astype(float) * P["sun"]
    d = pd.DataFrame({"sd": P["sd"], "hour": P["hour"], "dark": P["dark"], "school_am": P["school_am"],
                      "low": np.round(low, 1), "y": P["n_fb"]})
    c = d.groupby(["sd", "hour", "dark", "school_am", "low"], as_index=False).agg(y=("y", "sum"), n=("y", "size"))
    X = pd.get_dummies(c["sd"], prefix="sd").astype(float)
    X = pd.concat([X, pd.get_dummies(c["hour"].astype(str), prefix="h", drop_first=True).astype(float)], axis=1)
    for k in ("dark", "school_am", "low"):
        X[k] = c[k].astype(float).values
    m = sm.GLM(c["y"].values, X.values, family=sm.families.Poisson(), offset=np.log(c["n"].values)).fit()
    coef = dict(zip(X.columns, m.params))
    F = forward()
    low = ((F["elev"] > 0.5) & (F["elev"] < 20)).astype(float).values * F["psun"].values
    hc = np.array([coef.get(f"h_{h}", 0.0) for h in F["hour"].values])
    lin = (np.array([coef[f"sd_{s}"] for s in F["sd"].values]) + hc + coef["dark"] * F["dark"].values
           + coef["school_am"] * F["school_am"].values + coef["low"] * low)
    return pd.Series(np.exp(lin) * 1000).groupby([F["sd"].values, F["peak"].values]).mean()


def reader_b_suntime(P):
    """Constructing: each cell's rate by sun-elevation bin (sun-time), read off at January's sun-time."""
    d = P[P["peak"] != "OFF"].assign(st=lambda x: np.round(x["elev"] / 4.0))
    r = d.groupby(["sd", "peak", "st"])["n_fb"].mean()
    base = d.groupby(["sd", "peak"])["n_fb"].mean()
    F = forward().assign(st=lambda x: np.round(x["elev"] / 4.0))
    vals = [r.get((s, p, t), base[(s, p)]) for s, p, t in zip(F["sd"].values, F["peak"].values, F["st"].values)]
    return pd.Series(np.array(vals) * 1000).groupby([F["sd"].values, F["peak"].values]).mean()


def reader_c(P, months=None):
    """Per-record: section direction x peak x clock hour x sky (attributes from two-file joins), months pooled."""
    d = P[P["peak"] != "OFF"]
    if months is not None:
        d = d[d["month"].isin(months)]
    t = d.groupby(["sd", "peak", "hour", "sun"])["n_fb"].mean()
    F = forward()
    out = {}
    for (sd, pk), grp in F.groupby(["sd", "peak"]):
        vals = []
        for h, ps in zip(grp["hour"].values, grp["psun"].values):
            a = t.get((sd, pk, h, 1.0), np.nan)
            b = t.get((sd, pk, h, 0.0), np.nan)
            a = b if np.isnan(a) else a
            b = a if np.isnan(b) else b
            vals.append(a * ps + b * (1 - ps))
        out[(sd, pk)] = np.nanmean(vals) * 1000
    return pd.Series(out)


def reader_d_held(P, months):
    """Glare-naming: the glare model fitted on the record, January projected with each cell's observed alignment held."""
    coef, Gh, _ = fit(P)
    d = P[(P["peak"] != "OFF") & (P["month"].isin(months))]
    held = d.groupby(["sd", "peak"])["glare"].mean().to_dict()
    return project(coef, Gh, held=held)


def literal_normal_weather(P):
    d = P[P["peak"] != "OFF"]
    t = d.groupby(["sd", "peak", "sun"])["n_fb"].mean().unstack("sun")
    F = forward()
    ps = F.groupby("peak")["psun"].mean()
    return pd.Series({(sd, pk): (row.get(1.0, 0) * ps[pk] + row.get(0.0, 0) * (1 - ps[pk])) * 1000 for (sd, pk), row in t.iterrows()})


def literal_dark_share(P):
    d = P[P["peak"] != "OFF"]
    t = d.groupby(["sd", "peak", "dark"])["n_fb"].mean().unstack("dark")
    F = forward()
    fd = F.groupby("peak")["dark"].mean()
    out = {}
    for (sd, pk), row in t.iterrows():
        light = row.get(0.0, np.nan)
        dk = row.get(1.0, light)
        dk = light if np.isnan(dk) else dk
        out[(sd, pk)] = (light * (1 - fd[pk]) + dk * fd[pk]) * 1000
    return pd.Series(out)


READERS = {
    "first_look": lambda P: obs_peak(P),
    "a_field": reader_a,
    "b_lowsun": reader_b_lowsun,
    "b_suntime": reader_b_suntime,
    "c_all": lambda P: reader_c(P),
    "c_sepoct": lambda P: reader_c(P, [9, 10]),
    "c_oct": lambda P: reader_c(P, [10]),
    "d1_observed_aligned": lambda P: obs_peak(P, [9, 10]),
    "d2_held_aproct": lambda P: reader_d_held(P, range(4, 11)),
    "d3_held_sepoct": lambda P: reader_d_held(P, [9, 10]),
}
LITERAL = {
    "L1_aproct": lambda P: obs_peak(P),
    "L2_oct": lambda P: obs_peak(P, [10]),
    "L3_sepoct": lambda P: obs_peak(P, [9, 10]),
    "L4_normal_weather": literal_normal_weather,
    "L5_dark_share": literal_dark_share,
}
VARIANTS = {
    "cone15": dict(cone=15.0), "cone20": dict(cone=20.0), "cone30": dict(cone=30.0), "cone35": dict(cone=35.0),
    "band_box15": dict(efull=15.0, ezero=15.01), "band_box20": dict(efull=20.0, ezero=20.01),
    "band_8_20": dict(efull=8.0, ezero=20.0), "band_15_30": dict(efull=15.0, ezero=30.0),
    "lin_cone30": dict(shape="lin", cone=30.0), "box_cone20": dict(shape="box", cone=20.0), "loglin": dict(form="loglin"),
    "sun85": dict(psun_scale=0.85), "nohour": dict(hourfe=False), "sct_cloudy": dict(sunmap={"CLR": 1, "FEW": 1, "SCT": 0, "BKN": 0, "OVC": 0}),
    "no_controls": dict(controls=("wkend", "dark")),
}
