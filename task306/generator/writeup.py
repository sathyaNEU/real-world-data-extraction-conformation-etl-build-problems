"""submission.md from figures.json: tags, the recommendation, its components, the steps and the deliverable answers."""
import params as P


def c(x):
    return "{:,}".format(int(x))


def pct(x):
    return "%.1f per cent" % x


def write(path, fig):
    S, F = fig["slots"], P.FILES
    order = sorted(P.NAMES, key=lambda n: -S[n])
    split = ", ".join("%s %s" % (n, c(S[n])) for n in order)
    ro = fig["register_only"]["slots"]
    t = []
    t.append("## Tags\n")
    t.append("**Domain:** Energy systems and utilities (asset condition and maintenance).")
    t.append("**Analytical objective:** Opportunity sizing and decision support.\n")
    t.append("## 1. Final Recommendation\n")
    t.append("**Tool 2027 as %s slots: the %s slots in proportion to the %s pack failures outside the OEM warranty "
             "forecast for the five platforms in the Netherlands in 2027.**" % (split, c(P.SLOTS), c(fig["total"])))
    t.append("The packs that fail in 2027 are those of the cars in use in the Netherlands in 2027: the register of 30 "
             "June 2026 and the used imports that keep arriving after it. The Mira city car's imports arrive about "
             "%.1f years old, past its five-year pack warranty, and fail in their first months here: %s of its %s "
             "forecast failures are theirs. Summed over the register alone, the Mira city car would get %s slots, the "
             "Volta hatch %s, the Kestrel SUV %s and the Tern van %s.\n"
             % (fig["mira_import_age"], c(fig["arrivals"]["Mira city car"]),
                c(fig["forecast"]["Mira city car"]["whole"]), c(ro["Mira city car"]), c(ro["Volta hatch"]),
                c(ro["Kestrel SUV"]), c(ro["Tern van"])))
    t.append("## 2. Critical Components\n")
    t.append("1. The population whose packs fall due in 2027 is every car in use in the Netherlands in 2027: the "
             "register of 30 June 2026 holds the cars that had arrived by then, and the used imports registered after "
             "it are in the fleet of 2027 too. Cars registered new after it are inside their warranty all year.")
    t.append("2. The register shows the arrivals: in the twelve months to 30 June 2026, **%s** Mira city cars were "
             "first registered here after a first admission abroad, about **%s** a month at **%.1f** years old on "
             "average, past the Mira's **5**-year warranty; the other platforms' imports arrive inside their **8** "
             "years." % (c(fig["window_imports"]["Mira city car"]), c(fig["mira_imports_month"]),
                         fig["mira_import_age"]))
    t.append("3. The 2027 forecast is **%s** failures for the cars on the register and **%s** for the imports still to "
             "arrive (**%s** of them Mira city cars): **%s** to the nearest hundred."
             % (c(fig["base_total"]), c(fig["arrivals_total"]), c(fig["arrivals"]["Mira city car"]), c(fig["total"])))
    t.append("4. In lots of 50 the shares give %s whole lots; the **%d** lots left go to the two largest remainders, "
             "the Mira city car's **%.2f** and the Plover saloon's **%.2f**, ahead of the Tern van's **%.2f**."
             % (", ".join("%s %d" % (n, fig["floors"][n]) for n in order), fig["extra_lots"],
                fig["remainders"]["Mira city car"], fig["remainders"]["Plover saloon"], fig["remainders"]["Tern van"]))
    t.append("")
    t.append("## 3. Step-by-Step Solution\n")
    t.append("1. Took each car on %s (its make is its platform) with the pack it carried on 30 June 2026 from %s: "
             "its last replacement on or before that day (an OEM nieuw pack on the "
             "platform's curve, a Voltwerk revisie pack on the refurbished curve), else the pack it was built with from "
             "its datum eerste toelating; the OEM warranty ends 8 years after datum eerste toelating, 5 for the Mira "
             "city car (%s), whatever was fitted since." % (F["register"], F["log"], F["warranty"]))
    t.append("2. Gave each car the chance its pack fails in 2027 after the warranty, given it works on 30 June 2026: "
             "F(a1) less F(a0), over 1 less F(a) on 30 June 2026, pack ages in days since fitting over 365.25, F the "
             "curve in %s read by straight lines, a0 at the later of 1 January 2027 and the warranty's end, a1 at 1 "
             "January 2028; summed by platform, %s in all." % (F["curves"], c(fig["base_total"])))
    t.append("3. Took the used imports first registered here from 1 July 2025 to 30 June 2026 (datum eerste toelating "
             "before datum eerste tenaamstelling in Nederland), each with the pack the log shows it arrived with (its "
             "last replacement before that registration, else its original pack), and carried them into July 2026 to "
             "December 2027 at that rate and mix: each month takes in a twelfth of them on the same day of the month "
             "(the month's last day if shorter), at the same age, pack age and warranty, each at its chance of failing "
             "in 2027 after its warranty given its pack works on arrival; %s in all." % c(fig["arrivals_total"]))
    t.append("4. Added the two by platform (%s; %s to the nearest hundred) and split the %s slots in proportion: 60 "
             "lots of 50, each platform's whole lots first and the lots left to the largest remainders (the plan, %s, "
             "section 2)." % (", ".join("%s %s" % (n, c(fig["forecast"][n]["whole"])) for n in order), c(fig["total"]),
                              c(P.SLOTS), F["plan"]))
    t.append("5. Modules: took the stores movements booked from 1 July 2025 to 30 June 2026 in %s, issues less "
             "returns, each line in modules by %s (a Kestrel carrier is 2) and on its work order's platform; on a "
             "supplier lot whose lines add up to more than %s shows it received (the replacement lots for held "
             "packs), a pick list carrying one quantity against several work orders went out once; divided by the "
             "packs shipped in those months in %s and multiplied by 50." % (F["stores"], F["parts"], F["receipts"],
                                                                           F["shipments"]))
    t.append("6. First-run passes: followed each pakket_id in %s to its work order through %s (a BMS replaced on "
             "rework gives the pack a new pakket_id), took each work order's first run that was not an ABORT, kept the "
             "packs whose first run started from 1 July 2025 to 30 June 2026 and took the share that passed."
             % (F["eol"], F["bms"]))
    t.append("7. Intake rejects: took the cores received from 1 July 2025 to 30 June 2026 in %s at either dock; a core "
             "with a work order in %s was built on, so it passed intake, and its AFGEKEURD is the grade its scrapped "
             "pack left on 1 July 2026 (its quarantine tag in %s is dated the day the line scrapped it, an intake "
             "reject's the day it arrived); the share rejected is the AFGEKEURD rows with no work order over all the "
             "cores received." % (F["intake"], F["workorders"], F["recycler"]))
    t.append("")
    t.append("## 4. Deliverable Answers\n")
    t.append("### voltwerk_tooling_2027.xlsx\n")
    t.append("1. Slots in 2027, by platform:")
    for n in order:
        t.append("   - %s: %s" % (n, c(S[n])))
    t.append("2. Pack failures outside the OEM warranty forecast for 2027, all five platforms: %s" % c(fig["total"]))
    t.append("3. Modules a lot of 50 should carry, by platform:")
    for n in P.NAMES:
        t.append("   - %s: %s" % (n, c(fig["ask_a"][n])))
    t.append("4. Share of the packs with a first end-of-line run from July 2025 to June 2026 that passed it, by "
             "platform:")
    for n in P.NAMES:
        t.append("   - %s: %s" % (n, pct(fig["ask_b"][n])))
    t.append("5. Share of the cores received from July 2025 to June 2026 that were rejected at intake, by platform:")
    for n in P.NAMES:
        t.append("   - %s: %s" % (n, pct(fig["ask_c"][n])))
    t.append("\n### voltwerk_tooling_2027.png\n")
    t.append("1. Each platform's 2027 forecast beside its slots, the Mira city car's %s slots the largest." %
             c(S["Mira city car"]))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(t) + "\n")
