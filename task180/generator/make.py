"""Build task180 end to end: the world, target/ (every shipped export), the golden figures from target/ alone,
the golden deliverables, metadata.json and a byte-stable target.zip.

    python3 make.py            build
    python3 checks.py          the generator's assertions (run after make)
    python3 verify.py          the independent recomputation (run after make)
"""
import json
import os
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
sys.path.insert(0, HERE)

import params as P          # noqa: E402
import world as W           # noqa: E402
import pack                 # noqa: E402
import analysis as A        # noqa: E402
import golden as G          # noqa: E402
import submission as SUB    # noqa: E402

ZIP_TIME = (2027, 1, 5, 9, 12, 0)

SOURCES = {
    "pd07_release_detection_standard.pdf": "Petroleum Division standard PD-07 Rev. 3, controlled copy",
    "tpc_site_tank_register.xlsx": "Petroleum Division site and tank register (tanks, dispensers, cardlock pumps)",
    "forecourt_controller_config_2027-01-05.json": "Forecourt controller configuration export, all gas bars, 2027-01-05",
    "pos_fuel_sales_by_hose_2024_2026.csv": "Point-of-sale daily hose sales, monthly head-office exports 2024 to 2026 with the December 2026 preliminary",
    "atg_shift_close_inventory_2024_2026.csv": "Tank gauge shift-close inventory readings, gas bars, 2024 to 2026",
    "bills_of_lading_2024_2026.csv": "Terminal bills of lading for co-op consignees, 2024 to 2026",
    "service_work_orders_2024_2026.xlsx": "Service contractor work orders, gas bars, 2024 to 2026",
    "vacuum_truck_manifests_2024_2026.csv": "Vacuum hauler manifests for co-op gas bars, 2024 to 2026",
    "cardlock_gauge_delivery_reports_q4_2026.csv": "Cardlock console delivery reports pulled through the monitoring service at the month-end closes",
    "cardlock_gauge_hourly_inventory_q4_2026.csv": "Cardlock hourly inventory from the monitoring service, 30 Sep 2026 to 1 Jan 2027",
    "cardlock_transactions_q4_2026.csv": "Cardlock host transaction export, 30 Sep 2026 to 1 Jan 2027",
    "yorkton_daily_weather_2024_2026.csv": "Daily weather summary, Yorkton area, 2024 to 2026",
    "cathodic_protection_survey_2026.pdf": "Cathodic protection survey report, steel tanks, September 2026",
    "line_leak_detector_tests_2026.csv": "Annual line leak detector function tests, gas bars, 2026",
}
DISTRACTORS = ["yorkton_daily_weather_2024_2026.csv", "cathodic_protection_survey_2026.pdf",
               "line_leak_detector_tests_2026.csv", "vacuum_truck_manifests_2024_2026.csv"]


def zip_target():
    path = os.path.join(TASK, "target.zip")
    names = sorted(os.listdir(TARGET))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            zi = zipfile.ZipInfo(n, date_time=ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(os.path.join(TARGET, n), "rb") as f:
                z.writestr(zi, f.read())
    return path


def main():
    if os.path.isdir(TARGET):
        shutil.rmtree(TARGET)
    if os.path.isdir(GOLDEN):
        shutil.rmtree(GOLDEN)
    w = W.build()
    files = pack.write_all(w, TARGET)
    pk = A.run(TARGET)
    figs = A.figures(pk)
    with open(os.path.join(HERE, "figures.json"), "w") as f:
        json.dump(figs, f, indent=1, sort_keys=True)
        f.write("\n")
    G.write(pk, GOLDEN)
    meta = dict(answer="; ".join(figs["designated"]), as_of=P.AS_OF.isoformat(), bundle="target/",
                distractor_files=DISTRACTORS, field_terms=[],
                files={n: dict(date=P.AS_OF.isoformat(), licence="Synthetic record, no third party rights",
                               rows=files[n] if n.endswith((".csv", ".xlsx", ".json")) else "",
                               source=SOURCES[n]) for n in sorted(files)})
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(meta, f, indent=1, sort_keys=True)
        f.write("\n")
    zip_target()
    SUB.main()
    print("designated:", figs["designated"])
    print("losses:", {k: v for k, v in figs["loss_lph"].items() if v > 0.5})
    print("files:", len(files))


if __name__ == "__main__":
    main()
