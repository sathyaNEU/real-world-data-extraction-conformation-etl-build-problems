"""The district's customers and outages, October 2020 to September 2026.

Customers are metered points behind distribution transformers; each transformer hangs off a lateral fuse or
straight off a feeder's main line, which the breaker and three automated switches cut into a trunk and three
branches. Every outage is generated with its restoration steps; the outage export and the step file are cut from
the same records, so each customer's own restoration time is recoverable from the files."""
import datetime as dt
import math

import numpy as np

import world as W

GO_LIVE = dt.date(2014, 11, 9)              # connectivity model go-live: every existing meter row starts here
METERS = {"HR12": 3920, "HR14": 3131, "ML03": 4210, "ML07": 3602, "QH21": 2808, "QH22": 3347, "SP05": 3690,
          "SP09": 3399}
LATERAL_METERS = 412
EXCHANGE = {"HR12": (dt.date(2026, 2, 2), dt.date(2026, 4, 24)), "HR14": (dt.date(2026, 2, 9), dt.date(2026, 5, 1)),
            "QH21": (dt.date(2026, 4, 6), dt.date(2026, 7, 17)), "QH22": (dt.date(2026, 4, 13), dt.date(2026, 7, 24))}
EXCHANGE_SHARE = 0.62
# outages a year per feeder, ordinary causes (the cable failures in the work orders add their own)
FUSE_RATE = {"HR12": 7, "HR14": 8, "ML03": 9, "ML07": 7, "QH21": 6, "QH22": 6, "SP05": 8, "SP09": 6}
BRANCH_RATE = {"HR12": 0.7, "HR14": 0.8, "ML03": 0.9, "ML07": 0.8, "QH21": 0.6, "QH22": 0.6, "SP05": 0.8, "SP09": 0.5}
BANK_RATE = {"HRD": 0.35, "MLN": 0.4, "QHL": 0.3, "SPK": 0.35}
CABLE_ON_LATERAL = 0.9
FLISR_OK = 0.9


class Topo:
    pass


_SEEN = set()


def _meter_ids(rng, n):
    out = []
    while len(out) < n:
        x = int(rng.integers(40_000_000, 49_999_999))
        if x not in _SEEN:
            _SEEN.add(x)
            out.append("%d%02d" % (x, x % 97))
    return out


def topology(seed=W.SEED + 1):
    rng = np.random.default_rng(seed)
    _SEEN.clear()
    t = Topo()
    t.devices = {}         # device_id -> dict(type, feeder, parent, in_from, in_to, branch)
    t.meter_rows = []      # dict(meter_id, serial, transformer_id, device_id, feeder_id, eff_from, eff_to)
    t.fuses = {}           # feeder -> list of fuse ids (in service now)
    t.branch_heads = {}
    fuse_no = [310_000]
    tx_no = [5_100_000]
    serial_no = [70_000_000]

    def nxt(c, lo, hi):
        c[0] += int(rng.integers(lo, hi + 1))
        return c[0]

    for sub, sname, feeders in W.SUBSTATIONS:
        bank = "%s-TB1" % sub
        t.devices[bank] = dict(type="TRANSFORMER BANK", feeder=None, parent=None, sub=sub, branch=None,
                               in_from=None, in_to=None)
        for f in feeders:
            cb = "CB-%s" % f
            t.devices[cb] = dict(type="FEEDER BREAKER", feeder=f, parent=bank, sub=sub, branch=0, in_from=None,
                                 in_to=None)
            heads = {0: cb}
            for b in (1, 2, 3):
                a = "AS-%s-%d" % (f, b)
                t.devices[a] = dict(type="AUTOMATED SWITCH", feeder=f, parent=cb, sub=sub, branch=b, in_from=None,
                                    in_to=None)
                heads[b] = a
            t.branch_heads[f] = heads
            t.fuses[f] = []
            n = METERS[f]
            n_fuse = int(round(n / 72))
            fuse_list = []
            for i in range(n_fuse):
                b = int(rng.choice([0, 1, 2, 3], p=[0.16, 0.30, 0.30, 0.24]))
                fid = "FU-%06d" % nxt(fuse_no, 1, 9)
                t.devices[fid] = dict(type="FUSE", feeder=f, parent=heads[b], sub=sub, branch=b, in_from=None,
                                      in_to=None, weight=float(rng.gamma(2.2, 1 / 2.2)))
                fuse_list.append(fid)
                t.fuses[f].append(fid)
            # meters: about 82 per cent behind lateral fuses, the rest on main-line transformers
            ids = _meter_ids(rng, n)
            k = 0
            while k < n:
                per_tx = int(rng.integers(3, 13))
                if rng.random() < 0.82:
                    dev = fuse_list[int(rng.integers(len(fuse_list)))]
                else:
                    dev = heads[int(rng.choice([0, 1, 2, 3], p=[0.25, 0.27, 0.27, 0.21]))]
                tx = "T%07d" % nxt(tx_no, 1, 6)
                for m in ids[k:k + per_tx]:
                    t.meter_rows.append(dict(meter_id=m, serial="%d" % nxt(serial_no, 1, 40), transformer_id=tx,
                                             device_id=dev, feeder_id=f, eff_from=GO_LIVE, eff_to=None))
                k += per_tx
    # connection dates: meters added since go-live (new services), a few removals (demolitions)
    rows = t.meter_rows
    for r in rows:
        u = rng.random()
        if u < 0.105:
            r["eff_from"] = GO_LIVE + dt.timedelta(days=int(rng.integers(30, (dt.date(2026, 9, 20) - GO_LIVE).days)))
    for r in rows:
        if r["eff_from"] == GO_LIVE and rng.random() < 0.012:
            # removed before the reliability year being reported, so the asked year has no removals
            r["eff_to"] = GO_LIVE + dt.timedelta(days=int(rng.integers(200, (dt.date(2025, 9, 1) - GO_LIVE).days)))
    # the Mill Lane 3 lateral moved to Mill Lane 7 on 14 June 2026: a new fuse on Mill Lane 7, the old one retired
    old_fuse = "FU-%06d" % nxt(fuse_no, 1, 9)
    t.devices[old_fuse] = dict(type="FUSE", feeder="ML03", parent=t.branch_heads["ML03"][3], sub="MLN", branch=3,
                               in_from=None, in_to=W.LATERAL_MOVE, weight=1.3)
    new_fuse = "FU-%06d" % (fuse_no[0] + 4113)
    t.devices[new_fuse] = dict(type="FUSE", feeder="ML07", parent=t.branch_heads["ML07"][2], sub="MLN", branch=2,
                               in_from=W.LATERAL_MOVE, in_to=None, weight=1.3)
    t.lateral = (old_fuse, new_fuse)
    lat_ids = _meter_ids(rng, LATERAL_METERS)
    k = 0
    while k < LATERAL_METERS:
        per_tx = int(rng.integers(4, 11))
        tx = "T%07d" % nxt(tx_no, 1, 6)
        for m in lat_ids[k:k + per_tx]:
            ser = "%d" % nxt(serial_no, 1, 40)
            rows.append(dict(meter_id=m, serial=ser, transformer_id=tx, device_id=old_fuse, feeder_id="ML03",
                             eff_from=GO_LIVE, eff_to=W.LATERAL_MOVE))
            rows.append(dict(meter_id=m, serial=ser, transformer_id=tx, device_id=new_fuse, feeder_id="ML07",
                             eff_from=W.LATERAL_MOVE, eff_to=None))
        k += per_tx
    # 2026 meter exchange on the Harrow Road and Quarry Hill feeders: same metered point, new meter serial
    extra = []
    for r in rows:
        f = r["feeder_id"]
        if f in EXCHANGE and r["eff_to"] is None and r["eff_from"] < EXCHANGE[f][0] and rng.random() < EXCHANGE_SHARE:
            lo, hi = EXCHANGE[f]
            d = lo + dt.timedelta(days=int(rng.integers(0, (hi - lo).days + 1)))
            new = dict(r)
            new["serial"] = "%d" % (int(r["serial"]) + 30_000_000)
            new["eff_from"] = d
            r["eff_to"] = d
            extra.append(new)
    rows.extend(extra)
    # new developments: a subdivision, an apartment block or a commercial park comes on as whole transformers within a
    # few weeks (drawn apart from the rest, and all before the 2025-26 reliability year, so that year's rows stand)
    dev_rng = np.random.default_rng(seed + 50)
    by_m = {}
    for r in rows:
        by_m.setdefault(r["meter_id"], []).append(r)
    by_tx = {}
    for m, rs_ in by_m.items():
        rs_.sort(key=lambda r: r["eff_from"])
        by_tx.setdefault((rs_[0]["feeder_id"], rs_[0]["transformer_id"]), []).append(rs_)
    for f in W.FEEDERS:
        txs = sorted(tx for (ff, tx), ms in by_tx.items() if ff == f and all(
            rs_[-1]["eff_to"] is None and rs_[0]["eff_from"] < dt.date(2025, 6, 1) and
            all(r["feeder_id"] == f for r in rs_) for rs_ in ms))
        for _ in range(int(dev_rng.integers(2, 5))):
            day = dt.date(int(dev_rng.integers(2017, 2026)), int(dev_rng.integers(1, 13)), int(dev_rng.integers(1, 29)))
            if day >= dt.date(2025, 6, 1):
                day = day.replace(year=2024)
            size = int(dev_rng.integers(3, 11))
            start = int(dev_rng.integers(0, len(txs) - size))
            for tx in txs[start:start + size]:
                d = day + dt.timedelta(days=int(dev_rng.integers(0, 45)))
                for rs_ in by_tx[(f, tx)]:
                    rs_[0]["eff_from"] = d
            del txs[start:start + size]
    return t


def meters_at(t, day):
    """meter_id -> (device_id, feeder_id) for the rows in effect on a day (eff_from <= day < eff_to)."""
    out = {}
    for r in t.meter_rows:
        if r["eff_from"] <= day and (r["eff_to"] is None or day < r["eff_to"]):
            out[r["meter_id"]] = (r["device_id"], r["feeder_id"])
    return out


def chain(t, dev):
    out = []
    while dev is not None:
        out.append(dev)
        dev = t.devices[dev]["parent"]
    return out


CAUSES_FUSE = ["UG FAULT", "UG FAULT", "UG FAULT", "EQUIPMENT", "ANIMAL", "VEHICLE", "UNKNOWN", "DIG-IN"]
CAUSES_BRANCH = ["UG FAULT", "UG FAULT", "EQUIPMENT", "UNKNOWN"]


def _lognorm_minutes(rng, median, sigma, lo, hi):
    return float(min(max(median * math.exp(rng.normal(0, sigma)), lo), hi))


def outages(t, cable_events, d0=W.OMS_START, forced=(), seed=W.SEED + 2):
    """cable_events: list of (date, feeder at the time, cause) for the work orders from October 2020 (cable-condition
    and dig-ins); each gets an underground fault outage on its feeder that day. Returns a list of outage dicts with
    start (aware local datetime), device, feeders and steps [(restoring_device, aware datetime)]."""
    R = [None]
    out = []
    d1 = W.CUT
    days = (d1 - d0).days + 1
    storms = storm_days()

    def live_fuses(f, day):
        return [x for x in t.fuses[f] + [t.lateral[0], t.lateral[1]]
                if t.devices[x]["feeder"] == f and (t.devices[x]["in_from"] is None or t.devices[x]["in_from"] <= day)
                and (t.devices[x]["in_to"] is None or day < t.devices[x]["in_to"])]

    def start_time(day, lo_h=0.0, hi_h=24.0):
        while True:
            h = float(R[0].uniform(lo_h, hi_h))
            st = dt.datetime.combine(day, dt.time(0)) + dt.timedelta(minutes=round(h * 60))
            if st.date() != day:
                continue
            aware = st.replace(tzinfo=W.LOCAL)
            # no start inside a daylight-saving change hour and none in the hour of the ADMS cutover
            back = aware.astimezone(W.UTC).astimezone(W.LOCAL).replace(tzinfo=None)
            if back != st or aware.fold:
                continue
            if day.month == 11 and day.weekday() == 6 and day.day <= 7 and 0 <= st.hour <= 2:
                continue
            if abs((aware - W.ADMS_CUTOVER).total_seconds()) < 6 * 3600:
                continue
            return aware

    def fuse_outage(f, day, cause, storm=False, at=None, dev=None):
        fl = live_fuses(f, day)
        w = np.array([t.devices[x].get("weight", 1.0) for x in fl])
        pick = fl[int(R[0].choice(len(fl), p=w / w.sum()))]
        dev = dev or pick
        st = at or start_time(day)
        dur = _lognorm_minutes(R[0], 140 if storm else 92, 0.6, 22, 900)
        return dict(start=st, device=dev, feeders=[f], cause=cause, steps=[(dev, st + dt.timedelta(minutes=round(dur)))])

    def branch_outage(f, day, cause, storm=False, at=None):
        heads = t.branch_heads[f]
        b = int(R[0].integers(1, 4))
        st = at or start_time(day)
        cb = heads[0]
        if R[0].random() < FLISR_OK:
            s1 = R[0].uniform(0.9, 3.4)
            dur = _lognorm_minutes(R[0], 150 if storm else 112, 0.5, 35, 720)
            steps = [(cb, st + dt.timedelta(seconds=round(s1 * 60))), (heads[b], st + dt.timedelta(minutes=round(dur)))]
        else:
            s1 = _lognorm_minutes(R[0], 48, 0.3, 24, 95)
            dur = s1 + _lognorm_minutes(R[0], 85, 0.5, 30, 600)
            steps = [(cb, st + dt.timedelta(minutes=round(s1))), (heads[b], st + dt.timedelta(minutes=round(dur)))]
        return dict(start=st, device=cb, feeders=[f], cause=cause, steps=steps)

    def bank_outage(sub, day, at=None):
        feeders = [fs for s, _, fs in W.SUBSTATIONS if s == sub][0]
        st = at or start_time(day)
        a = _lognorm_minutes(R[0], 17, 0.3, 9, 35)
        b = a + _lognorm_minutes(R[0], 6, 0.4, 2, 14)
        order = list(feeders) if R[0].random() < 0.5 else list(reversed(feeders))
        steps = [("CB-%s" % order[0], st + dt.timedelta(minutes=round(a))),
                 ("CB-%s" % order[1], st + dt.timedelta(minutes=round(b)))]
        return dict(start=st, device="%s-TB1" % sub, feeders=list(feeders), cause="SUBSTATION", steps=steps)

    forced_by_day = {}
    for day, kind, who, hour in forced:
        forced_by_day.setdefault(day, []).append((kind, who, hour))
    ev_by_day = {}
    for d, f, c in cable_events:
        ev_by_day.setdefault(d, []).append((f, c))
    for i in range(days):
        day = d0 + dt.timedelta(days=i)
        R[0] = np.random.default_rng([seed, day.toordinal()])
        for f, c in ev_by_day.get(day, []):
            if c == "TPD":
                out.append(fuse_outage(f, day, "DIG-IN"))
            elif R[0].random() < CABLE_ON_LATERAL:
                out.append(fuse_outage(f, day, "UG FAULT"))
            else:
                out.append(branch_outage(f, day, "UG FAULT"))
        for kind, who, hour in forced_by_day.get(day, []):
            at = dt.datetime.combine(day, dt.time(int(hour), int(round((hour % 1) * 60)))).replace(tzinfo=W.LOCAL)
            if kind == "bank":
                out.append(bank_outage(who, day, at=at))
            elif kind == "branch":
                out.append(branch_outage(who, day, "EQUIPMENT", at=at))
            elif kind == "lateral":
                # the Mill Lane lateral's own fuse: the Mill Lane 3 fuse before the June 2026 transfer, then Mill Lane 7's
                f = "ML03" if day < W.LATERAL_MOVE else "ML07"
                out.append(fuse_outage(f, day, "UG FAULT", at=at, dev=t.lateral[0] if f == "ML03" else t.lateral[1]))
            elif kind == "pocket":
                # a lateral that keeps blowing its fuse: the feeder's most exposed fuse
                fl = live_fuses(who, day)
                dev = max(fl, key=lambda x: (t.devices[x].get("weight", 1.0), x))
                out.append(fuse_outage(who, day, "UNKNOWN", at=at, dev=dev))
            else:
                out.append(fuse_outage(who, day, "UNKNOWN", at=at))
        if day in storms:
            spec = storms[day]
            for f in W.FEEDERS:
                for _ in range(int(R[0].poisson(spec["fuse"]))):
                    at = start_time(day, *spec["hours"])
                    out.append(fuse_outage(f, day, "WEATHER", storm=True, at=at))
                for _ in range(int(R[0].poisson(spec["branch"]))):
                    at = start_time(day, *spec["hours"])
                    out.append(branch_outage(f, day, "WEATHER", storm=True, at=at))
            continue
        for f in W.FEEDERS:
            if R[0].random() < FUSE_RATE[f] / 365.25:
                out.append(fuse_outage(f, day, str(R[0].choice(CAUSES_FUSE[3:]))))
            if R[0].random() < BRANCH_RATE[f] / 365.25:
                out.append(branch_outage(f, day, str(R[0].choice(CAUSES_BRANCH[2:]))))
        for sub, _, _ in W.SUBSTATIONS:
            if R[0].random() < BANK_RATE[sub] / 365.25 and day < W.RY_ASK[0]:
                out.append(bank_outage(sub, day))
    out.sort(key=lambda o: (o["start"], o["device"]))
    return out


def storm_days():
    """The district's storms, local days, with the hours they ran and the outages a feeder takes."""
    S = {}

    def add(d, fuse, branch, hours=(0.0, 24.0)):
        S[d] = dict(fuse=fuse, branch=branch, hours=hours)
    add(dt.date(2020, 11, 15), 3, 0.7, (13, 23))
    add(dt.date(2021, 6, 30), 4, 0.8, (14, 22))
    add(dt.date(2021, 9, 1), 5, 1.0, (8, 23))          # remnants of a hurricane
    add(dt.date(2022, 2, 4), 3, 0.75, (2, 18))
    add(dt.date(2022, 7, 21), 3, 0.6, (15, 21))
    add(dt.date(2023, 4, 1), 3, 0.7, (10, 20))
    add(dt.date(2023, 8, 8), 4, 0.85, (13, 22))
    add(dt.date(2024, 1, 10), 3, 0.75, (0, 14))
    add(dt.date(2024, 7, 16), 3, 0.7, (15, 22))
    add(dt.date(2025, 2, 16), 3, 0.65, (3, 17))
    add(dt.date(2025, 6, 19), 3, 0.8, (14, 23))
    add(dt.date(2026, 1, 25), 4, 0.9, (1, 19))          # ice storm, legacy outage system
    add(dt.date(2026, 7, 28), 3, 0.75, (16.5, 23.8))    # evening thunderstorm, ADMS
    return S
