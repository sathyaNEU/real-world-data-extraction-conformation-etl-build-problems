"""submission.md, every figure from figures.json."""
import params as P

LN = {"N": "Crossmoor line", "E": "Ambrey line", "S": "Holm Ferry line"}


def n(v):
    return "{:,}".format(int(v))


def write(path, fig):
    st = fig["stations_r100"]
    order = sorted(fig["stations"], key=lambda c: -fig["stations"][c])
    pick, ru = fig["pick"], fig["runner_up"]
    others = [c for c in order if c not in (pick, ru)]
    g = fig["gates"]
    rp = fig["repay_gbp"]
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Urban & Regional Science (optimization: siting one platform dispatch team on a rail network).")
    L.append("**Analytical objective:** Opportunity Sizing & Decision Support.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Site the 2027 platform dispatch team at %s: it takes %s passenger-minutes of lateness a weekday off "
             "the network's trains, %s more than %s's %s.** Not %s, which removes the most overrun minutes on its own "
             "trains but whose units turn round with time to spare and pass almost none of it on; not Ambrey Parkway, "
             "whose "
             "longest dwells fall on the park-and-ride extras, whose units do not work again until the evening."
             % (pick, n(st[pick]), n(fig["gap"]), ru, n(st[ru]), ru))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. %s saves **%s** passenger-minutes per weekday across the network's weekday trains" % (pick, n(st[pick])))
    L.append("2. %s saves **%s** passenger-minutes per weekday" % (ru, n(st[ru])))
    L.append("3. The other shortlisted stations save %s" % ", ".join("%s **%s**" % (c, n(st[c])) for c in others))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Took the valuation from dispatch_team_brief_2027.docx section 3: passenger lateness on every weekday "
             "passenger train on the %d autumn 2026 weekdays as they ran, each passenger's minutes after the booked "
             "arrival where they leave the train, with the team removing three fifths of each train's dwell over its "
             "booked dwell at its station for trains booked to depart there from 06:30 up to 19:30." % fig["weekdays"])
    L.append("2. Joined each weekday's calls in train_running_autumn_2026.csv to working_timetable_autumn_2026.xlsx on "
             "headcode and TIPLOC, and weighted each train's arrival lateness at every station by its alighters in "
             "passenger_census_2026-10-13.csv, matched through station_register.csv.")
    L.append("3. Replayed each weekday with the team at each shortlisted station in turn: a train leaves that station "
             "earlier by three fifths of its overrun but never before its booked departure, keeps every later "
             "section's recorded running time, and leaves each later station at its booked time or its replayed "
             "arrival plus the dwell it recorded, whichever is later.")
    L.append("4. Followed each unit through its day by the running record's unit numbers: no working that left its "
             "origin late left sooner than four minutes after its unit's arrival, so a working that left late exactly "
             "four minutes after that arrival leaves four minutes after the unit's replayed arrival instead, not "
             "before its booked time, and the unit's later workings are replayed the same way.")
    L.append("5. Averaged the passenger lateness taken off over the %d weekdays: %s." %
             (fig["weekdays"], ", ".join("%s %s" % (c, n(st[c])) for c in order)))
    L.append("6. Gateline ask: differenced each array's cumulative counters in gateline_readings_2026-10-12_to_16.csv "
             "over 13 October 2026 in BST, adding %s across a wrap, resuming a restarted controller from the 02:00 "
             "reading it restored, and counting a tidal array's entries-counter passages in its exit-only hours as "
             "people leaving." % n(fig["constants"]["counter_wrap"]))
    L.append("7. Delay Repay ask: summed every approved payment row in delay_repay_claims_extract_2027-01-15.csv for "
             "journeys to or from RVC, appeal top-ups under the same claim_ref included; matched each claim to the train "
             "leaving its stated origin at its booked departure and calling at its destination, or the other way round "
             "where none does (a return ticket's claim names the ticket's stations); dated a claim whose journey date is "
             "the day it was first submitted, and whose train did not reach the destination 15 minutes late that day, "
             "by the last earlier weekday its train did; kept the weekdays from 7 September to 27 November 2026 and "
             "banded each claim by its train's lateness at the destination in the running record.")
    L.append("8. %s gets the team: %s passenger-minutes a weekday, %s ahead of %s." % (pick, n(st[pick]), n(fig["gap"]), ru))
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### dispatch_team_siting_2027.xlsx")
    L.append("")
    L.append("1. Weekday saving by shortlisted station, passenger-minutes to the nearest 100:")
    for c in order:
        L.append("   - %s: %s" % (c, n(st[c])))
    L.append("2. Pick %s (%s); runner-up %s (%s); gap %s passenger-minutes." % (pick, n(st[pick]), ru, n(st[ru]), n(fig["gap"])))
    L.append("3. Passengers through the gates at each gated shortlisted station on Tuesday 13 October 2026:")
    for s in P.GATED:
        L.append("   - %s: entered %s; left %s" % (s, n(g[s]["entered"]), n(g[s]["left"])))
    L.append("4. Delay Repay compensation paid, weekday journeys to or from Ravelstoke Central, 7 September to "
             "27 November 2026, pounds:")
    for ln in P.LINES:
        L.append("   - %s: 15 to 29 minutes £%s; 30 to 59 minutes £%s; 60 minutes or more £%s" %
                 (LN[ln], n(rp["%s|15 to 29" % ln]), n(rp["%s|30 to 59" % ln]), n(rp["%s|60 or more" % ln])))
    L.append("")
    L.append("### lateness_saved_by_station.png")
    L.append("")
    L.append("5. Ranked horizontal bar chart of every shortlisted station's weekday saving, %s highlighted at the top." % pick)
    L.append("")
    with open(path, "w") as fh:
        fh.write("\n".join(L))
