"""task273 architecture 4: submission.md, every figure from figures.json."""
import os

import params as P

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
NAMES = {g: c for g, c, *_ in P.CONDITIONS}


def nm(g):
    return "%s (%s)" % (NAMES[g], g)


def write(F):
    j = F["call"]["joining"]
    r = F["rungs_per_1000"]
    fr = F["freq_per_1000"]
    order = sorted(fr, key=lambda g: (-F["freq_exact"][g], g))
    cur = [g for g, c, on, f, v in P.CONDITIONS if on]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Biomedical & Clinical Research (statistical genomics).  ")
    L.append("**Analytical objective:** Descriptive & Distribution Analysis.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**%s**\n" % F["call"]["sentence"])
    L.append("The three founder conditions sit at %s per 1,000 Study members, against the policy's line of one in "
             "200, once each sequencing phase's calls are divided by its members' summed chance of a call. Not the "
             "calls counted over the cohort (%s per 1,000), which reads a phase 1 member with no call as a "
             "non-carrier; not the members read at least 10 or 20 times, which drops the island and glen members the "
             "cohort counts; not the cohort's calls over its pooled chance of a call, which gives members read 8 to "
             "17 times the mainland's chance of being called. Each of the three files the current eleven.\n" % (
                 ", ".join("%d" % fr[g] for g in j),
                 ", ".join("%.1f" % r["naive"][g] for g in j)))
    L.append("## 2. Critical Components\n")
    L.append("1. The reference cohort is **%s** members: %s from phase 1 and %s from phase 2." % (
        format(F["cohort"], ","), format(F["cohort_by_phase"]["1"], ","), format(F["cohort_by_phase"]["2"], ",")))
    for k, g in enumerate(j, start=2):
        L.append("%d. %s carrier frequency is **%d per 1,000**." % (k, nm(g), fr[g]))
    L.append("")
    L.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Built the reference cohort from the member register, members with consent in force and a released genotype "
        "on 1 November 2026 (policy 2.2): %s members." % format(F["cohort"], ","),
        "Kept the variants the register classed pathogenic or likely pathogenic on 1 November 2026 from its change "
        "history (policy 2.3), and matched the phase 1 calls to the register by their GRCh37 positions: %s and %s "
        "called carriers in phase 1 and phase 2 across the 30 genes." % (
            format(sum(v["1"] for v in F["called"].values()), ","), format(sum(v["2"] for v in F["called"].values()), ",")),
        "Took, for every cohort member and register site, the binomial chance that a heterozygote read as many times as "
        "the depth file gives passes the member's phase calling rule (methods report section 2: phase 1 at least %d "
        "alternate reads and %d per cent, phase 2 at least %d and %d per cent)." % (
            F["caller"]["1"]["k"], F["caller"]["1"]["f_pct"], F["caller"]["2"]["k"], F["caller"]["2"]["f_pct"]),
        "For each variant and phase, estimated the carriers as the phase's calls divided by the sum of its members' "
        "chances, times the phase's members; summed each gene's variants and phases and divided by the cohort.",
        "Compared each condition with one in 200 (policy 2.1): %d conditions reach it, the eleven on the 2026/27 "
        "panel (lowest %d per 1,000) and the three founder conditions at %s per 1,000; the other %d sit between %d and "
        "%d per 1,000." % (F["call"]["panel_size"], F["stay_min"], ", ".join("%d" % fr[g] for g in j),
                            30 - F["call"]["panel_size"], F["out_range"][0], F["out_range"][1]),
        "For the programme's 2025/26 figures, dated each couple's report by the later of its partners' result "
        "authorisations, or the first partner's alone where a sequential screen stopped (policy 4.1, 4.2); counted a "
        "partner's carried-forward result again in the new couple's report; classed each finding as the register's "
        "change history classed it on the day its result was authorised (policy 4.3), not by the export's "
        "classification column, which from the August 2025 LIMS release carries the class on the day of the export; "
        "and counted each couple once per condition.",
        "Recommended the %d-condition panel: %s join and no condition leaves." % (
            F["call"]["panel_size"], ", ".join(j)),
    ]
    for k, s in enumerate(steps, start=1):
        L.append("%d. %s" % (k, s))
    L.append("")
    L.append("## 4. Deliverable Answers\n")
    L.append("### carrier_panel_review_2027-28.xlsx\n")
    L.append("1. Each condition's carrier frequency per 1,000 Study members and its place on the 2027/28 panel, in "
             "the workbook's order:")
    for g in order:
        tag = "joins" if g in j else ("stays" if g in cur else "not on the panel")
        L.append("   - %s: %d, %s" % (nm(g), fr[g], tag))
    L.append("2. Couples told that one or both partners carry each condition on the 2026/27 panel, April to September "
             "2025 and October 2025 to March 2026:")
    for g in [g for g, *_ in P.CONDITIONS if g in cur]:
        L.append("   - %s: %d and %d" % (nm(g), F["ask_b"]["H1"][g], F["ask_b"]["H2"][g]))
    L.append("")
    L.append("### panel_recommendation_2027-28.docx\n")
    L.append("1. The recommendation: the %d-condition panel for 2027/28, the eleven current conditions kept and %s "
             "joining, none leaving." % (F["call"]["panel_size"], ", ".join(nm(g) for g in j)))
    L.append("2. A bar chart of all 30 conditions' carrier frequencies per 1,000 on a log scale against the one in "
             "200 line, the three joining conditions marked and labelled with their frequency.")
    L.append("")
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(L))
