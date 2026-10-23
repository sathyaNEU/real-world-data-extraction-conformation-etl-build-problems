"""metadata.json in the task folder, outside target/: the distractors by bundle path and the portal's keys."""
import json

import pack as P

DISTRACTORS = [P.FILES["weather"], P.FILES["report"]]


def write(path, n):
    meta = {
        "task": "task482",
        "domain": "General Statistics & Data Science (data integration, record linkage and entity resolution)",
        "client_domain": "General Statistics & Data Science",
        "house_domain": "supply-chain-logistics (transportation network)",
        "task_type": "data-integration-record-linkage-entity-resolution",
        "objective": "Data Extraction & Conformation (ETL)",
        "distractor_files": DISTRACTORS,
        "distractor_reasons": {
            P.FILES["weather"]: "Wellhaven's daily temperatures, rain and snow for the period: the weather behind the "
                                "season's ridership and the pay stations' cold-weather faults, which no station's "
                                "availability, sales or card downtime is computed from",
            P.FILES["report"]: "Northlane's quarterly report to the City: monthly trips, casual trips, fleet moves and "
                               "fault reports for the whole system, and the quarter's operations notes; it states no "
                               "station's availability, sales or downtime",
        },
        "stated_inputs": ["Schedule C", "90 per cent", "service hours 6:00 to midnight Eastern", "Q4 2026", "Q1 2027",
                          "whole per cent", "one decimal of a point", "dollars to the cent", "whole hours"],
        "deliverables": ["priority_stations_2027q1.xlsx", "station_availability_2026q4.html"],
        "as_of": "2027-01-12",
        "files": sorted(P.FILES.values()),
        "rows": {P.FILES[k]: v for k, v in sorted(n.items())},
        "sources": {
            "constructed": "every file is constructed for this task by its generator (task482/generator); the City of "
                           "Wellhaven, its bike-share stations, the operator Northlane Mobility, the pay-station "
                           "vendor, their staff and every number in the files are fictional",
            "public_specifications": "the station status archive follows the General Bikeshare Feed Specification "
                                     "(GBFS 2.3) station_status and station_information fields; the trip export, fleet "
                                     "moves log, rider fault reports, pay-station sales export, alarm log, work orders "
                                     "and asset register follow the layouts bike-share operators and kiosk vendors "
                                     "commonly publish or hand to their cities",
            "licence": "CC0 1.0 (constructed data)",
            "date": "2027-01-12",
        },
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
