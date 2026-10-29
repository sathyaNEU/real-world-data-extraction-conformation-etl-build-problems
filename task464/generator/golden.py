"""task464 architecture 10: the golden deliverables, written from figures.json.

  losses_programme_2027.xlsx    the eight projects with each one's 2025/26 saving and its value, the pick and the
                                runner-up, and the basis the paper states
  losses_saving_2027.png        the eight savings, one bar each, labelled, the pick highlighted
  iis_feeders_2025-26.csv       each feeder's 2025/26 CI per 100 customers and CML per customer, with its customers
"""
import csv
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
import world as W

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOLD = os.path.join(BASE, "golden")
THIN = Side(style="thin", color="BFBFBF")


def _km(F, name, w):
    return F["projects"][name].get("km")


def workbook(F):
    P = F["projects"]
    order = F["order"]
    call, runner = F["call"], F["runner_up"]
    wb = Workbook()
    ws = wb.active
    ws.title = "Programme"
    ws["A1"] = "Losses programme 2027/28: fund the %s reconductoring" % call
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Copsewell Cross 11 kV feeders. Losses each project's replacement conductor would have removed in 2025/26, "
                "for the investment review panel of 9 December 2026. Network losses strategy (%s), 30 November 2026."
                % W.PEOPLE["losses_lead"])
    ws["A2"].font = Font(italic=True, size=9, color="52514E")
    ws.append([])
    hdr = ["", "Feeder", "Breaker", "Sections replaced", "Route replaced (km)", "Existing conductor", "Replacement",
           "Saving 2025/26 (MWh)", "Value at GBP %.2f/MWh (GBP)" % W.LOSSES_VALUE_GBP_MWH]
    ws.append(hdr)
    for c in ws[4]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="E9EEF5")
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = Border(bottom=THIN)
    for i, k in enumerate(order, 1):
        p = P[k]
        mark = "Fund" if k == call else ("Runner-up" if k == runner else None)
        ws.append([mark, k, p["breaker"], ", ".join(p["sections"]), p["km"], p["old"], p["new_desc"], p["year_mwh"], p["value_gbp"]])
        if k == call:
            for cell in ws[ws.max_row]:
                cell.font = Font(bold=True)
    last = 4 + len(order)
    for row in ws.iter_rows(min_row=5, max_row=last):
        row[4].number_format = "0.00"
        row[7].number_format = "0.0"
        row[8].number_format = "#,##0"
        row[3].alignment = Alignment(wrap_text=True, vertical="top")
        row[5].alignment = Alignment(wrap_text=True, vertical="top")
        row[6].alignment = Alignment(wrap_text=True, vertical="top")
    ws.cell(row=last + 2, column=1, value="%s saves %.1f MWh a year against %.1f for %s, %.1f MWh more." % (
        call, P[call]["year_mwh"], P[runner]["year_mwh"], runner, F["gap_mwh"])).font = Font(size=10, bold=True)
    ws.cell(row=last + 3, column=1, value=("%s's replaced overhead line carries the Hob Moor Solar Park's export back toward the "
                                           "Kestle Park estate near the primary, so most of its saving falls in the summer "
                                           "half-year." % call) if call == "Kestle" else "").font = Font(size=9, color="52514E")
    ws.cell(row=last + 4, column=1, value="Savings to one decimal place of a MWh, ranked on the unrounded figures; values to "
                                          "the nearest GBP 100. Basis on the next sheet.").font = Font(size=9, color="52514E")
    for col, wd in zip("ABCDEFGHI", (10, 15, 8, 30, 10, 26, 22, 12, 14)):
        ws.column_dimensions[col].width = wd
    ws.row_dimensions[4].height = 44
    ws.freeze_panes = "A5"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True

    ns = wb.create_sheet("Basis")
    notes = [
        ("Year", "The 17,520 half-hours from 00:00 on 1 April 2025 to 24:00 on 31 March 2026, UK time."),
        ("Saving", "For each half-hour and each replaced section, the I2R loss at the current the section carried, on the "
                   "existing conductor less on the replacement, summed over the project's sections and the year."),
        ("Section current", "Each section's half-hourly current is the net of every connection beyond it on the feeder's "
                            "normal running arrangement: each secondary substation's monitored load and each HV customer's "
                            "settlement import less its export, balanced across three phases at 11 kV nominal."),
        ("Resistance", "EDS 02-0310 issue 7, resistance at 20 C; nothing added for the network's own losses or voltage drop."),
        ("Value", "Saving for the year at the 2027/28 losses value of GBP %.2f per MWh." % W.LOSSES_VALUE_GBP_MWH),
        ("Source", "2025/26 secondary substation monitoring, HV settlement data and the network model, extracted 12 June 2026."),
    ]
    for a, b in notes:
        ns.append([a, b])
    for row in ns.iter_rows():
        row[0].font = Font(bold=True)
        row[1].alignment = Alignment(wrap_text=True, vertical="top")
        row[0].alignment = Alignment(vertical="top")
    ns.column_dimensions["A"].width = 17
    ns.column_dimensions["B"].width = 100
    path = os.path.join(GOLD, "losses_programme_2027.xlsx")
    wb.save(path)
    return path


def chart(F):
    P = F["projects"]
    order = F["order"]
    call, runner = F["call"], F["runner_up"]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "svg.hashsalt": "task464",
                         "path.simplify": False})
    fig, ax = plt.subplots(figsize=(8.6, 4.6), dpi=150)
    names = list(reversed(order))
    vals = [P[k]["year_mwh"] for k in names]
    cols = ["#2A78D6" if k == call else ("#8FB3E3" if k == runner else "#B8B6B0") for k in names]
    bars = ax.barh(names, vals, color=cols, height=0.62)
    for b, v, k in zip(bars, vals, names):
        lab = "%.1f MWh" % v + ("  fund" if k == call else ("  runner-up" if k == runner else ""))
        ax.text(b.get_width() + max(vals) * 0.012, b.get_y() + b.get_height() / 2, lab, va="center", fontsize=8.8,
                fontweight="bold" if k == call else "normal")
    ax.set_xlim(0, max(vals) * 1.28)
    ax.set_xlabel("Losses removed in 2025/26, MWh")
    ax.set_title("Kestle's replacement conductor would have removed the most losses in 2025/26"
                 if call == "Kestle" else "%s's replacement conductor would have removed the most losses" % call,
                 fontsize=10.5, loc="left", fontweight="bold")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.text(0.01, 0.01, "Copsewell Cross 11 kV reconductoring projects; saving at each replaced section's own half-hourly "
                         "current, 1 April 2025 to 31 March 2026.", fontsize=7.4, color="#52514E")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    path = os.path.join(GOLD, "losses_saving_2027.png")
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)
    return path


def iis_csv(F):
    path = os.path.join(GOLD, "iis_feeders_2025-26.csv")
    with open(path, "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["feeder", "breaker", "ci_per_100_customers", "cml_per_customer"])
        for k in [f["name"] for f in W.FEEDERS]:
            v = F["iis"][k]
            wr.writerow([k, F["projects"][k]["breaker"], "%.1f" % v["ci"], "%.1f" % v["cml"]])
    return path


def main(F):
    os.makedirs(GOLD, exist_ok=True)
    return [workbook(F), chart(F), iis_csv(F)]
