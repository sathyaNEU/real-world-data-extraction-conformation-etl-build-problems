"""Write task162/metadata.json from the built pack: the distractors, the portal's keys, the input gates and every
shipped file's source, date and licence."""
import json
import os

import docs as DOC
import records as R

SOURCES = {
    R.F_INLET: "Lynmere Water telemetry archive, Northern zone inlet loggers (flow and pressure), hourly means in GMT, "
               "1 April 2025 to 31 March 2026",
    R.F_ZONE: "Lynmere Water telemetry archive, Northern zone average zone point loggers, hourly means in GMT, 2025-26",
    R.F_LOGGERS: "Lynmere Water telemetry, logger register for the Northern zone (serials, points, makes, units, dates)",
    R.F_DISTRICTS: "Lynmere Water network records, Northern zone district register",
    R.F_CODES: "Lynmere Water network records, district code history",
    R.F_PROPS: "Lynmere Water property system, North region extract of 2 November 2026",
    R.F_BILLS: "Lynmere Water billing, North region consumption by supply point and bill period, 2025-26 and its edges",
    R.F_OUTLET: "Lynmere Water telemetry, Thornholme service reservoir outlet meter TH-OUT-0417, daily volumes",
    R.F_EXPORT: "Lynmere Water leakage analysis, DMA leakage assessment export for the Phase 3 districts, 14 May 2026",
    R.F_CONTACTS: "Lynmere Water customer contact log, Northern zone, 2025-26",
    R.F_MILL: "Brackenby Paper Mill AMR, hourly flow on its trunk main off-take, 2025-26",
    DOC.F_METHOD: "Lynmere Water leakage analysis, method LW-LA-04 issue 6 (effective 1 April 2025)",
    DOC.F_SCHEDULE: "Leakage Outcome Contract LW/LOC/2024/07, Schedule 4 for Phase 3, Variation 3 (2 September 2026)",
    DOC.F_NOTE: "Lynmere Water contract manager's e-mail on the 2027-28 delivery plan's planning assumptions "
                "(19 October 2026)",
    DOC.F_VALVES: "Coldbeck Network Partners network modelling, Phase 3 pressure reducing valve schedule rev C "
                  "(9 October 2026)",
    DOC.F_CERT: "Fenwold Flow Services, certificate of verification FFS-25-1182 for outlet meter TH-OUT-0417 "
                "(12 November 2025)",
}
DISTRACTORS = [R.F_CONTACTS, R.F_MILL]
TITLE = ("Whether 22 fixed-outlet pressure reducing valves at the far end of a water company's trunk main will cut "
         "the districts' assessed leakage by the contracted reduction in 2027-28, when a paper mill's weekday shifts "
         "take the inlet pressures below the valves' settings for most of the working day, and how many find-and-fix "
         "gang-years must make up any shortfall")


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        n = sum(max(ws.max_row - 1, 0) for ws in wb.worksheets)
        wb.close()
        return n
    return None


def write(task_dir):
    target = os.path.join(task_dir, "target")
    out = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        out.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                    "source": "Constructed: " + SOURCES[f], "date": "2026-11-02",
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task162",
        "title": TITLE,
        "domain": "Energy Systems & Utilities",
        "client_domain": "Energy Systems & Utilities",
        "subdomain": "asset-condition-maintenance (a water network's leakage as the standing condition of its mains, "
                     "assessed district by district from night flows and pressures by FAVAD, and a pressure scheme's "
                     "effect on it forecast before the valves are installed)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "a committed go or hold (whether the phase meets its contracted reduction) with the phase's "
                        "forecast leakage, its reduction, the shortfall and the find-and-fix gang-years, beside a grid "
                        "of the zone's twelve other districts' 2025-26 assessed leakage and the zone's 2025-26 system input, "
                        "billed unmetered consumption and real losses, and a chart of the 22 Phase 3 districts",
        "as_of": "2026-11-02",
        "deliverables": ["phase3_leakage_forecast_2027_28.xlsx", "phase3_leakage_by_district.svg"],
        "distractor_files": DISTRACTORS,
        "field_terms": [],
        "stated_inputs": [],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task162/generator/build.py (seeded, deterministic) around "
                               "a fictional English water company and its pressure management partner, in the layouts "
                               "of a telemetry archive's hourly CSV export, network and property registers, a billing "
                               "extract by supply point, an assessment export workbook, a valve schedule workbook, "
                               "PDF method, contract and certificate documents and an e-mail; no real organisation's "
                               "records or person is depicted.",
                     "date": "2026-11-02", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-28",
        "generator": "task162/generator/build.py",
        "files": out,
    }
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta
