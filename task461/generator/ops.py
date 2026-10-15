"""Redrock Draw's operation from its commercial operation date to the pulls, and the records three systems kept of it.

The dispatch: one day-ahead cycle on each operating day whose spread at the node reached the 2026 threshold (charge in
the four lowest-priced hours before the four highest-priced ones, discharge in those four), Cordell's two capacity
tests, a transformer trip and a power conversion fault, and two evenings MPI instructed the battery to discharge in
real time. The records: the battery management system's hourly export (UTC, hour beginning; the site gateway's
cellular link drops a few times a month and the portal fills what it missed with zero energy and the last state it
saw), the revenue meter's fifteen-minute data (UTC, interval ending) and the day-ahead settlement statement lines."""
import datetime as dt

import numpy as np

import market as MK
import world as W

UTC0 = dt.datetime(2026, 1, 1)
UTC_END = dt.datetime(2026, 11, 3)
H = int((UTC_END - UTC0).total_seconds() // 3600)
DIS_AC = 95.8                     # MW day-ahead discharge award at the node, four hours
CHG_AC = 113.4                    # MW day-ahead charge award at the node, four hours
CELL = 0.9200                     # stored per DC MWh charged
USABLE = [(dt.datetime(2025, 12, 1), 412.6), (dt.datetime(2026, 3, 12, 22), 408.9), (dt.datetime(2026, 9, 14, 22), 404.7)]
MEASURED = {W.TESTS[0]: 408.9, W.TESTS[1]: 404.7}
OUTAGES = {dt.date(2026, 5, 27): "FAULT", dt.date(2026, 8, 17): "FAULT", dt.date(2026, 8, 18): "MAINT",
           dt.date(2026, 8, 19): "MAINT", dt.date(2026, 8, 20): "MAINT"}
EMERGENCY = [dt.date(2026, 1, 27), dt.date(2026, 8, 27)]
REPRICED = {dt.date(2026, 7, 20): 1.085, dt.date(2026, 7, 21): 1.062}    # the initial statements' evening node prices
FEE = 0.275                       # MPI's day-ahead administrative fee, $ per MWh of day-ahead energy
INITIAL_LAG = 2
FINAL_LAG = 31


def hidx(t):
    return int((t - UTC0).total_seconds() // 3600)


def usable_at(t):
    u = USABLE[0][1]
    for when, v in USABLE:
        if t >= when:
            u = v
    return u


def published_node(days):
    """The node's prices as MPI published them: at the hub's price until the network model carried the resource."""
    for x in days:
        if W.NODE_CREATED <= x["day"] < W.NODE_PROVISIONAL_END:
            x["node_pub"] = x["hub"].copy()
        else:
            x["node_pub"] = x["node"]
    return days


def award_hours(prices):
    """The day-ahead cycle the QSE offers: discharge in the four highest-priced hours, charge in the four lowest-priced
    hours before the first of them."""
    p = np.asarray(prices, dtype=float)
    dis = sorted(np.argsort(-p, kind="stable")[:4].tolist())
    before = list(range(dis[0]))
    if len(before) < 4:
        raise RuntimeError("no room to charge before the discharge")
    chg = sorted(sorted(before, key=lambda i: (p[i], i))[:4])
    return chg, dis


def local_hour(d, clock, hrs):
    """UTC start of the local clock hour `clock` on operating day d."""
    for hr in hrs:
        if hr[2] == clock and not hr[1]:
            return MK.hour_start_utc(d, hr)
    raise KeyError(clock)


def operate(days, seed=W.SEED + 21, seed_dc=W.SEED + 64):
    """Physical flows by UTC hour (MWh in the hour) and a record per operating day."""
    rng = np.random.default_rng(seed)
    rng_dc = np.random.default_rng(seed_dc)
    rng_aw = np.random.default_rng(seed + 4)        # the QSE's awards move a little with its loss forecast
    byday = {x["day"]: x for x in days}
    doy = np.array([(UTC0 + dt.timedelta(hours=k)).timetuple().tm_yday for k in range(H)])
    season = np.cos(2 * np.pi * (doy - 200) / 365)
    conv = 0.962 * (1 + 0.004 * season + rng.normal(0, 0.0012, H))            # DC to the meter side, by hour
    aux = 0.32 + 0.18 * np.clip(season, 0, None) + rng.normal(0, 0.03, H)       # station load, MW
    mode = np.array(["IDLE"] * H, dtype=object)
    dayrec = {}
    d = W.COD
    while d <= W.ARCHIVE_PULL:
        x = byday[d]
        hrs = x["hours"]
        sp = MK.tb4(x["node_pub"])
        rec = dict(day=d, spread=sp, status="idle", chg=[], dis=[])
        start = [MK.hour_start_utc(d, h) for h in hrs]
        if d in W.TESTS:
            post = local_hour(d, 6, hrs) >= W.FIRMWARE
            code = "MAINT" if post else "TEST"
            rec.update(status="test", code=code, measured=MEASURED[d])
            rec["chg_k"] = [hidx(local_hour(d, c, hrs)) for c in range(6, 11)]
            rec["rest_k"] = [hidx(local_hour(d, 11, hrs))]
            rec["dis_k"] = [hidx(local_hour(d, c, hrs)) for c in range(12, 17)]
        elif d in OUTAGES:
            rec.update(status="outage", code=OUTAGES[d])
            rec["k"] = [hidx(t) for t in start]
        elif d in EMERGENCY:
            rec.update(status="emergency")
            rec["chg_k"] = [hidx(local_hour(d, c, hrs)) for c in range(13, 17)]
            rec["dis_k"] = [hidx(local_hour(d, c, hrs)) for c in range(18, 22)]
        elif sp >= W.SETTING_2026:
            chg, dis = award_hours(x["node_pub"])
            rec.update(status="cycle", chg=chg, dis=dis,
                       chg_mw=round(CHG_AC * (1 + rng_aw.normal(0, 0.004)), 1),
                       dis_mw=round(DIS_AC * (1 + rng_aw.normal(0, 0.004)), 1))
            rec["chg_k"] = [hidx(start[i]) for i in chg]
            rec["dis_k"] = [hidx(start[i]) for i in dis]
        dayrec[d] = rec
        d += dt.timedelta(days=1)

    dc_chg = np.zeros(H); dc_dis = np.zeros(H); ac_chg = np.zeros(H); ac_dis = np.zeros(H)
    test_dis = np.zeros(H)
    for d, r in sorted(dayrec.items()):
        if r["status"] in ("cycle", "emergency"):
            cmw = r.get("chg_mw", CHG_AC)
            for k in r["chg_k"]:
                if 0 <= k < H:
                    ac_chg[k] = cmw - aux[k]
                    dc_chg[k] = ac_chg[k] * conv[k]
                    mode[k] = "CHARGE"
            stored = sum((cmw - aux[k]) * conv[k] if 0 <= k < H else (cmw - 0.4) * 0.962
                         for k in r["chg_k"]) * CELL
            stored *= 1 + rng_dc.normal(0, 0.0015)
            r["dc"] = stored
            for k in r["dis_k"]:
                if 0 <= k < H:
                    dc_dis[k] = stored / 4.0
                    ac_dis[k] = dc_dis[k] * conv[k]
                    mode[k] = "DISCHARGE"
        elif r["status"] == "test":
            m = r["measured"]
            for k in r["chg_k"]:
                dc_chg[k] = m / CELL / 5.0
                ac_chg[k] = dc_chg[k] / conv[k]
                mode[k] = r["code"]
            for k in r["rest_k"]:
                mode[k] = r["code"]
            rem = m
            for k in r["dis_k"]:
                e = min(100.0, rem)
                dc_dis[k] = e
                ac_dis[k] = e * conv[k]
                test_dis[k] = e
                mode[k] = r["code"]
                rem -= e
            r["dc"] = m
        elif r["status"] == "outage":
            for k in r["k"]:
                if 0 <= k < H:
                    mode[k] = r["code"]
    for k in range(H):                       # the new firmware's weekly self-test (no energy), logged as TEST
        t = UTC0 + dt.timedelta(hours=k)
        if t >= W.FIRMWARE + dt.timedelta(hours=2) and t.weekday() == 6 and t.hour == 9 and mode[k] == "IDLE":
            mode[k] = "TEST"
    E = 0.0
    efc = 7.413                              # commissioning cycles counted before the export opens
    soc = np.zeros(H); cnt = np.zeros(H)
    for k in range(H):
        u = usable_at(UTC0 + dt.timedelta(hours=k))
        E = min(u, E + dc_chg[k] * CELL)
        E = max(0.0, E - dc_dis[k])
        efc += dc_dis[k] / u
        soc[k] = 100.0 * E / u
        cnt[k] = efc
    # the revenue meter at the point of interconnection nets the station's auxiliary load
    delivered = np.maximum(ac_dis - aux * (ac_dis > 0), 0.0)
    received = ac_chg + aux * (ac_dis == 0)
    phys = dict(dc_chg=dc_chg, dc_dis=dc_dis, ac_chg=ac_chg, ac_dis=ac_dis, mode=mode, soc=soc, efc=cnt, aux=aux,
                conv=conv, test_dis=test_dis, delivered=delivered, received=received)
    return dayrec, phys


def dropouts(dayrec, phys, seed=W.SEED + 23):
    """The gateway's dropped spans (UTC hour index from, to): a few a month, two to nine hours; each month at least
    one catches part of an evening discharge; none touches a capacity test."""
    rng = np.random.default_rng(seed)
    dis = phys["dc_dis"]
    guard = set()
    for r in dayrec.values():
        if r["status"] == "test":
            for k in r["chg_k"] + r["dis_k"]:
                guard.update(range(k - 4, k + 5))
    drops = []
    for m in range(1, 11):
        ms = hidx(dt.datetime(2026, m, 1, 6))
        me = hidx(dt.datetime(2026, m + 1, 1, 5))
        n = 2 + int(rng.poisson(1.2))
        month, got, tries = [], False, 0
        while len(month) < n or not got:
            tries += 1
            if tries > 2000:
                raise RuntimeError("no dropout schedule for month %d" % m)
            if len(month) >= n:
                ks = [k for k in range(ms, me) if dis[k] > 0 and k not in guard]
                k = int(rng.choice(ks))
                a = k - int(rng.integers(0, 3))
                b = a + int(rng.integers(2, 6))
            else:
                a = ms + int(rng.integers(0, me - ms - 10))
                b = a + int(rng.integers(2, 10))
            if any(k in guard for k in range(a, b)):
                continue
            if any(not (b + 6 <= a2 or b2 + 6 <= a) for a2, b2 in drops + month):
                continue
            month.append((a, b))
            if dis[a:b].sum() > 0:
                got = True
        drops.extend(month)
    return sorted(drops)


def bms_view(phys, drops):
    """What the portal export shows: zero energy and the last state seen in the dropped hours."""
    v = {k: np.array(phys[k], dtype=object if k == "mode" else float) for k in
         ("dc_chg", "dc_dis", "ac_chg", "ac_dis", "soc", "efc", "mode")}
    lost = np.zeros(H, dtype=bool)
    for a, b in drops:
        lost[a:b] = True
        for k in range(a, b):
            for c in ("dc_chg", "dc_dis", "ac_chg", "ac_dis"):
                v[c][k] = 0.0
            for c in ("soc", "mode"):
                v[c][k] = v[c][a - 1]
    v["lost"] = lost
    return v


def statements(dayrec, days):
    """Day-ahead settlement statement lines for each operating day with day-ahead awards: the initial statement two
    days after the operating day and the final thirty-one days after, as far as the pull. MPI's sign: positive is a
    charge to the QSE, negative a payment to it. The administrative fee is computed for the operating day on all its
    day-ahead energy."""
    byday = {x["day"]: x for x in days}
    rows = []
    for d, r in sorted(dayrec.items()):
        if r["status"] != "cycle" or d < W.OPS_FIRST:
            continue
        x = byday[d]
        for stype, lag in (("INITIAL", INITIAL_LAG), ("FINAL", FINAL_LAG)):
            issue = d + dt.timedelta(days=lag)
            if issue > W.SETTLE_PULL:
                continue
            sp_name = W.NODE if issue >= W.NODE_RENAME else W.NODE_OLD
            sid = "DAM%s%s%s" % (d.strftime("%y%m%d"), "I" if stype == "INITIAL" else "F", W.RESOURCE[-4:])
            mwh_day = round(4 * r["chg_mw"] + 4 * r["dis_mw"], 1)
            for i, (hr, p) in enumerate(zip(x["hours"], x["node_pub"])):
                price = float(p)
                if stype == "INITIAL" and d in REPRICED and i in r["dis"]:
                    price = round(price * REPRICED[d], 2)
                base = dict(statement_id=sid, statement_type=stype, issue_date=issue, operating_date=d,
                            hour_ending=hr[0], repeated_hour=hr[1], resource=W.RESOURCE, settlement_point=sp_name)
                if i in r["dis"]:
                    rows.append(dict(base, charge_type="DAES", mwh=r["dis_mw"], price=price,
                                     amount=round(-r["dis_mw"] * price, 2)))
                if i in r["chg"]:
                    rows.append(dict(base, charge_type="DAEP", mwh=r["chg_mw"], price=price,
                                     amount=round(r["chg_mw"] * price, 2)))
                rows.append(dict(base, charge_type="DAAF", mwh=mwh_day, price=FEE, amount=round(mwh_day * FEE, 2)))
    return rows
