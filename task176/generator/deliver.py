"""task176 deliverables: the golden workbook fcc_closures_2027.xlsx, generator/figures.json and submission.md, every
figure computed here from the shipped files through calc.py."""
from __future__ import annotations

import json
import os

import common as C
import calc
import postprocess as PP

SLUG = {r: "R%d_%s" % (r, C.REGIONS[r].split()[-1]) for r in C.REGIONS}


def history(homes):
    import datetime as dt
    out = []
    for y in range(2016, 2027):
        d0, d1 = dt.date(y, 1, 1), dt.date(y, 12, 31)
        op = sum(1 for h in homes.values() if h["first"] < d0 and (h["close"] is None or h["close"] >= d0))
        cl = sum(1 for h in homes.values() if h["close"] is not None and d0 <= h["close"] <= d1)
        out.append((y, op, cl))
    return out


def compute(target):
    g = calc.golden(target)
    d = calc.default_route(g)
    a = calc.ask_child_days(target)
    b = calc.ask_money(target)
    return dict(
        golden=g["golden"], call=C.rnd(g["golden"], 50), stock=g["stock"], nk=g["nk"], ksummers=g["ksummers"],
        kcloses=g["kcloses"], pk=g["pk"], default=d, default_r=C.rnd(d, 50),
        a={k: a[k] for k in sorted(a)}, b={k: int(round(b[k])) for k in sorted(b)}, b_raw=b, history=history(g["homes"]))


def figures(x):
    f = {"call": {"closures_2027": x["call"]}, "cc1": x["stock"], "cc2": x["nk"], "cc3": x["ksummers"],
         "cc4": int(round(100 * x["pk"])), "cc5": x["kcloses"], "alt_tenure": x["default_r"],
         "constants": {"as_of_day": C.RECORD_END.day, "rounding_step": 50, "age_terms": list(calc.AGE_TERMS),
                       "region_numbers": sorted(C.REGIONS)}}
    f["a_statewide"] = {"H1": x["a"][1], "H2": x["a"][2]}
    for r in C.REGIONS:
        f["b_" + SLUG[r]] = {"Q%d" % q: x["b"][(r, q)] for q in (1, 2, 3, 4)}
    return f


def n(v):
    return "{:,}".format(v)


def submission(x):
    reg = C.REGIONS
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Sociology & Demography (event history and life course analysis).")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**About %s of the %s family child care homes licensed in Allerton on 31 December 2026 will close during "
             "2027, to the nearest 50.**" % (n(x["call"]), n(x["stock"])))
    L.append("%s of those homes reach, in 2027, the summer before their provider's youngest own child starts kindergarten, "
             "the summer in which %d per cent of the record's homes in that position closed. Not %s, the forecast from "
             "closure rates by years licensed, which puts the 2023 start-up grant round's homes, now in their fourth "
             "year, at the closure rate of homes that far into their licence, when most of their providers' youngest "
             "children were babies in 2023 and reach kindergarten together in September 2027." % (n(x["nk"]), round(100 * x["pk"]), n(x["default_r"])))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. Homes licensed on 31 December 2026: **%s**." % n(x["stock"]))
    L.append("2. Of those, homes whose provider's youngest own child living in the home starts kindergarten in "
             "September 2027 (turns five on or before 1 September 2027, after 1 September 2026): **%s**." % n(x["nk"]))
    L.append("3. Homes in the record open on 1 June of the summer before their youngest own child's kindergarten year, "
             "2016 to 2026: **%s**, of which **%s per cent** closed by 31 August." % (n(x["ksummers"]), round(100 * x["pk"])))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Mapped the worksheets filed before 1 July 2019 to current licence numbers through "
             "licence_number_crosswalk_2019.csv, read both relationship code sets and date formats, and kept each "
             "home's own children living in the home (relationship C or OWN CHILD, lives_in_home Y), one per initials "
             "and birth date.")
    L.append("2. Built home-months from January 2016 to December 2026 from fcc_licence_extract_20261231.csv (each "
             "home from the month after first issue or January 2016, to its closure month or December 2026), with the "
             "home's year of tenure, the provider's age of 63 or more and 68 or more, the June to August months, and "
             "whether the month falls in June to August of the year the youngest own child born by then starts "
             "kindergarten (the school-age rule in ccap_provider_payment_policy_2026.pdf, section 6).")
    L.append("3. Fitted a monthly Poisson model of closure on those terms: the kindergarten summer, not the years "
             "licensed, carries the closures of parent-run homes (%s of %s such homes closed that summer)."
             % (n(x["kcloses"]), n(x["ksummers"])))
    L.append("4. Applied the model month by month through 2027 to the %s homes licensed on 31 December 2026, "
             "%s of them in their youngest's kindergarten summer, and summed each home's chance of closing: %s to the "
             "nearest 50." % (n(x["stock"]), n(x["nk"]), n(x["call"])))
    L.append("5. Child-days (ccap_payment_lines_2026.csv): kept SFCC and LFCC lines of remittances not voided, "
             "expanded each line to its Monday to Friday days in 2026, and counted each child and day once.")
    L.append("6. Money (ccap_payment_lines_2026.csv): kept SFCC and LFCC remittances paid in the 2026 runs and not voided, "
             "took each remittance once as its number, run date and county office, and credited it to the region of the "
             "home that gave the care (licence extract county). A remittance carrying homes in more than one region was "
             "shared by its lines' pay (the section 5 rate prorated by the line's days over the month's Monday to Friday "
             "days), which sums to its amount; summed by the quarter of the run date.")
    L.append("7. Allerton should plan for about %s homes closing during 2027." % n(x["call"]))
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### %s" % C.DELIVERABLE)
    L.append("")
    L.append("1. Homes licensed on 31 December 2026 that will close during 2027, to the nearest 50: %s." % n(x["call"]))
    L.append("2. Child-days of subsidised care in family child care homes in Allerton, a child counted once on a day: "
             "first half of 2026 %s, second half %s." % (n(x["a"][1]), n(x["a"][2])))
    L.append("3. Money the subsidy paid to family child care homes, by the region of the home and quarter of the 2026 payment run, "
             "nearest dollar, first to fourth quarter:")
    for r in reg:
        L.append("   - %s: USD %s" % (reg[r], ", ".join(n(x["b"][(r, q)]) for q in (1, 2, 3, 4))))
    return "\n".join(L) + "\n"


def workbook(path, x):
    import xlsxwriter
    wb = xlsxwriter.Workbook(path)
    title = wb.add_format({"bold": True, "font_size": 13})
    sub = wb.add_format({"italic": True, "font_color": "#555555"})
    hf = wb.add_format({"bold": True, "bg_color": "#D9E1F2", "border": 1, "text_wrap": True, "valign": "top"})
    nf = wb.add_format({"num_format": "#,##0"})
    bold_n = wb.add_format({"num_format": "#,##0", "bold": True, "top": 1})
    bold = wb.add_format({"bold": True, "top": 1})
    big = wb.add_format({"num_format": "#,##0", "bold": True, "font_size": 14, "bg_color": "#FFF2CC", "border": 1})
    wrap = wb.add_format({"text_wrap": True, "valign": "top"})

    ws = wb.add_worksheet("Forecast 2027")
    ws.write(0, 0, "About %s of the %s licensed family child care homes are expected to close during 2027"
             % (n(x["call"]), n(x["stock"])), title)
    ws.write(1, 0, "Office of Child Care, supply and planning. Input to the 2027 Home Child Care Start-Up Grant round and the "
                   "supply report due 1 February 2027. Licensing record to 31 December 2026.", sub)
    ws.write(3, 0, "Homes licensed on 31 December 2026 (small and large)")
    ws.write_number(3, 1, x["stock"], nf)
    ws.write(4, 0, "Of which, provider's youngest own child living in the home starts kindergarten in September 2027")
    ws.write_number(4, 1, x["nk"], nf)
    ws.write(6, 0, "Homes expected to close during 2027, to the nearest 50", wb.add_format({"bold": True}))
    ws.write_number(6, 1, x["call"], big)
    ws.write(8, 0, "Method. Monthly closure chance for each home from a Poisson model fitted on home-months January 2016 to "
                   "December 2026: year of licence, provider aged 63 or more and 68 or more, June to August, and the June "
                   "to August before the provider's youngest own child starts kindergarten. Each home licensed on 31 "
                   "December 2026 is carried month by month through 2027 and its chances of closing are summed.", wrap)
    ws.write(9, 0, "In the record, %s homes were open on 1 June of the summer before their youngest own child's "
                   "kindergarten year and %s of them closed by 31 August (%d per cent); in other months a home's chance "
                   "of closing was well under 1 per cent a month." % (n(x["ksummers"]), n(x["kcloses"]), round(100 * x["pk"])), wrap)
    ws.write(11, 0, "Licensing record by year", wb.add_format({"bold": True}))
    ws.write(12, 0, "Year", hf)
    ws.write(12, 1, "Licensed on 1 January", hf)
    ws.write(12, 2, "Closed during the year", hf)
    for i, (yr, op, cl) in enumerate(x["history"], 13):
        ws.write_number(i, 0, yr)
        ws.write_number(i, 1, op, nf)
        ws.write_number(i, 2, cl, nf)
    foot = 13 + len(x["history"]) + 1
    ws.write(foot, 0, "Kindergarten year as in the CCAP provider payment policy, section 6 (a child turning five on or before "
                      "1 September starts that September). Homes are small and large family child care homes (Title 170, "
                      "6.40.010). Sources: licensing extract of 8 January 2027; capacity worksheets 2016 to 2026.", sub)
    ws.set_column(0, 0, 96)
    ws.set_column(1, 2, 14)
    ws.set_row(8, 60)
    ws.set_row(9, 32)
    ws.set_row(12, 30)

    def regional(name, head, cols, rows_fn, note):
        s = wb.add_worksheet(name)
        s.write(0, 0, head, title)
        s.write(1, 0, note, sub)
        s.write(3, 0, "Region", hf)
        for j, c in enumerate(cols, 1):
            s.write(3, j, c, hf)
        tot = [0] * len(cols)
        for i, r in enumerate(sorted(C.REGIONS), 4):
            s.write(i, 0, C.REGIONS[r])
            for j, v in enumerate(rows_fn(r), 1):
                s.write_number(i, j, v, nf)
                tot[j - 1] += v
        i = 4 + len(C.REGIONS)
        s.write(i, 0, "Allerton", bold)
        for j, v in enumerate(tot, 1):
            s.write_number(i, j, v, bold_n)
        s.set_column(0, 0, 22)
        s.set_column(1, len(cols), 16)
        s.freeze_panes(4, 1)

    cd = wb.add_worksheet("Subsidy child-days")
    cd.write(0, 0, "Child-days of subsidised care in family child care homes, Allerton, 2026", title)
    cd.write(1, 0, "CCAP payment lines, SFCC and LFCC providers, lines not voided; each child counted once on a day "
                   "(Monday to Friday) whatever the number of homes paid for that day.", sub)
    cd.write(3, 0, "Half of 2026", hf)
    cd.write(3, 1, "Child-days", hf)
    cd.write(4, 0, "January to June")
    cd.write_number(4, 1, x["a"][1], nf)
    cd.write(5, 0, "July to December")
    cd.write_number(5, 1, x["a"][2], nf)
    cd.write(6, 0, "2026", bold)
    cd.write_number(6, 1, x["a"][1] + x["a"][2], bold_n)
    cd.set_column(0, 0, 22)
    cd.set_column(1, 1, 16)
    money = wb.add_format({"num_format": "#,##0"})
    regional("Subsidy payments", "Money the subsidy paid to family child care homes, 2026 payment runs (USD)",
             ("January to March", "April to June", "July to September", "October to December"),
             lambda r: tuple(x["b"][(r, q)] for q in (1, 2, 3, 4)),
             "CCAP remittances for SFCC and LFCC homes by the date of the payment run and the region of the home that "
             "gave the care; voided remittances out, their reissues in; each remittance counted once (number, run and "
             "county office), a remittance for homes in several regions shared by its lines' pay.")
    nt = wb.add_worksheet("Notes")
    notes = ("Prepared 14 January 2027 from the January 2027 supply folder (licensing extract of 8 January 2027).",
             "A home is a family child care home licence, small or large. A home closes during 2027 when "
             "its licence ends between 1 January and 31 December 2027.",
             "Kindergarten year: the school year in the calendar year the child turns five on or before 1 September (CCAP "
             "provider payment policy, section 6).",
             "Regions are the department's five regions (county_region_lookup.csv).")
    for i, t in enumerate(notes):
        nt.write(i, 0, t, wrap)
    nt.set_column(0, 0, 110)
    wb.close()
    PP.stamp_ooxml(path, "Misty Hawkins", "Misty Hawkins", "2027-01-14T16:05:00Z", "2027-01-14T21:30:00Z", company=C.DEPT)


def main(target, golden_dir, figures_path, submission_path):
    x = compute(target)
    os.makedirs(golden_dir, exist_ok=True)
    workbook(os.path.join(golden_dir, C.DELIVERABLE), x)
    with open(figures_path, "w") as fh:
        json.dump(figures(x), fh, indent=1)
        fh.write("\n")
    with open(submission_path, "w") as fh:
        fh.write(submission(x))
    return x


if __name__ == "__main__":
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    task = os.path.dirname(here)
    main(os.path.join(task, "target"), os.path.join(task, "golden"), os.path.join(here, "figures.json"),
         os.path.join(task, "submission.md"))
