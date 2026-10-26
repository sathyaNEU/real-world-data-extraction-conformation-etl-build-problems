"""submission.md, every figure from figures.json."""
import figs as FG


def n(x):
    return "{:,}".format(x)


WORD = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
        11: "eleven", 12: "twelve"}


def band(F, k):
    return "%s to %s" % (n(F[k + "_low"]), n(F[k + "_high"]))


def write(path, F):
    h = F["hospital_visits_2025_26"]
    sk = F["sickness_by_quarter"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Healthcare delivery and health economics (utilization, access and demand forecasting).")
    L.append("**Analytical objective:** Forecasting and predictive modelling.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Plan for %s GP-referred visits at the community phlebotomy hub in 2027-28.**" % n(F["plan_visits_2027_28"]))
    L.append("Underlying 2025-26 GP-referred demand was about %s visits, about %s more than the walk-in clinic saw "
             "or turned away, because practices with their own phlebotomy clinics kept patients in-house for %s weeks "
             "after the clinic's run-out weeks; grown 3.5 per cent a year for two years it is about %s. Not %s, from "
             "2025-26's seen plus turned away (%s grown), which leaves out the patients the practices kept, or from a "
             "model of the previous week's run-outs or ten days of them, which sees only the start of the fall. Not %s, "
             "from the patients seen alone, which also leaves out the patients turned away.\n"
             % (band(F, "base_2025_26"), band(F, "kept_in_house"), WORD[F["window_weeks"]], band(F, "plan_unrounded"),
                n(F["default_path_plan"]), n(F["gp_arrivals_2025_26"]), n(F["seen_only_plan"])))
    L.append("## 2. Critical Components\n")
    L.append("1. GP-referred visits seen in 2025-26: **%s**." % n(F["gp_seen_2025_26"]))
    L.append("2. GP-referred patients turned away in 2025-26: **%s**, on **%s** of %s clinic days the tickets ran out."
             % (n(F["gp_turned_away_2025_26"]), F["run_out_days_2025_26"], F["clinic_days_2025_26"]))
    L.append("3. How long the run-outs hold GP-referred arrivals down, the window the record's fit picks from one to "
             "twelve weeks: **%s weeks**." % WORD[F["window_weeks"]])
    L.append("4. 2025-26 underlying GP-referred demand, with that window's run-outs taken out: **about %s**.\n"
             % band(F, "base_2025_26"))
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Counted each clinic day's GP-form and hospital-form visits from walkin_tickets_legacy_2023-04_to_2024-11.csv "
             "(Outcome Seen) to 17 November 2024 and from the CHECKED_IN events in phlebotomy_queue_events_2024-11-18_to_2026-09-30.csv "
             "(UTC read as UK time) from 18 November 2024: %s GP-referred visits seen in 2025-26." % n(F["gp_seen_2025_26"]))
    L.append("2. Read both layouts of reception_turned_away_log.xlsx (the GP and hospital boxes of both shifts in the 2023-24 and 2024-25 sheets, "
             "one line per run-out day from 2025-26, month totals left out): %s GP-form patients turned away on %s "
             "clinic days in 2025-26." % (n(F["gp_turned_away_2025_26"]), F["run_out_days_2025_26"]))
    L.append("3. Took each Monday-to-Friday week's run-out share (its logged run-out days over its clinic days) and "
             "modelled each clinic day's GP-referred arrivals (seen plus turned away), April 2023 to September 2026, as "
             "Poisson in weekday, month, a linear trend, the day after a bank holiday and the mean share of the previous "
             "L weeks, L from one to twelve by AIC: %s weeks, every window of five weeks or fewer at least %d worse, "
             "coefficient about %.2f (standard error %.3f), the fall sitting with the practices whose "
             "phlebotomy_les_2025-26 is Y in gp_practices_catchment.csv."
             % (WORD[F["window_weeks"]], F["aic_gap_five_weeks_or_fewer"], F["coef_about"], F["coef_se"]))
    L.append("4. Took the GP-referred arrivals of every clinic day of 2025-26 with that effect removed: about %s visits "
             "(the %s-week window and the %s-week window next to it in fit), grown 3.5 per cent a year for two years to "
             "about %s, %s to the nearest 2,500."
             % (band(F, "base_2025_26"), WORD[F["window_weeks"]], WORD[F["window_runner_up_weeks"]],
                band(F, "plan_unrounded"), n(F["plan_visits_2027_28"])))
    L.append("5. Named each 2025-26 hospital request's clinic code: forms issued before 16 March 2026 carry the old PAS's "
             "codes, which outpatient_clinic_codes.csv does not hold, and each old code is the new code whose forms issued "
             "in the second half of March 2026 fall on the same weekdays as the old code's, before the clinics changed "
             "their sessions in April (the register's clinic_days name all seven wrongly); then counted hospital-form "
             "visits by specialty and financial quarter of the visit date.")
    L.append("6. Counted sickness in eroster_phlebotomy_2023-04_to_2026-09.csv as the holders' Sickness lines plus the "
             "lines shown unassigned (Vacant line Y) from a sickness's sixth clinic day until the same holder returns, which "
             "are filled posts, the one vacant post being the post the annual report names (vacant from 14 July to 12 "
             "September 2025, as section 4 states); working days lost at 7.5 hours each and the rate over every clinic day "
             "of every filled post, by financial quarter.")
    L.append("7. Charted each Monday-to-Friday week of 2025-26, GP-referred visits seen, turned away and kept in-house, in "
             "gp_demand_2025-26.png.\n")
    L.append("## 4. Deliverable Answers\n")
    L.append("### hub_plan_2027-28.xlsx\n")
    L.append("1. GP-referred blood-test visits to plan for at the hub in 2027-28: %s." % n(F["plan_visits_2027_28"]))
    L.append("2. Hospital-clinic visits to the walk-in clinic in 2025-26 by financial quarter of the visit, Q1 to Q4:")
    for sp, q in h.items():
        L.append("   - %s: %s, %s, %s, %s" % (sp, n(q["Q1"]), n(q["Q2"]), n(q["Q3"]), n(q["Q4"])))
    L.append("3. Working days lost to sickness and the sickness absence rate, by financial quarter of 2025-26:")
    for q, v in sk.items():
        L.append("   - %s: %s days, %.1f per cent" % (FG.QN[q], v["days_lost"], v["rate_pct"]))
    L.append("\n### gp_demand_2025-26.png\n")
    L.append("1. Stacked bars for each Monday-to-Friday week of 2025-26: GP-referred visits seen, turned away and kept "
             "in-house by the practices with their own phlebotomy clinics.")
    with open(path, "w") as fh:
        fh.write("\n".join(L) + "\n")
