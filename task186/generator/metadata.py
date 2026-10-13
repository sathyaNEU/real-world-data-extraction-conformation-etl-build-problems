"""Write task186/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    "log": "Price reporting platform, regular gasoline price changes as received, 1 January 2025 to 15 November 2026",
    "rack": "Port Ostley Terminal published rack prices, regular, premium and ultra-low sulphur diesel",
    "register": "Price reporting platform station table and brand history, exported 16 November 2026",
    "crosswalk": "Price reporting platform station renumbering of 8 June 2026",
    "survey": "Monthly fuel sales survey returns for 2026 reference months to date",
    "frame": "Monthly fuel sales survey frame at November 2026",
    "subs": "Price reporting platform submissions received in November 2026, all grades",
    "brands": "Monitored brand register under the Fuel Price Transparency Act",
    "opslog": "Price reporting platform operations log",
    "bulletin": "Prices Division weekly fuel price bulletin 2026 as published",
    "complaints": "Office of the Fuel Price Commissioner price complaints line, 2026 to date",
    "standard": "Prices Division standard PM-04, levy pass-through monitoring, revision 2",
    "schedule": "Carbon Levy Regulation, Schedule 2, office consolidation",
    "notes": "Fuel Price Monitor extract notes, 16 November 2026",
}


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write(target, out_path):
    files = []
    for k, f in B.FILES.items():
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[k], "date": "2026-11-16",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    files.sort(key=lambda x: x["path"])
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task186",
        "title": "Which brand, if any, the Fuel Price Commissioner's pass-through inquiry should examine before the "
                 "1 January 2027 carbon levy rise, judged on how each brand's stations passed on the 1 January 2026 "
                 "rise, with the share of each brand's stations found, the stations each brand prices itself and the "
                 "regular litres its stations sold in the first quarter of 2026",
        "domain": "Survey Research & Official Statistics (secondary Economics & Econometrics)",
        "subdomain": "anomaly detection (station-level findings of excess levy pass-through held to a false discovery "
                     "rate, where every urban area's retail margins cycle)",
        "objective": "Anomaly Detection & Diagnostics",
        "prompt_shape": "01 (ranked list under a cap): the inquiry capped at one brand or none; every brand's share of "
                        "stations found, its stations priced by the brand on 1 December 2026 and its regular litres in "
                        "each month of the first quarter of 2026; the chart",
        "as_of": "2026-11-16",
        "deliverables": ["pass_through_inquiry_2027.docx", "inquiry_scope_2027.xlsx"],
        "distractor_files": [B.FILES[k] for k in B.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task186/generator/build.py (seeded, deterministic) around a "
                               "fictional province, statistics bureau, fuel price commissioner, fuel brands and stations; "
                               "no real organisation, station, person or record is depicted.",
                     "date": "2026-11-16", "license": "CC0-1.0 (original work)"}],
        "created": "2026-11-16",
        "generator": "task186/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))
