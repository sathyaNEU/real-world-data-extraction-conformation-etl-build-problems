"""Every figure the write-up states, so figures_check.py can hold it to the data."""
import json

import estimators as E
import world as W


def write(g, path):
    a3_month, a3_norec, a3_norec_names, a3_differ = g["a3"]
    out = {
        "constants": {
            "band_lower_bound": 9000,
            "band_upper_bound": 10000,
            "mirror_upper_bound": E.MIRROR_HI,
            "handbook_clause": 7.4,
            "handbook_segment_clause": 7.5,
            "fit_window_lower_bound": min(lo for lo, hi in E.WINDOWS),
            "fit_window_upper_bound": max(hi for lo, hi in E.WINDOWS),
            "bin_width_smallest": min(E.WIDTHS),
            "bin_width_largest": max(E.WIDTHS),
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
            "deposits_split_stated_to_the_nearest": W.GRAIN,
        },
        "steps": {
            "near_threshold_band_counted": g["band_all"],
            "same_day_screen": g["screen"],
            "band_read_on_its_own": g["one_total"],
            "customer_against_prior_year": g["rise"],
            "prior_year_on_the_same_reading": g["prior_total"],
            "mirror_deposits_observed": sum(g["mirror_obs"].values()),
            "counter_rows": g["stats"]["counter"],
            "machine_rows": g["stats"]["machine"],
            "specifications_in_the_grid": g["grid_n"],
            "specifications_the_record_leaves": g["sweep_n"],
            "specifications_the_record_refuses": g["grid_n"] - g["sweep_n"],
            "mirror_deposits_the_profile_puts_there":
                int(round(sum(g["mirror_obs"].values()) + sum(g["per_seg_raw"].values()))),
            "least_distance_to_a_rounding_edge": round(min(g["edges"].values()), 1),
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
