"""generator/figures.json: every number the write-up is allowed to state.

The avoidable counts are rounded to one decimal and the separation and episode counts to whole units,
because that is the precision the asking sentence states ("Avoidable complications to one decimal,
separations and episodes whole"). A figure stated here more coarsely than the prompt asked for is a wrong
figure, so the rounding lives in one place and the write-up copies it.
"""
import json
import os

AVOIDABLE_DP = 1          # the asking sentence's unit for a complication count


def write(gendir, g):
    a, r, t = g["answer"], g["runner"], g["third"]
    r0 = g["rung0"]
    site = {h["hospital"]: h["name"] for h in g["hospitals"]}

    def full(d):
        return "%s %s" % (site[d["hospital"]].replace(" Hospital", "").replace(" District", ""), d["name"])

    def av(x):
        return round(x, AVOIDABLE_DP)

    out = {
        "call": "place the improvement team with %s, cost centre %s" % (full(a), a["unit"]),
        "call_unit_code": a["unit"],
        "call_unit": full(a),
        "call_hospital": site[a["hospital"]],
        "avoidable_at_pick": av(a["avoidable"]),
        "runner_unit_code": r["unit"],
        "runner_unit": full(r),
        "avoidable_at_runner": av(r["avoidable"]),
        "third_unit_code": t["unit"],
        "third_unit": full(t),
        "avoidable_at_third": av(t["avoidable"]),
        "gap_complications": av(a["avoidable"] - r["avoidable"]),
        "margin": round(g["margin"], 3),
        "standard_error_lead": round(g["se_lead"], 2),
        "standard_error_lead_third": round(g["se_lead_third"], 2),
        "standard_error_of_gap": round(g["se_gap"], 2),
        "pick_standard_error": round(a["se"], 2),
        "runner_standard_error": round(r["se"], 2),

        # the pick, from the record
        "pick_planned_separations": a["plan"],
        "pick_record_separations": a["separations"],
        "pick_in_scope_episodes": a["episodes"],
        "pick_observed_complications": int(a["observed"]),
        "pick_developed_complications": round(a["developed"], 1),
        "pick_expected_complications": round(a["expected"], 1),
        "pick_expected_on_plan": round(a["expected_plan"], 1),
        "pick_published_ratio": round(a["ratio"], 3),
        "pick_developed_ratio": round(a["ratio_developed"], 3),
        "pick_uplift_complications": round(a["uplift"], 1),
        "pick_shortfall_per_cent": round(100.0 * (1.0 - a["completeness"]), 2),
        "pick_as_recorded": av(a["as_recorded"]),
        "pick_closed_quarters": a["quarters"],
        "pick_adjusted_rate": round(a["adjusted_rate"], 1),

        # the ladder and the record's own ranking
        "eligible_units": len(g["eligible"]),
        "eligible_unit_codes": [d["unit"] for d in g["units"]],
        "recorded_rank_of_call": g["recorded_rank"],
        "rung0_unit_code": r0["unit"],
        "rung0_unit": full(r0),
        "rung0_as_recorded": av(r0["as_recorded"]),
        "rung0_avoidable": av(r0["avoidable"]),
        "avoidable_by_unit": {d["unit"]: av(d["avoidable"]) for d in g["units"]},
        "as_recorded_by_unit": {d["unit"]: av(d["as_recorded"]) for d in g["units"]},
        "expected_on_plan_by_unit": {d["unit"]: round(d["expected_plan"], 1) for d in g["units"]},
        "planned_separations_by_unit": {d["unit"]: d["plan"] for d in g["units"]},
        "shortfall_per_cent_by_unit": {d["unit"]: round(100.0 * (1.0 - d["completeness"]), 2)
                                       for d in g["units"]},
        "uplift_by_unit": {d["unit"]: round(d["uplift"], 1) for d in g["units"]},
        "route_winners": {k.split()[0]: v["first"] for k, v in g["routes"].items()},
        "route_margins": {k.split()[0]: round(v["margin"], 3) for k, v in g["routes"].items()},
        "route_first_values": {k.split()[0]: round(v["first_value"], 2) for k, v in g["routes"].items()},

        # the observation process: what the close-out register measures
        "quarters_still_moving": sorted(k for k, v in g["lags"].items() if v > 0),
        "closes_still_to_run": {k: v for k, v in g["lags"].items()},
        "development_factor_by_unit_and_lag": {"%s:%d" % (c, l): round(v, 4)
                                               for (c, l), v in sorted(g["factors"].items())},
        "pick_factor_at_lag_0": round(g["factors"][(a["unit"], 0)], 4),
        "runner_factor_at_lag_0": round(g["factors"][(r["unit"], 0)], 4),
        "readings_of_the_development": len(g["convergence"]),
        "readings_naming_the_call": sum(1 for v in g["convergence"].values()
                                        if v["first"] == a["unit"]),
        "reading_margins": {k: round(v["margin"], 3) for k, v in g["convergence"].items()},

        # clauses the write-up cites
        "charter_clauses": ["4.1", "4.2", "4.3", "4.4", "4.5"],
        "specification_clauses": ["2.1", "2.2", "2.3", "2.4", "2.5", "3.1", "3.3", "3.4", "3.7"],
        "rate_denominator": 1000,
        "reference_rate": 96.6,

        # deliverable answers, at the precision the asking sentence states
        "hospital_year": {h["hospital"]: {"name": h["name"], "separations_reported": h["reported"],
                                          "episodes_measured": h["measured"],
                                          "separations_not_measured": h["separations"],
                                          "not_measured_with_a_complication": h["complications"]}
                          for h in g["hospitals"]},
        "not_measured_by_hospital": {h["hospital"]: h["separations"] for h in g["hospitals"]},
        "not_measured_with_a_complication_by_hospital": {h["hospital"]: h["complications"]
                                                         for h in g["hospitals"]},
        "outside_indicator": {o["quarter"]: {"separations": o["separations"],
                                             "with_complication": o["with_complication"]}
                              for o in g["outside"]},
        "complication_groups": {x["group"]: {"name": x["name"], "fy2025_26": x["fy2025"],
                                             "fy2026_27": x["fy2026"]} for x in g["groups_by_year"]},
    }
    p = os.path.join(gendir, "figures.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return p
