"""Write task461/metadata.json from the built pack: the decision, the deliverables, the distractors and each file's
provenance; never the method, a link or a graded figure."""
import json
import os

import world as W

F = W.FILES
SOURCES = {
    F["licence"]: "the Authority's environment protection licence conditions for the terminal (variation 4, 3 March 2025)",
    F["protocol"]: "the Authority's return protocol for petroleum products storage and loading premises (2026 edition)",
    F["tas_old"]: "the terminal management system's export of compartment loads, January to June 2026 (legacy system)",
    F["tas_new"]: "the replacement terminal management system's transaction export from its 29 June 2026 go-live",
    F["dockets"]: "the dispatch system's delivery docket lines for the distributor's fleet and its contract carrier",
    F["tankers"]: "the distributor's register of road tanker units (January 2027)",
    F["sites"]: "the dispatch system's list of delivery sites",
    F["vru_cems"]: "the vapour recovery unit's continuous emission monitor export, 15-minute intervals, 2026",
    F["vru_plc"]: "the vapour recovery unit controller's event log",
    F["gauging"]: "the tank gauging system's daily dips",
    F["outturns"]: "the terminal's register of ship receipts from the surveyors' outturn reports, 2026",
    F["shiftlog"]: "the terminal control room's shift log, 2026",
    F["workorders"]: "the maintenance system's work orders raised or closed in 2026",
    F["tankreg"]: "the terminal's register of storage tanks (January 2027)",
    F["weather"]: "daily weather observations at the nearest airport station, 2026",
    F["stacktest"]: "the vapour recovery unit's 2026 annual stack emission survey",
}
PACK_DATE = "2027-01-08"


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8", errors="replace") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write(target, out_path, n=None):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        rows = rows_of(p)
        if rows is None and n:
            key = [k for k, v in F.items() if v == f]
            rows = n.get(key[0]) if key else None
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows,
                      "source": "Constructed: " + SOURCES[f], "date": PACK_DATE,
                      "license": "CC0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task461",
        "architecture": 2,
        "title": "How much VOC Brennock Fuels' Warrenby terminal released from product loading in 2026, and whether "
                 "it kept within its licence's loading limit, for the annual return to the Coastal Air Quality "
                 "Authority, with each storage tank's release and the terminal's quarterly stock account",
        "domain": "Physical & Environmental Sciences",
        "subdomain": "emissions-inventory",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "other: the return file's release at each loading point in each quarter and each storage "
                        "tank's release over the year, a covering note with the year's release against the limit and "
                        "a monthly chart, and a stock account of each tank's gain or loss in each quarter",
        "as_of": PACK_DATE,
        "deliverables": [W.GOLDEN["return"], W.GOLDEN["note"], W.GOLDEN["stock"]],
        "distractor_files": [F[k] for k in W.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task461/generator/build.py (seeded, deterministic) in the "
                               "layouts of a fuel terminal's management system exports, a dispatch system's delivery "
                               "dockets, tanker and tank registers, a vapour recovery unit's monitor and controller "
                               "logs, tank gauging, ship outturns, a control room shift log, maintenance work orders, "
                               "airport weather and a regulator's licence and return protocol; the distributor, the "
                               "terminal, the carrier, the partner terminal, the regulator, the city, every site and "
                               "the people are fictional.",
                     "date": PACK_DATE, "license": "CC0 (original work)"}],
        "created": PACK_DATE,
        "generator": "task461/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as f:
        json.dump(meta, f, indent=1)
        f.write("\n")
    return meta
