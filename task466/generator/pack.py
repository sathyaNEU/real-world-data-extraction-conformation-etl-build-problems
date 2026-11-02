"""Writes the evidence pack under task466/target/ from the simulated world (world.py, records.py)."""
import datetime as dt
import os
import shutil

import numpy as np

import common as C
import records as R
import world as W

AUTH = "Quarrow Valley Regional Solid Waste Authority"
SITE = "Breck Hollow Landfill"
OPER = "Leyland Renewable Gas"
COOP = "Sauk Prairie Electric Cooperative"
DEQ = "State Department of Environmental Quality"


def lt(t):
    return C.local(t).strftime("%Y-%m-%d %H:%M")


def lts(t):
    return C.local(t).strftime("%Y-%m-%d %H:%M:%S")


def write_pack(t, target):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    C.pdf_canvas_settings()
    files = {}
    files["scada"] = write_scada(t, target)
    files["outages"] = write_outage_log(t, target)
    files["rule"] = write_rule(target)
    files["events"] = write_event_log(t, target)
    files["reports"] = write_operator_reports(t, target)
    files["sem"] = write_sem(t, target)
    files["checks"] = write_analyser_checks(t, target)
    files["plan"] = write_gas_plan(target)
    files["site"] = write_site_register(target)
    files["wells"] = write_well_register(t, target)
    files["weather"] = write_weather(t, target)
    files["leachate"] = write_leachate(t, target)
    files["weighbridge"] = write_weighbridge(t, target)
    return files


# ------------------------------------------------------------------------------------------------ SCADA hourly
def write_scada(t, target):
    fn = "BH_gas_plant_hourly_2024-2026.csv"
    p = t["plant"]
    r = W.rng(200)
    rho = W.RHO_N
    rows = []
    blower_a_months = {m for m in range(1, 13) if m % 2 == 1}
    for h, ts in enumerate(p["times"]):
        rf = p["run_frac"][h]
        loc = C.local(ts)
        a_duty = (loc.month in blower_a_months) ^ (loc.year % 2 == 0)
        blwa = rf if a_duty else 0.0
        blwb = 0.0 if a_duty else rf
        f1 = p["eng_fuel"][1][h] / (p["ch4"][h] / 100.0 * rho) if rf > 0 else 0.0
        f2 = p["eng_fuel"][2][h] / (p["ch4"][h] / 100.0 * rho) if rf > 0 else 0.0
        fl_true = p["flare_kg"][h] / (p["ch4"][h] / 100.0 * W.RHO_S) if rf > 0 else 0.0   # the meter's own m3 (20 C)
        fl = fl_true if fl_true >= W.FLARE_CUTOFF_M3H else 0.0
        lit = t["flare_lit_h"][h]
        temp = (1560 + r.normal(0, 25)) * lit + (r.uniform(140, 420)) * (1 - lit) if lit > 0 else r.uniform(110, 380)
        if rf > 0:
            row = [ts.strftime("%Y-%m-%d %H:%M"), "%.2f" % blwa, "%.2f" % blwb, "%.1f" % p["flow"][h],
                   "%.2f" % p["ch4"][h], "%.2f" % p["o2"][h], "%.2f" % p["co2"][h], "%.1f" % p["vac"][h],
                   "%.1f" % f1, "%.1f" % f2, "%.1f" % fl, "%.0f" % temp]
        else:
            row = [ts.strftime("%Y-%m-%d %H:%M"), "0.00", "0.00", "0.0", "", "", "", "%.1f" % p["vac"][h],
                   "0.0", "0.0", "0.0", "%.0f" % temp]
        rows.append(row)
    header = ["Timestamp (UTC)", "BLWA run (h)", "BLWB run (h)", "FT-101 LFG flow (Nm3/h)", "AT-101 CH4 (%)",
              "AT-101 O2 (%)", "AT-101 CO2 (%)", "PT-101 header vacuum (inWC)", "FT-201 GEN1 fuel (Nm3/h)",
              "FT-202 GEN2 fuel (Nm3/h)", "FT-301 flare gas (m3/h)", "TT-301 flare temp (F)"]
    pre = ["# Breck Hollow LFG plant historian - hourly averages",
           "# Export: 2027-01-04 08:12 UTC by tlhays (Leyland Renewable Gas)",
           "# Interval: 1 h, labelled at interval start"]
    C.write_csv(os.path.join(target, fn), header, rows, preamble=pre)
    return fn


# ------------------------------------------------------------------------------------------------ outage log
def write_outage_log(t, target):
    import openpyxl
    from openpyxl.styles import Font
    fn = "BH_gas_plant_outage_log_2024-2026.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Outages"
    ws.append(["Breck Hollow LFG plant - blower outages (gas system down). Times are site local time."])
    ws["A1"].font = Font(bold=True)
    ws.append([])
    ws.append(["No.", "Stopped", "Restarted", "Duration (h:mm)", "Cause", "Notes", "By"])
    for c in ws[3]:
        c.font = Font(bold=True)
    r = W.rng(210)
    initials = ["TLH", "JL", "TLH", "RMK", "JL"]
    notes = {"Utility power failure": ["Co-op feeder outage", "Supply lost, restored by co-op", "Lightning, feeder 4"],
             "Blower trip - high bearing temperature": ["Reset, bearing temp normal", "Changed to standby blower"],
             "Condensate knockout high level - plant ESD": ["Drained KO pot, pump reset", "Float switch cleaned"],
             "Gas analyser fault - plant ESD": ["Sample pump replaced", "Analyser rebooted"],
             "Planned shutdown - blower and valve maintenance": ["Per work order", "Header valve replacement"],
             "Storm - damage to plant supply line": ["Pole down on access road", "Ice storm, line repaired"],
             "Annual shutdown - flare and header inspection": ["Annual inspection, refractory OK"]}
    for k, o in enumerate(t["plant"]["outages"]):
        mins = int(round(o["hours"] * 60))
        nn = notes[o["cause"]]
        ws.append([k + 1, lt(o["start"]), lt(o["end"]), "%d:%02d" % (mins // 60, mins % 60), o["cause"],
                   nn[int(r.integers(0, len(nn)))], initials[int(r.integers(0, len(initials)))]])
    for col, w in zip("ABCDEFG", (6, 18, 18, 15, 46, 34, 6)):
        ws.column_dimensions[col].width = w
    C.save_workbook(wb, os.path.join(target, fn), dt.datetime(2027, 1, 5, 10, 0), OPER)
    return fn


# ------------------------------------------------------------------------------------------------ rule extract
def write_rule(target):
    fn = "DEQ_closed_landfill_methane_rule_extract.pdf"
    blocks = [
        ("%s" % DEQ, "B", 12),
        ("Closed Landfill Methane Rule (extract: Parts 1, 4, 5 and 6 and Schedule 2)", "B", 11),
        ("As amended effective 1 January 2025.", "", 9),
        ("", "", 9),
        ("Part 1  Definitions", "B", 10),
        ("1.1  Reporting year: a calendar year, local time.", "", 9),
        ("1.2  Methane generated: the methane the waste in a landfill produces in the reporting year.", "", 9),
        ("1.3  Methane captured: the methane a landfill's gas system draws from the landfill in the reporting year, "
         "measured at its gas plant as the landfill gas flow at normal conditions (0 degrees C, 101.325 kPa) times its "
         "methane content. A normal cubic metre of methane weighs 0.7168 kg.", "", 9),
        ("1.4  Collection efficiency: the fraction of the methane being generated beneath a landfill's cap that its gas "
         "system draws off while it runs, as set in Schedule 2.", "", 9),
        ("1.5  Destruction device: an engine, boiler or flare that burns captured landfill gas. Methane destroyed: the "
         "methane routed to a destruction device times the device's destruction efficiency in Schedule 2.", "", 9),
        ("1.6  Methane released: the methane generated in the reporting year less the methane captured, of which the "
         "fraction set in Schedule 2 is taken as oxidised in the cap, plus the methane captured and not destroyed.", "", 9),
        ("1.7  Operating hours: for an engine, the time it is synchronised to the grid and generating; for a flare, the "
         "time it burns landfill gas at or above its minimum combustion temperature of 1,400 degrees F. Hours are "
         "elapsed time summed, not a count of clock hours.", "", 9),
        ("1.8  Engine start: each time an engine is started from standstill.", "", 9),
        ("", "", 9),
        ("Part 4  Closed landfills with gas systems", "B", 10),
        ("4.1  A closed landfill whose gas system operated in the reporting year estimates its methane generated from its "
         "methane captured, at the collection efficiency of Schedule 2 for its cover.", "", 9),
        ("4.2  Where a landfill's cover falls in more than one class of Schedule 2, the collection efficiency is the "
         "average of the classes weighted by area.", "", 9),
        ("", "", 9),
        ("Part 5  Annual methane charge, closed landfills", "B", 10),
        ("5.1  The owner of a closed landfill pays an annual charge on the methane released in the reporting year:", "", 9),
        ("  Tier 1   methane released under 375 tonnes                         no charge", "T", 8),
        ("  Tier 2   375 tonnes or more and under 450 tonnes                   $118,000", "T", 8),
        ("  Tier 3   450 tonnes or more                                        $312,000 and a corrective action plan", "T", 8),
        ("5.2  The Department invoices the charge by 30 June of the year after the reporting year.", "", 9),
        ("", "", 9),
        ("Part 6  Annual return", "B", 10),
        ("6.1  The owner files by 31 March a return for the reporting year stating the methane generated, captured, "
         "destroyed in each destruction device and released; for each destruction device its operating hours in each "
         "quarter and, for an engine, its starts; and the surface monitoring results required by the landfill's gas "
         "management plan.", "", 9),
        ("", "", 9),
        ("Schedule 2  Factors", "B", 10),
        ("Collection efficiency (rule 1.4):", "", 9),
        ("  Final cover with geomembrane                         0.90", "T", 8),
        ("  Final soil cover, 2 ft or more                       0.80", "T", 8),
        ("  Intermediate cover                                   0.65", "T", 8),
        ("  Area with no gas collection                          0.00", "T", 8),
        ("Fraction of uncaptured methane oxidised in the cap:  0.10", "T", 8),
        ("Destruction efficiency: engine 0.99; enclosed flare 0.99; open flare 0.96", "T", 8),
    ]
    C.text_pdf(os.path.join(target, fn), "Closed Landfill Methane Rule - extract", blocks, author="Air Quality Division")
    return fn


# ------------------------------------------------------------------------------------------------ plant event log
def write_event_log(t, target):
    fn = "BH_engine_plant_events_2026.txt"
    a, b = R.quarter_minutes(2026, 0)[0], R.quarter_minutes(2026, 3)[1]
    lines = ["BRECK HOLLOW ENERGY PLANT  -  EVENT LOG EXPORT  -  2026-01-01 00:00 TO 2026-12-31 23:59 (SITE TIME)",
             "EXPORTED 2027-01-04 08:40 BY TLHAYS",
             "",
             "DATE        TIME      UNIT  EVENT                 TEXT"]
    for m, tag, code, text in t["events"]:
        if m < a - 60 * 24 * 3 or m >= b:
            continue
        ts = R.minute_time(m)
        loc = C.local(ts)
        if loc.year != 2026:
            continue
        lines.append("%s  %s  %-4s  %-20s  %s" % (loc.strftime("%Y-%m-%d"), loc.strftime("%H:%M:%S"), tag, code, text))
    with open(os.path.join(target, fn), "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\n".join(lines) + "\n")
    return fn


# ------------------------------------------------------------------------------------------------ operator monthly reports
def write_operator_reports(t, target):
    fn = "Leyland_BH_monthly_operating_reports_2026.pdf"
    p = t["plant"]
    blocks = [("%s - %s energy plant: monthly operating reports, 2026" % (OPER, SITE), "B", 12),
              ("Prepared for the %s under the 2016 gas rights agreement." % AUTH, "", 9), ("", "", 9)]
    r = W.rng(220)
    hm = {1: 61234.0, 2: 59876.0}
    kwh = {1: 48877000.0, 2: 47912000.0}
    prev_visit = dt.datetime(2025, 12, 30, 10, 0, tzinfo=C.TZ)
    for mo in range(1, 13):
        visit_day = int(r.integers(2, 7))
        visit = dt.datetime(2026 + (1 if mo == 12 else 0), (mo % 12) + 1, visit_day, 10, 0, tzinfo=C.TZ) if mo < 12 else \
            dt.datetime(2027, 1, 4, 10, 0, tzinfo=C.TZ)
        a = int((prev_visit.astimezone(C.UTC) - W.T0).total_seconds() // 60)
        b = int((visit.astimezone(C.UTC) - W.T0).total_seconds() // 60)
        blocks.append(("%s 2026" % dt.date(2026, mo, 1).strftime("%B"), "B", 10))
        blocks.append(("Service visit: %s.  Previous visit: %s." % (visit.strftime("%d %b %Y"), prev_visit.strftime("%d %b %Y")), "", 9))
        rows = []
        for e in (1, 2):
            on = p["eng_on_min"][e][a:b]
            run_h = on.sum() / 60.0
            # the hour meter also turns during warm-up, cool-down and unsynchronised test running
            n_st = int(((on[1:] & ~on[:-1]).sum()))
            test_h = sum(max(0, min(s["test"][1], b) - max(s["test"][0], a)) for s in p["eng_stops"][e] if "test" in s) / 60.0
            meter_h = run_h + test_h + n_st * 0.21 + r.uniform(0.5, 4.0)
            fuel_kg = p["eng_fuel"][e][a // 60:b // 60].sum()
            gen = fuel_kg * W.LHV_KWH_PER_KG * W.ENG_EFF
            hm0, kw0 = hm[e], kwh[e]
            hm[e] += meter_h
            kwh[e] += gen
            rows.append("  Engine %d   hour meter %9.1f -> %9.1f  (%6.1f h)   kWh meter %12.0f -> %12.0f" %
                        (e, hm0, hm[e], hm[e] - hm0, kw0, kwh[e]))
        for row in rows:
            blocks.append((row, "T", 7))
        avail = 100.0 * (1 - (1 - p["run_frac"][a // 60:b // 60]).mean())
        blocks.append(("Plant availability (gas system) %.1f%%. Flare: standby duty as required." % avail, "", 9))
        blocks.append(("", "", 9))
        prev_visit = visit
    blocks.append(("Leyland Renewable Gas - Tina Hays, plant manager", "", 9))
    C.text_pdf(os.path.join(target, fn), "Monthly operating reports 2026", blocks, author="Tina Hays")
    return fn


# ------------------------------------------------------------------------------------------------ surface walkovers
def write_sem(t, target):
    import openpyxl
    from openpyxl.styles import Font
    fn = "BH_surface_emissions_monitoring_2026.xlsx"
    wb = openpyxl.Workbook()
    first = True
    for wk in t["walks"]:
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = "Q%d walkover" % wk["q"]
        ws.append(["Breck Hollow - quarterly surface emissions walkover, Q%d 2026. Logger export, ppm methane." % wk["q"]])
        ws["A1"].font = Font(bold=True)
        ws.append(["Date", "Time", "Point", "Easting (ft)", "Northing (ft)", "CH4 (ppm)", "Background (ppm)", "Operator"])
        for c in ws[2]:
            c.font = Font(bold=True)
        for row in sorted(wk["rows"], key=lambda x: x["t"]):
            ws.append([row["t"].strftime("%Y-%m-%d"), row["t"].strftime("%H:%M:%S"), row["label"],
                       round(row["x"], 1), round(row["y"], 1), round(row["ppm_logged"], 0), 3, "JL"])
    ws = wb.create_sheet("Re-monitoring")
    ws.append(["Breck Hollow - re-monitoring of marked exceedance locations after repair. Position by handheld GPS (WGS84) as found on the day."])
    ws["A1"].font = Font(bold=True)
    ws.append(["Date", "Time", "Ref", "Latitude", "Longitude", "CH4 (ppm)", "Repair"])
    for c in ws[2]:
        c.font = Font(bold=True)
    r = W.rng(230)
    rep = ["Cap seam re-welded", "Well boot re-sealed", "Soil added at penetration", "Boot clamp tightened"]
    for row in t["walks"][0]["rm_rows"]:
        la, lo = R.site_to_wgs84(row["x"], row["y"])
        ws.append([row["t"].strftime("%Y-%m-%d"), row["t"].strftime("%H:%M"), row["label"], round(la, 6), round(lo, 6),
                   round(row["ppm"], 0), rep[int(r.integers(0, len(rep)))]])
    C.save_workbook(wb, os.path.join(target, fn), dt.datetime(2027, 1, 12, 15, 0), AUTH)
    return fn


def write_analyser_checks(t, target):
    fn = "SEM_analyser_checks_2026.csv"
    rows = []
    for c in t["checks"]:
        rows.append([c["t"].strftime("%Y-%m-%d"), c["t"].strftime("%H:%M"), "%.1f" % c["zero"], "%.0f" % c["span_ref"],
                     "%.1f" % c["span_read"], c["result"], c.get("note", "")])
    C.write_csv(os.path.join(target, fn), ["date", "time", "zero_ppm", "span_gas_ppm", "span_read_ppm", "result", "note"],
                rows)
    return fn


def write_gas_plan(target):
    fn = "BH_gas_management_plan_2025.pdf"
    blocks = [
        ("%s - Landfill Gas Management Plan (revision 4, March 2025)" % SITE, "B", 12),
        ("%s. Extract: sections 2, 7 and 8." % AUTH, "", 9),
        ("", "", 9),
        ("2  The gas system", "B", 10),
        ("2.1  The gas system collects landfill gas from 58 vertical wells and 4 horizontal collectors under the "
         "geomembrane cap and delivers it to the gas plant, where two blowers (one on duty, one on standby) draw the "
         "wellfield. The gas is burned in two engine-generators operated by Leyland Renewable Gas under the 2016 gas "
         "rights agreement, or in the enclosed flare when the engines cannot take it.", "", 9),
        ("", "", 9),
        ("7  Surface emissions monitoring", "B", 10),
        ("7.1  A walkover of the whole cap is made each quarter along a grid of 98.4 ft (30 m) spacing and at every well "
         "boot, with a portable flame ionisation analyser held within 3 inches of the surface.", "", 9),
        ("7.2  An exceedance is a reading of more than 500 ppm methane above background. Each exceedance location is "
         "marked, repaired within five days and re-monitored within ten days of the walkover; a location still over 500 "
         "ppm at re-monitoring is repaired again and re-monitored again within ten days.", "", 9),
        ("7.3  The analyser is zeroed and checked against a 500 ppm methane span gas at the start of each walkover day, at "
         "midday and at the end. If a check fails, the readings taken since the last passing check are void and those "
         "points are walked again after recalibration.", "", 9),
        ("", "", 9),
        ("8  Reporting", "B", 10),
        ("8.1  The Authority files the annual return under the Closed Landfill Methane Rule by 31 March, with the "
         "surface monitoring results of the reporting year.", "", 9),
    ]
    C.text_pdf(os.path.join(target, fn), "Landfill gas management plan", blocks, author=AUTH)
    return fn


def write_site_register(target):
    import openpyxl
    from openpyxl.styles import Font
    fn = "BH_site_register_2025.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Site"
    rows = [("Item", "Value"), ("Site", SITE), ("Owner", AUTH), ("Waste received", "September 1974 to 31 March 2017"),
            ("Waste in place (closure report, 2017)", "4.87 million tons"),
            ("Cap phase 1 (north and west cells), completed", "October 2018"),
            ("Cap phase 2 (south and east cells), completed", "September 2019"),
            ("Cap construction", "40-mil LLDPE geomembrane over 18 in. soil barrier, 24 in. cover soil"),
            ("Capped area", "%.1f acres (whole waste footprint)" % W.AREA_ACRES),
            ("Gas wells", "58 vertical wells, 4 horizontal collectors"),
            ("Gas plant", "2 blowers (duty/standby), enclosed flare 1,500 scfm, 2 engine-generators 1,060 kW each"),
            ("Engine operator", OPER), ("Electricity purchaser", COOP),
            ("Site grid", "US survey feet, grid north = true north; E1000 N2000 = 43.183150 N, 89.672840 W (WGS84)")]
    for rr in rows:
        ws.append(list(rr))
    ws["A1"].font = Font(bold=True)
    ws["B1"].font = Font(bold=True)
    ws.column_dimensions["A"].width = 44
    ws.column_dimensions["B"].width = 70
    C.save_workbook(wb, os.path.join(target, fn), dt.datetime(2025, 3, 20, 9, 0), AUTH)
    return fn


def write_well_register(t, target):
    import openpyxl
    from openpyxl.styles import Font
    fn = "BH_well_register_2025.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Wells"
    ws.append(["Well", "Type", "Zone", "Easting (ft)", "Northing (ft)", "Depth (ft)", "Screen top (ft bgs)", "Installed"])
    for c in ws[1]:
        c.font = Font(bold=True)
    r = W.rng(240)
    boots = [pt for pt in t["walks"][0]["pts"] if pt["kind"] == "boot"]
    for k, pt in enumerate(boots):
        ws.append([pt["label"].replace("WB-", ""), "vertical" if k < 58 else "horizontal",
                   "Z%d" % (1 + int(pt["x"] // 400) % 6), round(pt["x"], 1), round(pt["y"], 1),
                   int(r.uniform(38, 96)), int(r.uniform(12, 25)), "2018" if k < 30 else "2019"])
    C.save_workbook(wb, os.path.join(target, fn), dt.datetime(2025, 3, 20, 9, 0), AUTH)
    return fn


def write_weather(t, target):
    fn = "weather_station_daily_2024-2026.csv"
    rows = [[d["d"].isoformat(), d["tmax"], d["tmin"], d["p"], d["rain"]] for d in t["weather"]]
    C.write_csv(os.path.join(target, fn), ["date", "tmax_c", "tmin_c", "pressure_mean_hpa", "rain_mm"], rows)
    return fn


def write_leachate(t, target):
    fn = "leachate_pumping_2026.csv"
    rows = [[d["d"].isoformat(), d["sump"], d["level"], d["pumped"], d["hauled"]] for d in t["leachate"]]
    C.write_csv(os.path.join(target, fn), ["date", "sump", "level_ft", "pumped_gal", "hauled_gal"], rows)
    return fn


def write_weighbridge(t, target):
    fn = "BH_weighbridge_archive_2004-2017.csv"
    rows = [[d["y"], d["m"], d["code"], d["name"], d["tons"]] for d in t["weighbridge"]]
    C.write_csv(os.path.join(target, fn), ["year", "month", "code", "description", "tons"], rows)
    return fn
