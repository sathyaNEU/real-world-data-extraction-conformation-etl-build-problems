"""submission.md, drafted from figures.json.

    python3 task310/generator/writeup.py
"""
import json
import os

import params as P

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
NAMES = [P.REGIONS[r] for r in P.REGION_ORDER]


def c(n):
    return "{:,}".format(int(n))


def text(F):
    order = sorted(F["schedule"], key=lambda n: F["schedule"][n])
    call, ru = F["call"], F["runner_up"]
    kw, mw = F["kwh_per_battery"], F["round_mwh"]
    L = []
    L += ["## Tags", "",
          "**Domain:** Energy systems and utilities (generation capacity planning).",
          "**Analytical objective:** Opportunity sizing and decision support.", ""]
    L += ["## 1. Final Recommendation", "",
          "**Run the 2027 round in %s, then %s in 2028, %s in 2029 and %s in 2030: the 2027 round would deliver about "
          "%s MWh a year to its homes, %s kWh a battery.**" % (call, order[1], order[2], order[3], c(mw[call]),
                                                                c(kw[call])),
          "Not %s first: it leads only on the readings as recorded, because the %s estate homes' inverters held their "
          "output to the home's use plus the 0.5 kW export limit, and a battery would take the energy they held back."
          % (ru, call), ""]
    L += ["## 2. Critical Components", "",
          "1. Energy a programme battery would deliver to a home in a year (kWh): %s." %
          "; ".join("%s **%s**" % (n, c(kw[n])) for n in order),
          "2. Each round's yearly energy (MWh): %s." % "; ".join("%s **%s**" % (n, c(mw[n])) for n in order),
          "3. Round years: %s." % "; ".join("%s **%d**" % (n, F["schedule"][n]) for n in order), ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Built each panel home's 2025 hours in market time (UTC+10): solar from velkora_portal_hourly_2025.parquet "
          "(local hour-beginning with its UTC offset) and ondrava_cloud_counters_2025.csv (lifetime counters at local "
          "hour end, differenced, the clock moving at 03:00 on 6 April and 02:00 on 5 October, a replacement "
          "inverter's counter from zero), and general-supply use as solar plus E1 less B1 from "
          "southmark_meter_halfhours_2025.parquet (reads stamped at the end of the half hour; E2, the controlled load, "
          "left out per guideline Appendix A).",
          "2. Read each home's limit in southmark_connection_register_panel.csv: the %d Yarrandale Valley homes on "
          "MEG-CZ05 (0.5 kW) and %d Eastbrook Metro homes on MEG-L15 (1.5 kW) export no more than their limit and "
          "their inverters hold output to use plus the limit, so their recorded solar falls short of what their arrays "
          "produced." % (F["limited_homes"]["Yarrandale Valley"], F["limited_homes"]["Eastbrook Metro"]),
          "3. Rebuilt each limited home's solar hour by hour as its array kWp (hemp_solar_systems_2025.xlsx) times the "
          "median output per kWp of its region's unlimited homes that hour, capped at its inverter's AC rating and "
          "never below what it recorded.",
          "4. Ran the programme battery (10 kWh usable, 5 kW, 95 per cent stored on charge and 95 per cent delivered "
          "on discharge, empty on 1 January) hour by hour on each home's solar and general-supply use, charging only "
          "from solar beyond use and discharging only to use; averaged each region's 40 homes, multiplied by 2,400 "
          "and ordered the rounds by that value (guideline sections 3 and 4).",
          "5. Eligible homes: residential NMIs in southmark_der_register_2026-09-30.csv with an active PV row and no "
          "active battery on 30 September 2026, solar connected by 30 September 2025 dated from the earliest PV row "
          "of the NMI and of the NMI it replaced (previous_nmi in southmark_nmi_standing_data_2026-09-30.csv; a "
          "reissue re-dates the rows and a replaced system ran until its successor), less premises with a Paid "
          "Battery Booster claim, matched by the claim's NMI followed to the current one or, for claims lodged before "
          "July 2022 that carry none, by normalised address, suburb and postcode.",
          "6. Pilot energy: dropped re-sent telemetry rows (same serial and date), read each battery's lifetime "
          "counter at each quarter end (a replacement unit from zero), and counted the 24 homes whose two units "
          "report identical energy and counters every day (one Duo meter) once, while homes with two separately "
          "metered units count both.",
          "7. Installations: collapsed module rows to certificates, applied the withdrawals and installer corrections "
          "in the amendments, took certificates sharing module serials as one installation (the later lodgement), "
          "matched A numbers through previous_no in the accreditation register, kept installers Current with expiry "
          "on or after 31 December 2027, and placed each installation by suburb (postcodes 2716 and 2905 span two "
          "regions).",
          "8. Recommended %s for 2027, the largest yearly round energy." % call, ""]
    L += ["## 4. Deliverable Answers", "", "### battery_rounds_2027_2030.xlsx", "",
          "1. Round years: %s." % "; ".join("%d %s" % (F["schedule"][n], n) for n in order),
          "2. Energy a programme battery would deliver to a home in a year (kWh, nearest 50):"]
    for n in order:
        L.append("   - %s: %s" % (n, c(kw[n])))
    L.append("3. Each round's yearly energy (MWh, nearest 100):")
    for n in order:
        L.append("   - %s: %s" % (n, c(mw[n])))
    L.append("4. Homes eligible for the 2027 round on 30 September 2026:")
    for n in NAMES:
        L.append("   - %s: %s" % (n, c(F["ask_a"][n])))
    L.append("5. Energy the 2024 pilot batteries delivered to their homes in each quarter of 2025 (MWh, one decimal):")
    for q, v in F["ask_b"].items():
        L.append("   - %s: %.1f" % (q, v))
    L.append("6. Batteries installed in 2025 by installers accredited for the whole of 2027:")
    for n in NAMES:
        L.append("   - %s: %s" % (n, c(F["ask_c"][n])))
    L += ["", "### round_yield_by_region.png", "",
          "1. Bar chart of each round's yearly energy in round order, %s's 2027 bar the tallest and highlighted." % call,
          "", "### minister_brief_battery_rounds.pdf", "",
          "1. Recommendation: run the rounds %s; the 2027 round about %s MWh a year." %
          (", ".join("%s %d" % (n, F["schedule"][n]) for n in order), c(mw[call])), ""]
    return "\n".join(L)


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    open(os.path.join(TASK, "submission.md"), "w").write(text(F))


if __name__ == "__main__":
    main()
