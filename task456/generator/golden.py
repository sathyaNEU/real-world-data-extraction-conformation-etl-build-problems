"""The golden from the bundle alone: conform the census survey, the bed-status board and the transfer center's calls
to one row per compact hospital and local day, estimate each region's share of full adult ICU hospital-days with a
two-class latent class model of the three feeds, compare it with the compact's one in three, count the asks
(out-of-region placements, emergency department diversion hours, adult ICU closed hours before the window), and
write the activation notice and the conformed hospital-day file."""
import csv
import io
import json
import os

import numpy as np

import conform as CF
import methods as M
import pack as P
import world as W

PDF_NAME = "surge_activation_notice_2026-01-26.pdf"
CSV_NAME = "hospital_days_conformed_2025-12-22_2026-01-18.csv"


def compute(target):
    pk = CF.Pack(target, P.FILES)
    gd = M.golden(pk)
    cen = pk.census()
    X = dict(pk=pk, gd=gd, cen=cen)
    X["tenth"] = {g: M.tenth(gd["share"][g]) for g in W.RCODE}
    X["days"] = {g: int((gd["reg"] == g).sum()) for g in W.RCODE}
    X["hospitals"] = {g: len({r[1] for r in gd["rows"] if r[0] == g}) for g in W.RCODE}
    X["ask_a"] = M.ask_a(pk)
    X["ask_b"] = M.ask_b(pk)
    X["ask_c"] = M.ask_c(pk)
    X["rules"] = M.rules(gd)
    return X


def pct(x):
    return "%d%%" % x


def fmt(v):
    return format(int(v), ",")


def chart_png(X):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["font.family"] = "DejaVu Sans"
    gd = X["gd"]
    order = list(W.RCODE)
    y = np.arange(len(order))
    vals = [100 * gd["share"][g] for g in order]
    cols = ["#9b2c2c" if g in gd["regions"] else "#a7b0ba" for g in order]
    fig, ax = plt.subplots(figsize=(7.0, 3.9), dpi=150)
    ax.barh(y, vals, height=0.62, color=cols)
    for i, g in enumerate(order):
        ax.text(vals[i] + 1.2, y[i], pct(X["tenth"][g]), va="center", fontsize=7.8, color="#1c1f24")
    ax.axvline(100 / 3, color="#1c1f24", linestyle="--", linewidth=1.0)
    ax.text(100 / 3 + 0.8, len(order) - 0.45, "one in three (33.3%)", fontsize=7.6, color="#1c1f24", va="bottom")
    ax.set_yticks(y)
    ax.set_yticklabels([W.RNAME[g] for g in order], fontsize=7.8)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Full days, per cent of the region's adult ICU hospital-days", fontsize=8)
    ax.tick_params(axis="x", labelsize=7.5)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.set_title("Four regions had one in three hospital-days full or more, 22 December to 18 January",
                 fontsize=8.8, loc="left")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color="#9b2c2c", label="activated"), Patch(color="#a7b0ba", label="not activated")],
              loc="lower right", fontsize=7.4, frameon=False)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def write_pdf(X, path):
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    import docs  # noqa: F401  (registers the fonts)
    INK, GREY, RED = colors.HexColor("#1c1f24"), colors.HexColor("#5e636b"), colors.HexColor("#7f1d1d")
    body = ParagraphStyle("b", fontName="LiberationSans", fontSize=9.4, leading=13.2, textColor=INK, spaceAfter=6)
    kick = ParagraphStyle("k", fontName="LiberationSans-Bold", fontSize=8.4, leading=11, textColor=GREY, spaceAfter=2)
    h1 = ParagraphStyle("h1", fontName="LiberationSans-Bold", fontSize=14.5, leading=18.5, textColor=RED, spaceAfter=4)
    sub = ParagraphStyle("s", fontName="LiberationSans", fontSize=8.8, leading=12.2, textColor=GREY, spaceAfter=10)
    h2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.3, leading=14, textColor=RED, spaceBefore=8,
                        spaceAfter=3)
    cell = ParagraphStyle("c", fontName="LiberationSans", fontSize=8.5, leading=10.8, textColor=INK)
    num = ParagraphStyle("num", parent=cell, alignment=2)
    note = ParagraphStyle("n", fontName="LiberationSans-Italic", fontSize=7.7, leading=10.3, textColor=GREY,
                          spaceBefore=3, spaceAfter=8)

    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans", 7.5)
        canvas.setFillColor(GREY)
        canvas.drawString(20 * mm, 12 * mm, "%s  |  Activation notice, 26 January to 22 February 2026" % W.COMPACT)
        canvas.drawRightString(letter[0] - 20 * mm, 12 * mm, "%d" % doc.page)
        canvas.restoreState()

    gd = X["gd"]
    on = [W.RNAME[g] for g in W.RCODE if g in gd["regions"]]
    off = [W.RNAME[g] for g in W.RCODE if g not in gd["regions"]]
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=17 * mm,
                            bottomMargin=20 * mm, title="Activation notice, 26 January to 22 February 2026",
                            author=W.PEOPLE["data"], subject="", creator="", producer="")
    s = [Paragraph(W.COMPACT.upper(), kick),
         Paragraph("The compact activates in %s, %s, %s and %s from 26 January" % tuple(on), h1),
         Paragraph("Activation notice for 26 January to 22 February 2026, from the operations committee's review of "
                   "Tuesday 20 January. %s, data team, %s. Issued 21 January 2026." % (W.PEOPLE["data"], W.ALLIANCE),
                   sub),
         Paragraph("At its review of 20 January the operations committee activated the compact in <b>%s, %s, %s and "
                   "%s</b> for the four weeks from Monday 26 January to Sunday 22 February 2026: in each of them at "
                   "least one in three of the region's adult ICU hospital-days from 22 December to 18 January were "
                   "full days. In %s, %s, %s and %s the share was well under one in three, and the compact is not "
                   "activated there. Activation brings the transfer, staffing and ambulance arrangements of article 5 into force "
                   "in the four regions." % tuple(on + off), body)]
    rows = [[Paragraph("<b>Region</b>", cell), Paragraph("<b>Compact hospitals</b>", num),
             Paragraph("<b>Hospital-days</b>", num), Paragraph("<b>Share of hospital-days full</b>", num),
             Paragraph("<b>Activated</b>", cell)]]
    for g in W.RCODE:
        rows.append([Paragraph(W.RNAME[g], cell), Paragraph(str(X["hospitals"][g]), num),
                     Paragraph(fmt(X["days"][g]), num), Paragraph(pct(X["tenth"][g]), num),
                     Paragraph("<b>Yes</b>" if g in gd["regions"] else "No", cell)])
    rows.append([Paragraph("<b>All regions</b>", cell), Paragraph("<b>%d</b>" % sum(X["hospitals"].values()), num),
                 Paragraph("<b>%s</b>" % fmt(sum(X["days"].values())), num), Paragraph("", num), Paragraph("", cell)])
    t = Table(rows, colWidths=[40 * mm, 28 * mm, 28 * mm, 38 * mm, 24 * mm])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, RED), ("LINEABOVE", (0, -1), (-1, -1), 0.4, GREY),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 2.2),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2)]))
    s += [t, Paragraph("Shares to the nearest ten per cent; the committee decides on the unrounded share against one "
                       "in three (article 4.1).", note),
          Image(io.BytesIO(chart_png(X)), width=170 * mm, height=94.7 * mm),
          Paragraph("Source: the alliance's census survey, the regional bed-status board and the %s's call log, "
                    "extract of 20 January 2026." % W.CENTER, note),
          KeepTogether([Paragraph("How the shares were estimated", h2),
          Paragraph("None of the three feeds records full days. The census survey counts adult ICU patients against "
                    "staffed beds at 07:00 and misses a unit that fills later in the day; the bed-status board shows "
                    "an adult ICU Closed on nearly every full day, but also on many ordinary days, when a hospital "
                    "keeps its last staffed beds for its own patients; the transfer center shows a no-bed decline only "
                    "when a request reaches the hospital that day. We conformed the three feeds to the %s hospital-days "
                    "of the 28 days, on each hospital's own dates: the latest census report of each hospital and day, "
                    "the adult ICU line's board status replayed from its events, and the adult ICU calls declined for "
                    "no staffed bed. Each region's share of full days is the prevalence in a two-class latent class "
                    "model of the three feeds, each feed's chance of showing a full day and an ordinary day the same "
                    "at every hospital, the share free in each region, fitted by maximum likelihood; a day without a "
                    "census report (Christmas Day and New Year's Day at some hospitals) enters through the other two "
                    "feeds. The fit puts the board at about nine in ten full days and a third of ordinary days, the "
                    "census at about a third of full days and the transfer center at about a quarter, each with few "
                    "false signals. "
                    "Counting a day full whenever any feed shows it would put all eight regions over one in three; "
                    "counting it only when two feeds agree would put none there." % fmt(sum(X["days"].values())),
                    body)])]
    a, b, c = X["ask_a"], M.whole(X["ask_b"]), M.whole(X["ask_c"])
    rows = [[Paragraph("<b>Region</b>", cell),
             Paragraph("<b>Adult ICU placements in another region (22 December to 18 January)</b>", num),
             Paragraph("<b>Emergency department diversion, hours (22 December to 18 January)</b>", num),
             Paragraph("<b>Adult ICU shown Closed, hours (24 November to 21 December)</b>", num)]]
    for g in W.RCODE:
        rows.append([Paragraph(W.RNAME[g], cell), Paragraph(fmt(a[g]), num), Paragraph(fmt(b[g]), num),
                     Paragraph(fmt(c[g]), num)])
    rows.append([Paragraph("<b>All regions</b>", cell), Paragraph("<b>%s</b>" % fmt(sum(a.values())), num),
                 Paragraph("<b>%s</b>" % fmt(sum(b.values())), num), Paragraph("<b>%s</b>" % fmt(sum(c.values())), num)])
    t2 = Table(rows, colWidths=[40 * mm, 44 * mm, 44 * mm, 42 * mm])
    t2.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, RED), ("LINEABOVE", (0, -1), (-1, -1), 0.4, GREY),
                            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 2.2),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2)]))
    s += [KeepTogether([
        Paragraph("Transfers, diversion and closures by region", h2),
        Paragraph("For the transfer agreements, the EMS coordinators and the committee's reading of how the strain "
                  "built, region by region:", body), t2,
        Paragraph("Placements: adult ICU requests opened on the sending hospital's own dates in the 28 days, accepted "
                  "by a hospital in another region and not cancelled, by the sending hospital's region (annex A "
                  "counties; senders outside Tennessee have none); each placement of a patient moved on counts, and a "
                  "case the new call system took over at its 5 January start counts once. Diversion: an emergency "
                  "department's Divert status and, from 5 January, when the board shows diversion as Advisory, its "
                  "Advisory status with the reason EMS diversion. Closed: the adult ICU line's Closed status, board "
                  "events before 8 December read through the facility codes then in use. Hours on each hospital's "
                  "own clock, added over the region's hospitals and rounded to the whole hour. Source: the %s's two "
                  "call logs and the regional bed-status board, extract of 20 January 2026." % W.CENTER, note)])]
    s += [Spacer(1, 6), Paragraph("%s, data team, %s<br/>For the operations committee: %s, chair" % (
        W.PEOPLE["data"], W.ALLIANCE, W.PEOPLE["chair"]), body)]
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


def write_csv(X, path):
    gd, cen = X["gd"], X["cen"]
    rows = []
    for reg, lic, name, d, a, b, c in sorted(gd["rows"], key=lambda r: (r[3], r[0], r[2])):
        cs = cen.get((lic, d))
        rows.append((d.isoformat(), reg, W.RNAME[reg], lic, name, "" if cs is None else cs[0],
                     "" if cs is None else cs[1], "" if a is None else a, b, c))
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(["date", "region_code", "region_name", "licence_no", "facility_name",
                    "census_staffed_adult_icu_beds_0700", "census_adult_icu_patients_0700", "census_full_at_0700",
                    "board_adult_icu_closed", "transfer_center_no_bed_decline"])
        w.writerows(rows)
    return len(rows)


def figures(X):
    gd = X["gd"]
    a, b, c = X["ask_a"], M.whole(X["ask_b"]), M.whole(X["ask_c"])
    nm = W.RNAME
    return {
        "activated": [nm[g] for g in W.RCODE if g in gd["regions"]],
        "not_activated": [nm[g] for g in W.RCODE if g not in gd["regions"]],
        "regions_activated": len(gd["regions"]),
        "share_pct": {nm[g]: X["tenth"][g] for g in W.RCODE},
        "share_unrounded": {nm[g]: round(float(gd["share"][g]), 3) for g in W.RCODE},
        "share_unrounded_pct": {nm[g]: round(100 * float(gd["share"][g]), 1) for g in W.RCODE},
        "hospitals": {nm[g]: X["hospitals"][g] for g in W.RCODE},
        "hospitals_all": sum(X["hospitals"].values()),
        "hospital_days": {nm[g]: X["days"][g] for g in W.RCODE},
        "hospital_days_all": sum(X["days"].values()),
        "feed_full_day_rate_pct": {"census": round(100 * gd["s"][0]), "board": round(100 * gd["s"][1]),
                                   "transfer center": round(100 * gd["s"][2])},
        "feed_ordinary_day_rate_pct": {"census": round(100 * gd["f"][0], 1), "board": round(100 * gd["f"][1]),
                                       "transfer center": round(100 * gd["f"][2], 1)},
        "flagged_days": {"census": int(np.nansum(gd["Y"][:, 0])), "board": int(gd["Y"][:, 1].sum()),
                         "transfer center": int(gd["Y"][:, 2].sum()),
                         "no census report": int(np.isnan(gd["Y"][:, 0]).sum())},
        "any_feed_share_pct": {nm[g]: round(100 * X["rules"]["any feed"]["share"][g], 1) for g in W.RCODE},
        "any_feed_regions": len(X["rules"]["any feed"]["regions"]),
        "two_of_three_share_pct": {nm[g]: round(100 * X["rules"]["two of three"]["share"][g], 1) for g in W.RCODE},
        "two_of_three_regions": len(X["rules"]["two of three"]["regions"]),
        "placements_out_of_region": {nm[g]: a[g] for g in W.RCODE},
        "placements_out_of_region_all": sum(a.values()),
        "diversion_hours": {nm[g]: b[g] for g in W.RCODE},
        "diversion_hours_all": sum(b.values()),
        "diversion_hours_unrounded": {nm[g]: round(X["ask_b"][g], 2) for g in W.RCODE},
        "closed_hours": {nm[g]: c[g] for g in W.RCODE},
        "closed_hours_all": sum(c.values()),
        "closed_hours_unrounded": {nm[g]: round(X["ask_c"][g], 2) for g in W.RCODE},
        "window_days": 28, "threshold": "one in three", "rounding_shares_pct": 10,
    }


def main(target, out_dir, fig_path):
    os.makedirs(out_dir, exist_ok=True)
    X = compute(target)
    write_pdf(X, os.path.join(out_dir, PDF_NAME))
    X["csv_rows"] = write_csv(X, os.path.join(out_dir, CSV_NAME))
    import postprocess as PP
    PP.normalize_pdf(os.path.join(out_dir, PDF_NAME), b"D:20260121090812-06'00'", b"D:20260121093447-06'00'")
    with open(fig_path, "w") as f:
        json.dump(figures(X), f, indent=1, ensure_ascii=False)
        f.write("\n")
    return X
