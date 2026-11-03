"""Independent verifier: reads only target/ (pandas, its own code path) and recomputes every graded figure."""
import json
import os
import sys

import numpy as np
import pandas as pd
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), "target")
fails = []


def check(label, cond):
    print(("PASS " if cond else "FAIL ") + label)
    if not cond:
        fails.append(label)


def local(ts):
    ts = pd.to_datetime(ts, utc=True)
    return ts.dt.tz_convert("Europe/London").dt.tz_localize(None)


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    proc = " ".join(p.extract_text() for p in PdfReader(os.path.join(T, "LP04_leakage_procedure_rev3.pdf")).pages)
    check("procedure readable (positive control on the night-hour sentence)", "up to but" in proc and "1.15" in proc)
    areas = pd.read_excel(os.path.join(T, "dma_register_2026-09.xlsx"), sheet_name="Areas", header=3)
    areas = areas[areas["Area code"].notna()]
    sp = pd.read_excel(os.path.join(T, "dma_register_2026-09.xlsx"), sheet_name="Supply points")
    units = pd.read_excel(os.path.join(T, "dma_register_2026-09.xlsx"), sheet_name="Instrument units")
    umap = dict(zip(units["Tag"], units["Engineering unit"]))
    f = pd.read_csv(os.path.join(T, "historian_inlet_flows_20260801_20261102.csv"))
    f["m3h"] = f["Value"] * np.where(f["TagName"].map(umap) == "l/s", 3.6, 1.0)
    f["lt"] = local(f["TimestampUTC"])
    tag2area = {}
    for _, a in areas.iterrows():
        for t in str(a["Inlet meter tag(s)"]).split(";"):
            tag2area[t.strip()] = a["Area code"]
    f["area"] = f["TagName"].map(tag2area)
    g = f.groupby(["area", "lt"])["m3h"].agg(["sum", "count"]).reset_index()
    ntag = f.groupby("area")["TagName"].nunique()
    g = g[g["count"] == g["area"].map(ntag)]
    g["d"] = g["lt"].dt.date
    base = (pd.Timestamp("2026-09-07").date(), pd.Timestamp("2026-10-04").date())
    comp = (pd.Timestamp("2026-10-12").date(), pd.Timestamp("2026-11-01").date())
    night = g[g["lt"].dt.hour == 3]

    def per(df, p):
        return df[(df["d"] >= p[0]) & (df["d"] <= p[1])]
    mnf_b = per(night, base).groupby(["area", "d"])["sum"].mean().groupby("area").mean()
    mnf_c = per(night, comp).groupby(["area", "d"])["sum"].mean().groupby("area").mean()
    # large users at the night hour, by supply point
    amr = pd.read_csv(os.path.join(T, "amr_large_user_reads_hourly.csv"))
    amr["t"] = pd.to_datetime(amr["read_time_utc"], utc=True)
    amr = amr.sort_values(["meter_serial", "t"])
    amr["adv"] = amr.groupby("meter_serial")["register_m3"].diff().shift(-1)
    amr["gap"] = amr.groupby("meter_serial")["t"].diff().shift(-1)
    amr.loc[amr["adv"] < 0, "adv"] += 100000.0
    amr = amr[amr["gap"] == pd.Timedelta(hours=1)]
    acc = pd.read_excel(os.path.join(T, "large_user_accounts.xlsx"))
    s2a = dict(zip(sp["Supply point"], sp["Area code"]))
    rev = dict(zip(sp["Supply point"], sp["Revenue meter"]))
    acct_of = dict(zip(acc["Meter serial"], acc["Account"]))
    prev0 = {r["Previous code"]: r["Area code"] for _, r in areas.iterrows() if isinstance(r["Previous code"], str) and r["Previous code"]}
    m2a = {}
    for _, r in acc.iterrows():
        s = r["Supply point"]
        if s in s2a:
            if r["Meter serial"] == rev[s] or acct_of.get(rev[s]) == r["Account"]:
                m2a[r["Meter serial"]] = s2a[s]
        else:
            m2a[r["Meter serial"]] = prev0.get(r["Area (account)"], r["Area (account)"])
    amr["area"] = amr["meter_serial"].map(m2a)
    amr["lt"] = amr["t"].dt.tz_convert("Europe/London").dt.tz_localize(None)
    amr["d"] = amr["lt"].dt.date
    an = amr[amr["lt"].dt.hour == 3]
    nb = (base[1] - base[0]).days + 1
    nc = (comp[1] - comp[0]).days + 1
    lub = per(an, base).groupby("area")["adv"].sum() / nb
    luc = per(an, comp).groupby("area")["adv"].sum() / nc
    pr = pd.read_csv(os.path.join(T, "aznp_pressure_hourly_2026.csv"))
    pr["m"] = np.where(pr["unit"] == "bar", pr["mean_pressure"] / 0.0980665, pr["mean_pressure"])
    pr["lt"] = local(pr["hour_start_utc"])
    pr["d"] = pr["lt"].dt.date
    pn = pr[pr["lt"].dt.hour == 3]
    pb = per(pn, base).groupby("logger_id")["m"].mean()
    pc = per(pn, comp).groupby("logger_id")["m"].mean()
    own = {}
    fac = {}
    for _, a in areas.iterrows():
        c = a["Area code"]
        nu = (a["Household properties"] * 1.7 + a["Non-household properties (not logged)"] * 6.0) / 1000
        lb = mnf_b[c] - nu - lub.get(c, 0.0)
        lc = mnf_c[c] - nu - luc.get(c, 0.0)
        fac[c] = (pb[a["AZNP logger"]] / pc[a["AZNP logger"]]) ** 1.15
        own[c] = lc * fac[c] - lb
    # the boundary test on whole-day volumes
    import json as js
    gj = js.load(open(os.path.join(T, "gis_boundary_valves.geojson")))
    daily = g.groupby(["area", "d"])["sum"].mean()
    for ft in gj["features"]:
        a, b = ft["properties"]["dma_1"], ft["properties"]["dma_2"]
        da = per(g[g["area"] == a], comp)["sum"].mean() - per(g[g["area"] == a], base)["sum"].mean()
        db = per(g[g["area"] == b], comp)["sum"].mean() - per(g[g["area"] == b], base)["sum"].mean()
        if abs(da) > 2.0 and 0.85 <= -db / da <= 1.15:
            rise, fall = (a, b) if da > 0 else (b, a)
            na = per(night[night["area"] == rise], comp)["sum"].mean() - per(night[night["area"] == rise], base)["sum"].mean()
            nf = per(night[night["area"] == fall], comp)["sum"].mean() - per(night[night["area"] == fall], base)["sum"].mean()
            Tn = (na - nf) / 2
            own[rise] -= Tn * fac[rise]
            own[fall] += Tn * fac[fall]
            check("valve pair found is " + ft["properties"]["asset_id"], ft["properties"]["asset_id"] == figs["open_valve"])
    names = dict(zip(areas["Area code"], areas["Area name"]))
    for c, v in own.items():
        p = round(v / 3.6, 1) + 0.0
        check("own change %s %.1f l/s" % (names[c], p), abs(p - figs["own_change"][names[c]]) < 1e-9)
    top = max(own, key=own.get)
    check("call recomputes: " + names[top], names[top] == figs["call"])
    # asks
    lo, hi = pd.Timestamp("2026-09-30 23:00", tz="UTC"), pd.Timestamp("2026-11-01 00:00", tz="UTC")
    oc = amr[(amr["t"] >= lo) & (amr["t"] + pd.Timedelta(hours=1) <= hi)].groupby("area")["adv"].sum()
    for c in names:
        check("LU October %s" % names[c], int(round(oc.get(c, 0.0))) == figs["lu_oct"][names[c]])
    ev = pd.read_csv(os.path.join(T, "billing_account_events_extract.csv"), dtype=str)
    ev["eff"] = pd.to_datetime(ev["effective_date"], format="%d/%m/%Y")
    ev = ev[ev["eff"] <= "2026-10-31"]
    prev = {r["Previous code"]: r["Area code"] for _, r in areas.iterrows() if isinstance(r["Previous code"], str) and r["Previous code"]}
    ev["area"] = ev["area_code"].replace(prev)
    ev = ev.sort_values(["property_ref", "eff", "posted"])
    occ = {}
    for pref, grp in ev.groupby("property_ref"):
        st, cls = {}, None
        for _, e in grp.iterrows():
            if e["event"] == "OCC":
                st[e["account_no"]] = True
                cls = cls or e["property_class"]
            elif e["event"] == "VAC":
                st[e["account_no"]] = False
            else:
                cls = e["property_class"]
        if any(st.values()) and cls == "HH":
            occ[grp["area"].iloc[-1]] = occ.get(grp["area"].iloc[-1], 0) + 1
    for c in names:
        check("occupied %s" % names[c], occ.get(c, 0) == figs["occupied"][names[c]])
    wo = pd.read_excel(os.path.join(T, "works_orders_aug_oct_2026.xlsx"))
    assets = pd.read_csv(os.path.join(T, "mains_asset_list.csv"))
    amap = dict(zip(assets["asset_id"], assets["dma"]))
    wo["Asset"] = wo["Asset"].astype(str)
    inhouse = wo[~wo["Asset"].str.startswith("W26-")].drop_duplicates("Job")
    norm = lambda s: s if s.startswith("WM-") else "WM-%06d" % int(s.split("/")[0])
    jmap = dict(zip(inhouse["Job"], inhouse["Asset"].map(norm)))
    rep = wo[(wo["Task type"] == "REPAIR MAIN") & (wo["Task completed"] >= "2026-08-01") & (wo["Task completed"] < "2026-11-01")].copy()
    rep["aid"] = [jmap[a] if a.startswith("W26-") else jmap[j] for a, j in zip(rep["Asset"], rep["Job"])]
    rep["area"] = rep["aid"].map(amap)
    cnt = rep.drop_duplicates("Job").groupby("area").size()
    for c in names:
        check("repairs %s" % names[c], int(cnt.get(c, 0)) == figs["repairs"][names[c]])
    print("%d failed" % len(fails))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
