"""task166's goldens, computed from the shipped pack (calc.py): the decision workbook he_payoff_pilot_2027.xlsx, the chart
payoff_quotes_by_center.png, generator/figures.json and submission.md, every figure emitted from one computation."""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C            # noqa: E402
import common as K          # noqa: E402
import postprocess as PP    # noqa: E402

F_BOOK = "he_payoff_pilot_2027.xlsx"
F_CHART = "payoff_quotes_by_center.png"
QLABEL = {"2025Q4": "October to December 2025", "2026Q1": "January to March 2026", "2026Q2": "April to June 2026",
          "2026Q3": "July to September 2026"}
QSHORT = {"2025Q4": "Oct to Dec 2025", "2026Q1": "Jan to Mar 2026", "2026Q2": "Apr to Jun 2026",
          "2026Q3": "Jul to Sep 2026"}
SHORT = {"Grand Rapids": "Grand Rapids", "The Lakeshore": "the Lakeshore",
         "Kalamazoo and Battle Creek": "Kalamazoo and Battle Creek", "Muskegon and the North": "Muskegon and the North"}


def r10(x):
    return int(10 * round(x / 10.0))


def compute(target):
    gold, ctx = C.golden(target)
    H, FW, curt = ctx["H"], ctx["FW"], ctx["curt"]
    he = C.he_posted_monthly(target)
    ph = C.plan_he(target)
    H2 = C.add_own(H, he)
    FW2 = C.add_own(FW, he, ph)
    dev = {"blend": float(ctx["model"].deviance)}
    rival = {}
    for name, cov in (("own", ["own"]), ("first", ["first"]), ("walt", ["walt"]), ("own_first", ["own", "first"])):
        f = C.fit(H2, cov)
        dev[name] = float(f.deviance)
        rival[name] = C.project(FW2, f.predict(C.design(FW2, cov)), curt)
    tr = H[(H.t >= C.mo(2025, 12)) & (H.y == 1)]
    rival["trailing"] = (tr.groupby("region").H.sum() / 1e6).reindex(C.REG_ORDER)
    bk = ctx["book"].merge(ctx["los"][["region"]], left_on="key", right_index=True)
    leg, core, los = ctx["leg"], ctx["core"], ctx["los"]
    paid = C.paid_by_asof(core)
    ask = C.ask_table(C.statement_loans(target, los, core), paid)
    # payoffs and curtailments apart, for the workbook's detail
    h = ctx["model"].predict(C.design(FW, ["blend"]))
    pay_only = C.project(FW, h, 0.0)
    return dict(gold=gold, ctx=ctx, dev=dev, rival=rival, bk=bk, ask=ask, pay_only=pay_only, curt=curt)


def figures(R):
    g = R["gold"]
    order = g.sort_values(ascending=False)
    pick, second = order.index[0], order.index[1]
    bk = R["bk"]
    H = R["ctx"]["H"]
    own = R["rival"]["own"]
    f = {
        "call": {"center": pick, "principal_2027_musd": r10(g[pick]), "principal_2027_musd_unrounded": round(float(g[pick]), 2),
                 "second": second, "second_principal_musd_unrounded": round(float(g[second]), 2),
                 "margin": round(float(g[pick] / g[second]), 2)},
        "components": {"book_loans": int(len(bk)), "book_musd": round(float(bk.bal.sum()) / 1e6, 1),
                       "book_musd_pick": round(float(bk[bk.region == pick].bal.sum()) / 1e6, 1),
                       "payoffs_2019_2026": int(H.y.sum())},
        "steps": {"curtailment_pct_month": round(100 * R["curt"], 3),
                  "deviance": {k: round(v, 1) for k, v in R["dev"].items()},
                  "forecast_musd": {r: round(float(g[r]), 1) for r in C.REG_ORDER},
                  "own_rate_pick": own.idxmax(), "own_rate_pick_musd": round(float(own.max()), 1),
                  "own_rate_pick_musd_rounded": r10(float(own.max())),
                  "first_alone_pick": R["rival"]["first"].idxmax(),
                  "trailing_pick": R["rival"]["trailing"].idxmax()},
        "asks": {},
        "conventions": {"posted_rate_term_years": 30, "senior_lien_terms_months": [360, 180], "knots": C.KNOTS,
                        "marker_months": 24, "policy_section": "7.4", "as_of_year": 2026, "forecast_year": 2027,
                        "rounding_musd": 10},
    }
    for (rg, q), (a, b) in R["ask"].items():
        f["asks"]["%s|%s" % (rg, q)] = {"quoted": a, "paid_in_full": b}
    return f


# ------------------------------------------------------------------------------------------------- the workbook
def write_book(path, R, F):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = Workbook()
    ink = "1D232A"
    head_fill = PatternFill("solid", fgColor="E3E9EE")
    pick_fill = PatternFill("solid", fgColor="FFF4D6")
    bold = Font(name="Calibri", size=11, bold=True, color=ink)
    body = Font(name="Calibri", size=11, color=ink)
    grey = Font(name="Calibri", size=9, color="5A626B")
    title = Font(name="Calibri", size=14, bold=True, color="24515E")
    thin = Side(style="thin", color="B9C1C8")
    g = R["gold"]
    c = F["call"]
    # sheet 1: the recommendation and the regional forecast
    ws = wb.active
    ws.title = "Pilot region"
    ws["A1"] = "Muskegon and the North opens the payoff-retention pilot on 4 January 2027"
    ws["A1"].font = title
    ws["A2"] = ("Prepared by %s, Lending Analytics, for the Management Lending Committee meeting of 9 December 2026. "
                "Loans on the books at the close of 30 November 2026; Lending Policy 7.4." % K.PEOPLE["analytics"])
    ws["A2"].font = grey
    ws["A4"] = "Recommendation"
    ws["A4"].font = bold
    ws["A5"] = ("Open the pilot at the %s lending center: its members will pay off about $%d million of fixed-rate home "
                "equity principal in 2027, the most of the four centers. %s comes second."
                % (c["center"], c["principal_2027_musd"], SHORT[c["second"]][0].upper() + SHORT[c["second"]][1:]))
    ws["A5"].font = body
    ws["A5"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A5:F5")
    ws.row_dimensions[5].height = 32
    ws["A7"] = "2027 principal paid ahead of schedule, base case"
    ws["A7"].font = bold
    hdr = ["Regional lending center", "Loans on the books 30 Nov 2026", "Principal 30 Nov 2026 ($ millions)",
           "Paid in full 2027 ($ millions)", "Curtailments 2027 ($ millions)", "Total 2027 ($ millions)"]
    ws.append(hdr)
    for cell in ws[8]:
        cell.font = bold
        cell.fill = head_fill
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        cell.border = Border(bottom=thin)
    ws.row_dimensions[8].height = 44
    bk = R["bk"]
    pay = R["pay_only"]
    for rg in sorted(C.REG_ORDER, key=lambda r: -g[r]):
        b = bk[bk.region == rg]
        ws.append([rg, int(len(b)), round(float(b.bal.sum()) / 1e6, 1), round(float(pay[rg]), 1),
                   round(float(g[rg] - pay[rg]), 1), round(float(g[rg]), 1)])
    last = ws.max_row
    ws.append(["All centers", int(len(bk)), round(float(bk.bal.sum()) / 1e6, 1), round(float(pay.sum()), 1),
               round(float((g - pay).sum()), 1), round(float(g.sum()), 1)])
    for cell in ws[ws.max_row]:
        cell.font = bold
        cell.border = Border(top=thin)
    for row in ws.iter_rows(min_row=9, max_row=ws.max_row):
        row[1].number_format = "#,##0"
        for cell in row[2:]:
            cell.number_format = "0.0"
    for cell in ws[9]:
        cell.fill = pick_fill
    ws["A%d" % (ws.max_row + 2)] = ("Totals are summed before rounding. The pilot figure is given to the nearest $10 "
                                    "million as the committee asked.")
    ws["A%d" % ws.max_row].font = grey
    for col, w in zip("ABCDEF", (30, 16, 17, 16, 16, 15)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A9"
    # sheet 2: the payoff quotes
    ws = wb.create_sheet("Payoff quotes")
    ws["A1"] = "Fixed-rate home equity loans quoted a payoff, by center and quarter"
    ws["A1"].font = title
    ws["A2"] = ("A loan counts once in a quarter however many statements it had. Paid in full: closed as paid in full by "
                "the member on or before 30 November 2026.")
    ws["A2"].font = grey
    ws.append([])
    ws.append(["Regional lending center", "Quarter", "Loans quoted", "Of which paid in full by 30 Nov 2026"])
    for cell in ws[4]:
        cell.font = bold
        cell.fill = head_fill
        cell.border = Border(bottom=thin)
    for rg in C.REG_ORDER:
        for q, _, _ in C.QUARTERS:
            a, b = R["ask"][(rg, q)]
            ws.append([rg, QLABEL[q], a, b])
    for col, w in zip("ABCD", (30, 26, 14, 22)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A5"
    ws.print_title_rows = "4:4"
    ws.print_area = "A1:D%d" % ws.max_row
    ws.page_setup.orientation = "portrait"
    ws.page_setup.fitToWidth = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    # sheet 3: notes
    ws = wb.create_sheet("Notes")
    notes = [
        "Definitions",
        "Population, outcome, window, region and rates as Lending Policy 7.4.3 files them: the fixed-rate closed-end home "
        "equity loans on the books at the close of 30 November 2026; principal paid ahead of schedule (payoffs before "
        "maturity at the balance retired, and curtailments); payments posted in calendar 2027; the region of the "
        "collateral county; the planning cycle's base case.",
        "",
        "Forecast",
        "Each loan's monthly payoff probability is read off the debt on the house: the blended rate of the first mortgage "
        "and the home equity loan at their balances, less the posted 30-year fixed rate a month earlier. The first "
        "mortgage's rate comes from the senior lien the lending system took from the credit report (the amortization "
        "identity on its original amount, term and reported balance; a second funded with the purchase carries it as "
        "filed). Fitted by logistic regression on every loan-month from January 2019 to November 2026, with seasonality "
        "and a marker for a first mortgage opened in the last two years; curtailments at the trial balance's monthly rate "
        "of %.3f per cent of the balance." % F["steps"]["curtailment_pct_month"],
        "",
        "Payoff quotes",
        "Statements issued or updated in the payoff statement system, by the Eastern date of issue, the March 2026 "
        "statements prepared by hand during the system upgrade, and the home equity loan a statement on one of our first "
        "mortgages paid off as well. Home equity lines and voided requests are not counted.",
        "",
        "Sources",
        "core_he_trial_balance_2024-09_2026-11.csv, legacy_he_loans_2019-01_2024-08.csv, core_conversion_xref.csv, "
        "he_lending_file_2009-2026.csv, county_region_map.csv, posted_rate_sheets_2018-12_2026-11.csv, "
        "planning_cycle_2027_rates.xlsx, payoff_statement_log_2025-10_2026-11.csv, payoff_statements_manual_2026-03.xlsx, "
        "first_mortgage_servicing_2026-11.csv; pulled 3 December 2026.",
    ]
    for line in notes:
        ws.append([line])
        cell = ws.cell(row=ws.max_row, column=1)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        if line in ("Definitions", "Forecast", "Payoff quotes", "Sources"):
            cell.font = bold
        else:
            cell.font = body
    ws.column_dimensions["A"].width = 120
    wb.save(path)


# ------------------------------------------------------------------------------------------------- the chart
SERIES = {"Grand Rapids": "#2a78d6", "The Lakeshore": "#eb6834", "Kalamazoo and Battle Creek": "#1baf7a",
          "Muskegon and the North": "#eda100"}


def write_chart(path, R):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "svg.hashsalt": "task166"})
    qs = [q for q, _, _ in C.QUARTERS]
    fig, ax = plt.subplots(figsize=(9.2, 5.6), dpi=150)
    fig.patch.set_facecolor("#fcfcfb")
    ax.set_facecolor("#fcfcfb")
    bottoms = np.zeros(len(qs))
    x = np.arange(len(qs))
    for rg in C.REG_ORDER:
        vals = np.array([R["ask"][(rg, q)][0] for q in qs], float)
        ax.bar(x, vals, 0.58, bottom=bottoms, color=SERIES[rg], edgecolor="#fcfcfb", linewidth=2, label=rg, zorder=3)
        for xi, (v, b0) in enumerate(zip(vals, bottoms)):
            dark = rg in ("Grand Rapids",)
            ax.text(xi, b0 + v / 2, "%d" % v, ha="center", va="center", fontsize=9.5,
                    color="#ffffff" if dark else "#0b0b0b", zorder=4)
        bottoms += vals
    for xi, tot in enumerate(bottoms):
        ax.text(xi, tot + 4, "%d" % tot, ha="center", va="bottom", fontsize=9, color="#52514e")
    ax.set_xticks(x)
    ax.set_xticklabels([QSHORT[q] for q in qs])
    ax.set_ylabel("Fixed-rate home equity loans quoted a payoff")
    ax.set_ylim(0, max(bottoms) * 1.12)
    ax.grid(axis="y", color="#e4e3df", linewidth=0.8, zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#b5b3ad")
    ax.tick_params(colors="#52514e")
    top = max(C.REG_ORDER, key=lambda r: sum(R["ask"][(r, q)][0] for q in qs))
    ax.set_title("%s drew the most payoff quotes in every quarter" % top, loc="left", fontsize=12.5,
                 color="#0b0b0b", pad=28)
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 1.075), ncol=4, frameon=False, fontsize=9)
    fig.text(0.01, 0.012, "A loan counts once a quarter however many statements it had. Source: payoff statement "
             "system and the payoff desk's log, %s." % K.CU, fontsize=7.5, color="#52514e")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path, facecolor=fig.get_facecolor(), metadata={"Software": None})
    plt.close(fig)


# ------------------------------------------------------------------------------------------------- the write-up
def write_submission(path, R, F):
    g = R["gold"]
    c = F["call"]
    s = F["steps"]
    comp = F["components"]
    fc = s["forecast_musd"]
    d = s["deviance"]
    sec = SHORT[c["second"]]
    lines = [
        "## Tags", "",
        "**Domain:** Banking, credit and financial risk, deposit and liquidity behaviour (home equity prepayment).  ",
        "**Analytical objective:** Forecasting and predictive modeling.", "",
        "## 1. Final Recommendation", "",
        "**Open the payoff-retention pilot at the Muskegon and the North lending center: its members will pay off about "
        "$%d million of fixed-rate home equity principal in 2027, the most of the four centers, and %s comes second.**"
        % (c["principal_2027_musd"], sec),
        "The forecast reads each loan's payoff off the whole debt on the house, the first mortgage and the home equity "
        "loan at their balances: Muskegon and the North's 2024 to 2026 home equity loans are large and sit behind small "
        "seasoned first mortgages, so those stacks come into the money as the planning cycle's 30-year rate falls, and the "
        "region pays off %.1f against %.1f for %s. Not Grand Rapids, which a prepayment curve on each loan's own note rate "
        "puts first at about $%d million (%.1f), when its home equity loans sit behind large first mortgages that keep the "
        "debt on the house below the market. Not %s, which leads when payoffs are read off the first mortgage's own rate "
        "alone because its purchase seconds sit behind high-rate first mortgages; those seconds are small. Not Kalamazoo "
        "and Battle Creek, whose trailing payoffs were its 2023 purchase loans, now mostly paid off."
        % (fc["Muskegon and the North"], fc[c["second"]], sec, s["own_rate_pick_musd_rounded"], s["own_rate_pick_musd"],
           sec),
        "",
        "## 2. Critical Components", "",
        "1. Fixed-rate home equity loans on the books at the close of 30 November 2026: **%s** loans, **$%.1f million**"
        % ("{:,}".format(comp["book_loans"]), comp["book_musd"]),
        "2. Muskegon and the North's principal on the books at 30 November 2026: **$%.1f million**" % comp["book_musd_pick"],
        "3. Payoffs in full in the record the forecast is fitted on, January 2019 to November 2026: **%s**"
        % "{:,}".format(comp["payoffs_2019_2026"]),
        "",
        "## 3. Step-by-Step Solution", "",
        "1. Took the loans on the books from core_he_trial_balance_2024-09_2026-11.csv, the 2026-11-30 rows with LoanStatus "
        "ACTIVE: %s loans, $%.1f million, per Lending Policy 7.4.3." % ("{:,}".format(comp["book_loans"]), comp["book_musd"]),
        "2. Built one loan-month history from January 2019 to November 2026 from legacy_he_loans_2019-01_2024-08.csv to "
        "August 2024 (each month's balance on the loan's schedule from BAL_12_31_2018 or its funding) and the trial "
        "balance after it (the prior month-end balance, the first core month from BAL_AT_CONV), linked through "
        "core_conversion_xref.csv, with the region from he_lending_file_2009-2026.csv's property_county and "
        "county_region_map.csv: %s payoffs in full (PIF); maturities and charge-offs leave the record without "
        "counting." % "{:,}".format(comp["payoffs_2019_2026"]),
        "3. Recovered each first mortgage from the lending file's senior lien: its rate from the amortization identity on "
        "senior_lien_original_amount, senior_lien_term_months and senior_lien_balance after the payments from "
        "senior_lien_opened to senior_lien_balance_as_of (a blank term is the one of 360 and 180 months whose payment the "
        "reported payment carries; a second funded with the purchase carries senior_lien_note_rate_pct as filed), and its "
        "balance in every month on its schedule.",
        "4. Took the posted 30 YR FIXED MORTGAGE rate's monthly average from posted_rate_sheets_2018-12_2026-11.csv, each "
        "sheet in effect until the next, and the base case's 30-year fixed rate from planning_cycle_2027_rates.xlsx for "
        "December 2026 to December 2027.",
        "5. Fitted each loan-month's payoff probability by logistic regression on the stack's refinancing incentive, the "
        "blended rate of the first mortgage and the home equity loan at their balances less the posted 30-year rate a "
        "month earlier (piecewise linear, knots at -1, 0, 0.5, 1, 1.5 and 2 points), with a sine and cosine of the month "
        "and a marker for a first mortgage opened less than 24 months before: deviance %s, against %s on the first "
        "mortgage's own rate, %s with each lien against its own posted rate, %s with the loan's own and the first's "
        "rates side by side and %s on the loan's own note rate against the posted home equity rate."
        % ("{:,.1f}".format(d["blend"]), "{:,.1f}".format(d["first"]), "{:,.1f}".format(d["walt"]),
           "{:,.1f}".format(d["own_first"]), "{:,.1f}".format(d["own"])),
        "6. Took curtailments at the trial balance's rate, PrincipalPaid above ScheduledPrincipal in ACTIVE months over the "
        "prior month-end balance: %.3f per cent of the balance a month." % s["curtailment_pct_month"],
        "7. Ran the book from December 2026 through December 2027 on the base case, a payoff at the start-of-month balance "
        "and curtailments on the balance that survives the month, and summed 2027 by region: Muskegon and the North %.1f "
        "million (about %d to the nearest 10), the Lakeshore %.1f, Grand Rapids %.1f, Kalamazoo and Battle Creek %.1f; "
        "the pilot opens at Muskegon and the North and the Lakeshore comes second."
        % (fc["Muskegon and the North"], c["principal_2027_musd"], fc["The Lakeshore"], fc["Grand Rapids"],
           fc["Kalamazoo and Battle Creek"]),
        "8. Counted each center's loans quoted a payoff per quarter from payoff_statement_log_2025-10_2026-11.csv, ISSUED "
        "and UPDATED statements by their Eastern issue date, a legacy number through the cross-reference, home equity "
        "lines and VOID requests out; added the home equity loan behind each MTG statement whose amount paid it as well "
        "as the credit union's first mortgage (the mortgage in first_mortgage_servicing_2026-11.csv, the loan at the same "
        "property_street and property_zip in the lending file) and the home equity loans in "
        "payoff_statements_manual_2026-03.xlsx matched by property address; paid in full is LoanStatus PIF with a "
        "CloseDate on or before 2026-11-30.",
        "",
        "## 4. Deliverable Answers", "",
        "### he_payoff_pilot_2027.xlsx", "",
        "1. Center to open the payoff-retention pilot on 4 January 2027: **%s**" % c["center"],
        "2. Fixed-rate home equity principal its members will pay off in 2027: **$%d million** (nearest 10)"
        % c["principal_2027_musd"],
        "3. Center second: **%s**" % (sec[0].upper() + sec[1:]),
        "4. Fixed-rate home equity loans quoted a payoff, and of those paid in full by 30 November 2026, by center and "
        "quarter:",
    ]
    for rg in C.REG_ORDER:
        for q, _, _ in C.QUARTERS:
            a = F["asks"]["%s|%s" % (rg, q)]
            lines.append("   - %s, %s: **%d** quoted, **%d** paid in full" % (rg, QLABEL[q], a["quoted"], a["paid_in_full"]))
    lines += ["", "### payoff_quotes_by_center.png", "",
              "1. One bar per quarter, October to December 2025 through July to September 2026, split by center, each "
              "segment labelled with its count of loans quoted as in answer 4 above.", ""]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def main(target, golden_dir, fig_path):
    os.makedirs(golden_dir, exist_ok=True)
    R = compute(target)
    F = figures(R)
    with open(fig_path, "w", encoding="utf-8") as fh:
        json.dump(F, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    write_book(os.path.join(golden_dir, F_BOOK), R, F)
    PP.normalize_ooxml(os.path.join(golden_dir, F_BOOK), K.PEOPLE["analytics"], K.PEOPLE["analytics"],
                       "2026-12-04T14:12:00Z", "2026-12-08T21:37:00Z", excel=True, company=K.CU)
    write_chart(os.path.join(golden_dir, F_CHART), R)
    task_dir = os.path.dirname(golden_dir.rstrip("/"))
    sub = os.path.join(task_dir, "submission.md") if os.path.basename(golden_dir.rstrip("/")) == "golden" else \
        os.path.join(golden_dir, "submission.md")
    write_submission(sub, R, F)
    return R, F


if __name__ == "__main__":
    T = os.path.dirname(HERE)
    main(os.path.join(T, "target"), os.path.join(T, "golden"), os.path.join(HERE, "figures.json"))
