"""Write the task244 pack into a target folder and return the simulated survey and its records for the checks."""
import os

import docs
import params as P
import records as RC
import sim

FILES = {
    "request": "elfs_2027_flows_release_request.eml",
    "method": "elfs_methodology_note_2027.pdf",
    "protocol": "elfs_reinterview_protocol_v3.pdf",
    **{"persons_" + q.lower(): "elfs_%s_persons.csv" % q.lower() for q in P.QUARTERS},
    "reint_results": "elfs_reinterview_results_2026q4_2027q4.csv",
    "reint_log": "elfs_reinterview_fieldwork_log_2026q4_2027q4.csv",
    "flows": "elfs_2027_annual_flows_tables.xlsx",
    "gazetteer": "elfs_district_gazetteer_2027.csv",
    "projections": "esbs_population_projections_2026_2028.csv",
    "jobcentre": "esinmi_job_centre_registers_2027.xlsx",
    "bulletin": "elfs_labour_market_bulletin_2027q3.pdf",
    "dict": "DATA_DICTIONARY.md",
    "readme": "README.md",
    "deliv_xlsx": "elfs_2027_flows_quality.xlsx",
    "deliv_docx": "elfs_2027_flows_note.docx",
}
PACK = [k for k in FILES if not k.startswith("deliv_")]
DISTRACTORS = ["projections", "jobcentre", "bulletin"]


def run(target, documents=True, seed=P.SIM_SEED):
    os.makedirs(target, exist_ok=True)
    W = sim.make(seed)
    R = RC.Records(W)
    p = lambda k: os.path.join(target, FILES[k])
    csv = lambda df, k: df.to_csv(p(k), index=False, lineterminator="\n")
    for q in P.QUARTERS:
        csv(R.person_file(q), "persons_" + q.lower())
    csv(R.reint_results(), "reint_results")
    csv(R.reint_log(), "reint_log")
    csv(R.gazetteer(), "gazetteer")
    csv(R.projections(), "projections")
    if documents:
        docs.write_all(target, FILES, R)
    return dict(W=W, R=R)
