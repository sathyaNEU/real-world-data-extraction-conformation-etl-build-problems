"""task240 estimators: each published estimate and its coefficient of variation by every route the checks run (the
golden is the post-stratified estimator's Taylor linearisation), and the fieldwork figures the asks owe."""
import numpy as np
import pandas as pd

import params as P

IND = [i[0] for i in P.INDICATORS]
LINE = P.LINE


def indicators(df):
    """1 where the adult counts in the published estimate: a yes on the scale; don't know, refused and not asked do not"""
    return pd.DataFrame({"PEN": (df["q_pension"] == 1).astype(float), "RENT": (df["q_tenure"] == 3).astype(float),
                         "CARE": (df["q_care"] == 1).astype(float), "ARR": (df["q_arrears"] == 1).astype(float)},
                        index=df.index)


def age_group(age):
    return np.digitize(np.asarray(age), P.AGE_CUTS)


def vtot(z, stratum, psu):
    """with-replacement variance of a total from its PSU totals within strata"""
    t = pd.DataFrame({"z": z, "h": stratum, "p": psu}).groupby(["h", "p"])["z"].sum()
    g = t.groupby(level=0)
    nh = g.transform("size")
    dev = t - g.transform("mean")
    ok = nh > 1
    return float((nh[ok] / (nh[ok] - 1) * dev[ok] ** 2).sum())


def cv_table(df, w="w", cells=("region", "ag", "sex")):
    """every region-indicator estimate and its CV by each route: srs, kish, fixed (final weights held fixed),
    region (residuals within region only), golden (residuals within the post-stratification cells)"""
    Y = indicators(df)
    out = []
    for r, s in df.groupby("region"):
        ws = s[w].values
        cell = s[list(cells)].astype(str).agg("|".join, axis=1).values
        kish = len(s) * (ws ** 2).sum() / ws.sum() ** 2
        for y in IND:
            yy = Y.loc[s.index, y].values
            tot = float((ws * yy).sum())
            if tot <= 0:
                out.append(dict(region=r, ind=y, n=len(s), est=0.0)); continue
            p = tot / ws.sum()
            cm = pd.Series(ws * yy).groupby(cell).sum() / pd.Series(ws).groupby(cell).sum()
            e = yy - pd.Series(cell).map(cm).values
            rm = tot / ws.sum()
            out.append(dict(region=r, ind=y, n=len(s), est=tot, p=p,
                            srs=100 * np.sqrt((1 - p) / (len(s) * p)),
                            kish=100 * np.sqrt(kish * (1 - p) / (len(s) * p)),
                            fixed=100 * np.sqrt(vtot(ws * yy, s["stratum"].values, s["psu"].values)) / tot,
                            region_ps=100 * np.sqrt(vtot(ws * (yy - rm), s["stratum"].values, s["psu"].values)) / tot,
                            golden=100 * np.sqrt(vtot(ws * e, s["stratum"].values, s["psu"].values)) / tot))
    return pd.DataFrame(out)


def jackknife(df, N, w="w"):
    """delete-one-PSU jackknife, every replicate post-stratified again to the cell totals N (the design weights d may
    be any multiple of them within a cell, the final weights included)"""
    Y = indicators(df)
    res = {}
    for r, s in df.groupby("region"):
        cell = list(zip(s["region"], s["ag"], s["sex"]))
        Nc = np.array([N[c] for c in cell])
        d = s["d"].values
        full = {y: float((s[w].values * Y.loc[s.index, y].values).sum()) for y in IND}
        reps = []
        for h, g in s.groupby("stratum"):
            ps = g["psu"].unique()
            nh = len(ps)
            if nh < 2:
                continue
            for pp in ps:
                d2 = d.copy()
                out_m = (s["stratum"].values == h) & (s["psu"].values == pp)
                in_m = (s["stratum"].values == h) & ~out_m
                d2[out_m] = 0.0
                d2[in_m] *= nh / (nh - 1)
                sd = pd.Series(d2).groupby(pd.Series([str(c) for c in cell])).transform("sum").values
                w2 = np.where(sd > 0, d2 * Nc / np.where(sd > 0, sd, 1), 0.0)
                reps.append((h, nh, {y: float((w2 * Y.loc[s.index, y].values).sum()) for y in IND}))
        for y in IND:
            E = pd.DataFrame([(h, nh, t[y]) for h, nh, t in reps], columns=["h", "nh", "t"])
            v = sum((g["nh"].iloc[0] - 1) / g["nh"].iloc[0] * ((g["t"] - g["t"].mean()) ** 2).sum() for _, g in E.groupby("h"))
            res[(r, y)] = 100 * np.sqrt(v) / full[y] if full[y] > 0 else np.nan
    return res


def warned(T, col):
    return sorted((r, y) for r, y, v in zip(T["region"], T["ind"], T[col]) if v >= LINE)


def frame_from_world(W):
    df = pd.DataFrame(W.adults)
    df["stratum"] = df["region"] + np.where(df["urban"] == 1, "-U", "-R")
    df["ag"] = age_group(df["age"])
    return df


# ---------------------------------------------------------------------------------------------- the fieldwork asks
ELIGIBLE = (110, 210, 220, 230)
INELIGIBLE = (410, 420, 430)
CALL_TYPES = ("VISIT", "PHONE")


def response_rates(frame, e_scope="survey"):
    """frame: one row per issued address with its region and final outcome (NaN where no outcome is held, counted with
    310 as eligibility never established); the standard's rate: full interviews over the eligible addresses, the
    addresses whose eligibility was never established counted at the eligible share e of the survey's addresses whose
    eligibility was established (e_scope "region": the region's share instead)"""
    o = frame["final"]
    e_all = o.isin(ELIGIBLE).sum() / o.isin(ELIGIBLE + INELIGIBLE).sum()
    out = {}
    for r, g in frame.groupby("region"):
        o = g["final"]
        I = int((o == 110).sum())
        E = int(o.isin(ELIGIBLE).sum())
        N = int(o.isin(INELIGIBLE).sum())
        U = int((~o.isin(ELIGIBLE + INELIGIBLE)).sum())
        e = e_all if e_scope == "survey" else E / (E + N)
        out[r] = dict(I=I, E=E, N=N, U=U, e=float(e), rr=100 * I / (E + e * U))
    return out


def calls_by_region(calls, region_of):
    """calls: one row per call; region_of: each responding address and its region"""
    c = calls[calls["address_id"].isin(region_of)]
    n = c.groupby("address_id").size().reindex(list(region_of), fill_value=0)
    s = pd.DataFrame({"n": n.values, "region": [region_of[a] for a in n.index]})
    return {r: int(g["n"].sum()) for r, g in s.groupby("region")}


def ask_files(hh, iss, out, cr, region="current", unworked=True, late=True, issues="last", dedup=True, calls_only=True,
              e_scope="survey", call_issues="all"):
    """both asks computed from the shipped files under each handling; the golden takes every default:
    region   "current" each PSU's region as the published tables give it (the households file), "code" the issued file's
    unworked True keeps issued addresses with no outcome row (eligibility never established), False drops them
    late     True takes every household in the households file as a full interview, False the extract's codes only
    issues   "last" an address's outcome is its last issue's, "first" its first issue's, "rows" every issue a row
    dedup    True counts a call written twice by a tablet once
    calls_only  True keeps visits and telephone calls, False every event in the log
    call_issues "all" every issue's calls, "last" only the calls of the address's last issue"""
    psu_reg = dict(zip(hh["psu"], hh["region"]))
    iss = iss.copy()
    if region == "current":
        iss["region"] = [psu_reg.get(p, c) for p, c in zip(iss["psu"], iss["region_code"])]
    else:
        iss["region"] = iss["region_code"]
    o = out.sort_values(["address_id", "issue_no"])
    if issues == "rows":
        fin = o[["address_id", "outcome_code"]].rename(columns={"outcome_code": "final"})
    else:
        g = o.groupby("address_id")["outcome_code"]
        fin = (g.last() if issues == "last" else g.first()).rename("final").reset_index()
    fin["final"] = fin["final"].astype(float)
    if late:
        fin.loc[fin["address_id"].isin(set(hh["hh_id"])), "final"] = 110.0
    base = iss[["address_id", "region"]].merge(fin, on="address_id", how="left" if unworked else "inner")
    rr = {r: v["rr"] for r, v in response_rates(base, e_scope).items()}
    c = cr.copy()
    if calls_only:
        c = c[c["event_type"].isin(CALL_TYPES)]
    if dedup:
        c = c.drop_duplicates(["address_id", "issue_no", "event_time", "event_type", "result", "interviewer_id"])
    if call_issues == "last":
        last = o.groupby("address_id")["issue_no"].max()
        c = c[c["issue_no"].values == last.reindex(c["address_id"]).values]
    resp = sorted(set(base.loc[base["final"] == 110, "address_id"]))
    reg = dict(zip(iss["address_id"], iss["region"]))
    return rr, calls_by_region(c, {a: reg[a] for a in resp})


# ---------------------------------------------------------------------------------------------- from the shipped files
import os  # noqa: E402


def frame_from_files(target, F):
    """the responding adults with their final weights, design variables and answers, as the analysis files give them"""
    rd = lambda k: pd.read_csv(os.path.join(target, F[k]))
    hh, mem, wt = rd("households"), rd("members"), rd("weights")
    ad = mem[mem["age"] >= 16].merge(wt, on=["hh_id", "person_no"], how="inner", validate="one_to_one")
    ad = ad.merge(hh[["hh_id", "region", "stratum", "psu", "tenure", "arrears"]], on="hh_id", how="inner",
                  validate="many_to_one")
    df = pd.DataFrame({"hh_id": ad["hh_id"], "person_no": ad["person_no"], "region": ad["region"],
                       "stratum": ad["stratum"], "psu": ad["psu"], "age": ad["age"], "sex": ad["sex"],
                       "proxy": ad["proxy"], "q_pension": ad["pension"], "q_care": ad["care"],
                       "q_tenure": ad["tenure"], "q_arrears": ad["arrears"], "w": ad["final_weight"]})
    df["ag"] = age_group(df["age"])
    df["d"] = df["w"]
    return df.reset_index(drop=True)


def cell_totals(df, w="w"):
    return {k: float(v) for k, v in df.groupby(["region", "ag", "sex"])[w].sum().items()}


def solve(target, F):
    """every owed figure from the shipped files: the 48 estimates, their CVs by every route, the warnings, and the two
    fieldwork asks"""
    df = frame_from_files(target, F)
    T = cv_table(df)
    J = jackknife(df, cell_totals(df))
    T["jk"] = [J[(r, y)] for r, y in zip(T["region"], T["ind"])]
    rd = lambda k: pd.read_csv(os.path.join(target, F[k]), dtype={"result": str})
    hh, iss, out, cr = rd("households"), rd("issued"), rd("outcomes"), rd("calls")
    cr["result"] = cr["result"].fillna("")
    rr, calls = ask_files(hh, iss, out, cr)
    return dict(df=df, T=T, warned=warned(T, "golden"), routes={c: warned(T, c) for c in
                                                             ("srs", "kish", "fixed", "region_ps", "golden", "jk")},
                rr=rr, calls=calls, hh=hh, iss=iss, out=out, cr=cr, files=F)
