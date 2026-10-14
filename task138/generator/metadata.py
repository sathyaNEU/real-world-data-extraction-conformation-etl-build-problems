"""Write task138/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    K.WOP_PDF: "Kestrel Bend Irrigation District Water Order Procedure (Resolution 2019-07, revised Resolution 2025-18)",
    K.WOP_TABLES: "The Water Order Procedure's Tables 1 to 5 for the 2027 order (crop coefficients, crops, soil units, "
                  "application efficiency, loss allowances)",
    K.REQUESTS: "Growers' 2027 water requests, every version, from the District's request log",
    K.REGISTER: "Field register (GIS): fields, former field ids, turnouts, laterals, soil units, GIS acres",
    K.ST39: "Daily weather at state agricultural weather network station 39 (Kestrel Bend South), October 1995 to "
            "January 2027, in the network's export layout",
    K.YARD: "Daily weather at the District's yard station, April 2014 to January 2027, logger export",
    K.ORDERS: "Irrigation orders (sets) for the 2023 to 2026 seasons from the District's ordering system",
    K.METER_BOOK: "Riders' turnout meter reads for 2026",
    K.SHOP_LOG: "Meter shop log: the 2026 work orders and the meter inventory",
    K.HEADINGS: "Daily volume at each lateral heading, 2026 season (SCADA daily report)",
    K.WEIRS: "Riders' tail weir sheets, 2026 season",
    K.STRUCTURES: "District Engineer's structures inventory: tail weirs, lateral headings, main canal",
    K.OPS_LOG: "Canal operations log, 2026 season",
    K.DICTIONARY: "Data dictionary for the order working files",
    K.README: "Working-files note: each file, what it is and where it came from",
    K.GROUNDWATER: "Spring and fall depth to groundwater at 24 District monitoring wells, 2016 to 2026",
    K.CROP_REPORT: "The District's 2026 crop survey by field",
    K.NOTICE: "Tolan Valley Water Authority notice of the 2027 initial allocation and water orders (15 December 2026)",
}


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": "2027-02-01",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task138",
        "title": "How much water Kestrel Bend Irrigation District should order from the Tolan Valley Project for 2027",
        "domain": "Physical & Environmental Sciences",
        "subdomain": "hydrology-flood-frequency (a season's irrigation requirement at a 24-in-30 non-exceedance level "
                     "from replayed weather traces through a daily root-zone water balance, at a California irrigation "
                     "district)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "13: the thirty weather-year replays with the order at the 24th smallest (the order in whole "
                        "thousands of acre-feet, the replays chart), and four per-lateral asks on the 2026 season "
                        "(turnout deliveries, the water put in at the heading, the share of it not delivered, the tail "
                        "weir spill)",
        "as_of": "2027-02-01",
        "deliverables": [K.GOLD_BOOK, K.GOLD_CHART],
        "distractor_files": list(K.DISTRACTORS),
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task138/generator/build.py (seeded, deterministic) around "
                               "a fictional California irrigation district (Kestrel Bend Irrigation District), its "
                               "supplying authority (Tolan Valley Water Authority), structures, growers and people; no "
                               "real organisation, person or field is depicted. Soil series names are the county soil "
                               "survey's public series, used descriptively.",
                     "date": "2027-02-01", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-12",
        "revised": "2026-10-14",
        "generator": "task138/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))
