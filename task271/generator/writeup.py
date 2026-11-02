"""Writes submission.md from figures.json, so every figure in blocks 1 to 4 is one the generator computed."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def short(n):
    return n.replace(" Lake", "")


def listing(names):
    names = [short(n) for n in names]
    return ", ".join(names[:-1]) + " and " + names[-1]


def listing_or(names):
    names = [short(n) for n in names]
    return ", ".join(names[:-1]) + " or " + names[-1]


def write(f, path):
    hi = f["call"]["high_use"]
    plain = f["plain_expansion"]["set"]
    out = [n for n in plain if n not in hi]
    came = [n for n in hi if n not in plain]
    b = f["bands"]
    nh, ns = f["nearest_high"], f["nearest_standard"]
    L = []
    a = L.append
    a("## Tags\n")
    a("**Domain:** Survey Research & Official Statistics (sample design, allocation and weighting: a lake-stocking "
      "society's creel survey, each lake's open-water angler-hours per hectare expanded from route-timed aerial "
      "counts).")
    a("**Analytical objective:** Descriptive & Distribution Analysis.\n")
    a("## 1. Final Recommendation\n")
    a("**Put %s into the 2027 high-use tier; every other lake that takes catchables stays standard.** Each of the "
      "ten was fished for more than 500 angler-hours per hectare from 15 May to 31 August 2026 once each flight count "
      "is read against the hours that lake's own anglers fish, and it stays above %d however a count's time is read "
      "against those hours and whatever party size turns its boats into anglers; the standard lakes stay below %d. "
      "Depending on that reading, the high-use lake nearest the line is %s, and the standard lake nearest it %s. Not "
      "the plain expansion's list: with each lake's own anglers per boat, each count times the 17-hour day puts %s in "
      "and leaves %s out, because the flights pass every lake between about 09:30 and 17:00, the general lakes' busy "
      "hours and the fly-only lakes' quiet ones."
      % (listing(hi), b["high_use_above"], b["standard_below"], listing_or(nh), listing_or(ns), listing(out),
         listing(came)))
    a("")
    a("## 2. Critical Components\n")
    a("1. Each lake is counted at the time its place on the Vellacott route brings the aircraft over it, so every "
      "count falls between about 09:30 and 12:00 or 14:30 and 17:00; the interviews' start and finish times show "
      "the fly-only lakes fished mostly at dawn and dusk and the general lakes through the middle of the day.")
    a("2. Each count is divided by the share of that lake's interviewed angler-hours present at the time it was made "
      "(boats times the lake's own anglers per boat, plus shore anglers), averaged by survey day and expanded by "
      "weekday and weekend day in each month, then divided by the register's area.")
    a("3. %s come in above %d angler-hours per hectare and %s fall below %d, whether a count's time is read by its "
      "hour, the nearest hour, interpolated, over the hour around it or at its minute, with each lake's own hours or "
      "its regulation class's, and with the lake's own, its class's or one shared party size."
      % (listing(came), b["high_use_above"], listing(out), b["standard_below"]))
    a("4. With each lake's own anglers per boat, the plain expansion puts %s over 500 and leaves %s under it, whether "
      "the blank counts are left out or read as zero and with or without the strata; spreading the counts by the "
      "survey's pooled hourly profile leaves that list unchanged." % (listing(out), listing(came)))
    a("")
    a("## 3. Step-by-Step Solution\n")
    a("1. Matched survey_flight_counts_2026.csv (Vellacott numbers) and creel_interviews_2026.csv (tablet names) to "
      "lake_register_2026.xlsx, left out the loop and the lakes entered with no count, and where an interview gives no "
      "start took the finish less the hours fished.")
    a("2. Turned each count into anglers: boats times the lake's mean party size among boat parties, plus shore "
      "anglers.")
    a("3. For each lake, shared every interviewed party's anglers over the hours of 05:00 to 22:00 it fished and "
      "took each hour's share of the lake's interviewed angler-hours.")
    a("4. Divided each count by its lake's share for the hour of the count, averaged the counts of each survey day, "
      "took the mean survey day in each month's weekday and weekend strata, multiplied by the stratum's days and "
      "summed over 15 May to 31 August.")
    a("5. Divided by the register's surface area and set each lake that takes catchables against 500 "
      "(catchable_allocation_policy_2026.pdf, 2.2 and 2.3); every other reading of a count's time against the hours, "
      "and any party size, keeps each high-use lake above %d and each standard lake below %d."
      % (b["high_use_above"], b["standard_below"]))
    a("6. Releases: each trip's net load at its raceway's latest Monday sample count (fish per kg), reading trip "
      "sheet raceway numbers before the tank temperature column began as the old numbers "
      "(quillet_creek_raceway_numbers.csv), shared between drops by the drop crew's nets, less the dead fish counted "
      "at the drop.")
    a("7. Warm days: assigned each logger reading to the deployment its serial was in at that moment "
      "(logger_deployments_2026.csv), put loggers %s and %s from UTC onto Pacific time, and counted the "
      "July and August days whose 1 m readings averaged above 20 C." % tuple(f["utc_loggers"]))
    a("8. Recommended the ten lakes above for the high-use tier.")
    a("")
    a("## 4. Deliverable Answers\n")
    a("### stocking_tiers_2027.xlsx\n")
    a("1. High-use tier for 2027: %s." % listing(hi))
    a("2. Standard: %s." % listing(f["call"]["standard"]))
    a("3. Angler-hours per hectare, 2026 open-water season: every high-use lake above %d and every standard lake "
      "below %d, under every reading of the counts against the lakes' hours." % (b["high_use_above"], b["standard_below"]))
    a("4. Catchable rainbow trout released alive in 2026, nearest 100:")
    for n, v in sorted(f["releases_alive"].items()):
        a("   - %s: %s" % (short(n), "{:,}".format(v)))
    a("5. Days in July and August with the 1 m water averaging above 20 C (Pacific-time days):")
    for n, v in sorted(f["warm_days"].items()):
        a("   - %s: %d" % (short(n), v))
    a("")
    a("### stocking_board_note_2027.docx\n")
    a("1. Recommendation: %s into the 2027 high-use tier; every other lake standard." % listing(hi))
    a("2. Chart: a bar for each lake's angler-hours per hectare against the 500 line, the high-use lakes shaded "
      "dark.")
    a("")
    with open(path, "w") as fh:
        fh.write("\n".join(L))


if __name__ == "__main__":
    write(json.load(open(os.path.join(HERE, "figures.json"))), os.path.join(TASK, "submission.md"))
