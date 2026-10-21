"""task178 goldens: the trestle deck workbook and chart, generator/figures.json and submission.md, every figure read
from calc.py run on the shipped pack."""
from __future__ import annotations

import datetime as dt
import json
import os

import numpy as np

import common as C
import calc

MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December")


def r1(x):
    return float("%.1f" % (x + 1e-9))


def long_date(iso):
    d = dt.date.fromisoformat(iso)
    return "%d %s %d" % (d.day, MONTHS[d.month - 1], d.year)


def figures(target):
    g = calc.golden(target)
    dp = calc.default_path(target)
    E = g["E"]
    rv = calc.rivals(target)
    a = calc.ask_a(target)
    b = calc.ask_b(target)
    annual, design = calc.guidance(target)
    T, H, LD = calc._hw(target)
    fw = calc.forward_mask(LD)
    s = calc.skew_surges(target)
    k = C.DECK_SETTINGS.index(g["pick"])
    f = {
        "call_deck_ft": g["pick"],
        "call_expected_at_deck": r1(g["e_pick"]),
        "call_below_ft": g["below"],
        "call_expected_below": r1(g["e_below"]),
        "default_deck_ft": dp["pick"],
        "default_expected_at_deck": r1(dp["E"][k]),
        "design_msl_ft": design,
        "window_high_waters": int(fw.sum()),
        "window_highest_predicted_ft": float(H[fw].max()),
        "season_skew_surges": int(len(s)),
        "expected_by_setting": {"%.2f" % L: r1(e) for L, e in zip(C.DECK_SETTINGS, E)},
        "default_by_setting": {"%.2f" % L: r1(e) for L, e in zip(C.DECK_SETTINGS, dp["E"])},
        "rival_picks": {k2: calc.pick(v) for k2, v in rv.items()},
        "ask_a": [{"rank": i + 1, "date": d, "level_ft": lv} for i, (d, lv, _) in enumerate(a)],
        "ask_b": {str(y): {"closures": c, "at_street_level": h} for y, (c, h) in b.items()},
        "street_level_ft": C.STREET_LEVEL,
        "stnd_1995_below_mllw_ft": calc.datums(target)["STND1995"],
        "stnd_2026_below_mllw_ft": calc.datums(target)["STND2026"],
        "epoch_msl_ft": calc.datums(target)["MSL"],
        "bracket_offset_ft": C.BRACKET_OFFSET,
        "schedule_ft": list(C.DECK_SETTINGS),
    }
    return f


def write_book(f, path):
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    import postprocess as PP
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Deck elevation"
    bold = Font(bold=True)
    ws.append(["Granite Wharf work trestle: deck elevation for 1 April to 31 May 2027"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Port Tessaly gauge PTG-01, ft above MLLW (1983-2001 epoch), at the 2027 design mean sea level of "
               "%.2f ft MLLW" % f["design_msl_ft"]])
    ws.append([])
    ws.append(["Deck elevation to cut the piles to (ft MLLW)", f["call_deck_ft"]])
    ws["A4"].font = bold; ws["B4"].font = bold
    ws.append(["Tides expected to reach that deck, 1 April to 31 May 2027", f["call_expected_at_deck"]])
    ws.append(["Tides expected to reach the next elevation down (%.2f ft)" % f["call_below_ft"], f["call_expected_below"]])
    ws.append([])
    ws.append(["Pile schedule elevation (ft MLLW)", "Tides expected to reach it", "One tide or fewer"])
    for c in ws[8]:
        c.font = bold
    for L, e in f["expected_by_setting"].items():
        ws.append([float(L), e, "yes" if e <= C.DECK_BAR else "no"])
    ws.append([])
    ws.append(["The April and May 2027 high waters from the 2027 tide table (%d tides, the highest %.1f ft), each with "
               "the April and May skew surges of 1995 to 2026 at the 2027 design mean sea level." % (
                   f["window_high_waters"], f["window_highest_predicted_ft"])])
    ws.column_dimensions["A"].width = 58
    ws.column_dimensions["B"].width = 24
    ws.column_dimensions["C"].width = 18
    ws2 = wb.create_sheet("Survival tides")
    ws2.append(["Five highest tides at the gauge, 1 November 2016 to 30 November 2026, no two within three days"])
    ws2["A1"].font = Font(bold=True)
    ws2.append(["Rank", "Date", "Highest reading (ft MLLW)"])
    for c in ws2[2]:
        c.font = bold
    for r in f["ask_a"]:
        ws2.append([r["rank"], dt.date.fromisoformat(r["date"]), r["level_ft"]])
        ws2.cell(row=ws2.max_row, column=2).number_format = "yyyy-mm-dd"
        ws2.cell(row=ws2.max_row, column=3).number_format = "0.00"
    ws2.column_dimensions["B"].width = 14
    ws2.column_dimensions["C"].width = 26
    ws3 = wb.create_sheet("Front St closures")
    ws3.append(["DPW flooding closures of Front Street, by the year each began"])
    ws3["A1"].font = Font(bold=True)
    ws3.append(["Year", "Closures", "With the gauge at 11.80 ft MLLW or higher within 3 h of the start"])
    for c in ws3[2]:
        c.font = bold
    for y, v in f["ask_b"].items():
        ws3.append([int(y), v["closures"], v["at_street_level"]])
    ws3.column_dimensions["C"].width = 60
    wb.save(path)
    PP.normalize_ooxml(path, "Stacy Huber", "Stacy Huber", "2026-12-09T14:12:05Z", "2026-12-10T20:37:51Z", excel=True,
                       company=C.CITY)


def write_chart(f, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "svg.hashsalt": "task178",
                         "pdf.fonttype": 42})
    xs = [float(k) for k in f["expected_by_setting"]]
    ys = list(f["expected_by_setting"].values())
    fig, ax = plt.subplots(figsize=(8.2, 4.6), dpi=110)
    cols = ["#1f4e6e" if x == f["call_deck_ft"] else "#9fb3c4" for x in xs]
    ax.bar([("%.2f" % x) for x in xs], ys, color=cols, width=0.7)
    for i, v in enumerate(ys):
        ax.text(i, max(v, C.DECK_BAR) + 0.45, "%.1f" % v, ha="center", va="bottom", fontsize=9, color="#30363d")
    ax.axhline(C.DECK_BAR, color="#b5452f", lw=1.1, ls="--")
    ax.text(len(xs) - 0.55, C.DECK_BAR + 2.2, "one tide (the design basis bar)", color="#b5452f", ha="right", fontsize=8.5)
    kd = list(xs).index(f["call_deck_ft"])
    ax.annotate("deck: %.2f ft" % f["call_deck_ft"], xy=(kd, max(ys[kd], C.DECK_BAR) + 1.6), xytext=(kd + 0.9, 9.5),
                fontsize=9.5, color="#1f4e6e", arrowprops=dict(arrowstyle="-", color="#1f4e6e", lw=0.8))
    ax.set_xlabel("Deck elevation on the pile schedule (ft MLLW at PTG-01)")
    ax.set_ylabel("Tides expected to reach the deck")
    ax.set_title("Granite Wharf trestle, 1 April to 31 May 2027: deck set at %.2f ft" % f["call_deck_ft"], fontsize=11)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def submission(f):
    a = f["ask_a"]
    lines = ["## Tags", "",
             "**Domain:** Physical & Environmental Sciences (climate and weather extremes: the expected number of high "
             "waters reaching each candidate deck elevation of a temporary work trestle over a known April to May 2027 "
             "window at a Gulf of Maine harbor gauge, built from the window's own predicted high waters and the season's "
             "skew surges).",
             "**Analytical objective:** Forecasting & Predictive Modeling.", "",
             "## 1. Final Recommendation", "",
             "**Cut the Granite Wharf trestle piles to a deck elevation of %.2f ft MLLW.** High water is expected to reach "
             "that deck on %.1f tides between 1 April and 31 May 2027 and the next elevation down, %.2f ft, on %.1f, "
             "because the window's own high waters in the 2027 tide table sit low. Not %.2f ft, the April and May "
             "record's exceedance rate moved to 2027 sea level, which expects %.1f tides at %.2f ft because it averages "
             "over tides much higher than this spring's." % (
                 f["call_deck_ft"], f["call_expected_at_deck"], f["call_below_ft"], f["call_expected_below"],
                 f["default_deck_ft"], f["default_expected_at_deck"], f["call_deck_ft"]),
             "", "## 2. Critical Components", "",
             "1. Tides expected to reach the deck from 1 April to 31 May 2027 at %.2f ft MLLW: **%.1f**." % (
                 f["call_deck_ft"], f["call_expected_at_deck"]),
             "2. Tides expected to reach the next elevation down, %.2f ft MLLW: **%.1f**." % (
                 f["call_below_ft"], f["call_expected_below"]),
             "3. The 2027 design mean sea level the deck is set at: **%.2f ft MLLW**." % f["design_msl_ft"],
             "", "## 3. Step-by-Step Solution", "",
             "1. Read %s (quality V readings, less the 4.21 ft station datum offset of the datum sheet) and, after June "
             "2026, %s (metres to feet, less the 4.09 ft of STND 2026) as one ft MLLW series." % (C.F_VER, C.F_TEL),
             "2. Converted every high water in %s to UTC (EST all year to 2006, local EST/EDT from 2007) and took the "
             "series' highest reading within three hours of each." % C.F_TABLES,
             "3. For the April and May high waters of 1995 to 2026, took the skew surge (observed less predicted high "
             "water) less that year's mean sea level above the epoch's 5.12 ft from %s." % C.F_SLR,
             "4. For each of the %d high waters of 1 April to 31 May 2027 in the 2027 sheet, took the share of those "
             "skew surges reaching each pile schedule elevation at the %.2f ft design mean sea level, and summed them "
             "per elevation." % (f["window_high_waters"], f["design_msl_ft"]),
             "5. The lowest elevation with one tide or fewer is %.2f ft (%.1f tides), %.2f ft expecting %.1f: cut the "
             "piles to %.2f ft." % (f["call_deck_ft"], f["call_expected_at_deck"], f["call_below_ft"],
                                     f["call_expected_below"], f["call_deck_ft"]),
             "6. Survival tides: the highest reading at each high water from 1 November 2016 to 30 November 2026, the "
             "verified readings between the bracket re-securing on 30 October 2017 and the sensor reset on 12 March "
             "2018 raised 0.08 ft (station log and the datum sheet's levelling), the telemetry on STND 2026, five "
             "largest no two within three days.",
             "7. Street closures: Front Street FLOOD work orders in %s, the WOMS times read as UTC (they precede "
             "high water only so read), a work order opened within three hours of the previous one's closing counted as "
             "the same closure, the gauge's highest reading within three hours of each closure's start against 11.80 ft."
             % C.F_CLOSE,
             "", "## 4. Deliverable Answers", "", "### %s" % C.G_BOOK, "",
             "1. Deck elevation: %.2f ft MLLW." % f["call_deck_ft"],
             "2. Tides expected to reach the deck from 1 April to 31 May 2027: %.1f at %.2f ft, %.1f at %.2f ft." % (
                 f["call_expected_at_deck"], f["call_deck_ft"], f["call_expected_below"], f["call_below_ft"]),
             "3. Five highest tides at the gauge, 1 November 2016 to 30 November 2026, no two within three days:"]
    for r in a:
        lines.append("   - %d. %s, %.2f ft MLLW" % (r["rank"], long_date(r["date"]), r["level_ft"]))
    lines.append("4. Front Street flooding closures by year, each closure once, and those with the gauge at 11.80 "
                 "ft MLLW or higher within three hours either side of the start:")
    for y, v in f["ask_b"].items():
        lines.append("   - %s: %d closures, %d with the gauge at 11.80 ft or higher" % (y, v["closures"], v["at_street_level"]))
    lines += ["", "### %s" % C.G_CHART, "",
              "1. Bar chart of the tides expected to reach the deck at each pile schedule elevation, 10.60 to 12.60 ft, "
              "with a dashed line at one tide and the %.2f ft bar marked." % f["call_deck_ft"], ""]
    return "\n".join(lines)


def main(target, golden_dir, fig_path, sub_path):
    os.makedirs(golden_dir, exist_ok=True)
    f = figures(target)
    write_book(f, os.path.join(golden_dir, C.G_BOOK))
    write_chart(f, os.path.join(golden_dir, C.G_CHART))
    with open(fig_path, "w") as fh:
        json.dump(f, fh, indent=1, sort_keys=True)
        fh.write("\n")
    with open(sub_path, "w") as fh:
        fh.write(submission(f))
    return f
