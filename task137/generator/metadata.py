"""task137 metadata.json: the portal's keys, the distractors and each shipped file's provenance, outside target/."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as BD   # noqa: E402

CONSTRUCTED = ("constructed for this task by the generator under generator/, in the layout of the named organisation's own "
               "export; no real person, record or organisation's data")
PROV = {
    BD.F_ARR: ("Calderwick Police arrest records (custody system export), pulled 6 October 2026", "2026-10-06"),
    BD.F_POL: ("data.police.uk street-level crime layout (Crime ID, Month, Reported by, Falls within, Longitude, Latitude, "
               "Location, LSOA code, LSOA name, Crime type, Last outcome category, Context), April 2025 to March 2026; "
               "values constructed", "2026-06-04"),
    BD.F_LOOK: ("2021 LSOA to ward best-fit lookup in the ONS layout; codes and names constructed", "2024-07-22"),
    BD.F_ALLOC: ("Calderwick Police custody suite allocation with Custody Services' notes", "2026-09-10"),
    BD.F_MODEL: ("Calderwick Police custody demand model note, version 2.0", "2026-06-11"),
    BD.F_BRIEF: ("Estates and Custody Programme planning brief", "2026-10-20"),
    BD.F_CJU: ("Criminal Justice Unit remand file export", "2026-10-12"),
    BD.F_HC: ("custody healthcare provider contact export", "2026-04-14"),
    BD.F_ESTATE: ("estates register of the custody suites", "2026-09-01"),
    BD.F_POP: ("ward population estimates in the ONS mid-year layout; values constructed", "2025-07-15"),
    BD.F_LIC: ("licensing register of late-night premises", "2026-10-01"),
    BD.F_BH: ("GOV.UK bank holidays JSON layout (england-and-wales), 2025 and 2026 dates as published", "2026-10-19"),
}


def write(root):
    m = {
        "task": "task137",
        "title": "Calderwick Police's planning figure for its Tanner Street custody hub in 2027-28, the detentions the hub "
                 "will book in its first year, with the remand holds and initial health assessments its fit-out is sized from",
        "domain": "Urban & Regional Science",
        "client_domain": "Urban & Regional Science",
        "subdomain": "municipal service demand and resource allocation (a public service's first-year demand at a new site "
                     "from its demand model over the site's catchment, completed by a second agency's caseload booked into "
                     "the operator's facility)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "one figure to the nearest 250 with its two parts and a chart; remand cell hours and holds over 24 "
                        "hours by suite; initial health assessments by suite, day and night",
        "as_of": "2026-10-26",
        "deliverables": ["tanner_street_planning_figure_2027-28.xlsx", "hub_planning_note.docx"],
        "distractor_files": ["target/" + n for n in BD.DISTRACTORS],
        "distractors": [
            {"file": "target/" + BD.F_ESTATE, "wrong_basis": False,
             "why_relevant": "the estates register of the four suites and Tanner Street: cells, children's cells, interview "
                             "and medical rooms, status",
             "why_unused": "it records the estate, not demand or detentions; no figure reads it",
             "ruled_out_by": "its own columns"},
            {"file": "target/" + BD.F_POP, "wrong_basis": False,
             "why_relevant": "the wards' mid-2024 population, a natural driver for a demand per head",
             "why_unused": "the custody demand model is built on arrests, not population; no figure reads it",
             "ruled_out_by": "the model note's method (2.1 to 2.4)"},
            {"file": "target/" + BD.F_LIC, "wrong_basis": False,
             "why_relevant": "the premises licensed past midnight in the city centre wards, where night-time arrests come from",
             "why_unused": "the arrest records already carry the wards' arrests; no figure reads it",
             "ruled_out_by": "the model note's method"},
            {"file": "target/" + BD.F_BH, "wrong_basis": False,
             "why_relevant": "the bank holidays on which the remand courts do not sit",
             "why_unused": "the remand files carry each handover time; no figure reads it",
             "ruled_out_by": "the remand files' handed_to_escort column"},
        ],
        "provenance": [{"file": "target/" + n, "source": src, "dated": d, "licence": "constructed; released with the task "
                        "under the task's licence", "made": CONSTRUCTED} for n, (src, d) in PROV.items()],
        "stated_inputs": ["1 April 2027", "31 March 2028", "250", "2025-26", "24 hours", "07:00", "19:00"],
        "field_terms": [],
    }
    with open(os.path.join(root, "metadata.json"), "w") as fh:
        json.dump(m, fh, indent=1)
        fh.write("\n")


if __name__ == "__main__":
    write(os.path.dirname(HERE))
