"""Write the task241 pack into a target folder and return the clean truth for the checks."""
import os
from zoneinfo import ZoneInfo

import pandas as pd

import docs
import records as RC
import sim

FILES = {
    "thread": "ioa_dmqc_2027_release_thread.eml",
    "refnote": "ioa_reference_data_note.docx",
    "models": "ibfa_float_models.pdf",
    "register": "ibfa_float_register.csv",
    "profiles": "ibfa_profiles_2027.csv",
    "levels": "ibfa_profile_levels_2027.csv",
    "technical": "ibfa_cycle_technical_2027.csv",
    "deliveries": "ioa_dac_receipt_log_2027.csv",
    "arch_casts": "ioa_ctd_archive_stations.csv",
    "arch_levels": "ioa_ctd_archive_levels.csv",
    "intl_casts": "rhd_extract_iberian_basin_stations.csv",
    "intl_levels": "rhd_extract_iberian_basin_levels.csv",
    "recoveries": "ibfa_recovered_sensor_checks.csv",
    "oxygen": "ibfa_oxygen_2027.csv",
    "dict": "DATA_DICTIONARY.md",
    "readme": "README.md",
}
DISTRACTORS = ["recoveries", "oxygen"]
LISBON = ZoneInfo("Europe/Lisbon")


def lisbon(stamps):
    """UTC stamps as the data centre's receiving server writes them: Lisbon wall-clock time, no offset"""
    t = pd.to_datetime(pd.Series(stamps), utc=True).dt.tz_convert(LISBON)
    return t.dt.strftime("%Y-%m-%d %H:%M:%S").values


def run(target, documents=True):
    os.makedirs(target, exist_ok=True)
    W = sim.make()
    R = RC.Records(W)
    p = lambda k: os.path.join(target, FILES[k])
    csv = lambda df, k: df.to_csv(p(k), index=False, lineterminator="\n")
    csv(R.register(), "register")
    csv(R.profiles(), "profiles")
    csv(R.levels(), "levels")
    csv(R.technical(), "technical")
    d = R.deliveries()
    d.insert(0, "received", lisbon(d.pop("delivered")))
    csv(d, "deliveries")
    csv(R.archive_casts(), "arch_casts")
    csv(R.archive_levels(), "arch_levels")
    csv(R.intl_casts(), "intl_casts")
    csv(R.intl_levels(), "intl_levels")
    csv(R.recoveries(), "recoveries")
    csv(R.oxygen(), "oxygen")
    if documents:
        docs.thread(p("thread"), FILES)
        docs.reference_note(p("refnote"), FILES)
        docs.models(p("models"), R.register())
        with open(p("dict"), "w") as fh:
            fh.write(docs.dictionary(FILES))
        with open(p("readme"), "w") as fh:
            fh.write(docs.readme(FILES))
    return dict(W=W, R=R)
