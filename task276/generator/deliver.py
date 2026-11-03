"""The answers, the two golden deliverables, figures.json, submission.md and metadata.json, all from solve's S."""
import json
import os

import params as P
import postprocess

XLSX = "crossing_delay_2025_26.xlsx"
DOCX = "crossing_choice_2027.docx"


def k(v):
    return int(round(v / 1000.0)) * 1000


def f1(v):
    return "%.1f" % (round(v + 1e-12, 1))


def answers(S):
    names = S["names"]
    order = sorted(names, key=lambda n: -S["delay"][n])
    A = dict(order=order, call=S["call"], runner=S["runner"])
    A["delay"] = {n: k(S["delay"][n]) for n in names}
    A["gap"] = k(S["gap"])
    A["free"] = {n: k(S["free"][n]) for n in names}
    A["closures"] = {n: f1(S["per"][n]["closures"]) for n in names}
    A["fault"] = {n: f1(S["fault"]["golden"][n]) for n in names}
    A["hgv"] = {n: f1(S["hgv"]["golden"][n]) for n in names}
    reg = S["reg"]
    A["ref"] = {n: "%s %dm %02dch" % (reg[n]["elr"], reg[n]["miles"], reg[n]["chains"]) for n in names}
    A["county"] = {n: reg[n]["county"] for n in names}
    g = S["layout"][S["call"]]["gate"]
    A["storage_m"] = int(g["storage_m"])
    A["storage_veh"] = int(g["storage_m"] // S["M"]["vlen"])
    A["sat"] = S["M"]["sat"]
    A["vlen"] = S["M"]["vlen"]
    A["cycle"] = int(g["site"]["cycle"])
    A["wb_green"] = int(g["site"]["g1"])
    A["eb_green"] = int(g["site"]["g2"])
    A["site"] = g["site"]["site"]
    return A


def write_xlsx(path, A):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = Workbook()
    ws = wb.active
    ws.title = "Crossing delay"
    ws["A1"] = "Mill Lane's barrier closures cost road users the most school-morning delay in 2025/26"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Delay is the extra time vehicles counted on each crossing's approaches 07:00 to 10:00 on its county's "
                "school days took to reach the far count site because the barriers were lowered (programme paper "
                "LCRP/26/07, 3.2).")
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:H2")
    ws.row_dimensions[2].height = 30
    head = ["Rank", "Crossing", "Railway reference", "County", "Delay (vehicle-hours)",
            "Closures begun 07:00-10:00 per school morning", "Barrier down in fault-held closures, 1 Sep 2025 to 31 Aug "
            "2026 (hours)", "Heavy goods vehicles, school-day mornings (% of vehicles counted)"]
    ws.append([])
    ws.append(head)
    thin = Side(style="thin", color="999999")
    for c in ws[4]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.fill = PatternFill("solid", fgColor="DDE4EC")
        c.border = Border(bottom=thin)
    ws.row_dimensions[4].height = 58
    for i, n in enumerate(A["order"], 1):
        ws.append([i, n, A["ref"][n], A["county"][n], A["delay"][n], float(A["closures"][n]), float(A["fault"][n]),
                   float(A["hgv"][n])])
        r = ws.max_row
        ws.cell(r, 5).number_format = "#,##0"
        for col in (6, 7, 8):
            ws.cell(r, col).number_format = "0.0"
        if n == A["call"]:
            for col in range(1, 9):
                ws.cell(r, col).font = Font(bold=True)
    ws.append([])
    ws.append(["", "Recommended for 2027: %s. Runner-up: %s, %s vehicle-hours behind." % (
        A["call"], A["runner"], "{:,}".format(A["gap"]))])
    ws.cell(ws.max_row, 2).font = Font(bold=True)
    ws.append(["", "Delay rounded to the nearest thousand vehicle-hours; closures, fault hours and shares to one decimal."])
    for col, w in zip("ABCDEFGH", (6, 15, 16, 12, 13, 16, 22, 20)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "C5"
    ws.print_title_rows = "4:4"
    ns = wb.create_sheet("Notes")
    notes = [
        ("Prepared", "Network Planning, %s. Record as exported on 14 September 2026." % P.LEAD),
        ("Delay", "Extra time vehicles counted on a crossing's approaches between 07:00 and 10:00 took to reach the "
                  "count site on the far side because the barriers were lowered, against the same morning with the "
                  "barriers left raised (LCRP/26/07, 3.2). A vehicle held past 10:00 counts in full."),
        ("School days", "Weekdays inside the crossing's county's published term dates, outside half terms and bank "
                        "holidays (LCRP/26/07, 3.3)."),
        ("Constants", "Saturation flow, queued vehicle length and count spreading from the appraisal conventions "
                      "(version 3, March 2024); signal greens and saturation flows from the signal timing register."),
        ("Mill Lane", "Replayed through the river bridge's shuttle signals (SS 2207) and the 42 m between their stop "
                      "line and the barriers; every other shortlisted crossing has no control between its count sites."),
        ("Fault-held", "Barrier closures during which a barriers-failed-to-raise, obstacle detection or power fault was "
                       "reported, or that ended at a signaller's reset; 1 September 2025 to 31 August 2026."),
        ("Heavy goods", "QT-40 counters write the heavy column as a whole-number percentage of the quarter hour's "
                        "vehicles; converted before summing, including the rows each site logged before its present "
                        "counter was installed."),
    ]
    for a, b in notes:
        ns.append([a, b])
        ns.cell(ns.max_row, 1).font = Font(bold=True)
        ns.cell(ns.max_row, 2).alignment = Alignment(wrap_text=True, vertical="top")
        ns.cell(ns.max_row, 1).alignment = Alignment(vertical="top")
    ns.column_dimensions["A"].width = 13
    ns.column_dimensions["B"].width = 100
    wb.properties.creator = P.LEAD
    wb.save(path)
    postprocess.scrub(path, P.BOARD, "2026-10-28")
    postprocess.finish_office(path, "2026-10-21T09:12:00Z", "2026-10-28T16:05:00Z", P.BOARD)


def write_docx(path, A):
    import docx
    from docx.shared import Pt
    import build as B
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10.5)
    B.house_style(d)
    d.add_heading("Mill Lane for the 2027 level crossing scheme", level=1)
    d.add_paragraph("To: Selection panel, meeting of 12 November 2026\nFrom: %s, Network Planning Lead\nDate: 29 October "
                    "2026\nReference: LCRP/26/11" % P.LEAD)
    sec = d.sections[0]
    sec.footer.paragraphs[0].text = "Shires Transport Board, Level Crossing Replacement Programme, LCRP/26/11"
    d.add_heading("Recommendation", level=2)
    p = d.add_paragraph()
    p.add_run("Replace Mill Lane in 2027.").bold = True
    p.add_run(" Its barrier closures cost road users %s vehicle-hours on school-day mornings between 07:00 and 10:00 in "
              "the 2025/26 school year, the most on the shortlist. The runner-up is %s at %s vehicle-hours, %s "
              "vehicle-hours behind." % ("{:,}".format(A["delay"][A["call"]]), A["runner"],
                                         "{:,}".format(A["delay"][A["runner"]]), "{:,}".format(A["gap"])))
    d.add_heading("Why Mill Lane and not Station Road", level=2)
    d.add_paragraph(
        "Station Road has the longest closures on the shortlist, and if every held queue moved off at the road's own "
        "%s vehicles an hour once the barriers rose it would come out top, at about %s vehicle-hours against Mill "
        "Lane's %s. Mill Lane's queues cannot do that. The single-track river bridge on Mill Lane, %d metres west of "
        "the crossing, is worked by fixed-time shuttle signals (site %s, a %d-second cycle with %d seconds of green "
        "westbound and %d eastbound), and the gap between its stop line and the barriers holds %d vehicles. A "
        "westbound queue can only leave in the westbound green, and an eastbound queue cannot cross the bridge while "
        "the space before the barriers is full. Each closure's queue therefore drains at the bridge's pace, and Mill "
        "Lane's closures cost about twice what a release at the road's own rate would suggest."
        % ("{:,}".format(A["sat"]), "{:,}".format(A["free"]["Station Road"]), "{:,}".format(A["free"]["Mill Lane"]),
           A["storage_m"], A["site"], A["cycle"], A["wb_green"], A["eb_green"], A["storage_veh"]))
    d.add_paragraph(
        "The other crossings have no control between their count sites, so their delay is the barrier closures alone. "
        "The March 2026 queue survey's queues at barrier rise agree with the counts at every crossing, Mill Lane "
        "included; the survey shows how big each queue is, not how fast it clears.")
    d.add_heading("Shortlist", level=2)
    t = d.add_table(rows=1, cols=5)
    t.style = "Table Grid"
    for i, h in enumerate(["Crossing", "Delay (vehicle-hours)", "Closures per school morning", "Fault-held closure hours",
                           "Heavy goods vehicles (%)"]):
        t.rows[0].cells[i].text = h
    for n in A["order"]:
        r = t.add_row().cells
        r[0].text = n
        r[1].text = "{:,}".format(A["delay"][n])
        r[2].text = A["closures"][n]
        r[3].text = A["fault"][n]
        r[4].text = A["hgv"][n]
    d.add_paragraph("Source: barrier events from the rail infrastructure manager; approach counts, network and signal "
                    "timing register from the highway authority; term dates from the four county councils.")
    d.add_paragraph("Delay is rounded to the nearest thousand vehicle-hours and counts every vehicle counted between "
                    "07:00 and 10:00 in full, including time held after 10:00. Closures are those begun between 07:00 "
                    "and 10:00. Fault-held hours cover 1 September 2025 to 31 August 2026. Workings are in %s." % XLSX)
    d.core_properties.author = P.LEAD
    d.core_properties.title = "Mill Lane for the 2027 level crossing scheme"
    d.core_properties.revision = 3
    d.save(path)
    B.lean_docx(path)
    postprocess.scrub(path, P.BOARD, "2026-10-29")
    postprocess.finish_office(path, "2026-10-23T14:02:00Z", "2026-10-29T10:37:00Z", P.BOARD)


def write_goldens(folder, A):
    os.makedirs(folder, exist_ok=True)
    write_xlsx(os.path.join(folder, XLSX), A)
    write_docx(os.path.join(folder, DOCX), A)


def figures(A):
    F = {"call": A["call"], "runner_up": A["runner"], "gap": A["gap"], "saturation_flow": A["sat"],
         "storage_vehicles": A["storage_veh"], "storage_m": A["storage_m"], "bridge_cycle_s": A["cycle"],
         "bridge_wb_green_s": A["wb_green"], "bridge_eb_green_s": A["eb_green"], "vehicle_length_m": A["vlen"],
         "free_station_road": A["free"]["Station Road"], "free_mill_lane": A["free"]["Mill Lane"],
         "bridge_site_number": int(A["site"].split()[1]), "brief_delay_section": "3.2", "brief_days_section": "3.3"}
    for n in A["order"]:
        key = n.lower().replace(" ", "_")
        F["delay_" + key] = A["delay"][n]
        F["closures_" + key] = A["closures"][n]
        F["fault_hours_" + key] = A["fault"][n]
        F["hgv_share_" + key] = A["hgv"][n]
    return F


def submission(A):
    c, r = A["call"], A["runner"]
    fmt = lambda v: "{:,}".format(v)
    lines = ["# task276 submission", "", "## Tags", "",
             "**Domain:** Urban & Regional Science (network analysis: the road-user delay each shortlisted level "
             "crossing's barrier closures impose on the roads through it).",
             "**Analytical objective:** Descriptive & Distribution Analysis (how school-day morning closure delay is "
             "distributed across the programme's shortlisted crossings, choosing the 2027 replacement, with each "
             "crossing's closure frequency, fault-held closure hours and heavy goods vehicle share).", "",
             "## 1. Final Recommendation", "",
             "**Replace Mill Lane in 2027.**", "",
             "Its closures cost road users **%s vehicle-hours** on school-day mornings 07:00 to 10:00 in 2025/26, "
             "against Station Road's **%s**, a gap of **%s**. Not Station Road, which leads only when every held queue "
             "leaves at the road's own saturation flow once the barriers rise (%s against Mill Lane's %s); Mill Lane's "
             "queues can only leave in the greens of the river bridge's shuttle signals %d metres beyond the crossing."
             % (fmt(A["delay"][c]), fmt(A["delay"][r]), fmt(A["gap"]), fmt(A["free"]["Station Road"]),
                fmt(A["free"]["Mill Lane"]), A["storage_m"]), "",
             "## 2. Critical Components", "",
             "1. Mill Lane's section between its count sites holds the shuttle-signalled single-track bridge: a "
             "**%d**-second cycle, **%d** seconds of westbound and **%d** of eastbound green, **%d** vehicles of storage "
             "between the bridge stop line and the barriers." % (A["cycle"], A["wb_green"], A["eb_green"], A["storage_veh"]),
             "2. Delay by crossing: " + "; ".join("%s **%s**" % (n, fmt(A["delay"][n])) for n in A["order"]) + ".",
             "3. No other shortlisted crossing has a control between its count sites.", "",
             "## 3. Step-by-Step Solution", "",
             "1. Paired each LOWERED event in barrier_events_2025_26.csv with the next RAISED event per crossing, "
             "dropping repeats of the same event within three seconds, and converted UTC to UK local time.",
             "2. Took each crossing's school days from term_dates_2025_26.xlsx for its county in "
             "crossing_register_2025.pdf, weekdays in term outside half terms and bank holidays (crossing_programme_2027.docx 3.3).",
             "3. Spread each quarter hour's vehicles in approach_counts_2025_26.csv evenly across it at the count sites "
             "network_register_2026.xlsx gives each crossing (road_delay_appraisal_conventions.pdf 3).",
             "4. Matched each crossing to its node in network_nodes.csv by grid reference and walked network_links.csv "
             "between its two count sites: only Mill Lane's section holds a signal site, %s, whose single-track "
             "link is the bridge, %d metres from the crossing." % (A["site"], A["storage_m"]),
             "5. Replayed every school morning from 06:00, each vehicle passing the barriers when raised at %s vehicles "
             "an hour per lane and, at Mill Lane, the bridge stop line only in its direction's green at the register's "
             "%s, with %d vehicles of storage between the two stop lines; delay is each vehicle's exit time against the "
             "same morning with no closures (crossing_programme_2027.docx 3.2), summed over vehicles counted 07:00 to 10:00."
             % (fmt(A["sat"]), fmt(A["sat"]), A["storage_veh"]),
             "6. Fault-held hours: the barrier closures during which a BFR, ODF or PWR fault in lx_work_orders_2025_26.csv "
             "was reported (the renewed Long Drove machine, LXB/5203, matched by the closure held down at that "
             "minute) or which ended at a signaller's reset in signaller_occurrences_2025_26.xlsx, summed over the year.",
             "7. Heavy goods share: the veh_hgv column over veh_total for the quarter hours between 07:00 and 10:00 on school days, both "
             "approaches; at the QT-40 sites, and at an RX-5 site's rows before its counter's install date, the column "
             "is a whole-number percentage of the interval's vehicles, converted at veh_hgv times veh_total over 100.",
             "8. Mill Lane leads at %s vehicle-hours against Station Road's %s: replace Mill Lane in 2027."
             % (fmt(A["delay"][c]), fmt(A["delay"][r])), "",
             "## 4. Deliverable Answers", "", "### %s" % XLSX, "",
             "1. Each shortlisted crossing, ranked by delay: delay to the nearest thousand vehicle-hours, closures begun "
             "between 07:00 and 10:00 per school morning, hours barriers were down 1 September 2025 to 31 August 2026 in "
             "closures a fault held down, heavy goods vehicles as a share of vehicles counted on school-day mornings:"]
    for n in A["order"]:
        lines.append("   - %s: %s vehicle-hours, %s closures per school morning, %s fault-held hours, %s%% heavy goods "
                     "vehicles" % (n, fmt(A["delay"][n]), A["closures"][n], A["fault"][n], A["hgv"][n]))
    lines += ["", "### %s" % DOCX, "",
              "1. Recommendation: replace Mill Lane in 2027.",
              "2. Runner-up: Station Road.",
              "3. Gap between them: %s vehicle-hours." % fmt(A["gap"]), ""]
    return "\n".join(lines)


def write(task_dir, here, A):
    F = figures(A)
    with open(os.path.join(here, "figures.json"), "w") as fh:
        json.dump(F, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    with open(os.path.join(task_dir, "submission.md"), "w") as fh:
        fh.write(submission(A))
    return F
