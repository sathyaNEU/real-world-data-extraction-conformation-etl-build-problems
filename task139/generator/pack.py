"""Cuts the world into the files Copperline's systems write: the contract register, the 2024 crosswalk, the claim
lines, the odometer readings, the cancellation requests, the dealers' remittance bordereaux and the bank's payment
returns, and the dealer directory."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as K
import world as WD

CITIES = ("Fort Worth", "Arlington", "Dallas", "Denton", "Waco", "Abilene", "Wichita Falls", "Tyler", "Lubbock",
          "Amarillo", "Oklahoma City", "Norman", "Tulsa", "Lawton")
OK_CITIES = ("Oklahoma City", "Norman", "Tulsa", "Lawton")
GROUPS = ("Trinity Motor Group", "Brazos Auto Partners", "Independent")


def ids(C):
    """the new administration system's number for every contract and the old one for contracts written before the
    2024 migration"""
    r = K.rng('ids')
    order = sorted(C, key=lambda c: (c.sale, c.cid))
    nxt = 10400000
    for c in order:
        nxt += int(r.integers(1, 4))
        c.new_no = "CV%08d" % nxt
        c.old_no = ("DP-%06d" % (200000 + c.cid * 3 + int(r.integers(0, 3)))) if c.sale < K.MIGRATION else None
    return {c.cid: c for c in C}


def key_on(c, d):
    """the contract number the systems wrote on date d"""
    return c.old_no if (c.old_no and d < K.MIGRATION) else c.new_no


def register_rows(C):
    rows = []
    for c in sorted(C, key=lambda c: c.new_no):
        rows.append(dict(contract_number=c.new_no, vin=c.vin, channel=c.dealer, sale_date=str(c.sale),
                         odometer_at_sale=int(c.o0), vehicle_class=c.cls, contract_price="%.2f" % c.price,
                         lienholder=c.lien or ""))
    return rows


def crosswalk_rows(C):
    return [dict(old_contract_number=c.old_no, new_contract_number=c.new_no)
            for c in sorted(C, key=lambda c: c.old_no or "") if c.old_no]


def claim_rows(C):
    """repair-order lines: parts and labour, the deductible taken off, a reversal and its correction where a line was
    paid wrong, and goodwill payments the rate manual leaves out of claims cost"""
    r = K.rng('claim_lines')
    rows = []
    cn = 7000000
    facilities = ["RF%03d" % k for k in range(1, 181)]
    comps = ("engine", "transmission", "drive axle", "cooling", "fuel system", "electrical", "steering", "air conditioning")
    for c in C:
        for (d, odo, pay) in c.claims:
            cn += int(r.integers(1, 6))
            claim = "CL%07d" % cn
            gross = pay + K.DEDUCTIBLE
            labour = round(gross * r.uniform(0.35, 0.6), 2)
            parts = round(gross - labour, 2)
            comp = comps[int(r.integers(0, len(comps)))]
            fac = facilities[int(r.integers(0, len(facilities)))]
            paid_on = d + dt.timedelta(days=int(r.integers(2, 21)))
            base = dict(claim_number=claim, contract_number=key_on(c, paid_on), repair_order_date=str(d),
                        repair_odometer=odo, facility=fac, component=comp)
            lines = [("PARTS", parts), ("LABOR", labour), ("DEDUCTIBLE", -K.DEDUCTIBLE)]
            if r.random() < 0.025:                       # a labour line paid at the wrong rate, reversed, re-paid
                wrong = round(labour * r.uniform(1.2, 1.6), 2)
                lines = [("PARTS", parts), ("LABOR", wrong), ("DEDUCTIBLE", -K.DEDUCTIBLE), ("LABOR", -wrong),
                         ("LABOR", labour)]
            for j, (typ, amt) in enumerate(lines, 1):
                rows.append(dict(base, line_number=j, line_type=typ, amount="%.2f" % amt, paid_date=str(paid_on)))
            if r.random() < 0.015:                       # goodwill on a related repair the cover does not include
                rows.append(dict(base, line_number=len(lines) + 1, line_type="GOODWILL",
                                 amount="%.2f" % round(r.uniform(80, 600), 2), paid_date=str(paid_on)))
    rows.sort(key=lambda z: (z['paid_date'], z['claim_number'], z['line_number']))
    return rows


def reading_rows(C):
    """odometer readings: one on every repair order, the owners' maintenance-proof uploads, and Fareline's weekly
    mileage feed (by VIN) for its drivers' cars"""
    r = K.rng('readings')
    rows = []
    for c in C:
        for (d, odo, pay) in c.claims:
            rows.append(dict(source="REPAIR_ORDER", reference=key_on(c, d), reading_date=str(d), odometer=odo))
        if c.channel == "FARELINE":
            d = c.sale + dt.timedelta(days=(7 - c.sale.weekday()) % 7 or 7)
            while d <= c.end:
                rows.append(dict(source="FARELINE_FEED", reference=c.vin, reading_date=str(d),
                                 odometer=int(round(WD.path_odo(c, d)))))
                d += dt.timedelta(days=7)
        else:
            # the CarLink reporter the dealer fits at sale sends the odometer each month while the car is on cover,
            # and stops when the car leaves the owner; a month's report is now and then lost
            d = K.add_months(dt.date(c.sale.year, c.sale.month, 1), 1) - dt.timedelta(days=1)
            while d < c.end:
                if r.random() > 0.03:
                    rows.append(dict(source="CARLINK_MONTHLY", reference=key_on(c, d), reading_date=str(d),
                                     odometer=int(round(min(WD.path_odo(c, d), c.o0 + K.LIMIT)))))
                d = K.add_months(dt.date(d.year, d.month, 1), 2) - dt.timedelta(days=1)
            # the closing report: on the day the cover ends, or the reporter is removed when the car is sold, or the
            # 30 September month-end report for a cover still running
            rows.append(dict(source="CARLINK_MONTHLY", reference=key_on(c, c.end), reading_date=str(c.end),
                             odometer=int(round(min(WD.path_odo(c, c.end), c.o0 + K.LIMIT)))))
            # the owners' maintenance-proof uploads in the app, with the odometer on the receipt
            d = c.sale + dt.timedelta(days=int(r.exponential(200)) + 30)
            while d < c.end:
                odo = int(round(WD.path_odo(c, d)))
                rows.append(dict(source="MAINTENANCE_UPLOAD", reference=key_on(c, d), reading_date=str(d), odometer=odo))
                if r.random() < 0.04:                    # the same receipt uploaded twice
                    rows.append(dict(source="MAINTENANCE_UPLOAD", reference=key_on(c, d), reading_date=str(d),
                                     odometer=odo))
                d += dt.timedelta(days=int(r.exponential(220)) + 40)
    rows.sort(key=lambda z: (z['reading_date'], z['source'], z['reference']))
    return rows


def cancellation_requests(C):
    """requests to cancel a retail contract when its car is sold: the selling dealer's (by contract number, with the
    odometer at trade-in) or the owner's (a private sale), and the lienholder's payoff request (by VIN, no odometer)"""
    r = K.rng('cancels')
    reqs = []
    rid = 50000
    for c in C:
        if c.channel != "DEALER" or c.sold_on is None or c.sold_on < dt.date(2024, 12, 1):
            continue
        odo_sold = int(round(WD.path_odo(c, c.sold_on)))
        mine = []
        traded = r.random() < 0.65
        if traded or c.lien is None or r.random() < 0.6:
            who = "DEALER" if traded else "CUSTOMER"
            lag = int(r.integers(0, 11)) if traded else int(r.integers(2, 26))
            mine.append(dict(requested_by=who, contract_number=c.new_no, vin="", lienholder="",
                             odometer_stated=odo_sold + int(r.integers(0, 40)),
                             received_date=c.sold_on + dt.timedelta(days=lag)))
        if c.lien is not None:
            mine.append(dict(requested_by="LIENHOLDER", contract_number="", vin=c.vin, lienholder=c.lien,
                             odometer_stated="", received_date=c.sold_on + dt.timedelta(days=int(r.integers(5, 51)))))
        for q in mine:
            if q['received_date'] > K.VALUATION:
                continue
            rid += int(r.integers(1, 4))
            q['request_id'] = "CR%06d" % rid
            q['reason'] = "vehicle sold" if q['requested_by'] != "LIENHOLDER" else "loan payoff"
            q['cid'] = c.cid
            reqs.append(q)
    reqs.sort(key=lambda z: (z['received_date'], z['request_id']))
    return reqs


def cancel_rows(reqs):
    return [dict(request_id=q['request_id'], received_date=str(q['received_date']), requested_by=q['requested_by'],
                 contract_number=q['contract_number'], vin=q['vin'], lienholder=q['lienholder'],
                 odometer_stated=q['odometer_stated'], reason=q['reason']) for q in reqs]


def dealer_rows(C):
    r = K.rng('dealers')
    codes = sorted({c.dealer for c in C if c.channel == "DEALER"})
    rows = []
    used = set()
    for code in codes:
        g = GROUPS[int(r.choice(3, p=[0.25, 0.25, 0.5]))]
        while True:
            nm = "%s %s %s" % (["Lone Star", "Red River", "Prairie", "Crossroads", "Bluebonnet", "Frontier", "Mesa",
                                "Cedar Creek", "Pecan Valley", "Sooner", "Big Country", "Llano"][int(r.integers(0, 12))],
                               ["Ford", "Chevrolet", "Toyota", "Nissan", "Hyundai", "Honda", "Kia", "Auto"][int(r.integers(0, 8))],
                               ["Motors", "Auto Sales", "Pre-Owned", "Autoplex", "Car Center"][int(r.integers(0, 5))])
            if nm not in used:
                used.add(nm)
                break
        rows.append(dict(dealer_code=code, dealer_name=nm,
                         city=CITIES[int(r.integers(0, len(CITIES)))], dealer_group=g, state=""))
        r.random()
        rows[-1]['state'] = "OK" if rows[-1]['city'] in OK_CITIES else "TX"
    return rows


def remittances(C, dealers):
    """each dealer remits monthly for the contracts it sold, on a bordereau in its group's layout; a dealer-month's
    payment the bank returns unpaid is listed in the returns file, and about half are paid again on a later
    bordereau"""
    r = K.rng('remit')
    group = {d['dealer_code']: d['dealer_group'] for d in dealers}
    lines = []
    for c in C:
        if c.channel != "DEALER" or not (dt.date(2024, 11, 1) <= c.sale <= K.VALUATION):
            continue
        lag = 1 if r.random() < 0.88 else 2
        m = K.add_months(dt.date(c.sale.year, c.sale.month, 1), lag)
        lines.append(dict(c=c, month=m))
    by = {}
    for ln in lines:
        by.setdefault((ln['c'].dealer, ln['month']), []).append(ln)
    out, returns = [], []
    for (dealer, month), lns in sorted(by.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        if month > dt.date(2026, 9, 1):
            continue
        ref = "ACH%s%s" % (dealer[1:], month.strftime("%y%m"))
        returned = r.random() < 0.06
        for ln in lns:
            out.append(dict(c=ln['c'], month=month, ref=ref, group=group[dealer], dealer=dealer))
        if returned:
            settled = month + dt.timedelta(days=int(r.integers(3, 9)))
            ret_on = settled + dt.timedelta(days=int(r.integers(2, 6)))
            returns.append(dict(trace_number="0210%09d" % int(r.integers(10 ** 8, 10 ** 9)), dealer=dealer,
                                amount="%.2f" % round(sum(ln['c'].price for ln in lns), 2), settled_on=str(settled),
                                returned_on=str(ret_on), ref=ref,
                                return_code=["R01 insufficient funds", "R02 account closed", "R08 payment stopped"][int(r.integers(0, 3))]))
            if r.random() < 0.5:
                m2 = K.add_months(month, int(r.integers(1, 4)))
                if m2 <= dt.date(2026, 9, 1):
                    ref2 = "ACH%s%sR" % (dealer[1:], m2.strftime("%y%m"))
                    for ln in lns:
                        out.append(dict(c=ln['c'], month=m2, ref=ref2, group=group[dealer], dealer=dealer))
    return out, returns


def bordereau_sheets(out):
    """three layouts: Trinity Motor Group's (contract number, dollars), Brazos Auto Partners' (contract number, cents,
    its own deal number), the independents' standard form (VIN, sale date day first, dollars)"""
    r = K.rng('bdx')
    sheets = {"Trinity Motor Group": [], "Brazos Auto Partners": [], "Independent dealers": []}
    for x in sorted(out, key=lambda z: (z['month'], z['dealer'], z['c'].new_no, z['ref'])):
        c = x['c']
        if x['group'] == "Trinity Motor Group":
            sheets["Trinity Motor Group"].append([x['month'].strftime("%Y-%m"), x['dealer'], c.new_no, str(c.sale),
                                                  c.price, x['ref']])
        elif x['group'] == "Brazos Auto Partners":
            sheets["Brazos Auto Partners"].append([x['month'].strftime("%b %Y"), x['dealer'],
                                                   "BAP-%05d" % (c.cid % 99991), c.new_no, int(round(c.price * 100)),
                                                   x['ref']])
        else:
            sheets["Independent dealers"].append([x['dealer'], c.vin, c.sale.strftime("%d/%m/%Y"), c.price,
                                                  x['month'].strftime("%m/%Y"), x['ref']])
    heads = {"Trinity Motor Group": ["Bordereau month", "Dealer", "Contract No", "Sale date", "Remitted (USD)",
                                     "Payment ref"],
             "Brazos Auto Partners": ["Period", "Dealer code", "BAP deal no", "Copperline contract", "Remit (cents)",
                                      "ACH reference"],
             "Independent dealers": ["Dealer", "VIN", "Date of sale", "Amount", "Remittance month", "Payment reference"]}
    return sheets, heads


def return_rows(returns, dealers):
    """the bank's ACH returns report: its own trace number, the originator's account name as the bank holds it, the
    amount and dates; nothing on it carries Copperline's bordereau reference"""
    name = {d['dealer_code']: d['dealer_name'] for d in dealers}
    rows = [dict(trace_number=x['trace_number'], originator_name=name[x['dealer']].upper(), amount=x['amount'],
                 settlement_date=x['settled_on'], return_date=x['returned_on'], return_reason=x['return_code'])
            for x in returns]
    rows.sort(key=lambda z: (z['return_date'], z['trace_number']))
    return rows


def facility_rows():
    r = K.rng('facilities')
    rows = []
    for k in range(1, 181):
        rows.append(dict(facility="RF%03d" % k, city=CITIES[int(r.integers(0, len(CITIES)))],
                         facility_type=["franchised dealer", "independent shop", "transmission specialist"][int(r.choice(3, p=[0.45, 0.45, 0.10]))],
                         labor_rate_usd_per_hour="%.2f" % round(r.uniform(98, 168), 2),
                         in_network="Y" if r.random() < 0.8 else "N"))
    return rows
