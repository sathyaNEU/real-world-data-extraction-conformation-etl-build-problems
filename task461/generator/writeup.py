"""Write task461/submission.md from generator/figures.json (every number in blocks 1 to 4 comes from there)."""
import json

POINT_NAME = {"VRU-1": "VRU-1", "BAY-4": "BAY-4", "BAY-5": "BAY-5"}


def t1(v):
    return "%.1f" % v


def kg(v):
    return "{:,}".format(int(v))


def kl(v):
    return ("+" if v > 0 else "") + "{:,}".format(int(v))


def write(fig_path, out_path):
    F = json.load(open(fig_path))
    c, comp = F["call"], F["components"]
    rq, ry = F["loading_quarters_t"], F["loading_year_t"]
    rung = F["rungs_distillate_t"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Physical & Environmental Sciences (emissions inventory: a fuel terminal's VOC from product "
             "loading, its storage tanks and its stock account).")
    L.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Report %s tonnes of VOC from product loading for 2026: the Warrenby terminal exceeded its licence's "
             "limit by %s tonnes.**" % (t1(c["total_t"]), t1(c["excess_t"])))
    L.append("Bays 4 and 5 released %s t of it, because %s ML of the diesel loaded there went into compartments whose "
             "previous delivery was petrol made through a service station's vapour balance, and each of those loads "
             "pushed saturated petrol vapour out at a bay with no vapour collection. Not the loading-loss equation at "
             "diesel's own vapour pressure for every diesel load, which puts the two bays at %s t; not each "
             "compartment's previous fill in the terminal's own exports, which misses the petrol lifted at Selwyn "
             "Point (%s t); not every retail-fleet diesel load at petrol vapour, which counts the compartments that "
             "last carried diesel (%s t).\n" % (t1(comp["distillate_bays_t"]), t1(comp["switch_ml"]), t1(rung["R0"]),
                                                t1(rung["R2"]), t1(rung["R1"])))
    L.append("## 2. Critical Components\n")
    L.append("1. Bays 4 and 5 released **%s t** of VOC in 2026." % t1(comp["distillate_bays_t"]))
    L.append("2. **%s ML** of the **%s ML** of diesel loaded at bays 4 and 5 went into compartments whose previous "
             "delivery was petrol made through vapour balance." % (t1(comp["switch_ml"]), t1(comp["distillate_ml"])))
    L.append("3. The VRU-1 stack released **%s t**.\n" % t1(comp["vru_t"]))
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Conformed tas_loads_legacy_2026-01-01_to_2026-06-30.csv (to 30 June) and "
             "tas_loads_2026-06-29_to_2027-01-04.xlsx (from 1 July, its shadow-run rows and cancelled transactions "
             "left out) into one load register on terminal local time, each trailer plate or tanker id resolved to its "
             "fleet unit and dispatch compartment number through tanker_register_2027-01.xlsx.")
    L.append("2. Read dispatch_delivery_dockets_2025-12_to_2026-12.csv on the terminal's clock (each time carries its "
             "own offset) and took, for every load at bays 4 and 5, the last drop that unit's compartment completed "
             "before it: %s ML of the %s ML followed a petrol drop with vr1_hose Y."
             % (t1(comp["switch_ml"]), t1(comp["distillate_ml"])))
    L.append("3. Charged each of those loads its observed litres of saturated petrol vapour (saturation factor %s, the "
             "load month's grade season) beside diesel's own vapour at saturation %s, and every other distillate load "
             "diesel's own vapour alone, each at its meter temperature with Tables 1 and 2 of "
             "CAQA_return_protocol_petroleum_premises_2026.pdf: bays 4 and 5 released %s t."
             % (F["saturation"]["vapour_balanced"], F["saturation"]["normal"], t1(comp["distillate_bays_t"])))
    L.append("4. Summed vru1_outlet_cems_15min_2026.csv under protocol section 3 (VOC_OUT2 g/min converted to kg/h, "
             "each CAL interval at the mean of the valid readings in the hour either side, OFF at zero): %s t."
             % t1(comp["vru_t"]))
    L.append("5. Added the loading points against licence condition L1: %s t, over the limit by %s t."
             % (t1(c["total_t"]), t1(c["excess_t"])))
    L.append("6. Stock account: rolled each 06:00 AEST dip in tank_gauging_daily_2025-12-31_to_2027-01-04.csv back to "
             "local midnight with the loads and VRU-1 returns between, put each diesel load on the tank the shift log "
             "had on the header (a night shift's entries after midnight on the day after their shift date), and added "
             "vru1_plc_events_2026-01-01_to_2027-01-04.csv's product returns to the tank the shift log had VRU-1's "
             "absorber lined up to (TK-1 outside the HV-118, nozzle N7 and HV-119 repairs), the petrol rack's loads on "
             "manual BOLs from the dispatch dockets (source_doc MB-, one bill quantity per compartment, not per line) "
             "and the shift log's transfer meter readings, giving each tank's gain or loss below.")
    L.append("7. Tank method: standing loss at the rate for the seal and vents each tank had at the start of each day "
             "(maintenance_work_orders_2026.csv dates the TK-1, TK-2 and TK-3 secondary seals and the TK-4 and TK-5 "
             "pressure-vacuum vents), working loss on ship_receipts_outturn_2026.xlsx's shore received, giving each "
             "tank's kilograms below.\n")
    L.append("## 4. Deliverable Answers\n")
    L.append("### warrenby_2026_annual_return.csv\n")
    L.append("1. Release at each loading point, tonnes of VOC by quarter:")
    for p in ("VRU-1", "BAY-4", "BAY-5"):
        L.append("   - %s: Q1 %s, Q2 %s, Q3 %s, Q4 %s" % ((POINT_NAME[p],) + tuple(t1(rq["%s Q%d" % (p, q)])
                                                                           for q in range(1, 5))))
    L.append("2. Release from each storage tank over 2026, kilograms of VOC:")
    for tk in ("TK-1", "TK-2", "TK-3", "TK-4", "TK-5"):
        L.append("   - %s: %s" % (tk, kg(F["tanks_kg"][tk])))
    L.append("")
    L.append("### warrenby_2026_return_note.pdf\n")
    L.append("1. The year's release from product loading: %s t." % t1(c["total_t"]))
    L.append("2. Over the limit: yes, by %s t." % t1(c["excess_t"]))
    L.append("3. Chart: monthly stacked bars of the release at VRU-1, BAY-4 and BAY-5, January to December, each "
             "series named in the legend with its year total (%s, %s and %s t)." % (t1(ry["VRU-1"]), t1(ry["BAY-4"]),
                                                                                   t1(ry["BAY-5"])))
    L.append("")
    L.append("### warrenby_2026_stock_account.xlsx\n")
    L.append("1. Gain (+) or loss (-) of each tank in each quarter, kilolitres at 15 C:")
    for tk in ("TK-1", "TK-2", "TK-3", "TK-4", "TK-5"):
        g = F["stock_gain_kl"]
        L.append("   - %s: Q1 %s, Q2 %s, Q3 %s, Q4 %s" % ((tk,) + tuple(kl(g["%s Q%d" % (tk, q)]) for q in range(1, 5))))
    with open(out_path, "w") as f:
        f.write("\n".join(L) + "\n")
