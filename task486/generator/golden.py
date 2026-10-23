"""The golden workbook, computed from the cut pack (bundle.Golden): the 2027 allocation on the people each recipient
served in FY2026, the shelter nights by Continuum and quarter, and the waits from entry into rapid re-housing to
move-in; and generator/figures.json with every figure the write-up states."""
import collections
import json
import os
import sys

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B         # noqa: E402
import postprocess as PP   # noqa: E402
import world as W          # noqa: E402

OUT = "halvering_2027_fund_allocation.xlsx"
NAVY = "1F3A5F"
THIN = Side(style="thin", color="B9C0C4")
QLAB = ["Oct to Dec 2025", "Jan to Mar 2026", "Apr to Jun 2026", "Jul to Sep 2026"]


def figures(g):
    f = {}
    for k in B.RECIPIENTS:
        f["people|" + k] = g.counts[k]
        f["amount|" + k] = g.amounts[k]
        f["share|" + k] = round(100.0 * g.counts[k] / sum(g.counts.values()), 2)
    f["people|ALL"] = sum(g.counts.values())
    f["fund"] = B.FUND
    f["pool"] = int(B.FUND * (1 - B.ADMIN))
    f["split"] = sum(g.amounts.values())
    f["admin"] = B.FUND - f["split"]
    f["admin_pct"] = int(round(100 * B.ADMIN))
    I = g.I
    f["records"] = len(I.records)
    f["records_fy2026"] = sum(1 for a in g.act if a["active"])
    f["links"] = len(I.links)
    roots = I.resolve(constrained=False)
    grp = collections.defaultdict(list)
    for i, r in enumerate(roots):
        grp[r].append(i)
    f["conflict_groups"] = sum(1 for v in grp.values()
                               if any(n > 1 for n in collections.Counter(I.records[i][0] for i in v).values()))
    dc = I.counts(I.served(roots, g.act))
    da = B.allocation(dc)
    f["default_people|ALL"] = sum(dc.values())
    for k in B.RECIPIENTS:
        f["default_people|" + k] = dc[k]
        f["default_amount|" + k] = da[k]
    f["default_short|HAL"] = g.amounts["HAL"] - da["HAL"]
    for c in B.COCS:
        for q in range(4):
            f["nights|%s|Q%d" % (c, q + 1)] = g.nights[c][q]
        f["nights|%s|FY" % c] = sum(g.nights[c])
    for q in range(4):
        f["nights|ALL|Q%d" % (q + 1)] = sum(g.nights[c][q] for c in B.COCS)
    f["nights|ALL|FY"] = sum(sum(g.nights[c]) for c in B.COCS)
    for k in B.COCS + ["ALL"]:
        for t in B.TYPES:
            key = "%s|%s" % (k, "children" if t else "adults")
            f["rrh|" + key] = B.hround(g.rrh[(k, t)], 1)
            f["rrh_n|" + key] = g.rrh["n"][(k, t)]
    return f


def _title(ws, text, sub):
    ws["A1"] = text
    ws["A1"].font = Font(bold=True, size=13, color=NAVY)
    ws["A2"] = sub
    ws["A2"].font = Font(italic=True, size=9.5, color="5D636A")


def _head(ws, row, cols):
    for k, c in enumerate(cols):
        cell = ws.cell(row=row, column=k + 1, value=c)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=NAVY)
        cell.alignment = Alignment(horizontal="center" if k else "left", vertical="center", wrap_text=True)
    ws.row_dimensions[row].height = 32


def _row(ws, row, vals, fmts, bold=False):
    for k, (v, fm) in enumerate(zip(vals, fmts)):
        cell = ws.cell(row=row, column=k + 1, value=v)
        if fm:
            cell.number_format = fm
        cell.border = Border(bottom=THIN)
        if bold:
            cell.font = Font(bold=True)
        if k:
            cell.alignment = Alignment(horizontal="right")


def write_workbook(g, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Allocation 2027"
    _title(ws, "2027 Regional Homelessness Fund: %s split on the %s people the region served in FY2026" % (
        "${:,}".format(sum(g.amounts.values())), "{:,}".format(sum(g.counts.values()))),
           "Policy RF-2027. People served in federal fiscal year 2026 (1 October 2025 to 30 September 2026), each "
           "person counted once across the region. Halvering Valley Homeless Data Partnership, for the Regional Fund "
           "Committee meeting of 9 December 2026.")
    _head(ws, 4, ["Recipient", "People served, FY2026", "Share of people served", "2027 amount"])
    total = sum(g.counts.values())
    r = 5
    for k in B.RECIPIENTS:
        _row(ws, r, [W.RECIPIENT_NAME[k], g.counts[k], g.counts[k] / total, g.amounts[k]],
             [None, "#,##0", "0.00%", '"$"#,##0'])
        r += 1
    _row(ws, r, ["All recipients", total, 1.0, sum(g.amounts.values())], [None, "#,##0", "0.00%", '"$"#,##0'],
         bold=True)
    r += 2
    for label, v in (("2027 Fund (policy section 2)", B.FUND),
                     ("Partnership administration and regional data integration, 4 per cent, less the dollar the "
                      "rounding leaves over", B.FUND - sum(g.amounts.values())),
                     ("Split among the five recipients", sum(g.amounts.values()))):
        ws.cell(row=r, column=1, value=label)
        c = ws.cell(row=r, column=4, value=v)
        c.number_format = '"$"#,##0'
        c.alignment = Alignment(horizontal="right")
        r += 1
    r += 1
    notes = [
        "People served: a person is counted once for the region if any record of theirs shows service in FY2026 "
        "(policy section 3) and is placed with one recipient (section 4).",
        "One person across the sources: the State Data Linkage Unit's LINK findings from its run of 8 October 2026, "
        "taken strongest first. A link that would put two records of one source in one person is not taken, since "
        "each source holds a person once, so a chain through a record carrying only a year of birth stops at its "
        "weakest link.",
        "Amounts: the 18,000,000 dollars left after the 4 per cent set-aside, split in proportion to people served "
        "and rounded to the nearest dollar.",
    ]
    for t in notes:
        c = ws.cell(row=r, column=1, value=t)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.font = Font(size=9, color="333A40")
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
        ws.row_dimensions[r].height = 40
        r += 1
    for col, wd in zip("ABCD", (48, 20, 20, 18)):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A5"

    ws2 = wb.create_sheet("Shelter nights")
    _title(ws2, "Nights people spent in emergency shelters (night by night included) and safe havens, FY2026",
           "By Continuum and quarter. A person's night counts once: where a stay was left open after the person "
           "entered another shelter, the night is counted once. Night-by-night nights are bed-night services.")
    _head(ws2, 4, ["Continuum"] + QLAB + ["FY2026"])
    r = 5
    for c in B.COCS:
        _row(ws2, r, [W.COC_NAME[c]] + g.nights[c] + [sum(g.nights[c])], [None] + ["#,##0"] * 5)
        r += 1
    _row(ws2, r, ["Region"] + [sum(g.nights[c][q] for c in B.COCS) for q in range(4)] +
         [sum(sum(g.nights[c]) for c in B.COCS)], [None] + ["#,##0"] * 5, bold=True)
    for col, wd in zip("ABCDEF", (34, 15, 15, 15, 15, 14)):
        ws2.column_dimensions[col].width = wd
    ws2.freeze_panes = "B5"

    ws3 = wb.create_sheet("Rapid re-housing")
    _title(ws3, "Moves into housing from rapid re-housing in FY2026",
           "Average days from the household's entry into rapid re-housing to its move-in, over the FY2026 move-ins. "
           "A household that moved to another rapid re-housing project of the Continuum on the day it left the "
           "first is counted from its first entry.")
    _head(ws3, 4, ["Continuum", "Household type", "Move-ins, FY2026", "Average days, entry to move-in"])
    r = 5
    for c in B.COCS + ["ALL"]:
        name = W.COC_NAME[c] if c != "ALL" else "Region"
        for t in B.TYPES:
            _row(ws3, r, [name, B.TYPE_NAME[t], g.rrh["n"][(c, t)], B.hround(g.rrh[(c, t)], 1)],
                 [None, None, "#,##0", "0.0"], bold=(c == "ALL"))
            ws3.cell(row=r, column=2).alignment = Alignment(horizontal="left")
            r += 1
    for col, wd in zip("ABCD", (34, 26, 18, 30)):
        ws3.column_dimensions[col].width = wd
    ws3.freeze_panes = "B5"

    ws4 = wb.create_sheet("Notes")
    lines = [("Extract", "The Partnership's FY2026 integration extract of 14 October 2026 and the State Data Linkage "
              "Unit's findings for its run of 8 October 2026."),
             ("Fiscal year", "Federal fiscal year 2026, 1 October 2025 to 30 September 2026; local dates."),
             ("Recipients", "The four Continuums of Care and the Halvering Valley Coalition for Survivors."),
             ("Shelter nights", "A stay's nights run from its entry date to the night before its exit; an open stay "
              "to the night of 30 September 2026."),
             ("Rapid re-housing", "Move-ins read from the head of household's enrollment.")]
    _head(ws4, 1, ["Item", "Note"])
    for k, (a, b) in enumerate(lines):
        ws4.cell(row=k + 2, column=1, value=a).font = Font(bold=True)
        c = ws4.cell(row=k + 2, column=2, value=b)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws4.row_dimensions[k + 2].height = 30
    ws4.column_dimensions["A"].width = 18
    ws4.column_dimensions["B"].width = 96
    wb.save(path)
    PP.normalize_ooxml(path, W.PEOPLE["partnership_data"], W.PEOPLE["partnership_data"], "2026-10-15T16:12:00Z",
                       "2026-10-21T23:48:31Z", excel=True, company=W.PARTNERSHIP)


def main(target, gdir, fig_path):
    g = B.Golden(target)
    os.makedirs(gdir, exist_ok=True)
    write_workbook(g, os.path.join(gdir, OUT))
    f = figures(g)
    with open(fig_path, "w", encoding="utf-8") as fh:
        json.dump(f, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return g, f


if __name__ == "__main__":
    T = os.path.dirname(HERE)
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(T, "target"),
         sys.argv[2] if len(sys.argv) > 2 else os.path.join(T, "golden"),
         sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "figures.json"))
