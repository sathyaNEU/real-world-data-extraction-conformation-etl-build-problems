"""The two asks, computed from the shipped files only, with the stops a natural pipeline lands on.

Ask A: the diesel gallons each card account's vehicles bought in May, June and July 2026, by the local day the fuel was
pumped. Delta's direct-bill file stamps each fill in UTC; the Crossroads export and the SMPM file date a fill by the
merchant's business day, which the truck stops close at 10 pm (the odometer on the fill and the vehicle day show which
evening it was pumped).

Ask B: for each month of the 2025 Jackson and Knoxville programmes, the net gallons Overton delivered and the dollars it
billed above its posted rack, taxes aside: each load (terminal bill) once, in the month of its delivery; its billed fuel,
freight and service lines net of credit memos, less its net gallons at the posting in effect when it was lifted (a
posting takes effect at 6 pm the day before its effective date)."""
from __future__ import annotations

import collections
import csv
import datetime as dt
import os
from zoneinfo import ZoneInfo

import calc as C

CT, ET, UTC = ZoneInfo("America/Chicago"), ZoneInfo("America/New_York"), dt.timezone.utc
MONTHS = [(2026, 5), (2026, 6), (2026, 7)]
PROG_MONTHS = {"JXN": [(2025, 3), (2025, 4), (2025, 5)], "KNX": [(2025, 6), (2025, 7), (2025, 8)]}
F_DELIV = "overton_deliveries_2025.csv"
F_INV = "overton_invoices_2025.csv"
F_CRED = "overton_credit_memos_2025.csv"
F_RACK = "overton_rack_postings_2024-09_2026-08.csv"


# ------------------------------------------------------------------------------------------------- Ask A
def pump_dates(P):
    """Each diesel or DEF fill with the local date it was pumped."""
    out = []
    for f in P.cards:
        t = f["t"]
        if f["acct"] == "West":
            d = t.replace(tzinfo=UTC).astimezone(CT).date()
        elif t.hour >= 22:
            d = t.date() - dt.timedelta(days=1)
        else:
            d = t.date()
        out.append((f, d))
    return out


def ask_a(P, mode="golden"):
    """mode: golden; asrecorded (diesel, every date as the file gives it); utc_only (West corrected, business dates
    kept); business_only (business dates corrected, West's UTC read as local); allproducts (DEF in, golden dates)."""
    tot = collections.defaultdict(float)
    for f, d in pump_dates(P):
        if mode != "allproducts" and not f["diesel"]:
            continue
        rec = f["t"].date()
        if mode == "asrecorded":
            d = rec
        elif mode == "utc_only" and f["acct"] != "West":
            d = rec
        elif mode == "business_only" and f["acct"] == "West":
            d = rec
        tot[(f["acct"], (d.year, d.month))] += f["gal"]
    return {(a, m): tot[(a, m)] for a in ("West", "Central", "East") for m in MONTHS}


def ask_a_resent(P):
    """East with the re-sent week counted twice (the batch numbers differ, every detail line repeats)."""
    out = collections.defaultdict(float)
    with open(os.path.join(P.folder, C.F_EAST), encoding="utf-8") as fh:
        for ln in fh:
            if ln.startswith("D") and ln[55:59] == "DSL2":
                t = dt.datetime.strptime(ln[14:22] + ln[22:26], "%Y%m%d%H%M")
                d = t.date() - dt.timedelta(days=1) if t.hour >= 22 else t.date()
                out[(d.year, d.month)] += int(ln[59:68]) / 1000.0
    return {m: out[m] for m in MONTHS}


def odometer_check(P):
    """For the Crossroads and SMPM fills timed 10 pm or later: how many carry an odometer below the starting odometer
    of the vehicle day on their recorded date (pumped the evening before), and how many above it."""
    before = after = unknown = 0
    for f in P.cards:
        if f["acct"] == "West" or not f["diesel"] or f["t"].hour < 22:
            continue
        r = P.days.get(f["unit"], {}).get(f["t"].date())
        if r is None or f["odo"] < 1000:
            unknown += 1
            continue
        if f["odo"] <= r["odo0"] + 0.5:
            before += 1
        else:
            after += 1
    return before, after, unknown


# ------------------------------------------------------------------------------------------------- Ask B
def read_overton(folder):
    rack = {}
    with open(os.path.join(folder, F_RACK), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rack[(r["Terminal"].upper(), dt.date.fromisoformat(r["Effective Date"]))] = float(r["Overton Posted"])
    drops = []
    with open(os.path.join(folder, F_DELIV), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            drops.append(dict(ticket=r["Ticket"], bol=r["Terminal BOL"], terminal=r["Terminal"],
                              lifted=dt.datetime.strptime(r["Lifted"], "%m/%d/%Y %H:%M"),
                              delivered=dt.datetime.strptime(r["Delivered"], "%m/%d/%Y %H:%M"),
                              ship=r["Ship To"], net=float(r["BOL Net Gal"]), gross=float(r["Drop Gross Gal"])))
    inv = []
    with open(os.path.join(folder, F_INV), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            inv.append(dict(inv=r["Invoice"], date=dt.date.fromisoformat(r["Invoice Date"]), bol=r["Terminal BOL"],
                            item=r["Item"], cls=r["Class"], qty=float(r["Qty"]), amt=float(r["Amount"])))
    cred = []
    with open(os.path.join(folder, F_CRED), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            cred.append(dict(memo=r["Credit Memo"], ref=r["Ref Invoice"], bol=r["Terminal BOL"], cls=r["Class"],
                             amt=float(r["Amount"])))
    return rack, drops, inv, cred


def yard_of(ship):
    return ship.split()[1]


def ask_b(folder, mode="golden"):
    """mode: golden; per_drop (net summed over the delivery rows, each row priced at the rack); lift_date (the posting
    dated the lifting day); delivery_date (the posting dated the delivery day); no_credits (every invoice counted, the
    credit memos not read); by_lifting_month (loads dated by lifting)."""
    rack, drops, inv, cred = read_overton(folder)
    loads = {}
    for d in sorted(drops, key=lambda x: x["delivered"]):
        loads.setdefault(d["bol"], d)                    # the load's first drop
    gal = collections.defaultdict(float)
    usd = collections.defaultdict(float)
    month_of = {}
    for bol, d in loads.items():
        when = d["lifted"] if mode == "by_lifting_month" else d["delivered"]
        m = (yard_of(d["ship"]), (when.year, when.month))
        month_of[bol] = m
    if mode == "per_drop":
        for d in drops:
            gal[month_of[d["bol"]]] += d["net"]
    else:
        for bol, d in loads.items():
            gal[month_of[bol]] += d["net"]
    credited = {c["ref"] for c in cred}
    for line in inv:
        if line["cls"] == "TAX":
            continue
        if mode != "no_credits" and line["inv"] in credited:
            continue                                     # reversed in full by its credit memo
        usd[month_of[line["bol"]]] += line["amt"]
    for d in (drops if mode == "per_drop" else loads.values()):
        lifted = d["lifted"]                             # Overton's dispatch clock (Central)
        eff = lifted.date() + dt.timedelta(days=1) if (lifted.hour >= 18 and mode != "lift_date") else lifted.date()
        if mode == "delivery_date":
            eff = loads[d["bol"]]["delivered"].date()
        usd[month_of[d["bol"]]] -= d["net"] * rack[(d["terminal"], eff)]
    out = {}
    for y, ms in PROG_MONTHS.items():
        for m in ms:
            out[(y, m)] = (gal[(y, m)], usd[(y, m)])
    return out


def ask_b_promo(folder):
    """The letters' arithmetic: each load's net gallons at the programme margin, plus the split-drop charges."""
    rack, drops, inv, cred = read_overton(folder)
    promo = {"JXN": 0.024, "KNX": 0.016}
    loads = {}
    for d in sorted(drops, key=lambda x: x["delivered"]):
        loads.setdefault(d["bol"], d)
    out = collections.defaultdict(float)
    for bol, d in loads.items():
        y = yard_of(d["ship"])
        out[(y, (d["delivered"].year, d["delivered"].month))] += d["net"] * promo[y]
    for line in inv:
        if line["cls"] == "SERVICE" and line["inv"] not in {c["ref"] for c in cred}:
            d = loads[line["bol"]]
            out[(yard_of(d["ship"]), (d["delivered"].year, d["delivered"].month))] += line["amt"]
    return dict(out)
