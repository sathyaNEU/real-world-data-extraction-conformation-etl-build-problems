"""metadata.json in the task folder: per shipped file its source, date, licence and rows, the distractors and what the
task decides (never how)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
SYN = " (fictional, synthetic records)"
LIC = "CC0-1.0 (synthetic, generated for this task)"
RBA = "Ridgeline Benefit Administrators"
PCC = "Pembrook Castings Company"
SOURCES = {
    "rba_classic_claims_2024-01_2025-06.csv": (RBA + ", Classic adjudication platform, dental claim lines extract", "2025-07-03"),
    "rba_classic_predeterminations_2024-01_2025-06.csv": (RBA + ", Classic platform, predetermination log", "2025-07-03"),
    "rba_classic_accumulators_2024-01_2025-06.csv": (RBA + ", Classic platform, month-end benefit accumulators", "2025-07-03"),
    "rba_classic_eligibility_2025-06-30.csv": (RBA + ", Classic platform, eligibility spans at conversion", "2025-06-30"),
    "rba_member_crosswalk_2025-07-01.csv": (RBA + ", member identifier crosswalk, Classic to Nexus conversion", "2025-07-01"),
    "rba_nexus_claim_lines_2025-07_2026-10.csv": (RBA + ", Nexus adjudication platform, dental claim lines extract", "2026-10-09"),
    "rba_nexus_estimates_2025-06_2026-09.csv": (RBA + ", Nexus platform, predetermination estimates", "2026-10-09"),
    "rba_nexus_accumulators_2025-07_2026-09.csv": (RBA + ", Nexus platform, month-end benefit accumulators", "2026-10-09"),
    "rba_nexus_eligibility_2026-10-09.csv": (RBA + ", Nexus platform, eligibility spans", "2026-10-09"),
    "ridgeline_ppo_fee_schedule_2024-2027.xlsx": (RBA + ", network contracting, PPO fee schedules 2024 to 2027", "2026-09-15"),
    "rba_ortho_case_schedule_2026-09-30.csv": (RBA + ", orthodontic case schedule", "2026-10-01"),
    "rba_ortho_payments_2024-01_2026-09.csv": (RBA + ", orthodontic installment payments", "2026-10-01"),
    "pembrook_dental_plan_spd_2025.pdf": (PCC + ", Dental Plan Summary Plan Description 2025", "2024-11-18"),
    "pembrook_benefit_costing_standard_f17.pdf": (PCC + ", Finance Policy F-17, Costing Benefit Plan Changes", "2023-03-14"),
    "pembrook_board_bargaining_mandate_2026-09-28.pdf": (PCC + ", Board Resolution 2026-31, bargaining mandate", "2026-09-28"),
    "ridgeline_aso_agreement_schedule_c.pdf": (RBA + " and " + PCC + ", ASO Agreement Schedule C", "2025-05-21"),
    "ridgeline_plan_review_2025_renewal_2026.pdf": (RBA + ", 2025 plan year review and 2026 renewal", "2026-02-18"),
    "ridgeline_network_access_2026q2.xlsx": (RBA + ", network management, network access report Q2 2026", "2026-07-22"),
    "rba_admin_fee_invoices_2025-01_2026-09.csv": (RBA + ", administrative fee invoices", "2026-10-05"),
}
DISTRACTORS = ["target/ridgeline_network_access_2026q2.xlsx", "target/rba_admin_fee_invoices_2025-01_2026-09.csv",
               "target/rba_classic_accumulators_2024-01_2025-06.csv", "target/rba_nexus_accumulators_2025-07_2026-09.csv"]


def main():
    files = []
    for n in sorted(os.listdir(T)):
        src, date = SOURCES[n]
        rows = None
        if n.endswith(".csv"):
            rows = sum(1 for _ in open(os.path.join(T, n), "rb")) - 1
        files.append(dict(file=n, source=src + SYN, date=date, license=LIC, rows=rows))
    meta = dict(task="task482", title="Dental Plan annual maximum, 2027",
                setting="A fictional Missouri iron foundry and machining company's self-insured employee dental plan and "
                        "its claims administrator: the company, the plan, the administrator, the union and the people are "
                        "fictional, and every record is synthetic.", as_of="2026-10-16",
                decides="the annual maximum the company's bargaining committee can agree for 2027 under its board's "
                        "mandate, with the plan's predetermination service by quarter and its outstanding orthodontic "
                        "payments",
                deliverables=["pembrook_dental_member_year_2025.csv", "pembrook_dental_maximum_2027.pdf",
                              "pembrook_dental_maximum_2027.svg"],
                distractor_files=DISTRACTORS, stated_inputs=[], files=files)
    assert set(SOURCES) == set(os.listdir(T)), set(SOURCES) ^ set(os.listdir(T))
    json.dump(meta, open(os.path.join(TASK, "metadata.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
