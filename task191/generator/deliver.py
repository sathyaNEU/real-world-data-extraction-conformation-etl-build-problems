"""The golden deliverables, figures.json and submission.md, every figure computed by estim.py from target/.

    python3 task191/generator/deliver.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import estim as E                                     # noqa: E402
from common import GOLDEN, TASK, normalise_zip, set_mtime   # noqa: E402

DOCX = "attention_programme_depots_2027.docx"
XLSX = "warning_response_by_depot_2026.xlsx"
SVG = "warning_response_2026.svg"
WEEKS = ["5 to 11 October", "12 to 18 October", "19 to 25 October", "26 October to 1 November"]
MONTHS = ["July", "August", "September", "October"]
PLACE_NAMES = {"FCW 42": "the bus-only underpass beneath the railway at Almadraba (line 27)",
               "PCW 15": "the bollard gate on the Vía Verde busway (line 40)",
               "PCW 26": "the Glorieta del Olivo (line 44, outbound to its terminus)",
               "FCW 34": "the bend on the Los Molinos link road (line 33)"}


def pct(x):
    return round(100 * x, 1)


def eur(x):
    return "{:,}".format(int(x))


def compute():
    D = E.load()
    c = E.call(D)
    r0, f0, *_ = E.rates(c["ws"])
    hours, _ = E.ask_a(D)
    count, paid, _ = E.ask_b(D)
    km, _ = E.ask_c(D)
    fp = []
    for p in sorted(c["false"], key=lambda p: -p["n"]):
        key = "%s %d" % ("PCW" if p["pcw"] > 0.5 else "FCW", int(round(p["speed"])))
        fp.append(dict(name=PLACE_NAMES.get(key, key), warnings=p["n"], passes=int(p["passes"]),
                       share_pct=pct(p["share"])))
    pz = [p for p in c["places"] if p["share"] < 0.1 and p["nobrake"] > 0.9][0]
    fig = {
        "call": {"depots": c["taken"], "closest": c["closest"],
                 "closest_ratio": round(c["res"][c["closest"]]["ratio"], 2), "line_ratio": 1.3},
        "fleet_rate_pct": pct(c["fleet"]), "fleet_warnings": c["n"], "fleet_not_braked": c["nobrake"],
        "depots": {d: dict(warnings=v["n"], not_braked=v["nobrake"], rate_pct=pct(v["rate"]),
                           ratio=round(v["ratio"], 2)) for d, v in c["res"].items()},
        "gap_to_line": round(1.3 - round(c["res"][c["closest"]]["ratio"], 2), 2),
        "false_places": fp,
        "false_place_warnings": sum(p["warnings"] for p in fp),
        "plaza": dict(warnings=pz["n"], passes=int(pz["passes"]), share_pct=pct(pz["share"]),
                      not_braked_pct=pct(pz["nobrake"])),
        "default_path": dict(depots=E.taken(r0), fleet_rate_pct=pct(f0),
                             ratios={d: round(v["ratio"], 2) for d, v in r0.items()}),
        "hours_on_service": hours,
        "at_fault_collisions": count,
        "claims_paid_eur": paid,
        "kilometres_in_service": km,
        # The conventions and parameters the write-up's steps state, so every number it writes is one computed here.
        "conventions": {"brake_window_ms": 2000, "bin_m": 10, "share_set_aside_pct": 10,
                        "lines_in_metres_from_july": [40, 41, 44, 46], "week_starts_october": [d.day for d in E.WEEKS],
                        "chart_line_rate_pct": pct(E.RATIO * c["fleet"])},
    }
    return fig, c


def write_figures(fig):
    with open(os.path.join(HERE, "figures.json"), "w") as f:
        json.dump(fig, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")


def write_xlsx(fig):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    wb = Workbook()
    ws = wb.active
    ws.title = "Depots 2026"
    ws.append(["EMAL Safety and Training: collision-warning response by depot, January to October 2026"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Counted warnings are the forward-collision and pedestrian warnings with something in the bus's path; "
               "the warnings raised at the four fixed structures listed on the second sheet are set aside."])
    ws.append([])
    head = (["Depot", "Counted warnings", "Not braked on", "Rate (%)", "Ratio to fleet", "At-fault collisions",
             "Claims paid (EUR)"] + ["Km in service, %s" % m for m in MONTHS] +
            ["Hours on service, %s" % w for w in WEEKS])
    ws.append(head)
    for cell in ws[4]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    taken = set(fig["call"]["depots"])
    for d in E.DEPOT_ORDER:
        v = fig["depots"][d]
        row = [d, v["warnings"], v["not_braked"], v["rate_pct"], v["ratio"], fig["at_fault_collisions"][d],
               fig["claims_paid_eur"][d]] + fig["kilometres_in_service"][d] + fig["hours_on_service"][d]
        ws.append(row)
        if d in taken:
            for cell in ws[ws.max_row]:
                cell.fill = PatternFill("solid", fgColor="FCE4D6")
    ws.append(["Fleet", fig["fleet_warnings"], fig["fleet_not_braked"], fig["fleet_rate_pct"], 1.0])
    for cell in ws[ws.max_row]:
        cell.font = Font(bold=True)
    ws.append([])
    ws.append(["The programme's line is 1.3 times the fleet's rate. Hours on service exclude lines 000 and ESC; a "
               "session counts in the week it starts."])
    widths = [16, 11, 10, 9, 10, 11, 12] + [12] * 4 + [13] * 4
    for i, wdt in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = wdt
    ws2 = wb.create_sheet("Places set aside")
    ws2.append(["Place", "Warnings, Jan to Oct 2026", "Bus passes", "Share of passes (%)"])
    for cell in ws2[1]:
        cell.font = Font(bold=True)
    for p in fig["false_places"]:
        ws2.append([p["name"], p["warnings"], p["passes"], p["share_pct"]])
    pz = fig["plaza"]
    ws2.append([])
    ws2.append(["Kept: Plaza de Abastos shared space (lines 1, 3, 7, 9)", pz["warnings"], pz["passes"], pz["share_pct"]])
    ws2.column_dimensions["A"].width = 58
    for col in "BCD":
        ws2.column_dimensions[col].width = 16
    path = os.path.join(GOLDEN, XLSX)
    wb.save(path)
    normalise_zip(path)


def write_svg(fig):
    import matplotlib
    matplotlib.use("Agg")
    matplotlib.rcParams["svg.hashsalt"] = "task191"
    import matplotlib.pyplot as plt
    deps = sorted(E.DEPOT_ORDER, key=lambda d: -fig["depots"][d]["rate_pct"])
    vals = [fig["depots"][d]["rate_pct"] for d in deps]
    line = 1.3 * fig["fleet_rate_pct"]
    fig_, ax = plt.subplots(figsize=(8.2, 4.6), dpi=100)
    colours = ["#c0392b" if d in fig["call"]["depots"] else "#7f8c8d" for d in deps]
    ax.bar(deps, vals, color=colours, width=0.62)
    ax.axhline(line, color="#2c3e50", linestyle="--", linewidth=1.2)
    ax.text(len(deps) - 0.6, line + 0.6, "1.3 x fleet rate = %.1f%%" % line, ha="right", va="bottom", fontsize=9,
            color="#2c3e50")
    for i, v in enumerate(vals):
        ax.text(i, v + 0.4, "%.1f" % v, ha="center", va="bottom", fontsize=9)
    ax.set_ylabel("Counted warnings not braked on (%)")
    ax.set_title("Driver-Attention Programme 2027 runs at %s" % " and ".join(fig["call"]["depots"]), fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.xticks(fontsize=9)
    ax.set_ylim(0, max(vals) * 1.18)
    fig_.text(0.01, 0.01, "January to October 2026; warnings at the four fixed structures set aside. Fleet rate %.1f%%."
              % fig["fleet_rate_pct"], fontsize=8, color="#555555")
    fig_.tight_layout(rect=(0, 0.04, 1, 1))
    path = os.path.join(GOLDEN, SVG)
    fig_.savefig(path, format="svg", metadata={"Date": None, "Creator": None})
    plt.close(fig_)
    set_mtime(path)


def write_docx(fig):
    from docx import Document
    from docx.shared import Pt
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    taken = fig["call"]["depots"]
    doc.add_paragraph("EMAL Safety and Training. Paper for the Management Committee, 24 November 2026")
    doc.add_heading("Driver-Attention Programme 2027: the depots", level=1)
    doc.add_paragraph(
        "Recommendation: run the 2027 programme at %s, and at no other depot. Its drivers did not brake on %.1f per "
        "cent of their counted collision warnings between January and October, %.2f times the fleet's rate of %.1f "
        "per cent; the terms take a depot at 1.3 times." % (" and ".join(taken), fig["depots"][taken[0]]["rate_pct"],
                                                           fig["depots"][taken[0]]["ratio"], fig["fleet_rate_pct"]))
    cl = fig["call"]["closest"]
    doc.add_paragraph(
        "The depot closest to the line without reaching it is %s, at %.2f times the fleet's rate (%.1f per cent), "
        "%.2f short of 1.3." % (cl, fig["call"]["closest_ratio"], fig["depots"][cl]["rate_pct"], fig["gap_to_line"]))
    doc.add_heading("Which warnings count", level=2)
    doc.add_paragraph(
        "The terms count genuine warnings only, those raised with a vehicle, cyclist or pedestrian in the bus's path. "
        "Since the Red 2026 network went in, four fixed structures raise a warning on a large share of the buses that "
        "pass them with nothing in the way: %s. Together they raised %s of the period's warnings, and drivers rightly "
        "let almost all of them go. We set those warnings aside; every other warning stays in."
        % ("; ".join("%s (%s warnings, on %.1f per cent of passes)" % (p["name"], eur(p["warnings"]), p["share_pct"])
                     for p in fig["false_places"]), eur(fig["false_place_warnings"])))
    pz = fig["plaza"]
    doc.add_paragraph(
        "The Plaza de Abastos shared space is different. Its warnings are pedestrians stepping into the path of lines "
        "1, 3, 7 and 9 on market days: %s of them, on %.1f per cent of passes, and %.1f per cent not braked on. They "
        "are genuine, and they are where %s's rate comes from." % (eur(pz["warnings"]), pz["share_pct"],
                                                                pz["not_braked_pct"], taken[0]))
    doc.add_heading("Depots, January to October 2026", level=2)
    t = doc.add_table(rows=1, cols=5)
    t.style = "Table Grid"
    for i, h in enumerate(["Depot", "Counted warnings", "Not braked on", "Rate (%)", "Ratio to fleet"]):
        t.rows[0].cells[i].text = h
    for d in E.DEPOT_ORDER:
        v = fig["depots"][d]
        cells = t.add_row().cells
        cells[0].text = d
        cells[1].text = eur(v["warnings"])
        cells[2].text = eur(v["not_braked"])
        cells[3].text = "%.1f" % v["rate_pct"]
        cells[4].text = "%.2f" % v["ratio"]
    cells = t.add_row().cells
    cells[0].text = "Fleet"
    cells[1].text = eur(fig["fleet_warnings"])
    cells[2].text = eur(fig["fleet_not_braked"])
    cells[3].text = "%.1f" % fig["fleet_rate_pct"]
    cells[4].text = "1.00"
    doc.add_paragraph(
        "The workbook warning_response_by_depot_2026.xlsx carries the same table with each depot's at-fault "
        "collisions and claims paid, its kilometres in service from July to October and its drivers' hours on service "
        "for the four October weeks, and lists the places set aside.")
    doc.add_paragraph("Miriam Vilanova, Head of Driving Safety")
    cp = doc.core_properties
    cp.author = "EMAL Safety and Training"
    cp.title = "Driver-Attention Programme 2027: the depots"
    cp.comments = ""
    cp.last_modified_by = "EMAL Safety and Training"
    cp.revision = 1
    path = os.path.join(GOLDEN, DOCX)
    doc.save(path)
    normalise_zip(path, app="Microsoft Office Word")


def write_submission(fig):
    taken = fig["call"]["depots"]
    d0 = taken[0]
    cl = fig["call"]["closest"]
    dp = fig["default_path"]
    lines = []
    lines.append("## Tags\n")
    lines.append("> **Domain:** Human factors and ergonomics, safety incident and error analysis.")
    lines.append("> **Analytical objective:** Anomaly detection and diagnostics.\n")
    lines.append("## 1. Final Recommendation\n")
    lines.append("**Run the 2027 Driver-Attention Programme at %s, and at no other depot.**" % d0)
    lines.append(
        "%s's drivers did not brake on %.1f per cent of their genuine collision warnings in January to October 2026, "
        "%.2f times the fleet's %.1f per cent. Not %s: their high no-brake shares come from four fixed structures that "
        "raise a warning on a large share of passes with nothing in the path. %s comes closest at %.2f."
        % (d0, fig["depots"][d0]["rate_pct"], fig["depots"][d0]["ratio"], fig["fleet_rate_pct"],
           " or ".join(dp["depots"]), cl, fig["call"]["closest_ratio"]))
    lines.append("")
    lines.append("## 2. Critical Components\n")
    lines.append("1. The terms count genuine warnings only (something in the bus's path), one camera event each, by the "
                 "depot the bus was allocated to that day, in Lorvega local time.")
    lines.append("2. Read on every collision warning, the fleet's rate is %.1f per cent and %s reach 1.3 times it; %s "
                 "sits at %.2f." % (dp["fleet_rate_pct"], " and ".join(dp["depots"]), d0, dp["ratios"][d0]))
    lines.append("3. Four places fire on a large share of bus passes, from %.1f to %.1f per cent; every other place, the "
                 "Plaza de Abastos included at %.1f per cent, fires on under 3 per cent. Their %s warnings are not "
                 "genuine and are set aside." % (min(p["share_pct"] for p in fig["false_places"]),
                                                 max(p["share_pct"] for p in fig["false_places"]),
                                                 fig["plaza"]["share_pct"], eur(fig["false_place_warnings"])))
    lines.append("4. The Plaza de Abastos warnings are genuine: drivers there let %.1f per cent pass, so dropping the "
                 "busiest or most ignored places wrongly removes them too." % fig["plaza"]["not_braked_pct"])
    lines.append("")
    lines.append("## 3. Step-by-Step Solution\n")
    lines.append("1. From adas_collision_warnings_2025-10_2026-10.csv kept FCW, PCW, FWD_COLL and PED_COLL, one row per "
                 "event_id, local dates 1 January to 31 October 2026; not braked on is brake_2s N (firmware 1.x) or "
                 "brake_reaction_ms blank or over 2,000 (2.x).")
    lines.append("2. Gave each warning the depot of its bus that day from fleet_register_2026.xlsx Allocations.")
    lines.append("3. Snapped each warning to the nearest stop-to-stop segment of red_paradas_recorridos_2025_2026.xlsx "
                 "(Red 2026, valid dates) and counted bus passes per segment from service_return_2025-10_2026-10.csv "
                 "trips operated on every line and direction using it.")
    lines.append("4. Grouped warnings in 10 m bins along each segment and set aside the clusters firing on 10 per cent "
                 "or more of the segment's passes.")
    lines.append("5. Took each depot's rate and its ratio to the pooled fleet rate; a depot at 1.3 or more goes in.")
    lines.append("6. Hours on service from etm_logons_2026-10.csv: removed repeated rows and lines 000 and ESC, ended a "
                 "session at the same driver's next log-on, added the hour when clocks went back on 25 October, depot "
                 "from hr_depot_assignments_2026.csv on the start date, week of the start.")
    lines.append("7. At-fault collisions from incident_register_2026.xlsx with the driver's and the inspector's report "
                 "of one incident (same bus, minutes apart) counted once, codes A and C; claims paid from the October "
                 "bordereau, plates to buses through the registration history, a reopened claim's chain counted once "
                 "at its latest claim.")
    lines.append("8. Kilometres in service from the return by operating depot (line 25 at Las Tenerías), lines 40 to 46 "
                 "from July in metres, plus trips operated times each authorised diversion's change for its dates.")
    lines.append("")
    lines.append("## 4. Deliverable Answers\n")
    lines.append("### %s\n" % DOCX)
    lines.append("1. Depots the programme takes: %s." % d0)
    lines.append("2. Fleet's rate of counted warnings not braked on: %.1f per cent." % fig["fleet_rate_pct"])
    lines.append("3. Depot coming closest without qualifying: %s, ratio %.2f." % (cl, fig["call"]["closest_ratio"]))
    lines.append("")
    lines.append("### %s\n" % XLSX)
    lines.append("1. Counted warnings, not braked on, rate (per cent, one decimal) and ratio (two decimals):")
    for d in E.DEPOT_ORDER:
        v = fig["depots"][d]
        lines.append("   - %s: %s, %s, %.1f, %.2f" % (d, eur(v["warnings"]), eur(v["not_braked"]), v["rate_pct"], v["ratio"]))
    lines.append("2. At-fault collisions, January to October, and claims paid on them (euros):")
    for d in E.DEPOT_ORDER:
        lines.append("   - %s: %d, %s" % (d, fig["at_fault_collisions"][d], eur(fig["claims_paid_eur"][d])))
    lines.append("3. Kilometres in service, July, August, September and October (whole kilometres):")
    for d in E.DEPOT_ORDER:
        lines.append("   - %s: %s" % (d, ", ".join(eur(x) for x in fig["kilometres_in_service"][d])))
    lines.append("4. Drivers' hours on service, weeks from Monday 5, 12, 19 and 26 October (whole hours):")
    for d in E.DEPOT_ORDER:
        lines.append("   - %s: %s" % (d, ", ".join(eur(x) for x in fig["hours_on_service"][d])))
    lines.append("")
    lines.append("### %s\n" % SVG)
    lines.append("1. One bar per depot for the rate of counted warnings not braked on, with a dashed line at 1.3 times "
                 "the fleet's rate (%.1f per cent)." % (1.3 * fig["fleet_rate_pct"]))
    lines.append("2. %s marked in red; the title names it." % d0)
    with open(os.path.join(TASK, "submission.md"), "w") as f:
        f.write("\n".join(lines) + "\n")


def main():
    os.makedirs(GOLDEN, exist_ok=True)
    fig, c = compute()
    write_figures(fig)
    write_xlsx(fig)
    write_svg(fig)
    write_docx(fig)
    write_submission(fig)
    print("call: %s, closest %s %.2f, fleet %.1f" % (fig["call"]["depots"], fig["call"]["closest"],
                                                    fig["call"]["closest_ratio"], fig["fleet_rate_pct"]))


if __name__ == "__main__":
    main()
