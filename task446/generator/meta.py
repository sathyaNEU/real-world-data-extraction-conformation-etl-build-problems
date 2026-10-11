"""Write task446/metadata.json from the cut pack."""
import json
import os
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "..", "target")
DESC = {
    "loan_book_qe_extracts.csv": "Core lending quarter-end extracts, one row per facility per extract, 30 Sep 2025 to 30 Sep 2026",
    "loan_book_cwb_dub_20251231_late.csv": "Core lending extract for the Dublin booking entity at 31 Dec 2025, delivered late",
    "treasury_investment_positions_qe.csv": "Treasury investment book positions by quarter-end, from the custodian feed",
    "ccr_netting_set_exposure_qe.xlsx": "Derivative netting-set mark-to-market by quarter-end close (GBP thousands), with a rerun of the 30 Sep 2026 close",
    "csa_collateral_held_qe.csv": "Collateral held under credit support annexes by quarter-end",
    "treasury_fx_closing_rates.csv": "Treasury closing FX rates at each quarter-end",
    "gleif_lei_records_qe_archive.csv": "GLEIF LEI-CDF 3.1 level 1 records as archived at each quarter-end (reference-data universe)",
    "gleif_relationship_records_qe_archive.csv": "GLEIF RR-CDF 2.1 level 2 relationship records as archived at each quarter-end",
    "gleif_reporting_exceptions_20260930.csv": "GLEIF parent reporting exceptions at 30 Sep 2026",
    "isin_lei_20260930.csv": "GLEIF ISIN-to-LEI relationship file at 30 Sep 2026",
    "house_limit_register_20260930.xlsx": "House limit register by obligor group",
    "credit_committee_agenda_20261104.docx": "Credit committee agenda, 4 Nov 2026, Part B new commitment requests",
    "credit_concentration_policy.pdf": "Credit Concentration Policy v4.2 (obligor groups, exposure measure, house limits)",
    "limit_monitoring_standard_LMS-03.pdf": "LMS-03 limit utilisation projection and new commitments",
    "crdm_field_reference.md": "Credit Risk Data Mart field reference (data dictionary)",
    "crdm_extract_log_20261009.txt": "Quarter-end release log with row counts, sources and the late delivery (provenance)",
    "obligor_ratings_qe.csv": "Internal rating grades by customer and quarter-end",
    "sector_concentration_2026Q3.xlsx": "Portfolio MI sector page, 30 Sep 2026, management basis",
}


def rows(path):
    if path.endswith(".csv"):
        return sum(1 for _ in open(path, encoding="utf-8")) - 1
    if path.endswith(".xlsx"):
        wb = openpyxl.load_workbook(path, read_only=True)
        return sum(ws.max_row for ws in wb.worksheets)
    return None


def main():
    files = []
    for f in sorted(os.listdir(TARGET)):
        p = os.path.join(TARGET, f)
        files.append(dict(path=f, format=f.rsplit(".", 1)[1], bytes=os.path.getsize(p), rows=rows(p),
                          source="Constructed: " + DESC[f], date="2026-10-09",
                          license="CC0-1.0 (original work, constructed for this task)"))
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task446",
        "title": "How much of an acquisitive borrower's term loan the credit committee can approve under its house limit",
        "domain": "Banking, Credit & Financial Risk",
        "subdomain": "other: obligor-group credit concentration and house-limit monitoring",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "01 (ranked list under a cap): six requests ranked by projected utilisation of the house limit, each with its 30 September book split, five quarter-end exposures, projection, utilisation and approvable amount",
        "as_of": "2026-10-09",
        "deliverables": ["limit_check_2026-11-04.xlsx", "projected_utilisation_2026Q4.png"],
        "distractor_files": ["obligor_ratings_qe.csv", "sector_concentration_2026Q3.xlsx"],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task446/generator/make.py (seeded, deterministic) around a fictional UK bank (Calder & Wey Bank plc) and fictional borrowers, on the published GLEIF golden-copy CSV schemas (LEI-CDF 3.1, RR-CDF 2.1, reporting exceptions, ISIN-to-LEI) with valid ISO 17442 LEI and ISO 6166 ISIN check digits; managing LOU identifiers are real LOU LEIs; no real borrower, bank exposure or GLEIF record is depicted",
                     "date": "2026-10-09", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-11",
        "generator": "task446/generator/make.py",
        "files": files,
    }
    with open(os.path.join(HERE, "..", "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")


if __name__ == "__main__":
    main()
