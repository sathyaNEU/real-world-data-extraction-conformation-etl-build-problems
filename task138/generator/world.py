"""The district: laterals, turnouts and fields; the growers' 2027 water requests; four seasons of irrigation orders
from the growers' own schedules; the 2026 meters, lateral headings and tail weirs on the ask paths."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K
import weather as WX


class World:
    pass


# ---------------------------------------------------------------------------------------------------- the district

def build_district(W):
    r = K.rng("district")
    turnouts, fields = [], []
    used_new, used_old = set(), set()

    def new_id():
        while True:
            x = "F%05d" % int(r.integers(20100, 39999))
            if x not in used_new:
                used_new.add(x)
                return x

    def old_id():
        while True:
            x = "K%04d" % int(r.integers(1010, 8999))
            if x not in used_old:
                used_old.add(x)
                return x

    crop_codes = K.CROPS
    cp = np.array([K.CROP_SHARE[c] for c in crop_codes])
    cp = cp / cp.sum()
    soils = list(K.SOILS)
    for lat in K.LATERALS:
        n = K.TURNOUTS_PER_LATERAL[lat]
        lat_no = int(lat[1:])
        for k in range(1, n + 1):
            tid = "%02d-%03d" % (lat_no, k)
            moved = tid in K.MOVED
            soil0 = soils[int(r.choice(len(soils), p=K.SOIL_P))]
            nf = int(r.choice([1, 2, 3], p=[0.58, 0.30, 0.12]))
            t = dict(id=tid, lateral_built=lat, lateral=("L6" if moved else lat), moved=moved, fields=[],
                     meter_kind="M" if r.random() < 0.093 else "P")
            turnouts.append(t)
            crop0 = crop_codes[int(r.choice(len(crop_codes), p=cp))]
            for j in range(nf):
                crop = crop0 if (j == 0 or r.random() < 0.55) else crop_codes[int(r.choice(len(crop_codes), p=cp))]
                soil = soil0 if r.random() < 0.8 else soils[int(r.choice(len(soils), p=K.SOIL_P))]
                meths = K.METHOD_BY_CROP[crop]
                meth = meths[0] if r.random() < 0.68 else meths[-1]
                acres = float(np.clip(r.lognormal(math.log(56), 0.52), 6.0, 240.0))
                f = dict(id=new_id(), turnout=tid, lateral=t["lateral"], crop=crop, soil=soil, method=meth,
                         acres=round(acres, 2), grower_thr=float(r.uniform(0.38, 0.62)),
                         grower_depth=float(r.uniform(0.88, 1.12)), lag=int(r.integers(0, 3)))
                fields.append(f)
                t["fields"].append(f["id"])
    # former field ids (before the 2025 re-mapping); a parcel split gave two new fields one former id
    for t in turnouts:
        fl = [f for f in fields if f["turnout"] == t["id"]]
        if len(fl) >= 2 and r.random() < 0.22:
            o = old_id()
            fl[0]["former"] = o
            fl[1]["former"] = o
            for f in fl[2:]:
                f["former"] = old_id()
        else:
            for f in fl:
                f["former"] = old_id()
    W.turnouts, W.fields = turnouts, fields
    W.field = {f["id"]: f for f in fields}
    W.turnout = {t["id"]: t for t in turnouts}


def taw(f):
    """The field's root zone as it is (the growers' irrigation answers to it), not the procedure's planning tables."""
    awc, lim = K.PHYS_SOILS[f["soil"]]
    depth = K.PHYS_ROOT_FT[f["crop"]] if lim is None else min(K.PHYS_ROOT_FT[f["crop"]], lim)
    return awc * depth


def assign_2027(W):
    """Which fields carry an accepted 2027 request, which were withdrawn and which have none (fallowed or pulled)."""
    r = K.rng("requests-2027")
    for f in W.fields:
        u = r.random()
        f["req_status"] = "accepted" if u < 0.965 else ("withdrawn" if u < 0.985 else "none")
        f["revised"] = f["req_status"] == "accepted" and r.random() < 0.075


# ---------------------------------------------------------------------------------------------------- growers' orders

def _last_set_date(f, year, r):
    (m1, d1), (m2, d2) = K.LAST_SET_WINDOW[f["crop"]]
    a, b = dt.date(year, m1, d1), dt.date(year, m2, d2)
    return a + dt.timedelta(days=int(r.integers(0, (b - a).days + 1)))


HARVEST = {"ALM": ((8, 5), (8, 28)), "PIS": ((9, 1), (9, 20)), "WAL": ((9, 1), (9, 15)), "GRW": ((8, 10), (8, 28))}


def grower_season(W, f, year, true_wx):
    """The grower's own sets for one field and season: water when the field (as the grower judges it) has dried to
    the grower's own threshold, a refill of about the depletion, a dry-down before nut harvest, and a last set after
    harvest on a date of the grower's choosing. Each field and season draws from its own streams, the last set's date
    first. Returns a list of (start datetime, end datetime, cfs)."""
    r_last = K.rng("last-set", f["id"], year)
    r = K.rng("grower", f["id"], year)
    t_aw = taw(f)
    thr = f["grower_thr"] * t_aw
    kc = K.PHYS_KC[f["crop"]]
    ea = K.EA[f["method"]]
    last = _last_set_date(f, year, r_last)
    last_hour = int(r_last.choice([6, 7, 7, 8]))
    hv = HARVEST.get(f["crop"])
    if hv:
        (hm1, hd1), (hm2, hd2) = hv
        ha, hb = dt.date(year, hm1, hd1), dt.date(year, hm2, hd2)
        harvest = ha + dt.timedelta(days=int(r_last.integers(0, (hb - ha).days + 1)))
        cutoff = harvest - dt.timedelta(days=int(r_last.integers(10, 21)))
    else:
        harvest = cutoff = None
    # cfs: border and sprinkler sets take a big head, drip and micro a steady small one
    per_acre = {"Drip": 0.028, "Micro-sprinkler": 0.036, "Sprinkler": 0.040, "Border": 0.090}[f["method"]]
    cfs = max(1.0, round(f["acres"] * per_acre * float(r_last.uniform(0.85, 1.2)), 1))
    sets = []
    D = float(r.uniform(0, 0.25)) * t_aw   # the grower's sense of the field on 1 February
    thr = thr * {"Drip": 0.42, "Micro-sprinkler": 0.58, "Sprinkler": 0.85, "Border": 1.0}[f["method"]]
    max_hours = {"Drip": 60.0, "Micro-sprinkler": 48.0, "Sprinkler": 36.0, "Border": 30.0}[f["method"]]
    busy_until = dt.datetime(year, 2, 1)
    last_start = dt.datetime(last.year, last.month, last.day, last_hour, 0)
    wait = -1
    for d in K.season_days(year):
        e, rain = true_wx[d]
        D = min(t_aw, max(0.0, D + kc[d.month - 1] * e - rain))
        if d > last:
            continue
        if cutoff and cutoff <= d < harvest:
            continue
        due = D >= thr or d == last
        if due and wait < 0:
            wait = f["lag"] if d != last else 0
        if (wait == 0 or d == last) and (d == last or dt.datetime(d.year, d.month, d.day, 23, 0) > busy_until):
            depth = D * f["grower_depth"] / ea                       # inches of water at the turnout
            vol_af = max(depth * f["acres"] / 12.0, 0.35 * f["acres"] / 12.0)
            hours = vol_af / cfs * 12.1                              # 1 cfs for 12.1 hours is about an acre-foot
            if d == last:
                # the season's last set runs in daylight on the one day
                hours = min(hours, 15.5)
                start = last_start
            else:
                start = dt.datetime(d.year, d.month, d.day, int(r.choice([6, 7, 8, 18, 19])), int(r.choice([0, 30])))
                start = max(start, busy_until + dt.timedelta(hours=1))
                hours = min(hours, max_hours)
                # every earlier set ends a day before the last one starts
                room = (last_start - dt.timedelta(hours=24) - start).total_seconds() / 3600.0
                if room < 2.0:
                    wait = -1
                    continue
                hours = min(hours, room)
            hours = max(2.0, round(hours * 2) / 2)
            end = start + dt.timedelta(hours=hours)
            sets.append((start, end, cfs))
            busy_until = end
            applied = cfs * hours / 12.1 * 12.0 / f["acres"] * ea       # inches into the root zone
            D = max(0.0, D - applied)
            wait = -1
        elif wait > 0:
            wait -= 1
    assert all(sets[k][1] <= sets[k + 1][0] for k in range(len(sets) - 1)), (f["id"], year)
    # the last set is the season's last delivered water for the field
    assert sets and sets[-1][0].date() == last == sets[-1][1].date(), (f["id"], year)
    return sets


def build_orders(W, true_wx):
    """Every season's orders. Order numbers run by season; a share of orders were cancelled before water ran (one
    in about twenty-five), and some growers placed and cancelled a further order after their last set."""
    rows = []
    for year in K.ORDER_SEASONS:
        r = K.rng("orders", year)
        sets_all = []
        for f in W.fields:
            if True:
                ss = grower_season(W, f, year, true_wx)
                for s in ss:
                    sets_all.append((s[0], f["id"], s, "Delivered"))
                # cancelled orders: a few through the season, and for some fields one after the last set
                rc = K.rng("cancel", f["id"], year)
                n_c = int(rc.poisson(0.55))
                for _ in range(n_c):
                    a = ss[int(rc.integers(0, len(ss)))][0] + dt.timedelta(days=int(rc.integers(2, 9)))
                    if a.date() < ss[-1][0].date():
                        hrs = float(rc.choice([8.0, 10.0, 12.0, 24.0]))
                        sets_all.append((a, f["id"], (a, a + dt.timedelta(hours=hrs), ss[0][2]), "Cancelled"))
                rp = K.rng("cancel-after", f["id"], year)
                if rp.random() < 0.24:
                    a = ss[-1][0] + dt.timedelta(days=int(rp.integers(5, 31)))
                    if a.date() <= dt.date(year, 10, 31):
                        sets_all.append((a, f["id"], (a, a + dt.timedelta(hours=10.0), ss[-1][2]), "Cancelled"))
        sets_all.sort(key=lambda x: (x[0], x[1]))
        # each order is taken in office hours one to three working days ahead of its set; order numbers run in the
        # order the orders were entered
        taken = []
        for a, fid, s, status in sets_all:
            d, lead = a.date(), int(r.choice([1, 1, 1, 2, 2, 3]))
            while lead:
                d -= dt.timedelta(days=1)
                lead -= d.weekday() < 5
            entered = dt.datetime(d.year, d.month, d.day, 7, 0) + dt.timedelta(minutes=int(r.integers(0, 570)))
            taken.append((entered, fid, a, s, status))
        taken.sort(key=lambda x: (x[0], x[2], x[1]))
        for k, (entered, fid, a, s, status) in enumerate(taken):
            f = W.field[fid]
            assert entered < a
            rows.append(dict(season=year, order_no="%02d-%05d" % (year % 100, k + 101), turnout=f["turnout"],
                             field_id=fid if year >= 2025 else f["former"], cfs=s[2], start=s[0], end=s[1],
                             status=status, entered=entered))
    W.orders = rows


def delivered_sets(W, year):
    """(field id, start, end, cfs) for every delivered set of a season, by the current field id."""
    out = []
    by_former = {}
    for f in W.fields:
        by_former.setdefault(f["former"], []).append(f["id"])
    for o in W.orders:
        if o["season"] != year or o["status"] != "Delivered":
            continue
        fid = o["field_id"]
        out.append((fid, o["start"], o["end"], o["cfs"]))
    return out


def simulate():
    W = World()
    W.yard, W.st39 = WX.simulate()
    W.s39_rep, W.yard_rep = WX.reported(W.yard, W.st39)
    W.wx = WX.spliced(W.s39_rep, W.yard_rep)
    true_wx = {d: (w["et0_mm"] / 25.4, w["rain_in"]) for d, w in W.yard.items()}
    W.true_wx = true_wx
    build_district(W)
    assign_2027(W)
    build_orders(W, true_wx)
    build_requests(W)
    clear_tie_in(W)
    build_meters(W)
    build_laterals(W)
    return W


# ---------------------------------------------------------------------------------------------------- 2026 on the ask paths

TIE_IN = (dt.date(2026, 6, 13), dt.date(2026, 6, 15))
ASK_SALT = 0     # the draw of the 2026 meters, headings and weir sheets (the ask paths only)
NEW_METER_SHARE = 0.4   # replacements fitted new from the factory; the rest are the shop's rebuilt meters
# per lateral: a calibration offset shared by the lateral's meters (the batch it was tested against), and the scale of
# its tail spill
METER_OFFSET = {"L1": -0.000147, "L2": 0.0, "L3": -0.000292, "L4": 0.0, "L5": 0.0, "L6": 0.000263, "L7": 0.000229,
                "L8": 0.0, "L9": 0.000226}
SPILL_SCALE = {"L1": 1.00807, "L2": 1.00644, "L3": 1.0, "L4": 1.01765, "L5": 1.0, "L6": 1.00575, "L7": 1.0,
               "L8": 0.99074, "L9": 1.0065}


def clear_tie_in(W):
    """No water ran to the Lateral 5 tail turnouts while the connector was tied in: a 2026 set on one of them that
    touches 13 to 15 June moves to 16 June at the same hour."""
    moved = set(K.MOVED)
    for o in W.orders:
        if o["season"] != 2026 or o["turnout"] not in moved:
            continue
        if o["start"].date() <= TIE_IN[1] and o["end"].date() >= TIE_IN[0]:
            shift = dt.date(2026, 6, 16) - o["start"].date()
            o["start"] += shift
            o["end"] += shift


def turnout_flows_2026(W):
    """Per turnout, the delivered 2026 sets as (start, end, cfs)."""
    out = {t["id"]: [] for t in W.turnouts}
    for o in W.orders:
        if o["season"] == 2026 and o["status"] == "Delivered":
            out[o["turnout"]].append((o["start"], o["end"], o["cfs"]))
    for v in out.values():
        v.sort()
    return out


def volume_between(sets, a, b):
    """Acre-feet that ran through a turnout between datetimes a and b (cfs-hours over 12.1 is not exact; 1 cfs for
    one hour is 3,600 cubic feet)."""
    tot = 0.0
    for s, e, q in sets:
        lo, hi = max(s, a), min(e, b)
        if hi > lo:
            tot += q * (hi - lo).total_seconds() / K.CUFT_PER_AF
    return tot


def daily_volume(sets, day):
    a = dt.datetime(day.year, day.month, day.day)
    return volume_between(sets, a, a + dt.timedelta(days=1))


def lateral_on(t, when):
    """The lateral that fed a turnout at a datetime (the Lateral 5 tail from Lateral 6 after the tie-in)."""
    if t["moved"]:
        return "L5" if when < dt.datetime(2026, 6, 15, 12, 0) else "L6"
    return t["lateral_built"]


def build_meters(W):
    """Each turnout's meter at the start of 2026, the riders' weekly reads, the season's meter changes and the
    rollovers. Readings are the meter's own register: propeller meters in acre-feet to the hundredth, the 2025
    magnetic meters in hundreds of cubic feet."""
    r = K.rng("meters", ASK_SALT)
    flows = W.flows = turnout_flows_2026(W)
    meters, reads, changes = [], [], []
    used = set()

    def serial(kind):
        while True:
            s = ("P%05d" % int(r.integers(10000, 99999))) if kind == "P" else ("MG%06d" % int(r.integers(200000, 299999)))
            if s not in used:
                used.add(s)
                return s

    season_vol = {tid: volume_between(v, dt.datetime(2026, 1, 1), dt.datetime(2026, 12, 1)) for tid, v in flows.items()}
    # turnouts whose meter is changed in mid-season: two to five on every lateral, among turnouts that take water
    change_set = []
    for lat in K.LATERALS:
        cand = [t for t in W.turnouts if t["lateral_built"] == lat and season_vol[t["id"]] > 60 and t["meter_kind"] == "P"]
        k = {"L1": 4, "L2": 3, "L3": 2, "L4": 5, "L5": 4, "L6": 3, "L7": 3, "L8": 3, "L9": 4}[lat]
        idx = r.choice(len(cand), size=k, replace=False)
        change_set += [cand[int(i)]["id"] for i in sorted(idx)]
    rollover = []
    big = sorted([t for t in W.turnouts if t["meter_kind"] == "P" and t["id"] not in change_set],
                 key=lambda t: -season_vol[t["id"]])
    rollover = [t["id"] for t in big[1:20:3]][:6]
    W.change_set, W.rollover = change_set, rollover
    for t in W.turnouts:
        tid = t["id"]
        kind = t["meter_kind"]
        s0 = serial(kind)
        bias = float(r.normal(0, 0.012)) + METER_OFFSET[t["lateral_built"]]
        if kind == "P":
            cap, unit = 10000.0, "AF"
            reg0 = float(r.uniform(150, 9300))
            if tid in rollover:
                reg0 = 10000.0 - season_vol[tid] * float(r.uniform(0.25, 0.7))
            installed = dt.date(int(r.integers(2006, 2023)), int(r.integers(1, 13)), int(r.integers(1, 28)))
        else:
            cap, unit = 10000000.0, "HCF"
            reg0 = float(r.uniform(4000, 260000))
            installed = K.MAG_PROGRAM + dt.timedelta(days=int(r.integers(0, 40)))
        meters.append(dict(serial=s0, turnout=tid, kind=kind, units=unit, capacity=cap, installed=installed,
                           removed=None, bias=bias, reg0=reg0))
        cur = meters[-1]
        # read days: the lateral's route weekday, from the last one before the canal opens to the first after it closes
        sched = []
        lat_by_day = lambda d: lateral_on(t, dt.datetime(d.year, d.month, d.day, 12))
        d = dt.date(2026, 1, 19)
        while d <= dt.date(2026, 11, 13):
            lat = lat_by_day(d)
            if d.weekday() == K.ROUTE_DAY[lat]:
                sched.append(d)
            d += dt.timedelta(days=1)
        if t["moved"] and dt.date(2026, 6, 15) not in sched:
            sched.append(dt.date(2026, 6, 15))
            sched.sort()
        opening = max(x for x in sched if x <= dt.date(2026, 1, 31))
        closing = min(x for x in sched if x >= dt.date(2026, 11, 1))
        sched = [x for x in sched if opening <= x <= closing]
        # the riders miss a read now and then (never the opening, the closing or the tie-in read)
        keep = []
        for x in sched:
            if x not in (opening, closing, dt.date(2026, 6, 15)) and r.random() < 0.035:
                continue
            keep.append(x)
        ch = None
        if tid in change_set:
            # a weekday between two reads in May to September, at least two days from either
            inner = [x for x in keep if dt.date(2026, 5, 4) <= x <= dt.date(2026, 9, 25)]
            k0 = int(r.integers(0, len(inner) - 1))
            a, b = inner[k0], inner[k0 + 1]
            span = (b - a).days
            cd = a + dt.timedelta(days=int(r.integers(2, max(3, span - 1))))
            while cd.weekday() >= 5:
                cd -= dt.timedelta(days=1)
            ch = dt.datetime(cd.year, cd.month, cd.day, int(r.integers(9, 15)), int(r.choice([0, 15, 30, 45])))
        new_meter = None
        for x in keep:
            when = dt.datetime(x.year, x.month, x.day, int(r.integers(7, 16)), int(r.integers(0, 60)))
            if ch is not None and new_meter is None and when > ch:
                # the change: the shop's removal and installation reads
                vol_old = volume_between(flows[tid], dt.datetime(2026, 1, 1), ch) * (1 + cur["bias"])
                rem = cur["reg0"] + vol_old
                cur["removed"] = ch.date()
                # the replacement comes off the shop's shelf: a new meter goes in with its register at zero, a rebuilt
                # one with the register it carried out of its last service (the draw is kept for the stream either way)
                new_reg0 = float(r.uniform(300, 7400))
                unit = "New" if K.rng("meter-unit", tid).random() < NEW_METER_SHARE else "Rebuilt"
                if unit == "New":
                    new_reg0 = 0.0
                nm = dict(serial=serial("P"), turnout=tid, kind="P", units="AF", capacity=10000.0, installed=ch.date(),
                          removed=None, bias=float(r.normal(0, 0.012)) + METER_OFFSET[t["lateral_built"]], reg0=new_reg0,
                          since=ch, unit=unit)
                meters.append(nm)
                changes.append(dict(turnout=tid, when=ch, removed_serial=cur["serial"],
                                    removal=round(rem % cur["capacity"], 2), installed_serial=nm["serial"],
                                    installation=round(new_reg0, 2), unit=unit,
                                    reason=str(r.choice(["register stopped", "bearing worn, under-reading",
                                                         "propeller fouled", "register fogged", "annual test failed"]))))
                new_meter = nm
            m = new_meter or cur
            since = m.get("since", dt.datetime(2026, 1, 1))
            vol = volume_between(flows[tid], since, when) * (1 + m["bias"])
            if m["units"] == "AF":
                value = round((m["reg0"] + vol) % m["capacity"], 2)
            else:
                value = int(round((m["reg0"] + vol * 435.6) % m["capacity"]))
            reads.append(dict(turnout=tid, when=when, serial=m["serial"], value=value, units=m["units"],
                              lateral=lateral_on(t, when)))
    W.meters, W.reads, W.changes = meters, reads, changes


# the 2026 season's conveyance loss on each lateral (seepage and spill), as a share of the water put into it
LOSS_2026_BASE = {"L1": 0.072, "L2": 0.105, "L3": 0.064, "L4": 0.138, "L5": 0.091, "L6": 0.118, "L7": 0.083,
                  "L8": 0.097, "L9": 0.126}
LOSS_2026_FACTOR = {"L1": 1.20473, "L2": 0.93, "L3": 1.34788, "L4": 1.08295, "L5": 0.8835, "L6": 1.17353,
                    "L7": 0.96498, "L8": 1.27, "L9": 1.04}
WEIR = {  # crest length ft, crest gauge reading ft with no flashboards, coefficient (ft^0.5/s)
    "L1": (4.0, 1.18), "L2": (5.0, 1.42), "L3": (3.0, 0.96), "L4": (6.0, 1.55), "L5": (4.0, 1.21),
    "L6": (5.0, 1.36), "L7": (4.0, 1.09), "L8": (3.0, 1.12), "L9": (5.0, 1.47)}
WEIR_C = 3.33
BOARD_FT = 2.0 / 12.0
# flashboards in place: (date in, date out, boards)
BOARDS = {
    "L1": [(dt.date(2026, 5, 4), dt.date(2026, 9, 14), 1)],
    "L2": [(dt.date(2026, 4, 20), dt.date(2026, 9, 28), 1), (dt.date(2026, 7, 6), dt.date(2026, 8, 17), 1)],
    "L3": [(dt.date(2026, 6, 1), dt.date(2026, 8, 31), 1)],
    "L4": [(dt.date(2026, 4, 13), dt.date(2026, 10, 5), 1), (dt.date(2026, 6, 22), dt.date(2026, 9, 8), 1)],
    "L5": [(dt.date(2026, 5, 11), dt.date(2026, 9, 21), 1)],
    "L6": [(dt.date(2026, 5, 18), dt.date(2026, 10, 12), 1)],
    "L7": [(dt.date(2026, 6, 8), dt.date(2026, 9, 1), 1)],
    "L8": [(dt.date(2026, 4, 27), dt.date(2026, 8, 24), 1), (dt.date(2026, 7, 13), dt.date(2026, 8, 3), 1)],
    "L9": [(dt.date(2026, 5, 4), dt.date(2026, 9, 29), 1)],
}
ALTERNATE = {"L3": (dt.date(2026, 8, 3), dt.date(2026, 8, 29)), "L7": (dt.date(2026, 8, 3), dt.date(2026, 8, 29)),
             "L8": (dt.date(2026, 8, 4), dt.date(2026, 8, 28))}


def boards_on(lat, day):
    return sum(n for a, b, n in BOARDS[lat] if a <= day < b)


def build_laterals(W):
    """Each lateral's daily heading volume (what its turnouts took that day, its seepage and its spill, measured by
    the heading flume) and its tail weir's 07:00 readings with the riders' remarks. Seepage runs at a steady rate set
    so that the season's loss stands near the lateral's allowance (LOSS_2026_FACTOR)."""
    flows = W.flows
    W.headings, W.weir_rows, W.spill_true = [], [], {}
    est = {"L2": (dt.date(2026, 7, 21), 4), "L4": (dt.date(2026, 6, 2), 6), "L6": (dt.date(2026, 8, 10), 3),
           "L9": (dt.date(2026, 4, 14), 5)}
    days = K.season_days(2026)
    for lat in K.LATERALS:
        r_l = K.rng("lateral", lat, ASK_SALT)
        L, crest = WEIR[lat]
        spill_level = float(r_l.uniform(0.45, 1.3)) * SPILL_SCALE[lat]   # cfs, a lateral's typical tail spill
        deliv, q_spill, jit = [], [], []
        for d in days:
            dv = 0.0
            for t in W.turnouts:
                if lateral_on(t, dt.datetime(d.year, d.month, d.day, 12)) == lat:
                    dv += daily_volume(flows[t["id"]], d)
            deliv.append(dv)
            q = max(0.0, spill_level * float(r_l.lognormal(0, 0.45)) - (0.25 if r_l.random() < 0.12 else 0.0))
            if r_l.random() < 0.08:
                q = 0.0
            q_spill.append(q)
            jit.append(float(r_l.uniform(0.9, 1.1)))
        share = LOSS_2026_BASE[lat] * LOSS_2026_FACTOR[lat]
        target_loss = share / (1 - share) * sum(deliv)
        spill_af = sum(q * K.AF_PER_CFS_DAY for q in q_spill)
        seep_rate = max(0.5, (target_loss - spill_af) / sum(jit))
        e_days = set()
        if lat in est:
            s0, n = est[lat]
            e_days = {s0 + dt.timedelta(days=k) for k in range(n)}
        prev_boards = 0
        alt = ALTERNATE.get(lat)
        read_today = True
        r_note = K.rng("board-note", lat)     # the minutes between a board change and the reading after it
        for k, d in enumerate(days):
            true_in = deliv[k] + q_spill[k] * K.AF_PER_CFS_DAY + seep_rate * jit[k]
            meas = true_in * (1 + float(r_l.normal(0, 0.008)))
            q = "E" if d in e_days else ""
            if d in e_days:
                meas = true_in * (1 + float(r_l.normal(0, 0.03)))
            W.headings.append(dict(date=d, lateral=lat, af=round(meas, 2), quality=q))
            W.spill_true[(lat, d)] = q_spill[k]
            # the 07:00 reading at the tail weir
            nb = boards_on(lat, d)
            if alt and alt[0] <= d <= alt[1]:
                read_today = not read_today
            else:
                read_today = True
            crest_eff = crest + nb * BOARD_FT
            if q_spill[k] > 0:
                head = (q_spill[k] / (WEIR_C * L)) ** (2.0 / 3.0)
                gauge = crest_eff + head
            else:
                gauge = crest_eff - float(r_l.uniform(0.03, 0.25))
            remark = ""
            if nb != prev_boards:
                if nb > prev_boards:
                    remark = "set one 2-inch board" if prev_boards == 0 else "added a 2-inch board"
                else:
                    remark = "pulled boards" if nb == 0 else "pulled one board"
                read_today = True
            elif r_l.random() < 0.035:
                remark = str(r_l.choice(["trash on weir, cleaned", "tules cut back", "gauge board muddy, wiped",
                                         "low spill", "moss on crest"]))
            changed = nb != prev_boards
            prev_boards = nb
            if read_today:
                minute = int(r_l.integers(0, 50))
                if changed:
                    # the rider sets or pulls the board on arrival and notes the time, then reads the gauge
                    t = dt.datetime(d.year, d.month, d.day, 7, minute) - dt.timedelta(minutes=int(r_note.integers(3, 13)))
                    remark = "%s %s" % (t.strftime("%H:%M"), remark)
                W.weir_rows.append(dict(date=d, lateral=lat, time="07:%02d" % minute, gauge=round(gauge, 2),
                                        remarks=remark))



# ---------------------------------------------------------------------------------------------------- the 2027 requests

RANCH_A = ["Oak", "Sand", "Willow", "Cottonwood", "Quail", "Mesa", "Alder", "Sycamore", "Badger", "Heron", "Juniper",
           "Larkspur", "Mill", "Orchard", "Pioneer", "Redbud", "Sage", "Tule", "Valley", "Walnut", "Yokohl", "Granite",
           "Fairview", "Kettle", "Lone Pine", "Magpie", "North Fork", "Plover", "Rush", "Sunflower"]
RANCH_B = ["Ranch", "Farms", "Orchards", "Vineyards", "Ranch Co.", "Farming", "Family Farms", "Land Co."]


def _pick(rm, options, weights=None):
    p = None if weights is None else np.array(weights, dtype=float) / float(sum(weights))
    return str(options[int(rm.choice(len(options), p=p))])


def _revision_remark(v1, f, rm):
    """The clerk's note on a revised request says what the grower revised."""
    meth = f["method"].lower()
    if v1["method"] != f["method"]:
        note = _pick(rm, ["converted to %s for 2027" % meth, "changed to %s" % meth, "method corrected to %s" % meth])
        if abs(v1["acres"] - f["acres"]) >= 0.005 and rm.random() < 0.5:
            note += ", acres corrected"
        return note
    if f["acres"] < v1["acres"]:
        return _pick(rm, ["acreage corrected", "acres corrected, roads and ditch banks out", "revised by grower",
                          "corrected acres per county permit", "acres reduced per grower's survey"], [5, 2, 2, 1, 1])
    return _pick(rm, ["acreage corrected", "revised by grower", "corrected acres per county permit",
                      "acres corrected, block left off first filing"], [5, 2, 1, 1])


def _request_remark(f, growers, rm):
    """Most requests carry no remark; a changed irrigation system or an account matter gets one."""
    meth = f["method"].lower()
    if f["method_2026"] != f["method"] and rm.random() < 0.75:
        if f["method"] == "Border":
            return _pick(rm, ["back to border for 2027", "sprinklers pulled, border 2027"])
        return _pick(rm, ["converted to %s for 2027" % meth, "changed to %s" % meth, "new %s system" % meth])
    if rm.random() < 0.06:
        other = "%s %s" % (_pick(rm, RANCH_A), _pick(rm, RANCH_B))
        return _pick(rm, ["new owner, account transferred", "leased to %s" % other, "orders through the farm manager",
                          "billing to farm manager", "call grower before ordering", "gate key with the rider",
                          "phone number changed", "mailing address changed"], [3, 2, 2, 2, 2, 1, 2, 1])
    return ""


def _withdrawal_remark(f, rm):
    if f["crop"] in ("ALM", "PIS", "WAL", "CIT"):
        return _pick(rm, ["orchard to be pulled", "orchard to be pushed", "grower withdrew",
                          "trees coming out, replant 2028"], [3, 1, 2, 1])
    if f["crop"] == "GRW":
        return _pick(rm, ["vineyard to be pulled", "grower withdrew", "vines coming out"], [3, 2, 1])
    return _pick(rm, ["fallowing 2027", "grower withdrew", "field sold, new owner to file", "out of production 2027"],
                 [3, 2, 1, 1])


def build_requests(W):
    """Each turnout's grower files one request per field. A grower who changed a field's irrigation method for 2027
    or corrected its acres filed a second version; a few withdrew. Every field took water in 2026 and keeps its crop."""
    r = K.rng("request-rows")
    growers = {}
    for t in W.turnouts:
        a = RANCH_A[int(r.integers(len(RANCH_A)))]
        b = RANCH_B[int(r.integers(len(RANCH_B)))]
        growers[t["id"]] = ("G-%04d" % int(r.integers(1100, 9800)), "%s %s" % (a, b))
    rows = []
    k = 0
    for f in sorted(W.fields, key=lambda f: (f["turnout"], f["id"])):
        acct, ranch = growers[f["turnout"]]
        # 2026 attributes: about one field in twenty changed its method for 2027
        f["method_2026"] = f["method"]
        f["acres_2026"] = f["acres"]
        if r.random() < 0.05:
            other = [m for m in K.METHOD_BY_CROP[f["crop"]] if m != f["method"]]
            if other:
                f["method_2026"] = other[0]
        received = K.REQUESTS_OPEN + dt.timedelta(days=int(r.integers(0, 55)))
        k += 1
        base = dict(acct=acct, ranch=ranch, field=f["id"], turnout=f["turnout"], crop=f["crop"])
        rm = K.rng("request-remarks", f["id"])     # the clerk's remark, on its own stream
        if f["req_status"] == "accepted" and f["revised"]:
            v1 = dict(base, no="R27-%04d" % (1000 + k), version=1, status="Superseded", received=received,
                      method=f["method_2026"] if f["method_2026"] != f["method"] else f["method"],
                      acres=round(f["acres"] * float(r.choice([0.9, 0.95, 1.05, 1.1])), 2), remarks="")
            if v1["method"] == f["method"] and abs(v1["acres"] - f["acres"]) < 0.005:
                v1["acres"] = round(f["acres"] + 2.5, 2)
            rows.append(v1)
            r.choice(["acreage corrected", "method changed", "revised by grower"])   # keeps the row stream's draws
            rows.append(dict(base, no="R27-%04d" % (1000 + k), version=2, status="Accepted",
                             received=received + dt.timedelta(days=int(r.integers(3, 30))), method=f["method"],
                             acres=f["acres"], remarks=_revision_remark(v1, f, rm)))
        elif f["req_status"] == "accepted":
            rows.append(dict(base, no="R27-%04d" % (1000 + k), version=1, status="Accepted", received=received,
                             method=f["method"], acres=f["acres"], remarks=_request_remark(f, growers, rm)))
        elif f["req_status"] == "withdrawn":
            r.choice(["fallowing 2027", "orchard to be pulled", "grower withdrew"])   # keeps the row stream's draws
            rows.append(dict(base, no="R27-%04d" % (1000 + k), version=1, status="Withdrawn", received=received,
                             method=f["method"], acres=f["acres"], remarks=_withdrawal_remark(f, rm)))
    for x in rows:
        if x["received"] > K.REQUESTS_CLOSE:
            x["received"] = K.REQUESTS_CLOSE - dt.timedelta(days=int(r.integers(0, 4)))
    W.requests = rows
