"""Write task140/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    K.STANDARD_PDF: "Cell Capacity Standard CS-3 (revision of June 2026): reservable cores, firm holds, platform "
                    "services, the batch guarantee",
    K.MEMO: "Capacity memo for the C-22 review of 2027 Q1 (9 December 2026)",
    K.HWPLAN: "C-22 hardware plan for 2027 Q1, revision of 11 December 2026: racks and machines in service by date",
    K.REQUESTS: "Firm tenants' reservation requests for 2027 Q1 from the quota tool",
    K.BUDGETS: "Technology compute budgets by cost centre, 2026 and January to March 2027, with the freeze record",
    K.RATECARD: "Compute rate card for MAD1 reserved cores, every rate by effective date",
    K.LEDGER: "C-22 reservation ledger, 2025 Q1 to 2026 Q4",
    K.USAGE: "C-22 monitoring export: each tenant's average cores in use by hour, 1 January 2025 to 13 December 2026",
    K.CELLHOURLY: "C-22 machines installed and in service by hour, same period",
    K.DIRECTORY: "C-22 tenant directory",
    K.CAPREPORT: "C-22 capacity report for 2026 Q3",
    K.OPSLOG: "MAD1 operations log, July to December 2026",
    K.RUNS: "Batch training runs that held cores in 2026 Q3 (batch scheduler quarter snapshot)",
    K.CHECKPOINTS: "Checkpoints of those runs and the checkpoints their resumptions restored",
    K.RESIZES: "Resizes of elastic batch runs in 2026 Q3",
    K.MEVENTS: "C-22 machine events from the MAD1 cluster manager, 2026 Q3",
    K.INVENTORY: "MAD1 hardware inventory for C-22: assets and their cluster ids",
    K.QCHANGES: "Changes to firm reservations in 2026 Q3 from the quota tool",
    K.QRUNS: "Quota service reconciliation runs in 2026 Q3",
    K.CHARGEBACK: "Technology chargeback policy 2026",
    K.DICTIONARY: "Field definitions for the capacity review files",
    K.README: "Files note: each file, what it is and where it came from",
    K.SISTERS: "MAD1 compute cells' quarterly summary, 2025 and 2026",
    K.BATCH_DEMAND: "ML Platform's note on batch training demand for January to June 2027",
}


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": "2026-12-14",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task140",
        "title": "How many cores compute cell C-22 can guarantee to batch training for the first quarter of 2027",
        "domain": "Supply Chain & Logistics",
        "client_domain": "General Statistics & Data Science",
        "subdomain": "regression-classification-model-diagnostics (data-centre capacity planning: a dependent "
                     "platform service's load specified on its drivers and solved together with the residual "
                     "guarantee it depends on)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "other: the guarantee and the reservations it is struck after, the slide's split of the "
                        "reservable cores, and three 2026 Q3 tables (each batch team's redone core-hours and share; "
                        "each month's machine-hours lost by cause; each firm tenant's chargeback)",
        "as_of": "2026-12-14",
        "deliverables": [K.GOLD_BOOK, K.GOLD_DECK],
        "distractor_files": list(K.DISTRACTORS),
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task140/generator/build.py (seeded, deterministic) around "
                               "a fictional Spanish online travel company (Alisio Viajes, S.L.), its MAD1 data centre "
                               "and compute cell C-22, tenants, teams and people; no real organisation, person or "
                               "system is depicted.",
                     "date": "2026-12-14", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-12",
        "generator": "task140/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))
