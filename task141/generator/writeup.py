"""submission.md from generator/figures.json: the five blocks, every figure taken from the generator's own output."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import common as K  # noqa: E402

QLAB = ["October to December 2025", "January to March 2026", "April to June 2026", "July to September 2026"]
BANDS = ["under one year", "one to under two years", "two to under three years", "three years or more"]


def t(x):
    return "{:,}".format(int(round(x)))


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    six, seven = 6 * f["pod_size"], 7 * f["pod_size"]
    trail = ("Not %d either for the trailing year's %s admissions carried forward." if f["rung.persistence.pods"] ==
             f["rung.pooled.pods"] else "Not %d, the trailing year's %s admissions.") % (
        f["rung.persistence.pods"], t(f["trailing.felony_admissions"]))
    out = ["## Tags", "",
           "**Domain:** Criminology & Justice, recidivism risk assessment (a county's 2027 felony probation revocation "
           "admissions under a statute capping felony supervision at 24 months and barring extension past it, forecast "
           "from its two probation case systems, the Circuit Court's term orders, violation petitions and offense "
           "classes, and the jail's bookings).",
           "**Analytical objective:** Forecasting & Predictive Modeling.", "",
           "## 1. Final Recommendation", "",
           "**Okelan County's 2027 Jail Operations Plan should staff %d violator pods (%d beds) for felony probation "
           "revocation admissions.**" % (f["call.pods"], f["call.beds"]),
           "The projection is %s admissions (%s to %s across the standing variants of its construction), more than the "
           "%s that six pods cover and within the %s of seven under the county's standard of one pod for each %d "
           "admissions or part of %d. A felony term running out with a matter still open is extended where it has room "
           "under its class maximum and draws a violation petition where it has none: about two in five of the "
           "record's terms reaching their last 120 days at their class maximum drew a petition, in every offense class "
           "including drug felony class 4 with its 24-month maximum, against %s per cent of the terms with room. SB "
           "26-118 leaves no capped term any room, so the %s running terms it ends on 31 March 2027 and every term "
           "reaching 24 months end at the at-maximum rate. Not %d pods, which the two-clock projection at the record's "
           "pooled end-of-term rate gives (%s): that rate was earned by terms that could mostly still be extended. %s"
           % (t(f["call.admissions_whole"]), t(f["family.low"]), t(f["family.high"]), t(six), t(seven), f["pod_size"],
              f["pod_size"], "%.0f" % f["rate.with_room_pct"], t(f["transition_terms"]), f["rung.pooled.pods"],
              t(f["rung.pooled"]), trail), "",
           "## 2. Critical Components", "",
           "1. **%s** of the felony terms open at 30 September 2026 end on 31 March 2027 under section 4 of SB 26-118 "
           "(supervision begun by 31 March 2025, scheduled expiration later than 31 March 2027), and section 5 lets no "
           "order from 1 January 2027 set a term's expiration past its end under the Act, so none of them has room to "
           "be extended." % t(f["transition_terms"]),
           "2. Of the record's felony terms reaching their last 120 days before the scheduled expiration in force, "
           "**about two in five** of those at their class maximum had a violation petition filed in those days, in "
           "every offense class including drug felony class 4 with its 24-month maximum, against **%s per cent** of "
           "those with room, more than half of which were extended instead." % ("%.0f" % f["rate.with_room_pct"]),
           "3. The 2027 projection is more than **%s** admissions, the six pods' cover, and no more than **%s**, the "
           "seven pods' cover, under every standing variant of its construction (%s as built, %s to %s across the "
           "variants) and the standard of one pod for each %d admissions or part of %d, so **%d** pods."
           % (t(six), t(seven), t(f["call.admissions_whole"]), t(f["family.low"]), t(f["family.high"]),
              f["pod_size"], f["pod_size"], f["call.pods"]), "",
           "## 3. Step-by-Step Solution", "",
           "1. Joined the felony terms of %s and %s (offense class, supervision begin, term), the term orders in %s "
           "(each scheduled expiration in force and each extension), the longest term for each class in %s and the "
           "petitions in %s: %s felony terms open at the extract." % (
               K.CMS1, K.CMS2, K.ORDERS, K.COURT_CODES, K.PETITIONS, t(f["open_felony_terms"])),
           "2. Applied sections 3 to 5 of %s: each open term ends at the earlier of its scheduled expiration and the "
           "later of the day 24 calendar months after supervision began and 31 March 2027 (%s of them on 31 March "
           "2027), and no term may be extended past that end." % (K.ACT_PDF, t(f["transition_terms"])),
           "3. Split the end-of-term windows the record saw (the last 120 days before a scheduled expiration then in "
           "force, the term alive and on supervision when they opened) by whether the term in force (imposed plus the "
           "extensions ordered before the window opened) had reached its class maximum: about two in five of the "
           "windows at the maximum had a petition filed in them, against %s per cent of the windows with room, more "
           "than half of which ended in an extension instead." % ("%.0f" % f["rate.with_room_pct"]),
           "4. Projected 2027 under the Act at the record's rates (%s, section 4), each term's exposure counted from 1 "
           "July 2016, the first day of the extracts: the petition hazard by month on supervision outside the windows, "
           "each term leaving as it is revoked or terminated early at the record's rates; each open term's last 120 days "
           "before its end under the Act (from 1 January 2027 for the 31 March ends), the window's petition share "
           "applied per term on the record's filing days, at the at-maximum share where the Act or the class leaves no "
           "room and at the with-room shares otherwise (an extended term running %d months more, or to the latest end "
           "the Act allows if sooner, then ending with no room); pending petitions; new supervision starts at the "
           "trailing year's rate; the record's revocation rates and filing-to-decision days: %s admissions."
           % (K.PLAN_PDF, f["param.extension_months"], t(f["call.admissions_whole"])),
           "5. Checked the standing variants (an end-of-term window of 90, 105 or 150 days, the CSRS score as a "
           "covariate, one revocation rate, the mean lag, the 31 March windows opening before 1 January 2027, only the "
           "windows of terms with nothing pending, a term with room extended 9 months, or to the latest end the Act "
           "allows): %s to %s admissions, seven pods throughout; the pooled end-of-term rate gives %s (%d pods), the "
           "lost extensions shared between petition and lapse in proportion %s (%d), every one a petition %s (%d), and "
           "the trailing year's %s admissions carried forward %d." % (
               t(f["family.low"]), t(f["family.high"]), t(f["rung.pooled"]), f["rung.pooled.pods"], t(f["rung.iia"]),
               f["rung.iia.pods"], t(f["rung.full"]), f["rung.full.pods"], t(f["trailing.felony_admissions"]),
               f["rung.persistence.pods"]),
           "6. For the bed-days, read the new jail system's UTC times in county time, chained each person's bookings "
           "(annex moves, the system replacement, reclassifications), counted each midnight a person was serving a "
           "commitment the court had ordered, from the night after the order (a held probationer stays booked PV-HOLD "
           "until the order reaches the jail) to the release the bookings record, and each midnight of a weekend "
           "sentence's stays, and took the level from the term revoked: a PV-FEL booking of a misdemeanor revocation is "
           "misdemeanor, and a night on a felony and a misdemeanor commitment at once is felony.",
           "7. For the probationers, took each open felony term's officer in %s and that officer's office in the "
           "assignments in effect on 30 September 2026 (%s), with time on supervision in completed years at the "
           "extract." % (K.CMS2, K.ROSTER),
           "8. Applied the county's standard in the instructions' annex (one 64-bed pod for each %d admissions or part "
           "of %d; six pods cover %s, seven %s): %d pods for the projection's %s admissions." % (
               f["pod_size"], f["pod_size"], t(six), t(seven), f["call.pods"], t(f["call.admissions_whole"])), "",
           "## 4. Deliverable Answers", "",
           "### %s" % K.GOLD_BOOK, "",
           "1. Violator pods for 2027: %d (%d beds)." % (f["call.pods"], f["call.beds"]),
           "2. The 2027 projection behind them: more than %s felony probation revocation admissions (six pods' cover) "
           "and no more than %s (seven pods' cover)." % (t(six), t(seven)),
           "3. Violator bed-days, whole days:"]
    for i, q in enumerate(QLAB):
        out.append("   - %s: felony %s, misdemeanor %s" % (q, t(f["ask_a.q%d.felony" % (i + 1)]),
                                                         t(f["ask_a.q%d.misdemeanor" % (i + 1)])))
    out.append("4. Felony probationers on supervision on 30 September 2026, by supervising office (the office of the "
               "officer supervising the term that day) and time on supervision in completed years (%s):"
               % ", ".join(BANDS))
    for code, name, _ in K.OFFICES:
        out.append("   - %s: %s" % (name, ", ".join(t(f["ask_b.%s.band%d" % (code, k)]) for k in range(4))))
    out += ["", "### %s" % K.GOLD_MEMO, "",
            "1. The plan's violator housing section: seven pods, the %s terms ending on 31 March 2027 and the capped "
            "terms' end-of-term petitions at the rate of the terms already at their class maximum."
            % t(f["transition_terms"]),
            "", "### %s" % K.GOLD_CHART, "",
            "1. A line chart of monthly felony probation revocation admissions from January 2019 to September 2026 "
            "with the 2027 projection by month, peaking in %s 2027." % f["peak_month"], ""]
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(out))


if __name__ == "__main__":
    main()
