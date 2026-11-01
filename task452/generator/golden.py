"""The golden deliverables, built from the analysis of target/ alone: the memo (PDF, with its chart) and the workbook."""
import datetime as dt
import io
import os

import analysis as A
import common as C

LIMIT_KG = 85
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MAT_LABEL = {"limestone": "Limestone", "shale": "Shale", "sand": "Sand", "iron_ore": "Iron ore",
             "steel_slag": "Steel slag", "fly_ash": "Fly ash (PFA)", "coal": "Coal (as fired)", "srf": "SRF (as fired)"}


def compute(target):
    hg = A.mercury(target)
    a1 = A.ask1(target)
    a2 = A.ask2(target)
    fe = A.ask_feed(target)
    dflt = A.default_route(target)
    k1, k2 = round(hg["K1"]["release"]), round(hg["K2"]["release"])
    works = round(hg["K1"]["release"] + hg["K2"]["release"])
    return dict(hg=hg, a1=a1, a2=a2, fe=fe, dflt=dflt, k1=k1, k2=k2, works=works, over=works - LIMIT_KG)


def chart_png(res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7.2, 3.3), dpi=150)
    x = list(range(12))
    w = 0.38
    k1 = [res["a1"]["K1"]["months"][i] for i in x]
    k2 = [res["a1"]["K2"]["months"][i] for i in x]
    ax.bar([i - w / 2 for i in x], k1, w, label="Kiln 1", color="#3b6e8f")
    ax.bar([i + w / 2 for i in x], k2, w, label="Kiln 2", color="#c07a2c")
    ax.set_xticks(x)
    ax.set_xticklabels(MON, fontsize=8)
    ax.set_ylabel("Hours in direct operation", fontsize=8)
    ax.tick_params(axis="y", labelsize=8)
    ax.set_title("Hours on feed with the raw mill stopped, by month of 2026", fontsize=9)
    ax.legend(fontsize=8, frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def write_memo(res, path):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen import canvas
    import textwrap
    C.pdf_canvas_settings()
    c = canvas.Canvas(path, pagesize=A4, invariant=1)
    c.setTitle("Kiln mercury 2026 and the 2028 load")
    c.setAuthor("Environment and Quality, Kilcarrow Works")
    y = 282 * mm

    def para(text, size=9.5, bold=False, gap=2.0, width=100):
        nonlocal y
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        for ln in textwrap.wrap(text, width):
            c.drawString(18 * mm, y, ln)
            y -= size * 0.47 * mm
        y -= gap * mm

    hg = res["hg"]
    para("Kilcarrow Works - memo", 12, True, 1)
    para("To: Executive team.  From: Naomi Lynskey, Environment and Quality.  Date: 11 January 2027.", 9, False, 1)
    para("Subject: mercury to air in 2026 against the 85 kg annual load from 2028 (licence condition 5.6)", 9.5, True, 3)
    para("At its 2026 release the works would not keep under the 85 kg load. Kiln 1 released %d kg of mercury to air in "
         "2026 and kiln 2 released %d kg, %d kg for the works, %d kg over the load. Carbon injection, or another measure "
         "of the same size, is needed before 2028; it belongs in the 2027 capital round and in the reduction programme "
         "due to the Agency by 31 March." % (res["k1"], res["k2"], res["works"], res["over"]), 10, True, 3)
    para("How the figure was set", 9.5, True, 1)
    para("Mercury leaves a kiln line three ways: in clinker, in filter dust taken out of the system, and through the "
         "stack. Over a year the mercury the line took in with its raw materials and fuels is what left by those routes, "
         "so the release to air is the year's input less what went out in clinker and in dust. Inputs are the production "
         "ledger's monthly tonnages (raw materials dry, fuels as fired) times the laboratory's mercury composite for the "
         "month on the same basis (sand and slag: the quarter's composite); clinker is the ledger's clinker times its "
         "composite; kiln 1's dust is the ledger's filter dust to silo S7 times the month's dust composite. Kiln 2 returns "
         "its dust to the kiln feed.", 9, False, 2)
    rows = [("", "Kiln 1", "Kiln 2")]
    rows.append(("Mercury in raw materials and fuels, kg", "%.1f" % hg["K1"]["inputs"], "%.1f" % hg["K2"]["inputs"]))
    rows.append(("Less mercury in clinker, kg", "%.1f" % hg["K1"]["clinker"], "%.1f" % hg["K2"]["clinker"]))
    rows.append(("Less mercury in filter dust bled to silo S7, kg", "%.1f" % hg["K1"]["dust"], "-"))
    rows.append(("Released to air, kg", "%d" % res["k1"], "%d" % res["k2"]))
    c.setFont("Helvetica", 9)
    for i, r in enumerate(rows):
        c.setFont("Helvetica-Bold" if i in (0, len(rows) - 1) else "Helvetica", 9)
        c.drawString(22 * mm, y, r[0])
        c.drawRightString(140 * mm, y, r[1])
        c.drawRightString(170 * mm, y, r[2])
        y -= 5 * mm
    c.setFont("Helvetica-Oblique", 7.5)
    c.drawString(22 * mm, y, "Sources: production ledger 2026 (raw materials dry, fuels as fired); QC laboratory composites 2026.")
    y -= 6 * mm
    para("Why the stack tests give less", 9.5, True, 1)
    para("Every annual mercury test (2024 to 2026) ran with the raw mill on, when the mill takes the kiln gas's "
         "mercury into the raw meal and hands it back to the kiln. The tests agree with each other, but they measure "
         "that state only: carried over the year's kiln hours they give about %d kg for the works. "
         "Condition 5.6 counts every hour, and with the mill stopped (direct operation) the gas goes straight to the "
         "filter and the stored mercury goes with it. The chart shows each kiln's hours in direct operation by month."
         % int(round(res["dflt"]["K1"]["r0"] + res["dflt"]["K2"]["r0"])), 9, False, 2)
    img = ImageReader(io.BytesIO(chart_png(res)))
    c.drawImage(img, 18 * mm, y - 78 * mm, width=172 * mm, height=78 * mm)
    y -= 84 * mm
    para("Other 2026 figures for the annual report (NOx, hours on feed and hours in direct operation by quarter) are in "
         "kiln_emissions_2026.xlsx.", 8.5, False, 1)
    para("Note: direct operation is as defined in licence condition 1.5 (kiln producing clinker, raw mill stopped); hours "
         "are counted from the control system journal in Irish local time.", 7.5, False, 1)
    c.setFont("Helvetica", 7)
    c.drawString(18 * mm, 10 * mm, "Kilcarrow Works, Environment and Quality")
    c.drawRightString(192 * mm, 10 * mm, "Page 1 of 1")
    c.showPage()
    c.save()


def write_workbook(res, path):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    hg = res["hg"]
    ws = wb.active
    ws.title = "Mercury"
    ws.append(["Mercury to air, 2026 (kg)"])
    ws["A1"].font = Font(bold=True)
    ws.append([])
    ws.append(["Item", "Kiln 1", "Kiln 2"])
    for cell in ws[3]:
        cell.font = Font(bold=True)
    mats = ["limestone", "shale", "sand", "iron_ore", "steel_slag", "fly_ash", "coal", "srf"]
    for m in mats:
        v1 = hg["K1"]["per_mat"].get(m)
        v2 = hg["K2"]["per_mat"].get(m)
        ws.append(["In: " + MAT_LABEL[m], round(v1, 2) if v1 is not None else None, round(v2, 2) if v2 is not None else None])
    ws.append(["Total in", round(hg["K1"]["inputs"], 2), round(hg["K2"]["inputs"], 2)])
    ws.append(["Out in clinker", round(hg["K1"]["clinker"], 2), round(hg["K2"]["clinker"], 2)])
    ws.append(["Out in filter dust bled to silo S7", round(hg["K1"]["dust"], 2), 0])
    ws.append(["Released to air", res["k1"], res["k2"]])
    ws.append([])
    ws.append(["Works, released to air", res["works"]])
    ws.append(["Annual load from 2028 (condition 5.6)", LIMIT_KG])
    ws.append(["Over the load by", res["over"]])
    ws.column_dimensions["A"].width = 40
    ws2 = wb.create_sheet("Hours")
    ws2.append(["Kiln hours, 2026 (Irish local time)"])
    ws2["A1"].font = Font(bold=True)
    ws2.append([])
    ws2.append(["Quarter", "Kiln 1 on feed", "Kiln 1 direct operation", "Kiln 2 on feed", "Kiln 2 direct operation"])
    for cell in ws2[3]:
        cell.font = Font(bold=True)
    for q in range(4):
        ws2.append(["Q%d" % (q + 1), round(res["fe"]["K1"][q]), round(res["a1"]["K1"]["quarters"][q]),
                    round(res["fe"]["K2"][q]), round(res["a1"]["K2"]["quarters"][q])])
    ws2.append([])
    ws2.append(["Month", "Kiln 1 direct operation", "Kiln 2 direct operation"])
    for i, mm in enumerate(MON):
        ws2.append([mm, round(res["a1"]["K1"]["months"][i], 1), round(res["a1"]["K2"]["months"][i], 1)])
    ws3 = wb.create_sheet("NOx")
    ws3.append(["Nitrogen oxides (as NO2) to air, 2026"])
    ws3["A1"].font = Font(bold=True)
    ws3.append([])
    ws3.append(["Emission point", "Kiln", "Tonnes"])
    for cell in ws3[3]:
        cell.font = Font(bold=True)
    ws3.append(["A1-1", "Kiln 1", round(res["a2"]["K1"]["total"])])
    ws3.append(["A1-2", "Kiln 2", round(res["a2"]["K2"]["total"])])
    for wsx in (ws2, ws3):
        for col in ("A", "B", "C", "D", "E"):
            wsx.column_dimensions[col].width = 22
        wsx.freeze_panes = "A4"
    ws.freeze_panes = "A4"
    for row in ws2.iter_rows(min_row=4, max_row=7):
        for cell in row[1:]:
            cell.number_format = "#,##0"
    for row in ws.iter_rows(min_row=4, max_row=14):
        for cell in row[1:]:
            cell.number_format = "0.0"
    for r in (15, 17, 18, 19):
        for cell in ws[r][1:]:
            cell.number_format = "0"
    ws5 = wb.create_sheet("Notes")
    for line in ["Mercury to air: the year's mercury in raw materials (dry tonnes) and fuels (as fired) times the monthly",
                 "laboratory composites, less mercury in clinker and in kiln 1's filter dust to silo S7. Kilograms.",
                 "Direct operation: licence condition 1.5. Hours on feed: condition 6.5. Quarters in Irish local time.",
                 "NOx as NO2 from the stack CEMS, every half-hour of 2026; 11 to 20 May from the analyser loggers.",
                 "Prepared 11 January 2027 for the 2027 capital round and the annual environmental report."]:
        ws5.append([line])
    ws5.column_dimensions["A"].width = 110
    C.save_workbook(wb, path, dt.datetime(2027, 1, 11, 15, 40), "Environment and Quality")


def write_golden(target, outdir):
    os.makedirs(outdir, exist_ok=True)
    res = compute(target)
    write_memo(res, os.path.join(outdir, "kiln_mercury_memo_2026.pdf"))
    write_workbook(res, os.path.join(outdir, "kiln_emissions_2026.xlsx"))
    return res


def figures(res):
    """Every figure the write-up states, as it states it."""
    f = {
        "limit_kg": LIMIT_KG, "hg_K1_kg": res["k1"], "hg_K2_kg": res["k2"], "hg_works_kg": res["works"],
        "over_by_kg": res["over"], "verdict": "over the load: carbon injection needed",
        "tests_route_works_kg": int(round(res["dflt"]["K1"]["r0"] + res["dflt"]["K2"]["r0"])),
        "tests_route_K1_kg": int(round(res["dflt"]["K1"]["r0"])), "tests_route_K2_kg": int(round(res["dflt"]["K2"]["r0"])),
        "o2_reference_pct": 10, "licence_condition_load": "5.6", "licence_condition_hours": "6.5",
        "kiln_numbers": [1, 2],
    }
    for k in ("K1", "K2"):
        for q in range(4):
            f["direct_h_%s_Q%d" % (k, q + 1)] = int(round(res["a1"][k]["quarters"][q]))
            f["feed_h_%s_Q%d" % (k, q + 1)] = "{:,}".format(int(round(res["fe"][k][q])))
        f["nox_t_%s" % k] = int(round(res["a2"][k]["total"]))
    return f
