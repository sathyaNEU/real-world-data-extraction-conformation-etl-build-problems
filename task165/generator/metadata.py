"""task165 architecture 2: metadata.json (file roles, provenance, distractors)."""
import json
import os

LIC = "CC0 1.0 (synthetic, authored for this task)"
FILES = [
    ("outfall_014_flow_monitoring_2014-2025.parquet", "evidence",
     "synthetic: the authority's flow monitoring export for the Outfall 014 overflow pipe, both loggers", "2026-01-16"),
    ("wrp_influent_hourly_2014-2025.csv", "evidence",
     "synthetic: the plant historian's hourly influent export for the Southside and Northside WRPs", "2026-01-16"),
    ("outfall_regulator_register.csv", "evidence",
     "synthetic: the authority's register of CSO regulators, receiving sewers and plants", "2025-11-03"),
    ("TM-7_clay_street_storage_alternatives.pdf", "evidence",
     "synthetic: the consultant's technical memorandum on the Clay Street storage alternatives", "2025-12-18"),
    ("consent_decree_appendix_C_cso_control.pdf", "evidence",
     "synthetic: the authority's conformed copy of the consent decree's Appendix C", "2021-09-27"),
    ("northside_tank_scada_2020-2025.csv", "evidence",
     "synthetic: the Northside storage tank's SCADA export, 15-minute values", "2026-01-16"),
    ("northside_tank_om_manual_section4.pdf", "evidence",
     "synthetic: section 4 of the Northside storage tank's O&M manual", "2020-04-24"),
    ("cmms_work_orders_2020-2025.csv", "evidence",
     "synthetic: the maintenance system's completed work orders for the tank, pump station and nearby assets",
     "2026-01-16"),
    ("rain_gauge_tips_2014-2025.csv", "evidence",
     "synthetic: the rain gauge network's tip export, one row per tip", "2026-01-16"),
    ("rain_gauge_inventory.csv", "evidence", "synthetic: the rain gauge network's inventory", "2024-05-08"),
    ("rain_gauge_field_service_2014-2025.xlsx", "evidence",
     "synthetic: the field services technicians' visit log for the rain gauges", "2026-01-09"),
    ("wennick_river_stage_daily_2014-2025.csv", "distractor",
     "synthetic: daily mean stage at the river gauge below the city", "2026-01-12"),
    ("cso_overflow_notifications_2025.csv", "distractor",
     "synthetic: the 2025 public overflow notifications raised by the outfall detectors", "2026-01-05"),
]
DISTRACTOR_REASONS = {
    "wennick_river_stage_daily_2014-2025.csv": "the receiving river's stage looks relevant to how an outfall discharges, "
    "but the outfall meter records the discharge itself and no criterion turns on the river",
    "cso_overflow_notifications_2025.csv": "the notices count 2025's overflows without a tank; the decree evaluates "
    "the whole 2014 to 2025 metered record and no ask needs the notices",
}


def write(task_dir):
    md = {"task": "task165", "architecture": 2, "setting": "2026-01-16",
          "files": [dict(name=n, role=r, source=s, date=d, license=LIC) for n, r, s, d in FILES],
          "distractors": [n for n, r, _, _ in FILES if r == "distractor"],
          "distractor_reasons": DISTRACTOR_REASONS,
          "stated_inputs": [n for n, r, _, _ in FILES if r != "distractor"],
          "deliverables": ["clay_street_storage_evaluation.xlsx", "clay_street_tank_selection_board.pptx"]}
    json.dump(md, open(os.path.join(task_dir, "metadata.json"), "w"), indent=1)
