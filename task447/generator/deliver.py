"""The golden deliverable: N25-014_preliminary_review.pdf, the office's preliminary review sent to the
Attorney General, with the determination, the projected increase and its parts charted against the
threshold, and the two standing exhibits. Every figure comes from golden.compute (the shipped files).
"""
import io
import os
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

OUT = "N25-014_preliminary_review.pdf"
SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["BodyText"], fontName="Times-Roman", fontSize=10.5, leading=13.4, spaceAfter=5)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8.5, leading=10.5)
HEAD = ParagraphStyle("h", parent=BODY, fontName="Times-Bold", fontSize=12.5, leading=15, spaceAfter=1)
SEC = ParagraphStyle("c", parent=BODY, fontName="Times-Bold", fontSize=10.5, spaceBefore=6, spaceAfter=2)
CELL = ParagraphStyle("t", parent=BODY, fontName="Helvetica", fontSize=8.2, leading=10, spaceAfter=0)
CELLB = ParagraphStyle("tb", parent=CELL, fontName="Helvetica-Bold")

PARTS = [("P", "Professional prices"), ("IMG", "Referred imaging"), ("ECHO", "Referred echocardiography"),
         ("ENDO", "Referred endoscopy"), ("ARTH", "Referred arthroscopy"), ("LAB", "Referred laboratory")]


def r10k(x):
    return int(round(x / 10000.0)) * 10000


def money10k(x):
    return "${:,.0f}".format(r10k(x))


def figures(g):
    """The graded figures at the prompt's rounding, shared with submission.md."""
    parts = {"P": g["P"]}
    parts.update(g["fam"])
    return {
        "call": g["call"],
        "total_m": "%.1f" % (g["total"] / 1e6),
        "parts": {k: r10k(v) for k, v in parts.items()},
        "shares": {"%s|%s" % k: ("%.1f" % v[0], "%.1f" % v[1]) for k, v in g["shares"].items()},
        "counts": {str(k): v for k, v in g["counts"].items()},
        "joined": {str(k): v for k, v in g["joined"].items()},
    }


def chart(g):
    with matplotlib.rc_context({"font.family": "Carlito"}):
        return _chart(g)


def _chart(g):
    parts = [("Professional prices", g["P"])] + [(lab, g["fam"][k]) for k, lab in PARTS[1:]]
    fig, ax = plt.subplots(figsize=(6.6, 3.0), dpi=150)
    left = 0.0
    shades = ["#4d4d4d", "#1f4e79", "#2e75b6", "#5b9bd5", "#9dc3e6", "#c9ddf0"]
    for (lab, v), col in zip(parts, shades):
        ax.barh([0], [v / 1e6], left=[left], color=col, edgecolor="white", height=0.5)
        if v / 1e6 >= 0.35:
            short = "Professional" if lab.startswith("Professional") else lab.replace("Referred ", "").capitalize()
            ax.text(left + v / 2e6, 0, "%s\n\\$%.2fM" % (short, round(v / 1e4) / 100), ha="center", va="center",
                    fontsize=7, color="white")
        left += v / 1e6
    ax.axvline(2.0, color="#c00000", linestyle="--", linewidth=1.3)
    ax.text(1.98, 0.42, "Review threshold \\$2.0M", color="#c00000", fontsize=7.5, ha="right", va="bottom")
    ax.text(left + 0.03, 0, "Total \\$%.1fM" % (g["total"] / 1e6), fontsize=8, ha="left", va="center",
            fontweight="bold")
    ax.set_xlim(0, 2.6)
    ax.set_ylim(-0.6, 0.65)
    ax.set_yticks([])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, p: "\\$%.1fM" % x))
    ax.tick_params(axis="x", labelsize=7.5)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.set_title("Notice N25-014 adds \\$%.1fM to 2026 commercial spending, above the \\$2.0M review threshold"
                 % (g["total"] / 1e6), fontsize=9.5, loc="left")
    ax.set_xlabel("Projected increase in 2026 commercial allowed amounts (\\$ millions)", fontsize=7.5)
    handles = [matplotlib.patches.Patch(color=c, label=l) for (l, _), c in zip(parts, shades)]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize=6.8, frameon=False)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return buf


def _table(rows, widths, bold_last=False):
    data = [[Paragraph(str(c), CELLB if i == 0 or (bold_last and i == len(rows) - 1) else CELL) for c in r]
            for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black),
                           ("LINEABOVE", (0, 0), (-1, 0), 0.6, colors.black),
                           ("LINEBELOW", (0, -1), (-1, -1), 0.6, colors.black),
                           ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("TOPPADDING", (0, 0), (-1, -1), 1.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6)]))
    return t


def write(g, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUT)
    F = figures(g)
    P = lambda t: Paragraph(t, BODY)
    flow = [Paragraph("Office of Health Care Cost Review, Market Oversight Unit", SMALL),
            Paragraph("Notice N25-014 goes to a cost and market impact review" if F["call"] == "proceed" else
                      "Notice N25-014: preliminary review closed", HEAD),
            Spacer(1, 4),
            _table([("Preliminary review", "Notice N25-014"),
                    ("To", "Health Care Division, Office of the Attorney General"),
                    ("From", "Director of Market Oversight"),
                    ("Parties", "Ledgestone Health (acquiring); Brightwater Medical Group, S.C. (target)"),
                    ("Notice complete", "8 October 2025; review closes 7 November 2025"),
                    ("Date", "24 October 2025")], [1.5 * inch, 5.0 * inch]),
            Spacer(1, 8),
            Paragraph("Determination: the office proceeds to a cost and market impact review of notice N25-014." if
                      F["call"] == "proceed" else "Determination: the office closes the preliminary review.", SEC),
            P("Ledgestone Health's purchase of Brightwater Medical Group will raise commercial health care spending by "
              "<b>$%s million</b> in 2026, its first full year, against the $2.0 million threshold in rule OHCCR 4.06. "
              "The increase has two parts: Brightwater's professional services move to Ledgestone Medical Group's fee "
              "schedules, and the outpatient services Brightwater's physicians order move into Ledgestone's hospital "
              "outpatient departments." % F["total_m"])]
    rows = [("Projected 2026 increase", "Amount")]
    for k, lab in PARTS:
        rows.append((lab, money10k(g["P"] if k == "P" else g["fam"][k])))
    rows.append(("Total", "$%s million" % F["total_m"]))
    flow += [_table(rows, [3.6 * inch, 1.6 * inch], bold_last=True),
             Paragraph("Source: APCD extract OHCCR-MO-2025-031 and notice N25-014 Exhibit C, under OHCCR 4.03 to 4.05. "
                       "Parts are rounded to the nearest $10,000 and the total to $0.1 million; the parts are summed "
                       "before rounding.", SMALL),
             Spacer(1, 6),
             Image(chart(g), width=6.4 * inch, height=3.0 * inch), Spacer(1, 4)]
    flow += [Paragraph("Basis", SEC),
             P("Baseline: Brightwater's 2024 commercial services paid by 30 June 2025, being the professional "
               "services billed under its taxpayer number and the outpatient facility services its eighteen "
               "physicians referred (OHCCR 4.03). Professional services are repriced at Ledgestone Medical Group's "
               "schedules in Exhibit C. A referred service Ledgestone offers that went elsewhere in 2024 moves to "
               "Ledgestone in the expected share and is repriced at Ledgestone's filed rate.<super>1</super>"),
             P("Expected share (OHCCR 4.05): the practices Ledgestone and Wolf River acquired in 2021 to 2023 show "
               "the same result in every practice. Where the patient's plan places the acquiring system in its first "
               "tier, or has no tiers, 86 per cent of the referrals that used to go elsewhere moved to the acquirer; "
               "where the plan places it in the second tier, none moved. Norbridge's Tiered EPO patients at Wolf "
               "River's practices stayed while the plan kept Wolf River in its second tier and moved once it placed "
               "Wolf River first in plan year 2024. Shares pooled, by carrier or by product miss that year by eight "
               "points or more. Bayfield's Value Tier PPO, the commonest plan among Brightwater's patients, "
               "kept Ledgestone in its second tier through 2024 and places it in the first tier from plan year "
               "2025, so in 2026 those patients' referrals move as well. Only Cedarbrook Choice and Norbridge "
               "Tiered EPO patients, whose plans keep Ledgestone in the second tier, stay where they are.")]
    ex1 = [("Ledgestone share of commercial outpatient services, by residence", "2024",
            "After Brightwater's referrals move")]
    names = {"IMG": "imaging", "ENDO": "endoscopy", "ARTH": "arthroscopy"}
    for county in ("Manitowoc", "Kewaunee"):
        for f in ("IMG", "ENDO", "ARTH"):
            a, b = F["shares"]["%s|%s" % (county, f)]
            ex1.append(("%s County residents, %s" % (county, names[f]), "%s%%" % a, "%s%%" % b))
    ex2 = [("Ledgestone Health physicians", "On 1 January", "Joined by acquisition during the year")]
    for y in range(2020, 2026):
        ex2.append((str(y), str(F["counts"][str(y)]), str(F["joined"][str(y)]) if y <= 2024 else ""))
    flow += [KeepTogether([Paragraph("Exhibit 1. Ledgestone's outpatient market share", SEC),
                           _table(ex1, [3.6 * inch, 0.9 * inch, 1.9 * inch]),
                           Paragraph("Appendix A2 and A3: services counted in units on the latest claim version, net "
                                     "of voids; residence on the date of service; 2024 dates of service paid by 30 "
                                     "June 2025.", SMALL)]),
             KeepTogether([Paragraph("Exhibit 2. Ledgestone Health's physicians", SEC),
                           _table(ex2, [2.2 * inch, 1.4 * inch, 2.8 * inch]),
                           Paragraph("Appendix A4 and A5: doctors of medicine and osteopathy billing under numbers "
                                     "Ledgestone owns or controls, directly or through an entity it controls; "
                                     "acquisitions as physicians joining with their practice.", SMALL)]),
             Spacer(1, 8),
             Paragraph("<super>1</super> Bayfield pays Ledgestone a percent of the CY2025 Medicare amount by service "
                       "category under its 2025 agreement (Exhibit C, sheet Bayfield terms); Ledgestone's 2024 Bayfield "
                       "claims were paid under the earlier agreement and are not used to price the projection.", SMALL),
             Spacer(1, 4),
             Paragraph("Data: Wisconsin APCD extract OHCCR-MO-2025-031 (run 15 September 2025); provider ownership "
                       "register; NPI reassignment history; carrier tier placement filings 2020 to 2026; notice "
                       "N25-014 and Exhibit C.", SMALL)]
    doc = SimpleDocTemplate(path, pagesize=LETTER, leftMargin=0.95 * inch, rightMargin=0.95 * inch,
                            topMargin=0.75 * inch, bottomMargin=0.75 * inch, title="Preliminary review N25-014",
                            author="Market Oversight Unit", subject="", creator="Microsoft Word",
                            producer="Microsoft: Print To PDF")
    def footer(canvas, doc_):
        canvas.saveState()
        canvas.setFont("Times-Roman", 8)
        canvas.drawString(0.95 * inch, 0.5 * inch, "OHCCR preliminary review, notice N25-014")
        canvas.drawRightString(LETTER[0] - 0.95 * inch, 0.5 * inch, "Page %d" % doc_.page)
        canvas.restoreState()
    doc.build(flow, onFirstPage=footer, onLaterPages=footer)
    b = open(path, "rb").read()

    def same(m, new):
        old = m.group(0)
        return new.ljust(len(old))[:len(old)]
    b = re.sub(rb"ReportLab Generated PDF document \(opensource\)", lambda m: same(m, b"Microsoft Print To PDF"), b)
    b = re.sub(rb"ReportLab generated PDF document -- digest \(opensource\)", lambda m: same(m, b"end"), b)
    b = re.sub(rb"\(anonymous\)", lambda m: same(m, b"(OHCCR)"), b)
    b = b.replace(b"D:20000101000000+00'00'", b"D:20251024163105-05'00'")
    b = re.sub(rb"(/ID\s*\[\s*)<[0-9A-Fa-f]{32}>(\s*)<[0-9A-Fa-f]{32}>",
               lambda m: m.group(1) + b"<5E2B90C47D13A8F61C0E4B92D7A3F186>" + m.group(2) +
               b"<5E2B90C47D13A8F61C0E4B92D7A3F186>", b)
    assert b"ReportLab" not in b and b"reportlab" not in b
    open(path, "wb").write(b)
    return path, F
