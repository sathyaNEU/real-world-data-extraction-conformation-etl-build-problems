"""Write the task243 pack into a target folder and return the clean truth for the checks."""
import os

import docs
import records as RC
import sim

FILES = {
    "request": "crip2024_review_request.eml",
    "tor": "crvs_review_terms_of_reference_2023.pdf",
    "deaths": "crs_death_records_extract_20230331.csv",
    "births": "crs_birth_records_extract_20230331.csv",
    "cen2015": "popcen2015_household_population_age_sex_kalinawan.xlsx",
    "cen2020": "cph2020_household_population_age_sex_kalinawan.xlsx",
    "restab": "cph2020_special_tabulation_pdpfp_kalinawan.csv",
    "cover": "cph2020_special_tabulation_cover_note.pdf",
    "directory": "kalinawan_cities_municipalities_directory.csv",
    "roster": "pho_health_office_clinical_staff_2019_2023.xlsx",
    "fhsis": "fhsis_m2_mortality_reports_2015_2022.csv",
    "capacity": "lcro_capacity_survey_jul2023.xlsx",
    "dict": "DATA_DICTIONARY.md",
    "readme": "README.md",
    "deliv_xlsx": "lcro_death_registration_completeness_2015_2020.xlsx",
    "deliv_docx": "crvs_committee_note_2023.docx",
}
PACK = [k for k in FILES if not k.startswith("deliv_")]
DISTRACTORS = ["fhsis", "capacity"]


def run(target, documents=True):
    os.makedirs(target, exist_ok=True)
    W = sim.make()
    R = RC.Records(W)
    p = lambda k: os.path.join(target, FILES[k])
    csv = lambda df, k: df.to_csv(p(k), index=False, lineterminator="\n")
    csv(R.death_extract(), "deaths")
    csv(R.birth_extract(), "births")
    csv(R.residence_tab(), "restab")
    csv(R.directory(), "directory")
    csv(R.fhsis(), "fhsis")
    if documents:
        docs.write_all(target, FILES, R)
    return dict(W=W, R=R)
