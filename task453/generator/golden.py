"""The golden deliverables, computed from the shipped files only: rapid_response_certification_2027q1.pdf (the chief
statistician's certificate to the Minister: the designated regions, each region's seasonally adjusted payroll jobs for
the quarter against its 2026 average, a chart, how the series were built) and regional_payroll_jobs_2027q1.csv (each
region's employers with payroll jobs in March 2027 and the jobs its workplaces lost from March 2026), with
figures.json, every figure the write-up states."""
import csv
import io
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import calc as C        # noqa: E402
import world as W       # noqa: E402

PDF = "rapid_response_certification_2027q1.pdf"
CSV = "regional_payroll_jobs_2027q1.csv"
COMPONENTS = ("E01", "E03", "E09", "E08", "E10")      # the regions every valid route must place


def k10(v):
    return int(round(v / 10.0)) * 10


def floor1(v):
    return math.floor(v * 10 + 1e-9) / 10.0


def ceil1(v):
    return math.ceil(v * 10 - 1e-9) / 10.0


def compute(target):
    s = C.series(target)
    df = C.routes(s)
    X = dict(series=s, routes=df)
    X["call"] = C.designated(df, C.GOLD)
    X["default"] = C.designated(df, C.DEFAULT)
    X["robust"] = C.designated(df, "stl_robust")
    X["rows"] = {}
    for code in W.RCODE:
        sa, avg = C.sa_level(s, code)
        fam = df.loc[code, list(C.FAMILY)]
        lo, hi = float(fam.min()), float(fam.max())
        X["rows"][code] = dict(
            sa=sa, avg=avg, pct=float(df.loc[code, C.GOLD]), lo=lo, hi=hi,
            lo1=floor1(lo), hi1=ceil1(hi),
            sa_lo=math.floor(avg * (1 + lo / 100.0) / 10.0) * 10, sa_hi=math.ceil(avg * (1 + hi / 100.0) / 10.0) * 10,
            default=float(df.loc[code, C.DEFAULT]), classical=float(df.loc[code, "classical"]),
            shift=float(df.loc[code, "level_shift"]), designated=code in X["call"])
    wp = C.workplaces(target)
    X["lost"] = C.jobs_lost(wp, "workplace")
    X["employers"] = C.employers(wp, "business")
    return X


def fmt_pct(v):
    return ("%.1f" % v).replace("-", "−")


def chart_png(X):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["font.family"] = "DejaVu Sans"
    order = sorted(W.RCODE, key=lambda c: X["rows"][c]["pct"])
    vals = [X["rows"][c]["pct"] for c in order]
    names = [W.RNAME[c] for c in order]
    cols = ["#1f3b5c" if X["rows"][c]["designated"] else "#9fb3c8" for c in order]
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=150)
    ax.barh(range(len(order)), vals, color=cols, height=0.62)
    ax.axvline(-1.0, color="#b03a2e", lw=1.2, ls="--")
    ax.text(-1.0, -0.95, " designation line, −1.0%", color="#b03a2e", fontsize=7.5, va="center")
    ax.set_ylim(-1.35, len(order) - 0.4)
    ax.axvline(0, color="#333333", lw=0.6)
    for k, v in enumerate(vals):
        ax.text(v + (0.06 if v >= 0 else -0.06), k, fmt_pct(v), va="center", ha="left" if v >= 0 else "right", fontsize=7.5)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels(names, fontsize=8)
    ax.set_xlabel("Seasonally adjusted payroll jobs, Q1 2027, against the 2026 average (per cent)", fontsize=8)
    ax.set_xlim(min(vals) - 0.8, max(vals) + 0.8)
    ax.tick_params(axis="x", labelsize=7.5)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.set_title("Three regions sit more than 1.0 per cent below their 2026 payroll jobs", fontsize=9.5, loc="left")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def write_pdf(X, path):
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    FD = "/usr/share/fonts/truetype/liberation/"
    for nm, f in (("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
        pdfmetrics.registerFont(TTFont(nm, FD + nm.split("-")[0] + "-" + f + ".ttf"))
    pdfmetrics.registerFontFamily("LiberationSans", normal="LiberationSans", bold="LiberationSans-Bold",
                                  italic="LiberationSans-Italic", boldItalic="LiberationSans-Bold")
    INK, GREY = colors.HexColor("#1b1d20"), colors.HexColor("#5b6068")
    B = ParagraphStyle("b", fontName="LiberationSans", fontSize=9.6, leading=13.4, textColor=INK, spaceAfter=6)
    H = ParagraphStyle("h", fontName="LiberationSans-Bold", fontSize=12.5, leading=16, textColor=INK, spaceAfter=4)
    H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10, leading=13, textColor=INK, spaceBefore=6, spaceAfter=3)
    SM = ParagraphStyle("sm", fontName="LiberationSans", fontSize=7.8, leading=10, textColor=GREY, spaceAfter=3)
    CE = ParagraphStyle("ce", fontName="LiberationSans", fontSize=8.4, leading=10.5, textColor=INK)
    CR = ParagraphStyle("cr", parent=CE, alignment=2)
    CB = ParagraphStyle("cb", parent=CE, fontName="LiberationSans-Bold")
    CBR = ParagraphStyle("cbr", parent=CB, alignment=2)
    minister, mt = W.PEOPLE["minister"]
    chief, ct = W.PEOPLE["chief"]
    mgr, mgt = W.PEOPLE["manager"]
    rows = X["rows"]
    des = [c for c in W.RCODE if rows[c]["designated"]]
    running = ["the Capital" if c == "E01" else W.RNAME[c] for c in sorted(des, key=lambda c: W.RNAME[c].replace("Capital", "Capital"))]
    names_s = ", ".join(running[:-1]) + " and " + running[-1] if len(running) > 1 else running[0]

    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans", 7.2)
        canvas.setFillColor(GREY)
        canvas.drawString(0.9 * inch, 0.55 * inch, "%s  |  Certification RRP-2027-Q1  |  13 May 2027" % W.BUREAU)
        canvas.drawRightString(LETTER[0] - 0.9 * inch, 0.55 * inch, "Page %d of 2" % doc.page)
        canvas.restoreState()

    doc = SimpleDocTemplate(path, pagesize=LETTER, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.75 * inch,
                            bottomMargin=0.85 * inch, title="Regional Rapid Response Program: certification for the first quarter of 2027",
                            author=W.BUREAU, subject="", creator="", producer="")
    s = [Paragraph(W.BUREAU.upper(), SM),
         Paragraph("%s designated for the first quarter of 2027" % (names_s[0].upper() + names_s[1:]), H),
         Paragraph("To: %s, %s<br/>From: %s, %s<br/>Date: 13 May 2027<br/>Re: Certification under section 3 of the %s, first quarter of 2027"
                   % (minister, mt, chief, ct, W.REGULATION), B),
         Spacer(1, 4),
         Paragraph("I certify that %s are designated for the first quarter of 2027 under section 2 of the Regulation. "
                   "Each one's seasonally adjusted payroll jobs for January to March 2027 are more than 1.0 per cent "
                   "below its payroll jobs for 2026; no other region's are. The figures below are those section 3(3) "
                   "requires." % names_s, B)]
    head = [Paragraph(t, CB if k == 0 else CBR) for k, t in enumerate(
        ("Economic region", "Seasonally adjusted payroll jobs, Q1 2027", "Payroll jobs, 2026", "Per cent"))]
    data = [head]
    for c in des:
        r = rows[c]
        data.append([Paragraph(W.RNAME[c], CE), Paragraph("{:,}".format(k10(r["sa"])), CR),
                     Paragraph("{:,}".format(k10(r["avg"])), CR), Paragraph(fmt_pct(r["pct"]), CR)])
    t = Table(data, colWidths=[2.0 * inch, 1.75 * inch, 1.35 * inch, 0.9 * inch], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, INK), ("LINEBELOW", (0, -1), (-1, -1), 0.4, GREY),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    s.append(t)
    s.append(Paragraph("Jobs rounded to the nearest 10; the test compares unrounded figures (section 2(2)).", SM))
    s.append(Spacer(1, 6))
    s.append(Image(io.BytesIO(chart_png(X)), width=6.1 * inch, height=3.43 * inch))
    s.append(Paragraph("Figure 1. Every region's seasonally adjusted payroll jobs for the first quarter of 2027 against "
                       "its 2026 average; designated regions dark.", SM))
    s.append(Paragraph("How the series were built", H2))
    s.append(Paragraph(
        "Payroll jobs are the jobs on employers' monthly returns to the %s: its yearly tables for 2021 to 2023 and its "
        "monthly statistics from January 2024, with January to March 2027 as revised on 7 May 2027, placed in the "
        "economic regions through the bureau's municipal concordance (Wexleigh and Dorran, amalgamated as "
        "Wexleigh-Dorran in 2025, are in Quillon Plain under both codes)." % W.AGENCY, B))
    s.append(Paragraph(
        "From the January 2026 reference month the Agency places jobs at the workplace; before, every job of an employer "
        "sat at the municipality of its account address, and the earlier months were not revised. The change moved "
        "jobs out of the Capital (%s per cent at January 2026) and Saltmere Coast and into the regions where employers "
        "based there have mines, mills, plants, hospitals and stores, most of all Kestrow North (+%s per cent) and "
        "Varrenby Shore (+%s per cent). The quarter and 2026 are both on the new placement, but the seasonal pattern "
        "comes from the whole history, so each region's pattern was estimated with the change removed as a level shift: "
        "a regression of the logarithm of its monthly payroll jobs on month effects, a trend whose slope changes each "
        "January, and a level shift from January 2026. The seasonally adjusted figures remove the month effects. "
        "Estimated across the change instead, the pattern takes up part of it, and the first quarter's factors carry "
        "the January 2026 step into 2027." % (fmt_pct(rows["E01"]["shift"]).replace("−", "−"),
                                                 "%.1f" % rows["E08"]["shift"], "%.1f" % rows["E10"]["shift"]), B))
    s.append(Paragraph("Every region's result", H2))
    head = [Paragraph(t, CB if k == 0 else CBR) for k, t in enumerate(
        ("Economic region", "SA payroll jobs, Q1 2027", "Payroll jobs, 2026", "Per cent", "Designated"))]
    data = [head]
    for c in W.RCODE:
        r = rows[c]
        data.append([Paragraph(W.RNAME[c], CE), Paragraph("{:,}".format(k10(r["sa"])), CR),
                     Paragraph("{:,}".format(k10(r["avg"])), CR), Paragraph(fmt_pct(r["pct"]), CR),
                     Paragraph("Yes" if r["designated"] else "No", CR)])
    t = Table(data, colWidths=[1.8 * inch, 1.5 * inch, 1.3 * inch, 0.8 * inch, 0.9 * inch], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, INK), ("LINEBELOW", (0, -1), (-1, -1), 0.4, GREY),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 1.5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]))
    s.append(t)
    s.append(Paragraph("SA: seasonally adjusted. Source: %s employer return statistics; bureau seasonal adjustment." % W.AGENCY, SM))
    s.append(Spacer(1, 8))
    s.append(Paragraph("%s<br/>%s<br/>Prepared by %s, %s" % (chief, ct, mgr, mgt), B))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


def write_csv(X, path):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(("economic_region_code", "economic_region", "employers_with_payroll_jobs_2027_03",
                "jobs_lost_workplaces_none_left_2027_03", "jobs_lost_workplaces_kept_some_2027_03"))
    for c in W.RCODE:
        w.writerow((c, W.RNAME[c], int(X["employers"][c]), k10(X["lost"].loc[c, "none"]), k10(X["lost"].loc[c, "fewer"])))
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())


def figures(X):
    rows = X["rows"]
    df = X["routes"]
    fam = list(C.FAMILY)
    F = {"call": [W.RNAME[c] for c in X["call"]], "default_call": [W.RNAME[c] for c in X["default"]],
         "robust_call": [W.RNAME[c] for c in X["robust"]], "line_per_cent": 1.0, "stl_seasonal_windows": [7, 13],
         "designated_min_gap": round(min(abs(float(df.loc[c, r]) + 1) for c in X["call"] for r in fam), 2),
         "others_min_gap": round(min(abs(float(df.loc[c, r]) + 1) for c in W.RCODE if c not in X["call"] for r in fam), 2),
         "regions": {}}
    for c in W.RCODE:
        r = rows[c]
        F["regions"][W.RNAME[c]] = {
            "pct": round(r["pct"], 1), "pct_below": round(-r["pct"], 1), "pct_range": [r["lo1"], r["hi1"]],
            "pct_range_below": [round(-r["hi1"], 1), round(-r["lo1"], 1)],
            "sa_jobs": k10(r["sa"]), "sa_jobs_range": [r["sa_lo"], r["sa_hi"]], "avg_2026": k10(r["avg"]),
            "default_pct": round(r["default"], 1), "default_pct_below": round(-r["default"], 1),
            "classical_pct": round(r["classical"], 1),
            "level_shift_pct": round(r["shift"], 1), "level_shift_abs": round(abs(r["shift"]), 1),
            "designated": r["designated"], "employers_2027_03": int(X["employers"][c]),
            "jobs_lost_none": k10(X["lost"].loc[c, "none"]), "jobs_lost_fewer": k10(X["lost"].loc[c, "fewer"])}
    return F


def main(target, out_dir, fig_path):
    os.makedirs(out_dir, exist_ok=True)
    X = compute(target)
    write_pdf(X, os.path.join(out_dir, PDF))
    import postprocess as PP
    PP.normalize_pdf(os.path.join(out_dir, PDF), b"D:20270513101500-04'00'", b"D:20270513112230-04'00'")
    write_csv(X, os.path.join(out_dir, CSV))
    F = figures(X)
    with open(fig_path, "w") as fh:
        json.dump(F, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    for f in (PDF, CSV):
        os.utime(os.path.join(out_dir, f), (1778685300, 1778685300))
    return X


if __name__ == "__main__":
    T = os.path.dirname(HERE)
    main(os.path.join(T, "target"), os.path.join(T, "golden"), os.path.join(HERE, "figures.json"))
