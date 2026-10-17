"""The two asks, computed from the shipped bundle: last Christmas's call-ins by store (the hours of the shifts each
store put out to call-in for the four trading weeks to Christmas Eve 2025, and how many of those hours call-ins
covered and left uncovered), and cover across stores in those weeks (each store's call-in hours covered by casuals
from other stores, and the hours its own casuals covered at other stores). Each wrong path the ask sheet names is
computed beside the golden."""
from __future__ import annotations

import collections
import datetime as dt

import calc as C

WINDOW = (dt.date(2025, 11, 28), dt.date(2025, 12, 24))
PUBLISHED_25 = "2025-11-12T23:00:00Z"       # 10:00 on Thursday 13 November 2025, store time (AEDT)


def _reg(B):
    out = []
    for r in B.register:
        s0 = C.utc_to_local_min(r["shift_start_utc"])
        e0 = C.utc_to_local_min(r["shift_end_utc"])
        day = int(s0 // 1440)
        d = C.D0 + dt.timedelta(days=day)
        utc_d = dt.date.fromisoformat(r["shift_start_utc"][:10])
        out.append(dict(r=r, loc=r["location_id"], day=day, d=d, utc_d=utc_d, s=int(round(s0 - day * 1440)),
                        e=int(round(e0 - day * 1440)), span=e0 - s0, raised=C.utc_to_local_min(r["raised_at"]),
                        closed=C.utc_to_local_min(r["closed_at"]), reason=r["reason"], absent=r["absent_payroll_no"],
                        outcome=r["outcome"], by=r["filled_by"]))
    return out


def shifts(B, use_utc=False, span_hours=False, dedup=None, drops=True, window=None, opn=True, dayvoid=False,
           keepfill=False):
    """the shifts put out to call-in in the window, each with its final outcome:
    dedup None: postings grouped into shifts (re-raises and re-raises after a drop belong to their shift, an absence
    reported twice is one vacated line, the identical open lines a roster lists are each a shift);
    dedup 'rows': every register row a shift; dedup 'noninstant': every row a shift but those closed the minute they
    were raised; dedup 'keys': rows collapsed on store, date, times, reason, absent;
    dedup 'keysdrops': the same collapse with give-backs voided (the cracker's route);
    dedup 'raise': every call-in not raised as a re-raise at 07:00 a shift (a second report of an absence too);
    opn False: open lines left out; dayvoid: a fill voided by any absence its casual reported that day;
    keepfill: a given-back shift counted once but its first fill kept as the cover."""
    win = window or WINDOW
    rows = [x for x in _reg(B) if win[0] <= (x["utc_d"] if use_utc else x["d"]) <= win[1]]
    hours = (lambda x: x["span"] / 60.0) if span_hours else (lambda x: C.paid_min(x["span"]) / 60.0)
    out = []
    if dedup in ("rows", "noninstant"):
        for x in rows:
            if dedup == "noninstant" and abs(x["closed"] - x["raised"]) < 1e-6:
                continue
            out.append(dict(loc=x["loc"], hours=hours(x), covered=x["outcome"] == "FILLED", by=x["by"], d=x["d"]))
        return out
    if dedup == "keys":
        g = collections.OrderedDict()
        for x in sorted(rows, key=lambda x: x["raised"]):
            g.setdefault((x["loc"], x["day"], x["s"], x["e"], x["reason"], x["absent"]), []).append(x)
        for k, lst in g.items():
            fill = [x for x in lst if x["outcome"] == "FILLED"]
            out.append(dict(loc=lst[0]["loc"], hours=hours(lst[0]), covered=bool(fill), by=fill[-1]["by"] if fill else "",
                            d=lst[0]["d"]))
        return out
    # the shifts: a dropped fill is a FILLED posting whose filler is later the absent person on a call-in for the
    # same shift; that call-in carries the shift on
    pay_at = {}

    def pno(pc, d):
        key = (pc, d)
        if key not in pay_at:
            pay_at[key] = str(C.payroll_on(B, pc, d))
        return pay_at[key]

    absent_days = set()
    if dayvoid:
        for x in _reg(B):
            if x["reason"] == "ABS" and x["absent"]:
                absent_days.add((x["absent"], x["day"], x["raised"]))
    by_shift = collections.defaultdict(list)
    for x in rows:
        if not opn and x["reason"] == "OPN":
            continue
        by_shift[(x["loc"], x["day"], x["s"], x["e"])].append(x)
    for key, lst in by_shift.items():
        lst.sort(key=lambda x: x["raised"])
        fills = [x for x in lst if x["outcome"] == "FILLED"]
        dropped = set()
        continuing = set()
        if drops:
            for f in fills:
                p = pno(f["by"], f["d"])
                later = [x for x in lst if x["reason"] == "ABS" and x["absent"] == p and x["raised"] > f["closed"]]
                if later:
                    dropped.add(id(f))
                    for x in lst:
                        if x["reason"] == "ABS" and x["absent"] == p and x["raised"] >= later[0]["raised"]:
                            continuing.add(id(x))
                elif dayvoid and any(a == p and dd == f["day"] and r > f["closed"] for a, dd, r in absent_days):
                    dropped.add(id(f))
        if dedup == "keysdrops":
            # one shift per store, date, times, reason and absent payroll number; a give-back's call-ins carry on
            groups = collections.OrderedDict()
            for x in lst:
                if id(x) not in continuing:
                    groups.setdefault((x["reason"], x["absent"]), []).append(x)
            good = [f for f in fills if id(f) not in dropped]
            for gk, gl in groups.items():
                ids = {id(x) for x in gl}
                own = [f for f in good if id(f) in ids]
                if not own:
                    # a give-back's re-raise that was filled covers the shift it carries on
                    own = [f for f in good if id(f) in continuing and any(id(d) in ids for d in fills
                                                                           if id(d) in dropped)]
                out.append(dict(loc=key[0], hours=hours(lst[0]), covered=bool(own), by=own[0]["by"] if own else "",
                                d=lst[0]["d"]))
            continue
        # originals: open lines raised at publication, and each vacated line's first posting
        units = 0
        seen = set()
        for x in lst:
            if id(x) in continuing:
                continue
            if x["reason"] == "OPN":
                if x["r"]["raised_at"] == PUBLISHED_25 or not _is_repost(x):
                    units += 1
            elif dedup == "raise":
                if not _is_repost(x):
                    units += 1
            else:
                k2 = (x["reason"], x["absent"])
                if k2 not in seen:
                    seen.add(k2)
                    units += 1
        if keepfill:
            # the first fill stands as the cover; a fill on the give-back's re-raise is not counted again
            good = [f for f in fills if id(f) not in continuing]
        else:
            good = [f for f in fills if id(f) not in dropped]
        for f in good:
            out.append(dict(loc=key[0], hours=hours(lst[0]), covered=True, by=f["by"], d=f["d"]))
        for _ in range(units - len(good)):
            out.append(dict(loc=key[0], hours=hours(lst[0]), covered=False, by="", d=lst[0]["d"]))
    return out


def shift_shares(B, windows):
    """each store's share of call-in hours covered, counted by shift (reposts and re-raises after a drop folded into
    their shift), over the shifts dated in any of `windows`"""
    tot = collections.Counter()
    cov = collections.Counter()
    for w in windows:
        for x in shifts(B, window=w):
            tot[x["loc"]] += x["hours"]
            if x["covered"]:
                cov[x["loc"]] += x["hours"]
    return {loc: cov[loc] / tot[loc] if tot[loc] else 0.0 for loc in B.locs}


def _is_repost(x):
    m = x["raised"] % 1440
    return abs(m - 420) < 1e-6


def ask_a(B, **kw):
    sh = shifts(B, **kw)
    out = {}
    for loc in B.locs:
        mine = [x for x in sh if x["loc"] == loc]
        put = sum(x["hours"] for x in mine)
        cov = sum(x["hours"] for x in mine if x["covered"])
        out[loc] = dict(put_out=put, covered=cov, uncovered=put - cov)
    return out


def ask_b(B, home_rule="payroll", **kw):
    sh = shifts(B, **kw)
    imp = collections.Counter()
    exp = collections.Counter()
    for x in sh:
        if not x["covered"]:
            continue
        home = C.home_loc(B, x["by"], x["d"]) if home_rule == "payroll" else B.people[x["by"]]["home_location"]
        if home != x["loc"]:
            imp[x["loc"]] += x["hours"]
            exp[home] += x["hours"]
    return {loc: dict(imports=imp[loc], exports=exp[loc]) for loc in B.locs}


def stops(B):
    """each ask's ladder: the golden and every named wrong path"""
    return dict(
        A_golden=ask_a(B),
        A_S1_rows=ask_a(B, dedup="rows"),
        A_S2_keys=ask_a(B, dedup="keys"),
        A_S3_nodrops=ask_a(B, drops=False),
        A_S1b_noninstant=ask_a(B, dedup="noninstant"),
        A_S3b_raise=ask_a(B, dedup="raise"),
        A_S3c_keepfill=ask_a(B, keepfill=True),
        A_S4_utc=ask_a(B, use_utc=True),
        A_S5_span=ask_a(B, span_hours=True),
        A_S6_noopn=ask_a(B, opn=False),
        A_S7_dayvoid=ask_a(B, dayvoid=True),
        A_crack=ask_a(B, dedup="keysdrops"),
        B_golden=ask_b(B),
        B_S1_current=ask_b(B, home_rule="kws"),
        B_S2_nodrops=ask_b(B, drops=False),
        B_S3_rows=ask_b(B, dedup="rows"),
        B_S3b_raise=ask_b(B, dedup="raise"),
        B_S3c_keepfill=ask_b(B, keepfill=True),
        B_S7_dayvoid=ask_b(B, dayvoid=True),
        B_crack=ask_b(B, dedup="keysdrops"),
    )
