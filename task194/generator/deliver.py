"""The golden deliverables and figures.json, written from the computed result."""
import datetime as dt
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

import pack as PK


def rint(x):
    return int(round(x))


def ls(m3h):
    """m3/h to litres a second, printed to one decimal."""
    v = round(m3h / 3.6, 1)
    return 0.0 if v == 0 else v


def write(res, out):
    R, order = res["R"], res["order"]
    call, ru = order[0], order[1]
    figs = {"call": R[call]["name"], "call_code": call, "runner_up": R[ru]["name"], "runner_up_code": ru,
            "own_change": {}, "lu_oct": {}, "occupied": {}, "repairs": {}, "default": {}}
    for c in sorted(R):
        figs["own_change"][R[c]["name"]] = ls(R[c]["own"])
        figs["lu_oct"][R[c]["name"]] = rint(res["lu_oct"][c])
        figs["occupied"][R[c]["name"]] = int(res["occupied"][c])
        figs["repairs"][R[c]["name"]] = int(res["repairs"][c])
    figs["call_change"] = ls(R[call]["own"])
    figs["runner_up_change"] = ls(R[ru]["own"])
    figs["gap"] = ls(R[call]["own"] - R[ru]["own"])
    d2 = sorted(R, key=lambda c: -R[c]["r2"])
    d1 = sorted(R, key=lambda c: -R[c]["r1"])
    d0 = sorted(R, key=lambda c: -R[c]["r0"])
    figs["default"] = {"r0_pick": R[d0[0]]["name"], "r1_pick": R[d1[0]]["name"], "r2_pick": R[d2[0]]["name"],
                       "r2_pick_change": ls(R[d2[0]]["r2"]), "r1_pick_change": ls(R[d1[0]]["r1"]),
                       "r0_pick_change": ls(R[d0[0]]["r0"])}
    op = res["open_pairs"]
    figs["open_valve"] = op[0]["valve"] if op else ""
    figs["transfer_night"] = ls(op[0]["transfer_night"]) if op else 0.0
    figs["donor"] = R[op[0]["b"]]["name"] if op else ""
    figs["receiver"] = R[op[0]["a"]]["name"] if op else ""
    # workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Allocation"
    ws.append(["Week 46 leak detection crew allocation (LP04 rev 3, allocation 2026-46)"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Crew area", figs["call"], "Change in own leakage (l/s)", figs["call_change"]])
    ws.append(["Runner-up", figs["runner_up"], "Change in own leakage (l/s)", figs["runner_up_change"]])
    ws.append(["Gap (l/s)", figs["gap"]])
    ws.append([])
    ws.append(["Area code", "Area", "Change in own leakage (l/s)", "LU consumption Oct 2026 (m3)",
               "Occupied household properties 31 Oct", "Mains repairs Aug-Oct"])
    for c in ws[6]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for c in sorted(R, key=lambda k: R[k]["name"]):
        n = R[c]["name"]
        ws.append([c, n, figs["own_change"][n], figs["lu_oct"][n], figs["occupied"][n], figs["repairs"][n]])
        if c == call:
            for cell in ws[ws.max_row]:
                cell.fill = PatternFill("solid", fgColor="FFF2CC")
    notes = wb.create_sheet("Workings")
    notes.append(["Area", "MNF base (m3/h)", "MNF comp (m3/h)", "Pressure factor", "Net night flow change, normalised (m3/h)",
                  "Through boundary valve at night (m3/h)", "Own leakage change (m3/h)"])
    for c in sorted(R, key=lambda k: R[k]["name"]):
        r = R[c]
        notes.append([r["name"], round(r["mnf_b"], 2), round(r["mnf_c"], 2), round(r["fac"], 3), round(r["r2"], 2),
                      round(r["transfer_night"], 2), round(r["own"], 2)])
    for ws_ in (ws, notes):
        ws_.column_dimensions["A"].width = 16
        ws_.column_dimensions["B"].width = 18
        for col in "CDEFG":
            ws_.column_dimensions[col].width = 17
    ws.freeze_panes = "C7"
    notes.freeze_panes = "B2"
    for row in ws.iter_rows(min_row=7, min_col=3, max_col=3):
        for c in row:
            c.number_format = "0.0"
    for row in ws.iter_rows(min_row=7, min_col=4, max_col=5):
        for c in row:
            c.number_format = "#,##0"
    for cell in ("D2", "D3", "B4"):
        ws[cell].number_format = "0.0"
    for row in notes.iter_rows(min_row=2, min_col=2, max_col=7):
        for c in row:
            c.number_format = "0.000" if c.column == 4 else "0.00"
    for c in notes[1]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.print_title_rows = "6:6"
    basis = wb.create_sheet("Basis")
    for line in [
        ["Allocation", "2026-46, crew week 9 to 15 November 2026"],
        ["Procedure", "LP04 rev 3 (issued 14 September 2026)"],
        ["Baseline nights", "7 September to 4 October 2026"],
        ["Comparison nights", "12 October to 1 November 2026"],
        ["Night hour", "readings from 03:00 to before 04:00, local clock time"],
        ["Pressure", "each set normalised to the baseline AZNP night pressure, N1 = 1.15"],
        ["Boundary", "%s (%s / %s) moved %s's draw onto %s's inlet meter from 6 October; the night crossing, "
                     "%.1f l/s, is netted out of both areas" % (figs["open_valve"], figs["receiver"], figs["donor"],
                                                                  figs["donor"], figs["receiver"], figs["transfer_night"])],
        ["Large users", "revenue meters only, each in the area of its supply point on the register; check meters sit behind a revenue meter and are not added"],
        ["Households", "occupied at 23:59 on 31 October by effective date, a property counted while any of its accounts is open"],
        ["Repairs", "jobs with a REPAIR MAIN task completed 1 August to 31 October, contractor jobs placed through the job they took over"],
        ["Export", "SCADA historian and AMR extracts of 3 November 2026, 06:12"],
    ]:
        basis.append(line)
    basis.column_dimensions["A"].width = 18
    basis.column_dimensions["B"].width = 110
    PK.xlsx_props(wb, "Kirsty Lloyd", "Kirsty Lloyd", dt.datetime(2026, 11, 3, 13, 42), dt.datetime(2026, 11, 3, 16, 57))
    p = os.path.join(out, "crew_allocation_week46.xlsx")
    wb.save(p)
    PK.fixed_zip(p)
    # chart
    names = sorted(R, key=lambda k: -R[k]["own"])
    fig, ax = plt.subplots(figsize=(9, 4.6), dpi=110)
    vals = [R[c]["own"] / 3.6 for c in names]
    cols = ["#c0504d" if c == call else "#7f9fbf" for c in names]
    ax.bar(range(len(names)), vals, color=cols)
    ax.axhline(0, color="#444", lw=0.8)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels([R[c]["name"] for c in names], rotation=55, ha="right", fontsize=8)
    ax.set_ylabel("Change in own leakage (l/s)")
    ax.set_title("%s's own leakage rose %.1f l/s, the only rise no neighbouring area's fall cancels"
                 % (figs["call"], figs["call_change"]), fontsize=10, loc="left")
    for i, v in enumerate(vals):
        ax.text(i, v + (0.012 if v >= 0 else -0.04), "%.1f" % (round(v, 1) + 0.0), ha="center", fontsize=7, color="#333")
    ax.annotate("crew, week 46", (0, vals[0]), xytext=(1.2, vals[0] + 0.02), fontsize=8,
                arrowprops=dict(arrowstyle="-", color="#999", lw=0.6))
    ki = names.index(figs["call_code"]) if figs["call_code"] in names else 0
    kh = [i for i, c in enumerate(names) if R[c]["name"] == figs["receiver"]]
    if kh:
        ax.annotate("%s: %.1f l/s on the meter, all\nof it %s's water via %s" % (figs["receiver"], figs["default"]["r2_pick_change"],
                    figs["donor"], figs["open_valve"]), (kh[0], 0.0), xytext=(kh[0] + 0.6, 0.38), fontsize=7.5, color="#555",
                    arrowprops=dict(arrowstyle="-", color="#999", lw=0.6))
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.text(0.01, 0.01, "Source: SCADA historian, AZNP loggers and AMR reads to 2 November 2026; LP04 rev 3 night sets for allocation 2026-46.",
             fontsize=6.5, color="#666")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(os.path.join(out, "night_flow_changes.pdf"), metadata={"Title": "Own leakage change by DMA, week 46", "Author": "Kirsty Lloyd", "Creator": None, "Producer": None, "CreationDate": None})
    plt.close(fig)
    return figs
