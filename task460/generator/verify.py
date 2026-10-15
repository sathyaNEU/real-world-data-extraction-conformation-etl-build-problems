"""Independent verifier for task460: reads only the shipped bundle (target/) with pandas, on its own code path, and
recomputes the call, the first store left out and the gap, every store's avoided carbon dioxide per MWh, the three
rungs' winners, and the three invoice asks; then compares them with generator/figures.json and the golden files.

    python3 task460/generator/verify.py [target] [golden]
"""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
LB_PER_TONNE = 2204.62262
SEASON = {12: "DJF", 1: "DJF", 2: "DJF", 3: "MAM", 4: "MAM", 5: "MAM", 6: "JJA", 7: "JJA", 8: "JJA", 9: "SON", 10: "SON",
          11: "SON"}


def find(target, stem):
    hits = [f for f in os.listdir(target) if f.startswith(stem)]
    assert len(hits) == 1, (stem, hits)
    return os.path.join(target, hits[0])


def load(target):
    sites = pd.read_csv(find(target, "corvane_pilot_store_sites"))
    umap = pd.read_csv(find(target, "utility_balancing_area_map"))
    codes = pd.read_csv(find(target, "balancing_area_codes"))
    sites = sites.merge(umap[["utility_name", "balancing_area"]], left_on="delivery_utility", right_on="utility_name")
    codes["offset"] = codes["utc_offset"].str[:3].astype(int)
    rename = {r.former_code: r.ba_code for r in codes.itertuples() if isinstance(r.former_code, str) and r.former_code}
    hourly = pd.read_csv(find(target, "balancing_area_hourly_operating_data"))
    hourly["area"] = hourly["balancing_area"].replace(rename)
    hourly["start_utc"] = pd.to_datetime(hourly["utc_time_at_end_of_hour"], utc=True) - pd.Timedelta(hours=1)
    rates = pd.read_excel(find(target, "edc_generation_emission_rates_2025"), sheet_name=0, header=2)
    rates = rates[rates["BA code"].notna()].set_index("BA code")
    arrays = pd.read_csv(find(target, "pilot_array_output_model"))
    return sites, codes, hourly, rates, arrays


def marginal(hourly, rates, codes, area, regressor="net_generation_mw"):
    h = hourly[hourly["area"] == area].sort_values("start_utc").reset_index(drop=True).fillna(0)
    r = rates.loc[area]
    t = lambda col: (r[col] / LB_PER_TONNE) if pd.notna(r[col]) else 0.0
    co2 = (h["ng_coal_mw"] * t("CO2 coal output emission rate (lb/MWh)") +
           h["ng_natural_gas_mw"] * t("CO2 gas output emission rate (lb/MWh)") +
           h["ng_petroleum_mw"] * t("CO2 oil output emission rate (lb/MWh)"))
    off = int(codes.set_index("ba_code").loc[area, "offset"])
    local = h["start_utc"].dt.tz_convert(None) + pd.Timedelta(hours=off)
    d = pd.DataFrame({"dE": co2.diff(), "dX": h[regressor].diff(), "hour": local.dt.hour,
                      "season": local.dt.month.map(SEASON), "start_utc": h["start_utc"]}).iloc[1:]

    def slope(g):
        x = g["dX"] - g["dX"].mean()
        return float((x * (g["dE"] - g["dE"].mean())).sum() / (x * x).sum())
    s = d.groupby(["season", "hour"])[["dE", "dX"]].apply(slope).rename("mer").reset_index()
    m = pd.DataFrame({"start_utc": h["start_utc"], "hour": local.dt.hour, "season": local.dt.month.map(SEASON)})
    return m.merge(s, on=["season", "hour"], how="left"), off


def avoided(target):
    sites, codes, hourly, rates, arrays = load(target)
    out = {}
    for st in sites.itertuples():
        area = st.balancing_area
        m, off = marginal(hourly, rates, codes, area)
        a = arrays[arrays["store_number"] == st.store_number].copy()
        a["start_utc"] = (pd.to_datetime(a["hour_beginning_lst"]) - pd.Timedelta(hours=off)).dt.tz_localize("UTC")
        j = a.merge(m[["start_utc", "mer"]], on="start_utc", how="left")
        j = j[j["mer"].notna()]
        out[st.city] = dict(area=area, rate=float((j["ac_output_kw"] * j["mer"]).sum() / j["ac_output_kw"].sum()),
                            mwh=float(a["ac_output_kw"].sum() / 1000.0), store=int(st.store_number))
    return out, rates, sites


def asks(target, mwh):
    inv = pd.read_csv(find(target, "corvane_electricity_invoice_lines"),
                      parse_dates=["invoice_date", "service_period_start", "service_period_end"])
    head = inv.drop_duplicates("invoice_number")
    latest = head.sort_values("invoice_date").groupby(
        ["vendor_number", "meter_number", "service_period_start", "service_period_end"]).tail(1)["invoice_number"]
    cur = inv[inv["invoice_number"].isin(set(latest))].copy()
    y0, y1 = pd.Timestamp("2025-01-01"), pd.Timestamp("2025-12-31")
    days = (cur["service_period_end"] - cur["service_period_start"]).dt.days + 1
    inside = ((cur["service_period_end"].clip(upper=y1) - cur["service_period_start"].clip(lower=y0)).dt.days + 1).clip(lower=0)
    cur["frac"] = inside / days
    supplier = cur["vendor_name"].str.contains("Retail Energy")
    d = cur["line_description"]
    # the delivery utility's distribution energy: its kWh lines that are neither transmission nor a tax or assessment
    dist = (~supplier) & (cur["unit_of_measure"] == "KWH") & ~d.str.contains("ransmission|tax|assessment|receipts|excise",
                                                                               case=False, regex=True)
    use = (cur.loc[dist, "quantity"] * cur.loc[dist, "frac"]).groupby(cur.loc[dist, "store_number"]).sum() / 1000.0
    elec = ~d.str.startswith("Gas")
    paid = (cur.loc[elec, "line_amount_usd"] * cur.loc[elec, "frac"]).groupby(cur.loc[elec, "store_number"]).sum()
    return {int(s): dict(use=float(use[s]), price=float(paid[s] / use[s]), share=100.0 * mwh[int(s)] / float(use[s]))
            for s in use.index}


def main(target=None, golden=None):
    target = target or os.path.join(TASK, "target")
    golden = golden or os.path.join(TASK, "golden")
    F = json.load(open(os.path.join(HERE, "figures.json")))
    av, rates, sites = avoided(target)
    order = sorted(av, key=lambda t: -av[t]["rate"])
    bad = []

    def same(label, a, b):
        if a != b:
            bad.append("%s: verifier %s, generator %s" % (label, a, b))
    same("call", order[0], F["call"])
    same("first left out", order[1], F["first_left_out"])
    same("gap", float("%.2f" % (av[order[0]]["rate"] - av[order[1]]["rate"])), F["gap"])
    for t in av:
        same("%s rate" % t, float("%.2f" % av[t]["rate"]), F["stores"][t]["rate"])
        same("%s array MWh" % t, int(round(av[t]["mwh"])), F["stores"][t]["array_mwh"])
    town = {r.balancing_area: r.city for r in sites.itertuples()}
    avg = rates["CO2 output emission rate (lb/MWh)"] / LB_PER_TONNE
    nb = rates["CO2 non-baseload output emission rate (lb/MWh)"] / LB_PER_TONNE
    same("R0 winner", town[avg.idxmax()], F["rungs"]["avg"]["winner"])
    same("R1 winner", town[nb.idxmax()], F["rungs"]["nb"]["winner"])
    same("R0 value", float("%.2f" % avg.max()), F["rungs"]["avg"]["value"])
    same("R1 value", float("%.2f" % nb.max()), F["rungs"]["nb"]["value"])
    A = asks(target, {av[t]["store"]: av[t]["mwh"] for t in av})
    for t in av:
        a = A[av[t]["store"]]
        same("%s use" % t, int(round(a["use"])), F["stores"][t]["use"])
        same("%s share" % t, float("%.1f" % a["share"]), F["stores"][t]["share"])
        same("%s price" % t, int(round(a["price"])), F["stores"][t]["price"])
    hf = pd.read_csv(os.path.join(golden, "pilot_sites_hourly_avoided_emissions_2025.csv"))
    same("hourly rows", len(hf), F["hourly_rows"])
    g = hf.groupby("store_name")[["avoided_co2_kg", "array_output_kwh"]].sum()
    for t in av:
        nm = "Corvane %s" % t
        same("%s hourly file" % t, float("%.2f" % (g.loc[nm, "avoided_co2_kg"] / g.loc[nm, "array_output_kwh"])),
             F["stores"][t]["rate"])
    if bad:
        print("VERIFY FAILED:\n  " + "\n  ".join(bad))
        raise SystemExit(1)
    print("verify: independent recomputation agrees: %s (%.2f t/MWh), %s first left out (%.2f), gap %.2f; all eight "
          "stores' rates, array MWh, use, share and price; R0 %s, R1 %s; the hourly file's %d rows" % (
              order[0], av[order[0]]["rate"], order[1], av[order[1]]["rate"], F["gap"], F["rungs"]["avg"]["winner"],
              F["rungs"]["nb"]["winner"], len(hf)))


if __name__ == "__main__":
    main(*(sys.argv[1:3]))
