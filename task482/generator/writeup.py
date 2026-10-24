"""submission.md from generator/figures.json: the five blocks, every figure taken from the generator's own output."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
QN = {1: "Q1 (July to September 2025)", 2: "Q2 (October to December 2025)", 3: "Q3 (January to March 2026)",
      4: "Q4 (April to June 2026)"}


def c(n):
    return format(n, ",")


def joined(xs):
    xs = list(xs)
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    C = f["cities"]
    order = f["order"]
    q = f["call"]["qualify"]
    no = [n for n in order if n not in q]
    s = f["steps"]
    out = ["## Tags", "",
           "**Domain:** Survey Research & Official Statistics, census, register and administrative data quality (a state "
           "demographer's 2026 peak-season populations for the eight cities of a lake basin under a seasonal aid "
           "statute, conformed from its resident estimates, seven treatment plants' operating reports in two "
           "layouts and a joint plant's member meters, the basin's lodging fee returns and two booking platforms' "
           "remittance files).",
           "**Analytical objective:** Data Extraction & Conformation (ETL).", "",
           "## 1. Final Recommendation", "",
           "**%s qualify for 2027 Seasonal Communities Aid, USD %s each; %s do not.**" % (
               joined(q), c(f["call"]["share"]), joined(no)),
           "Each of the %d carried at least three times its residents on an average day of its busiest month, counted "
           "by the load its sewer delivered to its plant divided by the load each resident carries in the winter "
           "months. Not %s alone: residents plus the paid stays the returns and platforms record put only those two "
           "over, because the owners in their cottages and the residents' guests stay where no stay is recorded." % (
               s["qualify_n"], joined(s["records_qualify"])), "",
           "## 2. Critical Components", "",
           "1. Average population present in the busiest month of the measurement year: %s." % "; ".join(
               "%s **%s** (%s)" % (n, c(C[n]["present"]), C[n]["busiest"]) for n in order),
           "2. Three times the 1 July 2026 resident population: %s." % "; ".join(
               "%s **%s**" % (n, c(C[n]["three_x"])) for n in order), "",
           "## 3. Step-by-Step Solution", "",
           "1. Took each city's 1 July 2026 resident population from quillmere_county_population_estimates_2024_2026.csv "
           "(Pinehold on its 2025 boundary): %s." % "; ".join("%s %s" % (n, c(C[n]["residents"])) for n in order),
           "2. Built each plant's monthly influent BOD load, the average daily flow in MGD times the BOD in mg/L times "
           "8.34, from the e-reporting export (the latest accepted submission for each period) and the pond systems' "
           "operating reports, giving Esker Narrows and Hollin Bay the Narrows joint plant's BOD at each city's "
           "member-meter flow.",
           "3. Divided each city's January to April 2026 load by its residents plus the paid guests the fee returns "
           "and both platforms' stays put in town on an average day of those months: the load each person carries, "
           "%s lb of BOD a day in every city." % f["steps"]["lpp"],
           "4. Divided each month's load from October 2025 to September 2026 by that load per person to get the "
           "average population present, took the highest month and compared it with three times residents: %s "
           "qualify, the USD %s split equally." % (joined(q), c(f["call"]["appropriation"])),
           "5. For the fee, took each return for its period (an amended return replacing the earlier one, a "
           "supplemental return added to it) and each platform stay's guests on each night falling in the quarter at "
           "the rate in force that night, counting Kettle & Pine's nights back from the departure date its reservation "
           "reference carries (R and the departure as YYMMDD; its reporting period is the month after that date, and "
           "the fee it remitted on the stays across 1 January 2026 matches only that reading).",
           "6. For phosphorus, summed each month's average daily effluent flow (MGD) times total phosphorus (mg/L) times "
           "8.34 times the days of the month, the e-reporting plants on their latest accepted submission (the "
           "revisions returned for correction after acceptance left out) and the pond systems' flow read as the "
           "month's average, as ponds that hold the year's wastewater must: so read they released %d per cent or more "
           "of their 2025 inflow, against %d per cent or less at the days discharged." % (
               s["pond_release_month"], s["pond_release_days"]),
           "", "## 4. Deliverable Answers", "",
           "### seasonal_communities_aid_2027_certification.xlsx", "",
           "1. Certification, one row per city (busiest month, average population present to the nearest thousand, "
           "whether at least three times residents, aid):"]
    for n in order:
        x = C[n]
        out.append("   - %s: %s, %s, %s, USD %s" % (n, x["busiest"], c(x["present"]), "yes" if x["qualifies"] else "no",
                                                    c(x["aid"])))
    out.append("2. Lake Protection Fee generated by stays in fiscal 2026, by city and quarter, whole dollars:")
    for n in order:
        a = f["ask_a"][n]
        out.append("   - %s: Q1 USD %s, Q2 USD %s, Q3 USD %s, Q4 USD %s" % (n, c(a["q1"]), c(a["q2"]), c(a["q3"]),
                                                                          c(a["q4"])))
    out.append("3. Total phosphorus discharged in 2025, pounds, by half-year:")
    for n in f["plants"]:
        b = f["ask_b"][n]
        out.append("   - %s: January to June %.1f, July to December %.1f" % (
            "Narrows joint plant" if n == "Narrows" else n, b["h1"], b["h2"]))
    out += ["", "### busiest_month_population_2026.png", "",
            "1. Horizontal bar chart of each city's average population present in its busiest month, with a "
            "marker at three times its residents and each city labelled as qualifying or not, the %d qualifying "
            "cities first." % s["qualify_n"]]
    with open(os.path.join(TASK, "submission.md"), "w") as fh:
        fh.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
