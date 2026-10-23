"""task178 deliverables: figures.json, the golden workbook and chart, and submission.md, all computed by calc.py from the
shipped pack under target/."""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np

import calc
import common as C

PCT = "%"


def r1(x):
    return float("%.1f" % x)


def compute(target):
    call = calc.call(target)
    a, n_orders = calc.ask_a(target)
    sell, buy, _, n_draw = calc.ask_b(target)
    lam = call["impacts"]
    fam_lam = [lam["iv_hourly"], lam["iv_sign"], lam["iv_daily"], lam["ratio"]] + list(lam["iv_by_year"].values())
    fig = {
        "call": {
            "pricing_volatility_pct": call["setting"],
            "expected_volatility_band_pct": [call["setting"] - 1, call["setting"]],
            "settings": {str(s): ("covers" if s >= call["setting"] else "falls short") for s in C.GRID},
        },
        "components": {
            "price_impact_band_pct_per_usd_100mn": [math.floor(min(fam_lam) * 1000) / 10, math.ceil(max(fam_lam) * 1000) / 10],
            "golden_impact_pct_per_usd_100mn": round(lam["iv_hourly"] * 100, 2),
            "hourly_observations": call["n_hours"],
            "grid_settings_pct": list(C.GRID),
            "impact_per_usd_mn": 100,
            "sessions_per_year": C.ANN,
        },
        "rivals": {
            "record_vol_pct": r1(call["record_vol"]), "record_setting": math.ceil(call["record_vol"]),
            "net_flow_impact_vol_pct": r1(call["vol_ols_net"]), "net_flow_setting": math.ceil(call["vol_ols_net"]),
            "customer_flow_impact_vol_pct": r1(call["vol_reduced_form"]),
            "customer_flow_setting": math.ceil(call["vol_reduced_form"]),
        },
        "ask_a_hedging_cost_tqp_per_usd": {"Q%d" % q: {b[0]: r1(a[(q, b[0])]) for b in C.SIZE_BANDS} for q in range(1, 5)},
        "ask_b_forwards_due_2027_usd_mn": {"Q%d" % q: {"exporters_sell": r1(sell[q]), "importers_buy": r1(buy[q])}
                                           for q in range(1, 5)},
        "working": {"golden_vol_pct": round(call["golden"], 2), "orders_2026": n_orders, "drawdowns_netted": n_draw},
    }
    return fig, call, a, sell, buy


# ------------------------------------------------------------------------------------------------ the workbook
def write_book(path, fig, call):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    import postprocess as PP
    wb = openpyxl.Workbook()
    navy = "0F4C5C"
    head = Font(name="Calibri", bold=True, color="FFFFFF", size=10)
    fill = PatternFill("solid", fgColor=navy)
    pick = PatternFill("solid", fgColor="DCEBEF")
    thin = Side(style="thin", color="B8C4CC")
    box = Border(left=thin, right=thin, top=thin, bottom=thin)
    norm = Font(name="Calibri", size=10)
    bold = Font(name="Calibri", size=10, bold=True)
    note = Font(name="Calibri", size=9, italic=True, color="555B61")
    s = fig["call"]["pricing_volatility_pct"]
    lo, hi = fig["call"]["expected_volatility_band_pct"]
    ilo, ihi = fig["components"]["price_impact_band_pct_per_usd_100mn"]

    def table(ws, top, cols, rows, fmt=None):
        for j, c in enumerate(cols):
            cell = ws.cell(row=top, column=1 + j, value=c)
            cell.font, cell.fill, cell.border = head, fill, box
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        for i, r in enumerate(rows):
            for j, v in enumerate(r):
                cell = ws.cell(row=top + 1 + i, column=1 + j, value=v)
                cell.font, cell.border = norm, box
                if isinstance(v, (int, float)):
                    cell.alignment = Alignment(horizontal="right")
                    if fmt and j in fmt:
                        cell.number_format = fmt[j]
        return top + 1 + len(rows)

    ws = wb.active
    ws.title = "Pricing vol 2027"
    ws["A1"] = "Price 2027 one-year USD/TQP options at %d%%" % s
    ws["A1"].font = Font(name="Calibri", size=13, bold=True, color=navy)
    ws["A2"] = ("FX Options, Banco Cordillera. Set 30 Dec 2026 under the pricing policy v2.1, section 2. "
                "Prepared by Y. Cáceres.")
    ws["A2"].font = note
    rows = [["Pricing volatility, 2027 one-year options", "%d%%" % s],
            ["Expected 2027 volatility: closing rate, 2024-26 sessions, BCT spot operations taken off",
             "%d%% to %d%%" % (lo, hi)],
            ["Market price impact, %% of rate per USD 100 mn net flow (customer flow as instrument)", "%.1f to %.1f" % (ilo, ihi)],
            ["Recorded closing-rate volatility, 2024-26 (with BCT operations)", "%.1f%%" % fig["rivals"]["record_vol_pct"]]]
    for i, (k, v) in enumerate(rows):
        a, b = ws.cell(row=4 + i, column=1, value=k), ws.cell(row=4 + i, column=2, value=v)
        a.font = b.font = bold if i == 0 else norm
        b.alignment = Alignment(horizontal="right")
    grid = [[g, fig["call"]["settings"][str(g)]] for g in C.GRID]
    end = table(ws, 9, ["Grid setting (%)", "Against expected 2027 volatility"], grid)
    for i, g in enumerate(C.GRID):
        if g == s:
            for j in (1, 2):
                ws.cell(row=10 + i, column=j).font = bold
                ws.cell(row=10 + i, column=j).fill = pick
    ws.cell(row=end + 1, column=1, value="Routes checked and not used").font = Font(name="Calibri", size=10, bold=True)
    chk = [["Recorded volatility, no adjustment", fig["rivals"]["record_vol_pct"], fig["rivals"]["record_setting"]],
           ["BCT trades back at OLS impact on market net flow", fig["rivals"]["net_flow_impact_vol_pct"],
            fig["rivals"]["net_flow_setting"]],
           ["BCT trades back at OLS impact on customer flow", fig["rivals"]["customer_flow_impact_vol_pct"],
            fig["rivals"]["customer_flow_setting"]]]
    end2 = table(ws, end + 2, ["Route", "Volatility (%)", "Setting (%)"], chk, fmt={1: "0.0", 2: "0"})
    ws.cell(row=end2 + 1, column=1, value=("OLS impacts are biased low: BCT sold in the hours the peso fell hardest, so its "
                                           "trades move with the hour's own news. Instrument estimates (hourly, daily, by "
                                           "year) all fall in %d%% to %d%%." % (lo, hi))).font = note
    ws.freeze_panes = "A4"
    ws.column_dimensions["A"].width = 78
    ws.column_dimensions["B"].width = 30
    ws.column_dimensions["C"].width = 12

    ws2 = wb.create_sheet("Hedging cost 2026")
    ws2["A1"] = "Platform hedging cost 2026, TQP per USD against the arrival mid, dollar-weighted by order"
    ws2["A1"].font = Font(name="Calibri", size=11, bold=True, color=navy)
    bands = [b[0] for b in C.SIZE_BANDS]
    labels = {"under 1m": "Under USD 1 mn", "1m to 3m": "USD 1 to 3 mn", "3m to 10m": "USD 3 to 10 mn",
              "10m and over": "USD 10 mn and over"}
    rows = [["Q%d 2026" % q] + [fig["ask_a_hedging_cost_tqp_per_usd"]["Q%d" % q][b] for b in bands] for q in range(1, 5)]
    table(ws2, 3, ["Quarter"] + [labels[b] for b in bands], rows, fmt={1: "0.0", 2: "0.0", 3: "0.0", 4: "0.0"})
    ws2["A9"] = ("Source: platform confirmations 2026, CANCELLED executions removed. An order is one arrival (trader, side "
                 "and time stamp); its executions are summed into its size band.")
    ws2["A9"].font = note
    ws2.freeze_panes = "B4"
    for k, w in {"A": 12, "B": 16, "C": 16, "D": 16, "E": 19}.items():
        ws2.column_dimensions[k].width = w

    ws3 = wb.create_sheet("Forwards due 2027")
    ws3["A1"] = "Client USD forwards falling due in 2027, USD mn"
    ws3["A1"].font = Font(name="Calibri", size=11, bold=True, color=navy)
    rows = [["Q%d 2027" % q, fig["ask_b_forwards_due_2027_usd_mn"]["Q%d" % q]["exporters_sell"],
             fig["ask_b_forwards_due_2027_usd_mn"]["Q%d" % q]["importers_buy"]] for q in range(1, 5)]
    table(ws3, 3, ["Quarter", "Exporters sell USD", "Importers buy USD"], rows, fmt={1: "#,##0.0", 2: "#,##0.0"})
    ws3["A9"] = ("Window forwards at their undrawn balance; drawdowns counted at their own maturity. Cancelled deals, "
                 "EUR/TQP deals and Treasury desk deals excluded.")
    ws3["A9"].font = note
    ws3.freeze_panes = "B4"
    for k, w in {"A": 12, "B": 20, "C": 20}.items():
        ws3.column_dimensions[k].width = w

    ws4 = wb.create_sheet("Notes")
    notes = [["Item", "Basis"],
             ["As of", "30 Dec 2026; BCT hourly release of 30 Dec 2026 (sessions 2 Jan 2024 to 29 Dec 2026)"],
             ["Volatility", "Root mean square of daily log changes in the 16:00 closing rate, x 252 sessions, square root; "
                            "rounded up to the whole per cent (policy v2.1, s.2)"],
             ["Customer flow", "Dealers' reports of record (last report received per dealer and hour); Financiera Tres Valles "
                               "not of record after 30 Jun 2025"],
             ["BCT operations", "VIGENTE deals, VENTA less COMPRA, by local hour of deal"],
             ["Missing hour marks", "Hour joined to the next hour (3 marks missing in the release)"],
             ["Hedging cost", "Platform confirmations 2026; signed price less arrival mid, weighted by USD amount"],
             ["Forwards due", "Deal system export of 30 Dec 2026; client segments from the corporate client register"]]
    table(ws4, 1, notes[0], notes[1:])
    ws4.column_dimensions["A"].width = 20
    ws4.column_dimensions["B"].width = 110
    wb.save(path)
    PP.normalize_ooxml(path, "Yanet Cáceres", "Yanet Cáceres", "2026-12-29T21:14:02Z", "2026-12-30T19:47:31Z", excel=True,
                       company=C.DESK_BANK)


# ------------------------------------------------------------------------------------------------ the chart
def write_chart(path, fig, call):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    lo, hi = fig["call"]["expected_volatility_band_pct"]
    s = fig["call"]["pricing_volatility_pct"]
    rec = fig["rivals"]["record_vol_pct"]
    f, ax = plt.subplots(figsize=(7.4, 4.1), dpi=110)
    xs = list(C.GRID)
    cols = ["#0f4c5c" if g == s else ("#9fb8c0" if g > s else "#d4dade") for g in xs]
    ax.bar(xs, xs, color=cols, width=0.62, zorder=2)
    ax.axhspan(lo, hi, color="#e07a1f", alpha=0.20, zorder=1, lw=0)
    ax.text(7.52, hi + 0.15, "expected 2027 volatility, %d%% to %d%%" % (lo, hi), color="#a8520c", fontsize=8.5)
    ax.axhline(rec, color="#555b61", lw=1.0, ls="--", zorder=3)
    ax.text(7.52, rec + 0.15, "recorded 2024-26, with BCT operations: %.1f%%" % rec, color="#555b61", fontsize=8.5)
    for g in xs:
        ax.text(g, g + 0.12 if g < lo else g + 0.12, "covers" if g >= s else "short", ha="center", fontsize=7.5,
                color="#0f4c5c" if g >= s else "#7b858d")
    ax.set_xticks(xs)
    ax.set_xticklabels(["%d%%" % g for g in xs])
    ax.set_ylim(0, 14.6)
    ax.set_ylabel("volatility, % a year")
    ax.set_xlabel("pricing grid setting")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.set_title("%d%% is the lowest setting that covers the peso's free-float volatility" % s, fontsize=10, loc="left")
    f.text(0.01, 0.01, "Source: BCT hourly release 30 Dec 2026; Banco Cordillera FX Options. One-year USD/TQP options.",
           fontsize=7, color="#7b858d")
    f.tight_layout(rect=(0, 0.03, 1, 1))
    f.savefig(path, metadata={"Software": None})
    plt.close(f)


# ------------------------------------------------------------------------------------------------ the write-up
def submission(fig, call):
    s = fig["call"]["pricing_volatility_pct"]
    lo, hi = fig["call"]["expected_volatility_band_pct"]
    rv = fig["rivals"]
    ilo, ihi = fig["components"]["price_impact_band_pct_per_usd_100mn"]
    A = fig["ask_a_hedging_cost_tqp_per_usd"]
    B = fig["ask_b_forwards_due_2027_usd_mn"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Quantitative Finance (volatility and derivatives pricing).  ")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Price the 2027 one-year dollar options at %d per cent.** The closing rate's volatility over the 2024 to "
             "2026 sessions without the Banco Central's spot operations is between %d and %d per cent, so %d is the lowest "
             "whole-per-cent setting that covers it and %d falls short. Not the recorded %.1f per cent (a setting of %d), "
             "which the Bank's operations held down. Not %d or %d, which put the Bank's trades back at an impact read "
             "from the hour's move on the market's net flow (%.1f per cent) or on customer flow alone (%.1f per cent): "
             "the Bank traded against each hour's own move, so both regressions read the market's depth too low.\n"
             % (s, lo, hi, s, s - 1, rv["record_vol_pct"], rv["record_setting"], rv["net_flow_setting"],
                rv["customer_flow_setting"], rv["net_flow_impact_vol_pct"], rv["customer_flow_impact_vol_pct"]))
    L.append("## 2. Critical Components\n")
    L.append("1. The market's price impact of net dollar flow, with customer flow as the instrument, is **between %.1f and "
             "%.1f per cent** of the rate per 100 million dollars." % (ilo, ihi))
    L.append("2. The 2024 to 2026 closing-rate volatility without the Bank's operations is **between %d and %d per cent**."
             % (lo, hi))
    L.append("3. The settings of 8 to %d per cent fall short of it; %d and 13 per cent cover it.\n" % (s - 1, s))
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Summed the reports of record in %s (the last report received for each dealer and hour, Financiera "
             "Tres Valles' reports after 30 June 2025 left out per %s) into the customers' net dollar purchases each hour."
             % (C.F_FLOWS, C.F_DEALERS))
    L.append("2. Dropped the ANULADA rows of %s and netted VENTA less COMPRA into the Bank's net dollar sales each hour."
             % C.F_OPS)
    L.append("3. Took each hour's log change of the mid in %s, joining an hour to the next where its closing mark is "
             "missing." % C.F_MID)
    L.append("4. Regressed the hour's change on the market's net flow (customers less the Bank) with customer flow as the "
             "instrument, because the Bank traded against each hour's own move: between %.1f and %.1f per cent per 100 "
             "million dollars." % (ilo, ihi))
    L.append("5. Added each session's Bank net sales times that impact to the closing rate's daily log change and took the "
             "root mean square at 252 sessions (%s, section 2): between %d and %d per cent, rounded up to %d."
             % (C.F_POLICY, lo, hi, s))
    L.append("6. Hedging cost: grouped the CONFIRMED executions in %s into orders by trader, side and millisecond time "
             "stamp (an order that takes several resting quotes shows one execution per quote), banded each order by its "
             "total size, and dollar-weighted each execution's price less the arrival mid, signed by side, by 2026 "
             "quarter." % C.F_CONF)
    L.append("7. Forwards due: in %s, dropped ANULADA, EUR/TQP and Treasury-desk deals, netted each WINDOW deal by the "
             "outrights booked against it (same client, side and forward rate, maturing inside the window), and summed "
             "the 2027 maturities by quarter and segment from %s." % (C.F_FWD, C.F_CLIENTS))
    L.append("8. Priced the 2027 one-year options at %d per cent, the lowest setting at or above the expected volatility.\n"
             % s)
    L.append("## 4. Deliverable Answers\n")
    L.append("### %s\n" % C.G_BOOK)
    L.append("1. Pricing volatility for 2027 one-year options: %d per cent." % s)
    L.append("2. Grid settings against the expected 2027 volatility:")
    for g in C.GRID:
        L.append("   - %d per cent: %s" % (g, fig["call"]["settings"][str(g)]))
    L.append("3. 2026 hedging cost per dollar against the arrival mid, dollar-weighted, in pesos:")
    for q in range(1, 5):
        cells = A["Q%d" % q]
        L.append("   - Q%d 2026: under 1 million %.1f; 1 to 3 million %.1f; 3 to 10 million %.1f; 10 million and over %.1f"
                 % (q, cells["under 1m"], cells["1m to 3m"], cells["3m to 10m"], cells["10m and over"]))
    L.append("4. Client dollar forwards falling due in 2027, in millions of dollars:")
    for q in range(1, 5):
        L.append("   - Q%d 2027: exporters sell %.1f; importers buy %.1f" % (q, B["Q%d" % q]["exporters_sell"],
                                                                         B["Q%d" % q]["importers_buy"]))
    L.append("\n### %s\n" % C.G_CHART)
    L.append("5. Bars for the grid settings of 8 to 13 per cent with %d per cent highlighted, against a band for the "
             "expected 2027 volatility between %d and %d per cent and a dashed line at the recorded %.1f per cent."
             % (s, lo, hi, rv["record_vol_pct"]))
    return "\n".join(L) + "\n"


def main(target, golden, figures_path, sub_path):
    fig, call, *_ = compute(target)
    os.makedirs(golden, exist_ok=True)
    write_book(os.path.join(golden, C.G_BOOK), fig, call)
    write_chart(os.path.join(golden, C.G_CHART), fig, call)
    with open(figures_path, "w") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
        f.write("\n")
    with open(sub_path, "w") as f:
        f.write(submission(fig, call))
    return fig


if __name__ == "__main__":
    t = sys.argv[1]
    root = os.path.dirname(os.path.abspath(t))
    print(json.dumps(main(t, os.path.join(root, "golden"), os.path.join(root, "generator", "figures.json"),
                          os.path.join(root, "submission.md")), indent=1))
