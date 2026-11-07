"""submission.md, every figure carried from figures.json."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P   # noqa: E402

MONTHS = ["April", "May", "June", "July", "August", "September"]


def c(x):
    return "{:,}".format(int(round(x)))


def write(path, f):
    pct = f["share_prevented_pct_nearest5"]
    L = []
    L += ["## Tags", "",
          "> **Domain:** Human Factors & Ergonomics (usability and task performance studies).",
          "> **Analytical objective:** Experiment & Causal Analysis.", ""]
    L += ["## 1. Final Recommendation", "",
          "**Make PROBE-M mandatory at every en-route planner position from 1 April 2027.** Its use prevented about "
          "%d per cent of the STCA activations the six sectors would have raised in the time it was running, against "
          "the 20 per cent the acceptance criteria require, read at the same sector, number of aircraft and number "
          "climbing or descending, minute by minute. Not the Safety Performance Report's rate per 1,000 flight hours "
          "(%.1f with the probe running, %.1f without), which sets the probe's minutes against quieter ones; not a "
          "comparison at like occupancy alone, which leaves the probe's minutes with more climbing and descending "
          "traffic and shows no benefit." % (pct, f["rate_on_per_1000fh"], f["rate_off_per_1000fh"]), ""]
    L += ["## 2. Critical Components", "",
          "1. Activations counted as the Safety Performance Report counts them over the trial: **%s**, of which **%s** "
          "in the probe's running time, **%s** of those at combinations of sector, number of aircraft and number "
          "climbing or descending that also occur without the probe." % (
              c(f["activations_counted"]), c(f["observed_all"]), c(f["observed"])),
          "2. At the same sector, number of aircraft and number climbing or descending, minute by minute, the probe "
          "prevented about **%d per cent** of the activations its running time would have raised, above the "
          "criterion's 20 per cent." % pct,
          ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Took each flight's latest plan revision from fdps_sector_crossings_2026-04_2026-09.csv (a revision "
          "re-issues the flight's whole crossing list) and counted, for each sector and minute, the aircraft in the "
          "sector and those whose entry and exit levels differ.",
          "2. Marked the minutes with the probe running from probe_m_planner_workstation_log_2026-04_2026-09.csv, New "
          "Zealand time taken to UTC, a combined position's display covering both sectors (the acceptance criteria).",
          "3. Counted the activations in stca_activations_2026-04_2026-09.csv as the Safety Performance Report counts "
          "them (live only, once per event in the sector where it began, a combined-sector activation in the sector "
          "of the first-named aircraft): %s." % c(f["activations_counted"]),
          "4. Applied the activation rate of the minutes without the probe, at each sector, number of aircraft and "
          "number climbing or descending, to the probe's running minutes at combinations that also occur without "
          "it: %s expected against %s raised in them." % (c(f["expected"]), c(f["observed"])),
          "5. Took the share prevented, about %d per cent, against the acceptance criteria's one in five." % pct,
          "6. For the tables, split each flown crossing at New Zealand month ends, counted each month's activations "
          "per 1,000 flight hours in the sector where each began, and counted each flight once in each sector it "
          "entered.",
          "7. Recommended making PROBE-M mandatory from 1 April 2027.", ""]
    L += ["## 4. Deliverable Answers", "", "### probe_decision_2027.docx", "",
          "1. Recommendation: make PROBE-M mandatory at every en-route planner position from 1 April 2027.",
          "2. The share its use prevented: about %d per cent of the STCA activations the sectors would have raised in "
          "its running time (criterion 20 per cent)." % pct,
          "3. Chart: the share of minutes with the probe running by the number of aircraft climbing or descending in "
          "the sector, beside the activations in the probe's running time as raised and as the same traffic raised "
          "without it.", "", "### probe_trial_figures.xlsx", "",
          "1. Flight hours by sector and month, New Zealand time, whole hours:"]
    for s in P.SECTORS:
        L.append("   - %s: %s" % (s, ", ".join("%s %s" % (m, c(v)) for m, v in zip(MONTHS, f["flight_hours"][s]))))
    L.append("2. STCA activations per 1,000 flight hours by sector and month, one decimal:")
    for s in P.SECTORS:
        L.append("   - %s: %s" % (s, ", ".join("%s %.1f" % (m, v) for m, v in zip(MONTHS, f["stca_rate"][s]))))
    L.append("3. Flights handled over the trial, whole flights:")
    for s in P.SECTORS:
        L.append("   - %s: %s" % (s, c(f["flights_handled"][s])))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
