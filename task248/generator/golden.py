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


WORDS = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine"}


def _names(ts):
    return ", ".join(ts[:-1]) + " and " + ts[-1] if len(ts) > 1 else ts[0]


def groups(res):
    listed = res["golden_list"]
    mid = [t for t in listed if res["tanks"][t]["gold_pair"] == "reorder and half-full"]
    full = [t for t in listed if res["tanks"][t]["gold_pair"] == "reorder and normal fill"]
    return mid, full


def chart_png(res, pk):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    matplotlib.rcParams["svg.hashsalt"] = "task248"
    tids = res["golden_list"]
    lo = [res["tanks"][t]["gold"][0] for t in tids]
    up = [res["tanks"][t]["gold"][1] for t in tids]
    mid, full = groups(res)
    x = np.arange(len(tids))
    fig, ax = plt.subplots(figsize=(6.6, 3.2), dpi=150)
    ax.bar(x - 0.2, lo, 0.38, label="Reorder to half-full", color="#3b6ea5", edgecolor="white", linewidth=1.0)
    ax.bar(x + 0.2, up, 0.38, label="Half-full to normal fill", color="#b26a17", edgecolor="white", linewidth=1.0)
    for yv in (25, -25):
        ax.axhline(yv, color="#8a8a8a", lw=0.8, ls="--", zorder=0)
    ax.text(len(tids) - 0.45, 26.5, "25 gal limit (FS-3 3.4)", fontsize=6.5, color="#555555", ha="right", va="bottom")
    ax.axhline(0, color="#333333", lw=0.6)
    ax.set_xticks(x); ax.set_xticklabels(tids, fontsize=8)
    ax.set_ylabel("Gallons misstated (net, 60 F)", fontsize=7.5)
    ax.tick_params(axis="y", labelsize=7.5)
    ax.grid(axis="y", color="#e6e6e6", lw=0.5); ax.set_axisbelow(True)
    ax.set_title("%s misstate most from reorder to half-full; %s misstate in one direction over both halves"
                 % (_names(mid), _names(full)), fontsize=7.5, loc="left")
    ax.legend(fontsize=7, frameon=False, loc="lower left", ncol=2)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillGray(0.35)
    canvas.drawString(54, 30, "Highbank Marinas, Fuel Systems and UST Compliance")
    canvas.drawRightString(558, 30, "Page %d" % doc.page)
    canvas.restoreState()


def write_pdf(path, res, pk):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.lib import colors
    from reportlab import rl_config
    rl_config.invariant = 1
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9, leading=12, spaceAfter=5)
    small = ParagraphStyle("s", parent=body, fontSize=7, leading=9, textColor=colors.HexColor("#555555"), spaceAfter=8)
    head = ParagraphStyle("hd", parent=body, fontSize=8.5, leading=11, spaceAfter=0)
    h = ParagraphStyle("h", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=9.5, leading=12, spaceBefore=6, spaceAfter=3)
    tt = ParagraphStyle("t", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=12.5, leading=15, spaceBefore=8, spaceAfter=6)
    listed = res["golden_list"]
    n = len(listed)
    mid, full = groups(res)
    story = [Paragraph("<b>To:</b> Harold Mathis, Director of Marina Operations", head),
             Paragraph("<b>From:</b> Theresa Shelton, Fuel Systems and UST Compliance", head),
             Paragraph("<b>Date:</b> 12 January 2027", head),
             Paragraph("<b>Subject:</b> Winter re-charting list and wetstock cutover readiness", head),
             Paragraph("%s tank charts to redo before the 1 April start" % WORDS.get(n, str(n)), tt),
             Paragraph("<b>%d tanks need their charts redone before the service starts on 1 April 2027: %s.</b> Each "
                       "misstates the change in stock by more than 25 gallons between two of its reorder, half-full and "
                       "normal fill heights, read from the 2026 season (FS-3 section 3.4). %s misstate most through the "
                       "middle of the tank, from reorder to half-full, which a delivery never isolates because it runs "
                       "from about the reorder height to about full. %s misstate every gallon alike and are over the "
                       "limit across the whole working range, reorder to normal fill. The other %d tanks stay under the "
                       "limit between every pair of heights. The list goes to the calibration contractor for the winter "
                       "programme." % (n, _names(listed), _names(mid), _names(full), len(pk.reg) - n), body)]
    png = chart_png(res, pk)
    story.append(Image(io.BytesIO(png), width=468, height=227))
    story.append(Paragraph("Each tank's error read from the gauge's net change between two-hour readings against the dock "
                           "gallons its hoses metered, with the part proportional to volume carried from the 2026 "
                           "deliveries against their bills of lading, which no dock meter touches.", small))
    TS = TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8),
                     ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black), ("LINEBELOW", (0, -1), (-1, -1), 0.3, colors.grey),
                     ("ALIGN", (1, 1), (-1, -1), "RIGHT"), ("TOPPADDING", (0, 0), (-1, -1), 1.5),
                     ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)])
    story.append(Paragraph("Gauge feed: days of 2026 with no inventory reading", h))
    tanks = sorted(res["A1"])
    half = (len(tanks) + 1) // 2
    rows = [["Tank", "Days", "", "Tank", "Days"]]
    for i in range(half):
        a = tanks[i]
        b = tanks[i + half] if i + half < len(tanks) else None
        rows.append([a, res["A1"][a], "", b or "", res["A1"][b] if b else ""])
    tb = Table(rows, hAlign="LEFT", colWidths=[48, 40, 24, 48, 40])
    tb.setStyle(TS); story.append(tb)
    story.append(Paragraph("Local calendar days, as the Clearline onboarding letter of 3 December 2026 counts them. "
                           "Readings stamped 2016 after the 24 January storm are dated by each console's record sequence.",
                           small))
    story.append(Paragraph("Release detection: tank-months of 2026 without a passing 0.2 gal/h test", h))
    rows = [["Marina", "Tank-months"]] + [[m, res["A2"][m]] for m in sorted(res["A2"])]
    tb = Table(rows, hAlign="LEFT", colWidths=[190, 70]); tb.setStyle(TS); story.append(tb)
    story.append(Paragraph("A test counts in the month it ran (FS-3 section 6.1); a result the monitor re-polled after an "
                           "outage is the same test and counts once.", small))
    story.append(Paragraph("Dock gallons sold in 2026 by product", h))
    prods = ["REC-90 ethanol-free", "E10 unleaded", "Diesel"]
    marinas = sorted({k.split("|")[0] for k in res["A3"]})
    rows = [["Marina"] + prods]
    for m in marinas:
        rows.append([m] + ["{:,}".format(int(round(res["A3"]["%s|%s" % (m, p)]))) if "%s|%s" % (m, p) in res["A3"] else "-" for p in prods])
    tb = Table(rows, hAlign="LEFT", colWidths=[170, 95, 80, 70]); tb.setStyle(TS); story.append(tb)
    story.append(Paragraph("Gallons as the dock meters registered them, legacy point of sale to go-live on 16 November and "
                           "the new system after it; card sales dated by the sale, not the overnight settlement; Ashby "
                           "Hollow and Gilliam Creek sell REC-90 on their former E10 hoses from 1 December.", small))
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=48, bottomMargin=48,
                            title="Winter re-charting list and wetstock cutover readiness", author="Fuel Systems and UST Compliance",
                            subject="", creator="Highbank Marinas", producer="Highbank Marinas")
    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)


def write(golden_dir, res, pk):
    os.makedirs(golden_dir, exist_ok=True)
    write_list(os.path.join(golden_dir, "recharting_list_2027.csv"), res, pk)
    write_pdf(os.path.join(golden_dir, "cutover_readiness_2027.pdf"), res, pk)
