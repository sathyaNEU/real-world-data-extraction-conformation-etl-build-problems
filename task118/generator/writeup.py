"""task118 submission.md, written from figures.json (every figure emitted, none typed)."""
import datetime as dt

ORDER = ("Home Battery Network", "Peak Time Rewards", "Cool Credit", "Business Demand Partners")
MONTH = {"2026-06": "June", "2026-07": "July", "2026-08": "August", "2026-09": "September"}


def _day(s):
    d = dt.date.fromisoformat(s)
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)


def _kw(x, nd):
    return ("%%.%df" % nd) % x


def write(path, fig):
    mw, u, pu = fig["mw"], fig["units"], fig["per_unit_kw_fourth_day"]
    r0 = fig["ladder"]["R0 ex post, every event"]
    a = fig["ask_a"]
    fd = [_day(x) for x in fig["fourth_days"]["Cool Credit"]]
    lines = []
    lines += ["## Tags", "",
              "**Domain:** Energy Systems & Utilities (generation capacity planning).",
              "**Analytical objective:** Opportunity Sizing & Decision Support.", ""]
    lines += ["## 1. Final Recommendation", "",
              "**The USD 3.2 million expansion line should go to the Home Battery Network, which adds %d MW to the "
              "2027 accredited capacity against %d MW for Peak Time Rewards, the runner-up.** The deciding figure is "
              "each programme's 18:00 reduction on the fourth consecutive event day, where the design year's peak "
              "hour falls. Not Cool Credit, which leads on the record's average event at %d MW but adds %d MW in "
              "that hour; not Business Demand Partners, at %d MW."
              % (mw["Home Battery Network"], mw["Peak Time Rewards"], round(r0["Cool Credit"]), mw["Cool Credit"],
                 mw["Business Demand Partners"]), ""]
    lines += ["## 2. Critical Components", "",
              "1. The system peak hour of the design year, the hour beginning 18:00 MST on 23 July 2027, is the "
              "**fourth** consecutive weekday OP-7 calls.",
              "2. The budget buys **{:,}** batteries, **{:,}** rebate customers, **{:,}** thermostat premises or "
              "**{:,}** commercial sites.".format(u["Home Battery Network"], u["Peak Time Rewards"], u["Cool Credit"],
                                                  u["Business Demand Partners"]),
              "3. Accredited capacity added: Home Battery Network **%d MW**, Peak Time Rewards **%d MW**, Cool Credit "
              "**%d MW**, Business Demand Partners **%d MW**." % tuple(mw[p] for p in ORDER), ""]
    am = fig["ask_b_months"]
    cm = fig["ask_c_months_whole"]
    lines += ["## 3. Step-by-Step Solution", "",
              "1. Took the hour of highest forecast load in appendix_b_design_year_2027.csv (the hour beginning "
              "18:00 on 23 July 2027) and applied OP-7's trigger (a weekday whose forecast high reaches 110F) to "
              "the design year's daily highs: 20 to 23 July are called, so the peak hour is the fourth event day "
              "in a row.",
              "2. Rebuilt each event date's run day from dr_event_log_2024-2026.csv as consecutive calendar days "
              "with an event: the record's fourth days are %s, %s and %s." % tuple(fd),
              "3. Read each programme's reduction per enrolled unit in the hour beginning 18:00 MST: holdout less "
              "treatment mean kWh in ridgeway_cool_credit_panel_2024-2026.csv (UTC less seven hours), holdout less "
              "alerted mean kW in ridgeway_peak_time_rewards_2024-2026.csv, the mean verified site reduction in "
              "ridgeway_business_demand_partners_2024-2026.csv, and discharge over enrolled batteries in "
              "brightwell_fleet_event_summary_2024-2026.csv under the 3.0 kW setting of schedule 2.",
              "4. Averaged each over its fourth days (%s kW a Cool Credit premise, %s kW a rebate customer, %s kW a "
              "site, %s kW a battery) and multiplied by the whole units dr_expansion_costs_2027.xlsx's all-in costs "
              "buy: the Home Battery Network %d MW, Peak Time Rewards %d, Cool Credit %d, Business Demand Partners %d."
              % (_kw(pu["Cool Credit"], 3), _kw(pu["Peak Time Rewards"], 4), _kw(pu["Business Demand Partners"], 1),
                 _kw(pu["Home Battery Network"], 2), mw["Home Battery Network"], mw["Peak Time Rewards"],
                 mw["Cool Credit"], mw["Business Demand Partners"]),
              "5. Counted, for each 2026 event day, the premises in cool_credit_enrolments_cis_2026-10-16.csv "
              "enrolled that day with a thermostat online at 23:00 UTC: the enrolled serial or a device registered "
              "in halvern_device_registry_2026-10-16.json at the same address once both are normalised, "
              "its last row in halvern_status_changes_2026.csv ONLINE, or IDLE from 7 July 2026, the first event "
              "on which halvern_unreachable_devices_2026.csv stops listing idle devices.",
              "6. Dropped exact repeats from brightwell_dispatch_records_2026.csv, added each battery's record hours "
              "for an event (the MST date of the dispatch start), counted a premise in "
              "battery_interconnection_register_2026-10-16.csv once per event when any of its batteries reached "
              "three hours, and paid USD 15 an event in event order up to USD 255.",
              "7. Kept the latest submitted row per meter and month in arroyo_nominations_2026.csv for meters in "
              "cbmu_commercial_meters_2026-10-16.csv and summed nominated kW by month.",
              "8. Recommended the Home Battery Network, %d MW ahead of Peak Time Rewards."
              % (mw["Home Battery Network"] - mw["Peak Time Rewards"]), ""]
    lines += ["## 4. Deliverable Answers", "", "### dr_capacity_note_2027.docx", "",
              "1. Recommendation: expand the Home Battery Network with the USD 3.2 million.",
              "2. Accredited capacity each programme's expansion adds in the 2027 system peak hour, whole "
              "megawatts:"]
    for p in ORDER:
        lines.append("   - %s: %d MW" % (p, mw[p]))
    lines += ["3. Runner-up: Peak Time Rewards.",
              "4. A bar chart of each programme's megawatts sits under the table on page 1 of the note.", "",
              "### dr_programme_audit_2026.csv", "",
              "5. Cool Credit enrolled premises with a thermostat online at 16:00, each 2026 event day, whole "
              "premises:"]
    for d, v in a.items():
        lines.append("   - %s: {:,}".format(v) % _day(d))
    lines.append("6. Home Battery Network incentive owed by 2026 event month, nearest dollar:")
    for m, v in am.items():
        lines.append("   - %s: USD {:,}".format(v) % MONTH[m])
    lines.append("7. Home Battery Network premises that reached the season cap: {:,}".format(fig["ask_b_capped"]))
    lines.append("8. Business Demand Partners nominated capacity by month, whole kilowatts:")
    for m, v in cm.items():
        lines.append("   - %s 2026: {:,} kW".format(v) % MONTH[m])
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
