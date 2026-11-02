"""The golden deliverables, written from analysis results (figures read from the pack only)."""
import os, csv, io
import numpy as np


def write_list(path, res, pk):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["tank", "marina", "product", "capacity_gal", "misstates_most_between"])
        for tid in res["golden_list"]:
            g = pk.reg[tid]
            w.writerow([tid, g["marina"], g["product"], g["cap"], res["tanks"][tid]["gold_pair"]])


def chart_png(res, pk):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    matplotlib.rcParams["svg.hashsalt"] = "task248"
    tids = res["golden_list"]
    lo = [res["tanks"][t]["gold"][0] for t in tids]
    up = [res["tanks"][t]["gold"][1] for t in tids]
    x = np.arange(len(tids))
    fig, ax = plt.subplots(figsize=(6.6, 3.1), dpi=150)
    ax.bar(x - 0.19, lo, 0.38, label="Reorder to half-full", color="#3b6ea5")
    ax.bar(x + 0.19, up, 0.38, label="Half-full to normal fill", color="#d08c2b")
    ax.axhline(25, color="#7a7a7a", lw=0.8, ls="--"); ax.axhline(-25, color="#7a7a7a", lw=0.8, ls="--")
    ax.axhline(0, color="black", lw=0.6)
    ax.set_xticks(x); ax.set_xticklabels(tids, fontsize=8)
    ax.set_ylabel("Chart misstatement (gal, net 60 F)", fontsize=8)
    ax.tick_params(axis="y", labelsize=8)
    ax.set_title("Listed tanks: chart misstatement over each half of the working range, 2026 season", fontsize=8.5)
    ax.legend(fontsize=7, frameon=False, loc="lower left")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def write_pdf(path, res, pk):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.lib import colors
    from reportlab import rl_config
    rl_config.invariant = 1
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9, leading=12, spaceAfter=4)
    h = ParagraphStyle("h", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=10, leading=13, spaceBefore=6, spaceAfter=3)
    tt = ParagraphStyle("t", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=12, leading=15, spaceAfter=4)
    n = len(res["golden_list"])
    story = [Paragraph("Wetstock service cutover: chart re-charting list and readiness, January 2027", tt),
             Paragraph("Prepared for the Director of Marina Operations, 12 January 2027.", body),
             Paragraph("<b>%d tanks need their charts redone before 1 April 2027:</b> %s. Each misstates the change in stock by more than 25 gallons between two of its reorder, half-full and normal fill heights (FS-3 section 3.4), read from the 2026 season." % (n, ", ".join(res["golden_list"])), body)]
    png = chart_png(res, pk)
    story.append(Image(io.BytesIO(png), width=468, height=220))
    story.append(Paragraph("Read from the gauge's net change between readings against the dock gallons sold in each interval, with the proportional part carried from the deliveries against their bills of lading.", body))
    TS = TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8),
                     ("GRID", (0, 0), (-1, -1), 0.3, colors.grey), ("ALIGN", (1, 1), (-1, -1), "RIGHT")])
    story.append(Paragraph("Gauge feed: days of 2026 with no inventory reading", h))
    rows = [["Tank", "Days"]] + [[t, res["A1"][t]] for t in sorted(res["A1"])]
    half = (len(rows) + 1) // 2
    tb = Table([r1 + r2 for r1, r2 in zip(rows[:half], rows[half:] + [["", ""]] * (2 * half - len(rows)))] if False else rows, hAlign="LEFT")
    tb.setStyle(TS); story.append(tb)
    story.append(Paragraph("Release detection: tank-months of 2026 without a passing 0.2 gal/h test", h))
    rows = [["Marina", "Tank-months"]] + [[m, res["A2"][m]] for m in sorted(res["A2"])]
    tb = Table(rows, hAlign="LEFT"); tb.setStyle(TS); story.append(tb)
    story.append(Paragraph("Dock gallons sold in 2026 by product", h))
    prods = ["REC-90 ethanol-free", "E10 unleaded", "Diesel"]
    marinas = sorted({k.split("|")[0] for k in res["A3"]})
    rows = [["Marina"] + prods]
    for m in marinas:
        rows.append([m] + ["{:,}".format(int(round(res["A3"]["%s|%s" % (m, p)]))) if "%s|%s" % (m, p) in res["A3"] else "-" for p in prods])
    tb = Table(rows, hAlign="LEFT"); tb.setStyle(TS); story.append(tb)
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=48, bottomMargin=48,
                            title="Wetstock service cutover, January 2027", author="Fuel Systems and Compliance",
                            subject="", creator="Fuel Systems and Compliance", producer="Fuel Systems and Compliance")
    doc.build(story)


def write(golden_dir, res, pk):
    os.makedirs(golden_dir, exist_ok=True)
    write_list(os.path.join(golden_dir, "recharting_list_2027.csv"), res, pk)
    write_pdf(os.path.join(golden_dir, "cutover_readiness_2027.pdf"), res, pk)
