"""generator/figures.json: every number the write-up is allowed to state."""
import json
import os


def write(gendir, g):
    a, r = g["answer"], g["runner"]
    r0, r1, r2 = g["rung0"], g["rung1"], g["rung2"]
    out = {
        "call": "place the cycle IP-10 improvement team with Alderbrook Orthopaedics, cost centre %s"
                % a["unit"],
        "call_unit_code": a["unit"],
        "call_unit": "Alderbrook %s" % a["name"],
        "avoided_at_pick": round(a["avoided"]),
        "runner_unit_code": r["unit"],
        "runner_unit": "Alderbrook %s" % r["name"],
        "avoided_at_runner": round(r["avoided"]),
        "gap_complications": g["gap"],
        "pick_standardised_ratio": round(a["ratio"], 2),
        "pick_planned_separations": a["plan"],
        "pick_expected_complications": round(a["expected_plan"]),
        "pick_excess_complications": round(a["excess"], 1),
        "eligible_units": len(g["eligible"]),
        "eligible_unit_codes": [d["unit"] for d in sorted(g["units"], key=lambda x: -x["avoided"])],
        "charter_clauses": ["4.1", "4.2", "4.3", "4.4", "4.5"],
        "specification_clauses": ["2.1", "2.2", "2.3", "2.4", "2.5", "3.1", "3.2", "3.3", "3.4"],
        "rate_denominator": 1000,
        "closed_placements": len(g["record"]),
        "register_readings": {k: round(v, 6) for k, v in g["readings"].items()},
        "effect_models": {k: {"chi_square": round(v["chi_square"], 4),
                              "likelihood_ratio": float("%.6g" % v["likelihood_ratio"]),
                              "parameter": round(v["parameter"], 6)}
                          for k, v in g["models"].items()},
        "avoided_by_unit": {d["unit"]: round(d["avoided"]) for d in g["units"]},
        "rung0_unit_code": r0["unit"],
        "rung0_excess_now": round(r0["last_excess"]),
        "rung0_ratio_record": round(r0["ratio"], 2),
        "rung0_ratio_quarter": round(r0["last_ratio"], 2),
        "rung0_excess": round(r0["excess"], 1),
        "rung0_avoided": round(r0["avoided"]),
        "rung1_unit_code": r1["unit"],
        "rung1_ratio": round(r1["ratio"], 2),
        "rung1_adjusted_rate": round(r1["adjusted_rate"], 1),
        "rung1_planned_separations": r1["plan"],
        "rung1_excess": round(r1["excess"], 1),
        "rung1_avoided": round(r1["avoided"]),
        "rung2_unit_code": r2["unit"],
        "rung2_expected_next": round(r2["expected_next"]),
        "rung2_excess": round(r2["excess"], 1),
        "rung2_avoided": round(r2["avoided"]),
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
