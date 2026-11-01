"""The golden deliverables, computed from target/ alone through analysis.py, and the figure set F."""
import os

import analysis as A
from common import pdf_setup, save_workbook

ORDER_TYPES = ["ALBERGO", "CAMPEGGIO", "CASA VACANZE", "BED AND BREAKFAST", "AGRITURISMO", "AFFITTACAMERE"]


def r100(x):
    return int(round(x / 100.0)) * 100


def compute(target):
    p = A.load(target)
    res = A.main_call(p)
    F = {"comuni": []}
    for c in sorted(res, key=lambda c: -res[c]["golden"] / res[c]["residents"]):
        r = res[c]
        npr = r["golden"] / r["residents"]
        F["comuni"].append(dict(code=c, name=r["name"], residents=r["residents"], nights=r["golden"],
                                nights_r=r100(r["golden"]), npr=npr, npr_r=round(npr, 1), qualifies=npr >= A.THRESHOLD,
                                declared_q3=r["declared_q3"], jul=r["jul"], sep=r["sep"], reported=r["reported"],
                                missing=r["missing_returns"], filled_ct=r["R1_ct"], r2_ct=r["R2_ct"]))
    F["qualifying"] = [x["name"] for x in F["comuni"] if x["qualifies"]]
    near = min(F["comuni"], key=lambda x: abs(x["npr"] - A.THRESHOLD))
    F["nearest"] = dict(name=near["name"], npr_r=near["npr_r"], gap=round(near["npr"] - A.THRESHOLD, 1))
    ja = A.ask_jan_apr(p, "cir")
    names = {x["code"]: x["name"] for x in F["comuni"]}
    F["janapr"] = [dict(code=c, name=names[c], nights=ja[c], nights_r=r100(ja[c])) for c in sorted(ja)]
    occ = A.ask_oct_occupancy(p)
    F["occupancy"] = [dict(type=t, pct=occ[t], pct_r=round(occ[t], 1)) for t in ORDER_TYPES]
    tax = A.ask_tax_2025(p)
    F["tax"] = [dict(q=q, eur=tax[q], eur_r=r100(tax[q])) for q in (1, 2, 3, 4)]
    F["residents_total"] = sum(x["residents"] for x in F["comuni"])
    F["_pack"] = p
    F["_res"] = res
    return F


def chart(F, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rows = list(reversed(F["comuni"]))
    fig, ax = plt.subplots(figsize=(7.2, 6.0), dpi=110)
    colors = ["#1f5f8b" if x["qualifies"] else "#9db4c8" for x in rows]
    ax.barh([x["name"] for x in rows], [x["npr"] for x in rows], color=colors, height=.68)
    ax.axvline(30, color="#b03a2e", lw=1.4, ls="--")
    ax.text(30.6, -0.9, "30 nights per resident", color="#b03a2e", fontsize=8, va="bottom")
    for i, x in enumerate(rows):
        ax.text(x["npr"] + 0.6, i, "%.1f" % x["npr_r"], va="center", fontsize=7.5)
    ax.set_xlabel("Guest nights in August 2026 per resident on 1 January 2026")
    ax.set_title("Three comuni reach the 30-night line in August 2026", fontsize=10.5, loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="y", labelsize=8)
    ax.set_xlim(0, max(x["npr"] for x in rows) * 1.12)
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def workbook(F, path):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "August 2026"
    ws.append(["Peak-month services co-financing 2027: August 2026 guest nights by member comune"])
    ws["A1"].font = Font(bold=True)
    ws.append(["Residents from the ISTAT balance at 1 January 2026; nights for every guest, liable to the tourist tax or exempt"])
    ws.append([])
    ws.append(["Comune", "ISTAT code", "Residents 1 Jan 2026", "Guest nights August 2026", "Nights per resident",
               "Qualifies (30 or more)"])
    for c in ws[4]:
        c.font = Font(bold=True)
    for x in F["comuni"]:
        ws.append([x["name"], x["code"], x["residents"], x["nights_r"], x["npr_r"], "Yes" if x["qualifies"] else "No"])
    ws.append([])
    ws.append(["Qualifying comuni", ", ".join(F["qualifying"])])
    ws.append(["Closest to the line", "%s, %.1f nights per resident (%+.1f)" % (F["nearest"]["name"], F["nearest"]["npr_r"],
                                                                                F["nearest"]["gap"])])
    for col, wdt in zip("ABCDEF", (24, 11, 19, 23, 19, 21)):
        ws.column_dimensions[col].width = wdt
    w2 = wb.create_sheet("Jan-Apr 2026")
    w2.append(["Guest nights reported for January to April 2026 by member comune (2026 boundaries)"])
    w2["A1"].font = Font(bold=True)
    w2.append([])
    w2.append(["Comune", "ISTAT code", "Guest nights Jan-Apr 2026"])
    for x in F["janapr"]:
        w2.append([x["name"], x["code"], x["nights_r"]])
    w2.column_dimensions["A"].width = 24
    w2.column_dimensions["C"].width = 24
    w3 = wb.create_sheet("Occupancy Oct 2025")
    w3.append(["Net bed-place occupancy, October 2025, establishments on the regional register"])
    w3["A1"].font = Font(bold=True)
    w3.append([])
    w3.append(["Type of establishment", "Net bed-place occupancy (%)"])
    for x in F["occupancy"]:
        w3.append([x["type"], x["pct_r"]])
    w3.column_dimensions["A"].width = 24
    w3.column_dimensions["B"].width = 26
    w4 = wb.create_sheet("Tourist tax 2025")
    w4.append(["Tourist tax due to the member comuni, 2025, by quarter (EUR)"])
    w4["A1"].font = Font(bold=True)
    w4.append([])
    w4.append(["Quarter", "Tax due (EUR)"])
    for x in F["tax"]:
        w4.append(["Q%d 2025" % x["q"], x["eur_r"]])
    w4.column_dimensions["A"].width = 14
    w4.column_dimensions["B"].width = 16
    save_workbook(wb, path, creator="Ufficio di piano dei servizi associati")


def note(F, path, png):
    pdf_setup()
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer
    st = getSampleStyleSheet()
    doc = SimpleDocTemplate(path, pagesize=A4, title="Peak-month co-financing 2027",
                            author="Ufficio di piano dei servizi associati", leftMargin=2.2 * cm, rightMargin=2.2 * cm,
                            topMargin=1.8 * cm, bottomMargin=1.8 * cm)
    q = F["comuni"]
    qual = [x for x in q if x["qualifies"]]
    lines = "; ".join("%s %.1f" % (x["name"], x["npr_r"]) for x in qual)
    el = [Paragraph("Peak-month services co-financing 2027: qualifying comuni", st["Title"]),
          Paragraph("To the Assembly of the Union, 20 November 2026. From the peak services planning office.", st["Normal"]),
          Spacer(1, 8),
          Paragraph("<b>Decision.</b> %d member comuni qualify, each with at least 30 guest nights in August 2026 per "
                    "resident at 1 January 2026: %s (nights per resident). %s is the comune closest to the line, "
                    "%.1f nights per resident against 30." % (len(qual), lines, F["nearest"]["name"], F["nearest"]["npr_r"]),
                    st["Normal"]), Spacer(1, 6),
          Paragraph("<b>Basis.</b> The July to September 2026 tourist-tax declarations count every night each comune's "
                    "establishments hosted that quarter. The region's July and September returns are complete and agree "
                    "with them, so a comune's August is its declared quarter less its July and September; the August "
                    "returns that never reached the region belong to the busiest holiday houses, and filling them at the "
                    "occupancy of the houses that did report would leave Marina di Cervessa below the line.", st["Normal"]),
          Spacer(1, 8), Image(png, width=15.2 * cm, height=12.7 * cm), Spacer(1, 6),
          Paragraph("Collebruno, San Gaudenzio and Fontecupa levy no tourist tax; their establishments filed every "
                    "August return and their figures are the returns as filed.", st["Normal"])]
    doc.build(el)


def build(target, gold_dir, scratch):
    F = compute(target)
    os.makedirs(gold_dir, exist_ok=True)
    png = os.path.join(scratch, "chart.png")
    chart(F, png)
    workbook(F, os.path.join(gold_dir, "august_2026_guest_nights.xlsx"))
    note(F, os.path.join(gold_dir, "peak_cofinancing_2027_note.pdf"), png)
    return F
