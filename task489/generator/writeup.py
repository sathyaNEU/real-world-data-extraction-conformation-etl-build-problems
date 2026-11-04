"""task489: submission.md from generator/figures.json. Every number in blocks 1 to 4 is read from figures.json."""
import json


def t2(x):
    return "%.2f" % x


def write(fig_path, out_path):
    f = json.load(open(fig_path))
    pads = f["pads"]
    call = f["call"]
    big = f["rivals"]["big_slug"]
    dry = f["rivals"]["dry"]
    low = min(call, key=lambda p: pads[p]["int_t"])
    high_out = max((p for p in pads if not pads[p]["in"]), key=lambda p: pads[p]["int_t"])
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Physical & Environmental Sciences (emissions inventory).")
    L.append("**Analytical objective:** Data Extraction & Conformation (ETL).")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Convert the separator level controllers at %s in 2027.**" % (", ".join(call[:-1]) + " and " + call[-1]))
    L.append("Each pad's intermittent-vent controllers vented more than the plan's %s t of methane in 2026, the lowest "
             "being %s at %s t, and the highest pad left out is %s at %s t. Not %s, whose plunger slugs overfill their "
             "separators' level band: each slug empties the band in one dump, so the liquid-over-band count every "
             "flowing separator and the five dump counters support overstates them. Not %s, whose dry plunger wells "
             "bring slugs far smaller than the band: many arrivals go into each dump, so one dump per arrival "
             "overstates them." % (f["line_t"], low, t2(pads[low]["int_t"]), high_out,
                                              t2(pads[high_out]["int_t"]), ", ".join(big[:-1]) + " and " + big[-1],
                                              ", ".join(dry[:-1]) + " and " + dry[-1]))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. %s, the lowest pad in the conversion, vented **%s t**; %s, the highest pad out, **%s t**." % (
        low, t2(pads[low]["int_t"]), high_out, t2(pads[high_out]["int_t"])))
    L.append("2. The pads whose plunger slugs exceed their band vented **%s**." % (
        ", ".join("%s %s t" % (p, t2(pads[p]["int_t"])) for p in big)))
    L.append("3. The pads whose dry plunger wells bring slugs far smaller than their band vented **%s**." % (
        ", ".join("%s %s t" % (p, t2(pads[p]["int_t"])) for p in dry)))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    c = f["constants"]
    L.append("1. Took each separator's level band from its bore and controller span in deep_basin_equipment_register.xlsx "
             "(Vessels) and each level controller's supply gas per dump cycle from its maker's data sheet (MRS-03 4.2), at "
             "%s m3 per scf, the pad's 2026 methane fraction in gas_analyses_2025_2026.csv and %s kg per m3 (MRS-03 3.3, 4.4)."
             % (c["scf_to_m3"], c["ch4_kg_m3"]))
    L.append("2. Counted the five automated separators' dump cycles from scada_dump_counters_2026.csv over the production "
             "days (MRS-03 3.2, 4.2), each counter wrapping at %s." % "{:,}".format(c["wrap"]))
    L.append("3. Divided each flowing well's 2026 condensate and water in daily_well_volumes_2026.csv by its separator's band.")
    L.append("4. For each plunger well, shared each production day's liquid over that day's arrivals in "
             "plunger_cycles_2026.csv (each cycle once by controller serial and cycle count, the moved controllers placed "
             "on their wells by deep_basin_work_orders_2026.csv) and replayed the level arrival by arrival: a slug at or "
             "above the band is one dump, smaller slugs accumulate until the band fills.")
    L.append("5. Summed each pad's intermittent-vent methane and took the pads above %s t (methane_reduction_plan_2027.docx, "
             "section 3)." % f["line_t"])
    L.append("6. Counted each plunger well's cycles without an arrival as the rise in its controller's cycle count less the "
             "rise in its arrival count over the production days (the PCX-300 counters), on the well each unit was on.")
    L.append("7. Gave each sales gas pressure controller the survey's reading where sheldrake_pneumatic_survey_2026.pdf "
             "measured that device (found by pad, model and survey date, since the re-piped pads' tags were renumbered "
             "after the survey), its maker's rating otherwise, over its own stint as the work orders and the register date it "
             "and for the hours its supply was on (MRS-03 4.3), and summed by maker and area.")
    L.append("8. Recommended converting the %s pads above the line." % "{:d}".format(f["call_count"]))
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### larchmere_source_inventory_2026.xlsx")
    L.append("")
    L.append("1. Methane each intermittent-vent controller vented in 2026, kilograms:")
    for k in sorted(f["lc_kg"]):
        L.append("   - %s: %s kg" % (k, "{:,}".format(f["lc_kg"][k])))
    L.append("2. Each pad's 2026 intermittent-vent methane on the pads sheet, tonnes:")
    for p in sorted(pads):
        L.append("   - %s: %s t%s" % (p, t2(pads[p]["int_t"]), ", in the conversion" if pads[p]["in"] else ""))
    L.append("3. Each plunger lift well's 2026 cycles that ended without the plunger arriving:")
    for w in sorted(f["nonarrivals"]):
        L.append("   - %s: %s cycles" % (w, "{:,}".format(f["nonarrivals"][w])))
    L.append("4. The sales gas pressure controllers' 2026 methane for each maker in each area, kilograms:")
    for k in sorted(f["bleed_by_maker_area"]):
        L.append("   - %s: %s kg" % (k, "{:,}".format(f["bleed_by_maker_area"][k])))
    L.append("")
    L.append("### controller_conversion_2027.pptx")
    L.append("")
    L.append("1. Slide 1 lists the pads in the conversion with each pad's 2026 intermittent-vent methane: %s." % (
        "; ".join("%s %s t" % (p, t2(pads[p]["int_t"])) for p in sorted(call, key=lambda p: -pads[p]["int_t"]))))
    L.append("2. Slide 2 is a bar chart of every pad's 2026 intermittent-vent methane in descending order against a dashed "
             "line at the plan's %s t, the conversion pads in blue." % f["line_t"])
    L.append("")
    open(out_path, "w").write("\n".join(L))
