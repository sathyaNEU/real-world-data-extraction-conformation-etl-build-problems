"""The golden deliverables, computed from target/ alone: the superintendent's memo to the Select Board (PDF, with the
frequency chart) and the river's conformed annual low-flow record (CSV); and generator/figures.json, every figure the
write-up states."""
import csv
import datetime as dt
import io
import json
import math
import os

import numpy as np

import bundle as B
import methods as M
import world as W


def compute(target):
    rec = B.annual_record(target)
    lg = np.log10([v for y, (k, v) in sorted(rec.items()) if k == "gauged"])
    lm = np.log10([v for y, (k, v) in sorted(rec.items()) if k == "measured"])
    silent = sum(1 for k, _ in rec.values() if k == "none")
    missing = sum(1 for k, _ in rec.values() if k == "missing")
    r = M.routes(lg, lm, silent)
    g = M.decision(*r["R2"])
    rungs = {k: M.decision(*v) for k, v in r.items()}
    periods = B.stage2_periods(target)
    supply = B.own_supply(target)
    ask = []
    for a, b in periods:
        vals = [supply[d] for d in B.daterange(a, b)]
        ask.append(dict(year=a.year, start=a.isoformat(), end=b.isoformat(), days=len(vals),
                        average=float(np.mean(vals)), highest=float(np.max(vals))))
    n_blocks = int(round(g["block"] / W.BLOCK_MGD))
    return dict(record=rec, gauged=len(lg), measured=len(lm), silent=silent, missing=missing, golden=g, rungs=rungs,
                ask=ask, blocks=n_blocks, charge=n_blocks * W.BLOCK_PRICE)


def r2(v):
    return "%.2f" % (math.floor(v * 100 + 0.5 + 1e-9) / 100.0)


def figures(fx):
    g = fx["golden"]
    out = {
        "call": {"block_mgd": r2(g["block"]).rstrip("0").rstrip(".") if False else "%.1f" % g["block"],
                 "blocks": fx["blocks"], "reservation_charge_2027": "{:,}".format(fx["charge"])},
        "components": {"design_flow_cfs": r2(g["flows"][50]), "withdrawal_mgd": r2(g["withdrawals"][50]),
                       "shortfall_mgd": r2(g["shortfalls"][50]), "stage2_demand_mgd": "%.2f" % W.STAGE2_DEMAND[2027],
                       "gauged_years": fx["gauged"], "measured_years": fx["measured"], "silent_years": fx["silent"],
                       "missing_reports": fx["missing"], "suspension_flow_cfs": r2(W.SUSPEND_CFS)},
        "scenarios": {str(t): {"flow_cfs": r2(g["flows"][t]), "withdrawal_mgd": r2(g["withdrawals"][t]),
                               "shortfall_mgd": r2(g["shortfalls"][t])} for t in W.SCENARIOS},
        "flip": {"years": "%d" % int(math.floor(g["flip_years"] + 0.5)), "flow_cfs": r2(g["flip_flow"])},
        "rivals": {k: {"design_flow_cfs": r2(d["flows"][50]), "shortfall_mgd": r2(d["shortfalls"][50]),
                       "block_mgd": "%.1f" % d["block"]} for k, d in fx["rungs"].items()},
        "ask": [{"year": a["year"], "start": a["start"], "end": a["end"], "days": a["days"],
                 "average_mgd": r2(a["average"]), "highest_mgd": r2(a["highest"])} for a in fx["ask"]],
        "conformed_rows": len(fx["record"]),
        "stated": {"recurrence_intervals": list(W.SCENARIOS), "window_days": 7, "agreement_year": 1893,
                   "regional_skew": "%.2f" % W.REGIONAL_SKEW, "record_years": [W.FIRST_REPORT, W.FIT_YEARS[1]],
                   "passby_cfs": "%.2f" % W.PASSBY_CFS, "block_size_mgd": "%.1f" % W.BLOCK_MGD},
    }
    return out


# ---------------------------------------------------------------- the chart
def chart_png(fx):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from scipy import stats
    g = fx["golden"]
    rec = fx["record"]
    gauged = sorted(v for k, v in rec.values() if k == "gauged")
    meas = sorted(v for k, v in rec.values() if k == "measured")
    n_rep = fx["measured"] + fx["silent"]
    fig, ax = plt.subplots(figsize=(6.6, 3.9), dpi=150)
    ri = np.logspace(math.log10(1.05), math.log10(200), 200)
    curve = [M.flow(1.0 / t, g["mu"], g["sd"]) for t in ri]
    ax.plot(ri, curve, color="#1d5b63", lw=1.8, label="Fitted log-Pearson Type III (skew -0.30)")
    pg = [(len(gauged) + 1) / (i + 1) for i in range(len(gauged))]
    ax.scatter(pg, gauged, s=13, color="#4a6fa5", zorder=3, label="Gauge, 1951 to 2024 (%d years)" % len(gauged))
    pm = [(n_rep + 1) / (i + 1) for i in range(len(meas))]
    ax.scatter(pm, meas, s=22, marker="D", facecolor="white", edgecolor="#8a4b2a", lw=1.1, zorder=4,
               label="Water Works reports, seasons the pumps stopped (%d)" % len(meas))
    ax.axhline(W.SUSPEND_CFS, color="#8a4b2a", lw=0.8, ls=":", zorder=1)
    ax.text(160, W.SUSPEND_CFS * 1.04, "2 MGD (3.09 cfs)", fontsize=7, color="#8a4b2a", ha="right")
    q50 = g["flows"][50]
    ax.plot([50, 50], [0.8, q50], color="#b0392f", lw=1.0, ls="--")
    ax.plot([1.05, 50], [q50, q50], color="#b0392f", lw=1.0, ls="--")
    ax.annotate("50-year: %s cfs" % r2(q50), xy=(50, q50), xytext=(58, q50 * 0.82), fontsize=8, color="#b0392f")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1.05, 200)
    ax.set_ylim(0.8, 40)
    ax.set_xticks([1.25, 2, 5, 10, 25, 50, 100, 200])
    ax.set_xticklabels(["1.25", "2", "5", "10", "25", "50", "100", "200"])
    ax.set_yticks([1, 2, 3, 5, 10, 20, 40])
    ax.set_yticklabels(["1", "2", "3", "5", "10", "20", "40"])
    ax.set_xlabel("Recurrence interval, years", fontsize=8.5)
    ax.set_ylabel("7-day low flow, cfs", fontsize=8.5)
    ax.tick_params(labelsize=7.5)
    ax.grid(True, which="major", color="#dddddd", lw=0.5)
    ax.legend(fontsize=7, loc="upper left", frameon=False)
    ax.set_title("Varrow River at the intake: the 50-year 7-day low flow is %s cfs" % r2(q50), fontsize=9.5)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


# ---------------------------------------------------------------- the memo
def write_memo(path, fx, png):
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    import docs as DC   # noqa: F401  (registers the fonts)
    g = fx["golden"]
    ink = colors.HexColor("#1b1d1f")
    body = ParagraphStyle("b", fontName="LiberationSerif", fontSize=10.5, leading=14, textColor=ink, spaceAfter=6)
    head = ParagraphStyle("h", fontName="LiberationSans-Bold", fontSize=13, leading=16, textColor=colors.HexColor("#1d5b63"))
    h2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10, leading=13, textColor=ink, spaceBefore=6, spaceAfter=3)
    cell = ParagraphStyle("c", fontName="LiberationSans", fontSize=8.6, leading=10.6, textColor=ink)
    cellb = ParagraphStyle("cb", parent=cell, fontName="LiberationSans-Bold")
    note = ParagraphStyle("n", fontName="LiberationSans", fontSize=7.8, leading=10, textColor=colors.HexColor("#5b6067"))

    def table(rows, widths, right_from=1):
        data = [[Paragraph(str(c), cellb if i == 0 else cell) for c in r] for i, r in enumerate(rows)]
        t = Table(data, colWidths=widths, hAlign="LEFT")
        t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, ink), ("LINEBELOW", (0, -1), (-1, -1), 0.4, ink),
                               ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 3),
                               ("RIGHTPADDING", (0, 0), (-1, -1), 3)]))
        return t

    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans", 7.5)
        canvas.setFillColor(colors.HexColor("#5b6067"))
        canvas.drawString(0.85 * inch, 0.55 * inch, "Quillfield Water Department  |  Castlewick interconnect, 2027")
        canvas.drawRightString(letter[0] - 0.85 * inch, 0.55 * inch, "%d" % doc.page)
        canvas.restoreState()
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.85 * inch, rightMargin=0.85 * inch,
                            topMargin=0.7 * inch, bottomMargin=0.8 * inch,
                            title="Firm capacity on the Castlewick interconnect for 2027",
                            author=W.PEOPLE["superintendent"], subject="", creator="", producer="")
    blocks = fx["blocks"]
    s = [Paragraph("Town of Quillfield Water Department", head),
         Spacer(1, 4),
         table([["To", "Select Board"], ["From", "%s, %s" % (W.PEOPLE["superintendent"], W.TITLES["superintendent"])],
                ["Date", "October 16, 2026"], ["Re", "Firm capacity on the Castlewick interconnect for 2027"]],
               [0.6 * inch, 6.1 * inch]),
         Spacer(1, 8),
         Paragraph("<b>Reserve %.1f million gallons a day (%s blocks) of firm capacity on the Castlewick interconnect "
                   "for 2027.</b> At the river's 50-year 7-day low flow of %s cubic feet per second our permit lets us "
                   "take %s MGD, %s MGD short of the 2027 Stage 2 demand of %.2f MGD; %s blocks cover it, at a "
                   "reservation charge of $%s." % (g["block"], {3: "three", 4: "four", 2: "two", 1: "one"}.get(blocks, blocks),
                                                    r2(g["flows"][50]), r2(g["withdrawals"][50]), r2(g["shortfalls"][50]),
                                                    W.STAGE2_DEMAND[2027], {3: "three", 4: "four", 2: "two", 1: "one"}.get(blocks, blocks),
                                                    "{:,}".format(fx["charge"])), body),
         Paragraph("The design flow comes from Guidance WR-14's log-Pearson Type III, fitted by maximum likelihood to "
                   "the whole record of the river at the dam: the Survey gauge's %d approved climatic years from 1951 "
                   "to 2024 and the Water Works reports from 1894 to 1950. The reports measured the river only in the "
                   "%d seasons the mill agreement stopped the pumps; in the other %d reported years the pumps never "
                   "stopped, so each of those years' 7-day low flow stayed above the agreement's two million gallons a "
                   "day (3.09 cfs), and the fit takes them as that. The reports for 1909, 1918 and 1944 are missing and "
                   "are left out." % (fx["gauged"], fx["measured"], fx["silent"]), body),
         Paragraph("Drought scenarios", h2)]
    rows = [["Recurrence interval", "7-day low flow, cfs", "Withdrawal allowed, MGD", "Stage 2 shortfall, MGD"]]
    for t in W.SCENARIOS:
        sh = g["shortfalls"][t]
        rows.append(["%d years" % t, r2(g["flows"][t]), r2(g["withdrawals"][t]), r2(sh) if sh > 0 else "none"])
    s += [table(rows, [1.4 * inch, 1.6 * inch, 1.8 * inch, 1.8 * inch]),
          Spacer(1, 5),
          Paragraph("Three blocks stop covering the Stage 2 shortfall in a drought rarer than the %d-year 7-day low "
                    "flow (%s cfs)." % (int(math.floor(g["flip_years"] + 0.5)), r2(g["flip_flow"])), body),
          Image(io.BytesIO(png), width=6.6 * inch, height=3.9 * inch),
          Paragraph("Points plotted at Weibull positions, (n + 1)/rank, within the gauge's %d years and within the %d "
                    "reported years. Climatic year 2025 is left out of the fit: its winter months are still provisional."
                    % (fx["gauged"], fx["measured"] + fx["silent"]), note),
          ]
    rows = [["Stage 2 in effect", "Days", "Average day, MGD", "Highest day, MGD"]]
    for a in fx["ask"]:
        rows.append(["%s to %s" % (a["start"], a["end"]), str(a["days"]), r2(a["average"]), r2(a["highest"])])
    s += [KeepTogether([
          Paragraph("What our own system drew in past Stage 2 periods", h2),
          table(rows, [2.5 * inch, 0.8 * inch, 1.6 * inch, 1.6 * inch]),
          Spacer(1, 4),
          Paragraph("Water supplied to the Quillfield distribution system: the plant's finished water less the Elm "
                    "Hollow master meter, plus the Hollow Road wells (from the operator's round sheets since the "
                    "wellfield telemetry failed on June 14, 2023). Flows in cubic feet per second, water in million "
                    "gallons a day, both to two decimals; the shortfall and the block computed before rounding.", note)])]
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


CONFORMED_COLS = ["climatic_year", "source", "record", "seven_day_low_flow_cfs"]


def write_conformed(path, fx):
    rows = []
    for y in range(W.FIRST_REPORT, W.FIT_YEARS[1] + 1):
        k, v = fx["record"][y]
        if k == "gauged":
            rows.append([y, "State Hydrologic Survey gauge 01-2297.40", "gauged", r2(v)])
        elif k == "measured":
            rows.append([y, "Water Works report", "pumps stopped; lowest seven-day flow measured", r2(v)])
        elif k == "none":
            rows.append([y, "Water Works report", "no stoppage; 7-day low flow above 3.09", ""])
        else:
            rows.append([y, "Water Works report", "report not found", ""])
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\r\n")
        wr.writerow(CONFORMED_COLS)
        wr.writerows(rows)
    return len(rows)


def main(target, gdir, fig_path):
    os.makedirs(gdir, exist_ok=True)
    fx = compute(target)
    png = chart_png(fx)
    write_memo(os.path.join(gdir, W.GOLDEN["memo"]), fx, png)
    write_conformed(os.path.join(gdir, W.GOLDEN["table"]), fx)
    figs = figures(fx)
    with open(fig_path, "w", encoding="utf-8") as fh:
        json.dump(figs, fh, indent=1)
        fh.write("\n")
    return fx, figs
