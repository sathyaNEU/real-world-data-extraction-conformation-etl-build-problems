"""metadata.json in the task folder: per shipped file its source, date, licence and rows, and the distractors."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
SYN = " (fictional, synthetic records)"
LIC = "CC0-1.0 (synthetic, generated for this task)"
SOURCES = {
    "ems_property_electorate_2022-2025.csv": ("Lorrimere District Council, Electoral Services, property electorate report, revised registers 2022 to 2025", "2026-10-12"),
    "ELECTRA_PROPERTY_ELECTORATE_REV_2020.txt": ("Lorrimere District Council, Electra export, property electorate report, 2020 revised register", "2022-03-04"),
    "ELECTRA_PROPERTY_ELECTORATE_REV_2021.txt": ("Lorrimere District Council, Electra export, property electorate report, 2021 revised register", "2022-03-04"),
    "ELECTRA_NOTICES_OF_ALTERATION_2021-01_2022-03.txt": ("Lorrimere District Council, Electra export, notices of alteration", "2022-03-04"),
    "ems_migration_property_xref_2022-03.csv": ("Lorrimere District Council, Electoral Services, migration property cross-reference", "2022-03-07"),
    "llpg_extract_2026-10-12.csv": ("Lorrimere District Council, local land and property gazetteer extract", "2026-10-12"),
    "housing_completions_monitoring_2014-2026.xlsx": ("Lorrimere District Council, Planning Policy, housing completions monitoring", "2026-10-09"),
    "housing_trajectory_2026-09-30.xlsx": ("Lorrimere District Council, Planning Policy, housing trajectory", "2026-10-08"),
    "polling_district_review_2023_schedule.csv": ("Lorrimere District Council, review of polling districts 2023, schedule", "2023-01-30"),
    "wards_councillors_2014_order.csv": ("Lorrimere District Council, wards and councillors under the 2014 electoral changes order", "2026-10-12"),
    "snpp_2022based_lorrimere.csv": ("The statistics office, 2022-based sub-national population projections, Lorrimere extract", "2024-06-25"),
    "council_tax_dwellings_by_band_ward_2025-09.csv": ("Lorrimere District Council, Revenues, valuation list dwellings by band and ward", "2025-09-02"),
    "lorrimere_review_data_notes.txt": ("Lorrimere District Council, data supplied for the electoral review, field guide", "2026-10-12"),
    "lgbc_electorate_forecast_guidance_2024.pdf": ("Local Government Boundary Commission, technical guidance note 3 with the review letter", "2026-03-02"),
    "lorrimere_annual_canvass_report_2025.pdf": ("Lorrimere District Council, annual canvass report 2025", "2025-12-12"),
}
DISTRACTORS = ["target/snpp_2022based_lorrimere.csv", "target/council_tax_dwellings_by_band_ward_2025-09.csv"]


def main():
    files = []
    for n in sorted(os.listdir(T)):
        src, date = SOURCES[n]
        rows = None
        if n.endswith((".csv", ".txt")):
            rows = sum(1 for _ in open(os.path.join(T, n), "rb")) - (1 if n.endswith(".csv") else 0)
        files.append(dict(file=n, source=src + SYN, date=date, license=LIC, rows=rows))
    meta = dict(task="task485", title="Lorrimere electoral review: electorate forecast 2032",
                setting="A fictional district council in an unnamed UK-like country with individual electoral "
                        "registration and an annual canvass, and its national boundary commission: the district, its "
                        "wards, the bodies and the people are fictional, and every record is synthetic.", as_of="2026-10-16",
                deliverables=["ward_electorate_forecast_2032.xlsx", "ward_variance_2032.png"],
                distractor_files=DISTRACTORS, stated_inputs=["43", "10 per cent"], files=files)
    assert set(SOURCES) == set(os.listdir(T)), set(SOURCES) ^ set(os.listdir(T))
    json.dump(meta, open(os.path.join(TASK, "metadata.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
