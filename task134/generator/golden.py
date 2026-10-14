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
    adm = I["sf_admit"][on]
    pool_since = {"1 January %d" % y: int((adm >= W.dn(dt.date(y, 1, 1))).sum()) for y in (2025, 2026)}
    pool_ye = {}
    for y in range(2021, 2027):
        d = W.dn(dt.date(y, 12, 31))
        pool_ye[str(y)] = int(((I["sf_entry"] <= d) & (I["sf_end"] > d)).sum())
    conv_y = {}
    for y in range(2021, 2027):
        a0, a1 = W.dn(dt.date(y, 1, 1)), W.dn(dt.date(y + 1, 1, 1))
        conv_y[str(y)] = int(((I["cf_route"] == "CONV") & (I["cf_entry"] >= a0) & (I["cf_entry"] < a1)).sum())
    cells = {}
    for loc in W.LOCS:
        for ct in ("Residential", "Nursing"):
            f, n = ask[(loc, ct)]
            cells["%s %s" % (loc, ct.lower())] = dict(residents=counts[(loc, ct)], fee=round(float(f), 4),
                                                       fee_stated="%s" % format(r1(f), ","), net=round(float(n), 4),
                                                       net_stated="%s" % format(r1(n), ","))
    m = g["measure"]
    F = {
        "call": {W.QLABEL[k]: dict(unrounded=round(float(tot[k]), 2), stated=r10(tot[k])) for k in range(4)},
        "stock_31_december_2026": g["n_cf"],
        "pool_31_december_2026": g["n_sf"],
        "components": {W.QLABEL[k]: dict(today_residents=round(float(g["survivors"][k]), 1),
                                          direct_admissions=round(float(g["direct"][k]), 1),
                                          conversions=round(float(g["conversions"][k]), 1)) for k in range(4)},
        "direct_admissions_per_month": round(float(E.direct_rate(I, g["o"]).sum()), 2),
        "stage_1": {"date": "6 April 2026", "rise": E.RISE1, "conversions_that_day": m["on_day"],
                    "ordinary_week": round(m["flow"], 3), "ordinary_week_stated": "%.2f" % m["flow"],
                    "conversions_in_the_52_weeks_before": int(round(m["flow"] * 52)),
                    "excess": round(m["excess"], 2), "weeks": round(m["w1"], 2)},
        "stage_2": {"date": "5 April 2027", "rise": E.RISE2, "weeks": round(g["w2"], 2)},
        "upper_capital_limit": {"to 5 April 2026": W.CAPITAL[2025][1], "from 6 April 2026": W.CAPITAL[2026][1],
                                "from 5 April 2027": W.CAPITAL[2027][1]},
        "ordinary_week_window_weeks": 52,
        "pool_on_6_april_2026_still_self_funding": int((I["sf_admit"][E.pool(I)] < E.D1).sum()),
        "conversion_hazard_per_month_by_months_since_admission": haz,
        "pool_by_months_since_admission": pool,
        "pool_admitted_since": pool_since,
        "pool_at_year_end": pool_ye,
        "conversions_by_year": conv_y,
        "default_path": {W.QLABEL[k]: round(float(rungs["R5"][k]), 1) for k in range(4)},
        "default_path_stated": {W.QLABEL[k]: r10(rungs["R5"][k]) for k in range(4)},
        "rungs": {k: {W.QLABEL[j]: round(float(v[j]), 1) for j in range(4)} for k, v in rungs.items()},
        "ask": cells,
        "chart": {"order": list(W.LOCS)},
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
                 "home, with deaths and discharges competing and the capital clocks moved on by the April 2026 and April "
                 "2027 rises in the upper capital limit; direct admissions at the 2024 to 2026 rate.")
    for a in ("A10", "A11"):
        ws[a].font = Font(size=9)
    for col, w in zip("ABCDEF", [14, 13, 16, 16, 18, 12]):
        ws.column_dimensions[col].width = w
    ws.row_dimensions[4].height = 46
    ws.freeze_panes = "A5"
    ws2 = wb.create_sheet("Weekly cost by locality")
    rn = [r1(ask[(l, "Residential")][1]) for l in W.LOCS]
    nn = [r1(ask[(l, "Nursing")][1]) for l in W.LOCS]
    ws2["A1"] = ("A council-funded place costs the partnership £%d to £%d a week residential and £%d to £%d nursing after "
                 "contributions" % (min(rn), max(rn), min(nn), max(nn)))
    ws2["A1"].font = Font(bold=True, size=13)
    ws2["A2"] = ("Locality of the home (postcode lookup). Weekly fee at the 2026-27 contract rate agreed on 6 November 2026, "
                 "with supplements; contribution in force on 31 December 2026. £ a week, per resident.")
    ws2["A2"].font = Font(italic=True, size=9, color="595959")
    ws2.append([])
    hdr2 = ["Locality", "Care type", "Residents", "Average weekly fee (£)", "Average weekly cost to the partnership after contributions (£)"]
    ws2.append(hdr2)
    for j in range(1, 6):
        c = ws2.cell(row=4, column=j)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDEBF7")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for loc in W.LOCS:
        for ct in ("Residential", "Nursing"):
            f, n = ask[(loc, ct)]
            ws2.append([loc, ct, counts[(loc, ct)], r1(f), r1(n)])
    for r in range(5, 15):
        for j in (4, 5):
            ws2.cell(row=r, column=j).number_format = "#,##0"
    ws2["A16"] = "Residents placed in homes outside Strathallan are in no locality and are not in the table."
    ws2["A16"].font = Font(size=9)
    for col, w in zip("ABCDE", [14, 12, 10, 14, 22]):
        ws2.column_dimensions[col].width = w
    ws2.row_dimensions[4].height = 58
    ws2.freeze_panes = "A5"
    ws3 = wb.create_sheet("Notes")
    notes = [
        ("Prepared", "Planning and Performance, 22 January 2027, for the care home line of the 2027-28 budget"),
        ("Records", "Case management and finance system extracts run 18 January 2027, records to 31 December 2026"),
        ("Who counts", "Budget definitions 2.1 to 2.4: permanent placements only; residents in hospital and in homes outside Strathallan included; self-funders receiving free personal or nursing care excluded"),
        ("Funding date", "A conversion recorded in January 2027 but effective in December 2026 counts on 31 December 2026 (definitions 1.2)"),
        ("Deaths", "Placements still open in the case system are closed at the date of death in the NRS linkage of 15 January 2027"),
        ("Self-funders", "Self-funders are the open free personal care awards in the payment lines; months since admission from the admission date on the lines"),
        ("Capital limits", "The upper limit rose by £5,000 on 6 April 2026 and rises by £7,000 on 5 April 2027 (charging policy 3.2). 6 April 2026 brought %d conversions against %s in an ordinary week (the 52 weeks before), %s weeks' worth; 5 April 2027 is taken as %s weeks' worth (7,000 / 5,000 of it): every self-funder's capital reaches the limit that much sooner, those within it converting that day" % (
            F["stage_1"]["conversions_that_day"], F["stage_1"]["ordinary_week_stated"], "%.2f" % F["stage_1"]["weeks"], "%.2f" % F["stage_2"]["weeks"])),
        ("Weekly fee", "The fee payable under the placement's contract on 31 December 2026 (definitions 3.2): the 2026-27 national rate agreed on 6 November 2026 and backdated to 1 April 2026, plus the resident's supplement; the case system still carries the interim rate on 2026-27 episodes. The 2027-28 draft rates are not agreed and are not used"),
        ("Contribution", "The assessment in force on 31 December 2026 across all of a resident's debtor references (definitions 3.1); reviews completed early but effective in 2027 are not in force"),
        ("Locality", "The locality of the home, from its postcode in the care home register and the postcode lookup; the locality on the placement is the team holding the case"),
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
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: "£%s" % format(int(round(v)), ",")))
    ax.yaxis.grid(True, color="#e3e2de", linewidth=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color("#a3a29d")
    ax.spines["bottom"].set_color("#a3a29d")
    ax.legend(frameon=False, loc="upper right", ncol=2)
    ax.set_title("A council-funded nursing place costs the partnership £%d to £%d a week"
                 % (min(r1(v) for v in nur), max(r1(v) for v in nur)), loc="left", fontsize=12, fontweight="bold")
    fig.text(0.01, 0.072, "Council-funded residents in each locality's care homes on 31 December 2026; homes outside "
             "Strathallan not shown.", fontsize=8, color="#52514e")
    fig.text(0.01, 0.042, "Weekly fee at the 2026-27 contract rate agreed on 6 November 2026, with supplements, less the "
             "contribution in force on 31 December 2026.", fontsize=8, color="#52514e")
    fig.text(0.01, 0.012, "Source: case management and finance system extracts of 18 January 2027; contract rates; care "
             "home register and postcode lookup. Planning and Performance.", fontsize=8, color="#52514e")
    fig.tight_layout(rect=(0, 0.09, 1, 1))
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
    print(json.dumps(F["call"]))
