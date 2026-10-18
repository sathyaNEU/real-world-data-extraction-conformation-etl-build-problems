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


def pallets(x):
    return int(round(x / C.PALLET))


def compute(target):
    kids, visits = PR.register_view(target)
    fam, c = LD.family(kids, visits)
    P, sig = K.P_noisy(c)
    tot, Cm = K.total(c, P)
    on_m = c.S_on.sum(0)
    sw_m = (P * c.S_c).sum(0)
    ci = call_inputs(target)
    kids_m = [int(round(float(x))) for x in Cm]
    kids_cons, kids_max = sum(kids_m), C.MAX_MONTHS * kids_m[-1]
    line2_unrounded = kids_cons + kids_max
    line1_unrounded = ci["adults"] - ci["soh"] - ci["shipped"]
    rv, info = LD.rivals(c)
    bt = LD.backtests(kids, visits)
    a, b, s, n = K.fits(c.visits, c.cand, c.fr, None, "lin")
    default = K.total(c, K.P_smooth(c))[0]
    pk = AS.Pack(target)
    ask = AS.golden(pk)
    return dict(kids=kids, visits=visits, c=c, fam=fam, P=P, sig=sig, children=tot, Cm=Cm, on_m=on_m, sw_m=sw_m,
                kids_m=kids_m, kids_cons=kids_cons, kids_max=kids_max, ci=ci,
                line1_unrounded=line1_unrounded, line1=pallets(line1_unrounded),
                line2_unrounded=line2_unrounded, line2=pallets(line2_unrounded),
                rivals=rv, info=info, backtests=bt, slope_n=n, default_children=default,
                default_line2=pallets(default), switches=K.switches(c, P), ask=ask)


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
    pal = "{:,}".format(C.PALLET)
    ws.cell(row=1, column=1, value="C7 order of TLD 30s: line 1, %d pallets; line 2, %d pallets"
            % (R["line1"], R["line2"])).font = Font(name="Calibri", bold=True, size=13)
    ws.cell(row=2, column=1, value="TDF/3TC/DTG 300/300/50 mg tablets, bottle of 30 (ARV0412), for January to June "
                                   "2027. Stock count of 31 August 2026; SOP QP-04 version 3, sections 3 and 4; "
                                   "pallets of 84 cartons of 96 bottles (%s bottles); September 2026 quantification "
                                   "review." % pal).font = N
    ws.cell(row=2, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:B3")
    _head(ws, 4, ["Line", "Bottles"], [86, 15])
    lines = [
        ("Line 1. Patients aged 15 and over at the count or starting after it: consumption, September 2026 to June "
         "2027 (programme projection)", sum(ci["adult_months"])),
        ("Line 1. Maximum stock, six months of June 2027", C.MAX_MONTHS * ci["adult_months"][-1]),
        ("Line 1. Less usable stock at the count, Main warehouse and Northern depot", -ci["soh"]),
        ("Line 1. Less confirmed shipments due by 30 June 2027 (PO-2026-0147, lots 1 to 3)", -ci["shipped"]),
        ("Line 1 before rounding", R["line1_unrounded"]),
        ("Line 1, %d pallets" % R["line1"], R["line1"] * C.PALLET),
        ("Line 2. Children under 15 at the count: consumption, September 2026 to June 2027 (paediatric register "
         "forecast)", R["kids_cons"]),
        ("Line 2. Maximum stock, six months of June 2027", R["kids_max"]),
        ("Line 2 before rounding", R["line2_unrounded"]),
        ("Line 2, %d pallets" % R["line2"], R["line2"] * C.PALLET),
    ]
    bold = {"Line 1 before rounding", "Line 2 before rounding", "Line 1, %d pallets" % R["line1"],
            "Line 2, %d pallets" % R["line2"]}
    for i, (k, v) in enumerate(lines):
        ws.cell(row=5 + i, column=1, value=k).font = B if k in bold else N
        c = ws.cell(row=5 + i, column=2, value=int(v))
        c.number_format = "#,##0;-#,##0"
        c.font = B if k in bold else N
    r0 = 5 + len(lines) + 1
    ws.cell(row=r0, column=1, value="Children under 15 on TLD at the count").font = N
    ws.cell(row=r0, column=2, value=len(R["c"].on)).number_format = "#,##0"
    ws.cell(row=r0 + 1, column=1, value="Children under 15 on a paediatric first-line regimen at the count").font = N
    ws.cell(row=r0 + 1, column=2, value=len(R["c"].cand)).number_format = "#,##0"
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
                                     "moves onto TLD at the first reading of 30.0 kg or more (Annex 7, 2026 edition), "
                                     "or, for the %.1f%% of such readings since 1 March 2026 the clinician held back, at "
                                     "the next weighed visit." % (R["sig"], 100 * R["c"].lag))
             ).alignment = Alignment(wrap_text=True, vertical="top")
    w2.merge_cells("A14:D20")
    w2.freeze_panes = "A2"
    # out of sample
    w3 = wb.create_sheet("Out of sample")
    _head(w3, 1, ["Forecast from", "Months", "TLD from", "Bottle-months the register shows",
                  "Weighings around each line", "Error", "Each line reaching the band", "Error"],
          [14, 8, 9, 18, 16, 9, 16, 9])
    for i, bt in enumerate(R["backtests"]):
        a = bt["actual"]
        vals = [bt["origin"].strftime("%d %b %Y"), bt["months"], "%.0f kg" % bt["threshold"], a, round(bt["golden"]),
                (bt["golden"] - a) / a, round(bt["smooth_all"]), (bt["smooth_all"] - a) / a]
        for j, v in enumerate(vals):
            cc = w3.cell(row=2 + i, column=1 + j, value=v)
            if j in (5, 7):
                cc.number_format = "+0.0%;-0.0%"
            elif j >= 3:
                cc.number_format = "#,##0"
    w3.cell(row=6, column=1, value=("Each forecast stood at a month end the register has closed, under the band then "
                                    "in force (TLD from 35 kg until the 2026 guidelines): the children in care on a "
                                    "paediatric first line at that date and their weighings to it, followed over the "
                                    "months shown; the register's later rows give the bottle-months they took on "
                                    "TLD.")).alignment = Alignment(wrap_text=True, vertical="top")
    w3.merge_cells("A6:H9")
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
        ("Prepared for", "Quantification review, September 2026: the C7 order of TLD 30s, lines 1 and 2 (SOP 4.3)"),
        ("Stock count", "31 August 2026, Main warehouse and Northern depot (SOP 2.1); the quarantined batch is not "
                        "usable stock (SOP 3.3); stock and shipments netted on line 1 alone (SOP 4.3)"),
        ("On order", "Lots with a supplier-confirmed delivery date on or before 30 June 2027; the C7 framework "
                     "call-off FW-2027-C7A is planned and not on order (SOP 3.3)"),
        ("Line 1", "Programme projection, September 2026 round: patients aged 15 and over on 31 August 2026 and every "
                   "patient starting treatment from 1 September 2026 (SOP 4.2)"),
        ("Line 2", "Paediatric and adolescent ART register extract of 2 September 2026: children under 15 at the count "
                   "with no outcome entered, forecast to 30 June 2027 whatever their age by then (SOP 4.2); the legacy "
                   "layout linked through the 2024 crosswalk"),
        ("Rounding", "Each line rounded once to the nearest whole pallet of %s bottles (SOP 4.4); every other figure "
                     "in whole bottles" % "{:,}".format(C.PALLET)),
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
        call=R["line2"], call_bottles=R["line2"] * C.PALLET, call_unrounded=R["line2_unrounded"],
        kids_consumption=R["kids_cons"], kids_max_stock=R["kids_max"],
        line1=R["line1"], line1_bottles=R["line1"] * C.PALLET, line1_unrounded=R["line1_unrounded"],
        adults=ci["adults"], adult_consumption=sum(ci["adult_months"]),
        adult_max_stock=C.MAX_MONTHS * ci["adult_months"][-1], soh=ci["soh"], shipped=ci["shipped"],
        on_tld=len(R["c"].on), candidates=len(R["c"].cand), sigma=round(R["sig"], 2),
        held_back_pct=round(100 * R["c"].lag, 1), held_back_n=R["c"].lag_n, threshold_kg=30.0, pallet=C.PALLET,
        sections_cited=["SOP 2.1", "SOP 3.1", "SOP 3.2", "SOP 3.3", "SOP 4.1", "SOP 4.2", "SOP 4.3", "SOP 4.4",
                        "Annex 7.1", "Annex 7.2"],
        default_line2=R["default_line2"], default_children=int(round(R["default_children"])),
        rival_band_line2=int(round(R["rivals"]["band_0.5"] / C.PALLET)),
        rival_recent_line2=int(round(R["rivals"]["recent_3"] / C.PALLET)),
        asks={"%s %s %s" % (k, r, cy): v for k, D_ in (("delivered", A), ("dispensed", Bd)) for (r, cy), v in D_.items()},
        backtest=[dict(origin=b["origin"].isoformat(), months=b["months"], threshold=b["threshold"], actual=b["actual"],
                       golden=round(b["golden"]), golden_err=round(err(b, "golden"), 1), smooth=round(b["smooth_all"]),
                       smooth_err=round(err(b, "smooth_all"), 1)) for b in bt],
        golden_miss_pct=[round(abs(err(b, "golden")), 1) for b in bt],
        line_short_pct=[round(-err(b, "smooth_all"), 1) for b in bt],
    )
    return f


def submission(R, f):
    ci = R["ci"]
    A, Bd = R["ask"]["A"], R["ask"]["B"]
    gerr = [b["golden_err"] for b in f["backtest"]]
    serr = [b["smooth_err"] for b in f["backtest"]]
    assert max(abs(e) for e in gerr) < 15.0 and min(-e for e in serr) > 50.0, (gerr, serr)
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Healthcare Delivery & Health Economics (utilization, access and demand forecasting).")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Line 2 of the C7 order should carry %d pallets of TLD 30s (%s bottles) for the children in the "
             "paediatric register.** A child on a paediatric first-line regimen moves onto TLD at the first clinic "
             "weighing that reads 30 kg or more, and a weighing scatters more than a kilogram around the child's growth "
             "line, so most of those readings come months before the line itself reaches 30 kg; forecast from each "
             "child's scheduled weighings at the child's own dispensing interval, the children's need to June 2027 with "
             "six months of June's falls in the eleventh pallet. Not %d "
             "pallets, which is what moving each child when its fitted line reaches 30 kg gives: on every window the "
             "register has closed, under the band then in force, that route fell short by %s per cent. Not the register's own switch "
             "history either, its switch rates by recorded weight or its recent count of switches, because those switches "
             "came under the 35 kg band and the monthly visits that the 2026 guidelines changed in March."
             % (R["line2"], fmt(f["call_bottles"]), f["default_line2"],
                "%.0f to %.0f" % (min(f["line_short_pct"]), max(f["line_short_pct"]))))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. Line 1 is **%d pallets (%s bottles)**: patients aged 15 and over at the count or starting treatment after "
             "it consume **%s** bottles from September 2026 to June 2027 with a maximum stock of **%s**, less **%s** "
             "bottles of usable stock and **%s** bottles of confirmed shipments."
             % (R["line1"], fmt(f["line1_bottles"]), fmt(f["adult_consumption"]), fmt(f["adult_max_stock"]),
                fmt(ci["soh"]), fmt(ci["shipped"])))
    L.append("2. **%s** children under 15 were on TLD at the count and **%s** were on a paediatric first-line regimen."
             % (fmt(len(R["c"].on)), fmt(len(R["c"].cand))))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Summed the national row of %s from September 2026 to June 2027 (SOP QP-04, 4.1 and 4.2) with six months "
             "of June 2027 as the maximum stock (3.2), and took the usable batches at both warehouses and the lots with a "
             "confirmed delivery date from %s (2.1, 3.1 and 3.3): line 1 is %s bottles before rounding, %d pallets (4.3 "
             "and 4.4)." % (PK.F_PROJ, PK.F_STOCK, fmt(f["line1_unrounded"]), R["line1"]))
    L.append("2. Read the register's two layouts as one history: legacy ART numbers linked to the national identifier "
             "through %s, legacy regimen lines coded with %s, the June 2024 visits kept once and EPR rows re-sent after "
             "a failed sync dropped." % (PK.F_CW, PK.F_CODES))
    L.append("3. Took the children born after 31 August 2011 with no outcome entered in %s: %s on TLD and %s on a "
             "paediatric first-line regimen." % (PK.F_PTS, fmt(len(R["c"].on)), fmt(len(R["c"].cand))))
    L.append("4. Fitted a straight line in kilograms to each first-line child's weighings since January 2023 and "
             "scheduled its visits to June 2027 from its next appointment at its months-dispensed interval; the "
             "residual standard deviation around the lines, two parameters fitted per child, is %.2f kg." % R["sig"])
    L.append("5. Took each scheduled visit as weighed at the register's share of clinical visits over the last 12 months, "
             "the reading scattered around the child's line at that spread, and moved the child onto TLD at its first "
             "reading of 30.0 kg or more (Annex 7, 7.1 and 7.2), or at the next weighed visit for the %.1f per cent of "
             "the %s such readings since 1 March 2026 that the register shows held back; every child was kept at the "
             "register's exit rates of the last 12 months for children under 12 and 12 and over (SOP 4.1)."
             % (f["held_back_pct"], fmt(f["held_back_n"])))
    L.append("6. Stood the same forecast at three month ends the register has closed, under the band then in force "
             "(35 kg), followed for twelve months from the first two and six from the third (%s): it came within %s per "
             "cent of the bottle-months the register shows each time, while moving each child when its line reaches the "
             "band fell short by %s per cent." % (", ".join(b["origin"] for b in f["backtest"]),
                                                  "%.0f" % max(f["golden_miss_pct"]),
                                                  "%.0f to %.0f" % (min(f["line_short_pct"]), max(f["line_short_pct"]))))
    L.append("7. Counted one bottle for each child on TLD at each month's end with six months of June 2027 (SOP 4.1, 4.3), "
             "%s bottles on this construction, and rounded to the nearest pallet of %s bottles (4.4): %d pallets."
             % (fmt(f["call_unrounded"]), fmt(C.PALLET), R["line2"]))
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### %s" % G_XLSX)
    L.append("")
    L.append("1. Line 2 of the C7 order is %d pallets of TLD 30s (%s bottles)." % (R["line2"], fmt(f["call_bottles"])))
    L.append("2. Line 1 is %d pallets (%s bottles): consumption %s bottles and maximum stock %s bottles for patients aged "
             "15 and over at the count or starting treatment after it, netting %s bottles of usable stock and %s bottles "
             "of confirmed shipments." % (R["line1"], fmt(f["line1_bottles"]), fmt(f["adult_consumption"]),
                                          fmt(f["adult_max_stock"]), fmt(ci["soh"]), fmt(ci["shipped"])))
    L.append("3. %s children under 15 were on TLD at the count and %s on a paediatric first-line regimen."
             % (fmt(len(R["c"].on)), fmt(len(R["c"].cand))))
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
