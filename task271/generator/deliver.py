"""The goldens: the committee's workbook (every group's estimated risk of breast cancer by 70 for a woman who carries
it, whether the program takes it on, and the two High-Risk Breast Clinic planning figures) and the chart of the ten
risks against the 30 percent line, plus figures.json."""
import decimal
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                       # noqa: E402
from openpyxl import Workbook                         # noqa: E402
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side   # noqa: E402
from openpyxl.utils import get_column_letter          # noqa: E402

import analysis as A                                  # noqa: E402
import common as K                                    # noqa: E402
import models as M                                    # noqa: E402

PLUM = "5A2D5C"
THIN = Side(style="thin", color="B8BFC4")


def pct(x):
    return int(decimal.Decimal(repr(float(x) * 100)).quantize(decimal.Decimal("1"), rounding=decimal.ROUND_HALF_UP))


def figures(c, k):
    res = c["res"]
    fam = M.FAMILY
    qualify = [g for g in K.CODES if res[g]["kin"] >= A.LINE]
    lo = {g: min(res[g][f] for f in fam) for g in K.CODES}
    hi = {g: max(res[g][f] for f in fam) for g in K.CODES}
    routes = {r: A.sets(res, r) for r in M.FAMILY + M.ROUTES + M.RECORDED}
    return {
        "call": {"qualify": qualify, "qualify_labels": [K.LABEL[g] for g in qualify],
                 "not": [g for g in K.CODES if g not in qualify]},
        "verdict": {g: ("Yes" if g in qualify else "No") for g in K.CODES},
        "risk_kin_pct": {g: pct(res[g]["kin"]) for g in K.CODES},
        "risk_kin": {g: round(float(res[g]["kin"]), 4) for g in K.CODES},
        "family_range_pct": {g: [pct(lo[g]), pct(hi[g])] for g in K.CODES},
        "family_unrounded": {g: {f: round(float(res[g][f]), 4) for f in fam} for g in K.CODES},
        "routes": routes,
        "route_values": {g: {r: round(float(res[g][r]), 4) for r in M.ROUTES + M.RECORDED} for g in K.CODES},
        "f_n": round(c["f_n"], 4),
        "f_n_pct": round(c["f_n"] * 100, 1),
        "families": {g: res[g]["n_families"] for g in K.CODES},
        "relatives": {g: res[g]["n_relatives"] for g in K.CODES},
        "tested": {g: res[g]["n_tested"] for g in K.CODES},
        "tested_carriers": {g: res[g]["n_tested_carriers"] for g in K.CODES},
        "totals": {"families": sum(res[g]["n_families"] for g in K.CODES),
                   "relatives": sum(res[g]["n_relatives"] for g in K.CODES),
                   "ask_a": sum(k["a"].values()), "ask_b": sum(k["b"].values())},
        "ask_a": k["a"],
        "ask_b": k["b"],
        "default_pct": {g: pct(res[g]["default"]) for g in K.CODES},
        "sloppy_pct": {g: pct(res[g]["sloppy"]) for g in K.CODES},
        "tested_total": sum(res[g]["n_tested"] for g in K.CODES),
        "tested_carriers_total": sum(res[g]["n_tested_carriers"] for g in K.CODES),
        "late_testing": c["late_testing"],
        "filed": {"threshold_pct": 30, "age": 70, "clinic_ages": [30, 74], "registry_both": [42, 56],
                  "registry_one": [41, 51], "cpt": [19303, 19307], "clauses": ["2.3", "3.1", "3.2"]},
        "margin_floor_points": int(min(((res[g][f] - A.LINE) if g in qualify else (A.LINE - res[g][f])) * 100
                                       for g in K.CODES for f in fam)),
    }


def _head(ws, row, cols, widths):
    for j, (h, wd) in enumerate(zip(cols, widths), 1):
        cell = ws.cell(row, j, h)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=PLUM)
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[get_column_letter(j)].width = wd


def workbook(path, fig):
    wb = Workbook()
    ws = wb.active
    ws.title = "Groups 2027"
    ws["A1"] = "Family Outreach Program: variant groups for 2027"
    ws["A1"].font = Font(bold=True, size=13, color=PLUM)
    ws["A2"] = ("Program takes on the PALB2 protein-truncating and PALB2 missense groups; the other eight groups stay "
                "below 30 percent by age 70.")
    ws["A2"].font = Font(italic=True, size=10)
    cols = ["Group", "Gene", "Variant type", "Families", "Probands' mothers, sisters and daughters",
            "Risk of breast cancer by 70 for a carrier (estimate)", "Taken on from 1 April 2027",
            "Known carriers the clinic would be offered to on 1 April 2027",
            "Of whom no screening breast MRI, 1 Oct 2025 to 30 Sep 2026"]
    _head(ws, 4, cols, [13, 9, 18, 10, 16, 17, 13, 19, 19])
    ws.row_dimensions[4].height = 58
    r = 5
    for g in K.CODES:
        vals = [g, K.GENE[g], K.KIND[g], fig["families"][g], fig["relatives"][g], fig["risk_kin"][g],
                fig["verdict"][g], fig["ask_a"][g], fig["ask_b"][g]]
        for j, v in enumerate(vals, 1):
            cell = ws.cell(r, j, v)
            cell.border = Border(bottom=THIN)
            if j == 6:
                cell.number_format = "0%"
            elif j in (4, 5, 8, 9):
                cell.number_format = "#,##0"
            if j >= 4:
                cell.alignment = Alignment(horizontal="right" if j != 7 else "center")
        if fig["verdict"][g] == "Yes":
            for j in range(1, 10):
                ws.cell(r, j).fill = PatternFill("solid", fgColor="F1E6F2")
                ws.cell(r, j).font = Font(bold=True)
        r += 1
    ws.cell(r, 1, "All groups").font = Font(bold=True)
    for j, key in ((4, "families"), (5, "relatives"), (8, "ask_a"), (9, "ask_b")):
        cell = ws.cell(r, j, fig["totals"][key])
        cell.number_format = "#,##0"
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="right")
        cell.border = Border(top=Side(style="thin", color="1F2428"))
    ws.freeze_panes = "B5"
    n = wb.create_sheet("Notes")
    notes = [
        "How the figures were made",
        "Risk by 70: criteria 2.1 to 2.4. Each group is measured on all of its probands' mothers, sisters and daughters, "
        "living or dead, tested or not (the probands and half-sisters left out). A first-degree relative carries the "
        "family's variant with probability one half, so the share of these women with a first breast cancer before 70 "
        "(Kaplan-Meier on age, censored at the age the pedigree gives) is half the carriers' risk plus half the "
        "population's; the carriers' risk is twice that share less the population's risk.",
        "Population risk by 70: %.1f percent, from the tumor registry's 2016 to 2025 rates for female patients (first "
        "primary breast cancer, invasive or in situ), deaths from other causes set aside." % fig["f_n_pct"],
        "Check: a Mendelian likelihood over the same women (tested women's genotypes, the one-half prior for the "
        "others, the population's hazard for noncarriers) puts every group on the same side of 30 percent.",
        "Known carriers (criteria 3.1): final laboratory report showing the family's variant, enterprise ID, no death "
        "recorded to 30 September 2026, aged 30 to 74 on 1 April 2027, not both breasts removed on the tumor registry's "
        "first-course surgery or the surgical record.",
        "No screening MRI (criteria 3.2): no completed high-risk screening breast MRI at an Ellisford hospital from "
        "1 October 2025 to 30 September 2026, each study matched to its woman through the EMPI merge log.",
        "Prepared by %s, %s, from the registry extracts cut 30 September 2026." % (K.PEOPLE["requester"],
                                                                                  K.PEOPLE["requester_title"]),
    ]
    n.column_dimensions["A"].width = 120
    for i, t in enumerate(notes, 1):
        cell = n.cell(i, 1, t)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        if i == 1:
            cell.font = Font(bold=True)
    wb.save(path)


def chart(path, fig):
    order = sorted(K.CODES, key=lambda g: fig["risk_kin"][g])
    vals = [fig["risk_kin"][g] * 100 for g in order]
    colors = ["#5A2D5C" if fig["verdict"][g] == "Yes" else "#A9B1B8" for g in order]
    fig_, ax = plt.subplots(figsize=(8.2, 5.0), dpi=150)
    ax.barh(range(len(order)), vals, color=colors, height=0.62)
    ax.axvline(30, color="#B23A48", lw=1.4, ls="--")
    ax.text(30.4, len(order) - 0.45, "30% by age 70: program takes the group on", color="#B23A48", fontsize=8.5,
            va="center")
    for i, (g, v) in enumerate(zip(order, vals)):
        ax.text(v + 0.6, i, "%d%%" % round(v), va="center", fontsize=8.5, color="#1F2428")
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels(["%s (%s)" % (g, "%d families" % fig["families"][g]) for g in order], fontsize=8.5)
    ax.set_xlim(0, max(vals) + 9)
    ax.set_xlabel("Estimated risk of breast cancer by age 70 for a woman who carries the variant (%)", fontsize=9)
    ax.set_title("Only the two PALB2 groups clear 30% by age 70", fontsize=11.5, loc="left", color="#1F2428")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="x", labelsize=8.5)
    fig_.text(0.01, 0.01, "Kin-cohort estimate on each group's probands' mothers, sisters and daughters; population risk "
                          "from the Ellisford tumor registry. Ellisford Health ICRS, October 2026.", fontsize=7,
              color="#5D646A")
    fig_.tight_layout(rect=(0, 0.03, 1, 1))
    fig_.savefig(path, metadata={"Software": None})
    plt.close(fig_)


def write_figures(path, fig):
    with open(path, "w") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
        f.write("\n")


def write(target, golden):
    os.makedirs(golden, exist_ok=True)
    c = A.call(target)
    k = A.asks(target)
    fig = figures(c, k)
    workbook(os.path.join(golden, K.DELIVERABLES[0]), fig)
    chart(os.path.join(golden, K.DELIVERABLES[1]), fig)
    return fig, dict(call=c, asks=k)
