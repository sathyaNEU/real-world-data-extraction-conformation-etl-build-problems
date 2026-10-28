"""task464 architecture 8: the golden deliverables. Every figure comes from answers.figures()."""
import csv, os
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
import world as W
import answers

GOLD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "golden")


def main():
    import shutil
    if os.path.isdir(GOLD):
        shutil.rmtree(GOLD)
    os.makedirs(GOLD, exist_ok=True)
    f = answers.figures()
    order = sorted(W.CODES, key=lambda c: -f["corrected_share_pct"][c])
    coded_n = f["coded_counts"]

    path = os.path.join(GOLD, "withdrawal_reason_composition_2025_26.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["reason_code", "reason", "withdrawals_coded", "coded_share_pct",
                    "share_of_withdrawals_pct"])
        for c in order:
            w.writerow([c, W.LABEL[c], coded_n[c], "%.1f" % f["coded_share_pct"][c],
                        "%.1f" % f["corrected_share_pct"][c]])
    print("  golden/withdrawal_reason_composition_2025_26.csv")

    wb = Workbook()
    ws = wb.active
    ws.title = "Reason composition"
    ws["A1"] = ("RET-01 should target %s: %.1f per cent of %s withdrawals"
                % (f["call_label"].lower(), f["call_share_pct"], W.YEAR))
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("%s withdrawal review %s. %s withdrawals across the four terms at the five centres; "
                "shares to one decimal place." % (W.SERVICE, W.YEAR, format(f["withdrawals_total"], ",")))
    ws["A2"].font = Font(size=9, italic=True)
    ws["A4"] = ("%s %.1f per cent, ahead of %s at %.1f: a gap of %.1f points."
                % (f["call_label"], f["call_share_pct"], f["runner_up_label"].lower(),
                   f["runner_up_share_pct"], f["gap_points"]))
    ws["A4"].font = Font(bold=True, size=10)
    hdr = ["Reason", "Withdrawals coded", "Coded share (%)", "Share of withdrawals (%)"]
    ws.append([])
    ws.append(hdr)
    hr = ws.max_row
    for c in ws[hr]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="EDEDED")
        c.alignment = Alignment(wrap_text=True, vertical="bottom")
    for c in order:
        ws.append([W.LABEL[c], coded_n[c], f["coded_share_pct"][c], f["corrected_share_pct"][c]])
        if c == f["call"]:
            for cell in ws[ws.max_row]:
                cell.font = Font(bold=True)
    first, last = hr + 1, hr + len(order)
    ws.append(["All withdrawals", sum(coded_n[c] for c in order), None, None])
    for c in ws[ws.max_row]:
        c.font = Font(bold=True)
    ws.append([])
    ws.append(["Source: student record withdrawal exports (legacy system to winter 2025, Horizon SR v4 from "
               "spring 2026) and the %s coding moderation return." % W.YEAR])
    ws[ws.max_row][0].font = Font(size=8, italic=True, color="555555")
    ws.append(["The coded share is the code as first recorded. The share of withdrawals carries the "
               "moderating coder's split behind each code onto that code's count."])
    ws[ws.max_row][0].font = Font(size=8, italic=True, color="555555")
    for col, wd in zip("ABCD", (30, 18, 16, 22)):
        ws.column_dimensions[col].width = wd
    for row in ws.iter_rows(min_row=first, max_row=last + 1, min_col=2, max_col=2):
        for c in row:
            c.number_format = "#,##0"
    for row in ws.iter_rows(min_row=first, max_row=last, min_col=3, max_col=4):
        for c in row:
            c.number_format = "0.0"
    ws.freeze_panes = ws.cell(row=hr + 1, column=1)

    ch = BarChart()
    ch.type = "bar"
    ch.title = "%s leads the reasons for leaving" % f["call_label"]
    ch.y_axis.title = "Per cent of %s withdrawals" % W.YEAR
    ch.y_axis.numFmt = "0"
    ch.y_axis.majorGridlines = None
    ch.x_axis.title = None
    ch.add_data(Reference(ws, min_col=4, min_row=hr, max_row=last), titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=1, min_row=first, max_row=last))
    ch.x_axis.scaling.orientation = "maxMin"
    ser = ch.series[0]
    ser.graphicalProperties.solidFill = "9AA5B1"
    ser.graphicalProperties.line.solidFill = "9AA5B1"
    from openpyxl.chart.marker import DataPoint
    from openpyxl.chart.label import DataLabelList
    pt = DataPoint(idx=order.index(f["call"]))
    pt.graphicalProperties.solidFill = "1F5F8B"
    pt.graphicalProperties.line.solidFill = "1F5F8B"
    ser.dPt.append(pt)
    ser.dLbls = DataLabelList()
    ser.dLbls.showVal = True
    ser.dLbls.numFmt = "0.0"
    ch.height, ch.width = 8.5, 16
    ch.legend = None
    ws.add_chart(ch, "F6")

    ws2 = wb.create_sheet("Provision 2025-26")
    ws2["A1"] = "Learner-courses the five centres started in %s" % W.YEAR
    ws2["A1"].font = Font(bold=True, size=11)
    ws2["A2"] = "A learner-course is one learner on one course, however many terms it runs."
    ws2["A2"].font = Font(size=9, italic=True)
    ws2.append([])
    ws2.append(["Curriculum area", "Planned guided hours"])
    for c in ws2[ws2.max_row]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="EDEDED")
    for a in W.CURRICULUM:
        ws2.append([a, f["ask1_planned_hours"][a]])
        ws2.cell(row=ws2.max_row, column=2).number_format = "#,##0"
    ws2.append(["All areas", sum(f["ask1_planned_hours"].values())])
    ws2.cell(row=ws2.max_row, column=2).number_format = "#,##0"
    for c in ws2[ws2.max_row]:
        c.font = Font(bold=True)
    ws2.append([])
    ws2.append(["Centre", "Learner-courses started", "Completed (%)"])
    for c in ws2[ws2.max_row]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="EDEDED")
    for k in sorted(f["ask2_started"]):
        ws2.append([k, f["ask2_started"][k], f["ask2_completed_pct"][k]])
        ws2.cell(row=ws2.max_row, column=2).number_format = "#,##0"
        ws2.cell(row=ws2.max_row, column=3).number_format = "0.0"
    ws2.append([])
    ws2.append(["Source: enrolments_2025_26 and the 2025/26 course catalogue, the five centres in the site "
                "directory; subcontracted delivery excluded."])
    ws2[ws2.max_row][0].font = Font(size=8, italic=True, color="555555")
    for col, wd in zip("ABC", (32, 24, 16)):
        ws2.column_dimensions[col].width = wd

    ws3 = wb.create_sheet("Notes")
    notes = [
        ("As at", W.ASOF),
        ("Withdrawals", "Every withdrawal recorded across the four terms of %s, once each. Winter withdrawals "
                        "keyed after the legacy system closed appear in both exports and are counted once."
                        % W.YEAR),
        ("Reason codes", "The six codes of the Exit Comment Coding Manual, version 4.2. Codes typed in the "
                         "legacy system are read without regard to case or trailing spaces."),
        ("Moderation", "The quality team moderates every withdrawal coded OT and 400 of each other code. The "
                       "return is read code by code; its own mix is not the year's."),
        ("Learner-courses", "Courses running across the move to Horizon SR v4 were closed after the winter term "
                            "and opened again for spring under a new reference. Both halves are one "
                            "learner-course, placed at the centre where it started."),
        ("Rounding", "Shares to one decimal place, hours in whole hours, each from unrounded counts."),
    ]
    ws3.append(["Item", "Note"])
    for c in ws3[1]:
        c.font = Font(bold=True)
    for k, v in notes:
        ws3.append([k, v])
        ws3.cell(row=ws3.max_row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ws3.cell(row=ws3.max_row, column=1).alignment = Alignment(vertical="top")
    ws3.column_dimensions["A"].width = 18
    ws3.column_dimensions["B"].width = 96
    wb.properties.creator = W.PEOPLE["retention_lead"]
    wb.properties.lastModifiedBy = W.PEOPLE["retention_lead"]
    wb.save(os.path.join(GOLD, "retention_target_2027.xlsx"))
    print("  golden/retention_target_2027.xlsx")


if __name__ == "__main__":
    main()
