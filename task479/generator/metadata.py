"""metadata.json in the task folder, outside target/: the distractors by bundle path and the portal's keys."""
import json

import pack as P

DISTRACTORS = [P.FILES["crs"], P.FILES["firm"], P.FILES["crosswalk"]]


def write(target, path, n):
    meta = {
        "task": "task479",
        "domain": "General Statistics & Data Science (data integration, record linkage and entity resolution)",
        "client_domain": "General Statistics & Data Science",
        "task_type": "data-integration-record-linkage-entity-resolution",
        "objective": "Data Extraction & Conformation (ETL)",
        "distractor_files": DISTRACTORS,
        "distractor_reasons": {
            P.FILES["crs"]: "the members' Community Rating System classes and premium discounts; the expected claim rate "
                            "counts claims and building-years, which no class or discount changes",
            P.FILES["firm"]: "the flood map revisions in the members' communities; every policy and claim carries the "
                             "base flood elevation it was rated on, so no map is read",
            P.FILES["crosswalk"]: "the authority's property numbers matched to FEMA's buildings; the rate replays each "
                                  "building's own claims against its own floor and the pipeline counts the register's "
                                  "properties by community, so no property is joined to a building",
        },
        "deliverables": ["tsrfa_2027_private_flood_pilot.xlsx", "tsrfa_pilot_elevated_buildings_2026-09-30.csv"],
        "as_of": "2026-10-02",
        "files": sorted(P.FILES.values()),
        "rows": {P.FILES[k]: v for k, v in sorted(n.items())},
        "sources": {
            "constructed": "every file is constructed for this task by its generator (task479/generator); the "
                           "authority, its counties, communities, companies, people, buildings, policies, claims and "
                           "projects are fictional",
            "public_specifications": "the layouts and field names follow FEMA's NFIP policy and claims data (OpenFEMA "
                                     "FIMA NFIP Redacted Policies and Claims, the 2023 release's field names) and the "
                                     "NFIP's occupancy, condominium and cause-of-loss codes, U.S. government works in "
                                     "the public domain",
            "licence": "CC0 1.0 (constructed data)",
            "date": "2026-10-02",
        },
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
