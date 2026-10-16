"""The goldens: late_shift_staffing_fy2028.xlsx (the call, each fiscal 2028 month's expected compliance, the model
check, the Halvorsen table and the callback table) and late_shift_compliance_fy2028.png (each month's compliance
against the 90 per cent line), and generator/figures.json. Every figure is computed from target/ through calc.py."""
from __future__ import annotations

import datetime as dt
import json
import os

import numpy as np

import calc as CA
import common as K
import postprocess as PP
import records as R

GOLD_BOOK = "late_shift_staffing_fy2028.xlsx"
GOLD_PNG = "late_shift_compliance_fy2028.png"


def pct0(x):
    return int(K.round_half_up(100.0 * x, 0))


def pct1(x):
    return K.round_half_up(100.0 * x, 1)


def compute(target):
    """Every graded figure and the figures the write-up carries, from the shipped files."""
    G = {}
    C = CA.read_calls(target, R.F_LEGACY, R.F_I3)
    busy = CA.estimates(C)[0]
    pat, wab, nab = CA.estimates(C, C.late)[1:]           # the late shift's own callers
    pat_all, wab_all, nab_all = CA.estimates(C)[1:]       # one patience for every call
    pat_rest = CA.estimates(C, ~C.late)[1]
    fc = CA.read_forecast(target, R.F_FORECAST)
    gold = CA.fy2028(fc, busy, pat)
    G["C"], G["fc"] = C, fc
    G["busy"], G["patience"], G["wab"], G["n_abandoned_late"] = busy, pat, wab, nab
    G["patience_all"], G["wab_all"], G["n_abandoned"], G["patience_rest"] = pat_all, wab_all, nab_all, pat_rest
    G["n_911"] = int(C.is911.sum())
    G["n_911_late"] = int((C.is911 & C.late).sum())
    G["gold"] = gold
    G["short"] = CA.short_months(gold)
    G["erlang_c"] = CA.fy2028(fc, busy, pat, model="C")
    G["biased"] = CA.fy2028(fc, busy, wab)
    G["biased_all"] = CA.fy2028(fc, busy, wab_all)
    G["pooled"] = CA.fy2028(fc, busy, pat_all)
    # month totals of forecast late-shift calls
    tot = {}
    for y, m in K.fy_months(2028):
        s_ = 0.0
        for nd in K.late_nights(y, m):
            for h in K.night_hours(nd):
                s_ += fc[(y, m, h.weekday(), h.hour)][0]
        tot[(y, m)] = s_
    G["late_calls"] = tot
    G["nights"] = {(y, m): len(K.late_nights(y, m)) for y, m in K.fy_months(2028)}
    # patience by segment over the whole history (the hang-ups by hour that show the late shift's callers apart)
    seg = {}
    hr = C.lhour
    masks = [("Friday and Saturday nights, 22:00 to 02:00 (the late shift)", C.late),
             ("Friday and Saturday nights, 02:00 to 06:00", C.wknight & ~C.late),
             ("Other nights, 22:00 to 06:00", ~C.wknight & ((hr >= 22) | (hr < 6))),
             ("06:00 to 18:00", (hr >= 6) & (hr < 18)),
             ("18:00 to 22:00", (hr >= 18) & (hr < 22))]
    for lab, msk in masks:
        m_ = C.is911 & msk
        seg[lab] = (int(m_.sum()), int((m_ & C.ab).sum()), float(np.sum(C.wait[m_])), CA.estimates(C, msk)[1])
    G["segments"] = seg
    # out-of-sample check: parameters from January to June 2025, fiscal 2026 predicted
    loc_fy = np.array([K.fiscal_year(K.night_of(K.to_local(x))) for x in C.t])
    m25 = loc_fy == 2025
    b25 = CA.estimates(C, m25)[0]
    p25_late = CA.estimates(C, m25 & C.late)[1]
    p25_rest = CA.estimates(C, m25 & ~C.late)[1]
    p25_all = CA.estimates(C, m25)[1]
    ros = CA.read_roster(target, R.F_ROSTER)
    t0 = K.HIST_START.astimezone(K.UTC).timestamp()
    nh = int(round((K.HIST_END.astimezone(K.UTC).timestamp() - t0) / 3600))
    is_late = lambda key: (key[2] >= 22 and key[3] in (4, 5)) or (key[2] < 2 and key[3] in (5, 6))
    seg_pat = lambda key: p25_late if is_late(key) else p25_rest
    G["bt_params"] = (b25, p25_late, p25_rest, p25_all)
    bt = {}
    for lab, sel in (("late", lambda h: h[4] == 2026 and h[5]), ("rest", lambda h: h[4] == 2026 and not h[5]),
                     ("all", lambda h: h[4] == 2026)):
        seg_model = CA.backtest(C, ros, t0, nh, b25, seg_pat, sel)
        one = CA.backtest(C, ros, t0, nh, b25, p25_all, sel)
        bt[lab] = {"obs": seg_model["obs"], "ab_obs": seg_model["ab_obs"], "A": seg_model["A"], "ab_A": seg_model["ab_A"],
                   "A1": one["A"], "ab_A1": one["ab_A"], "C": seg_model["C"], "calls": seg_model["calls"]}
    G["backtest"] = bt
    G["loc_fy"] = loc_fy
    # ask A
    che = CA.read_che(target, R.F_CHE)
    polys = CA.read_boundary(target, R.F_BOUNDARY)
    dr = CA.read_directory(target, R.F_DIRECTORY)
    G["ask_a"] = CA.ask_a(C, che, polys, dr)
    G["che"], G["polys"], G["directory"] = che, polys, dr
    # ask B
    tasks = CA.read_callbacks(target, R.F_CALLBACK)
    share, den = CA.ask_b(C, tasks)
    G["ask_b"], G["ask_b_den"], G["tasks"] = share, den, tasks
    G["ask_b_num"] = {k: int(round(share[k] * den[k])) for k in share}
    return G


def _label(y, m):
    return "%s %d" % (K.MONTH_NAMES[m], y)


def write_book(path, G):
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Summary"
    short = ", ".join("%s %d" % (K.MONTH_NAMES[m], y) for y, m in G["short"])
    lines = [
        ("Friday and Saturday late shift (22:00 to 02:00), fiscal 2028: the case for a seasonal fifth call-taker", True),
        ("Prepared for the operations manager's FY2028 staffing request, 9 October 2026", False),
        ("", False),
        ("Recommendation", True),
        ("Fund a seasonal fifth call-taker on Friday and Saturday nights in July 2027, August 2027 and June 2028. With the "
         "four call-takers the FY2028 budget funds, those three months fall below the 90 per cent standard (July %d, "
         "August %d and June %d per cent); every other month stays above it, May and September at %d per cent."
         % (pct0(G["gold"][(2027, 7)]), pct0(G["gold"][(2027, 8)]), pct0(G["gold"][(2028, 6)]),
            pct0(G["gold"][(2027, 9)])), False),
        ("", False),
        ("How the months were forecast", True),
        ("Each forecast hour of the late shift is a queue of four call-takers whose callers hang up when they have "
         "waited too long (Erlang A), on the Tri-County board's FY2028 forecast for each Friday and Saturday night hour.",
         False),
        ("Busy time per answered 911 call, answer to Ready, January 2025 to September 2026: %.1f seconds." % G["busy"], False),
        ("The agency's callers are not alike. On Friday and Saturday nights from 22:00 they hang up far sooner than at "
         "any other time (Model check, patience by segment). The late shift's own callers' patience, the time all {:,} of its 911 "
         "calls waited divided by the {:,} that hung up before an answer, is {:.1f} seconds; the rest of the week's is "
         "{:.1f}. An answered caller's wait only shows that they would have held on at least that long."
         .format(G["n_911_late"], G["n_abandoned_late"], G["patience"], G["patience_rest"]), False),
        ("The standard queue with no hang-ups (Erlang C), or one patience for every call ({:.1f} seconds), would put May "
         "to September below 90 per cent; the patience read off the late shift's hang-ups' own waits ({:.1f} seconds) "
         "would put no month below it. See Model check.".format(G["patience_all"], G["wab"]), False),
    ]
    for i, (t, bold) in enumerate(lines, start=1):
        c = ws.cell(row=i, column=1, value=t if t else None)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        if bold:
            c.font = Font(bold=True, size=12 if i == 1 else 11)
    ws.column_dimensions["A"].width = 118
    # fiscal 2028 months
    w = wb.create_sheet("FY2028 late shift")
    head = ["Month", "Friday and Saturday nights", "Forecast late-shift 911 calls", "Expected compliance (%)",
            "Below 90 per cent"]
    for j, h in enumerate(head, start=1):
        w.cell(row=1, column=j, value=h).font = Font(bold=True)
    fill = PatternFill("solid", fgColor="F4D6D6")
    for i, (y, m) in enumerate(K.fy_months(2028), start=2):
        g = G["gold"][(y, m)]
        vals = [_label(y, m), G["nights"][(y, m)], int(round(G["late_calls"][(y, m)])), pct0(g),
                "yes" if g < 0.90 else "no"]
        for j, v in enumerate(vals, start=1):
            c = w.cell(row=i, column=j, value=v)
            if g < 0.90:
                c.fill = fill
    w.freeze_panes = "A2"
    for i in range(2, 14):
        w.cell(row=i, column=3).number_format = "#,##0"
    w.cell(row=15, column=1, value="Four call-takers on every late-shift night. Compliance as SOP 2.10 measures it: "
           "calls answered within 15 seconds over calls presented less those abandoned within 5 seconds; each night "
           "counted in the month it starts.")
    for col, wd in zip("ABCDE", (18, 26, 28, 24, 18)):
        w.column_dimensions[col].width = wd
    # model check
    w = wb.create_sheet("Model check")
    b25, p25l, p25r, p25a = G["bt_params"]
    w.cell(row=1, column=1, value="Fiscal 2026 predicted from January to June 2025 (busy time %.1f s; patience %.1f s on "
           "the late shift, %.1f s at other hours, %.1f s for every call together), every hour on its own call-takers and "
           "calls" % (b25, p25l, p25r, p25a)).font = Font(bold=True)
    head = ["Hours", "Calls", "Observed compliance (%)", "Observed hang-ups (% of calls)",
            "Erlang A, each segment's patience (%)", "Hang-ups (% of calls)", "Erlang A, one patience (%)",
            "Hang-ups (% of calls)", "Erlang C (%)"]
    for j, h in enumerate(head, start=1):
        w.cell(row=3, column=j, value=h).font = Font(bold=True)
        w.cell(row=3, column=j).alignment = Alignment(wrap_text=True, vertical="top")
    labs = {"late": "Friday and Saturday late shift", "rest": "Every other hour", "all": "The whole floor"}
    for i, k in enumerate(("late", "rest", "all"), start=4):
        bt = G["backtest"][k]
        vals = [labs[k], int(round(bt["calls"])), pct1(bt["obs"]), K.round_half_up(100 * bt["ab_obs"], 2), pct1(bt["A"]),
                K.round_half_up(100 * bt["ab_A"], 2), pct1(bt["A1"]), K.round_half_up(100 * bt["ab_A1"], 2), pct1(bt["C"])]
        for j, v in enumerate(vals, start=1):
            c = w.cell(row=i, column=j, value=v)
            if k == "late":
                c.font = Font(bold=True)
        w.cell(row=i, column=2).number_format = "#,##0"
        for j in (3, 5, 7, 9):
            w.cell(row=i, column=j).number_format = "0.0"
        for j in (4, 6, 8):
            w.cell(row=i, column=j).number_format = "0.00"
    w.cell(row=9, column=1, value="Patience by segment, January 2025 to September 2026").font = Font(bold=True)
    head = ["Hours", "911 calls", "Hung up before an answer", "Total waiting time (s)", "Patience (s)"]
    for j, h in enumerate(head, start=1):
        w.cell(row=10, column=j, value=h).font = Font(bold=True)
    for i, (lab, (n_, a_, tw, pt)) in enumerate(G["segments"].items(), start=11):
        for j, v in enumerate((lab, n_, a_, int(round(tw)), round(pt, 1)), start=1):
            w.cell(row=i, column=j, value=v)
        for j in (2, 3, 4):
            w.cell(row=i, column=j).number_format = "#,##0"
        w.cell(row=i, column=5).number_format = "0.0"
    w.cell(row=17, column=1, value="Patience is the total time the segment's calls waited, answered or not, over the "
           "calls that hung up: an answered call's wait is time its caller held on.")
    for col, wd in zip("ABCDEFGHI", (44, 11, 14, 16, 20, 14, 18, 14, 12)):
        w.column_dimensions[col].width = wd
    w.freeze_panes = "B4"
    # Halvorsen
    w = wb.create_sheet("Halvorsen FY2026")
    head = ["Quarter", "Wireless 911 calls placed from Halvorsen Township that reached the agency",
            "Of them, transferred to Wexley County Emergency Communications"]
    for j, h in enumerate(head, start=1):
        w.cell(row=1, column=j, value=h).font = Font(bold=True)
        w.cell(row=1, column=j).alignment = Alignment(wrap_text=True)
    qn = {1: "Q1 (July to September 2025)", 2: "Q2 (October to December 2025)", 3: "Q3 (January to March 2026)",
          4: "Q4 (April to June 2026)"}
    for i, q in enumerate((1, 2, 3, 4), start=2):
        r, t = G["ask_a"][(2026, q)]
        for j, v in enumerate((qn[q], r, t), start=1):
            w.cell(row=i, column=j, value=v)
    for i in range(2, 6):
        for j in (2, 3):
            w.cell(row=i, column=j).number_format = "#,##0"
    w.cell(row=7, column=1, value="Placed by each call's last handset location in the township boundary, answered or "
           "not, the backup centre's records found by the call's incident identifier; transfers to either of Wexley's "
           "PSAP URIs in the ESInet directory.")
    for col, wd in zip("ABC", (30, 34, 34)):
        w.column_dimensions[col].width = wd
    # callbacks
    w = wb.create_sheet("Callbacks Jan-Jun 2026")
    head = ["Month", "Abandoned 911 calls", "Dialled back within two minutes", "Share (%)"]
    for j, h in enumerate(head, start=1):
        w.cell(row=1, column=j, value=h).font = Font(bold=True)
    for i, (y, m) in enumerate([(2026, k) for k in range(1, 7)], start=2):
        vals = [_label(y, m), G["ask_b_den"][(y, m)], G["ask_b_num"][(y, m)], pct1(G["ask_b"][(y, m)])]
        for j, v in enumerate(vals, start=1):
            w.cell(row=i, column=j, value=v)
    for i in range(2, 8):
        w.cell(row=i, column=4).number_format = "0.0"
    w.cell(row=9, column=1, value="Every abandoned 911 call, by the month of its hang-up; dialled back when the "
           "callback desk's first dial to its number came within 120 seconds after the hang-up, a repeat abandon "
           "joined to the open task included.")
    for col, wd in zip("ABCD", (18, 20, 30, 12)):
        w.column_dimensions[col].width = wd
    wb.save(path)


def write_png(path, G):
    import matplotlib
    matplotlib.use("Agg")
    matplotlib.rcParams["svg.hashsalt"] = "task148"
    import matplotlib.pyplot as plt
    months = K.fy_months(2028)
    vals = [100.0 * G["gold"][ym] for ym in months]
    fig, ax = plt.subplots(figsize=(9.0, 4.6), dpi=110)
    cols = ["#9c2b2b" if v < 90 else "#5b7a99" for v in vals]
    xs = np.arange(len(months))
    ax.bar(xs, vals, color=cols, width=0.68)
    ax.axhline(90, color="#222222", linewidth=1.2, linestyle="--")
    ax.text(-0.45, 90.15, "Standard: 90%", ha="left", va="bottom", fontsize=8.5)
    for x, v in zip(xs, vals):
        ax.text(x, v + 0.12, "%d%%" % int(K.round_half_up(v, 0)), ha="center", va="bottom", fontsize=8.5)
    ax.set_xticks(xs)
    ax.set_xticklabels(["%s\n%d" % (K.MON3[m], y) for y, m in months], fontsize=8.5)
    ax.set_ylim(85, 97)
    ax.set_ylabel("Calls answered within 15 seconds (%)", fontsize=9)
    ax.set_title("With four call-takers, July, August and June fall below the 90 per cent standard\n"
                 "Friday and Saturday late shift (22:00 to 02:00), fiscal 2028: expected share of 911 calls answered "
                 "within 15 seconds", fontsize=10)
    fig.text(0.01, 0.01, "Source: Tri-County Regional 911 Board FY2028 hourly forecast; ACD history January 2025 to "
             "September 2026 (busy time %.0f s; late-shift callers' patience %.0f s).\nRed: below the standard, a "
             "seasonal fifth call-taker needed." % (G["busy"], G["patience"]), fontsize=7.2, color="#555555")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def figures(G):
    bt = G["backtest"]
    F = {"call": {"months_short": ["%s %d" % (K.MONTH_NAMES[m], y) for y, m in G["short"]], "fifth_call_taker_months": 3},
         "fiscal_2028_compliance_pct": {"%s %d" % (K.MONTH_NAMES[m], y): pct0(G["gold"][(y, m)]) for y, m in K.fy_months(2028)},
         "fiscal_2028_compliance_unrounded": {"%s %d" % (K.MON3[m], y): round(100 * G["gold"][(y, m)], 3) for y, m in K.fy_months(2028)},
         "parameters": {"busy_time_s": round(G["busy"], 1), "patience_late_shift_s": round(G["patience"], 1),
                        "patience_rest_of_week_s": round(G["patience_rest"], 1),
                        "patience_every_call_s": round(G["patience_all"], 1),
                        "hangups_own_wait_late_shift_s": round(G["wab"], 1), "hangups_own_wait_every_call_s": round(G["wab_all"], 1),
                        "calls_911": G["n_911"], "calls_911_late_shift": G["n_911_late"],
                        "abandoned_911": G["n_abandoned"], "abandoned_911_late_shift": G["n_abandoned_late"],
                        "call_takers": 4, "standard_pct": 90, "seconds": 15, "misdial_seconds": 5},
         "rivals": {"erlang_c_july_pct": pct0(G["erlang_c"][(2027, 7)]),
                    "erlang_c_months_short": ["%s %d" % (K.MONTH_NAMES[m], y) for y, m in CA.short_months(G["erlang_c"])],
                    "one_patience_months_short": ["%s %d" % (K.MONTH_NAMES[m], y) for y, m in CA.short_months(G["pooled"])],
                    "hangups_wait_july_pct": pct0(G["biased"][(2027, 7)])},
         "backtest_fy2026_late_shift": {"observed_pct": pct1(bt["late"]["obs"]), "erlang_a_pct": pct1(bt["late"]["A"]),
                                        "one_patience_pct": pct1(bt["late"]["A1"]), "erlang_c_pct": pct1(bt["late"]["C"]),
                                        "hangups_observed_pct": K.round_half_up(100 * bt["late"]["ab_obs"], 2),
                                        "hangups_erlang_a_pct": K.round_half_up(100 * bt["late"]["ab_A"], 2),
                                        "hangups_one_patience_pct": K.round_half_up(100 * bt["late"]["ab_A1"], 2)},
         "backtest_params": {"busy_s": round(G["bt_params"][0], 1), "patience_late_shift_s": round(G["bt_params"][1], 1),
                             "patience_rest_s": round(G["bt_params"][2], 1), "patience_every_call_s": round(G["bt_params"][3], 1)},
         "ask_a": {"Q%d" % q: {"reached": G["ask_a"][(2026, q)][0], "transferred_to_wexley": G["ask_a"][(2026, q)][1]}
                   for q in (1, 2, 3, 4)},
         "ask_b": {"%s 2026" % K.MONTH_NAMES[m]: {"share_pct": pct1(G["ask_b"][(2026, m)]),
                                                  "abandoned": G["ask_b_den"][(2026, m)],
                                                  "dialled_within_2_min": G["ask_b_num"][(2026, m)]} for m in range(1, 7)},
         "years": [2025, 2026, 2027, 2028], "late_shift": "22:00 to 02:00",
         "references": {"service": "911", "procedure": "SOP 2.10", "sections": ["2.2", "3.3", "4.2", "5.1", "6.1"]}}
    return F


def write_submission(path, G):
    """submission.md, drafted from the computed figures (every number in blocks 1 to 4 comes from G)."""
    g = G["gold"]
    bt = G["backtest"]["late"]
    A = G["ask_a"]
    pc = lambda ym: pct0(g[ym])
    others = sorted({pct0(g[ym]) for ym in K.fy_months(2028) if ym not in G["short"]})
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Urban & Regional Science (municipal service demand and resource allocation).")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Fund a seasonal fifth call-taker on the Friday and Saturday late shift in July 2027, August 2027 and June "
             "2028: with the four call-takers the FY2028 budget funds, those are the months of fiscal 2028 that fall "
             "short of the 90 per cent answering standard.**")
    L.append("July is expected at %d per cent and August and June at %d, while May and September, the closest above, sit "
             "at %d. Not Erlang C, which has every caller wait until answered and puts May to September short; not one "
             "patience for every call, which brings the rest of the week's patient callers onto the late shift and puts "
             "May to September short as well; not a patience read off the hang-ups' own waits, which leaves no month "
             "short." % (pc((2027, 7)), pc((2027, 8)), pc((2027, 9))))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. Expected compliance in the months that fall short: July 2027 **%d%%**, August 2027 **%d%%**, June 2028 "
             "**%d%%**; the closest months above the standard, September 2027 and May 2028, at **%d%%**."
             % (pc((2027, 7)), pc((2027, 8)), pc((2028, 6)), pc((2027, 9))))
    L.append("2. The queue runs on the late shift's own callers' patience, about two minutes, estimated on the late "
             "shift's calls alone.")
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Read acd_call_detail_legacy_2025-01-01_2025-05-16.csv (local time) and "
             "i3_call_log_2025-05-13_2026-09-30.jsonl (UTC) as one list of {:,} 911 calls, test calls left out as SOP "
             "2.10 section 2.2 has it.".format(G["n_911"]))
    L.append("2. Busy time: the mean of ready less answered over the answered calls, a position being busy until the "
             "call-taker sets Ready (SOP 2.10 section 4.2): %.1f seconds." % G["busy"])
    L.append("3. Patience, by segment: every call's wait (answer or hang-up less presentation) summed and divided by the "
             "calls that hung up, an answered call's wait counting as time its caller held on. On the late shift's own "
             "{:,} calls ({:,} hung up) it is {:.1f} seconds; at every other hour {:.1f}; over every call together {:.1f}."
             .format(G["n_911_late"], G["n_abandoned_late"], G["patience"], G["patience_rest"], G["patience_all"]))
    L.append("4. Checked out of sample: with January to June 2025's parameters, the late shift's fiscal 2026 hours hung "
             "up on %.2f per cent of calls; the late shift's own patience predicts %.2f, one patience for every call %.2f "
             "and Erlang C none." % (K.round_half_up(100 * bt["ab_obs"], 2), K.round_half_up(100 * bt["ab_A"], 2),
                                     K.round_half_up(100 * bt["ab_A1"], 2)))
    L.append("5. Took the agency's FY2028 rows of tri_county_911_hourly_forecast_fy2027_fy2028.xlsx (SOP 2.10 section "
             "5.1) for Friday and Saturday 22:00 and 23:00 and Saturday and Sunday 00:00 and 01:00, each night on the "
             "forecast of the month it starts (SOP 2.10 section 6.1).")
    L.append("6. Modelled each hour as a queue of four call-takers whose callers hang up (Erlang A, M/M/4+M) on those "
             "calls per hour with the busy time and the late shift's patience, and took each month's compliance as SOP "
             "2.10 section 3.3 defines it: expected calls answered within 15 seconds over expected calls less those "
             "abandoned within 5.")
    L.append("7. July 2027 (%d%%), August 2027 (%d%%) and June 2028 (%d%%) fall below 90 per cent; the other months "
             "are %d to %d per cent." % (pc((2027, 7)), pc((2027, 8)), pc((2028, 6)), others[0], others[-1]))
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### late_shift_staffing_fy2028.xlsx")
    L.append("")
    L.append("1. Months below 90 per cent, for a seasonal fifth call-taker: July 2027, August 2027 and June 2028.")
    L.append("2. Expected answer-time compliance by month, whole per cent:")
    for y, m in K.fy_months(2028):
        L.append("   - %s %d: %d%%" % (K.MONTH_NAMES[m], y, pc((y, m))))
    L.append("3. Wireless 911 calls placed from Halvorsen Township that reached the agency in fiscal 2026, answered or "
             "not, and of them transferred to Wexley County Emergency Communications:")
    qn = {1: "July to September 2025", 2: "October to December 2025", 3: "January to March 2026", 4: "April to June 2026"}
    for q in (1, 2, 3, 4):
        r, t = A[(2026, q)]
        L.append("   - Q{} ({}): {:,} reached, {:,} transferred".format(q, qn[q], r, t))
    L.append("4. Share of abandoned 911 calls dialled back within two minutes of the hang-up:")
    for m in range(1, 7):
        L.append("   - %s 2026: %.1f%%" % (K.MONTH_NAMES[m], pct1(G["ask_b"][(2026, m)])))
    L.append("")
    L.append("### late_shift_compliance_fy2028.png")
    L.append("")
    L.append("1. Bar chart of the twelve months' expected compliance against a dashed 90 per cent line, July 2027, "
             "August 2027 and June 2028 in red below it.")
    L.append("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


def main(target, golden, figures_path, B=None):
    os.makedirs(golden, exist_ok=True)
    G = compute(target)
    write_book(os.path.join(golden, GOLD_BOOK), G)
    PP.normalize_ooxml(os.path.join(golden, GOLD_BOOK), "Leon Carpenter", "Leon Carpenter", "2026-10-07T15:12:40Z",
                       "2026-10-09T18:46:02Z", excel=True, company=K.AGENCY)
    write_png(os.path.join(golden, GOLD_PNG), G)
    F = figures(G)
    write_submission(os.path.join(os.path.dirname(os.path.abspath(golden)), "submission.md"), G)
    with open(figures_path, "w") as fh:
        json.dump(F, fh, indent=1)
        fh.write("\n")
    return G
