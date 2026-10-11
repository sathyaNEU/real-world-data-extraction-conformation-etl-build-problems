"""Write task182/metadata.json from the built pack."""
import json
import os
import sys

import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    "register": "Kelvale Mine landholder bore register (MG-02 1.2): the 18 landholder bores with their owners, properties, "
                "landholders' names, aquifers, construction and baseline assessments; measuring point history; the "
                "network's reference and mine bores",
    "mg02": "Tarrabool Resources procedure MG-02 Landholder bore assessment and make good, revision 3 (effective 1 March 2026)",
    "notes": "Environment team's notes on the October 2026 network extract (field semantics, loggers, files)",
    "dips": "Monitoring database extract: every manual dip keyed from the field sheets, March 2012 to 6 October 2026",
    "loggers": "Logger download archive: hourly absolute pressure and temperature from the ten network loggers, May 2015 "
               "to the October 2026 downloads, UTC",
    "installs": "Logger installation register: serial, bore, installed and removed (Queensland time), sensor depth below "
                "the measuring point",
    "baro": "Site barometric logger, hourly absolute air pressure, May 2015 to October 2026, UTC",
    "climate": "Gridded climate data for the point nearest the pit: daily rainfall, Morton's areal potential "
               "evapotranspiration and temperature, 1 January 1990 to 30 September 2026",
    "take": "Pit dewatering meters: daily metered volume by source, 4 July 2022 to 30 September 2026",
    "contacts": "Environment team's landholder and community contact log, January to October 2026",
    "quality": "Groundwater quality: field and laboratory results for the network by sampling round, 2012 to 2026",
}


def rows_of(path):
    if path.endswith(".csv"):
        with open(path) as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".parquet"):
        return int(pq.ParquetFile(path).metadata.num_rows)
    return None


def write(target, out_path):
    files = []
    for k, f in B.FILES.items():
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[k], "date": "2026-10-09",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    files.sort(key=lambda x: x["path"])
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task182",
        "title": "Which neighbouring landholders' bores the pit has drawn down past their make-good trigger, when the "
                 "dry seasons lowered every shallow bore and the coal measures were still rising on the wet years",
        "domain": "Physical & Environmental Sciences",
        "subdomain": "environmental monitoring and exceedance (groundwater drawdown at landholder bores around an "
                     "open-cut coal mine in central Queensland)",
        "objective": "Anomaly Detection & Diagnostics",
        "prompt_shape": "11 (before and after with a control): each bore's September 2026 level against its own level "
                        "from the climate alone, 18 bores by four figures, the offers and the complainants",
        "as_of": "2026-10-13",
        "deliverables": ["bore_impact_assessment.xlsx", "make_good_recommendation.docx"],
        "distractor_files": [B.FILES[k] for k in B.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task182/generator/build.py (seeded, deterministic) around a "
                               "fictional open-cut coal mine (Kelvale Mine), its fictional owner (Tarrabool Resources), "
                               "a fictional creek (Mundoora Creek) and fictional properties and pastoral companies in "
                               "central Queensland, with a synthetic climate shaped on the region's seasons; no real "
                               "bore, person, property or mine is depicted.",
                     "date": "2026-10-09", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-11",
        "generator": "task182/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))
