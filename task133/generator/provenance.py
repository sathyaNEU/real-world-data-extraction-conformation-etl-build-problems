"""metadata.json: the decision, the deliverables, the distractors, the input gates and the provenance (no method)."""
import os

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
        "domain": "Urban & Regional Science",
        "client_domain": "urban-regional-science",
        "subdomain": "forecasting",
        "objective": "Forecasting & Predictive Modeling",
        "as_of": "2026-10-20",
        "question": ("the log truck loads a forestry company's FY2028 export harvest plan needs from its forests to its "
                     "export port once the route opens to 50MAX vehicles, by grade, with the cartage paid for FY2026's "
                     "loads by carrier and the FY2026 domestic mill deliveries by quarter"),
        "deliverables": ["matiri_fy2028_log_cartage_loads.xlsx", "fy2028_loads_by_grade.svg"],
        "distractor_files": [
            {"file": "export_log_prices_FY2026.csv",
             "why_relevant": "log prices by grade decide what a forestry company harvests and sends to export",
             "why_unused": "the harvest plan already fixes the FY2028 tonnes, and no graded figure reads a price"},
            {"file": "port_kowhai_vessel_calls_FY2026.csv",
             "why_relevant": "the ships that lift the logs set the port's demand for trucked logs",
             "why_unused": "the loads are sized on the plan's tonnes and the trucks' payloads, and no graded figure uses a vessel call"},
            {"file": "forest_road_closures_FY2026.csv",
             "why_relevant": "days a forest cannot cart shape a haulage roster",
             "why_unused": "the loads needed for a year's tonnes do not depend on the days lost, and no graded figure uses a closure"},
        ],
        "input_gates": {"files": len(files), "formats": sorted({f.rsplit(".", 1)[1] for f in files}),
                        "largest_file": largest, "largest_file_rows": rows[largest]},
        "files": {f: rows.get(f, "") for f in files},
        "sources": [
            {"files": "all files under target/",
             "origin": "constructed for this task by task133/generator/build.py (seeded and deterministic, seed %d)" % P.SEED,
             "license": "CC BY 4.0 (constructed data)", "date": "2026-11-01"},
            {"files": "New Zealand 50MAX and 44-tonne general access limits, JAS log scaling",
             "origin": "New Zealand vehicle dimensions and mass rules (public), the JAS log scaling standard used at New Zealand ports",
             "license": "public reference", "date": "2026"},
        ],
        "notes": ("Synthetic pack. Matiri Forest Products, Port Kowhai, Ruawharo District Council, the carriers, mills and "
                  "people are invented; Hawke's Bay place names and the 50MAX regime are real."),
    }
