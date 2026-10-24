"""metadata.json: the pairing, the files and their rows, the distractors, provenance and licence."""
import json
import os


def write(figs, names, path):
    target = os.path.join(os.path.dirname(path), "target")
    files = sorted(os.listdir(target))
    n = figs["rows"]
    rows = {names[k]: n[k] for k in ("elig", "roster", "xwalk", "sessions", "responses", "pv", "pd", "invoices")}
    doc = {
        "task": "task482",
        "domain": "Education & Learning Sciences (item response theory and test equating)",
        "client_domain": "Education & Learning Sciences",
        "task_type": "item-response-theory-test-equating",
        "objective": "Data Extraction & Conformation (ETL)",
        "distractor_files": [names["survey"], names["renewals"]],
        "distractor_reasons": {
            names["survey"]: "teachers' spring 2026 self-reports of how they used the platform; the outcomes guarantee "
                             "is settled on students' assessed achievement and the professional learning hours on the "
                             "sessions delivered, so no figure reads the survey",
            names["renewals"]: "Partnerships' 2026-27 renewal stages, probabilities and forecast revenue; the credits are "
                               "settled on the 2025-26 order forms and applied to the invoices actually raised",
        },
        "wrong_basis_distractors": {},
        "stated_inputs": ["58 partner districts", "2025-26 order forms", "half hour", "cent", "2526", "500", "520",
                          "540", "2026-11-30"],
        "forward_dated_files": {
            names["invoices"]: "the 2026-27 invoice register of 20 November 2026 carries its invoices' due dates and "
                               "service periods, which run past the register date by design",
            names["orders"]: "subscription terms end on 30 June or 31 July 2026, before the setting",
        },
        "deliverables": sorted(figs["deliverables"].values()),
        "as_of": "2026-11-20",
        "files": files,
        "rows": rows,
        "sources": {
            "constructed": "every file is constructed for this task by its generator (task482/generator); Lumenfold "
                           "Learning, the Lumenfold Science Outcomes Assessment, Caldrith Assessment Partners, the 58 "
                           "partner districts and their places, the students, identifiers, accounts, invoices and every "
                           "record and number in the files are fictional",
            "public_specifications": "the item response model (two-parameter logistic), the latent regression population "
                                     "model and plausible values follow the published methodology of large-scale "
                                     "assessment (Mislevy, 1991; Rubin, 1987); the states' prior-test performance level "
                                     "names follow each state's public assessment reporting; roster codes follow common "
                                     "state student information system conventions",
            "licence": "CC0 1.0 (constructed data)",
            "date": "2026-11-20",
        },
    }
    with open(path, "w") as f:
        json.dump(doc, f, indent=1)
