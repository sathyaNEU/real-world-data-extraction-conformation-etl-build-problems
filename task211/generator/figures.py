"""figures.json: every number the write-up states, as the write-up states it, emitted from the golden."""
import world as W

NAMES = {c: n for c, n, *_ in W.STATIONS}


def figures(g, info):
    f = {}
    codes = g["call_codes"]
    f["call_stations"] = codes
    f["call"] = {c: dict(site=NAMES[c], dates=[d.strftime("%d/%m/%Y") for d in g["call"][c]["dates"]],
                         peak=g["call"][c]["peak"], peak_day=g["peak_day"][c].strftime("%d/%m/%Y"),
                         days=len(g["call"][c]["dates"])) for c in codes}
    f["detection_days"] = sum(len(g["call"][c]["dates"]) for c in codes)
    f["nat_max_fall_pct"] = g["nat_max_fall"]
    f["art_min_fall_pct"] = g["art_min_fall"]
    f["wet_detection_days"] = g["routes"]["wet_days"]
    f["default_path_stations"] = g["routes"]["R0_codes"]
    f["default_path_count"] = len(g["routes"]["R0_codes"])
    f["checks"] = {c: dict(date=v["date"].strftime("%d/%m/%Y"), kit=v["kit"], source=v["source"], cert=v["cert"],
                           jig=v["jig"], pct="%.1f" % v["pct"], result="Pass" if v["passed"] else "Fail")
                   for c, v in sorted(g["checks"].items())}
    f["checks_failed"] = sorted(c for c, v in g["checks"].items() if not v["passed"])
    f["timely"] = {c: "%.1f" % v["pct"] for c, v in sorted(g["timely"].items())}
    f["air"] = {k: dict(sampler=v["sampler"], conc="%.2f" % v["conc"], volume="%.1f" % v["volume"])
                for k, v in sorted(g["air"].items())}
    f["air_range"] = ["%.2f" % min(v["conc"] for v in g["air"].values()),
                      "%.2f" % max(v["conc"] for v in g["air"].values())]
    f["method"] = dict(baseline_hours=48, floor_nsv_h=30, elevated_nsv_h=15, receipt_window_minutes=60,
                       quarter_intervals="{:,}".format(W.N10))
    f["counts"] = {k: v for k, v in info.items() if k != "reference"}
    return f
