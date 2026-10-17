"""Write the task242 pack into a target folder and return the clean truth for the checks."""
import os

import docs
import records as RC
import sim

FILES = {
    "request": "flag_review_request.eml",
    "register": "epi_cell_indicator_register.xlsx",
    "standard": "sop_epi_07_quality_flags.pdf",
    "bulletin": "dengue_bulletin_dec2027.pdf",
    "panelnote": "igm_lot_verification_cover_note.eml",
    "protocol": "serosurvey_2027_protocol.docx",
    "vcsop": "vector_surveillance_sop_extract.pdf",
    "cases": "ncmc_dengue_line_list_2026_27.csv",
    "results": "serosurvey_2027_igm_results.csv",
    "panel": "ngmc_igm_lot_verification_panel.csv",
    "sample": "serosurvey_2027_household_sample.csv",
    "visits": "serosurvey_2027_visits_kobo_export.csv",
    "lab": "ngmc_serology_specimen_register_survey.csv",
    "insp": "dbc_house_inspections_nov2027.csv",
    "wards": "ncmc_ward_master_2027.csv",
    "rain": "ncmc_rain_gauges_daily.csv",
    "fog": "ncmc_fogging_log_2027.csv",
    "dict": "DATA_DICTIONARY.md",
    "readme": "README.md",
}
DISTRACTORS = ["rain", "fog"]


def run(target, documents=True):
    os.makedirs(target, exist_ok=True)
    W = sim.make()
    R = RC.Records(W)
    p = lambda k: os.path.join(target, FILES[k])
    csv = lambda df, k: df.to_csv(p(k), index=False, lineterminator="\n")
    csv(R.line_list(), "cases")
    csv(R.sample(), "sample")
    csv(R.visits(), "visits")
    csv(R.lab_register(), "lab")
    csv(R.results(), "results")
    csv(R.panel(), "panel")
    csv(R.ward_master(), "wards")
    csv(R.inspections(), "insp")
    csv(R.rainfall(), "rain")
    csv(R.fogging(), "fog")
    if documents:
        docs.write_all(target, FILES, R)
    return dict(W=W, R=R)
