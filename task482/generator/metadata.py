"""metadata.json in the task folder, outside target/: the distractors by bundle path and the portal's keys."""
import json

import pack as P

DISTRACTORS = [P.FILES["quotes"], P.FILES["weather"]]


def write(path, n):
    meta = {
        "task": "task482",
        "domain": "General Statistics & Data Science (data integration, record linkage and entity resolution)",
        "client_domain": "General Statistics & Data Science",
        "task_type": "data-integration-record-linkage-entity-resolution",
        "objective": "Data Extraction & Conformation (ETL)",
        "distractor_files": DISTRACTORS,
        "distractor_reasons": {
            P.FILES["quotes"]: "procurement's quotations for the new pharmaceutical refrigerators (models, prices, "
                               "installation, qualification, lead times): what a replacement costs, not which stores "
                               "get one",
            P.FILES["weather"]: "the region's daily weather at its airport station, 2026, the storm days marked: the "
                                "weather behind the outages, which no store's hours or stock turn on",
        },
        "stated_inputs": ["8 C", "24 hours", "2026", "whole hours", "whole doses", "whole dollars"],
        "deliverables": ["penwick_refrigerator_replacements_2027.xlsx", "penwick_vaccine_hours_2026.svg"],
        "as_of": "2027-01-25",
        "files": sorted(P.FILES.values()),
        "rows": {P.FILES[k]: v for k, v in sorted(n.items())},
        "sources": {
            "constructed": "every file is constructed for this task by its generator (task482/generator); the "
                           "pharmacy chain, its stores and the chains it bought, the logger makes, the monitoring "
                           "vendor, the wholesaler, the manufacturers, the service contractor and the people are "
                           "fictional, and the NDCs and lot numbers are invented",
            "public_specifications": "the layouts follow the style of digital data logger exports (CSV and download "
                                     "reports), a wireless monitoring system's cloud export, a pharmaceutical "
                                     "wholesaler's invoice and credit memo lines with 11-digit NDCs, a pharmacy "
                                     "system's administration and inventory extracts, and a field service portal's "
                                     "visit history",
            "licence": "CC0 1.0 (constructed data)",
            "date": "2027-01-25",
        },
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
