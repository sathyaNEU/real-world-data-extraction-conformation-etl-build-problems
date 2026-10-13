"""task131: write submission.md from generator/figures.json (every figure emitted, never typed).

    python3 task131/generator/writeup.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
NAMES = {"A": "Design A (Evening 3 to 9)", "B": "Design B (Evening 4 to 8)", "C": "Design C (Stepped)"}


def chg(v):
    return "lowers it by %d MW" % v if v > 0 else "raises it by %d MW" % -v


def money(v):
    return ("-$%.2f" % -v) if v < 0 else ("$%.2f" % v)


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    ch = f["change_mw"]
    lo, hi = f["hot_tmax_range"]
    pk = f["pulldown_kw"]
    L = []
    L.append("# task131 submission\n")
    L.append("## Tags\n")
    L.append("**Domain:** Energy Systems & Utilities (tariff and demand-response evaluation: reading a randomised summer "
             "trial of three peak-window residential tariffs for what each would do to an isolated town system's "
             "design-day maximum demand).")
    L.append("**Analytical objective:** Experiment & Causal Analysis (which trialled design, if any, flat-rate households "
             "move onto from 1 July 2027, judged by its effect on the 2027-28 summer maximum demand at 50%% probability "
             "of exceedance).\n" % ())
    L.append("## 1. Final Recommendation\n")
    L.append("**Move every flat-rate residential customer onto Design C (Stepped) from 1 July 2027: it lowers the "
             "2027-28 summer maximum demand at %d%% probability of exceedance by %d MW.**\n" % (f["poe"], ch["C"]))
    L.append("Not Design A, which would raise the maximum by %d MW once its households' pull-down after 9 p.m. is added "
             "to the design day; not Design B, which cuts the most inside its window yet would raise the maximum by %d MW, "
             "its pull-down landing in the half-hour from 8 p.m. Keeping the Home Plan leaves the maximum at %.1f MW.\n"
             % (-ch["A"], -ch["B"], f["md50_mw"]))
    L.append("## 2. Critical Components\n")
    L.append("1. The trial has **%d** workdays at the heat of the %.1f-degree design day, at %.1f to %.1f degrees (19 to "
             "23 January and 10 and 11 February 2026); no other workday was above %.1f degrees"
             % (f["n_hot"], f["design_tmax"], lo, hi, f["mild_max"]))
    L.append("2. On those days Design B's households drew **%.1f kW** more than the control households in the half-hour "
             "from 8 p.m., and Design A's **%.1f kW** more in the half-hour from 9 p.m." % (pk["B"], pk["A"]))
    L.append("3. With every half-hour's effect added to the design-day profile for the forecast's **%s** Home Plan "
             "customers, the maximum falls in the half-hour from **8 p.m.** under Designs B and C and from **9 p.m.** "
             "under Design A\n" % "{:,}".format(f["n_flat"]))
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Parsed the four MRP_NEM12 extracts: the latest update of each meter serial's day, an exchange day summed "
             "across its two meters, 15-minute reads paired into half-hours; household demand is E1 plus E2 less B1, kWh "
             "times two, in kW.")
    L.append("2. Followed each household in summer_pricing_trial_register.xlsx by customer number through "
             "account_tariff_history_2026-03-12.csv to the premise it held each day, every household in its assigned arm "
             "as section 6 of summer_pricing_trial_plan.pdf reads the trial.")
    L.append("3. Took the trial's workdays (weekdays other than public holidays, 1 December 2025 to 28 February 2026) "
             "at the heat of the %.1f-degree design day in murrandi_demand_forecast_2026.xlsx: %d, at %.1f to %.1f "
             "degrees in IDCJAC0010_013027_1800_Data.csv, no other workday above %.1f."
             % (f["design_tmax"], f["n_hot"], lo, hi, f["mild_max"]))
    L.append("4. For each design and half-hour, took its households' mean demand less the control households', averaged "
             "over those %d days." % f["n_hot"])
    L.append("5. Added %s times each half-hour's effect to the 2027-28 50%% POE design-day profile and took the highest "
             "half-hour: Design C lowers the %.1f MW maximum by %d MW, Design A raises it by %d MW and Design B by %d MW."
             % ("{:,}".format(f["n_flat"]), f["md50_mw"], ch["C"], -ch["A"], -ch["B"]))
    L.append("6. For the tables: each household's general-supply tariff on 28 February 2026, followed by customer number; "
             "its general-supply charges at the gazetted 2025-26 charges in residential_charges_2025-26.pdf on the days it "
             "was billed on its design, against the Home Plan for the same reads; and its first submitted survey response, "
             "telephone answers to Q4 coded in the order read.")
    L.append("7. Recommendation: Design C from 1 July 2027, %d MW off the 2027-28 maximum demand.\n" % ch["C"])
    L.append("## 4. Deliverable Answers\n")
    L.append("### tariff_default_advice_2027-28.pdf\n")
    L.append("1. The call: move every flat-rate residential customer onto Design C (Stepped) from 1 July 2027.")
    L.append("2. Each design's change to the 2027-28 summer maximum demand at %d%% probability of exceedance, nearest "
             "whole MW:" % f["poe"])
    for a in ("C", "A", "B"):
        L.append("   - %s: %s" % (NAMES[a], chg(ch[a])))
    L.append("3. Bar chart of the three changes, Design C highlighted, each bar labelled with its change.\n")
    L.append("### tariff_trial_tables_2025-26.xlsx\n")
    L.append("1. Households on 28 February 2026 (still billed on the design; back on the Home Plan at their own request; "
             "no longer our customers):")
    for a in ("A", "B", "C"):
        r = f["retention"][a]
        L.append("   - %s: %d; %d; %d" % (NAMES[a], r["still"], r["back"], r["gone"]))
    L.append("2. Charges over the trial (households charged more than the Home Plan would have charged for the same "
             "metered use; mean of that difference per trial household including GST, a negative difference a saving):")
    for a in ("A", "B", "C"):
        b = f["bills"][a]
        L.append("   - %s: %d; %s" % (NAMES[a], b["more"], money(b["mean"])))
    L.append("3. Households answering the March 2026 survey who said they were likely or very likely to stay on the "
             "design, share to one decimal place:")
    for a in ("A", "B", "C"):
        s = f["survey"][a]
        L.append("   - %s: %.1f per cent" % (NAMES[a], s["share"]))
    with open(os.path.join(TASK, "submission.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
