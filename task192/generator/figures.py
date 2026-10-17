"""Write generator/figures.json: every number the write-up is allowed to state."""
import json
import os


def write(gendir, g):
    out = {
        "call_rate_pct": g["rate_pct"],
        "call_episodes": g["episodes"],
        "cohort_episodes": g["cohort"],
        "recorded_confrontational": g["recorded"],
        "closed_without": g["closed_quiet"],
        "still_open": g["still_open"],
        "actions_in_period": sum(v["actions"] for v in g["a1"].values()),
        "rung0_pct": g["rung0_pct"], "rung0_episodes": g["rung0_episodes"],
        "rung1_pct": g["rung1_pct"], "rung1_episodes": g["rung1_episodes"],
        "rung2_pct": g["rung2_pct"], "rung2_episodes": g["rung2_episodes"],
        "raw_episodes": round(g["raw_episodes"], 2),
        "raw_rate_pct": round(g["raw_rate"], 2),
        "weekly_variant_episodes": round(g["weekly_episodes"], 2),
        "fortnightly_variant_episodes": round(g["fortnightly_episodes"], 2),
        "episode_by_episode_episodes": round(g["projected_episodes"], 2),
        "fortnight_rows": len(g["a1"]), "route_rows": len(g["a2"]), "partner_rows": len(g["a3"]),
        "protocol_paragraphs": ["2.1", "2.2", "2.3", "2.4", "2.5", "3.1", "3.2", "3.3", "3.4",
                                "4.1", "4.2", "4.3", "4.4", "6.1", "6.2"],
        "fortnights": {k: {"actions": v["actions"], "municipalities": v["municipalities"],
                           "partner_share_pct": v["partner_share"],
                           "confrontational_actions": v["confrontational"]}
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
