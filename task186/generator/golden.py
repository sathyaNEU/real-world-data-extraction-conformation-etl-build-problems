"""The golden deliverables, computed from target/ through analysis.py: the recertification list (CSV) and the
screening-year review (PDF) with the detection chart, the currency counts and the lane throughput."""
import json
import math
import os
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.platypus import Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

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


WORDS = {3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven",
         12: "twelve"}
OFF_C, ON_C, RAW_C, INK_C = "#c4402f", "#2a78d6", "#9aa3aa", "#2b2b2b"


def word(n):
    return WORDS.get(n, str(n))


def evidence(T):
    """The rates that decide what is new to an officer, over every officer and over the endorsed alone."""
    tip = A.tip_events(T)
    win = tip[tip["in_window"]]
    fi = win[win["prior_img"] == 0]
    pop = set(A.population(T))
    pre = []
    for w in (win, win[win["staff_no"].isin(pop)]):
        pre.append(float(w.loc[(w["prior_obj"] > 0) & (w["prior_obj_win"] == 0), "hit"].mean()))
    return {"other_orientation": float(fi.loc[fi["prior_obj"] > 0, "hit"].mean()), "pre_window_min": min(pre)}


def chart(tab, off, path):
    t = tab.sort_values("golden").reset_index(drop=True)
    x = list(range(len(t)))
    is_off = [s in off for s in t["staff_no"]]
    fig, ax = plt.subplots(figsize=(10.2, 4.7), dpi=150)
    for xi, o, g, r in zip(x, is_off, t["golden"], t["overall"]):
        if o:
            ax.plot([xi, xi], [g * 100, r * 100], color="#c9ced2", lw=0.9, zorder=1)
    ax.scatter(x, t["overall"] * 100, s=18, facecolors="white", edgecolors=RAW_C, linewidths=0.9, zorder=2,
               label="Hit rate over every projection in the year")
    xo = [xi for xi, o in zip(x, is_off) if o]
    xc = [xi for xi, o in zip(x, is_off) if not o]
    ax.scatter(xc, [t["golden"][i] * 100 for i in xc], s=24, color=ON_C, edgecolors="white", linewidths=0.5,
               zorder=3, label="Detection performance, recertified")
    ax.scatter(xo, [t["golden"][i] * 100 for i in xo], s=30, color=OFF_C, edgecolors="white", linewidths=0.5,
               zorder=4, label="Detection performance, off X-ray duty from 1 January 2027")
    ax.axhline(80, color=INK_C, lw=0.9, ls=(0, (4, 3)), zorder=0)
    ax.text(len(t) - 0.5, 80.7, "SCS-04 standard, 80 per cent", ha="right", va="bottom", fontsize=8.3, color=INK_C)
    ax.text(max(xo) + 1.4, 63.5, "Off X-ray duty", fontsize=8.3, color=INK_C, ha="left", va="center")
    mid = xc[len(xc) // 3]
    ax.text(mid, t["golden"][mid] * 100 - 3.2, "Recertified", fontsize=8.3, color=INK_C, ha="left", va="top")
    ax.set_xticks([])
    ax.set_xlim(-1.5, len(t) + 0.5)
    ax.set_xlabel("Officers holding an X-ray endorsement on 30 November 2026, ordered by detection performance",
                  fontsize=8.6, color=INK_C)
    ax.set_ylabel("Per cent of threat images detected", fontsize=8.6, color=INK_C)
    ax.set_ylim(50, 101)
    ax.set_yticks(range(50, 101, 10))
    ax.tick_params(axis="y", labelsize=8.3, colors=INK_C)
    ax.grid(axis="y", color="#eceeef", lw=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#9aa3aa")
    ax.legend(loc="lower right", fontsize=8.0, frameon=False, handletextpad=0.4)
    n_mask = int(((t["golden"] < P.STANDARD) & (t["overall"] >= P.STANDARD)).sum())
    ax.set_title("%s officers detect fewer than 80 per cent of threat objects new to them; %s of them clear 80 per "
                 "cent on the raw hit rate" % (word(len(xo)).capitalize(), word(n_mask)), fontsize=9.6, loc="left",
                 color=INK_C)
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def write_all(target, golden, gen):
    os.makedirs(golden, exist_ok=True)
    os.makedirs(gen, exist_ok=True)
    T, M, asks_a, asks_b, pop_a = results(target)
    ev = evidence(T)
    tab = M["table"].copy()
    off = set(M["golden"])
    release = json.load(open(os.path.join(target, "tip_projection_settings.json")))["library_release"]
    # ------------------------------------------------------------------ recertification list
    rows = []
    for r in tab.sort_values(["surname", "given"]).itertuples():
        rows.append((r.staff_no, r.surname, r.given, r.employment, r.checkpoint, r.n_first, r.first_hits,
                     "%.1f" % (100 * r.golden),
                     "Off X-ray duty pending remedial training" if r.staff_no in off else "Recertified"))
    IO.write_csv(os.path.join(golden, CSV), ["staff_no", "surname", "given_name", "employment", "home_checkpoint",
                                             "new_object_projections", "new_objects_detected",
                                             "detection_performance_pct", "xray_duty_from_1_jan_2027"], rows,
                 newline="\n")
    # ------------------------------------------------------------------ chart and review
    png = os.path.join(gen, "detection_chart.png")
    chart(tab, off, png)
    ink = colors.HexColor("#222222")
    grey = colors.HexColor("#5b666d")
    st = {"k": ParagraphStyle("k", fontName="Helvetica", fontSize=8.2, leading=10.4, textColor=grey, spaceAfter=2),
          "t": ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=13.2, leading=16.5, textColor=ink, spaceAfter=6),
          "m": ParagraphStyle("m", fontName="Helvetica", fontSize=8.8, leading=11.2, textColor=ink),
          "p": ParagraphStyle("p", fontName="Helvetica", fontSize=9.2, leading=12.6, textColor=ink, spaceAfter=5),
          "h": ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=ink, spaceBefore=7,
                              spaceAfter=3),
          "c": ParagraphStyle("c", fontName="Helvetica", fontSize=7.8, leading=9.8, textColor=grey, spaceAfter=4),
          "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=8.3, leading=10.2, textColor=ink)}
    offt = tab[tab["staff_no"].isin(off)].sort_values("golden")
    masked = offt[offt["overall"] >= P.STANDARD]
    n_ft = int(sum(1 for r in masked.itertuples() if r.employment == "Full-time"))
    raw_off = M["r0"]
    memo = Table([[Paragraph("<b>To</b>", st["m"]), Paragraph("Teresa Malone, Head of Security Screening", st["m"])],
                  [Paragraph("<b>From</b>", st["m"]), Paragraph("Training and standards lead", st["m"])],
                  [Paragraph("<b>Date</b>", st["m"]), Paragraph("3 December 2026", st["m"])],
                  [Paragraph("<b>Subject</b>", st["m"]),
                   Paragraph("Screening year 2025-26: annual assessment, currency and lane throughput under SCS-04 "
                             "revision 6", st["m"])]],
                 colWidths=[20 * mm, 150 * mm], hAlign="LEFT")
    memo.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
                              ("TOPPADDING", (0, 0), (-1, -1), 1), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                              ("LINEBELOW", (0, -1), (-1, -1), 0.6, colors.HexColor("#9aa3aa"))]))
    tstyle = TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.3), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.3),
                         ("TEXTCOLOR", (0, 0), (-1, -1), ink),
                         ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#7d8b93")),
                         ("ALIGN", (1, 0), (-1, -1), "RIGHT"), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                         ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("LEFTPADDING", (0, 0), (0, -1), 0)])
    who = [["Officer", "Staff no.", "Employment", "Checkpoint", "New objects shown", "Detected", "Detection (%)"]]
    for r in offt.itertuples():
        who.append(["%s %s" % (r.given, r.surname), r.staff_no, r.employment, r.checkpoint, "{:,}".format(r.n_first),
                    "{:,}".format(r.first_hits), "%.1f" % (100 * r.golden)])
    t0 = Table(who, colWidths=[38 * mm, 20 * mm, 22 * mm, 23 * mm, 27 * mm, 18 * mm, 22 * mm], hAlign="LEFT")
    t0.setStyle(TableStyle(tstyle.getCommands() + [("ALIGN", (1, 0), (3, -1), "LEFT")]))
    story = [
        Paragraph("Silverwattle Coast Airport | Security Screening", st["k"]),
        Paragraph("%s officers come off X-ray duty at the January 2027 recertification" % word(len(off)).capitalize(),
                  st["t"]),
        memo, Spacer(1, 6),
        Paragraph("1. Annual assessment", st["h"]),
        Paragraph("<b>%s officers come off X-ray duty from 1 January 2027</b> until they have completed remedial "
                  "training and passed the image interpretation assessment (SCS-04 section 4). Every other officer "
                  "holding an X-ray endorsement on 30 November 2026, %d in all, is recertified for 2027."
                  % (word(len(off)).capitalize(), len(tab) - len(off)), st["p"]),
        t0, Spacer(1, 2),
        Paragraph("Projections from 1 July 2025 to 30 November 2025 count only to decide whether an object had "
                  "already been shown to the officer.", st["c"]),
        Paragraph("SCS-04 reads detection performance on prohibited items the officer has not been shown before. "
                  "Here an item is a threat object in the TIP library, whichever of its orientations was projected, "
                  "and before runs back through the CT record to 1 July 2025: in the screening year first showings "
                  "of an object were detected %.1f per cent of the time against %.1f per cent for repeat showings, an "
                  "orientation new to the officer whose object had already been shown %.1f per cent, and an object "
                  "first shown before December over %d per cent when shown again. Keyed on the image, or counted "
                  "from 1 December, first showings would take off only %s casual officers. %s of the officers "
                  "coming off clear 80 per cent on the raw hit rate, %s of them full-time."
                  % (100 * M["pooled_hit_first"], 100 * M["pooled_hit_repeat"], 100 * ev["other_orientation"],
                     int(math.floor(100 * ev["pre_window_min"])), word(len(M["r2"])),
                     word(len(masked)).capitalize(), word(n_ft)), st["p"]),
        Image(png, width=174 * mm, height=80.2 * mm),
        Paragraph("Source: threat image projection records, 1 July 2025 to 30 November 2026, joined to TIP library "
                  "release %s and the CT operator logins; officers from the officer register at 30 November 2026."
                  % release, st["c"]),
    ]
    cur = [["Month", "Endorsed all month", "Short of 20 hours"]]
    for (y, m), v in zip(A.MONTHS, asks_a):
        cur.append(["%s %d" % (MONTH_NAME[m], y), str(len(pop_a[(y, m)])), str(v)])
    t1 = Table(cur, colWidths=[38 * mm, 32 * mm, 32 * mm], hAlign="LEFT", repeatRows=1)
    t1.setStyle(tstyle)
    story += [KeepTogether([
                  Paragraph("2. Currency", st["h"]),
                  Paragraph("Officers endorsed for the whole of each month, by the officer register's endorsement "
                            "and lapse dates, who fell short of the 20 hours of X-ray time a month that SCS-04 section 5 "
                            "requires.", st["p"]),
                  t1, Spacer(1, 3),
                  Paragraph("Source: lane roster and payroll leave records. An officer's X-ray time on a lane is the "
                            "time worked there divided by the officers working the lane at each moment (SCS-04 "
                            "section 3); an officer on personal leave on a rostered day records no projection that day "
                            "and did not work.", st["c"])]),
              Paragraph("3. Throughput", st["h"]),
              Paragraph("Passenger bags each CT lane screened in each quarter of the screening year, to the nearest "
                        "thousand, for the year-end return to the security committee (SCS-04 section 6).", st["p"])]
    thr = [["Lane", "Dec-Feb", "Mar-May", "Jun-Aug", "Sep-Nov"]]
    for ln in P.LANES:
        thr.append([ln] + ["{:,}".format(A.rnd_k(asks_b[(ln, q)])) for q, _, _ in A.QUARTERS])
    t2 = Table(thr, colWidths=[20 * mm] + [26 * mm] * 4, hAlign="LEFT")
    t2.setStyle(tstyle)
    story += [t2, Spacer(1, 3),
              Paragraph("Source: CT units' hourly image counts, each unit placed on the lane it stood on that day "
                        "(D2's unit replaced in March 2026, and the spare unit's days on a lane whose own unit was away, "
                        "included). Images counted before a lane's first rostered start are start-up test "
                        "images (SCS-04 section 3), and no projection is recorded on the lane then; they are left out. "
                        "Quarters in Sydney time.",
                        st["c"])]

    def page(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.2)
        canvas.setFillColor(grey)
        canvas.drawString(18 * mm, 9 * mm, "SCS-04 annual assessment 2025-26 | Security Screening")
        canvas.drawRightString(A4[0] - 18 * mm, 9 * mm, "Page %d" % d.page)
        canvas.restoreState()
    path = os.path.join(golden, PDF)
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=15 * mm,
                            bottomMargin=16 * mm, title="Screening year 2025-26 review", author="Security Screening",
                            creator="Silverwattle Coast Airport", producer="Silverwattle Coast Airport", invariant=1)
    doc.build(story, onFirstPage=page, onLaterPages=page)
    data = open(path, "rb").read()
    for sig in (b"ReportLab Generated PDF document (opensource)", b"ReportLab generated PDF document -- digest (opensource)",
                b"ReportLab Generated PDF document http://www.reportlab.com"):
        data = data.replace(sig, b" " * len(sig))
    data = re.sub(rb"/CreationDate \(D:[^)]*\)", b"/CreationDate (D:20261203154000+11'00')", data)
    data = re.sub(rb"/ModDate \(D:[^)]*\)", b"/ModDate (D:20261203161800+11'00')", data)
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
        "image_off_count": len(M["r2"]),
        "inyear_off_count": len(M["r2b"]),
        "pooled_other_orientation_pct": round(100 * ev["other_orientation"], 1),
        "pre_window_repeat_floor_pct": int(math.floor(100 * ev["pre_window_min"])),
        "pooled_first_raw": round(float(M["pooled_hit_first"]), 5),
        "pooled_repeat_raw": round(float(M["pooled_hit_repeat"]), 5),
    }
    with open(os.path.join(gen, "figures.json"), "w") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
    return fig
