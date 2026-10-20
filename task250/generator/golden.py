"""The two goldens: the January 2028 setting workbook and the chart of each setting's drift alerts a year against the
field plan's visits.   GD.write(golden_dir, content)"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import params as P
import postprocess

XLSX = "drift_alert_setting_2028.xlsx"
PNG = "alerts_by_setting_2028.png"
BLUE, GREY, INK, INK2, GRID, SURF, AMBER = "#2a78d6", "#b9bcc2", "#0b0b0b", "#52514e", "#d9d8d4", "#fcfcfb", "#c2410c"
THIN = Side(style="thin", color="B7B6B1")


def _sheet(ws, title, sub, head, rows, widths, fmts, start=4):
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = sub
    ws["A2"].font = Font(italic=True, size=9, color="52514E")
    for j, h in enumerate(head, 1):
        c = ws.cell(row=start, column=j, value=h)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="E8E7E3")
        c.alignment = Alignment(wrap_text=True, vertical="bottom")
        c.border = Border(bottom=THIN)
    for i, r in enumerate(rows, start + 1):
        for j, (x, f) in enumerate(zip(r, fmts), 1):
            c = ws.cell(row=i, column=j, value=x)
            if f:
                c.number_format = f
            if isinstance(x, str):
                c.alignment = Alignment(horizontal="left")
    for k, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(k)].width = w
    ws.freeze_panes = ws.cell(row=start + 1, column=2)
    return start + len(rows)


def workbook(path, G):
    wb = Workbook()
    ws = wb.active
    ws.title = "Setting 2028"
    rows = []
    for k in P.SETTINGS:
        rows.append(["%.1f" % k, G["alerts_year_whole"][k], round(G["per_year"][k] * 3) - G["cut"][k], G["cut"][k],
                     round(G["per_year"][k] * 3), "Yes" if G["per_year"][k] <= G["budget"] else "No",
                     "Run in 2028" if k == G["setting"] else ""])
    last = _sheet(ws, "Run the %.1f setting in 2028: %d drift alerts a year against the %d visits the field plan leaves"
                  % (G["setting"], G["alerts_at_setting"], G["budget"]),
                  "QC-02 v4 section 7: the most sensitive setting whose drift alerts in the year fit the plan's visits, "
                  "planned on the 2025 to 2027 record.",
                  ["Setting", "Drift alerts a year in 2028", "Re-run alerts, 2025-27", "Drifts cut short, 2025-27",
                   "Alerts, 2025-27", "Within the %d visits" % G["budget"], ""], rows, [10, 14, 13, 13, 11, 12, 14],
                  [None, "0", "0", "0", "0", None, None])
    for i in range(5, last + 1):
        if ws.cell(row=i, column=7).value:
            for j in range(1, 8):
                ws.cell(row=i, column=j).font = Font(bold=True)
    ws.cell(row=last + 2, column=1, value=(
        "Re-run alerts: the alerts the quality control raises at the %d stations it keeps in 2028 when sections 4, 5 "
        "and 8 are re-run on the 2025 to 2027 anomalies with each estimate drawn from those stations, against the "
        "limits the January configuration sets from the recorded statistic. Drifts cut short: the %d drifts the sensor "
        "history shows repaired at drift-alert visits to kept stations, less those the re-run alerted at the setting "
        "before the repair; each would have kept growing until the setting's limit raised its alert. A year: the "
        "three years' alerts divided by three." % (G["n_keep"], G["repairs_kept"]))).font = Font(size=9, color="52514E")
    ws.print_title_rows = "4:4"

    ws2 = wb.create_sheet("Field visits 2027")
    rows = [[nm, G["ask_a"][nm]["visits"], G["ask_a"][nm]["days_waited"], G["ask_b"][nm]] for _, nm in P.DISTRICTS]
    rows.append(["Network", sum(r[1] for r in rows), sum(r[2] for r in rows), sum(r[3] for r in rows)])
    last = _sheet(ws2, "Field visits in 2027 by district",
                  "Visits by the day the technician was at the station: the old contractor's closed orders by their "
                  "visit date, the new contractor's by the first day its technician read the station's sensor there "
                  "while the order was open.",
                  ["District", "Drift-alert visits", "Days their alerts waited (total)",
                   "Breakdown visits at the stations kept in 2028"], rows, [26, 12, 14, 16], [None, "0", "0", "0"])
    for j in range(1, 5):
        ws2.cell(row=last, column=j).font = Font(bold=True)
    ws2.cell(row=last + 2, column=1, value=(
        "Drift-alert visits: every 2027 visit made for a quality-control drift alert, including alerts answered at "
        "the station's spring campaign visit and visits whose readings went in under the station's previous order. "
        "A spare sensor checked at the workshop (the ice point and 40 degrees, outside the range the station's logger "
        "recorded that day) is not a visit, nor is an order closed with a visit date but no technician at the station. "
        "Days waited: from the alert's day in the quality control's export to the visit. Breakdown visits: the old "
        "contractor's closed breakdown orders and the new contractor's correctives that answered no alert; a corrective "
        "closed with no technician at the station was reset remotely.")).font = Font(size=9, color="52514E")

    ws3 = wb.create_sheet("Notes")
    notes = [
        ("As of", "5 January 2028, for the configuration loaded on 15 January 2028."),
        ("Population", "The %d stations the network runs in 2028 (the register without the %d stations whose "
                       "closure is 31 December 2027)." % (G["n_keep"], G["n_close"])),
        ("Limits", "QC-02 section 6: the setting times the standard deviation (n - 1) of each station's drift "
                   "statistic as the quality control recorded it over 2025 to 2027."),
        ("Why the record undercounts", "Every drift a 3.0 alert found was set right within days of the alert, before "
                                       "a wider limit could raise it; a drift keeps growing until a technician sets the "
                                       "sensor right, so under a wider setting each would have raised that setting's "
                                       "alert later, once."),
        ("Budget", "The field plan 2028 leaves %d visits for drift alerts." % G["budget"]),
    ]
    for i, (k, v) in enumerate(notes, 1):
        ws3.cell(row=i, column=1, value=k).font = Font(bold=True)
        c = ws3.cell(row=i, column=2, value=v)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    ws3.column_dimensions["A"].width = 26
    ws3.column_dimensions["B"].width = 104
    wb.save(path)
    postprocess.scrub(path, P.ORG, "2028-01-05")
    postprocess.finish_office(path, "2028-01-05T08:20:00Z", "2028-01-05T16:45:00Z", P.ORG)


def chart(path, G):
    ks = list(P.SETTINGS)
    fig, ax = plt.subplots(figsize=(8.6, 5.4), dpi=150)
    fig.patch.set_facecolor(SURF)
    ax.set_facecolor(SURF)
    xs = list(range(len(ks)))
    for x, k in zip(xs, ks):
        tot = G["per_year"][k]
        cut = G["cut"][k] / 3.0
        chosen = k == G["setting"]
        base = BLUE if chosen else "#9cc3ee"
        ax.bar(x, tot - cut, width=0.56, color=base, zorder=2)
        ax.bar(x, cut, width=0.56, bottom=tot - cut, color="#1d4f91" if chosen else "#5f8fc9", zorder=2,
               edgecolor=SURF, linewidth=1.0)
        ax.text(x, tot + 1.2, "%d" % G["alerts_year_whole"][k], ha="center", va="bottom", fontsize=10,
                color=INK, fontweight="bold" if chosen else "normal")
    ax.axhline(G["budget"], color=AMBER, lw=1.6, zorder=1)
    ax.text(len(ks) - 0.55, G["budget"] + 1.2, "Field plan: %d drift-alert visits" % G["budget"], ha="right",
            va="bottom", fontsize=9, color=AMBER)
    ax.set_xticks(xs)
    ax.set_xticklabels(["Setting %.1f" % k + ("\n(run in 2028)" if k == G["setting"] else "") for k in ks],
                       fontsize=9.5, color=INK2)
    ax.set_ylabel("Drift alerts a year in 2028", fontsize=9.5, color=INK2)
    ax.set_ylim(0, max(G["per_year"].values()) * 1.15)
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(axis="both", length=0, colors=INK2, labelsize=9)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(facecolor="#9cc3ee", label="Re-run on 2025-27 with the %d stations kept" % G["n_keep"]),
                       Patch(facecolor="#5f8fc9", label="Drifts the 3.0 alerts' visits set right first")],
              loc="upper right", frameon=False, fontsize=8.6)
    fig.suptitle("Setting %.1f keeps 2028's drift alerts within the field plan: %d a year"
                 % (G["setting"], G["alerts_at_setting"]), x=0.02, y=0.98, ha="left", fontsize=11.5,
                 fontweight="bold", color=INK)
    fig.text(0.02, 0.905, "Setting %.1f would raise %d a year once the drifts its wider limit lets run are counted"
             % (G["runner_up"], G["alerts_year_whole"][G["runner_up"]]), fontsize=9, color=INK2)
    fig.text(0.02, 0.01, "Source: %s; quality-control export 2025-27 re-run with the 2028 network; sensor history; "
             "field plan 2028." % P.ORG, fontsize=7.5, color=INK2)
    fig.tight_layout(rect=(0, 0.03, 1, 0.9))
    fig.savefig(path, facecolor=SURF, metadata={"Software": None})
    plt.close(fig)


def write(golden, G):
    os.makedirs(golden, exist_ok=True)
    workbook(os.path.join(golden, XLSX), G)
    chart(os.path.join(golden, PNG), G)
