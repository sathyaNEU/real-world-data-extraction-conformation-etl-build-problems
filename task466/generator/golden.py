"""The golden deliverables, built from the analysis of target/ alone: the committee brief (PDF with its chart) and
the methane return workbook."""
import datetime as dt
import io
import os

import analysis as A
import common as C

MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def round_to(v, unit):
    return int(unit * round(v / unit))


def compute(target):
    r = A.compute(target)
    g = r["call"]
    r["released_10"] = round_to(g["golden_rel"], 10)
    r["generated_100"] = round_to(g["steady_gen"], 100)
    r["captured_1"] = int(round(g["captured"]))
    r["hh8_rel_1"] = int(round(g["hh8_rel"]))
    r["naive_rel_1"] = int(round(g["naive_rel"]))
    return r


def chart_png(res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rel = res["call"]["golden_rel"]
    fig, ax = plt.subplots(figsize=(7.0, 2.5), dpi=150)
    ax.axvspan(0, 375, color="#e8efe6")
    ax.axvspan(375, 450, color="#f6ecd2")
    ax.axvspan(450, 560, color="#f3dcd8")
    ax.barh([0], [rel], height=0.42, color="#3a5f7d")
    ax.axvline(375, color="#555555", lw=1.0, ls="--")
    ax.axvline(450, color="#555555", lw=1.0, ls="--")
    ax.text(187, 0.36, "Tier 1: no charge", ha="center", fontsize=8)
    ax.text(412, 0.36, "Tier 2: $118,000", ha="center", fontsize=8)
    ax.text(505, 0.36, "Tier 3: $312,000", ha="center", fontsize=8)
    ax.text(rel + 4, -0.02, "%d t" % res["released_10"], va="center", fontsize=9, color="#1f3346")
    ax.set_xlim(0, 560)
    ax.set_ylim(-0.4, 0.55)
    ax.set_yticks([])
    ax.set_xlabel("Methane released in 2026, tonnes (tier thresholds at 375 t and 450 t)", fontsize=8)
    ax.tick_params(axis="x", labelsize=8)
    ax.set_title("Breck Hollow 2026: methane released about %d t, in Tier 2" % res["released_10"], fontsize=9)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def write_brief(res, path):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import mm
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen import canvas
    import textwrap
    C.pdf_canvas_settings()
    g = res["call"]
    c = canvas.Canvas(path, pagesize=letter, invariant=1)
    c.setTitle("Breck Hollow methane charge 2026")
    y = 262 * mm

    def para(text, size=9.5, bold=False, gap=4.6, width=98):
        nonlocal y
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        for ln in textwrap.wrap(text, width):
            c.drawString(18 * mm, y, ln)
            y -= gap * mm
        y -= 1.6 * mm

    para("Quarrow Valley Regional Solid Waste Authority", 11, True)
    para("To: Finance Committee     From: Heidi Dillon, Environmental Compliance     Date: 15 January 2027", 9)
    para("Breck Hollow Landfill: 2026 methane charge for the 2027 budget", 10.5, True)
    para("Breck Hollow's 2026 return puts us in Tier 2 of the state's closed landfill methane charge. The 2027 budget "
         "should carry $118,000, invoiced by 30 June. We released about %d tonnes of methane in 2026, %d t above the "
         "Tier 2 threshold and %d t below Tier 3, so no corrective action plan is triggered."
         % (res["released_10"], int(g["golden_rel"] - 375), int(450 - g["golden_rel"])))
    png = chart_png(res)
    img = ImageReader(io.BytesIO(png))
    c.drawImage(img, 18 * mm, y - 62 * mm, width=176 * mm, height=62 * mm)
    y -= 66 * mm
    para("How the figure was built", 10, True)
    para("The gas plant captured %s t of methane in 2026 (historian flows at normal conditions times the measured "
         "methane content, local calendar year). The rule has us estimate what the waste generated from that capture at "
         "the 0.90 collection efficiency for our geomembrane cap. The blowers were down %d times for %.1f hours in all, "
         "and after each restart the wells drew off gas the waste had held during the stop, %d t over the year on top "
         "of the steady capture. That gas was generated during the outages, so generation is read from the steady "
         "hours: about %s t for the year. Released methane is the uncaptured part less 10 per cent oxidised in the "
         "cap, plus 1 per cent of the captured gas not destroyed in the engines and flare."
         % ("{:,}".format(res["captured_1"]), g["n_outages"], g["down_hours"], round(g["recovered"]),
            "{:,}".format(res["generated_100"])))
    para("Scaling the year's capture up by the share of hours the blowers ran, without taking out the gas recovered "
         "after restarts, would count that gas twice and put us at %d t, in Tier 3. Dividing the capture by 0.90 with "
         "no allowance for the outages would put us at %d t, in Tier 1. Neither matches the plant record."
         % (res["hh8_rel_1"], res["naive_rel_1"]))
    para("The return workbook (breck_hollow_methane_return_2026.xlsx) has the destruction device hours, engine starts, "
         "flare methane and the surface monitoring results the return needs.", 9)
    c.showPage()
    c.save()


def write_workbook(res, path):
    import openpyxl
    from openpyxl.styles import Font, Alignment
    wb = openpyxl.Workbook()
    g = res["call"]
    ws = wb.active
    ws.title = "Return 2026"
    bold = Font(bold=True)
    rows = [("Breck Hollow Landfill - Closed Landfill Methane Rule return, reporting year 2026", None),
            (None, None),
            ("Item", "Value"),
            ("Methane generated (t, nearest 100)", res["generated_100"]),
            ("Methane captured (t)", res["captured_1"]),
            ("Methane released (t, nearest 10)", res["released_10"]),
            ("Charge tier (rule 5.1)", res["tier"]),
            ("Charge payable in 2027 ($)", res["charge"]),
            (None, None),
            ("Basis", None),
            ("Collection efficiency (Schedule 2, geomembrane cap)", 0.90),
            ("Fraction of uncaptured methane oxidised in the cap", 0.10),
            ("Destruction efficiency, engines and enclosed flare", 0.99),
            ("Blower outages in 2026 (number)", g["n_outages"]),
            ("Hours the gas system was down in 2026", round(g["down_hours"], 2)),
            ("Methane recovered after restarts, generated during outages (t)", round(g["recovered"], 1))]
    for rr in rows:
        ws.append(list(rr))
    ws["A1"].font = bold
    ws["A3"].font = bold
    ws["B3"].font = bold
    ws["A10"].font = bold
    ws.column_dimensions["A"].width = 62
    ws.column_dimensions["B"].width = 16

    ws2 = wb.create_sheet("Destruction devices")
    ws2.append(["Quarter", "Engine 1 operating hours", "Engine 1 starts", "Engine 2 operating hours", "Engine 2 starts",
                "Flare operating hours", "Methane destroyed in flare (t)"])
    for cl in ws2[1]:
        cl.font = bold
        cl.alignment = Alignment(wrap_text=True)
    for q in (1, 2, 3, 4):
        e1, e2, fl = res["engines"][(1, q)], res["engines"][(2, q)], res["flare"][q]
        ws2.append(["Q%d 2026" % q, int(round(e1["hours"])), e1["starts"], int(round(e2["hours"])), e2["starts"],
                    int(round(fl["hours"])), int(round(fl["destroyed"]))])
    for col in "ABCDEFG":
        ws2.column_dimensions[col].width = 16

    ws3 = wb.create_sheet("Surface monitoring")
    ws3.append(["Walkover", "Locations over 500 ppm", "Of those, still over 500 ppm at first re-monitoring"])
    for cl in ws3[1]:
        cl.font = bold
        cl.alignment = Alignment(wrap_text=True)
    for q in (1, 2, 3, 4):
        s = res["sem"][q]
        ws3.append(["Q%d 2026" % q, s["exceed"], s["still"]])
    for col, w in zip("ABC", (12, 22, 30)):
        ws3.column_dimensions[col].width = w

    ws4 = wb.create_sheet("Generation working")
    ws4.append(["Month (local)", "Steady capture (kg CH4/h)", "Hours", "Methane generated (t)"])
    for cl in ws4[1]:
        cl.font = bold
    for m in g["months"]:
        ws4.append([MON[m["month"] - 1] + " 2026", round(m["steady_rate"], 1), int(m["hours"]),
                    round(m["steady_rate"] / 0.90 * m["hours"] / 1000.0, 1)])
    ws4.append([])
    ws4.append(["Steady capture: full running hours outside the outages and the elevated capture after each restart."])
    for col, w in zip("ABCD", (16, 24, 10, 22)):
        ws4.column_dimensions[col].width = w
    C.save_workbook(wb, path, dt.datetime(2027, 1, 15, 9, 30), "Quarrow Valley Regional Solid Waste Authority")


def write_golden(target, golden_dir):
    if not os.path.isdir(golden_dir):
        os.makedirs(golden_dir)
    res = compute(target)
    write_brief(res, os.path.join(golden_dir, "breck_hollow_charge_brief_2026.pdf"))
    write_workbook(res, os.path.join(golden_dir, "breck_hollow_methane_return_2026.xlsx"))
    return res


def figures(res):
    g = res["call"]
    f = {
        "tier": res["tier"], "charge_usd": res["charge"],
        "released_t_nearest_10": res["released_10"], "generated_t_nearest_100": res["generated_100"],
        "captured_t": res["captured_1"],
        "released_t_unrounded": round(g["golden_rel"], 1), "generated_t_unrounded": round(g["steady_gen"], 1),
        "recovered_after_restarts_t": round(g["recovered"], 1), "outages_n": g["n_outages"],
        "down_hours": round(g["down_hours"], 2), "running_share": round(g["f_rec"], 4),
        "default_hh8_generated_t": round(g["hh8_gen"], 1), "default_hh8_released_t": res["hh8_rel_1"],
        "naive_released_t": res["naive_rel_1"], "naive_generated_t": round(g["naive_gen"], 1),
        "threshold_tier2_t": 375, "threshold_tier3_t": 450, "charge_tier3_usd": 312000,
        "ce": 0.90, "ox": 0.10, "de": 0.99,
    }
    for q in (1, 2, 3, 4):
        for e in (1, 2):
            f["engine%d_hours_q%d" % (e, q)] = int(round(res["engines"][(e, q)]["hours"]))
            f["engine%d_starts_q%d" % (e, q)] = res["engines"][(e, q)]["starts"]
        f["flare_hours_q%d" % q] = int(round(res["flare"][q]["hours"]))
        f["flare_destroyed_t_q%d" % q] = int(round(res["flare"][q]["destroyed"]))
        f["sem_exceed_q%d" % q] = res["sem"][q]["exceed"]
        f["sem_still_q%d" % q] = res["sem"][q]["still"]
    return f
