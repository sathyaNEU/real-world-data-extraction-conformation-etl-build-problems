"""metadata.json: the committed answer and the declared distractors."""
import json

import world as W


def write(g, path):
    out = {
        "task": "task190",
        "domain": "accounting-audit-forensic",
        "task_type": "audit-testing-sampling",
        "objective": "anomaly-detection",
        "geography": W.GEO,
        "currency": W.CCY,
        "window": "%s to %s" % (W.YEAR_LO, W.YEAR_HI),
        "as_of": W.LEDGER_EXTRACT,
        "answer": ("%s euro of the capital programme payments for the year to 31 December 2026 was "
                   "misstated, which does not meet the conclusion at plan 4.3 and refers the "
                   "population for extended testing; %s carries most of it at %s euro."
                   % (format(g["total"], ","), W.PROG_NAME[g["largest"]],
                      format(g["per"][g["largest"]], ","))),
        "answer_unit": "euro of misstatement",
        "licence": "Synthetic records generated for this task; no third party licence attached.",
        "files": [],
        "distractor_files": ["grant_claim_2026.csv", "revenue_expenditure_summary_2026.csv",
                             "capital_payment_lines_2025.csv"],
        "distractor_note": ("The funder's grant claim covers a claim year to 31 March and a share of "
                            "eligible expenditure, so it holds no payment line the figure counts and "
                            "reconciles to nothing on the decision question. The revenue expenditure "
                            "summary is the other population the plan tests and the figure never "
                            "reads it. The prior year's payment lines ship because the testing "
                            "schedule extract covers two years, and the prior year's own "
                            "misstatement is stated nowhere. None of the three states or ranks "
                            "anything on the decision question."),
        "wrong_basis_distractor": None,
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return out
