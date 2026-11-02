"""The golden deliverables, written from analysis.py's figures: the January 2027 tightness-testing work order
(PDF, with the quarter's chart) and the cardlock drop shortfalls (XLSX)."""
import datetime as dt
import io
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                        # noqa: E402
import openpyxl                                                        # noqa: E402
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side  # noqa: E402

import docs as D                                                       # noqa: E402
import analysis as A                                                   # noqa: E402

NAMES = {"R": "regular", "P": "premium", "D": "diesel"}
TOWN = {"GB-118": "Wynyard", "GB-121": "Foam Lake", "GB-124": "Wadena", "GB-127": "Kelvington", "GB-131": "Ituna",
        "GB-134": "Canora", "GB-139": "Preeceville", "GB-142": "Kamsack", "GB-146": "Langenburg", "GB-153": "Russell",
        "GB-157": "Roblin", "GB-160": "Grandview", "CL-401": "Wynyard", "CL-404": "Canora", "CL-407": "Kamsack",
        "CL-412": "Russell"}
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#b9b7b0"
MARK = "#2a78d6"
LINE = "#c43d2f"


def chart_png(pk):
    rows = sorted(pk.q4.items(), key=lambda kv: kv[1]["loss_lph"])
    labels = ["%s %s" % (TOWN[k[0]], NAMES[k[1]]) for k, v in rows]
    vals = [v["loss_lph"] for k, v in rows]
    marked = [k in pk.designated for k, v in rows]
    fig, ax = plt.subplots(figsize=(6.9, 7.4), dpi=200)
    y = list(range(len(rows)))
    ax.barh(y, vals, height=0.62, color=[MARK if m else MUTED for m in marked],
            hatch=None, edgecolor="white", linewidth=0.6, zorder=2)
    for yi, v, m in zip(y, vals, marked):
        if m:
            ax.text(v + 0.03, yi, "%.1f L/h  test" % v, va="center", ha="left", fontsize=7.4, color=INK,
                    fontweight="bold")
    ax.axvline(0.75, color=LINE, linewidth=1.2, linestyle=(0, (4, 2)), zorder=3)
    ax.text(0.77, -0.45, "PD-07 line, 0.75 L/h", fontsize=7.4, color=LINE, va="bottom")
    ax.axvline(0, color=INK2, linewidth=0.6, zorder=1)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=6.9, color=INK)
    for tl, m in zip(ax.get_yticklabels(), marked):
        if m:
            tl.set_fontweight("bold")
    ax.set_xlabel("Loss to the ground, October to December 2026 (litres an hour)", fontsize=7.8, color=INK2)
    lo = min(-0.2, min(vals) - 0.05)
    ax.set_xlim(lo, max(1.6, max(vals) + 0.45))
    ax.set_ylim(-0.7, len(rows) - 0.3)
    ax.tick_params(axis="x", labelsize=7.2, colors=INK2)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#e4e3df", linewidth=0.6, zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#999892")
    ax.set_title("Two gas bar tank systems over the PD-07 line, October to December 2026", fontsize=9.2, color=INK,
                 loc="left", fontweight="bold")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return buf


def workorder_pdf(path, pk):
    S = D.styles()
    f = []
    names = ["%s %s" % (TOWN[k[0]], NAMES[k[1]]) for k in pk.designated]
    f.append(D.Paragraph("Tamarack Prairie Co-operative Ltd., Petroleum Division", S["ref"]))
    f.append(D.Paragraph("Work order TT-2027-01: %s to precision tightness testing" % " and ".join(names), S["title"]))
    f.append(D.table([["To", "Precision tank and line testing contractor (standing offer TPC-SO-2025-14)"],
                      ["From", "Leah Haynes, Controller, for Roy Turner, Petroleum Manager"],
                      ["Date", "6 January 2027"],
                      ["Subject", "PD-07 Rev. 3 quarterly review, October to December 2026: systems going for testing"]],
                     [22 * D.mm, 150 * D.mm], small=True, header=False))
    f.append(D.Spacer(1, 8))
    rows = [["Site", "Tank system", "Book shortfall, Q4 (litres)", "Loss to the ground (L/h)", "Test required"]]
    for k in pk.designated:
        v = pk.q4[k]
        rows.append(["%s %s" % (k[0], TOWN[k[0]]), "Tank %d, %s" % ({"R": 1, "P": 2, "D": 3}[k[1]], NAMES[k[1]]),
                     "{:,.0f}".format(v["short"]), "%.1f" % v["loss_lph"], "Tank and lines, precision"])
    f.append(D.table(rows, [36 * D.mm, 30 * D.mm, 40 * D.mm, 36 * D.mm, 40 * D.mm], align=[2, 3]))
    f.append(D.Paragraph("Source: PD-07 quarterly book from gauge closes, bills of lading and point-of-sale exports to "
                         "5 January 2027; service work orders 2024 to 2026.", S["small"]))
    f.append(D.Spacer(1, 4))
    f.append(D.Paragraph(
        "Both systems lost more than the PD-07 line of 0.75 litres an hour to the ground over the quarter. Please "
        "test the tank and its pressurised lines at each in January and send the results to the Controller's office. "
        "Both were reported to the province as suspected releases on 6 January 2027. Every other gas bar tank system "
        "was at or under the line and stays on monthly monitoring.", S["p"]))
    f.append(D.Paragraph("How the loss was worked out", S["h"]))
    f.append(D.Paragraph(
        "Each system's book shortfall is its gauge close on 1 October, plus product received at the bill of "
        "lading's net volume on the business day of the drop, less point-of-sale volume, less the gauge close on "
        "1 January. Part of every shortfall is product the dispenser meters handed out beyond what they "
        "registered: the co-op's meters drift that way with the litres they pass after a calibration. That part "
        "was taken out at the drift the 2024 to 2026 tank books show across the whole network, about %.1f mL per "
        "20 L draft for every 100,000 litres a meter passes, applied to each hose's litres since its last " % pk.k +
        "calibration or replacement in the work orders.<super>1</super> What is left, per hour of the quarter, is "
        "product lost to the ground.<super>2</super>", S["p"]))
    f.append(D.Paragraph(
        "Ituna's 1987 single-wall steel tank loses product whatever it sells, which is what the cathodic protection "
        "survey's low readings would lead one to expect. Canora's regular loses product in step with its sales, so a "
        "reconciliation that books every sales-linked loss to the meters would clear it; its meters were calibrated "
        "on 2 July 2026 and have passed too few litres since to account for more than a small part of its "
        "shortfall. Its submersible pump was replaced on the same visit, and the contractor should start with the "
        "pump head and the line from it. Kamsack's regular and Foam Lake's diesel run larger shortfalls than either, "
        "and their meters' use since calibration accounts for them.", S["p"]))
    img = D.Image(chart_png(pk), width=170 * D.mm, height=170 * D.mm * 7.4 / 6.9)
    f.append(D.KeepTogether([D.Paragraph("Every gas bar tank system against the line", S["h"]), img]))
    f.append(D.Paragraph("Bars in blue are the systems on this work order; the dashed line is the PD-07 line of "
                         "0.75 litres an hour.", S["small"]))
    f.append(D.Spacer(1, 4))
    f.append(D.Paragraph("1. Kamsack's diesel dispenser (5) was not calibrated at the April 2025 visit; its meters are "
                         "counted from June 2024.", S["small"]))
    f.append(D.Paragraph("2. Hours elapsed in the quarter per PD-07 s.4: 2,208 in Saskatchewan and 2,209 at the "
                         "Manitoba gas bars, whose clocks went back on 1 November.", S["small"]))
    D.write_pdf(path, dict(title="Work order TT-2027-01 tank system tightness testing January 2027",
                           author="Leah Haynes", subject="PD-07 quarterly review Q4 2026", creator="Microsoft Word",
                           producer="Microsoft: Print To PDF"),
                "Tamarack Prairie Co-operative Ltd. | Work order TT-2027-01", "Controller's office, PD-07 review",
                f, "2027-01-06 11:42:19")


def drops_xlsx(path, pk):
    wb = openpyxl.Workbook()
    hdr_fill = PatternFill("solid", fgColor="DDEBF7")
    thin = Side(style="thin", color="A6A6A6")
    months = [(10, "Oct 2026"), (11, "Nov 2026"), (12, "Dec 2026")]

    def header(ws, cols):
        ws.append(cols)
        for c in ws[ws.max_row]:
            c.font = Font(bold=True)
            c.fill = hdr_fill
            c.border = Border(bottom=thin)
            c.alignment = Alignment(horizontal="center", wrap_text=True)

    def table(ws, title, keys, label, data):
        ws.append([title])
        ws["A1"].font = Font(bold=True, size=12)
        ws.append(["Litres, to the nearest 10; a negative figure means the drops came in over their bills."])
        ws["A2"].font = Font(italic=True, size=9, color="555555")
        header(ws, [label] + [m[1] for m in months] + ["Q4 2026"])
        for k in keys:
            vals = [A.r10(data.get((k, m), 0.0)) for m, _ in months]
            ws.append([("%s %s" % (k, TOWN[k])) if k in TOWN else k] + vals +
                      [A.r10(sum(data.get((k, m), 0.0) for m, _ in months))])
        tot = [A.r10(sum(data.get((k, m), 0.0) for k in keys)) for m, _ in months]
        ws.append(["All"] + tot + [A.r10(sum(data.values()))])
        for c in ws[ws.max_row]:
            c.font = Font(bold=True)
            c.border = Border(top=thin)
        for row in ws.iter_rows(min_row=4, min_col=2, max_col=5):
            for c in row:
                c.number_format = "#,##0;-#,##0"
        ws.column_dimensions["A"].width = 26
        for col in "BCDE":
            ws.column_dimensions[col].width = 12
        ws.freeze_panes = "B4"

    ws = wb.active
    ws.title = "By carrier"
    table(ws, "Cardlock drops short of the bill of lading by carrier, Q4 2026", sorted({k[0] for k in pk.by_carrier}),
          "Carrier", pk.by_carrier)
    ws2 = wb.create_sheet("By cardlock")
    table(ws2, "Cardlock drops short of the bill of lading by cardlock, Q4 2026", sorted({k[0] for k in pk.by_site}),
          "Cardlock", pk.by_site)

    ws3 = wb.create_sheet("Drops")
    header(ws3, ["Bill of lading", "Carrier", "Cardlock", "Product", "Drop (CST)", "Bill net L @15C",
                 "Gauge rise L", "Drawn by fills during drop L", "Received L", "Short (+) / over (-) L", "Measured from"])
    for d in sorted(pk.drops, key=lambda x: x["when"]):
        src = "Gauge delivery report" if d["how"] == "report" else "Hourly gauge readings either side of the drop"
        ws3.append([d["bol"], d["carrier"], "%s %s" % (d["site"], TOWN[d["site"]]),
                    "Diesel" if d["prod"] == "D" else "Regular", d["when"].replace(second=0, microsecond=0),
                    int(d["net"]), round(d["received"] - d["drawn"], 1), round(d["drawn"], 2), round(d["received"], 1),
                    round(d["short"], 1), src])
    for row in ws3.iter_rows(min_row=2):
        row[4].number_format = "yyyy-mm-dd hh:mm"
        row[5].number_format = "#,##0"
        for c in row[6:10]:
            c.number_format = "#,##0.0;-#,##0.0"
    widths = [14, 22, 20, 9, 17, 14, 13, 17, 13, 16, 40]
    for i, wdt in enumerate(widths):
        ws3.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = wdt
    ws3.freeze_panes = "A2"
    ws3.auto_filter.ref = "A1:K%d" % ws3.max_row

    ws4 = wb.create_sheet("Notes")
    notes = [
        "Received litres are the gauge's rise over its delivery report plus the litres the fleet drew from that tank "
        "while the drop was going in (cardlock host transactions, UTC less six hours).",
        "Drops whose report the console no longer held at a monthly pull, and the Kamsack drop during the power cut "
        "of 19 November, are measured from the hourly readings either side of the rise plus the fills between them.",
        "Months are the month of the drop in CST, not the bill's loading date.",
        "Bills and gauge volumes are net litres at 15 C.",
        "Prepared 6 January 2027 from the extracts pulled to 5 January 2027.",
    ]
    ws4.append(["Notes"])
    ws4["A1"].font = Font(bold=True)
    for n in notes:
        ws4.append([n])
    ws4.column_dimensions["A"].width = 120
    wb.save(path)
    D.finalise_xlsx(path, "Cardlock drops Q4 2026", "Leah Haynes", "Leah Haynes", "Tamarack Prairie Co-operative Ltd.",
                    "2027-01-06T15:02:44", "2027-01-06T17:26:09")


def write(pk, outdir):
    os.makedirs(outdir, exist_ok=True)
    workorder_pdf(os.path.join(outdir, "tank_test_workorder_jan2027.pdf"), pk)
    drops_xlsx(os.path.join(outdir, "cardlock_drops_q4_2026.xlsx"), pk)
