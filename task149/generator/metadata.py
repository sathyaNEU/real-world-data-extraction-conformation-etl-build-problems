"""Write task149/metadata.json from the built pack."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks_records as AR   # noqa: E402
import deliver as DL        # noqa: E402
import distract as DS       # noqa: E402
import docs as DOC          # noqa: E402
import records as R         # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    R.F_LEGACY: "Ostrander Logistics legacy incident database, case export (cases with a date of injury 12/27/2020 to "
                "06/30/2024)",
    R.F_PLATFORM: "Ostrander Logistics EHS platform, full incident case extract from 07/01/2024 with the cases migrated "
                  "at go-live",
    R.F_WFM: "Ostrander Logistics workforce-management system, weekly hours by DC, department and pay code, FY2021 week "
             "1 to FY2026 week 44",
    R.F_WMS: "Ostrander Logistics WMS, weekly cases shipped by location and item category, FY2021 week 1 to FY2026 "
             "week 44",
    R.F_STD: "Ostrander Logistics Industrial Engineering, engineered labor standards (minutes per case) and site "
             "factors",
    R.F_PLAN: "Ostrander Logistics FP&A, FY2027 operating plan v3: cases and labor hours by DC and fiscal period",
    R.F_REG: "Ostrander Logistics DC register as at 11/02/2026",
    R.F_ITA: "Ostrander Logistics Form 300A summaries as submitted to OSHA's Injury Tracking Application, calendar 2021 "
             "to 2025",
    DOC.F_PROC: "Ostrander Logistics EHS procedure EHS-RK-01 rev 7, OSHA injury and illness recordkeeping",
    DOC.F_AGREE: "Ergonomics program services agreement between Ostrander Logistics and Lindqvist Ergonomics Group, "
                 "fiscal 2027, draft for signature",
    DOC.F_NOTES: "Ostrander Logistics Safety Analytics, field notes for the forecast folder",
    DOC.F_MANIFEST: "Ostrander Logistics Safety Analytics, folder manifest",
    AR.F_RTW: "Ostrander Logistics return-to-work program, case management system work-status log, files opened from "
              "12/28/2025",
    AR.F_ITEM: "Ostrander Logistics WMS item master, active items, 11/01/2026",
    AR.F_ITEMH: "Ostrander Logistics WMS item master history, every item version with its effective dates",
    AR.F_PICKS: "Ostrander Logistics WMS pick history summary, the program DCs' cases picked by SKU and fiscal period, "
                "FY2026 period 1 to week 44",
    DS.F_WC: "Workers' compensation third-party administrator, loss run for Ostrander Logistics valued 09/30/2026",
    DS.F_BBS: "Ostrander Logistics safety observation app, behavior-based safety observations FY2025 to FY2026 week 44",
}
DISTRACTORS = [DS.F_WC, DS.F_BBS]


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".parquet"):
        import pyarrow.parquet as pq
        return pq.ParquetFile(path).metadata.num_rows
    if path.endswith(".json"):
        with open(path, encoding="utf-8") as fh:
            return len(json.load(fh)["cases"])
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": "2026-11-02",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task149",
        "title": "How many recordable cases a third-party logistics company's twenty ergonomics program DCs will log in "
                 "fiscal 2027 under an operating plan that works their hours faster against the engineered standards",
        "domain": "Epidemiology & Public Health",
        "client_domain": "Epidemiology & Public Health",
        "subdomain": "health-burden-impact-modeling (the occupational injury burden of a working population under a "
                     "planned shift in its exposure: the recordable rate per hour worked as a function of pace against "
                     "the engineered labor standards, estimated within each DC on person-time, carried to the pace the "
                     "plan sets)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "one forecast figure to the nearest hundred, two tables for the twenty DCs (fiscal 2026 DART "
                        "days to 31 October 2026; cases picked over 50 pounds), and a one-slide chart of the five "
                        "fiscal years' recordable cases beside the forecast",
        "as_of": "2026-11-02",
        "deliverables": [DL.F_BOOK, DL.F_SLIDE],
        "distractor_files": DISTRACTORS,
        "stated_inputs": [],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task149/generator/build.py (seeded, deterministic) around a "
                               "fictional third-party logistics company in Ohio, its distribution centers, its "
                               "ergonomics vendor and their systems; no real organisation, person or system is "
                               "depicted. Form layouts follow 29 CFR Part 1904 and OSHA's Injury Tracking Application "
                               "field names; event codes follow BLS OIICS 2.01.",
                     "date": "2026-11-02", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-16",
        "generator": "task149/generator/build.py",
        "files": files,
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))
