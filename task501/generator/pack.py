"""Write the evidence pack: every file under its export name, in its own format and layout."""
import csv
import io
import os

import docs as DOC
import net as N
import post as PP
import records as RC
import world as W

FILES = dict(
    flows="dma_inlet_flows_2025-11_2026-10.csv",
    outlet="copt_hill_outlet_flow_2025-11_2026-10.csv",
    register="trunk_mains_register_2026-11.xlsx",
    valvelog="control_room_valve_log_2025-11_2026-10.csv",
    turbidity="dma_inlet_turbidity_2025-11_2026-10.csv",
    standard="nos12_planned_supply_route_changes_issue3.pdf",
    plan="tm107_ferrars_lane_relining_outage_plan_v1.pdf",
    jobs="mains_flushing_job_sheets_2025-26.csv",
    supply="nonhousehold_supply_points_2026-11.xlsx",
    consumption="nonhousehold_monthly_consumption_2025-04_2026-10.csv",
    amr="amr_large_users_hourly_2025-11_2026-10.csv",
    condition="trunk_mains_condition_assessment_2024.pdf",
    weather="stavenham_weather_daily_2025-11_2026-10.csv",
    samples="regulatory_tap_samples_2025-11_2026-10.csv",
)
DISTRACTORS = ["condition", "weather", "samples"]

HEADERS = dict(
    flows=["dma", "meter_serial", "reading_utc", "flow_l_s", "quality"],
    outlet=["reading_utc", "outlet_flow_l_s"],
    valvelog=["log_ref", "date", "time", "valve_no", "action", "turns", "job_ref", "logged_by", "remarks"],
    turbidity=["monitor_id", "dma", "reading_utc", "turbidity_ntu", "status"],
    jobs=["sheet_no", "night_of", "crew", "dma", "street", "section_ref", "main_dn_mm", "material", "section_length_m",
          "hydrant_no", "start", "finish", "gauge_flow_l_s", "volume_m3", "final_ntu", "remarks"],
    consumption=["spid", "month", "consumption_m3", "basis"],
    amr=["logger_id", "read_start_local", "volume_m3"],
    weather=["date", "max_temperature_c", "min_temperature_c", "rainfall_mm", "sunshine_h"],
    samples=["sample_ref", "sampled_on", "supply_zone", "postcode_sector", "iron_ug_l", "manganese_ug_l",
             "turbidity_ntu", "colour_mg_l_pt"],
)


def write_csv(path, header, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(header)
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    return len(rows)


def _sheet(ws, title, stamp, header, rows, widths):
    from openpyxl.styles import Font, PatternFill
    ws.append([title])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append([stamp])
    ws["A2"].font = Font(italic=True, size=9, color="555555")
    ws.append(header)
    for c in ws[3]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE5EC")
    for r in rows:
        ws.append([None if (isinstance(c, str) and c == "") else c for c in r])
    for i, wdt in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = wdt
    ws.freeze_panes = "A4"


def write_register(path, vlist):
    import openpyxl
    meters, swaps = RC.meter_serials()
    current = dict(meters)
    for d, (_, _, new) in swaps.items():
        current[d] = new
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Mains"
    rows = []
    for k, (mid, name, a, b, dn, mat, lining, year, length) in W.MAINS.items():
        status = "In service" if k in W.TRUNK else "Normally shut"
        note = {"T03": "Relining programme phase 2, 2027", "T04": "Relining programme phase 3"}.get(k, "")
        rows.append([mid, name, W.NODES[a], W.NODES[b], dn, mat, lining, year, length, status, note])
    _sheet(ws, "Stavenham trunk mains register: mains", "Extract 2 November 2026, Asset Information",
           ["Main", "Name", "From", "To", "DN (mm)", "Material", "Lining", "Laid", "Length (m)", "Status", "Note"],
           rows, [8, 34, 24, 24, 9, 13, 20, 7, 11, 14, 32])
    ws = wb.create_sheet("Valves")
    rows = [[v["valve_no"], v["main_id"], v["location"], v["role"], v["vtype"], v["dn"], v["normal"], v["turns"]]
            for v in sorted(vlist, key=lambda v: v["valve_no"])]
    _sheet(ws, "Stavenham trunk mains register: valves", "Extract 2 November 2026, Asset Information",
           ["Valve", "Main", "Location", "Position on main", "Type", "DN (mm)", "Normal position", "Turns to close"],
           rows, [10, 8, 24, 18, 11, 9, 16, 14])
    ws = wb.create_sheet("Districts")
    rng = RC.R(51)
    rows = []
    for d, (code, name, node) in W.DISTRICTS.items():
        props = int(round(W.RES[d] * 86400 / (138 * 2.3) + rng.integers(-60, 61)))
        rows.append([code, name, W.NODES[node], current[d], props, round(float(rng.uniform(14, 41)), 1)])
    _sheet(ws, "Stavenham district metered areas", "Extract 2 November 2026, Asset Information",
           ["DMA", "Name", "Inlet junction", "Inlet meter", "Properties", "Mains (km)"], rows, [9, 16, 24, 12, 11, 11])
    wb.save(path)
    PP.normalize_ooxml(path, "Asset Information", "Asset Information", "2019-04-03T08:12:00Z", "2026-11-02T08:41:00Z",
                       excel=True)


def write_supply(path, sp):
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Supply points"
    rows = [[s["spid"], s["name"], s["premises"], s["postcode"], s["dma"], s["meter"], s["cycle"], s["logger"],
             s["start"], s["end"]] for s in sp]
    _sheet(ws, "Non-household supply points, Stavenham", "Report run 02/11/2026 07:55, Business Customers",
           ["SPID", "Customer", "Premises", "Postcode", "DMA", "Meter serial", "Read cycle", "AMR logger",
            "Supply start", "Supply end"], rows, [15, 34, 38, 10, 8, 12, 15, 11, 12, 12])
    wb.save(path)
    PP.normalize_ooxml(path, "Business Customers", "Business Customers", "2026-11-02T07:55:00Z", "2026-11-02T07:55:00Z",
                       excel=True)


def consumption_rows(sp):
    out = []
    for s in sorted(sp, key=lambda s: s["spid"]):
        for m in sorted(s["mon_m3"]):
            out.append((s["spid"], m, str(s["mon_m3"][m]), s["basis"][m]))
    return out


def write_pack(out, tr=None):
    tr = tr or RC.truth()
    os.makedirs(out, exist_ok=True)
    p = lambda k: os.path.join(out, FILES[k])
    n = {}
    rows, minfo = RC.district_meter_rows(tr)
    n["flows"] = write_csv(p("flows"), HEADERS["flows"], rows)
    orow, _ = RC.outlet_rows(tr)
    n["outlet"] = write_csv(p("outlet"), HEADERS["outlet"], orow)
    vlist = RC.valves()
    n["valvelog"] = write_csv(p("valvelog"), HEADERS["valvelog"], RC.valve_log_rows(vlist))
    n["turbidity"] = write_csv(p("turbidity"), HEADERS["turbidity"], RC.turbidity_rows(tr))
    jrows, jtruth = RC.job_sheet_rows()
    n["jobs"] = write_csv(p("jobs"), HEADERS["jobs"], jrows)
    sp, amr = RC.customers(tr)
    n["consumption"] = write_csv(p("consumption"), HEADERS["consumption"], consumption_rows(sp))
    n["amr"] = write_csv(p("amr"), HEADERS["amr"], RC.amr_rows(amr))
    n["weather"] = write_csv(p("weather"), HEADERS["weather"], RC.weather_rows())
    n["samples"] = write_csv(p("samples"), HEADERS["samples"], RC.sample_rows(tr))
    write_register(p("register"), vlist)
    n["register"] = len(W.MAINS) + len(vlist) + len(W.DISTRICTS)
    write_supply(p("supply"), sp)
    n["supply"] = len(sp)
    DOC.standard(p("standard"))
    DOC.plan(p("plan"), vlist)
    crow = RC.condition_table()
    DOC.condition(p("condition"), crow)
    n["standard"] = n["plan"] = n["condition"] = 0
    PP.normalize_pdf(p("standard"), b"D:20250312101144+00'00'", b"D:20250318154702+00'00'")
    PP.normalize_pdf(p("plan"), b"D:20261113162018+00'00'", b"D:20261116091233+00'00'")
    PP.normalize_pdf(p("condition"), b"D:20240919113520+01'00'", b"D:20240923145806+01'00'")
    return n, dict(minfo=minfo, vlist=vlist, jtruth=jtruth, sp=sp, amr=amr)
