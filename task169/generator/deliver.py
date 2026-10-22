"""task169 deliver: the golden workbook and chart, generator/figures.json and submission.md, every figure computed
from the shipped pack by calc.py."""
from __future__ import annotations

import datetime as dt
import json
import os

import numpy as np

import common as C
import calc

WB = "returns_projection_2027.xlsx"
PNG = "detainer_days_2025.png"
MONTH_NAME = ("July", "August", "September", "October", "November", "December", "January", "February", "March",
              "April", "May", "June")


def compute(target):
    D = calc.load(target)
    S = calc.spells(D)
    g = calc.golden(D, S)
    s = calc.summarise(D, g["p"])
    proj = D["proj"]
    dist_n = {d: int((proj.dist == d).sum()) for d in C.DISTRICTS}
    order = sorted(C.DISTRICTS, key=lambda d: s[d])
    A = calc.ask_a(D)
    B = calc.ask_b(D)
    ch = calc.ask_chart(D)
    return dict(D=D, S=S, g=g, s=s, n=len(proj), dist_n=dist_n, high=order[-1], low=order[0], A=A, B=B, chart=ch)


def figures(r):
    f = {"call": {"rate_step": calc.step5(r["s"]["all"]), "highest_district": r["high"], "lowest_district": r["low"]},
         "cohort_size": r["n"], "spells": len(r["S"]), "window_days": C.WINDOW}
    for o, d in zip(calc.OFFICES, C.DISTRICTS):
        f["a1_" + o] = {"arrest": r["A"][o]["arrest"], "conditions": r["A"][o]["conditions"]}
    for d in C.DISTRICTS:
        f["b_" + d] = dict(r["B"][d])
    f["chart"] = {d: sum(r["B"][d].values()) for d in C.DISTRICTS}
    return f


def write_workbook(path, r):
    import xlsxwriter
    import postprocess as PP
    wb = xlsxwriter.Workbook(path)
    title = wb.add_format({"bold": True, "font_size": 13})
    sub = wb.add_format({"italic": True, "font_color": "#595959"})
    hf = wb.add_format({"bold": True, "bg_color": "#DCE6F1", "border": 1, "text_wrap": True, "valign": "top"})
    big = wb.add_format({"bold": True, "font_size": 12, "num_format": "0%"})
    pct1 = wb.add_format({"num_format": "0.0%"})
    pct0 = wb.add_format({"num_format": "0%"})
    num = wb.add_format({"num_format": "#,##0"})
    bold = wb.add_format({"bold": True})
    boldnum = wb.add_format({"bold": True, "num_format": "#,##0", "top": 1})
    wrap = wb.add_format({"text_wrap": True, "valign": "top"})

    ws = wb.add_worksheet("Projection 2027")
    ws.write(0, 0, "Two-year returns of the 2027 parole releases under Act 26-114", title)
    ws.write(1, 0, "Research and Projections Unit, prison population projection 2027. Records to 30 September 2026.", sub)
    ws.write(3, 0, "Two-year return rate carried in the projection", bold)
    ws.write_number(3, 3, calc.step5(r["s"]["all"]) / 100, big)
    ws.write(4, 0, "District with the highest rate", bold)
    ws.write(4, 3, r["high"], bold)
    ws.write(5, 0, "District with the lowest rate", bold)
    ws.write(5, 3, r["low"], bold)
    ws.write_row(7, 0, ["Parole district", "Office", "2027 releases to parole", "Estimated two-year return rate",
                        "Expected returns"], hf)
    for i, d in enumerate(C.DISTRICTS, start=8):
        ws.write(i, 0, d)
        ws.write(i, 1, C.OFFICE[d])
        ws.write_number(i, 2, r["dist_n"][d], num)
        ws.write_number(i, 3, r["s"][d], pct1)
        ws.write_number(i, 4, r["s"][d] * r["dist_n"][d], num)
    ws.write(12, 0, "State", bold)
    ws.write_number(12, 2, r["n"], boldnum)
    ws.write_number(12, 3, r["s"]["all"], wb.add_format({"bold": True, "num_format": "0.0%", "top": 1}))
    ws.write_number(12, 4, r["s"]["all"] * r["n"], boldnum)
    notes = ["Cohort: the Department's projected-release extract of 9 October 2026, projected movements PAR and RPR in 2027.",
             "A return is an ADM movement from the day after release to day 730 (methodology 3.1). Under the Act the "
             "Board recommits no one, so every return is a new court commitment.",
             "Arrests per day out of Department custody in the first 730 days after each 2019 to September 2024 release "
             "to parole, by time since release, age, prior commitments, offence, sex and district.",
             "Each arrest's chance of a Department sentence and the time from arrest to admission are the courts' own, "
             "by charge grade (felony A-B, felony C-E, misdemeanour), from arrests to 30 June 2024 that went to court; "
             "arrests the Board answered by revoking parole are left out because no court decided them.",
             "The rate is carried in steps of five percentage points (methodology 3.3); the district rates are shown at "
             "the model's precision for ranking only."]
    for i, t in enumerate(notes, start=14):
        ws.write(i, 0, t)
    ws.set_column(0, 0, 30)
    ws.set_column(1, 1, 8)
    ws.set_column(2, 4, 16)

    ws2 = wb.add_worksheet("Board revocations FY26")
    ws2.write(0, 0, "Parole revocations the Board ordered, 1 July 2025 to 30 June 2026, not rescinded", title)
    ws2.write(1, 0, "Legacy system actions to 2 January 2026 and the new case system from 5 January; entries the legacy "
                    "system took for carried-over cases after its close are counted once, from the new system.", sub)
    ws2.write_row(3, 0, ["District office", "Parole district", "On a reported arrest", "On conditions alone", "Total"], hf)
    for i, (o, d) in enumerate(zip(calc.OFFICES, C.DISTRICTS), start=4):
        a, c = r["A"][o]["arrest"], r["A"][o]["conditions"]
        ws2.write(i, 0, o)
        ws2.write(i, 1, d)
        ws2.write_number(i, 2, a, num)
        ws2.write_number(i, 3, c, num)
        ws2.write_formula(i, 4, "=C%d+D%d" % (i + 1, i + 1), num, a + c)
    ta = sum(r["A"][o]["arrest"] for o in calc.OFFICES)
    tc = sum(r["A"][o]["conditions"] for o in calc.OFFICES)
    ws2.write(8, 0, "All offices", bold)
    ws2.write_formula(8, 2, "=SUM(C5:C8)", boldnum, ta)
    ws2.write_formula(8, 3, "=SUM(D5:D8)", boldnum, tc)
    ws2.write_formula(8, 4, "=SUM(E5:E8)", boldnum, ta + tc)
    ws2.set_column(0, 1, 15)
    ws2.set_column(2, 4, 18)

    ws3 = wb.add_worksheet("Detainer days 2025")
    ws3.write(0, 0, "Days parolees were held on Board detainers in each district's county jails, 2025", title)
    ws3.write(1, 0, "Counting the day a detainer was lodged and not the day the person left. A legacy detainer with no "
                    "lift date ended when the person was admitted to the Department.", sub)
    ws3.write_row(3, 0, ["Parole district", "Jan-Mar 2025", "Apr-Jun 2025", "Jul-Sep 2025", "Oct-Dec 2025", "Year"], hf)
    for i, d in enumerate(C.DISTRICTS, start=4):
        ws3.write(i, 0, d)
        for j, (q, _, _) in enumerate(calc.QUARTERS, start=1):
            ws3.write_number(i, j, r["B"][d][q], num)
        ws3.write_formula(i, 5, "=SUM(B%d:E%d)" % (i + 1, i + 1), num, sum(r["B"][d].values()))
    ws3.set_column(0, 0, 15)
    ws3.set_column(1, 5, 13)
    wb.close()
    PP.stamp_ooxml(path, "Research and Projections Unit", "Research and Projections Unit", "2026-10-16T18:05:00Z",
                   "2026-10-16T18:05:00Z")


def write_chart(path, r):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "Liberation Sans", "font.size": 9,
                         "axes.spines.top": False, "axes.spines.right": False})
    qs = [q for q, _, _ in calc.QUARTERS]
    labels = ("January to March", "April to June", "July to September", "October to December")
    shades = ("#184f95", "#2a78d6", "#6da7ec", "#b7d3f6")
    x = np.arange(4)
    fig, ax = plt.subplots(figsize=(7.2, 4.3), dpi=150)
    base = np.zeros(4)
    for q, lab, col in zip(qs, labels, shades):
        v = np.array([r["B"][d][q] for d in C.DISTRICTS])
        ax.bar(x, v, width=0.58, bottom=base, color=col, label=lab, edgecolor="white", linewidth=1)
        base += v
    for i in range(4):
        ax.text(x[i], base[i] * 1.01 + 300, "{:,}".format(int(base[i])), ha="center", va="bottom", fontsize=9, color="#222222")
    ax.set_xticks(x, list(C.DISTRICTS))
    ax.set_ylabel("Detainer days in the district's county jails")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: "{:,}".format(int(v))))
    ax.set_ylim(0, base.max() * 1.15)
    ax.grid(axis="y", color="#e3e3e3", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="upper right", title="Quarter of 2025", fontsize=8, title_fontsize=8)
    ax.set_title("Board detainer days in 2025: Garrison's jails held the most", loc="left", fontsize=10.5,
                 fontweight="bold")
    fig.text(0.01, 0.01, "Board of Parole case systems and Department admissions. Counts the day a detainer was lodged, not "
             "the day the person left.", fontsize=7.5, color="#666666")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path, dpi=150, metadata={"Software": None})
    plt.close(fig)


def submission(r, f):
    s = r["s"]
    rate = f["call"]["rate_step"]
    lines = ["## Tags", "",
             "**Domain:** Criminology & Justice (recidivism and risk assessment).",
             "**Analytical objective:** Forecasting & Predictive Modeling.", "",
             "## 1. Final Recommendation", "",
             "**Carry a two-year return rate of %d per cent for the %s people the Department expects to release to parole "
             "in 2027, highest in %s and lowest in %s.** Under Act 26-114 the Board recommits no one, so every "
             "parolee's arrest goes to court and comes back as a new commitment at the courts' own rate. Not the record's "
             "new-commitment returns, which count only the arrests the Board left to the courts. Not the record's return "
             "rate of every kind, which counts recommitments the Act ends." % (rate, "{:,}".format(r["n"]), r["high"], r["low"]),
             "", "## 2. Critical Components", "",
             "1. The 2027 cohort is **%s** people on the projected-release extract." % "{:,}".format(r["n"]),
             "2. The two-year return rate under the Act is **%d per cent**." % rate,
             "3. The district with the highest rate is **%s** and the lowest **%s**." % (r["high"], r["low"]),
             "", "## 3. Step-by-Step Solution", "",
             "1. Read release movements PAR and RPR (PAROLE and REPAROLE before the 2022 upgrade) dated 1 January 2019 "
             "to 30 September 2024 in %s, each followed 730 days: %s releases." % (C.F_REL, "{:,}".format(len(r["S"]))),
             "2. Linked %s to Department numbers through %s and counted, for each release, arrests and days out of "
             "Department custody (ADM to the next release movement in %s) in four bands of time since release; fitted "
             "a Poisson model of arrests per day on age, prior commitments, offence, sex and district."
             % (C.F_ARR, C.F_XW, C.F_ADM),
             "3. Took from %s each court-decided arrest's chance of a DOC sentence by grade class (felony A-B, felony C-E, "
             "misdemeanour), arrests to 30 June 2024, leaving out the arrests the Board revoked on in its two case "
             "files, and the arrest-to-ADM time of those sentenced." % C.F_AOC,
             "4. For each person in %s, combined the arrest rate by time since release with that class mix, conversion "
             "and timing over 730 days; the cohort's rate is %d per cent, %s highest and %s lowest."
             % (C.F_PROJ, rate, r["high"], r["low"]),
             "5. Counted REVOKE and REVOKED decisions dated 1 July 2025 to 30 June 2026 by office, removing rescinded ones "
             "and the legacy entries dated after the legacy system closed on 2 January 2026, which repeat carried-over "
             "cases the new system decided; a decision citing an arrest number is on a reported arrest.",
             "6. Took each detainer once (one per legacy case, whose action rows repeat it, and a carried-over case from "
             "the new system), ended a legacy detainer with no lift date at the person's next ADM in %s, and counted "
             "days from the lodge day to the day before the end in each quarter, by the district of the county jail."
             % C.F_ADM,
             "7. Drew each district's 2025 detainer days from step 6 as a bar stacked by quarter in %s, labelled with its total." % PNG,
             "8. Carried %d per cent in the projection, %s highest and %s lowest." % (rate, r["high"], r["low"]),
             "", "## 4. Deliverable Answers", "", "### %s" % WB, "",
             "1. Two-year return rate of the 2027 parole releases under Act 26-114: %d per cent; highest district %s, "
             "lowest district %s." % (rate, r["high"], r["low"]),
             "2. Revocations the Board ordered from 1 July 2025 to 30 June 2026 and did not rescind:"]
    for o, d in zip(calc.OFFICES, C.DISTRICTS):
        lines.append("   - %s (%s): %s on a reported arrest, %s on conditions alone"
                     % (o, d, "{:,}".format(f["a1_" + o]["arrest"]), "{:,}".format(f["a1_" + o]["conditions"])))
    lines.append("3. Days parolees were held on Board detainers in each district's county jails, 2025:")
    for d in C.DISTRICTS:
        q = f["b_" + d]
        lines.append("   - %s: January to March %s, April to June %s, July to September %s, October to December %s"
                     % (d, "{:,}".format(q["Q1"]), "{:,}".format(q["Q2"]), "{:,}".format(q["Q3"]), "{:,}".format(q["Q4"])))
    lines += ["", "### %s" % PNG, "",
              "1. One bar per parole district, stacked by quarter of 2025, labelled with its year's detainer days: "
              + ", ".join("%s %s" % (d, "{:,}".format(v)) for d, v in f["chart"].items()) + "."]
    return "\n".join(lines) + "\n"


def main(target, golden, figpath, subpath):
    r = compute(target)
    f = figures(r)
    os.makedirs(golden, exist_ok=True)
    write_workbook(os.path.join(golden, WB), r)
    write_chart(os.path.join(golden, PNG), r)
    with open(figpath, "w") as fh:
        json.dump(f, fh, indent=1)
        fh.write("\n")
    with open(subpath, "w") as fh:
        fh.write(submission(r, f))
    return r, f
