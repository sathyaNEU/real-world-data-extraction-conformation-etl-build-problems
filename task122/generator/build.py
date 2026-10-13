"""task122 generator: build the evidence pack.

    python3 task122/generator/build.py [--out DIR]

Writes DIR/target/ and returns the in-memory world for the checks (DIR defaults to the task folder)."""
import argparse
import json
import os
import shutil
import sys
from datetime import datetime

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import params as P     # noqa: E402
import sim as S        # noqa: E402
import records as R    # noqa: E402
import events as EV    # noqa: E402
import docs            # noqa: E402

F = {
    "protocol": "VMK-4410-202_protocol_v3.0.pdf",
    "sap": "VMK-4410-202_SAP_v2.0.pdf",
    "synopsis": "VMK-4410-301_synopsis_draft_v0.3.pdf",
    "labman": "Tavlund_VMK-4410-202_laboratory_manual_v4.0.xlsx",
    "dict": "VMK-4410-202_data_dictionary.xlsx",
    "sites": "VMK-4410-202_sites.csv",
    "dm": "dm.csv", "sv": "sv.csv", "ex": "ex.csv", "ds": "ds.csv", "lb": "lb.csv", "ae": "ae.csv", "cm": "cm.csv",
    "vs": "vs.csv", "pc": "pc.csv",
    "manifest": "VMK-4410-202_export_manifest.csv",
}
DISTRACTORS = ["vs", "pc"]
DOMAINS = ["dm", "sv", "ex", "ds", "lb", "ae", "cm", "vs", "pc"]
DESC = {
    "protocol": ("the clinical study protocol, version 3.0 (amendment 2)", "Clinical Development", "2024-06-10"),
    "sap": ("the statistical analysis plan, version 2.0, final", "Biostatistics", "2025-11-28"),
    "synopsis": ("the VMK-4410-301 synopsis, draft version 0.3", "Clinical Development", "2026-10-05"),
    "labman": ("the central laboratory's manual for the study, version 4.0", "Tavlund Central Laboratory", "2024-06-17"),
    "dict": ("columns and conventions of the SDTM-style extract", "Data Management (CRO)", "2026-04-15"),
    "sites": ("the sites, their laboratories and activation dates", "Clinical Operations", "2026-04-15"),
    "dm": ("demographics of every screened subject", "Data Management (CRO)", "2026-04-15"),
    "sv": ("visits", "Data Management (CRO)", "2026-04-15"),
    "ex": ("study drug exposure", "Data Management (CRO)", "2026-04-15"),
    "ds": ("disposition and protocol milestones", "Data Management (CRO)", "2026-04-15"),
    "lb": ("laboratory results, central and local", "Data Management (CRO)", "2026-04-15"),
    "ae": ("adverse events", "Data Management (CRO)", "2026-04-15"),
    "cm": ("prior and concomitant medications", "Data Management (CRO)", "2026-04-15"),
    "vs": ("vital signs", "Data Management (CRO)", "2026-04-15"),
    "pc": ("trough concentrations of VMK-4410", "Data Management (CRO)", "2026-04-15"),
    "manifest": ("this list", "Data Management (CRO)", "2026-04-15"),
}
MTIME = {k: v[2] + " 10:30" for k, v in DESC.items()}
MTIME["synopsis"] = "2026-10-05 15:20"


def _fmt(v):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return ""
    if isinstance(v, (float, np.floating)):
        return ("%d" % int(v)) if float(v).is_integer() else ("%.10g" % v)
    return v


def write_csv(df, path):
    out = df.copy()
    for c in out.columns:
        if out[c].dtype.kind == "f" or out[c].dtype == object:
            out[c] = out[c].map(_fmt)
    out.to_csv(path, index=False, lineterminator="\n")


def world(noise_seed=None):
    seed = P.SEED
    Wd = S.simulate(seed, P.NOISE_SEED if noise_seed is None else noise_seed)
    cons = R.consent_dates(np.random.default_rng(seed + 19), Wd)
    Wd["dm"] = R.demographics(np.random.default_rng(seed + 20), Wd, cons)
    samples = R.laboratory(np.random.default_rng(seed + 21), Wd, [])
    Wd["sv"] = R.visits(Wd, samples)
    samples = R.renumber_unscheduled(samples, Wd["sv"])
    allp = pd.concat([Wd["pats"][["SUBJID", "SEX"]], Wd["fails"][["SUBJID", "SEX"]]])
    Wd["samples"] = samples
    Wd["lb"] = R.lab_table(samples, allp)
    lab_hi = {}
    for smp in samples:
        s = smp["SUBJID"]
        if s not in Wd["cs"] or "K" not in smp["TESTS"]:
            continue
        c = Wd["cs"][s]
        k = smp["TESTS"]["K"][2]
        day = S.day_of(smp["DATE"], c.rand)
        if k is not None and k > 5.5 and 2 <= day <= c.last_dose():
            lab_hi.setdefault(s, []).append((smp["DATE"], k))
    Wd["lab_hi"] = lab_hi
    Wd["ae"] = EV.adverse_events(np.random.default_rng(seed + 22), Wd, lab_hi)
    Wd["ex"] = R.dosing(Wd)
    Wd["ds"] = R.disposition(np.random.default_rng(seed + 23), Wd, Wd["sv"], cons)
    Wd["cm"] = EV.medications(np.random.default_rng(seed + 24), Wd, Wd["ae"], cons)
    Wd["vs"] = EV.vital_signs(np.random.default_rng(seed + 25), Wd)
    Wd["pc"] = EV.concentrations(np.random.default_rng(seed + 26), Wd)
    Wd["cons"] = cons
    return Wd


def site_list(Wd):
    st = Wd["sites"]
    n = Wd["pats"].groupby("SITEID").size()
    rows = []
    for _, r in st.iterrows():
        rows.append({"SITEID": r["SITEID"], "COUNTRY": r["COUNTRY_NAME"], "CITY": r["CITY"],
                     "CENTRAL_LABORATORY": P.CENTRAL[r["LAB_HUB"]],
                     "LOCAL_LABORATORY": "%s, %s" % (R.LOCAL_DEPT[r["COUNTRY"]], r["CITY"]),
                     "ACTIVATED": r["ACTIVATED"].isoformat(), "RANDOMISED": int(n.get(r["SITEID"], 0)), "STATUS": "CLOSED"})
    return pd.DataFrame(rows)


def write_pack(outdir, Wd=None):
    tgt = os.path.join(outdir, "target")
    if os.path.exists(tgt):
        shutil.rmtree(tgt)
    os.makedirs(tgt)
    Wd = Wd or world()
    for k in DOMAINS:
        write_csv(Wd[k], os.path.join(tgt, F[k]))
    write_csv(site_list(Wd), os.path.join(tgt, F["sites"]))
    docs.protocol(os.path.join(tgt, F["protocol"]))
    docs.sap(os.path.join(tgt, F["sap"]))
    docs.synopsis(os.path.join(tgt, F["synopsis"]))
    docs.lab_manual(os.path.join(tgt, F["labman"]))
    docs.data_dictionary(os.path.join(tgt, F["dict"]), [F[k] for k in DOMAINS])
    man = []
    for k in F:
        if k == "manifest":
            continue
        rows = len(Wd[k]) if k in DOMAINS else (len(Wd["sites"]) if k == "sites" else "")
        man.append({"file": F[k], "holds": DESC[k][0], "rows": rows, "from": DESC[k][1], "as_at": DESC[k][2]})
    pd.DataFrame(man).to_csv(os.path.join(tgt, F["manifest"]), index=False, lineterminator="\n")
    return tgt, Wd


def set_mtimes(tgt):
    for k, f in F.items():
        t = datetime.strptime(MTIME[k], "%Y-%m-%d %H:%M").timestamp()
        os.utime(os.path.join(tgt, f), (t, t))


def metadata(outdir):
    meta = {"task": "task122", "distractor_files": ["target/" + F[k] for k in DISTRACTORS],
            "deliverables": ["VMK-4410_phase3_dose_recommendation.pdf", "VMK-4410_phase2b_tables.xlsx"],
            "domain": "Biomedical & Clinical Research", "task_type": "longitudinal-outcomes-repeated-measures",
            "objective": "Experiment & Causal Analysis",
            "sources": {"all files": "constructed for this task by the author (synthetic, no third-party data); no licence restriction",
                        "CKD-EPI 2021 equation": "Inker LA et al., N Engl J Med 2021; the published equation, used as a formula only"}}
    with open(os.path.join(outdir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2)
    return meta


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.dirname(HERE))
    a = ap.parse_args()
    tgt, _ = write_pack(a.out)
    set_mtimes(tgt)
    metadata(a.out)
    print("wrote", tgt, len(os.listdir(tgt)), "files")
