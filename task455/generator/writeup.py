"""Write task455/submission.md from generator/figures.json: every figure in it comes from the build."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
ORDER = ["Brennock", "Caldmere", "Dunrath", "Eskwell", "Fennamore", "Quarrin", "Tolbeck"]


def n(x):
    return "{:,}".format(x)


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    c = f["counties"]
    y = f["y2025"]
    t = f["totals"]
    d1, d2, d3 = f["designated_order"]
    ru = f["runner_up"]
    by_rank = sorted(c, key=lambda k: c[k]["rank"])
    L = []
    L += ["## Tags", "",
          "**Domain:** Survey Research & Official Statistics (census, register and administrative data quality).",
          "**Analytical objective:** Data Extraction & Conformation (ETL).", ""]
    L += ["## 1. Final Recommendation", "",
          "**Commerce should designate %s, %s and %s as Formation Counties for 2027 to 2029.**" % (d1, d2, d3),
          "Their 2026 establishment birth rates are %.1f, %.1f and %.1f births per 100 establishments; %s is the "
          "runner-up at %.1f, %.1f below %s. Not Caldmere or Tolbeck, second and third on new employer accounts per "
          "100 establishments, whose %d and %d set-aside accounts continue businesses that operated before under "
          "another account (stores a buyer re-registered, businesses that moved into Tolbeck's enterprise park)."
          % (c[d1]["rate"], c[d2]["rate"], c[d3]["rate"], ru, c[ru]["rate"], f["gap"], d3, c["Caldmere"]["set_aside"],
             c["Tolbeck"]["set_aside"]), ""]
    L += ["## 2. Critical Components", "",
          "1. New 2026 employer accounts that continue a business that operated before: **%d** of **%d** (**%d** with a "
          "filed transfer, **%d** shown by the workforce)." % (t["filed_2026"] + t["workforce_2026"], t["new_2026"],
                                                              t["filed_2026"], t["workforce_2026"]),
          "2. 2026 births: %s." % ", ".join("%s **%d**" % (k, c[k]["births"]) for k in by_rank[:4]),
          "3. Establishments employing in the fourth quarter of 2025: %s." % ", ".join(
              "%s **%s**" % (k, n(c[k]["base"])) for k in by_rank[:4]),
          "4. 2026 birth rates per 100: %s." % ", ".join("%s **%.1f**" % (k, c[k]["rate"]) for k in by_rank[:4]), ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. In qcew_private_establishments_2024q4_2026q4.csv, found each account's first month with employment: %d "
          "accounts first reported employment in 2026 and none before (the guideline's birth definition)." % t["new_2026"],
          "2. Set aside the %d of them whose row in ui_employer_register_extract_2027-05-14.csv names a predecessor "
          "account." % t["filed_2026"],
          "3. In ui_wage_records_2024q4_2026q4.txt, set aside the %d others where more than half of the workers the "
          "account paid in its first quarter with employment were paid the quarter before by one account that reported "
          "no employment from that quarter on." % t["workforce_2026"],
          "4. Counted the %d births by the register's county (where the worksite lies, per the guideline) and divided by "
          "each county's establishments with employment in a month of the fourth quarter of 2025 (the guideline's "
          "base), %s in the region."
          % (t["births_2026"], n(t["base_2025q4"])),
          "5. Ranked the rates unrounded, as the guideline says: %s %.1f, %s %.1f, %s %.1f, then %s %.1f, %.1f below %s."
          % (d1, c[d1]["rate"], d2, c[d2]["rate"], d3, c[d3]["rate"], ru, c[ru]["rate"], f["gap"], d3),
          "6. Applied steps 1 to 3 to 2025, taking only accounts whose register liability date (first payroll) is in "
          "2025: %d births, over %s establishments with employment in the fourth quarter of 2024 counted by the "
          "register's county." % (t["births_2025"], n(t["base_2024q4"])),
          "7. Counted %d deaths in 2025: last month with employment in 2025, none in 2026, and not the predecessor or "
          "the workforce source of a new account." % t["deaths_2025"],
          "8. Designated %s, %s and %s." % (d1, d2, d3), ""]
    L += ["## 4. Deliverable Answers", "", "### formation_county_designation_2027.pdf", "",
          "1. Designation: %s, %s and %s." % (d1, d2, d3),
          "2. 2026 by county (births; new accounts set aside as businesses that operated before; birth rate per 100):"]
    for k in by_rank:
        L.append("   - %s: %d births; %d set aside; %.1f" % (k, c[k]["births"], c[k]["set_aside"], c[k]["rate"]))
    L += ["3. Runner-up: %s at %.1f, %.1f below %s." % (ru, c[ru]["rate"], f["gap"], d3),
          "4. Chart: paired bars of each county's 2025 births and deaths, labelled with their counts, on page 2.", "",
          "### lornock_establishment_births_2026.xlsx", "",
          "1. Each of the %d new 2026 accounts with its county and whether it is a birth (sheet New accounts 2026)."
          % f["new_accounts"],
          "2. The 2026 county figures as in the memo (sheet Designation 2026).",
          "3. 2025 births (birth rate per 100 establishments employing in the fourth quarter of 2024):"]
    for k in ORDER:
        L.append("   - %s: %d (%.1f)" % (k, y[k]["births"], y[k]["birth_rate"]))
    L.append("4. 2025 deaths (death rate per 100 establishments employing in the fourth quarter of 2024):")
    for k in ORDER:
        L.append("   - %s: %d (%.1f)" % (k, y[k]["deaths"], y[k]["death_rate"]))
    L.append("")
    out = "\n".join(L)
    assert "—" not in out and "–" not in out
    with open(os.path.join(TASK, "submission.md"), "w") as fh:
        fh.write(out)
    return out


if __name__ == "__main__":
    print(main())
