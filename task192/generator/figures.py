"""Write generator/figures.json: every number the write-up is allowed to state."""
import json
import os

import golden as G
import world as W

CANDIDATES = ("naive", "remove_fp_ppv", "remove_fp_fpr", "recall_only", "pv_pooled",
              "audit_prevalence", "hand_where_audited")


def write(gendir, g):
    cand = {"naive": g["raw_rung0"], "remove_fp_ppv": g["raw_rung1"],
            "remove_fp_fpr": g["raw_rung1b"], "recall_only": g["raw_rung2"],
            "pv_pooled": g["raw_rung3"], "audit_prevalence": g["raw_rung4"],
            "hand_where_audited": g["raw_rung5"]}
    out = {
        "call_actions": g["total"],
        "grain": g["grain"],
        "raw_total": round(g["raw_total"], 2),
        "candidates": {k: round(v, 2) for k, v in cand.items()},
        "candidate_cells": {k: G.grain(v) for k, v in cand.items()},
        "rung_codes_as_filed": G.grain(g["raw_rung0"]),
        "rung_false_marks_out": G.grain(g["raw_rung1"]),
        "rung_hand_where_audited": G.grain(g["raw_rung5"]),
        "rung_audited_shares": G.grain(g["raw_rung3"]),
        "rung_recall_only": G.grain(g["raw_rung2"]),
        "actions_in_period": g["actions_in_period"],
        "press_only_actions": g["press_only"],
        "actions_with_a_filer_report": g["filed_by_hand"],
        "hand_coded_confrontational": g["hand_confrontational"],
        "press_marked_confrontational": g["press_marked"],
        "sample_rows": g["sample_rows"],
        "sample_comparisons": g["sample_coded"],
        "sample_rows_without_a_manual_code": g["sample_uncoded"],
        "sample_tp": g["tp"], "sample_fn": g["fn"], "sample_fp": g["fp"], "sample_tn": g["tn"],
        "classifier_recall": g["recall"], "classifier_false_mark_rate": g["false_mark"],
        "audit_months": g["audit_covers"],
        "themes_without_an_audited_report": sorted(g["dead"]["rg_by_theme"]["broken"]),
        "audit_prevalence_share": round(g["audit_prevalence"], 4),
        "marked_rate_inside_the_audited_window_pct": round(100 * g["marked_rate_inside"], 1),
        "marked_rate_outside_it_pct": round(100 * g["marked_rate_outside"], 1),
        "record_prevalence_share": round(g["record_prevalence"], 4),
        "variant_continuity": round(g["variant_continuity"], 2),
        "variant_matrix_inverse": round(g["variant_matrix_inverse"], 2),
        "variant_hybrid": round(g["variant_hybrid"], 2),
        "variant_rg_fb_month": round(g["variant_rg_fb_month"], 2),
        "variant_rg_fb_theme": round(g["variant_rg_fb_theme"], 2),
        "variant_pv_fb_month": round(g["variant_pv_fb_month"], 2),
        "variant_pv_fb_theme": round(g["variant_pv_fb_theme"], 2),
        "variant_rg_coded_month": round(g["variant_rg_coded_month"], 2),
        "variant_rg_coded_theme": round(g["variant_rg_coded_theme"], 2),
        "variant_rg_r1": round(g["variant_rg_r1"], 2),
        "variant_rg_r2": round(g["variant_rg_r2"], 2),
        "sampling_sd": round(g.get("boot", {}).get("sd_rg", 0.0), 1),
        "sampling_sd_of_the_gap": round(g.get("boot", {}).get("sd_gap", 0.0), 1),
        "mean_gap": round(g.get("boot", {}).get("mean_gap", 0.0), 1),
        "gap_positive_share": round(g.get("boot", {}).get("positive", 0.0), 4),
        "fortnight_rows": len(g["a1"]), "route_rows": len(g["a2"]), "partner_rows": len(g["a3"]),
        "protocol_paragraphs": ["2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "3.2", "3.3",
                                "3.4", "4.1", "4.2", "4.3", "4.4", "4.5", "4.6", "6.1", "6.2"],
        "fortnights": {k: {"actions": v["actions"], "municipalities": v["municipalities"],
                           "partner_actions": v["partner_actions"],
                           "marked_actions": v["marked"]}
                       for k, v in g["a1"].items()},
        "routes": {k: {"received": v["received"], "unplaceable": v["unplaceable"],
                       "median_minutes": v["median_minutes"]} for k, v in g["a2"].items()},
        "partners": {k: {"filed": v["filed"], "after_close": v["after_close"], "euros": v["euros"]}
                     for k, v in g["a3"].items()},
    }
    p = os.path.join(gendir, "figures.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return p
