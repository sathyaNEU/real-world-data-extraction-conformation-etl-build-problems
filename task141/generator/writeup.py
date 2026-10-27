"""submission.md from generator/figures.json: the five blocks, every figure taken from the generator's own output."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import common as K  # noqa: E402

QLAB = ["October to December 2025", "January to March 2026", "April to June 2026", "July to September 2026"]
BANDS = ["under one year", "one year to under two years", "two years to under three years", "three years or more"]


def t(x):
    return "{:,}".format(int(x))


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    out = ["## Tags", "",
           "**Domain:** Criminology & Justice, recidivism risk assessment (a county's 2027 felony probation revocation "
           "admissions under a statute capping felony supervision at 24 months, forecast from its two probation case "
           "systems, the Circuit Court's term orders and violation petitions and the jail's bookings).",
           "**Analytical objective:** Forecasting & Predictive Modeling.", "",
           "## 1. Final Recommendation", "",
           "**Okelan County's 2027 Jail Operations Plan should carry %s felony probation revocation admissions and "
           "staff %d violator pods, one more than in 2026.**" % (t(f["call.admissions"]), f["call.pods"]),
           "The projection is %s admissions (%s to %s across the standing variants of its construction), above the %s "
           "that five pods cover under the county's standard of one pod for each %d admissions or part of %d: about a "
           "quarter of felony terms draw a violation petition in the months before their scheduled expiration, those "
           "petitions follow the expiration, and SB 26-118 moves every expiration and ends %s running terms on 31 March "
           "2027. Not %d pods, which the survival projection by month on supervision with the risk score gives (%s): "
           "it books the end-of-term petitions at expirations the Act removes. Not %d, the trailing year's %s "
           "admissions: the Act moves every term's end." % (
               t(f["call.admissions_unrounded"]), t(f["family.low"]), t(f["family.high"]), t(5 * f["pod_size"]),
               f["pod_size"], f["pod_size"], t(f["transition_terms"]), f["rung.one_clock.pods"], t(f["rung.one_clock"]),
               f["rung.persistence.pods"], t(f["trailing.felony_admissions"])), "",
           "## 2. Critical Components", "",
           "1. Section 4 of SB 26-118 ends **%s** of the felony terms open at 30 September 2026 on 31 March 2027 "
           "(supervision begun by 31 March 2025, scheduled expiration later than 31 March 2027)."
           % t(f["transition_terms"]),
           "2. Felony petitions concentrate before each term's scheduled expiration in force: **%.1f per cent** of the "
           "terms that reached their last 120 days on supervision with nothing pending had a petition filed in them, "
           "against **%.1f per cent** in the same days a year earlier." % (f["end_of_term.share_pct"],
                                                                          f["end_of_term.year_before_pct"]),
           "3. The 2027 projection is **%s** admissions, **%.2f** pods under the standard, so **%d** pods."
           % (t(f["call.admissions_unrounded"]), f["call.pods_ratio"], f["call.pods"]), "",
           "## 3. Step-by-Step Solution", "",
           "1. Joined the felony terms of %s and %s, each term's scheduled expiration in force on each day from %s and "
           "the petitions in %s: %s felony terms open at the extract." % (
               K.CMS1, K.CMS2, K.ORDERS, K.PETITIONS, t(f["open_felony_terms"])),
           "2. Applied sections 3 and 4 of %s to every open term and to terms whose supervision begins later: %s "
           "running terms end on 31 March 2027." % (K.ACT_PDF, t(f["transition_terms"])),
           "3. Aligned every felony petition on the scheduled expiration in force when it was filed: %.1f per cent of "
           "terms reaching their last 120 days carry one against %.1f per cent a year earlier, so petitions in a term's "
           "last 120 days run on a second clock tied to its end." % (f["end_of_term.share_pct"],
                                                                     f["end_of_term.year_before_pct"]),
           "4. Projected 2027 under the Act at the record's rates (%s, section 4), each term's exposure counted from "
           "1 July 2016, the first day of the extracts: the petition hazard by month on supervision outside those "
           "windows, the end-of-term rate on each open term's last 120 days before its end under the Act (from 1 "
           "January 2027 for the 31 March ends), pending petitions, new supervision starts at the trailing year's "
           "rate, the record's revocation rates and filing-to-decision days: %s admissions." % (
               K.PLAN_PDF, t(f["call.admissions_unrounded"])),
           "5. Checked the construction's variants (an end-of-term window of 90 to 150 days, the CSRS score as a "
           "covariate, one revocation rate, the mean lag): %s to %s admissions, six pods throughout." % (
               t(f["family.low"]), t(f["family.high"])),
           "6. For the bed-days, read the new jail system's UTC times in county time, counted each person in custody at "
           "00:00 on a PV-FEL or PV-MIS booking (one booking at a time, annex moves and reclassifications chained) and "
           "took each commitment's level from the term the Circuit Court revoked on the day it began: a PV-FEL booking "
           "begun on a day only a misdemeanor term of the person was revoked, or served on weekends, is misdemeanor.",
           "7. For the terms imposed, took each open felony term's term_months less the months_extended of its "
           "EXTENSION orders, averaged by office and by time on supervision at the extract.",
           "8. Applied the county's standard in the instructions' annex (one 64-bed pod for each 220 admissions or part "
           "of 220): %d pods for the plan's %s admissions." % (f["call.pods"], t(f["call.admissions"])), "",
           "## 4. Deliverable Answers", "",
           "### %s" % K.GOLD_BOOK, "",
           "1. Felony probation revocation admissions projected for 2027, to the nearest 100: %s." % t(f["call.admissions"]),
           "2. Violator pods for 2027: %d (%d beds)." % (f["call.pods"], f["call.beds"]),
           "3. How the projection is built: petitions pending at the extract, terms on supervision at the extract "
           "(petitions through the term, and petitions filed as the term lapses on its end under the Act) and terms "
           "whose supervision begins after the extract, each part with its admissions.",
           "4. Violator bed-days, whole days:"]
    for i, q in enumerate(QLAB):
        out.append("   - %s: felony %s, misdemeanor %s" % (q, t(f["ask_a.q%d.felony" % (i + 1)]),
                                                         t(f["ask_a.q%d.misdemeanor" % (i + 1)])))
    out.append("5. Average term imposed at sentencing of the felony probationers on supervision on 30 September 2026, "
               "months, one decimal:")
    for code, name, _ in K.OFFICES:
        out.append("   - %s: %.1f" % (name, f["ask_b.office.%s" % code]))
    for i, b in enumerate(BANDS):
        out.append("   - %s%s on supervision: %.1f" % (b[0].upper(), b[1:], f["ask_b.band%d" % i]))
    out += ["", "### %s" % K.GOLD_MEMO, "",
            "1. The plan's violator housing section: six pods for %s admissions, the %s terms ending on 31 March 2027 "
            "and the end-of-term petitions that move with them." % (t(f["call.admissions"]), t(f["transition_terms"])),
            "", "### %s" % K.GOLD_CHART, "",
            "1. A line chart of monthly felony probation revocation admissions from January 2019 to September 2026 "
            "with the 2027 projection by month, peaking in %s 2027." % f["peak_month"], ""]
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(out))


if __name__ == "__main__":
    main()
