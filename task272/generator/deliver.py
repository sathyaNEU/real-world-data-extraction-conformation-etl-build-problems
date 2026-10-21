"""The goldens: the program team's workbook (each member hospital, its measured drop after an approval, whether it
qualifies, and the two scorecard columns) and the chart of the 31 measures against the six-point line, plus
figures.json."""
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
import docs as DC                                     # noqa: E402
import models as M                                    # noqa: E402

TEAL = "1D5C63"
THIN = Side(style="thin", color="B8BFC4")


def half_up(x, places):
    q = decimal.Decimal(1).scaleb(-places)
    return float(decimal.Decimal(repr(float(x))).quantize(q, rounding=decimal.ROUND_HALF_UP))


def figures(res):
    c = res["call"]
    days = c["days"]
    fam = {code: M.family(days[code]) for code in K.CODES}
    ref = {code: M.reflexes(days[code]) for code in K.CODES}
    qualify = c["qualify"]
    dets = {code: sum(len(y) for _, _, y in days[code]) for code in K.CODES}
    a_k = {code: half_up(res["ask_a"][code] / 1000.0, 1) for code in K.CODES}
    margin = min((v - K.THRESHOLD) if code in qualify else (K.THRESHOLD - v)
                 for code in K.CODES for v in fam[code].values())
    return {
        "call": {"count": len(qualify), "qualify": qualify, "qualify_names": [K.NAME[x] for x in qualify],
                 "not": [x for x in K.CODES if x not in qualify]},
        "budget_usd": len(qualify) * DC.GRANT,
        "grant_usd": DC.GRANT,
        "verdict": {x: ("Yes" if x in qualify else "No") for x in K.CODES},
        "measure": {x: round(float(c["measure"][x]), 4) for x in K.CODES},
        "measure_1dp": {x: half_up(c["measure"][x], 1) for x in K.CODES},
        "family": {x: {k: round(float(v), 4) for k, v in fam[x].items()} for x in K.CODES},
        "family_margin_floor": round(float(margin), 3),
        "reflex": {x: {k: round(float(v), 4) for k, v in ref[x].items()} for x in K.CODES},
        "reflex_counts": {k: sum(1 for x in K.CODES if ref[x][k] >= K.THRESHOLD) for k in M.REFLEXES},
        "reflex_sets": {k: [x for x in K.CODES if ref[x][k] >= K.THRESHOLD] for k in M.REFLEXES},
        "determinations": dets,
        "determinations_total": sum(dets.values()),
        "counsellor_days": {x: len(days[x]) for x in K.CODES},
        "ask_a": a_k,
        "ask_a_usd": {x: round(res["ask_a"][x], 2) for x in K.CODES},
        "ask_a_total": half_up(sum(res["ask_a"].values()) / 1000.0, 1),
        "ask_b": dict(res["ask_b"]),
        "ask_b_total": sum(res["ask_b"].values()),
        "filed": {"threshold_points": K.THRESHOLD, "year": K.YEAR, "clauses": ["2.1", "2.2", "2.3", "2.4", "2.5",
                                                                             "2.6"],
                  "extract_cut": K.EXTRACT_CUT.isoformat()},
    }


def _head(ws, row, cols, widths):
    for j, (h, wd) in enumerate(zip(cols, widths), 1):
        cell = ws.cell(row, j, h)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=TEAL)
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[get_column_letter(j)].width = wd


def workbook(path, fig):
    wb = Workbook()
    ws = wb.active
    ws.title = "Grants FY2027"
    n = fig["call"]["count"]
    ws["A1"] = "Decision Coaching Grants FY2027: %d grants, $%s" % (n, format(fig["budget_usd"], ","))
    ws["A1"].font = Font(bold=True, size=13, color=TEAL)
    ws["A2"] = ("%d of the collaborative's 31 hospitals qualify under the criteria approved 8 December 2026: %s."
                % (n, ", ".join(fig["call"]["qualify_names"])))
    ws["A2"].font = Font(italic=True, size=10)
    cols = ["Code", "Hospital", "State", "Counsellor determinations, 2025",
            "Drop in the chance of approving right after an approval (points)", "Qualifies",
            "Assistance written off on counsellor approvals, net of reversals ($000)",
            "Counsellor denials for documents not received"]
    _head(ws, 4, cols, [7, 34, 7, 14, 18, 10, 20, 16])
    ws.row_dimensions[4].height = 62
    r = 5
    for code in K.CODES:
        st = next(h[3] for h in K.HOSPITALS if h[0] == code)
        vals = [code, K.NAME[code], st, fig["determinations"][code], fig["measure_1dp"][code], fig["verdict"][code],
                fig["ask_a"][code], fig["ask_b"][code]]
        for j, v in enumerate(vals, 1):
            cell = ws.cell(r, j, v)
            cell.border = Border(bottom=THIN)
            if j in (4, 8):
                cell.number_format = "#,##0"
            elif j == 5:
                cell.number_format = "0.0"
            elif j == 7:
                cell.number_format = "#,##0.0"
            if j >= 4:
                cell.alignment = Alignment(horizontal="center" if j == 6 else "right")
        if fig["verdict"][code] == "Yes":
            for j in range(1, 9):
                ws.cell(r, j).fill = PatternFill("solid", fgColor="E3F0F1")
                ws.cell(r, j).font = Font(bold=True)
        r += 1
    ws.cell(r, 1, "All hospitals").font = Font(bold=True)
    for j, v, fmt in ((4, fig["determinations_total"], "#,##0"), (6, "%d of 31" % n, None),
                      (7, fig["ask_a_total"], "#,##0.0"), (8, fig["ask_b_total"], "#,##0")):
        cell = ws.cell(r, j, v)
        if fmt:
            cell.number_format = fmt
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center" if j == 6 else "right")
        cell.border = Border(top=Side(style="thin", color="1F2428"))
    ws.freeze_panes = "C5"
    nt = wb.create_sheet("Notes")
    notes = [
        "How the figures were made",
        "Qualifies (criteria 2.1 to 2.6): each hospital's counsellors' 2025 approvals and denials, by counsellor and "
        "working day (local date; the Columbia extract's UTC clock put on Pacific time), in the order recorded; pends, "
        "withdrawals and the presumptive screening's approvals left out. Within each working day, the share approved "
        "right after a denial less the share approved right after an approval, pooled over the hospital's days, less "
        "what the same days give with each day's determinations in any order (the day's approvals held). A working day "
        "of n determinations shows a drop of about 100/(n-1) points with no counsellor swayed, and days with easier "
        "applications string approvals together, so neither the raw within-day drop nor the pooled one measures the "
        "counsellors.",
        "Check: the conditional logit that conditions on each working day's count, a random intercept for each "
        "counsellor-day, the day's rate over the counsellor's other determinations as a control, and Miller and "
        "Sanjurjo's per-day correction put every hospital on the same side of six points (the nearest is %.1f points "
        "from the line)." % fig["family_margin_floor"],
        "Grant: $%s for twelve months (criteria 1.2); FY2027 budget line %d x $%s = $%s." % (
            format(fig["grant_usd"], ","), fig["call"]["count"], format(fig["grant_usd"], ","),
            format(fig["budget_usd"], ",")),
        "Assistance written off: write-offs (FAWO) on applications a counsellor approved in 2025, each approval's "
        "write-off taken once (the adjustments extract repeats an approval's write-off on every account it covers), "
        "less reversals (FAWR) posted through 31 March 2026; the Willamette hub's December 2025 lines loaded twice "
        "counted once.",
        "Denials for documents not received: counsellor denials in 2025 with that reason; the collaborative's reason "
        "list was renumbered on 1 July 2025 (to 30 June, code 2 was documents not received and code 1 income above "
        "the limit), which the denials that reconsiderations reopen show.",
        "Prepared by %s, %s, %s, from the collaborative's 2025 extracts." % (
            K.PEOPLE["requester"], K.PEOPLE["requester_title"], K.FOUNDATION),
    ]
    nt.column_dimensions["A"].width = 120
    for i, t in enumerate(notes, 1):
        cell = nt.cell(i, 1, t)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        if i == 1:
            cell.font = Font(bold=True)
    wb.save(path)


def chart(path, fig):
    order = sorted(K.CODES, key=lambda x: fig["measure"][x])
    vals = [fig["measure"][x] for x in order]
    colors = ["#1D5C63" if fig["verdict"][x] == "Yes" else "#A9B1B8" for x in order]
    f, ax = plt.subplots(figsize=(8.4, 8.6), dpi=150)
    ax.barh(range(len(order)), vals, color=colors, height=0.66)
    ax.axvline(K.THRESHOLD, color="#B23A48", lw=1.4, ls="--")
    ax.axvline(0, color="#1F2428", lw=0.6)
    ax.text(K.THRESHOLD + 0.15, len(order) - 0.2, "6 points: a coaching grant", color="#B23A48", fontsize=8.5,
            va="center")
    for i, v in enumerate(vals):
        ax.text(v + (0.15 if v >= 0 else -0.15), i, "%.1f" % fig["measure_1dp"][order[i]], va="center",
                ha="left" if v >= 0 else "right", fontsize=7.8, color="#1F2428")
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels(["%s %s" % (x, K.NAME[x]) for x in order], fontsize=7.8)
    lo = min(vals)
    ax.set_xlim(min(lo - 1.5, -1.0), max(vals) + 2.0)
    ax.set_xlabel("Drop in the chance of approving right after an approval (percentage points)", fontsize=8.8)
    ax.set_title("%d of 31 hospitals clear the six-point line" % fig["call"]["count"], fontsize=12, loc="left",
                 color="#1F2428")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="x", labelsize=8.5)
    f.text(0.01, 0.01, "Counsellors' 2025 determinations; each working day's drop measured against the same day's "
                       "determinations in any order. %s, January 2027." % K.FOUNDATION, fontsize=7, color="#5D646A")
    f.tight_layout(rect=(0, 0.02, 1, 1))
    f.savefig(path, metadata={"Software": None})
    plt.close(f)


def write_figures(path, fig):
    with open(path, "w") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
        fh.write("\n")


def write(target, golden):
    os.makedirs(golden, exist_ok=True)
    res = A.run(target)
    fig = figures(res)
    workbook(os.path.join(golden, K.DELIVERABLES[0]), fig)
    chart(os.path.join(golden, K.DELIVERABLES[1]), fig)
    return fig, res
