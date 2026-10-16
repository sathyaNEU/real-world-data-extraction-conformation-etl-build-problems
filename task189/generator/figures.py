"""figures.json: every number the submission states, as the write-up states it."""
import json
import os

import world as W


def write(gen_dir, g):
    a1 = {k: {"samples": v[0], "below_limit": v[1]} for k, v in g["a1"].items()}
    a2 = {k: {"max_no3_mgl": v[0], "at_or_above_trigger": v[1]} for k, v in g["a2"].items()}
    S = W.STANDARD
    reads = ("mle", "km", "cond", "fitted_dist")
    nc = [min(o[k] for k in reads) for o in g["assess"].values() if o["mle"] > S]
    co = [max(o[k] for k in reads) for o in g["assess"].values() if o["mle"] <= S]
    fig = {"standard_ugl": S,
           "reporting_limit_sensitive_ugl": W.METHODS["TAS-LC-PHX-04"]["rl"],
           "reporting_limit_legacy_ugl": W.METHODS["KGL-GC-PHX-07"]["rl"],
           "legacy_limit_over_standard": round(W.METHODS["KGL-GC-PHX-07"]["rl"] / S, 1),
           "programme_points": 37,
           "nitrate_trigger_mgl_no3": W.NITRATE_TRIGGER,
           "nearest_compliant_pct_below": int(round(100 * (S - max(co)) / S)),
           "nearest_non_compliant_pct_above": int(round(100 * (min(nc) - S) / S)),
           "regulation_clauses": ["1.4", "4.2", "4.4", "7.2", "7.3", "7.5", "7.6"],
           "call": g["count"],
           "non_compliant": g["non_compliant"],
           "water_bodies_assessed": len(g["assess"]),
           "compliance_samples_total": sum(v[0] for v in g["a1"].values()),
           "below_limit_total": sum(v[1] for v in g["a1"].values()),
           "rungs": g["rungs"],
           "censored_readings_agreeing": len(reads),
           "a1_sampling": a1,
           "a2_nitrate": a2,
           "a3_quarter": g["a3"]}
    path = os.path.join(gen_dir, "figures.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return path
