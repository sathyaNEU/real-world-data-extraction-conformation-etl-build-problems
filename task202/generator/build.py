"""Write the task202 pack into a target folder and return the simulated world for the checks."""
import os

import docs
import records as RC
import sim

FILES = {
    "portal": "portal_awards_2025-01_2027-03.csv",
    "ret2425": "hrg_claim_returns_fy2024-25.xlsx",
    "ret2526": "hrg_claim_returns_fy2025-26.xlsx",
    "ret2627": "hrg_claim_returns_fy2026-27.xlsx",
    "policy": "hrg_operating_policy_2027_edition.pdf",
    "register": "hrg_partner_accreditation_register.csv",
    "xwalk": "partner_identifier_crosswalk.csv",
    "bands": "household_size_bands.csv",
    "prov": "province_reference.csv",
    "dict": "DATA_DICTIONARY.md",
    "manifest": "export_manifest.csv",
    "request": "referral_ceiling_request.eml",
    "summary": "hrg_annual_report_partner_summary_fy2025-26.pdf",
    "treasury": "treasury_disbursement_runs_2026_2027.csv",
    "followup": "hrg_household_followup_survey_2026.csv",
}
PACK = list(FILES)
DISTRACTORS = ["summary", "treasury", "followup"]


def run(target, documents=True):
    os.makedirs(target, exist_ok=True)
    W = sim.make()
    R = RC.Records(W)
    p = lambda k: os.path.join(target, FILES[k])
    out = lambda df, k: df.to_csv(p(k), index=False, lineterminator="\n")
    out(R.portal_awards(), "portal")
    out(R.register(), "register")
    out(R.crosswalk(), "xwalk")
    out(R.bands(), "bands")
    out(R.provinces(), "prov")
    out(R.treasury(), "treasury")
    out(R.followup(), "followup")
    if documents:
        docs.write_all(target, FILES, R, W, PACK)
    return dict(W=W, R=R)
