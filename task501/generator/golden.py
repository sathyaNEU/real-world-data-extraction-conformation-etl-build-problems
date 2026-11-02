"""The golden deliverables, figures.json and metadata.json, computed from the shipped pack by solve.py."""
import datetime as dt
import io
import json
import os

import numpy as np

import bundle as B
import pack as PK
import post as PP
import solve as S
import world as W

ASSESSED = "20 November 2026"
FLUSH, KEEP = "#eb6834", "#2a78d6"          # validated pair (dataviz validate_palette.js, light surface)


def r0(x):
    return int(np.floor(x + 0.5))


def r1(x):
    return "%.1f" % (np.floor(x * 10 + 0.5) / 10.0)


def compute(target):
    c = S.call(target)
    net = c["net"]
    mains = []
    for m in c["rises"]:
        k = c["F"][c["ok"].values][m].idxmax()
        mains.append(dict(id=m, name=net.mains[m]["Name"], dn=int(net.mains[m]["DN (mm)"]), peak=float(c["peak"][m]),
                          ref=float(c["ref"][m]), when=(k if c["ref"][m] > 0 else None), flush=m in c["flush"]))
    a, _ = S.ask_a(target)
    _, adf = S.ask_a(target, "golden")
    b, moved = S.ask_b(target, "golden", districts=[W.DCODE[d] for d in W.REROUTED])
    sp = B.supply(target)
    moved_rows = []
    for lid, (rec, new, over, _) in sorted(moved.items()):
        cust = sp.loc[sp["AMR logger"] == lid, "Customer"].iloc[0]
        moved_rows.append(dict(logger=lid, customer=cust, recorded=rec, supplied=new, hours=over))
    # components of ask A for the workbook
    sec = adf.groupby(["night_of", "crew", "section_ref"]).agg(w=("w", "sum"), L=("L", "first"), dn=("dn", "first"),
                                                                year=("year", "first")).reset_index()
    parts = sec.groupby(["dn", "year"]).agg(w=("w", "sum"), L=("L", "sum"), n=("section_ref", "count"))
    return dict(call=c, mains=mains, ask_a=a, ask_a_parts=parts, ask_b=b, moved=moved_rows)


def call_sentence(res):
    fl = [m for m in res["mains"] if m["flush"]]
    fl.sort(key=lambda m: (not m["id"].startswith("TM"), m["id"]))
    names = " and ".join("%s %s" % (m["id"], m["name"]) for m in fl)
    return "Flush two mains before the relining starts on 15 March 2027: %s." % names


def figures(res):
    out = {"call": call_sentence(res), "flush": [m["id"] for m in res["mains"] if m["flush"]],
           "mains": {}, "flushing_water_m3_per_100m": {}, "nonhousehold_water_ml": {}}
    for m in res["mains"]:
        out["mains"][m["id"]] = {"name": m["name"], "highest_hourly_flow_during_works_l_s": r0(m["peak"]),
                                 "highest_hourly_flow_carried_nov2025_oct2026_l_s": r0(m["ref"]),
                                 "flush": "Yes" if m["flush"] else "No"}
    for (dn, yr), v in sorted(res["ask_a"].items()):
        out["flushing_water_m3_per_100m"]["%d mm %d" % (dn, yr)] = r1(v)
    for d in W.REROUTED:
        out["nonhousehold_water_ml"]["%s %s" % (W.DCODE[d], W.DISTRICTS[d][1])] = r1(res["ask_b"][W.DCODE[d]])
    out["moved_supply_points"] = [dict(logger=m["logger"], customer=m["customer"], recorded=m["recorded"],
                                       supplied=m["supplied"]) for m in res["moved"]]
    out["diameters_mm"] = list(W.DIAMETERS)
    out["per_metres"] = 100
    return out


# ------------------------------------------------------------------------------------------------ workbook
def write_xlsx(path, res, figs):
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    wb = openpyxl.Workbook()
    bold = Font(bold=True)
    head = PatternFill("solid", fgColor="D9E2EA")
    ws = wb.active
    ws.title = "Flushing call"
    ws.append(["TM107 Ferrars Lane relining, 15 March to 15 September 2027: NOS 12 assessment"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Assessed %s against outage plan v1.0 (16 November 2026)" % ASSESSED])
    ws["A2"].font = Font(italic=True, size=9, color="555555")
    ws.append([])
    ws.append([figs["call"] + " No other main needs flushing."])
    ws["A4"].font = Font(bold=True, color="9C2A00")
    ws.append([])
    ws.append(["Main", "Name", "DN (mm)", "Highest hourly flow during the works (l/s)",
               "Highest hourly flow carried, Nov 2025 to Oct 2026 (l/s)", "Date of that flow", "Flush before works"])
    for c in ws[6]:
        c.font = bold
        c.fill = head
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for m in res["mains"]:
        f = figs["mains"][m["id"]]
        when = m["when"].strftime("%d %b %Y") if m["when"] is not None else "not in service"
        ws.append([m["id"], m["name"], m["dn"], f["highest_hourly_flow_during_works_l_s"],
                   f["highest_hourly_flow_carried_nov2025_oct2026_l_s"], when, f["flush"]])
        for col in ("D", "E"):
            ws["%s%d" % (col, ws.max_row)].number_format = "0"
    ws.freeze_panes = "A7"
    ws.append([])
    notes = [
        "Trunk mains have no meters: hourly flows rebuilt from the district inlet meters (UTC) through the valve "
        "positions in force each hour, from the control room valve log (local time) and the register.",
        "Works flows: the outage plan's valve changes applied to the districts' recorded inflows for 15 Mar to 15 Sep "
        "2026 (NOS 12, 4.3). Listed mains are those the arrangement loads above their normal flow in every hour.",
        "Flush where the works flow passes the highest hourly flow the main carried in the twelve months to October "
        "2026 (NOS 12, 4.2). IC05 has not been in service in the period.",
    ]
    for n in notes:
        ws.append([n])
    for col, wdt in zip("ABCDEFG", (8, 36, 9, 20, 22, 16, 12)):
        ws.column_dimensions[col].width = wdt
    ws.row_dimensions[6].height = 45

    ws = wb.create_sheet("Flushing water")
    ws.append(["2025-26 mains flushing programme: water used per 100 m of main flushed"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["From the contractor's job sheets (re-sent sheets removed; crew C14's meter readings from 1 Dec 2025 "
               "run on through each night and are differenced; twin-hydrant flushes counted once per section)"])
    ws["A2"].font = Font(italic=True, size=9, color="555555")
    ws.append([])
    ws.append(["Diameter (mm)", "2025 (m3 per 100 m)", "2026 (m3 per 100 m)", "2025 main flushed (m)",
               "2026 main flushed (m)", "2025 water used (m3)", "2026 water used (m3)"])
    for c in ws[4]:
        c.font = bold
        c.fill = head
        c.alignment = Alignment(wrap_text=True, vertical="top")
    parts = res["ask_a_parts"]
    for dn in W.DIAMETERS:
        row = [dn]
        for yr in W.ASK_YEARS:
            row.append(float(figs["flushing_water_m3_per_100m"]["%d mm %d" % (dn, yr)]))
        for yr in W.ASK_YEARS:
            row.append(int(round(parts.loc[(dn, yr), "L"])))
        for yr in W.ASK_YEARS:
            row.append(round(float(parts.loc[(dn, yr), "w"]), 1))
        ws.append(row)
        r_ = ws.max_row
        for col, fmt in zip("BCDEFG", ("0.0", "0.0", "#,##0", "#,##0", "#,##0.0", "#,##0.0")):
            ws["%s%d" % (col, r_)].number_format = fmt
    ws.freeze_panes = "B5"
    for col, wdt in zip("ABCDEFG", (13, 13, 13, 14, 14, 14, 14)):
        ws.column_dimensions[col].width = wdt
    ws.row_dimensions[4].height = 32

    ws = wb.create_sheet("Non-household water")
    ws.append(["Non-household water, November 2025 to October 2026, districts the relining re-routes"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Monthly settled consumption by supply point, placed in the district that supplies it"])
    ws["A2"].font = Font(italic=True, size=9, color="555555")
    ws.append([])
    ws.append(["DMA", "Name", "Supplied during works through", "Water used (Ml)"])
    for c in ws[4]:
        c.font = bold
        c.fill = head
    for d in W.REROUTED:
        ws.append([W.DCODE[d], W.DISTRICTS[d][1], "IC05" if W.DNODE[d] in ("N3", "N4") else "IC03",
                   float(figs["nonhousehold_water_ml"]["%s %s" % (W.DCODE[d], W.DISTRICTS[d][1])])])
        ws["D%d" % ws.max_row].number_format = "#,##0.0"
    ws.append(["Total", None, None, float(r1(sum(res["ask_b"][W.DCODE[d]] for d in W.REROUTED)))])
    ws["A%d" % ws.max_row].font = bold
    ws["D%d" % ws.max_row].font = bold
    ws["D%d" % ws.max_row].number_format = "#,##0.0"
    ws.freeze_panes = "A5"
    ws.append([])
    ws.append(["Supply points recorded in one DMA and supplied from its neighbour (logged use above the recorded "
               "DMA's whole inflow; load steps in the neighbour's inflow):"])
    ws.cell(row=ws.max_row, column=1).font = bold
    for m in res["moved"]:
        ws.append([m["logger"], m["customer"], "recorded %s, supplied from %s" % (m["recorded"], m["supplied"])])
    for col, wdt in zip("ABCD", (10, 30, 34, 16)):
        ws.column_dimensions[col].width = wdt
    ws = wb.create_sheet("Notes")
    notes = [
        ("As at", "Meters and valve log to 31 October 2026; outage plan v1.0 of 16 November 2026."),
        ("Clock", "District meters and turbidity on UTC hours; valve log on local time, converted (BST to 25 October)."),
        ("Meters", "Re-sent rows for BRK179 on 9 February removed; blank hours left out (none near a peak); "
                   "BRK146 and BRK194 meter changes joined on the DMA."),
        ("Switch hours", "An hour with valve work is taken in the arrangement that held for most of it."),
        ("Flushing water", "Year is that of night_of. Length is section_length_m, once per section and night."),
        ("Non-household", "Settled monthly consumption, 2025-11 to 2026-10. Supply points placed by the DMA whose "
                          "inflow carries them (see that sheet)."),
        ("Rounding", "Flows to the whole l/s, flushing water to 0.1 m3 per 100 m, non-household water to 0.1 Ml, "
                     "each rounded once from unrounded totals."),
    ]
    ws.append(["Item", "Note"])
    for c in ws[1]:
        c.font = bold
        c.fill = head
    for n_ in notes:
        ws.append(list(n_))
    ws.column_dimensions["A"].width = 16
    ws.column_dimensions["B"].width = 110
    wb.save(path)
    PP.normalize_ooxml(path, W.PEOPLE["planner"], W.PEOPLE["planner"], "2026-11-18T09:12:00Z", "2026-11-20T16:40:00Z",
                       excel=True)


# ------------------------------------------------------------------------------------------------ note
def chart_png(res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ms = sorted(res["mains"], key=lambda m: m["peak"])
    fig, ax = plt.subplots(figsize=(6.6, 3.0), dpi=150)
    y = np.arange(len(ms))
    cols = [FLUSH if m["flush"] else KEEP for m in ms]
    ax.barh(y, [r0(m["peak"]) for m in ms], color=cols, height=0.56, zorder=2)
    ax.scatter([r0(m["ref"]) for m in ms], y, marker="|", s=380, color="#0b0b0b", linewidths=2.0, zorder=3)
    for yi, m in zip(y, ms):
        ax.text(r0(m["peak"]) + 3, yi - 0.05, "%d" % r0(m["peak"]), va="center", fontsize=7.5, color="#0b0b0b")
    ax.set_yticks(y)
    ax.set_yticklabels(["%s %s" % (m["id"], m["name"].replace(" interconnector", " IC").replace(" main", ""))
                        for m in ms], fontsize=7.5)
    ax.set_xlabel("Highest hourly flow (l/s)", fontsize=8)
    ax.tick_params(axis="x", labelsize=7.5)
    ax.set_xlim(0, max(max(r0(m["peak"]), r0(m["ref"])) for m in ms) * 1.12)
    ax.grid(axis="x", color="#dddddd", linewidth=0.6, zorder=0)
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    ax.set_title("Four of the six already carried more than the works will send them", fontsize=8.6, loc="left",
                 color="#0b0b0b")
    ax.legend(handles=[Patch(color=FLUSH, label="During the works: flush"),
                       Patch(color=KEEP, label="During the works: no flush"),
                       Line2D([0], [0], marker="|", color="#0b0b0b", linestyle="None", markersize=10, mew=2,
                              label="Highest carried, Nov 2025 to Oct 2026")],
              fontsize=6.8, loc="lower right", frameon=False)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def write_note(path, res, figs):
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    import docs as DOC
    ink = colors.HexColor("#1b2430")
    body = ParagraphStyle("b", fontName=DOC.SANS, fontSize=9.2, leading=12.4, textColor=ink, spaceAfter=4)
    lead = ParagraphStyle("l", parent=body, fontName=DOC.SANS_B, fontSize=10.4, leading=13.8, spaceAfter=6)
    h1 = ParagraphStyle("h", fontName=DOC.SANS_B, fontSize=13.5, leading=17, textColor=colors.HexColor("#0f4c81"))
    small = ParagraphStyle("s", parent=body, fontSize=7.6, leading=10, textColor=colors.HexColor("#5d6872"))
    cell = ParagraphStyle("c", parent=body, fontSize=8.0, leading=10, spaceAfter=0)
    d = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=15 * mm,
                          bottomMargin=14 * mm, title="TM107 relining: trunk mains to flush", author=W.PEOPLE["planner"],
                          subject="NOS 12 assessment", creator=W.PEOPLE["planner"], producer=W.COMPANY)
    f = [Paragraph("%s | Network Operations" % W.COMPANY, small),
         Paragraph("TM107 relining: flush TM112 and IC05 before 15 March 2027", h1), Spacer(1, 2),
         Paragraph("To: %s, %s. From: %s, %s. %s. Ref: TM107 outage plan v1.0, NOS 12 section 4 assessment."
                   % (W.PEOPLE["head_ops"], W.TITLES["head_ops"], W.PEOPLE["planner"], W.TITLES["planner"], ASSESSED),
                   small), Spacer(1, 4)]
    fl = [m for m in res["mains"] if m["flush"]]
    nf = [m for m in res["mains"] if not m["flush"]]
    f.append(Paragraph(figs["call"], lead))
    f.append(Paragraph(
        "The relining arrangement loads six trunk mains above their normal flow. Four of them (%s) carried more water in "
        "the June and July 2026 Mill Road jobs than the relining will send them, so their deposits have already been "
        "worked at those flows and they need no flushing. TM112 carried at most %d l/s in the year (Brook Street "
        "relining, spring 2026) against %d l/s during the works, and IC05 has not been in service at all."
        % (", ".join(m["id"] for m in nf), r0(next(m for m in fl if m["id"] == "TM112")["ref"]),
           r0(next(m for m in fl if m["id"] == "TM112")["peak"])), body))
    png = chart_png(res)
    img = Image(io.BytesIO(png), width=170 * mm, height=170 * mm * 3.0 / 6.6)
    f.append(img)
    f.append(Paragraph("Source: district inlet meters (historian, hourly), control room valve log, trunk mains register, "
                       "outage plan v1.0.", small))
    rows = [["Main", "Name", "During the works (l/s)", "Carried, Nov 2025 to Oct 2026 (l/s)", "Flush"]]
    for m in res["mains"]:
        fm = figs["mains"][m["id"]]
        rows.append([m["id"], m["name"], str(fm["highest_hourly_flow_during_works_l_s"]),
                     str(fm["highest_hourly_flow_carried_nov2025_oct2026_l_s"]), fm["flush"]])
    t = Table([[Paragraph(c, cell) for c in r] for r in rows], colWidths=[16 * mm, 62 * mm, 30 * mm, 42 * mm, 16 * mm])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#9aa6ad")),
                           ("LINEBELOW", (0, -1), (-1, -1), 0.4, colors.HexColor("#9aa6ad")),
                           ("TOPPADDING", (0, 0), (-1, -1), 1.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6)]))
    f.append(Spacer(1, 3))
    f.append(t)
    f.append(Spacer(1, 5))
    f.append(Paragraph(
        "Basis. No trunk main is metered, so each main's hourly flow is rebuilt from the district inlet meters through "
        "the valve positions in force that hour (control room valve log, local time, against the trunk mains "
        "register). Flows during the works are the outage plan's valve changes applied to the districts' recorded "
        "inflows for 15 March to 15 September 2026 (NOS 12, 4.3); a main is flushed where that flow passes the highest "
        "hourly flow it carried in November 2025 to October 2026 (NOS 12, 4.2). The flushing water per 100 m and the "
        "non-household water for the re-routed districts are in ferrars_lane_flushing_2027.xlsx.", small))
    f.append(Paragraph("IC05's boundary valve was worked twice in the year under the exercising programme, cracked a few "
                       "turns and reshut each time; it carried no water.", small))

    def foot(canvas, doc):
        canvas.saveState()
        canvas.setFont(DOC.SANS, 7.2)
        canvas.setFillColor(colors.HexColor("#5d6872"))
        canvas.drawString(18 * mm, 9 * mm, "%s | NOS 12 assessment | TM107 relining" % W.COMPANY)
        canvas.drawRightString(A4[0] - 18 * mm, 9 * mm, "Page 1 of 1")
        canvas.restoreState()
    d.build(f, onFirstPage=foot)
    PP.normalize_pdf(path, b"D:20261120161502+00'00'", b"D:20261120163844+00'00'")


# ------------------------------------------------------------------------------------------------ metadata
def metadata(path, target, counts):
    rows = {k: counts.get(k, 0) for k in PK.FILES}
    largest = max(("flows", "turbidity", "amr"), key=lambda k: rows[k])
    prov = {
        "flows": ("Hourly mean inflow at each district metered area's inlet meter, historian export (UTC)",
                  "Network Operations telemetry", "2026-11-02"),
        "outlet": ("Hourly treated water outflow at Copt Hill works (UTC)", "Network Operations telemetry", "2026-11-02"),
        "register": ("Stavenham trunk mains register: mains, valves and district metered areas", "Asset Information",
                     "2026-11-02"),
        "valvelog": ("Control room valve operations log, Stavenham network, November 2025 to October 2026",
                     "Control Room", "2026-11-02"),
        "turbidity": ("Fifteen-minute turbidity at monitored district inlets (UTC)", "Water Quality telemetry",
                      "2026-11-02"),
        "standard": ("Network Operations Standard NOS 12, issue 3", W.COMPANY, "2025-03-18"),
        "plan": ("Outage plan for the TM107 Ferrars Lane relining, version 1.0", "Network Operations", "2026-11-16"),
        "jobs": ("Mains flushing contractor's job sheets, 2025-26 programme", "Mains flushing contractor",
                 "2026-04-02"),
        "supply": ("Non-household supply points in Stavenham", "Business Customers", "2026-11-02"),
        "consumption": ("Monthly settled consumption per non-household supply point, April 2025 to October 2026",
                        "Business Customers", "2026-11-02"),
        "amr": ("Hourly consumption from the loggers on large non-household meters (local time)", "Business Customers",
                "2026-11-02"),
        "condition": ("Trunk mains condition assessment 2024", "Asset Management", "2024-09-23"),
        "weather": ("Daily weather at Stavenham (Copt Hill)", "Network Operations", "2026-11-02"),
        "samples": ("Regulatory samples at customer taps, by water supply zone", "Water Quality", "2026-11-02"),
    }
    meta = {
        "task": "task501",
        "title": "Which trunk mains, if any, Lydden Valley Water must flush before the TM107 Ferrars Lane main comes out "
                 "for relining in March 2027, with its 2025-26 flushing water per 100 m by diameter and the re-routed "
                 "districts' non-household water",
        "domain": "Energy Systems & Utilities",
        "subdomain": "asset-condition-maintenance (water distribution trunk mains)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "07 (grid of cells): each trunk main the relining loads with its highest hourly flow during the "
                        "works and whether to flush it, the flushing water per 100 m by diameter and year, and the "
                        "non-household water by re-routed district",
        "as_of": "2026-11-16",
        "deliverables": ["ferrars_lane_flushing_2027.xlsx", "ferrars_lane_flushing_note.pdf"],
        "distractor_files": [PK.FILES[k] for k in PK.DISTRACTORS],
        "input_gates": {"files": len(PK.FILES), "formats": sorted({v.rsplit(".", 1)[1] for v in PK.FILES.values()}),
                        "largest_file": PK.FILES[largest], "largest_file_rows": rows[largest]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task501/generator/build.py (seeded, deterministic) around "
                               "a fictional water-only company (Lydden Valley Water) and town (Stavenham); no real "
                               "person, customer, company or asset is depicted.",
                     "date": "2026-11-16", "license": "CC0-1.0 (original work)"}],
        "provenance": [],
    }
    for k, fn in PK.FILES.items():
        cov, by, asof = prov[k]
        e = {"file": fn, "covers": cov, "issued_by": by, "as_of": asof, "license": "CC0-1.0 (original work)"}
        if rows.get(k):
            e["rows"] = rows[k]
        meta["provenance"].append(e)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")


def build(target, golden_dir, figures_path):
    os.makedirs(golden_dir, exist_ok=True)
    res = compute(target)
    figs = figures(res)
    write_xlsx(os.path.join(golden_dir, "ferrars_lane_flushing_2027.xlsx"), res, figs)
    write_note(os.path.join(golden_dir, "ferrars_lane_flushing_note.pdf"), res, figs)
    with open(figures_path, "w", encoding="utf-8") as fh:
        json.dump(figs, fh, indent=2)
        fh.write("\n")
    return res, figs
