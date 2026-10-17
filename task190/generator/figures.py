"""figures.json: every number the submission states."""
import json
import os

import world as W


def write(gen_dir, g):
    a = g["assess"]
    fig = {"framework_clauses": ["2.3", "6.2", "6.3", "6.4", "6.5"],
           "closed_record_cases": sum(a[n]["closed_cases"] for n in a),
           "covered": g["covered"], "just_misses": g["just_misses"],
           "capacity": W.CAPACITY, "lines_assessed": len(a),
           "confirmed_two_quarters": {n: a[n]["confirmed_two_quarters"] for n in a},
           "expected_carrying": {n: round(a[n]["expected_carrying"], 1) for n in a},
           "cohort_estimate": {n: round(a[n]["cohort_estimate"], 1) for n in a},
           "months_unseen": {n: round(a[n]["months_unseen"], 1) for n in a},
           "closed_cases": {n: a[n]["closed_cases"] for n in a},
           "rungs": g["rungs"],
           "cut_margin_pct": int(round(100 * (sorted((a[n]["expected_carrying"] for n in a),
                                                     reverse=True)[W.CAPACITY - 1] /
                                              sorted((a[n]["expected_carrying"] for n in a),
                                                     reverse=True)[W.CAPACITY] - 1))),
           "a1_contract": g["a1"], "a2_screening": g["a2"], "a3_queue": g["a3"]}
    path = os.path.join(gen_dir, "figures.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return path
