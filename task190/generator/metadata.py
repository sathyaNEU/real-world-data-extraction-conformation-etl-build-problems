"""metadata.json: the committed answer, the declared distractors and the file licences."""
import csv
import json
import os

import world as W

# one line per shipped file: what the authority's own system it came from, in the manifest's words
SOURCE = {
    "capital_payment_lines_2026.csv":
        "Constructed: the payment ledger's capital programme payment lines, year to 31 December 2026",
    "capital_payment_lines_2025.csv":
        "Constructed: the payment ledger's capital programme payment lines, year to 31 December 2025",
    "internal_audit_testing_schedule_2026.pdf":
        "Constructed: internal audit's testing schedule for the year to 31 December 2026, the tested "
        "lines as a table inside the working paper",
    "testing_schedule_extract_2025_2026.csv":
        "Constructed: internal audit's two-year extract of the testing schedules, 2025 and 2026",
    "capital_programme_register.csv":
        "Constructed: the capital programme board's register of work programmes, values in thousands",
    "supplier_master.xlsx":
        "Constructed: procurement's supplier master at the extract date",
    "supplier_number_crosswalk.csv":
        "Constructed: finance systems' crosswalk from the ledger's supplier numbers to the master's",
    "payment_run_log_2026.csv":
        "Constructed: finance operations' payment run log, year to 31 December 2026",
    "payment_release_cutoff_register.xlsx":
        "Constructed: finance operations' payment release cut-off register with its effective dates",
    "supplier_risk_approval_history.csv":
        "Constructed: procurement's supplier risk approval history, year to 31 December 2026",
    "supplier_risk_category_map.csv":
        "Constructed: procurement's risk category labelling map, from 1 October 2026",
    "audit_plan_2026.pdf":
        "Constructed: internal audit plan 2026, section 4",
    "audit_manual_part9.pdf":
        "Constructed: internal audit manual, part 9",
    "grant_claim_2026.csv":
        "Constructed: finance's funder grant claim for the claim year to 31 March",
    "revenue_expenditure_summary_2026.csv":
        "Constructed: finance's revenue expenditure summary, year to 31 December 2026",
    "field_dictionary.csv":
        "Constructed: finance systems' field definitions across the extracts",
    "provenance.md":
        "Constructed: internal audit's extract notes for this cut",
    "export_manifest.csv":
        "Constructed: internal audit's manifest of this cut",
}
LICENSE = "CC0-1.0 (original work, constructed for this task)"


def _rows(path):
    """The data rows in a csv, or None for a file whose rows are not a table."""
    if not path.endswith(".csv"):
        return None
    with open(path, newline="", encoding="utf-8") as fh:
        return max(0, sum(1 for _ in csv.reader(fh)) - 1)


def file_records(target):
    out = []
    for name in sorted(os.listdir(target)):
        p = os.path.join(target, name)
        out.append({"path": name, "format": name.rsplit(".", 1)[-1],
                    "bytes": os.path.getsize(p), "rows": _rows(p),
                    "source": SOURCE[name], "date": W.LEDGER_EXTRACT, "license": LICENSE})
    return out


def write(g, path, target=None):
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
        "files": file_records(target or os.path.join(os.path.dirname(path), "target")),
        "distractor_files": ["grant_claim_2026.csv", "capital_payment_lines_2025.csv"],
        "distractor_note": ("The funder's grant claim covers a claim year to 31 March and a "
                            "share of eligible expenditure, so it holds no payment line the "
                            "figure counts and reconciles to nothing on the decision question. "
                            "The prior year's payment lines ship because the two-year testing "
                            "extract needs them, and the prior year's own misstatement is stated "
                            "nowhere. Neither states or ranks anything on the decision question. "
                            "The revenue expenditure summary is NOT a distractor: a payment run "
                            "pays the whole authority and the capital extract holds only its "
                            "capital part, so the summary is the control the run log's excess "
                            "ties to month by month, and one of the supplemental asks reads it."),
        "wrong_basis_distractor": None,
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return out
