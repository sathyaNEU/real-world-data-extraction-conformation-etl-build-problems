"""The golden deliverables: the planning manager's forecast workbook and the chart for the review."""
import datetime as dt

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import openpyxl  # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill  # noqa: E402

import golden as G  # noqa: E402
import params as P  # noqa: E402
import postprocess as PP  # noqa: E402

MONTHS = {2: "February 2027", 3: "March 2027"}
GNAMES = {"RAV": "Ravelijn Drogist", "HGH": "Hooghuys Drogisterij", "VLM": "Vlietmarkt Supermarkten",
          "ZLF": "Independent drugstores"}


def workbook(path, fig):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Forecast"
    bold = Font(bold=True)
    head = PatternFill("solid", fgColor="D9E1F2")
    ws["A1"] = "Venlo site, Siersma Care: pick accuracy forecast for February and March 2027"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Prepared 6 January 2027 for the Q1 business review. Schedule 3 basis: order lines passing pack-out verification."
    hdr = ["Month", "Planned order lines", "Expected failing lines", "Forecast accuracy (%)", "Target (%)", "Target holds"]
    for j, h in enumerate(hdr, 1):
        c = ws.cell(row=4, column=j, value=h)
        c.font = bold
        c.fill = head
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, m in enumerate((2, 3), 5):
        f = fig["forecast"][m]
        vals = [MONTHS[m], f["plan"], f["fail_r"], f["acc_r"], 99.80, "No" if not f["holds"] else "Yes"]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=i, column=j, value=v)
            if j == 4:
                c.number_format = "0.0"
            if j == 5:
                c.number_format = "0.00"
    ws["A8"] = "Error probability per order line, 2026 record (all picked lines, both channels)"
    ws["A8"].font = bold
    rows = [("Pick", "Lines picked 2026", "Failing lines 2026", "Failure rate (%)")]
    for s, lab in (("whole", "Whole inner packs"), ("loose", "Loose units below one inner"),
                   ("mixed", "Whole inners plus loose units")):
        h = fig["hep_table"][s]
        rows.append((lab, h["lines"], h["fails"], round(100 * h["rate"], 3)))
    for i, r in enumerate(rows, 9):
        for j, v in enumerate(r, 1):
            c = ws.cell(row=i, column=j, value=v)
            if i == 9:
                c.font = bold
                c.fill = head
    ws["A14"] = ("Each planned line is carried at the rate of the pick it calls for, with each range's article mix and order "
                 "sizes taken from the same month of 2026 and the Daily range held in inners of four (PCN-2026-11).")
    ws["A15"] = ("Daily store lines of 6 and 18 units become whole inners plus loose units; lines of 12 and 24 stay whole inners.")
    for col, wdt in zip("ABCDEF", (30, 18, 18, 18, 11, 12)):
        ws.column_dimensions[col].width = wdt
    ws2 = wb.create_sheet("Store claims 2026")
    ws2["A1"] = "Accepted store claims for short, over or wrong articles on 2026 retail deliveries, units, by quarter of delivery"
    ws2["A1"].font = bold
    hdr2 = ["Customer", "Q1", "Q2", "Q3", "Q4", "2026"]
    for j, h in enumerate(hdr2, 1):
        c = ws2.cell(row=3, column=j, value=h)
        c.font = bold
        c.fill = head
    for i, g in enumerate(G.GROUP_ORDER, 4):
        vals = [fig["claims"][(g, q)] for q in (1, 2, 3, 4)]
        for j, v in enumerate([GNAMES[g]] + vals + [sum(vals)], 1):
            ws2.cell(row=i, column=j, value=v)
    ws2["A9"] = ("Each claimed line counted once; a missing roll cage counts the units it carried; portal entries made before "
                 "the portal's July 2026 release (offline 11 to 19 July) count store packs and are converted at the article's "
                 "store order unit.")
    for col, wdt in zip("ABCDEF", (26, 9, 9, 9, 9, 9)):
        ws2.column_dimensions[col].width = wdt
    wb.save(path)
    PP.normalize_ooxml(path, "Romy Friehus", "Romy Friehus", "2027-01-05T08:12:00Z", "2027-01-06T15:47:00Z", excel=True,
                       company="Kroonvaart Fulfilment B.V.")


def chart(path, fig):
    hist = fig["history"]
    fc = fig["forecast"]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    f, ax = plt.subplots(figsize=(8.6, 4.4), dpi=150)
    xs = list(range(1, 13))
    ax.plot(xs, [hist[m] for m in xs], color="#1f4e79", marker="o", ms=4, lw=1.6, label="2026 actual")
    ax.plot([12, 14, 15], [hist[12], fc[2]["acc_r"], fc[3]["acc_r"]], color="#c55a11", ls="--", lw=1.4)
    ax.plot([14, 15], [fc[2]["acc_r"], fc[3]["acc_r"]], color="#c55a11", marker="D", ms=5, lw=0, label="Forecast Feb and Mar 2027")
    ax.axhline(P.KPI, color="#7f7f7f", lw=1.1, ls=":")
    ax.text(15.35, P.KPI + 0.004, "Target 99.80", color="#595959", fontsize=8, ha="right", va="bottom")
    for x, m in ((14, 2), (15, 3)):
        ax.annotate("%.1f" % fc[m]["acc_r"], (x, fc[m]["acc_r"]), textcoords="offset points", xytext=(0, -13), ha="center",
                    fontsize=8, color="#c55a11")
    ax.set_xticks(xs + [14, 15])
    ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Feb\n2027", "Mar\n2027"])
    ax.set_xlim(0.5, 15.6)
    ax.set_ylim(99.60, 99.92)
    ax.set_ylabel("Pick accuracy (% of order lines)")
    ax.set_title("Venlo pick accuracy for Siersma: 2026 by month and the February and March 2027 forecast", fontsize=10)
    ax.grid(axis="y", color="#e5e5e5", lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(loc="lower left", frameon=False, fontsize=8)
    f.tight_layout()
    f.savefig(path, metadata={"Software": None})
    plt.close(f)
