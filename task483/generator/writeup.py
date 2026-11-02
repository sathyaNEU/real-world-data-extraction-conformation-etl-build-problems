"""task483 submission.md from generator/figures.json: every figure written here recomputes from target/."""
import json

DRUG = {"NIT": "nitrofurantoin", "TMP": "trimethoprim", "MEC": "pivmecillinam", "CEX": "cefalexin",
        "AMC": "co-amoxiclav", "FOS": "fosfomycin", "AMX": "amoxicillin"}
ORDER = ("NIT", "TMP", "MEC", "CEX", "AMC", "FOS", "AMX")


def write(fig_path, out_path):
    F = json.load(open(fig_path))
    a, b = F["slate"]
    net = {r["network"]: r for r in F["networks"]}
    ru = F["runner_up"]
    ch = F["chances"]
    rank = F["rank"]
    lines = []
    w = lines.append
    w("## Tags")
    w("")
    w("**Domain:** Pharmacology, Pharmacoepidemiology & Safety (benefit-risk assessment: the coverage side of empiric "
      "antibiotic choice for lower urinary tract infection, sized network by network for a GP federation's "
      "stewardship pathway).")
    w("**Analytical objective:** Opportunity Sizing & Decision Support.")
    w("")
    w("## 1. Final Recommendation")
    w("")
    w("**Place the two UTI pathway pharmacists in %s and %s from 1 April 2027. Moving their 2026 first courses on "
      "other antibacterials to nitrofurantoin would have stopped about %d and %d mismatched first courses; %s is the "
      "runner-up at about %d.**" % (a, b, net[a]["stopped_r10"], net[b]["stopped_r10"], ru, net[ru]["stopped_r10"]))
    w("Read on the urine cultures sent at a first course's own consultation, nitrofurantoin meets a resistant organism "
      "in about %d per cent of first courses, pivmecillinam in %d and fosfomycin in %d, so the networks whose other "
      "courses are mostly pivmecillinam and fosfomycin stop the most. Not %s and %s: priced at the laboratory's "
      "cumulative urine antibiogram, which is drawn mostly from cultures sent after a course failed, nitrofurantoin "
      "reads far higher and their trimethoprim courses look like the only gain." % (
          ch["NIT"]["pct"], ch["MEC"]["pct"], ch["FOS"]["pct"], "Kesterby", "Ashwell Vale"))
    w("")
    w("## 2. Critical Components")
    w("")
    w("1. %s and %s: **%d** and **%d** mismatched courses stopped (nearest 10); runner-up %s **%d**." % (
        a, b, net[a]["stopped_r10"], net[b]["stopped_r10"], ru, net[ru]["stopped_r10"]))
    w("2. 2026 first courses on other antibacterials: %s **%d**, %s **%d**, %s **%d**." % (
        a, net[a]["other"], b, net[b]["other"], ru, net[ru]["other"]))
    w("")
    w("## 3. Step-by-Step Solution")
    w("")
    w("1. Took first courses as specification 2.1 defines them from gp_uti_antibacterial_issues_2024-2026.csv: acute "
      "issues of a pathway antibacterial (uti_pathway_code_lists_2027-28.xlsx, sheet Pathway antibacterials) linked to a "
      "lower UTI problem (sheet Lower UTI problems), to women aged 16 to 64 at issue, with no such issue to the same "
      "pseudonym in the 28 days before; hub issues to the registered practice and Stanbridge Road to Hollin Lane "
      "(member_practice_register_2026.xlsx).")
    w("2. Counted each network's 2026 first courses by antibacterial (%d in all)." % F["first_courses_2026"])
    w("3. Joined urine_culture_results_2024-2026.csv to the first courses by pseudonym and kept, for each first course "
      "of 2024 to 2026, the culture collected on the day of its issue (the day before to the day after gives the same "
      "%d cultures); most of the laboratory's other cultures from these women follow a failed course and are left out." %
      F["presentation_cultures"])
    w("4. Each antibacterial's chance is the share of those cultures with any organism reported R to it (MECI, NITR, "
      "TRIM and the other columns; I and S are not resistant, no significant growth and mixed growth count as no "
      "resistant organism).")
    w("5. Each network's mismatched courses stopped is the sum over its 2026 first courses on other antibacterials of "
      "the antibacterial's chance less nitrofurantoin's; the two largest get the pharmacists (specification 4.1, 4.2).")
    w("6. For the wider advice: patients (women aged 65 and over, men aged 16 and over) with a 2026 culture from a "
      "member practice or the hub, network by registered practice, counted once per organism. The laboratory "
      "changed system on 7 September 2026 (H-prefixed accession numbers before it): the old system's ENTE is the "
      "enterococcus and its ENTC the Enterobacter cloacae complex, which the new system codes ECLO while giving ENTC to "
      "the enterococci; the old ENTC isolates are all amoxicillin and co-amoxiclav resistant, as an Enterobacter is and "
      "an enterococcus is not, and no ECLO appears before the change.")
    w("")
    w("## 4. Deliverable Answers")
    w("")
    w("### uti_pathway_placement_2027-28.xlsx")
    w("")
    w("1. Pharmacists to %s and %s; runner-up %s." % (a, b, ru))
    w("2. Each network's 2026 first courses on antibacterials other than nitrofurantoin, and mismatched courses stopped "
      "(nearest 10):")
    for n in rank:
        r = net[n]
        w("   - %s: %d, %d" % (n, r["other"], r["stopped_r10"]))
    w("3. Bar chart of mismatched courses stopped by network, %s and %s marked." % (a, b))
    w("4. Women aged 65 and over and men aged 16 and over with a 2026 urine culture from a practice or the hub that "
      "grew an enterococcus, and that grew Enterobacter cloacae (patients):")
    for r in F["networks"]:
        g = F["grid"][r["network"]]
        w("   - %s: %d, %d" % (r["network"], g["Enterococcus"], g["Enterobacter"]))
    w("")
    w("### uti_pathway_placement_note_2027-28.docx")
    w("")
    w("1. One pharmacist to %s and one to %s from 1 April 2027, about %d and %d mismatched first courses stopped on the "
      "2026 basis against %d for %s." % (a, b, net[a]["stopped_r10"], net[b]["stopped_r10"], net[ru]["stopped_r10"], ru))
    with open(out_path, "w") as fh:
        fh.write("\n".join(lines) + "\n")
