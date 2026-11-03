"""task402 submission.md, drafted from figures.json (every figure emitted, none typed)."""


def fmt(n):
    return "{:,}".format(n)


def month(k):
    import pandas as pd
    return pd.Period(k, "M").strftime("%B %Y")


def write(path, f):
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Psychology and behavioral science (mediation, moderation and process modelling).")
    L.append("**Analytical objective:** Root-cause analysis.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Commit the 2026-27 improvement fund to change A, the agency high-intensity therapists on 12-week "
             "assignments: they cost the service about %d recoveries in 2025-26.**" % f["a_cost"])
    L.append("Not C, the waiting list, whose wait-band shortfall sits on the same courses the cover held. Not B, D or E, "
             "each of which moved recovery by far less.")
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. Step 3 courses ending in 2025-26 that an agency therapist's lapsing assignment broke off: **%s**, of "
             "which **%d** recovered" % (fmt(f["broken_courses"]), f["broken_recovered"]))
    L.append("2. Recoveries those courses would have had: **%.1f**" % f["broken_expected"])
    L.append("3. Recoveries change A cost in 2025-26: **%d** to the nearest 50" % f["a_cost"])
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Joined care_contacts_2023-10-02_to_2025-10-12.csv and appointments_2025-10-13_to_2026-05-06.parquet, "
             "mapped legacy therapist codes to user IDs through clinical_system_users_2026-05-06.xlsx and summed the "
             "item scores in outcome_measures_items_2023-10-02_to_2025-10-12.csv: recoveries on the plan's annex measure "
             "were %s in 2024-25 and %s in 2025-26 by discharge date." % (fmt(f["recoveries_2024-25"]),
                                                                       fmt(f["recoveries_2025-26"])))
    L.append("2. Matched agency users by name to agency_bookings_psychological_therapies_2025-26.xlsx and took each "
             "booking's last line end as the assignment end.")
    L.append("3. Flagged step 3 courses ending in 2025-26 whose attended treatment began with an agency therapist and "
             "whose next appointment after that therapist's assignment end was with another therapist: %s courses, %d "
             "recovered." % (fmt(f["broken_courses"]), f["broken_recovered"]))
    L.append("4. Gave each flagged course the recovery rate of the year's other step 3 referrals that attended at least "
             "as many treatment appointments as it had before the lapse: %.1f expected, a cost of %.1f, %d to the "
             "nearest 50." % (f["broken_expected"], f["a_cost_exact"], f["a_cost"]))
    L.append("5. Counted step 3 patients waiting at each month end from the waiting list snapshots, removing those whose "
             "first attended treatment appointment fell on or before the month end in the appointment files.")
    L.append("6. Inferred each Steadyway module's sections from the content IDs seen for users who began before and after "
             "5 January 2026 separately, and counted a module finished when all its sections were completed.")
    L.append("7. Left out the long-standing locum's 2023 booking, took the later of two agency portal timesheets for a "
             "week before 1 August 2025 and added e-rostering adjustment lines from then, spread each week over the "
             "therapist's working days (a 30-hour booking's four days read from its appointments) and a late first claim "
             "over the weeks it covers, and costed each day at its booking line's rate.")
    L.append("8. Change A has the largest cost: fund fixed-term high-intensity posts.")
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### improvement_case_2026-27.pptx")
    L.append("")
    L.append("1. Change named: A, agency high-intensity therapists on 12-week assignments")
    L.append("2. Its cost: %d recoveries" % f["a_cost"])
    L.append("3. Slide 3: line chart of recoveries by month of discharge, April to March, 2025-26 against 2024-25")
    L.append("")
    L.append("### review_evidence_2025-26.xlsx")
    L.append("")
    L.append("1. Step 3 patients waiting at each month end, whole patients:")
    for k, v in f["ask_waiting"].items():
        L.append("   - %s: %s" % (month(k), fmt(v)))
    L.append("2. Patients who began on the new digital platform and finished at least four modules within eight weeks, "
             "whole patients:")
    for k, v in f["ask_digital"].items():
        L.append("   - %s: %d" % (month(k), v))
    L.append("3. Agency therapists brought in for the waiting list, hours to the nearest hour and cost to the nearest "
             "100 pounds:")
    for k in f["ask_hours"]:
        L.append("   - %s: %s hours, GBP %s" % (month(k), fmt(f["ask_hours"][k]), fmt(f["ask_cost"][k])))
    L.append("")
    open(path, "w").write("\n".join(L))
