"""The pack's data files, written from the world, and the bundle read back from them. Every figure calc.py and
asks.py compute comes from the bundle, so it is the shipped files' arithmetic.

    files written here: the Office's real-time database, annual national accounts and price indexes; TBS's portal
    pull and bulk download with their code lists; the Harbours Board's loadings; the desk's tracker and data folder
    index; the Harbourline poll and the Industry Federation's survey (the two distractors).
    docs.py writes the user guide, the notice and TBS's June bulletin."""
from __future__ import annotations

import csv
import datetime as dt
import io
import json
import math
import os

import numpy as np

import common as K
import national as NA
import partners as PT
import tracker as TR
import world as WD

F_DB = "so_realtime_gdp_database.csv"
F_ANNUAL = "so_annual_national_accounts_2025.xlsx"
F_PRICES = "so_price_indexes_2026-06.xlsx"
F_GUIDE = "so_gdp_user_guide_2026.pdf"
F_NOTICE = "so_notice_gdp_advance_2026-07-24.txt"
F_BULLETIN = "tbs_merchandise_trade_business_stocks_2026-06.pdf"
F_PORTAL = "tbs_portal_monthly_2019-01_2026-05.csv"
F_BULK = "tbs_trade_partner_sitc2_monthly_2023-01_2026-05.csv"
F_COUNTRIES = "tbs_country_codes.csv"
F_SITC = "tbs_sitc_rev4_divisions.csv"
F_PORTS = "harbours_board_bulk_loadings_2022-12_2026-06.csv"
F_TRACKER = "tarbert_gdp_tracker_2026q2.xlsx"
F_POLL = "harbourline_gdp_poll_2026-07-23.json"
F_SURVEY = "industry_federation_business_conditions_2026-06.csv"
F_INDEX = "tarbert_econ_data_index.csv"
DISTRACTORS = [F_POLL, F_SURVEY]

MONTHS = WD.MONTHS
MI = WD.MI
ESTIMATE = {"advance": "Advance", "second": "Second", "third": "Third", "annual": "Annual update"}
LAYOUT_CHANGE = "2024-U"       # the July 2024 annual update split business investment into three series
OLD_SERIES = ["GDP", "HFCE", "GFCE", "GFCF_DW", "GFCF_BUS", "GFCF_PUB", "CIPI_NF", "CIPI_FO", "X_G", "X_S", "M_G", "M_S"]
NEW_SERIES = ["GDP", "HFCE", "GFCE", "GFCF_DW", "GFCF_ME", "GFCF_NDC", "GFCF_IPP", "GFCF_PUB", "CIPI_NF", "CIPI_FO",
              "X_G", "X_S", "M_G", "M_S"]
PARTS = ["HFCE", "GFCE", "GFCF_DW", "GFCF_ME", "GFCF_NDC", "GFCF_IPP", "GFCF_PUB", "CIPI_NF", "CIPI_FO", "X_G", "X_S",
         "M_G", "M_S"]
SECTION_TITLE = dict(K.SITC)
BULLETIN_MONTHS = ["2026-03", "2026-04", "2026-05", "2026-06"]


def fmt1(x):
    return "%.1f" % x


# ---------------------------------------------------------------------------------------------------- national accounts
def ref_factor(W, R, c):
    """A component's level at year R's average prices relative to 2025's: its deflator's year-R mean."""
    d = W.DEFL[c]
    return float(np.mean([d[NA.QI[q]] for q in NA.QUARTERS if int(q[:4]) == R]))


def release_levels(W, rel, measure):
    """{series: {quarter: $m}} for one release, chain volume at its reference year's prices or current prices,
    whole dollars of millions; GDP the sum of its components in both."""
    est = W.EST[rel["id"]]
    k1 = NA.QI[rel["quarter"]]
    out = {}
    for c in PARTS:
        vals = {}
        for k in range(k1 + 1):
            v = est[c][k]
            if measure == "cvm":
                v = v * ref_factor(W, rel["ref"], c)
            else:
                v = v * W.DEFL[c][k]
            vals[NA.QUARTERS[k]] = v
        out[c] = vals
    out["GFCF_BUS"] = {q: out["GFCF_ME"][q] + out["GFCF_NDC"][q] + out["GFCF_IPP"][q] for q in out["HFCE"]}
    out["GDP"] = {q: sum(NA.SIGN[c] * out[c][q] for c in PARTS) for q in out["HFCE"]}
    return {c: {q: int(round(v)) for q, v in s.items()} for c, s in out.items()}


def db_rows(W):
    rows = []
    after = False
    for rel in W.RELEASES:
        if rel["id"] == "2026-U":
            continue
        if rel["id"] == LAYOUT_CHANGE:
            after = True
        series = NEW_SERIES if after else OLD_SERIES
        for measure, basis in (("cvm", "Chain volume, %d prices" % rel["ref"]), ("cp", "Current prices")):
            lv = release_levels(W, rel, measure)
            for q in lv["GDP"]:
                for c in series:
                    rows.append([rel["id"], rel["date"].isoformat(), ESTIMATE[rel["type"]], basis, q, c,
                                 NA.TITLES[c], lv[c][q]])
    return rows


DB_COLS = ["release_id", "release_date", "estimate", "price_basis", "quarter", "series_id", "series", "value_m"]


def latest_levels(W, measure):
    rel = [r for r in W.RELEASES if r["id"] == "2026-U"][0]
    return release_levels(W, rel, measure)


# ---------------------------------------------------------------------------------------------------- workbooks
def _wb():
    import openpyxl
    return openpyxl.Workbook()


def _font(bold=False, size=None, italic=False):
    from openpyxl.styles import Font
    kw = {"bold": bold, "italic": italic}
    if size:
        kw["size"] = size
    return Font(**kw)


def _fill(hex_):
    from openpyxl.styles import PatternFill
    return PatternFill("solid", fgColor=hex_)


def _set(ws, r, c, v, fmt=None, bold=False, fill=None, align=None, wrap=False):
    from openpyxl.styles import Alignment
    cell = ws.cell(row=r, column=c, value=v)
    if fmt:
        cell.number_format = fmt
    if bold:
        cell.font = _font(True)
    if fill:
        cell.fill = _fill(fill)
    if align or wrap:
        cell.alignment = Alignment(horizontal=align, wrap_text=wrap, vertical="bottom")
    return cell


def write_annual(path, W):
    from openpyxl.utils import get_column_letter
    wb = _wb()
    ws = wb.active
    ws.title = "Contents"
    ws["A1"] = "Annual national accounts 2025"
    ws["A1"].font = _font(True, 13)
    ws["A2"] = "Statistics Office. Released 21 July 2026, 10:45."
    _set(ws, 4, 1, "Table", bold=True)
    _set(ws, 4, 2, "Title", bold=True)
    tables = [("Table 1", "Expenditure on GDP, annual, chain volume measures, 2025 prices"),
              ("Table 2", "Expenditure on GDP, annual, current prices"),
              ("Table 3", "Expenditure on GDP, quarterly, chain volume measures, 2025 prices, seasonally adjusted"),
              ("Table 4", "Expenditure on GDP, quarterly, current prices, seasonally adjusted")]
    for i, (t, title) in enumerate(tables):
        ws.cell(row=5 + i, column=1, value=t)
        ws.cell(row=5 + i, column=2, value=title)
    notes = ["The annual estimates for 2023, 2024 and 2025 incorporate the annual enterprise and household surveys "
             "and the government's audited accounts for those years.",
             "The quarterly series from the June quarter 2023 are revised to the annual estimates and their seasonal "
             "factors re-estimated. Goods trade and non-farm business inventories, which come from Trade and Business "
             "Statistics' monthly data, are unchanged.",
             "Chain volume measures are at the average prices of 2025. The quarterly series are seasonally adjusted; "
             "annual figures are calendar-year sums of the original series.",
             "Business investment is shown as machinery and equipment, non-dwelling construction and intellectual "
             "property products.",
             "Enquiries: national accounts, Statistics Office."]
    for i, n in enumerate(notes):
        ws.cell(row=11 + i, column=1, value=n)
    ws.column_dimensions["A"].width = 10
    ws.column_dimensions["B"].width = 92
    heads = [("HFCE", "Household final consumption expenditure"), ("GFCE", "General government final consumption"),
             ("GFCF_DW", "Dwellings"), ("GFCF_ME", "Machinery and equipment"),
             ("GFCF_NDC", "Non-dwelling construction"), ("GFCF_IPP", "Intellectual property products"),
             ("GFCF_PUB", "General government investment"), ("CIPI_NF", "Changes in inventories: non-farm business"),
             ("CIPI_FO", "Changes in inventories: farm and other"), ("X_G", "Exports of goods"),
             ("X_S", "Exports of services"), ("M_G", "Imports of goods"), ("M_S", "Imports of services"),
             ("GDP", "Gross domestic product")]
    cvm, cp = latest_levels(W, "cvm"), latest_levels(W, "cp")
    for tname, title, lv, annual in (("Table 1", tables[0][1], cvm, True), ("Table 2", tables[1][1], cp, True),
                                     ("Table 3", tables[2][1], cvm, False), ("Table 4", tables[3][1], cp, False)):
        ws = wb.create_sheet(tname)
        ws["A1"] = title
        ws["A1"].font = _font(True, 12)
        ws["A2"] = "$ million" + ("" if annual else "; quarters end in March, June, September and December")
        _set(ws, 4, 1, "Year" if annual else "Quarter", bold=True, fill="DCE6EA")
        for j, (code, h) in enumerate(heads, 2):
            _set(ws, 4, j, h, bold=True, fill="DCE6EA", align="right", wrap=True)
        r = 5
        if annual:
            periods = [str(y) for y in range(2018, 2026)]
        else:
            periods = list(lv["GDP"].keys())
        for p in periods:
            ws.cell(row=r, column=1, value=p if annual else p[:4] + " Q" + p[-1])
            for j, (code, h) in enumerate(heads, 2):
                if annual:
                    v = sum(lv[code][q] for q in lv[code] if q.startswith(p))
                else:
                    v = lv[code][p]
                _set(ws, r, j, v, fmt="#,##0")
            r += 1
        ws.column_dimensions["A"].width = 10
        for j in range(2, len(heads) + 2):
            ws.column_dimensions[get_column_letter(j)].width = 13
        ws.row_dimensions[4].height = 44
        ws.freeze_panes = "B5"
    wb.save(path)


PRICE_SHEETS = [("PPI inputs", "Producer price indexes, inputs to the industry", "pin"),
                ("PPI outputs", "Producer price indexes, outputs of the industry", "pout"),
                ("Export prices", "Export price indexes by SITC section", "px"),
                ("Import prices", "Import price indexes by SITC section", "pm")]


def price_tables(W):
    months = K.month_list(K.PRICE0, K.LAST)
    ind = [(c, n) for c, n, *_ in K.INDUSTRIES]
    sec = [(s, "%s %s" % (s, n)) for s, n in K.SITC]
    return months, {
        "pin": (ind, {c: {m: float(W.PUB_P[c][MI[m]]) for m in months} for c, _ in ind}),
        "pout": (ind, {c: {m: float(W.PUB_POUT[c][MI[m]]) for m in months} for c, _ in ind}),
        "px": (sec, {s: {m: float(W.PUB_PX[s][MI[m]]) for m in months} for s, _ in sec}),
        "pm": (sec, {s: {m: float(W.PUB_PM[s][MI[m]]) for m in months} for s, _ in sec}),
    }


def write_prices(path, W):
    from openpyxl.utils import get_column_letter
    months, tabs = price_tables(W)
    wb = _wb()
    ws = wb.active
    ws.title = "Contents"
    ws["A1"] = "Price indexes, June 2026"
    ws["A1"].font = _font(True, 13)
    ws["A2"] = "Statistics Office. Released 16 July 2026, 10:45."
    for i, (sheet, title, _) in enumerate(PRICE_SHEETS):
        ws.cell(row=4 + i, column=1, value=sheet)
        ws.cell(row=4 + i, column=2, value=title)
    notes = ["All indexes: base 2019 (average of the twelve months) = 100. Monthly indexes measure the average price "
             "in the month. Not seasonally adjusted.",
             "Producer price indexes, inputs: the prices businesses in the industry pay for the goods they buy, "
             "including goods bought for resale. Outputs: the prices they receive for what they sell.",
             "Export price indexes are free on board; import price indexes are at the value for duty. Both are in "
             "local currency.",
             "The industries are those of Trade and Business Statistics' monthly survey of business stocks."]
    for i, n in enumerate(notes):
        ws.cell(row=9 + i, column=1, value=n)
    ws.column_dimensions["A"].width = 16
    ws.column_dimensions["B"].width = 60
    for sheet, title, key in PRICE_SHEETS:
        cols, data = tabs[key]
        ws = wb.create_sheet(sheet)
        ws["A1"] = title + ", 2019 = 100"
        ws["A1"].font = _font(True, 12)
        _set(ws, 3, 1, "Month", bold=True, fill="DCE6EA")
        for j, (code, name) in enumerate(cols, 2):
            _set(ws, 3, j, code if key in ("pin", "pout") else code, bold=True, fill="DCE6EA", align="right")
            _set(ws, 4, j, name, align="right", wrap=True)
        ws.row_dimensions[4].height = 58
        for i, m in enumerate(months):
            c = ws.cell(row=5 + i, column=1, value=dt.date(int(m[:4]), int(m[5:]), 1))
            c.number_format = "mmm yyyy"
            for j, (code, name) in enumerate(cols, 2):
                _set(ws, 5 + i, j, data[code][m], fmt="0.0")
        ws.column_dimensions["A"].width = 11
        for j in range(2, len(cols) + 2):
            ws.column_dimensions[get_column_letter(j)].width = 13
        ws.freeze_panes = "B5"
    wb.save(path)


# ---------------------------------------------------------------------------------------------------- TBS
PORTAL_MONTHS = K.month_list("2019-01", "2026-05")


def portal_rows(W):
    rows = []
    for c, name, *_ in K.INDUSTRIES:
        for kind, title, unit, src in (("STK", "Stocks, book value at end of month", "$m", W.PORTAL_B),
                                       ("COS", "Cost of sales", "$m", W.PORTAL_S)):
            for m in PORTAL_MONTHS:
                rows.append(["TBS.%s.%s.SA" % (kind, c), "%s: %s" % (title, name), unit, "Seasonally adjusted", m,
                             fmt1(src[c][MI[m]])])
        for m in PORTAL_MONTHS:
            rows.append(["TBS.RAT.%s" % c, "Stock-to-sales ratio: %s" % name, "months", "Seasonally adjusted", m,
                         "%.2f" % W.T[c][MI[m]]])
    for flow, title, sa_src, orig in (("EXP", "Exports", W.PORTAL_VX, "ORIG_X"), ("IMP", "Imports", W.PORTAL_VM, "ORIG_M")):
        for s, sname in K.SITC:
            for m in PORTAL_MONTHS:
                rows.append(["TBS.%s.S%s.SA" % (flow, s), "%s: %s %s" % (title, s, sname), "$m", "Seasonally adjusted",
                             m, fmt1(sa_src[s][MI[m]])])
            for m in PORTAL_MONTHS:
                v = W.PORTAL_ORIG[flow][s][MI[m]]
                rows.append(["TBS.%s.S%s.OR" % (flow, s), "%s: %s %s" % (title, s, sname), "$m", "Original", m,
                             fmt1(v)])
    return rows


PORTAL_COLS = ["series_id", "series", "unit", "adjustment", "month", "value"]


def original_terms(W):
    """TBS's original-terms section totals by month ($m one decimal): the bulk download's sums for 2023 on, the
    seasonally adjusted values with the seasonal factors before; SITC 3 exports have no seasonal pattern."""
    out = {"EXP": {}, "IMP": {}}
    for flow, sa, bulk_tot in (("EXP", W.PUB_VX, W.ORIG_X), ("IMP", W.PUB_VM, W.ORIG_M)):
        for s in K.SITC_CODES:
            v = np.array([round(sa[s][m] * PT.season(s, m), 1) for m in range(WD.NM)])
            if s in bulk_tot:
                for m in range(MI[PT.FIRST], MI[PT.LAST_PULL] + 1):
                    v[m] = round(bulk_tot[s][m], 1)
            if flow == "EXP" and s == "3":
                v = sa[s].copy()
            out[flow][s] = v
    # the bulk download (24 June) holds April and May as they then stood; the June bulletin revised them
    W.PORTAL_ORIG = {f: {s: v.copy() for s, v in d.items()} for f, d in out.items()}
    for f, src, pub in (("EXP", W.PORTAL_VX, W.PUB_VX), ("IMP", W.PORTAL_VM, W.PUB_VM)):
        for s in K.SITC_CODES:
            for m in (MI["2026-04"], MI["2026-05"]):
                if src[s][m]:
                    out[f][s][m] = round(W.PORTAL_ORIG[f][s][m] * pub[s][m] / src[s][m], 1)
    W.TBS_ORIG = out


def bulk_rows(W):
    rows = []
    for (m, flow, c, d), (v, q, u) in sorted(W.BULK.items()):
        rows.append([m, "Exports" if flow == "X" else "Imports", c, d, v, "" if q is None else q, u or ""])
    return rows


BULK_COLS = ["month", "flow", "country", "sitc_division", "value_000", "quantity", "quantity_unit"]


def country_rows():
    return [[c, n, r] for c, n, r in PT.COUNTRIES + PT.SPECIAL]


def sitc_rows():
    return [[d, t, d[0], SECTION_TITLE[d[0]]] for d, t in PT.DIVISIONS]


def port_rows(W):
    rows = []
    r = K.rng("ports", "vessels")
    for (m, cargo, port), t in sorted(W.PORTS.items()):
        size = {"Coal": 88000.0, "LNG": 70000.0, "Condensate": 42000.0}[cargo]
        vessels = int(round(t / size + r.normal(0.0, 0.6))) if cargo != "LNG" else int(round(t / size))
        rows.append([m, port, cargo, int(round(t)), max(vessels, 1)])
    return rows


PORT_COLS = ["month", "port", "cargo", "tonnes_loaded", "vessels"]


# ---------------------------------------------------------------------------------------------------- the bulletin's tables
def bulletin_tables(W):
    """TBS's June bulletin, as numbers: trade by section (seasonally adjusted, March to June), totals in original
    terms, coal and LNG by destination for June, stocks, cost of sales and ratios by industry (March to June), and
    the revisions to April and May."""
    T = {}
    T["exp"] = {s: {m: float(W.PUB_VX[s][MI[m]]) for m in BULLETIN_MONTHS} for s in K.SITC_CODES}
    T["imp"] = {s: {m: float(W.PUB_VM[s][MI[m]]) for m in BULLETIN_MONTHS} for s in K.SITC_CODES}
    T["orig"] = {f: {m: round(float(sum(W.TBS_ORIG[f][s][MI[m]] for s in K.SITC_CODES)), 1) for m in BULLETIN_MONTHS}
                 for f in ("EXP", "IMP")}
    mj = MI["2026-06"]
    T["energy"] = {c: {k: (round(float(W.SHIP_V[k][c][mj]), 1) if c in W.SHIP_V[k] else 0.0,
                           round(float(W.SHIP_T[k][c][mj]) / 1000.0, 1) if c in W.SHIP_T[k] else 0.0)
                       for k in ("32", "34")} for c in sorted(set(PT.COAL_MKT) | set(PT.LNG_MKT))}
    T["stocks"] = {c: {m: float(W.PUB_B[c][MI[m]]) for m in BULLETIN_MONTHS} for c in K.IND_CODES}
    T["sales"] = {c: {m: float(W.PUB_S[c][MI[m]]) for m in BULLETIN_MONTHS} for c in K.IND_CODES}
    T["ratio"] = {c: {m: float(W.T[c][MI[m]]) for m in BULLETIN_MONTHS} for c in K.IND_CODES}
    rev = {}
    for m in ("2026-04", "2026-05"):
        k = MI[m]
        rev[m] = {"exports": (round(float(sum(W.PORTAL_VX[s][k] for s in K.SITC_CODES)), 1),
                              round(float(sum(W.PUB_VX[s][k] for s in K.SITC_CODES)), 1)),
                  "imports": (round(float(sum(W.PORTAL_VM[s][k] for s in K.SITC_CODES)), 1),
                              round(float(sum(W.PUB_VM[s][k] for s in K.SITC_CODES)), 1)),
                  "stocks": (round(float(sum(W.PORTAL_B[c][k] for c in K.IND_CODES)), 1),
                             round(float(sum(W.PUB_B[c][k] for c in K.IND_CODES)), 1))}
    T["revisions"] = rev
    return T


# ---------------------------------------------------------------------------------------------------- the tracker
def tracker_base(W):
    lv = latest_levels(W, "cvm")
    base = {c: lv[c]["2026Q1"] for c in PARTS}
    base["GDP"] = lv["GDP"]["2026Q1"]
    return base


def write_tracker(path, W, base, est):
    wb = _wb()
    ws = wb.active
    ws.title = "Tracker"
    ws["A1"] = "Tarbert Economics: GDP tracker, June quarter 2026"
    ws["A1"].font = _font(True, 13)
    ws["A2"] = "As at 08:00 Tuesday 28 July 2026. $ million at 2025 prices, seasonally adjusted."
    ws["A3"] = "Lines fed by the TBS June bulletin are open until it is out."
    head = ["Line", "SO series", "Mar qtr 2026", "Jun qtr 2026 (track)", "Change", "Contribution (ppts)", "Source",
            "Updated"]
    for j, h in enumerate(head, 1):
        _set(ws, 5, j, h, bold=True, fill="E2E8D9", align="left" if j in (1, 2, 7, 8) else "right", wrap=True)
    updated = {"HFCE": "15 Jul", "GFCE": "20 Jul", "GFCF_DW": "10 Jul", "GFCF_ME": "21 Jul", "GFCF_NDC": "21 Jul",
               "GFCF_IPP": "1 Jul", "GFCF_PUB": "20 Jul", "CIPI_FO": "17 Jul", "X_S": "16 Jul", "M_S": "16 Jul",
               "X_G": "", "M_G": "", "CIPI_NF": ""}
    r = 6
    gdp1 = base["GDP"]
    for label, code, g, src in TR.LINES:
        ws.cell(row=r, column=1, value=label)
        ws.cell(row=r, column=2, value=code)
        _set(ws, r, 3, base[code], fmt="#,##0")
        if code in est:
            _set(ws, r, 4, est[code], fmt="#,##0")
            _set(ws, r, 5, est[code] - base[code], fmt="#,##0;-#,##0")
            sgn = -1.0 if code == "M_S" else 1.0
            _set(ws, r, 6, sgn * (est[code] - base[code]) / gdp1 * 100.0, fmt="0.00;-0.00")
        else:
            ws.cell(row=r, column=4, value="awaiting TBS")
        ws.cell(row=r, column=7, value=src)
        ws.cell(row=r, column=8, value=updated[code])
        r += 1
    _set(ws, r, 1, "Gross domestic product", bold=True)
    ws.cell(row=r, column=2, value="GDP")
    _set(ws, r, 3, gdp1, fmt="#,##0", bold=True)
    widths = [30, 10, 13, 15, 10, 13, 74, 9]
    from openpyxl.utils import get_column_letter
    for j, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.row_dimensions[5].height = 30
    ws.freeze_panes = "C6"
    ws2 = wb.create_sheet("Notes")
    notes = ["Base: the Statistics Office's latest estimates of the March quarter 2026.",
             "Track: each line's June-quarter level from the source shown; services lines in 2025 prices from the "
             "Office's travel and transport indicators.",
             "Contributions are the change over March-quarter GDP, in percentage points of quarterly growth.",
             "Imports of services enter with a negative sign.",
             "Kept by Jodie Ford (economics data). Lines are updated as sources are released."]
    for i, n in enumerate(notes, 1):
        ws2.cell(row=i, column=1, value=n)
    ws2.column_dimensions["A"].width = 110
    wb.save(path)


# ---------------------------------------------------------------------------------------------------- distractors
POLL = [2.3, 2.6, 2.1, 2.9, 2.4, 1.9, 2.7, 2.4, 2.2, 3.2, 2.5, 2.0, 2.6, 3.0, 1.6, 2.3, 3.4]


def poll_doc():
    vals = sorted(POLL)
    med = vals[len(vals) // 2]
    return {
        "poll": "Harbourline economists' poll: GDP, June quarter 2026",
        "release_forecast": "Statistics Office advance estimate, 30 July 2026",
        "closed": "2026-07-23T17:00:00+12:00",
        "measure": "real GDP, June quarter 2026 on March quarter 2026, per cent at a compound annual rate",
        "compiled_by": "Josh Dean, Harbourline",
        "attribution": "Forecasts are not attributed to their contributors.",
        "forecasts": POLL,
        "summary": {"responses": len(POLL), "median": med, "low": vals[0], "high": vals[-1]},
    }


def survey_rows():
    r = K.rng("survey")
    rows = []
    months = K.month_list("2025-01", "2026-06")
    base = {"Activity": 51.5, "New orders": 51.0, "Employment": 50.6, "Stocks": 49.8, "Prices paid": 57.0,
            "Selling prices": 53.0}
    for sector in ("Manufacturing", "Services", "Construction"):
        for i, m in enumerate(months):
            for ind, b in base.items():
                v = b + r.normal(0.0, 1.1)
                if m >= "2026-03" and ind == "Prices paid":
                    v += 4.0 if m < "2026-06" else 9.0
                if m >= "2026-04" and ind == "Stocks":
                    v -= 2.5 if m < "2026-06" else 4.5
                if m >= "2026-06" and ind in ("Activity", "New orders"):
                    v -= 2.2
                rows.append([m, sector, ind, "%.1f" % v])
    return rows


SURVEY_COLS = ["month", "sector", "indicator", "index"]


def index_rows():
    return [
        [F_GUIDE, "Statistics Office", "Quarterly national accounts: user guide (2026 edition)", "", "2026-04-30",
         "saved from the Office's website", "Statistics Office terms of reuse"],
        [F_NOTICE, "Statistics Office", "Notice: advance estimate of GDP, June quarter 2026", "", "2026-07-24",
         "media release", "Statistics Office terms of reuse"],
        [F_DB, "Statistics Office", "Real-time database of quarterly GDP estimates", "releases from 25 April 2019",
         "2026-06-26", "downloaded after each quarterly release", "Statistics Office terms of reuse"],
        [F_ANNUAL, "Statistics Office", "Annual national accounts 2025", "2018 to 2025; quarters to March 2026",
         "2026-07-21", "saved on release", "Statistics Office terms of reuse"],
        [F_PRICES, "Statistics Office", "Price indexes, June 2026", "January 2018 to June 2026", "2026-07-16",
         "saved on release", "Statistics Office terms of reuse"],
        [F_BULLETIN, "Trade and Business Statistics", "Merchandise trade and business stocks, June 2026", "June 2026",
         "2026-07-28", "PDF issued while the TBS portal is down", "TBS terms of reuse"],
        [F_PORTAL, "Trade and Business Statistics", "Portal monthly series pull", "January 2019 to May 2026",
         "2026-06-24", "monthly pull after the bulletin", "TBS terms of reuse"],
        [F_BULK, "Trade and Business Statistics", "Bulk download: trade by country and SITC division",
         "January 2023 to May 2026", "2026-06-24", "monthly pull after the bulletin", "TBS terms of reuse"],
        [F_COUNTRIES, "Trade and Business Statistics", "Country codes used in the bulk download", "", "2026-06-24",
         "", "TBS terms of reuse"],
        [F_SITC, "Trade and Business Statistics", "SITC Revision 4 divisions", "", "2026-06-24", "",
         "TBS terms of reuse"],
        [F_PORTS, "Harbours Board", "Bulk loadings by port, monthly", "December 2022 to June 2026", "2026-07-15",
         "monthly statistics", "Harbours Board open data"],
        [F_TRACKER, "Tarbert Economics", "GDP tracker, June quarter 2026", "June quarter 2026",
         "2026-07-28 08:00", "desk workbook", "internal"],
        [F_POLL, "Harbourline", "Economists' poll: GDP, June quarter 2026", "June quarter 2026", "2026-07-23",
         "wire subscription", "Harbourline subscriber terms"],
        [F_SURVEY, "Industry Federation", "Business conditions survey", "January 2025 to June 2026", "2026-07-06",
         "members' release", "Industry Federation terms"],
    ]


INDEX_COLS = ["file", "publisher", "title", "covers", "received", "how", "terms"]


# ---------------------------------------------------------------------------------------------------- the world for the pack
def prepare():
    """The world, its national accounts, partner trade, ports, the bulletin's tables, the tracker's base and track
    (the household line placed by tracker.GOLDEN_TARGET on the bulletin lines the golden builds)."""
    import calc as C
    W = WD.simulate()
    NA.simulate(W)
    PT.energy_by_market(W)
    PT.bulk(W)
    PT.port_loadings(W)
    original_terms(W)
    W.BULLETIN = bulletin_tables(W)
    base = tracker_base(W)
    B = provisional_bundle(W, base)
    bq2 = {"X_G": C.goods(B, "2026Q2", "x"), "M_G": C.goods(B, "2026Q2", "m"), "CIPI_NF": C.cipi(B, "2026Q2")}
    est = track_levels(base, bq2)
    W.BASE, W.TRACK = base, est
    return W


def track_levels(base, bq2):
    est = {}
    for label, c, g, src in TR.LINES:
        if g is None or g == "TBS":
            continue
        est[c] = int(round(g)) if c == "CIPI_FO" else int(round(base[c] * (1.0 + g)))
    target_q = ((1.0 + TR.GOLDEN_TARGET / 100.0) ** 0.25 - 1.0) * 100.0
    gdp1 = base["GDP"]
    known = sum((-1.0 if c == "M_S" else 1.0) * (est[c] - base[c]) for c in est)
    known += (bq2["X_G"] - base["X_G"]) - (bq2["M_G"] - base["M_G"]) + (bq2["CIPI_NF"] - base["CIPI_NF"])
    est["HFCE"] = int(round(base["HFCE"] + target_q / 100.0 * gdp1 - known))
    return est


def provisional_bundle(W, base):
    """The bundle from the world's own published tables (the same numbers the files will carry), for placing the
    tracker before the files exist."""
    B = {}
    months_all = MONTHS
    B["p25"] = {c: _rebase_arr({m: W.PUB_P[c][MI[m]] for m in months_all}) for c in K.IND_CODES}
    B["pout25"] = {c: _rebase_arr({m: W.PUB_POUT[c][MI[m]] for m in months_all}) for c in K.IND_CODES}
    B["px25"] = {s: _rebase_arr({m: W.PUB_PX[s][MI[m]] for m in months_all}) for s in K.SITC_CODES}
    B["pm25"] = {s: _rebase_arr({m: W.PUB_PM[s][MI[m]] for m in months_all}) for s in K.SITC_CODES}
    B["stocks"] = {c: {m: float(W.PUB_B[c][MI[m]]) for m in months_all if not np.isnan(W.PUB_B[c][MI[m]])}
                   for c in K.IND_CODES}
    B["sales"] = {c: {m: float(W.PUB_S[c][MI[m]]) for m in months_all if not np.isnan(W.PUB_S[c][MI[m]])}
                  for c in K.IND_CODES}
    B["ratio"] = {c: {m: float(W.T[c][MI[m]]) for m in months_all} for c in K.IND_CODES}
    B["xsa"] = {s: {m: float(W.PUB_VX[s][MI[m]]) for m in months_all} for s in K.SITC_CODES}
    B["msa"] = {s: {m: float(W.PUB_VM[s][MI[m]]) for m in months_all} for s in K.SITC_CODES}
    B["base"] = base
    B["gdp_q1"] = base["GDP"]
    return B


def _rebase_arr(d):
    """{month: 2019 = 100 index} over every generator month -> array rebased to the 2025 average (NaN before the
    file's first month)."""
    arr = np.array([d.get(m, np.nan) for m in MONTHS], dtype=float)
    yr = np.array([m.startswith("2025") for m in MONTHS])
    return arr / np.nanmean(arr[yr])


def write_all(out, W):
    """Every data file into out; returns {file: rows} for the input gates."""
    p = lambda f: os.path.join(out, f)
    n = {}
    n[F_DB] = K.write_csv(p(F_DB), DB_COLS, db_rows(W))
    write_annual(p(F_ANNUAL), W)
    write_prices(p(F_PRICES), W)
    n[F_PORTAL] = K.write_csv(p(F_PORTAL), PORTAL_COLS, portal_rows(W))
    n[F_BULK] = K.write_csv(p(F_BULK), BULK_COLS, bulk_rows(W), crlf=True)
    n[F_COUNTRIES] = K.write_csv(p(F_COUNTRIES), ["code", "country", "region"], country_rows())
    n[F_SITC] = K.write_csv(p(F_SITC), ["division", "title", "section", "section_title"], sitc_rows())
    n[F_PORTS] = K.write_csv(p(F_PORTS), PORT_COLS, port_rows(W))
    write_tracker(p(F_TRACKER), W, W.BASE, W.TRACK)
    with open(p(F_POLL), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(poll_doc(), fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    n[F_SURVEY] = K.write_csv(p(F_SURVEY), SURVEY_COLS, survey_rows())
    n[F_INDEX] = K.write_csv(p(F_INDEX), INDEX_COLS, index_rows())
    return n


# ---------------------------------------------------------------------------------------------------- the bundle
def read_csv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def bundle(out, W=None):
    """Everything calc.py and asks.py read, from the files in out (the bulletin's numbers from docs.py's tables,
    which the PDF prints; verify.py reads the PDF itself)."""
    import openpyxl
    import docs as D
    p = lambda f: os.path.join(out, f)
    B = {}
    # price indexes
    wb = openpyxl.load_workbook(p(F_PRICES), data_only=True)
    for sheet, title, key in PRICE_SHEETS:
        ws = wb[sheet]
        codes = [ws.cell(row=3, column=j).value for j in range(2, ws.max_column + 1)]
        d = {c: {} for c in codes}
        for r in range(5, ws.max_row + 1):
            dd = ws.cell(row=r, column=1).value
            if dd is None:
                continue
            m = "%04d-%02d" % (dd.year, dd.month)
            for j, c in enumerate(codes, 2):
                d[c][m] = float(ws.cell(row=r, column=j).value)
        B[key] = d
    B["p25"] = {c: _rebase_arr(B["pin"][c]) for c in K.IND_CODES}
    B["pout25"] = {c: _rebase_arr(B["pout"][c]) for c in K.IND_CODES}
    B["px25"] = {s: _rebase_arr(B["px"][s]) for s in K.SITC_CODES}
    B["pm25"] = {s: _rebase_arr(B["pm"][s]) for s in K.SITC_CODES}
    # TBS: the portal pull, then the bulletin over it for March to June 2026
    stocks = {c: {} for c in K.IND_CODES}
    sales = {c: {} for c in K.IND_CODES}
    ratio = {c: {} for c in K.IND_CODES}
    xsa = {s: {} for s in K.SITC_CODES}
    msa = {s: {} for s in K.SITC_CODES}
    xor = {s: {} for s in K.SITC_CODES}
    mor = {s: {} for s in K.SITC_CODES}
    for row in read_csv(p(F_PORTAL)):
        sid, m, v = row["series_id"], row["month"], float(row["value"])
        part = sid.split(".")
        if part[1] == "STK":
            stocks[part[2]][m] = v
        elif part[1] == "COS":
            sales[part[2]][m] = v
        elif part[1] == "RAT":
            ratio[part[2]][m] = v
        elif part[1] in ("EXP", "IMP"):
            s = part[2][1:]
            tgt = (xsa if part[1] == "EXP" else msa) if part[3] == "SA" else (xor if part[1] == "EXP" else mor)
            tgt[s][m] = v
    B["portal_stocks"] = {c: dict(v) for c, v in stocks.items()}
    B["portal_sales"] = {c: dict(v) for c, v in sales.items()}
    B["portal_ratio"] = {c: dict(v) for c, v in ratio.items()}
    B["portal_xsa"] = {s: dict(v) for s, v in xsa.items()}
    B["portal_msa"] = {s: dict(v) for s, v in msa.items()}
    B["portal_xor"], B["portal_mor"] = xor, mor
    T = D.BULLETIN_TABLES if W is None else W.BULLETIN
    for c in K.IND_CODES:
        for m in BULLETIN_MONTHS:
            stocks[c][m] = T["stocks"][c][m]
            sales[c][m] = T["sales"][c][m]
            ratio[c][m] = T["ratio"][c][m]
    for s in K.SITC_CODES:
        for m in BULLETIN_MONTHS:
            xsa[s][m] = T["exp"][s][m]
            msa[s][m] = T["imp"][s][m]
    B["stocks"], B["sales"], B["ratio"], B["xsa"], B["msa"] = stocks, sales, ratio, xsa, msa
    B["bulletin"] = T
    # the real-time database
    db = {}
    rel = {}
    for row in read_csv(p(F_DB)):
        db[(row["release_id"], row["price_basis"][:5], row["quarter"], row["series_id"])] = int(row["value_m"])
        rel[row["release_id"]] = (row["release_date"], row["estimate"], row["price_basis"])
    B["db"], B["releases"] = db, rel
    # the annual national accounts: the latest quarterly series
    wb = openpyxl.load_workbook(p(F_ANNUAL), data_only=True)
    heads = [wb["Table 3"].cell(row=4, column=j).value for j in range(2, wb["Table 3"].max_column + 1)]
    code_of = {"Household final consumption expenditure": "HFCE", "General government final consumption": "GFCE",
               "Dwellings": "GFCF_DW", "Machinery and equipment": "GFCF_ME", "Non-dwelling construction": "GFCF_NDC",
               "Intellectual property products": "GFCF_IPP", "General government investment": "GFCF_PUB",
               "Changes in inventories: non-farm business": "CIPI_NF",
               "Changes in inventories: farm and other": "CIPI_FO", "Exports of goods": "X_G",
               "Exports of services": "X_S", "Imports of goods": "M_G", "Imports of services": "M_S",
               "Gross domestic product": "GDP"}
    for sheet, key in (("Table 3", "latest"), ("Table 4", "latest_cp")):
        ws = wb[sheet]
        tab = {code_of[h]: {} for h in heads}
        for r in range(5, ws.max_row + 1):
            q = ws.cell(row=r, column=1).value
            if not q:
                continue
            qq = q.replace(" Q", "Q")
            for j, h in enumerate(heads, 2):
                tab[code_of[h]][qq] = int(ws.cell(row=r, column=j).value)
        B[key] = tab
    # the Office's latest non-farm inventories by quarter (the database's last release, which the update left as it was)
    last = [k for k, v in rel.items()][-1]
    B["office_cipi"] = {q: db[(last, "Chain", q, "CIPI_NF")] for q in NA.QUARTERS if (last, "Chain", q, "CIPI_NF") in db}
    # the tracker
    wb = openpyxl.load_workbook(p(F_TRACKER), data_only=True)
    ws = wb["Tracker"]
    base, track = {}, {}
    for r in range(6, ws.max_row + 1):
        code = ws.cell(row=r, column=2).value
        if not code:
            continue
        base[code] = ws.cell(row=r, column=3).value
        v = ws.cell(row=r, column=4).value
        if isinstance(v, (int, float)):
            track[code] = v
    B["gdp_q1"] = base.pop("GDP")
    B["base"], B["track"] = base, track
    # the bulk download, ports and codes
    bulk = {}
    for row in read_csv(p(F_BULK)):
        bulk[(row["month"], row["flow"], row["country"], row["sitc_division"])] = (
            int(row["value_000"]), int(row["quantity"]) if row["quantity"] else None, row["quantity_unit"])
    B["bulk"] = bulk
    B["ports"] = [(r["month"], r["port"], r["cargo"], int(r["tonnes_loaded"]), int(r["vessels"]))
                  for r in read_csv(p(F_PORTS))]
    B["countries"] = {r["code"]: r["country"] for r in read_csv(p(F_COUNTRIES))}
    return B
