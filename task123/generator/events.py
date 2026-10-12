"""Service events at each premise through the winter: seasonal turn-offs at lake cottages, nonpayment shutoffs
and their reconnections, customer and safety shutoffs, and low-income payment plan enrolments.

Events are drawn per premise from its own stream, before daily use is simulated, because a shut-off premise
uses no gas: the bills and the AMI reads carry every shutoff's nil days.

Shutoff policy in the world: every utility paused nonpayment shutoffs for the cold snap, 19 to 30 January
2026; Kestrel Valley's collections shutoffs from 5 to 16 January were worked by a contractor, Northline
Utility Services; Pine Harbor shuts off its AMI meters' valves from the head end.
"""
from datetime import timedelta

import world as W

D = W.D
TD = timedelta
PAUSE_FROM, PAUSE_TO = D(2026, 1, 19), D(2026, 1, 30)
CONTRACTOR_FROM, CONTRACTOR_TO = D(2026, 1, 5), D(2026, 1, 16)
SEASONAL_SHARE = {"Ashwell": 0.05, "Evanshade": 0.04, "Carrow": 0.03, "Farrish": 0.04, "Keswin": 0.03,
                  "Merrion": 0.04}
NP_RATE = {12: 0.0048, 1: 0.0045, 2: 0.0042}      # nonpayment shutoffs per account per month
LIPP_RATE = 0.072


def bday_on_or_after(d):
    while d.weekday() >= 5 or d in (D(2025, 12, 25), D(2025, 12, 26), D(2026, 1, 1)):
        d += TD(1)
    return d


def next_bday(d, n=1):
    for _ in range(n):
        d = bday_on_or_after(d + TD(1))
    return d


def draw(p):
    """Return the premise's events (dicts) and its nil-use spans [(first gas day, last gas day)]."""
    r = W.rng("events", p.pid)
    ev, nil = [], []
    # lake cottages turned off for the winter
    seasonal = r.random() < SEASONAL_SHARE.get(p.county, 0.0) and not p.ami
    if seasonal:
        off = bday_on_or_after(D(2025, 10, 13) + TD(int(r.integers(0, 35))))
        on = bday_on_or_after(D(2026, 4, 20) + TD(int(r.integers(0, 28))))
        ev.append(dict(kind="SEASONAL_OFF", date=off))
        ev.append(dict(kind="SEASONAL_ON", date=on))
        nil.append((off + TD(1), on))
    # low-income payment plan enrolment of each account (winter protection: enrolees are not shut off)
    lipp = {}
    for a, s, e in p.accounts:
        if r.random() < LIPP_RATE and not seasonal:
            start = max(s, D(2024, 6, 1)) + TD(int(r.integers(0, 420)))
            if e is not None and start > e:
                continue
            lipp[a] = start
            ev.append(dict(kind="LIPP", account=a, date=start, end=e))
    # nonpayment shutoffs, month by month, on business days outside the cold-snap pause
    for (y, m), rate in ((2025, 12), NP_RATE[12]), ((2026, 1), NP_RATE[1]), ((2026, 2), NP_RATE[2]):
        if seasonal:
            continue
        if r.random() < rate:
            day = bday_on_or_after(D(y, m, 1) + TD(int(r.integers(0, 27))))
            acct = None
            for a, s, e in p.accounts:
                if s <= day and (e is None or day <= e):
                    acct = a
            if acct is None or (acct in lipp and lipp[acct] <= day):
                continue
            ev.append(dict(kind="NP_DUE", account=acct, date=day))
    out = []
    for x in ev:
        if x["kind"] != "NP_DUE":
            out.append(x)
            continue
        due = x["date"]
        # the attempt: some cannot be completed (no access), retried two to six business days later
        attempts = []
        d = due
        if r.random() < 0.13:
            attempts.append(("UNABLE", d))
            d = next_bday(d, int(r.integers(2, 7)))
        sched = d
        comp = d
        if PAUSE_FROM <= sched <= PAUSE_TO:
            comp = bday_on_or_after(D(2026, 2, 2) + TD(int(r.integers(0, 5))))
        elif D(2025, 12, 29) <= sched <= D(2025, 12, 31) and r.random() < 0.55:
            comp = bday_on_or_after(D(2026, 1, 2) + TD(int(r.integers(0, 4))))
        elif r.random() < 0.12:
            comp = next_bday(sched, int(r.integers(1, 3)))
        if comp > W.SIM_END:
            continue
        # a shutoff whose account ends before it is never worked
        attempts.append(("DONE", comp))
        recon = None
        if r.random() < 0.72:
            recon = next_bday(comp, int(r.integers(1, 11)))
        out.append(dict(kind="NP", account=x["account"], due=due, sched=sched, date=comp, attempts=attempts,
                        recon=recon))
        nil.append((comp + TD(1), recon if recon else W.SIM_END))
    # customer-request, safety and move-out shutoffs in December to February (no nil use modelled for the
    # short safety closes; customer and move-out closes end the account's use until the next account)
    if not seasonal and r.random() < 0.012:
        day = bday_on_or_after(D(2025, 12, 1) + TD(int(r.integers(0, 85))))
        kind = ["CUST_OFF", "SAFETY_OFF", "SAFETY_OFF"][int(r.integers(0, 3))]
        recon = next_bday(day, int(r.integers(0, 3)))
        out.append(dict(kind=kind, date=day, recon=recon))
        if recon > day:
            nil.append((day + TD(1), recon))
    return out, nil


def close_unpaid(p, events):
    """A nonpayment shutoff not reconnected within ten business days closes the account (a final read on the
    closing day) and the premise stays vacant through the winter: the account ends there, later accounts and
    every later event at the premise are dropped."""
    first = None
    for x in events:
        if x["kind"] == "NP" and x["recon"] is None and (first is None or x["date"] < first["date"]):
            first = x
    if first is None:
        p.closed = None
        return events
    closure = next_bday(first["date"], 10)
    p.closed = closure if closure <= W.SIM_END else None
    if p.closed is None:
        return events
    first["closed"] = closure
    acc = []
    for a, s, e in p.accounts:
        if s > first["date"]:
            break
        acc.append([a, s, closure if (e is None or e > closure) else e])
    p.accounts = acc
    keep = []
    for x in events:
        if x is first:
            keep.append(x)
        elif x["kind"] == "LIPP":
            if x["date"] <= closure:
                keep.append(x)
        elif x["date"] <= first["date"]:
            keep.append(x)
    return keep


def apply_nil(U_row, nil):
    for a, b in nil:
        if b < W.SIM_START or a > W.SIM_END:
            continue
        ia, ib = W.IDX[max(a, W.SIM_START)], W.IDX[min(b, W.SIM_END)]
        U_row[ia:ib + 1] = 0.0
    return U_row
