"""The two deliverables from the shipped bundle, and figures.json (every figure the write-up states).

    python3 task134/generator/golden.py [--target DIR] [--out DIR]
"""
import argparse
import datetime as dt
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import askcalc as AC
import estimators as E
import readpack as RP
import world as W

TASK = os.path.dirname(HERE)
XLSX = "care_home_funding_forecast_2027-28.xlsx"
PNG = "care_home_costs_by_locality.png"
RES_COL, NUR_COL = "#2a78d6", "#eb6834"


def load_tables(tdir):
    import pandas as pd
    p = lambda f: os.path.join(tdir, f)
    pl, li, cw, dl = RP.load(tdir)
    T = dict(pl=pl, li=li, cw=cw, dl=dl)
    T["ass"] = pd.read_csv(p("charging_assessments_2021-2026.csv"), dtype=str, keep_default_na=False)
    T["lookup"] = pd.read_csv(p("postcode_locality_lookup.csv"), dtype=str, keep_default_na=False)
    T["reg"] = read_register(p("care_home_register_2026-12.xlsx"))
    return T


def read_register(path):
    import openpyxl
    import pandas as pd
    ws = openpyxl.load_workbook(path, read_only=True).active
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[0]
    out = []
    for r in rows[1:]:
        d = {}
        for k, v in zip(hdr, r):
            if isinstance(v, dt.datetime):
                v = v.date().isoformat()
            d[k] = "" if v is None else str(v)
        out.append(d)
    return pd.DataFrame(out)


def r10(x):
    return int(np.floor(x / 10.0 + 0.5) * 10)


def r1(x):
    return int(np.floor(x + 0.5))


def compute(tdir):
    T = load_tables(tdir)
    I, st, aw = RP.inputs(T["pl"], T["li"], T["cw"], T["dl"])
    g = E.golden(I)
    cen = RP.census(st, RP.month_ends())
    rungs = E.rungs(I, cen)
    ask, counts = AC.compute(T, return_counts=True)
    stops = {k: AC.vec(AC.compute(T, **kw)) for k, kw in AC.STOPS.items()}
    return T, I, g, rungs, ask, counts, stops


def figures(I, g, rungs, ask, counts, stops):
    tot = g["total"]
    o, HX, HC, HS = g["o"], g["HX"], g["HC"], g["HS"]
    on = E.pool(I)
    d0 = E.months(I["sf_admit"][on], np.full(on.sum(), W.ASOF))
    bands = [(0, 6), (6, 12), (12, 15), (15, 18), (18, 24), (24, 36), (36, 48), (48, 1e9)]
    blab = ["under 6", "6 to 11", "12 to 14", "15 to 17", "18 to 23", "24 to 35", "36 to 47", "48 and over"]
    occ, expo = E.occ_exp(I["sf_admit"], I["sf_entry"], I["sf_end"], I["sf_reason"] == "CONV", W.HIST_START, W.ASOF,
                          1.0, 180)
    haz = {}
    for (lo, hi), lab in zip(bands, blab):
        a, b = int(lo), int(min(hi, 180))
        haz[lab] = round(float(occ[a:b].sum() / expo[a:b].sum()), 4)
    pool = {lab: int(((d0 >= lo) & (d0 < hi)).sum()) for (lo, hi), lab in zip(bands, blab)}
    conv_y = {}
    for y in range(2021, 2027):
        a0, a1 = W.dn(dt.date(y, 1, 1)), W.dn(dt.date(y + 1, 1, 1))
        conv_y[str(y)] = int(((I["cf_route"] == "CONV") & (I["cf_entry"] >= a0) & (I["cf_entry"] < a1)).sum())
    order, top = AC.chart(ask)
    cells = {}
    for loc in W.LOCS:
        for ct in ("Residential", "Nursing"):
            c, n = ask[(loc, ct)]
            cells["%s %s" % (loc, ct.lower())] = dict(residents=counts[(loc, ct)], contribution=round(float(c), 4),
                                                       contribution_stated=r1(c), net=round(float(n), 4),
                                                       net_stated="%s" % format(r1(n), ","))
    F = {
        "call": {W.QLABEL[k]: dict(unrounded=round(float(tot[k]), 2), stated=r10(tot[k])) for k in range(4)},
        "stock_31_december_2026": g["n_cf"],
        "pool_31_december_2026": g["n_sf"],
        "components": {W.QLABEL[k]: dict(today_residents=round(float(g["survivors"][k]), 1),
                                          direct_admissions=round(float(g["direct"][k]), 1),
                                          conversions=round(float(g["conversions"][k]), 1)) for k in range(4)},
        "direct_admissions_per_month": round(float(E.direct_rate(I, g["o"]).sum()), 2),
        "conversion_hazard_per_month_by_months_since_admission": haz,
        "pool_by_months_since_admission": pool,
        "conversions_by_year": conv_y,
        "default_path": {W.QLABEL[k]: round(float(rungs["R1"][k]), 1) for k in range(4)},
        "default_path_stated": {W.QLABEL[k]: r10(rungs["R1"][k]) for k in range(4)},
        "rungs_31_march_2028": {k: round(float(v[3]), 1) for k, v in rungs.items()},
        "ask": cells,
        "chart": {"order": order, "title_locality": top,
                  "title": "%s's nursing places cost the partnership most: £%s a week after contributions"
                           % (top, format(r1(ask[(top, "Nursing")][1]), ","))},
        "ask_stops": {k: [round(float(x), 2) for x in v] for k, v in stops.items()},
    }
    return F


def workbook(F, ask, counts, path):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    import officex as OX
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Forecast"
    ws["A1"] = "Council-funded care home residents rise to about %d by 31 March 2028" % F["call"][W.QLABEL[3]]["stated"]
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Strathallan HSCP. Residents in place at the end of each quarter-end day (budget definitions 2.1 to 2.4); records to 31 December 2026."
    ws["A2"].font = Font(italic=True, size=9, color="595959")
    hdr = ["Quarter end", "Residents (nearest 10)", "Today's residents still in place", "Direct admissions still in place",
           "Converted from self-funding, still in place", "Total, unrounded"]
    ws.append([])
    ws.append(hdr)
    thin = Side(style="thin", color="A6A6A6")
    for j in range(1, 7):
        c = ws.cell(row=4, column=j)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDEBF7")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for k, q in enumerate(W.QLABEL):
        cp = F["components"][q]
        ws.append([dt.date.fromisoformat(W.dd(W.QEND[k]).isoformat()), F["call"][q]["stated"], cp["today_residents"],
                   cp["direct_admissions"], cp["conversions"], F["call"][q]["unrounded"]])
    for r in range(5, 9):
        ws.cell(row=r, column=1).number_format = "dd/mm/yyyy"
        ws.cell(row=r, column=2).number_format = "#,##0"
        ws.cell(row=r, column=2).font = Font(bold=True)
        for j in (3, 4, 5, 6):
            ws.cell(row=r, column=j).number_format = "0.0"
    ws["A10"] = "On 31 December 2026: %d council-funded residents; %d self-funding residents receiving free personal care." % (
        F["stock_31_december_2026"], F["pool_31_december_2026"])
    ws["A11"] = ("Self-funders' moves onto council funding are projected from each resident's months since admission to the "
                 "home, with deaths and discharges competing; direct admissions at the 2024 to 2026 rate.")
    for a in ("A10", "A11"):
        ws[a].font = Font(size=9)
    for col, w in zip("ABCDEF", [14, 13, 16, 16, 18, 12]):
        ws.column_dimensions[col].width = w
    ws.row_dimensions[4].height = 46
    ws.freeze_panes = "A5"
    ws2 = wb.create_sheet("Weekly cost by locality")
    ws2["A1"] = "Council-funded residents in each locality's care homes on 31 December 2026"
    ws2["A1"].font = Font(bold=True, size=13)
    ws2["A2"] = "Locality of the home (postcode lookup). Contribution in force on 31 December 2026; contracted weekly fee including supplements. £ a week, per resident."
    ws2["A2"].font = Font(italic=True, size=9, color="595959")
    ws2.append([])
    hdr2 = ["Locality", "Care type", "Residents", "Average weekly contribution (£)", "Average weekly cost to the partnership (£)"]
    ws2.append(hdr2)
    for j in range(1, 6):
        c = ws2.cell(row=4, column=j)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDEBF7")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for loc in W.LOCS:
        for ct in ("Residential", "Nursing"):
            c, n = ask[(loc, ct)]
            ws2.append([loc, ct, counts[(loc, ct)], r1(c), r1(n)])
    for r in range(5, 15):
        for j in (4, 5):
            ws2.cell(row=r, column=j).number_format = "#,##0"
    ws2["A16"] = "Residents placed in homes outside Strathallan are in no locality and are not in the table."
    ws2["A16"].font = Font(size=9)
    for col, w in zip("ABCDE", [14, 12, 10, 17, 19]):
        ws2.column_dimensions[col].width = w
    ws2.row_dimensions[4].height = 46
    ws2.freeze_panes = "A5"
    ws3 = wb.create_sheet("Notes")
    notes = [
        ("Prepared", "Planning and Performance, 22 January 2027, for the care home line of the 2027-28 budget"),
        ("Records", "Case management and finance system extracts run 18 January 2027, records to 31 December 2026"),
        ("Who counts", "Budget definitions 2.1 to 2.4: permanent placements only; residents in hospital and in homes outside Strathallan included; self-funders receiving free personal or nursing care excluded"),
        ("Funding date", "A conversion recorded in January 2027 but effective in December 2026 counts on 31 December 2026 (definitions 1.2)"),
        ("Deaths", "Placements still open in the case system are closed at the date of death in the NRS linkage of 15 January 2027"),
        ("Self-funders", "Self-funders are the open free personal care awards in the payment lines; months since admission from the admission date on the lines"),
        ("Contribution", "The assessment in force on 31 December 2026 across all of a resident's debtor references (definitions 3.1); reviews completed early but effective in 2027 are not in force"),
        ("Weekly fee", "The placement's contracted fee on 31 December 2026 including supplements (definitions 3.2); the 2027-28 draft contract rates are not agreed and are not used"),
        ("Locality", "The locality of the home, from its postcode in the care home register and the postcode lookup; the locality on the placement is the arranging team's"),
        ("Rounding", "Residents to the nearest 10, pounds to the nearest pound, each from the unrounded figure"),
    ]
    ws3.append(["Item", "Basis"])
    for j in (1, 2):
        ws3.cell(row=1, column=j).font = Font(bold=True)
    for a, b in notes:
        ws3.append([a, b])
    ws3.column_dimensions["A"].width = 14
    ws3.column_dimensions["B"].width = 110
    OX.xlsx_from_openpyxl(wb, path, W.PEOPLE["analyst"], W.PEOPLE["analyst"], dt.datetime(2027, 1, 19, 9, 31),
                          dt.datetime(2027, 1, 22, 16, 44), seed=4101)


def chart(F, ask, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "svg.hashsalt": "t134"})
    order = F["chart"]["order"]
    res = [ask[(l, "Residential")][1] for l in order]
    nur = [ask[(l, "Nursing")][1] for l in order]
    fig, ax = plt.subplots(figsize=(9.6, 5.4), dpi=110)
    x = np.arange(len(order))
    w = 0.38
    b1 = ax.bar(x - w / 2 - 0.01, res, w, color=RES_COL, label="Residential")
    b2 = ax.bar(x + w / 2 + 0.01, nur, w, color=NUR_COL, label="Nursing")
    for bars, vals in ((b1, res), (b2, nur)):
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + 8, "£%s" % format(r1(v), ","), ha="center", va="bottom",
                    fontsize=9, color="#0b0b0b")
    ax.set_xticks(x)
    ax.set_xticklabels(order)
    ax.set_ylabel("£ a week per resident, after the resident's contribution")
    ax.set_ylim(0, max(nur + res) * 1.15)
    ax.yaxis.grid(True, color="#e3e2de", linewidth=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color("#a3a29d")
    ax.spines["bottom"].set_color("#a3a29d")
    ax.legend(frameon=False, loc="upper right", ncol=2)
    ax.set_title(F["chart"]["title"], loc="left", fontsize=12, fontweight="bold")
    fig.text(0.01, 0.01, "Council-funded residents in each locality's care homes, 31 December 2026. Localities ordered by "
             "the weekly cost of a nursing place.", fontsize=8, color="#52514e")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def main(tdir, out):
    T, I, g, rungs, ask, counts, stops = compute(tdir)
    F = figures(I, g, rungs, ask, counts, stops)
    os.makedirs(out, exist_ok=True)
    workbook(F, ask, counts, os.path.join(out, XLSX))
    chart(F, ask, os.path.join(out, PNG))
    for name, when in ((XLSX, (2027, 1, 22, 16, 44)), (PNG, (2027, 1, 22, 16, 39))):
        ts = W.posix(dt.datetime(*when))
        os.utime(os.path.join(out, name), (ts, ts))
    return F


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=os.path.join(TASK, "target"))
    ap.add_argument("--out", default=os.path.join(TASK, "golden"))
    ap.add_argument("--figures", default=os.path.join(HERE, "figures.json"))
    a = ap.parse_args()
    F = main(a.target, a.out)
    with open(a.figures, "w") as f:
        json.dump(F, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(json.dumps(F["call"]), F["chart"]["title"])
