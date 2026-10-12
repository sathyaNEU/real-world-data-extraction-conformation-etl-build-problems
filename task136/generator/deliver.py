"""The golden deliverables: feeder_upgrade_2029.xlsx (the call, the forecast by feeder, the program estimate, the DER
Register check, battery storage) and yarrabin_pv_vs_hosting_2029.png, plus generator/figures.json, every figure
computed from the shipped pack (calc.py)."""
from __future__ import annotations

import datetime as dt
import json
import os

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import calc as C
import common as K
import postprocess as PP


def r1(x):
    return round(x + 1e-12, 1)


def ten(x):
    return int(round(x / 10.0) * 10)


def compute(target):
    L = C.load(target)
    base = C.base_forecast(L["reg"])
    camps = C.campaigns(L)
    pools = C.pools_2027(L)
    fc = C.forecast(L, base=base, camps=camps, pools=pools)
    rb = C.rates_by_basis(camps)
    default = C.forecast(L, basis="letterboxed", base=base, camps=camps, pools=pools)
    a, b = C.ask_a(L)
    storage = C.ask_b(L)
    return dict(L=L, base=base, camps=camps, pools=pools, fc=fc, rb=rb, default=default, ask_a=(a, b),
                ask_b=storage)


def figures(c):
    fc, pools, rb = c["fc"], c["pools"], c["rb"]
    w, ru = fc["winner"], fc["runner"]
    bdw, wtv = fc["lift"]["Bindarra Waters"], fc["lift"]["Wattleview"]
    a, b = c["ask_a"]
    out = {
        "call": {"feeder": w, "excess_mw": "%.1f" % r1(fc["excess"][w]), "runner_up": ru,
                 "runner_up_excess_mw": "%.1f" % r1(fc["excess"][ru]), "gap_mw": "%.1f" % r1(fc["gap"]),
                 "bindarra_waters_systems": ten(bdw), "wattleview_systems": ten(wtv)},
        "steps": {
            "connected_kw": {f: "{:,}".format(int(round(c["base"]["cap"].get(f, 0)))) for f in K.FEEDERS},
            "trend_kw": {f: "{:,}".format(int(round(c["base"]["trend"][f]))) for f in K.FEEDERS},
            "forecast_kw": {f: "{:,}".format(int(round(fc["fc"][f]))) for f in K.FEEDERS},
            "hosting_mw": {f: "%.2f" % c["L"]["hca"][f]["hc29"] for f in K.FEEDERS},
            "excess_mw": {f: "%.1f" % r1(fc["excess"][f]) for f in K.FEEDERS},
            "pooled_rate_pct": "%.2f" % (100 * rb["untapped"]["pooled"]),
            "campaigns": {x["key"]: {"untapped": "{:,}".format(x["untapped"]), "systems": x["systems"],
                                     "rate_pct": "%.2f" % (100 * x["systems"] / x["untapped"])} for x in c["camps"]},
            "bindarra_untapped_base": "{:,}".format(pools["Bindarra Waters"]["untapped_base"]),
            "bindarra_adopt_fy": pools["Bindarra Waters"]["adopt_fy"],
            "bindarra_untapped_open": "{:,}".format(pools["Bindarra Waters"]["untapped_open"]),
            "wattleview_untapped_base": "{:,}".format(pools["Wattleview"]["untapped_base"]),
            "wattleview_adopt_fy": pools["Wattleview"]["adopt_fy"],
            "wattleview_untapped_open": "{:,}".format(pools["Wattleview"]["untapped_open"]),
            "bindarra_systems_unrounded": "%.1f" % bdw, "wattleview_systems_unrounded": "%.1f" % wtv,
            "avg_kw_yrb24": "%.2f" % fc["avgkw"]["YRB24"], "avg_kw_yrb27": "%.2f" % fc["avgkw"]["YRB27"],
            "program_kw_yrb24": "{:,}".format(int(round(fc["add_kw"]["YRB24"]))),
            "program_kw_yrb27": "{:,}".format(int(round(fc["add_kw"]["YRB27"]))),
            "winner_forecast_mw": "%.1f" % r1(fc["fc"][w] / 1000.0),
            "winner_hosting_mw": "%.2f" % c["L"]["hca"][w]["hc29"],
        },
        "default_path": {"feeder": c["default"]["winner"], "excess_mw": "%.1f" % r1(c["default"]["excess"][c["default"]["winner"]]),
                         "bindarra_waters_systems": ten(c["default"]["lift"]["Bindarra Waters"]),
                         "wattleview_systems": ten(c["default"]["lift"]["Wattleview"])},
        "ask_a": {f: {"connected_not_on_der": a[f], "der_active_not_connected": b[f]} for f in K.FEEDERS},
        "ask_b": {f: "{:,}".format(ten(c["ask_b"][f])) for f in K.FEEDERS},
    }
    return out


HEAD = PatternFill("solid", fgColor="E4ECEF")
CALL = PatternFill("solid", fgColor="F3F0E6")


def _head(ws, row, values, widths=None):
    for j, v in enumerate(values, 1):
        c = ws.cell(row=row, column=j, value=v)
        c.font = Font(bold=True, size=10)
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[row].height = 44
    if widths:
        for j, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(j)].width = w


def write_book(path, c, figs):
    fc, pools, rb, L = c["fc"], c["pools"], c["rb"], c["L"]
    w, ru = fc["winner"], fc["runner"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Call"
    ws["A1"] = ("%s takes the FY2027-28 hosting-capacity augmentation: its rooftop PV sits furthest above hosting "
                "capacity at the 31 August 2029 design point" % w)
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Yarrabin 22 kV feeders, forecast under NPP-114 rev 3 from a base date of 31 August 2026."
    ws["A2"].font = Font(italic=True, size=9)
    rows = [
        ("Feeder to receive the augmentation", w, None),
        ("Rooftop PV above hosting capacity at 31 August 2029 (MW)", float(figs["call"]["excess_mw"]), "0.0"),
        ("Runner-up feeder", ru, None),
        ("Runner-up above hosting capacity (MW)", float(figs["call"]["runner_up_excess_mw"]), "0.0"),
        ("Gap between them (MW)", float(figs["call"]["gap_mw"]), "0.0"),
        ("Solar Streets 2027, Bindarra Waters: systems added", figs["call"]["bindarra_waters_systems"], "#,##0"),
        ("Solar Streets 2027, Wattleview: systems added", figs["call"]["wattleview_systems"], "#,##0"),
    ]
    for i, (k, v, fmt) in enumerate(rows, 4):
        ws.cell(row=i, column=1, value=k)
        cc = ws.cell(row=i, column=2, value=v)
        cc.fill = CALL
        cc.alignment = Alignment(horizontal="right")
        if fmt:
            cc.number_format = fmt
    ws.column_dimensions["A"].width = 58
    ws.column_dimensions["B"].width = 14
    notes = [
        "%s's forecast rooftop PV at 31 August 2029 is %s MW against a 2029 hosting capacity of %s MW; most of the "
        "difference is the Bindarra Waters bulk-buy." % (w, figs["steps"]["winner_forecast_mw"], figs["steps"]["winner_hosting_mw"]),
        "Each past Solar Streets campaign installed systems on %s to %s per cent of the owner-occupied houses in its "
        "suburb that had no PV when sign-ups opened (%s per cent over all seven); that is the rate carried to the "
        "2027 campaigns." % (min(v["rate_pct"] for v in figs["steps"]["campaigns"].values()),
                              max(v["rate_pct"] for v in figs["steps"]["campaigns"].values()),
                              figs["steps"]["pooled_rate_pct"]),
        "Systems per home letterboxed varied much more from one campaign to the next, because the suburbs differed "
        "in how many of their addresses were units, rented houses or houses that already had panels.",
    ]
    for i, t in enumerate(notes, 13):
        ws.cell(row=i, column=1, value=t).font = Font(size=9)
    ws.sheet_view.showGridLines = False

    f = wb.create_sheet("Forecast")
    f["A1"] = "Forecast rooftop PV (micro EG) at 31 August 2029 by feeder"
    f["A1"].font = Font(bold=True, size=11)
    _head(f, 3, ["Feeder", "Connected 31 Aug 2026 (kW)", "Trend (kW a year, FY2023-24 to FY2025-26)",
                 "Base forecast 31 Aug 2029 (kW)", "Solar Streets 2027 systems", "Program capacity (kW)",
                 "Forecast 31 Aug 2029 (kW)", "Hosting capacity, 2029 case (MW)",
                 "Above hosting capacity (MW)", "Rank"], [9, 13, 15, 14, 12, 12, 14, 13, 13, 7])
    camp_of = {p["feeder"]: (name, fc["lift"][name]) for name, p in pools.items()}
    for i, fd in enumerate(K.FEEDERS, 4):
        nm = camp_of.get(fd)
        vals = [fd, int(round(c["base"]["cap"].get(fd, 0))), int(round(c["base"]["trend"][fd])),
                int(round(c["base"]["base"][fd])), ten(nm[1]) if nm else None,
                int(round(fc["add_kw"].get(fd, 0))) if nm else None, int(round(fc["fc"][fd])),
                L["hca"][fd]["hc29"], r1(fc["excess"][fd]), fc["order"].index(fd) + 1]
        for j, v in enumerate(vals, 1):
            cc = f.cell(row=i, column=j, value=v)
            if j in (2, 3, 4, 6, 7):
                cc.number_format = "#,##0"
            elif j == 8:
                cc.number_format = "0.00"
            elif j == 9:
                cc.number_format = "0.0"
    tot = [("Yarrabin", None), (sum(c["base"]["cap"].get(fd, 0) for fd in K.FEEDERS), "#,##0"),
           (sum(c["base"]["trend"][fd] for fd in K.FEEDERS), "#,##0"), (sum(c["base"]["base"][fd] for fd in K.FEEDERS), "#,##0"),
           (sum(ten(v) for v in fc["lift"].values()), "#,##0"), (sum(fc["add_kw"].values()), "#,##0"),
           (sum(fc["fc"][fd] for fd in K.FEEDERS), "#,##0")]
    for j, (v, fmt) in enumerate(tot, 1):
        cc = f.cell(row=12, column=j, value=int(round(v)) if isinstance(v, float) else v)
        cc.font = Font(bold=True)
        if fmt:
            cc.number_format = fmt
    f["A14"] = ("Connected capacity: each NMI's latest connected configuration on the network model's feeder; trend: "
                "the yearly increase in connected capacity less program systems first connected that year; program "
                "systems at the feeder's FY2025-26 average inverter rating (NPP-114 3.2, 4.1, 4.2).")
    f["A14"].font = Font(size=9, italic=True)
    f.freeze_panes = "B4"
    f.page_setup.orientation = "landscape"
    f.page_setup.fitToWidth = 1
    f.sheet_properties.pageSetUpPr.fitToPage = True
    f.print_title_rows = "3:3"

    p = wb.create_sheet("Solar Streets")
    p["A1"] = "Solar Streets: systems per owner-occupied house without PV when sign-ups opened"
    p["A1"].font = Font(bold=True, size=11)
    _head(p, 3, ["Campaign", "Suburb", "Feeder", "Sign-ups opened", "Owner-occupied houses without PV at opening",
                 "Systems installed", "Systems per such house (%)"], [10, 18, 9, 13, 18, 12, 14])
    for i, x in enumerate(c["camps"], 4):
        vals = [x["key"], x["suburb"], x["feeder"], x["opening"], x["untapped"], x["systems"],
                round(100 * x["systems"] / x["untapped"], 2)]
        for j, v in enumerate(vals, 1):
            cc = p.cell(row=i, column=j, value=v)
            if j == 4:
                cc.number_format = "d mmm yyyy"
            elif j == 5:
                cc.number_format = "#,##0"
            elif j == 7:
                cc.number_format = "0.00"
    n = 4 + len(c["camps"])
    p.cell(row=n, column=1, value="All seven").font = Font(bold=True)
    p.cell(row=n, column=5, value=sum(x["untapped"] for x in c["camps"])).number_format = "#,##0"
    p.cell(row=n, column=6, value=sum(x["systems"] for x in c["camps"]))
    p.cell(row=n, column=7, value=round(100 * rb["untapped"]["pooled"], 2)).number_format = "0.00"
    _head(p, n + 2, ["2027 campaign", "Suburb", "Feeder", "Sign-ups open", "Owner-occupied houses without PV, 31 Aug 2026",
                     "Less first applications from such houses in FY2025-26", "Expected without PV at opening",
                     "Systems added", "Average inverter (kW, FY2025-26)", "Capacity added (kW)"])
    for i, (name, key) in enumerate((("Bindarra Waters", "BDW27"), ("Wattleview", "WTV27")), n + 3):
        pl = pools[name]
        vals = [key, name, pl["feeder"], dt.date(2027, 9, 6), pl["untapped_base"], pl["adopt_fy"], pl["untapped_open"],
                ten(fc["lift"][name]), round(fc["avgkw"][pl["feeder"]], 2), int(round(fc["add_kw"][pl["feeder"]]))]
        for j, v in enumerate(vals, 1):
            cc = p.cell(row=i, column=j, value=v)
            if j == 4:
                cc.number_format = "d mmm yyyy"
            elif j in (5, 7, 10):
                cc.number_format = "#,##0"
            elif j == 9:
                cc.number_format = "0.00"
    p.column_dimensions["H"].width = 11
    p.column_dimensions["I"].width = 13
    p.column_dimensions["J"].width = 12

    d = wb.create_sheet("DER Register check")
    d["A1"] = "Connected micro EG at 31 August 2026 against the DER Register extract of 5 September 2026"
    d["A1"].font = Font(bold=True, size=11)
    a, b = c["ask_a"]
    _head(d, 3, ["Feeder", "Connected systems not shown on the DER Register",
                 "Active DER Register sites with no connected system"], [9, 22, 22])
    for i, fd in enumerate(K.FEEDERS, 4):
        d.cell(row=i, column=1, value=fd)
        d.cell(row=i, column=2, value=a[fd])
        d.cell(row=i, column=3, value=b[fd])
    for j, v in enumerate(("Yarrabin", sum(a.values()), sum(b.values())), 1):
        d.cell(row=12, column=j, value=v).font = Font(bold=True)
    d["A14"] = ("Matched by NMI (ten characters); registrations lodged against a builder's temporary supply NMI are "
                "read at the permanent NMI from the re-allocation log.")
    d["A14"].font = Font(size=9, italic=True)
    d.freeze_panes = "B4"

    s = wb.create_sheet("Battery storage")
    s["A1"] = "Battery storage at active DER Register sites, 5 September 2026"
    s["A1"].font = Font(bold=True, size=11)
    _head(s, 3, ["Feeder", "Battery storage (kWh)"], [9, 16])
    for i, fd in enumerate(K.FEEDERS, 4):
        s.cell(row=i, column=1, value=fd)
        s.cell(row=i, column=2, value=ten(c["ask_b"][fd])).number_format = "#,##0"
    s.cell(row=12, column=1, value="Yarrabin").font = Font(bold=True)
    tc = s.cell(row=12, column=2, value=ten(sum(c["ask_b"].values())))
    tc.number_format = "#,##0"
    tc.font = Font(bold=True)
    s["A14"] = ("Each active AC connection's storage counted once (the extract repeats it on every battery module row); "
                "decommissioned connections excluded. Rounded to the nearest 10 kWh by feeder and in total.")
    s["A14"].font = Font(size=9, italic=True)

    n_ = wb.create_sheet("Notes")
    n_["A1"] = "Notes and sources"
    n_["A1"].font = Font(bold=True, size=11)
    lines = [
        ("Base date", "31 August 2026 (NPP-114 rev 3, clause 3.1); connection register extract of 1 September 2026 and "
                      "the network model at 31 August 2026."),
        ("Design point", "31 August 2029, the start of the spring minimum-demand season (clause 2.4)."),
        ("Rooftop PV", "Micro EG of 30 kVA or less at residential and business NMIs, at the inverter's AC rating; "
                       "systems migrated in 2019 take their inverters from the legacy equipment table."),
        ("Hosting capacity", "Buchanan Power Engineering report BPE-2026-031 (24 July 2026), spring 2029 "
                             "minimum-demand case (clause 5.1)."),
        ("Solar Streets 2027", "Merindah City Council letter of 14 August 2026 (reference SS/2027/01): sign-ups "
                               "6 September to 26 November 2027 in Bindarra Waters and Wattleview."),
        ("Past campaigns", "The council's Solar Streets summary, 2018 to 2024, for sign-up dates; systems counted from "
                           "program references in the connection register, which agree with the council's systems "
                           "installed for every campaign."),
        ("Owner-occupied house", "Rates roll land use code 02 (single unit dwelling) with rating category R1, matched "
                                 "to NMIs through the GIS cross-reference; without PV when no application at any of "
                                 "its NMIs, other than a withdrawn one, was received before the date."),
        ("DER Register", "Extract of 5 September 2026, AC connections and devices for NMIs on the Yarrabin feeders."),
        ("Rounding", "Carried unrounded and rounded once: MW to one decimal and systems to the nearest ten "
                     "(clause 7.1); battery storage to the nearest 10 kWh."),
    ]
    for i, (k, v) in enumerate(lines, 3):
        n_.cell(row=i, column=1, value=k).font = Font(bold=True, size=10)
        n_.cell(row=i, column=2, value=v).alignment = Alignment(wrap_text=True, vertical="top")
        n_.cell(row=i, column=1).alignment = Alignment(vertical="top")
        n_.row_dimensions[i].height = 30
    n_.column_dimensions["A"].width = 22
    n_.column_dimensions["B"].width = 110
    wb.save(path)
    PP.normalize_ooxml(path, K.PEOPLE["analyst"], K.PEOPLE["analyst"], "2026-10-13T00:12:44Z",
                       "2026-10-16T06:41:09Z", excel=True)


def write_chart(path, c, figs):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, Rectangle
    fc, L = c["fc"], c["L"]
    w = fc["winner"]
    surface, ink, ink2, muted, grid, base_c = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
    accent, ctx = "#2a78d6", "#c3c2b7"
    plt.rcParams.update({"font.family": "DejaVu Sans", "svg.hashsalt": "task136"})
    fig, ax = plt.subplots(figsize=(10, 5.8), dpi=150)
    fig.patch.set_facecolor(surface)
    ax.set_facecolor(surface)
    vals = [fc["fc"][f] / 1000.0 for f in K.FEEDERS]
    hcs = [L["hca"][f]["hc29"] for f in K.FEEDERS]
    width = 0.34
    for i, (f, v, h) in enumerate(zip(K.FEEDERS, vals, hcs)):
        col = accent if f == w else ctx
        rad = 0.05
        ax.add_patch(FancyBboxPatch((i - width / 2, -1.0), width, v + 1.0, boxstyle="round,pad=0,rounding_size=%.3f" % rad,
                                    mutation_aspect=4.0, linewidth=0, facecolor=col, zorder=2, clip_on=True))
        ax.plot([i - width / 2 - 0.08, i + width / 2 + 0.08], [h, h], color=ink, linewidth=2.0, solid_capstyle="butt",
                zorder=3)
    ax.set_xlim(-0.6, len(K.FEEDERS) - 0.4)
    top = max(vals) * 1.16
    ax.set_ylim(0, top)
    ax.set_yticks([y for y in range(0, int(top) + 1, 5)])
    ax.set_yticklabels(["%d" % y for y in range(0, int(top) + 1, 5)])
    ax.set_xticks(range(len(K.FEEDERS)))
    ax.set_xticklabels(K.FEEDERS, fontsize=10, color=ink2)
    ax.tick_params(axis="y", colors=muted, labelsize=9, length=0)
    ax.tick_params(axis="x", length=0, pad=6)
    ax.yaxis.grid(True, color=grid, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(base_c)
    ax.set_ylabel("MW", color=ink2, fontsize=10)
    for f in (w, fc["runner"]):
        i = K.FEEDERS.index(f)
        v = fc["fc"][f] / 1000.0
        ax.annotate(("%s MW above\nhosting capacity\nof %s MW" % (figs["call"]["excess_mw"], figs["steps"]["winner_hosting_mw"]))
                    if f == w else "%s MW above\nhosting capacity" % figs["call"]["runner_up_excess_mw"],
                    xy=(i, v), xytext=(0, 8), textcoords="offset points", ha="center", va="bottom", fontsize=9,
                    color=ink if f == w else ink2)
    fig.text(0.075, 0.955, "%s sits furthest above its hosting capacity at the 31 August 2029 design point" % w,
             fontsize=13, color=ink, weight="bold", ha="left")
    fig.text(0.075, 0.915, "Forecast rooftop PV connected at 31 August 2029 (bars) and each feeder's 2029 hosting "
             "capacity (black marks), Yarrabin 22 kV feeders", fontsize=9.5, color=ink2, ha="left")
    from matplotlib.lines import Line2D
    handles = [Rectangle((0, 0), 1, 1, facecolor=accent), Rectangle((0, 0), 1, 1, facecolor=ctx),
               Line2D([0], [0], color=ink, linewidth=2)]
    ax.legend(handles, ["%s forecast PV" % w, "Other feeders' forecast PV", "Hosting capacity, 2029 case"],
              loc="upper right", frameon=False, fontsize=9, labelcolor=ink2, ncol=3, bbox_to_anchor=(1.0, 1.06))
    fig.text(0.075, 0.025, "Source: Mirrabee Energy connection register and network model at 31 August 2026; "
             "hosting capacity assessment BPE-2026-031; NPP-114 rev 3.", fontsize=7.5, color=muted, ha="left")
    fig.subplots_adjust(left=0.075, right=0.985, top=0.84, bottom=0.11)
    fig.savefig(path, facecolor=surface, metadata={"Software": None})
    plt.close(fig)


def main(target, golden, figures_path):
    os.makedirs(golden, exist_ok=True)
    c = compute(target)
    figs = figures(c)
    write_book(os.path.join(golden, K.GOLD_BOOK), c, figs)
    write_chart(os.path.join(golden, K.GOLD_CHART), c, figs)
    with open(figures_path, "w", encoding="utf-8") as fh:
        json.dump(figs, fh, indent=1, ensure_ascii=False, default=str)
        fh.write("\n")
    return c, figs
