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


def write(f, path):
    hi = f["call"]["high_use"]
    plain = f["plain_expansion"]["set"]
    out = [n for n in plain if n not in hi]
    came = [n for n in hi if n not in plain]
    ah = f["angler_hours_per_ha"]
    ph = f["plain_expansion"]["per_ha"]
    low_in = min(hi, key=lambda n: ah[n])
    high_out = max((n for n in ah if n not in hi), key=lambda n: ah[n])
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
      "is read against the hours that lake's own anglers fish: %s is the lowest of them at %s, and the highest lake "
      "left standard is %s at %s. Not the plain expansion's list: each count times the 17-hour day puts %s in and "
      "leaves %s out, because the flights pass every lake between about 09:30 and 17:00, the general lakes' busy "
      "hours and the fly-only lakes' quiet ones."
      % (listing(hi), short(low_in), "{:,}".format(ah[low_in]), short(high_out), "{:,}".format(ah[high_out]),
         listing(out), listing(came)))
    a("")
    a("## 2. Critical Components\n")
    a("1. Each lake is counted at the time its place on the Vellacott route brings the aircraft over it, so every "
      "count falls between about 09:30 and 12:00 or 14:30 and 17:00; the interviews' start and finish times show "
      "the fly-only lakes fished mostly at dawn and dusk and the general lakes through the middle of the day.")
    a("2. Each count is divided by the share of that lake's interviewed angler-hours falling in the hour it was made "
      "(boats times the lake's own anglers per boat, plus shore anglers), averaged by survey day and expanded by "
      "weekday and weekend day in each month, then divided by the register's area.")
    a("3. %s come in at %s angler-hours per hectare; %s fall to %s." % (
        listing(came), ", ".join("{:,}".format(ah[n]) for n in came), listing(out),
        ", ".join("{:,}".format(ah[n]) for n in out)))
    a("4. The plain expansion gives %s %s and %s %s; spreading the counts by the survey's pooled hourly profile "
      "leaves that list unchanged." % (
        listing(out), ", ".join("{:,}".format(ph[n]) for n in out), listing(came),
        ", ".join("{:,}".format(ph[n]) for n in came)))
    a("")
    a("## 3. Step-by-Step Solution\n")
    a("1. Matched survey_flight_counts_2026.csv (Vellacott numbers) and creel_interviews_2026.csv (tablet names) to "
      "lake_register_2026.xlsx, dropped the loops and lakes entered with no count, and took a start of finish less "
      "hours fished where an interview gives no start.")
    a("2. Turned each count into anglers: boats times the lake's mean party size among boat parties, plus shore "
      "anglers.")
    a("3. For each lake, shared every interviewed party's anglers over the hours of 05:00 to 22:00 it fished and "
      "took each hour's share of the lake's interviewed angler-hours.")
    a("4. Divided each count by its lake's share for the hour of the count, averaged the counts of each survey day, "
      "took the mean survey day in each month's weekday and weekend strata, multiplied by the stratum's days and "
      "summed over 15 May to 31 August.")
    a("5. Divided by the register's surface area and set each lake that takes catchables against 500 "
      "(catchable_allocation_policy_2026.pdf, 2.2 and 2.3).")
    a("6. Releases: each trip's net load at its raceway's latest Monday sample count (fish per kg), reading trip "
      "sheet raceway numbers before the tank temperature column began as the old numbers "
      "(quillet_creek_raceway_numbers.csv), shared between drops by the drop crew's nets, less the dead at the drop.")
    a("7. Warm days: assigned each logger reading to the deployment its serial was in at that moment "
      "(logger_deployments_2026.csv), put loggers 20184409 and 20184421 from UTC onto Pacific time, and counted the "
      "July and August days whose 1 m readings averaged above 20 C.")
    a("8. Recommended the ten lakes above for the high-use tier.")
    a("")
    a("## 4. Deliverable Answers\n")
    a("### stocking_tiers_2027.xlsx\n")
    a("1. High-use tier for 2027: %s; standard: %s." % (listing(hi), listing(f["call"]["standard"])))
    a("2. Angler-hours per hectare, 2026 open-water season, nearest 10:")
    for n in sorted(ah, key=lambda n: -ah[n]):
        a("   - %s: %s (%s)" % (short(n), "{:,}".format(ah[n]), f["tier"][n]))
    a("3. Catchable rainbow trout released alive in 2026, nearest 100:")
    for n, v in sorted(f["releases_alive"].items()):
        a("   - %s: %s" % (short(n), "{:,}".format(v)))
    a("4. Days in July and August with the 1 m water averaging above 20 C (Pacific-time days):")
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
