"""The goldens: the two-page quote letter (heat_cover_quote_2027_28.pdf) with its chart, and the cover's record by
season (heat_cover_payouts.csv)."""
import csv
import io

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt                                                    # noqa: E402
from reportlab import rl_config                                                    # noqa: E402

rl_config.invariant = 1
from reportlab.lib.enums import TA_RIGHT                                          # noqa: E402
from reportlab.lib.pagesizes import A4                                             # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                    # noqa: E402
from reportlab.lib.units import mm                                                 # noqa: E402
from reportlab.platypus import (Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,  # noqa: E402
                                TableStyle)

import docs as D       # noqa: E402
import pricing as P    # noqa: E402
import world as W      # noqa: E402

QUOTE = "heat_cover_quote_2027_28.pdf"
PAYOUTS = "heat_cover_payouts.csv"
BAR, LINE, MUTED = "#3f6fa8", "#20242a", "#8a9097"


def chart(heat, gold):
    seasons = P.SEASONS
    a = gold["expected_heat"] - gold["slope_heat_decade"] / 10 * W.PRICED_SEASON
    b = gold["slope_heat_decade"] / 10
    fig, ax = plt.subplots(figsize=(7.2, 3.5), dpi=150)
    ax.bar(seasons, [heat[s] for s in seasons], width=0.72, color=BAR, linewidth=0)
    xs = [seasons[0], W.PRICED_SEASON]
    ax.plot(xs, [a + b * x for x in xs], color=LINE, linewidth=2)
    ax.plot([W.PRICED_SEASON], [gold["expected_heat"]], marker="o", markersize=7, color=LINE)
    top = max(heat[s] for s in seasons) * 1.28
    ax.set_ylim(0, top)
    ax.annotate("2027/28: %.1f heat days" % gold["expected_heat"], (W.PRICED_SEASON, gold["expected_heat"]),
                xytext=(W.PRICED_SEASON - 0.5, top * 0.93), textcoords="data", ha="right", va="top", fontsize=8.5,
                color=LINE, arrowprops=dict(arrowstyle="-", color=LINE, linewidth=0.8))
    ax.axvline(W.CHANGE.year + 0.5, color=MUTED, linewidth=1, linestyle=(0, (4, 3)))
    ax.text(W.CHANGE.year, top * 0.97, "probe in small shield from Nov 1995;\nglass era converted at each reading ",
            fontsize=7.5, color=MUTED, va="top", ha="right")
    ax.set_ylabel("Heat days (35.0 C or more)", fontsize=8.5)
    ax.set_xticks([1965, 1975, 1985, 1995, 2005, 2015, 2027])
    ax.set_xticklabels(["1965/66", "1975/76", "1985/86", "1995/96", "2005/06", "2015/16", "2027/28"], fontsize=8)
    ax.tick_params(axis="y", labelsize=8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.grid(axis="y", color="#e3e5e8", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.set_title("Merrin Flat heat days a season on today's probe, with the line the premium is read from",
                 fontsize=9.2, loc="left", color=LINE)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return buf


def _table(rows, widths, last_bold=True):
    def style(i, j):
        bold = i == 0 or (last_bold and i == len(rows) - 1)
        st = D.S_CELLB if bold else D.S_CELL
        return ParagraphStyle("r%d%d" % (bold, j > 0), parent=st, alignment=TA_RIGHT) if j > 0 else st
    data = [[Paragraph(str(c), style(i, j)) for j, c in enumerate(r)] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.7, D.INK), ("LINEABOVE", (0, -1), (-1, -1), 0.4, D.GREY),
                           ("ALIGN", (1, 0), (-1, -1), "RIGHT"), ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
    return t


def write_quote(path, fig, mc):
    gold = mc["golden"]
    rate = gold["premium"]
    who, role = W.PEOPLE["analyst"]
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=23 * mm, rightMargin=23 * mm, topMargin=21 * mm,
                            bottomMargin=20 * mm, title="Heat-day cover 2027/28: quote", author=who, subject="",
                            creator="", producer="")
    sd = fig["sub_districts"]
    s = [Paragraph("SOUTHWARD MUTUAL · WEATHER DESK", D.S_META),
         Paragraph("Merrin Valley heat-day cover 2027/28: $%d a hectare" % rate, D.S_H1),
         Paragraph("To %s, %s. From %s, %s, for %s. 6 September 2027. Ref HC104/2027." % (
             W.PEOPLE["coop"][0], W.PEOPLE["coop"][1], who, role, W.PEOPLE["portfolio"][0]), D.S_META),
         Paragraph("We quote $%d a hectare for the 2027/28 season on the terms of the quote term sheet (heat days at "
                   "35.0 C or more after the first %d, $%d each; severe heat days at 40.0 C or more, $%d each; at most "
                   "$%s a hectare). The premium assumes %s heat days and %s severe heat days at Merrin Flat in 2027/28, "
                   "the values for 2027/28 of the lines fitted to every season since 1965/66." % (
                       rate, W.DEDUCTIBLE_DAYS, W.HEAT_RATE, W.SEVERE_RATE, "{:,}".format(int(W.CAP)),
                       fig["expected_heat_days_2027_28"], fig["expected_severe_days_2027_28"]), D.S_BODY),
         Paragraph("Merrin Flat's heat days have run higher since the station went automatic in November 1995, and part "
                   "of that rise is the instrument, not the weather. The probe in its small shield reads the same as the "
                   "old glass thermometer on ordinary days and warmer on hot afternoons: in the Service's parallel "
                   "observations the difference is %s C at a glass reading of 34.5 C and %s C at 39.0 C, against %s C "
                   "on average at Merrin Flat. Brought to today's probe reading by reading, the glass years gain %d heat "
                   "days and %d severe heat days, and the heat-day line rises %s days a decade, not the %s days the "
                   "unconverted record shows. Converting the glass years by the average difference moves no half-degree "
                   "reading across either trigger and would have priced the cover at $%d a hectare." % (
                       fig["conversion_at_34_5"], fig["conversion_at_39_0"], fig["mean_conversion_merrin_flat"],
                       fig["glass_era_heat_days_added"], fig["glass_era_severe_days_added"],
                       fig["heat_line_slope_days_per_decade"], fig["default_heat_line_slope_days_per_decade"],
                       fig["default_premium_per_ha"]), D.S_BODY),
         Paragraph("The schedule at attachment", D.S_H2)]
    rows = [["Sub-district", "Member blocks", "Insured ha", "Premium"]]
    for name in W.SUB_DISTRICTS:
        v = sd[name]
        rows.append([name, v["blocks"], "%.1f" % v["ha"], "${:,}".format(v["premium"])])
    rows.append(["Total", fig["blocks_total"], fig["insured_ha_total"],
                 "${:,}".format(sum(v["premium"] for v in sd.values()))])
    s += [_table(rows, [48 * mm, 30 * mm, 30 * mm, 32 * mm]),
          Paragraph("Blocks on the policy schedule on 1 December 2027, each once at its insured area, by the "
                    "co-operative's sub-districts in its block register of 1 August 2027. Premium is the rate times "
                    "each sub-district's hectares, to the nearest whole dollar (50 cents up).", D.S_META),
          PageBreak(),
          Paragraph("The record the premium is read from", D.S_H2),
          Image(chart(mc["heat"], gold), width=164 * mm, height=164 * mm * 3.5 / 7.2),
          Paragraph("Seasons are 1 December to the end of February. Glass years (to 1994/95) are converted to the probe "
                    "at each half-degree reading by the mean probe-minus-glass difference at that reading in the "
                    "parallel observations; the probe years are as approved by the Service.", D.S_META),
          Paragraph("What the cover has paid", D.S_H2)]
    rows = [["Season", "Claims paid", "Paid"]]
    for lab, v in fig["seasons"].items():
        rows.append([lab, v["claims"], "${:,}".format(v["amount"])])
    s += [_table(rows, [30 * mm, 30 * mm, 34 * mm], last_bold=False),
          Paragraph("Paid claims from the finance ledger by the season each claim is for; duplicate lodgements that "
                    "were assessed but never paid are left out.", D.S_META)]
    frame = D._frame("Weather desk", "Quote HC104/2027", "Southward Mutual | Merrin Valley heat-day cover 2027/28", "Sans")
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


def write_payouts(path, fig):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["season", "claims_paid", "paid_dollars"])
        for lab, v in fig["seasons"].items():
            w.writerow([lab, v["claims"], v["amount"]])
