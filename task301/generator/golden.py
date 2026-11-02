"""The golden deliverables, computed from the shipped files under target/ alone (analysis.py): the appraisal service's
two-page note to the cabinet, cabinet_note_child_poverty_2027.pdf, and its annex workbook, appraisal_annex_2027.xlsx."""
import os

import analysis as AN
import io_util as IO

MEASURES = [("A", "Prestación Infancia Directa"), ("B", "Ayuda a la Crianza"), ("C", "Complemento Familiar: higher limit"),
            ("D", "Suplemento de Alquiler con Hijos"), ("E", "Complemento Familiar: higher amount")]
PROVS = [("81", "Valmesura"), ("82", "Las Cuencas"), ("83", "Sierra del Alba")]
MONTHS = [((2025, 3), "March 2025"), ((2025, 6), "June 2025"), ((2025, 9), "September 2025"),
          ((2025, 12), "December 2025")]
RIVAL_BOUND = 3000


def r100(x):
    return int(100 * round(x / 100.0))


def figures(target):
    """Every figure the deliverables and the write-up state, computed once."""
    G = AN.golden(target)
    L = G["ladder"]
    R0, R3 = L["R0"], L["R3"]
    standing_rival = max(v for d in L["licensed"].values() for m, v in d.items() if m != "A")
    assert standing_rival < RIVAL_BOUND
    F = {
        "call": G["call"], "call_name": dict(MEASURES)[G["call"]],
        "A": G["A_total"], "A_r": G["A_total_r"],
        "A_prov": G["A_by_prov"], "A_prov_r": G["A_by_prov_r"],
        "R0": R0, "R3": R3, "R0_r": {m: r100(v) for m, v in R0.items()}, "R3_r": {m: r100(v) for m, v in R3.items()},
        "rival_bound": RIVAL_BOUND, "standing_rival": standing_rival,
        "line": L["F"]["line"], "uprate": L["F"]["uprate"], "take_up_pct": round(100 * L["T"], 1),
        "A_rate": L["F"]["A_rate"], "A_limit": L["F"]["A_limit"], "C_old": L["F"]["C_old"], "C_new": L["F"]["C_new"],
        "cfv_old_limit": L["F"]["cfv_old_limit"],
        "pace12_widening": round(100 * L["W"][AN.GOLD][0][11], 1),
        "pace12_launch": round(100 * L["L"][AN.GOLD][0][11], 1),
        "families": G["families"], "fieldwork": G["fieldwork"],
    }
    F["families_region"] = {ym: sum(v.values()) for ym, v in F["families"].items()}
    el = sum(F["fieldwork"][pc][0] for pc, _ in PROVS)
    co = sum(F["fieldwork"][pc][1] for pc, _ in PROVS)
    F["fieldwork_region"] = (el, co, round(100.0 * co / el, 1))
    return F


def fmt(n):
    return "{:,}".format(int(n))


def write_workbook(F, path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = Workbook()
    thin = Side(style="thin", color="98A3AA")
    bold = Font(bold=True)
    head_fill = PatternFill("solid", fgColor="E1E8EC")

    def header(ws, row, cols, widths):
        for i, (c, w) in enumerate(zip(cols, widths), start=1):
            cell = ws.cell(row=row, column=i, value=c)
            cell.font = bold
            cell.fill = head_fill
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            cell.border = Border(bottom=thin)
            ws.column_dimensions[cell.column_letter].width = w
        ws.row_dimensions[row].height = 30

    ws = wb.active
    ws.title = "Measure A 2027"
    ws["A1"] = "Children brought above the poverty line in 2027 by measure A, Prestación Infancia Directa"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("ECVV 2026 households, 2025 disposable income raised 6.1 per cent, poverty line €11,580 a year per "
                "equivalent adult (appraisal guidance of 15 October 2026); children to the nearest hundred.")
    header(ws, 4, ["Province", "Children brought above the line in 2027"], [24, 22])
    r = 5
    for pc, name in PROVS:
        ws.cell(row=r, column=1, value=name)
        c = ws.cell(row=r, column=2, value=F["A_prov_r"][pc])
        c.number_format = "#,##0"
        r += 1
    ws.cell(row=r, column=1, value="Comunidad de Valmesura").font = bold
    c = ws.cell(row=r, column=2, value=F["A_r"])
    c.number_format = "#,##0"
    c.font = bold
    ws.freeze_panes = "A5"
    ws.print_title_rows = "4:4"

    ws = wb.create_sheet("Complemento 2025")
    ws["A1"] = "Families the Complemento Familiar was paying, last month of each quarter of 2025"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("As its decisions stood at 31 December 2025, each family once, in the province it lived in that month "
                "(register extract of 2 November 2026 and the 2025 incident log).")
    header(ws, 4, ["Province"] + [lab for _, lab in MONTHS], [24, 14, 14, 14, 14])
    r = 5
    for pc, name in PROVS:
        ws.cell(row=r, column=1, value=name)
        for j, (ym, _) in enumerate(MONTHS, start=2):
            c = ws.cell(row=r, column=j, value=F["families"][ym].get(pc, 0))
            c.number_format = "#,##0"
        r += 1
    ws.cell(row=r, column=1, value="Comunidad de Valmesura").font = bold
    for j, (ym, _) in enumerate(MONTHS, start=2):
        c = ws.cell(row=r, column=j, value=F["families_region"][ym])
        c.number_format = "#,##0"
        c.font = bold
    ws.freeze_panes = "B5"
    ws.print_title_rows = "4:4"

    ws = wb.create_sheet("ECVV 2026 fieldwork")
    ws["A1"] = "ECVV 2026 fieldwork by province"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Province in which the sample dwelling is located; a dwelling issued twice counts once, with the "
                "result of its last issue; response rate = complete interviews over eligible sample dwellings.")
    header(ws, 4, ["Province", "Eligible sample dwellings", "Complete interviews", "Response rate (%)"],
           [24, 16, 14, 14])
    r = 5
    for pc, name in PROVS:
        el, co, rate, _ = F["fieldwork"][pc]
        ws.cell(row=r, column=1, value=name)
        ws.cell(row=r, column=2, value=el).number_format = "#,##0"
        ws.cell(row=r, column=3, value=co).number_format = "#,##0"
        ws.cell(row=r, column=4, value=rate).number_format = "0.0"
        r += 1
    el, co, rate = F["fieldwork_region"]
    ws.cell(row=r, column=1, value="Comunidad de Valmesura").font = bold
    for j, v, f in ((2, el, "#,##0"), (3, co, "#,##0"), (4, rate, "0.0")):
        c = ws.cell(row=r, column=j, value=v)
        c.number_format = f
        c.font = bold
    ws.freeze_panes = "B5"

    ws = wb.create_sheet("Notes")
    notes = [
        ("Survey", "ecvv2026_households.csv and ecvv2026_persons.csv (IEV, ECVV 2026, incomes of 2025)."),
        ("Measures", "child_poverty_proposals_2027.pdf (28 October 2026); appraisal guidance of 15 October 2026."),
        ("Complemento", "cfv_register_extract_20261102.csv, cfv_incidents_2025.xlsx, territorial_codes.csv; "
                        "complemento_familiar_rules_2026.pdf (payment from the month after the decision, 6.1)."),
        ("Fieldwork", "ecvv2026_fieldwork_cases.csv; eligibility and response rate as in the ECVV 2026 main results."),
        ("As of", "Complemento register as extracted on 2 November 2026; families counted as the decisions stood "
                  "at 31 December 2025, so an award revoked in 2026 counts as granted in 2025."),
        ("Rounding", "Children to the nearest hundred from the unrounded figure, each province on its own; families, "
                     "dwellings and interviews whole; response rates to one decimal from the counts."),
        ("Prepared", "Servicio de Estudios y Evaluación, 6 November 2026."),
    ]
    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["B"].width = 100
    for i, (k, v) in enumerate(notes, start=1):
        ws.cell(row=i, column=1, value=k).font = bold
        c = ws.cell(row=i, column=2, value=v)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)
    IO.repack_ooxml(path, "Guiomar Iñiguez", "Guiomar Iñiguez", "2026-11-04T08:20:00Z", "2026-11-06T12:40:00Z",
                    "Appraisal annex 2027", "Consejería de Derechos Sociales y Familias")


def chart_png(F, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.4, "svg.hashsalt": "task301"})
    ink, ink2, grid = "#0b0b0b", "#52514e", "#e4e4e2"
    s27, sfull = "#2a78d6", "#eb6834"
    order = ["A", "B", "C", "D", "E"]
    labels = {"A": "A  Prestación Infancia Directa", "B": "B  Ayuda a la Crianza",
              "C": "C  Complemento: higher limit", "D": "D  Suplemento de Alquiler", "E": "E  Complemento: higher amount"}
    fig, ax = plt.subplots(figsize=(6.7, 3.3), dpi=150)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")
    ys = list(range(len(order)))[::-1]
    yr = [F["R3"][m] for m in order]
    full = [F["R0"][m] for m in order]
    ax.xaxis.grid(True, color=grid, lw=0.6)
    ax.set_axisbelow(True)
    ax.barh([y + 0.2 for y in ys], yr, height=0.36, color=s27, edgecolor="#ffffff", linewidth=1.0,
            label="Payments families receive in 2027")
    ax.barh([y - 0.2 for y in ys], full, height=0.36, color=sfull, edgecolor="#ffffff", linewidth=1.0,
            label="If every family covered were paid all year")
    ax.set_yticks(ys)
    ax.set_yticklabels([labels[m] for m in order], color=ink)
    ia = order.index(F["call"])
    ax.get_yticklabels()[ia].set_fontweight("bold")
    ax.text(yr[ia] + 180, ys[ia] + 0.2, fmt(F["A_r"]) + " (recommended)", va="center", fontsize=7.9,
            fontweight="bold", color=ink)
    ic = order.index("C")
    ax.text(full[ic] + 180, ys[ic] - 0.2, fmt(F["R0_r"]["C"]), va="center", fontsize=7.6, color=ink2)
    ax.set_xlim(0, max(full) * 1.13)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: "{:,.0f}".format(v)))
    ax.tick_params(colors=ink2, labelsize=7.8)
    ax.set_xlabel("Children brought above the poverty line in 2027", color=ink2)
    ax.legend(loc="lower right", frameon=False, fontsize=7.6, labelcolor=ink)
    ax.set_title("Measure A brings the most children above the line in 2027", loc="left", fontsize=9.4,
                 fontweight="bold", color=ink)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#b9b8b2")
    fig.tight_layout()
    fig.savefig(path, dpi=150, metadata={"Software": None}, facecolor=fig.get_facecolor())
    plt.close(fig)


def write_note(F, path, png):
    from reportlab.lib.units import mm
    p = F["A_prov_r"]
    blocks = [
        ("title", "Fund measure A: it brings the most children above the poverty line in 2027"),
        ("sub", "To the regional cabinet. Servicio de Estudios y Evaluación, Dirección General de Planificación y "
                "Evaluación. 6 November 2026. Appraisal of the 2027 child poverty measures under the department's "
                "guidance of 15 October 2026."),
        ("h", "Recommendation"),
        ("p", "Fund measure A, the Prestación Infancia Directa. Paid by the regional tax agency from January 2027 to "
              "families who filed a 2025 return with gross income under €%s, it brings %s children above the "
              "poverty line in 2027: %s in Valmesura, %s in Las Cuencas and %s in Sierra del Alba."
              % (fmt(F["A_limit"]), fmt(F["A_r"]), fmt(p["81"]), fmt(p["82"]), fmt(p["83"]))),
        ("img", (png, 170 * mm, 84 * mm)),
        ("small", "Children whose household is below the line of €%s a year per equivalent adult without the "
                  "measure and at or above it with the payments it receives during 2027 (guidance 3.5); ECVV 2026 "
                  "households, 2025 incomes raised 6.1 per cent, grossed by the household weights. Figures are "
                  "rounded to the nearest hundred, each province on its own (guidance 4.2)." % fmt(F["line"])),
        ("h", "Why not the higher Complemento limit"),
        ("p", "Raising the Complemento Familiar's limit to €%s (measure C) would bring %s children above the line "
              "if every family it newly covers were paid for the whole year, which is how the proposals are costed. "
              "Families have to claim the Complemento, and it pays only from the month after the claim is decided. "
              "After the last limit rise, in April 2024, the families it brought in claimed slowly: by the twelfth "
              "month %s per cent of them had claimed, against %s per cent of the families entitled at the launch in "
              "October 2022. At that pace, C's payments in 2027 reach too few families for long enough, and C brings "
              "fewer than %s children above the line in 2027."
              % (fmt(F["C_new"]), fmt(F["R0_r"]["C"]), "%.0f" % F["pace12_widening"], "%.0f" % F["pace12_launch"],
                 fmt(F["rival_bound"]))),
        ("p", "The new claimed payments, B and D, would start the way the Complemento itself started in October 2022 "
              "and also stay under %s children in 2027. E adds to families the Complemento already pays, most of "
              "them far below the line, and brings about %s above it." % (fmt(F["rival_bound"]), fmt(F["R3_r"]["E"]))),
        ("h", "Basis"),
        ("p", "Claimed measures are counted only with the families who claim them, each paid from the month after "
              "its decision (guidance 3.9): claims for C arrive month by month as the families the April 2024 rise "
              "brought in claimed, claims for B and D as the families entitled at the launch claimed, each as a share "
              "of the survey's households in the band. The annex gives the Complemento's caseload in each quarter of "
              "2025 and the ECVV 2026 fieldwork by province."),
    ]
    IO.write_pdf(path, "Child poverty measures 2027: note to the cabinet", "Guiomar Iñiguez",
                 "Consejería de Derechos Sociales y Familias", blocks,
                 "Consejería de Derechos Sociales y Familias - Servicio de Estudios y Evaluación",
                 "D:20261106124500+01'00'", "D:20261106124500+01'00'")


def build(target, out_dir, scratch):
    F = figures(target)
    os.makedirs(out_dir, exist_ok=True)
    write_workbook(F, os.path.join(out_dir, "appraisal_annex_2027.xlsx"))
    png = os.path.join(scratch, "measures_chart.png")
    chart_png(F, png)
    write_note(F, os.path.join(out_dir, "cabinet_note_child_poverty_2027.pdf"), png)
    return F
