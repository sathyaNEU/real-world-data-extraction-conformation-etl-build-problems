"""metadata.json: the task's title, tags, deliverables, distractors, input gates and each file's source, date and
license."""
import json
import os

import pack as P

SOURCES = {
    "extract": ("Ellsmere Police Department, Records Division: NIBRS offense extract", "2026-10-05"),
    "dictionary": ("Ellsmere Police Department, Records Division: extract data dictionary", "2026-10-05"),
    "ra_2021": ("Ellsmere Police Department: Return A workbook, 2021", "2022-01-21"),
    "ra_2022": ("Ellsmere Police Department: Return A workbook, 2022", "2023-01-19"),
    "ra_2023": ("Ellsmere Police Department: Return A workbook, 2023", "2024-01-23"),
    "ra_2024": ("Ellsmere Police Department: Return A workbook, 2024", "2025-01-28"),
    "dvu": ("Ellsmere Police Department, Domestic Violence Unit: case log", "2026-10-02"),
    "dvu_notes": ("Ellsmere Police Department, Domestic Violence Unit: case log field notes", "2026-10-02"),
    "method": ("University of Ellsmere Public Safety Lab: scorecard crime chapter methods (draft)", "2026-09-29"),
    "cert": ("State UCR Program: NIBRS certification letter", "2025-01-22"),
    "state_table": ("State UCR Program: Crime in the State 2025, table 8", "2026-09-15"),
    "state_repo": ("State UCR Program: repository download for Ellsmere, assault offenses, incident year 2025, at the "
                   "2025 data freeze", "2026-09-18"),
    "gvr": ("Ellsmere Police Department, Gun Violence Reduction Unit: shooting log", "2026-10-01"),
    "me": ("County Medical Examiner: homicide list", "2026-10-06"),
    "population": ("US Census Bureau-format population estimates for Ellsmere (vintages 2024 and 2025)", "2026-06-26"),
    "cad": ("Ellsmere Police Department: computer-aided dispatch extract, assault-related calls", "2026-01-12"),
}
DISTRACTORS = ["census_population_estimates_ellsmere.csv", "epd_cad_assault_calls_2024_2025.csv",
               "state_repository_download_ellsmere_13A_2025.csv"]


def write(target, path, golden_files, counts):
    files = sorted(os.listdir(target))
    fmts = sorted({os.path.splitext(n)[1].lstrip(".") for n in files})
    big = max(counts, key=lambda k: counts[k])
    meta = {
        "task": "task481",
        "architecture": 1,
        "title": ("By how much Ellsmere's aggravated assaults changed from 2024 to 2025 once 2024 is counted the way "
                  "NIBRS counts it, with the restated 2024 total and the 2025 count, and the non-fatal shooting "
                  "victims and the shootings they were hurt in for each quarter from 2023 to 2025"),
        "domain": "Survey Research & Official Statistics",
        "subdomain": ("seasonal-adjustment-official-time-series-production (a university public safety lab restates a "
                      "city's police-recorded aggravated assault series across the department's move from summary to "
                      "incident-based reporting, from the three months both returns were produced)"),
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "07: a grid of cells, two counts for each of twelve quarters, beside a single restated figure "
                        "and its change",
        "as_of": "2026-10-06",
        "deliverables": golden_files,
        "distractor_files": DISTRACTORS,
        "input_gates": {"files": len(files), "formats": fmts, "largest_file": P.FILES[big],
                        "largest_file_rows": counts[big]},
        "files": [{"file": P.FILES[k], "source": SOURCES[k][0], "date": SOURCES[k][1],
                   "license": "Synthetic data generated for this task; no real records. CC BY 4.0."}
                  for k in P.FILES],
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
