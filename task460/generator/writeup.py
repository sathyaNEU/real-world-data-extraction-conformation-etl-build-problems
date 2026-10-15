"""Write task460/submission.md from generator/figures.json."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W   # noqa: E402

ORDER_TOWNS = [W.AREAS[c]["name"] for c in W.ORDER]


def write(fig_path, out_path):
    F = json.load(open(fig_path))
    S = F["stores"]
    by_rate = sorted(S, key=lambda t: -S[t]["rate_unrounded"])
    pick, second = by_rate[0], by_rate[1]
    others = by_rate[2:]
    lo = min(S[t]["rate"] for t in others)
    hi = max(S[t]["rate"] for t in others)
    rg = F["rungs"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Physical & Environmental Sciences (emissions inventory: the grid emission factor that credits an "
             "on-site solar array, the operating margin of the store's balancing area in the hours the array generates).")
    L.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Corvane should site its 2027 on-site solar pilot at its %s store (store %d).**" % (F["call"],
                                                                                                  S[pick]["store"]))
    L.append("Its array would have avoided %.2f t of grid carbon dioxide per MWh it generated in 2025, the area's coal "
             "fleet following the load from 5 am to 6 pm while gas carries the nights; %s is the first store left out at "
             "%.2f, %.2f below. Not Brackwell, highest on the agency's 2025 average output emission rate (%.2f t/MWh): by "
             "day its coal runs at full output and gas follows the load, so its array avoids %.2f. Not Quillbury, highest "
             "on the non-baseload rate (%.2f): its old coal units run on winter evenings, after sunset, and its array "
             "avoids %.2f. Not Tennaford, highest on a marginal rate fitted to every hour of 2025: coal follows its load "
             "at night and gas through its business day, and its array avoids %.2f.\n" % (
                 S[pick]["rate"], F["first_left_out"], S[second]["rate"], F["gap"], rg["avg"]["value"],
                 S["Brackwell"]["rate"], rg["nb"]["value"], S["Quillbury"]["rate"], S["Tennaford"]["rate"]))
    L.append("## 2. Critical Components\n")
    L.append("1. Gorsefield's array avoids **%.2f** t of carbon dioxide per MWh of its 2025 output." % S[pick]["rate"])
    L.append("2. Halvane is the first store left out at **%.2f** t/MWh, **%.2f** below Gorsefield." % (
        S[second]["rate"], F["gap"]))
    L.append("3. Quillbury, highest on the agency's 2025 non-baseload output emission rate (**%.2f** t/MWh), avoids "
             "**%.2f** t/MWh: its old coal units run after sunset." % (rg["nb"]["value"], S["Quillbury"]["rate"]))
    L.append("")
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Matched each store to its balancing area through its delivery utility in utility_balancing_area_map.csv, "
             "reading Kestrel Point's rows filed under its former code KPLP as KSTP (balancing_area_codes.csv).")
    L.append("2. Put balancing_area_hourly_operating_data_2025.csv (each hour named by its end, UTC) and "
             "pilot_array_output_model_2025.csv (each hour named by its start, local standard time) on one UTC clock.")
    L.append("3. Computed each area's hourly fossil carbon dioxide from its coal, gas and oil net generation at the 2025 "
             "fuel output emission rates in edc_generation_emission_rates_2025.xlsx, pounds per MWh converted to tonnes.")
    L.append("4. Estimated each area's marginal emission rate for each season and local standard hour as the slope of the "
             "hour-to-hour change in that carbon dioxide on the change in the area's net generation, interchange being "
             "scheduled a day ahead (solar_pilot_siting_charter_2027.pdf).")
    L.append("5. Weighted each hour's rate by the store's modelled output, as the charter's measure of what an array "
             "avoids: Gorsefield %.2f, Halvane %.2f, the other six %.2f to %.2f t/MWh." % (
                 S[pick]["rate"], S[second]["rate"], lo, hi))
    L.append("6. Took each store's 2025 metered use from its delivery utility's distribution energy quantity in "
             "corvane_electricity_invoice_lines_fy2025.csv, once per meter and billing cycle from the cycle's latest "
             "invoice, each bill's days in 2025 pro rata, and divided the array's 2025 output by it.")
    L.append("7. Divided every electricity charge on both vendors' latest invoices with service in 2025, each bill "
             "prorated by its days in the year, by that use, leaving out Halvane Gas & Electric's gas lines.")
    L.append("8. Recommended Gorsefield, the store whose array would have avoided the most.\n")
    L.append("## 4. Deliverable Answers\n")
    L.append("### %s\n" % W.GOLDEN["memo"])
    L.append("1. Pilot store: %s; first store left out: %s, %.2f t/MWh below." % (F["call"], F["first_left_out"], F["gap"]))
    L.append("2. Grid carbon dioxide avoided per MWh of the array's 2025 output, tonnes per MWh:")
    for t in by_rate:
        L.append("   - %s: %.2f" % (t, S[t]["rate"]))
    L.append("3. 2025 metered electricity use, MWh:")
    for t in by_rate:
        L.append("   - %s: %s" % (t, "{:,}".format(S[t]["use"])))
    L.append("4. Share of 2025 use the array would have supplied, per cent:")
    for t in by_rate:
        L.append("   - %s: %.1f" % (t, S[t]["share"]))
    L.append("5. Paid for electricity per MWh used in 2025, dollars:")
    for t in by_rate:
        L.append("   - %s: %d" % (t, S[t]["price"]))
    L.append("6. Chart: each store's 2025 monthly metered use against its array's modelled monthly output, one panel per "
             "store, on page 2.\n")
    L.append("### %s\n" % W.GOLDEN["hourly"])
    L.append("1. %s rows, one per store and local standard hour of 2025: store, balancing area, the hour's start in UTC "
             "and local standard time, the array's output in kWh, the hour's marginal carbon dioxide rate in t/MWh and "
             "the carbon dioxide avoided in kg." % "{:,}".format(F["hourly_rows"]))
    L.append("2. Each store's avoided carbon dioxide over its array's output equals its figure in the memo.")
    with open(out_path, "w") as f:
        f.write("\n".join(L) + "\n")
