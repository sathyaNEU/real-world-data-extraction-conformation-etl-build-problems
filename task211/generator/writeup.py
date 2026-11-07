"""submission.md, drafted from figures.json: the tags, the call, the critical components, at most eight steps and
the deliverable answers grouped by file."""
import os

import pack


def write(task_dir, f):
    c1, c0 = f["call_stations"][1], f["call_stations"][0]
    A, B = f["call"][c1], f["call"][c0]
    md = []
    md.append("## Tags\n")
    md.append("- **Domain:** Physical & Environmental Sciences, environmental monitoring and exceedance (ambient gamma "
              "dose-rate monitoring network, natural against artificial increases).")
    md.append("- **Analytical objective:** Anomaly Detection & Diagnostics.\n")
    md.append("## 1. Final Recommendation\n")
    md.append("**Yes: notify increases of artificial origin at %s %s on %d days (%s), highest ten-minute value %d nSv/h, "
              "and at %s %s on %d days (%s), highest %d nSv/h.** No other station recorded one; clearing increases "
              "on rain at the nearest gauge would notify many more and miss the radiography on wet evenings.\n" % (
                  c1, A["site"], A["days"], ", ".join(A["dates"]), A["peak"], c0, B["site"], B["days"],
                  ", ".join(B["dates"]), B["peak"]))
    md.append("## 2. Critical Components\n")
    md.append("1. A natural excess (rain-washed radon progeny) never fell by more than **%d per cent** in one "
              "ten-minute step anywhere in the quarter." % f["nat_max_fall_pct"])
    md.append("2. Each of the **%d** detection days ended with the excess falling by **%d per cent or more** in one step "
              "and staying down." % (f["detection_days"], f["art_min_fall_pct"]))
    md.append("3. On **%d** of those days the nearest valley rain gauge recorded rain within an hour of the increase, so rain "
              "coincidence does not decide origin.\n" % f["wet_detection_days"])
    md.append("## 3. Step-by-Step Solution\n")
    md.append("1. Read `%s`, exact duplicate rows once, microsieverts converted, T and F records set aside." %
              pack.FILES["export"])
    md.append("2. Took each station's excess over its centred 48-hour running median of valid values.")
    md.append("3. Flagged every step where an excess of 30 nSv/h or more fell by more than half and the next value "
              "stayed below half of it; none occurs outside %s and %s (natural falls stop at %d per cent)." % (
                  c1, c0, f["nat_max_fall_pct"]))
    md.append("4. Walked back from each flagged step over values more than 15 nSv/h above the median; dated each "
              "increase by its start and took its highest ten-minute value.")
    md.append("5. Source checks: each kit's source is the kit register's, except while `%s` has it out: CS-0583 "
              "went out 5 August and back into KIT-2 4 September, so KIT-2 carried the spare CS-0417 (21 August "
              "stock check); certificate in force by date of issue, jig, Cs-137 decay; repeat is the check." %
              pack.FILES["sources"])
    md.append("6. Telemetry: earliest receipt per interval from `%s`, LoRa UK clock converted, against the interval's "
              "end; test-mode (T) values count (the agreement's timeliness clause), F records carry no value; over the quarter's 13,248 "
              "intervals." % pack.FILES["ingest"])
    md.append("7. Air filters: air drawn is `measured_flow_m3_h` in `%s` integrated from filter on to off, the "
              "transmitter's blank RUN rows filled by linear interpolation (the set-flow totaliser and AS2's set-flow "
              "volume do not measure it); latest result version." % pack.FILES["pump"])
    md.append("8. Notified %s and %s with their dates and highest values.\n" % (c1, c0))
    md.append("## 4. Deliverable Answers\n")
    md.append("### artificial_detections_2026Q3.docx\n")
    md.append("1. %s %s: %s; highest ten-minute value %d nSv/h (%s)." % (c1, A["site"], ", ".join(A["dates"]),
                                                                       A["peak"], A["peak_day"]))
    md.append("2. %s %s: %s; highest ten-minute value %d nSv/h (%s)." % (c0, B["site"], ", ".join(B["dates"]),
                                                                       B["peak"], B["peak_day"]))
    md.append("3. No other station recorded an increase of artificial origin.\n")
    md.append("### network_quarter_2026Q3.xlsx\n")
    md.append("1. Source checks, per cent of expected and result:")
    for c, v in f["checks"].items():
        md.append("   - %s (%s): %s, %s" % (c, v["date"], v["pct"], v["result"]))
    md.append("2. Telemetry, per cent of the quarter's intervals received within 60 minutes:")
    md.append("   - " + "; ".join("%s %s" % (c, v) for c, v in f["timely"].items()))
    md.append("3. Gross beta, mBq/m3 by filter:")
    for s in ("AS1", "AS2", "AS3"):
        md.append("   - %s: %s" % (s, "; ".join("%s %s" % (k, v["conc"]) for k, v in f["air"].items()
                                              if v["sampler"] == s)))
    md.append("")
    md.append("### excursion_traces_2026Q3.svg\n")
    md.append("1. One panel per detection day (%d), the ten-minute record from two hours before to two hours after, "
              "the step that ended each increase marked; titled with the %d and %d per cent falls." % (
                  f["detection_days"], f["art_min_fall_pct"], f["nat_max_fall_pct"]))
    open(os.path.join(task_dir, "submission.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
