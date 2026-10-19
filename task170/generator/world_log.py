"""The supply side of the clean truth: the facility registry (with the April 2026 regional boundary change and the
codes the registry reissued in early 2026), CMS's customer accounts, every TLD delivery from July 2025 to August 2026
with its proof of delivery, every facility's monthly logistics report, the adult programme projection, and CMS's
stock and shipments at the 31 August 2026 count.

Facility stock is simulated month by month: each ART site dispenses one bottle a month for each patient on TLD
(adults spread over the sites by size, the register's own children at their sites), and CMS tops it up on its route
day towards three months of stock. A delivery is posted in the warehouse system on the day it is picked and signed
for at the facility one to twelve days later. The Northern depot is restocked from the Main warehouse and serves
the Northern and Eastern routes from its own stock."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as C

D = dt.date
DAYS = dt.timedelta

# ------------------------------------------------------------------------------------------------ calendar
LOG_MONTHS = [(2025, m) for m in range(7, 13)] + [(2026, m) for m in range(1, 9)]


def mstart(y, m):
    return D(y, m, 1)


def mend(y, m):
    return D(y + (m == 12), m % 12 + 1, 1) - DAYS(days=1)


# ------------------------------------------------------------------------------------------------ registry
REISSUE = 7          # codes of sites closed in March 2026 reissued to new sites opened in April and May


def registry(F, rng, child_fac):
    """Registry records. Every operational ART site of the simulation keeps its code; seven small sites without
    paediatric patients close in March 2026 and their codes go to seven new sites in other regions opened in April or
    May 2026."""
    recs = []
    for k, f in enumerate(F):
        recs.append(dict(rid=k, mfl=f["mfl"], type=f["type"], district=f["district"], region=f["region"],
                         region_old=f["region_old"], opened=D(1998 + int(rng.integers(0, 22)), int(rng.integers(1, 13)), 1),
                         closed=None, size=f["size"], paper=f["paper"], has_children=k in child_fac))
    chosen = [recs[k] for k, f in enumerate(F) if f["closing"]]
    assert len(chosen) == REISSUE and not any(r["has_children"] for r in chosen)
    dists = {d[0]: d for d in C.DISTRICTS}
    new = []
    for j, r in enumerate(chosen):
        r["closed"] = D(2026, 3, int(rng.integers(10, 26)))
        others = [d for d in C.DISTRICTS if d[2] != r["region"]]
        dd = others[int(rng.integers(0, len(others)))]
        new.append(dict(rid=len(recs) + j, mfl=r["mfl"], type="Clinic", district=dd[0], region=dd[2], region_old=dd[3],
                        opened=D(2026, 4 + (j % 2), int(rng.integers(1, 20))), closed=None,
                        size=float(rng.uniform(0.6, 1.2)), paper=False, has_children=False))
    return recs + new, chosen, new


def region_at(rec, d):
    """The region a registry record's site sat in on date d (the boundary change took effect on 1 April 2026)."""
    return rec["region"] if d >= C.REALIGN else rec["region_old"]


# ------------------------------------------------------------------------------------------------ demand
def adults_by_site(recs, rng, national_aug=309_640):
    """Adults (15 and over) on TLD at each site at the end of August 2026, spread by size; earlier months grow back
    at the site's own rate."""
    live = [r for r in recs if r["closed"] is None]
    w = np.array([r["size"] * float(rng.lognormal(0, 0.18)) for r in live])
    w = w / w.sum()
    out = {}
    for r, s in zip(live, w):
        out[r["rid"]] = s * national_aug
    for r in recs:
        if r["closed"] is not None:
            out[r["rid"]] = float(rng.lognormal(np.log(700), 0.5))
    return out


def monthly_patients(recs, adults_aug, kids_tld, rng):
    """Patients on TLD at each site at each month end, July 2025 to August 2026: adults growing at 0.15 to 0.35 per
    cent a month back from August, the register's children on TLD at the site; a closed site's patients until it
    closes, a new site's from its opening, building up."""
    pats = {}
    for r in recs:
        g = float(rng.uniform(0.0015, 0.0035))
        series = []
        for (y, m) in LOG_MONTHS:
            k = (2026 - y) * 12 + (8 - m)
            a = adults_aug[r["rid"]] / (1 + g) ** k
            e = mend(y, m)
            if r["closed"] is not None and e > r["closed"]:
                a = 0.0
            if r["opened"] > e:
                a = 0.0
            elif r["opened"].year == 2026 and r["closed"] is None and r["opened"] >= D(2026, 1, 1):
                months_open = (e.year - r["opened"].year) * 12 + e.month - r["opened"].month + 1
                a = adults_aug[r["rid"]] * min(1.0, 0.35 + 0.13 * months_open)
            ch = kids_tld.get((r["rid"], y, m), 0)
            series.append(a + ch)
        pats[r["rid"]] = series
    return pats


# ------------------------------------------------------------------------------------------------ flows
REFUSE_REASONS = ["Refused: short expiry", "Refused: cartons damaged", "Refused: not ordered", "Refused: store locked"]


def donation_sites(recs, rng):
    """About one ART site in eight, at least three in every region, received a partner's emergency donation of TLD
    in November 2025 when CMS stock ran short; it is dispensed before CMS stock until it runs out."""
    out = set()
    for reg in C.REGIONS:
        live = [r["rid"] for r in recs if r["closed"] is None and r["region"] == reg and r["opened"] < D(2025, 7, 1)]
        k = max(3, int(round(0.125 * len(live))))
        for j in rng.permutation(len(live))[:k]:
            out.add(live[j])
    return out


def flows(recs, pats, rng):
    """Month by month at every site: dispensing, CMS deliveries (route day, posting and signature dates, the odd
    delivery refused at the gate and returned), the partner donation, short-dated stock handed back to CMS, stock.
    Returns dispensing and closing stock per site-month (CMS stock and donated stock apart), the deliveries and the
    returns."""
    disp, close, opening, recv = {}, {}, {}, {}
    don = {}
    deliveries = []
    returns = []
    # short-dated stock a facility hands back to CMS for redistribution (its own draws, so every other draw stands)
    rng_ret = np.random.default_rng(C.SEED + 404)
    route_day = {r["rid"]: int(rng.integers(3, 25)) for r in recs}
    every2 = {r["rid"]: bool(rng.random() < 0.35 and r["type"] in ("Clinic", "Private clinic") and r["closed"] is None)
              for r in recs}
    dsites = donation_sites(recs, rng)
    warm = [(2025, m) for m in range(1, 7)]
    for r in recs:
        rid = r["rid"]
        stock = pats[rid][0] * float(rng.uniform(2.2, 3.4))
        dstock = 0.0
        d_day = int(rng.integers(10, 26))
        for jj, (y, m) in enumerate(warm + LOG_MONTHS):
            j = jj - len(warm)
            p = pats[rid][max(0, j)]
            if j < 0 and r["opened"] > mend(y, m):
                p = 0.0
            if j < 0:
                # the six months before the extract: the site's stock settles; nothing is recorded
                due = (not every2[rid]) or (jj % 2 == rid % 2)
                if p > 0 and due:
                    q = 3.0 * p - stock + p
                    if q > 0.15 * p:
                        stock += int(np.ceil(q / 12.0) * 12)
                stock = max(0.0, stock - p)
                continue
            live = p > 0
            if not live:
                disp[(rid, y, m)] = 0
                opening[(rid, y, m)] = int(round(stock)) if stock > 0 else 0
                recv[(rid, y, m)] = 0
                close[(rid, y, m)] = 0
                stock = 0
                continue
            opening[(rid, y, m)] = int(round(stock))
            d_open = int(round(dstock))
            d_got = 0
            if rid in dsites and (y, m) == (2025, 11):
                d_got = int(np.ceil(p * float(rng.uniform(2.0, 3.0)) / 12.0) * 12)
                dstock += d_got
            got = 0
            due = (not every2[rid]) or (j % 2 == rid % 2)
            if due:
                target = 3.0 * p
                q = target - stock - dstock + p
                if q > 0.15 * p:
                    q = int(np.ceil(q / 12.0) * 12)
                    signed = D(y, m, min(28, route_day[rid] + int(rng.integers(-2, 3))))
                    if (y, m) == (2026, 1) and signed.day <= 10:
                        # CMS closes over the holidays: an early-January delivery goes out in mid-December
                        signed = D(2025, 12, int(rng.integers(15, 20)))
                    # a new site's opening stock arrives on the day it opens
                    signed = max(signed, r["opened"])
                    posted = signed - DAYS(days=int(rng.integers(1, 13)))
                    refused = bool(rng.random() < 0.016)
                    dl = dict(rid=rid, qty=q, posted=posted, signed=signed, refused=refused)
                    if refused:
                        dl["reason"] = REFUSE_REASONS[int(rng.integers(0, len(REFUSE_REASONS)))]
                        dl["returned"] = signed + DAYS(days=int(rng.integers(2, 7)))
                    deliveries.append(dl)
                    got = 0 if refused else q
            need = int(round(p * float(rng.normal(1.0, 0.035))))
            from_don = int(min(need, dstock))
            d_ = max(0, min(need - from_don, int(stock + got)))
            dstock -= from_don
            stock = stock + got - d_
            loss = int(rng.random() < 0.06) * int(rng.integers(1, 30))
            stock = max(0, stock - loss)
            if rng_ret.random() < 0.035 and stock >= 240:
                k = int(min(rng_ret.integers(2, 10), stock // 24)) * 12
                coll = D(y, m, int(rng_ret.integers(5, 26)))
                returns.append(dict(rid=rid, qty=k, collected=coll, posted=coll + DAYS(days=int(rng_ret.integers(3, 11)))))
                stock -= k
            disp[(rid, y, m)] = d_
            recv[(rid, y, m)] = got
            close[(rid, y, m)] = int(round(stock))
            if rid in dsites and (d_open > 0 or d_got > 0):
                don[(rid, y, m)] = dict(opening=d_open, received=d_got, dispensed=from_don, closing=int(round(dstock)))
    return disp, close, opening, recv, deliveries, don, returns


# ------------------------------------------------------------------------------------------------ the call's inputs
def projection(recs, adults_aug, rng):
    """The programme's projection of patients on TLD aged 15 and over at the count and every new initiation, by
    region, for each month from September 2026 to June 2027."""
    base = {}
    for r in recs:
        if r["closed"] is None:
            base[r["region"]] = base.get(r["region"], 0.0) + adults_aug[r["rid"]]
    out = {}
    for reg in C.REGIONS:
        g = float(rng.uniform(0.0016, 0.0031))
        out[reg] = [int(round(base[reg] * (1 + g) ** k)) for k in range(1, 11)]
    return out


def cms_stock(rng):
    """TLD 30-tablet bottles at CMS at the 31 August 2026 count, by warehouse and batch (usable and quarantined),
    and the shipments on order. The November lot of the C6 order is set by the generator (pack.place_order)."""
    batches = []
    for wh, n, lo, hi in (("Main warehouse", 6, 90_000, 260_000), ("Northern depot", 3, 25_000, 75_000)):
        for k in range(n):
            q = int(rng.integers(lo, hi))
            q -= q % 96
            q += int(rng.integers(0, 96)) if k == 0 else 0
            exp = D(2027 + int(rng.integers(0, 3)), int(rng.integers(1, 13)), 1) - DAYS(days=1)
            batches.append(dict(warehouse=wh, batch="TL%02d%04d" % (24 + int(rng.integers(1, 3)), int(rng.integers(1000, 9999))),
                                qty=q, expiry=exp, status="Usable"))
    q = int(rng.integers(18_000, 26_000))
    batches.append(dict(warehouse="Main warehouse", batch="TL25%04d" % int(rng.integers(1000, 9999)), qty=q - q % 96,
                        expiry=D(2028, 3, 31), status="Quarantined"))
    ship = [dict(po="PO-2026-0147", lot=1, qty=0, due=D(2026, 9, 18), status="Confirmed"),
            dict(po="PO-2026-0147", lot=2, qty=0, due=D(2026, 10, 23), status="Confirmed"),
            dict(po="PO-2026-0147", lot=3, qty=0, due=D(2026, 11, 20), status="Confirmed"),
            dict(po="FW-2027-C7A", lot=1, qty=0, due=D(2027, 2, 15), status="Planned")]
    for s, (lo, hi) in zip(ship, ((380_000, 420_000), (360_000, 400_000), (300_000, 340_000), (600_000, 700_000))):
        x = int(rng.integers(lo, hi))
        s["qty"] = x - x % 96
    return batches, ship
