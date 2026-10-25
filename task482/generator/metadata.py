"""metadata.json in the task folder: per shipped file its source, date, licence and rows, and the distractors."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
SYN = " (fictional, synthetic records)"
LIC = "CC0-1.0 (synthetic, generated for this task)"
SOURCES = {
    "mlh_tcoc_claims_2025-01_2026-09.csv": ("Merrinlake Health Plan, value-based partner claims extract", "2026-10-07"),
    "mlh_eligibility_2025_2026.csv": ("Merrinlake Health Plan, partner eligibility extract", "2026-10-07"),
    "mlh_attribution_runs_py2025_py2026.csv": ("Merrinlake Health Plan, attribution runs", "2026-10-07"),
    "mlh_care_coordination_remittance_2026.csv": ("Merrinlake Health Plan, care coordination remittance detail", "2026-10-16"),
    "KBP_CLAIMS_LPN_20261009.txt": ("Kesselcrest Benefit Partners, partner claims extract", "2026-10-09"),
    "KBP_ELIG_LPN_20261009.txt": ("Kesselcrest Benefit Partners, partner eligibility extract", "2026-10-09"),
    "KBP_ATTRIBUTION_PY2025F_PY2026R10.xlsx": ("Kesselcrest Benefit Partners, value-based partner attribution", "2026-10-06"),
    "KBP_CCF_REMIT_2026.xlsx": ("Kesselcrest Benefit Partners, care coordination remittances", "2026-10-14"),
    "pmh_partner_claims_2026-10-12.json": ("Pemberglen Mutual Health, value-based partner claims", "2026-10-12"),
    "pmh_members_2026-10-12.csv": ("Pemberglen Mutual Health, partner member coverage", "2026-10-12"),
    "pmh_attribution_py2025_py2026.csv": ("Pemberglen Mutual Health, attribution runs", "2026-10-12"),
    "pmh_ccf_payments_2026.csv": ("Pemberglen Mutual Health, care coordination payments", "2026-10-16"),
    "lpn_primary_care_roster_2026-10.xlsx": ("Larrowbrook Physician Network, credentialing, primary care roster", "2026-10-01"),
    "lpn_master_patient_index.csv": ("Larrowbrook Physician Network, master patient index extract", "2026-10-13"),
    "payer_em_fee_schedules_2026.xlsx": ("Larrowbrook Physician Network, managed care contracting, payer fee schedule excerpts", "2026-01-12"),
    "qualifying_primary_care_services.csv": ("Larrowbrook Physician Network, Performance Standard Appendix A", "2025-12-11"),
    "payer_completion_factors_2026-09.csv": ("The three payers' completion factors, Performance Standard Appendix C", "2026-10-12"),
    "lpn_performance_standard_2026.pdf": ("Larrowbrook Physician Network, Performance Standard for Commercial Members", "2025-12-16"),
    "lpn_board_resolution_2026-07.pdf": ("Larrowbrook Physician Network, Board Resolution 2026-11", "2026-07-24"),
    "payer_settlement_statements_py2025.pdf": ("The three payers' performance year 2025 shared savings statements", "2026-06-12"),
    "lpn_payer_feed_field_guide.txt": ("Larrowbrook Physician Network, payer performance analytics, feed field guide", "2026-10-13"),
    "kbp_medicare_advantage_attribution_2026.xlsx": ("Kesselcrest Benefit Partners, Medicare Advantage provider attribution", "2026-07-16"),
    "lpn_quality_composite_2025.csv": ("The three payers' 2025 quality measure results for the network's practices", "2026-05-29"),
}
DISTRACTORS = ["target/kbp_medicare_advantage_attribution_2026.xlsx", "target/lpn_quality_composite_2025.csv"]


def main():
    files = []
    for n in sorted(os.listdir(T)):
        src, date = SOURCES[n]
        rows = None
        if n.endswith((".csv", ".txt")):
            rows = sum(1 for _ in open(os.path.join(T, n), "rb")) - (1 if n.endswith(".csv") else 0)
        files.append(dict(file=n, source=src + SYN, date=date, license=LIC, rows=rows))
    meta = dict(task="task482", title="Two-sided risk track elections, 2027",
                setting="A fictional clinically integrated network of thirteen independent primary care practices in "
                        "Wisconsin and its three commercial payers: the network, the practices, the payers and the "
                        "people are fictional, and every record is synthetic.", as_of="2026-10-16",
                deliverables=["two_sided_track_elections_2027.xlsx", "practice_cost_vs_benchmark_2026.png"],
                distractor_files=DISTRACTORS, files=files)
    assert set(SOURCES) == set(os.listdir(T)), set(SOURCES) ^ set(os.listdir(T))
    json.dump(meta, open(os.path.join(TASK, "metadata.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
