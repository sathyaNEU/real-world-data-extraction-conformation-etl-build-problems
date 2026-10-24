"""submission.md from figures.json: tags, the recommendation, its components, the steps and the deliverable answers."""
import params as P


def c(x):
    return "{:,}".format(int(x))


def m(x):
    return "%.1f" % x


def write(path, fig):
    F = P.FILES
    s = fig["sites"]
    t = []
    t.append("## Tags\n")
    t.append("**Domain:** Urban and regional science (accessibility, agglomeration and location analysis).")
    t.append("**Analytical objective:** Opportunity sizing and decision support.\n")
    t.append("## 1. Final Recommendation\n")
    t.append("**Marrable Foodstores should open S3, %s, which will add GBP %s million a year to the chain's contribution "
             "once it is trading.**" % (fig["site_name"], m(fig["add"])))
    t.append("The guests on Wrentoft Lakes Holiday Park's %s pitches live outside the region, so no census output area "
             "holds them, and at GBP %s of in-store grocery spend a pitch for a season they lift the store's sales to "
             "GBP %s million. Not S1 Bellingtoft, which leads on the residents' spend alone and adds GBP %s million. Not "
             "S2 Eastgate, which adds GBP %s million because over a third of its sales would come from our own "
             "stores.\n" % (c(fig["wrentoft_lakes_pitches"]), c(fig["V"]), m(fig["s3_sales"]), m(s["S1"]["add"]),
                            m(s["S2"]["add"])))
    t.append("## 2. Critical Components\n")
    t.append("1. The holiday parks are origins of grocery spend that the census does not count: Wrentoft Lakes Holiday "
             "Park, the largest with **%s** pitches, is nearer S3 than any other site." % c(fig["wrentoft_lakes_pitches"]))
    t.append("2. A pitch's guests spend **GBP %s** a season in store, measured from the out-of-region card spend at "
             "our ten stores." % c(fig["V"]))
    t.append("3. With the guests carried, S3 sells **GBP %s million** a year and adds **GBP %s million**; on the "
             "residents alone it adds **GBP %s million**, %s of six, and S1 leads at **GBP %s million**.\n"
             % (m(fig["s3_sales"]), m(fig["add"]), m(fig["s3_resident"]), fig["s3_resident_rank"], m(fig["resident_add"])))
    t.append("## 3. Step-by-Step Solution\n")
    t.append("1. Shared each output area's grocery spend (its households in %s, times the weekly spend in %s, times "
             "%d weeks and %d per cent in store) among the %d grocery stores of %d m2 or more in %s and %s, by floor "
             "area over exp(-%.2f x %.2f x straight-line km) from the output area's centroid in %s (%s): on residents "
             "alone S1 adds GBP %s million and S3 GBP %s million."
             % (F["households"], F["spend"], fig["weeks_year"], fig["instore_pct"], fig["n_stores_share"],
                fig["min_area"], F["voa_list"], F["voa_smv"], fig["beta"], fig["roadf"], F["pwc"], F["model"],
                m(fig["resident_add"]), m(fig["s3_resident"])))
    t.append("2. Took each of our stores' guest spend from %s: cardholders whose home sector is outside the %s "
             "postcode area, March to October, above the store's own November to February monthly level, divided "
             "by the store's card share in %s." % (F["cards"], fig["area_code"], F["estate"]))
    t.append("3. Divided our ten stores' guest spend by the pitches of the %d pitch-measured sites in %s, each "
             "weighted by the model's share of its spend going to our stores from its postcode in %s: GBP %s a pitch "
             "for a season." % (fig["n_park_sites"], F["voa_smv"], F["onspd"], c(fig["V"])))
    t.append("4. Added each park as an origin, its pitches times GBP %s at its postcode, and appraised each site by "
             "the model sheet's rule (%d per cent of its sales, less %d per cent of what it takes from our stores, "
             "less the running costs in %s): S3 sells GBP %s million and adds GBP %s million, S1 adds GBP %s million."
             % (c(fig["V"]), fig["margin_pct"], fig["margin_pct"], F["shortlist"], m(fig["s3_sales"]), m(fig["add"]),
                m(s["S1"]["add"])))
    t.append("5. Cases: summed the cases of the DEL stops in %s by store for UK arrival dates from 6 October 2025 to "
             "29 March 2026 and divided by %d, counting a load a store turned away once: a stop closed in under %d "
             "minutes plus %s of a minute a case had its cases taken back and delivered to the store the next day on a "
             "trip of their own, so it is left out." % (F["tms"], fig["weeks"], fig["turn_base_min"], fig["turn_min_per_case"]))
    t.append("6. Paid hours: paired each colleague's clock-ins and clock-outs in %s into shifts (a clock-in or "
             "clock-out with no partner is a shift whose other punch was forgotten), dated each shift by its clock-in "
             "(by its clock-out where there is none) and placed it at the store, in %s, of that punch's terminal, not "
             "the location column; took one of the colleague's lines in %s for each shift starting that date, since the "
             "report lists a night shift against both dates it covers at its full paid hours, summed paid_hours by "
             "store and divided by %d." % (F["punches"], F["terminals"], F["wfm"], fig["weeks"]))
    t.append("7. Buses: from %s and %s, the departures with pickup allowed from stops within %d m of the site's postcode "
             "by the clock on %s %d January 2027, which are that day's services up to 24:00 and the previous day's "
             "services from 24:00 on (a GTFS service day runs past midnight), each bus once by its block_id: the same "
             "block at the same stop and time is one departure (a jointly run route's journey listed in both feeds, "
             "and a weekday journey the Friday-late timetable lists again), while a second bus on the same timetable on "
             "a block of its own (a school-day duplicate) is another." % (F["gtfs_lb"], F["gtfs_pdc"], fig["radius_m"],
                                                                          fig["bus_weekday"], fig["bus_day"]))
    t.append("8. Recommended S3, %s: it adds GBP %s million a year against S1's GBP %s million.\n"
             % (fig["site_name"], m(fig["add"]), m(s["S1"]["add"])))
    t.append("## 4. Deliverable Answers\n")
    t.append("### marrable_site_appraisal_2027.xlsx\n")
    t.append("1. The site to open: S3, %s." % fig["site_name"])
    t.append("2. Its addition to the chain's annual contribution: GBP %s million." % m(fig["add"]))
    t.append("3. Cases a week the distribution centre delivered to each store, 6 October 2025 to 29 March 2026:")
    for k, v in fig["ask_a"].items():
        t.append("   - Store %s: %s cases" % (k, c(v)))
    t.append("4. Paid hours a week worked at each store, 6 October 2025 to 29 March 2026:")
    for k, v in fig["ask_b"].items():
        t.append("   - Store %s: %s hours" % (k, c(v)))
    t.append("5. Bus departures that pick up passengers from stops within %d metres on %s %d January 2027:" % (
        fig["radius_m"], fig["bus_weekday"], fig["bus_day"]))
    for k, v in fig["ask_c"].items():
        t.append("   - %s %s: %s" % (k, s[k]["name"], c(v)))
    t.append("\n### new_store_case_2027.docx\n")
    t.append("1. The case for opening S3, %s, which adds GBP %s million a year." % (fig["site_name"], m(fig["add"])))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(t) + "\n")
