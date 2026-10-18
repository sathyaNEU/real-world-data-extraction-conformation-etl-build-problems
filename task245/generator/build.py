"""Write the task245 pack into a target folder and return the simulated year and its records for the checks."""
import os

import docs
import records as RC
import sim

FILES = {
    "request": "aq_audit_2027_pm10_note_request.eml",
    "procedure": "tbc_aq_network_qaqc_procedure_v4.pdf",
    "council": "thornmouth_council_aq_hourly_2027.csv",
    "operator": "tbt_pm10_permit_monitoring_2027.xlsx",
    "met": "port_met_mast_hourly_2027.csv",
    "register": "thornmouth_aq_station_register.csv",
    "servicelog": "aq_network_service_log_2027.xlsx",
    "deposit": "tbt_deposit_gauge_results_2027.xlsx",
    "plan": "tbt_dust_management_monitoring_plan_rev3.pdf",
    "asr2026": "asr2027_table_a3_no2_2026.pdf",
    "bgmap": "background_maps_2027_thornmouth_extract.csv",
    "dict": "DATA_DICTIONARY.md",
    "readme": "README.md",
    "deliv_xlsx": "thornmouth_pm10_2027_data_capture_review.xlsx",
    "deliv_pdf": "asr2027_pm10_data_capture_note.pdf",
}
PACK = [k for k in FILES if not k.startswith("deliv_")]
DISTRACTORS = ["asr2026", "bgmap"]


def run(target, documents=True):
    os.makedirs(target, exist_ok=True)
    W = sim.make()
    R = RC.Records(W)
    p = lambda k: os.path.join(target, FILES[k])
    csv = lambda df, k: df.to_csv(p(k), index=False, lineterminator="\n")
    csv(R.council_hourly(), "council")
    csv(R.met(), "met")
    csv(R.register(), "register")
    csv(R.background_map(), "bgmap")
    if documents:
        docs.write_all(target, FILES, R)
    return dict(W=W, R=R)
