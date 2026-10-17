"""task239 analysis from the shipped files: the returns that count, the structure check's teams and returns, each
item's team-level loading, the rungs a solver stops on, and every ask figure."""
import datetime as dt
import os

import numpy as np
import pandas as pd

import params as P

ITEM_CODES = [it[0] for it in P.ITEMS]
NEG = {it[0] for it in P.ITEMS if it[2]}
ONLINE_TC = ["Q3%s" % c for c in "abcdefghijkl"]
PAPER_TC = ["Q3_%02d" % k for k in range(1, 13)]
LINE = 0.75


# ---------------------------------------------------------------------------------------------- factor fits
def paf(S, iters=20000):
    d = np.sqrt(np.clip(np.diag(S), 1e-12, None))
    R = S / np.outer(d, d)
    h = np.clip(1 - 1 / np.diag(np.linalg.inv(R)), 0.05, 0.99)
    lam = None
    for _ in range(iters):
        Rr = R.copy()
        np.fill_diagonal(Rr, h)
        w, v = np.linalg.eigh(Rr)
        lam = v[:, -1] * np.sqrt(max(w[-1], 0))
        hn = lam ** 2
        if np.max(np.abs(hn - h)) < 1e-13:
            break
        h = hn
    return lam if lam.sum() > 0 else -lam


def ml1(S, iters=50000):
    d = np.sqrt(np.diag(S))
    R = S / np.outer(d, d)
    lam = paf(R) * 0.98
    psi = np.clip(1 - lam ** 2, 0.02, None)
    for _ in range(iters):
        Sig = np.outer(lam, lam) + np.diag(psi)
        b = lam @ np.linalg.inv(Sig)
        ezz = 1 - b @ lam + b @ R @ b
        exz = R @ b
        ln = exz / ezz
        pn = np.clip(np.diag(R) - ln * exz, 0.001, None)
        if np.max(np.abs(ln - lam)) < 1e-13:
            lam, psi = ln, pn
            break
        lam, psi = ln, pn
    return lam if lam.sum() > 0 else -lam


def pca1(S):
    d = np.sqrt(np.diag(S))
    w, v = np.linalg.eigh(S / np.outer(d, d))
    lam = v[:, -1] * np.sqrt(w[-1])
    return lam if lam.sum() > 0 else -lam


def decompose(Y, g):
    ut, inv = np.unique(g, return_inverse=True)
    G, n, N, J = len(ut), np.bincount(inv), len(Y), Y.shape[1]
    M = np.zeros((G, J))
    for j in range(J):
        M[:, j] = np.bincount(inv, Y[:, j]) / n
    D = Y - M[inv]
    SPW = D.T @ D / (N - G)
    Dm = M - Y.mean(0)
    SB = (Dm * n[:, None]).T @ Dm / (G - 1)
    c = (N ** 2 - (n ** 2).sum()) / (N * (G - 1))
    return dict(SPW=SPW, SB=SB, c=c, M=M, n=n, inv=inv, G=G, N=N)


def between(Y, g):
    d = decompose(Y, g)
    return (d["SB"] - d["SPW"]) / d["c"], d


def crosshalf(Y, g, seed=0):
    d = decompose(Y, g)
    rng = np.random.default_rng(seed)
    n, inv, G, J = d["n"], d["inv"], d["G"], Y.shape[1]
    order = np.argsort(inv, kind="stable")
    starts = np.r_[0, np.cumsum(n)[:-1]]
    Ys = Y[order]
    ha, hb, ok = np.zeros((G, J)), np.zeros((G, J)), np.zeros(G, bool)
    for t in range(G):
        rows = Ys[starts[t]:starts[t] + n[t]]
        p = rng.permutation(n[t])
        k = n[t] // 2
        if k >= 2:
            ha[t], hb[t], ok[t] = rows[p[:k]].mean(0), rows[p[k:]].mean(0), True
    A_ = ha[ok] - ha[ok].mean(0)
    B_ = hb[ok] - hb[ok].mean(0)
    return (A_.T @ B_ + B_.T @ A_) / (2 * (ok.sum() - 1))


# ---------------------------------------------------------------------------------------------- the files
def load(target, FILES):
    p = lambda k: os.path.join(target, FILES[k])
    D = dict(
        sessions=pd.read_csv(p("sessions"), dtype=str, keep_default_na=False),
        answers=pd.read_csv(p("answers"), dtype=str, keep_default_na=False),
        paper=pd.read_csv(p("paper"), dtype=str, keep_default_na=False),
        packs=pd.read_csv(p("packs"), dtype=str, keep_default_na=False),
        register=pd.read_csv(p("register"), dtype=str, keep_default_na=False),
        reorg=pd.read_csv(p("reorg"), dtype=str, keep_default_na=False),
        tablets=pd.read_csv(p("tablets"), dtype=str, keep_default_na=False),
    )
    return D


def norm_code(x):
    return "".join(ch for ch in str(x).upper() if ch.isalnum())


def site_switch(D):
    """the moment the tablets' second team list (the September structure) was loaded: the last load event"""
    t = D["tablets"]
    loads = t[t["event"] == "team list loaded"].copy()
    loads["at"] = pd.to_datetime(loads["at_local"])
    last = loads.groupby("tablet")["at"].max()
    return last.max().to_pydatetime() - dt.timedelta(hours=P.UTC_OFFSET), last


def all_returns(D, submitted_only=True, scale="golden"):
    """every submitted online session and every scanned form, one row each, with its scored answers; scale names a
    way of reading the codes (the golden, or one of the slips the checks run)"""
    S, A, Pp = D["sessions"], D["answers"], D["paper"]
    sub = S[S["status"] == "submitted"].copy() if submitted_only else S.copy()
    tc = A[A["question"].isin(ONLINE_TC)].pivot(index="session_id", columns="question", values="response")
    tc = tc.reindex(sub["session_id"])[ONLINE_TC]
    sub_t = sub["submitted_utc"].where(sub["submitted_utc"] != "", sub["started_utc"])
    on = pd.DataFrame({"rid": sub["session_id"].values, "channel": sub["link_type"].values,
                       "received": pd.to_datetime(sub_t.str.replace("Z", "")).values,
                       "started": pd.to_datetime(sub["started_utc"].str.replace("Z", "")).values,
                       "code": sub["team_code"].values, "inv": sub["inv_code"].values,
                       "entered": sub["entered_code"].values, "tablet_ref": sub["tablet_ref"].values})
    hi = 6 if scale == "dk_value" else 5
    for k, q in enumerate(ONLINE_TC):
        v = pd.to_numeric(tc[q].values, errors="coerce")
        v = np.where((v >= 1) & (v <= hi), v, np.nan)
        neg = ITEM_CODES[k] in NEG and scale != "neg_not_reversed"
        on[ITEM_CODES[k]] = 6 - v if neg else v
    pk = D["packs"].set_index("form_serial")["team_code"]
    pa = pd.DataFrame({"rid": "F" + Pp["form_serial"].values, "channel": "paper",
                       "received": (pd.to_datetime(Pp["scanned_at"]) - pd.Timedelta(hours=P.UTC_OFFSET)).values,
                       "started": pd.NaT, "code": Pp["form_serial"].map(pk).fillna("").values, "inv": "", "entered": "",
                       "tablet_ref": "", "serial": Pp["form_serial"].values})
    for k, q in enumerate(PAPER_TC):
        v = pd.to_numeric(Pp[q].values, errors="coerce")
        if scale == "paper_raw_codes":
            v = np.where((v >= 1) & (v <= 9), v, np.nan)
        elif scale == "dk_value":
            v = np.where((v >= 1) & (v <= 6), v, np.nan)
        else:
            v = np.where((v >= 1) & (v <= 5), v, np.nan)
        neg = ITEM_CODES[k] in NEG and scale != "neg_not_reversed"
        pa[ITEM_CODES[k]] = 6 - v if neg else v
    pa["any_answer"] = (Pp[[c for c in Pp.columns if c.startswith("Q")]] != "9").any(axis=1).values
    on["any_answer"] = True
    pa["scanned_date"] = pd.to_datetime(Pp["scanned_at"]).dt.date.values
    return pd.concat([on, pa], ignore_index=True)


def counted(D, member=True, replay=True, late=True, blank=True, resubmit=True, submitted_only=True, scale="golden"):
    """the returns that count (standard section 3); switches turn each rule off to give the rungs"""
    R = all_returns(D, submitted_only=submitted_only, scale=scale)
    keep = np.ones(len(R), bool)
    if late:
        keep &= ~((R["channel"] == "paper") & (pd.to_datetime(R["scanned_date"]) > pd.Timestamp(P.PAPER_DEADLINE)))
    if blank:
        keep &= R["any_answer"].values
    R = R[keep].copy()
    # one copy of a session a tablet sent twice (identical answers, so either copy)
    if replay:
        site = R["channel"] == "site"
        first = R[site].sort_values("received").drop_duplicates("tablet_ref", keep="first")
        R = pd.concat([R[~site], first]).sort_values(["received", "rid"])
    # the member behind each return: personal link code, the code typed on a tablet, the pack a form was posted in
    packs = D["packs"].set_index("form_serial")["inv_code"]
    known = set(D["sessions"]["inv_code"]) | set(D["packs"]["inv_code"])
    known.discard("")
    mem = np.where(R["channel"] == "personal", R["inv"], "")
    typed = R["entered"].map(norm_code)
    mem = np.where((R["channel"] == "site") & typed.isin(known), typed, mem)
    ser = R.get("serial")
    mem = np.where(R["channel"] == "paper", ser.map(packs).fillna("").values if ser is not None else "", mem)
    R["member"] = mem
    if resubmit and member:
        has = R["member"] != ""
        last = R[has].sort_values(["received", "rid"]).drop_duplicates("member", keep="last")
        R = pd.concat([R[~has], last])
    elif resubmit:
        pers = R["channel"] == "personal"
        last = R[pers].sort_values(["received", "rid"]).drop_duplicates("inv", keep="last")
        R = pd.concat([R[~pers], last])
    return R.sort_values(["received", "rid"]).reset_index(drop=True)


def resolve(D, R, site_rule="switch", paper_rule="map"):
    """each return's September team (standard 3.4): personal links carry September codes; tablets carried the July
    list until the second load; forms carry the printed July code; July codes go through the reorganisation map"""
    reg = set(D["register"]["team_code"])
    mp = D["reorg"]
    old = mp[mp["old_code"] != ""].groupby("old_code")["new_code"].agg(list).to_dict()

    def through_map(c):
        if c in old:
            succ = sorted(set(old[c]))
            return succ[0] if len(succ) == 1 else None
        return c if c in reg else None

    def raw(c):
        if c in reg:
            return c
        return through_map(c)

    switch, _ = site_switch(D)
    team = []
    for ch, c, st in zip(R["channel"], R["code"], R["started"]):
        if ch == "personal":
            team.append(c if c in reg else None)
        elif ch == "site":
            if site_rule == "switch":
                team.append(through_map(c) if pd.Timestamp(st) < pd.Timestamp(switch) else (c if c in reg else None))
            elif site_rule == "raw":
                team.append(raw(c))
            else:
                team.append(through_map(c))
        else:
            team.append(through_map(c) if paper_rule == "map" else raw(c))
    R = R.copy()
    R["team"] = team
    return R


def population(R, floor=5):
    has = R["team"].notna()
    cnt = R[has].groupby("team").size()
    rep = set(cnt[cnt >= floor].index)
    R = R.copy()
    R["reported"] = R["team"].isin(rep)
    R["complete"] = R[ITEM_CODES].notna().all(axis=1)
    R["used"] = R["reported"] & R["complete"]
    return R, rep


def scores(R):
    U = R[R["used"]]
    return U[ITEM_CODES].values.astype(float), U["team"].values


def loadings(Y, g, how="muml_paf"):
    if how == "pooled":
        return paf(np.cov(Y.T))
    d = decompose(Y, g)
    if how == "means":
        return paf(np.cov(d["M"].T))
    if how == "means_pca":
        return pca1(np.cov(d["M"].T))
    if how == "means_w":
        w = d["n"] / d["n"].sum()
        Mc = d["M"] - w @ d["M"]
        return paf((Mc * w[:, None]).T @ Mc)
    if how == "means_n10":
        big = d["n"] >= 10
        return paf(np.cov(d["M"][big].T))
    SigB = (d["SB"] - d["SPW"]) / d["c"]
    if how == "within":
        return paf(d["SPW"])
    if how in ("disatt", "disatt_h"):
        icc = np.diag(SigB) / (np.diag(SigB) + np.diag(d["SPW"]))
        nb = d["n"].mean() if how == "disatt" else len(d["n"]) / np.sum(1.0 / d["n"])
        rel = nb * icc / (1 + (nb - 1) * icc)
        Rm = np.corrcoef(d["M"].T)
        Rd = Rm / np.sqrt(np.outer(rel, rel))
        np.fill_diagonal(Rd, 1)
        return paf(Rd)
    if how == "blup":
        lam = (np.diag(SigB)[None, :] * d["n"][:, None]) / (np.diag(SigB)[None, :] * d["n"][:, None]
                                                              + np.diag(d["SPW"])[None, :])
        return paf(np.cov((Y.mean(0) + lam * (d["M"] - Y.mean(0))).T))
    if how == "muml_paf":
        return paf(SigB)
    if how == "muml_ml":
        return ml1(SigB)
    if how == "muml_pca":
        return pca1(SigB)
    if how == "unweighted":
        return paf(np.cov(d["M"].T) - d["SPW"] * np.mean(1 / d["n"]))
    if how == "crosshalf":
        return paf(crosshalf(Y, g))
    raise ValueError(how)


ROUTES = ["pooled", "within", "means", "means_pca", "means_w", "means_n10", "disatt", "blup",
          "muml_paf", "muml_ml", "muml_pca", "unweighted", "crosshalf"]
GOLDEN_ROUTES = ["muml_paf", "muml_ml", "muml_pca", "unweighted", "crosshalf"]


def verdict(lam):
    return [c for c, l in zip(ITEM_CODES, lam) if l >= LINE]


# ---------------------------------------------------------------------------------------------- the asks
def ledger(R):
    out = {}
    for ch in ("personal", "site", "paper"):
        x = R[R["channel"] == ch]
        out[ch] = dict(count=int(len(x)), outside=int((~x["reported"]).sum()),
                       incomplete=int((x["reported"] & ~x["complete"]).sum()), used=int(x["used"].sum()))
    return out


def favourable(R):
    """company-wide, every return that counts: each item's answers on the scale and the favourable ones among them"""
    out = {}
    for it in ITEM_CODES:
        v = R[it].dropna()
        out[it] = dict(base=int(len(v)), fav=int((v >= 4).sum()))
    return out


def divisions(D, R, rule="census"):
    reg = D["register"].set_index("team_code")
    census = P.REORG.isoformat()

    def div(code):
        r = reg.loc[code]
        if rule == "census":
            if r["division_since"] and r["division_since"] > census:
                return r["previous_division"]
            return r["division"]
        if rule == "current":
            return r["division"]
        if rule == "previous":
            return r["previous_division"] or r["division"]
        if rule == "prefix":
            return {P.PREFIX[d[0]]: d[1] for d in P.DIVISIONS}[code.split("-")[0]]
        raise ValueError(rule)

    used = R[R["used"]]
    rep = sorted(set(R.loc[R["reported"], "team"]))
    out = {d[1]: dict(teams=0, used=0) for d in P.DIVISIONS}
    for t in rep:
        out[div(t)]["teams"] += 1
    for t, k in used.groupby("team").size().items():
        out[div(t)]["used"] += int(k)
    return out


def solve(target, FILES):
    D = load(target, FILES)
    R = resolve(D, counted(D))
    R, rep = population(R)
    Y, g = scores(R)
    X = dict(D=D, R=R, reported=rep, Y=Y, g=g, files=FILES)
    X["lam"] = {h: loadings(Y, g, h) for h in ROUTES}
    X["golden"] = X["lam"]["muml_paf"]
    X["stay"] = verdict(X["golden"])
    X["ledger"] = ledger(R)
    X["fav"] = favourable(R)
    X["div"] = divisions(D, R)
    return X
