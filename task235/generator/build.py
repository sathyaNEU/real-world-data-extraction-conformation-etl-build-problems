"""Write the task235 pack into a target folder and return the clean truth for the checks."""
import os

import docs
import params as P
import records as RC
import sim

FILES = {
    "val": "purchase_service_validations_2026-10-05_to_2026-11-09.csv",
    "evt": "warehouse_purchase_completed_2026-10-05_to_2026-11-09.csv",
    "ses": "session_service_starts_2026-10-05_to_2026-11-09.csv",
    "links": "account_service_links_2026-10-05_to_2026-11-09.csv",
    "reg": "build_register.xlsx",
    "rates": "ecb_euro_reference_rates_2026-09-28_to_2026-11-06.csv",
    "cat": "metrics_catalogue_purchase_tracking.pdf",
    "sdk": "tern_sdk_release_notes.md",
    "crash": "crash_free_sessions_by_build.csv",
    "ratings": "store_ratings_by_version.csv",
    "push": "push_campaigns_2026-10.csv",
    "dict": "DATA_DICTIONARY.md",
    "readme": "README.md",
}
DISTRACTORS = ["crash", "ratings", "push"]


def run(target):
    os.makedirs(target, exist_ok=True)
    W = sim.make()
    R = RC.Records(W)
    V = R.validations()
    E = R.events()
    S = R.sessions()
    p = lambda k: os.path.join(target, FILES[k])
    V.to_csv(p("val"), index=False, lineterminator="\n")
    E.to_csv(p("evt"), index=False, lineterminator="\n")
    S.to_csv(p("ses"), index=False, lineterminator="\n")
    R.links().to_csv(p("links"), index=False, lineterminator="\n")
    R.rates().to_csv(p("rates"), index=False, lineterminator="\n")
    R.crash_free().to_csv(p("crash"), index=False, lineterminator="\n")
    R.ratings().to_csv(p("ratings"), index=False, lineterminator="\n")
    R.push().to_csv(p("push"), index=False, lineterminator="\n")
    docs.register(p("reg"))
    docs.catalogue(p("cat"))
    for k, text in (("sdk", docs.SDK_NOTES), ("dict", docs.DICTIONARY), ("readme", docs.README)):
        with open(p(k), "w") as fh:
            fh.write(text)
    return dict(W=W, R=R, V=V, E=E, S=S)
