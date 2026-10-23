"""The golden: every owed figure computed from the cut pack (bundle.py), written to generator/figures.json, and the three
deliverables, deq_rule18-4_applicability_2027.xlsx, deq_printing_press_voc_2026.csv and deq_printing_press_voc_2026.svg."""
import csv
import io
import json
import os

import numpy as np

import bundle as B

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = "deq_rule18-4_applicability_2027.xlsx"
CSV = "deq_printing_press_voc_2026.csv"
SVG = "deq_printing_press_voc_2026.svg"


def compute(target):
    I = B.Inputs(target)
    g = B.press_tons(I, "golden")
    f, (F, p) = B.relation(I, "golden")
    r0 = B.rung_tons(I, "R0")
    clean = B.cleaning_tons(I)
    gal = B.unaccounted_gal(I)
    num = I.facno
    cov = B.covered(g)
    below = sorted((n for n in I.order if n not in cov), key=lambda n: -g[n]["emitted"])
    near = below[0]
    low = min(cov, key=lambda n: g[n]["emitted"])
    tested = {n: round(I.latest(n)["dre"], 2) for n in I.controlled}
    fig = {
        "call": {"plants": cov, "count": len(cov), "of": len(I.order)},
        "plants": {n: {"facility_no": num[n], "press_voc_tons": B.hround(g[n]["emitted"]), "covered": n in cov,
                       "cleaning_voc_tons": B.round1(clean[n]), "unaccounted_gal": B.hround(gal[n])}
                   for n in I.order},
        "components": {
            "nearest_below": {"name": near, "tons": B.hround(g[near]["emitted"]),
                              "short_tons": B.hround(25.0 - g[near]["emitted"])},
            "lowest_covered": {"name": low, "tons": B.hround(g[low]["emitted"])},
            "floor_ppmc": round(float(F), 1), "pass_pct": round(100 * float(p), 2),
            "knee_ppmc": int(round(float(F / p), -2)),
            "tests": len(I.tests), "runs": int(len(I.ci)), "oxidizers": len(I.controlled),
            "area_tons": B.hround(sum(g[n]["emitted"] for n in I.order)),
            "covered_tons": B.hround(sum(g[n]["emitted"] for n in cov)),
        },
        "default": {"plants": B.covered(r0), "tons": {n: B.hround(r0[n]) for n in I.order},
                    "latest_dre_pct": tested},
        "stated": {"threshold_tons": 25, "rule": "18-4", "applies_from": "1 July 2027", "year": 2026,
                   "dilute_below_ppmc": int(B.DILUTE), "concentrated_above_ppmc": int(B.CONC),
                   "cs210_rev3_lb_gal": 7.10, "cs210_rev4_lb_gal": round(I.vpg("HW-CS-210"), 2),
                   "kg_to_lb": 2.20462, "renumbered": "1 April 2026", "reformulated": "1 June 2026",
                   "propane_to_carbon": 3, "former_facility_no": "0117"},
        "_unrounded": {"press": {n: {k: round(v, 4) for k, v in g[n].items()} for n in I.order},
                       "cleaning": {n: round(clean[n], 4) for n in I.order},
                       "gallons": {n: round(gal[n], 3) for n in I.order},
                       "default": {n: round(r0[n], 4) for n in I.order},
                       "floor": float(F), "pass": float(p)},
    }
    return fig


def write_csv(path, f):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(["facility_no", "plant", "press_voc_2026_tons", "rule_18_4_from_2027_07_01"])
    for n, x in f["plants"].items():
        w.writerow([x["facility_no"], n, x["press_voc_tons"], "Y" if x["covered"] else "N"])
    open(path, "w", encoding="utf-8", newline="").write(buf.getvalue())


def write_xlsx(path, f):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Appendix A"
    bold = Font(name="Calibri", size=11, bold=True)
    thin = Side(style="thin", color="808080")
    ws["A1"] = "Rule 18-4, Appendix A: plants subject from 1 July 2027"
    ws["A1"].font = Font(name="Calibri", size=14, bold=True)
    ws["A2"] = ("Air Quality Division, Emissions Inventory Section. From the 2026 inventory of the Kestle Valley's "
                "printing and converting plants, for the Environmental Quality Council's meeting of 25 March 2027.")
    ws["A2"].font = Font(name="Calibri", size=9, italic=True, color="555555")
    ws.append([])
    ws.append(["Plant", "Facility no.", "2026 press VOC (tons)"])
    for c in ws[4]:
        c.font = bold
        c.alignment = Alignment(wrap_text=True, vertical="bottom")
        c.border = Border(bottom=thin)
    for n in f["call"]["plants"]:
        x = f["plants"][n]
        ws.append([n, x["facility_no"], x["press_voc_tons"]])
    last = ws.max_row
    for row in ws.iter_rows(min_row=5, max_row=last):
        row[1].number_format = "@"
        row[2].number_format = "#,##0"
    nb = f["components"]["nearest_below"]
    ws.cell(row=last + 2, column=1, value="Section 18-4-3: 25 tons or more of VOC from the presses in calendar 2026. "
            "Nearest plant below the line: %s, %d tons, %d short." % (nb["name"], nb["tons"], nb["short_tons"]))
    ws.cell(row=last + 2, column=1).font = Font(name="Calibri", size=9, color="555555")
    for col, wd in zip("ABC", (34, 11, 14)):
        ws.column_dimensions[col].width = wd
    ws.row_dimensions[4].height = 30
    ws.freeze_panes = "A5"

    s2 = wb.create_sheet("Plants")
    s2.append(["Plant", "Facility no.", "2026 press VOC (tons)", "Subject to Rule 18-4", "2026 VOC from cleaning away "
               "from presses (tons)", "Inks, coatings and adhesives received in 2026 and unaccounted for (gal)"])
    for c in s2[1]:
        c.font = bold
        c.alignment = Alignment(wrap_text=True, vertical="bottom")
        c.border = Border(bottom=thin)
    fill = PatternFill("solid", fgColor="DDEBF7")
    for n, x in f["plants"].items():
        s2.append([n, x["facility_no"], x["press_voc_tons"], "Yes" if x["covered"] else "No", x["cleaning_voc_tons"],
                   x["unaccounted_gal"]])
        if x["covered"]:
            for c in s2[s2.max_row]:
                c.fill = fill
    for row in s2.iter_rows(min_row=2, max_row=s2.max_row):
        row[1].number_format = "@"
        row[2].number_format = "#,##0"
        row[3].alignment = Alignment(horizontal="center")
        row[4].number_format = "0.0"
        row[5].number_format = "#,##0"
    for col, wd in zip("ABCDEF", (34, 11, 12, 11, 16, 22)):
        s2.column_dimensions[col].width = wd
    s2.row_dimensions[1].height = 62
    s2.freeze_panes = "B2"
    s2.print_title_rows = "1:1"

    s3 = wb.create_sheet("Notes")
    cp = f["components"]
    notes = [
        ("2026 press VOC", "Section 18-4-3(b): the VOC in the press materials used on each plant's presses, less what "
         "its capture system and oxidizer destroyed. VOC used is each press log row through the product's safety data "
         "sheet (Thameside Laminating's rows before 1 May to Kelvedon Laminates). Captured VOC is that times the "
         "capture efficiency in the register. The %d performance tests since 2017 (%d runs, Marlow's propane figures "
         "times three to carbon) put each oxidizer's outlet at about %.0f ppmv as carbon below an inlet of about "
         "%s ppmv and at %.1f per cent of the inlet above it, and every test ran at maximum production. Each 2026 "
         "production day's inlet is its captured VOC over the oxidizer's process hours and mean airflow (the historian "
         "on Central time, fan speed times rated airflow) through the plant's carbon content; the day's outlet times "
         "its air and hours is what the oxidizer let through." % (cp["tests"], cp["runs"], cp["floor_ppmc"],
                                                                 "{:,}".format(cp["knee_ppmc"]), cp["pass_pct"])),
        ("Cleaning VOC", "Section 18-4-5(b): cleaning materials issued away from the presses at the safety data "
         "sheet revision in force on the issue date (HW-CS-210 at 7.10 lb VOC a gallon before its 1 June 2026 "
         "reformulation), less spent cleaning solvent shipped under each plant's cleaning profile, plus each parts "
         "washer's solvent added less spent solvent removed, Wexcombe's tickets and Ostrander's service lines."),
        ("Gallons unaccounted for", "Inks, coatings and adhesives: the 1 January 2026 count, plus what Corvane and "
         "Haldane shipped in 2026 net of returns, less the 31 December 2026 count and the press logs' use. Haldane "
         "documents dated before 1 April 2026 carry its old item numbers, read through its catalog's replaces column; "
         "adhesives sold by the pound are converted by density."),
        ("Rounding", "Press VOC and the shortfall to the whole ton, cleaning VOC to a tenth of a ton and gallons to "
         "the whole gallon, each from the unrounded figure."),
    ]
    s3.append(["Item", "Note"])
    for c in s3[1]:
        c.font = bold
    for k, v in notes:
        s3.append([k, v])
    for row in s3.iter_rows(min_row=2):
        row[1].alignment = Alignment(wrap_text=True, vertical="top")
        row[0].alignment = Alignment(vertical="top")
    s3.column_dimensions["A"].width = 24
    s3.column_dimensions["B"].width = 100
    wb.save(path)
    import postprocess as PP
    PP.normalize_ooxml(path, "Audrey Bautista", "Audrey Bautista", "2027-02-22T15:06:00Z", "2027-03-03T22:41:18Z",
                       excel=True, company=PP.COMPANY)


def write_svg(path, f):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    matplotlib.rcParams["svg.hashsalt"] = "task482-deq"
    matplotlib.rcParams["svg.fonttype"] = "none"
    matplotlib.rcParams["font.family"] = "DejaVu Sans"
    un = f["_unrounded"]["press"]
    names = sorted(f["plants"], key=lambda n: -un[n]["emitted"])
    vals = [un[n]["emitted"] for n in names]
    on = [f["plants"][n]["covered"] for n in names]
    blue, grey, ink, muted, line = "#2a6fb0", "#c3c8ce", "#1f2328", "#59636e", "#b3261e"
    fig, ax = plt.subplots(figsize=(9.6, 5.6), dpi=100)
    ys = np.arange(len(names))[::-1]
    ax.barh(ys, vals, height=0.66, color=[blue if o else grey for o in on], edgecolor="white", linewidth=2, zorder=3)
    for y, n, v, o in zip(ys, names, vals, on):
        ax.text(v + 0.6, y, "%d" % f["plants"][n]["press_voc_tons"], ha="left", va="center", fontsize=9,
                color=ink if o else muted, fontweight="bold" if o else "normal")
    ax.axvline(25, color=line, linewidth=1.6, zorder=4)
    ax.text(25.4, ys[0] + 0.55, "25 tons: Rule 18-4 applies", color=line, fontsize=8.5, va="bottom")
    ax.set_yticks(ys)
    ax.set_yticklabels(names, fontsize=9, color=ink)
    ax.set_xlabel("VOC emitted from the presses, 2026 (tons)", fontsize=9, color=muted)
    ax.set_xlim(0, max(vals) * 1.1)
    ax.set_ylim(-0.7, len(names) - 0.1)
    ax.tick_params(axis="x", labelsize=8.5, colors=muted)
    ax.grid(axis="x", color="#e6e8eb", linewidth=0.8, zorder=0)
    for side in ("top", "right", "bottom"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color("#9aa1a9")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=blue, label="Subject to Rule 18-4 from 1 July 2027"),
                       Patch(color=grey, label="Below 25 tons")], loc="lower right", frameon=False, fontsize=8.5)
    nb = f["components"]["nearest_below"]
    fig.suptitle("Five Kestle Valley plants' presses emitted 25 tons or more of VOC in 2026", x=0.012, ha="left",
                 fontsize=11.5, fontweight="bold", color=ink)
    ax.set_title("Press VOC after capture and oxidizer, by plant; the five in blue come under Rule 18-4.\n"
                 "Nearest below the line: %s, %d tons, %d short." % (nb["name"], nb["tons"], nb["short_tons"]),
                 loc="left", fontsize=8.5, color=muted, pad=10, linespacing=1.5)
    fig.text(0.012, 0.012, "Source: Department of Environmental Quality, 2026 inventory of printing and converting "
             "plants (press logs, oxidizer historians and performance tests).", fontsize=7.5, color=muted)
    fig.subplots_adjust(left=0.27, right=0.98, top=0.84, bottom=0.11)
    buf = io.StringIO()
    fig.savefig(buf, format="svg", metadata={"Date": None, "Creator": "Emissions Inventory Section"})
    plt.close(fig)
    svg = buf.getvalue().replace('id="matplotlib.', 'id="').replace("'DejaVu Sans'",
                                                                   "'DejaVu Sans', Arial, Helvetica, sans-serif")
    assert "matplotlib" not in svg.lower()
    open(path, "w", encoding="utf-8", newline="\n").write(svg)


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    f = compute(target)
    json.dump(f, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    out = os.path.join(os.path.dirname(HERE), "golden")
    os.makedirs(out, exist_ok=True)
    for fn in os.listdir(out):
        os.remove(os.path.join(out, fn))
    write_xlsx(os.path.join(out, XLSX), f)
    write_csv(os.path.join(out, CSV), f)
    write_svg(os.path.join(out, SVG), f)
    return f


if __name__ == "__main__":
    import sys
    f = main(sys.argv[1] if len(sys.argv) > 1 else None)
    print(json.dumps({k: v for k, v in f.items() if not k.startswith("_")}, indent=1)[:4000])
