"""Write task463/metadata.json from the built pack."""
import json
import os
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W   # noqa: E402

F = W.FILES
SOURCES = {
    F["wrenfold"]: "a supermarket group's weekly sales extract by product, all stores",
    F["gorsedale"]: "a co-operative's sales by fiscal year, period and week, by product",
    F["calendar"]: "the co-operative's fiscal calendar",
    F["calderby"]: "a supermarket's point-of-sale database extract: daily sales by store and SKU, its SKU table and stores",
    F["classes"]: "the statistics office's classification of the supermarkets' product lines to RPI items",
    F["published"]: "the statistics office's published RPI item indices and 12-month rates",
    F["plan"]: "the statistics office's plan for introducing supermarket transaction data into the RPI",
    F["dict"]: "the prices team's field definitions for the folder",
    F["deliveries"]: "the statistics office's log of the files received from the supermarkets",
    F["quotes"]: "the RPI field collection's price quotes for the sixteen items",
    F["returns"]: "the supermarkets' annual returns of 2025 retail sales",
    F["catmap"]: "the statistics office's map of the supermarkets' categories to RPI items",
    F["spending"]: "the statistics office's estimate of households' 2025 spending by RPI item",
    F["rsi"]: "the statistics office's monthly retail sales index",
    F["manifest"]: "the programme's register of the files in the folder: owner, period covered, version date, records and "
                   "handling",
}
DISTRACTORS = [F[k] for k in W.DISTRACTORS]
DELIVERABLES = [W.GOLDEN["workbook"], W.GOLDEN["chart"], W.GOLDEN["products"]]


def rows_of(path):
    if path.endswith((".csv", ".txt")):
        with open(path, encoding="utf-8", errors="replace") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".sqlite"):
        con = sqlite3.connect(path)
        n = con.execute("SELECT COUNT(*) FROM daily_sales").fetchone()[0]
        con.close()
        return n
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": W.PACK_DATE.isoformat(),
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task463",
        "architecture": 1,
        "title": "Which of the sixteen grocery and household items in the Kellesay Retail Prices Index move from "
                 "shelf-price collection to the three supermarkets' transaction data in the January 2027 index, an item "
                 "moving when its 12-month rate to September 2026 from the transaction data is within 1.5 points of its "
                 "published rate; with each supermarket's average days to complete monthly records and each item's 2025 "
                 "coverage of household spending",
        "domain": "Survey Research & Official Statistics",
        "subdomain": "seasonal-adjustment-official-time-series-production (official time-series production: a monthly "
                     "retail prices index compiled from supermarket transaction records, conformed into product-months "
                     "and set against the published index over a parallel year)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "10: a scorecard of sixteen items against the 1.5-point line (lines compared, transaction-data "
                        "rate, published rate, difference, move or stay), with each supermarket's timeliness, each item's "
                        "coverage, a chart of each item's two indices and the conformed product-month file",
        "as_of": W.PACK_DATE.isoformat(),
        "deliverables": DELIVERABLES,
        "distractor_files": DISTRACTORS,
        "stated_inputs": ["sixteen", "January 2027", "September 2026", "three"] + list(W.ICODE),
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task463/generator/build.py (seeded, deterministic) in the "
                               "layouts of three supermarkets' sales extracts (a weekly CSV, a fiscal-period text file "
                               "and a point-of-sale SQLite database), a statistics office's product classification, "
                               "published index workbook, introduction plan, data receipt log, field quotes, category map, "
                               "household spending estimates and retail sales index, and the supermarkets' annual "
                               "returns; the island, its statistics office, the supermarkets, their products and the "
                               "people are fictional.",
                     "date": W.PACK_DATE.isoformat(), "license": "CC0-1.0 (original work)"}],
        "created": W.PACK_DATE.isoformat(),
        "generator": "task463/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as f:
        json.dump(meta, f, indent=1)
        f.write("\n")
    return meta
