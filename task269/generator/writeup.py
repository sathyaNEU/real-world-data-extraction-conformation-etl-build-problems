"""submission.md from generator/figures.json: the five blocks, every figure emitted from the generator's own
numbers."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402

def f1(x):
    return "%.1f" % x


def litres(x):
    return "{:,.1f}".format(x)


def names(ws):
    return ", ".join(ws[:-1]) + " and " + ws[-1] if len(ws) > 1 else ws[0]


def text(fig):
    c, cp = fig["call"], fig["components"]
    a, b, s = fig["asks"]["A"], fig["asks"]["B"], fig["asks"]["C"]
    funded = c["funded"]
    out = []
    out += ["## Tags", "",
            "**Domain:** Healthcare Delivery & Health Economics (provider quality and risk adjustment).",
            "**Analytical objective:** Descriptive & Distribution Analysis.", ""]
    out += ["## 1. Final Recommendation", "",
            "**Fund a 2027 hand hygiene coaching nurse on five wards: %s.**" % names(funded),
            "Carried across every AM and PM shift by how far the shift's worked nursing hours fell short of its "
            "patients' required care hours, the gold auditors' moments put these five below 80 per cent and every "
            "other ward above it. Not 9B alone, which the audits as they stand give (9B %s per cent, every other ward "
            "%s or above): the auditors audited almost only on shifts whose hours covered the care, and staff performed "
            "hand hygiene less often where they did not. Not the AM and PM audit shares weighted by care hours, nor the "
            "audits carried across every shift by its care hours, which also leave 9B alone: the audited shifts carry "
            "the same care hours as the rest, and only the worked hours set against them separate the two." % (
                f1(cp["audits_as_they_stand"]["9B"]), f1(cp["audits_lowest_other_ward"])), ""]
    out += ["## 2. Critical Components", "",
            "1. The audits as they stand put 9B at **%s** per cent and every other ward at **%s** per cent or above."
            % (f1(cp["audits_as_they_stand"]["9B"]), f1(cp["audits_lowest_other_ward"])),
            "2. **%s** per cent of the audited AM and PM moments were on shifts whose patients' required care hours "
            "exceeded the nurses' worked hours by more than 10 per cent, against **%s** per cent of the wards' "
            "required care hours on AM and PM shifts."
            % (f1(cp["audited_moments_on_shifts_over_10_per_cent_short"]),
               f1(cp["care_hours_on_shifts_over_10_per_cent_short"])),
            "3. On the audited shifts, staff performed hand hygiene at **%s** per cent of the moments on those shifts "
            "and **%s** per cent on the rest." % (f1(cp["compliance_on_those_shifts"]),
                                                   f1(cp["compliance_on_other_audited_shifts"])), ""]
    out += ["## 3. Step-by-Step Solution", "",
            "1. Took the terms in hand_hygiene_coaching_grant_terms_2027.pdf, section 2: a ward is funded below 80 "
            "per cent of the hand hygiene moments on its AM and PM shifts from 1 July 2025 to 30 June 2026, a shift's "
            "moments in proportion to its patients' required care hours, at most six wards.",
            "2. Built every ward's AM and PM shifts: required care hours from acuity_patient_shifts_2025_26.csv, "
            "worked hours from the rostered rows of nursing_roster_actuals_2025_26.csv (supernumerary rows left out, "
            "per acuity_and_roster_extract_notes.txt), S1A read as 6A from 2 February 2026 per "
            "ward_and_area_reference.xlsx.",
            "3. Placed each ward session of hand_hygiene_audit_moments_2025_26.csv on the roster shift it began in "
            "(no session begins in an overlap; the sessions begun on a night shift, after midnight included, left "
            "out): the audits as they stand put 9B at %s per cent and every other ward "
            "at %s or above." % (f1(cp["audits_as_they_stand"]["9B"]), f1(cp["audits_lowest_other_ward"])),
            "4. Set the audited shifts against all shifts: %s per cent of audited moments sat on shifts whose required "
            "care hours exceeded worked hours by more than 10 per cent, against %s per cent of required care hours, "
            "with compliance there %s per cent against %s."
            % (f1(cp["audited_moments_on_shifts_over_10_per_cent_short"]),
               f1(cp["care_hours_on_shifts_over_10_per_cent_short"]), f1(cp["compliance_on_those_shifts"]),
               f1(cp["compliance_on_other_audited_shifts"])),
            "5. Fitted whether hand hygiene was performed on the audited moments by ward and by the shift's ratio of "
            "required care hours to worked hours (bands at 1.05, 1.15, 1.25 and 1.35, logistic), and carried each "
            "ward's fit across all its AM and PM shifts weighted by required care hours: %s fall below 80 per cent."
            % names(funded),
            "6. Ask A: linked each culture in blood_culture_isolates_2025_26.csv to its admission in "
            "blood_culture_patient_admissions_2025_26.csv by record number, or by date of birth and sex for a record "
            "number the admissions do not hold (to the patient with an admission covering the collection); applied hobsi_surveillance_definitions_v3.pdf, a stay in the hospital "
            "running on through an admission that began at the minute the patient's previous admission ended, and an "
            "episode being the patient's across admissions; "
            "attributed each episode to the ward the patient was on at collection, rebuilt from the admitting ward and "
            "ward_transfers_2025_26.csv (a culture's location is the ward that requested it); rates over "
            "midnight_census_2025_26.csv.",
            "7. Asks B and C: summed the bottles in store_issues_hand_hygiene_2025_26.csv issued to each ward's cost "
            "centre less returns (hand rub: a pump 0.5 L, a carton 2.4 L; soap: a pump 0.5 L) and the refills in "
            "dispenser_rounds_2025_26.csv on the ward's dispensers of each type, one refill or cartridge a record "
            "(a hand rub refill 1 L, a soap cartridge 0.8 L; a terminal clean's job carries the job's cartridges on "
            "each of its records), leaving out the records a handheld sent a second time (a dispenser's record at "
            "the same minute of the day as one of its records in the twenty days before); rates over the midnight "
            "census.",
            "8. Funded the five wards below 80 per cent, within the cap of six: %s." % names(funded), ""]
    out += ["## 4. Deliverable Answers", "", "### %s" % K.GOLDEN, "",
            "1. Wards funded for a 2027 coaching nurse: %s." % names(funded),
            "2. Hospital-onset bloodstream infections 2025-26 and their rate per 10,000 occupied bed days, every ward:"]
    for w in K.WARD:
        out.append("   - %s: %d, %s" % (w, a["hobsi"][w], f1(a["rate_per_10000_obd"][w])))
    out.append("3. Alcohol-based hand rub put out in 2025-26, litres and litres per 1,000 occupied bed days, every ward:")
    for w in K.WARD:
        out.append("   - %s: %s, %s" % (w, litres(b["litres"][w]), f1(b["litres_per_1000_obd"][w])))
    out.append("4. Liquid hand soap put out in 2025-26, litres and litres per 1,000 occupied bed days, every ward:")
    for w in K.WARD:
        out.append("   - %s: %s, %s" % (w, litres(s["litres"][w]), f1(s["litres_per_1000_obd"][w])))
    out += ["", "### %s" % K.CHART, "",
            "1. Bar chart with one bar per ward, its 2025-26 compliance over its AM and PM shifts together, against a "
            "dashed 80 per cent line, the five funded wards (%s) in orange and the rest in blue." % names(funded), ""]
    return "\n".join(out)


if __name__ == "__main__":
    task = os.path.dirname(HERE)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    with open(os.path.join(task, "submission.md"), "w", encoding="utf-8") as f:
        f.write(text(fig))
    print("submission.md written")
