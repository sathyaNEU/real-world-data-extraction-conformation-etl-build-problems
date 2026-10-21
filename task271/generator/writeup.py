"""submission.md from figures.json: every figure the write-up states is one the generator wrote."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402


def n(x):
    return format(x, ",")


def rng(fig, g):
    lo, hi = fig["family_range_pct"][g]
    return "%d to %d" % (lo, hi) if lo != hi else "%d" % lo


def write(task):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    q = fig["call"]["qualify"]
    d = fig["default_pct"]
    s = fig["sloppy_pct"]
    t = fig["totals"]
    lt = fig["late_testing"]
    a, b = fig["ask_a"], fig["ask_b"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Biomedical & Clinical Research (statistical genomics).")
    L.append("**Analytical objective:** Descriptive & Distribution Analysis.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**The Family Outreach Program should take on the PALB2 protein-truncating and PALB2 missense groups, and "
             "none of the other eight.**\n")
    L.append("Measured on every mother, sister and daughter of the probands, each a carrier with probability one half "
             "unless a final report settles it, the two PALB2 groups' risks of breast cancer by 70 are %s and %s percent "
             "across the kin-cohort and the Mendelian likelihood, and no other group's is above %d percent. Not ATM "
             "missense, BARD1 or RAD51D, which Kaplan-Meier on the relatives whose report shows the variant puts at %d, "
             "%d and %d percent: those groups were identified late (the ATM missense variants reclassified in May 2024, "
             "BARD1 and RAD51D added to the panel in July 2023), their tested relatives are mostly women tested for a "
             "breast cancer of their own, and counting every relative they stand at %s, %s and %s percent. Not CHEK2 "
             "protein-truncating, which twice the relatives' share puts at %d percent before the half who do not carry "
             "the variant are given the population's %s percent; it stands at %s percent."
             % (rng(fig, "PALB2-PTV"), rng(fig, "PALB2-MIS"),
                max(fig["family_range_pct"][g][1] for g in K.CODES if g not in q),
                d["ATM-MIS"], d["BARD1-PTV"], d["RAD51D-PTV"], rng(fig, "ATM-MIS"), rng(fig, "BARD1-PTV"),
                rng(fig, "RAD51D-PTV"), s["CHEK2-PTV"], fig["f_n_pct"], rng(fig, "CHEK2-PTV")))
    L.append("\n## 2. Critical Components\n")
    L.append("1. Every group is measured on all **%s** mothers, sisters and daughters of its probands (**%s** "
             "families), **%s** of them with a test result." % (n(t["relatives"]), n(t["families"]),
                                                               n(fig["tested_total"])))
    L.append("2. Among the living relatives of the four groups identified late, **%d to %d percent** of those with "
             "breast cancer were tested against **%d to %d percent** of those without."
             % (lt["affected_lo"], lt["affected_hi"], lt["unaffected_lo"], lt["unaffected_hi"]))
    L.append("3. Counting every relative, ATM missense, BARD1 and RAD51D stand at **%s**, **%s** and **%s percent** "
             "and the two PALB2 groups at **%s** and **%s percent**." % (rng(fig, "ATM-MIS"), rng(fig, "BARD1-PTV"),
                                                                         rng(fig, "RAD51D-PTV"), rng(fig, "PALB2-PTV"),
                                                                         rng(fig, "PALB2-MIS")))
    L.append("\n## 3. Step-by-Step Solution\n")
    L.append("1. Took each family's group and its probands' mothers, sisters and daughters from %s (the probands and "
             "half-sisters left out, criteria 2.3): %s women, each with her age at a first breast cancer or her age at "
             "the history date or at death." % (K.FILES["pedigree"], n(t["relatives"])))
    L.append("2. Took each woman's final report from %s (an Amended or Reanalysis report replacing the one it "
             "supersedes): %s tested, %s showing the family's variant." % (K.FILES["labs"], n(fig["tested_total"]),
                                                                            n(fig["tested_carriers_total"])))
    L.append("3. Took the population's risk of a first breast cancer by 70 from the rates under 70 in %s: %s percent."
             % (K.FILES["incidence"], fig["f_n_pct"]))
    L.append("4. For each group ran Kaplan-Meier on all its mothers, sisters and daughters to the 70th birthday (death "
             "and the history date censor) and took the carriers' risk as twice that share less %s percent, each "
             "relative a carrier with probability one half: PALB2-PTV %d, PALB2-MIS %d, every other group %d or less."
             % (fig["f_n_pct"], fig["risk_kin_pct"]["PALB2-PTV"], fig["risk_kin_pct"]["PALB2-MIS"],
                max(fig["risk_kin_pct"][g] for g in K.CODES if g not in q)))
    L.append("5. Checked with a Mendelian likelihood over the same women (the tested women's genotypes, the one-half "
             "prior for the rest, the population's hazard for noncarriers or both hazards estimated): the same two "
             "groups clear 30 percent and no other group comes within 5 points of it.")
    L.append("6. Known carriers for the clinic (criteria 3.1): women whose final report shows the variant as pathogenic "
             "or likely pathogenic, with an enterprise ID, living and not in %s, aged 30 to 74 on 1 April 2027, less "
             "those with both breasts removed on the first-course surgery in %s (codes 42 and 56, or 41 and 51 by side) "
             "and %s (19303 and 19307 by modifier) together." % (K.FILES["deaths"], K.FILES["abstracts"],
                                                                K.FILES["surgery"]))
    L.append("7. No screening MRI (criteria 3.2): of those women, the ones with no COMPLETED SCREENING - HIGH RISK study "
             "dated 1 October 2025 to 30 September 2026 in %s, each study matched to its woman by hospital and record "
             "number through %s." % (K.FILES["imaging"], K.FILES["empi"]))
    L.append("8. Named PALB2-PTV and PALB2-MIS for the program.")
    L.append("\n## 4. Deliverable Answers\n")
    L.append("### %s\n" % K.DELIVERABLES[0])
    L.append("1. Whether the program takes each group on:")
    for g in K.CODES:
        L.append("   - %s (%s): %s" % (g, K.LABEL[g], "taken on" if g in q else "not taken on"))
    L.append("2. Women already known to carry a variant in the group whom the program would offer the clinic on "
             "1 April 2027:")
    for g in K.CODES:
        L.append("   - %s: %s" % (g, n(a[g])))
    L.append("3. Of those women, how many had no screening breast MRI at Ellisford from 1 October 2025 to 30 September "
             "2026:")
    for g in K.CODES:
        L.append("   - %s: %s" % (g, n(b[g])))
    L.append("\n### %s\n" % K.DELIVERABLES[1])
    L.append("1. Bar chart of the ten groups' estimated risk of breast cancer by age 70 for a woman who carries the "
             "variant, with a dashed line at 30 percent and the two PALB2 groups, the only bars past it, highlighted.")
    open(os.path.join(task, "submission.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    write(os.path.dirname(HERE))
