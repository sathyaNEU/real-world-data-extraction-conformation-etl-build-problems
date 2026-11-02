"""metadata.json: the task's identity, its files, the distractors, the input gates, the sources and each shipped file's
provenance (its source, date, what it covers and its rows; no file under target/ lists or describes the others)."""
import json
import os

import pyarrow.parquet as pq

import docs as DC
import world as W

F = W.FILES
DISTRACTORS = [F[k] for k in W.DISTRACTORS]
DELIVERABLES = [W.GOLDEN["return"], W.GOLDEN["note"]]


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".parquet"):
        return pq.ParquetFile(path).metadata.num_rows
    if path.endswith(".xlsx"):
        from openpyxl import load_workbook
        return load_workbook(path, read_only=True).active.max_row - 1
    return None


def write(target, out_path, counts=None):
    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    rows = {f: rows_of(os.path.join(target, f)) for f in files}
    big = max((f for f in files if rows[f] is not None), key=lambda f: rows[f])
    meta = {
        "task": "task467",
        "architecture": 2,
        "title": "How much Wrenfield & Holt must pay into its customer goodwill fund under its written assurance to "
                 "Calvermoor Trading Standards for refunds made late in January to June 2026 and which months broke its "
                 "95 per cent commitment; with each month's refunds, late refunds, late share and goodwill vouchers in "
                 "pounds, and the refund-delay vouchers by product category",
        "domain": "General Statistics & Data Science",
        "subdomain": "data-integration-record-linkage-entity-resolution (an online retailer's refund timeliness return "
                     "to Trading Standards, conformed from its operations, finance and customer service systems)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "08: a rule replayed on history: each month's refunds made, refunds made late, late share and "
                        "whether the month met the commitment, January to June 2026, beside the payment and the breach "
                        "months, each month's goodwill vouchers in pounds and the refund-delay vouchers by product category",
        "as_of": W.AS_OF,
        "deliverables": DELIVERABLES,
        "distractor_files": DISTRACTORS,
        "stated_inputs": ["January to June 2026", "30 November", "14 days", "95 per cent"],
        "input_gates": {"files": len(files), "formats": fmts, "largest_file": big, "largest_file_rows": rows[big]},
        "sources": [
            {"files": "all files under target/",
             "origin": "constructed for this task by task467/generator/build.py (seeded, deterministic) in the layouts of "
                       "a UK online retailer's returns centre goods-in and processing systems, its finance system's refund "
                       "ledger, order system, customer case and goodwill voucher systems and e-commerce redemption "
                       "records, a county council Trading Standards written assurance, and the centre's review, daily "
                       "sheet and rota; the retailer, its centre, the council, the trust, the carriers and the people are "
                       "fictional; the 14-day refund period follows the Consumer Contracts (Information, Cancellation and "
                       "Additional Charges) Regulations 2013, regulation 34",
             "date": W.AS_OF,
             "license": "original work for this task; no third-party data"}],
        "provenance": [{"file": W.FILES[k], "source": src, "date": d, "covers": desc, "rows": rows[W.FILES[k]]}
                       for k, src, d, desc in DC.PROVENANCE],
    }
    assert sorted(r["file"] for r in meta["provenance"]) == files, "every shipped file has one provenance row"
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta
