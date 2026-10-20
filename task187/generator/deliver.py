"""The goldens: the board paper (le_repair_campaign_2027.pdf: the call, the energy the repair recovers, why the other
candidates are not the campaign, and the chart of each turbine's energy lost to downtime and to grid curtailment) and
the lost production workbook (lost_production_2025_26.xlsx), both written from figures.json, which is computed from
the shipped files read back."""
import io
import os

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt   # noqa: E402

import analysis as AN      # noqa: E402
import docs as D           # noqa: E402
import world as W          # noqa: E402

PAPER = "le_repair_campaign_2027.pdf"
WORKBOOK = "metered_generation_2025_26.xlsx"
DOWN_C, CURT_C = "#2a6f97", "#e0a23b"
INK, INK2, GRID, BG = "#1d2a24", "#56606a", "#e3e6e4", "#ffffff"


def nearest(x, step):
    return int(np.floor(x / step + 0.5) * step)


def whole(x):
    """A whole number as a table prints it, never a negative zero."""
    n = int(np.floor(x + 0.5))
    return "%d" % n


def figures(target):
    """Every figure the write-up and the goldens state, from the files under target/."""
    B = AN.read_bundle(target)
    AN.set_curve(B["curve"])
    F = AN.frame_bundle(B)
    r0 = AN.default_shortfall(F)
    r0y = AN.default_shortfall(F, whole_year=True)
    am, (cp, vci) = AN.matched_annex_m(F)
    tb = AN.matched_bins(F, dv=0.5, dti=0.02, ref="median", minn=10)
    call = AN.pick(am)
    Ag, Bg = AN.asks_bundle(B, "golden")
    energy = {t: float(F[t]["p"][F[t]["normal"] & AN.blade_set_mask(F[t]["k"], t)].sum() / 6000.0) for t in W.TURBINES}
    region2 = {t: AN.default_shortfall(F, lo=3.0, hi=10.0)[t] for t in W.TURBINES}
    low = AN.default_shortfall(F, lo=4.0, hi=8.0)
    # CH07's turbulence in the plantation's sector against the other turbines' at the same winds (8 to 12 m/s)
    x = F["CH07"]
    sec = (x["ndir"] > 200) & (x["ndir"] < 305) & (x["veff"] >= 8) & (x["veff"] < 12) & x["normal"]
    others = np.concatenate([F[t]["ti"][(F[t]["veff"] >= 8) & (F[t]["veff"] < 12) & F[t]["normal"]]
                             for t in W.TURBINES if t not in ("CH07", "CH05", "CH01")])
    ti_ratio = float(np.median(x["ti"][sec]) / np.median(others))
    am_year = AN.matched_annex_m(F, whole_year=True)[0]

    fig = {
        "call": call,
        "recovered_mwh": round(am[call], 1),
        "recovered_mwh_nearest_50": nearest(am[call], 50),
        "recovered_share_of_energy_pct": round(100 * am[call] / energy[call], 1),
        "recovered_mwh_turbulence_bins": round(tb[call], 1),
        "zero_turbulence_curve": {"cp": round(cp, 3), "cut_in_ms": vci},
        "runner_up": sorted(am, key=lambda t: -am[t])[1],
        "matched_mwh": {t: round(am[t], 1) for t in W.TURBINES},
        "shortfall_vs_warranted_mwh": {t: round(r0[t], 1) for t in W.TURBINES},
        "shortfall_vs_warranted_whole_year_ch09_mwh": round(r0y["CH09"], 1),
        "partial_load_3_to_10_mwh": {t: round(region2[t], 1) for t in W.TURBINES},
        "partial_load_4_to_8_mwh": {t: round(low[t], 1) for t in W.TURBINES},
        "ch07_turbulence_ratio": round(ti_ratio, 2),
        "ch09_whole_year_blade_loss_mwh": round(am_year["CH09"], 1),
        "default_lead_ratio": round(sorted(r0.values())[-1] / sorted(r0.values())[-2], 2),
        "default_pick": AN.pick(r0),
        "metered_generation_mwh": {t: int(round(Ag[t])) for t in W.TURBINES},
        "metered_generation_mwh_exact": {t: round(Ag[t], 2) for t in W.TURBINES},
        "metered_export_mwh": {k: int(round(Bg[k])) for k in AN.ASK_MONTHS},
        "metered_export_mwh_exact": {k: round(Bg[k], 2) for k in AN.ASK_MONTHS},
        "farm_metered_generation_mwh": int(round(sum(Ag.values()))),
        "farm_metered_export_mwh": int(round(sum(Bg.values()))),
        "normal_energy_mwh": {t: round(energy[t], 1) for t in W.TURBINES},
        "ch09_rotor_back": W.CH09_BACK.astimezone(W.LONDON).strftime("%d %B %Y"),
        "standard_clauses": [num for _, items in D.STANDARD_CLAUSES for num, _ in items],
        "parameters": {"rounding_step_mwh": 50, "standard_density_kg_m3": 1.225, "rated_kw": 2300,
                       "power_performance_standard": "IEC 61400-12-1", "state_codes_downtime": [30, 40, 41],
                       "ask_window_local": ["2025-10-01", "2026-09-01"],
                       "state_codes_normal": [10, 20], "bands_ms": [3, 4, 8, 8.5, 9.5, 10, 12],
                       "rotor_diameters_ch02_to_ch04": 3.5},
    }
    return fig


# ------------------------------------------------------------------------------------------------- the chart
def chart_png(fig):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.6, "axes.edgecolor": INK2,
                         "axes.labelcolor": INK2, "xtick.color": INK, "ytick.color": INK2})
    f, ax = plt.subplots(figsize=(7.0, 3.6), dpi=170)
    f.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    xs = np.arange(len(W.TURBINES))
    gen = [fig["metered_generation_mwh"][t] for t in W.TURBINES]
    ax.bar(xs, gen, width=0.62, color=DOWN_C, label="Metered generation", zorder=3, linewidth=0)
    for x, a in zip(xs, gen):
        ax.text(x, a + 55, "{:,}".format(a), ha="center", va="bottom", fontsize=7.4, color=INK)
    ax.set_xticks(xs)
    ax.set_xticklabels(W.TURBINES)
    ax.set_ylabel("Metered generation, MWh")
    ax.set_ylim(0, max(gen) * 1.13)
    ax.yaxis.grid(True, color=GRID, linewidth=0.7, zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="both", length=0)
    ax.set_title("Metered generation by turbine, ten months to 31 August 2026", loc="left", fontsize=9.6,
                 fontweight="bold", color=INK, pad=10)
    f.tight_layout()
    buf = io.BytesIO()
    f.savefig(buf, format="png", facecolor=BG, metadata={"Software": None})
    plt.close(f)
    return buf.getvalue()


# ------------------------------------------------------------------------------------------------- the paper
def write_paper(path, fig, png):
    from reportlab.lib.units import mm
    from reportlab.platypus import Image, KeepTogether, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import ParagraphStyle
    am, r0 = fig["matched_mwh"], fig["shortfall_vs_warranted_mwh"]
    call, ru = fig["call"], fig["runner_up"]
    body = ParagraphStyle("pb", parent=D.BODY, fontSize=9.8, leading=13.8)
    small = ParagraphStyle("ps", parent=D.META, fontSize=7.8, leading=10.2)
    who, role = W.PEOPLE["asset_manager"]
    doc = D._doc(path, "2027 leading-edge campaign", who)
    s = [Paragraph(W.SOCIETY.upper() + " · BOARD PAPER B-26-11-04", D.META),
         Paragraph("Book the 2027 leading-edge campaign on %s: its blades cost about %d MWh last year, and the "
                   "repair should recover %d MWh to the nearest 50 MWh" % (call, round(fig["recovered_mwh"]),
                                                                          fig["recovered_mwh_nearest_50"]), D.H1),
         Paragraph("To the Board, meeting of 12 November 2026. From %s, %s. 14 October 2026. For decision." % (who, role),
                   D.META)]
    s.append(Paragraph("Recommendation", D.H2))
    s.append(Paragraph(
        "Book the summer 2027 rope-access campaign with %s on %s. Measured as OM-07 clause 2.4 asks, against the same turbine "
        "in the same winds with its blades as new, %s's blades cost %.0f MWh over its normal operation in the twelve "
        "months to September 2026, %.1f per cent of what it produced. The repair should recover about that over the "
        "twelve months after the work: %d MWh to the nearest 50 MWh. The next largest loss at the same comparison is "
        "%s's, %.0f MWh, which makes %s the candidate for 2028." % (
            W.ROPE, call, call, fig["recovered_mwh"], fig["recovered_share_of_energy_pct"],
            fig["recovered_mwh_nearest_50"], ru, am[ru], ru), body))
    s.append(Paragraph("Why not the turbine with the largest shortfall", D.H2))
    s.append(Paragraph(
        "Against the warranted power curve at the same mean wind, CH07 falls %.0f MWh short, more than twice any other "
        "turbine, and CH01 and CH05 follow. None of that is blade loss. A ten-minute power is the power curve averaged "
        "over the gusts inside the ten minutes; the three turbines facing the plantation run in its eddies (CH07 at "
        "%.1f times the turbulence of the turbines in open air, at 8 to 12 m/s in south-westerly and westerly winds), "
        "so near rated power the gusts swing them "
        "below the curve's knee and they make less, while between 4 and 8.5 m/s the same gusts lift them above the "
        "warranted curve, which no blade does. Compared with an as-new turbine at each ten-minute record's own "
        "turbulence (the turbulence normalisation of IEC 61400-12-1 Annex M, from each nacelle anemometer's standard "
        "deviation), CH07, CH05 and CH01 lose less than 1 MWh each: their blades are sound, and a repair would "
        "recover nothing." % (r0["CH07"], fig["ch07_turbulence_ratio"]), body))
    s.append(Paragraph("Why not CH02, and why %s's loss was hidden" % call, D.H2))
    s.append(Paragraph(
        "Below rated, where erosion is usually looked for, CH02 shows the largest deficit (%.0f MWh between 3 and 10 "
        "m/s against %.0f for %s). Part of it is real: CH02's blades lose %.0f MWh at the same comparison. The rest is "
        "the loch: CH02 has the smoothest air on the site in westerly winds, and in smooth air a ten-minute power at "
        "low wind sits below a curve measured in ordinary turbulence. %s stands three and a half rotor diameters "
        "downwind of CH02 in westerly winds, and the wake's turbulence lifts its low-wind power by about as much as "
        "its blades lose there (its shortfall between 4 and 8 m/s is %.1f MWh); its loss shows near rated and at its "
        "own turbulence." % (fig["partial_load_3_to_10_mwh"]["CH02"], fig["partial_load_3_to_10_mwh"][call], call,
                             am["CH02"], call, fig["partial_load_4_to_8_mwh"][call]), body))
    s.append(Paragraph(
        "CH09's blades cost %.0f MWh over the whole year, but those were the blades of the rotor lowered for the "
        "main-bearing exchange in April; under OM-07 clause 2.5 it is measured on the pool rotor in service since "
        "%s, whose blades are sound." % (fig["ch09_whole_year_blade_loss_mwh"], fig["ch09_rotor_back"]), body))
    rows = [[Paragraph(x, D.CELLB) for x in ("Turbine", "Shortfall against the warranted curve at the same mean wind "
                                                        "(MWh)", "Blade loss at the same turbulence (MWh)",
                                             "Metered generation, ten months to 31 August (MWh)")]]
    for t in W.TURBINES:
        rows.append([Paragraph(("<b>%s</b>" % t) if t == call else t, D.CELL)] +
                    [Paragraph(whole(v), D.CELLR) for v in (r0[t], am[t])] +
                    [Paragraph("{:,}".format(fig["metered_generation_mwh"][t]), D.CELLR)])
    rows.append([Paragraph("<b>Farm</b>", D.CELL), Paragraph("", D.CELL), Paragraph("", D.CELL),
                 Paragraph("<b>{:,}</b>".format(fig["farm_metered_generation_mwh"]), D.CELLR)])
    tab = Table(rows, colWidths=[20 * mm, 44 * mm, 40 * mm, 50 * mm], hAlign="LEFT", repeatRows=1)
    tab.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.7, D.INK), ("LINEABOVE", (0, -1), (-1, -1), 0.5, D.GREY),
                             ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2.2),
                             ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2)]))
    s += [Spacer(1, 4), KeepTogether([tab, Paragraph(
        "Normal operation (states 10 and 20), October 2025 to September 2026; CH09 from %s. Sources: SCADA, met mast M1, "
        "the monthly round's counter reads, work orders, Schedule 3." % fig["ch09_rotor_back"], small)])]
    s.append(Paragraph("What the meters recorded, 2025-26", D.H2))
    s.append(Paragraph(
        "The ten turbines generated %s MWh over the ten months to 31 August 2026 as their own revenue counters "
        "record it, and the connection meter exported %s MWh over the same months. The counters are read on the "
        "monthly round rather than at the month end, so each turbine's figure is taken to the window's own ends from "
        "the ten-minute record. The workbook %s gives each turbine's generation and the export month by month." % (
            "{:,}".format(fig["farm_metered_generation_mwh"]), "{:,}".format(fig["farm_metered_export_mwh"]),
            WORKBOOK), body))
    s.append(Image(io.BytesIO(png), width=165 * mm, height=165 * mm * 3.6 / 7.0))
    s.append(Paragraph("Notes", D.H2))
    for n in (
        "1. Blade loss is the as-new power at each normal-operation record's own wind and turbulence less the power "
        "made, summed over the twelve months. The as-new curve is the zero-turbulence curve that reproduces Schedule 3 "
        "at the mast's turbulence (power coefficient %.3f, cut-in %.1f m/s, rated 2,300 kW), averaged over each "
        "record's turbulence. Comparing each turbine with the fleet in the same 0.5 m/s and turbulence bins gives "
        "%.0f MWh for %s." % (fig["zero_turbulence_curve"]["cp"], fig["zero_turbulence_curve"]["cut_in_ms"],
                              fig["recovered_mwh_turbulence_bins"], call),
        "2. Wind speeds are corrected to 1.225 kg/m3 with the mast's temperature and pressure. The SCADA export joins "
        "the site server's archive, stamped in UK local time, to the hosted platform's export, stamped in UTC from 3 "
        "February 2026; it is aligned to the mast and the ANM log on that basis.",
        "3. Downtime includes the hours a turbine's controller was isolated for its annual service or a repair, which "
        "the SCADA does not record; the work orders give them. The site communications outage of 18 and 19 November "
        "2025 (turbines running, counters recording) and the grid loss of 24 January 2026 are neither downtime nor "
        "curtailment.",
            ):
        s.append(Paragraph(n, small))
    foot = W.SOCIETY + " | Board paper B-26-11-04 | 2027 leading-edge campaign"
    doc.build(s, onFirstPage=D._frame(W.FARM, "Board, 12 November 2026", foot),
              onLaterPages=D._frame(W.FARM, "Board, 12 November 2026", foot))


# ------------------------------------------------------------------------------------------------- the workbook
def write_workbook(path, fig):
    import openpyxl
    from openpyxl.styles import Alignment, Font
    bold = Font(bold=True)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Metered generation"
    ws.append(["Turbine", "Metered generation (MWh)"])
    for c in ws[1]:
        c.font = bold
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for t in W.TURBINES:
        ws.append([t, fig["metered_generation_mwh"][t]])
    n = len(W.TURBINES) + 1
    ws.append(["Farm", "=SUM(B2:B%d)" % n])
    for c in ws[n + 1]:
        c.font = bold
    for row in ws.iter_rows(min_row=2, min_col=2, max_col=2):
        for c in row:
            c.number_format = "#,##0"
    for col, wd in zip("AB", (10, 24)):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A2"
    ex = wb.create_sheet("Metered export")
    ex.append(["Month", "Metered export (MWh)"])
    for c in ex[1]:
        c.font = bold
        c.alignment = Alignment(wrap_text=True, vertical="top")
    import analysis as _AN
    for k in _AN.ASK_MONTHS:
        ex.append([k, fig["metered_export_mwh"][k]])
    m = len(_AN.ASK_MONTHS) + 1
    ex.append(["Ten months", "=SUM(B2:B%d)" % m])
    for c in ex[m + 1]:
        c.font = bold
    for row in ex.iter_rows(min_row=2, min_col=2, max_col=2):
        for c in row:
            c.number_format = "#,##0"
    for col, wd in zip("AB", (14, 24)):
        ex.column_dimensions[col].width = wd
    ex.freeze_panes = "A2"
    c2 = wb.create_sheet("Campaign 2027")
    c2.append(["Turbine", "Shortfall against warranted curve, same mean wind (MWh)",
               "Blade loss at the same turbulence (MWh)", "Normal-operation energy (MWh)"])
    for c in c2[1]:
        c.font = bold
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for t in W.TURBINES:
        c2.append([t, round(fig["shortfall_vs_warranted_mwh"][t]), round(fig["matched_mwh"][t]),
                   round(fig["normal_energy_mwh"][t])])
    c2.append([])
    c2.append(["Campaign: %s; energy recovered over the twelve months after the work %d MWh (to the nearest 50 MWh)." % (
        fig["call"], fig["recovered_mwh_nearest_50"])])
    for col, wd in zip("ABCD", (10, 30, 26, 22)):
        c2.column_dimensions[col].width = wd
    c2.freeze_panes = "A2"
    nt = wb.create_sheet("Notes")
    for line in (
            "Twelve months October 2025 to September 2026 (UK local months). Lost production by OM-07 revision 3, "
            "section 4: the warranted power at the met mast's density-corrected 80 m wind, less the turbine's power, "
            "never negative, by ten-minute interval.",
            "Downtime: faults, repairs and planned service, including the hours a controller was isolated for service or "
            "repair (from the work orders; the SCADA has no rows for them). Grid curtailment: intervals with an ANM "
            "instruction in force, other than downtime and stops for ice, high wind or grid loss.",
            "SCADA timestamps: UK local time to 3 February 2026 (site server), UTC after (hosted platform).",
            "Figures rounded to the nearest MWh from unrounded interval sums; the farm total is the sum of the "
            "rounded turbine figures.",
            "Prepared by %s, %s, 14 October 2026." % W.PEOPLE["asset_manager"]):
        nt.append([line])
    nt.column_dimensions["A"].width = 120
    for row in nt.iter_rows():
        row[0].alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)
