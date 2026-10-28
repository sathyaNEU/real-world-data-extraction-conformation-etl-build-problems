"""task464 architecture 8: metadata.json, written from the built pack so it never drifts from it."""
import json, os
import world as W
import answers

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN = "%s, plan record released for the withdrawal review" % W.SERVICE

FILES = [
    ("withdrawals_autumn_winter_2025.csv", "spine",
     "Withdrawals recorded in the autumn and winter terms of 2025/26, exported from the student record system "
     "in use until the winter term closed, with each learner's exit comment and the reason code a coder gave it.",
     "%s, student records (legacy system export)" % W.SERVICE, "2026-01-09"),
    ("withdrawals_spring_summer_2026.json", "spine",
     "Withdrawals recorded in the spring and summer terms, from the Horizon SR v4 learner withdrawal extract, "
     "with the winter withdrawals keyed after the old system closed.",
     "%s, student records (Horizon SR v4)" % W.SERVICE, "2026-08-03"),
    ("coding_moderation_2025_26.csv", "spine",
     "The year's moderation return: the withdrawals the quality team drew by reason code, with the code "
     "recorded and the category the moderating coder placed the comment in.",
     "%s, quality team" % W.SERVICE, "2026-08-21"),
    ("coding_manual_2025.pdf", "governing document",
     "The exit comment coding manual, version 4.2: the six reason codes and when to use each.",
     "%s, quality team" % W.SERVICE, "2025-09-01"),
    ("quality_assurance_procedure.pdf", "governing document",
     "How the quality team draws and moderates the coding sample.", "%s, quality team" % W.SERVICE, "2025-09-01"),
    ("withdrawal_review_terms_of_reference.pdf", "governing document",
     "The terms of reference of the 2025/26 withdrawal review.", "%s, head of service" % W.SERVICE, W.ASOF),
    ("reason_code_list.csv", "reference", "The six reason codes and labels in manual order.",
     "%s, student records" % W.SERVICE, "2025-09-01"),
    ("enrolments_2025_26.csv", "operating extract",
     "Every 2025/26 enrolment on the student record, one row per learner, course and term.",
     "%s, student records (Horizon SR v4)" % W.SERVICE, "2026-08-03"),
    ("course_catalogue_2025_26.csv", "reference",
     "The 2025/26 course catalogue: each course reference with its centre, curriculum area, planned guided "
     "hours, start term and the number of terms it was planned over.",
     "%s, curriculum planning" % W.SERVICE, "2026-08-03"),
    ("site_directory.csv", "reference", "The service's five centres, with the former names the merger replaced.",
     "%s, estates" % W.SERVICE, "2026-01-05"),
    ("retention_budget_2027_lines.xlsx", "context artifact", "The 2027 retention budget lines and their status.",
     "%s, finance" % W.SERVICE, "2026-11-02"),
    ("learner_satisfaction_2025_26.xlsx", "distractor",
     "The 2025/26 learner satisfaction survey by centre and by curriculum area.",
     "%s, quality team" % W.SERVICE, "2026-08-14"),
    ("attendance_rates_2025_26.csv", "distractor",
     "Scheduled sessions and attendance rates by curriculum area and term.",
     "%s, quality team" % W.SERVICE, "2026-08-14"),
]


def main():
    f = answers.figures()
    names = sorted(os.listdir(os.path.join(BASE, "target")))
    listed = sorted(n for n, *_ in FILES)
    assert names == listed, (names, listed)
    meta = {
        "task": "task464",
        "domain": "education-learning-sciences",
        "subdomain": "text-analysis",
        "objective": "descriptive-distribution",
        "prompt_shape": "05",
        "as_of": W.ASOF,
        "currency": W.CURRENCY,
        "compiled_by": "%s, retention lead's office" % W.SERVICE,
        "compiled_on": W.ASOF,
        "licence": ("Compiled by %s for its 2025/26 withdrawal review. Every file is the service's own record, "
                    "synthetic, and released for the review's use." % W.SERVICE),
        "files": [{"path": "target/" + n, "role": role, "covers": cov, "source": src, "date": d,
                   "licence": "service record, synthetic, released for the review's use"}
                  for n, role, cov, src, d in FILES],
        "distractor_files": ["target/learner_satisfaction_2025_26.xlsx", "target/attendance_rates_2025_26.csv"],
        "stated_inputs": {"terms": [t["code"] for t in W.TERMS], "centres": len(W.SITES),
                          "reason_codes": len(W.CODES), "decision_year": W.DECISION_YEAR},
        "field_terms": ["withdrawal", "reason code", "moderation", "learner-course", "planned guided hours"],
        "deliverables": ["withdrawal_reason_composition_2025_26.csv", "retention_target_2027.xlsx"],
        "portal": {"call": "the one withdrawal reason the 2027 retention budget line targets",
                   "answer": f["call_label"], "share_pct": f["call_share_pct"],
                   "runner_up": f["runner_up_label"], "gap_points": f["gap_points"]},
    }
    json.dump(meta, open(os.path.join(BASE, "metadata.json"), "w"), indent=2)
    print("  metadata.json, %d files" % len(FILES))


if __name__ == "__main__":
    main()
