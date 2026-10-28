"""task464 architecture 9: the golden deliverables, written from figures.json.

  statin_sessions_2027.xlsx       the seven practices ranked on the brief's figure, each practice's expected
                                  number to the nearest 10, the placement, the rates the run used, and a chart
  cvd_repeat_returns_2025.csv     the network's 2025 return, one row per practice in the specification's layout
"""
import csv, json, os
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.marker import DataPoint
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
import world as W

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOLD = os.path.join(BASE, "golden")
FIG = os.path.join(BASE, "generator", "figures.json")

THIN = Side(style="thin", color="BFBFBF")


def workbook(F):
    name = {p["code"]: p["name"] for p in W.PRACTICES}
    order = F["ranking"]
    call = F["call"]
    wb = Workbook()
    ws = wb.active
    ws.title = "Placement"
    ws["A1"] = "Statin continuity sessions go to %s, January to June 2027" % name[call]
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Hensey Vale PCN board, 10 December 2026. Network searches of 1 December 2026; figure as the "
                "board brief of 3 December 2026 defines it.")
    ws["A2"].font = Font(italic=True, size=9, color="52514E")
    ws.append([])
    hdr = ["", "Practice", "ODS code", "Patients issued a statin, Sep to Nov 2026",
           "Expected with no statin issued, Mar to Jun 2027"]
    ws.append(hdr)
    for c in ws[4]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="E9EEF5")
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = Border(bottom=THIN)
    for i, c in enumerate(order, 1):
        mark = "Sessions" if i == 1 else ("Next" if i == 2 else None)
        ws.append([mark, name[c], c, F["population"][c], F["expected_rounded"][c]])
        if c == call:
            for cell in ws[ws.max_row]:
                cell.font = Font(bold=True)
    tot = 5 + len(order)
    ws.cell(row=tot, column=2, value="Network")
    ws.cell(row=tot, column=4, value=F["population_total"])
    for cell in ws[tot]:
        cell.border = Border(top=THIN)
        cell.font = Font(bold=True)
    for row in ws.iter_rows(min_row=5, max_row=tot):
        row[3].number_format = "#,##0"
        row[4].number_format = "#,##0"
        row[0].alignment = Alignment(horizontal="center")
    ws.cell(row=tot + 2, column=1, value="Expected numbers rounded to the nearest 10, as the brief asks; the order "
                                         "follows the unrounded figures.").font = Font(size=9, color="52514E")
    for col, wd in zip("ABCDE", (9, 30, 11, 20, 24)):
        ws.column_dimensions[col].width = wd
    ws.row_dimensions[4].height = 44
    ws.freeze_panes = "A5"
    ws.print_title_rows = "4:4"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True

    ch = BarChart()
    ch.type = "bar"
    ch.style = 2
    ch.title = "%s has the most patients expected to go without a statin" % name[call].replace(" Surgery", "")
    ch.y_axis.title = "Patients, nearest 10"
    ch.y_axis.majorGridlines = None
    ch.x_axis.scaling.orientation = "maxMin"
    data = Reference(ws, min_col=5, min_row=4, max_row=4 + len(order))
    cats = Reference(ws, min_col=2, min_row=5, max_row=4 + len(order))
    ch.add_data(data, titles_from_data=True)
    ch.set_categories(cats)
    ch.legend = None
    ser = ch.series[0]
    ser.graphicalProperties.solidFill = "B8B6B0"
    ser.graphicalProperties.line.solidFill = "B8B6B0"
    for i, c in enumerate(order):
        if c == call:
            pt = DataPoint(idx=i)
            pt.graphicalProperties.solidFill = "2A78D6"
            pt.graphicalProperties.line.solidFill = "2A78D6"
            ser.dPt.append(pt)
    ch.dataLabels = DataLabelList()
    ch.dataLabels.showVal = True
    ch.dataLabels.showSerName = False
    ch.dataLabels.showCatName = False
    ch.dataLabels.showLegendKey = False
    ch.dataLabels.showPercent = False
    ch.dataLabels.position = "outEnd"
    ch.x_axis.delete = False
    ch.y_axis.delete = False
    ch.gapWidth = 60
    ch.height = 8.5
    ch.width = 17
    ws.add_chart(ch, "G4")

    ns = wb.create_sheet("Notes")
    notes = [
        ("Figure", "Patients registered with the practice on 30 November 2026 and issued a statin by it from 1 September "
                   "to 30 November 2026 who, still registered with the same practice on 30 June 2027, will have had no "
                   "statin issued to them from 1 March to 30 June 2027. Leavers and deaths are not counted; patients "
                   "first issued a statin after 30 November are not in the figure."),
        ("Source", "Issue, repeat authorisation and registration searches of both clinical systems, run 1 December 2026, "
                   "covering issues from 1 January 2024."),
        ("Run", "Each patient's current statin repeat run forward from its last issue to the request after its last "
                "authorised issue, at the record's mean request interval (%.1f days after supply runs out)." % F["pace_mean"]),
        ("Not re-authorised", "%s of %s statin repeats that ran out, January 2024 to July 2026 (%.1f%%)."
         % ("{:,}".format(F["reviews_not_renewed"]), "{:,}".format(F["reviews_measured"]), F["reauth_fail_pct"])),
        ("Stopped between reviews", "%.2f%% per 28 days of supply in a new start's first six months, %.2f%% after."
         % (F["stop_rate_early_pct"], F["stop_rate_late_pct"])),
        ("Already lapsed", "A repeat that ran out more than three weeks before the searches with no new repeat is "
                           "counted as not issued."),
        ("Still registered", "%.1f%% of the network's statin patients stay registered seven months, 2024 and 2025 "
                             "windows." % F["stay_pct"]),
    ]
    ns.append(["Item", "Note"])
    for c in ns[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="E9EEF5")
    for k, v in notes:
        ns.append([k, v])
    for row in ns.iter_rows(min_row=2):
        row[1].alignment = Alignment(wrap_text=True, vertical="top")
        row[0].alignment = Alignment(vertical="top")
    ns.column_dimensions["A"].width = 22
    ns.column_dimensions["B"].width = 100
    out = os.path.join(GOLD, "statin_sessions_2027.xlsx")
    wb.save(out)
    return out


def returns(F):
    out = os.path.join(GOLD, "cvd_repeat_returns_2025.csv")
    with open(out, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["ods_code", "r1_denominator", "r1_numerator", "r1_percent", "r2_denominator", "r2_numerator",
                     "r2_percent"])
        for c in sorted(F["ask_a"]):
            a = F["ask_a"][c]; b = F["ask_b"][c]
            wr.writerow([c, a["patients"], a["at_80"], "%.1f" % a["pct"], b["started"], b["overrun"], "%d" % b["pct"]])
    return out


def main():
    os.makedirs(GOLD, exist_ok=True)
    F = json.load(open(FIG, encoding="utf-8"))
    return [workbook(F), returns(F)]


if __name__ == "__main__":
    print(main())
