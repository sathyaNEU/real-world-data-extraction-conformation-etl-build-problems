"""The two deliverables, written from generator/figures.json: growth_share_2027.xlsx and income_cost_by_step_2027.svg."""
import datetime as dt
import json
import os
import re
import sys

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import officex as OX

TASK = os.path.dirname(HERE)
STEPS = [20, 30, 40, 50, 60, 70, 80, 90, 100]
BLUE, ORANGE, GREY, INK, INK2 = "#2a78d6", "#eb6834", "#52514e", "#0b0b0b", "#52514e"


def workbook(fig, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "2027 growth share"
    bold = Font(bold=True)
    thin = Side(style="thin", color="A6A6A6")
    ws["A1"] = "The Wrexford Trust: growth share for 2027"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "For the trustees' meeting on 10 December 2026. Valuation of 30 November 2026."
    ws["A4"] = "Largest growth share inside the 10% volatility cap"
    ws["A4"].font = bold
    ws["C4"] = fig["call"] / 100.0
    ws["C4"].number_format = "0%"
    ws["C4"].font = Font(bold=True, size=12)
    ws["A5"] = "2027 grant payments (GBP)"
    ws["C5"] = fig["grant_payments_2027_stated"]
    ws["A6"] = "2027 running costs (GBP)"
    ws["C6"] = fig["running_costs"]
    for c in ("C5", "C6"):
        ws[c].number_format = "#,##0"
    hdr = ["Growth share", "Expected volatility (%)", "Inside the cap", "2027 investment income (GBP)",
           "Capital release needed (GBP)"]
    ws.append([])
    ws.append(hdr)
    r0 = ws.max_row
    for j in range(1, 6):
        c = ws.cell(row=r0, column=j)
        c.font = bold
        c.fill = PatternFill("solid", fgColor="DCE6F1")
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = Border(bottom=thin)
    for s in STEPS:
        v = fig["volatility_lead_lag_1"][str(s)]
        ws.append([s / 100.0, round(v, 2), "Yes" if v <= 10.0 else "No", fig["income_stated"][str(s)],
                   fig["release_stated"][str(s)]])
        r = ws.max_row
        ws.cell(row=r, column=1).number_format = "0%"
        ws.cell(row=r, column=2).number_format = "0.00"
        ws.cell(row=r, column=4).number_format = "#,##0"
        ws.cell(row=r, column=5).number_format = "#,##0"
        if s == fig["call"]:
            for j in range(1, 6):
                ws.cell(row=r, column=j).font = bold
    n = ws.max_row + 2
    notes = [
        "Expected volatility: standard deviation of the portfolio's twelve-month total return (investment policy 4.1 to 4.4), "
        "from the holdings' daily total returns over the two years to 30 November 2026 at each step's policy weights, "
        "with the one-day lead and lag covariances added to the daily covariance, times 252 days.",
        "The Kestwick funds are priced at their 12 noon valuation point (the North American fund at the previous New York "
        "close); the mandate at the London close.",
        "Income: procedure 7.2 and 7.3. Mandate dividends counted once per designation, security and event; Kestwick "
        "distributions per income unit; ex-dividend dates 1 December 2025 to 30 November 2026.",
        "Grant payments: open instalments of grants not withdrawn, project instalments after the first paid on the "
        "payment ledger's 35 to 70 days after the report date, euro at 1.1460.",
        "Capital release = grant payments + running costs - investment income. Pounds to the nearest thousand.",
    ]
    ws.cell(row=n, column=1, value="Notes").font = bold
    for k, t in enumerate(notes, 1):
        ws.cell(row=n + k, column=1, value=t)
    for col, w in zip("ABCDE", [14, 14, 12, 18, 18]):
        ws.column_dimensions[col].width = w
    ws.column_dimensions["A"].width = 30
    ws.freeze_panes = None
    OX.xlsx_from_openpyxl(wb, path, "Harriet Clarke", "Harriet Clarke", dt.datetime(2026, 12, 3, 9, 12),
                          dt.datetime(2026, 12, 4, 16, 48), company="The Wrexford Trust", seed=1204)


def chart(fig, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    matplotlib.rcParams["svg.hashsalt"] = "wrexford-2027"
    matplotlib.rcParams["font.family"] = "DejaVu Sans"
    inc = [fig["income_stated"][str(s)] / 1000.0 for s in STEPS]
    g = fig["grant_payments_2027_stated"] / 1000.0
    gr = (fig["grant_payments_2027_stated"] + fig["running_costs_stated"]) / 1000.0
    fig_, ax = plt.subplots(figsize=(8.6, 4.8))
    fig_.patch.set_facecolor("#fcfcfb")
    ax.set_facecolor("#fcfcfb")
    x = list(range(len(STEPS)))
    ax.bar(x, inc, width=0.62, color=BLUE, label="2027 investment income", zorder=2)
    ax.axhline(g, color=ORANGE, lw=2, zorder=3, label="2027 grant payments (%s)" % format(int(g * 1000), ","))
    ax.axhline(gr, color=GREY, lw=2, ls=(0, (5, 3)), zorder=3,
               label="Grant payments + running costs (%s)" % format(int(gr * 1000), ","))
    ax.set_xticks(x)
    ax.set_xticklabels(["%d%%" % s for s in STEPS], color=INK2)
    ax.set_xlabel("Growth share", color=INK2)
    ax.set_ylabel("GBP thousands", color=INK2)
    lo = min(inc + [g]) * 0.8
    ax.set_ylim(lo, max(inc + [gr]) * 1.06)
    for k, v in enumerate(inc):
        if STEPS[k] in (20, fig["title_step"], 100):
            ax.text(k, v + (max(inc) - lo) * 0.012, format(int(round(v * 1000)), ","), ha="center", va="bottom",
                    fontsize=8, color=INK)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#c9c8c4")
    ax.tick_params(colors=INK2, labelsize=9)
    ax.yaxis.grid(True, color="#e6e5e1", lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.legend(loc="upper right", frameon=False, fontsize=8.5, labelcolor=INK)
    ax.set_title("2027 income covers the grant payments up to %d%% growth" % fig["title_step"], loc="left",
                 fontsize=12, color=INK, pad=12)
    fig_.text(0.01, 0.01, "Investment income by procedure 7.2 at each growth share, valuation of 30 November 2026. "
                          "The Wrexford Trust, December 2026.", fontsize=7.5, color=INK2)
    fig_.tight_layout(rect=(0, 0.04, 1, 1))
    fig_.savefig(path, format="svg", metadata={"Creator": None, "Date": None, "Format": None, "Type": None})
    plt.close(fig_)
    s = open(path, encoding="utf-8").read()
    s = re.sub(r"<metadata>.*?</metadata>\s*", "", s, flags=re.S)
    s = re.sub(r"<!-- Created with [^>]*-->\s*", "", s)
    open(path, "w", encoding="utf-8").write(s)


def build(out=None):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    out = out or os.path.join(TASK, "golden")
    os.makedirs(out, exist_ok=True)
    workbook(fig, os.path.join(out, "growth_share_2027.xlsx"))
    chart(fig, os.path.join(out, "income_cost_by_step_2027.svg"))


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else None)
