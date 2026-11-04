"""salvage_marking_2027.pdf: the forestry manager's memo to the board, with the stand table and a chart of each
stand's 2021 to 2026 loss against the policy line. Every figure is read from figures.json's dictionary."""
import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                      # noqa: E402
from reportlab import rl_config                                      # noqa: E402
rl_config.invariant = 1
from reportlab.lib import colors                                     # noqa: E402
from reportlab.lib.pagesizes import letter                           # noqa: E402
from reportlab.lib.styles import ParagraphStyle                      # noqa: E402
from reportlab.lib.units import inch                                 # noqa: E402
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W   # noqa: E402

BODY = ParagraphStyle("b", fontName="Helvetica", fontSize=9.6, leading=12.6, spaceAfter=6)
NOTE = ParagraphStyle("n", fontName="Helvetica", fontSize=8.2, leading=10.4, spaceAfter=3,
                      textColor=colors.HexColor("#333333"))
HEAD = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=13, leading=16, spaceAfter=2)
META = ParagraphStyle("m", fontName="Helvetica", fontSize=9.2, leading=12)


def _chart(rows):
    rs = sorted(rows, key=lambda r: r["share"])
    fig, ax = plt.subplots(figsize=(6.4, 4.1), dpi=160)
    cols = ["#9b2c1f" if r["mark"] else "#7d8f69" for r in rs]
    ax.barh([r["stand"] for r in rs], [r["share"] for r in rs], color=cols, height=0.68)
    ax.axvline(15, color="#222222", lw=0.9, ls="--")
    ax.text(15.6, 0.2, "Policy 7.4 line, 15%", fontsize=7.5, color="#222222")
    for i, r in enumerate(rs):
        ax.text(r["share"] + 0.6, i, "%.1f" % r["share"], va="center", fontsize=6.6, color="#333333")
    ax.set_xlabel("Share of 2021 live basal area not tallied live in 2026 (%)", fontsize=8)
    ax.set_title("Three stands cross the Policy 7.4 line", fontsize=9.5, loc="left", fontweight="bold")
    ax.tick_params(axis="both", labelsize=7)
    ax.set_xlim(0, max(r["share"] for r in rs) * 1.12)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return buf


def write(path, d, g, rows, fig):
    treat = {r["stand_id"]: (r["last_treatment"] or "") for r in d["stands"]}
    mk = fig["marked"]
    sh = {r["stand"]: r for r in rows}
    burned = [s for s in W.BURN_DATES]
    b_lo = min(sh[s]["share"] for s in burned)
    b_hi = max(sh[s]["share"] for s in burned)
    t_lo = min(float(fig["tag_join_share_pct"][s]) for s in burned)
    t_hi = max(float(fig["tag_join_share_pct"][s]) for s in burned)
    rest = max(r["share"] for r in rows if not r["mark"])
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.85 * inch, rightMargin=0.85 * inch,
                            topMargin=0.7 * inch, bottomMargin=0.7 * inch, title="2027 salvage marking",
                            author=W.MANAGER, creator=W.COMPANY, producer=W.COMPANY, subject="Board Policy 7.4")
    order = sorted(mk, key=lambda s: -sh[s]["share"])
    names = "%s, %s and %s" % tuple(order) if len(order) == 3 else ", ".join(order)
    story = [Paragraph("Cinder Fork Timber Company", HEAD),
             Paragraph("Forestry Department", META), Spacer(1, 8),
             Table([["To:", "Board of Directors (N. Wolf, Chair)"], ["From:", "Tamara Larson, Forestry Manager"],
                    ["Date:", "November 4, 2026, for the December board meeting"],
                    ["Re:", "2027 salvage marking under Board Policy 7.4"]],
                   colWidths=[0.6 * inch, 5.6 * inch],
                   style=TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 9.2),
                                     ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 9.2),
                                     ("BOTTOMPADDING", (0, 0), (-1, -1), 1), ("TOPPADDING", (0, 0), (-1, -1), 1)])),
             Spacer(1, 10),
             Paragraph("<b>Mark %s for the 2027 salvage program.</b> They are the only stands where the trees tallied "
                       "live in 2021 and not tallied live in 2026 hold 15 per cent or more of the 2021 live basal "
                       "area: %s at %.1f per cent after the Juniper Saddle Fire, and %s at %.1f and %s at %.1f per "
                       "cent from bark beetle. No other stand is above %.1f per cent." % (
                           names, order[0], sh[order[0]]["share"], order[1], sh[order[1]]["share"], order[2],
                           sh[order[2]]["share"], rest), BODY),
             Paragraph("The five stands underburned in fall 2024 do not qualify. On their plots the contract crews "
                       "marked many tagged trees not found and tallied the same trees again under new tags, nearly "
                       "all of them trees the crews coded for bole char. Matched back to the 2021 stem map by position, species "
                       "and diameter, those trees are alive, and the five stands lost %.1f to %.1f per cent. Read on "
                       "tag numbers alone they would show %.1f to %.1f per cent and all five would be marked." % (
                           b_lo, b_hi, t_lo, t_hi), BODY),
             Image(_chart(rows), width=5.6 * inch, height=3.59 * inch),
             Paragraph("Figure 1. 2021 to 2026 loss by stand under Policy 7.4, section 2. Red bars are the stands "
                       "to mark.", NOTE),
             Spacer(1, 6)]
    head = ["Stand", "Acres", "Last treatment", "2021-26 loss\n(% of 2021 BA)", "2026 live BA\n(sq ft/ac)",
            "2026 net volume\n(bd ft/ac)", "Mark"]
    tab = [head]
    for r in rows:
        tab.append([r["stand"], "%d" % r["acres"], treat[r["stand"]] or "-", "%.1f" % r["share"], "%.1f" % r["ba"],
                    "{:,}".format(r["vol"]), "Yes" if r["mark"] else ""])
    t = Table(tab, colWidths=[0.62 * inch, 0.5 * inch, 2.05 * inch, 0.95 * inch, 0.85 * inch, 1.0 * inch, 0.45 * inch],
              repeatRows=1)
    style = [("FONT", (0, 0), (-1, -1), "Helvetica", 8), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 7.6),
             ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black), ("ALIGN", (1, 1), (1, -1), "RIGHT"),
             ("ALIGN", (3, 1), (5, -1), "RIGHT"), ("VALIGN", (0, 0), (-1, 0), "BOTTOM"),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5), ("TOPPADDING", (0, 0), (-1, -1), 1.5)]
    for i, r in enumerate(rows, start=1):
        if r["mark"]:
            style += [("FONT", (0, i), (-1, i), "Helvetica-Bold", 8),
                      ("BACKGROUND", (0, i), (-1, i), colors.HexColor("#f3e3df"))]
    t.setStyle(TableStyle(style))
    story += [Paragraph("<b>Stand table, 2021 and 2026 remeasurements</b>", BODY), t,
              Paragraph("Sources: CFI database, 2021 cycle; Tolan Ridge Forestry 2026 remeasurement export and "
                        "September height return; plot register of September 29, 2026; GIS stand table.", NOTE),
              Spacer(1, 6),
              Paragraph("Notes. Loss follows Policy 7.4: basal area at 2021 DBH of the trees tallied live in 2021 and "
                        "not tallied live in 2026 (cut trees excluded), over the plot conditions mapped to each stand. "
                        "%d trees the crews tallied as added were linked to 2021 trees marked not found; %d added "
                        "records duplicated a tree the crew had also entered under its found tag and are counted "
                        "once. Live basal area and volume are per acre of plot condition. Volume is net Scribner "
                        "Decimal C from Table 1 of the field manual, sawtimber conifers 11.0 inches and larger; heights "
                        "for plots measured July 20 to 24 are from the September revisit." % (
                            fig["retagged_linked"], fig["found_tag_duplicates"]), NOTE),
              Paragraph("Tree-level fates for all %s trees tallied live in 2021 are in tree_fates_2021_2026.csv. "
                        "cc: Brandon Freeman, Inventory Forester." % "{:,}".format(fig["trees_2021_live"]), NOTE)]
    doc.build(story)
