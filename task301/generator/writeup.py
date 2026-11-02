"""submission.md from the golden figures (golden.figures), every number written from the values figures.json holds."""
import golden as GD


def n(x):
    return "{:,}".format(int(x))


def figure_values(F):
    """Every figure blocks 1 to 4 state, in the form they state it."""
    out = [n(F["A_r"])] + [n(F["A_prov_r"][pc]) for pc, _ in GD.PROVS]
    out += [n(F["R0_r"]["C"]), n(F["rival_bound"]), n(F["R3_r"]["E"])]
    out += [n(F["line"]), "%.3f" % F["uprate"], "6.1", "%.1f" % F["take_up_pct"], n(F["A_limit"]), n(F["A_rate"]),
            n(F["C_old"]), n(F["C_new"]), n(F["cfv_old_limit"])]
    for ym, _ in GD.MONTHS:
        out += [n(F["families"][ym].get(pc, 0)) for pc, _ in GD.PROVS]
    for pc, _ in GD.PROVS:
        el, co, rate, _ = F["fieldwork"][pc]
        out += [n(el), n(co), "%.1f" % rate]
    return out


def write(F, path):
    p = F["A_prov_r"]
    L = ["## Tags", "",
         "**Domain:** Economics & Econometrics (elasticity, welfare and policy impact estimation).",
         "**Analytical objective:** Opportunity Sizing & Decision Support.", ""]
    L += ["## 1. Final Recommendation", "",
          "**Fund measure A, the Prestación Infancia Directa: it brings %s children above the poverty line in 2027 "
          "(Valmesura %s, Las Cuencas %s, Sierra del Alba %s).**" % (n(F["A_r"]), n(p["81"]), n(p["82"]), n(p["83"])),
          "Not C, the Complemento's higher limit, which leads only if its newly entitled families were paid all year; "
          "not B or D, new payments families must claim; not E, which tops up families mostly far below the line.", ""]
    L += ["## 2. Critical Components", "",
          "1. Measure A brings **%s** children above the line in 2027: Valmesura **%s**, Las Cuencas **%s**, Sierra "
          "del Alba **%s**." % (n(F["A_r"]), n(p["81"]), n(p["82"]), n(p["83"])),
          "2. Measure C would bring **%s** children above the line if every family it covers were paid all of 2027, "
          "but its payments received in 2027 bring fewer than **%s**." % (n(F["R0_r"]["C"]), n(F["rival_bound"])),
          "3. Measures B and D also stay under **%s** in 2027, and E brings **%s**." % (n(F["rival_bound"]),
                                                                                    n(F["R3_r"]["E"])), ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Built each household from ecvv2026_households.csv and ecvv2026_persons.csv: children born 2009 or "
          "later, equivalent adults from birth years, 2027 income as 2025 disposable income times %.3f, and "
          "computable income per equivalent adult as the appraisal guidance defines it." % F["uprate"],
          "2. Gave each measure's households their payments from child_poverty_proposals_2027.pdf and counted, with "
          "the household weights, the children moved from below €%s to at or above it: with a full year, C %s and A "
          "%s." % (n(F["line"]), n(F["R0_r"]["C"]), n(F["A_r"])),
          "3. Paid A and E for all of 2027 (automatic from January); B, C and D pay from the month after each "
          "claim's decision (complemento_familiar_rules_2026.pdf, payment), their eventual claimants at the "
          "department's %.1f per cent coverage (complemento_familiar_coverage_2025.pdf)." % F["take_up_pct"],
          "4. From cfv_register_extract_20261102.csv (both date layouts) took the granted initial claims of the "
          "families the April 2024 rise brought in (computable income from €%s to under €%s, claimed from 1 April "
          "2024) as C's claiming pace by month to October 2026, the claims before the rise under €%s as B and D's, "
          "and the months from claim to first payment." % (n(F["cfv_old_limit"]), n(F["C_old"]),
                                                           n(F["cfv_old_limit"])),
          "5. Took each household's chance of crossing the line over claim month and decision lag: A %s, B, C and D "
          "each under %s, E %s, so A is funded." % (n(F["A_r"]), n(F["rival_bound"]), n(F["R3_r"]["E"])),
          "6. Counted each family once in the last month of each quarter of 2025 from resolutions decided by 31 "
          "December 2025, keeping awards whose status now reads REVOKED because their revocation is dated 2026, in "
          "the province of its municipality (territorial_codes.csv) with the moves in cfv_incidents_2025.xlsx "
          "taking effect the month after: the families in the annex.",
          "7. Took each sample dwelling in ecvv2026_fieldwork_cases.csv as its municipality and serial (its census "
          "section changed for cases issued from April 2026), once at its last issue, in the province of its "
          "municipality, with eligibility, complete interviews and the response rate as ecvv2026_main_results.pdf "
          "defines them: the fieldwork figures in the annex.", ""]
    L += ["## 4. Deliverable Answers", "", "### cabinet_note_child_poverty_2027.pdf", "",
          "1. Recommends measure A, the Prestación Infancia Directa: %s children above the poverty line in 2027, "
          "Valmesura %s, Las Cuencas %s, Sierra del Alba %s." % (n(F["A_r"]), n(p["81"]), n(p["82"]), n(p["83"])),
          "2. Bar chart on page 1 comparing the measures' children above the line with a full year of payments and "
          "with the payments received in 2027, A highest in 2027.", "",
          "### appraisal_annex_2027.xlsx", "",
          "1. Families the Complemento Familiar was paying, as its decisions stood at 31 December 2025, by the "
          "province each family lived in that month (families):"]
    for ym, lab in GD.MONTHS:
        L.append("   - %s: %s" % (lab, "; ".join("%s %s" % (name, n(F["families"][ym].get(pc, 0)))
                                               for pc, name in GD.PROVS)))
    L.append("2. ECVV 2026 eligible sample dwellings, complete interviews and response rate (per cent) by province:")
    for pc, name in GD.PROVS:
        el, co, rate, _ = F["fieldwork"][pc]
        L.append("   - %s: %s; %s; %.1f" % (name, n(el), n(co), rate))
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")
