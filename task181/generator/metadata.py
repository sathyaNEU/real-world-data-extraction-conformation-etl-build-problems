"""Write task181/metadata.json from the built pack."""
import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B   # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    "line_list": "State notifiable conditions system: the unit's daily pertussis line-list extract, every notification "
                 "received 1 January 2019 to 07:00 AEDT 5 October 2026, one row per laboratory notification",
    "notes": "Surveillance field notes for the pertussis line list and the linked follow-up files",
    "run_report": "State system run report for the 07:00 extract of 5 October 2026",
    "protocol": "PR-07 Pertussis response protocol, version 3.1 (effective 2 March 2026)",
    "concordance": "The unit's residential postcode to LGA lookup (2021 Census correspondence ratios) and area populations",
    "admissions": "Patient administration system extract: inpatient episodes with a principal respiratory diagnosis at the "
                  "district's hospitals, 1 January 2019 to 4 October 2026",
    "births": "Maternity units' birth records, 1 January 2024 to 30 September 2026",
    "register": "Antenatal vaccination register: vaccines recorded in pregnancy for women in the district since 2019",
    "rosters": "School enrolment rosters received during follow-up in term 3 2026, one sheet per school, names removed",
    "influenza": "State notifiable conditions system: the unit's influenza notifications received in 2026",
    "bulletin": "The unit's communicable diseases weekly report for week 35 (24 to 30 August 2026)",
}


def rows_of(path):
    if path.endswith(".csv"):
        with open(path) as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".parquet"):
        return int(len(pd.read_parquet(path)))
    return None


def write(target, out_path):
    files = []
    for k, f in B.FILES.items():
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[k], "date": "2026-10-05",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    files.sort(key=lambda x: x["path"])
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task181",
        "title": "Which local government area the pertussis response team goes to this week, off a line list whose "
                 "areas reach the unit through laboratories of different speed",
        "domain": "Epidemiology & Public Health",
        "subdomain": "disease surveillance and outbreak anomaly detection (a regional public health unit's pertussis "
                     "notifications across inland New South Wales)",
        "objective": "Anomaly Detection & Diagnostics",
        "prompt_shape": "17 (periods around a change point): each area's 14-day count against its expected count, "
                        "plus the school clusters and a ten-area quarterly table of five measures",
        "as_of": "2026-10-05",
        "deliverables": ["response_team_brief.pptx", "pertussis_cases_by_lga.csv"],
        "distractor_files": [B.FILES[k] for k in B.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task181/generator/build.py (seeded, deterministic) around a "
                               "fictional public health unit (Southern Inland Public Health Unit), a fictional private "
                               "pathology network (Inland Pathology) and fictional schools, with real New South Wales "
                               "local government areas, postcodes, public holidays and ICD-10-AM codes; no real person, "
                               "case, school or laboratory result is depicted.",
                     "date": "2026-10-05", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-11",
        "generator": "task181/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))
