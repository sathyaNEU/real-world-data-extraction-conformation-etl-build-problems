"""The two deliverables: the placement workbook and the chart that carries the decision."""
import os

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.hashsalt"] = "task190"
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import world as W

THIN = Side(style="thin", color="8A8A8A")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
HEAD = PatternFill("solid", fgColor="E3E7EC")


def workbook(path, g):
    wb = Workbook()
    ws = wb.active
    ws.title = "Placement 2027"
    ws["A1"] = W.BANK
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Specialist review placement, 15 to 26 February 2027, for the risk committee of "
                "28 January 2027")
    ws["A3"] = ("Framework clause 6.2 and 6.4. Prepared from the case register and alert extract of "
                "18 January 2027.")
    for r in (2, 3):
        ws.cell(row=r, column=1).font = Font(size=9)
    hdr = ["Business line", "Cases confirmed in the two complete quarters", "Review covers"]
    for i, h in enumerate(hdr, start=1):
        c = ws.cell(row=5, column=i, value=h)
        c.font = Font(bold=True)
        c.fill = HEAD
        c.border = BOX
        c.alignment = Alignment(wrap_text=True, horizontal="center", vertical="bottom")
    row = 6
    for name in [l[0] for l in W.LINES]:
        o = g["assess"][name]
        covered = name in g["covered"]
        for i, v in enumerate([name, o["confirmed_two_quarters"], "yes" if covered else "no"], start=1):
            c = ws.cell(row=row, column=i, value=v)
            c.border = BOX
            if i >= 2:
                c.alignment = Alignment(horizontal="center")
            if i == 3 and covered:
                c.font = Font(bold=True)
        row += 1
    ws.cell(row=row + 1, column=1, value="Line that just misses").font = Font(bold=True)
    ws.cell(row=row + 1, column=2, value=g["just_misses"]).alignment = Alignment(horizontal="center")
    ws.cell(row=row + 3, column=1, value=(
        "The three lines the review covers are not the three that confirm the most cases. A case on "
        "the card and payment lines is seen within weeks of beginning, so those lines confirm the most "
        "and are carrying the least; a trade finance or correspondent case goes months before anyone "
        "sees it. The placement compares what each line is expected to be carrying at the review date, "
        "taken over its closed record as clause 6.3 defines it.")).font = Font(size=9, italic=True)
    ws.cell(row=row + 4, column=1, value="Prepared by %s, head of financial crime"
            % W.PEOPLE["head"]).font = Font(size=9)
    for col, wd in zip("ABC", [26, 22, 15]):
        ws.column_dimensions[col].width = wd
    ws.row_dimensions[5].height = 44
    wb.save(path)
    return path


def chart(path, g):
    names = [l[0] for l in W.LINES]
    conf = [g["assess"][n]["confirmed_two_quarters"] for n in names]
    covered = [n in g["covered"] for n in names]
    fig, ax = plt.subplots(figsize=(10.0, 5.2), dpi=140)
    bars = ax.bar(range(len(names)), conf,
                  color=["#2f5d50" if c else "#c3cbd2" for c in covered],
                  edgecolor="#7c868e", linewidth=0.5)
    for i, (c, v) in enumerate(zip(covered, conf)):
        if c:
            ax.text(i, v + max(conf) * 0.02, "review covers", ha="center", va="bottom", fontsize=7.8,
                    color="#2f5d50", rotation=90)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=38, ha="right", fontsize=8.4)
    ax.set_ylabel("Cases confirmed, 2026 Q3 and Q4", fontsize=9)
    ax.set_title("Cases confirmed by business line, and where the February 2027 review goes\n"
                 "%s" % ", ".join(g["covered"]), fontsize=10.5, loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_ylim(0, max(conf) * 1.3)
    ax.grid(axis="y", color="#e6e6e6", linewidth=0.6)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)
    return path
