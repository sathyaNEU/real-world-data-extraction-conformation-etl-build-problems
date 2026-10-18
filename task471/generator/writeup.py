"""submission.md, drafted from generator/figures.json: every figure the write-up states comes from there."""
import json

import world as W


def _join(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def write(fig_path, out_path):
    f = json.load(open(fig_path, encoding="utf-8"))
    t3 = f["three"]
    fo = f["first_left_out"]
    names = [r["name"] for r in t3]
    E = f["entries"]
    lines = [
        "## Tags",
        "",
        "**Domain:** Survey Research & Official Statistics (register and administrative data quality: a parking "
        "revenue control system's register of entries completed by a card survey of the parked cars, whose replies "
        "come back only when the car leaves).",
        "**Analytical objective:** Data Extraction & Conformation (ETL).",
        "",
        "## 1. Final Recommendation",
        "",
        "**The 2027 pitch for new nonstop service from Kessick Valley Regional should carry %s.**" % _join(names),
        "They carried %s, %s and %s of the service area's 2026 trips parked at Brennick International; %s, the first "
        "market left out, carried %s, %s below %s. Not %s, which each wave's returned cards expanded to its quarter "
        "give, because a card comes back only when its car leaves and each wave's boxes were taken in on the night of "
        "the second day after its last handout, so the long stays' cards handed in a wave's later days never came "
        "back." % (t3[0]["trips"], t3[1]["trips"], t3[2]["trips"], fo["name"], fo["trips"], f["gap"], t3[2]["name"],
                   _join(f["default_three"])),
        "",
        "## 2. Critical Components",
        "",
        "1. Transient entries in Economy C, Economy D and Long-Term, 2026: first quarter **%s**, second **%s**, third "
        "**%s**, fourth **%s**." % (E["Q1"], E["Q2"], E["Q3"], E["Q4"]),
        "2. Trips, 2026: %s." % _join(["%s **%s**" % (r["name"], r["trips"]) for r in t3]),
        "3. First market left out: %s, **%s** trips, **%s** below %s." % (fo["name"], fo["trips"], f["gap"],
                                                                        t3[2]["name"]),
        "",
        "## 3. Step-by-Step Solution",
        "",
        "1. Read %s, dropped the %s rows that repeat a card number (keying batch %s exported twice), kept the cards "
        "whose home ZIP's first five digits are on %s and gave each card the city market of its destination_code "
        "through %s." % (W.FILES["cards"], f["dup_rows"], f["dup_batch"], W.FILES["zips"], W.FILES["markets"]),
        "2. Took the candidates as Appendix A's shortlist in %s less %s, served seasonally at Sanford in %s (section "
        "3.1): %d markets." % (W.FILES["standard"], _join(f["served_shortlisted"]), W.FILES["schedule"],
                               f["candidates"]),
        "3. Found each card's handout day from its number in %s, and each wave's last box collection, day %s of the "
        "wave, in Table 1 of %s." % (W.FILES["handout"], f["close_day"], W.FILES["methods"]),
        "4. Weighted each card by its wave's cards handed over the cards handed on the days from which a stay of its "
        "nights could end by the last box collection, since a card comes back only when its car leaves.",
        "5. Expanded each candidate's share of each wave's weighted cards (every card in the denominator) to its "
        "quarter's transient entries in Economy C, Economy D and Long-Term from the four extracts (standard 2.1, 2.4) "
        "and added the quarters.",
        "6. Counted passengers the same way, each card's party being its Q4 answer in %s (the numbers written added, "
        "\"me\" one)." % W.FILES["verbatims"],
        "7. Ranked the candidates on trips: %s lead, and %s is first left out, %s trips below %s." % (
            _join(names), fo["name"], f["gap"], t3[2]["name"]),
        "8. Recommended %s for the 2027 pitch (standard 4.1)." % _join(names),
        "",
        "## 4. Deliverable Answers",
        "",
        "### %s" % W.GOLDEN["csv"],
        "",
        "1. Each candidate market's 2026 trips from the service area parked at Brennick and the passengers they "
        "carried, nearest hundred:",
    ]
    for r in f["markets"]:
        lines.append("   - %s (%s): %s trips, %s passengers" % (r["name"], r["code"], r["trips"], r["passengers"]))
    lines += [
        "",
        "### %s" % W.GOLDEN["brief"],
        "",
        "1. The three markets: %s." % _join(names),
        "2. First market left out: %s, %s trips, %s trips below %s." % (fo["name"], fo["trips"], f["gap"],
                                                                     t3[2]["name"]),
        "3. Bar chart of the %d candidate markets' 2026 trips, the three marked." % f["candidates"],
        "",
    ]
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
