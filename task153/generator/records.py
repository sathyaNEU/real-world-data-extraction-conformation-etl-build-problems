"""The data files, each in the layout of the system that writes it."""
from __future__ import annotations

import datetime as dt
import math

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import common as K
import world as WD

F_DAYS = "vehicle_days_2024-09-01_2026-08-27.csv"
F_GEO = "geofence_events_2026-03-01_2026-08-27.csv"
F_DEV = "telematics_device_assignments.csv"
F_UNITS = "fleet_units_2026-08.xlsx"
F_FMS = "fms_island_transactions_2025.csv"
F_WEST = "riverbend_direct_bill_2024-09_2026-08.csv"
F_CENTRAL = "crossroads_transactions_2024-09_2026-08.xlsx"
F_EAST = "smpm_card_activity_2024-09_2026-08.txt"
F_DELIV = "overton_deliveries_2025.csv"
F_INV = "overton_invoices_2025.csv"
F_CRED = "overton_credit_memos_2025.csv"
F_RACK = "overton_rack_postings_2024-09_2026-08.csv"
F_TANKS = "yard_tank_register.xlsx"
F_IFTA = "ifta_returns_2025Q3-2026Q2.xlsx"

DAY_COLS = ["Device Serial", "Vehicle", "Day", "TZ", "First Ignition", "First Lat", "First Lon", "Last Ignition Off",
            "Last Lat", "Last Lon", "Distance (mi)", "Engine Hours", "Idle Hours", "Fuel Used (gal)", "Odometer Start",
            "Odometer End"]
GEO_COLS = ["Event Time", "Device Serial", "Vehicle", "Geofence", "Event"]
DEV_COLS = ["Device Serial", "Vehicle", "Installed", "Removed"]
FMS_COLS = ["Txn", "Site", "Pump", "Fob", "Unit", "Date", "Time", "Gallons", "Odometer", "Product"]
WEST_COLS = ["TRAN_ID", "TRAN_DATE_TIME", "SITE_NO", "SITE_NAME", "SITE_CITY", "SITE_ST", "CARD_NO", "UNIT_NO",
             "DRIVER_NO", "ODOMETER", "PROD_CD", "PROD_DESC", "QTY", "PPG", "FET", "SET", "NET_AMT", "TOTAL",
             "REF_TRAN_ID"]
CENTRAL_COLS = ["Reference", "Transaction Date", "Transaction Time", "Post Date", "Card Number", "Vehicle ID",
                "Driver ID", "Odometer", "Merchant ID", "Merchant Name", "City", "State", "Product", "Quantity",
                "Unit Price", "Fuel Amount", "Federal Tax", "State Tax", "Network Fee", "Total", "Reverses"]
# a site or merchant posts a day's sales twice; the programme credits the duplicates later (date of the sales, date of
# the credit): Riverbend by credit rows, Crossroads by reversals, SMPM by credit records in a later batch
DUP_EVENTS = {
    "West": [(dt.date(2026, 4, 30), (dt.date(2026, 5, 5), 10.23)), (dt.date(2026, 6, 30), (dt.date(2026, 7, 7), 9.87))],
    "Central": [(dt.date(2026, 5, 29), (dt.date(2026, 6, 2), 9.24)), (dt.date(2026, 6, 30), (dt.date(2026, 7, 2), 14.6))],
    "East": [(dt.date(2026, 5, 29), (dt.date(2026, 6, 9), 11.08)), (dt.date(2026, 6, 30), (dt.date(2026, 7, 14), 10.4))],
}
DELIV_COLS = ["Ticket", "Terminal BOL", "Terminal", "Lifted (CT)", "Delivered (CT)", "Ship To", "Product",
              "BOL Net Gal", "Drop Gross Gal", "Temp F", "Truck", "Driver"]
INV_COLS = ["Invoice", "Invoice Date", "Ship To", "Terminal BOL", "Line", "Item", "Class", "Qty", "Unit Price",
            "Amount"]
CRED_COLS = ["Credit Memo", "Credit Date", "Ref Invoice", "Ship To", "Terminal BOL", "Line", "Item", "Class", "Qty",
             "Unit Price", "Amount"]
ITEM_CLASS = {"ULSD #2 CLEAR": "PRODUCT", "FREIGHT ZONE 3": "FREIGHT", "SPLIT DROP CHARGE": "SERVICE",
              "DELIVERY WAIT TIME": "SERVICE",
              "FEDERAL EXCISE TAX": "TAX", "TN DIESEL TAX": "TAX", "TN ENVIRONMENTAL ASSURANCE FEE": "TAX",
              "TN PETROLEUM SPECIAL TAX": "TAX"}
RACK_COLS = ["Effective Date", "Terminal", "Product", "Overton Posted", "TriState Contract Avg"]

ACCT_OF = {y: K.YARD[y]["account"] for y in K.YARDS}


def vname(u):
    """The telematics name each acquired company's administrator gave its vehicles."""
    acct = ACCT_OF[u.yard]
    body = {"van": "SPRINTER", "box": "BOX", "daycab": "DAYCAB", "sleeper": "SLPR"}[u.body]
    if acct == "West":
        return "D%d %s" % (u.unit, body)
    if acct == "Central":
        return "KSC-%d" % u.unit
    return "HSS %d %s" % (u.unit, body)


# ------------------------------------------------------------------------------------------------- devices
def devices(W):
    """One telematics device per vehicle; eight units had a failed device replaced in March and April 2026."""
    g = K.rng("devices")
    out = {}
    W.rename = {}
    pool = [u for u in W.units if u.status == "Active"]
    swap_idx = set(int(i) for i in g.choice(len(pool), size=8, replace=False))
    for i, u in enumerate(W.units):
        s1 = K.token("dev", u.unit, n=10).upper()
        inst = dt.date(2023, int(g.integers(2, 6)), int(g.integers(1, 28)))
        if u.status == "Sold":
            out[u.unit] = [(s1, inst, u.sold)]
        elif u in pool and pool.index(u) in swap_idx:
            sw = dt.date(2026, int(g.integers(3, 5)), int(g.integers(2, 27)))
            s2 = K.token("dev2", u.unit, n=10).upper()
            out[u.unit] = [(s1, inst, sw), (s2, sw, None)]
            # a new device reports under its serial until the administrator names it
            W.rename[u.unit] = (sw, sw + dt.timedelta(days=int(g.integers(2, 10))), s2)
        else:
            out[u.unit] = [(s1, inst, None)]
    W.dev = out
    return out


def vname_on(W, u, d):
    r = W.rename.get(u.unit)
    if r and r[0] <= d < r[1]:
        return r[2]
    return vname(u)


def serial_on(W, u, d):
    for (s, a, b) in W.dev[u.unit]:
        if a <= d and (b is None or d < b):
            return s
    return W.dev[u.unit][-1][0]


def dev_rows(W):
    for u in W.units:
        for (s, a, b) in W.dev[u.unit]:
            yield [s, vname(u), a.isoformat(), b.isoformat() if b else ""]


# ------------------------------------------------------------------------------------------------- vehicle days
def day_rows(W):
    rows = []
    for u in W.units:
        by = {}
        for leg in u.legs:
            by.setdefault(leg[0].date(), []).append(leg)
        g = K.rng("days", u.unit)
        for d in sorted(by):
            L = by[d]
            first, last = L[0], L[-1]
            lat0, lon0 = WD.place_ll(first[1])
            lat1, lon1 = WD.place_ll(last[3])
            miles = sum(x[5] for x in L)
            fuel = sum(x[4] for x in L)
            drive_h = sum((x[2] - x[0]).total_seconds() for x in L) / 3600.0
            idle = drive_h * float(g.uniform(0.07, 0.16)) + (float(g.uniform(0.4, 1.3)) if u.body == "sleeper" and
                                                              last[3][0] == "STOP" else 0.0)
            eng = drive_h * float(g.uniform(0.80, 0.92)) + idle
            # engine-reported fuel reads a little high against what the pump puts in, by unit
            ecu = fuel * (1.0 + 0.012 * math.sin(u.unit))
            rows.append([serial_on(W, u, d), vname_on(W, u, d), d.isoformat(), "CT" if u.tz is K.CENTRAL else "ET",
                         first[0].strftime("%H:%M"), "%.5f" % (lat0 + float(g.normal(0, 0.0004))),
                         "%.5f" % (lon0 + float(g.normal(0, 0.0004))), last[2].strftime("%H:%M"),
                         "%.5f" % (lat1 + float(g.normal(0, 0.0004))), "%.5f" % (lon1 + float(g.normal(0, 0.0004))),
                         "%.1f" % miles, "%.1f" % eng, "%.1f" % idle, "%.1f" % ecu, "%.1f" % first[6],
                         "%.1f" % (first[6] + miles)])
    rows.sort(key=lambda r: (r[2], r[1]))
    return rows


# ------------------------------------------------------------------------------------------------- geofence events
GEOFENCE = {"MEM": "KSC Memphis Yard", "JXN": "KSC Jackson Yard", "NSH": "KSC Nashville Yard",
            "CKV": "KSC Cookeville Yard", "KNX": "KSC Knoxville Yard", "TRI": "KSC Blountville Yard",
            "SPARTA": "Sparta Lot", "CROSSVILLE": "Crossville Lot"}


def geo_rows(W):
    a = dt.datetime(K.GEO_START.year, K.GEO_START.month, K.GEO_START.day, tzinfo=K.CENTRAL)
    b = dt.datetime(K.HIST_END.year, K.HIST_END.month, K.HIST_END.day, 23, 59, tzinfo=K.CENTRAL)
    rows = []
    for u in W.units:
        g = K.rng("geo", u.unit)
        for (te, tx, place) in u.visits:
            name = GEOFENCE[place[1]]
            ent = te - dt.timedelta(seconds=int(g.integers(20, 160)))
            if a <= ent <= b:
                rows.append((K.to_utc(ent), serial_on(W, u, ent.date()), vname_on(W, u, ent.date()), name, "Enter"))
            if tx is not None:
                ex = tx + dt.timedelta(seconds=int(g.integers(30, 200)))
                if a <= ex <= b:
                    rows.append((K.to_utc(ex), serial_on(W, u, ex.date()), vname_on(W, u, ex.date()), name, "Exit"))
        for (te, tx, name) in u.cust:
            if a <= te <= b:
                rows.append((K.to_utc(te), serial_on(W, u, te.date()), vname_on(W, u, te.date()), name, "Enter"))
                rows.append((K.to_utc(tx), serial_on(W, u, tx.date()), vname_on(W, u, tx.date()), name, "Exit"))
    rows.sort(key=lambda r: (r[0], r[2], r[4]))
    return [[r[0].strftime("%Y-%m-%dT%H:%M:%SZ"), r[1], r[2], r[3], r[4]] for r in rows]


# ------------------------------------------------------------------------------------------------- the unit list
# how each company's fleet administrator wrote the make and model (the model code is the maintenance system's)
MAKE_MODEL = {
    "West": {"SPR25": "MERCEDES SPRINTER 2500 170WB", "NRR19": "ISUZU NRR 19.5K BOX", "M2B26": "FREIGHTLINER M2-106 26FT",
             "CAS1D": "FREIGHTLINER CASCADIA 116 DAY", "T68SL": "KENWORTH T680 76IN SLPR"},
    "Central": {k: v[0] for k, v in K.MODELS.items()},
    "East": {"SPR25": "Sprinter 2500 Cargo (MB)", "NRR19": "Isuzu NRR", "M2B26": "M2 106 Box 26'",
             "CAS1D": "Cascadia Day Cab", "T68SL": "KW T680 Sleeper 76\""},
}


def unit_rows(W):
    out = []
    for u in W.units:
        out.append([u.unit, K.YARD[u.yard]["branch"], K.YARD[u.yard]["name"], u.year,
                    MAKE_MODEL[ACCT_OF[u.yard]][u.model], u.model,
                    {"van": "Cargo van", "box": "Straight truck", "daycab": "Tractor", "sleeper": "Tractor"}[u.body],
                    u.vin8, u.status, u.in_service, u.sold])
    return out


UNIT_COLS = ["Unit", "Branch", "Location", "Year", "Make/Model", "Model Code", "Class", "VIN (last 8)", "Status",
             "In Service", "Disposed"]
SPEC_COLS = ["Model Code", "Description", "Fuel Tank (gal)", "Tank Config", "DEF Tank (gal)", "GVWR (lb)"]


def spec_rows():
    return [
        ["SPR25", "Mercedes-Benz Sprinter 2500 cargo 170, 2.0L diesel", 24.5, "single", 5.3, 9050],
        ["NRR19", "Isuzu NRR 19,500 GVW, 20 ft dry box", 40.0, "single", 6.6, 19500],
        ["M2B26", "Freightliner M2 106, 26 ft dry box, liftgate", 56.0, "single", 7.0, 33000],
        ["CAS1D", "Freightliner Cascadia 116 day cab", 200.0, "2 x 100", 13.0, 52000],
        ["T68SL", "Kenworth T680 76 in mid-roof sleeper", 300.0, "2 x 150", 23.0, 52000],
    ]


# ------------------------------------------------------------------------------------------------- the island, 2025
def fms_rows(W):
    rows = []
    for u in W.units:
        if u.yard not in K.PROG:
            continue
        g = K.rng("fms", u.unit)
        fob = "%s%04d" % (u.yard[0], 1000 + (u.unit % 1000))
        for f in u.fills:
            if f["kind"] != "island":
                continue
            rows.append([f["t"], u.yard, int(g.integers(1, 3)), fob, u.unit, f["gal"], f["odo"]])
    rows.sort(key=lambda r: r[0])
    out = []
    seq = {"JXN": 20417, "KNX": 31102}
    resend = dt.date(2025, 7, 23)       # the Knoxville controller's modem outage: the day's buffer was uploaded twice
    again = []
    for r in rows:
        y = r[1]
        seq[y] += 1
        row = [seq[y], "%s-ISL1" % y, r[2], r[3], r[4], r[0].strftime("%m/%d/%Y"), r[0].strftime("%H:%M"),
               "%.1f" % r[5], "%.0f" % r[6], "ULSD"]
        out.append(row)
        if y == "KNX" and r[0].date() == resend:
            again.append(list(row))
    k = max(i for i, r in enumerate(out) if r[1] == "KNX-ISL1" and r[5] == resend.strftime("%m/%d/%Y"))
    out[k + 1:k + 1] = again
    return out


# ------------------------------------------------------------------------------------------------- card prices
def card_price(W, acct, station, t_local):
    """Pre-tax price per gallon on the account's terms: the rack average for the station's terminal for the day the
    fill was pumped, plus the margin."""
    term = WD.station_terminal(station)
    avg = W.R[(term, t_local.date())][1]
    return round(avg + K.TERMS[acct]["margin"], 4)


def def_price(t_local):
    return round(3.38 + 0.12 * math.sin(t_local.toordinal() / 47.0), 3)


def card_fills(W, acct):
    """Every card fill (diesel and DEF) by the account's vehicles, in pumping order."""
    out = []
    for u in W.units:
        if ACCT_OF[u.yard] != acct:
            continue
        for f in u.fills:
            if f["kind"] in ("card", "def"):
                out.append((f["t"], u, f))
    out.sort(key=lambda x: (x[0], x[1].unit))
    return out


def business_date(station, t_local):
    """The networks close their business day at 10 pm (Crossroads on Central time, SMPM's sites on their own Eastern
    clock); a sale made at 10 pm or later carries the next day's date."""
    if t_local.hour >= 22:
        return t_local.date() + dt.timedelta(days=1)
    return t_local.date()


def unit_prompt(u, g):
    r = g.random()
    if r < 0.86:
        return str(u.unit)
    if r < 0.93:
        return "0%d" % u.unit
    if r < 0.97:
        return "%d " % u.unit
    return "%d %02d" % (u.unit // 100, u.unit % 100)


def west_rows(W):
    g = K.rng("west")
    rows = []
    tid = 7731042
    for (t, u, f) in card_fills(W, "West"):
        s = WD.ST[f["station"]]
        tid += int(g.integers(1, 37))
        utc = K.to_utc(t)
        if f["kind"] == "def":
            cd, desc, ppg, fet, sett = "19", "DEF BULK", def_price(t), 0.0, 0.0
        else:
            cd, desc = "01", "ULSD #2"
            ppg = card_price(W, "West", f["station"], t)
            fet, sett = K.FET, K.STATE_TAX[s["st"]]
        qty = f["gal"]
        net = round(qty * ppg, 2)
        tot = round(net + qty * (fet + sett), 2)
        odo = int(f["odo"]) if g.random() > 0.03 else int(f["odo"]) + int(g.choice([-1000, 1000, 10000, -90]))
        rows.append([tid, utc.strftime("%Y-%m-%d %H:%M:%S"), f["station"], "RIVERBEND #%s" % f["station"],
                     s["city"].upper(), s["st"], "XXXXXXXXXXX%s" % u.card, unit_prompt(u, g), u.driver, odo, cd, desc,
                     "%.3f" % qty, "%.4f" % ppg, "%.2f" % round(qty * fet, 2), "%.2f" % round(qty * sett, 2),
                     "%.2f" % net, "%.2f" % tot, ""])
    # a site that re-sent a day's sales: the duplicates, and the credits that reverse them on a later invoice
    gd = K.rng("west-dups")
    W.dups = getattr(W, "dups", {})
    local = lambda r: dt.datetime.strptime(r[1], "%Y-%m-%d %H:%M:%S").replace(tzinfo=K.UTC).astimezone(K.CENTRAL)
    top = max(r[0] for r in rows)
    extra = []
    for (day, (cday, chour)) in DUP_EVENTS["West"]:
        day_rows = [r for r in rows if local(r).date() == day and r[10] == "01"]
        gal = {}
        for r in day_rows:
            gal[r[2]] = gal.get(r[2], 0.0) + float(r[12])
        site = max(sorted(gal), key=lambda k: gal[k])
        dups = [r for r in rows if local(r).date() == day and r[2] == site]
        t_cr = K.to_utc(K.local_dt(cday, chour, K.CENTRAL))
        for i, r in enumerate(dups):
            top += int(gd.integers(3, 29))
            d = list(r)
            d[0] = top
            extra.append(d)
            top += int(gd.integers(3, 29))
            c = list(d)
            c[0] = top
            c[1] = (t_cr + dt.timedelta(seconds=int(37 * i + gd.integers(0, 30)))).strftime("%Y-%m-%d %H:%M:%S")
            for k in (12, 14, 15, 16, 17):
                c[k] = "-" + c[k]
            c[18] = d[0]
            extra.append(c)
        W.dups[("West", day)] = (site, sum(float(r[12]) for r in dups if r[10] == "01"))
    rows = sorted(rows + extra, key=lambda r: (r[1], r[0]))
    return rows


def central_rows(W):
    g = K.rng("central")
    rows = []
    for (t, u, f) in card_fills(W, "Central"):
        s = WD.ST[f["station"]]
        bd = business_date(f["station"], t)
        post = bd + dt.timedelta(days=int(g.choice([1, 1, 1, 2, 2, 3])))
        while post.weekday() >= 5:
            post += dt.timedelta(days=1)
        if post > K.HIST_END:
            post = None                      # still pending when the export was run
        if f["kind"] == "def":
            prod, ppg, fet, sett, fee = "DEF", def_price(t), 0.0, 0.0, 0.0
        else:
            prod = "Diesel"
            ppg = card_price(W, "Central", f["station"], t)
            fet, sett, fee = K.FET, K.STATE_TAX[s["st"]], K.TERMS["Central"]["fee"]
        qty = round(f["gal"], 3)
        amt = round(qty * ppg, 2)
        odo = int(f["odo"]) if g.random() > 0.04 else int(g.choice([0, 1, int(f["odo"]) // 10]))
        rows.append([None, bd, t.strftime("%H:%M"), post, "**** **** **** %s" % u.card[-4:], str(u.unit), u.driver,
                     odo, f["station"], s["name"], s["city"], s["st"], prod, qty, ppg, amt, round(qty * fet, 2),
                     round(qty * sett, 2), round(qty * fee, 2), round(amt + qty * (fet + sett + fee), 2), None])
    gr = K.rng("central-ref")
    ref = 40817200
    for r in rows:
        ref += int(gr.integers(1, 9))
        r[0] = "XF%d" % ref
    # a merchant whose day's sales were posted twice: the duplicates, and the reversals that cancel them
    W.dups = getattr(W, "dups", {})
    extra = []
    for (day, (rday, rhour)) in DUP_EVENTS["Central"]:
        gal = {}
        for r in rows:
            if r[1] == day and r[12] == "Diesel":
                gal[r[8]] = gal.get(r[8], 0.0) + r[13]
        merchant = max(sorted(gal), key=lambda k: gal[k])
        dups = [r for r in rows if r[1] == day and r[8] == merchant]
        for i, r in enumerate(dups):
            ref += int(gr.integers(1, 9))
            d = list(r)
            d[0] = "XF%d" % ref
            extra.append(d)
        for i, d in enumerate(list(extra[-len(dups):])):
            ref += int(gr.integers(1, 9))
            c = list(d)
            c[0] = "XF%d" % ref
            c[1] = rday
            c[2] = "%02d:%02d" % divmod(int(rhour * 60) + 3 * i, 60)
            c[3] = rday + dt.timedelta(days=1)
            for k in (13, 15, 16, 17, 18, 19):
                c[k] = -c[k]
            c[20] = d[0]
            extra.append(c)
        W.dups[("Central", day)] = (merchant, sum(r[13] for r in dups if r[12] == "Diesel"))
    rows = sorted(rows + extra, key=lambda r: (r[1], r[2], r[0]))
    return rows


# the marketers' group's fixed-width export: batch header, detail and trailer records
def east_lines(W):
    g = K.rng("east")
    fills = card_fills(W, "East")
    weeks = {}
    for (t, u, f) in fills:
        bd = business_date(f["station"], t)
        monday = bd - dt.timedelta(days=bd.weekday())
        weeks.setdefault(monday, []).append((bd, t, u, f))
    lines = []
    batch = 88104
    resend = dt.date(2026, 7, 6)
    # a member site whose day's sales went out twice in its week's batch; the group credits the duplicates in a later
    # week's batch with C records carrying the date the credit was made
    dup_day = {e[0]: e[1] for e in DUP_EVENTS["East"]}
    credit_week = {}
    W.dups = getattr(W, "dups", {})
    for day, (cday, chour) in dup_day.items():
        gal = {}
        for (bd, t, u, f) in weeks.get(day - dt.timedelta(days=day.weekday()), []):
            if bd == day and f["kind"] != "def":
                gal[f["station"]] = gal.get(f["station"], 0.0) + f["gal"]
        site = max(sorted(gal), key=lambda k: gal[k])
        dup_day[day] = (site, cday, chour)
        credit_week.setdefault(cday - dt.timedelta(days=cday.weekday()), []).append(day)
    sent = {}
    for monday in sorted(weeks):
        if monday + dt.timedelta(days=7) > K.EXPORT_DATE:
            continue                         # this week's batch goes out the Monday after the pull
        batch += 1
        recs = sorted(weeks[monday], key=lambda x: (x[0], x[1], x[2].unit))
        dups = []
        for day, (site, cday, chour) in dup_day.items():
            if day - dt.timedelta(days=day.weekday()) == monday:
                dups += [x for x in recs if x[0] == day and x[3]["station"] == site]
        credits = []
        for day in credit_week.get(monday, []):
            site, cday, chour = dup_day[day]
            credits += [(cday, chour, x) for x in sent[day]]
        block = east_block(W, batch, monday, recs, g, dups=dups, credits=credits)
        for day, (site, cday, chour) in dup_day.items():
            if day - dt.timedelta(days=day.weekday()) == monday:
                sent[day] = W.east_dup_lines
                W.dups[("East", day)] = (site, sum(int(l[59:68]) / 1000.0 for l in W.east_dup_lines if l[55:59] == "DSL2"))
        lines.extend(block)
        if monday == resend:
            # the week's file was transmitted again the following Monday after an acknowledgement time-out
            batch += 1
            again = [l for l in block]
            again[0] = again[0][:1] + "%07d" % batch + again[0][8:]
            again[-1] = again[-1][:1] + "%07d" % batch + again[-1][8:]
            lines.extend(again)
    return lines


def east_block(W, batch, monday, recs, g, dups=(), credits=()):
    out = []
    out.append("H%07d%s%-10s%-30s" % (batch, monday.strftime("%Y%m%d"), "HSS0417", "HOLSTON SANITARY SUPPLY"))
    tot_g = 0
    n = 0
    dup_keys = {id(x[3]) for x in dups}
    W.east_dup_lines = []
    originals = []
    for (bd, t, u, f) in recs:
        s = WD.ST[f["station"]]
        if f["kind"] == "def":
            prod, ppg, tax = "DEF ", def_price(t), 0.0
        else:
            prod = "DSL2"
            ppg = card_price(W, "East", f["station"], t)
            tax = K.FET + K.STATE_TAX[s["st"]]
        gal = int(round(f["gal"] * 1000))
        tot_g += gal
        n += 1
        unit = str(u.unit) if g.random() < 0.9 else "HSS%d" % u.unit
        odo = int(f["odo"]) if g.random() > 0.05 else 0
        out.append("D%07d%06d%s%s%-6s%-8s%-8s%07d%-4s%09d%07d%07d%-24s%-2s" % (
            batch, n, bd.strftime("%Y%m%d"), t.strftime("%H%M"), f["station"], unit[:8], u.card + "0", odo % 10000000,
            prod, gal, int(round(ppg * 10000)), int(round(tax * 10000)), s["name"][:24].upper(), s["st"]))
        if id(f) in dup_keys:
            originals.append(out[-1])
    for line in originals:                     # the site's day sent again, after the week's own records
        n += 1
        d = "D%07d%06d" % (batch, n) + line[14:]
        tot_g += int(line[59:68])
        out.append(d)
        W.east_dup_lines.append(d)
    for i, (cday, chour, line) in enumerate(credits):
        n += 1
        t_cr = K.local_dt(cday, chour + i * 0.04, K.EASTERN)
        c = "C%07d%06d%s%s" % (batch, n, cday.strftime("%Y%m%d"), t_cr.strftime("%H%M")) + line[26:108] + line[1:14]
        tot_g -= int(line[59:68])
        out.append(c)
    out.append("T%07d%06d%012d" % (batch, n, tot_g))
    return out


# ------------------------------------------------------------------------------------------------- Overton 2025
def deliv_rows(W):
    g = K.rng("delivrows")
    rows = []
    trucks = {"JXN": ["T-114", "T-121", "T-127"], "KNX": ["T-208", "T-212"]}
    drivers = {"JXN": ["D-0471", "D-0538", "D-0612"], "KNX": ["D-0705", "D-0743"]}
    for e in W.deliveries:
        b = e["bol"]
        y = b["yard"]
        lift_ct = b["t_lift"].astimezone(K.CENTRAL)
        drop_ct = e["t_drop"].astimezone(K.CENTRAL)
        k = int(g.integers(0, len(trucks[y])))
        rows.append([e["ticket"], b["bol"], b["terminal"].upper(), lift_ct.strftime("%m/%d/%Y %H:%M"),
                     drop_ct.strftime("%m/%d/%Y %H:%M"), "KEEBLE %s TANK 1" % y, "ULSD #2 CLR",
                     "%.0f" % b["net"], "%.1f" % e["gross"], "%.1f" % b["temp"], trucks[y][k], drivers[y][k]])
    rows.sort(key=lambda r: r[0])
    return rows


def fmt_lines(rows, qty_col, price_col, amt_col):
    out = []
    for r in rows:
        r = [x.isoformat() if hasattr(x, "isoformat") else x for x in r]
        q = r[qty_col]
        r[qty_col] = "%d" % q if float(q).is_integer() else "%.1f" % q
        r[price_col] = "%.4f" % r[price_col]
        r[amt_col] = "%.2f" % r[amt_col]
        out.append(r)
    return out


def invoices(W):
    """One invoice per terminal bill (a load), dated its first drop; three July 2025 Knoxville loads were billed with a
    freight-zone charge that did not apply, credited and rebilled on 21 July."""
    g = K.rng("invoices")
    by_bol = {}
    for e in W.deliveries:
        by_bol.setdefault(e["bol"]["bol"], []).append(e)
    inv_no = 260410
    invs, creds = [], []
    rebill = []
    knx = sorted([v for v in by_bol.values() if v[0]["bol"]["yard"] == "KNX"], key=lambda v: v[0]["t_drop"])
    july = [v for v in knx if v[0]["t_drop"].month == 7 and v[0]["t_drop"].day < 21]
    err = set(v[0]["bol"]["bol"] for v in july)
    # the transport waited at a locked gate on two mornings (billed by the half hour)
    order = sorted(by_bol, key=lambda k: by_bol[k][0]["t_drop"])
    early = sorted(order, key=lambda k: by_bol[k][0]["t_drop"].astimezone(K.CENTRAL).time())
    wait = {}
    for y_, halves in (("JXN", 1), ("KNX", 2)):
        k = next(k for k in early if by_bol[k][0]["bol"]["yard"] == y_)
        wait[k] = halves
    for bolno in sorted(by_bol, key=lambda k: by_bol[k][0]["t_drop"]):
        v = by_bol[bolno]
        b = v[0]["bol"]
        y = b["yard"]
        st = WD.posting_in_effect(W.R, b["terminal"], b["t_lift"])[0]
        price = round(st + K.PROMO_2025[y], 4)
        idate = v[0]["t_drop"].date()
        inv_no += int(g.integers(1, 12))
        lines = [("ULSD #2 CLEAR", b["net"], price)]
        if bolno in err:
            lines.append(("FREIGHT ZONE 3", b["net"], K.FREIGHT_ZONE_ERR))
        if len(v) > 1:
            lines.append(("SPLIT DROP CHARGE", len(v) - 1, K.SPLIT_DROP_CHARGE))
        if bolno in wait:
            lines.append(("DELIVERY WAIT TIME", wait[bolno], 47.50))
        lines += [("FEDERAL EXCISE TAX", b["net"], K.FET), ("TN DIESEL TAX", b["net"], K.STATE_TAX["TN"]),
                  ("TN ENVIRONMENTAL ASSURANCE FEE", b["net"], 0.004), ("TN PETROLEUM SPECIAL TAX", b["net"], 0.01)]
        for i, (item, q, p) in enumerate(lines, 1):
            invs.append([inv_no, idate, "KEEBLE %s TANK 1" % y, bolno, i, item, ITEM_CLASS[item], q, p, round(q * p, 2)])
        if bolno in err:
            rebill.append((inv_no, bolno, b, price, idate, len(v)))
    cm = 9071
    for (orig, bolno, b, price, idate, nd) in rebill:
        cdate = dt.date(2025, 7, 21)
        cm += int(g.integers(1, 5))
        lines = [l for l in invs if l[0] == orig]
        for i, l in enumerate(lines, 1):
            creds.append(["CM%05d" % cm, cdate, orig, l[2], bolno, i, l[5], l[6], l[7], l[8], -l[9]])
        inv_no += int(g.integers(1, 6))
        new = [("ULSD #2 CLEAR", b["net"], price)]
        if nd > 1:
            new.append(("SPLIT DROP CHARGE", nd - 1, K.SPLIT_DROP_CHARGE))
        if bolno in wait:
            new.append(("DELIVERY WAIT TIME", wait[bolno], 47.50))
        new += [("FEDERAL EXCISE TAX", b["net"], K.FET), ("TN DIESEL TAX", b["net"], K.STATE_TAX["TN"]),
                ("TN ENVIRONMENTAL ASSURANCE FEE", b["net"], 0.004), ("TN PETROLEUM SPECIAL TAX", b["net"], 0.01)]
        for i, (item, q, p) in enumerate(new, 1):
            invs.append([inv_no, cdate, "KEEBLE KNX TANK 1", bolno, i, item, ITEM_CLASS[item], q, p, round(q * p, 2)])
    invs.sort(key=lambda r: (r[0], r[4]))
    W.rebill = rebill
    return invs, creds


def rack_rows(W):
    out = []
    for d in K.days(dt.date(2024, 9, 1), K.HIST_END + dt.timedelta(days=1)):
        for t in ("Memphis", "Nashville", "Knoxville"):
            ov, av = W.R[(t, d)]
            out.append([d.isoformat(), t, "ULSD #2", "%.4f" % ov, "%.4f" % av])
    return out


# ------------------------------------------------------------------------------------------------- workbooks
HEAD_FILL = "D9E1EA"


def write_book(path, sheets):
    """sheets: (title, columns, rows, widths, {column number: number format}) each; the header bold on a fill, the
    panes frozen under it."""
    wb = Workbook()
    first = True
    for (title, cols, rows, widths, fmts) in sheets:
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = title
        ws.append(cols)
        for c in range(1, len(cols) + 1):
            ws.cell(row=1, column=c).font = Font(bold=True)
            ws.cell(row=1, column=c).fill = PatternFill("solid", fgColor=HEAD_FILL)
            ws.cell(row=1, column=c).alignment = Alignment(wrap_text=True, vertical="top")
        for row in rows:
            ws.append(row)
        for c, w in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(c)].width = w
        for c, fmt in fmts.items():
            for rr in range(2, len(rows) + 2):
                ws.cell(row=rr, column=c).number_format = fmt
        ws.freeze_panes = "A2"
    wb.save(path)
    return sum(len(s[2]) for s in sheets)


def write_units(path, W):
    return write_book(path, [
        ("Units", UNIT_COLS, unit_rows(W), [7, 7, 12, 6, 38, 11, 14, 12, 8, 11, 11],
         {10: "mm/dd/yyyy", 11: "mm/dd/yyyy"}),
        ("Model Specs", SPEC_COLS, spec_rows(), [11, 50, 14, 11, 13, 11], {})])


def write_central(path, W):
    rows = central_rows(W)
    return write_book(path, [("Transactions", CENTRAL_COLS, rows,
                              [12, 12, 10, 11, 20, 10, 9, 10, 11, 30, 14, 6, 9, 10, 10, 11, 10, 10, 10, 11, 12],
                              {2: "mm/dd/yyyy", 4: "mm/dd/yyyy", 14: "0.000", 15: "0.0000", 16: "#,##0.00",
                               17: "#,##0.00", 18: "#,##0.00", 19: "#,##0.00", 20: "#,##0.00"})])


TANK_COLS = ["Yard", "Branch", "Tank", "Product", "Capacity (gal)", "Overfill Alarm (gal)", "Unpumpable (gal)",
             "Installed", "Island", "Meter Last Calibrated", "Status", "Status Since", "Last Dip", "Dip (gal)"]


def tank_rows(W):
    g = K.rng("tanks")
    inst = {"MEM": dt.date(2015, 6, 9), "JXN": dt.date(2016, 4, 26), "NSH": dt.date(2012, 10, 3),
            "CKV": dt.date(2017, 8, 14), "KNX": dt.date(2014, 5, 20), "TRI": dt.date(2018, 9, 11)}
    cal = {"MEM": dt.date(2023, 3, 7), "JXN": dt.date(2025, 2, 25), "NSH": dt.date(2023, 3, 9),
           "CKV": dt.date(2023, 3, 10), "KNX": dt.date(2025, 5, 28), "TRI": dt.date(2023, 3, 14)}
    since = {"MEM": dt.date(2023, 4, 3), "JXN": W.run_out["JXN"] + dt.timedelta(days=1), "NSH": dt.date(2023, 4, 3),
             "CKV": dt.date(2023, 4, 3), "KNX": W.run_out["KNX"] + dt.timedelta(days=1), "TRI": dt.date(2023, 4, 17)}
    tank_id = {"MEM": "T1", "JXN": "T1", "NSH": "AST-31", "CKV": "AST-35", "KNX": "41-1", "TRI": "46-1"}
    island = {"MEM": "1 hose", "JXN": "1 hose, 2 nozzles", "NSH": "2 hoses", "CKV": "1 hose", "KNX": "1 hose, 2 nozzles",
              "TRI": "1 hose"}
    out = []
    for y in K.YARDS:
        cap, alarm, bottom = K.TANKS[y]
        dip = W.tank_end[y] if y in W.tank_end else bottom + float(g.uniform(-60.0, 90.0))
        out.append([K.YARD[y]["name"], K.YARD[y]["branch"], tank_id[y], "ULSD", cap, alarm, bottom, inst[y],
                    island[y], cal[y], "Standby", since[y], dt.date(2026, 8, 24), int(round(dip))])
    return out


def write_tanks(path, W):
    return write_book(path, [("Tanks", TANK_COLS, tank_rows(W), [11, 7, 5, 7, 10, 11, 11, 11, 16, 12, 9, 11, 11, 9],
                              {5: "#,##0", 6: "#,##0", 7: "#,##0", 8: "mm/dd/yyyy", 10: "mm/dd/yyyy",
                               12: "mm/dd/yyyy", 13: "mm/dd/yyyy", 14: "#,##0"})])


# ------------------------------------------------------------------------------------------------- IFTA (not used)
IFTA_COLS = ["Quarter", "Licensee", "IFTA Account", "Jurisdiction", "Total Miles", "Taxable Miles", "Fleet MPG",
             "Taxable Gallons", "Tax-Paid Gallons", "Net Taxable Gallons", "Tax Rate", "Tax Due (Credit)"]
IFTA_RATE = {"TN": 0.2740, "MS": 0.1800, "AR": 0.2850, "KY": 0.2660, "VA": 0.4030, "NC": 0.4050, "GA": 0.3690,
             "AL": 0.3100, "WV": 0.3570}
LICENSEE = {"West": ("Delta Paper & Chemical LLC", "TN-0049318"), "Central": ("Keeble Supply Co.", "TN-0031742"),
            "East": ("Holston Sanitary Supply Inc.", "TN-0057206")}
QUALIFIED = ("M2B26", "CAS1D", "T68SL")


def ifta_rows(W):
    quarters = [(2025, 3), (2025, 4), (2026, 1), (2026, 2)]
    miles, paid = {}, {}
    for u in W.units:
        if u.model not in QUALIFIED:
            continue
        acct = ACCT_OF[u.yard]
        for (t0, p0, t1, p1, f, mi, odo) in u.legs:
            q = (t0.year, (t0.month - 1) // 3 + 1)
            if q not in quarters:
                continue
            sts = [ST_OF(p0), ST_OF(p1)]
            for s_ in sts:
                miles[(q, acct, s_)] = miles.get((q, acct, s_), 0.0) + mi / 2.0
        for fl in u.fills:
            if fl["kind"] not in ("card", "island"):
                continue
            q = (fl["t"].year, (fl["t"].month - 1) // 3 + 1)
            if q not in quarters:
                continue
            s_ = "TN" if fl["kind"] == "island" else WD.ST[fl["station"]]["st"]
            paid[(q, acct, s_)] = paid.get((q, acct, s_), 0.0) + fl["gal"]
    out = []
    for q in quarters:
        for acct in K.ACCOUNTS:
            keys = sorted({k[2] for k in list(miles) + list(paid) if k[0] == q and k[1] == acct},
                          key=lambda x: (x != "TN", x))
            tm = sum(miles.get((q, acct, j), 0.0) for j in keys)
            tg = sum(paid.get((q, acct, j), 0.0) for j in keys)
            mpg = round(tm / tg, 2)
            for j in keys:
                m = int(round(miles.get((q, acct, j), 0.0)))
                tax_g = int(round(m / mpg))
                pd = int(round(paid.get((q, acct, j), 0.0)))
                net = tax_g - pd
                out.append(["%dQ%d" % q, LICENSEE[acct][0], LICENSEE[acct][1], j, m, m, mpg, tax_g, pd, net,
                            IFTA_RATE[j], round(net * IFTA_RATE[j], 2)])
    return out


def ST_OF(place):
    if place[0] == "STOP":
        return WD.ST[place[1]]["st"]
    return "TN"


def write_ifta(path, W):
    return write_book(path, [("Returns", IFTA_COLS, ifta_rows(W), [8, 28, 12, 11, 11, 11, 9, 12, 13, 13, 9, 13],
                              {5: "#,##0", 6: "#,##0", 7: "0.00", 8: "#,##0", 9: "#,##0", 10: "#,##0;-#,##0",
                               11: "0.0000", 12: "#,##0.00;-#,##0.00"})])
