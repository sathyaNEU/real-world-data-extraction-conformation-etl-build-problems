"""task172 goldens: the quote workbook, the expiring-permits chart, generator/figures.json and submission.md, every figure
computed once from the shipped files (calc.py) and carried."""
from __future__ import annotations

import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as K           # noqa: E402
import common as C         # noqa: E402
import ladder as L         # noqa: E402
import postprocess as PP   # noqa: E402

MONTHS = {7: "July", 8: "August", 9: "September"}
QLABEL = {"2025 Q4": "October to December 2025", "2026 Q1": "January to March 2026", "2026 Q2": "April to June 2026",
          "2026 Q3": "July to September 2026"}


def figures(target):
    import numpy as np
    Q, A, B = K.solve(target)
    rens = Q["rens"]
    old = [(r["appt"] - r["received"]).days for r in rens if r["route"] == "appointment" and r["appt"] and
           r["received"] < dt.date(2026, 1, 1)]
    R = L.routes(Q)
    F = dict(
        quote_months=C.half_month(Q["months"]),
        quote_unrounded=round(Q["months"], 3),
        lead_weeks_now=int(round(Q["lead_weeks"])),
        lead_weeks_before=int(round(float(np.median(old)) / 7)),
        reach_expiry="about nine in ten",
        reach_appt_share=round(Q["reach_appt"], 3),
        reach_share=round(Q["reach"], 3),
        quarter_c9_share=round(Q["mix"]["(c)(9)"], 3),
        appt_share_c9=round(Q["pA_cat"]["(c)(9)"], 3),
        appt_share_c26=round(Q["pA_cat"]["(c)(26)"], 3),
        expedite_accepted=round(Q["accept"], 3),
        expedite_response_weeks=int(round(Q["e_days"] / 7)),
        expedite_response="about a week",
        rival_record_months=C.half_month(R["record KM, all receipts"]),
        rival_default_months=C.half_month(R["default: post-rule record, appointment waits plus the new delay"]),
        refile_days=C.REFILE_DAYS,
        month_days=C.MONTH_DAYS,
        standard_sections=["2.3", "3.1", "4.2", "4.3"],
        ask_a={"%d-%02d %s" % (y, m, cat): A[(y, m, cat)] for (y, m) in C.ASK_A_MONTHS for cat in C.CATS},
        ask_b={k: dict(rejected=v[0], refiled_30=v[1]) for k, v in B.items()},
    )
    return F, Q, A, B


def write_workbook(path, F):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.worksheet.properties import PageSetupProperties
    wb = Workbook()
    ws = wb.active
    ws.title = "Quote"
    head = Font(bold=True, size=14, color="1F3A5F")
    sub = Font(size=9, color="5A6470")
    bold = Font(bold=True)
    fill = PatternFill("solid", fgColor="E3EDF7")
    thin = Side(style="thin", color="9BB7D4")
    wrap = Alignment(wrap_text=True, vertical="top")
    ws["A1"] = "Quote %.1f months for the renewals filed January to March 2027" % F["quote_months"]
    ws["A1"].font = head
    ws["A2"] = ("Global Mobility analytics. Case-system export of 4 December 2026, for the benefits portal release of "
                "15 December 2026.")
    ws["A2"].font = sub
    ws["A4"] = "Portal text"
    ws["A4"].font = bold
    ws["A5"] = ("Four in five work-permit renewals filed from January to March 2027 should have USCIS's decision within "
                "%.1f months of USCIS receiving them." % F["quote_months"])
    ws["A5"].alignment = wrap
    ws.merge_cells("A5:C5")
    ws.row_dimensions[5].height = 30
    ws["A7"] = "Wait to quote"
    ws["B7"] = "%.1f months" % F["quote_months"]
    for c in ("A7", "B7"):
        ws[c].font = Font(bold=True, size=12)
        ws[c].fill = fill
    ws["A9"] = "What sets it"
    ws["A9"].font = bold
    for j, h in enumerate(("", "Value", "From")):
        c = ws.cell(row=10, column=j + 1, value=h or None)
        c.font, c.border = bold, Border(bottom=thin)
    rows = [("Fingerprint appointments set for renewals received October and November 2026 (median)",
             "%d weeks after receipt" % F["lead_weeks_now"], "counsel's appointment notices"),
            ("Fingerprint appointments for renewals received in 2024 and 2025 (median)",
             "%d weeks after receipt" % F["lead_weeks_before"], "counsel's appointment notices"),
            ("Renewals filed in the quarter that need a new fingerprint appointment, still pending on the day the "
             "filer's card expires", F["reach_expiry"], "the forecast below"),
            ("Team's expedite request when the card expires, to USCIS's decision (renewals filed since 30 October 2025)",
             F["expedite_response"], "case-action log, decision notices")]
    for i, (a, b, c) in enumerate(rows):
        ws.cell(row=11 + i, column=1, value=a).alignment = wrap
        ws.cell(row=11 + i, column=2, value=b).alignment = Alignment(vertical="top")
        ws.cell(row=11 + i, column=3, value=c).alignment = wrap
    ws["A16"] = "How the wait was forecast"
    ws["A16"].font = bold
    notes = ["A renewal waits for its fingerprint appointment, or not where USCIS reuses fingerprints it already holds, "
             "and then for the officer's review. The review was estimated on every renewal counsel filed since January "
             "2024, renewals still open at the export counted as still waiting. USCIS reused fingerprints for most "
             "(c)(9) renewals and sent most (c)(26) renewals to an appointment; about half the quarter's renewals are "
             "(c)(9), the 18-month cards issued from December 2025 coming due.",
             "Renewals filed since 30 October 2025 no longer extend the card (GM-07 3.1). A renewal still pending when "
             "the filer's card expires gets the team's expedite request around that day; USCIS has accepted most of "
             "them and decided the renewal a median of about a week after the request, in busy months as in quiet "
             "ones. While appointments came four to five weeks out, few renewals got that far; with appointments now "
             "set about %d weeks out, about nine in ten of the quarter's renewals that need one will." %
             F["lead_weeks_now"],
             "The quarter's renewals were simulated with the appointments now being set, each decided at the earlier of "
             "its normal decision and the team's request plus the expedite response, and the 80th percentile of the "
             "wait taken in months of 30.4 days, to the nearest half month (GM-07 4.3)."]
    for i, n in enumerate(notes):
        c = ws.cell(row=17 + i, column=1, value=n)
        c.alignment = wrap
        ws.merge_cells(start_row=17 + i, start_column=1, end_row=17 + i, end_column=3)
        ws.row_dimensions[17 + i].height = (74, 88, 58)[i]
    ws["A21"] = ("Waits run from the receipt date on USCIS's receipt notice (GM-07 2.3) to the date of the decision "
                 "notice, approval or denial; renewals withdrawn before a decision are left out (GM-07 4.2).")
    ws["A21"].font = sub
    ws["A21"].alignment = wrap
    ws.merge_cells("A21:C21")
    ws.row_dimensions[21].height = 26
    ws.column_dimensions["A"].width = 70
    ws.column_dimensions["B"].width = 22
    ws.column_dimensions["C"].width = 26
    ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
    ws.print_area = "A1:C21"

    ws2 = wb.create_sheet("Expiring permits")
    ws2["A1"] = "Expiring work permits peak in September 2027"
    ws2["A1"].font = head
    ws2["A2"] = "Work permits held by current employees and the spouses of current employees, by the card's last day"
    ws2["A2"].font = sub
    hdr = ("Month", "(c)(9)", "(c)(26)", "Total")
    for j, h in enumerate(hdr):
        c = ws2.cell(row=4, column=j + 1, value=h)
        c.font, c.fill, c.border = bold, fill, Border(bottom=thin)
        if j:
            c.alignment = Alignment(horizontal="right")
    tot = [0, 0]
    for i, (y, m) in enumerate(C.ASK_A_MONTHS):
        a, b = F["ask_a"]["%d-%02d (c)(9)" % (y, m)], F["ask_a"]["%d-%02d (c)(26)" % (y, m)]
        tot[0] += a
        tot[1] += b
        ws2.cell(row=5 + i, column=1, value="%s %d" % (MONTHS[m], y))
        for j, v in enumerate((a, b, a + b)):
            ws2.cell(row=5 + i, column=2 + j, value=v).number_format = "#,##0"
    ws2.cell(row=8, column=1, value="July to September 2027").font = bold
    for j, v in enumerate((tot[0], tot[1], tot[0] + tot[1])):
        c = ws2.cell(row=8, column=2 + j, value=v)
        c.number_format, c.font, c.border = "#,##0", bold, Border(top=thin)
    ws2["A10"] = ("Each current person's work permit (GM-07 1.3 and 1.4): the card USCIS approved most recently, from HR's "
                  "roster, counsel's approval notices, the case register and the green-card tracker, in the category "
                  "of the approval. A spouse is counted once, whether Global Mobility's records or Benefits' ID "
                  "carries her card, and belongs to the household the register, the tracker, the roster's onboarding "
                  "entry or Benefits names.")
    ws2["A10"].font = sub
    ws2["A10"].alignment = wrap
    ws2.merge_cells("A10:D10")
    ws2.row_dimensions[10].height = 54
    ws2.column_dimensions["A"].width = 26
    for col in "BCD":
        ws2.column_dimensions[col].width = 12
    ws2.freeze_panes = "A5"
    ws2.print_title_rows = "4:4"

    ws3 = wb.create_sheet("Lockbox rejections")
    ws3["A1"] = "Most rejected renewal packets were filed again within %d days" % F["refile_days"]
    ws3["A1"].font = head
    ws3["A2"] = "Renewal packets the lockbox rejected, by the notice date on the rejection"
    ws3["A2"].font = sub
    hdr = ("Quarter", "Rejected", "Filed again within %d days" % F["refile_days"])
    for j, h in enumerate(hdr):
        c = ws3.cell(row=4, column=j + 1, value=h)
        c.font, c.fill, c.border = bold, fill, Border(bottom=thin)
        if j:
            c.alignment = Alignment(horizontal="right")
    tr = [0, 0]
    for i, (lab, _, _) in enumerate(C.ASK_B_QUARTERS):
        r, f = F["ask_b"][lab]["rejected"], F["ask_b"][lab]["refiled_30"]
        tr[0] += r
        tr[1] += f
        ws3.cell(row=5 + i, column=1, value=QLABEL[lab])
        ws3.cell(row=5 + i, column=2, value=r).number_format = "#,##0"
        ws3.cell(row=5 + i, column=3, value=f).number_format = "#,##0"
    ws3.cell(row=9, column=1, value="October 2025 to September 2026").font = bold
    for j, v in enumerate(tr):
        c = ws3.cell(row=9, column=2 + j, value=v)
        c.number_format, c.font, c.border = "#,##0", bold, Border(top=thin)
    ws3["A11"] = ("Rejection notices counsel logged and those applicants forwarded to Global Mobility, one per case and "
                  "notice date. Filed again within 30 days means USCIS received the renewal again no later than the "
                  "30th day after the notice's date (GM-07 2.3 and 2.4), whoever filed it.")
    ws3["A11"].font = sub
    ws3["A11"].alignment = wrap
    ws3.merge_cells("A11:C11")
    ws3.row_dimensions[11].height = 40
    ws3.column_dimensions["A"].width = 32
    ws3.column_dimensions["B"].width = 12
    ws3.column_dimensions["C"].width = 26
    ws3.freeze_panes = "A5"
    ws3.print_title_rows = "4:4"
    wb.save(path)
    PP.normalize_ooxml(path, "Melinda Yang", "Melinda Yang", "2026-12-04T23:30:00Z", "2026-12-04T23:58:00Z", excel=True,
                       company=C.ORG)


def write_chart(path, F):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    matplotlib.rcParams["svg.hashsalt"] = "task172"
    matplotlib.rcParams["svg.fonttype"] = "none"
    matplotlib.rcParams["font.family"] = "DejaVu Sans"
    labels = ["%s %d" % (MONTHS[m], y) for (y, m) in C.ASK_A_MONTHS]
    c9 = [F["ask_a"]["%d-%02d (c)(9)" % (y, m)] for (y, m) in C.ASK_A_MONTHS]
    c26 = [F["ask_a"]["%d-%02d (c)(26)" % (y, m)] for (y, m) in C.ASK_A_MONTHS]
    fig, ax = plt.subplots(figsize=(8.0, 4.8), dpi=100)
    x = range(len(labels))
    w = 0.36
    b1 = ax.bar([i - w / 2 for i in x], c9, w, label="(c)(9), pending adjustment", color="#1F5A8A")
    b2 = ax.bar([i + w / 2 for i in x], c26, w, label="(c)(26), H-4 spouses", color="#D9822B")
    for bars in (b1, b2):
        for bar in bars:
            ax.annotate("%d" % bar.get_height(), (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                        xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=10,
                        color="#222222")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Work permits expiring")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: "{:,.0f}".format(v)))
    ax.set_title("Expiring work permits peak in September 2027", fontsize=13, loc="left", pad=22, color="#1F3A5F")
    ax.text(0, 1.02, "Held by current employees and the spouses of current employees, by the card's last day",
            fontsize=9, color="#5A6470", transform=ax.transAxes, va="bottom")
    fig.text(0.01, 0.01, "Global Mobility. HR roster, counsel's approval notices, case register and green-card tracker, "
             "export of 4 December 2026.", fontsize=7.5, color="#5A6470")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(axis="y", color="#E6E9ED", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_ylim(0, max(c9 + c26) * 1.15)
    ax.legend(frameon=False, loc="upper left", fontsize=9)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(path, format="svg", metadata={"Date": None, "Creator": None, "Format": None, "Type": None})
    plt.close(fig)
    with open(path, encoding="utf-8") as fh:
        svg = fh.read()
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg.replace('id="matplotlib.axis_', 'id="axis_'))


def write_submission(path, F):
    A, B = F["ask_a"], F["ask_b"]
    lines = [
        "## Tags", "",
        "**Domain:** General Statistics & Data Science (regression, classification and model diagnostics: a software "
        "company's global mobility team quoting in its benefits portal the wait within which four in five of its January "
        "to March 2027 work-permit renewals will have USCIS's decision, each renewal's wait cut at its own card's expiry "
        "by the team's expedite request, the model chosen on the renewals filed since automatic extension ended that "
        "were still pending at their card's expiry).",
        "**Analytical objective:** Forecasting & Predictive Modeling.", "",
        "## 1. Final Recommendation", "",
        "**The benefits portal should quote %.1f months for the work-permit renewals filed from January to March 2027.** "
        "USCIS is setting fingerprint appointments %d weeks after receipt, so about nine in ten of the quarter's "
        "renewals that need an appointment will still be pending on the day the filer's card expires, and since "
        "renewals stopped extending the card, those still pending at their card's expiry have mostly been decided about "
        "a week after the expedite request the team files when the card expires. Not %.1f months, the new appointment "
        "delay laid on the record's appointment-route waits, which ignores that those waits now end at the card's "
        "expiry. Not %.1f months, the 80th percentile of the record's own waits with open renewals censored, which "
        "reflects appointments %d to 5 weeks out." % (
            F["quote_months"], F["lead_weeks_now"], F["rival_default_months"], F["rival_record_months"],
            F["lead_weeks_before"]), "",
        "## 2. Critical Components", "",
        "1. Fingerprint appointments for renewals received in October and November 2026: a median of **%d weeks** after "
        "receipt, against **%d weeks** for renewals received in 2024 and 2025." % (F["lead_weeks_now"],
                                                                                  F["lead_weeks_before"]),
        "2. Renewals filed in the quarter that need a new fingerprint appointment and are still pending on the day the "
        "filer's card expires: **about nine in ten**.",
        "3. From the team's expedite request when a card expires to USCIS's decision, renewals filed since 30 October "
        "2025: a median of **about a week**.", "",
        "## 3. Step-by-Step Solution", "",
        "1. Joined renewal_case_notices_2024-01_2026-12.csv to renewal_case_register.xlsx (client_ref through case_id or "
        "legacy_case_id) and kept, for each renewal counsel filed, the receipt date (standard 2.3), the latest biometrics "
        "appointment notice, the decision notice and the expiry of the card it renews, withdrawn renewals left out "
        "(standard 4.2).",
        "2. Read the latest appointment notices: a median of %d weeks after receipt for renewals received in October and "
        "November 2026, %d weeks through 2024 and 2025, rising to about 5 by the summer of 2026." % (
            F["lead_weeks_now"], F["lead_weeks_before"]),
        "3. Estimated the review, from the appointment (or the receipt where USCIS reused fingerprints) to the decision, "
        "by Kaplan-Meier, censored at the export, at a stop of work or at an expedite request in "
        "case_actions_2024-2026.csv.",
        "4. For renewals filed since 30 October 2025 (standard 3.1), the case log shows the team's expedite request when "
        "each renewal still pending in its care reached its card's expiry (mostly the expiry date, some days before or "
        "after it); USCIS accepted most of the requests and decided those renewals a median of about a week later, in "
        "the busiest request months as in the quiet ones and after the appointment queue tripled, where the stage "
        "model fitted on the earlier renewals puts their typical remaining wait at more than two weeks.",
        "5. Read the quarter's mix from the work permits whose renewals reach USCIS in it: about half are (c)(9), whose "
        "renewals mostly reuse fingerprints (fewer than three in ten went to an appointment, against seven in ten of "
        "the (c)(26) renewals).",
        "6. Simulated the quarter's renewals with that mix, the new appointment lead, the review, the card-expiry gaps "
        "of the renewals filed since 30 October 2025, the request timing and the expedite response: about nine in ten "
        "of those sent to an appointment reach their card's expiry undecided.",
        "7. Took the 80th percentile of the simulated waits in months of %.1f days, to the nearest half month (standard "
        "4.3): %.1f months." % (F["month_days"], F["quote_months"]), "",
        "## 4. Deliverable Answers", "",
        "### q1_2027_renewal_quote.xlsx", "",
        "1. Wait to quote for the renewals filed from January to March 2027: %.1f months." % F["quote_months"],
        "2. Work permits held by current employees and the spouses of current employees expiring, by month and category:",
    ]
    for (y, m) in C.ASK_A_MONTHS:
        lines.append("   - %s %d: (c)(9) %d, (c)(26) %d" % (MONTHS[m], y, A["%d-%02d (c)(9)" % (y, m)],
                                                         A["%d-%02d (c)(26)" % (y, m)]))
    lines.append("3. Renewal packets the lockbox rejected, by the notice date on the rejection, and those filed again "
                 "within %d days of that date:" % F["refile_days"])
    for lab, _, _ in C.ASK_B_QUARTERS:
        lines.append("   - %s: %d rejected, %d filed again within %d days" % (
            QLABEL[lab], B[lab]["rejected"], B[lab]["refiled_30"], F["refile_days"]))
    lines += ["", "### q1_2027_expiring_permits.svg", "",
              "1. Grouped bar chart of the work permits expiring in July, August and September 2027, a (c)(9) and a "
              "(c)(26) bar for each month, each labelled with its count (%s)." % ", ".join(
                  "%d and %d" % (A["%d-%02d (c)(9)" % (y, m)], A["%d-%02d (c)(26)" % (y, m)])
                  for (y, m) in C.ASK_A_MONTHS)]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def main(target, golden, figures_path, submission):
    F, Q, A, B = figures(target)
    os.makedirs(golden, exist_ok=True)
    write_workbook(os.path.join(golden, "q1_2027_renewal_quote.xlsx"), F)
    write_chart(os.path.join(golden, "q1_2027_expiring_permits.svg"), F)
    with open(figures_path, "w", encoding="utf-8") as fh:
        json.dump(F, fh, indent=1, sort_keys=True)
        fh.write("\n")
    write_submission(submission, F)
    return F


if __name__ == "__main__":
    root = os.path.dirname(HERE)
    print(main(os.path.join(root, "target"), os.path.join(root, "golden"), os.path.join(HERE, "figures.json"),
               os.path.join(root, "submission.md")))
