"""The ladder's routes, each run on the shipped files: the tracker's own driver analysis on the attribute
ratings, the ratings beside the journey conditions, the cascade groups against the rest, the whole train's
busiest leg for every passenger, the unweighted file, and the golden family's constructions."""
import numpy as np
import statsmodels.api as sm

import analysis as A
import common as K

ITEMS = [q for q, _ in K.ITEMS]
P, C, S, F, O = "punctuality", "crowding", "on-board staffing", "fares", "other"
MAPS = {   # the tracker's items read as the four drivers: as their wording names them, and wider or narrower
    "as worded": {"q5a": P, "q5b": P, "q5c": O, "q5d": O, "q5e": C, "q5f": S, "q5g": S, "q5h": O, "q5i": F, "q5j": O},
    "wide": {"q5a": P, "q5b": P, "q5c": P, "q5d": C, "q5e": C, "q5f": S, "q5g": S, "q5h": S, "q5i": F, "q5j": S},
    "crowding wide": {"q5a": P, "q5b": P, "q5c": C, "q5d": C, "q5e": C, "q5f": S, "q5g": S, "q5h": O, "q5i": F,
                      "q5j": C},
    "narrow": {"q5a": P, "q5b": O, "q5c": O, "q5d": O, "q5e": C, "q5f": S, "q5g": O, "q5h": O, "q5i": F, "q5j": O},
}
ITEM_DRIVER = MAPS["as worded"]


def ratings(D, J):
    R = D["resp"].set_index("serial").loc[J["serial"], ITEMS].astype(float)
    R = R.where(R != 9)
    return R.values


def kda(D, J, mapping="as worded", outcome="q1", importance="regression"):
    """R0: overall satisfaction regressed on the ten ratings (weighted, complete answers), each aspect's
    importance times the fall in its mean rating, the fall shared out in proportion, summed by driver. The
    importance may instead be each rating's correlation with the overall verdict."""
    M = ratings(D, J)
    y = (J["q1"] if outcome == "q1" else J["sat"]).values.astype(float)
    w = J["weight"].values
    ok = ~np.isnan(M).any(axis=1) & ~np.isnan(y)
    if importance == "regression":
        b = sm.WLS(y[ok], sm.add_constant(M[ok]), weights=w[ok]).fit().params[1:]
    else:
        b = np.array([np.corrcoef(M[ok, j], y[ok])[0, 1] for j in range(len(ITEMS))])
    wave = J["wave"].values
    dm = []
    for j in range(len(ITEMS)):
        x = M[:, j]
        a = ~np.isnan(x)
        dm.append(np.average(x[a & (wave == 2026)], weights=w[a & (wave == 2026)]) -
                  np.average(x[a & (wave == 2025)], weights=w[a & (wave == 2025)]))
    con = -b * np.array(dm)
    fall = A.shares(J)["fall"]
    share = con / con.sum() * fall
    out = {}
    for q, v in zip(ITEMS, share):
        out[MAPS[mapping][q]] = out.get(MAPS[mapping][q], 0.0) + float(v)
    return out


def top(points):
    return max((k for k in points if k != "other"), key=points.get)


def kitchen_sink(D, J, mapping=None):
    """R1: the journey conditions beside the ten ratings in one weighted model of being satisfied; each term's
    effect times its change, the ratings summed by the driver they name."""
    M = ratings(D, J)
    sat = J["sat"].values
    w = J["weight"].values
    wave = (J["wave"].values == 2026).astype(float)
    ok = ~np.isnan(M).any(axis=1) & ~np.isnan(sat)
    cols = [J[c].values.astype(float) for _, c in A.DRIVERS]
    X = np.column_stack([c[ok] for c in cols] + [wave[ok]] + [M[ok, j] for j in range(len(ITEMS))])
    m = sm.WLS(sat[ok], sm.add_constant(X), weights=w[ok]).fit()
    names = [n for n, _ in A.DRIVERS] + ["wave"] + ITEMS
    out = {}
    for j, nm in enumerate(names):
        if nm == "wave":
            continue
        x = X[:, j]
        ww, wv = w[ok], wave[ok]
        d = np.average(x[wv == 1], weights=ww[wv == 1]) - np.average(x[wv == 0], weights=ww[wv == 0])
        if nm in dict(A.DRIVERS):
            key = nm
        elif mapping is None:
            continue                    # the ratings held as controls only
        else:
            key = MAPS[mapping][nm]
        out[key] = out.get(key, 0.0) - float(m.params[j + 1] * d * 100)
    return out


def cascade_did(J):
    """R2: the service groups that lost their class 166s at the October 2025 cascade (Hollin Vale, Coastway)
    against the rest; the extra fall there, carried to their share of journeys, credited to crowding."""
    w = J["weight"].values
    sat = J["sat"].values
    casc = J["group"].isin(["VALE", "COAST"]).values
    wave = J["wave"].values

    def s(m):
        return A.wmean(sat[m], w[m]) * 100
    did = (s((wave == 2025) & casc) - s((wave == 2026) & casc)) - (s((wave == 2025) & ~casc) - s((wave == 2026) & ~casc))
    share = np.average(casc[wave == 2026].astype(float), weights=w[wave == 2026])
    return {"extra_fall": float(did), "credited_to_crowding": float(did * share)}


def unweighted(J):
    s = J[~J["sat"].isna()]
    a = s[s["wave"] == 2025]["sat"].mean() * 100
    b = s[s["wave"] == 2026]["sat"].mean() * 100
    return {"2025": float(a), "2026": float(b), "fall": float(a - b)}


def golden_family(J):
    """The licensed constructions of the golden: the pooled weighted linear model with a wave term (the
    golden), the same with service group and time band, the 2025 wave's effects, the 2026 wave's effects."""
    fam = {"pooled": A.attribute(J)["points"], "pooled+controls": A.attribute(J, controls=True)["points"],
           "2025 effects": A.attribute(J, how=2025)["points"], "2026 effects": A.attribute(J, how=2026)["points"]}
    return fam


def logit_family(J):
    """A weighted logit of being satisfied with the same terms, each driver's effect read as the average
    discrete change and carried by the change in its prevalence."""
    S = J[~J["sat"].isna()]
    w = S["weight"].values
    cols = [c for _, c in A.DRIVERS]
    X = sm.add_constant(np.column_stack([S[c].values.astype(float) for c in cols] + [(S["wave"] == 2026).values.astype(float)]))
    m = sm.GLM(S["sat"].values, X, family=sm.families.Binomial(), freq_weights=w).fit()
    d = A.attribute(J)["delta"]
    out = {}
    for j, (nm, c) in enumerate(A.DRIVERS):
        if c == "fare":
            pr = m.predict(X)
            out[nm] = float(-np.average(pr * (1 - pr), weights=w) * m.params[j + 1] * d[c] * 100)
            continue
        X1, X0 = X.copy(), X.copy()
        X1[:, j + 1], X0[:, j + 1] = 1, 0
        out[nm] = float(-np.average(m.predict(X1) - m.predict(X0), weights=w) * d[c] * 100)
    return out


def stratified(J):
    """No model: for each driver, the 2026 respondents' satisfied share with and without it within each
    combination of the other binary drivers, the gap times the change in its prevalence there, summed over the
    combinations at their 2026 shares (fares by the ticket's change, its own gap per point of change)."""
    S = J[~J["sat"].isna()]
    w = S["weight"].values
    out = {}
    binary = [("crowding", "crowded"), ("punctuality", "late"), ("on-board staffing", "unstaffed")]
    for nm, c in binary:
        others = [o for _, o in binary if o != c]
        tot = 0.0
        s26 = S["wave"].values == 2026
        for key, g in S.groupby(others):
            m = S.index.isin(g.index)
            a26, a25 = m & s26, m & ~s26
            x = S[c].values
            if not (a26 & (x == 1)).any() or not (a26 & (x == 0)).any():
                continue
            gap = (np.average(S["sat"].values[a26 & (x == 1)], weights=w[a26 & (x == 1)]) -
                   np.average(S["sat"].values[a26 & (x == 0)], weights=w[a26 & (x == 0)]))
            d = np.average(x[a26], weights=w[a26]) - np.average(x[a25], weights=w[a25])
            tot += -gap * d * w[a26].sum() / w[s26].sum()
        out[nm] = float(tot * 100)
    return out
