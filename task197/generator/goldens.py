"""task197: the two golden deliverables."""
import os, datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.chart import BarChart, Reference, LineChart
from openpyxl.utils import get_column_letter
import sim, docs

THIN = Side(style="thin", color="D9D9D9")

def _head(ws, row, cells, width=None):
    ws.append(cells)
    for c in ws[row]:
        c.font = Font(bold=True, size=10)
        c.alignment = Alignment(wrap_text=True, vertical="bottom")
        c.fill = PatternFill("solid", fgColor="F2F2F2")
        c.border = Border(bottom=THIN)

def workbook(path, F):
    wb = Workbook()
    ws = wb.active; ws.title = "Scorecard"
    ws["A1"] = "Realised response gain against contract, qualifying under-frequency episodes"
    ws["A1"].font = Font(bold=True, size=11)
    ws["A2"] = "Review window %s to %s. Tolerance %.0f per cent of contracted gain. Prepared %s." % (
        F["window_from"], F["window_to"], F["tolerance"], F["as_of"])
    ws["A2"].font = Font(size=9, italic=True)
    ws.append([])
    _head(ws, 4, ["Site", "Name", "Contracted FCR (MW)", "Contracted gain (MW/Hz)",
                  "Realised gain (% of contract)", "Qualifying episodes", "Under tolerance"])
    for r in F["scorecard"]:
        ws.append([r["site"], r["name"], r["cap"], r["contract_gain"], r["gain_pct"], r["episodes"],
                   "yes" if r["under"] else "no"])
        for col in ("C", "D", "E"):
            ws["%s%d" % (col, ws.max_row)].number_format = "0.0#" if col != "E" else "0"
    n = len(F["scorecard"])
    ws.append([])
    ws.append(["Withdrawn for %s" % F["delivery_month"], F["call_name"], "", "", F["call_gain"], "", ""])
    ws.append(["Runner-up", F["runner_name"], "", "", F["runner_gain"], "", ""])
    ws.append(["Gap (percentage points)", "", "", "", F["gap_pp"], "", ""])
    for row in (6 + n, 7 + n, 8 + n):
        ws.cell(row=row, column=1).font = Font(bold=True)
    for col, w in zip("ABCDEFG", (12, 15, 14, 14, 16, 13, 12)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A5"
    ch = BarChart(); ch.type = "col"; ch.style = 2
    ch.title = "Realised response gain against contract, under-frequency episodes"
    ch.y_axis.title = "Per cent of contracted gain"; ch.x_axis.title = "Site"
    data = Reference(ws, min_col=5, min_row=4, max_row=4 + n)
    cats = Reference(ws, min_col=2, min_row=5, max_row=4 + n)
    ch.add_data(data, titles_from_data=True); ch.set_categories(cats)
    ch.y_axis.scaling.min = 60; ch.y_axis.scaling.max = 100
    ws2 = wb.create_sheet("Tolerance line")
    ws2["A1"] = "Tolerance"; ws2["A2"] = F["tolerance"]
    for i in range(n):
        ws2.cell(row=2 + i, column=1, value=F["tolerance"])
    ln = LineChart()
    ln.add_data(Reference(ws2, min_col=1, min_row=1, max_row=1 + n), titles_from_data=True)
    ch += ln
    ch.height, ch.width = 9.5, 20
    ws.add_chart(ch, "I4")
    ws2.sheet_state = "hidden"

    wd = wb.create_sheet("Down regulation")
    wd["A1"] = "Realised response gain against contract, qualifying over-frequency episodes"
    wd["A1"].font = Font(bold=True, size=11)
    wd.append([]); wd.append([])
    _head(wd, 3, ["Site", "Name", "Realised gain (% of contract)", "Qualifying episodes"])
    for r in F["down"]:
        wd.append([r["site"], r["name"], r["gain_pct"] if r["gain_pct"] is not None else "none",
                   r["episodes"]])
        if r["gain_pct"] is not None:
            wd["C%d" % wd.max_row].number_format = "0"
    for col, w in zip("ABCD", (12, 15, 18, 14)):
        wd.column_dimensions[col].width = w

    wa = wb.create_sheet("Block availability")
    wa["A1"] = "Reserve capacity hours committed and held available, review window"
    wa["A1"].font = Font(bold=True, size=11)
    wa.append([]); wa.append([])
    _head(wa, 3, ["Block", "Local hours", "Committed (MWh)", "Held available (MWh)", "Shortfall (MWh)"])
    for r in F["availability"]:
        wa.append([r["block"], r["hours"], r["committed"], r["available"], r["shortfall"]])
        for col in ("C", "D", "E"):
            wa["%s%d" % (col, wa.max_row)].number_format = "0.0"
    for col, w in zip("ABCDE", (10, 14, 17, 18, 16)):
        wa.column_dimensions[col].width = w

    we = wb.create_sheet("Imbalance exposure")
    we["A1"] = "Energy delivered against programme outside reserve commitment, review window"
    we["A1"].font = Font(bold=True, size=11)
    we["A2"] = ("Settlement periods for which the site held no delivery-block commitment. "
                "Clause 5 of the performance standard.")
    we["A2"].font = Font(size=9, italic=True)
    we.append([])
    _head(we, 4, ["Site", "Name", "Above programme (MWh)", "Below programme (MWh)"])
    for r in F["exposure"]:
        we.append([r["site"], r["name"], r["above"], r["below"]])
        for col in ("C", "D"):
            we["%s%d" % (col, we.max_row)].number_format = "0.0"
    we.append([])
    we.append(["Portfolio", "", F["exposure_above_total"], F["exposure_below_total"]])
    we.cell(row=we.max_row, column=1).font = Font(bold=True)
    for col, w in zip("ABCD", (12, 15, 22, 22)):
        we.column_dimensions[col].width = w

    wn = wb.create_sheet("Notes")
    for line in [
            ["Reserve performance scorecard, November 2026 determination"],
            ["Prepared by the reserve portfolio desk on 2026-10-13. Review window 2026-09-21 to"],
            ["2026-10-11 inclusive, which is the reserve quarter to the last delivery date before"],
            ["the determination."],
            [""],
            ["Realised response gain is clause 2 of the performance standard: power delivered in"],
            ["excess of the output the site would have produced at that second had the frequency"],
            ["stayed inside the dead band, per hertz beyond the dead band, taken at the extreme"],
            ["second of each qualifying episode, averaged with equal weight, as a percentage of the"],
            ["site's contracted capacity divided by 190 mHz. Reported to the nearest whole per cent."],
            [""],
            ["Out of scope: episodes in a settlement period the site was not committed to, and the"],
            ["parts of a block in which the site was not holding reserve. Upward and downward"],
            ["response are reported separately and are never averaged together."],
            [""],
            ["Capacity hours and energies are in MWh to one decimal place, summed over the window's"],
            ["delivery dates and rounded once. Episode counts are whole."],
            [""],
            ["Meppelerdiep had no qualifying over-frequency episode in the window, so its"],
            ["down-regulation gain is reported as none rather than as zero."],
            [""],
            ["The Oosterhout metering point was replaced at the connection with effect from"],
            ["2026-10-01; both codes are its own and both are included."],
        ]:
        wn.append(line)
    wn.column_dimensions["A"].width = 92
    wb.properties.creator = "Veerkracht Flex"; wb.properties.lastModifiedBy = "Veerkracht Flex"
    wb.properties.created = dt.datetime(2026, 10, 13, 7, 12, 0)
    wb.properties.modified = dt.datetime(2026, 10, 13, 9, 38, 0)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wb.save(path)
    docs.normalise_zip(path)


def memo(path, F):
    sc = F["scorecard"]
    out = []
    w = out.append
    w("# Reserve withdrawal determination, %s delivery month" % F["delivery_month"])
    w("")
    w("Reserve portfolio desk, %s. Notification to %s due %s." % (F["as_of"], F["tso"], F["filing_due"]))
    w("")
    w("## Determination")
    w("")
    w("%s (%s) comes out of the reserve portfolio for %s and takes the month's re-prequalification slot. "
      "Over the review window it delivered **%.0f per cent** of the response its contracted characteristic "
      "requires, against a tolerance of %.0f per cent." % (F["call_name"], F["call_site"],
      F["delivery_month"], F["call_gain"], F["tolerance"]))
    w("")
    w("The runner-up is %s (%s) at %.0f per cent, %.0f percentage points above %s, so the choice of site is "
      "not close enough to turn on any single episode." % (F["runner_name"], F["runner_site"],
      F["runner_gain"], F["gap_pp"], F["call_name"]))
    w("")
    w("## Scorecard")
    w("")
    w("| Site | Contracted FCR (MW) | Realised gain (%) | Qualifying episodes | Under tolerance |")
    w("|---|---|---|---|---|")
    for r in sc:
        w("| %s %s | %.2f | %.0f | %d | %s |" % (r["site"], r["name"], r["cap"], r["gain_pct"],
                                                 r["episodes"], "yes" if r["under"] else "no"))
    w("")
    others = [r for r in sc if r["under"] and r["site"] != F["call_site"]]
    words = {0: "No", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five"}
    w("%s further site%s sit%s under tolerance: %s. None of them is close to %s, and under the technical "
      "conditions they carry at contracted capacity until a further test slot is offered." % (
          words.get(len(others), str(len(others))), "" if len(others) == 1 else "s",
          "s" if len(others) == 1 else "",
          ", ".join("%s at %.0f per cent" % (r["name"], r["gain_pct"]) for r in others), F["call_name"]))
    w("")
    w("## How the figure is built")
    w("")
    w("Each qualifying episode is read at its extreme second on the published one-second frequency. The "
      "response credited to a site is its recorded power at that second less the power its own programme was "
      "taking it to at that second, and the programme is moving: every site traverses between settlement "
      "period setpoints over a span its controller fixes, which the archive shows at the boundaries where no "
      "episode ran. Taking the undisturbed level before the episode instead of the moving programme credits "
      "each site with whatever its programme did during the episode, which is why %s reads %.0f per cent on "
      "that basis against %.0f per cent here." % (F["rung0_name"], F["rung0_pre"], F["rung0_traj"]))
    w("")
    w("## Down regulation, availability and imbalance")
    w("")
    w("Down-regulation gains are on the same characteristic and are reported in the workbook; %s is the "
      "lowest there too at %.0f per cent, and %s had no qualifying over-frequency episode in the window. "
      "Reserve capacity held available and the shortfall against commitment are per block in the workbook; "
      "the withdrawn hours are taken from the platform's own log timestamps, which sit ninety seconds after "
      "each window opens throughout the file; the start field agrees with that on the rows the alarm "
      "handler wrote and reads two hours early on the rest. Outside the blocks they were committed to, "
      "the sites "
      "delivered %.1f MWh above programme and %.1f MWh below it, which is the imbalance position the desk "
      "carried and is dominated by the traverse lag rather than by any site missing dispatch." % (
          F["down_low_name"], F["down_low_gain"], F["down_none_name"],
          F["exposure_above_total"], F["exposure_below_total"]))
    w("")
    w("## Next steps")
    w("")
    w("1. Notify %s of the withdrawal of %s before %s and carry it at zero contracted capacity from %s." % (
        F["tso"], F["call_site"], F["filing_due"], F["delivery_start"]))
    w("2. Book the witnessed step test and pull the droop settings the controller is running, against the "
      "settings declared after the firmware change of 15 September.")
    w("3. Keep the %s remaining under tolerance on the watch list and re-measure at the next "
      "determination." % ({0: "no sites", 1: "one site", 2: "two sites", 3: "three sites",
          4: "four sites"}.get(len(others), "%d sites" % len(others))))
    w("")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write("\n".join(out))
