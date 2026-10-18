"""Write the task247 pack into a target folder and return the simulated world and its records for the checks."""
import os

import docs
import records as RC

FILES = {
    "request": "survey_list_request_2027-11-03.eml",
    "methods": "reef_heat_stress_watch_methods_v3.pdf",
    "guide": "srao_nrt_sst_user_guide_v3_2.pdf",
    "repnote": "srao_reprocessed_sst_release_note_2027-05.pdf",
    "sites": "watch_sites_register.csv",
    "clim": "srao_sst_daily_climatology_watch_pixels.csv",
    "nrt": "srao_nrt_sst_extract_watch_pixels_2018-01-01_2027-11-02.csv",
    "rep": "srao_reprocessed_sst_watch_pixels_2018_2026.csv",
    "bulletins": "heat_stress_bulletins_2027.xlsx",
    "protocol": "post_bleaching_survey_protocol_2023.pdf",
    "survey": "post_bleaching_survey_2023_slates.csv",
    "deployments": "logger_log_2023-08_2027-04.csv",
    "readings": "logger_readings_from_2024-04-01.csv",
    "kd490": "srao_kd490_monthly_watch_pixels_2024_2027.csv",
    "tide": "port_tide_gauge_hourly_2027.csv",
    "dict": "DATA_DICTIONARY.md",
    "readme": "README.md",
    "deliv_xlsx": "reef_heat_stress_2027.xlsx",
    "deliv_pdf": "survey_list_note_2027.pdf",
}
PACK = [k for k in FILES if not k.startswith("deliv_")]
DISTRACTORS = ["kd490", "tide"]


def run(target, documents=True):
    os.makedirs(target, exist_ok=True)
    R = RC.Records()
    p = lambda k: os.path.join(target, FILES[k])
    csv = lambda df, k: df.to_csv(p(k), index=False, lineterminator="\n")
    csv(R.sites(), "sites")
    csv(R.climatology(), "clim")
    csv(R.nrt(), "nrt")
    csv(R.reprocessed(), "rep")
    csv(R.survey_colonies(), "survey")
    csv(R.logger_deployments(), "deployments")
    csv(R.logger_readings(), "readings")
    csv(R.kd490(), "kd490")
    csv(R.tide(), "tide")
    B = R.bulletins()
    if documents:
        docs.write_all(target, FILES, R, B)
    return dict(W=R.W, R=R, B=B)
