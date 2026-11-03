"""The plant's exports as their own systems write them: Batchwise 4 (local time, to the 1 July cutover), Orbitas MES
(UTC, from the cutover, with the in-flight batches' history migrated), the RTO-1 DAHS (Eastern Standard Time all
year), the warehouse receipts, accounts payable, the ERP material master, the CMMS work orders and three files from
the plant's other emission units."""
import csv
import datetime as dt
import io

import numpy as np

import world as W

COMPANY = "Pellston Fine Chemicals, LLC"
FILES = {
    "bw": "batchwise4_batch_steps_2026-01-01_to_2026-07-01.csv",
    "orb": "orbitas_process_operations_2026H2.parquet",
    "opc": "orbitas_operation_codes.csv",
    "basis": "vent_calculation_basis_rev7.xlsx",
    "reg": "cvs1_closed_vent_system_register.xlsx",
    "dahs": "rto1_dahs_1min_2026.csv",
    "permit": "PTO-2219-0447_R3_permit.pdf",
    "test": "BST-25-0418_RTO-1_destruction_efficiency_report.pdf",
    "wms": "wms_receipts_2025-12-15_to_2027-01-08.csv",
    "ap": "ap_invoice_lines_2025-12-01_to_2027-01-29.xlsx",
    "mm": "erp_material_master_2027-01-04.csv",
    "wo": "cmms_work_orders_2026.csv",
    "form": "AQ-117_quarterly_emission_unit_report.xlsx",
    "boiler": "eu_b1_boiler_gas_use_2026.csv",
    "gen": "eu_g1_emergency_generator_log_2026.csv",
    "ldar": "ldar_method21_readings_2026.csv",
}
DISTRACTORS = ["boiler", "gen", "ldar"]

BW_STEP = {"CHG_LIQ": "CHG SOLVENT", "CHG_SOL": "CHG SOLIDS", "HEAT": "HEAT UP", "RXN": "RXN HOLD", "DIST": "DISTILL",
           "STRIP": "N2 STRIP", "EXTR": "EXTRACT", "SETL": "SETTLE", "VDIST": "VAC DISTILL", "COOL": "COOL",
           "XFER": "XFER TO DRYER", "DRUM": "DRUM OFF", "HOLD": "HOLD", "CIP": "SOLVENT WASH", "LOAD": "LOAD",
           "PRE": "PRE-DRY", "DRY": "DRY", "COOLD": "COOL DOWN", "UNLD": "UNLOAD", "FEED": "FEED/REFLUX",
           "HEADS": "HEADS CUT"}
OP_CODE = {"CHG_LIQ": "OP-110", "CHG_SOL": "OP-120", "HEAT": "OP-130", "RXN": "OP-140", "DIST": "OP-150",
           "VDIST": "OP-155", "STRIP": "OP-160", "EXTR": "OP-170", "SETL": "OP-175", "COOL": "OP-180",
           "XFER": "OP-190", "DRUM": "OP-195", "HOLD": "OP-099", "CIP": "OP-910", "LOAD": "OP-210", "PRE": "OP-220",
           "DRY": "OP-230", "COOLD": "OP-240", "UNLD": "OP-250", "FEED": "OP-310", "HEADS": "OP-320"}
OP_TEXT = {"OP-110": "Charge liquids", "OP-120": "Charge solids (manway open)", "OP-130": "Heat",
           "OP-140": "Reaction / hold at temperature", "OP-150": "Distillation, atmospheric", "OP-155": "Distillation, vacuum",
           "OP-160": "Strip with nitrogen", "OP-170": "Extraction / phase split", "OP-175": "Settle", "OP-180": "Cool / crystallise",
           "OP-190": "Transfer to dryer", "OP-195": "Drum off", "OP-099": "Hold (equipment wait)", "OP-910": "Clean (solvent wash)",
           "OP-210": "Dryer load", "OP-220": "Dryer pre-dry", "OP-230": "Dryer drying", "OP-240": "Dryer cool", "OP-250": "Dryer unload",
           "OP-310": "Still feed / reflux", "OP-320": "Still heads cut", "OP-410": "Sample and QC release",
           "OP-420": "Line flush (water)", "OP-430": "Pressure test"}
UNIT_BW = {s: s.replace("-", "") for s in W.SOURCES}
UNIT_ORB = {s: "PFC-" + s for s in W.SOURCES}
OPERATORS = ["JMK", "RTD", "AEV", "SLP", "DBW", "TNC", "KRH", "MJO", "LAF", "GPS", "CWE", "BRN"]


def local_dt(t):
    return dt.datetime(2026, 1, 1) + dt.timedelta(minutes=int(t) + W.local_offset_min(int(t)))


def est_dt(t):
    return dt.datetime(2026, 1, 1) + dt.timedelta(minutes=int(t))


def utc_dt(t):
    return dt.datetime(2026, 1, 1, 5, 0) + dt.timedelta(minutes=int(t))


def write_csv(path, cols, rows, pre=None, newline="\r\n"):
    buf = io.StringIO()
    if pre:
        for line in pre:
            buf.write(line + newline)
    wr = csv.writer(buf, lineterminator=newline)
    wr.writerow(cols)
    n = 0
    for r in rows:
        wr.writerow(r)
        n += 1
    open(path, "w", encoding="utf-8", newline="").write(buf.getvalue())
    return n


def batch_ids(w):
    """Batchwise numbers each unit's batches in its own series; Orbitas numbers process orders plant-wide from the
    cutover, in the order the orders were opened, with the gaps of orders cancelled before release."""
    rng = np.random.default_rng([W.SEED, 401])
    first = {}
    for st in w.steps:
        key = (st[0], st[1])
        if key not in first or st[6] < first[key]:
            first[key] = st[6]
    bw = {}
    seq = {s: int(rng.integers(3, 40)) for s in W.SOURCES}
    for key in sorted(first, key=lambda k: (first[k], k)):
        s = key[0]
        seq[s] += 1
        bw[key] = "B26-%s-%03d" % (s.split("-")[1], seq[s])
    orb = {}
    n = 1100417 + int(rng.integers(0, 60))
    for key in sorted(first, key=lambda k: (first[k], k)):
        n += 1 + (int(rng.integers(1, 4)) if rng.random() < 0.07 else 0)
        orb[key] = "%07d" % n
    return bw, orb


def classify(w):
    """Which export each step is in. Batchwise holds every step started before the cutover (the step in progress
    at the cutover open, with no end); Orbitas holds every step started from the cutover and, for each batch in
    progress at the cutover, its whole history migrated with its own times."""
    by_batch = {}
    for st in w.steps:
        by_batch.setdefault((st[0], st[1]), []).append(st)
    inflight = {k for k, sts in by_batch.items() if min(s[6] for s in sts) < W.CUTOVER < max(s[7] for s in sts)}
    return by_batch, inflight


def bw_rows(w, ids):
    bwid, _ = ids
    by_batch, inflight = classify(w)
    rng = np.random.default_rng([W.SEED, 402])
    rows = []
    for st in w.steps:
        if st[6] >= W.CUTOVER or st[7] <= 0:
            continue
        key = (st[0], st[1])
        op = OPERATORS[int(rng.integers(0, len(OPERATORS)))]
        start = local_dt(st[6]).strftime("%m/%d/%Y %H:%M")
        if st[7] > W.CUTOVER:
            end, status = "", "OPEN"
        else:
            end, status = local_dt(st[7]).strftime("%m/%d/%Y %H:%M"), "COMPLETE"
        prod = {"CLEAN": "CIP", "RECOVERY": "SOLV RECOVERY"}.get(st[2], st[2])
        stepno = st[3] + 1 if st[3] >= 0 else ""
        rows.append((UNIT_BW[st[0]], bwid[key], prod, stepno, BW_STEP[st[4]], start, end, status, op))
    return rows


def orb_table(w, ids):
    _, orbid = ids
    by_batch, inflight = classify(w)
    rng = np.random.default_rng([W.SEED, 403])
    cols = {k: [] for k in ("process_order", "equipment_id", "material", "operation", "op_code", "start_utc",
                            "end_utc", "origin", "op_status", "recorded_by")}
    for st in w.steps:
        key = (st[0], st[1])
        if st[6] < W.CUTOVER and key not in inflight:
            continue
        if st[6] >= W.YEAR:
            continue
        cols["process_order"].append(orbid[key])
        cols["equipment_id"].append(UNIT_ORB[st[0]])
        cols["material"].append({"CLEAN": "CLEAN-SOLV", "RECOVERY": "SR-RECOVERY"}.get(st[2], st[2]))
        cols["operation"].append("%04d" % (10 * (st[3] + 1)) if st[3] >= 0 else "0005")
        cols["op_code"].append(OP_CODE[st[4]])
        cols["start_utc"].append(utc_dt(st[6]).strftime("%Y-%m-%dT%H:%M:%SZ"))
        cols["end_utc"].append(utc_dt(st[7]).strftime("%Y-%m-%dT%H:%M:%SZ"))
        cols["origin"].append("MIGRATED" if st[6] < W.CUTOVER else "ORBITAS")
        cols["op_status"].append("CONFIRMED")
        cols["recorded_by"].append("MIG-BW4" if st[6] < W.CUTOVER else "u%04d" % int(rng.integers(1100, 1190)))
    return cols


def write_parquet(path, cols):
    import pyarrow as pa
    import pyarrow.parquet as pq
    t = pa.table({k: pa.array(v, type=pa.string()) for k, v in cols.items()})
    pq.write_table(t, path, compression="snappy", use_dictionary=True, write_statistics=False)
    return len(cols["process_order"])


def opcode_rows():
    return [(c, OP_TEXT[c]) for c in sorted(OP_TEXT)]


def dahs_rows(w):
    rows = []
    a, b, mode = w.chamber, w.te_b, w.status
    for t in range(W.YEAR):
        rows.append((est_dt(t).strftime("%Y-%m-%d %H:%M"), "%.1f" % a[t], "%.1f" % b[t], mode[t]))
    return rows


DAHS_PRE = ["Thermavex DAHS 6.2 one-minute export", "Site: Pellston Fine Chemicals, Harwick plant; Unit: RTO-1",
            "Period: 2026-01-01 00:00 to 2026-12-31 23:59 (Eastern Standard Time, no daylight saving adjustment)",
            "Exported 2027-01-05 08:12 by environmental workstation ENV-02", ""]
DAHS_COLS = ["Timestamp", "Chamber Temp (F)", "TE-101B (F)", "Mode"]
BW_COLS = ["Unit", "Batch", "Product", "Step No", "Step", "Start", "End", "Status", "Operator"]


# --------------------------------------------------------------------------------------------- purchasing
VENDORS = {"methanol": "Calder Petrochemical Distribution", "toluene": "Calder Petrochemical Distribution",
           "isopropanol": "Oakmere Solvents Inc.", "ethyl acetate": "Oakmere Solvents Inc.",
           "n-heptane": "Ridgeway Hydrocarbons Co.", "isohexane": "Ridgeway Hydrocarbons Co.",
           "tetrahydrofuran": "Selby Specialty Chemicals"}
ITEM_TEXT = {"methanol": "METHANOL, IMPCO GRADE - BULK TANK TRUCK (NET GAL @ 60F)",
             "toluene": "TOLUENE NITRATION GRADE - BULK (NET GAL @60F)",
             "isopropanol": "Isopropyl Alcohol 99% 55 gal drum",
             "ethyl acetate": "Ethyl Acetate 99.5% IBC tote",
             "n-heptane": "n-HEPTANE 99% (DRUM)", "n-heptane bulk": "n-HEPTANE 99% BULK TT, NET GAL 60F",
             "isohexane": "ISOHEXANE TECH. GRADE (DRUM)",
             "tetrahydrofuran": "Tetrahydrofuran, stabilized (BHT), 55G steel drum"}
UNIT_PRICE = {"methanol": 2.31, "toluene": 4.12, "isopropanol": 2.86, "ethyl acetate": 2.04, "n-heptane": 3.38,
              "isohexane": 3.55, "tetrahydrofuran": 6.94}


def purchasing(w):
    """Receipts (rows), invoices (lines) and the material master from the world's deliveries."""
    rng = np.random.default_rng([W.SEED, 404])
    receipts, invoices = [], []
    rc = 418772
    po = 4500231
    inv = {v: int(rng.integers(70000, 90000)) for v in sorted(set(VENDORS.values()))}
    for d in w.deliveries:
        s = d["solvent"]
        code = W.solvent_code(s, d["t"])
        day = local_dt(d["t"]).date()
        post = posting_date(day, rng)
        po += int(rng.integers(3, 29))
        bol = "%s%06d" % ({"Calder Petrochemical Distribution": "CPD", "Oakmere Solvents Inc.": "OSI",
                           "Ridgeway Hydrocarbons Co.": "RHC", "Selby Specialty Chemicals": "SSC"}[VENDORS[s]],
                          int(rng.integers(100000, 999999)))
        if d["mode"] == "bulk":
            tanks = {"methanol": ["T-401", "T-402"], "toluene": ["T-403"], "n-heptane": ["T-405"]}[s]
            gal = d["gal"]
            if len(tanks) == 2 and rng.random() < 0.34:
                g1 = round(gal * float(rng.uniform(0.38, 0.62)), 1)
                parts = [(tanks[0], g1), (tanks[1], round(gal - g1, 1))]
            else:
                parts = [(tanks[int(rng.integers(0, len(tanks)))], gal)]
            for tank, g in parts:
                rc += int(rng.integers(1, 5))
                receipts.append(dict(receipt="GR%07d" % rc, post=post, received=day, po="%d" % po, code=code,
                                     qty=g, uom="GAL", loc=tank, bol=bol, solvent=s, t=d["t"]))
            qty, uom = gal, "GAL"
        else:
            rc += int(rng.integers(1, 5))
            loc = "WH-2" if s != "ethyl acetate" else "WH-3"
            receipts.append(dict(receipt="GR%07d" % rc, post=post, received=day, po="%d" % po, code=code,
                                 qty=d["kg"], uom="KG", loc=loc, bol=bol, solvent=s, t=d["t"]))
            qty, uom = d["kg"], "KG"
        idate = day + dt.timedelta(days=int(rng.integers(2, 17)))
        while idate.weekday() >= 5:
            idate += dt.timedelta(days=1)
        vend = VENDORS[s]
        inv[vend] += int(rng.integers(1, 40))
        text = ITEM_TEXT["n-heptane bulk"] if (s == "n-heptane" and d["mode"] == "bulk") else ITEM_TEXT[s]
        price = UNIT_PRICE[s] * (1 + float(rng.normal(0, 0.03)))
        lb = qty * (W.DENSITY_LB_GAL[s] if uom == "GAL" else W.LB_PER_KG)
        unit_qty, unit_uom = (qty, "GAL") if uom == "GAL" else (qty, "KG")
        unit_price = round(price * (W.DENSITY_LB_GAL[s] if uom == "GAL" else W.LB_PER_KG), 3)
        invoices.append(dict(invoice="%s-%d" % (vend.split()[0][:3].upper(), inv[vend]), date=idate, vendor=vend,
                             po="%d" % po, ticket=bol, delivered=day, line=1, text=text, qty=unit_qty, uom=unit_uom,
                             price=unit_price, amount=round(unit_qty * unit_price, 2), doc="INV", solvent=s, lb=lb))
        first = invoices[-1]
        if d["mode"] != "bulk" and rng.random() < 0.18:
            invoices.append(dict(invoice=invoices[-1]["invoice"], date=idate, vendor=vend, po="%d" % po, ticket=bol,
                                 delivered=day, line=2, text="Drum deposit / returnable container charge" if d["mode"] == "drum" else
                                 "IBC tote deposit", qty=d.get("n", 1), uom="EA", price=45.0 if d["mode"] == "drum" else 160.0,
                                 amount=round(d.get("n", 1) * (45.0 if d["mode"] == "drum" else 160.0), 2), doc="INV",
                                 solvent=None, lb=0.0))
        if d["mode"] == "bulk" and rng.random() < 0.5:
            invoices.append(dict(invoice=invoices[-1]["invoice"], date=idate, vendor=vend, po="%d" % po, ticket=bol,
                                 delivered=day, line=2, text="Fuel surcharge", qty=1, uom="EA", price=round(float(rng.uniform(85, 160)), 2),
                                 amount=0.0, doc="INV", solvent=None, lb=0.0))
            invoices[-1]["amount"] = invoices[-1]["price"]
        if rng.random() < 0.09:
            # a subsequent debit: the supplier's price correction, posted against the same order quantity
            sdate = idate + dt.timedelta(days=int(rng.integers(12, 40)))
            while sdate.weekday() >= 5:
                sdate += dt.timedelta(days=1)
            inv[vend] += int(rng.integers(1, 40))
            step = round(first["price"] * float(rng.uniform(0.015, 0.045)), 3)
            invoices.append(dict(invoice="%s-%d" % (vend.split()[0][:3].upper(), inv[vend]), date=sdate, vendor=vend,
                                 po="%d" % po, ticket=bol, delivered=day, line=1, text=first["text"], qty=first["qty"],
                                 uom=first["uom"], price=step, amount=round(first["qty"] * step, 2), doc="SUB",
                                 solvent=s, lb=0.0))
    receipts.sort(key=lambda r: (r["post"], r["receipt"]))
    invoices.sort(key=lambda r: (r["date"], r["invoice"], r["line"]))
    w.receipts, w.invoices = receipts, invoices
    return receipts, invoices


WMS_COLS = ["Receipt No", "Posting Date", "PO Number", "Material", "Qty", "UoM", "Storage Loc", "BOL No"]


def posting_date(day, rng):
    """The receiving clerk's posting: a working day or so after the delivery, except that postings stop for the
    stock counts (from 24 June to the half-year close, and from 17 December to the year end) and the deliveries in
    the count are posted on the first working day after it."""
    for a, b, p in ((dt.date(2025, 12, 17), dt.date(2026, 1, 1), dt.date(2026, 1, 2)),
                    (dt.date(2026, 6, 24), dt.date(2026, 6, 30), dt.date(2026, 7, 1)),
                    (dt.date(2026, 12, 17), dt.date(2027, 1, 3), dt.date(2027, 1, 4))):
        if a <= day <= b:
            return p
    post = day + dt.timedelta(days=int(rng.choice([0, 0, 0, 1, 1, 2, 3])))
    while post.weekday() >= 5:
        post += dt.timedelta(days=1)
    return post


def wms_rows(w):
    lo, hi = dt.date(2025, 12, 15), dt.date(2027, 1, 8)
    out = []
    for r in w.receipts:
        if lo <= r["post"] <= hi:
            out.append((r["receipt"], r["post"].strftime("%Y-%m-%d"), r["po"], r["code"], "%.1f" % r["qty"], r["uom"],
                        r["loc"], r["bol"]))
    return out


def ap_lines(w):
    return [r for r in w.invoices if dt.date(2025, 12, 1) <= r["date"] <= dt.date(2027, 1, 29)]


MM_COLS = ["Material", "Description", "Base UoM", "Density (lb/gal @60F)", "Material Group", "Last Changed"]


def mm_rows():
    return [("SOL-01", "Methanol, bulk", "GAL", "6.63", "SOLV-BULK", "2024-02-12"),
            ("SOL-03", "Toluene, bulk", "GAL", "7.26", "SOLV-BULK", "2023-09-05"),
            ("SOL-04", "Isopropanol, drum", "KG", "", "SOLV-PKG", "2023-09-05"),
            ("SOL-05", "Ethyl acetate, tote", "KG", "", "SOLV-PKG", "2024-11-18"),
            ("SOL-07", "Isohexane, drum", "KG", "", "SOLV-PKG", "2026-06-01"),
            ("SOL-09", "Tetrahydrofuran, drum", "KG", "", "SOLV-PKG", "2022-04-27"),
            ("SOL-12", "n-Heptane, bulk", "GAL", "5.71", "SOLV-BULK", "2026-06-01"),
            ("SOL-14", "Acetone, drum (cleaning)", "KG", "", "SOLV-PKG", "2021-08-30"),
            ("NIT-01", "Nitrogen, liquid", "SCF", "", "GAS", "2020-01-14"),
            ("CAT-22", "Palladium on carbon 5%", "KG", "", "CATALYST", "2025-03-03")]


# --------------------------------------------------------------------------------------------- work orders
WO_COLS = ["WO No", "Asset", "Opened", "Closed", "Type", "Problem", "Work Done"]


def wo_rows(w):
    rng = np.random.default_rng([W.SEED, 405])
    f0, f1 = w.te_fail
    fixed = [
        ("RTO-1", W.DOY[7] * 1440 + 9 * 1440 + 7 * 60 + 15, f1, "CM",
         "Chamber temp on DAHS reading low against TE-101B and against burner firing rate.",
         "Checked TE-101A loop, found thermocouple degraded. 08/11 DAHS chamber input moved to TE-101B pending part. "
         "08/26 replaced TE-101A, input restored to TE-101A, loop checked."),
        ("RTO-1", w.down[0][0] - 6 * 1440 + 7 * 60 + 40, w.down[0][0] + 4 * 1440 + 515, "PM",
         "Planned outage, summer turnaround.", "Replaced burner management system and flame scanner; poppet valve seals "
         "renewed; media inspected."),
        ("RTO-1", 33 * 1440 + 11 * 60, 33 * 1440 + 15 * 60 + 20, "CM", "Flame failure trips, intermittent.",
         "Flame scanner cleaned and realigned. Monitoring."),
        ("RTO-1", 51 * 1440 + 8 * 60, 51 * 1440 + 9 * 60 + 40, "CM", "Repeat flame failure trip.",
         "Scanner replaced under warranty. BMS replacement scheduled for turnaround."),
        ("PSV-31", 140 * 1440 + 9 * 60, 140 * 1440 + 11 * 60, "PM", "Annual PSV inspection.",
         "Inspected in place, seat clean, tag renewed."),
    ]
    assets = ["R-101", "R-102", "R-103", "R-104", "R-105", "R-106", "D-201", "D-202", "SR-301", "P-410A", "P-410B",
              "T-401", "T-402", "T-403", "T-405", "CT-1", "AC-2", "B-1"]
    probs = [("CM", "Agitator seal weeping.", "Seal replaced."), ("PM", "Quarterly PM.", "Lubricated, inspected, OK."),
             ("CM", "Level transmitter erratic.", "Recalibrated LT."), ("CM", "Manway gasket leak.", "Gasket replaced."),
             ("PM", "Filter bag change.", "Bags changed, dP normal."), ("CM", "Vacuum pump low capacity.",
                                                                       "Pump rebuilt."),
             ("PM", "Annual inspection.", "No findings."), ("CM", "Steam trap blowing through.", "Trap replaced."),
             ("CM", "Jacket temp control hunting.", "TCV positioner retuned."), ("CM", "Sight glass fogged.",
                                                                                 "Cleaned, new gasket."),
             ("CM", "Agitator gearbox noisy.", "Oil changed, bearing checked; monitor."),
             ("PM", "PSV bench test due.", "Removed, tested at set, reinstalled."),
             ("CM", "Pump mech seal leaking at startup.", "Seal faces lapped, reinstalled."),
             ("CM", "Condenser outlet temp high.", "Back-flushed CW side."),
             ("PM", "Grounding / bonding check.", "Readings within limits."),
             ("CM", "Valve not closing fully.", "Actuator stroke adjusted."),
             ("CM", "Loose insulation on line.", "Re-lagged 6 ft section."),
             ("PM", "Semi-annual vibration route.", "Readings logged, no alarms."),
             ("CM", "Pressure gauge reading zero.", "Gauge replaced."),
             ("CM", "Hose crimp leaking at transfer station.", "Hose replaced, pressure tested.")]
    rows = []
    n = 26101400 + int(rng.integers(0, 80))
    events = [(a, b, t, p, d, x) for (x, a, b, t, p, d) in [(f[0], f[1], f[2], f[3], f[4], f[5]) for f in fixed]]
    for _ in range(140):
        a = int(rng.integers(0, W.YEAR - 3 * 1440))
        b = a + int(rng.integers(60, 3 * 1440))
        t, p, d = probs[int(rng.integers(0, len(probs)))]
        events.append((a, b, t, p, d, assets[int(rng.integers(0, len(assets)))]))
    events.sort(key=lambda e: e[0])
    for a, b, t, p, d, asset in events:
        n += int(rng.integers(1, 9))
        rows.append(("WO%d" % n, asset, local_dt(a).strftime("%Y-%m-%d %H:%M"), local_dt(b).strftime("%Y-%m-%d %H:%M"),
                     t, p, d))
    return rows


# --------------------------------------------------------------------------------------------- distractors
def boiler_rows():
    rng = np.random.default_rng([W.SEED, 406])
    rows = []
    for m in range(1, 13):
        hdd = [1010, 880, 690, 420, 170, 30, 5, 10, 90, 380, 650, 920][m - 1]
        therms = 21000 + hdd * 23.5 + float(rng.normal(0, 900))
        hours = 610 + float(rng.normal(0, 25)) if m not in (7, 12) else 455 + float(rng.normal(0, 25))
        rows.append(("2026-%02d" % m, "EU-B1", "B-1", "%.0f" % therms, "%.1f" % hours, "%d" % hdd))
    return rows


def gen_rows():
    rng = np.random.default_rng([W.SEED, 407])
    rows = []
    day = 9
    while day < 365:
        d = dt.date(2026, 1, 1) + dt.timedelta(days=day)
        rows.append((d.strftime("%m/%d/%Y"), "EU-G1", "GEN-1", "Monthly readiness test",
                     "%.1f" % float(rng.uniform(0.4, 0.6)), "%.1f" % (1200 + day * 0.06)))
        day += int(rng.integers(26, 34))
    rows.insert(5, ("05/18/2026", "EU-G1", "GEN-1", "Utility outage, storm", "6.4", "1217.4"))
    return rows


def ldar_rows():
    rng = np.random.default_rng([W.SEED, 408])
    rows = []
    comps = []
    for area in ("RX", "DRY", "TF", "SR"):
        for k in range(int(rng.integers(60, 110))):
            kind = ["VALVE", "VALVE", "VALVE", "CONNECTOR", "PUMP", "PRV"][int(rng.integers(0, 6))]
            comps.append(("%s-%s-%04d" % (area, kind[0], 100 + k * int(rng.integers(1, 3))), kind, area))
    for q, mon in ((1, 2), (2, 5), (3, 8), (4, 11)):
        for tag, kind, area in comps:
            day = int(rng.integers(3, 26))
            ppm = float(np.exp(rng.normal(1.6, 1.3)))
            if rng.random() < 0.012:
                ppm = float(rng.uniform(520, 9000))
            rows.append(("2026-%02d-%02d" % (mon, day), tag, kind, area, "%.0f" % ppm, "TVA-1000B #2207"))
    rows.sort()
    return rows
