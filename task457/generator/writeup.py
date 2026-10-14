"""Write task457/submission.md from generator/figures.json: every figure in it comes from the build."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
WORDS = ["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]


def money(x):
    return "${:,.0f}".format(x)


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    mem = f["call_members"]
    names = [m["name"] for m in mem]
    dec = f["december_filers_on_docket"]
    under = f["under_reporters"]
    instead = f["whole_year_reading_instead"]
    assert set(dec) <= set(names) and set(under) <= set(names) and not set(instead) & set(names)
    lst = lambda xs: ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]
    L = []
    L.append("# task457 submission\n")
    L.append("## Tags\n")
    L.append("**Domain:** Survey Research & Official Statistics, census, register and administrative data quality (the clinical "
             "faculty's annual disclosures, a timely self-report, validated against the Open Payments register on the years "
             "both cover: each disclosure compared with the payments the register shows made by the day it was submitted, "
             "each faculty member's amount-reporting error weighted by how many matched manufacturer-years they have, and "
             "carried to 2026, which the register has not yet published).")
    L.append("**Analytical objective:** Data Extraction & Conformation (ETL) (Open Payments payment records tied to the faculty "
             "through covered-recipient profiles, the disclosure system's versions, submission times, typed company names "
             "and two form editions, and the roster's appointments across the 2025 reorganisation and changed employee "
             "numbers conformed to one row per faculty member, manufacturer and year).\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**The docket for the committee's meeting of 11 February 2027 is %s.**\n" % lst(names))
    L.append("%s submitted their 2026 disclosures in December 2026, before the year's last payments, and are estimated with "
             "the share of the year each manufacturer had paid by that date; %s disclose about half of what the register "
             "publishes for them. Not %s, whom the corrections that read every disclosure as covering its whole year put on "
             "the docket: their earlier December disclosures make them look like under-reporters, and those corrections "
             "reproduce 2025 less closely. Not faculty with a single matched manufacturer-year reported low, whom an "
             "unweighted personal ratio promotes, nor faculty who leave small relationships out, whom the share of all "
             "published remuneration disclosed promotes.\n" % (lst(dec), lst(under), lst(instead)))
    L.append("## 2. Critical Components\n")
    L.append("1. **%d** faculty members holding an appointment on 31 December 2026 filed a 2026 disclosure naming a "
             "manufacturer that reports to Open Payments, and each is estimated." % f["faculty_estimated_2026"])
    L.append("2. **%s** of the fifteen submitted the 2026 disclosure in force in December 2026, before part of the year's "
             "payments were made." % WORDS[len(dec)].capitalize())
    L.append("3. Compared on 2025 with the largest single-manufacturer remuneration the register published for each of the "
             "**%d** faculty members estimated, the estimate that counts each disclosure to the day it was submitted comes "
             "closer than any that reads a disclosure as covering its whole year.\n" % f["faculty_estimated_2025"])
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Tied each record in open_payments_general_2021-2025_jan2027_extract.csv to a faculty member through its "
             "covered-recipient profile's NPI (open_payments_covered_recipient_profiles.csv) and the NPI in "
             "clinical_faculty_appointments.csv, and kept the five remuneration natures paid to the faculty member personally "
             "(policy 2.1 and 2.2), each payment with its Open Payments manufacturer ID and date of payment.")
    L.append("2. Took the version in force of each disclosure in coi_disclosures_2021-2026_export.xlsx with the Eastern date "
             "it was submitted, kept its remuneration items and gave each company its Open Payments ID from "
             "coi_entity_list.csv, a typed name or a listed company without an ID through the names manufacturers reported "
             "under in the register.")
    L.append("3. On each manufacturer-year from 2021 to 2025 that both sources carry, compared the amount disclosed with the "
             "payments the register shows made by the day that disclosure was submitted, and weighted each faculty member's "
             "disclosed-to-paid ratio toward the faculty-wide ratio by n/(n+%d), n their manufacturer-years: the weighting "
             "of this estimate that comes closest under policy 5.4 when the %d faculty members' 2025 estimates are compared "
             "with their largest 2025 single-manufacturer remuneration in the January 2027 publication."
             % (f["weighting_k_lines"], f["faculty_estimated_2025"]))
    L.append("4. Divided each 2026 amount disclosed for a manufacturer by the faculty member's weighted ratio and, where the "
             "disclosure in force was submitted in December 2026, by the share of the same manufacturer's 2025 payments to "
             "them made by that month and day (the faculty-wide share where it paid them nothing by then in 2025); took the "
             "largest for each of the %d faculty members and ranked them: the fifteen above lead, and the sixteenth is %s."
             % (f["faculty_estimated_2026"], f["first_left_off"]))
    a = f["ask_a_total"]
    L.append("5. Counted the faculty holding an appointment on 31 December 2026, one per NPI, by the department of the primary "
             "appointment that day (department_codes.csv giving the Department of Medicine's successors), and those with no "
             "submission of the 2026 disclosure under any of their employee numbers in coi_submission_history.csv by %s p.m. "
             "Eastern on 15 January 2027: %s owed, %d not submitted." % (f["deadline_eastern"], "{:,}".format(a["owed"]),
                                                                        a["not_submitted"]))
    L.append("6. Summed by nature the 2025 remuneration records tied through the profiles to the faculty holding an "
             "appointment at any time in 2025, payments made to the university excluded: %s." % money(f["ask_b_total"]))
    L.append("7. Summed by relationship type the 2026 remuneration items in force whose company appears in the register under "
             "no name: %s." % money(f["ask_c_total"]))
    L.append("8. Recommendation: the fifteen above form the docket for 11 February 2027.\n")
    L.append("## 4. Deliverable Answers\n")
    L.append("### coi_committee_docket_2027-02.docx\n")
    L.append("1. The fifteen faculty members on the docket, each with the manufacturer of their largest 2026 remuneration:")
    for m in mem:
        L.append("   - %s: %s" % (m["name"], m["manufacturer"]))
    L.append("2. Horizontal bar chart on page 2: the fifteen members' estimated 2026 remuneration from a single manufacturer "
             "and, in grey below a dashed line, the sixteenth, %s." % f["first_left_off"])
    L.append("3. Faculty who owed a 2026 disclosure and, of them, those who had not submitted it by %s p.m. Eastern on 15 "
             "January 2027, by department:" % f["deadline_eastern"])
    for k, v in f["ask_a"].items():
        L.append("   - %s: %s owed, %d not submitted" % (k, "{:,}".format(v["owed"]), v["not_submitted"]))
    L.append("   - All departments: %s owed, %d not submitted" % ("{:,}".format(a["owed"]), a["not_submitted"]))
    L.append("4. The 2025 remuneration Open Payments last published to faculty with appointments in 2025, by nature of "
             "payment, to the nearest thousand dollars:")
    for k, v in f["ask_b"].items():
        L.append("   - %s: %s" % (k, money(v)))
    L.append("   - All five natures: %s" % money(f["ask_b_total"]))
    L.append("5. 2026 remuneration the faculty disclosed from companies that do not report to Open Payments, by relationship "
             "type, to the nearest thousand dollars:")
    for k, v in f["ask_c"].items():
        L.append("   - %s: %s" % (k, money(v)))
    L.append("   - All types: %s\n" % money(f["ask_c_total"]))
    L.append("### faculty_remuneration_2026_conformed.csv\n")
    L.append("1. %s rows, one per faculty member and year from 2021 to 2026 in which they owed a disclosure, under the "
             "employee number holding the appointment that 31 December, each with the remuneration disclosed, the number of "
             "manufacturers disclosed, the remuneration published (blank for 2026) and the number of manufacturers "
             "published." % "{:,}".format(f["conformed_rows"]))
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
