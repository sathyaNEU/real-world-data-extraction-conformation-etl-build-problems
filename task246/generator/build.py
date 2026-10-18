"""Write the task246 pack into a target folder and return the simulated round and its records for the checks."""
import os

import docs
import records as RC
import sim

FILES = {
    "request": "lr2027_figures_request.eml",
    "protocol": "laga_nutrition_surveillance_protocol_v2_1.pdf",
    "sample": "lr2027_cluster_sample.csv",
    "teams": "lr2027_survey_teams.xlsx",
    "ncha_anthro": "ncha_lr2027_anthropometry.csv",
    "prk_anthro": "prk_lr2027_anthropometry.xlsx",
    "ncha_test": "ncha_lr2027_muac_standardisation.csv",
    "prk_test": "prk_lr2027_muac_standardisation.xlsx",
    "visits": "lr2027_household_visits.csv",
    "members": "lr2027_household_members.csv",
    "births": "lr2027_household_births.csv",
    "bulletin": "laga_ewb_bulletin_june_2027.pdf",
    "markets": "laga_market_prices_2025_2027.csv",
    "rain": "laga_rainfall_dekadal_2027.csv",
    "dict": "DATA_DICTIONARY.md",
    "readme": "README.md",
    "deliv_xlsx": "lr2027_muac_measurement_review.xlsx",
    "deliv_pdf": "lr2027_gam_measurement_note.pdf",
}
PACK = [k for k in FILES if not k.startswith("deliv_")]
DISTRACTORS = ["bulletin", "markets", "rain"]


def run(target, documents=True):
    os.makedirs(target, exist_ok=True)
    W = sim.make()
    R = RC.Records(W)
    p = lambda k: os.path.join(target, FILES[k])
    csv = lambda df, k: df.to_csv(p(k), index=False, lineterminator="\n")
    csv(R.cluster_sample(), "sample")
    csv(R.ncha_children(), "ncha_anthro")
    csv(R.ncha_test(), "ncha_test")
    csv(R.visits(), "visits")
    csv(R.members(), "members")
    csv(R.births(), "births")
    csv(R.market_prices(), "markets")
    csv(R.rainfall(), "rain")
    if documents:
        docs.write_all(target, FILES, R)
    return dict(W=W, R=R)
