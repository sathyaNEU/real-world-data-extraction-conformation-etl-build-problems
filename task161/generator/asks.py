"""task161 asks: the golden and every alternative path for the two supplemental asks.

A1: pallets outside the racks at the close of 6 December in each of the four buildings.
A2: for each month of 2026 to October, the TEU of the import containers whose freight reached the
    book from the two ports, and that TEU as a share of the two ports' loaded import TEU.

Inputs are plain records, so the same code runs on the generator's data and on files read back from
target/ (golden.py, verify.py, cracker.py).
"""
import datetime as dt
import numpy as np

BUILDINGS = ["CAR1", "RDZ1", "WIL1", "CMP1"]
TEU = {"22G1": 1.0, "42G1": 2.0, "45G1": 2.0, "L5G1": 2.25}
MONTHS_2026 = [(2026, m) for m in range(1, 11)]


# ----------------------------------------------------------------------------------- A1

def a1_golden(site_onhand, lpn_rows):
    """site_onhand: {site: pallets on hand at the close (every location of the site, yard trailers
    included)}; lpn_rows: the warehouse-location export at the same close. Outside the racks is
    what the site holds less what sits in its rack locations."""
    racked = {s: 0 for s in BUILDINGS}
    for r in lpn_rows:
        if r["location_type"] == "RACK" and r["site"] in racked:
            racked[r["site"]] += 1
    return {s: int(site_onhand[s] - racked[s]) for s in BUILDINGS}


def a1_lpn_only(lpn_rows):
    """Cracker path: the pallet-level export's non-rack rows by building (floor lanes and staging)."""
    out = {s: 0 for s in BUILDINGS}
    for r in lpn_rows:
        if r["location_type"] != "RACK" and r["site"] in out:
            out[r["site"]] += 1
    return out


# ----------------------------------------------------------------------------------- A2

def box_visits(receipts, to_local, gap_days=3):
    """One visit per ocean box arrival: receipts of the same box number within gap_days of each other
    are one box devanned across shifts; the same number months later is the box back with new freight."""
    last = {}
    visits = []
    for r in sorted(receipts, key=lambda x: x["received_at"]):
        if r["type"] not in TEU:
            continue
        d = to_local(r["received_at"])
        cn = r["equipment"]
        if cn in last and (d - last[cn][0]).days <= gap_days:
            last[cn] = (d, last[cn][1])
            continue
        last[cn] = (d, len(visits))
        visits.append((d, r["type"]))
    return visits


def a2_golden(receipts, manifest, la, lb, to_local):
    """receipts: dicts with received (UTC datetime), type, equipment; manifest: trailer -> source boxes
    with ISO types; la, lb: {month: loaded import TEU}. TEU counts direct ocean boxes by ISO type and
    the source boxes of every transload trailer; domestic transfers carry no port box."""
    src = {}
    for m in manifest:
        src.setdefault(m["trailer"], []).append(m["iso"])
    teu = {k: 0.0 for k in MONTHS_2026}
    for d, typ in box_visits(receipts, to_local):
        k = (d.year, d.month)
        if k in teu:
            teu[k] += TEU[typ]
    for r in receipts:
        if r["type"] == "53DV" and r["equipment"] in src:
            d = to_local(r["received_at"])
            k = (d.year, d.month)
            if k in teu:
                teu[k] += sum(TEU[t] for t in src[r["equipment"]])
    share = {k: 100.0 * teu[k] / (la[k] + lb[k]) for k in teu}
    return teu, share


def a2_variant(receipts, manifest, la, lb, to_local, trailers="exclude", month="local", teu45=2.25):
    """Alternative handlings: 53ft trailers excluded or counted at 53/20 TEU, the month taken from
    the UTC date, a 45ft box at 2 TEU."""
    src = {}
    for m in manifest:
        src.setdefault(m["trailer"], []).append(m["iso"])
    t = dict(TEU)
    t["L5G1"] = teu45
    teu = {k: 0.0 for k in MONTHS_2026}
    for r in receipts:
        d = to_local(r["received_at"]) if month == "local" else r["received_at"].date()
        k = (d.year, d.month)
        if k not in teu:
            continue
        if r["type"] in t:
            teu[k] += t[r["type"]]
        elif r["type"] == "53DV":
            if trailers == "len20":
                teu[k] += 53.0 / 20.0
            elif trailers == "manifest" and r["equipment"] in src:
                teu[k] += sum(t[x] for x in src[r["equipment"]])
            elif trailers == "all53_manifest":
                teu[k] += sum(t[x] for x in src.get(r["equipment"], [])) if r["equipment"] in src else 53.0 / 20.0
    share = {k: 100.0 * teu[k] / (la[k] + lb[k]) for k in teu}
    return teu, share


def rounded_a2(teu, share):
    """TEU to the whole TEU, shares in per cent to three decimals, as the prompt asks."""
    return {k: int(round(teu[k])) for k in teu}, {k: round(share[k], 3) for k in share}


def a2_rows(receipts, manifest, la, lb, to_local, dedup="none", trailers="exclude", month="local",
            teu45=2.25, gap_days=3):
    """Cracker and mirror paths: boxes counted per receipt row, or deduplicated globally on the box
    number, or by visit; 53ft trailers excluded, counted at 53/20 TEU, or through the manifest."""
    src = {}
    for m in manifest:
        src.setdefault(m["trailer"], []).append(m["iso"])
    t = dict(TEU)
    t["L5G1"] = teu45
    def day(r):
        return to_local(r["received_at"]) if month == "local" else r["received_at"].date()
    teu = {k: 0.0 for k in MONTHS_2026}
    boxes = [r for r in receipts if r["type"] in t]
    if dedup == "global":
        firsts = {}
        for r in sorted(boxes, key=lambda x: x["received_at"]):
            firsts.setdefault(r["equipment"], r)
        boxes = list(firsts.values())
        for r in boxes:
            k = (day(r).year, day(r).month)
            if k in teu:
                teu[k] += t[r["type"]]
    elif dedup == "visit":
        for d, typ in box_visits(boxes, to_local if month == "local" else (lambda ts: ts.date()), gap_days):
            k = (d.year, d.month)
            if k in teu:
                teu[k] += t[typ]
    elif dedup == "sameday":
        seenk = set()
        for r in boxes:
            key = (r["equipment"], day(r))
            if key in seenk:
                continue
            seenk.add(key)
            k = (day(r).year, day(r).month)
            if k in teu:
                teu[k] += t[r["type"]]
    else:
        for r in boxes:
            k = (day(r).year, day(r).month)
            if k in teu:
                teu[k] += t[r["type"]]
    for r in receipts:
        if r["type"] != "53DV":
            continue
        k = (day(r).year, day(r).month)
        if k not in teu:
            continue
        if trailers == "len20":
            teu[k] += 53.0 / 20.0
        elif trailers == "manifest" and r["equipment"] in src:
            teu[k] += sum(t[x] for x in src[r["equipment"]])
    share = {k: 100.0 * teu[k] / (la[k] + lb[k]) for k in teu}
    return teu, share
