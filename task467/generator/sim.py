"""The clean truth: Wrenfield & Holt's returned orders, every parcel's delivery to the Cotterby returns centre, the
hall's working (block-stacked roll cages, so the next parcel opened is always the newest still waiting), the processing
and refund records, the customer cases, goodwill vouchers and their redemptions, and the centre's operating records.

Everything is integer seconds of UK local wall-clock time (naive) until the writers in pack.py stamp a zone.
Random streams are separate per concern, so a change to one record family leaves the others byte-identical."""
import datetime as dt
from collections import defaultdict

import numpy as np

import world as W

EPOCH = dt.datetime(2024, 11, 1)


def sec(t):
    return int((t - EPOCH).total_seconds())


def at(s):
    return EPOCH + dt.timedelta(seconds=int(s))


def day_of(s):
    return at(s).date()


def rng(name):
    return np.random.default_rng([W.SEED, sum(ord(c) * (i + 1) for i, c in enumerate(name))])


# ----------------------------------------------------------------------------------------------- the operating profile
def arrivals_base(d):
    """Return parcels delivered to the centre per working day (before the Monday uplift)."""
    y, m, dd = d.year, d.month, d.day
    if (y, m) == (2024, 12):
        return 470 if dd <= 21 else 360
    if (y, m) == (2025, 1):
        return 760 if dd <= 25 else 600
    if (y, m) == (2025, 2):
        return 520
    if (y, m) in ((2025, 7),):
        return 540
    if (y, m) == (2025, 11):
        return 500 if dd <= 22 else 650
    if (y, m) == (2025, 12):
        return 680 if dd <= 20 else 400
    if (y, m) == (2026, 1):
        return 930
    if (y, m) == (2026, 2):
        return 640 if dd <= 14 else 520
    if (y, m) == (2026, 5):
        return 640 if 11 <= dd <= 30 else 500
    if (y, m) == (2026, 7):
        return 580
    return 490


def capacity_base(d):
    """Parcels the centre's team opens per full working day."""
    y, m = d.year, d.month
    table = {(2024, 12): 560, (2025, 1): 690, (2025, 2): 620, (2025, 11): 590, (2025, 12): 600,
             (2026, 1): 560, (2026, 2): 640, (2026, 3): 660, (2026, 4): 600, (2026, 5): 580}
    return table.get((y, m), 560)


def working(d):
    return d.weekday() < 6 and d not in W.BANK_HOLIDAYS


def payment_run_day(d):
    return d.weekday() < 5 and d not in W.BANK_HOLIDAYS


def next_run(s):
    """Refunds go out in the 18:00 payment run on weekdays; a refund triggered after the run waits for the next."""
    t = at(s)
    d = t.date()
    if payment_run_day(d) and t.time() < dt.time(18, 0):
        return d
    d += dt.timedelta(days=1)
    while not payment_run_day(d):
        d += dt.timedelta(days=1)
    return d


# ------------------------------------------------------------------------------------------------ the record family
def deliveries():
    """Each return parcel's goods-in time (seconds), carrier and door; 07:00 to 17:30 on delivery days."""
    r = rng("deliveries")
    out = []
    for d in W.days():
        if not working(d):
            continue
        n = r.poisson(arrivals_base(d) * (1.22 if d.weekday() == 0 else 1.0))
        base = sec(dt.datetime.combine(d, dt.time(7, 0)))
        secs = np.sort(r.choice(10 * 3600 + 1800, size=n, replace=False)) + base
        out.extend(int(s) for s in secs)
    return np.array(out, dtype=np.int64)


def processing_slots(deliv):
    """The team's opening slots: weekdays 06:00 to 22:00, Saturdays 07:00 to 17:00, Sundays and bank holidays
    08:00 to 14:00 at six tenths of the day's capacity. A slot opens a parcel only when the hall holds one."""
    r = rng("slots")
    taken = set(int(x) for x in deliv)
    out = []
    for d in W.days():
        cap = capacity_base(d)
        if d.weekday() == 6 or d in W.BANK_HOLIDAYS:
            n, h0, span = int(r.normal(0.6 * cap, 12)), 8, 6 * 3600
        elif d.weekday() == 5:
            n, h0, span = int(r.normal(0.85 * cap, 15)), 7, 10 * 3600
        else:
            n, h0, span = int(r.normal(cap, 18)), 6, 16 * 3600
        base = sec(dt.datetime.combine(d, dt.time(h0, 0)))
        for s in np.sort(r.choice(span, size=max(n, 0), replace=False)) + base:
            s = int(s)
            while s in taken:          # no slot shares a second with a goods-in scan
                s += 1
            taken.add(s)
            out.append(s)
    return np.array(sorted(out), dtype=np.int64)


def hall(deliv, slots, discipline="newest"):
    """Replay the hall: deliveries join, slots open the newest waiting parcel (block-stacked cages) or, for the
    rungs, the oldest. Returns (slot seconds, parcel index) for every slot that opened a parcel."""
    ev = [(int(s), 0, i) for i, s in enumerate(deliv)] + [(int(s), 1, j) for j, s in enumerate(slots)]
    ev.sort()
    stack, out, head = [], [], 0
    for t, kind, i in ev:
        if kind == 0:
            stack.append(i)
        elif discipline == "newest":
            if stack:
                out.append((t, stack.pop()))
        else:
            if head < len(stack):
                out.append((t, stack[head]))
                head += 1
    return out


def everything():
    """The whole clean truth as plain Python structures."""
    deliv = deliveries()
    slots = processing_slots(deliv)
    opened = hall(deliv, slots)
    n = len(deliv)
    r = rng("orders")
    # customers: a returning customer base, a tenth of it on the Irish site in euros
    n_cust = int(n * 0.74)
    cust_site = np.where(r.random(n_cust) < 0.12, "IE", "UK")
    cust_ids = r.choice(np.arange(1_200_000, 9_999_999), size=n_cust, replace=False)
    # each parcel is one returned order; a customer returns about 1.35 orders over the record
    pcust = r.integers(0, n_cust, size=n)
    deliv_days = np.array([day_of(s) for s in deliv])
    transit = r.choice([1, 1, 2, 2, 2, 3, 3, 4], size=n)
    keep_days = r.choice(np.arange(1, 26), size=n, p=np.r_[np.full(10, 0.06), np.full(15, 0.4 / 15)])
    ship_days = r.choice([1, 2, 2, 3], size=n)
    posted = deliv - (transit * 86400 + r.integers(0, 6 * 3600, size=n) + 9 * 3600)
    ordered = posted - (keep_days + ship_days) * 86400 - r.integers(0, 14 * 3600, size=n)
    totals = np.round(np.exp(r.normal(4.05, 0.55, size=n)), 2)
    # order references: allocated in order time across returned and other orders (assigned below)
    parcels = {"deliv": deliv, "cust": pcust, "posted": posted, "ordered": ordered, "total": totals,
               "deliv_day": deliv_days}
    # carriers and barcodes: prepaid Tarnwell labels for parcels posted on labels issued to 31 December 2025
    rb = rng("barcodes")
    label_issue = posted - r.integers(2 * 3600, 3 * 86400, size=n)
    has_label = np.array([day_of(s) <= W.LABELS_END for s in label_issue])
    carrier, barcode = [], []
    used = set()

    def fresh(fmt):
        while True:
            c = fmt(rb)
            if c not in used:
                used.add(c)
                return c
    for i in range(n):
        if has_label[i]:
            carrier.append("Tarnwell")
            barcode.append(fresh(lambda q: "TW%012d" % q.integers(10 ** 11, 10 ** 12)))
        else:
            c = rb.choice([c for c, _ in W.CARRIERS_2026], p=[p for _, p in W.CARRIERS_2026])
            carrier.append(str(c))
            if c == "Ambrell Post":
                barcode.append(fresh(lambda q: "AP%09dGB" % q.integers(10 ** 8, 10 ** 9)))
            elif c == "Tarnwell":
                barcode.append(fresh(lambda q: "TW%012d" % q.integers(10 ** 11, 10 ** 12)))
            elif c == "Kestrix":
                barcode.append(fresh(lambda q: "KX%010d" % q.integers(10 ** 9, 10 ** 10)))
            else:
                barcode.append(fresh(lambda q: "VP%dX%06d" % (q.integers(10, 99), q.integers(10 ** 5, 10 ** 6))))
    parcels["carrier"] = carrier
    parcels["barcode"] = barcode
    parcels["label"] = [barcode[i] if has_label[i] else "" for i in range(n)]
    parcels["label_issue"] = label_issue
    parcels["door"] = rb.choice(["D1", "D2", "D3", "D4"], size=n, p=[0.34, 0.31, 0.22, 0.13])
    # processing outcomes and the refunds they trigger
    ro = rng("outcomes")
    proc_time = np.full(n, -1, dtype=np.int64)
    for t, i in opened:
        proc_time[i] = t
    outcome = ro.choice(["REFUND", "REJECT_RETURNED", "REJECT_DISPOSED"], size=n, p=[0.946, 0.041, 0.013])
    refund_day = [next_run(proc_time[i]) if proc_time[i] >= 0 and outcome[i] == "REFUND" else None for i in range(n)]
    failed = ro.random(n) < 0.012
    reissue_gap = ro.integers(2, 7, size=n)
    reissue_day = []
    for i in range(n):
        if refund_day[i] is None or not failed[i]:
            reissue_day.append(None)
            continue
        d = refund_day[i] + dt.timedelta(days=int(reissue_gap[i]))
        while not payment_run_day(d):
            d += dt.timedelta(days=1)
        reissue_day.append(d)
    # a card refund that fails is reissued in a run the same month, and its reissue never moves it across day 15 of
    # its parcel's count (the failures that would have are paid first time)
    for i in range(n):
        if reissue_day[i] is None:
            continue
        dd = day_of(deliv[i])
        a, b = refund_day[i], reissue_day[i]
        if (a.year, a.month) != (b.year, b.month) or ((a - dd).days >= 15) != ((b - dd).days >= 15):
            reissue_day[i] = None
            failed[i] = False
    made_day = [reissue_day[i] if reissue_day[i] is not None else refund_day[i] for i in range(n)]
    parcels.update({"proc": proc_time, "outcome": outcome, "refund_day": refund_day, "failed": failed,
                    "reissue_day": reissue_day, "made_day": made_day})
    x = {"deliv": deliv, "slots": slots, "opened": opened, "parcels": parcels, "n_cust": n_cust,
         "cust_site": cust_site, "cust_ids": cust_ids}
    other_orders(x)
    cases_and_vouchers(x)
    allocate_order_refs(x)
    return x


# ---------------------------------------------------------------------------- orders, cases, vouchers, redemptions
def other_orders(x):
    """Each returning customer's other orders (about one every three months over the record)."""
    r = rng("other_orders")
    first, last = sec(dt.datetime(2025, 10, 1)), sec(dt.datetime.combine(W.END, dt.time(22)))
    p = x["parcels"]
    y26 = sec(dt.datetime(2026, 1, 1))
    active = sorted(set(int(c) for c, d in zip(p["cust"], p["deliv"]) if d >= y26 - 30 * 86400))
    oc, ot = [], []
    ks = r.poisson((last - first) / 86400 / 110, size=len(active))
    for c, k in zip(active, ks):
        if k:
            oc.extend([c] * int(k))
            ot.extend(int(t) for t in np.sort(r.integers(first, last, size=int(k))))
    x["other"] = {"cust": oc, "ordered": ot, "total": [float(v) for v in np.round(np.exp(r.normal(4.0, 0.6, size=len(oc))), 2)],
                  "kind": ["other"] * len(oc)}


def _order_lists(x):
    """Per customer, every order as (time, key), key ('R', parcel index) or ('O', other-order index)."""
    p, o = x["parcels"], x["other"]
    by = defaultdict(list)
    for i in range(len(p["deliv"])):
        by[int(p["cust"][i])].append((int(p["ordered"][i]), ("R", i)))
    for k in range(len(o["cust"])):
        by[o["cust"][k]].append((o["ordered"][k], ("O", k)))
    for c in by:
        by[c].sort()
    return by


def cases_and_vouchers(x):
    """Customer cases opened in 2026 (a customer waiting on a refund opens a refund-delay case more often the longer
    the wait), goodwill vouchers issued on them (a tenth of the case order's value, whole units of the order's
    currency, 5 to 40; the voucher form's order field defaults to the customer's latest order and the agent changes it
    only when the default is another returned order), vouchers for other reasons, and redemptions, each on a new order
    in the voucher's currency within its 90 days."""
    import bisect
    p, o = x["parcels"], x["other"]
    n = len(p["deliv"])
    rc = rng("cases")
    y26 = sec(dt.datetime(2026, 1, 1))
    endt = sec(dt.datetime.combine(W.END, dt.time(20)))
    cases = []
    for i in range(n):
        if p["outcome"][i] != "REFUND" or p["made_day"][i] is None:
            continue
        paid = sec(dt.datetime.combine(p["made_day"][i], dt.time(18, 5)))
        wait_days = (paid - p["posted"][i]) / 86400
        if wait_days <= 11:
            continue
        if rc.random() >= min(0.78, 0.22 + 0.02 * (wait_days - 11)):
            continue
        opened = int(p["posted"][i] + rc.uniform(10.5, max(11.0, wait_days - 0.3)) * 86400)
        if y26 <= opened <= endt:
            cases.append({"cust": int(p["cust"][i]), "opened": opened, "topic": "Refund delay", "key": ("R", i),
                          "channel": str(rc.choice(["Web form", "Chat", "Email", "Phone"], p=[0.46, 0.27, 0.17, 0.10]))})
    pool = [(int(p["cust"][i]), int(p["ordered"][i]), ("R", i)) for i in range(n)]
    pool += [(o["cust"][k], o["ordered"][k], ("O", k)) for k in range(len(o["cust"]))]
    pool = [a for a in pool if a[1] > sec(dt.datetime(2025, 11, 20))]
    topics = [("Where is my order", 0.30), ("Return label or address", 0.14), ("Exchange", 0.10),
              ("Damaged or faulty item", 0.16), ("Account or payment", 0.13), ("Promotion or price", 0.10),
              ("Delivery delay", 0.07)]
    tw = np.array([b for _, b in topics])
    for j in rc.integers(0, len(pool), size=int(len(cases) * 1.7)):
        c, ot, key = pool[int(j)]
        opened = int(ot + rc.uniform(1, 30) * 86400)
        if y26 <= opened <= endt:
            cases.append({"cust": c, "opened": opened, "key": key if rc.random() > 0.08 else None,
                          "topic": str(rc.choice([a for a, _ in topics], p=tw / tw.sum())),
                          "channel": str(rc.choice(["Web form", "Chat", "Email", "Phone"], p=[0.42, 0.30, 0.16, 0.12]))})
    cases.sort(key=lambda cs: (cs["opened"], cs["cust"]))
    seq = 5_100_000
    for cs in cases:
        seq += int(rc.integers(1, 3))
        cs["case_ref"] = "CS-%07d" % seq
        cs["closed"] = cs["opened"] + int(rc.uniform(0.2, 9) * 86400)
    rv, rr = rng("vouchers"), rng("redemptions")
    orders = _order_lists(x)
    total = lambda key: float(p["total"][key[1]]) if key[0] == "R" else o["total"][key[1]]
    vouchers, reds = [], []
    for cs in cases:
        reason = None
        if cs["topic"] == "Refund delay":
            if (cs["opened"] - p["posted"][cs["key"][1]]) / 86400 >= 14 and rv.random() < 0.66:
                reason = "Refund delay"
        elif cs["topic"] in ("Delivery delay", "Where is my order") and rv.random() < 0.20:
            reason = "Delivery delay"
        elif cs["topic"] == "Damaged or faulty item" and rv.random() < 0.25:
            reason = "Damaged item"
        elif cs["topic"] in ("Promotion or price", "Account or payment") and rv.random() < 0.08:
            reason = "Other"
        if reason is None:
            continue
        issued = cs["opened"] + int(rv.uniform(0.05, 2.2) * 86400)
        base = total(cs["key"]) if cs["key"] else float(np.round(np.exp(rv.normal(4.0, 0.5)), 2))
        base = base * (1.16 if x["cust_site"][cs["cust"]] == "IE" else 1.0)     # the order's value in its currency
        hist = orders[cs["cust"]]
        pos = bisect.bisect_right(hist, (issued, ("~", 0)))
        latest = hist[pos - 1][1] if pos else None
        auto = latest
        if latest is not None and latest[0] == "R" and cs["key"] is not None and latest != cs["key"]:
            auto = cs["key"]          # the default was another returned order: the agent picks the case's order
        v = {"case": cs["case_ref"], "cust": cs["cust"], "issued": issued, "reason": reason,
             "value": int(min(40, max(5, round(0.10 * base)))), "case_key": cs["key"], "auto_key": auto}
        vouchers.append(v)
        if rr.random() < 0.57:
            t = issued + int(rr.uniform(0.5, 88) * 86400)
            if t <= endt:
                tot = float(np.round(np.exp(rr.normal(4.15, 0.5)), 2))
                part = rr.random() < 0.18
                cur = 1.16 if x["cust_site"][cs["cust"]] == "IE" else 1.0
                applied = round(min(v["value"], tot * cur) * (rr.uniform(0.35, 0.8) if part else 1.0), 2)
                reds.append({"voucher": v, "t": t, "applied": applied, "total": tot, "cust": cs["cust"]})
                if part and rr.random() < 0.55:
                    t2 = t + int(rr.uniform(2, 40) * 86400)
                    if t2 <= min(endt, issued + 89 * 86400):
                        tot2 = float(np.round(np.exp(rr.normal(4.15, 0.5)), 2))
                        reds.append({"voucher": v, "t": t2, "applied": round(min(v["value"] - applied, tot2 * cur), 2),
                                     "total": tot2, "cust": cs["cust"]})
    # each redemption is a new order of the customer's, which later vouchers' order field can default to
    for d in sorted(reds, key=lambda d: d["t"]):
        k = len(o["cust"])
        o["cust"].append(d["cust"])
        o["ordered"].append(d["t"] - int(rr.integers(30, 600)))
        o["total"].append(d["total"])
        o["kind"].append("redemption")
        d["order_key"] = ("O", k)
    x["cases"], x["vouchers"], x["redemptions"] = cases, vouchers, reds
    # the vouchers' order field had to see the redemption orders placed before each voucher; recompute it now that
    # every order exists (the case order and the redemptions are unchanged)
    orders = _order_lists(x)
    for v in vouchers:
        hist = orders[v["cust"]]
        pos = bisect.bisect_right(hist, (v["issued"], ("~", 0)))
        latest = hist[pos - 1][1] if pos else None
        auto = latest
        if latest is not None and latest[0] == "R" and v["case_key"] is not None and latest != v["case_key"]:
            auto = v["case_key"]
        v["auto_key"] = auto
    rv2 = rng("voucher_codes")
    vseq = 41_000
    for v in sorted(vouchers, key=lambda v: v["issued"]):
        vseq += int(rv2.integers(1, 4))
        v["code"] = "GW%06d" % vseq
        v["expires"] = (at(v["issued"]) + dt.timedelta(days=90)).date()
    rseq = 880_000
    for d in sorted(reds, key=lambda d: d["t"]):
        rseq += int(rv2.integers(1, 5))
        d["id"] = "RD%07d" % rseq


CATEGORIES = [("Womenswear", 0.31, 0.40), ("Menswear", 0.18, 0.17), ("Footwear", 0.14, 0.16),
              ("Home", 0.17, 0.11), ("Kids", 0.11, 0.09), ("Accessories", 0.09, 0.07)]


def allocate_order_refs(x):
    """Order references run in order time across every order; each order carries its main product category (returned
    orders lean to clothing and footwear)."""
    p, o = x["parcels"], x["other"]
    n = len(p["deliv"])
    rcat = rng("categories")
    names = [c for c, _, _ in CATEGORIES]
    p["category"] = list(rcat.choice(names, size=n, p=[r for _, _, r in CATEGORIES]))
    o["category"] = list(rcat.choice(names, size=len(o["cust"]), p=[a for _, a, _ in CATEGORIES]))
    keys = [("R", i) for i in range(n)] + [("O", k) for k in range(len(o["cust"]))]
    times = [int(p["ordered"][i]) for i in range(n)] + list(o["ordered"])
    order = sorted(range(len(keys)), key=lambda j: (times[j], j))
    r = rng("order_refs")
    gaps = r.integers(1, 4, size=len(keys))
    num, ref = 20_418_000, {}
    for k, j in enumerate(order):
        num += int(gaps[k])
        ref[keys[j]] = "WH%08d" % num
    x["ref"] = ref
    p["order_ref"] = [ref[("R", i)] for i in range(n)]
    o["order_ref"] = [ref[("O", k)] for k in range(len(o["cust"]))]
