"""task306 goldens: the tooling workbook voltwerk_tooling_2027.xlsx and the chart voltwerk_tooling_2027.png, written from
figures.json."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import params as P
import postprocess

XLSX = "voltwerk_tooling_2027.xlsx"
PNG = "voltwerk_tooling_2027.png"
HEAD = PatternFill("solid", fgColor="DDE5EA")
TOT = Font(bold=True)
LINE = Border(top=Side(style="thin", color="8A8A8A"))


def _head(ws, row, cols):
    for j, h in enumerate(cols, 1):
        c = ws.cell(row=row, column=j, value=h)
        c.font = Font(bold=True)
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="top")


def _widths(ws, w):
    for j, x in enumerate(w, 1):
        ws.column_dimensions[get_column_letter(j)].width = x


def workbook(path, fig):
    wb = Workbook()
    ws = wb.active
    ws.title = "Slots 2027"
    ws["A1"] = "2027 slots: Mira city car 1,450, Volta hatch 900, Plover saloon 350, Kestrel SUV 250, Tern van 50"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Tooling plan 2027, section 2: the 3,000 slots in proportion to each platform's forecast of pack "
                "failures outside the OEM warranty in the Netherlands in 2027, lots of 50 by largest remainder. "
                "Operations planning, %s, August 2026." % P.ORG)
    ws["A2"].font = Font(italic=True, size=9)
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:I2")
    ws.row_dimensions[2].height = 30
    cols = ["Platform", "Failures 2027: cars on the register 30 June 2026", "Failures 2027: used imports still to "
            "arrive", "Failures 2027: forecast", "Share of the forecast", "Lots at that share", "Whole lots",
            "Lot from the remainders", "Slots 2027"]
    _head(ws, 4, cols)
    ws.row_dimensions[4].height = 46
    r = 5
    for n in P.NAMES:
        f = fig["forecast"][n]
        ws.append([n, fig["base_exact"][n], fig["arrivals_exact"][n], f["exact"], fig["share"][n], fig["lots_exact"][n],
                   fig["floors"][n], 1 if fig["extra_lot"][n] else 0, fig["slots"][n]])
        r += 1
    ws.append(["Total", round(sum(fig["base_exact"].values()), 2), round(sum(fig["arrivals_exact"].values()), 2),
               fig["total_exact"], 1.0, P.SLOTS // P.LOT,
               sum(fig["floors"].values()), sum(1 for v in fig["extra_lot"].values() if v), P.SLOTS])
    for c in ws[r]:
        c.font = TOT
        c.border = LINE
    for row in ws.iter_rows(min_row=5, max_row=r, min_col=2, max_col=4):
        for c in row:
            c.number_format = "#,##0"
    for row in ws.iter_rows(min_row=5, max_row=r, min_col=5, max_col=5):
        for c in row:
            c.number_format = "0.0%"
    for row in ws.iter_rows(min_row=5, max_row=r, min_col=6, max_col=6):
        for c in row:
            c.number_format = "0.00"
    for row in ws.iter_rows(min_row=5, max_row=r, min_col=9, max_col=9):
        for c in row:
            c.number_format = "#,##0"
    r += 2
    ws.cell(row=r, column=1, value="Forecast of pack failures outside the OEM warranty, 2027, all five platforms "
                                   "(nearest hundred):").font = Font(bold=True)
    c = ws.cell(row=r, column=4, value=fig["total"])
    c.number_format = "#,##0"
    c.font = Font(bold=True)
    _widths(ws, [16, 20, 20, 16, 12, 12, 10, 14, 11])
    ws.freeze_panes = "B5"

    ws = wb.create_sheet("Per lot")
    ws["A1"] = "What a lot of 50 carries, at the line's rates of July 2025 to June 2026"
    ws["A1"].font = Font(bold=True, size=13)
    cols = ["Platform", "Modules per lot of 50", "Modules issued, net of returns", "Packs shipped",
            "Packs with a first end-of-line run", "Passed it", "First-run pass share", "Cores received",
            "Rejected at intake", "Intake reject share"]
    _head(ws, 3, cols)
    ws.row_dimensions[3].height = 46
    for n in P.NAMES:
        a, b, c = fig["ask_a_detail"][n], fig["ask_b_detail"][n], fig["ask_c_detail"][n]
        ws.append([n, fig["ask_a"][n], a["modules"], a["ships"], b["packs"], b["passed"], fig["ask_b"][n] / 100.0,
                   c["cores"], c["rejected"], fig["ask_c"][n] / 100.0])
    for row in ws.iter_rows(min_row=4, max_row=8, min_col=7, max_col=7):
        for x in row:
            x.number_format = "0.0%"
    for row in ws.iter_rows(min_row=4, max_row=8, min_col=10, max_col=10):
        for x in row:
            x.number_format = "0.0%"
    for row in ws.iter_rows(min_row=4, max_row=8, min_col=2, max_col=4):
        for x in row:
            x.number_format = "#,##0"
    _widths(ws, [16, 12, 14, 10, 14, 9, 12, 10, 10, 12])
    ws.freeze_panes = "B4"

    ws = wb.create_sheet("Notes")
    notes = [
        ("What is forecast", "Pack failures in 2027 on cars in use in the Netherlands after the OEM's pack warranty has "
                             "ended (8 years from first admission; 5 for the Mira city car), Voltwerk refurbished "
                             "packs included whether or not our own two-year warranty still covers them. Cars are "
                             "taken to stay in use through 2027 (plan, section 3)."),
        ("Cars on the register", "Each car on the RDW extract of 30 June 2026 with the pack the replacement log shows "
                                 "it carried that day: its chance of failing in 2027 after its warranty, given it "
                                 "works on 30 June 2026, from the life curve read by straight lines between whole "
                                 "years of pack age."),
        ("Used imports still to arrive", "The register is the fleet of 30 June 2026; the fleet of 2027 also holds the "
                                         "used imports that arrive after it. Every month from July 2026 to December "
                                         "2027 is taken to bring in the cars the twelve months to June 2026 brought "
                                         "in (a first admission abroad before the first Dutch registration), in that "
                                         "year's average month: the same ages and the packs they arrived with, each "
                                         "at risk from its arrival. For the Mira city car that is about %d cars a "
                                         "month, %.1f years old on arrival on average, past their five-year warranty."
                                         % (fig["mira_imports_month"], fig["mira_import_age"])),
        ("Lots", "3,000 slots in 60 lots of 50: each platform takes the whole lots of its share, and the %d lots "
                 "left go to the largest remainders." % fig["extra_lots"]),
        ("Per lot", "Modules: every module issued from stores in July 2025 to June 2026 net of returns (a Kestrel "
                    "carrier is 2 modules), per pack shipped in those months, times 50; a pick that stores booked "
                    "against several work orders on a supplier's replacement lot went out once. First-run pass "
                    "share: packs whose first end-of-line run (an aborted run is no run) was in those months, "
                    "followed by work order through any BMS replacement. Intake reject share: cores received in "
                    "those months at either dock; a core the line built on passed intake, though one whose pack the "
                    "line scrapped carries AFGEKEURD in the intake export of 1 July."),
        ("Sources", "RDW register extract 30 June 2026; traction-battery replacement log to 30 June 2026; OEM and "
                    "Voltwerk life curves; warranty terms (February 2026); MES, stores and end-of-line exports of 1 "
                    "July 2026; the recycler's notes."),
    ]
    _head(ws, 1, ["Item", "Note"])
    for a, b in notes:
        ws.append([a, b])
    for row in ws.iter_rows(min_row=2, min_col=2, max_col=2):
        for x in row:
            x.alignment = Alignment(wrap_text=True, vertical="top")
    _widths(ws, [24, 110])
    wb.properties.creator = P.PEOPLE["planner"]
    wb.properties.lastModifiedBy = P.PEOPLE["planner"]
    wb.save(path)
    postprocess.scrub(path, P.ORG, "2026-08-14")
    postprocess.finish_office(path, "2026-08-11T08:20:00Z", "2026-08-14T15:12:00Z", P.ORG,
                              person=P.PEOPLE["planner"], revision=None)


def chart(path, fig):
    BLUE, ORANGE, INK, MUTED, SURF = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#fcfcfb"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5})
    fig_, ax = plt.subplots(figsize=(9.6, 5.4), dpi=150)
    fig_.patch.set_facecolor(SURF)
    ax.set_facecolor(SURF)
    order = sorted(P.NAMES, key=lambda n: -fig["slots"][n])
    x = range(len(order))
    w = 0.36
    fc = [fig["forecast"][n]["whole"] for n in order]
    sl = [fig["slots"][n] for n in order]
    b1 = ax.bar([i - w / 2 - 0.01 for i in x], fc, w, color=BLUE, label="Pack failures forecast, 2027",
                zorder=3)
    b2 = ax.bar([i + w / 2 + 0.01 for i in x], sl, w, color=ORANGE, label="Slots tooled, 2027", zorder=3)
    for bars, vals in ((b1, fc), (b2, sl)):
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 22, "{:,}".format(int(round(v))),
                    ha="center", va="bottom", fontsize=8.6, color=INK)
    ax.set_xticks(list(x))
    ax.set_xticklabels(order, color=INK)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: "{:,}".format(int(v))))
    ax.set_ylabel("Packs", color=MUTED)
    ax.tick_params(colors=MUTED, length=0)
    ax.grid(axis="y", color="#e4e3df", linewidth=0.8, zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#bdbcb6")
    ax.set_ylim(0, max(fc) * 1.16)
    ax.legend(frameon=False, loc="upper right", fontsize=9)
    fig_.suptitle("The Mira city car takes 1,450 of the 3,000 slots in 2027", x=0.07, ha="left", fontsize=13.5,
                  fontweight="bold", color=INK)
    ax.set_title("Pack failures outside the OEM warranty forecast for 2027 in the Netherlands (%s in all)\nand the "
                 "slots tooled in proportion to them, in lots of 50" % "{:,}".format(fig["total"]), loc="left",
                 fontsize=9.4, color=MUTED, pad=10)
    fig_.text(0.07, 0.015, "Source: RDW register of 30 June 2026, replacement log and life curves, with the used imports "
                           "arriving from July 2026. Operations planning, August 2026.", fontsize=7.6, color=MUTED)
    fig_.subplots_adjust(left=0.07, right=0.98, top=0.83, bottom=0.12)
    fig_.savefig(path, facecolor=SURF, metadata={"Software": None})
    plt.close(fig_)
