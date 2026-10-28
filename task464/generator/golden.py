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
    coded_n = {c: round(f["coded_share_pct"][c] / 100.0 * f["withdrawals_total"]) for c in W.CODES}

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
    ws["A1"] = "%s withdrawal review %s" % (W.SERVICE, W.YEAR)
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Reasons behind %s withdrawals across the four terms. Shares to one decimal place." % (
        format(f["withdrawals_total"], ","))
    ws["A2"].font = Font(size=9, italic=True)
    ws["A4"] = "2027 retention budget line RET-01 targets: %s" % f["call_label"]
    ws["A4"].font = Font(bold=True, size=11)
    ws["A5"] = ("%s at %.1f per cent of the year's withdrawals, ahead of %s at %.1f, a gap of %.1f points."
                % (f["call_label"], f["call_share_pct"], f["runner_up_label"],
                   f["runner_up_share_pct"], f["gap_points"]))
    ws["A5"].font = Font(size=9)
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
    first, last = hr + 1, hr + len(order)
    ws.append(["Total", sum(coded_n[c] for c in order), None,
               round(sum(f["corrected_share_pct"][c] for c in order), 1)])
    for c in ws[ws.max_row]:
        c.font = Font(bold=True)
    for col, wd in zip("ABCD", (30, 20, 18, 24)):
        ws.column_dimensions[col].width = wd
    for row in ws.iter_rows(min_row=first, max_row=ws.max_row, min_col=3, max_col=4):
        for c in row:
            c.number_format = "0.0"

    ch = BarChart()
    ch.type = "bar"
    ch.title = "Share of %s withdrawals by reason" % W.YEAR
    ch.y_axis.title = "Per cent of withdrawals"
    ch.x_axis.title = "Reason"
    ch.add_data(Reference(ws, min_col=4, min_row=hr, max_row=last), titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=1, min_row=first, max_row=last))
    ch.height, ch.width = 9, 17
    ch.legend = None
    ws.add_chart(ch, "F7")

    ws2 = wb.create_sheet("Supporting figures")
    ws2.append(["Curriculum area", "Enrolments %s" % W.YEAR, "Planned guided hours (nearest 10)"])
    for c in ws2[1]:
        c.font = Font(bold=True)
    for a in W.CURRICULUM:
        d = f["ask1_curriculum"][a]
        ws2.append([a, d["enrolments"], d["planned_hours_nearest_10"]])
    ws2.append([])
    ws2.append(["Centre", "Enrolments completed (%)"])
    ws2[ws2.max_row][0].font = Font(bold=True)
    ws2[ws2.max_row][1].font = Font(bold=True)
    for k, v in f["ask2_completion_pct"].items():
        ws2.append([k, v])
    ws2.append([])
    ws2.append(["Reason code", "Moderated comments placed in a different category"])
    ws2[ws2.max_row][0].font = Font(bold=True)
    ws2[ws2.max_row][1].font = Font(bold=True)
    for c in W.CODES:
        ws2.append([c, f["ask3_changed_on_moderation"][c]])
    ws2.append(["Total", f["ask3_changed_total"]])
    ws2[ws2.max_row][0].font = Font(bold=True)
    ws2[ws2.max_row][1].font = Font(bold=True)
    for col, wd in zip("ABC", (30, 26, 34)):
        ws2.column_dimensions[col].width = wd
    wb.save(os.path.join(GOLD, "retention_target_2027.xlsx"))
    print("  golden/retention_target_2027.xlsx")


if __name__ == "__main__":
    main()
