"""Writes the Rathgarvan pack into target/ from the world: thirteen files in five formats."""
import datetime as dt
import os
from zoneinfo import ZoneInfo

import numpy as np
from docx import Document
from docx.shared import Pt
from openpyxl import Workbook
from openpyxl.styles import Font

import io_util as IO
import params as P
import world as W

FILES = {
    "stays": "mobility_stays_2027w36_w47.csv",
    "devices": "mobility_devices_2027w36_w47.csv",
    "cells": "cell_zone_lookup_v3.csv",
    "census": "census2022_pow_rathgarvan_catchment.xlsx",
    "case": "rathgarvan_fbc_demand_refresh_dec2027.pdf",
    "review": "lisnagry_opening_review_apr2020.pdf",
    "gates": "ardnagree_line_gate_entries_20180101_20271130.csv",
    "register": "ardnagree_line_station_register.csv",
    "calendar": "kilcarrow_calendar_2018_2027.csv",
    "panel_note": "vantra_resident_panel_extract_notes.pdf",
    "housing": "rathgarvan_housing_pipeline_oct2027.xlsx",
    "jobs": "kilcarrow_employment_outlook_2030.docx",
    "timetable": "ardnagree_line_draft_timetable_2028.csv",
}
DISTRACTORS = ["housing", "jobs", "timetable"]
UTC = ZoneInfo("UTC")
LOCAL = ZoneInfo(P.TZ)


def to_utc(t):
    return t.replace(tzinfo=LOCAL).astimezone(UTC)


def zstamp(t):
    return t.strftime("%Y-%m-%dT%H:%M:00Z")


def panel_rows(devices):
    """The provider's extract: stays of 20 minutes or more starting on a local weekday in the panel weeks."""
    days = set(W.weekdays(P.PANEL_START, P.PANEL_END))
    rows, dev_rows = [], []
    for dev in devices:
        stays = [a for a in dev.acts] + W.home_stays(dev)
        stays.sort(key=lambda a: a[1])
        out = []
        for cell, s, e, _tag in stays:
            s = s.replace(second=0, microsecond=0)
            e = e.replace(second=0, microsecond=0)
            if s.date() not in days or (e - s).total_seconds() < 20 * 60:
                continue
            out.append((dev.did, cell, zstamp(to_utc(s)), zstamp(to_utc(e))))
        if not out:
            continue
        rows += out
        dev_rows.append((dev.did, dev.home, out[0][2], max(r[3] for r in out)))
    rows.sort(key=lambda r: (r[0], r[2]))
    dev_rows.sort()
    return rows, dev_rows


def cell_rows():
    names = {c: n for c, n, _p, _t, _s in P.DEST}
    rows = []
    sa = [c for c, _ in P.SMALL_AREAS]
    for i, (cell, _w) in enumerate(P.HOME_CELLS):
        a, b = sa[i % len(sa)], sa[(i + 3) % len(sa)]
        if i in (1, 5):
            rows.append((cell, a, "Small area %s (Rathgarvan)" % a, "0.64"))
            rows.append((cell, b, "Small area %s (Rathgarvan)" % b, "0.36"))
        else:
            rows.append((cell, a, "Small area %s (Rathgarvan)" % a, "1.00"))
    seen = set(c for c, _w in P.HOME_CELLS)
    for zone, cells in P.WORK_CELLS.items():
        for c in cells:
            if c in seen:
                continue
            seen.add(c)
            if c in P.STRADDLE:
                for z, sh in P.STRADDLE[c]:
                    rows.append((c, z, names[z], "%.2f" % sh))
            else:
                rows.append((c, zone, names[zone], "1.00"))
    for c in P.OUTSIDE_CELLS:
        rows.append((c, "KX03", "Outside County Kilcarrow", "1.00"))
    rows.sort()
    return rows


def write_census(path, final, prov):
    wb = Workbook()
    ws = wb.active
    ws.title = "Final release"
    note = ("Persons aged 15 and over at work, by small area of usual residence and zone of usual workplace. "
            "'Works mainly at or from home' counts persons who gave no regular workplace away from home; "
            "'No fixed place of work' counts persons whose work takes them to changing locations.")
    for sheet, rows, title in ((ws, final, "Census 2022 place of work: Rathgarvan catchment small areas, final release "
                                            "(October 2023)"),
                               (wb.create_sheet("Provisional release"), prov,
                                "Census 2022 place of work: Rathgarvan catchment small areas, provisional release "
                                "(June 2023)")):
        sheet["A1"] = title
        sheet["A1"].font = Font(bold=True)
        sheet["A2"] = note
        sheet["A3"] = "Source: Census 2022, place of work tables, small area of residence by workplace zone, as held " \
                      "by the Kilcarrow Metropolitan Transport Authority GIS team."
        hdr = ["Small area of residence", "Workplace zone code", "Workplace zone", "Persons at work"]
        for j, h in enumerate(hdr, 1):
            sheet.cell(row=5, column=j, value=h).font = Font(bold=True)
        for i, r in enumerate(rows, 6):
            for j, v in enumerate(r, 1):
                sheet.cell(row=i, column=j, value=v)
        sheet.column_dimensions["A"].width = 22
        sheet.column_dimensions["B"].width = 18
        sheet.column_dimensions["C"].width = 34
        sheet.column_dimensions["D"].width = 15
    wb.save(path)
    IO.repack_ooxml(path, "GIS Team", "GIS Team", "2023-10-19T10:12:00Z", "2023-10-19T15:40:00Z",
                    "Census 2022 place of work, Rathgarvan catchment", "Kilcarrow Metropolitan Transport Authority")


def ordinary_weekday_mean(gates, code, d0, d1, hol):
    v = [n for d, c, n in gates if c == code and d0 <= d <= d1 and d.weekday() < 5 and d not in hol]
    return sum(v) / len(v), len(v)


def write_review(path, gates):
    hol = set(P.BANK_HOLIDAYS_2019) | set(P.MIDTERM_2019) | {dt.date(2019, 12, 23) + dt.timedelta(days=i)
                                                            for i in range(12)} | {dt.date(2020, 2, 17) + dt.timedelta(days=i)
                                                                                 for i in range(5)}
    mean, n = ordinary_weekday_mean(gates, "LSG", dt.date(2019, 10, 7), dt.date(2020, 2, 28), hol)
    months = [("October 2019", dt.date(2019, 10, 1), dt.date(2019, 10, 31)),
              ("November 2019", dt.date(2019, 11, 1), dt.date(2019, 11, 30)),
              ("December 2019", dt.date(2019, 12, 1), dt.date(2019, 12, 31)),
              ("January 2020", dt.date(2020, 1, 1), dt.date(2020, 1, 31)),
              ("February 2020", dt.date(2020, 2, 1), dt.date(2020, 2, 29))]
    tab = [["Month", "Gate entries, all days (thousands)", "Ordinary weekdays"]]
    for name, a, b in months:
        tot = sum(nv for d, c, nv in gates if c == "LSG" and a <= d <= b)  # Lisnagry has one gateline
        k = sum(1 for d, c, nv in gates if c == "LSG" and a <= d <= b and d.weekday() < 5 and d not in hol)
        tab.append([name, "%.1f" % (tot / 1000.0), str(k)])
    diff = 100.0 * (mean - P.LISNAGRY_FORECAST) / P.LISNAGRY_FORECAST
    blocks = [
        ("t", "Lisnagry Station: post-opening review"),
        ("s", "Kilcarrow Metropolitan Transport Authority, Rail Planning. April 2020. Prepared by Deaglan Gilmore."),
        ("h", "1. The station"),
        ("p", "Lisnagry station opened on Monday 2 September 2019 on the Ardnagree line, between Ardnagree and "
              "Kilcarrow Central, with a 120-space car park and four-car platforms. Trains call every 15 minutes in "
              "the weekday peaks and every 30 minutes at other times."),
        ("h", "2. Forecast and outturn"),
        ("p", "The 2018 business case forecast %s commuter boardings on an average ordinary weekday in the first "
              "full year, built from the Census 2016 place-of-work tables for the station's catchment small areas at "
              "the station shares of the 2017 mode choice model." % "{:,}".format(P.LISNAGRY_FORECAST)),
        ("p", "After the opening weeks, the gates recorded an average of %s entries on ordinary weekdays from 7 "
              "October 2019 to 28 February 2020 (%d ordinary weekdays, public holidays and school breaks excluded), "
              "%+.1f per cent against the forecast. The on-board survey of 12 November 2019 found 93 per cent of "
              "boardings at Lisnagry before 10:00 were journeys to work." % ("{:,}".format(int(round(mean))), n, diff)),
        ("table", tab),
        ("h", "3. Car park and access"),
        ("p", "The car park filled by 08:10 on most weekdays from October. Cycle parking (24 stands) averaged 11 "
              "bicycles. Walk-in share of morning entries was 58 per cent in the November survey."),
        ("h", "4. Points for the line"),
        ("p", "Platform lighting at the Ardnagree end was upgraded in January 2020 after customer comments. Real-time "
              "information screens were commissioned on 4 November 2019."),
    ]
    IO.write_pdf(path, "Lisnagry Station post-opening review", "Deaglan Gilmore", "Microsoft Word for Microsoft 365",
                 blocks, "KMTA Rail Planning | Lisnagry post-opening review | April 2020", "D:20200421143300Z",
                 "D:20200421143300Z")
    return mean, n


def write_case(path):
    names = {c: n for c, n, _p, _t, _s in P.DEST}
    shares = [["Workplace zone code", "Workplace zone", "Station share of journeys to work"]]
    for c, n, _p, _t, s in P.DEST:
        shares.append([c, n, "%.2f" % s])
    sas = [["Small area", "Usual residents (2022)"]]
    pops = [1612, 1158, 1534, 1243, 1446, 1337, 1251]
    for (sa, _w), pop in zip(P.SMALL_AREAS, pops):
        sas.append([sa, "{:,}".format(pop)])
    blocks = [
        ("t", "Rathgarvan Station: Final Business Case, demand refresh"),
        ("s", "Kilcarrow Metropolitan Transport Authority, Rail Planning. Draft for the Investment Committee meeting of "
              "14 December 2027. Version 0.4, 6 December 2027. Author: Colum Curtis."),
        ("h", "1. Purpose"),
        ("p", "The new station at Rathgarvan opens in September 2028 on the Ardnagree line between Lisnagry and "
              "Kilcarrow Central. This refresh restates the commuter demand on which the Investment Committee will "
              "choose the station's scope."),
        ("h", "2. The demand the refresh states"),
        ("p", "Commuter boardings are the journeys to work that residents of the station's catchment begin at "
              "Rathgarvan on an average ordinary weekday in 2029, the station's first full year. An ordinary weekday "
              "is a Monday to Friday in school term that is not a public holiday."),
        ("p", "The catchment's commuters are the persons the Census 2022 place-of-work tables (final release) count "
              "in the seven small areas of Table 1, by zone of usual workplace, held at the 2022 base. Each workplace "
              "zone contributes the journeys to work its commuters make, at the station share the authority's 2026 "
              "mode choice model gives that zone (Table 2). Persons who work mainly at or from home, have no fixed "
              "place of work or work outside County Kilcarrow are outside the station's commuter market."),
        ("table", sas),
        ("p", "Table 1. Catchment small areas (within 1.2 km walk of the station entrances)."),
        ("table", shares),
        ("p", "Table 2. Station share of journeys to work from the catchment, by workplace zone (2026 mode choice "
              "model, run 26-07)."),
        ("h", "3. Scope decision"),
        ("p", "The full scheme (six-car platforms, a 220-space car park and the second entrance at Mill Road) is "
              "justified where the station carries %s or more commuter boardings on an average ordinary weekday in "
              "2029. Below that, the reduced scheme is built: four-car platforms and a 90-space car park, with passive "
              "provision for platform extension." % "{:,}".format(P.THRESHOLD)),
        ("h", "4. Evidence held"),
        ("p", "Census 2022 place-of-work tables for the catchment small areas (final and provisional releases); the "
              "operator's daily gate entries on the Ardnagree line since January 2018 and the station register; the "
              "Lisnagry post-opening review (April 2020); a twelve-week extract of Vantra Mobile's resident mobility "
              "panel for devices resident in the catchment (September to November 2027) with its cell lookup; the "
              "Rathgarvan housing pipeline (October 2027); the county employment outlook to 2030; the draft 2028 "
              "timetable."),
        ("h", "5. Programme"),
        ("p", "Investment Committee scope decision 14 December 2027; main works contract award March 2028; station "
              "opening September 2028; first full year of operation 2029."),
    ]
    IO.write_pdf(path, "Rathgarvan Station FBC demand refresh", "Colum Curtis", "Microsoft Word for Microsoft 365",
                 blocks, "KMTA Rail Planning | Rathgarvan FBC demand refresh | DRAFT v0.4 | 6 December 2027",
                 "D:20271206091500Z", "D:20271206094000Z", widths={3: [38 * 2.835, 80 * 2.835, 52 * 2.835]})


def write_panel_note(path):
    blocks = [
        ("t", "Resident Mobility Panel: extract notes"),
        ("s", "Vantra Insights (Vantra Mobile Ireland). Extract RMP-2027-114 for the Kilcarrow Metropolitan Transport "
              "Authority, delivered 1 December 2027. Contact: Eve Dunne, Data Products."),
        ("h", "Population"),
        ("p", "Devices on the Vantra network whose home cell lies in the Rathgarvan catchment cells listed in the "
              "licence schedule and which were active on at least 20 days of the extract weeks. Panel penetration in "
              "the catchment is about one resident adult in eleven. No expansion weights are supplied with this "
              "extract."),
        ("h", "Files"),
        ("table", [["File", "Contents"],
                   ["mobility_devices_2027w36_w47.csv", "device_id; home_cell; first_seen_utc and last_seen_utc "
                    "(the first stay start and last stay end in the extract)"],
                   ["mobility_stays_2027w36_w47.csv", "device_id; cell_id; stay_start_utc; stay_end_utc"],
                   ["cell_zone_lookup_v3.csv", "cell_id; zone_code; zone_name; area_share (share of the cell's "
                    "coverage area lying in the zone)"]]),
        ("h", "Definitions"),
        ("p", "A stay is a period of 20 minutes or more in which the device's location resolved to one cell. Stays "
              "are cut where the device's location changes cell or the device is inactive for more than 90 minutes. "
              "Stay times are in UTC to the minute. The extract holds every stay that starts on a local weekday from "
              "Monday 6 September to Friday 26 November 2027 (ISO weeks 36 to 47), each stay running to its end "
              "even where that falls after the window."),
        ("p", "The home cell is the cell where the device spent the most time between 22:00 and 06:00 local time "
              "over the extract weeks. A device_id is reissued when a SIM card is replaced; reissued identifiers "
              "are not linked to the earlier identifier. Device identifiers are not stable across extracts."),
        ("h", "Use"),
        ("p", "Licensed to the Kilcarrow Metropolitan Transport Authority for transport planning under licence "
              "2027-114. Counts of fewer than ten devices may not be published."),
    ]
    IO.write_pdf(path, "Resident Mobility Panel extract notes RMP-2027-114", "Eve Dunne", "Vantra Insights reporting",
                 blocks, "Vantra Insights | RMP-2027-114 | Commercial in confidence", "D:20271201103000Z",
                 "D:20271201103000Z", widths={2: [62 * 2.835, 108 * 2.835]})


def calendar_rows():
    rows = []
    def add(d, kind, name):
        rows.append((d.isoformat(), d.strftime("%A"), kind, name))
    for y in range(2018, 2028):
        hol = []
        hol.append((dt.date(y, 1, 1), "New Year's Day"))
        hol.append((dt.date(y, 3, 17), "St Patrick's Day"))
        for m, nm in ((5, "May bank holiday"), (6, "June bank holiday"), (8, "August bank holiday")):
            first = dt.date(y, m, 1)
            hol.append((first + dt.timedelta(days=(7 - first.weekday()) % 7), nm))
        oct_last = dt.date(y, 10, 31)
        hol.append((oct_last - dt.timedelta(days=oct_last.weekday()), "October bank holiday"))
        if y < 2027:
            hol.append((dt.date(y, 12, 25), "Christmas Day"))
            hol.append((dt.date(y, 12, 26), "St Stephen's Day"))
        for d, nm in hol:
            add(d, "public holiday", nm)
        mon = oct_last - dt.timedelta(days=oct_last.weekday())
        for i in range(5):
            add(mon + dt.timedelta(days=i), "school break", "October mid-term")
        feb = dt.date(y, 2, 1) + dt.timedelta(days=(7 - dt.date(y, 2, 1).weekday()) % 7 + 14)
        for i in range(5):
            add(feb + dt.timedelta(days=i), "school break", "February mid-term")
        d = dt.date(y, 7, 1)
        while d <= dt.date(y, 8, 31):
            if d.weekday() < 5:
                add(d, "school break", "Summer holidays")
            d += dt.timedelta(days=1)
        if y < 2027:
            d = dt.date(y, 12, 22)
            while d <= dt.date(y + 1, 1, 5):
                if d.weekday() < 5:
                    add(d, "school break", "Christmas holidays")
                d += dt.timedelta(days=1)
    rows = sorted(set(rows))
    return rows


def write_housing(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Pipeline"
    ws["A1"] = "Rathgarvan local area: residential pipeline, October 2027"
    ws["A1"].font = Font(bold=True)
    ws["A2"] = "Units by site and expected completion year (Planning Department returns)."
    hdr = ["Site ref", "Site", "Planning status", "Units", "2030", "2031", "2032", "2033", "2034"]
    sites = [("RG-H01", "Mill Road (former depot)", "Granted, phase 1", 214, [60, 90, 64, 0, 0]),
             ("RG-H02", "Garvan Fields", "Granted", 168, [0, 56, 56, 56, 0]),
             ("RG-H03", "Station Quarter", "Pre-application", 320, [0, 0, 80, 120, 120]),
             ("RG-H04", "Knockane Lane", "Granted, under appeal", 44, [44, 0, 0, 0, 0]),
             ("RG-H05", "Old Creamery", "Zoned", 96, [0, 0, 0, 48, 48])]
    for j, h in enumerate(hdr, 1):
        ws.cell(row=4, column=j, value=h).font = Font(bold=True)
    for i, (ref, nm, st, u, yrs) in enumerate(sites, 5):
        for j, v in enumerate([ref, nm, st, u] + yrs, 1):
            ws.cell(row=i, column=j, value=v)
    ws.column_dimensions["B"].width = 28
    ws.column_dimensions["C"].width = 24
    wb.save(path)
    IO.repack_ooxml(path, "Planning Department", "Planning Department", "2027-10-11T08:30:00Z",
                    "2027-10-14T16:05:00Z", "Rathgarvan residential pipeline", "Kilcarrow City and County Council")


def write_jobs(path):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    doc.add_heading("County Kilcarrow employment outlook to 2030", level=1)
    doc.add_paragraph("Economic Development Unit, September 2027. Jobs by employment area, 2022 (census workplace "
                      "counts) and the 2030 outlook under the regional growth framework's central scenario.")
    t = doc.add_table(rows=1, cols=4)
    t.style = "Light Grid Accent 1"
    for j, h in enumerate(["Employment area", "Jobs 2022", "Jobs 2030 (central)", "Change"]):
        t.rows[0].cells[j].text = h
    data = [("Kilcarrow city centre", 31200, 33400), ("Kilcarrow Docklands", 18900, 23100),
            ("University Hospital campus", 7400, 8100), ("Kilcarrow University", 4100, 4400),
            ("Carrigboy business park", 6800, 8300), ("Port of Kilcarrow, Ringcurran", 3300, 3500),
            ("Ballymurragh retail park", 2600, 2700), ("Airport business park", 2900, 3300)]
    for nm, a, b in data:
        r = t.add_row().cells
        r[0].text, r[1].text, r[2].text = nm, "{:,}".format(a), "{:,}".format(b)
        r[3].text = "%+.1f%%" % (100.0 * (b - a) / a)
    doc.add_paragraph("")
    doc.add_paragraph("The Docklands and Carrigboy figures include the two consented office campuses and the "
                      "biologics plant extension announced in 2026. Figures are rounded to the nearest hundred.")
    doc.core_properties.author = "Economic Development Unit"
    doc.save(path)
    IO.repack_ooxml(path, "Economic Development Unit", "Economic Development Unit", "2027-09-08T10:00:00Z",
                    "2027-09-19T14:22:00Z", "County Kilcarrow employment outlook to 2030",
                    "Kilcarrow City and County Council")


def timetable_rows(rng):
    rows = []
    t = 5 * 60 + 52
    while t <= 23 * 60 + 10:
        peak = (6 * 60 + 40 <= t <= 9 * 60 + 30) or (16 * 60 + 30 <= t <= 19 * 60)
        for direction, off in (("Kilcarrow Central and Carrigboy", 0), ("Ardnagree", 7)):
            tt = t + off
            rows.append(("RGV", "%02d:%02d" % (tt // 60, tt % 60), direction, "4-car", "Mon-Fri"))
        t += 15 if peak else 30
    return rows


def build(target, seed=P.SEED):
    os.makedirs(target, exist_ok=True)
    w = W.build(seed)
    n = {}
    stays, devs = panel_rows(w["devices"])
    n["stays"] = IO.write_csv(os.path.join(target, FILES["stays"]),
                              ["device_id", "cell_id", "stay_start_utc", "stay_end_utc"], stays)
    n["devices"] = IO.write_csv(os.path.join(target, FILES["devices"]),
                                ["device_id", "home_cell", "first_seen_utc", "last_seen_utc"], devs)
    n["cells"] = IO.write_csv(os.path.join(target, FILES["cells"]),
                              ["cell_id", "zone_code", "zone_name", "area_share"], cell_rows())
    write_census(os.path.join(target, FILES["census"]), w["census_final"], w["census_prov"])
    n["census"] = len(w["census_final"]) + len(w["census_prov"])
    write_case(os.path.join(target, FILES["case"]))
    mean, _k = write_review(os.path.join(target, FILES["review"]), w["gates"])
    n["gates"] = IO.write_csv(os.path.join(target, FILES["gates"]), ["date", "location_code", "entries"],
                              [(d.isoformat(), c, v) for d, c, v in w["gates"]])
    n["register"] = IO.write_csv(os.path.join(target, FILES["register"]),
                                 ["station_code", "station_name", "opened", "closed", "notes"],
                                 [(c, nm, o.isoformat(), cl.isoformat() if cl else "",
                                   {"UHK": "Code retired 28 Feb 2023; the station continues as KUH from 1 Mar 2023",
                                    "KUH": "Formerly UHK (same platforms, new code from the 2023 ticketing system)",
                                    "CBH": "Closed 13 Jun 2021; replaced by Carrigboy (CBY), 400 m east",
                                    "CBY": "Replaces Carrigboy Halt (CBH)",
                                    "LSG": "New station"}.get(c, ""))
                                  for c, nm, o, cl, _b, _r, _o in P.STATIONS])
    n["calendar"] = IO.write_csv(os.path.join(target, FILES["calendar"]), ["date", "weekday", "day_type", "name"],
                                 calendar_rows())
    write_panel_note(os.path.join(target, FILES["panel_note"]))
    write_housing(os.path.join(target, FILES["housing"]))
    write_jobs(os.path.join(target, FILES["jobs"]))
    n["timetable"] = IO.write_csv(os.path.join(target, FILES["timetable"]),
                                  ["station_code", "departs", "towards", "train_length", "days"],
                                  timetable_rows(np.random.default_rng(seed + 9)))
    return w, n, mean
