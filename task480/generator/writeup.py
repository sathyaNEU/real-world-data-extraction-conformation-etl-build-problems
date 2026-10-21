"""submission.md, drafted from generator/figures.json: every figure in it is read from there."""
import json

import world as W


WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
         11: "eleven", 12: "twelve"}


def andlist(xs):
    xs = list(xs)
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def write(figs, out):
    f = json.load(open(figs, encoding="utf-8"))
    c = f["counties"]
    q = f["call"]["counties"]
    order = sorted(W.NAMES, key=lambda x: -c[x]["tons_unrounded"])
    qs = [x for x in order if x in q]
    below = [x for x in order if x not in q]
    r1, r2 = f["rungs"]["R1"]["set"], f["rungs"]["R2"]["set"]
    p = f["pilot"]
    L = ["## Tags", "",
         "**Domain:** Physical & Environmental Sciences (emissions inventory: the 2027 NOx of a nonattainment area's "
         "older gasoline vehicles by county, conformed from the registration snapshot, the inspection program's test "
         "records and the model-year rate table, each vehicle's 2027 miles estimated from its one "
         "odometer reading).",
         "**Analytical objective:** Data Extraction & Conformation (ETL).", ""]
    L += ["## 1. Final Recommendation", "",
          "**Hold 2027 Vehicle Retirement Program intake events in the %s counties whose eligible vehicles will emit %d "
          "short tons of NOx or more in 2027: %s.**" % (WORDS[f["call"]["n"]], int(f["threshold"]), andlist(qs)),
          "Marlbank, the designated county nearest the line, comes to %d tons and Dunmarsh, the nearest below it, to %d. "
          "Not the %s counties the odometer reading divided by the vehicle's age files, which averages every year a car "
          "has been driven and overstates what an old car travels now. Not %s, which the area's mileage by age without "
          "each vehicle's own reading gives, dropping the long-distance drivers of Elkhollow and Marlbank and adding "
          "Dunmarsh." % (c["Marlbank"]["tons"], c["Dunmarsh"]["tons"], WORDS[len(r1)], andlist(r2)), ""]
    L += ["## 2. Critical Components", "",
          "1. Marlbank's eligible vehicles' 2027 NOx: **%d short tons**." % c["Marlbank"]["tons"],
          "2. Dunmarsh's eligible vehicles' 2027 NOx: **%d short tons**." % c["Dunmarsh"]["tons"],
          "3. Counties at 10 tons or more: **%d**." % f["call"]["n"], ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Took the eligible vehicles from vehicle_registrations_2026-07-01.csv under guidelines 2.1 (ACTIVE in a "
          "member county, model year %d to %d, fuel code G or F, GVWR class 1 or 2a): %s vehicles."
          % (W.ELIG_MY + ("{:,}".format(f["totals"]["eligible"]),)),
          "2. Gave each its reading from eip_inspections_2024_2025.csv: its first completed INITIAL test (PASS or FAIL; "
          "0 and 999999 not usable, KM readings in miles), joined by VIN, or by plate and "
          "model year where the typed VIN matches no registration; %s have one." % "{:,}".format(f["totals"]["read"]),
          "3. Fitted the cumulative miles the area's vehicles had travelled by age, a quadratic least-squares fit of every "
          "completed initial reading on age in years from 1 January of the model year (guidelines 3.3).",
          "4. Took each vehicle's 2027 miles as its reading over the curve at its age when tested, times the curve's rise "
          "from its age on 1 January 2027 to its age on 1 January 2028; vehicles without a reading take the average of "
          "their county and model year (3.4).",
          "5. Multiplied by the Table 2 rate in nox_running_rates_cy2027.xlsx for the model year and the class in "
          "registration_body_codes.csv and summed by county in short tons of 907,184.74 grams: %s counties at 10.0 or "
          "more (3.1, 3.2)." % WORDS[f["call"]["n"]],
          "6. Pilot: a voucher in vrp_pilot_vouchers_2025.xlsx whose VIN has an ACTIVE record on the registration "
          "snapshot was not retired (the owner took the vehicle back); each retired vehicle's charge is what the "
          "Calderwick and Thistlebury lines of vrp_pilot_dismantler_invoices_2025.csv bill for its tow_zone (%s), since "
          "Oakhaven's export repeats each invoice's total on every line: %s." % (
              ", ".join("$%d" % f["zone_charges"][z] for z in sorted(f["zone_charges"])), "; ".join(
                  "%s %d vehicles, $%s" % (x, p[x]["retired"], "{:,}".format(p[x]["charges"])) for x in W.PILOT_COUNTIES)),
          "7. Recommended intake events in %s." % andlist(qs), ""]
    L += ["## 4. Deliverable Answers", "", "### %s" % W.GOLDEN["workbook"], "",
          "1. Each county's eligible vehicles' 2027 NOx in short tons to the nearest ton, and whether it qualifies:"]
    for x in order:
        L.append("   - %s: %d; %s" % (x, c[x]["tons"], "qualifies" if c[x]["qualifies"] else "does not qualify"))
    L += ["2. Bar chart of the twelve counties' 2027 NOx with a line at 10 tons, on the Chart sheet.",
          "3. The vehicles the 2025 pilot retired and what the Department paid dismantlers for them:"]
    for x in W.PILOT_COUNTIES:
        L.append("   - %s: %d vehicles; $%s" % (x, p[x]["retired"], "{:,}".format(p[x]["charges"])))
    L += ["", "### %s" % W.GOLDEN["memo"], "",
          "1. The recommendation: intake events in %s." % andlist(qs)]
    open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
