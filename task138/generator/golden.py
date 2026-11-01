"""The golden deliverables, computed from target/ through analysis.py: the review workbook and the memo to the
Board with its frequency chart. Also writes figures.json for figures_check.py."""
import io
import json
import os
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import openpyxl  # noqa: E402
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side  # noqa: E402
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402
from scipy import stats  # noqa: E402

import analysis as A  # noqa: E402
import io_util as IO  # noqa: E402
import lp3 as L  # noqa: E402

BOOK = "levee_raise_review.xlsx"
MEMO = "levee_raise_memo.pdf"
REACH_NAMES = {"R1": "north tie-in to Pump Station 1", "R2": "Riverside Park",
               "R3": "Front Street to the Main Street closure", "R4": "Main Street closure to Cedar Street",
               "R5": "Cedar Street to the railroad closure", "R6": "railroad closure to the grain terminal",
               "R7": "grain terminal to Pump Station 2", "R8": "Pump Station 2 to the south tie-in"}


def cap(s):
    return s[0].upper() + s[1:]


def compute(target):
    P = A.Pack(target)
    m = A.main_figures(P)
    AF = A.AskFiles(target)
    a = A.ask_figures(AF)
    wy = np.array(P.hal.index)
    T = P.hal.values
    U = P.coy.reindex(wy).values
    cut = m["cut"]
    post = wy >= cut
    r = float(np.sum(T[post] * U[post]) / np.sum(U[post] ** 2))
    series = A.present_series(P)
    at_site = A.fit(T, P)
    rt = A.routes(P)
    reach_pts = {}
    off = A.station_offset(AF)[0][0]
    for k in a["settlement_raw"]:
        reach_pts[k] = 0
    z24 = AF.c24[AF.c24.code == "CL"].set_index("sta")
    for _, row in AF.c16[AF.c16.DESC == "CL"].iterrows():
        s = int(row["sta"]) - off
        if s in z24.index:
            reach_pts[z24.loc[s, "reach"]] += 1
    reach_span = AF.c24.groupby("reach")["sta"].agg(["min", "max"])
    return {"P": P, "m": m, "AF": AF, "a": a, "wy": wy, "T": T, "U": U, "r": r, "series": series, "post": post,
            "at_site": at_site, "routes": rt, "reach_pts": reach_pts, "reach_span": reach_span, "offset": off,
            "shift": A.datum_shift(AF), "change": A.coy_datum_change(AF)[0], "swap": A.halbrook_clock(AF)[0]}


# ------------------------------------------------------------------ workbook
HEAD = Font(bold=True, color="1F2A30")
FILL = PatternFill("solid", fgColor="E6ECEF")
THIN = Border(bottom=Side(style="thin", color="7D8B93"))


def _header(ws, row, cols):
    ws.append(cols)
    for c in ws[row]:
        c.font = HEAD
        c.fill = FILL
        c.border = THIN
        c.alignment = Alignment(wrap_text=True, vertical="bottom")


def write_book(path, G):
    P, m, a = G["P"], G["m"], G["a"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Raise options"
    ws.append(["Orrinsford levee: crown raise options against the LS-02 design flood"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Design flood (1 per cent annual chance, Orrinsford gauge, river as it now runs)",
               None, None, round(m["q_design"], -2)])
    ws.append(["Design flood, as reported (nearest 5,000 cfs)", None, None, m["q_design_5k"]])
    ws.append([])
    _header(ws, 5, ["Uniform crown raise (ft)", "Discharge held with freeboard (cfs)", "Governing cross-section",
                    "Annual chance of exceedance (%)", "Meets LS-02"])
    for i, rr in enumerate(A.RAISES):
        ws.append([rr, int(round(m["capacity"][i], -2)), "%d+%02d" % divmod(m["governing"][i], 100),
                   round(m["aep"][i], 1), "Yes" if m["aep"][i] <= 100 * P.aep else "No"])
    ws.append([])
    ws.append(["Recommended raise (ft)", None, None, m["raise"]])
    ws.append(["Shortfall at 118+70 today against design water surface plus freeboard (ft)", None, None,
               round(m["need"], 2)])
    for c, w in zip("ABCDE", (34, 22, 16, 18, 12)):
        ws.column_dimensions[c].width = w
    for row in ws.iter_rows(min_row=6, max_row=10):
        row[1].number_format = "#,##0"
        row[3].number_format = "0.0"
    ws["D2"].number_format = "#,##0"
    ws["D3"].number_format = "#,##0"

    wd = wb.create_sheet("Design flood series")
    wd.append(["Annual peaks at Orrinsford for the river as it now runs"])
    wd["A1"].font = Font(bold=True, size=12)
    wd.append(["Water years %d onward: Orrinsford as published. Earlier years: Coyle Bridge peak x %.3f, the "
               "Orrinsford to Coyle Bridge relation of water years %d to %d." % (G["m"]["cut"], G["r"], G["m"]["cut"],
                                                                                int(G["wy"].max()))])
    wd.append([])
    _header(wd, 4, ["Water year", "Coyle Bridge peak (cfs)", "Orrinsford peak as published (cfs)",
                    "Orrinsford peak, river as it now runs (cfs)", "Basis"])
    for w_, u, t, s, p in zip(G["wy"], G["U"], G["T"], G["series"], G["post"]):
        wd.append([int(w_), int(u), int(t), int(round(s)), "published" if p else "from Coyle Bridge"])
    f = m["fit"]
    n0 = wd.max_row + 2
    wd.cell(n0, 1, "Log-Pearson Type III, method of moments on log10 peaks").font = HEAD
    rows = [("Years", f["n"]), ("Mean of logs", round(f["mean"], 4)), ("Standard deviation of logs", round(f["sd"], 4)),
            ("Station skew", round(f["g"], 3)), ("Regional skew (SW-16-03, region 2)", P.gr),
            ("Weighted skew", round(f["gw"], 3)), ("1 per cent annual chance discharge (cfs)", round(m["q_design"], -2))]
    for i, (k, v) in enumerate(rows):
        wd.cell(n0 + 1 + i, 1, k)
        wd.cell(n0 + 1 + i, 4, v)
    for c, w in zip("ABCDE", (12, 22, 26, 30, 18)):
        wd.column_dimensions[c].width = w
    for row in wd.iter_rows(min_row=5, max_row=4 + len(G["wy"])):
        for c in row[1:4]:
            c.number_format = "#,##0"
    wd.freeze_panes = "A5"

    wsl = wb.create_sheet("Crown settlement")
    _header(wsl, 1, ["Reach", "Description", "From station", "To station", "Points compared",
                     "Settlement 2016 to 2024 (ft)"])
    for k, v in a["settlement"].items():
        lo, hi = G["reach_span"].loc[k, "min"], G["reach_span"].loc[k, "max"]
        wsl.append([k, cap(REACH_NAMES[k]), "%d+%02d" % divmod(int(lo), 100), "%d+%02d" % divmod(int(hi), 100),
                    G["reach_pts"][k], v])
    wsl.append([])
    wsl.append(["2016 shots moved to the 2019 stationing (%d ft) and to NAVD 88 (+%.2f ft, district benchmarks)."
                % (G["offset"], G["shift"])])
    for c, w in zip("ABCDEF", (8, 40, 13, 13, 15, 16)):
        wsl.column_dimensions[c].width = w
    for row in wsl.iter_rows(min_row=2, max_row=9):
        row[5].number_format = "0.00"

    wl = wb.create_sheet("Closure lead times")
    _header(wl, 1, ["Flood", "Coyle Bridge warning level reached (UTC)", "Main Street sill reached at Orrinsford (UTC)",
                    "Lead time (h)"])
    for (t_h, h) in a["lead_raw"]:
        t_c = t_h - np.timedelta64(int(round(h * 3600)), "s")
        wl.append([t_h.strftime("%B %Y"), t_c.strftime("%Y-%m-%d %H:%M"), t_h.strftime("%Y-%m-%d %H:%M"),
                   int(round(h))])
    wl.append([])
    wl.append(["Warning: 21.0 ft on the Coyle Bridge gauge before the %s datum change, 23.00 ft after (661.00 ft "
               "NGVD 29). Sill: %.2f ft NAVD 88. Orrinsford logger times before %s converted from CST."
               % ("%d %s" % (G["change"].day, G["change"].strftime("%B %Y")), G["AF"].sill,
                  "%d %s" % (G["swap"].day, G["swap"].strftime("%B %Y")))])
    for c, w in zip("ABCD", (16, 30, 30, 14)):
        wl.column_dimensions[c].width = w
    wn = wb.create_sheet("Notes")
    for line in ("Orrinsford levee crown review for the 2027 capital plan, as of 9 November 2026.",
                 "Annual peaks: State Water Survey export of 28 October 2026 (water years 1962 to 2026, 2026 "
                 "provisional), each peak in its water year (October to September).",
                 "Frequency method: LS-02 section 3, log-Pearson Type III by moments on log10 peaks, station skew "
                 "weighted with SW-16-03 region 2 (-0.08, mean square error 0.14).",
                 "Water surfaces: HWE-1907 Table 4, linear in discharge (LS-02 section 4). Freeboard: LS-02 section 5. "
                 "Crown: 2024 certification survey, ft NAVD 88, 2019 stationing.",
                 "Settlement: 2016 shots moved to the 2019 stationing and to NAVD 88; structures and benchmark check "
                 "shots left out.",
                 "Lead times: Coyle Bridge hourly record (UTC) and the ORF2 logger at Orrinsford, stamps before the June "
                 "2021 logger swap moved from CST to UTC; crossings interpolated within the hour.",
                 "Rounding: design discharge to the nearest 5,000 cfs, annual chances to 0.1 per cent, settlement "
                 "to 0.01 ft, lead times to whole hours; computed unrounded."):
        wn.append([line])
    wn.column_dimensions["A"].width = 120
    wb.save(path)
    IO.repack_ooxml(path, "OLDD Engineering", "OLDD Engineering", "2026-11-06T14:10:00Z", "2026-11-09T08:45:00Z",
                    "Orrinsford levee raise review", "Orrinsford Levee and Drainage District")


# ------------------------------------------------------------------ chart and memo
def chart_png(G):
    P, m = G["P"], G["m"]
    f, f0 = m["fit"], G["at_site"]
    aeps = np.array([50, 20, 10, 5, 2, 1, 0.5, 0.2])
    grid = np.exp(np.linspace(np.log(60), np.log(0.15), 120))
    zq = lambda fit, p: 10 ** (fit["mean"] + stats.pearson3.ppf(1 - p / 100.0, fit["gw"]) * fit["sd"])  # noqa: E731
    fig, ax = plt.subplots(figsize=(6.6, 3.25), dpi=150)
    xs = -stats.norm.ppf(grid / 100.0)
    ax.plot(xs, [zq(f, p) / 1000 for p in grid], color="#1f4e79", lw=2.0, label="River as it now runs")
    ax.plot(xs, [zq(f0, p) / 1000 for p in grid], color="#9aa5ad", lw=1.4, ls="--",
            label="Orrinsford record as published")
    s = np.sort(G["series"])[::-1]
    pp = 100 * np.arange(1, len(s) + 1) / (len(s) + 1)
    ax.scatter(-stats.norm.ppf(pp / 100.0), s / 1000, s=9, color="#1f4e79", alpha=0.55, zorder=3)
    xl = (-stats.norm.ppf(0.6), -stats.norm.ppf(0.0015))
    for i, rr in enumerate(A.RAISES):
        c = m["capacity"][i] / 1000
        ax.axhline(c, color="#b5651d" if rr == m["raise"] else "#c9b49a", lw=1.0 if rr != m["raise"] else 1.6)
        ax.text(xl[0] + 0.05, c + 0.6, "%d ft raise: %s cfs" % (rr, "{:,}".format(int(round(m["capacity"][i], -2)))),
                fontsize=6.6, color="#6b4a2b")
    ax.axvline(-stats.norm.ppf(0.01), color="#444444", lw=0.8, ls=":")
    ax.text(-stats.norm.ppf(0.01) - 0.04, 6, "1 per cent", fontsize=6.6, color="#444444", ha="right")
    ax.set_title("A %d ft raise is the smallest that holds the present river's 1 per cent flood" % m["raise"],
                 fontsize=8.6, loc="left", color="#1f2a30")
    ax.set_xticks([-stats.norm.ppf(p / 100.0) for p in aeps])
    ax.set_xticklabels(["%g" % p for p in aeps], fontsize=7)
    ax.set_xlim(*xl)
    ax.set_ylim(0, 150)
    ax.tick_params(axis="y", labelsize=7)
    ax.set_xlabel("Annual chance of exceedance (%)", fontsize=7.5)
    ax.set_ylabel("Peak discharge at Orrinsford (thousand cfs)", fontsize=7.5)
    ax.grid(axis="y", color="#e3e7ea", lw=0.6)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.legend(fontsize=7, frameon=False, loc="lower right")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def write_memo(path, G, png):
    P, m, a = G["P"], G["m"], G["a"]
    st = IO._styles()
    doc = SimpleDocTemplate(path, pagesize=IO.A4, leftMargin=19 * mm, rightMargin=19 * mm, topMargin=14 * mm,
                            bottomMargin=15 * mm, title="Orrinsford levee crown review", author="Dennis Zhang",
                            creator="Orrinsford Levee and Drainage District",
                            producer="Orrinsford Levee and Drainage District", invariant=1)
    width = IO.A4[0] - 38 * mm
    rows = [["Raise", "Holds with freeboard", "Annual chance", "Meets LS-02"]]
    for i, rr in enumerate(A.RAISES):
        rows.append(["%d ft" % rr, "{:,} cfs".format(int(round(m["capacity"][i], -2))), "%.1f%%" % m["aep"][i],
                     "yes" if m["aep"][i] <= 100 * P.aep else "no"])
    q5 = "{:,}".format(m["q_design_5k"])
    big = G["wy"][~G["post"]][np.argmax(G["U"][~G["post"]])]
    ib = list(G["wy"]).index(big)
    story = [
        Paragraph("The Orrinsford levee needs a %d ft crown raise before the 2027 flood season" % m["raise"], st["t"]),
        Paragraph("To the Board of Trustees from Dennis Zhang, district engineer. 9 November 2026. Crown review under "
                  "LS-02 for the 2027 capital plan.", st["s"]),
        Paragraph("<b>Recommendation.</b> Raise the levee crown by %d ft before the 2027 flood season. The design "
                  "flood for the river as it now runs is about %s cfs at the Orrinsford gauge, and the levee as "
                  "surveyed in 2024 holds only %s cfs with its freeboard: the railroad closure at 118+70 is %.2f ft "
                  "short. A 1 ft raise still leaves a %.1f%% annual chance of exceeding what the levee holds; 2 ft "
                  "brings it to %.1f%%." % (m["raise"], q5, "{:,}".format(int(round(m["capacity"][0], -2))),
                                            m["need"], m["aep"][1], m["aep"][2]), st["p"]),
        Paragraph("<b>Why the published record understates the flood.</b> Until the six agricultural levees "
                  "between Coyle Bridge and Orrinsford were raised (1996 to 2008, the last in force from water "
                  "year %d) their floodplains filled in every large flood and took the top off it before it "
                  "reached town: in %d Coyle Bridge peaked at %s cfs and Orrinsford at %s cfs. Since water year "
                  "%d Orrinsford has run at %.3f times Coyle Bridge at every size of flood, including %s and %s cfs "
                  "in 2020 and 2024. The fit to the published Orrinsford record (%s cfs) describes a river that "
                  "no longer exists, and a trend test on it does not show this. I carried Coyle Bridge's "
                  "peaks for %d to %d across at the present relation and kept Orrinsford's own peaks from %d."
                  % (m["cut"], big, "{:,}".format(int(G["U"][ib])), "{:,}".format(int(G["T"][ib])), m["cut"],
                     G["r"], "{:,}".format(int(P.hal[2020])), "{:,}".format(int(P.hal[2024])),
                     "{:,}".format(int(round(G["routes"]["R0_at_site"]["q"], -3))), int(G["wy"].min()),
                     m["cut"] - 1, m["cut"]), st["p"]),
        Image(io.BytesIO(png), width=width, height=width * 3.25 / 6.6),
        Paragraph("Present-river and published-record frequency curves at Orrinsford, with the discharge each "
                  "uniform raise would hold under LS-02 freeboard (railroad closure governs throughout). Annual "
                  "peaks: State Water Survey export of 28 October 2026, water year 2026 provisional; water surfaces: "
                  "HWE-1907 Table 4 read linearly in discharge; crown: 2024 certification survey.", st["s"]),
        Spacer(1, 4),
    ]
    t = Table([[Paragraph(IO.esc(c), st["head"] if i == 0 else st["cell"]) for c in r] for i, r in enumerate(rows)],
              colWidths=[22 * mm, 44 * mm, 32 * mm, 30 * mm], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, IO.RULE), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                           ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BACKGROUND", (0, m["raise"] + 1),
                                                                    (-1, m["raise"] + 1),
                                                                    colors.HexColor("#f3ead9"))]))
    story += [t, Spacer(1, 6)]
    sv = a["settlement"]
    worst = max(sv, key=sv.get)
    least = min(sv, key=sv.get)
    ld = a["lead"]
    words = {7: "seven", 6: "six", 8: "eight", 5: "five"}
    story += [
        Paragraph("<b>Settlement and warning time.</b> Between the 2016 and 2024 surveys the crown settled from "
                  "%.2f ft (%s, %s) to %.2f ft (%s, %s); the workbook gives every reach. The Coyle Bridge warning "
                  "gave between %d and %d hours before the river reached the Main Street sill in the %s floods "
                  "since October 2016, against about 18 hours to install the stoplogs."
                  % (sv[least], least, REACH_NAMES[least], sv[worst], worst, REACH_NAMES[worst],
                     min(h for _, h in ld), max(h for _, h in ld), words.get(len(ld), str(len(ld)))), st["p"]),
        Paragraph("The 2016 survey was taken on the stationing in use before the 2019 north tie-in and on NGVD 29; "
                  "its shots are compared at their present stations, on NAVD 88. Warning times use the warning "
                  "level OP-04 sets as an elevation, on the Coyle Bridge gauge datum in force at each flood.",
                  st["s"]),
    ]

    def page(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.2)
        canvas.setFillColor(colors.HexColor("#5b666d"))
        canvas.drawString(20 * mm, 9 * mm, "Orrinsford Levee and Drainage District | crown review | 2027 capital plan")
        canvas.drawRightString(IO.A4[0] - 20 * mm, 9 * mm, "Page %d" % d.page)
        canvas.restoreState()
    doc.build(story, onFirstPage=page, onLaterPages=page)
    data = open(path, "rb").read()
    for sig in (b"ReportLab Generated PDF document (opensource)",
                b"ReportLab generated PDF document -- digest (opensource)",
                b"ReportLab Generated PDF document http://www.reportlab.com"):
        data = data.replace(sig, b" " * len(sig))
    data = re.sub(rb"/CreationDate \(D:[^)]*\)", b"/CreationDate (D:20261109084500-06'00')", data)
    data = re.sub(rb"/ModDate \(D:[^)]*\)", b"/ModDate (D:20261109091200-06'00')", data)
    open(path, "wb").write(data)


def figures(G):
    m, a = G["m"], G["a"]
    rt = G["routes"]
    return {
        "call": {"raise_ft": m["raise"], "design_discharge_cfs": m["q_design_5k"]},
        "design_discharge_raw": round(m["q_design"], 1),
        "shortfall_118_70_ft": round(m["need"], 2),
        "aep_pct_by_raise": {"%d ft" % r: round(v, 1) for r, v in zip(A.RAISES, m["aep"])},
        "aep_raw": {"%d ft" % r: round(v, 4) for r, v in zip(A.RAISES, m["aep"])},
        "capacity_cfs_by_raise": {"%d ft" % r: int(round(v, -2)) for r, v in zip(A.RAISES, m["capacity"])},
        "first_fully_raised_wy": m["cut"],
        "present_relation": round(G["r"], 3),
        "settlement_ft": a["settlement"],
        "settlement_raw": {k: round(v, 4) for k, v in a["settlement_raw"].items()},
        "lead_time_h": {d: h for d, h in a["lead"]},
        "lead_raw": {t.strftime("%Y-%m-%d"): round(float(h), 3) for t, h in a["lead_raw"]},
        "flood_count": len(a["lead"]),
        "rungs": {k: {"q": int(round(v["q"])), "raise": v["raise"]} for k, v in rt.items()},
        "rungs_5k": {k: int(round(v["q"] / 5000.0) * 5000) for k, v in rt.items()},
        "rungs_1k": {k: int(round(v["q"], -3)) for k, v in rt.items()},
        "pre_raise_years": int((~G["post"]).sum()), "post_raise_years": int(G["post"].sum()),
        "river_miles": {"coyle": float(G["P"].gauges.set_index("Site").loc["05432100", "River mile"]),
                        "halbrook": float(G["P"].gauges.set_index("Site").loc["05433000", "River mile"])},
        "freeboard": {"general_ft": G["P"].fb_gen, "bridge_ft": G["P"].fb_bridge, "within_ft": 100,
                      "upstream_ft": G["P"].fb_up},
        "regional_skew_mse": G["P"].mse_r,
        "warning": {"elev_ngvd29": G["AF"].warn_elev, "stage_2014_ft": G["AF"].warn_stage,
                    "stage_now_ft": round(G["AF"].warn_elev - G["AF"].coy_datum_now, 2),
                    "datum_now": G["AF"].coy_datum_now, "step_ft": 2.00},
        "halbrook_gauge": {"datum_ngvd29": G["AF"].hb_datum,
                           "sill_stage_ft": round(G["AF"].sill - (G["AF"].hb_datum + G["shift"]), 2),
                           "clock_shift_h": 6},
        "stations": [118, 70, 62, 40, 180, 0],
        "rounding_cfs": 5000, "datum_names": [88, 29],
        "station_offset_ft": G["offset"], "datum_shift_ft": round(G["shift"], 2),
        "constants": {"warning_old_ft": 21.0, "warning_new_ft": 23.0, "sill_navd88": G["AF"].sill,
                      "install_h": 18, "at_site_q_1000": int(round(rt["R0_at_site"]["q"], -3)),
                      "coyle_1970": int(G["U"][list(G["wy"]).index(1970)]),
                      "halbrook_1970": int(G["T"][list(G["wy"]).index(1970)]),
                      "halbrook_2020": int(G["P"].hal[2020]), "halbrook_2024": int(G["P"].hal[2024]),
                      "regional_skew": G["P"].gr, "years": int(m["fit"]["n"]),
                      "weighted_skew": round(m["fit"]["gw"], 3), "station_skew": round(m["fit"]["g"], 3),
                      "mean_log": round(m["fit"]["mean"], 4), "sd_log": round(m["fit"]["sd"], 4)},
    }


def write_all(target, golden, gen):
    os.makedirs(golden, exist_ok=True)
    G = compute(target)
    write_book(os.path.join(golden, BOOK), G)
    write_memo(os.path.join(golden, MEMO), G, chart_png(G))
    json.dump(figures(G), open(os.path.join(gen, "figures.json"), "w"), indent=1, sort_keys=True)
    return G
