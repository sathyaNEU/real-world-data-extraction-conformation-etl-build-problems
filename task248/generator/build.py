"""Write the task248 pack into a target folder and return the simulated world and its records for the checks."""
import os

import docs
import records as RC

FILES = {
    "request": "desk_rota_winter_2028_request.eml",
    "methods": "wastewater_dashboard_methods_v4.pdf",
    "register": "wastewater_sites_register.csv",
    "lab": "phl_wastewater_results_2026-01_2028-04.csv",
    "labnote": "phl_results_export_notes.pdf",
    "contract": "rangeview_report_WL-2801.xlsx",
    "scada": "spw_inlet_historian_hourly_2026-01-05_2028-04-09.csv",
    "scadanote": "spw_historian_export_note.pdf",
    "travel": "spw_travel_times_memo_2025-11.pdf",
    "study": "paired_upstream_study_2026_results.csv",
    "studyreport": "paired_upstream_study_2026_field_report.pdf",
    "dashboard": "dashboard_export_winter_2027.xlsx",
    "rain": "rain_gauges_daily_2026-01_2028-04.csv",
    "eqa": "phl_eqa_returns_2026_2027.xlsx",
    "dict": "DATA_DICTIONARY.md",
    "contents": "folder_contents.md",
    "deliv_xlsx": "winter_2027_episodes_shed_load.xlsx",
    "deliv_docx": "verification_desk_winter_2028.docx",
}
PACK = [k for k in FILES if not k.startswith("deliv_")]
DISTRACTORS = ["rain", "eqa"]
CONTEXT = ["dashboard"]           # the context artifact: the published levels and episodes, correct on their basis


def run(target, documents=True):
    os.makedirs(target, exist_ok=True)
    R = RC.Records()
    p = lambda k: os.path.join(target, FILES[k])
    csv = lambda df, k: df.to_csv(p(k), index=False, lineterminator="\n")
    csv(R.register(), "register")
    csv(R.results(), "lab")
    csv(R.scada(), "scada")
    csv(R.study(), "study")
    csv(R.rainfall(), "rain")
    if documents:
        docs.write_all(target, FILES, R)
    return dict(W=R.W, R=R)
