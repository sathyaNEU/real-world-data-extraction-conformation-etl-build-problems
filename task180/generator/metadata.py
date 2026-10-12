"""Write task180/metadata.json from the built pack."""
import json
import os
import sys

import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    "cat": "Reviewed seismic catalogue of the survey's induced-seismicity networks, January 2023 to September 2026",
    "auto": "Origin table of the survey's event database (real-time system and analysts' review origins), same period",
    "hourly": "Hourly injection telemetry of each injection well (rate, wellhead pressure, temperature), same period",
    "reports": "Operators' monthly metered volume reports as received by the data office, 2023 to 2026",
    "inventory": "Station inventory (StationXML) of the plant networks and two regional stations, exported 12 October 2026",
    "gaps": "Data gaps of 60 s or more per station channel, 1 January to 30 September 2026",
    "visits": "Field crew visit sheet, 2026",
    "plant_reg": "Register of the five plants under seismic monitoring",
    "well_reg": "Well register with surveyed open-hole sections",
    "federal": "Federal agency's regional catalogue, magnitude 2.0 and over, 2023 to 2026",
    "gw": "Shallow groundwater monitoring at the plants, monthly, January 2025 to September 2026",
    "scheme": "Mining authority's traffic-light scheme for deep geothermal plants (2024)",
    "ordinance": "State ordinance on the seismological monitoring of deep geothermal projects (2026), unofficial English text",
    "bulletin": "Survey's traffic-light bulletin for the third quarter of 2026",
    "plans": "Mining authority's summary of the operators' 2027 operating plans",
    "notes": "Data office's extract notes",
}


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".parquet"):
        return int(pq.ParquetFile(path).metadata.num_rows)
    return None


def write(target, out_path):
    files = []
    for k, f in B.FILES.items():
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[k], "date": "2026-10-12",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    files.sort(key=lambda x: x["path"])
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task180",
        "title": "Which geothermal plants the 2027 borehole networks will put over the traffic-light amber, and in which "
                 "quarters, with each plant's 2026 injected volume, automatic-system count and network downtime",
        "domain": "Physical & Environmental Sciences",
        "subdomain": "environmental monitoring and exceedance (induced seismicity at deep geothermal plants against a "
                     "mining authority's traffic-light scheme)",
        "objective": "Anomaly Detection & Diagnostics",
        "prompt_shape": "07 (grid of cells): every plant's expected count in every quarter of 2027 against amber, with "
                        "every plant's injected volume, automatic-system count and hours under four stations for each "
                        "quarter of 2026 to date",
        "as_of": "2026-10-12",
        "deliverables": ["amber_outlook_2027.docx", "tls_annex_2026.xlsx"],
        "distractor_files": [B.FILES[k] for k in B.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task180/generator/build.py (seeded, deterministic) around a "
                               "fictional state geological survey, mining authority, five geothermal plants and their "
                               "operators in the southern Molasse basin; no real plant, operator, station, earthquake or "
                               "person is depicted.",
                     "date": "2026-10-12", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-12",
        "generator": "task180/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))
