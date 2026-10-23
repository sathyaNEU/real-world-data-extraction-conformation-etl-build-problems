"""The independent verifier: every graded figure recomputed from the cut pack by code that shares nothing with the
analysis (pandas readers, its own parsing of the report's table and of the agencies' clocks, its own joins), then
compared with generator/figures.json.

    python3 task273/generator/verify.py [task folder]"""
import json
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
USES = {"11": "Taxi", "12": "Ride-hail", "13": "Limousine", "14": "Airport shuttle", "15": "Paratransit",
        "21": "Parcel delivery", "22": "App delivery"}
GROUP = {(1, "U"): 1, (2, "U"): 1, (3, "U"): 2, (4, "U"): 2, (5, "U"): 3, (7, "U"): 3,
         (1, "R"): 4, (2, "R"): 4, (3, "R"): 5, (4, "R"): 5, (5, "R"): 6, (6, "R"): 6, (7, "R"): 6}
COST = {"K": 12850000, "A": 1183000, "B": 318000, "C": 161000, "O": 15300}


def find(target, stem):
    return os.path.join(target, [f for f in os.listdir(target) if f.startswith(stem)][0])


def local_clock(cr):
    """Pacific local date and hour of every crash, from each agency's own clock and format."""
    t = cr["CRASH_TIME"].fillna("").astype(str).str.strip()
    hour = pd.Series(np.nan, index=cr.index)
    date = pd.to_datetime(cr["CRASH_DATE"])
    utc = (cr["TIME_ZONE"] == "UTC") & (t != "")
    stamp = pd.to_datetime(cr.loc[utc, "CRASH_DATE"] + " " + t[utc]).dt.tz_localize("UTC").dt.tz_convert(
        "America/Los_Angeles")
    hour[utc] = stamp.dt.hour
    date[utc] = stamp.dt.tz_localize(None).dt.normalize()
    ampm = t.str.endswith(("AM", "PM")) & ~utc
    hour[ampm] = pd.to_datetime(t[ampm], format="%I:%M %p").dt.hour
    colon = t.str.contains(":") & ~utc & ~ampm
    hour[colon] = t[colon].str.split(":").str[0].astype(int)
    bare = (t != "") & ~utc & ~ampm & ~colon
    hour[bare] = t[bare].astype(int) // 100
    return date, hour


def load(target):
    cr = pd.read_csv(find(target, "crash_extract_2021_2025_crashes"), dtype=str, keep_default_na=False)
    un = pd.read_csv(find(target, "crash_extract_2021_2025_units"), dtype=str, keep_default_na=False)
    inv = pd.read_excel(find(target, "lrs_road_inventory"), sheet_name=None, dtype={"ROUTE_ID": str})
    seg, leg = inv["Segments"], inv["Legacy route numbers"]
    leg = dict(zip(leg["LEGACY_ROUTE_NO"].astype(str), leg["ROUTE_ID"]))
    ops = pd.read_excel(find(target, "commission_operator_register"), sheet_name="Operators")
    use_of = {"Taxi": "11", "Ride-hail": "12", "Limousine": "13", "Airport shuttle": "14", "Paratransit": "15",
              "Parcel delivery": "21", "App delivery": "22"}
    name_use = {}
    for _, r in ops.iterrows():
        for nm in str(r["NAMES_ON_CRASH_REPORTS"]).split(";"):
            name_use[nm.strip().lower()] = use_of[r["USE"]]
    cr["DATE_L"], cr["HOUR_L"] = local_clock(cr)
    cr["DTYPE"] = np.where(cr["DATE_L"].dt.weekday >= 5, "we", "wd")
    v2 = cr["FORM_VERSION"] == "PTCR-23"
    fs = pd.Series(pd.NA, index=cr.index, dtype="object")
    ur = pd.Series(pd.NA, index=cr.index, dtype="object")
    fs[v2 & (cr["F_SYSTEM"] != "")] = cr.loc[v2 & (cr["F_SYSTEM"] != ""), "F_SYSTEM"].astype(int)
    ur[v2 & (cr["URBAN_RURAL"] != "")] = cr.loc[v2 & (cr["URBAN_RURAL"] != ""), "URBAN_RURAL"]
    bysr = {k: v.sort_values("BEGIN_MP") for k, v in seg.groupby("ROUTE_ID")}
    for i in cr.index[~v2 & (cr["LOC_ROUTE"] != "")]:
        s = bysr[leg[cr.at[i, "LOC_ROUTE"]]]
        mp = float(cr.at[i, "MILEPOST"])
        hit = s[(s["BEGIN_MP"] <= mp) & (mp < s["END_MP"])]
        fs[i], ur[i] = int(hit["F_SYSTEM"].iloc[0]), hit["URBAN_RURAL"].iloc[0]
    cr["GROUP"] = [GROUP.get((f, u)) if not (pd.isna(f) or pd.isna(u)) else None for f, u in zip(fs, ur)]
    cr = cr.set_index("CRASH_ID")
    # units: the rule's use, and fault as each form records it
    un = un.join(cr[["FORM_VERSION", "AT_FAULT_UNIT"]], on="CRASH_ID")
    form2 = un["FORM_VERSION"] == "PTCR-23"
    mv = un["UNIT_TYPE"].isin(["1", "MV IN TRANSPORT"])
    use = pd.Series("OTHER", index=un.index)
    v2u = un["VEH_USE"].where(form2)
    use[form2 & v2u.isin(list(USES))] = v2u[form2 & v2u.isin(list(USES))]
    use[form2 & (un["VEH_USE"] == "00") & un["BODY_TYPE"].isin(["PASSENGER CAR", "SPORT UTILITY", "PICKUP", "VAN"])] = "PV"
    v1c = ~form2 & un["VEH_USE"].isin(["1", "2"])
    use[v1c] = un.loc[v1c, "CARRIER_NAME"].str.strip().str.lower().map(name_use).fillna("OTHER")
    use[~form2 & (un["VEH_USE"] == "0") & un["BODY_TYPE"].isin(["01", "02", "03", "04"])] = "PV"
    use[un["HIT_RUN_UNIT"] == "Y"] = "UNK"
    un["USE"] = use
    un["FAULT"] = np.where(form2, un["AT_FAULT_UNIT"] == un["UNIT_NO"], ~un["CONTRIB_CODE"].isin(["", "00"]))
    un["MV"] = mv
    return cr, un


def vmt_table(target):
    txt = subprocess.run(["pdftotext", "-layout", find(target, "travel_monitoring_report"), "-"], capture_output=True,
                         text=True).stdout
    block = txt[txt.index("Table 1."):txt.index("Table 2.")]
    names = ["Interstate", "Other freeways and expressways", "Other principal arterials", "Minor arterials",
             "Major collectors", "Minor collectors", "Local"]
    out = {}
    for line in block.splitlines():
        for i, nm in enumerate(names, 1):
            if line.strip().startswith(nm + " ") and ("Urban" in line or "Rural" in line):
                nums = [float(x.replace(",", "")) for x in re.findall(r"[\d,]+\.\d", line)]
                out[(i, "U" if "Urban" in line else "R")] = sum(nums)
    return out


def hourly_share(target):
    st = pd.read_csv(find(target, "ccs_stations"), dtype={"STATION_ID": str})
    hv = pd.read_csv(find(target, "ccs_hourly_volumes"), dtype={"STATION_ID": str})
    hv = hv.merge(st[["STATION_ID", "FACTOR_GROUP"]], on="STATION_ID")
    hv["DTYPE"] = np.where(pd.to_datetime(hv["COUNT_DATE"]).dt.weekday >= 5, "we", "wd")
    long = hv.melt(id_vars=["FACTOR_GROUP", "DTYPE"], value_vars=["HR%02d" % h for h in range(1, 25)],
                   var_name="HR", value_name="V").dropna()
    long["HOUR"] = long["HR"].str[2:].astype(int) - 1
    s = long.groupby(["FACTOR_GROUP", "DTYPE", "HOUR"])["V"].sum()
    return s / s.groupby(level=0).transform("sum")


def call(target):
    cr, un = load(target)
    mvu = un[un["MV"]]
    nmv = mvu.groupby("CRASH_ID").size()
    mvc = set(nmv[nmv >= 2].index)
    m = mvu[mvu["CRASH_ID"].isin(mvc)]
    af = m[m["FAULT"]].drop_duplicates(["CRASH_ID", "USE"]).groupby("USE").size()
    nf = m.groupby("CRASH_ID")["FAULT"].sum()
    one = set(nf[nf == 1].index)
    ex = m[m["CRASH_ID"].isin(one) & ~m["FAULT"]].join(cr[["GROUP", "DTYPE", "HOUR_L"]], on="CRASH_ID")
    ex = ex[ex["GROUP"].notna() & ex["HOUR_L"].notna()]
    ex["K"] = list(zip(ex["GROUP"].astype(int), ex["DTYPE"], ex["HOUR_L"].astype(int)))
    tot = ex.groupby("K").size()
    vm = vmt_table(target)
    gv = {}
    for (f, u), v in vm.items():
        gv[GROUP[(f, u)]] = gv.get(GROUP[(f, u)], 0.0) + v
    sh = hourly_share(target)
    E = {k: gv[k[0]] * sh[k] for k in tot.index}
    by = ex.groupby(["USE", "K"]).size()
    miles = {}
    for (u, k), n in by.items():
        miles[u] = miles.get(u, 0.0) + E[k] * n / tot[k]
    rate = {u: af.get(u, 0) / miles[u] for u in miles}
    return {USES[c]: rate[c] / rate["PV"] for c in USES}, {USES[c]: int(af.get(c, 0)) for c in USES}, int(af["PV"])


def asks(target):
    cr, un = load(target)
    ps = pd.read_csv(find(target, "crash_extract_2021_2025_persons"), dtype=str, keep_default_na=False)
    ps["PERSON_NO"] = ps["PERSON_NO"].astype(int)
    sev = {"1": "K", "2": "A", "3": "B", "4": "C", "5": "O"}
    ps["SEV"] = ps["INJURY_SEVERITY"].map(lambda s: sev.get(s, s))
    pt = {"1": "DRIVER", "2": "PASSENGER", "3": "PEDESTRIAN", "4": "BICYCLIST"}
    ps["PT"] = ps["PERSON_TYPE"].map(lambda s: pt.get(s, s))
    ps["KEY"] = np.where(ps["SEAT_POSITION"] != "", ps["SEAT_POSITION"], ps["PT"])
    ps = ps.sort_values("PERSON_NO").drop_duplicates(["CRASH_ID", "UNIT_NO", "KEY"], keep="last")
    reg = pd.read_csv(find(target, "road_fatality_register"), dtype=str)
    agency = {"State Patrol, District 6": "SP6", "Stonereach County Sheriff's Office": "SCSO",
              "Kelderwick Police Department": "KPD", "Fairhollow Police Department": "FPD"}
    reg["AGENCY"] = reg["AGENCY"].map(agency)
    ids = cr.reset_index()[["CRASH_ID", "AGENCY", "AGENCY_REPORT_NO"]]
    reg = reg.merge(ids, on=["AGENCY", "AGENCY_REPORT_NO"])
    dead = set(zip(reg["CRASH_ID"], reg["VEHICLE_NO"], reg["PERSON_TYPE"], reg["AGE"], reg["SEX"]))
    ps["FINAL"] = [("K" if (c, u, p, a, s) in dead else v) for c, u, p, a, s, v in
                   zip(ps["CRASH_ID"], ps["UNIT_NO"], ps["PT"], ps["AGE"], ps["SEX"], ps["SEV"])]
    veh = un[un["UNIT_TYPE"].isin(["1", "MV IN TRANSPORT", "2", "PARKED MV"]) & un["FAULT"] & un["USE"].isin(list(USES))]
    caused = veh.groupby("CRASH_ID")["USE"].apply(lambda s: sorted(set(s)))
    ksi_c = ps[ps["FINAL"].isin(["K", "A"])].groupby("CRASH_ID").size()
    order = "KABCO"
    worst = ps.groupby("CRASH_ID")["FINAL"].agg(lambda s: min(s, key=order.index))
    ksi = {v: 0 for v in USES.values()}
    cost = {v: 0 for v in USES.values()}
    for cid, uses in caused.items():
        for u in uses:
            ksi[USES[u]] += int(ksi_c.get(cid, 0))
            cost[USES[u]] += COST[worst.get(cid, "O")]
    return ksi, {k: float(np.floor(v / 1e6 * 10 + 0.5 + 1e-9) / 10) for k, v in cost.items()}


def run(task):
    target = os.path.join(task, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    ratio, af, pv = call(target)
    covered = [u for u in ["Taxi", "Ride-hail", "Limousine", "Airport shuttle", "Paratransit", "Parcel delivery",
                           "App delivery"] if ratio[u] >= 1.5]
    bad = []
    if covered != fig["call"]["covered"]:
        bad.append(("covered", covered, fig["call"]["covered"]))
    for u, r in ratio.items():
        if float(np.floor(r * 10 + 0.5 + 1e-9) / 10) != fig["uses"][u]["ratio"]:
            bad.append(("ratio", u, r, fig["uses"][u]["ratio"]))
        if af[u] != fig["uses"][u]["crashes_caused"]:
            bad.append(("crashes", u, af[u], fig["uses"][u]["crashes_caused"]))
    if pv != fig["private"]["crashes_caused"]:
        bad.append(("private", pv, fig["private"]["crashes_caused"]))
    ksi, cost = asks(target)
    for u in ksi:
        if ksi[u] != fig["asks"]["ksi"][u]:
            bad.append(("ksi", u, ksi[u], fig["asks"]["ksi"][u]))
        if abs(cost[u] - fig["asks"]["cost_millions"][u]) > 1e-9:
            bad.append(("cost", u, cost[u], fig["asks"]["cost_millions"][u]))
    print("verify: covered %s; ratios %s" % (covered, {u: round(r, 3) for u, r in ratio.items()}))
    print("verify: %s" % ("PASS" if not bad else "FAIL %s" % bad))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)))
