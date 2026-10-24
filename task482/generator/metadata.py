"""metadata.json in the task folder: per shipped file its source, date, licence and rows, and the distractors."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
SYN = " (fictional, synthetic records)"
LIC = "CC0-1.0 (synthetic, generated for this task)"
SOURCES = {
    "kettle_and_pine_remittance_report_2025-07_2026-09.csv": ("Kettle & Pine, Lake Protection Fee remittance report", "2026-10-09"),
    "edmr_dmr_export_quillmere_basin_2025-01_2026-09.csv": ("State electronic discharge monitoring report system, export for five basin permits", "2026-10-16"),
    "edmr_parameter_codes.csv": ("State electronic discharge monitoring report system, code lists", "2024-03-01"),
    "lake_protection_fee_ordinance.pdf": ("Quillmere Lake Basin Joint Powers Board, Lake Protection Fee ordinance", "2025-06-12"),
    "lake_protection_fee_returns_2025-07_2026-09.csv": ("Quillmere Lake Basin Fee Office, returns extract", "2026-10-16"),
    "lake_protection_fee_returns_field_list.txt": ("Quillmere Lake Basin Fee Office, returns extract field list", "2026-10-16"),
    "lakeward_stays_remittance_detail_2025-07_2026-09.csv": ("Lakeward Stays, Lake Protection Fee remittance detail", "2026-10-08"),
    "narrows_joint_member_meters_2025_2026.csv": ("Narrows Joint Wastewater Board, member meter reads", "2026-10-02"),
    "quillmere_basin_wastewater_facilities.pdf": ("Quillmere Lake Protection District, wastewater facilities fact sheet", "2026-03-17"),
    "quillmere_county_population_estimates_2024_2026.csv": ("Office of the State Demographer, city and township estimates", "2026-10-15"),
    "quillmere_county_traffic_counts_2024_2026.csv": ("Quillmere County Highway Department, permanent count stations", "2026-10-05"),
    "ruddmere_pinehold_ponds_operating_reports_2025_2026.xlsx": ("Northwoods Utility Services, pond systems' monthly operating reports", "2026-10-09"),
    "seasonal_communities_aid_act.pdf": ("Seasonal Communities Aid Act, unofficial text", "2025-11-04"),
    "sorrelton_coop_station_daily_2025_2026.csv": ("Cooperative observer station at Sorrelton, daily observations", "2026-10-01"),
}
DISTRACTORS = ["target/quillmere_county_traffic_counts_2024_2026.csv", "target/sorrelton_coop_station_daily_2025_2026.csv"]


def main():
    files = []
    for n in sorted(os.listdir(T)):
        src, date = SOURCES[n]
        rows = None
        if n.endswith((".csv", ".txt")):
            rows = sum(1 for _ in open(os.path.join(T, n), "rb")) - (1 if n.endswith(".csv") else 0)
        files.append(dict(file=n, source=src + SYN, date=date, license=LIC, rows=rows))
    meta = dict(task="task482", title="Seasonal Communities Aid certification, 2027",
                setting="A fictional lake basin of eight cities in Minnesota: the state demographer's office, the "
                        "aid statute, the basin's fee office, sanitary utilities, contract operator and two booking "
                        "platforms are fictional, and every record is synthetic.", as_of="2026-10-19",
                deliverables=["seasonal_communities_aid_2027_certification.xlsx",
                              "busiest_month_population_2026.png"],
                distractor_files=DISTRACTORS, files=files)
    assert set(SOURCES) == set(os.listdir(T)), set(SOURCES) ^ set(os.listdir(T))
    json.dump(meta, open(os.path.join(TASK, "metadata.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
