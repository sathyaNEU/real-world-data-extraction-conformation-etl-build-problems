"""The golden deliverables from the world's clean truth: eu_p1_2026_aq117.xlsx (the District's AQ-117 form for EU-P1's
four quarters, the month-by-month record behind it and the 2026 solvent deliveries) and eu_p1_2026_determination.docx,
plus generator/figures.json, every figure the write-up and the deliverables state."""
import datetime as dt
import json
import os

import numpy as np

import pack as P
import world as W

GOLD_XLSX = "eu_p1_2026_aq117.xlsx"
GOLD_DOCX = "eu_p1_2026_determination.docx"
SOLVENT_ORDER = ["methanol", "toluene", "isopropanol", "ethyl acetate", "n-heptane", "isohexane", "tetrahydrofuran"]
SOLVENT_NAME = {"methanol": "Methanol", "toluene": "Toluene", "isopropanol": "Isopropanol",
                "ethyl acetate": "Ethyl acetate", "n-heptane": "n-Heptane", "isohexane": "Isohexane",
                "tetrahydrofuran": "Tetrahydrofuran"}
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]


def r1(x):
    return "%.1f" % (round(x + 1e-12, 1))


def r100(x):
    return "{:,}".format(int(round(x / 100.0)) * 100)


def components(w, fan=W.FAN_MAX, dre=W.DRE):
    """Pounds per EST minute of 2026: VOC vented, released at PSV-31, vented while RTO-1 was not running, emitted at
    S-1 after RTO-1, emitted in all."""
    run = w.status == "RUN"
    voc, flow = w.voc_min, w.flow
    cap = np.where(flow > fan, fan / np.maximum(flow, 1e-9), 1.0)
    psv = np.where(run, voc * (1 - cap), 0.0)
    stack = np.where(run, voc * cap * (1 - dre), 0.0)
    off = np.where(run, 0.0, voc)
    return dict(vented=voc, psv=psv, offline=off, stack=stack, emitted=psv + stack + off,
                over=(run & (flow > fan)).astype(float))


def by_month(c):
    out = []
    for m in range(1, 13):
        a, b = W.month_start(m), W.month_start(m + 1)
        out.append({k: float(v[a:b].sum()) for k, v in c.items()})
    return out


def deliveries_2026(w):
    """Each delivery once, at the supplier's delivery date (plant local), in pounds."""
    rows = []
    for d in w.deliveries:
        day = P.local_dt(d["t"]).date()
        lb = d["gal"] * W.DENSITY_LB_GAL[d["solvent"]] if d["mode"] == "bulk" else d["kg"] * W.LB_PER_KG
        rows.append((day, d["solvent"], d["mode"], d["gal"] if d["mode"] == "bulk" else d["kg"], lb))
    return [r for r in rows if r[0].year == 2026]


def ask_figures(w):
    rows = deliveries_2026(w)
    by_s = {s: sum(r[4] for r in rows if r[1] == s) for s in SOLVENT_ORDER}
    by_q = [sum(r[4] for r in rows if (r[0].month - 1) // 3 == q) for q in range(4)]
    qty = {s: (sum(r[3] for r in rows if r[1] == s and r[2] == "bulk"),
               sum(r[3] for r in rows if r[1] == s and r[2] != "bulk")) for s in SOLVENT_ORDER}
    return by_s, by_q, qty


def figures(w):
    c = components(w)
    mon = by_month(c)
    q_lb = [sum(mon[m][k] for m in range(3 * q, 3 * q + 3)) for q in range(4) for k in ("emitted",)]
    q_t = [x / 2000 for x in q_lb]
    total = sum(q_lb) / 2000
    ytd = list(np.cumsum(q_t))
    default_q, default_y = W.emitted(w, "default", 1)
    hourly_q, hourly_y = W.emitted(w, "golden", 60)
    by_s, by_q, qty = ask_figures(w)
    tot = {k: sum(m[k] for m in mon) for k in mon[0]}
    fig = {
        "call": {"verdict": "over", "total_tons": r1(total), "limit_tons": "2.5", "margin_tons": r1(total - W.LIMIT_TONS),
                 "fan_scfm": "3,800", "dre_pct": "99.4", "std_temp_f": "68", "lb_per_kg": "2.20462", "year": "2026",
                 "rounding_lb": "100"},
        "quarters": {"Q%d" % (q + 1): {"tons": r1(q_t[q]), "ytd_tons": r1(ytd[q])} for q in range(4)},
        "months_lb": {MONTHS[m]: {k: int(round(mon[m][k])) for k in ("vented", "psv", "offline", "stack", "emitted")}
                      for m in range(12)},
        "capture": {"minutes_over_fan": int(tot["over"]), "psv31_lb": "{:,}".format(int(round(tot["psv"] / 100.0)) * 100),
                    "vented_tons": "%.1f" % (tot["vented"] / 2000), "offline_lb": "{:,}".format(int(round(tot["offline"]))),
                    "stack_lb": "{:,}".format(int(round(tot["stack"])))},
        "default_path": {"tons": r1(default_y / 2000)},
        "hourly_check": {"tons": r1(hourly_y / 2000)},
        "ask_a": {"Q%d" % (q + 1): r100(by_q[q]) for q in range(4)},
        "ask_b": {SOLVENT_NAME[s]: r100(by_s[s]) for s in SOLVENT_ORDER},
        "raw": {"total_tons": round(total, 4), "quarters_tons": [round(x, 4) for x in q_t],
                "ytd_tons": [round(x, 4) for x in ytd], "default_tons": round(default_y / 2000, 4),
                "hourly_tons": round(hourly_y / 2000, 4), "psv31_lb": round(tot["psv"], 2),
                "ask_a_lb": [round(x, 2) for x in by_q], "ask_b_lb": {SOLVENT_NAME[s]: round(by_s[s], 2) for s in SOLVENT_ORDER},
                "qty": {SOLVENT_NAME[s]: [round(qty[s][0], 1), round(qty[s][1], 1)] for s in SOLVENT_ORDER}},
    }
    return fig, mon


def write_xlsx(path, fig, mon):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = openpyxl.Workbook()
    thin = Side(style="thin", color="9AA3AB")
    box = Border(left=thin, right=thin, top=thin, bottom=thin)
    head = PatternFill("solid", fgColor="DDE3EA")
    ws = wb.active
    ws.title = "AQ-117"
    ws["A1"] = "Chalmont County Air Quality District"
    ws["A2"] = "Form AQ-117  Quarterly Emission Unit Report (Rev. 2023-01)"
    ws["A1"].font = ws["A2"].font = Font(bold=True)
    for i, (a, b) in enumerate([("Permittee", P.COMPANY + ", Harwick plant"), ("Permit No.", "PTO-2219-0447 R3"),
                                ("Emission unit", "EU-P1 process vents (CVS-1 to RTO-1)"), ("Pollutant", "VOC"),
                                ("Calendar year", 2026)], 4):
        ws.cell(row=i, column=1, value=a)
        ws.cell(row=i, column=2, value=b)
    hdr = ["Quarter", "Emitted this quarter (tons)", "Calendar year to date (tons)", "Calendar-year limit (tons)"]
    for j, h in enumerate(hdr, 1):
        c = ws.cell(row=10, column=j, value=h)
        c.font, c.fill, c.border = Font(bold=True), head, box
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for q, lab in enumerate(["Q1 (Jan-Mar)", "Q2 (Apr-Jun)", "Q3 (Jul-Sep)", "Q4 (Oct-Dec)"]):
        k = "Q%d" % (q + 1)
        vals = [lab, float(fig["quarters"][k]["tons"]), float(fig["quarters"][k]["ytd_tons"]), 2.5]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=11 + q, column=j, value=v)
            c.border = box
            if j > 1:
                c.number_format = "0.0"
    ws.cell(row=16, column=1, value="Certified true, accurate and complete (responsible official):")
    ws.cell(row=17, column=1, value="Name / title / date")
    for col, wdt in zip("ABCD", (34, 28, 28, 26)):
        ws.column_dimensions[col].width = wdt

    wm = wb.create_sheet("EU-P1 by month")
    cols = ["Month (2026, local time)", "VOC vented to CVS-1 (lb)", "Released at PSV-31 (lb)",
            "Vented while RTO-1 not in RUN (lb)", "Emitted at S-1 after RTO-1 (lb)", "VOC emitted (lb)"]
    for j, h in enumerate(cols, 1):
        c = wm.cell(row=1, column=j, value=h)
        c.font, c.fill, c.border = Font(bold=True), head, box
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for m in range(12):
        v = fig["months_lb"][MONTHS[m]]
        for j, x in enumerate([MONTHS[m], v["vented"], v["psv"], v["offline"], v["stack"], v["emitted"]], 1):
            c = wm.cell(row=2 + m, column=j, value=x)
            c.border = box
            if j > 1:
                c.number_format = "#,##0"
    wm.cell(row=14, column=1, value="2026").font = Font(bold=True)
    for j, k in enumerate(["vented", "psv", "offline", "stack", "emitted"], 2):
        c = wm.cell(row=14, column=j, value=int(round(sum(mon[m][k] for m in range(12)))))
        c.font, c.number_format, c.border = Font(bold=True), "#,##0", box
    wm.cell(row=16, column=1, value="Capture taken minute by minute as RTO-1's 3,800 scfm maximum draw over the header's "
                                   "summed vent flow; VOC above the draw released untreated at PSV-31. Destruction "
                                   "99.4 per cent (test BST-25-0418).")
    for col, wdt in zip("ABCDEF", (24, 18, 18, 20, 20, 16)):
        wm.column_dimensions[col].width = wdt
    wm.freeze_panes = "B2"

    wsd = wb.create_sheet("Solvent deliveries 2026")
    for j, h in enumerate(["Solvent", "Bulk (net US gal at 60 F)", "Drums and totes (net kg)", "Delivered (lb)"], 1):
        c = wsd.cell(row=1, column=j, value=h)
        c.font, c.fill, c.border = Font(bold=True), head, box
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, s in enumerate(SOLVENT_ORDER, 2):
        g, k = fig["raw"]["qty"][SOLVENT_NAME[s]]
        vals = [SOLVENT_NAME[s], g or None, k or None, int(fig["ask_b"][SOLVENT_NAME[s]].replace(",", ""))]
        for j, v in enumerate(vals, 1):
            c = wsd.cell(row=i, column=j, value=v)
            c.border = box
            if j in (2, 3):
                c.number_format = "#,##0.0"
            if j == 4:
                c.number_format = "#,##0"
    r = 11
    for j, h in enumerate(["Quarter (delivery date)", "All solvents delivered (lb)"], 1):
        c = wsd.cell(row=r, column=j, value=h)
        c.font, c.fill, c.border = Font(bold=True), head, box
    for q in range(4):
        c1 = wsd.cell(row=r + 1 + q, column=1, value="Q%d 2026" % (q + 1))
        c2 = wsd.cell(row=r + 1 + q, column=2, value=int(fig["ask_a"]["Q%d" % (q + 1)].replace(",", "")))
        c1.border = c2.border = box
        c2.number_format = "#,##0"
    wsd.cell(row=17, column=1, value="Each delivery counted once at the supplier's delivery date; pounds from net gallons "
                                     "at the material master's density, kilograms at 2.20462 lb/kg; rounded to the "
                                     "nearest 100 lb.")
    for col, wdt in zip("ABCD", (24, 22, 22, 16)):
        wsd.column_dimensions[col].width = wdt
    wsd.freeze_panes = "A2"
    wb_ = wb.create_sheet("Basis")
    basis = [("Records", "Batchwise 4 batch steps to the 1 July 2026 cutover; Orbitas process operations from the cutover "
                         "(exported 5 January 2027); vent calculation basis Rev 7; RTO-1 DAHS one-minute record "
                         "(exported 5 January 2027); CVS-1 register Rev 4"),
             ("Unit", "EU-P1: reactors R-101 to R-106 with their manway exhaust, dryers D-201 and D-202, still SR-301 "
                      "(permit Section A). EU-T1, EU-F1, EU-B1 and EU-G1 are reported separately."),
             ("Definitions", "Permit D.1: a ton is 2,000 lb; emitted means released to the atmosphere; standard "
                             "conditions 68 F and 29.92 in Hg; quarters in plant local time."),
             ("Destruction", "99.4 per cent, test BST-25-0418 (May 2025), accepted 7 July 2025 (permit B.4)."),
             ("Capture", "Header flow summed minute by minute from the steps in progress; above RTO-1's 3,800 scfm the "
                         "excess leaves at PSV-31 as mixed header gas. XV-30 is open whenever RTO-1 is not in RUN."),
             ("Rounding", "Quarters summed unrounded; tons to one decimal on the form, pounds to the nearest 100 on the "
                          "deliveries sheet.")]
    for i, (a, b) in enumerate(basis, 1):
        wb_.cell(row=i, column=1, value=a).font = Font(bold=True)
        wb_.cell(row=i, column=2, value=b).alignment = Alignment(wrap_text=True, vertical="top")
    wb_.column_dimensions["A"].width = 14
    wb_.column_dimensions["B"].width = 100
    wb.save(path)


def write_docx(path, fig, mon):
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    t = d.add_paragraph()
    run = t.add_run("Pellston Fine Chemicals, LLC, Harwick plant")
    run.bold = True
    d.add_paragraph("EU-P1 process vents: calendar 2026 VOC against permit PTO-2219-0447 R3, condition B.1")
    d.add_paragraph("To: file PTO-2219-0447. From: Alyssa Alexander, Environmental. 29 January 2027")
    c = fig["call"]
    d.add_heading("EU-P1 exceeded its 2026 VOC limit", level=1)
    d.add_paragraph("EU-P1 emitted %s tons of VOC in calendar 2026, over its 2.5-ton calendar-year limit by %s tons."
                    % (c["total_tons"], c["margin_tons"]))
    d.add_heading("Basis", level=2)
    d.add_paragraph(
        "Batch step records from Batchwise 4 (January to the 1 July cutover, plant local time) and Orbitas (from the "
        "cutover, UTC, with the in-flight batches' migrated history taken once) were placed on one clock, and each step "
        "took its vent flow and VOC rate from vent calculation basis Rev 7, the PX line's Nm3/h and kg/h converted to "
        "scfm at 68 F and to lb/hr. RTO-1's mode came from the DAHS one-minute record, kept in Eastern Standard Time.")
    d.add_paragraph(
        "The nine vents share header HDR-1 to RTO-1, whose fan draws at most %s scfm. Summed minute by minute, the "
        "vents' flow went above that in short spells through the year, mostly while both dryers were drying and a "
        "reactor was charging solids. The gas above the fan's draw lifts PSV-31 at the oxidizer inlet to atmosphere, so "
        "that share of each minute's VOC left untreated, about %s lb in the year. The rest reaching RTO-1 was destroyed "
        "at the 99.4 per cent demonstrated in test BST-25-0418, and VOC vented while RTO-1 was not in RUN went to "
        "atmosphere through the bypass." % (c["fan_scfm"], fig["capture"]["psv31_lb"]))
    d.add_paragraph(
        "Taking every vented pound as reaching RTO-1 would give %s tons, and checking the fan against hourly average "
        "header flow %s tons; both understate the release, because the coincidences last minutes, not hours."
        % (fig["default_path"]["tons"], fig["hourly_check"]["tons"]))
    d.add_heading("Quarters (AQ-117)", level=2)
    tb = d.add_table(rows=1, cols=3)
    tb.style = "Table Grid"
    for j, h in enumerate(["Quarter", "Emitted (tons)", "Calendar year to date (tons)"]):
        tb.rows[0].cells[j].text = h
    for q in range(4):
        k = "Q%d" % (q + 1)
        row = tb.add_row().cells
        row[0].text = k + " 2026"
        row[1].text = fig["quarters"][k]["tons"]
        row[2].text = fig["quarters"][k]["ytd_tons"]
    for row in tb.rows:
        for cell in row.cells[1:]:
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    src = d.add_paragraph("Source: eu_p1_2026_aq117.xlsx, sheets AQ-117 and EU-P1 by month.")
    src.runs[0].font.size = Pt(8.5)
    d.add_paragraph("The 2026 solvent deliveries are in the same workbook, sheet Solvent deliveries 2026, each delivery "
                    "at the supplier's delivery date.")
    note = d.add_paragraph("Note: quarters are counted in plant local time (permit D.1). The DAHS keeps Eastern Standard "
                           "Time all year, so from 8 March to 1 November each DAHS minute sits an hour later on the plant clock.")
    note.runs[0].font.size = Pt(8.5)
    d.save(path)


def main(w, gdir, fig_path):
    import postprocess as PP
    os.makedirs(gdir, exist_ok=True)
    fig, mon = figures(w)
    xp, dp = os.path.join(gdir, GOLD_XLSX), os.path.join(gdir, GOLD_DOCX)
    write_xlsx(xp, fig, mon)
    PP.normalize_ooxml(xp, "Alyssa Alexander", "Alyssa Alexander", "2027-01-28T15:05:00Z", "2027-01-29T23:40:00Z",
                       excel=True, company=P.COMPANY)
    write_docx(dp, fig, mon)
    PP.normalize_ooxml(dp, "Alyssa Alexander", "Alyssa Alexander", "2027-01-28T16:20:00Z", "2027-01-29T23:52:00Z",
                       company=P.COMPANY)
    with open(fig_path, "w", encoding="utf-8") as fh:
        json.dump(fig, fh, indent=1)
        fh.write("\n")
    return fig
