"""task157 architecture 3: the golden and every rung, from the records as the pack carries them.

The main call: each route's punctuality over the autumn record and its forecast for the closure, the closure
replayed on the recorded days with the minutes it adds passed on by buses and by drivers; the routes forecast below
the 80 per cent floor are the notice's routes. The asks: each route's operator-cause lost kilometres and
reliability over the autumn; the average weekday boardings at the stops the diversion leaves unserved, by direction
and time band, October and November."""
from __future__ import annotations

from collections import defaultdict
from datetime import date

import analysis as A
import params as P

OPERATOR_CAUSES = ("VD", "SS", "SI", "TR", "AV")
EXCUSED = ("PC", "RW", "WX", "BD")


def prev_links(S):
    """(day type, board, first journey code of a piece) -> (board of the piece before it in the duty, that piece's
    last journey code, scheduled gap in minutes)."""
    out = {}
    for dt, s in S.items():
        pcs = s["pieces"]
        for duty in s["duties"]:
            for a, b in zip(duty, duty[1:]):
                out[(dt, pcs[b]["board"], pcs[b]["journeys"][0]["code"])] = (
                    pcs[a]["board"], pcs[a]["journeys"][-1]["code"], pcs[b]["on"] - pcs[a]["off"])
    return out


def main(parsed, S):
    links = prev_links(S)
    autumn = A.punctuality(parsed)
    out = dict(autumn=autumn)
    runs = {
        "golden": dict(),
        "R0": dict(knock=False),
        "R1_buses": dict(drivers=False),
        "walk1": dict(walk=1.0), "walk2": dict(walk=2.0), "walk4": dict(walk=4.0),
        "turn0": dict(turn=0.0), "turn2": dict(turn=2.0),
        "turn2_walk3": dict(turn=2.0, walk=3.0),
        "drivers_only": dict(carry_bus=False),
        "no_corridor": dict(corridor=False),
        "scale_close_out": dict(scale=1.05),
        "scale_low": dict(scale=0.9),
        "over_corrected": dict(gap_aware=False, max_gap=999.0),
        "over_corrected_30": dict(gap_aware=False, max_gap=30.0),
        "all_joins": dict(max_gap=999.0),
    }
    for name, kw in runs.items():
        lk = links if kw.get("knock", True) else {}
        rep = A.replay(parsed, lk, **kw)
        p = A.punctuality(rep, drop=A.unserved)
        out[name] = dict(p=p, set=A.designate(p))
    # the closure's day mix (11 January to 28 March 2027: Good Friday runs the Sunday timetable)
    mix = defaultdict(int)
    for d in P.days(P.CLOSE_FIRST, P.CLOSE_LAST):
        mix[P.day_type(d)] += 1
    seen = defaultdict(set)
    for x in parsed:
        seen[x["dt"]].add(x["date"])
    w = {dt: mix[dt] / len(seen[dt]) for dt in mix}
    rep = A.replay(parsed, links)
    p = A.punctuality(rep, drop=A.unserved, weights=w)
    out["closure_mix"] = dict(p=p, set=A.designate(p))
    out["mix"] = dict(mix)
    # weekdays only, and the record after the clock change only
    for name, keep in (("weekdays", lambda x: x["dt"] == "MF"),
                       ("after_clock_change", lambda x: x["date"] >= P.CLOCK_CHANGE),
                       ("term_time", lambda x: P.is_school_day(x["date"]) or x["dt"] != "MF")):
        sub = [x for x in rep if keep(x)]
        p = A.punctuality(sub, drop=A.unserved)
        out[name] = dict(p=p, set=A.designate(p))
    return out


def seasonal(main_out, pub_rows):
    """Each route's forecast with the published series' winter shift added (January to March 2026 against
    September to November 2025, final figures)."""
    vals = defaultdict(dict)
    for r, month, dep, on, pct, status, published in pub_rows:
        if status != "final":
            continue
        vals[r][month] = 100.0 * on / dep
    out = {}
    for r in vals:
        w = sum(vals[r]["2026-%02d" % m] for m in (1, 2, 3)) / 3
        a = sum(vals[r]["2025-%02d" % m] for m in (9, 10, 11)) / 3
        out[r] = w - a
    p = {r: main_out["golden"]["p"][r] + out[r] for r in main_out["golden"]["p"]}
    return dict(shift=out, p=p, set=A.designate(p))


# ------------------------------------------------------------------ ask A: lost kilometres and reliability
def link_km(route, direction):
    R = P.ROUTES[route]
    return list(R["km"]) if direction == "O" else list(R["km_in"][::-1])


def lost_km(route, direction, kind, i0, i1):
    km = link_km(route, direction)
    n = len(km) + 1
    if kind == "whole":
        return sum(km)
    if kind == "part":
        return sum(km[i0 - 1:])           # from the stop where it ended to the end
    return sum(km[:i1 + 1])               # from the start to the stop where it started


def scheduled_km(S):
    out = defaultdict(float)
    for d in P.days(P.AVL_FIRST, P.AVL_LAST):
        dt = P.day_type(d)
        school = P.is_school_day(d)
        for r in P.ROUTE_ORDER:
            for j in S[dt]["journeys"][r]:
                if j["school"] and not school:
                    continue
                out[r] += sum(link_km(r, j["dir"]))
    return dict(out)


def ask_a(S, lost):
    """Operator-cause lost kilometres and reliability by route, 1 September to 6 December 2026 (truth: every lost
    span once)."""
    km = defaultdict(float)
    exc = defaultdict(float)
    for x in lost:
        kind, cause, i0, i1 = x["lost"]
        k = lost_km(x["route"], x["dir"], kind, i0, i1)
        if cause in OPERATOR_CAUSES:
            km[x["route"]] += k
        else:
            exc[x["route"]] += k
    sched = scheduled_km(S)
    rel = {r: 100.0 * (sched[r] - km[r]) / sched[r] for r in P.ROUTE_ORDER}
    return dict(op_km={r: km[r] for r in P.ROUTE_ORDER}, exc_km={r: exc[r] for r in P.ROUTE_ORDER}, sched_km=sched,
                reliability=rel)


# ------------------------------------------------------------------ ask B: boardings at the unserved stops
def ask_b(truth, rows):
    """Average weekday boardings in October and November 2026 at fare stages 3 and 4 (every stop the diversion
    leaves unserved), by direction and time band; the re-sent copies are one upload's repeat."""
    wk = sorted({t["date"] for t in truth if t["dt"] == "MF"})
    n = len(wk)
    cnt = defaultdict(int)
    for t in truth:
        if t["dt"] != "MF" or t["stage"] not in P.UNSERVED_STAGES:
            continue
        cnt[(t["true_dir"], t["band"])] += 1
    bands = ("AM peak", "PM peak", "Other times")
    return dict(weekdays=n, cells={(d, b): cnt[(d, b)] / n for d in ("I", "O") for b in bands},
                total=sum(cnt.values()) / n)


def ask_b_selected(truth):
    wk = sorted({t["date"] for t in truth if t["dt"] == "MF"})
    n = len(wk)
    cnt = defaultdict(int)
    for t in truth:
        if t["dt"] != "MF" or t["stage"] not in P.UNSERVED_STAGES:
            continue
        cnt[(t["sel_dir"], t["band"])] += 1
    bands = ("AM peak", "PM peak", "Other times")
    return {(d, b): cnt[(d, b)] / n for d in ("I", "O") for b in bands}


# ------------------------------------------------------------------ ask A from the shipped logs (the solver's path)
def _tod(s):
    h, m = s.split(":")
    return int(h) * 60 + int(m)


def ask_a_from_logs(S, log, ret, pieces_rows, mode="right", avl_seen=None):
    """Operator-cause lost kilometres by route, rebuilt from the control room log and the depot's returns.
    mode: right (each lost span once: the controller's journeys and the returns' uncovered pieces expanded to their
    journeys through the duty schedule and the timetable, less those the AVL saw run, joined on date and journey),
    union_no_avl (the same without the AVL's word on the returns), sum (the two sources added),
    controller (the log alone), returns_whole (a part-covered piece taken as wholly lost), tr_excused (turning short
    for late running read as excused), part_whole (a part journey counted whole)."""
    from datetime import datetime as _dt
    stop_idx = {}
    for dt in ("MF", "SA", "SU"):
        for r in P.ROUTE_ORDER:
            for j in S[dt]["journeys"][r]:
                stop_idx[j["code"]] = (r, j["dir"], [P.TP_ATCO[(r, k, j["dir"])] for k in j["tps"]])
    spans = defaultdict(list)          # (date, journey) -> [(first link, last link, cause, source)]
    for e in log:
        if e["event"] not in ("LOST", "PART LOST"):
            continue
        d = e["t"].date()
        code = e["journey"]
        r, dirn, codes = stop_idx[code]
        n = len(codes) - 1
        if e["event"] == "LOST" or mode == "part_whole":
            a, z = 0, n - 1
        else:
            a, z = codes.index(e["lost_from"]), codes.index(e["lost_to"]) - 1
        spans[(d, code)].append((a, z, e["cause"], "log"))
    if mode != "controller":
        names = {"MF": "Mon-Fri", "SA": "Sat", "SU": "Sun"}
        pidx = {}
        for row in pieces_rows:
            num, days, k, board, svc, on, on_at, off, off_at = row
            t_on, t_off = _tod(on), _tod(off)
            if t_off < t_on:
                t_off += 24 * 60          # relieved after midnight
            pidx[(num, k)] = (board, svc, t_on, on_at, t_off, off_at, days)
        boards = {}
        for dt in ("MF", "SA", "SU"):
            for b in S[dt]["boards"]:
                boards[(dt, b["board"])] = b["journeys"]
        for e in ret:
            if e["status"] not in ("UNCOVERED", "PART COVERED"):
                continue
            d = e["date"]
            dt = P.day_type(d)
            board, svc, on, on_at, off, off_at, days = pidx[(e["duty"], e["piece"])]
            js = [j for j in boards[(dt, board)] if j["dep"] >= on - 0.01 and j["arr"] <= off + 0.01]
            if e["status"] == "PART COVERED" and mode != "returns_whole":
                cf = _tod(e["covered_from"])
                js = [j for j in js if j["dep"] < cf]
            for j in js:
                if mode == "right" and avl_seen is not None and (d, j["code"]) in avl_seen:
                    continue              # the AVL saw it run: a spare covered it after the return was made
                n = len(j["tps"]) - 1
                spans[(d, j["code"])].append((0, n - 1, "SS", "returns"))
    km = defaultdict(float)
    for (d, code), sp in spans.items():
        r, dirn, codes = stop_idx[code]
        kms = link_km(r, dirn)
        if mode == "sum":
            use = sp
        else:
            # one journey's lost links once: the union of its spans
            links = set()
            cause_of = {}
            for a, z, c, src in sp:
                for l in range(a, z + 1):
                    links.add(l)
                    cause_of.setdefault(l, c)
            use = [(l, l, cause_of[l], "") for l in sorted(links)]
        for a, z, c, src in use:
            op = c in OPERATOR_CAUSES and not (mode == "tr_excused" and c == "TR")
            if op:
                km[r] += sum(kms[a:z + 1])
    return {r: km[r] for r in P.ROUTE_ORDER}



def ask_b_variant(truth, use_sel=False, use_rec_band=False):
    """The ask's table under a handling: use_sel takes the machine's selected direction (the journey not changed
    at the terminus), use_rec_band bands the machine's clock time (two machines kept summer time from 25 October)."""
    wk = sorted({t["date"] for t in truth if t["dt"] == "MF"})
    n = len(wk)
    cnt = defaultdict(int)
    for t in truth:
        if t["dt"] != "MF" or t["stage"] not in P.UNSERVED_STAGES:
            continue
        cnt[(t["sel_dir"] if use_sel else t["true_dir"], t["rec_band"] if use_rec_band else t["band"])] += 1
    bands = ("AM peak", "PM peak", "Other times")
    return {(d, b): cnt[(d, b)] / n for d in ("I", "O") for b in bands}
