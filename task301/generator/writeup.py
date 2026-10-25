"""submission.md from figures.json: tags, the recommendation, its components, the steps and the deliverable answers."""
import params as P


def c(x):
    return "{:,}".format(int(x))


def write(path, F):
    FL = P.FILES
    ex = F["export_mwh"]
    a, b = F["ask_a"], F["ask_b"]
    t = []
    t.append("## Tags\n")
    t.append("**Domain:** Energy systems and utilities (generation capacity planning).")
    t.append("**Analytical objective:** Opportunity sizing and decision support.\n")
    t.append("## 1. Final Recommendation\n")
    t.append("**Build Kingsley Fields in 2027: it will export about %s MWh in 2028, its first full year.**"
             % c(F["call_export_mwh"]))
    t.append("Hallam Down receives %.1f per cent more sun than Kingsley Fields, but its ten planned blocks would lose "
             "more than that, at least %.1f per cent of their output, to the dust of the broiler unit beside them, a loss "
             "Wexcombe's fiscal meter averages away and only its inverter blocks show, so it exports no more than %s "
             "MWh. Larkhill Common (%s MWh) and Marston Vale (%s MWh) receive less sun on the same performance.\n"
             % (F["hallam_lead_pct"], F["hallam_loss_range_pct"][0], c(F["hallam_export_range_mwh"][1]),
                c(ex["Larkhill Common"]), c(ex["Marston Vale"])))
    t.append("## 2. Critical Components\n")
    t.append("1. Knowle Park, the one farm on the frame and modules the build repeats, has a measured performance "
             "ratio of **%.2f** (its export over its %.1f MWp and its satellite irradiation from %s to 31 December 2025)."
             % (F["knowle_ratio_2dp"], F["knowle_mwp"], F["knowle_start"]))
    t.append("2. Hallam Down's average-year irradiation is **%.1f** per cent above Kingsley Fields', the best of the "
             "other three." % F["hallam_lead_pct"])
    t.append("3. Wexcombe's three blocks nearest its broiler unit, **%d** to **%d** m from the sheds, produce **%.1f** "
             "to **%.1f** per cent less than its blocks more than **%d** m away, while its fiscal meter runs **%.1f** "
             "per cent above its 2012 to 2014 peers."
             % (F["corner_range_m"][0], F["corner_range_m"][1], F["corner_loss_range_pct"][0],
                F["corner_loss_range_pct"][1], F["far_ref_m"], F["wexcombe_meter_vs_peers_pct"]))
    t.append("4. Carried by block distance to Hallam Down's ten planned blocks (**%d** to **%d** m from its unit) through "
             "its own rain, the deposit takes at least **%.1f** per cent of their output on every fit the Wexcombe blocks "
             "support, more than the %.1f per cent lead, so Hallam Down exports no more than **%s** MWh against "
             "Kingsley Fields' **%s**."
             % (F["hallam_block_range_m"][0], F["hallam_block_range_m"][1], F["hallam_loss_range_pct"][0],
                F["hallam_lead_pct"], c(F["hallam_export_range_mwh"][1]), c(F["call_export_mwh"])))
    t.append("\n## 3. Step-by-Step Solution\n")
    t.append("1. Divided Knowle Park's export in %s by its %.1f MWp (%s) and its irradiation in %s summed over every day "
             "it metered, outage days kept: a performance ratio of %.3f; the four bifacial farms' annual ratios, "
             "log-linear in age with a level for each farm, give a degradation of %.2f per cent a year."
             % (FL["export"], F["knowle_mwp"], FL["register"], FL["weather"], F["knowle_ratio"],
                F["fleet_degradation_pct"]))
    t.append("2. Multiplied each candidate's ten-year average irradiation in %s by %.1f MWp and that ratio, carried at "
             "that degradation from Knowle Park's mean age over its record to the candidate's age at mid-2028 from its "
             "energisation date in %s: Kingsley Fields %s MWh, Larkhill Common %s, Marston Vale %s, Hallam Down %s."
             % (FL["weather"], F["build_mwp"], FL["note"], c(ex["Kingsley Fields"]), c(ex["Larkhill Common"]),
                c(ex["Marston Vale"]), c(F["hallam_clean_export_mwh"])))
    t.append("3. Placed the 10-shed broiler units listed beside Wexcombe and Hallam Down in %s by distance and bearing "
             "from the centroid in %s, and measured every block in %s from the sheds."
             % (FL["environs"], FL["register"], FL["layout"]))
    t.append("4. Divided each Wexcombe block's daily energy in %s by its dc_mwp and by that day's median of the blocks "
             "more than %d m from the sheds, leaving out the block's days in %s: the three nearest run %.1f to %.1f per "
             "cent low, falling through dry spells and recovering after rain."
             % (FL["scada"], F["far_ref_m"], FL["omlog"], F["corner_loss_range_pct"][0], F["corner_loss_range_pct"][1]))
    t.append("5. Fitted each block within %d m a deposit that builds by a daily step on days under %d mm of rain, to no "
             "more than %d per cent, keeps %d per cent of itself on %d to %d mm and %d per cent on %d mm or more (the "
             "thresholds that fit best), with the step falling exponentially with distance, and ran it at each Hallam "
             "Down block through Hallam Down's own rain weighted by its irradiation: a loss of %.1f per cent, %s MWh "
             "against Kingsley Fields' %s; the fits on the farm's median block or a full wash at one threshold take no "
             "less than %.1f per cent."
             % (F["near_m"], F["wash_mm"][0], F["deposit_cap_pct"], F["wash_keep_pct"][0], F["wash_mm"][0],
                F["wash_mm"][1], F["wash_keep_pct"][1], F["wash_mm"][1], F["hallam_loss_pct"], c(F["hallam_export_mwh"]),
                c(F["call_export_mwh"]), F["hallam_loss_range_pct"][0]))
    t.append("6. Pyranometers: %s carries the logger's sensor setting, which stayed on the sensor that came down in 2025, "
             "so each mast's sensor was that one before the installed date in %s and the register's from it (the "
             "sensor that came down has a certificate sent from that mast dated after it); each recorded day's "
             "poa_signal_mvh over the sensitivity of the certificate in force that day in %s for the sensor then in "
             "the mast, summed, over the weather file's irradiation on the same days: %.3f at Hartsfield to %.3f at "
             "Dunsford Lane."
             % (FL["met"], FL["pyrreg"], FL["certs"], min(a.values()), max(a.values())))
    lo_b = min(b, key=b.get)
    hi_b = max(b, key=b.get)
    t.append("7. Alarm response: each fault alarm in %s (UTC) joined to its work order in %s, the van its technician had "
             "that day in %s and that van's first entry at the farm after the alarm in %s, whose times are UK time like "
             "the CMMS's (the CMMS attended stamp at a farm without signal is the tablet's sync after the visit, after "
             "the alarm cleared): averages from %.1f hours at %s to %.1f at %s."
             % (FL["alarms"], FL["workorders"], FL["vans"], FL["geofence"], b[lo_b], lo_b, b[hi_b], hi_b))
    t.append("8. Kingsley Fields exports the most of the four in 2028: build it, %s MWh.\n" % c(F["call_export_mwh"]))
    t.append("## 4. Deliverable Answers\n")
    t.append("### fenmore_site_selection_2027.xlsx\n")
    t.append("1. Site to build in 2027: Kingsley Fields")
    t.append("2. Its export in 2028: %s MWh" % c(F["call_export_mwh"]))
    t.append("3. Each operating farm's 2025 irradiation measured by its met-station pyranometer as a ratio to the site "
             "weather file's, over the days the pyranometer recorded:")
    for k in P.OPERATING:
        t.append("   - %s: %.3f" % (k, a[k]))
    t.append("4. Each operating farm's average hours in 2025 from an inverter fault alarm to the technician who attended "
             "it arriving on site:")
    for k in P.OPERATING:
        t.append("   - %s: %.1f" % (k, b[k]))
    t.append("\n### fenmore_build_paper_2027.docx\n")
    t.append("5. The case for building Kingsley Fields at %s MWh in 2028, and for passing over Hallam Down, whose "
             "broiler-dust loss exceeds its lead in irradiation." % c(F["call_export_mwh"]))
    t.append("6. Chart of each candidate's expected 2028 export: Kingsley Fields %s MWh, highlighted; Larkhill Common %s; "
             "Marston Vale %s; Hallam Down after broiler dust below Kingsley Fields, no more than %s on any fit, from %s "
             "before it."
             % (c(F["call_export_mwh"]), c(ex["Larkhill Common"]), c(ex["Marston Vale"]),
                c(F["hallam_export_range_mwh"][1]), c(F["hallam_clean_export_mwh"])))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(t) + "\n")
