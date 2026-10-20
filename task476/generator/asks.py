"""The asks' own records: work-order cost lines (each line carries the work order's cost of its type to date) and
service interruption tickets with the meter premises behind each service address. None of these rows is read by the
call."""
import datetime as dt

import truth as T
import world as W
import records as R

TYPES = ("LABOR", "MATERIAL", "CONTRACTOR", "RESTORATION")


def cost_lines(lk):
    """Leak work orders with charges in 2025 or 2026: each posting is the work order's cost of that type to date. A
    work order's cost center is its crew's district, which for leaks near a district line is the next district."""
    out = []
    names = list(W.DISTRICTS)
    for L in lk:
        if not (2025 <= L.found.year <= 2026):
            continue
        r = T.rng_for("costs", L.lid)
        wo = "WO-%s" % L.lid[1:].replace("-", "")
        cc = L.seg.district
        if r.random() < 0.09:
            i = names.index(cc)
            cc = names[(i + 1 + int(r.integers(0, len(names) - 1))) % len(names)]
        base = {1: 4200, 2: 3100, 3: 1900}[L.grade]
        when = [L.found] + [v[0] for v in R.visits(L)]
        for ty in TYPES:
            if ty == "RESTORATION" and r.random() < 0.4:
                continue
            total = 0.0
            for k, t in enumerate(when):
                if t.date() > W.EXTRACT or (ty in ("CONTRACTOR", "RESTORATION") and k == 0):
                    continue
                inc = round(float(r.uniform(0.2, 1.0)) * base * {"LABOR": 0.45, "MATERIAL": 0.2, "CONTRACTOR": 0.6,
                                                                 "RESTORATION": 0.35}[ty], 2)
                total = round(total + inc, 2)
                post = (t + dt.timedelta(days=int(r.integers(2, 12)))).date()
                if post > W.EXTRACT:
                    continue
                out.append(dict(wo=wo, leak=L.lid, cc=cc, district=L.seg.district, type=ty, posted=post,
                                amount=total, inc=inc))
    out.sort(key=lambda x: (x["posted"], x["wo"], x["type"]))
    return out


def ask_a(lines):
    """Each district's leak repair cost posted in 2026: per work order and type, the cost to date at the end of 2026
    less the cost to date at the end of 2025, by the leak's own district."""
    last = {}
    for x in lines:
        k = (x["wo"], x["type"])
        if x["posted"].year <= 2026:
            last.setdefault(k, {})[x["posted"].year] = x["amount"]
    out = {d: 0.0 for d in W.DISTRICTS}
    dist = {(x["wo"], x["type"]): x["district"] for x in lines}
    for k, v in last.items():
        if 2026 in v:
            out[dist[k]] += v[2026] - v.get(2025, 0.0)
    return {d: round(v, 2) for d, v in out.items()}


def premises(segs):
    """Service addresses on every main segment with the number of meters behind each (apartment buildings carry
    several)."""
    out = []
    n = 0
    used = set()
    for s in segs:
        r = T.rng_for("prem", s.sid)
        for k in range(int(r.integers(4, 14))):
            n += 1
            while True:
                num = int(r.integers(1, 60)) * 20 + int(r.integers(0, 19))
                if (num, R.street(s)) not in used:
                    used.add((num, R.street(s)))
                    break
            meters = int(r.choice([1, 1, 1, 1, 2, 2, 3, 4, 6, 8, 12, 24], p=[.3, .2, .15, .1, .07, .05, .04, .03, .02,
                                                                             .02, .01, .01]))
            out.append(dict(premise="P%07d" % (2000000 + n), addr="%d %s" % (num, R.street(s)), district=s.district,
                            meters=meters, seg=s.sid))
    return out


def tickets(lk, prem):
    """Service interruptions in 2026: when a repair shut off service, a ticket per service address interrupted;
    dispatch opens one and the field crew sometimes opens its own for the same address minutes later."""
    by_seg = {}
    for p in prem:
        by_seg.setdefault(p["seg"], []).append(p)
    out = []
    n = 0
    for L in lk:
        for t, act, g in R.visits(L):
            if act != "REPAIRED" or t.year != 2026:
                continue
            r = T.rng_for("tix", L.lid)
            if r.random() > 0.42:
                continue
            ps = by_seg.get(L.seg.sid, [])
            if not ps:
                continue
            hit = [ps[int(i)] for i in sorted(set(int(x) for x in r.integers(0, len(ps), size=int(r.integers(1, 4)))))]
            for p in hit:
                n += 1
                t0 = t + dt.timedelta(minutes=int(r.integers(-40, 30)))
                out.append(dict(ticket="DSP-%06d" % (300000 + n), opened=t0, addr=p["addr"], leak=L.lid,
                                restored=t0 + dt.timedelta(hours=float(r.uniform(1.5, 9))), src="DISPATCH",
                                premise=p["premise"]))
                if r.random() < 0.18:
                    n += 1
                    out.append(dict(ticket="FLD-%06d" % (300000 + n), opened=t0 + dt.timedelta(minutes=int(r.integers(4, 26))),
                                    addr=p["addr"], leak=L.lid, restored=out[-1]["restored"], src="FIELD",
                                    premise=p["premise"]))
    out.sort(key=lambda x: (x["opened"], x["ticket"]))
    return out


def ask_b(tix, prem):
    """Each district's customers (meters) whose service was interrupted in 2026: each interrupted service address
    once per event, its meters counted."""
    meters = {p["premise"]: (p["meters"], p["district"]) for p in prem}
    seen = set()
    out = {d: 0 for d in W.DISTRICTS}
    for t in tix:
        k = (t["premise"], t["leak"])
        if k in seen:
            continue
        seen.add(k)
        m, d = meters[t["premise"]]
        out[d] += m
    return out
