"""task464 architecture 9: submission.md, every figure emitted from figures.json."""
import json, os
import world as W

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(BASE, "generator", "figures.json")


def fmt(n):
    return "{:,}".format(n)


def main():
    F = json.load(open(FIG, encoding="utf-8"))
    name = {p["code"]: p["name"] for p in W.PRACTICES}
    order = F["ranking"]
    call = F["call"]
    second = order[1]
    L = []
    L += ["## Tags", "",
          "**Domain:** Pharmacology, Pharmacoepidemiology & Safety (medication adherence and persistence).",
          "**Analytical objective:** Descriptive & Distribution Analysis.", ""]
    L += ["## 1. Final Recommendation", "",
          "**Place the 2027 statin continuity sessions at %s, with %s next in line.**" % (name[call], name[second]),
          "%s of %s's %s patients in the brief's population have their latest statin issue on a repeat of six 56-day "
          "issues authorised in February or March 2026, so their repeats run out together before March 2027, and %d%% of statin repeats that "
          "run out are not re-authorised. Not %s, whose six-issue repeats bring its reviews round through the whole "
          "year rather than together. Not %s, the largest list, whose summer switch to atorvastatin re-authorised most "
          "of its statin patients for a year." % (fmt(F["six_56day_feb_mar_2026"][call]), name[call],
                                                  fmt(F["population"][call]), F["reauth_fail_whole"], name[second],
                                                  name[order[2]]), ""]
    L += ["## 2. Critical Components", "",
          "1. **%d%%** of statin repeats whose authorised issues were all issued were not re-authorised within 60 "
          "days." % F["reauth_fail_whole"],
          "2. %s has **%s** patients in the brief's population, **%s** of them with their latest statin issue on a "
          "repeat of six 56-day issues authorised in February or March 2026." % (name[call], fmt(F["population"][call]),
                                                     fmt(F["six_56day_feb_mar_2026"][call])), ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Stacked both systems' issue extracts through cvd_product_lookup.csv and took the patients registered "
          "on 30 November 2026 in patient_register_2026-12-01.csv who were issued a statin by that practice from "
          "1 September to 30 November 2026: %s patients across the seven practices." % fmt(F["population_total"]),
          "2. Matched each statin repeat authorised from January 2024 in repeat_authorisations_system_a.csv and "
          "repeat_authorisations_system_b.csv whose authorised issues were all issued, the last by 3 July 2026, to a "
          "new statin repeat for the patient within 60 days of its supply running out: %d%% were not "
          "re-authorised." % F["reauth_fail_whole"],
          "3. Measured stops between reviews as statin repeats left with issues unused and no statin issued for "
          "%d days, per %d days of statin supply, separately for a new start's first six months." % (F["stop_gap_days"],
                                                                                              F["stop_rate_supply_days"]),
          "4. Ran each patient's current repeat, the one their latest statin issue was on, forward from that issue at "
          "the record's mean request interval to the request after its last authorised issue; where that last issue "
          "falls before 1 March 2027 the patient is not issued in the window at the %d%% chance of no re-authorisation "
          "or after a stop between reviews on the way, a repeat that ran out over three weeks before the searches with "
          "no new repeat is not issued, and each chance is scaled by the record's seven-month stay on the "
          "register." % F["reauth_fail_whole"],
          "5. Summed by practice: %s has the largest expected number and %s the next." % (name[call], name[second]),
          "6. R1: took each ACE inhibitor or ARB issue's dosage from repeat_changes_2024-01_to_2026-11.csv, each "
          "change attached to the repeat the patient held for that product on its day (system A files a change "
          "against the drug line's current repeat) and a changed repeat read from the log's own history, since "
          "system B lists its current repeats as authorised; read a dose in milligrams against the product's "
          "strength, dropped the items in eps_item_cancellations_2024-2026.csv, carried supply forward within the "
          "drug and counted the days of %d covered per the return specification: each practice's R1 percentage "
          "below." % F["return_year"],
          "7. R2: took each start from the 'Ticagrelor 90mg twice daily started in secondary care' entries in "
          "cvd_clinical_events_2023-2026.csv within three days of a myocardial infarction however the hospital coded "
          "it (an infarction, a STEMI, an NSTEMI or 'Heart attack', not unstable angina or an old infarction), both "
          "inside the window, at the practice coded on the entry, and counted the patients issued ticagrelor 90mg on "
          "a day later than its first anniversary: each practice's R2 percentage below.",
          "8. Placed the sessions at %s." % name[call], ""]
    L += ["## 4. Deliverable Answers", "", "### statin_sessions_2027.xlsx", "",
          "1. Patients in the brief's population, by practice:"]
    for c in sorted(F["population"]):
        L.append("   - %s (%s): %s" % (name[c], c, fmt(F["population"][c])))
    L += ["2. Sessions placed at %s." % name[call],
          "3. Runner-up: %s." % name[second],
          "4. Bar chart of the seven practices on the brief's figure, %s highlighted, on the Placement sheet." % name[call], "",
          "### cvd_repeat_returns_2025.csv", "",
          "1. R1, ACE inhibitor or angiotensin II receptor blocker adherence in 2025, percentage to one decimal place:"]
    for c in sorted(F["ask_a"]):
        L.append("   - %s (%s): %.1f" % (name[c], c, F["ask_a"][c]["pct"]))
    L.append("2. R2, ticagrelor 90mg issued after the first anniversary of starting it, percentage to a whole number:")
    for c in sorted(F["ask_b"]):
        L.append("   - %s (%s): %d" % (name[c], c, F["ask_b"][c]["pct"]))
    L.append("")
    open(os.path.join(BASE, "submission.md"), "w", encoding="utf-8").write("\n".join(L))
    print("  submission.md, %d lines" % len(L))


if __name__ == "__main__":
    main()
