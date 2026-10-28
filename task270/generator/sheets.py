"""task270 workbooks in the pack: the fleet and stations list, the output area lookup, the on-call crew register, the
incident classification codes and the two distractors. Written with openpyxl and repacked by build.normalize."""
from __future__ import annotations

import datetime as dt

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import common as K
import records as R

HEAD_FILL = PatternFill("solid", fgColor="DCE6EE")
BOLD = Font(bold=True)


def _sheet(wb, title, cols, rows, widths=None, first=False, formats=None):
    ws = wb.active if first else wb.create_sheet()
    ws.title = title
    ws.append(cols)
    for c in range(1, len(cols) + 1):
        cell = ws.cell(row=1, column=c)
        cell.font = BOLD
        cell.fill = HEAD_FILL
        cell.alignment = Alignment(vertical="top", wrap_text=True)
    for r in rows:
        ws.append(list(r))
    for i, w in enumerate(widths or [14] * len(cols), start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    if formats:
        for col, fmt in formats.items():
            for row in ws.iter_rows(min_row=2, min_col=col, max_col=col):
                for cell in row:
                    cell.number_format = fmt
    ws.freeze_panes = "A2"
    return ws


def _props(wb, title):
    wb.properties.creator = K.SERVICE
    wb.properties.lastModifiedBy = K.SERVICE
    wb.properties.title = title
    stamp = dt.datetime(2027, 1, 12, 9, 0, 0)
    wb.properties.created = stamp
    wb.properties.modified = stamp


def fleet(Wd, path):
    wb = openpyxl.Workbook()
    st_rows = [(s["code"], s["name"], s["duty"], s["district"], s["e"], s["n"]) for s in Wd.stations]
    st_rows.sort(key=lambda r: r[0])
    _sheet(wb, "Stations", ["Station code", "Station", "Duty system", "District", "Easting", "Northing"], st_rows,
           [12, 18, 12, 14, 10, 10], first=True)
    ap = []
    for e in Wd.engines:
        s = Wd.stations[e["station"]]
        ap.append((e["call_sign"], e["registration"], s["code"], "Rescue pump", e["crew"]))
    ap.sort(key=lambda r: r[0])
    _sheet(wb, "Appliances", ["Call sign", "Registration", "Station code", "Appliance type", "Crewed by"], ap,
           [10, 12, 12, 14, 12])
    _props(wb, "Fleet and stations 2026")
    wb.save(path)


def oa_lookup(Wd, path):
    wb = openpyxl.Workbook()
    rows = [(Wd.oa21[k], K.LAD_CODE[K.DISTRICTS[Wd.oa_district[k]]], K.DISTRICTS[Wd.oa_district[k]])
            for k in range(Wd.n_oa)]
    rows.sort()
    _sheet(wb, "OA21 to LAD", ["OA21CD", "LAD22CD", "LAD22NM"], rows, [12, 12, 14], first=True)
    pairs = {}
    for k in range(Wd.n_oa):
        pairs.setdefault(Wd.oa11[k], []).append(Wd.oa21[k])
    rows = []
    for o11, lst in pairs.items():
        for o21 in lst:
            rows.append((o11, o21, "S" if len(lst) > 1 else "U"))
    rows.sort()
    _sheet(wb, "OA11 to OA21", ["OA11CD", "OA21CD", "CHGIND"], rows, [12, 12, 8])
    _props(wb, "Output area lookup")
    wb.save(path)


def crew_register(Wd, sim, path):
    crew, changes = R.crew_rows(Wd, sim)
    wb = openpyxl.Workbook()
    _sheet(wb, "Crew", ["Staff number", "Station code", "Role", "BA wearer", "LGV driver since"], crew,
           [12, 12, 16, 10, 16], first=True)
    _sheet(wb, "Role changes", ["Staff number", "Station code", "New role", "Effective from"], changes,
           [12, 12, 16, 14])
    _props(wb, "On-call crew register 2026")
    wb.save(path)


def codes(path):
    wb = openpyxl.Workbook()
    old = [("F01", "Accidental dwelling fire"), ("F02", "Deliberate dwelling fire"),
           ("F07", "Dwelling fire, motive not determined"), ("F03", "Fire in other building"),
           ("F04", "Road vehicle fire"), ("F05", "Secondary fire"), ("F06", "Chimney fire"),
           ("A01", "False alarm, apparatus"), ("A02", "False alarm, good intent"), ("A03", "False alarm, malicious"),
           ("S01", "Road traffic collision"), ("S02", "Other special service")]
    new = [("PFD", "Primary fire, dwelling"), ("PFO", "Primary fire, other building"),
           ("PFV", "Primary fire, road vehicle"), ("SEC", "Secondary fire"), ("CHM", "Chimney fire"),
           ("FAA", "False alarm, apparatus"), ("FAG", "False alarm, good intent"), ("FAM", "False alarm, malicious"),
           ("RTC", "Road traffic collision"), ("SSO", "Other special service")]
    _sheet(wb, "Codes to 31 Mar 2024", ["Code", "Description"], old, [8, 40], first=True)
    _sheet(wb, "Codes from 1 Apr 2024", ["Code", "Description"], new, [8, 40])
    xw = [("F01", "PFD", "Accidental"), ("F02", "PFD", "Deliberate"), ("F07", "PFD", "Not known"),
          ("F03", "PFO", ""), ("F04", "PFV", ""), ("F05", "SEC", ""), ("F06", "CHM", ""), ("A01", "FAA", ""),
          ("A02", "FAG", ""), ("A03", "FAM", ""), ("S01", "RTC", ""), ("S02", "SSO", "")]
    _sheet(wb, "Mapping", ["Code to 31 Mar 2024", "Code from 1 Apr 2024", "Cause"], xw, [20, 20, 12])
    _props(wb, "Incident classification codes")
    wb.save(path)


def population(Wd, path):
    r = K.rng("population")
    res = Wd.akind == "R"
    homes = np.bincount(Wd.aoa[res], minlength=Wd.n_oa)
    rows = []
    sizes, share = np.arange(1, 7), np.array([0.30, 0.34, 0.15, 0.13, 0.06, 0.02])
    for k in range(Wd.n_oa):
        # usual residents: the households in the occupied homes, and residents of a care home or hostel where there is one
        occupied = int(round(homes[k] * r.uniform(0.90, 0.985)))
        pp = int(r.choice(sizes, occupied, p=share).sum())
        if r.random() < 0.05:
            pp += int(r.integers(18, 71))
        rows.append((Wd.oa21[k], K.DISTRICTS[Wd.oa_district[k]], pp))
    rows.sort()
    wb = openpyxl.Workbook()
    _sheet(wb, "Mid-2025", ["OA21CD", "LAD22NM", "All persons"], rows, [12, 14, 12], first=True)
    _props(wb, "Population estimates mid-2025")
    wb.save(path)


def establishment(Wd, sim, path):
    code = {i: s["code"] for i, s in enumerate(Wd.stations)}
    n_oc = {}
    for p in sim["staff"]:
        n_oc[code[p.station]] = n_oc.get(code[p.station], 0) + 1
    rows = []
    for s in sorted(Wd.stations, key=lambda s: s["code"]):
        re_ = K.rng("estab", s["code"])
        if s["duty"] == "Wholetime":
            est = int(re_.choice([24, 26, 28, 28, 30])) * s["engines"]
            rows.append((s["code"], s["name"], "Wholetime", est, est - int(re_.integers(-1, 4))))
        else:
            est = int(re_.choice([10, 11, 12, 12, 12, 13, 14, 15]))
            rows.append((s["code"], s["name"], "On-call", est, n_oc.get(s["code"], 0)))
    wb = openpyxl.Workbook()
    _sheet(wb, "Establishment", ["Station code", "Station", "Duty system", "Establishment", "In post 1 Jan 2026"], rows,
           [12, 18, 12, 14, 16], first=True)
    _props(wb, "Station establishment 2026")
    wb.save(path)
