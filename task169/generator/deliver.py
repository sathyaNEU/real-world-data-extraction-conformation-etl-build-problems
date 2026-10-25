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
    W = calc.ask_c(D)
    ev = calc.conversion_evidence(D)
    bd = calc.board_devices(D)
    return dict(D=D, S=S, g=g, s=s, n=len(proj), dist_n=dist_n, high=order[-1], low=order[0], A=A, B=B, W=W, ev=ev,
                bd=bd)


def figures(r):
    f = {"call": {"rate_step": calc.step5(r["s"]["all"])},
         "cohort_size": r["n"], "spells": len(r["S"]), "window_days": C.WINDOW,
         "_unrounded": {"rate_pct": round(100 * r["s"]["all"], 1)}}
    ev = r["ev"]
    f["conv_revoked_arrests"] = {"arrests": ev["revoked"], "nolle_prosequi": ev["revoked_np"]}
    f["conv_courts"] = {"arrests": ev["others"], "nolle_prosequi": ev["others_np"], "doc": ev["others_doc"],
                        "felony_ab": ev["others_by"]["F1"], "felony_ce": ev["others_by"]["F2"],
                        "misdemeanour": ev["others_by"]["M"]}
    f["conv_after_max_date"] = {"arrests": ev["off"], "doc": ev["off_doc"], "felony_ab": ev["off_by"]["F1"],
                                "felony_ce": ev["off_by"]["F2"], "misdemeanour": ev["off_by"]["M"]}
    f["conv_every_arrest"] = {"arrests": ev["every"], "doc": ev["every_doc"]}
    bd = r["bd"]
    f["board_records"] = {"reheard_cases": bd["rehear"], "reissued_detainers": bd["reissued"]}
    for o, d in zip(calc.OFFICES, C.DISTRICTS):
        f["a1_" + o] = {"arrest": r["A"][o]["arrest"], "conditions": r["A"][o]["conditions"]}
    for d in C.DISTRICTS:
        f["b_" + d] = dict(r["B"][d])
    for i in calc.INSTITUTIONS:
        f["c_" + i] = dict(r["W"][i])
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
             "to parole, by time since release, age, prior commitments, offence, sex and district, carried over all 730 "
             "days, the cohort being out of Department custody until a return (methodology 4.1).",
             "Each arrest's chance of a Department sentence and the time from arrest to admission are the courts' own, "
             "by charge grade (felony A-B, felony C-E, misdemeanour), from arrests to 30 June 2024 that went to court; "
             "arrests the Board answered by revoking parole are left out because no court decided them.",
             "The rate is carried in steps of five percentage points (methodology 3.3); the district rates are the "
             "model's own, shown for the projection's district tables."]
    for i, t in enumerate(notes, start=14):
        ws.write(i, 0, t)
    ws.set_column(0, 0, 30)
    ws.set_column(1, 1, 8)
    ws.set_column(2, 4, 16)

    ws2 = wb.add_worksheet("Board revocations FY26")
    ws2.write(0, 0, "Recommitments the Board ordered, 1 July 2025 to 30 June 2026, not rescinded by 30 June 2026", title)
    ws2.write(1, 0, "One recommitment per parolee per hearing: two reports taken up at one hearing are one order, and a "
                    "case heard again after a rescission keeps its later order. Legacy system to 2 January 2026, new case "
                    "system from 5 January.", sub)
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
    ws3.write(0, 0, "Parolee-days held on Board detainers in each district's county jails, 2025", title)
    ws3.write(1, 0, "A parolee held on two detainers at once is held once. Counting the day a detainer was lodged and not "
                    "the day the person left; a legacy detainer with no lift date ended at the person's admission; a "
                    "carried-over detainer counted from its legacy lodge date, not the 5 January 2026 re-issue.", sub)
    ws3.write_row(3, 0, ["Parole district", "January to June", "July to December", "Year"], hf)
    for i, d in enumerate(C.DISTRICTS, start=4):
        ws3.write(i, 0, d)
        for j, (h, _, _) in enumerate(calc.HALVES, start=1):
            ws3.write_number(i, j, r["B"][d][h], num)
        ws3.write_formula(i, 3, "=SUM(B%d:C%d)" % (i + 1, i + 1), num, sum(r["B"][d].values()))
    ws3.set_column(0, 0, 15)
    ws3.set_column(1, 3, 16)

    ws4 = wb.add_worksheet("Writ days 2025")
    ws4.write(0, 0, "Days people spent out of each institution on court writs, 2025", title)
    ws4.write(1, 0, "Counting the day a person went out and not the day the trip ended. A trip ends at the return (WRI) "
                    "or, for a person the court released, at the release.", sub)
    ws4.write_row(3, 0, ["Institution", "January to June", "July to December", "Year"], hf)
    for i, inst in enumerate(calc.INSTITUTIONS, start=4):
        ws4.write(i, 0, inst)
        for j, (h, _, _) in enumerate(calc.HALVES, start=1):
            ws4.write_number(i, j, r["W"][inst][h], num)
        ws4.write_formula(i, 3, "=SUM(B%d:C%d)" % (i + 1, i + 1), num, sum(r["W"][inst].values()))
    ws4.set_column(0, 0, 15)
    ws4.set_column(1, 3, 16)
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
    rate = f["call"]["rate_step"]
    ev = r["ev"]
    bd = r["bd"]
    ob, fb = ev["others_by"], ev["off_by"]
    c = lambda v: "{:,}".format(v)
    lines = ["## Tags", "",
             "**Domain:** Criminology & Justice (recidivism and risk assessment).",
             "**Analytical objective:** Forecasting & Predictive Modeling.", "",
             "## 1. Final Recommendation", "",
             "**Carry a two-year return rate of %d per cent for the %s people the Department expects to release to parole "
             "in 2027.** Under Act 26-114 the Board recommits no one, so every parolee's arrest goes to court and comes "
             "back as a new commitment at the courts' own rate. Not the record's new-commitment returns, which count only "
             "the arrests the Board left to the courts. Not the record's return rate of every kind, which counts "
             "recommitments the Act ends." % (rate, "{:,}".format(r["n"])),
             "", "## 2. Critical Components", "",
             "1. The 2027 cohort is **%s** people on the projected-release extract." % "{:,}".format(r["n"]),
             "2. The two-year return rate under the Act is **%d per cent**." % rate,
             "", "## 3. Step-by-Step Solution", "",
             "1. Read release movements PAR and RPR (PAROLE and REPAROLE before the 2022 upgrade) dated 1 January 2019 "
             "to 30 September 2024 in %s, each followed %d days: %s releases." % (C.F_REL, C.WINDOW, "{:,}".format(len(r["S"]))),
             "2. Linked %s to Department numbers through %s and counted, for each release, every arrest (the ones the "
             "Board revoked on included) and the days out of Department custody (ADM to the next release movement in %s) "
             "in four bands of time since release; fitted a Poisson model of arrests per day on age, prior commitments, "
             "offence, sex and district." % (C.F_ARR, C.F_XW, C.F_ADM),
             "3. Matched every arrest linked to a Department number and dated on or before 30 June 2024 (%s, arrests on "
             "a release day included) to its case in %s on otn (a docket's latest entry): the %s the "
             "Board revoked on (an arrest_otn on a REVOKE or REVOKED decision in its two case files) were all nolle "
             "prossed (%s of %s, against %s of the %s others), so their record outcome is the Board's, not a court's; of "
             "the %s, %s ended in a DOC sentence (sentence_type DOC; CJ and PROB are not returns), by the arrest's top "
             "charge grade felony A-B %s of %s, felony C-E %s of %s, misdemeanour %s of %s, with the arrest-to-ADM time of "
             "those sentenced." % (c(ev["every"]), C.F_AOC, c(ev["revoked"]), c(ev["revoked_np"]), c(ev["revoked"]), c(ev["others_np"]),
                                   c(ev["others"]), c(ev["others"]), c(ev["others_doc"]), c(ob["F1"][0]), c(ob["F1"][1]),
                                   c(ob["F2"][0]), c(ob["F2"][1]), c(ob["M"][0]), c(ob["M"][1])),
             "4. Checked that rate where the Board could not revoke: of the %s arrests made on or after the maximum "
             "expiration date of the parole release before them, %s ended in a DOC sentence (felony A-B %s of %s, felony "
             "C-E %s of %s, misdemeanour %s of %s), the same rates; every arrest with the revoked ones in gives %s of %s, "
             "which counts the Board's revocations as court outcomes." % (c(ev["off"]), c(ev["off_doc"]), c(fb["F1"][0]),
                                                                          c(fb["F1"][1]), c(fb["F2"][0]), c(fb["F2"][1]),
                                                                          c(fb["M"][0]), c(fb["M"][1]),
                                                                          c(ev["every_doc"]), c(ev["every"])),
             "5. For each person in %s, out of Department custody from release until a return (section 4 of %s), sent "
             "every arrest the model expects in the %d days through those courts' rates for the grade mix of the "
             "person's governing offence, each timed by the arrest-to-ADM time, and took the share with a return (1 "
             "minus e to the minus the expected returns): %.1f per cent, %d per cent to the step."
             % (C.F_PROJ, C.F_METH, C.WINDOW, f["_unrounded"]["rate_pct"], rate),
             "6. Took REVOKE and REVOKED decisions dated 1 July 2025 to 30 June 2026 and counted one recommitment per "
             "parolee per hearing date (two cases decided together are one order), on a reported arrest when any of its "
             "cases cites an arrest number; the legacy entries dated after the legacy system closed on 2 January 2026 "
             "are the parallel run's copies of decisions the new system holds; a rescission dated by 30 June 2026 sets "
             "aside the order standing on its case when it came, so the %s legacy cases heard again after a rescission "
             "(REVOKE, RESCIND, REVOKE, the parolee held throughout) keep their later order." % bd["rehear"],
             "7. Took each detainer once (one per legacy case and lodge date; a carried-over case's detainer from its "
             "lodge day in the legacy table, the new system having re-issued the detainers of the %s cases still "
             "undecided at its go-live as lodged on 5 January 2026, to its end in the new system), ended a legacy "
             "detainer with no lift date at the person's next ADM in %s, merged each parolee's overlapping detainers, "
             "and counted days from the lodge day to the day before the end in each half of 2025 by the district of the "
             "county jail." % (bd["reissued"], C.F_ADM),
             "8. Ended each writ trip (a WRO in %s; no person has two open at once) at the person's next WRI or, where "
             "a release movement in %s comes first, at the release, and counted days from the day out to the day before "
             "the trip ended in each half of 2025 by the WRO's institution." % (C.F_ADM, C.F_REL),
             "", "## 4. Deliverable Answers", "", "### %s" % WB, "",
             "1. Two-year return rate of the 2027 parole releases under Act 26-114: %d per cent." % rate,
             "2. Recommitments the Board ordered from 1 July 2025 to 30 June 2026 and had not rescinded by 30 June 2026:"]
    for o, d in zip(calc.OFFICES, C.DISTRICTS):
        lines.append("   - %s (%s): %s that took up a reported arrest, %s on conditions alone"
                     % (o, d, "{:,}".format(f["a1_" + o]["arrest"]), "{:,}".format(f["a1_" + o]["conditions"])))
    lines.append("3. Parolee-days held on Board detainers in each district's county jails, 2025:")
    for d in C.DISTRICTS:
        q = f["b_" + d]
        lines.append("   - %s: January to June %s, July to December %s" % (d, "{:,}".format(q["H1"]), "{:,}".format(q["H2"])))
    lines.append("4. Days people spent out on court writs, by the institution they left, 2025:")
    for i in calc.INSTITUTIONS:
        q = f["c_" + i]
        lines.append("   - %s: January to June %s, July to December %s" % (i, "{:,}".format(q["H1"]), "{:,}".format(q["H2"])))
    return "\n".join(lines) + "\n"


def main(target, golden, figpath, subpath):
    r = compute(target)
    f = figures(r)
    os.makedirs(golden, exist_ok=True)
    write_workbook(os.path.join(golden, WB), r)
    with open(figpath, "w") as fh:
        json.dump(f, fh, indent=1)
        fh.write("\n")
    with open(subpath, "w") as fh:
        fh.write(submission(r, f))
    return r, f
