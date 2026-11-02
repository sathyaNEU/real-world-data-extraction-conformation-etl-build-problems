"""task459 golden deliverables: member_regions_2025.csv and home_care_allocation_2027.pdf, from analysis.py's results."""
import csv
import datetime as dt
import io
import os
import re

import analysis as AN

ORG = "Pinyon Valley Health Plan"
AUTHOR = "Nicholas Castillo"
PAPER_DATE = dt.datetime(2026, 10, 16, 11, 20)
BLUE, INK, INK2, GRID = "#2a78d6", "#0b0b0b", "#52514e", "#d9d8d4"


def results(target):
    """Every figure the goldens and the write-up state, computed once."""
    d = AN.load(target)
    call = AN.main_call(target)
    regions = d.regions
    agencies = [d.agency_of_region[r] for r in regions]
    a = AN.ask_a(target)
    b = AN.ask_b(target)
    c = AN.ask_c(target)
    return {
        "regions": regions, "agencies": agencies, "budget": d.budget,
        "counts": call["counts"], "alloc": call["alloc"], "member_region": call["regions"],
        "covered": sum(call["counts"].values()),
        "visits": a, "visits_total": {ag: sum(a[(ag, q)] for q in (1, 2, 3, 4)) for ag in agencies},
        "minutes": {ag: AN.m1(b[ag]) for ag in agencies},
        "spend_k": {r: AN.k1(c[r]) for r in regions},
    }


def write_member_csv(res, path):
    ag = dict(zip(res["regions"], res["agencies"]))
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["MEMBER_ID", "REGION_2025", "AGENCY_2027"])
        for m in sorted(res["member_region"]):
            r = res["member_region"][m]
            w.writerow([m, r, ag[r]])


def chart_png(res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "svg.hashsalt": "task459",
                         "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK})
    order = sorted(range(len(res["regions"])), key=lambda i: res["alloc"][res["regions"][i]])
    labels = ["%s\n(%s)" % (res["agencies"][i], res["regions"][i]) for i in order]
    vals = [res["alloc"][res["regions"][i]] / 1e6 for i in order]
    fig, ax = plt.subplots(figsize=(6.6, 3.5), dpi=200)
    bars = ax.barh(range(len(vals)), vals, height=0.62, color=BLUE, edgecolor="white", linewidth=1.0)
    for i, (bar, i0) in enumerate(zip(bars, order)):
        r = res["regions"][i0]
        ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
                "USD {:,}  ({:,} members)".format(res["alloc"][r], res["counts"][r]),
                va="center", ha="left", fontsize=7.6, color=INK)
    ax.set_yticks(range(len(vals)))
    ax.set_yticklabels(labels, fontsize=7.4)
    ax.set_xlim(0, max(vals) * 1.78)
    ax.set_xticks([x for x in range(0, int(max(vals)) + 2)])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, p: "%.0f" % x if x else "0"))
    ax.set_xlabel("2027 allocation (USD millions)", fontsize=8)
    ax.grid(axis="x", color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    bio = io.BytesIO()
    fig.savefig(bio, format="png", metadata={"Software": None})
    plt.close(fig)
    bio.seek(0)
    return bio


def write_board_pdf(res, path):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    base = ParagraphStyle("b", fontName="Helvetica", fontSize=9.6, leading=13, spaceAfter=6, textColor=colors.HexColor(INK))
    small = ParagraphStyle("s", parent=base, fontSize=8, leading=10.2, textColor=colors.HexColor(INK2), spaceAfter=3)
    head = ParagraphStyle("h", parent=base, fontName="Helvetica-Bold", fontSize=10.4, spaceBefore=8, spaceAfter=4)
    title = ParagraphStyle("t", parent=base, fontName="Helvetica-Bold", fontSize=13, leading=16.5, spaceAfter=6)
    rg, ag = res["regions"], res["agencies"]

    def tstyle(right_from=2, total=True):
        cmds = [("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.2), ("FONT", (0, 1), (-1, -1), "Helvetica", 8.2),
                ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor(INK)),
                ("ALIGN", (right_from, 0), (-1, -1), "RIGHT"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5), ("TOPPADDING", (0, 0), (-1, -1), 2.5)]
        if total:
            cmds += [("LINEABOVE", (0, -1), (-1, -1), 0.4, colors.HexColor(INK2)), ("FONT", (0, -1), (-1, -1), "Helvetica-Bold", 8.2)]
        return TableStyle(cmds)

    memo = Table([["To", "Board of Directors"], ["From", "%s, Director of Provider Contracting and Payment" % AUTHOR],
                  ["Date", "16 October 2026, for the meeting of 28 October 2026"],
                  ["Subject", "2027 in-home support allocations under Schedule B"]], colWidths=[0.8 * inch, 5.7 * inch],
                 hAlign="LEFT")
    memo.setStyle(TableStyle([("FONT", (0, 0), (0, -1), "Helvetica-Bold", 8.6), ("FONT", (1, 0), (1, -1), "Helvetica", 8.6),
                              ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor(INK)), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
                              ("LINEBELOW", (0, -1), (-1, -1), 0.6, colors.HexColor(INK))]))
    story = [Paragraph("PINYON VALLEY HEALTH PLAN  |  BOARD PAPER, AGENDA ITEM 6", small), memo, Spacer(1, 8),
             Paragraph("The 2027 in-home support budget follows where Covered Members lived in 2025", title),
             Paragraph("Schedule B divides the 2027 Budget of USD {:,} among the Agencies in proportion to the Covered "
                       "Members counted in each Region. {:,} Senior Choice members were enrolled on every day of 2025 and "
                       "were 75 or over on 31 December 2025. Each is counted once, in the Region where the Plan's 2025 "
                       "records place the member on the most days. These are the amounts I recommend the Board approve for "
                       "the 2027 agreements.".format(res["budget"], res["covered"]), base),
             Paragraph("A member's Region comes from the dated places in the Plan's own 2025 claims: each in-person medical "
                       "service at the rendering practice's location on the date of service, each fill at an Arizona retail "
                       "pharmacy and each visit by a Region's in-home support Agency. Every day of 2025 takes the place of "
                       "the nearest dated service, and the member counts in the Region holding the most days. The address on "
                       "file and the assigned primary care practice stay at the home that members who winter in the low "
                       "desert leave from October to May, and those members see their regular doctors, specialists and "
                       "laboratories during the summer months at home, so neither the address nor a count of claims shows "
                       "where they spent most of the year.", base)]
    rows = [["Region", "Agency", "Covered Members", "2027 Allocation (USD)"]]
    for r, a in zip(rg, ag):
        rows.append([r, a, "{:,}".format(res["counts"][r]), "{:,}".format(res["alloc"][r])])
    rows.append(["Total", "", "{:,}".format(res["covered"]), "{:,}".format(sum(res["alloc"].values()))])
    t = Table(rows, colWidths=[1.15 * inch, 2.95 * inch, 1.05 * inch, 1.35 * inch], hAlign="LEFT")
    t.setStyle(tstyle())
    story += [Spacer(1, 2), t,
              Paragraph("Allocation: the 2027 Budget times the Region's Covered Members over all Covered Members, rounded "
                        "to the nearest dollar (Schedule B, B.5). Source: membership snapshot of 2 January 2026; medical "
                        "claims for 2025 services paid through 30 June 2026; PBM and in-home support claims for 2025.", small),
              Spacer(1, 4), Image(chart_png(res), width=6.5 * inch, height=6.5 * inch * 3.5 / 6.6),
              Paragraph("Figure 1. 2027 allocation by Agency, with the Covered Members counted in its Region.", small)]
    # younger members
    story.append(Paragraph("Members aged 65 to 74: in-home support and medical spend in 2025", head))
    story.append(Paragraph("The Board asked for the 2025 use of members aged 65 to 74 on 31 December 2025, who are outside "
                           "the 2027 Budget. A Visit is one continuous attendance (Schedule B, B.7): an attendance longer than "
                           "four hours is billed on consecutive claims and counts once, replacement claims take the place of "
                           "the claims they correct, and voided claims are left out.", base))
    vrows = [["Agency", "Q1", "Q2", "Q3", "Q4", "2025", "Avg. minutes"]]
    for a in ag:
        vrows.append([a] + ["{:,}".format(res["visits"][(a, q)]) for q in (1, 2, 3, 4)] +
                     ["{:,}".format(res["visits_total"][a]), "%.1f" % res["minutes"][a]])
    vt = Table(vrows, colWidths=[2.75 * inch, 0.55 * inch, 0.55 * inch, 0.55 * inch, 0.55 * inch, 0.65 * inch, 0.9 * inch],
               hAlign="LEFT")
    vt.setStyle(tstyle(1, total=False))
    story += [vt, Paragraph("Visits by calendar quarter of the date of service; average length from arrival to departure. "
                            "Source: in-home support claims for 2025, agencies by the provider directory.", small)]
    srows = [["Region of the rendering practice", "Plan-paid spend (USD thousands)"]]
    for r in rg:
        srows.append([r, "{:,.1f}".format(res["spend_k"][r])])
    st = Table(srows, colWidths=[2.75 * inch, 2.0 * inch], hAlign="LEFT")
    st.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.2), ("FONT", (0, 1), (-1, -1), "Helvetica", 8.2),
                            ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor(INK)), ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5), ("TOPPADDING", (0, 0), (-1, -1), 2.5)]))
    story += [Spacer(1, 6), KeepTogether([st, Paragraph(
        "Plan-paid amount on medical claims for 2025 services, net of replacements and voids, by the Region of the "
        "rendering practice's location on the date of service (provider directory and 2025 location changes). The "
        "reference laboratory's claims fall in Maricopa, where it bills from.", small)])]

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.2)
        canvas.setFillColor(colors.HexColor(INK2))
        canvas.drawString(inch, 0.55 * inch, "Pinyon Valley Health Plan  |  Board of Directors, 28 October 2026  |  Agenda item 6")
        canvas.drawRightString(7.5 * inch, 0.55 * inch, "Page %d" % doc.page)
        canvas.restoreState()

    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=inch, rightMargin=inch, topMargin=0.75 * inch,
                            bottomMargin=0.85 * inch, title="2027 in-home support allocations under Schedule B",
                            author=AUTHOR, subject="Board paper, agenda item 6", creator=ORG,
                            producer=ORG + " document services", invariant=1)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    import pack as P
    P.finish_pdf(path, PAPER_DATE - dt.timedelta(minutes=40), PAPER_DATE)


def write_goldens(target, out_dir):
    res = results(target)
    write_member_csv(res, os.path.join(out_dir, "member_regions_2025.csv"))
    write_board_pdf(res, os.path.join(out_dir, "home_care_allocation_2027.pdf"))
    return res
