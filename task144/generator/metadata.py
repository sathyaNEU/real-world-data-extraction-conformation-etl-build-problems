"""Write task144/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    K.EV25: "Grachtwerk events warehouse star stream, schema v5, for the October 2026 Sluis shortlist and each "
            "repository the spotlight lottery featured (December 2024 to 1 March 2026)",
    K.EV26: "Grachtwerk events warehouse star stream, schema v6 (2 March to 27 September 2026)",
    K.ROLLUP: "Daily external first stars by surface for every repository shortlisted for Sluis",
    K.ACCOUNTS: "Grachtwerk account snapshot at 27 September 2026",
    K.MEMBERS: "Organisation memberships of the shortlisted repositories' owners",
    K.REPOS: "Repositories shortlisted for Sluis, January 2025 to October 2026",
    K.CROSSWALK: "Star surface codes of schema v5 and v6",
    K.LOTTERY: "The growth team's Sluis spotlight lottery log, 2025 and 2026 sheets",
    K.MEMO: "Sluis featuring memo of 15 September 2026",
    K.PW_CAMP: "Postwerk campaign report, April to May 2026",
    K.PW_LINKS: "Postwerk link report by subscriber, April to May 2026",
    K.RM_CAMP: "Relaymark campaign export, June to September 2026",
    K.RM_LINKS: "Relaymark click log, June to September 2026",
    K.NOMS: "October 2026 Sluis nomination form responses",
    K.RENAMES: "Grachtwerk repository renames in 2026",
    K.TRAFFIC: "Page traffic of the October 2026 shortlist by referrer group",
    K.TRENDING: "Grachtwerk daily trending lists for Go, Python, Rust and TypeScript",
}


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8-sig") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".parquet"):
        import pyarrow.parquet as pq
        return pq.ParquetFile(path).metadata.num_rows
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": "2026-09-28",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task144",
        "title": "Which repository on Grachtwerk's October 2026 shortlist gets the Sluis newsletter spotlight, by its "
                 "expected external stars in its first 90 days public if spotlighted",
        "domain": "Product Analytics",
        "client_domain": "Product Analytics",
        "subdomain": "feature-adoption-diffusion-modeling (the stars a newsletter spotlight would bring a new "
                     "repository on a code-hosting platform, forecast with each shortlisted repository's own 90-day "
                     "stars)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "other: one pick of seven with its expected 90-day external stars and the stars the spotlight "
                        "adds, each repository's expected stars if spotlighted, a chart, and two tables (each Sluis "
                        "issue's delivered subscribers and spotlight click-through, April to September 2026; each "
                        "shortlisted repository's nominators and the share outside its organisation)",
        "as_of": "2026-09-30",
        "deliverables": [K.GOLD_BOOK, K.GOLD_CHART],
        "distractor_files": list(K.DISTRACTORS),
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task144/generator/build.py (seeded, deterministic) around "
                               "a fictional Amsterdam code-hosting platform (Grachtwerk B.V.), its developer "
                               "newsletter (Sluis), two fictional email platforms (Postwerk, Relaymark), fictional "
                               "repositories, accounts and people; no real organisation, person or system is "
                               "depicted.",
                     "date": "2026-09-28", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-15",
        "revised": "2026-10-27",
        "generator": "task144/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))
