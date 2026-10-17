"""The two asks, computed from the shipped files only, with the stops a natural pipeline lands on.

Ask A: the diesel gallons each card account's vehicles bought in May, June and July 2026, by the local day of each
purchase. Riverbend stamps each transaction in UTC (Schedule A, A5); Crossroads and SMPM date a sale made at 10 pm or
later with the next day (Pricing Addendum 4, clause 5; the SMPM layout, positions 15-22); a duplicate posting and the
later credit that reverses it are no purchase (A6; clause 6; the layout's C record).

Ask B: for each month of the 2025 Jackson and Knoxville programmes, the net gallons Overton delivered and the dollars it
billed over the posted rack value of those gallons after credits, taxes aside: each load (terminal bill) once, in the
month of its delivery (one invoice per bill, dated the day of delivery); its billed fuel and delivery service lines net
of the credit memos (a credited invoice out, its rebill in), less its net gallons at Overton's posting in effect when it
was lifted (posted at 6 pm Central with the next day's date, the 2025 letters)."""
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
def pump_date(f):
    """The local day a card line was made: Riverbend's stamps are UTC (Schedule A, A5); Crossroads and SMPM date a sale
    made at 10 pm or later with the next day (Pricing Addendum 4, clause 5; the SMPM layout)."""
    t = f["t"]
    if f["acct"] == "West":
        return t.replace(tzinfo=UTC).astimezone(CT).date()
    if t.hour >= 22:
        return t.date() - dt.timedelta(days=1)
    return t.date()


def ask_a(P, mode="golden", credits="excluded"):
    """mode: golden (each line on the day it was made); asrecorded (every date as the file gives it); utc_only
    (Riverbend corrected, business dates kept); business_only (business dates corrected, Riverbend's UTC read as
    local); allproducts (DEF in). credits: excluded (a duplicate posting and the credit that reverses it are no
    purchase), netted (every line summed on its own date) or kept (the credits dropped, the duplicates kept)."""
    tot = collections.defaultdict(float)
    for f in P.cards:
        if mode != "allproducts" and not f["diesel"]:
            continue
        if credits == "excluded" and f["role"] != "sale":
            continue
        if credits == "kept" and f["role"] == "credit":
            continue
        d = pump_date(f)
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
    """Holston's diesel with the week received twice kept twice (the two transmissions differ only in batch number)."""
    out = collections.defaultdict(float)
    credited = {f["key"][1] for f in P.cards if f["acct"] == "East" and f["role"] == "dup"}
    with open(os.path.join(P.folder, C.F_EAST), encoding="utf-8") as fh:
        for ln in fh:
            if ln.startswith("D") and ln[55:59] == "DSL2" and ln[1:14] not in credited:
                t = dt.datetime.strptime(ln[14:22] + ln[22:26], "%Y%m%d%H%M")
                d = t.date() - dt.timedelta(days=1) if t.hour >= 22 else t.date()
                out[(d.year, d.month)] += int(ln[59:68]) / 1000.0
    return {m: out[m] for m in MONTHS}


def odometer_check(P):
    """For the Crossroads and SMPM sales timed 10 pm or later: how many carry an odometer at or below the starting
    odometer of the vehicle day on their recorded date (pumped the evening before), and how many above it."""
    before = after = unknown = 0
    for f in P.cards:
        if f["acct"] == "West" or not f["diesel"] or f["role"] != "sale" or f["t"].hour < 22:
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
                              lifted=dt.datetime.strptime(r["Lifted (CT)"], "%m/%d/%Y %H:%M"),
                              delivered=dt.datetime.strptime(r["Delivered (CT)"], "%m/%d/%Y %H:%M"),
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
    credit memos not read); no_rebills (a credited invoice and its rebill both left out); fuel_only (the delivery
    service lines left out); by_lifting_month (loads dated by lifting); by_invoice_month (dollars by invoice date)."""
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
    credited_bols = {line["bol"] for line in inv if line["inv"] in credited}
    for line in inv:
        if line["cls"] == "TAX":
            continue
        if mode == "fuel_only" and line["cls"] != "PRODUCT":
            continue
        if mode != "no_credits" and line["inv"] in credited:
            continue                                     # reversed in full by its credit memo
        if mode == "no_rebills" and line["bol"] in credited_bols:
            continue
        m = month_of[line["bol"]]
        if mode == "by_invoice_month":
            m = (m[0], (line["date"].year, line["date"].month))
        usd[m] += line["amt"]
    for d in (drops if mode == "per_drop" else loads.values()):
        if mode == "no_rebills" and d["bol"] in credited_bols:
            continue
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
