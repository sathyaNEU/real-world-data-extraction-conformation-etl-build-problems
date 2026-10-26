"""The goldens for task270: hfc_pack_replacements_2027.xlsx (the region the programme starts in, each region's 2026
pack loss share, its packs' full charge in tonnes of CO2 equivalent and the part on R404A, and its cabinet and cold
room charges) and pack_leakage_2026.png (the four regions' loss shares), plus generator/figures.json."""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
import matplotlib.ticker                 # noqa: E402
import openpyxl                          # noqa: E402
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side   # noqa: E402

import analysis as A                     # noqa: E402
import asks as AS                        # noqa: E402
import common as K                       # noqa: E402

PICK, OTHER, INK, MUTED = "#1f6f78", "#b9bec4", "#1d2126", "#5b636d"


def figures(target):
    r = A.run(target)
    R, L = r["R"], r["L"]
    rate = {g: K.r(R.loc[g, "rate"]) for g in K.REGIONS}
    a = AS.all_asks(target, L=L, P=r["P"], J=r["J"])
    lad = A.ladder(target, r["P"], r["J"])
    fig = {
        "call": {"region": r["call"], "name": K.REGION_NAME[r["call"]], "runner_up": r["runner"],
                 "runner_up_name": K.REGION_NAME[r["runner"]],
                 "gap_points": K.r(R.loc[r["call"], "rate"] - R.loc[r["runner"], "rate"])},
        "components": {"loss_share_pct": rate,
                       "packs_in_scope": {g: int((r["P"]["region"] == g).sum()) for g in K.REGIONS}},
        "asks": {"charge_co2e_t": a["charge_co2e_t"], "r404a_co2e_t": a["r404a_co2e_t"],
                 "equipment_kg": a["equipment_kg"]},
        "context": {"topup_share_pct": {g: K.r(R.loc[g, "topup_rate"]) for g in K.REGIONS},
                    "packs_total": int(len(r["P"])),
                    "order": [g for g in R["rate"].sort_values(ascending=False).index],
                    "ladder": {k: v[0] for k, v in lad.items()}},
        "references": {"rounding": "shares to the nearest whole per cent; CO2 equivalents to the nearest tonne; "
                                   "kilograms to one decimal place",
                       "years": [2024, 2025, 2026, 2027], "line_pct": 10, "strategy_sections": [2.3],
                       "calibration_min_net_kg": 0.5},
    }
    return fig, r, a


def chart(path, fig):
    sh = fig["components"]["loss_share_pct"]
    pick = fig["call"]["region"]
    order = list(reversed(fig["context"]["order"]))
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    f, ax = plt.subplots(figsize=(8.6, 4.4), dpi=150)
    f.patch.set_facecolor("#fbfbfa")
    ax.set_facecolor("#fbfbfa")
    ys = range(len(order))
    ax.barh(list(ys), [sh[g] for g in order], height=0.56,
            color=[PICK if g == pick else OTHER for g in order], edgecolor="none")
    for y, g in zip(ys, order):
        ax.text(sh[g] + 0.25, y, "%d%%" % sh[g], va="center", ha="left", fontsize=11, color=INK,
                fontweight="bold" if g == pick else "normal")
    ax.set_yticks(list(ys))
    ax.set_yticklabels([K.REGION_NAME[g] for g in order], fontsize=11)
    ax.set_xlim(0, 20)
    ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(5))
    ax.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%d"))
    ax.set_xlabel("Refrigerant lost in 2026 as a share of the HFC packs' full charge (%)", color=MUTED)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#c3c9d0")
    ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", colors=MUTED)
    ax.xaxis.grid(True, color="#e3e6e9", linewidth=0.8)
    ax.set_axisbelow(True)
    f.text(0.02, 0.95, "%s's HFC packs lost the largest share of their charge in 2026" % fig["call"]["name"],
           fontsize=13.5, fontweight="bold", color=INK, ha="left")
    f.text(0.02, 0.895, "HFC packs in service throughout 2026: refrigerant charged less recovered, plus the fall in what "
           "the packs held over the year", fontsize=9.2, color=MUTED, ha="left")
    f.text(0.02, 0.025, "Source: Kelbray Refrigeration job sheets and Tarnley receiver levels, 2024 to 2026; "
           "Hallowmere F-gas register.", fontsize=8, color=MUTED, ha="left")
    f.subplots_adjust(left=0.17, right=0.97, top=0.82, bottom=0.2)
    f.savefig(path, facecolor=f.get_facecolor(), metadata={"Software": None})
    plt.close(f)


def workbook(path, fig):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Programme 2027"
    bold = Font(bold=True)
    thin = Side(style="thin", color="999999")
    c = fig["call"]
    sh = fig["components"]["loss_share_pct"]
    ws["A1"] = "2027 pack programme: the first region"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Start the 2027 programme in %s. Its HFC packs lost %d%% of their full charge in 2026, against %d%% "
                "in %s, the next region." % (c["name"], sh[c["region"]], sh[c["runner_up"]], c["runner_up_name"]))
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:F2")
    ws.row_dimensions[2].height = 31
    ws.append([])
    ws.append(["Region", "HFC packs", "2026 loss, share of full charge (%)", "Full charge (t CO2e)",
               "Of which on R404A (t CO2e)", "Cabinets and cold rooms charged in 2026 (kg)"])
    for cell in ws[4]:
        cell.font = bold
        cell.alignment = Alignment(wrap_text=True, vertical="bottom")
        cell.border = Border(bottom=thin)
    ws.row_dimensions[4].height = 44
    a = fig["asks"]
    for g in fig["context"]["order"]:
        ws.append([K.REGION_NAME[g], fig["components"]["packs_in_scope"][g], sh[g], a["charge_co2e_t"][g],
                   a["r404a_co2e_t"][g], a["equipment_kg"][g]])
        row = ws.max_row
        ws.cell(row, 2).number_format = "0"
        ws.cell(row, 3).number_format = "0"
        ws.cell(row, 4).number_format = "#,##0"
        ws.cell(row, 5).number_format = "#,##0"
        ws.cell(row, 6).number_format = "0.0"
        if g == c["region"]:
            for cc in ws[row]:
                cc.fill = PatternFill("solid", fgColor="DCEDEE")
    ws.append([])
    notes = [
        "Loss: refrigerant charged into each pack in 2026 less refrigerant recovered from it, plus the charge it was "
        "short at the end of 2026 less the charge it was short at the end of 2025; the shortfall read from Tarnley's "
        "receiver level through each pack's own rise in level per kilogram charged on its 2024 to 2026 job sheets.",
        "HFC packs in service throughout 2026 (Refrigerant Strategy 2.3); packs decommissioned in 2026 and the new CO2 "
        "packs are outside the programme.",
        "CO2 equivalent at the global warming potentials in Refrigerant Strategy 2.4, each pack at the refrigerant on "
        "its latest Kelbray job sheet, which for the packs retrofitted to R448A or R449A is the new blend.",
        "Cabinets and cold rooms: each job's refrigerant as the cylinder log weighs it.",
        "Kelbray job sheets exported 7 January 2027; Tarnley receiver levels exported 6 January 2027."]
    for n in notes:
        ws.append([n])
        ws.merge_cells(start_row=ws.max_row, start_column=1, end_row=ws.max_row, end_column=6)
        ws.cell(ws.max_row, 1).alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(ws.max_row, 1).font = Font(size=9, color="555555")
        ws.row_dimensions[ws.max_row].height = 40
    for col, wd in zip("ABCDEF", (16, 10, 20, 15, 16, 22)):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A5"
    wb.save(path)


def write(target, golden):
    os.makedirs(golden, exist_ok=True)
    fig, r, a = figures(target)
    workbook(os.path.join(golden, K.BOOK), fig)
    chart(os.path.join(golden, K.CHART), fig)
    return fig, r


def write_figures(path, fig):
    with open(path, "w") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
        f.write("\n")
