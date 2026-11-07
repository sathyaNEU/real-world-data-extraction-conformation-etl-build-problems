"""task482 architecture 16: the golden deliverables and figures.json, written from golden.solve() on the pack.

    velden_low_carbon_premium_2027.docx   the purchasing note, with its chart
    brackwell_scr2_figures_2026.csv       the quarterly scrap and dross figures
"""
import csv
import io
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from docx import Document  # noqa: E402
from docx.enum.table import WD_TABLE_ALIGNMENT  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.shared import Cm, Pt, RGBColor  # noqa: E402

import golden as G  # noqa: E402
import postprocess as PP  # noqa: E402

NAME = {"BIL6063": "6063 extrusion billet", "BIL6082": "6082 extrusion billet", "INGLM25": "LM25 foundry ingot",
        "CSTLM25": "LM25-TF sand castings"}
MEMO = "velden_low_carbon_premium_2027.docx"
TABLE = "brackwell_scr2_figures_2026.csv"
HEAD = ["quarter", "scrap_old_cast_t", "scrap_extrusion_offcuts_t", "scrap_turnings_swarf_t", "scrap_ubc_t",
        "dross_sent_for_recovery_t"]


def chart(res):
    fam = res["fam"]
    order = G.FAMILIES
    vals = [fam[f]["intensity"] for f in order]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    fig, ax = plt.subplots(figsize=(6.4, 2.9), dpi=150)
    colours = ["#2f6f8f" if v <= G.LIMIT else "#c0504d" for v in vals]
    y = range(len(order))[::-1]
    ax.barh(list(y), vals, color=colours, height=0.58)
    ax.axvline(G.LIMIT, color="#333333", lw=1.1, ls="--")
    ax.text(G.LIMIT + 0.006, len(order) - 0.45, "SCR-2 limit 0.235", fontsize=8, color="#333333", va="center")
    for yy, v in zip(y, vals):
        ax.text(v + 0.006, yy, "%.3f" % v, va="center", fontsize=8)
    ax.set_yticks(list(y))
    ax.set_yticklabels([NAME[f] for f in order])
    ax.set_xlim(0, max(vals) * 1.18)
    ax.set_xlabel("t CO2 per tonne produced, 2026")
    ax.set_title("6082 billet and the castings are over the limit", fontsize=10, loc="left")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return buf


def _cell(c, text, bold=False, right=False, size=8.5):
    c.text = ""
    p = c.paragraphs[0]
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.bold = bold
    if right:
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT


def memo(res, path):
    fam, d, parts, beta = res["fam"], res["d"], res["parts"], res["beta"]
    earn = res["earning"]
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for s in doc.sections:
        s.left_margin = s.right_margin = Cm(2.2)
        s.top_margin = Cm(1.8)
        s.bottom_margin = Cm(1.8)
        fp = s.footer.paragraphs[0]
        fp.text = "Velden Automobil AG  |  Purchasing, light metals  |  internal"
        fp.runs[0].font.size = Pt(8)
        fp.runs[0].font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    hdr = [("To", "Tony Coleman, Purchasing, light metals"), ("From", "Supplier carbon reporting, light metals"),
           ("Date", "28 January 2027"), ("Subject", "Brackwell Alloys: SCR-2 low-carbon premium on 2027 call-offs")]
    for k, v in hdr:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run("%s:\t" % k)
        r.bold = True
        p.add_run(v)
    doc.add_paragraph()
    tot = sum(d["calloff"][f] for f in earn)
    h = doc.add_paragraph()
    r = h.add_run("Premium of EUR {:,} on {:,} t: 6063 billet and LM25 ingot qualify, 6082 billet and the castings "
                  "do not".format(res["premium"], tot))
    r.bold = True
    r.font.size = Pt(12.5)
    doc.add_paragraph(
        "Under SCR-2 section 7 Velden pays EUR 38 a tonne on the 2027 call-offs of each Brackwell family whose 2026 "
        "specific direct emissions were 0.235 t CO2/t or less. On Brackwell's 2026 data package two families "
        "qualify: 6063 extrusion billet at {a:.3f} and LM25 foundry ingot at {b:.3f}. Their call-offs of {c:,} t "
        "and {e:,} t give EUR {p:,}. 6082 billet ({g:.3f}) and the LM25-TF castings ({h:.3f}) are over the limit, "
        "so their {i:,} t and {j:,} t earn nothing.".format(
            a=fam["BIL6063"]["intensity"], b=fam["INGLM25"]["intensity"], c=d["calloff"]["BIL6063"],
            e=d["calloff"]["INGLM25"], p=res["premium"], g=fam["BIL6082"]["intensity"],
            h=fam["CSTLM25"]["intensity"], i=d["calloff"]["BIL6082"], j=d["calloff"]["CSTLM25"]))
    t = doc.add_table(rows=1, cols=7)
    t.style = "Light Grid Accent 1"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    heads = ["Family", "2026 production (t)", "2026 direct CO2 (t)", "t CO2/t", "Under limit", "2027 call-off (t)",
             "Premium (EUR)"]
    for c, x in zip(t.rows[0].cells, heads):
        _cell(c, x, bold=True)
    for f in G.FAMILIES:
        ok = f in earn
        row = t.add_row().cells
        vals = [NAME[f], "{:,.0f}".format(d["prod"][f]), "{:,.0f}".format(round(fam[f]["co2"], -1)),
                "%.3f" % fam[f]["intensity"], "yes" if ok else "no", "{:,}".format(d["calloff"][f]),
                "{:,}".format(38 * d["calloff"][f]) if ok else "0"]
        for k, (c, x) in enumerate(zip(row, vals)):
            _cell(c, x, right=k not in (0, 4))
    row = t.add_row().cells
    totals = ["Total", "{:,.0f}".format(sum(d["prod"].values())), "{:,.0f}".format(
        round(sum(fam[f]["co2"] for f in G.FAMILIES), -1)), "", "", "{:,}".format(sum(d["calloff"].values())),
        "{:,}".format(res["premium"])]
    for k, (c, x) in enumerate(zip(row, totals)):
        _cell(c, x, bold=True, right=k not in (0, 4))
    p = doc.add_paragraph()
    r = p.add_run("Production is the tonnes that passed Brackwell's final inspection in 2026, each lot at its last "
                  "result. Direct CO2 is the gas each family's processes burned plus its tonnage share of the gas no "
                  "process burned, at 0.18296 kg CO2/kWh. CO2 rounded to 10 t.")
    r.font.size = Pt(8)
    doc.add_picture(chart(res), width=Cm(15.5))
    doc.add_heading("How the gas was attributed", level=2)
    doc.add_paragraph(
        "Brackwell burns all of its gas through one site meter, so the gas each process burned has to be read from "
        "the meter. The supplier's 15-minute export (UTC; the imperial meter read in hundreds of cubic feet until "
        "the exchange on 14 April) was converted to cubic metres and then to kWh at the volume correction factor "
        "and the calorific value of the invoice covering each interval: {g:,.0f} MWh for 2026. Each local day's gas "
        "was then regressed on what each process did that day: tonnes melted in the casthouse furnaces M1 and M2 "
        "(each heat spread from charge to melt-out, re-keyed heats dropped), tonnes charged to the foundry tower "
        "melter M3, hours the homogenizing furnace H1 and the solution oven T1 fired (door closed to door opened), "
        "and heating degree days on base 15.5 C from the works' weather station.".format(g=parts["total"] / 1000.0))
    doc.add_paragraph(
        "The fit explains {r2:.1f} per cent of the daily variation. It gives {m:,.0f} kWh a tonne melted in the "
        "casthouse, {m3:,.0f} kWh a tonne in the tower melter, {h:,.0f} kWh an hour in the homogenizing furnace and "
        "{t:,.0f} kWh an hour in the solution oven, with {c:,.0f} kWh a day of pilot flames and {dd:,.0f} kWh a degree "
        "day of space heating.".format(r2=100 * res["r2"], m=beta["melt"], m3=beta["m3"], h=beta["h1"], t=beta["t1"],
                                       c=beta["const"], dd=beta["hdd"]))
    doc.add_paragraph(
        "The homogenizing furnace burns by the hour whatever the load weighs: a 6082 load soaks about {a:.0f} hours "
        "against about {b:.0f} for 6063, so 6082 billet carries {c:.0f} per cent of the furnace's gas on {e:.0f} per "
        "cent of its tonnes. Shared by tonnes, both billet alloys would sit at the same {f:.3f} and 6082 would "
        "qualify. The castings carry the tower melter and the solution oven, and melt about 1.65 t for every tonne "
        "that passes inspection. The gas no process burned ({base:,.0f} MWh) is shared by tonnes produced, as SCR-2 "
        "section 3 sets out.".format(
            a=parts["hours"]["BIL6082"] / sum(1 for ld in d["h1"] if ld["family"] == "BIL6082"),
            b=parts["hours"]["BIL6063"] / sum(1 for ld in d["h1"] if ld["family"] == "BIL6063"),
            c=100 * parts["hours"]["BIL6082"] / sum(parts["hours"].values()),
            e=100 * parts["tonnes"]["BIL6082"] / sum(parts["tonnes"].values()),
            f=res["r1_billet"], base=parts["base"] / 1000.0))
    p = doc.add_paragraph()
    r = p.add_run("Sources: Brackwell SCR-2 data package of 21 January 2027 (site gas meter export, Northgate gas "
                  "invoices, furnace and oven logs, production lots, weather); Velden call-off schedule 2027, "
                  "revision 0.")
    r.font.size = Pt(8)
    doc.save(path)
    PP.normalize_ooxml(path, "Tony Coleman", "Tony Coleman", "2027-01-26T09:14:00Z", "2027-01-28T11:52:00Z",
                       company="Velden Automobil AG")


def table(res, path):
    a, b = res["ask_a"], res["ask_b"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(HEAD)
        for q in G.QUARTERS:
            w.writerow(["2026-%s" % q] + [int(round(a[g][q])) for g in G.GRADES] + [int(round(b[q]))])


def write_all(target, golden_dir, here):
    res = G.solve(target)
    beta = res["beta"]
    alt, _ = G.attribute(res["d"], beta, h1="tonnes")
    res["r1_billet"] = alt["BIL6063"]["intensity"]
    os.makedirs(golden_dir, exist_ok=True)
    memo(res, os.path.join(golden_dir, MEMO))
    table(res, os.path.join(golden_dir, TABLE))
    fig = G.figures(res)
    json.dump(fig, open(os.path.join(here, "figures.json"), "w"), indent=1, sort_keys=True)
    return fig, res
