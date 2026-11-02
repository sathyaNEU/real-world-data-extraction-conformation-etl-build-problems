"""The analyst's computations on run intervals and claims: exposure by hour and light, and the model family.

Inputs are plain arrays so the golden (reading the pack), the checks (reading the world) and the verifier's twin
(its own parser) can all call them:
    runs:   date (datetime.date), depot code, start and end in local clock hours (float, start < end), km
    claims: date, depot code, local clock hour (float)
    sun:    {(depot, row): (sunrise minute GMT, sunset minute GMT)} with row_of(date) and bst_offset(date)
"""
import math

import numpy as np
import pandas as pd
import statsmodels.api as sm

BANDS = [0, 4, 7, 9, 15, 19, 22, 24]


def band(h):
    return int(np.digitize([h % 24], BANDS[1:-1])[0])


def exposure(runs, sun, row_of, bst_offset):
    """One row per (run, clock hour, light) piece: km spread evenly over the run's interval."""
    rec = []
    for i, (d, dep, a, b, km) in enumerate(runs):
        off = bst_offset(d)
        rise, sett = sun[(dep, row_of(d))]
        rl, sl = rise / 60.0 + off, sett / 60.0 + off
        cuts = {a, b} | {float(h) for h in range(int(math.floor(a)) + 1, int(math.ceil(b)))} | {x for x in (rl, sl) if a < x < b}
        cuts = sorted(cuts)
        for x, y in zip(cuts[:-1], cuts[1:]):
            m = (x + y) / 2
            rec.append((i, d, dep, int(m) % 24, 1 if (m < rl or m > sl) else 0, km * (y - x) / (b - a)))
    df = pd.DataFrame(rec, columns=["run", "date", "depot", "hour", "dark", "km"])
    df["band"] = np.digitize(df.hour.values + 0.5, BANDS[1:-1])
    dd = pd.to_datetime(df.date)
    df["month"] = dd.dt.month.values
    df["quarter"] = dd.dt.quarter.values
    df["year"] = dd.dt.year.values
    return df


def claim_frame(claims, sun, row_of, bst_offset):
    rec = []
    for d, dep, h in claims:
        off = bst_offset(d)
        rise, sett = sun[(dep, row_of(d))]
        rl, sl = rise / 60.0 + off, sett / 60.0 + off
        rec.append((d, dep, int(h) % 24, 1 if (h < rl or h > sl) else 0))
    df = pd.DataFrame(rec, columns=["date", "depot", "hour", "dark"])
    df["band"] = np.digitize(df.hour.values + 0.5, BANDS[1:-1])
    dd = pd.to_datetime(df.date)
    df["month"] = dd.dt.month.values
    df["quarter"] = dd.dt.quarter.values
    df["year"] = dd.dt.year.values
    return df


def cells(E, C, cols):
    k = E.groupby(cols).km.sum()
    c = C.groupby(cols).size()
    g = pd.concat([k.rename("km"), c.rename("n")], axis=1).fillna(0).reset_index()
    return g[g.km > 0]


def poisson_fit(E, C, cols):
    g = cells(E, C, cols)
    X = pd.get_dummies(g[cols].astype(str), drop_first=True).astype(float)
    X = sm.add_constant(X, has_constant="add")
    m = sm.GLM(g.n.values, X, family=sm.families.Poisson(), offset=np.log(g.km.values)).fit()
    return m, list(X.columns)


def predict(m, names, F, cols, by="quarter"):
    g = F.groupby(cols + [by]).km.sum().reset_index()
    X = pd.get_dummies(g[cols].astype(str), drop_first=False).astype(float)
    X = sm.add_constant(X, has_constant="add").reindex(columns=names, fill_value=0.0)
    g["p"] = m.predict(X, offset=np.log(g.km.values))
    return g.groupby(by).p.sum()


def forecast(E, C, F, cols):
    """Poisson rate on km with the given terms, carried onto the forward exposure F; returns quarters and year."""
    if not cols:
        r = len(C) / E.km.sum()
        q = F.groupby("quarter").km.sum() * r
        return q, float(q.sum()), None
    m, names = poisson_fit(E, C, cols)
    q = predict(m, names, F, cols)
    return q, float(q.sum()), m


def cell_rates(E, C, cols):
    g = cells(E, C, cols)
    g["rate"] = g.n / g.km
    return g.set_index(cols).rate


def cell_forecast(E, C, F, cols, fallback_cols):
    """Rates per cell of cols, falling back to fallback_cols where the record holds no exposure in a cell."""
    r = cell_rates(E, C, cols)
    rf = cell_rates(E, C, fallback_cols)
    g = F.groupby(cols + ["quarter"]).km.sum().reset_index()
    out = []
    for _, row in g.iterrows():
        key = tuple(row[c] for c in cols) if len(cols) > 1 else row[cols[0]]
        if key in r.index and E.loc[np.logical_and.reduce([E[c] == row[c] for c in cols]), "km"].sum() > 1e5:
            rate = r.loc[key]
        else:
            fk = tuple(row[c] for c in fallback_cols) if len(fallback_cols) > 1 else row[fallback_cols[0]]
            rate = rf.loc[fk]
        out.append((row["quarter"], row["km"] * rate))
    q = pd.DataFrame(out, columns=["quarter", "p"]).groupby("quarter").p.sum()
    return q, float(q.sum())


MODELS_EASY = {
    "overall rate per km": [],
    "by clock band": ["band"],
    "by clock hour": ["hour"],
    "by month and clock band": ["month", "band"],
    "by depot and clock band": ["depot", "band"],
    "by year and clock band": ["year", "band"],
}
MODELS_LIGHT = {
    "clock band and light (golden)": ["band", "dark"],
    "light only": ["dark"],
    "clock hour and light": ["hour", "dark"],
    "month, clock band and light": ["month", "band", "dark"],
    "depot, clock band and light": ["depot", "band", "dark"],
    "year, clock band and light": ["year", "band", "dark"],
}


FINEST = ["depot", "year", "month", "hour", "band", "dark"]


def fit_on(G, cols):
    """Poisson rate on km fitted on a fixed cell table G (one row per finest cell), so nested models compare by LR."""
    X = pd.get_dummies(G[cols].astype(str), drop_first=True).astype(float)
    X = sm.add_constant(X, has_constant="add")
    return sm.GLM(G.n.values, X, family=sm.families.Poisson(), offset=np.log(G.km.values)).fit()


def lr_test(E, C, small, big):
    """Likelihood-ratio statistic, degrees of freedom and p-value of adding big's terms to small's."""
    from scipy import stats
    G = cells(E, C, FINEST)
    G = G[G.km > 0].copy()
    if "dark_am" in big or "dark_am" in small:
        G["am"] = (G.hour < 12).astype(int)
        G["dark_am"] = G.dark * G.am
    m0, m1 = fit_on(G, small), fit_on(G, big)
    lr = 2 * (m1.llf - m0.llf)
    df = int(round(m1.df_model - m0.df_model))
    return float(lr), df, float(stats.chi2.sf(lr, df))


def _frame(rec, cols):
    df = pd.DataFrame(rec, columns=cols)
    df["band"] = np.digitize(df.hour.values + 0.5, BANDS[1:-1])
    dd = pd.to_datetime(df.date)
    df["month"] = dd.dt.month.values
    df["quarter"] = dd.dt.quarter.values
    df["year"] = dd.dt.year.values
    df["dark_am"] = (df.dark * (df.hour < 12)).astype(int)
    return df


def exposure_hourmid(runs, sun, row_of, bst_offset):
    """The coarser construction: km split at clock-hour edges only, each piece dark when its clock hour's midpoint is
    before sunrise or after sunset."""
    rec = []
    for i, (d, dep, a, b, km) in enumerate(runs):
        off = bst_offset(d)
        rise, sett = sun[(dep, row_of(d))]
        rl, sl = rise / 60.0 + off, sett / 60.0 + off
        cuts = sorted({a, b} | {float(h) for h in range(int(math.floor(a)) + 1, int(math.ceil(b)))})
        for x, y in zip(cuts[:-1], cuts[1:]):
            h = int((x + y) / 2)
            rec.append((i, d, dep, h % 24, 1 if (h + 0.5 < rl or h + 0.5 > sl) else 0, km * (y - x) / (b - a)))
    return _frame(rec, ["run", "date", "depot", "hour", "dark", "km"])


def claim_frame_hourmid(claims, sun, row_of, bst_offset):
    """Claims labelled by their clock hour's midpoint, consistent with exposure_hourmid."""
    rec = []
    for d, dep, h in claims:
        off = bst_offset(d)
        rise, sett = sun[(dep, row_of(d))]
        rl, sl = rise / 60.0 + off, sett / 60.0 + off
        hm = int(h) + 0.5
        rec.append((d, dep, int(h) % 24, 1 if (hm < rl or hm > sl) else 0))
    return _frame(rec, ["date", "depot", "hour", "dark"])


FAMILY = {"light only": ["dark"], "band + light": ["band", "dark"], "hour + light": ["hour", "dark"],
          "month + band + light": ["month", "band", "dark"], "depot + band + light": ["depot", "band", "dark"],
          "band + light, morning and evening multipliers": ["band", "dark", "dark_am"],
          "light only, morning and evening multipliers": ["dark", "dark_am"],
          "month + hour + light": ["month", "hour", "dark"]}


def with_am(df):
    df = df.copy()
    df["dark_am"] = (df.dark * (df.hour < 12)).astype(int)
    return df
