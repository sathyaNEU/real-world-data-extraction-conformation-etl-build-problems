"""The golden deliverables: the Order's schedule workbook (each boiler's 2026 sulphur dioxide leaving the stack on the
limestone its scrubber consumed, and each site's boiler ash taken off site) and the bar chart against the 250 tonne
line; returns every figure the write-up states."""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402
import openpyxl  # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill  # noqa: E402

import golden as G  # noqa: E402
import pack as PK  # noqa: E402
import world as W  # noqa: E402

BOLD = Font(bold=True)
HEAD_FILL = PatternFill("solid", fgColor="DCE6F1")
TOTAL_FILL = PatternFill("solid", fgColor="F2F2F2")
LIST_FILL = PatternFill("solid", fgColor="FBE3D6")
WORDS = {4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight"}


def ten(x):
    return int(math.floor(x / 10.0 + 0.5) * 10)


def hundred(x):
    return int(math.floor(x / 100.0 + 0.5) * 100)


def whole(x):
    return int(math.floor(x + 0.5))


def r1(x):
    return math.floor(x * 10 + 0.5) / 10.0


def r2(x):
    return math.floor(x * 100 + 0.5) / 100.0


def name(w, bid):
    site = bid.split("-")[0]
    firm = w.sites[site]["firm"]
    if site in PK.UNIT_NAME:
        lab = PK.unit_label(bid)
        return "%s %s" % (firm, lab[0].lower() + lab[1:]) if lab.startswith("Boiler") else "%s %s" % (firm, lab)
    return firm


def listing(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def _head(ws, row):
    for c in ws[row]:
        c.font = BOLD
        c.fill = HEAD_FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")


def schedule(tr):
    """per boiler, in the register's order: coal burned, the site's sulphur, sulphur dioxide formed less the ash's
    share, limestone and calcium carbonate consumed, sulphur dioxide removed and leaving the stack"""
    w, rt = tr["w"], tr["rt"]
    cb = G.coal_burned(w.returns)
    S = G.site_sulphur(w.lots)
    per = {p["boiler"]: p for p in w.permits}
    rows = []
    for bid in sorted(rt, key=lambda b: PK.PERMIT[b]):
        r = rt[bid]
        formed = r["s_gas"] * G.M
        removed = r["caco3"] / W.MCACO3 / per[bid]["ratio"] * W.MSO2
        rows.append(dict(id=bid, permit=PK.PERMIT[bid], site=w.sites[bid.split("-")[0]]["firm"],
                         unit=PK.unit_label(bid), name=name(w, bid), coal=cb[bid], s=S[bid.split("-")[0]],
                         formed=formed, limestone=r["cons"], caco3=r["caco3"], removed=removed, so2=r["golden"],
                         listed=r["golden"] >= W.LINE, tested=r["tested"]))
        assert abs(formed - removed - r["golden"]) < 1e-6
    return rows


def write(path, tr):
    w = tr["w"]
    rows = schedule(tr)
    listed = [r["name"] for r in rows if r["listed"]]
    unlisted = [r["name"] for r in rows if not r["listed"]]
    tested_listed = [r["name"] for r in rows if r["tested"] >= W.LINE]
    ash = tr["ash"]
    tot = dict(formed=sum(r["formed"] for r in rows), removed=sum(r["removed"] for r in rows),
               so2=sum(r["so2"] for r in rows), coal=sum(r["coal"] for r in rows),
               tested=sum(r["tested"] for r in rows))
    rt = tr["rt"]
    dz = [r for r in rows if rt[r["id"]]["design"] >= W.LINE and not r["listed"]]
    assert len(dz) == 1
    figs = dict(call=dict(listed=listed, not_listed=unlisted, n_listed=len(listed)), order=[r["name"] for r in rows],
                design=dict(name=dz[0]["name"], so2=ten(rt[dz[0]["id"]]["design"])),
                boilers={r["name"]: dict(so2=ten(r["so2"]), listed="listed" if r["listed"] else "not listed",
                                         tested=ten(r["tested"]), so2_unrounded=r1(r["so2"]),
                                         over_line_pct=r1(100 * (r["so2"] / W.LINE - 1)),
                                         ratio=r1(r["so2"] / r["tested"])) for r in rows},
                components=dict(formed=hundred(tot["formed"]), removed=hundred(tot["removed"]), coal=whole(tot["coal"]),
                                leaving_10=ten(tot["so2"])),
                default=dict(listed=tested_listed),
                ash={w.sites[s]["firm"]: dict(t=ten(v["t"]), rec=r1(v["rec_pct"])) for s, v in sorted(ash.items())},
                ash_order=[w.sites[s]["firm"] for s in sorted(ash)],
                constants=dict(line=int(W.LINE), mso2=W.MSO2, ms=W.MS, mcaco3=W.MCACO3,
                               ratios=sorted({r2(p["ratio"]) for p in w.permits}), sites=16, boilers=18,
                               contractors=3, ash_sites=len(ash), ask_figures=2 * len(ash),
                               guidance_section_sulphur="4.2"))

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Schedule"
    ws.append(["%s boilers reach the 250 tonne line in 2026: %s" % (WORDS[len(listed)], listing(listed))])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Sulphur dioxide leaving the stack, 1 January to 31 December 2026, compiled under the Directorate's "
               "guidance for the 2026 inventory year (AQD/INV/2026/03). Sulphur dioxide in tonnes to the nearest 10; "
               "the line is tested on the unrounded figure."])
    ws.append([])
    ws.append(["Permit No", "Site", "Unit", "Coal burned (t)", "Sulphur as received (%)",
               "SO2 formed, less the ash's share (t)", "Limestone consumed (t)", "CaCO3 consumed (t)",
               "Limestone ratio (mol CaCO3 per mol SO2 removed)", "SO2 removed (t)", "SO2 leaving the stack (t)",
               "Listed under the Order"])
    _head(ws, 4)
    for r in rows:
        ratio = next(p["ratio"] for p in w.permits if p["boiler"] == r["id"])
        ws.append([r["permit"], r["site"], r["unit"], whole(r["coal"]), r2(r["s"]), whole(r["formed"]),
                   whole(r["limestone"]), whole(r["caco3"]), ratio, whole(r["removed"]), ten(r["so2"]),
                   "Listed" if r["listed"] else "Not listed"])
        if r["listed"]:
            for c in ws[ws.max_row]:
                c.fill = LIST_FILL
    ws.append(["Northern Priority Area", None, None, whole(tot["coal"]), None, None,
               whole(sum(r["limestone"] for r in rows)), whole(sum(r["caco3"] for r in rows)), None, None,
               ten(tot["so2"]), "%d listed" % len(listed)])
    for c in ws[ws.max_row]:
        c.font = BOLD
        c.fill = TOTAL_FILL
    fmt = {"D": "#,##0", "E": "0.00", "F": "#,##0", "G": "#,##0", "H": "#,##0", "I": "0.00", "J": "#,##0",
           "K": "#,##0"}
    for col, f in fmt.items():
        for cell in ws[col][4:]:
            cell.number_format = f
    for col, wd in zip("ABCDEFGHIJKL", [13, 34, 13, 12, 11, 14, 12, 12, 15, 11, 12, 12]):
        ws.column_dimensions[col].width = wd
    ws.row_dimensions[4].height = 58
    ws.freeze_panes = "D5"
    ws.print_title_rows = "4:4"

    wa = wb.create_sheet("Ash 2026")
    wa.append(["Boiler ash taken off site in 2026 by the three ash contractors"])
    wa["A1"].font = Font(bold=True, size=12)
    wa.append(["Whinmoss Waste Haulage, Carnhope Skips and Pellrigg and Sons Haulage: bottom and fly ash collected from 1 "
               "January to 31 December 2026, at the collecting contractor's weighbridge weight. A Whinmoss invoice line "
               "whose reference is a Carnhope or Pellrigg job number bills that job, and the load is counted once, on the "
               "local contractor's record. Tonnes to the nearest 10; shares to one decimal."])
    wa.append([])
    wa.append(["Site", "Permit Nos", "Ash taken off site (t)", "Sent to recovery (%)"])
    _head(wa, 4)
    rec_t = 0.0
    all_t = 0.0
    for s, v in sorted(ash.items()):
        wa.append([w.sites[s]["firm"], PK.site_permits(s), ten(v["t"]), r1(v["rec_pct"])])
        rec_t += v["t"] * v["rec_pct"] / 100
        all_t += v["t"]
    wa.append(["Northern Priority Area", None, ten(all_t), r1(100 * rec_t / all_t)])
    for c in wa[wa.max_row]:
        c.font = BOLD
        c.fill = TOTAL_FILL
    for cell in wa["C"][4:]:
        cell.number_format = "#,##0"
    for cell in wa["D"][4:]:
        cell.number_format = "0.0"
    for col, wd in zip("ABCD", [38, 28, 14, 14]):
        wa.column_dimensions[col].width = wd
    wa.row_dimensions[4].height = 30
    wa.freeze_panes = "A5"
    figs["ash_area"] = dict(t=ten(all_t), rec=r1(100 * rec_t / all_t))

    no = wb.create_sheet("Notes")
    notes = [
        "Sulphur dioxide leaving the stack (guidance section 3.1): the sulphur dioxide formed from the sulphur in the coal "
        "fired, less the sulphur the ash retains, less the sulphur dioxide the abatement plant removed over the year; "
        "sulphur to sulphur dioxide at 64.066 over 32.065 (section 3.2).",
        "Coal burned: the four quarterly returns (permit condition C7), quarters 1 and 2 on the 2019 template and 3 and "
        "4 on the 2026 template. Sulphur: each site's 2026 receipts as received, weighted by the tonnes delivered, a "
        "delivery dated by its receipt (section 4.2); both Quarholt and both Nethstead boilers take their site's "
        "figure (section 4.3).",
        "Sulphur dioxide removed: the calcium carbonate each scrubber consumed over 2026 at its guarantee schedule's "
        "operating stoichiometry, in moles of calcium carbonate (100.087 g a mole) per mole of sulphur dioxide removed "
        "(64.066 g a mole). Limestone consumed is the scrubber's 2026 quarry tickets less the change in its silo from "
        "the first quarter's opening stock to the fourth quarter's closing stock; each ticket's calcium carbonate is "
        "its ISO week's certificate, as delivered.",
        "The 2026 performance tests measure each scrubber's removal on the day of its test. The limestone each scrubber "
        "consumed covers the year, so the year's removal is taken from it.",
        "Listed: 250 tonnes or more on the unrounded figure (the Order's note, section 2).",
        "Ash: the three contractors' 2026 records conformed to the sites through the Directorate's customer "
        "cross-reference; Carnhope Skips' net weights converted from kilograms; general waste, scrap metal and "
        "effluent screenings left out; recovery is ash taken to Yarrdale Blocks or Velthwaite Cement Works.",
        "Prepared by the Industrial Emissions team, Air Quality Directorate, for the schedule to the Minister.",
    ]
    for t_ in notes:
        no.append([t_])
        no.cell(no.max_row, 1).alignment = Alignment(wrap_text=True, vertical="top")
    no.column_dimensions["A"].width = 112
    wb.save(path("workbook"))

    chart(path("chart"), rows, listed)
    return figs


def chart(path, rows, listed):
    """each boiler's 2026 sulphur dioxide leaving the stack against the 250 tonne line, highest first"""
    hot, grey, ink, ink2, line = "#b5462b", "#a9a7a1", "#0b0b0b", "#52514e", "#b9b8b3"
    rs = sorted(rows, key=lambda r: r["so2"])
    y = list(range(len(rs)))
    vals = [r["so2"] for r in rs]
    fig, ax = plt.subplots(figsize=(8.8, 6.0), dpi=150)
    ax.barh(y, vals, height=0.62, color=[hot if r["listed"] else grey for r in rs], zorder=2)
    ax.axvline(W.LINE, color=ink, linewidth=1.1, zorder=4)
    ax.text(W.LINE + 4, len(rs) - 0.35, "250 t: the Order's line", fontsize=7.8, color=ink, va="bottom")
    for yi, r in zip(y, rs):
        ax.text(r["so2"] + 4, yi, "{:,}".format(ten(r["so2"])), va="center", ha="left", fontsize=7.6,
                color=ink if r["listed"] else ink2, fontweight="bold" if r["listed"] else "normal")
    ax.set_yticks(y)
    ax.set_yticklabels([r["name"] for r in rs], fontsize=8.2, color=ink)
    ax.set_ylim(-0.7, len(rs) + 0.4)
    ax.set_xlim(0, max(vals) * 1.12)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: "{:,.0f}".format(v)))
    ax.set_xlabel("Sulphur dioxide leaving the stack, 2026 (tonnes)", fontsize=8.6, color=ink2)
    ax.tick_params(axis="x", labelsize=8, colors=ink2)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#e4e3df", linewidth=0.8, zorder=0)
    for s_ in ("top", "right", "left"):
        ax.spines[s_].set_visible(False)
    ax.spines["bottom"].set_color(line)
    import matplotlib.patches as mpatches
    handles = [mpatches.Patch(color=hot, label="Listed: 250 t or more"), mpatches.Patch(color=grey, label="Not listed")]
    ax.legend(handles=handles, loc="lower right", frameon=False, fontsize=7.6, handlelength=1.3)
    fig.suptitle("%s of the 18 coal boilers reach the 250 tonne line on the limestone their scrubbers consumed" %
                 WORDS[len(listed)], x=0.012, y=0.975, ha="left", fontsize=10.2, color=ink)
    fig.text(0.012, 0.012, "Air Quality Directorate, Industrial Emissions. Sulphur dioxide leaving the stack, 1 January "
             "to 31 December 2026, under the 2026 inventory guidance; tonnes to the nearest 10.", fontsize=6.6,
             color=ink2)
    fig.subplots_adjust(left=0.33, right=0.97, top=0.91, bottom=0.11)
    fig.savefig(path, facecolor="white", metadata={"Software": None, "Title": "Boiler sulphur dioxide 2026",
                                                   "Author": "Air Quality Directorate"})
    plt.close(fig)
