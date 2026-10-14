"""The ask: for the council-funded residents in each locality's care homes on 31 December 2026, residential and
nursing, the average weekly fee for their places and the average weekly cost of those places to the partnership after
the contributions the residents were assessed to pay. The golden and every designed stop, from the shipped tables."""
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


def fee_of(r, how):
    """the weekly fee of a resident's 31 December 2026 episode: 'agreed' the 2026-27 rate agreed on 6 November 2026 and
    backdated to 1 April 2026, with the resident's supplement (the episode's fee less the interim rate it was entered
    at); 'register' the fee on the episode; 'schedule' the agreed rate alone; 'offer' the draft 2027-28 rate with the
    supplement"""
    k = 1 if r["care"] == "Nursing" else 0
    if how == "register":
        return r["fee"]
    supp = r["fee"] - W.NCHC_INTERIM_2026[k]
    if how == "schedule":
        return W.NCHC[2026][k]
    if how == "offer":
        return W.NCHC_DRAFT_2027[k] + supp
    return W.NCHC[2026][k] + supp


def compute(T, group="home", contrib="inforce", refs="all", active_only=False, fee="agreed", types=("PERM",),
            use_deaths=True, drop_mismatch=False, return_counts=False):
    """T: dict of the shipped tables. Returns {(locality, care): (fee, net)}"""
    res = residents(T["pl"], T["cw"], T["dl"], types=types, use_deaths=use_deaths)
    hl = home_locality(T["reg"], T["lookup"], active_only)
    con = contributions(T["ass"], T["cw"], contrib, refs)
    acc = {c: [] for c in CELLS}
    for r in res:
        home_loc = hl.get(r["svc"])
        if drop_mismatch and home_loc != r["team"]:
            continue
        loc = home_loc if group == "home" else r["team"]
        if loc is None:
            continue
        c = con.get(r["cl"], 0.0)
        f = fee_of(r, fee)
        acc[(loc, r["care"])].append((f, f - c))
    out = {}
    for k, v in acc.items():
        a = np.array(v) if v else np.zeros((0, 2))
        out[k] = (a[:, 0].mean(), a[:, 1].mean()) if len(a) else (np.nan, np.nan)
    if return_counts:
        return out, {k: len(v) for k, v in acc.items()}
    return out


STOPS = {
    "s1": dict(fee="register"),
    "s2": dict(group="team"),
    "s3": dict(contrib="latest"),
    "s4": dict(active_only=True),
    "s5": dict(fee="schedule"),
    "s6": dict(fee="offer"),
    "o1": dict(drop_mismatch=True),
    "lazy": dict(group="team", contrib="latest", fee="register"),
}
HAZARDS = {"primary": dict(fee="register"), "second": dict(group="team"), "h1": dict(contrib="latest"),
           "h2": dict(refs="one"), "h3": dict(active_only=True), "h4": dict(fee="schedule")}
NECESSITY = {
    "placements_fee_as_entered": dict(fee="register"),
    "placements_locality": dict(group="team"),
    "assessments_latest": dict(contrib="latest"),
    "crosswalk_one_ref": dict(refs="one"),
    "register_active_only": dict(active_only=True),
    "lookup_unread": dict(group="team"),
    "rates_unread": dict(fee="register"),
    "deaths_unread": dict(use_deaths=False),
    "definitions_interim_kept": dict(types=("PERM", "INT")),
    "codes_unread": dict(types=("PERM", "INT", "RESP")),
}


def vec(out):
    """the 20 figures in the order the workbook lists them: by locality, residential then nursing, fee then net"""
    v = []
    for loc in W.LOCS:
        for ct in ("Residential", "Nursing"):
            v += [out[(loc, ct)][0], out[(loc, ct)][1]]
    return np.array(v)


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
    rows = []
    for r in wide:
        rows.append(dict(cl=r["cl"], ptype=r["ptype"], dead_unread=r["cl"] not in alive, team=r["team"],
                         home=hl.get(r["svc"]), home_active=ha.get(r["svc"]), care=r["care"], fee=fee_of(r, "agreed"),
                         reg=fee_of(r, "register"), sched=fee_of(r, "schedule"), offer=fee_of(r, "offer"),
                         c_in=cin.get(r["cl"], 0.0), c_lat=clat.get(r["cl"], 0.0), c_in1=cin1.get(r["cl"], 0.0),
                         c_lat1=clat1.get(r["cl"], 0.0), svc=r["svc"]))
    return pd.DataFrame(rows)
