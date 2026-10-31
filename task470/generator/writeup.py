"""submission.md, drafted from generator/figures.json: every figure the write-up states comes from there."""
import json

import world as W


def _join(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def write(fig_path, out_path):
    f = json.load(open(fig_path, encoding="utf-8"))
    q = f["qualifying"]
    rv = f["rivals"]
    t = f["totals"]
    lines = [
        "## Tags",
        "",
        "**Domain:** Survey Research & Official Statistics (census, register and administrative data quality: a "
        "register-based dwelling statistic conformed from the cadastre, the meter data hub's metering points and hourly "
        "values, the population register and the land, business and shareholder registers).",
        "**Analytical objective:** Data Extraction & Conformation (ETL).",
        "",
        "## 1. Final Recommendation",
        "",
        "**%s of the ten municipalities qualify for the 2027 grant: %s.**" % (
            f["count_word"], _join(["%s (%s)" % (r["name"], r["nr"]) for r in q])),
        "Their vacancy shares run from %s to %s per cent against the regulation's %s; the highest share below the line "
        "is %s's %s per cent. Not none, which a consumption floor anywhere from %s to %s kWh a day gives, because an "
        "empty dwelling in November is left heated and uses more electricity than many lived-in ones; and not all "
        "%d, which the population register's empty dwellings give, because the regulation counts who lived there, "
        "not who was registered." % (
            min(r["share"] for r in q), max(r["share"] for r in q), f["threshold"], f["highest_below"]["name"],
            f["highest_below"]["share"], rv["floor_low"], rv["floor_high"], rv["register_count"]),
        "",
        "## 2. Critical Components",
        "",
        "1. Counted dwellings in the county: **%s**; vacant in the fortnight: **%s**." % (t["counted"], t["vacant"]),
        "2. A dwelling was lived in when, on at least one day, its morning or evening use rose above its own night-time "
        "use by more than **%s kWh** an hour; vacant when no day did." % f["cut"],
        "3. Vacant dwellings still carrying a registered resident on 1 November: **%s**; lived-in dwellings with "
        "nobody registered: **%s**." % (f["vacant_registered"], f["lived_unregistered"]),
        "",
        "## 3. Step-by-Step Solution",
        "",
        "1. Took the cadastre's units of type Bolig in use on or before 1 November 2026 (Section 3): %s dwellings." % (
            t["counted"]),
        "2. Joined each to its household metering points by bruksenhet_id, else by municipality and address for a "
        "single-unit house; Snøholt's points carry Fjordeid's old municipality number.",
        "3. Put the hourly values on Norwegian time (UTC+1), kept the later delivery where an estimated day was "
        "replaced, and added a dwelling's two points where its meter changed.",
        "4. For each day took the mean of 06 to 09 and of 16 to 22 against the mean of 01 to 05; a rise above %s kWh "
        "on any day marks the dwelling as lived in (Section 4: nobody lived in it on any day)." % f["cut"],
        "5. Divided each municipality's vacant dwellings by its counted dwellings, rounded to one decimal, and "
        "designated those at 5.0 per cent or more (Section 6).",
        "6. Rolled the population register of 5 January 2027 back to 1 November by undoing every later event, reading "
        "the November block renumberings as a change of unit number and the earlier events' old numbers as the "
        "renumbered flats; ages on 1 November.",
        "7. Rolled the land register back to 1 November by tinglyst date and counted the dwellings held by the "
        "municipality, its KF or a company whose shares it holds all of with its own companies, titles without an "
        "organisation number in the municipality's own name included.",
        "",
        "## 4. Deliverable Answers",
        "",
        "### %s" % W.GOLDEN["xlsx"],
        "",
        "1. Counted dwellings listed: %s, of which vacant: %s; persons registered on 1 November 2026 across them: %s." % (
            t["counted"], t["vacant"], t["persons"]),
        "2. Vacant dwellings and vacancy share by municipality:",
    ]
    for m in f["municipalities"]:
        lines.append("   - %s (%s): %s of %s counted dwellings, %s per cent" % (m["name"], m["nr"], m["vacant"],
                                                                              m["counted"], m["share"]))
    lines += [
        "",
        "### %s" % W.GOLDEN["docx"],
        "",
        "1. Qualifying municipalities: %s." % _join(["%s (%s per cent)" % (r["name"], r["share"]) for r in q]),
        "2. Bar chart of the ten municipalities' vacancy shares against the %s per cent threshold, the qualifying "
        "municipalities highlighted." % f["threshold"],
        "3. Persons registered in the counted dwellings on 1 November 2026, under 18, 18 to 66, 67 and over:",
    ]
    for r in f["ask_a"]:
        lines.append("   - %s (%s): %s, %s, %s" % (r["name"], r["nr"], r["under_18"], r["age_18_66"], r["age_67"]))
    lines.append("4. Counted dwellings held on the land register on 1 November 2026 by the municipality or a company it "
                 "owns:")
    for r in f["ask_b"]:
        lines.append("   - %s (%s): %s" % (r["name"], r["nr"], r["held"]))
    lines.append("")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
