"""Write submission.md from figures.json: every figure in blocks 1 to 4 is emitted, never typed."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TOWN = {"CL-401": "Wynyard", "CL-404": "Canora", "CL-407": "Kamsack", "CL-412": "Russell"}
MON = {10: "October", 11: "November", 12: "December"}


def n10(v):
    return "{:,}".format(v)


def main():
    global F
    F = json.load(open(os.path.join(HERE, "figures.json")))
    it, ca = F["loss_lph"]["GB-131 regular"], F["loss_lph"]["GB-134 regular"]
    tot, met = F["total_lph"], F["meters_lph"]
    hrs = F["quarter_hours"]
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Physical & Environmental Sciences (environmental monitoring and exceedance).")
    L.append("**Analytical objective:** Anomaly Detection & Diagnostics.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Ituna regular (GB-131) and Canora regular (GB-134) go on the January 2027 tightness-testing work order, "
             "having lost %.1f and %.1f litres an hour to the ground over October to December 2026.** Canora's %.1f L/h "
             "shortfall moves with its sales, but its meters, calibrated on 2 July 2026, give away only %.1f L/h of it "
             "at the drift the network's own tank books show. Not Ituna alone, which statistical inventory "
             "reconciliation files by booking every sales-linked loss to the meters. Not Kamsack regular or Foam Lake "
             "diesel, whose %.1f and %.1f L/h shortfalls are what their meters' use since calibration gives away."
             % (it, ca, tot["GB-134 regular"], met["GB-134 regular"], tot["GB-142 regular"], tot["GB-121 diesel"]))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. Canora regular's October to December book shortfall is **%.1f L/h**, of which its meters give away **%.1f L/h**"
             % (tot["GB-134 regular"], met["GB-134 regular"]))
    L.append("2. Kamsack regular's **%.1f L/h** and Foam Lake diesel's **%.1f L/h** shortfalls carry meter over-delivery of "
             "**%.1f L/h** and **%.1f L/h**" % (tot["GB-142 regular"], tot["GB-121 diesel"], met["GB-142 regular"],
                                               met["GB-121 diesel"]))
    L.append("3. The meters drift **%.1f mL per 20 L draft for every 100,000 litres** passed since calibration, one rate "
             "across the network" % F["drift_rate_one_decimal"])
    L.append("4. Ituna regular loses **%.1f L/h** to the ground and Canora regular **%.1f L/h**" % (it, ca))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Built each gas bar tank system's daily book per PD-07 s.3 from the 05:00 closes in "
             "atg_shift_close_inventory_2024_2026.csv, the bills' net litres on the drop's business day in "
             "bills_of_lading_2024_2026.csv and the latest export of each hose-day in pos_fuel_sales_by_hose_2024_2026.csv: "
             "October to December shortfalls of %.1f L/h at Ituna regular, %.1f at Canora regular, %.1f at Kamsack regular "
             "and %.1f at Foam Lake diesel." % (tot["GB-131 regular"], tot["GB-134 regular"], tot["GB-142 regular"],
                                                 tot["GB-121 diesel"]))
    L.append("2. Dated each hose's last calibration or replacement from service_work_orders_2024_2026.xlsx, through the "
             "dispenser serials in forecourt_controller_config_2027-01-05.json and the dispenser numbers in "
             "tpc_site_tank_register.xlsx, and summed each day's hose litres times the litres that hose had passed since: "
             "each tank-quarter's exposure.")
    L.append("3. Fitted one drift per litre over the %d tank-quarters from 2024 Q1 to 2026 Q3 with every hose's reset on "
             "record, quarter shortfall on exposure with no constant: %.1f mL per 20 L for every 100,000 litres."
             % (F["drift_fit_tank_quarters"], F["drift_rate_one_decimal"]))
    L.append("4. Took each system's October to December exposure times that drift out of its shortfall and divided by "
             "the quarter's elapsed hours (%s in Saskatchewan, %s in Manitoba): Ituna regular %.1f L/h and Canora "
             "regular %.1f L/h, every other system near zero." % (n10(hrs[0]), n10(hrs[-1]), it, ca))
    L.append("5. Applied PD-07 s.5: Ituna regular and Canora regular are over %.2f L/h and go on the January work order."
             % F["threshold_lph"])
    L.append("6. For each cardlock bill in bills_of_lading_2024_2026.csv, took the received litres as the matching "
             "report's increase in cardlock_gauge_delivery_reports_q4_2026.csv (one row per delivery number across the "
             "pulls) plus the litres drawn from that tank inside the report window in cardlock_transactions_q4_2026.csv "
             "(UTC less six hours); the %d drops with no report were rebuilt from "
             "cardlock_gauge_hourly_inventory_q4_2026.csv as the rise between the readings either side plus the fills "
             "between them, dated by the rise." % F["cardlock_rebuilt_drops"])
    L.append("7. Summed bill net less received by carrier and by cardlock in the month each drop arrived, to the nearest "
             "10 litres (block 4).")
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### tank_test_workorder_jan2027.pdf")
    L.append("")
    L.append("1. Systems going for testing:")
    L.append("   - Ituna regular, GB-131 tank 1: %.1f litres an hour" % it)
    L.append("   - Canora regular, GB-134 tank 1: %.1f litres an hour" % ca)
    L.append("2. Bar chart on page 2 of every gas bar tank system's loss against the dashed %.2f line, the two systems "
             "going for testing in blue and labelled." % F["threshold_lph"])
    L.append("")
    L.append("### cardlock_drops_q4_2026.xlsx")
    L.append("")
    L.append("1. Litres short of the bills of lading, net of drops that came in over, by carrier:")
    for carrier in sorted({k.split("|")[0] for k in F["cardlock_short_by_carrier"]}):
        L.append("   - %s: %s" % (carrier, ", ".join("%s %s" % (MON[m], n10(F["cardlock_short_by_carrier"]["%s|%d" % (carrier, m)]))
                                                    for m in (10, 11, 12))))
    L.append("2. Litres short of the bills of lading, net of drops that came in over, by cardlock:")
    for site in sorted({k.split("|")[0] for k in F["cardlock_short_by_site"]}):
        L.append("   - %s %s: %s" % (site, TOWN[site], ", ".join("%s %s" % (MON[m], n10(F["cardlock_short_by_site"]["%s|%d" % (site, m)]))
                                                              for m in (10, 11, 12))))
    L.append("")
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(L))


if __name__ == "__main__":
    main()
