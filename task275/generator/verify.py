"""task275 verifier: every graded figure recomputed with pandas from the shipped files alone, independently of the
generator's analysis and pack modules, and compared with generator/figures.json.

    python3 task275/generator/verify.py"""
from __future__ import annotations

import json
import os
import sys
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
UK = ZoneInfo("Europe/London")


def load(target):
    f = lambda n: pd.read_csv(os.path.join(target, n), dtype=str, keep_default_na=False)
    return {k: f(n) for k, n in (("reg", "vessel_register.csv"), ("trips", "elogbook_trips_2025.csv"),
                                 ("land", "elogbook_landings_2025.csv"), ("dep", "observer_deployments_2025.csv"),
                                 ("hauls", "observer_hauls_2025.csv"), ("sales", "sales_notes_2025.csv"),
                                 ("vms", "vms_positions_2025.csv"), ("tp", "vms_transponders.csv"),
                                 ("ports", "port_limits.csv"))}


def utc_to_uk(s):
    return pd.to_datetime(s).dt.tz_localize("UTC").dt.tz_convert(UK).dt.tz_localize(None)


def call(D, keep=False):
    seg = dict(zip(D["reg"]["vessel_pln"], D["reg"]["segment"]))
    tr = D["trips"].copy()
    tr["seg"] = tr["vessel_pln"].map(seg)
    tr["hours"] = tr["fishing_hours"].astype(float)
    tr["dep_uk"] = utc_to_uk(tr["departure_utc"])
    ld = D["land"].copy()
    ld["w"] = ld["live_weight_kg"].astype(float)
    ld["bms"] = ld["mcrs_status"].eq("BMS")
    agg = ld.pivot_table(index="trip_id", columns="bms", values="w", aggfunc="sum", fill_value=0.0)
    tr["mk"] = tr["trip_id"].map(agg.get(False, pd.Series(dtype=float))).fillna(0.0)
    tr["bms"] = tr["trip_id"].map(agg.get(True, pd.Series(dtype=float))).fillna(0.0)
    # observed trips: the deployment log's vessel, normalised, and the logbook departure nearest the notified one
    dep = D["dep"][D["dep"]["outcome"] == "Observed"].copy()
    m = dep["vessel_pln"].str.upper().str.extract(r"^\s*([A-Z]+)[\s-]*0*(\d+)")
    dep["pln"] = m[0] + " " + m[1].astype(int).astype(str)
    dep["when"] = pd.to_datetime(dep["notified_departure"])
    h = D["hauls"].copy()
    h["w"] = h["weight_kg"].astype(float)
    frac = h.pivot_table(index="observer_trip_ref", columns="fraction", values="w", aggfunc="sum", fill_value=0.0)
    # the haul records hold the hauls sampled: each observed trip's weighings raised to its hours fished
    hh = h.drop_duplicates(["observer_trip_ref", "haul_no"])
    sampled = ((pd.to_datetime(hh["hauled_local"]) - pd.to_datetime(hh["shot_local"])).dt.total_seconds() / 3600
               ).groupby(hh["observer_trip_ref"]).sum()
    tr["obs"] = False
    tr["o_bms"] = 0.0
    tr["o_dis"] = 0.0
    for _, r in dep.iterrows():
        c = tr[tr["vessel_pln"] == r["pln"]]
        gap = (c["dep_uk"] - r["when"]).abs()
        i = gap.idxmin()
        assert gap[i] <= pd.Timedelta(hours=12), r["deployment_ref"]
        f = tr.loc[i, "hours"] / sampled[r["observer_trip_ref"]]
        tr.loc[i, ["obs", "o_bms", "o_dis"]] = [True, frac.loc[r["observer_trip_ref"], "BMS"] * f,
                                                frac.loc[r["observer_trip_ref"], "DIS"] * f]
    out = {}
    for s, X in tr.groupby("seg"):
        O, N = X[X["obs"]], X[~X["obs"]]
        disc = O["o_dis"].sum()
        catch = (O["mk"] + O["bms"] + O["o_dis"]).sum() + N["mk"].sum()
        for g, Ng in N.groupby("po_ground"):
            Og = O[O["po_ground"] == g]
            u = (Og["o_bms"] + Og["o_dis"]).sum() / Og["hours"].sum()
            U = u * Ng["hours"].sum()
            disc += U - Ng["bms"].sum()
            catch += U
        out[s] = 100.0 * disc / catch
    return (out, tr) if keep else out


def routes(tr):
    """the golden raised by marketable landings, the observers' discards raised by hours and by landed weight, and
    each segment's marketable catch landed an hour, observed against unobserved"""
    tr = tr.assign(landed=tr["mk"] + tr["bms"])
    by_mk, r2h, r2w, par = {}, {}, {}, {}
    for s, X in tr.groupby("seg"):
        O, N = X[X["obs"]], X[~X["obs"]]
        disc = O["o_dis"].sum()
        catch = (O["mk"] + O["bms"] + O["o_dis"]).sum() + N["mk"].sum()
        for g, Ng in N.groupby("po_ground"):
            Og = O[O["po_ground"] == g]
            U = (Og["o_bms"] + Og["o_dis"]).sum() / Og["mk"].sum() * Ng["mk"].sum()
            disc += U - Ng["bms"].sum()
            catch += U
        by_mk[s] = 100.0 * disc / catch
        for col, out in (("hours", r2h), ("landed", r2w)):
            d = 0.0
            for g, Xg in X.groupby("po_ground"):
                Og = Xg[Xg["obs"]]
                if len(Og):
                    d += Og["o_dis"].sum() / Og[col].sum() * Xg[col].sum()
            out[s] = 100.0 * d / (X["landed"].sum() + d)
        par[s] = (O["mk"].sum() / O["hours"].sum(), N["mk"].sum() / N["hours"].sum())
    return by_mk, r2h, r2w, par


def two_terminals(D, apart_nm):
    v = D["vms"].assign(hr=D["vms"]["position_utc"].str[:13], la=D["vms"]["latitude"].astype(float),
                        lo=D["vms"]["longitude"].astype(float))
    n = v.groupby(["vessel_pln", "hr"])["terminal_id"].nunique()
    two = n[n >= 2]
    sub = v.set_index(["vessel_pln", "hr"]).loc[two.index].reset_index()
    apart = 0
    for _, g in sub.groupby(["vessel_pln", "hr"]):
        a, b = [x[["la", "lo"]].to_numpy() for _, x in g.groupby("terminal_id")][:2]
        dx = (a[:, None, 1] - b[None, :, 1]) * 60 * np.cos(np.radians((a[:, None, 0] + b[None, :, 0]) / 2))
        dy = (a[:, None, 0] - b[None, :, 0]) * 60
        apart += np.hypot(dx, dy).min() > apart_nm
    return two.index.get_level_values(0).nunique(), len(two), apart


def ask_a(D):
    seg = dict(zip(D["reg"]["vessel_pln"], D["reg"]["segment"]))
    s = D["sales"].copy()
    s = s[s["landing_date"].str[:4] == "2025"]
    markets = set(D["ports"].loc[D["ports"]["fish_market"] == "Y", "port_name"])
    # at a market port the market is the buyer of record; another buyer's note there repeats the market's lots
    main = (s[s["port_of_landing"].isin(markets)].groupby(["port_of_landing", "buyer_reg_no"]).size()
            .reset_index().sort_values(0).groupby("port_of_landing").tail(1))
    mk = dict(zip(main["port_of_landing"], main["buyer_reg_no"]))
    # at a market port the market sells the landing; another buyer's line for the same lot (same vessel, landing,
    # species and grade, the weight within 3 per cent) is its own record of a lot it bought there
    s = s.reset_index(drop=True)
    s["w"] = s["weight_kg"].astype(float)
    key = ["vessel_pln", "landing_date", "port_of_landing", "species", "size_grade"]
    at_mkt = s["port_of_landing"].isin(markets)
    is_mkt = at_mkt & (s["buyer_reg_no"] == s["port_of_landing"].map(mk))
    others = s[at_mkt & ~is_mkt].reset_index()
    pairs = others.merge(s[is_mkt][key + ["w"]], on=key, how="inner", suffixes=("", "_m"))
    dup = set(pairs.loc[(pairs["w"] - pairs["w_m"]).abs() <= 0.03 * pairs["w_m"], "index"])
    s = s[~s.index.isin(dup)]
    s["seg"] = s["vessel_pln"].map(seg)
    return (s.groupby("seg")["value_gbp"].apply(lambda x: x.astype(float).sum()) / 1000.0).round(1).to_dict()


def ask_b(D):
    seg = dict(zip(D["reg"]["vessel_pln"], D["reg"]["segment"]))
    v = D["vms"].copy()
    v["t"] = pd.to_datetime(v["position_utc"])
    v["la"] = v["latitude"].astype(float)
    v["lo"] = v["longitude"].astype(float)
    inside = np.zeros(len(v), dtype=bool)
    for _, p in D["ports"].iterrows():
        pla, plo, rad = float(p["harbour_lat"]), float(p["harbour_lon"]), float(p["port_limit_radius_nm"])
        dx = (v["lo"] - plo) * 60 * np.cos(np.radians((v["la"] + pla) / 2))
        dy = (v["la"] - pla) * 60
        inside |= np.hypot(dx, dy).to_numpy() <= rad
    v = v[~inside].copy()
    # the vessel that carried each terminal: the equipment record's current and previous terminals; a terminal one
    # vessel had before and another has now is split where the first vessel's own terminal starts reporting
    tp = D["tp"]
    span = D["vms"].assign(t=pd.to_datetime(D["vms"]["position_utc"])).groupby("terminal_id")["t"].agg(["min", "max"])
    cur = tp[["terminal_id", "vessel_pln"]]
    prv = tp.loc[tp["previous_terminal_id"] != "", ["previous_terminal_id", "vessel_pln"]].rename(
        columns={"previous_terminal_id": "terminal_id"})
    own = pd.concat([cur.assign(role="cur"), prv.assign(role="prev")])
    n = own.groupby("terminal_id").size()
    single = own[own["terminal_id"].map(n) == 1][["terminal_id", "vessel_pln"]]
    j = v.drop(columns="vessel_pln").merge(single, on="terminal_id")
    for u in n[n == 2].index:
        P = own[(own["terminal_id"] == u) & (own["role"] == "prev")]["vessel_pln"].iloc[0]
        Q = own[(own["terminal_id"] == u) & (own["role"] == "cur")]["vessel_pln"].iloc[0]
        p_now = tp.loc[tp["vessel_pln"] == P, "terminal_id"].iloc[0]
        q_old = tp.loc[tp["vessel_pln"] == Q, "previous_terminal_id"].iloc[0]
        x = v[v["terminal_id"] == u].drop(columns="vessel_pln").copy()
        early, late = x["t"] < span.loc[p_now, "min"], x["t"] > span.loc[q_old, "max"]
        assert (early | late).all() and not (early & late).any(), u
        x["vessel_pln"] = np.where(early, P, Q)
        j = pd.concat([j, x])
    assert not j.duplicated(["terminal_id", "position_utc"]).any()
    j["uk"] = utc_to_uk(j["position_utc"]).dt.date
    j = j[pd.to_datetime(j["uk"]).dt.year == 2025]
    days = j.drop_duplicates(["vessel_pln", "uk"]).groupby("vessel_pln").size()
    out = {}
    for pln, n in days.items():
        out[seg[pln]] = out.get(seg[pln], 0) + int(n)
    return out


def run(task):
    target = os.path.join(task, "target")
    fig = json.load(open(os.path.join(task, "generator", "figures.json")))
    D = load(target)
    sh = call(D)
    fails = 0
    des = [s for s in sh if sh[s] > fig["threshold"]]
    order = list(fig["segments"])
    ok = sorted(des) == sorted(fig["call"]["designated"])
    print("verify call:", "PASS" if ok else "FAIL", sorted(des))
    fails += not ok
    for s in order:
        f = fig["segments"][s]
        a = int(np.floor(sh[s] + 0.5))
        if a != f["share"]:
            print("verify share %s: FAIL %d against %d" % (s, a, f["share"]))
            fails += 1
    sh, tr = call(D, keep=True)
    by_mk, r2h, r2w, par = routes(tr)
    half = lambda x, nd=0: float(np.floor(x * 10 ** nd + 0.5) / 10 ** nd)
    checks_ = [("raised by marketable landings, every whole per cent the golden's",
                all(int(np.floor(by_mk[s] + 0.5)) == fig["segments"][s]["share"] for s in order)),
               ("the observers' discards by hours and by landed weight name NEP alone",
                sorted(s for s in r2h if r2h[s] > fig["threshold"]) == ["NEP"] ==
                sorted(s for s in r2w if r2w[s] > fig["threshold"]) == fig["default_path_by_landed_weight_designated"]),
               ("marketable catch landed an hour, observed and unobserved",
                all((half(par[s][0], 1), half(par[s][1], 1)) == (fig["segments"][s]["marketable_kg_per_hour_observed"],
                                                                  fig["segments"][s]["marketable_kg_per_hour_unobserved"])
                    for s in order)),
               ("vessels and hours with two terminals under the extract's names, most of them miles apart",
                two_terminals(D, fig["vms_two_terminals"]["apart_nm"]) ==
                (fig["vms_two_terminals"]["vessels"], fig["vms_two_terminals"]["vessel_hours"],
                 fig["vms_two_terminals"]["apart_hours"]) and
                fig["vms_two_terminals"]["apart_hours"] > fig["vms_two_terminals"]["vessel_hours"] / 2)]
    for name, ok in checks_:
        if not ok:
            print("verify %s: FAIL" % name)
            fails += 1
    A = ask_a(D)
    for s in order:
        if abs(A[s] - fig["segments"][s]["first_sale_gbp_thousands"]) > 1e-6:
            print("verify ask A %s: FAIL %.1f against %.1f" % (s, A[s], fig["segments"][s]["first_sale_gbp_thousands"]))
            fails += 1
    B = ask_b(D)
    for s in order:
        if B[s] != fig["segments"][s]["days_at_sea"]:
            print("verify ask B %s: FAIL %d against %d" % (s, B[s], fig["segments"][s]["days_at_sea"]))
            fails += 1
    print("verify: %s (%d figures)" % ("PASS" if not fails else "FAIL", 1 + 3 * len(order)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(run(TASK))
