"""What the systems recorded by 31 December 2026: the ledger's records (clerk-keyed notices and, from 2026, the
custodian feed's distribution advices), the withdrawn and reissued notices, cash arrival dates and the custodian's
programme account. Works on the simulated world in place and returns the records pack.py writes."""
from datetime import date, datetime, timedelta

import numpy as np

import world as W

BOUNDARIES = [date(2025, 12, 31), date(2026, 3, 31), date(2026, 6, 30), date(2026, 9, 30), date(2026, 12, 31)]
FEED = set(W.FEED_START)


def is_cash(n):
    return any(l[0] != "IN_KIND" for l in n["lines"])


def cash_total(n):
    return round(sum(l[3] for l in n["lines"] if l[0] != "IN_KIND"), 2)


def clerk_keys(f, n):
    """True when Rechnungswesen keyed this notice from the manager's PDF."""
    if n["type"] != "DISTRIBUTION" or f.mcode not in FEED:
        return True
    stop = W.CLERK_STOP.get(f.mcode, W.PARALLEL_END + timedelta(days=1))
    return n["notice_date"] < stop


def on_feed(f, n):
    """True when the custodian's CF-PM feed loaded an advice for this notice's cash."""
    return (f.mcode in FEED and n["type"] == "DISTRIBUTION" and n["status"] == "ISSUED" and is_cash(n)
            and W.FEED_START[f.mcode] <= n["arrival"] <= W.PLAN_DATE)


def _arrivals(funds, rng):
    for f in funds:
        for n in sorted(f.notices, key=lambda x: (x["notice_date"], x["notice_id"])):
            n["arrival"] = n["value_date"]
            if n["type"] == "DISTRIBUTION" and f.ccy != "CHF" and n["value_date"] >= date(2024, 1, 1) and rng.rand() < 1 / 6.0:
                n["arrival"] = W.add_bdays(n["value_date"], int(rng.randint(1, 5)))


def _boundary_items(funds, rng, held_fn):
    """Each strategy gets, at each 2026 quarter edge, a distribution of a manager the clerks key whose cash arrives
    after the edge although the notice states a payment date before it (cross-border credits routinely do)."""
    made = []
    for s in ("BO", "GR", "PC", "IN"):
        pool = [f for f in funds if f.strategy == s and f.mcode not in FEED]
        for B in BOUNDARIES:
            crossing = [(f, n) for f in pool for n in f.notices if n["type"] == "DISTRIBUTION" and n["status"] == "ISSUED"
                        and is_cash(n) and n["value_date"] <= B < n["arrival"]]
            if crossing:
                made.append((s, B, crossing[0][1]["notice_id"], "natural"))
                continue
            cands = [(abs((n["value_date"] - B).days), f.idx, n["notice_id"], f, n) for f in pool for n in f.notices
                     if n["type"] == "DISTRIBUTION" and n["status"] == "ISSUED" and is_cash(n) and f.ccy != "CHF"
                     and abs((n["value_date"] - B).days) <= 21]
            if cands:
                _, _, _, f, n = sorted(cands, key=lambda c: (c[0], c[1], c[2]))[0]
                vd = W.bday_back(B - timedelta(days=int(rng.randint(0, 2))))
                n["value_date"] = vd
                n["notice_date"] = min(n["notice_date"], W.bday_back(vd - timedelta(days=7)))
                n["arrival"] = W.add_bdays(vd, int(rng.randint(1, 4)))
                while n["arrival"] <= B:
                    n["arrival"] = W.add_bdays(n["arrival"], 1)
                made.append((s, B, n["notice_id"], "moved"))
                continue
            # no distribution near the edge: a held company pays a dividend recapitalisation or an income distribution
            hosts = [f for f in pool if f.ccy != "CHF" and held_fn(f, B)] or [f for f in pool if held_fn(f, B)]
            f = hosts[int(rng.randint(len(hosts)))]
            iv = held_fn(f, B)
            amt = round(iv.cost * float(rng.uniform(0.05, 0.11)), 2)
            vd = W.bday_back(B - timedelta(days=int(rng.randint(0, 2))))
            nd = W.bday_back(vd - timedelta(days=int(rng.randint(7, 11))))
            f.n_dn += 1
            n = dict(notice_id=f"{f.code}-DN-{f.n_dn:03d}", type="DISTRIBUTION", notice_date=nd, value_date=vd,
                     arrival=W.add_bdays(vd, int(rng.randint(1, 4))), status="ISSUED", remarks="", source="clerk",
                     lines=[("INCOME", iv.ref, f"Dividend recapitalisation: {iv.company}", amt)])
            while n["arrival"] <= B:
                n["arrival"] = W.add_bdays(n["arrival"], 1)
            f.notices.append(n)
            made.append((s, B, n["notice_id"], "created"))
    return made


def _held_at(f, d):
    held = [iv for iv in f.investments if iv.initial_date <= d - timedelta(days=120) and (iv.exit_date is None or iv.exit_date > d + timedelta(days=30))
            and iv.status in ("HELD", "REALISED")]
    held.sort(key=lambda iv: (-iv.cost, iv.ref))
    return held[0] if held else None


def _withdraw_distribution(funds, rng):
    cands = [(n["value_date"], f.idx, n["notice_id"], f, n) for f in funds if f.strategy == "PC" and f.mcode not in FEED
             for n in f.notices if n["type"] == "DISTRIBUTION" and n["status"] == "ISSUED" and is_cash(n)
             and date(2026, 4, 1) <= n["value_date"] <= date(2026, 6, 19)]
    cands.sort(key=lambda c: (c[0], c[1], c[2]))
    _, _, _, f, n = cands[len(cands) // 2]
    new = dict(n)
    new["notice_id"] = n["notice_id"] + "R"
    shift = int(rng.randint(2, 5))
    new["notice_date"] = W.add_bdays(n["notice_date"], shift)
    new["value_date"] = W.add_bdays(n["value_date"], shift)
    new["arrival"] = new["value_date"]
    new["remarks"] = f"reissue of {n['notice_id']}"
    n["status"] = "CANCELLED"
    n["remarks"] = f"withdrawn by manager; reissued as {new['notice_id']}"
    f.notices.append(new)
    return n["notice_id"]


def _in_specie(funds):
    cands = [(n["value_date"], f.idx, n["notice_id"], f, n) for f in funds if f.strategy == "GR" and f.mcode not in FEED
             for n in f.notices if n["type"] == "DISTRIBUTION" and n["status"] == "ISSUED"
             and date(2026, 7, 1) <= n["value_date"] <= date(2026, 9, 25)
             and any(l[0] == "RETURN_OF_CAPITAL" for l in n["lines"]) and any(l[0] == "REALISED_GAIN" for l in n["lines"])]
    if not cands:
        raise RuntimeError("no growth realisation in the third quarter of 2026 to settle in specie")
    cands.sort(key=lambda c: (c[0], c[1], c[2]))
    _, _, _, f, n = cands[0]
    ref = next(l[1] for l in n["lines"] if l[0] == "RETURN_OF_CAPITAL")
    iv = next(i for i in f.investments if i.ref == ref)
    total = round(sum(l[3] for l in n["lines"] if l[1] == ref), 2)
    n["lines"] = [l for l in n["lines"] if l[1] != ref] + [("IN_KIND", ref, f"Distribution in specie: listed shares of {iv.company}", total)]
    iv.status = "REALISED_IN_KIND"
    return n["notice_id"]


def _withdraw_calls(funds, rng):
    calls = [(n["notice_date"], f.idx, n["notice_id"], f, n) for f in funds for n in f.notices if n["type"] == "CAPITAL_CALL"
             and date(2019, 1, 1) <= n["notice_date"] <= date(2026, 11, 20)
             and not (n["notice_date"] <= f.ip_end <= n["value_date"] + timedelta(days=10))]
    calls.sort(key=lambda x: (x[0], x[1], x[2]))
    picks = [calls[k] for k in sorted(rng.choice(len(calls), 11, replace=False))]
    out = []
    for _, _, _, f, n in picks:
        shift = int(rng.randint(2, 5))
        new = dict(n)
        new["notice_id"] = n["notice_id"] + "R"
        new["notice_date"] = W.add_bdays(n["notice_date"], shift)
        new["value_date"] = W.add_bdays(n["value_date"], shift)
        if new["notice_date"].month == 12 and new["value_date"].year != new["notice_date"].year:
            new["value_date"] = W.bday_back(date(new["notice_date"].year, 12, 22))
        if new["notice_date"] <= f.ip_end < new["value_date"]:
            new["value_date"] = W.bday_back(f.ip_end)
        new["arrival"] = new["value_date"]
        new["remarks"] = f"reissue of {n['notice_id']}"
        n["status"] = "CANCELLED"
        n["remarks"] = f"withdrawn by manager; reissued as {new['notice_id']}"
        f.notices.append(new)
        out.append(n["notice_id"])
    return out


def observe(funds, fx):
    rng = np.random.RandomState(W.SEED * 31)
    _arrivals(funds, rng)
    withdrawn_calls = _withdraw_calls(funds, rng)
    rng_d = np.random.RandomState(W.SEED * 31 + W.DIST_STREAM)   # the 2025-26 distribution timings, a stream of their own
    boundary = _boundary_items(funds, rng_d, _held_at)
    withdrawn_dist = _withdraw_distribution(funds, rng_d)
    in_specie = _in_specie(funds)
    feed_seq = [0]

    # custodian references, one per cash movement on the programme account, in date order
    events = []
    for f in funds:
        for n in f.notices:
            if n["status"] != "ISSUED":
                continue
            if n["type"] == "CAPITAL_CALL" and date(2025, 1, 1) <= n["value_date"] <= W.PLAN_DATE:
                events.append((n["value_date"], 0, f.idx, n["notice_id"], f, n))
            if n["type"] == "DISTRIBUTION" and is_cash(n) and date(2025, 1, 1) <= n["arrival"] <= W.PLAN_DATE:
                events.append((n["arrival"], 1, f.idx, n["notice_id"], f, n))
    events.sort(key=lambda e: (e[0], e[1], e[2], e[3]))
    for k, (d, kind, _, _, f, n) in enumerate(events):
        n["custodian_ref"] = f"PM{d.year % 100:02d}-{100417 + k * 3 + (k % 7):06d}"

    # the ledger's records: clerk-keyed notices, and from 2026 the feed's advices
    records = []
    for f in funds:
        for n in f.notices:
            if n["notice_date"] > W.PLAN_DATE:
                continue
            if clerk_keys(f, n):
                records.append(dict(n, fund=f, source="clerk"))
            if on_feed(f, n):
                cats = [l[0] for l in n["lines"] if l[0] != "IN_KIND"]
                cat = "RETURN_OF_CAPITAL" if "RETURN_OF_CAPITAL" in cats else ("REALISED_GAIN" if "REALISED_GAIN" in cats else "INCOME")
                feed_seq[0] += 1
                records.append(dict(notice_id=n["custodian_ref"], type="DISTRIBUTION", notice_date=n["arrival"],
                                    value_date=n["arrival"], arrival=n["arrival"], status="ISSUED", remarks="", fund=f,
                                    source="feed", lines=[(cat, "", f"Distribution {f.name}, advice {n['custodian_ref']}", cash_total(n))],
                                    of=n["notice_id"]))
    return dict(records=records, events=events, withdrawn_calls=withdrawn_calls, withdrawn_dist=withdrawn_dist,
                in_specie=in_specie, boundary=boundary)


def custodian_postings(funds, fx, events, rng_seed=W.SEED * 37):
    """The programme account at the custodian (CHF), 1 January 2025 to 31 December 2026: calls paid, distributions
    credited and swept to the general portfolio the same day, top-ups from the general portfolio, the facility drawn in
    the September 2026 week, interest and charges. Foreign currency is converted at the custodian's dealing rate."""
    rng = np.random.RandomState(rng_seed)
    rows = []
    bal = 36_284_336.18
    rows.append(dict(booking_date=date(2025, 1, 1), value_date=date(2025, 1, 1), text="Saldovortrag", counterparty="", reference="Opening balance 2025",
                     transaction_ref="PM25-100000", amount=bal, kind="open"))
    by_day = {}
    for d, kind, _, _, f, n in events:
        by_day.setdefault(d, []).append((kind, f, n))
    d = date(2025, 1, 1)
    month_seen = set()
    facility_drawn = 0.0
    while d <= W.PLAN_DATE:
        if d.weekday() < 5:
            key = (d.year, d.month)
            # the reserve was CHF 35 million under RL-PM-04 and is CHF 150 million from October 2026; in September 2026 the
            # month's transfer from the general portfolio waited for a bond sale to settle
            held_back = date(2026, 8, 24) <= d < date(2026, 9, 24)
            level = W.RESERVE if d >= date(2026, 10, 1) else 35_000_000.0
            due_today = sum(sum(l[3] for l in n["lines"]) * fx.rate(d, f.ccy) for kind, f, n in by_day.get(d, []) if kind == 0)
            low = bal - due_today < 8_000_000.0
            if (key not in month_seen or low) and not held_back:
                month_seen.add(key)
                top = round(level - bal + facility_drawn + due_today * (1 if low else 0) + float(rng.uniform(250_000, 2_400_000)), 2)
                if top > 0:
                    bal += top
                    rows.append(dict(booking_date=d, value_date=d, text="Uebertrag vom Gesamtportfolio", counterparty=W.ORG,
                                     reference=f"Liquiditaetsausgleich Programmkonto {d:%d.%m.%Y}", transaction_ref="", amount=top, kind="topup"))
            for kind, f, n in sorted(by_day.get(d, []), key=lambda x: (x[0], x[1].idx, x[2]["notice_id"])):
                fcy = sum(l[3] for l in n["lines"] if l[0] != "IN_KIND")
                ref = fx.rate(d, f.ccy)
                if kind == 0:
                    spread = 0.0 if f.ccy == "CHF" else float(rng.uniform(0.0015, 0.0035))
                    chf = round(fcy * ref * (1 + spread), 2)
                    bal -= chf
                    rows.append(dict(booking_date=d, value_date=d, text="Zahlung Kapitalabruf", counterparty=f.paying_agent,
                                     reference=f"{n['notice_id']} {f.name}", transaction_ref=n["custodian_ref"], amount=-chf, kind="call"))
                    if bal < 0.0:
                        draw = float(np.ceil((-bal + 5_000_000) / 1_000_000) * 1_000_000)
                        facility_drawn += draw
                        bal += draw
                        rows.append(dict(booking_date=d, value_date=d, text="Ziehung Standby-Fazilitaet", counterparty=W.BANK,
                                         reference="Standby facility 2026, drawing", transaction_ref="", amount=draw, kind="facility"))
                else:
                    spread = 0.0 if f.ccy == "CHF" else float(rng.uniform(0.0015, 0.0035))
                    chf = round(fcy * ref * (1 - spread), 2)
                    rows.append(dict(booking_date=d, value_date=d, text="Gutschrift Ausschuettung", counterparty=f.paying_agent,
                                     reference=f"{n['notice_id']} {f.name}", transaction_ref=n["custodian_ref"], amount=chf, kind="dist"))
                    rows.append(dict(booking_date=d, value_date=d, text="Uebertrag an Gesamtportfolio", counterparty=W.ORG,
                                     reference=f"Sweep {n['custodian_ref']}", transaction_ref="", amount=-chf, kind="sweep"))
            if facility_drawn > 0 and d >= date(2026, 10, 2) and d.day <= 6:
                bal -= facility_drawn
                rows.append(dict(booking_date=d, value_date=d, text="Rueckzahlung Standby-Fazilitaet", counterparty=W.BANK,
                                 reference="Standby facility 2026, repayment", transaction_ref="", amount=-facility_drawn, kind="facility"))
                facility_drawn = 0.0
            nxt = d + timedelta(days=1)
            if nxt.month != d.month:
                intr = round(bal * float(rng.uniform(0.0002, 0.0045)) / 12.0, 2)
                bal += intr
                rows.append(dict(booking_date=d, value_date=d, text="Zinsgutschrift" if intr >= 0 else "Zinsbelastung", counterparty=W.CUSTODIAN,
                                 reference=f"Zinsabschluss {d:%m/%Y}", transaction_ref="", amount=intr, kind="interest"))
                if d.month in (3, 6, 9, 12):
                    fee = -round(100_000_000 * W.COMMIT_FEE / 4.0, 2)
                    bal += fee
                    rows.append(dict(booking_date=d, value_date=d, text="Bereitstellungskommission", counterparty=W.BANK,
                                     reference=f"Standby facility {d.year}, commitment fee Q{(d.month - 1) // 3 + 1}", transaction_ref="", amount=fee, kind="fee"))
                    chg = -round(float(rng.uniform(1800, 4200)), 2)
                    bal += chg
                    rows.append(dict(booking_date=d, value_date=d, text="Depot- und Kontofuehrungsgebuehren", counterparty=W.CUSTODIAN,
                                     reference=f"Gebuehren Q{(d.month - 1) // 3 + 1} {d.year}", transaction_ref="", amount=chg, kind="charge"))
        d += timedelta(days=1)
    # booking dates: a few credits value-dated a day before they are booked; the sweep follows the booking
    for k, r in enumerate(rows):
        if r["kind"] == "dist" and rng.rand() < 0.12:
            r["booking_date"] = W.add_bdays(r["value_date"], 1)
            rows[k + 1]["booking_date"] = r["booking_date"]
    return rows
