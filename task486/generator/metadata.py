"""metadata.json in the task folder, outside target/: the distractors by bundle path and the portal's keys."""
import json

import pack as P

DISTRACTORS = [P.FILES["pit"], P.FILES["hic"]]


def write(path, n):
    meta = {
        "task": "task486",
        "domain": "General Statistics & Data Science (data integration, record linkage and entity resolution)",
        "client_domain": "General Statistics & Data Science",
        "task_type": "data-integration-record-linkage-entity-resolution",
        "objective": "Data Extraction & Conformation (ETL)",
        "distractor_files": DISTRACTORS,
        "distractor_reasons": {
            P.FILES["pit"]: "the region's 2026 point-in-time count by Continuum, people sheltered and unsheltered on the "
                            "night of 28 January 2026; a one-night count, not the FY2026 people served that policy "
                            "RF-2027 section 2 splits the fund on, so no figure reads it",
            P.FILES["hic"]: "the 2026 housing inventory count, each project's beds and units on that night; a capacity "
                            "inventory that no people-served count, night or wait is computed from",
        },
        "wrong_basis_distractors": {
            P.FILES["pit"]: "ranks the Continuums by one night's count; ruled out by RF-2027 section 2, which splits the "
                            "fund in proportion to the people each recipient served in FY2026",
        },
        "stated_inputs": ["policy RF-2027", "FY2026", "2027 Fund", "each quarter of FY2026", "whole dollars",
                          "whole numbers", "one decimal"],
        "deliverables": ["halvering_2027_fund_allocation.xlsx"],
        "as_of": "2026-10-14",
        "files": sorted(P.FILES.values()),
        "rows": {P.FILES[k]: v for k, v in sorted(n.items())},
        "sources": {
            "constructed": "every file is constructed for this task by its generator (task486/generator); the Halvering "
                           "Valley region, its counties, Continuums of Care, the Homeless Data Partnership, the "
                           "coalition, the clinic, the outreach team, the State Data Linkage Unit, their staff and every "
                           "record and number in the files are fictional",
            "public_specifications": "the HMIS files follow the HUD HMIS CSV layout and the HMIS Data Standards' project "
                                     "types, relationship, date-of-birth quality and destination codes (FY2024, and "
                                     "FY2022 for one vendor); the clinic's housing statuses are HRSA's UDS categories; "
                                     "the pair file follows the layout a privacy-preserving linkage service returns "
                                     "(per-field agreement codes and Fellegi-Sunter style scores)",
            "licence": "CC0 1.0 (constructed data)",
            "date": "2026-10-14",
        },
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
