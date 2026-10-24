"""metadata.json in the task folder: per shipped file its source, date, licence and rows, and the distractors."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
SYN = " (fictional, synthetic records)"
LIC = "CC0-1.0 (synthetic, generated for this task)"
SOURCES = {
    "acs5_2019_2023_b25040_halvard_bg.csv": ("ACS 5-year table B25040, 2019-2023 release, Halvard County block groups", "2024-12-12"),
    "acs5_2020_2024_b25040_halvard_bg.csv": ("ACS 5-year table B25040, 2020-2024 release, Halvard County block groups", "2025-12-11"),
    "assessor_housing_units_by_block_group_2025.csv": ("Halvard County Assessor, housing units by block group (2010 block groups)", "2025-09-02"),
    "burn_curtailment_calls_2023_2026.csv": ("Halvard County Air Quality Program, burn curtailment calls", "2026-05-01"),
    "burn_zone_parcels_2025.csv": ("Halvard County Air Quality Program, burn zone parcel list", "2025-12-31"),
    "coldwater_activity_export_2023-07_2026-06.txt": ("Coldwater Fuel & Propane, customer activity export", "2026-07-07"),
    "coldwater_export_record_layout.txt": ("Coldwater Fuel & Propane, export record layout", "2019-03-15"),
    "device_code_scc_crosswalk.csv": ("Halvard County Air Quality Program, device code crosswalk", "2023-03-14"),
    "emission_factors_2023.csv": ("Montana DEQ, emission factor table, 2023 edition", "2023-11-16"),
    "forest_firewood_permits_2019_2025.csv": ("National forest ranger districts, personal-use firewood permits", "2026-02-10"),
    "halvard_coop_propane_by_month_2023_2026.xlsx": ("Halvard Valley Farmers Cooperative, propane gallons by member account and month", "2026-07-08"),
    "heating_fuel_equivalents.csv": ("Montana DEQ energy office, heating fuel equivalents", "2025-09-30"),
    "heating_survey_2024_25_methods.pdf": ("Arrowleaf Survey Research, 2024-25 household heating survey methods", "2025-08-19"),
    "heating_survey_2024_25_responses.csv": ("Arrowleaf Survey Research, 2024-25 household heating survey responses", "2025-08-19"),
    "khlv_daily_temperatures_2023-07_2026-06.csv": ("Halvard airport station KHLV, daily maximum and minimum", "2026-07-02"),
    "maintenance_plan_chapter4_rwc.pdf": ("Halvard Valley PM2.5 maintenance plan, Chapter 4, with County Code 8.30.140", "2023-03-14"),
    "montana_rwc_tool_documentation_2023.pdf": ("Montana DEQ, residential wood combustion tool documentation, 2023 edition", "2023-11-16"),
    "solid_fuel_device_registry_2026-05-15.csv": ("Halvard County solid fuel device registry extract", "2026-05-15"),
    "tab2020_tab2010_bg_relationship_halvard.csv": ("Census Bureau, 2020 to 2010 block group relationship file, Halvard County", "2023-04-18"),
    "wapiti_propane_accounts.csv": ("Wapiti Propane, account list", "2026-07-06"),
    "wapiti_propane_tickets_2023-07_2026-06.csv": ("Wapiti Propane, delivery tickets", "2026-07-06"),
}
DISTRACTORS = ["target/burn_curtailment_calls_2023_2026.csv", "target/forest_firewood_permits_2019_2025.csv"]


def main():
    files = []
    for n in sorted(os.listdir(T)):
        src, date = SOURCES[n]
        rows = None
        if n.endswith((".csv", ".txt")):
            rows = sum(1 for _ in open(os.path.join(T, n), "rb")) - (1 if n.endswith(".csv") else 0)
        files.append(dict(file=n, source=src + SYN, date=date, license=LIC, rows=rows))
    meta = dict(task="task484", title="Halvard Valley burn zone determinations, 2026-27",
                setting="A fictional county air quality program in Montana, its PM2.5 maintenance area's five burn "
                        "zones, three fictional propane distributors and a fictional survey vendor; every record is "
                        "synthetic.", as_of="2026-07-28", deliverables=["rwc_inventory_2025_26.xlsx",
                                                                      "zone_determinations_2026_27.csv"],
                distractor_files=DISTRACTORS, files=files)
    assert set(SOURCES) == set(os.listdir(T)), set(SOURCES) ^ set(os.listdir(T))
    json.dump(meta, open(os.path.join(TASK, "metadata.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
