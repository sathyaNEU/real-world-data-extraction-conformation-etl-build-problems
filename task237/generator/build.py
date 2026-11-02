"""Write the task237 pack into a target folder and return the clean truth for the checks.

No file in the pack describes the data (dataset-generation section 3): there is no readme, dictionary, codebook or
manifest. Each file carries its own conventions the way its system writes them (the export's UTC columns, the long
file's one row per variable reached, each vendor's own value labels), the organisation's rules sit in TAS-4 and the
manual, and every file's provenance is in metadata.json, outside target/."""
import os

import numpy as np

import docs
import estim as E
import records as RC
import sim

FILES = {
    "online": "ncp_bcs12_pilot_export_wave6.csv",
    "ledger": "ncp_incentive_ledger_bcs12_pilot.csv",
    "para": "ncp_paradata_bcs12_pilot.csv",
    "ncp_labels": "ncp_bcs12_pilot_value_labels.csv",
    "capi": "flr_bcs12_pilot_interviews_long.csv",
    "bc": "flr_backcheck_log_bcs12_pilot.csv",
    "flr_labels": "flr_bcs12_pilot_value_labels.csv",
    "reg": "bcs12_translation_register_wave6.xlsx",
    "wave5": "ccs_wave5_bcs12_results_by_region.csv",
    "std": "translation_adaptation_standard_TAS-4.pdf",
    "manual": "bcs12_technical_manual_english.pdf",
}
DISTRACTORS = ["para", "wave5"]


def run(target):
    os.makedirs(target, exist_ok=True)
    W = sim.make()
    R = RC.Records(W)
    online, ledger, para = R.online()
    capi, bc = R.capi()
    reg = R.register()
    p = lambda k: os.path.join(target, FILES[k])
    csv = lambda df, k: df.to_csv(p(k), index=False, lineterminator="\n")
    csv(online, "online")
    csv(ledger, "ledger")
    csv(para, "para")
    csv(R.ncp_labels(), "ncp_labels")
    csv(capi, "capi")
    csv(bc, "bc")
    csv(R.flr_labels(), "flr_labels")
    csv(R.wave5(), "wave5")
    docs.register(p("reg"), reg)
    docs.standard(p("std"))
    X = W.english()
    S = np.cov(X, rowvar=False)
    eng = dict(n=len(X), rel="%.2f" % E.trait_share(S)["share"])
    docs.manual(p("manual"), eng)
    return dict(W=W, R=R, online=online, ledger=ledger, capi=capi, bc=bc, reg=reg, english=eng)
