"""The golden deliverables: the safety plan memo (docx), the forecast workbook (xlsx) and the quarterly chart (png),
written from analysis.main()'s figures."""
import os

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import postprocess as PP
import world as W

MEMO = "safety_plan_recordables_2027.docx"
BOOK = "recordables_forecast_2027.xlsx"
CHART = "recordables_by_quarter_2027.png"
RED = "7A2E1F"


def r0(x):
    return int(round(x))


def summary(F):
    g = F["gold"]
    A = F["asks"]
    tot = dict(quarters=[sum(A[dd]["quarters"][q] for dd in W.DISTRICTS) for q in range(3)],
               total=sum(A[dd]["total"] for dd in W.DISTRICTS))
    return dict(total=r0(g["total"]), rate=g["rate"], quarters=[r0(x) for x in g["quarters"]],
                qrates=g["quarter_rates"], hours=g["hours"], qhours=g["quarter_hours"], clean=g["clean"],
                tech=g["tech"], recorded=F["recorded"]["all"], recorded_crew=F["recorded"]["crew"],
                naive=r0(F["r0"]), asks=A, ytd=tot)


def _cell_text(cell, text, bold=False, size=None, align=None):
    from docx.shared import Pt
    cell.text = ""
    p = cell.paragraphs[0]
    run = p.add_run(text)
    run.bold = bold
    if size:
        run.font.size = Pt(size)
    if align:
        p.alignment = align


def memo(path, F):
    import docx
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt
    S = summary(F)
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    d.add_heading("2027 contract-year safety plan: recordable injury forecast", level=1)
    d.add_paragraph("To: Jerome Warren, Contractor Safety Manager, Pinewater EMC. From: Samantha Galvan, Director of "
                    "Environment, Health and Safety, Redbud Line Services. Date: 23 October 2026. Under CS-4 "
                    "section 4.")
    d.add_heading("The forecast", level=2)
    d.add_paragraph(
        "Redbud forecasts %d recordable injuries on Pinewater work in 2027, a recordable rate of %.2f per 200,000 "
        "hours on the %s hours of our 2027 work plan. That is above the 3.0 limit in CS-4 section 5, so our plan "
        "puts Redbud in enhanced oversight for the 2027 contract year, and we would like to agree the corrective "
        "action plan with you in November rather than in January." % (S["total"], S["rate"], "{:,}".format(r0(S["hours"]))))
    t = d.add_table(rows=6, cols=4)
    t.style = "Table Grid"
    head = ["Quarter", "Hours worked (plan)", "Recordable injuries", "Recordable rate"]
    for k, h in enumerate(head):
        _cell_text(t.rows[0].cells[k], h, bold=True, size=9.5)
    for q in range(4):
        vals = ["Q%d 2027" % (q + 1), "{:,}".format(r0(S["qhours"][q])), "%d" % S["quarters"][q], "%.2f" % S["qrates"][q]]
        for k, v in enumerate(vals):
            _cell_text(t.rows[q + 1].cells[k], v, size=9.5, align=None if k == 0 else WD_ALIGN_PARAGRAPH.RIGHT)
    vals = ["2027", "{:,}".format(r0(S["hours"])), "%d" % S["total"], "%.2f" % S["rate"]]
    for k, v in enumerate(vals):
        _cell_text(t.rows[5].cells[k], v, bold=True, size=9.5, align=None if k == 0 else WD_ALIGN_PARAGRAPH.RIGHT)
    d.add_paragraph("Quarters are rounded separately and do not add exactly to the year.").runs[0].italic = True
    d.add_heading("Why the forecast is above what we have recorded", level=2)
    d.add_paragraph(
        "Our crews recorded %.2f recordable injuries per 200,000 hours on Pinewater work from January 2021 to "
        "September 2026, and our technicians %.2f. Carried onto the 2027 plan, that record gives about %d "
        "recordables, inside the limit. We do not think it is what 2027 will record. Every crew in HR-14 earns its "
        "recognition award after 90 days without a recordable, and the programme ends on 31 December 2026. Read "
        "against each crew's own count, our case records show crews recording injuries at a steady rate for the "
        "first five weeks of a count and at well under half that rate in its last month, while the cases that keep "
        "a worker off work, which cannot go unrecorded, come in at much the same rate all through the count. In the "
        "first 35 days of their counts, when an award is far off, crews recorded %.2f per 200,000 hours. That is "
        "the rate we have planned on for every crew in 2027, with the technicians at their own %.2f."
        % (S["recorded_crew"], S["tech"], S["naive"], S["clean"], S["tech"]))
    d.add_heading("First-aid cases in 2026 to date (CS-4 section 4(c))", level=2)
    d.add_paragraph("5 January to 27 September 2026, field employees on Pinewater work, each injury once as the case "
                    "records finally classify it. A case the nurse line opened from a worker's call is the same "
                    "injury as the supervisor's case for that worker in the days before the call, when there is one. "
                    "Each injury is in the quarter of its injury date and the district of the worker's crew or team "
                    "on that day.")
    t2 = d.add_table(rows=6, cols=5)
    t2.style = "Table Grid"
    h2 = ["District", "Q1 (from 5 January)", "Q2", "Q3 (to 27 September)", "5 January to 27 September"]
    for k, h in enumerate(h2):
        _cell_text(t2.rows[0].cells[k], h, bold=True, size=9)
    for i, dist in enumerate(W.DISTRICTS):
        a = S["asks"][dist]
        vals = [dist] + ["%d" % v for v in a["quarters"]] + ["%d" % a["total"]]
        for k, v in enumerate(vals):
            _cell_text(t2.rows[i + 1].cells[k], v, size=9, align=None if k == 0 else WD_ALIGN_PARAGRAPH.RIGHT)
    y = S["ytd"]
    vals = ["All districts"] + ["%d" % v for v in y["quarters"]] + ["%d" % y["total"]]
    for k, v in enumerate(vals):
        _cell_text(t2.rows[5].cells[k], v, bold=True, size=9, align=None if k == 0 else WD_ALIGN_PARAGRAPH.RIGHT)
    d.add_heading("What we are doing", level=2)
    d.add_paragraph("We are briefing every district safety coordinator on the end of HR-14 this month, so that "
                    "supervisors expect more recordables on the log from January and treat them as reporting, not "
                    "as a loss of control. The quarterly forecast and the 2026 first-aid cases are in "
                    "recordables_forecast_2027.xlsx, with the chart recordables_by_quarter_2027.png.")
    d.save(path)
    PP.normalize_docx(path, W.PEOPLE["director"], W.PEOPLE["director"], "2026-10-20T13:04:00Z", "2026-10-23T15:37:00Z",
                      6, 96, "t130-memo", title="2027 contract-year safety plan: recordable injury forecast",
                      company=W.COMPANY)


def _table(ws, top, head, rows, widths=None, formats=None):
    thin = Side(style="thin", color="BBBBBB")
    for k, h in enumerate(head):
        c = ws.cell(row=top, column=k + 1, value=h)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=RED)
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for i, r in enumerate(rows):
        for k, v in enumerate(r):
            c = ws.cell(row=top + 1 + i, column=k + 1, value=v)
            c.border = Border(bottom=thin)
            if formats and formats[k]:
                c.number_format = formats[k]
    if widths:
        for k, w in enumerate(widths):
            ws.column_dimensions[openpyxl.utils.get_column_letter(k + 1)].width = w


def workbook(path, F):
    S = summary(F)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "2027 forecast"
    ws["A1"] = "Redbud Line Services: 2027 recordable injury forecast on Pinewater work (CS-4 section 4(a) and (b))"
    ws["A1"].font = Font(bold=True, size=12)
    rows = [["Q%d 2027" % (q + 1), r0(S["qhours"][q]), S["quarters"][q], round(S["qrates"][q], 2)] for q in range(4)]
    rows.append(["2027", r0(S["hours"]), S["total"], round(S["rate"], 2)])
    _table(ws, 3, ["Quarter", "Hours worked (plan)", "Recordable injuries (forecast)", "Recordable rate"], rows,
           [14, 20, 22, 16], [None, "#,##0", "0", "0.00"])
    ws["A10"] = "CS-4 limit"
    ws["B10"] = 3.0
    ws["B10"].number_format = "0.0"
    ws["A11"] = "Above the limit"
    ws["B11"] = "Yes" if S["rate"] > W.LIMIT else "No"
    ws2 = wb.create_sheet("2026 by district")
    ws2["A1"] = "First-aid cases on Pinewater work, 5 January to 27 September 2026 (CS-4 section 4(c))"
    ws2["A1"].font = Font(bold=True, size=12)
    rows = [[dist] + list(S["asks"][dist]["quarters"]) + [S["asks"][dist]["total"]] for dist in W.DISTRICTS]
    y = S["ytd"]
    rows.append(["All districts"] + list(y["quarters"]) + [y["total"]])
    _table(ws2, 3, ["District", "Q1 (5 Jan to 31 Mar)", "Q2 (1 Apr to 30 Jun)", "Q3 (1 Jul to 27 Sep)",
                    "5 Jan to 27 Sep"], rows, [14, 14, 14, 14, 14], [None, "0", "0", "0", "0"])
    ws3 = wb.create_sheet("Basis")
    ws3["A1"] = "Rates used for 2027 (recordables per 200,000 hours worked on Pinewater work, 2021 to 2026)"
    ws3["A1"].font = Font(bold=True, size=12)
    _table(ws3, 3, ["Rate", "Value", "Note"], [
        ["Crews, first 35 days of each recognition count", round(S["clean"], 2),
         "applied to every crew hour in the 2027 plan"],
        ["Technicians (outside HR-14)", round(S["tech"], 2), "applied to every technician hour in the 2027 plan"],
        ["Crews, as recorded over every day of the counts", round(S["recorded_crew"], 2), "for comparison"],
        ["All field employees, as recorded", round(S["recorded"], 2), "for comparison"]], [46, 10, 48],
        [None, "0.00", None])
    rows = [["%d to %d" % (lo, hi - 1), int(n), r0(e), round(r, 2)] for lo, hi, n, e, r in F["bins"]]
    _table(ws3, 10, ["Day of the crew's count", "Recordables", "Hours worked", "Rate"], rows, None,
           [None, "0", "#,##0", "0.00"])
    ws4 = wb.create_sheet("Notes")
    for i, t in enumerate([
        "Recordable injuries are cases meeting 29 CFR 1904.7, as the case records finally classify them; "
        "recurrences linked to an earlier case are not new cases (29 CFR 1904.6).",
        "Hours worked are regular and overtime hours on Pinewater work; paid leave, holiday pay and mutual-aid hours "
        "are excluded, and prior-period adjustments are counted in the pay period they correct.",
        "Each crew's count runs from 11 January 2021 (HR-14 Revision 2) and restarts the day after a recordable "
        "injury to any member or the day after its 90th day.",
        "First-aid cases count each injury once: a nurse-line case is the injury of the supervisor's case for the "
        "same worker dated up to three days before the call; each injury is placed in the district of the worker's "
        "crew or team on its injury date.",
        "The 2027 hours are the work plan of 15 October 2026."], start=1):
        ws4.cell(row=i, column=1, value=t)
    ws4.column_dimensions["A"].width = 120
    wb.save(path)
    PP.normalize_ooxml(path, W.PEOPLE["director"], W.PEOPLE["director"], "2026-10-19T16:12:00Z", "2026-10-23T15:20:00Z",
                       excel=True, company=W.COMPANY)


def chart(path, F):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    S = summary(F)
    g = F["gold"]
    q = ["Q1", "Q2", "Q3", "Q4"]
    limit = [W.LIMIT * h / W.RATE_BASE for h in S["qhours"]]
    recorded = [S["recorded"] * h / W.RATE_BASE for h in S["qhours"]]
    fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=120)
    ax.bar(q, g["quarters"], color="#7A2E1F", width=0.55, label="2027 forecast")
    ax.plot(q, limit, color="#1B4D3E", marker="_", markersize=34, linestyle="none", markeredgewidth=2.4,
            label="Recordables the 3.0 limit allows")
    ax.plot(q, recorded, color="#999999", marker="_", markersize=34, linestyle="none", markeredgewidth=1.6,
            label="At the 2021-2026 recorded rate")
    for i, v in enumerate(g["quarters"]):
        ax.text(i, v + 1.2, "%d" % r0(v), ha="center", fontsize=9)
    ax.set_ylabel("Recordable injuries")
    ax.set_ylim(0, max(g["quarters"]) * 1.25)
    ax.set_title("Redbud on Pinewater work: 2027 recordable injuries by quarter", fontsize=11)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=8.5, loc="lower right")
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def write(golden_dir, F):
    os.makedirs(golden_dir, exist_ok=True)
    memo(os.path.join(golden_dir, MEMO), F)
    workbook(os.path.join(golden_dir, BOOK), F)
    chart(os.path.join(golden_dir, CHART), F)
