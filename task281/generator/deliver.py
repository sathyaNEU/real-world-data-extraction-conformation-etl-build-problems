"""The golden deliverables and figures.json, computed from target/ alone through analysis.py.

    ai_operating_points_2027.xlsx   the 2027 points, their referrals, the reading center reads, camera faults
    operating_points_2027_committee.pptx  the Committee slide: the call and the heatmap of each clinic's
                                          estimated sensitivity at every vendor point, its point outlined
"""
import datetime as dt
import json
import os
import zipfile

import analysis as A

BOOK = "ai_operating_points_2027.xlsx"
BRIEF = "operating_points_2027_committee.pptx"
STAMP = (2026, 11, 16, 16, 40, 0)
NAMES = {"OF": "Orrin Falls", "TB": "Thistlebrook", "WM": "Wendmere", "PB": "Pellsbury", "QH": "Quarry Hill",
         "RW": "Rookwood", "SC": "Sallow Creek", "VD": "Veldane", "BF": "Brackenfield", "YB": "Yarrowby",
         "KN": "Kestle Road", "HM": "Hollinmoor"}


def rnd(x, nd=0):
    """Half-up rounding, the way the workbook and the write-up state figures."""
    from decimal import Decimal, ROUND_HALF_UP
    q = Decimal(1).scaleb(-nd)
    return float(Decimal(repr(x)).quantize(q, rounding=ROUND_HALF_UP)) if nd else int(
        Decimal(repr(x)).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def figures(P, G):
    L = G["ladder"]
    order = sorted(P.codes, key=lambda c: NAMES[c])
    cut = dict(P.ops)
    per = {c: 0 for c in P.codes}
    for s in P.screens():
        nm = G["picks"][s["code"]]
        if s["ung"] or (s["score"] is not None and s["score"] >= cut[nm]):
            per[s["code"]] += 1
    f = {
        "points": {NAMES[c]: G["picks"][c] for c in order},
        "referrals_by_clinic": {NAMES[c]: per[c] for c in order},
        "referrals_total": G["referrals"],
        "capacity": P.capacity,
        "headroom": P.capacity - G["referrals"],
        "sensitivity_at_point_pct": {NAMES[c]: rnd(100 * L["golden"][c][0][G["picks"][c]]) for c in order},
        "grid_pct": {NAMES[c]: {nm: rnd(100 * L["golden"][c][0][nm]) for nm, _ in P.ops} for c in order},
        "nr40_share_pct": {NAMES[c]: rnd(100 * L["golden"][c][2].get("NR-40", 0.0)) for c in order},
        "validation_by_model_pct": {m: {nm: rnd(100 * v, 1) for nm, v in d.items()} for m, d in L["by_model"].items()},
        "validation_counts": {m: {"screened": n, "referable": k} for m, (n, k) in L["counts"].items()},
        "pooled_pct": {nm: rnd(100 * v, 1) for nm, v in L["pooled"][P.codes[0]][0].items()},
        "rung_picks": {r: {NAMES[c]: L[r][c][1] for c in order} for r in ("pooled", "casemix", "worst_subgroup",
                                                                           "snapshot")},
        "rung_referrals": {r: A.referrals(P, {c: L[r][c][1] for c in P.codes})
                           for r in ("pooled", "casemix", "worst_subgroup", "snapshot")},
        "reads_by_clinic": {NAMES[c]: G["overreads_clinic"][c][0] for c in order},
        "confirmed_pct_by_clinic": {NAMES[c]: rnd(100 * G["overreads_clinic"][c][1]) for c in order},
        "days_by_quarter": {q: rnd(v, 1) for q, v in G["overreads_quarter"].items()},
        "floor_pct": rnd(100 * P.floor),
    }
    dt_ = G["downtime"]
    f["downtime"] = {"%s, fault reported %s" % (NAMES[v["clinic"]], v["opened"].isoformat()): v["days"]
                     for k, v in dt_.items()}
    f["referrals_high_everywhere"] = A.referrals(P, {c: "High" for c in P.codes})
    f["referrals_enhanced_everywhere"] = A.referrals(P, {c: "Enhanced" for c in P.codes})
    return f, order, per


def workbook(P, G, f, order, per, path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    L = G["ladder"]
    wb = Workbook()
    bold = Font(bold=True)
    head_fill = PatternFill("solid", fgColor="DCE6F1")
    thin = Side(style="thin", color="A6A6A6")

    def header(ws, row, vals):
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=row, column=j, value=v)
            c.font = bold
            c.fill = head_fill
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.border = Border(bottom=thin)

    ws = wb.active
    ws.title = "2027 points"
    ws["A1"] = "RetinaCheck operating points for contract year 2027 (CAI-03 v3, section 3)"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Sensitivity for referable DR estimated on each clinic's Oct 2025 to Sep 2026 screenings; floor 85%."
    cols = ["Clinic", "2027 point", "Est. sensitivity at point", "Referrals implied (2025-26 screenings)",
            "Share of screenings on NR-40 camera"] + ["Est. sensitivity, %s" % nm for nm, _ in P.ops]
    header(ws, 4, cols)
    r = 5
    for c in order:
        cells = L["golden"][c][0]
        ws.cell(row=r, column=1, value=NAMES[c])
        ws.cell(row=r, column=2, value=G["picks"][c])
        ws.cell(row=r, column=3, value=round(cells[G["picks"][c]], 4)).number_format = "0%"
        ws.cell(row=r, column=4, value=per[c]).number_format = "#,##0"
        ws.cell(row=r, column=5, value=round(L["golden"][c][2].get("NR-40", 0.0), 4)).number_format = "0%"
        for j, (nm, _) in enumerate(P.ops):
            ws.cell(row=r, column=6 + j, value=round(cells[nm], 4)).number_format = "0%"
        r += 1
    ws.cell(row=r, column=1, value="Network").font = bold
    ws.cell(row=r, column=4, value=G["referrals"]).number_format = "#,##0"
    ws.cell(row=r, column=4).font = bold
    r += 1
    ws.cell(row=r, column=1, value="Pellam capacity, 2027")
    ws.cell(row=r, column=4, value=P.capacity).number_format = "#,##0"
    r += 1
    ws.cell(row=r, column=1, value="Headroom")
    ws.cell(row=r, column=4, value=P.capacity - G["referrals"]).number_format = "#,##0"
    r += 2
    ws.cell(row=r, column=1, value="Validation study sensitivity by camera model (camera from the asset register's "
                                   "location history on each image's capture date)").font = bold
    r += 1
    header(ws, r, ["Camera model", "Images", "Referable"] + [nm for nm, _ in P.ops])
    for m in ("NR-40", "NR-70"):
        r += 1
        n, k = L["counts"][m]
        ws.cell(row=r, column=1, value=m)
        ws.cell(row=r, column=2, value=n)
        ws.cell(row=r, column=3, value=k)
        for j, (nm, _) in enumerate(P.ops):
            ws.cell(row=r, column=4 + j, value=round(L["by_model"][m][nm], 4)).number_format = "0.0%"
    for j, wdt in enumerate([16, 11, 13, 17, 15, 13, 13, 13, 13], 1):
        ws.column_dimensions[get_column_letter(j)].width = wdt
    ws.freeze_panes = "B5"

    ws = wb.create_sheet("Reading center 2025-26")
    ws["A1"] = "Pellam reads of the AI's referrals, screenings Oct 2025 to Sep 2026"
    ws["A1"].font = Font(bold=True, size=12)
    header(ws, 3, ["Clinic", "AI referrals read", "Closing grade Referable"])
    r = 4
    for c in order:
        ws.cell(row=r, column=1, value=NAMES[c])
        ws.cell(row=r, column=2, value=G["overreads_clinic"][c][0]).number_format = "#,##0"
        ws.cell(row=r, column=3, value=round(G["overreads_clinic"][c][1], 4)).number_format = "0%"
        r += 1
    r += 1
    header(ws, r, ["Quarter of screening", "Avg days, screening to closing grade"])
    for q, v in G["overreads_quarter"].items():
        r += 1
        ws.cell(row=r, column=1, value=q)
        ws.cell(row=r, column=2, value=round(v, 2)).number_format = "0.0"
    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 18
    ws.column_dimensions["C"].width = 18

    ws = wb.create_sheet("Camera faults 2025-26")
    ws["A1"] = "Camera faults in the reference year (CAI-03 v3, 4.2)"
    ws["A1"].font = Font(bold=True, size=12)
    header(ws, 3, ["Ticket", "Clinic", "Fault reported", "Clinic days with no screening"])
    r = 4
    for k, v in G["downtime"].items():
        ws.cell(row=r, column=1, value=k)
        ws.cell(row=r, column=2, value=NAMES[v["clinic"]])
        ws.cell(row=r, column=3, value=v["opened"]).number_format = "d mmm yyyy"
        ws.cell(row=r, column=4, value=v["days"])
        r += 1
    for col, wdt in zip("ABCD", (11, 16, 15, 16)):
        ws.column_dimensions[col].width = wdt

    ws = wb.create_sheet("Notes")
    notes = [
        ("As of", "16 November 2026; reference year 1 October 2025 to 30 September 2026 (CAI-03 v3, 2.1)"),
        ("Point rule", "Least sensitive vendor point with estimated sensitivity at or above 85% (CAI-03 v3, 3.1)"),
        ("Sensitivity", "Referable DR (moderate NPDR or worse, or DME) referred as Referable or Ungradable, estimated "
                        "per camera model from the 2025 local validation study and weighted by each clinic's "
                        "screenings on each model"),
        ("Camera", "The serial the Biomedical Engineering location history places at the clinic on the capture date"),
        ("Referrals", "Reference-year screenings with an Ungradable result or a DR score at or above the point's "
                      "threshold; capacity per Pellam agreement PERC-CV-2027, 2.1"),
        ("Reading center", "AI referrals are REF7734 referral orders; teleretinal photography reads are excluded; a "
                           "referral closes on its last Referable or Not referable grade (CAI-03 v3, 4.1)"),
        ("Camera faults", "Clinic days after the fault with no AI screening captured, up to the next camera's "
                          "arrival in the location history (CAI-03 v3, 4.2)"),
    ]
    for i, (k, v) in enumerate(notes, 1):
        ws.cell(row=i, column=1, value=k).font = bold
        ws.cell(row=i, column=2, value=v).alignment = Alignment(wrap_text=True, vertical="top")
    ws.column_dimensions["A"].width = 16
    ws.column_dimensions["B"].width = 96
    when = dt.datetime(2026, 11, 16, 15, 2, 0)
    wb.properties.creator = "Quality and Clinical AI"
    wb.properties.lastModifiedBy = "Quality and Clinical AI"
    wb.properties.created = when
    wb.properties.modified = when
    wb.properties.title = "RetinaCheck operating points 2027"
    wb.save(path)
    from pack import normalise_zip
    normalise_zip(path, when="2026-11-16T23:02:00Z")


def chart(P, G, order, path):
    import matplotlib
    matplotlib.use("Agg")
    matplotlib.rcParams["svg.hashsalt"] = "task281"
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    from matplotlib.patches import Rectangle
    L = G["ladder"]
    ops = [nm for nm, _ in P.ops]
    vals = [[100 * L["golden"][c][0][nm] for nm in ops] for c in order]
    cmap = LinearSegmentedColormap.from_list("s", ["#b2182b", "#f4a582", "#f7f7f7", "#92c5de", "#2166ac"])
    fig, ax = plt.subplots(figsize=(7.2, 6.4), dpi=150)
    im = ax.imshow(vals, cmap=cmap, vmin=70, vmax=100, aspect="auto")
    for i, c in enumerate(order):
        for j, nm in enumerate(ops):
            v = vals[i][j]
            ax.text(j, i, "%d%%" % A_round(v), ha="center", va="center", fontsize=9,
                    color="#111111" if 78 < v < 96 else "white")
        j = ops.index(G["picks"][c])
        ax.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, lw=2.4, ec="#111111"))
    ax.set_xticks(range(len(ops)))
    ax.set_xticklabels(["%s\n(DR score %d+)" % (nm, cut) for nm, cut in P.ops], fontsize=9)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([NAMES[c] for c in order], fontsize=9)
    ax.set_title("Five clinics fall below the 85% floor at Standard\n"
                 "Estimated sensitivity for referable DR, Oct 2025 to Sep 2026 screenings\n"
                 "Outlined: each clinic's 2027 point", fontsize=9.5, loc="left")
    cb = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.03)
    cb.set_label("Estimated sensitivity (%); line at the 85% floor", fontsize=8.5)
    cb.ax.axhline(85, color="#111111", lw=1.2)
    cb.ax.tick_params(labelsize=8)
    fig.text(0.01, 0.01, "Network referrals at the 2027 points: %s against Pellam capacity %s." %
             ("{:,}".format(G["referrals"]), "{:,}".format(P.capacity)), fontsize=8)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path, dpi=150, metadata={"Software": None})
    plt.close(fig)


def brief(P, G, f, order, png, path):
    """One slide for the Clinical AI Oversight Committee: the call, the reason and the grid."""
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    s = prs.slides.add_slide(prs.slide_layouts[6])
    std = ", ".join(sorted(k for k, v in f["points"].items() if v == "Standard"))
    vm = f["validation_by_model_pct"]

    def box(x, y, w_, h, paras):
        tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w_), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        for i, (text, size, bold) in enumerate(paras):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            r = p.add_run()
            r.text = text
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.name = "Calibri"
            r.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
            p.space_after = Pt(6)

    box(0.5, 0.35, 12.3, 0.9, [("Standard at seven clinics, Enhanced at two, High at three in 2027", 26, True),
                               ("RetinaCheck operating points for contract year 2027. Clinical AI Oversight Committee, "
                                "December meeting. Quality and Clinical AI.", 12, False)])
    box(0.5, 6.3, 5.6, 0.9, [("Sources: local validation study 2025 (CVCH-QI-2025-01); RetinaCheck result export, "
                              "screenings Oct 2025 to Sep 2026; Biomedical Engineering asset register and location "
                              "history; CAI-03 v3 section 3; Pellam agreement PERC-CV-2027.", 9, False)])
    box(12.6, 7.05, 0.5, 0.3, [("1", 9, False)])
    box(0.5, 1.5, 5.6, 5.6, [
        ("Recommendation", 16, True),
        ("Standard at %s." % std, 13, False),
        ("Enhanced at Kestle Road and Veldane.", 13, False),
        ("High at Brackenfield, Hollinmoor and Rookwood.", 13, False),
        ("On the 2025-26 screenings these points imply %s referrals against Pellam's 2027 capacity of %s." %
         ("{:,}".format(f["referrals_total"]), "{:,}".format(f["capacity"])), 13, False),
        ("Why not Standard everywhere", 16, True),
        ("The validation study pooled images from both camera models. At Standard the AI found %.1f%% of referable "
         "eyes on the NR-40 and %.1f%% on the NR-70. Rookwood, Brackenfield and Hollinmoor screened on an NR-40 all "
         "year; Kestle Road and Veldane have run on NR-40 loaners since February and March." %
         (vm["NR-40"]["Standard"], vm["NR-70"]["Standard"]), 13, False),
    ])
    s.shapes.add_picture(png, Inches(6.35), Inches(1.35), height=Inches(5.95))
    when = dt.datetime(2026, 11, 16, 15, 2, 0)
    cp = prs.core_properties
    cp.author = cp.last_modified_by = "Quality and Clinical AI"
    cp.title = "RetinaCheck operating points 2027"
    cp.created = cp.modified = when
    cp.revision = 3
    prs.save(path)
    from pack import normalise_zip
    normalise_zip(path, when="2026-11-16T23:02:00Z", app="Microsoft Office PowerPoint")


def A_round(v):
    return rnd(v)


def write_all(target, golden_dir, gen_dir):
    os.makedirs(golden_dir, exist_ok=True)
    os.makedirs(gen_dir, exist_ok=True)
    P = A.Pack(target)
    G = A.golden(P)
    f, order, per = figures(P, G)
    workbook(P, G, f, order, per, os.path.join(golden_dir, BOOK))
    png = os.path.join(gen_dir, "sensitivity_grid.png")
    chart(P, G, order, png)
    brief(P, G, f, order, png, os.path.join(golden_dir, BRIEF))
    with open(os.path.join(gen_dir, "figures.json"), "w") as fh:
        json.dump(f, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return P, G, f
