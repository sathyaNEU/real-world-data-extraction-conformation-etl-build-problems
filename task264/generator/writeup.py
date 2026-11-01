"""submission.md and figures.json, every figure emitted from the same frame the goldens use."""
import json
import math
import os


def rnd(x):
    return int(math.floor(x + 0.5))


def pair_txt(rows, a, b):
    pa = [r for r in rows if r["unit"] == a][0]["points"]
    pb = [r for r in rows if r["unit"] == b][0]["points"]
    return ("%d points each" % pa) if pa == pb else ("%d and %d points" % (pa, pb))


def write(F, task_dir, fig_path):
    fund = F["funded"]
    d = F["default"]
    rows = F["rows"]
    nm = {r["unit"]: r["name"] for r in rows}
    orm, thi = "41274", "41388"
    funded_txt = ", ".join("%s %d" % (r["name"], r["placed"]) for r in fund)
    figs = {
        "call": {"placed": F["placed"], "held": F["held"], "volume": "1,250", "providers": len(fund),
                 "per_provider": {r["name"]: r["placed"] for r in fund}, "floor": 14.5},
        "components": {"eligible": "{:,}".format(F["eligible"]), "answered": "{:,}".format(F["answered"]),
                       "resp_flag_pct": rnd(F["resp_flag"]), "resp_rest_pct": rnd(F["resp_rest"]),
                       "change_below_expected": round(abs(F["d_flag"]), 1),
                       "outcomes": {r["name"]: r["points"] for r in rows}},
        "steps": {"national_expected": round(F["netE"], 2), "flagged": "{:,}".format(F["n_flag"]),
                  "window_days": 90, "m12_from_weeks": 48, "m12_to_weeks": 64, "triage_days": 10,
                  "default_placed": {nm[u]: d[u] for u in d if d[u] > 0}},
        "csv": [{"provider": r["name"], "outcome": r["points"], "placed": r["placed"]}
                for r in rows] + [{"held": F["held"]}],
        "askA": [{"provider": r["name"], "over52": r["over52"], "within18_pct": r["within18"], "waiting": r["waiting"]}
                 for r in F["waits"]],
        "askB": [{"provider": r["name"], "participation_pct": r["part"]} for r in F["part"]],
        "thresholds": {"weeks52": 52, "weeks18": 18, "methods": "21 to 28", "months": 12, "snapshot_year": 2026},
    }
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Healthcare Delivery & Health Economics (provider quality and risk adjustment: an integrated "
             "care board placing its 2027-28 additional elective lumbar spinal operations on each provider's case-mix "
             "adjusted 12-month disability change).")
    L.append("**Analytical objective:** Descriptive & Distribution Analysis.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Place %d of the 1,250 additional 2027-28 operations with five providers (%s) and hold %d for in-year "
             "commissioning.** Over every eligible 2023-25 operation, with each missing 12-month score filled from the "
             "answerers at its provider who shared its emergency readmission status, Thistledene Hospital and Ormsbrook "
             "Spine Clinic score %s, under the 14.5-point floor. Not seven providers taking all 1,250 "
             "(Ormsbrook Spine Clinic %d, Thistledene Hospital %d), the result of reading the returned questionnaires or "
             "filling the rest from the case-mix: patients readmitted as an emergency within 90 days of discharge "
             "returned the questionnaire %d%% of the time against %d%% of the rest, and reported a change %.1f points "
             "below the case-mix expectation."
             % (F["placed"], funded_txt, F["held"], pair_txt(rows, thi, orm), d[orm], d[thi], rnd(F["resp_flag"]),
                rnd(F["resp_rest"]), abs(F["d_flag"])))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. Eligible operations **%s**, of which **%s** have a scored 12-month questionnaire."
             % (format(F["eligible"], ","), format(F["answered"], ",")))
    L.append("2. Patients with an emergency admission within 90 days of discharge returned it **%d%%** of the time "
             "against **%d%%** of the rest, and their returned change sits **%.1f** points below expected."
             % (rnd(F["resp_flag"]), rnd(F["resp_rest"]), abs(F["d_flag"])))
    L.append("3. Outcomes over every eligible operation, in points: " + ", ".join(
        "%s **%d**" % (r["name"], r["points"]) for r in rows) + ".")
    L.append("4. The providers at or above the floor offered **%d** operations, under the 1,250, so **%d** are held."
             % (F["placed"], F["held"]))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Built the 2023-24 and 2024-25 index operations from apc_spells_lumbar_cohort_2022-26.csv under section 2 "
             "of spinal_contracting_policy_2027-28.pdf, keeping each spell's latest submission and treating Penderwick "
             "House's two codes in provider_reference_2026-09.csv as one provider.")
    L.append("2. Scored both questionnaire deliveries with the eight-section rule and linked them through "
             "mossgill_nhs_number_link_2026-09.csv, with deaths from cohort_deaths_linked_2026-09.csv: %s eligible "
             "operations, %s with a 12-month score from 48 to 64 weeks." % (format(F["eligible"], ","), format(F["answered"], ",")))
    L.append("3. Took each operation's expected change from Appendix B of the policy; the national expected change over "
             "the eligible operations is %.2f points." % F["netE"])
    L.append("4. Joined each eligible operation to the same patient's later spells in the cohort extract: an emergency "
             "admission (methods 21 to 28) within 90 days of discharge marks %s operations, whose patients returned the "
             "questionnaire %d%% of the time against %d%%, so the missing scores are not ignorable on the case-mix."
             % (format(F["n_flag"], ","), rnd(F["resp_flag"]), rnd(F["resp_rest"])))
    L.append("5. Filled each missing score with the mean observed-minus-expected change of the answerers at the same "
             "provider with the same readmission status and took %.2f plus each provider's mean over all its eligible "
             "operations." % F["netE"])
    L.append("6. Applied the 14.5-point floor and offered each provider at or above it its total in "
             "spinal_capacity_returns_2027-28.xlsx in descending order of outcome: five providers, %d placed, %d held."
             % (F["placed"], F["held"]))
    L.append("7. Took the 31 March 2026 rows of ptl_spinal_month_end_2026-01_to_2026-03.csv, dated each triaged "
             "patient's clock from the surgical routing in msk_triage_referrals_2023-06_to_2026-03.json to that site with "
             "the same birth year, sex, postcode district and practice up to 10 days before the provider's receipt, dated "
             "each transferred patient's clock from the sending trust's record in "
             "ptl_spinal_removals_2025-11_to_2026-04.csv, and counted each patient moved on or before 31 March only at "
             "the receiving provider.")
    L.append("8. Over the 2025-26 index operations by procedure date, linked each pre-operative questionnaire by NHS "
             "number, placed each one without an NHS number on the unlinked operation at its site with the same sex and "
             "a birth year the age on admission allows, nearest its booked date, and tested the 90-day window against "
             "the hospital record's procedure date.")
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### spinal_volume_2027-28.csv")
    L.append("")
    L.append("1. One row per provider, outcome in whole points and operations placed:")
    for r in rows:
        L.append("   - %s: outcome %d, placed %d" % (r["name"], r["points"], r["placed"]))
    L.append("   - Not placed (held for in-year commissioning): %d" % F["held"])
    L.append("")
    L.append("### spinal_volume_board_paper.docx")
    L.append("")
    L.append("1. Recommendation: place %d operations with the five providers above and hold %d for in-year "
             "commissioning (section 1 and Table 1)." % (F["placed"], F["held"]))
    L.append("2. Stacked bar chart of each provider's waiting list on 31 March 2026 split at 52 weeks (Figure 1).")
    L.append("3. Patients waiting more than 52 weeks on 31 March 2026, and the share who had waited 18 weeks or less "
             "(whole patients, whole per cent):")
    for r in F["waits"]:
        L.append("   - %s: %d; %d%%" % (r["name"], r["over52"], r["within18"]))
    L.append("4. 2025-26 pre-operative questionnaire participation (whole per cent):")
    for r in F["part"]:
        L.append("   - %s: %d%%" % (r["name"], r["part"]))
    L.append("")
    open(os.path.join(task_dir, "submission.md"), "w", encoding="utf-8").write("\n".join(L))
    json.dump(figs, open(fig_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
    return figs
