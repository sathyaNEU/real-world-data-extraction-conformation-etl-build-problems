"""The three supermarkets' sales feeds as each one's systems write them, cut from the lines' monthly truth: Wrenfold's
weekly file (Sunday to Saturday weeks, values with GST, two February weeks resent after a till fault), Gorsedale's
fiscal-period file (Monday to Sunday weeks in 4-4-5 periods, EANs held as numbers), Calderby's daily point-of-sale
database (three stores, values net of GST, returns as negative units, its own SKUs keyed to GTINs); and the office's
delivery log of every file received."""
import datetime as dt

import numpy as np

import world as W

FY_START = {"FY2026": dt.date(2025, 2, 3), "FY2027": dt.date(2026, 2, 2)}
PERIOD_WEEKS = [4, 4, 5, 4, 4, 5, 4, 4, 5, 4, 4, 5]
FIRST_SAT, LAST_SAT = dt.date(2025, 9, 6), dt.date(2026, 9, 26)
FIRST_SUN, LAST_SUN = dt.date(2025, 9, 7), dt.date(2026, 9, 27)
DOW = [0.12, 0.12, 0.13, 0.14, 0.17, 0.20, 0.12]                  # Monday to Sunday
TILL_FAULT_WEEKS = [dt.date(2026, 2, 14), dt.date(2026, 2, 21)]
TILL_FAULT_RESENT = dt.datetime(2026, 3, 9, 10, 14, 37)


def weeks(first, last):
    out, d = [], first
    while d <= last:
        out.append(d)
        d += dt.timedelta(days=7)
    return out


def fiscal(week_end):
    """Gorsedale's fiscal year, period and week for a week ending on a Sunday."""
    start = week_end - dt.timedelta(days=6)
    fy = "FY2027" if start >= FY_START["FY2027"] else "FY2026"
    wk = (start - FY_START[fy]).days // 7 + 1
    acc, p = 0, 0
    for i, n in enumerate(PERIOD_WEEKS):
        if wk <= acc + n:
            p = i + 1
            break
        acc += n
    return fy, p, wk


def calendar_rows():
    rows = []
    for fy, start in sorted(FY_START.items()):
        for wk in range(1, 53):
            ws = start + dt.timedelta(days=7 * (wk - 1))
            _, p, _ = fiscal(ws + dt.timedelta(days=6))
            rows.append([fy, "P%02d" % p, wk, ws.isoformat(), (ws + dt.timedelta(days=6)).isoformat()])
    return rows


def _split(rng, total, k, p=None):
    if total <= 0:
        return np.zeros(k, dtype=int)
    p = np.full(k, 1.0 / k) if p is None else np.asarray(p) / np.sum(p)
    return rng.multinomial(int(total), p)


def _weekly_value(rng, L, m, units):
    """A week's sales value with GST: member-priced units at the member price."""
    if L["member_price"][m] is not None and units > 0:
        mu = rng.binomial(units, L["member_share"][m])
        return round(mu * L["member_price"][m] + (units - mu) * L["shelf"][m], 2)
    return round(units * L["shelf"][m], 2)


def line_rng(seed, L, k):
    """A line's own stream for a feed, so re-drawing one item's lines leaves every other line's rows unchanged."""
    return np.random.default_rng([seed, k, int(L["gtin"]) % 2147483647, W.NUDGE.get(L["item"], 0)])


def wrenfold(ls, seed):
    wk = weeks(FIRST_SAT, LAST_SAT)
    by_month = {}
    for w in wk:
        by_month.setdefault(W.month_index(w), []).append(w)
    rows = []
    for L in ls:
        if L["retailer"] != "W":
            continue
        rng = line_rng(seed, L, 101)
        for m in range(W.NM):
            if L["units"][m] <= 0:
                continue
            ws = by_month[m]
            for w, u in zip(ws, _split(rng, round(L["units"][m]), len(ws))):
                if u <= 0:
                    continue
                v = _weekly_value(rng, L, m, int(u))
                ext = w + dt.timedelta(days=4)
                if w in TILL_FAULT_WEEKS:
                    lost = int(round(u * rng.uniform(0.09, 0.13)))
                    vu = round(v * (u - lost) / u, 2)
                    rows.append([w.isoformat(), L["gtin"], L["desc"], int(u - lost), vu, ext.isoformat()])
                    rows.append([w.isoformat(), L["gtin"], L["desc"], int(u), v, TILL_FAULT_RESENT.date().isoformat()])
                else:
                    rows.append([w.isoformat(), L["gtin"], L["desc"], int(u), v, ext.isoformat()])
    rows.sort(key=lambda r: (r[5], r[0], r[1]))
    return rows


def gorsedale_desc(desc):
    s = desc.upper().replace(" X", " X").replace("'", "")
    for a, b in (("CHOCOLATE", "CHOC"), ("BISCUITS", "BISC"), ("SPARKLING", "SPKLNG"), ("ORANGE", "ORNG"),
                 ("TOILET TISSUE", "TOILET TIS"), ("CONDITIONER", "CONDTNR"), ("YOGHURT", "YOG"), ("BREAKFAST", "BKFST")):
        s = s.replace(a, b)
    return s[:30]


def gorsedale(ls, seed):
    rng0 = np.random.default_rng([seed, 102])
    wk = weeks(FIRST_SUN, LAST_SUN)
    by_month = {}
    for w in wk:
        by_month.setdefault(W.month_index(w), []).append(w)
    item_no = {}
    rows = []
    for L in ls:
        if L["retailer"] != "G":
            continue
        no = item_no.setdefault(L["gtin"], 400000 + 37 * len(item_no) + int(rng0.integers(0, 30)))
        rng = line_rng(seed, L, 102)
        for m in range(W.NM):
            if L["units"][m] <= 0:
                continue
            ws = by_month[m]
            for w, u in zip(ws, _split(rng, round(L["units"][m]), len(ws))):
                if u <= 0:
                    continue
                fy, p, n = fiscal(w)
                rows.append([fy, "P%02d" % p, n, no, int(L["gtin"]), gorsedale_desc(L["desc"]), int(u),
                             "%.2f" % _weekly_value(rng, L, m, int(u))])
    rows.sort(key=lambda r: (r[0], r[2], r[3]))
    return rows


def calderby(ls, seed):
    """Daily store rows: (sale_date, store_id, sku, units, net_value), and the SKU table."""
    rng0 = np.random.default_rng([seed, 103])
    days_of = {}
    d = dt.date(2025, 9, 1)
    while d <= dt.date(2026, 9, 30):
        days_of.setdefault(W.month_index(d), []).append(d)
        d += dt.timedelta(days=1)
    stores = [s for s, _, _ in W.CALDERBY_STORES]
    share = [w for _, _, w in W.CALDERBY_STORES]
    skus, rows = [], []
    nsku = 0
    for L in ls:
        if L["retailer"] != "C":
            continue
        nsku += 1
        sku = "C%05d" % (21000 + nsku * 7 + int(rng0.integers(0, 5)))
        first = days_of[L["start"]][0] if L["start"] > 0 else dt.date(2023, 3, 1) + dt.timedelta(days=int(rng0.integers(0, 700)))
        rng = line_rng(seed, L, 103)
        skus.append([sku, L["gtin"], L["desc"], first.isoformat()])
        for m in range(W.NM):
            if L["units"][m] <= 0:
                continue
            ds = days_of[m]
            cells = [(day, s) for day in ds for s in stores]
            p = [DOW[day.weekday()] * share[stores.index(s)] for day, s in cells]
            for (day, s), u in zip(cells, _split(rng, round(L["units"][m]), len(cells), p)):
                if u <= 0:
                    continue
                net = round(u * L["shelf"][m] / (1 + W.GST), 2)
                rows.append([day.isoformat(), s, sku, int(u), net])
                if rng.random() < 0.004:
                    rows.append([day.isoformat(), s, sku, -1, -round(L["shelf"][m] / (1 + W.GST), 2)])
    rows.sort(key=lambda r: (r[0], r[1], r[2]))
    return rows, skus


def utc(local):
    """A Kellesay clock time as UTC: the island keeps British time."""
    def last_sunday(y, mo):
        d = dt.date(y, mo, 31)
        return d - dt.timedelta(days=(d.weekday() + 1) % 7)
    y = local.year
    bst = dt.datetime.combine(last_sunday(y, 3), dt.time(1)) <= local < dt.datetime.combine(last_sunday(y, 10), dt.time(2))
    return local - dt.timedelta(hours=1 if bst else 0)


def deliveries(seed, wrows, grows, crows):
    """Every file the office received: Wrenfold's weekly files, Gorsedale's period files, Calderby's monthly extracts."""
    rng = np.random.default_rng([seed, 104])
    out = []
    # Wrenfold: each week's file from its nightly export, the Wednesday or Thursday after the week
    nrows = {}
    for r in wrows:
        nrows[(r[0], r[5])] = nrows.get((r[0], r[5]), 0) + 1
    for (we, ext), n in sorted(nrows.items()):
        w = dt.date.fromisoformat(we)
        if ext == TILL_FAULT_RESENT.date().isoformat():
            local = TILL_FAULT_RESENT
            name = "WRF_SALES_WE%s_R1.csv" % w.strftime("%Y%m%d")
        else:
            lag = 4 + (1 if rng.random() < 0.3 else 0) + (3 if w in (dt.date(2025, 12, 27), dt.date(2026, 1, 3), dt.date(2026, 4, 4)) else 0)
            local = dt.datetime.combine(w + dt.timedelta(days=lag), dt.time(0, 0)) + dt.timedelta(minutes=int(rng.integers(20, 75)))
            name = "WRF_SALES_WE%s.csv" % w.strftime("%Y%m%d")
        out.append(["Wrenfold Stores", name, (w - dt.timedelta(days=6)).isoformat(), w.isoformat(), n,
                    utc(local).strftime("%Y-%m-%dT%H:%M:%SZ")])
    # Gorsedale: one file per fiscal period, from its nightly export a week or so after the period closes
    per = {}
    for r in grows:
        per.setdefault((r[0], r[1]), []).append(r)
    for (fy, p), rs in sorted(per.items()):
        wks = sorted({r[2] for r in rs})
        start = FY_START[fy] + dt.timedelta(days=7 * (wks[0] - 1))
        end = FY_START[fy] + dt.timedelta(days=7 * wks[-1] - 1)
        lag = int(rng.integers(6, 10)) + (5 if end == dt.date(2025, 12, 28) else 0)
        local = dt.datetime.combine(end + dt.timedelta(days=lag), dt.time(0, 0)) + dt.timedelta(minutes=int(rng.integers(5, 55)))
        out.append(["Gorsedale Co-operative", "GORSEDALE_%s_%s.txt" % (fy, p), start.isoformat(), end.isoformat(), len(rs),
                    utc(local).strftime("%Y-%m-%dT%H:%M:%SZ")])
    # Calderby's: a monthly extract of the point-of-sale database; March 2026 sent again with a store's missing days
    mon = {}
    for r in crows:
        mon[r[0][:7]] = mon.get(r[0][:7], 0) + 1
    for ym, n in sorted(mon.items()):
        y, mo = int(ym[:4]), int(ym[5:])
        last = (dt.date(y + (mo == 12), mo % 12 + 1, 1) - dt.timedelta(days=1))
        lag = int(rng.integers(5, 10))
        local = dt.datetime.combine(last + dt.timedelta(days=lag), dt.time(23, 0)) + dt.timedelta(minutes=int(rng.integers(20, 80)))
        first = dt.date(y, mo, 1).isoformat()
        if ym == "2026-03":
            short = n - int(rng.integers(900, 1100))
            out.append(["Calderby's", "calderby_pos_%s.sqlite" % ym, first, last.isoformat(), short,
                        utc(local).strftime("%Y-%m-%dT%H:%M:%SZ")])
            again = dt.datetime(2026, 4, 22, 23, 41, 12)
            out.append(["Calderby's", "calderby_pos_%s_v2.sqlite" % ym, first, last.isoformat(), n,
                        utc(again).strftime("%Y-%m-%dT%H:%M:%SZ")])
        else:
            out.append(["Calderby's", "calderby_pos_%s.sqlite" % ym, first, last.isoformat(), n,
                        utc(local).strftime("%Y-%m-%dT%H:%M:%SZ")])
    out.sort(key=lambda r: r[5])
    return out
