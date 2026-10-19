"""The goldens and figures.json, every figure computed from the shipped pack: the Commission's workbook
(pd_2027_entry_examination_components.xlsx) and the validity chart (entry_examination_validity_candidate_pool.png)."""
import os

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import analysis as A
import common as K
import pack as PK

WB = "pd_2027_entry_examination_components.xlsx"
CHART = "entry_examination_validity_candidate_pool.png"
COMP = K.COMPONENTS
ADMS = [a["name"] for a in K.ADMIN]


def compute(target):
    smp = PK.sample(target)
    ro = A.routes(smp)
    gold = ro["golden"]
    c = A.call(gold)
    cnt = A.counts(smp)
    cost, total, sat = A.cost(target)
    appl = A.applicants(target)
    comp = A.completion(target, appl)
    fig = dict(
        call=dict(keep=[K.LABEL[x] for x in c["keep"]], first_below=K.LABEL[c["first_below"]],
                  order=[K.LABEL[x] for x in c["order"]]),
        components=dict(pool=cnt["pool"], appointees=cnt["appointees"],
                        appointee_r={K.LABEL[x]: round(float(v), 2) for x, v in zip(COMP, ro["appointees"])},
                        oral_over_inventory_floor=float(np.floor(100 * min(
                            ro[m][COMP.index("oral")] - ro[m][COMP.index("inventory")] for m in A.LICENSED)) / 100)),
        ask_a={K.LABEL[x]: round(cost[x], 2) for x in COMP},
        ask_b=dict(applicants={a: appl[a] for a in ADMS}, applicants_total=sum(appl.values()),
                   completion={K.LABEL[x]: round(comp[x], 2) for x in COMP}),
        sat={K.LABEL[x]: sat[x] for x in COMP},
        rivals=dict(appointees=[K.LABEL[x] for x in A.call(ro["appointees"])["keep"]],
                    case2=[K.LABEL[x] for x in A.call(ro["case2"])["keep"]],
                    mixed=[K.LABEL[x] for x in A.call(ro["mixed"])["keep"]]),
    )
    exact = dict(routes=ro, cost=cost, total=total, sat=sat, appl=appl, comp=comp)
    return fig, exact


THIN = Side(style="thin", color="B8C4CC")
HEAD = PatternFill("solid", fgColor="DCE6EC")
KEEP = PatternFill("solid", fgColor="E2EFE6")


def _head(ws, row):
    for c in ws[row]:
        c.font = Font(bold=True)
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="top")


def write_workbook(path, fig, exact):
    ro = exact["routes"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "2027 components"
    ws.append(["2027 entry examination: the written test and the oral board are kept"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Validity in the candidate pool: each component's correlation with the academy criterion across the "
               "%s candidates who sat all five components in the 2024 and 2025 examinations, %s of them appointed."
               % (format(fig["components"]["pool"], ","), fig["components"]["appointees"])])
    ws.append([])
    ws.append(["Rank", "Component", "Validity in the candidate pool", "Correlation among the appointees", "2027"])
    _head(ws, 4)
    order = [x for x in sorted(COMP, key=lambda x: -ro["golden"][COMP.index(x)])]
    for i, x in enumerate(order, 1):
        j = COMP.index(x)
        kept = "Keep" if K.LABEL[x] in fig["call"]["keep"] else "Drop"
        ws.append([i, K.LABEL[x], round(float(ro["golden"][j]), 2), fig["components"]["appointee_r"][K.LABEL[x]], kept])
        r = ws.max_row
        ws.cell(r, 3).number_format = "0.00"
        ws.cell(r, 4).number_format = "0.00"
        if kept == "Keep":
            for c in ws[r]:
                c.fill = KEEP
        if i == 2:
            for c in ws[r]:
                c.border = Border(bottom=Side(style="medium", color="2C5A3F"))
    for col, w in zip("ABCDE", (7, 30, 16, 16, 9)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A5"

    c = wb.create_sheet("Cost per candidate")
    c.append(["Component", "Cost center", "Cost, four examinations ($)", "Candidates who sat it",
              "Cost per candidate ($)"])
    _head(c, 1)
    for x in COMP:
        c.append([K.LABEL[x], K.CC_OF[x], round(exact["total"][x], 2), exact["sat"][x], fig["ask_a"][K.LABEL[x]]])
        c.cell(c.max_row, 3).number_format = "#,##0"
        c.cell(c.max_row, 5).number_format = "#,##0.00"
    c.append(["All five", None, round(sum(exact["total"].values()), 2), None, None])
    c.cell(c.max_row, 3).number_format = "#,##0"
    for cell in c[c.max_row]:
        cell.font = Font(bold=True)
    for col, w in zip("ABCDE", (30, 11, 18, 14, 14)):
        c.column_dimensions[col].width = w
    c.freeze_panes = "A2"

    a = wb.create_sheet("Applicants and completion")
    a.append(["Examination", "People who applied"])
    _head(a, 1)
    for nm in ADMS:
        a.append([nm, fig["ask_b"]["applicants"][nm]])
        a.cell(a.max_row, 2).number_format = "#,##0"
    a.append(["Four examinations", fig["ask_b"]["applicants_total"]])
    a.cell(a.max_row, 2).number_format = "#,##0"
    for cell in a[a.max_row]:
        cell.font = Font(bold=True)
    a.append([])
    a.append(["Component", "Candidates who sat it", "Completion rate (%)"])
    _head(a, a.max_row)
    for x in COMP:
        a.append([K.LABEL[x], exact["sat"][x], fig["ask_b"]["completion"][K.LABEL[x]]])
        a.cell(a.max_row, 3).number_format = "0.00"
    for col, w in zip("ABC", (30, 18, 16)):
        a.column_dimensions[col].width = w

    n = wb.create_sheet("Notes")
    notes = [
        "Validity in the candidate pool corrects the appointees' correlations for how the appointees were chosen: the "
        "lists ranked on the written test and the oral board with the veterans' credit and took only candidates who "
        "passed the physical ability test, so the pool's covariances of those four scores and the appointees' "
        "covariances of every score and the academy criterion give the pool's correlations (the multivariate "
        "correction for selection on several variables).",
        "Academy criterion: the final average, or for a recruit who separated, the average at separation (classes "
        "24-2 to 26-2; the gradebook changed layout from class 25-3).",
        "Scores as the trial plan sets them: written test scaled score, oral board score, physical ability test points "
        "on the faster run, Pellwyn scaled score, work style inventory Dependability.",
        "Cost: each component's cost center for the four examinations, with 4410 shared by minutes a candidate. The "
        "30 June 2024 accruals are out (their invoices posted in full in July and August 2024 and the accrued balance "
        "was reversed in one line on 4410 on 1 July 2024); the 30 June 2025 accruals are in (from FY2025 the invoice "
        "posts only its difference from the accrual). Retroactive FOP pay of April 2025 is in.",
        "People who applied: entry applications submitted by 11:59 p.m. Eastern on the closing date, a person counted "
        "once in each examination; records joined on name and date of birth, on email, or on name and phone. Lateral "
        "entry applicants (the autumn 2025 requisition carried them after 4 August 2025) are out.",
        "Prepared by Personnel Research, %s, for the Civil Service Commission's meeting of 12 November 2026."
        % K.DIVISION,
    ]
    for t in notes:
        n.append([t])
    n.column_dimensions["A"].width = 120
    for row in n.iter_rows():
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)


def write_chart(path, fig, exact):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    ro = exact["routes"]
    order = sorted(range(5), key=lambda j: -ro["golden"][j])
    names = [K.LABEL[COMP[j]] for j in order]
    pool = [float(ro["golden"][j]) for j in order]
    app = [float(ro["appointees"][j]) for j in order]
    keep = [nm in fig["call"]["keep"] for nm in names]
    fg, ax = plt.subplots(figsize=(8.6, 4.9), dpi=150)
    y = np.arange(5)[::-1]
    ax.barh(y + 0.19, app, height=0.36, color="#b8c2c8", label="Among the appointees")
    ax.barh(y - 0.19, pool, height=0.36, color=["#2c5a3f" if k else "#7d9488" for k in keep],
            label="In the candidate pool")
    for yy, v in zip(y, pool):
        ax.text(v + 0.006, yy - 0.19, "%.2f" % v, va="center", fontsize=8.6, color="#1d2226")
    for yy, v in zip(y, app):
        ax.text(v + 0.006, yy + 0.19, "%.2f" % v, va="center", fontsize=8.2, color="#5b6268")
    ax.set_yticks(y)
    ax.set_yticklabels(names)
    ax.axhline(2.5, color="#2e3b44", lw=1.0, ls="--")
    ax.text(0.585, 2.56, "kept for 2027", ha="right", va="bottom", fontsize=8.4, color="#2e3b44")
    ax.set_xlim(0, 0.6)
    ax.set_xlabel("Correlation with the academy criterion")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="lower right", frameon=False, fontsize=8.6)
    fg.suptitle("Across the candidate pool, the written test and the oral board predict the academy best",
                x=0.012, ha="left", fontsize=11.5, fontweight="bold", color="#1d2226")
    fg.text(0.01, 0.01, "%s candidates who sat all five components, 2024 and 2025 examinations; %s appointed. "
                        "Academy classes 24-2 to 26-2." % (format(fig["components"]["pool"], ","),
                                                           fig["components"]["appointees"]),
            fontsize=7.4, color="#5b6268")
    fg.tight_layout(rect=(0, 0.04, 1, 0.95))
    fg.savefig(path, metadata={"Software": None})
    plt.close(fg)


def write(target, golden):
    fig, exact = compute(target)
    if os.path.exists(golden):
        for f in os.listdir(golden):
            os.remove(os.path.join(golden, f))
    os.makedirs(golden, exist_ok=True)
    write_workbook(os.path.join(golden, WB), fig, exact)
    write_chart(os.path.join(golden, CHART), fig, exact)
    return fig, exact
