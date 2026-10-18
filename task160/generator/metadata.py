"""Write task160/metadata.json from the built pack: the distractors, the input gates and every shipped file's source,
date and licence."""
import json
import os

import openpyxl

import docs as DOC
import pack as PK

ORIGIN = "Constructed for this task (seeded, deterministic): "
SOURCES = {
    PK.F_LEGACY: "Tri-Region Hospital Cooperative capacity system (legacy), daily member capacity reports, census "
                 "nights 1 July 2021 to 30 June 2024",
    PK.F_DAILY: "Tri-Region Hospital Cooperative capacity system, daily member capacity census, 1 July 2024 to "
                "20 December 2026",
    PK.F_DECL: "Tri-Region Hospital Cooperative capacity system, surge plan declarations, 1 July 2021 to "
               "20 December 2026",
    PK.F_MEMBERS: "Tri-Region Hospital Cooperative pool office, members and keys for the 2026-27 season",
    PK.F_BLOCKS: "Tri-Region Hospital Cooperative pool office, January block orders filed 2021 to 2025",
    PK.F_CRS: "Crestfield Medical Staffing, member shift report for the cooperative's members, 1 November 2025 to "
              "20 December 2026",
    PK.F_ISN25: "Inland Seas Nursing, weekly member shift sheets, winter 2025-26",
    PK.F_ISN26: "Inland Seas Nursing, weekly member shift sheets, winter 2026-27 to the week of 14 December",
    PK.F_WW: "Tri-Region Hospital Cooperative surveillance unit, wastewater results, 6 September 2021 to "
             "17 December 2026",
    PK.F_OUTLOOK: "Tri-Region Hospital Cooperative surveillance unit, respiratory admissions outlook issued "
                  "18 December 2026",
    PK.F_SURVEY: "Tri-Region Hospital Cooperative workforce survey, members' quarterly RN returns, 2025 Q1 to "
                 "2026 Q3",
    PK.F_MANIFEST: "Tri-Region Hospital Cooperative pool office, extract manifest for the 21 December 2026 pull",
    PK.F_DICT: "Tri-Region Hospital Cooperative pool office, data dictionary",
    DOC.F_AGREEMENT: "Tri-Region Hospital Cooperative, winter surge staffing pool agreement 2026-27 (24 September "
                     "2026)",
    DOC.F_REGISTER: "Tri-Region Hospital Cooperative pool office, surge plan register 2026-27 (2 November 2026)",
    DOC.F_RATES: "Tri-Region Hospital Cooperative finance, agency rate schedule 2026-27 (1 October 2026)",
}
DISTRACTORS = list(PK.DISTRACTORS)
TITLE = ("How many agency RN shifts a multi-state hospital cooperative's winter surge pool should block-book for the "
         "four weeks from 4 January 2027, region by region, when this winter's respiratory surge reached the Southeast "
         "in November and Central in December and the North's eight hospitals are new to the pool")


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".xlsx"):
        wb = openpyxl.load_workbook(path, read_only=True)
        n = sum(max((ws.max_row or 1) - 1, 0) for ws in wb.worksheets)
        wb.close()
        return n
    if path.endswith(".json"):
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        return len(d["results"]) if isinstance(d, dict) and "results" in d else None
    return None


def write(task_dir):
    target = os.path.join(task_dir, "target")
    out = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        out.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                    "source": ORIGIN + SOURCES[f], "date": "2026-12-21",
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task160",
        "title": TITLE,
        "domain": "Healthcare Delivery & Health Economics",
        "client_domain": "Healthcare Delivery & Health Economics",
        "house_domain": "healthcare-delivery-health-economics",
        "subdomain": "patient flow, beds and workforce optimization (a hospital cooperative's winter agency nurse pool: "
                     "the January block forecast region by region, each region's respiratory surge timed by its lag "
                     "behind the region it follows, read off the closed winters' capacity census)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "a committed block of agency RN shifts for four weeks, each of last winter's 16 pool hospitals' "
                        "funded shifts and shifts billed to the pool that it did not fund, and a weekly chart of the "
                        "funded shifts labelled with the busiest week's total and the shifts billed to the pool that "
                        "week",
        "as_of": "2026-12-21",
        "deliverables": ["winter_pool_block_jan2027.xlsx", "pool_shifts_winter_2025-26.png"],
        "distractor_files": DISTRACTORS,
        "field_terms": [],
        "stated_inputs": [],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task160/generator/build.py (seeded, deterministic) around "
                               "a fictional multi-state hospital cooperative (Georgia and South Carolina, Tennessee, "
                               "Kentucky and West Virginia, northern Michigan), its 24 member hospitals and two nurse "
                               "staffing agencies, in the layouts of a hospital cooperative's daily capacity "
                               "reporting system before and after a system change, a surge declaration log, agency "
                               "billing and payroll exports, a wastewater surveillance export and the pool's own "
                               "agreement, register and order book; no real organisation's records or person is "
                               "depicted.",
                     "date": "2026-12-21", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-18",
        "generator": "task160/generator/build.py",
        "files": out,
    }
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta
