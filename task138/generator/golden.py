"""The golden deliverable (dunraith_planning.xlsx, with its chart sheet) and figures.json, all from analysis.py
run on the cut pack."""
import json
import os

import openpyxl  # noqa: E402
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side  # noqa: E402

import analysis as A  # noqa: E402
import io_util as IO  # noqa: E402

BOOK = "dunraith_planning.xlsx"
HOT_F = 99.0


def r10(x):
    return int(round(x / 10.0)) * 10


def figures(S):
    f, wn, rr = S["filed"], S["wn"], S["relief"]
    gold = S["plans"]["golden"]
    days, peaks = S["days"], S["peaks"]
    out = {
        "call": {str(r["year"]): {"transfer_mw": r["transfer"], "planning_peak_mw": int(round(r["peak"]))}
                 for r in gold},
        "planning_peak_1dp": {str(r["year"]): round(r["peak"], 1) for r in gold},
        "weather_normal_mw": {str(r["year"]): round(r["weather_normal"], 1) for r in gold},
        "relief_mw": {str(r["year"]): round(r["relief_mw"], 1) for r in gold},
        "excess_mw": {str(r["year"]): round(r["peak"] - f.firm, 1) for r in gold},
        "weather_normal_2024_mw": round(wn["B"], 1),
        "slope_mw_per_f": round(wn["slope"], 2),
        "days_in_fit": wn["n_days"],
        "relief_pct": {"golden": round(100 * rr["golden"], 1), "all_hours": round(100 * rr["all_hours"], 1),
                       "daily_peak_hour": round(100 * rr["daily_peak_hour"], 1)},
        "hot_hours": {"on": rr["n_hot_on"], "off": rr["n_hot_off"]},
        "rungs_transfer_mw": {k: [r["transfer"] for r in v] for k, v in S["plans"].items()},
        "rungs_planning_peak_2027": {k: round(v[0]["peak"], 1) for k, v in S["plans"].items()},
        "bands": [{"from_f": lo, "to_f": hi, "relief_pct": round(100 * r, 1), "on": a, "off": b}
                  for lo, hi, r, a, b in A.relief_by_band(rr["P"])],
        "feeder_energy_mwh": {k: r10(v) for k, v in S["energy"].items()},
        "feeder_energy_total_mwh": r10(sum(S["energy"].values)),
        "hot_days": {d.strftime("%Y-%m-%d"): {"tmax_f": round(t, 1), "peak_mw": round(peaks[d][0], 1),
                                              "interval_end_local": (peaks[d][1] + A.pd.Timedelta(minutes=15))
                                              .strftime("%H:%M")}
                     for d, t in days.items()},
        "constants": {"firm_mw": f.firm, "design_f": f.design, "block_mw": f.block, "growth_pct": round(100 * f.growth, 2),
                      "threshold_f": f.threshold, "hot_f": HOT_F, "base_year": 2024, "window": "16:00 to 21:00",
                      "voltage_cut_pct": 3.5, "bandcenter_cvr_v": 119.2, "bandcenter_normal_v": 123.5,
                      "first_year": 2027, "last_year": 2031, "ten": 10},
        "ids": {"low_side_kv": 24.9, "line_kv": 69, "recorder_prefix": 41},
        "criteria_sections": [3.1, 3.2, 3.3, 4.1, 5],
    }
    return out


THIN = Side(style="thin", color="9AA5AD")
HEAD_FILL = PatternFill("solid", fgColor="DCE3E8")


def _head(ws, row, ncol):
    for c in range(1, ncol + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = Font(bold=True)
        cell.fill = HEAD_FILL
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        cell.border = Border(bottom=THIN)


def write_book(path, S, F):
    f = S["filed"]
    gold = S["plans"]["golden"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Capacity review"
    ws["A1"] = "Dunraith needs load transferred in every summer from 2027: 1.0 MW, rising to 5.0 MW by 2031"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("System Planning, capacity review for the 2027 construction work plan and budget. 27 October 2026. "
                "Distribution Planning Criteria rev 4, sections 3 and 4.")
    ws["A2"].font = Font(italic=True, color="4F5B62")
    hdr = ["Summer", "Weather-normal peak, feeders as run 2022 to 2026 (MW)", "CVR relief at the planning peak (MW)",
           "Planning peak (MW)", "Firm rating (MW)", "Excess over firm rating (MW)", "Transfer requirement (MW)"]
    ws.append([])
    ws.append(hdr)
    _head(ws, 4, len(hdr))
    for r in gold:
        ws.append([r["year"], round(r["weather_normal"], 1), round(r["relief_mw"], 1), int(round(r["peak"])), f.firm,
                   round(r["peak"] - f.firm, 1), r["transfer"]])
    for row in ws.iter_rows(min_row=5, max_row=9):
        row[0].number_format = "0"
        for c in row[1:3] + row[4:6]:
            c.number_format = "0.0"
        row[3].number_format = "0"
        row[6].number_format = "0.0"
        row[6].font = Font(bold=True)
    notes = [
        "",
        "Weather-normal peak: least-squares line of each summer day's highest hourly Dunraith load on the day's maximum "
        "temperature at Mossford airport, %d days at 85 F or more in 2022 to 2026, read at the 101 F design "
        "temperature (%.1f MW, the 2024 level) and carried at the base-case 0.95 per cent a year, compounded."
        % (F["days_in_fit"], F["weather_normal_2024_mw"]),
        "CVR relief: the 2027 operating plan runs CVR on every Dunraith feeder from 1 June 2027. Relief at the "
        "planning peak is %.1f per cent of load, from the 2025 pilot: DUN-2, DUN-5 and DUN-7 against DUN-1, DUN-3, "
        "DUN-4, DUN-6 and DUN-8, CVR hours against normal hours as the regulator log switched them, 16:00 to 21:00 "
        "on days at 99 F or more." % F["relief_pct"]["golden"],
        "Transfer requirement: excess over the 104.0 MW firm rating rounded up to whole 0.5 MW switching blocks. "
        "Planning peaks are shown to the nearest MW; the requirement is worked from the unrounded peak.",
    ]
    for n in notes:
        ws.append([n])
    for r in range(11, 14):
        ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=7)
        ws.row_dimensions[r].height = 44
    for c, w in zip("ABCDEFG", (9, 26, 20, 13, 12, 16, 16)):
        ws.column_dimensions[c].width = w
    ws.row_dimensions[4].height = 46
    ws.freeze_panes = "A5"

    wp = wb.create_sheet("CVR pilot 2025")
    wp.append(["Relief of the 3.5 per cent voltage cut by afternoon heat, 2025 pilot (16:00 to 21:00)"])
    wp["A1"].font = Font(bold=True, size=12)
    wp.append([])
    wp.append(["Day's maximum at Mossford airport", "CVR hours", "Normal hours", "Relief (per cent of load)"])
    _head(wp, 3, 4)
    for b in F["bands"]:
        lab = "%d F or more" % b["from_f"] if b["from_f"] >= 99 else "%d to %d F" % (b["from_f"], b["to_f"])
        if b["from_f"] < 85:
            lab = "under 85 F"
        wp.append([lab, b["on"], b["off"], b["relief_pct"]])
    for row in wp.iter_rows(min_row=4, max_row=3 + len(F["bands"])):
        row[3].number_format = "0.0"
    wp.append([])
    wp.append(["Carried to the planning peak", "", "", F["relief_pct"]["golden"]])
    wp.cell(row=wp.max_row, column=1).font = Font(bold=True)
    wp.cell(row=wp.max_row, column=4).font = Font(bold=True)
    wp.append(["For reference, not used: every pilot hour", "", "", F["relief_pct"]["all_hours"]])
    wp.append(["For reference, not used: each day's peak hour", "", "", F["relief_pct"]["daily_peak_hour"]])
    wp.append([])
    wp.append(["Relief is 1 less the ratio of the pilot feeders' load to the comparison feeders' load in CVR hours to "
               "that ratio in normal hours. Hours with a switch inside them and hours the historian marks Bad are left "
               "out. DUN-5 stayed at the normal setting in the week of 8 September (command not executed) and DUN-7 "
               "went to CVR at 09:40 on 14 July; both are taken from the regulator log."])
    wp.merge_cells(start_row=wp.max_row, start_column=1, end_row=wp.max_row, end_column=4)
    wp.cell(row=wp.max_row, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    wp.row_dimensions[wp.max_row].height = 58
    for c, w in zip("ABCD", (40, 11, 13, 24)):
        wp.column_dimensions[c].width = w

    we = wb.create_sheet("Feeder energy 2026")
    we.append(["Members' energy by feeder, 1 June to 30 September 2026 (MWh)"])
    we["A1"].font = Font(bold=True, size=12)
    we.append([])
    we.append(["Feeder", "Energy at members' meters (MWh)", "Note"])
    _head(we, 3, 3)
    note = {"DUN-1": "section beyond S-1302 counted here to 30 June",
            "DUN-3": "section beyond S-1302 counted here from 1 July",
            "DUN-4": "section beyond S-4471 counted here to 30 June",
            "DUN-8": "section beyond S-4471 counted here from 1 July",
            "DUN-6": "section beyond S-6120 counted here to 30 June",
            "DUN-2": "section beyond S-6120 counted here from 1 July",
            "DUN-5": "two LP-3 services on CT metering from 2 and 3 June",
            "DUN-7": "one LP-3 service on CT metering from 3 June"}
    for k, v in F["feeder_energy_mwh"].items():
        we.append([k, v, note.get(k, "")])
    we.append(["Total", F["feeder_energy_total_mwh"], "sum of unrounded feeder figures"])
    we.cell(row=we.max_row, column=1).font = Font(bold=True)
    we.cell(row=we.max_row, column=2).font = Font(bold=True)
    for row in we.iter_rows(min_row=4, max_row=we.max_row):
        row[1].number_format = "#,##0"
    we.append([])
    we.append(["Daily kWh from the meter data system times each meter's multiplier from the day the present meter "
               "was set (whole kWh before), on the feeder that served the transformer that day (SO-2026-114, "
               "30 June 2026, traced through the register's device connectivity)."])
    we.merge_cells(start_row=we.max_row, start_column=1, end_row=we.max_row, end_column=3)
    we.cell(row=we.max_row, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    we.row_dimensions[we.max_row].height = 44
    for c, w in zip("ABC", (9, 18, 46)):
        we.column_dimensions[c].width = w

    wh = wb.create_sheet("Hottest days 2026")
    wh.append(["The feeders' peak 15-minute demand on the ten hottest days of summer 2026"])
    wh["A1"].font = Font(bold=True, size=12)
    wh.append([])
    wh.append(["Date", "Maximum at Mossford airport (F)", "Peak 15-minute demand, T1 + T2 (MW)",
               "Interval ending (CDT)"])
    _head(wh, 3, 4)
    for d, v in sorted(F["hot_days"].items()):
        wh.append([d, v["tmax_f"], v["peak_mw"], v["interval_end_local"]])
    for row in wh.iter_rows(min_row=4, max_row=wh.max_row):
        row[1].number_format = "0.0"
        row[2].number_format = "0.0"
    wh.append([])
    wh.append(["MV-90 recorders 41-2207 and 41-2208 (the transformers' 24.9 kV side); 41-2391, the 69 kV line terminal, "
               "is not a feeder. UTC interval-ending stamps moved to CDT. The replacement recorder at the T2 cabinet "
               "(from 9 June, 10:40) stamps each interval at its start; its stamps are moved up 15 minutes."])
    wh.merge_cells(start_row=wh.max_row, start_column=1, end_row=wh.max_row, end_column=4)
    wh.cell(row=wh.max_row, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    wh.row_dimensions[wh.max_row].height = 58
    for c, w in zip("ABCD", (12, 18, 22, 14)):
        wh.column_dimensions[c].width = w
    wh.freeze_panes = "A4"

    from openpyxl.chart import BarChart, LineChart, Reference
    bar = BarChart()
    bar.type = "col"
    bar.title = "Dunraith's planning peak passes its 104.0 MW firm rating in every summer from 2027"
    bar.y_axis.title = "MW"
    bar.x_axis.title = "Summer"
    bar.add_data(Reference(ws, min_col=4, min_row=4, max_row=9), titles_from_data=True)
    bar.set_categories(Reference(ws, min_col=1, min_row=5, max_row=9))
    bar.y_axis.scaling.min = 100
    bar.y_axis.scaling.max = 111
    bar.y_axis.majorGridlines = None
    bar.gapWidth = 60
    line = LineChart()
    line.add_data(Reference(ws, min_col=5, min_row=4, max_row=9), titles_from_data=True)
    line.add_data(Reference(ws, min_col=2, min_row=4, max_row=9), titles_from_data=True)
    line.series[0].graphicalProperties.line.solidFill = "B03A2E"
    line.series[0].graphicalProperties.line.width = 28575
    line.series[1].graphicalProperties.line.solidFill = "8A5A1F"
    line.series[1].graphicalProperties.line.dashStyle = "dash"
    bar.series[0].graphicalProperties.solidFill = "2F6F8F"
    bar += line
    bar.legend.position = "b"
    bar.width, bar.height = 24, 13
    cs = wb.create_chartsheet("Chart")
    cs.add_chart(bar)
    wb.move_sheet("Chart", offset=-(len(wb.sheetnames) - 2))
    wb.save(path)
    IO.repack_ooxml(path, "Julie Gibbs", "Julie Gibbs", "2026-10-26T15:02:00Z", "2026-10-27T13:44:00Z",
                    "Dunraith capacity review 2027 to 2031", "Breckwater Electric Cooperative")


def write_all(target, golden, gen):
    os.makedirs(golden, exist_ok=True)
    S = A.solve(target)
    F = figures(S)
    write_book(os.path.join(golden, BOOK), S, F)
    json.dump(F, open(os.path.join(gen, "figures.json"), "w"), indent=1, sort_keys=True)
    return S, F
