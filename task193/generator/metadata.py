"""metadata.json: what the pack is, and which files are not needed for the answer."""
import json
import os

import world as W


def write(tgt, counts):
    out = {
        "task": "task193",
        "world": {"geography": "Denmark", "currency": "DKK",
                  "organisation": "a national medicines agency",
                  "as_of": W.AS_OF.isoformat(),
                  "decision": "which product and reaction pairs the assessment desk takes forward "
                              "from the quarter to 30 September 2026"},
        "licence": "Synthetic. Every product, licence holder, report and person in this pack is "
                   "invented, and no figure describes a real medicine or a real person. Generated "
                   "for analytical assessment, free to use and redistribute.",
        "source": "generated 2026-10-17 from generator/, seed 193",
        "files": [{"name": n, "rows": r} for n, r in sorted(counts.items())],
        "stated_inputs": {
            "criteria": "the standard's paragraph 3.2: a ratio of %.1f or more, a chi-square of "
                        "%.0f or more, %d or more reports" % (W.PRR_MIN, W.CHI_MIN, W.N_MIN),
            "window": "1 July to 30 September 2026 on receipt date, the standard's paragraph 2.1",
            "capacity": "%d assessments, the capacity report" % W.CAPACITY,
            "triage": W.TRIAGE.isoformat()},
        "distractors": [
            {"file": "literature_screening_log.csv",
             "why": "the division's literature screening for the same quarter. It is real work and "
                    "would matter to a signal from the literature, but the run in question reads "
                    "spontaneous reports only and no figure in the answer touches it."},
            {"file": "enquiry_log.csv",
             "why": "the agency's enquiry line for the quarter. Plausible context for how much the "
                    "division heard from the public, and used by no figure."},
            {"file": "campaign_vaccination_log.csv",
             "why": "doses administered by week and region. It explains why the quarter looks as it "
                    "does and is worth weighing, but no answer divides by it: the run is on reports, "
                    "not on rates per dose."}],
        "wrong_basis_distractor": None,
        "notes": "Three formats besides csv: the standard and the capacity report are PDFs, the "
                 "data agreement schedule is a workbook, the extract manifest is JSON."}
    p = os.path.join(tgt, "..", "metadata.json")
    with open(os.path.normpath(p), "w") as f:
        json.dump(out, f, indent=1)
        f.write("\n")
