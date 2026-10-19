"""Risk models for the expected deaths: the golden's own family (the patient's condition before surgery, the earlier
operation included) and the routes a solver might take. Each returns observed over expected deaths by hospital."""
import numpy as np
import pandas as pd
import statsmodels.api as sm

H = ["A", "B", "C", "D", "E", "F", "G", "H"]
COMORB = ["chf", "ckd", "copd", "liver", "dm", "af"]
INDEX = ["age10", "male", "mal", "tot", "whip", "urg", "wtloss"] + COMORB


def prep(df):
    d = df.copy()
    d["age10"] = (d.age - 67) / 10
    d["age2"] = d.age10 ** 2
    d["ncom"] = d[COMORB].astype(int).sum(axis=1) + d.wtloss.astype(int)
    for c in d.columns:
        if d[c].dtype == bool:
            d[c] = d[c].astype(float)
    return d


def ratio(d, cols, link="logit", out="dead"):
    X = sm.add_constant(d[cols].astype(float), has_constant="add")
    fam = sm.families.Binomial(sm.families.links.Logit() if link == "logit" else sm.families.links.Probit())
    m = sm.GLM(d[out].astype(float), X, family=fam).fit()
    g = d.assign(e=m.predict(X)).groupby("h")
    return (g[out].sum() / g.e.sum()).reindex(H), m


def eb(d, r):
    """Empirical Bayes on the log ratio, each hospital's expected deaths giving its precision."""
    g = d.groupby("h")
    o = g.dead.sum().reindex(H).astype(float)
    e = o / r
    y = np.log(np.maximum(o, .5) / e)
    v = 1 / np.maximum(o, .5)
    tau2 = max(np.var(y.values, ddof=1) - np.mean(v.values), 1e-4)
    w = tau2 / (tau2 + v)
    mu = np.average(y, weights=1 / (tau2 + v))
    return np.exp(w * y + (1 - w) * mu)


GOLDEN = INDEX + ["redo"]
FAMILY = {
    "logit": (GOLDEN, "logit"),
    "probit": (GOLDEN, "probit"),
    "age2": (GOLDEN + ["age2"], "logit"),
    "earlier_terms": (GOLDEN + ["chole", "stent"], "logit"),
    "count": (["age10", "male", "mal", "tot", "whip", "urg", "ncom", "redo"], "logit"),
    "many": (GOLDEN + ["htn", "lipid", "gerd", "obese", "smoke", "osa", "thyroid", "depress"], "logit"),
    "many_earlier": (GOLDEN + ["htn", "lipid", "gerd", "obese", "smoke", "osa", "thyroid", "depress", "chole", "stent",
                               "age2"], "logit"),
}


def family(df):
    d = prep(df)
    return {k: ratio(d, cols, link)[0] for k, (cols, link) in FAMILY.items()}


def routes(df):
    d = prep(df)
    R = {}
    R["raw"] = d.groupby("h").dead.mean().reindex(H)
    R["index"] = ratio(d, INDEX)[0]
    R["index_dx"] = ratio(d, INDEX + ["comp"])[0]
    R["index_min"] = ratio(d, ["age10", "male", "tot", "whip", "urg"])[0]
    d["any_earlier"] = ((d.redo + d.chole + d.stent) > 0).astype(float)
    d["earlier_op"] = ((d.redo + d.chole) > 0).astype(float)
    R["any_earlier"] = ratio(d, INDEX + ["any_earlier"])[0]
    R["earlier_op"] = ratio(d, INDEX + ["earlier_op"])[0]
    R["golden_eb"] = eb(d, ratio(d, GOLDEN)[0])
    R["golden_min"] = ratio(d, ["age10", "male", "tot", "whip", "urg", "redo"])[0]
    return R


def top3(s):
    return "".join(sorted(s.sort_values().index[:3]))
