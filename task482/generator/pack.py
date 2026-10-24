"""Writes the shipped data files from the world's records, each in the layout and vocabulary of the system that keeps
it: the office's resident estimates, the state's e-reporting export for five plants, the contract operator's pond
reports, the joint plant's member meters, the basin's Lake Protection Fee returns, the two booking platforms'
remittance files, the e-reporting parameter codes, and two files the office keeps for other work."""
import csv
import datetime as dt

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

import world as W

GEOID = {"Birchwick": "2799104", "Teskadel": "2799116", "Ruddmere": "2799122", "Sorrelton": "2799139",
         "Pinehold": "2799143", "Tamsen Point": "2799158", "Esker Narrows": "2799161", "Hollin Bay": "2799177"}
TOWNSHIPS = (("Arlen Township", "2799201", (1406, 1219, 1224)), ("Quill Township", "2799214", (2148, 2160, 2171)),
             ("Vessing Township", "2799226", (893, 899, 904)))
OPERATOR = "Northwoods Utility Services"


def write_csv(path, header, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(header)
        w.writerows(rows)


def mdy(d):
    return "%02d/%02d/%d" % (d.month, d.day, d.year)


def month_end(y, m):
    return dt.date(y, m, W.days_in(y, m))


# ------------------------------------------------------------------------------------------- the residents

def residents_csv(path):
    rows = []
    tot = [0, 0, 0]
    for t in W.TOWNS:
        n, res = t[0], t[1]
        note = ""
        if n == "Pinehold":
            note = ("Boundary change: 412 acres of Arlen Township annexed effective 1 January 2025 (order A-2024-117); "
                    "2025 and 2026 estimates on the current boundary, 2024 on the former boundary")
        hh = int(round(res[2] / dict(Birchwick=2.21, Teskadel=2.34, Ruddmere=2.08, Sorrelton=2.29, Pinehold=2.27)
                       .get(n, 2.25)))
        rows.append([GEOID[n], n + " city", W.COUNTY, res[0], res[1], res[2], hh, note])
        for i in range(3):
            tot[i] += res[i]
    for n, g, res in TOWNSHIPS:
        note = "Area annexed to Pinehold city effective 1 January 2025" if n == "Arlen Township" else ""
        rows.append([g, n, W.COUNTY, res[0], res[1], res[2], int(round(res[2] / 2.31)), note])
        for i in range(3):
            tot[i] += res[i]
    rows.append(["27991", W.COUNTY, W.COUNTY, tot[0], tot[1], tot[2], "", "County total"])
    write_csv(path, ["GEOID", "GEOGRAPHY", "COUNTY", "POPEST_2024_07_01", "POPEST_2025_07_01", "POPEST_2026_07_01",
                     "HOUSEHOLDS_2026_07_01", "NOTE"], rows)


# ----------------------------------------------------------------------------------------------- the plants

PARAM = [  # code, description, unit, location code, location description
    ("50050", "Flow, in conduit or thru treatment plant", "MGD", "G", "Raw sewage influent"),
    ("00310", "BOD, 5-day, 20 deg. C", "mg/L", "G", "Raw sewage influent"),
    ("00530", "Solids, total suspended", "mg/L", "G", "Raw sewage influent"),
    ("50050", "Flow, in conduit or thru treatment plant", "MGD", "1", "Effluent gross"),
    ("00310", "BOD, 5-day, 20 deg. C", "mg/L", "1", "Effluent gross"),
    ("00530", "Solids, total suspended", "mg/L", "1", "Effluent gross"),
    ("00665", "Phosphorus, total [as P]", "mg/L", "1", "Effluent gross"),
]
RESUB = {  # plant, year, month: the chain of submissions, and the first lab result's ratio to the corrected one
    ("BIR", 2025, 4): dict(f=1.37, chain=("Superseded", "Accepted", "Returned")),
    ("BIR", 2025, 8): dict(f=0.71, chain=("Superseded", "Accepted", "Returned")),
    ("BIR", 2026, 2): dict(f=1.22, chain=("Superseded", "Accepted")),
    ("TES", 2025, 3): dict(f=1.31, chain=("Superseded", "Accepted")),
    ("TES", 2025, 6): dict(f=1.44, chain=("Superseded", "Accepted", "Returned")),
    ("TES", 2025, 9): dict(f=1.58, chain=("Superseded", "Accepted", "Returned")),
    ("SOR", 2025, 2): dict(f=0.76, chain=("Superseded", "Accepted")),
    ("SOR", 2025, 5): dict(f=1.52, chain=("Superseded", "Accepted", "Returned")),
    ("SOR", 2025, 11): dict(f=1.41, chain=("Superseded", "Accepted", "Returned")),
    ("TAM", 2025, 2): dict(f=0.68, chain=("Superseded", "Accepted", "Returned")),
    ("TAM", 2025, 7): dict(f=1.29, chain=("Superseded", "Accepted")),
    ("TAM", 2025, 10): dict(f=1.47, chain=("Superseded", "Accepted", "Returned")),
    ("NAR", 2025, 6): dict(f=1.36, chain=("Superseded", "Accepted", "Returned")),
    ("NAR", 2025, 12): dict(f=0.73, chain=("Superseded", "Accepted", "Returned")),
    ("NAR", 2026, 5): dict(f=1.25, chain=("Superseded", "Accepted")),
}


def edmr_csv(path, mor):
    """The state's e-reporting export for the five mechanical plants: one row per value, every submission of a
    monitoring period with its received date and status. A resubmission repeats the whole report with the corrected
    value; a submission returned for correction stays in the export."""
    r = W.rng(301)
    rows = []
    sub = 4410000
    for code in ("BIR", "TES", "SOR", "TAM", "NAR"):
        pl = W.PLANTS[code]
        for row in mor[code]:
            y, m = row["y"], row["m"]
            end = month_end(y, m)
            base = end + dt.timedelta(days=int(r.integers(6, 19)))
            vals = [row["inf_flow"], row["inf_bod"], row["inf_tss"], row["eff_flow"], row["eff_bod"], row["eff_tss"],
                    row["eff_tp"]]
            fmt = ["%.4f", "%.0f", "%.0f", "%.4f", "%.1f", "%.1f", "%.2f"]
            rs = RESUB.get((code, y, m))
            chain = rs["chain"] if rs else ("Accepted",)
            for k, status in enumerate(chain):
                sub += int(r.integers(11, 97))
                rec = base + dt.timedelta(days=0 if k == 0 else int(r.integers(9, 26)) * k)
                for (pc, desc, unit, loc, _), v, f in zip(PARAM, vals, fmt):
                    if rs and pc == "00665":
                        # the original carried the lab's first result; the accepted resubmission the corrected one;
                        # a later submission returned for correction repeated the first result
                        v = round(v * rs["f"], 2) if status in ("Superseded", "Returned") else v
                    rows.append([pl["permit"], pl["name"], "SD001" if loc == "1" else "WS001", loc, pc, desc,
                                 mdy(end), "MO AVG", f % v, unit, "", "%d" % sub, mdy(rec), status])
    write_csv(path, ["PERMIT_ID", "FACILITY_NAME", "PERM_FEATURE_ID", "MONITORING_LOCATION_CODE", "PARAMETER_CODE",
                     "PARAMETER_DESC", "MONITORING_PERIOD_END_DATE", "STATISTICAL_BASE", "DMR_VALUE", "DMR_UNIT",
                     "NODI_CODE", "SUBMISSION_ID", "RECEIVED_DATE", "SUBMISSION_STATUS"], rows)


def ponds_xlsx(path, mor):
    """The contract operator's monthly operating reports for the two stabilization pond systems, one sheet per pond
    and year. The ponds discharge only in their spring and autumn drawdowns; the operator reports each flow as the
    month's average daily flow, as the state's reports do."""
    wb = openpyxl.Workbook()
    first = True
    for code in ("RUD", "PIN"):
        pl = W.PLANTS[code]
        for yr in (2025, 2026):
            ws = wb.active if first else wb.create_sheet()
            first = False
            ws.title = "%s %d" % (pl["towns"][0], yr)
            ws.append(["%s, permit %s: monthly operating report summary, %d" % (pl["name"], pl["permit"], yr)])
            ws.append(["Prepared by %s for the City of %s" % (OPERATOR, pl["towns"][0])])
            ws.append([])
            ws.append(["Month", "Influent flow, MGD", "Influent BOD5, mg/L", "Influent TSS, mg/L",
                       "Discharge", "Days discharged", "Effluent flow, MGD",
                       "Effluent BOD5, mg/L", "Effluent TSS, mg/L", "Effluent total P, mg/L", "Remarks"])
            for c in ws[4]:
                c.font = Font(bold=True)
                c.alignment = Alignment(wrap_text=True, vertical="top")
            for row in mor[code]:
                if row["y"] != yr:
                    continue
                d = row["days"]
                rem = None
                if d and row["m"] in (4, 5):
                    rem = "Spring drawdown, secondary cell"
                elif d:
                    rem = "Autumn drawdown"
                elif row["m"] in (12, 1, 2, 3):
                    rem = "Ice cover"
                ws.append([dt.date(yr, row["m"], 1).strftime("%b %Y"), round(row["inf_flow"], 4),
                           round(row["inf_bod"]), round(row["inf_tss"]), "Yes" if d else "No", d if d else None,
                           round(row["eff_flow"], 3) if d else None, round(row["eff_bod"], 1) if d else None,
                           round(row["eff_tss"], 1) if d else None, round(row["eff_tp"], 2) if d else None, rem])
            for i, w in enumerate([11, 15, 12, 12, 10, 10, 18, 11, 11, 12, 30], 1):
                ws.column_dimensions[get_column_letter(i)].width = w
            ws.row_dimensions[4].height = 45
            ws.freeze_panes = "B5"
    wb.save(path)


def meters_csv(path, meters):
    """The joint plant's billing meters on each member town's force main, read at midnight as each month ends.
    Esker Narrows' meter was replaced on 14 August 2025 and the new one's register started at zero."""
    rows = []
    for n, mid0, mid1 in (("Esker Narrows", "NJ-M1-04471", "NJ-M1-09112"), ("Hollin Bay", "NJ-M2-04473", None)):
        reg = dict(old=48_211_900, new=0)
        for (y, m) in W.MOR_MONTHS:
            vol = int(round(meters[(n, y, m)]))
            if n == "Esker Narrows" and (y, m) == (2025, 8):
                part = int(round(vol * 13 / 31))
                reg["old"] += part
                rows.append([mid0, n, "08/14/2025 10:40", reg["old"], part, "Meter removed (register failure)"])
                reg["new"] += vol - part
                rows.append([mid1, n, mdy(month_end(y, m) + dt.timedelta(days=1)) + " 00:00", reg["new"], vol - part,
                             "New meter set 08/14/2025"])
                continue
            mid = mid1 if (n == "Esker Narrows" and (y, m) > (2025, 8)) else mid0
            key = "new" if mid == mid1 else "old"
            reg[key] += vol
            rows.append([mid, n, mdy(month_end(y, m) + dt.timedelta(days=1)) + " 00:00", reg[key], vol, ""])
    write_csv(path, ["METER_ID", "MEMBER", "READ_AT", "REGISTER_GAL", "VOLUME_SINCE_LAST_READ_GAL", "REMARK"], rows)


def parameter_codes_csv(path):
    rows = [["50050", "Flow, in conduit or thru treatment plant", "MGD", "Million gallons per day"],
            ["00310", "BOD, 5-day, 20 deg. C", "mg/L", "Milligrams per liter"],
            ["00530", "Solids, total suspended", "mg/L", "Milligrams per liter"],
            ["00665", "Phosphorus, total [as P]", "mg/L", "Milligrams per liter"],
            ["00610", "Nitrogen, ammonia total [as N]", "mg/L", "Milligrams per liter"],
            ["81010", "BOD, 5-day, percent removal", "%", "Percent"]]
    loc = [["1", "Effluent gross"], ["G", "Raw sewage influent"], ["K", "Percent removal"]]
    stat = [["MO AVG", "Monthly average of the period's results"], ["MO MAX", "Highest result in the period"],
            ["MO TOTAL", "Total for the period"]]
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["TABLE", "CODE", "DESCRIPTION", "UNIT_OR_NOTE"])
        for a in rows:
            w.writerow(["PARAMETER"] + a[:2] + [a[2] + " (" + a[3] + ")"])
        for a in loc:
            w.writerow(["MONITORING_LOCATION"] + a + [""])
        for a in stat:
            w.writerow(["STATISTICAL_BASE"] + a + [""])


# ------------------------------------------------------------------------------------------- the paid stays

WORDS_A = ("Loon", "Pine", "Birch", "Cedar", "Tamarack", "Walleye", "Northern", "Bluewater", "Driftwood", "Heron",
           "Aspen", "Sandy", "Juniper", "Eagle", "Moonrise", "Lakeview", "Kettle", "Quillmere", "Shoreline", "Fern")
WORDS_B = dict(Resort=("Resort", "Cabins Resort", "Lodge and Cabins", "Shores Resort", "Point Resort"),
               Lodge=("Lodge", "Lake Lodge", "Inn and Suites", "Lodge and Marina"),
               Motel=("Motel", "Motor Inn", "Inn", "Budget Inn"),
               Inn=("Inn", "Lake Inn", "Guest House", "House Inn"),
               Campground=("Campground", "RV Park", "Family Campground", "Camp and RV"),
               **{"Bed and breakfast": ("Bed and Breakfast", "B&B", "Guest Rooms", "House B&B")})
STREETS = ("Lakeshore Dr", "County Road 12", "Main St", "Pine Ridge Rd", "Shady Lane", "Birch Point Rd", "Hwy 34",
           "Narrows Rd", "Old Mill Rd", "Bay View Dr", "Tamarack Trl", "Loon Lake Rd", "Sunset Ln", "Church St",
           "Harbor Rd", "Cedar Ave", "North Shore Rd", "Fernwood Ln", "Quill Ave", "Resort Rd")
MAIL_CITIES = (("Minneapolis", "MN"), ("Edina", "MN"), ("St. Cloud", "MN"), ("Fargo", "ND"), ("Des Moines", "IA"),
               ("Eau Claire", "WI"), ("Rochester", "MN"), ("Sioux Falls", "SD"))


def business_names(props):
    r = W.rng(311)
    used = set()
    for p_ in props:
        while True:
            nm = "%s %s" % (WORDS_A[int(r.integers(len(WORDS_A)))], WORDS_B[p_["kind"]][int(r.integers(len(WORDS_B[p_["kind"]])))])
            if nm not in used:
                used.add(nm)
                break
        p_["name"] = nm
        p_["address"] = "%d %s" % (int(r.integers(10, 9800)), STREETS[int(r.integers(len(STREETS)))])
        if r.random() < 0.22:
            p_["mail"] = MAIL_CITIES[int(r.integers(len(MAIL_CITIES)))]
        else:
            p_["mail"] = (p_["town"], "MN")


def rate_on(d):
    return W.RATES[1] if d >= W.RATE_CHANGE else W.RATES[0]


def returns_rows(props, ln):
    """Lake Protection Fee returns, periods July 2025 to September 2026: monthly for eight units or more, quarterly
    otherwise. An amended return replaces the earlier return for its period; a supplemental return reports guest-nights
    left off it and adds to it. Returns are filed by the 20th of the month after the period."""
    r = W.rng(321)
    rows = []
    periods_m = list(W.month_iter(dt.date(2025, 7, 1), dt.date(2026, 9, 30)))
    for i, p_ in enumerate(props):
        if p_["freq"] == "monthly":
            pers = [((y, m),) for (y, m) in periods_m]
        else:
            pers = [tuple(periods_m[k:k + 3]) for k in range(0, len(periods_m), 3)]
        for months in pers:
            g = sum(ln[(i, y, m)][0] for (y, m) in months)
            ex = sum(ln[(i, y, m)][1] for (y, m) in months)
            start = dt.date(months[0][0], months[0][1], 1)
            end = month_end(*months[-1])
            rate = rate_on(start)
            due = month_end(*months[-1]) + dt.timedelta(days=int(r.integers(5, 21)))
            kind = r.random()
            if kind < 0.035 and g > 40:
                # an original with a keying error, then an amended return with the right counts
                bad = int(round(g * float(r.uniform(0.80, 0.93))))
                rows.append(_ret(p_, start, end, "Original", bad, ex, rate, due))
                rows.append(_ret(p_, start, end, "Amended", g, ex, rate, due + dt.timedelta(days=int(r.integers(20, 80)))))
            elif kind < 0.06 and g > 40:
                # guest-nights from a booking channel left off the original, reported on a supplemental return
                extra = int(round(g * float(r.uniform(0.06, 0.18))))
                rows.append(_ret(p_, start, end, "Original", g - extra, ex, rate, due))
                rows.append(_ret(p_, start, end, "Supplemental", extra, 0, rate,
                                 due + dt.timedelta(days=int(r.integers(30, 110)))))
            else:
                rows.append(_ret(p_, start, end, "Original", g, ex, rate, due))
    return rows


def _ret(p_, start, end, typ, g, ex, rate, filed):
    taxable = max(0, g - ex)
    return [p_["account"], p_["name"], p_["kind"], p_["address"], p_["town"], p_["mail"][0], p_["mail"][1],
            "Monthly" if p_["freq"] == "monthly" else "Quarterly", mdy(start), mdy(end), typ, g, ex, taxable,
            "%.2f" % rate, "%.2f" % (taxable * rate), mdy(filed)]


def returns_csv(path, props, ln):
    business_names(props)
    rows = returns_rows(props, ln)
    rows.sort(key=lambda x: (x[0], dt.datetime.strptime(x[8], "%m/%d/%Y"), dt.datetime.strptime(x[16], "%m/%d/%Y")))
    write_csv(path, ["ACCOUNT_NO", "BUSINESS_NAME", "PROPERTY_TYPE", "PROPERTY_ADDRESS", "PROPERTY_CITY", "MAILING_CITY",
                     "MAILING_STATE", "FILING_FREQUENCY", "PERIOD_START", "PERIOD_END", "RETURN_TYPE",
                     "GUEST_NIGHTS_TOTAL", "GUEST_NIGHTS_EXEMPT", "GUEST_NIGHTS_TAXABLE", "FEE_RATE", "FEE_DUE",
                     "DATE_FILED"], rows)
    return rows


def booking_fee(b):
    if b["nights"] >= 30:
        return 0.0
    return sum(rate_on(b["checkin"] + dt.timedelta(days=i)) for i in range(b["nights"])) * b["guests"]


def lakeward_csv(path, lst, bk):
    """Lakeward Stays' fee remittance detail: one row per stay remitted, remitted with the month the stay checked out,
    July 2025 to September 2026."""
    r = W.rng(331)
    addr = {}
    rows = []
    for b in bk:
        L = lst[b["listing"]]
        if L["platform"] != 0:
            continue
        out = b["checkin"] + dt.timedelta(days=b["nights"])
        if not (dt.date(2025, 7, 1) <= out <= dt.date(2026, 9, 30)):
            continue
        if b["listing"] not in addr:
            addr[b["listing"]] = "%d %s" % (int(r.integers(10, 9800)), STREETS[int(r.integers(len(STREETS)))])
        rows.append(["HM%s" % format(b["id"], "X"), L["id"], addr[b["listing"]], L["town"].upper(), "MN",
                     b["checkin"].isoformat(), out.isoformat(), b["nights"], b["guests"], "%.2f" % booking_fee(b),
                     "%d-%02d" % (out.year, out.month)])
    rows.sort(key=lambda x: (x[10], x[5], x[0]))
    write_csv(path, ["confirmation_code", "listing_id", "listing_street", "listing_city", "listing_state", "check_in",
                     "check_out", "nights", "guests", "lake_protection_fee_usd", "remittance_month"], rows)
    return rows


def kettlepine_csv(path, lst, bk):
    """Kettle & Pine's remittance report: the stays whose fee it remitted in each reporting period, a stay remitted in
    the month after it checked out. The reservation reference carries the departure date (R, then YYMMDD), the date
    Kettle & Pine's folios are numbered by."""
    r = W.rng(341)
    rows = []
    addr = {}
    seq = {}
    for b in bk:
        L = lst[b["listing"]]
        if L["platform"] != 1:
            continue
        out = b["checkin"] + dt.timedelta(days=b["nights"])
        per = dt.date(out.year + (out.month == 12), out.month % 12 + 1, 1)
        if not (dt.date(2025, 7, 1) <= per <= dt.date(2026, 9, 1)):
            continue
        k = out
        seq[k] = seq.get(k, 1000 + int(r.integers(0, 900))) + int(r.integers(1, 9))
        if b["listing"] not in addr:
            addr[b["listing"]] = "%d %s" % (int(r.integers(10, 9800)), STREETS[int(r.integers(len(STREETS)))])
        rows.append(["%d-%02d" % (per.year, per.month), "R%s-%04d" % (out.strftime("%y%m%d"), seq[k] % 10000),
                     L["id"], addr[b["listing"]], L["town"], b["nights"], b["guests"], "%.2f" % booking_fee(b)])
    rows.sort(key=lambda x: (x[0], x[2], x[1]))
    write_csv(path, ["Reporting period", "Reservation", "Property ID", "Property address", "Municipality", "Nights",
                     "Party size", "Fee remitted (USD)"], rows)
    return rows


def returns_layout_txt(path):
    lines = [
        "QUILLMERE LAKE PROTECTION FEE - RETURNS EXTRACT - FIELD LIST",
        "Extract of returns filed with the Quillmere Lake Basin Fee Office for periods 07/2025 through 09/2026,",
        "pulled 10/16/2026 for the Office of the State Demographer under the 2024 data sharing agreement.",
        "One row per return filed. CSV, comma delimited, CR LF line ends.",
        "",
        "ACCOUNT_NO            fee account of the lodging property",
        "BUSINESS_NAME         registered business name",
        "PROPERTY_TYPE         Resort, Lodge, Motel, Inn, Campground, Bed and breakfast",
        "PROPERTY_ADDRESS      street address of the property",
        "PROPERTY_CITY         city in which the property lies",
        "MAILING_CITY          city of the account's mailing address",
        "MAILING_STATE         state of the mailing address",
        "FILING_FREQUENCY      Monthly (8 or more rentable units) or Quarterly",
        "PERIOD_START          first day of the return period, MM/DD/YYYY",
        "PERIOD_END            last day of the return period, MM/DD/YYYY",
        "RETURN_TYPE           Original; Amended (replaces the account's earlier return for the period);",
        "                      Supplemental (reports guest-nights omitted from an earlier return for the period)",
        "GUEST_NIGHTS_TOTAL    guest-nights in the period (persons x nights)",
        "GUEST_NIGHTS_EXEMPT   guest-nights of stays of 30 consecutive nights or more",
        "GUEST_NIGHTS_TAXABLE  total less exempt",
        "FEE_RATE              fee per taxable guest-night in force for the period, USD",
        "FEE_DUE               taxable guest-nights x rate, USD",
        "DATE_FILED            date the return was received, MM/DD/YYYY",
        "",
        "Stays booked through a marketplace platform that collects and remits the fee under a collection agreement",
        "(Lakeward Stays, Kettle & Pine) are remitted by the platform and are not reported on the property's return.",
        "The platforms' remittance files are provided as each platform sends them.",
    ]
    with open(path, "w", newline="") as f:
        f.write("\r\n".join(lines) + "\r\n")


# ------------------------------------------------------------------------------- files kept for other work

def traffic_csv(path):
    """The county highway department's two permanent count stations at the basin's entries: average daily traffic
    by month, both directions."""
    r = W.rng(351)
    rows = []
    shape = [0.38, 0.41, 0.44, 0.52, 0.78, 1.0, 1.32, 1.24, 0.93, 0.74, 0.55, 0.62]
    for st, loc, base in (("ATR 214", "CSAH 12 at the Quill River bridge", 4120),
                          ("ATR 219", "TH 34, 0.6 mi west of Sorrelton", 6880)):
        for (y, m) in W.month_iter(dt.date(2024, 1, 1), dt.date(2026, 9, 30)):
            f = {2024: 0.98, 2025: 1.0, 2026: 1.02}[y]
            adt = base * shape[m - 1] * f * (1 + r.normal(0, 0.03))
            rows.append([st, loc, "%d-%02d" % (y, m), int(round(adt)),
                         round(100 * (0.07 + 0.02 * r.random()), 1), W.days_in(y, m) - int(r.integers(0, 3))])
    write_csv(path, ["STATION", "LOCATION", "MONTH", "AVG_DAILY_TRAFFIC", "PCT_HEAVY_COMMERCIAL", "DAYS_COUNTED"], rows)


def weather_csv(path):
    """The cooperative observer station at Sorrelton: daily maximum and minimum temperature, precipitation,
    snowfall and snow depth."""
    r = W.rng(361)
    rows = []
    d = dt.date(2025, 1, 1)
    while d <= dt.date(2026, 9, 30):
        doy = d.timetuple().tm_yday
        tmean = 41 - 31 * np.cos(2 * np.pi * (doy - 17) / 365.25) + r.normal(0, 7)
        rng_ = 18 + 4 * r.random()
        tmax, tmin = tmean + rng_ / 2, tmean - rng_ / 2
        p = r.random() < (0.22 + 0.12 * np.sin(2 * np.pi * (doy - 80) / 365.25))
        pr = round(float(r.gamma(0.9, 0.28)), 2) if p else 0.0
        snow = round(pr * 11, 1) if tmax < 34 and pr else 0.0
        rows.append([d.isoformat(), int(round(tmax)), int(round(tmin)), "%.2f" % pr, "%.1f" % snow,
                     "" if not (d.month in (11, 12, 1, 2, 3)) else int(max(0, 10 + 8 * np.cos(2 * np.pi * (doy - 30) / 365.25) + r.normal(0, 3)))])
        d += dt.timedelta(days=1)
    write_csv(path, ["DATE", "TMAX_F", "TMIN_F", "PRCP_IN", "SNOW_IN", "SNWD_IN"], rows)
