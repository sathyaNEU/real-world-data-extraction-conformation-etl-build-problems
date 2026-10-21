"""An independent recomputation of every graded figure from target/ with pandas, written apart from bundle.py: the two
price register extracts conformed, joined to the valuation register and the address points, each area's hedonic
change, the designation and the ask; compared with generator/figures.json and the golden workbook.

    python3 task482/generator/verify.py [target] [golden]"""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def main(target=None, gdir=None):
    target = target or os.path.join(TASK, "target")
    gdir = gdir or os.path.join(TASK, "golden")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    old = pd.read_csv(os.path.join(target, "ppr_residential_sales_filed_2024-10-01_to_2025-10-10.csv"),
                      encoding="cp1252", dtype=str, keep_default_na=False)
    new = pd.read_csv(os.path.join(target, "ppr_residential_sales_filed_2025-10-01_to_2026-10-14.csv"), dtype=str)
    val = pd.read_csv(os.path.join(target, "valuation_register_dwellings_extract_2026-10-15.csv"), dtype=str)
    pts = pd.read_csv(os.path.join(target, "address_points_buildings_extract_2026-10-15.csv"), dtype=str)
    e = old["Eircode"].str.upper().str.replace(" ", "", regex=False)
    old["eir"] = np.where(e.str.len() > 0, e.str[:3] + " " + e.str[3:], "")
    val["addr"] = val["address"].str.lower().str.replace(",", " ", regex=False).str.split().str.join(" ")
    old["addr"] = old["Address"].str.lower().str.replace(",", " ", regex=False).str.split().str.join(" ")
    m1 = old[old["eir"] != ""].merge(val[["property_number", "eircode"]], left_on="eir", right_on="eircode")
    m2 = old[old["eir"] == ""].merge(val[["property_number", "addr"]], on="addr")
    o = pd.concat([m1, m2])
    o = pd.DataFrame({
        "pn": o["property_number"], "date": pd.to_datetime(o["Date of Sale (dd/mm/yyyy)"], format="%d/%m/%Y"),
        "price": o["Price (€)"].str.replace("[€,]", "", regex=True).astype(float)
        * np.where(o["VAT Exclusive"] == "Yes", 1.135, 1.0),
        "fmp": o["Not Full Market Price"] == "No", "new": o["Description of Property"].str.startswith("New")})
    o["price"] = o["price"].round(0)
    n = pd.DataFrame({"pn": new["property_number"], "date": pd.to_datetime(new["sale_date"]),
                      "price": new["consideration_eur"].astype(float), "fmp": new["market_basis"] == "FMP",
                      "new": new["dwelling_status"] == "NEW"})
    s = pd.concat([o, n]).drop_duplicates(["pn", "date"], keep="last")
    s = s.merge(val[["property_number", "eircode", "la_code", "dwelling_type", "floor_area_m2"]], left_on="pn",
                right_on="property_number").merge(pts[["eircode", "ed_code", "building_id"]], on="eircode")
    s["floor"] = s["floor_area_m2"].astype(float)
    y1, y2, y3 = pd.Timestamp("2024-10-01"), pd.Timestamp("2025-10-01"), pd.Timestamp("2026-09-30")
    mk = s[s["fmp"] & (s["date"] >= y1) & (s["date"] <= y3)].copy()
    mk["y"] = (mk["date"] >= y2).astype(float)
    import openpyxl
    ws = openpyxl.load_workbook(os.path.join(target, "census_2022_dwelling_stock_by_area_and_type.xlsx"),
                                data_only=True).active
    hdr = [c.value for c in ws[4]]
    census = {r[0]: dict(zip(hdr[2:6], r[2:6])) for r in ws.iter_rows(min_row=5, values_only=True) if r[0]}
    out, bad = {}, []
    for code, g in mk.groupby("la_code"):
        yt = pd.get_dummies(g["dwelling_type"], dtype=float).mul(g["y"], axis=0).add_prefix("y_")
        X = pd.concat([pd.Series(1.0, index=g.index, name="c"), yt, np.log(g["floor"] / 100.0).rename("lf"),
                       g["new"].astype(float).rename("nw"),
                       pd.get_dummies(g["dwelling_type"], drop_first=True, dtype=float),
                       pd.get_dummies(g["ed_code"], drop_first=True, dtype=float)], axis=1)
        beta = pd.Series(np.linalg.solve(X.T.values @ X.values, X.T.values @ np.log(g["price"].values)), index=X.columns)
        base = g[g["y"] == 0].groupby("dwelling_type")["price"].mean()
        w = {t: census[code][t] * base[t] for t in base.index}
        out[code] = 100 * (sum(w[t] * np.exp(beta["y_" + t]) for t in w) / sum(w.values()) - 1)
        if round(out[code], 1) != fig["change"][code]:
            bad.append("change %s %.2f against %.1f" % (code, out[code], fig["change"][code]))
    des = sorted(k for k, v in out.items() if round(v, 1) > 8)
    if des != fig["call"]["designated"]:
        bad.append("designation %s" % des)
    y = s[(s["date"] >= y2) & (s["date"] <= y3)]
    grp = y.groupby(["building_id", "date", "price", "fmp"]).agg(n=("pn", "size"), la=("la_code", "first")).reset_index()
    blk = (grp["n"] > 1) & (~grp["fmp"])
    grp["purchases"] = np.where(blk, 1, grp["n"])
    grp["paid"] = np.where(blk, grp["price"], grp["price"] * grp["n"])
    a = grp.groupby("la")[["purchases", "paid"]].sum()
    for code in a.index:
        if int(a.loc[code, "purchases"]) != fig["ask"][code]["purchases"] or \
                int(round(a.loc[code, "paid"])) != fig["ask"][code]["paid"]:
            bad.append("ask %s" % code)
    print("verify: %d areas, %d market sales, designation %s, %d mismatches" % (len(out), len(mk), ",".join(des),
                                                                                len(bad)))
    for x in bad:
        print("  MISMATCH", x)
    return not bad


if __name__ == "__main__":
    ok = main(*(sys.argv[1:3]))
    raise SystemExit(0 if ok else 1)
