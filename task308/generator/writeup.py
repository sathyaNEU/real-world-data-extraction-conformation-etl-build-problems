"""submission.md from figures.json: every figure emitted, none typed."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P  # noqa: E402


def c(v):
    return format(v, ",")


def usd(v):
    return ("USD %d million" % v) if v >= 0 else ("USD -%d million" % -v)


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    R, N, Y = F["removed_mwh"], F["net_musd"], F["payment_musd"]
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** Energy systems and utilities (generation capacity planning).")
    out.append("**Analytical objective:** Opportunity sizing and decision support.\n")
    out.append("## 1. Final Recommendation\n")
    out.append("**Award the 2027 capacity contract to the %d MW Red Willow firm import: under RA-3 it removes %s MWh of "
               "the 2027 fleet's %s MWh a year of expected unserved energy, a net value of %s after its USD %.1f "
               "million capacity payment.**" % (F["offer_mw"]["Red Willow import"], c(R["Red Willow import"]),
                                                 c(F["base_eue_mwh"]), usd(N["Red Willow import"]),
                                                 Y["Red Willow import"]))
    out.append("Not Ketchum Ridge, the cheapest capacity at USD %.1f million: every hour with a shortfall fell while "
               "the ten peakers on Northgate's interruptible service were out together on lack of fuel, so a peaker "
               "on that service would have been out too and removes %d MWh (%s). Not Sandhill Draw (%s) or Coulee "
               "Flats (%s), whose output is low in those winter hours.\n"
               % (Y["Ketchum Ridge"], R["Ketchum Ridge"], usd(N["Ketchum Ridge"]), usd(N["Sandhill Draw"]),
                  usd(N["Coulee Flats"])))
    out.append("## 2. Critical Components\n")
    out.append("1. The 2027 fleet's expected unserved energy over the ten weather years is **%s MWh** a year."
               % c(F["base_eue_mwh"]))
    out.append("2. **%d** per cent of it falls in hours when all ten Northgate IT peakers were out on lack of fuel "
               "(cause %d), so Ketchum Ridge, on the same service, removes **%d MWh**."
               % (F["share_in_fuel_outage_hours_pct"], F["fuel_cause_code"], R["Ketchum Ridge"]))
    out.append("3. The Red Willow import removes **%s MWh**, a net value of **%s**." % (c(R["Red Willow import"]),
                                                                                  usd(N["Red Willow import"])))
    out.append("")
    out.append("## 3. Step-by-Step Solution\n")
    out.append("1. Put weather_years_2027_hourly.csv on UTC (hour ending in local prevailing time; the starred hour on the autumn change day is the "
               "standard-time 01:00) and read 2019's load column, delivered in kW, in MW.")
    out.append("2. Replayed the 2027 fleet in fleet_list_2027.xlsx (Sandoval 1 retires) through the forced outages "
               "and derates of outage_event_log_2016_2025.csv at each event's latest revision, a part hour for its "
               "part and the least capability governing overlaps (RA-3 sections 4 and 6), with the %d MW import "
               "in every hour the tie is in service (red_willow_tie_outages_2016_2025.csv, CST and CDT stamps): "
               "load less wind, solar, units and imports, where positive, averaged over the ten years, is %s MWh."
               % (F["existing_import_mw"], c(F["base_eue_mwh"])))
    out.append("3. Every one of those shortfall hours fell inside a lack-of-fuel event (cause %d) that took all ten "
               "Elk Prairie, Torrance and Wexford peakers out together; the fleet list puts them on Northgate IT, "
               "the service the Ketchum Ridge offer takes its gas on." % F["fuel_cause_code"])
    out.append("4. Counted each offer alone in every replayed hour (RA-3 section 7): Ketchum Ridge at %d MW times the "
               "share of the Northgate IT peakers' capability available in that hour, %d MWh removed; the Red "
               "Willow import at %d MW whenever the tie is in service, %s MWh; Sandhill Draw and Coulee Flats at "
               "their modelled output in offer_profiles_2016_2025.parquet (hours beginning UTC), %s and %s MWh."
               % (F["offer_mw"]["Ketchum Ridge"], R["Ketchum Ridge"], F["offer_mw"]["Red Willow import"],
                  c(R["Red Willow import"]), c(R["Sandhill Draw"]), c(R["Coulee Flats"])))
    out.append("5. Valued each reduction at USD %s per MWh less the 2027 payment the offers sheet quotes (USD %.1f, "
               "%.1f, %.1f and %.1f million): net %s, %s, %s and %s; the Red Willow import is the award."
               % (c(F["voll"]), Y["Ketchum Ridge"], Y["Red Willow import"], Y["Sandhill Draw"], Y["Coulee Flats"],
                  usd(N["Ketchum Ridge"]), usd(N["Red Willow import"]), usd(N["Sandhill Draw"]),
                  usd(N["Coulee Flats"])))
    out.append("6. Member energy: took the highest version of each interval in mdm_interval_export_2025.parquet, "
               "delivered less received, each point's member from the assignment history of "
               "delivery_point_register_2025.xlsx; where meter_service_orders_2025.csv records a current "
               "transformer replacement, the export kept applying the old multiplier for weeks after it, so each "
               "interval from the replacement on is carried at the new multiplier; summed by member in MWh.")
    out.append("7. 12-CP: the same intervals, with the meters the service orders found on standard time moved an "
               "hour later from the spring change (2025-03-09 03:00 CDT) up to the first interval after the visit "
               "that reset them, and the MDM's estimate for the stamp the reset skipped dropped; each month's peak is the hour with the highest net energy "
               "over all points, and a member's 12-CP average is its net energy in those twelve hours averaged.")
    out.append("")
    out.append("## 4. Deliverable Answers\n")
    out.append("### capacity_award_2027.xlsx\n")
    out.append("1. The 2027 fleet's expected unserved energy: %s MWh a year" % c(F["base_eue_mwh"]))
    out.append("2. Each offer's EUE removed, 2027 capacity payment and net value:")
    for o in P.OFFERS:
        out.append("   - %s: %s MWh removed; payment USD %.1f million; net value %s" % (o, c(R[o]), Y[o], usd(N[o])))
    out.append("3. Award: Red Willow import")
    out.append("4. Each member's 2025 net energy delivered, MWh:")
    for k in P.MEMBERS:
        out.append("   - %s: %s" % (k, c(F["ask_a_mwh"][k])))
    out.append("5. Each member's 2025 12-CP average, MW:")
    for k in P.MEMBERS:
        out.append("   - %s: %.1f" % (k, F["ask_b_mw"][k]))
    out.append("")
    out.append("### capacity_award_2027.docx\n")
    out.append("1. The committee paper recommends the Red Willow import, with a bar chart of the four offers' net "
               "values (the Red Willow import highlighted) and the member allocation table.")
    text = "\n".join(out) + "\n"
    with open(os.path.join(os.path.dirname(HERE), "submission.md"), "w") as fh:
        fh.write(text)


if __name__ == "__main__":
    main()
