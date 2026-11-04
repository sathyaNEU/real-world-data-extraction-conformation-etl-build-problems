"""metadata.json: every pack file with its source, date, licence and row count, the two distractors and why each is
unused, and the deliverables."""
import json
import os

import world as W

LIC = "CC0-1.0 (synthetic, generated for this task)"
SOURCES = {
    "power": ("%s (fictional), synthetic records" % W.UTILITY),
    "pump_tests": "the ranch's pump test contractors (fictional), synthetic reports",
    "levels": "the ranch's level loggers and technician log (fictional), synthetic records",
    "ranch": "%s (fictional), synthetic records" % W.COMPANY,
    "agency": "%s (fictional), synthetic records" % W.AGENCY,
    "district": "%s (fictional), synthetic records" % W.DISTRICT,
    "weather": "a weather station record in the style of a state network (fictional station), synthetic",
}
DATES = {"power/vrp_usage_export_2025-09-01_2026-03-31.csv": "2026-04-02",
         "power/vrp_interval_data_2026-04-01_2026-10-31.csv": "2026-11-01",
         "power/vrp_rate_change_confirmation_2026-05-14.pdf": "2026-05-14",
         "power/vrp_agricultural_tou_schedules_2026.pdf": "2026-02-18",
         "ranch/ochre_flats_well_register.xlsx": "2026-10-28", "ranch/totalizer_reads_wy2026.xlsx": "2026-11-02",
         "levels/logger_download_log.csv": "2026-11-01",
         "agency/sallow_plains_gsa_wy2026_allocation_notice.pdf": "2026-10-15",
         "agency/wy2026_extraction_return_template.csv": "2026-10-15",
         "district/alkali_slough_wd_deliveries_wy2026.csv": "2026-10-09",
         "weather/sallow_plains_west_station_daily_2025-09_2026-10.csv": "2026-11-01"}
DISTRACTORS = [
    {"file": W.FILES["district"], "why": "the district's canal deliveries to the ranch's turnouts: surface water, which the "
                                        "agency's groundwater allocation and extraction return do not count"},
    {"file": W.FILES["cimis"], "why": "daily reference evapotranspiration and weather at a nearby station: crop demand, "
                                     "not a record of what any well pumped"},
]


def write(path, n):
    target = os.path.join(os.path.dirname(path), "target")
    files = []
    for root, _, fs in os.walk(target):
        for f in sorted(fs):
            rel = os.path.relpath(os.path.join(root, f), target)
            top = rel.split(os.sep)[0]
            rows = None
            if rel.endswith(".csv"):
                rows = sum(1 for _ in open(os.path.join(root, f), encoding="utf-8")) - 1
            date = DATES.get(rel, "2026-11-01" if top == "levels" else ("2025-09-25" if top == "pump_tests" else "2026-11-01"))
            role = "distractor" if rel in (W.FILES["district"], W.FILES["cimis"]) else "input"
            files.append({"path": rel, "source": SOURCES[top], "date": date, "license": LIC, "rows": rows, "role": role})
    files.sort(key=lambda r: r["path"])
    meta = {"task": "task476",
            "title": "Ochre Flats Farming Company water year 2026 groundwater extraction return and transfer purchase",
            "setting": "A fictional farming company in a fictional subbasin of California's San Joaquin Valley; every "
                       "record is synthetic.",
            "as_of": "2026-11-02", "files": files, "distractors": DISTRACTORS,
            "deliverables": ["wy2026_extraction_return.csv", "transfer_purchase_memo.docx"]}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
