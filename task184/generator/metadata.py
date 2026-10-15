"""Write task184/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    "rms": "Records management system offence extract for the Harbourgate streets, 2025 and 2026 seasons, run "
           "22 January 2027",
    "legacy": "Crime information system offence extract for the same streets, 2025 season to 27 July 2025",
    "notes": "Performance and Analysis unit's notes on the extract: scope, the two systems, migration dates, the "
             "class crosswalk and the known differences",
    "dictionary": "Records management system data dictionary for the offence table",
    "rules": "Force extract from the Crime Recording Standard: recording, occurrence date and time, classification "
             "and location",
    "contract": "Harbourgate hotspot patrol tasking agreement for the 2027 season, with the tasking schedule and "
                "the classes covered",
    "schedule": "The week's patrol slots as the tasking agreement lists them",
    "register": "Harbourgate location register: the five registered locations, their street number ranges and beats",
    "gazetteer": "Kelverstoke corporate street gazetteer: the quarter's streets and their alternative spellings",
    "beats": "Kelverstoke neighbourhood beat map",
    "premises": "Harbourgate licensed premises register with terminal hours and capacities",
    "counts": "Business improvement district pedestrian sensor feed, hourly counts in UTC, 2025 and 2026 seasons",
    "availability": "Pedestrian sensor availability log published by the sensor supplier",
    "sensors": "Pedestrian sensor register: location, position, installation date and feed time zone",
    "trading": "Harbourgate trading hours schedule",
    "plan": "Neighbourhood team's record of the hours the patrol worked in each slot under the 2026 agreement",
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
                      "source": "Constructed: " + SOURCES[k], "date": "2027-01-22",
                      "license": "CC0-1.0 (original work)"})
    files.sort(key=lambda x: x["path"])
    biggest = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task184",
        "title": "Which eight of the week's forty-two four-hour patrol slots a city's 2027 Harbourgate hotspot "
                 "patrol covers, and the contracted offences it would meet in each slot of the week, where almost "
                 "every covered offence is recorded with an occurrence window rather than a time",
        "domain": "Criminology & Justice",
        "subdomain": "crime incidence and hotspot analysis (patrol tasking from recorded offences whose occurrence "
                     "time is known only as the window the victim can vouch for)",
        "objective": "Anomaly Detection & Diagnostics",
        "prompt_shape": "07 (a grid of cells): the offences met in each of the week's forty-two day-by-band slots, "
                        "the eight the contract buys read off the grid with their figures and their total, the "
                        "chart of the week, and the volume, location and footfall tables behind the paper",
        "as_of": "2027-01-22",
        "deliverables": ["harbourgate_patrol_slate_2027.pdf", "harbourgate_slot_weights.xlsx"],
        "distractor_files": [B.FILES[k] for k in B.DISTRACTORS],
        "field_terms": ["beat", "slot"],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": biggest["path"], "largest_file_rows": biggest["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task184/generator/build.py (seeded, deterministic) "
                               "around a fictional city, police force, community safety partnership and business "
                               "improvement district; no real organisation, place, person or record is depicted.",
                     "date": "2027-01-22", "license": "CC0-1.0 (original work)"}],
        "created": "2027-01-22",
        "generator": "task184/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))
