"""The goldens: the board's workbook (each region's estimated share of expansion members who worked 80 hours or more in
March 2026, the four regions for the track, and the members covered and the parents and caretakers of a child under 14
on 1 October 2026) and the chart of the ten shares, plus figures.json."""
import decimal
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                       # noqa: E402
from openpyxl import Workbook                         # noqa: E402
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side   # noqa: E402
from openpyxl.utils import get_column_letter          # noqa: E402

import common as K                                    # noqa: E402

TEAL = "14606B"
THIN = Side(style="thin", color="B8BFC4")


def pct(x):
    """A share as a whole percent, half up, from the unrounded share."""
    return int(decimal.Decimal(repr(float(x) * 100)).quantize(decimal.Decimal("1"), rounding=decimal.ROUND_HALF_UP))


def figures(c, a, b):
    order = c["order"]
    names = [K.NAME[K.CODES[i]] for i in order]
    four = [K.NAME[K.CODES[i]] for i in order[:4]]
    S = c["SS"]
    out = S["out"]
    reg = S["reg"]
    known = S["y"] >= 0
    p = c["p"][0]
    return {
        "call": {"regions": four, "first_below": names[4], "order": names},
        "share": {K.NAME[K.CODES[i]]: pct(c["share"][i]) for i in range(10)},
        "share_unrounded": {K.NAME[K.CODES[i]]: round(float(c["share"][i]), 6) for i in range(10)},
        "sampled": {K.NAME[K.CODES[i]]: int((reg == i).sum()) for i in range(10)},
        "outcomes": {"completed": int((out == 1).sum()), "declined": int((out == 2).sum()),
                     "declined_key_answered": int(((out == 2) & known).sum()), "not_reached": int((out == 0).sum()),
                     "known": int(known.sum()), "sampled": int(len(out))},
        "filed": {"hours": 80, "ages": [19, 64], "per_region": 1500, "reached_codes": [1100, 2110],
                  "clauses": ["2.1", "2.4", "3.1", "3.2", "3.3"]},
        "known_share": {K.NAME[K.CODES[i]]: pct(S["y"][known & (reg == i)].mean()) for i in range(10)},
        "overall": {"estimated": pct(float(c["share"].mean())), "interviewed": pct(S["y"][out == 1].mean())},
        "answer_rate": {"worked_80": {"day": round(float(p[1, 0]), 3), "evening": round(float(p[1, 1]), 3),
                                      "saturday": round(float(p[1, 2]), 3)},
                        "not_80": {"day": round(float(p[0, 0]), 3), "evening": round(float(p[0, 1]), 3),
                                   "saturday": round(float(p[0, 2]), 3)}},
        "ask_a": {K.NAME[k]: int(v) for k, v in a.items()},
        "ask_b": {K.NAME[k]: int(v) for k, v in b.items()},
        "totals": {"ask_a": int(sum(a.values())), "ask_b": int(sum(b.values()))},
    }


def _head(ws, row, cols):
    for j, h in enumerate(cols, 1):
        cell = ws.cell(row, j, h)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=TEAL)
        cell.alignment = Alignment(wrap_text=True, vertical="center")


def workbook(path, fig):
    wb = Workbook()
    ws = wb.active
    ws.title = "Regions"
    ws["A1"] = "Community Engagement Support track 2027: the four regions"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Track regions: %s. Each region's share is estimated for all 1,500 members the survey sampled there, "
                "reached or not." % ", ".join(fig["call"]["regions"]))
    ws["A2"].font = Font(italic=True, size=9)
    cols = ["Apple Health region", "Members sampled", "Estimated share who worked 80 hours or more, March 2026",
            "Rank (smallest share first)", "2027 track", "Members covered on 1 October 2026",
            "Parents and caretakers of a child under 14"]
    _head(ws, 4, cols)
    ws.row_dimensions[4].height = 44
    for i, n in enumerate(fig["call"]["order"], 5):
        on = n in fig["call"]["regions"]
        vals = [n, fig["sampled"][n], fig["share"][n] / 100, i - 4, "Yes" if on else None, fig["ask_a"][n],
                fig["ask_b"][n]]
        for j, v in enumerate(vals, 1):
            cell = ws.cell(i, j, v)
            cell.border = Border(bottom=THIN)
            if j == 3:
                cell.number_format = "0%"
            if j in (2, 6, 7):
                cell.number_format = "#,##0"
            if on:
                cell.font = Font(bold=True)
    t = 5 + len(fig["call"]["order"])
    ws.cell(t, 1, "Ten regions").font = Font(bold=True)
    for j, key in ((6, "ask_a"), (7, "ask_b")):
        c = ws.cell(t, j, fig["totals"][key])
        c.font = Font(bold=True)
        c.number_format = "#,##0"
    c = ws.cell(t, 2, sum(fig["sampled"].values()))
    c.font = Font(bold=True)
    c.number_format = "#,##0"
    for j, wdt in enumerate([22, 11, 20, 13, 9, 15, 17], 1):
        ws.column_dimensions[get_column_letter(j)].width = wdt
    ws.freeze_panes = "B5"
    wn = wb.create_sheet("Notes")
    notes = [
        "How the shares were estimated",
        "The survey's 1,500 sampled members in each region, from the sample file, with every call to each of them from "
        "the Kestrelby dialer export and the Member Services Center CRM export (survey calls only; pilot and test "
        "calls left out) and the outcome of each from the interview file (completed interviews and the key question "
        "answered by members who declined).",
        "A member's class (worked for pay 80 hours or more in March 2026, or not) is known for the members interviewed "
        "and for those who answered the key question. For the rest it is estimated from the member's own calls: a "
        "latent class model in which each class has its own chance that a call reaches the member in each calling "
        "window (weekday day, weekday evening, Saturday), the same in every region, and a member reached declines with "
        "the same chance in either class. Fitted by maximum likelihood (EM) to every sampled member's calls.",
        "Shares compared unrounded and shown to the whole percent (criteria 2.4).",
        "",
        "Planning figures",
        "Members covered on 1 October 2026: expansion members aged 19 to 64 that day whose coverage included it, by the "
        "region of the county lived in that day (criteria 3.1 and 3.2), rebuilt from the roster of 19 October and the "
        "change log for 1 to 19 October.",
        "Parents and caretakers: of those members, case heads, spouses and caretaker relatives in an Apple Health case "
        "with a child under 14 in it on 1 October 2026 (criteria 3.3), from the household composition extract of 15 "
        "October, a child's age and days in the case taken on 1 October.",
    ]
    for line in notes:
        wn.append([line] if line else [None])
    wn["A1"].font = Font(bold=True)
    wn["A6"].font = Font(bold=True)
    for row in wn.iter_rows(min_row=1, max_row=len(notes)):
        row[0].alignment = Alignment(wrap_text=True, vertical="top")
    wn.column_dimensions["A"].width = 120
    wb.save(path)


def chart(path, fig):
    names = fig["call"]["order"]
    vals = [100 * fig["share_unrounded"][n] for n in names]
    on = [n in fig["call"]["regions"] for n in names]
    fig_, ax = plt.subplots(figsize=(8.2, 4.9), dpi=150)
    y = list(range(len(names)))[::-1]
    ax.barh(y, vals, height=0.62, color=["#14606b" if o else "#b4bcc2" for o in on], zorder=3)
    for yy, n, v in zip(y, names, vals):
        ax.text(v + 0.6, yy, "%d%%" % fig["share"][n], va="center", fontsize=9, color="#1f2428")
    cut = (y[3] + y[4]) / 2
    ax.axhline(cut, color="#1f2428", lw=0.8, ls="--", zorder=4)
    ax.text(69.5, cut + 0.12, "four navigator teams", fontsize=8, color="#5d646a", ha="right", va="bottom")
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=9)
    ax.set_xlim(0, 70)
    ax.set_xticks(range(0, 71, 10))
    ax.set_xticklabels(["%d%%" % t for t in range(0, 71, 10)], fontsize=8)
    ax.set_xlabel("Estimated share of expansion members aged 19 to 64 who worked 80 hours or more, March 2026",
                  fontsize=8.5)
    ax.grid(axis="x", color="#e3e7ea", lw=0.6, zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    four = fig["call"]["regions"]
    fig_.text(0.01, 0.975, "%s, %s, %s and %s have the smallest shares already working 80 hours a month"
              % tuple(four), fontsize=10.5, ha="left", va="top")
    fig_.text(0.01, 0.012, "Source: 2026 Member Work and Income Survey, 1,500 sampled members per region. Shares for every "
              "sampled member, reached or not,\nestimated from a callback model of the Member Services Center's and "
              "Kestrelby's call records.", fontsize=7, color="#5d646a", linespacing=1.35)
    fig_.tight_layout(rect=(0, 0.055, 1, 0.94))
    fig_.savefig(path, metadata={"Software": None})
    plt.close(fig_)


def write_figures(path, fig):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(fig, f, indent=1, ensure_ascii=False)
        f.write("\n")


def write(target, golden):
    """Read the cut pack as the golden reads it, then write the workbook, the chart and figures.json."""
    import warnings
    warnings.filterwarnings("ignore")
    import analysis as A
    import routes as RT
    c = A.call(target)
    a, b = A.planning(target)
    fig = figures(c, a, b)
    R = RT.run(c)
    gold = set(fig["call"]["regions"])

    def off(route):
        return [K.NAME[K.CODES[i]] for i in sorted(RT.four(R[route]), key=lambda i: R[route][i])
                if K.NAME[K.CODES[i]] not in gold]
    fig["rivals"] = {"respondents_not_golden": off("respondents (interviews)"),
                     "cells_not_golden": off("age and sex cells"),
                     "late_not_golden": off("reached at call 4 or later, carried")}
    if os.path.exists(golden):
        import shutil
        shutil.rmtree(golden)
    os.makedirs(golden)
    workbook(os.path.join(golden, K.DELIVERABLES[0]), fig)
    chart(os.path.join(golden, K.DELIVERABLES[1]), fig)
    return fig, dict(c=c, a=a, b=b)
