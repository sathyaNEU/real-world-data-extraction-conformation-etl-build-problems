"""Billing's subscription records for the paying population: the subscriptions live at 30 September 2025 and every
subscription event from 1 October 2025 to 30 September 2026, as the billing platform exports them.

The paying accounts and the months they moved to Plus or cancelled come from the world. Billing adds what the platform
holds: the currency and billing interval, Team seats, the billing day, discounts, the April 2026 price list (applied at
each subscription's first renewal on or after 1 April), the cancellations a customer requests and the end of the period
already paid, the payments being retried, the customers that moved to business billing (a new customer record for the
same account) and the companies that put their staff's Plus subscriptions onto one Team subscription."""
import datetime as dt

import numpy as np

import params as P
import world as W

UTC = dt.timezone.utc
OPEN = dt.datetime(2025, 9, 30, 23, 0, tzinfo=UTC)       # midnight at the end of 30 September 2025, BST
CLOSE = dt.datetime(2026, 9, 30, 23, 0, tzinfo=UTC)
RISE = dt.datetime(2026, 4, 1, tzinfo=UTC)

CUR = ["GBP", "EUR", "USD"]
# Plus a month by currency: the list before 1 April 2026 and from it
PLUS_2025 = {"GBP": [18, 8, 26, 13, 6], "EUR": [21, 9, 30, 15, 7], "USD": [23, 10, 33, 17, 8]}
PLUS_2026 = {"GBP": [20, 8, 28, 13, 6], "EUR": [23, 9, 32, 15, 7], "USD": [25, 10, 35, 17, 8]}
FX = [("2024/25", "EUR", 1.1700), ("2024/25", "USD", 1.2600), ("2025/26", "EUR", 1.1600), ("2025/26", "USD", 1.2700),
      ("2026/27", "EUR", 1.1500), ("2026/27", "USD", 1.3300)]


def b36(n, width=10):
    s = ""
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    n = int(n)
    while n:
        n, r = divmod(n, 36)
        s = digits[r] + s
    return s.rjust(width, "0")[-width:]


def hid(x, slot):
    return int((W._mix(np.array([x * 1000003 + slot * 7919 + P.SEED], dtype=np.uint64)) >> np.uint64(12))[0])


def u(x, slot):
    return float(W.uni(np.array([x], dtype=np.int64), -5, slot)[0])


def acct(i):
    return "LK%07d" % (1000000 + int(i))


def price(app, cur, plan, interval, when):
    base = (PLUS_2026 if when >= RISE else PLUS_2025)[cur][app]
    if plan == "team":
        base = int(round(base * 1.5))
    return base * (10 if interval == "year" else 1)


def plan_code(app, plan, interval):
    return "%s-%s-%s" % (P.CODE[P.APPS[app]], "PLUS" if plan == "plus" else "TEAM", "Y" if interval == "year" else "M")


def month_start(m):
    return dt.datetime(2000 + m // 12, m % 12 + 1, 1, tzinfo=UTC)


def add_months(d, k):
    y, mo = d.year + (d.month - 1 + k) // 12, (d.month - 1 + k) % 12 + 1
    return d.replace(year=y, month=mo, day=min(d.day, 28))


def periods(start, interval):
    """the period boundaries from a start, monthly or yearly"""
    step = 12 if interval == "year" else 1
    k = 0
    while True:
        yield add_months(start, k)
        k += step


def first_after(start, interval, t):
    """the first period boundary strictly after t"""
    step = 12 if interval == "year" else 1
    n = (t.year - start.year) * 12 + (t.month - start.month)
    n = max(0, n - n % step)
    b = add_months(start, n)
    while b <= t:
        b = add_months(b, step)
    return b


def prev_boundary(start, interval, b):
    step = 12 if interval == "year" else 1
    p = add_months(b, -step)
    return p if p >= start else start


class Sub:
    __slots__ = ("sid", "cus", "acc", "app", "plan", "interval", "cur", "seats", "unit", "disc", "disc_end", "start",
                 "status", "end", "cancel_req")

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))


def build(world):
    """the opening list (as it stood at 30 September 2025) and the year's events, as rows"""
    paid_at, spells = world["paid_at"], world["spells"]
    opening, ev, companies = [], [], []
    nsub = [0]

    def new_sid(x, k):
        nsub[0] += 1
        return "sub_" + b36(hid(x, 50 + k) ^ (nsub[0] * 2654435761), 14)

    def attrs(x):
        c = CUR[0 if u(x, 1) < 0.70 else (1 if u(x, 1) < 0.88 else 2)]
        team = u(x, 3) < 0.09
        return dict(cur=c, interval="year" if u(x, 2) < 0.26 else "month", plan="team" if team else "plus",
                    seats=(3 + int(u(x, 4) * 10)) if team else 1, day=1 + int(u(x, 5) * 28))

    def start_time(m, day, x):
        return month_start(m).replace(day=day, hour=7 + int(u(x, 7) * 15), minute=int(u(x, 8) * 60),
                                      second=int(u(x, 9) * 60))

    def row(s, t, kind, **over):
        r = dict(t=t, kind=kind, sid=s.sid, cus=s.cus, acc=s.acc, app=s.app, plan=s.plan, interval=s.interval,
                 cur=s.cur, seats=s.seats, unit=s.unit, disc=s.disc, disc_end=s.disc_end if s.disc else None,
                 status=s.status, start=s.start)
        r.update(over)
        return r

    # the opening list: every subscription live at the end of 30 September 2025
    live = {}
    for x, (app, since) in sorted(paid_at.items()):
        a = attrs(x)
        st = start_time(max(since, P.LAUNCH[app]), a["day"], x)
        disc, dend = 0, None
        if since < 300 and u(x, 6) < 0.06:
            disc, dend = 20, add_months(st, 24)
        live[x] = Sub(sid=new_sid(x, 0), cus="cus_" + b36(hid(x, 1), 12), acc=acct(x), app=app, plan=a["plan"],
                      interval=a["interval"], cur=a["cur"], seats=a["seats"],
                      unit=price(app, a["cur"], a["plan"], a["interval"], OPEN), disc=disc, disc_end=dend, start=st,
                      status="past_due" if u(x, 10) < 0.015 else "active", end=None, cancel_req=None)
    # companies: one customer record paying for several staff accounts' Plus subscriptions in one app
    by_app = {}
    for x, s in live.items():
        if s.plan == "plus" and s.cur == "GBP" and u(x, 11) < 0.05:
            by_app.setdefault(s.app, []).append(x)
    for app in sorted(by_app):
        xs, k = by_app[app], 0
        while k + 1 < len(xs):
            grp = xs[k:k + 2 + int(u(xs[k], 12) * 4)]
            if len(grp) < 2:
                break
            for x in grp:
                live[x].cus = "cus_" + b36(hid(grp[0], 2), 12)
            companies.append(grp)
            k += len(grp)
    for x in sorted(live):
        s = live[x]
        opening.append(row(s, OPEN, "open"))
    # the account's cancellation request, from the month its owner stopped paying
    req = {}
    for (x, app, m, what) in spells:
        if what == "end":
            req[x] = month_start(m) + dt.timedelta(days=int(u(x, 14) * 27), hours=8 + int(u(x, 15) * 12),
                                                   minutes=int(u(x, 16) * 60))
    # new subscriptions in the window
    timeline = [(x, live[x]) for x in sorted(live)]
    for (x, app, m, what) in sorted(spells):
        if what != "start" or x in live:
            continue
        a = attrs(x)
        st = start_time(m, a["day"], x)
        disc = 50 if (0.06 <= u(x, 6) < 0.11 and a["interval"] == "month") else 0
        s = Sub(sid=new_sid(x, 1), cus="cus_" + b36(hid(x, 1), 12), acc=acct(x), app=app, plan=a["plan"],
                interval=a["interval"], cur=a["cur"], seats=a["seats"], unit=price(app, a["cur"], a["plan"], a["interval"], st),
                disc=disc, disc_end=add_months(st, 3) if disc else None, start=st, status="active", end=None,
                cancel_req=None)
        live[x] = s
        ev.append(row(s, st, "created"))
        timeline.append((x, s))
    # the companies that move their staff onto one Team subscription
    for g in companies:
        if u(g[0], 13) >= 0.45:
            continue
        tc = OPEN + dt.timedelta(days=40 + int(u(g[0], 17) * 300), hours=10, minutes=int(u(g[0], 22) * 60))
        members = [live[y] for y in g if y not in req or req[y] > tc]
        if len(members) < 2:
            continue
        for sm in members:
            sm.end = tc
        admin = members[0]
        admin_acc = acct(1200000 + int(u(g[0], 25) * 600000))     # the company administrator's own account
        team = Sub(sid=new_sid(g[0], 7), cus=admin.cus, acc=admin_acc, app=admin.app, plan="team", interval="month",
                   cur="GBP", seats=len(members) + int(u(g[0], 18) * 3), unit=price(admin.app, "GBP", "team", "month", tc),
                   disc=0, disc_end=None, start=tc, status="active", end=None, cancel_req=None)
        team.cancel_req = "company"
        timeline.append((("team", g[0]), team))
    # a payment that fails until the platform ends the subscription, and the owner subscribing again the same day,
    # which the platform opens under a new customer record
    moved, failed = {}, {}
    company_member = {x for g in companies for x in g}
    for x, s in list(timeline):
        if isinstance(x, tuple) or s.end is not None or x in company_member or u(x, 19) >= 0.04:
            continue
        bf = first_after(s.start, s.interval, max(s.start, OPEN) + dt.timedelta(days=10 + int(u(x, 20) * 320)))
        tb = bf + dt.timedelta(days=14, hours=6, minutes=int(u(x, 23) * 60))
        if tb >= CLOSE or (x in req and req[x] <= tb + dt.timedelta(days=1)):
            continue
        s.end = tb
        failed[x] = bf
        iv = "year" if u(x, 21) < 0.4 else s.interval
        t_new = tb + dt.timedelta(hours=2 + int(u(x, 26) * 9), minutes=int(u(x, 27) * 60))
        ns = Sub(sid=new_sid(x, 2), cus="cus_" + b36(hid(x, 2), 12), acc=s.acc, app=s.app, plan=s.plan, interval=iv,
                 cur=s.cur, seats=s.seats, unit=price(s.app, s.cur, s.plan, iv, t_new), disc=0, disc_end=None,
                 start=t_new, status="active", end=None, cancel_req=None)
        if t_new >= CLOSE:
            continue
        moved[x] = ns
    timeline += [(x, ns) for x, ns in moved.items()]
    # each subscription's year: renewals, the April price list, discount ends, plan changes, then its end
    for x, s in timeline:
        if (isinstance(x, tuple) and s.cancel_req == "company") or (x in moved and moved[x] is s):
            ev.append(row(s, s.start, "created"))
        own_req = req.get(x) if not isinstance(x, tuple) else None
        if own_req is not None and x in moved and moved[x] is not s:
            own_req = None                                   # the request falls on the account's new subscription
        stop = s.end if s.end is not None else CLOSE
        if x in failed and moved.get(x) is not s and not isinstance(x, tuple):
            stop = failed[x] - dt.timedelta(seconds=1)       # the renewal charge at this boundary fails
        b = first_after(s.start, s.interval, max(OPEN, s.start))
        last = prev_boundary(s.start, s.interval, b)
        while b <= stop and b <= CLOSE and (own_req is None or b <= own_req):
            changed = False
            if s.disc and s.disc_end is not None and s.disc_end <= b:
                s.disc, s.disc_end, changed = 0, None, True
            newp = price(s.app, s.cur, s.plan, s.interval, b)
            if newp != s.unit:
                s.unit, changed = newp, True
            k = b.year * 12 + b.month
            key = x if not isinstance(x, tuple) else x[1] + 7
            nxt_interval = s.interval
            if s.plan == "team" and u(key, 200 + k % 97) < 0.03:
                s.seats = max(2, s.seats + (1 if u(key, 300 + k % 89) < 0.6 else -1) * (1 + int(u(key, 400 + k % 83) * 2)))
                changed = True
            elif s.plan == "plus" and s.interval == "month" and u(key, 500 + k % 79) < 0.004:
                nxt_interval, s.unit, changed = "year", price(s.app, s.cur, s.plan, "year", b), True
            elif s.plan == "plus" and u(key, 600 + k % 73) < 0.0012:
                s.plan, s.seats = "team", 3 + int(u(key, 700 + k % 71) * 4)
                s.unit, changed = price(s.app, s.cur, "team", s.interval, b), True
            if s.status == "past_due":
                s.status, changed = "active", True
            was_year = s.interval == "year"
            s.interval = nxt_interval
            if was_year:
                ev.append(row(s, b, "renewed"))
            elif changed:
                ev.append(row(s, b, "updated"))
            last = b
            b = add_months(b, 12 if s.interval == "year" else 1)
        if s.end is not None and s.end <= CLOSE and x in failed and moved.get(x) is not s and not isinstance(x, tuple):
            s.status = "past_due"
            ev.append(row(s, failed[x], "updated"))
            ev.append(row(s, s.end, "ended", status="canceled"))
        elif s.end is not None and s.end <= CLOSE:
            ev.append(row(s, s.end, "cancelled"))
            ev.append(row(s, s.end, "ended", status="canceled"))
        elif own_req is not None and own_req < CLOSE:
            ev.append(row(s, own_req, "cancelled"))
            pe = add_months(last, 12 if s.interval == "year" else 1)
            while pe <= own_req:
                pe = add_months(pe, 12 if s.interval == "year" else 1)
            if pe <= CLOSE:
                ev.append(row(s, pe, "ended", status="canceled"))
    order = ["created", "renewed", "updated", "cancelled", "ended"]
    ev.sort(key=lambda r: (r["t"], r["sid"], order.index(r["kind"])))
    return opening, ev, companies


def iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")
