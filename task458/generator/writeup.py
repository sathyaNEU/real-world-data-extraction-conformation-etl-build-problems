"""Write task458/submission.md from generator/figures.json: every figure in it comes from the build."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
GROUP_NAME = {"SSI-DIS": "disabled adults", "ADULT-EXP": "expansion adults", "PARENT-CR": "parents and caretaker relatives",
              "AGED-65": "adults 65 and over"}
QN = {"2025 Q3": "July to September 2025", "2025 Q4": "October to December 2025", "2026 Q1": "January to March 2026",
      "2026 Q2": "April to June 2026"}


def n(x):
    return "{:,}".format(x)


def lst(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    C = f["counties"]
    five = f["designated"]
    fr = f["full_year_route"]
    L = ["# task458 submission\n", "## Tags\n"]
    L.append("**Domain:** Healthcare Delivery & Health Economics, payment, claims and health-plan analytics (claims-based "
             "case identification against enrollment: each county's members with a serious mental illness and with an "
             "opioid use disorder estimated from the members a claim identifies, each weighted for the months it was "
             "enrolled, for need-based prescriber standards over a contract year).")
    L.append("**Analytical objective:** Data Extraction & Conformation (ETL) (the NPPES monthly file updated by its weekly "
             "files, the claims system's claim versions and the enrollment system's spans conformed to one row per "
             "county and eligibility group).\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**The board should designate %s for the 2027 Prescriber Service Award Pilot.**\n" % lst(five))
    fk, gr, yk = C["Franklin"], C["Grant"], C["Yakima"]
    wy = f["window_yield_pct"]
    L.append("Each fails at least two NP-31 standards once every member a claim identifies is counted for the months it "
             "was enrolled: Franklin's %d and Grant's %d practising prescribers each fall short of 16.5 per 1,000 of their "
             "%s and %s adult members with a serious mental illness and of 23.0 per 1,000 of their %s and %s with an "
             "opioid use disorder. Not Yakima: carrying its full-year members' prevalence to all its members, eligibility group by "
             "group, puts it at %s prescribers per 1,000 members with a serious mental illness and fails it on all three "
             "standards, but its members in short seasonal spells have the conditions far less often (%s per cent of "
             "expansion adults enrolled two months are identified with a serious mental illness, against %s per cent of the "
             "full-year expansion adults within their first two months); counted for the months each member was enrolled "
             "it has %s members with a serious mental illness, and its %d prescribers meet all three standards. Not the "
             "count of members a claim identifies, which designates only %s: NP-31 counts every member who has the "
             "condition.\n" % (
                 fk["prescribers"], gr["prescribers"], n(fk["smi"]), n(gr["smi"]), n(fk["oud"]), n(gr["oud"]),
                 fr["yakima_s_smi"],
                 wy["exp_two_months"], wy["exp_full_year_first_two"], n(yk["smi"]), yk["prescribers"],
                 lst(f["identified_count_designated"])))
    L.append("## 2. Critical Components\n")
    L.append("1. NP-31 counts **%d** practising behavioral-health prescribers in Adams, **%d** in Douglas, **%d** in Franklin, "
             "**%d** in Grant and **%d** in Okanogan on 1 November 2026 (**%d** in Yakima)." % tuple(
                 C[c]["prescribers"] for c in ("Adams", "Douglas", "Franklin", "Grant", "Okanogan", "Yakima")))
    L.append("2. Adult members with a serious mental illness, estimated: Adams **%s**, Douglas **%s**, Franklin **%s**, Grant "
             "**%s**, Okanogan **%s** (Yakima **%s**); with an opioid use disorder: **%s**, **%s**, **%s**, **%s**, **%s** "
             "(Yakima **%s**)." % tuple([n(C[c]["smi"]) for c in ("Adams", "Douglas", "Franklin", "Grant", "Okanogan", "Yakima")] +
                                [n(C[c]["oud"]) for c in ("Adams", "Douglas", "Franklin", "Grant", "Okanogan", "Yakima")]))
    three = [c for c in five if C[c]["fails"] == 3]
    two = [c for c in five if C[c]["fails"] == 2]
    L.append("3. %s fail all three standards and %s both prescriber ratios; every other county meets all three, Yakima "
             "included.\n" % (lst(three), lst(two)))
    L.append("## 3. Step-by-Step Solution\n")
    tot = f["totals"]
    cp = f["capture_pct"]
    L.append("1. Updated npidata_pfile_wa_20050523-20261011.csv record by record with the three weekly files to 1 November "
             "2026 and took NP-31 2.6 and 2.7's practising prescribers (primary taxonomy in Appendix B, NPI active on 1 "
             "November, practice ZIP code to the county with the larger BUS_RATIO in ZIP_COUNTY_062026.xlsx, rendering "
             "provider of a final claim or encounter): %d in the ten counties." % tot["practising"])
    L.append("2. Joined enrollment_spans_2025-07-01_2026-06-30.csv into %s adult members by client_id, each in the county and "
             "eligibility group of the span covering the last enrolled day (2.2, 2.3), with the months enrolled; %s were "
             "enrolled all twelve months." % (n(tot["adult_members"]), n(tot["full_year"])))
    L.append("3. Kept the final version of each claim in bh_claims_encounters_dos_2025-07-01_2026-06-30.csv (frequency 7 in "
             "place of the claim it replaces, frequency 8 and the claim it voids removed) and identified conditions by the "
             "Appendix A codes in any position (2.4), with the month of each member's first identifying service: %s members "
             "with a serious mental illness, %s with an opioid use disorder." % (n(tot["rec_smi"]), n(tot["rec_oud"])))
    L.append("4. A condition shows only in services billed while a member is enrolled: of the members enrolled all year with "
             "a serious mental illness, %s per cent are first identified in July 2025 and %s per cent within three months. "
             "Members in short seasonal spells fall well short of that share (%s per cent of expansion adults enrolled two "
             "months against %s per cent of the full-year expansion adults within their first two months), while those "
             "enrolled seven to eleven months are identified as often as the full-year members are within the same months, "
             "so the seasonal members have the conditions less often and the full-year prevalence is not carried to them." % (
                 cp["smi_1"], cp["smi_3"], wy["exp_two_months"], wy["exp_full_year_first_two"]))
    L.append("5. Counted each identified member as 1 over the share of the full-year members with the condition identified "
             "within the same number of months as the member was enrolled (2.5 counts every member who has the condition, "
             "and a full-year member no claim identifies as not having it), summed by county; counted the members with a serious mental illness who had an Appendix C service from a "
             "behavioral-health prescriber anywhere (2.8; every one is among the identified) and computed the three "
             "standards against 16.5, 23.0 and 68 per cent (3.1, 3.2).")
    L.append("6. Designated the counties failing two or more (4.1): %s." % lst(five))
    L.append("7. For the payments, took the final fee-for-service claims with a behavioral-health prescriber as rendering "
             "provider and each claim's paid_amt once (it repeats on every line of the claim and equals the sum of its "
             "lines' lesser of billed_amt and the allowable in bh_professional_fee_schedule_fy2026.csv), by the member's "
             "county and the quarter of the service date.")
    L.append("8. Recommendation: designate %s.\n" % lst(five))
    L.append("## 4. Deliverable Answers\n")
    L.append("### prescriber_pilot_county_scorecard_2027.xlsx\n")
    L.append("1. Designated counties: %s." % lst(five))
    L.append("2. Each county's practising prescribers, estimated adult members with a serious mental illness and with an "
             "opioid use disorder (nearest 10), and standing on the three standards:")
    for c, x in C.items():
        names = {"meets_smi": "the serious-mental-illness ratio", "meets_oud": "the opioid-use-disorder ratio",
                 "meets_reach": "the reach"}
        missed = [nm for k, nm in names.items() if not x[k]]
        kept = [nm for k, nm in names.items() if x[k]]
        verdict = ("fails all three standards" if x["fails"] == 3 else "meets all three standards" if x["fails"] == 0 else
                   "fails both prescriber ratios, meets the reach" if x["fails"] == 2 and x["meets_reach"] else
                   "fails %s, meets %s" % (lst(missed), lst(kept)))
        L.append("   - %s: %d prescribers; %s with a serious mental illness, %s with an opioid use disorder; %s; %s" % (
            c, x["prescribers"], n(x["smi"]), n(x["oud"]), verdict, "designated" if x["designated"] else "not designated"))
    L.append("3. Net fee-for-service payments for services behavioral-health prescribers rendered to each county's adult "
             "members, whole dollars, %s:" % ", ".join("%s" % QN[q] for q in f["payments"]["Adams"]))
    for c, p in f["payments"].items():
        L.append("   - %s: %s" % (c, ", ".join("$" + n(v) for v in p.values())))
    L.append("\n### county_adult_members_2026_conformed.csv\n")
    L.append("1. Adult members and net fee-for-service payments for behavioral-health prescribers' services (whole dollars), "
             "by county and eligibility group:")
    for k, x in f["conformed"].items():
        c, g = k.split("|")
        L.append("   - %s, %s: %s members, $%s" % (c, GROUP_NAME[g], n(x["members"]), n(x["paid"])))
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
