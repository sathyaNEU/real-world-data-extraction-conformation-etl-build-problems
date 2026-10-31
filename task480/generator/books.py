"""The pack's workbooks: the Center's census history by municipality, its 2026 group quarters survey, and the
Department of Transportation's certified local road miles."""
import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font

import pack as P
import sim as S
import world as W

FIPS = dict((m[1], m[0]) for m in W.MUNIS)
FIPS[W.IVY_TOWN[1]] = W.IVY_TOWN[0]


def _title(ws, a1, a2):
    ws["A1"] = a1
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = a2
    ws["A2"].font = Font(size=9, italic=True)


def write_history(path):
    h = P.history()
    wb = openpyxl.Workbook()
    first = True
    src = {2000: "Census 2000 Summary File 1 (100-percent data), tables P1, P27, H1 and H3",
           2010: "2010 Census Summary File 1, tables P1, P16, P42, H1 and H3",
           2020: "2020 Census Demographic and Housing Characteristics File, tables P1, P15, P18 and H1"}
    for y in (2000, 2010, 2020):
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = str(y)
        _title(ws, "%s: decennial census counts by municipality, %d" % (W.COUNTY, y),
               "Municipalities as they stood on 1 April %d. Source: U.S. Census Bureau, %s." % (y, src[y]))
        hdr = ["FIPS code", "Municipality", "Total population", "Household population", "Group quarters population",
               "Housing units", "Occupied housing units"]
        for j, v in enumerate(hdr, 1):
            c = ws.cell(row=4, column=j, value=v)
            c.font = Font(bold=True)
            c.alignment = Alignment(wrap_text=True, vertical="bottom")
        names = sorted(h[y], key=lambda m: (m.split(" ")[0] != "City", m.split(" ")[0] != "Village", m))
        r = 5
        tot = [0] * 5
        for m in names:
            vals = h[y][m]
            ws.cell(row=r, column=1, value=FIPS[m])
            ws.cell(row=r, column=2, value=m)
            for j, v in enumerate(vals, 3):
                ws.cell(row=r, column=j, value=int(v)).number_format = "#,##0"
                tot[j - 3] += int(v)
            r += 1
        ws.cell(row=r, column=2, value="%s total" % W.COUNTY).font = Font(bold=True)
        for j, v in enumerate(tot, 3):
            c = ws.cell(row=r, column=j, value=v)
            c.number_format = "#,##0"
            c.font = Font(bold=True)
        for col, wdt in zip("ABCDEFG", [11, 24, 12, 13, 13, 11, 13]):
            ws.column_dimensions[col].width = wdt
        ws.freeze_panes = "A5"
    wb.save(path)


def write_gq(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Survey 2026"
    _title(ws, "%s: Annual Survey of Group Quarters, 2026" % W.CENTER,
           "Reference date 1 April 2026. %s; facilities in %s." % (W.OFFICE, W.COUNTY))
    hdr = ["Facility", "Address", "Municipality", "Group quarters type", "Licensed beds", "Residents, 1 April 2026",
           "Form returned"]
    for j, v in enumerate(hdr, 1):
        c = ws.cell(row=4, column=j, value=v)
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="bottom")
    r = np.random.default_rng(W.SEED + 91)
    row = 5
    for f, t, m, e, v in S.gq_on(W.EST):
        b = P.facility_building(f)
        beds = int(v * r.uniform(1.04, 1.22)) + (0 if t != "College residence hall" else int(v * 0.05))
        for j, val in enumerate([f, "%d %s %s" % (b["number"] + 1, b["street"][0].title(), b["street"][1].title()), m, t, beds, v,
                                 "2026-%02d-%02d" % (4 + int(r.integers(0, 2)), 1 + int(r.integers(0, 27)))], 1):
            ws.cell(row=row, column=j, value=val)
        row += 1
    for col, wdt in zip("ABCDEFG", [40, 28, 20, 30, 10, 12, 12]):
        ws.column_dimensions[col].width = wdt
    ws.freeze_panes = "A5"
    wb.save(path)


def write_roads(path):
    """road miles under each municipality's jurisdiction as certified for the 2027 aid year (a formula factor the
    Department certifies on its own)"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Certified miles"
    _title(ws, "%s: certified local road mileage for the 2027 aid year" % W.DOT,
           "Miles of public road under municipal jurisdiction on 1 January 2026, by surface; %s." % W.COUNTY)
    hdr = ["Municipality", "Paved miles", "Gravel miles", "Total miles", "Certified"]
    for j, v in enumerate(hdr, 1):
        ws.cell(row=4, column=j, value=v).font = Font(bold=True)
    r = np.random.default_rng(W.SEED + 93)
    row = 5
    for code, name, kind, eras in W.MUNIS:
        base = {"city": 58, "village": 21, "town": 64}[kind] * r.uniform(0.75, 1.3)
        paved = round(base * (0.97 if kind != "town" else r.uniform(0.55, 0.85)), 2)
        gravel = round(base - paved, 2) if kind == "town" else 0.0
        for j, val in enumerate([name, paved, gravel, round(paved + gravel, 2),
                                 "2026-03-%02d" % (2 + int(r.integers(0, 26)))], 1):
            c = ws.cell(row=row, column=j, value=val)
            if j in (2, 3, 4):
                c.number_format = "0.00"
        row += 1
    for col, wdt in zip("ABCDE", [24, 12, 12, 12, 12]):
        ws.column_dimensions[col].width = wdt
    wb.save(path)
