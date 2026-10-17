"""Every figure the write-up states, so figures_check.py can hold it to the data."""
import json

import world as W


def write(g, path):
    a3_month, a3_norec, a3_norec_names, a3_differ = g["a3"]
    out = {
        "constants": {
            "band_lower_bound": 9000,
            "band_upper_bound": 10000,
            "handbook_clause": 7.4,
            "handbook_segment_clause": 7.5,
        },
        "call": {
            "deposits_split": g["total"],
            "largest_segment": W.SEG_NAME[g["largest"]],
            "largest_segment_deposits_split": g["per_seg"][g["largest"]],
        },
        "critical_components": {
            "segment_deposits_split": {W.SEG_NAME[k]: g["per_seg"][k] for k in W.SEG_KEYS},
            "segment_cash_deposits_paid_in": {W.SEG_NAME[k]: g["deposits"][k] for k in W.SEG_KEYS},
            "cash_deposits_paid_in_total": sum(g["deposits"].values()),
            "band_deposits_observed": g["band_all"],
            "band_deposits_observed_by_segment": {W.SEG_NAME[k]: g["band_obs"][k] for k in W.SEG_KEYS},
        },
        "steps": {
            "same_day_screen": g["rung0"],
            "same_day_screen_habit_netted": g["rung1"],
            "customer_against_prior_year": g["rung2"],
            "one_profile_for_the_book": g["pooled_total"],
            "counter_rows": g["stats"]["counter"],
            "machine_rows": g["stats"]["machine"],
            "estimators_swept": g["sweep_n"],
        },
        "deliverables": {
            "structured_cash_deposits_2027.xlsx": {
                "deposits_split_total": g["total"],
                "largest_segment": W.SEG_NAME[g["largest"]],
                "rows": {W.SEG_NAME[k]: [g["deposits"][k], g["per_seg"][k]] for k in W.SEG_KEYS},
            },
            "structured_deposits_by_segment.png": {
                "bars": {W.SEG_NAME[k]: g["per_seg"][k] for k in W.SEG_KEYS},
                "marked": W.SEG_NAME[g["largest"]],
            },
        },
        "asks": {
            "till_sessions_by_quarter": {q: list(v) for q, v in g["a1"].items()},
            "rating_moves_by_band": {b: list(v) for b, v in g["a2"].items()},
            "machine_hours_by_month": a3_month,
            "machines_with_no_service_record": a3_norec,
            "machines_with_no_service_record_names": a3_norec_names,
            "sites_differing_from_vendor": a3_differ,
        },
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return out
