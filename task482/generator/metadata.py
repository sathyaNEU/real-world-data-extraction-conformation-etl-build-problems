"""metadata.json in the task folder, outside target/: the distractors by bundle path and the portal's keys."""
import json

import pack as P

DISTRACTORS = [P.FILES["headcount"], P.FILES["outcomes"]]


def write(path, n):
    meta = {
        "task": "task482",
        "domain": "Education & Learning Sciences (item response theory and test equating)",
        "client_domain": "Education & Learning Sciences",
        "task_type": "item-response-theory-test-equating",
        "objective": "Data Extraction & Conformation (ETL)",
        "distractor_files": DISTRACTORS,
        "distractor_reasons": {
            P.FILES["headcount"]: "each college's fall 2026 headcount, FTE and first-time students: the colleges' size, "
                                  "not the students the QPI placed, and counted on a census date rather than by sitting",
            P.FILES["outcomes"]: "fall 2026 course outcomes by college and course: how placed students fared, which "
                                 "neither sets a placement score nor counts placements",
        },
        "stated_inputs": ["0.20", "-0.70", "60"],
        "deliverables": ["qpi_placement_review_2027.xlsx", "qpi_form27a_score_conversion.csv",
                         "qpi_form27a_expected_score_curve.svg"],
        "as_of": "2027-02-05",
        "files": sorted(P.FILES.values()),
        "rows": {P.FILES[k]: v for k, v in sorted(n.items())},
        "sources": {
            "constructed": "every file is constructed for this task by its generator (task482/generator); the community "
                           "college system, its colleges, its placement test, the item bank, the delivery platforms, "
                           "the students and the people are fictional",
            "public_specifications": "the layouts are the pack's own, in the style of a computer-based test delivery "
                                     "export and an item bank export, described in its data dictionary",
            "licence": "CC0 1.0 (constructed data)",
            "date": "2027-02-05",
        },
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
