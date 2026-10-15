"""Write task462/submission.md from generator/figures.json."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W   # noqa: E402

ORDER = sorted(W.NAMES)


def _and(names):
    return ", ".join(names[:-1]) + " and " + names[-1]


def write(fig_path, out_path):
    F = json.load(open(fig_path))
    rated, I, E = F["rated"], F["intensity"], F["emitted_t"]
    near_in, near_out = F["nearest_in"], F["nearest_out"]
    wrong = F["default_wrongly_rated"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Physical & Environmental Sciences (emissions inventory: each gas producer's methane emitted "
             "over the rating year, measured from four aerial campaigns whose passes detect a plume with a chance that "
             "rises with its rate, against the methane its wells produced).")
    L.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Rate four Tollaver Basin producers low-methane for 2027: %s.**" % _and(rated))
    L.append("Their measured methane intensities over the rating year are %s per cent, under the %.2f per cent line, "
             "and %s, the nearest of the other eight, is at %.3f. Not the eight that averaging each producer's detected "
             "plumes over the four campaigns rates, adding %s: it counts every site a pass imaged without a plume as "
             "emitting nothing, though a pass detects a plume of %.1f kg/h only half the time. Not none, as carrying "
             "each detected source through the whole year would have it, the tank batteries' dumps seen on one pass "
             "in four standing for every hour.\n" % (
                 _and(["%.3f" % I[p] for p in rated]), F["limit"], near_out, I[near_out], _and(wrong), F["q50"]))
    L.append("## 2. Critical Components\n")
    L.append("1. The chance that a pass detects a plume, fitted to Talmora's %d controlled releases: one in two at "
             "**%.1f kg/h**, nine in ten at **%.1f kg/h**." % (F["releases"], F["q50"], F["q90"]))
    L.append("2. %s, the rated producer nearest the line: **%.3f** per cent." % (near_in, I[near_in]))
    L.append("3. %s, the unrated producer nearest the line: **%.3f** per cent." % (near_out, I[near_out]))
    L.append("")
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Attributed each plume in %s to the site in %s nearest it within %d m, as the rating standard places "
             "plumes, and each attributed plume to the producer operating the site on its imaging day." % (
                 W.FILES["plumes"], W.FILES["sites"], F["radius_m"]))
    L.append("2. Placed each site under its flight lines through its facility numbers in %s: a site imaged on two "
             "lines in a campaign counts the mean of its two passes, and a site a line lost to cloud left without an "
             "image is measured by its other campaigns, as the standard combines them." % W.FILES["coverage"])
    L.append("3. Fitted Talmora's logistic detection curve in the log of the metered rate to the %d releases in %s by "
             "maximum likelihood, as its methods note describes: %.1f kg/h detected half the time, %.1f kg/h nine "
             "times in ten." % (F["releases"], W.FILES["releases"], F["q50"], F["q90"]))
    L.append("4. Counted each plume at %d kg/h or more at its rate divided by its chance of detection, summed each "
             "site's plumes on each pass, averaged its passes and then its campaigns within each operator's part of "
             "the rating year, and multiplied by that part's hours: each producer's methane emitted." % F["floor"])
    L.append("5. Took each producer's methane produced from %s (the latest report for each well and month, to the "
             "operator of record, restated from %.2f to %.2f psia) with the 2026 composite methane shares in %s at "
             "%.1f kg per Mcf, and divided: each producer's measured methane intensity." % (
                 W.FILES["production"], F["state_psia"], F["std_psia"], W.FILES["gas"], F["kg_per_mcf"]))
    L.append("6. Summed the plant's lines in %s by the production month in each line's reference, October 2025 to "
             "September 2026, with the March 2026 statement at its second revision and the energy-only lines restated "
             "at the station's heating value for the month, to producers through %s: gas delivered." % (
                 W.FILES["statements"], W.FILES["stations"]))
    L.append("7. Summed codes FL and FR (routine flaring from January 2026, counted as flared in %s) in %s, the latest "
             "report for each lease, month and code, each lease to its operator of record in the month in %s: gas "
             "flared." % (W.FILES["basin"], W.FILES["flaring"], W.FILES["leases"]))
    L.append("8. Rated the producers at %.2f per cent or less: %s." % (F["limit"], _and(
        ["%s (%.3f)" % (p, I[p]) for p in rated])))
    L.append("")
    L.append("## 4. Deliverable Answers\n")
    L.append("### %s\n" % W.GOLDEN["workbook"])
    L.append("1. Rated low-methane for 2027: %s; the other eight are not rated." % _and(rated))
    L.append("2. Methane emitted over the rating year in whole tonnes, measured methane intensity in per cent, and "
             "rating:")
    for p in ORDER:
        L.append("   - %s: %s t, %.3f, %s" % (p, format(E[p], ","), I[p], "rated" if p in rated else "not rated"))
    L.append("3. Gas delivered to the Tollaver Gas Processing Plant over the rating year, whole million cubic feet:")
    for p in ORDER:
        L.append("   - %s: %s" % (p, format(F["delivered_mmcf"][p], ",")))
    L.append("4. Gas flared over the rating year, whole million cubic feet:")
    for p in ORDER:
        L.append("   - %s: %s" % (p, format(F["flared_mmcf"][p], ",")))
    L.append("5. Chart: each producer's measured methane intensity as a bar against the %.2f per cent line, on the "
             "Intensity chart sheet, the four rated producers under it.\n" % F["limit"])
    L.append("### %s\n" % W.GOLDEN["plumes"])
    L.append("1. %s rows, one per plume Talmora reported in the four campaigns, %s of them with the register site within "
             "%d m and the producer operating it on the imaging day, and %d with no producer site within %d m." % (
                 format(F["csv_rows"], ","), format(F["plumes_attributed"], ","), F["radius_m"],
                 F["plumes_unattributed"], F["radius_m"]))
    with open(out_path, "w") as f:
        f.write("\n".join(L) + "\n")
