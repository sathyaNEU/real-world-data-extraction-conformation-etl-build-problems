"""metadata.json in the task folder, outside target/: the distractors by bundle path and the portal's keys."""
import json

import pack as P

DISTRACTORS = [P.FILES["rents"], P.FILES["mortgages"]]


def write(target, path, n):
    meta = {
        "task": "task482",
        "domain": "Survey Research & Official Statistics (census, register and administrative data quality)",
        "client_domain": "Survey Research & Official Statistics",
        "task_type": "census-register-administrative-data-quality",
        "objective": "Data Extraction & Conformation (ETL)",
        "distractor_files": DISTRACTORS,
        "distractor_reasons": {
            P.FILES["rents"]: "registered rents by area in the second quarter of 2026; the designation turns on the "
                              "price of dwellings bought, and rents are a different market",
            P.FILES["mortgages"]: "mortgage drawdowns by area and quarter; a count and value of loans, not of the price "
                                  "of an unchanged dwelling, and it stops at June 2026",
        },
        "stated_inputs": ["8", "13.5"],
        "deliverables": ["bso_area_property_price_change_2026.xlsx"],
        "as_of": "2026-10-15",
        "files": sorted(P.FILES.values()),
        "rows": {P.FILES[k]: v for k, v in sorted(n.items())},
        "sources": {
            "constructed": "every file is constructed for this task by its generator (task482/generator); the nation, "
                           "its statistics office, the areas, the dwellings, the sales and the people are fictional",
            "public_specifications": "the price register's old layout follows the public layout of a national "
                                     "residential property price register; the other layouts are the pack's own, "
                                     "described in its dictionary",
            "licence": "CC0 1.0 (constructed data)",
            "date": "2026-10-15",
        },
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
