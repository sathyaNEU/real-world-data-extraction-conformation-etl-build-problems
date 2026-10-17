"""The index constructions for task264, shared by the checks and the goldens: the GEKS-Tornqvist change of a category in
a format with the elementary price taken at four grains (the item pooled over the format's stores, the same over the
stores in the panel all window, the item at each store, the item at the chain that prices it), plus the variants the
convergence and neutrality checks run."""
from __future__ import annotations

import numpy as np
import pandas as pd

import common as K


def movement_frame(T):
    """The clean truth as one row per code, line and week sold: store, chain, format, line code, category, week,
    units, dollars, marked-down units, promotion and price-check flags."""
    items = T["items"]
    cat = np.array([it["cat"] for it in items])
    code = np.array([it["code"] for it in items])
    parts = []
    for x in T["sold"]:
        i, t = np.nonzero(x["units"] > 0)
        parts.append(pd.DataFrame(dict(
            store=x["code"], chain=x["chain"], fmt=x["fmt"], site=x["site"], item=code[i], cat=cat[i], t=t,
            units=x["units"][i, t], dollars=x["dollars"][i, t], md=x["md"][i, t], mdflag=x["mdflag"][i, t],
            promo=x["promo"][i, t], check=x["check"][i, t])))
    return pd.concat(parts, ignore_index=True)


def geks_change(P, Q):
    """P, Q: products x weeks (price where sold, quantity; nan and 0 elsewhere). Each pair of weeks is compared by a
    Tornqvist index over the products sold in both, each weighted by the mean of its shares of spending on them in the
    two weeks; GEKS takes the geometric mean over every bridging week; the change is the mean of the last four weeks'
    index over the mean of the first four, less one, in per cent."""
    ok = (Q > 0) & np.isfinite(P)
    n = P.shape[1]
    E = np.where(ok, P * Q, 0.0)
    L = np.where(ok, np.log(np.where(ok, P, 1.0)), 0.0)
    lnB = np.zeros((n, n))
    for a in range(n):
        m = ok[:, a:a + 1] & ok
        Ea = np.where(m, E[:, a:a + 1], 0.0)
        Eb = np.where(m, E, 0.0)
        sa, sb = Ea.sum(0), Eb.sum(0)
        with np.errstate(invalid="ignore", divide="ignore"):
            w = 0.5 * (Ea / sa + Eb / sb)
        lnB[a] = np.nansum(np.where(m, w * (L - L[:, a:a + 1]), 0.0), axis=0)
    lvl = (lnB[0][:, None] + lnB).mean(axis=0)        # ln GEKS(0, t) = mean over s of [ln B(0, s) + ln B(s, t)]
    I = np.exp(lvl - lvl[0])
    return 100.0 * (I[-4:].mean() / I[:4].mean() - 1.0)


def matrices(df, key):
    """Per (category, format): the product matrices for a product key (a list of columns besides the line)."""
    g = df.groupby(["cat", "fmt", "item"] + key + ["t"], sort=True)[["units", "dollars"]].sum().reset_index()
    out = {}
    for (cat, fmt), d in g.groupby(["cat", "fmt"], sort=True):
        inv = d.groupby(["item"] + key, sort=True).ngroup().to_numpy()
        n = int(inv.max()) + 1
        Q = np.zeros((n, K.W))
        D = np.zeros((n, K.W))
        np.add.at(Q, (inv, d["t"].to_numpy()), d["units"].to_numpy())
        np.add.at(D, (inv, d["t"].to_numpy()), d["dollars"].to_numpy())
        with np.errstate(invalid="ignore", divide="ignore"):
            P = np.where(Q > 0, D / Q, np.nan)
        out[(cat, fmt)] = (P, Q)
    return out


def changes(df, grain):
    """grain: pooled (the line over the format's stores), balanced (the same over the stores with rows in all 52
    weeks), store (the line at each store), chain (the line at each chain)."""
    if grain == "pooled":
        M = matrices(df, [])
    elif grain == "balanced":
        weeks = df.groupby("store")["t"].nunique()
        keep = set(weeks[weeks == K.W].index)
        M = matrices(df[df["store"].isin(keep)], [])
    elif grain == "store":
        M = matrices(df, ["store"])
    elif grain == "site":
        M = matrices(df, ["site"])
    elif grain == "chain":
        M = matrices(df, ["chain"])
    else:
        raise ValueError(grain)
    return {k: geks_change(*v) for k, v in M.items()}


def chain_each(df):
    """Variant: each chain's own GEKS change of the category, combined across the chains in the format by their window
    spending on it (a chain absent from the window's first weeks has no change of its own and is left out)."""
    M = matrices(df, ["chain"])
    out = {}
    for (cat, fmt), _ in M.items():
        d = df[(df["cat"] == cat) & (df["fmt"] == fmt)]
        ch, wt = [], []
        for c, dc in d.groupby("chain"):
            if dc["t"].min() > 0:
                continue
            P, Q = matrices(dc, [])[(cat, fmt)]
            ch.append(geks_change(P, Q))
            wt.append(dc["dollars"].sum())
        out[(cat, fmt)] = float(np.dot(ch, wt) / np.sum(wt))
    return out


def store_imputed(df):
    """Variant: the line at each store, a week the store sold none carrying its chain's price at no quantity."""
    out = {}
    g = df.groupby(["cat", "fmt", "item", "chain", "t"])[["units", "dollars"]].sum()
    cp = (g["dollars"] / g["units"]).rename("cprice")
    s = df.groupby(["cat", "fmt", "item", "chain", "store", "t"])[["units", "dollars"]].sum().reset_index()
    for (cat, fmt), d in s.groupby(["cat", "fmt"]):
        prods = d[["item", "chain", "store"]].drop_duplicates().reset_index(drop=True)
        prods["pid"] = np.arange(len(prods))
        d = d.merge(prods, on=["item", "chain", "store"])
        Q = np.zeros((len(prods), K.W))
        np.add.at(Q, (d["pid"].to_numpy(), d["t"].to_numpy()), d["units"].to_numpy())
        c = cp.loc[(cat, fmt)].reset_index()
        P = np.full((len(prods), K.W), np.nan)
        lookup = {(a, b, t): v for a, b, t, v in c[["item", "chain", "t", "cprice"]].itertuples(index=False)}
        first = d.groupby("pid")["t"].min().to_dict()
        last = d.groupby("pid")["t"].max().to_dict()
        for row in prods.itertuples(index=False):
            for t in range(first[row.pid], last[row.pid] + 1):
                v = lookup.get((row.item, row.chain, t))
                if v is not None:
                    P[row.pid, t] = v
        Qe = np.where(np.isfinite(P) & (Q == 0), 1e-12, Q)
        out[(cat, fmt)] = geks_change(P, Qe)
    return out


def verdicts(ch, weights=None):
    """Per category: the national change (the format changes combined with the committee's weights), each format's
    gap to it, the largest absolute gap and whether every gap is within the tolerance."""
    w = weights or K.FORMAT_WEIGHTS
    tot = sum(w.values())
    res = {}
    for cat in K.CATS:
        nat = sum(w[f] * ch[(cat, f)] for f in K.FORMATS) / tot
        gaps = {f: ch[(cat, f)] - nat for f in K.FORMATS}
        worst = max(abs(g) for g in gaps.values())
        res[cat] = dict(national=nat, gaps=gaps, worst=worst, publish=worst <= K.TOLERANCE)
    return res


def published(v):
    return [c for c in K.CATS if v[c]["publish"]]
