"""Write task462/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W   # noqa: E402

F = W.FILES
SOURCES = {
    F["plumes"]: "the survey provider's plume detections for its four basin campaigns of the rating year, each plume's "
                 "origin, rate, wind and nearest facility",
    F["coverage"]: "the survey provider's flight-line coverage: each campaign's lines, the facilities under them, the "
                   "times flown and whether each line was imaged",
    F["releases"]: "the survey provider's 2025 single-blind controlled-release study workbook",
    F["methods"]: "the survey provider's technical note on its instrument, detection, quantification and validation",
    F["standard"]: "the ratings company's low-methane producer rating standard (version 1.1, 2 September 2026)",
    F["sites"]: "the ratings company's register of the rated producers' sites in the basin",
    F["production"]: "the state commission's monthly well production reports for the basin, original and amended",
    F["operators"]: "the state commission's operator list",
    F["gas"]: "the producers' composite gas analyses by field, 2024 and 2026",
    F["flaring"]: "the state commission's monthly flaring and venting reports by lease, original and amended",
    F["leases"]: "the state commission's lease register with each operator's effective date",
    F["basin"]: "the state commission's monthly basin summary of flared and vented gas",
    F["statements"]: "the processing plant's monthly allocation statement lines to its shippers",
    F["stations"]: "the processing plant's meter station list",
    F["heating"]: "the processing plant's monthly heating value by meter station",
    F["ghgrp"]: "the producers' greenhouse gas reports (Subpart W layout) for their basin facilities, 2023 to 2025",
    F["satellite"]: "a satellite product's monthly methane estimates for the basin as a whole",
    F["dict"]: "the ratings team's field definitions for the folder",
    F["manifest"]: "the list of the files in the folder, with source, as-of date and terms",
}
DISTRACTORS = [F[k] for k in W.DISTRACTORS]
DELIVERABLES = [W.GOLDEN["workbook"], W.GOLDEN["plumes"]]


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
        "task": "task462",
        "architecture": 1,
        "title": "Which of the Tollaver Basin's twelve gas producers carry Tarvane Methane Ratings' 2027 low-methane "
                 "rating, a measured methane intensity of 0.20 per cent or less over the rating year to 30 September "
                 "2026, conformed from Talmora Aerial's four campaigns of plume detections and flight coverage, its "
                 "controlled-release study, the site register and the state commission's production reports; with each "
                 "producer's gas delivered to the processing plant and gas flared over the rating year",
        "domain": "Physical & Environmental Sciences",
        "subdomain": "emissions-inventory (a measurement-informed methane inventory of each producer's sites over the "
                     "rating year, from snapshot aerial detections whose chance of detection rises with the plume's "
                     "rate, against the methane its wells produced)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "01: a slate of twelve producers each rated, with each producer's methane emitted and measured "
                        "intensity, its gas delivered to the plant and flared over the rating year, an intensity chart "
                        "against the 0.20 per cent line and the conformed plume file",
        "as_of": W.PACK_DATE.isoformat(),
        "deliverables": DELIVERABLES,
        "distractor_files": DISTRACTORS,
        "stated_inputs": ["twelve", "2027", "0.20", "four"],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task462/generator/build.py (seeded, deterministic) in the "
                               "layouts of an aerial methane survey provider's plume detections, flight coverage, "
                               "controlled-release workbook and methods note, a ratings company's standard and site "
                               "register, a state oil and gas commission's production, operator, flaring, lease and "
                               "basin summary extracts, a processing plant's allocation statements, station list and "
                               "heating values, producers' greenhouse gas reports and gas analyses, and a satellite "
                               "product's basin estimates; the basin, its producers, the plant, the commission's "
                               "records, the provider, the ratings company and the people are fictional.",
                     "date": W.PACK_DATE.isoformat(), "license": "CC0-1.0 (original work)"}],
        "created": W.PACK_DATE.isoformat(),
        "generator": "task462/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as f:
        json.dump(meta, f, indent=1)
        f.write("\n")
    return meta
