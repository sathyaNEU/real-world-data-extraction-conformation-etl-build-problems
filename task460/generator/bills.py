"""Corvane's accounts-payable export of electricity invoice lines for the eight candidate stores: each store's
delivery utility bills every meter on its read cycle (and, at Halvane, the store's gas service on the same
invoice), and Corvane's national retail supplier bills each meter by calendar month, allocating the utility's cycle
reads to months by days. Every metered kilowatt-hour appears on several charge lines of both bills. Two cycles
were billed on an estimated read and billed again on the actual read; the export carries invoices only, so both
bills for those cycles are in it (and the supplier's two bills for each month those cycles touch)."""
import datetime as dt

import numpy as np

import world as W

D0 = dt.date(2024, 11, 1)
D1 = dt.date(2026, 2, 28)

# Delivery tariffs by store's area: customer charge $/month, distribution and transmission $/kWh, demand $/kW,
# state kWh excise $/kWh (0 where the state taxes otherwise), sales tax rate; supplier energy price $/kWh and
# capacity $/kW-month.
TARIFF = {
    "BRKW": dict(cust=58.40, dist=0.03312, trans=0.01184, dem=6.85, excise=0.00064, tax=0.060, energy=0.06180, cap=4.95),
    "QLBY": dict(cust=74.25, dist=0.04126, trans=0.01507, dem=9.40, excise=0.0, tax=0.040, energy=0.06799, cap=7.20),
    "TNFD": dict(cust=46.00, dist=0.02968, trans=0.01045, dem=5.90, excise=0.0, tax=0.0625, energy=0.05610, cap=3.85),
    "GRSF": dict(cust=52.75, dist=0.03091, trans=0.01128, dem=6.40, excise=0.00058, tax=0.0575, energy=0.05935, cap=4.30),
    "FRVW": dict(cust=39.80, dist=0.02643, trans=0.00912, dem=5.15, excise=0.0, tax=0.065, energy=0.05025, cap=3.10),
    "OSTM": dict(cust=61.10, dist=0.03587, trans=0.01263, dem=8.75, excise=0.00072, tax=0.056, energy=0.06463, cap=5.60),
    "KSTP": dict(cust=81.60, dist=0.05214, trans=0.01822, dem=11.85, excise=0.0, tax=0.0725, energy=0.07960, cap=6.75),
    "HLVN": dict(cust=49.30, dist=0.03203, trans=0.01102, dem=6.10, excise=0.0, tax=0.0475, energy=0.05870, cap=4.05),
}
RPS = 0.00412
# each utility's own words for its lines: customer, distribution energy, transmission energy, demand, kWh excise, tax
WORDS = {
    "BRKW": ("Customer charge", "Distribution energy charge", "Transmission service charge", "Distribution demand charge",
             "State electricity excise tax", "Sales tax"),
    "QLBY": ("Basic service charge", "Delivery service - energy", "Transmission - energy", "Delivery service - demand",
             None, "Sales and use tax"),
    "TNFD": ("Customer charge", "Distribution kWh charge", None, "Distribution kW charge", None, "State sales tax"),
    "GRSF": ("Customer charge", "Energy delivery charge", "Transmission energy charge", "Demand delivery charge",
             "Gross receipts tax (kWh)", "Sales tax"),
    "FRVW": ("Monthly service charge", "Distribution charge per kWh", "Transmission charge per kWh", "Distribution demand",
             None, "Utility tax"),
    "OSTM": ("Customer charge", "Delivery energy charge", "Transmission energy charge", "Delivery demand charge",
             "Regulatory assessment (kWh)", "Sales tax"),
    "KSTP": ("Customer charge", "Distribution energy", "Transmission energy", "Distribution demand", None, "Utility users tax"),
    "HLVN": ("Electric customer charge", "Electric distribution energy charge", "Electric transmission charge",
             "Electric distribution demand charge", None, "Electric sales tax"),
}
# Tennaford's distribution energy is billed in declining blocks, and its transmission on demand
TNFD_BLOCKS = ((50000, 0.03642), (150000, 0.02971), (None, 0.02514))
TNFD_TRANS_KW = 3.12
# the supplier buys at the wholesale delivery point: its energy quantity is the metered kWh times the territory's
# distribution loss factor
LOSS = {"BRKW": 1.0412, "QLBY": 1.0538, "TNFD": 1.0365, "GRSF": 1.0447, "FRVW": 1.0581, "OSTM": 1.0496, "KSTP": 1.0623,
        "HLVN": 1.0429}
VENDOR_NO = {"BRKW": "V100418", "QLBY": "V100562", "TNFD": "V100731", "GRSF": "V100804", "FRVW": "V100917",
             "OSTM": "V101026", "KSTP": "V101152", "HLVN": "V101233"}
SUPPLIER_NO = "V204460"
READ_DAY = {"BRKW": 9, "QLBY": 14, "TNFD": 6, "GRSF": 11, "FRVW": 17, "OSTM": 4, "KSTP": 21, "HLVN": 12}
# cycles billed first on an estimated read (store's area, meter index, the month the cycle starts), and the
# estimate's error against the actual read
REBILLED = {("QLBY", 0, (2025, 1)): 0.137, ("OSTM", 0, (2025, 7)): -0.118}


def daily_use(rng, mwh, season):
    """kWh by calendar day, D0 to D1: the meter's 2025 use shaped by its winter and summer weight, weekend trade,
    the spring planting season and weather."""
    days = [D0 + dt.timedelta(days=k) for k in range((D1 - D0).days + 1)]
    doy = np.array([d.timetuple().tm_yday for d in days])
    wint, summ = season
    shape = 1.0 + (wint - 1.0) * np.clip(np.cos(2 * np.pi * (doy - 20) / 365), 0, None) \
        + (summ - 1.0) * np.clip(np.cos(2 * np.pi * (doy - 205) / 365), 0, None)
    wk = np.array([1.06 if d.weekday() >= 5 else 0.975 for d in days])
    spring = 1.0 + 0.08 * np.exp(-((doy - 120) / 25.0) ** 2)
    noise = np.exp(rng.normal(0, 0.035, len(days)))
    base = shape * wk * spring * noise
    in25 = np.array([d.year == 2025 for d in days])
    kwh = base / base[in25].sum() * mwh * 1000.0 * (1 + rng.normal(0, 0.004))
    return days, kwh


def read_dates(rng, code):
    reads = []
    y, m = 2024, 11
    while (y, m) <= (2026, 2):
        d = dt.date(y, m, READ_DAY[code]) + dt.timedelta(days=int(rng.integers(-2, 3)))
        if d.weekday() == 6:
            d += dt.timedelta(days=1)
        reads.append(d)
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return reads


def month_bounds(y, m):
    m0 = dt.date(y, m, 1)
    m1 = (dt.date(y + 1, 1, 1) if m == 12 else dt.date(y, m + 1, 1)) - dt.timedelta(days=1)
    return m0, m1


def allocate(cyc, m0, m1):
    q = 0.0
    for c in cyc:
        ov = (min(c["to"], m1) - max(c["from"], m0)).days + 1
        if ov > 0:
            q += c["kwh"] * ov / ((c["to"] - c["from"]).days + 1)
    return int(round(q))


def build(seed=W.SEED + 23):
    rng = np.random.default_rng(seed)
    lines, meters = [], {}
    for code in W.ORDER:
        s = W.STORES[code]
        t = TARIFF[code]
        reads = read_dates(rng, code)
        acct = "%04d-%06d-%d" % (int(rng.integers(1000, 9999)), int(rng.integers(100000, 999999)), int(rng.integers(1, 9)))
        sup_acct = "ARE-%04d" % s["store"]
        next_inv = int(rng.integers(4100000, 4800000))
        pre = "Electric " if s.get("gas") else ""
        gas_no = "G%07d" % int(rng.integers(1000000, 9999999)) if s.get("gas") else None
        meters[code] = []
        for mi, (meter, mwh) in enumerate(s["meters"]):
            mno = "%s%07d" % ("E" if not s.get("gas") else "M", int(rng.integers(1000000, 9999999)))
            days, kwh = daily_use(rng, mwh, s["season"])
            day_kwh = dict(zip(days, kwh))
            true_cyc, billed = [], []
            for a, b in zip(reads[:-1], reads[1:]):
                span = [a + dt.timedelta(days=k) for k in range((b - a).days)]
                q = int(round(sum(day_kwh[d] for d in span)))
                kw = round(max(day_kwh[d] for d in span) / 24 * 1.85 * (1 + rng.normal(0, 0.03)), 1)
                c = dict(**{"from": a, "to": b - dt.timedelta(days=1)}, kwh=q, kw=kw)
                true_cyc.append(c)
                err = REBILLED.get((code, mi, (a.year, a.month)))
                if err is not None:
                    est = dict(c, kwh=int(round(q * (1 + err))), kw=round(kw * (1 + err / 2), 1))
                    billed.append((est, c["to"] + dt.timedelta(days=int(rng.integers(3, 7)))))
                    billed.append((c, c["to"] + dt.timedelta(days=int(rng.integers(33, 41)))))
                else:
                    billed.append((c, c["to"] + dt.timedelta(days=int(rng.integers(3, 7)))))
            meters[code].append(dict(meter=meter, number=mno, cycles=true_cyc, days=day_kwh))
            for c, idate in billed:
                next_inv += int(rng.integers(1, 40))
                ino = "%s-%07d" % (code[:2], next_inv)
                wd = WORDS[code]
                ls = [(wd[0], 1, "MO", t["cust"])]
                if code == "TNFD":
                    left, lo = c["kwh"], 0
                    for size, rate in TNFD_BLOCKS:
                        q = left if size is None else min(left, size)
                        if q > 0:
                            ls.append(("%s, %s" % (wd[1], "first 50,000 kWh" if lo == 0 else ("next 150,000 kWh" if size
                                                                                                else "over 200,000 kWh")),
                                       q, "KWH", q * rate))
                        left -= q
                        lo += size or 0
                    ls.append((wd[3], c["kw"], "KW", c["kw"] * t["dem"]))
                    ls.append(("Transmission kW charge", c["kw"], "KW", c["kw"] * TNFD_TRANS_KW))
                else:
                    ls.append((wd[1], c["kwh"], "KWH", c["kwh"] * t["dist"]))
                    ls.append((wd[2], c["kwh"], "KWH", c["kwh"] * t["trans"]))
                    ls.append((wd[3], c["kw"], "KW", c["kw"] * t["dem"]))
                    if wd[4]:
                        ls.append((wd[4], c["kwh"], "KWH", c["kwh"] * t["excise"]))
                sub = sum(round(x[3], 2) for x in ls)
                ls.append((wd[5], "", "", sub * t["tax"]))
                gas_meter = None
                if s.get("gas") and mi == 0:
                    gas_meter = gas_no
                    th = int(round(950 + 2300 * max(0.0, np.cos(2 * np.pi * (c["from"].timetuple().tm_yday - 20) / 365))
                                   + rng.normal(0, 60)))
                    gs = [("Gas customer charge", 1, "MO", 32.00), ("Gas distribution charge", th, "THERM", th * 0.4185),
                          ("Gas supply charge", th, "THERM", th * 0.5310)]
                    gsub = sum(round(x[3], 2) for x in gs)
                    gs.append(("Gas sales tax", "", "", gsub * t["tax"]))
                    ls = ls + gs
                for k, (desc, qty, uom, amt) in enumerate(ls):
                    lines.append(dict(vendor=VENDOR_NO[code], vendor_name=s["utility"], invoice=ino, invoice_date=idate,
                                      store=s["store"], account=acct, meter=gas_meter if desc.startswith("Gas") else mno,
                                      service_from=c["from"], service_to=c["to"], line=k + 1, desc=desc, qty=qty, uom=uom,
                                      amount=round(amt, 2), code=code, kind="utility"))
            # the supplier: one invoice per meter per calendar month, the utility's cycle reads allocated by days; a
            # month an estimated cycle touched is billed on the estimate and again on the actual read
            est_cyc = [dict(c) for c in true_cyc]
            for k, c in enumerate(true_cyc):
                err = REBILLED.get((code, mi, (c["from"].year, c["from"].month)))
                if err is not None:
                    est_cyc[k] = dict(c, kwh=int(round(c["kwh"] * (1 + err))), kw=round(c["kw"] * (1 + err / 2), 1))
            y, m = 2024, 12
            while (y, m) <= (2026, 1):
                m0, m1 = month_bounds(y, m)
                versions = [(est_cyc, m1 + dt.timedelta(days=int(rng.integers(9, 15))))]
                if est_cyc != true_cyc and any(c["kwh"] != e["kwh"] and c["to"] >= m0 and c["from"] <= m1
                                               for c, e in zip(true_cyc, est_cyc)):
                    versions.append((true_cyc, m1 + dt.timedelta(days=int(rng.integers(44, 52)))))
                for vi, (cyc, idate) in enumerate(versions):
                    q = int(round(allocate(cyc, m0, m1) * LOSS[code]))
                    if q <= 0:
                        continue
                    plc = round(0.82 * max(c["kw"] for c in cyc if c["to"] >= m0 and c["from"] <= m1), 1)
                    ino = "ARE%02d%02d-%04d%d" % (y % 100, m, s["store"], mi + 1 + 4 * vi)
                    ls = [("Energy - fixed price", q, "KWH", q * t["energy"]),
                          ("Renewable portfolio standard cost", q, "KWH", q * RPS),
                          ("Capacity charge", plc, "KW", plc * t["cap"])]
                    sub = sum(round(x[3], 2) for x in ls)
                    ls.append(("Sales tax", "", "", sub * t["tax"]))
                    for k, (desc, qty, uom, amt) in enumerate(ls):
                        lines.append(dict(vendor=SUPPLIER_NO, vendor_name=W.SUPPLIER, invoice=ino, invoice_date=idate,
                                          store=s["store"], account=sup_acct, meter=mno, service_from=m0, service_to=m1,
                                          line=k + 1, desc=desc, qty=qty, uom=uom, amount=round(amt, 2), code=code,
                                          kind="supplier"))
                y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    lines.sort(key=lambda r: (r["invoice_date"], r["vendor"], r["invoice"], r["line"]))
    return lines, meters
