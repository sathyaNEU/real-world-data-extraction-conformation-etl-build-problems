"""The records the region's systems hold, cut from the world: the count management system's hourly export, the station
register, the road network, the validation contractor's counts."""
import datetime as dt

import numpy as np
import pandas as pd

import ops
import params as P
import sim

CONTRACTOR_ORDER_SEED = 77


def code_at(code, day):
    """the number a station carried on a day (two were renumbered when their controllers were replaced)"""
    if code in P.RENUMBERED and day >= P.RENUMBERED[code][1]:
        return P.RENUMBERED[code][0]
    return code


def new_controller(code, day):
    if code in P.RENUMBERED:
        return day >= P.RENUMBERED[code][1]
    return code in P.NEW_CONTROLLERS


def occ_text(occ, newc):
    """the older TCX-2 reports occupancy to one decimal, the newer TCX-4 to two"""
    return "%.2f" % occ if newc else "%.1f" % occ


def switch_hour(O, code):
    """the first hour a renumbered station counts under its new number (after the replacement's lost hours)"""
    return O["swaps"][code]["first_new"] if code in O["swaps"] else None


def code_hour(O, code, i):
    s = switch_hour(O, code)
    return P.RENUMBERED[code][0] if s is not None and i >= s else code


def tcx4_hour(O, code, i):
    s = switch_hour(O, code)
    return i >= s if s is not None else code in P.NEW_CONTROLLERS


def hourly(W, O):
    """the count management system's hourly export: every station, direction and hour it holds"""
    C = W["C"]
    rows = []
    loc = C["loc"]
    stamps = [x.strftime("%Y-%m-%d %H:%M") for x in loc]
    offs = [x.strftime("%z") for x in loc]
    offs = [o[:3] + ":" + o[3:] for o in offs]
    for x in W["st"]:
        lost = O["lost"].get(x["code"], set())
        for d in x["dirs"]:
            r = W["rec"][(x["code"], d)]
            occ = W["true"][(x["code"], d)]["occ"]
            for i in range(sim.NH):
                if i in lost:
                    continue
                rows.append((code_hour(O, x["code"], i), d, stamps[i], offs[i], int(r[i]),
                             occ_text(occ[i], tcx4_hour(O, x["code"], i))))
    df = pd.DataFrame(rows, columns=["station", "direction", "local_start", "utc_offset", "vehicles", "occupancy"])
    # the export runs station by station, each direction's hours in time order
    order = sorted(df["station"].unique(), key=lambda c: (int(c[1:3]), c))
    df["station"] = pd.Categorical(df["station"], categories=order, ordered=True)
    df = df.sort_values(["station", "direction"], kind="stable")
    df["station"] = df["station"].astype(str)
    return df.reset_index(drop=True)


def _z(t):
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def events(W, O):
    """TrafficVault's station event log: what the TCX-4 controllers reported and what TrafficVault raised itself"""
    rng = np.random.default_rng(W["seed"] + 640)
    sx = {x["code"]: x for x in W["st"]}
    polls = O["polls"]
    rows = []   # (code at receipt, logged time, raised_by, event, receipt time)

    def add(code, t, by, ev, rec=None):
        rows.append([code, t, by, ev, rec or t])

    def code_t(code, t):
        return R_code(code, ops.local(t).date())

    for r in O["power"]:
        c = r["code"]
        ok = [t for t, by, ev in r["events"] if ev == "COMMS_OK"]
        rec = ok[0] if ok else None
        for t, by, ev in r["events"]:
            receipt = rec if (t.year == 2000 and rec) else t
            add(code_t(c, receipt), t, by, ev, receipt)
    for code, s in O["swaps"].items():
        for t, by, ev in s["ev_old"]:
            add(code, t, by, ev)
        for t, by, ev in s["ev_new"]:
            add(s["new"], t, by, ev, s["clock"] if t.year == 2000 else t)
    for w in O["work"]:
        if w["category"] == "Upgrade":
            continue
        for c, a, b in w["onsite"]:
            if ops.controller(sx[c], a.date()) == "TCX-4":
                add(code_t(c, ops.utc(a)), ops.utc(a + dt.timedelta(seconds=int(rng.integers(40, 360)))),
                    "controller", "DOOR_OPEN")
                add(code_t(c, ops.utc(b)), ops.utc(b - dt.timedelta(seconds=int(rng.integers(30, 300)))),
                    "controller", "DOOR_CLOSE")
        for c, at, how in w["resets"]:
            add(code_t(c, ops.utc(at)), ops.utc(at), "controller", "RESET")
        if w["comms"]:
            c, fault, restore = w["comms"]
            t0 = ops.poll_after(polls[c], ops.utc(fault))
            t1 = ops.poll_after(polls[c], ops.utc(restore) + dt.timedelta(seconds=ops.BOOT_S))
            add(code_t(c, t0), t0, "TrafficVault", "COMMS_LOST")
            add(code_t(c, t1), t1, "TrafficVault", "COMMS_OK")
    for c, a, b in O["crew"] + O["region"]:
        if ops.controller(sx[c], a.date()) == "TCX-4":
            add(code_t(c, ops.utc(a)), ops.utc(a), "controller", "DOOR_OPEN")
            add(code_t(c, ops.utc(b)), ops.utc(b), "controller", "DOOR_CLOSE")
    # a clock correction most Sunday nights at every TCX-4, and the polls that fail once and succeed at the next
    busy = {}
    for row in rows:
        busy.setdefault(row[0], []).append(row[4])
    for p in O["power"]:
        a, b = p["window"]
        t = a - dt.timedelta(minutes=30)
        while t <= b + dt.timedelta(minutes=30):
            busy.setdefault(code_t(p["code"], t), []).append(t)
            t += dt.timedelta(minutes=10)
    for x in W["st"]:
        for day in W["C"]["days"]:
            if day.weekday() == 6 and ops.controller(x, day) == "TCX-4" and rng.random() < 0.6:
                t = ops.poll_after(polls[x["code"]], ops.utc(dt.datetime.combine(day, dt.time(3, 0))))
                t = t + dt.timedelta(seconds=9)
                if not _near(busy.get(R_code(x["code"], day), []), t, 6):
                    add(R_code(x["code"], day), t, "TrafficVault", "CLOCK_SET")
        for _ in range(int(rng.poisson(13))):
            day = W["C"]["days"][int(rng.integers(len(W["C"]["days"])))]
            t = ops.poll_after(polls[x["code"]], ops.utc(dt.datetime.combine(day, dt.time(0, 0)) +
                                                          dt.timedelta(minutes=int(rng.integers(0, 1440)))))
            code = R_code(x["code"], day)
            if _near(busy.get(code, []), t, 12) or (x["code"] in P.RENUMBERED and
                                                     abs((P.RENUMBERED[x["code"]][1] - day).days) <= 1):
                continue
            k = int(rng.choice([1, 1, 1, 2]))
            add(code, t, "TrafficVault", "COMMS_LOST")
            add(code, t + dt.timedelta(seconds=ops.POLL_S * k), "TrafficVault", "COMMS_OK")
            busy.setdefault(code, []).append(t)
    # a controller re-sends some of what it had buffered when TrafficVault reaches it again
    by_code = {}
    for row in rows:
        by_code.setdefault(row[0], []).append(row)
    dups = []
    for code, rs in by_code.items():
        rs.sort(key=lambda r: (r[4], r[1]))
        lost_at = None
        for r in rs:
            if r[3] == "COMMS_LOST":
                lost_at = r[4]
            elif r[3] == "COMMS_OK" and lost_at is not None:
                since = lost_at - dt.timedelta(seconds=ops.POLL_S)
                held = [q for q in rs if q[2] == "controller" and since <= q[4] <= r[4]]
                if held and rng.random() < 0.45:
                    k = int(rng.integers(1, len(held) + 1))
                    dups.extend([q[:4] + [r[4] + dt.timedelta(seconds=1)] for q in held[-k:]])
                lost_at = None
    rows.extend(dups)
    df = pd.DataFrame(rows, columns=["station", "t", "raised_by", "event", "receipt"])
    df["logged_utc"] = df["t"].map(_z)
    order = sorted(df["station"].unique(), key=lambda c: (int(c[1:3]), c))
    df["station"] = pd.Categorical(df["station"], categories=order, ordered=True)
    df = df.sort_values(["station", "receipt"], kind="stable")
    df["station"] = df["station"].astype(str)
    return df[["station", "logged_utc", "raised_by", "event"]].reset_index(drop=True)


def _near(ts, t, minutes):
    return any(abs((u - t).total_seconds()) < minutes * 60 for u in ts)


def R_code(code, day):
    return code_at(code, day)


def work_orders(W, O):
    """the maintenance contractor's work orders at the stations and the labour booked to them"""
    orders, labour = [], []
    for w in sorted(O["work"], key=lambda w: w["order"]):
        orders.append(dict(order=w["order"], opened=w["opened"], closed=w["closed"], category=w["category"],
                           stations="; ".join(code_at(c, w["opened"]) if w["category"] != "Upgrade" else c
                                              for c in w["stations"]),
                           description=w["description"], resolution=w["resolution"]))
        for day, tech, hours in sorted(w["labour"]):
            labour.append(dict(order=w["order"], date=day, technician=tech, hours=hours))
    return pd.DataFrame(orders), pd.DataFrame(labour)


def contractor_codes(W):
    rng = np.random.default_rng(CONTRACTOR_ORDER_SEED)
    order = rng.permutation(len(W["st"]))
    return {W["st"][i]["code"]: "HLB-%02d" % (k + 1) for k, i in enumerate(order)}


def register(W, jn):
    """the station register; each station described from the nearest junction on its road"""
    cc = contractor_codes(W)
    rng = np.random.default_rng(91)
    rows = []
    for x in W["st"]:
        code = P.RENUMBERED[x["code"]][0] if x["code"] in P.RENUMBERED else x["code"]
        newc = x["code"] in P.NEW_CONTROLLERS
        rows.append(dict(station=code, road="RR %d" % x["road"], km=round(x["km"], 2),
                         location=location(x, jn), district=x["district"], lanes_each_way=x["lanes"],
                         controller="TCX-4" if newc else "TCX-2",
                         in_service_since=int(rng.choice([2009, 2011, 2013, 2016, 2019])) if x["kind"] == "other"
                         else 2019, validation_site=cc[x["code"]]))
    st = pd.DataFrame(rows)
    hist = pd.DataFrame([dict(old_station=a, new_station=b, from_date=d, reason="controller replaced, TCX-2 to TCX-4")
                         for a, (b, d) in P.RENUMBERED.items()])
    return st, hist


CROSS = ["Harbour Rd", "Linden St", "Mill Rd", "Quarry Line", "Station St", "Orchard Rd", "Kingsley Ave", "Bell Rd",
         "Cedar Line", "Parkhill Dr", "Victoria St", "Fenwick Rd", "Grange Rd", "Maple Ave", "Church St", "Willow Rd",
         "Concession 4", "Sideroad 15", "Townline Rd", "Dunmore Rd", "Elgin St", "Ridge Rd", "Brant St", "Lakeview Dr",
         "Forest Rd", "Union St", "Wellesley Rd", "Ashby Line", "Marlow Rd", "Kessel Rd"]


def location(x, jn):
    road = "RR %d" % x["road"]
    j = jn[jn["road"] == road]
    k = (j["km"] - x["km"]).abs().idxmin()
    near = j.loc[k]
    m = int(round(abs(near["km"] - x["km"]) * 100.0) * 10)
    if x["axis"] == "NS":
        side = "north" if x["km"] > near["km"] else "south"
    else:
        side = "east" if x["km"] > near["km"] else "west"
    return "%d m %s of %s" % (m, side, near["crossing"])


def network(W):
    """junctions and structures along every regional road with a station, by kilometre point"""
    rng = np.random.default_rng(57)
    junctions, structures = [], []
    roads = sorted({x["road"] for x in W["st"]})
    for road in roads:
        sts = [x for x in W["st"] if x["road"] == road]
        length = max(x["km"] for x in sts) + rng.uniform(4, 9)
        kms = list(np.round(np.cumsum(rng.uniform(0.7, 2.4, 40)), 2))
        kms = [k for k in kms if k < length]
        blocked = []
        for b in P.BRIDGES:
            if b["road"] == road:
                blocked.append((b["s_km"] - 0.05, b["n_km"] + 0.05))
        for x in sts:
            if x["kind"] == "other" and x["congested"]:
                # a signalised junction a few hundred metres downstream in each direction
                for sgn in (-1, 1):
                    kms.append(round(x["km"] + sgn * rng.uniform(0.22, 0.45), 2))
        kms = sorted({k for k in kms if not any(a <= k <= c for a, c in blocked)})
        for k in kms:
            near_cong = any(abs(k - x["km"]) < 0.5 and x["kind"] == "other" and x["congested"] for x in sts)
            ctl = "signals" if near_cong or rng.random() < 0.35 else str(rng.choice(["all-way stop", "two-way stop",
                                                                                     "roundabout"]))
            junctions.append(dict(road="RR %d" % road, km=k, crossing=str(rng.choice(CROSS)), control=ctl))
        for b in P.BRIDGES:
            if b["road"] == road:
                structures.append(dict(structure="B-%03d" % (road * 10 + 1), name=b["name"], road="RR %d" % road,
                                       km_from=b["km"][0], km_to=b["km"][1], type="bridge", carries="Kessel River",
                                       lanes_each_way=b["lanes"], built=int(rng.choice([1931, 1948, 1956, 1962]))))
        for c in range(int(rng.integers(0, 3))):
            k = float(np.round(rng.uniform(0.5, length), 2))
            if any(abs(k - x["km"]) < 0.3 for x in sts) or any(a <= k <= c for a, c in blocked):
                continue
            structures.append(dict(structure="C-%03d" % (road * 10 + 2 + c), name="", road="RR %d" % road,
                                   km_from=k, km_to=round(k + 0.02, 2), type="culvert", carries="creek",
                                   lanes_each_way=None, built=int(rng.choice([1968, 1975, 1984, 1997]))))
    jn = pd.DataFrame(junctions).sort_values(["road", "km"], key=lambda s: s.map(_roadkey) if s.name == "road" else s)
    sn = pd.DataFrame(structures).sort_values(["road", "km_from"], key=lambda s: s.map(_roadkey) if s.name == "road"
                                              else s)
    return jn.reset_index(drop=True), sn.reset_index(drop=True)


def _roadkey(r):
    return int(str(r).split()[-1])


def validation(W):
    """the contractor's 15-minute counts on each station's filmed weekday: the video count of the vehicles that
    passed and the loops' count for the same quarter hour, each direction"""
    cc = contractor_codes(W)
    rng = np.random.default_rng(W["seed"] + 202)
    C = W["C"]
    rows = []
    for x in W["st"]:
        idx = [i for i in range(sim.NH) if C["date"][i] == x["vday"]]
        for d in x["dirs"]:
            q = W["true"][(x["code"], d)]["q"]
            r = W["rec"][(x["code"], d)]
            for i in idx:
                w = rng.dirichlet(np.full(4, 30.0))
                vq = rng.multinomial(int(q[i]), w)
                lq = rng.multinomial(int(r[i]), w)
                for k in range(4):
                    t = C["loc"][i] + dt.timedelta(minutes=15 * k)
                    rows.append(dict(site=cc[x["code"]], date=x["vday"], direction=d, start=t.strftime("%H:%M"),
                                     video=int(vq[k]), loops=int(lq[k])))
    df = pd.DataFrame(rows)
    return df.sort_values(["date", "site", "direction", "start"]).reset_index(drop=True)
