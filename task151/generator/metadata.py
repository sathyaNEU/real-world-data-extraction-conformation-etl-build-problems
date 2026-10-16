"""Write task151/metadata.json from the built pack."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import deliver as DL        # noqa: E402
import docs as DOC          # noqa: E402
import records as R         # noqa: E402

TASK = os.path.dirname(HERE)
ASOF = "2026-12-11"
SOURCES = {
    R.F_LEGACY: "League Statistics Feed (fictional league), box-score batting lines 2021 to 2024, legacy layout "
                "(pipe-delimited archive export)",
    R.F_BAT: "League Statistics Feed (fictional league), box-score batting lines 2025 and 2026, platform layout",
    R.F_XWALK: "League Statistics Feed, legacy player code to League player ID crosswalk built at the 2025 platform "
               "change",
    R.F_CLUBS: "League Statistics Feed, club directory (platform team IDs, abbreviations, legacy codes)",
    R.F_CAL: "League Statistics Feed, championship-season calendar 2021 to 2027",
    R.F_TRANS: "League Statistics Feed, transaction wire January 1, 2024 to December 11, 2026 (JSON export)",
    R.F_ILREP: "League office, weekly injured-list report, championship seasons 2024 to 2026",
    R.F_SCHED27: "League office, 2027 championship-season schedule as published",
    R.F_DC: "Harlan Voss Baseball Data (fictional vendor), projected depth charts, January 31 snapshots 2021 to 2026",
    R.F_PROJ: "Harlan Voss Baseball Data (fictional vendor), preseason hitter projections 2022 to 2027",
    R.F_DC27: "Raleigh Oaks Baseball Operations, 2027 depth chart as of December 10, 2026",
    R.F_REG: "Raleigh Oaks Finance and Baseball Operations, player contract register extract, 2024 to 2026 seasons",
    R.F_PAY: "Raleigh Oaks HRIS payroll, player earnings register, pay dates January 2023 to December 11, 2026",
    R.F_HRIS: "Raleigh Oaks HRIS, legacy employee number map from the January 2025 migration",
    R.F_CODES: "Raleigh Oaks HRIS payroll, earning codes (legacy payroll and HRIS)",
    DOC.F_FIN14: "Triangle Baseball Club, LLC Finance Department, Accounting Policy FIN-14 Player Compensation "
                 "(effective January 1, 2025)",
    DOC.F_TERMS: "Raleigh Oaks Baseball Operations, summary of terms of the five free-agent hitters signed for 2027",
    DOC.F_ILRULES: "League office, League Rules (2024 edition) Article 22 Injured Lists, excerpt",
    DOC.F_NOTES: "League Statistics, field notes for the batting lines, crosswalk, club directory and calendar",
    DOC.F_MANIFEST: "Raleigh Oaks Finance, manifest of the December 11, 2026 pull",
}
DISTRACTORS = [R.F_PROJ, R.F_SCHED27]


def rows_of(path):
    if path.endswith(".csv") or path.endswith(".txt") and "batting" in path:
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".json"):
        return json.load(open(path, encoding="utf-8")).get("count")
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": ASOF,
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task151",
        "title": "How much a baseball club accrues at signing for the plate-appearance bonuses in five free-agent "
                 "hitters' 2027 contracts, each bonus at its expected amount for the 2027 season",
        "domain": "General Statistics & Data Science",
        "client_domain": "General Statistics & Data Science",
        "subdomain": "resampling-simulation-monte-carlo-methods (the expected value of stepped plate-appearance "
                     "bonuses from the distribution of comparable whole seasons: the winter-planned regulars' seasons "
                     "of starts, each read at the signing's 2027 lineup slot's plate appearances per start)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "a total accrual built from five players' accruals (fifteen bonus lines), a table of nine "
                        "injured-list stints (date taken effect and regular-season days), a table of the "
                        "plate-appearance bonuses paid for three seasons by player and in total, and a one-page memo",
        "as_of": ASOF,
        "deliverables": [DL.F_BOOK, DL.F_MEMO],
        "distractor_files": DISTRACTORS,
        "stated_inputs": [],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{
            "files": "all files under target/",
            "origin": "constructed for this task by task151/generator/build.py (seeded, deterministic) around a "
                      "fictional 30-club professional baseball league, its clubs (the Raleigh Oaks among them), its "
                      "statistics feed and league office, a fictional projection vendor and the club's own finance, "
                      "payroll and baseball operations systems; no real league, club, player, vendor or person is "
                      "depicted. Box-score conventions (plate-appearance components, lineup slots, doubleheader and "
                      "suspended-game numbering) and injured-list mechanics follow common professional baseball "
                      "practice.",
            "date": ASOF,
            "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-16",
        "generator": "task151/generator/build.py",
        "files": files,
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta
