"""task489: the golden deliverables and generator/figures.json, computed from the simulation's truth.
larchmere_source_inventory_2026.xlsx follows the pack's MRS-03 Annex B template; controller_conversion_2027.pptx
is the two-slide note for the conversion order."""
import json
import os

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.properties import PageSetupProperties

import sim as S
import world as W

HEAD = Font(name="Calibri", bold=True, size=11)
FILL = PatternFill("solid", fgColor="DDEBF7")
BASIS = {"F": "Separator liquid over level band", "FA": "SCADA dump count", "PB": "One dump per plunger arrival",
         "PS": "Plunger slugs filling the level band"}


def rnd(x, n=0):
    """Round half away from zero at the stated precision (the figures are asserted clear of every edge)."""
    q = 10 ** n
    return (int(abs(x) * q + 0.5) / q) * (1 if x >= 0 else -1)


def compute(wd):
    tr = S.truth(wd)
    bt = S.bleed_truth(wd)
    na = S.nonarrival_truth(wd)
    bma = S.bleed_by_maker_area(bt, wd)
    pad = {s["code"]: s for s in wd["sites"]}
    lc_rows = []
    for row in tr["lc"]:
        sep = row["sep"]
        grp = "FA" if sep["auto"] else sep["group"]
        cyc = row["dumps"]["golden"]
        gas_m3 = cyc * W.LC_MODELS[sep["model"]]["scf_per_cycle"] * W.SCF_TO_M3
        lc_rows.append({"pad": pad[sep["site"]]["name"], "code": sep["site"], "lsd": pad[sep["site"]]["lsd"],
                        "tag": sep["lc_tag"], "cls": "Intermittent vent",
                        "make": "%s %s" % (W.MAKERS[W.LC_MODELS[sep["model"]]["maker"]], sep["model"]),
                        "serial": sep["serial"], "basis": BASIS[grp], "activity": cyc, "unit": "dump cycles",
                        "gas_m3": gas_m3, "kg": row["kg"]["golden"], "group": sep["group"], "uwi": sep["uwi"]})
    bl_rows = []
    for b in bt:
        gas_m3 = b["rate"] * b["hours"] * W.SCF_TO_M3
        bl_rows.append({"pad": pad[b["site"]]["name"], "code": b["site"], "lsd": pad[b["site"]]["lsd"],
                        "tag": retag(b), "cls": "Continuous bleed",
                        "make": "%s %s" % (W.MAKERS[W.BLEED_MODELS[b["model"]]["maker"]], b["model"]),
                        "serial": b["serial"], "basis": "Survey measured bleed" if b["measured"] else "Maker's rated bleed",
                        "activity": b["hours"], "unit": "hours", "gas_m3": gas_m3, "kg": b["kg"]})
    pads = []
    for s in wd["sites"]:
        it = tr["site_t"][s["code"]]["golden"]
        ct = sum(r["kg"] for r in bl_rows if r["code"] == s["code"]) / 1000.0
        pads.append({"pad": s["name"], "code": s["code"], "lsd": s["lsd"], "int_t": it, "cont_t": ct,
                     "in": it > W.LINE_T})
    wells = []
    for sep in wd["seps"]:
        if sep["group"] == "F":
            continue
        w = next(x for x in wd["wells"] if x["uwi"] == sep["uwi"])
        wells.append({"uwi": sep["uwi"], "name": w["name"], "pad": pad[sep["site"]]["name"], "nonarr": na[sep["uwi"]]})
    bm = [{"maker": W.MAKERS[mk], "area": ar, "kg": v} for (mk, ar), v in sorted(bma.items())]
    return {"tr": tr, "lc": lc_rows, "bl": bl_rows, "pads": pads, "wells": wells, "bleed_ma": bm}


def retag(b):
    """The tag a continuous-bleed device carries in the register at the export (the re-piped pads' PCs renumbered)."""
    if b["site"] in {s for s, _ in W.RETAGGED} and b["tag"] in ("PC-1", "PC-2"):
        return "PC-2" if b["tag"] == "PC-1" else "PC-1"
    return b["tag"]


def _head(row, wrap=True):
    for c in row:
        c.font = HEAD
        c.fill = FILL
        c.alignment = Alignment(wrap_text=wrap, vertical="center")


def _total(ws, row):
    for c in ws[row]:
        c.font = Font(name="Calibri", bold=True, size=11)
        c.border = Border(top=Side(style="thin", color="7F7F7F"))


def write_inventory(path, g):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Annex B sources"
    ws.append(["MRS-03 Annex B: source-level methane inventory"])
    ws["A1"].font = Font(name="Calibri", bold=True, size=13)
    ws.append(["Operator", W.ORG])
    ws.append(["Reporting year", "2026 (production days 1 January to 31 December)"])
    ws.append(["Prepared by", "%s, %s" % (W.PEOPLE["lead"], W.TITLES["lead"])])
    ws.append([])
    ws.append(["Pad", "Surface location", "Source tag", "Source class", "Make and model", "Serial", "Activity basis",
               "Activity in the reporting year", "Activity unit", "Gas vented (m3)", "Methane (kg)"])
    _head(ws[6])
    ws.row_dimensions[6].height = 30
    rows = sorted(g["lc"] + g["bl"], key=lambda r: (r["pad"], 0 if r["cls"].startswith("Inter") else 1, r["tag"], r["serial"]))
    for r in rows:
        cycles = r["unit"] == "dump cycles"
        act = rnd(r["activity"], 0) if cycles else rnd(r["activity"], 1)
        ws.append([r["pad"], r["lsd"], r["tag"], r["cls"], r["make"], r["serial"], r["basis"], act, r["unit"],
                   rnd(r["gas_m3"], 1), int(rnd(r["kg"], 0))])
        n = ws.max_row
        ws.cell(n, 8).number_format = "#,##0" if cycles else "#,##0.0"
        ws.cell(n, 10).number_format = "#,##0.0"
        ws.cell(n, 11).number_format = "#,##0"
    last = ws.max_row
    ws.append(["Total, all sources", None, None, None, None, None, None, None, None,
               rnd(sum(r["gas_m3"] for r in rows), 1), int(rnd(sum(r["kg"] for r in rows), 0))])
    _total(ws, ws.max_row)
    ws.cell(ws.max_row, 10).number_format = "#,##0.0"
    ws.cell(ws.max_row, 11).number_format = "#,##0"
    for i, w in enumerate([16, 16, 11, 17, 33, 11, 33, 13, 12, 12, 11], 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "B7"
    ws.auto_filter.ref = "A6:K%d" % last
    ws.print_title_rows = "6:6"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)

    ws2 = wb.create_sheet("Annex B pads")
    ws2.append(["Pad", "Surface location", "Intermittent-vent controllers, methane (t)",
                "Continuous-bleed controllers, methane (t)", "2027 conversion"])
    _head(ws2[1])
    ws2.row_dimensions[1].height = 30
    for p in sorted(g["pads"], key=lambda p: p["pad"]):
        ws2.append([p["pad"], p["lsd"], rnd(p["int_t"], 2), rnd(p["cont_t"], 2), "Yes" if p["in"] else "No"])
    ws2.append(["All pads", None, rnd(sum(p["int_t"] for p in g["pads"]), 2), rnd(sum(p["cont_t"] for p in g["pads"]), 2),
                "%d pads" % sum(p["in"] for p in g["pads"])])
    _total(ws2, ws2.max_row)
    for row in ws2.iter_rows(min_row=2, min_col=3, max_col=4):
        for c in row:
            c.number_format = "0.00"
    for row in ws2.iter_rows(min_row=2, min_col=5, max_col=5):
        for c in row:
            c.alignment = Alignment(horizontal="center")
    for i, w in enumerate([16, 16, 20, 20, 12], 1):
        ws2.column_dimensions[get_column_letter(i)].width = w
    ws2.freeze_panes = "A2"

    ws3 = wb.create_sheet("Plunger lift wells")
    ws3.append(["UWI", "Well name", "Pad", "2026 cycles without plunger arrival"])
    _head(ws3[1])
    ws3.row_dimensions[1].height = 30
    for w in sorted(g["wells"], key=lambda w: (w["pad"], w["name"])):
        ws3.append([w["uwi"], w["name"], w["pad"], w["nonarr"]])
        ws3.cell(ws3.max_row, 4).number_format = "#,##0"
    for i, w in enumerate([23, 25, 16, 19], 1):
        ws3.column_dimensions[get_column_letter(i)].width = w
    ws3.freeze_panes = "A2"

    ws4 = wb.create_sheet("Sales PCs by maker")
    ws4.append(["Maker", "Area", "Sales gas pressure controllers, methane 2026 (kg)"])
    _head(ws4[1])
    ws4.row_dimensions[1].height = 30
    for x in g["bleed_ma"]:
        ws4.append([x["maker"], x["area"], int(rnd(x["kg"], 0))])
        ws4.cell(ws4.max_row, 3).number_format = "#,##0"
    for i, w in enumerate([28, 11, 22], 1):
        ws4.column_dimensions[get_column_letter(i)].width = w

    ws5 = wb.create_sheet("Notes")
    notes = [
        "Notes to the 2026 inventory",
        "",
        "Reporting year: the production days 1 January to 31 December 2026, each the 24 hours from 08:00 local time "
        "(MRS-03 3.2).",
        "Level controllers: dump cycles in the year times the maker's rated supply gas per cycle (MRS-03 4.2). The five "
        "separators the SCADA host counts use their counted cycles; the Activity basis column gives each controller's "
        "basis.",
        "Continuous-bleed controllers: the 2026 survey's reading on the device it measured, the maker's rating otherwise, "
        "for the hours the device was in service with its instrument supply on (MRS-03 4.3, 5.1).",
        "Conversions: 0.02826 m3 per scf, and methane at the pad's 2026 methane mole fraction times 0.678 kg per m3 "
        "(MRS-03 3.3, 4.4).",
        "Pads: tonnes are summed from unrounded kilograms. The 2027 conversion column applies the methane reduction "
        "plan's line, more than 0.5 t from a pad's intermittent-vent controllers (plan section 3).",
        "Plunger lift wells: cycles without an arrival are the rise in each controller's cycle count less the rise in "
        "its arrival count over the production days, on the well each unit ran.",
        "Not included: optical gas imaging leaks and tank vents, reported under MRS-05 and MRS-07 (MRS-03 4.5).",
        "Records: the January 2027 exports of the SCADA host and historian, production accounting's closed allocations, "
        "the equipment register and the 2026 work orders.",
    ]
    for t in notes:
        ws5.append([t or None])
    ws5["A1"].font = Font(name="Calibri", bold=True, size=12)
    ws5.column_dimensions["A"].width = 118
    for row in ws5.iter_rows(min_row=3):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)


INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
ACCENT = "#2a78d6"
NUMBER_WORDS = ["No", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven",
                "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen", "Twenty"]


def chart_png(path, g):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    from matplotlib.ticker import FormatStrFormatter
    plt.rcParams["font.family"] = "DejaVu Sans"
    pads = sorted(g["pads"], key=lambda p: -p["int_t"])
    fig, ax = plt.subplots(figsize=(11, 4.3), dpi=200)
    fig.patch.set_facecolor("white")
    xs = list(range(len(pads)))
    ax.bar(xs, [p["int_t"] for p in pads], color=[ACCENT if p["in"] else MUTED for p in pads], width=0.68, zorder=2)
    ax.axhline(W.LINE_T, color=INK, lw=1.1, ls=(0, (5, 3)), zorder=3)
    ax.text(len(pads) - 0.5, W.LINE_T + 0.018, "Plan line, %.1f t" % W.LINE_T, color=INK2, ha="right", va="bottom",
            fontsize=9)
    low = min((p for p in pads if p["in"]), key=lambda p: p["int_t"])
    high = max((p for p in pads if not p["in"]), key=lambda p: p["int_t"])
    for p in (low, high):
        i = pads.index(p)
        ax.text(i, p["int_t"] + 0.018, "%.2f t" % rnd(p["int_t"], 2), ha="center", va="bottom", fontsize=8.5, color=INK)
    ax.set_xticks(xs)
    ax.set_xticklabels([p["pad"] for p in pads], rotation=50, ha="right", fontsize=8, color=INK2)
    ax.set_xlim(-0.6, len(pads) - 0.4)
    ax.set_ylim(0, max(p["int_t"] for p in pads) * 1.12)
    ax.yaxis.set_major_formatter(FormatStrFormatter("%.1f"))
    ax.tick_params(axis="y", labelsize=9, colors=INK2, length=0)
    ax.tick_params(axis="x", length=0)
    ax.set_ylabel("Methane, 2026 (t)", fontsize=9, color=INK2)
    ax.grid(axis="y", color="#e1e0d9", lw=0.6, zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#c3c2b7")
    ax.legend(handles=[Patch(color=ACCENT, label="In the 2027 conversion"), Patch(color=MUTED, label="Kept to 2028")],
              frameon=False, fontsize=8.5, loc="upper right", labelcolor=INK2)
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": None}, facecolor="white")
    plt.close(fig)


def write_deck(path, g, png):
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.util import Inches, Pt

    def rgb(h):
        return RGBColor.from_string(h.lstrip("#"))

    def text(slide, x, y, w, h, s, size, color=INK, bold=False, align=None):
        tf = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame
        tf.word_wrap = True
        tf.text = s
        for para in tf.paragraphs:
            if align:
                para.alignment = align
            for run in para.runs:
                run.font.size = Pt(size)
                run.font.bold = bold
                run.font.name = "Calibri"
                run.font.color.rgb = rgb(color)
        return tf

    def frame(slide, n, title, sub, source):
        text(slide, 0.6, 0.35, 12.1, 0.8, title, 26, INK, bold=True)
        text(slide, 0.6, 1.08, 12.1, 0.5, sub, 13, INK2)
        line = slide.shapes.add_connector(1, Inches(0.6), Inches(6.92), Inches(12.73), Inches(6.92))
        line.line.color.rgb = rgb("#c3c2b7")
        line.line.width = Pt(0.75)
        line.shadow.inherit = False
        text(slide, 0.6, 6.98, 11.2, 0.4, source, 9, MUTED)
        text(slide, 11.9, 6.98, 0.83, 0.4, str(n), 9, MUTED, align=PP_ALIGN.RIGHT)

    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]
    pads = sorted(g["pads"], key=lambda p: -p["int_t"])
    rows = [p for p in pads if p["in"]]
    low = min(rows, key=lambda p: p["int_t"])
    high = max((p for p in pads if not p["in"]), key=lambda p: p["int_t"])
    src = ("Source: Larchmere 2026 source-level inventory under MRS-03 Revision 4 (larchmere_source_inventory_2026.xlsx, "
           "Annex B pads). Methane Reduction, 24 January 2027.")

    s1 = prs.slides.add_slide(blank)
    frame(s1, 1, "%s pads go into the 2027 zero-emission controller conversion" % NUMBER_WORDS[len(rows)],
          "Pads whose intermittent-vent controllers vented more than 0.5 t of methane in 2026, as reported under MRS-03 "
          "(methane reduction plan, section 3)", src)
    shape = s1.shapes.add_table(len(rows) + 1, 3, Inches(0.6), Inches(1.85), Inches(7.4), Inches(0.42 * (len(rows) + 1)))
    tb = shape.table
    for j, wdt in enumerate((2.7, 2.4, 2.3)):
        tb.columns[j].width = Inches(wdt)
    for j, h in enumerate(("Pad", "Surface location", "Methane 2026 (t)")):
        tb.cell(0, j).text = h
    for i, p in enumerate(rows, 1):
        tb.cell(i, 0).text = p["pad"]
        tb.cell(i, 1).text = p["lsd"]
        tb.cell(i, 2).text = "%.2f" % rnd(p["int_t"], 2)
    for r_ in range(len(rows) + 1):
        for c_ in range(3):
            cell = tb.cell(r_, c_)
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb("#184f95") if r_ == 0 else (rgb("#f1f0ec") if r_ % 2 == 0 else rgb("#ffffff"))
            for para in cell.text_frame.paragraphs:
                if c_ == 2:
                    para.alignment = PP_ALIGN.RIGHT
                for run in para.runs:
                    run.font.size = Pt(13)
                    run.font.name = "Calibri"
                    run.font.bold = r_ == 0
                    run.font.color.rgb = rgb("#ffffff") if r_ == 0 else rgb(INK)
    text(s1, 8.6, 1.85, 4.1, 0.4, "The order", 14, INK, bold=True)
    text(s1, 8.6, 2.3, 4.1, 2.6,
         "One order for the conversion kits, placed with the supplier by 15 February 2027, fixes this list.\n\n"
         "Installs run from May, after spring break-up, to the end of September.\n\n"
         "The other %d pads keep their controllers until the 2028 programme; the highest of them, %s, vented %.2f t."
         % (len(pads) - len(rows), high["pad"], rnd(high["int_t"], 2)), 12, INK2)

    s2 = prs.slides.add_slide(blank)
    frame(s2, 2, "The line falls between %s at %.2f t and %s at %.2f t"
          % (low["pad"], rnd(low["int_t"], 2), high["pad"], rnd(high["int_t"], 2)),
          "Every pad's 2026 methane from its intermittent-vent controllers, highest first, against the plan's 0.5 t line",
          src)
    s2.shapes.add_picture(png, Inches(0.6), Inches(1.7), width=Inches(12.1))
    prs.save(path)


def figures(g):
    tr = g["tr"]
    name = {p["code"]: p["pad"] for p in g["pads"]}
    gold = set(tr["sets"]["golden"])
    fig = {"call": sorted(p["pad"] for p in g["pads"] if p["in"]),
           "call_count": sum(p["in"] for p in g["pads"]),
           "line_t": W.LINE_T,
           "pads": {p["pad"]: {"int_t": rnd(p["int_t"], 2), "cont_t": rnd(p["cont_t"], 2), "in": p["in"]} for p in g["pads"]},
           "lc_kg": {"%s %s" % (r["pad"], r["tag"]): int(rnd(r["kg"], 0)) for r in g["lc"]},
           "bleed_by_maker_area": {"%s, %s" % (x["maker"], x["area"]): int(rnd(x["kg"], 0)) for x in g["bleed_ma"]},
           "nonarrivals": {w["name"]: w["nonarr"] for w in g["wells"]},
           "rivals": {"big_slug": sorted(name[c] for c in set(tr["sets"]["r1"]) - gold),
                      "dry": sorted(name[c] for c in set(tr["sets"]["label"]) - gold)},
           "ladder": {k: sorted(name[c] for c in v) for k, v in tr["sets"].items()},
           "constants": {"scf_to_m3": W.SCF_TO_M3, "ch4_kg_m3": W.CH4_KG_PER_M3, "wrap": 65536},
           "standard_clauses": [3.2, 3.3, 4.2, 4.3, 4.4],
           "campaign_rate_scf_h": round(tr["ef_scf_h"], 2),
           "int_total_t": rnd(sum(p["int_t"] for p in g["pads"]), 2)}
    return fig


def main(target, gdir, fig_path):
    os.makedirs(gdir, exist_ok=True)
    wd = S.simulate()
    g = compute(wd)
    write_inventory(os.path.join(gdir, W.DELIVERABLES[0]), g)
    import tempfile
    tmpd = tempfile.mkdtemp()
    png = os.path.join(tmpd, "chart.png")
    chart_png(png, g)
    write_deck(os.path.join(gdir, W.DELIVERABLES[1]), g, png)
    import postprocess as PP
    PP.normalize_ooxml(os.path.join(gdir, W.DELIVERABLES[0]), W.PEOPLE["lead"], W.PEOPLE["lead"], "2027-01-19T16:02:00Z",
                       "2027-01-24T22:37:00Z", excel=True, company=W.ORG)
    PP.normalize_ooxml(os.path.join(gdir, W.DELIVERABLES[1]), W.PEOPLE["lead"], W.PEOPLE["lead"], "2027-01-22T17:41:00Z",
                       "2027-01-24T23:05:00Z", company=W.ORG)
    import time
    ts = time.mktime(W.STAMP + (0, 0, -1))
    for f in W.DELIVERABLES:
        os.utime(os.path.join(gdir, f), (ts, ts))
    fig = figures(g)
    with open(fig_path, "w") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
    return g, fig
