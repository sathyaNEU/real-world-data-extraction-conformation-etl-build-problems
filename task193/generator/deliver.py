"""The two files the coordinator would put in front of the division."""
import os

import world as W

NAME = {}


def names():
    if not NAME:
        for c, n, _h, _a, _k, _e in W.PRODUCTS:
            NAME[c] = n
        NAME[W.DOMINANT] = W.DOM_NAME
        NAME[W.RENAMED[0]] = W.RENAMED[2]
    return NAME


def workbook(path, g):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    nm = names()
    wb = Workbook()
    ws = wb.active
    ws.title = "Signals taken forward"
    thin = Side(style="thin", color="BFBFBF")
    box = Border(left=thin, right=thin, top=thin, bottom=thin)
    ws["A1"] = "%s: signals of disproportionate reporting, quarter to 30 September 2026" % W.AGENCY
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Pairs meeting the three criteria in paragraph 3.2, with the reporting of the autumn "
                "booster campaign left out of what each pair is measured against.")
    ws["A2"].font = Font(size=9, italic=True)
    ws.append([])
    head = ["Product", "Reaction", "Reports", "Proportional reporting ratio", "Chi-square",
            "Held down by the campaign's reporting"]
    ws.append(head)
    for c in ws[4]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="bottom")
        c.fill = PatternFill("solid", fgColor="EDEDE8")
        c.border = box
    masked = {tuple(x) for x in g["masked_pairs"]}
    for r in g["signals"]:
        key = (r["code"], r["reaction"])
        ws.append([nm[r["code"]], r["reaction"], r["reports"], round(r["prr"], 2),
                   round(r["chi"], 1),
                   "yes, %.2f against the whole database" % r["prr_crude"]
                   if key in masked else None])
        for c in ws[ws.max_row]:
            c.border = box
    row = ws.max_row + 2
    ws.cell(row=row, column=1, value="Pairs taken forward").font = Font(bold=True)
    ws.cell(row=row, column=3, value=g["taken_forward"]).font = Font(bold=True)
    ws.cell(row=row + 1, column=1, value="The desk's capacity for the quarter")
    ws.cell(row=row + 1, column=3, value=W.CAPACITY)
    ws.cell(row=row + 2, column=1, value="Assessment slots left")
    ws.cell(row=row + 2, column=3, value=W.CAPACITY - g["taken_forward"])
    ws.cell(row=row + 3, column=1, value="Pairs the whole-database comparison alone takes forward")
    ws.cell(row=row + 3, column=3, value=g["crude_count"])
    for i, wid in enumerate((22, 26, 10, 16, 12, 42), start=1):
        ws.column_dimensions[chr(64 + i)].width = wid
    ws.freeze_panes = "A5"
    wb.save(path)


def chart(path, g):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    nm = names()
    masked = {tuple(x) for x in g["masked_pairs"]}
    rows = sorted(g["signals"], key=lambda r: r["prr"])
    lab = ["%s, %s" % (nm[r["code"]], r["reaction"].lower()) for r in rows]
    fig, ax = plt.subplots(figsize=(9.2, 6.4), dpi=150)
    y = range(len(rows))
    for i, r in enumerate(rows):
        hid = (r["code"], r["reaction"]) in masked
        ax.barh(i, r["prr"], height=.62, color="#8c3b3b" if hid else "#4a6b86",
                edgecolor="#2d2d2d", linewidth=.5, zorder=3)
        if hid:
            ax.plot([r["prr_crude"]], [i], marker="D", color="#d9a24a", markersize=6,
                    markeredgecolor="#4a3a12", zorder=5)
        ax.text(r["prr"] + .06, i, "%.2f" % r["prr"], va="center", fontsize=8, zorder=4)
    ax.axvline(W.PRR_MIN, color="#222222", linestyle="--", linewidth=1.1, zorder=2)
    ax.text(W.PRR_MIN + .02, len(rows) - .35, "paragraph 3.2 takes a pair forward at 2.00",
            fontsize=8, rotation=90, va="top")
    ax.set_yticks(list(y))
    ax.set_yticklabels(lab, fontsize=8.5)
    ax.set_xlabel("Proportional reporting ratio, the campaign's reporting left out of the comparison",
                  fontsize=9)
    ax.set_title("Signals taken forward, quarter to 30 September 2026", fontsize=11.5, loc="left")
    ax.set_xlim(0, max(r["prr"] for r in rows) * 1.18)
    ax.grid(axis="x", color="#dddddd", linewidth=.6, zorder=1)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    import matplotlib.patches as mp
    ax.legend(handles=[mp.Patch(color="#8c3b3b", label="held below 2.00 while the campaign is in the comparison"),
                       mp.Patch(color="#4a6b86", label="past 2.00 either way"),
                       plt.Line2D([], [], marker="D", color="#d9a24a", linestyle="none",
                                  markeredgecolor="#4a3a12",
                                  label="the same pair measured against the whole database")],
              fontsize=8, loc="lower right", framealpha=.95)
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": None, "Creator": None, "Title": None})
    plt.close(fig)
