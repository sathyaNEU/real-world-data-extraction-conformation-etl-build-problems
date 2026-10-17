"""submission.md, drafted from generator/figures.json: every figure in it is emitted, none typed."""
import json
import os

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))


def _and(names):
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def _p(x):
    return "%.2f" % x


def _d(x):
    return "{:,}".format(int(x))


def write(fig_path, out_path):
    F = json.load(open(fig_path))
    cv = F["covers"]
    buy, dec = F["call"]["buy"], F["call"]["decline"]
    rec = F["recovered"]
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** General Statistics & Data Science (data integration: each county's dryland grain sorghum "
             "yield history conformed from a state statistics service's county and district estimates in two "
             "downloads, the years it withheld recovered from the district totals).")
    L.append("**Analytical objective:** Data Extraction & Conformation (ETL).")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Buy the %s covers and decline %s's.**" % (_and(buy), "'s and ".join(dec)))
    L.append("Their quoted rates are %s times their expected losses of %s per cent, under the policy's 1.4; %s. "
             "Not the published years alone, which leave out the %d county-years the service withheld and decline all "
             "five covers; not filling those years from the district's yield or the county's published years, which "
             "still declines all five; not reading them as total failures, which buys Tresham's too." % (
                 _and([_p(cv[c]["multiple"]) for c in buy]), _and([_p(cv[c]["expected_loss"]) for c in buy]),
                 "; ".join("%s's runs %s times its %s" % (c, _p(cv[c]["multiple"]), _p(cv[c]["expected_loss"]))
                           for c in dec), F["withheld_count"]))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    def recs(c):
        return ", ".join("**%.1f** (%s)" % (rec["%s %s" % (c, y)]["yld"], y)
                         for y in sorted(k.split()[1] for k in rec if k.split()[0] == c))
    L.append("1. Withheld years recovered from the district totals, bushels per harvested acre: Ardley %s; Elster %s; "
             "Pallard %s; Tresham %s." % (recs("Ardley"), recs("Elster"), recs("Pallard"), recs("Tresham")))
    L.append("2. Expected loss, per cent of liability: %s." % "; ".join(
        "%s **%s**" % (c, _p(cv[c]["expected_loss"])) for c in W.MEMBERS))
    L.append("3. Quoted rate as a multiple of expected loss: %s." % "; ".join(
        "%s **%s**" % (c, _p(cv[c]["multiple"])) for c in W.MEMBERS))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Took non-irrigated grain sorghum harvested acres, production and yield for every county and district "
             "from %s and %s, the October 2026 download for the years it holds (methods note 4.1) and the 2008 "
             "district recode applied (5.1): %d county-years of the five counties are withheld (S)." % (
                 W.FILES["pull24"], W.FILES["pull26"], F["withheld_count"]))
    L.append("2. Recovered each withheld county-year as its district's harvested acres and production less those of "
             "the district's published counties (methods note 2.1), yield their ratio: %s." % "; ".join(
                 "%s %s" % (k, "%.1f" % v["yld"]) for k, v in sorted(rec.items())))
    L.append("3. Brought each crop year's yield, 1991 to 2025, to 2027 by adding the trend in %s for each year, took "
             "each year's indemnity share against 90 per cent of the expected 2027 yield and averaged the 35 shares "
             "(risk policy 5.3): expected losses %s per cent." % (
                 W.FILES["terms"], ", ".join("%s %s" % (c, _p(cv[c]["expected_loss"])) for c in W.MEMBERS)))
    L.append("4. Set each quoted rate in %s against 1.4 times the expected loss (risk policy 5.2): buy %s, decline %s." % (
        W.FILES["quotes"], _and(buy), _and(dec)))
    L.append("5. Summed the non-irrigated acres in %s submitted before the 5:00 p.m. Central close of 30 October 2026 "
             "(22:00 UTC; %s), each field's latest submission, by the field's county: %s acres; each cover's liability "
             "is its acres times its expected yield times 90 per cent times $%s a bushel (the term sheet's $%s per "
             "hundredweight at %d pounds), its premium the quoted rate times the liability." % (
                 W.FILES["enrol"], W.FILES["notice"],
                 ", ".join("%s %s" % (c, "{:,.1f}".format(F["acres"][c])) for c in W.MEMBERS),
                 "%.2f" % F["price_per_bu"], "%.2f" % F["stated"]["price_cwt"], F["stated"]["bushel_lb"]))
    L.append("6. Converted the grain sorghum tickets in %s to bushels at 14 per cent moisture by the conversion in %s, "
             "left out the terminal's tickets written against a transfer in %s and summed by origin county: %s bushels "
             "received, divided by each county's 2016 to 2020 all-practices production in the October 2026 download." % (
                 W.FILES["tickets"], W.FILES["dict"], W.FILES["transfers"],
                 ", ".join("%s %s" % (c, _d(F["receipts_bu"][c])) for c in W.MEMBERS)))
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### %s" % W.GOLDEN["workbook"])
    L.append("")
    L.append("1. Buy the %s covers; decline %s." % (_and(buy), _and(dec)))
    L.append("2. Each cover's expected loss, quoted rate, quoted rate as a multiple of the expected loss, the quoted "
             "rate at which its call changes (per cent of liability; the multiple to two decimals) and its call:")
    for c in W.MEMBERS:
        L.append("   - %s: %s, %s, %s, %s, %s" % (c, _p(cv[c]["expected_loss"]), _p(cv[c]["quote"]), _p(cv[c]["multiple"]),
                                                _p(cv[c]["change_rate"]), cv[c]["call"].lower()))
    L.append("3. Each cover's 2027 liability and premium, dollars to the nearest hundred:")
    for c in W.MEMBERS:
        L.append("   - %s: %s and %s" % (c, _d(F["liability"][c]), _d(F["premium"][c])))
    L.append("4. The cooperative's 2016 to 2020 grain sorghum receipts from each county as a share of the county's "
             "grain sorghum production (all practices), per cent to one decimal:")
    for c in W.MEMBERS:
        L.append("   - %s: %.1f" % (c, F["receipts_share"][c]))
    L.append("5. Chart on the Covers sheet: clustered columns of each cover's quoted rate beside the rate at which its "
             "call changes, both labelled in per cent of liability.")
    L.append("")
    L.append("### %s" % W.GOLDEN["record"])
    L.append("")
    L.append("1. %d rows, one per county and crop year 1991 to 2025, with harvested acres, production, yield and "
             "source; the withheld county-years recovered from district totals (harvested acres, bushels, bushels per "
             "acre):" % F["record_rows"])
    for k, v in sorted(rec.items()):
        L.append("   - %s: %s, %s, %.1f" % (k, _d(v["harvested"]), _d(v["production"]), v["yld"]))
    txt = "\n".join(L) + "\n"
    assert "—" not in txt and "–" not in txt
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(txt)
