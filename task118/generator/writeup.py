"""submission.md from figures.json: tags, the recommendation, its components, the steps and the deliverable answers."""
import params as P


def c(x):
    return "{:,}".format(int(x))


def write(path, fig):
    F = P.FILES
    L = fig["localities"]
    w, r = fig["winner"], fig["runner"]
    t = []
    t.append("## Tags\n")
    t.append("**Domain:** Pharmacology, pharmacoepidemiology and safety (benefit-risk assessment).")
    t.append("**Analytical objective:** Opportunity sizing and decision support.\n")
    t.append("## 1. Final Recommendation\n")
    t.append("**Place the hypnotic deprescribing team in %s, where it will avoid %d emergency admissions for a fall in "
             "2027; %s is the runner-up at %d, %d fewer.**" % (fig["winner_name"], fig["avoided_r"],
                                                                 fig["runner_name"], fig["runner_avoided_r"],
                                                                 fig["gap_r"]))
    t.append("The extra risk of a fall eases the longer a patient has been on a benzodiazepine or Z-drug, and %s's "
             "current users started most recently. Not Corvenham Central, which leads only if each start is taken from "
             "the patient's first item in the dispensing extract, which opens on 1 April 2026. Not %s, which leads only "
             "if every patient already on the drug when the extract opens is taken to have started over two years "
             "before.\n" % (fig["winner_name"], fig["runner_name"]))
    t.append("## 2. Critical Components\n")
    t.append("1. Current users (%s, section 4): **%s**, **%s** of them in %s." % (
        F["policy"], c(fig["n_users"]), c(L[w]["users"]), fig["winner_name"]))
    t.append("2. Admissions for a fall avoided from 1 April to 31 December 2027: **%d** in %s, **%d** in %s, **%d** or "
             "fewer in each other locality.\n" % (fig["avoided_r"], fig["winner_name"], fig["runner_avoided_r"],
                                                  fig["runner_name"], fig["others_max_r"]))
    t.append("## 3. Step-by-Step Solution\n")
    t.append("1. Took the current users from %s (born in 1961 or earlier, an item dispensed 1 July to 30 September "
             "2026), each in the locality of their practice in %s: %s." % (F["dispensing"], F["register"],
                                                                          c(fig["n_users"])))
    t.append("2. Dated each user's first start by the first template of their chain in %s, walked back by "
             "replaces_template_id and, where a template carries a migration_source_ref (%s, moved 13 July 2026), on "
             "through %s by SupersededRef; a chain whose first template replaces one not in the export started before "
             "April 2024." % (F["templates"], fig["migrated_practice_name"], F["legacy"]))
    t.append("3. Summed each user's rate ratio less 1 over the days from 1 April to 31 December 2027 at the months since "
             "that start, over 365, times %.1f per 100 and %d per cent (%s, sections 4 to 6)." % (
                 fig["base"], fig["stop_pct"], F["policy"]))
    t.append("4. Totalled by locality: %s %d, %s %d, the other four %d or fewer." % (
        fig["winner_name"], fig["avoided_r"], fig["runner_name"], fig["runner_avoided_r"], fig["others_max_r"]))
    t.append("5. Rebuilt the stays in %s (%s, F1): episodes into spells by provider_code and hospital_spell_no, and a "
             "spell whose patient was discharged to another hospital (destination 51) into the patient's spell at "
             "another site beginning that day or the next, however the receiving hospital coded it; counted the stays "
             "beginning with an emergency admission, W00 to W19 in their first episode, admitted in 2025-26, by age at "
             "admission and the practice's locality (Q80117 through the register's previous codes): %s %s aged 65 to "
             "79 and %s aged 80 or over." % (F["sus"], F["falls_def"], fig["winner_name"],
                                           c(fig["asks"][w]["falls_65_79"]), c(fig["asks"][w]["falls_80"])))
    t.append("6. Bed-days (F2): each stay's last discharge less its first admission, summed: %s %s." % (
        fig["winner_name"], c(fig["asks"][w]["bed_days"])))
    t.append("7. Readmissions (F3): the stays ended alive and followed by another stay beginning with an emergency "
             "admission on the day the stay ended or in the 30 days after: %s %s." % (
                 fig["winner_name"], c(fig["asks"][w]["readmitted"])))
    t.append("8. Recommended %s (%d) over %s (%d), %d fewer.\n" % (
        fig["winner_name"], fig["avoided_r"], fig["runner_name"], fig["runner_avoided_r"], fig["gap_r"]))
    t.append("## 4. Deliverable Answers\n")
    t.append("### deprescribing_case_2027.docx\n")
    t.append("1. The locality: %s." % fig["winner_name"])
    t.append("2. Emergency admissions for a fall it avoids in 2027: %d." % fig["avoided_r"])
    t.append("3. The runner-up: %s." % fig["runner_name"])
    t.append("4. How many fewer it would avoid: %d." % fig["gap_r"])
    t.append("\n### deprescribing_placement_2027.xlsx\n")
    a = fig["asks"]
    labels = [("falls_65_79", "Emergency admissions for a fall in 2025-26, aged 65 to 79"),
              ("falls_80", "Emergency admissions for a fall in 2025-26, aged 80 or over"),
              ("bed_days", "Bed-days those admissions used"),
              ("readmitted", "Those admissions followed by another emergency admission within 30 days of leaving "
                             "hospital")]
    for i, (k, lab) in enumerate(labels, 1):
        t.append("%d. %s:" % (i, lab))
        for code, _, _, _ in P.LOCALITIES:
            t.append("   - %s: %s" % (L[code]["name"], c(a[code][k])))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(t) + "\n")
