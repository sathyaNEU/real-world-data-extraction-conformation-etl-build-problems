"""task483 goldens: the placement workbook and the one-page note, computed from target/ alone (analysis.py), and
generator/figures.json with every graded figure at the precision it is graded."""
import io
import json
import os

import openpyxl
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import analysis as A

GOLDEN = {"workbook": "uti_pathway_placement_2027-28.xlsx", "note": "uti_pathway_placement_note_2027-28.docx"}
HEAD = PatternFill("solid", fgColor="D9E1F2")
PICK = PatternFill("solid", fgColor="E2EFDA")
THIN = Side(style="thin", color="A6A6A6")


def r10(x):
    """Nearest 10, halves away from zero."""
    q = abs(x) / 10.0
    v = int(q + 0.5) * 10
    return v if x >= 0 else -v


def pct(x):
    return int(100 * x + 0.5)


def figures(L):
    g = A.golden(L)
    n, ch, st = g["pool"], g["chances"], g["stopped"]
    nets = L["order"]
    rows = []
    for net in nets:
        rows.append({"network": net, "first_courses": sum(n[(net, d)] for d in A.DRUGS),
                     "nitrofurantoin": n[(net, "NIT")],
                     "other": sum(n[(net, d)] for d in A.OFF),
                     "by_drug": {d: n[(net, d)] for d in A.OFF},
                     "stopped": round(st[net], 3), "stopped_r10": r10(st[net])})
    two, rk = g["slate"], g["rank"]
    pres = g["pres"]
    chances = {d: {"cultures": len(pres), "resistant": sum(A.resistant(s, d) for s in pres),
                   "chance": round(ch[d], 5), "pct": pct(ch[d])} for d in A.DRUGS}
    grid = {net: {grp: g["grid"].get((net, grp), 0) for grp in A.GROUPS} for net in nets}
    return {"slate": two, "runner_up": rk[2], "rank": rk, "networks": rows, "chances": chances,
            "presentation_cultures": len(pres), "first_courses_2024_2026": len(g["fc"]),
            "first_courses_2026": sum(n.values()), "grid": grid,
            "filed": {"ages": [16, 64, 65], "lookback_days": 28, "pathway_year": [2026, 2027, 2028],
                      "specification_sections": [2.1, 2.2, 2.3, 3.1, 3.2, 4.1, 4.2]},
            "gap_second_to_runner_up": round(st[rk[1]] - st[rk[2]], 3),
            "margin_second_to_runner_up": round(st[rk[1]] / st[rk[2]], 4)}


def _box(ws, r1, r2, c1, c2):
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            ws.cell(row=r, column=c).border = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)


def workbook(F, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Placement"
    ws["A1"] = "UTI pathway 2027-28: pharmacist placement"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Pharmacists to %s and %s from 1 April 2027; runner-up %s. Basis: 2026 first courses for lower UTI in "
                "women aged 16 to 64 (specification 2.1 to 4.2)." % (F["slate"][0], F["slate"][1], F["runner_up"]))
    hdr = ["Network", "2026 first courses", "Nitrofurantoin", "Other antibacterials", "Trimethoprim", "Pivmecillinam",
           "Cefalexin", "Co-amoxiclav", "Fosfomycin", "Amoxicillin", "Mismatched courses stopped (nearest 10)",
           "Pharmacist"]
    ws.append([])
    ws.append(hdr)
    order = sorted(F["networks"], key=lambda r: -r["stopped"])
    for r in order:
        ws.append([r["network"], r["first_courses"], r["nitrofurantoin"], r["other"]] +
                  [r["by_drug"][d] for d in A.OFF] + [r["stopped_r10"], "Yes" if r["network"] in F["slate"] else None])
    top = 4
    last = top + len(order)
    for c in range(1, len(hdr) + 1):
        cell = ws.cell(row=top, column=c)
        cell.font = Font(bold=True)
        cell.fill = HEAD
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    for rr in range(top + 1, last + 1):
        if ws.cell(row=rr, column=12).value == "Yes":
            for c in range(1, len(hdr) + 1):
                ws.cell(row=rr, column=c).fill = PICK
    _box(ws, top, last, 1, len(hdr))
    ws.row_dimensions[top].height = 44
    for c, w in zip("ABCDEFGHIJKL", (18, 11, 13, 13, 12, 12, 11, 12, 11, 12, 18, 11)):
        ws.column_dimensions[c].width = w
    chart = BarChart()
    chart.type = "bar"
    chart.style = 10
    chart.title = "Mismatched first courses stopped by moving 2026 courses to nitrofurantoin"
    chart.y_axis.title = "Courses (nearest 10)"
    chart.x_axis.title = None
    data = Reference(ws, min_col=11, min_row=top, max_row=last)
    cats = Reference(ws, min_col=1, min_row=top + 1, max_row=last)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.legend = None
    chart.height, chart.width = 7.5, 16
    ws.add_chart(chart, "A%d" % (last + 3))

    ws2 = wb.create_sheet("Chances")
    ws2.append(["Each pathway antibacterial's chance that a first course meets an organism the laboratory reports "
                "resistant: urine cultures sent at the first course's consultation, 2024 to 2026"])
    ws2["A1"].font = Font(bold=True)
    ws2.append([])
    ws2.append(["Antibacterial", "Cultures", "Resistant organism", "Chance (%)", "Less nitrofurantoin (points)"])
    nit = F["chances"]["NIT"]["chance"]
    for d in A.DRUGS:
        c = F["chances"][d]
        ws2.append([A.DRUG_LABEL[d], c["cultures"], c["resistant"], c["pct"],
                    None if d == "NIT" else round(100 * (c["chance"] - nit), 1)])
    for c in range(1, 6):
        ws2.cell(row=3, column=c).font = Font(bold=True)
        ws2.cell(row=3, column=c).fill = HEAD
    _box(ws2, 3, 3 + len(A.DRUGS), 1, 5)
    for c, w in zip("ABCDE", (18, 10, 18, 11, 26)):
        ws2.column_dimensions[c].width = w

    ws3 = wb.create_sheet("Outside the pathway")
    ws3.append(["Women aged 65 and over and men aged 16 and over with a 2026 urine culture from a member practice or the "
                "hub growing each organism (patients)"])
    ws3["A1"].font = Font(bold=True)
    ws3.append([])
    ws3.append(["Network", "Enterococcus", "Enterobacter cloacae"])
    for r in F["networks"]:
        net = r["network"]
        ws3.append([net] + [F["grid"][net][g] for g in A.GROUPS])
    for c in range(1, 4):
        ws3.cell(row=3, column=c).font = Font(bold=True)
        ws3.cell(row=3, column=c).fill = HEAD
    _box(ws3, 3, 3 + len(F["networks"]), 1, 3)
    for c, w in zip("ABC", (18, 14, 14)):
        ws3.column_dimensions[c].width = w
    wb.save(path)


def chart_png(F):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["svg.hashsalt"] = "task483"
    order = sorted(F["networks"], key=lambda r: r["stopped"])
    fig, ax = plt.subplots(figsize=(6.2, 2.9), dpi=150)
    cols = ["#4E7A3A" if r["network"] in F["slate"] else "#9DB3C9" for r in order]
    ax.barh([r["network"] for r in order], [r["stopped_r10"] for r in order], color=cols)
    for i, r in enumerate(order):
        ax.text(r["stopped_r10"] + 0.6, i, "%d" % r["stopped_r10"], va="center", fontsize=8)
    ax.set_xlabel("Mismatched first courses stopped (2026 basis, nearest 10)", fontsize=8)
    ax.tick_params(labelsize=8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def note(F, path):
    import docx
    from docx.shared import Cm, Pt
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10)
    for s in d.sections:
        s.top_margin = s.bottom_margin = Cm(1.6)
        s.left_margin = s.right_margin = Cm(1.9)
    h = d.add_paragraph()
    run = h.add_run("UTI pathway 2027-28: where the two pharmacists go")
    run.bold = True
    run.font.size = Pt(13)
    d.add_paragraph("To: Clinical Director    From: Antimicrobial Stewardship Lead    13 January 2027")
    a, b = F["slate"]
    stp = {r["network"]: r for r in F["networks"]}
    d.add_paragraph(
        "Placement: one pharmacist to %s and one to %s from 1 April 2027. On the 2026 basis, moving their first courses "
        "on other antibacterials to nitrofurantoin would have stopped about %d and %d mismatched first courses. "
        "%s is the runner-up at about %d." % (a, b, stp[a]["stopped_r10"], stp[b]["stopped_r10"], F["runner_up"],
                                             stp[F["runner_up"]]["stopped_r10"]))
    ch = F["chances"]
    d.add_paragraph(
        "Each antibacterial's chance of meeting a resistant organism is read on the urine cultures practices sent at "
        "the first course's own consultation in 2024 to 2026 (%d cultures): nitrofurantoin %d%%, pivmecillinam %d%%, "
        "fosfomycin %d%%, trimethoprim %d%%. Most of the laboratory's other urines from these women were sent after a "
        "course had not worked, and those over-represent the organisms the federation's current first courses miss, "
        "nitrofurantoin's above all, so they are not used for the chance a first course runs."
        % (F["presentation_cultures"], ch["NIT"]["pct"], ch["MEC"]["pct"], ch["FOS"]["pct"], ch["TMP"]["pct"]))
    t = d.add_table(rows=1, cols=3)
    t.style = "Light Grid Accent 1"
    hdr = t.rows[0].cells
    hdr[0].text, hdr[1].text, hdr[2].text = "Network", "2026 first courses on other antibacterials", \
        "Mismatched courses stopped (nearest 10)"
    for r in sorted(F["networks"], key=lambda r: -r["stopped"]):
        c = t.add_row().cells
        c[0].text, c[1].text, c[2].text = r["network"], "%d" % r["other"], "%d" % r["stopped_r10"]
    d.add_paragraph()
    d.add_picture(io.BytesIO(chart_png(F)), width=Cm(14.5))
    d.add_paragraph("Detail by antibacterial, and the 2026 organisms in older women and men for the pharmacists' wider "
                    "advice, are in uti_pathway_placement_2027-28.xlsx.")
    d.core_properties.author = "Josephine James"
    d.save(path)


def main(target, gdir, fig_path):
    os.makedirs(gdir, exist_ok=True)
    L = A.load(target)
    F = figures(L)
    workbook(F, os.path.join(gdir, GOLDEN["workbook"]))
    note(F, os.path.join(gdir, GOLDEN["note"]))
    with open(fig_path, "w") as fh:
        json.dump(F, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return F
