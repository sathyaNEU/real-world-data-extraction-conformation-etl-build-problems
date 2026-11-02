"""Emits task466/submission.md from generator/figures.json (every figure read, never typed)."""


def fmt(n):
    return "{:,}".format(int(n))


def write(f, path):
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Physical & Environmental Sciences, emissions inventory (landfill methane).")
    L.append("**Analytical objective:** Data Extraction & Conformation (ETL).")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Breck Hollow's 2026 return puts the Authority in %s of the closed landfill methane charge, so the 2027 "
             "budget should carry $%s.**" % (f["tier"], fmt(f["charge_usd"])))
    L.append("The landfill released %d t of methane in 2026, between the %d t and %d t thresholds. Not Tier 3 at %d t, "
             "which scales the year's capture up by the share of hours the blowers ran and so counts the methane drawn "
             "off after each restart a second time. Not Tier 1 at %d t, which divides the capture by %.2f as if the "
             "waste generated nothing while the blowers were down."
             % (f["released_t_nearest_10"], f["threshold_tier2_t"], f["threshold_tier3_t"], f["default_hh8_released_t"],
                f["naive_released_t"], f["ce"]))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. Methane captured in 2026 is **%s t**." % fmt(f["captured_t"]))
    L.append("2. Methane generated in 2026 is **%s t** (nearest 100)." % fmt(f["generated_t_nearest_100"]))
    L.append("3. Methane released in 2026 is **%d t** (nearest 10), in %s." % (f["released_t_nearest_10"], f["tier"]))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Summed each hour's FT-101 flow at normal conditions times its AT-101 methane content times %s kg "
             "(rule %s) in BH_gas_plant_hourly_2024-2026.csv over the 2026 local year (rule %s): %s t captured."
             % (f["rho_n"], f["clauses"][1], f["clauses"][0], fmt(f["captured_t"])))
    L.append("2. Set the %d blower outages of BH_gas_plant_outage_log_2024-2026.xlsx (%s hours down) against the "
             "historian: after each restart the capture runs above its pre-outage level while the wells draw off "
             "methane the waste held during the stop, %d t over the year." % (f["outages_n"], f["down_hours"],
                                                                               round(f["recovered_after_restarts_t"])))
    L.append("3. Read the waste's generation from the steady hours (full blower hours outside the outages and those "
             "recoveries), month by month at the %.2f collection efficiency of Schedule 2 for the geomembrane cap "
             "(BH_site_register_2025.xlsx), over every hour of the year (rule %s): %s t."
             % (f["ce"], f["clauses"][2], fmt(f["generated_t_nearest_100"])))
    L.append("4. Applied rule %s with Schedule 2's %.2f cap oxidation and %.2f destruction efficiency: %d t released, "
             "%s at $%s under rule %s." % (f["clauses"][3], f["ox"], f["de"], f["released_t_nearest_10"], f["tier"],
                                           fmt(f["charge_usd"]), f["clauses"][6]))
    L.append("5. Engine hours and starts (rules %s and %s) from BH_engine_plant_events_2026.txt in site time "
             "converted across the daylight-saving changes: synchronised time from RUNNING to the next STOP, TRIP or "
             "BREAKER OPEN, both engines running when the year opens, each utility power failure ending the run at "
             "the failure's start in the outage log (the controller writes only CONTROLLER POWER UP when the supply "
             "returns); a start is each RUNNING from standstill plus each test run (START REQUEST then STOP with no "
             "RUNNING), never a RUNNING after BREAKER OPEN or a START FAIL."
             % (f["clauses"][4], f["clauses"][5]))
    L.append("6. Flare figures: its gas by difference at the plant (FT-101 less FT-201 and FT-202, all normal cubic "
             "metres) times the methane content, %s kg and %.2f (rule %s); its hours from TEMP PERMISSIVE or TEMP "
             "NORMAL to the next LOW TEMP or FLARE STOP in the event log, with the flare lit when the year opens."
             % (f["rho_n"], f["de"], f["clauses"][7]))
    L.append("7. Surface monitoring from BH_surface_emissions_monitoring_2026.xlsx: exceedances are readings above %d "
             "ppm (%d over the background), the third quarter's readings between the passing morning check and the "
             "failed midday check in SEM_analyser_checks_2026.csv void under plan section %s, and each location's first "
             "re-monitoring is its earliest re-check matched by position, the WGS84 fix converted to the site grid by "
             "the site register's tie."
             % (f["sem_reading_threshold_ppm"], f["sem_threshold_ppm"], f["clauses"][8]))
    L.append("8. The 2027 budget carries $%s for the %s charge." % (fmt(f["charge_usd"]), f["tier"]))
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### breck_hollow_charge_brief_2026.pdf")
    L.append("")
    L.append("1. %s of the closed landfill methane charge." % f["tier"])
    L.append("2. Charge for the 2027 budget: $%s." % fmt(f["charge_usd"]))
    L.append("3. Chart of the 2026 methane released (%d t) as a bar against the %d t and %d t tier thresholds, the tier "
             "bands shaded and labelled." % (f["released_t_nearest_10"], f["threshold_tier2_t"], f["threshold_tier3_t"]))
    L.append("")
    L.append("### breck_hollow_methane_return_2026.xlsx")
    L.append("")
    L.append("1. Methane generated in 2026: %s t." % fmt(f["generated_t_nearest_100"]))
    L.append("2. Methane captured in 2026: %s t." % fmt(f["captured_t"]))
    L.append("3. Methane released in 2026: %d t." % f["released_t_nearest_10"])
    L.append("4. Each engine's operating hours and starts by quarter:")
    for q in (1, 2, 3, 4):
        L.append("   - Q%d: Engine 1 %s h and %d starts; Engine 2 %s h and %d starts" %
                 (q, fmt(f["engine1_hours_q%d" % q]), f["engine1_starts_q%d" % q], fmt(f["engine2_hours_q%d" % q]),
                  f["engine2_starts_q%d" % q]))
    L.append("5. The flare's operating hours and methane destroyed in it by quarter:")
    for q in (1, 2, 3, 4):
        L.append("   - Q%d: %s h, %d t" % (q, fmt(f["flare_hours_q%d" % q]), f["flare_destroyed_t_q%d" % q]))
    L.append("6. Each quarterly walkover's exceedance locations and those still exceedances at their first re-monitoring:")
    for q in (1, 2, 3, 4):
        L.append("   - Q%d: %d exceedance locations, %d still exceedances" % (q, f["sem_exceed_q%d" % q], f["sem_still_q%d" % q]))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
