"""The golden deliverables, computed from target/ through analysis.py: the recertification list (CSV) and the
screening-year review (PDF) with the detection chart, the currency counts and the lane throughput."""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import analysis as A  # noqa: E402
import io_util as IO  # noqa: E402
import params as P  # noqa: E402

CSV = "recertification_2027.csv"
PDF = "screening_year_review_2026.pdf"
MONTH_NAME = {12: "December", 1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July",
              8: "August", 9: "September", 10: "October", 11: "November"}


def results(target):
    T = A.load(target)
    M = A.main_call(T)
    asks_a, _hrs = A.ask_a(T)
    asks_b = A.ask_b(T)
    pop_a = A.whole_month_population(T)
    return T, M, asks_a, asks_b, pop_a


def chart(tab, off, path):
    t = tab.sort_values("golden").reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(10.2, 4.6), dpi=110)
    x = range(len(t))
    ax.scatter(x, t["overall"] * 100, s=16, facecolors="none", edgecolors="#8a96a0", linewidths=0.9,
               label="Hit rate, every projection in the year")
    col = ["#b8402f" if s in off else "#2f5d7c" for s in t["staff_no"]]
    ax.scatter(x, t["golden"] * 100, s=22, c=col, label="Detection performance (objects new to the officer)")
    ax.axhline(80, color="#333333", lw=1.0, ls="--")
    ax.text(len(t) - 0.5, 80.6, "80 per cent standard", ha="right", va="bottom", fontsize=8.5, color="#333333")
    ax.set_xticks([])
    ax.set_xlabel("Endorsed officers, ordered by detection performance (red: off X-ray duty from 1 January 2027)",
                  fontsize=8.8)
    ax.set_ylabel("Per cent", fontsize=9)
    ax.set_ylim(50, 101)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="lower right", fontsize=8.2, frameon=False)
    n_off = len(off)
    n_mask = int(((t["golden"] < P.STANDARD) & (t["overall"] >= P.STANDARD)).sum())
    words = {6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 5: "five", 4: "four"}
    ax.set_title("%s officers detect fewer than 80 per cent of threat items new to them; %s of them clear 80 per "
                 "cent on the raw hit rate" % (words.get(n_off, str(n_off)).capitalize(), words.get(n_mask, str(n_mask))),
                 fontsize=9.6, loc="left")
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def write_all(target, golden, gen):
    os.makedirs(golden, exist_ok=True)
    os.makedirs(gen, exist_ok=True)
    T, M, asks_a, asks_b, pop_a = results(target)
    tab = M["table"].copy()
    off = set(M["golden"])
    # ------------------------------------------------------------------ recertification list
    rows = []
    for r in tab.sort_values(["surname", "given"]).itertuples():
        rows.append((r.staff_no, r.surname, r.given, r.employment, r.checkpoint, r.n_first, r.first_hits,
                     "%.1f" % (100 * r.golden), "Off X-ray duty: remedial training" if r.staff_no in off else "Continue"))
    IO.write_csv(os.path.join(golden, CSV), ["staff_no", "surname", "given_name", "employment", "home_checkpoint",
                                             "projections_of_new_objects", "detected", "detection_performance_pct",
                                             "xray_duty_from_1_jan_2027"], rows, newline="\n")
    # ------------------------------------------------------------------ chart and review
    png = os.path.join(gen, "detection_chart.png")
    chart(tab, off, png)
    st = {"t": ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=13, leading=16, spaceAfter=6),
          "p": ParagraphStyle("p", fontName="Helvetica", fontSize=9.2, leading=12.4, spaceAfter=5),
          "h": ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10, leading=13, spaceBefore=6, spaceAfter=3),
          "c": ParagraphStyle("c", fontName="Helvetica", fontSize=8.4, leading=10.4)}
    offt = tab[tab["staff_no"].isin(off)].sort_values("golden")
    names = "; ".join("%s %s (%s, %s, %.1f per cent)" % (r.given, r.surname, r.staff_no, r.employment.lower(),
                                                         100 * r.golden) for r in offt.itertuples())
    masked = offt[offt["overall"] >= P.STANDARD]
    story = [
        Paragraph("Screening year 2025-26: X-ray recertification, currency and lane throughput", st["t"]),
        Paragraph("Security Screening, training and standards. Prepared 3 December 2026 for the January 2027 "
                  "recertification under SCS-04 revision 6.", st["c"]),
        Paragraph("Recertification", st["h"]),
        Paragraph("<b>%d officers come off X-ray duty from 1 January 2027 for remedial training:</b> %s. Every other "
                  "officer holding an X-ray endorsement on 30 November 2026 is recertified." % (len(off), names), st["p"]),
        Paragraph("Detection performance is read on the projections of threat objects the officer had not been shown "
                  "before on the CT lanes. Projections of an object already shown and confirmed, in any of its three "
                  "orientations, were detected %.1f per cent of the time against %.1f per cent for objects new to the "
                  "officer, so the year's raw hit rate mostly measures recognition of the library for the officers "
                  "shown it most. %d of the %d officers coming off clear 80 per cent on the raw hit rate."
                  % (100 * M["pooled_hit_repeat"], 100 * M["pooled_hit_first"], len(masked), len(off)), st["p"]),
        Image(png, width=174 * mm, height=78.5 * mm),
        Paragraph("Currency: endorsed officers short of 20 hours of X-ray time", st["h"]),
    ]
    cur = [["Month", "Endorsed all month", "Short of 20 hours"]]
    for (y, m), v in zip(A.MONTHS, asks_a):
        cur.append(["%s %d" % (MONTH_NAME[m], y), str(len(pop_a[(y, m)])), str(v)])
    tstyle = TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.4), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.4),
                         ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#7d8b93")),
                         ("ALIGN", (1, 0), (-1, -1), "RIGHT"), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                         ("TOPPADDING", (0, 0), (-1, -1), 1.5)])
    t1 = Table(cur, colWidths=[38 * mm, 32 * mm, 32 * mm], hAlign="LEFT")
    t1.setStyle(tstyle)
    story += [t1, Spacer(1, 4),
              Paragraph("Passenger bags screened by lane and quarter, nearest thousand", st["h"])]
    thr = [["Lane", "Dec-Feb", "Mar-May", "Jun-Aug", "Sep-Nov"]]
    for ln in P.LANES:
        thr.append([ln] + ["{:,}".format(A.rnd_k(asks_b[(ln, q)])) for q, _, _ in A.QUARTERS])
    t2 = Table(thr, colWidths=[20 * mm] + [26 * mm] * 4, hAlign="LEFT")
    t2.setStyle(tstyle)
    story += [t2, Spacer(1, 4),
              Paragraph("Counts are from the CT units' hourly records, each unit placed on the lane it stood on that "
                        "day; images counted before a lane's first rostered start are performance tests and are left "
                        "out.", st["c"])]
    path = os.path.join(golden, PDF)
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=16 * mm, title="Screening year review 2025-26", author="Security Screening",
                            creator="Silverwattle Coast Airport", producer="Silverwattle Coast Airport", invariant=1)
    doc.build(story)
    data = open(path, "rb").read()
    for sig in (b"ReportLab Generated PDF document (opensource)", b"ReportLab generated PDF document -- digest (opensource)",
                b"ReportLab Generated PDF document http://www.reportlab.com"):
        data = data.replace(sig, b" " * len(sig))
    open(path, "wb").write(data)
    # ------------------------------------------------------------------ figures.json
    fig = {
        "call_off_count": len(off),
        "call_off": [dict(staff_no=r.staff_no, name="%s %s" % (r.given, r.surname), employment=r.employment,
                          detection_pct=round(100 * r.golden, 1), raw_hit_pct=round(100 * r.overall, 1))
                     for r in offt.itertuples()],
        "masked_count": len(masked),
        "endorsed_population": len(tab),
        "pooled_first_pct": round(100 * M["pooled_hit_first"], 1),
        "pooled_repeat_pct": round(100 * M["pooled_hit_repeat"], 1),
        "default_off": M["r0"], "default_off_count": len(M["r0"]),
        "ask_a": {"%d-%02d" % mk: v for mk, v in zip(A.MONTHS, asks_a)},
        "ask_a_population": {"%d-%02d" % mk: len(pop_a[mk]) for mk in A.MONTHS},
        "ask_b": {"%s %s" % (ln, q): A.rnd_k(asks_b[(ln, q)]) for ln in P.LANES for q, _, _ in A.QUARTERS},
        "ask_b_raw": {"%s %s" % (ln, q): int(asks_b[(ln, q)]) for ln in P.LANES for q, _, _ in A.QUARTERS},
        "standard_pct": 80, "currency_hours": 20,
        "designated_below_pct": 75, "others_at_least_pct": 83,
        "recertified_count": int(len(tab) - len(off)),
        "masked_ft_count": int(sum(1 for r in masked.itertuples() if r.employment == "Full-time")),
        "raw_off_count": len(M["r0"]),
        "pooled_first_raw": round(float(M["pooled_hit_first"]), 5),
        "pooled_repeat_raw": round(float(M["pooled_hit_repeat"]), 5),
    }
    with open(os.path.join(gen, "figures.json"), "w") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
    return fig
