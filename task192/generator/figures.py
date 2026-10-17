"""Write generator/figures.json: every number the write-up is allowed to state."""
import json
import os


def write(gendir, g):
    out = {
        "call_actions": g["total"],
        "rung0_actions": g["rung0"], "rung1_actions": g["rung1"], "rung2_actions": g["rung2"],
        "actions_in_period": g["actions_in_period"],
        "press_only_actions": g["press_only"],
        "actions_with_a_filer_report": g["filed_by_hand"],
        "hand_coded_confrontational": g["hand_confrontational"],
        "press_marked_confrontational": g["press_marked"],
        "sample_rows": g["sample_rows"],
        "sample_tp": g["tp"], "sample_fn": g["fn"], "sample_fp": g["fp"], "sample_tn": g["tn"],
        "classifier_recall": g["recall"], "classifier_false_mark_rate": g["false_mark"],
        "raw_total": round(g["raw_total"], 2),
        "variant_continuity": round(g["variant_continuity"], 2),
        "variant_by_round": round(g["variant_by_round"], 2),
        "variant_by_theme": round(g["variant_by_theme"], 2),
        "variant_press_only_sample": round(g["variant_press_only_sample"], 2),
        "variant_matrix_inverse": round(g["variant_matrix_inverse"], 2),
        "fortnight_rows": len(g["a1"]), "route_rows": len(g["a2"]), "partner_rows": len(g["a3"]),
        "protocol_paragraphs": ["2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "3.2", "3.3", "3.4",
                                "4.1", "4.2", "4.3", "4.4", "4.5", "6.1", "6.2"],
        "fortnights": {k: {"actions": v["actions"], "municipalities": v["municipalities"],
                           "partner_share_pct": v["partner_share"], "marked_actions": v["marked"]}
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
