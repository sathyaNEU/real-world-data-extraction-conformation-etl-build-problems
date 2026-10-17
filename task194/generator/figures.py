"""generator/figures.json: every number the write-up is allowed to state."""
import json
import os


def write(gendir, g):
    a, r, t = g["answer"], g["runner"], g["third"]
    r0, r3 = g["rung0"], g["rung3"]
    f, d = g["facts"], g["demo"]
    out = {
        "call": "place the cycle IP-11 improvement team with Alderbrook Orthopaedics, cost centre %s"
                % a["unit"],
        "call_unit_code": a["unit"],
        "call_unit": "Alderbrook %s" % a["name"],
        "avoidable_at_pick": round(a["avoidable"]),
        "runner_unit_code": r["unit"],
        "runner_unit": "Marrowfield %s" % r["name"],
        "avoidable_at_runner": round(r["avoidable"]),
        "third_unit_code": t["unit"],
        "avoidable_at_third": round(t["avoidable"]),
        "gap_complications": round(a["avoidable"]) - round(r["avoidable"]),
        "margin": round(g["margin"], 2),
        "standard_error_lead": round(g["se_lead"], 2),
        "standard_error_of_gap": round(g["se_gap"], 2),
        "pick_standard_error": round(a["se"], 2),
        "runner_standard_error": round(r["se"], 2),
        "pick_planned_separations": a["plan"],
        "pick_record_separations": a["separations"],
        "pick_in_scope_episodes": a["episodes"],
        "pick_observed_complications": int(a["observed"]),
        "pick_expected_published": round(a["expected"], 1),
        "pick_expected_comparison": round(a["expected_net"], 1),
        "pick_expected_complications": round(a["expected_plan"], 1),
        "pick_published_ratio": round(a["ratio"], 2),
        "pick_comparison_ratio": round(a["ratio_net"], 2),
        "pick_published_excess": round(a["published_excess"], 1),
        "pick_adjusted_rate": round(a["adjusted_rate"], 1),
        "pick_closed_quarters": a["quarters"],
        "eligible_units": len(g["eligible"]),
        "eligible_unit_codes": [d2["unit"] for d2 in g["units"]],
        "published_rank_of_call": g["published_rank"],
        "avoidable_by_unit": {d2["unit"]: round(d2["avoidable"]) for d2 in g["units"]},
        "published_excess_by_unit": {d2["unit"]: round(d2["published_excess"], 1) for d2 in g["units"]},
        "charter_clauses": ["4.1", "4.2", "4.3", "4.4", "4.5"],
        "specification_clauses": ["2.1", "2.2", "2.3", "2.4", "2.5", "3.1", "3.2", "3.3", "3.4"],
        "rate_denominator": 1000,
        "reference_rate": 96.6,
        "year_end_day": 31,
        "rung0_unit_code": r0["unit"],
        "rung0_published_excess": round(r0["published_excess"], 1),
        "rung0_avoidable": round(r0["avoidable"]),
        "rung0_published_ratio": round(r0["ratio"], 2),
        "rung3_unit_code": r3["unit"],
        "rung3_per_1000": round(r3["per_1000"], 1),
        "pick_per_1000": round(a["per_1000"], 1),
        "published_table_derived_year_end_day": 30,
        "neutral_ratio": 1.00,
        "unit_quarters_in_the_series": sum(1 for _ in g["units"]) and len(
            [1 for k in g["bundle"]["panel"]]),
        "rung3_avoidable": round(r3["avoidable"]),
        "band_drift": {b: round(v, 3) for b, v in f["drift"].items()},
        "band_drift_low": round(f["drift_low"], 3),
        "band_drift_high": round(f["drift_high"], 3),
        "band_drift_spread": round(f["drift_spread"], 2),
        "surgical_share_low": round(f["surgical_low"], 3),
        "surgical_share_high": round(f["surgical_high"], 3),
        "candidates_with_no_surgical_work": f["surgical_none"],
        "demonstration_unit_code": d["unit"],
        "demonstration_published_low": round(d["published_low"], 1),
        "demonstration_published_high": round(d["published_high"], 1),
        "demonstration_published_multiple": round(d["published_multiple"], 1),
        "demonstration_comparison_low": round(d["internal_low"], 1),
        "demonstration_comparison_high": round(d["internal_high"], 1),
        "demonstration_comparison_spread": round(d["internal_spread"], 2),
        "demonstration_shifted_quarters": d["shifted"],
        "demonstration_mix_swing": round(d["mix_swing"], 3),
        "readings_of_clause_43": len(g["convergence"]),
        "readings_naming_the_call": sum(1 for v in g["convergence"].values()
                                        if v["first"] == a["unit"]),
        "reading_margins": {k: round(v["margin"], 2) for k, v in g["convergence"].items()},
        "route_winners": {k.split()[0]: v["first"] for k, v in g["routes"].items()},
        "route_margins": {k.split()[0]: round(v["margin"], 2) for k, v in g["routes"].items()},
        "hospital_year": {h["hospital"]: {"name": h["name"], "episodes": h["episodes"],
                                          "complications": h["complications"],
                                          "adjusted_rate_per_1000": round(h["rate"], 1)}
                          for h in g["hospitals"]},
        "outside_indicator": {o["quarter"]: {"separations": o["separations"],
                                             "with_complication": o["with_complication"]}
                              for o in g["outside"]},
        "complication_groups": {x["group"]: {"name": x["name"], "fy2025_26": x["fy2025"],
                                             "fy2026_27": x["fy2026"]} for x in g["groups"]},
    }
    p = os.path.join(gendir, "figures.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return p
