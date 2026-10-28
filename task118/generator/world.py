"""The States of Eskerholm's five excise duties: their duty and GST history, the quarterly clearances and prices the
Statistics Office publishes (a partial-adjustment demand at constant 2026 prices), and Customs' line-level declarations
for July 2025 to September 2026 with the excise accounted on releases from bonded warehouses (the asks' truth)."""
import datetime as dt
from decimal import ROUND_HALF_UP, Decimal
import zoneinfo

import numpy as np

import params as P

D = dt.timedelta
LONDON = zoneinfo.ZoneInfo("Europe/London")
UTC = dt.timezone.utc


def qlabel(t):
    return "%dQ%d" % (P.FIRST_YEAR + t // 4, t % 4 + 1)


def qstart(t):
    return dt.date(P.FIRST_YEAR + t // 4, 3 * (t % 4) + 1, 1)


def gst(t):
    return 0.03 if t < P.GST_FROM else P.GST


def series():
    """for each duty: the duty rate in force each quarter (Budget changes on 1 January), producer real costs, the retail
    price at constant 2026 prices and the quarterly volume"""
    rs = np.random.default_rng(P.SEED)
    out = {}
    T = P.QUARTERS
    for code, name, unit, q_year, c26, d26, beta, lam in P.DUTIES:
        d = np.zeros(T)
        d[-1] = d26
        steps = []
        vals, pr = P.STEPS.get(code, P.STEPS_DEFAULT)
        for t in range(T - 2, -1, -1):
            jan = (t + 1) % 4 == 0
            step = float(rs.choice(vals, p=pr)) if jan else 0.0
            d[t] = d[t + 1] / (1 + step)
            if jan and step != 0.0:
                steps.append((qstart(t + 1), step))
        x, dev = 0.0, np.zeros(T)
        for t in range(T):
            x = 0.7 * x + rs.normal(0, P.SHOCK[code])
            dev[t] = x
        c = c26 * np.exp(dev - dev[-1])
        price = np.array([(c[t] + d[t]) * (1 + gst(t)) for t in range(T)])
        lnP = np.log(price)
        lr = beta / (1 - lam)
        a = np.log(q_year / 4) - lr * lnP[-1]
        lnQ = np.zeros(T)
        lnQ[0] = a + lr * lnP[0]
        seas = P.SEASON[code]
        for t in range(1, T):
            mu = (1 - lam) * a + beta * lnP[t] + lam * lnQ[t - 1]
            lnQ[t] = mu + seas[t % 4] - lam * seas[(t - 1) % 4] + rs.normal(0, P.NOISE[code])
        out[code] = dict(name=name, duty=d, cost=c, price=price, volume=np.exp(lnQ), steps=sorted(steps))
    return out


def money(x, dp):
    """half-up rounding on the decimal value, as a rate is set"""
    q = Decimal(1).scaleb(-dp)
    return float(Decimal(repr(float(x))).quantize(q, rounding=ROUND_HALF_UP))


def rate_history(S):
    """duty rate changes as the Budgets made them (effective dates) and the 2027 rates already set before any Budget
    measure: alcohol to the penny a litre, road fuel to a hundredth of a penny"""
    rows = []
    for code, name, unit, *_ in P.DUTIES:
        dp = 4 if code == "FUEL" else 2
        d = S[code]["duty"]
        rows.append((code, dt.date(2008, 1, 1), money(d[0], dp)))
        for t in range(1, P.QUARTERS):
            if abs(d[t] - d[t - 1]) > 1e-12:
                rows.append((code, qstart(t), money(d[t], dp)))
        rows.append((code, dt.date(2027, 1, 1), money(money(d[-1], dp) * P.UPRATE_2027, dp)))
    return rows


# ------------------------------------------------------------------------------------------------- the declarations

CPC = [  # code, description, duty
    ("4000", "Entry for free circulation and home use, duty paid on import", "payable"),
    ("7100", "Entry of goods into an excise warehouse, duty suspended", "suspended"),
    ("4071", "Release from an excise warehouse for home use, duty payable", "payable"),
    ("7171", "Removal from one excise warehouse to another, duty suspended", "suspended"),
    ("3171", "Export or removal out of Eskerholm from an excise warehouse, duty suspended", "suspended"),
    ("6171", "Repayment of duty on goods returned to an excise warehouse or destroyed after release", "repayment"),
]

WAREHOUSES = [  # id, name, premises, goods, approved from (None: drawn), approval ended
    ("EKW087", "Lower Town Bond", "6 Fish Street, Port Haverel", "Alcohol", dt.date(1994, 4, 1), dt.date(2019, 6, 30)),
    ("EKW094", "Pier Road Bond", "18 Pier Road, Ardvane", "Alcohol", dt.date(1997, 9, 1), dt.date(2021, 3, 31)),
    ("EKW101", "Harbour Bond", "2 Harbour Walk, Port Haverel", "Alcohol", None, None),
    ("EKW108", "Quayside Bonded Stores", "14 Quayside, Port Haverel", "Alcohol", None, None),
    ("EKW115", "Port Haverel Excise Warehouse", "Unit 3, Anchor Way, Port Haverel", "Alcohol", None, None),
    ("EKW122", "Ardvane Bond", "9 Church Street, Ardvane", "Alcohol", None, None),
    ("EKW129", "Northgate Distribution Bond", "Unit 11, Northgate Industrial Estate, Northgate", "Alcohol", None, None),
    ("EKW136", "Airport Bonded Warehouse", "Cargo Centre, Eskerholm Airport", "Alcohol", None, None),
    ("EKW150", "Eskerholm Fuel Terminal", "Terminal Road, Eastquay", "Road fuel", None, None),
    ("EKW157", "Eastquay Tank Farm", "Quay Road, Eastquay", "Road fuel", None, dt.date(2025, 10, 9)),
    ("EKW164", "Moorside Bonded Stores", "Unit 7, Moorside Business Park, Moorside", "Alcohol", None, None),
    ("EKW171", "Marine Parade Bond", "31 Marine Parade, Ardvane", "Alcohol", None, dt.date(2025, 11, 14)),
    ("EKW178", "Ropewalk Bond", "3 Ropewalk, Port Haverel", "Alcohol", None, None),
    ("EKW185", "Moorside Fuel Depot", "Unit 12, Moorside Business Park, Moorside", "Road fuel", None, None),
    ("EKW192", "Airport Fuel Farm", "Fuel Farm Road, Eskerholm Airport", "Road fuel", None, None),
    ("EKW199", "Mill Lane Bond", "4 Mill Lane, Port Haverel", "Alcohol", dt.date(2003, 5, 1), dt.date(2021, 8, 31)),
    ("EKW206", "Mill Lane Bonded Stores", "4 Mill Lane, Port Haverel", "Alcohol", dt.date(2021, 9, 1), None),
]
LAPSED = {"EKW157", "EKW171"}       # approvals that ended inside the extract; removals to them afterwards are releases
ALCOHOL = ("BEER", "CIDR", "WINE", "SPIR")


def warehouses():
    """the register of approved excise warehouses, with two approvals that ended inside the extract"""
    rs = np.random.default_rng(P.SEED + 30)
    out = []
    for wid, name, prem, goods, frm, end in WAREHOUSES:
        if frm is None:
            frm = dt.date(int(rs.integers(1996, 2019)), int(rs.integers(1, 13)), 1)
        out.append(dict(id=wid, name=name, premises=prem, goods=goods, approved=frm, ended=end,
                        fuel=goods == "Road fuel"))
    return out


def approved_on(w, d):
    return w["approved"] <= d and (w["ended"] is None or d < w["ended"])


def quarter_of(d):
    return "%dQ%d" % (d.year, (d.month - 1) // 3 + 1)


def declarations(S, rates):
    """line-level declarations, 1 July 2025 to 30 September 2026, one row per item, the declaration's duty on every
    item row, acceptance times in UTC; and the excise accounted for on releases by duty and quarter"""
    rs = np.random.default_rng(P.SEED + 31)
    whs = warehouses()
    traders = ["T%05d" % int(x) for x in rs.choice(np.arange(10000, 99999), size=46, replace=False)]
    table = {}
    for code, start, r in rates:
        table.setdefault(code, []).append((start, r))
    for c in table:
        table[c].sort()

    def rate(code, day):
        if code == "REBF":
            return P.REBATED_RATE
        r = None
        for start, v in table[code]:
            if start <= day:
                r = v
        return r

    def daily(code, day):
        t = (day.year - P.FIRST_YEAR) * 4 + (day.month - 1) // 3
        q0 = dt.date(day.year, 3 * ((day.month - 1) // 3) + 1, 1)
        q1 = dt.date(day.year + (q0.month == 10), (q0.month + 3 - 1) % 12 + 1, 1)
        return S[code]["volume"][min(t, P.QUARTERS - 1)] / (q1 - q0).days

    lines = []
    truth = {code: {q: 0.0 for q in P.ASK_QUARTERS} for code, *_ in P.DUTIES}
    seq = [0]

    def stamp(day, overnight=False):
        """an acceptance time: business hours, a few late-evening postings, and the overnight deferment run"""
        if overnight:
            local = dt.datetime.combine(day, dt.time(0, int(rs.integers(2, 58)), int(rs.integers(0, 60))), LONDON)
        elif rs.random() < 0.04:
            local = dt.datetime.combine(day, dt.time(23, int(rs.integers(5, 59)), int(rs.integers(0, 60))), LONDON)
        else:
            local = dt.datetime.combine(day, dt.time(int(rs.integers(7, 19)), int(rs.integers(0, 60)),
                                                     int(rs.integers(0, 60))), LONDON)
        return local.astimezone(UTC)

    def add(cpc, items, day, wh_from, wh_to, trader, mop, duty_day, ref="", status="ACCEPTED", decl=None,
            when=None, suspended=False):
        """items: [(duty code, litres)]; the declaration's duty is the sum of its items' duty, each at the rate in
        force on duty_day, and the extract carries it on every item row"""
        if decl is None:
            seq[0] += 1
            decl = "CE%09d" % ((seq[0] * 387420489 + 104729) % 10 ** 9)   # unique: the multiplier is prime to 10
        when = when or stamp(day)
        item_duty = [round(q * rate(c, duty_day), 2) for c, q in items] if (cpc in ("4000", "4071", "6171") or
                                                                           suspended) else [0.0] * len(items)
        total = round(sum(item_duty), 2)
        rows = []
        for k, (c, q) in enumerate(items, 1):
            rows.append(dict(declaration=decl, item=k, cpc=cpc, duty_code=c, accepted_utc=when,
                             trader=trader, warehouse_from=wh_from, warehouse_to=wh_to, quantity_litres=q,
                             method_of_payment=mop, duty_gbp=total, reference=ref, status=status))
        lines.extend(rows)
        return rows, item_duty

    def litres(code, day, k):
        return max(1, int(round(daily(code, day) * rs.gamma(3.0, 1.0 / 3.0) / k)))

    N = {"FUEL": 32.0}
    K = {"FUEL": N["FUEL"] * 0.49 * 0.945}
    for c in ALCOHOL:
        N[c] = 30.0
        K[c] = N[c] * 0.60 * 1.10
    day = P.DECL_FROM
    while day <= P.DECL_TO:
        for code, *_ in P.DUTIES:
            fuel = code == "FUEL"
            src = [w for w in whs if w["fuel"] == fuel and approved_on(w, day)]
            n = int(rs.poisson(N[code]))
            for _ in range(n):
                qty = litres(code, day, K[code])
                trader = traders[int(rs.integers(0, len(traders)))]
                w = src[int(rs.integers(0, len(src)))]
                kind = rs.random()
                if kind < (0.06 if fuel else 0.25):            # duty paid on import
                    add("4000", [(code, qty)], day, "", "", trader, "IMMEDIATE", day)
                elif kind < (0.50 if fuel else 0.55):          # into bond
                    add("7100", [(code, int(qty * 1.4))], day, "", w["id"], trader, "SUSPENDED", day, suspended=True)
                elif kind < (0.93 if fuel else 0.90):          # release from bond for home use
                    items = [(code, qty)]
                    if fuel and rs.random() < 0.25:            # marked gas oil on the same load
                        items.append(("REBF", max(1, int(qty * rs.uniform(0.25, 0.6)))))
                    elif not fuel and rs.random() < 0.15:      # a mixed alcohol load
                        others = [c for c in ALCOHOL if c != code]
                        for c in rs.choice(others, size=int(rs.integers(1, 3)), replace=False):
                            items.append((str(c), litres(str(c), day, K[str(c)])))
                    order = list(rs.permutation(len(items))) if (not fuel or rs.random() < 0.2) else list(range(len(items)))
                    items = [items[i] for i in order]
                    deferred = rs.random() < 0.8
                    mop = "DEFERMENT" if deferred else "IMMEDIATE"
                    when = stamp(day, overnight=deferred and rs.random() < 0.35)
                    rows, duties = add("4071", items, day, w["id"], "", trader, mop, day, when=when)
                    q = quarter_of(when.astimezone(LONDON).date())
                    if rs.random() < 0.04:                     # cancelled before the goods moved
                        for r_ in rows:
                            r_["status"] = "CANCELLED"
                        continue
                    # corrections: a new declaration naming the one it corrects, at the release day's rates. Keepers
                    # correct within weeks, and correct the last month's releases after their stock counts early in the
                    # next quarter (the year-end count the fullest, the half-year next); Customs' verification corrects
                    # some corrections again.
                    qend = dt.date(day.year + (day.month > 9), (3 * ((day.month - 1) // 3 + 1)) % 12 + 1, 1)
                    recon = (qend - day).days <= 30
                    count = {1: 0.24, 7: 0.14}.get(qend.month, 0.05) if recon else 0.0
                    prev, n_corr = rows[0]["declaration"], 0
                    if rs.random() < 0.05 + count:
                        later = (qend + D(days=int(rs.integers(0, 21)))) if recon else day + D(days=int(rs.integers(3, 40)))
                        while later <= P.DECL_TO and n_corr < 3:
                            j = int(rs.integers(0, len(items)))
                            fix = 1 + float(rs.choice([-0.2, -0.1, -0.05, 0.05, 0.1, 0.25]))
                            items = [(c, max(1, int(round(qv * fix)))) if i == j else (c, qv)
                                     for i, (c, qv) in enumerate(items)]
                            rc, duties = add("4071", items, later, w["id"], "", trader, mop, day, ref=prev)
                            prev, n_corr = rc[0]["declaration"], n_corr + 1
                            if rs.random() >= (0.35 if n_corr == 1 else 0.2):
                                break
                            later = later + D(days=int(rs.integers(10, 50)))
                    for (c, _), dd in zip(items, duties):
                        if c in truth and q in truth[c]:
                            truth[c][q] += dd
                    if rs.random() < 0.025:                    # returned to bond or destroyed: duty repaid
                        later = day + D(days=int(rs.integers(5, 60)))
                        if later <= P.DECL_TO:
                            c0, q0 = items[0]
                            part = max(1, int(round(q0 * float(rs.choice([0.25, 0.5, 1.0])))))
                            rp, rd = add("6171", [(c0, part)], later, "", w["id"], trader, "REPAYMENT", day,
                                         ref=rows[0]["declaration"])
                            q2 = quarter_of(rp[0]["accepted_utc"].astimezone(LONDON).date())
                            if c0 in truth and q2 in truth[c0]:
                                truth[c0][q2] -= rd[0]
                elif kind < (0.98 if fuel else 0.96):          # between warehouses
                    dest = [x for x in whs if x["fuel"] == fuel and approved_on(x, day) and x["id"] != w["id"]]
                    add("7171", [(code, qty)], day, w["id"], dest[int(rs.integers(0, len(dest)))]["id"], trader,
                        "SUSPENDED", day)
                else:                                          # out of Eskerholm
                    add("3171", [(code, qty)], day, w["id"], "", trader, "SUSPENDED", day)
        # removals to premises whose approval had ended: keepers still consigning to them as if they were bonded
        for wl in whs:
            if wl["id"] not in LAPSED or day <= wl["ended"]:
                continue
            for code in (("FUEL",) if wl["fuel"] else ALCOHOL):
                if rs.random() < P.LAPSED_DAILY:
                    src = [x for x in whs if x["fuel"] == wl["fuel"] and approved_on(x, day)]
                    qty = litres(code, day, K[code])
                    rows, _ = add("7171", [(code, qty)], day, src[int(rs.integers(0, len(src)))]["id"], wl["id"],
                                  traders[int(rs.integers(0, len(traders)))], "SUSPENDED", day)
                    q = quarter_of(rows[0]["accepted_utc"].astimezone(LONDON).date())
                    if q in truth[code]:
                        truth[code][q] += round(qty * rate(code, day), 2)
        day += D(days=1)
    # the system posted a batch of rows twice (identical rows)
    dup = [lines[i] for i in rs.choice(len(lines), size=int(len(lines) * 0.012), replace=False)]
    lines.extend(dict(x) for x in dup)
    lines.sort(key=lambda x: (x["accepted_utc"], x["declaration"], x["item"]))
    truth = {c: {q: round(v, 2) for q, v in qs.items()} for c, qs in truth.items()}
    return lines, truth, whs
