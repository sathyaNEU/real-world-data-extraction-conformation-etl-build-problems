"""metadata.json: the distractors and the portal's keys."""
import json

import world as W


def write(g, path):
    out = {
        "task": "task190",
        "domain": "banking-credit-financial-risk",
        "task_type": "fraud-aml-detection",
        "objective": "anomaly-detection",
        "geography": W.GEO,
        "currency": W.CCY,
        "as_of": W.EXTRACT,
        "window": "%s to %s" % (W.YEAR_LO, W.YEAR_HI),
        "answer": ("%d cash deposits were split below the prescribed transaction threshold in the "
                   "year ended 30 June 2027, the largest segment being %s at %d."
                   % (g["total"], W.SEG_NAME[g["largest"]], g["per_seg"][g["largest"]])),
        "answer_unit": "count of deposits",
        "distractor_files": [
            "prescribed_transaction_extract_preliminary.csv",
            "prescribed_transaction_extract_revised.csv",
            "card_settlement_summary_2027.csv",
        ],
        "distractor_note": ("The two prescribed transaction extracts cover cash at or above the "
                            "threshold, so they hold no deposit the figure counts; the card "
                            "settlement summary is the obvious way to judge whether a cash take "
                            "is plausible and the figure never reads it. Neither is a "
                            "wrong-basis distractor: neither states or ranks anything on the "
                            "decision question."),
        "files": [],
        "licence": "Synthetic records generated for this task; no third party licence attached.",
        "wrong_basis_distractor": None,
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return out
