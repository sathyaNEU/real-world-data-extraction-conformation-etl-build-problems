"""The producing systems' records, derived from the simulated fund: settled custody positions at each custodian, the
custodians' statements and income reports, the corporate actions feed, and the golden figures of the asks."""
import datetime as dt

import numpy as np

import world as W
from world import D, DAYS, IDX

SWITCH = W.CUSTODY_SWITCH                    # Northcote's first day
Q_BOUNDS = [(D(2025, 10, 1), D(2025, 12, 31), "Q1"), (D(2026, 1, 1), D(2026, 3, 31), "Q2"),
            (D(2026, 4, 1), D(2026, 6, 30), "Q3"), (D(2026, 7, 1), D(2026, 9, 30), "Q4")]


def quarter(d):
    for a, b, q in Q_BOUNDS:
        if a <= d <= b:
            return q
    return None


def settled_positions(act):
    """settled holding per (day index, sleeve, sid): the trade-date holding less trades not yet settled"""
    trade_pos = {}
    for (i, tag, sid, q) in act["holdings"]:
        trade_pos[(i, tag, sid)] = q
    pending = {}
    for t in act["trades"]:
        if t["side"] in ("B", "S"):
            sgn = 1 if t["side"] == "B" else -1
            pending.setdefault((t["sleeve"], t["sid"]), []).append((t["day"], t["settle"], sgn * t["qty"]))
    out = {}
    by_day = {}
    for (i, tag, sid), q in trade_pos.items():
        by_day.setdefault(i, []).append((tag, sid, q))
    sids_seen = {}
    for i in range(len(DAYS)):
        d = DAYS[i]
        cur = {(tag, sid): q for tag, sid, q in by_day.get(i, [])}
        # names sold out today still have a settled holding until the sale settles
        for key, lst in pending.items():
            for td, sd, dq in lst:
                if td <= d < sd and key not in cur:
                    cur[key] = 0
        for (tag, sid), q in cur.items():
            unsettled = sum(dq for td, sd, dq in pending.get((tag, sid), []) if td <= d < sd)
            sq = q - unsettled
            if sq > 0:
                out[(i, tag, sid)] = sq
    return out


def scrip_offer(world, act):
    """issuers that offer a scrip alternative on every dividend: the two the sub-advisers elected, three of each
    sleeve's holdings that pay in the first half of the year, and a few the fund does not hold"""
    r = W.rng("scripoffer")
    out = {sid for (tag, sid, ex) in act["scrip"]}
    held = {"V": set(), "G": set()}
    for e in act["income"]:
        if D(2025, 10, 1) <= e["ex"] <= D(2026, 3, 31):
            held[e["sleeve"]].add(e["sid"])
    secmap = {s["sid"]: s for s in world["secs"]}
    for tag in ("V", "G"):
        pool = sorted(sid for sid in held[tag] if secmap[sid]["market"] == "Main Market" and sid != act["pen"]
                      and sid not in out)
        for k in r.choice(len(pool), size=3, replace=False):
            out.add(pool[int(k)])
    others = sorted(s["sid"] for s in world["secs"] if s["market"] == "Main Market" and s["sid"] != act["pen"]
                    and s["sid"] not in held["V"] | held["G"])
    for k in r.choice(len(others), size=5, replace=False):
        out.add(others[int(k)])
    return out


def entitlements(act):
    """every dividend entitlement the fund booked at an ex-date: sleeve, sid, ex, pay, shares, pence, gbp, paid"""
    pen = act["pen"]
    out = []
    for e in act["income"]:
        never = e["sid"] == pen and e["ex"] >= D(2026, 3, 1)
        out.append(dict(e, never_paid=never))
    return out


def income_golden(act):
    """A1: dividend income by sleeve and quarter of the accounting year, by ex-date, paid or still to be paid"""
    g = {}
    for e in entitlements(act):
        q = quarter(e["ex"])
        if q is None or e["never_paid"]:
            continue
        g[(e["sleeve"], q)] = g.get((e["sleeve"], q), 0.0) + e["gbp"]
    return g


def costs_golden(act):
    """A2: commission and stamp duty reserve tax by sleeve and quarter of the trade date"""
    g = {}
    for t in act["trades"]:
        if t["side"] not in ("B", "S"):
            continue
        q = quarter(t["day"])
        if q is None:
            continue
        g[(t["sleeve"], q)] = g.get((t["sleeve"], q), 0.0) + t["comm"] + t["sdrt"]
    return g


def aim_golden(world, act, settled):
    """A3: the growth sleeve's AIM holdings at each quarter-end, at the custodian's settled holdings and close prices"""
    secmap = {s["sid"]: s for s in world["secs"]}
    out = {}
    for a, b, q in Q_BOUNDS:
        i = IDX[b] if b in IDX else IDX[max(d for d in DAYS if d <= b)]
        d = DAYS[i]
        tot, aim, n = 0.0, 0.0, 0
        for (j, tag, sid), qty in settled.items():
            if j != i or tag != "G":
                continue
            px = world["closes"][sid][i]
            if sid == act["pen"] and d >= W.PENROSE_SUSPENDED:
                px = world["closes"][sid][IDX[D(2026, 3, 13)]]
            mv = round(qty * px / 100, 2)
            tot += mv
            if W.market_on(secmap[sid], d, world["moves"]) == "AIM":
                aim += mv
                n += 1
        out[q] = (n, aim / tot)
    return out
