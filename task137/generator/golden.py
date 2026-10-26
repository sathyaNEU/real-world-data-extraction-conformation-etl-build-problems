"""The two golden deliverables: the hub plan workbook and the weekly demand chart."""
import datetime as dt
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

import figs as FG
import params as P

XLSX = "hub_plan_2027-28.xlsx"
PNG = "gp_demand_2025-26.png"


def band(F, k):
    return "{:,} to {:,}".format(F[k + "_low"], F[k + "_high"])


def write(folder, F, X):
    os.makedirs(folder, exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "Plan 2027-28"
    bold = Font(bold=True)
    ws.append(["Kingsmead community phlebotomy hub: GP-referred activity plan for 2027-28"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Prepared for the Outpatients business office from the walk-in clinic's records, April 2023 to September 2026"])
    ws.append([])
    rows = [
        ("Plan: GP-referred blood-test visits in 2027-28 (nearest 2,500)", F["plan_visits_2027_28"]),
        ("2025-26 GP-referred visits seen", F["gp_seen_2025_26"]),
        ("2025-26 GP-referred patients turned away after the tickets had gone", F["gp_turned_away_2025_26"]),
        ("2025-26 clinic days the tickets ran out (of %d)" % F["clinic_days_2025_26"], F["run_out_days_2025_26"]),
        ("Weeks a run-out week holds GP-referred arrivals down (window chosen by fit)", F["window_weeks"]),
        ("2025-26 visits kept in-house by practices with their own clinics (model, nearest 100)", band(F, "kept_in_house")),
        ("2025-26 underlying GP-referred demand (model, nearest 100)", band(F, "base_2025_26")),
        ("Grown 3.5% a year for two years (nearest 100)", band(F, "plan_unrounded")),
    ]
    for label, v in rows:
        ws.append([label, v])
    ws.cell(row=4, column=1).font = bold
    ws.cell(row=4, column=2).font = bold
    ws.append([])
    ws.append(["Method: each clinic day's GP-referred arrivals (seen plus turned away) modelled on weekday, month, trend, "
               "the day after a bank holiday and the mean run-out share of the previous %d weeks, the window with the "
               "lowest AIC of one to twelve weeks (coefficient about %.2f); 2025-26 taken with that effect removed and "
               "grown at the ICB's assumption. The model ranges run from the %d-week window to the %d-week window next to "
               "it in fit." % (F["window_weeks"], F["coef_about"], F["window_weeks"], F["window_runner_up_weeks"])])
    ws.column_dimensions["A"].width = 74
    ws.column_dimensions["B"].width = 18
    for r in range(4, 4 + len(rows)):
        ws.cell(row=r, column=2).number_format = "#,##0"
        ws.cell(row=r, column=2).alignment = Alignment(horizontal="right")
    ws2 = wb.create_sheet("Hospital clinics 2025-26")
    ws2.append(["Hospital-clinic visits to the walk-in clinic, 2025-26, by requesting specialty and quarter"])
    ws2["A1"].font = Font(bold=True)
    ws2.append(["Specialty", "Q1 Apr-Jun", "Q2 Jul-Sep", "Q3 Oct-Dec", "Q4 Jan-Mar", "2025-26"])
    for c in ws2[2]:
        c.font = bold
    tot = [0, 0, 0, 0]
    for sp, q in F["hospital_visits_2025_26"].items():
        vals = [q["Q1"], q["Q2"], q["Q3"], q["Q4"]]
        tot = [a + b for a, b in zip(tot, vals)]
        ws2.append([sp] + vals + [sum(vals)])
    ws2.append(["All specialties"] + tot + [sum(tot)])
    for c in ws2[ws2.max_row]:
        c.font = bold
    ws2.append([])
    ws2.append(["Specialty from the clinic code on the request form. Forms issued before 16 March 2026 carry the old "
                "PAS's codes, each linked to the new code issued on the same clinic days in the last fortnight of March "
                "2026, before the clinics moved days on 1 April. Financial quarter of the visit date."])
    ws2["A%d" % ws2.max_row].font = Font(italic=True, size=9)
    ws2.column_dimensions["A"].width = 30
    for col in "BCDEF":
        ws2.column_dimensions[col].width = 13
    for row in ws2.iter_rows(min_row=3, max_row=3 + len(F["hospital_visits_2025_26"]), min_col=2, max_col=6):
        for c in row:
            c.number_format = "#,##0"
    ws2.freeze_panes = "B3"
    ws3 = wb.create_sheet("Sickness 2025-26")
    ws3.append(["Phlebotomy team sickness absence, 2025-26 (substantive posts; 7.5-hour clinic days)"])
    ws3["A1"].font = Font(bold=True)
    ws3.append(["Quarter", "Working days lost to sickness", "Sickness absence rate (%)"])
    for c in ws3[2]:
        c.font = bold
    for q, v in F["sickness_by_quarter"].items():
        ws3.append([FG.QN[q], v["days_lost"], v["rate_pct"]])
        ws3.cell(row=ws3.max_row, column=2).number_format = "0"
        ws3.cell(row=ws3.max_row, column=3).number_format = "0.0"
    ws3.append([])
    ws3.append(["Rate as the annual report defines it (section 4): hours lost to sickness over the hours rostered to the "
                "substantive team, vacant posts and bank shifts left out. Lines the e-roster shows unassigned from a "
                "sickness's sixth clinic day until the holder returns count as that holder's sickness; the one vacant "
                "post is the one the report names."])
    ws3["A%d" % ws3.max_row].font = Font(italic=True, size=9)
    ws3.column_dimensions["A"].width = 26
    ws3.column_dimensions["B"].width = 30
    ws3.column_dimensions["C"].width = 26
    ws4 = wb.create_sheet("Notes")
    for line in (["Notes"],
                 ["Records", "Walk-in queue records 3 April 2023 to 30 September 2026 (old kiosk to 17 November 2024, "
                             "new kiosk from 18 November 2024; the parallel-run fortnight counted once)"],
                 ["GP-referred", "The request form the patient chose at the kiosk (GP form)"],
                 ["Turned away", "Reception's log of patients turned away after the day's tickets had gone"],
                 ["Run-out share", "A Monday-to-Friday week's clinic days on the log over its clinic days; the model "
                                   "takes the mean over the %d weeks before each day" % F["window_weeks"]],
                 ["Quarters", "Financial quarters of 2025-26, Q1 April to June; hospital-clinic visits by the visit's date"],
                 ["Growth", "The integrated care board's planning assumption for GP direct access phlebotomy, 3.5% a "
                            "year, applied to 2025-26 for two years; no working-day adjustment"],
                 ["Not in the plan", "Patients sent from hospital clinics, who stay at Outpatients block A; the booked "
                                     "clinic at %s, which carries on as now" % P.SATELLITE]):
        ws4.append(line)
    ws4["A1"].font = Font(bold=True)
    for r in range(2, ws4.max_row + 1):
        ws4.cell(row=r, column=1).font = bold
        ws4.cell(row=r, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ws4.cell(row=r, column=1).alignment = Alignment(vertical="top")
    ws4.column_dimensions["A"].width = 18
    ws4.column_dimensions["B"].width = 96
    import docs as DC
    DC.save_xlsx(wb, os.path.join(folder, XLSX), dt.datetime(2026, 10, 2, 16, 5), P.PEOPLE["outpatients"])
    # chart
    from matplotlib.ticker import FuncFormatter
    wk = X["wk"]
    fig, ax = plt.subplots(figsize=(10, 4.9), dpi=110)
    x = range(len(wk))
    kw = dict(width=0.78, edgecolor="white", linewidth=1.0)
    ax.bar(x, wk.seen, color="#005EB8", label="Seen at the walk-in clinic", **kw)
    ax.bar(x, wk.away, bottom=wk.seen, color="#ED8B00", label="Turned away once the tickets had gone", **kw)
    ax.bar(x, wk.kept, bottom=wk.seen + wk.away, color="#41B6E6",
           label="Kept in-house by practices in the weeks after run-outs", **kw)
    ticks = [i for i, w in enumerate(wk.wk) if w.day <= 7]
    ax.set_xticks(ticks)
    ax.set_xticklabels([wk.wk.iloc[i].strftime("%b %y") for i in ticks], fontsize=8, color="#425563")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: "{:,.0f}".format(v)))
    ax.tick_params(axis="y", labelsize=8, colors="#425563")
    ax.set_ylabel("GP-referred visits a week", fontsize=9, color="#425563")
    ax.set_title("2025-26 GP-referred demand was about %s visits: %s seen, %s turned away, about %s kept in-house"
                 % (band(F, "base_2025_26"), "{:,}".format(F["gp_seen_2025_26"]),
                    "{:,}".format(F["gp_turned_away_2025_26"]), band(F, "kept_in_house")),
                 fontsize=10, loc="left", color="#231F20")
    ax.set_ylim(0, max(wk.seen + wk.away + wk.kept) * 1.2)
    ax.grid(axis="y", color="#E8EDEE", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(fontsize=8, loc="upper left", ncol=3, frameon=False, bbox_to_anchor=(0.0, 1.0))
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#AEB7BD")
    fig.text(0.01, 0.012, "Weeks run Monday to Friday; the first and last bars are part-weeks (1 to 4 April 2025, 30 and "
             "31 March 2026).\nKept in-house: each day's GP-referred arrivals with the run-out effect of the previous %d "
             "weeks removed, less the arrivals recorded." % F["window_weeks"], fontsize=7, color="#425563")
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(os.path.join(folder, PNG), metadata={"Software": None})
    plt.close(fig)
