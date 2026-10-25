"""The golden deliverables: the Unit's workbook (each region's cattle-manure ammonia over 2025-26, its farmed land, its
kilograms a hectare against the line and its designation; the contractors' spring spreading by region; notes) and the
chart of each region's kilograms a hectare against the line; returns every figure the write-up states."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import openpyxl  # noqa: E402
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side  # noqa: E402
from openpyxl.utils import get_column_letter  # noqa: E402

import contractors as C  # noqa: E402
import golden as G  # noqa: E402
import world as W  # noqa: E402

BOLD = Font(bold=True)
HEAD_FILL = PatternFill("solid", fgColor="DDE7E3")
TOTAL_FILL = PatternFill("solid", fgColor="F2F2F2")
DES_FILL = PatternFill("solid", fgColor="F6E3C8")
TOP = Border(top=Side(style="thin"))


def _head(ws, row):
    for c in ws[row]:
        c.font = BOLD
        c.fill = HEAD_FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")


def fmt1(x):
    return "{:,.1f}".format(x)


def fmt2(x):
    return "{:,.2f}".format(x)


def figures(tr):
    gold, land = tr["gold"], tr["land"]
    kgha = gold / land
    des = [r for i, r in enumerate(W.REG) if kgha[i] >= W.LINE]
    w = tr["w"]
    farm_region = {h["farm_no"]: h["region"] for h in w.herds if h.get("farm_no")}
    L0 = G.census_route(tr["cen"], farm_region)
    L3 = (G.days(tr["P"]) / W.NDAY * G.table5()).sum(1)
    A = C.golden(tr["cj"], tr["herd_region"])
    P = tr["P"]
    regions = {}
    for i, r in enumerate(W.REG):
        regions[r] = dict(tonnes=fmt1(gold[i] / 1000), kg_ha="%.2f" % kgha[i], land_ha=fmt2(land[i]),
                          designated="Yes" if r in des else "No")
    ask = {r: dict(m3="{:,.0f}".format(round(A[r][0], -2)), less_pct="%.1f" % A[r][1]) for r in W.REG}
    tot_v = sum(A[r][0] for r in W.REG)
    tot_l = sum(A[r][0] * A[r][1] / 100 for r in W.REG)
    return dict(
        call=dict(designated=des, not_designated=[r for r in W.REG if r not in des]),
        regions=regions, ask_a=ask,
        components=dict(tonnes_total=fmt1(gold.sum() / 1000), land_total=fmt2(land.sum()),
                        animal_days="{:,.0f}".format(float((P.p1 - P.p0).sum()))),
        ask_a_total=dict(m3="{:,.0f}".format(round(tot_v, -2)), less_pct="%.1f" % (100 * tot_l / tot_v)),
        default=dict(designated=G.designated(L0, land), kg_ha={r: "%.2f" % (L0[i] / land[i]) for i, r in enumerate(W.REG)}),
        mean_count=dict(designated=G.designated(L3, land)),
        constants=dict(line=W.LINE, order=W.REG, gallon_m3="%.8f" % C.GAL, programme_year="2025-26",
                       rule_sections=["3", "4", "5", "6"]),
        _raw=dict(kg_ha={r: float(kgha[i]) for i, r in enumerate(W.REG)}, tonnes={r: float(gold[i] / 1000) for i, r in enumerate(W.REG)},
                  land={r: float(land[i]) for i, r in enumerate(W.REG)},
                  ask_m3={r: float(A[r][0]) for r in W.REG}, ask_less={r: float(A[r][1]) for r in W.REG}))


def workbook(path, f):
    raw = f["_raw"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Designation 2027"
    ws.append(["Ammonia Action Regions 2027: ammonia from cattle manure arising in each region, programme year "
               "1 November 2025 to 31 October 2026"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["%d regions at or above the line of %d kg NH3 a hectare of farmed land: %s." % (
        len(f["call"]["designated"]), W.LINE, ", ".join(f["call"]["designated"]))])
    ws.append([])
    ws.append(["Region", "Region code", "Ammonia from cattle manure (t NH3)", "Farmed land (ha)",
               "Ammonia a hectare (kg NH3/ha)", "Against the line (%)", "Designated"])
    _head(ws, 4)
    for r in W.REG:
        ws.append([r, W.RCODE[r], round(raw["tonnes"][r], 1), round(raw["land"][r], 2), round(raw["kg_ha"][r], 2),
                   round(100 * (raw["kg_ha"][r] / W.LINE - 1), 1), f["regions"][r]["designated"]])
        if f["regions"][r]["designated"] == "Yes":
            for cell in ws[ws.max_row]:
                cell.fill = DES_FILL
    last = ws.max_row
    tot_t, tot_l = sum(raw["tonnes"].values()), sum(raw["land"].values())
    ws.append(["All regions", None, round(tot_t, 1), round(tot_l, 2), round(1000 * tot_t / tot_l, 2), None, None])
    for cell in ws[ws.max_row]:
        cell.font = BOLD
        cell.fill = TOTAL_FILL
        cell.border = TOP
    for row in range(5, ws.max_row + 1):
        ws.cell(row, 3).number_format = "#,##0.0"
        ws.cell(row, 4).number_format = "#,##0.00"
        ws.cell(row, 5).number_format = "0.00"
        ws.cell(row, 6).number_format = "+0.0;-0.0"
        ws.cell(row, 2).alignment = Alignment(horizontal="center")
        ws.cell(row, 7).alignment = Alignment(horizontal="center")
    ws.append([])
    ws.append(["Designation is decided on unrounded figures (designation rules, section 5). Figures as at the National "
               "Bovine Register extract of 9 November 2026."])
    for k, wd in enumerate([16, 9, 15, 13, 14, 12, 11]):
        ws.column_dimensions[get_column_letter(k + 1)].width = wd
    ws.freeze_panes = "A5"
    ws.print_title_rows = "4:4"

    ws2 = wb.create_sheet("Contractor spreading")
    ws2.append(["Cattle slurry spread by contractors on farms in each region, 13 January to 30 April 2026"])
    ws2["A1"].font = Font(bold=True, size=12)
    ws2.append(["Countrywide Slurry Services, Vale Agri and Basin Agri, each job counted once."])
    ws2.append([])
    ws2.append(["Region", "Region code", "Cattle slurry spread (m3)", "Spread by trailing shoe, trailing hose or "
                "injection (%)"])
    _head(ws2, 4)
    for r in W.REG:
        ws2.append([r, W.RCODE[r], round(raw["ask_m3"][r], -2), round(raw["ask_less"][r], 1)])
    tv = sum(raw["ask_m3"].values())
    tl = sum(raw["ask_m3"][r] * raw["ask_less"][r] / 100 for r in W.REG)
    ws2.append(["All regions", None, round(tv, -2), round(100 * tl / tv, 1)])
    for cell in ws2[ws2.max_row]:
        cell.font = BOLD
        cell.fill = TOTAL_FILL
        cell.border = TOP
    for row in range(5, ws2.max_row + 1):
        ws2.cell(row, 3).number_format = "#,##0"
        ws2.cell(row, 4).number_format = "0.0"
        ws2.cell(row, 2).alignment = Alignment(horizontal="center")
    for k, wd in enumerate([16, 9, 15, 22]):
        ws2.column_dimensions[get_column_letter(k + 1)].width = wd
    ws2.freeze_panes = "A5"

    ws3 = wb.create_sheet("Notes")
    notes = [
        "Notes",
        "",
        "Measure: ammonia from cattle manure arising in the region over the programme year, at the Environmental "
        "Protection Office's 2025 factors (designation rules, section 3). Each animal-day is placed in the region of the "
        "herd holding the animal that day in the National Bovine Register, at the housed rate inside that region's "
        "housing season (factor note, Tables 3 and 4) and the grass rate outside it.",
        "Animal-days: from the date of birth, or 1 November 2025, to the day before the exit date, or 31 October 2026; "
        "an animal is in its departure herd until the arrival date. Days at marts, dealers' premises and export assembly "
        "centres sit in the region of those premises.",
        "Categories: calves under 12 months, cattle 12 to 24 months and over 24 months, and cows from first calving, dairy "
        "by the factor note's breed list.",
        "Regions: the 2024 regional structure, by the herd register's district for each herd number, a reissued number "
        "taken at the record valid on the day.",
        "Farmed land: the 2026 Land Parcel Register declarations by herd, commonage at each herd's share.",
        "Contractor spreading: cattle slurry only (pig slurry and digestate left out), on herds in the herd register, "
        "dated 13 January to 30 April 2026; Vale Agri's loads at each tanker's capacity, Countrywide's thousands of gallons and "
        "Basin Agri's metered cubic metres, at 0.00454609 cubic metres a gallon. A Countrywide invoice line whose reference is "
        "a Vale Agri or Basin Agri job number bills that contractor's job and is not counted again.",
        "Rounding: tonnes to one decimal, kilograms a hectare to two decimals, slurry to the nearest hundred cubic metres, "
        "shares to one decimal.",
        "Prepared by the Ammonia Programme Unit for the Minister's designation by 1 December 2026."]
    for line in notes:
        ws3.append([line] if line else [])
    ws3["A1"].font = Font(bold=True, size=12)
    ws3.column_dimensions["A"].width = 120
    for row in ws3.iter_rows(min_row=3):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)


def chart(path, f):
    raw = f["_raw"]["kg_ha"]
    order = sorted(W.REG, key=lambda r: raw[r])
    vals = [raw[r] for r in order]
    des = set(f["call"]["designated"])
    ink, muted, grid = "#1F2A2E", "#5B6770", "#D9DEE1"
    on, off = "#B5562B", "#9AA7AE"
    fig, ax = plt.subplots(figsize=(8.6, 5.6), dpi=150)
    ax.barh(range(len(order)), vals, height=0.62, color=[on if r in des else off for r in order], zorder=2)
    ax.axvline(W.LINE, color=ink, lw=1.2, ls=(0, (4, 3)), zorder=3)
    ax.text(W.LINE + 0.25, len(order) - 0.45, "Line: %d kg NH3/ha" % W.LINE, color=ink, fontsize=8.5, va="center")
    for k, (r, v) in enumerate(zip(order, vals)):
        ax.text(v - 0.3, k, "%.2f" % v, va="center", ha="right", fontsize=8, color="white" if r in des else ink)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels(order, fontsize=9, color=ink)
    ax.set_xlim(0, max(vals) * 1.12)
    ax.set_xlabel("Ammonia from cattle manure, kg NH3 a hectare of farmed land, 1 Nov 2025 to 31 Oct 2026",
                  fontsize=8.5, color=muted)
    ax.tick_params(axis="x", labelsize=8, colors=muted)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color=grid, lw=0.6, zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(grid)
    ax.set_title("%s regions reach the line: %s" % (["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight"][len(des)],
                                                  ", ".join(r for r in W.REG if r in des)),
                 loc="left", fontsize=10.5, color=ink, pad=12, fontweight="bold")
    fig.text(0.01, 0.012, "Bars in orange: designated as Ammonia Action Regions for 2027.\nSource: Ammonia Programme Unit, "
             "from the National Bovine Register (extract 9 November 2026) and the Land Parcel Register 2026.",
             fontsize=7, color=muted, linespacing=1.4)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(path, metadata={"Software": None, "Title": "Cattle ammonia per hectare 2025-26",
                                "Author": "Ammonia Programme Unit"})
    plt.close(fig)


def write(gpath, tr):
    f = figures(tr)
    workbook(gpath("workbook"), f)
    chart(gpath("chart"), f)
    f.pop("_raw")
    return f
