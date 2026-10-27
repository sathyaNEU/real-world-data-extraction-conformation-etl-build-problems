"""metadata.json in the task folder: per shipped file its source, date, licence and rows, and the distractors."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
sys.path.insert(0, HERE)

import common as K  # noqa: E402

SYN = " (fictional, synthetic records)"
LIC = "CC0-1.0 (synthetic, generated for this task)"
CVN = "Corvane Therapeutics"
EDC = CVN + ", CVN2184-UC-201 clinical database as locked on 14 July 2026"
SOURCES = {
    K.SITES: (EDC + ", site list", "2026-07-14"),
    K.RAND: ("Corvane Therapeutics interactive response technology, randomisation log, unblinded at database lock", "2026-07-14"),
    K.BASE: (EDC + ", baseline characteristics", "2026-07-14"),
    K.DOSE: (EDC + ", study drug infusion records", "2026-07-14"),
    K.VISITS: (EDC + ", visit dates", "2026-07-14"),
    K.CONC: ("Brightwater Bioanalytics, dovikizumab serum concentration results for CVN2184-UC-201", "2026-07-09"),
    K.EFF_LOCK: (EDC + ", week-12 efficacy dataset", "2026-07-14"),
    K.EFF_TOP: (CVN + ", topline efficacy extract of 2 June 2026 (site endoscopy reads)", "2026-06-02"),
    K.LAB: ("Meridian Central Laboratory, CVN2184-UC-201 albumin and C-reactive protein results", "2026-07-08"),
    K.ENDO: (EDC + ", endoscopy reads with central reading and adjudication", "2026-07-14"),
    K.ADA: ("Brightwater Bioanalytics, anti-dovikizumab antibody results by analytical run", "2026-07-10"),
    K.ADA_RUNS: ("Brightwater Bioanalytics, immunogenicity assay run log", "2026-07-10"),
    K.DEVICES: ("Tidepath Clinical Outcomes, e-diary handset dispensing log for CVN2184-UC-201", "2026-07-13"),
    K.DIARY: ("Tidepath Clinical Outcomes, e-diary entries for CVN2184-UC-201", "2026-07-13"),
    K.AE: (EDC + ", adverse event records", "2026-07-14"),
    K.CONMED: (EDC + ", concomitant medications", "2026-07-14"),
    K.CHARTER: (CVN + ", phase 3 dose-selection charter CVN-CP-0142 version 1.0", "2026-06-09"),
    K.SAP: (CVN + ", CVN2184-UC-201 statistical analysis plan version 2.0, section 6", "2026-04-02"),
    K.IB: (CVN + ", dovikizumab investigator's brochure edition 6, section 5", "2026-01-15"),
    K.PHASE1: (CVN + ", CVN2184-HV-101 pharmacokinetic summary tables", "2024-03-18"),
}
DISTRACTORS = ["target/" + K.PHASE1, "target/" + K.CONMED, "target/" + K.EFF_TOP]


def main():
    files = []
    for n in sorted(os.listdir(T)):
        src, date = SOURCES[n]
        rows = None
        if n.endswith(".csv"):
            rows = sum(1 for _ in open(os.path.join(T, n), "rb")) - 1
        files.append(dict(file=n, source=src + SYN, date=date, license=LIC, rows=rows))
    meta = dict(task="task171", title="Dovikizumab's phase 3 induction dose for ulcerative colitis from the CVN2184-UC-201 "
                                      "exposure-response",
                setting="A fictional biopharmaceutical company's phase 2b trial of an anti-IL-23 antibody in ulcerative "
                        "colitis (600 mg or placebo), whose dose-selection charter picks the phase 3 induction dose from "
                        "forecast week-12 remission at 300, 600 and 900 mg. The company, its antibody, its vendors and "
                        "its people are fictional, and every record is synthetic.",
                as_of="2026-10-20", deliverables=[K.MEMO, K.TABLES, K.CHART], distractor_files=DISTRACTORS,
                stated_inputs=["the 14 July 2026 database lock", "300, 600 or 900 mg at weeks 0, 4 and 8",
                               "percentages to one decimal place"], files=files)
    assert set(SOURCES) == set(os.listdir(T)), set(SOURCES) ^ set(os.listdir(T))
    json.dump(meta, open(os.path.join(TASK, "metadata.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
