"""metadata.json in the task folder: per shipped file its source, date, licence and rows, and the distractors."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
SYN = " (fictional, synthetic records)"
LIC = "CC0-1.0 (synthetic, generated for this task)"
SOURCES = {
    "nbr_animals_2025-26.csv": ("Ministry of Agriculture, National Bovine Register, animal export for the programme year 2025-26", "2026-11-09"),
    "nbr_movements_2025-26.csv": ("Ministry of Agriculture, National Bovine Register, movement export for the programme year 2025-26", "2026-11-09"),
    "nbr_herd_register_2026-11.xlsx": ("Ministry of Agriculture, National Bovine Register, herd register", "2026-11-09"),
    "nbr_export_notes.txt": ("Ministry of Agriculture, National Bovine Register, notes to the exports", "2026-11-09"),
    "nso_june_livestock_census_2026.csv": ("National Statistics Office, June Agricultural Census 2026, cattle by farm", "2026-09-17"),
    "nso_june_livestock_census_2026_tables.pdf": ("National Statistics Office, June Agricultural Census 2026, cattle, final results", "2026-09-17"),
    "epo_cattle_ammonia_factors_2025.pdf": ("Environmental Protection Office, Ammonia emission factors for cattle, 2025 edition", "2025-08-18"),
    "moa_livestock_housing_survey_2025.xlsx": ("Ministry of Agriculture, Livestock Housing Survey 2025, housing and slurry storage", "2025-07-14"),
    "arp_designation_rules_2025.pdf": ("Ministry of Agriculture, Ammonia Reduction Programme, designation rules, 2025 edition", "2025-09-30"),
    "lpr_farmed_area_2026.csv": ("Ministry of Agriculture, Land Parcel Register, 2026 declarations by herd", "2026-11-06"),
    "vale_agri_jobs_2026.csv": ("Vale Agri, slurry jobs January to May 2026, supplied to the Ammonia Programme Unit", "2026-11-02"),
    "countrywide_invoice_lines_2026.xlsx": ("Countrywide Slurry Services, invoice lines January to May 2026, supplied to the Ammonia Programme Unit", "2026-11-03"),
    "basin_agri_job_sheets_2026.xlsx": ("Basin Agri, job sheets January to May 2026, supplied to the Ammonia Programme Unit", "2026-11-04"),
    "moa_fertiliser_sales_by_region_2025-26.csv": ("Ministry of Agriculture, fertiliser sales by region, programme year 2025-26", "2026-10-28"),
    "creamery_milk_intake_by_region_2025.csv": ("Ministry of Agriculture, creamery milk intake by region, 2025", "2026-02-20"),
    "nso_pig_poultry_census_2026.csv": ("National Statistics Office, June Agricultural Census 2026, pigs and poultry by region", "2026-09-17"),
}
DISTRACTORS = ["target/moa_fertiliser_sales_by_region_2025-26.csv", "target/creamery_milk_intake_by_region_2025.csv",
               "target/nso_pig_poultry_census_2026.csv"]


def main():
    files = []
    for n in sorted(os.listdir(T)):
        src, date = SOURCES[n]
        rows = None
        if n.endswith((".csv", ".txt")):
            rows = sum(1 for _ in open(os.path.join(T, n), "rb")) - (1 if n.endswith(".csv") else 0)
        files.append(dict(file=n, source=src + SYN, date=date, license=LIC, rows=rows))
    meta = dict(task="task485", title="Ammonia Action Regions 2027: cattle manure ammonia by region, 2025-26",
                setting="A fictional national agriculture department in an unnamed Atlantic country with a national "
                        "bovine register, an annual June livestock census and an ammonia reduction programme: the "
                        "country, its regions, the bodies, the contractors and the people are fictional, and every "
                        "record is synthetic.", as_of="2026-11-10",
                deliverables=["ammonia_action_regions_2027.xlsx", "cattle_ammonia_per_hectare_2025-26.png"],
                distractor_files=DISTRACTORS, stated_inputs=["26 kilograms a hectare", "13 January to 30 April 2026"],
                files=files)
    assert set(SOURCES) == set(os.listdir(T)), set(SOURCES) ^ set(os.listdir(T))
    json.dump(meta, open(os.path.join(TASK, "metadata.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
