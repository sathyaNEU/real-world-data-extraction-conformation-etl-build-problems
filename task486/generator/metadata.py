"""metadata.json: the task's title, tags, deliverables, distractors, input gates and each file's source, date and
license."""
import json
import os

import pack as P

SOURCES = {
    "blocks": ("2020 Census Demographic and Housing Characteristics File, table P12, blocks of Kelvane County, long "
               "form kept by the agency's planning staff", "2026-10-02"),
    "bgs": ("2020 Census Demographic and Housing Characteristics File, table P12, block groups", "2026-10-02"),
    "tracts": ("2020 Census Demographic and Housing Characteristics File, table P12, the county and its tracts",
               "2026-10-02"),
    "hu": ("2020 Census Demographic and Housing Characteristics File, table H1, blocks", "2026-10-02"),
    "colmeta": ("2020 Census DHC download: column metadata for P12 and H1", "2026-10-02"),
    "notes": ("State Data Center: technical bulletin 2023-04, notes for local users of the 2020 DHC", "2024-02-14"),
    "assign": ("Kelvane County Department of Planning and Development: provider area of each census block",
               "2026-10-02"),
    "points": ("Kelvane County Department of Planning and Development: address points register", "2026-10-02"),
    "acs": ("American Community Survey 2018-2022 five-year estimates, table B01001, block groups", "2026-10-02"),
    "instructions": ("State Department on Aging: program instruction AP-27-02, FY2027 area plan update",
                     "2026-08-14"),
    "policy": ("Kelvane Area Agency on Aging: Board policy N-3, provider allocation of nutrition funds", "2023-09-21"),
    "facilities": ("State licensing list of residential care facilities in Kelvane County, census blocks added by the "
                   "agency", "2026-09-08"),
    "providers": ("Kelvane Area Agency on Aging: provider directory", "2026-10-09"),
    "roster": ("Kelvane Area Agency on Aging case management system: home-delivered meal client roster",
               "2026-10-09"),
    "episodes": ("Kelvane Area Agency on Aging case management system: home-delivered meal episodes", "2026-10-09"),
    "log": ("Route tablet system: home-delivered meal delivery log, FY2026", "2026-10-06"),
    "items": ("Kelvane Area Agency on Aging: route item codes", "2026-10-06"),
    "deaths": ("State Department on Aging: monthly death match runs, statewide", "2026-10-06"),
    "links": ("State Department on Aging: participant registry number links, statewide", "2026-10-06"),
    "inventory": ("Kelvane Area Agency on Aging: data inventory of the planning files", "2026-10-09"),
    "guide": ("Kelvane Area Agency on Aging: field guide to the planning files", "2026-10-09"),
}
DISTRACTORS = ["kelvane_address_points_2026-10-02.csv", "acs2022_5yr_kelvane_block_groups_b01001.csv",
               "licensed_residential_care_kelvane.xlsx"]


def write(target, path, golden_files, counts):
    files = sorted(os.listdir(target))
    fmts = sorted({os.path.splitext(n)[1].lstrip(".") for n in files})
    big = max(counts, key=lambda k: counts[k])
    meta = {
        "task": "task486",
        "architecture": 1,
        "title": ("How many residents aged 60 and over, and aged 75 and over, lived in each of Kelvane County's six "
                  "senior-services provider areas on census day in 2020, with each provider's home-delivered meals "
                  "in FY2026 and its active home-delivered meal clients on 30 September 2026"),
        "domain": "General Statistics & Data Science",
        "subdomain": ("data-integration-record-linkage-entity-resolution (an area agency on aging fuses a formally "
                      "private census release's block group and block tables with census-day housing counts into "
                      "counts of older residents for provider areas whose boundaries cut block groups, and conforms "
                      "its route tablets' delivery log, its case records and the state's death match into each "
                      "provider's service figures)"),
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "14: cuts of a distribution per segment, two age cuts for each of six provider areas, beside "
                        "two service figures for each provider",
        "as_of": "2026-10-09",
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
