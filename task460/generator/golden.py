"""The golden deliverables, computed from the shipped files only: the recommendation memo to the Capital Committee
(PDF, with the chart) and the store-by-hour conformed file (CSV); and generator/figures.json."""
import csv
import datetime as dt
import io
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import methods as M     # noqa: E402
import world as W       # noqa: E402

H = 8760
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def r2(x):
    return float("%.2f" % x)


def compute(target):
    D = M.load(target)
    g = M.golden(D)
    R = M.rungs(D)
    A = M.asks(target, D, g)
    code_of = {st: s["area"] for st, s in D["stores"].items()}
    st_of = {v: k for k, v in code_of.items()}
    order = sorted(g, key=lambda st: -g[st]["rate"])
    pick, second = order[0], order[1]
    rows = {}
    for st in g:
        c = code_of[st]
        rows[c] = dict(store=st, area=c, town=W.AREAS[c]["name"], name=D["stores"][st]["name"], rate=g[st]["rate"],
                       rate2=r2(g[st]["rate"]), mwh=g[st]["mwh"], tonnes=g[st]["tonnes"], use=A[st]["use_mwh"],
                       use0=int(round(A[st]["use_mwh"])), share=A[st]["share"], share1=float("%.1f" % A[st]["share"]),
                       price=A[st]["price"], price0=int(round(A[st]["price"])), months=A[st]["months"],
                       array_months=A[st]["array_months"], avg=R[st]["avg"], nb=R[st]["nb"], fossil=R[st]["fossil"],
                       pooled=R[st]["pooled"], all_hours=R[st]["all_hours"], hourly_average=R[st]["hourly_average"])
    WP = M.ask_wrong_paths(target, D, g)
    loss = sorted(100.0 * (WP[st]["supplier"] / A[st]["use_mwh"] - 1.0) for st in g)
    return dict(D=D, g=g, R=R, A=A, rows=rows, order=[code_of[s] for s in order], pick=code_of[pick],
                second=code_of[second], gap=g[pick]["rate"] - g[second]["rate"], st_of=st_of, loss=(loss[0], loss[-1]))


# ---------------------------------------------------------------------------------------------- the chart
def chart_png(X):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["font.family"] = "DejaVu Sans"
    rows = X["rows"]
    order = X["order"]
    fig, axes = plt.subplots(2, 4, figsize=(7.2, 3.9), dpi=150, sharey=True)
    x = np.arange(12)
    top = max(max(rows[c]["months"].max() for c in rows), 1.0)
    for ax, c in zip(axes.ravel(), order):
        r = rows[c]
        pick = c == X["pick"]
        ax.bar(x - 0.21, r["months"], width=0.42, color="#9aa4ad", label="metered use")
        ax.bar(x + 0.21, r["array_months"], width=0.42, color="#2f6b3f" if pick else "#e0a43a", label="array output")
        ax.set_title("%s (%.1f%%)" % (r["town"], r["share1"]), fontsize=7.6, loc="left",
                     fontweight="bold" if pick else "normal")
        ax.set_xticks([0, 3, 6, 9])
        ax.set_xticklabels(["Jan", "Apr", "Jul", "Oct"], fontsize=6.5)
        ax.tick_params(axis="y", labelsize=6.5)
        ax.set_ylim(0, top * 1.08)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    axes[0, 0].set_ylabel("MWh per month", fontsize=7)
    axes[1, 0].set_ylabel("MWh per month", fontsize=7)
    from matplotlib.patches import Patch
    fig.legend(handles=[Patch(color="#9aa4ad", label="2025 metered use"),
                        Patch(color="#e0a43a", label="array's modelled 2025 output"),
                        Patch(color="#2f6b3f", label="array output, recommended store")],
               loc="lower center", ncol=3, fontsize=7, frameon=False, bbox_to_anchor=(0.5, -0.01))
    lo = min(rows[c]["share1"] for c in rows)
    hi = max(rows[c]["share1"] for c in rows)
    fig.suptitle("Each array would have supplied %d to %d per cent of its store's 2025 use (share in brackets)"
                 % (int(lo), int(round(hi))), fontsize=8.8, x=0.02, ha="left")
    fig.tight_layout(rect=(0, 0.06, 1, 0.95))
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


# ---------------------------------------------------------------------------------------------- the memo
def write_pdf(X, path):
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    FD = "/usr/share/fonts/truetype/liberation/"
    for nm, f in (("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
        try:
            pdfmetrics.getFont(nm)
        except KeyError:
            pdfmetrics.registerFont(TTFont(nm, FD + nm.split("-")[0] + "-" + f + ".ttf"))
    pdfmetrics.registerFontFamily("LiberationSans", normal="LiberationSans", bold="LiberationSans-Bold",
                                  italic="LiberationSans-Italic", boldItalic="LiberationSans-Bold")
    INK, GREY, GREEN = colors.HexColor("#1b1d20"), colors.HexColor("#5b6068"), colors.HexColor("#2f5d3a")
    B = ParagraphStyle("b", fontName="LiberationSans", fontSize=9.4, leading=13.0, textColor=INK, spaceAfter=6)
    T = ParagraphStyle("t", fontName="LiberationSans-Bold", fontSize=12.4, leading=15.6, textColor=GREEN, spaceAfter=6)
    H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=9.8, leading=13, textColor=INK, spaceBefore=5,
                        spaceAfter=3)
    SM = ParagraphStyle("sm", fontName="LiberationSans", fontSize=7.7, leading=9.8, textColor=GREY, spaceAfter=3)
    HD = ParagraphStyle("hd", fontName="LiberationSans", fontSize=8.8, leading=12, textColor=INK)
    CE = ParagraphStyle("ce", fontName="LiberationSans", fontSize=8.2, leading=10.2, textColor=INK)
    CR = ParagraphStyle("cr", parent=CE, alignment=2)
    CB = ParagraphStyle("cb", parent=CE, fontName="LiberationSans-Bold")
    CBR = ParagraphStyle("cbr", parent=CB, alignment=2)
    rows = X["rows"]
    p, s2 = rows[X["pick"]], rows[X["second"]]
    br, qb, tn = rows["BRKW"], rows["QLBY"], rows["TNFD"]

    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans", 7.2)
        canvas.setFillColor(GREY)
        canvas.drawString(0.9 * inch, 0.55 * inch, "%s  |  Energy and Sustainability  |  2027 solar pilot site  |  "
                          "13 November 2026" % W.ORG)
        canvas.drawRightString(LETTER[0] - 0.9 * inch, 0.55 * inch, "Page %d" % doc.page)
        canvas.restoreState()

    doc = SimpleDocTemplate(path, pagesize=LETTER, leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.7 * inch,
                            bottomMargin=0.85 * inch, title="2027 on-site solar pilot: site recommendation",
                            author=W.ORG, subject="", creator="", producer="")
    s = [Paragraph("%s  |  ENERGY AND SUSTAINABILITY" % W.ORG.upper(), SM),
         Paragraph("Site the 2027 solar pilot at %s: its array would have avoided %.2f t of grid carbon dioxide for every "
                   "MWh it generated in 2025" % (p["name"], p["rate"]), T),
         Paragraph("To: Capital Committee<br/>From: %s, %s<br/>Prepared with: %s, %s<br/>Date: 13 November 2026<br/>"
                   "Re: Pilot site under the 2027 On-Site Solar Pilot siting charter (minute CC-26-41)" % (
                       W.PEOPLE["director"], W.TITLES["director"], W.PEOPLE["analyst"], W.TITLES["analyst"]), HD),
         Spacer(1, 8),
         Paragraph(
             "I recommend that the Committee name %s (store %d) as the 2027 pilot store in the capital plan. On the "
             "charter's measure, the carbon dioxide the generators of the store's balancing area would not have emitted "
             "in 2025 had the array been supplying the store, its array avoids %.2f t per MWh it generates. %s is the "
             "first store left out at %.2f t per MWh, %.2f below. The other six arrays would each have avoided between "
             "%.2f and %.2f t per MWh." % (
                 p["name"], p["store"], p["rate"], s2["name"], s2["rate"], X["gap"],
                 min(rows[c]["rate"] for c in X["order"][2:]), max(rows[c]["rate"] for c in X["order"][2:])), B),
         Paragraph(
             "An array's output is taken off the generators at the margin in the hours it generates, so what it avoids "
             "is their emission rate in its own hours. In Gorsefield's area gas carries the nights and the coal fleet "
             "follows the load from 5 am to 6 pm, the hours the array generates. Brackwell has the highest average "
             "output emission rate, %.2f t per MWh, but by day its coal runs at full output and gas follows the load, so "
             "its array avoids %.2f. Quillbury's high non-baseload rate (%.2f) comes from old coal units run on winter "
             "evenings, after sunset (%.2f in the array's hours). Tennaford's coal follows the load through the night, "
             "which puts a marginal rate fitted to every hour of 2025 above every other area's, but gas follows its "
             "business day from 7 am to 6 pm (%.2f in the array's hours)." % (
                 br["avg"], br["rate"], qb["nb"], qb["rate"], tn["rate"]), B)]
    head = ["Store", "Balancing area", "Array output 2025 (MWh)", "Grid CO2 avoided (t/MWh)", "Metered use 2025 (MWh)",
            "Share of use supplied", "Paid per MWh ($)"]
    data = [[Paragraph(t, CB if k < 2 else CBR) for k, t in enumerate(head)]]
    for c in X["order"]:
        r = rows[c]
        sty = CB if c == X["pick"] else CE
        styr = CBR if c == X["pick"] else CR
        data.append([Paragraph("%s (%d)" % (r["name"], r["store"]), sty), Paragraph(W.AREAS[c]["ba"], sty),
                     Paragraph("{:,}".format(int(round(r["mwh"]))), styr), Paragraph("%.2f" % r["rate"], styr),
                     Paragraph("{:,}".format(r["use0"]), styr), Paragraph("%.1f%%" % r["share1"], styr),
                     Paragraph("%d" % r["price0"], styr)])
    t = Table(data, colWidths=[1.45 * inch, 1.65 * inch, 0.78 * inch, 0.78 * inch, 0.78 * inch, 0.7 * inch, 0.66 * inch],
              hAlign="LEFT", repeatRows=1)
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, INK), ("LINEBELOW", (0, -1), (-1, -1), 0.4, GREY),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 1.6),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6),
                           ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#eef4ef"))]))
    s.append(t)
    s.append(Paragraph(
        "Sources: %s hourly operating data and 2025 generation and emission rates (release 1.0); %s array model runs "
        "on 2025 weather; Corvane accounts payable. Stores in order of grid CO2 avoided." % (W.AGENCY, W.VENDOR_MODEL), SM))
    s.append(Paragraph("How the avoided carbon dioxide was measured", H2))
    s.append(Paragraph(
        "For each area I put the agency's hourly operating data and each store's modelled array output on one clock (the "
        "operating data name each hour by its end in UTC, the model by its start in local standard time) and estimated "
        "the area's marginal emission rate in each season (December to February, March to May, June to August, "
        "September to November) and hour of the local day: the hour-to-hour change in the area's fossil carbon dioxide "
        "(its hourly coal, gas and oil generation at the agency's 2025 output emission rates for each fuel) against the "
        "hour-to-hour change in its net generation, which with interchange scheduled a day ahead is the change its own "
        "generators make to follow the load. Each store's figure is that rate weighted by its array's output, hour by "
        "hour. Month-by-hour bins, the hour of day alone, or changes in demand or fossil generation in place of net "
        "generation give the same figures to two decimals.", B))
    s.append(Paragraph("Use and price from the invoices", H2))
    s.append(Paragraph(
        "Metered use is each delivery utility's distribution energy quantity, once per meter and billing cycle (Tennaford "
        "bills it in declining blocks, which are summed), from the latest invoice for the cycle, with each bill's days "
        "in 2025 counted pro rata; Quillbury and Kestrel Point add their garden-centre meters. %s bills the same "
        "consumption by calendar month at the wholesale delivery point, %.1f to %.1f per cent above the meters, so its "
        "quantities are not added. The price is every electricity charge on both vendors' invoices for 2025 over that "
        "use; Halvane Gas & Electric's gas lines are left out. Each array is sized below its store's daytime load "
        "(charter 3.3), so the share supplied is its 2025 output over the store's use." % (W.SUPPLIER, X["loss"][0],
                                                                                            X["loss"][1]), B))
    s.append(Paragraph(
        "Kestrel Point's area filed its data under its former code, KPLP, until 30 June 2025. The operator filed a few "
        "hours of demand from each hour's net generation and interchange after telemetry gaps; leaving them out moves no "
        "figure.", SM))
    s.append(Spacer(1, 4))
    s.append(Image(io.BytesIO(chart_png(X)), width=6.7 * inch, height=3.63 * inch))
    s.append(Paragraph("Figure 1. Each store's 2025 metered use by calendar month (from its billing cycles, by days) "
                       "against its array's modelled 2025 output.", SM))
    s.append(Spacer(1, 6))
    s.append(Paragraph("%s<br/>%s" % (W.PEOPLE["director"], W.TITLES["director"]), B))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


# ---------------------------------------------------------------------------------------------- the hourly file
HOURLY_COLS = ["store_number", "store_name", "balancing_area", "hour_beginning_utc", "hour_beginning_local_standard",
               "array_output_kwh", "marginal_co2_t_per_mwh", "avoided_co2_kg"]


def hourly_rows(X):
    D = X["D"]
    t0 = dt.datetime(2025, 1, 1)
    for c in W.ORDER:
        st = X["rows"][c]["store"]
        utc = D["codes"][c]["utc"]
        m = X["g"][st]["mer"]
        arr = D["arrays"][st]
        lh, mon, _ = M.clock(utc)
        season = np.array([M.SEASON[x] for x in mon])
        bins = {}
        for h in range(H):
            bins.setdefault((season[h], lh[h]), m[h])
        for k in range(H):
            lst = t0 + dt.timedelta(hours=k)
            rate = bins[(M.SEASON[lst.month], lst.hour)]
            kwh = arr[k]
            yield [st, X["rows"][c]["name"], c, (lst - dt.timedelta(hours=utc)).strftime("%Y-%m-%dT%H:%MZ"),
                   lst.strftime("%Y-%m-%d %H:%M"), "%.1f" % kwh, "%.4f" % rate, "%.1f" % (kwh * rate)]


def write_hourly(X, path):
    n = 0
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(HOURLY_COLS)
        for r in hourly_rows(X):
            w.writerow(r)
            n += 1
    return n


# ---------------------------------------------------------------------------------------------- figures.json
def figures(X, n_hourly):
    rows = X["rows"]
    out = {"call": rows[X["pick"]]["town"], "pick_store": rows[X["pick"]]["store"], "first_left_out": rows[X["second"]]["town"],
           "gap": float("%.2f" % X["gap"]), "gap_unrounded": round(X["gap"], 4), "stores": {}, "rungs": {},
           "hourly_rows": n_hourly}
    for c in W.ORDER:
        r = rows[c]
        out["stores"][r["town"]] = dict(store=r["store"], area=c, rate=r["rate2"], rate_unrounded=round(r["rate"], 4),
                                        array_mwh=int(round(r["mwh"])), use=r["use0"], use_unrounded=round(r["use"], 2),
                                        share=r["share1"], share_unrounded=round(r["share"], 3), price=r["price0"],
                                        price_unrounded=round(r["price"], 2), tonnes=int(round(r["tonnes"])),
                                        avg=r2(r["avg"]), nb=r2(r["nb"]), fossil=r2(r["fossil"]), pooled=r2(r["pooled"]),
                                        all_hours=r2(r["all_hours"]), hourly_average=r2(r["hourly_average"]))
    for key in ("avg", "nb", "all_hours", "pooled", "hourly_average", "fossil"):
        o = sorted(rows, key=lambda c: -rows[c][key])
        out["rungs"][key] = dict(winner=rows[o[0]]["town"], value=r2(rows[o[0]][key]), second=rows[o[1]]["town"],
                                 second_value=r2(rows[o[1]][key]), gorsefield_place=o.index("GRSF") + 1)
    out["share_range"] = [min(rows[c]["share1"] for c in rows), max(rows[c]["share1"] for c in rows)]
    out["loss_factor_range_pct"] = [float("%.1f" % X["loss"][0]), float("%.1f" % X["loss"][1])]
    return out


def main(target, out_dir, fig_path):
    X = compute(target)
    os.makedirs(out_dir, exist_ok=True)
    write_pdf(X, os.path.join(out_dir, W.GOLDEN["memo"]))
    n = write_hourly(X, os.path.join(out_dir, W.GOLDEN["hourly"]))
    F = figures(X, n)
    with open(fig_path, "w") as f:
        json.dump(F, f, indent=1, sort_keys=True)
    return X, F


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
