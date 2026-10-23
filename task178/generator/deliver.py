"""task178 goldens: the design-flow workbook and the frequency-curve chart, generator/figures.json and submission.md,
every figure read from calc.py run on the shipped pack."""
from __future__ import annotations

import datetime as dt
import json
import os

import numpy as np
from scipy import stats

import common as C
import calc

GOLDEN_FORM = "breakpoint_fit"
MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December")


def long_date(iso):
    d = dt.date.fromisoformat(iso)
    return "%d %s %d" % (d.day, MONTHS[d.month - 1], d.year)


def r(x, u):
    return int(round(x / u) * u)


def figures(target):
    g = calc.main_call(target, GOLDEN_FORM)
    d = calc.main_call(target, "single_log")
    lin = calc.main_call(target, "single_lin")
    st = calc.read_stage(target)
    a = calc.ask_a(target, st)
    b = calc.ask_b(target, st)
    caps = dict(C.ALTERNATIVES)
    name, cap = g["pick"]
    f = {
        "call": {"alternative": name, "design_discharge_cfs": r(g["q100"], 1000)},
        "crit": {"station_skew": round(float(g["fit"]["g"]), 1), "alternative_capacity_cfs": cap},
        "ask_a": {str(y): {"stage_ft": v[0], "date": v[1]} for y, v in a.items()},
        "ask_b": {str(y): {"pipe_level_ft": v[0], "fall_ft": v[1]} for y, v in b.items()},
        "default": {"alternative": d["pick"][0], "design_discharge_cfs": r(d["q100"], 1000),
                    "station_skew": round(float(d["fit"]["g"]), 1)},
        "rival_arithmetic_rating": {"alternative": lin["pick"][0], "design_discharge_cfs": r(lin["q100"], 1000)},
        "breakpoint_ft": round(float(g["rating"].hb), 2),
        "annual_peaks": len(g["peaks"]),
        "measurements": int(len(g["h"])),
        "measurements_above_breakpoint": int((g["h"] >= g["rating"].hb).sum()),
        "next_smaller_alternative": [n for n, c in C.ALTERNATIVES if c < cap][-1],
        "capacities_cfs": caps,
        "regional_skew": C.REG_SKEW,
        "datum_shift_ft": C.DATUM_SHIFT,
        "cms_to_cfs": C.CFS_PER_CMS,
        "controller_offset_ft": C.LOGGER_OFFSET_ERR,
        "radar_face_install_ft": C.RADAR_FACE_INSTALL,
        "radar_face_new_ft": C.RADAR_FACE_NEW,
        "regional_skew_mse": C.REG_SKEW_MSE,
        "exact": {"design_discharge_cfs": round(float(g["q100"]), 1), "weighted_skew": round(float(g["fit"]["gw"]), 4),
                  "mean_log": round(float(g["fit"]["mean"]), 4), "sd_log": round(float(g["fit"]["sd"]), 4),
                  "station_skew": round(float(g["fit"]["g"]), 4)},
    }
    return f, g


def write_book(f, g, path):
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    import postprocess as PP
    wb = openpyxl.Workbook()
    bold = Font(bold=True)
    head_fill = PatternFill("solid", fgColor="DDE8E1")
    ws = wb.active
    ws.title = "Design flow"
    ws.append(["Sauer pipe bridge replacement: design discharge and waterway alternative"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["TUM-02 Tumwick River near Sauer, annual peaks of water years 1980 to 2025, Engineering Standard 4.2"])
    ws.append([])
    ws.append(["Alternative to carry forward", f["call"]["alternative"]])
    ws.append(["Its capacity (cfs)", f["crit"]["alternative_capacity_cfs"]])
    ws.append(["1 percent annual chance peak discharge at TUM-02 (cfs)", f["call"]["design_discharge_cfs"]])
    for c in ("A4", "B4", "A6", "B6"):
        ws[c].font = bold
    ws.append([])
    ws.append(["Log-Pearson Type III, moments of base-10 logs", ""])
    ws["A8"].font = bold
    fit = g["fit"]
    ws.append(["Annual peaks", fit["n"]])
    ws.append(["Mean of logs", round(float(fit["mean"]), 4)])
    ws.append(["Standard deviation of logs", round(float(fit["sd"]), 4)])
    ws.append(["Station skew", round(float(fit["g"]), 3)])
    ws.append(["Mean square error of station skew (Table 4.2)", round(float(fit["mse_g"]), 3)])
    ws.append(["Generalized skew (MSE %.3f)" % C.REG_SKEW_MSE, C.REG_SKEW])
    ws.append(["Weighted skew", round(float(fit["gw"]), 3)])
    ws.append(["Frequency factor K at 1 percent", round(float(stats.pearson3.ppf(0.99, fit["gw"])), 4)])
    ws.append([])
    ws.append(["Alternative", "Capacity (cfs)", "Annual chance capacity is exceeded"])
    for c in ws[ws.max_row]:
        c.font = bold
        c.fill = head_fill
    for n, cap in C.ALTERNATIVES:
        ws.append([n, cap, round(calc.lp3_aep(fit, cap), 4)])
        ws.cell(ws.max_row, 3).number_format = "0.00%"
    ws.column_dimensions["A"].width = 52
    ws.column_dimensions["B"].width = 16
    ws.column_dimensions["C"].width = 34
    for row in ws.iter_rows(min_row=4, max_row=6, min_col=2, max_col=2):
        for c in row:
            if isinstance(c.value, int):
                c.number_format = "#,##0"
    for row in ws.iter_rows(min_row=20, max_row=ws.max_row, min_col=2, max_col=2):
        for c in row:
            c.number_format = "#,##0"

    ws2 = wb.create_sheet("Annual peaks")
    ws2.append(["Water year", "Peak stage (ft, current datum)", "Peak discharge (cfs)", "Weibull exceedance probability"])
    for c in ws2[1]:
        c.font = bold
        c.fill = head_fill
    peaks = g["peaks"]
    qp = g["qpeaks"]
    order = np.argsort(-qp)
    rank = np.empty(len(qp), int)
    rank[order] = np.arange(1, len(qp) + 1)
    for (wy, h, _), q, k in zip(peaks, qp, rank):
        ws2.append([wy, round(h, 2), int(round(float(q), -1)), round(k / (len(qp) + 1), 4)])
    for col, w in zip("ABCD", (12, 30, 22, 30)):
        ws2.column_dimensions[col].width = w
    for row in ws2.iter_rows(min_row=2, min_col=3, max_col=3):
        for c in row:
            c.number_format = "#,##0"
    ws2.freeze_panes = "A2"

    ws3 = wb.create_sheet("Rating")
    ws3.append(["Stage-discharge relation fitted to %d measurements, water years 1980 to 2025" % f["measurements"]])
    ws3["A1"].font = bold
    ws3.append(["Channel: power law fitted below the break; floodplain term above it; break at %.2f ft (least squares on "
                "log discharge)" % f["breakpoint_ft"]])
    ws3.append([])
    ws3.append(["Stage (ft)", "Discharge (cfs)"])
    for c in ws3[4]:
        c.font = bold
        c.fill = head_fill
    for hh in np.arange(2.0, 13.01, 0.5):
        ws3.append([round(float(hh), 2), int(round(float(g["rating"](np.array([hh]))[0]), -1))])
    ws3.column_dimensions["A"].width = 14
    ws3.column_dimensions["B"].width = 18

    ws4 = wb.create_sheet("Work windows")
    ws4.append(["Highest river stage at TUM-02, 15 July to 15 September"])
    ws4["A1"].font = bold
    ws4.append(["Year", "Stage (ft)", "Date"])
    for c in ws4[2]:
        c.font = bold
        c.fill = head_fill
    for y, v in f["ask_a"].items():
        ws4.append([int(y), v["stage_ft"], dt.date.fromisoformat(v["date"])])
        ws4.cell(ws4.max_row, 3).number_format = "yyyy-mm-dd"
    for col, w in zip("ABC", (10, 12, 14)):
        ws4.column_dimensions[col].width = w
    ws4.freeze_panes = "A3"

    ws5 = wb.create_sheet("Pipe crests")
    ws5.append(["Water level at the pipe bridge radar at TUM-02's crest reading"])
    ws5["A1"].font = bold
    ws5.append(["Water year", "Water level at radar (ft NAVD88)", "Fall from TUM-02 (ft)"])
    for c in ws5[2]:
        c.font = bold
        c.fill = head_fill
    for y, v in f["ask_b"].items():
        ws5.append([int(y), v["pipe_level_ft"], v["fall_ft"]])
    for col, w in zip("ABC", (12, 32, 22)):
        ws5.column_dimensions[col].width = w
    ws5.freeze_panes = "A3"
    ws6 = wb.create_sheet("Notes")
    notes = [
        ("Notes",),
        ("Stages are feet on the TUM-02 gage datum in use since 1 October 2009 (182.40 ft NAVD88); stages and gage "
         "heights recorded before then are raised 2.00 ft.",),
        ("Measured discharges in m3/s (ADCP, through water year 2014) are converted at 35.3147 cfs per m3/s.",),
        ("Annual peaks are the largest instantaneous stage of each water year (1 October to 30 September): the register "
         "for 1980 to 2015, the 15-minute record for 2016 to 2025.",),
        ("Frequency analysis per Engineering Standard 4.2 (issue 3). The design discharge is reported to the nearest 1,000 cfs.",),
        ("Work windows: readings taken while a hydrographer was on site are left out (visit log times are local); the "
         "controller offset of 0.47 ft is removed from 11 June to 27 August 2025.",),
        ("Pipe crests: historian stamps before the 21 June 2022 server replacement are UTC; the radar level is the "
         "surveyed sensor face less the measured distance (199.34 ft to 16 November 2022, 199.84 ft after).",),
        ("Prepared from the pack of 20 January 2026.",),
    ]
    for n_ in notes:
        ws6.append(list(n_))
    ws6["A1"].font = bold
    ws6.column_dimensions["A"].width = 120
    wb.save(path)
    PP.normalize_ooxml(path, "Gary Wagner", "Gary Wagner", "2026-01-21T17:02:44Z", "2026-01-27T22:39:18Z", excel=True,
                       company=C.COMPANY)


def write_chart(f, g, path):
    import matplotlib
    matplotlib.use("Agg")
    matplotlib.rcParams["svg.hashsalt"] = "task178"
    matplotlib.rcParams["svg.fonttype"] = "none"
    matplotlib.rcParams["font.family"] = "DejaVu Sans"
    import matplotlib.pyplot as plt
    fit = g["fit"]
    qp = np.sort(g["qpeaks"])[::-1]
    n = len(qp)
    pexc = np.arange(1, n + 1) / (n + 1)
    z = lambda p: stats.norm.ppf(1 - np.asarray(p))
    fig, ax = plt.subplots(figsize=(10.0, 5.8), dpi=100)
    pp = np.array([0.95, 0.9, 0.8, 0.5, 0.2, 0.1, 0.04, 0.02, 0.01, 0.005, 0.002])
    pc = np.linspace(0.97, 0.0015, 200)
    k = stats.pearson3.ppf(1 - pc, fit["gw"])
    ax.plot(z(pc), 10 ** (fit["mean"] + k * fit["sd"]), color="#22543d", lw=1.8,
            label="Log-Pearson Type III, weighted skew %.3f" % fit["gw"])
    ax.scatter(z(pexc), qp, s=16, color="#3c6e91", zorder=3, label="Annual peaks, WY 1980 to 2025 (Weibull)")
    for nm, cap in C.ALTERNATIVES:
        col = "#b24a2f" if nm == f["call"]["alternative"] else "#9aa3ab"
        ax.axhline(cap, color=col, lw=1.0 if nm != f["call"]["alternative"] else 1.4, ls="--")
        ax.text(1.008, cap, "%s  %s cfs" % (nm, "{:,}".format(cap)), va="center", fontsize=8, color=col,
                transform=ax.get_yaxis_transform(), clip_on=False)
    ax.axvline(z(0.01), color="#5a626b", lw=0.8, ls=":")
    q100 = calc.lp3_q(fit)
    ax.plot([z(0.01)], [q100], marker="o", color="#b24a2f", ms=6, zorder=4)
    ax.annotate("1%% annual chance: %s cfs" % "{:,}".format(f["call"]["design_discharge_cfs"]), (z(0.01), q100),
                xytext=(z(0.2), q100 * 1.18), fontsize=8.5, arrowprops=dict(arrowstyle="-", color="#5a626b", lw=0.7))
    ax.set_yscale("log")
    ax.set_xticks(z(pp))
    ax.set_xticklabels(["%g" % (100 * p) for p in pp])
    ax.set_xlim(z(0.97), z(0.0012))
    ax.set_ylim(1500, 26000)
    ax.set_yticks([2000, 3000, 5000, 7000, 10000, 15000, 20000])
    ax.set_yticklabels(["2,000", "3,000", "5,000", "7,000", "10,000", "15,000", "20,000"])
    from matplotlib.ticker import NullFormatter
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.set_xlabel("Annual exceedance probability (percent)")
    ax.set_ylabel("Peak discharge at TUM-02 (cfs)")
    ax.set_title("Alternative %s (%s cfs) is the smallest waterway that passes the 1%% annual chance flood"
                 % (f["call"]["alternative"], "{:,}".format(f["crit"]["alternative_capacity_cfs"])), fontsize=10.5)
    ax.grid(True, which="major", color="#e3e7ea", lw=0.6)
    ax.legend(loc="upper left", fontsize=8.5, frameon=False)
    fig.tight_layout()
    fig.savefig(path, format="svg", metadata={"Date": None, "Creator": None, "Title": "Sauer crossing frequency curve"})
    plt.close(fig)
    import re as _re
    svg = open(path, encoding="utf-8").read()
    svg = _re.sub(r"<!-- Created with [^>]*-->\n?", "", svg).replace('id="matplotlib.', 'id="')
    open(path, "w", encoding="utf-8").write(svg)


def submission(f):
    c = f["call"]
    caps = f["capacities_cfs"]
    below = f["next_smaller_alternative"]
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Physical & Environmental Sciences, hydrology and flood frequency.")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Carry forward Alternative %s (%s cfs) for the Sauer pipe bridge.** The 1 per cent annual chance peak "
             "discharge at TUM-02 is %s cfs, so Alternative %s (%s cfs) falls short. Not Alternative %s, which a single "
             "power-law rating through every gauging gives, because that curve runs under every gauging above about "
             "%.1f ft and understates the floodplain peaks."
             % (c["alternative"], "{:,}".format(caps[c["alternative"]]), "{:,}".format(c["design_discharge_cfs"]), below,
                "{:,}".format(caps[below]), f["default"]["alternative"], f["breakpoint_ft"]))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. The station skew of the 46 annual peaks' base-10 logarithms is **%.1f**." % f["crit"]["station_skew"])
    L.append("2. The 1 per cent annual chance peak discharge at TUM-02 is **%s cfs**." % "{:,}".format(c["design_discharge_cfs"]))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Took water years 1980 to 2015's peaks from tum02_annual_peaks_wy1980-2015.csv and water years 2016 to "
             "2025's maxima from tum02_stage_15min_wy2016-2025.csv, adding 2.00 ft to stages before 1 October 2009 "
             "(tum02_station_description.pdf): 46 peak stages on the current datum.")
    L.append("2. Stacked the measurements in tum02_measurement_notes_1980-2004.xlsx and tum02_measurements_wy2005-2025.csv, "
             "m3/s converted at 35.3147 and old-datum gage heights raised 2.00 ft: %d measurements." % f["measurements"])
    L.append("3. Fitted the rating as a power law below a break and a floodplain term added above it, the break found by "
             "least squares on log discharge at %.2f ft, and rated every peak stage through it." % f["breakpoint_ft"])
    L.append("4. Fitted log-Pearson Type III by moments of the logs with the station skew weighted with the generalized "
             "skew of %.2f as %s sets out: %s cfs at 1 per cent, so "
             "Alternative %s." % (C.REG_SKEW, C.F_STANDARD, "{:,}".format(c["design_discharge_cfs"]), c["alternative"]))
    L.append("5. Work windows: dropped every 15-minute reading from arrival to departure of each visit in "
             "tum02_site_visits_2016-2025.csv, its times read on the local clock (orifice purges lift the readings "
             "inside the visit), and took the 0.47 ft controller offset off from the 11 June 2025 visit to the 27 August "
             "2025 reset; the highest remaining reading in each 15 July to 15 September window gives the stages below.")
    L.append("6. Pipe crests: read scada_sauer_crossing_2019-2025.csv's timestamps as UTC before the 21 June 2022 "
             "historian replacement (cmms_work_orders_sauer_2019-2025.csv) and local after, and the level as the "
             "sensor face less the distance, 199.34 ft before and 199.84 ft after the 16 November 2022 bracket "
             "replacement (tum02_levels_log.txt); read it at TUM-02's crest reading for the levels and falls below.")
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### sauer_crossing_design_flow.xlsx")
    L.append("")
    L.append("1. Alternative carried forward: Alternative %s." % c["alternative"])
    L.append("2. 1 per cent annual chance peak discharge at TUM-02: %s cfs." % "{:,}".format(c["design_discharge_cfs"]))
    L.append("3. Highest stage the river reached at TUM-02 in each 15 July to 15 September window, ft, with its date:")
    for y, v in f["ask_a"].items():
        L.append("   - %s: %.2f ft on %s" % (y, v["stage_ft"], long_date(v["date"])))
    L.append("4. Water level at the pipe bridge radar at TUM-02's crest reading, ft NAVD88, and the fall from TUM-02, ft:")
    for y, v in f["ask_b"].items():
        L.append("   - Water year %s: %.2f ft, fall %.2f ft" % (y, v["pipe_level_ft"], v["fall_ft"]))
    L.append("")
    L.append("### sauer_crossing_frequency_curve.svg")
    L.append("")
    L.append("1. The 46 annual peak discharges plotted at Weibull exceedance probabilities on a probability axis, the fitted "
             "log-Pearson Type III curve, the seven alternatives' capacities as horizontal lines with Alternative %s "
             "highlighted, the 1 per cent point marked at %s cfs, titled with the alternative carried forward."
             % (c["alternative"], "{:,}".format(c["design_discharge_cfs"])))
    return "\n".join(L) + "\n"


def main(target, golden_dir, fig_path, sub_path):
    os.makedirs(golden_dir, exist_ok=True)
    f, g = figures(target)
    write_book(f, g, os.path.join(golden_dir, C.G_BOOK))
    write_chart(f, g, os.path.join(golden_dir, C.G_CHART))
    with open(fig_path, "w", encoding="utf-8") as fh:
        json.dump(f, fh, indent=1, sort_keys=True, default=lambda o: o.item() if hasattr(o, "item") else str(o))
        fh.write("\n")
    with open(sub_path, "w", encoding="utf-8") as fh:
        fh.write(submission(f))
    return f
