"""metadata.json for task199 (architecture 2): provenance per file, the distractors and the deliverables.

It names the decision and the files; it never describes the method or the data's structure.
"""
import json
import os

COVERS = {
    "tawi_core_legacy_stmt_2025-10_2026-03.csv": "Core banking statement lines for the EDD register customers' accounts, October 2025 to March 2026, legacy core system layout",
    "tawi_t24_stmt_2026-04_2026-09.csv": "Statement entries for the same accounts from the T24 core, April to September 2026",
    "t24_transaction_codes.csv": "T24 transaction code table",
    "t24_account_conversion_20260401.csv": "Account conversion table from the T24 go-live on 1 April 2026",
    "swift_mt103_outward_fy2026.txt": "Outward MT103 payment messages from the register customers' accounts, review year",
    "swift_mt103_inward_fy2026.txt": "Inward MT103 payment messages to the register customers' accounts, review year",
    "cbk_indicative_rates_2025-09_2026-10.csv": "Daily indicative exchange rates (mean, buy, sell) in the Central Bank of Kenya layout",
    "customer_master_extract_20261016.csv": "Customer master extract for the register customers",
    "edd_register_profiles_2026.xlsx": "EDD register and customer profiles as refreshed at the last review",
    "FCC-07_EDD_annual_review_rev4.pdf": "Financial Crime Compliance procedure FCC-07, revision 4",
    "teller_cash_txn_2025-10_2026-09.csv": "Teller system cash transactions on the register customers' accounts, review year",
    "kra_gateway_payments_2025-09_2026-10.csv": "KRA payment gateway submissions by the register customers",
    "bulk_salary_uploads_2026-07_2026-10.csv": "Salary upload service batches by the register customers, July to October 2026",
    "screening_alerts_fy2026.csv": "Name-screening alerts on payment counterparties, review year",
    "tawi_tariff_business_2026.pdf": "Tariff guide for business accounts, 2026",
}

DISTRACTORS = ["target/screening_alerts_fy2026.csv", "target/tawi_tariff_business_2026.pdf"]


def write(target, path, rows=None):
    files = []
    for fn in sorted(os.listdir(target)):
        files.append({
            "path": "target/" + fn,
            "covers": COVERS.get(fn, ""),
            "source": "Synthetic. Generated for this task by a seeded script; Tawi Bank Limited, its customers, "
                      "counterparties and people are fictional. No real bank, company or person is represented.",
            "date": "2026-10-16",
            "licence": "CC0 1.0 (synthetic data released into the public domain)",
            "rows": (rows or {}).get(fn),
        })
    meta = {
        "task": "task199",
        "title": "EDD annual review referral, Tawi Bank Limited",
        "domain": "Banking, Credit & Financial Risk",
        "analytical_objective": "Anomaly Detection & Diagnostics",
        "decision": "Which customer on the EDD register the review refers to the Financial Investigations Unit this "
                    "cycle, with its third-party receipts against its expected annual turnover",
        "deliverables": ["edd_referral_2026.docx", "edd_review_2026.xlsx"],
        "as_of": "2026-10-16",
        "distractor_files": DISTRACTORS,
        "files": files,
    }
    with open(path, "w") as f:
        json.dump(meta, f, indent=1)
        f.write("\n")
