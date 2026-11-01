"""Emits submission.md and generator/figures.json from target/ (every figure the write-up states comes from here)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import results as R  # noqa: E402
import golden  # noqa: E402

SECTIONS = ["1.3", "3.4", "4.1", "4.2", "4.3"]


def fm(x):
    return f"{x:.1f}"


def emit(tdir, task_dir):
    F = R.compute(tdir)
    seg = F["seg_m1"]
    r0 = F["r0_half_m"]
    r1 = R.half_million(F["ladder"]["R1_division_average_mix"])
    r3 = R.half_million(F["ladder"]["R3_more_severe_of_two"])
    a, b, sh = F["ask_a_k"], F["ask_b"], F["ask_b_share"]
    segline = "; ".join(f"{s} {fm(seg[s])}" for s in R.SEG_NAMES)

    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Banking, Credit & Financial Risk (stress testing and capital: a regional bank's ICAAP "
             "severe-scenario credit loss on its business lending book for the stress year).")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append(f"**The severe scenario puts NZD {fm(F['total_half_m'])} million of stressed credit loss on the business "
             f"banking book in the stress year to 30 September 2027.**")
    L.append(f"By reporting segment, in NZD million: {segline}. "
             f"Not NZD {fm(r0)} million, the result of stressing each borrower at its own division's sales path, which "
             f"leaves the firms that builders, hotels and tour operators pay at mild multipliers. "
             f"Not NZD {fm(r1)} million, which averages the payer mix over each division and so understates the "
             f"borrowers most exposed to the hardest-hit payers on a steep Table 2 curve. "
             f"Not NZD {fm(r3)} million, which takes the harsher of the own-division and payer readings for every borrower "
             f"and so stresses builders whose work councils and ministries pay for at the full construction path.")
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append(f"1. The performing business book is **{F['n_perf']} borrowers** with exposure at default of "
             f"**NZD {fm(F['ead_m1'])} million**.")
    L.append(f"2. **{F['other_share_pct']:.0f} per cent** of those borrowers' trading credits in the year to "
             f"30 September 2026 came from payers outside the borrower's own ANZSIC division.")
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append(f"1. Took business_lending_book_2026-09-30.csv, left out the {F['n_default']} customers in risk grade D "
             f"(CR-ST-02 section 1.3) and set exposure at default per section 3.4: {F['n_perf']} borrowers, "
             f"NZD {fm(F['ead_m1'])} million.")
    L.append("2. Read each borrower's ANZSIC division from its BIC code on nzbn_extract_canterbury_otago_southland_2026-10-12.csv "
             "by NZBN (section 4.1), not from the book's industry field, which is blank or on the 1993 codes for some borrowers.")
    L.append(f"3. Classified operating_account_credits_2025-10_to_2026-09.csv: own-account transfers, GST refunds, insurance "
             f"claims, loan advances and credit interest are not sales; card settlements, branch cash and payments from "
             f"individuals are household sales at the borrower's own division; every other payer was matched to the NZBN "
             f"extract's legal or trading name (upper case, LIMITED as LTD, & as AND, first 20 characters): "
             f"{F['other_share_pct']:.0f} per cent of trading credits came from another division.")
    L.append(f"4. Weighted each source division's change in ICAAP_2026_severe_scenario_board_approved.xlsx by the borrower's "
             f"credits to get the change in its own sales, took the Table 2 multiplier on the fall, capped the stressed PD "
             f"at 100 per cent, applied the Table 3 LGD to each facility and summed: NZD {fm(F['total_half_m'])} million.")
    L.append("5. Net credit losses: summed the Business rows of write_offs_2023-10_to_2026-09.csv by posting half and "
             "subtracted the receipts in collections_receipts_FY2026.xlsx dated in the half and on or after the customer's "
             "first write-off, keeping the agency's net remittance and dropping its statement upload (Agency collection, "
             "the same payment gross of commission), and crediting each guarantor's receipts on its personal case "
             "(customer_master_extract_2026-10-09.csv) to the company it guaranteed in guarantees_register_2026-09-30.csv; "
             "segment from the customer master's NZBN on the NZBN extract.")
    L.append("6. Default back-test: graded each customer in risk_grade_snapshot_2025-09-30.csv at the grade in force on "
             "30 September 2025 (grade_overrides_2024-2026.xlsx), counted defaults dated 1 October 2025 to 30 September "
             "2026 in default_register_business_FY2026.csv and default_register_rural_FY2026.csv, gave each defaulted "
             "facility the lending book holds to the customer that holds it (a connected group's cross-default sits under "
             "the group lead's number) and read surviving numbers back through customer_merge_log_2026-03-14.csv.")
    L.append(f"7. The business banking book's stressed credit loss for the stress year to 30 September 2027 is "
             f"NZD {fm(F['total_half_m'])} million.")
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append(f"### {golden.XLSX}")
    L.append("")
    L.append(f"1. Stressed credit loss, business banking book, stress year to 30 September 2027: NZD {fm(F['total_half_m'])} million.")
    L.append("2. Stressed credit loss by reporting segment, NZD million:")
    for s in R.SEG_NAMES:
        L.append(f"   - {s}: {fm(seg[s])}")
    L.append("3. Borrower-level working: one row per performing borrower with its own division, risk grade, trading credits, "
             "sales change through its payers, Table 2 multiplier, stressed PD, EAD and stressed loss.")
    L.append("4. Net credit losses, financial year to 30 September 2026, NZD thousand (H1 October to March, H2 April to September):")
    for s in R.SEG_NAMES:
        L.append(f"   - {s}: H1 {a[(s, 'H1')]:,.0f}, H2 {a[(s, 'H2')]:,.0f}")
    L.append("5. Business borrowers by risk-grade band at 30 September 2025 that defaulted in the following twelve months:")
    for k, lab in enumerate(R.BAND_LABEL):
        L.append(f"   - {lab}: {b[k][1]} defaulted, {sh[k]:.1f} per cent of the band")
    L.append("")
    L.append(f"### {golden.DOCX}")
    L.append("")
    L.append("1. Bar chart of stressed credit loss by reporting segment in NZD million (Figure 1), each bar labelled with "
             "its segment figure.")
    L.append(f"2. The paper states the NZD {fm(F['total_half_m'])} million total, the segment losses, the net credit losses "
             f"by segment and half and the default back-test as in the workbook.")
    L.append("")
    md = "\n".join(L)
    open(os.path.join(task_dir, "submission.md"), "w", encoding="utf-8").write(md)

    figs = {
        "call": {"total_nzd_m_nearest_half": F["total_half_m"], "total_nzd": round(F["total"])},
        "segments_nzd_m": {s: seg[s] for s in R.SEG_NAMES},
        "rivals_nzd_m": {"own_division": r0, "division_average_mix": r1, "more_severe_of_two": r3},
        "components": {"performing_borrowers": F["n_perf"], "ead_nzd_m": F["ead_m1"],
                       "other_division_share_pct": F["other_share_pct"], "grade_d_customers": F["n_default"],
                       "pd_cap_pct": 100, "name_match_characters": 20},
        "ask_a_net_credit_losses_nzd_k": {f"{s} {h}": a[(s, h)] for s in R.SEG_NAMES for h in R.HALVES},
        "ask_b_defaults": {lab: b[k][1] for k, lab in enumerate(R.BAND_LABEL)},
        "ask_b_share_pct": {lab: sh[k] for k, lab in enumerate(R.BAND_LABEL)},
        "ask_b_borrowers": {lab: b[k][0] for k, lab in enumerate(R.BAND_LABEL)},
        "standard_sections": SECTIONS,
        "grade_bands": ["1", "3", "4", "5", "6", "7", "9"],
        "calendar": {"book_date": "30 September 2026", "stress_year_end": "30 September 2027",
                     "back_test_from": "1 October 2025", "back_test_grade_date": "30 September 2025",
                     "day": 30, "years": [2025, 2026, 2027]},
    }
    gdir = os.path.join(task_dir, "generator")
    with open(os.path.join(gdir, "figures.json"), "w", encoding="utf-8") as f:
        json.dump(figs, f, indent=1, ensure_ascii=False)
        f.write("\n")
    return F, md


if __name__ == "__main__":
    emit(sys.argv[1], sys.argv[2])
