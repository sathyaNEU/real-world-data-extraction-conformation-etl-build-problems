"""The goldens: the board's workbook (the eight hospitals' ratios and the three centres, the 2026 resections so far and
the allowed amount per stay of the cooperative's own members) and the chart of the eight ratios, plus figures.json."""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                       # noqa: E402
from openpyxl import Workbook                         # noqa: E402
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side   # noqa: E402
from openpyxl.utils import get_column_letter          # noqa: E402

import common as K                                    # noqa: E402

PLUM = "5B2A6E"
THIN = Side(style="thin", color="B8BFC4")


def r1(x):
    """Round half up to one decimal, on the unrounded ratio."""
    import decimal
    return float(decimal.Decimal(repr(float(x))).quantize(decimal.Decimal("0.1"), rounding=decimal.ROUND_HALF_UP))


def dollars(x):
    """Round half up to the whole dollar."""
    import decimal
    return int(decimal.Decimal(repr(float(x))).quantize(decimal.Decimal("1"), rounding=decimal.ROUND_HALF_UP))


def figures(m, a, b):
    order = list(m["ratio"].sort_values().index)
    return {
        "call": {"centres": [K.NAME[h] for h in m["centres"]], "first_below": K.NAME[order[3]]},
        "ratio": {K.NAME[h]: r1(m["ratio"][h]) for h in K.ELIGIBLE},
        "ratio_unrounded": {K.NAME[h]: round(float(m["ratio"][h]), 4) for h in K.ELIGIBLE},
        "operations": {K.NAME[h]: int(m["operations"][h]) for h in K.ELIGIBLE},
        "deaths": {K.NAME[h]: int(m["observed"][h]) for h in K.ELIGIBLE},
        "expected": {K.NAME[h]: round(float(m["expected"][h]), 1) for h in K.ELIGIBLE},
        "totals": {"operations": int(m["operations"].sum()), "deaths": int(m["observed"].sum())},
        "earlier_share": {K.NAME[h]: round(100 * float(m["redo_share"][h]), 1) for h in K.ELIGIBLE},
        "earlier_coefficient": round(float(m["model"].params["redo"]), 2),
        "filed": {"follow_up_days": K.FOLLOW, "clauses": dict(K.CLAUSE)},
        "rival": {"own_record_ratio": {K.NAME[h]: round(float(m["own_record"][h]), 2) for h in K.ELIGIBLE},
                  "own_record_centres": [K.NAME[h] for h in m["own_record"].sort_values().index[:3]]},
        "ask_a": {K.NAME[h]: int(a[h]) for h in K.ELIGIBLE},
        "ask_b": {K.NAME[h]: dollars(b[h][1]) for h in K.ELIGIBLE},
    }


def _head(ws, row, cols):
    for j, h in enumerate(cols, 1):
        cell = ws.cell(row, j, h)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=PLUM)
        cell.alignment = Alignment(wrap_text=True, vertical="center")


def workbook(path, fig):
    wb = Workbook()
    ws = wb.active
    ws.title = "Centres"
    ws["A1"] = "Pancreatic Surgery Centres 2027: deaths within 90 days of resection against expected, 2023 to 2025"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Centres for 2027: %s. Observed deaths over the deaths the same patients' condition before surgery "
                "would have produced at the eight hospitals together." % ", ".join(fig["call"]["centres"]))
    ws["A2"].font = Font(italic=True, size=9)
    cols = ["Hospital", "Operations", "Deaths within 90 days", "Expected deaths", "Ratio (observed to expected)",
            "2027 centre"]
    _head(ws, 4, cols)
    names = sorted(fig["ratio"], key=lambda n: fig["ratio_unrounded"][n])
    for i, n in enumerate(names, 5):
        vals = [n, fig["operations"][n], fig["deaths"][n], fig["expected"][n], fig["ratio"][n],
                "Yes" if n in fig["call"]["centres"] else None]
        for j, v in enumerate(vals, 1):
            cell = ws.cell(i, j, v)
            cell.border = Border(bottom=THIN)
            if j == 4:
                cell.number_format = "0.0"
            if j == 5:
                cell.number_format = "0.0"
            if n in fig["call"]["centres"]:
                cell.font = Font(bold=True)
    t = 5 + len(names)
    ws.cell(t, 1, "Eight hospitals").font = Font(bold=True)
    ws.cell(t, 2, fig["totals"]["operations"]).font = Font(bold=True)
    ws.cell(t, 3, fig["totals"]["deaths"]).font = Font(bold=True)
    ws.cell(t + 2, 1, "Expected deaths come from a logistic model of death within 90 days fitted to the eight "
                      "hospitals' 2023 to 2025 resections, on the patient's age, sex, diagnosis, operation, urgency, "
                      "conditions present on admission and any earlier operation on the pancreas or bile ducts in the "
                      "consortium's files since 2016. Ratios compared unrounded, shown to one decimal.").font = Font(size=9)
    for j, wdt in enumerate([36, 12, 14, 14, 16, 12], 1):
        ws.column_dimensions[get_column_letter(j)].width = wdt
    ws.freeze_panes = "A5"
    # the two asks
    wc = wb.create_sheet("2026 so far")
    wc["A1"] = "Pancreatic resections discharged January to June 2026"
    wc["A1"].font = Font(bold=True, size=12)
    wc["A2"] = "ULHDC revised release of 18 September 2026; a stay the release holds twice is counted once."
    wc["A2"].font = Font(italic=True, size=9)
    _head(wc, 4, ["Hospital", "Resections"])
    for i, h in enumerate(K.ELIGIBLE, 5):
        wc.cell(i, 1, K.NAME[h])
        wc.cell(i, 2, fig["ask_a"][K.NAME[h]])
    wc.column_dimensions["A"].width, wc.column_dimensions["B"].width = 36, 12
    wm = wb.create_sheet("Members")
    wm["A1"] = "Corrisbrook members' pancreatic resection stays discharged 2023 to 2025: allowed per stay"
    wm["A1"].font = Font(bold=True, size=12)
    wm["A2"] = ("Facility claims received through 30 September 2026, each claim at its latest version; a stay's interim "
                "claims added together; a voided claim and its void left out.")
    wm["A2"].font = Font(italic=True, size=9)
    _head(wm, 4, ["Hospital", "Average allowed per stay ($)"])
    for i, h in enumerate(K.ELIGIBLE, 5):
        wm.cell(i, 1, K.NAME[h])
        c = wm.cell(i, 2, fig["ask_b"][K.NAME[h]])
        c.number_format = "#,##0"
    wm.column_dimensions["A"].width, wm.column_dimensions["B"].width = 36, 26
    wb.save(path)


def chart(path, fig):
    names = sorted(fig["ratio"], key=lambda n: fig["ratio_unrounded"][n])
    vals = [fig["ratio_unrounded"][n] for n in names]
    cols = ["#5b2a6e" if n in fig["call"]["centres"] else "#9aa3aa" for n in names]
    fig_, ax = plt.subplots(figsize=(8.2, 4.6), dpi=150)
    y = list(range(len(names)))[::-1]
    ax.scatter(vals, y, s=70, c=cols, zorder=3)
    for yy, v, n in zip(y, vals, names):
        ax.text(v + .03, yy, "%.1f" % fig["ratio"][n], va="center", fontsize=9)
    ax.axvline(1.0, color="#1f2428", lw=.8, ls="--")
    ax.text(1.008, -.55, "as expected (1.0)", fontsize=8, color="#5d646a", va="center")
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=9)
    ax.set_xlabel("Deaths within 90 days, observed to expected (2023 to 2025 resections)")
    fig_.text(0.01, 0.965, "%s, %s and %s have the three lowest ratios: the 2027 centres"
              % tuple(n.split()[0] for n in fig["call"]["centres"]), fontsize=11, ha="left", va="top")
    fig_.text(0.01, 0.01, "Source: ULHDC discharge files 2016 to 2025 and death linkage of 31 August 2026. Expected "
              "deaths from one model of the eight hospitals' patients, earlier operations included.", fontsize=7,
              color="#5d646a")
    ax.set_xlim(0.4, max(vals) + .25)
    ax.set_ylim(-.9, len(names) - .4)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig_.tight_layout(rect=(0, 0.03, 1, 0.93))
    fig_.savefig(path, metadata={"Software": None})
    plt.close(fig_)


def write_figures(path, fig):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(fig, f, indent=1, ensure_ascii=False)
        f.write("\n")


def write(target, golden):
    """Read the cut pack as the golden reads it, then write the workbook, the chart and figures.json."""
    import os
    import warnings
    warnings.filterwarnings("ignore")
    import analysis as A
    import pack
    P = pack.load(target)
    m = A.main_call(P)
    import models as M
    m["own_record"] = M.ratio(M.prep(m["df"]), M.INDEX)[0]
    a, b = A.ask_a(P), A.ask_b(P)
    fig = figures(m, a, b)
    if os.path.exists(golden):
        import shutil
        shutil.rmtree(golden)
    os.makedirs(golden)
    workbook(os.path.join(golden, "pancreatic_centres_2027.xlsx"), fig)
    chart(os.path.join(golden, "pancreatic_centres_2027.png"), fig)
    return fig, dict(P=P, m=m, a=a, b=b)
