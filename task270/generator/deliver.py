"""The goldens and figures.json, every figure computed from the shipped pack: the pricing committee's workbook
(2027_rating_basis_bands.xlsx) and the band chart (band_c_frequency_2027_basis.png)."""
import os

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import analysis as A
import common as K

WB = "2027_rating_basis_bands.xlsx"
CHART = "band_c_frequency_2027_basis.png"


def half_up(x, nd=0):
    from decimal import ROUND_HALF_UP, Decimal
    q = Decimal(1).scaleb(-nd)
    return float(Decimal(repr(x)).quantize(q, rounding=ROUND_HALF_UP))


def compute(target):
    res = A.run(target)
    gold = A.top3(res["R2"])
    order = gold["order"]
    g, th = res["glass"], res["theft"]
    fig = dict(
        call=dict(band=gold["band"], band_names=[K.NAME[c] for c in gold["band"]], below=gold["below"],
                  below_name=K.NAME[gold["below"]], order=[K.NAME[c] for c in order]),
        components=dict(
            vehicle_years={K.NAME[c]: int(half_up(res["E"][c])) for c in K.CODES},
            reported_claims={K.NAME[c]: res["n0"][c] for c in K.CODES},
            reported_frequency={K.NAME[c]: half_up(res["R0"][c], 1) for c in K.CODES},
            vehicle_years_total=int(half_up(sum(res["E"].values()))),
            reported_claims_total=sum(res["n0"].values())),
        basis_2027=dict(threshold=int(A.T_GOLDEN), share_above=half_up(100 * res["S"], 1),
                        range=[int(min(A.T_GRID)), int(max(A.T_GRID))],
                        frequency={K.NAME[c]: half_up(res["R2"][c], 1) for c in K.CODES},
                        claims={K.NAME[c]: int(half_up(res["N2"][c])) for c in K.CODES}),
        ask_a=dict(claims={K.NAME[c]: g["n"][c] for c in K.CODES},
                   vehicle_years={K.NAME[c]: int(half_up(res["E25c"][c])) for c in K.CODES},
                   frequency={K.NAME[c]: half_up(g["freq"][c], 1) for c in K.CODES},
                   average={K.NAME[c]: int(half_up(g["avg"][c])) for c in K.CODES}),
        ask_b=dict(thefts={K.NAME[c]: th["n"][c] for c in K.CODES},
                   vehicle_years={K.NAME[c]: int(half_up(res["E25"][c])) for c in K.CODES},
                   frequency={K.NAME[c]: half_up(10.0 * th["freq"][c], 1) for c in K.CODES},
                   average={K.NAME[c]: int(half_up(th["avg"][c])) for c in K.CODES}),
        units=dict(claims_per_vehicle_years=100, thefts_per_vehicle_years=1000),
        rivals=dict(reported=[K.NAME[c] for c in A.top3(res["R0"])["band"]],
                    reported_below=K.NAME[A.top3(res["R0"])["below"]],
                    lift=[K.NAME[c] for c in A.top3(res["R1"])["band"]],
                    lift_factor=half_up(res["u"], 2),
                    lift_every_step=[K.NAME[c] for c in A.top3(res["R1b"])["band"]]),
    )
    return fig, res


THIN = Side(style="thin", color="B9C3CA")
HEAD = PatternFill("solid", fgColor="DDE5EA")
BAND = PatternFill("solid", fgColor="E6EEF0")


def _head(ws, row):
    for c in ws[row]:
        c.font = Font(bold=True)
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="top")


def write_workbook(path, fig, res):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Accident bands"
    band = fig["call"]["band"]
    ws.append(["Band C for 2027: %s, %s and %s" % tuple(fig["call"]["band_names"])])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Accident frequency on the 2027 wording (PC/26/09, section 2), accident years 2024 and 2025. First "
               "region below band C: %s." % fig["call"]["below_name"]])
    ws.append([])
    ws.append(["Rating region", "Vehicle-years 2024-25", "Accident claims reported", "Reported per 100 vehicle-years",
               "Claims above £%s" % format(fig["basis_2027"]["threshold"], ","),
               "Accident claims, 2027 wording", "Per 100 vehicle-years, 2027 wording", "Band"])
    _head(ws, 4)
    order = A.top3(res["R2"])["order"]
    above = {c: 0 for c in K.CODES}
    for a in res["A"]:
        if a["incurred"] > A.T_GOLDEN:
            above[a["region"]] += 1
    for i, c in enumerate(order):
        bandname = "C" if c in band else ("B" if i < 5 else "A")
        ws.append([K.NAME[c], round(res["E"][c], 1), res["n0"][c], round(res["R0"][c], 1), above[c],
                   int(half_up(res["N2"][c])), round(res["R2"][c], 1), bandname])
        r = ws.max_row
        ws.cell(r, 2).number_format = "#,##0"
        ws.cell(r, 3).number_format = "#,##0"
        ws.cell(r, 4).number_format = "0.0"
        ws.cell(r, 5).number_format = "#,##0"
        ws.cell(r, 6).number_format = "#,##0"
        ws.cell(r, 7).number_format = "0.0"
        if c in band:
            for cell in ws[r]:
                cell.fill = BAND
        if i == 2:
            for cell in ws[r]:
                cell.border = Border(bottom=Side(style="medium", color="1D4F55"))
    ws.append(["All regions", round(sum(res["E"].values()), 1), sum(res["n0"].values()),
               round(100.0 * sum(res["n0"].values()) / sum(res["E"].values()), 1), sum(above.values()),
               int(half_up(sum(res["N2"].values()))), round(100.0 * sum(res["N2"].values()) / sum(res["E"].values()), 1),
               None])
    r = ws.max_row
    for k, f in ((2, "#,##0"), (3, "#,##0"), (4, "0.0"), (5, "#,##0"), (6, "#,##0"), (7, "0.0")):
        ws.cell(r, k).number_format = f
    for cell in ws[r]:
        cell.font = Font(bold=True)
    for col, w in zip("ABCDEFGH", (26, 13, 13, 13, 13, 14, 14, 7)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "B5"

    g = wb.create_sheet("Windscreen 2025")
    g.append(["Rating region", "Comprehensive vehicle-years 2025", "Windscreen claims 2025",
              "Claims per 100 vehicle-years", "Average cost incl. VAT (£)"])
    _head(g, 1)
    for c in K.CODES:
        g.append([K.NAME[c], round(res["E25c"][c], 1), res["glass"]["n"][c], fig["ask_a"]["frequency"][K.NAME[c]],
                  fig["ask_a"]["average"][K.NAME[c]]])
        r = g.max_row
        g.cell(r, 2).number_format = "#,##0"
        g.cell(r, 3).number_format = "#,##0"
        g.cell(r, 4).number_format = "0.0"
        g.cell(r, 5).number_format = "#,##0"
    for col, w in zip("ABCDE", (26, 16, 14, 14, 14)):
        g.column_dimensions[col].width = w
    g.freeze_panes = "B2"

    t = wb.create_sheet("Theft 2025")
    t.append(["Rating region", "Vehicle-years 2025", "Thefts 2025", "Thefts per 1,000 vehicle-years",
              "Average cost net of salvage (£)"])
    _head(t, 1)
    for c in K.CODES:
        t.append([K.NAME[c], round(res["E25"][c], 1), res["theft"]["n"][c], fig["ask_b"]["frequency"][K.NAME[c]],
                  fig["ask_b"]["average"][K.NAME[c]]])
        r = t.max_row
        t.cell(r, 2).number_format = "#,##0"
        t.cell(r, 3).number_format = "#,##0"
        t.cell(r, 4).number_format = "0.0"
        t.cell(r, 5).number_format = "#,##0"
    for col, w in zip("ABCDE", (26, 14, 12, 15, 16)):
        t.column_dimensions[col].width = w
    t.freeze_panes = "B2"

    n = wb.create_sheet("Notes")
    S = fig["basis_2027"]
    notes = [
        "Accident claims: claims under the accident section with an amount paid or reserved above nil at 30 September "
        "2026, before recoveries, by accident date in 2024 and 2025, at fault, split or not at fault (PC/26/09, 2.2). "
        "Vehicle-years and claims by the rating region of the garaging postcode on the day (2.3).",
        "2027 wording: under the 2024 scale a claim costs a policyholder the premium lost over the climb back to the "
        "step, so damage below that cost was paid privately and never claimed, most on the middle steps. Claims above "
        "£%s are complete on every step. Each region's claims above £%s are divided by the share of claims that large "
        "among the policies a claim already cost nothing (step 0 and Step Protection holders): %.1f per cent. The "
        "band is the same for any threshold from £1,500 to £3,000." % (format(S["threshold"], ","),
                                                                       format(S["threshold"], ","), S["share_above"]),
        "Step Protection holders claim %.2f times as often as other policyholders on steps 6 to 9, but they claim more "
        "often above £%s as well: they bought the add-on, so their rate is not the rate the 2027 wording brings."
        % (fig["rivals"]["lift_factor"], format(S["threshold"], ",")),
        "Windscreen (3.1 to 3.3): the glass partner's jobs billed to the Society, a job's lines one claim, at the "
        "invoiced amount with VAT, and the claims paid to repairers the policyholder chose; jobs dated by booking. "
        "The platform's glass claims from 1 July 2025 are the partner's jobs again and carry the amount before VAT.",
        "Theft (4.1 to 4.3): a theft's claims share the police crime reference (written with separators on the legacy "
        "system); a recovered car's repair claim belongs to its theft. Cost is every claim's incurred less the salvage "
        "agent's net proceeds, from both years' statements.",
        "Prepared by %s, Pricing Actuary, for the Pricing Committee meeting of 21 October 2026. Data cut 30 September "
        "2026." % K.PEOPLE["actuary"],
    ]
    for line in notes:
        n.append([line])
    n.column_dimensions["A"].width = 120
    for row in n.iter_rows():
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)


def write_chart(path, fig, res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "svg.hashsalt": "task270"})
    order = A.top3(res["R2"])["order"]
    band = fig["call"]["band"]
    names = [K.NAME[c] for c in order]
    v2 = [res["R2"][c] for c in order]
    v0 = [res["R0"][c] for c in order]
    fg, ax = plt.subplots(figsize=(8.8, 5.0), dpi=150)
    y = np.arange(len(order))[::-1]
    ax.barh(y, v2, height=0.62, color=["#1d4f55" if c in band else "#9fb4b7" for c in order],
            label="2027 wording")
    ax.scatter(v0, y, marker="|", s=260, color="#c0503a", linewidths=2.2, zorder=3, label="As reported")
    for yy, v, r in zip(y, v2, v0):
        ax.text(max(v, r) + 0.18, yy, "%.1f" % v, va="center", fontsize=8.8, color="#1f2428")
    ax.set_yticks(y)
    ax.set_yticklabels(names)
    ax.axhline(y[2] - 0.5, color="#2f3b48", lw=1.0, ls="--")
    ax.text(16.6, y[2] - 0.42, "band C", ha="right", va="bottom", fontsize=8.6, color="#2f3b48")
    ax.set_xlim(0, 17)
    ax.set_xlabel("Accident claims per 100 vehicle-years, 2024 and 2025 accident years")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="lower right", frameon=False, fontsize=8.6)
    rep = A.top3(res["R0"])["band"]
    joins = [K.NAME[c] for c in band if c not in rep]
    drops = [K.NAME[c] for c in rep if c not in band]
    fg.suptitle("On the 2027 wording, %s joins band C and %s drops out" % (" and ".join(joins), " and ".join(drops)),
                x=0.012, ha="left", fontsize=11.5, fontweight="bold", color="#1f2428")
    fg.text(0.01, 0.01, "Claims above £%s divided by the share that large among step 0 and Step Protection claims. "
                        "Data cut 30 September 2026." % format(fig["basis_2027"]["threshold"], ","),
            fontsize=7.4, color="#5d646a")
    fg.tight_layout(rect=(0, 0.04, 1, 0.95))
    fg.savefig(path, metadata={"Software": None})
    plt.close(fg)


def write(target, golden):
    fig, res = compute(target)
    if os.path.exists(golden):
        for f in os.listdir(golden):
            os.remove(os.path.join(golden, f))
    os.makedirs(golden, exist_ok=True)
    write_workbook(os.path.join(golden, WB), fig, res)
    import postprocess as PP
    PP.normalize_ooxml(os.path.join(golden, WB), K.PEOPLE["actuary"], K.PEOPLE["actuary"], "2026-10-06T08:40:00Z",
                       "2026-10-08T17:12:00Z", title="2027 rating basis: bands, windscreen and theft", excel=True)
    write_chart(os.path.join(golden, CHART), fig, res)
    return fig, res
