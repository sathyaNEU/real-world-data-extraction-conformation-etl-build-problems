"""task232 estimators on the simulation's records: each condition's secondary transmission per child-hour of contact
under each way of counting a room's illnesses, the extra child-hours of contact each lateness setting adds per
notification, and each feed's setting."""
import math
from datetime import timedelta

import params as P
import world as W


def others(inv, d):
    return sum(1 for p in inv.roster.people if p is not inv.index and (p["pid"], d) in inv.att)


def contact_hours(inv):
    tot = 0.0
    for d in inv.inf_days:
        a, b = inv.att[(inv.index["pid"], d)]
        tot += (b - a) * others(inv, d)
    return tot


RUNGS = ["all", "before", "lower", "upper", "window"]


def keep(inv, rung, on):
    lo, hi = P.COND[inv.cond][1], P.COND[inv.cond][2]
    if rung == "all":
        return True
    if rung == "before":
        return inv.onset <= on <= inv.excl_date
    low_ok = (on - inv.first_inf).days >= lo
    up_ok = (on - inv.last_inf).days <= hi
    if rung == "lower":
        return low_ok
    if rung == "upper":
        return up_ok
    return low_ok and up_ok


def rates(invs, rung, confirmed_only=False):
    num = {c: 0 for c in P.COND_KEYS}
    den = {c: 0.0 for c in P.COND_KEYS}
    for inv in invs:
        if not inv.closed:
            continue
        den[inv.cond] += contact_hours(inv)
        for x in inv.cases:
            if confirmed_only and x["status"] != "confirmed":
                continue
            if keep(inv, rung, x["onset"]):
                num[inv.cond] += 1
    return {c: num[c] / den[c] for c in P.COND_KEYS}, num, den


def held(call, d, s, e):
    """Hours of a booked session [s, e] on day d that the case attends when the unit's call is at `call`: the whole
    session on days before the call's day, none on later days, and on the call's day none if the call comes before the
    session starts, else until an hour after the call."""
    cd = call.date()
    if d < cd:
        return e - s
    if d > cd:
        return 0.0
    ch = W.wall(call)
    if ch <= s:
        return 0.0
    return min(ch + P.LEAVE_AFTER, e) - s


def extra(inv, T):
    a = inv.auth
    c0 = W.call_time(a)
    cT = W.call_time(W.add_hours(a, T))
    idx = inv.index
    tot = 0.0
    d = c0.date()
    while d <= cT.date():
        if W.centre_open(inv.centre, d) and d.weekday() in idx["days"]:
            h = held(cT, d, idx["start"], idx["end"]) - held(c0, d, idx["start"], idx["end"])
            if h > 0:
                tot += h * others(inv, d)
        d += timedelta(days=1)
    return tot


def basis(invs):
    return [i for i in invs if P.BASIS_FROM <= i.auth.date() <= P.BASIS_TO]


def costs(invs, rate):
    out = {}
    B = basis(invs)
    for f in P.FEEDS:
        rs = [i for i in B if i.feed == f]
        out[f] = [sum(rate[i.cond] * extra(i, T) for i in rs) / 3.0 for T in P.SETTINGS]
    return out


def setting(curve):
    ok = [T for T, c in zip(P.SETTINGS, curve) if c <= P.TOLERANCE]
    return max(ok) if ok else None
