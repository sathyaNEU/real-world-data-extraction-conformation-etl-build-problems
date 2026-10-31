"""Write task480/metadata.json from the built pack."""
import json
import os

import world as W

SOURCES = {
    "roll": "the Tamarack County assessor's real property roll of residential parcels, 1 January 2026",
    "cos": "the county's consolidated log of certificates of occupancy issued by the municipal building inspectors, "
           "January 2020 to June 2026",
    "demo": "the county's consolidated log of demolition permits since 2000",
    "bg2020": "the 2020 census Demographic and Housing Characteristics counts for the county's block groups",
    "history": "the State Data Center's compilation of the 2000, 2010 and 2020 census counts by municipality",
    "boundary": "the state's register of municipal annexations and consolidations since 2000",
    "gq": "the State Data Center's annual survey of group quarters, 2026",
    "points": "the county's address points, July 2026",
    "births": "the State Registrar's resident birth file for the county, filings July 2025 to August 2026",
    "deaths": "the State Registrar's resident death file for the county, filings July 2025 to August 2026",
    "act": "an excerpt of the Municipal Road Aid Act (statutes, ch. 84, subch. II)",
    "method": "the State Data Center's statement of its 2026 municipal estimates program",
    "roads": "the Department of Transportation's certified local road miles for the 2027 aid year",
    "vintage": "the Census Bureau's Vintage 2025 county population estimates for the state",
}


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            n = sum(1 for _ in fh) - 1
        return n - 1 if "census2020_dhc" in path else n
    return None


def write(out_path, n, target):
    files = []
    by_name = {v: k for k, v in W.FILES.items()}
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[by_name[f]], "date": "2026-10-30",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task480",
        "architecture": 3,
        "title": "The municipalities of Tamarack County that reach 10,000 residents on 1 July 2026 and move into the "
                 "road aid formula's urban tier for 2027, with each municipality's resident births and deaths",
        "domain": "Survey Research & Official Statistics",
        "subdomain": "census-register-administrative-data-quality (a state data center's certification of municipal "
                     "populations for a road aid formula)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "10: a scorecard of every municipality against the 10,000 line, with each municipality's resident "
                        "births and deaths and a chart of the estimates against the line",
        "as_of": "2026-10-30",
        "deliverables": ["tamarack_municipal_estimates_2026.xlsx", "urban_tier_estimates_2026.svg"],
        "distractor_files": [W.FILES[k] for k in W.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task480/generator/build.py (seeded, deterministic) in the "
                               "layouts of a county assessor's residential roll, municipal building inspectors' "
                               "certificate and demolition logs, the Census Bureau's 2020 block group tables, a state "
                               "boundary register, county address points and a state registrar's resident vital files; "
                               "the county, its municipalities, the state's offices and every person and address are "
                               "fictional, and the state and county codes are not any real state's.",
                     "date": "2026-10-30", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-30",
        "generator": "task480/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta
