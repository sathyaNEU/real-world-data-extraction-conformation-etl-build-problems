"""metadata.json: the decision, the deliverables, the distractors, the input gates and the provenance (no method)."""
import os

import make_pack
import params as P


def metadata(tdir):
    files = sorted(os.listdir(tdir))
    rows = {}
    for f in files:
        if f.endswith(".csv"):
            with open(os.path.join(tdir, f), encoding="utf-8") as h:
                rows[f] = sum(1 for _ in h) - 1
    largest = max(rows, key=rows.get)
    return {
        "task": "task133",
        "domain": "Banking, Credit & Financial Risk",
        "client_domain": "banking-credit-financial-risk",
        "subdomain": "stress-testing-capital",
        "objective": "Forecasting & Predictive Modeling",
        "as_of": "2026-10-16",
        "question": ("the stressed credit loss the board-approved ICAAP severe scenario puts on a regional bank's business "
                     "banking book in the stress year to 30 September 2027, in total and by reporting segment, with the "
                     "year's net credit losses and the 2025 risk-grade default back-test"),
        "deliverables": ["orari_icaap_business_stress_2027.xlsx", "board_paper_business_stress_2027.docx"],
        "distractor_files": [
            {"file": "industry_sales_quarterly_south_island_2021Q4-2026Q3.csv",
             "why_relevant": "the recent history of each industry's sales is what a stress scenario's industry paths are usually judged against",
             "why_unused": "the stress applies the scenario the Board approved as it stands, and no graded figure reads the history"},
            {"file": "rural_book_stress_summary_ICAAP_2026.pdf",
             "why_relevant": "the rural book is stressed under the same scenario for the same ICAAP paper",
             "why_unused": "the business banking book's standard scopes the rural book out, and no graded figure includes it"},
            {"file": "business_deposit_balances_2026-09-30.xlsx",
             "why_relevant": "the same customers' deposit balances sit beside their lending in any review of a business relationship",
             "why_unused": "the stress is on lending exposures at default, and no graded figure uses a deposit balance"},
        ],
        "input_gates": {
            "files": len(files),
            "formats": sorted({f.rsplit(".", 1)[1] for f in files}),
            "largest_file": largest,
            "largest_file_rows": rows[largest],
        },
        "files": {f: rows.get(f, "") for f in files},
        "sources": [
            {"files": "all files under target/",
             "origin": "constructed for this task by task133/generator/build.py (seeded and deterministic, seed %d)" % P.SEED,
             "license": "CC BY 4.0 (constructed data)", "date": "2026-11-01"},
            {"files": "ANZSIC 2006 division names and letters",
             "origin": "Australian and New Zealand Standard Industrial Classification 2006, Stats NZ and the ABS",
             "license": "CC BY 4.0", "date": "2006"},
            {"files": "NZBN register layout and entity types",
             "origin": "New Zealand Business Number register public data layout, Ministry of Business, Innovation and Employment",
             "license": "CC BY 4.0", "date": "2026"},
        ],
        "notes": ("Synthetic pack. Orari Bank Limited, every borrower, payer, guarantor and person is invented; New Zealand "
                  "place names, the ANZSIC 2006 divisions and the register's layout are real."),
    }
