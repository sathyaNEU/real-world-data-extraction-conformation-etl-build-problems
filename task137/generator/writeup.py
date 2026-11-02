"""submission.md from figures.json: tags, the call, the components, at most eight steps, the deliverable answers."""
import golden as GD

QN = {"2025Q1": "January to March 2025", "2025Q2": "April to June 2025", "2025Q3": "July to September 2025",
      "2025Q4": "October to December 2025", "2026Q1": "January to March 2026", "2026Q2": "April to June 2026"}


def money(x):
    return "£{:,}".format(x)


def write(path, F):
    bt = F["backtest"]
    rc = F["repair_cost_by_depot"]
    a = F["recoveries_by_collision_quarter"]
    L = []
    L += ["## Tags", "",
          "**Domain:** Actuarial Science & Insurance (claims frequency and severity: a self-insured delivery fleet's "
          "collision claims for a year on a new route schedule, priced per kilometre on clock time and light).",
          "**Analytical objective:** Forecasting & Predictive Modeling.", ""]
    L += ["## 1. Final Recommendation", "",
          "**The delivery trucks will make %d collision claims in 2027: %d from April to September and %d in the other "
          "six months.**" % (F["claims_2027"], F["claims_2027_apr_sep"], F["claims_2027_other_months"]),
          "The 2027 schedule drives %.1f per cent of its kilometres before sunrise or after sunset, against %.1f per cent "
          "in the record, at about %.1f times the daylight collision rate at the same clock time. Not %d, the record's "
          "rate per kilometre by time of day, which prices the small hours at the summer schedule's daylight rate." % (
              F["dark_km_share_2027_pct"], F["dark_km_share_record_pct"], F["dark_multiplier_1dp"],
              F["default_path_2027"]), ""]
    L += ["## 2. Critical Components", "",
          "1. Kilometres planned for 2027 driven before sunrise or after sunset (driver handbook Appendix C, UK clock "
          "time): **%.1f per cent**, against **%.1f per cent** of the kilometres driven October 2023 to September 2026" % (
              F["dark_km_share_2027_pct"], F["dark_km_share_record_pct"]),
          "2. A kilometre driven in the dark carries about **%.1f times** the collision rate of a daylight kilometre in "
          "the same clock band" % F["dark_multiplier_1dp"], ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Read both Gridtrak exports (miles to kilometres, the overlap week once, UTC to UK clock time by the "
          "handbook's summer-time rule) with each truck's depot from fleet_register_2026-10.xlsx, to 30 September 2026.",
          "2. Took the trucks' claims from ravensby_fleet_claims_listing_2026-10-31.xlsx per the fund terms (cars, "
          "duplicates and withdrawn notifications out) to 30 September 2026: %d claims." % F["claims_in_record"],
          "3. Spread each run's kilometres evenly over its clock hours and split them at its depot's sunrise and sunset "
          "from driver_handbook_2026.pdf Appendix C: %.1f per cent of the record's kilometres in the dark." % (
              F["dark_km_share_record_pct"]),
          "4. Fitted a Poisson rate per kilometre on clock band and light: a dark kilometre at %.1f times a daylight one; "
          "the 04:00 to 07:00 dark kilometres of the May to August schedule had %d claims against %.1f expected by "
          "that model "
          "fitted without them and %.1f at the 04:00 to 07:00 rate." % (
              F["dark_multiplier_1dp"], bt["claims"], bt["expected_light_model"], bt["expected_band_rate"]),
          "5. Carried the rates onto every route and delivery day of route_schedule_2027.xlsx: %.1f claims, %.1f of them "
          "from April to September and %.1f in the other six months." % (F["claims_2027_unrounded"],
                                                                        F["claims_2027_apr_sep_unrounded"],
                                                                        F["claims_2027_other_months_unrounded"]),
          "6. Counted each Brantwick invoice once in ap_ledger_brantwick_2023-10_2026-10.csv: identical lines (job, "
          "invoice date, description, net) are one invoice posted twice, except two identical ADAS calibration lines on "
          "a job for a truck the register shows with camera and radar, which are one per sensor; summed net by the "
          "truck's depot and the collision's incident date through brantwick_jobs_2023-10_2026-10.csv.",
          "7. Placed each other insurer's receipt in claims_recovery_account_2024-10_2026-10.csv on its collision: by our "
          "claim number where quoted, else on the one claim of that payer whose net repair cost, in full for a "
          "non-fault claim or at a quarter, a third, a half, two thirds or three quarters for a split one, equals the "
          "amount to the penny; summed by the collision's quarter.",
          "8. The fund should be set for %d collision claims in 2027." % F["claims_2027"], ""]
    L += ["## 4. Deliverable Answers", "", "### %s" % GD.XLSX, "",
          "1. Collision claims in 2027: %d" % F["claims_2027"],
          "2. April to September: %d; January to March and October to December: %d" % (
              F["claims_2027_apr_sep"], F["claims_2027_other_months"]),
          "3. Paid back by other insurers towards each quarter's collisions, received to 31 October 2026:"]
    for k in ("2025Q1", "2025Q2", "2025Q3", "2025Q4", "2026Q1", "2026Q2"):
        L.append("   - %s collisions: %s" % (QN[k], money(a[k])))
    L.append("4. Brantwick repair cost of each depot's collisions:")
    for code, name in GD.DEPOTS:
        L.append("   - %s: %s for January to June 2025 collisions, %s for July to December 2025 collisions, %s for "
                 "January to June 2026 collisions" % (name, money(rc["%s 2025H1" % code]), money(rc["%s 2025H2" % code]),
                                                      money(rc["%s 2026H1" % code])))
    L += ["", "### %s" % GD.DOCX, "",
          "1. One-page note to the board giving %d claims for 2027, split between April to September and the other six "
          "months, with the reason (the new schedule's dark early hours from October to March)" % F["claims_2027"],
          "2. Chart of collision claims by month of incident, October 2023 to September 2026 in blue and the months of "
          "2027 in orange as expected on the new schedule", ""]
    open(path, "w", encoding="utf-8").write("\n".join(L))
