"""The independent verifier: every graded figure recomputed from target/ alone (no generator module is imported), then
compared with generator/figures.json.

    python3 task485/generator/verify.py
"""
import json
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
Y0, Y1 = pd.Timestamp("2025-11-01"), pd.Timestamp("2026-11-01")     # the programme year, end exclusive
NDAY = (Y1 - Y0).days
LINE = 26.0
GAL = 0.00454609
CATS = ["Calves", "Cattle 12 to 24 months", "Cattle over 24 months", "Dairy cows", "Suckler cows"]
DAIRY = {"HO", "FR", "JE", "NR", "MO"}
OK, BAD = [], []


def check(label, cond, detail=""):
    (OK if cond else BAD).append(label)
    print("%s  %s%s" % ("PASS" if cond else "FAIL", label, ("  " + detail) if detail else ""))


def rates():
    txt = subprocess.run(["pdftotext", "-layout", os.path.join(T, "epo_cattle_ammonia_factors_2025.pdf"), "-"],
                         capture_output=True, text=True).stdout
    part = txt.split("4. The factors")[1].split("Table 3.")[0]
    out = {}
    for c in CATS:
        m = re.search(re.escape(c) + r"\s+([0-9.]+)\s+([0-9.]+)", part)
        out[c] = (float(m.group(1)), float(m.group(2)))
    return out


def seasons():
    hs = pd.read_excel(os.path.join(T, "moa_livestock_housing_survey_2025.xlsx"), sheet_name="Housing")
    days = pd.date_range(Y0, Y1 - pd.Timedelta(days=1))
    out = {}
    for _, r in hs.iterrows():
        h = pd.to_datetime(r["Usual housing date"] + " 2000", format="%d %B %Y")
        t = pd.to_datetime(r["Usual turnout date"] + " 2000", format="%d %B %Y")
        housed = np.array([(d.month, d.day) >= (h.month, h.day) or (d.month, d.day) < (t.month, t.day) for d in days])
        assert housed.sum() == r["Housed days in a 365-day year"], r["Region"]
        out[r["Region"]] = np.concatenate([[0], np.cumsum(housed)])
    return out


def herd_regions():
    hr = pd.read_excel(os.path.join(T, "nbr_herd_register_2026-11.xlsx"), sheet_name="Herds", dtype=str)
    hr["Valid to"] = pd.to_datetime(hr["Valid to"])
    cur = hr[hr["Valid to"].isna() | (hr["Valid to"] >= Y0)]
    assert cur["Herd No"].is_unique
    return dict(zip(cur["Herd No"], cur["Region"])), dict(zip(cur["Herd No"], cur["Herd type"]))


def ammonia(region_of):
    an = pd.read_csv(os.path.join(T, "nbr_animals_2025-26.csv"), dtype=str)
    mv = pd.read_csv(os.path.join(T, "nbr_movements_2025-26.csv"), dtype=str)
    dt = lambda s: pd.to_datetime(s, format="%d/%m/%Y")
    an["birth"] = (dt(an["DATE_OF_BIRTH"]) - Y0).dt.days
    an["exitd"] = (dt(an["EXIT_DATE"]) - Y0).dt.days
    an["fc"] = (dt(an["FIRST_CALVING_DATE"]) - Y0).dt.days
    an["s"] = an["birth"].clip(lower=0)
    an["e"] = an["exitd"].fillna(NDAY).clip(upper=NDAY)
    idx = {t: i for i, t in enumerate(an["TAG_NUMBER"])}
    mv["i"] = mv["TAG_NUMBER"].map(idx)
    mv["day"] = (dt(mv["ARRIVAL_DATE"]) - Y0).dt.days
    ev = pd.concat([pd.DataFrame(dict(i=np.arange(len(an)), day=an["s"].values, order=-1, herd=an["HERD_AT_START"].values)),
                    pd.DataFrame(dict(i=mv["i"].values, day=mv["day"].values, order=mv["MOVEMENT_ID"].astype(int).values,
                                      herd=mv["DESTINATION_HERD"].values))])
    s_of, e_of = an["s"].values, an["e"].values
    ev["day"] = np.maximum(ev["day"].values, s_of[ev["i"].values])
    ev = ev.sort_values(["i", "day", "order"]).reset_index(drop=True)
    nxt = np.append(ev["day"].values[1:], NDAY)
    same = np.append(ev["i"].values[1:] == ev["i"].values[:-1], False)
    end = np.where(same, nxt, e_of[ev["i"].values])
    end = np.minimum(end, e_of[ev["i"].values])
    seg = ev.assign(end=end)
    seg = seg[seg["end"] > seg["day"]]
    a = seg["i"].values
    s, e = seg["day"].values.astype(int), seg["end"].values.astype(int)
    birth = an["birth"].values
    fc = an["fc"].fillna(10 ** 6).values
    cuts = np.stack([birth[a] + 365, birth[a] + 730, fc[a]], 1)
    cuts = np.minimum(np.maximum(cuts, s[:, None]), e[:, None])
    cuts.sort(1)
    pts = np.concatenate([s[:, None], cuts, e[:, None]], 1)
    p0, p1 = pts[:, :-1].ravel(), pts[:, 1:].ravel()
    rows = np.repeat(np.arange(len(a)), 4)
    keep = p1 > p0
    p0, p1, rows = p0[keep].astype(int), p1[keep].astype(int), rows[keep]
    aa = a[rows]
    herd = seg["herd"].values[rows]
    region = np.array([region_of[h] for h in herd])
    age = p0 - birth[aa]
    cow = (an["SEX"].values[aa] == "F") & (fc[aa] <= p0)
    dairy = an["BREED"].isin(DAIRY).values[aa]
    cat = np.where(age < 365, 0, np.where(cow, np.where(dairy, 3, 4), np.where(age < 730, 1, 2)))
    R = rates()
    rh = np.array([R[c][0] for c in CATS])
    rg = np.array([R[c][1] for c in CATS])
    cum = seasons()
    kg = {}
    for r in sorted(set(region)):
        m = region == r
        hd = cum[r][p1[m]] - cum[r][p0[m]]
        kg[r] = float((hd * rh[cat[m]] + (p1[m] - p0[m] - hd) * rg[cat[m]]).sum())
    return kg, int((p1 - p0).sum())


def land(region_of):
    lp = pd.read_csv(os.path.join(T, "lpr_farmed_area_2026.csv"), dtype={"HERD_NO": str})
    lp["ha"] = lp["AREA_HA"] * lp["SHARE_PCT"] / 100
    lp["region"] = lp["HERD_NO"].map(region_of)
    assert lp["region"].notna().all()
    return lp.groupby("region")["ha"].sum().to_dict()


def contractors(region_of):
    lo, hi = pd.Timestamp("2026-01-13"), pd.Timestamp("2026-04-30")
    av = pd.read_csv(os.path.join(T, "vale_agri_jobs_2026.csv"), dtype=str)
    av["date"] = pd.to_datetime(av["Date"], format="%d/%m/%Y")
    av["m3"] = av["Loads"].astype(int) * av["Capacity (gal)"].astype(int) * GAL
    av["less"] = av["Spreader"].isin(["TRAILING SHOE", "DRIBBLE BAR"])
    av = av[(av["Material"] == "CATTLE SLURRY") & av["date"].between(lo, hi) & av["Herd No"].isin(region_of)]
    nm = pd.read_excel(os.path.join(T, "basin_agri_job_sheets_2026.xlsx"), sheet_name="Job sheets 2026", dtype={"Herd No": str})
    nm = nm[(nm["Product"] == "Cattle slurry") & pd.to_datetime(nm["Date"]).between(lo, hi) & nm["Herd No"].isin(region_of)]
    nm = nm.assign(m3=nm["Metered m3"].astype(float), less=nm["Applicator"].isin(["Trailing shoe", "Dribble bar"]))
    kb = pd.read_excel(os.path.join(T, "countrywide_invoice_lines_2026.xlsx"), sheet_name="Invoice lines",
                       dtype={"Reference": str, "Herd No": str})
    kb["herd"] = kb["Herd No"].str.replace(" ", "", regex=False)
    jobs = set(av["Job No"]) | set(pd.read_csv(os.path.join(T, "vale_agri_jobs_2026.csv"), dtype=str)["Job No"]) | \
        set(pd.read_excel(os.path.join(T, "basin_agri_job_sheets_2026.xlsx"), sheet_name="Job sheets 2026")["Job No"])
    kb = kb[kb["Service"].str.startswith("SS-") & pd.to_datetime(kb["Invoice date"]).between(lo, hi)
            & ~kb["Reference"].isin(jobs)]
    kb = kb.assign(m3=kb["Qty"].astype(float) * 1000 * GAL, less=kb["Service"].isin(["SS-TS", "SS-TH", "SS-UMB", "SS-INJ"]))
    allj = pd.concat([av.assign(region=av["Herd No"].map(region_of))[["region", "m3", "less"]],
                      nm.assign(region=nm["Herd No"].map(region_of))[["region", "m3", "less"]],
                      kb.assign(region=kb["herd"].map(region_of))[["region", "m3", "less"]]])
    allj["lm3"] = allj["m3"] * allj["less"]
    g = allj.groupby("region")[["m3", "lm3"]].sum()
    return {r: (float(g.loc[r, "m3"]), 100 * float(g.loc[r, "lm3"] / g.loc[r, "m3"])) for r in g.index}


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    region_of, types = herd_regions()
    kg, days = ammonia(region_of)
    la = land(region_of)
    order = f["constants"]["order"]
    des = [r for r in order if kg[r] / la[r] >= LINE]
    check("the call: the designated regions", des == f["call"]["designated"], str(des))
    for r in order:
        g = f["regions"][r]
        check("%s tonnes %s" % (r, g["tonnes"]), "{:,.1f}".format(kg[r] / 1000) == g["tonnes"], "{:,.1f}".format(kg[r] / 1000))
        check("%s kg a hectare %s" % (r, g["kg_ha"]), "%.2f" % (kg[r] / la[r]) == g["kg_ha"], "%.2f" % (kg[r] / la[r]))
        check("%s farmed land %s" % (r, g["land_ha"]), "{:,.2f}".format(la[r]) == g["land_ha"])
    c = f["components"]
    check("component: tonnes in all", "{:,.1f}".format(sum(kg.values()) / 1000) == c["tonnes_total"])
    check("component: farmed land in all", "{:,.2f}".format(sum(la.values())) == c["land_total"])
    check("step: animal-days", "{:,.0f}".format(days) == c["animal_days"], "{:,.0f}".format(days))
    A = contractors(region_of)
    for r in order:
        a = f["ask_a"][r]
        check("%s ask A %s m3" % (r, a["m3"]), "{:,.0f}".format(round(A[r][0], -2)) == a["m3"], "{:,.0f}".format(A[r][0]))
        check("%s ask A %s per cent" % (r, a["less_pct"]), "%.1f" % A[r][1] == a["less_pct"], "%.2f" % A[r][1])
    tv = sum(v for v, _ in A.values())
    tl = sum(v * s / 100 for v, s in A.values())
    check("step: contractors' slurry in all", "{:,.0f}".format(round(tv, -2)) == f["ask_a_total"]["m3"])
    check("step: low-emission share in all", "%.1f" % (100 * tl / tv) == f["ask_a_total"]["less_pct"])
    print("\n%d PASS, %d FAIL" % (len(OK), len(BAD)))
    if BAD:
        sys.exit(1)


if __name__ == "__main__":
    main()
