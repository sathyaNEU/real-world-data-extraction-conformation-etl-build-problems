"""The asks' records and their goldens: Tollard's plant changes in the window (node splits, one of them registered
by both of Tollard's systems, and class upgrades), its month-end subscriber counts, and its outage reports (an
outage worked by the field team and the network operations centre filed under two tickets); then, from the pack,
each hub's outage credits (Ask A) and each hub's downstream capacity (Ask B), with the stops a careful solver files.
None of these rows is a panel household's, a panel node's evening, or a test."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K
import records as R

MONTH_ENDS = (dt.date(2026, 7, 31), dt.date(2026, 8, 31), dt.date(2026, 9, 30), dt.date(2026, 10, 31))
DESIGNATED_2025 = ("EH", "SC")
CAP_FROM = K.WINDOW_START
CAP_TO = K.WINDOW_END


class Plant:
    def __init__(self, rc):
        self.rc = rc
        rng = self.rng = np.random.default_rng(rc.seed * 7919 + 43)
        reg = rc.register
        panel = set(rc.node_id)
        live = [r for r in reg if r[5] is None and r[0] not in panel and r[4] < dt.date(2026, 6, 1)]
        by_hub = {}
        for r in live:
            by_hub.setdefault(r[1], []).append(r)
        nxt = {h: 1 + max(int(r[0][3:]) for r in reg if r[1] == h) for h in K.HUB}
        self.window_splits = []                    # (parent, children, date, registered twice)
        self.remedy = []                           # the 2025 designations' works: (hub, node, work, date, Mbit/s)
        self.upgrades = []                          # (node, old class, new class, date)
        changed = set()
        twice_hubs = list(K.HUB)                    # each hub has one split both systems registered
        for h in K.HUB:
            pool = [r for r in by_hub[h] if r[2] != "D31"]
            n_split = int(rng.integers(1, 3)) + (1 if h in twice_hubs else 0)
            for k in range(n_split):
                r = pool.pop(int(rng.integers(0, len(pool))))
                twice = (h in twice_hubs) and k == 0
                last = 36 if twice else K.DAYS - 5
                on = K.WINDOW_START + dt.timedelta(days=int(rng.integers(5, last)))
                r[5] = on - dt.timedelta(days=1)
                kids = []
                cls = "D31" if rng.uniform() < 0.35 else r[2]
                three = (k > 0) and rng.uniform() < 0.35   # a genuine three-way split, beside the twice-registered ones
                for c in range(3 if three else 2):
                    nid = "%s-%03d" % (h, nxt[h])
                    nxt[h] += 1
                    reg.append([nid, h, cls, K.NODE_CLASSES[cls][1], on, None, r[0]])
                    kids.append(nid)
                ghost = []
                if twice:
                    # the field system's record of the same two new nodes, under its own numbers and a day later
                    for c in range(2):
                        nid = "%s-%03d" % (h, nxt[h] + 7 + c)
                        reg.append([nid, h, cls, K.NODE_CLASSES[cls][1], on + dt.timedelta(days=1), None, r[0]])
                        ghost.append(nid)
                    nxt[h] += 9
                self.window_splits.append((r[0], tuple(kids), on, tuple(ghost)))
                changed.add(r[0])
            for k in range(int(rng.integers(1, 3))):
                cand = [r for r in by_hub[h] if r[0] not in changed and r[2] == "D30-32" and r[5] is None]
                r = cand[int(rng.integers(0, len(cand)))]
                on = K.WINDOW_START + dt.timedelta(days=int(rng.integers(3, K.DAYS - 3)))
                r[5] = on - dt.timedelta(days=1)
                reg.append([r[0], h, "D31", K.NODE_CLASSES["D31"][1], on, None, ""])
                self.upgrades.append((r[0], "D30-32", "D31", on))
                changed.add(r[0])
            # the 2025 remedy: in the two hubs designated in December 2025, nodes split or upgraded in 2026
            if h in DESIGNATED_2025:
                for k in range(3):
                    cand = [r for r in by_hub[h] if r[0] not in changed and r[2] == "D30-32" and r[5] is None]
                    r = cand[int(rng.integers(0, len(cand)))]
                    on = dt.date(2026, int(rng.integers(3, 9)), int(rng.integers(1, 28)))
                    r[5] = on - dt.timedelta(days=1)
                    if k == 0:
                        kids = []
                        for c in range(2):
                            nid = "%s-%03d" % (h, nxt[h])
                            nxt[h] += 1
                            reg.append([nid, h, "D30-32", K.NODE_CLASSES["D30-32"][1], on, None, r[0]])
                            kids.append(nid)
                        self.remedy.append((h, r[0], "split into %s and %s" % tuple(kids), on,
                                            2 * K.NODE_CLASSES["D30-32"][1] - K.NODE_CLASSES["D30-32"][1]))
                    else:
                        reg.append([r[0], h, "D31", K.NODE_CLASSES["D31"][1], on, None, ""])
                        self.remedy.append((h, r[0], "upgraded to DOCSIS 3.1", on,
                                            K.NODE_CLASSES["D31"][1] - K.NODE_CLASSES["D30-32"][1]))
                    changed.add(r[0])
            # nodes built for new subdivisions: in service with no subscribers yet at the end of October
            for k in range(int(rng.integers(0, 2))):
                nid = "%s-%03d" % (h, nxt[h])
                nxt[h] += 1
                on = K.WINDOW_START + dt.timedelta(days=int(rng.integers(20, K.DAYS - 2)))
                reg.append([nid, h, "D31", K.NODE_CLASSES["D31"][1], on, None, ""])
        reg.sort(key=lambda r: (r[0][:2], int(r[0][3:]), r[4]))
        self.ghosts = {g for s in self.window_splits for g in s[3]}

        # month-end subscriber counts (the ghost records carry none: they are not nodes)
        self.subs = {}
        base = {}
        for r in reg:
            if r[0] in self.ghosts:
                continue
            if r[0] not in base:
                base[r[0]] = int(rng.integers(120, 270))
        kid_of = {k: s for s in self.window_splits for k in s[1]}
        for me in MONTH_ENDS:
            for r in reg:
                n = r[0]
                if n in self.ghosts or not (r[4] <= me and (r[5] is None or me <= r[5])):
                    continue
                if n in kid_of:
                    parent = kid_of[n][0]
                    v = int(base[parent] / len(kid_of[n][1]) * rng.uniform(0.9, 1.1))
                elif r[4] > dt.date(2026, 9, 1) and r[6] == "" and n not in {u[0] for u in self.upgrades}:
                    v = 0
                else:
                    v = int(base[n] * (1 + 0.004 * MONTH_ENDS.index(me)) + rng.integers(-3, 4))
                self.subs[(n, me)] = max(v, 0)

        # outages: tickets per node in service, planned work at night, unplanned at any hour
        self.tickets = []                           # ticket, node, start_utc, end_utc, kind, cause
        self.dual = []                              # (node, field ticket, noc ticket)
        # each node's own service span (an upgraded node's two rows are one span); outages fall inside it
        span_of = {}
        for r in reg:
            if r[0] in self.ghosts or r[0] in kid_of or r[4] >= dt.date(2026, 7, 1):
                continue
            lo, hi = span_of.get(r[0], (r[4], r[5]))
            lo = min(lo, r[4])
            hi = None if (hi is None or r[5] is None) else max(hi, r[5])
            span_of[r[0]] = (lo, hi)
        tid = iter(rng.permutation(np.arange(410000, 499999)))
        start0 = dt.datetime.combine(K.WINDOW_START - dt.timedelta(days=4), dt.time(0))
        end0 = dt.datetime.combine(K.WINDOW_END + dt.timedelta(days=4), dt.time(0))
        node_ids = sorted(n for n, (lo, hi) in span_of.items() if hi is None or hi >= K.WINDOW_START)
        for n in node_ids:
            hi = span_of[n][1]
            last = min(end0, dt.datetime.combine(hi, dt.time(0))) if hi is not None else end0
            hours_avail = (last - start0).total_seconds() / 3600
            k = rng.poisson(0.55 * hours_avail / ((K.DAYS + 8) * 24))
            for _ in range(k):
                kind = "Planned" if rng.uniform() < 0.25 else "Unplanned"
                for attempt in range(40):
                    if kind == "Planned":
                        day = start0 + dt.timedelta(days=int(rng.integers(0, max(1, int(hours_avail // 24)))))
                        loc = day + dt.timedelta(hours=float(rng.uniform(0.0, 2.0)))
                        hours = float(rng.uniform(2.0, 5.5))
                    else:
                        loc = start0 + dt.timedelta(hours=float(rng.uniform(0, hours_avail)))
                        hours = float(np.clip(rng.lognormal(math.log(3.2), 0.7), 0.4, 60.0))
                    end_loc = loc + dt.timedelta(hours=hours)
                    if hi is not None and end_loc >= dt.datetime.combine(hi + dt.timedelta(days=1), dt.time(0)):
                        continue
                    if n in panel and _evening_overlap(loc, end_loc):
                        continue
                    break
                else:
                    continue
                cause = rng.choice(["POWER", "FIBER", "AMP", "NODE", "WEATHER"] if kind == "Unplanned"
                                   else ["MAINT"])
                t = "TT-%06d" % next(tid)
                s_utc, e_utc = K.to_utc(loc.replace(microsecond=0)), K.to_utc(end_loc.replace(microsecond=0))
                s_utc = s_utc.replace(second=0)
                e_utc = e_utc.replace(second=0)
                members = [n]
                if kind == "Unplanned" and rng.uniform() < 0.15:
                    same_hub = [m for m in node_ids if m[:2] == n[:2] and m != n and m not in panel
                                and (span_of[m][1] is None or end_loc.date() < span_of[m][1])]
                    members += list(rng.choice(same_hub, int(rng.integers(1, 4)), replace=False))
                for m in members:
                    self.tickets.append([t, str(m), s_utc, e_utc, kind, str(cause)])
        # one outage worked by the field team and the operations centre, each filing its own ticket
        cands = [i for i, x in enumerate(self.tickets) if x[4] == "Unplanned" and x[1] not in panel
                 and (x[3] - x[2]).total_seconds() >= 4.5 * 3600 and _in_window(x[2])]
        seen_t = set()
        picks = []
        for h in K.HUB:                            # every hub's figure carries one, and five more fall at random
            mine = [i for i in rng.permutation(cands) if self.tickets[i][1][:2] == h and self.tickets[i][0] not in seen_t]
            if mine:
                seen_t.add(self.tickets[mine[0]][0])
                picks.append(int(mine[0]))
        for i in rng.permutation(cands):
            if len(picks) >= 13:
                break
            if self.tickets[i][0] in seen_t:
                continue
            seen_t.add(self.tickets[i][0])
            picks.append(int(i))
        for i in picks:
            t0, n, s, e, kind, cause = self.tickets[i]
            noc = "TT-%06d" % next(tid)
            ds = dt.timedelta(minutes=int(rng.integers(6, 41)))
            de = dt.timedelta(minutes=int(rng.integers(-15, 16)))
            for x in [x for x in self.tickets if x[0] == t0]:
                self.tickets.append([noc, x[1], s + ds, e + de, kind, cause])
            self.dual.append((n, t0, noc))
        self.tickets.sort(key=lambda x: (x[2], x[0], x[1]))

    def register_rows(self):
        return self.rc.register_rows()

    def subcount_table(self):
        nodes = sorted({n for n, me in self.subs}, key=lambda n: (n[:2], int(n[3:])))
        rows = []
        for n in nodes:
            rows.append([n, n[:2]] + [self.subs.get((n, me), None) for me in MONTH_ENDS])
        return (["node_id", "hub_code"] + ["subscribers_%s" % me.isoformat() for me in MONTH_ENDS], rows)

    def outage_rows(self):
        return (["ticket_id", "node_id", "outage_start_utc", "service_restored_utc", "work_type", "cause_code"],
                [[t, n, s.strftime("%Y-%m-%d %H:%M"), e.strftime("%Y-%m-%d %H:%M"), k, c]
                 for t, n, s, e, k, c in self.tickets])


def _evening_overlap(a, b):
    """True when [a, b) (local) touches 4 pm to 1 am on any evening"""
    d = a.date() - dt.timedelta(days=1)
    while dt.datetime.combine(d, dt.time(0)) <= b:
        lo = dt.datetime.combine(d, dt.time(16))
        hi = lo + dt.timedelta(hours=9)
        if a < hi and lo < b:
            return True
        d += dt.timedelta(days=1)
    return False


def _in_window(utc):
    return K.WINDOW_START <= K.to_local(utc).date() <= K.WINDOW_END


# ------------------------------------------------------------------------------------------------ goldens from the pack
def _register(target):
    from pack import rows, date
    return [(r["node_id"], r["hub_code"], r["node_class"], int(r["ds_capacity_mbps"]), date(r["in_service_from"]),
             date(r["in_service_to"]), r["split_from"]) for r in rows(target, "nodes")]


def _counts(target):
    import openpyxl
    from pack import path
    wb = openpyxl.load_workbook(path(target, "subcounts"), read_only=True)
    ws = wb.worksheets[0]
    it = ws.iter_rows(values_only=True)
    head = next(it)
    mes = [dt.date.fromisoformat(h.split("_")[1]) for h in head[2:]]
    subs = {}
    for r in it:
        for me, v in zip(mes, r[2:]):
            if v not in (None, ""):
                subs[(r[0], me)] = int(v)
    return subs


def capacity(target, day, drop_ghosts=True, first_row_only=False):
    """each hub's downstream capacity in service on a day (Mbit/s)"""
    reg = _register(target)
    ghosts = set()
    if drop_ghosts:
        # a split makes two new nodes or three; children of one parent beyond the ones carrying subscribers in the
        # month-end counts and in service a day after their siblings are the second system's record of them
        counted = {n for n, me in _counts(target)}
        kids = {}
        for n, h, c, cap, a, b, parent in reg:
            if parent:
                kids.setdefault(parent, []).append((a, n))
        for parent, ks in kids.items():
            first = min(a for a, n in ks)
            for a, n in ks:
                if a > first and n not in counted:
                    ghosts.add(n)
    out = {h: 0 for h in K.HUB}
    seen = set()
    for n, h, c, cap, a, b, parent in reg:
        if n in ghosts:
            continue
        if first_row_only:
            # one row a node, the first the register lists, read as the node
            if n in seen:
                continue
            seen.add(n)
            if a <= day and (b is None or day <= b or n in upgraded(reg)):
                out[h] += cap
            continue
        if a <= day and (b is None or day <= b):
            out[h] += cap
    return out


def capacity_added(target, **kw):
    a, b = capacity(target, CAP_FROM, **kw), capacity(target, CAP_TO, **kw)
    return {h: b[h] - a[h] for h in K.HUB}


def new_rows_only(target):
    """capacity added read as the capacity of the register's rows that came into service in the window"""
    out = {h: 0 for h in K.HUB}
    for n, h, c, cap, a, b, parent in _register(target):
        if CAP_FROM < a <= CAP_TO:
            out[h] += cap
    return out


def upgraded(reg):
    ids = [r[0] for r in reg]
    return {n for n in ids if ids.count(n) > 1}


def credits(target, merge=True, dedupe_ticket=False, local_window=True, planned=False, count_month="before"):
    """each hub's subscriber-days of credit for the unplanned outages that began in the window"""
    from pack import rows
    subs = _counts(target)
    hub_of = {n: h for n, h, *_ in _register(target)}
    by_node = {}
    seen = set()
    for r in rows(target, "outages"):
        if r["work_type"] != "Unplanned" and not planned:
            continue
        if dedupe_ticket:
            if r["ticket_id"] in seen:
                continue
            seen.add(r["ticket_id"])
        s = dt.datetime.strptime(r["outage_start_utc"], "%Y-%m-%d %H:%M")
        e = dt.datetime.strptime(r["service_restored_utc"], "%Y-%m-%d %H:%M")
        by_node.setdefault(r["node_id"], []).append([s, e])
    out = {h: 0 for h in K.HUB}
    for n, iv in by_node.items():
        iv.sort()
        if merge:
            m = [iv[0][:]]
            for s, e in iv[1:]:
                if s <= m[-1][1]:
                    m[-1][1] = max(m[-1][1], e)
                else:
                    m.append([s, e])
            iv = m
        for s, e in iv:
            began = K.to_local(s).date() if local_window else s.date()
            if not (K.WINDOW_START <= began <= K.WINDOW_END):
                continue
            hours = (e - s).total_seconds() / 3600
            if hours < 4:
                continue
            days = math.ceil(hours / 24 - 1e-12)
            if count_month == "before":
                me = dt.date(began.year, began.month, 1) - dt.timedelta(days=1)
            else:
                nm = dt.date(began.year + (began.month == 12), began.month % 12 + 1, 1)
                me = nm - dt.timedelta(days=1)
            out[hub_of[n]] += days * subs[(n, me)]
    return out
