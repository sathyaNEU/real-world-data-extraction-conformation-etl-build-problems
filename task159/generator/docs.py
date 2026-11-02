"""The documents of the pack: the survey control sheet, the 2027 budget basis memo, the monthly reconciliation report,
and two documents the budget does not use (the Phase 5 slope review and the corporate price deck)."""
import math
import numpy as np
import pandas as pd

import params as P
import world as W
from io_util import write_pdf

STAMP_BASIS = "D:20261112163000-05'00'"
STAMP_RECON = "D:20261104101500-05'00'"
STAMP_GEOT = "D:20260915142000-04'00'"
STAMP_PRICE = "D:20261021090000-04'00'"

# filed sentences (also read back by verify.py)
S_CUTOFF = ("From 1 January 2027 the ore cut-off is 0.90 g/t gold. Material from 0.50 to 0.90 g/t goes to the "
            "low-grade stockpile, from 0.30 to 0.50 g/t to the mineralised waste dump and the rest to waste.")
S_SELECT = ("Grade control selects ore at the face block by block, as it has since the pit opened. A block's "
            "grade-control grade is the average of the primary blast-hole assays from the holes collared in it; field "
            "duplicates and the laboratory's control samples are not blast-hole assays. A block is ore when its "
            "grade-control grade is 0.90 g/t or more.")
S_GOLD = ("Budget gold is the gold contained in the ore mined in calendar 2027, in troy ounces, on grade-control "
          "grades and the resource model's block tonnages.")
S_SCHED = ("The Schedule sheet of mine plan 2027 v3 lists every Main Zone block the plan mines in 2027, ore and waste "
           "alike, with its month. Waste outside the Main Zone is scheduled in the fleet plan and carries no gold.")
S_PLANBASIS = "The plan's Summary sheet reports ore and gold on the 2026R resource model's estimates at 0.90 g/t."


def _wrap(text, width=96):
    out, line = [], ""
    for w in text.split():
        if len(line) + len(w) + 1 > width:
            out.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    if line:
        out.append(line)
    return out


def _para(lines, text, size=10, width=96, bold=False, gap=6):
    font = "Helvetica-Bold" if bold else "Helvetica"
    for l in _wrap(text, width):
        lines.append((font, size, l, None, 14))
    if gap:
        lines.append(("Helvetica", 4, "", None, gap))


def grid_control(path):
    th = math.radians(P.ROT_DEG)
    mons = [("KCM-01", 10120.000, 20085.000, 1311.842), ("KCM-02", 10955.000, 20140.000, 1308.117),
            ("KCM-04", 10510.000, 20610.000, 1314.605), ("KCM-07", 10240.000, 20480.000, 1309.230)]
    lines = ["KELVANNA LAKE MINE - MINE GRID CONTROL",
             "Survey Department, issue 3, 14 February 2024 (K. Howell, Chief Surveyor)",
             "",
             "Mine grid ........ Kelvanna Mine Grid (KMG), ground scale",
             "Map grid ......... NAD83(CSRS) UTM zone 17N",
             "Heights .......... mine RL = CGVD2013 orthometric height + 1000.000 m",
             "",
             "KMG to UTM, two-dimensional similarity transformation:",
             "  dX = E(KMG) - 10000.000      dY = N(KMG) - 20000.000",
             "  E(UTM) = %.3f + k * ( dX * cos(a) + dY * sin(a))" % P.E_ORIGIN,
             "  N(UTM) = %.3f + k * (-dX * sin(a) + dY * cos(a))" % P.N_ORIGIN,
             "  a = %.5f degrees (KMG north is %.2f degrees east of UTM grid north)" % (P.ROT_DEG, P.ROT_DEG),
             "  k = %.6f (combined scale factor, ground to grid)" % P.SCALE,
             "",
             "Control monuments (fixed by static GNSS, 2023-11-28):",
             "  MONUMENT   E(KMG)       N(KMG)       RL(KMG)     E(UTM)        N(UTM)         HEIGHT"]
    for name, x, y, rl in mons:
        e, n = W.mine_to_utm(x, y)
        lines.append("  %-9s %10.3f  %11.3f  %9.3f  %12.3f  %13.3f  %8.3f" % (name, x, y, rl, e, n, rl - 1000.0))
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\n".join(lines) + "\n")


def budget_basis(path, plan_file):
    L = []
    L.append(("Helvetica-Bold", 12, "AUBRETH GOLD CORPORATION - KELVANNA LAKE MINE", None, 18))
    L.append(("Helvetica-Bold", 11, "Memorandum", None, 18))
    for a, b in (("To:", "Cindy Smith, General Manager"), ("From:", "Jeffrey Russell, Superintendent, Mine Planning"),
                 ("Copy:", "Brent Peck (Grade Control), Charles Bailey (Mill), Rachael Ochoa (Metallurgy)"),
                 ("Date:", "12 November 2026"), ("Subject:", "2027 budget: basis of ore and gold")):
        L.append(("Helvetica", 10, [a, b], [52, 120], 14))
    L.append(("Helvetica", 4, "", None, 10))
    _para(L, "1. Cut-off", bold=True, gap=2)
    _para(L, S_CUTOFF + " The board approved the change on 27 October 2026 on the new power contract and the 2027 "
                        "reagent and labour rates.")
    _para(L, "2. Ore selection", bold=True, gap=2)
    _para(L, S_SELECT)
    _para(L, "3. Budget gold", bold=True, gap=2)
    _para(L, S_GOLD)
    _para(L, "4. Schedule", bold=True, gap=2)
    _para(L, S_SCHED + " The file is " + plan_file + ".")
    _para(L, "5. The plan's figures", bold=True, gap=2)
    _para(L, S_PLANBASIS + " Mill throughput and availability for 2027 are on the Assumptions sheet.")
    _para(L, "6. Timetable", bold=True, gap=2)
    _para(L, "The budget goes to the board on 8 December 2026. Mine planning needs the budget gold figure and the "
             "supporting trails for the board pack by 27 November.")
    L.append(("Helvetica", 9, "JR/kl   ref MP-2026-118", None, 14))
    write_pdf(path, "2027 budget - basis of ore and gold", "Jeffrey Russell", [L], STAMP_BASIS)


def reconciliation_table(df, gc_by_block, md):
    hist = df[df["period"] == "HIST"].copy()
    hist["gc"] = hist["ijk"].map(gc_by_block)
    md = md.copy()
    md["mi"] = [(d.year - 2023) * 12 + d.month - 1 for d in md["day"]]
    md["dry_rep"] = (md["wet_t"].round(0)) * (1 - md["moist"].round(1) / 100.0)
    md["au_rep"] = md["dry_rep"] * md["head"].round(3)
    rows = []
    for mi in range(P.HIST_MONTHS):
        h = hist[hist["month_idx"] == mi]
        mo = h[h["model"] >= P.OLD_ORE_CUT]
        gco = h[h["gc"] >= P.OLD_ORE_CUT]
        m_t, m_au = mo["tonnes"].sum(), (mo["tonnes"] * mo["model"]).sum()
        g_t, g_au = gco["tonnes"].sum(), (gco["tonnes"] * gco["gc"]).sum()
        mm = md[md["mi"] == mi]
        k_t, k_au = mm["dry_rep"].sum(), mm["au_rep"].sum()
        rows.append(dict(month=W.month_start(mi), m_t=m_t, m_g=m_au / m_t, m_oz=m_au / P.TROY, g_t=g_t, g_g=g_au / g_t,
                         g_oz=g_au / P.TROY, k_t=k_t, k_g=k_au / k_t, k_oz=k_au / P.TROY))
    r = pd.DataFrame(rows)
    return r


def reconciliation_pdf(path, r):
    def fmt_row(label, d):
        f1t, f1g, f1 = d["g_t"] / d["m_t"], d["g_g"] / d["m_g"], d["g_oz"] / d["m_oz"]
        f2, f3 = d["k_oz"] / d["g_oz"], d["k_oz"] / d["m_oz"]
        return [label, "%.1f" % (d["m_t"] / 1000), "%.2f" % d["m_g"], "%.0f" % d["m_oz"], "%.1f" % (d["g_t"] / 1000),
                "%.2f" % d["g_g"], "%.0f" % d["g_oz"], "%.1f" % (d["k_t"] / 1000), "%.2f" % d["k_g"],
                "%.0f" % d["k_oz"], "%.2f" % f1t, "%.2f" % f1g, "%.2f" % f1, "%.2f" % f2, "%.2f" % f3]
    xs = [36, (118,), (150,), (190,), (232,), (264,), (304,), (346,), (378,), (418,), (452,), (480,), (508,), (536,),
          (564,)]
    head1 = ["", "Resource model", "", "", "Grade control", "", "", "Mill", "", "", "F1", "", "", "F2", "F3"]
    head2 = ["Month", "kt", "g/t", "oz", "kt", "g/t", "oz", "kt", "g/t", "oz", "t", "g", "oz", "oz", "oz"]
    pages = []
    years = [2023, 2024, 2025, 2026]
    for y in years:
        L = [("Helvetica-Bold", 11, "Kelvanna Lake Mine - monthly reconciliation, %d" % y, None, 16),
             ("Helvetica", 8, "Mined volume by month-end survey. Resource model 2026R (AU_OK); grade control per the "
                              "GC system; mill by production day (06:00).", None, 12),
             ("Helvetica", 8, "Model and grade control are reported for ore at the 0.50 g/t cut-off. F1 = grade control / "
                              "model; F2 = mill / grade control; F3 = mill / model.", None, 16),
             ("Helvetica-Bold", 7.5, head1, xs, 11), ("Helvetica-Bold", 7.5, head2, xs, 12)]
        ry = r[[m.year == y for m in r["month"]]]
        for _, d in ry.iterrows():
            L.append(("Helvetica", 7.5, fmt_row(d["month"].strftime("%b %Y"), d), xs, 11.5))
        tot = ry[["m_t", "g_t", "k_t", "m_oz", "g_oz", "k_oz"]].sum()
        d = dict(m_t=tot["m_t"], g_t=tot["g_t"], k_t=tot["k_t"], m_oz=tot["m_oz"], g_oz=tot["g_oz"], k_oz=tot["k_oz"])
        d["m_g"], d["g_g"], d["k_g"] = (d["m_oz"] * P.TROY / d["m_t"], d["g_oz"] * P.TROY / d["g_t"],
                                        d["k_oz"] * P.TROY / d["k_t"])
        L.append(("Helvetica-Bold", 7.5, fmt_row("%d%s" % (y, " YTD" if y == 2026 else ""), d), xs, 16))
        L.append(("Helvetica", 7.5, "Prepared by grade control (B. Peck) and metallurgy (R. Ochoa); issued "
                                    "4 November 2026 with October 2026.", None, 12))
        pages.append(L)
    # summary page
    L = [("Helvetica-Bold", 11, "Kelvanna Lake Mine - reconciliation summary, January 2023 to October 2026", None, 18),
         ("Helvetica-Bold", 7.5, head1, xs, 11), ("Helvetica-Bold", 7.5, head2, xs, 12)]
    allrows = []
    for y in years:
        ry = r[[m.year == y for m in r["month"]]]
        allrows.append((str(y), ry))
    allrows.append(("Jan 2023-Oct 2026", r))
    for label, ry in allrows:
        tot = ry[["m_t", "g_t", "k_t", "m_oz", "g_oz", "k_oz"]].sum()
        d = dict(m_t=tot["m_t"], g_t=tot["g_t"], k_t=tot["k_t"], m_oz=tot["m_oz"], g_oz=tot["g_oz"], k_oz=tot["k_oz"])
        d["m_g"], d["g_g"], d["k_g"] = (d["m_oz"] * P.TROY / d["m_t"], d["g_oz"] * P.TROY / d["g_t"],
                                        d["k_oz"] * P.TROY / d["k_t"])
        L.append(("Helvetica-Bold" if label.startswith("Jan") else "Helvetica", 7.5, fmt_row(label, d), xs, 12))
    pages.append(L)
    write_pdf(path, "Monthly reconciliation Jan 2023 - Oct 2026", "Brent Peck", pages, STAMP_RECON)


def slope_review(path):
    L = [("Helvetica-Bold", 12, "Kelvanna Lake - Phase 5 and 6 pit slope review", None, 18),
         ("Helvetica", 9, "Geotechnical engineering, 15 September 2026 (for mine planning)", None, 18)]
    _para(L, "Scope. Review of the Phase 5 east wall and Phase 6 west wall designs below the 1220 bench against the "
             "2026 core logging, the televiewer surveys of holes KL25-301 to KL25-309 and the prism monitoring to "
             "August 2026.")
    _para(L, "Findings. The footwall mafic volcanics carry a persistent foliation dipping 62 to 68 degrees into the pit "
             "on the east wall. Planar sliding on foliation controls the bench face angle there; the west wall in "
             "felsic volcanics is controlled by two joint sets and is not foliation-limited.")
    rows = [("Sector", "Bench face", "Berm (m)", "Inter-ramp", "Overall", "FoS (min)"),
            ("P5 east, above 1220", "65", "8.5", "47", "43", "1.31"),
            ("P5 east, below 1220", "60", "9.0", "44", "41", "1.28"),
            ("P6 west, above 1200", "70", "8.0", "51", "46", "1.42"),
            ("P6 west, below 1200", "70", "8.5", "50", "45", "1.37")]
    for i, r in enumerate(rows):
        L.append(("Helvetica-Bold" if i == 0 else "Helvetica", 9, list(r), [52, 200, 270, 330, 400, 460], 14))
    L.append(("Helvetica", 4, "", None, 8))
    _para(L, "Recommendation. Adopt the reduced east-wall face angle below the 1220 bench in the 2027 mine plan and "
             "continue weekly prism reads on the 1240 and 1225 berms. No change to the haul road alignment.")
    write_pdf(path, "Phase 5 and 6 pit slope review", "Geotechnical engineering", [L], STAMP_GEOT)


def price_deck(path):
    L = [("Helvetica-Bold", 12, "Aubreth Gold Corporation - 2027 budget price and FX deck", None, 18),
         ("Helvetica", 9, "Corporate finance, 21 October 2026. For all sites' 2027 budgets.", None, 18)]
    rows = [("Assumption", "2027 budget", "Long term"),
            ("Gold (USD/oz)", "2,900", "2,450"), ("Silver (USD/oz)", "32.00", "27.50"),
            ("CAD per USD", "1.36", "1.33"), ("Diesel, Ontario sites (CAD/L)", "1.42", "1.38"),
            ("Grid power, Kelvanna Lake (CAD/kWh)", "0.121", "0.116"), ("Sodium cyanide (CAD/t)", "4,180", "3,950"),
            ("Ontario royalty and mining tax", "per statute", "per statute")]
    for i, r in enumerate(rows):
        L.append(("Helvetica-Bold" if i == 0 else "Helvetica", 9.5, list(r), [52, 300, 400], 15))
    L.append(("Helvetica", 4, "", None, 8))
    _para(L, "Sites use the budget column for 2027 revenue and costs and the long-term column for reserve cut-offs and "
             "life-of-mine plans. Hedging is a corporate matter and is not allocated to sites.")
    write_pdf(path, "2027 budget price and FX deck", "Corporate finance", [L], STAMP_PRICE)
