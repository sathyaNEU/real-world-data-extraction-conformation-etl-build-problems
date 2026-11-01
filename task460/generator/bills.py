"""Corvane's accounts-payable export of electricity invoice lines for the eight candidate stores.

Each store's delivery utility reads every meter monthly and bills it on its own read cycle; Corvane's national retail
supplier bills each meter on the same cycles from the utility's reads. In the spring
of 2025 Corvane moved its stores' main utility accounts to a bill-payment service in three waves: from a store's go-live
the utility sends its bills to the service, the service pays them and invoices Corvane weekly, one line per bill paid,
so the utility's own invoice lines (and the kilowatt-hours on them) stop reaching accounts payable. The garden-centre
accounts at Quillbury and Kestrel Point stayed on direct payment. At most stores the first bill after the go-live had
already reached Corvane and was paid by accounts payable as well; the utility carried the overpayment as a credit on
the account, so the service paid less on the bills that followed. The supplier billed energy at the wholesale delivery
point (the meter's kilowatt-hours times the territory's loss factor) with its renewable portfolio standard cost on the
same quantity until its new term began with the first read on or after 1 July 2025; the new term prices energy on the
meter's kilowatt-hours with the standard's cost in the price."""
import datetime as dt

import numpy as np

import world as W

D0 = dt.date(2024, 11, 1)
D1 = dt.date(2026, 2, 28)
PULL_LAST = dt.date(2026, 2, 28)          # the export's last invoice date
Y0, Y1 = dt.date(2025, 1, 1), dt.date(2025, 12, 31)

# Delivery tariffs by store's area: customer charge $/month, distribution and transmission $/kWh, demand $/kW,
# state kWh excise $/kWh (0 where the state taxes otherwise), sales tax rate; supplier energy price $/kWh at the
# wholesale delivery point and capacity $/kW-month (first term).
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
# the supplier's second term (from 1 July 2025): energy priced on the meter's kWh, the standard's cost in the price;
# each zone's price moved with the forward market against the first term's loss-adjusted price plus the standard's cost
TERM2 = dt.date(2025, 7, 1)
TERM2_MOVE = {"BRKW": 0.024, "QLBY": -0.017, "TNFD": 0.031, "GRSF": 0.012, "FRVW": -0.034, "OSTM": 0.038,
              "KSTP": -0.008, "HLVN": 0.019}
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
BILL_PREFIX = {"BRKW": "BP", "QLBY": "QE", "TNFD": "TE", "GRSF": "GP", "FRVW": "FE", "OSTM": "OS", "KSTP": "KP",
               "HLVN": "HG"}
# Tennaford's distribution energy is billed in declining blocks, and its transmission on demand
TNFD_BLOCKS = ((50000, 0.03642), (150000, 0.02971), (None, 0.02514))
TNFD_TRANS_KW = 3.12
# the territory's distribution loss factor, by which the supplier's first term grossed the meter's kWh up to the
# wholesale delivery point
LOSS = {"BRKW": 1.0412, "QLBY": 1.0538, "TNFD": 1.0365, "GRSF": 1.0447, "FRVW": 1.0581, "OSTM": 1.0496, "KSTP": 1.0623,
        "HLVN": 1.0429}
VENDOR_NO = {"BRKW": "V100418", "QLBY": "V100562", "TNFD": "V100731", "GRSF": "V100804", "FRVW": "V100917",
             "OSTM": "V101026", "KSTP": "V101152", "HLVN": "V101233"}
SUPPLIER_NO = "V204460"
PAYSERV = "Halworth Utility Payment Services LLC"
PAYSERV_NO = "V306118"
READ_DAY = {"BRKW": 9, "QLBY": 14, "TNFD": 6, "GRSF": 11, "FRVW": 17, "OSTM": 4, "KSTP": 21, "HLVN": 12}
# the bill-payment service's go-live for each store's main account: bills dated from this day go to the service
GOLIVE = {"QLBY": dt.date(2025, 3, 1), "KSTP": dt.date(2025, 3, 1), "BRKW": dt.date(2025, 3, 1),
          "TNFD": dt.date(2025, 3, 24), "GRSF": dt.date(2025, 3, 24), "FRVW": dt.date(2025, 3, 24),
          "OSTM": dt.date(2025, 4, 14), "HLVN": dt.date(2025, 4, 14)}
# stores whose first bill after the go-live had already reached Corvane and was paid by accounts payable as well
PAID_TWICE = {"QLBY", "KSTP", "BRKW", "TNFD", "GRSF", "FRVW", "OSTM"}


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
    """kWh of the cycles allocated to the days m0 to m1, each cycle's kWh spread evenly over its days."""
    q = 0.0
    for c in cyc:
        ov = (min(c["to"], m1) - max(c["from"], m0)).days + 1
        if ov > 0:
            q += c["kwh"] * ov / ((c["to"] - c["from"]).days + 1)
    return q


def frac_2025(a, b):
    lo, hi = max(a, Y0), min(b, Y1)
    return max((hi - lo).days + 1, 0) / ((b - a).days + 1)


def bill_lines(code, c, gas_therms=None):
    """The utility's charge lines for one cycle: (description, quantity, unit, amount) electric, then gas."""
    t = TARIFF[code]
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
    ls = [(d, q, u, round(a, 2)) for d, q, u, a in ls]
    sub = sum(x[3] for x in ls)
    ls.append((wd[5], "", "", round(sub * t["tax"], 2)))
    gs = []
    if gas_therms is not None:
        th = gas_therms
        gs = [("Gas customer charge", 1, "MO", 32.00), ("Gas distribution charge", th, "THERM", round(th * 0.4185, 2)),
              ("Gas supply charge", th, "THERM", round(th * 0.5310, 2))]
        gsub = sum(x[3] for x in gs)
        gs.append(("Gas sales tax", "", "", round(gsub * t["tax"], 2)))
    return ls, gs


def friday_after(d):
    return d + dt.timedelta(days=(4 - d.weekday()) % 7)


def build(seed=W.SEED + 23):
    ru = np.random.default_rng(seed)            # the meters: reads, daily use, demand
    rb = np.random.default_rng(seed + 977)      # the billing: numbers, dates, therms
    ra = np.random.default_rng(seed + 4049)     # the supplier's account and invoice numbering
    lines, meters, truth = [], {}, {}
    pay_lines = []                              # the payment service's lines, numbered once every week is known
    for code in W.ORDER:
        s = W.STORES[code]
        t = TARIFF[code]
        lf = LOSS[code]
        reads = read_dates(ru, code)
        sup_acct = "%d-%07d" % (int(ra.integers(30, 99)), int(ra.integers(1000000, 9999999)))
        next_inv = int(rb.integers(4100000, 4800000))
        gas_no = "G%07d" % int(rb.integers(1000000, 9999999)) if s.get("gas") else None
        price2 = round((t["energy"] + RPS) * lf * (1 + TERM2_MOVE[code]), 5)
        meters[code] = []
        tr = dict(use_kwh=0.0, months=np.zeros(12), charges=0.0, utility_charges=0.0, supplier_charges=0.0,
                  credit=0.0, paid_twice=None, golive=GOLIVE[code], price2=price2, lf=lf)
        for mi, (kind, mwh) in enumerate(s["meters"]):
            mno = "%s%07d" % ("E" if not s.get("gas") else "M", int(ru.integers(1000000, 9999999)))
            acct = "%04d-%06d-%d" % (int(rb.integers(1000, 9999)), int(rb.integers(100000, 999999)), int(rb.integers(1, 9)))
            days, kwh = daily_use(ru, mwh, s["season"])
            day_kwh = dict(zip(days, kwh))
            cycles = []
            for a, b in zip(reads[:-1], reads[1:]):
                span = [a + dt.timedelta(days=k) for k in range((b - a).days)]
                q = int(round(sum(day_kwh[d] for d in span)))
                kw = round(max(day_kwh[d] for d in span) / 24 * 1.85 * (1 + ru.normal(0, 0.03)), 1)
                cycles.append(dict(**{"from": a, "to": b - dt.timedelta(days=1)}, kwh=q, kw=kw, read=b))
            meters[code].append(dict(meter=kind, number=mno, account=acct, cycles=cycles, days=day_kwh))
            on_service = mi == 0                 # the main account moved to the payment service; garden centres did not
            credit, first_after = 0.0, True
            for c in cycles:
                bdate = c["read"] + dt.timedelta(days=int(rb.integers(3, 7)))
                if bdate > PULL_LAST:
                    continue
                next_inv += int(rb.integers(1, 40))
                bno = "%s-%07d" % (BILL_PREFIX[code], next_inv)
                th = None
                if s.get("gas") and mi == 0:
                    th = int(round(950 + 2300 * max(0.0, np.cos(2 * np.pi * (c["from"].timetuple().tm_yday - 20) / 365))
                                   + rb.normal(0, 60)))
                ls, gs = bill_lines(code, c, th)
                etot, gtot = round(sum(x[3] for x in ls), 2), round(sum(x[3] for x in gs), 2)
                f25 = frac_2025(c["from"], c["to"])
                tr["utility_charges"] += f25 * etot
                tr["use_kwh"] += f25 * c["kwh"]
                via_service = on_service and bdate >= GOLIVE[code]
                direct = not via_service
                if via_service and first_after and code in PAID_TWICE:
                    direct = True                # the bill reached Corvane before the address change and AP paid it
                    tr["paid_twice"] = dict(bill=bno, amount=etot + gtot, period=(c["from"], c["to"]))
                if direct:
                    for k, (desc, qty, uom, amt) in enumerate(ls + gs):
                        lines.append(dict(vendor=VENDOR_NO[code], vendor_name=s["utility"], invoice=bno, invoice_date=bdate,
                                          store=s["store"], account=acct, meter=gas_no if desc.startswith("Gas") else mno,
                                          service_from=c["from"], service_to=c["to"], line=k + 1, desc=desc, qty=qty,
                                          uom=uom, amount=amt, code=code, kind="utility"))
                if via_service:
                    due_e, due_g = etot, gtot
                    if first_after and code in PAID_TWICE:
                        credit = etot + gtot     # the service paid the same bill; the utility holds the overpayment
                    elif credit > 0:
                        take = min(credit, etot)
                        due_e, credit = round(etot - take, 2), round(credit - take, 2)
                        tr["credit"] += take
                    paid = rb.integers(2, 5)
                    fund = friday_after(bdate + dt.timedelta(days=int(paid)))
                    parts = [("electric", due_e, mno)] + ([("gas", due_g, gas_no)] if gs else [])
                    for what, amt, meter in parts:
                        desc = "%s bill %s dated %s" % (s["utility"], bno, bdate.isoformat())
                        if gs:
                            desc += ", %s service" % what
                        pay_lines.append(dict(vendor=PAYSERV_NO, vendor_name=PAYSERV, invoice="HUPS-%s" % fund.strftime("%y%m%d"),
                                              invoice_date=fund, store=s["store"], account=acct, meter=meter,
                                              service_from=c["from"], service_to=c["to"], line=0, desc=desc, qty="",
                                              uom="", amount=round(amt, 2), code=code, kind="service"))
                    first_after = False
            # the supplier: one invoice per meter per read cycle, on the utility's reads (sent to it after each read);
            # its second term applies from the first cycle beginning on or after 1 July 2025
            for m in range(1, 13):
                tr["months"][m - 1] += allocate(cycles, *month_bounds(2025, m)) / 1000.0
            for c in cycles:
                idate = c["read"] + dt.timedelta(days=int(rb.integers(5, 11)))
                if idate > PULL_LAST:
                    continue
                plc = round(0.82 * c["kw"], 1)
                ino = None                       # numbered below, in the supplier's own running sequence
                if c["from"] < TERM2:
                    q = int(round(c["kwh"] * lf))
                    ls = [("Energy - fixed price", q, "KWH", round(q * t["energy"], 2)),
                          ("Renewable portfolio standard cost", q, "KWH", round(q * RPS, 2)),
                          ("Capacity charge", plc, "KW", round(plc * t["cap"], 2))]
                else:
                    q = c["kwh"]
                    ls = [("Energy - fixed price", q, "KWH", round(q * price2, 2)),
                          ("Capacity charge", plc, "KW", round(plc * t["cap"], 2))]
                sub = sum(x[3] for x in ls)
                ls.append(("Sales tax", "", "", round(sub * t["tax"], 2)))
                tr["supplier_charges"] += frac_2025(c["from"], c["to"]) * sum(x[3] for x in ls)
                for k, (desc, qty, uom, amt) in enumerate(ls):
                    lines.append(dict(vendor=SUPPLIER_NO, vendor_name=W.SUPPLIER, invoice=ino, invoice_date=idate,
                                      store=s["store"], account=sup_acct, meter=mno, service_from=c["from"],
                                      service_to=c["to"], line=k + 1, desc=desc, qty=qty, uom=uom, amount=amt, code=code,
                                      kind="supplier"))
        tr["charges"] = tr["utility_charges"] + tr["supplier_charges"]
        truth[code] = tr
    # the supplier numbers its invoices in one running sequence across all its customers, so Corvane's run with gaps
    sup_inv = {}
    for r in lines:
        if r["kind"] == "supplier":
            sup_inv.setdefault((r["invoice_date"], r["store"], r["meter"], r["service_from"]), []).append(r)
    no = int(ra.integers(30100000, 30900000))
    for k in sorted(sup_inv):
        no += int(ra.integers(180, 2600))
        for r in sup_inv[k]:
            r["invoice"] = "AR%08d" % no
    # the payment service's weekly invoices list every Corvane bill it paid that week; the export keeps the eight
    # stores' lines, so their line numbers run with gaps
    by_inv = {}
    for r in pay_lines:
        by_inv.setdefault(r["invoice"], []).append(r)
    for no in sorted(by_inv):
        ln = int(rb.integers(1, 30))
        for r in sorted(by_inv[no], key=lambda r: (r["store"], r["desc"])):
            r["line"] = ln
            ln += int(rb.integers(4, 60))
            lines.append(r)
    lines.sort(key=lambda r: (r["invoice_date"], r["vendor"], r["invoice"], r["line"]))
    return lines, meters, truth
