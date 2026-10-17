"""Write the pack's data files: the two downloads of the service's estimates, the cooperative's enrolment, scale
tickets, transfer log, member roster and prior covers, the drought-monitor extract and Quillfield Re's quote
schedule."""
import csv
import datetime as dt

import numpy as np

import sim as S
import world as W


def write_csv(path, header, rows, delimiter=",", lineterminator="\r\n"):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, delimiter=delimiter, lineterminator=lineterminator)
        wr.writerow(header)
        for r in rows:
            wr.writerow(r)
    return len(rows)


# ---------------------------------------------------------------- the service's export
EXPORT_COLS = ["Program", "Year", "Period", "Geo Level", "Ag District", "Ag District Code", "County", "County ANSI",
               "Commodity", "Data Item", "Domain", "Domain Category", "Value", "CV (%)", "Load Time"]

PREFIX = {
    ("SORGHUM", "NON-IRRIGATED"): ("SORGHUM, GRAIN, NON-IRRIGATED", "SORGHUM, NON-IRRIGATED"),
    ("SORGHUM", "IRRIGATED"): ("SORGHUM, GRAIN, IRRIGATED", "SORGHUM, IRRIGATED"),
    ("SORGHUM", "ALL"): ("SORGHUM, GRAIN", "SORGHUM"),
    ("WHEAT", "NON-IRRIGATED"): ("WHEAT, WINTER, NON-IRRIGATED", "WHEAT, WINTER, NON-IRRIGATED"),
    ("WHEAT", "IRRIGATED"): ("WHEAT, WINTER, IRRIGATED", "WHEAT, WINTER, IRRIGATED"),
    ("WHEAT", "ALL"): ("WHEAT, WINTER", "WHEAT, WINTER"),
    ("CORN", "NON-IRRIGATED"): ("CORN, GRAIN, NON-IRRIGATED", "CORN, NON-IRRIGATED"),
    ("CORN", "IRRIGATED"): ("CORN, GRAIN, IRRIGATED", "CORN, IRRIGATED"),
    ("CORN", "ALL"): ("CORN, GRAIN", "CORN"),
    ("SOYBEANS", "IRRIGATED"): ("SOYBEANS, IRRIGATED", "SOYBEANS, IRRIGATED"),
    ("SOYBEANS", "ALL"): ("SOYBEANS", "SOYBEANS"),
    ("SUNFLOWER", "NON-IRRIGATED"): ("SUNFLOWER, NON-IRRIGATED", "SUNFLOWER, NON-IRRIGATED"),
    ("SUNFLOWER", "ALL"): ("SUNFLOWER", "SUNFLOWER"),
    ("HAY", "ALL"): ("HAY, ALFALFA", None),
}
PRACTICE_ORDER = {"ALL": 0, "IRRIGATED": 1, "NON-IRRIGATED": 2}


def fmt_int(v):
    return "{:,}".format(int(round(float(v))))


def fmt_yield(crop, prod, harv):
    if harv <= 0:
        return "(NA)"
    y = prod / harv
    if crop == "SUNFLOWER":
        return fmt_int(y)
    if crop == "HAY":
        return "%.2f" % y
    return "%.1f" % y


def items(crop, pr, rec, i):
    """(data item, value) pairs for one estimate in one year, unformatted value or None for a withheld mark."""
    unit = S.UNIT[crop][0]
    main, plant = PREFIX[(crop, pr)]
    out = []
    if plant and "planted" in rec:
        out.append((plant + " - ACRES PLANTED", ("int", rec["planted"][i])))
    out.append((main + " - ACRES HARVESTED", ("int", rec["harvested"][i])))
    out.append((main + " - PRODUCTION, MEASURED IN " + unit, ("int", rec["production"][i])))
    out.append((main + " - YIELD, MEASURED IN " + unit + " / ACRE", ("yield", rec["production"][i], rec["harvested"][i])))
    return out


def load_time(year, revised):
    if revised:
        return "2026-03-26 15:00:00.000"
    if year < 2001:
        return "2002-06-18 09:00:00.000"
    rel = dt.date(year + 1, 2, 20) + dt.timedelta(days=int(np.random.default_rng([W.STREAM, 61, year]).integers(0, 9)))
    return "%s 15:00:00.000" % rel.isoformat()


def export_rows(x, vintage):
    """The rows of one download: 'old' is March 2024 (1991 to 2023, before the 2026 revision), 'new' October 2026
    (2016 to 2025, county estimates for 2017 to 2021 revised)."""
    lo, hi = W.OLD_PULL if vintage == "old" else W.NEW_PULL
    cty = x["cty_old"] if vintage == "old" else x["cty_new"]
    dist = x["dist_old"] if vintage == "old" else x["dist_new"]
    state = x["state_old"] if vintage == "old" else x["state_new"]
    pub = x["pub"]
    rows = []

    def code(d, year):
        if vintage == "old" and year < W.RECODE_YEAR:
            return str(d // 10)
        return str(d)

    def ansi(c):
        a = W.COUNTIES[c][0]
        return str(int(a)) if vintage == "old" else a

    def emit(year, level, d, county, crop, pr, rec, i, published, cv_ok):
        if rec["harvested"][i] <= 0 and rec.get("planted", np.zeros(len(S.YEARS)))[i] <= 0:
            return                       # no estimate where the crop was not grown
        revised = vintage == "new" and W.REVISED[0] <= year <= W.REVISED[1]
        for item, val in items(crop, pr, rec, i):
            if not published:
                v, cv = "(S)", ""
            elif val[0] == "int":
                v, cv = fmt_int(val[1]), ""
            else:
                v = fmt_yield(crop, val[1], val[2])
                cv = ""
                if cv_ok and year >= 2008:
                    c = S.cv_percent(county.title() if county else "", crop, pr, float(val[2]), year) if county else None
                    cv = "%.1f" % c if c is not None else ""
            rows.append(["SURVEY", year, "YEAR", level, W.DISTRICTS[d].upper() if d else "", code(d, year) if d else "",
                         county, ansi(county.title()) if county else "", crop, item, "TOTAL", "NOT SPECIFIED", v, cv,
                         load_time(year, revised)])

    for year in range(lo, hi + 1):
        i = year - W.Y0
        for (crop, pr), rec in sorted(state.items(), key=lambda kv: (S.CROPS.index(kv[0][0]), PRACTICE_ORDER[kv[0][1]])):
            emit(year, "STATE", None, "", crop, pr, rec, i, True, False)
        dkeys = {}
        for (d, crop, pr), rec in list(dist.items()) + list(x["other"].items()):
            dkeys[(d, crop, pr)] = rec
        for (d, crop, pr), rec in sorted(dkeys.items(), key=lambda kv: (kv[0][0], S.CROPS.index(kv[0][1]),
                                                                       PRACTICE_ORDER[kv[0][2]])):
            emit(year, "AGRICULTURAL DISTRICT", d, "", crop, pr, rec, i, True, False)
        for c in sorted(W.COUNTIES, key=lambda k: (W.COUNTIES[k][1], k)):
            d = W.COUNTIES[c][1]
            for crop in S.CROPS:
                for pr in ("ALL", "IRRIGATED", "NON-IRRIGATED"):
                    if (c, crop, pr) not in cty:
                        continue
                    if (crop, pr) not in PREFIX:
                        continue
                    if crop == "HAY" and pr != "ALL":
                        continue
                    emit(year, "COUNTY", d, c.upper(), crop, pr, cty[(c, crop, pr)], i, bool(pub[(c, crop, pr)][i]), True)
    return rows


# ---------------------------------------------------------------- the cooperative's files
ENROL_COLS = ["submission_id", "submitted_at", "member_no", "field_id", "field_county", "crop", "practice", "acres",
              "action"]
TICKET_COLS = ["ticket_no", "site", "ticket_date", "account", "commodity", "origin_county", "gross_lb", "tare_lb",
               "net_lb", "moisture_pct", "test_weight", "reference"]
TRANSFER_COLS = ["transfer_no", "ship_date", "from_site", "to_site", "commodity", "net_lb", "carrier"]
DROUGHT_COLS = ["MapDate", "County", "None", "D0", "D1", "D2", "D3", "D4", "ValidStart", "ValidEnd"]


def enrol_rows(subs):
    return [[s["sid"], s["stamp"], s["member"], s["field"], s["county"], "Grain sorghum", s["practice"],
             "%.1f" % s["acres"], s["action"]] for s in subs]


def ticket_rows(rows):
    return [[t["ticket"], t["site"], t["date"].isoformat(), t["account"], t["crop"].title(), t["origin"],
             t["gross"], t["tare"], t["net"], "%.1f" % t["moisture"], "%.1f" % t["tw"], t["reference"]] for t in rows]


def transfer_rows(tr):
    return [[t["transfer"], t["date"].isoformat(), t["frm"], t["to"], t["crop"].title(), t["net"], t["carrier"]]
            for t in tr]


def drought_rows(ws):
    out = []
    for w in ws:
        d = w["date"]
        end = d + dt.timedelta(days=6)
        out.append([d.strftime("%Y%m%d"), w["county"] + " County", "%.2f" % w["none"]] + ["%.2f" % v for v in w["d"]]
                   + [d.isoformat(), end.isoformat()])
    return out


def _sheet_header(ws, title, sub, row=1):
    from openpyxl.styles import Font
    ws.cell(row=row, column=1, value=title).font = Font(name="Calibri", size=13, bold=True)
    ws.cell(row=row + 1, column=1, value=sub).font = Font(name="Calibri", size=9, italic=True, color="595959")


def _table(ws, top, header, rows, widths, formats=None):
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    thin = Side(style="thin", color="A6A6A6")
    for j, h in enumerate(header, start=1):
        c = ws.cell(row=top, column=j, value=h)
        c.font = Font(name="Calibri", size=10, bold=True)
        c.fill = PatternFill("solid", fgColor="E7EEF3")
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = Border(bottom=thin)
    for i, r in enumerate(rows, start=top + 1):
        for j, v in enumerate(r, start=1):
            c = ws.cell(row=i, column=j, value=v)
            c.font = Font(name="Calibri", size=10)
            if formats and formats.get(j):
                c.number_format = formats[j]
    for j, w in enumerate(widths, start=1):
        ws.column_dimensions[ws.cell(row=top, column=j).column_letter].width = w
    ws.freeze_panes = ws.cell(row=top + 1, column=1)


def quote_workbook(path, ts):
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Dryland grain sorghum"
    _sheet_header(ws, "Quillfield Re: area-yield drought covers, 2027 crop year",
                  "Quote schedule for Ardley Plains Growers' Cooperative, 14 October 2026; rates hold to 30 November "
                  "2026 and are subject to the term sheet of the same date.")
    rows = [[c, ts[c]["expected"], "90%", round(W.QUOTES[c] / 100.0, 6)] for c in W.MEMBERS]
    _table(ws, 4, ["County", "Expected yield 2027 (bu per harvested acre)", "Coverage level",
                   "Quoted premium rate (per cent of liability)"], rows, [14, 22, 12, 24],
           {2: "0.0", 4: "0.00%"})
    ws.cell(row=11, column=1, value="Each county's cover is quoted and may be bought on its own.")
    ws2 = wb.create_sheet("Irrigated grain sorghum")
    _sheet_header(ws2, "Irrigated grain sorghum, 2027 crop year", "Quoted at the cooperative's request of 2 October "
                  "2026; index the county's irrigated grain sorghum yield.")
    _table(ws2, 4, ["County", "Expected yield 2027 (bu per harvested acre)", "Coverage level",
                    "Quoted premium rate (per cent of liability)"], [["Corvin", 109.4, "85%", 0.0185]],
           [14, 22, 12, 24], {2: "0.0", 4: "0.00%"})
    ws3 = wb.create_sheet("Dryland winter wheat")
    _sheet_header(ws3, "Dryland winter wheat, 2027 crop year", "Indicative only; the wheat term sheet follows in "
                  "January 2027.")
    wq = {"Ardley": (47.2, 0.0612), "Corvin": (49.8, 0.0455), "Elster": (45.9, 0.0688), "Pallard": (47.6, 0.0581),
          "Tresham": (44.8, 0.0640)}
    _table(ws3, 4, ["County", "Expected yield 2027 (bu per harvested acre)", "Coverage level",
                    "Indicative premium rate (per cent of liability)"], [[c, wq[c][0], "85%", wq[c][1]] for c in W.MEMBERS],
           [14, 22, 12, 24], {2: "0.0", 4: "0.00%"})
    wb.save(path)


def roster_workbook(path, members):
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Members"
    _sheet_header(ws, "Ardley Plains Growers' Cooperative: member roster", "As at 30 September 2026. Member numbers "
                  "are the accounts the elevators and the member portal use.")
    _table(ws, 4, ["Member no.", "Entity type", "Home county", "Joined", "Status"],
           [[m["member_no"], m["entity"], m["home_county"], m["joined"], m["status"]] for m in members],
           [12, 14, 14, 9, 10])
    wb.save(path)


def prior_workbook(path, rows):
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Statements"
    _sheet_header(ws, "Area-yield covers 2019 to 2025: annual statements", "Corvin and Tresham dryland grain sorghum "
                  "covers, one-year terms, trigger at 85 per cent of each year's expected yield.")
    _table(ws, 4, ["County", "Crop year", "Expected yield (bu/acre)", "Trigger yield (bu/acre)",
                   "Final county yield (bu/acre)", "Liability ($)", "Premium rate", "Indemnity ($)"],
           [[r["county"], r["year"], r["expected"], r["trigger"], r["final"], r["liability"], r["rate"] / 100.0,
             r["indemnity"]] for r in rows], [10, 10, 13, 13, 14, 14, 11, 13],
           {3: "0.0", 4: "0.0", 5: "0.0", 6: "#,##0", 7: "0.00%", 8: "#,##0"})
    wb.save(path)
