"""task146 architecture 2: the golden deliverables (the Board paper with its chart, and the ladder workbook)."""
import datetime as dt
import io
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import golden as G  # noqa: E402

PAPER = "structural_hedge_reset_2027.pdf"
LADDER = "stable_balance_ladder_2026-11.xlsx"


def m(x):
    return int(round(x / 1e6))


def _chart(res):
    st = res["golden"]["stable"]
    xs = ["Nov 2027", "Nov 2028", "Nov 2029"]
    stable = [st[k]["total"] / 1e6 for k in G.HORIZONS]
    new = res["hedge"] - res["after_january"]
    out = [(res["after_january"] + new) / 1e6, (res["after_january"] - 49_500_000 + new) / 1e6, new / 1e6]
    fig, ax = plt.subplots(figsize=(6.4, 3.0), dpi=150)
    ax.bar([i - 0.18 for i in range(3)], stable, width=0.36, color="#2F5D8A", label="Stable balance")
    ax.bar([i + 0.18 for i in range(3)], out, width=0.36, color="#B9C7D6", label="Swaps outstanding after the reset")
    for i, (a, b) in enumerate(zip(stable, out)):
        ax.text(i - 0.18, a + 2, "%d" % round(a), ha="center", fontsize=7.5)
        ax.text(i + 0.18, b + 2, "%d" % round(b), ha="center", fontsize=7.5)
    ax.set_xticks(range(3))
    ax.set_xticklabels(xs, fontsize=8)
    ax.set_ylabel("GBP million", fontsize=8)
    ax.tick_params(axis="y", labelsize=7.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(fontsize=7.5, frameon=False, loc="upper right")
    ax.set_title("Instant-access stable balance against the hedge, 30 November 2026", fontsize=8.5)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return buf


def paper(res, path):
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.2, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13, leading=16)
    cell = ParagraphStyle("c", fontName="Helvetica", fontSize=8.2, leading=10)
    g = res["golden"]
    new = res["hedge"] - res["after_january"]
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title="Structural hedge reset, January 2027", author="Treasury",
                            creator="Treasury", subject="Board paper", invariant=1)
    s = [Paragraph("Board, 26 January 2027 | Item 6 | Structural hedge reset", ParagraphStyle(
        "s", parent=body, fontSize=8, textColor=colors.HexColor("#555555"))),
         Paragraph("Structural hedge reset: set the hedge at GBP %d million" % m(res["hedge"]), h1),
         Paragraph("<b>Recommendation.</b> Set the hedge at GBP %d million and replace the GBP 51 million swap "
                   "maturing on 29 January 2027 with a new three-year receive-fixed swap of GBP %d million, maturing "
                   "in January 2030. The swaps outstanding then stand at the hedge." % (m(res["hedge"]), m(new)), body),
         Paragraph("Of the GBP %d million held in instant-access savings on 30 November 2026, the Society expects "
                   "to keep GBP %d million a year on, GBP %d million two years on and GBP %d million three years on. "
                   "Members moving to each spring's Loyalty Saver issue close one account and open another on the "
                   "same day for the same amount; that money stays in instant-access savings and is counted as kept "
                   "(section 7.3)." % (m(g["book"]), m(g["stable"][12]["total"]), m(g["stable"][24]["total"]),
                                       m(g["stable"][36]["total"])), body),
         Spacer(1, 4), Image(_chart(res), width=165 * mm, height=77 * mm), Spacer(1, 4)]
    rows = [["Product", "Balance 30 Nov 2026", "Stable, Nov 2027", "Stable, Nov 2028", "Stable, Nov 2029"]]
    for f in G.FAMILIES:
        rows.append([f, m(g["now"][f])] + [m(g["stable"][k][f]) for k in G.HORIZONS])
    rows.append(["Instant-access savings", m(g["book"])] + [m(g["stable"][k]["total"]) for k in G.HORIZONS])
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=[50 * mm, 30 * mm, 30 * mm, 30 * mm, 30 * mm])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E3E8EF"))]))
    s += [t, Spacer(1, 5), Paragraph("GBP million. After the reset the swaps outstanding at the second and third "
                                     "anniversaries are GBP %d million and GBP %d million, within the stable balance "
                                     "at each (section 7.4)." % (m(res["after_january"] - 49_500_000 + new), m(new)), body)]
    doc.build(s)


def ladder(res, path):
    g = res["golden"]
    wb = Workbook()
    ws = wb.active
    ws.title = "Ladder"
    ws.append(["Instant-access stable balance, measured 30 November 2026 (GBP million)"])
    ws.append([])
    ws.append(["Product", "Balance 30 Nov 2026", "Stable 30 Nov 2027", "Stable 30 Nov 2028", "Stable 30 Nov 2029"])
    for f in G.FAMILIES:
        ws.append([f, m(g["now"][f])] + [m(g["stable"][k][f]) for k in G.HORIZONS])
    ws.append(["Instant-access savings", m(g["book"])] + [m(g["stable"][k]["total"]) for k in G.HORIZONS])
    ws.column_dimensions["A"].width = 26
    for c in "BCDE":
        ws.column_dimensions[c].width = 19
    wb.properties.creator = "Liam Bowen"
    wb.properties.created = dt.datetime(2026, 12, 9, 14, 6)
    wb.properties.modified = dt.datetime(2026, 12, 16, 11, 41)
    wb.save(path)
    import pack as PK
    PK.normalize_xlsx(path, (2026, 12, 16, 11, 41, 0))


def goldens(target, out):
    os.makedirs(out, exist_ok=True)
    D = G.load(target)
    res = G.call(D)
    paper(res, os.path.join(out, PAPER))
    ladder(res, os.path.join(out, LADDER))
    res["D"] = D
    return res
