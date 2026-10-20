"""metadata.json in the task folder, outside target/: the distractors by bundle path and the portal's keys."""
import json

import pack as P

DISTRACTORS = [P.FILES["irs22"], P.FILES["rel_rev"]]


def write(target, path, n):
    meta = {
        "task": "task475",
        "domain": "Demographic & Social Science (income and poverty statistics from tax returns)",
        "client_domain": "Survey Research & Official Statistics",
        "task_type": "census-register-administrative-data-quality",
        "objective": "Data Extraction & Conformation (ETL)",
        "distractor_files": DISTRACTORS,
        "distractor_reasons": {
            P.FILES["irs22"]: "the tax year 2022 statistics, kept from the 2026 allocation; the policy counts the "
                              "latest year the IRS has published at the plan date, tax year 2023",
            P.FILES["rel_rev"]: "the same address counts from county to ZIP code; the policy shares each ZIP code's "
                                "returns among counties, which only the ZIP code to county file gives",
        },
        "deliverables": ["corran_valley_2027_weatherization_allocation.xlsx",
                         "corran_valley_ty2023_county_credit_families.csv"],
        "as_of": "2026-10-02",
        "files": sorted(P.FILES.values()),
        "rows": {P.FILES[k]: v for k, v in sorted(n.items())},
        "sources": {
            "constructed": "every file is constructed for this task by its generator (task475/generator); the "
                           "council, its counties, agencies, people, ZIP codes and records are fictional",
            "public_specifications": "the IRS Statistics of Income individual ZIP code data layout and field names "
                                     "(N1, A00100, N59660, A59660, AGI_STUB) and the earned income credit parameters "
                                     "for tax years 2022 and 2023 (Rev. Proc. 2021-45 and 2022-38), U.S. government "
                                     "works in the public domain",
            "licence": "CC0 1.0 (constructed data)",
            "date": "2026-10-02",
        },
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
