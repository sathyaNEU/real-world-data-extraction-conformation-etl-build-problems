"""task464 architecture 10: submission.md, every figure emitted from figures.json."""
import os
import world as W

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def gbp(v):
    return "GBP {:,}".format(v)


def main(F):
    P = F["projects"]
    call, runner = F["call"], F["runner_up"]
    c, r = P[call], P[runner]
    order = [f["name"] for f in W.FEEDERS]
    rung0 = F["rungs"]["head_current"]["winner"]
    L = []
    L += ["## Tags", "",
          "**Domain:** Energy Systems & Utilities (asset condition and maintenance).",
          "**Analytical objective:** Opportunity Sizing & Decision Support.", ""]
    L += ["## 1. Final Recommendation", "",
          "**Fund the %s reconductoring from the 2027/28 losses programme.**" % call,
          ("Its replacement conductor would have removed %.1f MWh of losses in 2025/26, worth %s at GBP %.2f per MWh, "
           "%.1f MWh more than %s at %.1f MWh, because the Hob Moor Solar Park's export runs back through %s's old "
           "overhead line to the Kestle Park estate near Copsewell Cross. Not %s, which leads only when every section is "
           "charged with the feeder-head current. Not %s, whose replaced sections carry its whole load out of the "
           "primary but less current than the solar farm's export." % (
               c["year_mwh"], gbp(c["value_gbp"]), F["losses_value_gbp_mwh"], F["gap_mwh"], runner, r["year_mwh"], call,
               rung0, runner)), ""]
    L += ["## 2. Critical Components", "",
          "1. %s's project replaces **%.2f km** of route and removes **%.3f ohm** per phase." % (call, c["km"], c["dR_ohm"]),
          "2. %s's replaced sections would have lost **%.1f MWh** less in 2025/26." % (call, c["year_mwh"]),
          "3. %s, the runner-up, would have saved **%.1f MWh**." % (runner, r["year_mwh"]), ""]
    L += ["## 3. Step-by-Step Solution", "",
          ("1. Built each feeder's normal running arrangement from the closed sections in hv_network_model.xlsx and placed "
           "every secondary substation (secondary_substations.csv, by site number) and HV customer (hv_connections.csv, "
           "by agreement) on its node."),
          ("2. Took each substation's half-hourly kW and kVAr from lv_monitoring_2025-26.parquet, as kVA times power factor "
           "before its monitor's vendor change, and each HV customer's import less its export from "
           "hv_settlement_2025-26.csv, settlement periods placed on the UTC half-hours."),
          ("3. Summed the flows of every connection beyond each section the brief lists to get the section's current each "
           "half-hour; %s's replaced sections carry the solar farm's export less the load beyond them." % call),
          ("4. Took each replaced section's loss at that current on its existing and its replacement conductor, at 11 kV "
           "and the resistances of hv_conductor_data_EDS-02-0310.pdf, per the brief: %s saves %.1f MWh and %s %.1f MWh."
           % (call, c["year_mwh"], runner, r["year_mwh"])),
          "5. Valued each project's year at GBP %.2f per MWh: %s for %s." % (F["losses_value_gbp_mwh"], gbp(c["value_gbp"]), call),
          ("6. Counted 2025/26 CI and CML per iis_reporting_definitions_2025-26.pdf from interruptions_2023-2026.csv, "
           "dropping the work-management LV jobs at sites already off in an HV incident, ending a site's minutes when "
           "generator_hire_2025-26.xlsx shows a generator connected there, leaving out sites a generator kept on supply "
           "through a planned outage, and dividing by customers_by_substation_2023-2026.csv at 31 March 2026: the "
           "feeders' figures below."),
          "7. Funded %s, with %s the runner-up." % (call, runner), ""]
    L += ["## 4. Deliverable Answers", "", "### losses_programme_2027.xlsx", "",
          "1. Saving in 2025/26 in MWh to one decimal place, and its value at the losses value to the nearest GBP 100:"]
    for k in order:
        L.append("   - %s: %.1f MWh, %s" % (k, P[k]["year_mwh"], gbp(P[k]["value_gbp"])))
    L += ["2. Fund %s." % call, "3. Runner-up: %s." % runner, "",
          "### losses_saving_2027.png", "",
          "1. Bar chart of the eight projects' 2025/26 savings, each bar labelled with its MWh, %s highlighted." % call, "",
          "### iis_feeders_2025-26.csv", "",
          "1. 2025/26 customer interruptions per 100 customers and customer minutes lost per customer, one decimal place:"]
    for k in order:
        v = F["iis"][k]
        L.append("   - %s: CI %.1f, CML %.1f" % (k, v["ci"], v["cml"]))
    L.append("")
    open(os.path.join(BASE, "submission.md"), "w").write("\n".join(L))
    return os.path.join(BASE, "submission.md")
