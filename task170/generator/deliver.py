"""The golden deliverables, figures.json and submission.md, computed from the cut pack (pack_read.py, asks.py,
ladder.py) and written once."""
from __future__ import annotations

import datetime as dt
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402
import numpy as np  # noqa: E402
import openpyxl  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill  # noqa: E402
from openpyxl.utils import get_column_letter  # noqa: E402

import asks as AS  # noqa: E402
import calc as K  # noqa: E402
import common as C  # noqa: E402
import ladder as LD  # noqa: E402
import pack as PK  # noqa: E402
import pack_read as PR  # noqa: E402
import postprocess as PP  # noqa: E402

D = dt.date
G_XLSX = "c7_tld_order.xlsx"
G_PNG = "c4_c5_tld_flows.png"
MONTHS = ["Sep 2026", "Oct 2026", "Nov 2026", "Dec 2026", "Jan 2027", "Feb 2027", "Mar 2027", "Apr 2027", "May 2027",
          "Jun 2027"]


def call_inputs(target):
    wb = openpyxl.load_workbook(os.path.join(target, PK.F_PROJ))
    ws = wb["Projection"]
    rows = [[c.value for c in r] for r in ws.iter_rows(min_row=5, max_row=11)]
    nat = rows[-1][1:]
    adults = sum(nat) + C.MAX_MONTHS * nat[-1]
    st = openpyxl.load_workbook(os.path.join(target, PK.F_STOCK))
    soh = sum(r[5] for r in st["Stock on hand"].iter_rows(min_row=2, values_only=True) if r[4] == "Usable")
    conf = [(r[0], r[1], r[3], r[4]) for r in st["On order"].iter_rows(min_row=2, values_only=True) if r[5] == "Confirmed"]
    return dict(adult_months=nat, adults=adults, soh=soh, shipments=conf, shipped=sum(x[2] for x in conf))


def compute(target):
    kids, visits = PR.register_view(target)
    fam, c = LD.family(kids, visits)
    P, sig = K.P_noisy(c, thr=30.0)
    tot, Cm = K.total(c, P)
    on_m = c.S_on.sum(0)
    sw_m = (P * c.S_c).sum(0)
    ci = call_inputs(target)
    kids_m = [int(round(float(x))) for x in Cm]
    kids_cons, kids_max = sum(kids_m), C.MAX_MONTHS * kids_m[-1]
    unrounded = ci["adults"] + kids_cons + kids_max - ci["soh"] - ci["shipped"]
    order = int(C.LOT * round(unrounded / C.LOT))
    rv, info = LD.rivals(c)
    bt = LD.backtests(kids, visits)
    a, b, s, n = K.fits(c.visits, c.cand, c.fr, None, "lin")
    P_sm = K.P_smooth(c)
    default = K.total(c, P_sm)[0]
    pk = AS.Pack(target)
    ask = AS.golden(pk)
    return dict(kids=kids, visits=visits, c=c, fam=fam, P=P, sig=sig, children=tot, Cm=Cm, on_m=on_m, sw_m=sw_m,
                kids_m=kids_m, kids_cons=kids_cons, kids_max=kids_max,
                ci=ci, unrounded=unrounded, order=order, rivals=rv, info=info, backtests=bt, slope_n=n,
                default_children=default, default_order=int(C.LOT * round((ci["adults"] + default - ci["soh"] - ci["shipped"]) / C.LOT)),
                switches=K.switches(c, P), ask=ask)


def fmt(x):
    return "{:,}".format(int(round(x)))


# ---------------------------------------------------------------------------------------------------- workbook
HEAD = PatternFill("solid", fgColor="DCE6E0")
B = Font(name="Calibri", bold=True, size=11)
N = Font(name="Calibri", size=11)


def _head(ws, row, vals, widths=None):
    for j, v in enumerate(vals):
        c = ws.cell(row=row, column=j + 1, value=v)
        c.font = B
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="top")
    if widths:
        for j, w in enumerate(widths):
            ws.column_dimensions[get_column_letter(j + 1)].width = w


def write_xlsx(R, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "C7 order"
    ci = R["ci"]
    ws.cell(row=1, column=1, value="C7 order of TLD 30s: %s bottles" % fmt(R["order"])).font = Font(name="Calibri", bold=True, size=13)
    ws.cell(row=2, column=1, value="TDF/3TC/DTG 300/300/50 mg tablets, bottle of 30 (ARV0412), for January to June "
                                   "2027. Stock count of 31 August 2026; SOP QP-04 version 3, sections 3 and 4; "
                                   "September 2026 quantification review.").font = N
    ws.cell(row=2, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:B3")
    _head(ws, 4, ["Line", "Bottles"], [84, 15])
    lines = [
        ("Patients aged 15 and over at the count or starting after it: consumption, September 2026 to June 2027 "
         "(programme projection)", sum(ci["adult_months"])),
        ("Patients aged 15 and over at the count or starting after it: maximum stock, six months of June 2027",
         C.MAX_MONTHS * ci["adult_months"][-1]),
        ("Children under 15 at the count: consumption, September 2026 to June 2027 (paediatric register forecast)",
         R["kids_cons"]),
        ("Children under 15 at the count: maximum stock, six months of June 2027", R["kids_max"]),
        ("Forecast need", ci["adults"] + R["kids_cons"] + R["kids_max"]),
        ("Less usable stock at the count, Main warehouse and Northern depot", -ci["soh"]),
        ("Less confirmed shipments due by 30 June 2027 (PO-2026-0147, lots 1 to 3)", -ci["shipped"]),
        ("Order before rounding", R["unrounded"]),
    ]
    for i, (k, v) in enumerate(lines):
        ws.cell(row=5 + i, column=1, value=k).font = B if k in ("Forecast need", "Order before rounding") else N
        c = ws.cell(row=5 + i, column=2, value=int(v))
        c.number_format = "#,##0;-#,##0"
        c.font = N
    r0 = 5 + len(lines)
    ws.cell(row=r0, column=1, value="C7 order, nearest 5,000 bottles").font = B
    c = ws.cell(row=r0, column=2, value=R["order"])
    c.number_format = "#,##0"
    c.font = B
    ws.cell(row=r0 + 2, column=1, value="Children under 15 on TLD at the count").font = N
    ws.cell(row=r0 + 2, column=2, value=len(R["c"].on)).number_format = "#,##0"
    ws.cell(row=r0 + 3, column=1, value="Children under 15 on a paediatric first-line regimen at the count").font = N
    ws.cell(row=r0 + 3, column=2, value=len(R["c"].cand)).number_format = "#,##0"
    ws.freeze_panes = "A5"
    ws.print_title_rows = "4:4"
    # children by month
    w2 = wb.create_sheet("Children")
    _head(w2, 1, ["Month end", "On TLD at the count, still in care", "Moved onto TLD after the count, in care",
                  "Children on TLD (bottles)"], [12, 22, 24, 18])
    for k, m in enumerate(MONTHS):
        w2.cell(row=2 + k, column=1, value=m)
        on_k = int(round(float(R["on_m"][k])))
        for j, v in enumerate((on_k, R["kids_m"][k] - on_k, R["kids_m"][k])):
            cc = w2.cell(row=2 + k, column=2 + j, value=v)
            cc.number_format = "#,##0"
    w2.cell(row=12, column=1, value="Total").font = B
    cc = w2.cell(row=12, column=4, value=R["kids_cons"])
    cc.number_format = "#,##0"
    cc.font = B
    w2.cell(row=14, column=1, value=("Expected children in care on TLD at each month's end, one bottle each (SOP 4.1). "
                                     "Children on TLD at the count are carried at the register's exit rates of the last "
                                     "12 months, under 12 and 12 and over. Each child on a paediatric first-line "
                                     "regimen: a straight line through every weighing since January 2023; each "
                                     "scheduled visit to June 2027, at the child's months-dispensed interval from the "
                                     "next appointment, is weighed at the share of clinical visits of the last 12 "
                                     "months and the reading scatters around the line (residual SD %.2f kg); the child "
                                     "moves onto TLD at the first reading of 30.0 kg or more (Annex 7.2)." % R["sig"])
             ).alignment = Alignment(wrap_text=True, vertical="top")
    w2.merge_cells("A14:D19")
    w2.freeze_panes = "A2"
    # out of sample
    w3 = wb.create_sheet("Out of sample")
    _head(w3, 1, ["Forecast from", "Months", "Bottle-months the register shows", "Weighings around each line",
                  "Error", "Each line reaching 30 kg", "Error", "Switch rates by recorded weight band", "Error"],
          [14, 8, 18, 16, 9, 16, 9, 18, 9])
    for i, bt in enumerate(R["backtests"]):
        a = bt["actual"]
        vals = [bt["origin"].strftime("%d %b %Y"), bt["months"], a, round(bt["golden"]), (bt["golden"] - a) / a,
                round(bt["smooth_all"]), (bt["smooth_all"] - a) / a, round(bt["band_0.5"]), (bt["band_0.5"] - a) / a]
        for j, v in enumerate(vals):
            cc = w3.cell(row=2 + i, column=1 + j, value=v)
            if j in (4, 6, 8):
                cc.number_format = "+0.0%;-0.0%"
            elif j >= 2:
                cc.number_format = "#,##0"
    w3.cell(row=6, column=1, value=("Each route stood at a month end the register has closed: the children in care on "
                                    "a paediatric first line at that date and their weighings to it, followed over the "
                                    "months shown; the register's later rows give the bottle-months they took on "
                                    "TLD.")).alignment = Alignment(wrap_text=True, vertical="top")
    w3.merge_cells("A6:I8")
    w3.freeze_panes = "B2"
    # regions
    w4 = wb.create_sheet("Regions C4 C5")
    _head(w4, 1, ["Region", "Delivered C4 (Jul-Dec 2025)", "Delivered C5 (Jan-Jun 2026)", "Dispensed C4 (Jul-Dec 2025)",
                  "Dispensed C5 (Jan-Jun 2026)"], [14, 18, 18, 18, 18])
    A, Bd = R["ask"]["A"], R["ask"]["B"]
    for i, reg in enumerate(AS.REGIONS):
        for j, v in enumerate((reg, A[(reg, "C4")], A[(reg, "C5")], Bd[(reg, "C4")], Bd[(reg, "C5")])):
            cc = w4.cell(row=2 + i, column=1 + j, value=v)
            if j:
                cc.number_format = "#,##0"
    w4.cell(row=8, column=1, value="All regions").font = B
    for j, v in enumerate((sum(A[(r, "C4")] for r in AS.REGIONS), sum(A[(r, "C5")] for r in AS.REGIONS),
                           sum(Bd[(r, "C4")] for r in AS.REGIONS), sum(Bd[(r, "C5")] for r in AS.REGIONS))):
        cc = w4.cell(row=8, column=2 + j, value=v)
        cc.number_format = "#,##0"
        cc.font = B
    w4.cell(row=10, column=1, value=("Bottles of TLD 30s. Each facility in its region in the facility registry as drawn "
                                     "from 1 April 2026; a facility code reissued to a new site counts the closed site "
                                     "to its closure and the new site from its opening. Deliveries: CMS customer "
                                     "deliveries dated by the proof of delivery, those refused at the gate left out. "
                                     "Dispensing: each facility's approved eLMIS report for the month, the partner's "
                                     "donated TLD included.")).alignment = Alignment(wrap_text=True, vertical="top")
    w4.merge_cells("A10:E14")
    w4.freeze_panes = "B2"
    # notes
    w5 = wb.create_sheet("Notes")
    _head(w5, 1, ["Item", "Note"], [22, 100])
    notes = [
        ("Prepared for", "Quantification review, September 2026: the C7 order of TLD 30s"),
        ("Stock count", "31 August 2026, Main warehouse and Northern depot (SOP 2.1); the quarantined batch is not "
                        "usable stock (SOP 3.3)"),
        ("On order", "Lots with a supplier-confirmed delivery date on or before 30 June 2027; the C7 framework "
                     "call-off FW-2027-C7A is planned and not on order (SOP 3.3)"),
        ("Patients 15 and over", "Programme projection, September 2026 round: patients aged 15 and over on 31 August "
                                 "2026 and every patient starting treatment from 1 September 2026 (SOP 4.2)"),
        ("Children under 15", "Paediatric and adolescent ART register extract of 2 September 2026: children under 15 "
                              "at the count with no outcome entered, forecast to 30 June 2027 whatever their age by "
                              "then (SOP 4.2); the legacy layout linked through the 2024 crosswalk"),
        ("Rounding", "Every line in whole bottles; the order rounded once to the nearest 5,000 bottles"),
    ]
    for i, (k, v) in enumerate(notes):
        w5.cell(row=2 + i, column=1, value=k).font = N
        cc = w5.cell(row=2 + i, column=2, value=v)
        cc.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)
    PP.normalize_ooxml(path, C.PEOPLE["quant_lead"], C.PEOPLE["quant_lead"], "2026-09-14T07:30:00Z",
                       "2026-09-18T15:12:00Z", excel=True, company=C.ORG)


def write_png(R, path):
    ch = R["ask"]["chart"]
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.9), dpi=110, sharey=True)
    x = np.arange(len(AS.REGIONS))
    top = max(max(ch["delivered"].values()), max(ch["dispensed"].values()))
    for ax, cy, span in zip(axes, ("C4", "C5"), ("July to December 2025", "January to June 2026")):
        dv = [ch["delivered"][(r, cy)] for r in AS.REGIONS]
        sp = [ch["dispensed"][(r, cy)] for r in AS.REGIONS]
        b1 = ax.bar(x - 0.2, dv, 0.4, color="#2f6f57", label="Delivered by CMS (signed for)")
        b2 = ax.bar(x + 0.2, sp, 0.4, color="#a9c7b6", label="Dispensed (approved reports)")
        for bars, vals in ((b1, dv), (b2, sp)):
            for bb, v in zip(bars, vals):
                ax.text(bb.get_x() + bb.get_width() / 2, v + top * 0.012, "{:,}".format(v), rotation=90, ha="center",
                        va="bottom", fontsize=7.2, color="#1d2126")
        ax.set_xticks(x)
        ax.set_xticklabels(AS.REGIONS, fontsize=8.5)
        ax.set_title("%s, %s" % (cy, span), fontsize=10)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: "{:,.0f}".format(v)))
    axes[0].set_ylabel("Bottles of 30 tablets")
    axes[0].set_ylim(0, top * 1.30)
    axes[1].legend(frameon=False, fontsize=8, loc="upper right")
    c5_short = [r for r in AS.REGIONS if ch["dispensed"][(r, "C5")] > ch["delivered"][(r, "C5")]]
    if len(c5_short) == len(AS.REGIONS):
        title = "TLD 30s by region: in C5 every region's facilities dispensed more than CMS delivered to them"
    else:
        title = "TLD 30s by region: CMS deliveries and facility dispensing, C4 and C5"
    fig.suptitle(title, fontsize=11)
    fig.text(0.01, 0.01, "Regions as drawn from 1 April 2026. Deliveries by proof-of-delivery date; dispensing from "
                         "approved monthly reports.", fontsize=7, color="#5b6169")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


# ---------------------------------------------------------------------------------------------------- figures, write-up
def figures(R):
    ci = R["ci"]
    A, Bd = R["ask"]["A"], R["ask"]["B"]
    bt = R["backtests"]
    err = lambda b, k: 100.0 * (b[k] - b["actual"]) / b["actual"]
    f = dict(
        order=R["order"], adults=ci["adults"], adult_consumption=sum(ci["adult_months"]),
        adult_max_stock=C.MAX_MONTHS * ci["adult_months"][-1], soh=ci["soh"], shipped=ci["shipped"],
        on_tld=len(R["c"].on), candidates=len(R["c"].cand), sigma=round(R["sig"], 2), threshold_kg=30.0,
        rounding_step=C.LOT, sections_cited=["SOP 2.1", "SOP 3.1", "SOP 3.2", "SOP 3.3", "SOP 4.1", "SOP 4.2",
                                             "Annex 7.1", "Annex 7.2"],
        default_order=R["default_order"],
        rival_band_order=int(C.LOT * round((ci["adults"] + R["rivals"]["band_0.5"] - ci["soh"] - ci["shipped"]) / C.LOT)),
        rival_recent_order=int(C.LOT * round((ci["adults"] + R["rivals"]["recent_3"] - ci["soh"] - ci["shipped"]) / C.LOT)),
        asks={"%s %s %s" % (k, r, cy): v for k, D_ in (("delivered", A), ("dispensed", Bd)) for (r, cy), v in D_.items()},
        backtest=[dict(origin=b["origin"].isoformat(), months=b["months"], actual=b["actual"], golden=round(b["golden"]),
                       golden_err=round(err(b, "golden"), 1), smooth=round(b["smooth_all"]),
                       smooth_err=round(err(b, "smooth_all"), 1), band=round(b["band_0.5"]),
                       band_err=round(err(b, "band_0.5"), 1)) for b in bt],
    )
    return f


def submission(R, f):
    ci = R["ci"]
    A, Bd = R["ask"]["A"], R["ask"]["B"]
    bt = R["backtests"]
    gold_max = max(abs(b["golden_err"]) for b in f["backtest"])
    smooth_min = min(-b["smooth_err"] for b in f["backtest"])
    assert gold_max < 10.0 and smooth_min > 200.0 / 3, (gold_max, smooth_min)
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Healthcare Delivery & Health Economics (utilization, access and demand forecasting).")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**The C7 order should carry %s bottles of TLD.** Each child under 15 moves onto TLD at the first scheduled "
             "weighing that reads 30 kg or more, and because a weighing scatters more than a kilogram around the child's "
             "growth line, that reading comes months before the line itself reaches 30 kg; forecast that way, the "
             "children's switches came within a tenth of what the register shows on every window it has closed. Not "
             "an order that moves each child when its fitted growth line reaches 30 kg, which waits for the line and "
             "fell short by two thirds or more on every closed window. Not the register's switch rates by recorded "
             "weight band or its recent switch count carried forward, which carry over what other children did at "
             "other points of their growth rather than when these children will be weighed." % fmt(R["order"]))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. Patients aged 15 and over at the count or starting treatment after it consume **%s** bottles from "
             "September 2026 to June 2027, and their maximum stock is **%s** bottles."
             % (fmt(f["adult_consumption"]), fmt(f["adult_max_stock"])))
    L.append("2. Usable stock at the count is **%s** bottles and confirmed shipments due by 30 June 2027 are **%s** "
             "bottles." % (fmt(ci["soh"]), fmt(ci["shipped"])))
    L.append("3. **%s** children under 15 were on TLD at the count and **%s** were on a paediatric first-line regimen."
             % (fmt(len(R["c"].on)), fmt(len(R["c"].cand))))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Summed the national row of %s from September 2026 to June 2027 (SOP QP-04, 4.1 and 4.2) and took six "
             "months of June 2027 as the maximum stock (3.2): %s and %s bottles."
             % (PK.F_PROJ, fmt(f["adult_consumption"]), fmt(f["adult_max_stock"])))
    L.append("2. Took the usable batches at both warehouses and the lots with a confirmed delivery date from %s (SOP "
             "2.1, 3.1 and 3.3): %s and %s bottles." % (PK.F_STOCK, fmt(ci["soh"]), fmt(ci["shipped"])))
    L.append("3. Read the register's two layouts as one history: legacy ART numbers linked to the national identifier "
             "through %s, legacy regimen lines coded with %s, the June 2024 visits kept once and EPR rows re-sent after "
             "a failed sync dropped." % (PK.F_CW, PK.F_CODES))
    L.append("4. Took the children born after 31 August 2011 with no outcome entered in %s: %s on TLD and %s on a "
             "paediatric first-line regimen." % (PK.F_PTS, fmt(len(R["c"].on)), fmt(len(R["c"].cand))))
    L.append("5. Fitted a straight line in kilograms to each first-line child's weighings since January 2023 and "
             "scheduled its visits to June 2027 from its next appointment at its months-dispensed interval; the "
             "residual standard deviation around the lines, two parameters fitted per child, is %.2f kg." % R["sig"])
    L.append("6. Took each scheduled visit as weighed at the register's share of clinical visits over the last 12 "
             "months, the reading scattered around the child's line at that spread, moved the child onto TLD at its "
             "first reading of 30.0 kg or more (Annex 7, 7.1 and 7.2), and kept every child at the register's exit "
             "rates of the last 12 months for children under 12 and over 12.")
    L.append("7. Stood the same forecast at 31 August 2025 over 12 months and at 31 December 2025 and 28 February 2026 "
             "over 6 months: within a tenth of the bottle-months the register shows for those children each time, while "
             "moving each child when its line reaches 30 kg fell short by two thirds or more each time.")
    L.append("8. Counted one bottle for each child on TLD at each month's end with six months of June 2027 (SOP 4.1 "
             "and 3.2), added the patients aged 15 and over, netted the stock and shipments and rounded to the "
             "nearest 5,000: %s bottles." % fmt(R["order"]))
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### %s" % G_XLSX)
    L.append("")
    L.append("1. The C7 order is %s bottles of TLD 30s." % fmt(R["order"]))
    L.append("2. For patients aged 15 and over at the count or starting treatment after it, consumption is %s bottles "
             "and maximum stock %s bottles." % (fmt(f["adult_consumption"]), fmt(f["adult_max_stock"])))
    L.append("3. The order nets %s bottles of usable stock and %s bottles of confirmed shipments."
             % (fmt(ci["soh"]), fmt(ci["shipped"])))
    L.append("4. Bottles delivered by CMS to each region's ART facilities, dated by when they were signed for, and "
             "bottles those facilities reported dispensing, whole bottles:")
    for reg in AS.REGIONS:
        L.append("   - %s: delivered %s in C4 and %s in C5; dispensed %s in C4 and %s in C5"
                 % (reg, fmt(A[(reg, "C4")]), fmt(A[(reg, "C5")]), fmt(Bd[(reg, "C4")]), fmt(Bd[(reg, "C5")])))
    L.append("")
    L.append("### %s" % G_PNG)
    L.append("")
    L.append("1. Two panels, C4 and C5: for each region a bar of the bottles CMS delivered and a bar of the bottles its "
             "facilities reported dispensing, each labelled with its figure in the table above.")
    return "\n".join(L) + "\n"


def main(target, golden_dir, fig_path, sub_path):
    os.makedirs(golden_dir, exist_ok=True)
    R = compute(target)
    write_xlsx(R, os.path.join(golden_dir, G_XLSX))
    write_png(R, os.path.join(golden_dir, G_PNG))
    f = figures(R)
    open(fig_path, "w").write(json.dumps(f, indent=1, sort_keys=True) + "\n")
    open(sub_path, "w").write(submission(R, f))
    return R, f
