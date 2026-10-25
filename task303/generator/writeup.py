"""submission.md from figures.json: tags, the recommendation, its components, the steps and the deliverable answers."""
import params as P

CAND = ["F-112", "F-114", "F-205", "F-208", "F-301", "F-303"]


def c(x):
    return "{:,}".format(int(x))


def write(path, fig):
    F = P.FILES
    cl, k, d, sh = fig["call"], fig["candidates"], fig["default"], fig["shared"]
    order = sorted(CAND, key=lambda f: k[f]["rank"])
    rest = [f for f in order if f not in (cl["feeder"], "F-112", "F-114")]
    t = ["## Tags\n",
         "**Domain:** Energy systems and utilities (asset condition and maintenance).",
         "**Analytical objective:** Opportunity sizing and decision support.\n",
         "## 1. Final Recommendation\n",
         "**Convert the backbone of %s (%s) in 2027: it removes %s customer-minutes of sustained interruption a year, "
         "worth USD %s a year at the commission's USD %.2f a customer-minute.**"
         % (cl["feeder"], cl["substation"], c(cl["figure"]), c(cl["value"]), fig["rate"]),
         "F-112 (Pell Creek) comes next at %s; it leads at %s only when every breaker ticket is credited to its own "
         "backbone, and most of its vegetation, wind and wildlife breaker tickets fall on the %d occasions all three Pell "
         "Creek feeders lost supply in the same minute, which no backbone conversion prevents. F-114 falls from %s to %s the "
         "same way; %s come to %s.\n"
         % (c(k["F-112"]["figure"]), c(d["F-112"]["figure"]), sh["F-112"]["tickets"], c(d["F-114"]["figure"]),
            c(k["F-114"]["figure"]), ", ".join(rest[:-1]) + " and " + rest[-1],
            ", ".join(c(k[f]["figure"]) for f in rest[:-1]) + " and " + c(k[rest[-1]]["figure"])),
         "## 2. Critical Components\n",
         "1. Outside the accepted major event days of 2019 to 2025, the breakers of all three Pell Creek feeders "
         "(F-112, F-114, F-117) opened in the same minute **%d** times, and the Byers Mill feeders' **%d** times; "
         "Sorrel Hill's never did. Each is a loss of the substation's supply, logged on every feeder's own breaker "
         "with the cause found on the line feeding the substation, and the conversion does not prevent it."
         % (sh["F-112"]["tickets"], sh["F-301"]["tickets"]),
         "2. Without those tickets the conversion removes **%s** customer-minutes a year on %s against **%s** on F-112, "
         "where crediting every breaker ticket gives F-112 **%s**."
         % (c(cl["figure"]), cl["feeder"], c(k["F-112"]["figure"]), c(d["F-112"]["figure"])),
         "",
         "## 3. Step-by-Step Solution\n",
         "1. Stacked %s (feeder %d as F-%d, the cause and device codes and Eastern local times as %s describes) and "
         "%s (UTC stamps put on Eastern time); a ticket's minutes are DUR_MIN, or its restoration less its start, and "
         "its customer-minutes are its customers interrupted times its minutes."
         % (F["legacy"], fig["fdr_example"], fig["fdr_example"], F["notes"], F["current"]),
         "2. Left out every ticket that began on an Eastern date listed in %s." % F["meds"],
         "3. Kept the six candidates' feeder breaker and line recloser tickets caused by vegetation, wind or wildlife "
         "(%s, section 1)." % F["plan"],
         "4. Took out the tickets opened in the same minute on every feeder at the substation (the substations' "
         "feeders from %s): %d on each Pell Creek feeder, %d on each Byers Mill feeder, none at Sorrel Hill; they are "
         "losses of the substation's supply, not faults on the candidate's backbone."
         % (F["inventory"], sh["F-112"]["tickets"], sh["F-301"]["tickets"]),
         "5. Took nine in ten of the remaining customer-minutes and divided by seven (the plan, section 3): %s; %s at "
         "USD %.2f (section 4) is USD %s a year."
         % ("; ".join("%s %s" % (f, c(k[f]["figure"])) for f in order), cl["feeder"], fig["rate"], c(cl["value"])),
         "6. Storm record: each candidate's tickets in %s that began on an accepted major event day of 2023 to 2025, "
         "each restored at its crew's Restored time in %s, not at the outage system's restoration (the storm desk's "
         "later entry, or the crew's time as it arrived), with the contract crews' device times read as Eastern "
         "standard time, which they keep all year (read as daylight time, every contract crew on a summer storm day "
         "is en route before the desk gave it the job); customer-minutes summed, and over the customers interrupted."
         % (F["current"], F["crews"]),
         "7. Taps: each candidate's fuse tickets outside the major event days over 2019 to 2025, where a legacy "
         "DUR_MIN with a decimal point is a trouble crew's handheld ticket, its duration in hours and minutes (%s is "
         "%d minutes, and no such entry has more than %d after the point) and its OUT_DT the day the crew closed it, "
         "so it began on the day that, with its duration, ends on OUT_DT (only then do the ticket numbers run in the "
         "order the interruptions began); customer-minutes over seven, and over the customers interrupted."
         % (fig["hmm_example"]["text"], fig["hmm_example"]["minutes"], fig["hmm_max_after_point"]),
         "8. Recommend converting %s, the largest figure, as the plan funds." % cl["feeder"],
         "",
         "## 4. Deliverable Answers\n",
         "### hardening_memo_2027.pdf\n",
         "1. Convert the backbone of %s (%s) in 2027." % (cl["feeder"], cl["substation"]),
         "2. Customer-minutes of sustained interruption it removes a year: %s" % c(cl["figure"]),
         "3. Every candidate's figure, customer-minutes a year:"]
    for f in order:
        t.append("   - %s: %s" % (f, c(k[f]["figure"])))
    t.append("4. What %s's figure earns a year at the commission's incentive rate: USD %s" % (cl["feeder"],
                                                                                         c(cl["value"])))
    t.append("")
    t.append("### hardening_tables_2027.xlsx\n")
    t.append("1. Customer-minutes on the commission's accepted major event days of 2023 to 2025, and those minutes "
             "per customer interrupted:")
    for f in CAND:
        s = fig["storm"][f]
        t.append("   - %s: %s customer-minutes; %.1f minutes per customer interrupted" % (f, c(s["cmi"]), s["per"]))
    t.append("2. Customer-minutes a year from interruptions the tap fuses cleared outside the major event days over "
             "2019 to 2025, and those minutes per customer interrupted:")
    for f in CAND:
        s = fig["taps"][f]
        t.append("   - %s: %s customer-minutes a year; %.1f minutes per customer interrupted" % (f, c(s["year"]),
                                                                                           s["per"]))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(t) + "\n")
