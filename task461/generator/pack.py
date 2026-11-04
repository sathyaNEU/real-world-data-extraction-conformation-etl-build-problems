"""Each system's own record of the year, written the way that system writes it: the terminal management system's
two exports across the 1 July cutover, the dispatch system's delivery dockets in UTC, the tanker and tank registers,
the delivery sites, the vapour recovery unit's CEMS export and PLC event log, the tank gauging system's 06:00 AEST
dips, the ships' outturns, the control room shift log, the maintenance work orders and the airport weather."""
import csv
import datetime as dt
import io
import math

import numpy as np

import sim as S
import terminal as T
import world as W

D = dt.timedelta
CUTOVER_LOCAL = dt.datetime(2026, 7, 1)
SHADOW_FROM_LOCAL = dt.datetime(2026, 6, 29, 6, 0)


def write_csv(path, cols, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(cols)
    n = 0
    for r in rows:
        w.writerow(r)
        n += 1
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write(buf.getvalue())
    return n


def fmt_dmy(t):
    return t.strftime("%d/%m/%Y")


def iso_off(utc, hours):
    t = utc + D(hours=hours)
    return t.strftime("%Y-%m-%dT%H:%M:%S") + ("+%02d:00" % hours)


def secs(t):
    return t.replace(microsecond=0)


# ----------------------------------------------------------------------------------------------- unit identities
def identities(x, rng):
    """Plates as the legacy TMS saw them (two trailers re-registered in March), and the TMS tanker ids."""
    plate_hist = {}
    changes = {"BF-14": ("dog", dt.datetime(2026, 3, 9)), "OH-121": ("lead", dt.datetime(2026, 3, 23))}
    letters = "ABCDEFGHJKLMNPRSTUVWXYZ"
    for u in x["units"]:
        trailers = ["lead"] + (["dog"] if u.config == "B-double" else [])
        for i, tr in enumerate(trailers):
            cur = u.plates[i]
            hist = [(dt.datetime(2000, 1, 1), cur)]
            if u.uid in changes and changes[u.uid][0] == tr:
                old = "X%s%02d%s%s" % (letters[int(rng.integers(0, 23))], int(rng.integers(10, 99)),
                                        letters[int(rng.integers(0, 23))], letters[int(rng.integers(0, 23))])
                hist = [(dt.datetime(2000, 1, 1), old), (changes[u.uid][1], cur)]
            plate_hist[(u.uid, tr)] = hist
    return plate_hist


def plate_at(plate_hist, uid, tr, local):
    p = None
    for since, pl in plate_hist[(uid, tr)]:
        if local >= since:
            p = pl
    return p


def legacy_trailer_comp(u, comp):
    if u.config == "B-double":
        return ("lead", comp) if comp <= 5 else ("dog", comp - 5)
    return ("lead", comp)


# ----------------------------------------------------------------------------------------------- TMS exports
OLD_COLS = ["BOL_NO", "LINE", "LOAD_DATE", "LOAD_TIME", "BAY", "ARM", "PRODUCT", "TRAILER_REGO", "COMP", "GROSS_L",
            "TEMPERATURE", "VCF", "DENS15", "CARRIER", "CARD_NO"]
NEW_COLS = ["Transaction ID", "Loaded (local)", "Bay", "Arm", "Product", "Tanker", "Compartment", "Gross obs L",
            "Net 15C L", "Temp C", "Density 15 kg/m3", "Account", "Status"]
ARM = {"ULP": 1, "P95": 2, "P98": 3}


def tms_rows(x, y, rng, plate_hist):
    units = {u.uid: u for u in x["units"]}
    ours = [l for l in x["loads"] if l["terminal"] == "WARRENBY"]
    cards = {}
    for u in x["units"]:
        cards[u.uid] = ["%07d" % int(v) for v in rng.choice(np.arange(3300000, 3399999), size=3, replace=False)]
    old, new = [], []
    line_no = {}
    tid = [5_120_440]
    for l in ours:
        loc = W.to_local(l["utc"])
        if loc.year < 2026 or loc >= W.EXPORT_END_LOCAL:
            continue
        if W.in_tas_fault(l["bay"], loc):
            continue
        u = units[l["unit"]]
        arm = ARM.get(l["product"], 1 if (l["comp"] % 2) else 2)
        if loc < CUTOVER_LOCAL:
            tr, c = legacy_trailer_comp(u, l["comp"])
            line_no[l["bol"]] = line_no.get(l["bol"], 0) + 1
            old.append([l["bol"], line_no[l["bol"]], fmt_dmy(loc), loc.strftime("%H:%M:%S"), l["bay"], arm,
                        W.NAME_OLD_TAS[l["product"]], plate_at(plate_hist, u.uid, tr, loc), c, l["gross"],
                        "%.1f" % l["temp"], "%.4f" % l["vcf"], "%.1f" % S.DENSITY[l["product"]],
                        u.operator, cards[u.uid][int(rng.integers(0, 3))]])
        if loc >= SHADOW_FROM_LOCAL:
            tid[0] += int(rng.integers(1, 4))
            row = [tid[0], loc.strftime("%Y-%m-%d %H:%M:%S"), l["bay"], arm, W.NAME_NEW_TAS[l["product"]], u.tas_id,
                   l["comp"], l["gross"], l["net"], round(l["temp"], 1), S.DENSITY[l["product"]],
                   "BRENNOCK" if u.operator == "BRN" else "OAKHURST", "Complete"]
            if loc >= CUTOVER_LOCAL and rng.random() < 0.0062:
                # an aborted load: the transaction is cancelled and the compartment loaded again under a new id
                cancelled = list(row)
                cancelled[12] = "Cancelled"
                cancelled[1] = (loc - D(minutes=int(rng.integers(4, 9)))).strftime("%Y-%m-%d %H:%M:%S")
                cancelled[0] = tid[0]
                tid[0] += 1
                row[0] = tid[0]
                new.append(cancelled)
            new.append(row)
    return old, new


# ----------------------------------------------------------------------------------------------- dockets
DOCKET_COLS = ["docket_line", "trip_ref", "fleet_unit", "compartment", "product", "site_code", "litres_delivered",
               "vr1_hose", "arrived_at", "completed_at", "source_terminal", "source_doc", "bol_litres_15c", "driver_id"]


def docket_rows(x):
    rows = []
    n = 0
    manual = {}
    for d in sorted(x["drops"], key=lambda d: d["load_utc"]):
        if d["terminal"] == "WARRENBY" and W.in_tas_fault(d["bay"], W.to_local(d["load_utc"])) and d["ref"] not in manual:
            manual[d["ref"]] = "MB-%04d" % (412 + len(manual))
    for d in x["drops"]:
        if W.to_local(d["done"]) >= dt.datetime(2027, 1, 1):
            continue
        n += 1
        rows.append(["DL%07d" % (3_400_000 + n * 3 + (d["comp"] % 3)), "TR%06d" % (610_000 + d["trip"]), d["unit"],
                     d["comp"], W.NAME_DOCKET[d["product"]], d["site"], d["litres"], "Y" if d["vr"] else "",
                     iso_off(secs(d["arr"]), W.offset_h(d["arr"])), iso_off(secs(d["done"]), W.offset_h(d["done"])),
                     "WARRENBY" if d["terminal"] == "WARRENBY" else "SELWYN PT", manual.get(d["ref"], d["ref"]),
                     d["loaded"], d["driver"]])
    return rows


SITE_COLS = ["site_code", "site_name", "site_type", "locality", "postcode", "customer_class"]


def site_rows(x, rng):
    rows = []
    for s in x["sites"]:
        pc = "2%03d" % int(rng.integers(280, 330)) if s["metro"] else "2%03d" % int(rng.integers(330, 420))
        cls = ("Company site" if s["name"].startswith("Brennock") else "Dealer") if s["metro"] else "Commercial"
        rows.append([s["code"], s["name"], s["kind"], s["area"], pc, cls])
    rows.sort(key=lambda r: r[0])
    return rows


# ----------------------------------------------------------------------------------------------- VRU
CEMS_COLS = ["interval_start", "channel", "value", "unit", "status"]
SWAP_UTC = None


def cems_rows(x, y, rng):
    """15-minute outlet VOC mass rate. Until the analyser swap during the 12 May stop the channel is VOC_OUT in kg/h;
    after it VOC_OUT2 in g/min. Status CAL is the daily zero and span check (no value), OFF a planned stop."""
    off = x["vru_off"]
    swap = off[1][1]
    rows = []
    t = W.YEAR_START_UTC
    while t < W.YEAR_END_UTC:
        loc = W.to_local(t)
        kg = y["outlet_15"].get(t, 0.0)
        status = "OK"
        if any(a <= t < b for a, b in off):
            status = "OFF"
        elif loc.hour == 5 and loc.minute == 0:
            status = "CAL"
        rate = kg / 0.25 * (1 + rng.normal(0, 0.028)) + max(0.0, 0.0042 + rng.normal(0, 0.0011))
        if status == "OFF":
            rate = 0.0
        new_ch = t >= swap
        ch, unit = ("VOC_OUT2", "g/min") if new_ch else ("VOC_OUT", "kg/h")
        if status == "CAL":
            val = ""
        elif new_ch:
            val = "%.2f" % (rate * 1000 / 60)
        else:
            val = "%.3f" % rate
        rows.append([iso_off(t, W.offset_h(t)), ch, val, unit, status])
        t = t + D(minutes=15)
    return rows


PLC_COLS = ["event_time", "event", "detail", "litres_15c"]


def plc_rows(x, y, rng):
    rows = []
    for r in y["returns"]:
        loc = W.to_local(r["utc"])
        if loc.year < 2026 or loc >= W.EXPORT_END_LOCAL:
            continue
        rows.append((r["utc"], [loc.strftime("%d/%m/%Y %H:%M:%S"), "PRODUCT RETURN", "Absorber return pump P-41",
                                r["litres"]]))
    # regeneration cycles while petrol was loading, two beds alternating
    hours = sorted({r["utc"].replace(minute=0, second=0) for r in y["returns"]})
    bed = 0
    for h in hours:
        loc = W.to_local(h)
        if loc.year < 2026 or loc >= W.EXPORT_END_LOCAL:
            continue
        for k in range(int(rng.integers(1, 4))):
            ts = h + D(minutes=int(rng.integers(0, 59)), seconds=int(rng.integers(0, 59)))
            bed = 1 - bed
            rows.append((ts, [W.to_local(ts).strftime("%d/%m/%Y %H:%M:%S"), "REGEN", "Bed %s vacuum regeneration"
                              % ("AB"[bed]), ""]))
    for a, b in x["vru_off"]:
        rows.append((a, [W.to_local(a).strftime("%d/%m/%Y %H:%M:%S"), "UNIT STOP", "Planned stop, loading interlock "
                         "active", ""]))
        rows.append((b, [W.to_local(b).strftime("%d/%m/%Y %H:%M:%S"), "UNIT START", "Interlock released", ""]))
    rows.sort(key=lambda r: (r[0], r[1][1]))
    return [r for _, r in rows]


# ----------------------------------------------------------------------------------------------- gauging
GAUGE_COLS = ["dip_time", "tank", "product", "innage_mm", "temperature_c", "density_15", "gov_l", "nsv_l"]


def gauge_rows(x, y, rng):
    rows = []
    day = dt.datetime(2025, 12, 31)
    end = dt.datetime(2027, 1, 4)
    while day <= end:
        utc = day + D(hours=6) - D(hours=10)
        for tk in T.ALL_TANKS:
            p = W.TANKS[tk]["product"]
            nsv_true = T.stock_at(y["hist"], tk, utc)
            temp = round(x["temp_at"](utc) + rng.normal(0, 0.35), 1)
            v = S.vcf(p, temp)
            area = math.pi * W.TANKS[tk]["diameter_m"] ** 2 / 4.0
            gov_true = nsv_true / v
            innage = gov_true / 1000.0 / area * 1000.0 + rng.normal(0, 1.1)
            gov = innage / 1000.0 * area * 1000.0
            nsv = gov * v
            rows.append([(utc + D(hours=10)).strftime("%d/%m/%Y %H:%M"), tk, W.NAME_OLD_TAS[p], int(round(innage)), "%.1f" % temp,
                         "%.1f" % S.DENSITY[p], int(round(gov)), int(round(nsv))])
        day = day + D(days=1)
    return rows


# ----------------------------------------------------------------------------------------------- outturns
OUT_COLS = ["Voyage", "Vessel", "Load port", "B/L date", "Grade", "Shore tank", "Commenced", "Completed",
            "B/L qty L15", "Ship's figure L15", "Shore received L15", "Report date", "Surveyor"]


def outturn_rows(x, y, rng):
    rows = []
    ports = {"MT Kestrel Spirit": "Port Kembla", "MT Coral Venture": "Gladstone", "MT Argyle Star": "Port Kembla"}
    surveyors = ["Meridian Marine Survey", "Coastline Inspection Services"]
    for r in y["receipts"]:
        a, b = W.to_local(r["start"]), W.to_local(r["end"])
        if a.year != 2026:
            continue
        ship = int(round(r["bl"] * (1 - abs(rng.normal(0.0009, 0.0006)))))
        rep = (b + D(days=int(rng.choice([1, 1, 2, 2, 3])))).date()
        bl_date = (W.to_local(r["call"]) - D(days=int(rng.integers(2, 5)))).date()
        rows.append([r["voyage"], r["vessel"], ports[r["vessel"]], bl_date, W.NAME_LONG[r["product"]], r["tank"],
                     a.replace(second=0, microsecond=0), b.replace(second=0, microsecond=0), r["bl"], ship, r["shore"],
                     rep, surveyors[int(rng.integers(0, 2))]])
    return rows


# ----------------------------------------------------------------------------------------------- shift log
LOG_COLS = ["shift_date", "shift", "time", "operator", "entry"]
CREW = {"D": ["KM", "RT", "JS", "PL"], "N": ["DW", "AH", "BC", "SN"]}


def shift_of(local):
    if 6 <= local.hour < 18:
        return local.date(), "D"
    if local.hour >= 18:
        return local.date(), "N"
    return (local - D(days=1)).date(), "N"


def log_entry(local, text, rng, rows):
    sd, sh = shift_of(local)
    rows.append((local, [sd.strftime("%d/%m/%Y"), sh, local.strftime("%H:%M"),
                         CREW[sh][int(rng.integers(0, 4))], text]))


def shift_log_rows(x, y, rng):
    rows = []
    for lu in y["lineups"]:
        loc = W.to_local(lu["utc"])
        if loc.year != 2026:
            continue
        lvl = T.stock_at(y["hist"], lu["frm"], lu["utc"]) / 1000.0
        log_entry(loc, "Diesel header changed over %s to %s (%s at %s kL)" % (lu["frm"], lu["to"], lu["frm"],
                  "{:,}".format(int(round(lvl)))), rng, rows)
    for r in y["receipts"]:
        a, b = W.to_local(r["start"]), W.to_local(r["end"])
        if b.year != 2026 and a.year != 2026:
            continue
        log_entry(a - D(minutes=int(rng.integers(35, 80))), "%s (%s) all fast No 1 berth, hoses connected" %
                  (r["vessel"], r["voyage"]), rng, rows)
        log_entry(a, "Commenced discharge %s to %s" % (W.NAME_DOCKET[r["product"]].lower(), r["tank"]), rng, rows)
        log_entry(b, "Completed %s to %s, ship's figure %s kL" % (W.NAME_DOCKET[r["product"]].lower(), r["tank"],
                  "{:,}".format(int(round(r["bl"] / 1000.0)))), rng, rows)
    for tr in y["transfers"]:
        a, b = W.to_local(tr["start"]), W.to_local(tr["end"])
        log_entry(a, "Transfer %s to %s commenced, transfer meter %s L" % (tr["src"], tr["dst"],
                  "{:,}".format(tr["meter_start"])), rng, rows)
        log_entry(b, "Transfer %s to %s completed, transfer meter %s L" % (tr["src"], tr["dst"],
                  "{:,}".format(tr["meter_end"])), rng, rows)
    for i, (a, b) in enumerate(x["vru_off"]):
        log_entry(W.to_local(a), "VRU-1 stopped for planned maintenance, petrol loading suspended on interlock", rng, rows)
        if i == 1:
            log_entry(W.to_local(a) + D(minutes=50), "Instrument tech on site, VRU-1 outlet analyser replaced, new "
                      "channel VOC_OUT2 on the CEMS", rng, rows)
        log_entry(W.to_local(b), "VRU-1 back in service, interlock released, petrol loading resumed", rng, rows)
    log_entry(dt.datetime(2026, 4, 5, 3, 40), "Daylight saving ended 03:00, TMS and VRU PLC back on AEST; tank "
              "gauging unchanged, it runs on AEST all year", rng, rows)
    log_entry(dt.datetime(2026, 10, 4, 3, 35), "Daylight saving started 02:00, TMS and VRU PLC now on AEDT; tank "
              "gauging stays on AEST, 06:00 dips now read 07:00 local", rng, rows)
    seal_days = [dt.datetime(2026, 2, 16, 7, 20), dt.datetime(2026, 5, 11, 7, 5), dt.datetime(2026, 9, 1, 7, 40)]
    for tk, sday in zip(("TK-1", "TK-2", "TK-3"), seal_days):
        log_entry(sday, "Contractor on %s roof under hot work permit, secondary seal works, tank stays in service" % tk,
                  rng, rows)
        done = dt.datetime.strptime(W.TANKS[tk]["seal_from"], "%Y-%m-%d %H:%M")
        log_entry(done + D(minutes=25), "%s seal works finished, roof hatches closed, permit signed off" % tk, rng, rows)
    for a, b in W.TAS_FAULTS:
        log_entry(a, "Bays 1 to 3 TAS controller fault, petrol loading on manual BOLs, dispatch advised", rng, rows)
        log_entry(b, "Bays 1 to 3 back on the TAS, manual BOLs to dispatch", rng, rows)
    said = {"HV-118": "HV-118", "TK-1-N7": "TK-1 nozzle N7", "HV-119": "HV-119"}
    for a, b, tk, asset in T.ABSORBER_PLAN:
        log_entry(a, "VRU-1 absorber supply and return lined up from TK-1 to %s, %s isolated for repair"
                  % (tk, said[asset]), rng, rows)
        log_entry(b, "%s back in service, VRU-1 absorber supply and return back on TK-1" % said[asset], rng, rows)
    # routine: two handovers a day and the odd operating note
    notes = ["Water draw TK-%d, %d L to separator", "Bay %d arm %d slow flow, strainer cleaned",
             "Fire pump weekly run, OK", "Sample %s to lab for appearance and density", "Bay %d earth rig fault, reset",
             "Foam system inspection walk, no issues", "Gate camera 2 offline, IT notified",
             "Bund valve check, all closed", "Bay %d preset keypad sticking, logged with TMS support"]
    day = dt.datetime(2026, 1, 1)
    while day.year == 2026:
        for hh, sh in ((6, "D"), (18, "N")):
            t = day + D(hours=hh, minutes=int(rng.integers(2, 15)))
            log_entry(t, "Handover received, bays 1 to 5 in service, VRU-1 %s" % ("normal" if rng.random() < 0.93 else
                      "regen alarm cleared"), rng, rows)
        for k in range(int(rng.integers(0, 3))):
            t = day + D(hours=float(rng.uniform(0.5, 23.5)))
            if t.month in (4, 10) and t.day in (4, 5) and 1 <= t.hour <= 3:
                continue
            n = notes[int(rng.integers(0, len(notes)))]
            nn = n.count("%")
            if "TK-%d" in n:
                txt = n % (int(rng.integers(4, 6)), int(rng.integers(40, 260)))
            elif "Sample" in n:
                txt = n % ["PULP98 TK-3", "diesel TK-4", "diesel TK-5", "ULP91 TK-1", "PULP95 TK-2"][int(rng.integers(0, 5))]
            elif nn == 2:
                txt = n % (int(rng.integers(1, 6)), int(rng.integers(1, 4)))
            elif nn == 1:
                txt = n % int(rng.integers(1, 6))
            else:
                txt = n
            log_entry(t, txt, rng, rows)
        day = day + D(days=1)
    rows.sort(key=lambda r: (r[0], r[1][4]))
    return [r for _, r in rows]


# ----------------------------------------------------------------------------------------------- work orders
WO_COLS = ["wo_no", "asset_tag", "asset_description", "work_type", "description", "raised", "completed", "status",
           "contractor"]


def work_order_rows(x, rng):
    rows = []
    n = [26004100]

    def wo(asset, desc_a, wtype, desc, raised, done, who):
        n[0] += int(rng.integers(3, 17))
        rows.append(["WO%d" % n[0], asset, desc_a, wtype, desc, raised.strftime("%d/%m/%Y"),
                     done.strftime("%d/%m/%Y %H:%M") if done else "", "Closed" if done else "Open", who])
    seals = [("TK-1", dt.datetime(2026, 1, 19)), ("TK-2", dt.datetime(2026, 4, 14)), ("TK-3", dt.datetime(2026, 8, 4))]
    for tk, raised in seals:
        done = dt.datetime.strptime(W.TANKS[tk]["seal_from"], "%Y-%m-%d %H:%M")
        wo(tk, "%s %s tank" % (tk, W.NAME_LONG[W.TANKS[tk]["product"]].lower()), "Project",
           "Supply and install rim-mounted secondary seal to internal floating roof (vapour loss reduction programme "
           "2026)", raised, done, "Tankcare Engineering")
    wo("VRU-1-AT1", "VRU-1 outlet hydrocarbon analyser", "Corrective", "Replace outlet analyser (end of life), "
       "commission new CEMS channel", dt.datetime(2026, 4, 28), W.to_local(x["vru_off"][1][0]) + D(minutes=180),
       "Calibre Instruments")
    for b in (1, 2, 3, 4, 5):
        for m in (2, 5, 8, 11):
            d0 = dt.datetime(2026, m, int(rng.integers(3, 26)), int(rng.integers(8, 15)), int(rng.integers(0, 59)))
            arms = 3 if b <= 3 else 2
            wo("BAY-%d" % b, "Bay %d loading arms 1 to %d meters" % (b, arms), "Statutory", "Quarterly meter proving, "
               "as found and as left within tolerance", d0 - D(days=10), d0, "Calibre Metering")
    for tk in T.ALL_TANKS:
        d0 = dt.datetime(2026, int(rng.integers(2, 12)), int(rng.integers(3, 26)), 10, 30)
        wo(tk, "%s tank" % tk, "Inspection", "Annual external inspection, roof drains and vents", d0 - D(days=20), d0,
           "Tankcare Engineering")
    for a, b in x["vru_off"]:
        la = W.to_local(a)
        wo("VRU-1", "VRU-1 carbon bed vapour recovery unit", "Preventive", "Planned stop: vacuum pump service, bed "
           "valve stroke test", la - D(days=14), W.to_local(b), "VaporTek Services")
    wo("TGS-1", "Tank gauging system server", "Preventive", "Annual service: firmware update, clock checked against "
       "GPS (system time AEST, no daylight saving), radar gauges TK-1 to TK-5 verified against manual dips",
       dt.datetime(2026, 3, 2), dt.datetime(2026, 3, 18, 11, 25), "Gaugetech Systems")
    wo("P-41", "Absorber return pump", "Corrective", "Mechanical seal weep, replace seal", dt.datetime(2026, 6, 2),
       dt.datetime(2026, 6, 4, 13, 10), "In house")
    wo("GATE-2", "Gate 2 camera", "Corrective", "Camera offline, replace PoE switch", dt.datetime(2026, 10, 7), None,
       "Coastal Security")
    absorber = {"HV-118": ("TK-1 absorber supply valve HV-118", "Valve seized in the open position on the weekly "
                                                                   "stroke test, replace valve"),
                "TK-1-N7": ("TK-1 absorber return nozzle N7", "Weep at the nozzle N7 flange, replace gasket and studs"),
                "HV-119": ("TK-1 absorber return valve HV-119", "Actuator failed to close on demand, replace actuator")}
    for a, b, tk, asset in T.ABSORBER_PLAN:
        what, desc = absorber[asset]
        wo(asset, what, "Corrective", desc, a, b - D(minutes=35), "In house" if asset == "TK-1-N7" else "Valvecare Services")
    for tk in ("TK-4", "TK-5"):
        done = dt.datetime.strptime(W.TANKS[tk]["vents_from"], "%Y-%m-%d %H:%M")
        wo(tk, "%s %s tank" % (tk, W.NAME_LONG[W.TANKS[tk]["product"]].lower()), "Project",
           "Replace open goose-neck vents with pressure-vacuum vents (vapour loss reduction programme 2026)",
           done - D(days=12), done, "Tankcare Engineering")
    rows.sort(key=lambda r: (r[5][6:] + r[5][3:5] + r[5][:2], r[0]))
    return rows


# ----------------------------------------------------------------------------------------------- weather (distractor)
WX_COLS = ["Date", "Maximum temperature (Degree C)", "Minimum temperature (Degree C)", "Rainfall amount (millimetres)",
           "9am wind speed (km/h)", "3pm wind speed (km/h)"]


def weather_rows(x, rng):
    rows = []
    day = dt.datetime(2026, 1, 1)
    while day.year == 2026:
        doy = day.timetuple().tm_yday
        base = 20.5 + 5.6 * math.cos(2 * math.pi * (doy - 22) / 365.0)
        tmax = base + 4.2 + rng.normal(0, 2.6)
        tmin = base - 5.0 + rng.normal(0, 2.1)
        rain = 0.0 if rng.random() < 0.68 else round(float(rng.gamma(0.8, 7.0)), 1)
        rows.append([day.strftime("%Y-%m-%d"), "%.1f" % tmax, "%.1f" % tmin, "%.1f" % rain,
                     int(abs(rng.normal(13, 7))), int(abs(rng.normal(22, 8)))])
        day = day + D(days=1)
    return rows
