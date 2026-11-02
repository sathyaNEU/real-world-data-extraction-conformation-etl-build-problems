"""The golden deliverables: the dose review workbook and the two-page memo with its chart."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import openpyxl  # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill  # noqa: E402

import analysis  # noqa: E402
from io_util import repack_xlsx, write_pdf  # noqa: E402

XLSX = "cqtc_dose_review.xlsx"
PDF = "cqtc_dose_memo.pdf"
PH2B = [25, 50, 100]


def sig3(x):
    e = int(np.floor(np.log10(abs(x)))) - 2
    v = round(x / 10 ** e) * 10 ** e
    return int(v) if v >= 100 else v


def fmt_int(n):
    return "{:,}".format(int(n))


def figures(F):
    """Every figure the deliverables and the write-up state, rounded once."""
    G = F["G"]
    out = {"call_mg": G["call"]}
    for d in PH2B:
        out["c_high_%d" % d] = sig3(F["ch"][d])
        out["below10_%d" % d] = "yes" if G["ubs"][d] < 10 else "no"
        out["ub_%d" % d] = round(G["ubs"][d], 1)
        out["pt_%d" % d] = round(G["pred"][d][0], 1)
    for d, v in F["ask_a"].items():
        out["auc_sad_%d" % d] = analysis.sig2(v)[0]
    for (study, d), v in F["ask_b"].items():
        out["night_hr_%s_%d" % (study, d)] = round(v + 0.0, 1)
    out["exp_hour_mean"] = round(float(np.mean(list(F["ex"]["hour"].values()))), 2)
    out["exp_pooled_mean"] = round(float(np.mean(list(F["ex"]["pooled"].values()))), 2)
    out["slope_per100"] = round(float(G["model"]["b"][2]) * 100, 2)
    out["qtcf_call"] = F["rungs"]["QTcF"]["call"]
    out["pooled_call"] = F["rungs"]["pooled_own"]["call"]
    return out


def chart(F, path):
    D = F["D"]
    G = F["G"]
    val = analysis.qtc_table(D, "own", F["ex"]["hour"])
    rows, base = analysis.model_rows(D, val)
    pl = {}
    for r in rows:
        if not r["trt"]:
            pl.setdefault(r["nominal"], []).append(r["dq"])
    act = [(r["conc"], r["dq"] - np.mean(pl[r["nominal"]])) for r in rows if r["trt"]]
    act.sort()
    x = np.array([a[0] for a in act])
    y = np.array([a[1] for a in act])
    edges = np.quantile(x, np.linspace(0, 1, 11))
    bx, by, be = [], [], []
    for i in range(10):
        m = (x >= edges[i]) & (x <= edges[i + 1] if i == 9 else x < edges[i + 1])
        bx.append(np.median(x[m]))
        by.append(np.mean(y[m]))
        be.append(1.645 * np.std(y[m], ddof=1) / np.sqrt(m.sum()))
    grid = np.linspace(0, max(1350, x.max()), 120)
    pred = [analysis.cqtc.predict(G["model"], c) for c in grid]
    fig, ax = plt.subplots(figsize=(6.6, 3.7), dpi=150)
    ax.scatter(x, y, s=5, color="#9aa7b1", alpha=0.45, lw=0, label="Observed, placebo-adjusted")
    ax.errorbar(bx, by, yerr=be, fmt="o", color="#1f4e79", ms=4, capsize=2, lw=1, label="Concentration deciles (mean, 90% CI)")
    ax.plot(grid, [p[0] for p in pred], color="#c0392b", lw=1.6, label="Model prediction")
    ax.fill_between(grid, [p[0] - (p[1] - p[0]) for p in pred], [p[1] for p in pred], color="#c0392b", alpha=0.13,
                    lw=0, label="90% confidence band")
    ax.axhline(10, color="#333333", lw=0.9, ls="--")
    ax.text(grid[-1], 10.4, "10 ms", ha="right", va="bottom", fontsize=7.5)
    for d, c in zip(PH2B, ["#2e7d32", "#ef6c00", "#6a1b9a"]):
        ax.axvline(F["ch"][d], color=c, lw=1.1)
        ax.text(F["ch"][d], -9.2, " %d mg" % d, color=c, fontsize=7.5, rotation=90, va="bottom")
    ax.set_xlabel("VLT-317 plasma concentration (ng/mL)", fontsize=8.5)
    ax.set_ylabel("Placebo-adjusted change in QTcI (ms)", fontsize=8.5)
    ax.set_ylim(-10, 22)
    ax.tick_params(labelsize=7.5)
    ax.legend(fontsize=6.6, loc="upper left", frameon=False)
    ax.set_title("Concentration-QTcI, studies 101 and 102, with each dose's high clinical exposure", fontsize=8.5)
    fig.tight_layout()
    fig.savefig(path, dpi=150, metadata={"Software": None})
    plt.close(fig)


def workbook(F, fig, path):
    G = F["G"]
    D = F["D"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Dose call"
    bold = Font(bold=True)
    ws.append(["VLT-317 phase 2b doses against the 10 ms bound (C-QTc plan v2.0, QTcI)"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append([])
    ws.append(["Dose (mg QD)", "High clinical exposure (ng/mL)", "Predicted placebo-corrected dQTcI (ms)",
               "Upper 90% bound (ms)", "Below 10 ms"])
    for c in ws[3]:
        c.font = bold
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for d in PH2B:
        ws.append([d, fig["c_high_%d" % d], fig["pt_%d" % d], fig["ub_%d" % d], fig["below10_%d" % d].capitalize()])
    ws.append([])
    ws.append(["Highest dose clearing the bound", "%d mg once daily" % fig["call_mg"]])
    ws["A9"].font = bold
    ws.append(["High clinical exposure", "Day 10 geometric mean Cmax (study 102) x 2.61 (itraconazole, study 103)"])
    ws.append(["Heart-rate correction", "Each subject's own exponent from his drug-free Holter, fitted within clock "
               "hour (mean %.2f; a single 24-hour line gives %.2f)" % (fig["exp_hour_mean"], fig["exp_pooled_mean"])])
    ws.append(["Concentration slope", "%.2f ms per 100 ng/mL" % fig["slope_per100"]])
    ws.append(["Upper bounds", "Per-hour, half-hour, two- and three-hour clock bins and cosinor fits all keep 25 and "
               "50 mg below 10 ms and 100 mg above it; the upper bound at 50 mg runs about 7 to 8 ms across them"])
    for col, w in zip("ABCDE", (30, 22, 24, 16, 12)):
        ws.column_dimensions[col].width = w
    for r in ws.iter_rows(min_row=10, max_row=13):
        r[1].alignment = Alignment(wrap_text=True, vertical="top")

    ws = wb.create_sheet("QTcI exponents")
    ws.append(["Subject", "Study", "Drug-free segments", "Exponent b (within clock hour)", "Single 24-hour line"])
    for c in ws[1]:
        c.font = bold
    for sid in sorted(F["ex"]["hour"]):
        ws.append([sid, "VLT-317-" + D["subj"][sid]["study"], int(len(F["df"][sid])), round(F["ex"]["hour"][sid], 4),
                   round(F["ex"]["pooled"][sid], 4)])
    for col, w in zip("ABCDE", (10, 13, 18, 26, 18)):
        ws.column_dimensions[col].width = w

    ws = wb.create_sheet("Model")
    names = ["Intercept", "Treatment (VLT-317)", "Concentration (per ng/mL)"] + \
        ["Time %g h" % t for t in analysis.ECG_TIMES[1:]] + ["Baseline QTcI (centred)"]
    ws.append(["Fixed effect", "Estimate", "Standard error"])
    for c in ws[1]:
        c.font = bold
    for n, b, se in zip(names, G["model"]["b"], np.sqrt(np.diag(G["model"]["cov"]))):
        ws.append([n, round(float(b), 5), round(float(se), 5)])
    ws.append([])
    ws.append(["Observations", G["n"]])
    ws.append(["Subjects", G["model"]["n_subj"]])
    ws.append(["Residual SD (ms)", round(float(np.sqrt(G["model"]["s2"])), 3)])
    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 16

    ws = wb.create_sheet("SAD AUC")
    ws.append(["Dose (mg)", "Geometric mean AUC0-inf (ng.h/mL)", "Subjects"])
    for c in ws[1]:
        c.font = bold
    gm, per = analysis.ask_a(D)
    for d in (25, 50, 100, 200, 400):
        ws.append([d, fig["auc_sad_%d" % d], len([k for k in per if D["subj"][k]["dose"] == d])])
    ws.append([])
    ws.append(["Subject", "Dose (mg)", "AUC0-inf (ng.h/mL)"])
    for c in ws[ws.max_row]:
        c.font = bold
    for sid in sorted(per):
        ws.append([sid, D["subj"][sid]["dose"], round(per[sid])])
    ws.column_dimensions["B"].width = 32

    ws = wb.create_sheet("Night heart rate")
    ws.append(["Study", "Dose (mg)", "Placebo-corrected change, 00:00-06:00 (bpm)"])
    for c in ws[1]:
        c.font = bold
    for (study, d), v in F["ask_b"].items():
        ws.append(["VLT-317-" + study, d, fig["night_hr_%s_%d" % (study, d)]])
    ws.column_dimensions["C"].width = 40
    ws.column_dimensions["A"].width = 14
    for w in wb.worksheets:
        w.sheet_view.showGridLines = True
    ws0 = wb["Dose call"]
    for row in ws0.iter_rows(min_row=4, max_row=6):
        if row[4].value == "No":
            row[4].fill = PatternFill("solid", fgColor="F4CCCC")
    wb.save(path)
    repack_xlsx(path, "Hilde Lemmens", "Hilde Lemmens", "2026-10-26T13:05:00Z", "2026-10-28T08:47:00Z",
                "VLT-317 C-QTc dose review", "Valtenna Therapeutics NV")


def memo(F, fig, png, path):
    t = [["Dose", "High clinical exposure", "Upper 90% bound", "Below 10 ms"]]
    for d in PH2B:
        t.append(["%d mg QD" % d, "%s ng/mL" % fmt_int(fig["c_high_%d" % d]), "%.1f ms" % fig["ub_%d" % d],
                  fig["below10_%d" % d].capitalize()])
    auc = [["Single dose", "25 mg", "50 mg", "100 mg", "200 mg", "400 mg"],
           ["AUC0-inf (ng.h/mL)"] + [fmt_int(fig["auc_sad_%d" % d]) for d in (25, 50, 100, 200, 400)]]
    hr = [["Study", "25 mg", "50 mg", "100 mg", "200 mg", "400 mg"],
          ["101 (single)"] + ["%+.1f" % fig["night_hr_101_%d" % d] for d in (25, 50, 100, 200, 400)],
          ["102 (first dose)"] + ["%+.1f" % fig["night_hr_102_%d" % d] for d in (25, 50, 100)] + ["", ""]]
    b = [("t", "VLT-317: phase 2b doses and the QT bound"),
         ("s", "To: Micha&euml;l Tanghe. From: Hilde Lemmens. 28 October 2026. Basis: C-QTc analysis plan v2.0, "
               "studies 101 and 102, DDI study 103."),
         ("p", "<b>50 mg once daily is the highest phase 2b dose that clears the 10 ms bound.</b> At its high "
               "clinical exposure (%s ng/mL) the upper 90%% bound of the predicted placebo-corrected QTcI change is "
               "about %.0f ms. 100 mg does not clear it: at %s ng/mL the bound is about %.0f ms, so 100 mg would need "
               "a dedicated QT study or a lower ceiling." % (fmt_int(fig["c_high_50"]), fig["ub_50"],
                                                              fmt_int(fig["c_high_100"]), fig["ub_100"])),
         ("table", t),
         ("image", (png, 166, 93)),
         ("h", "What sets the answer"),
         ("p", "VLT-317 raises heart rate with concentration, so the call rests on how QT is corrected for it. The "
               "plan's QTcI uses each subject's own exponent from his drug-free Holter. Fitted as one line through the "
               "whole 24 hours, the exponent comes out at %.2f on average, because QT also runs longer at night for "
               "reasons other than the slower heart rate; fitted within each clock hour it is %.2f. With the 24-hour "
               "line the drug's heart-rate rise is over-corrected and only 25 mg passes; with Fridericia (one third) it "
               "is under-corrected and all three doses appear to pass. Corrected for heart rate alone, 25 and 50 mg "
               "pass and 100 mg fails." % (fig["exp_pooled_mean"], fig["exp_hour_mean"])),
         ("h", "Exposure and heart rate"),
         ("table", auc),
         ("p", "Change in mean heart rate from 00:00 to 06:00 on the night after the first dose against the same hours "
               "the night before, less the same change in each study's placebo subjects (bpm):"),
         ("table", hr),
         ]
    import reportlab.lib.units as u
    write_pdf(path, "VLT-317 phase 2b doses and the QT bound", "Hilde Lemmens", "Microsoft Word", b,
              "Valtenna Therapeutics NV | Clinical Pharmacology | Internal", "D:20261028094701+01'00'",
              "D:20261028094701+01'00'",
              widths={4: [30 * u.mm, 50 * u.mm, 45 * u.mm, 35 * u.mm], 6: [38 * u.mm] + [26.4 * u.mm] * 5})


def write(F, out):
    os.makedirs(out, exist_ok=True)
    fig = figures(F)
    png = os.path.join(out, "_chart.png")
    chart(F, png)
    workbook(F, fig, os.path.join(out, XLSX))
    memo(F, fig, png, os.path.join(out, PDF))
    os.remove(png)
    return fig
