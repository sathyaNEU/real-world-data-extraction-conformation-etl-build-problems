"""The two deliverables: the position table the engineer keeps, and the note the review panel reads."""
import datetime as dt
import math
import os

import numpy as np

import world as W

BAND_LABEL = {25: "25", 31.5: "31.5", 40: "40", 50: "50", 63: "63", 80: "80", 100: "100", 125: "125",
              160: "160", 200: "200", 250: "250", 315: "315", 400: "400", 500: "500", 630: "630",
              800: "800", 1000: "1000", 1250: "1250", 1600: "1600", 2000: "2000", 2500: "2500",
              3150: "3150", 4000: "4000", 5000: "5000", 6300: "6300", 8000: "8000", 10000: "10000",
              12500: "12500"}


def table(path, g):
    """specific_sound_levels.csv: one row per monitoring position, in schedule order."""
    import csv as _c
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = _c.writer(fh, lineterminator="\n")
        w.writerow(["position_code", "dwelling_ref", "specific_sound_level_db_laeq", "valid_minutes",
                    "excluded_minutes", "highest_third_octave_band_hz", "tone_prominent"])
        for row in g["rows"]:
            band = BAND_LABEL[row["band_hz"]] if row["band_hz"] else "none"
            tone = "none" if row["tone"] is None else ("yes" if row["tone"] else "no")
            w.writerow([row["position"], row["dwelling"], "%.1f" % row["specific_db"],
                        row["valid_minutes"], row["excluded_minutes"], band, tone])
    return path


def chart(path, g):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ordered = g["ordered"]
    codes = [r["position"] for r in ordered]
    vals = [r["specific_db"] for r in ordered]
    picked = set(g["slate"])
    fig, ax = plt.subplots(figsize=(7.2, 3.1), dpi=200)
    bars = ax.bar(range(len(codes)), vals,
                  color=["#1f4e5f" if c in picked else "#b8c6cc" for c in codes],
                  edgecolor="#13343b", linewidth=0.5, width=0.74)
    ax.set_xticks(range(len(codes)))
    ax.set_xticklabels(codes, fontsize=7.5, rotation=0)
    ax.set_ylabel("Specific sound level, dB LAeq", fontsize=8)
    ax.set_ylim(34, max(vals) + 2.2)
    ax.tick_params(axis="y", labelsize=7.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    cut = (vals[g["cap"] - 1] + vals[g["cap"]]) / 2.0
    for i, (b, v) in enumerate(zip(bars, vals)):
        off = 0.46 if abs(v + 0.22 - cut) < 0.3 else 0.22
        ax.text(b.get_x() + b.get_width() / 2.0, v + off, "%.1f" % v, ha="center", fontsize=6.6,
                color="#13343b")
    ax.axhline(cut, color="#8a4b08", linewidth=0.9, linestyle=(0, (4, 3)))
    ax.text(len(codes) - 0.4, cut + 0.18, "slot reaches %d dwellings" % g["cap"], ha="right",
            fontsize=6.8, color="#8a4b08")
    ax.set_title("The plant's own contribution at each dwelling: %s to %s carry the slot"
                 % (g["slate_ordered"][0], g["slate_ordered"][-1]), fontsize=8.6, loc="left",
                 color="#13343b")
    fig.tight_layout(pad=0.5)
    fig.savefig(path, metadata={"Software": None, "Source": None})
    plt.close(fig)
    return path


def note(path, g, chart_png):
    from reportlab import rl_config
    rl_config.invariant = 1
    rl_config.useA85 = 0
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_JUSTIFY
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    SS = getSampleStyleSheet()
    BODY = ParagraphStyle("b", parent=SS["BodyText"], fontName="Helvetica", fontSize=9.2, leading=12.6,
                          alignment=TA_JUSTIFY, spaceAfter=5)
    H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Helvetica-Bold", fontSize=12.5,
                        spaceAfter=3)
    H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=10,
                        spaceAfter=3, spaceBefore=9)
    SMALL = ParagraphStyle("s", parent=BODY, fontSize=7.8, leading=10)
    CELL = ParagraphStyle("c", fontName="Helvetica", fontSize=8, leading=10)
    CELLB = ParagraphStyle("cb", fontName="Helvetica-Bold", fontSize=8, leading=10)
    TBL = TableStyle([("GRID", (0, 0), (-1, -1), 0.3, colors.Color(0.5, 0.5, 0.5)),
                      ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.91, 0.92, 0.91)),
                      ("VALIGN", (0, 0), (-1, -1), "TOP"),
                      ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                      ("TOPPADDING", (0, 0), (-1, -1), 1.8), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8)])

    def wrap(rows):
        return [[Paragraph(str(c), CELLB if i == 0 else CELL) for c in row] for i, row in enumerate(rows)]

    d = SimpleDocTemplate(path, pagesize=A4, title="Mitigation shortlist, October slot", author="",
                          subject="", creator="", leftMargin=18 * mm, rightMargin=18 * mm,
                          topMargin=16 * mm, bottomMargin=16 * mm)
    sel = g["slate_dwellings"]
    reasons = {r["position"]: r for r in g["rows"]}
    f = [Paragraph("Five dwellings for the October acoustic treatment slot", H1),
         Paragraph("To %s, operations manager. From %s, environmental engineer. 16 October 2026. "
                   "Autumn 2026 noise survey, %s %s. Slot to be ordered Monday 26 October."
                   % (W.PEOPLE["operations"][0], W.PEOPLE["engineer"][0], W.OPERATOR, W.SITE), SMALL),
         Paragraph("The survey put a meter at each of the fourteen positions in the schedule for two "
                   "weeks between 31 August and 11 October. The specific sound level below is the plant's "
                   "own contribution at the dwelling over the assessment period, with the residual sound "
                   "of each position's surroundings taken off in energy. The five dwellings the slot "
                   "reaches are %s. %s is the first dwelling off the list, %.1f dB below the fifth."
                   % (", ".join("%s (%s)" % (c, dref) for c, dref, _, _ in sel),
                      g["sixth"], g["margin_db"]), BODY),
         Image(chart_png, width=168 * mm, height=72.3 * mm),
         Paragraph("What the slot covers", H2),
         Table(wrap([["Position", "Dwelling", "Specific sound level, dB LAeq", "Glazing"]]
                    + [[c, "%s, %s" % (dref, name), "%.1f" % lvl,
                        "with acoustic trickle vents" if reasons[c]["tone"]
                        else "standard unit"]
                       for c, dref, name, lvl in sel]),
               colWidths=[22 * mm, 74 * mm, 34 * mm, 38 * mm], style=TBL),
         Paragraph("A tone is prominent at %d of the five, and those four take the glazing with acoustic "
                   "trickle vents; %s takes the standard unit."
                   % (sum(1 for c, _, _, _ in sel if reasons[c]["tone"]),
                      ", ".join(c for c, _, _, _ in sel if not reasons[c]["tone"])), SMALL),
         Paragraph("The plant through the survey", H2),
         Paragraph("The plant ran to its ordinary pattern in every one of the six weeks, so the positions "
                   "measured in different weeks are comparable.", BODY),
         Table(wrap([["Week beginning", "Biogas burned, m3", "Blower air delivered, thousand Nm3",
                      "Centrifuge runs"]]
                    + [["%d %s" % (W.WEEKS[k].day, W.WEEKS[k].strftime("%B")),
                        "{:,}".format(v["biogas_m3"]), "{:,}".format(v["blower_air_knm3"]),
                        "%d" % v["centrifuge_runs"]]
                       for k, v in sorted(g["weekly"].items())]),
               colWidths=[32 * mm, 40 * mm, 56 * mm, 32 * mm], style=TBL),
         Paragraph("Levels are to one decimal place. Minutes the mast counted rain in, minutes it showed "
                   "above the plan's wind limit and minutes a meter recorded nothing for are out of every "
                   "level, as the plan requires, and the %d deployments whose field checks sat away from "
                   "the calibrator, on two of the five meters, have been corrected."
                   % g["corrected_count"], SMALL)]
    d.build(f)
    return path
