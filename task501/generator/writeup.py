"""Render submission.md from generator/figures.json: the prose is fixed here, every figure comes from the file the
generator wrote, so no figure in the write-up is typed."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
KEYS = ["A", "B", "C", "D", "E"]


def render(f):
    R = f["reproduction_number"]
    y = f["option_birth_years"]
    L = []
    w = L.append
    w("## Tags")
    w("")
    w("**Domain:** Epidemiology & Public Health (infectious-disease transmission modeling).")
    w("**Analytical objective:** Forecasting & Predictive Modeling.")
    w("")
    w("## 1. Final Recommendation")
    w("")
    w("**We should fund option B, the MMR catch-up for those born %s: it is the only option that brings measles' "
      "reproduction number in the region below one for winter 2027-28 (%s, against %s with no catch-up).** Not no "
      "catch-up, which the region's %s per cent immunity (%s as R0 times the susceptible share) supports only if everyone "
      "mixes at random, while the %s-year-olds, %s per cent susceptible, have about half their contacts with each "
      "other. Not D or E, the least immune cohort and the most people made immune, which leave it at %s because adults "
      "mix too little among themselves. Not A or C, which leave it at %s."
      % (y["B"], R["Option B"], R["No catch-up"], f["region_immune_per_cent"], f["default_R0_times_susceptible_share"],
         f["age_group_teenagers"], f["susceptible_share_15_19_per_cent"], R["Option D"], R["Option A"]))
    w("")
    w("## 2. Critical Components")
    w("")
    w("1. Reproduction number with no catch-up, winter 2027-28, the dominant eigenvalue of the next-generation matrix "
      "scaled to R0 %s: **%s**" % (f["R0"], R["No catch-up"]))
    w("2. Reproduction number under option B: **%s**" % R["Option B"])
    w("3. Reproduction number under options A, C, D and E: **%s** each" % R["Option A"])
    w("4. Susceptible share of %s-year-olds on 1 January 2028: **%s per cent**, against **%s per cent** across the "
      "region" % (f["age_group_teenagers"], f["susceptible_share_15_19_per_cent"], f["susceptible_share_region_per_cent"]))
    w("")
    w("## 3. Step-by-Step Solution")
    w("")
    w("1. Joined measles_immunity_profile_oriel_2027-05.csv to population_projection_oriel_2028-01-01.csv by year of "
      "birth (PS-07 3.3 and 3.4): each survey age group's susceptible share on 1 January 2028, %s per cent for %s and "
      "%s per cent overall." % (f["susceptible_share_15_19_per_cent"], f["age_group_teenagers"],
                                f["susceptible_share_region_per_cent"]))
    w("2. Built the next-generation matrix from Table 2 of nscs_2023_published_tables.xlsx (contacts per day by age "
      "group) times each age group's susceptible share, scaled so that a wholly susceptible region gives the R0 of %s "
      "(PS-07 3.2)." % f["R0"])
    w("3. Took its dominant eigenvalue: %s with no catch-up, so a catch-up is needed (PS-07 3.6)." % R["No catch-up"])
    w("4. Took each option's expected people made immune in mmr_catch_up_options_autumn_2027.pdf off the susceptibles "
      "of its birth years (PS-07 3.5) and recomputed: option B %s; options A, C, D and E %s." % (R["Option B"], R["Option A"]))
    w("5. Counted each option's residents in register_people_active_born_1993-2017.csv, reading each lho_code in the "
      "scheme in force on its lho_recorded date (circular 03/2024: LH27 recorded before 1 July 2024 is Monaghan West, "
      "in the region).")
    w("6. Counted their valid doses in register_mmr_events_born_1993-2017.csv, re-pointed through "
      "register_merges_born_1993-2017.csv and without the GP lines gp_return_queries_mmr_2005-2027.csv shows replaced "
      "or withdrawn, under guidelines 12.5 at 30 June 2027.")
    w("7. Counted confirmed cases with rash onset in the window in nds_measles_cases_oriel_2019-2027.csv by year of "
      "birth, each back-entered 2019 outbreak record (its legacy number in the comments) counted once with its migrated "
      "record.")
    w("8. Recommended option B, the only option below one (PS-07 3.6).")
    w("")
    w("## 4. Deliverable Answers")
    w("")
    w("### winter_measles_2027.xlsx")
    w("")
    w("1. Call: fund option B, the MMR catch-up for those born %s." % y["B"])
    w("2. Reproduction number for winter 2027-28, to one decimal place:")
    for k in ["No catch-up"] + ["Option %s" % x for x in KEYS]:
        w("   - %s: %s" % (k, R[k]))
    w("3. People born in each option's years whom the register holds as living in the region at 30 June 2027:")
    for k in KEYS:
        w("   - Option %s (born %s): %s" % (k, y[k], f["ask1_register_residents"][k]))
    w("4. Of those, people with no valid MMR dose and with exactly one:")
    for k in KEYS:
        w("   - Option %s: %s with no valid dose, %s with exactly one" % (k, f["ask2_no_valid_dose"][k],
                                                                       f["ask2_one_valid_dose"][k]))
    w("5. Confirmed measles cases with rash onset from 1 January 2019 to 30 June 2027 born in each option's years, and "
      "how many of them were imported:")
    for k in KEYS:
        imp = f["ask3_imported"][k]
        w("   - Option %s: %s confirmed, %s imported" % (k, f["ask3_confirmed_cases"][k], "none" if imp == "0" else imp))
    w("")
    w("### measles_readiness_2027.pptx")
    w("")
    w("1. Slide 1 opens with the call: fund option B, the catch-up for those born %s, the only option that brings the "
      "winter's reproduction number below one (%s)." % (y["B"], R["Option B"]))
    w("2. Slide 2: bar chart of the six reproduction numbers (no catch-up %s, A %s, B %s, C %s, D %s, E %s) against a "
      "dashed line at one, option B's bar the only one under it." % tuple(R[k] for k in
                                                                        ["No catch-up"] + ["Option %s" % x for x in KEYS]))
    return "\n".join(L) + "\n"


def main(figs_path=None, out=None):
    figs_path = figs_path or os.path.join(HERE, "figures.json")
    out = out or os.path.join(TASK, "submission.md")
    f = json.load(open(figs_path, encoding="utf-8"))
    text = render(f)
    assert "\u2014" not in text and "\u2013" not in text
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(text)
    return out


if __name__ == "__main__":
    main(*sys.argv[1:])
