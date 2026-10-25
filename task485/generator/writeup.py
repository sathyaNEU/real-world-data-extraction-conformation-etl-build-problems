"""submission.md from generator/figures.json: the five blocks, every figure taken from the generator's own output."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 11: "eleven", 12: "twelve"}


def joined(xs):
    xs = list(xs)
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def t(x):
    return "{:,}".format(x)


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    B = f["boilers"]
    order = f["order"]
    listed, unlisted = f["call"]["listed"], f["call"]["not_listed"]
    near = min(listed, key=lambda k: B[k]["so2_unrounded"])
    top_off = max(unlisted, key=lambda k: B[k]["so2_unrounded"])
    dflt = f["default"]["listed"]
    bypassed = [k for k in listed if k not in dflt]
    ratios = [B[k]["ratio"] for k in bypassed]
    design = f["design"]
    c = f["components"]
    k = f["constants"]
    out = ["## Tags", "",
           "**Domain:** Physical & Environmental Sciences, emissions inventory (an environment ministry's 2026 sulphur "
           "dioxide inventory of eighteen permitted coal boilers with wet limestone scrubbers, conformed from four coal "
           "suppliers' delivery analyses, the operators' quarterly returns, two quarries' tickets and weekly "
           "certificates, the scrubber guarantee schedules and two laboratories' test reports).",
           "**Analytical objective:** Data Extraction & Conformation (ETL).", "",
           "## 1. Final Recommendation", "",
           "**The 2027 Sulphur Dioxide Order lists %s boilers, %s, whose sulphur dioxide leaving the stack over 2026 "
           "was %s tonnes against the 250 tonne line; the other %s boilers are under it.**" % (
               WORDS[len(listed)], joined(listed), joined(t(B[x]["so2"]) for x in listed), WORDS[len(unlisted)]),
           "%s is the nearest to the line among the %s at %s tonnes, and %s the highest of the rest at %s. Not %s "
           "alone, which the removals the scrubbers showed at their 2026 performance tests give when carried across "
           "the year: %s consumed too little limestone for those removals, so their sulphur dioxide runs %s to %s "
           "times their tested figures. Not %s, which its design removal puts at %s tonnes: over the year its "
           "scrubber removed more than its design." % (
               near, WORDS[len(listed)], t(B[near]["so2"]), top_off, t(B[top_off]["so2"]), joined(dflt),
               "the scrubbers at " + joined(bypassed), "%.1f" % min(ratios), "%.1f" % max(ratios), design["name"],
               t(design["so2"])), "",
           "## 2. Critical Components", "",
           "1. Sulphur dioxide formed from the coal the eighteen boilers fired in 2026, less the ash's share, to the "
           "nearest 100: **%s tonnes**." % t(c["formed"]),
           "2. Sulphur dioxide the eighteen scrubbers removed over 2026, from the calcium carbonate they consumed, to "
           "the nearest 100: **%s tonnes**." % t(c["removed"]), "",
           "## 3. Step-by-Step Solution", "",
           "1. Took each boiler's coal burned from the four quarters of boiler_returns_2026.xlsx, quarters 1 and 2 on "
           "the 2019 template and 3 and 4 on the 2026 template: %s tonnes in all." % t(c["coal"]),
           "2. Took each site's sulphur as received from coal_deliveries_2026.csv, the deliveries received from 1 "
           "January to 31 December 2026 weighted by net tonnes (guidance section 4.2), each customer code put to its "
           "site through coal_supplier_customers.csv.",
           "3. Took off each boiler's sulphur retained in ash from permitted_boilers_register_2026.xlsx and converted "
           "at %s over %s: %s tonnes of sulphur dioxide formed." % (k["mso2"], k["ms"], t(c["formed"])),
           "4. Took each scrubber's limestone consumed as its 2026 tickets in limestone_tickets_2026.csv, put to "
           "permits by the Delivery points sheet of limestone_certificates_2026.xlsx, less its silo's change from the "
           "first quarter's opening to the fourth quarter's closing stock in the returns, each ticket at its ISO "
           "week's calcium carbonate in the same workbook.",
           "5. Converted each scrubber's calcium carbonate to sulphur dioxide removed at its operating stoichiometry in "
           "scrubber_guarantee_schedules.pdf, %s to %s moles of calcium carbonate per mole removed: %s tonnes." % (
               "%.2f" % k["ratios"][0], "%.2f" % k["ratios"][-1], t(c["removed"])),
           "6. Subtracted each boiler's removal from its sulphur dioxide formed and tested the remainder unrounded "
           "against 250 tonnes (the Order's note, section 2): %s boilers at or over the line." % WORDS[len(listed)],
           "7. For the ash, conformed whinmoss_invoice_lines_2026.xlsx, carnhope_jobs_2026.csv and "
           "pellrigg_dockets_2026.xlsx to the sites through ash_contractor_customers.csv, kept bottom and fly ash "
           "collected in 2026, read Carnhope's net weights in kilograms, and dropped every Whinmoss line whose "
           "reference is a Carnhope or Pellrigg job number, because that line bills the local contractor's own "
           "collection, counted on its record: each site's tonnes and recovery share below.",
           "8. The Order lists %s." % joined(listed), "",
           "## 4. Deliverable Answers", "",
           "### sulphur_dioxide_order_schedule_2027.xlsx", "",
           "1. Each boiler's sulphur dioxide leaving the stack in 2026, tonnes to the nearest 10, and whether the "
           "Order lists it, in the register's order:"]
    for x in order:
        out.append("   - %s: %s tonnes, %s" % (x, t(B[x]["so2"]), B[x]["listed"]))
    out.append("2. Each site's boiler ash taken off site in 2026 by the three contractors, tonnes to the nearest 10, "
               "and the share sent to recovery at Yarrdale Blocks or Velthwaite Cement Works, per cent to one "
               "decimal:")
    for s in f["ash_order"]:
        v = f["ash"][s]
        out.append("   - %s: %s tonnes, %.1f per cent" % (s, t(v["t"]), v["rec"]))
    out += ["", "### boiler_sulphur_dioxide_2026.png", "",
            "1. A horizontal bar chart of the eighteen boilers' 2026 sulphur dioxide leaving the stack, highest at the "
            "top, against a line at 250 tonnes, the %s listed boilers in red-brown and every bar labelled with its "
            "tonnes to the nearest 10." % WORDS[len(listed)], ""]
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(out))


if __name__ == "__main__":
    main()
