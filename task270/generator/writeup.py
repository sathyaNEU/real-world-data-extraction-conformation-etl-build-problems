"""Write submission.md from generator/figures.json, so every figure in it is emitted, never typed."""
import json
import os

import common as K

HERE = os.path.dirname(os.path.abspath(__file__))


def n(x):
    return format(x, ",")


def write(task):
    f = json.load(open(os.path.join(HERE, "figures.json")))
    call, comp, b27, riv = f["call"], f["components"], f["basis_2027"], f["rivals"]
    band = call["band_names"]
    below = call["below_name"]
    rep = comp["reported_frequency"]
    order = [K.NAME[c] for c in K.CODES]
    joins = [x for x in band if x not in riv["reported"]]
    drops = [x for x in riv["reported"] if x not in band]
    assert len(joins) == 1 and len(drops) == 1 and drops[0] == below
    j, d = joins[0], drops[0]
    lines = []
    lines.append("## Tags")
    lines.append("")
    lines.append("**Domain:** Actuarial Science & Insurance, claims frequency and severity (which three of a mutual "
                 "motor insurer's eight rating regions go in the top accident frequency band of its 2027 rating basis, "
                 "once the 2027 wording makes step protection standard and an at-fault claim no longer costs a policy "
                 "its no-claims steps).")
    lines.append("**Analytical objective:** Descriptive & Distribution Analysis (each region's accident claim "
                 "frequency over the 2024 and 2025 accident years on the 2027 wording, read from a claims record cut "
                 "below the size each policyholder chose to pay for privately rather than lose steps).")
    lines.append("")
    lines.append("## 1. Final Recommendation")
    lines.append("")
    lines.append("**Band C of the 2027 rating basis holds %s, %s and %s; %s is the first region below.**" %
                 (band[0], band[1], band[2], below))
    lines.append("%s's policyholders stand mostly on the middle no-claims steps, where a claim costs the most premium "
                 "over the climb back, so they paid more of their small damage themselves; scaled from its claims above "
                 "£%s, which nobody pays privately, by the %s per cent of step 0 and Step Protection claims that large, "
                 "%s moves above %s on the 2027 wording. Not %s on the reported frequency (%s against %s's %s per 100 "
                 "vehicle-years), which counts only the claims the 2024 scale let through. Not %s on the Step "
                 "Protection holders' uplift (%s times other policyholders' frequency on steps 6 to 9), which the "
                 "holders' claims above £%s share, so it carries their choice of the add-on, and which never reaches "
                 "steps 1 to 5, where most claims are kept back." % (j, n(b27["threshold"]), b27["share_above"], j, d,
                                                                      d, rep[d], j, rep[j], d, riv["lift_factor"],
                                                                      n(b27["threshold"])))
    lines.append("")
    lines.append("## 2. Critical Components")
    lines.append("")
    lines.append("1. Vehicle-years earned over the 2024 and 2025 accident years: **%s**; accident claims paid or reserved "
                 "above nil: **%s**" % (n(comp["vehicle_years_total"]), n(comp["reported_claims_total"])))
    lines.append("2. Reported frequency per 100 vehicle-years: %s **%s** against %s **%s**" % (d, rep[d], j, rep[j]))
    lines.append("")
    lines.append("## 3. Step-by-Step Solution")
    lines.append("")
    lines.append("1. Earned each policy year in %s and %s (the legacy expiry date is the last day on cover, the "
                 "platform's term_end the renewal date, a cancellation ends cover) over 2024 and 2025, split at each "
                 "mid-term adjustment in %s and placed by %s on the day (rating_basis_2027_note.pdf, section 2): %s "
                 "vehicle-years." % (K.FILES["pol_legacy"], K.FILES["pol_platform"], K.FILES["mta"], K.FILES["regions"],
                                     n(comp["vehicle_years_total"])))
    lines.append("2. Took the accident claims in %s (amounts in pence) and %s with incurred above nil and an accident "
                 "date in 2024 or 2025 (section 2), each joined to the policy year covering its accident date, through %s where "
                 "a claim carries the platform number: %s claims, %s reporting %s per 100 vehicle-years and %s %s." %
                 (K.FILES["clm_legacy"], K.FILES["clm_platform"], K.FILES["crosswalk"],
                  n(comp["reported_claims_total"]), d, rep[d], j, rep[j]))
    lines.append("3. Compared claim sizes by step: a claim costs a step 0 or Step Protection policy no steps, and their "
                 "claims show the full size distribution; on steps 1 to 9 without protection small claims are missing in "
                 "proportion to the premium a claim costs on the step (no_claims_step_scale_2024.pdf), and above "
                 "£%s the two distributions agree." % n(b27["threshold"]))
    lines.append("4. Divided each region's accident claims above £%s by %s per cent, the share of step 0 and Step "
                 "Protection claims above £%s, over its vehicle-years: %s, %s and %s lead, %s next; the same band at "
                 "every threshold from £%s to £%s." % (n(b27["threshold"]), b27["share_above"], n(b27["threshold"]),
                                                        band[0], band[1], band[2], below, n(b27["range"][0]),
                                                        n(b27["range"][1])))
    lines.append("5. Windscreen (the basis note, section 3): counted %s's jobs billed to the Society in %s that repair "
                 "or replace a screen, a job's lines one claim, at net plus VAT, and the windscreen claims of repairers "
                 "the policyholder chose; the platform's windscreen claims from 1 July 2025 that carry a partner job's "
                 "policy number, booking day and net amount are that job registered again and are not counted twice, "
                 "and a partner job that is a camera recalibration alone recalibrates the screen another repairer "
                 "fitted on the same policy just before, so its amount with VAT is part of that repairer's claim and it "
                 "is not a claim of its own; over comprehensive vehicle-years in 2025 by cover and region on the day." %
                 (K.PARTNER, K.FILES["glass"]))
    lines.append("6. Theft (the basis note, section 4): grouped the theft claims of both exports by police crime reference (the legacy "
                 "system writes it with separators), so a recovered car's repair claim stays with its theft, dated each "
                 "theft by its first claim's loss date, kept those with a cost, and took every claim's incurred less "
                 "the net proceeds in %s (both years' statements), over 2025 vehicle-years on either cover." %
                 K.FILES["salvage"])
    lines.append("7. Band C for 2027: %s, %s and %s; first region below, %s." % (band[0], band[1], band[2], below))
    lines.append("")
    lines.append("## 4. Deliverable Answers")
    lines.append("")
    lines.append("### 2027_rating_basis_bands.xlsx")
    lines.append("")
    lines.append("1. Band C: %s, %s, %s" % tuple(band))
    lines.append("2. First region below band C: %s" % below)
    lines.append("3. 2025 windscreen claims per 100 vehicle-years with glass cover, and their average cost including VAT:")
    for x in order:
        lines.append("   - %s: %s; £%s" % (x, f["ask_a"]["frequency"][x], n(f["ask_a"]["average"][x])))
    lines.append("4. 2025 thefts per 1,000 vehicle-years, and their average cost net of salvage:")
    for x in order:
        lines.append("   - %s: %s; £%s" % (x, f["ask_b"]["frequency"][x], n(f["ask_b"]["average"][x])))
    lines.append("")
    lines.append("### band_c_frequency_2027_basis.png")
    lines.append("")
    lines.append("1. A bar chart of the eight regions' accident frequencies on the 2027 wording, band C (%s, %s and %s) "
                 "marked above the line, each region's reported frequency shown beside its bar." % tuple(band))
    with open(os.path.join(task, "submission.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    write(os.path.dirname(HERE))
