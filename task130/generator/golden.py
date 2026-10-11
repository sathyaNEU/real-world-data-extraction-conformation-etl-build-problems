"""Golden deliverables, read from target/ only: the call-off workbook and the run-off chart."""
import datetime as dt
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import openpyxl
import xlcalc
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import estimators as E
import postprocess as P

TASK = os.path.dirname(HERE)
SIZES = E.SIZES
LABEL = {1: "1 bed", 2: "2 bed", 3: "3 bed", 4: "4+ bed"}
MONTHS = ["31 Oct 2026", "30 Nov 2026", "31 Dec 2026", "31 Jan 2027", "28 Feb 2027", "31 Mar 2027"]


def figures(target):
    c, pl, rv, mb, lt = E.load(target)
    hh = E.households(mb)
    run = E.golden(target)
    start = E.start_counts(pl, hh)
    units = E.callout(run)
    rates = E.lot3_2728(target)
    cost = E.weekly_cost(units, rates)
    return dict(run=run, start=start, units=units, rates=rates, cost=cost, total=sum(units.values()))


def workbook(fig, path):
    wb = openpyxl.Workbook()
    wb.properties.creator = "Maria Field"
    wb.properties.lastModifiedBy = "Maria Field"
    wb.properties.created = dt.datetime(2026, 10, 5, 14, 5)
    wb.properties.modified = dt.datetime(2026, 10, 6, 9, 40)
    wb.properties.title = "Tenter House replacement units call-off 2027"
    head = Font(bold=True, color="FFFFFF")
    fill = PatternFill("solid", fgColor="2F5D50")
    thin = Side(style="thin", color="9AA9A3")

    ws = wb.active
    ws.title = "Call-off"
    ws["A1"] = "Tenter House: replacement units to call off for 1 April 2027"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Larkmoor Borough Council, Housing Needs Service. Kent and Medway TA DPS, Lot 3 (self-contained, "
                "12-month lease). Prepared by Maria Field for Cllr Irene Roberts, 6 October 2026.")
    ws["A2"].font = Font(italic=True, size=9)
    hdr = ["Bedrooms", "Households in Tenter House 30 Sep 2026", "Households expected there 31 Mar 2027",
           "Units to call off", "Lot 3 weekly rate from 1 Apr 2027 (GBP)", "Weekly cost (GBP)"]
    for j, h in enumerate(hdr, 1):
        c = ws.cell(row=4, column=j, value=h)
        c.font, c.fill = head, fill
        c.alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[4].height = 44
    r = 5
    for s in SIZES:
        ws.cell(row=r, column=1, value=LABEL[s])
        ws.cell(row=r, column=2, value=fig["start"][s])
        ws.cell(row=r, column=3, value=fig["run"][s][-1])
        ws.cell(row=r, column=4, value=fig["units"][s])
        ws.cell(row=r, column=5, value=fig["rates"][s]).number_format = "#,##0.00"
        ws.cell(row=r, column=6, value="=D%d*E%d" % (r, r)).number_format = "#,##0.00"
        r += 1
    ws.cell(row=r, column=1, value="Total").font = Font(bold=True)
    for j, col in ((2, "B"), (3, "C"), (4, "D"), (6, "F")):
        c = ws.cell(row=r, column=j, value="=SUM(%s5:%s8)" % (col, col))
        c.font = Font(bold=True)
        c.border = Border(top=thin)
    ws.cell(row=r, column=6).number_format = "#,##0.00"
    r += 2
    ws.cell(row=r, column=1, value="Weekly cost of the call-off, nearest pound:").font = Font(bold=True)
    ws.cell(row=r, column=6, value=int(round(fig["cost"]))).number_format = "£#,##0"
    ws.cell(row=r, column=6).font = Font(bold=True)
    notes = [
        "Households and units are whole numbers. Each household is counted under the unit it will need on "
        "1 April 2027 under Part 3 of the allocations scheme, from the people on its application on 30 September "
        "2026 (closure procedure, point 5); 4+ means four or more.",
        "Expected households: those the move-on plan's lets (revised 14 September 2026) do not reach by 31 March. "
        "Each month's homes go in the round held on the third Monday of the month before, to every household owed "
        "the main duty, in or out of TA, by duty date within the bedrooms it needs on the round day (scheme 3.4 "
        "and 6.4). Needs are worked out from the household members for each round; the bedroom need on the case "
        "record is only reassessed at a decision, a reported birth, a move or an offer.",
        "October's lets were all offered in the round of 21 September and are counted once. No homes with five or "
        "more bedrooms are planned, so households needing five or more stay on that list.",
        "Rates: DPS price schedule, Lot 3, 2027/28 column (August 2026 CPI uplift of 3.8 per cent).",
    ]
    r += 2
    for t in notes:
        ws.cell(row=r, column=1, value=t).alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
        ws.row_dimensions[r].height = 30
        ws.cell(row=r, column=1).font = Font(size=9)
        r += 1
    for col, w in zip("ABCDEF", (12, 18, 18, 12, 20, 16)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A5"

    ro = wb.create_sheet("Run-off")
    ro["A1"] = "Households expected to be living in Tenter House at each month end"
    ro["A1"].font = Font(bold=True, size=13)
    ro["A2"] = ("By the size of unit each household will need on 1 April 2027. 30 September 2026 is the extract "
                "position; the months follow the revised move-on plan.")
    ro["A2"].font = Font(italic=True, size=9)
    hdr = ["Bedrooms", "30 Sep 2026"] + MONTHS
    for j, h in enumerate(hdr, 1):
        c = ro.cell(row=4, column=j, value=h)
        c.font, c.fill = head, fill
        c.alignment = Alignment(horizontal="center")
    r = 5
    for s in SIZES:
        ro.cell(row=r, column=1, value=LABEL[s])
        ro.cell(row=r, column=2, value=fig["start"][s])
        for j, v in enumerate(fig["run"][s], 3):
            ro.cell(row=r, column=j, value=v)
        r += 1
    ro.cell(row=r, column=1, value="All").font = Font(bold=True)
    for j in range(2, 9):
        col = openpyxl.utils.get_column_letter(j)
        c = ro.cell(row=r, column=j, value="=SUM(%s5:%s8)" % (col, col))
        c.font = Font(bold=True)
        c.border = Border(top=thin)
    for j in range(1, 9):
        ro.column_dimensions[openpyxl.utils.get_column_letter(j)].width = 13
    ro.freeze_panes = "B5"
    xlcalc.freeze(wb)
    wb.save(path)
    P.normalize_zip(path, (2026, 10, 6, 9, 40, 0))


def chart(fig, path):
    cols = {1: "#9CC3B2", 2: "#4E8F76", 3: "#2F5D50", 4: "#C9873B"}
    xl = ["30 Sep"] + ["31 Oct", "30 Nov", "31 Dec", "31 Jan", "28 Feb", "31 Mar"]
    series = {s: [fig["start"][s]] + fig["run"][s] for s in SIZES}
    tot = [sum(series[s][k] for s in SIZES) for k in range(7)]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    f, ax = plt.subplots(figsize=(10, 6.2), dpi=150)
    bottom = [0] * 7
    for s in SIZES:
        ax.bar(range(7), series[s], bottom=bottom, color=cols[s], width=0.62, label=LABEL[s],
               edgecolor="white", linewidth=1.2)
        bottom = [b + v for b, v in zip(bottom, series[s])]
    for k, t in enumerate(tot):
        ax.text(k, t + 2.5, str(t), ha="center", va="bottom", fontsize=10, color="#222222",
                fontweight="bold" if k == 6 else "normal")
    u = fig["units"]
    ax.annotate("Call-off for 1 April: %d units\n%d one-bed, %d two-bed, %d three-bed, %d four-bed"
                % (fig["total"], u[1], u[2], u[3], u[4]),
                xy=(6, tot[6]), xytext=(3.55, tot[6] + 72), fontsize=9.5, color="#222222",
                arrowprops=dict(arrowstyle="->", color="#555555", lw=1))
    ax.set_xticks(range(7))
    ax.set_xticklabels(xl)
    ax.set_xlabel("Month end (2026 to 2027)")
    ax.set_ylabel("Households living in Tenter House")
    ax.set_ylim(0, max(tot) * 1.18)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.grid(axis="y", color="#E3E8E6", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(title="Unit needed on 1 April", frameon=False, loc="upper right")
    ax.set_title("Call off %d replacement units for 1 April 2027: Tenter House runs down from %d households to %d"
                 % (fig["total"], tot[0], tot[6]), fontsize=12, loc="left", pad=12)
    f.text(0.01, 0.01, "Source: housing needs extracts to 30 Sep 2026; move-on plan revised 14 Sep 2026. "
           "Larkmoor Borough Council, TA and procurement.", fontsize=7.5, color="#666666")
    f.tight_layout(rect=(0, 0.03, 1, 1))
    f.savefig(path, metadata={"Software": None})
    plt.close(f)


def main(target=None, outdir=None):
    target = target or os.path.join(TASK, "target")
    outdir = outdir or os.path.join(TASK, "golden")
    os.makedirs(outdir, exist_ok=True)
    fig = figures(target)
    workbook(fig, os.path.join(outdir, "tenter_house_replacement_units.xlsx"))
    chart(fig, os.path.join(outdir, "tenter_house_runoff.png"))
    print("call-off", fig["units"], "total", fig["total"], "weekly cost %.2f" % fig["cost"])
    print("run-off", fig["run"])
    return fig


if __name__ == "__main__":
    main()
