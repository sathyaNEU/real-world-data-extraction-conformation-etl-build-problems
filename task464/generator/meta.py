"""task464 architecture 9: metadata.json, written from the built pack so it never drifts from it."""
import json, os
import world as W
import answers

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NET = W.NETWORK
SEARCH = "%s, network searches of the practices' clinical systems run by the digital and data lead" % NET

FILES = [
    ("repeat_issues_system_a_2024-01_to_2026-11.csv", "spine",
     "Every statin, ACE inhibitor, angiotensin II receptor blocker, DOAC and antiplatelet issue recorded from "
     "1 January 2024 to 30 November 2026 at the four practices on clinical system A, in that system's issue "
     "report layout.", SEARCH, "2026-12-01"),
    ("repeat_issues_system_b_2024-01_to_2026-11.jsonl", "spine",
     "The same issues for the three practices on clinical system B, in that system's JSON lines export.",
     SEARCH, "2026-12-01"),
    ("repeat_authorisations_system_a.csv", "context artifact",
     "System A's repeat authorisations for those medicines active at any point from 1 January 2024: the register "
     "of repeats, with each one's authorised issues, dates and current dosage.", SEARCH, "2026-12-01"),
    ("repeat_authorisations_system_b.csv", "context artifact",
     "System B's repeat authorisations for the same medicines, in its own layout.", SEARCH, "2026-12-01"),
    ("patient_register_2026-12-01.csv", "operating extract",
     "Registration episodes at the seven practices for every patient in the issue searches, under the network's "
     "pseudonym.", SEARCH, "2026-12-01"),
    ("eps_item_cancellations_2024-2026.csv", "operating extract",
     "Items cancelled through the Electronic Prescription Service tracker before they were dispensed.",
     "%s, EPS prescription tracker item report" % NET, "2026-12-01"),
    ("repeat_changes_2024-01_to_2026-11.csv", "operating extract",
     "Edits made in place to those repeats (dosage, quantity, notes, authorising clinician), from the medicines "
     "safety search.", SEARCH, "2026-12-01"),
    ("cvd_clinical_events_2023-2026.csv", "operating extract",
     "The network's coded cardiovascular events search: diagnoses, observations, results and the coded entries of "
     "discharge summaries.", SEARCH, "2026-12-01"),
    ("cvd_product_lookup.csv", "reference",
     "The network's crosswalk of each system's product strings to the drug, strength, form and BNF class.",
     "%s, medicines team" % NET, "2026-06-15"),
    ("pcn_practice_profiles_2026.xlsx", "reference",
     "The seven member practices: ODS code, clinical system, list size, staffing and current pharmacist sessions.",
     "%s, network manager" % NET, "2026-10-05"),
    ("statin_continuity_sessions_brief.pdf", "governing document",
     "The clinical director's brief to the network board on the 2027 statin continuity sessions.",
     "%s, clinical director" % NET, "2026-12-03"),
    ("icb_cvd_repeat_return_2025_spec.pdf", "governing document",
     "The integrated care board's specification for the 2025 CVD medicines repeat return.",
     "Integrated care board, medicines optimisation team", "2026-07-15"),
    ("qof_cvd_achievement_2025-26.csv", "distractor",
     "The practices' published 2025-26 QOF achievement on four cardiovascular indicators.",
     "Quality and Outcomes Framework, practice achievement as published", "2026-09-10"),
    ("dispensed_items_cvd_2025-26.csv", "distractor",
     "Items and quantities dispensed against the practices' prescriptions, by month and chemical, 2025-26.",
     "Dispensing data by prescribing practice, as the network receives it", "2026-07-20"),
]


def main():
    f = answers.figures(write=False)
    names = sorted(os.listdir(os.path.join(BASE, "target")))
    listed = sorted(n for n, *_ in FILES)
    assert names == listed, (names, listed)
    meta = {
        "task": "task464",
        "domain": "pharmacology-pharmacoepidemiology-safety",
        "subdomain": "medication-adherence-persistence",
        "objective": "descriptive-distribution",
        "prompt_shape": "01",
        "as_of": "2026-12-03",
        "extract_to": W.iso(W.ASOF),
        "currency": W.CURRENCY,
        "compiled_by": "%s, digital and data lead" % NET,
        "compiled_on": "2026-12-03",
        "licence": ("Synthetic records compiled for %s's statin continuity sessions brief and its 2025 return. "
                    "Every file is constructed, contains no real patient, and is released for this task's use." % NET),
        "files": [{"path": "target/" + n, "role": role, "covers": cov, "source": src, "date": d,
                   "licence": "synthetic, constructed for this task, free to use"}
                  for n, role, cov, src, d in FILES],
        "distractor_files": ["target/qof_cvd_achievement_2025-26.csv", "target/dispensed_items_cvd_2025-26.csv"],
        "stated_inputs": {"practices": len(W.PRACTICES), "outcome_window": ["2027-03-01", "2027-06-30"],
                          "population_window": ["2026-09-01", "2026-11-30"], "rounding": W.ROUND_TO},
        "field_terms": ["repeat authorisation", "authorised issues", "re-authorisation", "persistence",
                        "proportion of days covered"],
        "deliverables": ["statin_sessions_2027.xlsx", "cvd_repeat_returns_2025.csv"],
        "portal": {"call": "the practice that hosts the statin continuity sessions, January to June 2027",
                   "answer": f["call_name"], "expected": f["call_expected"], "runner_up": f["runner_up_name"]},
    }
    json.dump(meta, open(os.path.join(BASE, "metadata.json"), "w"), indent=2)
    print("  metadata.json, %d files" % len(FILES))


if __name__ == "__main__":
    main()
