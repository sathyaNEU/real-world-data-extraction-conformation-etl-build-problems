"""submission.md, drafted from generator/figures.json so every figure it states is one the generator computed.

    python3 task273/generator/writeup.py"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def money(x):
    return "$" + format(x, ",")


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    fix = f["call"]["fix"]
    routes = dict(zip(fix, f["call"]["fix_routes"]))
    rec = f["recorded_ms"]
    raw = f["routes"]["raw"]
    hdr_extra = [c for c in f["routes"]["hdr"] if c not in fix]
    codes = sorted(f["ask_a"])
    lo, hi = f["fix_share_range_pct"]
    fix_list = ", ".join("%s (%s)" % (c, routes[c]) for c in fix[:-1]) + " and %s (%s)" % (fix[-1], routes[fix[-1]])
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** General Statistics & Data Science (missing data, censoring and measurement error).")
    out.append("**Analytical objective:** Descriptive & Distribution Analysis.\n")
    out.append("## 1. Final Recommendation\n")
    words = {3: "three", 5: "five", 10: "ten"}
    out.append("**The platform teams should fix %s of the %d public API endpoints before the 4 December code freeze: %s.**"
               % (words[len(fix)], f["filed"]["endpoints"], fix_list))
    out.append("")
    out.append("At the forecast January peak each of the %s has a 99th-percentile response time above 800 ms for the "
               "requests customers send, the nearest, %s, at about %.1f seconds, once every pod's garbage-collection "
               "pauses in its run of record are met by requests that keep arriving while a pod is paused. Not the "
               "%s the load test's recorded percentiles name (%s, at %s ms): each test client waited for its response "
               "before sending again, so a paused pod's clients sent nothing and the record holds one slow request per "
               "blocked client. Not the %s HdrHistogram's back-fill names: it credits each blocked client with every "
               "request it would have sent while its pod was paused, as if that pod were the only one, and so also "
               "names %s, whose full collections hold one pod in %s, and %s, whose slowest requests are slow on "
               "their own.\n"
               % (words[len(fix)], f["nearest_line"], f["nearest_s"], words[len(raw)], ", ".join(raw),
                  ", ".join("{:,}".format(rec[c]) for c in raw), words[len(f["routes"]["hdr"])], hdr_extra[0],
                  words[f["pods"][hdr_extra[0]]], ", ".join(hdr_extra[1:-1]) + " and " + hdr_extra[-1]))
    out.append("## 2. Critical Components\n")
    out.append("1. The runs of record are the last complete run of each of the **%d** endpoints, minutes 3 to 13; the "
               "first runs of %s stopped early and are set aside." % (f["runs"]["endpoints"],
                                                                     ", ".join(f["runs"]["stopped_early"])))
    out.append("2. Each pod's stop-the-world pauses come from the GC log export, each line ending its pause; the "
               "freeze-list endpoints' pods are paused, on average, for **%.1f to %.1f percent** of each measurement."
               % (lo, hi))
    out.append("3. Over the requests customers send, **%s endpoints** exceed 800 ms at the 99th percentile: %s; "
               "recorded, %s sits at **%s ms** and %s at **%s ms**." % (
                   words[len(fix)], ", ".join(fix), [c for c in fix if c not in raw][0],
                   "{:,}".format(rec[[c for c in fix if c not in raw][0]]), [c for c in fix if c not in raw][1],
                   "{:,}".format(rec[[c for c in fix if c not in raw][1]])))
    out.append("")
    out.append("## 3. Step-by-Step Solution\n")
    out.append("1. Conformed loadtest_jmeter_results_2026-11-10_to_12.jtl (timeStamp is the start, plus elapsed) and "
               "loadtest_k6_results_2026-11-16_to_19.csv (timestamp is the completion, less metric_value) into one "
               "request log by endpoint and pod, and kept each endpoint's last complete run, minutes 3 to 13 "
               "(standard 3.2): %d runs." % f["runs"]["endpoints"])
    out.append("2. Built every pod's pauses from perf_gc_log_export_2026-11-10_to_19.log: Pause lines only, each "
               "ending at its stamp, wall-clock stamps at UTC-05:00, uptime stamps placed from the JVM start that "
               "perf_cluster_pod_events_2026-11.csv gives, after each pod's restart.")
    out.append("3. Took each recorded request's own service time: its response time less the pause time on its pod "
               "while it was in flight.")
    out.append("4. Rebuilt the response times customers would see (standard 1.2, 2.1, 2.2): %s arrivals spread evenly "
               "over each measurement window, each to one of the service's pods with equal chance, each taking a "
               "recorded service time and held by its pod's pauses; the 99th percentile exceeds 800 ms for %s."
               % ("{:,}".format(f["n_mc"]), ", ".join(fix)))
    out.append("5. Compared the recorded 99th percentiles: over 800 ms only for %s." % ", ".join(raw))
    out.append("6. Forecast peak-hour volume (standard 4.1, 4.2): each endpoint's busiest clock hour of January 2026 in "
               "edge_requests_hourly_2026-01.csv on the route that served it (the old path up to the rename in "
               "developer_portal_changelog_2026.html, the new path from it), less the monitors in edge_uptime_monitors.yaml "
               "created before January, times the employers on its plans on 1 November in "
               "crm_employer_accounts_2026-11-01.csv over those on 1 January, found by undoing every event in "
               "billing_subscription_events_2026.csv, latest first.")
    out.append("7. Service credits (standard 5.2): legacy_billing_credits_2026-01_to_04.csv (cents, void credits out) "
               "and billing_credits_2026-05-01_to_11-19.json (credits and reversals) for incidents in "
               "status_page_incidents_2025-12_to_2026-11.xlsx that began from 1 January to 31 October 2026 (Eastern), "
               "by the route each hit, each legacy credit carried forward into the new system counted once at the "
               "amount issued.")
    out.append("8. %s endpoints go on the freeze list: %s." % (words[len(fix)].capitalize(),
                                                                  ", ".join(fix[:-1]) + " and " + fix[-1]))
    out.append("")
    out.append("## 4. Deliverable Answers\n")
    out.append("### yearend_readiness_2027.xlsx\n")
    out.append("1. Verdicts, every endpoint:")
    for c in codes:
        out.append("   - %s: %s" % (c, "fix before the freeze" if c in fix else "meets the standard"))
    out.append("2. Forecast peak-hour volume for January 2027, whole requests an hour:")
    for c in codes:
        out.append("   - %s: %s" % (c, "{:,}".format(f["ask_a"][c])))
    out.append("3. Service credits for breaches from 1 January to 31 October 2026, net of reversals, to the nearest "
               "dollar:")
    for c in codes:
        out.append("   - %s: %s" % (c, money(f["ask_b"][c])))
    out.append("")
    out.append("### yearend_readiness_2027.png\n")
    out.append("1. Bar chart of every endpoint's 99th-percentile response time at the forecast peak against the 800 ms "
               "line, the %d freeze-list endpoints highlighted and the recorded percentile marked on each bar." % len(fix))
    text = "\n".join(out) + "\n"
    assert "—" not in text
    open(os.path.join(TASK, "submission.md"), "w").write(text)


if __name__ == "__main__":
    main()
