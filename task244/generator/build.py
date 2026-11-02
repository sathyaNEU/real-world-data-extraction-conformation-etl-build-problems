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
    "deliv_xlsx": "elfs_2027_flows_quality.xlsx",
    "deliv_docx": "elfs_2027_flows_note.docx",
}
PACK = [k for k in FILES if not k.startswith("deliv_")]
DISTRACTORS = ["projections", "jobcentre", "bulletin"]
# provenance for metadata.json (outside the pack): what each file is, who in the setting made it and, where the file
# itself states it, when; nothing under target/ describes the pack
PROVENANCE = {
    "request": ("the Director of Labour and Social Statistics' request for the release's quality note",
                "Labour and Social Statistics Division", "2028-02-02"),
    "method": ("the survey's methodology note, 2027 edition, revised for the district boundary change",
               "Labour and Social Statistics Division", "2027-04-14"),
    "protocol": ("the supervisors' reinterview protocol, version 3, in force from 2026Q4", "Field Operations Department",
                 "2026-09-22"),
    **{"persons_" + q.lower(): ("the survey's quarterly person file for %s" % q,
                               "Labour and Social Statistics Division", None) for q in P.QUARTERS},
    "reint_results": ("the supervisors' reinterview results for the interviews of 2026Q4 to 2027Q4",
                      "Field Operations Department", None),
    "reint_log": ("the supervisors' reinterview fieldwork log for the interviews of 2026Q4 to 2027Q4",
                  "Field Operations Department", None),
    "flows": ("the 2027 annual labour market flows tables as tabulated, Tables F1 and F2",
              "Labour and Social Statistics Division", "2028-01-28"),
    "gazetteer": ("the survey districts' enumeration areas as from 1 April 2027, with the codes before the boundary "
                  "change", "Labour and Social Statistics Division", None),
    "projections": ("the bureau's projections of the population aged 15 and over by district, sex and age group, 2026 "
                    "to 2028", "Esinmi State Bureau of Statistics", None),
    "jobcentre": ("the job centres' registers of job seekers at each month's end, 2027",
                  "Esinmi State Ministry of Labour and Productivity", "2028-01-09"),
    "bulletin": ("the labour market bulletin for the third quarter of 2027", "Labour and Social Statistics Division",
                 "2027-11-14"),
}


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
