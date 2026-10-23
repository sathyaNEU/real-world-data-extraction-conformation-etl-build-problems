"""metadata.json in the task folder, outside target/: the distractors by bundle path and the portal's keys."""
import json

import pack as P

DISTRACTORS = [P.FILES["oews"], P.FILES["demand"]]


def write(path, n):
    meta = {
        "task": "task483",
        "domain": "Survey Research & Official Statistics (census, register and administrative data quality)",
        "client_domain": "Survey Research & Official Statistics",
        "task_type": "census-register-administrative-data-quality",
        "objective": "Data Extraction & Conformation (ETL)",
        "distractor_files": DISTRACTORS,
        "distractor_reasons": {
            P.FILES["oews"]: "the state's May 2025 occupational wage estimates for the occupations the college trains "
                             "for: what the occupations pay statewide, not what the programs' own completers earned",
            P.FILES["demand"]: "the board's in-demand occupations list for its outreach and sector partnerships: which "
                               "occupations the board promotes, which no test in the designation standard reads",
        },
        "stated_inputs": ["2027-28 grant year", "July 2024 to June 2025 fiscal year", "whole thousands of dollars",
                          "whole per cent", "whole dollars", "nearest 10 dollars"],
        "deliverables": ["larkspur_workforce_value_2027-28.xlsx", "larkspur_program_tests_2027-28.svg"],
        "as_of": "2026-10-16",
        "files": sorted(P.FILES.values()),
        "rows": {P.FILES[k]: v for k, v in sorted(n.items())},
        "sources": {
            "constructed": "every file is constructed for this task by its generator (task483/generator); the state, "
                           "its workforce board and data center, the college and its campuses, the other colleges and "
                           "training providers, the employers and the people are fictional, and every identifier "
                           "(student, participant, employer account, loan, invoice, payment) is invented",
            "public_specifications": "the layouts follow the style of state postsecondary earnings outcome releases "
                                     "(campus by program by cohort cells with earnings percentiles and small-cell "
                                     "suppression), unemployment insurance quarterly wage records, workforce grant "
                                     "participant rosters and provider payment exports, a college's completion "
                                     "extracts from two student systems, an invoice register and a Direct Loan "
                                     "disbursement export",
            "licence": "CC0 1.0 (constructed data)",
            "date": "2026-10-16",
        },
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
