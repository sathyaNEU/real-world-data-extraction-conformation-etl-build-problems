"""The independent verifier: reads only the shipped pack and the golden workbook, recomputes every graded figure with
its own code (pandas, no generator module), and compares.

    python3 task486/generator/verify.py <target dir> <golden dir>
"""
import os
import sys

import numpy as np
import openpyxl
import pandas as pd

AS_OF = "2026-09-30"


def r10(x):
    return int(np.floor(x / 10.0 + 0.5) * 10)


def census(target):
    p = lambda n: os.path.join(target, n)
    bg = pd.read_csv(p("dhc2020_kelvane_block_groups_p12.csv"), skiprows=[1], dtype={"GEO_ID": str})
    bg["bg"] = bg["GEO_ID"].str[-12:]
    lab = pd.read_csv(p("dhc2020_p12_h1_column_metadata.csv"))
    lab = lab[lab["Column Name"].str.startswith("P12_")]

    def cols(lo):
        keep = []
        for code, text in zip(lab["Column Name"], lab["Label"]):
            last = text.split("!!")[-1]
            first = last.split()[0]
            if first.isdigit() and int(first) >= lo and text.count("!!") == 3:
                keep.append(code)
        return keep
    c60, c75 = cols(60), cols(75)
    bg["n60"], bg["n75"] = bg[c60].sum(axis=1), bg[c75].sum(axis=1)
    hu = pd.read_csv(p("dhc2020_kelvane_blocks_h1.csv"), skiprows=[1], dtype={"GEO_ID": str})
    hu["block"] = hu["GEO_ID"].str.replace("1000000US", "", regex=False)
    asg = pd.read_csv(p("provider_area_blocks.csv"), dtype={"TRACT_BLOCK": str, "EFFECTIVE_TO": str})
    asg = asg[asg["EFFECTIVE_TO"].isna()].copy()
    asg["block"] = asg["TRACT_BLOCK"].str.zfill(10).radd(hu["block"].iloc[0][:5])
    m = hu.merge(asg[["block", "PROV_AREA"]], on="block", how="left", validate="one_to_one")
    assert m["PROV_AREA"].notna().all()
    m["bg"] = m["block"].str[:12]
    by = m.groupby(["bg", "PROV_AREA"])["H1_001N"].sum().reset_index()
    by["share"] = by["H1_001N"] / by.groupby("bg")["H1_001N"].transform("sum")
    nareas = by.groupby("bg")["PROV_AREA"].transform("count")
    by.loc[nareas == 1, "share"] = 1.0
    by = by.merge(bg[["bg", "n60", "n75"]], on="bg", validate="many_to_one")
    out = {}
    for w in ("60", "75"):
        s = (by["n" + w] * by["share"]).groupby(by["PROV_AREA"]).sum()
        out[w] = {a: r10(v) for a, v in s.items()}
    county = pd.read_csv(p("dhc2020_kelvane_county_tracts_p12.csv"), skiprows=[1], dtype={"GEO_ID": str}).iloc[0]
    return out, {"60": int(county[c60].sum()), "75": int(county[c75].sum())}, int((nareas > 1).groupby(by["bg"]).any().sum())


def services(target):
    p = lambda n: os.path.join(target, n)
    asg = pd.read_csv(p("provider_area_blocks.csv"), dtype={"TRACT_BLOCK": str, "EFFECTIVE_TO": str})
    asg = asg[asg["EFFECTIVE_TO"].isna()]
    area_of = dict(zip(asg["TRACT_BLOCK"].str.zfill(10), asg["PROV_AREA"]))
    ros = pd.read_csv(p("hdm_client_roster_2026-10-09.csv"), dtype=str)
    ros["area"] = ros["home_block"].str[5:].map(area_of)
    assert ros["area"].notna().all()
    log = pd.read_csv(p("hdm_route_delivery_log_fy2026.csv"), dtype=str)
    items = pd.read_csv(p("hdm_item_codes.csv"))
    meals_of = dict(zip(items["item_code"], items["meals"]))
    g = log.groupby(["client_id", "delivery_date", "item_code"]).size().rename("rows").reset_index()
    g = g.merge(ros[["client_id", "meals_per_day", "area"]], on="client_id", validate="many_to_one")
    cap = np.where(g["item_code"] == "HOT", g["meals_per_day"].astype(int), 1)
    g["meals"] = np.minimum(g["rows"], cap) * g["item_code"].map(meals_of)
    meals = g.groupby("area")["meals"].sum().to_dict()
    ep = pd.read_csv(p("hdm_service_episodes_2026-10-09.csv"), dtype=str, keep_default_na=False)
    open_ = ep[(ep["enrolled"] <= AS_OF) & ((ep["closed"] == "") | (ep["closed"] > AS_OF))]["client_id"].unique()
    deaths = pd.read_csv(p("state_death_match_runs_2025-07_to_2026-10.csv"), dtype=str)
    deaths = deaths[deaths["date_of_death"] <= AS_OF]
    links = pd.read_csv(p("state_registry_number_links.csv"), dtype=str)
    fwd = dict(zip(links["prior_participant_id"], links["current_participant_id"]))
    dead = {fwd.get(s, s) for s in deaths["state_participant_id"]}
    act = ros[ros["client_id"].isin(open_) & ~ros["state_participant_id"].isin(dead)]
    active = act.groupby("area").size().to_dict()
    return {a: int(v) for a, v in meals.items()}, {a: int(v) for a, v in active.items()}


def golden_table(gdir):
    ws = openpyxl.load_workbook(os.path.join(gdir, "kelvane_provider_area_counts.xlsx")).worksheets[0]
    return {r[0]: tuple(r[2:6]) for r in ws.iter_rows(min_row=6, max_row=11, values_only=True)}


def main(target, gdir):
    counts, county, ncut = census(target)
    meals, active = services(target)
    gold = golden_table(gdir)
    good = True
    for a, (g60, g75, gm, ga) in gold.items():
        mine = (counts["60"][a], counts["75"][a], meals[a], active[a])
        same = mine == (g60, g75, gm, ga)
        good &= same
        if not same:
            print("verify: %s differs: verifier %s, golden %s" % (a, mine, (g60, g75, gm, ga)))
    tie = all(sum(counts[w].values()) == r10(county[w]) for w in ("60", "75"))
    good &= tie and ncut == 12
    print("verify: %s (24 figures recomputed from the shipped files; %d cut block groups; the six areas add to the "
          "county's %d and %d to the nearest ten: %s)" % ("PASS" if good else "FAIL", ncut, county["60"], county["75"],
                                                          tie))
    return good


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1], sys.argv[2]) else 1)
