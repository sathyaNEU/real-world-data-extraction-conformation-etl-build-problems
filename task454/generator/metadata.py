"""metadata.json: source, date and licence of every shipped file, and the declared distractors."""
import json, os

FILES = {
    "apn_pos_research_extract_2026.csv": ("Synthetic, constructed in the layout of a card scheme's de-identified point-of-sale research sample: one row per sampled card, merchant region and month of 2026", "2027-01-22"),
    "apn_research_cards_2026.xlsx": ("Synthetic card register of the research sample: each sampled card's selection stratum and weight", "2027-01-22"),
    "apn_regional_totals_2026.csv": ("Synthetic monthly card spending totals by merchant region and issuer location, all card products", "2027-01-22"),
    "erp_sa2_30jun2026_preliminary.csv": ("Synthetic preliminary estimated resident population by statistical area level 2, in the layout of a national statistics office's regional population release", "2026-12-17"),
    "erp_sa2_30jun2025_revised.xlsx": ("Synthetic revised estimated resident population by statistical area level 2 for 30 June 2025", "2026-12-17"),
    "rvif_2027_round_guidelines.pdf": ("Constructed governing document: the Fund's guidelines for the 2027 round", "2026-11-09"),
    "rtip_agreements_2026-12-31.xlsx": ("Synthetic grants management system export of the older program's agreements", "2027-01-05"),
    "rtip_claims_2026.csv": ("Synthetic export of the older program's 2026 claims", "2027-01-05"),
    "ap_payments_rtip_2026.csv": ("Synthetic accounts payable export of the older program's 2026 payments", "2027-01-08"),
    "ar_receipts_rtip_2026.csv": ("Synthetic accounts receivable export of the older program's 2026 receipts", "2027-01-08"),
    "rtip_closure_decision_2026.pdf": ("Constructed governing document: the board's decision closing the older program", "2026-10-21"),
}
DISTRACTORS = {
    "apn_regional_totals_2026.csv": "The scheme's monthly totals by merchant region carry every card product and overseas cards and no cardholder; they are a control on the research sample's coverage and no part of the measure or the asks.",
    "erp_sa2_30jun2025_revised.xlsx": "The 30 June 2025 revised estimates sit beside the 30 June 2026 preliminary release; the guidelines file the 2026 estimates as the denominator.",
}


def write(task, T):
    out = {"task": "task454", "files": {}, "distractors": DISTRACTORS, "generator": "generator/build.py",
           "licence_note": "Every file is synthetic or constructed for this task and released under CC BY 4.0; no third-party data are included."}
    for fn in sorted(os.listdir(T)):
        src, date = FILES[fn]
        out["files"][fn] = {"source": src, "date": date, "licence": "CC BY 4.0 (constructed for this task)"}
    json.dump(out, open(os.path.join(task, "metadata.json"), "w"), indent=1, sort_keys=True)
