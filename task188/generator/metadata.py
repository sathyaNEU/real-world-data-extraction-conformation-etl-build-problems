"""Write task188/metadata.json from the built pack."""
import json
import os
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    "db": "District field database extract: trap sites, trap-nights, catches by species and sex, pools and RT-PCR "
          "results, 2024 and 2025 seasons and 2026 to 15 August",
    "county": "County public health laboratory's RT-PCR report for the district's week-32 pools",
    "protocol": "District mosquito surveillance and adult control protocol, 2026 season",
    "contract": "Aerial ULV adulticide agreement between the district and its applicator, 2026 season",
    "dictionary": "Field database data dictionary",
    "register": "Trap site register 2026: sites, legacy code crosswalk and the zone sections from 1 May 2026",
    "zonemap": "Treatment zone polygons from 1 May 2026",
    "cases": "County epidemiologist's West Nile virus human case log, 2026",
    "weather": "Daily weather at the regional airport, May to August 2026",
    "birds": "Dead bird reports to the district's hotline, 2026, with test results",
    "flights": "Aerial blocks designated and flown, 2024 to 2026",
    "manifest": "Extract manifest",
}


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".sqlite"):
        con = sqlite3.connect(path)
        n = {t: con.execute("SELECT COUNT(*) FROM %s" % t).fetchone()[0] for (t,) in
             con.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
        con.close()
        return n
    return None


def write(target, out_path):
    files = []
    for k, f in B.FILES.items():
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[k], "date": "2026-08-17",
                      "license": "CC0-1.0 (original work)"})
    files.sort(key=lambda x: x["path"])
    db = [x for x in files if x["format"] == "sqlite"][0]
    meta = {
        "task": "task188",
        "title": "Which of a vector control district's eight treatment zones gets the week's single aerial adulticide "
                 "application, judged by the estimated number of West Nile virus-infected Culex females collected per "
                 "CO2 trap-night, with each zone's locally acquired human cases and CO2 trap-nights run and lost this "
                 "season",
        "domain": "Epidemiology & Public Health",
        "subdomain": "disease surveillance and outbreak anomaly detection (arbovirus surveillance: mosquito trapping, "
                     "pooled RT-PCR testing and the infected-vector index that books adult mosquito control)",
        "objective": "Anomaly Detection & Diagnostics",
        "prompt_shape": "01 (a ranked list under a cap): the zone for the flight with its figure, the runner-up with "
                        "its figure and the infection rate that flips the flight; each zone's locally acquired human "
                        "cases and CO2 trap-nights run and lost; the chart of each zone's cases by week of onset",
        "as_of": "2026-08-17",
        "deliverables": ["aerial_spray_recommendation.pdf", "zone_season_2026.xlsx", "human_cases_by_zone.png"],
        "distractor_files": [B.FILES[k] for k in B.DISTRACTORS],
        "field_terms": ["trap"],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": db["path"], "largest_table_rows": max(db["rows"].values())},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task188/generator/build.py (seeded, deterministic) around "
                               "a fictional vector control district, county, health department, laboratory and "
                               "applicator; no real organisation, place, person or record is depicted.",
                     "date": "2026-08-17", "license": "CC0-1.0 (original work)"}],
        "created": "2026-08-17",
        "generator": "task188/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))
