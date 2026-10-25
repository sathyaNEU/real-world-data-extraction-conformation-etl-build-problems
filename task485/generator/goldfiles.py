"""The golden deliverables: the review's electorate forecast workbook (each ward's 2032 electors, electors per
councillor, variance and finding, the 2021 register by ward, the build-up the forecast uses, notes) and the chart of
each ward's 2032 variance against the 10 per cent lines; returns every figure the write-up states."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402
import openpyxl  # noqa: E402
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side  # noqa: E402
from openpyxl.utils import get_column_letter  # noqa: E402

import golden as G  # noqa: E402

BOLD = Font(bold=True)
HEAD_FILL = PatternFill("solid", fgColor="DCE6F1")
TOTAL_FILL = PatternFill("solid", fgColor="F2F2F2")
OUT_FILL = PatternFill("solid", fgColor="FCE4D6")
TOP = Border(top=Side(style="thin"))
WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 18: "18"}


def _head(ws, row):
    for c in ws[row]:
        c.font = BOLD
        c.fill = HEAD_FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")


def finding(v):
    if v > 10:
        return "Outside: above the average"
    if v < -10:
        return "Outside: below the average"
    return "Within 10 per cent"


def write(path, target):
    L = G.load(target)
    e, S, c = G.forecast(L)
    v, avg, tot = G.verdicts(L, e)
    wards = L["wards"]
    order = list(wards)
    fail = [w for w in order if abs(v[w]) > 10]
    meet = [w for w in order if w not in fail]
    reg25 = G.ward_totals(L, 2025)
    A = G.ask_a(target, wards)
    dflt_e = G.default_path(L)
    dv, davg, dtot = G.verdicts(L, dflt_e)
    dfail = [w for w in order if abs(dv[w]) > 10]
    traj = G.trajectory_years(L)
    switch = G.switch_off_net(target, wards)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Electoral equality 2032"
    ws.append(["Lorrimere District: electoral equality on the forecast for the register to be published 1 December 2032"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Existing wards and councillor numbers (the 2014 order), council size 43. %s wards lie more than 10 per cent "
               "from the district average of %s electors per councillor." % (WORDS[len(fail)].capitalize(),
                                                                              "{:,.0f}".format(round(avg)))])
    ws.append([])
    ws.append(["Ward code", "Ward", "Councillors", "Electors, 1 December 2025 register", "Forecast electors, 1 December 2032",
               "Electors per councillor, 2032", "Variance from average, 2032 (%)", "Finding"])
    _head(ws, 4)
    for w in order:
        name, cl = wards[w]
        ws.append([w, name, cl, reg25[w], round(e[w]), round(e[w] / cl), round(v[w], 1), finding(v[w])])
        if w in fail:
            for cell in ws[ws.max_row]:
                cell.fill = OUT_FILL
    last = ws.max_row
    ws.append([None, "Lorrimere District", "=SUM(C5:C%d)" % last, "=SUM(D5:D%d)" % last, "=SUM(E5:E%d)" % last,
               "=E%d/C%d" % (last + 1, last + 1), None, None])
    for cell in ws[ws.max_row]:
        cell.font = BOLD
        cell.fill = TOTAL_FILL
        cell.border = TOP
    for r in range(5, ws.max_row + 1):
        ws.cell(r, 4).number_format = "#,##0"
        ws.cell(r, 5).number_format = "#,##0"
        ws.cell(r, 6).number_format = "#,##0"
        ws.cell(r, 7).number_format = "+0.0;-0.0;0.0"
        for col in (3, 4, 5, 6, 7):
            ws.cell(r, col).alignment = Alignment(horizontal="right")
    ws.append([])
    ws.append(["Source: Lorrimere District Council registers of 1 December 2022 to 2025, local land and property gazetteer "
               "at 12 October 2026, housing completions monitoring and housing trajectory at 30 September 2026."])
    ws.freeze_panes = "C5"
    for i, wd in enumerate([10, 22, 12, 18, 18, 16, 16, 28]):
        ws.column_dimensions[get_column_letter(i + 1)].width = wd
    ws.row_dimensions[4].height = 45
    ws.print_title_rows = "4:4"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1

    w2 = wb.create_sheet("Register 2021")
    w2.append(["Local government electors on the register published 1 December 2021, by ward"])
    w2["A1"].font = Font(bold=True, size=12)
    w2.append(["The register as published, from Electra's report of the register it held on 4 March 2022 less the "
               "notices of alteration of 4 January, 1 February and 1 March 2022."])
    w2.append([])
    w2.append(["Ward code", "Ward", "Councillors", "Local government electors, 1 December 2021"])
    _head(w2, 4)
    for w in order:
        name, cl = wards[w]
        w2.append([w, name, cl, A[w]])
    last2 = w2.max_row
    w2.append([None, "Lorrimere District", "=SUM(C5:C%d)" % last2, "=SUM(D5:D%d)" % last2])
    for cell in w2[w2.max_row]:
        cell.font = BOLD
        cell.fill = TOTAL_FILL
        cell.border = TOP
    for r in range(5, w2.max_row + 1):
        w2.cell(r, 4).number_format = "#,##0"
    w2.freeze_panes = "C5"
    for i, wd in enumerate([10, 22, 12, 22]):
        w2.column_dimensions[get_column_letter(i + 1)].width = wd
    w2.row_dimensions[4].height = 30

    w3 = wb.create_sheet("Build-up")
    w3.append(["Electors per dwelling by canvasses since a dwelling came into use, as a share of the settled level"])
    w3["A1"].font = Font(bold=True, size=12)
    w3.append(["Registers of 1 December 2022 to 2025 at the dwellings in the completions monitoring; the settled level "
               "from the 2025 register at dwellings at their seventh canvass or later."])
    w3.append([])
    w3.append(["Canvasses by the register", "Share of the settled level"])
    _head(w3, 4)
    for k in sorted(c):
        w3.append(["%d (rolling registration only)" % k if k == 0 else k, round(c[k], 3)])
    w3.append(["7 or more", 1.0])
    for r in range(5, w3.max_row + 1):
        w3.cell(r, 2).number_format = "0.000"
        w3.cell(r, 1).alignment = Alignment(horizontal="left")
    w3.append([])
    w3.append(["Settled level, electors per dwelling", None])
    w3.cell(w3.max_row, 1).font = BOLD
    w3.append(["Houses (RD02 to RD04)", round(S["house"], 2)])
    w3.append(["Flats (RD06)", round(S["flat"], 2)])
    w3.column_dimensions["A"].width = 34
    w3.column_dimensions["B"].width = 18

    w4 = wb.create_sheet("Notes")
    for line in [
        "Electors: local government electors aged 18 or over on the revised register; attainers and overseas electors "
        "registered for parliamentary elections only are not counted, electors registered for local elections only are "
        "(technical guidance note 3, section 1).",
        "Forecast date: the register to be published on 1 December 2032 (the Commission's letter of 2 March 2026).",
        "Dwellings counted: every dwelling in use today and the dwellings the housing trajectory at 30 September 2026 "
        "expects by the 2032 register, completions falling evenly through each monitoring year and each year's mix the "
        "site's remaining mix; dwellings the trajectory places after 31 March 2033 are not counted.",
        "A dwelling is first canvassed in the year it is in use on 31 August, and applications determined by 31 October "
        "reach the register published on 1 December (annual canvass report 2025).",
        "Each dwelling at its seventh canvass or later on the 2025 register is carried at its 2025 count; every younger "
        "dwelling, and every dwelling in use since or to come, at the settled level of its type times the share its "
        "canvass count on 1 December 2032 holds on the Build-up sheet.",
        "Variance: a ward's electors per councillor against the district's forecast electors over 43 councillors. A ward "
        "more than 10 per cent above or below does not provide good electoral equality (guidance, section 2).",
        "Forecast electors are shown to the nearest elector; findings are taken on unrounded figures.",
        "Prepared for the Commission's meeting of 17 November 2026. Review Manager: Megan Stewart."]:
        w4.append([line])
        w4.cell(w4.max_row, 1).alignment = Alignment(wrap_text=True, vertical="top")
    w4.column_dimensions["A"].width = 120
    wb.save(path("workbook"))

    # the chart: each ward's variance, the wards outside the line marked, the lines labelled
    rows = sorted(order, key=lambda w: v[w])
    fig, ax = plt.subplots(figsize=(8.6, 7.4), dpi=150)
    cols = ["#c0504d" if w in fail else "#8497b0" for w in rows]
    ax.barh(range(len(rows)), [v[w] for w in rows], color=cols, height=0.62, edgecolor="white", linewidth=1.0)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([wards[w][0] for w in rows], fontsize=8.5)
    for x in (-10, 10):
        ax.axvline(x, color="#404040", linestyle=(0, (4, 3)), linewidth=1.0)
        ax.text(x, len(rows) - 0.35, "%+d%%" % x, ha="center", va="bottom", fontsize=8, color="#404040")
    ax.axvline(0, color="#7f7f7f", linewidth=0.8)
    for i, w in enumerate(rows):
        if w in fail:
            ax.text(v[w] + (0.4 if v[w] > 0 else -0.4), i, "%+.1f" % v[w], va="center",
                    ha="left" if v[w] > 0 else "right", fontsize=8, color="#262626")
    ax.set_xlim(-18, 20)
    ax.set_ylim(-0.7, len(rows) - 0.1)
    ax.set_xlabel("Variance from the district's average electors per councillor, 1 December 2032 forecast (per cent)",
                  fontsize=8.5)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: "%+d" % x if x else "0"))
    ax.tick_params(axis="x", labelsize=8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="x", color="#e7e7e7", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.set_title("%s of Lorrimere's 23 wards fall outside electoral equality on the 2032 forecast" %
                 WORDS[len(fail)].capitalize(), fontsize=11, loc="left", pad=14)
    fig.text(0.01, 0.028, "Existing wards and councillor numbers; district average %s electors per councillor. Red: more "
             "than 10 per cent from the average." % "{:,.0f}".format(round(avg)), fontsize=6.8, color="#595959")
    fig.text(0.01, 0.008, "Source: Lorrimere District Council registers 2022 to 2025, gazetteer at 12 October 2026, "
             "completions monitoring and housing trajectory at 30 September 2026.", fontsize=6.8, color="#595959")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(path("chart"), metadata={"Software": None})
    plt.close(fig)

    def r1(x):
        return round(x, 1)
    figs = dict(
        call=dict(fail=[wards[w][0] for w in fail], meet=[wards[w][0] for w in meet], fail_codes=fail,
                  findings={wards[w][0]: finding(v[w]) for w in order}),
        components=dict(electors_2025="{:,}".format(sum(reg25.values())), trajectory_dwellings="{:,}".format(traj)),
        forecast=dict(total="{:,}".format(round(tot)), average="{:,.1f}".format(avg), average_whole="{:,}".format(round(avg)),
                      variance={wards[w][0]: r1(v[w]) for w in order},
                      electors={wards[w][0]: round(e[w]) for w in order}),
        default=dict(fail=[wards[w][0] for w in dfail], variance={wards[w][0]: r1(dv[w]) for w in order}),
        buildup={str(k): round(c[k], 2) for k in sorted(c)}, settled={t: round(x, 2) for t, x in S.items()},
        ask_a={wards[w][0]: A[w] for w in order}, ask_a_total="{:,}".format(sum(A.values())),
        switch_off=dict(net=switch["net"], low=switch["low"], high=switch["high"]),
        constants=dict(council_size=43, councillors={wards[w][0]: wards[w][1] for w in order},
                       order=[wards[w][0] for w in order]))
    return figs
