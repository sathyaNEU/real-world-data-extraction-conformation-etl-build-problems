"""Write task456/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pack as P    # noqa: E402

TASK = os.path.dirname(HERE)
F = P.FILES
SOURCES = {
    F["compact"]: "the Ridgeline ICU Surge Compact among the alliance's member hospitals, effective 1 October 2025",
    F["annex"]: "the compact's data annex, version of 3 November 2025",
    F["regions"]: "every Tennessee county with its surge region (the compact's Annex A)",
    F["crosswalk"]: "the alliance's facility crosswalk of the compact hospitals' keys in each feed",
    F["aliases"]: "the transfer center's list of the facility names its staff type for sending facilities",
    F["codes"]: "the transfer center's decline reason codes",
    F["survey_old"]: "the census survey's export of November 2025 (the survey's earlier form)",
    F["survey_new"]: "the census survey's export of 1 December 2025 to 19 January 2026",
    F["board"]: "the regional bed-status board's event log, 1 November 2025 to 20 January 2026",
    F["tc_old"]: "the transfer center's call log from its earlier call system, to 4 January 2026",
    F["tc_new"]: "the transfer center's call log from its new call system, 5 to 19 January 2026",
    F["dict"]: "the field descriptions of the data files",
    F["manifest"]: "the export manifest of 20 January 2026",
    F["federal"]: "the compact hospitals' federal respiratory reporting extract, weekly, December 2025 to January 2026",
    F["history"]: "the compact's reviews and activations of the 2024-25 season",
}
DISTRACTORS = [F["federal"], F["history"]]
DELIVERABLES = ["surge_activation_notice_2026-01-26.pdf", "hospital_days_conformed_2025-12-22_2026-01-18.csv"]


def rows_of(path):
    if path.endswith((".csv", ".jsonl")):
        with open(path, encoding="utf-8", errors="replace") as fh:
            n = sum(1 for _ in fh)
        return n - 1 if path.endswith(".csv") else n
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": "2026-01-20",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task456",
        "architecture": 1,
        "title": "Which regions a hospital alliance's ICU surge compact activates at its January review, each region's "
                 "share of full adult ICU hospital-days estimated from three conflicting capacity feeds",
        "domain": "General Statistics & Data Science",
        "subdomain": "data-integration-record-linkage-entity-resolution (three feeds that each record full ICU days "
                     "with error conformed into one hospital-day dataset, and each region's share of full days "
                     "estimated as the prevalence of a latent class model of the feeds)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "10: a scorecard of each region's share of full hospital-days against the compact's one in "
                        "three, with a chart, three region-by-region asks and the conformed hospital-day file",
        "as_of": "2026-01-20",
        "deliverables": DELIVERABLES,
        "distractor_files": DISTRACTORS,
        "stated_inputs": [],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task456/generator/build.py (seeded, deterministic) in the "
                               "layouts of a hospital alliance's census survey, a regional bed-status board's event log "
                               "and a transfer center's call exports; the counties, their FIPS codes and their time "
                               "zones are Tennessee's; the alliance, its compact, the transfer center, the hospitals "
                               "and the people are fictional.",
                     "date": "2026-01-20", "license": "CC0-1.0 (original work)"}],
        "created": "2026-01-20",
        "generator": "task456/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
