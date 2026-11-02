"""task163 golden deliverables and write-up: the budget workbook, the chart and submission.md, every figure read from
figures.json (never typed)."""
from __future__ import annotations

import os

import common as K
import postprocess as PP

F_BOOK = "reslot_claims_2027.xlsx"
F_DECK = "reslot_review_2027.pptx"


def _money(x):
    return "{:,.2f}".format(x)


def workbook(path, f):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    thin = Side(style="thin", color="B7B7B7")
    head_fill = PatternFill("solid", fgColor="DDE6EA")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Claims 2027"
    r = f["raw"]
    ws["A1"] = "Aubrine mis-pick claims, 2027: shelving re-slot against today's layout"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Uphall. Claims per Schedule 3 (validated, wrong item received); 2027 lines from the demand plan."
    ws["A2"].font = Font(italic=True, size=9, color="555555")
    ws.append([])
    ws.append(["", "Today's layout", "Family re-slot"])
    rows = [
        ("2027 order lines (demand plan)", f["lines_2027"], f["lines_2027"], "#,##0"),
        ("Picks beside a face within 15 g", r["alike_share_cur27"], r["alike_share_plan"], "0.0%"),
        ("Mis-pick claims, 2027", K.round_to(r["cur_claims"], 10), f["call_plan_claims"], "#,##0"),
        ("Claims per 10,000 order lines", f["call_cur_per_10k"], f["call_plan_per_10k"], "0.0"),
        ("Schedule 3 limit per 10,000 lines", K.KPI_PER_10K, K.KPI_PER_10K, "0.0"),
        ("Within the limit", "Yes" if f["call_cur_per_10k"] <= K.KPI_PER_10K else "No",
         "Yes" if f["call_plan_per_10k"] <= K.KPI_PER_10K else "No", None),
    ]
    for label, a, b, fmt in rows:
        ws.append([label, a, b])
        if fmt:
            ws.cell(ws.max_row, 2).number_format = fmt
            ws.cell(ws.max_row, 3).number_format = fmt
    ws.append([])
    ws.append(["Basis: the 52 weeks to 20 September 2026 on today's faces"])
    ws.cell(ws.max_row, 1).font = Font(bold=True)
    basis = [
        ("Validated wrong-item claims", f["base_claims"], "#,##0"),
        ("Order lines picked", f["base_lines"], "#,##0"),
        ("Claims per 10,000 order lines", f["base_per_10k"], "0.00"),
        ("Picks beside a face within 15 g", r["alike_share_base"], "0.0%"),
        ("Claims per 10,000 picks beside a face within 15 g", f["claims_per_10k_alike"], "0.00"),
    ]
    for label, v, fmt in basis:
        ws.append([label, v])
        ws.cell(ws.max_row, 2).number_format = fmt
    for row in ws.iter_rows(min_row=4, max_row=4):
        for c in row:
            c.font = Font(bold=True)
            c.fill = head_fill
            c.border = Border(bottom=thin)
    ws.column_dimensions["A"].width = 50
    ws.column_dimensions["B"].width = 16
    ws.column_dimensions["C"].width = 16

    ws2 = wb.create_sheet("Agency hour")
    ws2.append(["Corsley agency hours worked, by the month each shift started"])
    ws2["A1"].font = Font(bold=True, size=12)
    ws2.append(["Month", "Hours worked", "Billed at base rates (GBP)", "Night and Sunday premiums (GBP)",
                "Cost per hour worked (GBP)"])
    for c in ws2[2]:
        c.font = Font(bold=True)
        c.fill = head_fill
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for m in K.ASK_A_MONTHS:
        key = "%d-%02d" % m
        d = f["ask_a_detail"][key]
        ws2.append(["%s %d" % (K.MON3[m[1]], m[0]), d["hours"], d["base"], d["premium"], f["ask_a"][key]])
        row = ws2.max_row
        ws2.cell(row, 2).number_format = "#,##0.00"
        ws2.cell(row, 3).number_format = "#,##0.00"
        ws2.cell(row, 4).number_format = "#,##0.00"
        ws2.cell(row, 5).number_format = "0.00"
    ws2.append([])
    ws2.append(["Premiums: each reconciliation line covers the pay period ending the Sunday nine days before its "
                "invoice, at GBP %.2f per night hour and GBP %.2f per Sunday hour."
                % (f["ask_a_uplifts"]["u_night"], f["ask_a_uplifts"]["u_sunday"])])
    ws2.cell(ws2.max_row, 1).font = Font(italic=True, size=9, color="555555")
    for col, wd in zip("ABCDE", (12, 14, 18, 20, 16)):
        ws2.column_dimensions[col].width = wd
    ws2.row_dimensions[2].height = 30

    ws3 = wb.create_sheet("Returned stock")
    ws3.append(["Units graded at the returns bench, October 2025 to September 2026"])
    ws3["A1"].font = Font(bold=True, size=12)
    ws3.append(["Family", "Units graded", "Repacked", "Scrapped", "Stock value scrapped (GBP)"])
    for c in ws3[2]:
        c.font = Font(bold=True)
        c.fill = head_fill
    for fam in ["Make-up", "Skincare", "Fragrance", "Haircare", "Bath and body"]:
        v = f["ask_b"][fam]
        ws3.append([fam, v["units"], v["repack_pct"] / 100.0, v["scrap_pct"] / 100.0, v["scrap_value"]])
        row = ws3.max_row
        ws3.cell(row, 2).number_format = "#,##0"
        ws3.cell(row, 3).number_format = "0.0%"
        ws3.cell(row, 4).number_format = "0.0%"
        ws3.cell(row, 5).number_format = "#,##0"
    tot_units = sum(f["ask_b"][x]["units"] for x in f["ask_b"])
    tot_val = sum(f["ask_b_raw"][x]["scrap_value"] for x in f["ask_b_raw"])
    ws3.append(["All families", tot_units, None, None, int(K.round_half_up(tot_val, 0))])
    ws3.cell(ws3.max_row, 2).number_format = "#,##0"
    ws3.cell(ws3.max_row, 5).number_format = "#,##0"
    for c in ws3[ws3.max_row]:
        c.font = Font(bold=True)
        c.border = Border(top=thin)
    ws3.append([])
    ws3.append(["Grades 2 and 3 read as repack and scrap on bench sheets, as scrap and repack on the handheld from "
                "8 June 2026 (the reading under which Ravelrig's invoices reproduce at one set of prices)."])
    ws3.cell(ws3.max_row, 1).font = Font(italic=True, size=9, color="555555")
    for col, wd in zip("ABCDE", (16, 14, 11, 11, 24)):
        ws3.column_dimensions[col].width = wd
    ws4 = wb.create_sheet("Notes")
    notes = [
        ("Prepared", "30 October 2026, Uphall quality"),
        ("Claims", "Validated claims that a parcel held a product other than the one ordered, counted against the "
                   "line's despatch date (Schedule 3, 3.2). Duplicates, rejected and open claims excluded."),
        ("History", "The 52 weeks 22 September 2025 to 20 September 2026 (ISO weeks 2025-W39 to 2026-W38); claims "
                    "for those despatches were all closed by the extract of 30 October 2026."),
        ("Check-weigh", "PB-SOP-02: a parcel more than 15 g over or under its expected weight is held. A face counts "
                        "as beside an item when it is the next face left or right on the same shelf."),
        ("2027", "Order lines and faces from the slotting plan approved 14 October 2026 (Aubrine demand plan of "
                 "12 October 2026). Today's layout is the location master as at 30 October 2026."),
        ("Agency", "Corsley invoices; a shift counts in the month it started; premiums net of VAT."),
        ("Returns", "Each return at its latest grade, October 2025 to September 2026; stock value at item master "
                    "standard cost."),
        ("Rounding", "Claims to the nearest 100; claims per 10,000 lines and shares to one decimal; hour costs to "
                     "the penny; stock values to the pound."),
    ]
    for k, v in notes:
        ws4.append([k, v])
        ws4.cell(ws4.max_row, 1).font = Font(bold=True)
        ws4.cell(ws4.max_row, 2).alignment = Alignment(wrap_text=True, vertical="top")
    ws4.column_dimensions["A"].width = 14
    ws4.column_dimensions["B"].width = 110
    for ws_ in (ws2, ws3):
        ws_.freeze_panes = "A3"
    wb.save(path)
    PP.normalize_ooxml(path, K.PEOPLE["quality"], K.PEOPLE["quality"], "2026-10-30T14:05:00Z", "2026-10-30T17:48:00Z",
                       title="Aubrine re-slot claims budget 2027", excel=True)


def chart(path, f):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "svg.hashsalt": "task163"})
    fig, ax = plt.subplots(figsize=(7.6, 4.4), dpi=110)
    labels = ["2026 actual\n(52 weeks to 20 Sep)", "2027\ntoday's layout", "2027\nfamily re-slot"]
    vals = [f["raw"]["base_per_10k"], f["raw"]["cur_per_10k"], f["raw"]["plan_per_10k"]]
    shown = [K.round_half_up(v, 1) for v in vals]
    colours = ["#8C9BA5", "#5B7F95", "#B5533C"]
    bars = ax.bar(labels, vals, color=colours, width=0.56)
    for b, s in zip(bars, shown):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.06, "%.1f" % s, ha="center", va="bottom",
                fontsize=11, fontweight="bold")
    ax.axhline(K.KPI_PER_10K, color="#333333", linestyle="--", linewidth=1.2)
    ax.text(-0.42, K.KPI_PER_10K + 0.06, "Schedule 3 limit %.1f" % K.KPI_PER_10K, ha="left", fontsize=9)
    ax.set_ylabel("Mis-pick claims per 10,000 order lines")
    ax.set_ylim(0, max(vals) * 1.22)
    ax.set_title("Aubrine mis-pick claims per 10,000 order lines", fontsize=11, loc="left")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.text(0.01, 0.01, "2027 on the demand plan of 12 Oct 2026; claims per pick beside a face within 15 g held at "
             "the 2026 rate.", fontsize=7.5, color="#555555")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(path, format="png", metadata={"Software": None})
    plt.close(fig)


def deck(path, f):
    """One slide for the account review: the call in the title, the chart beneath it."""
    import io
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    buf = io.BytesIO()
    chart(buf, f)
    buf.seek(0)
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    s = prs.slides.add_slide(prs.slide_layouts[5])
    title = s.shapes.title
    title.text = ("Hold the family re-slot as drawn: %.1f claims per 10,000 lines in 2027 against the limit of %.1f"
                  % (f["call_plan_per_10k"], K.KPI_PER_10K))
    title.left, title.top, title.width, title.height = Inches(0.6), Inches(0.35), Inches(12.1), Inches(1.1)
    for p in title.text_frame.paragraphs:
        for r in p.runs:
            r.font.size = Pt(26)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0x22, 0x2B, 0x33)
    s.shapes.add_picture(buf, Inches(0.8), Inches(1.6), height=Inches(5.0))
    box = s.shapes.add_textbox(Inches(9.55), Inches(2.0), Inches(3.4), Inches(4.4))
    tf = box.text_frame
    tf.word_wrap = True
    pts = [
        "About %s mis-pick claims on 2027's lines under the re-slot; today's layout stays at %.1f per 10,000."
        % ("{:,}".format(f["call_plan_claims"]), f["call_cur_per_10k"]),
        "Parcels are check-weighed to 15 g: a wrong item gets through only when it weighs within 15 g of the one "
        "ordered.",
        "The re-slot puts each line's shades side by side: %.1f%% of 2027 picks would sit beside such a face, "
        "against %.1f%% now." % (f["alike_share_plan_pct"], f["alike_share_base_pct"]),
    ]
    for k, t in enumerate(pts):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        p.text = t
        p.space_after = Pt(10)
        for r in p.runs:
            r.font.size = Pt(15)
            r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    src = s.shapes.add_textbox(Inches(0.6), Inches(6.85), Inches(12.1), Inches(0.4))
    src.text_frame.text = ("Source: Aubrine claims register and Uphall WMS exports to 20 September 2026; slotting plan "
                           "approved 14 October 2026; Schedule 3 of the fulfilment agreement; PB-SOP-02.   1")
    for r in src.text_frame.paragraphs[0].runs:
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    prs.save(path)
    PP.normalize_ooxml(path, K.PEOPLE["quality"], K.PEOPLE["quality"], "2026-10-30T15:20:00Z", "2026-10-30T17:55:00Z",
                       title="Aubrine re-slot review")


def submission(path, f):
    a = f["ask_a"]
    b = f["ask_b"]
    r = f["raw"]
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Human Factors & Ergonomics (human reliability assessment).")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Hold the family re-slot as drawn: it would take Aubrine's 2027 mis-pick claims to about %s, %.1f per "
             "10,000 order lines against the Schedule 3 limit of %.1f, where today's layout stays at %.1f.**"
             % ("{:,}".format(f["call_plan_claims"]), f["call_plan_per_10k"], K.KPI_PER_10K, f["call_cur_per_10k"]))
    L.append("Not the 2026 claims per line carried onto 2027 (about %s, inside the limit), which assumes the layout "
             "cannot change what the check-weigh lets through. Not a look-alike multiplier fitted on claims beside "
             "same-line or same-family faces, which reads the claims' clustering as pickers erring more and also "
             "stays inside the limit." % "{:,}".format(f["default_claims"]))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. The baseline is **%s** validated wrong-item claims on **%s** order lines in the %d weeks to 20 "
             "September 2026" % ("{:,}".format(f["base_claims"]), "{:,}".format(f["base_lines"]), f["base_weeks"]))
    L.append("2. **%.1f%%** of those picks sat beside a face whose item weighs within %d g of theirs; on the plan's "
             "faces and 2027 lines **%.1f%%** would" % (f["alike_share_base_pct"], K.TOL_G, f["alike_share_plan_pct"]))
    L.append("3. Claims run at **%.2f** per 10,000 picks beside a face within %d g, the same beside look-alike and "
             "other neighbours" % (f["claims_per_10k_alike"], K.TOL_G))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Counted the validated Wrong item received claims in aubrine_claims_register.xlsx on lines despatched "
             "22 September 2025 to 20 September 2026, as Schedule 3 counts them: %s, on %s lines in pick_velocity_by_week.csv."
             % ("{:,}".format(f["base_claims"]), "{:,}".format(f["base_lines"])))
    L.append("2. Placed each claim's products and each MISPICK hold's items on location_master.csv through "
             "item_master.csv: every wrong item came from the face to the left or right on the same shelf, every "
             "claim's pair weighs within %d g and every hold's pair further apart (pack_bench_procedure.pdf, step 3), "
             "and holds plus claims per line are the same whatever the neighbour." % K.TOL_G)
    L.append("3. Weighted each item's share of neighbours within %d g by its lines: %.1f%% of 2026 picks, %.2f claims "
             "per 10,000 such picks." % (K.TOL_G, f["alike_share_base_pct"], f["claims_per_10k_alike"]))
    L.append("4. Rebuilt the plan's shelves from slotting_plan_2027.xlsx (Faces 2027) with its 2027 forecast lines: "
             "%.1f%% of 2027 picks would sit beside a face within %d g, against %.1f%% on today's faces."
             % (f["alike_share_plan_pct"], K.TOL_G, f["alike_share_cur27_pct"]))
    L.append("5. Carried %.2f per 10,000 onto both layouts: %s claims and %.1f per 10,000 lines under the plan, %.1f "
             "under today's layout, against the limit of %.1f." % (f["claims_per_10k_alike"],
                                                                   "{:,}".format(f["call_plan_claims"]),
                                                                   f["call_plan_per_10k"], f["call_cur_per_10k"],
                                                                   K.KPI_PER_10K))
    L.append("6. In corsley_invoice_lines.csv each Premium reconciliation line is the night hours at GBP %.2f plus the "
             "Sunday hours at GBP %.2f of the four-week pay period ending the Sunday nine days before its invoice; "
             "spread back onto those shifts and added to the hours billed, by the month each shift started, it gives "
             "the cost of an agency hour worked." % (f["ask_a_uplifts"]["u_night"], f["ask_a_uplifts"]["u_sunday"]))
    L.append("7. In returns_grading_log.csv, kept each return's latest grade and read grades 2 and 3 as repack and "
             "scrap on bench sheets and as scrap and repack on the handheld from 8 June 2026, the one reading under "
             "which ravelrig_invoices_2025-26.pdf reproduces at constant prices (GBP %.2f small, GBP %.2f large); "
             "shares and scrapped value at item_master.csv standard cost, by family."
             % tuple(f["ask_b_fit"]["prices"]))
    L.append("8. The plan breaks the limit and today's layout does not, so the re-slot is held as drawn.")
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### reslot_claims_2027.xlsx")
    L.append("")
    L.append("1. Mis-pick claims on 2027's order lines under the family re-slot: %s." % "{:,}".format(f["call_plan_claims"]))
    L.append("2. Claims per 10,000 order lines, 2027: %.1f under the re-slot, %.1f under today's layout; the limit is "
             "%.1f, so the re-slot is over it." % (f["call_plan_per_10k"], f["call_cur_per_10k"], K.KPI_PER_10K))
    L.append("3. Cost of an agency hour worked, by month (GBP):")
    for m in K.ASK_A_MONTHS:
        L.append("   - %s %d: %s" % (K.MONTH_NAMES[m[1]], m[0], "%.2f" % a["%d-%02d" % m]))
    L.append("4. Returned units, October 2025 to September 2026, by family:")
    for fam in ["Make-up", "Skincare", "Fragrance", "Haircare", "Bath and body"]:
        v = b[fam]
        L.append("   - %s: repacked %.1f%%, scrapped %.1f%%, stock value scrapped GBP %s"
                 % (fam, v["repack_pct"], v["scrap_pct"], "{:,}".format(v["scrap_value"])))
    L.append("")
    L.append("### reslot_review_2027.pptx")
    L.append("")
    L.append("1. One slide, the call in its title, with a bar chart of claims per 10,000 order lines: the actual for the "
             "52 weeks at %.1f, today's layout at %.1f and the family re-slot at %.1f for the coming year, and the "
             "Schedule 3 limit of %.1f as a dashed line."
             % (K.round_half_up(r["base_per_10k"], 1), f["call_cur_per_10k"], f["call_plan_per_10k"], K.KPI_PER_10K))
    L.append("")
    with open(path, "w") as fh:
        fh.write("\n".join(L))


def write_all(out, f, task_dir=None):
    os.makedirs(out, exist_ok=True)
    workbook(os.path.join(out, F_BOOK), f)
    deck(os.path.join(out, F_DECK), f)
    if task_dir:
        submission(os.path.join(task_dir, "submission.md"), f)
