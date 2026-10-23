"""task482 asks: each store's vaccine stock from the 2025 to the 2026 year-end physical inventory (Meridale's
deliveries, the administrations, write-offs, Meridale's return credits, transfers between stores) and each store's
refrigerator service history with Brannon. Nothing here reads or moves a temperature record.

Stock is held in doses. Multi-dose vials (10 doses) are opened as needed and kept 28 days after first puncture. The
2025-26 influenza vaccine expires on 30 June 2026: what is left is written off on 1 July and the unopened units go
back to Meridale for credit. The 2025-26 COVID-19 vaccine is written off when the 2026-27 formula arrives. A store's
doses unaccounted for are the doses that left its stock with no record: doses given but never entered, breakage
nobody logged, and, before the 1 June 2026 inventory update, what was left in a multi-dose vial at its beyond-use
date (the update added the write-off for it).
"""
import datetime as dt
import math
from collections import defaultdict

import numpy as np

import world as W

DAY0 = dt.date(2025, 12, 30)                    # the stock extracts run from 30 December 2025
DAYS = (dt.date(2026, 12, 31) - DAY0).days + 1
UPDATE = dt.date(2026, 6, 1)                     # the inventory update: multi-dose vials written off in doses from here
FLU25_EXPIRY = dt.date(2026, 6, 30)
FORMULA_DAY = dt.date(2026, 9, 10)               # the 2025-26 COVID-19 vaccine written off
PLATFORM = dt.date(2026, 7, 1)                   # Brannon invoices from its new platform: amounts include sales tax
TAX = 0.06
BUD = 28                                         # days a punctured multi-dose vial is kept
COUNT_30DEC_2025 = [101, 104, 108, 201, 205, 303, 305, 310]    # 2025 year-end inventory taken on 30 December
VIAL_BROKEN = sorted((set(W.BY_NO) - set(COUNT_30DEC_2025) - set(W.COUNT_30DEC)) | {101, 201, 305, 102, 203, 306})
ACCOUNTS_MOVED = dt.date(2026, 4, 1)             # the Lindqvist stores' Meridale accounts moved to Penwick's
RETURNABLE = ("F25S", "F25V")                     # Halvorsen takes back unopened 2025-26 influenza vaccine; Corbel does not

LABELERS = {"70841": "Halvorsen Vaccines", "6623": "Corbel Biologics", "81420": "Brightwater Biopharma",
            "58960": "Aldane Pharmaceuticals"}
# key, NDC as the pharmacy system holds it, description, package, doses per package, units per package, Meridale
# unit, package cost, multi-dose vial, season
ITEMS = [
    ("F25S", "70841-215-10", "Influenza vaccine 2025-2026 formula, trivalent, 0.5 mL prefilled syringe",
     "10 x 0.5 mL syringes", 10, 10, "CT", 186.50, False, "2025-2026"),
    ("F25V", "70841-217-01", "Influenza vaccine 2025-2026 formula, trivalent, 5 mL multi-dose vial",
     "1 x 5 mL vial (10 doses)", 10, 1, "VL", 158.40, True, "2025-2026"),
    ("F25H", "6623-0418-02", "Influenza vaccine high-dose 2025-2026 formula, 0.5 mL prefilled syringe",
     "10 x 0.5 mL syringes", 10, 10, "CT", 702.00, False, "2025-2026"),
    ("F26S", "70841-221-10", "Influenza vaccine 2026-2027 formula, trivalent, 0.5 mL prefilled syringe",
     "10 x 0.5 mL syringes", 10, 10, "CT", 191.20, False, "2026-2027"),
    ("F26V", "70841-223-01", "Influenza vaccine 2026-2027 formula, trivalent, 5 mL multi-dose vial",
     "1 x 5 mL vial (10 doses)", 10, 1, "VL", 162.30, True, "2026-2027"),
    ("F26H", "6623-0436-02", "Influenza vaccine high-dose 2026-2027 formula, 0.5 mL prefilled syringe",
     "10 x 0.5 mL syringes", 10, 10, "CT", 718.50, False, "2026-2027"),
    ("C25", "81420-0336-1", "COVID-19 vaccine 2025-2026 formula, 0.5 mL prefilled syringe",
     "10 x 0.5 mL syringes", 10, 10, "CT", 1365.00, False, "2025-2026"),
    ("C26", "81420-0352-1", "COVID-19 vaccine 2026-2027 formula, 0.5 mL prefilled syringe",
     "10 x 0.5 mL syringes", 10, 10, "CT", 1398.00, False, "2026-2027"),
    ("RSV", "58960-104-01", "RSV vaccine, adjuvanted, single-dose antigen vial with diluent vial",
     "1 kit (1 dose)", 1, 1, "KT", 295.00, False, ""),
    ("PCV", "58960-141-10", "Pneumococcal 21-valent conjugate vaccine, 0.5 mL prefilled syringe",
     "10 x 0.5 mL syringes", 10, 10, "CT", 2620.00, False, ""),
    ("RZV", "6623-0512-11", "Zoster vaccine recombinant, adjuvanted, single-dose kit",
     "10 single-dose kits", 10, 10, "CT", 1960.00, False, ""),
    ("TDP", "70841-305-10", "Tdap vaccine, 0.5 mL prefilled syringe",
     "10 x 0.5 mL syringes", 10, 10, "CT", 548.00, False, ""),
    ("HPB", "81420-0411-5", "Hepatitis B vaccine (recombinant), adult, 1 mL prefilled syringe",
     "10 x 1 mL syringes", 10, 10, "CT", 690.00, False, ""),
]
ITEM = {k[0]: dict(key=k[0], ndc=k[1], desc=k[2], package=k[3], dpp=k[4], upp=k[5], uom=k[6], cost=k[7], mdv=k[8],
                   season=k[9]) for k in ITEMS}
SHORT = {"F25S": "FLU 25-26 PFS", "F25V": "FLU 25-26 MDV", "F25H": "FLU HD 25-26", "F26S": "FLU 26-27 PFS",
         "F26V": "FLU 26-27 MDV", "F26H": "FLU HD 26-27", "C25": "COVID 25-26", "C26": "COVID 26-27", "RSV": "RSV",
         "PCV": "PCV21", "RZV": "ZOSTER RZV", "TDP": "TDAP", "HPB": "HEP B ADULT"}

# share of a store's doses, and each month's share of the product's year (the 2025-26 products carry January to
# their end, the 2026-27 products from their first delivery)
SHARE = {"FLU": 0.56, "C": 0.14, "RSV": 0.06, "PCV": 0.06, "RZV": 0.09, "TDP": 0.06, "HPB": 0.03}
FLU_SPLIT = {"S": 0.54, "H": 0.31, "V": 0.15}
MONTHS = {
    "FLU": [0.07, 0.035, 0.015, 0.005, 0, 0, 0, 0.03, 0.30, 0.34, 0.15, 0.055],
    "C": [0.09, 0.05, 0.03, 0.02, 0.02, 0.02, 0.02, 0.03, 0.22, 0.28, 0.15, 0.07],
    "RSV": [0.06, 0.04, 0.03, 0.02, 0.02, 0.02, 0.03, 0.07, 0.22, 0.24, 0.15, 0.10],
    "PCV": [0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.08, 0.11, 0.12, 0.10, 0.10],
    "RZV": [1 / 12.0] * 12,
    "TDP": [0.07, 0.07, 0.07, 0.07, 0.08, 0.09, 0.11, 0.16, 0.08, 0.07, 0.07, 0.06],
    "HPB": [1 / 12.0] * 12,
}
DEC2025 = {"FLU": 0.09, "C": 0.10, "RSV": 0.10, "PCV": 0.10, "RZV": 1 / 12.0, "TDP": 0.06, "HPB": 1 / 12.0}
DOW_F = [1.0, 1.0, 1.0, 1.0, 1.0, 0.8, 0.5]
OPEN_H = {0: (8, 21), 1: (8, 21), 2: (8, 21), 3: (8, 21), 4: (8, 21), 5: (9, 18), 6: (10, 18)}

SHIP_TO = {no: 4400000 + (no * 3517) % 99991 for no in W.BY_NO}
OLD_SHIP_TO = {no: 3100000 + (no * 2203) % 89989 for no in W.BY_NO if no // 100 == 3}
BRANNON_SITE = {no: "S-%05d" % (20000 + (no * 389) % 7919) for no in W.BY_NO}
LEGACY_NO = {201: 2, 202: 3, 203: 5, 204: 6, 205: 7, 206: 9, 207: 11, 208: 12, 209: 14, 210: 15,
             301: 1, 302: 4, 303: 5, 304: 6, 305: 8, 306: 9, 307: 10, 308: 12, 309: 13, 310: 15}


def fam(key):
    return "FLU" if key[0] == "F" else "C" if key[0] == "C" else key


def ndc11(ndc10):
    a, b, c = ndc10.split("-")
    return a.zfill(5) + b.zfill(4) + c.zfill(2)


def day_of(d):
    return (d - DAY0).days


def local_dt(m):
    return W.local_of(m)[0]


def lot_code(key, k):
    lab = ITEM[key]["ndc"].split("-")[0]
    base = {"70841": "HV", "6623": "CB", "81420": "BW", "58960": "AL"}[lab]
    n = (sum(ord(ch) for ch in key) * 131 + k * 977) % 9000 + 1000
    return "%s%s%04d" % (base, "ABCDEFGHJKLMNPRSTUVWXYZ"[(k * 7 + len(key)) % 23], n)


def lot_expiry(key, k):
    if key.startswith("F25"):
        return FLU25_EXPIRY
    if key.startswith("F26"):
        return dt.date(2027, 6, 30)
    if key == "C25":
        return dt.date(2026, 10, 31) + dt.timedelta(days=20 * (k % 3))
    if key == "C26":
        return dt.date(2027, 6, 30) + dt.timedelta(days=30 * (k % 3))
    return dt.date(2027, 9, 30) + dt.timedelta(days=61 * (k % 5))


def active(key, d, started):
    """whether a product is given on a date: the 2025-26 products to their season's end, the 2026-27 products from
    their first delivery"""
    if key.startswith("F25"):
        return d <= dt.date(2026, 4, 30)
    if key == "C25":
        return d < FORMULA_DAY
    if key.startswith("F26") or key == "C26":
        return started.get(key) is not None and d >= started[key]
    return True


def rate(st, key, d):
    """mean doses of a product a store gives on a date"""
    f = fam(key)
    m = MONTHS[f][d.month - 1] if d.year == 2026 else DEC2025[f]
    days_in = 31 if d.month in (1, 3, 5, 7, 8, 10, 12) else 30 if d.month != 2 else 28
    r = st["volume"] * SHARE[f] * m / days_in * DOW_F[d.weekday()] / 0.93
    if f == "FLU":
        r *= FLU_SPLIT[key[-1]]
    return r


class Stock:
    """one product's stock at one store: lots first in, first out; a multi-dose vial open with its doses left"""

    def __init__(self, key):
        self.key = key
        self.q = []                  # [lot index, doses] (unopened vials in whole tens)
        self.open = None             # [lot index, doses left, day opened]

    def total(self):
        return sum(x[1] for x in self.q) + (self.open[1] if self.open else 0)

    def add(self, k, doses):
        if self.q and self.q[-1][0] == k:
            self.q[-1][1] += doses
        else:
            self.q.append([k, doses])

    def take(self, n):
        """remove n doses from the oldest lots; return [(lot, doses)]"""
        out = []
        while n > 0 and self.q:
            k, have = self.q[0]
            t = min(have, n)
            out.append((k, t))
            self.q[0][1] -= t
            n -= t
            if self.q[0][1] == 0:
                self.q.pop(0)
        return out


def store_volume():
    r = np.random.default_rng(W.SEED * 1000 + 901)
    return {s["no"]: int(round(s["door"] * 75 * r.uniform(0.85, 1.15))) for s in W.STORES}


def deliveries_local():
    """each store's Meridale deliveries: (local datetime of delivery, local date invoiced); 30 December 2025 and the
    world's 2026 deliveries"""
    out = {}
    for s in W.STORES:
        r = np.random.default_rng(W.SEED * 1000 + s["no"] * 7 + 41)
        lst = [(dt.datetime(2025, 12, 30, 10, int(r.integers(0, 50))), dt.date(2025, 12, 29))]
        for (a, k, _) in W.deliveries(s):
            t = local_dt(a) - dt.timedelta(minutes=int(r.integers(4, 16)))
            inv = t.date() - dt.timedelta(days=1)
            while inv.weekday() >= 5 or inv in (dt.date(2026, 1, 1), dt.date(2026, 11, 26), dt.date(2026, 12, 25)):
                inv -= dt.timedelta(days=1)
            lst.append((t, inv))
        out[s["no"]] = lst
    return out


def open_minutes(e):
    """local datetimes of the routine door openings, by local date"""
    by = defaultdict(list)
    for m in e["opens"]:
        t = local_dt(m)
        by[t.date()].append(t)
    return by


def plan_transfers():
    """stock moved between stores of one former chain in the 2026-27 season: (date, from, to, product, doses)"""
    r = np.random.default_rng(W.SEED * 1000 + 977)
    out = []
    groups = {c: [s["no"] for s in W.STORES if s["make"] == c] for c in "FKP"}
    for c in "FKP":
        for _ in range(int(r.integers(7, 11))):
            a, b = r.choice(groups[c], 2, replace=False)
            d = dt.date(2026, 9, 8) + dt.timedelta(days=int(r.integers(0, 78)))
            while d.weekday() >= 5 or d == dt.date(2026, 11, 26):
                d += dt.timedelta(days=1)
            key = str(r.choice(["F26S", "F26S", "F26H", "C26"]))
            out.append((d, int(a), int(b), key, int(r.choice([10, 10, 20])), int(r.integers(12, 15)),
                        int(r.integers(0, 59))))
    return sorted(out)


def simulate_stock(E):
    """every store's stock flows: the files' rows and the truth they come from"""
    vol = store_volume()
    deliv = deliveries_local()
    transfers = plan_transfers()
    flows = {no: dict(receipts=[], admin=[], writeoffs=[], credits=[], t_in=[], t_out=[], lost=[], counts={})
             for no in W.BY_NO}
    stock = {}
    started = {no: {} for no in W.BY_NO}
    rng = {no: np.random.default_rng(W.SEED * 1000 + no * 7 + 43) for no in W.BY_NO}
    lots = defaultdict(int)
    target_lost = {}
    for s in W.STORES:
        no = s["no"]
        st = dict(volume=vol[no])
        s["_st"] = st
        r = rng[no]
        stock[no] = {k: Stock(k) for k in ITEM}
        # opening stock on 30 December 2025: the season's influenza bought ahead, two weeks of the rest
        for key in ITEM:
            if key in ("F26S", "F26V", "F26H", "C26"):
                continue
            if key.startswith("F25"):
                need = sum(rate(st, key, DAY0 + dt.timedelta(days=i)) for i in range(122))
                extra = {"F25S": r.integers(10, 25) + 1.5 * math.sqrt(need), "F25H": r.integers(3, 13),
                         "F25V": 10 * r.integers(1, 3)}[key]
                n = int(need * r.uniform(1.02, 1.1)) + int(extra)
            else:
                n = int(sum(rate(st, key, DAY0 + dt.timedelta(days=i)) for i in range(14)) * 1.4) + 4
            if ITEM[key]["mdv"]:
                n = 10 * int(math.ceil(n / 10.0))
            stock[no][key].add(-1, n)
        target_lost[no] = int(vol[no] * r.uniform(0.026, 0.045))
    # the dates broken unopened vials were written off at the stores where one was (January to May)
    vial_breaks = {}
    for no in VIAL_BROKEN:
        r = rng[no]
        k = int(r.choice([1, 1, 2])) if vol[no] >= 1500 else 1
        vial_breaks[no] = sorted(DAY0 + dt.timedelta(days=int(d)) for d in r.choice(np.arange(4, 45), k, replace=False))
    late_breaks = {no: DAY0 + dt.timedelta(days=int(rng[no].integers(270, 335))) for no in (104, 202, 209, 305, 308)}
    opens = {no: open_minutes(E[no]) for no in W.BY_NO}
    for di in range(DAYS):
        d = DAY0 + dt.timedelta(days=di)
        events = []
        for s in W.STORES:
            no = s["no"]
            st = s["_st"]
            r = rng[no]
            closed = d in (dt.date(2026, 1, 1), dt.date(2026, 11, 26), dt.date(2026, 12, 25))
            for (t, inv) in deliv[no]:
                if t.date() == d:
                    events.append((t, 0, no, "deliver", inv))
            if not closed:
                lo, hi = OPEN_H[d.weekday()]
                pool = opens[no].get(d, [])
                draws = [(key, int(r.poisson(rate(st, key, d)))) for key in ITEM if active(key, d, started[no])]
                if d == dt.date(2026, 12, 31) and no in W.COUNT_30DEC and sum(n for _, n in draws) < 3:
                    draws.append(("F26S", 3 - sum(n for _, n in draws)))
                for key, n in draws:
                    for _ in range(n):
                        if pool:
                            t = pool[int(r.integers(0, len(pool)))]
                        else:
                            t = dt.datetime(d.year, d.month, d.day, lo) + dt.timedelta(
                                minutes=int(r.integers(0, (hi - lo) * 60)))
                        events.append((t, 2, no, "give", key))
                if r.random() < target_lost[no] / 340.0:
                    t = dt.datetime(d.year, d.month, d.day, lo) + dt.timedelta(minutes=int(r.integers(30, (hi - lo) * 60)))
                    events.append((t, 3, no, "lose", None))
                if r.random() < 1 / 55.0:
                    t = dt.datetime(d.year, d.month, d.day, lo) + dt.timedelta(minutes=int(r.integers(30, (hi - lo) * 60)))
                    events.append((t, 3, no, "spoil", None))
                if no in vial_breaks and d in vial_breaks[no]:
                    events.append((dt.datetime(d.year, d.month, d.day, lo + 1, int(r.integers(5, 55))), 1, no,
                                   "break_vial", "F25V"))
                if no in late_breaks and d == late_breaks[no]:
                    events.append((dt.datetime(d.year, d.month, d.day, lo + 2, int(r.integers(5, 55))), 1, no,
                                   "break_vial", "F26V"))
                if d == dt.date(2026, 7, 1):
                    events.append((dt.datetime(2026, 7, 1, 9, int(r.integers(10, 50))), 1, no, "expire_flu25", None))
                if d == FORMULA_DAY:
                    events.append((dt.datetime(2026, 9, 10, 9, int(r.integers(10, 50))), 1, no, "formula", None))
            events.append((dt.datetime(d.year, d.month, d.day, OPEN_H[d.weekday()][1] - 1, 59), 4, no, "bud", None))
            if d == dt.date(2025, 12, 30) and no in COUNT_30DEC_2025 or d == dt.date(2025, 12, 31) and \
                    no not in COUNT_30DEC_2025:
                events.append((dt.datetime(d.year, d.month, d.day, 21, int(r.integers(22, 55))), 5, no, "count", 2025))
            if d.year == 2026 and d.month == 12 and d.day in (30, 31):
                t = local_dt(W.year_end_count(W.BY_NO[no]))
                if t.date() == d:
                    events.append((t, 5, no, "count", 2026))
        for (td, a, b, key, q, hh, mm) in transfers:
            if td == d:
                t0 = dt.datetime(d.year, d.month, d.day, hh, mm)
                events.append((t0, 1, a, "send", (b, key, q, t0 + dt.timedelta(minutes=95 + 7 * (a % 9)))))
        events.sort(key=lambda x: (x[0], x[1], x[2]))
        pending = []
        for ev in events:
            t, _, no, kind, arg = ev
            S = stock[no]
            f = flows[no]
            r = rng[no]
            st = W.BY_NO[no]["_st"]
            while pending and pending[0][0] <= t:
                tt, nb, key, k, q, tno = pending.pop(0)
                stock[nb][key].add(k, q)
                flows[nb]["t_in"].append((tt, key, lots_name(key, k), q, tno))
            if kind == "deliver":
                inv = arg
                nxt = [x[0] for x in deliv[no] if x[0] > t]
                gap = ((nxt[0] - t).days if nxt else 7) + 1
                lines = []
                for key in ITEM:
                    if key.startswith("F25"):
                        continue
                    if key == "C25" and d >= dt.date(2026, 9, 1):
                        continue
                    first = False
                    if key in ("F26S", "F26V", "F26H") and started[no].get(key) is None:
                        if d < dt.date(2026, 8, 18):
                            continue
                        first = True
                    if key == "C26" and started[no].get(key) is None:
                        if d < dt.date(2026, 9, 8):
                            continue
                        first = True
                    horizon = [d + dt.timedelta(days=i) for i in range(1, 15)]
                    if first:
                        sim = dict(started[no])
                        sim[key] = d
                        need = sum(rate(st, key, x) for x in horizon if active(key, x, sim)) * 1.25
                    else:
                        if not active(key, d + dt.timedelta(days=1), started[no]):
                            continue
                        need = sum(rate(st, key, x) for x in horizon[:gap + 4]) * 1.25 + 2
                    have = S[key].total()
                    if have >= need:
                        continue
                    pk = int(math.ceil((need - have) / ITEM[key]["dpp"]))
                    k = lots[key] // 6
                    lots[key] += 1
                    S[key].add(k, pk * ITEM[key]["dpp"])
                    if first:
                        started[no][key] = d
                    lines.append((key, pk, k))
                if lines:
                    f["receipts"].append((t, inv, lines))
            elif kind == "give":
                key = arg
                if ITEM[key]["mdv"]:
                    took = give_mdv(S[key], d, f, t)
                else:
                    took = S[key].take(1)
                if took:
                    f["admin"].append((t, key, lots_name(key, took[0][0])))
            elif kind == "lose":
                cand = [k for k in ITEM if S[k].total() > 0 and active(k, d, started[no])]
                if cand:
                    key = cand[int(r.integers(0, len(cand)))]
                    if ITEM[key]["mdv"]:
                        took = give_mdv(S[key], d, f, t)
                    else:
                        took = S[key].take(1)
                    if took:
                        f["lost"].append((t, key, 1, "unrecorded"))
            elif kind == "spoil":
                cand = [k for k in ITEM if S[k].total() > 0 and not ITEM[k]["mdv"] and active(k, d, started[no])]
                if cand:
                    key = cand[int(r.integers(0, len(cand)))]
                    took = S[key].take(1)
                    reason = "BROKEN" if r.random() < 0.55 else "WASTED - NOT ADMINISTERED"
                    for (k, q) in took:
                        f["writeoffs"].append((t, key, lots_name(key, k), q, q, reason))
            elif kind == "break_vial":
                key = arg
                if S[key].q and S[key].q[0][1] >= 10:
                    k = S[key].q[0][0]
                    S[key].take(10)
                    logged = 1 if d < UPDATE else 10
                    f["writeoffs"].append((t, key, lots_name(key, k), 10, logged, "BROKEN"))
            elif kind == "expire_flu25":
                for key in ("F25S", "F25H", "F25V"):
                    if S[key].open:
                        k, left, _ = S[key].open
                        f["writeoffs"].append((t, key, lots_name(key, k), left, left, "EXPIRED"))
                        S[key].open = None
                    for (k, q) in S[key].take(S[key].total()):
                        f["writeoffs"].append((t, key, lots_name(key, k), q, q, "EXPIRED"))
                        if key in RETURNABLE:
                            units = q // 10 if ITEM[key]["mdv"] else q
                            f["credits"].append((key, lots_name(key, k), units, q))
            elif kind == "formula":
                for (k, q) in S["C25"].take(S["C25"].total()):
                    f["writeoffs"].append((t, "C25", lots_name("C25", k), q, q, "FORMULA CHANGE"))
            elif kind == "bud":
                for key in ("F25V", "F26V"):
                    o = S[key].open
                    if o and (d - o[2]).days >= BUD - 1 and o[1] > 0:
                        if d < UPDATE:
                            f["lost"].append((t, key, o[1], "vial at beyond-use date"))
                        else:
                            f["writeoffs"].append((t, key, lots_name(key, o[0]), o[1], o[1], "WASTED - BEYOND USE"))
                        S[key].open = None
            elif kind == "count":
                f["counts"][arg] = (t, {k: S[k].total() for k in ITEM})
            elif kind == "send":
                nb, key, q, tr = arg
                if S[key].total() >= q + 20:
                    tno = "TR%05d" % (26000 + len(flows[no]["t_out"]) * 31 + no)
                    for (k, qq) in S[key].take(q):
                        f["t_out"].append((t, key, lots_name(key, k), qq, nb, tno, tr))
                        pending.append((tr, nb, key, k, qq, tno))
                    pending.sort()
        while pending and pending[0][0].date() == d:
            tt, nb, key, k, q, tno = pending.pop(0)
            stock[nb][key].add(k, q)
            flows[nb]["t_in"].append((tt, key, lots_name(key, k), q, tno))
    for s in W.STORES:
        s.pop("_st", None)
    return flows


LOT_EXP = {}


def lots_name(key, k):
    name = lot_code(key, k + 3)
    LOT_EXP[name] = lot_expiry(key, k + 3)
    return name


def give_mdv(S, d, f, t):
    """one dose from the open vial, opening the next when it is empty or past its beyond-use date"""
    if S.open and (S.open[1] <= 0 or (d - S.open[2]).days >= BUD):
        S.open = None
    if S.open is None:
        if not S.q or S.q[0][1] < 10:
            return []
        k = S.q[0][0]
        S.take(10)
        S.open = [k, 10, d]
    S.open[1] -= 1
    k = S.open[0]
    if S.open[1] == 0:
        S.open = None
    return [(k, 1)]


def window(no, flows):
    """the two count times bounding a store's year"""
    return flows[no]["counts"][2025][0], flows[no]["counts"][2026][0]


def unaccounted_truth(flows):
    out = {}
    for no, f in flows.items():
        a, b = window(no, flows)
        out[no] = sum(q for (t, key, q, why) in f["lost"] if a < t <= b)
    return out


# --- Brannon -------------------------------------------------------------------------------------------------------
MODELS = {"pharma": [("Northcold", "PG-23", 145.00), ("Northcold", "PG-12", 128.00), ("Stellane", "V-26", 152.00)],
          "household": [("Keswell", "HR-18", 120.00), ("Keswell", "HR-21", 124.00)]}


def model_of(no):
    s = W.BY_NO[no]
    lst = MODELS[s["unit"]]
    return lst[(no * 7 + no // 100) % len(lst)]


PM_ADDONS = [("replaced door gasket corner section", 18.40), ("replaced interior light bulb", 9.60),
             ("replaced condenser intake filter", 24.90), ("tightened and lubricated door closer", 0.0),
             ("replaced shelf clip set", 12.75), ("replaced door closer spring", 31.60)]
LABOR, LABOR_AFTER, TRIP = 118.00, 177.00, 65.00
TECHS = ["T104", "T117", "T122", "T138", "T141", "T156", "T163"]
# store: [(first visit, work, parts, second visit, work, parts)]; a first visit named for a world event is the call
# that event brought ("drift" a failing thermostat, "ajar" a door that did not close), "end" the visit that ended it
REPAIRS = {
    102: [(dt.date(2025, 12, 22), "Door out of alignment; adjusted leveling legs and door hinge", 0.0)],
    104: [(dt.date(2026, 3, 17), "Condenser fan motor noisy; diagnosed, motor ordered", 0.0,
           dt.date(2026, 3, 24), "Replaced condenser fan motor", 186.40)],
    106: [("drift0", "Cabinet running warm; controller failing, setpoint lowered and part ordered", 0.0,
           "end", "Replaced temperature controller and verified setpoint", 342.75)],
    109: [(dt.date(2026, 2, 11), "Interior light switch replaced", 38.60)],
    110: [("ajar0", "Door not closing on its own; replaced door closer", 64.20),
          ("ajar1", "Door gasket torn at the hinge side; gasket ordered", 0.0,
           "+6", "Replaced door gasket", 128.90)],
    201: [("drift0", "Cabinet running warm; replaced temperature controller", 318.40),
          ("drift1", "Cabinet running warm; controller reading high, part ordered", 0.0,
           "end", "Replaced temperature probe and controller board", 395.10)],
    202: [(dt.date(2026, 3, 10), "Door gasket replaced", 116.20)],
    203: [(dt.date(2026, 5, 6), "Door gasket replaced", 112.30)],
    205: [(dt.date(2025, 12, 29), "Compressor short cycling; start relay ordered", 0.0,
           dt.date(2026, 1, 6), "Replaced compressor start relay and overload", 96.80)],
    207: [(dt.date(2026, 10, 20), "Display board intermittent", 0.0,
           dt.date(2026, 10, 27), "Replaced display board", 214.60)],
    208: [(dt.date(2026, 6, 9), "Compressor start relay replaced", 88.50)],
    209: [(dt.date(2026, 8, 11), "Alarm board fault; board ordered", 0.0,
           dt.date(2026, 8, 18), "Replaced alarm and display board", 263.20)],
    210: [("ajar0", "Door gasket split; replaced door gasket", 121.40)],
    302: [(dt.date(2026, 6, 23), "Evaporator fan motor replaced", 154.80)],
    304: [(dt.date(2026, 12, 21), "Door hinge cam worn; replaced hinge cam", 47.90)],
    305: [("ajar0", "Door dropping on hinge; replaced hinge and adjusted door", 72.60)],
    307: [(dt.date(2026, 12, 28), "Unit short cycling; defrost thermostat ordered", 0.0,
           dt.date(2027, 1, 5), "Replaced defrost thermostat", 89.70)],
    308: [(dt.date(2026, 4, 14), "Door gasket replaced", 109.80)],
    310: [(dt.date(2026, 5, 19), "Evaporator fan blade cracked; replaced fan blade", 41.30)],
}
LATE_JUNE_PM = (202, 208, 310)


def _wd(d):
    while d.weekday() >= 5:
        d += dt.timedelta(days=1)
    return d


def _after(d, t):
    return d.weekday() >= 5 or int(t[:2]) < 8 or int(t[:2]) >= 18


def brannon_history():
    """one row per visit as Brannon's portal lists it, and each work order's truth. Every work order carries the store
    of each visit: before the 1 July 2026 platform move Brannon put a morning's preventive maintenance route (two stores
    of one former chain) on one work order and one invoice."""
    r = np.random.default_rng(W.SEED * 1000 + 1201)
    wos = []
    pms = []
    for i, s in enumerate(W.STORES):
        no = s["no"]
        m1 = 1 + i % 6
        for m in (m1, m1 + 6):
            if m == 6 and no in LATE_JUNE_PM:
                vd = _wd(dt.date(2026, 6, int(r.integers(22, 27))))
            else:
                vd = _wd(dt.date(2026, m, int(r.integers(3, 25))))
            pms.append(dict(no=no, m=m, date=vd, unit=s["unit"], make=s["make"]))
    routes = defaultdict(list)
    for p in pms:
        if p["m"] <= 6 and not (p["no"] in LATE_JUNE_PM and p["m"] == 6):
            routes[(p["m"], p["make"])].append(p)
        else:
            routes[("own", p["no"], p["m"])].append(p)
    for key in sorted(routes, key=str):
        grp = sorted(routes[key], key=lambda p: p["no"])
        while grp:
            take, grp = (grp[:2], grp[2:]) if key[0] != "own" else (grp[:1], grp[1:])
            day = take[0]["date"]
            visits, works, prices, stores = [], [], [], []
            parts, extra = 0.0, 0.0
            for j, p in enumerate(take):
                work = ("Preventive maintenance: cleaned condenser coil, checked door gasket, hinges and closer, "
                        "checked thermostat against reference thermometer")
                h = 0.75
                if len(take) == 1 and r.random() < 0.55:
                    what, parts = PM_ADDONS[int(r.integers(0, len(PM_ADDONS)))]
                    extra = float(r.choice([0.25, 0.5]))
                    h += extra
                    work += "; " + what
                t0 = "06:%02d" % int(r.integers(15, 35)) if j == 0 else "07:%02d" % int(r.integers(12, 25))
                visits.append((day, t0, h))
                works.append(work)
                prices.append(model_of(p["no"])[2])
                stores.append(p["no"])
            wos.append(dict(stores=stores, visits=visits, work=works, call="PM", parts=parts, pm=prices,
                            extra=extra))
    for s in W.STORES:
        no = s["no"]
        ev = {kind: [x for x in W.events(s) if x[0] == kind] for kind in ("thermostat", "ajar")}
        for rep in REPAIRS.get(no, []):
            first, work1, parts = rep[0], rep[1], rep[2]
            two = len(rep) > 3
            end = None
            if isinstance(first, str):
                kind = "thermostat" if first.startswith("drift") else "ajar"
                a, k = ev[kind][int(first[-1])][1], ev[kind][int(first[-1])][2]
                if kind == "thermostat":
                    end = local_dt(a + k)
                    v1 = local_dt(a + int(k * 0.45)) if two else end
                    d1, t1 = v1.date(), "%02d:%02d" % (v1.hour, v1.minute)
                else:
                    d1 = _wd(local_dt(a + k).date() + dt.timedelta(days=1))
                    t1 = "%02d:%02d" % (int(r.integers(9, 15)), int(r.integers(0, 59)))
            else:
                d1, t1 = first, "%02d:%02d" % (int(r.integers(9, 15)), int(r.integers(0, 59)))
            visits = [(d1, t1, float(r.choice([1.0, 1.25, 1.5])))]
            works = [work1]
            if two:
                second, work2, parts2 = rep[3], rep[4], rep[5]
                if second == "end":
                    d2, t2 = end.date(), "%02d:%02d" % (end.hour, end.minute)
                elif isinstance(second, str):
                    d2 = _wd(d1 + dt.timedelta(days=int(second)))
                    t2 = "%02d:%02d" % (int(r.integers(9, 15)), int(r.integers(0, 59)))
                else:
                    d2, t2 = second, "%02d:%02d" % (int(r.integers(9, 15)), int(r.integers(0, 59)))
                visits.append((d2, t2, float(r.choice([1.25, 1.5, 2.0]))))
                works.append(work2)
                parts += parts2
            wos.append(dict(stores=[no] * len(visits), visits=visits, work=works, call="Service call",
                            parts=round(parts, 2), pm=None, extra=0.0))
    # each work order's invoice on completion (work finished in the last fortnight of a year is invoiced in the first
    # week of the next), numbered in Brannon's own sequence across its customers
    for w in wos:
        last = w["visits"][-1][0]
        if last.month == 12 and last.day >= 18:
            w["invoice_date"] = _wd(dt.date(last.year + 1, 1, 4) + dt.timedelta(days=int(r.integers(0, 3))))
        elif w["pm"] and w["stores"][0] in LATE_JUNE_PM and last.month == 6 and last.day >= 22:
            w["invoice_date"] = _wd(dt.date(2026, 7, 1) + dt.timedelta(days=int(r.integers(0, 2))))
        else:
            w["invoice_date"] = _wd(last + dt.timedelta(days=int(r.integers(0, 3)) if w["pm"] else int(r.integers(1, 4))))
        w["completed"] = last
        price(w)
    tune_cents(wos)
    wos.sort(key=lambda w: (w["invoice_date"], w["stores"][0], w["visits"][0][0]))
    inv = 61840
    for w in wos:
        inv += int(r.integers(3, 40))
        w["invoice"] = str(inv)
    wos.sort(key=lambda w: (w["visits"][0][0], w["stores"][0]))
    wo = 418200
    for w in wos:
        wo += int(r.integers(5, 60))
        w["wo"] = "W%06d" % wo
        w["tech"] = TECHS[int(r.integers(0, len(TECHS)))]
    return wos


def price(w):
    if w["pm"]:
        sub = sum(w["pm"]) + w["parts"] + w["extra"] * LABOR
    else:
        sub = TRIP * len(w["visits"]) + w["parts"]
        for (vd, tt, h) in w["visits"]:
            billed = max(1.0, math.ceil(h * 4) / 4.0)
            sub += billed * (LABOR_AFTER if _after(vd, tt) else LABOR)
    w["subtotal"] = round(sub, 2)
    w["total"] = round(w["subtotal"] + round(w["subtotal"] * TAX + 1e-9, 2), 2)
    w["amount"] = w["subtotal"] if w["invoice_date"] < PLATFORM else w["total"]


def shares(w):
    """each store's part of a work order's total: a route's by its units' maintenance prices"""
    if w["pm"] and len(set(w["stores"])) > 1:
        tot = sum(w["pm"])
        return {no: w["total"] * p / tot for no, p in zip(w["stores"], w["pm"])}
    return {w["stores"][0]: w["total"]}


def store_totals(wos):
    out = defaultdict(float)
    for w in wos:
        if w["completed"].year == 2026:
            for no, v in shares(w).items():
                out[no] += v
    return out


def tune_cents(wos):
    """keep every store's spend off a half dollar and no two stores on one whole dollar: a single-store work order's
    parts move by cents"""
    for _ in range(200):
        tot = store_totals(wos)
        seen = {}
        moved = False
        for no in sorted(W.BY_NO):
            v = tot[no]
            near = abs(v - math.floor(v) - 0.5) < 0.15
            if near or int(v + 0.5) in seen:
                own = [w for w in wos if set(w["stores"]) == {no} and w["completed"].year == 2026]
                calls = [w for w in own if not w["pm"]]
                w = calls[-1] if calls else own[-1]
                if w["pm"] and w["parts"] == 0:
                    w["parts"], w["extra"] = 9.60, 0.25
                    w["work"][0] += "; replaced interior light bulb"
                    d0, t0, h0 = w["visits"][0]
                    w["visits"][0] = (d0, t0, h0 + 0.25)
                else:
                    w["parts"] = round(w["parts"] + 0.35, 2)
                price(w)
                moved = True
                break
            seen[int(v + 0.5)] = no
        if not moved:
            return
    raise AssertionError("tune_cents did not settle")


def service_truth(wos):
    return {no: round(v, 2) for no, v in sorted(store_totals(wos).items())}
