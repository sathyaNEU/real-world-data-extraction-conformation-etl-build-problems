"""task183 asks: the An Post agency's business lodgements for every Lough Ree business account, and the till
service's central Z-report log for every till-service customer. The customers outside the review are simulated
here; the reviewed customers' rows come from sim.py, so both files agree with the main records wherever they meet.

Two systems' own behaviour, nothing planted:
- An Post's counters moved from the older platform to the newer one office by office during the year. The older
  platform writes the whole cash tendered (notes and coin) into the export's notes field and the coin declaration
  into the coin field; the newer one writes notes and coin apart.
- Mobile tills (market stalls, a food truck, event caterers) hold their Z-reports and send them when they next
  connect, so the central log stamps a batch of Z-reports with one received time."""
from __future__ import annotations

import datetime as dt
import random

import sim as S
import world as W

YEAR = (W.REVIEW_START, W.REVIEW_END)
LOG_END = dt.date(2026, 10, 12)          # the till log is pulled on the extract date; last receipts 12 October

# ---- An Post: offices on the older counter platform, and the day each moved to the newer one -------------------
OLD_PLATFORM = {            # office: first day on the newer platform (None: still on the older one at year end)
    "5021": dt.date(2025, 11, 17),
    "4476": dt.date(2026, 1, 19),
    "4521": dt.date(2026, 3, 23),
    "4611": dt.date(2026, 5, 18),
    "4914": dt.date(2026, 7, 13),
    "4709": None,
}


def older_platform(office, d):
    if office not in OLD_PLATFORM:
        return False
    nd = OLD_PLATFORM[office]
    return nd is None or d < nd


AP_STEMS = [("hardware", "Hardware"), ("pharmacy", "Pharmacy"), ("butcher", "Family Butchers"),
            ("florist", "Florists"), ("gifts", "Gift Shop"), ("pub", "Bar"), ("restaurant", "Restaurant"),
            ("vending", "Vending Services"), ("amusements", "Amusements"), ("parking", "Car Parks"),
            ("fuel", "Service Station"), ("hotel", "Hotel"), ("bakery", "Bakery"), ("drapery", "Drapery"),
            ("garden", "Garden Centre"), ("bookmaker", "Turf Accountants"), ("bingo", "Bingo Hall")]
SURNAMES = ["Kearney", "Fallon", "Moran", "Geraghty", "Tiernan", "Feeney", "Gilmartin", "Naughton", "Duignan",
            "Mulvihill", "Egan", "Kilbride", "Hanley", "Brennan", "Quinn", "Durkan", "Rabbitte", "Cuffe", "Hession",
            "Glynn", "Tully", "Nevin", "Costello", "Flanagan", "Keaveney", "Mannion", "Furey", "Garvey", "Lyons",
            "Concannon", "Grealish", "Hannon"]
COIN_HEAVY = {"vending", "amusements", "parking", "bingo"}


def ap_others():
    """The business customers outside the review who lodge at post office counters."""
    r = random.Random(W.SEED + 101)
    out = []
    serial = 12003
    plan = []
    # the older-platform offices each carry six lodgers, the rest of the network three
    for o in W.OFFICES:
        n = 6 if o[0] in OLD_PLATFORM else 3
        plan.extend([o] * n)
    for i, o in enumerate(plan):
        serial += r.choice((5, 7, 9, 11, 13))
        kind, label = AP_STEMS[(i * 7 + 3) % len(AP_STEMS)]
        if o[0] in OLD_PLATFORM and i % 6 in (1, 4):
            kind, label = r.choice([("vending", "Vending Services"), ("amusements", "Amusements"),
                                    ("parking", "Car Parks"), ("bingo", "Bingo Hall")])
        days = sorted(r.sample(range(6), r.choice((1, 2, 2, 3, 3))))
        out.append(dict(cid="BC-%05d" % serial, name="%s %s, %s" % (SURNAMES[i % len(SURNAMES)], label, o[1]),
                        kind=kind, office=o[0], sort=W.BRANCH[o[3]][3], acct="%08d" % r.randint(30000000, 89999999),
                        days=days, mean=round(r.uniform(380, 3600), 2), coin_heavy=kind in COIN_HEAVY,
                        coin_p=r.uniform(0.45, 0.8)))
    return out


AP_OTHERS = ap_others()


def _coin(r, heavy):
    """A coin lodgement in euro: loose coin counted to the 5 cent, never a whole multiple of five euro."""
    while True:
        v = round(r.uniform(150, 900) if heavy else r.uniform(4, 95), 2)
        v = round(round(v / 0.05) * 0.05, 2)
        if abs(v / 5.0 - round(v / 5.0)) > 1e-9:
            return v


def _split(r, amount, heavy, with_coin):
    """Split a lodgement into notes (a whole multiple of five euro) and coin (loose coin, never a whole five)."""
    if not with_coin:
        return float(max(5.0, round(amount / 5.0) * 5.0)), 0.0
    coin = _coin(r, heavy)
    return float(max(0.0, round((amount - coin) / 5.0) * 5.0)), coin


def ap_lodgements():
    """Every business lodgement the post office counters took for the Bank in the review year, as the truth: one
    dict per lodgement with its counter time, office, account and its notes and coin."""
    r = random.Random(W.SEED + 103)
    T = S.truth()
    out = []
    # the reviewed customers' post office lodgements (their amounts are the account file's credits)
    for c in W.CUSTOMERS:
        if c["channel"] != "post":
            continue
        for L in T.cust[c["cid"]]["lodgements"]:
            if not (YEAR[0] <= L["day"] <= YEAR[1]):
                continue
            heavy = c["trade"] == "launderette"
            with_coin = heavy or r.random() < 0.6
            if with_coin:
                target = _coin(r, heavy) if not heavy else round(L["amount"] * r.uniform(0.22, 0.4), 2)
                notes = max(0.0, int((L["amount"] - target) // 5) * 5.0)
                coin = round(L["amount"] - notes, 2)
            else:
                notes = int(L["amount"] // 5) * 5.0
                coin = round(L["amount"] - notes, 2)
            out.append(dict(day=L["day"], time=L["time"], office=L["office"], sort=W.BRANCH[c["home"]][3],
                            acct=c["acct"], notes=notes, coin=coin, review=True))
    # everyone else
    for c in AP_OTHERS:
        for d in W.days(YEAR[0], YEAR[1]):
            if d.weekday() not in c["days"] or d in W.BANK_HOLIDAYS:
                continue
            if r.random() < 0.07:
                continue                                        # a week the business did not get to the counter
            amt = round(c["mean"] * S.lognorm(r, 0.28), 2)
            with_coin = c["coin_heavy"] or r.random() < c["coin_p"]
            notes, coin = _split(r, amt, c["coin_heavy"], with_coin)
            if d.weekday() == 5:
                t = dt.time(9 + r.randint(0, 3), r.randint(0, 59))
            else:
                t = dt.time(9 + r.randint(0, 7), r.randint(0, 59))
                if t.hour == 16 and t.minute > 50:
                    t = dt.time(16, r.randint(0, 50))
            out.append(dict(day=d, time=t, office=c["office"], sort=c["sort"], acct=c["acct"], notes=notes,
                            coin=coin, review=False))
    out.sort(key=lambda x: (x["day"], x["office"], x["time"], x["acct"]))
    return out


AP_HEADER = ["ap_ref", "counter_date", "counter_time", "office_code", "office", "nsc", "account_no", "notes_eur",
             "coin_eur"]


def ap_rows():
    """An Post's export of the Bank's business lodgements. The older platform writes all the cash into notes_eur.
    The file for 21 January 2026 was sent twice and both copies stand in the export."""
    out = []
    seq = {}
    for L in ap_lodgements():
        k = (L["day"], L["office"])
        seq[k] = seq.get(k, 0) + 1
        ref = "%s%s%04d" % (L["office"], L["day"].strftime("%y%m%d"), seq[k])
        notes = L["notes"]
        if older_platform(L["office"], L["day"]):
            notes = round(L["notes"] + L["coin"], 2)
        out.append([ref, L["day"].isoformat(), L["time"].strftime("%H:%M"), L["office"], W.OFFICE[L["office"]][1],
                    L["sort"].replace("-", ""), L["acct"], "%.2f" % notes, "%.2f" % L["coin"]])
    resent = [x for x in out if x[1] == "2026-01-21"]
    out.extend(resent)
    out.sort(key=lambda x: (x[1], x[3], x[0]))
    return out


AP_FEE_PER = 1.15
AP_FEE_RATE = 0.00065


def ap_fee(cash):
    return round(AP_FEE_PER + AP_FEE_RATE * cash + 1e-9, 2)


# ---- the till service ------------------------------------------------------------------------------------------
TILL_STEMS = [  # kind, label, mcc, batch uploader, late closer
    ("restaurant", "Bistro", "5812", False, False), ("pub", "Lounge Bar", "5813", False, True),
    ("bakery", "Bakery", "5462", False, False), ("butcher", "Butchers", "5411", False, False),
    ("florist", "Florist", "5992", False, False), ("gifts", "Gift Shop", "5947", False, False),
    ("hardware", "Hardware", "5251", False, False), ("pharmacy", "Pharmacy", "5912", False, False),
    ("drapery", "Drapery", "5651", False, False), ("books", "Bookshop", "5942", False, False),
    ("restaurant", "Steakhouse", "5812", False, False), ("pub", "Inn", "5813", False, True),
    ("hotelbar", "Hotel Bar", "5813", False, True), ("deli", "Deli", "5499", False, False),
    ("market", "Farm Produce (market stall)", "5499", True, False),
    ("market", "Artisan Cheese (market stall)", "5499", True, False),
    ("foodtruck", "Wood-Fired Pizza (food truck)", "5812", True, False),
    ("market", "Crafts (market stall)", "5999", True, False),
    ("caterer", "Event Catering", "5812", True, False),
    ("market", "Organic Veg (market stall)", "5499", True, False),
]


def till_others():
    r = random.Random(W.SEED + 131)
    out = []
    serial = 13041
    towns = [b for b in W.BRANCHES]
    for i, (kind, label, mcc, batch, late) in enumerate(TILL_STEMS):
        serial += r.choice((6, 8, 12, 14))
        b = towns[(i * 5 + 2) % len(towns)]
        c = dict(cid="BC-%05d" % serial, name="%s %s, %s" % (SURNAMES[(i * 3 + 5) % len(SURNAMES)], label, b[1]),
                 kind=kind, mcc=mcc, batch=batch, late=late, home=b[0],
                 mid="44%08d" % r.randint(10000000, 99999999), tacct="TS-%d" % (700000 + serial),
                 card_day=round(r.uniform(180, 950), 2), k=round(r.uniform(0.35, 1.1) if not batch
                                                                 else r.uniform(0.8, 1.6), 3),
                 z0=r.randint(900, 5200), msc=round(r.uniform(0.006, 0.011), 5))
        if batch:
            c["base_days"] = sorted(r.sample(range(7), r.choice((2, 3, 3, 4))))
        else:
            c["base_days"] = [0, 1, 2, 3, 4, 5] if kind not in ("pub", "hotelbar", "restaurant") else list(range(7))
        out.append(c)
    return out


TILL_OTHERS = till_others()


class TillTruth:
    """Each non-review till customer's trading days and takings, and when each Z-report reached the central log."""

    def __init__(self):
        T = S.truth()
        r = random.Random(W.SEED + 137)
        self.days = {}
        start = dt.date(2025, 1, 1)
        for c in TILL_OTHERS:
            rows = {}
            for d in W.days(start, W.EXPORT_END):
                trade = d.weekday() in c["base_days"]
                if c["batch"]:
                    if trade and r.random() < 0.18:
                        trade = False                         # a market or event the stall skipped
                    if not trade and r.random() < 0.07:
                        trade = True                          # a fair, a festival or a private booking
                else:
                    if d in W.BANK_HOLIDAYS and c["kind"] not in ("pub", "hotelbar", "restaurant"):
                        trade = False
                    if d.month == 12 and d.day in (25, 26):
                        trade = False
                if not trade:
                    continue
                m = T.week_level[d] * S.lognorm(r, 0.22)
                card = round(c["card_day"] * m, 2)
                if card < 25:
                    card = round(25 + r.uniform(0, 30), 2)
                recent = {v["card"] for x, v in rows.items() if (d - x).days <= 60}
                while card in recent:
                    card = round(card + 0.01, 2)
                refund = round(min(card * 0.3, r.uniform(5, 40)), 2) if r.random() < 0.01 else 0.0
                cash = round(c["k"] * card * S.lognorm(r, 0.08), 2)
                paid = round(cash * r.uniform(0.0, 0.03), 2)
                other = round(r.uniform(5, 30), 2) if r.random() < 0.12 else 0.0
                # a mobile trader sometimes takes cards on the portable terminal alone, the till left in the van
                till_used = not (c["batch"] and r.random() < 0.08)
                rows[d] = dict(card=card, refund=refund, cash=cash, paid=paid, other=other, till=till_used)
            self.days[c["cid"]] = rows
        # Z numbers and receipts
        self.z = {}
        rr = random.Random(W.SEED + 139)
        for c in TILL_OTHERS:
            z = c["z0"]
            zs = []
            tdays = sorted(d for d, v in self.days[c["cid"]].items() if v["till"])
            if not c["batch"]:
                for d in tdays:
                    z += 1
                    if c["late"] and d.weekday() in (3, 4, 5) or (c["late"] and rr.random() < 0.3):
                        at = dt.datetime.combine(d + dt.timedelta(days=1), dt.time(0, rr.randint(5, 59),
                                                                                   rr.randint(0, 59)))
                        if rr.random() < 0.4:
                            at = at.replace(hour=1)
                    else:
                        at = dt.datetime.combine(d, dt.time(rr.randint(17, 22), rr.randint(0, 59), rr.randint(0, 59)))
                    zs.append(dict(day=d, z=z, at=at))
            else:
                # held on the till, sent when it next connects: every four to nine days, in the morning
                i = 0
                nxt = tdays[0] + dt.timedelta(days=rr.randint(1, 6))
                pending = []
                for d in tdays:
                    while d >= nxt:
                        if pending:
                            at = dt.datetime.combine(nxt, dt.time(rr.randint(8, 11), rr.randint(0, 59),
                                                                  rr.randint(0, 59)))
                            for p in pending:
                                p["at"] = at
                            zs.extend(pending)
                            pending = []
                        nxt = nxt + dt.timedelta(days=rr.randint(4, 9))
                    z += 1
                    pending.append(dict(day=d, z=z, at=None))
                while pending:
                    at = dt.datetime.combine(nxt, dt.time(rr.randint(8, 11), rr.randint(0, 59), rr.randint(0, 59)))
                    for p in pending:
                        p["at"] = at
                    zs.extend(pending)
                    pending = []
            self.z[c["cid"]] = zs


TT = None


def till_truth():
    global TT
    if TT is None:
        TT = TillTruth()
    return TT


def seg_till_z():
    """The reviewed till customers' Z-reports: the numbers pack.till_rows writes, and the evening each was sent."""
    T = S.truth()
    r = random.Random(W.SEED + 23)
    rr = random.Random(W.SEED + 149)
    out = {}
    for c in sorted(W.CUSTOMERS, key=lambda x: x["cid"]):
        if not c["till"]:
            continue
        t = T.cust[c["cid"]]
        z = r.randint(1200, 4800)
        zs = []
        for d in W.days(W.HISTORY_START, W.EXPORT_END):
            if t["card"][d] <= 0:
                continue
            z += 1
            other = round(r.uniform(0, 25), 2) if r.random() < 0.2 else 0.0
            at = dt.datetime.combine(d, dt.time(rr.randint(17, 22), rr.randint(0, 59), rr.randint(0, 59)))
            zs.append(dict(day=d, z=z, other=other, at=at))
        out[c["cid"]] = zs
    return out


TILL_LOG_HEADER = ["till_account", "customer_id", "received_at", "z_no", "cash_sales", "card_sales",
                   "other_tenders", "paid_outs", "gross_sales"]


def till_log_rows():
    """The till service's central log of Z-reports received from 1 October 2025 to the extract, every customer."""
    T = S.truth()
    TT_ = till_truth()
    rows = []
    lo = dt.datetime.combine(W.REVIEW_START, dt.time(0, 0))
    hi = dt.datetime.combine(LOG_END, dt.time(23, 59, 59))
    for cid, zs in seg_till_z().items():
        c = W.BY_CID[cid]
        t = T.cust[cid]
        tacct = "TS-%d" % (700000 + int(cid.split("-")[1]))
        for zz in zs:
            if not (lo <= zz["at"] <= hi):
                continue
            d = zz["day"]
            cash_sales = round(t["cash"][d] + t["paid_out"][d], 2)
            card_sales = round(t["card"][d] - t["refunds"].get(d, 0.0), 2)
            rows.append([tacct, cid, zz["at"].strftime("%Y-%m-%d %H:%M:%S"), zz["z"], "%.2f" % cash_sales,
                         "%.2f" % card_sales, "%.2f" % zz["other"], "%.2f" % t["paid_out"][d],
                         "%.2f" % (cash_sales + card_sales + zz["other"])])
    for c in TILL_OTHERS:
        days = TT_.days[c["cid"]]
        for zz in TT_.z[c["cid"]]:
            if not (lo <= zz["at"] <= hi):
                continue
            v = days[zz["day"]]
            cash_sales = round(v["cash"] + v["paid"], 2)
            card_sales = round(v["card"] - v["refund"], 2)
            rows.append([c["tacct"], c["cid"], zz["at"].strftime("%Y-%m-%d %H:%M:%S"), zz["z"], "%.2f" % cash_sales,
                         "%.2f" % card_sales, "%.2f" % v["other"], "%.2f" % v["paid"],
                         "%.2f" % (cash_sales + card_sales + v["other"])])
    rows.sort(key=lambda x: (x[2], x[0], x[3]))
    return rows


def ms_extra_rows():
    """The non-review till customers' terminals in the merchant services daily file."""
    TT_ = till_truth()
    rows = []
    rr = random.Random(W.SEED + 151)
    for c in TILL_OTHERS:
        for d, v in sorted(TT_.days[c["cid"]].items()):
            if d < W.HISTORY_START or d > W.EXPORT_END:
                continue
            gc, rc = int(round(v["card"] * 100)), int(round(v["refund"] * 100))
            msc = int(round((gc - rc) * c["msc"]))
            n = max(1, int(round(v["card"] / rr.uniform(9.0, 30.0))))
            rows.append([d.isoformat(), c["mid"], n, gc, rc, msc, gc - rc - msc, W.next_working(d).isoformat()])
    return rows


def mreg_extra_rows():
    r = random.Random(W.SEED + 157)
    rows = []
    for c in TILL_OTHERS:
        opened = dt.date(r.randint(2014, 2023), r.randint(1, 12), r.randint(1, 28))
        rows.append([c["mid"], c["cid"], c["name"].split(",")[0], c["mcc"], "Till service",
                     "%s %08d" % (W.BRANCH[c["home"]][3], r.randint(30000000, 89999999)), opened.strftime("%d/%m/%Y"),
                     "Active"])
    return rows
