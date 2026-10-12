"""The ask: for the council-funded residents in each locality's care homes on 31 December 2026, residential and
nursing, the average weekly contribution they were assessed to pay and the average weekly cost of their places to the
partnership after it. The golden and every designed stop, from the shipped tables."""
import numpy as np
import pandas as pd

import readpack as RP
import world as W

CELLS = [(loc, ct) for loc in W.LOCS for ct in ("Residential", "Nursing")]


def residents(pl, cw, dl, types=("PERM",), use_deaths=True):
    """council-funded residents on 31 December 2026 with the episode in place that day"""
    st = RP.stays(pl, cw, dl, types=types, use_deaths=use_deaths)
    out = []
    for s in st:
        if not (s["entry"] <= W.ASOF < s["exit"]):
            continue
        ep = None
        for r in s["rows"]:
            if RP.day(r.start_date) <= W.ASOF and (r.end_date == "" or RP.day(r.end_date) >= W.ASOF):
                ep = r
        if ep is None:
            ep = s["rows"][-1]
        out.append(dict(cl=s["cl"], svc=ep.service_no, care=ep.care_type, fee=float(ep.weekly_fee), team=ep.locality,
                        ptype=s["ptype"]))
    return out


def home_locality(reg, lookup, active_only=False):
    lk = dict(zip(lookup["postcode"], lookup["locality"]))
    out = {}
    for r in reg.itertuples(index=False):
        if active_only and r.cancelled:
            continue
        out[r.service_no] = lk.get(r.postcode)
    return out


def contributions(ass, cw, how="inforce", refs="all"):
    """the weekly contribution of each person: the assessment in force on 31 December 2026 (latest effective on or
    before it, as the records stand), or the latest completed by the extract"""
    by_client = {}
    for r in cw.itertuples(index=False):
        if not r.debtor_ref:
            continue
        tgt = r.merged_into or r.client_id
        if refs == "one" and r.merged_into:
            continue
        by_client.setdefault(tgt, []).append(r.debtor_ref)
    a = ass[ass["outcome"] != "SELF"].copy()
    a["eff"] = [RP.day(v) for v in a["effective_from"]]
    a["comp"] = [RP.day(v) for v in a["completed"]]
    by_ref = {k: g for k, g in a.groupby("debtor_ref")}
    out = {}
    for cl, rs in by_client.items():
        parts = [by_ref[x] for x in rs if x in by_ref]
        if not parts:
            continue
        g = pd.concat(parts)
        if how == "inforce":
            g = g[g["eff"] <= W.ASOF]
            if len(g) == 0:
                continue
            g = g.sort_values(["eff", "comp"], kind="stable")
        else:
            g = g.sort_values(["comp", "eff"], kind="stable")
        v = g.iloc[-1]["weekly_contribution"]
        out[cl] = float(v) if v != "" else 0.0
    return out


def compute(T, group="home", contrib="inforce", refs="all", active_only=False, fee="contract", types=("PERM",),
            use_deaths=True, drop_mismatch=False, return_counts=False):
    """T: dict of the shipped tables. Returns {(locality, care): (contribution, net)}"""
    res = residents(T["pl"], T["cw"], T["dl"], types=types, use_deaths=use_deaths)
    hl = home_locality(T["reg"], T["lookup"], active_only)
    con = contributions(T["ass"], T["cw"], contrib, refs)
    rate = {"Residential": W.NCHC[2026][0], "Nursing": W.NCHC[2026][1]}
    acc = {c: [] for c in CELLS}
    for r in res:
        home_loc = hl.get(r["svc"])
        if drop_mismatch and home_loc != r["team"]:
            continue
        loc = home_loc if group == "home" else r["team"]
        if loc is None:
            continue
        c = con.get(r["cl"], 0.0)
        f = r["fee"] if fee == "contract" else rate[r["care"]]
        acc[(loc, r["care"])].append((c, f - c))
    out = {}
    for k, v in acc.items():
        a = np.array(v) if v else np.zeros((0, 2))
        out[k] = (a[:, 0].mean(), a[:, 1].mean()) if len(a) else (np.nan, np.nan)
    if return_counts:
        return out, {k: len(v) for k, v in acc.items()}
    return out


STOPS = {
    "s1": dict(group="team"),
    "s2": dict(group="team", contrib="latest"),
    "s3": dict(contrib="latest"),
    "s4": dict(active_only=True),
    "s5": dict(fee="schedule"),
    "o1": dict(drop_mismatch=True),
    "lazy": dict(group="team", contrib="latest", fee="schedule"),
}
HAZARDS = {"primary": dict(group="team"), "h1": dict(contrib="latest"), "h2": dict(refs="one"),
           "h3": dict(active_only=True), "h4": dict(fee="schedule")}
NECESSITY = {
    "placements_locality": dict(group="team"),
    "assessments_latest": dict(contrib="latest"),
    "crosswalk_one_ref": dict(refs="one"),
    "register_active_only": dict(active_only=True),
    "lookup_unread": dict(group="team"),
    "deaths_unread": dict(use_deaths=False),
    "definitions_interim_kept": dict(types=("PERM", "INT")),
    "codes_unread": dict(types=("PERM", "INT", "RESP")),
}


def vec(out):
    """the 20 figures in the order the workbook lists them: by locality, residential then nursing, contribution then
    net"""
    v = []
    for loc in W.LOCS:
        for ct in ("Residential", "Nursing"):
            v += [out[(loc, ct)][0], out[(loc, ct)][1]]
    return np.array(v)


def chart(out):
    """nursing net weekly cost by locality, dearest first"""
    order = sorted(W.LOCS, key=lambda l: -out[(l, "Nursing")][1])
    return order, order[0]


def kept(v, g):
    return int((np.round(v) == np.round(g)).sum())


def table(T):
    """one row per resident on 31 December 2026 under the widest reading (every placement type, deaths unread), with
    every variant of each quantity, so the stops can be recomputed quickly"""
    wide = residents(T["pl"], T["cw"], T["dl"], types=("PERM", "INT", "RESP"), use_deaths=False)
    alive = {r["cl"] for r in residents(T["pl"], T["cw"], T["dl"], types=("PERM", "INT", "RESP"), use_deaths=True)}
    hl = home_locality(T["reg"], T["lookup"])
    ha = home_locality(T["reg"], T["lookup"], active_only=True)
    cin, clat = contributions(T["ass"], T["cw"], "inforce"), contributions(T["ass"], T["cw"], "latest")
    cin1, clat1 = contributions(T["ass"], T["cw"], "inforce", "one"), contributions(T["ass"], T["cw"], "latest", "one")
    rate = {"Residential": W.NCHC[2026][0], "Nursing": W.NCHC[2026][1]}
    rows = []
    for r in wide:
        rows.append(dict(cl=r["cl"], ptype=r["ptype"], dead_unread=r["cl"] not in alive, team=r["team"],
                         home=hl.get(r["svc"]), home_active=ha.get(r["svc"]), care=r["care"], fee=r["fee"],
                         sched=rate[r["care"]], c_in=cin.get(r["cl"], 0.0), c_lat=clat.get(r["cl"], 0.0),
                         c_in1=cin1.get(r["cl"], 0.0), c_lat1=clat1.get(r["cl"], 0.0), svc=r["svc"]))
    return pd.DataFrame(rows)


def fast(df, group="home", contrib="inforce", refs="all", active_only=False, fee="contract", types=("PERM",),
         use_deaths=True, drop_mismatch=False):
    m = df["ptype"].isin(types).values.copy()
    if use_deaths:
        m &= ~df["dead_unread"].values
    hl = (df["home_active"] if active_only else df["home"]).values
    if drop_mismatch:
        m &= (hl == df["team"].values)
    loc = hl if group == "home" else df["team"].values
    col = {("inforce", "all"): "c_in", ("latest", "all"): "c_lat", ("inforce", "one"): "c_in1", ("latest", "one"): "c_lat1"}[(contrib, refs)]
    c = df[col].values
    f = df["fee"].values if fee == "contract" else df["sched"].values
    out = {}
    for cell in CELLS:
        k = m & (loc == cell[0]) & (df["care"].values == cell[1])
        out[cell] = (c[k].mean(), (f[k] - c[k]).mean()) if k.any() else (np.nan, np.nan)
    return out
