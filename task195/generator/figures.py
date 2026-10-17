"""generator/figures.json: every number the write-up is allowed to state."""
import json
import os

import world as W


def write(gendir, g):
    t = g["table"]
    out = {
        "call": g["call"],
        "comparison_specimens": g["comparison"],
        "confirmed_events": t["n_mixed"],
        "panel_clean": t["n_clean"],
        "service_detected": t["inc_detected"],
        "service_false_calls": t["inc_false"],
        "service_false_rate_pct": round(t["inc_false_rate_pct"], 2),
        "chosen_cutoff": g["call"],
        "chosen_detected": g["chosen"]["detected"],
        "chosen_gain": g["chosen"]["gain"],
        "chosen_gain_pp": round(g["chosen"]["gain_pp"], 2),
        "chosen_false_rate_pct": round(g["chosen"]["false_rate_pct"], 2),
        "runner_up_cutoff": "%.3f" % g["runner_up"]["cutoff"],
        "runner_up_gain_pp": round(g["runner_up"]["gain_pp"], 2),
        "cutoffs": {"%.3f" % r["cutoff"]: {
            "detected": r["detected"], "gain": r["gain"], "gain_pp": round(r["gain_pp"], 2),
            "false_calls": r["false_calls"], "false_rate_pct": round(r["false_rate_pct"], 2),
            "established": "Yes" if r["established"] else "No",
            "ceiling_ok": "Yes" if r["ceiling_ok"] else "No",
            "interval_pp": [round(r["lo_paired"], 2), round(r["hi_paired"], 2)]}
            for r in t["cutoffs"]},
        "panel_weeks": {w["report_ref"]: {"week_ending": w["report_date"],
                                          "specimens": w["specimens"],
                                          "difference": w["difference"],
                                          "results_issued": w["results_issued"]}
                        for w in g["panel_weeks"]},
        "baseline": {b["month"]: {"released": b["released"], "flagged": b["flagged"],
                                  "per_thousand": round(b["per_thousand"], 1)}
                     for b in g["baseline"]},
        "dilution": {d["level"]: {"prepared": d["prepared"], "replicates": d["replicates"],
                                  "median_recovery": round(d["median_recovery"], 3),
                                  "within_fifth": d["within_fifth"]}
                     for d in g["dilution"]},
        "rungs": g["rungs"],
        "protocol_clauses": ["3.1", "3.2", "3.3", "3.4", "3.5", "4.1", "4.2", "5.1", "5.2"],
        "cutoff_values": ["%.3f" % c for c in W.CUTOFFS],
        "confidence_level_pct": 95,
    }
    p = os.path.join(gendir, "figures.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return p
