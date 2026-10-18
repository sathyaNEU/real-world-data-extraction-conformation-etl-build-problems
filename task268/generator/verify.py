"""Independent verifier for task268: reads only the shipped pack (no generator state) on its own code path (pandas),
recomputes the pick, every core's graded figures and both asks, and compares them with generator/figures.json.

    python3 task268/generator/verify.py task268/target"""
import json
import os
import sys

import numpy as np
import pandas as pd

SQFT = 10.7639104
GROUP = {"11": "SI01", "21": "SI01", "23": "SI01", "31-33": "SI01", "22": "SI02", "42": "SI02", "44-45": "SI02",
         "48-49": "SI02"}


def main(pack):
    f = lambda n: os.path.join(pack, n)
    od = pd.concat([pd.read_csv(f("commuting_od_tract_2022_main.csv"), dtype={"w_tract": str, "h_tract": str}),
                    pd.read_csv(f("commuting_od_tract_2022_aux.csv"), dtype={"w_tract": str, "h_tract": str})])
    sv = pd.read_csv(f("wls_puf_2025-10_2026-09.csv"), dtype={"NAICS_SECTOR": str, "HOMEREL": str})
    pop = pd.read_csv(f("acs5_2022_b01003_tracts.csv"), skiprows=[1])
    pop["tract"] = pop["GEO_ID"].str[-11:]
    pop = pop.set_index("tract")["B01003_001E"].astype(float)
    gz = pd.read_csv(f("gazetteer_tracts_2022.txt"), sep="\t", dtype={"GEOID": str})
    gz.columns = [c.strip() for c in gz.columns]
    land = gz.set_index("GEOID")["ALAND"] / 1e6
    dl = pd.read_excel(f("cbsa_delineation_2023_six_states.xlsx"), sheet_name="List 1", header=2, dtype=str)
    dl = dl[dl["CBSA Code"].fillna("").str.fullmatch(r"\d{5}")]
    dl["county"] = dl["FIPS State Code"].str.zfill(2) + dl["FIPS County Code"].str.zfill(3)
    cbsa_of = dict(zip(dl["county"], dl["CBSA Code"]))
    typ = {(c, k): t for c, k, t in zip(dl["CBSA Code"], dl["county"], dl["Central/Outlying County"])}
    cores = pd.read_excel(f("candidate_cores_2027.xlsx"), sheet_name="Core tracts", dtype={"Tract": str})

    # shares of weekdays on the premises by industry group and residence relation, weighted
    s = sv[sv["HOMEREL"].isin(["1", "2", "3"])].copy()
    s["g"] = s["NAICS_SECTOR"].map(lambda x: GROUP.get(x, "SI03"))
    s["r"] = s["HOMEREL"].map({"1": "C", "2": "O", "3": "X"})
    s["num"] = s["FINALWT"] * s["DAYS_PREM"]
    s["den"] = s["FINALWT"] * 5
    agg = s.groupby(["g", "r"])[["num", "den"]].sum()
    share = (agg["num"] / agg["den"]).to_dict()

    def ring(h, w):
        cb = cbsa_of.get(w[:5])
        t = typ.get((cb, h[:5])) if cb else None
        return "X" if t is None else ("C" if t == "Central" else "O")

    od = od[od["w_tract"] != od["h_tract"]].copy()
    od["ring"] = [ring(h, w) for h, w in zip(od["h_tract"], od["w_tract"])]
    od["att"] = sum(od["SI0%d" % k] * od["ring"].map(lambda r, k=k: share[("SI0%d" % k, r)]) for k in (1, 2, 3))
    out_away = od.groupby("h_tract")["att"].sum()
    in_work = od.groupby("w_tract")["att"].sum()
    res = {}
    for m, sub in cores.groupby("Metro"):
        tr = [t for t in sub["Tract"] if land.get(t, 0) > 0]
        P = np.array([pop.get(t, 0.0) - out_away.get(t, 0.0) + in_work.get(t, 0.0) for t in tr])
        a = np.array([land[t] for t in tr])
        d = P / a
        res[m] = dict(present=P.sum(), pwd=(P * d).sum() / P.sum(), dense=P[d >= 20000].sum() / P.sum())
    order = sorted(res, key=lambda m: -res[m]["pwd"])

    # ask A: units on the market on 30 September 2026, a floor listed whole beside its own suites counted once
    L = pd.read_csv(f("retail_space_listings_20261001.csv"), dtype={"census_tract": str, "suite": str, "status_date": str})
    L["suite"] = L["suite"].fillna("")
    L["status_date"] = L["status_date"].fillna("")
    L["m2"] = L["space_sf"] / SQFT
    ok = ((L["date_listed"] <= "2026-09-30") & (L["floor"].astype(str) == "1") & L["property_type"].isin(["Retail", "Flex"])
          & L["m2"].between(150, 450) & ((L["status"] == "Available") | (L["status_date"] > "2026-09-30")))
    L = L[ok].copy()
    yr = np.where(L["rent_basis"] == "/SF/YR", L["asking_rent"] * SQFT,
                  np.where(L["rent_basis"] == "/SF/MO", L["asking_rent"] * 12 * SQFT, L["asking_rent"] * 12 / L["m2"]))
    L["rate"] = yr
    suites = L[L["suite"] != ""].groupby(["city", "address"])["space_sf"].agg(["sum", "count"])
    whole = [(s_ == "" and (c, a) in suites.index and suites.loc[(c, a), "count"] >= 2 and suites.loc[(c, a), "sum"] == sf)
             for s_, c, a, sf in zip(L["suite"], L["city"], L["address"], L["space_sf"])]
    L = L[~np.array(whole, dtype=bool)]
    ask_a = {}
    for m, sub in cores.groupby("Metro"):
        x = L[L["census_tract"].isin(set(sub["Tract"]))]
        ask_a[m] = (len(x), float(np.median(x["rate"])))

    # ask B: dark stores delivering in the 30 September scrape, less shops both finders list at one address and unit
    S = pd.read_csv(f("competitor_locator_scrapes_2026.csv"), dtype={"census_tract": str, "unit": str})
    S["unit"] = S["unit"].fillna("")
    S = S[(S["scrape_date"] == "2026-09-30") & S["services"].str.contains("Delivery")]
    keys = S.groupby(["address", "unit"])["brand"].nunique()
    shared = set(keys[keys > 1].index)
    S = S[[(a, u) not in shared for a, u in zip(S["address"], S["unit"])]]
    ask_b = {}
    for m, sub in cores.groupby("Metro"):
        x = S[S["census_tract"].isin(set(sub["Tract"]))]
        for b in ("Tilldash", "Hopcrate"):
            ask_b[(m, b)] = int((x["brand"] == b).sum())

    fig = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
    bad = []
    r = lambda v, u: int(v / u + 0.5) * u
    if fig["call"]["metro"] != order[0] or fig["call"]["runner_up"] != order[1]:
        bad.append("call %s/%s against %s/%s" % (fig["call"]["metro"], fig["call"]["runner_up"], order[0], order[1]))
    if fig["call"]["gap"] != r(res[order[0]]["pwd"] - res[order[1]]["pwd"], 100):
        bad.append("gap")
    for m, v in res.items():
        c = fig["cores"][m]
        if c["present"] != r(v["present"], 1000) or c["density"] != r(v["pwd"], 100) or c["dense_share"] != int(100 * v["dense"] + .5):
            bad.append("core %s" % m)
        a = fig["ask_a"][m]
        if a["units"] != ask_a[m][0] or a["median_rent"] != int(ask_a[m][1] + .5):
            bad.append("ask A %s" % m)
        for b in ("Tilldash", "Hopcrate"):
            if fig["ask_b"][m][b] != ask_b[(m, b)]:
                bad.append("ask B %s %s" % (m, b))
    print("verify: pick %s, runner-up %s, %d mismatches" % (order[0], order[1], len(bad)))
    for b in bad:
        print("  ", b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
