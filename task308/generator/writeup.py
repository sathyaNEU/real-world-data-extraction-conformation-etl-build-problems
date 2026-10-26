"""submission.md from figures.json: tags, the recommendation, its components, the steps and the deliverable answers."""
import params as P

F = P.FILES
ORDER = ["Fenland", "Pennine", "Severn Vale", "Coastal North"]


def v1(x):
    return "%.1f" % x


def gbpm(x):
    return "GBP %s million" % ("{:,.1f}".format(x))


def write(path, fig):
    call = fig["call"]["region"]
    val = fig["values"]
    cc, st = fig["cc"], fig["steps"]
    others = sorted([r for r in P.REGIONS if r != call], key=lambda r: -val[r])
    # the rival clauses below hold only while the runner-up rounds to nil and the other two are below it
    assert val[others[0]] == 0.0 and val[others[1]] < 0 and val[others[2]] < 0, val
    t = ["## Tags\n",
         "**Domain:** Actuarial science and insurance (catastrophe exposure and accumulation).",
         "**Analytical objective:** Opportunity sizing and decision support.\n",
         "## 1. Final Recommendation\n",
         "**%s should take the 2027 catastrophe layer: it is worth %s a year there, %s more than on any other book.** "
         "Not %s (%s), which leads when recorded repair costs are carried forward by the index alone and where what "
         "the layer would recover about pays for its premium and expected reinstatement premium; nor %s (%s) or %s "
         "(%s), where the premium and the expected reinstatement premium exceed what the layer would recover.\n"
         % (call, gbpm(val[call]), gbpm(fig["call"]["margin"]), others[0], gbpm(val[others[0]]), others[1],
            gbpm(val[others[1]]), others[2], gbpm(val[others[2]])),
         "## 2. Critical Components\n",
         "1. Pennine's four pre-2021 freezes (December 2010, January 2013, December 2017 and February 2018) each "
         "exhaust the layer at the 2027 scale: **%d** full recoveries of GBP %d million." % (cc["pennine_exhausting"],
                                                                                            int(cc["layer_limit"])),
         "2. Pennine's expected recoveries are **GBP %.2f million** a year." % cc["pennine_recoveries"],
         "3. Pennine's expected reinstatement premium is **GBP %.2f million** a year, against a quoted premium of "
         "**GBP %.2f million**.\n" % (cc["pennine_reinstatement"], cc["pennine_premium"]),
         "## 3. Step-by-Step Solution\n",
         "1. Built each region's windstorm, flood and freeze loss occurrences in %s by date of loss under %s: one period "
         "of %d hours (windstorm) or %d hours (flood, freeze) from each catastrophe's first loss, holding every claim of "
         "the peril dated in it." % (F["claims"], F["events"], st["hours"][0], st["hours"][1]),
         "2. Carried each claim to the 2027 book and 2027 costs under %s: its district's 2027 policies (the plan in %s, "
         "spread by the mid-2025 mix in %s) over the year's, times %s over the index for its month of loss in %s."
         % (F["basis"], F["plan"], F["exposure"], v1(st["index_2027"]), F["index"]),
         "3. Counted each region's repair panel firms each year (the distinct repair_contractor on its claims) and each "
         "occurrence's claims per firm, then and at the 2027 scale on the 2025 panel: Pennine's four pre-2021 freezes go "
         "from %s to %s claims a firm to %s to %s." % (v1(st["pennine_freezes_then"][0]), v1(st["pennine_freezes_then"][1]),
                                                       v1(st["pennine_freezes_2027"][0]), v1(st["pennine_freezes_2027"][1])),
         "4. Fitted the log of each occurrence's index-adjusted cost per claim on its claims per firm across the %d "
         "occurrences of %d claims or more, claim-weighted, with a level for each peril and a hinge at %s claims a firm "
         "(%s per cent a claim a firm above it), and re-priced each occurrence by the fit at its 2027 claims per firm "
         "over the fit at its own." % (st["fit_occurrences"], st["fit_min_claims"], v1(st["fit_threshold"]),
                                      v1(st["fit_slope_pct"])),
         "5. Applied the layer under %s to each occurrence, capped each year at GBP %d million, averaged 2010 to 2025 and "
         "took off the quoted premium and the expected reinstatement premium: %s." %
         (F["quotes"], int(st["annual_cap"]), "; ".join("%s %s" % (r, gbpm(val[r])) for r in
                                                        sorted(P.REGIONS, key=lambda q: -val[q]))),
         "6. Ask A: the five perils' claims in %s; each claim the Major Loss Unit holds in %s (its cases grouped by "
         "policy, peril and the date of loss on their latest rows, and joined to the platform claim with that policy and "
         "peril dated on any date of loss the cases have carried) at the sum of its cases' latest incurred, in the year "
         "of that latest date of loss, unless one of its cases dropped out of the reports before October 2026 without a "
         "Closed row, when the platform's claim stands as it is; the unit's claims with no platform claim added in the "
         "year of their latest date of loss unless one of their cases dropped out the same way; over the mid-year "
         "policies in force in %s: the twelve figures in block 4."
         % (F["claims"], F["mlu"], F["exposure"]),
         "7. Ask B: %s plus every Lowther and Pike term in %s whose dates cover 31 December 2025, less each term with "
         "a cancellation effective by that day unless the term is listed for a later month that began after the "
         "cancellation took effect (a reinstatement; a rewrite ends one term and starts another under the same policy "
         "number), each at its first listed sum insured moved by endorsements effective by that day: the four figures "
         "in block 4." % (F["direct"], F["bdx"]),
         "8. Recommended %s, where the layer is worth most.\n" % call,
         "## 4. Deliverable Answers\n",
         "### cat_layer_placement_2027.pdf\n",
         "1. Region to take the layer: %s." % call,
         "2. The layer's value on %s: %s." % (call, gbpm(val[call])),
         "3. The layer's value on each of the other three: %s.\n" % "; ".join("%s %s" % (r, gbpm(val[r])) for r in others),
         "### cat_layer_workbook_2027.xlsx\n",
         "1. Incurred at 31 October 2026 per policy in force, escape of water, accidental damage, theft, fire and "
         "subsidence claims taken together:"]
    for y in ("2023", "2024", "2025"):
        t.append("   - %s: %s" % (y, "; ".join("%s GBP %.2f" % (r, fig["askA"][r][y]) for r in ORDER)))
    t.append("2. Buildings sums insured on 31 December 2025:")
    for r in ORDER:
        t.append("   - %s: %s" % (r, gbpm(fig["askB"][r])))
    with open(path, "w") as fh:
        fh.write("\n".join(t) + "\n")
