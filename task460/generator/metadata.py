"""Write task460/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W   # noqa: E402

F = W.FILES
SOURCES = {
    F["hourly"]: "the Electricity Data Commission's hourly operating data (Form EDC-H1) for the eight balancing areas "
                 "with a candidate store, 2025",
    F["arrays"]: "the engineering firm's hourly AC output model for each candidate store's designed array on 2025 weather",
    F["plants"]: "the Commission's plant register for the eight areas, data year 2025",
    F["rates"]: "the Commission's published generation and emission rates by balancing area, data year 2025",
    F["rates24"]: "the same publication for data year 2024",
    F["sites"]: "Corvane's candidate store sites with each store's delivery utility and feasibility-study array",
    F["codes"]: "the Commission's balancing area code list",
    F["utilmap"]: "the Commission's table of utilities and the balancing area each serves",
    F["invoices"]: "Corvane accounts payable: every electricity invoice line for the eight stores with service in 2025",
    F["charter"]: "the Capital Committee's 2027 on-site solar pilot siting charter (approved 15 September 2026)",
    F["label"]: "the retail supplier's 2025 power content label",
    F["dict"]: "the energy team's field definitions for the folder",
    F["manifest"]: "the list of the files in the folder, with source, as-of date and terms",
}
DISTRACTORS = [F[k] for k in W.DISTRACTORS]
DELIVERABLES = [W.GOLDEN["memo"], W.GOLDEN["hourly"]]


def rows_of(path):
    if path.endswith((".csv", ".txt")):
        with open(path, encoding="utf-8", errors="replace") as fh:
            return sum(1 for _ in fh) - 1
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
        "task": "task460",
        "architecture": 1,
        "title": "Which of Corvane Home & Garden's eight candidate stores gets its 2027 on-site solar pilot, the store "
                 "whose array would have avoided the most grid carbon dioxide per megawatt-hour it generated in 2025, "
                 "conformed from hourly balancing-area operating data, a plant register, published emission rates, an "
                 "array output model and accounts-payable invoice lines",
        "domain": "Physical & Environmental Sciences",
        "subdomain": "emissions-inventory (the avoided-emissions factor of a grid-connected project: the operating "
                     "margin of the store's balancing area in the hours its array generates, estimated from the hourly "
                     "changes in the area's fossil CO2 and weighted by the array's output)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "01: a ranked list under a cap of one (eight stores, one pilot), with each store's avoided CO2 "
                        "per MWh, the first store left out and its gap, each store's 2025 metered use, the share its "
                        "array would have supplied and the price paid, a chart and the store-by-hour conformed file",
        "as_of": W.PACK_DATE.isoformat(),
        "deliverables": DELIVERABLES,
        "distractor_files": DISTRACTORS,
        "stated_inputs": ["2027", "2025"],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task460/generator/build.py (seeded, deterministic) in the "
                               "layouts of a national hourly balancing-area operating data file, a plant register and "
                               "an annual emission rates publication, a solar array output model and an accounts-payable "
                               "invoice line export; the country, its balancing areas, plants, utilities, supplier, the "
                               "retailer, its stores and people are fictional, as is every code and account number.",
                     "date": W.PACK_DATE.isoformat(), "license": "CC0-1.0 (original work)"}],
        "created": W.PACK_DATE.isoformat(),
        "generator": "task460/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as f:
        json.dump(meta, f, indent=1)
        f.write("\n")
    return meta
