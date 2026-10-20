"""submission.md from figures.json: every figure the write-up states is one the generator wrote."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402


def f1(x):
    return "%.1f" % x


def write(task):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    s1, s2 = fig["call"]["sites"]
    below = fig["call"]["below"]
    d = fig["decline"]
    a, b = fig["ask_a"], fig["ask_b"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Psychology & Behavioral Science (longitudinal growth curve modelling).")
    L.append("**Analytical objective:** Descriptive & Distribution Analysis.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**The Research Committee should name %s and %s as the recruiting sites for ARV-1102.**\n" % (s1, s2))
    L.append("Once the one-time gain a patient's second completed ACE-III carries from having sat the test before "
             "(%s points) is taken out of each patient's own decline, %s's patients decline %s ACE-III points a year "
             "and %s's %s, ahead of %s on the unrounded figures. Not Penwardine, fourth once the gain is out, which a "
             "slope through every assessment ranks second because nearly half of its patients sat their first ACE-III "
             "before 2022 and carry the gain through the whole period, where most of %s's are new to the test. Not "
             "%s's last place on that slope, which is the gain flattening the slopes drawn through a patient's first "
             "two or three assessments at the clinic whose patients are nearly all new to the test. Not that gain "
             "estimated from the period's assessments alone, which takes each patient's first assessment in the "
             "period for their first, misses the gain the patients seen before 2022 carry throughout, and names %s "
             "and %s again."
             % ((f1(fig["gain"]), s1, f1(d[s1]), s2, f1(d[s2]), below, below, s1)
                + tuple(fig["rivals"]["period_only"])))
    L.append("\n## 2. Critical Components\n")
    L.append("1. The second completed ACE-III carries a one-time gain of **%s** points over the patient's own trend, "
             "estimated within patients." % f1(fig["gain"]))
    L.append("2. %s's patients decline **%s** ACE-III points a year net of the gain, the fastest of the eight." %
             (s1, f1(d[s1])))
    L.append("3. %s's patients decline **%s** points a year, ahead of every clinic outside the pair on the "
             "unrounded figures." % (s2, f1(d[s2])))
    L.append("\n## 3. Step-by-Step Solution\n")
    L.append("1. Joined the CIS forms to the EPR sets through the master patient index (merged hospital numbers "
             "included, sets entered in error left out) and numbered each patient's completed assessments over their "
             "whole record.")
    L.append("2. Kept the patients whose latest diagnosis on the record on 30 September 2026 is Alzheimer's disease "
             "or mild cognitive impairment, with two or more completed assessments from 1 January 2022 to 30 "
             "September 2026, at the clinic of the last (paper RC/26/11, section 3): %s patients."
             % format(fig["counts"]["patients_compared"], ","))
    L.append("3. Estimated the change the test itself produces, which the paper's figure excludes, as a step at "
             "each patient's second completed assessment of their whole record, CIS assessments before 2022 counted, "
             "within patients: each "
             "patient with three or more assessments in the period given their own intercept and slope and one "
             "shared step: %s points." % f1(fig["gain"]))
    L.append("4. Took each patient's decline as the least-squares slope of their totals net of the gain and averaged "
             "each clinic's patients, ranked unrounded: %s %s and %s %s points a year lead."
             % (s1, f1(d[s1]), s2, f1(d[s2])))
    L.append("5. Questionnaire B1 and B2: episodes open on 30 September 2026 in the EPR episodes extract, less "
             "the patients the appointments show discharged at a review, or handed to the care home liaison team, "
             "between the episode's start and that day, less deaths on the Spine, by the latest "
             "recorded diagnosis and by age on 1 January 2027.")
    L.append("6. Questionnaire C1 and C2: for each referral's first diagnosis given from 1 October 2025 to 30 "
             "September 2026, the tracker's referral date to the appointment that gave it: the one whose outcome "
             "records the diagnosis given or, for a finding of no dementia or of depression, the one that discharged "
             "the patient, not the tracker's diagnosis date, the day it reached the problem list.")
    L.append("7. Named %s and %s as the recruiting sites." % (s1, s2))
    L.append("\n## 4. Deliverable Answers\n")
    L.append("### arv1102_site_selection.xlsx\n")
    L.append("1. Recruiting sites: %s and %s." % (s1, s2))
    L.append("2. Decline in ACE-III points a year, to the nearest half point, fastest first:")
    for c in fig["call"]["order"]:
        L.append("   - %s: %s" % (c, f1(d[c])))
    L.append("3. Gain at the second completed assessment: %s points." % f1(fig["gain"]))
    L.append("4. B1, patients with Alzheimer's disease or mild cognitive impairment under follow-up on 30 September "
             "2026, and B2, of whom %d or under on 1 January 2027:" % fig["terms"]["age_limit"])
    for c in K.NAMES:
        L.append("   - %s: %s under follow-up, %s aged %d or under" % (c, format(a["under_follow_up"][c], ","),
                                                                     format(a["aged_85_or_under"][c], ","),
                                                                     fig["terms"]["age_limit"]))
    L.append("5. C1, share given their diagnosis within %d days of referral, and C2, average days from referral to "
             "diagnosis, diagnoses given 1 October 2025 to 30 September 2026:" % fig["terms"]["six_weeks_days"])
    for c in K.NAMES:
        L.append("   - %s: %s per cent, %s days" % (c, f1(b["within_42_days_pct"][c]), f1(b["average_days"][c])))
    L.append("\n### arv1102_clinic_decline.png\n")
    L.append("1. Bar chart of the eight clinics' declines, fastest at the top, %s and %s highlighted above a line "
             "marking the recruiting sites, each clinic's half-point figure beside its name." % (s1, s2))
    open(os.path.join(task, "submission.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    write(os.path.dirname(HERE))
